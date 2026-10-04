# WOW WEAPON ENCHANT COMPENDIUM
**Corpus Mass Translation — World of Warcraft weapon enchants, warcraft.wiki.gg, Classic through Warlords of Draenor. Built 2026-10-04.**

## HOW TO USE / TIER OVERVIEW
Each entry: the source tooltip as fetched, the 3.5e rules, the GURPS crosswalk, price, pool coverage, collisions and forks. Rate card and rules: Crusader (Affix Registry section 2) and `docs/translation/FUSED_ENGINE_RESOLUTION.md`. Conventions used throughout: 1 PPM = 10% per damaging hit; source seconds / 6 = rounds (GURPS keeps exact seconds); primary-stat procs +2 / +4; secondary ratings one +1 step; damage riders from the pool ladders; price = bonus-equivalent squared x 2,000 gp; healing ends Fatal Wound stacks. `Registered` means indexed here; a Notion Registry family entry is written when an affix is first rolled or placed. Plain flat-stat enchants and cosmetic or test IDs are excluded. Crusader is already ratified.

| Tier | Registered |
|---|---:|
| 2 Heroic Elite | 0 |
| 3 Heroic | 10 |
| 4 Competent | 31 |

## TIER 3 — HEROIC (LEVELS 9-12)

### BERSERKING
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


---

### BLADE WARD
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


---

### BLOOD DRAINING
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


---

### DANCING STEEL
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


---

### DEATHFROST
**WoW weapon enchant — Profession, Burning Crusade (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Deathfrost)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Burning Crusade
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Deathfrost
tooltip: "Permanently enchant a melee weapon to cause your damaging spells and melee weapon hits to occasionally inflict additional Frost damage and slow the target."
facts: spells 50% proc, 25-second internal cooldown; melee 10-12.5% proc, no internal cooldown; item level cap 600; slow does not work on targets level 73 or higher (patch 3.0.3); patch 2.4.0 added; patch 2.4.3 now procs off DoTs including Consecration; reagents 2 Primal Shadow, 2 Primal Water.
gaps: frost damage amount, slow amount and duration NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). For spells: one d100 per damaging spell the wielder casts, 01-10, then not again for 4 rounds (the source's 25 s internal cooldown). On fire: +1d6 cold damage and the target's land speed is x0.7 for 1 round (Icy Chill precedent; the source gives neither amount). Procs off damage-over-time ticks (patch 2.4.3). No slow on creatures of 17+ Hit Dice.

## GURPS 4e
On the same d100: Innate Attack Burning [Cold] 1d Follow-Up, plus Affliction (Reduced Move 30%) 5 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Freezing (Elemental 09-16) + Slowing (Condition 01-08).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Frost damage and slow amounts are not in the source; Freezing Magic-rung 1d6 and the Icy Chill slow are used. 2. The source's 'no slow on level 73+' is read as no slow on Tier 1 creatures (17+ Hit Dice). 3. Spell proc is cut from the source's 50% to 10% per cast to match the ratified melee convention.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### EXECUTIONER
**WoW weapon enchant — Profession, Burning Crusade (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Executioner)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Burning Crusade
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Executioner
tooltip: "Permanently enchant a melee weapon to occasionally grant you 60 critical strike rating."
facts: patch 4.0.1 (2010-10-12) changed from armor penetration to critical strike rating; patch 3.3.3 (2010-03-23) only one instance of the effect active at a time; item level cap 600. Secondary (search, original): ignores 840 armor for 15 seconds. Reagents 6 Void Crystal, 10 Large Prismatic Shard, 6 Greater Planar Essence, 30 Arcane Dust, 3 Elixir of Major Strength.
gaps: proc rate NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire, for 3 rounds the wielder's attacks ignore worn DR (the engine's ignores-armor flag; source original: ignores 840 armor for 15 s). Natural toughness is not ignored. Only one instance active at a time (source patch 3.3.3). The current crit-rating version (+60 crit rating) is the later redesign and is not used.

## GURPS 4e
On the same d100: for exactly 15 seconds the wielder's attacks skip worn DR (ignores_armor flag), natural DR still applies.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Armor Piercing (Offensive 19-24).

## NAME COLLISION
Pool affix 'Executioner' (Offensive 37-42, bonus damage vs bloodied targets): different mechanic; names stay, never merge. Also the Armor Piercing row is a flat ignore-DR value, not a timed proc.

## FORKS NEEDING A RULING
1. Armor-penetration amount is from a search snippet (840); proc rate not in the source (default 10%).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### MONGOOSE
**WoW weapon enchant — Profession, Burning Crusade (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Mongoose)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Burning Crusade
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Mongoose
tooltip: "Permanently enchant a melee weapon to occasionally increase Agility by 60 and haste by 15. Cannot be applied to items higher than level 600."
facts: current page values (scaled down from the original). Secondary (search, original TBC): +120 Agility and 30 haste rating, lasts 15 seconds, proc most likely normalized to 1 PPM. Reagents 40 Arcane Dust, 8 Greater Planar Essence, 10 Large Prismatic Shard, 6 Void Crystal.
gaps: PPM NOT PRESENT on the page itself.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire: +4 Dexterity (untyped) for 3 rounds, applying to attack, AC, Reflex and Dex skills (source original: +120 Agility, 15 s). The source's +30 haste rating is under one step and is dropped. Re-proc on the same weapon refreshes and does not stack; two Mongoose weapons stack (untyped, as Crusader).

