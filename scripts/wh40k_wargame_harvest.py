#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wh40k_wargame_harvest.py  --  THE NEW PATH ENGINE reference-layer harvester.

Extracts UNIT PROFILES (datasheet characteristic lines) from the BORN-DIGITAL
Warhammer 40,000 *tabletop wargame* codex PDFs and writes:
    reference/wh40k_wargame_index.json
    reference/wh40k_wargame_index.md

This is the WARGAME (miniatures game), DISTINCT from the 40K Roleplay line.
Every emitted row carries  "system": "WH40K".

Technique (geometric grid reconstruction, PyMuPDF "words" mode):
  1. Cluster words into visual rows by y (gap-based single linkage).
  2. A HEADER row = the longest contiguous run of characteristic-label tokens
     actually present (WS BS S T W I A Ld Sv / Front Side Rear Armour / Points ...).
     We read whatever labels are there -- no hard-coded schema.
  3. Each value row below maps its stat tokens to the nearest header column by
     x-centre; the word tokens left of the first column are the unit name.
  4. A separate additive pass slices each printed SPECIAL RULES section from
     the same PDF text layer, attaches it verbatim to the matching profile, and
     records the rules page citation. Ambiguous/absent sections remain empty and
     are reported as NO COVERAGE; no rule text is inferred.

Codex Imperialis (1993, 2nd ed) has NO header labels in its text layer (they are
part of the table graphic), so its value rows are captured POSITIONALLY (c1..cN,
raw values) and every such row is flagged 'soft' -- we never fabricate the
M/WS/BS... labels that are not in the PDF.

