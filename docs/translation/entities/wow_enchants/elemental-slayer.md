# ELEMENTAL SLAYER
**WoW weapon enchant — Profession, Cataclysm (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Elemental_Slayer)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Cataclysm
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Elemental_Slayer
tooltip: "Permanently enchant a melee weapon to sometimes disrupt elementals when struck by your melee attacks, dealing Arcane damage and silencing them for 5 sec."
facts: item level cap 600; reagents 7 Hypnotic Dust, 2 Heavenly Shard, 1 Greater Celestial Essence.
gaps: proc rate, damage amount NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). Against creatures of the elemental type: +1d6 force damage (the source's Arcane damage; force is the 3.5e arcane damage type) and the target cannot cast spells or use spell-like abilities for 1 round (source: silenced 5 s). No save. Melee only.

## GURPS 4e
On the same d100, against Elemental-type foes: Innate Attack Crushing [Cosmic] 1d Follow-Up plus Affliction (Mute) 5 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
Banefire (Elemental 93-96) keys on element subtypes; this keys on the elemental creature type. Different; names stay.

## FORKS NEEDING A RULING
1. Damage amount and proc rate not in the source (Magic-rung 1d6, 10%).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
