# RUNE OF SPELLSHATTERING
**WoW weapon enchant — Death knight runeforging (https://warcraft.wiki.gg/wiki/Rune_of_Spellshattering)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Death knight runeforging
quality: clean
url: https://warcraft.wiki.gg/wiki/Rune_of_Spellshattering
tooltip: "Affixes your two-handed rune weapon with a rune that deflects 4% of all spell damage and reduces the duration of Silence effects by 50%."
facts: level 57; cast time 5 seconds; removed 7.0.3.
gaps: none.
```

## D&D 3.5e
As Spellbreaking on a two-handed weapon at double the step: each damaging spell that hits the wielder deals 2 less damage (source 4%), Silence on the wielder lasts half as long.

## GURPS 4e
Damage Resistance 2 against spell damage only and Silence duration halved.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Spell Ward (Defensive 37-42).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Same flat-point reading as Spellbreaking.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