Stdlib + PyMuPDF (fitz) only. No cross-imports. Does NOT run git.
"""

import sys
import os
import re
import json
import math
import statistics

try:
    import fitz  # PyMuPDF
except Exception as e:  # pragma: no cover
    sys.stderr.write("FATAL: PyMuPDF (fitz) is required: %s\n" % e)
    raise

# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------
SRC_DIR = r"I:\Sourcebooks\Warhammer\40K\Compilation v2\Codex"

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
OUT_JSON = os.path.join(_ROOT, "reference", "wh40k_wargame_index.json")
OUT_MD = os.path.join(_ROOT, "reference", "wh40k_wargame_index.md")

PROGRESS = (r"C:\Users\Chad\AppData\Local\Temp\claude"
            r"\I--repos-the-new-path-engine--claude-worktrees-intelligent-lamport-3a158a"
            r"\1c5f36b4-d94a-4698-95d9-c2304f8a0818\scratchpad"
            r"\wh40k_wargame_progress.json")

SYSTEM = "WH40K"

# ----------------------------------------------------------------------------
# Label vocabulary (lower-cased keys)
# ----------------------------------------------------------------------------
# Canonical display form for each recognised header token.
CANON = {
    "ws": "WS", "bs": "BS", "s": "S", "t": "T", "w": "W", "i": "I", "a": "A",
    "ld": "Ld", "sv": "Sv", "m": "M", "int": "Int", "cl": "Cl", "wp": "WP",
    "front": "Front", "side": "Side", "rear": "Rear",
    "armour": "Armour", "armor": "Armour",
    "f": "F", "r": "R",
    "pts": "Points", "points": "Points", "pts/model": "Points",
    "page": "Page",
}
LABELS = set(CANON.keys())
# "strong" labels almost never occur as prose -> used to qualify a header row.
STRONG = {"ws", "bs", "ld", "sv", "int", "cl", "wp",
          "front", "side", "rear", "armour", "armor",
          "pts", "points", "pts/model"}
# columns that are not game characteristics -> dropped from the emitted profile
# (but kept during mapping so their values do not pollute a real column).
DROP_LABELS = {"Page"}

# A value cell: only digits/dashes/parens/plus/slash/dot, with at least one
# digit, OR a lone dash.  Matches 4, 10, 3+, 6(10), 2(3), 4(5), -/3+, +12, 45, -.
_VALCHARS = set("0123456789()+-/.\u2013\u2014")
_DASHES = {"-", "\u2013", "\u2014"}


def is_value(tok):
    if tok in _DASHES:
        return True
    if not tok:
        return False
    if not set(tok) <= _VALCHARS:
        return False
    return any(c.isdigit() for c in tok)


def has_alpha(tok):
    return any(c.isalpha() for c in tok)


# ----------------------------------------------------------------------------
# Unit special-rule extraction
# ----------------------------------------------------------------------------
# Rules are read from the same born-digital PDF text layer as the profile.  The
# profile detector above remains untouched: this is an additive attachment pass
# over its rows, and no characteristic value is rewritten.
_RULE_STOP_HEADINGS = {
    "wargear", "options", "unit type", "unit composition", "transport",
    "dedicated transport", "weapons", "psychic powers", "transport capacity",
    "number squad", "equipment", "armoury", "harlequins armoury",
}
_RULE_STAT_LABELS = {
    "m", "ws", "bs", "s", "t", "w", "i", "a", "ld", "sv", "f", "r",
    "front", "side", "rear",
}
_RULE_GENERIC_NAME = {
    "space", "marine", "veteran", "squad", "company", "captain", "sergeant",
    "sgt", "brother", "lord", "the", "of", "blood", "angels", "harlequin",
    "troupe",
}
_RULE_VALUE = re.compile(r"^[+\-\u2013\u2014]?\d+(?:[+()/.,\-\u2013\u2014\d]*)?$")

# Verified layout exceptions.  On these two Blood Angels army-list pages the
# PDF emits the columns out of reading order, but the rule sections and named
# profiles remain clean.  The list is section order, verified against the page.
_RULE_SECTION_HINTS = {
    ("Blood Angels - 2007 - 5th Edition", 24):
        ["Land Raider", "Land Raider Crusader", None],
    ("Blood Angels - 2007 - 5th Edition", 26):
        ["Rhino", "Drop Pod"],
}

# Verified summary-name aliases.  These point only to another harvested profile
# in the same book; the attached text and its citation are copied verbatim.
_RULE_ALIASES = {
    "Blood Angels - 2007 - 5th Edition": {
        "Furioso": "Furioso Dreadnought",
        "Company Captain": "Captain",
        "Tycho": "Cpt. Tycho",
    },
    "Space Marines - 2008 - 5th Edition": {
        "Chronus": "Antaro Chronus",
        "Ironclad": "Ironclad Dreadnought",
    },
}


def _rule_norm(text):
    return re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip()


def _rule_field_key(line):
    return re.sub(r"\s+", " ", line.strip()).casefold().rstrip(":").strip()


def _special_heading(line):
    """Return '' for a unit-local heading, a subject for an ALL-CAPS shared
    heading, or None when the line is ordinary prose."""
    raw = re.sub(r"\s+", " ", line.strip())
    key = raw.casefold().rstrip(":").strip()
    if key in ("special rule", "special rules"):
        return ""
    letters = [c for c in raw if c.isalpha()]
    if (key.endswith(" special rules") and len(key.split()) <= 5 and letters
            and all(c.isupper() for c in letters)):
        return key[:-len(" special rules")].strip()
    return None


def _is_rule_profile_header(line):
    toks = [t.casefold().strip(".,:") for t in line.split()]
    return (len(toks) >= 3
            and sum(t in _RULE_STAT_LABELS for t in toks) >= 3
            and all(t in _RULE_STAT_LABELS for t in toks))


def _is_rule_entry_heading(lines, index):
    """An ALL-CAPS unit title followed by POINTS or a characteristic header."""
    raw = lines[index].strip()
    letters = [c for c in raw if c.isalpha()]
    if len(letters) < 4 or not all(c.isupper() for c in letters):
        return False
    if _rule_field_key(raw) in _RULE_STOP_HEADINGS:
        return False
    if _special_heading(raw) is not None:
        return False
    following = lines[index + 1:min(len(lines), index + 16)]
    has_points = any(re.search(r"\b(?:\d+|NO)\s+POINTS?\b", x, re.I)
                     for x in following[:5])
    single_stats = sum(_rule_field_key(x) in _RULE_STAT_LABELS for x in following)
    return (has_points
            or any(_is_rule_profile_header(x) for x in following[:7])
            or single_stats >= 5)


def _extract_rule_sections(lines):
    """Return book-verbatim SPECIAL RULES bodies with their line anchors."""
    headings = [(i, _special_heading(line)) for i, line in enumerate(lines)
                if _special_heading(line) is not None]
    out = []
    for pos, (start, subject) in enumerate(headings):
        end = headings[pos + 1][0] if pos + 1 < len(headings) else len(lines)
        for j in range(start + 1, end):
            key = _rule_field_key(lines[j])
            structural = (key in _RULE_STOP_HEADINGS
                          or any(key.startswith(h + ":")
                                 for h in _RULE_STOP_HEADINGS))
            if (structural or _is_rule_profile_header(lines[j])
                    or _is_rule_entry_heading(lines, j)):
                end = j
                break
        body = [x.rstrip() for x in lines[start + 1:end]]
        while body and (not body[0].strip()
                        or re.fullmatch(r"\d+", body[0].strip())):
            body.pop(0)
        while body and (not body[-1].strip()
                        or re.fullmatch(r"\d+", body[-1].strip())
                        or _rule_field_key(body[-1])
                        in {"eldar harlequins", "thought for the day"}):
            body.pop()
        text = "\n".join(body).strip()
        if text and sum(c.isalpha() for c in text) >= 3:
            out.append({"start": start, "end": end, "subject": subject,
                        "text": text})
    return out


def _rule_anchor_score(lines, index):
    return sum(bool(_RULE_VALUE.fullmatch(x.strip()))
               for x in lines[index + 1:min(len(lines), index + 14)])


def _rule_name_tokens(text):
    return set(_rule_norm(text).split()) - _RULE_GENERIC_NAME


def _profile_anchors(rows, lines, sections):
    """Find the printed profile-name line, preferring the occurrence followed
    by numeric stat cells over a prose mention or page title."""
    used = set()
    anchors = []
    hpos = [s["start"] for s in sections]
    for row in rows:
        key = _rule_norm(row["name"])
        occurrences = [i for i, line in enumerate(lines)
                       if _rule_norm(line) == key and i not in used]
        if occurrences:
            anchor = max(
                occurrences,
                key=lambda i: (_rule_anchor_score(lines, i),
                               -min([abs(i - h) for h in hpos] or [0])))
            used.add(anchor)
        else:
            anchor = None
        anchors.append((row, anchor))
    return anchors


def _add_rule(row, text, citation):
    if not text:
        return
    blocks = row.setdefault("_rule_blocks", [])
    citations = row.setdefault("_rule_citations", [])
    if text not in blocks:
        blocks.append(text)
    if citation not in citations:
        citations.append(citation)


def _assign_page_rules(rows, lines, citation):
    """Attach local sections to profiles.  Equal row/section counts are paired
    in printed order.  Multi-profile datasheets share one section; crowded army
    list pages use the nearest profile group and token evidence."""
    sections = [s for s in _extract_rule_sections(lines) if not s["subject"]]
    anchored = _profile_anchors(rows, lines, sections)
    available = [(row, anchor) for row, anchor in anchored if anchor is not None]
    if not sections or not available:
        return

    if len(sections) == len(available) == len(rows):
        for section, (row, anchor) in zip(
                sections, sorted(available, key=lambda pair: pair[1])):
            _add_rule(row, section["text"], citation)
        return

    entry_count = sum(_is_rule_entry_heading(lines, i)
                      for i in range(len(lines)))
    if len(sections) == 1 and entry_count <= 1:
        for row, anchor in available:
            _add_rule(row, sections[0]["text"], citation)
        return

    for section in sections:
        body_tokens = _rule_name_tokens(section["text"])
        primary, primary_anchor = max(
            available,
            key=lambda pair: (
                len(_rule_name_tokens(pair[0]["name"]) & body_tokens),
                -abs(pair[1] - section["start"])))
        for row, anchor in available:
            same_context = (row.get("unit_context")
                            and row.get("unit_context")
                            == primary.get("unit_context"))
            if row is primary or abs(anchor - primary_anchor) <= 16 or same_context:
                _add_rule(row, section["text"], citation)


def _leading_rule_title(lines):
    parts = []
    for line in lines[:8]:
        text = line.strip()
        if not text or re.fullmatch(r"\d+", text):
            continue
        letters = [c for c in text if c.isalpha()]
        if letters and all(c.isupper() for c in letters):
            parts.append(text)
        else:
            break
    title = " ".join(parts)
    title = re.sub(r"\b(?:[A-Z]\s+){2,}[A-Z]\b",
                   lambda m: m.group(0).replace(" ", ""), title)
    return re.sub(r"\s+", " ", title).strip()


def attach_special_rules(doc, rows, cite_book):
    """Attach exact PDF SPECIAL RULES text and page citations to profile rows.
    Returns the number of attached profiles."""
    by_page = {}
    for row in rows:
        match = re.search(r"\[PDF page (\d+)\]", row.get("citation", ""), re.I)
        if match:
            by_page.setdefault(int(match.group(1)), []).append(row)

    title_catalog = []
    shared = []
    for page_no in range(1, doc.page_count + 1):
        lines = doc[page_no - 1].get_text("text").splitlines()
        sections = _extract_rule_sections(lines)
        citation = "%s [PDF page %d]" % (cite_book, page_no)
        if page_no in by_page:
            _assign_page_rules(by_page[page_no], lines, citation)

        # A unit page with no harvested profile (normally a vehicle whose stat
        # line exists only in the summary) is banked by its printed page title.
        local = [s for s in sections if not s["subject"]]
        title = _leading_rule_title(lines)
        if title and local and page_no not in by_page:
            title_catalog.append(
                (title, "\n\n".join(s["text"] for s in local), citation))

        for section in sections:
            if section["subject"]:
                shared.append((section["subject"], section["text"], citation))

    # Verified out-of-order army-list columns.
    for (book, page_no), subjects in _RULE_SECTION_HINTS.items():
        if book != cite_book or not (1 <= page_no <= doc.page_count):
            continue
        lines = doc[page_no - 1].get_text("text").splitlines()
        sections = [s for s in _extract_rule_sections(lines) if not s["subject"]]
        for subject, section in zip(subjects, sections):
            if subject:
                title_catalog.append(
                    (subject, section["text"],
                     "%s [PDF page %d]" % (cite_book, page_no)))

    # This heading explicitly says the block applies to all Harlequin units and
    # characters.  Keep the shared text verbatim and cite its own page.
    if cite_book == "Harlequins":
        for subject, text, citation in shared:
            if subject == "harlequin":
                for row in rows:
                    _add_rule(row, text, citation)

    # Exact-name duplicates (summary vs datasheet) inherit only when every
    # source block for that name is identical.
    by_name = {}
    for row in rows:
        blocks = tuple(row.get("_rule_blocks", []))
        cites = tuple(row.get("_rule_citations", []))
        if blocks:
            by_name.setdefault(_rule_norm(row["name"]), []).append((blocks, cites))
    for row in rows:
        if row.get("_rule_blocks"):
            continue
        values = by_name.get(_rule_norm(row["name"]), [])
        if values and len({v[0] for v in values}) == 1:
            blocks, citations = values[0]
            for index, text in enumerate(blocks):
                citation = citations[min(index, len(citations) - 1)]
                _add_rule(row, text, citation)

    # Match summary-only vehicle rows to a unit page title.  Exact matches win;
    # a unique contained match handles 'Predator/Baal Predator'.
    for row in rows:
        if row.get("_rule_blocks"):
            continue
        variants = [_rule_norm(v) for v in re.split(r"[/]", row["name"])]
        candidates = []
        for title, text, citation in title_catalog:
            tnorm = _rule_norm(title)
            if any(v == tnorm or (len(v) >= 5 and (v in tnorm or tnorm in v))
                   for v in variants):
                candidates.append((title, text, citation))
        exact = [c for c in candidates if _rule_norm(c[0]) in variants]
        choices = exact or candidates
        if choices and len({c[1] for c in choices}) == 1:
            _add_rule(row, choices[0][1], choices[0][2])

    # Small, source-verified name differences between detail and summary rows.
    aliases = _RULE_ALIASES.get(cite_book, {})
    for row in rows:
        if row.get("_rule_blocks") or row["name"] not in aliases:
            continue
        target = aliases[row["name"]]
        matches = [r for r in rows
                   if r["name"] == target and r.get("_rule_blocks")]
        if matches:
            blocks = matches[0]["_rule_blocks"]
            citations = matches[0]["_rule_citations"]
            for index, text in enumerate(blocks):
                citation = citations[min(index, len(citations) - 1)]
                _add_rule(row, text, citation)

    attached = 0
    for row in rows:
        blocks = row.pop("_rule_blocks", [])
        citations = row.pop("_rule_citations", [])
        if blocks:
            row["special_rules"] = "\n\n".join(blocks)
            row["rules_citations"] = citations
            attached += 1
    return attached


# ----------------------------------------------------------------------------
# PDF helpers
# ----------------------------------------------------------------------------
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
    # normalise: each row -> sorted by x, with a representative y
    out = []
    for r in rows:
        r = sorted(r, key=lambda t: t[1])
        ry = statistics.median([t[0] for t in r])
        out.append((ry, r))
    return out


def merge_touching(row_tokens, gap=2.5):
    """
    Merge horizontally touching tokens of the SAME kind -- used only for header
    label reconstruction (e.g. a split 'w'+'s' glyph -> 'ws').  Never merges a
    word with an adjacent value digit (that would corrupt names / drop a stat).
    """
    if not row_tokens:
        return []
    merged = [list(row_tokens[0])]  # [yc, x0, x1, txt]
    for tok in row_tokens[1:]:
        prev = merged[-1]
        # only stitch a split single-glyph label (e.g. 'w'+'s' -> 'ws');
        # never fuse two full labels ('WS'+'BS') or a word with a digit.
        both_single = len(prev[3]) == 1 and len(tok[3]) == 1
        same_kind = (is_value(prev[3]) == is_value(tok[3]))
        if both_single and same_kind and (tok[1] - prev[2]) < gap:
            prev[2] = tok[2]
            prev[3] = prev[3] + tok[3]
        else:
            merged.append(list(tok))
    return [(t[0], t[1], t[2], t[3]) for t in merged]


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
    run: list of (xc, raw).  Stat columns are evenly spaced (~12-40px); a stray
    prose single-letter label ('a', 'I' ...) sits ~100px from the real block.
    Split the run at outsized gaps and keep the longest sub-run.
    """
    if len(run) <= 1:
        return run
    xcs = [xc for xc, _ in run]
    gaps = [xcs[i + 1] - xcs[i] for i in range(len(xcs) - 1)]
    med = statistics.median(gaps)
    thresh = max(50.0, 2.5 * med)
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


