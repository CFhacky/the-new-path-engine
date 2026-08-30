#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
whfb_wargame_harvest.py  --  THE NEW PATH ENGINE reference-layer harvester.

Extracts UNIT PROFILES (characteristic lines) and their explicit SPECIAL RULES
sections from born-digital Warhammer Fantasy Battle *tabletop wargame* army
books plus explicitly bounded, page-image-verified vision batches, and writes:
    reference/whfb_wargame_index.json
    reference/whfb_wargame_index.md

This is the WARGAME (Warhammer Fantasy Battle miniatures game), DISTINCT from the
Warhammer Fantasy Roleplay (WFRP) line, which is a separate index.
Every emitted row carries  "system": "WHFB".

WHFB profile schema (single digits; Ld up to 10; '-' or '*' allowed):
    M WS BS S T W I A Ld
    (Movement, Weapon Skill, Ballistic Skill, Strength, Toughness, Wounds,
     Initiative, Attacks, Leadership)
A datasheet usually prints several profile lines (unit + champion + mount/monster).
8th-ed books also print a Troop Type (Infantry/Cavalry/Monster/Chariot/...) either
as a "TROOP TYPE:" line beneath the profile block (bestiary entries) or as a
trailing text column after Ld (army-list summary). Both are captured when present.
The unit's book-raw SPECIAL RULES block is attached by same-column geometry,
explicit subject heading, or the summary table's printed Page reference plus an
exact name occurrence; ambiguous links remain named NO COVERAGE gaps.

Technique (geometric grid reconstruction, PyMuPDF "words" mode) -- mirrors the
sibling wh40k_wargame_harvest.py:
  1. Cluster words into visual rows by y (gap-based single linkage).
  2. A HEADER row = the longest contiguous run of characteristic-label tokens
     actually present (M WS BS S T W I A Ld). The header is read LIVE -- never
     hard-coded -- so a book that adds/omits a column still parses.
  3. Each value row below maps its stat tokens to the nearest header column by
     x-centre. Names in these books are laid out glyph-by-glyph (no space chars
     in the content stream), so the unit name is reconstructed from the contiguous
     glyph cluster left of the first stat column, inserting spaces at word-gaps.

Officialness: the OFFICIAL Games Workshop 8th-ed army books are born-digital with
a clean vector text layer. Several other born-digital files are fan-made/unofficial
(filenames carrying '9th', 'PDF Room', 'pdf-free', 'v1.2x', 'derevision', or a 40K
'Black Legion' misfile) -- these are classified DIGITAL-UNOFFICIAL and skipped so a
fan stat is never silently passed as an official one. The 1994 4th-ed Chaos book is
born-digital by char-count but its font/CMap is broken: the characteristic DIGITS
are corrupted in the text layer (a '4' extracts as '-j'/'~'), so it is caught by a
token-corruption gate and reported as NO COVERAGE rather than fabricating numbers
(Inviolable Rule 1). Core rulebooks are skipped by policy (rules, not a roster).

