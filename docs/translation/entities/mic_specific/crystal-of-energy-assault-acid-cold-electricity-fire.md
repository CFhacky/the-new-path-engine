# CRYSTAL OF ENERGY ASSAULT (ACID, COLD, ELECTRICITY, FIRE)
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