def normalise_columns(run):
    """
    run: list of (xc, raw_label)  (already the contiguous label run).
    Returns list of columns: [{"label":canon, "xc":float, "drop":bool}].
    Handles: Front/Side/Rear + 'Armour' merge, F/S/R triple relabel, Page drop.
    """
    toks = [(xc, raw.lower()) for xc, raw in run]

    # 1) merge  X + armour  (X in front/side/rear)
    merged = []
    k = 0
    while k < len(toks):
        xc, lab = toks[k]
        if lab in ("front", "side", "rear") and k + 1 < len(toks) and toks[k + 1][1] in ("armour", "armor"):
            nxc = 0.5 * (xc + toks[k + 1][0])
            merged.append((nxc, lab))
            k += 2
        else:
            merged.append((xc, lab))
            k += 1
    toks = merged

    # 2) relabel a consecutive single-letter f,s,r triple -> front,side,rear
    labs = [l for _, l in toks]
    for a in range(len(labs) - 2):
        if labs[a] == "f" and labs[a + 1] == "s" and labs[a + 2] == "r":
            toks[a] = (toks[a][0], "front")
            toks[a + 1] = (toks[a + 1][0], "side")
            toks[a + 2] = (toks[a + 2][0], "rear")

    # 3) canonicalise + resolve duplicate labels
    cols = []
    seen = {}
    for xc, lab in toks:
        canon = CANON.get(lab, lab.upper())
        key = canon
        if canon in seen and canon not in DROP_LABELS:
            seen[canon] += 1
            key = "%s#%d" % (canon, seen[canon])
        else:
            seen.setdefault(canon, 1)
        cols.append({"label": key, "xc": xc, "drop": canon in DROP_LABELS})
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
        real = [c for c in cols if not c["drop"]]
        if len(real) < 3:
            continue
        headers.append({"y": ry, "cols": cols})
    headers.sort(key=lambda h: h["y"])
    return headers


