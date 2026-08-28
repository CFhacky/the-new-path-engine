#!/usr/bin/env python3
"""wh40krp_forcefield_harvest.py — collate WH40K Roleplay FORCE FIELDS.

THE PROCESS (the 40K shelf): other GAME SYSTEMS are welcome in the reference
layer AS LONG AS each is clearly LABELLED by system — the translator tools turn
them into the hybrid's 3.5e + GURPS.  This is the **Warhammer 40,000 Roleplay**
(Fantasy Flight Games d100) FORCE FIELD index — the protective *devices* of Dark
Heresy / Rogue Trader / Deathwatch / Only War / Black Crusade, stamped
`"system": "WH40K Roleplay"`.

WHY A SEPARATE INDEX.  A force field is mechanically NOT armour and NOT gear: it
has a **Protection Rating** (roll 1d100; on a result <= the rating the incoming
hit is wholly nullified) and an **Overload** chance (the field burns out and must
be recharged/repaired), but NO Armour Points and NO hit locations.  The sibling
`wh40krp_armour_index` (AP/locations) and `wh40krp_gear_index` (equipment) BOTH
deliberately excluded force fields to avoid schema pollution, so they lived in no
index — this file closes that gap.  Armour and gear rows are NOT duplicated here.

    reference/wh40krp_forcefield_index.json — every force field: name, protection
                                              rating, overload, weight, and the
                                              acquisition gate, book + PDF page.
    reference/wh40krp_forcefield_index.md   — the same, for human eyes.

`--export` emits a translator-ready packet (a 40K RP force field the system-
translator skill converts to the 3.5e + GURPS pair).

WORKFLOW
    python wh40krp_forcefield_harvest.py                       # (re)build index
    python wh40krp_forcefield_harvest.py --search "refractor"  # find candidates
    python wh40krp_forcefield_harvest.py --export "Iron Halo"
    python wh40krp_forcefield_harvest.py --selftest

GOVERNING SOURCES
    I:\\Sourcebooks\\_text\\Warhammer\\40K Roleplay\\ — the five core rulebooks.
    Each core's Armoury *may* carry one small "Force Fields" table, OCR'd as a
    VERTICAL COLUMN-DUMP: each cell on its own line, in a fixed column order that
    varies by book.  Two shapes occur:

        Only War / Black Crusade : Name | Protection Rating | Weight kg | Availability
        Deathwatch               : Name | Protection Rating | Overload Roll | Wt | Req | Renown

    Only War and Black Crusade acquire a field by Availability and give the
    overload chance in a SEPARATE craftsmanship table (Poor 01-15 / Common 01-10 /
    Good 01-05 / Best 01), NOT per field — so their rows carry no per-field
    overload (the table does not state one, and RAW forbids inventing it).
    Deathwatch grades acquisition by Requisition + Renown and states each field's
    Overload Roll inline, so its rows carry `req`, `renown`, and `overload`.

    NO COVERAGE.  The **Dark Heresy** and **Rogue Trader** cores have no Force
    Fields table at all (Dark Heresy's Armoury runs Table 5-12 Armour -> 5-13
    Clothing; Rogue Trader's runs Table 5-12 Armour -> Power Armour -> Gear).  The
    harvester searches every core, finds no such table in those two, and prints
    NO COVERAGE for them rather than guessing.

    The parser finds each "Table ...: Force Fields" heading, reads the column
    HEADER row to learn that table's template, then reads each row FORWARD from
    the field name: the Protection Rating is the first stat cell, the row
    terminates on an Availability rarity (Very Rare / Near Unique / ...) or, for
    Deathwatch, on a Renown rank (or a "--" = no rank).  Book RAW only — every
    value is the book's, cited to book + PDF page; an unrecoverable cell is left
    empty and the row noted in `soft`; nothing is invented.  Field *effects*
    (Refractor's Stealth penalty, Conversion's flash burst, Displacer's warp
    jump, Power Field's Encumbrance) live in prose blurbs beside the table and are
    deliberately NOT reproduced in the mechanical line.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CORPUS = Path(r"I:\Sourcebooks\_text")
REPO = Path(__file__).resolve().parent.parent
OUT_JSON = REPO / "reference" / "wh40krp_forcefield_index.json"
OUT_MD = REPO / "reference" / "wh40krp_forcefield_index.md"
SYSTEM = "WH40K Roleplay"
PROGRESS = Path(
    r"C:\Users\Chad\AppData\Local\Temp\claude"
    r"\I--repos-the-new-path-engine--claude-worktrees-intelligent-lamport-3a158a"
    r"\1c5f36b4-d94a-4698-95d9-c2304f8a0818\scratchpad\wh40krp_forcefield_progress.json")

PAGE = re.compile(r"\[PDF page (\d+)\]")
# Heading detector — tolerant of the OCR's missing spaces ("Table5-14:Force
# Fields") as well as the normal "Table 6-19: Force Fields".
RE_TBL_HEADING = re.compile(r"^\s*Table\s*[\dIVXLC]", re.IGNORECASE)

DASHES = "\u2013\u2014-"
RE_DASH = re.compile(rf"^[{DASHES}]+$")
RE_INT = re.compile(r"^\d{1,4}$")                       # 30, 55, 80, 500, req 40
RE_DEC = re.compile(r"^\d{1,3}\.\d{1,2}$")              # 0.5, 1.5
RE_KG = re.compile(r"^\d{1,4}(?:\.\d{1,2})?\s*kg\.?$", re.IGNORECASE)   # 0.5 kg
RE_OVERLOAD = re.compile(rf"^0?\d{{1,2}}\s*[{DASHES}]\s*0?\d{{1,2}}$")   # 01-10

# Availability rarity ladder (a closed set) — the terminal cell of an OW/BC row.
RARITIES = {
    "ubiquitous", "abundant", "plentiful", "common", "average", "scarce",
    "rare", "very rare", "extremely rare", "near unique", "unique",
}
# First words of the two-word rarities, in case OCR ever splits them.
RARITY_STARTS = {"very", "extremely", "near"}
# Deathwatch Renown ranks — the terminal cell of a Deathwatch row.
RENOWN_RANKS = {"respected", "distinguished", "famed", "hero"}

# Column-header tokens (used to auto-detect a table's template and skip its
# header row).  A cell whose every token is one of these is a header cell.
HEADER_TOKENS = {
    "name", "type", "protection", "rating", "overload", "roll", "wt", "wt.",
    "weight", "kg", "req", "req.", "requisition", "renown", "availability",
    "avail", "effect", "notes",
}

_STOPWORDS = {
    "the", "and", "for", "you", "your", "his", "her", "are", "was", "with",
    "that", "this", "not", "use", "can", "may", "of", "to", "in", "on", "a",
    "an", "is", "he", "it", "as", "at", "by", "or", "be", "but", "they", "their",
    "them", "if", "from", "will", "have", "has", "all", "one", "who", "which",
    "when", "does", "into", "only", "over", "than", "then", "so", "no", "must",
    "such", "these", "each", "also", "make", "made",
}


def _avnorm(s: str) -> str:
    """Normalise a terminal/header cell: drop footnote marks, lower-case."""
    return re.sub(r"\s+", " ", s).strip().strip("\u2020*.,\u2013\u2014- ").lower()


def _norm_name(s: str) -> str:
    s = s.replace("\ufb01", "fi").replace("\ufb02", "fl")   # OCR ligatures
    s = re.sub(r"\s+", " ", s).strip()
    s = s.strip(" ,\u2020*\u2013\u2014-").strip()
    return s


def _is_stat(c: str) -> bool:
    c = c.strip()
    if not c:
        return False
    return bool(RE_INT.match(c) or RE_DEC.match(c) or RE_KG.match(c)
                or RE_OVERLOAD.match(c) or RE_DASH.match(c))


def _is_name_start(c: str) -> bool:
    c = c.strip()
    if not c or not c[0].isalpha():
        return False
    low = _avnorm(c)
    if low in HEADER_TOKENS or low in RARITIES or low in RENOWN_RANKS:
        return False
    if low in RARITY_STARTS:            # a stray "Very"/"Near"/"Extremely"
        return False
    return True


def _plausible_name(s: str) -> bool:
    s = s.strip()
    if not (2 <= len(s) <= 60):
        return False
    if not s[0].isalpha():
        return False
    low = _avnorm(s)
    if low in HEADER_TOKENS or low in RARITIES or low in RENOWN_RANKS:
        return False
    if sum(c.isalpha() for c in s) < 2:
        return False
    return True


def _field_like(s: str) -> bool:
    """A conservative gate for the `soft` list: does this string plausibly name a
    force field (rather than a prose sentence fragment)?  Keeps `soft` honest."""
    s = s.strip()
    if re.search(r'[.!?,;:"]$', s):
        return False
    words = s.split()
    if not (1 <= len(words) <= 6) or not s[0].isupper():
        return False
    if any(w.strip(",.").lower() in _STOPWORDS for w in words):
        return False
    return True


def _match_terminal(cells: List["Cell"], i: int, terminal: str):
    """If a row's terminal cell begins at cells[i], return (value_or_None, consumed);
    else None.  value is None for a Deathwatch "--" (no Renown rank required)."""
    n = len(cells)
    low = _avnorm(cells[i].text)
    if terminal == "renown":
        if low in RENOWN_RANKS:
            return low.title(), 1
        if RE_DASH.match(cells[i].text.strip()):
            return None, 1
        return None
    # availability terminal
    if low in RARITIES:
        return low.title(), 1
    if low in RARITY_STARTS and i + 1 < n:
        two = (low + " " + _avnorm(cells[i + 1].text)).strip()
        if two in RARITIES:
            return two.title(), 2
    if RE_DASH.match(cells[i].text.strip()):
        return None, 1
    return None


@dataclass
class ForceField:
    name: str
    book: str
    page: Optional[int]
    line: int
    citation: str
    system: str = SYSTEM
    protection_rating: Optional[str] = None
    overload: Optional[str] = None
    weight: Optional[str] = None
    availability: Optional[str] = None      # Only War / Black Crusade
    req: Optional[str] = None               # Deathwatch Requisition
    renown: Optional[str] = None            # Deathwatch Renown rank

    def filled(self) -> int:
        return sum(1 for v in (self.protection_rating, self.overload, self.weight,
                               self.availability, self.req, self.renown) if v)


@dataclass
class Cell:
    text: str
    line: int
    page: int


@dataclass
class Region:
    template: dict
    cells: List[Cell]


def _pages_for(lines: List[str]) -> List[int]:
    pages: List[int] = []
    page = 0
    for ln in lines:
        m = PAGE.search(ln)
        if m:
            page = int(m.group(1))
        pages.append(page)
    return pages


def _build_cells(idxs: List[int], lines: List[str], pages: List[int]) -> List[Cell]:
    cells: List[Cell] = []
    for i in idxs:
        ln = lines[i]
        if PAGE.search(ln):
            continue
        for piece in ln.split("\t"):
            s = piece.strip()
            if s:
                cells.append(Cell(s, i, pages[i]))
    return cells


def _detect_template(cells: List[Cell]) -> Tuple[dict, List[Cell]]:
    """Read the leading header cells to learn the table's template, and return
    (template, data_cells) with the header stripped.  The Protection Rating is
    always the first stat column; the canonical middle order is
    [protection_rating, (overload), (weight), (req)] before the terminal."""
    has_overload = has_weight = has_req = False
    terminal: Optional[str] = None
    k = 0
    while k < len(cells):
        toks = _avnorm(cells[k].text).split()
        if toks and all(t in HEADER_TOKENS for t in toks):
            for t in toks:
                if t == "overload":
                    has_overload = True
                if t in ("wt", "wt.", "weight", "kg"):
                    has_weight = True
                if t in ("req", "req.", "requisition"):
                    has_req = True
                if t == "renown":
                    terminal = "renown"
                if t in ("availability", "avail") and terminal is None:
                    terminal = "avail"
            k += 1
        else:
            break
    middle = ["protection_rating"]
    if has_overload:
        middle.append("overload")
    if has_weight:
        middle.append("weight")
    if has_req:
        middle.append("req")
    return ({"middle": middle, "terminal": terminal or "avail"}, cells[k:])


def _regions(lines: List[str], pages: List[int], titles: Dict[str, str]) -> List[Region]:
    """Find every "Table ...: Force Fields" heading, bound its region at the next
    table heading OR the next PDF-page marker (all five cores' tables sit wholly
    within one page span), and hand back the header-stripped cells."""
    regions: List[Region] = []
    i, n = 0, len(lines)
    while i < n:
        ln = lines[i]
        if RE_TBL_HEADING.match(ln) and ":" in ln:
            title = _avnorm(ln.split(":", 1)[1])
            if title in titles:
                j = i + 1
                buf: List[int] = []
                while (j < n and not RE_TBL_HEADING.match(lines[j])
                       and not PAGE.search(lines[j])):
                    buf.append(j)
                    j += 1
                template, data = _detect_template(_build_cells(buf, lines, pages))
                regions.append(Region(template, data))
                i = j
                continue
        i += 1
    return regions


def _read_row(cells: List[Cell], i: int, tmpl: dict):
    """Read one force-field row starting at the name cell cells[i].
    Return (name, next_i, fields, ok, reason, page, line)."""
    n = len(cells)
    page, line = cells[i].page, cells[i].line
    parts = [cells[i].text]
    i += 1
    while i < n and cells[i].text.strip().startswith("("):   # wrapped '(...)'
        parts.append(cells[i].text)
        i += 1
    name = _norm_name(" ".join(parts))

    middle = tmpl["middle"]
    run: List[str] = []
    cap = len(middle) + 3
    steps = 0
    ok = False
    term_val: Optional[str] = None
    while i < n and steps <= cap:
        term = _match_terminal(cells, i, tmpl["terminal"])
        if term is not None:
            term_val, consumed = term
            i += consumed
            ok = True
            break
        if _is_stat(cells[i].text):
            run.append(cells[i].text.strip())
            i += 1
            steps += 1
            continue
        break                       # a name / prose cell — row has no terminal

    fields: dict = {}
    reason: Optional[str] = None
    if ok and len(run) == len(middle):
        for key, val in zip(middle, run):
            fields[key] = val
    elif ok and run:                # terminal found but column count wobbled
        if RE_INT.match(run[0]):    # salvage the one field that must never be lost
            fields["protection_rating"] = run[0]
        reason = (f"column count mismatch: {len(run)} stat cell(s) for "
                  f"{len(middle)} column(s) {middle}")
    elif ok:
        reason = "no stat cells before terminal (OCR)"
    else:
        reason = "no availability/renown terminal parsed (OCR)"

    if ok:
        if tmpl["terminal"] == "renown":
            fields["renown"] = term_val
        else:
            fields["availability"] = term_val
    return name, i, fields, ok, reason, page, line


def detect_forcefields(lines: List[str], pages: List[int], book: str,
                       citation: str, titles: Dict[str, str]
                       ) -> Tuple[List[ForceField], List[dict], int]:
    rows: List[ForceField] = []
    soft: List[dict] = []
    regions = _regions(lines, pages, titles)
    for region in regions:
        cells, tmpl = region.cells, region.template
        i, n = 0, len(cells)
        while i < n:
            if not _is_name_start(cells[i].text):
                i += 1
                continue
            name, i, fields, ok, reason, page, line = _read_row(cells, i, tmpl)
            if not _plausible_name(name):
                continue
            pr = fields.get("protection_rating")
            if ok and pr and RE_INT.match(pr):
                rows.append(ForceField(
                    name=name, book=book, page=page, line=line + 1,
                    citation=f"{book}, [PDF page {page}]",
                    protection_rating=pr, overload=fields.get("overload"),
                    weight=fields.get("weight"), availability=fields.get("availability"),
                    req=fields.get("req"), renown=fields.get("renown")))
            elif _field_like(name):
                partial = {k: v for k, v in fields.items() if v}
                if partial and not all(str(v) == str(page) for v in partial.values()):
                    soft.append({"name": name, "book": book, "page": page,
                                 "line": line + 1,
                                 "reason": reason or "no protection rating parsed",
                                 "partial": partial})
    # one row per (book, name): keep the richest, then the first seen.
    best: Dict[str, ForceField] = {}
    for r in rows:
        cur = best.get(r.name.lower())
        if cur is None or r.filled() > cur.filled():
            best[r.name.lower()] = r
    return sorted(best.values(), key=lambda r: (r.line,)), soft, len(regions)


@dataclass
class Source:
    key: str
    book: str
    path: Path
    citation: str
    titles: Dict[str, str]
    coverage: str = "pending"
    lines: List[str] = field(default_factory=list)
    forcefields: List[ForceField] = field(default_factory=list)
    soft: List[dict] = field(default_factory=list)


_40K = Path("Warhammer/40K Roleplay")

# All five cores are configured and searched for a table titled "Force Fields".
# Dark Heresy and Rogue Trader have none and will report NO COVERAGE.
FF_TITLE = {"force fields": "Force Field"}

SOURCES: List[Source] = [
    Source("dh-core", "Dark Heresy \u2014 Core Rulebook",
           _40K / "Dark Heresy/Rulebooks/Dark Heresy - Core Rulebook.pdf.md",
           "Dark Heresy Core Rulebook (FFG, WH40K Roleplay) \u2014 no Force Fields "
           "table in the core Armoury (it runs Table 5-12 Armour -> 5-13 Clothing); "
           "NO COVERAGE",
           FF_TITLE),
    Source("rt-core", "Rogue Trader \u2014 Core Rulebook",
           _40K / "Rogue Trader/Rulebooks/Rogue Trader - Core Rulebook (updated with 1.4 errata).md",
           "Rogue Trader Core Rulebook, 1.4 errata (FFG, WH40K Roleplay) \u2014 no "
           "Force Fields table in the core Armoury (it runs Table 5-12 Armour -> "
           "Power Armour -> Gear); NO COVERAGE",
           FF_TITLE),
    Source("dw-core", "Deathwatch \u2014 Core Rulebook",
           _40K / "Deathwatch/Rulebooks/Deathwatch - Core Rulebook.md",
           "Deathwatch Core Rulebook (FFG, WH40K Roleplay), Armoury \u2014 Table 5\u201314: "
           "Force Fields; Astartes fields carry a per-field Protection Rating + "
           "Overload Roll, acquired by Requisition (req) + Renown",
           FF_TITLE),
    Source("ow-core", "Only War \u2014 Core Rulebook",
           _40K / "Only War/Rulebooks/Only War - Core Rulebook.md",
           "Only War Core Rulebook (FFG, WH40K Roleplay), Armoury \u2014 Table 6-19: "
           "Force Fields; Protection Rating + Weight, acquired by Availability; "
           "overload is craftsmanship-based (Table 6-18), not per field",
           FF_TITLE),
    Source("bc-core", "Black Crusade \u2014 Core Rulebook",
           _40K / "Black Crusade/Rulebooks/Black Crusade - Core Rulebook.md",
           "Black Crusade Core Rulebook (FFG, WH40K Roleplay), Armoury \u2014 Table 5-13: "
           "Force Fields; Protection Rating + Weight, acquired by Availability; "
           "overload is craftsmanship-based (Table 5-12), not per field",
           FF_TITLE),
]


def _fresh_sources() -> List[Source]:
    return [Source(s.key, s.book, s.path, s.citation, s.titles) for s in SOURCES]


class Corpus:
    def __init__(self, base: Path, sources: List[Source]):
        self.base = base
        self.sources = sources
        for src in self.sources:
            path = base / src.path
            if not path.exists():
                src.coverage = f"NO COVERAGE \u2014 extraction missing: {path}"
                continue
            src.lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            pages = _pages_for(src.lines)
            src.forcefields, src.soft, nregions = detect_forcefields(
                src.lines, pages, src.book, src.citation, src.titles)
            if nregions == 0:
                src.coverage = (f"NO COVERAGE \u2014 no Force Fields table located "
                                f"in {path.name}")
            elif not src.forcefields:
                src.coverage = (f"NO COVERAGE \u2014 Force Fields table found but no "
                                f"rows parsed in {path.name}")
            else:
                src.coverage = f"ok \u2014 {len(src.forcefields)} force fields from {path.name}"
            _write_progress(self.sources)

    def all_fields(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for f in src.forcefields:
                yield src, f

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, f in self.all_fields(book):
            nm = f.name.lower()
            if nm == q:
                exact.append((src, f))
            elif q in nm:
                partial.append((src, f))
        return exact if exact else partial


def _write_progress(sources: List[Source]) -> None:
    try:
        PROGRESS.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS.write_text(json.dumps(
            {"system": SYSTEM,
             "books": [{"book": s.book, "coverage": s.coverage,
                        "fields": len(s.forcefields), "soft": len(s.soft)}
                       for s in sources]}, indent=1), encoding="utf-8")
    except Exception:
        pass


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    soft_total = 0
    covered = 0
    sources_out = []
    md: List[str] = [
        "# WH40K ROLEPLAY FORCE FIELD INDEX \u2014 The New Path",
        "",
        "**Generated by `scripts/wh40krp_forcefield_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** These are **Warhammer 40,000 Roleplay** FORCE FIELDS \u2014",
        "the protective *devices* of the Fantasy Flight Games d100 line (Dark Heresy /",
        "Rogue Trader / Deathwatch / Only War / Black Crusade). A force field is not",
        "armour and not gear: when an active field is attacked you roll 1d100, and on a",
        "result **<= its Protection Rating** the hit is wholly nullified; the field may",
        "instead **Overload** (burn out until recharged/repaired). Because a field has a",
        "Protection Rating and Overload but no Armour Points or hit locations, it lives",
        f"in this small index of its own. Every row is stamped `system: {SYSTEM}`; a 40K",
        "RP force field is SOURCE MATERIAL for the system-translator skill, not campaign",
        "RAW. Acquisition differs by game: Only War and Black Crusade use **Availability**",
        "(overload is craftsmanship-based, in a separate table, so no per-field overload",
        "is listed); Deathwatch uses **Requisition** + **Renown** and states each field's",
        "**Overload Roll** inline. A field left `\u2014` is one the book does not state. Field",
        "effects live in the books' prose and are intentionally not reproduced here. Use",
        "`--export \"NAME\"` for the translator packet.",
        "",
        "**NO COVERAGE:** the Dark Heresy and Rogue Trader cores carry no Force Fields",
        "table (in those lines force fields are supplement material), so they contribute",
        "no rows \u2014 see their entries below.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.forcefields)
        soft_total += len(src.soft)
        if src.forcefields:
            covered += 1
        sources_out.append({"key": src.key, "book": src.book, "system": SYSTEM,
                            "citation": src.citation, "coverage": src.coverage,
                            "forcefields": [asdict(f) for f in src.forcefields],
                            "soft": src.soft})
        md.append(f"## {src.book} \u2014 {len(src.forcefields)} force fields  "
                  f"*(system: {SYSTEM})*")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.forcefields:
            # Deathwatch-shape rows carry req/renown; Only War / Black Crusade carry
            # availability.  Render whichever columns the book actually populates.
            dw_shape = any(f.req or f.renown for f in src.forcefields)
            if dw_shape:
                md.append("| Force Field | Protection Rating | Overload | Weight | "
                          "Req | Renown | Page |")
                md.append("|---|---|---|---|---|---|---|")
                for f in sorted(src.forcefields, key=lambda x: x.name.lower()):
                    md.append(
                        f"| {f.name} | {f.protection_rating or '\u2014'} | "
                        f"{f.overload or '\u2014'} | {f.weight or '\u2014'} | "
                        f"{f.req or '\u2014'} | {f.renown or '\u2014'} | "
                        f"{f.page if f.page is not None else '\u2014'} |")
            else:
                md.append("| Force Field | Protection Rating | Overload | Weight | "
                          "Availability | Page |")
                md.append("|---|---|---|---|---|---|")
                for f in sorted(src.forcefields, key=lambda x: x.name.lower()):
                    md.append(
                        f"| {f.name} | {f.protection_rating or '\u2014'} | "
                        f"{f.overload or '\u2014'} | {f.weight or '\u2014'} | "
                        f"{f.availability or '\u2014'} | "
                        f"{f.page if f.page is not None else '\u2014'} |")
        if src.soft:
            md.append("")
            md.append(f"*Soft ({len(src.soft)}): rows the OCR left ambiguous \u2014 "
                      "banked here for honesty, not in the index.*")
            for s in src.soft:
                md.append(f"- {s['name']} (p.{s['page']}): {s['reason']}; "
                          f"partial {s['partial']}")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/wh40krp_forcefield_harvest.py",
                    "system": SYSTEM, "corpus": str(corpus.base),
                    "total_forcefields": total, "total_soft": soft_total,
                    "books_covered": covered, "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, covered


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 8:
        print(f"'{name}' matches {len(hits)} fields; narrow with --book or the exact name:")
        for src, f in hits[:20]:
            print(f"  {f.name}   [{f.book}, p.{f.page}]")
        return 1
    packets = []
    for src, f in hits:
        lo = max(0, f.line - 1)
        body = [ln for ln in src.lines[lo:lo + 8] if not PAGE.search(ln)]
        packets.append({
            "packet": "wh40krp-forcefield-for-translation",
            "instructions": ("A Warhammer 40,000 Roleplay force field (system: "
                             f"{SYSTEM}) \u2014 a protective device with a Protection "
                             "Rating (1d100 <= rating nullifies the hit) and an "
                             "Overload chance. Feed to the system-translator skill "
                             "for the paired 3.5e AND GURPS treatment. The raw_block "
                             "is OCR text from a column-dump table."),
            "name": f.name, "system": SYSTEM,
            "source": {"book": f.book, "pdf_page": f.page,
                       "extraction": str(corpus.base / src.path),
                       "line": f.line, "citation": src.citation},
            "parsed": {k: v for k, v in asdict(f).items()
                       if k in ("protection_rating", "overload", "weight",
                                "availability", "req", "renown") and v},
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


# --- selftest ---------------------------------------------------------------
# A column-dump fixture exercising both real template shapes: the Only War /
# Black Crusade Name|Protection Rating|Weight|Availability (with a two-word rarity
# and a '(...)' name), and the Deathwatch Name|Protection|Rating|Overload|Wt|Req|
# Renown (with a wrapped "Protection"/"Rating" header and a 'kg'-suffixed weight).
# A craftsmanship overload table and a trailing Relics table prove the region
# boundaries hold; an in-region prose line proves prose never banks.
FIXTURE = """## [PDF page 200]
Table 6-19: Force Fields
Name
Protection Rating
Weight kg
Availability
Refractor Field
30
2
Very Rare
Conversion Field
50
1
Extremely Rare
Power Field (Personal)
80
50
Near Unique
Table 6-18: Field Overload Chance
Field Craftsmanship
Overload Roll
Poor
01-15

