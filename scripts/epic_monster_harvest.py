#!/usr/bin/env python3
"""epic_monster_harvest.py — the D&D 3.5 epic monsters (Epic Level Handbook, Ch. 6).

WHY THIS ONE IS DIFFERENT (same reason as epic_spell_harvest.py / epic_feat_
harvest.py). The Epic Level Handbook's text layer is corrupted OCR (dropped
leading characters, Cyrillic bleed, scrambled columns), so parsing it yields
garbage names and numbers. Instead, the ELH PDF's PAGE IMAGES are legible, so
the "Monsters" chapter (Chapter 6, PDF pp.157-230) was transcribed BY VISION
from those rendered pages (PyMuPDF render at ~2.8x, columns cropped higher where
needed, and read by eye). This is still book RAW — read directly off the page,
never invented — and every entry is cited to the exact PDF page of its stat
block.

SCOPE. The structured mechanics preserve the original KEY fields for every epic
monster: name, size_type (the Size + Type line), hit_dice, armor_class,
challenge_rating, alignment, one-line special_attacks and special_qualities,
and the Str/Dex/Con/Int/Wis/Cha abilities line. Each row now also carries the
true line span of its complete printed stat block and description in a
reproducible two-column OCR source. Shared variant sections share one book block.

    reference/epic_monster_index.json — mechanics + exact full-description spans
    reference/epic_monster_index.md   — the same, for human eyes

ROSTER = 64 monsters, the complete "Monsters by Challenge Rating" table (ELH
p.156), CR 5 (mercane) to CR 57 (hecatoncheires). Each monster's own stat-block
"Challenge Rating:" line is authoritative; the p.156 summary table was used only
as a roster cross-check (and to fill two obscured stat-block CR cells: the hoary
steed, CR 9).

FIDELITY NOTES (MECHANICS layer — book RAW; a number is transcribed exactly off
the image, and where a glyph is faded it is disambiguated only by the block's own
internal arithmetic, never guessed; anything unresolved is flagged in-line):
  * Abomination stat blocks list MAXIMUM hit points per Hit Die (a stated
    Abomination Trait) — e.g. Atropal 66d12 = 792 hp (= 66*12), Anaxim 38d10 =
    380 hp; non-abominations use average hp.
  * A handful of dice/AC/CR glyphs were faded or clipped by the page's red border
    art; each such value is either cross-checked against the block's own Con
    bonus / component sum (and stated so) or flagged '[clipped/illegible]' /
    '[faint]'. Notable: Xixecal's full dice expression is degraded (only its
    1,656 hp — the abomination maximum — is legible); Phaethon 62d8+806 and
    Thorciasid 29d8+348 HD counts were faded but pinned by their Con bonuses;
    the advanced red great wyrm's own block reads CR 39 while the p.156 summary
    appears to read 35 (its own block wins).
  * Several right-column blocks clip the Charisma value at the binding; those are
    marked '[clipped]' rather than invented.

PROVENANCE
    Epic Level Handbook (WotC, 3.5e), Chapter 6 "Monsters" (PDF pp.157-230).
    Vision-transcribed from the PDF page images because the OCR text layer is
    corrupt.
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
OUT_JSON = REPO / "reference" / "epic_monster_index.json"
OUT_MD = REPO / "reference" / "epic_monster_index.md"
CORPUS = Path(r"I:\Sourcebooks\_text")
SOURCE_REL = (Path("D&D 3.5e") / "DM Toolkits" /
              "Epic Level Handbook.epic-monsters.ocr-columns.md")
SOURCE = CORPUS / SOURCE_REL
PDF_SOURCE = Path(r"I:\Sourcebooks\D&D 3.5e\DM Toolkits\Epic Level Handbook.pdf")
TESSERACT = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
BOOK = "Epic Level Handbook"
PAGES = "157-230"
CITATION = (
    "Epic Level Handbook (WotC, 3.5e), Chapter 6 'Monsters' (PDF pp.157-230). "
    "Vision-transcribed from the PDF page images because the OCR text layer is "
    "corrupt; each monster is cited to the PDF page of its stat block. Key "
    "mechanical fields only (Size/Type, Hit Dice, AC, Challenge Rating, "
    "alignment, one-line special attacks/qualities, ability scores)."
)
NOTE = (
    "Vision-transcribed from the ELH PDF page images (the OCR text layer is "
    "corrupt). Book RAW, read off the page. Abomination blocks use MAXIMUM hit "
    "points per HD (a stated Abomination Trait). Faded/clipped glyphs are "
    "cross-checked against the block's own arithmetic or flagged in-line, never "
    "invented. Roster = the complete p.156 Monsters-by-CR table (64 monsters); "
    "each stat block's own Challenge Rating line is authoritative."
)

# ---------------------------------------------------------------------------
# THE MONSTERS — ELH Chapter 6, sorted by challenge rating then name.
# (name, size_type, hit_dice, armor_class, challenge_rating, alignment,
#  special_attacks, special_qualities, abilities, page)
# The challenge_rating string keeps any provenance note in-line; cr_int() peels
# off the leading integer for sorting / selftest.
# ---------------------------------------------------------------------------
_MONSTERS = [
    ('Mercane', 'Large Outsider (Lawful)', '7d8+21 (52 hp)', '15 (-1 size, +2 Dex, +4 natural)', '5', 'Always lawful neutral', 'Spell-like abilities', 'SR 25, spell-like abilities, telepathy', 'Str 15, Dex 15, Con 16, Int 20, Wis 17, Cha 11', 204),
    ('Hoary Steed', 'Large Magical Beast (Cold)', '12d10+36 (102 hp)', '23 (-1 size, +4 Dex, +10 natural)', '9 (stat-block CR cell obscured on p197; value from the p156 Monsters-by-CR table)', 'Always neutral evil', '--', 'Cold resistance 25, air walk, astral projection and etherealness, magic circle against good, misty breath, SR 20, DR 10/+3, immunities', 'Str 22, Dex 18, Con 17, Int 6, Wis 13, Cha 14', 197),
    ('Legendary Bear', 'Large Animal', '20d8+140 (230 hp)', '21 (-1 size, +2 Dex, +10 natural)', '9', 'Always neutral', 'Improved grab', 'Scent', 'Str 36, Dex 14, Con 24, Int 2, Wis 16, Cha 12', 202),
    ('Legendary Tiger', 'Large Animal', '26d8+182 (299 hp)', '23 (-1 size, +4 Dex, +10 natural)', '10', 'Always neutral', 'Pounce, improved grab, rake 2d6+5', 'Scent', 'Str 32, Dex 18, Con 24, Int 2, Wis 14, Cha 10', 202),
    ('Behemoth Eagle', 'Colossal Outsider', '21d8+126 (220 hp)', '24 (+12 Dex, -8 size, +10 natural)', '18', 'Always neutral', 'Rend 8d8+20', 'Evasion, SR 30, DR 20/+6', 'Str 25, Dex 34, Con 23, Int 17, Wis 19, Cha 16', 169),
    ('Behemoth Gorilla', 'Huge Outsider', '21d8+252 (346 hp)', '38 (+8 Dex, -2 size, +22 natural)', '19', 'Always neutral', 'Rend 8d8+20 (per combat text)', 'Scent, SR 30, DR 20/+6', 'Str 31, Dex 26, Con 35, Int 6, Wis 15, Cha 12', 169),
    ('Chichimec', 'Medium-Size Outsider (Air)', '27d8+189 (405 hp)', '39 (+7 Dex, +22 natural)', '21', 'Always neutral evil', 'Spell-like abilities, summon air elemental, Charisma drain', 'Abomination traits, fast healing, SR 33, DR 20/+6, electricity immunity', 'Str 34, Dex 25, Con 24, Int 12, Wis 14, Cha [clipped/illegible]', 160),
    ('Mithral Golem', 'Huge Construct', '36d10 (198 hp)', '42 (-2 size, +4 Dex, +26 natural, +4 haste)', '21', 'Always neutral', '--', 'Construct traits, magic immunity, DR 50/+5, alacrity', 'Str 39, Dex 19, Con --, Int --, Wis 11, Cha 1', 194),
    ('Mu Spore', 'Colossal Plant', '35d8+315 (472 hp)', '27 (-3 Dex, -8 size, +28 natural)', '21', 'Usually chaotic neutral', 'Spore cough, improved grab, swallow whole', 'Acid resistance 20, blindsight 210 ft., DR 25/+5, fast healing 10, plant traits, sticky', 'Str 36, Dex 5, Con 29, Int 18, Wis 28, Cha 28', 205),
    ('Pseudonatural Troll', 'Large Outsider', '6d8+66 (114 hp)', '51 (-1 size, +7 Dex, +35 natural)', '21', 'Always chaotic evil', 'Constant insight, improved grab, rend 4d8+25, rotting constriction', 'DR 25/+6, SR 30, acid and electricity resistance 20, regeneration 5, scent, spell-like abilities, darkvision 90 ft.', 'Str 45, Dex 24, Con 33, Int 6, Wis 10, Cha 6', 211),
    ('White Slaad', 'Large Outsider (Chaotic)', '24d8+312 plus 20 (440 hp)', '40 (+8 Dex, -1 size, +23 natural)', '21', 'Always chaotic neutral', 'Chaos spittle, spell-like abilities, summon slaad, stun, weapon breaker', 'Fast healing 15, DR 35/+5, resistances, alternate form', 'Str 36, Dex 26, Con 37, Int 26, Wis 27, Cha 27', 218),
    ('Anaxim', 'Medium-Size Construct, Outsider (Lawful)', '38d10 (380 hp)', '37 (+7 Dex, +20 natural), touch 17, flat-footed 30', '22', 'Always lawful neutral', 'Rend 4d6+18, sonic blast, spell-like abilities, summon iron golem', 'Abomination traits, construct traits, fast healing 15, SR 34, DR 30/+6', 'Str 35, Dex 25, Con --, Int 20, Wis 20, Cha [clipped/illegible]', 158),
    ('Ha-naga', 'Colossal Aberration', '20d8+220 (310 hp)', '40 (-8 size, +14 Dex, +24 natural)', '22', 'Usually chaotic evil', 'Charming gaze, poison, improved grab, constrict 4d6+12; casts as a 21st-level sorcerer (+ cleric/Chaos/Evil domain spells)', 'Flight, SR 30, DR 15/+7 (DR value partly clipped)', 'Str 27, Dex ~38 (+14 per Init/AC), Con ~32 (+11 per HD), Int ~35, Wis ~23, Cha ~36 [left-column ability line margin-clipped; Dex/Con cross-checked]', 195),
    ('Thorciasid', 'Medium-Size Aberration', '29d8+348 (478 hp) [HD-count digit faint; cross-checked: 29*4.5+348=478 and Con 34 gives 29*12=348]', '42 (+14 Dex, +18 natural)', '22', 'Usually neutral', 'Ability drain, energy drain', 'DR 20/+6, darkvision 240 ft., SR 34, fire resistance 30', 'Str 22, Dex 38, Con 34, Int 25, Wis 29, Cha [clipped]', 220),
    ('Brachyurus', 'Large Magical Beast', '38d10+684 (893 hp)', '40 (+14 Dex, -1 size, +17 natural)', '23', 'Usually lawful neutral', 'Frightful howl, savage 15d6+25', 'Blindsight 240 ft., DR 15/+5, fast healing 10, low-light vision, SR 32, scent, acid/cold/electricity/fire/sonic resistance 20', 'Str 30, Dex 38, Con 47, Int 18, Wis 32, Cha 19', 170),
    ('Lavawight', 'Medium-Size Undead (Fire)', '32d12 (208 hp)', '46 (+8 Dex, +28 natural)', '23', 'Chaotic evil', 'Rend 6d8+31, blazefire, spell-like abilities', 'Undead traits, fire subtype, heat aura, SR 34, DR 20/+6, fiery hardness', 'Str 42, Dex 27, Con --, Int 10, Wis 22, Cha 28', 200),
    ('Paragon Mind Flayer', 'Medium-Size Aberration', '8d8+64 plus 96 (224 hp) [paragon template: maximum hp plus +12/HD]', '50 (+9 Dex, +7 natural, +12 insight, +12 luck)', '23', 'Usually lawful evil', 'Mind blast, psionics, improved grab, extract', 'SR 35, telepathy, fire and cold resistance 10, DR 20/+6, fast healing 23', 'Str 27, Dex 29, Con 27, Int 34, Wis 32, Cha [clipped]', 208),
    ('Ruin Swarm', 'Colossal Ooze', '50d10+500 plus 40 (815 hp)', '18 (-8 size, +16 Dex)', '23', 'Neutral', 'Engulf', 'Swarm, ooze traits, blindsight 200 ft., fast healing 15', 'Str 42, Dex 42, Con 30, Int --, Wis 23, Cha 32', 213),
    ('Winterwight', 'Medium-Size Undead (Cold)', '42d12 (273 hp)', '46 (+8 Dex, +28 natural)', '23', 'Always chaotic evil', 'Rend 6d8+31, blightfire, spell-like abilities', 'Undead traits, cold subtype, cold aura, SR 34, DR 20/+6, icy hardness', 'Str 42, Con --, Cha 28; Dex/Int/Wis clipped at the left binding margin (approx Dex 26, Int 20, Wis 20 -- uncertain)', 227),
    ('Sirrush', 'Large Magical Beast', '40d10+680 (900 hp)', '44 (+15 Dex, -1 size, +20 natural)', '24', 'Usually chaotic neutral', 'Pounce, stunning roar', 'Blindsight 300 ft., DR 30/+5, darkvision 60 ft., fast healing 20, low-light vision, SR 39, scent, acid/cold/electricity/fire/sonic resistance 10', 'Str 42, Dex 40, Con 44, Int 15, Wis 18, Cha 28', 216),
    ('Stone Colossus', 'Colossal Construct', '64d10 (352 hp)', '44 (-8 size, -3 Dex, +45 natural)', '24', 'Usually neutral', 'Shatter', 'Construct traits, magic immunity, antimagic field, DR 30/+6', 'Str 70, Dex 5, Con --, Int 7, Wis 10, Cha 5', 171),
    ('Tayellah', 'Gargantuan Magical Beast', '34d10+408 (595 hp)', '44 (+19 Dex, -4 size, +15 insight, +4 natural)', '24', 'Always neutral', 'Pounce, improved grab, rake 4d6+15', 'SR 34, DR 15/+6', 'Str 32, Dex 48, Con 34, Int 14, Wis 32, Cha 19', 220),
    ('Vermiurge', 'Large Aberration', '42d8+546 (735 hp)', '40 (-1 size, +7 Dex, +24 natural) [printed total 40; the Dex component prints as +3 but Dex 25/Init +7 imply +7]', '24', 'Usually lawful neutral', 'Aura of doom, concealing aura, frightful presence, poison, spell-like abilities', 'DR 30/+5, darkvision 60 ft., fast healing 10, immune to all mind-affecting effects, low-light vision, SR 34, scent', 'Str 34, Dex 25, Con 36, Int 18, Wis 40, Cha 44', 226),
    ('Adamantine Golem', 'Huge Construct', '54d10 (297 hp)', '37 (-2 size, -1 Dex, +30 natural)', '25', 'Always neutral', 'Trample', 'Construct traits, magic immunity, DR 50/+7', 'Str 51, Dex 9, Con --, Int --, Wis 11, Cha 1', 194),
    ('Black Slaad', 'Huge Outsider (Chaotic)', '29d8+406 (536 hp)', '48 (+6 Dex, -2 size, +34 natural)', '25', 'Usually chaotic neutral (sometimes chaotic evil)', 'Chaos spittle, chaos touch, spell-like abilities, summon slaad, stun, weapon breaker', 'Fast healing 30, DR 45/+7, resistances, alternate form, darkvision 320 ft.', 'Str 42, Dex 22, Con 38, Int 29, Wis 30, Cha [clipped]', 218),
    ('Elder Treant', 'Colossal Plant', '50d8+800 (1,025 hp) [HD-count digit faint; cross-checked: 50*4.5+800=1025 and Con 42 gives 50*16=800]', '41 (-1 Dex, -8 size, +40 natural)', '25', 'Always neutral good', 'Animate trees, trample, triple damage against objects, spell-like abilities', 'Plant traits, half damage, SR 29, DR 5/-- (DR requirement clipped)', 'Str 40, Dex 8, Con 42, Int 19, Wis 33, Cha 35', 223),
    ('Gloom', 'Medium-Size Monstrous Humanoid', '25d8+225 (337 hp)', '40 (+18 Dex, +12 insight)', '25', 'Usually lawful evil', 'Fear gaze, sneak attack +13d6', 'Blindsight 60 ft., opportunist, evasion, spell-like abilities, SR 35, DR 25/+6', 'Str 32, Dex 46, Con 29, Int 26, Wis 25, Cha [clipped]', 192),
    ('Hoary Hunter', 'Medium-Size Fey (Cold)', '46d6+598 (759 hp)', '46 (+11 Dex, +15 insight, +10 natural)', '25', 'Always neutral evil', 'Spell-like abilities (rides with a +6 keen longsword of binding)', 'Cold resistance 50, SR 36, DR 20/+6', 'Str 38, Dex 33, Con 36, Int 31, Wis 23, Cha 26', 197),
    ('Hunefer', 'Medium-Size Undead', '50d12+3 (603 hp) [603 = maximum for 50d12 (600) plus a +3 bonus]', '52 (+12 Dex, +20 natural, +10 insight)', '25', 'Always lawful evil', 'Despair (Will DC 48), hunefer rot, spell-like abilities', 'Blindsight 300 ft., resistant to blows, DR 20/+5, fast healing 30, SR 37, undead traits, fire vulnerability', 'Str 47, Dex 35, Con --, Int 18, Wis 38, Cha 36', 198),
    ('Phane', 'Large Outsider (Chaotic) (Incorporeal)', '36d8+324 (612 hp)', '50 (-1 size, +3 Dex, +11 deflection, +23 insight) [printed total 50; listed components sum to 46 -- book internal inconsistency]', '25', 'Always chaotic evil', 'Spell-like abilities, stasis touch, chronal blast, time leach, summon past time duplicate', 'Abomination traits, null time field, time regression, fast healing 15, regeneration 15, SR 37, DR 30/+6, sonic immunity', 'Str --, Dex 25, Con 29, Int 24, Wis 16, Cha [clipped/illegible]', 166),
    ('Infernal', 'Large Outsider (Evil) (Chaotic or Lawful)', '40d8+360 (680 hp)', '50 (+7 Dex, -1 size, +34 natural)', '26', 'Lawful evil or chaotic evil', 'Improved grab, spell suck, learned spell immunity, spell-like abilities, summon fiend', 'Abomination traits, fast healing 5, regeneration 15, SR 38, DR 35/+7', 'Str 43, Dex 25, Con 28, Int 22, Wis 26, Cha 29', 164),
    ('Neh-thalggu (Brain Collector)', 'Huge Aberration (Incorporeal)', '32d8+192 (336 hp)', '35 (-2 size, +4 Dex, +3 deflection, +20 insight)', '26', 'Usually chaotic neutral, neutral evil, or chaotic evil', 'Extract brains (ranged attack), poison, spells', 'Dimensional travel, DR 25/+[unclear], incorporeal traits, amorphous physiology, manifest maw, SR 30, darkvision 60 ft.', 'Str --, Dex 19, Con 22, Int 20, Wis 20, Cha [clipped]', 206),
    ('Shadow of the Void', 'Large Undead (Incorporeal, Cold)', '35d12 (227 hp)', '48 (-1 size, +9 Dex, +10 deflection, +20 insight)', '26', 'Always lawful evil', 'Blightfire, create spawn, spell-like abilities', 'Undead traits, incorporeal traits, turn resistance +6, cold subtype, cold aura, SR 36, DR 20/+6', 'Str --, Dex 29, Con --, Int 21, Wis 25, Cha 33', 214),
    ('Shape of Fire', 'Large Undead (Fire, Incorporeal)', '35d12 (227 hp)', '48 (-1 size, +9 Dex, +10 deflection, +20 insight)', '26', 'Always lawful evil', 'Blazefire, create spawn, spell-like abilities', 'Undead traits, incorporeal traits, turn resistance +6, fire subtype, heat aura, SR 36, DR 20/+6', 'Str --, Dex 29, Con --, Int 21, Wis 25, Cha 31', 215),
    ('Worm That Walks', 'Medium-Size Ooze', '23d10+46+10 (hp faded; reads ~297, but that exceeds the 286 max for 23d10+56 -- likely 197 or a book misprint). Sample is a 23rd-level wizard converted by the worm-that-walks template', '47 (+4 Dex, +8 bracers, +3 ring, +2 amulet, +20 insight)', '26', 'Any evil', 'Spell-like abilities, engulf, frightful presence; casts as a 23rd-level wizard', 'Blindsight 300 ft., SR 36, discorporate, ooze traits', 'Str 10, Dex 14 (18 with gloves), Con 13 (15 with ioun stone), Int 20 (26 with headband), Wis 12, Cha 8', 228),
    ('Flesh Colossus', 'Colossal Construct', '100d10 (550 hp)', '45 (-8 size, -2 Dex, +25 natural, +20 profane)', '27', 'Neutral evil or neutral', 'Frightful presence, horrific appearance, stomp, stench', 'Construct traits, magic immunity, DR 20/+7, negative energy affinity', 'Str 35, Dex 6, Con --, Int 1 (or as controlling spirit), Wis 11 (or as controlling spirit), Cha 3 (or as controlling spirit)', 171),
    ('Gibbering Orb', 'Huge Aberration', '27d8+216 (340 hp)', '48 (+12 Dex, -2 size, +16 natural, +12 insight)', '27', 'Usually chaotic evil', 'Gibbering, improved grab, swallow whole, eye rays, spell-like abilities', 'All-around vision, flight, amorphous, SR 37, DR 25/+6', 'Str 32, Dex 35, Con 27, Int 40, Wis 24, Cha 22', 191),
    ('Uvuudaum', 'Large Outsider (Evil)', '38d8+646 (817 hp) [HD line washed out by art on p224; HD count read as 38, bonus/hp reconstructed from confirmed Con 44 (+17): 38*17=646, 38*4.5+646=817]', '52 (+14 Dex, -1 size, +29 natural)', '27', 'Usually neutral evil', 'Confusion aura (Will DC 47), spell-like abilities, Wisdom drain 2d4 (Fort DC 47); head spike +51 melee (4d6+21 plus Wisdom drain)', 'Blindsight 500 ft., DR 25/+6, electricity resistance 30, fast healing 20, regeneration', 'Str 39, Dex 38, Con 44, Int 42, Wis 38, Cha 46', 224),
    ('LeShay', 'Medium-Size Fey', '50d6+650 (828 hp)', '52 (+17 Dex, +20 insight, +5 natural)', '28', 'Any', 'Gaze, spell-like abilities, leShay weapons (2 +10 keen brilliant energy bastard swords)', 'Superior two-weapon fighting, DR 30/+7, elf traits, immune to poison and disease, low-light vision, SR 42, fast healing 10', 'Str 21, Dex 45, Con 37, Int 33, Wis 23, Cha 47', 202),
    ('Prismasaurus', 'Huge Magical Beast', '60d10+540 (870 hp)', '55 (-2 size, +7 Dex, +40 natural)', '28', 'Always neutral', 'Prismatic emanations', 'Immunities, prismatic blur, SR 38, DR 20/+6', 'Str 32, Dex 25, Con 29, Int 4, Wis 19, Cha 10', 210),
    ('Three-Headed Sirrush', 'Large Magical Beast', '45d10+855 (1,102 hp)', '50 (+17 Dex, -1 size, +24 natural)', '28', 'Usually chaotic neutral', 'Pounce, stunning roar', 'Blindsight 350 ft., DR 35/+6, darkvision 60 ft., fast healing 25, low-light vision, SR 42, scent, acid/cold/electricity/fire/sonic resistance 15', 'Str 47, Dex 45, Con 48; Int/Wis/Cha in the top-right margin were clipped (approx Int 20, Wis 23, Cha 13 -- uncertain)', 216),
    ('Demilich', 'Diminutive Undead', '21d12 (130 hp)', '51 (+4 size, +3 Dex, +5 natural, +8 bracers of armor, +2 ring of protection, +21 insight) [sample demilich, includes gear]', '29', 'Neutral evil', 'Trap the soul, fear aura, paralyzing touch, 21st-level wizard spellcaster, Perfect Automatic Still Spell, spell-like abilities', 'Magic immunity, phylactery transference, turn resistance +20, DR 30/--, undead traits, acid/fire/sonic resistance 20, immune to cold/electricity/polymorph/mind-affecting', 'Str 10, Dex 16 (with gloves), Con --, Int 39 (with headband), Wis 24, Cha 20', 174),
    ('Hagunemnon (Protean)', 'Large Shapechanger', '44d8+616 (814 hp)', '50 (-1 size, +13 Dex, +28 natural)', '29', 'Chaotic neutral', 'Psionics, destabilize form', 'Alter shape, DR 25/+6, darkvision 120 ft., immunities, regeneration 50, SR 34', 'Str 53, Dex 37, Con 39, Int 20, Wis 23, Cha 34', 196),
    ('Atropal', 'Large Undead, Outsider (Evil)', '66d12 (792 hp)', '51 (-1 size, +2 Dex, +40 natural)', '30', 'Always lawful evil', 'Constitution drain, energy drain 2d4 negative levels (Fort DC 59), spell-like abilities, summon nightcrawler', 'Abomination traits, undead traits, rebuke/command undead, regeneration 20, SR 42, DR 40/+6, negative energy aura', 'Str 43, Dex 15, Con --, Int 26, Wis 22, Cha 42', 159),
    ('Elder Titan', 'Colossal Outsider', '70d8+700 (1,015 hp)', '58 (-8 size, +32 natural, +24 insight)', '30', 'Always neutral', 'Spell-like abilities, spells (casts as a 29th-level wizard/cleric); Colossal +5 warhammer +87 melee', 'DR 45/+7, SR 40', 'Str 45, Dex 10, Con 31, Int 33, Wis 37, Cha 26', 221),
    ('Genius Loci', 'Colossal Ooze', '70d10+1,400 plus 40 (1,825 hp)', '0 (-2 Dex, -8 size)', '30', 'Usually any evil', 'Enslave, improved grab, constrict 4d10+30', 'Blindsight 200 ft., fast healing 50, ooze traits', 'Str 50, Dex 6, Con 50, Int --, Wis 24, Cha 26', 190),
    ('Dream Larva', 'Large Outsider (Chaotic)', '40d8+360 (680 hp)', '52 (-1 size, +3 Dex, +40 natural)', '31', 'Always chaotic evil', 'Worst nightmare, improved grab, sending, spell-like abilities, summon nightwalker', 'Abomination traits, sonic immunity, regeneration 15, fast healing 15, SR 44, DR 40/+8', 'Str 42, Dex 17, Con 29, Int 16, Wis 34, Cha [clipped, ~30]', 161),
    ('Force Dragon (adult)', 'Gargantuan Dragon (Force)', '45d12+585 (877 hp)', '64 (-4 size, +14 deflection, +44 natural)', '31', 'Usually neutral', 'Crush 4d6+30 (DC 45), tail sweep 2d6+30 (DC 45), breath weapon (cone of force 60 ft., 30d12, Ref DC 45), frightful presence (DC 46), spells (CL 18th), spell-like abilities', 'Immunities, DR 30/+6, SR 39, blindsight, keen senses, deflecting force, blur (20% miss chance), immune to force effects', 'Str 51, Dex 10, Con 37, Int 38, Wis 39, Cha 38', 183),
    ('Umbral Blot (Blackball)', 'Medium-Size Construct', '57d10 (313 hp)', '40 (+10 Dex, +20 natural)', '32', 'Always neutral', 'Disintegrating touch (Fort DC 38), vortex', 'Blindsight 200 ft., construct traits, fast healing 10, planar travel, SR 44, acid/cold/electricity/fire/sonic resistance 30', 'Str 10, Dex 30, Con --, Int 20, Wis 30, Cha 30', 223),
    ('Iron Colossus', 'Colossal Construct', '96d10 (528 hp)', '60 (-8 size, -2 Dex, +60 natural)', '33', 'Usually neutral', 'Breath weapon', 'Construct traits, magic immunity, antimagic field, rustproof, DR 30/+7', 'Str 60, Dex 7, Con --, Int 9, Wis 12, Cha 7', 171),
    ('Living Vault', 'Colossal Construct', '96d10 (528 hp)', '60 (-8 size, -2 Dex, +60 natural)', '33', 'Neutral', 'Imprisonment', 'Recognition, safekeeping, construct traits, magic immunity, DR 30/+7', 'Str 80, Dex 7, Con --, Int 9, Wis 12, Cha 7', 203),
    ('Phaethon', 'Gargantuan Outsider (Fire)', '62d8+806 (HD-count digit faint; confirmed via Con 36 = +13/HD x 62 = 806)', '47 (-4 size, +7 Dex, +34 natural)', '34', 'Always chaotic evil', 'Fiery touch, fiery overrun, spell-like abilities, improved grab, swallow whole, summon elder fire elemental', 'Abomination traits, fire immunity, oozelike immunities, regeneration 25, fast healing 25, DR 40/+8', 'Str 58, Dex 25, Con 36, Int 8, Wis 18, Cha 39', 165),
    ('Primal Air Elemental', 'Colossal Elemental (Air)', '96d8+864 (1,296 hp)', '66 (-8 size, +16 Dex, +48 natural)', '35', 'Usually neutral', 'Air mastery, whirlwind', 'Elemental traits, DR 35/+8, SR 42, air subtype', 'Str 32, Dex 43, Con 28, Int 8, Wis 13, Cha 13', 187),
    ('Primal Earth Elemental', 'Colossal Elemental (Earth)', '96d8+960 (1,392 hp)', '49 (-8 size, -1 Dex, +48 natural)', '35', 'Usually neutral', 'Earth mastery, push', 'Elemental traits, DR 35/+8 (plus 9/--), SR 42, earth subtype', 'Str 43, Dex 8, Con 31, Int 8, Wis 13, Cha 13', 187),
    ('Primal Fire Elemental', 'Colossal Elemental (Fire)', '96d8+864 (1,296 hp)', '64 (-8 size, +14 Dex, +48 natural)', '35', 'Usually neutral', 'Burn', 'Elemental traits, DR 35/+8, SR 42, fire subtype', 'Str 32, Dex 39, Con 28, Int 8, Wis 13, Cha 13', 187),
    ('Primal Water Elemental', 'Colossal Elemental (Water)', '96d8+960 (1,392 hp)', '64 (-8 size, +14 Dex, +48 natural)', '35', 'Usually neutral', 'Water mastery, drench, vortex', 'Elemental traits, DR 35/+8 (plus 9/--), SR 42, water subtype', 'Str 42, Dex 38, Con 31, Int 8, Wis 13, Cha 13', 187),
    ('Xixecal', 'Colossal Outsider (Cold)', '1,656 hp (LEGIBLE, = maximum hp per abomination trait). Full XdY+Z dice expression DEGRADED/illegible on the page image; best reconstruction 72d8+1,080 (Colossal Outsider d8, Con ~40 = +15: 72*(8+15)=1,656); alt 69d8+1,104 (Con 42) also fits 1,656', '64 (-8 size, +7 Dex, +55 natural)', '36', 'Always chaotic evil', 'Rend 4d8+42, cold, spell-like abilities, breath weapon, summon white dragon, Constitution drain', 'Abomination traits, cold subtype, dire winter, fast healing 30, regeneration 30, SR 48, DR 45/+9', 'Str 66, Dex 13, Con ~40 (tens digit 4 clear; units faint), Int 12, Wis 6, Cha 34', 167),
    ('Advanced Red Great Wyrm (sample advanced dragon)', 'Colossal+ Dragon (Fire)', '61d12+1,037 (1,433 hp)', '70 (-8 size, +3 Dex, +60 natural, +5 bracers)', '39 (per its own stat block, p180; the p156 summary CR table appears to list 35 -- flagged, likely a 39/35 OCR ambiguity)', 'Chaotic evil (base red dragon; the abbreviated sample block omits the alignment line)', 'Crush 8d6+36 (DC 57), tail sweep 4d6+36 (DC 57), breath weapon (cone of fire 80 ft., 38d10, Ref DC 57), frightful presence (DC 51), spells (CL 33rd), spell-like abilities', 'Immunities (sleep, paralysis), DR 35/+6, SR 46, blindsight, keen senses (darkvision 7,600 ft.), fire subtype', 'Str 59, Dex 16 (with gloves), Con 45, Int 32, Wis 33, Cha 32', 180),
    ('Devastation Centipede', 'Colossal Vermin', '128d8+1,152 (1,728 hp)', '55 (-8 size, +13 Dex, +40 natural)', '39', 'Always neutral', 'Poison (Fort DC 93, 2d12 Dex)', 'Darkvision 300 ft., SR 50, DR 40/+9', 'Str 33, Dex 37, Con 29, Int --, Wis 10, Cha 2', 178),
    ('Devastation Spider', 'Colossal Vermin', '128d8+1,280 (1,856 hp)', '58 (-8 size, +14 Dex, +42 natural)', '41', 'Always neutral', 'Poison (Fort DC 94, 2d12 Con), web', 'Darkvision 300 ft., SR 50, DR 35/+8', 'Str 37, Dex 39, Con 30, Int --, Wis 10, Cha 2', 178),
    ('Devastation Scorpion', 'Colossal Vermin', '128d8+1,408 (1,984 hp)', '60 (-8 size, +12 Dex, +46 natural)', '42', 'Always neutral', 'Improved grab, squeeze, poison (Fort DC 95, 2d12 Str)', 'Darkvision 300 ft., SR 50, DR 45/+8', 'Str 38, Dex 35, Con 32, Int --, Wis 10, Cha 2', 178),
    ('Prismatic Dragon (old)', 'Colossal Dragon (Light)', '58d12+1,102 (1,479 hp)', '78 (-8 size, +19 deflection, +57 natural)', '48', 'Usually neutral', 'Breath weapon (prismatic spray effect), spell-like abilities (at this age incl. sunburst; CL 26th)', 'Deflecting force, immune to light and blindness, damage reduction (scales by age)', 'Str 57, Dex 10, Con 49, Int 48, Wis [obscured, ~49], Cha 48 (from Prismatic-Dragon-by-Age abilities table, old row)', 185),
    ('Devastation Beetle', 'Colossal Vermin', '128d8+2,304 (2,880 hp)', '72 (-8 size, +10 Dex, +60 natural)', '50', 'Always neutral', 'Trample 30d10+24, acid cloud', 'Darkvision 300 ft., SR 60, DR 50/+10', 'Str 42, Dex 31, Con 46, Int --, Wis 10, Cha 9', 178),
    ('Hecatoncheires', 'Huge Outsider (Evil)', '52d8+572 (988 hp)', '70 (-2 size, +30 natural, +20 insight, +12 armor [+2 half-plate])', '57', 'Always chaotic evil', 'Superior multiweapon fighting, spell-like abilities, summon hecatoncheires', 'Abomination traits, electricity immunity, regeneration 40, fast healing 50, SR 70, DR [tens-digit margin-clipped]/+12', 'Str 50, Dex 15, Con 32, Int 10, Wis 8, Cha 24', 163),
]

COLS = ["name", "size_type", "hit_dice", "armor_class", "challenge_rating",
        "alignment", "special_attacks", "special_qualities", "abilities", "page"]

# ---------------------------------------------------------------------------
# FULL-DESCRIPTION SOURCE — rendered PDF pages, raw two-column OCR.
# ---------------------------------------------------------------------------
SOURCE_PAGE_RE = re.compile(r"^## \[PDF pages? (\d+)(?:-(\d+))?\]$")
SOURCE_HEADING_RE = re.compile(r"^(.+?) \[EPIC MONSTER DESCRIPTION\]$")

_DESCRIPTION_KEY_OVERRIDES = {
    "Advanced Red Great Wyrm (sample advanced dragon)": "Advanced Dragons",
    "Force Dragon (adult)": "Force Dragon",
    "Prismatic Dragon (old)": "Prismatic Dragon",
    "Hagunemnon (Protean)": "Hagunemnon",
    "Neh-thalggu (Brain Collector)": "Neh-thalggu",
    "Umbral Blot (Blackball)": "Umbral Blot",
    "Behemoth Eagle": "Behemoth",
    "Behemoth Gorilla": "Behemoth",
    "Stone Colossus": "Colossus",
    "Flesh Colossus": "Colossus",
    "Iron Colossus": "Colossus",
    "Devastation Beetle": "Devastation Vermin",
    "Devastation Centipede": "Devastation Vermin",
    "Devastation Scorpion": "Devastation Vermin",
    "Devastation Spider": "Devastation Vermin",
    "Primal Air Elemental": "Elemental, Primal",
    "Primal Earth Elemental": "Elemental, Primal",
    "Primal Fire Elemental": "Elemental, Primal",
    "Primal Water Elemental": "Elemental, Primal",
    "Mithral Golem": "Golem",
    "Adamantine Golem": "Golem",
    "Hoary Hunter": "Hoary Hunter",
    "Hoary Steed": "Hoary Hunter",
    "Legendary Bear": "Legendary Animal",
    "Legendary Tiger": "Legendary Animal",
    "Sirrush": "Sirrush",
    "Three-Headed Sirrush": "Sirrush",
    "White Slaad": "Slaad",
    "Black Slaad": "Slaad",
}


def _description_key(name: str) -> str:
    return _DESCRIPTION_KEY_OVERRIDES.get(
        name, re.sub(r"\s*\([^)]*\)\s*$", "", name).strip()
    )


def _all_description_keys() -> List[str]:
    return sorted({_description_key(row[0]) for row in _MONSTERS})


# Canonical section key -> (book page, visual column, y). The coordinates were
# checked against rendered pages. Shared book sections deliberately back more
# than one stat row where the book prints the variants together.
DESCRIPTION_ANCHORS: Dict[str, Tuple[int, int, float]] = {
    "Anaxim": (158, 0, 874.0),
    "Atropal": (159, 1, 60.0),
    "Chichimec": (160, 1, 380.0),
    "Dream Larva": (161, 1, 55.0),
    "Hecatoncheires": (162, 1, 715.0),
    "Infernal": (164, 0, 55.0),
    "Phaethon": (165, 0, 655.0),
    "Phane": (166, 0, 724.0),
    "Xixecal": (167, 1, 740.0),
    "Behemoth": (169, 0, 350.0),
    "Brachyurus": (170, 0, 70.0),
    "Colossus": (170, 1, 710.0),
    "Demilich": (174, 0, 575.0),
    "Devastation Vermin": (177, 0, 575.0),
    "Advanced Dragons": (179, 0, 630.0),
    "Force Dragon": (182, 0, 261.0),
    "Prismatic Dragon": (184, 1, 218.0),
    "Elemental, Primal": (186, 1, 335.0),
    "Genius Loci": (190, 0, 65.0),
    "Gibbering Orb": (191, 0, 600.0),
    "Gloom": (192, 1, 533.0),
    "Golem": (193, 1, 245.0),
    "Ha-naga": (195, 0, 290.0),
    "Hagunemnon": (196, 0, 65.0),
    "Hoary Hunter": (197, 0, 400.0),
    "Hunefer": (198, 1, 748.0),
    "Lavawight": (200, 0, 121.0),
    "Legendary Animal": (201, 0, 60.0),
    "LeShay": (202, 0, 440.0),
    "Living Vault": (203, 1, 600.0),
    "Mercane": (204, 1, 639.0),
    "Mu Spore": (205, 1, 315.0),
    "Neh-thalggu": (206, 1, 405.0),
    "Paragon Mind Flayer": (208, 1, 242.0),
    "Prismasaurus": (210, 0, 550.0),
    "Pseudonatural Troll": (211, 0, 255.0),
    "Ruin Swarm": (213, 0, 170.0),
    "Shadow of the Void": (214, 0, 120.0),
    "Shape of Fire": (215, 0, 420.0),
    "Sirrush": (216, 0, 160.0),
    "Slaad": (217, 1, 170.0),
    "Tayellah": (220, 0, 65.0),
    "Thorciasid": (220, 1, 500.0),
    "Elder Titan": (221, 1, 690.0),
    "Elder Treant": (223, 0, 65.0),
    "Umbral Blot": (223, 1, 345.0),
    "Uvuudaum": (224, 1, 710.0),
    "Vermiurge": (226, 0, 110.0),
    "Winterwight": (227, 0, 135.0),
    "Worm That Walks": (228, 0, 275.0),
}

# Tesseract places the final Hunefer line and the Lavawight title at the same
# vertical coordinate. The stable OCR line order is therefore the only exact
# boundary: rank is zero-based among rows at that y-coordinate.
DESCRIPTION_LINE_SPLITS: Dict[str, Tuple[int, int, float, int]] = {
    "Lavawight": (200, 0, 121.0, 1),
}


def _source_hash() -> Optional[str]:
    return hashlib.sha256(SOURCE.read_bytes()).hexdigest() if SOURCE.is_file() else None


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
    for book_page in range(158, 231):
        page = doc[book_page - 1]
        columns = ((8, 350), (350, 692)) if book_page % 2 == 0 \
            else ((8, 285), (285, 692))
        for column, (x0, x1) in enumerate(columns):
            clip = page.rect & fitz.Rect(x0, 55, x1, 945)
            pix = page.get_pixmap(
                matrix=fitz.Matrix(4, 4), clip=clip, alpha=False
            )
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
        print(f"OCR source extraction: page {book_page}/230", flush=True)
    return lanes


def _meaningful_ocr(lines: Sequence[dict], low: float, high: float) -> List[str]:
    out: List[str] = []
    for row in lines:
        if low <= row["top"] < high:
            text = row["text"].strip()
            if sum(char.isalnum() for char in text) >= 2:
                out.append(text)
    return out


def _line_split_index(
    name: str,
    page: int,
    column: int,
    lines: Sequence[dict],
) -> Optional[int]:
    spec = DESCRIPTION_LINE_SPLITS.get(name)
    if spec is None:
        return None
    split_page, split_column, split_y, rank = spec
    if (page, column) != (split_page, split_column):
        raise RuntimeError(f"line split for {name} is on the wrong OCR lane")
    matches = [
        index for index, row in enumerate(lines)
        if abs(row["top"] - split_y) < 0.1
    ]
    if rank >= len(matches):
        raise RuntimeError(
            f"line split for {name} expected rank {rank} at y={split_y}, "
            f"found {len(matches)} row(s)"
        )
    return matches[rank]


def _description_body(
    name: str,
    next_name: Optional[str],
    lane_map: Dict[Tuple[int, int], List[dict]],
    lane_keys: Sequence[Tuple[int, int]],
) -> Tuple[List[str], List[int]]:
    page, column, y = DESCRIPTION_ANCHORS[name]
    if next_name is None:
        end_page, end_column, end_y = 230, 1, float("inf")
    else:
        end_page, end_column, end_y = DESCRIPTION_ANCHORS[next_name]

    lane_index = {key: index for index, key in enumerate(lane_keys)}
    start_lane = lane_index[(page, column)]
    end_lane = lane_index[(end_page, end_column)]
    if end_lane < start_lane:
        raise RuntimeError(f"description end precedes start for {name}")

    body: List[str] = []
    pages = set()
    for index in range(start_lane, end_lane + 1):
        lane_page, lane_column = lane_keys[index]
        lane_lines = lane_map[(lane_page, lane_column)]
        first = 0
        last = len(lane_lines)
        low = y - 5 if index == start_lane else float("-inf")
        high = end_y - 8 if index == end_lane else float("inf")

        if index == start_lane:
            split = _line_split_index(
                name, lane_page, lane_column, lane_lines
            )
            if split is not None:
                first = split
                low = float("-inf")
        if index == end_lane and next_name is not None:
            split = _line_split_index(
                next_name, lane_page, lane_column, lane_lines
            )
            if split is not None:
                last = split
                high = float("inf")

        selected = _meaningful_ocr(lane_lines[first:last], low, high)
        if selected:
            body.extend(selected)
            pages.add(lane_page)
    return body, sorted(pages)


def extract_description_source() -> int:
    if not PDF_SOURCE.is_file():
        print(f"NO COVERAGE: {BOOK} epic monster descriptions "
              f"(missing PDF: {PDF_SOURCE})")
        return 1
    try:
        import fitz
    except Exception as exc:
        print(f"NO COVERAGE: {BOOK} epic monster descriptions "
              f"(PyMuPDF unavailable: {exc})")
        return 1

    names = _all_description_keys()
    missing = set(names) - set(DESCRIPTION_ANCHORS)
    extra = set(DESCRIPTION_ANCHORS) - set(names)
    if missing or extra:
        raise RuntimeError(
            f"description anchor mismatch: missing={sorted(missing)}, "
            f"extra={sorted(extra)}"
        )
    try:
        doc = fitz.open(PDF_SOURCE)
        lanes = _ocr_lanes(doc)
    except Exception as exc:
        print(f"NO COVERAGE: {BOOK} epic monster descriptions ({exc})")
        return 1

    lane_map = {(lane["page"], lane["column"]): lane["lines"]
                for lane in lanes}
    lane_keys = sorted(lane_map)
    ordered = sorted(names, key=lambda key: DESCRIPTION_ANCHORS[key])
    chunks = [
        "# EPIC MONSTER DESCRIPTION EXTRACTION",
        "",
        "Derived from Epic Level Handbook PDF page images, pp. 158-230.",
        "Two-column OCR is preserved raw. Monster section headings alone are",
        "restored from the book-verified index and rendered-page audit.",
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
            f"{name.upper()} [EPIC MONSTER DESCRIPTION]",
            *body,
            "",
        ])

    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    SOURCE.write_text("\n".join(chunks).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {SOURCE}")
    print(f"{len(ordered)}/{len(ordered)} epic-monster description blocks recovered")
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
    canonical = {_name_key(name): name for name in _all_description_keys()}
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
                f"unknown epic-monster heading at line {index + 1}: {line!r}"
            )
        headings.append((canonical[key], marker_index, index, marker_pages))

    spans: Dict[str, DescriptionSpan] = {}
    for position, (name, _, start, pages) in enumerate(headings):
        end = headings[position + 1][1] if position + 1 < len(headings) \
            else len(lines)
        while end > start and not lines[end - 1].strip():
            end -= 1
        if name in spans:
            raise ValueError(f"duplicate epic-monster description heading: {name}")
        spans[name] = DescriptionSpan(
            page=int(pages.split("-", 1)[0]),
            pages=pages,
            start=start,
            end=end,
        )
    return spans


def _source_lines() -> List[str]:
    return SOURCE.read_text(encoding="utf-8").splitlines() \
        if SOURCE.is_file() else []


@dataclass
class EpicMonster:
    name: str
    book: str
    size_type: str
    hit_dice: str
    armor_class: str
    challenge_rating: str
    alignment: str
    special_attacks: str
    special_qualities: str
    abilities: str
    citation: str
    page: int
    description_key: str = ""
    description_pages: str = ""
    start: int = 0
    end: int = 0
    soft: Optional[str] = None


def cr_int(cr: str) -> int:
    """Leading integer of a challenge_rating string (e.g. '39 (per...)' -> 39)."""
    m = re.match(r"\s*(\d+)", str(cr))
    return int(m.group(1)) if m else -1


def build(lines: Optional[Sequence[str]] = None) -> List[EpicMonster]:
    source_lines = list(lines) if lines is not None else _source_lines()
    spans = detect_description_spans(source_lines) if source_lines else {}
    if lines is None and not source_lines:
        print(f"NO COVERAGE: {BOOK} epic monster descriptions "
              "(derived OCR source is missing)")

    out: List[EpicMonster] = []
    seen = set()
    for row in _MONSTERS:
        d = dict(zip(COLS, row))
        key = d["name"].lower()
        if key in seen:
            continue
        seen.add(key)
        description_key = _description_key(d["name"])
        span = spans.get(description_key)
        d["book"] = BOOK
        d["citation"] = CITATION
        d["description_key"] = description_key
        if span:
            d["description_pages"] = span.pages
            d["start"] = span.start
            d["end"] = span.end
            d["soft"] = None
        else:
            d["description_pages"] = ""
            d["start"] = 0
            d["end"] = 0
            d["soft"] = ("NO COVERAGE: full description "
                         "(derived description extraction is missing)")
        out.append(EpicMonster(**d))
    out.sort(key=lambda m: (cr_int(m.challenge_rating), m.name))
    return out


def write_index() -> int:
    monsters = build()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    md: List[str] = [
        "# EPIC MONSTER INDEX — The New Path",
        "",
        "**Generated by `scripts/epic_monster_harvest.py`. Do not hand-edit; rerun",
        "the harvest.** D&D 3.5 epic monsters from the Epic Level Handbook (Chapter",
        "6, 'Monsters'). **Vision-transcribed from the PDF page images** because the",
        "book's OCR text layer is corrupt — this is still book RAW, read directly",
        "off the page, and every entry is cited to the PDF page of its stat block.",
        "Key mechanical fields remain the vision-verified transcription; every row",
        "also carries an exact span into reproducible two-column OCR of the full",
        "printed stat block and description.",
        "",
        "Abomination stat blocks carry MAXIMUM hit points per Hit Die (a stated",
        "Abomination Trait). Faded or art-clipped glyphs are cross-checked against",
        "the block's own Con-bonus / component arithmetic, or flagged in-line —",
        "never invented.",
        "",
        f"*{len(monsters)} epic monsters — the complete p.156 Monsters-by-CR table, "
        f"CR {cr_int(monsters[0].challenge_rating)} to "
        f"{cr_int(monsters[-1].challenge_rating)}.*",
        "",
        "| Monster | CR | Size / Type | Hit Dice | AC | Alignment | Special Attacks | Special Qualities | Abilities | Page | Description Pages |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for m in monsters:
        cells = [m.name, m.challenge_rating, m.size_type, m.hit_dice, m.armor_class,
                 m.alignment, m.special_attacks, m.special_qualities, m.abilities,
                 str(m.page), m.description_pages]
        cells = [c.replace("|", r"\|") for c in cells]
        md.append("| " + " | ".join(cells) + " |")
    md.append("")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/epic_monster_harvest.py",
                    "corpus": str(CORPUS),
                    "source_path": str(SOURCE_REL),
                    "source_sha256": _source_hash(),
                    "book": BOOK, "citation": CITATION, "pages": PAGES,
                    "description_pages": "158-230",
                    "description_blocks": len(_all_description_keys()),
                    "full_description_entries": sum(
                        m.start < m.end for m in monsters),
                    "note": (NOTE + " Full printed stat blocks and descriptions "
                             "are attached by exact line span into a reproducible "
                             "two-column OCR extraction; shared book sections back "
                             "their printed variant rows."),
                    "total_monsters": len(monsters),
                    "monsters": [asdict(m) for m in monsters]}, indent=1),
        encoding="utf-8")
    return len(monsters)


def export_packet(query: str, out_path: Optional[Path]) -> int:
    q = query.casefold().strip()
    hits = [monster for monster in build() if q in monster.name.casefold()]
    if not hits:
        print(f"NO COVERAGE: epic monster export ({query!r} not found)")
        return 1
    lines = _source_lines()
    packet = {
        "generated_by": "scripts/epic_monster_harvest.py --export",
        "query": query,
        "source": str(SOURCE),
        "source_sha256": _source_hash(),
        "entries": [],
    }
    for monster in hits:
        row = asdict(monster)
        row["full"] = "\n".join(lines[monster.start:monster.end]).strip() \
            if monster.start < monster.end else ""
        packet["entries"].append(row)
    text = json.dumps(packet, indent=2)
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {out_path}")
    else:
        print(text)
    return 0


def selftest() -> int:
    failures: List[str] = []
    monsters = build()

    # Lock the complete p.156 roster count.
    if len(monsters) != 64:
        failures.append(f"monster count {len(monsters)}, expected exactly 64")

    by_name = {m.name: m for m in monsters}

    # no duplicate names
    if len({m.name.lower() for m in monsters}) != len(monsters):
        failures.append("duplicate monster names")

    # every monster carries the key stat fields + a positive page + a numeric CR
    for m in monsters:
        for fld in ("size_type", "hit_dice", "armor_class", "challenge_rating",
                    "alignment", "abilities"):
            if not str(getattr(m, fld)).strip():
                failures.append(f"{m.name}: missing {fld}")
                break
        if not m.page or m.page <= 0:
            failures.append(f"{m.name}: bad page {m.page}")
        if cr_int(m.challenge_rating) < 0:
            failures.append(f"{m.name}: unparseable CR {m.challenge_rating!r}")
        if m.book != BOOK:
            failures.append(f"{m.name}: book not {BOOK!r}")

    # known epic monsters present with the right size_type / hit_dice / CR
    probes = {
        "Atropal": ("Large Undead, Outsider (Evil)", "66d12", 30),
        "Hecatoncheires": ("Huge Outsider (Evil)", "52d8+572", 57),
        "Mercane": ("Large Outsider (Lawful)", "7d8+21", 5),
        "Devastation Beetle": ("Colossal Vermin", "128d8+2,304", 50),
        "Demilich": ("Diminutive Undead", "21d12", 29),
        "Umbral Blot (Blackball)": ("Medium-Size Construct", "57d10", 32),
        "Elder Titan": ("Colossal Outsider", "70d8+700", 30),
        "Winterwight": ("Medium-Size Undead (Cold)", "42d12", 23),
    }
    for name, (st, hd, cr) in probes.items():
        m = by_name.get(name)
        if not m:
            failures.append(f"missing monster '{name}'")
            continue
        if m.size_type != st:
            failures.append(f"{name}: size_type {m.size_type!r}, expected {st!r}")
        if hd not in m.hit_dice:
            failures.append(f"{name}: hit_dice {m.hit_dice!r} lacks {hd!r}")
        if cr_int(m.challenge_rating) != cr:
            failures.append(f"{name}: CR {m.challenge_rating!r}, expected {cr}")

    # CR range sanity (the roster spans 5..57)
    crs = [cr_int(m.challenge_rating) for m in monsters]
    if min(crs) != 5 or max(crs) != 57:
        failures.append(f"CR range {min(crs)}..{max(crs)}, expected 5..57")

    fixture = [
        "## [PDF page 158]",
        "ANAXIM [EPIC MONSTER DESCRIPTION]",
        "raw anaxim body",
        "",
        "## [PDF pages 169-170]",
        "BEHEMOTH [EPIC MONSTER DESCRIPTION]",
        "raw behemoth body",
    ]
    fixture_spans = detect_description_spans(fixture)
    anaxim = fixture_spans.get("Anaxim")
    behemoth = fixture_spans.get("Behemoth")
    if not anaxim or (anaxim.pages, anaxim.start, anaxim.end) != ("158", 1, 3):
        failures.append(f"span fixture Anaxim mismatch: {anaxim}")
    if not behemoth or (behemoth.pages, behemoth.start,
                       behemoth.end) != ("169-170", 5, 7):
        failures.append(f"span fixture Behemoth mismatch: {behemoth}")

    if set(_all_description_keys()) != set(DESCRIPTION_ANCHORS):
        failures.append("description keys and verified anchors differ")
    if len(_all_description_keys()) != 50:
        failures.append(
            f"description block count {len(_all_description_keys())}, expected 50"
        )

    key_counts = Counter(m.description_key for m in monsters)
    expected_shared = {
        "Behemoth": 2,
        "Colossus": 3,
        "Devastation Vermin": 4,
        "Elemental, Primal": 4,
        "Golem": 2,
        "Hoary Hunter": 2,
        "Legendary Animal": 2,
        "Sirrush": 2,
        "Slaad": 2,
    }
    for key, count in expected_shared.items():
        if key_counts.get(key) != count:
            failures.append(
                f"description key {key!r} backs {key_counts.get(key, 0)} rows, "
                f"expected {count}"
            )

    source_lines = _source_lines()
    recovered = [m for m in monsters if m.start < m.end]
    if len(recovered) != 64:
        failures.append(f"full description rows {len(recovered)}, expected 64")
    if len({(m.start, m.end) for m in recovered}) != 50:
        failures.append("description spans are not exactly 50 shared blocks")
    if source_lines and not _source_hash():
        failures.append("derived source exists but has no SHA-256")
    if source_lines:
        hunefer = by_name["Hunefer"]
        lavawight = by_name["Lavawight"]
        hunefer_lines = source_lines[hunefer.start:hunefer.end]
        lavawight_lines = source_lines[lavawight.start:lavawight.end]
        if not any("doubles" in line.casefold()
                   for line in hunefer_lines[-5:]):
            failures.append("Hunefer/Lavawight split dropped Hunefer's last line")
        if any("lavawi" in _name_key(line)
               for line in hunefer_lines[-5:]):
            failures.append("Hunefer span bleeds into the Lavawight title")
        if not any("lavawi" in _name_key(line)
                   for line in lavawight_lines[1:4]):
            failures.append("Lavawight span omits its raw OCR title")
    for m in monsters:
        if m.soft is not None:
            failures.append(f"'{m.name}' unexpectedly soft: {m.soft}")
        if not m.description_pages:
            failures.append(f"'{m.name}' has no description_pages")
        if m.start < m.end:
            if m.end > len(source_lines):
                failures.append(f"'{m.name}' span ends past source length")
            elif _name_key(m.description_key) not in _name_key(source_lines[m.start]):
                failures.append(
                    f"'{m.name}' span does not lead with {m.description_key!r}"
                )

    for f in failures:
        print(f"SELFTEST FAIL: {f}")
    print("selftest: " + ("PASS" if not failures else f"{len(failures)} failure(s)"))
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--search", metavar="TEXT")
    ap.add_argument("--export", metavar="NAME",
                    help="emit a translator-ready packet")
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
        hits = [m for m in build()
                if q in m.name.lower()
                or q in m.size_type.lower()
                or q in m.alignment.lower()
                or q in m.special_attacks.lower()
                or q in m.special_qualities.lower()]
        for m in hits:
            print(f"  {m.name} — CR {m.challenge_rating.split(' ')[0]}, {m.size_type}, "
                  f"HD {m.hit_dice.split(' (')[0]}, AC {m.armor_class.split(' ')[0]}, "
                  f"{m.alignment} [p.{m.page}]")
        print(f"{len(hits)} match(es).")
        return 0 if hits else 1

    n = write_index()
    print(f"{n} D&D 3.5 epic monsters (Epic Level Handbook, Chapter 6, "
          f"vision-transcribed from the PDF page images).")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