## GURPS 4e
On the same d100: DX +2 for exactly 15 seconds (the 3.5e +4 at 2:1), refreshed by a same-weapon re-proc, stacking across two weapons.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. The current wiki tooltip is scaled down (60 Agility, 15 haste); the original TBC values (+120, 30 haste rating, 15 s, about 1 PPM) come from a search snippet and are what this entry uses. 2. Haste is dropped as below one step.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### RUNE OF RAZORICE
**WoW weapon enchant — Death knight runeforging (https://warcraft.wiki.gg/wiki/Rune_of_Razorice)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Death knight runeforging
quality: clean
url: https://warcraft.wiki.gg/wiki/Rune_of_Razorice
tooltip: "Engrave your weapon with a rune that causes (1.127% of Attack power) extra weapon damage as Frost damage and increases enemies' vulnerability to your Frost attacks by 3%, stacking up to 5 times."
facts: level 8, cast time 5 seconds; debuff Razorice: Frost damage taken from the Death Knight's abilities +3% per stack, 20 seconds, max 5 stacks; patch 3.3.3 changed from 10 stacks of 1% to 5 stacks of 2%.
gaps: proc NOT PRESENT (it is an every-hit effect).
```

## D&D 3.5e
Every damaging melee hit adds +1d6 cold damage (the Freezing Magic-rung value; source 1.127% of attack power as extra Frost damage) and one Razorice stack on the target, up to 5 stacks, each stack lasting 4 rounds (20 s). While the target holds 2 or more stacks the wielder's cold damage against it gains +1 per damage roll; at 4 or more, +2 (the source's 3% per stack vulnerability, at about 15% on the full 5, read as +1 per 2 stacks). Class lock: runeforging is a Death Knight craft.

## GURPS 4e
Innate Attack Burning [Cold] 1d Follow-Up on every damaging hit; stacks as the 3.5e side; +1 damage on cold attacks at 2 stacks, +2 at 4, for exactly 20 seconds from the last stack.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Freezing (Elemental 09-16) + Vulnerability (Condition 73-78).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Percent vulnerability to flat damage is an interpretation, flagged. 2. Death Knight runeforging has no 3.5e class; the rune is usable only by a wielder the GM rules a rune-smith.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### RUNE OF THE STONESKIN GARGOYLE
**WoW weapon enchant — Death knight runeforging (https://warcraft.wiki.gg/wiki/Rune_of_the_Stoneskin_Gargoyle)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Death knight runeforging
quality: clean
url: https://warcraft.wiki.gg/wiki/Rune_of_the_Stoneskin_Gargoyle
tooltip: "Engrave your weapon with a rune that increases Armor by 5% and all stats by 5%." (current)
facts: level 8; cast time 5 seconds; patch 7.0.3 armor 4% to 5%, stat bonus changed from 2% Stamina to 5% all stats; patch 4.0.1 Defense 25 replaced with 4% Armor; patch 3.0.8 added. Page calls it the only recommended runeforge for death knight tanks.
gaps: original Wrath tooltip not retrieved.
```

## D&D 3.5e
While wielded: +1 untyped bonus to every ability score and +1 natural armor bonus to AC (the source's +5% Armor and +5% all stats, which on typical scores is about +1 each). Class lock as Razorice; the page calls it the death knight tank's rune.

## GURPS 4e
Attributes +1 each (ST, DX, IQ, HT) and DR +1 (Gadget), uncosted.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Iron Skin (Defensive 19-24).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Percent stats to a flat +1 on every score is an interpretation; flagged. 2. Priced at +2 although the all-stat bonus is generous, to keep it Rare-rung.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### WINDFURY WEAPON
**WoW weapon enchant — Shaman imbue (https://warcraft.wiki.gg/wiki/Windfury_Weapon)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Shaman imbue
quality: clean
url: https://warcraft.wiki.gg/wiki/Windfury_Weapon
tooltip: "Imbue your main-hand weapon with the element of Wind for 1 hour. Each main-hand attack has a 25% chance to trigger two extra attacks, dealing (27.945% of Attack power) Physical damage each."
facts: current retail version (patch 12.0.0); 25% proc; no internal cooldown but cannot proc off itself; duration 1 hour; many damage retunes 9.0.2 to 12.0.0.
gaps: the Classic-era tooltip was not retrieved.
```

## D&D 3.5e
On each main-hand hit, d100 01-25 fires (the source's 25%): the wielder immediately makes two extra melee attacks at the highest base attack bonus with the same weapon. The extra attacks cannot fire Windfury (source: cannot proc off itself). Melee main-hand weapon only.

## GURPS 4e
On the same d100: two extra attacks at the full weapon skill, same weapon; the extra attacks cannot trigger the effect again.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Rapid Assault (Offensive 25-30).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. The Classic-era tooltip was not retrieved; the current retail wording (25%, two attacks) is used. 2. Priced below DMG Speed (+3): 25% of two attacks is half an extra attack per hit.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

## TIER 4 — COMPETENT (LEVELS 5-8)

### BATTLEMASTER
**WoW weapon enchant — Profession, Burning Crusade (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Battlemaster)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Burning Crusade
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Battlemaster
tooltip: "Permanently enchant a melee weapon to occasionally heal nearby party members for 76 to 126 when attacking in melee."
facts: "Proc rate is 1 PPM melee only" (testing data approximately 1.5-1.8% per swing); item level cap 600; reagents 8 Void Crystal, 8 Large Prismatic Shard, 2 Primal Water.
gaps: patch changes NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire every ally within 30 ft, wielder included, is healed 5 HP (the Crusader Magic-rung heal; source 76 to 126 healing, a little over a third of Crusader's 240). Magical healing: ends Fatal Wound stacks. Melee hits only.

## GURPS 4e
On the same d100: Regeneration burst of 5 HP to each ally within 10 yards, at once.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Heal is the Magic-rung 5; source ratio to Crusader is about 0.4, which rounds to the same step.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### BLACK MAGIC
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


---

### COLOSSUS
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


---

### DEMONSLAYING
**WoW weapon enchant — Profession, Classic (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Demonslaying)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Classic
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Demonslaying
tooltip: "Permanently enchant a melee weapon to have a chance of stunning and doing heavy damage to demons. Causes your weapon to become engulfed in flames, much like Fiery Weapon."
facts: enchanting skill 230-290; item level cap 136; reagents 1 Elixir of Demonslaying, 2 Rich Illusion Dust, 2 Large Brilliant Shard.
gaps: proc rate, stun length and damage amounts NOT PRESENT.
```

## D&D 3.5e
Against creatures with the demon subtype (tanar'ri, baatezu and other fiends the campaign names demons): +2d6 damage on every damaging hit (Banefire Magic-rung value, the 'heavy damage'), and on a 01-10 d100 the target is stunned 1 round, Fortitude DC 14 negates (Slowing/Dazing Magic-rung DC). Melee only.

## GURPS 4e
Innate Attack (Bane) 2d Follow-Up against demons, plus Affliction (Stunned) 1 second with a Quick Contest of the target's HT against effective skill 14.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Banefire (Elemental 93-96).

## NAME COLLISION
Dragondoom, Banefire family (names unrelated).

## FORKS NEEDING A RULING
1. Proc rate, stun length and damage amounts are not in the source; Banefire and Dazing Magic-rung values used. 2. 'Demon' means the demon subtype only; devils are a separate subtype (default: devils excluded).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### EARTHLIVING WEAPON
**WoW weapon enchant — Shaman imbue (https://warcraft.wiki.gg/wiki/Earthliving_Weapon)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Shaman imbue
quality: clean
url: https://warcraft.wiki.gg/wiki/Earthliving_Weapon
tooltip: "Imbue your weapon with the element of Earth for 1 hour. Your Riptide, Healing Wave, Healing Surge, and Chain Heal healing a 20% chance to trigger Earthliving on the target, healing for (138.915% of Spell power) over 6 sec."
facts: current retail version; 20% proc; 1 hour imbue, 6 second heal over time; patch 11.0.2 HoT duration 12 to 6 seconds and healing +75%.
gaps: Classic-era version not retrieved.
```

## D&D 3.5e
Proc: one d100 on each healing spell the wielder casts on a creature, 01-20 fires (the source's 20%). On fire the target also regains 3 HP at the start of each of its next 2 turns (the source's heal over 6 s at the Magic rung). Magical healing: ends Fatal Wound stacks.

## GURPS 4e
On the same d100 (per healing spell): Regeneration 3 HP at 3 seconds and again at 6 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Retail wording used; the Classic version was not retrieved.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### ELEMENTAL FORCE
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


---

### ELEMENTAL SLAYER
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


---

### HEARTSONG
**WoW weapon enchant — Profession, Cataclysm (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Heartsong)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Cataclysm
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Heartsong
tooltip: "Permanently enchant a weapon to sometimes increase Versatility by 30 for 15 sec when healing or dealing damage with spells."
facts: 20-second internal cooldown, approximately 25% proc; item level cap 136; reagents 9 Hypnotic Dust, 3 Greater Celestial Essence, 3 Heavenly Shard, 3 Volatile Life.
gaps: none.
```

## D&D 3.5e
Proc: one d100 on each damaging or healing spell the wielder casts, 01-10 fires, then not again for 3 rounds (the source's 20 s internal cooldown). On fire for 3 rounds (15 s): +1 untyped bonus to spell damage and to healing done, and the wielder takes 1 less damage from each hit (the source's Versatility +30 turns damage done, healing done and damage taken one step each).

## GURPS 4e
On the same d100: +1 damage on the wielder's spell attacks, +1 HP on healing, DR 1 against hits, exactly 15 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Versatility to three +1 steps is an interpretation; flagged. 2. Source proc about 25%; 10% used.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### HURRICANE
**WoW weapon enchant — Profession, Cataclysm (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Hurricane)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Cataclysm
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Hurricane
tooltip: "Permanently enchant a melee weapon to sometimes increase haste by 74 for 12 sec when healing or dealing spell or melee damage."
facts: internal cooldown 45 seconds; approximately 10-15% proc; item level cap 136; reagents 6 Heavenly Shard, 6 Volatile Air; patch 4.0.3a added.
gaps: none.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On a damaging hit or spell, then not again for 8 rounds (45 s internal cooldown): +1 untyped bonus on attack rolls and +2 initiative for 2 rounds (the source's +74 haste rating, 12 s; haste is read as one attack-step plus initiative). Healing spells also roll it.

## GURPS 4e
On the same d100: +1 skill with weapon attacks and +2 to initiative-type reaction rolls for exactly 12 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Haste rating to a +1 step is an interpretation; flagged. 2. Source proc about 10-15%; 10% used.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### ICY CHILL
**WoW weapon enchant — Profession, Classic (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Icy_Chill)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Classic
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Icy_Chill
tooltip: "Permanently enchant a melee weapon to often chill the target, reducing their movement and attack speed. Has a reduced effect for players above level 60."
facts: enchanting skill 285-300; item level cap 136; reagents 4 Large Brilliant Shard, 1 Essence of Water, 1 Essence of Air, 1 Icecap. Secondary (wiki Icy Chill spell page via search): frost debuff, movement slowed by 30%, time between attacks increased by 25%, for 5 seconds. Patch 2.3.2 changed functionality (no numbers given).
gaps: proc rate or PPM NOT PRESENT (page notes it is unclear whether PPM or chance on hit).
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire the target is chilled for 1 round (5 s): land speed x0.7 (round down to 5 ft) and -1 on attack rolls (the source's 25% longer time between attacks, at one step). No save (the source gives none), no SR. Melee weapons only. Does not stack with itself.

## GURPS 4e
On a damaging hit that fires: Affliction (Reduced Move 30% and -1 to skill with weapon attacks), exactly 5 seconds, no resistance roll. Same d100 as 3.5e.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Slowing (Condition 01-08).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Proc rate is not in the source (page says unclear PPM versus chance on hit); default 10% per damaging hit. 2. Slow is lighter than the Slowing row (no save, 1 round, speed x0.7), as the source's 30% implies.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### JADE SPIRIT
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


---

### LANDSLIDE
**WoW weapon enchant — Profession, Cataclysm (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Landslide)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Cataclysm
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Landslide
tooltip: "Permanently enchant a weapon to sometimes increase attack power by 100 for 12 sec when striking in melee."
facts: 1 PPM, no internal cooldown, can refresh itself; item level cap 600; patch 4.0.3a added; reagents 6 Hypnotic Dust, 5 Greater Celestial Essence, 5 Heavenly Shard, 5 Maelstrom Crystal.
gaps: none.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire for 2 rounds (12 s): +2 on melee damage rolls (untyped; source +100 attack power at 1 PPM). Re-proc refreshes; two weapons stack.

## GURPS 4e
On the same d100: Striking ST +1 for exactly 12 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Striking (Offensive 01-06).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
none.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### MARK OF BLACKROCK
**WoW weapon enchant — Profession, Warlords of Draenor (https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404))**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Warlords of Draenor
quality: degraded
url: https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404)
tooltip: (as summarized) +500 armor below 50% health for 12 sec.
facts: numbers only as summarized.
gaps: verbatim tooltip, proc rate NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire while the wielder is at or below half hit points: +2 natural armor bonus to AC for 2 rounds (source summary: +500 armor below 50% health for 12 s).

## GURPS 4e
On the same d100, only below half HP: DR +1 for exactly 12 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Degraded source (summary only).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: degraded.


---

### MARK OF BLEEDING HOLLOW
**WoW weapon enchant — Profession, Warlords of Draenor (https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404))**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Warlords of Draenor
quality: degraded
url: https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404)
tooltip: (as summarized) +500 mastery for 12 sec.
facts: numbers only as summarized.
gaps: verbatim tooltip, proc rate NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire for 2 rounds (12 s): +1 untyped bonus on melee damage rolls (source summary: +500 mastery; mastery is class-dependent and read at one step).

## GURPS 4e
On the same d100: +1 damage for exactly 12 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Degraded source (summary only). 2. Mastery read as +1 damage.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: degraded.


---

### MARK OF SHADOWMOON
**WoW weapon enchant — Profession, Warlords of Draenor (https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404))**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Warlords of Draenor
quality: degraded
url: https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404)
tooltip: (as summarized) +500 spirit for 15 sec.
facts: numbers only as summarized.
gaps: verbatim tooltip, proc rate NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire the wielder gains fast healing 1 for 3 rounds (source summary: +500 spirit for 15 s; Spirit is a regeneration stat). Fast healing is magical healing: ends Fatal Wound stacks.

## GURPS 4e
On the same d100: Regeneration (slow) 1 HP per second for exactly 15 seconds, capped at the 3.5e total.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Degraded source (summary only). 2. Spirit to fast healing 1 is an interpretation; flagged.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: degraded.


---

### MARK OF WARSONG
**WoW weapon enchant — Profession, Warlords of Draenor (https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404))**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Warlords of Draenor
quality: degraded
url: https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404)
tooltip: (as summarized) +1000 haste, -10% every 2 sec.
facts: numbers only as summarized.
gaps: verbatim tooltip, proc rate, duration NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire: +2 on attack rolls in the first round, +1 in the second, nothing after (source summary: +1000 haste decaying 10% every 2 s). Untyped.

