# WINDSONG
**WoW weapon enchant — Profession, Mists of Pandaria (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Windsong)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Mists of Pandaria
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Windsong
tooltip: "Permanently enchants a melee weapon to sometimes increase your critical strike, haste, or mastery by 59 for 12 sec when dealing damage or healing with spells and melee attacks."
facts: item level cap 136; reagents 12 Spirit Dust, 1 Ethereal Shard; patch 5.0.4 added; hotfixes 2012-10-12 and 2012-10-16 (periodic effects can activate it; no longer removes Stealth).
gaps: proc rate NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire roll d3: 1 = +1 on confirmation rolls for critical hits, 2 = +1 on attack rolls, 3 = +1 damage; all untyped, 2 rounds (the source randomly picks crit, haste or mastery at +59 for 12 s). Heals and spells also roll it.

## GURPS 4e
On the same d100 plus a d3: +1 to confirm crits, +1 skill, or +1 damage, exactly 12 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Ratings read as +1 steps; flagged. 2. Proc rate not in the source (10%).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
