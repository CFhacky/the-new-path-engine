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


def _read_name_backward(cells: List[Cell], name_end: int,
                        prose_fn: Callable[[str], bool] = _is_prose) -> Tuple[str, int]:
    """Returns (name, index of the first name cell) read backward from name_end.
    `prose_fn` gates what counts as an over-long prose cell (the supplement path
    passes a looser cap so genuine long armour names — e.g. Ascension's
    'Cadian-pattern "Kasrkin" Storm Trooper Carapace' — are not rejected)."""
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
        if prose_fn(c):
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


def _detect_armour_from_cells(
        cells: List[Cell], cat_at: List[Optional[str]], book: str, schema: str, *,
        allow_scramble: bool = False,
        forward_fn: Callable[[List[Cell], int, str], dict] = _forward_fields,
        ap_ok: Callable[[str], bool] = _is_ap_cell,
        ap_parse: Callable[[str], object] = _parse_ap,
        name_ok: Callable[[str], bool] = _plausible_name,
        prose_fn: Callable[[str], bool] = _is_prose,
        do_dashap: bool = True,
        sanitize_fn: Optional[Callable[[Armour], Optional[Armour]]] = None,
) -> List[Armour]:
    """The shared AP-anchor pipeline. Anchors on an AP cell guarded by a Locations
    phrase before and a Weight after; reads the name backward and the trailing
    fields forward. With the defaults this reproduces the original core behaviour
    exactly — the five core sources run through here unchanged. The supplement
    path overrides the pluggable pieces (forward-field parse, AP/name predicates,
    prose cap, dash-AP off, and a per-row sanitiser)."""
    n = len(cells)

    armour: List[Armour] = []
    consumed: set = set()

    if allow_scramble:
        _recover_scramble(cells, cat_at, book, armour, consumed)

    for p in range(n):
        if p in consumed:
            continue
        if not (cells[p].region and ap_ok(cells[p].text)):
            continue
        loc = _read_location_before(cells, p)
        if loc is None:
            continue
        location, name_end = loc
        if not (p + 1 < n and cells[p + 1].region and _is_weightish(cells[p + 1].text)):
            continue
        name, name_start = _read_name_backward(cells, name_end, prose_fn)
        if not name_ok(name):
            continue
        fwd = forward_fn(cells, p, schema)
        a = Armour(
            name=name, book=book, page=cells[p].page,
            start=cells[name_start].line + 1, end=cells[p].line + 6,
            category=cat_at[name_end + 1] if name_end + 1 < n else cat_at[p],
            locations=location, armour_points=ap_parse(cells[p].text),
            weight=fwd.get("weight"), cost=fwd.get("cost"),
            availability=fwd.get("availability"), req=fwd.get("req"),
            renown=fwd.get("renown"))
        if sanitize_fn is not None:
            a = sanitize_fn(a)
            if a is None:                        # structurally broken row → skip
                continue
        armour.append(a)

    if do_dashap:
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


def detect_armour(lines: List[str], pages: List[int], book: str,
                  schema: str = "avail", allow_scramble: bool = False) -> List[Armour]:
    """CORE detector — the five 40K RP core rulebooks. Builds cells from the core
    region rule and runs the shared pipeline with the original defaults, so its
    output is byte-for-byte unchanged."""
    region = _regions(lines)
    cells = _build_cells(lines, pages, region)
    cat_at = _categories_by_index(cells)
    return _detect_armour_from_cells(cells, cat_at, book, schema,
                                     allow_scramble=allow_scramble)