def title_above(rows, header_y):
    """Best-effort datasheet title: nearest all-caps line above the header."""
    best = None
    for ry, rtoks in rows:
        if ry >= header_y - 2 or ry < header_y - 220:
            continue
        alpha = [t[3] for t in rtoks if has_alpha(t[3])]
        if not alpha:
            continue
        letters = "".join(c for t in alpha for c in t if c.isalpha())
        if len(letters) < 4:
            continue
        upper = sum(1 for c in letters if c.isupper())
        if upper / max(1, len(letters)) < 0.8:
            continue
        txt = " ".join(alpha).strip()
        if 2 <= len(txt) <= 60:
            if best is None or ry > best[0]:
                best = (ry, txt)
    return best[1] if best else None


# ----------------------------------------------------------------------------
# Value-row parsing
# ----------------------------------------------------------------------------
FIELD_LABELS = {
    "unit composition", "unit type", "wargear", "special rules", "options",
    "composition", "type", "points", "psychic powers", "dedicated transport",
    "transport", "crew", "weapons", "type:", "access points",
}


def parse_name(rtoks, first_xc, max_tokens=5, window=130.0, near=95.0, edge_gap=18.0):
    """
    The unit name: the contiguous word cluster immediately left of the first
    stat column.  Name-internal word gaps are tiny (~2-6px); the jump to any
    preceding prose is much larger (~30px+), so we cluster right-to-left on the
    horizontal EDGE gap and stop at the first large gap.
    """
    cand = []
    for (yc, x0, x1, txt) in rtoks:
        xc = 0.5 * (x0 + x1)
        if xc < first_xc - 2 and xc > first_xc - window and has_alpha(txt):
            cand.append((x0, x1, txt))
    if not cand:
        return ""
    cand.sort(key=lambda c: c[0])  # left -> right
    # rightmost token must sit close to the stat block, else this isn't a name
    if 0.5 * (cand[-1][0] + cand[-1][1]) < first_xc - near:
        return ""
    kept = [cand[-1]]
    for i in range(len(cand) - 2, -1, -1):
        gap = kept[0][0] - cand[i][1]  # left neighbour's right edge
        if gap <= edge_gap:
            kept.insert(0, cand[i])
        else:
            break
    if len(kept) > max_tokens:
        return ""  # a long tight run == flowing prose, not a name
    name = " ".join(t for _, _, t in kept)
    name = name.replace("\u2022", "").strip(" .,-\u2013\u2014")
    return name.strip()


