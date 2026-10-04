# COLOSSUS
**WoW weapon enchant — Profession, Mists of Pandaria (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Colossus)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Mists of Pandaria
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Colossus
tooltip: "Permanently enchants a melee weapon to make your damaging melee strikes sometimes activate a Mogu protection spell, absorbing up to 371 damage."
facts: item level cap 136.
gaps: proc rate, duration, patch history NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On a damaging melee hit that fires, the wielder gains 8 temporary hit points (the Life Shield Rare-rung value; source: a Mogu protection absorbing up to 371 damage). The temporary hit points last until used or 1 minute; they do not stack with other temporary hit points.

## GURPS 4e
On the same d100: a damage absorption pool of 8 HP (Damage Resistance burst) until used or 60 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Life Shield (Defensive 31-36).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Duration and proc rate are not in the source (10%, 1 minute). 2. Absorb shield read as temporary hit points.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