Stdlib + PyMuPDF (fitz) only. No cross-imports. Does NOT run git.
"""

import sys
import os
import re
import json
import math
import hashlib
import statistics

try:
    import fitz  # PyMuPDF
except Exception as e:  # pragma: no cover
    sys.stderr.write("FATAL: PyMuPDF (fitz) is required: %s\n" % e)
    raise

# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------
SRC_DIRS = [
    r"I:\Sourcebooks\Warhammer\Fantasy\Armybooks",
    r"I:\Sourcebooks\Warhammer\Fantasy Army Books",
]

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
OUT_JSON = os.path.join(_ROOT, "reference", "whfb_wargame_index.json")
OUT_MD = os.path.join(_ROOT, "reference", "whfb_wargame_index.md")

PROGRESS = (r"C:\Users\Chad\AppData\Local\Temp\claude"
            r"\I--repos-the-new-path-engine--claude-worktrees-intelligent-lamport-3a158a"
            r"\1c5f36b4-d94a-4698-95d9-c2304f8a0818\scratchpad"
            r"\whfb_wargame_progress.json")

SYSTEM = "WHFB"

# Bounded vision batch: this official 8th-edition scan has no text layer at all.
# Exactly one rendered roster page was read at 3x and verified directly against
# the page image.  The remaining pages stay explicit NO COVERAGE.
VISION_HIGH_ELVES_STEM = "Armybook_8ed - High Elves"
VISION_HIGH_ELVES_PDF_PAGE = 91
VISION_HIGH_ELVES_PRINTED_PAGE = 92
VISION_HIGH_ELVES_SHA256 = (
    "43e54b9b3b52d363708a823287d87fd439c4e0038de3ab20393455f5cb22056b")

# ----------------------------------------------------------------------------
# Label vocabulary (lower-cased keys) -- WHFB characteristic line
# ----------------------------------------------------------------------------
CANON = {
    "m": "M", "ws": "WS", "bs": "BS", "s": "S", "t": "T", "w": "W",
    "i": "I", "a": "A", "ld": "Ld", "ld.": "Ld", "l.d": "Ld", "ld,": "Ld",
    # not part of the M..Ld line but occasionally seen adjacent -> dropped
    "pts": "Points", "points": "Points", "page": "Page",
}
LABELS = set(CANON.keys())
# "strong" labels almost never occur as prose -> used to qualify a header row.
STRONG = {"ws", "bs", "ld", "ld.", "l.d", "ld,"}
# columns that are not game characteristics -> dropped from the emitted profile
# (kept during mapping so their values do not pollute a real column).
DROP_LABELS = {"Points", "Page"}

# The nine real characteristics, in canonical order (for the selftest + docs).
WHFB_STATS = ["M", "WS", "BS", "S", "T", "W", "I", "A", "Ld"]

# A value cell: only digits/dashes/star/parens/plus/slash/dot with at least one
# digit, OR a lone dash, OR a lone star, OR a random-movement die (2D6/D6/3D6).
_VALCHARS = set("0123456789()+-/.*\u2013\u2014")
_DASHES = {"-", "\u2013", "\u2014"}
_STARS = {"*"}
_DICE_RE = re.compile(r"^\d*[dD]\d+$")


def is_value(tok):
    if tok in _DASHES or tok in _STARS:
        return True
    if not tok:
        return False
    if _DICE_RE.match(tok):
        return True
    if not set(tok) <= _VALCHARS:
        return False
    return any(c.isdigit() for c in tok)


def has_alpha(tok):
    return any(c.isalpha() for c in tok)


# ----------------------------------------------------------------------------
# PDF helpers
# ----------------------------------------------------------------------------
def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def avg_chars_per_page(doc, sample=12):
    n = doc.page_count
    if n <= 0:
        return 0.0
    if n == 1:
        idxs = [0]
    else:
        idxs = sorted(set(int(round(k * (n - 1) / (sample - 1))) for k in range(sample)))
    tot = 0
    for i in idxs:
        tot += len(doc[i].get_text("text"))
    return tot / float(len(idxs))


def is_digital(doc):
    return avg_chars_per_page(doc) > 400.0


# The mangled-encoding signature: fraction of alpha-bearing tokens that also
# carry a junk glyph (backslash / caret / tilde / pipe / backtick).  Clean GW
# books score ~0.0-0.2%; the broken 1994 Chaos book scores ~2.7%.
_JUNK = set("\\~^`|")


def junk_alpha_fraction(doc, sample=16):
    n = doc.page_count
    if n <= 0:
        return 0.0
    if n == 1:
        idxs = [0]
    else:
        idxs = sorted(set(int(round(k * (n - 1) / (sample - 1))) for k in range(sample)))
    alpha = 0
    junky = 0
    for i in idxs:
        for w in doc[i].get_text("words"):
            t = (w[4] or "").strip()
            if not t or not any(c.isalpha() for c in t):
                continue
            alpha += 1
            if any(c in _JUNK for c in t):
                junky += 1
    return (junky / float(alpha)) if alpha else 0.0


CORRUPTION_THRESHOLD = 0.015  # 1.5% junk-alpha tokens -> broken text layer


def cluster_rows(words, ygap=4.0):
    """Group words into visual rows using a y-centre gap threshold."""
    items = []
    for w in words:
        x0, y0, x1, y1, txt = w[0], w[1], w[2], w[3], w[4]
        if txt is None or txt.strip() == "":
            continue
        items.append((0.5 * (y0 + y1), x0, x1, txt.strip()))
    items.sort(key=lambda r: (r[0], r[1]))
    rows = []
    cur = []
    last_y = None
    for yc, x0, x1, txt in items:
        if last_y is None or (yc - last_y) <= ygap:
            cur.append((yc, x0, x1, txt))
        else:
            rows.append(cur)
            cur = [(yc, x0, x1, txt)]
        last_y = yc
    if cur:
        rows.append(cur)
    out = []
    for r in rows:
        r = sorted(r, key=lambda t: t[1])
        ry = statistics.median([t[0] for t in r])
        out.append((ry, r))
    return out


def merge_touching(row_tokens, gap=2.5):
    """
    Merge horizontally touching single-glyph tokens of the SAME kind -- used only
    for header label reconstruction (e.g. a split 'W'+'S' glyph -> 'WS').  Never
    merges a word with an adjacent value digit.
    """
    if not row_tokens:
        return []
    merged = [list(row_tokens[0])]  # [yc, x0, x1, txt]
    for tok in row_tokens[1:]:
        prev = merged[-1]
        both_single = len(prev[3]) == 1 and len(tok[3]) == 1
        same_kind = (is_value(prev[3]) == is_value(tok[3]))
        if both_single and same_kind and (tok[1] - prev[2]) < gap:
            prev[2] = tok[2]
            prev[3] = prev[3] + tok[3]
        else:
            merged.append(list(tok))
    return [(t[0], t[1], t[2], t[3]) for t in merged]


# ----------------------------------------------------------------------------
# Name / heading reconstruction (glyph-by-glyph text layers)
# ----------------------------------------------------------------------------
NAME_SPACE = 2.8     # gap (px) above which a space is inserted between glyphs
NAME_BRIDGE = 14.0   # max gap (px) still counted inside one name cluster
NAME_NEAR = 88.0     # rightmost name glyph must sit within this of the 1st column


def reconstruct(tokens, space=NAME_SPACE):
    """
    tokens: list of (x0, x1, txt) left->right. Re-join text the PDF laid out
    glyph-by-glyph, inserting a space where the horizontal gap widens past
    `space`.  In some books word-gaps are only weakly larger than letter-gaps,
    so this errs toward joining (a jammed name is preferable to a mid-word split);
    the clean ALL-CAPS heading is captured separately as unit_context.
    """
    s = ""
    prev_x1 = None
    for (x0, x1, txt) in tokens:
        if prev_x1 is not None and (x0 - prev_x1) > space:
            s += " "
        s += txt
        prev_x1 = x1
    return s


_LEAD_JUNK = set("\u2022*^;:~`|\"'\u2013\u2014.,�<>()[]{}=+/\\_")


def clean_name(name):
    """Trim decorative drop-cap / bullet glyphs and stray punctuation."""
    if not name:
        return ""
    name = name.replace("\u2019", "'").replace("\u2018", "'")
    name = re.sub(r"\s+", " ", name).strip()
    # strip a leading decorative token: a short lead (a lone glyph, or a
    # punctuation+glyph pair) followed by a space and then a real word -- e.g.
    # "I Dragon Ogre...", "-I Steed...", "J Kroak".  WHFB unit names never begin
    # with a standalone one/two-character word, so this is safe.
    for _ in range(3):
        m = re.match(r"^(\S{1,2})\s+(\S.*)$", name)
        if not m:
            break
        head, rest = m.group(1), m.group(2).strip()
        if len(rest) < 3 or not has_alpha(rest):
            break
        # drop a 1-char lead, or a 2-char lead that is not itself a real word
        if len(head) == 1 or not head.isalpha():
            name = rest
            continue
        break
    # strip leading/trailing junk chars (incl. a bullet hyphen; internal hyphens
    # in names like "Kroq-Gar" are preserved since strip() only trims the ends)
    name = name.strip("".join(_LEAD_JUNK) + " -")
    # strip a leading decorative capital glued to a Title-case word (a drop-cap
    # bar read as a letter): "ISaurus Warrior" -> "Saurus Warrior", "ITroglodon"
    # -> "Troglodon".  A real initial is followed by a lower-case letter
    # ("Ironbreaker", "Kroxigor") and is left intact.
    m = re.match(r"^[A-Z]([A-Z][a-z]{2,}.*)$", name)
    if m:
        name = m.group(1)
    # These books space names weakly (word-gaps ~= letter-gaps), so many names
    # extract jammed.  WHFB unit names never contain an intra-word capital, so a
    # lower->UPPER boundary is always a lost word break: "SkeletonWarrior" ->
    # "Skeleton Warrior", "ChaosWarrior" -> "Chaos Warrior".  Also re-space a
    # lower-case connector that stayed glued to the preceding word.
    name = re.sub(r"([a-z])([A-Z])", r"\1 \2", name)
    # re-space a lower-case connector left glued to the word before it once
    # camelCase has separated the following word ("Juggernautof Khorne" ->
    # "Juggernaut of Khorne", "Vilitchthe Curseling" -> "Vilitch the Curseling",
    # "Keeperofthe Gate" -> "Keeper of the Gate").  The connector must be followed
    # by a space, so it can't bite into words like Glade / Skarbrand / Scythe.
    name = re.sub(r"([a-z])ofthe\b", r"\1 of the", name)
    name = re.sub(r"\bofthe\b", "of the", name)
    name = re.sub(r"([a-z])(of|von|the) ", r"\1 \2 ", name)
    name = re.sub(r"\s+", " ", name).strip()
    if " " in name:  # drop a dangling connector left when the trailing word was cut
        name = re.sub(r"(?<=[a-z])(of|the|von)$", "", name).strip()
    return name


def parse_name(rtoks, first_xc, col_gap):
    """
    Reconstruct the unit name: the contiguous glyph cluster immediately left of
    the first stat column.  These books position each glyph separately, so we
    gather every alpha/name-ish token left of the stat block and keep the tight
    run ending nearest the values, then re-insert spaces at word-gaps.
    """
    stat_left = first_xc - 0.5 * col_gap
    cand = []
    for (yc, x0, x1, txt) in rtoks:
        if x1 <= stat_left - 1.0 and (has_alpha(txt) or txt in ("-", "'", "&")
                                      or txt.startswith("(") or txt.endswith(")")):
            cand.append((x0, x1, txt))
    if not cand:
        return ""
    cand.sort(key=lambda c: c[0])
    # rightmost token must sit reasonably close to the stat block
    if 0.5 * (cand[-1][0] + cand[-1][1]) < first_xc - NAME_NEAR:
        return ""
    kept = [cand[-1]]
    for i in range(len(cand) - 2, -1, -1):
        gap = kept[0][0] - cand[i][1]
        if gap <= NAME_BRIDGE:
            kept.insert(0, cand[i])
        else:
            break
    name = reconstruct(kept)
    return clean_name(name)


def reconstruct_full_row(rtoks, space=NAME_SPACE):
    """Whole-row text (for TROOP TYPE / heading detection)."""
    return reconstruct([(x0, x1, txt) for (yc, x0, x1, txt) in rtoks], space)


# ----------------------------------------------------------------------------
# Header detection & normalisation
# ----------------------------------------------------------------------------
def longest_label_run(tokens):
    """Return (start, end) of the longest contiguous run of LABEL tokens."""
    best = (0, 0, 0)
    i = 0
    n = len(tokens)
    while i < n:
        if tokens[i].lower() in LABELS:
            j = i
            while j < n and tokens[j].lower() in LABELS:
                j += 1
            if (j - i) > best[0]:
                best = (j - i, i, j)
            i = j
        else:
            i += 1
    return best[1], best[2]


def densest_subrun(run):
    """
    run: list of (xc, raw).  Stat columns are evenly spaced (~12-16px); a stray
    prose single-letter label sits far from the real block.  Split the run at
    outsized gaps and keep the longest sub-run.
    """
    if len(run) <= 1:
        return run
    xcs = [xc for xc, _ in run]
    gaps = [xcs[i + 1] - xcs[i] for i in range(len(xcs) - 1)]
    med = statistics.median(gaps)
    thresh = max(40.0, 2.5 * med)
    segments = []
    cur = [run[0]]
    for i, g in enumerate(gaps):
        if g > thresh:
            segments.append(cur)
            cur = [run[i + 1]]
        else:
            cur.append(run[i + 1])
    segments.append(cur)
    segments.sort(key=lambda s: (len(s), s[-1][0] - s[0][0]), reverse=True)
    return segments[0]


def _merge_split_labels(run):
    """
    Some books render the two-letter labels WS / BS as two half-spaced glyphs
    ('W'+'S', 'B'+'S') sitting ~half a column apart, which would otherwise become
    two phantom columns.  Merge an adjacent W|B followed by S when their centres
    are much closer than the median column spacing.
    """
    if len(run) < 3:
        return run
    xcs = [xc for xc, _ in run]
    gaps = [xcs[i + 1] - xcs[i] for i in range(len(xcs) - 1)]
    med = statistics.median(gaps)
    out = []
    i = 0
    while i < len(run):
        xc, lab = run[i]
        if i + 1 < len(run):
            xc2, lab2 = run[i + 1]
            if lab.lower() in ("w", "b") and lab2.lower() == "s" \
                    and (xc2 - xc) < 0.7 * med:
                out.append((0.5 * (xc + xc2), lab + lab2))
                i += 2
                continue
        out.append((xc, lab))
        i += 1
    return out


def normalise_columns(run):
    """
    run: list of (xc, raw_label)  (the contiguous label run).
    Returns list of columns: [{"label":canon, "xc":float, "drop":bool}].
    """
    run = _merge_split_labels(run)
    cols = []
    seen = {}
    for xc, raw in run:
        lab = raw.lower()
        canon = CANON.get(lab, lab.upper())
        key = canon
        if canon in seen and canon not in DROP_LABELS:
            seen[canon] += 1
            key = "%s#%d" % (canon, seen[canon])
        else:
            seen.setdefault(canon, 1)
        cols.append({"label": key, "xc": xc, "drop": canon in DROP_LABELS})
    return cols


def trim_to_canonical(cols):
    """
    The WHFB characteristic header is the fixed sequence M WS BS S T W I A Ld.
    A stray decorative glyph (e.g. a drop-cap 'W'/'I' from adjacent flavour text)
    can slip into the label run at roughly column spacing and create a phantom
    column with a duplicated label.  If the canonical 9-stat sequence appears as
    a contiguous window, lock onto it and drop the strays; otherwise leave the
    live-read columns untouched (a genuinely non-standard table still parses).
    """
    bases = [c["label"].split("#")[0] for c in cols]
    L = len(WHFB_STATS)
    if bases == WHFB_STATS:
        return cols
    for s in range(0, len(cols) - L + 1):
        if bases[s:s + L] == WHFB_STATS:
            win = cols[s:s + L]
            return [{"label": WHFB_STATS[k], "xc": win[k]["xc"], "drop": False}
                    for k in range(L)]
    return cols


def find_headers(rows):
    """rows: list of (ry, row_tokens). Returns list of header dicts."""
    headers = []
    for ry, rtoks in rows:
        mtoks = merge_touching(rtoks)
        toks = [t[3] for t in mtoks]
        a, b = longest_label_run(toks)
        if b - a < 4:
            continue
        run = mtoks[a:b]
        strong = sum(1 for t in run if t[3].lower() in STRONG)
        if strong < 2:
            continue
        run_xc = densest_subrun([(0.5 * (t[1] + t[2]), t[3]) for t in run])
        if len(run_xc) < 4:
            continue
        cols = normalise_columns(run_xc)
        cols = trim_to_canonical(cols)
        real = [c for c in cols if not c["drop"]]
        if len(real) < 3:
            continue
        # reject a malformed header that still carries a duplicated characteristic
        # label (e.g. a glyph mis-render that split/duplicated a column): WHFB
        # never repeats a stat, so such a header would only produce garbage rows.
        bases = [c["label"].split("#")[0] for c in real]
        if len(set(bases)) != len(bases):
            continue
        headers.append({"y": ry, "cols": cols})
    headers.sort(key=lambda h: h["y"])
    return headers


FURNITURE = {"bestiary", "army", "armies", "warhammer", "lords", "heroes",
             "core", "special", "rare", "the", "points", "summary", "reference",
             "contents", "units", "unit", "characters", "monsters", "and", "of"}


def heading_above(rows, header_y, page_h):
    """
    Best-effort datasheet title (captured as unit_context).  In the army-list
    summary each unit's name sits just above its profile; in the bestiary the
    ALL-CAPS datasheet title sits at the top of the page, far above.  So we take
    the nearest qualifying title within ~200px, else the page-top title.
    """
    cands = []
    for ry, rtoks in rows:
        if ry >= header_y - 2 or (header_y - ry) > 0.9 * page_h:
            continue
        letters = "".join(c for t in rtoks for c in t[3] if c.isalpha())
        if len(letters) < 4:
            continue
        if sum(1 for c in letters if c.isupper()) / len(letters) < 0.72:
            continue
        txt = reconstruct_full_row(rtoks)
        txt = re.sub(r"\s*\d+\s*point.*$", "", txt, flags=re.I).strip()
        txt = clean_name(txt)
        low = txt.lower()
        if not (2 <= len(txt) <= 44):
            continue
        if low in FIELD_LABELS or all(w in FURNITURE for w in low.split()):
            continue
        cands.append((ry, txt))
    if not cands:
        return None
    near = [c for c in cands if (header_y - c[0]) <= 200]
    if near:
        return max(near, key=lambda c: c[0])[1]   # nearest above
    return min(cands, key=lambda c: c[0])[1]        # page-top title


# ----------------------------------------------------------------------------
# Value-row parsing
# ----------------------------------------------------------------------------
FIELD_LABELS = {
    "troop type", "special rules", "magic", "magic items", "options", "equipment",
    "mount", "unit strength", "points", "wargear", "special rule", "composition",
    "unit size", "base size", "type", "profile", "profiles", "lore",
}

TROOP_TYPE_RE = re.compile(r"troop\s*type\s*:?\s*(.+)", re.I)
# recognised troop-type keywords (for the inline trailing column)
TROOP_KEYWORDS = ("infantry", "cavalry", "monstrous", "monster", "chariot",
                  "war beast", "warbeast", "beast", "swarm", "unique", "character",
                  "behemoth", "war machine", "warmachine", "flying")


def clean_troop_type(txt):
    """Trim a troop-type phrase to its leading clause (before any trailing prose)."""
    if not txt:
        return None
    txt = re.sub(r"\s+", " ", txt).strip()
    txt = txt.split(".")[0].strip(" .,:")   # cut trailing sentence/prose
    txt = re.sub(r"\s*\([^)]*$", "", txt).strip()  # drop an unclosed paren tail
    if 2 <= len(txt) <= 48 and has_alpha(txt):
        return txt
    return None


def parse_troop_type_inline(rtoks, cols):
    """Trailing text column to the RIGHT of the last stat column -> troop type."""
    last_xc = max(c["xc"] for c in cols)
    col_gap = _median_col_gap(cols)
    tail = [(x0, x1, txt) for (yc, x0, x1, txt) in rtoks
            if (0.5 * (x0 + x1)) > last_xc + 0.6 * col_gap and has_alpha(txt)]
    if not tail:
        return None
    tail.sort(key=lambda c: c[0])
    txt = reconstruct(tail).strip()
    low = txt.lower()
    if any(k in low for k in TROOP_KEYWORDS):
        return clean_troop_type(txt)
    return None


def _median_col_gap(cols):
    xcs = sorted(c["xc"] for c in cols)
    gaps = [xcs[i + 1] - xcs[i] for i in range(len(xcs) - 1)]
    return statistics.median(gaps) if gaps else 14.0


def extract_glyphs(rtoks, cols):
    """Ordered value glyphs inside the stat-block x-window (unmerged)."""
    xcs = [c["xc"] for c in cols]
    med = _median_col_gap(cols)
    lo = min(xcs) - 0.75 * med
    hi = max(xcs) + 0.75 * med
    vals = []
    for (yc, x0, x1, txt) in rtoks:
        if not is_value(txt):
            continue
        xc = 0.5 * (x0 + x1)
        if xc < lo or xc > hi:
            continue
        vals.append([x0, x1, txt])
    vals.sort(key=lambda v: v[0])
    return vals


def _implausible(profile):
    """
    Count clearly-impossible cells in a candidate profile.  Used ONLY to choose
    between competing digit-GROUPINGS of the very same PDF glyphs (never to alter
    a digit): a WHFB characteristic is a single digit 0-10, Leadership is never 0,
    and no M..Ld value is a 3-digit number.  A split two-digit value that has been
    mis-grouped shows up here as e.g. Ld '0' or A '11'/'22'.
    """
    bad = 0
    for k, v in profile.items():
        base = k.split("#")[0]
        if v in ("-", "*") or not v:
            continue
        if v.isdigit():
            iv = int(v)
            if len(v) >= 3 or iv > 16:
                bad += 1
            elif base == "Ld" and iv == 0:
                bad += 1
    return bad


def _positional_profile(vals, real_cols):
    return {c["label"]: v[2] for c, v in zip(real_cols, vals)}


def _combine(a, b):
    return [a[0], b[1], a[2] + b[2]]


def parse_value_row(rtoks, cols):
    """Map a value row to columns. Returns (name, profile_dict, troop_inline, soft)."""
    real_idx = [i for i, c in enumerate(cols) if not c["drop"]]
    real_cols = [cols[i] for i in real_idx]
    ncols = len(real_cols)
    xcs = [c["xc"] for c in cols]
    first_xc = min(xcs)
    med = _median_col_gap(cols)
    tol = max(5.0, 0.6 * med)

    name = parse_name(rtoks, first_xc, med)
    if not name or not has_alpha(name) or len(name.strip(" '\"()-&.")) < 2:
        return None
    if name.endswith(":") or name.strip().lower() in FIELD_LABELS:
        return None
    if name.lower() in LABELS:
        return None
    lead = name.lstrip("'\"([")[:1]
    if lead.isalpha() and not lead.isupper():
        return None  # lower-case lead == flowing prose, not a datasheet name

    glyphs = extract_glyphs(rtoks, cols)
    merge_cap = 0.55 * med
    soft = None
    profile = {}

    def ends_aligned(vals):
        if len(vals) != ncols or ncols < 3:
            return False
        l = abs(0.5 * (vals[0][0] + vals[0][1]) - real_cols[0]["xc"]) <= 2.5 * tol
        r = abs(0.5 * (vals[-1][0] + vals[-1][1]) - real_cols[-1]["xc"]) <= 2.5 * tol
        return l and r

    n = len(glyphs)
    if n == ncols and ends_aligned(glyphs):
        profile = _positional_profile(glyphs, real_cols)
    elif n == ncols + 1:
        # exactly one split multi-digit value: try each tight adjacent merge and
        # keep the grouping that yields the most plausible profile (fewest
        # impossible cells), breaking ties by the tightest merged gap.
        best = None
        for gi in range(n - 1):
            gap = glyphs[gi + 1][0] - glyphs[gi][1]
            if gap >= merge_cap:
                continue
            cand = glyphs[:gi] + [_combine(glyphs[gi], glyphs[gi + 1])] + glyphs[gi + 2:]
            if not ends_aligned(cand):
                continue
            prof = _positional_profile(cand, real_cols)
            key = (_implausible(prof), gap)
            if best is None or key < best[0]:
                best = (key, prof)
        if best is not None:
            profile = best[1]
            if best[0][0] > 0:
                soft = "ambiguous digit grouping (two-digit value split across glyphs)"
        # else: fall through to nearest-x below
    if not profile:
        # partial / irregular / stray-token row -> nearest-column mapping,
        # concatenating glyphs that share a nearest column (handles split digits).
        buckets = {}
        for (x0, x1, txt) in glyphs:
            xc = 0.5 * (x0 + x1)
            j = min(range(len(xcs)), key=lambda k: abs(xcs[k] - xc))
            if abs(xcs[j] - xc) > tol:
                continue
            buckets.setdefault(j, []).append((x0, x1, txt))
        for j, toks in buckets.items():
            if cols[j]["drop"]:
                continue
            toks.sort()
            val = "".join(t[2] for t in toks)
            profile[cols[j]["label"]] = val
            if len(toks) > 1:
                # tightly-packed digits are one split multi-digit value (e.g. a
                # column showing 10); a wide internal gap means two different
                # values genuinely collided -> flag the row soft.
                wide = max(toks[k + 1][0] - toks[k][1]
                           for k in range(len(toks) - 1)) >= merge_cap
                if wide or not val.lstrip("-").isdigit():
                    soft = "column collision (ambiguous x-mapping)"

    need = max(3, math.ceil(ncols / 2.0))
    if len(profile) < need:
        return None

    # A WHFB characteristic is a single digit 0-10 (or '-'/'*'); a 3-digit number,
    # a value > 16, or Leadership 0 can only be glyph-merge corruption from a
    # messy summary table.  We refuse to emit a fabricated-looking number
    # (Inviolable Rule 1) -- the same unit is captured cleanly from its bestiary
    # entry, so drop the corrupted row rather than guess.
    for k, v in profile.items():
        if v.isdigit() and (len(v) >= 3 or int(v) > 16):
            return None
        if k.split("#")[0] == "Ld" and v == "0":
            return None

    troop_inline = parse_troop_type_inline(rtoks, cols)
    return name, profile, troop_inline, soft


def is_garbled(name):
    """A real WHFB unit name is letters/space/apostrophe/hyphen only, and any
    hyphen joins two capitalised parts (Kroq-Gar, Ceithin-Har).  A replacement
    glyph, stray punctuation, doubled/edge hyphen, or hyphen-then-lower-case is
    decorative-title-font corruption."""
    return bool(re.search(r"[^A-Za-z '\-]", name)
                or re.search(r"--|-\s|\s-|-[a-z]", name))


def titlecase_heading(s):
    small = {"of", "the", "and", "von", "de", "a"}
    out = []
    for i, w in enumerate(s.split()):
        wl = w.lower()
        out.append(wl if (wl in small and i > 0) else (wl[:1].upper() + wl[1:]))
    return " ".join(out)


def resolve_garbled(rows_out, soft_out):
    """
    Rescue rows whose inline name came out mangled by a broken decorative font:
    if a clean-named row with the identical profile already exists in this book,
    drop the mangled duplicate; otherwise fall back to the clean ALL-CAPS
    datasheet heading (unit_context) as the name; if neither works, drop the row.
    """
    clean_profiles = set()
    for r in rows_out:
        if not is_garbled(r["name"]):
            clean_profiles.add(tuple(sorted(r["profile"].items())))
    kept = []
    dropped_cites = set()
    for r in rows_out:
        if is_garbled(r["name"]):
            pk = tuple(sorted(r["profile"].items()))
            ctx = r.get("unit_context")
            if pk in clean_profiles:
                dropped_cites.add(r["citation"])
                continue
            if ctx and not is_garbled(ctx):
                r["name"] = titlecase_heading(ctx)
            else:
                dropped_cites.add(r["citation"])
                continue
        kept.append(r)
    soft_out[:] = [s for s in soft_out if s["citation"] not in dropped_cites]
    return kept


# Structural labels that end a unit's special-rules area.  Named rule
# paragraphs are retained only when their heading ends in a colon; this keeps
# adjacent lore/quotation boxes out of the mechanical reference layer.
_RULE_STOP_PREFIXES = (
    "ARMY SPECIAL RULES", "TROOP TYPE", "MAGIC", "EQUIPMENT", "OPTIONS",
    "UNIT SIZE", "PROFILE", "MOUNTS", "MAGIC ITEMS", "WEAPONS", "ARMOUR",
    "UPGRADE", "UPGRADES", "POINTS",
)
_RULE_STOP_KEYS = tuple(
    re.sub(r"[^A-Z0-9]+", "", prefix) for prefix in _RULE_STOP_PREFIXES)
_RULE_TITLE_RE = re.compile(
    r"^[A-Z][A-Za-z0-9'’+() /-]{1,80}:\s+\S")
_SPECIAL_RULES_RE = re.compile(
    r"S\s*P\s*E\s*C\s*I\s*A\s*L\s+R\s*U\s*L\s*E\s*S"
    r"(?:\s*\(([^)]+)\))?\s*:",
    re.I)


def _clean_rule_block(text):
    """Collapse PDF display line-wraps without rewriting any book wording."""
    return " ".join(line.strip() for line in text.splitlines() if line.strip())


def _label_x(rtoks, label):
    """Find a whole-word or glyphwise display label and return its x-centre."""
    wanted = label.lower()
    for i in range(len(rtoks)):
        joined = ""
        x0 = rtoks[i][1]
        for j in range(i, min(len(rtoks), i + len(label) + 1)):
            joined += re.sub(r"[^A-Za-z]", "", rtoks[j][3]).lower()
            if joined == wanted:
                return 0.5 * (x0 + rtoks[j][2])
            if not wanted.startswith(joined):
                break
    return None


def page_reference_hint(rows, header, value_toks, page_count, page_width):
    """Read an army-list summary's printed Page column, when present."""
    mid = page_width / 2.0
    hc = sum(c["xc"] for c in header["cols"]) / float(len(header["cols"]))
    right = hc >= mid
    header_toks = None
    for ry, rtoks in rows:
        if abs(ry - header["y"]) <= 2.0:
            header_toks = [
                t for t in rtoks
                if ((0.5 * (t[1] + t[2]) >= mid) == right)
            ]
            break
    if not header_toks:
        return None
    page_x = _label_x(header_toks, "Page")
    if page_x is None or page_x <= header["cols"][-1]["xc"]:
        return None

    candidates = []
    for _yc, x0, x1, txt in value_toks:
        raw = txt.strip()
        xc = 0.5 * (x0 + x1)
        if raw.isdigit() and 1 <= int(raw) <= page_count:
            candidates.append((abs(xc - page_x), int(raw)))
    candidates.sort()
    if candidates and candidates[0][0] <= 14.0:
        return candidates[0][1]
    return None


