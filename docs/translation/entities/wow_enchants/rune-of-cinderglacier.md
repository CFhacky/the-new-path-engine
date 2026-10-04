# RUNE OF CINDERGLACIER
**WoW weapon enchant — Death knight runeforging (https://warcraft.wiki.gg/wiki/Rune_of_Cinderglacier)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Death knight runeforging
quality: clean
url: https://warcraft.wiki.gg/wiki/Rune_of_Cinderglacier
tooltip: "Affixes your rune weapon with a rune that has a chance to increase the damage by 20% of your next 2 spells that deal Frost or Shadow damage. Lasts 30 sec."
facts: spell ID 53341; duration 30 seconds; patch 3.0.2 added; patch 6.0.2 removed.
gaps: proc rate NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire, the wielder's next two cold or negative-energy damaging effects within 5 rounds (30 s) each deal +2 damage (the source's +20% on typical Magic-rung damage). Class lock as Razorice.

## GURPS 4e
On the same d100: the next two cold or Toxic [Cosmic] attacks within exactly 30 seconds gain +2 damage each.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Proc rate not in the source (default 10%). 2. 20% to flat +2 is an interpretation.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
