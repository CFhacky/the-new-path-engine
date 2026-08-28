#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Harvest CHAOS MUTATIONS and GIFTS OF THE CHAOS GODS from Warhammer Fantasy
Roleplay (WFRP 2e) and write reference/wfrp_mutation_index.{json,md}.

Each row is ONE mutation or ONE Chaos gift, tagged with its d100/d1000 roll and
its mechanical effect text, RAW from the book. This index is DISTINCT from
reference/wfrp_creature_index.* (creature profiles) -- no creature stats here.

Primary source (born-digital clean text, not OCR):
    I:\\Sourcebooks\\_text\\Warhammer\\Fantasy\\Tome_of_Corruption.md
Secondary:
    I:\\Sourcebooks\\_text\\Warhammer\\Fantasy\\Nights_Dark_Masters_Lost_Bloodlines.md

Tables harvested (Tome of Corruption, WFRP 2e):
    Mutations : Table 3-1 (master d1000), 3-2 Khorne, 3-3 Nurgle, 3-4 Slaanesh,
                3-5 Tzeentch  -- all reference one shared "Mutations Defined"
                glossary for effect text.
    Gifts     : Table 13-1 Rewards of Chaos (undivided), 13-3 Khorne, 13-4
                Nurgle, 13-5 Slaanesh, 13-6 Tzeentch.
Lost Bloodlines (WFRP 2e): the in-file "New Blood Gifts" (a handful of Vampire
    blood gifts whose full effect text is present in the folder); the remaining
    Blood Gift table entries reference the parent Night's Dark Masters (not in
    the folder) and are reported as NO COVERAGE.

INVIOLABLE: book RAW only -- never invent/guess a value. If an entry's effect is
layout-tangled and cannot be cleanly separated, its effect is left empty and the
row is recorded in the `soft` list. Every row is stamped system="WFRP",
edition="WFRP 2e" and cited to book + PDF page. Stdlib only, self-contained.

Usage:
    python wfrp_mutation_harvest.py --selftest      # fixtures + live invariants
    python wfrp_mutation_harvest.py                 # write the two index files
    python wfrp_mutation_harvest.py --debug         # harvest + diagnostics, no write
    python wfrp_mutation_harvest.py --search TEXT    # grep harvested rows