## GURPS 4e
On the same d100: +2 then +1 skill with weapon attacks over two seconds-rounds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Degraded source (summary only). 2. Decay stepped to two rounds.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: degraded.


---

### MARK OF THE FROSTWOLF
**WoW weapon enchant — Profession, Warlords of Draenor (https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404))**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Warlords of Draenor
quality: degraded
url: https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404)
tooltip: (as summarized) +500 multistrike for 6 sec, 2 stacks.
facts: numbers only as summarized.
gaps: verbatim tooltip, proc rate NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire, +1 damage on melee damage rolls for 1 round (6 s); a second proc stacks once (2 stacks, +2) (source summary: +500 multistrike for 6 s, 2 stacks; multistrike is a chance to repeat a hit, read at one step).

## GURPS 4e
On the same d100: +1 damage per stack, 2 stacks, exactly 6 seconds each.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Degraded source (summary only). 2. Multistrike to flat damage is an interpretation; flagged.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: degraded.


---

### MARK OF THE SHATTERED HAND
**WoW weapon enchant — Profession, Warlords of Draenor (https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404))**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Warlords of Draenor
quality: degraded
url: https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404)
tooltip: (as summarized) 1500 bleed damage + 4500/6 sec.
facts: numbers only as summarized; the "4500/6 sec" reading is ambiguous.
gaps: verbatim tooltip, proc rate NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire the target bleeds 2 HP at the start of its turn for 3 rounds (6 HP total); bleeds from repeated procs do not stack, they refresh. Untyped, ignores DR, bloodless creatures immune (the Fatal Wound conventions). Source summary: 1500 bleed damage plus 4500 per 6 s (ambiguous).

