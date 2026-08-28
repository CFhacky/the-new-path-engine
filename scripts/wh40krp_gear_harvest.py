#!/usr/bin/env python3
"""wh40krp_gear_harvest.py — collate WH40K Roleplay GEAR (system: WH40K Roleplay).

THE PROCESS (the 40K shelf): other GAME SYSTEMS are welcome in the reference
layer AS LONG AS each is clearly LABELLED by system — the translator tools turn
them into the hybrid's 3.5e + GURPS. This is the **Warhammer 40,000 Roleplay**
(Fantasy Flight Games d100) GEAR index — the NON-weapon, NON-armour equipment of
Dark Heresy / Rogue Trader / Deathwatch / Only War / Black Crusade — kept apart
from the weapon and armour indices and stamped `"system": "WH40K Roleplay"`.

    reference/wh40krp_gear_index.json — every gear item: name, category, weight,
                                        cost, availability, book + PDF page.
    reference/wh40krp_gear_index.md   — the same, for human eyes.

`--export` emits a translator-ready packet (a 40K RP gear item the system-
translator skill converts to the 3.5e + GURPS pair).

WORKFLOW
    python wh40krp_gear_harvest.py                     # (re)build the index
    python wh40krp_gear_harvest.py --search "medikit"  # find candidates
    python wh40krp_gear_harvest.py --export "Auspex/Scanner"
    python wh40krp_gear_harvest.py --selftest

GOVERNING SOURCES
    I:\\Sourcebooks\\_text\\Warhammer\\40K Roleplay\\ — the five core rulebooks.
    Each book's Armoury chapter carries several small "Gear" tables — General
    Equipment / Clothing, Drugs & Consumables, Tools, Cybernetics, and (Black
    Crusade) Wargear.  They were OCR'd as a VERTICAL COLUMN-DUMP: each row is a
    run of cells, one per line, in a fixed column order that VARIES by book:
        Dark Heresy : Name, Wt(kg), Cost, Availability   (Cybernetics: no Wt)
        Rogue Trader: Name, Wt,     Availability          (Cybernetics: Name+Avail)
        Only War    : Name, Wt(kg), Availability          (Cybernetics: Name+Avail)
        Black Crus. : Name, Wt(kg), Availability          (Cybernetics: Name+Avail)
        Deathwatch  : Name, Wt,     Req, Renown           (Cybernetics: no Wt)
    Rogue Trader / Only War / Black Crusade acquire gear by Availability (no
    Throne cost).  Deathwatch grades acquisition by Requisition + Renown, not
    Cost/Availability; its Req is stored in `cost` and its Renown in
    `availability` (a "\u2013" Renown means no rank is required, stored empty).

    The parser detects each gear table by its heading, reads the column HEADER
    row to learn that table's template, then reads rows FORWARD from each item
    name: the trailing cells (weight/cost) are typed and the row terminates on an
    Availability rarity (Common/Scarce/Rare/Very Rare/... or "Adeptus Mechanicus
    Only") or, for Deathwatch, on the Renown cell.  Prose blurbs between the stat
    table and the next table never emit — a row is banked only when a clean
    terminal (rarity/renown) is found right after typed stat cells.  Weapons and
    armour are left to their sibling indices (a stray explosive such as a
    melta-bomb listed under Wargear is filtered out).  A configured source whose
    file is missing prints NO COVERAGE.  Book RAW only — every value is the
    book's, cited to book + PDF page; an unrecoverable cell is left empty and the
    row noted in `soft`; nothing is invented.  (Item effects live in multi-
    paragraph blurbs beside the tables and are deliberately NOT extracted, to
    avoid summarising prose into the mechanical line.)
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
OUT_JSON = REPO / "reference" / "wh40krp_gear_index.json"
OUT_MD = REPO / "reference" / "wh40krp_gear_index.md"
SYSTEM = "WH40K Roleplay"
PROGRESS = Path(
    r"C:\Users\Chad\AppData\Local\Temp\claude"
    r"\I--repos-the-new-path-engine--claude-worktrees-intelligent-lamport-3a158a"
    r"\1c5f36b4-d94a-4698-95d9-c2304f8a0818\scratchpad\wh40krp_gear_progress.json")

PAGE = re.compile(r"\[PDF page (\d+)\]")
RE_TBL_ANY = re.compile(r"^\s*Table\s+\S", re.IGNORECASE)

DASHES = "\u2013\u2014-"
RE_DASH = re.compile(rf"^[{DASHES}]+$")

# A weight cell: "0.5", "1", "25", "0.5 kg", "2 kg", "2kg", or the garbled "2 k".
LOOSE_WEIGHT = re.compile(r"^\d{1,4}(?:\.\d{1,2})?\s*k?g?\.?$", re.IGNORECASE)
# A cost cell: an integer (optionally grouped with commas) or the literal "Var".
RE_COST = re.compile(r"^(?:\d{1,3}(?:,\d{3})+|\d{1,6}|[Vv]ar\.?)$")
# A bare Deathwatch stat number (Wt / Req).
RE_DW_NUM = re.compile(r"^\d{1,4}$")

# Availability rarity ladder (a closed set) — the terminal cell of a gear row.
RARITIES = {
    "ubiquitous", "abundant", "plentiful", "common", "average", "scarce",
    "rare", "very rare", "extremely rare", "near unique", "unique",
}
# Deathwatch Renown ranks (its acquisition gate, stored in `availability`).
RENOWN_RANKS = {"respected", "distinguished", "famed", "hero"}

# Column-header tokens (used to auto-detect a table's template and skip its
# header row).  A cell whose every token is one of these is a header cell.
HEADER_TOKENS = {
    "name", "type", "wt", "wt.", "weight", "kg", "cost", "req", "req.",
    "requisition", "renown", "availability", "avail", "effect",
}

# Explosives/weapons that can appear inside a Wargear/Tools gear table but belong
# to the weapon index — filtered so they do not bleed through.
WEAPON_BLEED = re.compile(r"\b(?:grenade|missile|melta[\s\-]?bomb|warhead)\b",
                          re.IGNORECASE)
# Armour-line words that must never appear as a gear name (bleed guard for the
# armour index).  Worn items the books themselves file under Clothing/Gear
# (Synskin, Void Suit, Survival Suit) are legitimately gear and are NOT blocked.
ARMOUR_BLEED = re.compile(
    r"\b(?:flak armour|carapace|ceramite|power armour|mesh armour|"
    r"xenos hide|enforcer light)\b", re.IGNORECASE)


def _norm_name(s: str) -> str:
    s = s.replace("\ufb01", "fi").replace("\ufb02", "fl")   # OCR ligatures
    s = re.sub(r"\s+", " ", s).strip()
    s = s.strip(" ,\u2020*\u2013\u2014-").strip()
    return s


def _avnorm(s: str) -> str:
    """Normalise an availability/renown cell: drop footnote marks, lower-case."""
    return re.sub(r"\s+", " ", s).strip().strip("\u2020*.,\u2013\u2014- ").lower()


def _is_weight_strict(c: str) -> bool:
    c = c.strip()
    return bool(re.search(r"kg", c, re.IGNORECASE)) or bool(re.match(r"^\d+\.\d+$", c))


def _is_cost_strict(c: str) -> bool:
    return bool(RE_COST.match(c.strip()))


def _is_stat_like(c: str) -> bool:
    c = c.strip()
    if not c:
        return False
    return bool(RE_DASH.match(c) or LOOSE_WEIGHT.match(c) or _is_cost_strict(c))


def _plausible_name(s: str) -> bool:
    s = s.strip()
    if not (2 <= len(s) <= 60):
        return False
    if not s[0].isalpha():
        return False
    low = _avnorm(s)
    if low in HEADER_TOKENS or low in RARITIES or low in RENOWN_RANKS or low == "var":
        return False
    if low.startswith("adeptus mechanicus"):
        return False
    if sum(c.isalpha() for c in s) < 2:
        return False
    if WEAPON_BLEED.search(s) or ARMOUR_BLEED.search(s):
        return False
    return True


_STOPWORDS = {
    "the", "and", "for", "you", "your", "his", "her", "are", "was", "with",
    "that", "this", "not", "use", "can", "may", "of", "to", "in", "on", "a",
    "an", "is", "he", "it", "as", "at", "by", "or", "be", "but", "they", "their",
    "them", "if", "from", "will", "have", "has", "all", "one", "who", "which",
    "when", "does", "into", "only", "over", "than", "then", "so", "no",
}


def _item_like(s: str) -> bool:
    """A conservative gate for the `soft` list: does this string plausibly name a
    gear item (rather than a prose sentence fragment)?  Keeps `soft` honest."""
    s = s.strip()
    if re.search(r'[.!?,;:"]$', s):
        return False
    words = s.split()
    if not (1 <= len(words) <= 5) or not s[0].isupper():
        return False
    if any(w.strip(",.").lower() in _STOPWORDS for w in words):
        return False
    return True


def _is_name_start(c: str) -> bool:
    c = c.strip()
    if not c or not c[0].isalpha():
        return False
    low = _avnorm(c)
    if low in HEADER_TOKENS or low in RARITIES or low in RENOWN_RANKS or low == "var":
        return False
    if low.startswith("adeptus"):       # availability phrase, not a name
        return False
    if low in ("mechanicus only", "mechanicus", "only"):
        return False
    return True


def _match_availability(cells: List["Cell"], i: int) -> Optional[Tuple[str, int]]:
    """If a gear row's Availability terminal begins at cells[i], return
    (value, cells_consumed); else None.  Handles the single-cell rarity ladder
    and the multi-cell 'Adeptus Mechanicus Only' restricted phrase."""
    n = len(cells)
    low = _avnorm(cells[i].text)
    if low in RARITIES:
        return low.title(), 1
    if low.startswith("adeptus"):
        if "only" in low:
            return "Adeptus Mechanicus Only", 1
        j = i
        while j + 1 < n and j - i < 2:
            j += 1
            if "only" in cells[j].text.lower():
                return "Adeptus Mechanicus Only", j - i + 1
        return None
    return None


@dataclass
class Gear:
    name: str
    category: str
    book: str
    page: Optional[int]
    line: int
    system: str = SYSTEM
    weight: Optional[str] = None
    cost: Optional[str] = None
    availability: Optional[str] = None

    def quick_fields(self) -> int:
        return sum(1 for v in (self.weight, self.cost, self.availability) if v)


@dataclass
class Cell:
    text: str
    line: int
    page: int


@dataclass
class Region:
    category: str
    template: dict          # {'has_weight':bool,'has_cost':bool,'terminal':str}
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


def _norm_title(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def _build_cells(line_idxs: List[int], lines: List[str], pages: List[int]) -> List[Cell]:
    cells: List[Cell] = []
    for i in line_idxs:
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
    (template, data_cells) with the header stripped."""
    has_weight = has_cost = False
    terminal: Optional[str] = None
    k = 0
    while k < len(cells):
        toks = _avnorm(cells[k].text).split()
        if toks and all(t in HEADER_TOKENS for t in toks):
            for t in toks:
                if t in ("wt", "wt.", "weight", "kg"):
                    has_weight = True
                if t in ("cost", "req", "req.", "requisition"):
                    has_cost = True
                if t == "renown":
                    terminal = "renown"
                if t in ("availability", "avail") and terminal is None:
                    terminal = "avail"
            k += 1
        else:
            break
    return ({"has_weight": has_weight, "has_cost": has_cost,
             "terminal": terminal or "avail"}, cells[k:])


