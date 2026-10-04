# MIC SPECIFIC WEAPON AND WEAPON CRYSTAL COMPENDIUM
**Corpus Mass Translation — Magic Item Compendium specific weapons and weapon augment crystals (PDF pp. 47-67). Built 2026-10-04.**

## HOW TO USE / TIER OVERVIEW
Each entry: the normalized book text, the 3.5e rules as printed, the GURPS crosswalk, printed price, pool coverage, collisions and forks. Rules: `docs/translation/FUSED_ENGINE_RESOLUTION.md`. Conventions: `mic_translations.py` header (printed save DCs stay fixed, GURPS only contributes the defender contest and DR, crystals priced per rung, relic gating kept as printed). `Registered` means indexed here; a Notion Registry family entry is written when an affix is first rolled or placed. Storm Gauntlets is excluded: its entry text was not in the OCR range read.

| Tier | Registered |
|---|---:|
| 1 Legendary | 3 |
| 2 Heroic Elite | 18 |
| 3 Heroic | 50 |
| 4 Competent | 5 |
| 5 Baseline | 3 |

## TIER 1 — LEGENDARY (LEVELS 17-20)

### EXPLOSIVE SLING
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 1 — Legendary (levels 17-20)** (rule in `mic_pipeline.py`; printed price 36,300 gp (item level 17))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: This +1 sling imbues stones launched from it with an explosive charge. When you hit a target with a stone fired from an explosive sling, the stone explodes, dealing an extra 2d6 points of fire damage to the target (no save). In addition, each other creature within 10 feet of the target when the stone explodes takes 2d6 points of fire damage (Reflex DC 22 negates).
facts: 36,300 gp; item level 17th; caster level 15th; activation —; prerequisites Craft Magic Arms and Armor, fireball
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): This +1 sling imbues stones launched from it with an explosive charge. When you hit a target with a stone fired from an explosive sling, the stone explodes, dealing an extra 2d6 points of fire damage to the target (no save). In addition, each other creature within 10 feet of the target when the stone explodes takes 2d6 points of fire damage (Reflex DC 22 negates).

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 sling; stones deal +2d6 fire on hit (no resist) and 2d6 fire to creatures within 10 ft (Dodge contest vs 22 negates). Resist roll: Quick Contest of the target's Dodge against an effective skill equal to the printed DC (22).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
36,300 gp (item level 17) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### ROD OF CELESTIAL MIGHT
**MIC Specific weapon (rod) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 1 — Legendary (levels 17-20)** (rule in `mic_pipeline.py`; printed price 38,600 gp (item level 17))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (rod)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: A rod of celestial might functions as a +1/+1 quarterstaff. Its abilities can be activated only by a non-evil character. 1. After a successful attack with the rod against an evil outsider, you can trigger a holy smite effect centered on the target as an immediate (command) action (three times per day). 2. If you are within 60 feet of an evil outsider, you can summon an avoral guardinal (as summon monster VII) as a standard (command) action (once per day).
facts: 38,600 gp; item level 17th; caster level 13th; activation See text; prerequisites Craft Magic Arms and Armor, Craft Rod, holy smite, summon monster VII
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): A rod of celestial might functions as a +1/+1 quarterstaff. Its abilities can be activated only by a non-evil character. 1. After a successful attack with the rod against an evil outsider, you can trigger a holy smite effect centered on the target as an immediate (command) action (three times per day). 2. If you are within 60 feet of an evil outsider, you can summon an avoral guardinal (as summon monster VII) as a standard (command) action (once per day).

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1/+1 quarterstaff, usable abilities only by a non-evil wielder: 3/day holy smite as an immediate action after a hit on an evil outsider; 1/day summon an avoral guardinal near an evil outsider.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
38,600 gp (item level 17) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### TENTACLE ROD, GREATER
**MIC Specific weapon (rod) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 1 — Legendary (levels 17-20)** (rule in `mic_pipeline.py`; printed price 36,000 gp (item level 17))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (rod)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When activated, a greater tentacle rod makes six attacks (one per tentacle) against a single target within your melee reach. The rod uses its own attack bonus (+18), and each attack deals 9 points of bludgeoning damage. Treat the rod as a magic weapon for overcoming damage reduction. If at least three tentacles strike the same living creature in a round, it becomes fatigued (Fort DC 20 negates); creatures already fatigued suffer no additional effect. If all six tentacles strike the same living creature in a round, it instead becomes exhausted (Fort DC 20 negates).
facts: 36,000 gp; item level 17th; caster level 12th; activation Standard (command); prerequisites Craft Magic Arms and Armor, Craft Rod, animate objects, Evard's black tentacles, ray of exhaustion, ray of fatigue
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When activated, a greater tentacle rod makes six attacks (one per tentacle) against a single target within your melee reach. The rod uses its own attack bonus (+18), and each attack deals 9 points of bludgeoning damage. Treat the rod as a magic weapon for overcoming damage reduction. If at least three tentacles strike the same living creature in a round, it becomes fatigued (Fort DC 20 negates); creatures already fatigued suffer no additional effect. If all six tentacles strike the same living creature in a round, it instead becomes exhausted (Fort DC 20 negates).

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Six tentacle attacks at +18 for 9 bludgeoning each; three or more hits fatigue, all six exhaust (HT contest vs 20 negates). Resist roll: Quick Contest of the target's HT against an effective skill equal to the printed DC (20).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
36,000 gp (item level 17) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

## TIER 2 — HEROIC ELITE (LEVELS 13-16)