def _label_xs(rtoks, label):
    """Return every x-centre for a whole-word or glyphwise display label."""
    wanted = label.lower()
    out = []
    for i in range(len(rtoks)):
        joined = ""
        x0 = rtoks[i][1]
        for j in range(i, min(len(rtoks), i + len(label) + 1)):
            joined += re.sub(r"[^A-Za-z]", "", rtoks[j][3]).lower()
            if joined == wanted:
                out.append(0.5 * (x0 + rtoks[j][2]))
                break
            if not wanted.startswith(joined):
                break
    return out


def summary_reference_map(doc):
    """Read exact unit -> bestiary-page links from army-list summary tables."""
    found = {}
    for pi in range(doc.page_count):
        rows = cluster_rows(doc[pi].get_text("words"))
        headers = []
        for ri, (ry, rtoks) in enumerate(rows):
            page_xs = _label_xs(rtoks, "Page")
            for page_x in page_xs:
                previous = [x for x in page_xs if x < page_x]
                lower = max(previous) + 12.0 if previous else 0.0
                m_xs = [
                    0.5 * (t[1] + t[2]) for t in rtoks
                    if lower < 0.5 * (t[1] + t[2]) < page_x
                    and re.sub(r"[^A-Za-z]", "", t[3]).lower() == "m"
                ]
                if m_xs:
                    headers.append((ri, ry, page_x, lower, max(m_xs)))

        for ri, hy, page_x, lower, m_x in headers:
            next_y = min([
                h[1] for h in headers
                if h[1] > hy + 2.0 and abs(h[2] - page_x) < 20.0
            ] + [1e9])
            med = max(8.0, min(24.0, (page_x - m_x) / 10.0))
            for ry, rtoks in rows[ri + 1:]:
                if ry >= next_y - 1.0 or ry - hy > 180.0:
                    break
                segment = [
                    t for t in rtoks
                    if lower < 0.5 * (t[1] + t[2]) < page_x + 12.0
                ]
                values = []
                for t in segment:
                    raw = t[3].strip()
                    xc = 0.5 * (t[1] + t[2])
                    if (raw.isdigit() and 1 <= int(raw) <= doc.page_count
                            and abs(xc - page_x) <= 14.0):
                        values.append((abs(xc - page_x), int(raw)))
                if not values:
                    continue
                name = parse_name(segment, m_x, med)
                if name and has_alpha(name):
                    found.setdefault(_norm_name(name), set()).add(
                        min(values)[1])
    return found