## GURPS 4e
Follow-Up Toxic Attack (Follow-Up +0%) 2 HP per second for 3 seconds on the same d100.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Fatal Wound family (Affix Registry section 1).

## NAME COLLISION
Fatal Wound family (stacking bleed) and DMG Wounding; names stay, never merge.

## FORKS NEEDING A RULING
1. Degraded source (summary only); the '4500/6 sec' reading is ambiguous and the entry uses the smaller bleed. 2. Does not stack, unlike Fatal Wound.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: degraded.


---

### MARK OF THE THUNDERLORD
**WoW weapon enchant — Profession, Warlords of Draenor (https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404))**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Warlords of Draenor
quality: degraded
url: https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404)
tooltip: (as summarized from the truncated slot page) +500 crit for 6 sec, crits extending duration.
facts: numbers only as summarized; no tooltip wording.
gaps: verbatim tooltip, proc rate, caps NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire for 1 round (6 s): +2 on rolls to confirm critical hits; each confirmed critical hit during it extends the effect by 1 round, up to 3 rounds in all (source summary: +500 crit for 6 s, crits extend the duration).

## GURPS 4e
On the same d100: +1 to critical-hit confirmation, extended 1 second-round per crit, exactly 6 seconds base.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Degraded source: only a summary of the numbers was retrieved; no verbatim tooltip, no proc rate.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: degraded.


