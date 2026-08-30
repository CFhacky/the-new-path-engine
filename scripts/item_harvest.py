#!/usr/bin/env python3
"""item_harvest.py — collate magic item stat blocks for translation.

THE PROCESS (Chad, 2026-08-07, companion to term_harvest.py and
creature_harvest.py): this is the native D&D item collation. GURPS 3e magic
items use `gurps3e_item_harvest.py` and remain edition-labeled rather than being
mixed into this index.

It walks the magic-item text extractions and produces the COLLATION:

    reference/magic_item_index.json  — every item block found: name, tag,
                                       book, PDF page, line span, and the
                                       quick fields a triage read needs
                                       (price, item level, body slot, caster
                                       level, aura tier/school/DC, activation),
                                       parsed where the OCR is clean
    reference/magic_item_index.md    — the same index for human eyes, by book

The raw text is deliberately NOT copied into the repository — the Magic Item
Compendium alone is 65k lines of OCR and would bloat it for nothing (the same
reasoning creature_harvest.py applies to twelve books of bestiary). Instead,
`--export` emits a TRANSLATOR-READY PACKET on demand: the verbatim block plus
provenance and parsed fields, as JSON on stdout or to a file. That packet is
the input the `system-translator` skill expects when converting an item into
the hybrid's paired 3.5e + GURPS treatment.

WORKFLOW
    python item_harvest.py                       # (re)build the index
    python item_harvest.py --search "belt"       # find candidates
    python item_harvest.py --export "Belt of Battle"
        -> JSON packet -> feed to the system-translator skill
    python item_harvest.py --selftest

GOVERNING SOURCES
    I:\\Sourcebooks\\_text\\D&D 3.5e\\Magic and Items\\Magic Item Compendium.md
    — the OCR text extraction, item entries in the MIC's own grammar:

        ITEM NAME                                (ALL-CAPS, its own line;
        [SYNERGY]                                 tag on its own line or
                                                  appended: "CHAMPION [RELIC]")
        Price (Item Level): 12,000 gp (13th)     (or "Price: +1 bonus")
        Body Slot: Waist                         (or "Property: Armor")
        Caster Level: 9th
        Aura: Moderate; (DC 19) transmutation
        Activation: — and swift (mental)
        [flavor + rules prose, Prerequisites, Cost to Create]

    The anchor is a name line whose next content line is a real Price value —
    the same three-line-test discipline spell_lookup.py uses for the Spell
    Compendium. Long names wrap across column lines ("TENTACLE ROD," /
    "GREATER"), so the harvest joins upward from the priced line. The PDFs on
    I:\\Sourcebooks stand behind every extraction when the OCR is ambiguous.

    Block DETECTION is source-specific. This harvester now covers the Magic
    Item Compendium, the DMG's own magic items, and the Arms & Equipment Guide,
    each through its own detector. GURPS magic items remain in the separately
    labeled GURPS 3e index rather than being mixed into native D&D items. A
    configured Source whose file cannot be read prints NO COVERAGE and is never
    improvised. A dedicated additive path joins the DMG's table-first rod/staff
    rows to their source-printed description headings without changing any
    legacy detector row.
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
OUT_JSON = REPO / "reference" / "magic_item_index.json"
OUT_MD = REPO / "reference" / "magic_item_index.md"

# ---------------------------------------------------------------------------
# Field grammar (the MIC's own entry shape)
# ---------------------------------------------------------------------------

PAGE = re.compile(r"\[PDF page (\d+)\]")

# An ALL-CAPS name on its own line, with an optional trailing bracket tag the
# MIC appends to some names ("CHAMPION [RELIC]", "... [AUGMENT CRYSTAL]").
# Group 1 is the name core, group 2 the tag. Allows the comma of "AGILITY,
# GREATER", apostrophes (straight and curly) of "MELF'S ...", hyphen and slash.
# No trailing punctuation such as "!" — that rejects sidebar shouts like
# "YOU CHANGED MY MAGIC ITEMS!". A pure "[SYNERGY]" line has no name core and
# does not match here; it is caught as a standalone tag in the scan.
NAME_LINE = re.compile(
    r"^([A-Z][A-Z0-9 ,'\u2019/\-]{2,54}?)\s*(?:\[([A-Z][A-Z ]+)\])?\s*$")

PRICE = re.compile(r"^Price(?:\s*\(Item Level\))?\s*:\s*(.+)$", re.IGNORECASE)
# A Price VALUE that looks like a real price: starts with + or a digit, or is
# one of the book's non-numeric prices, or contains "gp"/"bonus". This rejects
# the template legend "Price (Item Level): The purchase price of the item...".
PRICE_VALUE_OK = re.compile(r"^(?:[+\u2212]?\d|Varies|Special|\u2014|-)"
                            r"|(?:\bgp\b|\bbonus\b)", re.IGNORECASE)
ITEM_LEVEL = re.compile(r"\((\d+(?:st|nd|rd|th))\)\s*$", re.IGNORECASE)

BODY_SLOT = re.compile(r"^Body Slot\s*:\s*(.+)$", re.IGNORECASE)
PROPERTY = re.compile(r"^Property\s*:\s*(.+)$", re.IGNORECASE)
CASTER = re.compile(r"^Caster Level\s*:\s*(.+)$", re.IGNORECASE)
ACTIVATION = re.compile(r"^Activation\s*:\s*(.+)$", re.IGNORECASE)
AURA = re.compile(
    r"^Aura\s*:\s*(Faint|Moderate|Strong|Overwhelming|No)\b[.;,]?\s*"
    r"(?:\(DC\s*(\d+)\)\s*)?([A-Za-z][A-Za-z ]*?)?\s*$",
    re.IGNORECASE,
)

# Name lines that are structure, not items — belt and braces even though the
# Price-within-window test already rejects most of them.
NON_ITEM = {
    "ITEM NAME", "MAGIC ITEM", "MAGIC ITEMS", "NEW ITEM TYPES", "TABLE",
    "INTRODUCTION", "CONTENTS", "CREDITS", "APPENDIX", "GLOSSARY", "INDEX",
}


def _letter_majority(name: str) -> bool:
    letters = sum(ch.isalpha() for ch in name)
    return letters >= max(3, len(name.replace(" ", "")) // 2)


def _name_core(line: str) -> Optional[Tuple[str, Optional[str]]]:
    """(name core, tag) if the stripped line is a valid ALL-CAPS name, else
    None. A pure bracket tag line ("[SYNERGY]") returns None."""
    s = line.strip()
    if s.startswith("["):
        return None
    m = NAME_LINE.match(s)
    if not m:
        return None
    core = m.group(1).strip()
    if core in NON_ITEM or not _letter_majority(core):
        return None
    return core, (m.group(2).strip() if m.group(2) else None)


@dataclass
class Item:
    name: str
    book: str
    page: int
    start: int  # line span in the extraction, for --export
    end: int
    tag: Optional[str] = None           # RELIC / SYNERGY / AUGMENT CRYSTAL / SET
    price: Optional[str] = None
    item_level: Optional[str] = None
    body_slot: Optional[str] = None
    property: Optional[str] = None
    caster_level: Optional[str] = None
    aura: Optional[str] = None          # tier: Faint/Moderate/Strong/...
    aura_school: Optional[str] = None
    aura_dc: Optional[str] = None
    activation: Optional[str] = None

    def quick_fields(self) -> int:
        return sum(1 for v in (self.price, self.body_slot, self.property,
                               self.caster_level, self.aura) if v)


def parse_quick_fields(item: Item, body_lines: List[str]) -> None:
    for raw in body_lines:
        line = raw.strip()
        if not line:
            continue
        if item.price is None:
            m = PRICE.match(line)
            if m and PRICE_VALUE_OK.search(m.group(1).strip()):
                value = m.group(1).strip()
                lvl = ITEM_LEVEL.search(value)
                if lvl:
                    item.item_level = lvl.group(1)
                    value = ITEM_LEVEL.sub("", value).strip()
                item.price = value
                continue
        if item.body_slot is None:
            m = BODY_SLOT.match(line)
            if m:
                item.body_slot = m.group(1).strip()
                continue
        if item.property is None:
            m = PROPERTY.match(line)
            if m:
                item.property = m.group(1).strip()
                continue
        if item.caster_level is None:
            m = CASTER.match(line)
            if m:
                item.caster_level = m.group(1).strip()
                continue
        if item.aura is None:
            m = AURA.match(line)
            if m:
                item.aura = m.group(1).title()
                if m.group(2):
                    item.aura_dc = m.group(2)
                if m.group(3):
                    school = m.group(3).strip().lower()
                    if school:
                        item.aura_school = school
                continue
        if item.activation is None:
            m = ACTIVATION.match(line)
            if m:
                item.activation = m.group(1).strip()
                continue


# ---------------------------------------------------------------------------
# Detectors — one per item-book grammar (no cross-import; add here)
# ---------------------------------------------------------------------------


def _gather_name_up(lines: List[str], anchor: int) -> Tuple[int, str, Optional[str]]:
    """MIC item names wrap across column lines: the anchor is the LAST name
    fragment (the one right above Price); "TENTACLE ROD," and "GREATER" arrive
    on two lines, "CLOAK OF" / "SOULBOUND" / "RESISTANCE," / "GREATER" on four
    (blank-separated). Walk upward collecting consecutive ALL-CAPS fragments,
    tolerating at most a two-line blank/page-marker gap between them, and join
    them into the full name. Returns (topmost line index, full name, tag).
    """
    core = _name_core(lines[anchor])
    frags = [core[0]]
    tag = core[1]
    top = anchor
    j, gap = anchor - 1, 0
    while j >= 0 and len(frags) < 6:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            gap += 1
            if gap > 2:
                break
            j -= 1
            continue
        up = _name_core(lines[j])
        if up is None:
            break
        frags.append(up[0])
        if up[1] and not tag:
            tag = up[1]
        top, gap = j, 0
        j -= 1
    frags.reverse()
    return top, re.sub(r"\s+", " ", " ".join(frags)).strip().title(), tag


def detect_mic(lines: List[str], pages: List[int], book: str) -> List[Item]:
    """Detect Magic Item Compendium entries: an ALL-CAPS name whose first
    content line (skipping a bracketed tag and page markers) is a real Price.
    """
    n = len(lines)
    starts: List[Tuple[int, str, Optional[str]]] = []
    used = set()
    for i, ln in enumerate(lines):
        core = _name_core(ln)
        if core is None:
            continue
        # The first few CONTENT lines after the name must contain a Price.
        j, seen, priced, tag = i + 1, 0, False, core[1]
        while j < n and seen < 4:
            s = lines[j].strip()
            if not s or PAGE.search(lines[j]):
                j += 1
                continue
            # A bracketed tag line ("[SYNERGY]") sits between name and Price;
            # capture it and step over it without spending a content slot.
            if s.startswith("[") and s.endswith("]"):
                if not tag:
                    tag = s.strip("[] ").strip() or None
                j += 1
                continue
            seen += 1
            m = PRICE.match(s)
            if m and PRICE_VALUE_OK.search(m.group(1).strip()):
                priced = True
                break
            # Any other prose line before a Price means this ALL-CAPS line was
            # a category header (e.g. "THIRD EYE") or a heading, not an item.
            break
        if not priced or i in used:
            continue
        used.add(i)
        top, full, up_tag = _gather_name_up(lines, i)
        starts.append((top, full, tag or up_tag))

    starts.sort()
    items: List[Item] = []
    for k, (s, name, tag) in enumerate(starts):
        e = starts[k + 1][0] if k + 1 < len(starts) else min(n, s + 120)
        e = min(e, s + 120)
        item = Item(name=name, book=book, page=pages[s], start=s, end=e, tag=tag)
        parse_quick_fields(item, lines[s + 1:e])
        items.append(item)
    return items


# ---------------------------------------------------------------------------
# DMG detector — a different grammar: "Name: description ... TRAILER", where the
# trailer is "Aura School; CL Nth; <prereqs>; Price N gp; Weight W". The name is
# the nearest "Name:" colon-line above a trailer. term_harvest.py OWNS the two
# weapon/armor "special ability" sections of this same book (the affixes), so
# those ranges are masked here — the affixes are not re-listed as items. Rods
# and staffs whose entries defeat this trailer-first grammar are recovered by
# the additive, table-aware path below; this legacy detector remains untouched.
# ---------------------------------------------------------------------------

DMG_TRAILER = re.compile(
    r"^(Faint|Moderate|Strong|Overwhelming)\s+([A-Za-z]+)\s*[;,.]?\s*CL\s+([\w/]+)",
    re.IGNORECASE)
DMG_NAME = re.compile(r"^([A-Z][A-Za-z0-9'’\-()/,. ]{2,46}?):\s+(\S.*)$")
DMG_NAME_REJECT = re.compile(
    r"^(Note|Price|Weight|CL|Prerequisites?|Cost|Aura|Special|Lore|DC|Caster Level|"
    r"Market Price|Construction|Strong|Moderate|Faint|Overwhelming|Table|Chapter|Activation|"
    r"Description|Benefit|Normal|Duration|Range|Target|Saving Throw|Example|XP Cost)\b",
    re.IGNORECASE)
DMG_PRICE = re.compile(r"Price\s+([0-9][\d,]*)", re.IGNORECASE)
# The two sections term_harvest.py governs; skipped here to avoid double-listing.
DMG_MASK = [
    (r"Magic Armor.{0,3}and Shield Special Ability Descriptions", r"^Specific Armors"),
    (r"Magic Weapon Special Ability Descriptions", r"^Specific Weapons"),
]


def detect_dmg(lines: List[str], pages: List[int], book: str) -> List[Item]:
    n = len(lines)
    masks: List[Tuple[int, int]] = []
    for s_anchor, e_anchor in DMG_MASK:
        sr, er = re.compile(s_anchor), re.compile(e_anchor)
        s = next((i for i, l in enumerate(lines) if sr.search(l)), None)
        if s is None:
            continue
        e = next((i for i in range(s + 1, n) if er.search(lines[i])), n)
        masks.append((s, e))

    def masked(i: int) -> bool:
        return any(a <= i < b for a, b in masks)

    items: List[Item] = []
    used = set()
    for i, ln in enumerate(lines):
        if masked(i) or not DMG_TRAILER.match(ln.strip()):
            continue
        tm = DMG_TRAILER.match(ln.strip())
        # Name: the nearest "Name:" colon-line above, stopping at a prior trailer.
        j, steps, name_idx, name = i - 1, 0, None, None
        while j >= 0 and steps < 40:
            s = lines[j].strip()
            if s and not PAGE.search(lines[j]):
                if DMG_TRAILER.match(s):
                    break
                nm = DMG_NAME.match(s)
                if nm and not DMG_NAME_REJECT.match(s):
                    name_idx, name = j, nm.group(1).strip()
                    break
            j -= 1
            steps += 1
        if name_idx is None or name_idx in used:
            continue
        used.add(name_idx)
        # Gather the trailer text (it wraps) for the price, and set the block end.
        ttext, k, steps, end = [ln.strip()], i + 1, 0, i + 1
        while k < n and steps < 4:
            s = lines[k].strip()
            if PAGE.search(lines[k]):
                k += 1
                continue
            if s == "":
                break
            if DMG_NAME.match(s) and not DMG_NAME_REJECT.match(s):
                end = k
                break
            ttext.append(s)
            end = k + 1
            if re.search(r"Weigh", s, re.IGNORECASE):
                break
            k += 1
            steps += 1
        item = Item(name=name, book=book, page=pages[name_idx], start=name_idx, end=end)
        item.aura = tm.group(1).title()
        item.aura_school = tm.group(2).lower()
        item.caster_level = tm.group(3)
        pm = DMG_PRICE.search(" ".join(ttext))
        if pm:
            item.price = f"{pm.group(1)} gp"
        items.append(item)
    items.sort(key=lambda it: it.start)
    return items


# Additive DMG table-first recovery. These rows are source-verified against
# Tables 7-19 (PDF p.235) and 7-25 (PDF p.244) plus their own description
# blocks. The legacy detector above remains unchanged and its rows stay first.
# tuple: name, source heading, table aliases, price, OCR price evidence,
#        aura, aura school(s), caster level, table page, section
DMG_TABLE_GAP_ROWS = [
    ("Absorption", "Absorption", ("Absorption",), "50,000 gp", ("$0,000", "50,000"), "Strong", "abjuration", "15th", 235, "rod"),
    ("Alertness", "Alertness", ("Alertness",), "85,000 gp", ("85,000",), "Moderate", "abjuration, divination, enchantment, and evocation", "11th", 235, "rod"),
    ("Flailing", "Flailing", ("Flailing",), "50,000 gp", ("$0,000", "50,000"), "Moderate", "enchantment", "9th", 235, "rod"),
    ("Lordly Might", "Lordly Might", ("Lordly might",), "70,000 gp", ("70,000",), "Strong", "enchantment, evocation, necromancy, and transmutation", "19th", 235, "rod"),
    ("Negation", "Negation", ("Negation",), "37,000 gp", ("37,000",), "Strong", "varied", "15th", 235, "rod"),
    ("Splendor", "Splendor", ("Splendor",), "25,000 gp", ("23,000", "25,000"), "Strong", "conjuration and transmutation", "12th", 235, "rod"),
    ("Thunder and Lightning", "Thunder and Lightning", ("Thunder and lightning",), "33,000 gp", ("33,000",), "Moderate", "evocation", "9th", 235, "rod"),
    ("Wonder", "Wonder", ("Worder", "Wonder"), "12,000 gp", ("12,000",), "Moderate", "enchantment", "10th", 235, "rod"),
    ("Abjuration", "Abjuration", ("Abjuration",), "65,000 gp", ("65,000",), "Strong", "abjuration", "13th", 244, "staff"),
    ("Divination", "Divination", ("Divination",), "73,500 gp", ("73,500",), "Strong", "divination", "13th", 244, "staff"),
    ("Illusion", "Tusion", ("illusion",), "65,000 gp", ("65,000",), "Strong", "illusion", "13th", 244, "staff"),
    ("Illumination", "Ulumination", ("iumination", "Illumination"), "48,250 gp", ("48,250",), "Strong", "evocation", "15th", 244, "staff"),
    ("Necromancy", "Necromancy", ("Necromancy",), "65,000 gp", ("65,000",), "Strong", "necromancy", "13th", 244, "staff"),
    ("Power", "Power", ("Power",), "211,000 gp", ("211,000",), "Strong", "varied", "15th", 244, "staff"),
    ("Swarming Insects", "Swarming Insects", ("Swarming insects",), "24,750 gp", ("24,750",), "Moderate", "conjuration", "9th", 244, "staff"),
    ("Woodlands", "Woodlands", ("Woodlands",), "101,250 gp", ("101,250",), "Moderate", "varied", "13th", 244, "staff"),
]

DMG_METAMAGIC_GAPS = {
    "Empower": (("Lesser", "9,000 gp", ("9,000",)), ("", "32,500 gp", ("32,500",)), ("Greater", "73,000 gp", ("73,000",))),
    "Enlarge": (("Lesser", "3,000 gp", ("3,000",)), ("", "11,000 gp", ("11,000", "17,000")), ("Greater", "24,500 gp", ("24,500",))),
    "Extend": (("Lesser", "3,000 gp", ("3,000",)), ("", "11,000 gp", ("11,000", "17,000")), ("Greater", "24,500 gp", ("24,500",))),
    "Maximize": (("Lesser", "14,000 gp", ("14,000",)), ("", "54,000 gp", ("54,000",)), ("Greater", "121,500 gp", ("121,400", "121,500"))),
    "Quicken": (("Lesser", "35,000 gp", ("35,000",)), ("", "75,500 gp", ("75,500",)), ("Greater", "170,000 gp", ("170,000",))),
    "Silent": (("Lesser", "3,000 gp", ("3,000",)), ("", "11,000 gp", ("11,000",)), ("Greater", "24,500 gp", ("24,500",))),
}

DMG_METAMAGIC_TABLE_ALIASES = {
    ("Enlarge", "Lesser"): ("Metamagic, Enlarge, lester",),
    ("Quicken", "Lesser"): ("Metarmagic, Quicken, lesser",),
}

DMG_ROD_HEADINGS = (
    "Absorption", "Alertness", "Cancellation", "Enemy Detection", "Flailing",
    "Flame Extinguishing", "Immovable Rod", "Lordly Might",
    "Metal and Mineral Detection", "Metamagic Rods", "Metamagic, Empower",
    "Metamagic, Enlarge", "Metamagic, Extend", "Metamagic, Maximize",
    "Metamagic, Quicken", "Metamagic, Silent", "Negation", "Python",
    "Rulership", "Security", "Splendor", "Thunder and Lightning", "Viper",
    "Withering", "Wonder",
)
DMG_STAFF_HEADINGS = (
    "Abjuration", "Charming", "Conjuration", "Defense", "Divination",
    "Earth and Stone", "Enchantment", "Evocation", "Fire", "Frost",
    "Healing", "Tusion", "Ulumination", "Life", "Necromancy", "Passage",
    "Power", "Size Alteration", "Swarming Insects", "Transmutation",
    "Woodlands",
)


def _dmg_line(lines: List[str], pattern: str, start: int = 0) -> Optional[int]:
    rx = re.compile(pattern, re.IGNORECASE)
    return next((i for i in range(start, len(lines)) if rx.search(lines[i])), None)


def _dmg_heading(lines: List[str], heading: str, start: int, end: int) -> Optional[int]:
    rx = re.compile(r"^" + re.escape(heading) + r"\s*:", re.IGNORECASE)
    return next((i for i in range(start, end) if rx.match(lines[i].strip())), None)


def _dmg_table_evidence(lines: List[str], start: int, end: int,
                        aliases: Tuple[str, ...],
                        prices: Tuple[str, ...]) -> bool:
    for raw in lines[start:end]:
        folded = raw.casefold()
        if (any(alias.casefold() in folded for alias in aliases)
                and any(price.casefold() in folded for price in prices)):
            return True
    return False


def _dmg_gap_specs():
    specs = list(DMG_TABLE_GAP_ROWS)
    for base, variants in DMG_METAMAGIC_GAPS.items():
        for size, price, evidence in variants:
            suffix = f", {size}" if size else ""
            name = f"Metamagic, {base}{suffix}"
            aliases = DMG_METAMAGIC_TABLE_ALIASES.get((base, size), (name,))
            specs.append((name, f"Metamagic, {base}", aliases, price,
                          evidence, "Strong", "no school", "17th", 235, "rod"))
    return specs


def detect_dmg_table_gaps(lines: List[str], pages: List[int], book: str,
                          existing_names=()) -> List[Item]:
    """Recover only the 34 table-first rows missed by detect_dmg.

    A row is accepted only when its verified name/price pair is present in the
    book's own table and its own description heading is present in the matching
    section. OCR aliases are explicit and source-verified; output values are
    repaired only where the PDF image itself confirms the character.
    """
    rod_desc = _dmg_line(lines, r"^\s*Rod Descriptions\s*$")
    scrolls = _dmg_line(lines, r"^\s*SCROLLS\s*$", rod_desc or 0)
    staff_start = _dmg_line(lines, r"^\s*STAFFS\s*$", scrolls or 0)
    wands = _dmg_line(lines, r"^\s*WANDS\s*$", staff_start or 0)
    rod_table = _dmg_line(lines, r"7-19.*Ro(?:d|p)s")
    staff_table = _dmg_line(lines, r"7-25.*STAFFS", staff_start or 0)
    staff_table_end = (_dmg_line(lines, r"\[PDF page \d+\]",
                                 (staff_table + 1) if staff_table is not None else 0))
    anchors = (rod_desc, scrolls, staff_start, wands, rod_table,
               staff_table, staff_table_end)
    if any(v is None for v in anchors):
        if len(lines) > 10000:
            print("NO COVERAGE: DMG table-first rods/staffs "
                  "(section or table anchors not found)")
        return []

    table_bounds = {
        "rod": (rod_table, rod_desc),
        "staff": (staff_table, staff_table_end),
    }
    heading_bounds = {
        "rod": (rod_desc, scrolls, DMG_ROD_HEADINGS),
        "staff": (staff_start, wands, DMG_STAFF_HEADINGS),
    }
    existing = {name.casefold() for name in existing_names}
    strict = len(lines) > 10000
    recovered: List[Item] = []

    for (name, heading, aliases, price, evidence, aura, school, caster,
         table_page, section) in _dmg_gap_specs():
        if name.casefold() in existing:
            continue
        ts, te = table_bounds[section]
        hs, he, headings = heading_bounds[section]
        present = (pages[ts] == table_page
                   and _dmg_table_evidence(lines, ts, te, aliases, evidence))
        start = _dmg_heading(lines, heading, hs, he)
        if not present or start is None:
            if strict:
                reason = "table row" if not present else "description heading"
                print(f"NO COVERAGE: DMG {name} ({reason} not found)")
            continue

        next_starts = [_dmg_heading(lines, candidate, start + 1, he)
                       for candidate in headings]
        next_starts = [i for i in next_starts if i is not None]
        end = min(next_starts) if next_starts else he
        if name == "Abjuration":
            end = min(end, staff_table)
        item = Item(name=name, book=book, page=pages[start],
                    start=start, end=end, price=price,
                    caster_level=caster, aura=aura, aura_school=school)
        recovered.append(item)

    recovered.sort(key=lambda item: (item.start, item.name))
    return recovered


def detect_dmg_with_tables(lines: List[str], pages: List[int], book: str) -> List[Item]:
    legacy = detect_dmg(lines, pages, book)
    additions = detect_dmg_table_gaps(
        lines, pages, book, existing_names=[item.name for item in legacy])
    return legacy + additions


# ---------------------------------------------------------------------------
# Arms & Equipment Guide (3.0) detector — "Name: description ... TRAILER", the
# trailer being "Caster Level: Nth; Prerequisites: ...; Market Price: X gp;
# Weight: W" (3.0 has no aura line). Anchor on the Caster Level trailer; name is
# the nearest "Name:" colon-line above. The OCR mangles "Market" to "Markel"
# etc., so the price match is loose.
# ---------------------------------------------------------------------------

AEG_CL = re.compile(r"^Caster Level\s*:\s*(\w+)", re.IGNORECASE)
AEG_PRICE = re.compile(r"Ma\w*\s*Price\s*:\s*([0-9][\d,]*)", re.IGNORECASE)
AEG_WRAPPED_SUFFIX = re.compile(r"^([a-z][A-Za-z'’\-]{2,32}):(?:\s+.*)?$")
AEG_WRAPPED_PREFIX = re.compile(r"^[A-Z][A-Za-z0-9'’ /,()]{2,42}-$")


def _aeg_name_above(lines: List[str], cl_idx: int) -> Optional[Tuple[int, str]]:
    """Find the owning A&EG item title, skipping page furniture.

    The normal search is capped at 40 lines. When an intervening CHAPTER header
    proves that the item crossed a page, it may extend to 120 lines, but always
    stops at the previous Caster Level footer. A wrapped title such as
    ``Headband of Sim-`` / ``plemindedness:`` is joined only when both printed
    fragments are present immediately above the body.
    """
    j, steps, saw_chapter = cl_idx - 1, 0, False
    while j >= 0 and steps < 120:
        s = lines[j].strip()
        if s and not PAGE.search(lines[j]):
            if AEG_CL.match(s):
                break
            normal = DMG_NAME.match(s)
            if normal:
                if not DMG_NAME_REJECT.match(s):
                    return j, normal.group(1).strip()
                if re.match(r"^CHAPTER\b", s, re.IGNORECASE):
                    saw_chapter = True
            suffix = AEG_WRAPPED_SUFFIX.match(s)
            if suffix:
                k = j - 1
                while k >= 0 and j - k <= 3 \
                        and (not lines[k].strip() or PAGE.search(lines[k])):
                    k -= 1
                if k >= 0:
                    prefix = lines[k].strip()
                    if (AEG_WRAPPED_PREFIX.match(prefix)
                            and not DMG_NAME_REJECT.match(prefix)):
                        name = prefix[:-1] + suffix.group(1)
                        return k, re.sub(r"\s+", " ", name).strip()
        j -= 1
        steps += 1
        if steps >= 40 and not saw_chapter:
            break
    return None


def detect_aeg(lines: List[str], pages: List[int], book: str) -> List[Item]:
    n = len(lines)
    items: List[Item] = []
    used = set()
    for i, ln in enumerate(lines):
        clm = AEG_CL.match(ln.strip())
        if not clm:
            continue
        found = _aeg_name_above(lines, i)
        if found is None:
            continue
        name_idx, name = found
        if name_idx in used:
            continue
        used.add(name_idx)
        # gather the trailer (it wraps) for the price
        ttext, k, steps = [ln.strip()], i + 1, 0
        while k < n and steps < 3:
            s = lines[k].strip()
            if PAGE.search(lines[k]):
                k += 1
                continue
            if s == "" or (DMG_NAME.match(s) and not DMG_NAME_REJECT.match(s)):
                break
            ttext.append(s)
            if re.search(r"Weigh", s, re.IGNORECASE):
                break
            k += 1
            steps += 1
        item = Item(name=name, book=book, page=pages[name_idx], start=name_idx,
                    end=min(n, i + 4))
        item.caster_level = clm.group(1)
        pm = AEG_PRICE.search(" ".join(ttext))
        if pm:
            item.price = f"{pm.group(1)} gp"
        items.append(item)
    items.sort(key=lambda it: it.start)
    return items


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[Item]]] = {
    "mic": detect_mic,
    "dmg": detect_dmg_with_tables,
    "aeg": detect_aeg,
}


@dataclass
class Source:
    key: str
    book: str          # provenance label
    path: Path         # relative to CORPUS
    citation: str
    detector: str
    coverage: str = "pending"
    lines: List[str] = field(default_factory=list)
    items: List[Item] = field(default_factory=list)


SOURCES: List[Source] = [
    Source(
        key="mic",
        book="Magic Item Compendium",
        path=Path("D&D 3.5e/Magic and Items/Magic Item Compendium.md"),
        citation="Magic Item Compendium (WotC, 2007), item entries",
        detector="mic",
    ),
    Source(
        key="dmg",
        book="Dungeon Master's Guide v3.5",
        path=Path("D&D 3.5e/Core/Dungeon Masters Guide v3.5.md"),
        citation="Dungeon Master's Guide v3.5, specific items and wondrous "
                 "items; rods Table 7-19 p.235 and descriptions pp.235-238; "
                 "staffs Table 7-25 p.244 and descriptions pp.244-246 "
                 "(weapon/armor special abilities are term_harvest.py's)",
        detector="dmg",
    ),
    Source(
        key="aeg",
        book="Arms and Equipment Guide",
        path=Path("D&D 3.0/Arms And Equipment Guide.md"),
        citation="Arms and Equipment Guide (3.0), magic items",
        detector="aeg",
    ),
]


# ---------------------------------------------------------------------------
# Corpus
# ---------------------------------------------------------------------------


def _pages_for(lines: List[str]) -> List[int]:
    pages: List[int] = []
    page = 0
    for ln in lines:
        m = PAGE.search(ln)
        if m:
            page = int(m.group(1))
        pages.append(page)
    return pages


def _fresh_sources() -> List[Source]:
    return [Source(**{k: getattr(s, k) for k in
                      ("key", "book", "path", "citation", "detector")})
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
            src.items = DETECTORS[src.detector](src.lines, pages, src.book)
            src.coverage = f"ok — {len(src.items)} items from {path.name}"

    def all_items(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for it in src.items:
                yield src, it

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, it in self.all_items(book):
            n = it.name.lower()
            if n == q:
                exact.append((src, it))
            elif q in n:
                partial.append((src, it))
        return exact if exact else partial


# ---------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# MAGIC ITEM INDEX — The New Path",
        "",
        "**Generated by `scripts/item_harvest.py`. Do not hand-edit; rerun",
        "the harvest.** One row per magic item entry found in the item",
        "extractions. The raw text stays on `I:\\Sourcebooks` — use",
        "`python scripts/item_harvest.py --export \"NAME\"` to emit the",
        "translator-ready packet for any row, then hand that packet to the",
        "system-translator skill for the paired 3.5e + GURPS build.",
        "",
        "Every entry names its book and the PDF page the extraction recorded.",
        "This index holds the MECHANICAL vocabulary only — price, body slot,",
        "caster level, and aura — never invented facts; a field left as `—`",
        "is one the OCR did not cleanly yield, recoverable from the source PDF.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.items)
        parsed_well += sum(1 for it in src.items if it.quick_fields() >= 3)
        sources_out.append({
            "key": src.key,
            "book": src.book,
            "citation": src.citation,
            "coverage": src.coverage,
            "items": [asdict(it) for it in src.items],
        })
        md.append(f"## {src.book} — {len(src.items)} items")
        md.append("")
        md.append(f"*Source: {src.citation}.*")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.items:
            md.append("| Item | Tag | Price | Lvl | Body Slot / Property | CL | Aura | Page |")
            md.append("|---|---|---|---|---|---|---|---|")
            for it in src.items:
                slot = it.body_slot or (f"({it.property})" if it.property else "—")
                aura = it.aura or "—"
                if it.aura_school:
                    aura = f"{aura} {it.aura_school}"
                if it.aura_dc:
                    aura = f"{aura} DC{it.aura_dc}"
                md.append(
                    f"| {it.name} | {it.tag or '—'} | {it.price or '—'} | "
                    f"{it.item_level or '—'} | {slot} | {it.caster_level or '—'} | "
                    f"{aura} | {it.page or '—'} |"
                )
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps(
            {
                "generated_by": "scripts/item_harvest.py",
                "corpus": str(corpus.base),
                "total_items": total,
                "sources": sources_out,
            },
            indent=1,
        ),
        encoding="utf-8",
    )
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 6:
        print(f"'{name}' matches {len(hits)} items; narrow with --book or the exact name:")
        for src, it in hits[:20]:
            print(f"  {it.name}   [{it.book}, p.{it.page}]")
        return 1
    packets = []
    for src, it in hits:
        body = [ln for ln in src.lines[it.start:it.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "magic-item-for-translation",
            "instructions": (
                "Feed this packet to the system-translator skill. Both a 3.5e "
                "AND a GURPS treatment are required in the output — a conversion "
                "missing either system is incomplete (that skill's own rule). "
                "The raw_block is OCR text; check oddities (a strange price, a "
                "garbled DC) against the source PDF on I:\\Sourcebooks before "
                "trusting a number."
            ),
            "name": it.name,
            "tag": it.tag,
            "source": {
                "book": it.book, "pdf_page": it.page,
                "extraction": str(corpus.base / src.path),
                "lines": [it.start + 1, it.end],
                "citation": src.citation,
            },
            "parsed": {k: v for k, v in asdict(it).items()
                       if k in ("price", "item_level", "body_slot", "property",
                                "caster_level", "aura", "aura_school", "aura_dc",
                                "activation") and v},
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


# ---------------------------------------------------------------------------
# Selftest — detector against an embedded fixture, then live corpus checks
# ---------------------------------------------------------------------------

FIXTURE = """## [PDF page 72]
BELT OF BATTLE
Price (Item Level): 12,000 gp (13th)
Body Slot: Waist
Caster Level: 9th
Aura: Moderate; (DC 19) transmutation
Activation: — and swift (mental)
Weight: —