# ---------------------------------------------------------------------------
# SUPPLEMENT PATH — the armour-bearing 40K RP splatbooks.
#
# The supplements were OCR'd in the SAME column-dump format as the cores, but
# their scans are rougher and their tables less regular, so four things defeat
# the core detector and are handled here ADDITIVELY (the five core sources never
# run through this path):
#   1. The armour table's TITLE is unreliable — it may carry an <Htable> tag, be
#      named for a world type rather than "Armour" ("Hive World Armour", "War
#      Zone Protective Gear", "Protective Devices"), or put "Armour" mid-title
#      ("Feral And Feudal (Primitive) Armour"). Instead of trusting the title,
#      `_regions_supp` opens the region at the unmistakable "Locations Covered"
#      COLUMN HEADER — the one marker unique to armour tables — and skips over the
#      header block so a typo'd header ("Availabiity") cannot bleed into a name.
#   2. Column ORDER varies (DH puts Wt before Cost; the Inquisitor's War-Zone
#      table swaps them; Rogue Trader/Only War carry no Cost; Deathwatch grades by
#      Req/Renown). `_forward_fields_supp` assigns the trailing cells BY TYPE
#      (kg-cell→weight, integer→cost, rarity→availability) rather than by fixed
#      position, so the swap parses correctly.
#   3. AP is sometimes a conditional ("3 (6)", "5 (4 on Head)"), names run long
#      ("Cadian-pattern 'Kasrkin' Storm Trooper Carapace", 47 chars), and OCR
#      spills a stray leading letter ("p Mantle of the Fallen Wolf"). Relaxed
#      AP/name predicates and a per-row sanitiser cover these.
#   4. A few rows are space-fused onto one line ("Magma Suit All", "90kg Near
#      Unique"). `_defuse_supp_armour_line` re-splits ONLY at two unambiguous
#      seams (a trailing whole-body "All"; a "<kg> <Rarity>" pair).
# Dash-AP rows (force fields / upgrades: Refractor Field, Rosarius, Ecclesiarchy
# Overlay) and non-location rows ("See Text") are NOT recovered here — they belong
# to the gear/force-field indices — so the supplement armour index stays clean.
# ---------------------------------------------------------------------------

# A table title, tolerant of a leading "<Htable>"-style tag.
def _is_table_title(ln: str) -> bool:
    return bool(RE_TBL_ANY.match(re.sub(r"^\s*<[^>]+>\s*", "", ln)))


# The armour column-header row, in any of its OCR shapes: "Location(s) Covered",
# "Locations Covered", the fused "Locations Covered AP", or the wrapped "Locations"
# followed by "Covered" on the next line.
RE_LOC_HDR_LINE = re.compile(
    r"^\s*(?:name\s+)?location(?:\(s\)|s)?\s+covered\b", re.IGNORECASE)
RE_LOC_HDR_WRAP = re.compile(r"^\s*location(?:\(s\)|s)?\s*$", re.IGNORECASE)
RE_COVERED = re.compile(r"^\s*covered\b", re.IGNORECASE)

# Column-header tokens (armour tables). A header-block line is a run of these; the
# "avail" prefix rule absorbs OCR typos like "Availabiity"/"Availabilty".
_HDR_TOKENS = {"name", "armour", "type", "location", "locations", "covered",
               "ap", "wt", "wt.", "weight", "kg", "cost", "req", "renown"}
# A foreign column header that means a DIFFERENT table has begun (force fields /
# upgrades / weapons) — closes an open armour region as a safety belt.
_FOREIGN_HDR = {"protection rating", "upgrade type", "class", "damage", "rof"}


def _is_header_line(ln: str) -> bool:
    low = re.sub(r"[^a-z().\s]", "", ln.strip().lower())
    low = low.replace("(s)", "s")
    words = low.split()
    if not words:
        return False
    def _hword(w: str) -> bool:
        return w in _HDR_TOKENS or w.startswith("avail")
    return all(_hword(w) for w in words)


def _is_foreign_header(ln: str) -> bool:
    low = re.sub(r"\s+", " ", ln.strip().lower())
    return low in _FOREIGN_HDR


def _loc_header_here(lines: List[str], i: int) -> bool:
    s = lines[i].strip()
    if RE_LOC_HDR_LINE.match(s):
        return True
    if RE_LOC_HDR_WRAP.match(s):                   # wrapped: confirm next is "Covered"
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines) and RE_COVERED.match(lines[j].strip()):
            return True
    return False


