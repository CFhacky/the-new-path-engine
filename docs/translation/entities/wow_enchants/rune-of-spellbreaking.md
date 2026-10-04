# RUNE OF SPELLBREAKING
**WoW weapon enchant — Death knight runeforging (https://warcraft.wiki.gg/wiki/Rune_of_Spellbreaking)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Death knight runeforging
quality: clean
url: https://warcraft.wiki.gg/wiki/Rune_of_Spellbreaking
tooltip: "Affixes your one-handed rune weapon with a rune that deflects 2% of all spell damage and reduces the duration of Silence effects by 50% (not cumulative with additional Silence duration reduction)."
facts: level 57; patch 3.2.0 now reduces damage from Holy spells; removed 7.0.3.
gaps: none.
```

## D&D 3.5e
While wielded: each damaging spell that hits the wielder deals 1 less damage (minimum 0; the source deflects 2% of spell damage, which at the Magic rung is 1 point), and Silence effects on the wielder last half as long (rounded down, minimum 1 round). One-handed weapons only.

## GURPS 4e
Damage Resistance 1 against spell damage only (Gadget; Only vs spells -20%) and Silence duration halved.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Spell Ward (Defensive 37-42).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Percentage deflection to a flat point; flagged.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
