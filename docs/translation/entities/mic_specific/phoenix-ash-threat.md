# PHOENIX ASH THREAT
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