def extract_special_rules(page, header, headers):
    """Return the explicit SPECIAL RULES block for one geometric profile grid.

    WHFB bestiary pages place the characteristic grid and its rules in the same
    half-page column.  Matching by both column and vertical order prevents a
    neighbouring unit's rules from being attached on two-unit pages.
    """
    mid = page.rect.width / 2.0
    hcentre = sum(c["xc"] for c in header["cols"]) / float(len(header["cols"]))
    right = hcentre >= mid
    clip = fitz.Rect(mid if right else 0.0, 0.0,
                     page.rect.width if right else mid, page.rect.height)

    later_headers = []
    for other in headers:
        if other["y"] <= header["y"] + 2.0:
            continue
        oc = sum(c["xc"] for c in other["cols"]) / float(len(other["cols"]))
        if (oc >= mid) == right:
            later_headers.append(other["y"])
    stop_y = min(later_headers + [page.rect.height + 1.0])

    blocks = []
    for b in page.get_text("blocks", clip=clip, sort=True):
        txt = _clean_rule_block(b[4])
        if txt:
            blocks.append((float(b[1]), float(b[3]), txt))

    candidates = []
    for bi, (y0, y1, txt) in enumerate(blocks):
        if y0 < header["y"] - 5.0 or y0 >= stop_y:
            continue
        m = _SPECIAL_RULES_RE.search(txt)
        if m:
            candidates.append((y0, bi, m.start()))
    if not candidates:
        return None

    _y0, start_i, marker = min(candidates, key=lambda x: x[0])
    first = blocks[start_i][2][marker:].strip()
    if not first:
        return None
    pieces = [first]

    # Unique unit rules follow as titled paragraphs (for example,
    # "The Hunger: ...").  A PDF block normally holds the whole paragraph.
    # Unheaded prose, quotations, and decorative lore boxes are deliberately
    # excluded rather than guessed into a mechanical rule span.
    for y0, _y1, txt in blocks[start_i + 1:]:
        if y0 >= stop_y:
            break
        if _SPECIAL_RULES_RE.search(txt):
            break
        if not _RULE_TITLE_RE.match(txt):
            continue
        upper = txt.upper()
        compact = re.sub(r"[^A-Z0-9]+", "", upper)
        if any(compact.startswith(prefix) for prefix in _RULE_STOP_KEYS):
            break
        if upper.startswith("AND TO TELL OF "):
            continue
        pieces.append(txt)

    joined = "\n\n".join(pieces)
    marker_match = _SPECIAL_RULES_RE.search(joined)
    if marker_match is None:
        return None
    if not joined[marker_match.end():].strip() and len(pieces) == 1:
        return None
    return joined


def page_rule_catalog(page):
    """Return (profile-name set, rule text) pairs for one bestiary page."""
    rows = cluster_rows(page.get_text("words"))
    headers = find_headers(rows)
    catalog = []
    hys = [h["y"] for h in headers]
    for hi, h in enumerate(headers):
        rules = extract_special_rules(page, h, headers)
        if not rules:
            continue
        next_hy = hys[hi + 1] if hi + 1 < len(hys) else 1e9
        names = set()
        got = 0
        misses = 0
        for ry, rtoks in rows:
            if ry <= h["y"] + 1.0:
                continue
            if ry >= next_hy - 1.0 or ry - h["y"] > 320.0:
                break
            parsed = parse_value_row(rtoks, h["cols"])
            if parsed is None:
                if got:
                    misses += 1
                    if misses >= 3:
                        break
                continue
            misses = 0
            got += 1
            names.add(_norm_name(parsed[0]))
        catalog.append((names, rules))
    return catalog


def page_unanchored_catalog(page):
    """Collect (printed subject, rule text) without assuming a parsed grid."""
    found = []
    mid = page.rect.width / 2.0
    for right in (False, True):
        clip = fitz.Rect(mid if right else 0.0, 0.0,
                         page.rect.width if right else mid, page.rect.height)
        starts = []
        for b in page.get_text("blocks", clip=clip, sort=True):
            txt = _clean_rule_block(b[4])
            match = _SPECIAL_RULES_RE.search(txt)
            if match:
                starts.append((float(b[1]), (match.group(1) or "").strip()))
        fake_headers = [
            {"y": y - 1.0,
             "cols": [{"xc": (0.75 if right else 0.25) * page.rect.width}]}
            for y, _subject in starts
        ]
        for (start, subject), fake in zip(starts, fake_headers):
            txt = extract_special_rules(page, fake, fake_headers)
            if txt:
                found.append((subject, txt))
    unique = {}
    for subject, txt in found:
        unique.setdefault((subject, txt), None)
    return list(unique.keys())


def page_unanchored_rules(page):
    return sorted(set(txt for _subject, txt in page_unanchored_catalog(page)))


def _lookup_norm(text):
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def _subject_matches(subject, name):
    """Match an exact subject or one member of an explicit and/or list."""
    name_key = _lookup_norm(name)
    if not name_key:
        return False
    parts = re.split(r"\s+(?:and|or)\s+|[,/&]", subject, flags=re.I)
    return any(_lookup_norm(part) == name_key for part in parts)


def _page_mentions(page, name):
    return _lookup_norm(name) in _lookup_norm(page.get_text("text"))


