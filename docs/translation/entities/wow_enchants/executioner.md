# EXECUTIONER
**WoW weapon enchant — Profession, Burning Crusade (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Executioner)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Burning Crusade
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Executioner
tooltip: "Permanently enchant a melee weapon to occasionally grant you 60 critical strike rating."
facts: patch 4.0.1 (2010-10-12) changed from armor penetration to critical strike rating; patch 3.3.3 (2010-03-23) only one instance of the effect active at a time; item level cap 600. Secondary (search, original): ignores 840 armor for 15 seconds. Reagents 6 Void Crystal, 10 Large Prismatic Shard, 6 Greater Planar Essence, 30 Arcane Dust, 3 Elixir of Major Strength.
gaps: proc rate NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire, for 3 rounds the wielder's attacks ignore worn DR (the engine's ignores-armor flag; source original: ignores 840 armor for 15 s). Natural toughness is not ignored. Only one instance active at a time (source patch 3.3.3). The current crit-rating version (+60 crit rating) is the later redesign and is not used.

## GURPS 4e
On the same d100: for exactly 15 seconds the wielder's attacks skip worn DR (ignores_armor flag), natural DR still applies.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Armor Piercing (Offensive 19-24).

## NAME COLLISION
Pool affix 'Executioner' (Offensive 37-42, bonus damage vs bloodied targets): different mechanic; names stay, never merge. Also the Armor Piercing row is a flat ignore-DR value, not a timed proc.

## FORKS NEEDING A RULING
1. Armor-penetration amount is from a search snippet (840); proc rate not in the source (default 10%).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
