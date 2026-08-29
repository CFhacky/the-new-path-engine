#!/usr/bin/env python3
"""epic_item_harvest.py — the D&D 3.5 epic magic items (Epic Level Handbook, Ch. 4).

WHY THIS ONE IS DIFFERENT (same reason as epic_feat_harvest.py /
epic_spell_harvest.py). The Epic Level Handbook's text layer is corrupted OCR
(dropped leading characters, Cyrillic bleed: "Eye of Graumsh", "Momento Mori"),
so parsing it yields garbage names and prices. Instead, the ELH PDF's PAGE
IMAGES are perfectly legible, so Chapter 4 "Epic Magic Items" (pp.124-147) was
transcribed BY VISION from those rendered pages. This is still book RAW — read
directly off the page, never invented — and every entry is cited to its page.

Two bodies of mechanics are captured, exactly as printed:

  (A) EPIC ITEM SPECIAL ABILITIES — the four random-generation tables of epic
      weapon / armor / shield special abilities, each a (name, market-price
      modifier, one-line effect):
        * Table 4-6  Armor Special Abilities          (p.127) — 14
        * Table 4-7  Shield Special Abilities         (p.127) — 16
        * Table 4-15 Melee Weapon Special Abilities   (p.132) — 12
        * Table 4-16 Ranged Weapon Special Abilities  (p.133) — 13
      The market-price modifier is the bonus-equivalent ("+6 bonus") exactly as
      the tables print it. Effects are the one-line summary of each ability's
      full description on the same spread.

  (B) SPECIFIC EPIC MAGIC ITEMS — named items with a market price, from the
      compact random-generation tables (cross-checked against, and where the
      table was faint filled from, the full item descriptions):
        * Table 4-8  Specific Epic Magic Armor and Shields (p.128-129) — 7
        * Table 4-17 Specific Weapons                      (p.133-135) — 12
        * Table 4-18 Epic Rings                            (p.135) — 25
        * Table 4-19 Epic Rods                             (p.137-140) — 25
        * Table 4-24 Epic Staffs                           (p.142-144) — 13
        * Table 4-25 Epic Wondrous Items                   (p.144-146) — 16
      Ability-boost wondrous items (belt of epic strength, cloak of epic
      resistance, etc.) are recorded once each with the price RANGE the
      description prints across their bonus tiers.

    reference/epic_item_index.json — every ability + item: name, kind,
                                     slot_or_type, market_price, effect, page,
                                     and an exact full-description source span
    reference/epic_item_index.md   — the same, for human eyes

Description bodies are recovered from rendered ELH pp.126-146 with reproducible
4× two-column OCR. Bodies remain raw OCR; only the 103 book-verified headings
are restored. Variant rows share the single common description the book prints.

TRANSCRIPTION NOTES (book RAW; where the image was not clean it is noted here,
never guessed):
  * Armor of the Celestial Battalion prints Market Price 656,300 gp; the middle
    digit is faint but the printed XP cost (16,560) confirms 656,300 over 616,300.
  * The Rod of the Wyrm color variants' prices are garbled in Table 4-19 (the
    leading "1," drops on alternating rows); they are taken instead from the
    item's own description (ELH p.140), which prints them cleanly by color pair.
  * NOT harvested: the epic scroll generation tables (4-20..4-23, generic, not
    named items) and the named ARTIFACTS on pp.150-154 (Eye of Gruumsh, Axe of
    the Dwarvish Lord, etc.), which as artifacts carry no market price.

PROVENANCE
    Epic Level Handbook (WotC, 3.5e), Chapter 4 "Epic Magic Items", pp.124-147.
    Rendered from Epic Level Handbook.pdf via PyMuPDF at ~2.8x (and cropped
    higher for the tables) and read by vision because the OCR text layer is
    unusable.
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
OUT_JSON = REPO / "reference" / "epic_item_index.json"
OUT_MD = REPO / "reference" / "epic_item_index.md"
CORPUS = Path(r"I:\Sourcebooks\_text")
SOURCE_REL = Path(r"D&D 3.5e\DM Toolkits\Epic Level Handbook.epic-items.ocr-columns.md")
SOURCE = CORPUS / SOURCE_REL
PDF_SOURCE = Path(r"I:\Sourcebooks\D&D 3.5e\DM Toolkits\Epic Level Handbook.pdf")
TESSERACT = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
BOOK = "Epic Level Handbook"
CITATION = (
    "Epic Level Handbook (WotC, 3.5e), Chapter 4 'Epic Magic Items', pp.124-147 "
    "— epic weapon/armor/shield special-ability tables (4-6 p.127, 4-7 p.127, "
    "4-15 p.132, 4-16 p.133) and specific-item tables (4-8 pp.128-129, 4-17 "
    "pp.133-135, 4-18 p.135, 4-19 pp.137-140, 4-24 pp.142-144, 4-25 pp.144-146), "
    "cross-checked against the full item descriptions. Vision-transcribed from "
    "the PDF page images because the OCR text layer is corrupt."
)
PAGES = "124-147"

# ---------------------------------------------------------------------------
# (A) SPECIAL ABILITIES — the random-generation tables.
#     (name, slot_or_type, market_price_modifier, effect, page)
# ---------------------------------------------------------------------------
_ARMOR_ABILITIES = [  # Table 4-6, p.127
    ("Great invulnerability (10/+2)", "+4 bonus", "Grants the wearer damage reduction 10/+2"),
    ("Great invulnerability (15/+3)", "+5 bonus", "Grants the wearer damage reduction 15/+3"),
    ("Negating", "+5 bonus", "When the wearer is struck by a magic weapon, the armor casts greater dispel magic on that weapon"),
    ("Acid warding", "+6 bonus", "Absorbs the first 50 points of acid damage each round the wearer would take"),
    ("Cold warding", "+6 bonus", "Absorbs the first 50 points of cold damage each round the wearer would take"),
    ("Fire warding", "+6 bonus", "Absorbs the first 50 points of fire damage each round the wearer would take"),
    ("Great invulnerability (20/+4)", "+6 bonus", "Grants the wearer damage reduction 20/+4"),
    ("Great spell resistance (SR 21)", "+6 bonus", "Grants the wearer spell resistance 21"),
    ("Lightning warding", "+6 bonus", "Absorbs the first 50 points of electricity damage each round the wearer would take"),
    ("Sonic warding", "+6 bonus", "Absorbs the first 50 points of sonic damage each round the wearer would take"),
    ("Great invulnerability (25/+5)", "+7 bonus", "Grants the wearer damage reduction 25/+5"),
    ("Great spell resistance (SR 23)", "+7 bonus", "Grants the wearer spell resistance 23"),
    ("Great spell resistance (SR 25)", "+8 bonus", "Grants the wearer spell resistance 25"),
    ("Great spell resistance (SR 27)", "+9 bonus", "Grants the wearer spell resistance 27"),
]

_SHIELD_ABILITIES = [  # Table 4-7, p.127
    ("Great invulnerability (10/+2)", "+4 bonus", "Grants the bearer damage reduction 10/+2"),
    ("Great invulnerability (15/+3)", "+5 bonus", "Grants the bearer damage reduction 15/+3"),
    ("Acid warding", "+6 bonus", "Absorbs the first 50 points of acid damage each round the bearer would take"),
    ("Cold warding", "+6 bonus", "Absorbs the first 50 points of cold damage each round the bearer would take"),
    ("Fire warding", "+6 bonus", "Absorbs the first 50 points of fire damage each round the bearer would take"),
    ("Great invulnerability (20/+4)", "+6 bonus", "Grants the bearer damage reduction 20/+4"),
    ("Great spell resistance (SR 21)", "+6 bonus", "Grants the bearer spell resistance 21"),
    ("Infinite arrow deflection", "+6 bonus", "Functions like a shield of arrow deflection but can deflect any number of projectiles or thrown weapons each round"),
    ("Lightning warding", "+6 bonus", "Absorbs the first 50 points of electricity damage each round the bearer would take"),
    ("Sonic warding", "+6 bonus", "Absorbs the first 50 points of sonic damage each round the bearer would take"),
    ("Great invulnerability (25/+5)", "+7 bonus", "Grants the bearer damage reduction 25/+5"),
    ("Great spell resistance (SR 23)", "+7 bonus", "Grants the bearer spell resistance 23"),
    ("Exceptional arrow deflection", "+8 bonus", "Functions like a shield of arrow deflection but deflects any type of ranged attack, including ranged touch spells (Reflex DC 20)"),
    ("Great spell resistance (SR 25)", "+8 bonus", "Grants the bearer spell resistance 25"),
    ("Great spell resistance (SR 27)", "+9 bonus", "Grants the bearer spell resistance 27"),
    ("Great reflection", "+10 bonus", "Mirrorlike shield reflects any spell targeting the bearer back at the caster (as spell turning)"),
]

_MELEE_ABILITIES = [  # Table 4-15, p.132
    ("Acidic blast", "+6 bonus", "On a hit deals +3d6 acid damage (more on a critical)"),
    ("Fiery blast", "+6 bonus", "On a hit deals +3d6 fire damage (more on a critical)"),
    ("Icy blast", "+6 bonus", "On a hit deals +3d6 cold damage (more on a critical)"),
    ("Lightning blast", "+6 bonus", "On a hit deals +3d6 electricity damage (more on a critical)"),
    ("Mighty disruption", "+6 bonus", "Like a weapon of disruption; any undead struck must make a Fortitude save (DC 21) or be destroyed; must be a bludgeoning weapon"),
    ("Sonic blast", "+6 bonus", "On a hit deals +3d6 sonic damage (more on a critical)"),
    ("Dread", "+7 bonus", "Against its designated foe the enhancement bonus is +4 better and it deals +4d6 bonus damage; a successful critical forces a Fortitude save (DC 27) or the foe is destroyed"),
    ("Chaotic power", "+8 bonus", "Chaotically aligned; strikes a lawful target for +3d6 chaotic damage and one negative level (more on a critical)"),
    ("Everdancing", "+8 bonus", "Like a dancing weapon but can be loosed as a free action and fights as long as desired"),
    ("Holy power", "+8 bonus", "Good aligned; strikes an evil target for +3d6 holy (good) damage and one negative level (more on a critical)"),
    ("Lawful power", "+8 bonus", "Lawfully aligned; strikes a chaotic target for +3d6 lawful damage and one negative level (more on a critical)"),
    ("Unholy power", "+8 bonus", "Evilly aligned; strikes a good target for +3d6 unholy (evil) damage and one negative level (more on a critical)"),
]

_RANGED_ABILITIES = [  # Table 4-16, p.133
    ("Acidic blast", "+6 bonus", "Bestows +3d6 acid damage (more on a critical) upon the weapon's ammunition"),
    ("Distant shot", "+6 bonus", "Can be used against any target within line of sight with no range penalty"),
    ("Fiery blast", "+6 bonus", "Bestows +3d6 fire damage (more on a critical) upon the weapon's ammunition"),
    ("Icy blast", "+6 bonus", "Bestows +3d6 cold damage (more on a critical) upon the weapon's ammunition"),
    ("Lightning blast", "+6 bonus", "Bestows +3d6 electricity damage (more on a critical) upon the weapon's ammunition"),
    ("Sonic blast", "+6 bonus", "Bestows +3d6 sonic damage (more on a critical) upon the weapon's ammunition"),
    ("Triple-throw", "+6 bonus", "A thrown weapon creates two duplicates when thrown; all three attack separately, then the duplicates vanish"),
    ("Unerring accuracy", "+6 bonus", "Negates any cover or concealment bonus (short of total) of its target"),
    ("Dread", "+7 bonus", "Against its designated foe the enhancement bonus is +4 better and it deals +4d6 bonus damage; a successful critical forces a Fortitude save (DC 27) or the foe is destroyed"),
    ("Chaotic power", "+8 bonus", "Chaotically aligned; deals +3d6 chaotic damage and one negative level to a lawful target (more on a critical)"),
    ("Holy power", "+8 bonus", "Good aligned; deals +3d6 holy (good) damage and one negative level to an evil target (more on a critical)"),
    ("Lawful power", "+8 bonus", "Lawfully aligned; deals +3d6 lawful damage and one negative level to a chaotic target (more on a critical)"),
    ("Unholy power", "+8 bonus", "Evilly aligned; deals +3d6 unholy (evil) damage and one negative level to a good target (more on a critical)"),
]

# ---------------------------------------------------------------------------
# (B) SPECIFIC ITEMS.  (name, slot_or_type, market_price, effect, page)
# ---------------------------------------------------------------------------
_SPECIFIC_ARMOR = [  # Table 4-8 + descriptions, pp.128-129
    ("Shapeshifter's armor", "armor", "400,165 gp", "+6 hide armor that grants its full armor bonus regardless of any form the wearer takes (polymorph self, shapechange, wild shape, and the like)", 129),
    ("Warlord's breastplate", "armor", "416,200 gp", "+6 mithral breastplate (light armor); grants +4 enhancement to Charisma and lets the wearer attract and lead followers as the Leadership feat (no cohort)", 129),
    ("Dragonskin armor", "armor", "564,550 gp", "+5 full plate of great-wyrm hide; sprouts dragon wings for fly 90 ft. (clumsy) 4 hours/day, grants immunity to one energy type by dragon color, and +4 on Intimidate vs dragons (-4 Diplomacy vs dragons)", 129),
    ("Armor of the celestial battalion", "armor", "656,300 gp", "Bright silver full plate so fine it can be worn under clothing; max Dex +10, no armor check penalty, counts as light armor, lets the wearer fly (as fly) and surrounds him with magic circle against evil", 128),
    ("Armor of the abyssal horde", "armor", "768,260 gp", "Crimson-and-black full plate with a demon-shaped helm; the armor bestows negative levels on any nonevil creature wearing it (as long as worn)", 128),
    ("Antimagic armor", "armor", "871,500 gp", "Adamantine armor that grants a bonus on dispel checks made against the wearer", 128),
    ("Bulwark of the great dragon", "shield", "1,612,970 gp", "+6 large shield of great-wyrm scales; 3/day belch a breath weapon of the matching dragon type, and grants the bearer energy resistance 50 to that type", 129),
]

_SPECIFIC_WEAPONS = [  # Table 4-17 + descriptions, pp.133-135
    ("Stormbrand", "weapon", "235,350 gp", "+4 thundering shocking burst greatsword; lets the wielder fly at will and move normally in the strongest winds, and grants electricity resistance 30 and sonic resistance 30 when drawn", 135),
    ("Quarterstaff of alacrity", "weapon", "462,600 gp", "+5 quarterstaff of speed with equal power on both ends (an extra attack with each end each round); grants +5 resistance on Reflex saves and Deflect Arrows / Infinite Deflection", 134),
    ("Souldrinker", "weapon", "478,335 gp", "+5 bastard sword that bestows 2d4 negative levels whenever it deals damage (as energy drain); each negative level grants the wielder 5 temporary hit points", 134),
    ("Backstabber", "weapon", "770,310 gp", "+2 short sword that adds +2d6 to the wielder's sneak attack damage (only if the wielder already has sneak attack)", 133),
    ("Mace of ruin", "weapon", "1,000,312 gp", "+7 heavy mace that ignores the hardness or damage reduction of anything it strikes and can score critical hits against objects and constructs", 134),
    ("Grimsoul", "weapon", "856,500 gp", "+6 keen longsword that, instead of extra critical damage, imprisons the struck victim in a pommel gem as binding heightened to 16th level (DC 30)", 134),
    ("Elven greatbow", "weapon", "2,900,400 gp", "For an elf, a +5 mighty composite longbow of unerring accuracy whose pull matches the wielder's Strength and whose arrows are keen; a mere +2 composite longbow for a nonelf", 134),
    ("Finaldeath", "weapon", "3,580,308 gp", "+5 undead dread ghost touch morningstar; grants the wielder immunity to energy drain, and the Positive Energy Aura feat if able to turn undead", 134),
    ("Chaosbringer", "weapon", "4,025,350 gp", "+6 greataxe of chaotic power; lets the wielder rage 1/day (or +1/day, and gain Incite Rage if he has greater rage)", 134),
    ("Holy devastator", "weapon", "4,620,315 gp", "A +3 holy longsword for anyone; for a paladin, a +7 longsword of holy power granting +5 sacred on saves vs evil and doubling paladin level to smite-evil damage", 134),
    ("Unholy despoiler", "weapon", "4,620,315 gp", "A +3 unholy longsword for anyone; for a blackguard, a +7 longsword of unholy power granting +5 profane on saves vs good and doubling blackguard level to smite-good damage", 135),
    ("Everwhirling chain", "weapon", "5,220,325 gp", "+4 defending everdancing spiked chain of speed; the wielder can make any number of attacks of opportunity per round (as Improved Combat Reflexes)", 134),
]

_RINGS = [  # Table 4-18, p.135
    ("Universal elemental resistance, major", "216,000 gp", "Provides major resistance to every energy type", 135),
    ("Elemental immunity (acid)", "240,000 gp", "Adamantine band granting immunity to acid damage", 135),
    ("Elemental immunity (cold)", "240,000 gp", "Adamantine band granting immunity to cold damage", 135),
    ("Elemental immunity (electricity)", "240,000 gp", "Adamantine band granting immunity to electricity damage", 135),
    ("Elemental immunity (fire)", "240,000 gp", "Adamantine band granting immunity to fire damage", 135),
    ("Elemental immunity (sonic)", "240,000 gp", "Adamantine band granting immunity to sonic damage", 135),
    ("Adamant law", "250,000 gp", "Sheathes the wearer in a shield of law effect; bestows a negative level on any chaotic creature that dons it", 135),
    ("Chaotic fury", "250,000 gp", "Sheathes the wearer in a cloak of chaos effect; bestows a negative level on any lawful creature that dons it", 135),
    ("Epic wizardry (V)", "250,000 gp", "Grants two extra spell slots (as a ring of wizardry) for 5th-level spells", 135),
    ("Ineffable evil", "250,000 gp", "Evil-aligned protective ring", 135),
    ("Virtuous good", "250,000 gp", "Good-aligned protective ring", 135),
    ("Rapid healing", "300,000 gp", "Greatly speeds the wearer's natural healing", 135),
    ("Sequestering", "300,000 gp", "Conceals the wearer from detection", 135),
    ("Epic wizardry (VI)", "360,000 gp", "Grants two extra spell slots for 6th-level spells", 135),
    ("Ironskin", "400,000 gp", "Hardens the wearer's flesh, granting damage reduction", 135),
    ("Epic wizardry (VII)", "490,000 gp", "Grants two extra spell slots for 7th-level spells", 135),
    ("Weaponbreaking", "600,000 gp", "Any weapon that strikes the wearer must succeed on a Fortitude save or shatter", 135),
    ("Epic wizardry (VIII)", "640,000 gp", "Grants two extra spell slots for 8th-level spells", 135),
    ("Epic protection +6", "720,000 gp", "+6 deflection bonus to AC (and equal resistance bonus on saves)", 135),
    ("Epic wizardry (IX)", "810,000 gp", "Grants two extra spell slots for 9th-level spells", 135),
    ("Epic protection +7", "980,000 gp", "+7 deflection bonus to AC (and equal resistance bonus on saves)", 135),
    ("Epic protection +8", "1,280,000 gp", "+8 deflection bonus to AC (and equal resistance bonus on saves)", 135),
    ("Epic protection +9", "1,620,000 gp", "+9 deflection bonus to AC (and equal resistance bonus on saves)", 135),
    ("Epic protection +10", "2,000,000 gp", "+10 deflection bonus to AC (and equal resistance bonus on saves)", 135),
    ("Universal elemental immunity", "2,160,000 gp", "Grants immunity to every energy type", 135),
]

_RODS = [  # Table 4-19 (pp.137) + descriptions (pp.137-140)
    ("Epic spellcaster", "245,000 gp", "Adamantine rod granting a +10 insight bonus on Spellcraft checks to cast epic spells", 138),
    ("Nightmares", "284,000 gp", "Ebony skull-topped rod; anyone within 20 ft. feels unease (Will DC 17 or nightmare on next sleep); the wielder can wail 20 creatures within 30 ft. with wail of the banshee (DC 23)", 139),
    ("Epic splendor", "297,000 gp", "+8 enhancement to Charisma; 3/day create fine clothing, and 1/week a palatial mansion", 138),
    ("The path", "306,870 gp", "+30 on Wilderness Lore for tracking / Intuit Direction; telescoping true-seeing view, plus map, passage, bridge and pass without trace powers", 139),
    ("Epic cancellation", "330,000 gp", "Drains all magical properties from a touched item (including epic magic items, not artifacts); the item gets a Will save", 137),
    ("Epic negation", "446,000 gp", "3/day negates the function of a spell, spell-like ability, or magic item (including epic, not artifacts) with a ranged touch ray", 138),
    ("Besiegement", "447,745 gp", "Becomes a +6 weapon on a charge; 2/day a battering ram, plus a siege-engine power that conjures catapults and siege towers", 137),
    ("Fortification", "465,665 gp", "+3 light mace for building and defending fortifications; improves cover, 3/day create food and water for 24, and creates walls, doors and siege engines", 139),
    ("Epic rulership", "575,000 gp", "Royal scepter that commands the obedience of creatures within 360 ft. totaling 900 HD, for up to 1,500 total minutes", 138),
    ("Invulnerability", "600,000 gp", "Adamantine rod granting the holder natural armor, a resistance bonus on saves, damage reduction 50/+3, immunity to critical hits, and spell resistance 32", 139),
    ("Paradise", "610,000 gp", "Creates a nondimensional refuge (as a rod of security) for up to 999 creatures for up to 1,000 days, with natural healing at five times the normal rate", 139),
    ("Restless death", "625,000 gp", "The holder rebukes or commands undead as if four levels higher, and can command animate dead / slay living powers", 140),
    ("Excellent magic", "650,000 gp", "1/day supplies up to 2,000 XP for a spell's XP cost, or can be drained to pay an epic spell's XP development cost", 138),
    ("Epic absorption", "1,500,000 gp", "As a rod of absorption but draws single-target ray spells and spell-like abilities into itself, storing up to 150 spell levels to release as spells", 137),
    ("Epic might", "4,293,432 gp", "As a rod of lordly might but adamantine and far more powerful: usable as several weapon forms with six buttons and many spell-like functions", 138),
    # Rod of the Wyrm — 10 dragon-color variants; prices from the description (p.140).
    ("Rod of the wyrm (white)", "1,458,200 gp", "+5 quarterstaff that, on command, grows into a wyrm-age dragon of the matching color under the wielder's command (same-alignment wielder only)", 140),
    ("Rod of the wyrm (brass)", "1,458,200 gp", "+5 quarterstaff that, on command, grows into a wyrm-age dragon of the matching color under the wielder's command (same-alignment wielder only)", 140),
    ("Rod of the wyrm (black)", "1,562,600 gp", "+5 quarterstaff that, on command, grows into a wyrm-age dragon of the matching color under the wielder's command (same-alignment wielder only)", 140),
    ("Rod of the wyrm (copper)", "1,562,600 gp", "+5 quarterstaff that, on command, grows into a wyrm-age dragon of the matching color under the wielder's command (same-alignment wielder only)", 140),
    ("Rod of the wyrm (bronze)", "1,670,600 gp", "+5 quarterstaff that, on command, grows into a wyrm-age dragon of the matching color under the wielder's command (same-alignment wielder only)", 140),
    ("Rod of the wyrm (green)", "1,670,600 gp", "+5 quarterstaff that, on command, grows into a wyrm-age dragon of the matching color under the wielder's command (same-alignment wielder only)", 140),
    ("Rod of the wyrm (blue)", "1,782,200 gp", "+5 quarterstaff that, on command, grows into a wyrm-age dragon of the matching color under the wielder's command (same-alignment wielder only)", 140),
    ("Rod of the wyrm (silver)", "1,782,200 gp", "+5 quarterstaff that, on command, grows into a wyrm-age dragon of the matching color under the wielder's command (same-alignment wielder only)", 140),
    ("Rod of the wyrm (gold)", "1,897,400 gp", "+5 quarterstaff that, on command, grows into a wyrm-age dragon of the matching color under the wielder's command (same-alignment wielder only)", 140),
    ("Rod of the wyrm (red)", "1,897,400 gp", "+5 quarterstaff that, on command, grows into a wyrm-age dragon of the matching color under the wielder's command (same-alignment wielder only)", 140),
]

_STAFFS = [  # Table 4-24 (p.142) + descriptions (pp.142-144)
    ("Staff of spheres", "228,375 gp", "Otiluke's freezing sphere, resilient sphere, and telekinetic sphere", 144),
    ("Staff of mighty force", "265,000 gp", "Quickened shield, forcecage, and Bigby's crushing hand", 143),
    ("Staff of walls", "275,625 gp", "Wall of iron, wall of stone, and wall of force", 144),
    ("Staff of winter", "292,500 gp", "Cone of cold, ice storm, Otiluke's freezing sphere, and wall of ice", 144),
    ("Staff of prism", "326,812 gp", "Prismatic sphere, prismatic spray, and prismatic wall", 144),
    ("Staff of rapid barrage", "417,750 gp", "Intensified quickened magic missile and heightened quickened fireball; either power usable as a free action once per round", 144),
    ("Staff of planar might", "460,000 gp", "+5 outsider bane quarterstaff; wielder is immune to planar alignment traits and can cast greater planar ally, greater planar binding, and gate", 143),
    ("Staff of domination", "464,400 gp", "Dominate monster, demand, mass charm, and heightened geas", 142),
    ("Staff of fiery power", "500,000 gp", "+5 flaming quarterstaff granting fire resistance 30; wall of fire, delayed blast fireball, meteor swarm, and elder-fire-elemental summon monster IX", 143),
    ("Staff of nature's fury", "500,000 gp", "+5 aberration bane quarterstaff; earthquake, fire storm, whirlwind, and summon nature's ally", 143),
    ("Staff of the hierophant", "501,167 gp", "Creeping doom, command plants, elemental swarm, and shambler", 143),
    ("Staff of the cosmos", "683,437 gp", "Jet-black star-field staff; chain lightning, meteor swarm, and sunburst", 142),
    ("Staff of necromancy", "1,505,312 gp", "Circle of death, create greater undead, finger of death, and soul bind (souls trapped in the staff)", 143),
]

_WONDROUS = [  # Table 4-25 (p.145) + descriptions (pp.144-146)
    ("Horseshoes of the peerless steed", "217,000 gp", "Adhere to any hooved creature; the rider gains +10 competence on Ride (treated as skilled), the mount gains the benefits of Trample/Run/Bull Rush/Spirited Charge and SR 32 vs enchantment, and its ground speed doubles", 146),
    ("Mantle of great stealth", "242,000 gp", "+30 on Hide and Move Silently; the wearer is blurred (one-half concealment, as blur) and gains nondetection", 146),
    ("Boots of swiftness", "256,000 gp", "+6 enhancement to Dexterity, doubled speed, evasion, +20 competence on Balance/Climb/Jump/Tumble, and 3/day haste", 144),
    ("Cabinet of feasting", "288,000 gp", "3/day produces a feast for up to 40 people (as heroes' feast)", 145),
    ("Mantle of epic spell resistance", "290,000 gp", "Grants the wearer spell resistance 40", 146),
    ("Gate key", "378,000 gp", "Attunes any bounded space to another previously visited bounded space (even on another plane), opening a linked interdimensional portal; up to 60 pairs", 145),
    ("Bracers of relentless might", "4,384,000 gp", "+12 enhancement to Strength and Constitution; the wearer is treated as two size categories larger for combat-related opposed checks (bull rush, grapple, trip)", 145),
    ("Cloak of epic resistance", "360,000-1,000,000 gp", "+6 to +10 resistance bonus on all saving throws (price scales with the bonus)", 145),
    ("Belt of epic strength", "640,000-1,440,000 gp", "+8 to +12 enhancement bonus to Strength (price scales with the bonus)", 145),
    ("Bracers of epic health", "640,000-1,440,000 gp", "+8 to +12 enhancement bonus to Constitution (price scales with the bonus)", 145),
    ("Cloak of epic charisma", "640,000-1,440,000 gp", "+8 to +12 enhancement bonus to Charisma (price scales with the bonus)", 145),
    ("Gloves of epic dexterity", "640,000-1,440,000 gp", "+8 to +12 enhancement bonus to Dexterity (price scales with the bonus)", 146),
    ("Headband of epic intellect", "640,000-1,440,000 gp", "+8 to +12 enhancement bonus to Intelligence (price scales with the bonus)", 146),
    ("Periapt of epic wisdom", "640,000-1,440,000 gp", "+8 to +12 enhancement bonus to Wisdom (price scales with the bonus)", 146),
    ("Amulet of epic natural armor", "720,000-2,000,000 gp", "+6 to +10 enhancement bonus to natural armor (price scales with the bonus)", 145),
    ("Bracers of epic armor", "1,210,000-2,250,000 gp", "+11 to +15 armor bonus to AC (price scales with the bonus)", 145),
]

_ABILITY_TABLES = [
    ("armor", 127, _ARMOR_ABILITIES),
    ("shield", 127, _SHIELD_ABILITIES),
    ("weapon (melee)", 132, _MELEE_ABILITIES),
    ("weapon (ranged)", 133, _RANGED_ABILITIES),
]

_SPECIFIC_TABLES = [
    _SPECIFIC_ARMOR,
    _SPECIFIC_WEAPONS,
    _RINGS,
    _RODS,
    _STAFFS,
    _WONDROUS,
]

SOURCE_PAGE_RE = re.compile(r"^## \[PDF pages? (\d+)(?:-(\d+))?\]$")
SOURCE_HEADING_RE = re.compile(r"^(.+?) \[EPIC ITEM DESCRIPTION\]$")

# Canonical description heading -> (book page, column, y). These anchors were
# verified against the rendered PDF. Variant table rows deliberately share the
# one description block the book prints for their common ability or item.
DESCRIPTION_ANCHORS: Dict[str, Tuple[int, int, float]] = {
    "Acid warding": (126, 0, 753.0),
    "Cold warding": (126, 0, 871.0),
    "Exceptional arrow deflection": (126, 1, 886.0),
    "Fire warding": (127, 0, 644.0),
    "Great invulnerability": (127, 0, 821.0),
    "Great reflection": (127, 1, 486.0),
    "Great spell resistance": (127, 1, 664.0),
    "Infinite arrow deflection": (127, 1, 826.0),
    "Lightning warding": (128, 0, 220.0),
    "Negating": (128, 0, 418.0),
    "Sonic warding": (128, 0, 679.0),
    "Antimagic armor": (128, 1, 149.0),
    "Armor of the abyssal horde": (128, 1, 296.0),
    "Armor of the celestial battalion": (128, 1, 709.0),
    "Bulwark of the great dragon": (129, 0, 74.0),
    "Dragonskin armor": (129, 0, 488.0),
    "Shapeshifter's armor": (129, 0, 871.0),
    "Warlord's breastplate": (129, 1, 136.0),
    "Acidic blast": (129, 1, 843.0),
    "Chaotic power": (130, 0, 667.0),
    "Distant shot": (130, 1, 682.0),
    "Dread": (130, 1, 759.0),
    "Everdancing": (131, 0, 489.0),
    "Fiery blast": (131, 0, 678.0),
    "Holy power": (131, 0, 857.0),
    "Icy blast": (132, 0, 627.0),
    "Lawful power": (132, 0, 816.0),
    "Lightning blast": (132, 1, 624.0),
    "Mighty disruption": (132, 1, 814.0),
    "Sonic blast": (133, 0, 427.0),
    "Triple-throw": (133, 0, 694.0),
    "Unerring accuracy": (133, 1, 269.0),
    "Unholy power": (133, 1, 357.0),
    "Backstabber": (133, 1, 861.0),
    "Chaosbringer": (134, 0, 93.0),
    "Elven greatbow": (134, 0, 267.0),
    "Everwhirling chain": (134, 0, 445.0),
    "Finaldeath": (134, 0, 633.0),
    "Grimsoul": (134, 0, 800.0),
    "Holy devastator": (134, 1, 194.0),
    "Mace of ruin": (134, 1, 415.0),
    "Quarterstaff of alacrity": (134, 1, 549.0),
    "Souldrinker": (134, 1, 727.0),
    "Stormbrand": (135, 0, 92.0),
    "Unholy despoiler": (135, 0, 264.0),
    "Adamant law": (135, 0, 561.0),
    "Chaotic fury": (135, 1, 460.0),
    "Elemental immunity": (135, 1, 622.0),
    "Epic protection": (136, 0, 93.0),
    "Epic wizardry": (136, 0, 224.0),
    "Ineffable evil": (136, 0, 592.0),
    "Ironskin": (136, 0, 755.0),
    "Rapid healing": (136, 1, 106.0),
    "Sequestering": (136, 1, 211.0),
    "Universal elemental immunity": (136, 1, 314.0),
    "Universal elemental resistance, major": (136, 1, 535.0),
    "Virtuous good": (136, 1, 668.0),
    "Weaponbreaking": (137, 0, 111.0),
    "Besiegement": (137, 0, 727.0),
    "Epic absorption": (137, 1, 212.0),
    "Epic cancellation": (137, 1, 390.0),
    "Epic might": (137, 1, 627.0),
    "Epic negation": (138, 0, 741.0),
    "Epic rulership": (138, 1, 125.0),
    "Epic spellcaster": (138, 1, 390.0),
    "Epic splendor": (138, 1, 476.0),
    "Excellent magic": (138, 1, 778.0),
    "Fortification": (139, 0, 113.0),
    "Invulnerability": (139, 0, 592.0),
    "Nightmares": (139, 0, 799.0),
    "Paradise": (139, 1, 154.0),
    "The path": (139, 1, 327.0),
    "Restless death": (139, 1, 864.0),
    "Rod of the wyrm": (140, 0, 267.0),
    "Staff of the cosmos": (142, 0, 902.0),
    "Staff of domination": (142, 1, 478.0),
    "Staff of fiery power": (142, 1, 712.0),
    "Staff of the hierophant": (143, 0, 403.0),
    "Staff of mighty force": (143, 0, 653.0),
    "Staff of nature's fury": (143, 0, 805.0),
    "Staff of necromancy": (143, 1, 195.0),
    "Staff of planar might": (143, 1, 506.0),
    "Staff of prism": (143, 1, 864.0),
    "Staff of rapid barrage": (144, 0, 192.0),
    "Staff of spheres": (144, 0, 414.0),
    "Staff of walls": (144, 0, 592.0),
    "Staff of winter": (144, 0, 784.0),
    "Amulet of epic natural armor": (144, 1, 252.0),
    "Belt of epic strength": (144, 1, 428.0),
    "Boots of swiftness": (144, 1, 578.0),
    "Bracers of epic armor": (144, 1, 800.0),
    "Bracers of epic health": (145, 0, 107.0),
    "Bracers of relentless might": (145, 0, 211.0),
    "Cabinet of feasting": (145, 0, 356.0),
    "Cloak of epic charisma": (145, 0, 504.0),
    "Cloak of epic resistance": (145, 0, 786.0),
    "Gate key": (145, 1, 697.0),
    "Gloves of epic dexterity": (146, 0, 161.0),
    "Headband of epic intellect": (146, 0, 336.0),
    "Horseshoes of the peerless steed": (146, 0, 558.0),
    "Mantle of epic spell resistance": (146, 0, 797.0),
    "Mantle of great stealth": (146, 0, 886.0),
    "Periapt of epic wisdom": (146, 1, 180.0),
}

# Stop before unrelated generation tables or boxed non-index material.
DESCRIPTION_ENDS: Dict[str, Tuple[int, int, float]] = {
    "Sonic warding": (128, 0, 795.0),
    "Warlord's breastplate": (129, 1, 345.0),
    "Unholy power": (133, 1, 755.0),
    "Unholy despoiler": (135, 0, 450.0),
    "Adamant law": (135, 0, 720.0),
    "Elemental immunity": (135, 1, 705.0),
    "Ironskin": (136, 0, 815.0),
    "Weaponbreaking": (137, 0, 215.0),
    "Rod of the wyrm": (140, 0, 760.0),
}


def _description_key(name: str) -> str:
    name = re.sub(r"\s*\([^)]*\)\s*$", "", name)
    return re.sub(r"\s*\+\d+\s*$", "", name).strip()


def _all_description_keys() -> List[str]:
    names = [row[0] for _, _, rows in _ABILITY_TABLES for row in rows]
    names.extend(row[0] for table in _SPECIFIC_TABLES for row in table)
    return sorted({_description_key(name) for name in names})


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
    for book_page in range(126, 147):
        page = doc[book_page - 1]
        for column, (x0, x1) in enumerate(((8, 350), (350, 692))):
            clip = fitz.Rect(x0, 55, x1, 945)
            pix = page.get_pixmap(matrix=fitz.Matrix(4, 4), clip=clip, alpha=False)
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
                text = " ".join(data["text"][index] for index in indexes).strip()
                lines.append({
                    "top": 55 + min(data["top"][index] for index in indexes) / 4,
                    "text": text,
                })
            lines.sort(key=lambda row: row["top"])
            lanes.append({"page": book_page, "column": column, "lines": lines})
        print(f"OCR source extraction: page {book_page}/146", flush=True)
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
    # Several descriptions flow around a table at the top of the next visual
    # column. Select the actual continuation lane rather than ingesting that
    # unrelated table between the two prose fragments.
    flow_around_tables = {
        "Cold warding": (
            (126, 0, 866.0, float("inf")), (126, 1, 780.0, 878.0)),
        "Exceptional arrow deflection": (
            (126, 1, 881.0, float("inf")), (127, 0, 390.0, 636.0)),
        "Great invulnerability": (
            (127, 0, 816.0, float("inf")), (127, 1, 420.0, 478.0)),
        "Acidic blast": (
            (129, 1, 838.0, float("inf")), (130, 0, 570.0, 659.0)),
        "Chaotic power": (
            (130, 0, 662.0, float("inf")), (130, 1, 575.0, 674.0)),
        "Holy power": (
            (131, 0, 852.0, float("inf")), (131, 1, 790.0, float("inf"))),
        "Lawful power": (
            (132, 0, 811.0, float("inf")), (132, 1, 380.0, 616.0)),
        "Mighty disruption": (
            (132, 1, 809.0, float("inf")),),
        "Staff of the cosmos": (
            (142, 0, 897.0, float("inf")), (142, 1, 275.0, 470.0)),
    }
    if name in flow_around_tables:
        body: List[str] = []
        pages = set()
        for page, column, low, high in flow_around_tables[name]:
            selected = take(page, column, low, high)
            if selected:
                body.extend(selected)
                pages.add(page)
        return body, sorted(pages)

    if name == "Cloak of epic resistance":
        body = take(145, 0, DESCRIPTION_ANCHORS[name][2] - 5, float("inf"))
        body += take(145, 1, 615.0, DESCRIPTION_ANCHORS["Gate key"][2] - 8)
        return body, [145]

    page, column, y = DESCRIPTION_ANCHORS[name]
    if name in DESCRIPTION_ENDS:
        end_page, end_column, end_y = DESCRIPTION_ENDS[name]
    elif next_name is not None:
        end_page, end_column, end_y = DESCRIPTION_ANCHORS[next_name]
    else:
        end_page, end_column, end_y = 146, 1, 350.0

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
        print(f"NO COVERAGE: {BOOK} item descriptions (missing PDF: {PDF_SOURCE})")
        return 1
    try:
        import fitz
    except Exception as exc:
        print(f"NO COVERAGE: {BOOK} item descriptions (PyMuPDF unavailable: {exc})")
        return 1

    keys = _all_description_keys()
    missing = set(keys) - set(DESCRIPTION_ANCHORS)
    extra = set(DESCRIPTION_ANCHORS) - set(keys)
    if missing or extra:
        raise RuntimeError(f"description anchor mismatch: missing={sorted(missing)}, "
                           f"extra={sorted(extra)}")
    try:
        doc = fitz.open(PDF_SOURCE)
        lanes = _ocr_lanes(doc)
    except Exception as exc:
        print(f"NO COVERAGE: {BOOK} item descriptions ({exc})")
        return 1

    lane_map = {(lane["page"], lane["column"]): lane["lines"] for lane in lanes}
    lane_keys = sorted(lane_map)
    ordered = sorted(keys, key=lambda key: DESCRIPTION_ANCHORS[key])
    chunks = [
        "# EPIC ITEM DESCRIPTION EXTRACTION",
        "",
        "Derived from Epic Level Handbook PDF page images, pp. 126-146.",
        "Two-column OCR is preserved raw. Item and ability headings alone are",
        "restored from the book-verified index transcription.",
        "",
    ]
    for index, name in enumerate(ordered):
        next_name = ordered[index + 1] if index + 1 < len(ordered) else None
        body, pages = _description_body(name, next_name, lane_map, lane_keys)
        if not body:
            raise RuntimeError(f"empty OCR description block for {name}")
        page_label = str(pages[0]) if len(pages) == 1 else f"{pages[0]}-{pages[-1]}"
        chunks.extend([
            f"## [PDF pages {page_label}]",
            f"{name.upper()} [EPIC ITEM DESCRIPTION]",
            *body,
            "",
        ])

    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    SOURCE.write_text("\n".join(chunks).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {SOURCE}")
    print(f"{len(ordered)}/{len(ordered)} epic-item description blocks recovered")
    return 0


def _name_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.casefold())


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
            raise ValueError(f"description heading before page marker at line {index + 1}")
        key = _name_key(heading_match.group(1))
        if key not in canonical:
            raise ValueError(f"unknown epic-item heading at line {index + 1}: {line!r}")
        headings.append((canonical[key], marker_index, index, marker_pages))

    spans: Dict[str, DescriptionSpan] = {}
    for position, (name, _, start, pages) in enumerate(headings):
        end = headings[position + 1][1] if position + 1 < len(headings) else len(lines)
        while end > start and not lines[end - 1].strip():
            end -= 1
        if name in spans:
            raise ValueError(f"duplicate epic-item description heading: {name}")
        spans[name] = DescriptionSpan(page=int(pages.split("-", 1)[0]), pages=pages,
                                      start=start, end=end)
    return spans


def _source_lines() -> List[str]:
    if not SOURCE.is_file():
        return []
    return SOURCE.read_text(encoding="utf-8").splitlines()


@dataclass(frozen=True)
class DescriptionSpan:
    page: int
    pages: str
    start: int
    end: int


@dataclass
class EpicItem:
    name: str
    kind: str            # "special-ability" | "specific-item"
    slot_or_type: str    # armor / shield / weapon(...) / ring / rod / staff / wondrous
    book: str
    market_price: Optional[str]
    effect: Optional[str]
    citation: str
    page: int
    description_key: str
    description_pages: str
    start: int
    end: int
    soft: Optional[str]


def build(lines: Optional[Sequence[str]] = None) -> List[EpicItem]:
    source_lines = list(lines) if lines is not None else _source_lines()
    spans = detect_description_spans(source_lines) if source_lines else {}
    out: List[EpicItem] = []
    seen = set()

    def span_fields(name: str) -> Tuple[str, str, int, int, Optional[str]]:
        description_key = _description_key(name)
        span = spans.get(description_key)
        if span:
            return description_key, span.pages, span.start, span.end, None
        return (description_key, "", 0, 0,
                "NO COVERAGE: full description (derived description extraction is missing)")

    # (A) special abilities — the same ability name recurs across the four
    # tables, so the (slot, name) pair is the identity.
    for slot, page, rows in _ABILITY_TABLES:
        for name, mod, effect in rows:
            key = ("special-ability", slot, name.lower())
            if key in seen:
                continue
            seen.add(key)
            description_key, description_pages, start, end, soft = span_fields(name)
            out.append(EpicItem(name=name, kind="special-ability", slot_or_type=slot,
                                book=BOOK, market_price=mod, effect=effect,
                                citation=CITATION, page=page,
                                description_key=description_key,
                                description_pages=description_pages,
                                start=start, end=end, soft=soft))

    # (B) specific items.
    # armor/weapons carry (name, slot, price, effect, page); rings/rods/staffs/
    # wondrous carry (name, price, effect, page) with a fixed slot per table.
    def add_specific(name, slot, price, effect, page):
        key = ("specific-item", slot, name.lower())
        if key in seen:
            return
        seen.add(key)
        description_key, description_pages, start, end, soft = span_fields(name)
        out.append(EpicItem(name=name, kind="specific-item", slot_or_type=slot,
                            book=BOOK, market_price=price, effect=effect,
                            citation=CITATION, page=page,
                            description_key=description_key,
                            description_pages=description_pages,
                            start=start, end=end, soft=soft))

    for name, slot, price, effect, page in _SPECIFIC_ARMOR:
        add_specific(name, slot, price, effect, page)
    for name, slot, price, effect, page in _SPECIFIC_WEAPONS:
        add_specific(name, slot, price, effect, page)
    for name, price, effect, page in _RINGS:
        add_specific(name, "ring", price, effect, page)
    for name, price, effect, page in _RODS:
        add_specific(name, "rod", price, effect, page)
    for name, price, effect, page in _STAFFS:
        add_specific(name, "staff", price, effect, page)
    for name, price, effect, page in _WONDROUS:
        add_specific(name, "wondrous", price, effect, page)

    return out


def _counts(items: List[EpicItem]):
    from collections import Counter
    by_kind = Counter(e.kind for e in items)
    by_slot = Counter(e.slot_or_type for e in items)
    return by_kind, by_slot


def write_index() -> int:
    if not SOURCE.is_file():
        raise FileNotFoundError(
            f"derived description extraction is missing: {SOURCE}; "
            "run --extract-source first"
        )
    items = build()
    recovered = sum(item.start < item.end for item in items)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    by_kind, by_slot = _counts(items)
    abilities = [e for e in items if e.kind == "special-ability"]
    specifics = [e for e in items if e.kind == "specific-item"]

    md: List[str] = [
        "# EPIC MAGIC ITEM INDEX — The New Path",
        "",
        "**Generated by `scripts/epic_item_harvest.py`. Do not hand-edit; rerun",
        "the harvest.** D&D 3.5 epic magic items from the Epic Level Handbook",
        "(Chapter 4, 'Epic Magic Items', pp.124-147). **Vision-transcribed from the",
        "PDF page images** because the book's OCR text layer is corrupt — this is",
        "still book RAW, read directly off the page. Two kinds of entry:",
        "**special-ability** (the epic weapon / armor / shield ability tables, each",
        "with its market-price modifier as a bonus equivalent) and **specific-item**",
        "(named rings, rods, staffs, wondrous items, weapons and armor with a market",
        "price). Ability-boost wondrous items are listed once with the price range",
        "the book prints across their bonus tiers.",
        "",
        f"*{len(items)} entries — {by_kind.get('special-ability', 0)} special "
        f"abilities, {by_kind.get('specific-item', 0)} specific items; "
        f"{recovered} full description spans.*",
        "",
        "## Epic item special abilities (Tables 4-6, 4-7, 4-15, 4-16)",
        "",
        "| Special Ability | Applies to | Market Price Modifier | Effect | Table Page | Description Pages |",
        "|---|---|---|---|---|---|",
    ]
    for e in abilities:
        md.append(f"| {e.name} | {e.slot_or_type} | {e.market_price} | {e.effect} | {e.page} | {e.description_pages} |")
    md += [
        "",
        "## Specific epic magic items (Tables 4-8, 4-17, 4-18, 4-19, 4-24, 4-25)",
        "",
        "| Item | Type | Market Price | Effect | Item Page | Description Pages |",
        "|---|---|---|---|---|---|",
    ]
    slot_order = {"weapon": 0, "armor": 1, "shield": 2, "ring": 3, "rod": 4,
                  "staff": 5, "wondrous": 6}
    for e in sorted(specifics, key=lambda e: (slot_order.get(e.slot_or_type, 9), e.name)):
        md.append(f"| {e.name} | {e.slot_or_type} | {e.market_price} | {e.effect} | {e.page} | {e.description_pages} |")
    md.append("")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/epic_item_harvest.py",
                    "book": BOOK, "citation": CITATION, "pages": PAGES,
                    "corpus": str(CORPUS),
                    "source_path": str(SOURCE_REL),
                    "source_sha256": _source_hash(),
                    "description_blocks": len(detect_description_spans(_source_lines())),
                    "full_description_entries": recovered,
                    "note": ("Vision-transcribed from the ELH PDF page images; the "
                             "OCR text layer is corrupt. Book RAW, read off the page. "
                             "All rows carry exact spans into a reproducible raw "
                             "two-column OCR extraction of 103 description blocks; "
                             "variants share the book's common block. "
                             "(A) weapon/armor/shield special-ability tables 4-6, 4-7, "
                             "4-15, 4-16; (B) specific-item tables 4-8, 4-17, 4-18, "
                             "4-19, 4-24, 4-25, cross-checked against the item "
                             "descriptions. Rod of the wyrm prices are from the item "
                             "description (p.140), where Table 4-19 was garbled. Not "
                             "harvested: the generic epic-scroll tables and the named "
                             "artifacts on pp.150-154 (no market price)."),
                    "total_entries": len(items),
                    "by_kind": dict(by_kind),
                    "by_slot_or_type": dict(by_slot),
                    "entries": [asdict(e) for e in items]}, indent=1),
        encoding="utf-8")
    return len(items)


def export_packet(query: str, out_path: Optional[Path]) -> int:
    q = query.casefold().strip()
    hits = [item for item in build() if q in item.name.casefold()]
    if not hits:
        print(f"NO COVERAGE: epic item export ({query!r} not found)")
        return 1
    lines = _source_lines()
    packet = {
        "generated_by": "scripts/epic_item_harvest.py --export",
        "query": query,
        "source": str(SOURCE),
        "source_sha256": _source_hash(),
        "entries": [],
    }
    for item in hits:
        row = asdict(item)
        row["full_description"] = ("\n".join(lines[item.start:item.end]).strip()
                                   if item.start < item.end else "")
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
    items = build()
    abilities = [e for e in items if e.kind == "special-ability"]
    specifics = [e for e in items if e.kind == "specific-item"]
    names = {(e.kind, e.slot_or_type, e.name) for e in items}

    # both kinds present, in force
    if not abilities:
        failures.append("no special-ability entries")
    if not specifics:
        failures.append("no specific-item entries")
    if len(abilities) != 55:
        failures.append(f"{len(abilities)} special abilities; expected exactly 55")
    if len(specifics) != 98:
        failures.append(f"{len(specifics)} specific items; expected exactly 98")
    if len(items) != 153:
        failures.append(f"{len(items)} total entries; expected exactly 153")

    # every slot/table represented
    slots = {e.slot_or_type for e in items}
    for s in ("armor", "shield", "weapon (melee)", "weapon (ranged)",
              "weapon", "ring", "rod", "staff", "wondrous"):
        if s not in slots:
            failures.append(f"no entries with slot_or_type '{s}'")

    # known special abilities exist with exact modifiers
    def find_ability(slot, name):
        return next((e for e in abilities
                     if e.slot_or_type == slot and e.name.lower() == name.lower()), None)
    for slot, name, mod in (
            ("armor", "Great spell resistance (SR 27)", "+9 bonus"),
            ("shield", "Great reflection", "+10 bonus"),
            ("shield", "Exceptional arrow deflection", "+8 bonus"),
            ("weapon (melee)", "Mighty disruption", "+6 bonus"),
            ("weapon (melee)", "Unholy power", "+8 bonus"),
            ("weapon (ranged)", "Distant shot", "+6 bonus"),
            ("weapon (ranged)", "Triple-throw", "+6 bonus")):
        a = find_ability(slot, name)
        if not a:
            failures.append(f"missing {slot} ability '{name}'")
        elif a.market_price != mod:
            failures.append(f"{slot} '{name}' modifier {a.market_price!r}, expected {mod!r}")

    # known specific items with exact prices
    def find_item(name):
        return next((e for e in specifics if e.name.lower() == name.lower()), None)
    for name, price in (
            ("Stormbrand", "235,350 gp"),
            ("Everwhirling chain", "5,220,325 gp"),
            ("Epic protection +10", "2,000,000 gp"),
            ("Staff of necromancy", "1,505,312 gp"),
            ("Bracers of relentless might", "4,384,000 gp"),
            ("Antimagic armor", "871,500 gp"),
            ("Armor of the celestial battalion", "656,300 gp"),
            ("Rod of the wyrm (red)", "1,897,400 gp")):
        it = find_item(name)
        if not it:
            failures.append(f"missing specific item '{name}'")
        elif it.market_price != price:
            failures.append(f"'{name}' price {it.market_price!r}, expected {price!r}")

    # the four ability tables each landed with the right count
    for slot, n in (("armor", 14), ("shield", 16),
                    ("weapon (melee)", 12), ("weapon (ranged)", 13)):
        got = sum(1 for e in abilities if e.slot_or_type == slot)
        if got != n:
            failures.append(f"{slot} abilities: {got}, expected {n}")

    # every entry has a market price and an effect; every ability's is a bonus
    for e in items:
        if not e.market_price:
            failures.append(f"'{e.name}' has no market_price")
        if not e.effect:
            failures.append(f"'{e.name}' has no effect")
        if e.kind == "special-ability" and e.market_price and "bonus" not in e.market_price:
            failures.append(f"ability '{e.name}' modifier not a bonus: {e.market_price!r}")
        if e.page < 124 or e.page > 147:
            failures.append(f"'{e.name}' page {e.page} outside the chapter (124-147)")

    # no duplicate identity
    if len(names) != len(items):
        failures.append("duplicate (kind, slot, name) entries")

    # Embedded span fixture: page markers belong to the following canonical
    # heading, and each block ends immediately before the next marker.
    fixture = [
        "## [PDF page 126]",
        "ACID WARDING [EPIC ITEM DESCRIPTION]",
        "raw acid body",
        "",
        "## [PDF pages 126-127]",
        "COLD WARDING [EPIC ITEM DESCRIPTION]",
        "raw cold body",
    ]
    fixture_spans = detect_description_spans(fixture)
    acid = fixture_spans.get("Acid warding")
    cold = fixture_spans.get("Cold warding")
    if not acid or (acid.pages, acid.start, acid.end) != ("126", 1, 3):
        failures.append(f"span fixture acid mismatch: {acid}")
    if not cold or (cold.pages, cold.start, cold.end) != ("126-127", 5, 7):
        failures.append(f"span fixture cold mismatch: {cold}")

    if set(_all_description_keys()) != set(DESCRIPTION_ANCHORS):
        failures.append("description keys and verified anchors differ")
    source_lines = _source_lines()
    recovered = [e for e in items if e.start < e.end]
    if len(recovered) != 153:
        failures.append(f"full description spans: {len(recovered)}, expected 153")
    if len({(e.start, e.end) for e in recovered}) != 103:
        failures.append("description span groups are not exactly 103")
    for e in items:
        if e.soft is not None:
            failures.append(f"'{e.name}' unexpectedly soft: {e.soft}")
        if not e.description_pages:
            failures.append(f"'{e.name}' has no description_pages")
        if e.start < e.end:
            if e.end > len(source_lines):
                failures.append(f"'{e.name}' span ends past source length")
            elif _name_key(e.description_key) not in _name_key(source_lines[e.start]):
                failures.append(f"'{e.name}' span does not lead with description_key")

    live_spans = detect_description_spans(source_lines) if source_lines else {}
    routed = ("Cold warding", "Exceptional arrow deflection",
              "Great invulnerability", "Acidic blast", "Chaotic power",
              "Holy power", "Lawful power", "Mighty disruption",
              "Staff of the cosmos")
    for key in routed:
        span = live_spans.get(key)
        if span:
            segment = "\n".join(source_lines[span.start:span.end])
            if re.search(r"\b(?:table|tame|taste)\s+4[-—]", segment, re.I):
                failures.append(f"'{key}' span swallowed a generation table")

    for key, expected_rows in (("Great invulnerability", 8),
                               ("Great spell resistance", 8),
                               ("Rod of the wyrm", 10)):
        group = [e for e in items if e.description_key == key]
        if len(group) != expected_rows or len({(e.start, e.end) for e in group}) != 1:
            failures.append(f"shared description span drift for {key}")

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
                or q in e.slot_or_type.lower()
                or (e.effect and q in e.effect.lower())
                or (e.market_price and q in e.market_price.lower())]
        for e in sorted(hits, key=lambda e: (e.kind, e.slot_or_type, e.name)):
            tag = "ability" if e.kind == "special-ability" else "item"
            print(f"  [{tag}] {e.name} ({e.slot_or_type}) — {e.market_price} "
                  f"— {e.effect} (p.{e.page})")
        print(f"{len(hits)} match(es).")
        return 0 if hits else 1

    n = write_index()
    by_kind, _ = _counts(build())
    print(f"{n} D&D 3.5 epic magic item entries (Epic Level Handbook, Chapter 4, "
          f"vision-transcribed): {by_kind.get('special-ability', 0)} special "
          f"abilities + {by_kind.get('specific-item', 0)} specific items.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
