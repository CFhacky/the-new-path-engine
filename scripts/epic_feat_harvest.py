#!/usr/bin/env python3
"""epic_feat_harvest.py — D&D 3.5 epic feats and description spans.

WHY THIS ONE IS DIFFERENT. The Epic Level Handbook's text layer is corrupt
(dropped leading characters, Cyrillic bleed, and interleaved columns). The
summary mechanics therefore remain the book-raw vision transcription of Table
1-36 (pp.46-49). Description pages 50-69 are recovered separately from the PDF
page images with two-column OCR, then stored in a derived source whose canonical
headings are restored only from the verified table names. Dire Charge appears in
the description section on p.53 but is omitted from Table 1-36, so it is included
as a separately cited 154th feat.

Five descriptions cross or occupy the genuinely blurred p.60 page image and
cannot be recovered from either image or text layer without invention. Those
rows remain explicit NO COVERAGE records with empty spans.

    reference/epic_feat_index.json — 154 epic feats with type, prerequisites,
                                     citations, and exact description spans
    reference/epic_feat_index.md   — the same, for human eyes

PROVENANCE
    Epic Level Handbook (WotC, 3.5e), Table 1-36 "Epic Feats", pp.46-49; Dire
    Charge description p.53; descriptions pp.50-69. Summary values were read
    from rendered PDF pages. Description bodies are raw two-column Tesseract OCR
    of the rendered page images; only canonical feat headings are restored.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO = Path(__file__).resolve().parent.parent
OUT_JSON = REPO / "reference" / "epic_feat_index.json"
OUT_MD = REPO / "reference" / "epic_feat_index.md"

CORPUS = Path(r"I:\Sourcebooks\_text")
SOURCE_REL = Path(r"D&D 3.5e\DM Toolkits\Epic Level Handbook.epic-feats.ocr-columns.md")
SOURCE = CORPUS / SOURCE_REL
PDF_SOURCE = Path(r"I:\Sourcebooks\D&D 3.5e\DM Toolkits\Epic Level Handbook.pdf")
TESSERACT = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")

BOOK = "Epic Level Handbook"
CITATION = "Epic Level Handbook (WotC, 3.5e), Table 1-36 'Epic Feats', pp.46-49 " \
           "(vision-transcribed from the PDF page images; the OCR text layer is corrupt)"
PAGES = "46-49"
DIRE_CITATION = ("Epic Level Handbook (WotC, 3.5e), Dire Charge description p.53 "
                 "(description-only feat omitted from Table 1-36)")
DIRE_PAGES = "53"

NO_COVERAGE_REASON = (
    "Epic Level Handbook p.60 page image is blurred and its text layer is unusable; "
    "the full description cannot be recovered without fabrication"
)
NO_COVERAGE_NAMES = {
    "Improved Spell Capacity",
    "Improved Spell Resistance",
    "Improved Stunning Fist",
    "Improved Whirlwind Attack",
    "Incite Rage",
}

# (name, type, prerequisites) — transcribed from ELH Table 1-36, pp.46-49.
# type: "" general | W wild | M metamagic | I item-creation | D divine.
_T = [
    ("Additional Magic Item Space", "", "—"),
    ("Armor Skin", "", "—"),
    ("Augmented Alchemy", "", "Int 21, Alchemy 24 ranks"),
    ("Automatic Quicken Spell", "", "Quicken Spell, Spellcraft 30 ranks, ability to cast 9th-level arcane or divine spells"),
    ("Automatic Silent Spell", "", "Silent Spell, Spellcraft 24 ranks, ability to cast 9th-level arcane or divine spells"),
    ("Automatic Still Spell", "", "Still Spell, Spellcraft 27 ranks, ability to cast 9th-level arcane or divine spells"),
    ("Bane of Enemies", "", "Wilderness Lore 24 ranks, five or more favored enemies (as the ranger class feature)"),
    ("Death of Enemies", "", "Bane of Enemies, Wilderness Lore 30 ranks"),
    ("Beast Companion", "W", "Beast Wild Shape, Master Wild Shape, Knowledge (nature) 24 ranks, wild shape 6/day"),
    ("Beast Wild Shape", "W", "Knowledge (nature) 24 ranks, wild shape 6/day"),
    ("Dragon Wild Shape", "W", "Wis 30, Beast Wild Shape, Knowledge (nature) 30 ranks, wild shape 6/day"),
    ("Magical Beast Wild Shape", "W", "Wis 25, Beast Wild Shape, Knowledge (nature) 27 ranks, wild shape 6/day"),
    ("Plant Wild Shape", "W", "Beast Wild Shape, Knowledge (nature) 24 ranks, wild shape 6/day"),
    ("Vermin Wild Shape", "W", "Beast Wild Shape, Knowledge (nature) 24 ranks, wild shape 6/day"),
    ("Blinding Speed", "", "Dex 25"),
    ("Bonus Domain", "", "Wis 21, ability to cast 9th-level divine spells"),
    ("Bulwark of Defense", "", "Con 25, defensive stance 3/day"),
    ("Chaotic Rage", "", "Rage 5/day, chaotic alignment"),
    ("Combat Archery", "", "Dodge, Mobility, Point Blank Shot"),
    ("Craft Epic Magic Arms and Armor", "I", "Craft Magic Arms and Armor, Knowledge (arcana) 28 ranks, Spellcraft 28 ranks"),
    ("Craft Epic Rod", "I", "Craft Rod, Knowledge (arcana) 32 ranks, Spellcraft 32 ranks"),
    ("Craft Epic Staff", "I", "Craft Staff, Knowledge (arcana) 35 ranks, Spellcraft 35 ranks"),
    ("Craft Epic Wondrous Item", "I", "Craft Wondrous Item, Knowledge (arcana) 26 ranks, Spellcraft 26 ranks"),
    ("Damage Reduction", "", "Con 21"),
    ("Deafening Song", "", "Perform 24 ranks, bardic music class feature"),
    ("Hindering Song", "", "Deafening Song, Perform 21 ranks, bardic music class feature"),
    ("Dexterous Fortitude", "", "Dex 25, slippery mind class feature"),
    ("Dexterous Will", "", "Dex 25, slippery mind class feature"),
    ("Diminutive Wild Shape", "W", "Ability to wild shape into a Huge animal"),
    ("Dire Charge", "", "Improved Initiative"),
    ("Fine Wild Shape", "W", "Ability to wild shape into a Diminutive creature"),
    ("Distant Shot", "", "Dex 25, Far Shot, Point Blank Shot, Spot 20 ranks"),
    ("Efficient Item Creation", "", "Item creation feat to be selected, Knowledge (arcana) 24 ranks, Spellcraft 24 ranks"),
    ("Energy Resistance", "", "—"),
    ("Enhance Spell", "M", "Maximize Spell"),
    ("Epic Dodge", "", "Dex 25, Dodge, Tumble 30 ranks, improved evasion, defensive roll class feature"),
    ("Epic Endurance", "", "Con 25, Endurance"),
    ("Epic Fortitude", "", "—"),
    ("Epic Inspiration", "", "Cha 25, Perform 30 ranks, bardic music class feature"),
    ("Epic Leadership", "", "Cha 25, Leadership, Leadership score 25"),
    ("Legendary Commander", "", "Cha 25, Epic Leadership, Leadership, Diplomacy 30 ranks, must rule own kingdom and have a stronghold"),
    ("Epic Prowess", "", "—"),
    ("Epic Reflexes", "", "—"),
    ("Epic Reputation", "", "—"),
    ("Epic Skill Focus", "", "20 ranks in the skill selected"),
    ("Epic Speed", "", "Dex 21, Run"),
    ("Epic Spell Focus", "", "Greater Spell Focus and Spell Focus in the school selected, ability to cast at least one 9th-level spell of the school"),
    ("Epic Spell Penetration", "", "Greater Spell Penetration, Spell Penetration"),
    ("Epic Spellcasting", "", "Spellcraft 24 ranks, Knowledge (arcana) 24 ranks and ability to cast 9th-level arcane spells (OR the Knowledge religion/nature divine variants)"),
    ("Epic Toughness", "", "—"),
    ("Epic Weapon Focus", "", "Weapon Focus in the weapon to be chosen"),
    ("Epic Weapon Specialization", "", "Epic Weapon Focus, Weapon Focus, Weapon Specialization (all in the weapon to be chosen)"),
    ("Epic Will", "", "—"),
    ("Exceptional Deflection", "", "Dex 21, Wis 19, Deflect Arrows, Improved Unarmed Strike"),
    ("Extended Life Span", "", "—"),
    ("Familiar Spell", "", "Int 25 (if your spellcasting is controlled by Intelligence) OR Cha 25 (if controlled by Charisma)"),
    ("Fast Healing", "", "Con 25"),
    ("Forge Epic Ring", "I", "Forge Ring, Knowledge (arcana) 35 ranks, Spellcraft 35 ranks"),
    ("Gargantuan Wild Shape", "W", "Ability to wild shape into a Huge animal"),
    ("Colossal Wild Shape", "W", "Ability to wild shape into a Gargantuan creature"),
    ("Great Charisma", "", "—"),
    ("Great Constitution", "", "—"),
    ("Great Dexterity", "", "—"),
    ("Great Intelligence", "", "—"),
    ("Great Smiting", "", "Cha 25, smite ability (from class feature or domain granted power)"),
    ("Great Strength", "", "—"),
    ("Great Wisdom", "", "—"),
    ("Group Inspiration", "", "Perform 30 ranks, bardic music class feature"),
    ("Holy Strike", "", "Smite evil class feature, any good alignment"),
    ("Ignore Material Components", "", "Eschew Materials, Spellcraft 25 ranks, ability to cast 9th-level arcane or divine spells"),
    ("Improved Alignment-Based Casting", "", "Access to domain of Chaos, Evil, Good, or Law, alignment must match domain chosen, ability to cast 9th-level divine spells"),
    ("Improved Arrow of Death", "", "Dex 19, Wis 19, Point Blank Shot, Precise Shot, arrow of death class feature"),
    ("Improved Aura of Courage", "", "Cha 25, aura of courage class feature"),
    ("Improved Aura of Despair", "", "Cha 25, aura of despair class feature"),
    ("Improved Combat Casting", "", "Combat Casting, Concentration 25 ranks"),
    ("Improved Combat Reflexes", "", "Dex 21, Combat Reflexes"),
    ("Improved Darkvision", "", "Darkvision"),
    ("Improved Death Attack", "", "Death attack class feature, sneak attack +5d6"),
    ("Improved Elemental Wild Shape", "W", "Wis 25, ability to wild shape into an elemental"),
    ("Improved Favored Enemy", "", "Five or more favored enemies"),
    ("Improved Heighten Spell", "M", "Heighten Spell, Spellcraft 20 ranks"),
    ("Improved Ki Strike", "", "Wis 21, Ki strike +3"),
    ("Improved Low-Light Vision", "", "Low-light vision"),
    ("Improved Manifestation", "", "Ability to manifest powers of the normal maximum level in at least one psionic class"),
    ("Improved Metamagic", "", "Four metamagic feats, Spellcraft 30 ranks"),
    ("Improved Manyshot", "", "Dex 19, base attack bonus +21, Manyshot, Point Blank Shot, Rapid Shot"),
    ("Improved Sneak Attack", "", "Sneak attack +8d6"),
    ("Improved Spell Capacity", "", "Ability to cast spells of the normal maximum spell level in at least one spellcasting class"),
    ("Improved Spell Resistance", "", "Must have spell resistance from a feat, class feature, or other permanent effect"),
    ("Improved Stunning Fist", "", "Dex 19, Wis 19, Improved Unarmed Strike, Stunning Fist"),
    ("Improved Whirlwind Attack", "", "Int 13, Dex 23, Dodge, Expertise, Mobility, Spring Attack, Whirlwind Attack"),
    ("Incite Rage", "", "Cha 25, greater rage class feature"),
    ("Infinite Deflection", "", "Dex 25, Combat Reflexes, Deflect Arrows, Improved Unarmed Strike"),
    ("Inspire Excellence", "", "Perform 30 ranks, bardic music class feature"),
    ("Instant Reload", "", "Quick Draw, Rapid Reload, Weapon Focus (crossbow type to be selected)"),
    ("Intensify Spell", "M", "Empower Spell, Maximize Spell, Spellcraft 30 ranks, ability to cast 9th-level arcane or divine spells"),
    ("Keen Strike", "", "Str 23, Wis 23, Improved Critical (unarmed strike), ki strike +3"),
    ("Vorpal Strike", "", "Str 25, Wis 25, Improved Critical (unarmed strike), Improved Unarmed Strike, Keen Strike, Stunning Fist, ki strike +5"),
    ("Lasting Inspiration", "", "Perform 25 ranks, bardic music class feature"),
    ("Legendary Climber", "", "Dex 21, Balance 12 ranks, Climb 24 ranks"),
    ("Legendary Leaper", "", "Jump 24 ranks"),
    ("Legendary Rider", "", "Ride 24 ranks"),
    ("Legendary Tracker", "", "Wis 25, Track, Knowledge (nature) 30 ranks, Wilderness Lore 30 ranks"),
    ("Legendary Wrestler", "", "Str 21, Dex 21, Improved Unarmed Strike, Escape Artist 15 ranks"),
    ("Lingering Damage", "", "Sneak attack +8d6, crippling strike class feature"),
    ("Master Staff", "", "Craft Staff, Spellcraft 15 ranks"),
    ("Master Wand", "", "Craft Wand, Spellcraft 15 ranks"),
    ("Mighty Rage", "", "Str 21, Con 21, greater rage class feature"),
    ("Mobile Defense", "", "Dex 15, Dodge, Mobility, Spring Attack, defensive stance 5/day class feature"),
    ("Multispell", "", "Quicken Spell, ability to cast 9th-level arcane or divine spells"),
    ("Multiweapon Rend", "", "Dex 15, base attack bonus +9, three or more hands, Multidexterity, Multiweapon Fighting"),
    ("Music of the Gods", "", "Cha 25, Perform 30 ranks, bardic music class feature"),
    ("Negative Energy Burst", "D", "Cha 25, ability to rebuke or command undead, ability to cast inflict critical wounds, an evil alignment"),
    ("Overwhelming Critical", "", "Str 23, Cleave, Great Cleave, Improved Critical (weapon to be chosen), Power Attack, Weapon Focus (weapon to be chosen)"),
    ("Devastating Critical", "", "Str 25, Cleave, Great Cleave, Improved Critical (weapon to be chosen), Overwhelming Critical (weapon to be chosen), Power Attack, Weapon Focus (weapon to be chosen)"),
    ("Penetrate Damage Reduction", "", "—"),
    ("Perfect Health", "", "Con 25, Great Fortitude"),
    ("Perfect Multiweapon Fighting", "", "Dex 25, three or more hands, Greater Multiweapon Fighting, Multidexterity, Multiweapon Fighting"),
    ("Perfect Two-Weapon Fighting", "", "Dex 25, Ambidexterity, Greater Two-Weapon Fighting, Improved Two-Weapon Fighting, Two-Weapon Fighting"),
    ("Permanent Emanation", "", "Spellcraft 25 ranks, ability to cast the spell to be made permanent"),
    ("Planar Turning", "", "Wis 25, Cha 25, ability to turn or rebuke undead"),
    ("Polyglot", "", "Int 25, Speak Language (five languages)"),
    ("Positive Energy Aura", "", "Cha 25, ability to turn undead, ability to cast dispel evil"),
    ("Ranged Inspiration", "", "Perform 25 ranks, bardic music class feature"),
    ("Rapid Inspiration", "", "Perform 30 ranks, bardic music class feature"),
    ("Reactive Countersong", "", "Combat Reflexes, Perform 30 ranks, bardic music class feature"),
    ("Reflect Arrows", "", "Dex 25, Deflect Arrows, Improved Unarmed Strike"),
    ("Righteous Strike", "", "Wis 19, Improved Unarmed Strike, Stunning Fist, any lawful alignment"),
    ("Ruinous Rage", "", "Str 25, Power Attack, Sunder, rage 5/day"),
    ("Scribe Epic Scroll", "I", "Scribe Scroll, Knowledge (arcana) 24 ranks, Spellcraft 24 ranks"),
    ("Self-Concealment", "", "Dex 30, Hide 30 ranks, Tumble 30 ranks, improved evasion"),
    ("Shattering Strike", "", "Epic Weapon Focus (unarmed strike), Weapon Focus (unarmed strike), Concentration 25 ranks, ki strike +3"),
    ("Sneak Attack of Opportunity", "", "Sneak attack +8d6, opportunist class feature"),
    ("Spectral Strike", "", "Wis 19, ability to turn or rebuke undead"),
    ("Spell Knowledge", "", "Ability to cast the maximum spell level of an arcane spellcasting class"),
    ("Spell Opportunity", "", "Combat Casting, Combat Reflexes, Quicken Spell, Spellcraft 25 ranks"),
    ("Spell Stowaway", "", "Spellcraft 24 ranks, caster level 12th"),
    ("Spellcasting Harrier", "", "Combat Reflexes"),
    ("Spontaneous Domain Access", "", "Wis 25, Spellcraft 30 ranks, ability to cast 9th-level divine spells"),
    ("Spontaneous Spell", "", "Spellcraft 25 ranks, ability to cast the maximum normal spell level of at least one spellcasting class"),
    ("Storm of Throws", "", "Dex 23, Point Blank Shot, Quick Draw, Rapid Shot"),
    ("Superior Initiative", "", "Improved Initiative"),
    ("Swarm of Arrows", "", "Dex 23, Point Blank Shot, Rapid Shot, Weapon Focus (type of bow used)"),
    ("Tenacious Magic", "", "Spellcraft 15 ranks, ability to cast the spell to be made tenacious"),
    ("Terrifying Rage", "", "Intimidate 25 ranks, rage 5/day"),
    ("Thundering Rage", "", "Str 25, rage 5/day"),
    ("Trap Sense", "", "Search 25 ranks, Spot 25 ranks, ability to find traps as a rogue"),
    ("Two-Weapon Rend", "", "Dex 15, base attack bonus +9, Ambidexterity, Improved Two-Weapon Fighting, Two-Weapon Fighting"),
    ("Uncanny Accuracy", "", "Dex 21, Point Blank Shot, Precise Shot, Spot 20 ranks"),
    ("Undead Mastery", "D", "Cha 21, ability to rebuke or command undead"),
    ("Zone of Animation", "D", "Cha 25, Undead Mastery, ability to rebuke or command undead"),
    ("Unholy Strike", "", "Smite good class feature, any evil alignment"),
    ("Widen Aura of Courage", "", "Cha 25, aura of courage class feature"),
    ("Widen Aura of Despair", "", "Cha 25, aura of despair class feature"),
]
TYPE_NAME = {"": "general", "W": "wild", "M": "metamagic", "I": "item-creation", "D": "divine"}
TYPE_LABEL = {
    "": "GENERAL",
    "W": "WILD",
    "M": "METAMAGIC",
    "I": "ITEM CREATION",
    "D": "DIVINE",
}

# Twenty-nine description headings have no usable text-layer name. These page,
# column, and y anchors were verified against the rendered PDF pages. The other
# 125 headings retain a readable [Epic] marker and are assigned in book order.
MANUAL_HEADINGS: Dict[str, Tuple[int, int, float]] = {
    "Additional Magic Item Space": (50, 0, 578.0),
    "Armor Skin": (50, 0, 826.0),
    "Augmented Alchemy": (50, 1, 548.0),
    "Epic Spellcasting": (55, 0, 548.0),
    "Epic Toughness": (55, 1, 395.0),
    "Epic Weapon Focus": (55, 1, 474.0),
    "Epic Weapon Specialization": (55, 1, 634.0),
    "Epic Will": (55, 1, 812.0),
    "Exceptional Deflection": (55, 1, 868.0),
    "Gargantuan Wild Shape": (56, 1, 255.0),
    "Great Strength": (57, 0, 55.0),
    "Improved Darkvision": (58, 0, 55.0),
    "Improved Death Attack": (58, 0, 216.0),
    "Improved Spell Resistance": (60, 0, 590.0),
    "Improved Stunning Fist": (60, 0, 810.0),
    "Improved Whirlwind Attack": (60, 1, 500.0),
    "Incite Rage": (60, 1, 780.0),
    "Lingering Damage": (62, 1, 55.0),
    "Magical Beast Wild Shape": (62, 1, 194.0),
    "Mobile Defense": (63, 0, 190.0),
    "Multispell": (63, 0, 330.0),
    "Plant Wild Shape": (65, 0, 560.0),
    "Polyglot": (65, 0, 688.0),
    "Positive Energy Aura": (65, 0, 780.0),
    "Ranged Inspiration": (65, 1, 645.0),
    "Spontaneous Spell": (67, 1, 345.0),
    "Storm of Throws": (67, 1, 590.0),
    "Superior Initiative": (67, 1, 750.0),
    "Swarm of Arrows": (67, 1, 855.0),
}

SOURCE_PAGE_RE = re.compile(r"^## \[PDF pages? (\d+)(?:-(\d+))?\]$")
SOURCE_HEADING_RE = re.compile(
    r"^(.+?) \[(GENERAL|WILD|METAMAGIC|ITEM CREATION|DIVINE)\] \[EPIC\]$"
)


def _name_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.casefold())


def _records() -> Dict[str, Tuple[str, str]]:
    records = {name: (ty, prereq) for name, ty, prereq in _T}
    if len(records) != len(_T):
        raise AssertionError("duplicate epic-feat names in the governing table")
    return records


def _source_hash() -> Optional[str]:
    if not SOURCE.is_file():
        return None
    return hashlib.sha256(SOURCE.read_bytes()).hexdigest()


def _ocr_lanes(doc) -> List[dict]:
    try:
        import fitz
        import pytesseract
        from PIL import Image, ImageFilter, ImageOps
        from io import BytesIO
    except Exception as exc:
        raise RuntimeError(f"OCR dependencies unavailable: {exc}") from exc

    if not TESSERACT.is_file():
        raise RuntimeError(f"Tesseract not found at {TESSERACT}")
    pytesseract.pytesseract.tesseract_cmd = str(TESSERACT)

    lanes: List[dict] = []
    for book_page in range(50, 70):
        page = doc[book_page - 1]
        for column, (x0, x1) in enumerate(((55, 355), (365, 690))):
            clip = fitz.Rect(x0, 55, x1, 945)
            pix = page.get_pixmap(
                matrix=fitz.Matrix(4, 4),
                clip=clip,
                alpha=False,
            )
            image = Image.open(BytesIO(pix.tobytes("png"))).convert("L")
            image = ImageOps.autocontrast(image, cutoff=1)
            image = image.filter(ImageFilter.UnsharpMask(radius=1, percent=130, threshold=2))
            data = pytesseract.image_to_data(
                image,
                config="--oem 3 --psm 6",
                output_type=pytesseract.Output.DICT,
            )
            groups: Dict[Tuple[int, int, int], List[int]] = defaultdict(list)
            for index, token in enumerate(data["text"]):
                if token.strip():
                    key = (
                        data["block_num"][index],
                        data["par_num"][index],
                        data["line_num"][index],
                    )
                    groups[key].append(index)
            lines: List[dict] = []
            for indexes in groups.values():
                indexes.sort(key=lambda index: data["left"][index])
                text = " ".join(data["text"][index] for index in indexes).strip()
                lines.append(
                    {
                        "top": 55 + min(data["top"][index] for index in indexes) / 4,
                        "text": text,
                    }
                )
            lines.sort(key=lambda row: row["top"])
            lanes.append({"page": book_page, "column": column, "lines": lines})
        print(f"OCR source extraction: page {book_page}/69", flush=True)
    return lanes


def _marker_positions(doc, names: Sequence[str]) -> Dict[str, Tuple[int, int, float]]:
    markers: List[Tuple[int, int, float, str]] = []
    for book_page in range(50, 70):
        page = doc[book_page - 1]
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                raw = "".join(span["text"] for span in line["spans"]).strip()
                if "Epic]" not in raw and "[Epic" not in raw:
                    continue
                x0, y0, x1, _ = line["bbox"]
                column = 0 if (x0 + x1) / 2 < 350 else 1
                markers.append((book_page, column, float(y0), raw))
    markers.sort(key=lambda row: (row[0], row[1], row[2]))

    automatic = [name for name in names if name not in MANUAL_HEADINGS]
    if len(markers) != 125 or len(automatic) != 125:
        raise RuntimeError(
            f"heading reconciliation failed: {len(markers)} markers for "
            f"{len(automatic)} automatic names"
        )
    positions = {
        name: (page, column, y)
        for name, (page, column, y, _) in zip(automatic, markers)
    }
    positions.update(MANUAL_HEADINGS)

    probes = {
        "Automatic Quicken Spell": (50, 1),
        "Dire Charge": (53, 0),
        "Improved Elemental Wild Shape": (58, 0),
        "Improved Low-Light Vision": (58, 1),
        "Zone of Animation": (69, 0),
    }
    for name, expected in probes.items():
        if positions[name][:2] != expected:
            raise RuntimeError(
                f"heading reconciliation drifted for {name}: "
                f"{positions[name][:2]} != {expected}"
            )
    return positions


def _meaningful_ocr(lines: Sequence[dict], low: float, high: float) -> List[str]:
    out: List[str] = []
    for row in lines:
        if low <= row["top"] < high:
            text = row["text"].strip()
            if sum(char.isalnum() for char in text) >= 2:
                out.append(text)
    return out


def _generic_body(
    name: str,
    next_name: Optional[str],
    positions: Dict[str, Tuple[int, int, float]],
    lane_map: Dict[Tuple[int, int], List[dict]],
    lane_keys: Sequence[Tuple[int, int]],
) -> Tuple[List[str], List[int]]:
    page, column, y = positions[name]
    lane_index = {key: index for index, key in enumerate(lane_keys)}
    start_lane = lane_index[(page, column)]
    if next_name is None:
        next_page, next_column, next_y = 69, 0, 508.0
    else:
        next_page, next_column, next_y = positions[next_name]
    end_lane = lane_index[(next_page, next_column)]

    body: List[str] = []
    pages = set()
    for index in range(start_lane, end_lane + 1):
        lane_page, lane_column = lane_keys[index]
        low = y + 15 if index == start_lane else float("-inf")
        high = next_y - 8 if index == end_lane else float("inf")
        selected = _meaningful_ocr(lane_map[(lane_page, lane_column)], low, high)
        if selected:
            body.extend(selected)
            pages.add(lane_page)
    return body, sorted(pages)


def _description_body(
    name: str,
    next_name: Optional[str],
    positions: Dict[str, Tuple[int, int, float]],
    lane_map: Dict[Tuple[int, int], List[dict]],
    lane_keys: Sequence[Tuple[int, int]],
) -> Tuple[List[str], List[int]]:
    take = lambda page, column, low, high: _meaningful_ocr(
        lane_map[(page, column)], low, high
    )

    if name == "Perfect Two-Weapon Fighting":
        body = take(64, 0, positions[name][2] + 15, 610)
        body += take(64, 1, float("-inf"), 276)
        return body, [64]

    if name == "Planar Turning":
        body = take(64, 1, positions[name][2] + 15, 600)
        body += take(65, 0, 470, MANUAL_HEADINGS["Plant Wild Shape"][2] - 8)
        body.append("PLANAR TURNING, AN ALTERNATIVE [EPIC]")
        body += take(64, 0, 638, float("inf"))
        body += take(64, 1, 627, float("inf"))
        return body, [64, 65]

    return _generic_body(name, next_name, positions, lane_map, lane_keys)


def extract_description_source() -> int:
    if not PDF_SOURCE.is_file():
        print(f"NO COVERAGE: {BOOK} description extraction (missing PDF: {PDF_SOURCE})")
        return 1
    try:
        import fitz
    except Exception as exc:
        print(f"NO COVERAGE: {BOOK} description extraction (PyMuPDF unavailable: {exc})")
        return 1

    records = _records()
    names = sorted(records)
    try:
        doc = fitz.open(PDF_SOURCE)
        positions = _marker_positions(doc, names)
        lanes = _ocr_lanes(doc)
    except Exception as exc:
        print(f"NO COVERAGE: {BOOK} description extraction ({exc})")
        return 1

    lane_map = {
        (lane["page"], lane["column"]): lane["lines"]
        for lane in lanes
    }
    lane_keys = sorted(lane_map)
    ordered = sorted(names, key=lambda name: positions[name])
    if ordered != names:
        raise RuntimeError("description heading anchors are not in canonical book order")

    chunks = [
        "# EPIC FEAT DESCRIPTION EXTRACTION",
        "",
        "Derived from Epic Level Handbook PDF page images, pp. 50-69.",
        "Two-column OCR is preserved raw. Feat headings alone are restored from",
        "the book-verified Table 1-36 transcription and Dire Charge on p.53.",
        "",
    ]
    recovered = 0
    for index, name in enumerate(names):
        if name in NO_COVERAGE_NAMES:
            continue
        next_name = names[index + 1] if index + 1 < len(names) else None
        body, pages = _description_body(name, next_name, positions, lane_map, lane_keys)
        if not body:
            raise RuntimeError(f"empty OCR description block for {name}")
        page_label = str(pages[0]) if len(pages) == 1 else f"{pages[0]}-{pages[-1]}"
        type_code = records[name][0]
        chunks.extend(
            [
                f"## [PDF pages {page_label}]",
                f"{name.upper()} [{TYPE_LABEL[type_code]}] [EPIC]",
                *body,
                "",
            ]
        )
        recovered += 1

    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    SOURCE.write_text("\n".join(chunks).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {SOURCE}")
    print(f"{recovered}/{len(names)} epic-feat description spans recovered")
    for name in sorted(NO_COVERAGE_NAMES):
        print(f"NO COVERAGE: {name} full description ({NO_COVERAGE_REASON})")
    return 0


@dataclass(frozen=True)
class DescriptionSpan:
    page: int
    pages: str
    start: int
    end: int
    type_label: str


@dataclass
class EpicFeat:
    name: str
    book: str
    type: str
    prerequisites: Optional[str]
    citation: str
    pages: str
    page: int
    description_pages: str
    start: int
    end: int
    soft: Optional[str]


def detect_description_spans(
    lines: Sequence[str],
    canonical_names: Sequence[str],
) -> Dict[str, DescriptionSpan]:
    canonical = {_name_key(name): name for name in canonical_names}
    headings: List[Tuple[str, int, int, str, str]] = []
    marker_index = -1
    marker_page = 0
    marker_pages = ""

    for index, line in enumerate(lines):
        page_match = SOURCE_PAGE_RE.match(line.strip())
        if page_match:
            marker_index = index
            marker_page = int(page_match.group(1))
            marker_pages = (
                marker_page
                if page_match.group(2) is None
                else f"{marker_page}-{int(page_match.group(2))}"
            )
            marker_pages = str(marker_pages)
            continue

        heading_match = SOURCE_HEADING_RE.match(line.strip())
        if not heading_match:
            continue
        if marker_index < 0:
            raise ValueError(f"description heading before page marker at line {index + 1}")
        key = _name_key(heading_match.group(1))
        if key not in canonical:
            raise ValueError(f"unknown epic-feat heading at line {index + 1}: {line!r}")
        headings.append(
            (
                canonical[key],
                marker_index,
                index,
                marker_pages,
                heading_match.group(2),
            )
        )

    spans: Dict[str, DescriptionSpan] = {}
    for position, (name, _, start, pages, type_label) in enumerate(headings):
        end = headings[position + 1][1] if position + 1 < len(headings) else len(lines)
        while end > start and not lines[end - 1].strip():
            end -= 1
        if name in spans:
            raise ValueError(f"duplicate epic-feat description heading: {name}")
        spans[name] = DescriptionSpan(
            page=int(pages.split("-", 1)[0]),
            pages=pages,
            start=start,
            end=end,
            type_label=type_label,
        )
    return spans


def _source_lines() -> List[str]:
    if not SOURCE.is_file():
        return []
    return SOURCE.read_text(encoding="utf-8").splitlines()


def build(lines: Optional[Sequence[str]] = None) -> List[EpicFeat]:
    records = _records()
    source_lines = list(lines) if lines is not None else _source_lines()
    spans = detect_description_spans(source_lines, records) if source_lines else {}
    no_coverage_pages = {
        "Improved Spell Capacity": (59, "59-60"),
        "Improved Spell Resistance": (60, "60"),
        "Improved Stunning Fist": (60, "60"),
        "Improved Whirlwind Attack": (60, "60"),
        "Incite Rage": (60, "60-61"),
    }

    out: List[EpicFeat] = []
    for name, type_code, prereq in _T:
        span = spans.get(name)
        if span:
            page = span.page
            description_pages = span.pages
            start, end = span.start, span.end
            soft = None
        else:
            page, description_pages = no_coverage_pages.get(name, (0, ""))
            start = end = 0
            reason = (
                NO_COVERAGE_REASON
                if name in NO_COVERAGE_NAMES
                else "derived description extraction is missing"
            )
            soft = f"NO COVERAGE: full description ({reason})"

        citation = DIRE_CITATION if name == "Dire Charge" else CITATION
        table_pages = DIRE_PAGES if name == "Dire Charge" else PAGES
        out.append(
            EpicFeat(
                name=name,
                book=BOOK,
                type=TYPE_NAME[type_code],
                prerequisites=None if prereq in ("—", "") else prereq,
                citation=citation,
                pages=table_pages,
                page=page,
                description_pages=description_pages,
                start=start,
                end=end,
                soft=soft,
            )
        )
    return out


def write_index() -> Tuple[int, int]:
    if not SOURCE.is_file():
        raise FileNotFoundError(
            f"derived description extraction is missing: {SOURCE}; "
            "run --extract-source first"
        )

    feats = build()
    recovered = sum(feat.start < feat.end for feat in feats)
    by_type = Counter(feat.type for feat in feats)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    for feat in feats:
        if feat.soft:
            print(f"NO COVERAGE: {feat.name} full description ({NO_COVERAGE_REASON})")

    md: List[str] = [
        "# EPIC FEAT INDEX — The New Path",
        "",
        "**Generated by `scripts/epic_feat_harvest.py`. Do not hand-edit; rerun",
        "the harvest.** D&D 3.5 epic feats from the Epic Level Handbook. Summary",
        "mechanics are book-raw vision transcription of Table 1-36 (pp.46-49).",
        "Dire Charge is the description-only feat on p.53 that the table omits.",
        "Description spans point into a derived, raw two-column OCR extraction of",
        "the rendered PDF pages 50-69; only the canonical headings were restored.",
        "The five p.60-dependent descriptions remain explicit NO COVERAGE gaps.",
        "",
        f"*{len(feats)} epic feats — {recovered} full description spans, "
        f"{len(feats) - recovered} NO COVERAGE; "
        + ", ".join(f"{count} {kind}" for kind, count in sorted(by_type.items()))
        + ".*",
        "",
        "| Epic Feat | Type | Prerequisites | Description pages | Status |",
        "|---|---|---|---:|---|",
    ]
    for feat in feats:
        prereq = (feat.prerequisites or "—").replace("|", "\\|")
        status = (
            f"lines {feat.start}-{feat.end}"
            if feat.start < feat.end
            else feat.soft or "NO COVERAGE"
        )
        md.append(
            f"| {feat.name} | {feat.type} | {prereq} | "
            f"{feat.description_pages or '—'} | {status} |"
        )
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    payload = {
        "generated_by": "scripts/epic_feat_harvest.py",
        "corpus": str(CORPUS),
        "source_path": str(SOURCE_REL),
        "source_sha256": _source_hash(),
        "book": BOOK,
        "citation": CITATION,
        "pages": PAGES,
        "note": (
            "Table 1-36 mechanics are vision-transcribed from the ELH PDF page "
            "images because its text layer is corrupt. Dire Charge is separately "
            "cited to its p.53 description because the table omits it. Full spans "
            "slice a raw, two-column OCR extraction of rendered pages 50-69; only "
            "canonical headings were restored. Five descriptions dependent on "
            "unreadable p.60 remain explicit NO COVERAGE rows."
        ),
        "total_epic_feats": len(feats),
        "full_description_spans": recovered,
        "no_coverage": len(feats) - recovered,
        "by_type": dict(sorted(by_type.items())),
        "epic_feats": [asdict(feat) for feat in feats],
    }
    OUT_JSON.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8")
    return len(feats), recovered


def export_packet(query: str, out_path: Optional[Path]) -> int:
    feats = build()
    exact = [feat for feat in feats if feat.name.casefold() == query.casefold()]
    matches = exact or [
        feat for feat in feats if query.casefold() in feat.name.casefold()
    ]
    if not matches:
        print(f"NO COVERAGE: epic feat matching {query!r} (not found)")
        return 1
    if len(matches) != 1:
        print(f"ambiguous epic-feat query {query!r}:")
        for feat in matches:
            print(f"  {feat.name}")
        return 1

    feat = matches[0]
    lines = _source_lines()
    raw_block = (
        "\n".join(lines[feat.start:feat.end]).strip()
        if feat.start < feat.end
        else ""
    )
    packet = {
        "packet": "the-new-path-engine/epic-feat/v1",
        "instructions": (
            "Use the parsed table mechanics and book-raw OCR block only. "
            "Do not repair uncertain OCR or invent missing values."
        ),
        "name": feat.name,
        "source": {
            "book": feat.book,
            "pdf_page": feat.page,
            "pages": feat.description_pages,
            "extraction": str(SOURCE_REL),
            "lines": [feat.start, feat.end],
            "citation": feat.citation,
        },
        "parsed": {
            "type": feat.type,
            "prerequisites": feat.prerequisites,
        },
        "raw_block": raw_block,
        "soft": feat.soft,
    }
    rendered = json.dumps(packet, indent=2, ensure_ascii=False) + "\n"
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered, encoding="utf-8")
        print(f"wrote {out_path}")
    else:
        print(rendered, end="")
    return 0


def selftest() -> int:
    failures: List[str] = []

    fixture = [
        "# fixture",
        "",
        "## [PDF page 50]",
        "ALPHA BLADE [GENERAL] [EPIC]",
        "Prerequisite: Str 21.",
        "Benefit: Exact alpha text.",
        "",
        "## [PDF pages 51-52]",
        "BETA STANCE [WILD] [EPIC]",
        "Prerequisite: Wild shape.",
        "Benefit: Exact beta text.",
    ]
    try:
        fixture_spans = detect_description_spans(
            fixture, ["Alpha Blade", "Beta Stance"]
        )
        alpha = fixture_spans["Alpha Blade"]
        beta = fixture_spans["Beta Stance"]
        if (alpha.page, alpha.pages, alpha.start, alpha.end, alpha.type_label) != (
            50, "50", 3, 6, "GENERAL"
        ):
            failures.append(f"fixture Alpha Blade span drifted: {alpha}")
        if (beta.page, beta.pages, beta.start, beta.end, beta.type_label) != (
            51, "51-52", 8, 11, "WILD"
        ):
            failures.append(f"fixture Beta Stance span drifted: {beta}")
        if fixture[alpha.start] != "ALPHA BLADE [GENERAL] [EPIC]":
            failures.append("fixture Alpha Blade slice does not lead with its heading")
    except Exception as exc:
        failures.append(f"description-span fixture raised {exc!r}")

    if not SOURCE.is_file():
        failures.append(f"missing derived description extraction: {SOURCE}")
        print(
            f"NO COVERAGE: {BOOK} descriptions "
            f"(missing derived extraction: {SOURCE})"
        )
        feats = build([])
        lines: List[str] = []
        spans: Dict[str, DescriptionSpan] = {}
    else:
        lines = _source_lines()
        try:
            spans = detect_description_spans(lines, _records())
            feats = build(lines)
        except Exception as exc:
            failures.append(f"live description extraction raised {exc!r}")
            spans = {}
            feats = build([])

    names = {feat.name for feat in feats}
    expected_names = set(_records())
    if len(feats) != 154 or names != expected_names:
        failures.append(
            f"live feat set is {len(feats)}/{len(names)} unique; expected "
            "154/154 exact canonical names"
        )
    if len({feat.name.casefold() for feat in feats}) != len(feats):
        failures.append("duplicate epic-feat names")

    type_counts = Counter(feat.type for feat in feats)
    expected_types = {
        "general": 131,
        "wild": 11,
        "item-creation": 6,
        "metamagic": 3,
        "divine": 3,
    }
    if type_counts != expected_types:
        failures.append(f"type counts {dict(type_counts)}, wanted {expected_types}")

    expected_recovered = expected_names - NO_COVERAGE_NAMES
    if set(spans) != expected_recovered or len(spans) != 149:
        failures.append(
            f"description coverage is {len(spans)} names; expected exact "
            "149-name set with only the five p.60 gaps"
        )

    records = _records()
    bad_spans = []
    for feat in feats:
        if feat.name in NO_COVERAGE_NAMES:
            if not (
                feat.start == feat.end == 0
                and feat.soft
                and feat.soft.startswith("NO COVERAGE:")
            ):
                failures.append(f"{feat.name} must remain an empty NO COVERAGE span")
            continue
        if not (0 <= feat.start < feat.end <= len(lines)):
            bad_spans.append((feat.name, feat.start, feat.end, "bounds"))
            continue
        block = lines[feat.start:feat.end]
        heading = SOURCE_HEADING_RE.match(block[0].strip()) if block else None
        type_code = records[feat.name][0]
        if (
            feat.end - feat.start < 3
            or not heading
            or _name_key(heading.group(1)) != _name_key(feat.name)
            or heading.group(2) != TYPE_LABEL[type_code]
            or any(SOURCE_PAGE_RE.match(line.strip()) for line in block)
        ):
            bad_spans.append((feat.name, feat.start, feat.end, "shape"))
    if bad_spans:
        failures.append(f"invalid live full-description spans: {bad_spans[:5]}")

    by_name = {feat.name: feat for feat in feats}
    probes = {
        "Additional Magic Item Space": (50, "50"),
        "Dire Charge": (53, "53"),
        "Epic Spellcasting": (55, "55"),
        "Planar Turning": (64, "64-65"),
        "Zone of Animation": (69, "69"),
    }
    for name, expected in probes.items():
        feat = by_name.get(name)
        got = (feat.page, feat.description_pages) if feat else None
        if got != expected:
            failures.append(f"{name} description pages {got}, wanted {expected}")

    dire = by_name.get("Dire Charge")
    if not dire or (
        dire.prerequisites != "Improved Initiative"
        or dire.citation != DIRE_CITATION
        or dire.pages != "53"
    ):
        failures.append(f"Dire Charge exact mechanics/citation drifted: {dire}")

    devastating = by_name.get("Devastating Critical")
    if (
        not devastating
        or not devastating.prerequisites
        or "Overwhelming Critical" not in devastating.prerequisites
    ):
        failures.append(
            f"Devastating Critical prerequisites look wrong: "
            f"{devastating.prerequisites if devastating else None!r}"
        )

    if spans:
        perfect = by_name["Perfect Two-Weapon Fighting"]
        planar = by_name["Planar Turning"]
        zone = by_name["Zone of Animation"]
        perfect_raw = "\n".join(lines[perfect.start:perfect.end]).upper()
        planar_raw = "\n".join(lines[planar.start:planar.end]).upper()
        zone_raw = "\n".join(lines[zone.start:zone.end]).upper()
        if "PLANAR TURNING, AN ALTERNATIVE" in perfect_raw:
            failures.append("Planar Turning alternative leaked into Perfect Two-Weapon")
        if "PLANAR TURNING, AN ALTERNATIVE" not in planar_raw:
            failures.append("Planar Turning alternative sidebar is missing")
        if len(zone_raw) < 150 or "NONEPIC FEATS" in zone_raw:
            failures.append("Zone of Animation span is truncated or crossed chapter end")

    heading_count = sum(
        bool(SOURCE_HEADING_RE.match(line.strip())) for line in lines
    )
    if lines and heading_count != 149:
        failures.append(f"derived source has {heading_count} canonical headings, wanted 149")
    if "\ufffd" in json.dumps(
        [asdict(feat) for feat in feats], ensure_ascii=False
    ):
        failures.append("parsed epic-feat data contains U+FFFD")

    for failure in failures:
        print(f"SELFTEST FAIL: {failure}")
    print("selftest: " + ("PASS" if not failures else f"{len(failures)} failure(s)"))
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--search", metavar="TEXT")
    ap.add_argument("--export", metavar="NAME", help="emit a translator-ready packet")
    ap.add_argument("--out", type=Path, help="write the export packet here")
    ap.add_argument(
        "--extract-source",
        action="store_true",
        help="rebuild the derived two-column OCR description source from the PDF",
    )
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.extract_source:
        return extract_description_source()

    if args.selftest:
        return selftest()

    if args.export:
        return export_packet(args.export, args.out)

    if args.search:
        q = args.search.casefold()
        hits = [feat for feat in build() if q in feat.name.casefold()]
        for feat in hits:
            coverage = (
                f"description pp.{feat.description_pages}"
                if feat.start < feat.end
                else "NO COVERAGE"
            )
            print(
                f"  {feat.name} [{feat.type}] — "
                f"{feat.prerequisites or '—'}; {coverage}"
            )
        print(f"{len(hits)} match(es).")
        return 0 if hits else 1

    total, recovered = write_index()
    print(
        f"{total} D&D 3.5 epic feats; {recovered} full description spans; "
        f"{total - recovered} NO COVERAGE."
    )
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