def parse_value_row(rtoks, cols):
    """Map a value row to columns. Returns (name, profile_dict, soft_reason|None)."""
    real_cols = cols  # includes drop cols for mapping
    xcs = [c["xc"] for c in real_cols]
    first_xc = min(xcs)
    gaps = [xcs[i + 1] - xcs[i] for i in range(len(xcs) - 1)]
    med = statistics.median(gaps) if gaps else 12.0
    tol = max(5.0, 0.6 * med)

    name = parse_name(rtoks, first_xc)

    assigned = {}
    collision = False
    for (yc, x0, x1, txt) in rtoks:
        if not is_value(txt):
            continue
        xc = 0.5 * (x0 + x1)
        # nearest column
        j = min(range(len(xcs)), key=lambda k: abs(xcs[k] - xc))
        if abs(xcs[j] - xc) > tol:
            continue
        lab = real_cols[j]["label"]
        if lab in assigned:
            collision = True
        assigned[lab] = txt

    # build profile excluding dropped columns
    profile = {}
    for c in real_cols:
        if c["drop"]:
            continue
        if c["label"] in assigned:
            profile[c["label"]] = assigned[c["label"]]

    ncols = sum(1 for c in real_cols if not c["drop"])
    need = max(2, math.ceil(ncols / 2.0))
    if not name or len(profile) < need:
        return None
    if name.endswith(":") or name.strip().lower() in FIELD_LABELS:
        return None
    if name.lower() in LABELS:
        return None
    # real datasheet names are Title-Case / ALLCAPS; a lower-case lead == prose
    first = name.lstrip("'\"([")[:1]
    if first.isalpha() and not first.isupper():
        return None
    soft = "column collision (ambiguous x-mapping)" if collision else None
    return name, profile, soft


def harvest_header_book(doc, book, edition, cite_book):
    """Harvest a book whose tables have readable header rows."""
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
            ctx = title_above(rows, h["y"])
            got = 0
            misses = 0
            for ry, rtoks in rows:
                if ry <= h["y"] + 1:
                    continue
                if ry >= next_hy - 1:
                    break
                if ry - h["y"] > 500:
                    break
                parsed = parse_value_row(rtoks, h["cols"])
                if parsed is None:
                    if got >= 1:
                        misses += 1
                        if misses >= 2:
                            break
                    continue
                misses = 0
                got += 1
                name, profile, soft = parsed
                row = {
                    "name": name,
                    "profile": profile,
                    "edition": edition,
                    "system": SYSTEM,
                    "book": cite_book,
                    "citation": "%s [PDF page %d]" % (cite_book, page_no),
                }
                if ctx:
                    row["unit_context"] = ctx
                if soft:
                    row["soft"] = soft
                    soft_out.append({"citation": row["citation"], "name": name,
                                     "reason": soft, "profile": profile})
                rows_out.append(row)

    attach_special_rules(doc, rows_out, cite_book)
    return rows_out, soft_out, coverage_gaps


def harvest_positional_book(doc, book, edition, cite_book):
    """
    Harvest a book with NO header labels in its text layer (Codex Imperialis).
    Capture name + raw ordered values positionally; flag every row soft.
    """
    rows_out = []
    soft_out = []
    reason = ("2nd-ed profile: characteristic labels are not in the PDF text "
              "layer (imaged); values captured positionally as c1..cN, unlabeled; "
              "text layer is OCR-mangled")
    for i in range(doc.page_count):
        words = doc[i].get_text("words")
        rows = cluster_rows(words)
        page_no = i + 1
        for ry, rtoks in rows:
            # first value token in the row
            fv = None
            for idx, (yc, x0, x1, txt) in enumerate(rtoks):
                if is_value(txt):
                    fv = idx
                    break
            if fv is None or fv == 0:
                continue
            first_v_x0 = rtoks[fv][1]
            # name = tight contiguous alpha cluster immediately left of the values
            name = parse_name(rtoks, 0.5 * (rtoks[fv][1] + rtoks[fv][2]),
                              max_tokens=3, window=120.0, near=62.0, edge_gap=16.0)
            if not name or len(name) < 2 or not has_alpha(name):
                continue
            if name.endswith(":") or name.strip().lower() in FIELD_LABELS:
                continue
            # contiguous run of value tokens
            vals = []
            for (yc, x0, x1, txt) in rtoks[fv:]:
                if is_value(txt):
                    vals.append(txt)
                else:
                    break
            if not (7 <= len(vals) <= 13):
                continue
            profile = {("c%d" % (k + 1)): v for k, v in enumerate(vals)}
            row = {
                "name": name,
                "profile": profile,
                "edition": edition,
                "system": SYSTEM,
                "book": cite_book,
                "citation": "%s [PDF page %d]" % (cite_book, page_no),
                "soft": reason,
            }
            rows_out.append(row)
            soft_out.append({"citation": row["citation"], "name": name,
                             "reason": reason, "profile": profile})
    attach_special_rules(doc, rows_out, cite_book)
    return rows_out, soft_out, []


