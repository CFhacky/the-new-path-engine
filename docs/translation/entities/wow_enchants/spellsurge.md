# SPELLSURGE
**WoW weapon enchant — Profession, Burning Crusade (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Spellsurge)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Burning Crusade
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Spellsurge
tooltip: "Permanently enchant a melee weapon to make your spells sometimes restore 100 mana to nearby party members. Cannot be applied to items higher than level 600."
facts: 3% chance on spell cast to restore 100 mana to all party members over 10 seconds; item level cap 600; reagents 12 Large Prismatic Shard, 10 Greater Planar Essence, 20 Arcane Dust.
gaps: patch changes NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each spell the wielder casts, 01-03 fires (the source's 3%). On fire every ally within 30 ft, wielder included, recovers 5 mana (the Souldrinker Magic-rung value; source: 100 mana over 10 s to party members). Hybrid campaign note: only characters who carry a mana pool benefit. Melee weapon, spells cast by the wielder.

## GURPS 4e
On the same d100 (per spell cast): Energy Reserve recovery of 5 points to each ally within 10 yards.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Mana scale: 100 mana at the source's level is rescaled to the pool's Souldrinker rung; default 5 mana.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
