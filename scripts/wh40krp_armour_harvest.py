#!/usr/bin/env python3
"""wh40krp_armour_harvest.py — collate WH40K Roleplay armour (system: WH40K Roleplay).

THE PROCESS (Chad, opening the 40K shelf): other GAME SYSTEMS are welcome in the
reference layer AS LONG AS each is clearly LABELLED by system — the translator
tools convert them into the hybrid's 3.5e + GURPS. This is the **Warhammer
40,000 Roleplay** (Fantasy Flight Games d100) ARMOUR index — Dark Heresy / Rogue
Trader / Deathwatch / Only War / Black Crusade — kept entirely separate and
stamped `"system": "WH40K Roleplay"`. Sibling of wh40krp_weapon_harvest.py; it
solves the same books and the same OCR column-dump, for armour.

    reference/wh40krp_armour_index.json — every armour piece: name, category,
                                          locations, armour_points, weight, cost,
                                          availability, req, renown, notes,
                                          book + PDF page
    reference/wh40krp_armour_index.md   — the same, for human eyes

`--export` emits a translator-ready packet (a 40K RP armour the system-translator
skill converts to the 3.5e + GURPS pair).

WORKFLOW
    python wh40krp_armour_harvest.py                     # (re)build the index
    python wh40krp_armour_harvest.py --search "carapace" # find candidates
    python wh40krp_armour_harvest.py --export "Flak Vest"
    python wh40krp_armour_harvest.py --selftest

GOVERNING SOURCES
    I:\\Sourcebooks\\_text\\Warhammer\\40K Roleplay\\ — the five core rulebooks.
    Their Armour tables (Table 5-12 "Armour" and its kin) were OCR'd as a VERTICAL
    COLUMN-DUMP: each armour piece is a run of cells, one per line, in a fixed
    column order that VARIES BY BOOK —
        DH:  Name, Location(s) Covered, AP, Wt, Cost, Availability
        RT:  Name, Locations Covered, AP, kg, Availability          (no Cost)
        OW:  Name, Locations Covered, AP, Weight, Availability      (no Cost)
        BC:  Name, Locations Covered, AP, Wt, Availability          (no Cost)
        DW:  Name, Locations Covered, AP, kg, Req, Renown           (no Cost/Avail)
    The detector ANCHORS on the AP cell (a small integer, a split like "8/10", or
    "Varies") that sits BETWEEN a Locations phrase and a Weight value. The name is
    read BACKWARD from the anchor; the trailing fields are read FORWARD and
    assigned by the book's schema, so the messier books still parse:
      * Rogue Trader wraps names ("Advanced Helmet"+"Systems") and locations
        ("Arms, Body,"+"Legs") across lines, fuses weight+availability ("0.5 Rare",
        "40 Ext. Rare"), and SCRAMBLES its power-armour block (both names+locations,
        then both stats) — recovered by un-shuffling the block from its own cells.
      * Deathwatch grades by Req/Renown (no Cost/Availability), splits power-armour
        AP ("8/10"), lists "Varies", and uses category-shaped names as REAL rows.
    A configured source whose file is missing prints NO COVERAGE. Book RAW only —
    every stat is the book's, cited to book + PDF page; nothing is invented. Rows
    whose AP the OCR left as a dash (utility screens/upgrades) are captured into a
    `soft` list with armour_points empty rather than fabricated.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CORPUS = Path(r"I:\Sourcebooks\_text")
REPO = Path(__file__).resolve().parent.parent
OUT_JSON = REPO / "reference" / "wh40krp_armour_index.json"
OUT_MD = REPO / "reference" / "wh40krp_armour_index.md"
SYSTEM = "WH40K Roleplay"

PAGE = re.compile(r"\[PDF page (\d+)\]")
DASHES = "\u2013\u2014-"                         # en-dash / em-dash / hyphen

# --- cell-level patterns (a cell is one column value from the OCR column-dump) --
# AP: the anchor. A small integer ("1".."14"), a location-split value ("8/10"),
# or the literal "Varies" (Deathwatch primitive armour).
RE_AP = re.compile(r"^\d{1,2}$|^\d{1,2}\s*/\s*\d{1,2}$")
# Weight: a number optionally signed and optionally kg-suffixed ("5 kg", "0.5",
# "40", "+0.5 kg", "10.2 kg"), or the leading number of a fused "40 Ext. Rare".
RE_WT_LEAD = re.compile(r"^\+?\d{1,3}(?:\.\d{1,2})?(?:\s*kg\.?)?", re.IGNORECASE)
RE_WT_PURE = re.compile(r"^\+?\d{1,3}(?:\.\d{1,2})?(?:\s*kg\.?)?$", re.IGNORECASE)
RE_INT = re.compile(r"^[\d,]{1,7}$")             # cost / req (may carry commas)
RE_DASH = re.compile(rf"^[{DASHES}]+$")

# Location vocabulary: a cell is a Locations-Covered value iff, once commas are
# dropped, every token is one of these body words. Handles "Arms, Body, Legs",
# "Body, Arms", "Arms, Body Legs" (OCR-dropped comma), "All", "Head", "Varies".
LOC_WORDS = {"all", "head", "body", "arms", "legs", "varies"}

# Category sub-headers (a closed set). In DH/RT/OW/BC these GROUP the rows; in
# Deathwatch the same strings are REAL armour rows (distinguished positionally:
# a category header is NOT immediately followed by a Locations cell).
CATEGORY_HEADERS = {
    "primitive armour", "flak armour", "mesh armour", "carapace armour",
    "power armour", "exotic armour", "other armours", "advanced armour",
}

# Availability rarity ladder (a closed set). Two-word rarities appear as one cell
# in DH/OW/BC and fused onto the weight in Rogue Trader.
RARITIES = {
    "ubiquitous", "abundant", "plentiful", "common", "average", "scarce",
    "rare", "very rare", "extremely rare", "ext. rare", "near unique", "unique",
}
RARITY_TAIL = re.compile(
    r"(ubiquitous|abundant|plentiful|common|average|scarce|extremely rare|"
    r"ext\.\s*rare|very rare|near unique|unique|rare)\s*$", re.IGNORECASE)

# Deathwatch grades by Renown (not Availability); a Req cell is "N/A" or digits
# possibly carrying dagger footnotes ("60†", "100†††"). These
# must read as stat cells so the backward name read stops at them.
RENOWN_WORDS = {"respected", "distinguished", "famed", "hero"}

# Column-header / structural words that can never be an armour name.
HEADER_WORDS = {
    "name", "locations covered", "location(s) covered", "locations", "covered",
    "ap", "wt", "wt.", "weight", "kg", "cost", "availability", "req", "renown",
    "armour type", "locations covered ap", "ap kg avail.", "avail", "avail.",
}


def _clean_name(s: str) -> str:
    s = s.replace("\ufb01", "fi").replace("\ufb02", "fl")   # OCR ligatures
    s = re.sub(r"\s+", " ", s).strip()
    s = s.strip(" ,\u2013\u2014-\u2020*\u00a0")             # daggers, dashes, etc.
    return s.strip()


def _is_location(t: str) -> bool:
    t = t.strip()
    if not t:
        return False
    toks = [w for w in re.split(r"[,\s]+", t) if w]
    if not toks:
        return False
    return all(w.lower() in LOC_WORDS for w in toks)


def _norm_location(t: str) -> str:
    return re.sub(r"\s+", " ", t.replace(",", ", ")).replace(" ,", ",").strip(" ,")


def _is_ap_cell(t: str) -> bool:
    t = t.strip()
    return bool(RE_AP.match(t)) or t.lower() == "varies"


def _parse_ap(t: str):
    """int when a plain integer; the raw string for a split ("8/10") or "Varies"."""
    t = t.strip()
    if re.fullmatch(r"\d{1,2}", t):
        return int(t)
    return re.sub(r"\s*/\s*", "/", t)


def _is_weightish(t: str) -> bool:
    t = t.strip()
    return bool(RE_WT_LEAD.match(t)) or t.lower().startswith("varies")


def _weight_token(t: str) -> Optional[str]:
    t = t.strip()
    if not t or RE_DASH.match(t):
        return None
    if t.lower().startswith("varies"):
        return "Varies"
    m = RE_WT_LEAD.match(t)
    if m:
        return re.sub(r"\s+", " ", m.group(0)).strip()
    return None


def _is_rarity(t: str) -> bool:
    return t.strip().lower() in RARITIES


def _split_weight_rarity(t: str) -> Optional[Tuple[str, str]]:
    """RT fuses weight+availability ("0.5 Rare", "40 Ext. Rare"). Split iff a
    rarity sits on the tail and a real weight leads. Returns (weight, avail)."""
    t = t.strip()
    if RE_WT_PURE.match(t):                       # a clean weight, nothing fused
        return None
    m = RARITY_TAIL.search(t)
    if not m:
        return None
    head = t[:m.start()].strip()
    wt = _weight_token(head)
    if wt is None or head == "":
        return None
    return wt, re.sub(r"\s+", " ", m.group(1)).strip()


def _is_stat_like(t: str) -> bool:
    """A cell that is a number / rarity / renown / dash / weight — never a name."""
    t = t.strip()
    if not t or RE_DASH.match(t):
        return True
    low = t.lower()
    if RE_INT.match(t) or RE_WT_PURE.match(t) or _is_ap_cell(t):
        return True
    if low in RARITIES or low.startswith("varies"):
        return True
    if RARITY_TAIL.search(t) and _is_weightish(t):    # fused weight+rarity
        return True
    bare = t.rstrip("†‡*").strip()          # drop dagger footnote marks
    lowb = bare.lower()
    if lowb == "n/a" or lowb in RENOWN_WORDS or (bare and RE_INT.match(bare)):
        return True                                   # Deathwatch Req / Renown cell
    return False


def _is_prose(t: str) -> bool:
    t = t.strip()
    return len(t) > 45 or t.count(" ") > 6


def _name_ish(t: str) -> bool:
    """Could this cell be (part of) an armour name?"""
    t = t.strip()
    if not t or not (t[0].isalpha() or t[0] == "("):
        return False
    if _is_location(t) or _is_stat_like(t) or _is_prose(t):
        return False
    if t.lower() in HEADER_WORDS:
        return False
    return True


def _plausible_name(s: str) -> bool:
    s = _clean_name(s)
    if not (2 <= len(s) <= 45):
        return False
    if not s[0].isalnum():
        return False
    low = s.lower()
    if low in HEADER_WORDS or low in RARITIES or _is_location(s):
        return False
    return sum(c.isalpha() for c in s) >= 2


@dataclass
class Armour:
    name: str
    book: str
    page: Optional[int]
    start: int                     # source line (1-based when reported)
    end: int
    system: str = SYSTEM
    category: Optional[str] = None
    locations: Optional[str] = None
    armour_points: Optional[object] = None       # int, or str ("8/10", "Varies")
    weight: Optional[str] = None
    cost: Optional[str] = None
    availability: Optional[str] = None
    req: Optional[str] = None
    renown: Optional[str] = None
    notes: Optional[str] = None
    soft: bool = False

    def quick_fields(self) -> int:
        return sum(1 for v in (self.category, self.locations, self.armour_points,
                               self.weight, self.cost, self.availability,
                               self.req, self.renown) if v not in (None, ""))


@dataclass
class Cell:
    text: str
    line: int
    page: int
    region: bool


def _pages_for(lines: List[str]) -> List[int]:
    pages: List[int] = []
    page = 0
    for ln in lines:
        m = PAGE.search(ln)
        if m:
            page = int(m.group(1))
        pages.append(page)
    return pages


# Armour-table titles open a region; the next "Table ..." title closes it. The
# opener must end in ": Armour" so "Armour Upgrades" / "Power Armour History" do
# not (re)open it.
RE_TBL_ANY = re.compile(r"^\s*Table\s*\S", re.IGNORECASE)
RE_TBL_ARMOUR = re.compile(r"^\s*Table\s*\S.*:\s*Armou?r\s*$", re.IGNORECASE)


def _regions(lines: List[str]) -> List[bool]:
    inside = [False] * len(lines)
    open_ = False
    for i, ln in enumerate(lines):
        if RE_TBL_ANY.match(ln):
            open_ = bool(RE_TBL_ARMOUR.match(ln))
        inside[i] = open_
    return inside


def _build_cells(lines: List[str], pages: List[int], region: List[bool]) -> List[Cell]:
    cells: List[Cell] = []
    for i, ln in enumerate(lines):
        if PAGE.search(ln):
            continue
        for piece in ln.split("\t"):
            s = piece.strip()
            if s:
                cells.append(Cell(s, i, pages[i], region[i]))
    return cells


def _categories_by_index(cells: List[Cell]) -> List[Optional[str]]:
    """Track the current category sub-header per cell index. A category header is
    a CATEGORY_HEADERS cell (or a two-cell wrapped one, RT's "Carapace"+"Armour")
    that is NOT immediately followed by a Locations cell (which would make it a
    Deathwatch-style row name)."""
    n = len(cells)
    cat_at: List[Optional[str]] = [None] * n
    cur: Optional[str] = None
    for i in range(n):
        if not cells[i].region:
            cur = None
            cat_at[i] = None
            continue
        low = cells[i].text.strip().lower()
        nxt = cells[i + 1].text if i + 1 < n else ""
        if low in CATEGORY_HEADERS and not _is_location(nxt):
            cur = re.sub(r"\s+", " ", cells[i].text).strip()
        elif (i + 1 < n and cells[i + 1].region
              and (low + " " + cells[i + 1].text.strip().lower()) in CATEGORY_HEADERS
              and not _is_location(cells[i + 2].text if i + 2 < n else "")):
            cur = _clean_name(cells[i].text + " " + cells[i + 1].text)
        cat_at[i] = cur
    return cat_at


def _read_location_before(cells: List[Cell], p: int) -> Optional[Tuple[str, int]]:
    """From an AP anchor at p, read the Locations cell(s) just before it. Absorbs
    a wrapped location fragment (RT's "Arms, Body," + "Legs"). Returns
    (normalised location, index of the cell before the location) or None."""
    if p - 1 < 0 or not cells[p - 1].region or not _is_location(cells[p - 1].text):
        return None
    loc_idx = p - 1
    loc = cells[loc_idx].text
    while (loc_idx - 1 >= 0 and cells[loc_idx - 1].region
           and _is_location(cells[loc_idx - 1].text)
           and cells[loc_idx - 1].text.rstrip().endswith(",")):
        loc = cells[loc_idx - 1].text + " " + loc
        loc_idx -= 1
    return _norm_location(loc), loc_idx - 1


def _read_name_backward(cells: List[Cell], name_end: int) -> Tuple[str, int]:
    """Returns (name, index of the first name cell) read backward from name_end."""
    parts: List[str] = []
    j, steps, first = name_end, 0, name_end
    while j >= 0 and steps < 4 and cells[j].region:
        c = cells[j].text
        low = c.strip().lower()
        if low in HEADER_WORDS or _is_stat_like(c) or _is_location(c):
            break
        if low in CATEGORY_HEADERS:
            if not parts:                       # Deathwatch: the category word IS
                parts.insert(0, c)              # the row's name (Carapace Armour…)
                first = j
            break
        if (j - 1 >= 0 and cells[j - 1].region and parts and
                (cells[j - 1].text.strip() + " " + c.strip()).lower()
                in CATEGORY_HEADERS):           # RT wrapped header ("Carapace"+"Armour")
            break
        if _is_prose(c):
            break
        parts.insert(0, c)
        first = j
        j -= 1
        steps += 1
    return _clean_name(" ".join(parts)), first


def _forward_fields(cells: List[Cell], p: int, schema: str) -> dict:
    """Read the trailing fields after the AP anchor at p, by the book's schema."""
    nxt: List[str] = []
    q = p + 1
    while q < len(cells) and cells[q].region and len(nxt) < 4:
        nxt.append(cells[q].text)
        q += 1
    out: dict = {}
    if not nxt:
        return out

    if schema == "cost_avail":                  # DH: Wt, Cost, Availability
        out["weight"] = _weight_token(nxt[0])
        if len(nxt) > 1 and RE_INT.match(nxt[1].strip()):
            out["cost"] = nxt[1].strip()
        if len(nxt) > 2 and _is_rarity(nxt[2]):
            out["availability"] = re.sub(r"\s+", " ", nxt[2]).strip()
    elif schema == "req_renown":                # DW: kg, Req, Renown
        out["weight"] = _weight_token(nxt[0])
        if len(nxt) > 1:
            out["req"] = nxt[1].strip()
        if len(nxt) > 2:
            out["renown"] = nxt[2].strip()
    else:                                       # RT/OW/BC: Wt, Availability
        split = _split_weight_rarity(nxt[0])
        if split:
            out["weight"], out["availability"] = split
        else:
            out["weight"] = _weight_token(nxt[0])
            if len(nxt) > 1 and _is_rarity(nxt[1]):
                out["availability"] = re.sub(r"\s+", " ", nxt[1]).strip()
    return out


def _recover_scramble(cells: List[Cell], cat_at: List[Optional[str]], book: str,
                      out: List[Armour], consumed: set) -> None:
    """Rogue Trader's power-armour block is OCR-reordered as
    [Name1, Loc1, Name2, Loc2, AP1, Wt+Avail1, AP2, Wt+Avail2]. Detect that exact
    shape and un-shuffle it from the block's own cells. Marked soft so a human can
    verify the reconstruction."""
    n = len(cells)
    for i in range(1, n - 6):
        block = cells[i - 1:i + 7]
        if not all(c.region for c in block):
            continue
        n1, l1, n2, l2, a1, w1, a2, w2 = (c.text for c in block)
        if not (_name_ish(n1) and _is_location(l1) and _name_ish(n2)
                and _is_location(l2) and re.fullmatch(r"\d{1,2}", a1.strip())
                and _is_weightish(w1) and re.fullmatch(r"\d{1,2}", a2.strip())
                and _is_weightish(w2)):
            continue
        for offset, (nm, lc, ap, wa) in enumerate(
                ((n1, l1, a1, w1), (n2, l2, a2, w2))):
            idx = (i - 1) if offset == 0 else (i + 1)
            split = _split_weight_rarity(wa)
            wt = split[0] if split else _weight_token(wa)
            av = split[1] if split else None
            out.append(Armour(
                name=_clean_name(nm), book=book, page=cells[idx].page,
                start=cells[idx].line + 1, end=cells[i + 6].line + 2,
                category=cat_at[idx], locations=_norm_location(lc),
                armour_points=_parse_ap(ap), weight=wt, availability=av,
                soft=True,
                notes="AP/weight/availability recovered by un-scrambling the "
                      "OCR-reordered power-armour block"))
        consumed.update(range(i - 1, i + 7))
        return


def _recover_dashap(cells: List[Cell], cat_at: List[Optional[str]], book: str,
                    schema: str, consumed: set) -> List[Armour]:
    """Utility rows whose AP the OCR left as a dash (Deathwatch 'Masking Screen',
    Rogue Trader 'Advanced Helmet Systems'). Captured with armour_points empty and
    flagged soft — never invented."""
    n = len(cells)
    softs: List[Armour] = []
    for p in range(1, n - 1):
        if p in consumed:
            continue
        if not (cells[p].region and RE_DASH.match(cells[p].text)):
            continue                            # p = the dash AP cell
        prev = cells[p - 1].text
        if not (cells[p - 1].region and (RE_DASH.match(prev) or _is_location(prev))):
            continue                            # p-1 = Locations (dash or a phrase)
        # read the name backward from the cell before the (dashed) location
        name, name_start = _read_name_backward(cells, p - 2)
        if not _plausible_name(name):
            continue
        # forward trailing fields (weight/req/renown/avail), AP intentionally empty
        fwd = _forward_fields(cells, p, schema)
        softs.append(Armour(
            name=name, book=book, page=cells[p].page,
            start=cells[name_start].line + 1, end=cells[p].line + 4,
            category=cat_at[p], locations=None if RE_DASH.match(prev)
            else _norm_location(prev), armour_points=None,
            weight=fwd.get("weight"), cost=fwd.get("cost"),
            availability=fwd.get("availability"), req=fwd.get("req"),
            renown=fwd.get("renown"), soft=True,
            notes="AP is a dash in the source (utility/upgrade item); left empty"))
    return softs


def detect_armour(lines: List[str], pages: List[int], book: str,
                  schema: str = "avail", allow_scramble: bool = False) -> List[Armour]:
    region = _regions(lines)
    cells = _build_cells(lines, pages, region)
    cat_at = _categories_by_index(cells)
    n = len(cells)

    armour: List[Armour] = []
    consumed: set = set()

    if allow_scramble:
        _recover_scramble(cells, cat_at, book, armour, consumed)

    for p in range(n):
        if p in consumed:
            continue
        if not (cells[p].region and _is_ap_cell(cells[p].text)):
            continue
        loc = _read_location_before(cells, p)
        if loc is None:
            continue
        location, name_end = loc
        if not (p + 1 < n and cells[p + 1].region and _is_weightish(cells[p + 1].text)):
            continue
        name, name_start = _read_name_backward(cells, name_end)
        if not _plausible_name(name):
            continue
        fwd = _forward_fields(cells, p, schema)
        armour.append(Armour(
            name=name, book=book, page=cells[p].page,
            start=cells[name_start].line + 1, end=cells[p].line + 6,
            category=cat_at[name_end + 1] if name_end + 1 < n else cat_at[p],
            locations=location, armour_points=_parse_ap(cells[p].text),
            weight=fwd.get("weight"), cost=fwd.get("cost"),
            availability=fwd.get("availability"), req=fwd.get("req"),
            renown=fwd.get("renown")))

    armour.extend(_recover_dashap(cells, cat_at, book, schema, consumed))

    # footnotes (BC "† Obsidian Armour negates ...") — attach to the named row.
    for c in cells:
        if not c.region:
            continue
        t = c.text.strip()
        if not (t[:1] in ("\u2020", "*") and len(t) > 6):
            continue
        body = t.lstrip("\u2020*\u2021 ").strip()
        for a in armour:
            if a.notes is None and a.name.lower() in body.lower():
                a.notes = body

    # one row per (name, book): keep the richest, then the first seen.
    best: Dict[str, Armour] = {}
    order: List[str] = []
    for a in armour:
        k = a.name.lower()
        if k not in best:
            order.append(k)
            best[k] = a
        elif a.quick_fields() > best[k].quick_fields():
            best[k] = a
    return sorted(best.values(), key=lambda a: (a.start, a.name))


@dataclass
class Source:
    key: str
    book: str
    path: Path
    citation: str
    schema: str
    allow_scramble: bool = False
    coverage: str = "pending"
    lines: List[str] = field(default_factory=list)
    armour: List[Armour] = field(default_factory=list)


_40K = Path("Warhammer/40K Roleplay")
SOURCES: List[Source] = [
    Source("dh-core", "Dark Heresy — Core Rulebook",
           _40K / "Dark Heresy/Rulebooks/Dark Heresy - Core Rulebook.pdf.md",
           "Dark Heresy Core Rulebook (FFG, WH40K Roleplay), Armoury, "
           "Table 5-12: Armour [PDF page 146]", "cost_avail"),
    Source("rt-core", "Rogue Trader — Core Rulebook",
           _40K / "Rogue Trader/Rulebooks/Rogue Trader - Core Rulebook (updated with 1.4 errata).md",
           "Rogue Trader Core Rulebook, 1.4 errata (FFG, WH40K Roleplay), Armoury, "
           "Table 5-12: Armour [PDF page 139]", "avail", True),
    Source("dw-core", "Deathwatch — Core Rulebook",
           _40K / "Deathwatch/Rulebooks/Deathwatch - Core Rulebook.md",
           "Deathwatch Core Rulebook (FFG, WH40K Roleplay), Armoury, "
           "Table 5-13: Armour (uses Req/Renown, not Cost/Availability) "
           "[PDF page 166]", "req_renown"),
    Source("ow-core", "Only War — Core Rulebook",
           _40K / "Only War/Rulebooks/Only War - Core Rulebook.md",
           "Only War Core Rulebook (FFG, WH40K Roleplay), Armoury, "
           "Table 6-17: Armour [PDF page 196]", "avail"),
    Source("bc-core", "Black Crusade — Core Rulebook",
           _40K / "Black Crusade/Rulebooks/Black Crusade - Core Rulebook.md",
           "Black Crusade Core Rulebook (FFG, WH40K Roleplay), Armoury, "
           "Table 5-10: Armour [PDF page 175]", "avail"),
]


def _fresh_sources() -> List[Source]:
    return [Source(s.key, s.book, s.path, s.citation, s.schema, s.allow_scramble)
            for s in SOURCES]


class Corpus:
    def __init__(self, base: Path, sources: List[Source]):
        self.base = base
        self.sources = sources
        for src in self.sources:
            path = base / src.path
            if not path.exists():
                src.coverage = f"NO COVERAGE — extraction missing: {path}"
                continue
            src.lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            pages = _pages_for(src.lines)
            src.armour = detect_armour(src.lines, pages, src.book, src.schema,
                                       src.allow_scramble)
            n_soft = sum(1 for a in src.armour if a.soft)
            src.coverage = (f"ok — {len(src.armour)} armour from {path.name}"
                            + (f" ({n_soft} soft)" if n_soft else ""))

    def all_armour(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for a in src.armour:
                yield src, a

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, a in self.all_armour(book):
            nm = a.name.lower()
            if nm == q:
                exact.append((src, a))
            elif q in nm:
                partial.append((src, a))
        return exact if exact else partial


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    soft_total = 0
    sources_out = []
    md: List[str] = [
        "# WH40K ROLEPLAY ARMOUR INDEX — The New Path",
        "",
        "**Generated by `scripts/wh40krp_armour_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** These are **Warhammer 40,000 Roleplay** armour —",
        "the Fantasy Flight Games d100 line (Dark Heresy / Rogue Trader /",
        "Deathwatch / Only War / Black Crusade). Every row is stamped",
        f"`system: {SYSTEM}`; a 40K RP armour is SOURCE MATERIAL for the",
        "system-translator skill, not campaign RAW. The Armoury stat tables were",
        "OCR'd as column-dumps; a field left `—` is one the source does not carry",
        "(e.g. Rogue Trader/Only War/Black Crusade have no Cost column; Deathwatch",
        "grades by Req/Renown, not Cost/Availability). Rows marked **(soft)** had",
        "their AP left as a dash in the source, or were recovered from an",
        "OCR-scrambled block — verify against the book. Use `--export \"NAME\"` for",
        "the translator packet.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.armour)
        soft_total += sum(1 for a in src.armour if a.soft)
        sources_out.append({"key": src.key, "book": src.book, "system": SYSTEM,
                            "citation": src.citation, "coverage": src.coverage,
                            "armour": [asdict(a) for a in src.armour]})
        md.append(f"## {src.book} — {len(src.armour)} armour  *(system: {SYSTEM})*")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.armour:
            md.append("| Armour | Category | Locations | AP | Weight | Cost | "
                      "Avail | Req | Renown | Page | Notes |")
            md.append("|---|---|---|---|---|---|---|---|---|---|---|")
            for a in src.armour:
                nm = a.name + (" *(soft)*" if a.soft else "")
                ap = "—" if a.armour_points in (None, "") else str(a.armour_points)
                md.append(
                    f"| {nm} | {a.category or '—'} | {a.locations or '—'} | "
                    f"{ap} | {a.weight or '—'} | {a.cost or '—'} | "
                    f"{a.availability or '—'} | {a.req or '—'} | "
                    f"{a.renown or '—'} | {a.page if a.page is not None else '—'} | "
                    f"{a.notes or '—'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/wh40krp_armour_harvest.py",
                    "system": SYSTEM, "corpus": str(corpus.base),
                    "total_armour": total, "soft_rows": soft_total,
                    "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, soft_total


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 8:
        print(f"'{name}' matches {len(hits)} armour; narrow with --book or the exact name:")
        for src, a in hits[:20]:
            print(f"  {a.name}   [{a.book}, p.{a.page}]")
        return 1
    packets = []
    for src, a in hits:
        lo = max(0, a.start - 1)
        body = [ln for ln in src.lines[lo:a.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "wh40krp-armour-for-translation",
            "instructions": ("A Warhammer 40,000 Roleplay armour (system: "
                             f"{SYSTEM}). Feed to the system-translator skill for "
                             "the paired 3.5e AND GURPS treatment. The raw_block "
                             "is OCR text from a column-dump table."),
            "name": a.name, "system": SYSTEM,
            "source": {"book": a.book, "pdf_page": a.page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [a.start, a.end], "citation": src.citation},
            "parsed": {k: v for k, v in asdict(a).items()
                       if k in ("category", "locations", "armour_points", "weight",
                                "cost", "availability", "req", "renown", "notes")
                       and v not in (None, "")},
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
# Three column-dump fixtures, one per schema, built from REAL rows of the cores.
FIXTURE_DH = """## [PDF page 146]
Table 5-12: Armour
Armour Type
Location(s) Covered
AP
Wt
Cost
Availability
Primitive Armour
Gang Leathers
Arms, Body, Legs
1
5 kg
25
Average
Carapace Armour
Storm Trooper Carapace
All
6
17 kg
3,750
Very Rare
Power Armour
Light Power Armour
All
7
40 kg
8,500
Very Rare
Power Armour
All
8
65 kg
15,000
Very Rare
Table 5-13: Clothing & Personal Items
Name
"""

FIXTURE_DW = """## [PDF page 166]
Table 5\u201313: Armour
Name
Locations Covered AP
kg
Req
Renown
Astartes Power Armour
All
8/10
180
N/A
\u2013
Astartes Artificer Armour
All
12
100
60\u2020
Hero\u2020\u2020
Astartes Scout Armour
Body, Arms
6
30
N/A
\u2014
Primitive Armour
Varies
Varies
Varies
N/A
N/A
Flak Armour
All
4
15
N/A
\u2013
Table 5\u201314: Force Fields
Name
"""

FIXTURE_RT = """## [PDF page 139]
Table 5\u201312: Armour
Name
Locations
Covered
AP kg Avail.
Mesh Armour
Mesh Cowl
Head
3
0.5 Rare
Mesh Combat Cloak
Arms, Body,
Legs
4
1.5 Very Rare
Carapace
Armour
Carapace Helm
Head
4
2
Rare
Power Armour
Light Power Armour
All
Power Armour
All
7
40 Ext. Rare
8
65 Ext. Rare
Table 5\u201313: Gear
Name
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    # --- DH fixture (cost_avail) ---
    ls = FIXTURE_DH.splitlines()
    dh = detect_armour(ls, _pages_for(ls), "Fixture DH", "cost_avail")
    names = [a.name for a in dh]
    want = ["Gang Leathers", "Storm Trooper Carapace", "Light Power Armour",
            "Power Armour"]
    if names != want:
        failures.append(f"DH fixture names {names}, wanted {want}")
    else:
        by = {a.name: a for a in dh}
        gl = by["Gang Leathers"]
        got = (gl.category, gl.locations, gl.armour_points, gl.weight, gl.cost,
               gl.availability, gl.system)
        exp = ("Primitive Armour", "Arms, Body, Legs", 1, "5 kg", "25",
               "Average", SYSTEM)
        if got != exp:
            failures.append(f"DH Gang Leathers {got}, wanted {exp}")
        pa = by["Power Armour"]
        if (pa.armour_points, pa.weight, pa.cost, pa.availability) != \
                (8, "65 kg", "15,000", "Very Rare"):
            failures.append(f"DH Power Armour bad: {pa}")
        if pa.category != "Power Armour":
            failures.append(f"DH Power Armour category {pa.category!r}")
        st = by["Storm Trooper Carapace"]
        if st.cost != "3,750" or st.availability != "Very Rare":
            failures.append(f"DH Storm Trooper cost/avail {st.cost},{st.availability}")

    # --- DW fixture (req_renown, split AP, Varies, category-shaped names) ---
    ls = FIXTURE_DW.splitlines()
    dw = detect_armour(ls, _pages_for(ls), "Fixture DW", "req_renown")
    names = [a.name for a in dw]
    want = ["Astartes Power Armour", "Astartes Artificer Armour",
            "Astartes Scout Armour", "Primitive Armour", "Flak Armour"]
    if names != want:
        failures.append(f"DW fixture names {names}, wanted {want}")
    else:
        by = {a.name: a for a in dw}
        ap = by["Astartes Power Armour"]
        got = (ap.locations, ap.armour_points, ap.weight, ap.req, ap.renown, ap.cost)
        exp = ("All", "8/10", "180", "N/A", "\u2013", None)
        if got != exp:
            failures.append(f"DW Astartes Power Armour {got}, wanted {exp}")
        sc = by["Astartes Scout Armour"]        # name must not absorb prior Req/Renown
        if (sc.locations, sc.armour_points, sc.req, sc.renown) != \
                ("Body, Arms", 6, "N/A", "\u2014"):
            failures.append(f"DW Scout row bad (Req/Renown bleed?): {sc}")
        ar = by["Astartes Artificer Armour"]
        if ar.req != "60\u2020" or ar.renown != "Hero\u2020\u2020":
            failures.append(f"DW Artificer req/renown {ar.req!r},{ar.renown!r}")
        pr = by["Primitive Armour"]
        if pr.armour_points != "Varies" or pr.weight != "Varies":
            failures.append(f"DW Primitive AP/wt {pr.armour_points},{pr.weight}")
        fl = by["Flak Armour"]
        if fl.armour_points != 4 or fl.req != "N/A":
            failures.append(f"DW Flak AP/req {fl.armour_points},{fl.req}")
        if any(a.availability or a.cost for a in dw):
            failures.append("DW rows must not carry cost/availability")

    # --- RT fixture (avail, wraps, fused weight+avail, scrambled power armour) ---
    ls = FIXTURE_RT.splitlines()
    rt = detect_armour(ls, _pages_for(ls), "Fixture RT", "avail", allow_scramble=True)
    names = sorted(a.name for a in rt)
    want = sorted(["Mesh Cowl", "Mesh Combat Cloak", "Carapace Helm",
                   "Light Power Armour", "Power Armour"])
    if names != want:
        failures.append(f"RT fixture names {names}, wanted {want}")
    else:
        by = {a.name: a for a in rt}
        ch = by["Carapace Helm"]                # wrapped 2-cell category header
        if ch.name != "Carapace Helm" or ch.category != "Carapace Armour" \
                or ch.armour_points != 4:
            failures.append(f"RT Carapace Helm bad (wrapped header bleed?): {ch}")
        mc = by["Mesh Cowl"]
        if (mc.weight, mc.availability, mc.armour_points) != ("0.5", "Rare", 3):
            failures.append(f"RT Mesh Cowl wt/avail/ap {mc.weight},{mc.availability},"
                            f"{mc.armour_points} (fused weight+avail must split)")
        mcc = by["Mesh Combat Cloak"]
        if mcc.locations != "Arms, Body, Legs":
            failures.append(f"RT Mesh Combat Cloak locations {mcc.locations!r} "
                            f"(wrapped location must join)")
        if mcc.weight != "1.5" or mcc.availability != "Very Rare":
            failures.append(f"RT Mesh Combat Cloak wt/avail {mcc.weight},{mcc.availability}")
        lpa = by["Light Power Armour"]
        if (lpa.armour_points, lpa.weight, lpa.availability, lpa.soft) != \
                (7, "40", "Ext. Rare", True):
            failures.append(f"RT Light Power Armour recovered wrong: "
                            f"{lpa.armour_points},{lpa.weight},{lpa.availability},"
                            f"soft={lpa.soft}")
        pa = by["Power Armour"]
        if (pa.armour_points, pa.weight, pa.availability) != (8, "65", "Ext. Rare"):
            failures.append(f"RT Power Armour recovered wrong: {pa}")

    # --- no phantom rows from prose ---
    stray = detect_armour("The suit grants 6 Armour Points to All locations.".splitlines(),
                          [0], "Prose", "avail")
    if stray:
        failures.append(f"prose produced phantom armour: {[a.name for a in stray]}")

    # --- live corpus invariants ---
    if base.is_dir() and any((base / s.path).exists() for s in SOURCES):
        corpus = Corpus(base, _fresh_sources())
        total = sum(len(s.armour) for s in corpus.sources)
        if not (85 <= total <= 140):
            failures.append(f"{total} armour indexed across the cores; expected 85..140")
        floors = {"dh-core": 25, "rt-core": 16, "dw-core": 8, "ow-core": 15,
                  "bc-core": 25}
        for src in corpus.sources:
            if (base / src.path).exists() and len(src.armour) < floors.get(src.key, 8):
                failures.append(f"{src.key} yielded only {len(src.armour)} armour; "
                                f"expected >= {floors.get(src.key, 8)}")
        for known in ("Flak Vest", "Carapace Helm", "Storm Trooper Carapace"):
            if not corpus.find(known):
                failures.append(f"known armour not found in live corpus: {known}")
        for _, a in corpus.all_armour():
            if a.system != SYSTEM:
                failures.append(f"{a.name}: missing/incorrect system stamp")
                break
            if not a.name:
                failures.append("a live armour row has no name")
                break
            if a.armour_points in (None, "") and not a.soft:
                failures.append(f"{a.name}: no AP and not flagged soft")
                break
            if a.name.strip().lower() in HEADER_WORDS:
                failures.append(f"header/junk leaked as a name: {a.name!r}")
                break
        # AP integers must be sane armour values (0..20); strings only "8/10"/"Varies"
        for _, a in corpus.all_armour():
            v = a.armour_points
            if isinstance(v, int) and not (0 <= v <= 20):
                failures.append(f"{a.name}: implausible AP {v}")
                break
    else:
        print("  [SKIP] 40K RP extractions not found — fixture checks only")

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
        found = sorted({(a.name, a.book, a.page or -1,
                         str(a.armour_points) if a.armour_points not in (None, "") else "—")
                        for _, a in corpus.all_armour(args.book) if q in a.name.lower()})
        for name, bk, page, apv in found:
            loc = bk if page < 0 else f"{bk}, p.{page}"
            print(f"  {name}   [AP {apv}; {loc}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.armour for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.armour):4d} armour" if src.armour else "   0 armour"
        print(f"  {src.book:34s} {status}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, soft_total = write_index(corpus)
    print(f"\n{total} WH40K Roleplay armour across "
          f"{sum(1 for s in corpus.sources if s.armour)} book(s); "
          f"{soft_total} soft. (system: {SYSTEM})")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
