#!/usr/bin/env python3
"""wfrp_gear_harvest.py — collate WFRP 2e ARMS & ARMOUR (system: WFRP).

THE PROCESS (Chad, opening the Warhammer Fantasy Roleplay shelf): other GAME
SYSTEMS are welcome in the reference layer AS LONG AS each is clearly LABELLED
by system — the translator tools convert them into the hybrid's 3.5e + GURPS.
This is the **Warhammer Fantasy Roleplay** (2nd edition, Black Industries /
Green Ronin d100) WEAPON + ARMOUR index. Every row is one weapon or one piece
of armour, stamped `"system": "WFRP"`, tagged `category: "weapon"|"armour"`.

    reference/wfrp_gear_index.json — every row: name, category, and the
                                     mechanical stats the book states, cited to
                                     book + PDF page + table.
    reference/wfrp_gear_index.md   — the same, for human eyes.

`--export` emits a translator-ready packet (a WFRP gear row the system-translator
skill converts to the 3.5e + GURPS pair).

WORKFLOW
    python wfrp_gear_harvest.py                       # (re)build the index
    python wfrp_gear_harvest.py --search "mail"       # find candidates
    python wfrp_gear_harvest.py --export "Rapier"
    python wfrp_gear_harvest.py --selftest

GOVERNING SOURCE
    I:\\Sourcebooks\\_text\\Warhammer\\Fantasy\\Old_World_Armoury.md — the
    dedicated WFRP 2e arms-&-armour sourcebook, the goldmine. The Fantasy/
    folder holds NO WFRP 2e core rulebook (its other books are Warhammer Fantasy
    BATTLE wargame army books, a different game), so the Armoury is the sole
    arms-&-armour source; the harvest prints NO COVERAGE for a core rulebook.

    The Armoury's stat tables were OCR'd as a VERTICAL COLUMN-DUMP: each cell of
    a table sits on its own line (a trailing tab per cell; the OCR occasionally
    fuses the last two cells of a row onto one line with a tab between them, and
    sprinkles blank separator lines). The detector reads each table by its known
    column schema: it finds the table title, walks past the header (which always
    ends on the "Availability" column), collects the data cells to the table's
    end (next Table / "Ammunition" / footnote / page-break), then segments the
    cell stream into fixed-width rows ANCHORED and VALIDATED on the unmistakable
    Group cell (weapons: Ordinary/Fencing/Flail/Parrying/Two-handed/Cavalry/
    Crossbow/Longbow/Sling/Throwing/Entangling/Gunpowder/Explosive/Engineer) or
    Location cell (armour: Head/Body/Arms/Legs/All). Armour category sub-headers
    (Leather / Studded Leather / Chain / Scale / Plate / Ithilmar Mail / Gromril
    Plate) set each row's armour `type`. A handful of new items are introduced in
    prose as semicolon stat blocks ("Khopesh: Cost 10 gc; Enc 50; Group Ordinary;
    Dmg SB; ...") — a second parser reads those. Ammunition sub-tables (arrows,
    shot, powder) are NOT weapons and are excluded.

    Book RAW only — every stat is the book's, cited to book + PDF page + table;
    nothing is invented. An unrecoverable / ambiguous cell is left empty and the
    row is recorded to the `soft` list (see --selftest and the .md footer).
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
OUT_JSON = REPO / "reference" / "wfrp_gear_index.json"
OUT_MD = REPO / "reference" / "wfrp_gear_index.md"
SYSTEM = "WFRP"

PAGE = re.compile(r"\[PDF page (\d+)\]")
DASHES = "\u2013\u2014\u2212-"                       # en / em / minus / hyphen
LONE_DASH = re.compile(rf"^[{DASHES}]+$")

# --- cell-level validators (a cell is one column value from the column-dump) ---
# Price: "2 gc", "1 s", "25 s", "100 gc", or a lone dash. gc/s/d = gold crown /
# silver shilling / brass penny.  (Loose: only used to lock row alignment.)
RE_PRICE = re.compile(rf"^(?:[{DASHES}]+|\d[\d,]*\s*(?:gc|gp|s|d)\b\.?)$", re.IGNORECASE)
RE_ENC = re.compile(rf"^(?:[{DASHES}]+|\d{{1,4}})$")          # encumbrance points
RE_AP = re.compile(rf"^(?:[{DASHES}]+|\d)$")                   # armour points 0-9
RE_INT = re.compile(r"^\d{1,3}$")
# Damage: "SB", "SB +1", "SB\u20134", "SB-2", "SB (SB+1)", a fixed number, or the
# book's "n/a" (entangling weapons \u2014 Lasso, Net \u2014 deal no damage).
RE_DAM = re.compile(
    rf"^(?:SB(?:\s*[+{DASHES}]\s*\d+)?(?:\s*\(.*\))?|\d{{1,2}}|n/?a)$",
    re.IGNORECASE)
# A cost column the book prints as a dash (no listed price), with the currency
# unit sometimes glued on by the OCR ("\u2014gc", "\u2014 gc", "\u2014").
RE_DASH_PRICE = re.compile(rf"^[{DASHES}]+\s*(?:gc|gp|s|d)?$", re.IGNORECASE)

# Weapon Group vocabulary — the anchor for a weapon row. A closed set drawn from
# the book's melee, missile, gunpowder and bolt-thrower tables.
WEAPON_GROUPS = {
    "ordinary", "fencing", "flail", "parrying", "two-handed", "two handed",
    "cavalry", "entangling", "crossbow", "longbow", "sling", "throwing",
    "gunpowder", "explosive", "engineer", "engineering",
}
# Armour location words — the anchor for an armour row (cells are these, or
# comma-combinations: "Body, Arms", "Body, Arms, Legs").
ARMOUR_LOCS = {"head", "body", "arms", "legs", "all"}
# WFRP availability ladder (a closed set; a row's trailing cell).
RARITIES = {"plentiful", "common", "average", "scarce", "rare", "very rare",
            "exotic", "abundant", "extremely rare"}


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def _clean(s: str) -> str:
    """Whitespace-normalise a value cell (kept RAW otherwise)."""
    s = s.replace("\ufb01", "fi").replace("\ufb02", "fl")
    return re.sub(r"\s+", " ", s).strip()


def _clean_name(s: str) -> str:
    """A weapon/armour name: drop the OCR footnote asterisk ('Flail*' -> 'Flail')
    and surrounding punctuation. The '*' is a table footnote (requires two hands),
    not part of the name."""
    return _clean(s).strip(" *\u2020").strip()


def _is_weapon_group(cell: str) -> bool:
    return _norm(cell) in WEAPON_GROUPS


def _is_armour_loc(cell: str) -> bool:
    toks = [t.strip().lower() for t in cell.split(",") if t.strip()]
    return bool(toks) and all(t in ARMOUR_LOCS for t in toks)


def _val_or_none(cell: str) -> Optional[str]:
    """A value cell, or None when the book prints a lone dash (a STATED blank —
    e.g. Ithilmar/Gromril have no open-market price/availability)."""
    c = _clean(cell)
    return None if (not c or LONE_DASH.match(c)) else c


def _price_or_none(cell: str) -> Optional[str]:
    """A price cell, or None when the book prints a dash for 'no listed price'
    (the OCR sometimes glues the unit on: '—gc', '— gc')."""
    c = _clean(cell)
    return None if (not c or RE_DASH_PRICE.match(c)) else c


def _qualities(cell: str) -> List[str]:
    """Split a Qualities cell into a list. 'None'/dash -> [] (book states none)."""
    c = _clean(cell)
    if not c or LONE_DASH.match(c) or c.lower() == "none":
        return []
    return [q.strip() for q in c.split(",") if q.strip()]


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #
@dataclass
class Gear:
    name: str
    category: str                       # "weapon" | "armour"
    book: str
    page: Optional[int]
    citation: str
    start: int                          # source line (1-based)
    end: int
    system: str = SYSTEM
    # weapon fields
    group: Optional[str] = None
    damage: Optional[str] = None
    reach_or_range: Optional[str] = None
    reload: Optional[str] = None
    qualities: Optional[List[str]] = None
    crew: Optional[str] = None
    # armour fields
    type: Optional[str] = None
    locations: Optional[str] = None
    armour_points: Optional[int] = None
    # shared
    price: Optional[str] = None
    encumbrance: Optional[str] = None
    availability: Optional[str] = None

    def stat_fields(self) -> int:
        return sum(1 for v in (self.group, self.damage, self.reach_or_range,
                               self.reload, self.qualities, self.type,
                               self.locations, self.armour_points, self.price,
                               self.encumbrance, self.availability)
                   if v not in (None, [], ""))

    def to_row(self) -> dict:
        d = asdict(self)
        return {k: v for k, v in d.items() if v not in (None, [], "")}


@dataclass
class Cell:
    text: str
    line: int                           # 0-based source line index
    page: Optional[int]


# --------------------------------------------------------------------------- #
# Table configuration — the book's column schema per table (Book RAW: this only
# tells the parser the column ORDER the Armoury prints; no value is supplied).
# --------------------------------------------------------------------------- #
@dataclass
class TableCfg:
    title: str                          # regex for the (whole-line) table title
    label: str                          # human citation label
    page: int                           # PDF page it lives on
    columns: List[str]                  # ordered field names
    anchor: str                         # "group" | "locations"
    category: str                       # "weapon" | "armour"
    category_headers: Tuple[str, ...] = ()   # armour type sub-headers


_W7 = ["name", "price", "encumbrance", "group", "damage", "qualities", "availability"]
_W9 = ["name", "price", "encumbrance", "group", "damage", "reach_or_range",
       "reload", "qualities", "availability"]
_W10 = ["name", "crew", "price", "encumbrance", "group", "damage",
        "reach_or_range", "reload", "qualities", "availability"]
_ARM = ["name", "price", "encumbrance", "locations", "armour_points", "availability"]

DASH_CLASS = r"[\u2013\u2014\-]"
TABLES: List[TableCfg] = [
    TableCfg(rf"Table\s+2{DASH_CLASS}1:\s*Armour", "Table 2-1: Armour", 22,
             _ARM, "locations", "armour",
             ("Leather", "Studded Leather", "Chain", "Scale", "Plate",
              "Ithilmar Mail", "Gromril Plate")),
    TableCfg(rf"Table\s+3{DASH_CLASS}1:\s*Best Craftsmanship Hand Weapons",
             "Table 3-1: Best Craftsmanship Hand Weapons", 31, _W7, "group", "weapon"),
    TableCfg(rf"Table\s+3{DASH_CLASS}2:\s*Best Craftsmanship Great Weapons",
             "Table 3-2: Best Craftsmanship Great Weapons", 39, _W7, "group", "weapon"),
    TableCfg(rf"Table\s+3{DASH_CLASS}3:\s*Melee Weapons",
             "Table 3-3: Melee Weapons", 42, _W7, "group", "weapon"),
    TableCfg(rf"Table\s+3{DASH_CLASS}4:\s*Missile Weapons",
             "Table 3-4: Missile Weapons", 42, _W9, "group", "weapon"),
    TableCfg(rf"Table\s+4{DASH_CLASS}2:\s*Gunpowder Weapons",
             "Table 4-2: Gunpowder Weapons", 49, _W9, "group", "weapon"),
    TableCfg(rf"Table\s+4{DASH_CLASS}4:\s*Bolt Throwers",
             "Table 4-4: Bolt Throwers", 51, _W10, "group", "weapon"),
]

RE_TABLE_LINE = re.compile(rf"^\s*Table\s+\d", re.IGNORECASE)
RE_FOOTNOTE = re.compile(r"^\s*[*\u2020]")
RE_PAGE_LINE = re.compile(r"^\s*##\s*\[PDF page")
RE_EMDASH_HEAD = re.compile(r"^\s*\u2014\s*\w")      # "— Missile Weapons —"


def _pages_for(lines: List[str]) -> List[Optional[int]]:
    pages: List[Optional[int]] = []
    page: Optional[int] = None
    for ln in lines:
        m = PAGE.search(ln)
        if m:
            page = int(m.group(1))
        pages.append(page)
    return pages


def _is_end(line: str) -> bool:
    s = line.strip()
    return bool(RE_TABLE_LINE.match(s) or s == "Ammunition"
                or RE_FOOTNOTE.match(s) or RE_PAGE_LINE.match(s)
                or RE_EMDASH_HEAD.match(s))


def _cells_in_region(lines: List[str], pages: List[Optional[int]],
                     lo: int, hi: int) -> List[Cell]:
    """Tab-split every line in [lo, hi) into non-empty cells (skip PDF-page
    markers and blank separator lines)."""
    out: List[Cell] = []
    for i in range(lo, hi):
        if PAGE.search(lines[i]):
            continue
        for piece in lines[i].split("\t"):
            s = piece.strip()
            if s:
                out.append(Cell(s, i, pages[i]))
    return out


def _anchor_ok(cfg: TableCfg, cell: str) -> bool:
    return _is_armour_loc(cell) if cfg.anchor == "locations" else _is_weapon_group(cell)


def parse_table(cfg: TableCfg, lines: List[str], pages: List[Optional[int]],
                book: str) -> Tuple[List[Gear], List[dict]]:
    """Parse one column-dump table into Gear rows. Returns (rows, soft)."""
    rows: List[Gear] = []
    soft: List[dict] = []

    title_re = re.compile(rf"^\s*{cfg.title}\s*$", re.IGNORECASE)
    t_idx = next((i for i, ln in enumerate(lines) if title_re.match(ln)), None)
    if t_idx is None:
        return rows, soft

    # Walk past the header (it always ends on the "Availability" column).
    data_lo = None
    for i in range(t_idx + 1, min(t_idx + 60, len(lines))):
        for piece in lines[i].split("\t"):
            if _norm(piece) == "availability":
                data_lo = i + 1
                break
        if data_lo is not None:
            break
    if data_lo is None:
        return rows, soft

    data_hi = next((i for i in range(data_lo, len(lines)) if _is_end(lines[i])),
                   len(lines))
    stream = _cells_in_region(lines, pages, data_lo, data_hi)

    ncols = len(cfg.columns)
    anchor_i = cfg.columns.index(cfg.anchor)
    price_i = cfg.columns.index("price")
    cat_headers = {h for h in cfg.category_headers}

    # Segment the flat cell stream into fixed-width rows, tracking the armour
    # category sub-header (Leather/Chain/…) as the row `type`. Each row is
    # ANCHORED + VALIDATED on its Group/Location cell so a stray cell resyncs
    # instead of corrupting the run.
    typed: List[Tuple[Cell, Optional[str]]] = []
    cur_type: Optional[str] = None
    for c in stream:
        if c.text in cat_headers:
            cur_type = c.text
            continue
        typed.append((c, cur_type))

    def _chunk_ok(j: int) -> bool:
        if j + ncols > len(typed):
            return False
        vals = [typed[j + k][0].text for k in range(ncols)]
        return _anchor_ok(cfg, vals[anchor_i]) and bool(RE_PRICE.match(vals[price_i]))

    i = 0
    while i + ncols <= len(typed):
        if not _chunk_ok(i):
            # drift / leaked prose: resync to the next aligned row start.
            j = i + 1
            while j + ncols <= len(typed) and not _chunk_ok(j):
                j += 1
            skipped = [typed[k][0].text for k in range(i, min(j, len(typed)))]
            if any(s not in cat_headers for s in skipped):
                soft.append({"table": cfg.label, "line": typed[i][0].line + 1,
                             "issue": "unaligned cells skipped",
                             "cells": skipped[:ncols]})
            if j + ncols > len(typed):
                break
            i = j
            continue

        chunk = [typed[i + k] for k in range(ncols)]
        vals = {cfg.columns[k]: chunk[k][0].text for k in range(ncols)}
        row_type = chunk[0][1]
        c0 = chunk[0][0]

        g = Gear(name=_clean_name(vals["name"]), category=cfg.category, book=book,
                 page=c0.page, citation=f"{book}, PDF p.{cfg.page} ({cfg.label})",
                 start=c0.line + 1, end=chunk[-1][0].line + 1)
        g.price = _price_or_none(vals.get("price", ""))
        g.encumbrance = _val_or_none(vals.get("encumbrance", ""))
        g.availability = _val_or_none(vals.get("availability", ""))
        if cfg.category == "weapon":
            g.group = _clean(vals["group"])
            g.damage = _val_or_none(vals.get("damage", ""))
            if "reach_or_range" in vals:
                g.reach_or_range = _val_or_none(vals["reach_or_range"])
            if "reload" in vals:
                g.reload = _val_or_none(vals["reload"])
            g.qualities = _qualities(vals.get("qualities", ""))
            if "crew" in vals:
                g.crew = _val_or_none(vals["crew"])
            if g.damage and not RE_DAM.match(g.damage):
                soft.append({"table": cfg.label, "name": g.name,
                             "line": c0.line + 1,
                             "issue": f"damage cell '{g.damage}' unexpected shape"})
        else:
            g.type = row_type
            g.locations = _clean(vals["locations"])
            ap = _val_or_none(vals.get("armour_points", ""))
            if ap is not None and RE_INT.match(ap):
                g.armour_points = int(ap)
            elif ap is not None:
                soft.append({"table": cfg.label, "name": g.name,
                             "line": c0.line + 1,
                             "issue": f"armour points '{ap}' not an integer"})
            if row_type is None:
                soft.append({"table": cfg.label, "name": g.name,
                             "line": c0.line + 1,
                             "issue": "no armour type sub-header in scope"})

        if not g.name or _norm(g.name) in ("name", "armour type"):
            soft.append({"table": cfg.label, "line": c0.line + 1,
                         "issue": f"missing/header name near '{vals}'"})
        else:
            rows.append(g)
        i += ncols

    return rows, soft


# --------------------------------------------------------------------------- #
# Inline semicolon stat blocks: "Khopesh: Cost 10 gc; Enc 50; Group Ordinary;
# Dmg SB; Qualities Slow; Avail Rare."  (a few new items introduced in prose)
# --------------------------------------------------------------------------- #
RE_INLINE_START = re.compile(r"^([A-Z][A-Za-z0-9'\u2019 /\-]{1,44}?):\s+Cost\b")
RE_FIELD = re.compile(
    r"\b(Cost|Enc|Group|Dmg|Damage|Range|Reload|Qualities|Quality|Avail|"
    r"Availability|Protection|AP|Crew)\b\s*(.*?)\s*(?=;|\.\s*$|$)",
    re.IGNORECASE)


def parse_inline(lines: List[str], pages: List[Optional[int]],
                 book: str) -> Tuple[List[Gear], List[dict]]:
    rows: List[Gear] = []
    soft: List[dict] = []
    i = 0
    n = len(lines)
    while i < n:
        m = RE_INLINE_START.match(lines[i].strip())
        if not m:
            i += 1
            continue
        name = _clean_name(m.group(1))
        buf = lines[i].strip()
        j = i
        # accumulate wrapped continuation lines until an availability field lands
        while j + 1 < n and not re.search(r"\b(Avail|Availability)\b", buf, re.IGNORECASE) \
                and (j - i) < 4:
            j += 1
            buf += " " + lines[j].strip()
        buf = re.sub(r"\s+", " ", buf)

        fields: Dict[str, str] = {}
        body = buf.split(":", 1)[1] if ":" in buf else buf
        for fm in RE_FIELD.finditer(body):
            key = fm.group(1).lower()
            val = fm.group(2).strip().rstrip(".").strip()
            fields.setdefault(key, val)

        page = pages[i]
        cite = f"{book}, PDF p.{pages[i]} (inline entry)"
        is_armour = ("protection" in fields) or ("ap" in fields)
        is_weapon = ("group" in fields) or ("dmg" in fields) or ("damage" in fields)

        if is_armour and not is_weapon:
            g = Gear(name=name, category="armour", book=book, page=page,
                     citation=cite, start=i + 1, end=j + 1)
            g.price = _price_or_none(fields.get("cost", ""))
            g.encumbrance = _val_or_none(fields.get("enc", ""))
            g.locations = _clean(fields.get("protection", "")) or None
            ap = _val_or_none(fields.get("ap", ""))
            if ap and RE_INT.match(ap):
                g.armour_points = int(ap)
            g.availability = _val_or_none(fields.get("avail")
                                          or fields.get("availability", ""))
            rows.append(g)
        elif is_weapon:
            g = Gear(name=name, category="weapon", book=book, page=page,
                     citation=cite, start=i + 1, end=j + 1)
            g.price = _price_or_none(fields.get("cost", ""))
            g.encumbrance = _val_or_none(fields.get("enc", ""))
            g.group = _clean(fields.get("group", "")) or None
            g.damage = _val_or_none(fields.get("dmg") or fields.get("damage", ""))
            g.reach_or_range = _val_or_none(fields.get("range", ""))
            g.reload = _val_or_none(fields.get("reload", ""))
            g.qualities = _qualities(fields.get("qualities")
                                     or fields.get("quality", ""))
            g.availability = _val_or_none(fields.get("avail")
                                          or fields.get("availability", ""))
            rows.append(g)
        else:
            # e.g. "Pavise: Cost 50 gc; Enc 120; Availability Scarce." — no
            # Group/Dmg/AP/Protection, so weapon-vs-armour is ambiguous. RAW
            # rule: do not guess a category — record it soft.
            soft.append({"table": "inline entry", "name": name, "line": i + 1,
                         "issue": "no Group/Dmg/AP/Protection — category "
                                  "ambiguous; not classified",
                         "fields": fields})
        i = j + 1
    return rows, soft


# --------------------------------------------------------------------------- #
# Source + corpus
# --------------------------------------------------------------------------- #
@dataclass
class Source:
    key: str
    book: str
    path: Path
    detector: str                       # "owa" (Old World Armoury) | ...
    coverage: str = "pending"
    lines: List[str] = field(default_factory=list)
    rows: List[Gear] = field(default_factory=list)
    soft: List[dict] = field(default_factory=list)


_FANTASY = Path("Warhammer/Fantasy")
SOURCES: List[Source] = [
    Source("owa", "Old World Armoury",
           _FANTASY / "Old_World_Armoury.md", "owa"),
]
# A WFRP 2e CORE RULEBOOK is expected-but-absent from the Fantasy/ folder; kept
# here so the harvest can print NO COVERAGE for it explicitly.
EXPECTED_ABSENT = [("WFRP 2e Core Rulebook",
                    "no WFRP roleplay core rulebook in Warhammer/Fantasy/ "
                    "(only Warhammer Fantasy BATTLE wargame books)")]


def detect_owa(lines: List[str], pages: List[Optional[int]],
               book: str) -> Tuple[List[Gear], List[dict]]:
    rows: List[Gear] = []
    soft: List[dict] = []
    for cfg in TABLES:
        r, s = parse_table(cfg, lines, pages, book)
        rows.extend(r)
        soft.extend(s)
    r, s = parse_inline(lines, pages, book)
    rows.extend(r)
    soft.extend(s)

    # Defensive de-dup: one row per (name, category, citation). Keep the richest.
    best: Dict[Tuple[str, str, str], Gear] = {}
    for g in rows:
        k = (g.name.lower(), g.category, g.citation)
        cur = best.get(k)
        if cur is None or g.stat_fields() > cur.stat_fields():
            best[k] = g
    ordered = sorted(best.values(), key=lambda g: (g.start,))
    return ordered, soft


DETECTORS = {"owa": detect_owa}


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
            src.rows, src.soft = DETECTORS[src.detector](src.lines, pages, src.book)
            nw = sum(1 for g in src.rows if g.category == "weapon")
            na = sum(1 for g in src.rows if g.category == "armour")
            src.coverage = f"ok — {nw} weapons + {na} armour from {path.name}"

    def all_rows(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for g in src.rows:
                yield src, g

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, g in self.all_rows(book):
            nm = g.name.lower()
            if nm == q:
                exact.append((src, g))
            elif q in nm:
                partial.append((src, g))
        return exact if exact else partial


# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #
def _md_weapon_row(g: Gear) -> str:
    q = ", ".join(g.qualities) if g.qualities else "—"
    return (f"| {g.name} | {g.group or '—'} | {g.damage or '—'} | "
            f"{g.reach_or_range or '—'} | {g.reload or '—'} | {q} | "
            f"{g.encumbrance or '—'} | {g.price or '—'} | "
            f"{g.availability or '—'} | {g.page if g.page else '—'} |")


def _md_armour_row(g: Gear) -> str:
    ap = g.armour_points if g.armour_points is not None else "—"
    return (f"| {g.name} | {g.type or '—'} | {g.locations or '—'} | {ap} | "
            f"{g.encumbrance or '—'} | {g.price or '—'} | "
            f"{g.availability or '—'} | {g.page if g.page else '—'} |")


def write_index(corpus: Corpus) -> Tuple[int, int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    all_rows = [g for _, g in corpus.all_rows()]
    weapons = [g for g in all_rows if g.category == "weapon"]
    armour = [g for g in all_rows if g.category == "armour"]
    all_soft = [s for src in corpus.sources for s in src.soft]

    md: List[str] = [
        "# WFRP ARMS & ARMOUR INDEX — The New Path",
        "",
        "**Generated by `scripts/wfrp_gear_harvest.py`. Do not hand-edit; rerun",
        "the harvest.** These are **Warhammer Fantasy Roleplay (2nd edition)**",
        "weapons and armour. Every row is stamped `system: WFRP` and tagged",
        "`category: weapon|armour`; a WFRP gear row is SOURCE MATERIAL for the",
        "system-translator skill, not campaign RAW. Stats are Book RAW, cited to",
        "book + PDF page + table; a field left `—` is one the book prints as a",
        "dash or the OCR did not cleanly yield. Use `--export \"NAME\"` for a",
        "translator packet.",
        "",
        f"**Totals: {len(all_rows)} rows — {len(weapons)} weapons, "
        f"{len(armour)} armour.**",
        "",
    ]
    for name, why in EXPECTED_ABSENT:
        md.append(f"> NO COVERAGE — {name}: {why}.")
    md.append("")

    for src in corpus.sources:
        md.append(f"## {src.book}  *(system: {SYSTEM})*")
        md.append("")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        sw = [g for g in src.rows if g.category == "weapon"]
        sa = [g for g in src.rows if g.category == "armour"]
        if sw:
            md.append(f"### Weapons — {len(sw)}")
            md.append("")
            md.append("| Weapon | Group | Damage | Range | Reload | Qualities | "
                      "Enc | Price | Avail | Page |")
            md.append("|---|---|---|---|---|---|---|---|---|---|")
            for g in sorted(sw, key=lambda g: (g.group or "", g.name.lower())):
                md.append(_md_weapon_row(g))
            md.append("")
        if sa:
            md.append(f"### Armour — {len(sa)}")
            md.append("")
            md.append("| Armour | Type | Locations | AP | Enc | Price | Avail | "
                      "Page |")
            md.append("|---|---|---|---|---|---|---|---|")
            for g in sorted(sa, key=lambda g: (g.start,)):
                md.append(_md_armour_row(g))
            md.append("")

    if all_soft:
        md.append("## Soft / uncertain rows")
        md.append("")
        md.append("Rows the harvest could not fully or confidently resolve "
                  "(RAW rule: never guessed).")
        md.append("")
        for s in all_soft:
            bits = "; ".join(f"{k}={v}" for k, v in s.items())
            md.append(f"- {bits}")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    sources_out = []
    for src in corpus.sources:
        sources_out.append({
            "key": src.key, "book": src.book, "system": SYSTEM,
            "coverage": src.coverage,
            "rows": [g.to_row() for g in src.rows],
            "soft": src.soft,
        })
    OUT_JSON.write_text(json.dumps({
        "generated_by": "scripts/wfrp_gear_harvest.py",
        "system": SYSTEM,
        "corpus": str(corpus.base),
        "no_coverage": [{"expected": n, "reason": w} for n, w in EXPECTED_ABSENT],
        "total_rows": len(all_rows),
        "total_weapons": len(weapons),
        "total_armour": len(armour),
        "sources": sources_out,
    }, indent=1, ensure_ascii=False), encoding="utf-8")
    return len(weapons), len(armour), len(all_soft)


def export_packet(corpus: Corpus, name: str, book: Optional[str],
                  out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 8:
        print(f"'{name}' matches {len(hits)} rows; narrow with --book or an exact name:")
        for src, g in hits[:20]:
            print(f"  {g.name}   [{g.category}; {g.book}, p.{g.page}]")
        return 1
    packets = []
    for src, g in hits:
        lo = max(0, g.start - 1)
        body = [ln for ln in src.lines[lo:g.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "wfrp-gear-for-translation",
            "instructions": ("A Warhammer Fantasy Roleplay (2e) "
                             f"{g.category} (system: {SYSTEM}). Feed to the "
                             "system-translator skill for the paired 3.5e AND "
                             "GURPS treatment. raw_block is OCR from a column-dump."),
            "name": g.name, "category": g.category, "system": SYSTEM,
            "source": {"book": g.book, "pdf_page": g.page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [g.start, g.end], "citation": g.citation},
            "parsed": g.to_row(),
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1,
                      ensure_ascii=False)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


# --------------------------------------------------------------------------- #
# Selftest
# --------------------------------------------------------------------------- #
# A column-dump fixture: an armour category + rows (Table 2-1 style), a melee
# row with tab-merged qualities+availability (Table 3-3 style), a missile row
# (Table 3-4 style, fixed-number damage + range/reload), and an inline block.
FIXTURE_LINES = """## [PDF page 22]
Table 2\u20131: Armour
Armour Type\t
Cost\t
Enc\t
Location(s) Covered\t
AP \t
Availability
Leather\t
\t
\t
\t
\t
\t Leather Jack\t
12 gc\t
50\t
Body, Arms\t
1\t
Common
Plate\t
\t
\t
\t
\t
\t Full Plate Armour\t
400 gc\t
400\t
All\t
5\t
Very Rare
## [PDF page 42]
Table 3\u20133: Melee Weapons
Name\t
Cost\t
Enc\t
Group\t
Damage\t
Qualities\t
Availability
Rapier\t
18 gc\t
40\t
Fencing\t
SB \u20131\t
Fast\t
Scarce
Buckler\t
2 gc\t
10\t
Parrying\t
SB \u20134\t
Balanced, Defensive, Pummelling\t Average
Table 3\u20134: Missile Weapons
Name\t
Cost\t
Enc\t
Group\t
Damage\t
Range\u2020\t
Reload\t
Qualities\t
Availability
Longbow\t
15 gc\t
90\t
Longbow\t
3\t
30/60\t
Half\t
Armour Piercing\t
Average
Ammunition
Arrows (5)\t
1 s\t
Khopesh: Cost 10 gc; Enc 50; Group Ordinary; Dmg SB; Qualities
Slow; Avail Rare.
"""


def selftest(base: Path) -> int:
    failures: List[str] = []
    lines = FIXTURE_LINES.splitlines()
    pages = _pages_for(lines)
    rows, soft = detect_owa(lines, pages, "Fixture Armoury")
    by = {g.name: g for g in rows}

    want = {"Leather Jack", "Full Plate Armour", "Rapier", "Buckler",
            "Longbow", "Khopesh"}
    if set(by) != want:
        failures.append(f"fixture detected {sorted(by)}, wanted {sorted(want)}")
    else:
        lj = by["Leather Jack"]
        if (lj.category, lj.type, lj.locations, lj.armour_points, lj.encumbrance,
                lj.price, lj.availability) != \
                ("armour", "Leather", "Body, Arms", 1, "50", "12 gc", "Common"):
            failures.append(f"Leather Jack parsed wrong: {lj.to_row()}")
        fp = by["Full Plate Armour"]
        if (fp.type, fp.armour_points, fp.availability) != ("Plate", 5, "Very Rare"):
            failures.append(f"Full Plate Armour parsed wrong: {fp.to_row()}")

        rp = by["Rapier"]
        if (rp.category, rp.group, rp.damage, rp.qualities, rp.price,
                rp.availability) != \
                ("weapon", "Fencing", "SB \u20131", ["Fast"], "18 gc", "Scarce"):
            failures.append(f"Rapier parsed wrong: {rp.to_row()}")

        bk = by["Buckler"]   # qualities + availability tab-merged onto one line
        if bk.qualities != ["Balanced", "Defensive", "Pummelling"] \
                or bk.availability != "Average":
            failures.append(f"Buckler merge split wrong: {bk.to_row()}")

        lb = by["Longbow"]   # missile: fixed-number damage + range + reload
        if (lb.group, lb.damage, lb.reach_or_range, lb.reload, lb.qualities) != \
                ("Longbow", "3", "30/60", "Half", ["Armour Piercing"]):
            failures.append(f"Longbow parsed wrong: {lb.to_row()}")

        kh = by["Khopesh"]   # inline semicolon block
        if (kh.category, kh.group, kh.damage, kh.qualities, kh.price,
                kh.availability) != \
                ("weapon", "Ordinary", "SB", ["Slow"], "10 gc", "Rare"):
            failures.append(f"Khopesh inline parsed wrong: {kh.to_row()}")

    if any(g.system != SYSTEM for g in rows):
        failures.append("a fixture row is missing the WFRP system stamp")
    # Ammunition ("Arrows (5)") must NOT be harvested as a weapon.
    if "Arrows (5)" in by:
        failures.append("ammunition leaked into the weapon index")

    # Live-harvest invariants.
    owa = base / SOURCES[0].path
    if owa.exists():
        corpus = Corpus(base, [Source("owa", "Old World Armoury",
                                      SOURCES[0].path, "owa")])
        live = [g for _, g in corpus.all_rows()]
        nw = sum(1 for g in live if g.category == "weapon")
        na = sum(1 for g in live if g.category == "armour")
        if not (55 <= nw <= 90):
            failures.append(f"weapon count {nw} outside expected band 55..90")
        if not (35 <= na <= 55):
            failures.append(f"armour count {na} outside expected band 35..55")
        for g in live:
            if g.system != SYSTEM:
                failures.append(f"live row missing system stamp: {g.name}")
                break
            if not g.name or g.category not in ("weapon", "armour"):
                failures.append(f"live row bad name/category: {g.name!r}/{g.category}")
                break
            if _norm(g.name) in ("name", "availability", "group", "cost", "enc",
                                 "armour type", "damage", "qualities"):
                failures.append(f"header/junk leaked as a row name: {g.name!r}")
                break
        for g in live:
            if g.category == "armour" and g.armour_points is None:
                failures.append(f"armour row with no AP: {g.name}")
                break
            if g.category == "weapon" and not g.group:
                failures.append(f"weapon row with no group: {g.name}")
                break
        for probe in ("Rapier", "Mail Shirt", "Longbow", "Halberd"):
            if not corpus.find(probe):
                failures.append(f"known WFRP gear not found live: {probe}")
    else:
        print("  [SKIP] Old World Armoury extraction not found — fixture only")

    for f in failures:
        print(f"SELFTEST FAIL: {f}")
    print("selftest: " + ("PASS" if not failures else f"{len(failures)} failure(s)"))
    return 0 if not failures else 1


# --------------------------------------------------------------------------- #
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

    corpus = Corpus(args.corpus, SOURCES)

    if args.search:
        q = args.search.lower()
        found = sorted({(g.name, g.category, g.book, g.page or -1,
                         g.damage or g.locations or "—")
                        for _, g in corpus.all_rows(args.book)
                        if q in g.name.lower()})
        for nm, cat, bk, page, key in found:
            loc = bk if page < 0 else f"{bk}, p.{page}"
            print(f"  {nm}  [{cat}; {key}; {loc}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.rows for s in corpus.sources)
    for src in corpus.sources:
        print(f"  {src.book:24s} [{src.coverage}]")
    for name, why in EXPECTED_ABSENT:
        print(f"  {name:24s} [NO COVERAGE — {why}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    nw, na, ns = write_index(corpus)
    print(f"\n{nw + na} WFRP gear rows — {nw} weapons + {na} armour"
          f"{f'; {ns} soft' if ns else ''}. (system: {SYSTEM})")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