def attach_rule_backfills(doc, rows, cite_book):
    """Use exact duplicate names and printed army-list page references safely."""
    exact = {}
    for row in rows:
        if row.get("special_rules"):
            key = _norm_name(row["name"])
            exact.setdefault(key, []).append(
                (row["special_rules"], list(row.get("rules_citations", []))))

    catalog_cache = {}
    loose_cache = {}
    summary_refs = summary_reference_map(doc)

    def loose_catalog(page_no):
        if page_no not in loose_cache:
            loose_cache[page_no] = page_unanchored_catalog(doc[page_no - 1])
        return loose_cache[page_no]

    for row in rows:
        if row.get("special_rules"):
            continue
        key = _norm_name(row["name"])
        options = exact.get(key, [])
        unique = {}
        for txt, cites in options:
            unique.setdefault(txt, cites)
        if len(unique) == 1:
            txt, cites = next(iter(unique.items()))
            row["special_rules"] = txt
            row["rules_citations"] = cites
            continue

        # Subject-qualified headings such as "SPECIAL RULES (Hound of
        # Orion):" are authoritative even when the profile grid is elsewhere
        # on the page.  An unqualified section is used only when it is the
        # page's sole section and the profile itself is cited to that page.
        mpage = re.search(r"\[PDF page (\d+)\]", row["citation"])
        direct_page = int(mpage.group(1)) if mpage else None
        if direct_page and 1 <= direct_page <= doc.page_count:
            direct_catalog = loose_catalog(direct_page)
            subject_texts = {
                txt for subject, txt in direct_catalog
                if _subject_matches(subject, row["name"])
            }
            if len(subject_texts) == 1:
                row["special_rules"] = next(iter(subject_texts))
                row["rules_citations"] = [row["citation"]]
                continue
            if (not any(subject for subject, _txt in direct_catalog)
                    and len({txt for _subject, txt in direct_catalog}) == 1):
                row["special_rules"] = direct_catalog[0][1]
                row["rules_citations"] = [row["citation"]]
                continue

        hint = row.get("_rules_page_hint")
        printed_pages = summary_refs.get(key, set())
        if len(printed_pages) == 1:
            hint = next(iter(printed_pages))
        if not hint or not (1 <= hint <= doc.page_count):
            continue
        hinted_page = doc[hint - 1]
        if not _page_mentions(hinted_page, row["name"]):
            continue
        if hint not in catalog_cache:
            catalog_cache[hint] = page_rule_catalog(hinted_page)
        catalog = catalog_cache[hint]
        texts = {txt for names, txt in catalog if key in names}
        subject_texts = {
            txt for subject, txt in loose_catalog(hint)
            if _subject_matches(subject, row["name"])
        }
        texts.update(subject_texts)
        if not texts:
            unqualified = {
                txt for subject, txt in loose_catalog(hint) if not subject}
            if len(unqualified) == 1:
                texts = unqualified
        if len(texts) == 1:
            row["special_rules"] = next(iter(texts))
            row["rules_citations"] = [
                "%s [PDF page %d]" % (cite_book, hint)]

    # Final safe fallback: a subject printed inside the heading itself is an
    # explicit book-level name link, independent of profile-table geometry.
    subject_index = []
    for page_no in range(1, doc.page_count + 1):
        for subject, txt in loose_catalog(page_no):
            if subject:
                subject_index.append((subject, txt, page_no))
    for row in rows:
        if row.get("special_rules"):
            continue
        matches = [
            (txt, page_no) for subject, txt, page_no in subject_index
            if _subject_matches(subject, row["name"])
        ]
        texts = {txt for txt, _page_no in matches}
        if len(texts) == 1:
            txt = next(iter(texts))
            page_no = next(pno for candidate, pno in matches
                           if candidate == txt)
            row["special_rules"] = txt
            row["rules_citations"] = [
                "%s [PDF page %d]" % (cite_book, page_no)]

    for row in rows:
        row.pop("_rules_page_hint", None)


def harvest_book(doc, army, edition, official, cite_book):
    """Harvest a born-digital WHFB army book with readable header rows."""
    rows_out = []
    soft_out = []
    coverage_gaps = []

    for i in range(doc.page_count):
        words = doc[i].get_text("words")
        rows = cluster_rows(words)
        if not rows:
            continue
        headers = find_headers(rows)
        page_no = i + 1
        page_h = doc[i].rect.height or 792.0

        # pages that clearly hold a stat grid but yielded no header
        value_like = 0
        for ry, rtoks in rows:
            stat_toks = sum(1 for (yc, x0, x1, txt) in rtoks if is_value(txt))
            if stat_toks >= 7:
                value_like += 1
        if value_like and not headers:
            coverage_gaps.append((page_no, "value rows present but no header row parsed"))
            continue
        if not headers:
            continue

        hys = [h["y"] for h in headers]
        for hi, h in enumerate(headers):
            next_hy = hys[hi + 1] if hi + 1 < len(hys) else 1e9
            ctx = heading_above(rows, h["y"], page_h)
            # first pass: collect value rows + scan for a TROOP TYPE: line in block
            block_rows = []
            block_troop = None
            got = 0
            misses = 0
            for ry, rtoks in rows:
                if ry <= h["y"] + 1:
                    continue
                if ry >= next_hy - 1:
                    break
                if ry - h["y"] > 320:
                    break
                full = reconstruct_full_row(rtoks)
                mtt = TROOP_TYPE_RE.search(full)
                if mtt and block_troop is None:
                    tt = clean_troop_type(mtt.group(1))
                    if tt:
                        block_troop = tt
                parsed = parse_value_row(rtoks, h["cols"])
                if parsed is None:
                    if got >= 1:
                        misses += 1
                        if misses >= 3:
                            break
                    continue
                misses = 0
                got += 1
                hint = page_reference_hint(
                    rows, h, rtoks, doc.page_count, doc[i].rect.width)
                block_rows.append((page_no, parsed, hint))

            rule_text = extract_special_rules(doc[i], h, headers)
            rule_match = _SPECIAL_RULES_RE.search(rule_text or "")
            rule_subject = ((rule_match.group(1) or "").strip()
                            if rule_match else "")
            for (pno, parsed, hint) in block_rows:
                name, profile, troop_inline, soft = parsed
                troop = troop_inline or block_troop
                row = {
                    "name": name,
                    "profile": profile,
                    "army": army,
                    "edition": edition,
                    "official": official,
                    "system": SYSTEM,
                    "book": cite_book,
                    "citation": "%s [PDF page %d]" % (cite_book, pno),
                }
                if troop:
                    row["troop_type"] = troop
                if hint and hint != pno:
                    row["_rules_page_hint"] = hint
                if ctx and ctx.lower() != name.lower():
                    row["unit_context"] = ctx
                if (rule_text and
                        (not rule_subject or _subject_matches(rule_subject, name))):
                    row["special_rules"] = rule_text
                    row["rules_citations"] = [row["citation"]]
                if soft:
                    row["soft"] = soft
                    soft_out.append({"citation": row["citation"], "name": name,
                                     "reason": soft, "profile": profile})
                rows_out.append(row)

    rows_out = resolve_garbled(rows_out, soft_out)
    attach_rule_backfills(doc, rows_out, cite_book)
    return rows_out, soft_out, coverage_gaps


# ----------------------------------------------------------------------------
# Book / edition / army helpers + officialness classification
# ----------------------------------------------------------------------------
_ORD = {"1": "1st", "2": "2nd", "3": "3rd", "4": "4th", "5": "5th",
        "6": "6th", "7": "7th", "8": "8th", "9": "9th"}

# filename markers of fan-made / unofficial redistributions
UNOFFICIAL_MARKERS = ["9th", "pdf room", "pdf-free", "pdfroom", "derevision",
                      "v1.2", "v12", "black legion", "-free"]


def book_stem(fname):
    return os.path.splitext(fname)[0].strip()


def infer_edition(fname):
    m = re.search(r"Armybook_(\d)ed", fname, re.I)
    if not m:
        m = re.search(r"(\d)(?:st|nd|rd|th)\s*ed", fname, re.I)
    if m:
        return _ORD.get(m.group(1), "unknown")
    return "unknown"


