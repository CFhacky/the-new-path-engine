# FIENDSLAYER CRYSTAL
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
