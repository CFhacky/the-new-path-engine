# WARHAMMER DWARF WEAPON RUNE COMPENDIUM
**Corpus Mass Translation — Warhammer Fantasy Dwarf weapon runes (Warhammer Armies: Dwarfs, unofficial 9th-edition compilation, PDF Room scan, pp. 201-203). Built 2026-10-04.**

## HOW TO USE / TIER OVERVIEW
Each entry: the source tooltip as fetched, the 3.5e rules, the GURPS crosswalk, price, pool coverage, collisions and forks. Rate card and rules: Crusader (Affix Registry section 2) and `docs/translation/FUSED_ENGINE_RESOLUTION.md`. Conventions used throughout: 1 / 2 / 3 copies of a rune = the Crusader rungs (Magic +1, Rare +2, Unique +3); +1 WS = +1 attack, +1 S = +2 Strength, armour-save modifiers = ignored DR, Multiple Wounds = extra weapon-damage rolls, Killing Blow = a Lethal-severity crit result on a confirmed natural 20; master runes are single-rung; the Rules of the Runes carry over; price = bonus-equivalent squared x 2,000 gp. `Registered` means indexed here; a Notion Registry family entry is written when an affix is first rolled or placed. Only the 21 weapon runes are here; armour, talismanic, banner and engineering runes are not weapon enchants, and WFRP runic weapons (Old World Armoury) were not read in this pass. The source is an unofficial compilation, not a Games Workshop product.

| Tier | Registered |
|---|---:|
| 2 Heroic Elite | 10 |
| 3 Heroic | 6 |
| 4 Competent | 3 |

## TIER 2 — HEROIC ELITE (LEVELS 13-16)

### MASTER RUNE OF ALARIC THE MAD
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 201))**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `wow_pipeline.py`; price +3 = 18,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 201)
tooltip: "A weapon engraved with the Master Rune of Alaric the Mad has the Ignores Armour Saves special rule."
facts: cost 40 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
The weapon's attacks ignore armor and shield bonuses to AC (including enhancement bonuses to that armor) and ignore worn DR (the engine's ignores-armor flag). Natural armor, Dex, dodge and deflection still apply. Unlike Brilliant Energy it harms undead, constructs and objects normally. Always on. Master rune: one per item and per army.

## GURPS 4e
The weapon's attacks skip worn DR (ignores_armor flag); the defender's 3d6 active defenses are unchanged.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+3 = 18,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Brilliant Energy (DMG, weapon-affix corpus) / Armor Piercing (Offensive 19-24).

## NAME COLLISION
DMG Brilliant Energy (+4, also passes through nonliving matter); different reach, names stay.

## FORKS NEEDING A RULING
1. 'Ignores Armour Saves' is read as ignore armor and shield AC plus worn DR; natural toughness stays.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.


---

### MASTER RUNE OF DEATH
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 201))**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `wow_pipeline.py`; price +3 = 18,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 201)
tooltip: "A weapon engraved with the Master Rune of Death grants its wielder the Heroic Killing Blow special rule."
facts: cost 40 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
Heroic Killing Blow: on a confirmed natural 20 the engine forces a Lethal-severity result on the location table (the same table as the Vorpal ruling), against a target of any size. Not a death effect and no separate save. Master rune.

## GURPS 4e
On a confirmed critical hit, the same Lethal-severity location result; no size limit.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+3 = 18,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Vorpal (DMG, weapon-affix corpus ruling).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Vorpal forces the Head; this rune forces Lethal severity on the rolled location (less reliable, reflecting the lower cost), per the engine's crit table.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.


---

### MASTER RUNE OF DRAGON SLAYING
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 201))**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `wow_pipeline.py`; price +3 = 18,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 201)
tooltip: "Against Dragons and Drakes, a weapon engraved with the Master Rune of Dragon Slaying will always wound on a To Wound roll of 2+ and has the Multiple Wounds (2) special rule."
facts: cost 40 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
Against creatures of the dragon type (including drakes and wyrms): the weapon acts as a bane weapon (+2 effective enhancement bonus and +2d6 damage) and every damaging hit adds one extra roll of the weapon's damage dice (Multiple Wounds (2)). Master rune.

## GURPS 4e
Innate Attack (Bane) 2d Follow-Up against dragons, and the injury is doubled (a second damage roll).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+3 = 18,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Bane (DMG, weapon-affix corpus).

## NAME COLLISION
DMG Bane and WoW Demonslaying (type-slaying family); names stay.

## FORKS NEEDING A RULING
1. 'Always wounds on a 2+' has no 3.5e roll; it is carried by the bane attack bonus.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.


