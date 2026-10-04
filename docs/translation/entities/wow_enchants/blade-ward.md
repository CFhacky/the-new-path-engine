# BLADE WARD
**WoW weapon enchant — Profession, Wrath of the Lich King (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Blade_Ward)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Wrath of the Lich King
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Blade_Ward
tooltip: "Permanently enchant a weapon to sometimes grant Blade Warding when striking an enemy. Blade Warding increases your parry rating by 100 and inflicts 286 to 315 damage on your next parry. Lasts 10 sec."
facts: approximately 5% proc chance per hit; item level cap 600; reagents 4 Abyss Crystal, 8 Greater Cosmic Essence, 1 Titansteel Bar.
gaps: patch changes NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-05 fires (the source's about 5%). On fire for 2 rounds (10 s): +2 dodge bonus to AC and the first melee attack that misses the wielder deals 2d6 untyped damage to its attacker (source: +100 parry rating and 286 to 315 damage on the next parry). The damage ignores worn DR and the effect then ends.

## GURPS 4e
On the same d100: Enhanced Parry +1 for exactly 10 seconds; the first successful parry deals 2d to the attacker.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Thorns (Defensive 43-48) + Bladesinger (Skill/Class 31-36).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Parry becomes dodge AC because the 3.5e chassis has no parry stat. 2. Damage uses the Thorns Rare-rung 2d6.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
