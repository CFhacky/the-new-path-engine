#!/usr/bin/env python3
"""epic_spell_harvest.py — the D&D 3.5 epic spells (Epic Level Handbook, Chapter 2).

WHY THIS ONE IS DIFFERENT (same reason as epic_feat_harvest.py). The Epic Level
Handbook's text layer is corrupted OCR (dropped leading characters, Cyrillic
bleed: "Spelleraft", "Momento Mori" garbles), so parsing it yields garbage
numbers and names. Instead, the ELH PDF's PAGE IMAGES are perfectly legible, so
the epic-spell chapter (Chapter 2, "Epic Spells") was transcribed BY VISION from
those rendered pages. This is still book RAW — read directly off the page, never
invented — and every entry is cited to the exact page.

Two bodies of mechanics are captured, exactly as printed:

  * the epic spell SEEDS (Table 2-1 "Epic Seeds", ELH p.88) — the base building
    blocks, each with its base Spellcraft DC. Every seed's base DC was
    cross-checked against the "To Develop / Seeds:" lines of the sample spells
    (e.g. destroy DC 29, conjure DC 21, summon DC 14, ward DC 14, animate dead
    DC 23) and all agree.

  * the ~46 SAMPLE EPIC SPELLS — each a full description (school + Spellcraft DC
    read off the entry header, ELH pp.74-88) paired with its one-line effect as
    printed in the "Epic Spells by Spellcraft DC" summary list (pp.73-74).

    reference/epic_spell_index.json — every seed + sample spell: name, kind,
                                      spellcraft_dc, school, effect, book, page,
                                      and exact full-description source span
    reference/epic_spell_index.md   — the same, for human eyes

FOUR BOOK-INTERNAL DC DISCREPANCIES. The quick "Epic Spells by Spellcraft DC"
list on pp.73-74 disagrees with four full-entry headers by 2. Each such entry
carries the full-entry DC (the actual spell description's stated value) as
spellcraft_dc and records the summary's differing number in `note`:
Origin of Species: Achaierai (entry 38 / list 40), Raise Island (entry 48 /
list 50), Epic Spell Reflection (entry 68 / list 70), Pestilence (entry 104 /
list 102).

PROVENANCE
    Epic Level Handbook (WotC, 3.5e), Chapter 2 "Epic Spells". Mechanics were
    read by vision from rendered PDF pages because the embedded text layer is
    unusable. Seed base DCs come from Table 2-1 (p.88); sample-spell schools +
    Spellcraft DCs from the full descriptions (pp.74-88); one-line effects from
    the "Epic Spells by Spellcraft DC" summary (pp.73-74). ``--extract-source``
    separately renders pp.74-102 at 4x and OCRs each visual column, preserving
    all body text raw while restoring only the 70 book-verified headings. Every
    row records an exact span into that reproducible description source.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO = Path(__file__).resolve().parent.parent
OUT_JSON = REPO / "reference" / "epic_spell_index.json"
OUT_MD = REPO / "reference" / "epic_spell_index.md"
CORPUS = Path(r"I:\Sourcebooks\_text")
SOURCE_REL = Path("D&D 3.5e") / "DM Toolkits" / \
    "Epic Level Handbook.epic-spells.ocr-columns.md"
SOURCE = CORPUS / SOURCE_REL
PDF_SOURCE = Path(r"I:\Sourcebooks\D&D 3.5e\DM Toolkits\Epic Level Handbook.pdf")
TESSERACT = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
BOOK = "Epic Level Handbook"
CITATION = (
    "Epic Level Handbook (WotC, 3.5e), Chapter 2 'Epic Spells' — Table 2-1 "
    "'Epic Seeds' (base Spellcraft DCs, p.88) and the sample epic spells (full "
    "descriptions with school + Spellcraft DC, pp.74-88; 'Epic Spells by "
    "Spellcraft DC' summary + one-line effects, pp.73-74). Vision-transcribed "
    "from the PDF page images because the OCR text layer is corrupt."
)
PAGES = "73-88"
SEED_PAGE = 88  # Table 2-1 "Epic Seeds"
SEED_NOTE = ("Spellcasters without at least 24 ranks in Knowledge (religion) "
             "may not use the heal or life spell seeds (Table 2-1 footnote).")

# ---------------------------------------------------------------------------
# SEEDS — ELH Table 2-1 "Epic Seeds" (p.88). (name, base Spellcraft DC).
# 24 seeds, transcribed exactly off the rendered table image. Cross-checked
# against the sample spells' "Seed(s):" development lines (all agree).
# ---------------------------------------------------------------------------
_SEEDS = [
    ("Afflict", 14),
    ("Animate", 25),
    ("Animate Dead", 23),
    ("Armor", 14),
    ("Banish", 27),
    ("Compel", 19),
    ("Conceal", 17),
    ("Conjure", 21),
    ("Contact", 23),
    ("Delude", 14),
    ("Destroy", 29),
    ("Dispel", 19),
    ("Energy", 19),
    ("Foresee", 17),
    ("Fortify", 17),
    ("Heal", 25),
    ("Life", 27),
    ("Reflect", 27),
    ("Reveal", 19),
    ("Slay", 25),
    ("Summon", 14),
    ("Transform", 21),
    ("Transport", 27),
    ("Ward", 14),
]

# ---------------------------------------------------------------------------
# SAMPLE EPIC SPELLS — ELH pp.74-88.
# (name, spellcraft_dc, school, effect, page, note)
#   spellcraft_dc / school : off the full-entry header (the authoritative value).
#   effect                 : the one-line summary as printed in the "Epic Spells
#                            by Spellcraft DC" list (pp.73-74).
#   page                   : PDF/print page of the full-entry header.
#   note                   : records a summary-vs-entry DC discrepancy, else None.
# ---------------------------------------------------------------------------
_D = None  # readability alias for "no note"
_SPELLS = [
    ("Peripety", 27, "Abjuration",
     "Ranged attacks against you are reflected back on your attacker", 84, _D),
    ("Ruin", 27, "Transmutation",
     "Object or target takes 20d6 damage", 85, _D),
    ("Dreamscape", 29, "Transmutation [Teleportation]",
     "You physically travel the region of dreams", 77, _D),
    ("Mummy Dust", 35, "Necromancy [Evil]",
     "Create two Large 18 HD mummies", 83, _D),
    ("Dragon Knight", 38, "Conjuration (Summoning) [Fire]",
     "An adult red dragon appears and attacks your enemies", 77, _D),
    ("Origin of Species: Achaierai", 38, "Conjuration (Creation, Healing)",
     "Create a true-breeding creature", 84,
     "The 'Epic Spells by Spellcraft DC' summary list (p.73) prints DC 40; the "
     "full entry (p.84) prints DC 38 (used here)."),
    ("Eclipse", 42, "Conjuration (Creation)",
     "A solar eclipse follows you", 78, _D),
    ("Let Go of Me", 43, "Transmutation",
     "Grappler takes 20d6 damage, you take 10d6", 81, _D),
    ("Greater Spell Resistance", 45, "Transmutation",
     "Subject gains SR 35 for 20 hours", 80, _D),
    ("Spell Worm", 45, "Enchantment (Compulsion) [Mind-Affecting]",
     "Subject abandons all her spells", 86, _D),
    ("Epic Mage Armor", 46, "Conjuration (Creation) [Force]",
     "Subject gains +20 AC bonus", 79, _D),
    ("Raise Island", 48, "Conjuration (Creation)",
     "You create a small island in the sea", 85,
     "The summary list (p.73) prints DC 50; the full-entry (p.85) header (faded) "
     "reads DC 48 (used here)."),
    ("Animus Blast", 50, "Evocation [Cold]",
     "Victims of your 10d6 coldball animate as skeletons and serve you", 74, _D),
    ("Dragon Strike", 50, "Conjuration (Summoning) [Fire]",
     "Ten adult red dragons appear and attack your enemies", 77, _D),
    ("Lord of Nightmares", 50, "Conjuration (Summoning)",
     "You are possessed by a dream larva for 20 rounds and take 12d6 damage", 82, _D),
    ("Rain of Fire", 50, "Evocation [Fire]",
     "You create a 2-mile-radius fire storm dealing 1 point of fire damage per round", 85, _D),
    ("Contingent Resurrection", 52, "Conjuration (Healing)",
     "Subject automatically resurrected if slain", 74, _D),
    ("Epic Repulsion", 52, "Abjuration",
     "One creature or object is warded against one type of creature", 79, _D),
    ("Mass Frog", 55, "Transmutation",
     "All in 40-ft.-radius are transformed into frogs", 82, _D),
    ("Soul Scry", 55, "Divination",
     "You experience everything the target experiences", 86, _D),
    ("Crown of Vermin", 56, "Conjuration (Summoning)",
     "You have an aura of one thousand venomous vermin", 75, _D),
    ("Verdigris", 58, "Transmutation",
     "100-ft-area overrun by tsunami of plant growth dealing 10d6 damage", 88, _D),
    ("Greater Ruin", 59, "Transmutation",
     "Object or target takes 35d6 damage", 80, _D),
    ("Superb Dispelling", 59, "Abjuration",
     "As greater dispelling, but +40 on check", 87, _D),
    ("Create Living Vault", 60, "Conjuration (Creation)",
     "You fashion a living vault attuned to you", 75, _D),
    ("Nailed to the Sky", 62, "Transmutation [Teleportation]",
     "Affix foe to the heavens", 83, _D),
    ("Safe Time", 64, "Transmutation [Teleportation]",
     "You contingently duck damage in a static time stream for 1 round", 85, _D),
    ("Epic Spell Reflection", 68, "Abjuration",
     "Creature or object permanently warded against spells", 80,
     "The summary list (p.73) prints DC 70; the full entry (p.80) prints DC 68 "
     "(used here)."),
    ("Epic Counterspell", 69, "Abjuration",
     "Cancel another's epic spell", 79, _D),
    ("Time Duplicate", 71, "Transmutation [Teleportation]",
     "You and your future self exist together for 1 round", 87, _D),
    ("Soul Dominion", 72, "Divination, Enchantment (Compulsion) [Mind-Affecting]",
     "You achieve remote control of the target", 86, _D),
    ("Summon Behemoth", 72, "Conjuration (Summoning)",
     "A behemoth appears and attacks your enemies", 86, _D),
    ("Animus Blizzard", 78, "Evocation [Cold]",
     "Victims of your 20d6 coldball animate as wights and serve you", 74, _D),
    ("Eidolon", 79, "Conjuration (Creation)",
     "Creates duplicate that shares your soul", 78, _D),
    ("Enslave", 80, "Enchantment (Compulsion) [Mind-Affecting]",
     "Subject is a permanent thrall", 79, _D),
    ("Demise Unseen", 82, "Necromancy [Death, Evil], Illusion [Figment]",
     "Animated ghoul of slain victim fools its companions that all is well", 76, _D),
    ("Momento Mori", 86, "Necromancy [Death]",
     "A thought that kills", 83, _D),
    ("Hellball", 90, "Evocation [Acid, Fire, Electricity, Sonic]",
     "You deal 10d6 each of acid, fire, electricity, and sonic damage, you take 10d6", 80, _D),
    ("Damnation", 97, "Enchantment (Compulsion) [Teleportation, Mind-Affecting]",
     "Send your foe to hell", 76, _D),
    ("Kinetic Control", 103, "Abjuration",
     "You store and redirect damage", 81, _D),
    ("Pestilence", 104, "Conjuration, Necromancy",
     "Inflict slimy doom on all creatures and plants in a half-mile-diameter area", 84,
     "The summary list (p.74) prints DC 102; the full entry (p.84) prints DC 104 "
     "(used here)."),
    ("Living Lightning", 140, "Evocation [Electricity]",
     "Spell can cast itself, dealing 10d6 electricity damage to foe", 82, _D),
    ("Eternal Freedom", 150, "Abjuration",
     "Permanent immunity to many hold, stun, stasis and other spells and effects", 80, _D),
    ("Verdigris Tsunami", 170, "Transmutation",
     "1,000-ft.-radius area overrun by permanent tsunami of plant growth dealing 40d6 damage", 88, _D),
    ("Dire Winter", 319, "Evocation [Cold]",
     "1,000-ft. radius emanation deals 2d6 cold damage for 20 hours", 76, _D),
    ("Vengeful Gaze of God", 419, "Transmutation",
     "Target takes 305d6 damage; you take 200d6", 87, _D),
]


# ---------------------------------------------------------------------------
# FULL-DESCRIPTION SOURCE — rendered PDF pages, raw two-column OCR.
# ---------------------------------------------------------------------------
SOURCE_PAGE_RE = re.compile(r"^## \[PDF pages? (\d+)(?:-(\d+))?\]$")
SOURCE_HEADING_RE = re.compile(r"^(.+?) \[EPIC SPELL DESCRIPTION\]$")

# Canonical heading -> (book page, visual column, y). Every anchor was verified
# against the rendered PDF. Odd-numbered pages use a wider right column because
# the book's mirrored gutter shifts the column boundary.
DESCRIPTION_ANCHORS: Dict[str, Tuple[int, int, float]] = {
    "Animus Blast": (74, 0, 836.0),
    "Animus Blizzard": (74, 1, 335.0),
    "Contingent Resurrection": (74, 1, 691.0),
    "Create Living Vault": (75, 0, 316.5),
    "Crown of Vermin": (75, 1, 66.0),
    "Damnation": (76, 0, 435.0),
    "Demise Unseen": (76, 1, 68.0),
    "Dire Winter": (76, 1, 553.0),
    "Dragon Knight": (77, 1, 61.0),
    "Dragon Strike": (77, 1, 477.0),
    "Dreamscape": (77, 1, 856.0),
    "Eclipse": (78, 0, 739.0),
    "Eidolon": (78, 1, 297.0),
    "Enslave": (79, 0, 299.0),
    "Epic Counterspell": (79, 0, 861.5),
    "Epic Mage Armor": (79, 1, 346.0),
    "Epic Repulsion": (79, 1, 656.0),
    "Epic Spell Reflection": (80, 0, 151.0),
    "Eternal Freedom": (80, 0, 493.0),
    "Greater Spell Resistance": (80, 1, 64.0),
    "Greater Ruin": (80, 1, 391.0),
    "Hellball": (80, 1, 672.0),
    "Kinetic Control": (81, 0, 608.0),
    "Let Go of Me": (81, 1, 598.0),
    "Living Lightning": (82, 0, 59.0),
    "Lord of Nightmares": (82, 0, 771.0),
    "Mass Frog": (82, 1, 611.0),
    "Momento Mori": (83, 0, 196.0),
    "Mummy Dust": (83, 0, 551.5),
    "Nailed to the Sky": (83, 1, 684.0),
    "Origin of Species: Achaierai": (84, 0, 357.5),
    "Peripety": (84, 0, 803.0),
    "Pestilence": (84, 1, 227.5),
    "Rain of Fire": (85, 0, 188.0),
    "Raise Island": (85, 0, 575.0),
    "Ruin": (85, 1, 210.5),
    "Safe Time": (85, 1, 535.5),
    "Soul Dominion": (86, 0, 196.5),
    "Soul Scry": (86, 0, 700.5),
    "Spell Worm": (86, 1, 347.0),
    "Summon Behemoth": (86, 1, 805.5),
    "Superb Dispelling": (87, 0, 300.0),
    "Time Duplicate": (87, 0, 583.0),
    "Vengeful Gaze of God": (87, 1, 511.0),
    "Verdigris": (88, 0, 66.0),
    "Verdigris Tsunami": (88, 0, 512.0),
    "Afflict": (92, 1, 73.0),
    "Animate": (92, 1, 610.0),
    "Animate Dead": (93, 0, 190.0),
    "Armor": (93, 1, 383.0),
    "Banish": (94, 0, 115.0),
    "Compel": (94, 0, 456.0),
    "Conceal": (94, 1, 146.0),
    "Conjure": (94, 1, 650.0),
    "Contact": (95, 0, 173.5),
    "Delude": (95, 0, 571.5),
    "Destroy": (95, 1, 465.0),
    "Dispel": (96, 0, 297.0),
    "Energy": (96, 1, 235.0),
    "Foresee": (97, 0, 228.0),
    "Fortify": (97, 1, 142.0),
    "Heal": (98, 0, 247.0),
    "Life": (98, 1, 118.0),
    "Reflect": (98, 1, 766.0),
    "Reveal": (99, 0, 599.0),
    "Slay": (99, 1, 587.0),
    "Summon": (100, 0, 306.0),
    "Transform": (100, 1, 165.0),
    "Transport": (101, 0, 327.0),
    "Ward": (101, 1, 443.0),
}

DESCRIPTION_ENDS: Dict[str, Tuple[int, int, float]] = {
    "Verdigris Tsunami": (88, 0, 930.0),
}

# The seed chapter uses several inset examples and art-driven continuations.
# These routes retain only the named seed's primary block and its own
# mechanically relevant "another use" box.
DESCRIPTION_FLOWS: Dict[str, Tuple[Tuple[int, int, float, float], ...]] = {
    "Contact": (
        (95, 0, 168.0, 566.0),
        (95, 1, 765.0, float("inf")),
    ),
    "Delude": (
        (95, 0, 566.0, 720.0),
        (95, 1, 55.0, 457.0),
    ),
    "Destroy": (
        (95, 1, 460.0, 755.0),
        (96, 0, 55.0, 289.0),
    ),
    "Energy": (
        (96, 1, 230.0, float("inf")),
        (97, 0, 55.0, 220.0),
        (97, 0, 720.0, float("inf")),
    ),
    "Foresee": (
        (97, 0, 223.0, 715.0),
        (97, 1, 55.0, 134.0),
    ),
    "Ward": (
        (101, 1, 438.0, 815.0),
        (102, 0, 520.0, float("inf")),
        (102, 1, 55.0, 270.0),
        (101, 0, 815.0, float("inf")),
        (101, 1, 815.0, float("inf")),
    ),
}


def _all_description_names() -> List[str]:
    names = [name for name, _ in _SEEDS]
    names.extend(row[0] for row in _SPELLS)
    return sorted(set(names))


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

    pages = tuple(range(74, 89)) + tuple(range(92, 103))
    lanes: List[dict] = []
    for book_page in pages:
        page = doc[book_page - 1]
        columns = ((8, 350), (350, 692)) if book_page % 2 == 0 \
            else ((8, 285), (285, 692))
        for column, (x0, x1) in enumerate(columns):
            clip = page.rect & fitz.Rect(x0, 55, x1, 945)
            pix = page.get_pixmap(matrix=fitz.Matrix(4, 4),
                                  clip=clip, alpha=False)
            image = Image.open(BytesIO(pix.tobytes("png"))).convert("L")
            image = ImageOps.autocontrast(image, cutoff=1)
            image = image.filter(
                ImageFilter.UnsharpMask(radius=1, percent=130, threshold=2)
            )
            data = pytesseract.image_to_data(
                image, config="--oem 3 --psm 6",
                output_type=pytesseract.Output.DICT,
            )
            groups: Dict[Tuple[int, int, int], List[int]] = defaultdict(list)
            for index, token in enumerate(data["text"]):
                if token.strip():
                    key = (data["block_num"][index], data["par_num"][index],
                           data["line_num"][index])
                    groups[key].append(index)
            lines: List[dict] = []
            for indexes in groups.values():
                indexes.sort(key=lambda index: data["left"][index])
                text = " ".join(data["text"][index]
                                for index in indexes).strip()
                lines.append({
                    "top": 55 + min(data["top"][index]
                                    for index in indexes) / 4,
                    "text": text,
                })
            lines.sort(key=lambda row: row["top"])
            lanes.append({"page": book_page, "column": column, "lines": lines})
        print(f"OCR source extraction: page {book_page}/102", flush=True)
    return lanes


def _meaningful_ocr(lines: Sequence[dict], low: float, high: float) -> List[str]:
    out: List[str] = []
    for row in lines:
        if low <= row["top"] < high:
            text = row["text"].strip()
            if sum(char.isalnum() for char in text) >= 2:
                out.append(text)
    return out


def _description_body(
    name: str,
    next_name: Optional[str],
    lane_map: Dict[Tuple[int, int], List[dict]],
    lane_keys: Sequence[Tuple[int, int]],
) -> Tuple[List[str], List[int]]:
    take = lambda page, column, low, high: _meaningful_ocr(
        lane_map[(page, column)], low, high
    )
    if name in DESCRIPTION_FLOWS:
        body: List[str] = []
        pages = set()
        for page, column, low, high in DESCRIPTION_FLOWS[name]:
            selected = take(page, column, low, high)
            if selected:
                body.extend(selected)
                pages.add(page)
        return body, sorted(pages)

    page, column, y = DESCRIPTION_ANCHORS[name]
    if name in DESCRIPTION_ENDS:
        end_page, end_column, end_y = DESCRIPTION_ENDS[name]
    elif next_name is not None:
        end_page, end_column, end_y = DESCRIPTION_ANCHORS[next_name]
    else:
        end_page, end_column, end_y = page, column, float("inf")

    lane_index = {key: index for index, key in enumerate(lane_keys)}
    start_lane = lane_index[(page, column)]
    end_lane = lane_index[(end_page, end_column)]
    if end_lane < start_lane:
        raise RuntimeError(f"description end precedes start for {name}")

    body: List[str] = []
    pages = set()
    for index in range(start_lane, end_lane + 1):
        lane_page, lane_column = lane_keys[index]
        low = y - 5 if index == start_lane else float("-inf")
        high = end_y - 8 if index == end_lane else float("inf")
        selected = _meaningful_ocr(lane_map[(lane_page, lane_column)], low, high)
        if selected:
            body.extend(selected)
            pages.add(lane_page)
    return body, sorted(pages)


def extract_description_source() -> int:
    if not PDF_SOURCE.is_file():
        print(f"NO COVERAGE: {BOOK} epic spell descriptions "
              f"(missing PDF: {PDF_SOURCE})")
        return 1
    try:
        import fitz
    except Exception as exc:
        print(f"NO COVERAGE: {BOOK} epic spell descriptions "
              f"(PyMuPDF unavailable: {exc})")
        return 1

    names = _all_description_names()
    missing = set(names) - set(DESCRIPTION_ANCHORS)
    extra = set(DESCRIPTION_ANCHORS) - set(names)
    if missing or extra:
        raise RuntimeError(f"description anchor mismatch: missing={sorted(missing)}, "
                           f"extra={sorted(extra)}")
    try:
        doc = fitz.open(PDF_SOURCE)
        lanes = _ocr_lanes(doc)
    except Exception as exc:
        print(f"NO COVERAGE: {BOOK} epic spell descriptions ({exc})")
        return 1

    lane_map = {(lane["page"], lane["column"]): lane["lines"]
                for lane in lanes}
    lane_keys = sorted(lane_map)
    ordered = sorted(names, key=lambda key: DESCRIPTION_ANCHORS[key])
    chunks = [
        "# EPIC SPELL DESCRIPTION EXTRACTION",
        "",
        "Derived from Epic Level Handbook PDF page images, pp. 74-102.",
        "Two-column OCR is preserved raw. Spell and seed headings alone are",
        "restored from the book-verified index transcription.",
        "",
    ]
    for index, name in enumerate(ordered):
        next_name = ordered[index + 1] if index + 1 < len(ordered) else None
        body, pages = _description_body(name, next_name, lane_map, lane_keys)
        if not body:
            raise RuntimeError(f"empty OCR description block for {name}")
        page_label = str(pages[0]) if len(pages) == 1 \
            else f"{pages[0]}-{pages[-1]}"
        chunks.extend([
            f"## [PDF pages {page_label}]",
            f"{name.upper()} [EPIC SPELL DESCRIPTION]",
            *body,
            "",
        ])

    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    SOURCE.write_text("\n".join(chunks).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {SOURCE}")
    print(f"{len(ordered)}/{len(ordered)} epic-spell description blocks recovered")
    return 0


def _name_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.casefold())


@dataclass(frozen=True)
class DescriptionSpan:
    page: int
    pages: str
    start: int
    end: int


def detect_description_spans(lines: Sequence[str]) -> Dict[str, DescriptionSpan]:
    canonical = {_name_key(name): name for name in _all_description_names()}
    headings: List[Tuple[str, int, int, str]] = []
    marker_index = -1
    marker_pages = ""
    for index, line in enumerate(lines):
        page_match = SOURCE_PAGE_RE.match(line.strip())
        if page_match:
            marker_index = index
            first = int(page_match.group(1))
            marker_pages = (str(first) if page_match.group(2) is None
                            else f"{first}-{int(page_match.group(2))}")
            continue
        heading_match = SOURCE_HEADING_RE.match(line.strip())
        if not heading_match:
            continue
        if marker_index < 0:
            raise ValueError(
                f"description heading before page marker at line {index + 1}"
            )
        key = _name_key(heading_match.group(1))
        if key not in canonical:
            raise ValueError(
                f"unknown epic-spell heading at line {index + 1}: {line!r}"
            )
        headings.append((canonical[key], marker_index, index, marker_pages))

    spans: Dict[str, DescriptionSpan] = {}
    for position, (name, _, start, pages) in enumerate(headings):
        end = headings[position + 1][1] if position + 1 < len(headings) \
            else len(lines)
        while end > start and not lines[end - 1].strip():
            end -= 1
        if name in spans:
            raise ValueError(f"duplicate epic-spell description heading: {name}")
        spans[name] = DescriptionSpan(
            page=int(pages.split("-", 1)[0]),
            pages=pages,
            start=start,
            end=end,
        )
    return spans


def _source_lines() -> List[str]:
    if not SOURCE.is_file():
        return []
    return SOURCE.read_text(encoding="utf-8").splitlines()


@dataclass
class EpicSpellEntry:
    name: str
    kind: str  # "seed" | "spell"
    book: str
    spellcraft_dc: int
    school: Optional[str]
    effect: Optional[str]
    citation: str
    page: int
    note: Optional[str] = None
    description_pages: str = ""
    start: int = 0
    end: int = 0
    soft: Optional[str] = None


def build(lines: Optional[Sequence[str]] = None) -> List[EpicSpellEntry]:
    source_lines = list(lines) if lines is not None else _source_lines()
    spans = detect_description_spans(source_lines) if source_lines else {}
    if lines is None and not source_lines:
        print(f"NO COVERAGE: {BOOK} epic spell descriptions "
              "(derived OCR source is missing)")

    def span_fields(name: str) -> Tuple[str, int, int, Optional[str]]:
        span = spans.get(name)
        if span:
            return span.pages, span.start, span.end, None
        return ("", 0, 0,
                "NO COVERAGE: full description "
                "(derived description extraction is missing)")

    out: List[EpicSpellEntry] = []
    seen = set()
    for name, dc in _SEEDS:
        key = ("seed", name.lower())
        if key in seen:
            continue
        seen.add(key)
        note = SEED_NOTE if name in ("Heal", "Life") else None
        pages, start, end, soft = span_fields(name)
        out.append(EpicSpellEntry(
            name=name, kind="seed", book=BOOK, spellcraft_dc=dc,
            school=None, effect=None, citation=CITATION, page=SEED_PAGE,
            note=note, description_pages=pages, start=start, end=end, soft=soft,
        ))
    for name, dc, school, effect, page, note in _SPELLS:
        key = ("spell", name.lower())
        if key in seen:
            continue
        seen.add(key)
        pages, start, end, soft = span_fields(name)
        out.append(EpicSpellEntry(
            name=name, kind="spell", book=BOOK, spellcraft_dc=dc,
            school=school, effect=effect, citation=CITATION, page=page,
            note=note, description_pages=pages, start=start, end=end, soft=soft,
        ))
    return out


def write_index() -> int:
    entries = build()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    from collections import Counter
    by_kind = Counter(e.kind for e in entries)
    seeds = [e for e in entries if e.kind == "seed"]
    spells = sorted((e for e in entries if e.kind == "spell"),
                    key=lambda e: (e.spellcraft_dc, e.name))

    md: List[str] = [
        "# EPIC SPELL INDEX — The New Path",
        "",
        "**Generated by `scripts/epic_spell_harvest.py`. Do not hand-edit; rerun",
        "the harvest.** D&D 3.5 epic spells from the Epic Level Handbook (Chapter",
        "2, 'Epic Spells'). **Vision-transcribed from the PDF page images** because",
        "the book's OCR text layer is corrupt — this is still book RAW, read",
        "directly off the page. Two kinds of entry: **seeds** (the base building",
        "blocks, Table 2-1, with a base Spellcraft DC) and **sample spells** (each",
        "with school, the development Spellcraft DC, and the one-line effect as",
        "printed in the 'Epic Spells by Spellcraft DC' summary). Where the summary",
        "list's DC disagrees with a full-entry header, the full-entry value is used",
        "and the summary's number is noted. All rows carry exact spans into a",
        "reproducible raw two-column OCR extraction of the printed descriptions;",
        "mechanical values remain the vision-verified transcription above.",
        "",
        f"*{len(entries)} entries — {by_kind.get('seed', 0)} seeds, "
        f"{by_kind.get('spell', 0)} sample spells.*",
        "",
        "## Epic seeds (Table 2-1, ELH p.88)",
        "",
        "| Seed | Base Spellcraft DC | Description Pages | Note |",
        "|---|---|---|---|",
    ]
    for e in sorted(seeds, key=lambda e: e.name):
        note = "heal/life: 24+ ranks Know(religion)" if e.note else ""
        md.append(f"| {e.name} | {e.spellcraft_dc} | {e.description_pages} | {note} |")
    md += [
        "",
        "## Sample epic spells (ELH pp.73-88)",
        "",
        "| Epic Spell | Spellcraft DC | School | Effect | Table/Entry Page | Description Pages |",
        "|---|---|---|---|---|---|",
    ]
    for e in spells:
        eff = e.effect or ""
        if e.note:
            eff = eff + " *(see note)*"
        md.append(f"| {e.name} | {e.spellcraft_dc} | {e.school or '—'} | {eff} | {e.page} | {e.description_pages} |")
    md.append("")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/epic_spell_harvest.py",
                    "corpus": str(CORPUS),
                    "source_path": str(SOURCE_REL),
                    "source_sha256": _source_hash(),
                    "book": BOOK, "citation": CITATION, "pages": PAGES,
                    "description_pages": "74-102",
                    "description_blocks": 70,
                    "full_description_entries": sum(
                        e.start < e.end for e in entries),
                    "note": ("Vision-transcribed mechanics plus exact line spans "
                             "into a reproducible two-column OCR extraction of "
                             "all printed epic spell and seed descriptions. The "
                             "PDF text layer is corrupt; values remain book RAW "
                             "and vision-verified. Seed base DCs are from Table "
                             "2-1 (p.88); sample spell mechanics are from the full "
                             "entries (pp.74-88) and summary (pp.73-74)."),
                    "total_entries": len(entries),
                    "by_kind": dict(by_kind),
                    "entries": [asdict(e) for e in entries]}, indent=1),
        encoding="utf-8")
    return len(entries)


def export_packet(query: str, out_path: Optional[Path]) -> int:
    q = query.casefold().strip()
    hits = [entry for entry in build() if q in entry.name.casefold()]
    if not hits:
        print(f"NO COVERAGE: epic spell export ({query!r} not found)")
        return 1
    lines = _source_lines()
    packet = {
        "generated_by": "scripts/epic_spell_harvest.py --export",
        "query": query,
        "source": str(SOURCE),
        "source_sha256": _source_hash(),
        "entries": [],
    }
    for entry in hits:
        row = asdict(entry)
        row["full_description"] = (
            "\n".join(lines[entry.start:entry.end]).strip()
            if entry.start < entry.end else ""
        )
        packet["entries"].append(row)
    text = json.dumps(packet, ensure_ascii=False, indent=2)
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {out_path}")
    else:
        print(text)
    return 0


def selftest() -> int:
    failures: List[str] = []
    entries = build()
    seeds = {e.name: e for e in entries if e.kind == "seed"}
    spells = {e.name: e for e in entries if e.kind == "spell"}

    # Exact core-count locks preserve the previously committed harvest.
    if len(seeds) != 24:
        failures.append(f"{len(seeds)} seeds; expected exactly 24")
    if len(spells) != 46:
        failures.append(f"{len(spells)} sample spells; expected exactly 46")
    if len(entries) != 70:
        failures.append(f"{len(entries)} total entries; expected exactly 70")

    # known seeds with exact base DCs (cross-checked against To Develop lines)
    for name, dc in (("Energy", 19), ("Destroy", 29), ("Summon", 14),
                     ("Ward", 14), ("Conjure", 21), ("Animate Dead", 23),
                     ("Life", 27)):
        s = seeds.get(name)
        if not s:
            failures.append(f"missing seed '{name}'")
        elif s.spellcraft_dc != dc:
            failures.append(f"seed '{name}' base DC {s.spellcraft_dc}, expected {dc}")

    # known sample spells with exact DCs
    for name, dc in (("Hellball", 90), ("Vengeful Gaze of God", 419),
                     ("Dire Winter", 319), ("Momento Mori", 86),
                     ("Epic Mage Armor", 46), ("Ruin", 27)):
        sp = spells.get(name)
        if not sp:
            failures.append(f"missing sample spell '{name}'")
        elif sp.spellcraft_dc != dc:
            failures.append(f"spell '{name}' DC {sp.spellcraft_dc}, expected {dc}")

    # the heal/life footnote landed
    if seeds.get("Heal") and not seeds["Heal"].note:
        failures.append("heal seed missing the Knowledge (religion) footnote")

    # discrepancy notes recorded on the four known mismatches
    for name in ("Origin of Species: Achaierai", "Raise Island",
                 "Epic Spell Reflection", "Pestilence"):
        if spells.get(name) and not spells[name].note:
            failures.append(f"'{name}' should carry a summary-vs-entry DC note")

    # every sample spell has a school + effect; every entry a positive DC
    for e in entries:
        if e.spellcraft_dc <= 0:
            failures.append(f"'{e.name}' has non-positive Spellcraft DC")
        if e.kind == "spell" and not e.school:
            failures.append(f"sample spell '{e.name}' missing school")
        if e.kind == "spell" and not e.effect:
            failures.append(f"sample spell '{e.name}' missing effect")

    # no duplicate (kind, name)
    keys = [(e.kind, e.name.lower()) for e in entries]
    if len(set(keys)) != len(keys):
        failures.append("duplicate (kind, name) entries")

    # Embedded span fixture: each block leads with its canonical heading and
    # ends immediately before the next page marker.
    fixture = [
        "## [PDF page 74]",
        "ANIMUS BLAST [EPIC SPELL DESCRIPTION]",
        "raw animus body",
        "",
        "## [PDF pages 74-75]",
        "CONTINGENT RESURRECTION [EPIC SPELL DESCRIPTION]",
        "raw resurrection body",
    ]
    fixture_spans = detect_description_spans(fixture)
    animus = fixture_spans.get("Animus Blast")
    contingent = fixture_spans.get("Contingent Resurrection")
    if not animus or (animus.pages, animus.start, animus.end) != ("74", 1, 3):
        failures.append(f"span fixture Animus Blast mismatch: {animus}")
    if not contingent or (contingent.pages, contingent.start,
                          contingent.end) != ("74-75", 5, 7):
        failures.append(
            f"span fixture Contingent Resurrection mismatch: {contingent}"
        )

    if set(_all_description_names()) != set(DESCRIPTION_ANCHORS):
        failures.append("description names and verified anchors differ")
    source_lines = _source_lines()
    recovered = [e for e in entries if e.start < e.end]
    if len(recovered) != 70:
        failures.append(f"full description spans: {len(recovered)}, expected 70")
    if len({(e.start, e.end) for e in recovered}) != 70:
        failures.append("description spans are not exactly 70 unique blocks")
    if source_lines and not _source_hash():
        failures.append("derived source exists but has no SHA-256")
    for e in entries:
        if e.soft is not None:
            failures.append(f"'{e.name}' unexpectedly soft: {e.soft}")
        if not e.description_pages:
            failures.append(f"'{e.name}' has no description_pages")
        if e.start < e.end:
            if e.end > len(source_lines):
                failures.append(f"'{e.name}' span ends past source length")
            elif _name_key(e.name) not in _name_key(source_lines[e.start]):
                failures.append(f"'{e.name}' span does not lead with its name")

    live_spans = detect_description_spans(source_lines) if source_lines else {}
    for name, excluded in (
        ("Delude", "ORIGIN OF SPECIES"),
        ("Destroy", "CONTACT ANOTHER USE"),
        ("Foresee", "ENERGY ANOTHER USE"),
        ("Ward", "EPIC PSIONIC POWERS"),
    ):
        span = live_spans.get(name)
        if span:
            segment = "\n".join(source_lines[span.start:span.end])
            if excluded.casefold() in segment.casefold():
                failures.append(f"'{name}' span swallowed {excluded}")

    for f in failures:
        print(f"SELFTEST FAIL: {f}")
    print("selftest: " + ("PASS" if not failures else f"{len(failures)} failure(s)"))
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--search", metavar="TEXT")
    ap.add_argument("--export", metavar="NAME", help="emit a translator-ready packet")
    ap.add_argument("--out", type=Path, help="write the export packet here")
    ap.add_argument("--extract-source", action="store_true",
                    help="rebuild the external two-column OCR description source")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.extract_source:
        return extract_description_source()
    if args.selftest:
        return selftest()
    if args.export:
        return export_packet(args.export, args.out)

    if args.search:
        q = args.search.lower()
        hits = [e for e in build()
                if q in e.name.lower()
                or (e.school and q in e.school.lower())
                or (e.effect and q in e.effect.lower())]
        for e in sorted(hits, key=lambda e: (e.kind, e.spellcraft_dc, e.name)):
            if e.kind == "seed":
                print(f"  [seed]  {e.name} — base Spellcraft DC {e.spellcraft_dc} (p.{e.page})")
            else:
                print(f"  [spell] {e.name} — DC {e.spellcraft_dc}, {e.school} "
                      f"— {e.effect} (p.{e.page})")
        print(f"{len(hits)} match(es).")
        return 0 if hits else 1

    n = write_index()
    print(f"{n} D&D 3.5 epic spell entries (Epic Level Handbook, Chapter 2, "
          f"vision-transcribed): 24 seeds + 46 sample spells.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