def _regions(lines: List[str], pages: List[int], gear_titles: Dict[str, str]) -> List[Region]:
    regions: List[Region] = []
    i, n = 0, len(lines)
    while i < n:
        if RE_TBL_ANY.match(lines[i]) and ":" in lines[i]:
            title = _norm_title(lines[i].split(":", 1)[1])
            cat = gear_titles.get(title)
            if cat:
                j = i + 1
                buf: List[int] = []
                while j < n and not RE_TBL_ANY.match(lines[j]):
                    buf.append(j)
                    j += 1
                template, data = _detect_template(_build_cells(buf, lines, pages))
                regions.append(Region(cat, template, data))
                i = j
                continue
        i += 1
    return regions


def _read_name(cells: List[Cell], i: int, tmpl: dict) -> Tuple[str, int, dict]:
    """Read an item name starting at cells[i]; return (name, next_i, prefill).
    A stat fused onto the name line is peeled off so it does not pollute the name:
    a Deathwatch bare number ('Astartes Psychic Hood 15', 'Bionic Locomotion 15')
    or a kg-suffixed weight ('Rendering Apothecarium 20 kg').  The peeled value is
    assigned to the FIRST stat column the table actually has — weight if present,
    otherwise cost — so Deathwatch's Cybernetics (Name|Req|Renown, no weight) reads
    the fused number as its Requisition, not as a weight."""
    n = len(cells)
    text = cells[i].text
    i += 1
    prefill: dict = {}
    if tmpl["terminal"] == "renown":
        m = re.match(r"^(.*[^\d\s])\s+(\d{1,4})$", text)
        peeled = m.group(2) if m else None
    else:
        m = re.match(r"^(.*[^\d\s])\s+(\d{1,4}(?:\.\d{1,2})?\s*kg\.?)$", text, re.IGNORECASE)
        peeled = m.group(2).strip() if m else None
    if m:
        text = m.group(1)
        prefill["weight" if tmpl["has_weight"] else "cost"] = peeled
    parts = [text]
    while i < n and cells[i].text.startswith("("):     # wrapped '(...)' continuation
        parts.append(cells[i].text)
        i += 1
    return _norm_name(" ".join(parts)), i, prefill


def _assign_stats(run: List[str], tmpl: dict, fields: dict) -> None:
    run = [c.strip() for c in run]
    if tmpl["has_weight"] and tmpl["has_cost"]:
        if len(run) >= 2:
            fields.setdefault("weight", run[0])
            fields.setdefault("cost", run[1])
        elif len(run) == 1:
            c = run[0]
            if _is_cost_strict(c) and not _is_weight_strict(c):
                fields.setdefault("cost", c)
            else:
                fields.setdefault("weight", c)
    elif tmpl["has_weight"]:
        if len(run) == 1:
            fields.setdefault("weight", run[0])
        elif len(run) > 1:
            strict = [c for c in run if _is_weight_strict(c)]
            fields.setdefault("weight", strict[0] if strict else run[0])
    elif tmpl["has_cost"]:
        if run:
            fields.setdefault("cost", run[0])


def _read_avail_row(cells: List[Cell], i: int, tmpl: dict,
                    prefill: dict) -> Tuple[dict, int, bool, Optional[str]]:
    n = len(cells)
    fields = dict(prefill)
    run: List[str] = []
    cap = int(tmpl["has_weight"]) + int(tmpl["has_cost"]) + 3
    steps = 0
    while i < n and steps <= cap:
        av = _match_availability(cells, i)
        if av:
            _assign_stats(run, tmpl, fields)
            fields["availability"] = av[0]
            return fields, i + av[1], True, None
        t = cells[i].text
        if _is_stat_like(t):
            run.append(t)
            i += 1
            steps += 1
            continue
        break                           # a name / prose cell — row has no rarity
    if run:                             # looked like a row but the rarity was lost
        _assign_stats(run, tmpl, fields)
        return fields, i, False, "no availability cell parsed (OCR)"
    return fields, i, False, None


