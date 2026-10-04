# JADE SPIRIT
**WoW weapon enchant — Profession, Mists of Pandaria (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Jade_Spirit)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Mists of Pandaria
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Jade_Spirit
tooltip: "Permanently enchants a melee weapon to sometimes increase your Intellect by 65 when healing or dealing damage with spells. If less than 25% of your mana remains when the effect is triggered, your Versatility will also increase by 30."
facts: item level cap 136; reagents 4 Mysterious Essence, 10 Sha Crystal; patch 5.0.4 added.
gaps: proc rate and duration NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging or healing spell cast by the wielder, 01-10 fires. On fire: +2 Intelligence (untyped) for 3 rounds (source +65 Intellect; duration not given). If the wielder has used more than 75% of a mana pool, also +1 on spell damage (the source's Versatility +30 below 25% mana).

## GURPS 4e
On the same d100: IQ +1; if Energy Reserve is below a quarter, also +1 damage on attack spells, 15 seconds assumed.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Duration and proc rate not in the source (3 rounds, 10%).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