def infer_army(fname):
    stem = book_stem(fname)
    s = re.sub(r"^Armybook_\d+ed\s*-\s*", "", stem, flags=re.I)
    s = re.sub(r"^Warhammer(\s+Armies)?[_:\s-]+", "", s, flags=re.I)
    s = re.sub(r"\bPDF\s*Room\b", "", s, flags=re.I)
    s = re.sub(r"\bpdf-?free\b", "", s, flags=re.I)
    s = re.sub(r"\b9th\s*(edition|ed)?\b", "", s, flags=re.I)
    s = re.sub(r"\b\d{4}\b", "", s)                 # year
    s = re.sub(r"\bv1\.?2\d?\b", "", s, flags=re.I)  # version tag
    s = re.sub(r"\([^)]*\)", "", s)                  # (cut)/(buggy)
    s = re.sub(r"[-_]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip(" -\u2013:")
    # tidy a few known spellings
    s = s.replace("Orcs And Goblins", "Orcs & Goblins")
    return s.strip() or stem


def classify(fname):
    """Return (kind, edition, army, official) for a digital file.
    kind in {'official','unofficial','rulebook'}."""
    low = fname.lower()
    edition = infer_edition(fname)
    army = infer_army(fname)
    if low.startswith("rulebook") or "rulebook" in low:
        return "rulebook", edition, army, False
    if any(mk in low for mk in UNOFFICIAL_MARKERS):
        return "unofficial", "unofficial (fan)", army, False
    return "official", edition, army, True


def _norm_name(n):
    return re.sub(r"\s+", "", n.lower())


def _prefer_rule_text(target, source):
    """Keep the longer cited book-raw rule span when duplicate profiles merge."""
    incoming = source.get("special_rules", "")
    current = target.get("special_rules", "")
    if incoming and len(incoming) > len(current):
        target["special_rules"] = incoming
        target["rules_citations"] = list(source.get("rules_citations", []))


def dedupe_within_book(rows):
    """
    Collapse duplicate rows within a book (the army-list summary repeats the
    bestiary datasheets).  Two passes: (1) exact (name, profile) matches; then
    (2) subset matches -- a partial row (a summary copy that dropped a cell)
    whose profile is contained, key-for-key, in a same-named fuller row is
    removed in favour of the complete one.
    """
    seen = {}
    out = []
    removed = 0
    for r in rows:
        key = (r["book"], _norm_name(r["name"]), tuple(sorted(r["profile"].items())))
        if key in seen:
            removed += 1
            idx = seen[key]
            if "troop_type" not in out[idx] and "troop_type" in r:
                out[idx]["troop_type"] = r["troop_type"]
            _prefer_rule_text(out[idx], r)
            continue
        seen[key] = len(out)
        out.append(r)

    # subset pass: drop a row whose profile is a strict subset of a same-named row
    by_name = {}
    for i, r in enumerate(out):
        by_name.setdefault(_norm_name(r["name"]), []).append(i)
    drop = set()
    for _n, idxs in by_name.items():
        if len(idxs) < 2:
            continue
        for a in idxs:
            if a in drop:
                continue
            pa = out[a]["profile"]
            for b in idxs:
                if b == a or b in drop:
                    continue
                pb = out[b]["profile"]
                if len(pa) < len(pb) and all(k in pb and pb[k] == v
                                             for k, v in pa.items()):
                    if "troop_type" not in out[b] and "troop_type" in out[a]:
                        out[b]["troop_type"] = out[a]["troop_type"]
                    if "unit_context" not in out[b] and "unit_context" in out[a]:
                        out[b]["unit_context"] = out[a]["unit_context"]
                    _prefer_rule_text(out[b], out[a])
                    drop.add(a)
                    break
    if drop:
        removed += len(drop)
        out = [r for i, r in enumerate(out) if i not in drop]
    return out, removed


# ----------------------------------------------------------------------------
# File discovery
# ----------------------------------------------------------------------------
def _is_faq_path(path):
    """True if any directory component marks an errata/FAQ area (not a roster)."""
    parts = os.path.normpath(path).split(os.sep)
    return any("faq" in p.lower() for p in parts[:-1])


def discover_pdfs():
    files = []
    faq = []
    for root in SRC_DIRS:
        if not os.path.isdir(root):
            continue
        for dirpath, _dirs, fnames in os.walk(root):
            for fn in sorted(fnames):
                if not fn.lower().endswith(".pdf"):
                    continue
                full = os.path.join(dirpath, fn)
                if _is_faq_path(full):
                    faq.append(full)
                else:
                    files.append(full)
    files = sorted(set(files), key=lambda p: (os.path.basename(p).lower(), p))
    faq = sorted(set(faq), key=lambda p: (os.path.basename(p).lower(), p))
    return files, faq


def high_elves_vision_rows():
    """Return the verified one-page High Elves vision batch.

    The scan has zero PyMuPDF words on all 96 pages.  PDF page 91 (printed p.92)
    was rendered at 3x and read directly.  It contains 12 printed profile lines;
    the repeated Elven Steed line is identical in two units, so the index keeps
    11 unique (name, profile) rows under the normal within-book dedupe policy.
    """
    common = "SPECIAL RULES: Always Strikes First, Martial Prowess, Valour of Ages."
    riders = ("SPECIAL RULES: Always Strikes First (Riders only), Martial "
              "Prowess, Valour of Ages.")
    reavers = ("SPECIAL RULES: Always Strikes First (Riders only), Fast Cavalry, "
               "Martial Prowess, Valour of Ages.")
    # name, unit context, troop type, M WS BS S T W I A Ld, rule block
    raw = [
        ("Spearman", "SPEARMEN", "Infantry", (5, 4, 4, 3, 3, 1, 5, 1, 8), common),
        ("Sentinel", "SPEARMEN", "Infantry", (5, 4, 4, 3, 3, 1, 5, 2, 8), common),
        ("Archer", "ARCHERS", "Infantry", (5, 4, 4, 3, 3, 1, 5, 1, 8), common),
        ("Hawkeye", "ARCHERS", "Infantry", (5, 4, 5, 3, 3, 1, 5, 1, 8), common),
        ("Sea Guard", "LOTHERN SEA GUARD", "Infantry", (5, 4, 4, 3, 3, 1, 5, 1, 8), common),
        ("Sea Master", "LOTHERN SEA GUARD", "Infantry", (5, 4, 4, 3, 3, 1, 5, 2, 8), common),
        ("Silver Helm", "SILVER HELMS", "Cavalry", (5, 4, 4, 3, 3, 1, 5, 1, 8), riders),
        ("High Helm", "SILVER HELMS", "Cavalry", (5, 4, 4, 3, 3, 1, 5, 2, 8), riders),
        ("Elven Steed", "SILVER HELMS", "-", (9, 3, 0, 3, 3, 1, 4, 1, 5), riders),
        ("Ellyrian Reaver", "ELLYRIAN REAVERS", "Cavalry", (5, 4, 4, 3, 3, 1, 5, 1, 8), reavers),
        ("Harbinger", "ELLYRIAN REAVERS", "Cavalry", (5, 4, 5, 3, 3, 1, 5, 1, 8), reavers),
    ]
    citation = "%s [PDF page %d] (printed p.%d)" % (
        VISION_HIGH_ELVES_STEM, VISION_HIGH_ELVES_PDF_PAGE,
        VISION_HIGH_ELVES_PRINTED_PAGE)
    rows = []
    for name, context, troop, values, rules in raw:
        rows.append({
            "name": name,
            "profile": dict(zip(WHFB_STATS, map(str, values))),
            "army": "High Elves",
            "edition": "8th",
            "official": True,
            "system": SYSTEM,
            "book": VISION_HIGH_ELVES_STEM,
            "citation": citation,
            "troop_type": troop,
            "unit_context": context,
            "special_rules": rules,
            "rules_citations": [citation],
            "vision_transcribed": True,
        })
    return rows


# ----------------------------------------------------------------------------
# Top-level harvest
# ----------------------------------------------------------------------------
def harvest_all(verbose=True):
    result = {
        "rows": [],
        "soft": [],
        "per_book": {},
        "per_book_rules": {},
        "rule_gaps": [],
        "digital_official": [],
        "digital_unofficial": [],   # (stem, reason)
        "skipped_rulebook": [],
        "skipped_faq": [],
        "no_profiles": [],          # digital, official-looking, but 0 rows
        "mangled": [],              # (stem, junkfrac)
        "vision_partial": [],        # bounded page-image batches
        "no_coverage": [],          # scanned / open-failed / uncovered pages
        "page_gaps": [],
    }

    files, faq_files = discover_pdfs()
    for path in faq_files:
        result["skipped_faq"].append(book_stem(os.path.basename(path)))
    if verbose and faq_files:
        print("SKIP (FAQ/errata folder): %d file(s) not army rosters" % len(faq_files))

    for path in files:
        fname = os.path.basename(path)
        stem = book_stem(fname)
        try:
            doc = fitz.open(path)
        except Exception as e:
            if verbose:
                print("NO COVERAGE: %s (open failed: %s)" % (fname, e))
            result["no_coverage"].append(stem)
            continue

        if not is_digital(doc):
            if stem == VISION_HIGH_ELVES_STEM:
                actual_sha = file_sha256(path)
                if (doc.page_count != 96 or
                        actual_sha != VISION_HIGH_ELVES_SHA256):
                    if verbose:
                        print("NO COVERAGE: %s (vision source fingerprint/page "
                              "count does not match the verified scan)" % fname)
                    result["no_coverage"].append(
                        "%s (vision source mismatch)" % stem)
                    doc.close()
                    continue
                rows = high_elves_vision_rows()
                result["rows"].extend(rows)
                result["per_book"][stem] = len(rows)
                result["per_book_rules"][stem] = sum(
                    bool(r.get("special_rules")) for r in rows)
                result["vision_partial"].append({
                    "book": stem,
                    "covered_pdf_pages": [VISION_HIGH_ELVES_PDF_PAGE],
                    "covered_printed_pages": [VISION_HIGH_ELVES_PRINTED_PAGE],
                    "profiles": len(rows),
                    "printed_profile_lines": 12,
                    "source_sha256": VISION_HIGH_ELVES_SHA256,
                    "method": "vision transcription from a 3x PyMuPDF render",
                })
                result["no_coverage"].append(
                    "%s [PDF pages 1-90, 92-96]" % stem)
                if verbose:
                    print("VISION-PARTIAL: %s [PDF page %d] -> %d unique "
                          "profiles (all other pages NO COVERAGE)"
                          % (fname, VISION_HIGH_ELVES_PDF_PAGE, len(rows)))
                doc.close()
                continue
            if verbose:
                print("NO COVERAGE: %s (scanned, image-only)" % fname)
            result["no_coverage"].append(stem)
            doc.close()
            continue

        kind, edition, army, official = classify(fname)

        if kind == "rulebook":
            if verbose:
                print("SKIP (policy): %s (core rulebook, not an army roster)" % fname)
            result["skipped_rulebook"].append(stem)
            doc.close()
            continue

        if kind == "unofficial":
            marker = next((mk for mk in UNOFFICIAL_MARKERS if mk in fname.lower()), "fan")
            if verbose:
                print("DIGITAL-UNOFFICIAL (skipped): %s [marker: %s]" % (fname, marker))
            result["digital_unofficial"].append((stem, marker))
            doc.close()
            continue

        # official candidate -> guard against a broken text layer (Rule 1)
        jf = junk_alpha_fraction(doc)
        if jf > CORRUPTION_THRESHOLD:
            if verbose:
                print("NO COVERAGE: %s (born-digital but broken font/CMap -- "
                      "characteristic values corrupted in text layer, %.1f%% junk)"
                      % (fname, 100.0 * jf))
            result["mangled"].append((stem, round(jf, 4)))
            doc.close()
            continue

        rows, soft, gaps = harvest_book(doc, army, edition, official, stem)
        rows, removed = dedupe_within_book(rows)
        if not rows:
            # digital & official-looking but produced no profiles -> not a roster
            if verbose:
                print("DIGITAL (no unit profiles found): %s "
                      "(likely errata/supplement, not a datasheet roster)" % fname)
            result["no_profiles"].append(stem)
            doc.close()
            continue
        result["rows"].extend(rows)
        result["soft"].extend(soft)
        result["per_book"][stem] = len(rows)
        result["per_book_rules"][stem] = sum(
            bool(r.get("special_rules")) for r in rows)
        for row in rows:
            if row.get("special_rules"):
                continue
            result["rule_gaps"].append(
                "%s / %s (no unambiguous explicit SPECIAL RULES section)"
                % (stem, row["name"]))
        result["digital_official"].append(stem)
        for (pno, why) in gaps:
            note = "%s [PDF page %d]: %s" % (stem, pno, why)
            result["page_gaps"].append(note)
        if verbose:
            extra = " (%d exact dupes merged)" % removed if removed else ""
            print("DIGITAL-OFFICIAL: %s [%s, %s] -> %d profiles%s"
                  % (stem, army, edition, len(rows), extra))

        try:
            os.makedirs(os.path.dirname(PROGRESS), exist_ok=True)
            with open(PROGRESS, "w", encoding="utf-8") as fh:
                json.dump({
                    "done_books": list(result["per_book"].keys()),
                    "per_book": result["per_book"],
                    "total_rows": len(result["rows"]),
                    "digital_official": result["digital_official"],
                    "digital_unofficial": [s for s, _ in result["digital_unofficial"]],
                    "mangled": [s for s, _ in result["mangled"]],
                    "skipped_rulebook": result["skipped_rulebook"],
                    "no_coverage": result["no_coverage"],
                }, fh, indent=2)
        except Exception:
            pass
        doc.close()

    return result


# ----------------------------------------------------------------------------
# Output writers
# ----------------------------------------------------------------------------
def profile_str(profile):
    # keep canonical stat order where possible
    order = {k: n for n, k in enumerate(WHFB_STATS)}
    items = sorted(profile.items(), key=lambda kv: order.get(kv[0], 99))
    return " ".join("%s%s" % (k, v) for k, v in items)


def write_outputs(result):
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    payload = {
        "system": SYSTEM,
        "note": ("Warhammer Fantasy Battle tabletop WARGAME unit profiles "
                 "(characteristic lines: M WS BS S T W I A Ld) plus each profile's "
                 "explicit book-raw SPECIAL RULES section when unambiguously linked. "
                 "Distinct from the Warhammer Fantasy Roleplay (WFRP) line. Extracted "
                 "from born-digital army-book PDF text layers plus one bounded, "
                 "page-image-verified High Elves vision batch; uncovered scanned pages "
                 "are listed under no_coverage_scanned."),
        "methodology_notes": [
            "Profiles reconstructed geometrically from the PDF text layer (PyMuPDF "
            "words mode): a header row of characteristic labels (M WS BS S T W I A Ld) "
            "fixes each column's x-centre, and every value row maps its stat tokens to "
            "the nearest column. The header is read live -- never hard-coded -- so a "
            "table that omits or reorders a column still parses. No number is ever "
            "guessed or corrected; unreadable cells are left empty.",
            "The official 8th-edition High Elves PDF is a 96-page image-only scan: "
            "PyMuPDF returns 0 characters and 0 words on every page. Exactly PDF "
            "page 91 (printed p.92) was rendered at 3x and transcribed by vision, "
            "then checked directly against the page image. Its 12 printed profile "
            "lines yield 11 unique rows because Elven Steed is repeated identically. "
            "Every other High Elves page remains explicit NO COVERAGE.",
            "These books lay text out glyph-by-glyph (there are no space characters in "
            "the content stream), so each unit name is rebuilt from the contiguous glyph "
            "cluster immediately left of the first stat column, inserting a space where "
            "the horizontal gap widens to a word break. Decorative drop-cap / bullet "
            "glyphs are trimmed. The clean ALL-CAPS datasheet heading above the table is "
            "captured separately as unit_context.",
            "A datasheet prints several profile lines -- the unit, its champion/command "
            "upgrade, and any mount or monster -- each emitted as its own row sharing the "
            "unit_context heading. Troop Type (Infantry/Cavalry/Monster/Chariot/War "
            "Beast/...) is captured from the 'TROOP TYPE:' line beneath a bestiary block "
            "or from the trailing text column after Ld in the army-list summary.",
            "Movement values keep verbatim any '*' (variable) or random-movement die "
            "(e.g. 2D6); '-' marks a characteristic a model does not have. Leadership can "
            "reach 10. Parenthetical values are kept as printed.",
            "SPECIAL RULES text is copied verbatim from the unit's PDF section. The "
            "attachment uses same-column profile geometry, explicit subject-qualified "
            "headings, or the army-list summary's printed Page column plus an exact "
            "name occurrence on the cited bestiary page. Display-spaced headings such "
            "as 'S P E C I A L R U L E S' are recognised. Ambiguous links remain named "
            "NO COVERAGE gaps; no rule text is inferred.",
            "Only the OFFICIAL Games Workshop army books are harvested. Born-digital files "
            "whose filenames mark them fan-made/unofficial ('9th', 'PDF Room', 'pdf-free', "
            "version tags) are classified DIGITAL-UNOFFICIAL and skipped so a fan stat is "
            "never passed as an official one. The 1994 4th-ed Chaos book is born-digital by "
            "character count but its font/CMap is broken -- the characteristic DIGITS "
            "extract as garbage (a '4' becomes '-j'/'~') -- so a token-corruption gate "
            "(alpha-junk fraction > 1.5%) routes it to NO COVERAGE rather than fabricating "
            "numbers (Inviolable Rule 1). Core rulebooks are skipped by policy.",
            "Summary/army-list tables duplicate the per-datasheet bestiary profiles; exact "
            "(name, profile) duplicates are merged within each book (space/case "
            "insensitive), preferring the row that also carries a troop_type.",
        ],
        "total_profiles": len(result["rows"]),
        "profiles_with_special_rules": sum(result["per_book_rules"].values()),
        "digital_official_books": result["digital_official"],
        "digital_unofficial_skipped": [
            {"book": s, "marker": mk} for s, mk in result["digital_unofficial"]],
        "skipped_rulebooks": result["skipped_rulebook"],
        "skipped_faq_errata_count": len(result["skipped_faq"]),
        "skipped_faq_errata": result["skipped_faq"],
        "digital_no_profiles": result["no_profiles"],
        "no_coverage_mangled": [
            {"book": s, "junk_alpha_fraction": jf} for s, jf in result["mangled"]],
        "partial_coverage_vision": result["vision_partial"],
        "no_coverage_scanned": result["no_coverage"],
        "page_gaps": result["page_gaps"],
        "special_rules_no_coverage": result["rule_gaps"],
        "per_book_counts": result["per_book"],
        "per_book_rule_counts": result["per_book_rules"],
        "soft_count": len(result["soft"]),
        "rows": result["rows"],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)

    lines = []
    lines.append("# Warhammer Fantasy Battle Wargame -- Unit Profile Index")
    lines.append("")
    lines.append("**System:** WHFB (tabletop wargame -- NOT the WFRP roleplay line)  ")
    lines.append("**Total profiles:** %d" % len(result["rows"]))
    lines.append("**Profiles with special rules:** %d"
                 % sum(result["per_book_rules"].values()))
    lines.append("**Named special-rules gaps:** %d" % len(result["rule_gaps"]))
    lines.append("**Soft / uncertain rows:** %d  " % len(result["soft"]))
    lines.append("")
    lines.append("Profiles (M WS BS S T W I A Ld) extracted geometrically from the PDF "
                 "text layer (PyMuPDF words mode) of born-digital OFFICIAL Games "
                 "Workshop army books, plus one bounded High Elves page transcribed "
                 "from a verified 3x render. Fan-made files and uncovered scanned pages "
                 "remain explicit NO COVERAGE.")
    lines.append("")
    lines.append("## Methodology")
    lines.append("")
    for n in payload["methodology_notes"]:
        lines.append("- %s" % n)
    lines.append("")
    lines.append("## Digital OFFICIAL books harvested")
    lines.append("")
    lines.append("| Book | Army | Edition | Profiles | Rules |")
    lines.append("| --- | --- | --- | --- | --- |")
    for s in result["digital_official"]:
        ed = infer_edition(s)
        ar = infer_army(s)
        lines.append("| %s | %s | %s | %d | %d |"
                     % (s, ar, ed, result["per_book"].get(s, 0),
                        result["per_book_rules"].get(s, 0)))
    lines.append("")
    if result["vision_partial"]:
        lines.append("## Bounded VISION coverage (official scanned book)")
        lines.append("")
        for b in result["vision_partial"]:
            lines.append("- %s: PDF page %d (printed p.%d), %d unique profiles "
                         "from %d printed profile lines; all other pages remain "
                         "NO COVERAGE."
                         % (b["book"], b["covered_pdf_pages"][0],
                            b["covered_printed_pages"][0], b["profiles"],
                            b["printed_profile_lines"]))
        lines.append("")
    if result["digital_unofficial"]:
        lines.append("## Digital UNOFFICIAL / fan-made (skipped -- not harvested)")
        lines.append("")
        for s, mk in result["digital_unofficial"]:
            lines.append("- %s  _(marker: %s)_" % (s, mk))
        lines.append("")
    if result["mangled"]:
        lines.append("## NO COVERAGE (born-digital but broken text layer)")
        lines.append("")
        for s, jf in result["mangled"]:
            lines.append("- %s  _(%.1f%% junk-alpha tokens: font/CMap corrupts the "
                         "characteristic digits; not harvested per Inviolable Rule 1)_"
                         % (s, 100.0 * jf))
        lines.append("")
    if result["skipped_rulebook"]:
        lines.append("## Skipped by policy (core rulebooks, not army rosters)")
        lines.append("")
        for s in result["skipped_rulebook"]:
            lines.append("- %s" % s)
        lines.append("")
    if result["no_profiles"]:
        lines.append("## Digital, but no unit profiles (errata/supplement, not harvested)")
        lines.append("")
        for s in result["no_profiles"]:
            lines.append("- %s" % s)
        lines.append("")
    if result["skipped_faq"]:
        lines.append("## Skipped (FAQ / errata subfolder -- %d files, not army rosters)"
                     % len(result["skipped_faq"]))
        lines.append("")
        for s in result["skipped_faq"]:
            lines.append("- %s" % s)
        lines.append("")
    if result["rule_gaps"]:
        lines.append("## NO COVERAGE (special-rules attachment)")
        lines.append("")
        lines.append("These profiles remain mechanically indexed, but no unambiguous "
                     "explicit unit SPECIAL RULES section could be linked:")
        lines.append("")
        for gap in result["rule_gaps"]:
            lines.append("- %s" % gap)
        lines.append("")
    lines.append("## NO COVERAGE (scanned, image-only books or uncovered pages)")
    lines.append("")
    for s in result["no_coverage"]:
        lines.append("- %s" % s)
    lines.append("")
    if result["page_gaps"]:
        lines.append("## Digital pages whose profiles could not be parsed")
        lines.append("")
        for g in result["page_gaps"]:
            lines.append("- %s" % g)
        lines.append("")

    by_book = {}
    for r in result["rows"]:
        by_book.setdefault(r["book"], []).append(r)
    for cb in sorted(by_book.keys()):
        lines.append("## %s" % cb)
        lines.append("")
        lines.append("| Unit | Profile | Troop Type | Context | Edition | Citation | Rules | Soft |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
        for r in by_book[cb]:
            soft = "yes" if "soft" in r else ""
            rules = "yes" if r.get("special_rules") else ""
            nm = r["name"].replace("|", "\\|")
            pr = profile_str(r["profile"]).replace("|", "\\|")
            tt = r.get("troop_type", "").replace("|", "\\|")
            ctx = r.get("unit_context", "").replace("|", "\\|")
            lines.append("| %s | %s | %s | %s | %s | %s | %s | %s |" %
                         (nm, pr, tt, ctx, r["edition"], r["citation"],
                          rules, soft))
        lines.append("")

    with open(OUT_MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


# ----------------------------------------------------------------------------
# Self test
# ----------------------------------------------------------------------------
def _synthetic_cold_one_riders():
    """
    Authentic words-list fixture taken from the exact glyph geometry of
    'Armybook_8ed - Lizardmen.pdf' page 37 (Cold One Riders datasheet):
    header  M WS BS s T W I A Ld  and value row  Cold One Rider 4 4 0 4 4 1 2 2 8.
    """
    hdr = [
        (404.6, 410.7, "M"), (417.9, 428.4, "WS"), (433.2, 441.3, "BS"),
        (449.8, 451.8, "s"), (463.2, 467.2, "T"), (476.6, 483.1, "W"),
        (493.0, 495.1, "I"), (505.7, 510.8, "A"), (518.4, 526.3, "Ld"),
    ]
    val = [
        (316.3, 320.1, "C"), (322.1, 324.7, "o"), (326.0, 331.1, "ld"),
        (334.8, 338.8, "O"), (341.1, 344.0, "n"), (345.6, 347.9, "e"),
        (351.6, 355.4, "R"), (357.1, 362.1, "id"), (363.5, 365.8, "e"),
        (366.9, 369.2, "r"),
        (406.1, 408.7, "4"), (421.4, 424.0, "4"), (435.8, 438.4, "0"),
        (449.7, 452.3, "4"), (463.9, 466.5, "4"), (479.0, 481.6, "1"),
        (492.3, 494.9, "2"), (506.4, 509.0, "2"), (521.0, 523.6, "8"),
    ]
    words = []
    for (x0, x1, t) in hdr:
        words.append((x0, 452.0, x1, 460.0, t, 0, 0, 0))
    for (x0, x1, t) in val:
        words.append((x0, 463.0, x1, 471.0, t, 0, 0, 0))
    return words


def selftest():
    ok = True

    # (a) synthetic fixture -- header read + name + full profile reconstruct
    words = _synthetic_cold_one_riders()
    rows = cluster_rows(words)
    headers = find_headers(rows)
    assert len(headers) == 1, "expected exactly one header, got %d" % len(headers)
    h = headers[0]
    labels = [c["label"] for c in h["cols"]]
    assert labels == WHFB_STATS, labels  # 's' canonicalised to 'S'
    parsed = None
    for ry, rtoks in rows:
        if ry > h["y"] + 1:
            parsed = parse_value_row(rtoks, h["cols"])
            break
    assert parsed is not None, "value row failed to parse"
    name, profile, troop_inline, soft = parsed
    assert name == "Cold One Rider", repr(name)
    expect = {"M": "4", "WS": "4", "BS": "0", "S": "4", "T": "4",
              "W": "1", "I": "2", "A": "2", "Ld": "8"}
    assert profile == expect, profile
    print("selftest: synthetic Cold One Rider fixture OK -> %s | %s"
          % (name, profile_str(profile)))

    # (a2) value-token grammar
    for good in ("4", "10", "-", "*", "2D6", "3+", "6(10)"):
        assert is_value(good), "is_value rejected %r" % good
    for bad in ("Infantry", "Cold", "WS", "Ld"):
        assert not is_value(bad), "is_value accepted %r" % bad
    print("selftest: value-token grammar OK")

    # (a3) normal, display-spaced, and subject-qualified rules headings
    normal = _SPECIAL_RULES_RE.search("SPECIAL RULES: Fly.")
    spaced = _SPECIAL_RULES_RE.search(
        "S P E C I A L R U L E S : Daemonic.")
    subject = _SPECIAL_RULES_RE.search(
        "SPECIAL RULES (Hound of Orion): Forest Spirit.")
    assert normal and not normal.group(1)
    assert spaced and not spaced.group(1)
    assert subject and subject.group(1) == "Hound of Orion"
    assert _subject_matches(subject.group(1), "Hound of Orion")
    assert not _subject_matches(subject.group(1), "Orion")
    print("selftest: SPECIAL RULES heading grammar OK")

    # (a4) live Lizardmen p37 fixture (guarded)
    liz = os.path.join(SRC_DIRS[0], "8 ed", "Armybook_8ed - Lizardmen.pdf")
    if os.path.isfile(liz):
        doc = fitz.open(liz)
        rows = cluster_rows(doc[36].get_text("words"))  # 1-indexed page 37
        hs = find_headers(rows)
        found = False
        for hh in hs:
            if [c["label"] for c in hh["cols"]] != WHFB_STATS:
                continue
            for ry, rtoks in rows:
                if ry <= hh["y"] + 1:
                    continue
                p = parse_value_row(rtoks, hh["cols"])
                if p and p[0] == "Cold One Rider":
                    assert p[1] == expect, p[1]
                    found = True
                    break
            if found:
                break
        doc.close()
        assert found, "live Lizardmen p37 Cold One Rider row not found/parsed"
        print("selftest: live Lizardmen p37 Cold One Rider OK")
    else:
        print("selftest: live Lizardmen fixture skipped (PDF not present)")

    # (b) live-harvest invariants
    res = harvest_all(verbose=False)
    rows = res["rows"]
    total = len(rows)
    assert total == 302, "expected 302 profiles, got %d" % total
    expected_profiles = {
        "Armybook_8ed - Daemons of Chaos - 2012": 54,
        "Armybook_8ed - Dwarfs - 2014": 40,
        "Armybook_8ed - High Elves": 11,
        "Armybook_8ed - Lizardmen": 49,
        "Armybook_8ed - Vampire Counts": 52,
        "Armybook_8ed - Warriors of Chaos 2012": 49,
        "Armybook_8ed - Wood Elves": 47,
    }
    expected_rules = {
        "Armybook_8ed - Daemons of Chaos - 2012": 38,
        "Armybook_8ed - Dwarfs - 2014": 34,
        "Armybook_8ed - High Elves": 11,
        "Armybook_8ed - Lizardmen": 28,
        "Armybook_8ed - Vampire Counts": 44,
        "Armybook_8ed - Warriors of Chaos 2012": 32,
        "Armybook_8ed - Wood Elves": 41,
    }
    assert res["per_book"] == expected_profiles, res["per_book"]
    assert res["per_book_rules"] == expected_rules, res["per_book_rules"]
    assert sum(expected_rules.values()) == 228
    assert len(res["rule_gaps"]) == 74, len(res["rule_gaps"])
    for r in rows:
        assert r["system"] == "WHFB", "row not labelled WHFB: %r" % r
        assert r["name"] and has_alpha(r["name"]), "empty/invalid name: %r" % r
        assert isinstance(r["profile"], dict) and r["profile"], "empty profile: %r" % r
        assert "[PDF page" in r["citation"], "bad citation: %r" % r
        assert r.get("official") is True, "harvested row not marked official: %r" % r
        low = r["name"].lower()
        assert low not in LABELS, "header token leaked as name: %r" % r
        assert not re.match(r"^(ws|bs|ld|troop\s*type)\b", low), "header/field leak: %r" % r
        if r.get("special_rules"):
            assert r.get("rules_citations"), "rules missing citation: %r" % r
            assert all("[PDF page" in c for c in r["rules_citations"]), r
            markers = list(_SPECIAL_RULES_RE.finditer(r["special_rules"]))
            assert len(markers) == 1, "nested/missing rules heading: %r" % r
            subject = (markers[0].group(1) or "").strip()
            if subject:
                assert _subject_matches(subject, r["name"]), (
                    "subject mismatch: %r" % r)
            assert "And to tell of the Juggernaut:" not in r["special_rules"], r
            assert not re.search(
                r"(?mi)^\s*(?:OPTIONS|EQUIPMENT|MAGIC ITEMS|UPGRADES?)\s*:",
                r["special_rules"]), "rule span leaked a new section: %r" % r
        # profile keys must be within the recognised schema (+ dup suffixes)
        for k in r["profile"]:
            base = k.split("#")[0]
            assert base in WHFB_STATS or base in ("Points",), "odd profile key %r" % k
    keyed = {(r["book"], r["name"]): r for r in rows}
    assert "Daemon of Khorne" in keyed[
        ("Armybook_8ed - Daemons of Chaos - 2012",
         "Bloodthirster")]["special_rules"]
    assert "The Hunger:" in keyed[
        ("Armybook_8ed - Vampire Counts", "Vampires")]["special_rules"]
    assert "Ancestral Grudge" in keyed[
        ("Armybook_8ed - Dwarfs - 2014", "Lord")]["special_rules"]
    assert "SPECIA L RULES (Hound of Orion):" in keyed[
        ("Armybook_8ed - Wood Elves", "Hound of Orion")]["special_rules"]
    assert "Impetuous:" in keyed[
        ("Armybook_8ed - Wood Elves", "Ceithin-Har")]["special_rules"]
    assert "Hunter’s Mount:" in keyed[
        ("Armybook_8ed - Wood Elves", "Gwindalor")]["special_rules"]
    hawkeye = keyed[(VISION_HIGH_ELVES_STEM, "Hawkeye")]
    assert hawkeye["profile"] == {
        "M": "5", "WS": "4", "BS": "5", "S": "3", "T": "3",
        "W": "1", "I": "5", "A": "1", "Ld": "8"}, hawkeye
    assert hawkeye["vision_transcribed"] is True
    assert hawkeye["citation"].endswith("[PDF page 91] (printed p.92)")
    assert len(res["vision_partial"]) == 1, res["vision_partial"]
    assert res["vision_partial"][0]["printed_profile_lines"] == 12
    assert res["vision_partial"][0]["source_sha256"] == VISION_HIGH_ELVES_SHA256
    assert len(res["digital_official"]) == 6, \
        "expected 6 official digital books, got %d" % len(res["digital_official"])
    assert len(res["mangled"]) >= 1, "expected the 1994 Chaos book to be gated as mangled"
    assert len(res["digital_unofficial"]) >= 6, "expected fan books to be flagged"
    assert len(res["no_coverage"]) >= 30, "expected many scanned books"
    print("selftest: live-harvest invariants OK (total=%d, official=%d, unofficial=%d, "
          "mangled=%d, scanned=%d, soft=%d)"
          % (total, len(res["digital_official"]), len(res["digital_unofficial"]),
             len(res["mangled"]), len(res["no_coverage"]), len(res["soft"])))

    print("selftest: PASS")
    return ok


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------
def main(argv):
    if "--selftest" in argv:
        try:
            selftest()
        except AssertionError as e:
            print("selftest: FAIL -- %s" % e)
            return 1
        except Exception as e:
            print("selftest: ERROR -- %s" % e)
            return 2
        return 0

    print("Harvesting WHFB wargame unit profiles from digital and bounded-vision sources...")
    res = harvest_all(verbose=True)
    write_outputs(res)
    print("")
    print("Wrote %s (%d profiles; %d with special rules; %d named gaps)"
          % (OUT_JSON, len(res["rows"]),
             sum(res["per_book_rules"].values()), len(res["rule_gaps"])))
    print("Wrote %s" % OUT_MD)
    print("Digital-official: %d | Vision-partial: %d | Digital-unofficial: %d | "
          "Mangled: %d | Rulebooks: %d | FAQ/errata: %d | No-profiles: %d | "
          "Scanned/uncovered (NO COVERAGE): %d | Soft rows: %d"
          % (len(res["digital_official"]), len(res["vision_partial"]),
             len(res["digital_unofficial"]), len(res["mangled"]),
             len(res["skipped_rulebook"]), len(res["skipped_faq"]),
             len(res["no_profiles"]), len(res["no_coverage"]),
             len(res["soft"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