This leather belt bears a platinum buckle set
with three small black pearls.

AGILITY, GREATER
[SYNERGY]
Price: +8,000 gp
Caster Level: 15th
Aura: Strong; (DC 22) transmutation

As agility, except the armor grants a +5 resistance bonus.

Cost to Create: 4,000 gp, 320 XP, 8 days.

BELT OF THE
CHAMPION [RELIC]
Price (Item Level): 4,500 gp (9th)
Body Slot: Waist
Caster Level: 20th
Aura: Strong; (DC 25) transmutation

This belt is forged of thick golden links.

THIRD EYE
This small hemispherical crystal has a wide flat facet.
When you issue the proper command thought it adheres.

YOU CHANGED MY MAGIC ITEMS!
Yes, we did. Chances are, if your character owns a magic item.
"""

DMG_FIXTURE = """## [PDF page 218]
Magic Weapon Special Ability Descriptions
Flaming: Upon command, a flaming weapon is sheathed in fire.
Strong evocation; CL 10th; Craft Magic Arms and Armor, flame blade; Price +1 bonus; Weight —.
Specific Weapons
Flame Tongue: This sword deals extra fire damage on a hit.
Strong evocation; CL 12th; Craft Magic Arms and Armor, fireball; Price 20,700 gp; Weight 3 lb.
Boots of Speed: As a free action, the wearer can act as though hasted for 10 rounds/day.
Moderate transmutation; CL 10th; Craft Wondrous Item, haste; Price 12,000 gp; Weight 1 lb.
"""

DMG_TABLE_FIXTURE = """## [PDF page 235]
TABLE 7-19: Rods
78-80 Absorption 50,000 gp
Rod Descriptions
Absorption: This rod stores spell energy.
Strong abjuration; CL 15th; Craft Rod, spell turning; Price 50,000 gp.
SCROLLS
## [PDF page 244]
STAFFS
Abjuration: This staff allows use of shield and dispel magic.
TABLE 7-25: STAFFS
39-43 Abjuration 65,000 gp
## [PDF page 245]
Strong abjuration; CL 13th; Craft Staff, shield; Price 65,000 gp.
Charming: This table row is not part of this focused fixture.
Power: A description heading without a matching table row must not be accepted.
WANDS
"""


AEG_FIXTURE = """## [PDF page 80]
Equestrian's Saddle: Anyone seated in this military saddle feels more comfortable
CHAPTER 4: HIRELINGS AND CREATURES
and competent at equestrianism. The saddle grants a bonus on Ride checks.
Caster Level: 5th; Prerequisites: Craft Wondrous Item;
Market Price: 2,000 gp; Weight: 30 lb.