---

### MASTER RUNE OF SMITING
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 201))**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `wow_pipeline.py`; price +3 = 18,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 201)
tooltip: "A weapon engraved with the Master Rune of Smiting has the Multiple Wounds (D6) special rule."
facts: cost 40 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
Multiple Wounds (D6): every damaging hit adds one extra roll of the weapon's damage dice (dice only: no Strength, no extra dice, not multiplied on a critical hit). Master rune.

## GURPS 4e
Each damaging hit's injury is rolled twice (the second roll the weapon dice only).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+3 = 18,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Multiple Wounds (D6) averages 3.5 wounds on the tabletop; one extra damage roll is the 3.5e reading because 3.5e damage already scales with dice. A GM wanting more can step this to 1d3 extra rolls at a higher price.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.


---

### RUNE OF CLEAVING
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 203))**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `wow_pipeline.py`; price +1 / +2 / +3 = 2,000 / 8,000 / 18,000 gp by rune count (Magic / Rare / Unique))

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 203)
tooltip: "One Rune of Cleaving: the Armour Piercing (1) special rule. Two Runes: Armour Piercing (1) and +1 Strength. Three Runes: Armour Piercing (1), +1 Strength and the Killing Blow special rule."
facts: cost 10/30/50 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
1 rune: the weapon ignores 2 points of DR (Armour Piercing (1)). 2 runes: also +2 Strength (untyped, one WFB Strength step) while wielded. 3 runes: also Killing Blow: the threat range widens by one step and a confirmed natural 20 against a same-size or smaller target forces a Lethal-severity location result.

## GURPS 4e
Armor Divisor (2) at 1 rune; ST +1 at 2 runes; at 3 runes the same Lethal-severity crit result against same-size targets.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 / +2 / +3 = 2,000 / 8,000 / 18,000 gp by rune count (Magic / Rare / Unique) (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Armor Piercing (Offensive 19-24).

## NAME COLLISION
Mighty Cleaving (DMG, the Cleave feat extension) is unrelated.

## FORKS NEEDING A RULING
1. Armour Piercing (1) is read as ignoring 2 DR.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.


---

### RUNE OF DAEMON SLAYING
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 202))**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `wow_pipeline.py`; price +1 / +2 / +3 = 2,000 / 8,000 / 18,000 gp by rune count (Magic / Rare / Unique))

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 202)
tooltip: "Against any model with the Daemonic special rule, a weapon engraved with a Rune of Daemon Slaying receives a +1 bonus To Hit and To Wound. With two Runes: +1 To Hit and To Wound and the Multiple Wounds (D3) special rule. With three Runes: hits and Wounds on a roll of 2+, has Multiple Wounds (D3) and no ward saves can be taken against it."
facts: cost 25/50/100 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
Against creatures with the demon, devil or daemon subtype (the Daemonic rule). 1 rune: +1 effective enhancement bonus and +1d6 damage. 2 runes: +2 effective enhancement, +2d6, and one extra roll of the weapon's damage dice on a damaging hit (Multiple Wounds (D3), read as one extra roll). 3 runes: hits on a natural 2 or higher, +4d6, one extra damage roll, and the target's SR, ward and deflection bonuses do not apply (no ward saves).

