# MENDING
**WoW weapon enchant — Profession, Cataclysm (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Mending)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Cataclysm
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Mending
tooltip: "Permanently enchant a weapon to sometimes heal you when damaging an enemy with spells and melee attacks."
facts: requires a level 300 or higher item (as returned); patch 4.0.3a added.
gaps: heal amount and proc rate NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire the wielder heals 5 HP (the Crusader Magic-rung heal; the source gives no amount). Works on spell damage as well as melee (one d100 per damaging spell cast). Magical healing: ends Fatal Wound stacks.

## GURPS 4e
On the same d100: Regeneration burst of 5 HP at once.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Heal amount and proc rate are not in the source; both default to the Crusader Magic rung. 2. Overlaps the heal half of the Crusader Magic rung; kept separate because it carries no Strength bonus.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