# ----------------------------------------------------------------------------
# Book / edition helpers
# ----------------------------------------------------------------------------
def clean_book_name(fname):
    stem = os.path.splitext(fname)[0]
    stem = re.sub(r"^Warhammer 40k - Codex - ", "", stem)
    return stem.strip()


def infer_edition(fname):
    m = re.search(r"(\d)(st|nd|rd|th)\s+Edition", fname, re.I)
    if m:
        return (m.group(1) + m.group(2)).lower()
    return "unknown"


def dedupe_within_book(rows):
    """Collapse exact (book, name, profile) duplicates (summary vs datasheet)."""
    seen = set()
    out = []
    removed = 0
    for r in rows:
        nkey = re.sub(r"\s+", "", r["name"].lower())
        key = (r["book"], nkey, tuple(sorted(r["profile"].items())))
        if key in seen:
            removed += 1
            continue
        seen.add(key)
        out.append(r)
    return out, removed


# ----------------------------------------------------------------------------
# Top-level harvest
# ----------------------------------------------------------------------------
# Codex Imperialis is treated positionally regardless of stray tokens.
POSITIONAL_BOOKS = {"Codex Imperialis - 1993 - 2nd Edition"}


def harvest_all(verbose=True):
    result = {
        "rows": [],
        "soft": [],
        "per_book": {},
        "per_book_rules": {},
        "digital": [],
        "no_coverage": [],
        "page_gaps": [],
        "rule_gaps": [],
    }
    if not os.path.isdir(SRC_DIR):
        sys.stderr.write("FATAL: source dir not found: %s\n" % SRC_DIR)
        return result

    files = sorted(f for f in os.listdir(SRC_DIR) if f.lower().endswith(".pdf"))
    for fname in files:
        path = os.path.join(SRC_DIR, fname)
        try:
            doc = fitz.open(path)
        except Exception as e:
            if verbose:
                print("NO COVERAGE: %s (open failed: %s)" % (fname, e))
            result["no_coverage"].append(fname)
            continue

        if not is_digital(doc):
            if verbose:
                print("NO COVERAGE: %s (scanned, image-only)" % fname)
            result["no_coverage"].append(fname)
            doc.close()
            continue

        cite_book = clean_book_name(fname)
        edition = infer_edition(fname)
        result["digital"].append(fname)

        if cite_book in POSITIONAL_BOOKS:
            rows, soft, gaps = harvest_positional_book(doc, fname, edition, cite_book)
        else:
            rows, soft, gaps = harvest_header_book(doc, fname, edition, cite_book)

        rows, removed = dedupe_within_book(rows)
        result["rows"].extend(rows)
        result["soft"].extend(soft)
        result["per_book"][cite_book] = len(rows)
        result["per_book_rules"][cite_book] = sum(
            bool(r.get("special_rules")) for r in rows)
        for row in rows:
            if row.get("special_rules"):
                continue
            note = ("%s / %s (no unambiguous explicit SPECIAL RULES section)"
                    % (cite_book, row["name"]))
            result["rule_gaps"].append(note)
            if verbose:
                print("NO COVERAGE: " + note)
        for (pno, why) in gaps:
            note = "%s [PDF page %d]: %s" % (cite_book, pno, why)
            result["page_gaps"].append(note)
            if verbose:
                print("NO COVERAGE: " + note)
        if verbose:
            extra = " (%d exact dupes merged)" % removed if removed else ""
            print("DIGITAL: %s -> %d profiles, %d with special rules%s"
                  % (cite_book, len(rows),
                     result["per_book_rules"][cite_book], extra))

        # incremental progress
        try:
            os.makedirs(os.path.dirname(PROGRESS), exist_ok=True)
            with open(PROGRESS, "w", encoding="utf-8") as fh:
                json.dump({
                    "done_books": list(result["per_book"].keys()),
                    "per_book": result["per_book"],
                    "per_book_rules": result["per_book_rules"],
                    "total_rows": len(result["rows"]),
                    "total_rules": sum(result["per_book_rules"].values()),
                    "digital": result["digital"],
                    "no_coverage": result["no_coverage"],
                    "rule_gaps": result["rule_gaps"],
                }, fh, indent=2)
        except Exception:
            pass
        doc.close()

    return result


# ----------------------------------------------------------------------------
# Output writers
# ----------------------------------------------------------------------------
def profile_str(profile):
    return " ".join("%s%s" % (k, v) for k, v in profile.items())


