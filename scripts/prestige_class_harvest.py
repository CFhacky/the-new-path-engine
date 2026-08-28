#!/usr/bin/env python3
"""prestige_class_harvest.py — D&D 3.0/3.5 prestige classes from the Dragon
Magazine Prestige Class Compendium (Issues #274-353).

WHY THIS ONE IS A VISION HARVEST (same story as epic_feat_harvest /
ad2e_monster_harvest). The compendium is a 355-page scan: 321 of its 355 pages
have NO text layer at all (image-only), and the ~34 pages that do carry corrupt
OCR ("bbodsister" for "bloodsister", "al Each" for "at Each"). Parsing the text
layer is hopeless. But the PDF's page IMAGES are perfectly legible, so each
prestige class's name, Hit Die, and — the killer field — its full REQUIREMENTS
(prerequisite) block were transcribed BY VISION from the rendered pages
(PyMuPDF render at 2.3x -> read the PNG). This is still book RAW — read directly
off the page, not invented — and every entry cites its PDF page.

The prestige classes are scattered across the magazine and interleaved with
flavor prose; they were LOCATED via the PDF outline (80 article bookmarks) and
the corrupt text layer, then each candidate page was rendered and read. The
compendium reprints ordinary FEATS too (with "Prerequisites:"); those are NOT
prestige classes and are excluded — every entry here has a class level table,
a Hit Die, and a Class Requirements / Requirements block.

    reference/prestige_class_index.json — every PrC: name, hit_die, the full
                                          requirements string, book, citation,
                                          PDF page
    reference/prestige_class_index.md   — the same, for human eyes

PROVENANCE
    Dragon Magazine Prestige Class Compendium (Issues 274-353), v1.0, a fan
    compilation of the prestige classes published in Dragon Magazine #274-353
    (3.0/3.5e). Rendered from the PDF via PyMuPDF and read by vision because the
    OCR text layer is corrupt and absent on most pages. `page` is the PDF page.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO = Path(__file__).resolve().parent.parent
OUT_JSON = REPO / "reference" / "prestige_class_index.json"
OUT_MD = REPO / "reference" / "prestige_class_index.md"
BOOK = "Dragon Magazine Prestige Class Compendium (Issues 274-353)"
CITATION = (
    "Dragon Magazine Prestige Class Compendium (Issues 274-353), v1.0 — a "
    "compilation of the 3.0/3.5e prestige classes from Dragon Magazine "
    "#274-353. Vision-transcribed from the PDF page images (321/355 pages are "
    "image-only and the rest carry corrupt OCR). Book RAW, read off the page. "
    "`page` is the PDF page."
)

# (name, hit_die, requirements, page) — each transcribed BY VISION from the
# rendered PDF page cited. `requirements` is the class's prerequisite block,
# copied as printed. Grouped by source article (Dragon issue in the comment).
_T = [
    # --- Race-based PrCs -------------------------------------------------
    # Paragons of the Kindred (Dragon 328) — nonhuman-deity clerics
    ("Chimeric Champion of Garl Glittergold", "d8",
     "Race: Gnome. Patron Deity: Garl Glittergold. Base Will Save: +5. Skills: Craft (alchemy) 3 ranks, Knowledge (arcana) 10 ranks. Feats: Brew Potion, Scribe Scroll. Spells: Able to cast 3rd-level or higher divine spells.", 12),
    ("Itinerant Warder of Yondalla", "d6",
     "Race: Halfling. Patron Deity: Yondalla. Base Will Save: +5. Skills: Diplomacy 10 ranks, Tumble 4 ranks. Feats: Dodge, Mobility. Spells: Able to cast divine spells.", 14),
    ("Justice Hammer of Moradin", "d10",
     "Race: Dwarf. Patron Deity: Moradin. Base Attack Bonus: +5. Skills: Concentration 5 ranks, Knowledge (local) 3 ranks. Feats: Iron Will, Power Attack. Spells: Able to cast divine spells.", 16),
    ("Mystic Keeper of Corellon Larethian", "d8",
     "Race: Elf or half-elf. Patron Deity: Corellon Larethian. Base Attack Bonus: +5. Skills: Concentration 10 ranks, Perform (dance) 2 ranks. Feats: Still Spell, Weapon Finesse. Spells: Able to cast divine spells.", 18),
    # Ancestral Avenger (Dragon 279)
    ("Ancestral Avenger", "d8",
     "Race: Elf or half-elf. Base Attack: +5. Wilderness Lore: 3 ranks. Feats: Alertness, Iron Will, Tracking.", 19),
    # Giant Killer (Dragon 291)
    ("Gnome Giant-Killer", "d10",
     "Race: Gnome. Base Attack Bonus: +5. Escape Artist: 3 ranks. Tumble: 3 ranks. Feats: Dodge, Mobility, Spring Attack. Special: Speak Language (Giant).", 22),
    # Lightbearer (Dragon 285)
    ("Lightbearer", "d8",
     "Alignment: Any good. Race: Gnome or halfling. Knowledge (religion): 8 ranks. Knowledge (local): 4 ranks. Diplomacy: 4 ranks. Feats: Alertness.", 24),
    # The Stonelord (Dragon 278)
    ("Stonelord", "d8",
     "Base Attack: +5 or better. Craft (stoneworking): 6 ranks. Spellcraft: 3 ranks. Race: Dwarf. Feats: Endurance. Language: Terran. Special: Must undergo an arduous ritual (immersion in sacred loam, fasting deep underground, and ingesting 1,000 gp worth of powdered gemstones).", 25),
    # Exiles from the Vault (Dragon 298) — Kilsek drow
    ("Bloodsister", "d10",
     "Race: Drow. Sex: Female. Alignment: Any evil. Base Attack Bonus: +6 or better. Feats: Ambidexterity, Exotic Weapon Proficiency (hand crossbow), Two-Weapon Fighting.", 29),
    ("Nightshade", "d8",
     "Race: Drow. Alignment: Any evil. Move Silently: 7 ranks. Feats: Point Blank Shot. Special: Must be able to cast arcane spells.", 31),
    # Crusades of the Ashen Compact (Dragon 298) — anti-drow
    ("Deep Avenger", "d8",
     "Base Attack Bonus: +7. Feats: Blind-Fight, Power Attack. Special: Must speak Undercommon; must have lost a loved one to the drow within the last 5 years.", 36),
    ("Gloomblade", "d6",
     "Move Silently: 10 ranks. Hide: 10 ranks. Feats: Alertness, Blind-Fight. Special: Must speak Undercommon.", 37),
    ("Gray Sage", "d4",
     "Feats: Blind-Fight, Silent Spell, Spell Penetration. Spells: Able to cast any 4th-level Conjuration spell. Special: Must speak Undercommon.", 38),

    # --- Faiths of Faerun / deity PrCs ----------------------------------
    # Champions of Virtue (Dragon 283) — Greyhawk deity clerics
    ("Shining Blade of Heironeous", "d10",
     "Alignment: Lawful Good. Patron Deity: Heironeous. Base Attack Bonus: +7. Base Will Save: +3. Skills: Knowledge (religion) 7 ranks. Spellcasting: Ability to cast divine spells.", 41),
    ("Radiant Servant of Pelor", "d6",
     "Alignment: Neutral Good. Patron Deity: Pelor. Base Will Save: +5. Skills: Knowledge (religion) 9 ranks, Heal 5 ranks, Knowledge (undead) 3 ranks. Feats: Extra Turning. Spellcasting: Ability to cast divine spells.", 43),
    ("Fleet Runner of Ehlonna", "d8",
     "Alignment: Neutral Good. Patron Deity: Ehlonna. Base Will Save: +3. Skills: Knowledge (nature) 11 ranks, Knowledge (religion) 3 ranks, Wilderness Lore 5 ranks. Feats: Dodge, Mobility, Run. Spellcasting: Ability to cast divine spells.", 44),
    ("Mighty Contender of Kord", "d10",
     "Alignment: Chaotic Good. Patron Deity: Kord. Base Fortitude Save: +6. Skills: Knowledge (religion) 9 ranks. Feats: Endurance, Power Attack. Spellcasting: Ability to cast divine spells.", 47),
    # Arvoreen's Keepers (Dragon 321)
    ("Arvoreen's Keeper", "d8",
     "Race: Halfling. Religion: Arvoreen. Alignment: Lawful good, neutral good, or lawful neutral. Base Attack Bonus: +4. Skills: Craft (trapmaking) 4 ranks, Listen 4 ranks, Sense Motive 4 ranks, Spot 4 ranks, Survival 4 ranks. Feats: Alertness, Martial Weapon Proficiency (short sword), Simple Weapon Proficiency (sling) or Martial Weapon Proficiency (shortbow), Track. Spells: Must be able to cast divine spells. Special: Must be judged worthy by a cleric of Arvoreen.", 50),
    ("Arvoreen's Warder", "d8",
     "Race: Halfling. Religion: Arvoreen. Alignment: Lawful good, neutral good, or lawful neutral. Base Attack Bonus: +4. Skills: Craft (trapmaking) 4 ranks, Listen 4 ranks, Sense Motive 4 ranks, Spot 4 ranks, Survival 4 ranks. Feats: Alertness, Martial Weapon Proficiency (short sword), Simple Weapon Proficiency (sling) or Martial Weapon Proficiency (shortbow), Track. Special: Must be judged worthy by a cleric of Arvoreen.", 51),
    # Battleguard of Tempus (Dragon 317)
    ("Battleguard of Tempus", "d10",
     "Patron: Tempus. Alignment: Any nonlawful. Base Attack Bonus: +4. Skills: Craft (armorsmithing) 5 ranks, Craft (weaponsmithing) 5 ranks, Handle Animal 3 ranks, Ride 3 ranks. Feats: Combat Casting, Leadership, Weapon Focus (any). Spells: Ability to cast 2nd-level divine spells; clerics must have access to the War domain. Special: Must have fought in at least five battles and been on the winning side of at least three battles involving fifty or more combatants.", 53),
    # Blessed of Gruumsh (Dragon 282)
    ("Blessed of Gruumsh", "d10",
     "Alignment: Any non-good. Race: Orc or half-orc. Base Attack Bonus: +6. Knowledge (religion): 3 ranks. Feats: Weapon Proficiency (orc double-axe), Power Attack, Cleave. Special: In a ritual dedicated to Gruumsh, the character must remove one of his own eyes.", 55),
    # Dancers of Sharess (Dragon 290)
    ("Dancer of Sharess", "d6",
     "Patron Deity: Sharess. Alignment: Chaotic good. Base Attack Bonus: +3. Perform: 4 ranks (including Perform [dancing]). Knowledge (religion): 9 ranks. Spellcasting: Able to cast 3rd-level divine spells; clerics must select the Charm domain.", 58),
    # Deathstalker of Bhaal (Dragon 322)
    ("Deathstalker of Bhaal", "d8",
     "Patron Deity: Bhaal. Alignment: Lawful evil. Skills: Hide 5 ranks, Move Silently 5 ranks, Survival 2 ranks. Feats: Quick Draw. Spells: Ability to cast 3rd-level divine spells; clerics must have access to the Death or Destruction domain. Special: Must have murdered at least sixteen sentient creatures using sixteen different weapons or methods.", 60),
    # Dreadmaster (Dragon 287)
    ("Dreadmaster", "d8",
     "Patron Deity: Bane. Alignment: Lawful evil. Base Attack Bonus: +4. Intimidate: 5 ranks. Sense Motive: 4 ranks. Feats: Leadership, Skill Focus (Intimidate), Spell Focus (Enchantment). Spellcasting: Ability to cast 3rd-level divine spells; clerics must have access to the Hatred or Tyranny domain. Cohort: A cohort of at least 6th level.", 62),
    # Green Hunter (Dragon 294)
    ("Green Hunter", "d8",
     "Patron Deity: Thard Harr. Alignment: Any good. Base Attack Bonus: +4. Knowledge (nature): 5 ranks. Wilderness Lore: 5 ranks. Feats: Track. Spells: Ability to cast divine spells.", 65),
    # Nightcloak (Dragon 286)
    ("Nightcloak", "d8",
     "Patron Deity: Shar. Alignment: Neutral evil. Base Attack Bonus: +4. Bluff: 2 ranks. Move Silently: 2 ranks. Perform: 4 ranks. Feats: Iron Will, Shadow Weave Magic, Spell Focus (Enchantment, Illusion, or Necromancy), and Pernicious Magic or Tenacious Magic. Spellcasting: Ability to cast 2nd-level divine spells; clerics must have access to the Darkness domain.", 66),
    # Silverstar (Dragon 285)
    ("Silverstar", "d8",
     "Patron Deity: Selune. Alignment: Chaotic Good. Base Attack Bonus: +4. Intuit Direction: 2 ranks. Sense Motive: 2 ranks. Feats: Blind-Fight, Dodge, Mobility, Spring Attack. Spellcasting: Ability to cast 2nd-level divine spells; clerics must have access to the Moon domain.", 68),

    # --- Campaign Setting Specific --------------------------------------
    # The Exiled Factions (Dragon 315) — Planescape
    ("Harmonium Peacekeeper", "d10",
     "Alignment: Any lawful. Base Attack Bonus: +6. Knowledge (religion): 5 ranks. Ride: 5 ranks. Feats: Mounted Combat.", 72),
    ("Anarchomancer", "d4",
     "Alignment: Any chaotic. Disguise: 6 ranks. Bluff: 6 ranks. Feats: Greater Spell Focus (illusion) or Greater Spell Focus (enchantment). Spellcasting: Ability to cast at least one arcane illusion spell of 1st-5th level, and ability to cast polymorph.", 74),
    # Fractious Factions (Dragon 287) — Planescape
    ("The Athar", "d8",
     "Base Attack: +7. Base Will Save: +3. Knowledge (religion): 10 ranks. Spellcasting: Ability to cast divine spells. Special: Must abandon the worship of gods and refuse to acknowledge them as worthy of praise (clerics become ex-clerics).", 76),
    ("The Cipher", "d8",
     "Balance: 5 ranks. Jump: 10 ranks. Knowledge (religion): 10 ranks. Feats: Improved Initiative, Power Attack, Sunder.", 77),
    ("The Sensate", "d6",
     "Intuit Direction: 5 ranks. Spot: 7 ranks. Listen: 7 ranks. Feats: Alertness, Skill Focus (Knowledge [any]).", 79),
    ("The Sinker", "d10",
     "Base Attack Bonus: +5. Disable Device: 5 ranks. Knowledge (architecture & engineering): 3 ranks. Feats: Great Fortitude, Power Attack, Sunder.", 80),
    ("The Taker", "d6",
     "Base Attack Bonus: +4. Bluff: 5 ranks. Diplomacy: 5 ranks. Intimidate: 5 ranks. Feats: Skill Focus (Bluff, Diplomacy, or Intimidate).", 82),
    ("The Xaositect", "d8",
     "Alignment: Any chaotic. Base Attack Bonus: +4. Base Fort Save: +2. Base Reflex Save: +2. Base Will Save: +2.", 83),
    # Heroes of Cormyr (Dragon 307) — Forgotten Realms
    ("Battlepriest of Cormyr", "d8",
     "Alignment: Any nonevil and nonchaotic. Base Attack Bonus: +5. Concentration: 5 ranks. Diplomacy: 5 ranks. Heal: 3 ranks. Feats: Combat Casting, Leadership. Spells: Ability to cast divine spells and access to the Nobility, Protection, Strength, or War domain.", 87),
    ("Council Mage of Cormyr", "d4",
     "Alignment: Any nonevil and nonchaotic. Gather Information: 2 ranks. Knowledge (arcana): 6 ranks. Scry: 6 ranks. Spellcraft: 12 ranks. Feats: Skill Focus (Spellcraft), any metamagic feat, any item creation feat. Spellcasting: Ability to cast 5th-level arcane spells, knowledge of spells from at least five schools. Special: Membership on Cormyr's Council of Mages and a blood vow to never harm Cormyr or her Crown.", 88),
    ("Noble Adventurer of Cormyr", "d8",
     "Base Attack Bonus: +4. Diplomacy: 4 ranks. Knowledge (nobility and royalty): 4 ranks. Ride: 4 ranks. Special: Must be literate and possess equipment and treasure worth more than the starting equipment for a PC of their level.", 89),
    ("Moon Drover of Cormyr", "d8",
     "Patron: Bright Nydra (Selune). Alignment: Chaotic good. Base Fortitude Save: +5. Base Will Save: +5. Handle Animal: 3 ranks. Knowledge (nature): 5 ranks. Wilderness Lore: 3 ranks. Spellcasting: Ability to cast 2nd-level divine spells and access to the Good, Protection, Travel, or Chaos domain.", 91),
    ("Royal Scout of Cormyr", "d8",
     "Alignment: Any nonevil and nonchaotic. Base Attack Bonus: +5. Hide: 3 ranks. Innuendo: 1 rank. Intuit Direction: 1 rank. Move Silently: 3 ranks. Ride: 5 ranks. Spot: 3 ranks. Wilderness Lore: 5 ranks. Feats: Alertness, Track. Special: Membership in the Purple Dragons; must be literate.", 93),
    # Taladas (Dragon 315) — Dragonlance
    ("Companion of the Dead", "d12",
     "Race: Gnome. Intimidate: 10 ranks. Knowledge (history): 5 ranks. Feats: Armor Proficiency (heavy), Diehard, Endurance, Power Attack, Toughness, Weapon Focus (any melee weapon). Special: Must sever all ties with family and forsake all personal wealth and possessions (except armor, melee weapons, and combat-augmenting magic items).", 95),
    ("Shark Cultist", "d8",
     "Alignment: Chaotic evil, chaotic neutral, or neutral evil. Craft (leatherworking): 1 rank. Knowledge (nature): 5 ranks. Swim: 8 ranks. Feats: Exotic Weapon Proficiency (sharktooth gauntlet), Skill Focus (Swim). Special: Must slay a shark of at least Large size in single combat and craft a war-helmet and sharktooth gauntlets from its body.", 96),
    # Ranger Knight of Furyondy (Dragon 317) — Greyhawk
    ("Ranger Knight of Furyondy", "d10",
     "Alignment: Any good. Base Attack: +5. Handle Animal: 4 ranks. Hide: 2 ranks. Move Silently: 2 ranks. Ride: 8 ranks. Feats: Mounted Combat, Track, Trample, Two-Weapon Fighting.", 99),
    # The Sundered Empire (Dragon 315) — Chainmail/Greyhawk
    ("Boge of Nomog-Geaya", "d8",
     "Race: Hobgoblin. Feats: Leadership, Weapon Focus (longsword). Special: Ability to cast 3rd-level divine spells.", 102),
    # Champions of Vengeance (Dragon 297) — Greyhawk (also reprinted at p283)
    ("Knight of the Chase", "d8",
     "Alignment: Chaotic good. Base Attack Bonus: +6. Handle Animal: 4 ranks. Ride: 4 ranks. Feats: Weapon Focus (longsword). Special: Must be an ardent worshiper of Trithereon who has performed some great undertaking in his name.", 105),
    # Masks of Iron (Dragon 302) — Greyhawk
    ("Mask of Johydee", "d8",
     "Alignment: Neutral good. Base Attack Bonus: +5. Disguise: 6 ranks. Gather Information: 6 ranks. Spot: 4 ranks. Feats: Alertness, Skill Focus (Bluff, Diplomacy, or Gather Information). Special: Must be an ardent worshiper of Johydee and speak Old Oeridian.", 110),
    # Champions of Fate (Dragon 321) — Al-Qadim
    ("Barber", "d8",
     "Base Attack Bonus: +3. Skills: Bluff 5 ranks, Diplomacy 5 ranks, Disguise 5 ranks, Gather Information 8 ranks, Heal 2 ranks, Profession (barber) 2 ranks. Feat: Investigator or Negotiator.", 112),
    ("Corsair", "d8",
     "Base Attack Bonus: +4. Skills: Balance 4 ranks, Climb 4 ranks, Intimidate 6 ranks, Use Rope 4 ranks. Feats: Two-Weapon Fighting, Weapon Finesse, Weapon Focus (scimitar).", 113),
    ("Holy Slayer", "d8",
     "Alignment: Any lawful. Base Attack Bonus: +4. Skills: Disguise 2 ranks, Hide 2 ranks, Intimidate 8 ranks, Knowledge (religion) 2 ranks, Move Silently 2 ranks. Feat: Weapon Focus (the slayer brotherhood's chosen one-handed weapon).", 115),
    ("Mamluk", "d12",
     "Alignment: Any lawful. Base Attack Bonus: +5. Base Fortitude Saving Throw: +4. Skills: Knowledge (history) 4 ranks, Survival 4 ranks. Feats: Great Fortitude, Toughness.", 117),
    # Dragonmarked (Dragon 320) — Eberron
    ("Dragonmark Heir", "d8",
     "Race: Member of the appropriate dragonmarked race and house. Skills: 7 ranks in any two skills. Feats: Favored in House, Least Dragonmark.", 121),
    # Ice Wall Campaign (Dragon 307) — Westeros
    ("Ranger of the Night's Watch", "d8",
     "Base Attack Bonus: +4. Knowledge (local - the Ice Wall): 4 ranks. Ride: 6 ranks. Feat: Endurance. Special: Must take the oath of the Night's Watch and remain obedient to its officers.", 127),

    # --- Warriors -------------------------------------------------------
    # 3 Gladiators (Dragon 303)
    ("Invisible Blade", "d6",
     "Bluff: 8 ranks. Sense Motive: 6 ranks. Feats: Point Blank Shot, Far Shot, Weapon Focus (dagger, kukri, or punching dagger). Special: Must defeat an opponent of CR equal to his character level in single combat using only daggers, kukris, or punching daggers.", 131),
    ("Occult Slayer", "d8",
     "Base Attack Bonus: +5. Knowledge (arcana): 4 ranks. Spellcraft: 3 ranks. Feats: Improved Initiative, Weapon Focus (any). Special: The candidate (or someone close to her) must have been brought to 0 hit points or below by a magical attack.", 132),
    ("Reaping Mauler", "d10",
     "Base Attack Bonus: +5. Escape Artist: 8 ranks. Tumble: 5 ranks. Feats: Clever Wrestling, Improved Unarmed Strike. Special: Must have defeated at least three opponents one size category larger than himself with his bare hands.", 134),
    # Master Siege Engineer (Dragon 295)
    ("Master Siege Engineer", "d10",
     "Feats: Skill Focus (Profession [siege engineer]). Craft (siege weaponry): 4 ranks. Knowledge (architecture and engineering): 4 ranks. Profession (siege engineer): 8 ranks. Spot: 4 ranks.", 135),
    # Duelist (Dragon 275)
    ("Duelist", "d10",
     "Base Attack Bonus: +6. Skills: Perform 3 ranks, Tumble 5 ranks. Feats: Dodge, Weapon Proficiency (rapier), Ambidexterity, Mobility.", 136),
    # Bowman Charger (Dragon 325)
    ("Bowman Charger", "d10",
     "Base Attack Bonus: +6. Skills: Handle Animal 8 ranks, Ride 8 ranks. Feats: Mounted Archery, Mounted Combat, Ride-By Attack, Weapon Focus (composite shortbow).", 139),

    # --- Stealthy -------------------------------------------------------
    # Assassin Specialty Classes (Dragon 312)
    ("Oppressor", "d8",
     "Alignment: Any evil. Base Attack Bonus: +5. Intimidate: 8 ranks. Feats: Improved Grapple, Improved Unarmed Strike, Persuasive. Sneak Attack: +1d6. Special: Must have killed someone in public and be a known killer in at least one region.", 143),
    ("Poisoner", "d6",
     "Alignment: Any evil. Bluff: 5 ranks. Craft (poisonmaking): 8 ranks. Sleight of Hand: 8 ranks. Feat: Exotic Weapon Proficiency (blowgun). Special: Must have used poison to kill a specific person.", 144),
    ("Replacement Killer", "d6",
     "Alignment: Any evil. Bluff: 8 ranks. Diplomacy: 5 ranks. Disguise: 8 ranks. Knowledge (nobility and royalty): 3 ranks. Sense Motive: 5 ranks. Feats: Deceitful, Skill Focus (Disguise).", 146),
    # 3 Ninjas (Dragon 289)
    ("Poison Fist", "d6",
     "Alignment: Any non-good. Base Attack Bonus: +3. Hide: 8 ranks. Intimidate: 5 ranks. Move Silently: 8 ranks. Feats: Dodge, Improved Unarmed Strike, Great Fortitude, Mobility, Stunning Fist (or monk's stunning attack). Special: Must choose a poison fist clan (Snake, Scorpion, or Spider).", 150),
    ("Ghost-Faced Killer", "d8",
     "Alignment: Any evil. Base Attack Bonus: +5. Hide: 6 ranks. Concentration: 4 ranks. Intimidate: 4 ranks. Move Silently: 6 ranks. Feats: Death Blow, Improved Initiative, Power Attack, Quick Draw.", 152),
    ("Weightless Foot", "d8",
     "Alignment: Any non-chaotic, non-evil. Base Attack Bonus: +4. Base Reflex Save: +2. Balance: 8 ranks. Climb: 4 ranks. Concentration: 4 ranks. Jump: 6 ranks. Tumble: 4 ranks. Feats: Dodge, Iron Will, Mobility, Point Blank Shot. Special: Must have the evasion special ability.", 155),
    # Nightsong Guild (Dragon 294 / 293)
    ("Nightsong Infiltrator", "d6",
     "Open Locks: 10 ranks. Move Silently: 6 ranks. Disable Device: 4 ranks. Pick Pocket: 5 ranks. Feats: Alertness. Special: Must complete three months of training with the Nightsong Guild and contribute 10% of all earnings.", 157),
    ("Nightsong Enforcer", "d8",
     "Base Attack Bonus: +5. Move Silently: 10 ranks. Hide: 10 ranks. Feats: Improved Initiative, Quick Draw. Special: Must complete three months of training with the Nightsong Guild and contribute 10% of all earnings.", 159),

    # --- Martial Arts ---------------------------------------------------
    # Animal Fists (Dragon 319) — the Shen (each animal is a separate PrC)
    ("Shen (Crane)", "d8",
     "Base Attack Bonus: +5. Knowledge (nature): 2 ranks. Survival: 3 ranks. Feat: Improved Unarmed Strike. Additional (Crane): Combat Expertise, Dodge, Balance 5 ranks, Jump 5 ranks.", 162),
    ("Shen (Dragon)", "d8",
     "Base Attack Bonus: +5. Knowledge (nature): 2 ranks. Survival: 3 ranks. Feat: Improved Unarmed Strike. Additional (Dragon): Weapon Focus (unarmed strike), Concentration 4 ranks, Intimidate 3 ranks.", 163),
    ("Shen (Mantis)", "d8",
     "Base Attack Bonus: +5. Knowledge (nature): 2 ranks. Survival: 3 ranks. Feat: Improved Unarmed Strike. Additional (Mantis): Combat Expertise, Improved Trip, Concentration 2 ranks, Escape Artist 5 ranks.", 164),
    ("Shen (Monkey)", "d8",
     "Base Attack Bonus: +5. Knowledge (nature): 2 ranks. Survival: 3 ranks. Feat: Improved Unarmed Strike. Additional (Monkey): Weapon Focus (quarterstaff), Balance 5 ranks, Tumble 5 ranks.", 164),
    ("Shen (Panther)", "d8",
     "Base Attack Bonus: +5. Knowledge (nature): 2 ranks. Survival: 3 ranks. Feat: Improved Unarmed Strike. Additional (Panther): Improved Initiative, Hide 5 ranks, Move Silently 5 ranks.", 165),
    ("Shen (Snake)", "d8",
     "Base Attack Bonus: +5. Knowledge (nature): 2 ranks. Survival: 3 ranks. Feat: Improved Unarmed Strike. Additional (Snake): Stunning Fist, Concentration 4 ranks, Heal 2 ranks.", 165),
    ("Shen (Tiger)", "d8",
     "Base Attack Bonus: +5. Knowledge (nature): 2 ranks. Survival: 3 ranks. Feat: Improved Unarmed Strike. Additional (Tiger): Power Attack, Concentration 2 ranks, Intimidate 4 ranks.", 166),
    # Acolyte of the Fist (Dragon 296)
    ("Acolyte of the Fist", "d8",
     "Alignment: Any lawful. Tumble: 8 ranks. Jump: 8 ranks. Feats: Improved Unarmed Strike, Iron Will, Stunning Fist. Special: Once begun, cannot advance in another class until all ten levels are gained.", 168),
    # Oath & Order (Dragon 299)
    ("Reaper's Child", "d8",
     "Unarmed Base Attack Bonus: +4/+1. Knowledge (religion): 4 ranks. Feats: Improved Unarmed Strike, Deflect Arrows, Dodge. Alignment: Lawful evil. Special: Must undergo the grisly secret initiation known as the \"Oath.\"", 171),
    ("Monk of the Enabled Hand", "d8",
     "Unarmed Base Attack Bonus: +4/+1. Feats: Improved Unarmed Strike, Deflect Arrows, Expertise, Improved Disarm. Alignment: Any lawful. Special: Must obtain permission to join the order at one of its chapter houses.", 172),
    # Way of the Fist (Dragon 295)
    ("Primal Rager", "d10",
     "Alignment: Any nonlawful. Base Attack Bonus: +8. Wilderness Lore: 5 ranks. Feats: Improved Unarmed Strike, Iron Will. Special: Ability to rage 2/day.", 175),
    ("Fierce Grappler", "d10",
     "Base Attack Bonus: +6. Escape Artist: 5 ranks. Feats: Improved Unarmed Strike, Power Attack, Stunning Fist.", 176),
    ("Brawler", "d10",
     "Base Attack Bonus: +7. Intimidate: 5 ranks. Feats: Alertness, Combat Reflexes, Improved Unarmed Strike.", 177),

    # --- Outdoors -------------------------------------------------------
    # Woodland Prestige Classes (Dragon 292) — "Stone, Road, and Tusk"
    ("Cave Stalker", "d8",
     "Base Attack Bonus: +5. Feats: Blind-Fight, Track. Race: Dwarf. Craft (trapmaking): 5 ranks. Move Silently: 5 ranks. Wilderness Lore: 5 ranks.", 179),
    ("Fiend Binder", "d8",
     "Alignment: Any evil. Feats: Iron Will. Race: Orc or half-orc. Animal Empathy: 8 ranks. Intimidate: 4 ranks. Spellcasting: Ability to cast summon monster I or summon nature's ally I.", 181),
    ("Prairie Runner", "d8",
     "Feats: Endurance, Run. Race: Halfling. Intuit Direction: 4 ranks. Wilderness Lore: 8 ranks. Special: Must spend three days alone on the prairie.", 182),
    # Elder Druid (Dragon 286)
    ("Elder Druid", "d4",
     "Alignment: Any nonevil. Knowledge (arcana): 10 ranks. Knowledge (history): 5 ranks. Feats: Skill Focus (Knowledge [history]). Spellcasting: Must be able to cast spells. Special: Must be nominated and trained by another Elder Druid and forsake all other loyalties to any political power, nation, or deity.", 186),

    # --- Magic ----------------------------------------------------------
    # The Mystic (Dragon 274)
    ("The Mystic", "d6",
     "Spellcraft: 10 ranks. Knowledge (arcana): 10 ranks. Knowledge (religion): 5 ranks. Feats: Spell Penetration, Spell Focus, one metamagic feat, and one item creation feat.", 187),
    # Arcane Weather (Dragon 308)
    ("Aeromancer", "d4",
     "Knowledge (arcana): 14 ranks. Knowledge (nature): 5 ranks. Feats: Any two metamagic feats. Special: Access to and ability to cast gust of wind and control weather.", 194),
    # Eldritch Master (Dragon 280)
    ("Eldritch Master", "d4",
     "Knowledge (arcana): 8 ranks. Spellcraft: 6 ranks. Diplomacy: 2 ranks. Intimidate: 2 ranks. Spellcasting: Must be able to cast arcane spells. Special: Must have made a pact or bargain with some powerful, otherworldly entity.", 197),
    # Shaper of Form (Dragon 326)
    ("Shaper of Form", "d6",
     "Skills: Craft (alchemy) 5 ranks, Craft (any other) 8 ranks, Knowledge (arcana) 5 ranks. Feats: Great Fortitude, Spell Focus (transmutation). Spells: Ability to cast six spells from the transmutation school. Special: Must have been contacted by the spirits of form.", 198),
    # Force Missile Mage (Dragon 328)
    ("Force Missile Mage", "d4",
     "Skills: Concentration 9 ranks, Spellcraft 9 ranks. Feat: Combat Casting. Spells: Ability to cast magic missile once per day.", 202),
    # Channeling the Elements (Dragon 314) — 4 elemental PrCs
    ("Earthshaker", "d8",
     "Knowledge (dungeoneering): 6 ranks. Knowledge (nature): 12 ranks. Spells: Ability to cast soften earth and stone. Language: Terran.", 206),
    ("Icesinger", "d6",
     "Alignment: Any non-good. Concentration: 9 ranks. Perform (any one): 9 ranks. Feats: Iron Will plus either Skill Focus (Concentration) or Skill Focus (Perform [any]). Special: Bardic music ability.", 207),
    ("Firestorm Berserker", "d12",
     "Alignment: Any chaotic. Base Attack Bonus: +8. Intimidate: 6 ranks. Feats: Iron Will, Great Fortitude, Toughness. Special: Rage 3 times/day.", 208),
    ("Purebreath Devotee", "d8",
     "Base Attack Bonus: +5. Knowledge (nature): 4 ranks. Feats: Endurance, Iron Will. Special: Must go three days without eating, drinking, or using magic items that prevent hunger or thirst.", 210),
    # Flamesteward (Dragon 283)
    ("Flame Steward", "d8",
     "Alignment: Any non-evil. Heal: 8 ranks. Knowledge (religion): 5 ranks. Knowledge (arcana): 5 ranks. Feats: Endurance, Power Attack.", 212),
    # Darkwater Knight (Dragon 314)
    ("Darkwater Knight", "d6",
     "Patron Deity: Any nature deity. Knowledge (nature): 6 ranks. Survival: 6 ranks. Swim: 6 ranks. Feats: Skill Focus (Swim), Water Focus. Language: Aquan. Spells: Ability to cast at least three spells with the Water descriptor (one of at least 2nd level).", 215),
    # The Master Astrologer (Dragon 340)
    ("Master Astrologer", "d4",
     "Skills: Knowledge (the planes) 4 ranks, Sense Motive 4 ranks, Profession (astrologer) 8 ranks. Feats: Skill Focus (Profession [astrologer]). Spells: Able to prepare spells.", 219),
    # Rage Mage (Dragon 277)
    ("Rage Mage", "d6",
     "Alignment: Any non-lawful. Base Attack: +5. Feat: Combat Casting. Special Ability: Rage. Note: Must be able to cast at least 1st-level arcane spells.", 224),
    # Psi-Hunter (Dragon 281)
    ("Psi-Hunter", "d8",
     "Base Attack Bonus: +5. Knowledge (psionics): 3 ranks. Feats: Track, Iron Will. Spellcasting: Must be able to cast arcane spells.", 227),

    # --- Psionics -------------------------------------------------------
    # The Splintered Mind (Dragon 281)
    ("Truth Seeker", "d8",
     "Alignment: Any non-evil. Base Attack: +5. Feats: Improved Unarmed Strike, Combat Reflexes, Dual Strike. Skills: Diplomacy 8 ranks, Sense Motive 4 ranks.", 230),
    # Hidden Teachings of the Githzerai (Dragon 323) — githzerai monasteries
    ("Zerth Cenobite", "d8",
     "Base Attack Bonus: +4. Knowledge (the planes): 8 ranks. Feats: Improved Unarmed Strike, Deflect Arrows, Dodge, Mobility. Alignment: Any lawful. Special: Must find the Monastery of Zerth'Ad'Lun, be accepted by the sensei, and complete a unique trial.", 238),
    ("Arcanopath Monk", "d8",
     "Base Attack Bonus: +4. Knowledge (arcana): 8 ranks. Feats: Improved Unarmed Strike, Deflect Arrows, Dodge, Mobility. Alignment: Any lawful. Special: Must find the Monastery of Finithamon, be accepted by the sensei, and have slain an arcane spellcaster.", 240),
    # Spirit Speaker (Dragon 323)
    ("Spirit Speaker", "d8",
     "Base Attack Bonus: +4. Base Will Save: +2. Skills: Diplomacy 3 ranks, Knowledge (arcana) 1 rank, Knowledge (nature) 1 rank.", 244),

    # --- Bards and Charlatans -------------------------------------------
    # Master of the Secret Sound (Dragon 297)
    ("Master of the Secret Sound", "d6",
     "Knowledge (arcana): 5 ranks. Listen: 5 ranks. Perform: 8 ranks. Spellcraft: 5 ranks. Feats: Alertness. Spellcasting: Must be able to cast 5th-level spells, five of which are sonic or language-dependent. Special: Must undergo a secret ritual each new level.", 246),
    # Musical Masters (Dragon 311) — bard PrCs
    ("Worldspeaker", "d6",
     "Concentration: 8 ranks. Decipher Script: 8 ranks. Knowledge (history): 4 ranks. Knowledge (nature): 4 ranks. Special: Must speak, read, and write three languages not on the character's racial bonus-language list.", 249),
    ("Mourner", "d6",
     "Diplomacy: 8 ranks. Knowledge (religion): 5 ranks. Perform: 8 ranks. Special: Must have the bardic music ability.", 250),
    ("Memory Smith", "d8",
     "Alignment: Any good. Craft (weaponsmithing or armorsmithing): 5 ranks. Knowledge (religion): 3 ranks. Perform: 8 ranks. Use Magic Device: 5 ranks. Patron Deity: Must worship Moradin above all other gods.", 251),
    ("Battle Howler of Gruumsh", "d8",
     "Alignment: Any chaotic. Knowledge (religion): 2 ranks. Perform: 8 ranks. Feats: Cleave, Power Attack. Patron Deity: Must worship Gruumsh above all other gods.", 252),
    ("Green Whisperer", "d6",
     "Alignment: Any neutral. Knowledge (nature): 8 ranks. Perform: 8 ranks. Survival: 5 ranks.", 253),
    # Charlatan (Dragon 335)
    ("Charlatan", "d6",
     "Skills: Bluff 8 ranks, Knowledge (arcana) 2 ranks or Knowledge (religion) 2 ranks, Perform (act) 4 ranks, Spellcraft 2 ranks. Feat: Skill Focus (Bluff).", 255),
    # Jester (Dragon 330)
    ("Jester", "d6",
     "Perform (comedy): 13 ranks. Perform (any other): 13 ranks. Bluff: 6 ranks.", 260),

    # --- Good -----------------------------------------------------------
    # Aerial Avenger (Dragon 319)
    ("Aerial Avenger", "d8",
     "Base Reflex Save: +3. Skills: Tumble 5 ranks. Feats: Dodge, Mobility. Special: Must have a fly speed or the ability to cast fly at least twice per day.", 264),
    # The Infused (Dragon 321) — celestial-bonded (two paths)
    ("The Infused", "d12 (warrior) / d8 (spellcaster)",
     "Base Attack Bonus: +4. Base Will Save: +2. Alignment: Any (cannot advance while evil). Special: Must share her soul with the personality of a particular celestial. Two paths (Infused Warrior / Infused Spellcaster) with identical requirements.", 267),
    # Cultists of Good Monsters (Dragon 307)
    ("Whitehorn", "d10",
     "Alignment: Chaotic good. Gender: Female. Ride: 8 ranks. Feats: Mounted Combat. Special: Must have ridden a unicorn at some time in her life.", 276),
    ("Follower of the Skyserpent", "d8",
     "Alignment: Lawful good. Concentration: 8 ranks. Sense Motive: 8 ranks. Spellcraft: 8 ranks. Spellcasting: Ability to cast 2nd-level arcane or divine spells. Special: Must have caught a villain red-handed, defeated him unaided, and received the blessing of a couatl.", 277),
    ("Tree-Friend", "d10",
     "Alignment: Chaotic good, chaotic neutral, or neutral good. Wilderness Lore: 8 ranks. Knowledge (nature): 8 ranks. Special: Must have saved a dryad's bound tree from destruction or corruption.", 277),
    ("Artist's Vengeance", "d8",
     "Alignment: Chaotic good. Perform: 8 ranks. Intimidate: 8 ranks. Class Feature: Bardic music ability. Special: The candidate's art must have been attacked, unfairly critiqued, or destroyed by another force.", 279),
    # The Justicar (Dragon 290)
    ("Justicar", "d10",
     "Alignment: Any lawful. Base Attack Bonus: +6. Feats: Track, Skill Focus (Gather Information). Wilderness Lore: 5 ranks. Gather Information: 5 ranks. Search: 5 ranks.", 281),
    # Sworn Slayer (Dragon 324)
    ("Sworn Slayer", "d10",
     "Base Attack Bonus: +6. Skills: Knowledge (appropriate to the chosen creature type) 4 ranks, Sense Motive 4 ranks. Special: Must swear a vow to destroy all creatures of a chosen kind in response to a great loss suffered at their claws.", 288),
    # Darkwood Stalker (Dragon 292)
    ("Darkwood Stalker", "d8",
     "Base Attack Bonus: +5. Feats: Dodge, Track. Race: Elf or half-elf. Hide: 5 ranks. Listen: 5 ranks. Move Silently: 5 ranks. Spot: 5 ranks. Wilderness Lore: 5 ranks. Speak Language: Orc.", 291),
    # Guardians of the Docrae (Dragon 315) — Blackmoor
    ("Omatu Master", "d8",
     "Race: Halfling. Base Attack Bonus: +4. Skill: Perform (dance) 2 ranks. Feats: Improved Trip, Improved Unarmed Strike, Skill Focus (Tumble), Stunning Fist. Special: Must have fought a Medium or larger opponent using only unarmed strikes and take an oath to protect the Docrae community.", 293),
    # Hunter of the Dead (Dragon 276)
    ("Hunter of the Dead", "d8",
     "Alignment: Any non-evil. Base Attack: +5. Knowledge (undead): 5 ranks. Special Ability: Must be able to turn undead. Special: Must have lost one level or ability score point to the draining power of the undead.", 295),
    # Luminaire / Masque of the Red Death (Dragon 315)
    ("Luminaire", "d8",
     "Alignment: Chaotic good. Base Attack Bonus: +3. Diplomacy: 4 ranks. Knowledge (any one): 7 ranks. Feats: Combat Expertise. Special: Must be a member of La Lumiere.", 298),
    # Dragon Hunters (Dragon 296) — 4 dragon-slaying PrCs
    ("Dragonscribe", "d4",
     "Diplomacy: 7 ranks. Knowledge (arcana): 13 ranks. Feats: Spell Penetration, Iron Will. Language: Draconic. Special: Must have personally observed at least three different kinds of dragons and be able to cast a 2nd-level or higher arcane spell from the Abjuration, Conjuration, and Divination schools.", 300),
    ("Knight of the Scale", "d10",
     "Alignment: Any good. Base Attack Bonus: +6. Knowledge (arcana): 4 ranks. Ride: 9 ranks. Feats: Mounted Combat, Weapon Focus (lance, heavy). Special: Must have killed a young adult or older dragon and commissioned armor made from its scales.", 302),
    ("Heartseeker", "d6",
     "Base Attack Bonus: +4. Concentration: 8 ranks. Knowledge (arcana): 8 ranks. Listen: 5 ranks. Spot: 5 ranks. Feats: Combat Casting, Spell Penetration, Weapon Focus (any bow). Spellcasting: Ability to cast arcane spells.", 305),
    ("Vengeance Sworn", "d10",
     "Base Attack Bonus: +6. Intimidate: 5 ranks. Knowledge (arcana): 5 ranks. Wilderness Lore: 5 ranks. Feats: Ambidexterity, Two-Weapon Fighting, Expertise. Special Ability: Rage. Spellcasting: Ability to cast 1st-level divine spells. Special: Must have been killed by a dragon or had a loved one killed by a dragon.", 305),
    # Wormhunter (Dragon 338)
    ("Wormhunter", "d8",
     "Special: Must meet at least two of the following five criteria - base attack bonus +7; able to cast 4th-level divine spells; Knowledge (religion) 10 ranks; base Fortitude save +4; sneak attack +4d6. Special: Must have read through a copy of the Apostolic Scrolls.", 307),
    # Dragonkith (Dragon 284)
    ("Dragonkith", "d8",
     "Language: Draconic. Base Attack Bonus: +6. Knowledge (arcana): 4 ranks. Feats: Alertness, Endurance. Special: Must be chosen by a dragon of the same alignment (loses all class abilities if the bond ends or the dragon dies).", 311),

    # --- Evil -----------------------------------------------------------
    # The Minions of Darkness / Monster Cult PrCs (Dragon 300)
    ("Faceless One", "d8",
     "Race: Any humanoid or monstrous humanoid. Alignment: Any evil. Bluff: 8 ranks. Disguise: 8 ranks. Spells: Must be able to cast alter self. Special: Must be accepted into the cult of the Faceless Ones and pass himself off as a person of importance for at least three days without magic.", 312),
    ("Deep Thrall", "d10",
     "Alignment: Neutral evil. Race: Any humanoid or monstrous humanoid. Sense Motive: 5 ranks. Swim: 8 ranks. Language: Aquan. Special: Must make friendly contact with a kraken (or be its slave) and accept being scarred by its tentacle.", 314),
    ("Shoal Servant", "d8",
     "Alignment: Neutral evil. Base Attack Bonus: +5. Feats: Great Fortitude. Patron: Blibdoolpoolp. Race: Any humanoid. Spellcasting: Must be able to cast divine spells. Special: Must stand at the seashore through three tides and be blessed by a kuo-toan cleric.", 316),
    ("Tiger Mask", "d8",
     "Alignment: Lawful evil. Race: Any non-monstrous humanoid. Diplomacy: 5 ranks. Gather Information: 8 ranks. Language: Infernal. Spellcasting: Must be able to cast 2nd-level spells. Special: Must make friendly contact with a rakshasa and undergo a scarring ritual.", 318),
    # Monster Cultist PrCs (Dragon 296)
    ("Sphere Minion", "d6",
     "Race: Any humanoid or monstrous humanoid. Alignment: Lawful evil. Patron: The Great Mother. Knowledge (arcana): 8 ranks. Spot: 4 ranks. Feats: Alertness, Weapon Focus (ray).", 322),
    ("Illithidkin", "d6",
     "Race: Any humanoid or monstrous humanoid. Alignment: Lawful evil. Patron: Ilsensine. Concentration: 8 ranks. Knowledge (psionics): 8 ranks. Special: Must willingly consume the brain of a sentient creature.", 323),
    ("Snake Servant", "d8",
     "Race: Any humanoid or monstrous humanoid. Alignment: Lawful evil. Patron: Shekenster. Base Attack Bonus: +5. Bluff: 5 ranks. Disguise: 5 ranks. Special: Must undergo a ceremony in which a medusa poisons him until his Strength is reduced to 0.", 324),
    ("Waker of the Beast", "d12",
     "Race: Any humanoid or monstrous humanoid. Alignment: Any evil. Base Attack Bonus: +7. Feats: Power Attack, Toughness.", 325),
    # Flesheater (Dragon 300)
    ("Flesheater", "d8",
     "Race: Halfling. Alignment: Chaotic evil. Move Silently: 8 ranks. Hide: 8 ranks. Feats: Evil Brand, Willing Deformity, Improved Unarmed Strike. Special: Must have all of their teeth sharpened to points.", 328),
    # Life Drinker (Dragon 288)
    ("Lifedrinker", "d12",
     "Alignment: Any evil. Knowledge (arcana): 6 ranks. Spellcraft: 6 ranks. Special: Must have the vampire template.", 329),
    # The Tainted (Dragon 302) — fiend-bonded (two paths)
    ("The Tainted", "d10 (warrior) / d6 (spellcaster)",
     "Alignment: Any nonevil. Base Attack Bonus: +2. Base Will Save: +1. Special: Must share his soul with the personality of a particular fiend. Two paths (Tainted Warrior / Tainted Spellcaster) with identical requirements.", 332),
    # Body of Knowledge (Dragon 317) — Osteomancer / Flux Adept / Cerebrex
    ("Osteomancer", "d8",
     "Spellcasting: Ability to cast at least five transmutation spells, one of which is 3rd-level or higher. Skills: Heal 4 ranks, Knowledge (arcana) 4 ranks, Knowledge (nature) 4 ranks. Feat: Toughness.", 341),
    ("Flux Adept", "d6",
     "Spellcasting: Ability to cast 2nd-level spells. Skills: Heal 5 ranks, Knowledge (arcana) 7 ranks. Feats: At least one metamagic feat, Endurance, Great Fortitude.", 344),
    ("Cerebrex", "d4",
     "Spellcasting: Ability to cast 3rd-level arcane spells. Skills: Concentration 8 ranks, Craft (alchemy) 4 ranks, Knowledge (arcana) 8 ranks, Spellcraft 8 ranks.", 346),

    # --- From Games -----------------------------------------------------
    # Warcraft III (Dragon 299)
    ("Dwarven Thane", "d10",
     "Race: Dwarf. Base Attack Bonus: +6. Feats: Ambidexterity, Power Attack, Two-Weapon Fighting, Weapon Focus (any axe), Weapon Focus (any hammer). Knowledge (religion): 5 ranks. Special: Must be a devout follower of a dwarven deity or of earth spirits.", 349),
    ("Orc Blademaster", "d8",
     "Race: Orc or half-orc. Base Attack Bonus: +6. Knowledge (religion): 5 ranks. Feats: Dodge, Exotic Weapon Proficiency (bastard sword), Mobility, Spring Attack, Expertise.", 350),
    # Battle Realms (Dragon 298)
    ("Kabuki Warrior", "d10",
     "Base Attack Bonus: +5 or better. Bluff: 5 ranks. Perform: 5 ranks. Tumble: 3 ranks. Feats: Dodge, Expertise, Mobility, Spring Attack. Special: The ability to cast three Illusion spells.", 353),
    ("Dragon Warrior", "d10",
     "Alignment: Any nonchaotic, nonlawful (loses all class abilities if she becomes lawful or chaotic). Base Attack Bonus: +6 or better. Concentration: 3 ranks. Knowledge (religion): 3 ranks. Feats: Iron Will, Toughness, Weapon Focus (greatsword).", 355),
]


@dataclass
class PrestigeClass:
    name: str
    book: str
    hit_die: Optional[str]
    requirements: Optional[str]
    citation: str
    page: int


def build() -> List[PrestigeClass]:
    out: List[PrestigeClass] = []
    seen = set()
    for name, hd, req, page in _T:
        key = name.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(PrestigeClass(
            name=name, book=BOOK,
            hit_die=(hd or None),
            requirements=(req.strip() or None) if req else None,
            citation=CITATION, page=page))
    return out


def write_index() -> int:
    prcs = build()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    by_hd = Counter(p.hit_die or "?" for p in prcs)
    md: List[str] = [
        "# PRESTIGE CLASS INDEX — The New Path",
        "",
        "**Generated by `scripts/prestige_class_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** D&D 3.0/3.5 prestige classes from the **Dragon",
        "Magazine Prestige Class Compendium (Issues 274-353)** — a compilation of",
        "the prestige classes published in Dragon Magazine #274-353.",
        "**Vision-transcribed from the PDF page images** (321 of 355 pages are",
        "image-only and the rest carry corrupt OCR) — still book RAW, read off the",
        "page. The `requirements` field is each class's prerequisite block, the",
        "qualifying mechanic a translator needs; the full class-feature text lives",
        "at the class's page in the compendium. `page` is the PDF page.",
        "",
        f"*{len(prcs)} prestige classes — Hit Die: " +
        ", ".join(f"{n}x {hd}" for hd, n in sorted(by_hd.items())) + ".*",
        "",
        "| Prestige Class | Hit Die | Requirements | Page |",
        "|---|---|---|---|",
    ]
    for p in sorted(prcs, key=lambda x: x.page):
        req = (p.requirements or "-").replace("|", "\\|")
        md.append(f"| {p.name} | {p.hit_die or '-'} | {req} | {p.page} |")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/prestige_class_harvest.py",
                    "book": BOOK, "citation": CITATION,
                    "note": ("Vision-transcribed from the compendium PDF page "
                             "images (image-only / corrupt-OCR source). Book "
                             "RAW, read off the page. `page` is the PDF page."),
                    "total_prestige_classes": len(prcs),
                    "by_hit_die": dict(by_hd),
                    "prestige_classes": [asdict(p) for p in prcs]}, indent=1),
        encoding="utf-8")
    return len(prcs)


def selftest() -> int:
    failures: List[str] = []
    prcs = build()
    if len(prcs) <= 15:
        failures.append(f"only {len(prcs)} prestige classes; expected > 15")
    names = {p.name for p in prcs}
    # a spread of specific PrCs transcribed from across the compendium
    for probe in ("Bloodsister", "Ancestral Avenger", "Radiant Servant of Pelor",
                  "Deathstalker of Bhaal", "Dragonmark Heir", "Osteomancer",
                  "Kabuki Warrior", "Shen (Tiger)", "The Tainted", "Duelist"):
        if probe not in names:
            failures.append(f"missing prestige class '{probe}'")
    # every entry must carry a non-empty requirements string and a page cite
    for p in prcs:
        if not p.requirements or not p.requirements.strip():
            failures.append(f"{p.name}: empty requirements")
        if not isinstance(p.page, int) or p.page < 1:
            failures.append(f"{p.name}: bad page {p.page!r}")
    # spot-check a couple of transcriptions
    bs = next((p for p in prcs if p.name == "Bloodsister"), None)
    if bs and (bs.hit_die != "d10" or "Drow" not in (bs.requirements or "")
               or "Female" not in (bs.requirements or "")):
        failures.append(f"Bloodsister transcription looks wrong: {bs.hit_die} / {bs.requirements!r}")
    rs = next((p for p in prcs if p.name == "Radiant Servant of Pelor"), None)
    if rs and "Pelor" not in (rs.requirements or ""):
        failures.append(f"Radiant Servant of Pelor missing Pelor in reqs: {rs.requirements!r}")
    if len({p.name.lower() for p in prcs}) != len(prcs):
        failures.append("duplicate prestige-class names")
    # hit dice all look like dNN (allow the two dual-path descriptors)
    for p in prcs:
        hd = (p.hit_die or "")
        if not hd.startswith("d"):
            failures.append(f"{p.name}: hit_die not a die '{hd}'")
    for f in failures:
        print(f"SELFTEST FAIL: {f}")
    print("selftest: " + ("PASS" if not failures else f"{len(failures)} failure(s)"))
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--search", metavar="TEXT",
                    help="print prestige classes whose name or requirements match TEXT")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if args.search:
        q = args.search.lower()
        hits = [p for p in build()
                if q in p.name.lower() or q in (p.requirements or "").lower()]
        for p in sorted(hits, key=lambda x: x.name):
            print(f"  {p.name} [{p.hit_die or '-'}] — {p.requirements or '-'} [p.{p.page}]")
        print(f"{len(hits)} match(es).")
        return 0 if hits else 1

    n = write_index()
    print(f"{n} D&D 3.x prestige classes "
          f"(Dragon Magazine Prestige Class Compendium #274-353, vision-transcribed).")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