def _regions_supp(lines: List[str]) -> List[bool]:
    """Open the armour region at a Locations-Covered header (skipping its header
    block); close it at the next table title or a foreign-table header."""
    inside = [False] * len(lines)
    open_ = False
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]
        if _is_table_title(ln) or _is_foreign_header(ln):
            open_ = False
            inside[i] = False
            i += 1
            continue
        if not open_ and _loc_header_here(lines, i):
            j = i                                  # consume the header block
            while j < n and (not lines[j].strip() or _is_header_line(lines[j])):
                inside[j] = False
                j += 1
            open_ = True
            i = j
            continue
        inside[i] = open_
        i += 1
    return inside


# Two unambiguous space-fusion seams (see note 4). Anchored so a clean data line
# is never touched: only a name that ENDS in a lone whole-body "All", and a
# "<number>kg <Rarity>" pair, are split.
_SUPP_RARITY_ALT = (r"Ubiquitous|Abundant|Plentiful|Common|Average|Scarce|"
                    r"Very Rare|Extremely Rare|Ext\.\s*Rare|Near[ \-]?Unique|"
                    r"Unique|Rare")
_RE_FUSE_WT_RARITY = re.compile(
    rf"(\b\d{{1,3}}(?:\.\d{{1,2}})?\s*kg\.?)\s+(?=(?:{_SUPP_RARITY_ALT})\b)",
    re.IGNORECASE)
_RE_FUSE_NAME_ALL = re.compile(r"^([A-Z][A-Za-z'’\-][A-Za-z'’\- ]{1,40}?)\s+(All)\s*$")


def _defuse_supp_armour_line(ln: str) -> str:
    s = _RE_FUSE_WT_RARITY.sub("\\1\t", ln)
    s = _RE_FUSE_NAME_ALL.sub("\\1\t\\2", s)
    return s


def _build_cells_supp(lines: List[str], pages: List[int], region: List[bool]) -> List[Cell]:
    cells: List[Cell] = []
    for i, ln in enumerate(lines):
        if PAGE.search(ln):
            continue
        src = _defuse_supp_armour_line(ln) if region[i] else ln
        for piece in src.split("\t"):
            s = piece.strip()
            if s:
                cells.append(Cell(s, i, pages[i], region[i]))
    return cells


# AP in a supplement may be a conditional ("3 (6)", "5 (4 on Head)") on top of the
# core forms (plain int, "8/10", "Varies"), and often carries a trailing footnote
# dagger ("8†" — Tome of Blood's Mantle of Hate). The dagger is stripped for the
# stat; the conditional is kept raw. A pure-dagger AP ("††", variable-by-
# Corruption) is not a number and stays skipped.
RE_AP_PAREN = re.compile(r"^\d{1,2}\s*\([^)]{1,24}\)$")


def _ap_strip(t: str) -> str:
    return t.strip().rstrip("†‡*").strip()


def _is_ap_cell_supp(t: str) -> bool:
    t = _ap_strip(t)
    return _is_ap_cell(t) or bool(RE_AP_PAREN.match(t))


def _parse_ap_supp(t: str):
    t = _ap_strip(t)
    if RE_AP_PAREN.match(t):
        return re.sub(r"\s+", " ", t)
    return _parse_ap(t)


def _is_prose_supp(t: str) -> bool:
    t = t.strip()
    return len(t) > 62 or t.count(" ") > 9        # looser cap for long armour names


def _plausible_name_supp(s: str) -> bool:
    s = _clean_name(s)
    if not (2 <= len(s) <= 62):
        return False
    if not s[0].isalnum():
        return False
    low = s.lower()
    if low in HEADER_WORDS or low in RARITIES or _is_location(s):
        return False
    return sum(c.isalpha() for c in s) >= 2


_RE_WT_KG = re.compile(r"^\+?\d{1,3}(?:\.\d{1,2})?\s*kg\.?$", re.IGNORECASE)
_RE_COST = re.compile(r"^\+?[\d,]{1,7}$")