---

### MENDING
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


---

### POWER TORRENT
**WoW weapon enchant — Profession, Cataclysm (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Power_Torrent)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Cataclysm
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Power_Torrent
tooltip: "Permanently enchant a weapon to sometimes increase Intellect by 83 for 12 sec when dealing damage or healing with spells."
facts: internal cooldown 45 seconds; approximately 33% proc; item level cap 136; patch 4.0.3a added.
gaps: none.
```

## D&D 3.5e
Proc: one d100 on each damaging or healing spell the wielder casts, 01-10 fires, then not again for 8 rounds (the source's 45 s internal cooldown). On fire: +2 Intelligence (untyped) for 2 rounds (source +83 Intellect, 12 s).

## GURPS 4e
On the same d100: IQ +1 for exactly 12 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Source proc is about 33%; cut to 10% per cast.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### RIVER'S SONG
**WoW weapon enchant — Profession, Mists of Pandaria (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_River%27s_Song)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Mists of Pandaria
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_River%27s_Song
tooltip: "sometimes increase your dodge by 65 for 7 sec when dealing melee damage"
facts: item level cap 136; reagents 1 River's Heart, 50 Mysterious Essence; patch 5.0.4 added.
gaps: proc rate NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire for 2 rounds (7 s): +1 dodge bonus to AC (the source's +65 dodge rating).

## GURPS 4e
On the same d100: Enhanced Dodge +1 for exactly 7 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Proc rate not in the source (10%).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### RUNE OF CINDERGLACIER
**WoW weapon enchant — Death knight runeforging (https://warcraft.wiki.gg/wiki/Rune_of_Cinderglacier)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Death knight runeforging
quality: clean
url: https://warcraft.wiki.gg/wiki/Rune_of_Cinderglacier
tooltip: "Affixes your rune weapon with a rune that has a chance to increase the damage by 20% of your next 2 spells that deal Frost or Shadow damage. Lasts 30 sec."
facts: spell ID 53341; duration 30 seconds; patch 3.0.2 added; patch 6.0.2 removed.
gaps: proc rate NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire, the wielder's next two cold or negative-energy damaging effects within 5 rounds (30 s) each deal +2 damage (the source's +20% on typical Magic-rung damage). Class lock as Razorice.

## GURPS 4e
On the same d100: the next two cold or Toxic [Cosmic] attacks within exactly 30 seconds gain +2 damage each.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Proc rate not in the source (default 10%). 2. 20% to flat +2 is an interpretation.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### RUNE OF SPELLBREAKING
**WoW weapon enchant — Death knight runeforging (https://warcraft.wiki.gg/wiki/Rune_of_Spellbreaking)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Death knight runeforging
quality: clean
url: https://warcraft.wiki.gg/wiki/Rune_of_Spellbreaking
tooltip: "Affixes your one-handed rune weapon with a rune that deflects 2% of all spell damage and reduces the duration of Silence effects by 50% (not cumulative with additional Silence duration reduction)."
facts: level 57; patch 3.2.0 now reduces damage from Holy spells; removed 7.0.3.
gaps: none.
```

