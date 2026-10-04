# PIERCING ATTACK
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "Adds a chance to missile weapon attacks to Pierce the target when hit, and hit subsequent targets behind them"
facts: percent summed from all sources; blocking does not stop a piercing missile; a missile can pierce up to 4 times (5 targets); per-item chances: Stormstrike 25%, Gut Siphon 33%, Razortail 33%, Doomslinger 35%, Kuko Shakaku 50%, Ichorsting 50%, Warshrike 50%, Demon Machine 66%, Buriza-Do Kyanon 100%.
gaps: none.
```

## D&D 3.5e
Ranged weapons only. On each damaging hit, d100 01-25 fires (the Magic-rung of the source's 25 to 100% item values): the missile continues to the next creature in a straight line within 10 ft behind the target, which is attacked as normal; this repeats up to 4 times (5 targets). A shield or block does not stop the missile.

## GURPS 4e
On the same d100: the missile continues to the next target behind, up to 4 times; each target gets its own active defenses.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. The source chance is set per item (25 to 100%); 25% is the Magic rung. 2. 'Behind the target' is read as a line within 10 ft.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.