### AXE OF THE SEA REAVERS
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `mic_pipeline.py`; printed price 10,320 gp (item level 13))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: This +1 greataxe allows you to float atop the water, no matter your weight (continuous, no activation). You can also activate it for two abilities: utter a war cry, and you and all allies within 15 feet gain a +2 morale bonus on attack rolls, weapon damage, saves, skill checks and ability checks for 1 round; or speak a command word, and all enemies within 15 feet become panicked for 1 round (Will DC 16 negates). Each of these abilities is usable once per day.
facts: 10,320 gp; item level 13th; caster level 7th; activation — and standard (command); prerequisites Craft Magic Arms and Armor, fear, heroism
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): This +1 greataxe allows you to float atop the water, no matter your weight (continuous, no activation). You can also activate it for two abilities: utter a war cry, and you and all allies within 15 feet gain a +2 morale bonus on attack rolls, weapon damage, saves, skill checks and ability checks for 1 round; or speak a command word, and all enemies within 15 feet become panicked for 1 round (Will DC 16 negates). Each of these abilities is usable once per day.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Continuous water-walking on any surface of water; war cry (+2 morale to attack, damage, saves and checks for 6 seconds, 15 ft); panic (Fear Affliction) 6 seconds, Will vs 16. Resist roll: Quick Contest of the target's Will against an effective skill equal to the printed DC (16).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
10,320 gp (item level 13) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### BOW OF SONGS
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `mic_pipeline.py`; printed price 12,330 gp (item level 13))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: This +1 shortbow blends music with every shot. On your turn, you can expend one daily use of your bardic music ability to gain a bonus equal to your Charisma bonus on the next attack roll and (if your attack hits) on the corresponding damage roll that you make with the bow.
facts: 12,330 gp; item level 13th; caster level 8th; activation Swift (command); prerequisites Craft Magic Arms and Armor, sculpt sound, elf, bardic music
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): This +1 shortbow blends music with every shot. On your turn, you can expend one daily use of your bardic music ability to gain a bonus equal to your Charisma bonus on the next attack roll and (if your attack hits) on the corresponding damage roll that you make with the bow.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Spend a bardic music use as a swift action: Charisma bonus added to the next attack roll and to its damage (3.5e chassis); no separate GURPS rider.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
12,330 gp (item level 13) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### CHAIN OF OBEISANCE [RELIC]
**MIC Specific weapon (relic) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `mic_pipeline.py`; printed price 20,400 gp (item level 15))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (relic)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: A chain of obeisance functions as a +1 unholy spiked chain if you are lawful evil, neutral evil, or lawful neutral. Relic Power: with the proper divine connection you can wield this weapon in a grapple as if it were a light weapon. If you pin your opponent while wielding it, the foe must succeed on a DC 22 Will save or be dominated as by dominate monster; no more than one creature can be dominated at a time. To use the relic power you must worship Hextor and sacrifice a 7th-level divine spell slot or have the True Believer feat and at least 13 HD. [lore omitted]
facts: 20,400 gp; item level 15th; caster level 20th; activation —; prerequisites Craft Magic Arms and Armor, Sanctify Relic, dominate monster
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): A chain of obeisance functions as a +1 unholy spiked chain if you are lawful evil, neutral evil, or lawful neutral. Relic Power: with the proper divine connection you can wield this weapon in a grapple as if it were a light weapon. If you pin your opponent while wielding it, the foe must succeed on a DC 22 Will save or be dominated as by dominate monster; no more than one creature can be dominated at a time. To use the relic power you must worship Hextor and sacrifice a 7th-level divine spell slot or have the True Believer feat and at least 13 HD. [lore omitted] Relic: the printed alignment gate and worship or slot condition apply exactly as printed; outside them the item is a masterwork weapon.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 unholy spiked chain (alignment-gated); relic power: wieldable in a grapple as a light weapon; pin a foe and it is dominated (Will vs 22) as dominate monster, one creature at a time.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
20,400 gp (item level 15) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### CHROMATIC ROD [RELIC]
**MIC Specific weapon (relic) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `mic_pipeline.py`; printed price 12,308 gp (item level 13))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (relic)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When you wield a chromatic rod, it functions as a +1 morningstar with the corrosive, frost, flaming, or shock property if you are chaotic evil, neutral evil, or chaotic neutral. You can select or change the property by speaking the command word, but it can have no more than one such property at a time. Relic Power: with the proper divine connection you can use spell-like abilities, each once per day: 5th-level slot / 9 HD: wall of ice (300-ft. range, up to twenty 10-foot squares), insect plague (1,200-ft. range, six adjacent swarms); 7th-level slot / 13 HD: dominate person (75-ft. range, Will DC 20 negates), find the path (200 minutes), veil (Will DC 21). To use them you must worship Tiamat and sacrifice a divine spell slot or have the True Believer feat and the Hit Dice given. [lore omitted]
facts: 12,308 gp; item level 13th; caster level 20th; activation Standard (command); prerequisites Craft Magic Arms and Armor, Craft Rod, Sanctify Relic, dominate person, find the path, insect plague, veil, wall of ice
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When you wield a chromatic rod, it functions as a +1 morningstar with the corrosive, frost, flaming, or shock property if you are chaotic evil, neutral evil, or chaotic neutral. You can select or change the property by speaking the command word, but it can have no more than one such property at a time. Relic Power: with the proper divine connection you can use spell-like abilities, each once per day: 5th-level slot / 9 HD: wall of ice (300-ft. range, up to twenty 10-foot squares), insect plague (1,200-ft. range, six adjacent swarms); 7th-level slot / 13 HD: dominate person (75-ft. range, Will DC 20 negates), find the path (200 minutes), veil (Will DC 21). To use them you must worship Tiamat and sacrifice a divine spell slot or have the True Believer feat and the Hit Dice given. [lore omitted] Relic: the printed alignment gate and worship or slot condition apply exactly as printed; outside them the item is a masterwork weapon.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 morningstar; command word picks corrosive, frost, flaming or shock (one at a time); relic powers by slot or HD: wall of ice, insect plague, dominate person (Will vs 20), find the path, veil (Will vs 21), each 1/day. Resist roll: Quick Contest of the target's Will against an effective skill equal to the printed DC (20, 21).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
12,308 gp (item level 13) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### CUDGEL THAT NEVER FORGETS [RELIC]
**MIC Specific weapon (relic) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `mic_pipeline.py`; printed price 20,312 gp (item level 15))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (relic)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When you wield a cudgel that never forgets, it functions as a +1 axiomatic heavy mace if you are lawful neutral, lawful good, or neutral. Relic Power: with the proper divine connection the weapon reveals its intelligence (AL LN; Int 16, Wis 10, Cha 16; speech, darkvision 60 ft., hearing, Intimidate +13) and can produce cure moderate wounds three times per day. Its imprecations count as an attempt to demoralize an opponent every round on your turn. To use the relic power you must worship St. Cuthbert and sacrifice a 5th-level divine spell slot or have the True Believer feat and at least 9 HD. If you sacrifice a 7th-level slot (or have True Believer and 13 HD), the cudgel remembers which foes have struck you: if an enemy hits you with a weapon (including a natural weapon), the cudgel thereafter has an enhancement bonus 2 higher than normal against that foe and deals an extra 2d6 points of damage against it; no disguise or shapechanging ability guards against this. [lore omitted]
facts: 20,312 gp; item level 15th; caster level 20th; activation —; see text; prerequisites Craft Magic Arms and Armor, Sanctify Relic, cure moderate wounds, true seeing
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When you wield a cudgel that never forgets, it functions as a +1 axiomatic heavy mace if you are lawful neutral, lawful good, or neutral. Relic Power: with the proper divine connection the weapon reveals its intelligence (AL LN; Int 16, Wis 10, Cha 16; speech, darkvision 60 ft., hearing, Intimidate +13) and can produce cure moderate wounds three times per day. Its imprecations count as an attempt to demoralize an opponent every round on your turn. To use the relic power you must worship St. Cuthbert and sacrifice a 5th-level divine spell slot or have the True Believer feat and at least 9 HD. If you sacrifice a 7th-level slot (or have True Believer and 13 HD), the cudgel remembers which foes have struck you: if an enemy hits you with a weapon (including a natural weapon), the cudgel thereafter has an enhancement bonus 2 higher than normal against that foe and deals an extra 2d6 points of damage against it; no disguise or shapechanging ability guards against this. [lore omitted] Relic: the printed alignment gate and worship or slot condition apply exactly as printed; outside them the item is a masterwork weapon.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 axiomatic heavy mace; relic: sapient (Int 16, Wis 10, Cha 16), cure moderate wounds 3/day, free demoralize each round; at the higher slot it marks foes that have hit the wielder (+2 enhancement and +2d6 vs that foe).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
20,312 gp (item level 15) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### DAGGER OF DENIAL [RELIC]
**MIC Specific weapon (relic) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `mic_pipeline.py`; printed price 20,302 gp (item level 15))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (relic)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When you wield this weapon, it functions as a +1 unholy dagger. Unlike most relics it functions for a wielder of any alignment and retains its sentience and basic relic powers even without the divine connection, though it will not reveal its intelligence or use relic powers for you. If you aren't neutral, lawful evil, neutral evil, or chaotic evil, the dagger betrays you at the first opportunity, surreptitiously dispelling your spells and those of your allies. Relic Power: with the proper divine connection it reveals its intelligence (AL NE; Int 18, Wis 10, Cha 18; speech, telepathy, darkvision 120 ft., blindsense, hearing; Intimidate +13, Spellcraft +14, Bluff +14; Ego 26) and can use detect magic at will and greater dispel magic once per day. To use the relic power you must worship Vecna and sacrifice a 6th-level divine spell slot or have the True Believer feat and at least 11 HD. With an 8th-level slot (or True Believer and 15 HD) it grants a continuous detect scrying effect and can use arcane eye once per day. It generally readies an action to counterspell a foe's spellcasting with greater dispel magic. [lore omitted]
facts: 20,302 gp; item level 15th; caster level 20th; activation —; see text; prerequisites Craft Magic Arms and Armor, Sanctify Relic, arcane eye, detect magic, detect scrying, greater dispel magic
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When you wield this weapon, it functions as a +1 unholy dagger. Unlike most relics it functions for a wielder of any alignment and retains its sentience and basic relic powers even without the divine connection, though it will not reveal its intelligence or use relic powers for you. If you aren't neutral, lawful evil, neutral evil, or chaotic evil, the dagger betrays you at the first opportunity, surreptitiously dispelling your spells and those of your allies. Relic Power: with the proper divine connection it reveals its intelligence (AL NE; Int 18, Wis 10, Cha 18; speech, telepathy, darkvision 120 ft., blindsense, hearing; Intimidate +13, Spellcraft +14, Bluff +14; Ego 26) and can use detect magic at will and greater dispel magic once per day. To use the relic power you must worship Vecna and sacrifice a 6th-level divine spell slot or have the True Believer feat and at least 11 HD. With an 8th-level slot (or True Believer and 15 HD) it grants a continuous detect scrying effect and can use arcane eye once per day. It generally readies an action to counterspell a foe's spellcasting with greater dispel magic. [lore omitted] Relic: the printed alignment gate and worship or slot condition apply exactly as printed; outside them the item is a masterwork weapon. Betrayal clause (non-evil, non-neutral wielder) is kept as printed; recommended NPC-side use.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 unholy dagger usable by any alignment; sapient (Ego 26); non-evil, non-neutral wielders are betrayed (it dispels their and their allies' spells); detect magic at will, greater dispel magic 1/day; at the higher slot continuous detect scrying and arcane eye 1/day.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
20,302 gp (item level 15) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### LASH OF SANDS
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `mic_pipeline.py`; printed price 22,301 gp (item level 15))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: This +1 desiccating burst whip is twice as heavy as a normal whip, deals lethal damage, and is effective even against opponents in armor. Once per day, you can activate the whip when you strike an opponent with it. Doing so creates a mass of leather bindings that enwrap the target, entangling it as if with a net for 3 rounds or until it escapes. Each round the creature remains entangled, it takes 1d4 points of damage, or 1d8 points if it is a plant or an elemental that has the water subtype. Nonliving creatures take no damage from this effect.
facts: 22,301 gp; item level 15th; caster level 12th; activation Free (mental); prerequisites Craft Magic Arms and Armor, animate rope, desiccate (Snd 114)
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): This +1 desiccating burst whip is twice as heavy as a normal whip, deals lethal damage, and is effective even against opponents in armor. Once per day, you can activate the whip when you strike an opponent with it. Doing so creates a mass of leather bindings that enwrap the target, entangling it as if with a net for 3 rounds or until it escapes. Each round the creature remains entangled, it takes 1d4 points of damage, or 1d8 points if it is a plant or an elemental that has the water subtype. Nonliving creatures take no damage from this effect.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 desiccating burst whip, lethal damage, works vs armor; 1/day on a hit: entangle as a net for 18 seconds, 1d4 per turn (1d8 vs plants and water elementals), nonliving take none.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
22,301 gp (item level 15) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### QUARTERSTAFF OF BATTLE
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `mic_pipeline.py`; printed price 24,600 gp (item level 15))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: While wielding this +1/+1 quarterstaff, you can attempt to disarm opponents as if you had the Improved Disarm feat. In addition it has three abilities you can use when you activate the weapon. 1. For the next 2 rounds the staff automatically deflects all ranged attacks from Medium or smaller attackers, as well as all ranged attacks created by spells of 2nd level or lower, that target you or any ally adjacent to you (three times per day). 2. Both ends of the staff gain the speed weapon property (DMG 225) for 5 rounds (once per day). 3. Your next attack with the quarterstaff on this turn is a battlestrike: if it hits, the quarterstaff deals an extra 2d6 points of damage, and the target is knocked prone and stunned for 1 round (Fort DC 22 negates the stun and prone effects) (once per day).
facts: 24,600 gp; item level 15th; caster level 12th; activation Swift (command); prerequisites Craft Magic Arms and Armor, haste, protection from arrows, Tenser's transformation
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): While wielding this +1/+1 quarterstaff, you can attempt to disarm opponents as if you had the Improved Disarm feat. In addition it has three abilities you can use when you activate the weapon. 1. For the next 2 rounds the staff automatically deflects all ranged attacks from Medium or smaller attackers, as well as all ranged attacks created by spells of 2nd level or lower, that target you or any ally adjacent to you (three times per day). 2. Both ends of the staff gain the speed weapon property (DMG 225) for 5 rounds (once per day). 3. Your next attack with the quarterstaff on this turn is a battlestrike: if it hits, the quarterstaff deals an extra 2d6 points of damage, and the target is knocked prone and stunned for 1 round (Fort DC 22 negates the stun and prone effects) (once per day).

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1/+1 quarterstaff; Improved Disarm; abilities: 2 rounds deflection of small ranged attacks (3/day), speed on both ends 5 rounds (1/day), battlestrike +2d6, knockdown and stun (HT contest vs 22 negates) (1/day). Resist roll: Quick Contest of the target's HT against an effective skill equal to the printed DC (22).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
24,600 gp (item level 15) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### ROD OF CATS
**MIC Specific weapon (rod) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `mic_pipeline.py`; printed price 10,600 gp (item level 13))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (rod)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When held, this +1/masterwork quarterstaff grants you low-light vision and a +5 competence bonus on Hide and Move Silently checks (continuous). Once per day you can activate it for one of two effects: a spider climb effect on you for 50 minutes, or a darkness effect targeted on the rod (you and anyone touching the rod can see normally within it). The rod also has a secret compartment (DC 25 Search to find) large enough to hold a set of thieves' tools, a scroll, or an object of similar size.
facts: 10,600 gp; item level 13th; caster level 5th; activation — and standard (command); prerequisites Craft Magic Arms and Armor, Craft Rod, cat's grace, darkness, low-light vision (SC 134), spider climb
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When held, this +1/masterwork quarterstaff grants you low-light vision and a +5 competence bonus on Hide and Move Silently checks (continuous). Once per day you can activate it for one of two effects: a spider climb effect on you for 50 minutes, or a darkness effect targeted on the rod (you and anyone touching the rod can see normally within it). The rod also has a secret compartment (DC 25 Search to find) large enough to hold a set of thieves' tools, a scroll, or an object of similar size.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1/masterwork quarterstaff; continuous low-light vision and +5 Hide and Move Silently; 1/day spider climb 50 minutes or darkness on the rod; secret compartment (Search 25).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
10,600 gp (item level 13) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### ROD OF DEFIANCE
**MIC Specific weapon (rod) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `mic_pipeline.py`; printed price 7,312 gp (item level 14))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (rod)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: You can use a rod of defiance in combat as a +1 heavy mace. In addition, each undead creature within 30 feet of you while you hold the rod is treated as if it had 4 fewer Hit Dice (minimum 1 HD) for the purpose of turn or rebuke undead checks.
facts: 7,312 gp; item level 14th; caster level 10th; activation —; prerequisites Craft Magic Arms and Armor, Craft Rod, turn undead or rebuke undead
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): You can use a rod of defiance in combat as a +1 heavy mace. In addition, each undead creature within 30 feet of you while you hold the rod is treated as if it had 4 fewer Hit Dice (minimum 1 HD) for the purpose of turn or rebuke undead checks.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 heavy mace; undead within 30 ft are treated as 4 Hit Dice lower (minimum 1) for turn and rebuke checks.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
7,312 gp (item level 14) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### ROD OF ENERVATING STRIKE
**MIC Specific weapon (rod) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `mic_pipeline.py`; printed price 18,312 gp (item level 15))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (rod)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: Crafted from wood exposed to the Negative Energy Plane, a rod of enervating strike functions as a +1 heavy mace. In addition, when you successfully strike a creature with the rod in melee, the target is subjected to an inflict light wounds effect (1d8+5 damage; Will DC 11 half). If you score a critical hit with the rod, the creature is instead subjected to an inflict serious wounds effect (3d8+15 damage; Will DC 14 half). When you use the rod on a minor negative-dominant plane, its inflict effects are empowered as if by the Empower Spell feat. When used on a major negative-dominant plane, these effects are maximized as if by the Maximize Spell feat.
facts: 18,312 gp; item level 15th; caster level 15th; activation —; prerequisites Craft Magic Arms and Armor, Craft Rod, inflict serious wounds
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Crafted from wood exposed to the Negative Energy Plane, a rod of enervating strike functions as a +1 heavy mace. In addition, when you successfully strike a creature with the rod in melee, the target is subjected to an inflict light wounds effect (1d8+5 damage; Will DC 11 half). If you score a critical hit with the rod, the creature is instead subjected to an inflict serious wounds effect (3d8+15 damage; Will DC 14 half). When you use the rod on a minor negative-dominant plane, its inflict effects are empowered as if by the Empower Spell feat. When used on a major negative-dominant plane, these effects are maximized as if by the Maximize Spell feat.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 heavy mace; each melee hit adds inflict light wounds (1d8+5, Will contest vs 11 for half), crit adds inflict serious wounds (3d8+15, Will vs 14); empowered on minor and maximized on major negative planes. Resist roll: Quick Contest of the target's Will against an effective skill equal to the printed DC (11, 14).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
18,312 gp (item level 15) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### ROD OF FREEDOM
**MIC Specific weapon (rod) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `mic_pipeline.py`; printed price 18,402 gp (item level 15))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (rod)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: This +4 silver heavy mace has three special abilities. (1) While the rod is in your hand, you gain a +4 morale bonus on saving throws against charm or compulsion effects (continuous). (2) You can activate it as a free (mental) action at will to deal nonlethal damage without penalty on your next attack roll (decide before the attack). (3) Any time you strike a creature under a charm or compulsion effect with the rod, you can activate it as a swift (command) action to make a special caster level check (1d20+9) and attempt to dispel the effect (DC 11 + caster level of the effect); five times per day.
facts: 18,402 gp; item level 15th; caster level 9th; activation See text; prerequisites Craft Magic Arms and Armor, Craft Rod, break enchantment
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): This +4 silver heavy mace has three special abilities. (1) While the rod is in your hand, you gain a +4 morale bonus on saving throws against charm or compulsion effects (continuous). (2) You can activate it as a free (mental) action at will to deal nonlethal damage without penalty on your next attack roll (decide before the attack). (3) Any time you strike a creature under a charm or compulsion effect with the rod, you can activate it as a swift (command) action to make a special caster level check (1d20+9) and attempt to dispel the effect (DC 11 + caster level of the effect); five times per day.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +4 silver heavy mace; +4 morale vs charm and compulsion; free-action nonlethal at will; swift dispel check 1d20+9 vs 11 + effect caster level on a struck charmed creature, 5/day.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
18,402 gp (item level 15) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### ROD OF WHIPS
**MIC Specific weapon (rod) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `mic_pipeline.py`; printed price 15,000 gp (item level 14))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (rod)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: On command, a rod of whips grows a magic tendril of force from one end that functions as a whip. Once activated, it acts as a +1 dancing whip that can strike incorporeal creatures as a force effect. A rod of whips can be activated three times per day, and each activation lasts for 10 rounds.
facts: 15,000 gp; item level 14th; caster level 12th; activation Standard (command); prerequisites Craft Magic Arms and Armor, Craft Rod, animate objects, spiritual weapon
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): On command, a rod of whips grows a magic tendril of force from one end that functions as a whip. Once activated, it acts as a +1 dancing whip that can strike incorporeal creatures as a force effect. A rod of whips can be activated three times per day, and each activation lasts for 10 rounds.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). 3/day, 10 rounds: a force whip acting as a +1 dancing whip that strikes incorporeal creatures.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
15,000 gp (item level 14) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### ROGUE BLADE
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `mic_pipeline.py`; printed price 12,320 gp (item level 13))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When you activate this +1 rapier, it provides you with the effect of a blink spell for 6 rounds. The effect ends prematurely if you stop holding the rogue blade. This effect can be used twice per day.
facts: 12,320 gp; item level 13th; caster level 6th; activation Swift (mental); prerequisites Craft Magic Arms and Armor, blink
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When you activate this +1 rapier, it provides you with the effect of a blink spell for 6 rounds. The effect ends prematurely if you stop holding the rogue blade. This effect can be used twice per day.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 rapier; twice per day blink for 6 rounds, ends if the blade is dropped.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
12,320 gp (item level 13) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### RUBY BLADE [RELIC]
**MIC Specific weapon (relic) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `mic_pipeline.py`; printed price 20,302 gp (item level 15))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (relic)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When you wield a ruby blade, it functions as a +1 axiomatic dagger if you are lawful evil, lawful neutral, lawful good, or neutral. Relic Power: with the proper divine connection, and if you have levels in a class that allows you to rebuke undead, your effective level in that class is considered 4 higher for the purpose of bolstering, rebuking, or commanding undead (continuous). In addition, you can activate a ruby blade to produce the effect of status spell once per day. To use the relic power you must worship Wee Jas and sacrifice a 6th-level divine spell slot or have the True Believer feat and at least 11 HD. [lore omitted]
facts: 20,302 gp; item level 15th; caster level 20th; activation — and standard (command); prerequisites Craft Magic Arms and Armor, Sanctify Relic, order's wrath, status
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When you wield a ruby blade, it functions as a +1 axiomatic dagger if you are lawful evil, lawful neutral, lawful good, or neutral. Relic Power: with the proper divine connection, and if you have levels in a class that allows you to rebuke undead, your effective level in that class is considered 4 higher for the purpose of bolstering, rebuking, or commanding undead (continuous). In addition, you can activate a ruby blade to produce the effect of status spell once per day. To use the relic power you must worship Wee Jas and sacrifice a 6th-level divine spell slot or have the True Believer feat and at least 11 HD. [lore omitted] Relic: the printed alignment gate and worship or slot condition apply exactly as printed; outside them the item is a masterwork weapon.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 axiomatic dagger; relic: +4 effective level for rebuking or commanding undead (continuous); status 1/day.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
20,302 gp (item level 15) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### SCOURGE OF PAIN
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `mic_pipeline.py`; printed price 26,320 gp (item level 16))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: Each time this +1 scourge strikes, it deals an extra 1d8 points of nonlethal damage and causes agonizing pain in the creature struck. The target takes a -4 penalty on attack rolls, saving throws, and checks for 1d4 rounds (Fort DC 17 negates). Multiple strikes on the same creature don't stack.
facts: 26,320 gp; item level 16th; caster level 9th; activation —; prerequisites Craft Magic Arms and Armor, symbol of pain
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Each time this +1 scourge strikes, it deals an extra 1d8 points of nonlethal damage and causes agonizing pain in the creature struck. The target takes a -4 penalty on attack rolls, saving throws, and checks for 1d4 rounds (Fort DC 17 negates). Multiple strikes on the same creature don't stack.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 scourge; each hit adds 1d8 nonlethal and -4 to attack, saves and checks for 1d4 rounds (HT contest vs 17 negates; no stacking). Resist roll: Quick Contest of the target's HT against an effective skill equal to the printed DC (17).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
26,320 gp (item level 16) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### TENTACLE ROD
**MIC Specific weapon (rod) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `mic_pipeline.py`; printed price 14,000 gp (item level 14))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (rod)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When activated, a tentacle rod makes three attacks (one per tentacle) against a single target within your melee reach that you designate. The rod uses its own attack bonus (+12) rather than yours, and each attack deals 6 points of bludgeoning damage. Treat the rod as a magic weapon for the purpose of overcoming damage reduction. If all three tentacles strike the same living creature in a round, that creature becomes slowed (as the slow spell) for 5 rounds (Fort DC 14 negates).
facts: 14,000 gp; item level 14th; caster level 6th; activation Standard (command); prerequisites Craft Magic Arms and Armor, Craft Rod, animate objects, Evard's black tentacles, slow
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When activated, a tentacle rod makes three attacks (one per tentacle) against a single target within your melee reach that you designate. The rod uses its own attack bonus (+12) rather than yours, and each attack deals 6 points of bludgeoning damage. Treat the rod as a magic weapon for the purpose of overcoming damage reduction. If all three tentacles strike the same living creature in a round, that creature becomes slowed (as the slow spell) for 5 rounds (Fort DC 14 negates).

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Standard (command): three tentacle attacks at +12 for 6 bludgeoning each; all three hit slows the target 30 seconds (HT contest vs 14 negates). Resist roll: Quick Contest of the target's HT against an effective skill equal to the printed DC (14).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
14,000 gp (item level 14) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### WATER WHIP
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `mic_pipeline.py`; printed price 20,301 gp (item level 15))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: This +1 whip deals lethal damage and can affect armored creatures, unlike a normal whip. While wielding it you are difficult to disarm: if the whip is knocked from your grasp it flows back into your hand at the beginning of your next turn (even from someone else's grasp) provided it is within 30 feet, requiring no action. Drawing a water whip is always a free action. A fire elemental and a water elemental are bound within, allowing it to emanate either flaming or frost (DMG 224); you choose when you activate it, and it deals an extra 1d6 points of the appropriate damage (fire or cold). [lore omitted]
facts: 20,301 gp; item level 15th; caster level 5th; activation — and standard (command); prerequisites Bind Elemental (ECS 51) or Craft Magic Arms and Armor, planar binding
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): This +1 whip deals lethal damage and can affect armored creatures, unlike a normal whip. While wielding it you are difficult to disarm: if the whip is knocked from your grasp it flows back into your hand at the beginning of your next turn (even from someone else's grasp) provided it is within 30 feet, requiring no action. Drawing a water whip is always a free action. A fire elemental and a water elemental are bound within, allowing it to emanate either flaming or frost (DMG 224); you choose when you activate it, and it deals an extra 1d6 points of the appropriate damage (fire or cold). [lore omitted]

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 whip dealing lethal damage, works against armor; returns to hand within 30 ft; frost or flaming +1d6 chosen on activation.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
20,301 gp (item level 15) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

## TIER 3 — HEROIC (LEVELS 9-12)

### ASSASSIN WHIP
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 5,301 gp (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: Twice per day, you can activate this +1 whip after successfully hitting a Medium or smaller target that is standing on the ground. Doing this causes tendrils of vegetation to spring forth from the ground, entangling the target and dealing 2d6 points of damage per round. This effect lasts for 3 rounds or until the affected creature escapes from the tendrils (a DC 20 Strength check or DC 20 Escape Artist check made as a full-round action).
facts: 5,301 gp; item level 10th; caster level 5th; activation Free (command); prerequisites Craft Magic Arms and Armor, entangle
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Twice per day, you can activate this +1 whip after successfully hitting a Medium or smaller target that is standing on the ground. Doing this causes tendrils of vegetation to spring forth from the ground, entangling the target and dealing 2d6 points of damage per round. This effect lasts for 3 rounds or until the affected creature escapes from the tendrils (a DC 20 Strength check or DC 20 Escape Artist check made as a full-round action).

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Binding of vegetation on a ground-standing Medium or smaller target: Innate Attack Crushing 2d6 each turn for 18 seconds; escape by ST or Escape Artist vs 20.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
5,301 gp (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### AXE OF ANCESTRAL VIRTUE [RELIC]
**MIC Specific weapon (relic) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 8,530 gp (item level 12))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (relic)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When you wield an axe of ancestral virtue, it functions as a +1 keen adamantine dwarven waraxe if you are lawful good, lawful neutral, or neutral good. Relic Power: with the proper divine connection the axe reveals its intelligence (AL LN; Int 10, Wis 17, Cha 17; speech, telepathy, darkvision 120 ft., hearing; Ego 17) and can use bless, cure moderate wounds (wielder only) and faerie fire, each three times per day; with a 7th-level divine slot sacrificed (or True Believer and 13 HD) it can also use haste (wielder only) three times per day. To use the relic power you must worship Moradin and sacrifice a 5th-level divine spell slot or have the True Believer feat and at least 9 HD. [lore omitted]
facts: 8,530 gp; item level 12th; caster level 20th; activation —; prerequisites Craft Magic Arms and Armor, Sanctify Relic, bless, cure moderate wounds, faerie fire, haste, keen edge
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When you wield an axe of ancestral virtue, it functions as a +1 keen adamantine dwarven waraxe if you are lawful good, lawful neutral, or neutral good. Relic Power: with the proper divine connection the axe reveals its intelligence (AL LN; Int 10, Wis 17, Cha 17; speech, telepathy, darkvision 120 ft., hearing; Ego 17) and can use bless, cure moderate wounds (wielder only) and faerie fire, each three times per day; with a 7th-level divine slot sacrificed (or True Believer and 13 HD) it can also use haste (wielder only) three times per day. To use the relic power you must worship Moradin and sacrifice a 5th-level divine spell slot or have the True Believer feat and at least 9 HD. [lore omitted] Relic: the printed alignment gate and worship or slot condition apply exactly as printed; outside them the item is a masterwork weapon.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Weapon bonuses per 3.5e (+1 keen adamantine waraxe, alignment-gated); relic powers as printed (bless, cure moderate wounds, faerie fire 3/day; haste at the higher slot); sapient item per the printed Ego 17.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
8,530 gp (item level 12) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### BLADED CROSSBOW
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 4,660 gp (item level 9))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: This crossbow has an exceptionally strong stock shaped so you can grip and swing it as a melee weapon. You can use a bladed crossbow as either a +1 heavy crossbow for ranged attacks, or as a +1 battleaxe for melee attacks.
facts: 4,660 gp; item level 9th; caster level 11th; activation —; prerequisites Craft Magic Arms and Armor, blade barrier
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): This crossbow has an exceptionally strong stock shaped so you can grip and swing it as a melee weapon. You can use a bladed crossbow as either a +1 heavy crossbow for ranged attacks, or as a +1 battleaxe for melee attacks.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Switchable: heavy crossbow +1 (ranged) or battleaxe +1 (melee); the Gadget holds both modes.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
4,660 gp (item level 9) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### BLAZING SKYLANCE
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 8,310 gp (item level 12))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: Three times per day, you can command this +1 lance to fire a 15-foot cone of searing flames from its tip, dealing 5d4 points of fire damage to targets within the cone's area (Reflex DC 13 half).
facts: 8,310 gp; item level 12th; caster level 5th; activation Standard (command); prerequisites Craft Magic Arms and Armor, burning hands
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Three times per day, you can command this +1 lance to fire a 15-foot cone of searing flames from its tip, dealing 5d4 points of fire damage to targets within the cone's area (Reflex DC 13 half).

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Burning cone 15 ft: Innate Attack Burning 5d4 as-is, 3/day, Dodge-based contest vs 13 for half. Resist roll: Quick Contest of the target's Dodge against an effective skill equal to the printed DC (13).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
8,310 gp (item level 12) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### BOWSTAFF
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 4,600 gp (item level 9))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: By activating a bowstaff, you can change this +1/masterwork quarterstaff into a +1 longbow or back again. Each version performs like a regular magic weapon of its kind.
facts: 4,600 gp; item level 9th; caster level 15th; activation Swift (command); prerequisites Craft Magic Arms and Armor, polymorph any object
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): By activating a bowstaff, you can change this +1/masterwork quarterstaff into a +1 longbow or back again. Each version performs like a regular magic weapon of its kind.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Swift (command) change between +1 masterwork quarterstaff and +1 longbow; both forms share the Gadget.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
4,600 gp (item level 9) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### CRYSTAL ECHOBLADE
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 4,310 gp (item level 9))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: A crystal echoblade normally functions as a +1 longsword, but is enhanced by your musical ability. If you use your bardic music ability while wielding the weapon, the blade resonates in harmony, dealing additional sonic damage on each attack equal to half your bard level.
facts: 4,310 gp; item level 9th; caster level 10th; activation —; prerequisites Craft Magic Arms and Armor, bardic music
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): A crystal echoblade normally functions as a +1 longsword, but is enhanced by your musical ability. If you use your bardic music ability while wielding the weapon, the blade resonates in harmony, dealing additional sonic damage on each attack equal to half your bard level.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 longsword; each attack while the wielder is using bardic music adds sonic damage equal to half bard level as a Follow-Up damage rider.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
4,310 gp (item level 9) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### CRYSTAL OF ARCANE STEEL
**MIC Weapon augment crystal — Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 500 gp (3rd) least; 2,000 gp (6th) lesser; 6,000 gp (10th) greater (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Weapon augment crystal
quality: clean
url: Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)
tooltip: Functions only when attached to a melee weapon. Least: +1 insight bonus on your weapon damage roll when delivering a spell or spell-like ability through a melee attack with the weapon. Lesser: as least, and +1 insight bonus on the attack roll. Greater: as lesser, and increases the save DC of the spell or spell-like ability by 1.
facts: prices (item level): 500 gp (3rd) least; 2,000 gp (6th) lesser; 6,000 gp (10th) greater; caster level 5th; activation —; prerequisites Craft Magic Arms and Armor, magic weapon
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Functions only when attached to a melee weapon. Least: +1 insight bonus on your weapon damage roll when delivering a spell or spell-like ability through a melee attack with the weapon. Lesser: as least, and +1 insight bonus on the attack roll. Greater: as lesser, and increases the save DC of the spell or spell-like ability by 1. 3.5e ladder: Least = Magic rung, Lesser = Rare rung, Greater = Unique rung of the Crusader ladder.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Rider on a spell delivered through the weapon: +1 damage, +1 attack, then +1 to the effect's resist DC (Quick Contest effective skill +1).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
500 gp (3rd) least; 2,000 gp (6th) lesser; 6,000 gp (10th) greater (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### CRYSTAL OF ENERGY ASSAULT (ACID, COLD, ELECTRICITY, FIRE)
**MIC Weapon augment crystal — Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 600 gp (3rd) least; 3,000 gp (7th) lesser; 6,000 gp (10th) greater (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Weapon augment crystal
quality: clean
url: Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)
tooltip: Adds one type of energy damage (acid, cold, electricity or fire; the crystal is one type) to the weapon's attacks; doesn't stack with energy damage of the same type the weapon already deals. Least: 1 point of energy damage. Lesser: extra 1d6 energy damage. Greater: extra 1d6 plus a secondary effect by type: Acid: target takes -1 penalty to AC for 1 round (multiple hits don't stack). Cold: target's speed reduced by 10 feet for 1 round, minimum 5 feet (no stacking). Electricity: target is dazzled for 1 round. Fire: target takes an additional 1d6 fire damage 1 round later (multiple hits don't increase the next round's damage beyond 1d6).
facts: prices (item level): 600 gp (3rd) least; 3,000 gp (7th) lesser; 6,000 gp (10th) greater; caster level 5th; activation —; prerequisites Craft Magic Arms and Armor; Melf's acid arrow, ray of frost, lightning bolt, or fireball; or energy bolt (EPH 100)
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Adds one type of energy damage (acid, cold, electricity or fire; the crystal is one type) to the weapon's attacks; doesn't stack with energy damage of the same type the weapon already deals. Least: 1 point of energy damage. Lesser: extra 1d6 energy damage. Greater: extra 1d6 plus a secondary effect by type: Acid: target takes -1 penalty to AC for 1 round (multiple hits don't stack). Cold: target's speed reduced by 10 feet for 1 round, minimum 5 feet (no stacking). Electricity: target is dazzled for 1 round. Fire: target takes an additional 1d6 fire damage 1 round later (multiple hits don't increase the next round's damage beyond 1d6). 3.5e ladder: Least = Magic rung, Lesser = Rare rung, Greater = Unique rung of the Crusader ladder.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Follow-Up damage rider of the crystal's type: +1 / +1d6 / +1d6 with the greater secondary effect (acid -1 AC; cold -10 ft speed; electricity dazzled; fire +1d6 next round).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
600 gp (3rd) least; 3,000 gp (7th) lesser; 6,000 gp (10th) greater (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Flaming (Elemental 01-08) / Freezing (09-16) / Shocking (17-24) / Corrosive: the crystal is a socketable ladder with a greater-rung secondary effect.

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### CRYSTAL OF LIFE DRINKING
**MIC Weapon augment crystal — Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 400 gp (2nd) least; 1,500 gp (5th) lesser; 6,000 gp (10th) greater (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Weapon augment crystal
quality: clean
url: Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)
tooltip: Each time you damage a living creature with the weapon (nonlethal damage doesn't activate it): Least: you heal 1 point of damage; when it has healed a total of 10 points it becomes inert until the following day. Lesser: heal 3 points per attack until it has healed 30. Greater: heal 5 points per attack until it has healed 50.
facts: prices (item level): 400 gp (2nd) least; 1,500 gp (5th) lesser; 6,000 gp (10th) greater; caster level 5th; activation —; prerequisites Craft Magic Arms and Armor, vampiric touch
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Each time you damage a living creature with the weapon (nonlethal damage doesn't activate it): Least: you heal 1 point of damage; when it has healed a total of 10 points it becomes inert until the following day. Lesser: heal 3 points per attack until it has healed 30. Greater: heal 5 points per attack until it has healed 50. 3.5e ladder: Least = Magic rung, Lesser = Rare rung, Greater = Unique rung of the Crusader ladder.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). On each damaging hit to a living target the wielder heals 1 / 3 / 5 HP up to a daily cap of 10 / 30 / 50 HP.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
400 gp (2nd) least; 1,500 gp (5th) lesser; 6,000 gp (10th) greater (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Leech (Resource 19-24): same heal-on-hit shape, here with a daily cap.

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### DAGGER OF DEFIANCE
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 6,302 gp (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: This +1 dagger grants you a +3 resistance bonus on saves against enchantment and fear effects.
facts: 6,302 gp; item level 10th; caster level 7th; activation —; prerequisites Craft Magic Arms and Armor, remove fear
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): This +1 dagger grants you a +3 resistance bonus on saves against enchantment and fear effects.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 dagger; +3 resistance bonus on saves against enchantment and fear (applied to the wielder's contest rolls as +3).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
6,302 gp (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### DAWNSTAR [RELIC]
**MIC Specific weapon (relic) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 9,308 gp (item level 12))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (relic)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When you wield a dawnstar, it functions as a +2 morningstar if you are lawful good, neutral good, chaotic good, or neutral. Relic Power: with the proper divine connection a dawnstar gains the brilliant energy property (DMG 224). If it is ever sundered or otherwise broken, it explodes, dealing 200 points of damage to every creature and object within 10 feet, 150 points within 20 feet and 100 points within 30 feet; each affected creature can attempt a DC 17 Reflex save to halve the damage. You are unharmed by the explosion. To use the relic power you must worship Pelor and sacrifice a 7th-level divine spell slot or have the True Believer feat and at least 13 HD. [lore omitted]
facts: 9,308 gp; item level 12th; caster level 20th; activation —; prerequisites Craft Magic Arms and Armor, Sanctify Relic, sunburst
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When you wield a dawnstar, it functions as a +2 morningstar if you are lawful good, neutral good, chaotic good, or neutral. Relic Power: with the proper divine connection a dawnstar gains the brilliant energy property (DMG 224). If it is ever sundered or otherwise broken, it explodes, dealing 200 points of damage to every creature and object within 10 feet, 150 points within 20 feet and 100 points within 30 feet; each affected creature can attempt a DC 17 Reflex save to halve the damage. You are unharmed by the explosion. To use the relic power you must worship Pelor and sacrifice a 7th-level divine spell slot or have the True Believer feat and at least 13 HD. [lore omitted] Relic: the printed alignment gate and worship or slot condition apply exactly as printed; outside them the item is a masterwork weapon.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +2 morningstar; relic: brilliant energy; if broken it explodes for 200/150/100 damage at 10/20/30 ft with Dodge contest vs 17 for half, wielder unharmed.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
9,308 gp (item level 12) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### DEATH SPIKE
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 6,304 gp (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: A death spike functions as a +1 cold iron spear, but whenever you reduce a living creature to -1 or fewer hit points on a melee attack with the spear, you can activate it to gain 1d8 temporary hit points and a +2 morale bonus on damage rolls. These benefits last for 1 hour; multiple uses don't stack. The spear can be activated three times per day. If you also wear a magic item that grants a bonus to your Charisma score, you can add the item's bonus to the temporary hit points granted by the spear.
facts: 6,304 gp; item level 10th; caster level 5th; activation Free (command); prerequisites Craft Magic Arms and Armor, death knell, magic weapon
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): A death spike functions as a +1 cold iron spear, but whenever you reduce a living creature to -1 or fewer hit points on a melee attack with the spear, you can activate it to gain 1d8 temporary hit points and a +2 morale bonus on damage rolls. These benefits last for 1 hour; multiple uses don't stack. The spear can be activated three times per day. If you also wear a magic item that grants a bonus to your Charisma score, you can add the item's bonus to the temporary hit points granted by the spear.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 cold iron spear; on reducing a living creature to -1 HP or less in melee: 1d8 temporary HP and +2 morale damage for 1 hour, 3/day.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
6,304 gp (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### DEMOLITION CRYSTAL
**MIC Weapon augment crystal — Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 1,000 gp (4th) least; 3,000 gp (7th) lesser; 6,000 gp (10th) greater (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Weapon augment crystal
quality: clean
url: Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)
tooltip: Designed for those who fight constructs. Least: the weapon deals an extra 1d6 points of damage to constructs. Lesser: as least, and the weapon is treated as adamantine for overcoming the damage reduction of constructs. Greater: as lesser, and the weapon can deliver sneak attacks and critical hits against constructs as if they were living creatures.
facts: prices (item level): 1,000 gp (4th) least; 3,000 gp (7th) lesser; 6,000 gp (10th) greater; caster level 11th; activation —; prerequisites Craft Magic Arms and Armor, disintegrate
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Designed for those who fight constructs. Least: the weapon deals an extra 1d6 points of damage to constructs. Lesser: as least, and the weapon is treated as adamantine for overcoming the damage reduction of constructs. Greater: as lesser, and the weapon can deliver sneak attacks and critical hits against constructs as if they were living creatures. 3.5e ladder: Least = Magic rung, Lesser = Rare rung, Greater = Unique rung of the Crusader ladder.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1d6 vs constructs; adamantine for construct DR; sneak attack and crits against constructs.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
1,000 gp (4th) least; 3,000 gp (7th) lesser; 6,000 gp (10th) greater (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Bane (construct) family in the weapon-affix corpus.

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### DWARF CRUSHER
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 9,010 gp (item level 12))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: This Large +1 adamantine greatclub can only be activated by a bearer who has a Strength of 21 or higher and the Power Attack feat. When it is activated, the next attack you make with it in that round against a dwarf, a construct, or a creature that has the earth subtype is treated as a touch attack. You must also take at least a -5 penalty on this attack roll using the Power Attack feat to gain this benefit. This effect functions three times per day.
facts: 9,010 gp; item level 12th; caster level 6th; activation Swift (command); prerequisites Craft Magic Arms and Armor, bull's strength, giant
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): This Large +1 adamantine greatclub can only be activated by a bearer who has a Strength of 21 or higher and the Power Attack feat. When it is activated, the next attack you make with it in that round against a dwarf, a construct, or a creature that has the earth subtype is treated as a touch attack. You must also take at least a -5 penalty on this attack roll using the Power Attack feat to gain this benefit. This effect functions three times per day.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Large +1 adamantine greatclub; next attack vs dwarf, construct or earth creature is a touch attack (needs ST 21 and Power Attack at -5), 3/day.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
9,010 gp (item level 12) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### FIENDSLAYER CRYSTAL
**MIC Weapon augment crystal — Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 1,000 gp (4th) least; 3,000 gp (7th) lesser; 5,000 gp (9th) greater (item level 9))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Weapon augment crystal
quality: clean
url: Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)
tooltip: Least: the weapon deals an extra 1d6 points of damage to evil outsiders. Lesser: as least, and the weapon is treated as good-aligned for overcoming damage reduction. Greater: as lesser, and if the weapon scores a critical hit against an evil outsider, that creature can't use any teleportation abilities or spells for 1 round. Any evil creature grasping a weapon that bears a fiendslayer crystal gains one negative level, which remains while it holds the weapon and disappears when it no longer wields it; this negative level never results in actual level loss, but cannot be overcome in any way (including restoration) while the weapon is wielded.
facts: prices (item level): 1,000 gp (4th) least; 3,000 gp (7th) lesser; 5,000 gp (9th) greater; caster level 9th; activation —; prerequisites Craft Magic Arms and Armor, align weapon, good alignment
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Least: the weapon deals an extra 1d6 points of damage to evil outsiders. Lesser: as least, and the weapon is treated as good-aligned for overcoming damage reduction. Greater: as lesser, and if the weapon scores a critical hit against an evil outsider, that creature can't use any teleportation abilities or spells for 1 round. Any evil creature grasping a weapon that bears a fiendslayer crystal gains one negative level, which remains while it holds the weapon and disappears when it no longer wields it; this negative level never results in actual level loss, but cannot be overcome in any way (including restoration) while the weapon is wielded. The negative level is the Energy Drained condition (per ruling), never level loss. 3.5e ladder: Least = Magic rung, Lesser = Rare rung, Greater = Unique rung of the Crusader ladder.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1d6 vs evil outsiders; good-aligned for DR; greater crit blocks teleport for 6 seconds; an evil wielder takes one negative level while holding it (Energy Drained, never level loss).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
1,000 gp (4th) least; 3,000 gp (7th) lesser; 5,000 gp (9th) greater (item level 9) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Bane (evil outsider) and Holy in the weapon-affix corpus.

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### FORCEFUL SKYLANCE
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 8,310 gp (item level 12))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: Three times per day, you can command this +1 lance to produce a magic missile effect, firing three missiles with each use. These missiles can be aimed at up to three targets within 150 feet of you.
facts: 8,310 gp; item level 12th; caster level 5th; activation Standard (command); prerequisites Craft Magic Arms and Armor, magic missile
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Three times per day, you can command this +1 lance to produce a magic missile effect, firing three missiles with each use. These missiles can be aimed at up to three targets within 150 feet of you.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). 3/day magic missile: three missiles at up to three targets within 150 ft (auto-hit).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
8,310 gp (item level 12) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### GALEB DUHR HAMMER
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 5,312 gp (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: A galeb duhr hammer acts as a +1 warhammer. In addition, if you have the stonecunning racial ability, whenever you score a critical hit with it against a creature standing on the ground, the surface your target is standing on attempts to hold the creature in place: for 5 rounds the victim's speed falls to 5 feet and it takes a -2 penalty on attack rolls and to AC. [lore omitted]
facts: 5,312 gp; item level 10th; caster level 10th; activation —; prerequisites Craft Magic Arms and Armor, stone shape
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): A galeb duhr hammer acts as a +1 warhammer. In addition, if you have the stonecunning racial ability, whenever you score a critical hit with it against a creature standing on the ground, the surface your target is standing on attempts to hold the creature in place: for 5 rounds the victim's speed falls to 5 feet and it takes a -2 penalty on attack rolls and to AC. [lore omitted]

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 warhammer; with stonecunning, a critical hit on a creature standing on the ground holds it: speed 5 ft, -2 attack and AC for 30 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
5,312 gp (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### GHOST NET
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 8,320 gp (item level 11))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: You can throw this item at a target as though it were an ordinary net. It has no effect against corporeal targets, but any incorporeal target hit by a ghost net is treated as corporeal for the purpose of dealing damage to it with physical or magical attacks (though the net doesn't entangle an incorporeal target); it does not have the usual 50% chance to ignore damage from corporeal sources. A creature ensnared by a ghost net also cannot turn ethereal (or, if snared on the Ethereal Plane, can't return to the Material Plane). The creature can extract itself with a successful DC 20 Escape Artist check as a full-round action; a ghost net can't be burst with a Strength check.
facts: 8,320 gp; item level 11th; caster level 13th; activation —; prerequisites Craft Magic Arms and Armor, ghost trap (SC 103)
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): You can throw this item at a target as though it were an ordinary net. It has no effect against corporeal targets, but any incorporeal target hit by a ghost net is treated as corporeal for the purpose of dealing damage to it with physical or magical attacks (though the net doesn't entangle an incorporeal target); it does not have the usual 50% chance to ignore damage from corporeal sources. A creature ensnared by a ghost net also cannot turn ethereal (or, if snared on the Ethereal Plane, can't return to the Material Plane). The creature can extract itself with a successful DC 20 Escape Artist check as a full-round action; a ghost net can't be burst with a Strength check.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Thrown net; an incorporeal target hit becomes corporeal for damage purposes (no 50% miss) and cannot go ethereal; escape by Escape Artist vs 20; cannot be burst.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
8,320 gp (item level 11) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### HOOKED HAMMER OF THE HEARTHFIRE [RELIC]
**MIC Specific weapon (relic) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 5,120 gp (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (relic)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: While you wield a hooked hammer of the hearthfire, it functions as a +1/+1 gnome hooked hammer if you are neutral good, neutral, chaotic good, or lawful good. Relic Power: with the proper divine connection both ends of this weapon also have the flaming property (DMG 224), and it automatically deals 1d6 points of fire damage per round to any kobold or goblinoid unfortunate enough to grasp its handle. To use the relic power you must worship Garl Glittergold and sacrifice a 4th-level divine spell slot or have the True Believer feat and at least 7 HD. If you sacrifice a 5th-level slot (or True Believer and 9 HD), both ends instead have the flaming burst property. [lore omitted]
facts: 5,120 gp; item level 10th; caster level 20th; activation —; prerequisites Craft Magic Arms and Armor, Sanctify Relic, flame strike
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): While you wield a hooked hammer of the hearthfire, it functions as a +1/+1 gnome hooked hammer if you are neutral good, neutral, chaotic good, or lawful good. Relic Power: with the proper divine connection both ends of this weapon also have the flaming property (DMG 224), and it automatically deals 1d6 points of fire damage per round to any kobold or goblinoid unfortunate enough to grasp its handle. To use the relic power you must worship Garl Glittergold and sacrifice a 4th-level divine spell slot or have the True Believer feat and at least 7 HD. If you sacrifice a 5th-level slot (or True Believer and 9 HD), both ends instead have the flaming burst property. [lore omitted] Relic: the printed alignment gate and worship or slot condition apply exactly as printed; outside them the item is a masterwork weapon.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1/+1 gnome hooked hammer; relic power: both ends flaming (flaming burst at the higher slot), kobolds and goblinoids take 1d6 fire per round holding it.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
5,120 gp (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### LIVING CHAIN
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 4,325 gp (item level 9))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: This +1 spiked chain coils around the target's limbs on a successful attack, granting you a +2 bonus on Strength checks made to trip the target.
facts: 4,325 gp; item level 9th; caster level 7th; activation —; prerequisites Craft Magic Arms and Armor, bull's strength
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): This +1 spiked chain coils around the target's limbs on a successful attack, granting you a +2 bonus on Strength checks made to trip the target.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 spiked chain; +2 on Strength checks to trip the struck target.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
4,325 gp (item level 9) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### MACE OF THE DARK CHILDREN
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 8,012 gp (item level 12))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: This +1 adamantine heavy mace grants you a +3 profane bonus on rebuke undead attempts. You also treat your level as two higher when determining how many Hit Dice of undead you can rebuke.
facts: 8,012 gp; item level 12th; caster level 9th; activation —; prerequisites Craft Magic Arms and Armor, animate dead
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): This +1 adamantine heavy mace grants you a +3 profane bonus on rebuke undead attempts. You also treat your level as two higher when determining how many Hit Dice of undead you can rebuke.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 adamantine heavy mace; +3 profane bonus on rebuke attempts and level counts two higher for rebuke Hit Dice.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
8,012 gp (item level 12) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### MANTICORE GREATSWORD
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 5,350 gp (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: Such a weapon functions as a +1 greatsword. When you activate it, you can launch either one spike (a standard action) or all six spikes (a full-round action) from its hilt as a ranged attack that provokes attacks of opportunity. Treat the spikes as thrown weapons. Each spike deals 1d6 points of piercing damage and has a range increment of 20 feet. The spikes have an enhancement bonus equal to that of the weapon, and are treated as being made of the same material and having the same alignment (if any) as the weapon. The spikes crumble to dust 1 round after they are launched. A manticore greatsword regenerates any thrown spikes at dawn each day.
facts: 5,350 gp; item level 10th; caster level 10th; activation Standard (command) or full-round (command); prerequisites Craft Magic Arms and Armor, magic missile
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Such a weapon functions as a +1 greatsword. When you activate it, you can launch either one spike (a standard action) or all six spikes (a full-round action) from its hilt as a ranged attack that provokes attacks of opportunity. Treat the spikes as thrown weapons. Each spike deals 1d6 points of piercing damage and has a range increment of 20 feet. The spikes have an enhancement bonus equal to that of the weapon, and are treated as being made of the same material and having the same alignment (if any) as the weapon. The spikes crumble to dust 1 round after they are launched. A manticore greatsword regenerates any thrown spikes at dawn each day.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 greatsword; launch one (standard) or six (full-round) spikes, Innate Attack Piercing 1d6 as-is each, range 20 ft increments; regrow at dawn.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
5,350 gp (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### MORNINGSTAR OF THE MANY [RELIC]
**MIC Specific weapon (relic) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 7,308 gp (item level 11))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (relic)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When you wield it, a morningstar of the many functions as a +1 morningstar if you are chaotic evil, neutral evil, or chaotic neutral. Furthermore the weapon overcomes damage reduction as if it has all four of the alignment descriptors (chaotic, evil, good and lawful). Relic Power: with the proper divine connection you can command it to mutate for 6 rounds, taking on a different form and weapon property each round: 1 vicious morningstar; 2 flaming burst shortspear; 3 anarchic morningstar; 4 wounding battleaxe; 5 unholy morningstar; 6 vorpal longsword. It retains its normal enhancement bonus regardless of form; after the 6th round it again becomes a +1 morningstar until you speak the command word again. This ability functions five times per day. To use the relic power you must worship Erythnul and sacrifice a 5th-level divine spell slot or have the True Believer feat and at least 9 HD. [lore omitted]
facts: 7,308 gp; item level 11th; caster level 20th; activation Swift (command); prerequisites Craft Magic Arms and Armor, Sanctify Relic, circle of death
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When you wield it, a morningstar of the many functions as a +1 morningstar if you are chaotic evil, neutral evil, or chaotic neutral. Furthermore the weapon overcomes damage reduction as if it has all four of the alignment descriptors (chaotic, evil, good and lawful). Relic Power: with the proper divine connection you can command it to mutate for 6 rounds, taking on a different form and weapon property each round: 1 vicious morningstar; 2 flaming burst shortspear; 3 anarchic morningstar; 4 wounding battleaxe; 5 unholy morningstar; 6 vorpal longsword. It retains its normal enhancement bonus regardless of form; after the 6th round it again becomes a +1 morningstar until you speak the command word again. This ability functions five times per day. To use the relic power you must worship Erythnul and sacrifice a 5th-level divine spell slot or have the True Believer feat and at least 9 HD. [lore omitted] Relic: the printed alignment gate and worship or slot condition apply exactly as printed; outside them the item is a masterwork weapon.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 morningstar that overcomes DR as chaotic, evil, good and lawful; relic: six-round mutation (vicious morningstar, flaming burst shortspear, anarchic morningstar, wounding battleaxe, unholy morningstar, vorpal longsword), 5/day. Vorpal round follows the engine ruling: a confirmed natural 20 forces Head at Lethal.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
7,308 gp (item level 11) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### PHOENIX ASH THREAT
**MIC Weapon augment crystal — Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 500 gp (3rd) least; 2,000 gp (6th) lesser; 6,000 gp (10th) greater (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Weapon augment crystal
quality: clean
url: Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)
tooltip: Leaves smoldering embers on your enemies after every strike. Each round, at the start of your turn, the embers deal fire damage to each target struck by the weapon in the previous round. Least: a creature you hit takes 1 point of fire damage on the following round; multiple hits against the same target aren't cumulative. Lesser: 3 points of fire damage. Greater: 5 points of fire damage.
facts: prices (item level): 500 gp (3rd) least; 2,000 gp (6th) lesser; 6,000 gp (10th) greater; caster level 5th; activation —; prerequisites Craft Magic Arms and Armor, burning hands
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Leaves smoldering embers on your enemies after every strike. Each round, at the start of your turn, the embers deal fire damage to each target struck by the weapon in the previous round. Least: a creature you hit takes 1 point of fire damage on the following round; multiple hits against the same target aren't cumulative. Lesser: 3 points of fire damage. Greater: 5 points of fire damage. 3.5e ladder: Least = Magic rung, Lesser = Rare rung, Greater = Unique rung of the Crusader ladder.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Smoldering embers: 1 / 3 / 5 fire damage to each target hit last round, no stacking.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
500 gp (3rd) least; 2,000 gp (6th) lesser; 6,000 gp (10th) greater (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Flaming (Elemental 01-08): lingering fire the following round.

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### PICK OF PIERCING
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 9,308 gp (item level 12))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: Three times per day, you can touch any object created of force (such as Bigby's forceful hand or a wall of force) with this +1 heavy pick. Treat this touch as a touch attack against the touch AC provided by the spell or AC 0, if the spell does not provide the force effect with an AC of its own. A successful touch attack destroys the object as if you had cast disintegrate on it.
facts: 9,308 gp; item level 12th; caster level 11th; activation Free (command); prerequisites Craft Magic Arms and Armor, disintegrate
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Three times per day, you can touch any object created of force (such as Bigby's forceful hand or a wall of force) with this +1 heavy pick. Treat this touch as a touch attack against the touch AC provided by the spell or AC 0, if the spell does not provide the force effect with an AC of its own. A successful touch attack destroys the object as if you had cast disintegrate on it.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). 3/day, touch attack against a force object: disintegrate the object (wall of force, Bigby's hand).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
9,308 gp (item level 12) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### RAPIER OF DESPERATE MEASURES [RELIC]
**MIC Specific weapon (relic) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 9,320 gp (item level 12))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (relic)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When you wield a rapier of desperate measures, it functions as a +2 rapier if you are chaotic neutral, neutral, chaotic good, or chaotic evil. Relic Power: with the proper divine connection it gains the keen property (DMG 225) while you have fewer than your full normal hit points, and the speed property (DMG 225) while you have fewer than half your full normal hit points. To use the relic power you must worship Olidammara and sacrifice a 5th-level divine spell slot or have the True Believer feat and at least 9 HD. [lore omitted]
facts: 9,320 gp; item level 12th; caster level 20th; activation —; prerequisites Craft Magic Arms and Armor, Sanctify Relic, keen edge
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When you wield a rapier of desperate measures, it functions as a +2 rapier if you are chaotic neutral, neutral, chaotic good, or chaotic evil. Relic Power: with the proper divine connection it gains the keen property (DMG 225) while you have fewer than your full normal hit points, and the speed property (DMG 225) while you have fewer than half your full normal hit points. To use the relic power you must worship Olidammara and sacrifice a 5th-level divine spell slot or have the True Believer feat and at least 9 HD. [lore omitted] Relic: the printed alignment gate and worship or slot condition apply exactly as printed; outside them the item is a masterwork weapon.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +2 rapier; relic power: keen under full HP, speed under half HP (engine: speed applies the printed extra attack, not an extra GURPS step).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
9,320 gp (item level 12) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### RAPIER OF UNERRING DIRECTION [RELIC]
**MIC Specific weapon (relic) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 9,320 gp (item level 12))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (relic)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When you wield a rapier of unerring direction, it functions as a +1 ghost touch rapier. Relic Power: with the proper divine connection it automatically ignores all miss chances, whether they stem from concealment, blink, displacement, or some other source. To use the relic power you must worship Fharlanghn and sacrifice a 5th-level divine spell slot or have the True Believer feat and at least 9 HD. [lore omitted]
facts: 9,320 gp; item level 12th; caster level 20th; activation —; prerequisites Craft Magic Arms and Armor, Sanctify Relic, true seeing
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When you wield a rapier of unerring direction, it functions as a +1 ghost touch rapier. Relic Power: with the proper divine connection it automatically ignores all miss chances, whether they stem from concealment, blink, displacement, or some other source. To use the relic power you must worship Fharlanghn and sacrifice a 5th-level divine spell slot or have the True Believer feat and at least 9 HD. [lore omitted] Relic: the printed alignment gate and worship or slot condition apply exactly as printed; outside them the item is a masterwork weapon.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 ghost touch rapier; relic power ignores all miss chances from concealment, blink and displacement (Registry convention: miss chance is 3.5e side).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
9,320 gp (item level 12) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### RAPTOR ARROW [RELIC]
**MIC Specific weapon (relic, ammunition) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 6,006 gp (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (relic, ammunition)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When you fire a raptor arrow, it functions as a +1 arrow with a variant of the returning quality if you are neutral good, lawful good, chaotic good, or neutral. At the beginning of the round after it is fired from a bow, a raptor arrow flies through the air and restrings itself on the bow from which it was fired. Unlike most ammunition, raptor arrows are not destroyed when used. Relic Power: with the proper divine connection a raptor arrow also gains the bane property (DMG 224) against the targeted foe. To use the relic power you must worship Ehlonna and sacrifice a 4th-level divine spell slot or have the True Believer feat. [lore omitted]
facts: 6,006 gp; item level 10th; caster level 12th; activation — (ammunition); prerequisites Craft Magic Arms and Armor, Sanctify Relic, summon monster I
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When you fire a raptor arrow, it functions as a +1 arrow with a variant of the returning quality if you are neutral good, lawful good, chaotic good, or neutral. At the beginning of the round after it is fired from a bow, a raptor arrow flies through the air and restrings itself on the bow from which it was fired. Unlike most ammunition, raptor arrows are not destroyed when used. Relic Power: with the proper divine connection a raptor arrow also gains the bane property (DMG 224) against the targeted foe. To use the relic power you must worship Ehlonna and sacrifice a 4th-level divine spell slot or have the True Believer feat. [lore omitted] Relic: the printed alignment gate and worship or slot condition apply exactly as printed; outside them the item is a masterwork weapon.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 arrow with a returning variant (restrings the shooting bow next round, not destroyed); relic: bane against the targeted foe.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
6,006 gp (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### REVELATION CRYSTAL
**MIC Weapon augment crystal — Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 400 gp (2nd) least; 1,000 gp (4th) lesser; 5,000 gp (9th) greater (item level 9))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Weapon augment crystal
quality: clean
url: Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)
tooltip: Helps you battle foes who rely on invisibility. Least: when you damage an invisible creature with the weapon, the creature emits a glowing golden aura (as bright as a torch) for 1 round, revealing the square or squares it occupies and where it moves; attackers still suffer the 50% miss chance. Lesser: as least, and any active invisibility effects on the damaged creature are suppressed for 1 round (even if natural or extraordinary). Greater: as lesser, and it also suppresses active effects that grant concealment or similar (blur, displacement) for 1 round; no effect on concealment from the environment (fog, darkness).
facts: prices (item level): 400 gp (2nd) least; 1,000 gp (4th) lesser; 5,000 gp (9th) greater; caster level 9th; activation —; prerequisites Craft Magic Arms and Armor, true seeing
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Helps you battle foes who rely on invisibility. Least: when you damage an invisible creature with the weapon, the creature emits a glowing golden aura (as bright as a torch) for 1 round, revealing the square or squares it occupies and where it moves; attackers still suffer the 50% miss chance. Lesser: as least, and any active invisibility effects on the damaged creature are suppressed for 1 round (even if natural or extraordinary). Greater: as lesser, and it also suppresses active effects that grant concealment or similar (blur, displacement) for 1 round; no effect on concealment from the environment (fog, darkness). 3.5e ladder: Least = Magic rung, Lesser = Rare rung, Greater = Unique rung of the Crusader ladder.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Hit on an invisible creature: golden aura for 6 seconds, with greater rungs suppressing invisibility and then blur or displacement; miss chance stays 50%.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
400 gp (2nd) least; 1,000 gp (4th) lesser; 5,000 gp (9th) greater (item level 9) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### ROD OF SURPRISES
**MIC Specific weapon (rod) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 6,000 gp (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (rod)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: The rod's buttons cause it to lengthen and sprout a blade. It can be used as a javelin, kama, longspear, quarterstaff, scythe, shortspear, short sword, or spear, and is treated as a +1 weapon in any of these forms. The rod can store a message of up to twenty-five words as the magic mouth spell, replaying it when the triggering conditions are met; you can reset the message as a standard action. It can also lengthen up to 60 feet and support up to 800 pounds without bending.
facts: 6,000 gp; item level 10th; caster level 5th; activation Standard (manipulation); prerequisites Craft Magic Arms and Armor, Craft Rod, levitate, magic mouth, wood shape
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): The rod's buttons cause it to lengthen and sprout a blade. It can be used as a javelin, kama, longspear, quarterstaff, scythe, shortspear, short sword, or spear, and is treated as a +1 weapon in any of these forms. The rod can store a message of up to twenty-five words as the magic mouth spell, replaying it when the triggering conditions are met; you can reset the message as a standard action. It can also lengthen up to 60 feet and support up to 800 pounds without bending.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 in all eight forms (javelin, kama, longspear, quarterstaff, scythe, shortspear, short sword, spear); stores a 25-word magic mouth message; extends 60 ft and bears 800 lb.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
6,000 gp (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### ROD OF THE RECLUSE [RELIC]
**MIC Specific weapon (relic, rod) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 9,305 gp (item level 12))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (relic, rod)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When you wield this rod, it functions as a +2 light mace if you are chaotic evil, neutral evil, or chaotic neutral. Relic Power: with the proper divine connection you can activate the rod to deliver poison (Fort DC 20, 2d6 Str/2d6 Str) with the next melee attack you make with it. If you score a critical hit, the Strength damage from that blow (both initial and secondary) becomes Strength drain instead. This ability functions five times per day. To use the relic power you must worship Lolth and sacrifice a 6th-level divine spell slot or have the True Believer feat and at least 11 HD. [lore omitted]
facts: 9,305 gp; item level 12th; caster level 20th; activation Swift (command); prerequisites Craft Magic Arms and Armor, Craft Rod, Sanctify Relic, poison
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When you wield this rod, it functions as a +2 light mace if you are chaotic evil, neutral evil, or chaotic neutral. Relic Power: with the proper divine connection you can activate the rod to deliver poison (Fort DC 20, 2d6 Str/2d6 Str) with the next melee attack you make with it. If you score a critical hit, the Strength damage from that blow (both initial and secondary) becomes Strength drain instead. This ability functions five times per day. To use the relic power you must worship Lolth and sacrifice a 6th-level divine spell slot or have the True Believer feat and at least 11 HD. [lore omitted] Relic: the printed alignment gate and worship or slot condition apply exactly as printed; outside them the item is a masterwork weapon.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +2 light mace; relic: poison on next hit 5/day (Fort 20, 2d6 Str/2d6 Str; a crit makes it Strength drain); worshippers of Lolth. Resist roll: Quick Contest of the target's HT against an effective skill equal to the printed DC (20).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
9,305 gp (item level 12) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### SKEWER-OF-GNOMES [RELIC]
**MIC Specific weapon (relic) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 9,302 gp (item level 12))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (relic)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When you carry a skewer-of-gnomes, it functions as a Small +1 gnome bane spear if you are lawful evil, lawful neutral, or neutral evil. Relic Power: with the proper divine connection the spear also gains the unholy property (DMG 226) and reveals its quasisentience to you. A skewer-of-gnomes automatically sets itself against a charge, attacking and dealing double damage whenever a foe charges you; this attack uses your highest base attack bonus and all relevant modifiers, as if making an attack of opportunity. To use the relic power you must worship Kurtulmak and sacrifice a 5th-level divine spell slot or have the True Believer feat and at least 9 HD. [lore omitted]
facts: 9,302 gp; item level 12th; caster level 20th; activation —; prerequisites Craft Magic Arms and Armor, Sanctify Relic, unholy blight
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When you carry a skewer-of-gnomes, it functions as a Small +1 gnome bane spear if you are lawful evil, lawful neutral, or neutral evil. Relic Power: with the proper divine connection the spear also gains the unholy property (DMG 226) and reveals its quasisentience to you. A skewer-of-gnomes automatically sets itself against a charge, attacking and dealing double damage whenever a foe charges you; this attack uses your highest base attack bonus and all relevant modifiers, as if making an attack of opportunity. To use the relic power you must worship Kurtulmak and sacrifice a 5th-level divine spell slot or have the True Believer feat and at least 9 HD. [lore omitted] Relic: the printed alignment gate and worship or slot condition apply exactly as printed; outside them the item is a masterwork weapon.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Small +1 gnome bane spear; relic: unholy, quasisentience, auto set against a charge dealing double damage (attack at highest BAB).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
9,302 gp (item level 12) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### SPEAR OF RETRIBUTION [RELIC]
**MIC Specific weapon (relic) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 9,302 gp (item level 12))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (relic)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When you wield a spear of retribution, it functions as a +1 returning spear if you are chaotic evil, chaotic neutral, or neutral evil. Relic Power: with the proper divine connection you gain a +2 morale bonus on attack rolls and damage rolls made with the spear against any enemy that dealt damage to you in the previous round. Against an enemy that scored a critical hit against you in the previous round, the spear also gains the keen property (DMG 225). To use the relic power you must worship Gruumsh and sacrifice a 5th-level divine spell slot or have the True Believer feat and at least 9 HD. [lore omitted]
facts: 9,302 gp; item level 12th; caster level 20th; activation —; prerequisites Craft Magic Arms and Armor, Sanctify Relic, righteous might
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When you wield a spear of retribution, it functions as a +1 returning spear if you are chaotic evil, chaotic neutral, or neutral evil. Relic Power: with the proper divine connection you gain a +2 morale bonus on attack rolls and damage rolls made with the spear against any enemy that dealt damage to you in the previous round. Against an enemy that scored a critical hit against you in the previous round, the spear also gains the keen property (DMG 225). To use the relic power you must worship Gruumsh and sacrifice a 5th-level divine spell slot or have the True Believer feat and at least 9 HD. [lore omitted] Relic: the printed alignment gate and worship or slot condition apply exactly as printed; outside them the item is a masterwork weapon.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 returning spear; relic: +2 morale on attack and damage vs any enemy that damaged the wielder last round; keen vs one that critted.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
9,302 gp (item level 12) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### SPECTRAL DAGGER
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 6,000 gp (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When you grasp the hilt of a spectral dagger, a 'blade' of ghostly light coalesces. The weapon has no enhancement bonus (and can't be imbued with one). Attacks with it are treated as touch attacks, but the weapon does not deal damage normally. Instead, any target struck is affected by a chill touch spell (Fort DC 11 partial or Will DC 11 negates; see PH 209). It fades away if it leaves your hand, so it can't make ranged attacks.
facts: 6,000 gp; item level 10th; caster level 5th; activation —; prerequisites Craft Magic Arms and Armor, chill touch
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When you grasp the hilt of a spectral dagger, a 'blade' of ghostly light coalesces. The weapon has no enhancement bonus (and can't be imbued with one). Attacks with it are treated as touch attacks, but the weapon does not deal damage normally. Instead, any target struck is affected by a chill touch spell (Fort DC 11 partial or Will DC 11 negates; see PH 209). It fades away if it leaves your hand, so it can't make ranged attacks.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). No enhancement; attacks are touch attacks; a struck target suffers chill touch (HT contest vs 11 partial or Will vs 11 negates); fades if released. Resist roll: Quick Contest of the target's HT / Will against an effective skill equal to the printed DC (11).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
6,000 gp (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### SPIDER FANG
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 5,302 gp (item level 9))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: This +1 dagger quickly cuts through webs (magical or otherwise) without getting stuck. As a move action you can cut through a web entangling you or another creature. You can move through webs created by a web spell at half your normal speed (the weapon doesn't prevent you from being stuck in the first place). These are continuous effects. Once per day you can activate it to create a freestanding 10-foot-by-10-foot vertical curtain of cobwebs; it doesn't block movement but provides concealment to creatures behind it. Anyone touching the curtain causes it to collapse, dealing 2d4 points of acid damage to that creature.
facts: 5,302 gp; item level 9th; caster level 5th; activation — and standard (command); prerequisites Craft Magic Arms and Armor, Melf's acid arrow, web
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): This +1 dagger quickly cuts through webs (magical or otherwise) without getting stuck. As a move action you can cut through a web entangling you or another creature. You can move through webs created by a web spell at half your normal speed (the weapon doesn't prevent you from being stuck in the first place). These are continuous effects. Once per day you can activate it to create a freestanding 10-foot-by-10-foot vertical curtain of cobwebs; it doesn't block movement but provides concealment to creatures behind it. Anyone touching the curtain causes it to collapse, dealing 2d4 points of acid damage to that creature.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 dagger; cuts webs without sticking, half speed through web spells, 1/day 10x10 ft web curtain (concealment, collapses for 2d4 acid on touch).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
5,302 gp (item level 9) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### STAFF OF THE UNYIELDING OAK [RELIC]
**MIC Specific weapon (relic) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 5,600 gp (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (relic)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: A treant bound into quarterstaff form. When you wield it, it functions as a +1/+1 quarterstaff if you are neutral, neutral good, neutral evil, lawful neutral, or chaotic neutral. Relic Power: with the proper divine connection you can command the staff to become a treant (as the changestaff spell, except that the treant is fully real and can speak to other treants and animated trees). If in treant form it is reduced to 0 hit points or fewer, it reverts to staff form and cannot be used again for twenty-eight days. It can take treant form any number of times per day but can be in that form for only 12 hours overall in any one day. To use the relic power you must worship Obad-Hai and sacrifice an 8th-level divine spell slot or have the True Believer feat and at least 15 HD. [lore omitted]
facts: 5,600 gp; item level 10th; caster level 20th; activation Standard (command); prerequisites Craft Wondrous Item, Sanctify Relic, changestaff
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): A treant bound into quarterstaff form. When you wield it, it functions as a +1/+1 quarterstaff if you are neutral, neutral good, neutral evil, lawful neutral, or chaotic neutral. Relic Power: with the proper divine connection you can command the staff to become a treant (as the changestaff spell, except that the treant is fully real and can speak to other treants and animated trees). If in treant form it is reduced to 0 hit points or fewer, it reverts to staff form and cannot be used again for twenty-eight days. It can take treant form any number of times per day but can be in that form for only 12 hours overall in any one day. To use the relic power you must worship Obad-Hai and sacrifice an 8th-level divine spell slot or have the True Believer feat and at least 15 HD. [lore omitted] Relic: the printed alignment gate and worship or slot condition apply exactly as printed; outside them the item is a masterwork weapon.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1/+1 quarterstaff; relic: becomes a real treant (changestaff), 12 hours a day, 28 days of dormancy if reduced to 0 HP.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
5,600 gp (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### STONEREAVER
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 6,320 gp (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: In the hands of a nondwarf, stonereaver functions as a +1 greataxe. In the hands of a dwarf, the weapon also gains the bane property (DMG 224) against elementals that have the earth subtype and against constructs primarily made of earth, stone, or metal.
facts: 6,320 gp; item level 10th; caster level 8th; activation —; prerequisites Craft Magic Arms and Armor, stone shape
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): In the hands of a nondwarf, stonereaver functions as a +1 greataxe. In the hands of a dwarf, the weapon also gains the bane property (DMG 224) against elementals that have the earth subtype and against constructs primarily made of earth, stone, or metal.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 greataxe; in a dwarf's hands bane against earth elementals and constructs of earth, stone or metal.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
6,320 gp (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### STUNSHOT SLING
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 7,800 gp (item level 11))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: This weapon functions as a +1 sling. Three times per day, you can activate it so that the next target you hit on your current turn must succeed on a Fortitude save (DC equal to your attack roll result) or be stunned for 1 round.
facts: 7,800 gp; item level 11th; caster level 5th; activation Free (command); prerequisites Craft Magic Arms and Armor, sound burst
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): This weapon functions as a +1 sling. Three times per day, you can activate it so that the next target you hit on your current turn must succeed on a Fortitude save (DC equal to your attack roll result) or be stunned for 1 round.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 sling; 3/day free action: the next hit must beat a Fortitude save equal to the attack roll or be stunned 6 seconds (HT contest against the attack roll result).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
7,800 gp (item level 11) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### SWORD OF MIGHTY THEWS [RELIC]
**MIC Specific weapon (relic) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 9,350 gp (item level 12))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (relic)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When you wield a sword of mighty thews, it functions as a +1 dragonbane greatsword, provided you are chaotic good, neutral good, or chaotic neutral. Relic Power: with the proper divine connection you are immune to the frightful presence of dragons as long as you wield the sword, and you gain a +5 luck bonus on Reflex saves against a dragon's breath weapon. To use the relic power you must worship Kord and sacrifice a 5th-level divine spell slot or have the True Believer feat and at least 9 HD. [lore omitted]
facts: 9,350 gp; item level 12th; caster level 20th; activation —; prerequisites Craft Magic Arms and Armor, Sanctify Relic, antidragon aura (SC 14)
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When you wield a sword of mighty thews, it functions as a +1 dragonbane greatsword, provided you are chaotic good, neutral good, or chaotic neutral. Relic Power: with the proper divine connection you are immune to the frightful presence of dragons as long as you wield the sword, and you gain a +5 luck bonus on Reflex saves against a dragon's breath weapon. To use the relic power you must worship Kord and sacrifice a 5th-level divine spell slot or have the True Believer feat and at least 9 HD. [lore omitted] Relic: the printed alignment gate and worship or slot condition apply exactly as printed; outside them the item is a masterwork weapon.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 dragonbane greatsword; relic: immune to dragon frightful presence, +5 luck on Reflex saves vs breath weapons.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
9,350 gp (item level 12) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### SWORD OF VIRTUE BEYOND REPROACH [RELIC]
**MIC Specific weapon (relic) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 9,315 gp (item level 12))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (relic)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When you wield this weapon, it functions as a +1 holy longsword if you are lawful good, neutral good, or lawful neutral. Relic Power: with the proper divine connection, if you fail a save against an enemy's charm or compulsion effect while wielding the sword, you are immune to its effects for 1d4 rounds (DM rolls secretly). The effect is only suppressed during this time, not negated; when the suppression ends any effects received during previous rounds take effect. To use the relic power you must worship Heironeous and sacrifice a 6th-level divine spell slot or have the True Believer feat and at least 11 HD. [lore omitted]
facts: 9,315 gp; item level 12th; caster level 20th; activation —; prerequisites Craft Magic Arms and Armor, Sanctify Relic, mind blank
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When you wield this weapon, it functions as a +1 holy longsword if you are lawful good, neutral good, or lawful neutral. Relic Power: with the proper divine connection, if you fail a save against an enemy's charm or compulsion effect while wielding the sword, you are immune to its effects for 1d4 rounds (DM rolls secretly). The effect is only suppressed during this time, not negated; when the suppression ends any effects received during previous rounds take effect. To use the relic power you must worship Heironeous and sacrifice a 6th-level divine spell slot or have the True Believer feat and at least 11 HD. [lore omitted] Relic: the printed alignment gate and worship or slot condition apply exactly as printed; outside them the item is a masterwork weapon.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 holy longsword; relic: a failed save vs charm or compulsion is suppressed for 1d4 rounds (GM rolls secretly) and takes effect afterwards.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
9,315 gp (item level 12) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### SWORDBOW
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 6,375 gp (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: This +1 longbow changes into a +1 longsword (or vice versa) when activated; you can interchange bow and sword attacks as part of the same full attack action. In either form it has the same enhancement bonus, which can be improved as if improving two separate weapons (e.g. +1 to +2 costs 12,000 gp, as if improving two +1 weapons to +2). Special weapon properties cost twice the normal amount and apply to both weapons if possible; a property that can't apply to both (vorpal, distance) applies only to the swordbow in an eligible form, and a property that can apply in only one form does not cost double.
facts: 6,375 gp; item level 10th; caster level 5th; activation Free (command); prerequisites Craft Magic Arms and Armor, shrink item, elf
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): This +1 longbow changes into a +1 longsword (or vice versa) when activated; you can interchange bow and sword attacks as part of the same full attack action. In either form it has the same enhancement bonus, which can be improved as if improving two separate weapons (e.g. +1 to +2 costs 12,000 gp, as if improving two +1 weapons to +2). Special weapon properties cost twice the normal amount and apply to both weapons if possible; a property that can't apply to both (vorpal, distance) applies only to the swordbow in an eligible form, and a property that can apply in only one form does not cost double.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Free-command swap between +1 longbow and +1 longsword; the two forms share one enhancement bonus, improving it costs as two weapons.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
6,375 gp (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### SWORDBOW, GREAT
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 6,775 gp (item level 11))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: Functions as a swordbow, except that its two forms are a +1 composite longbow (+4 Str bonus) and a +1 greatsword. In either form it has the same enhancement bonus, which can be improved as if improving two separate weapons (e.g. +1 to +2 costs 12,000 gp, as if improving two +1 weapons to +2). Special weapon properties cost twice the normal amount and apply to both weapons if possible; a property that can't apply to both (vorpal, distance) applies only to the swordbow in an eligible form, and a property that can apply in only one form does not cost double.
facts: 6,775 gp; item level 11th; caster level 5th; activation Free (command); prerequisites Craft Magic Arms and Armor, shrink item, elf
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Functions as a swordbow, except that its two forms are a +1 composite longbow (+4 Str bonus) and a +1 greatsword. In either form it has the same enhancement bonus, which can be improved as if improving two separate weapons (e.g. +1 to +2 costs 12,000 gp, as if improving two +1 weapons to +2). Special weapon properties cost twice the normal amount and apply to both weapons if possible; a property that can't apply to both (vorpal, distance) applies only to the swordbow in an eligible form, and a property that can apply in only one form does not cost double.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Swordbow whose forms are +1 composite longbow (+4 Str) and +1 greatsword.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
6,775 gp (item level 11) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### SWORDBOW, LIGHT
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 6,330 gp (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: Functions as a swordbow, except that its two forms are a +1 shortbow and a +1 rapier. In either form it has the same enhancement bonus, which can be improved as if improving two separate weapons (e.g. +1 to +2 costs 12,000 gp, as if improving two +1 weapons to +2). Special weapon properties cost twice the normal amount and apply to both weapons if possible; a property that can't apply to both (vorpal, distance) applies only to the swordbow in an eligible form, and a property that can apply in only one form does not cost double.
facts: 6,330 gp; item level 10th; caster level 5th; activation Free (command); prerequisites Craft Magic Arms and Armor, shrink item, elf
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Functions as a swordbow, except that its two forms are a +1 shortbow and a +1 rapier. In either form it has the same enhancement bonus, which can be improved as if improving two separate weapons (e.g. +1 to +2 costs 12,000 gp, as if improving two +1 weapons to +2). Special weapon properties cost twice the normal amount and apply to both weapons if possible; a property that can't apply to both (vorpal, distance) applies only to the swordbow in an eligible form, and a property that can apply in only one form does not cost double.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Swordbow whose forms are +1 shortbow and +1 rapier.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
6,330 gp (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### THE FIST
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 7,005 gp (item level 11))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: The fist is a +1 adamantine spiked gauntlet. While wearing it, you are protected from chill metal and heat metal spells (continuous). In addition, once per day you can activate the fist: your next attack with the gauntlet before the end of your turn deals an extra 2d6 points of damage, knocks the target prone, and stuns it for 1 round (Fort DC 22 negates the stun and prone effects).
facts: 7,005 gp; item level 11th; caster level 15th; activation — and swift (command); prerequisites Craft Magic Arms and Armor, Bigby's clenched fist, endure elements
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): The fist is a +1 adamantine spiked gauntlet. While wearing it, you are protected from chill metal and heat metal spells (continuous). In addition, once per day you can activate the fist: your next attack with the gauntlet before the end of your turn deals an extra 2d6 points of damage, knocks the target prone, and stuns it for 1 round (Fort DC 22 negates the stun and prone effects).

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 adamantine spiked gauntlet; continuous protection from chill metal and heat metal; 1/day swift: extra 2d6, knockdown and stun 6 seconds (HT contest vs 22 negates). Resist roll: Quick Contest of the target's HT against an effective skill equal to the printed DC (22).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
7,005 gp (item level 11) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### TRIDENT OF SERENITY
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 5,315 gp (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When you activate this +1 trident, it creates a calm emotions effect centered on you (Will DC 16 negates). The effect lasts for 5 rounds and does not require concentration. Any creature that successfully saves is immune to further uses of that ability for 24 hours. This ability functions three times per day.
facts: 5,315 gp; item level 10th; caster level 5th; activation Standard (command); prerequisites Craft Magic Arms and Armor, calm emotions
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When you activate this +1 trident, it creates a calm emotions effect centered on you (Will DC 16 negates). The effect lasts for 5 rounds and does not require concentration. Any creature that successfully saves is immune to further uses of that ability for 24 hours. This ability functions three times per day.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 trident; 3/day calm emotions on the wielder for 30 seconds, Will contest vs 16; a creature that resists is immune 24 hours. Resist roll: Quick Contest of the target's Will against an effective skill equal to the printed DC (16).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
5,315 gp (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### TRUEDEATH CRYSTAL
**MIC Weapon augment crystal — Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 1,000 gp (4th) least; 5,000 gp (9th) lesser; 10,000 gp (12th) greater (item level 12))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Weapon augment crystal
quality: clean
url: Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)
tooltip: Least: the weapon deals an extra 1d6 points of damage to undead. Lesser: as least, and the weapon also functions as a ghost touch weapon (DMG 224). Greater: as lesser, and the weapon can deliver sneak attacks and critical hits against undead as if they were living creatures.
facts: prices (item level): 1,000 gp (4th) least; 5,000 gp (9th) lesser; 10,000 gp (12th) greater; caster level 5th; activation —; prerequisites Craft Magic Arms and Armor, consecrate
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Least: the weapon deals an extra 1d6 points of damage to undead. Lesser: as least, and the weapon also functions as a ghost touch weapon (DMG 224). Greater: as lesser, and the weapon can deliver sneak attacks and critical hits against undead as if they were living creatures. 3.5e ladder: Least = Magic rung, Lesser = Rare rung, Greater = Unique rung of the Crusader ladder.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1d6 vs undead; ghost touch; sneak attacks and crits against undead.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
1,000 gp (4th) least; 5,000 gp (9th) lesser; 10,000 gp (12th) greater (item level 12) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Bane (undead) and Ghost Touch in the weapon-affix corpus.

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### VIPERBLADE
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 6,302 gp (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: These +1 daggers secrete toxic venom. A viperblade has 5 charges, renewed each day at dawn. Spending 1 or more charges envenoms the blade (at no risk to you) for the next attack you make during this turn. The poison deals 1d6 points of Constitution damage (both primary and secondary). Save DC by charges spent: 1 charge Fort DC 12; 2 charges Fort DC 15; 3 charges Fort DC 18.
facts: 6,302 gp; item level 10th; caster level 7th; activation Swift (mental); prerequisites Craft Magic Arms and Armor, poison
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): These +1 daggers secrete toxic venom. A viperblade has 5 charges, renewed each day at dawn. Spending 1 or more charges envenoms the blade (at no risk to you) for the next attack you make during this turn. The poison deals 1d6 points of Constitution damage (both primary and secondary). Save DC by charges spent: 1 charge Fort DC 12; 2 charges Fort DC 15; 3 charges Fort DC 18.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 dagger, 5 charges: next hit envenomed, 1d6 Con (primary and secondary), Fort DC 12, 15 or 18 by charges spent (HT contest). Resist roll: Quick Contest of the target's HT against an effective skill equal to the printed DC (12, 15, 18).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
6,302 gp (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### WARLOCK'S SCEPTER
**MIC Specific weapon (rod) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 8,305 gp (item level 12))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (rod)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: This +1 light mace confers a +1 profane bonus on your ranged touch attack rolls while you hold it (continuous). It also has 5 charges, renewed each day at dawn; spending charges improves the damage of the next eldritch blast (CAr 7) you make that round: 1 charge +1d6; 3 charges +2d6; 5 charges +4d6. After the charges are expended the rod remains a +1 light mace but no longer provides the ranged touch bonus until its charges are restored.
facts: 8,305 gp; item level 12th; caster level 10th; activation — or swift (mental); prerequisites Craft Magic Arms and Armor, Craft Rod, bestow curse
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): This +1 light mace confers a +1 profane bonus on your ranged touch attack rolls while you hold it (continuous). It also has 5 charges, renewed each day at dawn; spending charges improves the damage of the next eldritch blast (CAr 7) you make that round: 1 charge +1d6; 3 charges +2d6; 5 charges +4d6. After the charges are expended the rod remains a +1 light mace but no longer provides the ranged touch bonus until its charges are restored.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 light mace; +1 profane on ranged touch attacks; charges add +1d6, +2d6 or +4d6 to the next eldritch blast.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
8,305 gp (item level 12) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### WHIP OF WEBS
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 6,301 gp (item level 10))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When you strike a creature with this +1 whip, you can activate it to wrap the target in a web of tough, leathery filaments. The creature is entangled as if by a net (PH 119) for 3 rounds or until it escapes. Multiple strikes aren't cumulative. This ability functions three times per day.
facts: 6,301 gp; item level 10th; caster level 6th; activation Free (command); prerequisites Craft Magic Arms and Armor, web
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When you strike a creature with this +1 whip, you can activate it to wrap the target in a web of tough, leathery filaments. The creature is entangled as if by a net (PH 119) for 3 rounds or until it escapes. Multiple strikes aren't cumulative. This ability functions three times per day.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 whip; 3/day on a hit entangle as a net for 18 seconds; no stacking.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
6,301 gp (item level 10) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### WITCHLIGHT RESERVOIR
**MIC Weapon augment crystal — Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)**
**Tier 3 — Heroic (levels 9-12)** (rule in `mic_pipeline.py`; printed price 5,000 gp (9th) (single item, considered a greater augment crystal) (item level 9))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Weapon augment crystal
quality: clean
url: Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)
tooltip: To imbue the crystal, directly expose it for 8 hours to sunlight, moonlight, blood or wine (at least one pint of the last two); exposing a full reservoir to a new substance replaces the old effect. When activated it adds an extra effect to the weapon's next successful melee strike (made before the end of your turn): Sunlight: +2d6 fire damage (or +4d6 if the target is undead). Moonlight: +2d6 electricity damage (or +4d6 if the target is a lycanthrope). Blood: +2d6 damage to a living target. Wine: -2 penalty on Will saves for 1 round. It functions five times before it loses its power and must be imbued again. [lore omitted]
facts: prices (item level): 5,000 gp (9th) (single item, considered a greater augment crystal); caster level 10th; activation Swift (mental); prerequisites Craft Magic Arms and Armor, burning hands, shocking grasp, touch of idiocy, vampiric touch
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): To imbue the crystal, directly expose it for 8 hours to sunlight, moonlight, blood or wine (at least one pint of the last two); exposing a full reservoir to a new substance replaces the old effect. When activated it adds an extra effect to the weapon's next successful melee strike (made before the end of your turn): Sunlight: +2d6 fire damage (or +4d6 if the target is undead). Moonlight: +2d6 electricity damage (or +4d6 if the target is a lycanthrope). Blood: +2d6 damage to a living target. Wine: -2 penalty on Will saves for 1 round. It functions five times before it loses its power and must be imbued again. [lore omitted] Single item; the book calls it a greater augment crystal (Unique rung).

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Expose 8 hours to sunlight, moonlight, blood or wine; swift activation adds +2d6 fire (+4d6 undead), +2d6 electricity (+4d6 lycanthropes), +2d6 to a living target, or -2 Will saves for 6 seconds; five uses then recharge.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
5,000 gp (9th) (single item, considered a greater augment crystal) (item level 9) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

