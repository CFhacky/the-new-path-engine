# ICY CHILL
**WoW weapon enchant — Profession, Classic (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Icy_Chill)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Classic
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Icy_Chill
tooltip: "Permanently enchant a melee weapon to often chill the target, reducing their movement and attack speed. Has a reduced effect for players above level 60."
facts: enchanting skill 285-300; item level cap 136; reagents 4 Large Brilliant Shard, 1 Essence of Water, 1 Essence of Air, 1 Icecap. Secondary (wiki Icy Chill spell page via search): frost debuff, movement slowed by 30%, time between attacks increased by 25%, for 5 seconds. Patch 2.3.2 changed functionality (no numbers given).
gaps: proc rate or PPM NOT PRESENT (page notes it is unclear whether PPM or chance on hit).
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire the target is chilled for 1 round (5 s): land speed x0.7 (round down to 5 ft) and -1 on attack rolls (the source's 25% longer time between attacks, at one step). No save (the source gives none), no SR. Melee weapons only. Does not stack with itself.

## GURPS 4e
On a damaging hit that fires: Affliction (Reduced Move 30% and -1 to skill with weapon attacks), exactly 5 seconds, no resistance roll. Same d100 as 3.5e.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Slowing (Condition 01-08).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Proc rate is not in the source (page says unclear PPM versus chance on hit); default 10% per damaging hit. 2. Slow is lighter than the Slowing row (no save, 1 round, speed x0.7), as the source's 30% implies.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
