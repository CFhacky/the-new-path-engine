# HIT CAUSES MONSTER TO FLEE
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "causes the target to flee in the direction opposite of the attacker due to applying a flee effect"
facts: only normal and minion monsters; applied by any melee or ranged attack except blade sentinel, blade shield and extra multishot arrows; the target may keep fleeing after the effect expires until its next AI check; cannot overwrite grim ward or terror; if applied with Hit Blinds Target, flee takes precedence.
gaps: duration NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires. On fire the target must succeed on a Will save (DC 13) or flee from the attacker for 1d4 rounds (fear). Creatures of 17+ Hit Dice and mindless creatures are immune. Flee takes precedence over blind.

## GURPS 4e
On the same d100: Quick Contest Will against effective skill 13; on failure Terror for 1d4 seconds-rounds (4 to 24 seconds), exact 1d4 x 6 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Terrifying (Condition 25-30).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Duration is not in the source (1d4 rounds is the Terrifying row's). 2. The source's monsters 'may continue fleeing after expiry until their next AI check' has no 3.5e meaning.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.
