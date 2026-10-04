# DANCING STEEL
**WoW weapon enchant — Profession, Mists of Pandaria (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Dancing_Steel)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Mists of Pandaria
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Dancing_Steel
tooltip: "Permanently enchants a melee weapon to sometimes increase your Strength or Agility by 81 when dealing melee damage. Your highest stat is always chosen."
facts: item level cap 136; patch 5.2.0 15% increased chance to activate; patch 5.0.4 added; reagents 12 Spirit Dust, 10 Sha Crystal.
gaps: proc rate and duration NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire for 3 rounds: +4 to Strength or Dexterity, whichever score is higher (untyped; source: +81 Strength or Agility, the highest stat is always chosen). Re-proc refreshes; two weapons stack.

## GURPS 4e
On the same d100: ST or DX +2 (the higher), exactly 15 seconds assumed.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Mongoose (this corpus).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Duration and proc rate are not in the source (3 rounds and 10% assumed). 2. Same rung as Mongoose, which it mirrors.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