def _read_renown_row(cells: List[Cell], i: int, tmpl: dict,
                     prefill: dict) -> Tuple[dict, int, bool, Optional[str]]:
    n = len(cells)
    fields = dict(prefill)
    if tmpl["has_weight"] and "weight" not in fields:
        if i < n and (RE_DW_NUM.match(cells[i].text.strip())
                      or RE_DASH.match(cells[i].text.strip())):
            fields["weight"] = cells[i].text.strip()
            i += 1
        else:
            return fields, i, False, None
    if tmpl["has_cost"] and "cost" not in fields:
        if i < n and RE_DW_NUM.match(cells[i].text.strip()):
            fields["cost"] = cells[i].text.strip()
            i += 1
        elif i < n and RE_DASH.match(cells[i].text.strip()):
            i += 1
        else:
            return fields, i, False, None      # no Requisition number — prose
    if i < n:
        low = _avnorm(cells[i].text)
        if low in RENOWN_RANKS:
            fields["availability"] = low.title()
            i += 1
        elif RE_DASH.match(cells[i].text.strip()):
            i += 1
    return fields, i, True, None


def detect_gear(lines: List[str], pages: List[int], book: str,
                gear_titles: Dict[str, str]) -> Tuple[List[Gear], List[dict]]:
    rows: List[Gear] = []
    soft: List[dict] = []
    for region in _regions(lines, pages, gear_titles):
        cells = region.cells
        tmpl = region.template
        renown = tmpl["terminal"] == "renown"
        i, n = 0, len(cells)
        while i < n:
            if not _is_name_start(cells[i].text):
                i += 1
                continue
            page, start_line = cells[i].page, cells[i].line
            name, i, prefill = _read_name(cells, i, tmpl)
            reader = _read_renown_row if renown else _read_avail_row
            fields, i, ok, reason = reader(cells, i, tmpl, prefill)
            if not _plausible_name(name) or WEAPON_BLEED.search(name) or ARMOUR_BLEED.search(name):
                continue
            if ok:
                rows.append(Gear(name=name, category=region.category, book=book,
                                 page=page, line=start_line + 1,
                                 weight=fields.get("weight"), cost=fields.get("cost"),
                                 availability=fields.get("availability")))
            elif reason and _item_like(name):
                partial = {k: v for k, v in fields.items() if v}
                # Drop the pervasive artefact where a bare printed page-number line
                # (e.g. "147") is misread as the lone stat of a prose fragment.
                if partial and not all(str(v) == str(page) for v in partial.values()):
                    soft.append({"name": name, "category": region.category,
                                 "book": book, "page": page, "line": start_line + 1,
                                 "reason": reason, "partial": partial})

    # one row per (book, category, name): keep the richest, then the first seen.
    best: Dict[Tuple[str, str], Gear] = {}
    for g in rows:
        k = (g.category.lower(), g.name.lower())
        cur = best.get(k)
        if cur is None or g.quick_fields() > cur.quick_fields():
            best[k] = g
    return sorted(best.values(), key=lambda g: (g.line,)), soft


# ---------------------------------------------------------------------------
# SUPPLEMENT PATH — the gear-bearing 40K RP splatbooks.
#
# Mirrors the sibling weapon harvester: the five CORE sources keep running
# through detect_gear() UNCHANGED (byte-identical), and the supplements run
# through detect_gear_supp() ADDITIVELY.  The splat armouries reuse their parent
# book's column SHAPES, but their OCR is rougher, so four things defeat the core
# detector and are handled here:
#   1. The name column is headed by a SYNONYM ("Item", "Substance",
#      "Consumable", "Upgrade") and the title sometimes wraps onto a second line
#      ("Hive Consumables, Drugs," + "And Services"); `_regions_supp` matches a
#      per-book allow-list on a punctuation-stripped title and
#      `_detect_template_supp` skips the wrap remnant to find the header.
#   2. The Cost and Wt columns appear in EITHER order (Dark Heresy core is
#      Name|Wt|Cost, but the Inquisitor's Handbook / Blood of Martyrs are
#      Name|Cost|Wt); values are therefore assigned BY TYPE — a "kg"/decimal cell
#      is weight, a bare integer / Var / Varies / Priceless cell is cost — so the
#      column order no longer matters.
#   3. Availability carries values outside the core rarity ladder ("Uncommon",
#      "Issued Only") and cosmetic noise (a "Near-Unique" hyphen, a "Scarce†"
#      dagger); RARITIES_SUPP + `_avterm` absorb those.
#   4. Mixed tables append a Services price-list block, and rows carry sub-variant
#      labels ("Basic"/"Superior") plus weapon/armour/ammunition bleed; the row
#      walker STOPS at a "Service" sub-header and `_sanitize_gear_supp` rejects a
#      bare-variant name or a weapon/armour/ammo bleed row (→ soft, never faked).
# Book RAW throughout — a cell that cannot be trusted is left empty or the row is
# dropped to `soft`; nothing is invented, exactly as on the core path.
# ---------------------------------------------------------------------------

# Availability ladder for the supplements = the core rarity set PLUS the two
# extra printed values the splat armouries use ("Uncommon"; "Issued Only", the
# Ecclesiarchy's issue-only gate in Blood of Martyrs).  This is a SEPARATE set —
# the core RARITIES is never touched, so core output cannot shift.
RARITIES_SUPP = RARITIES | {"uncommon", "issued only"}

# Name-column header synonyms (the splats head the first column variously).
NAME_COL_SUPP = {"name", "item", "substance", "consumable", "upgrade", "unit",
                 "drug", "poison"}
# A Services price-list sub-header ends the harvestable part of a mixed table.
SERVICE_STOP = {"service", "services"}
# Bare sub-variant labels that are never a standalone item name (they qualify the
# row above — "Salvation Auger" → "Basic"/"Superior"; "Cogitator" → "Emplaced"/
# "Personal"); rejected to soft rather than banked as phantom items.
VARIANT_REJECT = {"basic", "superior", "standard", "short-range", "long-range",
                  "short range", "long range", "cylinder", "emplaced", "personal"}
# Supplement-only bleed guard: built-in cyber-weapons, a lone "Weapon" upgrade,
# any "… Armour" line (worn armour belongs to the armour index — no supplement
# gear item legitimately carries the word), and ammunition (plural forms only, so
# "Bolt Casing" is kept but "Psycannon Bolts" / "Void Rounds" are dropped).
BLEED_SUPP = re.compile(
    r"\b(?:weapons?|inbuilt\s+(?:blade|pistol|gun)|armou?r|shells|rounds|bolts|"
    r"cartridges|ammunition|munitions)\b", re.IGNORECASE)
# Leading weight token, used to scrub a value fused with a trailing word
# ("4kg case" → "4kg") while keeping the books' RAW forms ("1-kg", "+8kg").
RE_WT_LEAD = re.compile(r"^([+]?\d{1,4}(?:[.,]\d{1,3})?\s*-?\s*kg)", re.IGNORECASE)

# A weight-looking cell: carries "kg", or is a bare decimal (an unqualified kg).
RE_WT_SUPP = re.compile(r"kg", re.IGNORECASE)
RE_DEC_SUPP = re.compile(r"^[+]?\d{1,4}\.\d{1,2}$")
# A cost-looking cell: an integer (optionally comma-grouped, +prefixed, +/ea-
# suffixed), or one of the literal words the books print for a variable price.
RE_COST_SUPP = re.compile(
    r"^(?:[+]?\d{1,3}(?:,\d{3})+\+?|[+]?\d{1,6}\+?|\d{1,6}\s*ea\.?"
    r"|[Vv]ar(?:ies)?\.?|[Pp]riceless)$")


def _looks_weight(c: str) -> bool:
    c = c.strip()
    return bool(RE_WT_SUPP.search(c)) or bool(RE_DEC_SUPP.match(c))


def _looks_cost(c: str) -> bool:
    return bool(RE_COST_SUPP.match(c.strip()))