def _rarity_norm(t: str) -> Optional[str]:
    """The book's raw rarity string if the cell is a rarity (hyphen/dagger and
    two-word tolerant), else None."""
    base = t.strip().rstrip("\u2020\u2021*").strip()
    low = re.sub(r"\s+", " ", base.lower().replace("-", " ")).strip()
    return base if low in RARITIES else None


def _forward_fields_supp(cells: List[Cell], p: int, schema: str) -> dict:
    """Assign the trailing cells after the AP anchor BY TYPE, so a book's column
    order (and the odd Cost/Wt swap) does not matter. Nothing is invented — a cell
    that fits no column is dropped, not guessed."""
    n = len(cells)
    nxt: List[str] = []
    q = p + 1
    while q < n and cells[q].region and len(nxt) < 5:
        nxt.append(cells[q].text)
        q += 1
    toks = [t.strip() for t in nxt if t.strip()]
    out: dict = {}
    if not toks:
        return out

    if schema == "req_renown":                    # Deathwatch: Wt, Req, Renown
        wt = _weight_token(toks[0])
        if wt:
            out["weight"] = wt
        if len(toks) > 1 and toks[1]:
            out["req"] = toks[1].strip()
        if len(toks) > 2 and toks[2]:
            out["renown"] = toks[2].strip()
        return out

    look = toks[:4]
    used = [False] * len(look)

    for i, t in enumerate(look):                  # Weight: the kg-suffixed cell…
        if _RE_WT_KG.match(t):
            out["weight"] = _weight_token(t)
            used[i] = True
            break
    if "weight" not in out and schema == "avail":  # …or a bare number when no Cost
        for i, t in enumerate(look):
            if not used[i] and RE_WT_PURE.match(t):
                out["weight"] = _weight_token(t)
                used[i] = True
                break

    for i in range(len(look)):                     # Availability: a rarity cell
        if used[i]:
            continue
        if i + 1 < len(look) and not used[i + 1]:
            r2 = _rarity_norm(look[i] + " " + look[i + 1])
            if r2:
                out["availability"] = r2
                used[i] = used[i + 1] = True
                break
        r1 = _rarity_norm(look[i])
        if r1:
            out["availability"] = r1
            used[i] = True
            break

    if schema == "cost_avail":                     # Cost: an integer / +N / "Special"
        for i, t in enumerate(look):
            if used[i]:
                continue
            if _RE_COST.match(t) or t.lower() == "special":
                out["cost"] = t
                used[i] = True
                break
    return out


_NAME_LEAD_NOISE = re.compile(r"^(?:[a-z]\s+)+")   # OCR spill: a lone leading letter
# Value words that can spill from the PREVIOUS row's trailing cells onto the front
# of a name (e.g. the Radical's Handbook 'Holo-Armour' whose Cost/Availability are
# both "Special" bled into "Special Special Mecronid Armour"). A real armour name
# never begins with a rarity word or these placeholders, so a leading run of them
# is stripped. Never touches "Armour"/body words — only pure value tokens.
_NAME_LEAD_DROP = ({w for r in RARITIES for w in re.split(r"[ .]+", r) if w} |
                   {"special", "see", "text", "as", "upgraded", "varies", "na"})


def _sanitize_supp_armour(a: Armour) -> Optional[Armour]:
    """Scrub a supplement row; return None to reject it. Never invents a value."""
    toks = _NAME_LEAD_NOISE.sub("", a.name).split()
    i = 0
    while i < len(toks):
        w = toks[i].lower().strip(",").strip("†‡*").strip()
        if w in _NAME_LEAD_DROP:
            i += 1
            continue
        break
    stripped = _clean_name(" ".join(toks[i:]))
    a.name = stripped or _clean_name(a.name)
    if not _plausible_name_supp(a.name):
        return None
    if a.req is not None and not a.req.strip():
        a.req = None
    if a.renown is not None and not a.renown.strip():
        a.renown = None
    return a


