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
                                     slot_or_type, market_price, effect, page
    reference/epic_item_index.md   — the same, for human eyes

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
OUT_JSON = REPO / "reference" / "epic_item_index.json"
OUT_MD = REPO / "reference" / "epic_item_index.md"
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


def build() -> List[EpicItem]:
    out: List[EpicItem] = []
    seen = set()

    # (A) special abilities — the same ability name recurs across the four
    # tables, so the (slot, name) pair is the identity.
    for slot, page, rows in _ABILITY_TABLES:
        for name, mod, effect in rows:
            key = ("special-ability", slot, name.lower())
            if key in seen:
                continue
            seen.add(key)
            out.append(EpicItem(name=name, kind="special-ability", slot_or_type=slot,
                                book=BOOK, market_price=mod, effect=effect,
                                citation=CITATION, page=page))

    # (B) specific items.
    # armor/weapons carry (name, slot, price, effect, page); rings/rods/staffs/
    # wondrous carry (name, price, effect, page) with a fixed slot per table.
    def add_specific(name, slot, price, effect, page):
        key = ("specific-item", slot, name.lower())
        if key in seen:
            return
        seen.add(key)
        out.append(EpicItem(name=name, kind="specific-item", slot_or_type=slot,
                            book=BOOK, market_price=price, effect=effect,
                            citation=CITATION, page=page))

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
    items = build()
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
        f"abilities, {by_kind.get('specific-item', 0)} specific items.*",
        "",
        "## Epic item special abilities (Tables 4-6, 4-7, 4-15, 4-16)",
        "",
        "| Special Ability | Applies to | Market Price Modifier | Effect | Page |",
        "|---|---|---|---|---|",
    ]
    for e in abilities:
        md.append(f"| {e.name} | {e.slot_or_type} | {e.market_price} | {e.effect} | {e.page} |")
    md += [
        "",
        "## Specific epic magic items (Tables 4-8, 4-17, 4-18, 4-19, 4-24, 4-25)",
        "",
        "| Item | Type | Market Price | Effect | Page |",
        "|---|---|---|---|---|",
    ]
    slot_order = {"weapon": 0, "armor": 1, "shield": 2, "ring": 3, "rod": 4,
                  "staff": 5, "wondrous": 6}
    for e in sorted(specifics, key=lambda e: (slot_order.get(e.slot_or_type, 9), e.name)):
        md.append(f"| {e.name} | {e.slot_or_type} | {e.market_price} | {e.effect} | {e.page} |")
    md.append("")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/epic_item_harvest.py",
                    "book": BOOK, "citation": CITATION, "pages": PAGES,
                    "note": ("Vision-transcribed from the ELH PDF page images; the "
                             "OCR text layer is corrupt. Book RAW, read off the page. "
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
    if len(abilities) < 50:
        failures.append(f"only {len(abilities)} special abilities; the 4 tables give 55")
    if len(specifics) < 80:
        failures.append(f"only {len(specifics)} specific items; expected ~98")
    if len(items) < 140:
        failures.append(f"only {len(items)} total entries; expected ~153")

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

    for f in failures:
        print(f"SELFTEST FAIL: {f}")
    print("selftest: " + ("PASS" if not failures else f"{len(failures)} failure(s)"))
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