def _supp_stat_like(c: str) -> bool:
    c = c.strip()
    return bool(RE_DASH.match(c)) or _looks_weight(c) or _looks_cost(c)


def _avterm(s: str) -> str:
    """Normalise a cell for terminal (availability) matching: lower-case, fold a
    hyphen/dash to a space ('Near-Unique' → 'near unique'), drop a trailing
    footnote dagger / punctuation, collapse whitespace."""
    s = re.sub(r"\s+", " ", s).strip().lower()
    s = s.replace("–", " ").replace("—", " ").replace("-", " ")
    s = re.sub(r"[†‡*.,]+$", "", s).strip()
    return re.sub(r"\s+", " ", s).strip()


def _norm_title_supp(s: str) -> str:
    """Normalise a table title for the supplement allow-list: lower-case, collapse
    whitespace, and strip trailing wrap punctuation so a title that wrapped onto a
    second line ('War Zone Drugs &', 'Hive Consumables, Drugs,') still matches."""
    s = re.sub(r"\s+", " ", s).strip().lower()
    return re.sub(r"[\s,&.–—-]+$", "", s).strip()


def _match_avail_supp(cells: List["Cell"], i: int) -> Optional[Tuple[str, int]]:
    """If a supplement gear row's Availability terminal begins at cells[i], return
    (value, cells_consumed); else None.  Handles the single-cell rarity ladder and
    a two-cell split ('Near'+'Unique')."""
    n = len(cells)
    a = _avterm(cells[i].text)
    if a in RARITIES_SUPP:
        return a.title(), 1
    if i + 1 < n:
        two = (a + " " + _avterm(cells[i + 1].text)).strip()
        if two in RARITIES_SUPP:
            return two.title(), 2
    return None


def _detect_template_supp(cells: List["Cell"]) -> Tuple[dict, List["Cell"]]:
    """Read the header row to learn the table's template.  Skips any title-wrap
    remnant cells before the name-column synonym, then classifies the stat headers
    (weight / cost / availability / renown).  Returns (template, data_cells)."""
    n = len(cells)
    name_idx = None
    for k in range(min(n, 8)):                      # find the name-column header
        low = _avnorm(cells[k].text)
        if low in NAME_COL_SUPP or (low.split() and low.split()[0] in NAME_COL_SUPP
                                    and len(low.split()) == 1):
            name_idx = k
            break
    if name_idx is None:
        return ({"has_weight": False, "has_cost": False, "terminal": "avail"}, cells)
    has_weight = has_cost = False
    terminal: Optional[str] = None
    j = name_idx + 1
    while j < n:
        toks = _avnorm(cells[j].text).split()
        if toks and all(t in HEADER_TOKENS for t in toks):
            for t in toks:
                if t in ("wt", "wt.", "weight", "kg"):
                    has_weight = True
                if t in ("cost", "req", "req.", "requisition"):
                    has_cost = True
                if t == "renown":
                    terminal = "renown"
                if t in ("availability", "avail") and terminal is None:
                    terminal = "avail"
            j += 1
        else:
            break
    return ({"has_weight": has_weight, "has_cost": has_cost,
             "terminal": terminal or "avail"}, cells[j:])


def _regions_supp(lines: List[str], pages: List[int],
                  gear_titles: Dict[str, str]) -> List["Region"]:
    regions: List[Region] = []
    i, n = 0, len(lines)
    while i < n:
        if RE_TBL_ANY.match(lines[i]) and ":" in lines[i]:
            title = _norm_title_supp(lines[i].split(":", 1)[1])
            cat = gear_titles.get(title)
            if cat:
                j = i + 1
                buf: List[int] = []
                while j < n and not RE_TBL_ANY.match(lines[j]):
                    buf.append(j)
                    j += 1
                tmpl, data = _detect_template_supp(_build_cells(buf, lines, pages))
                regions.append(Region(cat, tmpl, data))
                i = j
                continue
        i += 1
    return regions


def _is_name_start_supp(c: str) -> bool:
    c = c.strip()
    if not c:
        return False
    if c[0].isdigit():                          # a digit-led name ('9-70 …') must
        if " " not in c or not re.search(r"[A-Za-z]", c):   # carry a real word, or
            return False                        # it is a stray stat number
    elif not c[0].isalpha() or not c[0].isupper():
        return False                            # real item names are capitalised
    low = _avnorm(c)
    if (low in HEADER_TOKENS or low in RARITIES_SUPP or low in RENOWN_RANKS
            or low in NAME_COL_SUPP or low in SERVICE_STOP or low in VARIANT_REJECT):
        return False
    if low.startswith("adeptus"):
        return False
    first = low.split()[0] if low.split() else low
    if first in ("with", "and", "or", "per"):   # a spilled continuation fragment
        return False
    return True


def _assign_supp(run: List[str], tmpl: dict, fields: dict) -> None:
    """Assign the collected stat cells BY TYPE, so a Cost|Wt table and a Wt|Cost
    table both parse: a 'kg'/decimal cell is the weight, a bare-integer / Var /
    Priceless cell is the cost.  Dash placeholders are dropped."""
    run = [c.strip() for c in run if c.strip() and not RE_DASH.match(c.strip())]
    if tmpl["has_weight"] and tmpl["has_cost"]:
        for c in run:
            if _looks_weight(c) and "weight" not in fields:
                fields["weight"] = c
            elif _looks_cost(c) and "cost" not in fields:
                fields["cost"] = c
    elif tmpl["has_weight"]:
        if run:
            fields.setdefault("weight", run[0])
    elif tmpl["has_cost"]:
        if run:
            fields.setdefault("cost", run[0])


def _read_avail_supp(cells: List["Cell"], i: int, tmpl: dict,
                     prefill: dict) -> Tuple[dict, int, bool, Optional[str]]:
    n = len(cells)
    fields = dict(prefill)
    run: List[str] = []
    cap = 3 + int(tmpl["has_weight"]) + int(tmpl["has_cost"])
    steps = 0
    while i < n and steps <= cap:
        term = _match_avail_supp(cells, i)
        if term:
            _assign_supp(run, tmpl, fields)
            fields["availability"] = term[0]
            return fields, i + term[1], True, None
        if _avnorm(cells[i].text) in SERVICE_STOP:
            break
        t = cells[i].text
        if _supp_stat_like(t):
            run.append(t)
            i += 1
            steps += 1
            continue
        break
    if run:
        _assign_supp(run, tmpl, fields)
        return fields, i, False, "no availability cell parsed (OCR)"
    return fields, i, False, None


def _sanitize_gear_supp(g: "Gear") -> Optional["Gear"]:
    """Scrub a supplement row; return None to reject it (soft skip).  Never invents
    a value — a field that does not fit its type is blanked, not guessed."""
    nm = g.name
    if (WEAPON_BLEED.search(nm) or ARMOUR_BLEED.search(nm) or BLEED_SUPP.search(nm)):
        return None                             # weapon / armour / ammunition bleed
    if _avnorm(nm) in VARIANT_REJECT or not _plausible_name(nm):
        return None
    if g.weight is not None:
        w = g.weight.strip()
        if RE_DASH.match(w):
            g.weight = None
        elif re.match(r"^[Vv]ar(?:ies)?\.?$", w):
            g.weight = w                        # the books' literal "Var" weight
        elif RE_WT_LEAD.match(w):
            g.weight = RE_WT_LEAD.match(w).group(1)   # scrub a fused trailing word
        elif RE_DEC_SUPP.match(w):
            g.weight = w                        # a bare decimal (unqualified kg)
        else:
            g.weight = None                     # not a weight → drop, don't fake
    if g.cost is not None:
        c = g.cost.strip()
        g.cost = c if (not RE_DASH.match(c) and _looks_cost(c)) else None
    if g.availability is not None:
        av = _avterm(g.availability)
        if av not in RARITIES_SUPP and av not in RENOWN_RANKS:
            g.availability = None
    return g