## GURPS 4e
Innate Attack (Bane) 1d / 2d / 4d against daemons, with the extra injury roll at 2 and 3 runes; at 3 runes no ward or Magic Resistance applies.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 / +2 / +3 = 2,000 / 8,000 / 18,000 gp by rune count (Magic / Rare / Unique) (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Banefire (Elemental 93-96).

## NAME COLLISION
WoW Demonslaying and Damage vs Demons (D2): names stay.

## FORKS NEEDING A RULING
1. 'Daemonic' read as the demon, devil or daemon subtype; default includes devils.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.


---

### RUNE OF FIRE
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 202))**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `wow_pipeline.py`; price +1 / +2 / +3 = 2,000 / 8,000 / 18,000 gp by rune count (Magic / Rare / Unique))

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 202)
tooltip: "One Rune of Fire: the Flaming Attacks special rule. Two Runes: Flaming Attacks, and grants its wielder a Strength 4 Breath Weapon with the Flaming Attacks special rule. Three Runes: Flaming Attacks and a Strength 4 Breath Weapon that has the Flaming Attacks and Multiple Wounds (D3) special rules."
facts: cost 10/45/75 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
1 rune: Flaming Attacks (the Flaming row's +1d6 fire damage on a hit). 2 runes: also a breath weapon once per encounter, a 15-ft cone of 2d6 fire (Reflex DC 14 half). 3 runes: the breath weapon is 3d6 and the burned target takes one further 1d6 fire damage at the start of its next turn (Multiple Wounds (D3), read as a second damage roll).

## GURPS 4e
Innate Attack Burning 1d Follow-Up on every damaging hit (1 rune); plus an Innate Attack Burning cone 2d once per encounter (2 runes); 3d plus a second 1d the next second (3 runes).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 / +2 / +3 = 2,000 / 8,000 / 18,000 gp by rune count (Magic / Rare / Unique) (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Flaming (Elemental 01-08) + Elemental Burst (Elemental 75-80).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Strength 4 breath weapon is read as 2d6 / 3d6 by the Elemental Burst Magic and Rare values.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.


---

### RUNE OF FURY
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 203))**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `wow_pipeline.py`; price +1 / +2 / +3 = 2,000 / 8,000 / 18,000 gp by rune count (Magic / Rare / Unique))

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 203)
tooltip: "One Rune of Fury grants its wielder +1 Attack. Two Runes: +1 Attack and the Frenzy special rule. Three Runes: +1 Attack and Frenzy and, after each successful roll To Hit and To Wound, it grants its user another Attack; roll To Hit and To Wound as normal. Attacks generated this way do not generate further Attacks."
facts: cost 15/30/60 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
1 rune: +1 Attack, an extra attack at the highest base attack bonus once per day as a swift action (Rapid Assault T5). 2 runes: three times per day, plus the Frenzy special rule read as rage (+2 Str, -2 AC, must engage) once per encounter. 3 runes: an extra attack at will, rage, and after each hit that deals damage the weapon grants one further attack (the further attacks do not chain).

## GURPS 4e
Altered Time Rate (limited uses 1/day, 3/day, at will matching 3.5e) plus Berserk at 2 and 3 runes.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 / +2 / +3 = 2,000 / 8,000 / 18,000 gp by rune count (Magic / Rare / Unique) (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Rapid Assault (Offensive 25-30).

## NAME COLLISION
DMG Speed (+3, an extra attack on every full attack); different cadence, names stay.

## FORKS NEEDING A RULING
1. '+1 Attack' every round would match DMG Speed; here it follows Rapid Assault's limited-use ladder to keep the price at +1 / +2 / +3.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.


---

### RUNE OF MIGHT
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 203))**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `wow_pipeline.py`; price +2 / +3 = 8,000 / 18,000 gp by rune count (Rare / Unique))

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 203)
tooltip: "One Rune of Might doubles its wielder's Strength against foes of Toughness 5 or higher in close combat. Two Runes: the previous effect and the Multiple Wounds (D3) special rule against foes of Toughness 5 or higher in close combat. A third Rune has no further effect."
facts: cost 30/40 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
1 rune (Rare): against creatures of Large size or larger (the source's Toughness 5 or higher) the wielder's Strength bonus to damage is doubled. 2 runes (Unique): also one extra roll of the weapon's damage dice on a damaging hit against them (Multiple Wounds (D3), read as one extra roll). A third rune has no further effect.

## GURPS 4e
Striking ST x2 on damage against SM +1 or larger; second damage roll at 2 runes.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 / +3 = 8,000 / 18,000 gp by rune count (Rare / Unique) (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Toughness 5 or higher is read as Large or larger.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.


---

### RUNE OF STRIKING
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 203))**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `wow_pipeline.py`; price +1 / +2 / +3 = 2,000 / 8,000 / 18,000 gp by rune count (Magic / Rare / Unique))

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 203)
tooltip: "One Rune of Striking grants its wielder +1 Weapon Skill. Two Runes: +1 Weapon Skill and the wielder may re-roll failed To Hit rolls in close combat. Three Runes: Weapon Skill 10 and re-roll failed To Hit rolls in close combat."
facts: cost 10/35/50 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
1 rune: +1 attack bonus (one WFB Weapon Skill step, the Striking row). 2 runes: +2 attack bonus and once per round the wielder may reroll one missed attack. 3 runes: +4 attack bonus and the reroll (the source's Weapon Skill 10).

## GURPS 4e
Weapon Bond +1 / +2 / +4 to weapon skill, with a reroll of one missed attack per second at 2 and 3 runes.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 / +2 / +3 = 2,000 / 8,000 / 18,000 gp by rune count (Magic / Rare / Unique) (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Striking (Offensive 01-06).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Weapon Skill 10 is capped at +4 attack rather than the +26 the profile table would give.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.


---

## TIER 3 — HEROIC (LEVELS 9-12)

### MASTER RUNE OF BREAKING
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 201))**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 201)
tooltip: "If a Dwarf with a weapon engraved with the Master Rune of Breaking scores one or more successful hits against a model with a magic weapon, the foe's magic weapon is destroyed on a D6 roll of 2+ (roll once, regardless of the number of successful hits). A foe with a destroyed magic weapon counts as being armed with a hand weapon. If the foe has more than one magic weapon (Paired weapons count as one), roll a D6 to randomly determine which one is destroyed."
facts: cost 25 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
On a damaging hit against a creature wielding a magic weapon, that weapon must succeed on a Fortitude save (the owner's save bonus, DC 20) or be destroyed; one check per round. A creature with several magic weapons risks one at random. Artifacts are immune. A creature whose weapon is destroyed is armed with an ordinary weapon of the same kind. Master rune.

## GURPS 4e
On the same hit: Quick Contest of the weapon owner's HT against effective skill 20; on failure the weapon breaks.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
Sunder (a combat maneuver) and MIC Sundering (extra damage on sunder): different, names stay.

## FORKS NEEDING A RULING
1. 'D6 roll of 2+' (about 83%) is replaced by a DC 20 save so a well-built weapon can resist. 2. Default applies to NPC weapons; whether it can break a PC's magic weapon is a GM call (default: yes, with the save).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.


---

### MASTER RUNE OF FLIGHT
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 202))**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp (Throwing +1 and Returning +1))

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 202)
tooltip: "A weapon engraved with the Master Rune of Flight can be thrown like a throwing weapon with a range of up to 12" which always hits on a roll of 2+. Roll To Wound as if the target had suffered a hit from the weapon in close combat. Any additional runes on the weapon will also take effect. After this, the weapon flies back to the wielder. A weapon with the Master Rune of Flight can also be used in close combat as normal."
facts: cost 20 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
The weapon can be thrown with a 20-ft range increment, hits on any natural 2 or higher, and returns to the wielder's hand (Throwing +1 and Returning +1). Any other runes take effect on the thrown hit. It can still be used in melee.

