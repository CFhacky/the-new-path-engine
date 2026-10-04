# CRYSTAL OF LIFE DRINKING
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