## D&D 3.5e
While wielded: each damaging spell that hits the wielder deals 1 less damage (minimum 0; the source deflects 2% of spell damage, which at the Magic rung is 1 point), and Silence effects on the wielder last half as long (rounded down, minimum 1 round). One-handed weapons only.

## GURPS 4e
Damage Resistance 1 against spell damage only (Gadget; Only vs spells -20%) and Silence duration halved.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Spell Ward (Defensive 37-42).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Percentage deflection to a flat point; flagged.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### RUNE OF SPELLSHATTERING
**WoW weapon enchant — Death knight runeforging (https://warcraft.wiki.gg/wiki/Rune_of_Spellshattering)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Death knight runeforging
quality: clean
url: https://warcraft.wiki.gg/wiki/Rune_of_Spellshattering
tooltip: "Affixes your two-handed rune weapon with a rune that deflects 4% of all spell damage and reduces the duration of Silence effects by 50%."
facts: level 57; cast time 5 seconds; removed 7.0.3.
gaps: none.
```

## D&D 3.5e
As Spellbreaking on a two-handed weapon at double the step: each damaging spell that hits the wielder deals 2 less damage (source 4%), Silence on the wielder lasts half as long.

## GURPS 4e
Damage Resistance 2 against spell damage only and Silence duration halved.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Spell Ward (Defensive 37-42).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Same flat-point reading as Spellbreaking.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### RUNE OF SWORDBREAKING
**WoW weapon enchant — Death knight runeforging (https://warcraft.wiki.gg/wiki/Rune_of_Swordbreaking)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Death knight runeforging
quality: clean
url: https://warcraft.wiki.gg/wiki/Rune_of_Swordbreaking
tooltip: "Affixes your one-handed rune weapon with a rune that increases Parry chance by 2% and reduces the duration of Disarm effects by 50%."
facts: level 63; cast time 5 seconds; patch 5.1.0 disarm reduction 60% to 50%; patch 4.0.6 50% to 60%; patch 3.0.2 added; removed 6.0.2.
gaps: none.
```

## D&D 3.5e
While wielded: +1 dodge bonus to AC (the source's +2% parry chance, at one step) and a +4 bonus on checks to avoid being disarmed, and a weapon the wielder is disarmed of can be recovered as a move action instead of a standard action (the source halves Disarm duration). One-handed weapons only.

## GURPS 4e
Enhanced Parry +1 and +4 to resist Disarm; recovery of a dropped weapon takes half the time.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Bladesinger (Skill/Class 31-36).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. The WoW disarm debuff (cannot use weapon for a time) is read as the 3.5e disarm maneuver; flagged.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### RUNE OF SWORDSHATTERING
**WoW weapon enchant — Death knight runeforging (https://warcraft.wiki.gg/wiki/Rune_of_Swordshattering)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Death knight runeforging
quality: clean
url: https://warcraft.wiki.gg/wiki/Rune_of_Swordshattering
tooltip: "Affixes your two-handed rune weapon with a rune that increases Parry chance by 4% and reduces the duration of Disarm effects by 50%."
facts: level 63; same patch history as Swordbreaking.
gaps: none.
```

## D&D 3.5e
As Swordbreaking on a two-handed weapon, at double the parry step: +2 dodge bonus to AC (source +4% parry), +4 on checks to avoid being disarmed, disarmed weapon recovered as a move action.

## GURPS 4e
Enhanced Parry +2 and +4 to resist Disarm; recovery in half the time.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Bladesinger (Skill/Class 31-36).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Same disarm reading as Swordbreaking.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### SPELLSURGE
**WoW weapon enchant — Profession, Burning Crusade (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Spellsurge)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Burning Crusade
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Spellsurge
tooltip: "Permanently enchant a melee weapon to make your spells sometimes restore 100 mana to nearby party members. Cannot be applied to items higher than level 600."
facts: 3% chance on spell cast to restore 100 mana to all party members over 10 seconds; item level cap 600; reagents 12 Large Prismatic Shard, 10 Greater Planar Essence, 20 Arcane Dust.
gaps: patch changes NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each spell the wielder casts, 01-03 fires (the source's 3%). On fire every ally within 30 ft, wielder included, recovers 5 mana (the Souldrinker Magic-rung value; source: 100 mana over 10 s to party members). Hybrid campaign note: only characters who carry a mana pool benefit. Melee weapon, spells cast by the wielder.

## GURPS 4e
On the same d100 (per spell cast): Energy Reserve recovery of 5 points to each ally within 10 yards.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Mana scale: 100 mana at the source's level is rescaled to the pool's Souldrinker rung; default 5 mana.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### UNHOLY WEAPON
**WoW weapon enchant — Profession, Classic (https://warcraft.wiki.gg/wiki/Unholy_Weapon)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Classic
quality: clean
url: https://warcraft.wiki.gg/wiki/Unholy_Weapon
tooltip: "Permanently enchant a melee weapon to often inflict a curse on the target, inflicting Shadow damage and reducing their melee damage."
facts: enchanting skill 295-300; item level cap 136; reagents 4 Essence of Undeath, 4 Large Brilliant Shard; patch 3.3.0 (2009-12-08): now inflicts Shadow damage in addition to its original effect. Secondary (search): the curse reduces the target's damage by 15 and lasts 12 seconds.
gaps: proc rate NOT PRESENT; shadow damage amount NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire the target takes 1d4 negative-energy damage (the shadow damage added in patch 3.3.0; the amount is not in the source, so this is the Shadowtouch Magic-rung value) and a curse: -2 on its melee damage rolls for 2 rounds (source: -15 damage, 12 s). No save, no SR; undead take the negative damage as Shadowtouch does (half).

## GURPS 4e
Innate Attack Toxic [Cosmic] 1d Follow-Up on the hit, plus Affliction (Weakened: -2 damage on the target's melee attacks), exactly 12 seconds. Same d100.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
DMG/Registry affix 'Unholy' (alignment weapon, +2d6 vs good): different mechanic; names stay, never merge. Pool 'Weakening' (-Str) is also different.

## FORKS NEEDING A RULING
1. Shadow damage amount and proc rate are not in the source; values are Magic-rung design values.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### WINDSONG
**WoW weapon enchant — Profession, Mists of Pandaria (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Windsong)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Mists of Pandaria
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Windsong
tooltip: "Permanently enchants a melee weapon to sometimes increase your critical strike, haste, or mastery by 59 for 12 sec when dealing damage or healing with spells and melee attacks."
facts: item level cap 136; reagents 12 Spirit Dust, 1 Ethereal Shard; patch 5.0.4 added; hotfixes 2012-10-12 and 2012-10-16 (periodic effects can activate it; no longer removes Stealth).
gaps: proc rate NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire roll d3: 1 = +1 on confirmation rolls for critical hits, 2 = +1 on attack rolls, 3 = +1 damage; all untyped, 2 rounds (the source randomly picks crit, haste or mastery at +59 for 12 s). Heals and spells also roll it.

## GURPS 4e
On the same d100 plus a d3: +1 to confirm crits, +1 skill, or +1 damage, exactly 12 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Ratings read as +1 steps; flagged. 2. Proc rate not in the source (10%).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

### WINDWALK
**WoW weapon enchant — Profession, Cataclysm (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Windwalk)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Cataclysm
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Windwalk
tooltip: "Permanently enchant a weapon to sometimes increase dodge by 99 and movement speed by 10% for 10 sec when striking in melee, stacking with passive movement speed effects."
facts: no internal cooldown, can refresh itself; item level cap 136; patch 4.0.3a added.
gaps: proc rate NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire for 2 rounds: +1 dodge bonus to AC and +5 ft land speed (source: +99 dodge rating and +10% movement speed, 10 s, no internal cooldown, refreshes itself). Re-proc refreshes.

## GURPS 4e
On the same d100: Enhanced Dodge +1 and Enhanced Move (Ground) 0.5 for exactly 10 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Swiftfoot (Utility 01-06).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Proc rate not in the source (default 10%).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.


---

## COVERED BY AN EXISTING REGISTRY ROW (no second document)

| Enchant | Existing row | Note |
|---|---|---|
| Avalanche | Shocking (Elemental 17-24), element chosen at creation | Avalanche deals 74 Nature damage often (proc rate not given). The Elemental pool rows are element-parametric riders; Nature has no 3.5e energy type. Default element: electricity (Shocking). Fork: acid is the other reasonable reading. |
| Fiery Weapon | Flaming (Elemental 01-08) | Flaming deals +1d4/+1d6/+1d8/+2d6/+3d6 fire on every hit. Fiery Weapon's 34 fire at 6 PPM is the same shape (a near-every-hit fire rider); no new family. Gap: none. |
| Flametongue Weapon | Flaming (Elemental 01-08) | The Enhancement-spec Flametongue adds fire damage to each attack (3.96% of Attack Power): Flaming covers it. The Elemental-spec +5% Fire spell damage is a spell rider, covered by Elemental Attunement (Elemental 87-92). |
| Frostbrand Weapon | Freezing (Elemental 09-16) + Slowing (Condition 01-08) | Frostbrand (Classic): chance of 48 frost damage and a 25% movement slow for 8 s. Freezing gives the frost rider; Slowing gives the slow. Covered together. |
| Lifestealing | Vampiric (MIC, registered in the weapon-affix corpus) / Leech (Resource 19-24) | Lifestealing steals about 30 life per proc as shadow damage; Vampiric (+1d6 and heal equal) and Leech (heal per hit) cover the heal-on-hit shape. Difference: Lifestealing is a 6 PPM proc, the existing rows are every-hit. Fork recorded in the compendium: none needed. |
| Rockbiter Weapon | Striking (Offensive 01-06) | Classic Rockbiter is +50 melee attack power and threat; a flat enhancement-style bonus, covered by Striking. The threat clause has no 3.5e mechanic. |
| Rune of the Fallen Crusader | Crusader family (Affix Registry section 2) | The Registry's Crusader source record already names this rune as the percent-scaled sibling (heal 4% max HP, +15% Strength, 15 s). The family covers it; its flat values replace the percentages. |

## OPEN VERIFICATION ITEMS

- Mark of Blackrock: degraded source (summary only; no verbatim tooltip or proc rate)
- Mark of Bleeding Hollow: degraded source (summary only; no verbatim tooltip or proc rate)
- Mark of Shadowmoon: degraded source (summary only; no verbatim tooltip or proc rate)
- Mark of Warsong: degraded source (summary only; no verbatim tooltip or proc rate)
- Mark of the Frostwolf: degraded source (summary only; no verbatim tooltip or proc rate)
- Mark of the Shattered Hand: degraded source (summary only; no verbatim tooltip or proc rate)
- Mark of the Thunderlord: degraded source (summary only; no verbatim tooltip or proc rate)
- Berserking: forks listed in its entry
- Blade Ward: forks listed in its entry
- Blood Draining: forks listed in its entry
- Dancing Steel: forks listed in its entry
- Deathfrost: forks listed in its entry
- Executioner: forks listed in its entry
- Mongoose: forks listed in its entry
- Rune of Razorice: forks listed in its entry
- Rune of the Stoneskin Gargoyle: forks listed in its entry
- Windfury Weapon: forks listed in its entry
- Battlemaster: forks listed in its entry
- Black Magic: forks listed in its entry
- Colossus: forks listed in its entry
- Demonslaying: forks listed in its entry
- Earthliving Weapon: forks listed in its entry
- Elemental Force: forks listed in its entry
- Elemental Slayer: forks listed in its entry
- Heartsong: forks listed in its entry
- Hurricane: forks listed in its entry
- Icy Chill: forks listed in its entry
- Jade Spirit: forks listed in its entry
- Mark of Blackrock: forks listed in its entry
- Mark of Bleeding Hollow: forks listed in its entry
- Mark of Shadowmoon: forks listed in its entry
- Mark of Warsong: forks listed in its entry
- Mark of the Frostwolf: forks listed in its entry
- Mark of the Shattered Hand: forks listed in its entry
- Mark of the Thunderlord: forks listed in its entry
- Mending: forks listed in its entry
- Power Torrent: forks listed in its entry
- River's Song: forks listed in its entry
- Rune of Cinderglacier: forks listed in its entry
- Rune of Spellbreaking: forks listed in its entry
- Rune of Spellshattering: forks listed in its entry
- Rune of Swordbreaking: forks listed in its entry
- Rune of Swordshattering: forks listed in its entry
- Spellsurge: forks listed in its entry
- Unholy Weapon: forks listed in its entry
- Windsong: forks listed in its entry
- Windwalk: forks listed in its entry
