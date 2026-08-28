#!/usr/bin/env python3
"""wh40krp_weapon_harvest.py — collate WH40K Roleplay weapons (system: WH40K Roleplay).

THE PROCESS (Chad, 2026-08-28, opening the 40K shelf): other GAME SYSTEMS are
welcome in the reference layer AS LONG AS each is clearly LABELLED by system —
the translator tools convert them into the hybrid's 3.5e + GURPS. This is the
**Warhammer 40,000 Roleplay** (Fantasy Flight Games d100) WEAPON index — Dark
Heresy / Rogue Trader / Deathwatch / Only War / Black Crusade — kept entirely
separate and stamped `"system": "WH40K Roleplay"`.

    reference/wh40krp_weapon_index.json — every weapon: name, class, range, RoF,
                                          damage, pen, clip, reload, special,
                                          weight, availability, book + PDF page
    reference/wh40krp_weapon_index.md   — the same, for human eyes

`--export` emits a translator-ready packet (a 40K RP weapon the system-translator
skill converts to the 3.5e + GURPS pair).

WORKFLOW
    python wh40krp_weapon_harvest.py                     # (re)build the index
    python wh40krp_weapon_harvest.py --search "bolt"     # find candidates
    python wh40krp_weapon_harvest.py --export "Lasgun"
    python wh40krp_weapon_harvest.py --selftest

GOVERNING SOURCES
    I:\\Sourcebooks\\_text\\Warhammer\\40K Roleplay\\ — the five core rulebooks.
    Their Armoury tables (Table 5-7 "Ranged Weapons", Table 5-9 "Melee Weapons",
    and their kin) were OCR'd as a VERTICAL COLUMN-DUMP: each weapon is a run of
    cells, one per line, in a fixed column order —
        RANGED: Name, Class, Range, RoF, Dam, Pen, Clip, Rld, Special, Wt,
                [Cost], Availability
        MELEE : Name, Class, Range, Dam, Pen, Special, Wt, [Cost], Availability
    The detector splits every line on tabs (the OCR sometimes fuses two cells on
    one line), then ANCHORS on the unmistakable Damage cell (`XdY+Z type`). The
    identity fields (name/class/range/RoF) are read backward from the anchor; the
    trailing fields (pen/clip/reload/special/weight/availability) are read forward
    and assigned BY TYPE, so the messier books (merged Name+Class in Rogue Trader,
    wrapped multi-line names in Deathwatch, omitted-empty cells) still parse. A
    configured source whose file is missing prints NO COVERAGE.  Book RAW only —
    every stat is the book's, cited to book + PDF page; nothing is invented.
    (Deathwatch's armoury uses Req/Renown in place of Cost/Availability, so its
    `availability` is left blank — that column does not exist in the source.)
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
OUT_JSON = REPO / "reference" / "wh40krp_weapon_index.json"
OUT_MD = REPO / "reference" / "wh40krp_weapon_index.md"
SYSTEM = "WH40K Roleplay"

PAGE = re.compile(r"\[PDF page (\d+)\]")

# --- cell-level patterns (a cell is one column value from the OCR column-dump) --
DASHES = "\u2013\u2014-"                       # en-dash / em-dash / hyphen
# Damage: the anchor. "1d10+2 E", "2d10 R", "5d10+10 E", "1d5-1 I", "2d10\u2020 E".
RE_DAM = re.compile(
    rf"^\d{{1,2}}\s*[dD]\s*\d{{1,3}}(?:\s*[+{DASHES}]\s*\d{{1,3}})?\s*[\u2020*]?\s*"
    rf"[A-Za-z]{{0,3}}\.?$")
# Rate of Fire: three slash-separated tokens of {S, digit, dash}. "S/3/-", "S/2/4".
# The OCR sometimes drops the final token ("S/-/") or slips a space in ("S/3 /-"),
# so tolerate empty tail groups and internal spaces, but demand one real S/digit.
RE_ROF = re.compile(
    rf"^(?=.*[SsBb\d])[SsBb\d\s{DASHES}]*/[SsBb\d\s{DASHES}]*/[SsBb\d\s{DASHES}]*$")
# Range: a distance ("30m", "0.5km", "SBx3 m") or a dash (melee, no range).
RE_RANGE = re.compile(rf"^(?:\d{{1,3}}(?:\.\d)?\s*k?m|SB\s*[x\u00d7]\s*\d\s*m?|[{DASHES}]{{1,3}})$",
                      re.IGNORECASE)
# Reload: "Full", "Half", "2 Full", "2Full", "Free", or a dash.
RE_RLD = re.compile(rf"^(?:\d\s*)?(?:Full|Half|Free)$|^[{DASHES}]$", re.IGNORECASE)
# The OCR sometimes fuses reload + special into one cell ("2 Full Reliable").
RE_RLD_PREFIX = re.compile(r"^(\d?\s*(?:Full|Half|Free))\b[\s,]*(.*)$", re.IGNORECASE)
# Weight cell: a number, optionally with kg. "1.5kg", "4 kg", "55kg", "18", "5.5".
RE_WT = re.compile(r"^\d{1,3}(?:\.\d{1,2})?\s*kg?\.?$|^\d{1,3}(?:\.\d{1,2})?$", re.IGNORECASE)
RE_INT = re.compile(r"^[\d,]{1,7}$")           # pen / clip / cost (may carry commas)
RE_DASH = re.compile(rf"^[{DASHES}]+$")

CLASS_ALT = r"Pistol|Basic|Heavy|Melee|Thrown|Exotic|Mounted|Vehicle"
CLASS_KW = re.compile(rf"\b(?:{CLASS_ALT})\b", re.IGNORECASE)
# A trailing class fragment left on a merged name by a combo class ("Melee/Thrown"
# splits as name + '...Melee/'); strip a class word that ends on a bare separator.
CLASS_FRAG_TAIL = re.compile(rf"[\s,/]*(?:{CLASS_ALT})\s*[/,]\s*$", re.IGNORECASE)

# Pure special-quality adjectives that never appear inside a weapon NAME, so a lone
# one sitting before a name (OCR spill from the previous row) must not be absorbed.
PURE_SPECIAL = {
    "reliable", "accurate", "tearing", "unbalanced", "unwieldy", "primitive",
    "flexible", "defensive", "inaccurate", "unreliable", "felling", "concussive",
    "corrosive", "crippling", "overheats", "overheat", "scatter", "balanced",
}

# Availability rarity ladder (a closed set; the last cell of a ranged/melee row).
RARITIES = {
    "ubiquitous", "abundant", "plentiful", "common", "average", "scarce",
    "rare", "very rare", "extremely rare", "near unique", "unique",
}
RARITY_TAIL = re.compile(
    r"(ubiquitous|abundant|plentiful|common|average|scarce|extremely rare|"
    r"very rare|near unique|unique|rare)\s*$", re.IGNORECASE)

# Deathwatch grades acquisition by Renown, not Availability; a Renown rank can be
# fused onto the previous row's trailing cell ("30/45 Distinguished").
RENOWN = {"respected", "distinguished", "famed", "hero"}

# A weight cell used as a landmark for recovering an OCR-displaced Only War name.
WT_TOKEN = re.compile(r"^\d{1,3}(?:\.\d{1,2})?\s*kg\.?$", re.IGNORECASE)
# Common single-word special qualities — so a lone quality is never mistaken for a
# displaced name (multi-word weapon names stay unambiguous).
SPECIAL_WORDS = {
    "reliable", "accurate", "tearing", "balanced", "unbalanced", "unwieldy",
    "primitive", "flexible", "defensive", "scatter", "blast", "flame", "shocking",
    "toxic", "smoke", "compact", "inaccurate", "storm", "felling", "proven",
    "recharge", "overheat", "overheats", "maximal", "snare", "concussive",
    "devastating", "lance", "graviton", "sanctified", "corrosive", "crippling",
    "hallucinogenic", "power", "razor", "sharp", "ogryn-proof", "twin-linked",
    "reliable,", "spray", "haywire", "indirect", "vengeful",
}

# Column-header / structural words that can never be a weapon name.
HEADER_WORDS = {
    "name", "class", "range", "rof", "dam", "damage", "dmg", "pen", "clip",
    "rld", "reload", "special", "wt", "wt.", "kg", "cost", "availability",
    "req", "renown", "range rof", "pen clip rld", "range dam", "pen special",
    "wt req renown", "s weapons",
}

# Weapon-table titles start a region; the next non-weapon "Table ..." closes it.
# Weapon tables are Ranged / Melee / Thrown / Exotic weapon lists and the
# Grenades / Missiles / Explosives lists (thrown weapons in their own table).
RE_TBL_ANY = re.compile(r"^\s*Table\s+\S", re.IGNORECASE)
RE_TBL_WEAPON = re.compile(
    r"Table\s+\S.*\b(?:Ranged Weapons?|Melee Weapons?|Thrown Weapons?|"
    r"Exotic\b.*Weapons?|Grenades|Missiles|Explosives)\b", re.IGNORECASE)


def _clean_name(s: str) -> str:
    s = s.replace("\ufb01", "fi").replace("\ufb02", "fl")   # OCR ligatures
    s = re.sub(r"\s+", " ", s).strip(" ,\u2013\u2014-\u2020*")
    return s


def _recover_displaced_name(fcells: List[str]) -> Optional[Tuple[str, int]]:
    """Only War's OCR sometimes shifts a weapon's name into its stat row, almost
    always immediately before the weight cell (`...Special, NAME, 2.5kg...`). When
    the backward read yielded no name, look for that kg-adjacent alphabetic cell.
    Returns (name, index-in-fcells) or None. Kept high-precision: a lone special
    quality is never accepted as a name."""
    for k in range(len(fcells) - 1):
        c = fcells[k].strip()
        if not WT_TOKEN.match(fcells[k + 1].strip()):
            continue
        if not c or not c[0].isalpha() or "/" in c:   # names start with a letter
            continue
        low = c.lower()
        if low in RARITIES or RE_RLD.match(c) or RE_DAM.match(c) or RE_ROF.match(c):
            continue
        if re.match(r"^\d?\s*(?:Full|Half)\b", c, re.IGNORECASE):   # merged reload
            continue
        multiword = " " in c.strip()
        singleton_ok = (len(low) >= 5 and
                        all(w not in SPECIAL_WORDS for w in low.split()))
        if (multiword or singleton_ok) and _plausible_name(_clean_name(c)):
            return _clean_name(c), k
    return None


def _plausible_name(s: str) -> bool:
    s = s.strip()
    if not (2 <= len(s) <= 50):
        return False
    if not s[0].isalnum():
        return False
    if s.lower() in HEADER_WORDS or s.lower() in RARITIES:
        return False
    # Section headers are PLURAL ("Las Weapons", "Bolt Weapons"); keep singular
    # weapon names ("Great Weapon", "Astartes Combi-Weapon").
    if re.search(r"weapons$", s, re.IGNORECASE):
        return False
    letters = sum(c.isalpha() for c in s)
    return letters >= 2


def _name_part_ok(t: str) -> bool:
    """Whether a cell can be part of a weapon name read backward. Names begin with
    a letter (or a '(' for a wrapped continuation like '(Godwyn)'), never carry a
    slash (a stat cell), and are not a stat/rarity/Renown/header/section token."""
    t = t.strip()
    if not t or not (t[0].isalpha() or t[0] == "("):
        return False
    if "/" in t:
        return False
    low = t.lower()
    last = low.split()[-1] if low.split() else low
    if low in HEADER_WORDS or low in RARITIES or last in RENOWN:
        return False
    if low.strip(",") in PURE_SPECIAL:          # a special quality spilled from
        return False                            # the previous row, not a name
    if RE_DAM.match(t) or RE_ROF.match(t) or RE_RLD.match(t) or RARITY_TAIL.search(t):
        return False
    if re.search(r"weapons$", low):             # a (plural) section header
        return False
    return True


def _first_num_token(s: str) -> Optional[str]:
    m = re.match(r"^\s*(\d{1,3}(?:\.\d{1,2})?\s*kg?\.?|\d{1,3}(?:\.\d{1,2})?)", s,
                 re.IGNORECASE)
    return m.group(1).strip() if m else (s.strip() or None)


def _is_special_cell(t: str) -> bool:
    """A special-quality cell: has letters, and is not a weight / rarity / reload."""
    t = t.strip()
    if not t or RE_DASH.match(t):
        return False
    if RE_WT.match(t) or RE_RLD.match(t) or RE_INT.match(t):
        return False
    if t.lower() in RARITIES:
        return False
    return any(c.isalpha() for c in t)


@dataclass
class Weapon:
    name: str
    book: str
    page: Optional[int]
    start: int                     # source line (1-based when reported)
    end: int
    system: str = SYSTEM
    weapon_class: Optional[str] = None
    rng: Optional[str] = None
    rof: Optional[str] = None
    damage: Optional[str] = None
    pen: Optional[str] = None
    clip: Optional[str] = None
    reload: Optional[str] = None
    special: Optional[str] = None
    weight: Optional[str] = None
    availability: Optional[str] = None
    cost: Optional[str] = None

    def quick_fields(self) -> int:
        return sum(1 for v in (self.weapon_class, self.rng, self.rof, self.damage,
                               self.pen, self.clip, self.reload, self.special,
                               self.weight, self.availability) if v)


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


def _regions(lines: List[str]) -> List[bool]:
    """Mark lines that fall inside a weapon-table region (from a weapon-table
    title to the next non-weapon 'Table ...' title)."""
    inside = [False] * len(lines)
    open_ = False
    for i, ln in enumerate(lines):
        if RE_TBL_ANY.match(ln):
            open_ = bool(RE_TBL_WEAPON.search(ln))
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


def _identity(cells: List[Cell], p: int) -> Optional[dict]:
    """Read a weapon's identity backward from a Damage anchor at index p.
    Returns dict(ranged, name, class, range, rof, id_start) or None."""
    if p < 2:
        return None
    prev = cells[p - 1].text
    if RE_ROF.match(prev):                        # ranged: ... Range, RoF, Dam
        ranged, rof = True, prev
        if p - 3 < 0:
            return None
        rng = cells[p - 2].text
        class_idx = p - 3
        if not RE_RANGE.match(rng):
            return None
    elif CLASS_KW.search(prev) and not RE_RANGE.match(prev):
        # melee with no Range column (Deathwatch): ... Name, Class, Dam
        ranged, rof, rng = False, None, None
        class_idx = p - 1
    elif RE_RANGE.match(prev):                    # melee with Range: Class, Range, Dam
        ranged, rof, rng = False, None, prev
        class_idx = p - 2
    else:
        return None
    if class_idx < 0:
        return None
    ccell = cells[class_idx].text
    matches = list(CLASS_KW.finditer(ccell))
    if not matches:
        return None
    # If the cell is nothing but class words (a plain or combo class like
    # "Melee, Thrown"), the name lives entirely in the cells before it. Otherwise
    # the cell is a merged Name+Class ("Belasco Dueling Pistol Pistol").
    residue = re.sub(r"[\s,/]+", " ", CLASS_KW.sub("", ccell)).strip(" ,/\u2013\u2014-")
    if residue == "":
        weapon_class = re.sub(r"\s+", " ", ccell).strip(" ,")
        remainder = ""
    else:
        cm = matches[-1]                     # class keyword = last kw in the cell
        weapon_class = cm.group(0).title()
        remainder = ccell[:cm.start()].strip(" ,\u2013\u2014-")
        remainder = CLASS_FRAG_TAIL.sub("", remainder).strip(" ,/\u2013\u2014-")

    name_parts: List[str] = []
    j, steps = class_idx - 1, 0
    while j >= 0 and steps < 3:
        t = cells[j].text.strip()
        if not _name_part_ok(t):
            break
        name_parts.insert(0, t)
        j -= 1
        steps += 1
    id_start = (j + 1) if name_parts else class_idx
    if remainder:
        name_parts.append(remainder)
    name = _clean_name(" ".join(x for x in name_parts if x))
    return {"ranged": ranged, "name": name, "weapon_class": weapon_class,
            "rng": rng, "rof": rof, "id_start": id_start}


def _parse_forward(fcells: List[str], ranged: bool) -> dict:
    """Assign the trailing cells (after Pen) to clip/reload/special/weight/cost/
    availability by TYPE, tolerating omitted-empty cells and space-merges."""
    out: dict = {}
    cells = [c.strip() for c in fcells]
    if not cells:
        return out
    out["pen"] = cells.pop(0)

    # Availability comes off the right: a lone rarity cell, a two-cell rarity
    # ("Extremely"+"Rare"), or a space-merge ("16 kg Scarce").
    if cells:
        if len(cells) >= 2 and (cells[-2] + " " + cells[-1]).lower() in RARITIES:
            out["availability"] = (cells[-2] + " " + cells[-1]).strip()
            cells = cells[:-2]
        elif cells[-1].lower() in RARITIES:
            out["availability"] = cells.pop()
        else:
            m = RARITY_TAIL.search(cells[-1])
            if m and RE_WT.match(cells[-1]) is None:
                out["availability"] = m.group(1)
                head = cells[-1][:m.start()].strip()
                if head:
                    cells[-1] = head
                else:
                    cells.pop()

    rest: List[str]
    if ranged:
        # The reload is its own cell ("Full", "2 Full") OR the OCR fused it onto
        # the special ("2 Full Reliable"); split the prefix off in that case.
        ridx = rld_val = split_special = None
        for k, c in enumerate(cells):
            if RE_RLD.match(c):
                ridx, rld_val = k, c
                break
            m = RE_RLD_PREFIX.match(c)
            if m and m.group(2).strip():
                ridx, rld_val, split_special = k, m.group(1).strip(), m.group(2).strip()
                break
        if ridx is not None:
            out["reload"] = rld_val
            clip = next((c for c in cells[:ridx] if RE_INT.match(c)), None)
            if clip:
                out["clip"] = clip
            rest = cells[ridx + 1:]
            if split_special:
                rest = [split_special] + rest
        else:
            rest = cells
            if rest and RE_INT.match(rest[0]):
                out["clip"] = rest.pop(0)
    else:
        rest = cells

    specials: List[str] = []
    while rest and _is_special_cell(rest[0]):
        specials.append(rest.pop(0).strip(" ,"))
    if specials:
        out["special"] = ", ".join(s for s in specials if s)
    while rest and RE_DASH.match(rest[0]):       # empty special placeholder
        rest.pop(0)
    if rest:
        out["weight"] = _first_num_token(rest.pop(0))
    while rest and RE_DASH.match(rest[0]):
        rest.pop(0)
    if rest and RE_INT.match(rest[0]):
        out["cost"] = rest.pop(0)
    return out


def _detect_weapons_from_cells(
        cells: List[Cell], book: str,
        forward_fn: Callable[[List[str], bool], dict] = _parse_forward,
        sanitize_fn: Optional[Callable[[Weapon], Optional[Weapon]]] = None,
) -> List[Weapon]:
    """The shared anchor/identity/forward pipeline. `forward_fn` assigns the
    trailing cells; `sanitize_fn` (supplement path only) may scrub or reject a
    row. With the defaults this reproduces the original core behaviour exactly —
    the five core sources run through here unchanged."""
    n = len(cells)

    anchors: List[Tuple[int, dict]] = []
    for p in range(n):
        if not (cells[p].region and RE_DAM.match(cells[p].text)):
            continue
        idn = _identity(cells, p)
        if idn is None:                          # keep valid structure; the name
            continue                             # may still be recovered below
        anchors.append((p, idn))

    weapons: List[Weapon] = []
    for a, (p, idn) in enumerate(anchors):
        # forward-run stops at the next weapon's identity (same region) or a cap
        hi = min(p + 1 + 14, n)
        if a + 1 < len(anchors):
            hi = min(hi, anchors[a + 1][1]["id_start"])
        fcells = []
        for q in range(p + 1, hi):
            if not cells[q].region:
                break
            fcells.append(cells[q].text)
        name = idn["name"]
        if not _plausible_name(name):
            rec = _recover_displaced_name(fcells)     # Only War displaced name
            if rec is None:
                continue
            name, k = rec
            fcells = fcells[:k] + fcells[k + 1:]       # keep it out of the stats
        fwd = forward_fn(fcells, idn["ranged"])
        w = Weapon(name=name, book=book, page=cells[p].page,
                   start=cells[idn["id_start"]].line + 1, end=cells[p].line + 8,
                   weapon_class=idn["weapon_class"], rng=idn["rng"],
                   rof=idn["rof"], damage=cells[p].text)
        w.pen = fwd.get("pen")
        w.clip = fwd.get("clip")
        w.reload = fwd.get("reload")
        w.special = fwd.get("special")
        w.weight = fwd.get("weight")
        w.availability = fwd.get("availability")
        w.cost = fwd.get("cost")
        if sanitize_fn is not None:
            scrubbed = sanitize_fn(w)
            if scrubbed is None:                  # structurally broken row → skip
                continue
            w = scrubbed
        weapons.append(w)

    # one row per (name, book): keep the richest, then the first seen.
    best: Dict[str, Weapon] = {}
    for w in weapons:
        k = w.name.lower()
        cur = best.get(k)
        if cur is None or w.quick_fields() > cur.quick_fields():
            best[k] = w
    return sorted(best.values(), key=lambda w: w.start)


def detect_weapons(lines: List[str], pages: List[int], book: str) -> List[Weapon]:
    region = _regions(lines)
    cells = _build_cells(lines, pages, region)
    return _detect_weapons_from_cells(cells, book)


# ---------------------------------------------------------------------------
# SUPPLEMENT PATH — the weapon-bearing 40K RP splatbooks.
#
# The supplements were OCR'd in the SAME column-dump format as the cores, but
# their scans are rougher, so three things defeat the core detector and are
# handled here ADDITIVELY (the five core sources never run through this path):
#   1. Region titles name the weapon FAMILY ("Las and SP Weapons", "Xenos
#      Weapons", "Necron Weapons", a bare "Weapons"), not "... Ranged Weapons",
#      and OCR sometimes mangles MELEE ("ITIELEE"). `_regions_supp` opens on any
#      "Table ...: <family> Weapon(s)" while still excluding the weapon-adjacent
#      NON-list tables (Weapon Upgrades / Pattern / Emplacements / Attributes).
#   2. Adjacent stat cells are space-fused onto one physical line
#      ("100m S/-/-", "S/3/- 1d10+5 X", "12 kg Scarce"). `_defuse_supp_line`
#      re-splits them at high-confidence token boundaries (identity fields only,
#      so a weapon NAME — which never holds a range/RoF/damage token — is safe).
#   3. Rows carry dash / "N/A" placeholders and are followed by footnote prose
#      that the core's type-based, read-from-both-ends forward pass mishandles.
#      `_parse_forward_supp` walks the trailing columns strictly LEFT-TO-RIGHT
#      and stops after Availability; `_sanitize_supp` then scrubs or rejects
#      anything still malformed so no fabricated field ever reaches the index.
# ---------------------------------------------------------------------------

# A weapon-adjacent table whose title carries one of these words is NOT a
# weapon list (upgrades, customisation patterns, emplacements, daemon-weapon
# attribute menus, ammunition-only, etc.) and must not open a region.
RE_TBL_NOT_WEAPON_LIST = re.compile(
    r"\b(?:Upgrades?|Pattern|Emplacements?|Attributes?|Modif\w*|Qualit\w+|"
    r"Training|Advances?|Costs?|Positive|Negative|Tips|Ammunition)\b",
    re.IGNORECASE)


def _title_opens_supp_region(ln: str) -> bool:
    if re.search(r"\b(?:Grenades|Missiles|Explosives)\b", ln, re.IGNORECASE):
        return True                              # thrown-weapon lists (as cores)
    if re.search(r"Weapons?\b", ln, re.IGNORECASE) and \
            not RE_TBL_NOT_WEAPON_LIST.search(ln):
        return True                              # any "<family> Weapon(s)" list
    return False


def _regions_supp(lines: List[str]) -> List[bool]:
    inside = [False] * len(lines)
    open_ = False
    for i, ln in enumerate(lines):
        if RE_TBL_ANY.match(ln):
            open_ = _title_opens_supp_region(ln)
        inside[i] = open_
    return inside


_SUPP_RANGE_TOK = r"(?:\d{1,3}(?:\.\d)?\s?k?m|SB\s?[x\u00d7]\s?\d\s?m?)"
_SUPP_ROF_TOK = rf"[SBsb\d]\s?/\s?[SBsb\d{DASHES}]*\s?/\s?[SBsb\d{DASHES}]*"
_SUPP_DAM_START = r"\d{1,2}\s?[dD]\s?\d"
_SUPP_WT_TOK = r"\d{1,3}(?:\.\d{1,2})?\s?kg\b"


def _defuse_supp_line(ln: str) -> str:
    """Insert tab boundaries between space-fused stat tokens on one physical
    line. High-precision: only the Range|RoF, RoF|Damage, x|Weight and
    Weight|Availability seams — each anchored on an unmistakable stat token, so
    a real weapon name is never split."""
    s = ln
    s = re.sub(rf"({_SUPP_RANGE_TOK})\s+(?={_SUPP_ROF_TOK})", "\\1\t", s)
    s = re.sub(rf"({_SUPP_ROF_TOK})\s+(?={_SUPP_DAM_START})", "\\1\t", s)
    s = re.sub(rf"(?<=\D)\s+(?={_SUPP_WT_TOK})", "\t", s)          # <x> | Weight
    s = re.sub(rf"({_SUPP_WT_TOK})\s+(?=[A-Z(])", "\\1\t", s)      # Weight | Avail
    return s


def _norm_supp_cell(s: str) -> str:
    """A rarity cell carrying only a trailing footnote dagger ("Scarce†") is
    normalised to the bare rarity, so the identity read recognises it as a stat
    (not a name fragment) and the availability parse still matches it."""
    base = s.rstrip("†‡*").rstrip()
    if base != s and base.lower() in RARITIES:
        return base
    return s


def _build_cells_supp(lines: List[str], pages: List[int], region: List[bool]) -> List[Cell]:
    cells: List[Cell] = []
    for i, ln in enumerate(lines):
        if PAGE.search(ln):
            continue
        src = _defuse_supp_line(ln) if region[i] else ln
        for piece in src.split("\t"):
            s = piece.strip()
            if s:
                cells.append(Cell(_norm_supp_cell(s), i, pages[i], region[i]))
    return cells


RE_CLIP_INT = re.compile(r"^(\d{1,4})[\u2020\u2021*]*$")   # clip: digits + daggers
NA_TOK = re.compile(rf"^(?:n\s*/?\s*a|[{DASHES}]+)$", re.IGNORECASE)


def _clip_int(t: str) -> Optional[str]:
    m = RE_CLIP_INT.match(t.strip())
    return m.group(1) if m else None


def _supp_special_stop(t: str) -> bool:
    """True at the cell that ends a special-quality run: a weight, a rarity /
    Renown cell, a footnote marker, or a prose sentence (OCR over-read tail)."""
    t = t.strip()
    if RE_WT.match(t):
        return True
    low = t.lower().rstrip("\u2020\u2021*").strip()
    if low in RARITIES or low in RENOWN:
        return True
    if t[:1] in "\u2020\u2021*":
        return True
    if re.search(r"\bSee page\b|Rulebook\b", t, re.IGNORECASE):
        return True
    if len(t.split()) >= 8:                       # a sentence, not a stat cell
        return True
    return False


def _parse_forward_supp(fcells: List[str], ranged: bool) -> dict:
    """Assign the trailing cells strictly left-to-right in column order —
    Pen, Clip, Rld, Special.., Wt, [Cost], Availability — treating dash / N/A
    as empty-cell placeholders, and STOPPING after Availability so the footnote
    prose that follows the last row of a table is never absorbed."""
    out: dict = {}
    cells = [c.strip() for c in fcells if c.strip()]
    if not cells:
        return out
    out["pen"] = cells.pop(0)
    if ranged:
        if cells:                                 # Clip
            ci = _clip_int(cells[0])
            if ci is not None:
                out["clip"] = ci
                cells.pop(0)
            elif NA_TOK.match(cells[0]):
                cells.pop(0)                      # empty clip
        if cells:                                 # Reload
            if NA_TOK.match(cells[0]):
                cells.pop(0)                      # empty reload
            elif RE_RLD.match(cells[0]):
                out["reload"] = cells.pop(0)
            else:
                m = RE_RLD_PREFIX.match(cells[0])
                if m and m.group(2).strip():      # "2 Full Reliable" fused
                    out["reload"] = m.group(1).strip()
                    cells[0] = m.group(2).strip()
    specials: List[str] = []                      # Special (ranged and melee)
    while cells and _is_special_cell(cells[0]) and not _supp_special_stop(cells[0]):
        specials.append(cells.pop(0).strip(" ,"))
        if len(specials) >= 8:
            break
    if specials:
        out["special"] = ", ".join(s for s in specials if s)
    while cells and NA_TOK.match(cells[0]):
        cells.pop(0)                              # empty special placeholder
    if cells and RE_WT.match(cells[0]):           # Weight
        out["weight"] = _first_num_token(cells.pop(0))
    while cells and NA_TOK.match(cells[0]):
        cells.pop(0)
    if cells and RE_INT.match(cells[0]):          # Cost (optional)
        out["cost"] = cells.pop(0)
    if cells:                                     # Availability, then STOP
        two = (cells[0] + " " + cells[1]).strip() if len(cells) >= 2 else ""
        if two and two.lower().rstrip("\u2020*") in RARITIES:
            out["availability"] = two
        elif cells[0].lower().rstrip("\u2020*") in RARITIES or cells[0].lower() in RENOWN:
            out["availability"] = cells[0].rstrip("\u2020*")
        else:
            m = RARITY_TAIL.search(cells[0])
            if m and not RE_WT.match(cells[0]):
                out["availability"] = m.group(1)
    return out


# Leading name tokens that never begin a weapon name — column labels, rarity
# words, Renown ranks, and the bare quality word "Special" — safe to strip off
# the FRONT of a name when OCR spilled them in from an adjacent cell/row.
_NAME_LEAD_DROP = (set(HEADER_WORDS) | {r.split()[0] for r in RARITIES} |
                   set(RENOWN) | {"rare", "unique", "special", "req", "renown"})
# Header labels that must NEVER survive inside a name (a fused-header leak).
_NAME_HARD_HEADER = {"availability", "reload", "rof", "rld", "clip", "cost"}
# A leading special quality with a parenthetical VALUE ("Blast (3) (in addition)")
# spilled from the previous row — a real name never carries a "(digit)".
_NAME_LEAD_SPECIAL = re.compile(r"^(?:[A-Za-z][\w'’-]*\s*\(\d+\)(?:\s*\([^)]*\))?[\s,]*)+")
# A trailing combo-class fragment: "... Melee or" (from a "Melee or Thrown"
# class), or a bare trailing class word that can never end a real weapon name.
_NAME_TAIL_COMBO = re.compile(rf"[\s,]+(?:{CLASS_ALT})\s+or$", re.IGNORECASE)
_NAME_TAIL_CLASS = re.compile(r"[\s,]+(?:Basic|Melee|Thrown|Exotic)$", re.IGNORECASE)
_CLASS_WORDS_LOW = {c.lower() for c in CLASS_ALT.split("|")}


def _sanitize_supp(w: Weapon) -> Optional[Weapon]:
    """Scrub a supplement row; return None to reject it (soft skip). Never
    invents a value — a field that cannot be trusted is blanked, not guessed."""
    # name: strip a leading special-with-value fragment spilled from the row above
    w.name = _NAME_LEAD_SPECIAL.sub("", w.name).strip()
    # name: strip a leading run of header/rarity/quality junk (OCR spill)
    toks = w.name.split()
    i = 0
    while i < len(toks):
        low = toks[i].lower().strip(",").strip("\u2020\u2021*").strip()
        if low in _NAME_LEAD_DROP or toks[i].endswith(","):
            i += 1
            continue
        break
    name = _clean_name(" ".join(toks[i:]))
    if name:
        w.name = name
    # name: strip a trailing combo-class fragment / bare non-name class word
    w.name = _clean_name(_NAME_TAIL_CLASS.sub("", _NAME_TAIL_COMBO.sub("", w.name)))
    if not _plausible_name(w.name) or w.name.lower() in _CLASS_WORDS_LOW:
        return None
    if any(t.lower().strip(",").strip("\u2020\u2021*") in _NAME_HARD_HEADER
           for t in w.name.split()):
        return None                               # fused-header leak → soft skip
    # A "damage" that is really a randomised RANGE ("3d10m", an Ork throw range)
    # mis-anchored as the damage cell — a real 40K damage never ends in "m".
    if w.damage and re.search(r"[dD]\s?\d{1,3}\s?m$", w.damage.strip()):
        return None
    if w.weapon_class:                             # tidy stray dagger/dash on class
        w.weapon_class = w.weapon_class.rstrip(" †‡*–—-").strip() or w.weapon_class
    # a damage-type letter split off into Pen ("1d10+4" | pen "E") → restore it
    if w.pen and re.match(r"^[eirxEIRX]$", w.pen.strip()) and w.damage and \
            not re.search(r"[A-Za-z]$", w.damage.strip().rstrip("\u2020*")):
        w.damage = w.damage.strip() + " " + w.pen.strip().upper()
        w.pen = None
    if w.pen is not None:                          # Pen is an integer, or blank
        pc = w.pen.strip().rstrip("\u2020\u2021*").strip()
        w.pen = pc if RE_INT.match(pc) else None
    if w.clip is not None and not RE_INT.match(w.clip.strip()):
        w.clip = None
    if w.weight is not None and not RE_WT.match(w.weight.strip()):
        w.weight = None
    if w.availability is not None:                 # a known rarity / Renown rank
        av = w.availability.strip().rstrip("\u2020*").strip()
        w.availability = av if (av.lower() in RARITIES or av.lower() in RENOWN) else None
    if w.special is not None:                      # drop any absorbed footnote
        sp = re.sub(r"\s+", " ", w.special).strip(" ,\u2013\u2014-")
        cut = re.search(r"(See page|Rulebook)", sp, re.IGNORECASE)
        if cut:
            sp = sp[:cut.start()].strip(" ,")
        w.special = sp or None
    return w


# A damage cell OCR'd WITHOUT its trailing type letter, and the lone type letter
# (E/I/R/X = Energy/Impact/Rending/eXplosive) OCR frequently drops onto the next
# line. Likewise a weight number and its "kg" unit are sometimes split. Both get
# stitched back before parsing so the trailing columns don't shift by one cell.
RE_DAM_NOTYPE = re.compile(
    rf"^\d{{1,2}}\s*[dD]\s*\d{{1,3}}(?:\s*[+{DASHES}]\s*\d{{1,3}})?\s*[†*]?$")
RE_DAM_TYPE = re.compile(r"^[EIRXeirx]\.?$")
RE_KG_UNIT = re.compile(r"^kg\.?$", re.IGNORECASE)
RE_BARE_NUM = re.compile(r"^\d{1,3}(?:\.\d{1,2})?$")


def _stitch_supp_cells(cells: List[Cell]) -> List[Cell]:
    out: List[Cell] = []
    k = 0
    while k < len(cells):
        c = cells[k]
        nxt = cells[k + 1] if k + 1 < len(cells) else None
        if (nxt is not None and c.region and nxt.region and
                RE_DAM_NOTYPE.match(c.text) and RE_DAM_TYPE.match(nxt.text)):
            out.append(Cell(f"{c.text.strip()} {nxt.text.strip().upper().rstrip('.')}",
                            c.line, c.page, c.region))
            k += 2
        elif (nxt is not None and c.region and nxt.region and
                RE_BARE_NUM.match(c.text) and RE_KG_UNIT.match(nxt.text)):
            out.append(Cell(f"{c.text.strip()} kg", c.line, c.page, c.region))
            k += 2
        else:
            out.append(c)
            k += 1
    return out


def detect_weapons_supp(lines: List[str], pages: List[int], book: str) -> List[Weapon]:
    region = _regions_supp(lines)
    cells = _stitch_supp_cells(_build_cells_supp(lines, pages, region))
    return _detect_weapons_from_cells(cells, book, _parse_forward_supp, _sanitize_supp)


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[Weapon]]] = {
    "wh40krp": detect_weapons,
    "wh40krp_supp": detect_weapons_supp,
}


@dataclass
class Source:
    key: str
    book: str
    path: Path
    citation: str
    detector: str
    coverage: str = "pending"
    lines: List[str] = field(default_factory=list)
    weapons: List[Weapon] = field(default_factory=list)


_40K = Path("Warhammer/40K Roleplay")
SOURCES: List[Source] = [
    Source("dh-core", "Dark Heresy — Core Rulebook",
           _40K / "Dark Heresy/Rulebooks/Dark Heresy - Core Rulebook.pdf.md",
           "Dark Heresy Core Rulebook (FFG, WH40K Roleplay), Armoury", "wh40krp"),
    Source("rt-core", "Rogue Trader — Core Rulebook",
           _40K / "Rogue Trader/Rulebooks/Rogue Trader - Core Rulebook (updated with 1.4 errata).md",
           "Rogue Trader Core Rulebook, 1.4 errata (FFG, WH40K Roleplay), Armoury", "wh40krp"),
    Source("dw-core", "Deathwatch — Core Rulebook",
           _40K / "Deathwatch/Rulebooks/Deathwatch - Core Rulebook.md",
           "Deathwatch Core Rulebook (FFG, WH40K Roleplay), Armoury "
           "(uses Req/Renown, not Cost/Availability)", "wh40krp"),
    Source("ow-core", "Only War — Core Rulebook",
           _40K / "Only War/Rulebooks/Only War - Core Rulebook.md",
           "Only War Core Rulebook (FFG, WH40K Roleplay), Armoury", "wh40krp"),
    Source("bc-core", "Black Crusade — Core Rulebook",
           _40K / "Black Crusade/Rulebooks/Black Crusade - Core Rulebook.md",
           "Black Crusade Core Rulebook (FFG, WH40K Roleplay), Armoury", "wh40krp"),

    # --- SUPPLEMENTS (added later; the wh40krp_supp detector) ----------------
    # Dark Heresy line
    Source("dh-inquisitor", "Dark Heresy — The Inquisitor's Handbook",
           _40K / "Dark Heresy/Rulebooks/Dark Heresy - The Inquisitor's Handbook.md",
           "Dark Heresy: The Inquisitor's Handbook (FFG, WH40K Roleplay), Armoury",
           "wh40krp_supp"),
    Source("dh-radicals", "Dark Heresy — The Radical's Handbook",
           _40K / "Dark Heresy/Rulebooks/Dark Heresy - The Radical's Handbook.md",
           "Dark Heresy: The Radical's Handbook (FFG, WH40K Roleplay), Armoury",
           "wh40krp_supp"),
    Source("dh-lathe", "Dark Heresy — The Lathe Worlds",
           _40K / "Dark Heresy/Rulebooks/Dark Heresy - The Lathe Worlds.md",
           "Dark Heresy: The Lathe Worlds (FFG, WH40K Roleplay), Armoury", "wh40krp_supp"),
    Source("dh-ascension", "Dark Heresy — Ascension",
           _40K / "Dark Heresy/Rulebooks/Dark Heresy - Ascension.md",
           "Dark Heresy: Ascension (FFG, WH40K Roleplay), Armoury", "wh40krp_supp"),
    Source("dh-blood", "Dark Heresy — Blood of Martyrs",
           _40K / "Dark Heresy/Rulebooks/Dark Heresy - Blood of Martyrs.md",
           "Dark Heresy: Blood of Martyrs (FFG, WH40K Roleplay), Armoury", "wh40krp_supp"),
    # Rogue Trader line
    Source("rt-storm", "Rogue Trader — Into the Storm (Explorer's Handbook)",
           _40K / "Rogue Trader/Rulebooks/Rogue Trader - Into The Storm  - The Explorer's Handbook.md",
           "Rogue Trader: Into the Storm (FFG, WH40K Roleplay), Armoury", "wh40krp_supp"),
    Source("rt-hostile", "Rogue Trader — Hostile Acquisitions",
           _40K / "Rogue Trader/Rulebooks/Rogue Trader - Hostile Acquisitions.md",
           "Rogue Trader: Hostile Acquisitions (FFG, WH40K Roleplay), Armoury", "wh40krp_supp"),
    # Deathwatch line  (armoury grades by Req/Renown, not Cost/Availability)
    Source("dw-rites", "Deathwatch — Rites of Battle",
           _40K / "Deathwatch/Rulebooks/Deathwatch - Rites of Battle.md",
           "Deathwatch: Rites of Battle (FFG, WH40K Roleplay), Armoury", "wh40krp_supp"),
    Source("dw-founding", "Deathwatch — First Founding",
           _40K / "Deathwatch/Rulebooks/Deathwatch - First Founding.md",
           "Deathwatch: First Founding (FFG, WH40K Roleplay), Armoury", "wh40krp_supp"),
    Source("dw-honour", "Deathwatch — Honour the Chapter",
           _40K / "Deathwatch/Rulebooks/Deathwatch - Honour the Chapter.md",
           "Deathwatch: Honour the Chapter (FFG, WH40K Roleplay), Armoury", "wh40krp_supp"),
    # Only War line
    Source("ow-hammer", "Only War — Hammer of the Emperor",
           _40K / "Only War/Rulebooks/Only War - Hammer of The Emperor.md",
           "Only War: Hammer of the Emperor (FFG, WH40K Roleplay), Armoury", "wh40krp_supp"),
    # Black Crusade line
    Source("bc-blood", "Black Crusade — Tome of Blood",
           _40K / "Black Crusade/Rulebooks/Black Crusade - Tome of Blood.md",
           "Black Crusade: Tome of Blood (FFG, WH40K Roleplay), Armoury", "wh40krp_supp"),
    Source("bc-excess", "Black Crusade — Tome of Excess",
           _40K / "Black Crusade/Rulebooks/Black Crusade - Tome of Excess.md",
           "Black Crusade: Tome of Excess (FFG, WH40K Roleplay), Armoury", "wh40krp_supp"),
    Source("bc-fate", "Black Crusade — Tome of Fate",
           _40K / "Black Crusade/Rulebooks/Black Crusade - Tome of Fate.md",
           "Black Crusade: Tome of Fate (FFG, WH40K Roleplay), Armoury", "wh40krp_supp"),
]


def _fresh_sources() -> List[Source]:
    return [Source(*(getattr(s, k) for k in ("key", "book", "path", "citation", "detector")))
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
            src.weapons = DETECTORS[src.detector](src.lines, pages, src.book)
            src.coverage = f"ok — {len(src.weapons)} weapons from {path.name}"

    def all_weapons(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for w in src.weapons:
                yield src, w

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, w in self.all_weapons(book):
            nm = w.name.lower()
            if nm == q:
                exact.append((src, w))
            elif q in nm:
                partial.append((src, w))
        return exact if exact else partial


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# WH40K ROLEPLAY WEAPON INDEX — The New Path",
        "",
        "**Generated by `scripts/wh40krp_weapon_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** These are **Warhammer 40,000 Roleplay** weapons —",
        "the Fantasy Flight Games d100 line (Dark Heresy / Rogue Trader /",
        "Deathwatch / Only War / Black Crusade). Every row is stamped",
        f"`system: {SYSTEM}`; a 40K RP weapon is SOURCE MATERIAL for the",
        "system-translator skill, not campaign RAW. The Armoury stat tables were",
        "OCR'd as column-dumps; a field left `—` is one the OCR did not cleanly",
        "yield. Use `--export \"NAME\"` for the translator packet.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.weapons)
        parsed_well += sum(1 for w in src.weapons if w.quick_fields() >= 6)
        sources_out.append({"key": src.key, "book": src.book, "system": SYSTEM,
                            "citation": src.citation, "coverage": src.coverage,
                            "weapons": [asdict(w) for w in src.weapons]})
        md.append(f"## {src.book} — {len(src.weapons)} weapons  *(system: {SYSTEM})*")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.weapons:
            md.append("| Weapon | Class | Range | RoF | Damage | Pen | Clip | "
                      "Reload | Special | Wt | Avail | Page |")
            md.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
            for w in src.weapons:
                md.append(
                    f"| {w.name} | {w.weapon_class or '—'} | {w.rng or '—'} | "
                    f"{w.rof or '—'} | {w.damage or '—'} | {w.pen or '—'} | "
                    f"{w.clip or '—'} | {w.reload or '—'} | {w.special or '—'} | "
                    f"{w.weight or '—'} | {w.availability or '—'} | "
                    f"{w.page if w.page is not None else '—'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/wh40krp_weapon_harvest.py",
                    "system": SYSTEM, "corpus": str(corpus.base),
                    "total_weapons": total, "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 8:
        print(f"'{name}' matches {len(hits)} weapons; narrow with --book or the exact name:")
        for src, w in hits[:20]:
            print(f"  {w.name}   [{w.book}, p.{w.page}]")
        return 1
    packets = []
    for src, w in hits:
        lo = max(0, w.start - 1)
        body = [ln for ln in src.lines[lo:w.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "wh40krp-weapon-for-translation",
            "instructions": ("A Warhammer 40,000 Roleplay weapon (system: "
                             f"{SYSTEM}). Feed to the system-translator skill for "
                             "the paired 3.5e AND GURPS treatment. The raw_block "
                             "is OCR text from a column-dump table."),
            "name": w.name, "system": SYSTEM,
            "source": {"book": w.book, "pdf_page": w.page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [w.start, w.end], "citation": src.citation},
            "parsed": {k: v for k, v in asdict(w).items()
                       if k in ("weapon_class", "rng", "rof", "damage", "pen",
                                "clip", "reload", "special", "weight",
                                "availability", "cost") and v},
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
# A column-dump fixture exercising: a clean ranged row, a merged Name+Class row
# (Rogue Trader style), a wrapped two-line name (Deathwatch style), and a melee
# row with a space-merged weight+availability (Black Crusade style).
FIXTURE = """## [PDF page 100]
Table 5-7: Ranged Weapons
Las Weapons
Name
Class
Range
RoF
Dam
Pen
Clip
Rld
Special
Wt
Cost
Availability
Lasgun
Basic
100m
S/3/\u2013
1d10+3 E
0
60
Full
Reliable
4kg
75
Common
Belasco Dueling Pistol Pistol
45m
S/\u2013/\u2013
1d10+5 E
4
1
Full
Accurate
1.5
250
Very Rare
Astartes Bolter
(Godwyn)
Basic
100m
S/2/4
2d10+5 X
5
28
Full
Tearing
18
75
Common
Table 5-9: Melee Weapons
Chain Weapons
Name
Class
Range
Dam
Pen
Special
Wt
Cost
Availability
Chainsword
Melee
\u2013
1d10+2 R
2
Tearing, Balanced
6 kg
250
Average
Arm-mounted
Chainblade
Melee
\u2013
1d10+2 R
3
Tearing
5 kg Rare
## [PDF page 101]
Table 5-11: Ammo
Name
"""


# A supplement fixture exercising the wh40krp_supp path: a FAMILY-named weapon
# table title ("Las and SP Weapons"), a split damage-type letter ("1d10+4" then
# "E" on the next line) with a fused reload+special ("3 Full Unstable") and a
# dagger-suffixed rarity ("Scarce†"), and a Necron-style table with a fused
# "Range RoF" header and dash clip/reload placeholders.
SUPP_FIXTURE = """## [PDF page 200]
Table 3-6: Las and SP Weapons
Las Weapons
Name
Class
Range
RoF
Damage
Pen
Clip
Reload
Special
Wt.
Availability
Accatran-pattern
MkIV Lasgun
Basic
80m
S/3/–
1d10+3 E
0
60
Full
Reliable
4 kg
Average
Table 6-1: Xenos Weapons
Ranged Weapons
Name
Class
Range
Rof
Dam
Pen
Clip
Rld
Special
Wt
Cost
Availability
Morgauth
Burn Caster
Basic
20m
S/3/–
1d10+4
E
9
12
3 Full Unstable
4 kg
2,750
Scarce†
Table 3-4: Necron Weapons
Ranged Weapons
Name
Class
Range RoF
Dam
Pen Clip Rld
Special
Wt.
Availability
Gauss Cannon
Heavy
100m
S/4/6
1d10+12 E
5
–
–
Gauss†
35kg
Near Unique
## [PDF page 201]
Table 3-7: Weapon Upgrades
Name
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    lines = FIXTURE.splitlines()
    ws = detect_weapons(lines, _pages_for(lines), "Fixture Core Rulebook")
    names = [w.name for w in ws]
    want = ["Lasgun", "Belasco Dueling Pistol", "Astartes Bolter (Godwyn)",
            "Chainsword", "Arm-mounted Chainblade"]
    if names != want:
        failures.append(f"fixture detected {names}, wanted {want}")
    else:
        by = {w.name: w for w in ws}
        lg = by["Lasgun"]
        got = (lg.weapon_class, lg.rng, lg.rof, lg.damage, lg.pen, lg.clip,
               lg.reload, lg.special, lg.weight, lg.availability, lg.cost)
        exp = ("Basic", "100m", "S/3/\u2013", "1d10+3 E", "0", "60", "Full",
               "Reliable", "4kg", "Common", "75")
        if got != exp:
            failures.append(f"Lasgun parsed {got}, wanted {exp}")
        if lg.system != SYSTEM:
            failures.append(f"system must be {SYSTEM!r}")

        bel = by["Belasco Dueling Pistol"]
        if bel.weapon_class != "Pistol":
            failures.append(f"Belasco class {bel.weapon_class!r}, wanted 'Pistol' "
                            f"(merged Name+Class must split)")
        if bel.availability != "Very Rare" or bel.weight != "1.5":
            failures.append(f"Belasco wt/avail ({bel.weight!r},{bel.availability!r}),"
                            f" wanted ('1.5','Very Rare')")

        cs = by["Chainsword"]
        got = (cs.weapon_class, cs.rof, cs.damage, cs.pen, cs.special, cs.weight,
               cs.availability)
        exp = ("Melee", None, "1d10+2 R", "2", "Tearing, Balanced", "6 kg", "Average")
        if got != exp:
            failures.append(f"Chainsword parsed {got}, wanted {exp} (melee = no RoF)")

        acb = by["Arm-mounted Chainblade"]
        if acb.availability != "Rare" or acb.weight != "5 kg":
            failures.append(f"Arm-mounted Chainblade wt/avail "
                            f"({acb.weight!r},{acb.availability!r}), wanted "
                            f"('5 kg','Rare') (space-merged weight+availability)")

    # No weapon anchor may be harvested from outside a weapon-table region.
    stray = detect_weapons("The blast deals 2d10+5 X to all nearby.".splitlines(),
                           [0], "Prose")
    if stray:
        failures.append(f"prose produced phantom weapons: {[w.name for w in stray]}")

    # --- SUPPLEMENT fixture: the wh40krp_supp path -------------------------
    slines = SUPP_FIXTURE.splitlines()
    sws = detect_weapons_supp(slines, _pages_for(slines), "Fixture Supplement")
    snames = [w.name for w in sws]
    swant = ["Accatran-pattern MkIV Lasgun", "Morgauth Burn Caster", "Gauss Cannon"]
    if snames != swant:
        failures.append(f"supp fixture detected {snames}, wanted {swant}")
    else:
        sby = {w.name: w for w in sws}
        acc = sby["Accatran-pattern MkIV Lasgun"]       # family-titled region
        if (acc.weapon_class, acc.damage, acc.clip, acc.reload, acc.special,
                acc.weight, acc.availability) != \
                ("Basic", "1d10+3 E", "60", "Full", "Reliable", "4 kg", "Average"):
            failures.append(f"supp Accatran parsed "
                            f"{(acc.weapon_class, acc.damage, acc.clip, acc.reload, acc.special, acc.weight, acc.availability)!r}")
        mor = sby["Morgauth Burn Caster"]               # split damage-type letter
        got = (mor.weapon_class, mor.damage, mor.pen, mor.clip, mor.reload,
               mor.special, mor.weight, mor.cost, mor.availability)
        exp = ("Basic", "1d10+4 E", "9", "12", "3 Full", "Unstable", "4 kg",
               "2,750", "Scarce")
        if got != exp:
            failures.append(f"supp Morgauth parsed {got}, wanted {exp}")
        gc = sby["Gauss Cannon"]                         # fused header + dash cells
        if (gc.weapon_class, gc.rng, gc.rof, gc.damage, gc.pen, gc.clip,
                gc.reload, gc.weight, gc.availability) != \
                ("Heavy", "100m", "S/4/6", "1d10+12 E", "5", None, None, "35kg",
                 "Near Unique"):
            failures.append(f"supp Gauss Cannon parsed "
                            f"{(gc.weapon_class, gc.rng, gc.rof, gc.damage, gc.pen, gc.clip, gc.reload, gc.weight, gc.availability)!r}")
        if any(w.system != SYSTEM for w in sws):
            failures.append("supp fixture weapon missing system stamp")

    if base.is_dir() and any((base / s.path).exists() for s in SOURCES):
        corpus = Corpus(base, _fresh_sources())
        by_key = {s.key: s for s in corpus.sources}
        # HARD CONSTRAINT: the five cores stay byte-count exact (53/81/31/62/100).
        core_expect = {"dh-core": 53, "rt-core": 81, "dw-core": 31,
                       "ow-core": 62, "bc-core": 100}
        core_total = 0
        for key, exp_n in core_expect.items():
            src = by_key.get(key)
            if src is None or not (base / src.path).exists():
                continue
            core_total += len(src.weapons)
            if len(src.weapons) != exp_n:
                failures.append(f"CORE PRESERVATION: {key} yielded "
                                f"{len(src.weapons)} weapons; must be exactly {exp_n}")
        if core_total and core_total != 327:
            failures.append(f"CORE PRESERVATION: cores total {core_total}, must be 327")
        supp_total = sum(len(s.weapons) for s in corpus.sources
                         if s.key not in core_expect)
        if core_total == 327 and supp_total < 100:
            failures.append(f"only {supp_total} supplement weapons harvested; "
                            f"expected the splatbooks to add well over 100")
        for wpn in ("Lasgun", "Bolt Pistol", "Chainsword"):
            if not corpus.find(wpn):
                failures.append(f"known weapon not found in live corpus: {wpn}")
        lg = corpus.find("Lasgun")
        if lg and lg[0][1].damage is None:
            failures.append("live Lasgun has no damage parsed")
        # every live weapon must carry the system stamp and a damage value
        bad = [w.name for _, w in corpus.all_weapons() if w.system != SYSTEM]
        if bad:
            failures.append(f"{len(bad)} live weapons missing system stamp")
        nodmg = sum(1 for _, w in corpus.all_weapons() if not w.damage)
        if nodmg:
            failures.append(f"{nodmg} live weapons missing damage (anchor invariant)")
        # a specific SUPPLEMENT weapon, harvested live, parses correctly
        hits = corpus.find("Hades Assault Flamer")
        if not hits:
            failures.append("supplement weapon 'Hades Assault Flamer' not found live")
        else:
            hw = hits[0][1]
            if (hw.weapon_class, hw.damage) != ("Basic", "1d10+4 E"):
                failures.append(f"live Hades Assault Flamer parsed "
                                f"{(hw.weapon_class, hw.damage)!r}, wanted "
                                f"('Basic', '1d10+4 E')")
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
        found = sorted({(w.name, w.book, w.page or -1, w.damage or "—")
                        for _, w in corpus.all_weapons(args.book) if q in w.name.lower()})
        for name, bk, page, dam in found:
            loc = bk if page < 0 else f"{bk}, p.{page}"
            print(f"  {name}   [{dam}; {loc}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.weapons for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.weapons):4d} weapons" if src.weapons else "   0 weapons"
        print(f"  {src.book:34s} {status}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} WH40K Roleplay weapons across "
          f"{sum(1 for s in corpus.sources if s.weapons)} book(s); "
          f"{parsed_well} with 6+ fields parsed. (system: {SYSTEM})")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