def detect_armour_supp(lines: List[str], pages: List[int], book: str,
                       schema: str = "avail", allow_scramble: bool = False) -> List[Armour]:
    """SUPPLEMENT detector — armour-bearing splatbooks. Same anchor pipeline, with
    the supplement region rule and the relaxed/typed overrides."""
    region = _regions_supp(lines)
    cells = _build_cells_supp(lines, pages, region)
    cat_at = _categories_by_index(cells)
    return _detect_armour_from_cells(
        cells, cat_at, book, schema, allow_scramble=False,
        forward_fn=_forward_fields_supp, ap_ok=_is_ap_cell_supp,
        ap_parse=_parse_ap_supp, name_ok=_plausible_name_supp,
        prose_fn=_is_prose_supp, do_dashap=False,
        sanitize_fn=_sanitize_supp_armour)


DETECTORS: Dict[str, Callable[..., List[Armour]]] = {
    "core": detect_armour,
    "supp": detect_armour_supp,
}


@dataclass
class Source:
    key: str
    book: str
    path: Path
    citation: str
    schema: str
    allow_scramble: bool = False
    detector: str = "core"
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

    # --- SUPPLEMENTS (added later; the "supp" detector; rows carry their own PDF
    #     page). Additive only — the five cores above are untouched. ------------
    # Dark Heresy line
    Source("dh-inquisitor", "Dark Heresy — The Inquisitor's Handbook",
           _40K / "Dark Heresy/Rulebooks/Dark Heresy - The Inquisitor's Handbook.md",
           "Dark Heresy: The Inquisitor's Handbook (FFG, WH40K Roleplay), Armoury "
           "(world-type armour tables)", "cost_avail", False, "supp"),
    Source("dh-radicals", "Dark Heresy — The Radical's Handbook",
           _40K / "Dark Heresy/Rulebooks/Dark Heresy - The Radical's Handbook.md",
           "Dark Heresy: The Radical's Handbook (FFG, WH40K Roleplay), Armoury, "
           "Table 4-6: Armour & Table 6-2: Xenos Armour", "cost_avail", False, "supp"),
    Source("dh-ascension", "Dark Heresy — Ascension",
           _40K / "Dark Heresy/Rulebooks/Dark Heresy - Ascension.md",
           "Dark Heresy: Ascension (FFG, WH40K Roleplay), Armoury, "
           "Table 6-3: Armour", "avail", False, "supp"),
    Source("dh-blood", "Dark Heresy — Blood of Martyrs",
           _40K / "Dark Heresy/Rulebooks/Dark Heresy - Blood of Martyrs.md",
           "Dark Heresy: Blood of Martyrs (FFG, WH40K Roleplay), Armoury, "
           "Table 5-3: Ecclesiarchal Armour", "cost_avail", False, "supp"),
    # Rogue Trader line
    # NOTE: Rogue Trader — Into the Storm is SKIPPED. Its main armour table
    # (Table 3-8: Armour) is character-shattered OCR (rows are glyph soup), and
    # the secondary Ork/Kroot armouries (Table 3-20 et al.) use a split
    # "non-Kroot/Kroot" Availability format ("Very Rare/Scarce") with OCR-mangled
    # names ("'Eavy Armor") and locations ("Body. Arms, legs") — not bankable
    # cleanly, so it is left out rather than emit polluted rows.
    Source("rt-hostile", "Rogue Trader — Hostile Acquisitions",
           _40K / "Rogue Trader/Rulebooks/Rogue Trader - Hostile Acquisitions.md",
           "Rogue Trader: Hostile Acquisitions (FFG, WH40K Roleplay), Armoury, "
           "Table 2-16: Armour", "avail", False, "supp"),
    # Deathwatch line  (armoury grades by Req/Renown, not Cost/Availability)
    Source("dw-founding", "Deathwatch — First Founding",
           _40K / "Deathwatch/Rulebooks/Deathwatch - First Founding.md",
           "Deathwatch: First Founding (FFG, WH40K Roleplay), Armoury, "
           "Table 4-3: Armour", "req_renown", False, "supp"),
    Source("dw-honour", "Deathwatch — Honour the Chapter",
           _40K / "Deathwatch/Rulebooks/Deathwatch - Honour the Chapter.md",
           "Deathwatch: Honour the Chapter (FFG, WH40K Roleplay), Armoury", "req_renown",
           False, "supp"),
    Source("dw-rites", "Deathwatch — Rites of Battle",
           _40K / "Deathwatch/Rulebooks/Deathwatch - Rites of Battle.md",
           "Deathwatch: Rites of Battle (FFG, WH40K Roleplay), Armoury", "req_renown",
           False, "supp"),
    # Only War line
    Source("ow-hammer", "Only War — Hammer of the Emperor",
           _40K / "Only War/Rulebooks/Only War - Hammer of The Emperor.md",
           "Only War: Hammer of the Emperor (FFG, WH40K Roleplay), Armoury", "avail",
           False, "supp"),
    # Black Crusade line
    Source("bc-blood", "Black Crusade — Tome of Blood",
           _40K / "Black Crusade/Rulebooks/Black Crusade - Tome of Blood.md",
           "Black Crusade: Tome of Blood (FFG, WH40K Roleplay), Armoury", "avail",
           False, "supp"),
    Source("bc-excess", "Black Crusade — Tome of Excess",
           _40K / "Black Crusade/Rulebooks/Black Crusade - Tome of Excess.md",
           "Black Crusade: Tome of Excess (FFG, WH40K Roleplay), Armoury", "avail",
           False, "supp"),
    Source("bc-fate", "Black Crusade — Tome of Fate",
           _40K / "Black Crusade/Rulebooks/Black Crusade - Tome of Fate.md",
           "Black Crusade: Tome of Fate (FFG, WH40K Roleplay), Armoury, "
           "Table 2-3: Protective Devices", "avail", False, "supp"),
]


