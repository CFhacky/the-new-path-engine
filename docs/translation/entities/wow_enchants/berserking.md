# BERSERKING
**WoW weapon enchant — Profession, Wrath of the Lich King (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Berserking)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Wrath of the Lich King
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Berserking
tooltip: "Permanently enchant a melee weapon to sometimes increase your attack power by 400, but at the cost of reduced armor."
facts: reagents 12 Infinite Dust, 4 Greater Cosmic Essence, 4 Dream Shard, 10 Abyss Crystal, Runed Copper Rod (tool).
gaps: proc rate, duration, armor reduction amount, item level cap NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire for 3 rounds: +3 damage on melee damage rolls and -2 AC (untyped; source +400 attack power and 'reduced armor', amounts for armor loss and duration not given). Re-proc refreshes; two weapons stack.

## GURPS 4e
On the same d100: Striking ST +1 and DR -1 (Gadget) for exactly 15 seconds, refreshed by re-proc.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
Pool affix 'Berserker' (Offensive 61-66, +damage with -AC while attacking) and MIC 'Berserker' (extra 1d8 while raging): different mechanics; names stay, never merge.

## FORKS NEEDING A RULING
1. Duration, proc rate and armor reduction are not in the source (default 10%, 3 rounds, -2 AC).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