def _read_renown_row_supp(cells: List["Cell"], i: int, tmpl: dict,
                          prefill: dict) -> Tuple[dict, int, bool, Optional[str]]:
    """Deathwatch supplement (First Founding) Wargear: Name | Requisition | Renown.
    Stricter than the core reader — a valid row MUST end on a Renown rank OR an
    explicit '–' (no-rank) cell.  This is what stops the Wargear region, which
    runs to the next 'Table' heading, from banking NPC stat-block bleed
    ('Wounds: 22', 'Loyalty: 32') as phantom wargear."""
    n = len(cells)
    fields = dict(prefill)
    if tmpl["has_cost"] and "cost" not in fields:
        if i < n and RE_DW_NUM.match(cells[i].text.strip()):
            fields["cost"] = cells[i].text.strip()
            i += 1
        elif i < n and RE_DASH.match(cells[i].text.strip()):
            i += 1
        else:
            return fields, i, False, None          # no Requisition number → prose
    if i < n:
        low = _avnorm(cells[i].text)
        if low in RENOWN_RANKS:
            fields["availability"] = low.title()
            return fields, i + 1, True, None
        if RE_DASH.match(cells[i].text.strip()):
            return fields, i + 1, True, None       # explicit no-rank (valid)
    return fields, i, False, "no Renown terminal (region over-run past the table)"


_ROMAN_HEAD = re.compile(r"^[IVXLC]+\s*[:.]")


def _supp_soft_worthy(name: str) -> bool:
    """Keep the supplement `soft` list honest: bank a genuinely ambiguous gear row,
    but drop the chapter-header / stat-label bleed a long region sweeps in
    ('III: Feral & Feudal Worlds', 'Wounds:')."""
    return _item_like(name) and ":" not in name and not _ROMAN_HEAD.match(name)


def detect_gear_supp(lines: List[str], pages: List[int], book: str,
                     gear_titles: Dict[str, str]) -> Tuple[List["Gear"], List[dict]]:
    rows: List[Gear] = []
    soft: List[dict] = []
    for region in _regions_supp(lines, pages, gear_titles):
        cells = region.cells
        tmpl = region.template
        renown = tmpl["terminal"] == "renown"
        i, n = 0, len(cells)
        while i < n:
            if _avnorm(cells[i].text) in SERVICE_STOP:      # services block → stop
                break
            if not _is_name_start_supp(cells[i].text):
                i += 1
                continue
            page, start_line = cells[i].page, cells[i].line
            name, i, prefill = _read_name(cells, i, tmpl)
            if renown:
                fields, i, ok, reason = _read_renown_row_supp(cells, i, tmpl, prefill)
            else:
                fields, i, ok, reason = _read_avail_supp(cells, i, tmpl, prefill)
            if ok:
                g = Gear(name=name, category=region.category, book=book, page=page,
                         line=start_line + 1, weight=fields.get("weight"),
                         cost=fields.get("cost"), availability=fields.get("availability"))
                clean = _sanitize_gear_supp(g)
                if clean is not None:
                    rows.append(clean)
                elif _supp_soft_worthy(name):
                    soft.append({"name": name, "category": region.category,
                                 "book": book, "page": page, "line": start_line + 1,
                                 "reason": "rejected (weapon/armour/ammo/variant bleed)",
                                 "partial": {k: v for k, v in fields.items() if v}})
            elif reason and _supp_soft_worthy(name):
                partial = {k: v for k, v in fields.items() if v}
                if partial and not all(str(v) == str(page) for v in partial.values()):
                    soft.append({"name": name, "category": region.category,
                                 "book": book, "page": page, "line": start_line + 1,
                                 "reason": reason, "partial": partial})

    best: Dict[Tuple[str, str], Gear] = {}
    for g in rows:
        k = (g.category.lower(), g.name.lower())
        cur = best.get(k)
        if cur is None or g.quick_fields() > cur.quick_fields():
            best[k] = g
    return sorted(best.values(), key=lambda g: (g.line,)), soft


# Detector registry — a Source names its detector; the cores use "core"
# (detect_gear, unchanged), the splats use "supp" (detect_gear_supp).
DETECTORS: Dict[str, Callable[[List[str], List[int], str, Dict[str, str]],
                              Tuple[List["Gear"], List[dict]]]] = {
    "core": detect_gear,
    "supp": detect_gear_supp,
}


@dataclass
class Source:
    key: str
    book: str
    path: Path
    citation: str
    gear_titles: Dict[str, str]
    detector: str = "core"          # "core" (cores, unchanged) or "supp" (splats)
    coverage: str = "pending"
    lines: List[str] = field(default_factory=list)
    gear: List[Gear] = field(default_factory=list)
    soft: List[dict] = field(default_factory=list)


_40K = Path("Warhammer/40K Roleplay")

# Per-book gear tables, keyed by the normalised heading text after "Table N:".
# Only these tables are harvested — this precisely excludes Services, Medical
# Care, Signature Wargear, Cybernetic Replacement, Servitors & Familiars,
# Archeotech (starship) Components and the Random Issue Gear d100 flavour list.
DH_TITLES = {
    "clothing & personal items": "Clothing & Personal Items",
    "drugs and consumables": "Drugs & Consumables",
    "tools": "Tools",
    "cybernetics": "Cybernetics",
}
RT_TITLES = {
    "gear": "Gear",
    "drugs and consumables": "Drugs & Consumables",
    "tools": "Tools",
    "cybernetics": "Cybernetics",
}
DW_TITLES = {
    "equipment": "Equipment",
    "drugs and consumables": "Drugs & Consumables",
    "tools": "Tools",
    "cybernetics": "Cybernetics",
}
OW_TITLES = {
    "clothing and worn gear": "Clothing & Worn Gear",
    "drugs": "Drugs",
    "tools": "Tools",
    "cybernetics": "Cybernetics",
}
BC_TITLES = {
    "clothing": "Clothing",
    "tools": "Tools",
    "wargear": "Wargear",
    "cybernetics": "Cybernetics",
}

# --- SUPPLEMENT gear-table allow-lists (the "supp" detector) -----------------
# Curated per book: ONLY genuine gear / tools / drugs / consumables / cybernetics
# tables.  Deliberately EXCLUDED (as on the core path): weapon lists, armour &
# force-field tables (e.g. IH "War Zone Protective Gear", RT "Kroot Gear"),
# ammunition sub-tables, services / medical-care price lists (IH "Feral & Feudal
# Consumables And Services"), installation-difficulty tables (IH "Implants &
# Bionic Components"), and the craftsmanship-pattern rules tables (OW "General
# Equipment Pattern Positive/Negative", "Special Equipment Doctrines").  Keys are
# `_norm_title_supp` of the heading line (trailing wrap punctuation stripped).
IH_TITLES = {
    "feral and feudal gear": "General Equipment",
    "personal equipment": "General Equipment",
    "forge world gear": "General Equipment",
    "frontier gear and tools": "Tools",
    "frontier substances": "Drugs & Consumables",
    "void gear": "General Equipment",
    "war zone infantry gear": "General Equipment",
    "war zone drugs": "Drugs & Consumables",             # "…& Medical Gear" (wrapped)
    "holy ordos gear, tools and": "Tools",               # "…Ammunition" (wrapped)
    "implants and blessings": "Cybernetics",
    "hive consumables, drugs": "Drugs & Consumables",    # "…And Services" (wrapped)
}
RAD_TITLES = {
    "gear": "General Equipment",
    "drugs": "Drugs & Consumables",
    "dark tech gear and tools": "Tools",
    "xenos tools": "Tools",
}
ASC_TITLES = {"gear": "General Equipment"}
BOM_TITLES = {"ecclesiarchal tools": "Tools"}
HOST_TITLES = {
    "gear and tools": "Tools",
    "drugs, poisons": "Drugs & Consumables",             # "…and Consumables" (wrapped)
    "cybernetics and implants": "Cybernetics",
}
FF_TITLES = {"wargear": "Wargear"}
HAMMER_SUPP_TITLES = {
    "clothing and worn gear": "Clothing & Worn Gear",
    "tools": "Tools",
    "cybernetics": "Cybernetics",
}
TOB_SUPP_TITLES = {"wargear and equipment": "Wargear"}
TOE_SUPP_TITLES = {
    "wargear and equipment": "Wargear",
    "drugs and consumables": "Drugs & Consumables",
}
TOF_SUPP_TITLES = {"wargear and equipment": "Wargear"}

