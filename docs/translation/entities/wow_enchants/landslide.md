# LANDSLIDE
**WoW weapon enchant — Profession, Cataclysm (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Landslide)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Cataclysm
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Landslide
tooltip: "Permanently enchant a weapon to sometimes increase attack power by 100 for 12 sec when striking in melee."
facts: 1 PPM, no internal cooldown, can refresh itself; item level cap 600; patch 4.0.3a added; reagents 6 Hypnotic Dust, 5 Greater Celestial Essence, 5 Heavenly Shard, 5 Maelstrom Crystal.
gaps: none.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire for 2 rounds (12 s): +2 on melee damage rolls (untyped; source +100 attack power at 1 PPM). Re-proc refreshes; two weapons stack.

## GURPS 4e
On the same d100: Striking ST +1 for exactly 12 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Striking (Offensive 01-06).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