Horseless Saddle: When the command word is spoken, this riding saddle leaps.
Caster Level: 8th; Prerequisites: Craft Wondrous Item, phantom steed;
Market Price: 43,200 gp; Weight: 25 lb.
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "D&D 3.5e" / "Magic and Items").mkdir(parents=True)
        (d / "D&D 3.5e" / "Magic and Items" / "Magic Item Compendium.md").write_text(
            FIXTURE, encoding="utf-8")
        corpus = Corpus(d, [Source(key="mic", book="Magic Item Compendium",
                                   path=Path("D&D 3.5e/Magic and Items/Magic Item Compendium.md"),
                                   citation="fixture", detector="mic")])
        items = [it for _, it in corpus.all_items()]
        names = [it.name for it in items]
        # Belt of Battle, Agility Greater, and the wrapped + tagged Belt of the
        # Champion are items; Third Eye is a bare category header (no Price) and
        # the sidebar shout is punctuation-tailed. The wrapped name must join
        # across lines and the inline "[RELIC]" tag must be captured.
        want_names = ["Belt Of Battle", "Agility, Greater", "Belt Of The Champion"]
        if names != want_names:
            failures.append(f"fixture detected {names}, wanted {want_names} "
                            f"(Third Eye header and the shout rejected; the "
                            f"Champion name joined across wrapped/tagged lines)")
        else:
            belt = items[0]
            got = (belt.price, belt.item_level, belt.body_slot, belt.caster_level,
                   belt.aura, belt.aura_dc, belt.aura_school)
            want = ("12,000 gp", "13th", "Waist", "9th", "Moderate", "19", "transmutation")
            if got != want:
                failures.append(f"Belt of Battle quick fields {got}, wanted {want}")
            greater = items[1]
            if greater.price != "+8,000 gp" or greater.aura != "Strong" \
                    or greater.tag != "SYNERGY":
                failures.append(f"Agility, Greater parsed price={greater.price!r} "
                                f"aura={greater.aura!r} tag={greater.tag!r}, "
                                f"wanted +8,000 gp / Strong / SYNERGY")
            champ = items[2]
            if champ.tag != "RELIC" or champ.item_level != "9th":
                failures.append(f"Belt of the Champion tag={champ.tag!r} "
                                f"level={champ.item_level!r}, wanted RELIC / 9th")

    # DMG detector: the trailer grammar, with the masked affix section excluded.
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "D&D 3.5e" / "Core").mkdir(parents=True)
        (d / "D&D 3.5e" / "Core" / "Dungeon Masters Guide v3.5.md").write_text(
            DMG_FIXTURE, encoding="utf-8")
        corpus = Corpus(d, [Source(key="dmg", book="Dungeon Master's Guide v3.5",
                                   path=Path("D&D 3.5e/Core/Dungeon Masters Guide v3.5.md"),
                                   citation="fixture", detector="dmg")])
        dmg_items = [it for _, it in corpus.all_items()]
        dmg_names = [it.name for it in dmg_items]
        # Flaming is inside the masked weapon-abilities section (term_harvest's);
        # only the two specific/wondrous items are harvested here.
        if dmg_names != ["Flame Tongue", "Boots of Speed"]:
            failures.append(f"DMG fixture detected {dmg_names}, wanted "
                            f"['Flame Tongue', 'Boots of Speed'] (Flaming affix "
                            f"must be masked out — term_harvest owns it)")
        else:
            ft = dmg_items[0]
            got = (ft.aura, ft.aura_school, ft.caster_level, ft.price)
            if got != ("Strong", "evocation", "12th", "20,700 gp"):
                failures.append(f"Flame Tongue trailer {got}, wanted "
                                f"Strong / evocation / 12th / 20,700 gp")
            bs = dmg_items[1]
            if (bs.aura, bs.caster_level, bs.price) != ("Moderate", "10th", "12,000 gp"):
                failures.append(f"Boots of Speed {(bs.aura, bs.caster_level, bs.price)}, "
                                f"wanted Moderate / 10th / 12,000 gp")

    # Table-first fixture: both the table row and the owning description
    # heading are required. A heading without a table row remains uncovered.
    table_lines = DMG_TABLE_FIXTURE.splitlines()
    table_items = detect_dmg_table_gaps(
        table_lines, _pages_for(table_lines), "Dungeon Master's Guide v3.5")
    table_got = [(it.name, it.price, it.page, it.aura, it.caster_level)
                 for it in table_items]
    table_want = [
        ("Absorption", "50,000 gp", 235, "Strong", "15th"),
        ("Abjuration", "65,000 gp", 244, "Strong", "13th"),
    ]
    if table_got != table_want:
        failures.append(f"DMG table-first fixture {table_got}, wanted "
                        f"{table_want} (Power heading without a table row "
                        "must remain uncovered)")

    # A&EG detector: a running CHAPTER header inside an item body must be
    # skipped while searching backward for the real source-printed name.
    aeg_lines = AEG_FIXTURE.splitlines()
    aeg_items = detect_aeg(aeg_lines, _pages_for(aeg_lines),
                           "Arms and Equipment Guide")
    aeg_names = [it.name for it in aeg_items]
    if aeg_names != ["Equestrian's Saddle", "Horseless Saddle"]:
        failures.append(
            f"A&EG fixture detected {aeg_names}, wanted Equestrian's/Horseless "
            "Saddle (CHAPTER running header must never become an item)")
    elif (aeg_items[0].page, aeg_items[0].caster_level, aeg_items[0].price) != (
            80, "5th", "2,000 gp"):
        failures.append(
            "A&EG fixture failed page/CL/price recovery: "
            f"{(aeg_items[0].page, aeg_items[0].caster_level, aeg_items[0].price)}")

    if base.is_dir() and (base / SOURCES[0].path).exists():
        corpus = Corpus(base, _fresh_sources())
        counts = {s.key: len(s.items) for s in corpus.sources}
        expected_counts = {"mic": 842, "dmg": 250, "aeg": 362}
        if counts != expected_counts:
            failures.append(f"live source counts {counts}, wanted {expected_counts}")
        belt = corpus.find("belt of battle", book="mic")
        if not belt:
            failures.append("Belt of Battle not found in live MIC")
        else:
            b = belt[0][1]
            if b.item_level != "13th" or b.body_slot != "Waist":
                failures.append(f"live Belt of Battle: level={b.item_level!r} "
                                f"slot={b.body_slot!r}, wanted 13th / Waist")
        champ = corpus.find("belt of the champion", book="mic")
        if not champ:
            failures.append("Belt of the Champion (inline [RELIC] tag) not "
                            "recovered from live MIC")
        heal = corpus.find("healing belt", book="mic")
        if not heal:
            failures.append("Healing Belt not found in live MIC")
        # Live DMG source: specific/wondrous items, affixes masked out.
        dmg_src = next((s for s in corpus.sources if s.key == "dmg"), None)
        if dmg_src and (base / dmg_src.path).exists():
            dmg_pages = _pages_for(dmg_src.lines)
            legacy_items = detect_dmg(dmg_src.lines, dmg_pages, dmg_src.book)
            if len(legacy_items) != 216:
                failures.append(f"legacy DMG detector changed to {len(legacy_items)} rows; "
                                "wanted locked checkpoint count 216")
            elif ([asdict(item) for item in dmg_src.items[:216]]
                  != [asdict(item) for item in legacy_items]):
                failures.append("the 216 locked legacy DMG rows are not the unchanged "
                                "prefix of the additive harvest")
            additions = dmg_src.items[len(legacy_items):]
            want_additions = {spec[0] for spec in _dmg_gap_specs()}
            got_additions = {item.name for item in additions}
            if len(additions) != 34 or got_additions != want_additions:
                failures.append(f"DMG table-first additions {len(additions)} / "
                                f"{sorted(got_additions)}, wanted 34 / "
                                f"{sorted(want_additions)}")
            reps = {item.name: item for item in additions}
            for name, wanted in {
                "Absorption": ("50,000 gp", 235, "Strong", "15th"),
                "Metamagic, Maximize, Greater": (
                    "121,500 gp", 237, "Strong", "17th"),
                "Illumination": ("48,250 gp", 245, "Strong", "15th"),
            }.items():
                item = reps.get(name)
                got = ((item.price, item.page, item.aura, item.caster_level)
                       if item else None)
                if got != wanted:
                    failures.append(f"live DMG {name} {got}, wanted {wanted}")
            bs = corpus.find("boots of speed", book="dmg")
            if not bs:
                failures.append("Boots of Speed not found in live DMG")
            elif bs[0][1].aura_school != "transmutation":
                failures.append(f"live Boots of Speed school={bs[0][1].aura_school!r}, "
                                f"wanted transmutation")
            if corpus.find("ghost touch", book="dmg"):
                failures.append("Ghost Touch (a weapon special ability) leaked into "
                                "the DMG item harvest — the affix mask failed")
        aeg_src = next((s for s in corpus.sources if s.key == "aeg"), None)
        if aeg_src and (base / aeg_src.path).exists():
            headers = [it.name for it in aeg_src.items
                       if re.match(r"^(?:CHAPTER|TABLE)\b", it.name, re.IGNORECASE)]
            if headers:
                failures.append(f"A&EG running headers leaked as items: {headers[:5]}")
            for name in ("Equestrian’s Saddle", "Vampire Hunter", "Axe of Shards"):
                if not corpus.find(name, book="aeg"):
                    failures.append(f"live A&EG item not recovered: {name}")
    else:
        print(f"  [SKIP] MIC extraction not found under {base} — fixture checks only")

    for failure in failures:
        print(f"SELFTEST FAIL: {failure}")
    print("selftest: " + ("PASS" if not failures else f"{len(failures)} failure(s)"))
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--corpus", type=Path, default=CORPUS,
                    help="base of the text extractions (default I:\\Sourcebooks\\_text)")
    ap.add_argument("--search", metavar="TEXT", help="substring search on indexed names")
    ap.add_argument("--book", help="restrict to one source (key or book title, e.g. mic)")
    ap.add_argument("--export", metavar="NAME", help="emit a translator-ready packet")
    ap.add_argument("--out", type=Path, help="write the packet here instead of stdout")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest(args.corpus)

    corpus = Corpus(args.corpus, _fresh_sources())

    if args.search:
        q = args.search.lower()
        found = sorted({(it.name, it.book, it.page, it.price or "—")
                        for _, it in corpus.all_items(args.book) if q in it.name.lower()})
        for name, book, page, price in found:
            print(f"  {name}   [{price}, {book}, p.{page}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.items for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.items):5d} items" if src.items else "    0 items"
        print(f"  {src.book:28s} {status}  [{src.coverage}]")
    if not any_ok:
        print("\nNothing harvested at all — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} items across {sum(1 for s in corpus.sources if s.items)} source(s); "
          f"{parsed_well} with 3+ quick fields parsed.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