def _fresh_sources() -> List[Source]:
    return [Source(s.key, s.book, s.path, s.citation, s.schema, s.allow_scramble,
                   s.detector)
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
            src.armour = DETECTORS[src.detector](src.lines, pages, src.book,
                                                 src.schema, src.allow_scramble)
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
        "OCR-scrambled block — verify against the book. Coverage is the five core",
        "rulebooks PLUS the armour-bearing supplements (Inquisitor's/Radical's",
        "Handbooks, Ascension, Blood of Martyrs, Hostile Acquisitions, First",
        "Founding, Tome of Blood/Fate); force fields, upgrades and armour whose AP",
        "the source leaves variable are left to their own indices. Use",
        "`--export \"NAME\"` for the translator packet.",
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


# --- supplement fixtures (the "supp" detector) ------------------------------
# cost_avail: an <Htable>-tagged title with "Armour" mid-name; the region opens on
# the Locations-Covered header and SKIPS the header block so the typo'd
# "Availabiity" cannot bleed into the first name; a conditional AP "3 (6)"; a
# "Special/Special" cost/avail whose words must NOT prefix the next name; and the
# War-Zone table's Cost/Wt column SWAP.
SUPP_FIXTURE_CA = """## [PDF page 300]
<Htable>Table 3-3: Feral And Feudal (Primitive) Armour
Armour
Location(s) Covered
AP
Wt
Cost
Availabiity
Banded Armour
Arms, Body, Legs
3
12kg
50
Rare
Volcanis Shroud
Head, Arms, Body, Legs
3 (6)
20kg
350
Average
Holo-Armour
All
4
4 kg
Special
Special
Mecronid Armour
All
7
2 kg
15,000
Very Rare
Table 6-5: War Zone Protective Gear
Armour Type
Location(s) Covered
AP
Cost
Wt
Availability
Carapace Armour
Windrider Carapace
Body
6
800
6kg
Scarce
Table 9-9: Gear
Name
"""

# req_renown: a leading lone-letter OCR spill ("p") before a name must be
# stripped; AP is a legitimate 0.
SUPP_FIXTURE_RR = """## [PDF page 301]
Table 4-3: Wolf Armour
Name
Locations Covered
AP
Wt
Req
Renown
Great Wolf Pelt
Body
0
2kg
10
Respected
p
Mantle of the Fallen Wolf
Body
0
2kg
20
Distinguished
Table 4-4: Relics
Name
"""

# avail: a name longer than the core 45-char cap; a footnote-dagger AP ("8\u2020");
# a space-fused "Magma Suit All" name+location and "90kg Near Unique" weight+avail
# (the de-fuser); and a following Force-Field table that must yield NO armour.
SUPP_FIXTURE_AV = """## [PDF page 302]
Table 6-3: Ascended Armour
Name
Location(s) Covered
AP
Wt
Availability
Cadian-pattern Kasrkin Storm Trooper Carapace Mk7
All
6
15 kg
Very Rare
Table 2-3: Protective Devices
Armour
Name
Locations Covered
AP Wt
Availability
Mantle of Hate
All
8\u2020
150kg
Near Unique
Magma Suit All
9
90kg Near Unique
Force Field
Name
Protection Rating
Wt
Availability
Prismatic Amulet
60
3kg
Near Unique
Table 9-9: Ammo
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

    # --- SUPPLEMENT fixtures: the "supp" detector ------------------------
    ls = SUPP_FIXTURE_CA.splitlines()
    ca = detect_armour_supp(ls, _pages_for(ls), "Fixture Supp CA", "cost_avail")
    names = [a.name for a in ca]
    want = ["Banded Armour", "Volcanis Shroud", "Holo-Armour", "Mecronid Armour",
            "Windrider Carapace"]
    if names != want:
        failures.append(f"supp CA names {names}, wanted {want}")
    else:
        by = {a.name: a for a in ca}
        bd = by["Banded Armour"]                 # header block must not bleed in
        got = (bd.locations, bd.armour_points, bd.weight, bd.cost, bd.availability,
               bd.system)
        exp = ("Arms, Body, Legs", 3, "12kg", "50", "Rare", SYSTEM)
        if got != exp:
            failures.append(f"supp Banded Armour {got}, wanted {exp}")
        vs = by["Volcanis Shroud"]               # conditional AP kept as a string
        if vs.armour_points != "3 (6)":
            failures.append(f"supp Volcanis AP {vs.armour_points!r}, wanted '3 (6)'")
        mec = by["Mecronid Armour"]              # 'Special Special' must not prefix
        if mec.name != "Mecronid Armour" or mec.cost != "15,000":
            failures.append(f"supp Mecronid leaked: name={mec.name!r} cost={mec.cost!r}")
        wc = by["Windrider Carapace"]            # War-Zone Cost/Wt column swap
        got = (wc.category, wc.armour_points, wc.weight, wc.cost, wc.availability)
        exp = ("Carapace Armour", 6, "6kg", "800", "Scarce")
        if got != exp:
            failures.append(f"supp Windrider (Cost/Wt swap?) {got}, wanted {exp}")

    ls = SUPP_FIXTURE_RR.splitlines()
    rr = detect_armour_supp(ls, _pages_for(ls), "Fixture Supp RR", "req_renown")
    names = [a.name for a in rr]
    if names != ["Great Wolf Pelt", "Mantle of the Fallen Wolf"]:
        failures.append(f"supp RR names {names}")
    else:
        by = {a.name: a for a in rr}
        gw = by["Great Wolf Pelt"]
        got = (gw.armour_points, gw.weight, gw.req, gw.renown, gw.cost, gw.availability)
        if got != (0, "2kg", "10", "Respected", None, None):
            failures.append(f"supp Great Wolf Pelt {got}")
        mf = by["Mantle of the Fallen Wolf"]     # leading lone-letter noise stripped
        if mf.name != "Mantle of the Fallen Wolf" or mf.renown != "Distinguished":
            failures.append(f"supp Mantle noise/renown {mf.name!r},{mf.renown!r}")

    ls = SUPP_FIXTURE_AV.splitlines()
    av = detect_armour_supp(ls, _pages_for(ls), "Fixture Supp AV", "avail")
    names = [a.name for a in av]
    want = ["Cadian-pattern Kasrkin Storm Trooper Carapace Mk7", "Mantle of Hate",
            "Magma Suit"]
    if names != want:
        failures.append(f"supp AV names {names}, wanted {want} (force field leaked?)")
    else:
        by = {a.name: a for a in av}
        cad = by["Cadian-pattern Kasrkin Storm Trooper Carapace Mk7"]
        if len(cad.name) <= 45:                  # proves the relaxed name-length cap
            failures.append("supp AV long-name fixture is not actually > 45 chars")
        got = (cad.locations, cad.armour_points, cad.weight, cad.availability)
        if got != ("All", 6, "15 kg", "Very Rare"):
            failures.append(f"supp Cadian long name {got}")
        mh = by["Mantle of Hate"]                # footnote-dagger AP -> int 8
        got = (mh.armour_points, mh.weight, mh.availability)
        if got != (8, "150kg", "Near Unique"):
            failures.append(f"supp Mantle of Hate (dagger AP?) {got}")
        ms = by["Magma Suit"]                    # de-fused name+loc and weight+avail
        got = (ms.locations, ms.armour_points, ms.weight, ms.availability)
        if got != ("All", 9, "90kg", "Near Unique"):
            failures.append(f"supp Magma Suit (de-fuse?) {got}")

    # --- no phantom rows from prose ---
    stray = detect_armour("The suit grants 6 Armour Points to All locations.".splitlines(),
                          [0], "Prose", "avail")
    if stray:
        failures.append(f"prose produced phantom armour: {[a.name for a in stray]}")

    # --- live corpus invariants ---
    if base.is_dir() and any((base / s.path).exists() for s in SOURCES):
        corpus = Corpus(base, _fresh_sources())
        by_key = {s.key: s for s in corpus.sources}
        # HARD CONSTRAINT: the five cores stay EXACT (28/20/9/17/28 = 102).
        core_expect = {"dh-core": 28, "rt-core": 20, "dw-core": 9, "ow-core": 17,
                       "bc-core": 28}
        core_total = 0
        for key, exp_n in core_expect.items():
            src = by_key.get(key)
            if src is None or not (base / src.path).exists():
                continue
            core_total += len(src.armour)
            if len(src.armour) != exp_n:
                failures.append(f"CORE PRESERVATION: {key} yielded "
                                f"{len(src.armour)} armour; must be exactly {exp_n}")
        if core_total and core_total != 102:
            failures.append(f"CORE PRESERVATION: cores total {core_total}, must be 102")
        supp_total = sum(len(s.armour) for s in corpus.sources
                         if s.key not in core_expect)
        if core_total == 102 and supp_total < 30:
            failures.append(f"only {supp_total} supplement armour harvested; "
                            f"expected the splatbooks to add 30+")
        for known in ("Flak Vest", "Carapace Helm", "Storm Trooper Carapace"):
            if not corpus.find(known):
                failures.append(f"known armour not found in live corpus: {known}")
        # a specific SUPPLEMENT row, harvested live, parses (name + AP + locations)
        hits = corpus.find("Great Wolf Pelt")
        if not hits:
            failures.append("supplement armour 'Great Wolf Pelt' not found live")
        else:
            gw = hits[0][1]
            if (gw.armour_points, gw.locations, "First Founding" in gw.book) != \
                    (0, "Body", True):
                failures.append(f"live Great Wolf Pelt parsed "
                                f"{(gw.armour_points, gw.locations, gw.book)!r}")
        hits = corpus.find("Banded Armour")      # Inquisitor's Handbook world-armour table
        if not hits:
            failures.append("supplement armour 'Banded Armour' not found live")
        elif (hits[0][1].armour_points, hits[0][1].locations) != (3, "Arms, Body, Legs"):
            failures.append(f"live Banded Armour parsed "
                            f"{(hits[0][1].armour_points, hits[0][1].locations)!r}")
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
        # AP integers must be sane (0..20); strings only "8/10"/"N (…)"/"Varies"
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
