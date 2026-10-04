# PREVENT MONSTER HEAL
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "stops monster damage regeneration for 80 minutes (120,000 frames)"
facts: applied only by player characters (not mercenaries or iron golems); only if the monster takes damage; cannot be applied to Uber/Pandemonium event bosses (Lilith, Duriel, Izual, Mephisto, Diablo, Baal).
gaps: none.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires. On fire the target cannot regenerate or benefit from fast healing for 80 minutes (the source's duration); magical healing and potions still work. Not applied by allies or summoned creatures, and not against named bosses.

## GURPS 4e
On the same d100: regeneration and fast healing suppressed for 80 minutes.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Cursed Wound (Condition 55-60).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. The source applies it on every damaging hit (no chance); the ratified 10% proc is used to keep it a Registry-style proc. 2. Named bosses are immune (the source's list of event bosses).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.