## [PDF page 201]
Table5\u201314:Force Fields
Name
Protection
Rating
Overload Roll
Wt
Req
Renown
Astartes Storm Shield
55
01\u201310
10
35
Distinguished
Iron Halo
50
01
0.5 kg
40
Hero
Iron halos are precious relics of the Chapter.
Table 5-99: Relics
Name
Req
"""

FIXTURE_TITLES = {"force fields": "Force Field"}


def selftest(base: Path) -> int:
    failures: List[str] = []

    lines = FIXTURE.splitlines()
    fields, soft, nreg = detect_forcefields(
        lines, _pages_for(lines), "Fixture Core Rulebook", "Fixture", FIXTURE_TITLES)
    by = {f.name: f for f in fields}
    names = [f.name for f in fields]
    want = ["Refractor Field", "Conversion Field", "Power Field (Personal)",
            "Astartes Storm Shield", "Iron Halo"]
    if names != want:
        failures.append(f"fixture detected {names}, wanted {want}")
    else:
        checks = [
            # name, protection_rating, overload, weight, availability, req, renown
            ("Refractor Field", "30", None, "2", "Very Rare", None, None),
            ("Conversion Field", "50", None, "1", "Extremely Rare", None, None),
            ("Power Field (Personal)", "80", None, "50", "Near Unique", None, None),
            ("Astartes Storm Shield", "55", "01\u201310", "10", None, "35", "Distinguished"),
            ("Iron Halo", "50", "01", "0.5 kg", None, "40", "Hero"),
        ]
        for nm, pr, ov, wt, av, rq, rn in checks:
            f = by[nm]
            got = (f.protection_rating, f.overload, f.weight, f.availability,
                   f.req, f.renown, f.system)
            exp = (pr, ov, wt, av, rq, rn, SYSTEM)
            if got != exp:
                failures.append(f"{nm} parsed {got}, wanted {exp}")
    if any("halos are" in f.name.lower() or "precious" in f.name.lower() for f in fields):
        failures.append("fixture prose line leaked into the index as a field row")
    if any(_avnorm(f.name) in ("field craftsmanship", "poor", "overload roll")
           for f in fields):
        failures.append("a craftsmanship/overload-table cell escaped as a field")

    if base.is_dir() and any((base / s.path).exists() for s in SOURCES):
        corpus = Corpus(base, _fresh_sources())
        counts = {s.key: len(s.forcefields) for s in corpus.sources}
        total = sum(counts.values())
        if total != 13:
            failures.append(f"{total} force fields indexed across the cores; expected 13")
        for key, want_n in (("dw-core", 3), ("ow-core", 5), ("bc-core", 5)):
            if counts.get(key) != want_n:
                failures.append(f"{key} yielded {counts.get(key)} force fields; expected {want_n}")
        for key in ("dh-core", "rt-core"):
            src = next(s for s in corpus.sources if s.key == key)
            if (base / src.path).exists() and not src.coverage.startswith("NO COVERAGE"):
                failures.append(f"{key} should report NO COVERAGE, got: {src.coverage}")
        for _, f in corpus.all_fields():
            if f.system != SYSTEM:
                failures.append(f"{f.name}: system stamp is {f.system!r}")
                break
            if not f.name:
                failures.append("a live force-field row has an empty name")
                break
            if not (f.protection_rating and RE_INT.match(f.protection_rating)):
                failures.append(f"{f.name}: missing/invalid protection rating "
                                f"{f.protection_rating!r}")
                break
            if _avnorm(f.name) in HEADER_TOKENS or _avnorm(f.name) in RARITIES \
                    or _avnorm(f.name) in RENOWN_RANKS:
                failures.append(f"header/junk name banked: {f.name!r}")
                break
        # Known fields resolve where they should.
        refr = corpus.find("Refractor Field")
        refr_books = {f.book for _, f in refr}
        if not any("Only War" in b for b in refr_books) or not any("Black Crusade" in b for b in refr_books):
            failures.append(f"Refractor Field not found in both Only War and Black Crusade: {refr_books}")
        if refr and not all(f.protection_rating == "30" for _, f in refr):
            failures.append("live Refractor Field protection rating is not 30 everywhere")
        halo = corpus.find("Iron Halo")
        if not halo:
            failures.append("Iron Halo not found in live corpus")
        elif not all(f.protection_rating == "50" and f.overload and f.req and f.renown
                     for _, f in halo):
            failures.append("live Iron Halo missing protection/overload/req/renown")
        for known in ("Conversion Field", "Displacer Field", "Astartes Storm Shield"):
            if not corpus.find(known):
                failures.append(f"known force field not found in live corpus: {known}")
    else:
        print("  [SKIP] 40K RP extractions not found \u2014 fixture checks only")

    for f in failures:
        print(f"SELFTEST FAIL: {f}")
    print("selftest: " + ("PASS" if not failures else f"{len(failures)} failure(s)"))
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--corpus", type=Path, default=CORPUS)
    ap.add_argument("--search", metavar="TEXT")
    ap.add_argument("--book")
    ap.add_argument("--export", metavar="NAME")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest(args.corpus)

    corpus = Corpus(args.corpus, _fresh_sources())

    if args.search:
        q = args.search.lower()
        found = sorted({(f.name, f.protection_rating or "\u2014", f.book, f.page or -1)
                        for _, f in corpus.all_fields(args.book) if q in f.name.lower()})
        for name, pr, bk, page in found:
            loc = bk if page < 0 else f"{bk}, p.{page}"
            print(f"  {name}   [PR {pr}; {loc}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.forcefields for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.forcefields):3d} field(s)" if src.forcefields else "  NO COVERAGE"
        soft = f" (+{len(src.soft)} soft)" if src.soft else ""
        tag = src.coverage.split(" \u2014 ")[0]
        print(f"  {src.book:30s} {status}{soft}  [{tag}]")
    if not any_ok:
        print("\nNothing harvested \u2014 refusing to write empty reference files.")
        return 1
    total, covered = write_index(corpus)
    print(f"\n{total} WH40K Roleplay force fields across {covered} book(s) "
          f"(system: {SYSTEM}).")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
