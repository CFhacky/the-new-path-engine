# BLACK MAGIC
**WoW weapon enchant — Profession, Wrath of the Lich King (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Black_Magic)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Wrath of the Lich King
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Black_Magic
tooltip: "Permanently enchant a melee weapon to cause your harmful spells to sometimes increase haste by 62."
facts: approximately 35% proc, 35-second internal cooldown; item level cap 600; patch 3.3.0 (2009-12-08) changed from inflicting damage over time on the target to increasing the caster's haste rating; patch 3.0.8 reagents changed to 6 Greater Cosmic Essence, 6 Dream Shard, 6 Abyss Crystal.
gaps: duration NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging spell the wielder casts, 01-10 fires, then not again for 6 rounds (the source's 35 s internal cooldown). On fire: +2 caster level on the wielder's damaging spells for 2 rounds (the source's +62 haste rating has no direct 3.5e step; caster level is the closest damage proxy, the Catalyst Magic-rung +2). Melee weapon.

## GURPS 4e
On the same d100: Talent (Magical) +2 on the wielder's attack spells for exactly 12 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Catalyst (Resource 73-78).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Haste maps to +2 caster level; this is an interpretation, flagged. 2. Duration not in the source; 12 s assumed from the Cataclysm-era sibling enchants. 3. Source proc is about 35%; cut to 10% per cast.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