def write_outputs(result):
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    payload = {
        "system": SYSTEM,
        "note": ("Warhammer 40,000 tabletop WARGAME unit profiles (datasheet "
                 "characteristic lines). Distinct from the WH40K Roleplay line. "
                 "Extracted from born-digital codex PDF text layers only; scanned "
                 "codexes are listed under no_coverage."),
        "methodology_notes": [
            "Profiles reconstructed geometrically from the PDF text layer (PyMuPDF "
            "words mode): a header row of characteristic labels fixes each column's "
            "x-centre, and every value row maps its stat tokens to the nearest "
            "column. No number is ever guessed or corrected -- unreadable cells are "
            "left empty.",
            "Unit-local SPECIAL RULES sections are attached verbatim from the same "
            "born-digital PDF, with their own PDF-page citations. Multi-profile "
            "datasheets share one rules block; summary-only vehicles are matched to "
            "their named unit page. Ambiguous or absent sections remain empty.",
            "3rd-5th ed infantry schema: WS BS S T W I A Ld Sv (some tables prefix a "
            "Points column). Values keep any parenthetical modifiers verbatim, e.g. "
            "T4(5) on bikes, S6(10) / A2(3) on Dreadnoughts.",
            "Vehicles use Armour Values: tanks are BS + Front/Side/Rear; walkers are "
            "WS BS S (Front Side Rear) I A. The header token 'Armour' is merged into "
            "its Front/Side/Rear column, and a walker's abbreviated F/S/R triple is "
            "relabelled Front/Side/Rear so it never collides with S (Strength).",
            "Codex Imperialis 1993 (2nd ed) is a special case: its profile tables' "
            "characteristic labels are NOT in the PDF text layer (they are part of "
            "the table graphic) and the surrounding text is OCR-mangled. Its rows are "
            "therefore captured POSITIONALLY -- name + raw ordered values under c1..cN "
            "keys -- and EVERY such row is flagged 'soft'. The 2nd-ed M/WS/BS/.../Int/"
            "Cl/WP labels are intentionally NOT fabricated onto these values.",
            "Summary/reference tables duplicate per-datasheet profiles; exact "
            "(name, profile) duplicates are merged within each book (space/case "
            "insensitive), keeping the datasheet citation.",
        ],
        "total_profiles": len(result["rows"]),
        "profiles_with_special_rules": sum(result["per_book_rules"].values()),
        "digital_books": [clean_book_name(f) for f in result["digital"]],
        "no_coverage_scanned": [clean_book_name(f) for f in result["no_coverage"]],
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
    lines.append("# Warhammer 40,000 Wargame -- Unit Profile Index")
    lines.append("")
    lines.append("**System:** WH40K (tabletop wargame -- NOT the 40K Roleplay line)  ")
    lines.append("**Total profiles:** %d  " % len(result["rows"]))
    lines.append("**Profiles with attached special rules:** %d"
                 % sum(result["per_book_rules"].values()))
    lines.append("**Soft / uncertain rows:** %d  " % len(result["soft"]))
    lines.append("")
    lines.append("Extracted geometrically from the PDF text layer (PyMuPDF words "
                 "mode). Only born-digital codexes are covered; the 45 scanned, "
                 "image-only codexes are listed below as NO COVERAGE.")
    lines.append("")
    lines.append("## Methodology")
    lines.append("")
    for n in payload["methodology_notes"]:
        lines.append("- %s" % n)
    lines.append("")
    lines.append("## Digital books harvested")
    lines.append("")
    lines.append("| Book | Edition | Profiles | With rules |")
    lines.append("| --- | --- | --- | --- |")
    for f in result["digital"]:
        cb = clean_book_name(f)
        lines.append("| %s | %s | %d | %d |" % (
            cb, infer_edition(f), result["per_book"].get(cb, 0),
            result["per_book_rules"].get(cb, 0)))
    lines.append("")
    lines.append("## NO COVERAGE (scanned, image-only)")
    lines.append("")
    for f in result["no_coverage"]:
        lines.append("- %s" % clean_book_name(f))
    lines.append("")
    if result["page_gaps"]:
        lines.append("## NO COVERAGE (digital pages whose profiles could not be parsed)")
        lines.append("")
        for g in result["page_gaps"]:
            lines.append("- %s" % g)
        lines.append("")
    if result["rule_gaps"]:
        lines.append("## NO COVERAGE (unit special rules)")
        lines.append("")
        lines.append("These profiles have no unambiguous explicit SPECIAL RULES "
                     "section in the born-digital text layer; no text was guessed.")
        lines.append("")
        for g in result["rule_gaps"]:
            lines.append("- %s" % g)
        lines.append("")

    # profiles grouped by book
    by_book = {}
    for r in result["rows"]:
        by_book.setdefault(r["book"], []).append(r)
    for cb in sorted(by_book.keys()):
        lines.append("## %s" % cb)
        lines.append("")
        lines.append("| Unit | Profile | Edition | Citation | Rules | Soft |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for r in by_book[cb]:
            soft = "yes" if "soft" in r else ""
            rules = "yes" if r.get("special_rules") else ""
            nm = r["name"].replace("|", "\\|")
            pr = profile_str(r["profile"]).replace("|", "\\|")
            lines.append("| %s | %s | %s | %s | %s | %s |" %
                         (nm, pr, r["edition"], r["citation"], rules, soft))
        lines.append("")

    with open(OUT_MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


# ----------------------------------------------------------------------------
# Self test
# ----------------------------------------------------------------------------
def _synthetic_chapter_master():
    """A minimal words-list encoding the Space Marines p54 fixture geometry."""
    hdr = [
        (383.04, 393.83, "WS"), (401.04, 410.42, "BS"), (417.60, 421.86, "S"),
        (431.28, 435.44, "T"), (443.52, 451.32, "W"), (461.04, 463.34, "I"),
        (473.28, 478.19, "A"), (486.24, 494.36, "Ld"), (500.16, 508.35, "Sv"),
    ]
    val = [
        (296.40, 323.68, "Chapter"), (326.68, 349.33, "Master"),
        (387.36, 391.14, "6"), (403.44, 407.22, "5"), (416.88, 421.47, "4"),
        (431.28, 435.87, "4"), (445.68, 449.46, "3"), (460.08, 463.86, "5"),
        (474.00, 477.78, "3"), (486.48, 495.10, "10"), (499.68, 507.50, "3+"),
    ]
    words = []
    for (x0, x1, t) in hdr:
        words.append((x0, 397.55, x1, 405.0, t, 0, 0, 0))
    for (x0, x1, t) in val:
        words.append((x0, 407.39, x1, 415.0, t, 0, 0, 0))
    return words


def selftest():
    ok = True

    # (a) synthetic fixture
    words = _synthetic_chapter_master()
    rows = cluster_rows(words)
    headers = find_headers(rows)
    assert len(headers) == 1, "expected exactly one header, got %d" % len(headers)
    h = headers[0]
    labels = [c["label"] for c in h["cols"]]
    assert labels == ["WS", "BS", "S", "T", "W", "I", "A", "Ld", "Sv"], labels
    # the value row
    parsed = None
    for ry, rtoks in rows:
        if ry > h["y"] + 1:
            parsed = parse_value_row(rtoks, h["cols"])
            break
    assert parsed is not None, "value row failed to parse"
    name, profile, soft = parsed
    assert name == "Chapter Master", repr(name)
    expect = {"WS": "6", "BS": "5", "S": "4", "T": "4", "W": "3",
              "I": "5", "A": "3", "Ld": "10", "Sv": "3+"}
    assert profile == expect, profile
    print("selftest: synthetic Chapter Master fixture OK -> %s | %s"
          % (name, profile_str(profile)))

    # (a2) live page-54 fixture (guarded)
    sm = os.path.join(SRC_DIR, "Warhammer 40k - Codex - Space Marines - 2008 - 5th Edition.pdf")
    if os.path.isfile(sm):
        doc = fitz.open(sm)
        pg = doc[53]  # 1-indexed page 54
        rows = cluster_rows(pg.get_text("words"))
        hs = find_headers(rows)
        found = False
        for h in hs:
            if [c["label"] for c in h["cols"]] != \
               ["WS", "BS", "S", "T", "W", "I", "A", "Ld", "Sv"]:
                continue
            for ry, rtoks in rows:
                if ry <= h["y"] + 1:
                    continue
                p = parse_value_row(rtoks, h["cols"])
                if p and p[0] == "Chapter Master":
                    assert p[1] == expect, p[1]
                    found = True
                    break
            if found:
                break
        doc.close()
        assert found, "live SM2008 p54 Chapter Master row not found/parsed"
        print("selftest: live SM2008 p54 Chapter Master OK")
    else:
        print("selftest: live SM2008 fixture skipped (PDF not present)")

    # (b) live-harvest invariants
    res = harvest_all(verbose=False)
    rows = res["rows"]
    total = len(rows)
    expected_counts = {
        "Blood Angels - 2007 - 5th Edition": 41,
        "Codex Imperialis - 1993 - 2nd Edition": 23,
        "Harlequins": 18,
        "Space Marines - 2008 - 5th Edition": 54,
    }
    assert total == 136, "expected 136 locked profiles, got %d" % total
    assert res["per_book"] == expected_counts, res["per_book"]
    for r in rows:
        assert r["system"] == "WH40K", "row not labelled WH40K: %r" % r
        assert r["name"] and has_alpha(r["name"]), "empty/invalid name: %r" % r
        assert isinstance(r["profile"], dict) and r["profile"], \
            "empty profile: %r" % r
        assert "[PDF page" in r["citation"], "bad citation: %r" % r
        low = r["name"].lower()
        assert low not in LABELS, "header token leaked as name: %r" % r
        assert not re.match(r"^(ws|bs|ld|sv)\b", low), "header leak: %r" % r
        if r.get("special_rules"):
            assert r.get("rules_citations"), "rules missing citation: %r" % r
            assert all("[PDF page" in c for c in r["rules_citations"]), r
            assert not re.search(
                r"(?mi)^\s*(?:WARGEAR|OPTIONS|WS\s+BS)\s*$",
                r["special_rules"]), "rule span leaked a new section: %r" % r

    attached = sum(bool(r.get("special_rules")) for r in rows)
    assert attached == 118, "expected 118 rule attachments, got %d" % attached
    assert len(res["rule_gaps"]) == 18, res["rule_gaps"]
    keyed = {(r["book"], r["name"]): r for r in rows}
    assert "Orbital Bombardment" in keyed[
        ("Space Marines - 2008 - 5th Edition", "Chapter Master")]["special_rules"]
    assert "Inspiring." in keyed[
        ("Blood Angels - 2007 - 5th Edition", "Lord Dante")]["special_rules"]
    assert "Holo suit" in keyed[("Harlequins", "Great Harlequin")]["special_rules"]
    # at least the four expected digital books were seen
    assert len(res["digital"]) == 4, "expected 4 digital books, got %d" % len(res["digital"])
    assert len(res["no_coverage"]) >= 40, "expected many scanned books"
    print("selftest: live-harvest invariants OK "
          "(total=%d, rules=%d, digital=%d, scanned=%d, soft=%d)"
          % (total, attached, len(res["digital"]),
             len(res["no_coverage"]), len(res["soft"])))

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

    print("Harvesting WH40K wargame unit profiles from born-digital codexes...")
    res = harvest_all(verbose=True)
    write_outputs(res)
    print("")
    print("Wrote %s (%d profiles)" % (OUT_JSON, len(res["rows"])))
    print("Wrote %s" % OUT_MD)
    print("Digital books: %d | Rules: %d/%d | "
          "Scanned (NO COVERAGE): %d | Soft rows: %d"
          % (len(res["digital"]), sum(res["per_book_rules"].values()),
             len(res["rows"]), len(res["no_coverage"]), len(res["soft"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
