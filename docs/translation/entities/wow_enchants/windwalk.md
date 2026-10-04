# WINDWALK
**WoW weapon enchant — Profession, Cataclysm (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Windwalk)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Cataclysm
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Windwalk
tooltip: "Permanently enchant a weapon to sometimes increase dodge by 99 and movement speed by 10% for 10 sec when striking in melee, stacking with passive movement speed effects."
facts: no internal cooldown, can refresh itself; item level cap 136; patch 4.0.3a added.
gaps: proc rate NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire for 2 rounds: +1 dodge bonus to AC and +5 ft land speed (source: +99 dodge rating and +10% movement speed, 10 s, no internal cooldown, refreshes itself). Re-proc refreshes.

## GURPS 4e
On the same d100: Enhanced Dodge +1 and Enhanced Move (Ground) 0.5 for exactly 10 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Swiftfoot (Utility 01-06).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Proc rate not in the source (default 10%).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
