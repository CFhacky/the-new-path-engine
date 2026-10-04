# MONGOOSE
**WoW weapon enchant — Profession, Burning Crusade (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Mongoose)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Burning Crusade
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Mongoose
tooltip: "Permanently enchant a melee weapon to occasionally increase Agility by 60 and haste by 15. Cannot be applied to items higher than level 600."
facts: current page values (scaled down from the original). Secondary (search, original TBC): +120 Agility and 30 haste rating, lasts 15 seconds, proc most likely normalized to 1 PPM. Reagents 40 Arcane Dust, 8 Greater Planar Essence, 10 Large Prismatic Shard, 6 Void Crystal.
gaps: PPM NOT PRESENT on the page itself.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire: +4 Dexterity (untyped) for 3 rounds, applying to attack, AC, Reflex and Dex skills (source original: +120 Agility, 15 s). The source's +30 haste rating is under one step and is dropped. Re-proc on the same weapon refreshes and does not stack; two Mongoose weapons stack (untyped, as Crusader).

## GURPS 4e
On the same d100: DX +2 for exactly 15 seconds (the 3.5e +4 at 2:1), refreshed by a same-weapon re-proc, stacking across two weapons.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. The current wiki tooltip is scaled down (60 Agility, 15 haste); the original TBC values (+120, 30 haste rating, 15 s, about 1 PPM) come from a search snippet and are what this entry uses. 2. Haste is dropped as below one step.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
