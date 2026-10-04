# RUNE OF SWORDSHATTERING
**WoW weapon enchant — Death knight runeforging (https://warcraft.wiki.gg/wiki/Rune_of_Swordshattering)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Death knight runeforging
quality: clean
url: https://warcraft.wiki.gg/wiki/Rune_of_Swordshattering
tooltip: "Affixes your two-handed rune weapon with a rune that increases Parry chance by 4% and reduces the duration of Disarm effects by 50%."
facts: level 63; same patch history as Swordbreaking.
gaps: none.
```

## D&D 3.5e
As Swordbreaking on a two-handed weapon, at double the parry step: +2 dodge bonus to AC (source +4% parry), +4 on checks to avoid being disarmed, disarmed weapon recovered as a move action.

## GURPS 4e
Enhanced Parry +2 and +4 to resist Disarm; recovery in half the time.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Bladesinger (Skill/Class 31-36).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Same disarm reading as Swordbreaking.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