## GURPS 4e
Throwing range ST x 1; the thrown attack succeeds on any roll of skill 16 or better; the weapon returns to the hand.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (Throwing +1 and Returning +1) (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Throwing + Returning (DMG, weapon-affix corpus).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. 12" is read as a 20-ft increment (two increments to about 40 ft).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.


---

### MASTER RUNE OF SKALF BLACKHAMMER
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 201))**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 201)
tooltip: "A weapon engraved with the Master Rune of Skalf Blackhammer will Wound any model not in magic armour on a To Wound roll of 2+, regardless of the target's Toughness. Against models in magic armour, a roll of 3+ is required."
facts: cost 30 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
The weapon ignores the target's DR/X and natural armor bonus unless the target wears magic armor; against a target in magic armor it ignores DR/X only. Master rune.

## GURPS 4e
The weapon's attacks ignore natural DR (and worn DR on a target in nonmagical armor); against magic armor, ignore natural DR only.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. 'Wound on 2+ regardless of Toughness' is read as ignoring DR/X and natural armor.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.


---

### MASTER RUNE OF SNORRI SPANGELHELM
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 202))**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 202)
tooltip: "A weapon engraved with the Master Rune of Snorri Spangelhelm always hits on a To Hit roll of 2+."
facts: cost 25 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
The weapon's attack rolls hit on any natural 2 or higher (a natural 1 still misses); a hit is a critical threat only if the roll is within the threat range. Master rune.

## GURPS 4e
The weapon's effective skill is never below 16 for attack rolls; the defender still rolls any active defense.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. 'Hits on 2+' is read as removing AC as an obstacle but keeping the natural-1 miss.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.


---

### MASTER RUNE OF SWIFTNESS
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 202))**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 202)
tooltip: "A weapon engraved with the Master Rune of Swiftness has the Always Strikes First special rule."
facts: cost 25 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
Always Strikes First: in melee the wielder's attacks resolve before any opposing melee attack in every round regardless of initiative order, and he wins ties. Master rune.

## GURPS 4e
The wielder's attacks resolve before any opposing attack in the same second.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. 'Always Strikes First' is a miniatures initiative override; here it is resolution order inside the round, not an initiative bonus.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.


---