SOURCES: List[Source] = [
    Source("dh-core", "Dark Heresy — Core Rulebook",
           _40K / "Dark Heresy/Rulebooks/Dark Heresy - Core Rulebook.pdf.md",
           "Dark Heresy Core Rulebook (FFG, WH40K Roleplay), Armoury — Gear tables "
           "(Clothing & Personal Items, Drugs & Consumables, Tools, Cybernetics)",
           DH_TITLES),
    Source("rt-core", "Rogue Trader — Core Rulebook",
           _40K / "Rogue Trader/Rulebooks/Rogue Trader - Core Rulebook (updated with 1.4 errata).md",
           "Rogue Trader Core Rulebook, 1.4 errata (FFG, WH40K Roleplay), Armoury — "
           "Gear tables (Gear, Drugs & Consumables, Tools, Cybernetics); acquired by "
           "Availability, no Throne cost",
           RT_TITLES),
    Source("dw-core", "Deathwatch — Core Rulebook",
           _40K / "Deathwatch/Rulebooks/Deathwatch - Core Rulebook.md",
           "Deathwatch Core Rulebook (FFG, WH40K Roleplay), Armoury — Gear tables "
           "(Equipment, Drugs & Consumables, Tools, Cybernetics); Requisition stored "
           "in cost, Renown in availability (\u2013 = no rank required)",
           DW_TITLES),
    Source("ow-core", "Only War — Core Rulebook",
           _40K / "Only War/Rulebooks/Only War - Core Rulebook.md",
           "Only War Core Rulebook (FFG, WH40K Roleplay), Armoury — Gear tables "
           "(Clothing & Worn Gear, Drugs, Tools, Cybernetics); acquired by "
           "Availability, no Throne cost",
           OW_TITLES),
    Source("bc-core", "Black Crusade — Core Rulebook",
           _40K / "Black Crusade/Rulebooks/Black Crusade - Core Rulebook.md",
           "Black Crusade Core Rulebook (FFG, WH40K Roleplay), Armoury — Gear tables "
           "(Clothing, Tools, Wargear, Cybernetics); acquired by Availability/Infamy, "
           "no Throne cost",
           BC_TITLES),

    # --- SUPPLEMENTS (added later; the "supp" detector) ----------------------
    # Dark Heresy line
    Source("dh-inquisitor", "Dark Heresy — The Inquisitor's Handbook",
           _40K / "Dark Heresy/Rulebooks/Dark Heresy - The Inquisitor's Handbook.md",
           "Dark Heresy: The Inquisitor's Handbook (FFG, WH40K Roleplay), Extended "
           "Armoury — gear/tools/drugs/implant tables (Feral & Feudal, Hive, Forge "
           "World, Frontier, Void, War Zone, Holy Ordos); Cost/Wt columns vary in "
           "order; excludes War Zone Protective armour and the bionic-install table",
           IH_TITLES, "supp"),
    Source("dh-radicals", "Dark Heresy — The Radical's Handbook",
           _40K / "Dark Heresy/Rulebooks/Dark Heresy - The Radical's Handbook.md",
           "Dark Heresy: The Radical's Handbook (FFG, WH40K Roleplay), Armoury — "
           "Gear, Drugs, Dark Tech Gear & Tools, Xenos Tools",
           RAD_TITLES, "supp"),
    Source("dh-ascension", "Dark Heresy — Ascension",
           _40K / "Dark Heresy/Rulebooks/Dark Heresy - Ascension.md",
           "Dark Heresy: Ascension (FFG, WH40K Roleplay), Armoury — Gear "
           "(acquired by Availability)",
           ASC_TITLES, "supp"),
    Source("dh-blood", "Dark Heresy — Blood of Martyrs",
           _40K / "Dark Heresy/Rulebooks/Dark Heresy - Blood of Martyrs.md",
           "Dark Heresy: Blood of Martyrs (FFG, WH40K Roleplay), Armoury — "
           "Ecclesiarchal Tools (Name|Cost|Wt; 'Issued Only' availability)",
           BOM_TITLES, "supp"),
    # Rogue Trader line  (Into the Storm & Navis Primer carry no harvestable gear —
    # see the SKIPPED note below — so only Hostile Acquisitions is sourced)
    Source("rt-hostile", "Rogue Trader — Hostile Acquisitions",
           _40K / "Rogue Trader/Rulebooks/Rogue Trader - Hostile Acquisitions.md",
           "Rogue Trader: Hostile Acquisitions (FFG, WH40K Roleplay), Armoury — "
           "Gear & Tools, Drugs/Poisons/Consumables, Cybernetics & Implants "
           "(acquired by Availability)",
           HOST_TITLES, "supp"),
    # Deathwatch line  (Wargear grades by Requisition/Renown, not Cost/Availability)
    Source("dw-founding", "Deathwatch — First Founding",
           _40K / "Deathwatch/Rulebooks/Deathwatch - First Founding.md",
           "Deathwatch: First Founding (FFG, WH40K Roleplay), Armoury — Wargear "
           "(Requisition stored in cost, Renown in availability)",
           FF_TITLES, "supp"),
    # Only War line
    Source("ow-hammer", "Only War — Hammer of the Emperor",
           _40K / "Only War/Rulebooks/Only War - Hammer of The Emperor.md",
           "Only War: Hammer of the Emperor (FFG, WH40K Roleplay), Armoury — "
           "Clothing & Worn Gear, Tools, Cybernetics; excludes the equipment-"
           "pattern craftsmanship tables",
           HAMMER_SUPP_TITLES, "supp"),
    # Black Crusade line
    Source("bc-blood", "Black Crusade — Tome of Blood",
           _40K / "Black Crusade/Rulebooks/Black Crusade - Tome of Blood.md",
           "Black Crusade: Tome of Blood (FFG, WH40K Roleplay), Armoury — Wargear "
           "& Equipment (Khornate wargear)",
           TOB_SUPP_TITLES, "supp"),
    Source("bc-excess", "Black Crusade — Tome of Excess",
           _40K / "Black Crusade/Rulebooks/Black Crusade - Tome of Excess.md",
           "Black Crusade: Tome of Excess (FFG, WH40K Roleplay), Armoury — Wargear "
           "& Equipment, Drugs & Consumables (Slaaneshi wargear)",
           TOE_SUPP_TITLES, "supp"),
    Source("bc-fate", "Black Crusade — Tome of Fate",
           _40K / "Black Crusade/Rulebooks/Black Crusade - Tome of Fate.md",
           "Black Crusade: Tome of Fate (FFG, WH40K Roleplay), Armoury — Wargear "
           "& Equipment (Tzeentchian wargear)",
           TOF_SUPP_TITLES, "supp"),
    # SKIPPED (verified, not fabricated): Rogue Trader — Into the Storm (its gear
    # tables OCR'd as CID-font gibberish, item cells unrecoverable) and The Navis
    # Primer (no gear/tools/drugs/cybernetics tables — Navigator/psychic content);
    # Deathwatch — Rites of Battle & Honour the Chapter and Dark Heresy — The Lathe
    # Worlds (known shattered scans, no gear tables survive).
]