## TIER 4 — COMPETENT (LEVELS 5-8)

### BOW OF THE WINTERMOON [RELIC]
**MIC Specific weapon (relic) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 4 — Competent (levels 5-8)** (rule in `mic_pipeline.py`; printed price 3,400 gp (item level 8))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (relic)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: When you wield this bow, it functions as a +1 composite longbow if you are chaotic good, neutral good, or chaotic neutral. It adjusts its pull automatically, allowing you to add your full Strength bonus to your damage roll with each arrow fired. Relic Power: with the proper divine connection this bow gains the frost and drow bane weapon properties (DMG 224). To use the relic power you must worship Corellon Larethian and sacrifice a 5th-level divine spell slot or have the True Believer feat and at least 9 HD. [lore omitted]
facts: 3,400 gp; item level 8th; caster level 20th; activation —; prerequisites Craft Magic Arms and Armor, Sanctify Relic, ice storm, summon monster I
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): When you wield this bow, it functions as a +1 composite longbow if you are chaotic good, neutral good, or chaotic neutral. It adjusts its pull automatically, allowing you to add your full Strength bonus to your damage roll with each arrow fired. Relic Power: with the proper divine connection this bow gains the frost and drow bane weapon properties (DMG 224). To use the relic power you must worship Corellon Larethian and sacrifice a 5th-level divine spell slot or have the True Believer feat and at least 9 HD. [lore omitted] Relic: the printed alignment gate and worship or slot condition apply exactly as printed; outside them the item is a masterwork weapon.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 composite longbow (full Strength bonus to damage) when wielded by the listed alignments; relic power: frost and drow bane properties (registered in the DMG/MIC property corpus).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
3,400 gp (item level 8) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### CRYSTAL OF ADAMANT WEAPONRY
**MIC Weapon augment crystal — Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)**
**Tier 4 — Competent (levels 5-8)** (rule in `mic_pipeline.py`; printed price 300 gp (2nd) least; 1,400 gp (5th) lesser; 3,400 gp (8th) greater (item level 8))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Weapon augment crystal
quality: clean
url: Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)
tooltip: Least: improves the hardness of a weapon by 2. Lesser: by 5. Greater: by 10.
facts: prices (item level): 300 gp (2nd) least; 1,400 gp (5th) lesser; 3,400 gp (8th) greater; caster level 9th; activation —; prerequisites Craft Magic Arms and Armor, diamondsteel (SC 64)
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Least: improves the hardness of a weapon by 2. Lesser: by 5. Greater: by 10. 3.5e ladder: Least = Magic rung, Lesser = Rare rung, Greater = Unique rung of the Crusader ladder.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Weapon Breakable DR improved by 2 / 5 / 10 steps on the Gadget (the hardness of 3.5e becomes Gadget DR).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
300 gp (2nd) least; 1,400 gp (5th) lesser; 3,400 gp (8th) greater (item level 8) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### CRYSTAL OF RETURN
**MIC Weapon augment crystal — Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)**
**Tier 4 — Competent (levels 5-8)** (rule in `mic_pipeline.py`; printed price 300 gp (2nd) least; 1,000 gp (4th) lesser; 4,000 gp (8th) greater (item level 8))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Weapon augment crystal
quality: clean
url: Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)
tooltip: Least: draw the weapon as a free action. Lesser: as least, and you can call the weapon (if unattended) to your hand from up to 30 feet away as a move action. Greater: as lesser, and the weapon gains the returning property (DMG 225), functioning only for a weapon designed to be thrown.
facts: prices (item level): 300 gp (2nd) least; 1,000 gp (4th) lesser; 4,000 gp (8th) greater; caster level 5th; activation —; prerequisites Craft Magic Arms and Armor, mage hand
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Least: draw the weapon as a free action. Lesser: as least, and you can call the weapon (if unattended) to your hand from up to 30 feet away as a move action. Greater: as lesser, and the weapon gains the returning property (DMG 225), functioning only for a weapon designed to be thrown. 3.5e ladder: Least = Magic rung, Lesser = Rare rung, Greater = Unique rung of the Crusader ladder.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Free draw; call from 30 ft (move action); greater adds returning on thrown weapons.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
300 gp (2nd) least; 1,000 gp (4th) lesser; 4,000 gp (8th) greater (item level 8) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Returning (DMG weapon property, registered in the weapon-affix corpus).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### CRYSTAL OF SECURITY
**MIC Weapon augment crystal — Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)**
**Tier 4 — Competent (levels 5-8)** (rule in `mic_pipeline.py`; printed price 300 gp (2nd) least; 1,000 gp (4th) lesser; 3,000 gp (7th) greater (item level 7))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Weapon augment crystal
quality: clean
url: Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)
tooltip: Least: +2 bonus on any check made to draw the weapon (such as when grappling) or to keep it in your hand (such as an opposed disarm check or opposed Strength check if you and an opponent both grab it). Lesser: bonus +5. Greater: bonus +10.
facts: prices (item level): 300 gp (2nd) least; 1,000 gp (4th) lesser; 3,000 gp (7th) greater; caster level 5th; activation —; prerequisites Craft Magic Arms and Armor, bull's strength
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Least: +2 bonus on any check made to draw the weapon (such as when grappling) or to keep it in your hand (such as an opposed disarm check or opposed Strength check if you and an opponent both grab it). Lesser: bonus +5. Greater: bonus +10. 3.5e ladder: Least = Magic rung, Lesser = Rare rung, Greater = Unique rung of the Crusader ladder.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +2 / +5 / +10 on checks to draw or keep the weapon (grappling, disarm, Strength contest).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
300 gp (2nd) least; 1,000 gp (4th) lesser; 3,000 gp (7th) greater (item level 7) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### METEORIC KNIFE
**MIC Specific weapon — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 4 — Competent (levels 5-8)** (rule in `mic_pipeline.py`; printed price 2,802 gp (item level 7))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: This knife functions as a +1 dagger. In addition, it has three charges, which are renewed each day at dawn. Spending charges enhances the dagger for 1 round: 1 charge: the dagger gains the returning property. 2 charges: the flaming and returning properties. 3 charges: the flaming and returning properties and, if it hits a creature, it deals normal damage and creates an explosion of fire that deals an extra 3d6 points of fire damage to the target and all creatures adjacent to it (Reflex DC 14 half).
facts: 2,802 gp; item level 7th; caster level 11th; activation Swift (command); prerequisites Craft Magic Arms and Armor, fireball, telekinesis
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): This knife functions as a +1 dagger. In addition, it has three charges, which are renewed each day at dawn. Spending charges enhances the dagger for 1 round: 1 charge: the dagger gains the returning property. 2 charges: the flaming and returning properties. 3 charges: the flaming and returning properties and, if it hits a creature, it deals normal damage and creates an explosion of fire that deals an extra 3d6 points of fire damage to the target and all creatures adjacent to it (Reflex DC 14 half).

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). +1 dagger, 3 charges per day: 1 returning for 6 seconds; 2 flaming and returning; 3 flaming, returning and on a hit +3d6 fire to target and adjacent (Dodge contest vs 14 for half). Resist roll: Quick Contest of the target's Dodge against an effective skill equal to the printed DC (14).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
2,802 gp (item level 7) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

