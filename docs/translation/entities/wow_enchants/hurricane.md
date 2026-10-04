# HURRICANE
**WoW weapon enchant — Profession, Cataclysm (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Hurricane)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Cataclysm
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Hurricane
tooltip: "Permanently enchant a melee weapon to sometimes increase haste by 74 for 12 sec when healing or dealing spell or melee damage."
facts: internal cooldown 45 seconds; approximately 10-15% proc; item level cap 136; reagents 6 Heavenly Shard, 6 Volatile Air; patch 4.0.3a added.
gaps: none.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On a damaging hit or spell, then not again for 8 rounds (45 s internal cooldown): +1 untyped bonus on attack rolls and +2 initiative for 2 rounds (the source's +74 haste rating, 12 s; haste is read as one attack-step plus initiative). Healing spells also roll it.

## GURPS 4e
On the same d100: +1 skill with weapon attacks and +2 to initiative-type reaction rolls for exactly 12 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Haste rating to a +1 step is an interpretation; flagged. 2. Source proc about 10-15%; 10% used.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