def _fresh_sources() -> List[Source]:
    return [Source(s.key, s.book, s.path, s.citation, s.gear_titles, s.detector)
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
            src.gear, src.soft = DETECTORS[src.detector](src.lines, pages, src.book,
                                                         src.gear_titles)
            src.coverage = f"ok — {len(src.gear)} gear items from {path.name}"
            _write_progress(self.sources)

    def all_gear(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for g in src.gear:
                yield src, g

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, g in self.all_gear(book):
            nm = g.name.lower()
            if nm == q:
                exact.append((src, g))
            elif q in nm:
                partial.append((src, g))
        return exact if exact else partial


def _write_progress(sources: List[Source]) -> None:
    try:
        PROGRESS.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS.write_text(json.dumps(
            {"system": SYSTEM,
             "books": [{"book": s.book, "coverage": s.coverage,
                        "gear": len(s.gear), "soft": len(s.soft)}
                       for s in sources]}, indent=1), encoding="utf-8")
    except Exception:
        pass


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    soft_total = 0
    sources_out = []
    md: List[str] = [
        "# WH40K ROLEPLAY GEAR INDEX — The New Path",
        "",
        "**Generated by `scripts/wh40krp_gear_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** These are **Warhammer 40,000 Roleplay** GEAR items —",
        "the non-weapon, non-armour equipment of the Fantasy Flight Games d100 line",
        "(Dark Heresy / Rogue Trader / Deathwatch / Only War / Black Crusade — the",
        "five core rulebooks plus their gear-bearing supplements):",
        "general equipment & clothing, drugs & consumables, tools & kits, and",
        f"cybernetics/bionics. Every row is stamped `system: {SYSTEM}`; a 40K RP",
        "gear item is SOURCE MATERIAL for the system-translator skill, not campaign",
        "RAW. Weapons and armour live in their sibling indices. Acquisition differs",
        "by game: Dark Heresy lists a Throne **cost**; Rogue Trader / Only War /",
        "Black Crusade use **Availability** only; Deathwatch uses **Requisition**",
        "(shown under Cost) and **Renown** (shown under Availability; `—` = no rank).",
        "A field left `—` is one the OCR did not cleanly yield. Item effects live in",
        "the books' prose blurbs and are intentionally not reproduced here. Use",
        "`--export \"NAME\"` for the translator packet.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.gear)
        soft_total += len(src.soft)
        parsed_well += sum(1 for g in src.gear if g.quick_fields() >= 2)
        sources_out.append({"key": src.key, "book": src.book, "system": SYSTEM,
                            "citation": src.citation, "coverage": src.coverage,
                            "gear": [asdict(g) for g in src.gear],
                            "soft": src.soft})
        cats = sorted({g.category for g in src.gear})
        md.append(f"## {src.book} — {len(src.gear)} gear items  *(system: {SYSTEM})*")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.gear:
            md.append("| Item | Category | Weight | Cost | Availability | Page |")
            md.append("|---|---|---|---|---|---|")
            for g in sorted(src.gear, key=lambda x: (x.category, x.name.lower())):
                md.append(
                    f"| {g.name} | {g.category} | {g.weight or '—'} | "
                    f"{g.cost or '—'} | {g.availability or '—'} | "
                    f"{g.page if g.page is not None else '—'} |")
        if src.soft:
            md.append("")
            md.append(f"*Soft ({len(src.soft)}): rows the OCR left ambiguous — "
                      "banked here for honesty, not in the index.*")
            for s in src.soft:
                md.append(f"- {s['name']} ({s['category']}, p.{s['page']}): "
                          f"{s['reason']}; partial {s['partial']}")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/wh40krp_gear_harvest.py",
                    "system": SYSTEM, "corpus": str(corpus.base),
                    "total_gear": total, "total_soft": soft_total,
                    "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 8:
        print(f"'{name}' matches {len(hits)} items; narrow with --book or the exact name:")
        for src, g in hits[:20]:
            print(f"  {g.name}   [{g.book}, p.{g.page}]")
        return 1
    packets = []
    for src, g in hits:
        lo = max(0, g.line - 1)
        body = [ln for ln in src.lines[lo:lo + 10] if not PAGE.search(ln)]
        packets.append({
            "packet": "wh40krp-gear-for-translation",
            "instructions": ("A Warhammer 40,000 Roleplay gear item (system: "
                             f"{SYSTEM}). Feed to the system-translator skill for "
                             "the paired 3.5e AND GURPS treatment. The raw_block "
                             "is OCR text from a column-dump table."),
            "name": g.name, "system": SYSTEM, "category": g.category,
            "source": {"book": g.book, "pdf_page": g.page,
                       "extraction": str(corpus.base / src.path),
                       "line": g.line, "citation": src.citation},
            "parsed": {k: v for k, v in asdict(g).items()
                       if k in ("category", "weight", "cost", "availability") and v},
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
# A column-dump fixture exercising every template shape: Dark-Heresy Wt+Cost+Avail
# (with a slash-name), Cybernetics Cost+Avail plus the multi-cell "Adeptus
# Mechanicus Only", Rogue-Trader bare-weight + a wrapped '(...)' name, and
# Deathwatch Wt+Req+Renown with a name+weight fused onto one line. A trailing
# non-gear table and an in-region prose line prove the boundaries hold.
FIXTURE = """## [PDF page 150]
Table 5-16: Tools
Name
Wt
Cost	 Availability
Auspex/Scanner
0.5 kg	 145
Scarce
Combi-tool
1 kg
200
Rare
Table 5\u201319: Cybernetics
Name
Cost
Availability
Bionic Arm
1,000
Scarce
Ballistic Mechadendrite
600
Adeptus

Mechanicus Only
Cortex Implants
5,000
Very Rare
Table 5\u201313: Gear
Name
kg
Availability
Cameleoline Cloak
0.5
Rare
Clothing and Adornment
(Common)
\u2013
Abundant\u2020
Survival suits keep the wearer alive in extreme conditions.
Table 5\u201317: Equipment
Name
Wt
Req
Renown
Astartes Harness
8
4
\u2013
Astartes Psychic Hood 15
25
Distinguished
Table 5-99: Ammunition
Name
Cost
"""

FIXTURE_TITLES = {"tools": "Tools", "cybernetics": "Cybernetics",
                  "gear": "Gear", "equipment": "Equipment"}


# A supplement fixture exercising the wh40krp_supp path: an "Item"-headed table
# with the Cost|Wt columns in the OPPOSITE order to Dark Heresy core (assigned by
# type, not position), the extra terminals "Uncommon"/"Issued Only" and a
# "Near-Unique" hyphen, an ammunition bleed row that must be dropped, a Services
# sub-header that must STOP the table, a bare-weight table with a name+weight
# fused onto one line, and a Deathwatch Requisition/Renown table with a name+req
# fusion plus a stat-block-bleed line ("Wounds: 22") that has no Renown terminal.
SUPP_FIXTURE = """## [PDF page 300]
Table 4-4: Personal Equipment
Item
Cost
Wt
Availability
Axe-Rake
20
4kg
Uncommon
Chaplet Ecclesiasticus
1,000
1 kg
Issued Only
Occlusive Vault
15
–
Near-Unique
Blazer Shotgun Shells
4
–
Common
Service
Cost
Wt
Availability
Porter
10
–
Plentiful
Table 4-7: Gear
Name
Weight
Availability
Immateria Ward 1 kg
Very Rare
Table 4-9: Wargear
Name
Requisition Renown
Blood Chalice
25
Famed
The Glorious Standard 40
Hero
Wounds:
22
Table 9-9: Weapon Upgrades
Name
Cost
"""

SUPP_FIXTURE_TITLES = {"personal equipment": "General Equipment",
                       "gear": "General Equipment", "wargear": "Wargear"}


def selftest(base: Path) -> int:
    failures: List[str] = []

    lines = FIXTURE.splitlines()
    gear, soft = detect_gear(lines, _pages_for(lines), "Fixture Core Rulebook",
                             FIXTURE_TITLES)
    by = {g.name: g for g in gear}
    names = [g.name for g in gear]
    want = ["Auspex/Scanner", "Combi-tool", "Bionic Arm", "Ballistic Mechadendrite",
            "Cortex Implants", "Cameleoline Cloak", "Clothing and Adornment (Common)",
            "Astartes Harness", "Astartes Psychic Hood"]
    if names != want:
        failures.append(f"fixture detected {names}, wanted {want}")
    else:
        checks = [
            ("Auspex/Scanner", "Tools", "0.5 kg", "145", "Scarce"),
            ("Combi-tool", "Tools", "1 kg", "200", "Rare"),
            ("Bionic Arm", "Cybernetics", None, "1,000", "Scarce"),
            ("Ballistic Mechadendrite", "Cybernetics", None, "600", "Adeptus Mechanicus Only"),
            ("Cortex Implants", "Cybernetics", None, "5,000", "Very Rare"),
            ("Cameleoline Cloak", "Gear", "0.5", None, "Rare"),
            ("Clothing and Adornment (Common)", "Gear", "\u2013", None, "Abundant"),
            ("Astartes Harness", "Equipment", "8", "4", None),
            ("Astartes Psychic Hood", "Equipment", "15", "25", "Distinguished"),
        ]
        for nm, cat, wt, cost, avail in checks:
            g = by[nm]
            got = (g.category, g.weight, g.cost, g.availability, g.system)
            exp = (cat, wt, cost, avail, SYSTEM)
            if got != exp:
                failures.append(f"{nm} parsed {got}, wanted {exp}")
    # The prose line inside the Gear region must not become a row.
    if any("survival suits" in g.name.lower() for g in gear):
        failures.append("fixture prose line leaked into the index as a gear row")
    # The trailing non-gear Ammunition table must contribute nothing.
    if any(g.category not in ("Tools", "Cybernetics", "Gear", "Equipment") for g in gear):
        failures.append("a row escaped the four fixture gear tables")

    # --- SUPPLEMENT fixture: the wh40krp_supp path -------------------------
    slines = SUPP_FIXTURE.splitlines()
    sgear, ssoft = detect_gear_supp(slines, _pages_for(slines), "Fixture Supplement",
                                    SUPP_FIXTURE_TITLES)
    sby = {g.name: g for g in sgear}
    snames = [g.name for g in sgear]
    swant = ["Axe-Rake", "Chaplet Ecclesiasticus", "Occlusive Vault",
             "Immateria Ward", "Blood Chalice", "The Glorious Standard"]
    if snames != swant:
        failures.append(f"supp fixture detected {snames}, wanted {swant}")
    else:
        schecks = [
            # (name, category, weight, cost, availability) — Cost|Wt swapped order,
            # extra terminals, dash weight, a name+weight fuse, and DW req/renown.
            ("Axe-Rake", "General Equipment", "4kg", "20", "Uncommon"),
            ("Chaplet Ecclesiasticus", "General Equipment", "1 kg", "1,000", "Issued Only"),
            ("Occlusive Vault", "General Equipment", None, "15", "Near Unique"),
            ("Immateria Ward", "General Equipment", "1 kg", None, "Very Rare"),
            ("Blood Chalice", "Wargear", None, "25", "Famed"),
            ("The Glorious Standard", "Wargear", None, "40", "Hero"),
        ]
        for nm, cat, wt, cost, avail in schecks:
            g = sby[nm]
            got = (g.category, g.weight, g.cost, g.availability, g.system)
            exp = (cat, wt, cost, avail, SYSTEM)
            if got != exp:
                failures.append(f"supp {nm} parsed {got}, wanted {exp}")
    # The ammunition bleed row, the Services block, and the stat-block bleed line
    # must never reach the index.
    for banned in ("Blazer Shotgun Shells", "Porter", "Wounds"):
        if any(banned.lower() in g.name.lower() for g in sgear):
            failures.append(f"supp fixture leaked a banned row: {banned!r}")

    if base.is_dir() and any((base / s.path).exists() for s in SOURCES):
        corpus = Corpus(base, _fresh_sources())
        by_key = {s.key: s for s in corpus.sources}
        # HARD CONSTRAINT — the five cores stay EXACTLY 60/99/38/86/84 (= 367) and
        # are untouched by the supplement path.  This locks core preservation.
        core_expect = {"dh-core": 60, "rt-core": 99, "dw-core": 38,
                       "ow-core": 86, "bc-core": 84}
        core_total = 0
        for key, exp_n in core_expect.items():
            src = by_key.get(key)
            if src is None or not (base / src.path).exists():
                continue
            core_total += len(src.gear)
            if len(src.gear) != exp_n:
                failures.append(f"CORE PRESERVATION: {key} yielded "
                                f"{len(src.gear)} gear items; must be exactly {exp_n}")
        if core_total and core_total != 367:
            failures.append(f"CORE PRESERVATION: cores total {core_total}, must be 367")
        supp_total = sum(len(s.gear) for s in corpus.sources
                         if s.key not in core_expect)
        if core_total == 367 and supp_total < 120:
            failures.append(f"only {supp_total} supplement gear items harvested; "
                            f"expected the splatbooks to add well over 120")
        for _, g in corpus.all_gear():
            if g.system != SYSTEM:
                failures.append(f"{g.name}: system stamp is {g.system!r}")
                break
            if not g.name:
                failures.append("a live gear row has an empty name")
                break
            if _avnorm(g.name) in HEADER_TOKENS or _avnorm(g.name) in RARITIES:
                failures.append(f"header/junk name banked: {g.name!r}")
                break
            if WEAPON_BLEED.search(g.name) or ARMOUR_BLEED.search(g.name):
                failures.append(f"weapon/armour bleed-through: {g.name!r}")
                break
        for known in ("Auspex/Scanner", "Medikit", "Chrono"):
            if not corpus.find(known):
                failures.append(f"known gear not found in live corpus: {known}")
        aug = corpus.find("Bionic Arm")
        if aug and all(g.availability is None for _, g in aug):
            failures.append("live Bionic Arm rows all missing availability")
        # a specific SUPPLEMENT gear row, harvested live, parses correctly — this
        # one is unique to a splat and exercises the Name|Cost|Wt (swapped) order
        # plus the extended "Issued Only" terminal, end to end.
        chap = corpus.find("Chaplet Ecclesiasticus")     # Blood of Martyrs, Tools
        if not chap:
            failures.append("supplement gear 'Chaplet Ecclesiasticus' not found live")
        else:
            cg = chap[0][1]
            got = (cg.category, cg.weight, cg.cost, cg.availability)
            if got != ("Tools", "1 kg", "1,000", "Issued Only"):
                failures.append(f"live Chaplet Ecclesiasticus parsed {got}, wanted "
                                f"('Tools', '1 kg', '1,000', 'Issued Only')")
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
        found = sorted({(g.name, g.category, g.book, g.page or -1,
                         g.availability or "—")
                        for _, g in corpus.all_gear(args.book) if q in g.name.lower()})
        for name, cat, bk, page, avail in found:
            loc = bk if page < 0 else f"{bk}, p.{page}"
            print(f"  {name}   [{cat}; {avail}; {loc}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.gear for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.gear):4d} gear" if src.gear else "   0 gear"
        soft = f" (+{len(src.soft)} soft)" if src.soft else ""
        print(f"  {src.book:34s} {status}{soft}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} WH40K Roleplay gear items across "
          f"{sum(1 for s in corpus.sources if s.gear)} book(s); "
          f"{parsed_well} with 2+ stat fields. (system: {SYSTEM})")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