## TIER 5 — BASELINE (LEVELS 1-4)

### ARROW OF BITING
**MIC Specific weapon (ammunition) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 5 — Baseline (levels 1-4)** (rule in `mic_pipeline.py`; printed price 506 gp (item level 3))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (ammunition)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: This +1 arrow injects any creature it strikes with poison (injury, Fort DC 16, 1d6 Con/1d6 Con). An arrow of biting can also be created as a crossbow bolt for the same price.
facts: 506 gp; item level 3rd; caster level 7th; activation — (ammunition); prerequisites Craft Magic Arms and Armor, poison
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): This +1 arrow injects any creature it strikes with poison (injury, Fort DC 16, 1d6 Con/1d6 Con). An arrow of biting can also be created as a crossbow bolt for the same price.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Innate Attack follow-up: injury poison (Toxic), primary at once and secondary one minute later, 1d6 as-is, resisted by HT vs 16. Resist roll: Quick Contest of the target's HT against an effective skill equal to the printed DC (16).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
506 gp (item level 3) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### CRYSTAL OF ILLUMINATION
**MIC Weapon augment crystal — Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)**
**Tier 5 — Baseline (levels 1-4)** (rule in `mic_pipeline.py`; printed price 100 gp (1st) least; 400 gp (2nd) lesser; 1,000 gp (4th) greater (item level 4))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Weapon augment crystal
quality: clean
url: Magic Item Compendium, ch.2 Weapon Augment Crystals, PDF pp. 65-67 (augment rules DMG-style MIC p. 221)
tooltip: Activating causes your weapon to glow. Least: bright illumination in a 5-foot radius and shadowy illumination for 5 feet beyond. Lesser: 20-foot radius and 20 feet beyond. Greater: 60-foot radius and 60 feet beyond.
facts: prices (item level): 100 gp (1st) least; 400 gp (2nd) lesser; 1,000 gp (4th) greater; caster level 5th; activation Swift (command); prerequisites Craft Magic Arms and Armor, daylight
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): Activating causes your weapon to glow. Least: bright illumination in a 5-foot radius and shadowy illumination for 5 feet beyond. Lesser: 20-foot radius and 20 feet beyond. Greater: 60-foot radius and 60 feet beyond. 3.5e ladder: Least = Magic rung, Lesser = Rare rung, Greater = Unique rung of the Crusader ladder.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Swift command: light radius 5 / 20 / 60 ft with equal shadowy ring.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
100 gp (1st) least; 400 gp (2nd) lesser; 1,000 gp (4th) greater (item level 4) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

