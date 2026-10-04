# BLOOD DRAINING
**WoW weapon enchant — Profession, Wrath of the Lich King (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Blood_Draining)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Wrath of the Lich King
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Blood_Draining
tooltip: "Permanently enchant your weapon to sometimes grant Blood Reserve when striking an enemy or inflicting damage with bleed attacks. When you fall below 35% health, Blood Reserve restores 180 to 219 health. Lasts 20 sec and stacks up to 5 times. Cannot be applied to items higher than level 600."
facts: patch 3.1.0 (2009-04-14) added; hotfix 2009-05-22 fixed Blood Reserve restoring proper health amounts; reagents 40 Infinite Dust, 1 Scarlet Ruby, 4 Abyss Crystal.
gaps: proc rate NOT PRESENT; whether the heal is per stack or total is not stated.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire (also on the wielder's bleed ticks dealing damage) the wielder gains one Blood Reserve; up to 5 at once, each lasting 4 rounds (20 s). Whenever the wielder's hit points fall below 35% of maximum, every Blood Reserve is spent at once and each heals 8 HP (the Lifedrinker Magic-to-Rare value; source 180 to 219). Magical healing: ends Fatal Wound stacks.

## GURPS 4e
On the same d100: Regeneration (limited) stored burst, up to 5 stacks, 20 seconds each, each 8 HP when HP drops below 35%.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. The source does not say whether the heal is per stack or total; default per stack, spent together. 2. Proc rate not in the source (default 10%).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
