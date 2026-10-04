# ELEMENTAL FORCE
**WoW weapon enchant — Profession, Mists of Pandaria (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Elemental_Force)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Mists of Pandaria
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Elemental_Force
tooltip: "Permanently enchants a melee weapon to sometimes inflict 58 additional Elemental damage when dealing damage with spells and melee attacks. Cannot be applied to items higher than level 50."
facts: reagents 3 Mysterious Essence; several squishes; patch 5.0.4 added.
gaps: proc rate NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire +1d6 damage of a random element (the Prismatic Magic-rung rider; the source's 58 'Elemental damage'). Works on damaging spells and melee hits. Level cap in the source (items up to level 50) is dropped.

## GURPS 4e
On the same d100: Innate Attack Follow-Up 1d of a randomly chosen energy type.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Prismatic (Elemental 69-74).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Proc rate not in the source (10%). 2. The source's item-level cap of 50 is a game-balance cap with no 3.5e meaning.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