### FOUNTAINHEAD ARROW
**MIC Specific weapon (ammunition) — Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64**
**Tier 5 — Baseline (levels 1-4)** (rule in `mic_pipeline.py`; printed price 306 gp (item level 2))

## SOURCE (normalized transcription of the OCR; see packet header)
```
group: Specific weapon (ammunition)
quality: clean
url: Magic Item Compendium, ch.2 Weapons (specific weapons), PDF pp. 47-64
tooltip: A fountainhead arrow is an otherwise normal arrow designed to be targeted at a point on the ground, a wall, or any other flat surface. If you hit the target area (treat as AC 5), the arrow creates a geyser of spewing acid. Each round on your turn (starting on the turn you fired the arrow), the arrow creates a 10-foot-radius burst of acid that deals 2d8 points of acid damage to all creatures in the area (Reflex DC 14 half). This effect continues for 3 rounds. It can be created as a crossbow bolt for the same price.
facts: 306 gp; item level 2nd; caster level 11th; activation — (ammunition); prerequisites Craft Magic Arms and Armor, Melf's acid arrow
gaps: none
```

## D&D 3.5e
Rules as printed in MIC (restated in the source block): A fountainhead arrow is an otherwise normal arrow designed to be targeted at a point on the ground, a wall, or any other flat surface. If you hit the target area (treat as AC 5), the arrow creates a geyser of spewing acid. Each round on your turn (starting on the turn you fired the arrow), the arrow creates a 10-foot-radius burst of acid that deals 2d8 points of acid damage to all creatures in the area (Reflex DC 14 half). This effect continues for 3 rounds. It can be created as a crossbow bolt for the same price.

