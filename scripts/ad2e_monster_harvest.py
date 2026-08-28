#!/usr/bin/env python3
"""ad2e_monster_harvest.py — AD&D 2e monsters, vision-transcribed (labelled).

WHY THIS ONE IS DIFFERENT (same story as epic_feat_harvest). The AD&D 2e
Monstrous Compendium stat blocks were OCR'd as a two-column dump whose VALUE
cells do not line up with their labels (the value order is scrambled), so parsing
the text extraction is hopeless. But the source PDF's page IMAGES are perfectly
legible, so each monster's stat block was transcribed BY VISION from the rendered
pages (PyMuPDF render → read the PNG). This is still book RAW — read directly off
the page, not invented — and cited to the exact pages. Labelled `system: AD&D 2e`
per the other-editions policy (the translator tools convert it); it is a DIFFERENT
edition from the 3.5e `creature_index` and the 5e `dnd5e_creature_index`.

This index now covers BOTH Planescape Monstrous Compendium bestiaries of the
planes — Appendix II (Outer Planes) and Appendix III (Inner/Astral/Ethereal
Planes). Every row carries its own `book`, so the two appendices are kept
distinct while sharing one index. App III was harvested the same way as App II:
its PDF is IMAGE-ONLY (empty/garbled text layer), so each of its stat blocks was
read by vision off the rendered page and cited to the printed page number.

    reference/ad2e_monster_index.json — every monster: the full AD&D 2e stat
                                        block (AC descending, THAC0, HD, No.
                                        Appearing, alignment, size, XP, ...)
    reference/ad2e_monster_index.md   — the same, for human eyes

PROVENANCE
    Planescape Monstrous Compendium Appendix II (TSR, AD&D 2e) — 25 monsters.
    Planescape Monstrous Compendium Appendix III (TSR, 1998, AD&D 2e; by Monte
    Cook) — 71 stat blocks (the Inner-Planes appendix of minor "animals" is
    prose-only and deliberately NOT indexed here — this index holds only full
    stat-block monsters). Both were rendered from the PDF and read by vision
    because the OCR text layer scrambles / does not exist for the stat columns.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO = Path(__file__).resolve().parent.parent
OUT_JSON = REPO / "reference" / "ad2e_monster_index.json"
OUT_MD = REPO / "reference" / "ad2e_monster_index.md"
SYSTEM = "AD&D 2e"
BOOK_II = "Planescape Monstrous Compendium Appendix II"
BOOK_III = "Planescape Monstrous Compendium Appendix III"
CITATION_II = ("Planescape Monstrous Compendium Appendix II (TSR, AD&D 2e); "
               "vision-transcribed from the PDF page images (the OCR text layer "
               "scrambles the stat columns)")
CITATION_III = ("Planescape Monstrous Compendium Appendix III (TSR, 1998, AD&D "
                "2e); vision-transcribed from the PDF page images (the source is "
                "image-only — its text layer is empty/garbled). Cited to the "
                "printed page number.")
# Back-compat aliases (this module's original single-book constants).
BOOK = BOOK_II
CITATION = CITATION_II

# Field order matches the AD&D 2e stat block. Transcribed from the MC App pages.
COLS = ["name", "page", "climate_terrain", "frequency", "organization",
        "activity_cycle", "diet", "intelligence", "treasure", "alignment",
        "no_appearing", "armor_class", "movement", "hit_dice", "thac0",
        "no_of_attacks", "damage_attack", "special_attacks", "special_defenses",
        "magic_resistance", "size", "morale", "xp_value"]

_ROWS = [
    ("Aasimar", 7, "Any", "Rare", "Solitary", "Any", "Omnivore", "Very (11-12)", "R, U", "Any nonevil",
     "1 (1-2)", "3 (10)", "12", "3+3", "17", "1 or by weapon", "1d3 or by weapon", "Spell use",
     "1/2 damage from fire and cold; +2 to saves vs. charm, emotion, fear, or domination", "10%", "M (5.5-6.5' tall)", "Elite (13-14)", "420"),
    ("Abrian", 9, "Outlands, Lower Planes", "Common", "Flock", "Day", "Carnivore", "Low (5-7)", "B (nest); individual J,K,M", "Chaotic evil",
     "4-40", "6", "18", "2+3", "17", "1 beak and 1 kick", "1d3/1d8", "Shriek", "None", "None", "M (7' tall)", "Unsteady (5-7)", "175"),
    ("Eladrin, Bralani (Lesser)", 31, "Arborea (Pelion)", "Uncommon (Common)", "Band", "Any", "Omnivore", "Very (13-14)", "Incidental", "Chaotic good",
     "1-3 (3-24)", "2 (-2)", "15, Fl 30 (A)", "6+9", "15", "1 or 2", "By weapon +4 or 1d10/1d10", "Whirlwind", "See below", "35%", "M (5' tall)", "Elite (13-14)", "9,000"),
    ("Eladrin, Firre (Greater)", 33, "Arborea", "Rare", "Solitary", "Any", "Omnivore", "Genius (17-18)", "Incidental", "Chaotic good",
     "1-4", "-3", "15, Fl 36 (A)", "7+10", "13", "1 or 2", "By weapon +6 or 3d6/3d6", "Spellsong", "Magic use, shapechange; struck only by cold iron or weapon of +2 or better", "40%", "M (6' tall)", "Champion (15-16)", "14,000"),
    ("Eladrin, Ghaele (Greater)", 34, "Arborea", "Rare", "Solitary", "Any", "Omnivore", "Exceptional-Genius (15-18)", "Incidental", "Chaotic good",
     "1 (1-3)", "-5", "18, Fl 60 (A)", "10+15", "11", "1 or 2", "By weapon +7 or 2d12/2d12", "Positive energy, gaze", "Struck only by cold iron or weapon of +3 or better", "40%", "M (6' tall) or L (20' wingspan)", "Fearless (19-20)", "19,000"),
    ("Eladrin, Noviere (Lesser)", 35, "Arborea", "Uncommon", "Clan", "Any", "Omnivore", "High (13-14)", "Incidental", "Chaotic good",
     "2-16", "3 (-3)", "15, Sw 24", "5+7", "15", "1 weapon or 1 ram", "By weapon +3 or 2d8", "Drowning", "Dolphin form", "20%", "M (5' tall or 7' long)", "Fanatic (17-18)", "5,000"),
    ("Eladrin, Shiere (Lesser)", 36, "Arborea", "Common", "Company", "Night", "Omnivore", "Very-Exceptional (11-16)", "Incidental", "Chaotic good",
     "3-24", "4 (-4)", "15, Fl 24 (A)", "8+12", "13", "2", "By weapon +6", "Glance", "Magic use", "25%", "M (7' tall)", "Fearless (19-20)", "11,000"),
    ("Fhorge", 39, "Outlands, Acheron, Baator", "Uncommon", "Pack", "Any", "Omnivore", "Semi- (2-4)", "None", "Neutral",
     "1 (2-8)", "6, head 3", "15", "5+5", "15", "1 and 1", "3d6 and 1d3", "Charge", "+2 on saves vs. mind-affecting or emotion-based spells; continue fighting until reduced to -10 hp", "None", "L (5' high at shoulder)", "Elite (13-14)", "1,400"),
    ("Guardinal, Cervidal", 46, "Elysium", "Common", "Family", "Day", "Herbivore", "High (11-12)", "Incidental", "Neutral good",
     "1 (2-5)", "2", "18, Ju 3", "4+2", "17", "2 hooves and 1 butt", "1d6+2/1d6+2/1d12+3", "Charge", "Negate poison or illusion", "20%", "M (5.5' tall)", "Elite (13-14)", "3,000"),
    ("Guardinal, Lupinal", 49, "Elysium", "Rare", "Pack", "Any", "Omnivore", "Exceptional (15-16)", "Incidental", "Neutral good",
     "1-8", "-2", "18", "8+4", "13", "3", "1d4+4/1d4+4/2d6", "Howl, pull-down", "Struck only by silver or +2 or better weapons", "35%", "M (6' tall)", "Fanatic (17-18)", "9,000"),
    ("Guardinal, Ursinal", 50, "Elysium", "Rare", "Solitary", "Any", "Omnivore", "Genius (17-18)", "Incidental", "Neutral good",
     "1 (1-2)", "-4", "12", "10+5", "11", "3", "2d6+7/2d6+7/1d10", "Spell-like powers", "Struck only by silver weapons or those of +3 or better enchantment", "45%", "L (8' tall)", "Fanatic (17-18)", "14,000"),
    ("Incantifer", 53, "Any", "Very Rare", "Solitary", "Any", "Special", "Supra-genius (19-20)", "R x3 and incidental", "Neutral (evil)",
     "1", "0 or better", "12", "9d4+18 to 9d4+26", "13", "1", "By weapon", "Spells", "Absorption", "20% + 5% per level over 9th", "M (5-6' tall)", "Average (8-10)", "13,000+"),
    ("Leomarh", 61, "Outlands (any plains)", "Uncommon", "Pride", "Day", "Carnivore", "Low (5-7)", "None", "Neutral",
     "2-12", "4", "15", "6+2", "15", "3", "1d6+1/1d6+1/1d10", "Rear claws, knock-down", "Camouflage, immune to magic missiles", "None", "L (6'-7' long)", "Average (8-10)", "1,400"),
    ("Monster of Legend", 65, "Any", "Very rare", "Solitary", "Any", "Carnivore", "Per prime-material monster", "G, Z x2", "Per prime-material monster",
     "1", "0 or better (-6)", "Per prime-material monster (18, Fl 30 D)", "75-150 hit points (120 hp)", "5", "Per prime-material monster (3)", "Varies (4d6/4d6/2d10)", "Varies (roar)", "Varies", "Special (80%)", "Varies (H, 12' tall)", "Fearless (19-20)", "Special (35,000)"),
    ("Noctral", 69, "Mount Celestia", "Rare", "Solitary", "Dusk, night", "Carnivore", "Supra-genius (19-20)", "G", "Lawful good",
     "1", "1", "1, Fl 36 (C)", "5", "15", "3", "2d4/2d4/1d4+1", "Swoop, surprise", "Invisibility", "30%", "M (20' wingspan)", "Champion (15-16)", "3,000"),
    ("Rager", 77, "Any", "Rare", "Band", "Any", "Carnivore", "Low-Very (5-14)", "P, L, Q", "Any chaotic",
     "1-8", "Varies", "12", "3d10 to 8d10", "Varies", "Varies", "By weapon", "Berserk", "None", "None", "M (5'-7' tall)", "Champion (15-16)", "270-2,000 (by HD)"),
    ("Razorvine", 79, "Any", "Common", "Patch", "None", "Sun, soil", "Non- (0)", "None", "Neutral",
     "2-20 vines", "5", "0", "5 hp per vine", "20", "Special", "1d3, 1d4, or 1d6 + special", "None", "None", "None", "M (12'-20' long)", "None", "35 per vine"),
    ("Rilmani, Argenach", 88, "The Spire, any prime world", "Very rare", "Solitary", "Any", "Omnivore", "Genius (17-18)", "R, Z, U", "Neutral",
     "1 (1-4 at the Spire)", "-1", "15", "9", "11", "2 or 1", "1d20/1d20 (rays) or 1d8+10 (weapon +3, +7 damage) or 1d10 (bare fists)", "Beams, spells", "+3 weapon to hit", "55%", "M (7' tall)", "Champion (15-16)", "16,000"),
    ("Rilmani, Aurumach", 89, "The Spire", "Very rare", "Solitary", "Any", "Omnivore", "Godlike (21+)", "R, U, V x2", "Neutral",
     "1 (1-3 on the Spire)", "-3 (-7 in armor)", "15", "12", "9", "3", "1d10+11 (weapon +3, Strength bonus) or 2d8 (bare fists)", "Aura, spells", "Aura, struck only by +4 or better weapons", "65%", "L (10' tall)", "Fanatic (17-18)", "27,000"),
    ("Simpathetic", 95, "Plains, desert, the Abyss", "Very rare", "Family or flock", "Day", "Carnivore/scavenger", "High (13-14)", "None", "Chaotic evil",
     "1-6 (family) or 4-400 (flock)", "7", "3, Fl 18 (B)", "1-4 hp", "20", "1", "1d2", "Alignment drain, spit blood", "Immune to fire-based attacks", "20%", "T (2' wingspan)", "Champion (15-16)", "175"),
    ("Tanar'ri, Alkilith (True)", 107, "The Abyss", "Rare", "Solitary", "Any", "Carnivore", "High (13-14)", "F", "Chaotic evil",
     "1-3", "3", "6", "11", "9", "4", "2d4/2d4/2d4/2d4", "Acid, poison", "1/2 damage from Type S or B weapons; struck only by +2 or better weapons", "40%", "L (6' diameter)", "Champion (15-16)", "17,000"),
    ("Terlen", 115, "Carceri, Gehenna, Gray Waste", "Uncommon", "School", "Day", "Carnivore", "Animal (1)", "None", "Neutral (evil)",
     "1-8", "5", "3, Sw 15, Fl 15 (C)", "4+3", "17", "1", "2d8", "None", "Camouflage", "10%", "M (7' long)", "Elite (13-14)", "975"),
    ("Tso", 117, "Outlands, any lawful plane", "Rare", "Brood", "Any", "Omnivore", "High (13-14)", "E (individuals J,K,M,Q)", "Lawful evil",
     "3-18", "1 (0)", "9, Cl 3", "7", "13", "3 and 1", "1d4/1d4/1d8 and by weapon", "Poison, magic use", "None", "None", "M (5.5' tall)", "Unsteady (5-7)", "3,000"),
    ("Wastrel", 123, "Any forest, marsh, or swamp", "Common", "Flock", "Day", "Scavenger", "Semi- (2-4)", "None", "Neutral evil",
     "10-100", "6", "3, Fl 15 (C)", "1+1", "19", "1", "1d3", "Ability drain", "None", "50%", "S (3' wingspan)", "Unreliable (2-4)", "270"),
    ("Wraithworm", 125, "Any desert or wasteland", "Uncommon", "Solitary", "Day", "Carnivore", "Animal (1)", "None", "Neutral",
     "1", "5", "9", "5+3", "15", "1", "1d8", "Level drain, poison", "Wraithform", "30%", "M (10' long)", "Average (8-10)", "3,000"),
]

# --- Planescape MC Appendix III (TSR, 1998; by Monte Cook) -------------------
# 71 stat blocks, vision-transcribed off the image-only PDF pages (matrix 2.3;
# re-rendered to 4-6x where a value needed a spot-check). Same COLS order as
# _ROWS. `page` is the PRINTED page number (as cited in App II). Group entries
# with multiple named stat blocks are one row per block (Archomental Evil/Good,
# Homunculus Elemental, Paraelemental, Psurlon, Quasielemental Neg/Pos,
# Salamander, Shocker). The complete set was cross-checked against the book's own
# alphabetical index (every "(PS3)" full-stat entry present; the "(PS3, in
# Appendix)" minor animals — with no stat block — are deliberately excluded).
# NOTE: the Ruvoka page HEADER renders the name "RUVKOVA" in the decorative
# Planescape display font, but the body text (~6x) and the book's own index both
# spell it "ruvoka" — so the canonical/indexed spelling is used here.
_ROWS_APP3 = [
    ('Animental', 14, 'Inner Planes', 'Common (animals), rare (monsters)', 'Varies (usually solitary)', 'Any', 'Varies (usually carnivorous)', 'Varies', 'Nil', 'Neutral',
     'Varies (usually 1)', 'Varies', 'Varies', 'Varies', 'Varies', 'Varies', 'Varies', 'Varies', 'Varies', 'Nil', 'Varies', 'Varies', 'Varies'),
    ('Archomental (Evil), Cryonax', 16, 'Paraplane of Ice', 'Unique', 'Unique', 'Any', 'Carnivorous', 'Genius (17)', 'H,V,X', 'Neutral evil',
     '1', '-6', '9', '90 hp', '5', '2', '5d4/5d4', 'See below', 'See below', '75%', "L (15' tall)", 'Fearless (20)', '28,000'),
    ('Archomental (Evil), Imix', 16, 'Plane of Fire', 'Unique', 'Unique', 'Any', 'Carnivorous', 'Genius (18)', 'R,U', 'Neutral evil',
     '1', '-4', '18', '90 hp', '5', '1', '6d6', 'Heat, spells', 'See below', '85%', "L (18' tall)", 'Fearless (20)', '25,000'),
    ('Archomental (Evil), Ogremoch', 16, 'Plane of Earth', 'Unique', 'Unique', 'Any', 'Carnivorous', 'Exceptional (16)', 'H,U,Z', 'Neutral evil',
     '1', '-7', '9', '110 hp', '5', '2', '5d10/5d10', 'Spells', 'See below', '85%', "L (10' tall)", 'Fearless (20)', '28,000'),
    ('Archomental (Evil), Olhydra', 16, 'Plane of Water', 'Unique', 'Unique', 'Any', 'Carnivorous', 'Genius (18)', 'H,S,U', 'Neutral evil',
     '1', '-5', '6, Sw 18', '90 hp', '5', '1', '2d12', 'Engulf, spells', 'See below', '70%', "L (20' dia.)", 'Fearless (20)', '27,000'),
    ('Archomental (Evil), Yan-C-Bin', 16, 'Plane of Air', 'Unique', 'Unique', 'Any', 'Carnivorous', 'Genius (17)', 'U,Z', 'Neutral evil',
     '1', '-6', 'Fl 48 (A)', '85 hp', '5', '2', '2d10/2d10', 'See below', 'See below', '90%', "L (10' dia.)", 'Fearless (20)', '28,000'),
    ('Archomental (Good), Ben-hadar', 20, 'Plane of Water', 'Unique', 'Unique', 'Any', 'Carnivorous', 'Genius (17)', 'U,Z', 'Neutral good',
     '1', '-4', '12, Sw 18', '90 hp', '5', '2', '3d6/3d6', 'Spells', 'See below', '80%', "L (18' tall)", 'Fearless (20)', '24,000'),
    ('Archomental (Good), Chan', 20, 'Plane of Air', 'Unique', 'Unique', 'Any', 'Carnivorous', 'Genius (18)', 'H,S,U', 'Neutral good',
     '1', '-6', 'Fl 48 (A)', '90 hp', '5', '2', '2d10/2d10', 'Spells', 'See below', '85%', "L (10' diameter)", 'Fearless (20)', '28,000'),
    ('Archomental (Good), Sunnis', 20, 'Plane of Earth', 'Unique', 'Unique', 'Any', 'Carnivorous', 'Exceptional (16)', 'H,U,Z', 'Neutral good',
     '1', '-7', '9', '115 hp', '5', '2', '3d12/3d12', 'Spells', 'See below', '70%', "L (12' tall)", 'Fearless (20)', '29,000'),
    ('Archomental (Good), Zaaman Rul', 20, 'Plane of Fire', 'Unique', 'Unique', 'Any', 'Carnivorous', 'Genius (17)', 'R,U', 'Neutral good',
     '1', '-3', '12', '80 hp', '5', '1', '3d10', 'Spells, burning touch', 'See below', '60%', "L (10' tall)", 'Fearless (20)', '23,000'),
    ('Belker', 22, 'Paraplane of Smoke', 'Rare', 'Solitary', 'Any', 'Carnivore', 'Very (11-12)', 'Nil', 'Neutral evil',
     '1 or 1d3', '-2', '12, Fl 18 (B)', '7+3', '13', '3 or 2', '1d3/1d3/1d4 or 1d6/1d6', 'Noxious fumes', 'Smoke form, immunities', '20% (40% in smoke form)', "L (7'-9' tall)", 'Champion (15-16)', '5,000'),
    ('Bzastra', 24, 'Elemental Plane of Water', 'Very rare', 'Varies', 'Any', 'Omnivorous', 'Average to genius (10-18)', 'V', 'Neutral (rarely, any)',
     '1d6', '6 (or 0)', 'Sw 9', '5', '15', '1', '2d6', 'Telekinesis', 'Telekinesis', 'Nil', "M (5' tall)", 'Steady (11-12)', '650'),
    ('Chososion', 26, 'Inner Planes', 'Very rare', 'Solitary', 'Any', 'Inner-planar nature', 'High (13-14)', 'Nil', 'Neutral',
     '1', '-5', 'Fl 12 (A)', '8', '13', '2', '1d8/1d8', 'Discorporating poison', 'Struck only by +4 or better weapons, immunities', '95%', "M (6' across)", 'Elite (14)', '8,000'),
    ('Darklight', 28, 'Quasiplane of Radiance (any)', 'Very rare', 'Solitary', 'Any', 'Life energy', 'Very (11-12)', 'None', 'Any evil',
     '1', '0', 'Fl 12 (C)', '6+6 (but see below)', '13 (but see below)', '2', '1d4/1d4', 'Level drain, eye blast', 'Struck only by +1 weapons, invisibility, immunities', 'Nil', "M (6' tall)", 'Champion (15-16)', '7,000'),
    ('Devete', 30, 'Astral Plane', 'Rare', 'Solitary', 'Any', 'N/A', 'Average (8-10)', 'Nil', 'Neutral (rarely, neutral evil)',
     '1 (rarely, 1d3)', '6', '12 (42 on the Astral)', '4', '17', '3', 'Varies', 'Mimicry', 'Mimicry, immunities', 'Nil', "M (5' tall)", 'Elite (13-14)', '975'),
    ('Devourer', 32, 'Ethereal or Astral Plane', 'Very rare', 'Solitary', 'Any', 'Life energy', 'Exceptional (15-16)', 'Nil', 'Neutral evil',
     '1', '2', '12', '9+3', '11', '1', '2d6', 'Level drain, spirit theft, spells', 'Hit point recovery, protection from spells', '45%', "L (8' tall)", 'Fanatic (17)', '13,000'),
    ('Dharum Suhn', 34, 'Elemental Plane of Earth', 'Uncommon', 'Clan', 'Any', 'None', 'Genius (17-18)', 'Q (x20)', 'Neutral (lawful)',
     '1d4', '0', '6', '24', '5', '2', '3d8/3d8', 'Spells', 'Struck only by +1 or better weapons, immune to blunt weapons and impact attacks', '60%', "H (20' tall)", 'Fearless (20)', '32,000'),
    ('Egarus', 36, 'Quasiplane of Vacuum', 'Rare', 'Patch', 'N/A', 'Absence', 'Non- (0)', 'Nil', 'Neutral',
     '1d3 patches', '10', 'Nil', 'N/A', 'N/A', '0', '0', 'Disintegration', 'Teleportation, immune to cold, fire, physical attacks, most spells', '25%', 'T (one patch is 6" across)', 'N/A', '270'),
    ('Entrope', 38, 'Inner Planes', 'Very rare', 'None', 'Any', 'Planar boundaries', 'Low to average (7-10)', 'Nil', 'Chaotic neutral',
     '1', '3', '12', '11+6', '9', '3', '1d8/1d8/1d12', 'Sunder space', 'Struck only by +2 or better weapons, immune to elements', 'Nil', "H (20' long)", 'Fanatic (17-18)', '10,000'),
    ('Facet', 40, 'Quasiplane of Salt', 'Uncommon', 'Army', 'Any', 'Water', 'Average (8-10)', 'Nil', 'Neutral',
     '2d6', '4', '9', '3 (see below)', '17 (see below)', '2', '1d4/1d4 (see below)', 'Dehydration', 'Nil', 'Nil', "M (5' tall) (see below)", 'Average (8-10)', '175 (combined facet: 2-member 420, 3-member 1,400, 4-member 3,000, 5-member 6,000)'),
    ('Fire Bat', 42, 'Elemental Plane of Fire', 'Common', 'Pack', 'Any', 'Blood', 'Semi- (2-4)', 'I', 'Neutral evil',
     '10 + 1d10', '8', '6, Fl 21 (B)', '2', '19', '1', '2d4', 'Heat, blood drain', "Reform body, immune to fire, detect invisible, infravision 120'", 'Nil', "S (2' long, 4' wingspan)", 'Average (8-10)', '175'),
    ('Frost Salamander', 44, 'Paraplane of Ice', 'Rare', 'Solitary', 'Any', 'Omnivorous', 'Low (5-7)', 'E', 'Chaotic evil',
     '1d3', '3', '12', '12', '9', '5', '1d6 (x4)/2d6', 'Cold', 'Struck only by +1 or better weapons, immune to cold', 'Nil', "L (8' long)", 'Steady (11-12)', '9,000'),
    ('Fundamental', 46, 'Inner Planes', 'Common', 'Flock', 'Any', 'Varies', 'Semi- (3)', 'Nil', 'Neutral',
     '2d10', '3-6 (see below)', '9-24 (see below)', '1+1', '19', '1', '1d6', 'Nil', 'Struck only by +1 or better weapons, surprise, partial invisibility, immune to own element and sleep and charm', 'Nil', 'T (1-2\' "wingspan")', 'Average to steady (10-12)', '175'),
    ('Garmorm', 48, 'Astral Plane', 'Rare', 'Solitary', 'Any', 'Mental energy', 'Very to genius (12-18)', 'V', 'Chaotic evil',
     '1d3', '4 or 0', '18', '5-10', '15 (5-6 HD), 13 (7-8 HD), 11 (9-10 HD)', '1d6+5', '2d6 + 1d4 per absorbed face', 'Mental absorption, spells, magical items', 'Immune to psionics', '25%', "L (12' long)", 'Steady (11-12)', '8,000 (5 HD) / 9,000 (6 HD) / 10,000 (7 HD) / 11,000 (8 HD) / 12,000 (9 HD) / 13,000 (10 HD)'),
    ('Homunculus, Elemental (Breather)', 50, 'Varies', 'Varies', 'Nil', 'Any', 'None', 'Non- (0)', 'Nil', 'Neutral',
     '1', '8', 'Nil', '1d3 hp', 'N/A', 'Nil', 'Nil', 'Nil', 'Immune to one element', 'Nil', 'T (3" tall)', 'N/A', '15'),
    ('Homunculus, Elemental (Skin)', 50, 'Varies', 'Varies', 'Nil', 'Any', 'None', 'Non- (0)', 'Nil', 'Neutral',
     '1', '10', 'Nil', '2', 'N/A', 'Nil', 'Nil', 'Nil', 'Immune to one element', 'Nil', "M (6' tall)", 'N/A', '65'),
    ('Immoth', 52, 'Paraplane of Ice', 'Rare', 'Solitary', 'Any', 'Carnivorous', 'High to exceptional (14-16)', 'Special', 'Neutral',
     '1', '2', '12', '10+3', '9', '3', '1d8+1/1d8+1/2d4+2', 'Poison, words of power', 'Immune to cold, bladed weapons inflict half damage', '25%', "L (8' tall)", 'Fanatic (17-18)', '8,000'),
    ('Khargra', 54, 'Elemental Plane of Earth', 'Common', 'School', 'Any', 'Minerals', 'Low (5-7)', 'See below', 'Neutral',
     '1d8', '-3', '15 (3 out of element)', '6', '9', '3', 'Nil (arms), 3d6 (bite)', 'Surprise', 'Immune to heat and cold', 'Nil', "S (3 1/2' long)", 'Elite (13-14)', '1,400'),
    ('Klyndes', 56, 'Quasiplane of Steam', 'Rare', 'Solitary', 'Any', 'Carnivorous', 'Very (11-12)', 'Nil', 'Neutral',
     '1', '4', 'Fl 12 (A)', '4', '17', '4', '1d6 (x4)', 'Surprise', 'Shadow form, immune to heat, needs no air to breathe', 'Nil', "M (6' tall)", 'Steady (11-12)', '650'),
    ('Magran', 58, 'Ethereal Plane', 'Rare', 'School', 'Any', 'Carnivorous', 'Low (5-7)', 'Special', 'Neutral',
     '1d3 (or 3d6)', '3', '18', '12', '9', '1', '3d8', 'Hypnosis, swallow whole', 'Invisibility', 'Nil', "H (20' long)", 'Average (8-10)', '8,000'),
    ('Menglis', 60, 'Inner Planes', 'Very rare', 'Solitary', 'Any', 'None', 'High to genius (14-17)', 'Nil', 'Neutral',
     '1', '-4', '18', '9', '11', '1', '2d4+4', 'Disintegration', 'Struck only by +1 or better weapons, immune to elemental attacks', '45%', "L (10' tall)", 'Champion (20)', '8,000'),
    ('Nathri', 62, 'Ethereal Plane', 'Uncommon', 'Clan', 'Any', 'Omnivorous', 'Low to high (7-13)', 'K', 'Chaotic neutral',
     '2d20 (rarely, 2d100)', '6', '18', '1+1', '19', '1', '1d4 or by weapon', 'Poison', '+1 to saves vs. charm', 'Nil', "S (4' tall)", 'Steady (11-12)', '120'),
    ('Ooze Sprite', 64, 'Paraplane of Ooze', 'Common', 'Tribal', 'Any', 'Carnivorous', 'Average (8-10)', 'Nil', 'Neutral',
     '1d6 (sometimes 3d6)', '6', '6', '3 (king 10)', '17', '1', '1d6', 'Mind control', 'Malleable form, hide in ooze', 'Nil', "M (5'-6' long)", 'Average (8-10)', '650 (Ooze Sprite King: 5,000)'),
    ('Opposition', 66, 'Inner Planes', 'Very rare', 'Sect', 'Any', 'Omnivorous', 'Low to genius (5-18)', 'P,L,Q', 'Varies (generally neutral)',
     '1d6', 'Varies (4)', 'Varies (12)', 'Varies (4d10)', 'Varies (17)', 'Varies (1)', 'By weapon', 'Varies', 'Varies', 'Varies (nil)', 'Varies (M)', 'Elite to fanatic (14-18)', 'Varies'),
    ('Paraelemental, Ice', 68, 'Paraplane of Ice', 'Common', 'Band', 'Any', 'Warmth', 'Low to high (5-14)', 'Nil', 'Neutral',
     '1d6', '3', '6', '8, 12 or 16', '13 (8 HD), 9 (12 HD), 5 (16 HD)', '1', '3d8', 'Cold aura', 'See below', 'Nil', "L (8'-16' tall)", 'Champion (15-16)', '7,000 (8 HD) / 11,000 (12 HD) / 15,000 (16 HD)'),
    ('Paraelemental, Magma', 68, 'Paraplane of Magma', 'Common', 'Band', 'Any', 'Any solid', 'Low to high (5-14)', 'Nil', 'Neutral',
     '2d4', '3', '6', '8, 12 or 16', '13 (8 HD), 9 (12 HD), 5 (16 HD)', '1', '3d6', 'Heat aura', 'See below', 'Nil', "L (8'-16' tall)", 'Champion (15-16)', '3,000 (8 HD) / 7,000 (12 HD) / 11,000 (16 HD)'),
    ('Paraelemental, Ooze', 68, 'Paraplane of Ooze', 'Common', 'Band', 'Any', 'Any solid', 'Low to high (5-14)', 'Nil', 'Neutral',
     '1d6', '0', '36', '8, 12 or 16', '13 (8 HD), 9 (12 HD), 5 (16 HD)', '1', '2d8', 'Multiple tendrils', 'See below', 'Nil', "L (8'-16' tall)", 'Champion (15-16)', '3,000 (8 HD) / 7,000 (12 HD) / 11,000 (16 HD)'),
    ('Paraelemental, Smoke', 68, 'Paraplane of Smoke', 'Common', 'Band', 'Any', 'Air', 'Low to high (5-14)', 'Nil', 'Neutral',
     '1d6', '2', 'Fl 18 (E)', '8, 12 or 16', '13 (8 HD), 9 (12 HD), 5 (16 HD)', 'Special', '2d8', 'Blinding smoke', 'See below', 'Nil', "L (8'-16' tall)", 'Champion (15-16)', '3,000 (8 HD) / 7,000 (12 HD) / 11,000 (16 HD)'),
    ('Phirblas', 72, 'Ethereal Plane', 'Rare', 'Family', 'Any', 'Herbivorous', 'High to genius (14-18)', 'R,U', 'Neutral good',
     '1d4', '8 (1 with plate mail)', '9', '5', '15', '1', '1d4+1 or by weapon', 'Hypnotic pattern, suggestion', 'ESP, immunities', '20%', "M (6' tall)", 'Steady to elite (11-14)', '1,400'),
    ('Primal', 74, 'Inner Planes', 'Very rare', 'Solitary', 'Any', 'Omnivore', 'Average to genius (8-18)', 'R,S,T', 'Any',
     '1d4', 'Varies (10)', '12', 'Varies (6d4 hp)', 'Varies (19)', '1', 'By weapon (1d6)', 'Varies by rank', 'Varies by rank', 'Nil', "M (5'-7' tall)", 'Steady (11-12)', 'Varies (1,400)'),
    ('Psurlon', 76, 'Astral Plane', 'Very rare', 'Community', 'Any', 'Carnivore', 'Genius (17-18)', 'V', 'Lawful evil',
     '1d4', '4', '9', '7', '13', '3', '3d4/3d4/2d8', 'Psionics', 'See below', '40%', "M (7' long)", 'Elite (15-16)', '4,000'),
    ('Psurlon, Adept', 76, 'Astral Plane', 'Very rare', 'Solitary', 'Any', 'Carnivore', 'Supra-genius (19-20)', 'R,V', 'Lawful evil',
     '1', '3', '9', '12', '9', '3', '3d6/3d6/3d8', 'Psionics', 'See below', '50%', "M (10' long)", 'Fanatic (17-18)', '9,000'),
    ('Psurlon, Giant', 76, 'Astral Plane', 'Very rare', 'Solitary', 'Any', 'Carnivore', 'Genius (17-18)', 'C,G,V', 'Neutral evil',
     '1', '2', '15', '18', '3', '3', '3d8/3d8/3d10', 'Psionics', 'See below', '60%', "H (20' long)", 'Fearless (19)', '15,000'),
    ('Quasielemental (Negative), Ash', 78, 'Quasiplane of Ash', 'Common', 'Band', 'Any', 'Fire', 'Low to high (5-14)', 'Nil', 'Neutral',
     '1d6', '3', '12', '6, 9 or 12', '15 (6 HD), 11 (9 HD), 9 (12 HD)', '1', '1d6 + 1hp/HD', 'Drain heat', 'See below', 'Nil', "M (6' tall)", 'Champion (15-16)', '2,000 (6 HD) / 5,000 (9 HD) / 8,000 (12 HD)'),
    ('Quasielemental (Negative), Dust', 78, 'Quasiplane of Dust', 'Common', 'Band', 'Any', 'Any solid', 'Low to high (5-14)', 'Nil', 'Neutral',
     '1d6', '-1', '12', '6, 9 or 12', '15 (6 HD), 11 (9 HD), 9 (12 HD)', '1', '1d6 + 1 hp/HD', 'Engulf, dust storm', 'See below', 'Nil', "M (6' tall)", 'Champion (15-16)', '3,000 (6 HD) / 6,000 (9 HD) / 9,000 (12 HD)'),
    ('Quasielemental (Negative), Salt', 78, 'Quasiplane of Salt', 'Uncommon', 'Solitary', 'Any', 'Water', 'Low to high (5-14)', 'Nil', 'Neutral',
     '1d6', '1', '3', '6, 9 or 12', '15 (6 HD), 11 (9 HD), 9 (12 HD)', '1', '1d8 + 1 hp/HD', 'Absorb moisture', 'See below', 'Nil', "L (9'-12' tall)", 'Champion (15-16)', '2,000 (6 HD) / 5,000 (9 HD) / 8,000 (12 HD)'),
    ('Quasielemental (Negative), Vacuum', 78, 'Quasiplane of Vacuum', 'Uncommon', 'Band', 'Any', 'Anything', 'Low to high (5-14)', 'Nil', 'Neutral',
     '1d6', '-1', '36', '6, 9 or 12', '15 (6 HD), 11 (9 HD), 9 (12 HD)', '1', '1d4 + 1 hp/HD', 'Draw air', 'See below', 'Nil', "S (4' diameter)", 'Champion (15-16)', '2,000 (6 HD) / 5,000 (9 HD) / 8,000 (12 HD)'),
    ('Quasielemental (Positive), Lightning', 82, 'Quasiplane of Lightning', 'Common', 'Band', 'Any', 'Any energy', 'Low to high (5-14)', 'Nil', 'Neutral',
     '1d6', '2', 'Fl 18 (E) (plus special)', '6, 9 or 12', '15 (6 HD), 11 (9 HD), 9 (12 HD)', '1', '1d6 + 1hp/HD', 'Lightning globe', 'See below', 'Nil', "S (3' diameter)", 'Champion (15-16)', '2,000 (6 HD) / 5,000 (9 HD) / 8,000 (12 HD)'),
    ('Quasielemental (Positive), Mineral', 82, 'Quasiplane of Mineral', 'Common', 'Band', 'Any', 'Any stone', 'Low to high (5-14)', 'Nil', 'Neutral',
     '1d6', '0', '6', '6, 9 or 12', '15 (6 HD), 11 (9 HD), 9 (12 HD)', '1', '1d8 + 1 hp/HD', 'Merging', 'See below', 'Nil', "L (9'-12' high)", 'Champion (15-16)', '3,000 (6 HD) / 6,000 (9 HD) / 8,000 (12 HD)'),
    ('Quasielemental (Positive), Radiance', 82, 'Quasiplane of Radiance', 'Common', 'Band', 'Any', 'Darkness', 'Low to high (5-14)', 'Nil', 'Neutral',
     '1d6', '0', 'Fl 48 (E)', '6, 9 or 12', '15 (6 HD), 11 (9 HD), 9 (12 HD)', '1', '1d3 + 1 hp/HD', 'Beams, blinding', 'See below', 'Nil', "S (3' diameter)", 'Champion (15-16)', '3,000 (6 HD) / 6,000 (9 HD) / 9,000 (12 HD)'),
    ('Quasielemental (Positive), Steam', 82, 'Quasiplane of Steam', 'Common', 'Band', 'Any', 'Any gas', 'Low to high (5-14)', 'Nil', 'Neutral',
     '1d6', '2', 'Fl 12 (E)', '6, 9 or 12', '15 (6 HD), 11 (9 HD), 9 (12 HD)', '1', '1d6 + 1 hp/HD', 'None', 'See below', 'Nil', "G (60' wide)", 'Champion (15-16)', '2,000 (6 HD) / 5,000 (9 HD) / 8,000 (12 HD)'),
    ('Rast', 86, 'Quasiplane of Ash', 'Uncommon', 'Pack', 'Any', 'Carnivorous', 'Animal to semi (1-3)', 'Nil', 'Neutral',
     '1d6+1 (rarely, 1)', '5', 'Fl 18 (B)', '4+2', '17', '4 or 1', '1d4/1d4/1d4/1d4 or 1d8+3', 'Paralyzation, blood drain', 'Immune to fire and heat', 'Nil', "M (5' across)", 'Elite (13-14)', '975'),
    ('Ravid', 88, 'Any (Positive Energy Plane)', 'Very rare (common)', 'Solitary', 'Any', 'Special', 'Low (5-7)', 'Nil', 'Neutral',
     '1', '-4', 'Fl 24 (A)', '3', '17', '2', '1d4/1d6', 'Energy jolt, animation', 'Animation', '20%', "M (6' long)", 'Unsteady (5-7)', '1,400'),
    ('Ruvoka', 90, 'Inner Planes', 'Very rare', 'Solitary (tribal)', 'Any', 'Omnivorous', 'High (13-14)', 'See below', 'Neutral',
     '1', '6 or better', '12 (18 within element)', '3+', '17 or better', '1', 'By weapon (+2 to +6 for Str)', 'Spells', 'Spells', 'Nil', "M-L (7' to 12' tall)", 'Elite to fanatic (14-18)', '975 (3 HD) / 1,400 (4 HD) / 2,000 (5 HD) / 3,000 (6 HD) / 4,000 + 1,000/HD (7+ HD)'),
    ('Salamander, Lesser', 92, 'Plane of Fire', 'Uncommon', 'Tribe', 'Any', 'Omnivore', 'Average (8-10)', 'K,M', 'Neutral evil',
     '3d6', '8', '12', '2+2', '19', '1', 'By weapon', '+2 heat dmg', 'See below', 'Nil', "M (6' long)", 'Average (8-10)', '175'),
    ('Salamander, Noble', 92, 'Plane of Fire', 'Very rare', 'Solitary', 'Any', 'Omnivore', 'Genius (17-18)', 'G', 'Lawful evil',
     '1', '0', '18', '12', '9', '2', 'By weapon +4, 2d8+4', '+1d6 heat dmg', 'See below', '25%', "L (10' long)", 'Fanatic (17-18)', '10,000'),
    ('Scile', 94, 'Quasiplane of Radiance', 'Common', 'Cloud', 'Any', 'Color', 'Low to average (7-9)', 'Nil', 'Neutral',
     '10d10', '0', 'Fl 9 (A)', '1 hp', '20', 'Nil', 'Nil', 'Drain color', 'Struck only by +1 or better weapons, immunities', 'Nil', 'T (1/100" long)', 'Fanatic (17-18)', '35'),
    ('Shad', 96, 'Elemental Plane of Earth', 'Rare', 'Tribal', 'Any', 'Omnivorous', 'Average (9-10)', 'Q', 'Neutral',
     '2d8', '6', '12', '2+1', '19', '1', '1d3 or by weapon', 'None', 'Contortion, save bonus, immunities', 'Nil', "S-M (4'-5 1/2' tall)", 'Steady (11-12)', '175'),
    ('Shocker, Contented One', 98, 'Quasiplane of Lightning', 'Common', 'Varies', 'Any', 'Nil', 'Semi- (2-4)', 'Q', 'Chaotic neutral',
     '6d4', '10 or 0', '9', '1+2', '19', '1', '2d4', 'See below', 'See below', '20%', "M (6' tall)", 'Average (8-10)', '270'),
    ('Shocker, Sojourner', 98, 'Quasiplane of Lightning', 'Rare', 'Varies', 'Any', 'Nil', 'Avg (8-10)', 'Q', 'Chaotic neutral',
     '2d4', '10 or 0', '15', '5-10', '15 (5-6 HD), 13 (7-8 HD), 11 (9-10 HD)', '1', '3d4', 'See below', 'See below', '50%', "M (6' tall)", 'Elite (15-16)', '2,000 (5 HD) / 3,000 (6 HD) / 4,000 (7 HD) / 5,000 (8 HD) / 6,000 (9 HD) / 7,000 (10 HD)'),
    ('Sislan', 100, 'Elemental Plane of Air', 'Rare', 'Triumvirate', 'Any', 'Nil', 'Average to high (10-14)', 'Nil', 'Chaotic neutral',
     '1d3', '2', 'Fl 24 (A)', '6+3', '15 (12 vs. nonflyers)', '3', '1d6/1d6/1d6', 'Stun, grasp', 'Struck only by +1 or better weapons, immunities', 'Nil', "L (12' tall)", 'Fanatic (17-18)', '4,000'),
    ('Suisseen', 102, 'Elemental Plane of Water', 'Common', 'None', 'Any', 'Omnivorous', 'Low (5-7)', 'Nil', 'Neutral (neutral evil)',
     '1', '3 (membrane), 0 (water)', 'Sw 15', '8', '13', '1', '1d4+1 or 2d8+2', 'Drowning', 'Immune to fire', 'Nil', "L (10' long)", 'Elite (13-14)', '2,000'),
    ('Terithran', 104, 'Ethereal Plane', 'Rare', 'Solitary', 'Any', 'Carnivorous?', 'Low to average (7-9)', 'Nearly drained magical items', 'Neutral',
     '1', '6 (3 on the Prime)', '18 (15 on the Prime)', '5+1', '15', '2', '1d8+1/1d8+1', 'Spell-like powers', 'Spell-like powers', '50%', "S (4' tall)", 'Average (9-10)', '2,000'),
    ('Thoqqua', 106, 'Planes of Fire, Earth, Magma', 'Very rare', 'Pairs', 'Any', 'Stone', 'Low (5-7)', 'Nil', 'Neutral',
     '1d2', '2', '12, Br 3', '3 (but see below)', '17', '1', '2d6 or 4d8', 'Heat, charge', 'Melt weapons, gain hit points from heat/fire attacks', 'Nil', "M (4'-5' long)", 'Steady (11-12)', '650'),
    ('Trilloch', 108, 'Negative Energy Plane (any)', 'Very rare', 'Solitary', 'Any', 'Waning life force', 'Animal (1)', 'Nil', 'Neutral',
     '1', 'N/A', '12', 'N/A', 'N/A', 'N/A', 'N/A', 'Induce violence, aid attacks', 'Invisibility, immunities', 'Nil', "S-M (2'-6' diameter)", 'Unsteady (5-7)', '650'),
    ('Tsnng', 110, 'Quasiplane of Mineral', 'Rare', 'Cabal', 'Any', 'Omnivorous', 'Genius to supra-genius (18-20)', 'Q x3,T,U', 'Neutral',
     '2d4', '2', '9', '6', '15', '1', '1d4 or by weapon + gem bonus', 'Spells, impale', 'None', 'Nil', "M (5'-6' tall)", 'Steady (11-12)', '2,000'),
    ('Ungulosin', 112, 'Elemental Plane of Water', 'Very rare', 'Solitary', 'Any', 'N/A', 'Semi (2-3)', 'Nil', 'Neutral',
     '1', '6', 'Sw 18', '5', '15', '1', '1d4+4', 'Poison', 'See below', 'Nil', "H (15'+ long)", 'Steady (12)', '1,400'),
    ('Vacuous', 114, 'Quasiplane of Vacuum', 'Rare', 'Pack', 'Any (nocturnal, if appropriate)', 'Carnivorous', 'Exceptional (15-16)', 'Nil', 'Lawful evil',
     '1d6', '4', '9, Fl 18 (B)', '4+2', '17', '2', '1d6/1d6', 'Suction, ingestion', 'Immune to sleep, hold, charm', 'Nil', "M (5' tall)", 'Elite (13-14)', '1,400'),
    ('Wavefire', 116, 'Quasiplane of Steam', 'Uncommon', 'Solitary', 'Any', 'Air', 'Average (8-9)', 'Nil', 'Neutral',
     '1d3', '1 (6 out of water)', 'Sw 48 (3 out of water)', '8', '13', '1', '3d6', 'Scalding', 'Struck only by +1 or better weapons, immunities', 'Nil', "L (12' tall)", 'Average (8)', '4,000'),
    ('Xag-ya/Xeg-yi', 118, 'Energy Planes', 'Uncommon', 'Solitary', 'Any', 'Energy', 'High (13-14)', 'Nil', 'Neutral',
     '1', '0', 'Fl 6 (B)', '5-8', '15 (5-6 HD), 13 (7-8 HD)', '1', '1d6+6', 'Energy blast or drain', 'See below', '15%', "M (4' diameter)", 'Steady (11)', '5,000 (5 HD) / 6,000 (6 HD) / 7,000 (7 HD) / 8,000 (8 HD)'),
    ('Xill', 120, 'Ethereal Plane (Inner Planes)', 'Uncommon', 'Clan', 'Any', 'Omnivorous', 'Very (11-12)', 'C', 'Lawful evil',
     '1d6', '0', '15', '5', '15 (13 with missiles)', '4', '1d4/1d4/1d4/1d4 or by weapon', 'Paralyzation, clerical spells', 'See below', '70%', "M (4'-5' tall)", 'Elite (15)', '3,000'),
]


@dataclass
class Ad2eMonster:
    name: str
    book: str
    system: str
    page: Optional[int]
    climate_terrain: Optional[str] = None
    frequency: Optional[str] = None
    organization: Optional[str] = None
    activity_cycle: Optional[str] = None
    diet: Optional[str] = None
    intelligence: Optional[str] = None
    treasure: Optional[str] = None
    alignment: Optional[str] = None
    no_appearing: Optional[str] = None
    armor_class: Optional[str] = None
    movement: Optional[str] = None
    hit_dice: Optional[str] = None
    thac0: Optional[str] = None
    no_of_attacks: Optional[str] = None
    damage_attack: Optional[str] = None
    special_attacks: Optional[str] = None
    special_defenses: Optional[str] = None
    magic_resistance: Optional[str] = None
    size: Optional[str] = None
    morale: Optional[str] = None
    xp_value: Optional[str] = None
    citation: str = CITATION


def build() -> List[Ad2eMonster]:
    out: List[Ad2eMonster] = []
    for rows, book, cite in ((_ROWS, BOOK_II, CITATION_II),
                             (_ROWS_APP3, BOOK_III, CITATION_III)):
        for row in rows:
            d = dict(zip(COLS, row))
            d["book"] = book
            d["system"] = SYSTEM
            d["citation"] = cite
            out.append(Ad2eMonster(**d))
    return out


def write_index() -> int:
    monsters = build()
    n2 = sum(1 for m in monsters if m.book == BOOK_II)
    n3 = sum(1 for m in monsters if m.book == BOOK_III)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    md: List[str] = [
        "# AD&D 2e MONSTER INDEX — The New Path",
        "",
        "**Generated by `scripts/ad2e_monster_harvest.py`. Do not hand-edit; rerun",
        "the harvest.** **AD&D 2nd Edition** monsters — a DIFFERENT edition from the",
        "3.5e `creature_index` and the 5e `dnd5e_creature_index`. Every row is",
        "stamped `system: AD&D 2e` and is SOURCE MATERIAL for the system-translator",
        "skill. **Vision-transcribed from the Planescape Monstrous Compendium",
        "Appendix II AND Appendix III PDF page images** (the OCR text layer scrambles",
        "/ does not exist for the stat columns) — still book RAW, read off the page.",
        "Each row carries its own `book` (the `App` column below). AD&D 2e uses",
        "DESCENDING Armor Class and THAC0.",
        "",
        f"*{len(monsters)} monsters — {n2} from MC Appendix II, {n3} from MC "
        f"Appendix III.*",
        "",
        "| Monster | AC | HD | THAC0 | No. App. | Move | Alignment | Size | XP | Page | App |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for m in monsters:
        app = "III" if m.book == BOOK_III else "II"
        md.append(f"| {m.name} | {m.armor_class} | {m.hit_dice} | {m.thac0} | "
                  f"{m.no_appearing} | {m.movement} | {m.alignment} | {m.size} | "
                  f"{m.xp_value} | {m.page} | {app} |")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/ad2e_monster_harvest.py",
                    "system": SYSTEM,
                    "books": [
                        {"book": BOOK_II, "citation": CITATION_II,
                         "monsters": n2},
                        {"book": BOOK_III, "citation": CITATION_III,
                         "monsters": n3},
                    ],
                    "note": ("Vision-transcribed from the PDF page images; the OCR "
                             "text layer scrambles / does not exist for the stat "
                             "columns. Book RAW. Every monster carries its own "
                             "'book' and 'citation'."),
                    "total_monsters": len(monsters),
                    "monsters": [asdict(m) for m in monsters]}, indent=1),
        encoding="utf-8")
    return len(monsters)


def selftest() -> int:
    failures: List[str] = []
    monsters = build()
    n2 = sum(1 for m in monsters if m.book == BOOK_II)
    n3 = sum(1 for m in monsters if m.book == BOOK_III)
    # per-book counts (App II preserved exactly at 25; App III adds 71)
    if n2 != 25:
        failures.append(f"expected 25 MC App II monsters, got {n2}")
    if n3 != 71:
        failures.append(f"expected 71 MC App III monsters, got {n3}")
    if len(monsters) != 96:
        failures.append(f"expected 96 total monsters, got {len(monsters)}")
    names = {m.name for m in monsters}
    # App II probes (unchanged)
    for probe in ("Aasimar", "Guardinal, Ursinal", "Rilmani, Aurumach",
                  "Tanar'ri, Alkilith (True)", "Wraithworm"):
        if probe not in names:
            failures.append(f"missing App II monster '{probe}'")
    # App III probes — a spread across the alphabet, including group sub-types
    for probe in ("Animental", "Archomental (Evil), Imix",
                  "Archomental (Good), Zaaman Rul", "Belker",
                  "Homunculus, Elemental (Skin)", "Paraelemental, Ice",
                  "Quasielemental (Positive), Radiance", "Psurlon, Giant",
                  "Ruvoka", "Salamander, Noble", "Xag-ya/Xeg-yi", "Xill"):
        if probe not in names:
            failures.append(f"missing App III monster '{probe}'")
    if len({m.name.lower() for m in monsters}) != len(monsters):
        failures.append("duplicate monster names")
    # every monster must carry the core AD&D 2e stat fields + a book label
    for m in monsters:
        for fld in ("armor_class", "hit_dice", "thac0", "alignment", "xp_value"):
            if not getattr(m, fld):
                failures.append(f"{m.name}: missing {fld}")
                break
        if m.system != "AD&D 2e":
            failures.append(f"{m.name}: system not 'AD&D 2e'")
        if m.book not in (BOOK_II, BOOK_III):
            failures.append(f"{m.name}: unexpected book {m.book!r}")
        if m.citation != (CITATION_III if m.book == BOOK_III else CITATION_II):
            failures.append(f"{m.name}: citation does not match its book")
    aas = next((m for m in monsters if m.name == "Aasimar"), None)
    if aas and (aas.armor_class, aas.hit_dice, aas.thac0, aas.xp_value) != ("3 (10)", "3+3", "17", "420"):
        failures.append(f"Aasimar stats wrong: {(aas.armor_class, aas.hit_dice, aas.thac0, aas.xp_value)}")
    if aas and aas.book != BOOK_II:
        failures.append("Aasimar not labelled App II")
    # App III exact-stat spot check + book label
    bel = next((m for m in monsters if m.name == "Belker"), None)
    if bel and (bel.armor_class, bel.hit_dice, bel.thac0, bel.xp_value) != ("-2", "7+3", "13", "5,000"):
        failures.append(f"Belker stats wrong: {(bel.armor_class, bel.hit_dice, bel.thac0, bel.xp_value)}")
    if bel and bel.book != BOOK_III:
        failures.append("Belker not labelled App III")
    for f in failures:
        print(f"SELFTEST FAIL: {f}")
    print(f"selftest: {n2} App II + {n3} App III = {len(monsters)} monsters — "
          + ("PASS" if not failures else f"{len(failures)} failure(s)"))
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--search", metavar="TEXT")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if args.search:
        q = args.search.lower()
        hits = [m for m in build() if q in m.name.lower()]
        for m in hits:
            app = "III" if m.book == BOOK_III else "II"
            print(f"  {m.name} — AC {m.armor_class}, HD {m.hit_dice}, THAC0 {m.thac0}, "
                  f"{m.alignment}, XP {m.xp_value} [App {app} p.{m.page}]")
        print(f"{len(hits)} match(es).")
        return 0 if hits else 1

    n = write_index()
    print(f"{n} AD&D 2e monsters (Planescape MC Appendix II + III, "
          f"vision-transcribed). (system: {SYSTEM})")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