"""

import argparse
import json
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #
SYSTEM = "WFRP"
EDITION = "WFRP 2e"

CORPUS = Path(r"I:\Sourcebooks\_text")
FANTASY = CORPUS / "Warhammer" / "Fantasy"

TOME_FILE = "Tome_of_Corruption.md"
TOME_BOOK = "WFRP: Tome of Corruption"
LOST_FILE = "Nights_Dark_Masters_Lost_Bloodlines.md"
LOST_BOOK = "WFRP: Night's Dark Masters -- Lost Bloodlines"

# repo layout: this file lives in <repo>/scripts/
REPO = Path(__file__).resolve().parent.parent
REF_DIR = REPO / "reference"
OUT_JSON = REF_DIR / "wfrp_mutation_index.json"
OUT_MD = REF_DIR / "wfrp_mutation_index.md"

PROGRESS = Path(
    r"C:\Users\Chad\AppData\Local\Temp\claude"
    r"\I--repos-the-new-path-engine--claude-worktrees-intelligent-lamport-3a158a"
    r"\1c5f36b4-d94a-4698-95d9-c2304f8a0818\scratchpad\wfrp_mutation_progress.json"
)

# dash characters seen in the born-digital text: en-dash, em-dash, figure-dash,
# non-breaking hyphen, hyphen-minus.  DASHCHARS is for use INSIDE a character
# class; DASHCLASS is the standalone bracket expression.
DASHCHARS = "\u2013\u2014\u2012\u2011-"
DASHCLASS = "[" + DASHCHARS + "]"
ENDASH = "\u2013"

PAGE_RE = re.compile(r"\[PDF page (\d+)\]")
ROLL_RE = re.compile(r"^\d{1,4}\s*(?:" + DASHCLASS + r"\s*\d{1,4})?$")
# a glossary Fear-RATING line: "Fear <value>" where <value> is a real fear
# rating -- a number ("2", "10"), a slash/dash form ("1/2/3", "-1/-2/-3"), or one
# of the special words.  Deliberately does NOT match name-phrases that merely
# begin with "Fear" ("Fear of Blood") or the format sidebar ("Fear Number").
_FVAL = "[" + DASHCHARS + r"]?\d[\d/\s" + DASHCHARS + r"]*"
FEARLINE_RE = re.compile(
    r"^Fear\s+(?:" + _FVAL + r"|n/a|N/A|Special|Varies|None|Nil)\s*$")
FEAR_VALUE_RE = re.compile(r"^Fear\s+(.*\S)\s*$")
TYPE_RE = re.compile(r"^Type:\s*(Single|Multiple)", re.IGNORECASE)
# a fear cell inside an index table: 0-9, "10", a range "0-1", or a slash form
# such as Growth's "1/2/3".  (The authoritative Fear value is taken from the
# glossary; this pattern only needs to bound the [fear, page] record tail.)
FEARCELL_RE = re.compile(
    r"^" + DASHCLASS + r"?(?:10|[0-9])"
    r"(?:\s*/\s*" + DASHCLASS + r"?[0-9])*"
    r"(?:\s*" + DASHCLASS + r"\s*[0-9])?$")
# a page cell inside an index table (printed book page, always >=2 digits here)
PAGECELL_RE = re.compile(r"^\d{2,3}$")

HEADER_TOKENS = {
    "d1000", "roll", "mutation", "fear", "points", "page", "result",
    "fear points", "extras", "extras\u2026",
}

# boxed sidebars in Chapter III that the PDF interleaves between a mutation's
# prose and its continuation; a glossary body must stop at these headings so it
# does not absorb non-mutation text.
SIDEBAR_STOP = {
    "adjudicating mutations", "mutation format", "virulent plagues",
    "mutations defined", "mutations of the ruinous powers", "quick mutants",
    "fate points and mutations", "special considerations",
    "mutant adventure seeds", "sample chaos spawn", "special rules",
    "using chaos spawn", "chaos spawn attacks",
}

# structural labels that never occur inside a single mutation's own effect;
# their appearance means the capture ran into a foreign block (a disease stat,
# the format sidebar, or the next entry).  Used as a truncation safety net.
FOREIGN_MARKER_RE = re.compile(
    r"Type:\s*(?:Single|Multiple)\b|Description:|Duration:\s*\d|"
    r"Adjudicating Mutations|Mutation Format|Virulent Plagues")

# a creature/career STAT BLOCK that the PDF places after an entry's prose (a
# Cross-Breed profile, a Daemon advance scheme, a steed's Skills/Talents list).
# Anchored on real block headers so legit prose ('on your Main Profile') is kept.
STATBLOCK_RE = re.compile(
    r"[\"'“‘”’]?\s*\w[\w ]*Advance Scheme"
    r"|Main Profile\s+WS\b"
    r"|Secondary Profile\s+A\s+W\b"
    r"|Becoming an [A-Z]"
    r"|Career Entries\b|Career Exits\b"
    r"|Weapon Skill\s*\(WS\)"
    r"|\bSkills:\s|\bTalents:\s|\bTrappings:\s")


def trim_statblock(text):
    """Truncate an effect at a leaked creature/career stat block, if present."""
    m = STATBLOCK_RE.search(text)
    if m and m.start() > 0:
        return text[:m.start()].strip()
    return text

# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #


def norm_dash(s):
    """Standardise every dash variant to a single en-dash."""
    return re.sub(DASHCLASS, ENDASH, s)


# genuine short-form name variants confirmed identical via the index's printed
# page reference matching the glossary entry's page (printed + 2 = PDF page):
#   "Scales" (master index, printed p.49) == glossary "Scaly Skin" (PDF p.51)
ALIASES = {"scales": "scaly skin"}


def norm_key(s):
    """Normalise a name for cross-table matching.  Hyphens/dashes collapse to
    spaces so 'Iron-hard Skin' (index) matches 'Iron Hard Skin' (glossary)."""
    s = s.strip().lower()
    s = re.sub(r"[\u2026]", "...", s)              # ellipsis char -> ...
    s = re.sub(r"\.\.\.$", "", s)                  # drop trailing ellipsis
    s = re.sub(r"\s*\(cosmetic\)\s*$", "", s)      # drop (Cosmetic) tag
    s = re.sub(DASHCLASS, " ", s)                  # dashes/hyphens -> space
    s = s.replace("\u2019", "'")                   # curly apostrophe
    s = re.sub(r"^the\s+", "", s)                  # leading "The "
    s = re.sub(r"[.*:]+$", "", s)                  # trailing punctuation
    s = re.sub(r"\s+", " ", s).strip()
    return ALIASES.get(s, s)


def clean_text(s):
    """Whitespace-normalise a captured effect string (RAW words preserved)."""
    s = s.replace("\u00ad", "")                    # soft hyphen
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    # de-hyphenate words split across the PDF's hard line wraps: "reddish- tan"
    s = re.sub(r"(\w)-\s+(\w)", r"\1\2", s)
    return s.strip()


def is_blank(s):
    return s.strip() == ""


# --------------------------------------------------------------------------- #
# Stream: strip running headers / page markers, keep (pdf_page, text) per line
# --------------------------------------------------------------------------- #


def build_stream(raw_lines):
    """Return list of (pdf_page:int|None, text:str) with structural noise removed.

    Drops the '## [PDF page N]' markers, the printed running-header page number,
    and the running chapter/book header line that follows each page break.
    """
    out = []
    page = None
    i = 0
    n = len(raw_lines)
    hdr_re = re.compile(r"^(Chapter\s+[IVXLCDM]+\s*:|Lost Bloodlines:)")
    while i < n:
        ln = raw_lines[i].rstrip("\n").rstrip("\r")
        m = PAGE_RE.search(ln)
        if ln.lstrip().startswith("## [PDF page") and m:
            page = int(m.group(1))
            i += 1
            # skip blank lines directly after the marker
            while i < n and is_blank(raw_lines[i]):
                i += 1
            # running header pattern is "<printed page number>" then "Chapter ..:"
            if i < n and re.fullmatch(r"\d{1,4}", raw_lines[i].strip()):
                j = i + 1
                while j < n and is_blank(raw_lines[j]):
                    j += 1
                if j < n and hdr_re.match(raw_lines[j].strip()):
                    i = j + 1                       # eat page-no AND header line
                    continue
                # a bare integer NOT followed by a header is real content -> keep
            if i < n and hdr_re.match(raw_lines[i].strip()):
                i += 1                              # header with no page-no line
                continue
            continue
        out.append((page, ln))
        i += 1
    return out


# --------------------------------------------------------------------------- #
# Mutation index tables (Table 3-1 .. 3-5): vertical [roll, name, fear, page]
# --------------------------------------------------------------------------- #


def find_table(stream, label_regex):
    """Return the index in `stream` of the line whose text matches label_regex."""
    for idx, (_pg, txt) in enumerate(stream):
        if label_regex.search(txt):
            return idx
    return -1


def _is_header_line(txt):
    t = norm_dash(txt).strip().lower().rstrip(".")
    return t in HEADER_TOKENS


_CAPTION_RE = re.compile(r"^Table\s+\d+\s*" + DASHCLASS + r"?\s*\d*\s*:")


def _is_index_header_here(stream, i):
    """True if stream[i] begins a mutation-index column header ('Roll'/'D1000'
    then 'Mutation').  Distinguishes an index table from a description's own
    sub-table (whose 'Roll' is followed by a custom label, not 'Mutation')."""
    n = len(stream)
    if i >= n:
        return False
    t = norm_dash(stream[i][1]).strip()
    if t not in ("Roll", "D1000"):
        return False
    j = _next_nonblank(stream, i + 1)
    return j < n and norm_dash(stream[j][1]).strip().lower() == "mutation"


def _is_table_caption_line(txt):
    """True for a real table CAPTION line (a short 'Table N-M: Title'), NOT a
    prose sentence that merely references a table mid-flow (e.g. 'Table 3-4:
    Mutations of Slaanesh and if Tzeentch, use Table 3-5: ...')."""
    t = norm_dash(txt).strip()
    # a caption is a short title with no trailing sentence period (prose
    # references like 'Table 3-1: Mutations.' DO end with a period)
    return bool(_CAPTION_RE.match(t)) and len(t) <= 45 and not t.endswith(".")


def _next_nonblank(stream, k):
    n = len(stream)
    while k < n and is_blank(stream[k][1]):
        k += 1
    return k


def is_pagecell(s):
    """True for an index 'Page' cell: a 2-3 digit printed book page (>=20).

    The >=20 floor separates a page number (chapter III pages are 27-56, gift
    pages 167-176) from a Fear-points value (0-10), so a Fear cell of '10'
    is never mistaken for the page that ends the record."""
    s = s.strip()
    return bool(PAGECELL_RE.match(s)) and 20 <= int(s) <= 600


def read_quad(stream, i):
    """Read ONE mutation-index record starting at stream[i] (a roll line).

    Record shape (vertical): roll / NAME / fear-cell(s) / page-cell.  The NAME is
    the first line after the roll (these index cells are never wrapped -- long
    names are truncated with an ellipsis, not wrapped).  The record ends at the
    page cell (a number >=20 whose following non-blank line is the next roll or a
    table boundary); everything between the name and the page is the Fear cell,
    whatever its shape ('3', '10', '1/2/3', '-1/-2/-3', 'Varies', 'Two Totals').
    Returns (roll, name, fear, page_ref, pdf_page, next_i) or None.
    """
    n = len(stream)
    pg, txt = stream[i]
    t = norm_dash(txt).strip()
    if not ROLL_RE.match(t) or t.lower().startswith("table"):
        return None
    j = _next_nonblank(stream, i + 1)
    if j >= n:
        return None
    name = clean_text(stream[j][1])
    ncheck = norm_dash(name).strip()
    if (not name or _is_header_line(name) or ROLL_RE.match(ncheck)
            or ncheck.lower().startswith("table")):
        return None
    # scan for the page cell that closes the record
    fear_lines = []
    j += 1
    steps = 0
    while j < n and steps < 10:
        s = norm_dash(stream[j][1]).strip()
        if is_blank(s):
            j += 1
            continue
        if _is_header_line(s) or (s.lower().startswith("table ") and ":" in s):
            break                                   # hit next chunk / caption
        if is_pagecell(s):
            k = _next_nonblank(stream, j + 1)
            nxt = norm_dash(stream[k][1]).strip() if k < n else ""
            if (k >= n or ROLL_RE.match(nxt) or _is_header_line(nxt)
                    or nxt.lower().startswith("table")):
                fear = clean_text(" ".join(fear_lines)) or None
                return (norm_dash(t), name, fear, s, pg, k)
        fear_lines.append(s)
        j += 1
        steps += 1
    return None


def parse_mut_chunk(stream, start_idx):
    """Parse one mutation-index column-chunk.

    `start_idx` may point at a 'Table' caption or a 'D1000'/'Roll' header line;
    the header token block is consumed, then records are read until the run
    breaks.  Returns (records, end_idx); each record is
    (roll, name, fear, page_ref, pdf_page).
    """
    i = start_idx + 1
    n = len(stream)
    while i < n and (_is_header_line(stream[i][1]) or is_blank(stream[i][1])):
        i += 1
    recs = []
    while i < n:
        q = read_quad(stream, i)
        if q is None:
            break
        roll, name, fear, page_ref, pg, nxt = q
        if name:
            recs.append((roll, name, fear, page_ref, pg))
        i = nxt
    return recs, i


def detect_mut_runs(stream, min_len=3):
    """Return [(start_idx, records)] for every maximal run of mutation-index
    quads in the stream (records as in parse_mut_chunk)."""
    runs = []
    i = 0
    n = len(stream)
    while i < n:
        q = read_quad(stream, i)
        if q is None:
            i += 1
            continue
        start = i
        recs = []
        while True:
            q = read_quad(stream, i)
            if q is None:
                break
            recs.append((q[0], q[1], q[2], q[3], q[4]))
            i = q[5]
        if len(recs) >= min_len:
            runs.append((start, recs))
    return runs


# --------------------------------------------------------------------------- #
# Gift / reward index tables (Table 13-1, 13-3 .. 13-6): vertical [roll, name]
# --------------------------------------------------------------------------- #


def parse_gift_index(stream, start_idx):
    """Parse a 2-column gift/reward index (roll / result-name).

    Returns (rows, end_idx, span) where rows are (roll:str, name:str,
    pdf_page:int|None) and span is (start_idx, end_idx) for later exclusion.
    """
    rows = []
    i = start_idx + 1
    n = len(stream)
    while i < n and (_is_header_line(stream[i][1]) or is_blank(stream[i][1])):
        i += 1
    while i < n:
        pg, txt = stream[i]
        t = norm_dash(txt).strip()
        if is_blank(t):
            i += 1
            continue
        if not ROLL_RE.match(t) or t.lower().startswith("table"):
            break
        roll = t
        # collect the result name (usually 1 line, occasionally wrapped)
        j = i + 1
        name_parts = []
        while j < n:
            a = norm_dash(stream[j][1]).strip()
            if is_blank(a):
                j += 1
                continue
            if ROLL_RE.match(a) or a.lower().startswith("table"):
                break
            name_parts.append(stream[j][1].strip())
            j += 1
            # gift result names are short; stop after the first non-blank line
            break
        name = clean_text(" ".join(name_parts))
        name = re.sub(r"\*+$", "", name).strip()     # drop footnote asterisks
        if name:
            rows.append((norm_dash(roll), name, pg))
        i = j
    return rows, i, (start_idx, i)


# --------------------------------------------------------------------------- #
# Mutation glossary ("Mutations Defined"): Name / Fear N / Type: / Description:
# --------------------------------------------------------------------------- #


def _bad_name_line(txt):
    """True if `txt` cannot be a glossary mutation NAME heading."""
    t = txt.strip()
    if not t:
        return True
    if FEARLINE_RE.match(norm_dash(t)):
        return True                                 # this IS a Fear-rating line
    low = t.lower()
    for pre in ("type:", "description:", "variations:", "roll", "table ",
                "chapter ", "note:", "example:", "d1000"):
        if low.startswith(pre):
            return True
    if _is_header_line(t):
        return True
    if ROLL_RE.match(norm_dash(t)):
        return True
    if len(t) > 64:
        return True
    return False


def _is_glossary_anchor(stream, i, page_hi=None):
    """True if stream[i] is a NAME heading immediately followed (skipping blanks)
    by a Fear-rating line -- the start of a 'Mutations Defined' entry."""
    n = len(stream)
    if i >= n:
        return False
    pg, txt = stream[i]
    if page_hi is not None and pg is not None and pg > page_hi:
        return False
    if _bad_name_line(txt):
        return False
    j = _next_nonblank(stream, i + 1)
    return j < n and bool(FEARLINE_RE.match(norm_dash(stream[j][1]).strip()))


def parse_mut_glossary(stream, page_lo=25, page_hi=62):
    """Return {norm_key: {name, fear, type, effect, page, soft}} for mutations.

    Anchored on the strong triple  Name / 'Fear N' / 'Type: Single|Multiple'.
    Guarded to Chapter III's PDF-page band so the anchor cannot fire elsewhere.
    """
    gloss = {}
    n = len(stream)
    i = 0
    while i < n:
        pg, txt = stream[i]
        if pg is not None and not (page_lo <= pg <= page_hi):
            i += 1
            continue
        if not _is_glossary_anchor(stream, i, page_hi):
            i += 1
            continue
        name = clean_text(txt)
        j = _next_nonblank(stream, i + 1)           # the Fear-rating line
        fm = FEAR_VALUE_RE.match(norm_dash(stream[j][1]).strip())
        fear = norm_dash(fm.group(1)).strip() if fm else None
        # an optional 'Type:' line may follow the Fear rating
        k = _next_nonblank(stream, j + 1)
        typ = None
        body_start = j + 1
        if k < n and stream[k][1].strip().lower().startswith("type:"):
            typ = stream[k][1].strip()
            body_start = k + 1
        body, end = _collect_glossary_body(stream, body_start, page_hi)
        effect, soft = _extract_description(typ, body)
        key = norm_key(name)
        if key and key not in gloss:
            gloss[key] = {
                "name": name, "fear": fear,
                "type": clean_text(typ) if typ else None,
                "effect": effect, "page": pg, "soft": soft,
            }
        i = end
    return gloss


def _collect_glossary_body(stream, start, page_hi):
    """Collect body lines until the next glossary anchor / Table header / band exit."""
    body = []
    n = len(stream)
    i = start
    while i < n:
        pg, txt = stream[i]
        if pg is not None and pg > page_hi:
            break
        if _is_table_caption_line(txt):
            break
        if _is_glossary_anchor(stream, i, page_hi):     # next entry begins
            break
        if _is_index_header_here(stream, i):            # ran into an index table
            break
        if read_quad(stream, i) is not None:            # (or its record rows)
            break
        if txt.strip().lower() in SIDEBAR_STOP:         # ran into a boxed sidebar
            break
        body.append(txt)
        i += 1
    return body, i


def _extract_description(typ, body_lines):
    """Return (effect, soft).  effect = the 'Description:' text (RAW, joined).

    If there is no explicit 'Description:' label the entry is delivered as a
    sub-table or other layout; capture the body text but flag it soft.
    """
    text = "\n".join(body_lines)
    # drop trailing same-entry sections that are not the mechanical effect
    text = re.split(r"(?im)^\s*(?:Variations|Example)s?\s*:", text, maxsplit=1)[0]
    m = re.search(r"(?is)Description:\s*(.*)", text)
    core = clean_text(m.group(1)) if m else clean_text(text)
    soft = m is None                               # no explicit Description
    # safety net: truncate if a foreign structural label (interleaved sidebar /
    # disease box / next entry) or an inline worked Example slipped in.
    fm = FOREIGN_MARKER_RE.search(core)
    if fm and fm.start() > 0:
        core = core[:fm.start()].strip()
    em = re.search(r"\bExample:\s", core)
    if em and em.start() > 0:
        core = core[:em.start()].strip()
    core = trim_statblock(core)
    return core, soft


# --------------------------------------------------------------------------- #
# Gift definition prose (Chapter XIII): name-heading -> paragraph(s)
# --------------------------------------------------------------------------- #


def parse_gift_defs(stream, known_names, exclude_spans, page_lo=165, page_hi=185):
    """Return {norm_key: {name, effect, page}} for gift/reward descriptions.

    A heading is a line that exactly equals one of `known_names` (normalised),
    lies in Chapter XIII's page band, and is NOT inside an index-table span.
    Body runs until the next heading / Table line.
    """
    keyset = {norm_key(k): k for k in known_names}
    defs = {}
    n = len(stream)

    def in_excluded(idx):
        return any(a <= idx < b for (a, b) in exclude_spans)

    i = 0
    while i < n:
        pg, txt = stream[i]
        if pg is None or not (page_lo <= pg <= page_hi) or in_excluded(i):
            i += 1
            continue
        key = norm_key(txt)
        if key in keyset and not ROLL_RE.match(norm_dash(txt.strip())):
            # collect body until next heading / table
            body = []
            j = i + 1
            while j < n:
                pg2, t2 = stream[j]
                if pg2 is not None and pg2 > page_hi:
                    break
                if in_excluded(j):
                    j += 1
                    continue
                s2 = t2.strip()
                if _is_table_caption_line(t2):
                    break
                if norm_key(t2) in keyset and not ROLL_RE.match(norm_dash(s2)):
                    break
                body.append(t2)
                j += 1
            eff = trim_statblock(clean_text("\n".join(body)))
            if STATBLOCK_RE.match(eff):
                eff = ""            # this heading is a stat block, not the prose
            if key not in defs and eff:
                defs[key] = {"name": clean_text(txt), "effect": eff, "page": pg}
            i = j
            continue
        i += 1
    return defs


# --------------------------------------------------------------------------- #
# Row assembly
# --------------------------------------------------------------------------- #

MUT_TABLES = [
    # (label_regex, table_label, god)
    (re.compile(r"^Table\s+3" + DASHCLASS + r"1:\s*Mutations\s*$"),
     "Table 3-1: Mutations", None),
    (re.compile(r"^Table\s+3" + DASHCLASS + r"2:\s*Mutations of Khorne"),
     "Table 3-2: Mutations of Khorne", "Khorne"),
    (re.compile(r"^Table\s+3" + DASHCLASS + r"3:\s*Mutations of Nurgle"),
     "Table 3-3: Mutations of Nurgle", "Nurgle"),
    (re.compile(r"^Table\s+3" + DASHCLASS + r"4:\s*Mutations of Slaanesh"),
     "Table 3-4: Mutations of Slaanesh", "Slaanesh"),
    (re.compile(r"^Table\s+3" + DASHCLASS + r"5:\s*Mutations of Tzeentch"),
     "Table 3-5: Mutations of Tzeentch", "Tzeentch"),
]

GIFT_TABLES = [
    (re.compile(r"^Table\s+13" + DASHCLASS + r"1:\s*Rewards of Chaos"),
     "Table 13-1: Rewards of Chaos", None, "undivided"),
    (re.compile(r"^Table\s+13" + DASHCLASS + r"3:\s*Gifts of Khorne"),
     "Table 13-3: Gifts of Khorne", "Khorne", None),
    (re.compile(r"^Table\s+13" + DASHCLASS + r"4:\s*Gifts of Nurgle"),
     "Table 13-4: Gifts of Nurgle", "Nurgle", None),
    (re.compile(r"^Table\s+13" + DASHCLASS + r"5:\s*Gifts of Slaanesh"),
     "Table 13-5: Gifts of Slaanesh", "Slaanesh", None),
    (re.compile(r"^Table\s+13" + DASHCLASS + r"6:\s*Gifts of Tzeentch"),
     "Table 13-6: Gifts of Tzeentch", "Tzeentch", None),
]


def _find_all(stream, label_regex):
    return [i for i, (_p, t) in enumerate(stream) if label_regex.search(norm_dash(t))]


def harvest_tome(stream, diag=None):
    """Return (rows, soft, coverage) for the Tome of Corruption."""
    rows = []
    soft = []
    coverage = {}

    # ---- mutations -------------------------------------------------------- #
    gloss = parse_mut_glossary(stream)
    if diag is not None:
        diag["glossary_entries"] = len(gloss)

    def lookup_gloss(name):
        k = norm_key(name)
        if k in gloss:
            return gloss[k]
        if name.rstrip().endswith(("\u2026", "...")):        # truncated index name
            for gk, gv in gloss.items():
                if gk.startswith(k):
                    return gv
        return None

    # collect index records per table.  The master (Table 3-1) is a d1000 table
    # split into four column-chunks headed by 'D1000'; each god table (3-2..3-5)
    # is a set of d100 column-chunk runs on one PDF page, whose caption may sit
    # ABOVE (Khorne) or BELOW (the rest) its body.  Records are assigned to a
    # table by roll-width (3-digit -> master) and nearest god caption.
    def roll_width(roll):
        return len(roll.split(ENDASH)[0].strip())

    # -- master: parse every 'D1000'-headed chunk, merge -------------------- #
    master_recs = []
    for i, (_p, t) in enumerate(stream):
        if t.strip() == "D1000":
            recs, _e = parse_mut_chunk(stream, i)
            master_recs.extend(recs)

    # -- god captions ------------------------------------------------------- #
    god_caps = {}      # god -> stream idx of its caption
    god_label = {}     # god -> table label
    for label_re, tlabel, god in MUT_TABLES:
        if god is None:
            continue
        hits = _find_all(stream, label_re)
        god_label[god] = tlabel
        if hits:
            god_caps[god] = hits[0]
        else:
            coverage[tlabel] = "NO COVERAGE (table header not found)"

    # -- god runs: detect all quad-runs, keep 2-digit, assign to nearest cap - #
    god_recs = {g: [] for g in god_caps}
    WINDOW = 900
    for start, recs in detect_mut_runs(stream, min_len=3):
        if any(roll_width(r[0]) >= 3 for r in recs):
            continue                                # master chunk -> skip here
        # nearest god caption within window
        best_g, best_d = None, None
        for g, cidx in god_caps.items():
            d = abs(start - cidx)
            if best_d is None or d < best_d:
                best_g, best_d = g, d
        if best_g is not None and best_d <= WINDOW:
            god_recs[best_g].extend(recs)

    # -- emit rows ---------------------------------------------------------- #
    def emit_mut_rows(recs, tlabel, god):
        seen = set()
        cnt = 0
        for roll, name, fear_cell, page_ref, pg in recs:
            key = (roll, norm_key(name))
            if key in seen:
                continue
            seen.add(key)
            g = lookup_gloss(name)
            effect = g["effect"] if g else ""
            gfear = g["fear"] if g else (fear_cell or None)
            gtype = g["type"] if g else None
            is_soft = (g is None) or (g and g["soft"]) or (not effect)
            row = {
                "name": name, "kind": "mutation",
                "roll": roll, "effect": effect,
                "table": tlabel, "system": SYSTEM, "edition": EDITION,
                "book": TOME_BOOK, "page": pg,
                "citation": f"{TOME_BOOK}, PDF p.{pg}",
            }
            if god:
                row["god"] = god
            if gfear is not None:
                row["fear"] = gfear
            if gtype:
                row["type"] = gtype
            rows.append(row)
            cnt += 1
            if is_soft:
                soft.append({
                    "name": name, "table": tlabel, "roll": roll,
                    "reason": "no glossary Description found" if g is None
                    else "effect delivered as sub-table / unlabelled",
                })
        return cnt

    master_label = MUT_TABLES[0][1]
    if master_recs:
        c = emit_mut_rows(master_recs, master_label, None)
        coverage[master_label] = f"ok -- {c} rows (4 d1000 column-chunks merged)"
    else:
        coverage[master_label] = "NO COVERAGE (no D1000 chunks found)"

    for g in ("Khorne", "Nurgle", "Slaanesh", "Tzeentch"):
        if g in god_caps:
            c = emit_mut_rows(god_recs[g], god_label[g], g)
            coverage[god_label[g]] = f"ok -- {c} rows"

    # ---- gifts ------------------------------------------------------------ #
    gift_index = {}         # tlabel -> list[(roll, name, pg)]
    exclude_spans = []
    all_gift_names = set()
    for label_re, tlabel, god, alignment in GIFT_TABLES:
        hits = _find_all(stream, label_re)
        if not hits:
            coverage[tlabel] = "NO COVERAGE (table header not found)"
            continue
        recs, _end, span = parse_gift_index(stream, hits[0])
        gift_index[tlabel] = (recs, god, alignment)
        exclude_spans.append(span)
        for _r, nm, _p in recs:
            all_gift_names.add(nm)

    gdefs = parse_gift_defs(stream, all_gift_names, exclude_spans)
    if diag is not None:
        diag["gift_defs"] = len(gdefs)

    def lookup_gift(name):
        k = norm_key(name)
        if k in gdefs:
            return gdefs[k]["effect"], False
        # gift result may point at a mutation defined in the mutation glossary
        g = lookup_gloss(name)
        if g and g["effect"]:
            return g["effect"], False
        return "", True

    for label_re, tlabel, god, alignment in GIFT_TABLES:
        if tlabel not in gift_index:
            continue
        recs, god, alignment = gift_index[tlabel]
        seen = set()
        cnt = 0
        for roll, name, pg in recs:
            nk = norm_key(name)
            if nk in seen:
                continue
            seen.add(nk)
            effect, is_soft = lookup_gift(name)
            row = {
                "name": name, "kind": "gift",
                "roll": roll, "effect": effect,
                "table": tlabel, "system": SYSTEM, "edition": EDITION,
                "book": TOME_BOOK, "page": pg,
                "citation": f"{TOME_BOOK}, PDF p.{pg}",
            }
            if god:
                row["god"] = god
            if alignment:
                row["alignment"] = alignment
            rows.append(row)
            cnt += 1
            if is_soft:
                soft.append({
                    "name": name, "table": tlabel, "roll": roll,
                    "reason": "no in-book description located (cross-ref/other chapter)",
                })
        coverage[tlabel] = f"ok -- {cnt} rows"

    return rows, soft, coverage


# --------------------------------------------------------------------------- #
# Lost Bloodlines: in-file "New Blood Gifts" only
# --------------------------------------------------------------------------- #

BLOODLINES = ["Jade-Blooded", "Mahtmasi"]


def parse_blood_tables(stream):
    """Return list of (bloodline, roll, name, pdf_page) for each Table 3 Blood Gifts."""
    out = []
    n = len(stream)
    tbl_re = re.compile(r"^Table\s+3:\s*Blood Gifts", re.IGNORECASE)
    hits = [i for i, (_p, t) in enumerate(stream) if tbl_re.search(t.strip())]
    for idx in hits:
        # the bloodline name is the header line right after "Roll"
        i = idx + 1
        bloodline = None
        while i < n and i < idx + 6:
            t = stream[i][1].strip()
            if t.lower() == "roll":
                i += 1
                continue
            if is_blank(t):
                i += 1
                continue
            nk = norm_key(t)
            for bl in BLOODLINES:
                if norm_key(bl) == nk:
                    bloodline = bl
                    break
            break
        if not bloodline:
            continue
        i += 1
        # read up to 10 (roll, name) pairs
        count = 0
        while i < n and count < 10:
            t = stream[i][1].strip()
            if is_blank(t):
                i += 1
                continue
            if not re.fullmatch(r"10|[1-9]", t):
                break
            roll = t
            j = i + 1
            while j < n and is_blank(stream[j][1]):
                j += 1
            if j >= n:
                break
            name = clean_text(stream[j][1])
            out.append((bloodline, roll, name, stream[j][0]))
            count += 1
            i = j + 1
    return out


def parse_blood_defs(stream):
    """Return {norm_key: (name, effect, pdf_page)} for in-file 'New Blood Gifts'."""
    defs = {}
    n = len(stream)
    section_headers = ("weaknesses", "thrall career", "new blood gifts",
                       "jade-blooded", "mahtmasi", "bloodline", "table")
    # gifts described in-file (heading == gift name, followed by prose)
    described = ["Bend Mortal Minds", "Walk as the Wind",
                 "Call Sandstorm", "Dust to Dust"]
    want = {norm_key(d): d for d in described}
    i = 0
    while i < n:
        t = stream[i][1].strip()
        if norm_key(t) in want:
            body = []
            j = i + 1
            while j < n:
                s = stream[j][1].strip()
                low = norm_key(s)
                if low in want:
                    break
                if any(s.lower().startswith(h) for h in section_headers):
                    break
                if s.lower().startswith("table "):
                    break
                body.append(stream[j][1])
                j += 1
            eff = clean_text("\n".join(body))
            k = norm_key(t)
            if k not in defs and eff:
                defs[k] = (clean_text(t), eff, stream[i][0])
            i = j
            continue
        i += 1
    return defs


def harvest_lost(stream):
    """Return (rows, soft, coverage) for Lost Bloodlines in-file blood gifts."""
    rows = []
    soft = []
    coverage = {}
    tbl_rows = parse_blood_tables(stream)
    defs = parse_blood_defs(stream)
    if not tbl_rows:
        coverage["Lost Bloodlines: Table 3 Blood Gifts"] = \
            "NO COVERAGE (no Blood Gifts table found)"
        return rows, soft, coverage
    covered = 0
    uncovered = 0
    for bloodline, roll, name, pg in tbl_rows:
        k = norm_key(name)
        if k in defs:
            dname, eff, dpg = defs[k]
            rows.append({
                "name": dname, "kind": "gift",
                "roll": roll, "effect": eff,
                "table": f"Table 3: Blood Gifts ({bloodline})",
                "bloodline": bloodline,
                "category": "Vampire Blood Gift",
                "system": SYSTEM, "edition": EDITION,
                "book": LOST_BOOK, "page": dpg,
                "citation": f"{LOST_BOOK}, PDF p.{dpg}",
            })
            covered += 1
        else:
            uncovered += 1
    coverage["Lost Bloodlines: Blood Gifts (in-file effects)"] = (
        f"ok -- {covered} rows with effect text"
    )
    coverage["Lost Bloodlines: Blood Gifts (parent-book effects)"] = (
        f"NO COVERAGE -- {uncovered} table entries reference gifts defined in the "
        f"parent Night's Dark Masters (not in the Fantasy/ folder); effects not harvested"
    )
    return rows, soft, coverage


# --------------------------------------------------------------------------- #
# Load / harvest
# --------------------------------------------------------------------------- #


def load_stream(path):
    with open(path, "r", encoding="utf-8") as fh:
        raw = fh.readlines()
    return build_stream(raw)


def run_harvest(corpus, diag=None):
    fantasy = corpus / "Warhammer" / "Fantasy"
    rows, soft, coverage = [], [], {}

    tome_path = fantasy / TOME_FILE
    if tome_path.exists():
        tstream = load_stream(tome_path)
        r, s, c = harvest_tome(tstream, diag=diag)
        rows += r
        soft += s
        coverage.update(c)
    else:
        coverage[TOME_BOOK] = f"NO COVERAGE (file missing: {tome_path})"

    lost_path = fantasy / LOST_FILE
    if lost_path.exists():
        lstream = load_stream(lost_path)
        r, s, c = harvest_lost(lstream)
        rows += r
        soft += s
        coverage.update(c)
    else:
        coverage[LOST_BOOK] = f"NO COVERAGE (file missing: {lost_path})"

    return rows, soft, coverage


# --------------------------------------------------------------------------- #
# Output writers
# --------------------------------------------------------------------------- #


def write_progress(rows, soft, coverage, status="harvested"):
    try:
        by_kind = {}
        for r in rows:
            by_kind[r["kind"]] = by_kind.get(r["kind"], 0) + 1
        data = {
            "status": status,
            "total_rows": len(rows),
            "by_kind": by_kind,
            "soft_count": len(soft),
            "coverage": coverage,
        }
        PROGRESS.parent.mkdir(parents=True, exist_ok=True)
        with open(PROGRESS, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
    except Exception:
        pass


def _god_of(r):
    return r.get("god") or r.get("alignment") or r.get("bloodline") or ""


def write_json(rows, soft, coverage, path=OUT_JSON):
    by_kind = {}
    by_table = {}
    for r in rows:
        by_kind[r["kind"]] = by_kind.get(r["kind"], 0) + 1
        by_table[r["table"]] = by_table.get(r["table"], 0) + 1
    payload = {
        "generated_by": "scripts/wfrp_mutation_harvest.py",
        "system": SYSTEM,
        "edition": EDITION,
        "corpus": str(CORPUS),
        "description": ("WFRP 2e Chaos mutations and Gifts of the Chaos Gods "
                        "(plus in-file Vampire blood gifts). One row per "
                        "table entry, with RAW mechanical effect text. "
                        "DISTINCT from wfrp_creature_index (creature profiles)."),
        "total_rows": len(rows),
        "by_kind": by_kind,
        "by_table": by_table,
        "coverage": coverage,
        "soft_count": len(soft),
        "soft": soft,
        "rows": rows,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=1, ensure_ascii=False)
    return path


def _md_escape(s):
    return s.replace("|", "\\|").replace("\n", " ").strip()


def write_md(rows, soft, coverage, path=OUT_MD):
    by_kind = {}
    for r in rows:
        by_kind[r["kind"]] = by_kind.get(r["kind"], 0) + 1
    lines = []
    lines.append("# WARHAMMER FANTASY ROLEPLAY (WFRP 2e) -- "
                 "CHAOS MUTATION & GIFT INDEX")
    lines.append("")
    lines.append("**Generated by `scripts/wfrp_mutation_harvest.py`. Do not "
                 "hand-edit; rerun the harvest.** Every row is one **Chaos "
                 "mutation** or one **Gift of the Chaos Gods** (a d100/d1000 "
                 "table entry) from **Warhammer Fantasy Roleplay 2nd edition**, "
                 "with its mechanical effect text quoted RAW from the book. This "
                 "is a DIFFERENT game system from the campaign's 3.5e / GURPS "
                 "RAW: a WFRP block is SOURCE MATERIAL for the system-translator "
                 "skill, not campaign RAW. This index is DISTINCT from "
                 "`reference/wfrp_creature_index.*` (creature profiles) -- no "
                 "creature stats live here. Every row is stamped `system: WFRP`, "
                 "`edition: WFRP 2e` and cited to book + PDF page. `roll` is the "
                 "table's own d100/d1000 range, verbatim. Rows whose effect text "
                 "could not be cleanly separated carry an empty `effect` and are "
                 "listed under **Soft / uncertain** at the foot of this file.")
    lines.append("")
    total = len(rows)
    lines.append(f"**Total: {total} rows** "
                 f"({by_kind.get('mutation', 0)} mutations, "
                 f"{by_kind.get('gift', 0)} gifts). "
                 f"Soft/uncertain: {len(soft)}.")
    lines.append("")
    lines.append("## Coverage")
    lines.append("")
    for k, v in coverage.items():
        lines.append(f"- **{k}** -- {v}")
    lines.append("")

    # group rows by table, in a stable order
    order = [t for _re, t, *_ in MUT_TABLES] + \
            [t for _re, t, *_ in GIFT_TABLES]
    tables = {}
    for r in rows:
        tables.setdefault(r["table"], []).append(r)
    ordered_tables = [t for t in order if t in tables] + \
        [t for t in tables if t not in order]

    for tlabel in ordered_tables:
        trows = tables[tlabel]
        god = ""
        for r in trows:
            if _god_of(r):
                god = _god_of(r)
                break
        suffix = f"  *(god/alignment: {god})*" if god else ""
        lines.append(f"## {tlabel} -- {len(trows)} rows{suffix}")
        lines.append("")
        lines.append("| Roll | Name | Fear | Effect (RAW) | Page |")
        lines.append("|---|---|---|---|---|")
        for r in trows:
            eff = r["effect"] or "_(soft: see foot of file)_"
            if len(eff) > 600:
                eff = eff[:597] + "..."
            fear = r.get("fear", "")
            lines.append(
                f"| {_md_escape(r['roll'])} | {_md_escape(r['name'])} | "
                f"{_md_escape(str(fear))} | {_md_escape(eff)} | {r.get('page','')} |"
            )
        lines.append("")

    if soft:
        lines.append("## Soft / uncertain rows")
        lines.append("")
        lines.append("These rows are emitted with an empty `effect` (RAW rule: "
                     "never fabricate). Cause noted per row.")
        lines.append("")
        lines.append("| Table | Roll | Name | Reason |")
        lines.append("|---|---|---|---|")
        for s in soft:
            lines.append(
                f"| {_md_escape(s['table'])} | {_md_escape(s['roll'])} | "
                f"{_md_escape(s['name'])} | {_md_escape(s['reason'])} |"
            )
        lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    return path


# --------------------------------------------------------------------------- #
# Selftest
# --------------------------------------------------------------------------- #

FIXTURE_MUT = """## [PDF page 41]

39
Chapter III: A Catalogue of Change
Table 3\u20133: Mutations of Nurgle
Roll
Mutation
Fear
Points
Page
01
Acid Excretion
1
27
02
Atrophy
0
30
04\u201306
Bestial Appearance
2
31
"""

FIXTURE_GLOSS = """## [PDF page 29]

27
Chapter III: A Catalogue of Change
Mutations Defined
Fangs\t
Fear 1
Type: Single.
Description: Your incisors lengthen and sharpen. You can use them to
make attacks. They deal SB\u20132 Damage and have the Precise Quality.
Variations: Instead of long sharp teeth, you might gain tusks.
Fast\t
Fear 0
Type: Multiple.
Description: You develop uncanny speed. Each time you gain this
mutation, your Movement Characteristic increases by +1.
Fear of Blood\t
Fear 0
Type: Single.
Description: Whenever you see blood, you must take a Fear Test.
Centauroid\t
Fear 2
Description: Your legs are replaced by the trunk of some other creature.
Chaos Spawn\t
Fear n/a
Type: Single.
Description: The Ruinous Powers cast you down. You become an NPC.
"""

FIXTURE_GIFT = """## [PDF page 172]

170
Chapter XIII: Slaves to Chaos
Table 13\u20133: Gifts of Khorne
Roll
Result
01\u201303
Face of Khorne
04\u201306
Face of a Bloodthirster
Gifts of Khorne
Face of Khorne
A Daemon appears before you and attacks. Gain the Terrifying Talent.
Face of a Bloodthirster
Bones erupt from your face. Gain the Frightening Talent. Future results
of this Gift apply to a member of your retinue.
"""


def _fixture_stream(text):
    return build_stream([ln + "\n" for ln in text.split("\n")])


def selftest():
    failures = []

    def check(cond, msg):
        if not cond:
            failures.append(msg)

    # (a) fixture: mutation index parse ------------------------------------- #
    st = _fixture_stream(FIXTURE_MUT)
    idx = find_table(st, re.compile(r"Table\s+3" + DASHCLASS + r"3"))
    recs, _e = parse_mut_chunk(st, idx)
    names = {n: (roll, fear, pg) for roll, n, fear, pg, _p in recs}
    check("Acid Excretion" in names, "fixture: Acid Excretion missing")
    if "Acid Excretion" in names:
        check(names["Acid Excretion"][0] == "01",
              f"fixture: Acid Excretion roll != 01 ({names['Acid Excretion'][0]})")
    check("Bestial Appearance" in names, "fixture: Bestial Appearance missing")
    if "Bestial Appearance" in names:
        check(names["Bestial Appearance"][0] == "04\u201306",
              "fixture: Bestial Appearance roll != 04\u201306")
    check(len(recs) == 3, f"fixture: expected 3 Nurgle recs, got {len(recs)}")

    # (b) fixture: mutation glossary parse ---------------------------------- #
    st = _fixture_stream(FIXTURE_GLOSS)
    gl = parse_mut_glossary(st, page_lo=25, page_hi=62)
    check(norm_key("Fangs") in gl, "fixture: Fangs not in glossary")
    if norm_key("Fangs") in gl:
        fx = gl[norm_key("Fangs")]
        check(fx["fear"] == "1", f"fixture: Fangs fear != 1 ({fx['fear']})")
        check("SB\u20132 Damage" in fx["effect"],
              "fixture: Fangs effect missing 'SB-2 Damage'")
        check("Precise" in fx["effect"], "fixture: Fangs effect missing 'Precise'")
        check("Variations" not in fx["effect"],
              "fixture: Fangs effect leaked Variations")
    check(norm_key("Fast") in gl, "fixture: Fast not in glossary")
    if norm_key("Fast") in gl:
        check("+1" in gl[norm_key("Fast")]["effect"],
              "fixture: Fast effect missing '+1'")
    # a NAME that starts with 'Fear' must still be captured (not mistaken for a
    # Fear-rating line)
    check(norm_key("Fear of Blood") in gl,
          "fixture: 'Fear of Blood' (Fear-prefixed name) not captured")
    if norm_key("Fear of Blood") in gl:
        check("Fear Test" in gl[norm_key("Fear of Blood")]["effect"],
              "fixture: Fear of Blood effect missing 'Fear Test'")
    # an entry with NO 'Type:' line (Fear -> Description directly)
    check(norm_key("Centauroid") in gl,
          "fixture: 'Centauroid' (no Type: line) not captured")
    if norm_key("Centauroid") in gl:
        check("other creature" in gl[norm_key("Centauroid")]["effect"],
              "fixture: Centauroid effect missing text")
    # a non-numeric Fear value ('n/a')
    check(norm_key("Chaos Spawn") in gl, "fixture: 'Chaos Spawn' not captured")
    if norm_key("Chaos Spawn") in gl:
        check(gl[norm_key("Chaos Spawn")]["fear"] == "n/a",
              "fixture: Chaos Spawn fear != n/a")

    # (c) fixture: gift index + defs ---------------------------------------- #
    st = _fixture_stream(FIXTURE_GIFT)
    gidx = find_table(st, re.compile(r"Table\s+13" + DASHCLASS + r"3"))
    grecs, _e, span = parse_gift_index(st, gidx)
    gnames = {n: roll for roll, n, _p in grecs}
    check("Face of Khorne" in gnames, "fixture: Face of Khorne missing")
    check("Face of a Bloodthirster" in gnames,
          "fixture: Face of a Bloodthirster missing")
    if "Face of Khorne" in gnames:
        check(gnames["Face of Khorne"] == "01\u201303",
              "fixture: Face of Khorne roll != 01\u201303")
    gdefs = parse_gift_defs(st, set(gnames), [span], page_lo=165, page_hi=185)
    check(norm_key("Face of a Bloodthirster") in gdefs,
          "fixture: Bloodthirster def missing")
    if norm_key("Face of a Bloodthirster") in gdefs:
        check("Frightening Talent" in gdefs[norm_key("Face of a Bloodthirster")]["effect"],
              "fixture: Bloodthirster effect missing 'Frightening Talent'")
        check("Face of a Bloodthirster" not in
              gdefs[norm_key("Face of Khorne")]["effect"],
              "fixture: Face of Khorne def leaked into next entry")

    # (d) live-harvest invariants ------------------------------------------ #
    live_ok = FANTASY.joinpath(TOME_FILE).exists()
    if live_ok:
        rows, soft, coverage = run_harvest(CORPUS)
        n = len(rows)
        check(250 <= n <= 900, f"live: total rows {n} out of band [250,900]")
        muts = [r for r in rows if r["kind"] == "mutation"]
        gifts = [r for r in rows if r["kind"] == "gift"]
        check(len(muts) >= 200, f"live: only {len(muts)} mutations (<200)")
        check(len(gifts) >= 40, f"live: only {len(gifts)} gifts (<40)")
        roll_ok = re.compile(r"^\d{1,4}(?:" + DASHCLASS + r"\d{1,4})?$")
        hdrbad = {"roll", "mutation", "result", "fear", "points", "page",
                  "type", "description", "extras"}
        leak_re = re.compile(r"\bDescription:|\bType:\s*(?:Single|Multiple)\b"
                             r"|\bVariations:|\bDuration:\s*\d")
        for r in rows:
            check(r["system"] == "WFRP", f"live: bad system on {r['name']}")
            check(r["edition"] == "WFRP 2e", f"live: bad edition on {r['name']}")
            check(r["kind"] in ("mutation", "gift"),
                  f"live: bad kind on {r['name']}")
            check(bool(r["name"].strip()), "live: empty name row")
            check(r["name"].strip().lower() not in hdrbad,
                  f"live: header-fragment name '{r['name']}'")
            check(not r["name"].lower().startswith("table "),
                  f"live: table-label name '{r['name']}'")
            check(not re.search(r"\d", r["name"]),
                  f"live: digit in name (index garble?) '{r['name']}'")
            check(roll_ok.match(norm_dash(r["roll"])),
                  f"live: roll not dNN-shaped '{r['roll']}' on {r['name']}")
            check("effect" in r, f"live: no effect field on {r['name']}")
            # no effect may leak a foreign structural label (sidebar/next entry)
            check(not leak_re.search(r["effect"]),
                  f"live: effect leaked a structural label on '{r['name']}'")
            # no effect may leak a creature/career stat block
            check(not STATBLOCK_RE.search(r["effect"]),
                  f"live: effect leaked a stat block on '{r['name']}'")
        # spot rows
        nurgle_acid = [r for r in muts if r["table"].endswith("Nurgle")
                       and norm_key(r["name"]) == "acid excretion"]
        check(nurgle_acid and nurgle_acid[0]["roll"] == "01",
              "live: Nurgle 'Acid Excretion' roll 01 not found")
        fok = [r for r in gifts if norm_key(r["name"]) == "face of khorne"]
        check(bool(fok) and "Terrifying" in fok[0]["effect"],
              "live: gift 'Face of Khorne' effect missing")
        # entries with unusual Fear values must still resolve to an effect
        shrink = [r for r in muts if norm_key(r["name"]) == "shrink"]
        check(shrink and "implode" in shrink[0]["effect"],
              "live: 'Shrink' (negative fear) effect not resolved")
        fob = [r for r in muts if norm_key(r["name"]) == "fear of blood"]
        check(fob and fob[0]["effect"].strip(),
              "live: 'Fear of Blood' (Fear-prefixed name) effect not resolved")
        # the master d1000 table must be complete (all four column-chunks)
        master = [r for r in muts if r["table"] == MUT_TABLES[0][1]]
        check(len(master) >= 150,
              f"live: master Table 3-1 only {len(master)} rows (<150)")
        # nearly all mutation rows should carry effect text
        with_eff = [r for r in muts if r["effect"].strip()]
        check(len(with_eff) >= int(0.95 * len(muts)),
              f"live: only {len(with_eff)}/{len(muts)} mutations carry effect text")
    else:
        sys.stderr.write("selftest: NOTE live corpus not found; "
                         "fixtures only.\n")

    if failures:
        for f in failures:
            sys.stderr.write("FAIL: " + f + "\n")
        print("selftest: FAIL (%d)" % len(failures))
        return 1
    print("selftest: PASS")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--corpus", type=Path, default=CORPUS)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--debug", action="store_true",
                    help="harvest + diagnostics, do not write output files")
    ap.add_argument("--search", metavar="TEXT",
                    help="print harvested rows whose name/effect contains TEXT")
    ap.add_argument("--out-json", type=Path, default=OUT_JSON)
    ap.add_argument("--out-md", type=Path, default=OUT_MD)
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    diag = {}
    rows, soft, coverage = run_harvest(args.corpus, diag=diag)
    write_progress(rows, soft, coverage,
                   status="debug" if (args.debug or args.search) else "written")

    if args.search:
        q = args.search.lower()
        hits = [r for r in rows if q in r["name"].lower()
                or q in r["effect"].lower()]
        for r in hits:
            print(f"[{r['kind']}] {r['name']}  (roll {r['roll']}; {r['table']}; "
                  f"{_god_of(r) or '-'})")
            if r["effect"]:
                print("    " + (r["effect"][:200]))
        print(f"\n{len(hits)} match(es).")
        return 0

    by_kind = {}
    by_table = {}
    god_split = {}
    for r in rows:
        by_kind[r["kind"]] = by_kind.get(r["kind"], 0) + 1
        by_table[r["table"]] = by_table.get(r["table"], 0) + 1
        g = _god_of(r) or "(none)"
        god_split[g] = god_split.get(g, 0) + 1

    if args.debug:
        print("=== DIAGNOSTICS ===")
        print("glossary entries parsed:", diag.get("glossary_entries"))
        print("gift defs parsed:", diag.get("gift_defs"))
        print()
        print("=== COVERAGE ===")
        for k, v in coverage.items():
            print(f"  {k}: {v}")
        print()
        print("=== COUNTS ===")
        print("total:", len(rows), "| by kind:", by_kind)
        print("by table:")
        for k, v in by_table.items():
            print(f"  {v:>4}  {k}")
        print("by god/alignment:", god_split)
        print("soft rows:", len(soft))
        print()
        print("=== 12 SAMPLE ROWS ===")
        for r in rows[:6] + rows[-6:]:
            eff = (r["effect"][:90] + "...") if len(r["effect"]) > 90 else r["effect"]
            print(f"  [{r['kind']}] {r['name']} (roll {r['roll']}, {r['table']})")
            print(f"       -> {eff or '(soft/empty)'}")
        return 0

    jp = write_json(rows, soft, coverage, args.out_json)
    mp = write_md(rows, soft, coverage, args.out_md)
    print(f"Wrote {jp}")
    print(f"Wrote {mp}")
    print(f"total={len(rows)} by_kind={by_kind} soft={len(soft)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