### RUNE OF DISMAY
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 203))**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +1 / +2 = 2,000 / 8,000 gp by rune count (Magic / Rare))

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 203)
tooltip: "One Rune of Dismay grants its wielder the Fear special rule. Two Runes grant the Terror special rule. A third Rune has no further effect."
facts: cost 15/25 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
1 rune (Magic): Fear. Each enemy that first attacks the wielder in an encounter must succeed on a Will save (DC 13) or be shaken for 1d4 rounds. 2 runes (Rare): Terror. The save is DC 15 and a failure leaves the enemy frightened for 1d4 rounds. Mindless creatures and creatures of 17+ Hit Dice are immune. A third rune has no further effect.

## GURPS 4e
A Fright Check at -1 (Fear) or -2 (Terror) for each enemy that first attacks the wielder; Terror on failure for 1d4 seconds-rounds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 / +2 = 2,000 / 8,000 gp by rune count (Magic / Rare) (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Terrifying (Condition 25-30).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Fear and Terror are read as the Terrifying row's Will DCs 13 and 15.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.


---

## TIER 4 — COMPETENT (LEVELS 5-8)

### GRUDGE RUNE
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 203))**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 203)
tooltip: "For each Grudge Rune in your army, nominate one enemy character or monster at the beginning of the game. The wielder of a weapon engraved with a Grudge Rune gains +1 To Hit and can re-roll failed To Wound rolls in close combat when attacking the nominated model. Multiples of this rune have no further effect."
facts: cost 20 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
At the start of each encounter the wielder designates one enemy creature as a swift action; against it the wielder gets +1 on attack rolls and may once per round reroll one damage roll and keep the better. One designation per Grudge Rune carried; multiples have no further effect.

## GURPS 4e
Hunter's Mark accessibility (marked target only) with +1 skill and a damage reroll per second against it.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Hunter's Mark (Offensive 55-60).

## NAME COLLISION
Ranger favored enemy and MIC Hunting: different, names stay.

## FORKS NEEDING A RULING
1. 'Nominate at the beginning of the game' is read as at the start of each encounter.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.


---

### MASTER RUNE OF BANISHMENT
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 202))**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 202)
tooltip: "A weapon engraved with the Master Rune of Banishment may re-roll failed To Wound rolls against models with the Ethereal, Undead or Vampiric special rule."
facts: cost 20 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
The weapon functions as ghost touch, and against undead and incorporeal creatures the wielder may once per round reroll one damage roll and keep the better. Master rune.

## GURPS 4e
Affects Insubstantial on all attacks; against undead, one damage reroll per second-turn, take the better.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Ghost Touch (DMG, weapon-affix corpus).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. 'Re-roll failed To Wound' is read as a damage reroll.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.


---

### MASTER RUNE OF KRAGG THE GRIM
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 202))**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 202)
tooltip: "This rune can only be placed on great weapons. It allows the great weapon to be inscribed with runes."
facts: cost 15 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
Utility rune: lets a two-handed weapon (a great weapon) carry runes at all. It has no combat effect and uses one of the item's three rune slots. Master rune.

## GURPS 4e
No GURPS effect; a rules permission only.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Priced +1 (2,000 gp) as a permission, by its 15 WFB points.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.


---

## COVERED BY AN EXISTING REGISTRY ROW (no second document)

| Enchant | Existing row | Note |
|---|---|---|
| Rune of Parrying | Warding (Defensive 01-06) | -1 to enemy To Hit in close combat is a +1 deflection bonus to AC against melee, Warding's T5/T4 value. No new family. |
| Rune of Speed | Predator's Instinct (Offensive 73-78) | +1 Initiative per rune is Predator's Instinct's initiative bonus (+1/+2/+2/+3/+4); stacking per rune matches the row's rungs. |

## OPEN VERIFICATION ITEMS

- Master Rune of Alaric the Mad: forks listed in its entry
- Master Rune of Death: forks listed in its entry
- Master Rune of Dragon Slaying: forks listed in its entry
- Master Rune of Smiting: forks listed in its entry
- Rune of Cleaving: forks listed in its entry
- Rune of Daemon Slaying: forks listed in its entry
- Rune of Fire: forks listed in its entry
- Rune of Fury: forks listed in its entry
- Rune of Might: forks listed in its entry
- Rune of Striking: forks listed in its entry
- Master Rune of Breaking: forks listed in its entry
- Master Rune of Flight: forks listed in its entry
- Master Rune of Skalf Blackhammer: forks listed in its entry
- Master Rune of Snorri Spangelhelm: forks listed in its entry
- Master Rune of Swiftness: forks listed in its entry
- Rune of Dismay: forks listed in its entry
- Grudge Rune: forks listed in its entry
- Master Rune of Banishment: forks listed in its entry
- Master Rune of Kragg the Grim: forks listed in its entry