## GURPS 4e
Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). Hit on a point (AC 5): geyser of acid, 10-ft radius burst each turn for 18 seconds, Innate Attack Corrosion 2d8 as-is, Dodge contest vs 14 for half. Resist roll: Quick Contest of the target's Dodge against an effective skill equal to the printed DC (14).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
306 gp (item level 2) (printed MIC market price; crystals priced per rung).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none (specific item; no affix family involved).

## NAME COLLISION
none found (checked entity files of the other corpora and the Registry lexicon by name).

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `mic_translations.py` header. Extraction quality: clean.


---

## COVERED BY AN EXISTING REGISTRY ROW (no second document)

| Enchant | Existing row | Note |
|---|---|---|

## OPEN VERIFICATION ITEMS

- Storm Gauntlets: the entry text was not in the OCR range read (only an art caption on p. 59); excluded and recorded as a gap.
- PDF pp. 59-60 are two-column interleaved in the OCR: Rod of Whips (15,000 gp, 14th, CL 12th), Rogue Blade (12,320 gp, 13th, CL 6th) and Ruby Blade figures were assigned from layout; confirm against the page image.
- Prices, caster levels and DCs are as the OCR showed them after normalizing obvious noise ('sth' read as 5th, 'dé' as d6); confirm any figure that drives play against the printed page.
- Relic items: Moradin, Corellon, Hextor, Tiamat, St. Cuthbert, Vecna, Pelor, Garl Glittergold, Erythnul, Olidammara, Fharlanghn, Ehlonna, Lolth, Wee Jas, Kurtulmak, Gruumsh, Obad-Hai, Kord and Heironeous are named as printed; map to campaign deities before placing one.
