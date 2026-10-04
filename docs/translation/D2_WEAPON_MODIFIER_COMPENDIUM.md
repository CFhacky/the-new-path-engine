# DIABLO II WEAPON MODIFIER COMPENDIUM
**Corpus Mass Translation — Diablo II weapon modifiers (Maxroll attack-modifier reference, PureDiablo melee affix lists). Built 2026-10-04.**

## HOW TO USE / TIER OVERVIEW
Each entry: the source tooltip as fetched, the 3.5e rules, the GURPS crosswalk, price, pool coverage, collisions and forks. Rate card and rules: Crusader (Affix Registry section 2) and `docs/translation/FUSED_ENGINE_RESOLUTION.md`. Conventions used throughout: chance-based mods roll one d100 per damaging hit, 01-10 fires; D2 level-difference chance formulas are replaced by a fixed Fortitude or Will save, DC 13-14; 'normal and minion monsters only' is read as creatures under 17 Hit Dice; GURPS keeps exact seconds; price = bonus-equivalent squared x 2,000 gp; healing ends Fatal Wound stacks. `Registered` means indexed here; a Notion Registry family entry is written when an affix is first rolled or placed. Excluded: plain stat suffixes, socket affixes, requirement reductions, throwing-quantity and per-level affixes. The runeword registry already exists in Notion. Magic-affix ladders already covered by a pool row (fire, cold, lightning, poison, damage, attack rating) are listed at the end, not restated.

| Tier | Registered |
|---|---:|
| 2 Heroic Elite | 1 |
| 3 Heroic | 4 |
| 4 Competent | 8 |

## TIER 2 — HEROIC ELITE (LEVELS 13-16)

### IGNORE TARGET'S DEFENSE
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `wow_pipeline.py`; price +3 = 18,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "Calculates attacks made on normal, minion monsters, or Character Summons as having 0 Defense"
facts: only for attacks made with that weapon; does not work on player characters, mercenaries, elites or act bosses.
gaps: none.
```

## D&D 3.5e
Melee and ranged. The wielder's attacks with this weapon against creatures of under 17 Hit Dice (the source's normal and minion monsters and character summons; not player characters, mercenaries, elites or bosses) resolve as touch attacks (the target's armor, shield and natural armor bonuses to AC are ignored; Dex, dodge and deflection still apply). Always on, no d100.

## GURPS 4e
The defender's Parry, Block and Dodge are rolled at -3 (a defender with 0 Defense in the source rolls as undefended); against Tier 1 targets and player characters the weapon has no effect.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+3 = 18,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. 'Defense 0' is read as a touch attack on the 3.5e side and as a -3 to the defender's 3d6 contest on the GURPS side (the engine does not name this mechanism). 2. Priced at +3: an always-on touch attack is stronger than MIC Impaling's 3/day at +1.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.


---

## TIER 3 — HEROIC (LEVELS 9-12)

### CHANCE TO CAST ON ATTACK
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "Gives a % Chance to Cast the listed Skill when making a melee attack hit check against a target"
facts: the attack need not hit, only be attempted; procced also by mercenaries, summons and monsters with gear; skill synergies apply; ranged weapons do not proc unless used by a shape-shifted druid; charged bolt and frozen orb originate from the attacker, all others from the target.
gaps: none.
```

## D&D 3.5e
Proc: one d100 on each attack roll the wielder makes with this weapon, hit or miss (the source triggers on the attack attempt), 01-10 fires. On fire the weapon casts a spell chosen at creation (level 1 to 3, caster level 5, normal save DC for the spell level), centered on the target or the wielder as the spell requires. Melee weapons only. Procs never proc other procs.

## GURPS 4e
On the same d100 per attack roll: the chosen spell as an Innate Attack, resisted as the spell requires.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
DMG Spell Storing (a caster loads the spell); this weapon casts a fixed spell by itself. Different; names stay.

## FORKS NEEDING A RULING
1. The cast skill is chosen at creation and the source's skill level scales; a fixed spell level 1 to 3 at caster level 5 is used. 2. The source's chance varies by item (5 to 25% in the search example); the ratified 10% is used.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.


---

### CHANCE TO CAST ON STRIKING
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "Gives a % Chance to Cast the listed Skill when making a melee attack hit check that succeeds, and hit is not Blocked or Dodged"
facts: the attack must hit but need not deal damage; venom and enchant are cast on the attacker; poison nova and static field centre on the attacker; directional skills (firestorm, twister, tornado, bone spirit, charged bolt, frozen orb) cast toward the target from the attacker; all others originate at the target. Search example: "5% Chance To Cast Level 18 Volcano On Striking".
gaps: none.
```

## D&D 3.5e
Proc: one d100 on each successful hit with this weapon (the hit must connect and not be blocked or dodged; damage is not required), 01-10 fires. On fire the weapon casts a spell chosen at creation (level 1 to 3, caster level 5, normal save DC), centered on the target (self-centered spells such as a nova or an aura center on the wielder). Melee weapons only.

## GURPS 4e
On the same d100 per successful strike: the chosen spell as an Innate Attack.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
Chance to Cast on Attack (same corpus), DMG Spell Storing: different triggers and sources; names stay.

## FORKS NEEDING A RULING
1. Same fixed-spell reading as Chance to Cast on Attack. 2. Differs from it only in needing a connecting hit.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.


---

### CRUSHING BLOW
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "deals additional damage prior to the attack's damage, equal to a fraction of the remaining Life total of the target"
facts: formula 1/4 of current Life / (0.5 + 0.5N), N = players in game up to 8; critical hits do not increase it; affected by the target's Damage Resist and Damage Reduced by %; not affected by -% Damage Resistance; integer Damage Reduced does not reduce it; Sanctuary does not protect Immune-to-Physical undead.
gaps: per-item chance values not on this page (the search snippet shows Bloodtree Stump at 50%).
```

## D&D 3.5e
Proc: one d100 on each damaging melee hit, 01-10 fires. On fire the target takes extra damage equal to one quarter of its current hit points, maximum 25, before normal damage. Not multiplied on a critical hit; ignores DR/X; reduced by percentage-type resistances; creatures immune to physical damage take none. Creatures of 17+ Hit Dice take one eighth of current hit points instead (maximum 25).

## GURPS 4e
Crushing Attack (Follow-Up) on the same d100: injury equal to 1/4 of the target's current HP, maximum 25 HP, applied after DR; against Tier 1 targets 1/8.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
Pool 'Lethal Focus' (crit bonus) and DMG Mighty Cleaving: different mechanics.

## FORKS NEEDING A RULING
1. The source gives no cap and halves the fraction for some enemies only by difficulty; the 25 cap and the Tier 1 eighth are design values. 2. Chance per item varies in the source (the search shows Bloodtree Stump at 50%); the ratified 10% proc is used.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.


---

### FREEZE TARGET
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "Freezes normal or minions monsters, and applies Chill to all other targets as long as target is not Immune to Cold or have 0 Chill Effectiveness"
facts: only freezes normal and minion monsters; freeze or chill length random 1 to 9 seconds (25-225 frames), effectiveness 1/2 in Nightmare and 1/4 in Hell; chance, melee: 30 + 5(4 x {Freeze Target sum} + {attacker level - defender level}); ranged: that / 3; applied by any melee or ranged attack except blade sentinel, blade shield and extra multishot arrows.
gaps: none.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires. On fire the target must succeed on a Fortitude save (DC 14) or be held (frozen) for 1d2 rounds (the source's 1 to 9 seconds); on a success it is chilled instead (land speed x0.7, -1 on attacks, 1 round). Creatures of 17+ Hit Dice and creatures immune to cold are only chilled. Does not stack.

## GURPS 4e
On the same d100: Quick Contest of the target's HT against effective skill 14; on failure Affliction (Immobilized) for 1d6 seconds (source 1 to 9); on success or against Tier 1, Reduced Move 30% for 5 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Freezing (Elemental 09-16) + Slowing (Condition 01-08).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. The source's chance formula depends on the Freeze Target total and the level gap; it is replaced by the fixed DC 14 save. 2. 'Normal and minion monsters only' is read as creatures under 17 Hit Dice.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.


---

## TIER 4 — COMPETENT (LEVELS 5-8)

### FIRES EXPLOSIVE ARROWS OR BOLTS
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "replaces any standard Attack with explodingarrow with Skill Level determined by the weapon source"
facts: does not apply if a skill is used with the weapon; weapon source levels: Raven Claw 3, Hellcast 5, Demon Machine 6, Kuko Shakaku 7, Blood Raven's Charge 13, Brand 15.
gaps: Exploding Arrow damage numbers NOT PRESENT.
```

## D&D 3.5e
Ranged weapons only. Each damaging hit also bursts in a 5-ft radius around the target for 1d6 fire damage, Reflex DC 13 half (the Magic-rung value; the source gives no Exploding Arrow damage). No d100; every hit. Does not apply when the wielder uses a skill-based shot.

## GURPS 4e
Innate Attack (Burning, Explosion 1) 1d on every damaging hit, centered on the target.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Elemental Burst (Elemental 75-80).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Exploding Arrow damage and the item source levels (3 to 15) are not in the source; the Elemental Burst Magic-rung scale is used. 2. Elemental Burst triggers on a crit; this entry triggers on every hit (that is the delta).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.


---

### FIRES MAGIC ARROWS
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "Replaces any standard Attack with magicarrow with Skill Level determined by the weapon source"
facts: does not apply if a skill is used with the weapon; source levels: M'avina's Caster 1, Witherstring 3, Wizendraw 5, Widowmaker 11, Witchwild String 20.
gaps: Magic Arrow damage numbers NOT PRESENT.
```

## D&D 3.5e
Ranged weapons only. Every damaging hit counts as magic and deals +1d4 force damage (the Magic-rung value; the source gives no Magic Arrow damage). Force damage ignores DR/X and incorporeal miss chances. No d100.

## GURPS 4e
Innate Attack (Crushing [Cosmic]) 1d Follow-Up on every damaging hit, ignoring worn DR.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Magic Arrow damage and the item source levels (1 to 20) are not in the source; value is design. 2. Force is the closest 3.5e reading of D2's 'magic' damage.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.


---

### HIT BLINDS TARGET
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "cast a level 1-20 dimvision on the target which Blinds it"
facts: blinds only normal and minion monsters; reduces monster awareness to melee range only (no skills or special abilities); chance, melee: 30 + 5(4 x {Hit Blinds Target sum} + {attacker level - defender level}), ranged: that / 3; dimvision level min((% chance - random(99)) / 5 + 1, 20); duration halved in Nightmare, quartered in Hell; if applied together with Flee, flee takes precedence.
gaps: base duration NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires. On fire the target is blinded for 1 round unless it succeeds on a Fortitude save (DC 14); a blinded creature can fight only at melee reach and cannot use special attacks or spell-like abilities at range. Creatures of 17+ Hit Dice are immune. Flee takes precedence if both effects fire.

## GURPS 4e
On the same d100: Quick Contest HT against effective skill 14; on failure Affliction (Blindness) for 6 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Blinding (Condition 43-48).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Duration is not in the source (1 round assumed, the Blinding row's value). 2. The source blinds on a plain hit; the pool row blinds on a crit.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.


---

### HIT CAUSES MONSTER TO FLEE
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "causes the target to flee in the direction opposite of the attacker due to applying a flee effect"
facts: only normal and minion monsters; applied by any melee or ranged attack except blade sentinel, blade shield and extra multishot arrows; the target may keep fleeing after the effect expires until its next AI check; cannot overwrite grim ward or terror; if applied with Hit Blinds Target, flee takes precedence.
gaps: duration NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires. On fire the target must succeed on a Will save (DC 13) or flee from the attacker for 1d4 rounds (fear). Creatures of 17+ Hit Dice and mindless creatures are immune. Flee takes precedence over blind.

## GURPS 4e
On the same d100: Quick Contest Will against effective skill 13; on failure Terror for 1d4 seconds-rounds (4 to 24 seconds), exact 1d4 x 6 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Terrifying (Condition 25-30).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Duration is not in the source (1d4 rounds is the Terrifying row's). 2. The source's monsters 'may continue fleeing after expiry until their next AI check' has no 3.5e meaning.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.


---

### LIFE REGENERATION
**Diablo II weapon modifier — Magic affix ladder (PureDiablo) (https://www.purediablo.com/?p=3211)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Magic affix ladder (PureDiablo)
quality: clean
url: https://www.purediablo.com/?p=3211
tooltip: suffix "Regeneration" +3-5 life regeneration (req. 52).
facts: as returned.
gaps: the time unit of the regeneration NOT PRESENT.
```

## D&D 3.5e
While wielded the wielder has fast healing 1 (the Magic rung of the source's +3 to +5 life regeneration; the source gives no time unit). Fast healing is magical healing: it ends Fatal Wound stacks.

## GURPS 4e
Regeneration (slow) 1 HP per second while wielded, Gadget.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. The source's time unit is not given (the page says only '+3-5 life regeneration'); fast healing 1 is the Magic rung.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.


---

### OPEN WOUNDS
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "causes the target to begin Bleeding, applying damage and stopping damage regeneration for 8 seconds"
facts: applies only if monsters take damage or are regenerating; always applies to characters if the strike succeeds; damage effectiveness 1/2 for elites and act bosses, 1/4 for player characters (melee), 1/8 (ranged); no damage reduction can affect it; reapplication replaces the effect and resets the timer; duration cannot be reduced; life gain still works. Life drain per frame (1/256ths): level 1-15 9 x slvl + 31; 16-30 18 x slvl - 104; 31-45 27 x slvl - 374; 46-60 36 x slvl - 779; over 60 45 x slvl - 1319. Example: a level 50 character does 797.65 damage over 8 s (200 frames).
gaps: none.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires. On fire the target bleeds 3 HP at the start of its turn for 2 rounds (8 s) and for that time cannot regenerate or benefit from fast healing (magical healing still works). Untyped, ignores DR, bloodless creatures immune. A new proc refreshes the timer and does not stack. Against creatures of 17+ Hit Dice the bleed is 1 HP per round.

## GURPS 4e
On the same d100: Follow-Up Toxic Attack 6 HP spread over exactly 8 seconds; suppresses regeneration for 8 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Fatal Wound family (Affix Registry section 1) + Cursed Wound (Condition 55-60).

## NAME COLLISION
Fatal Wound family (stacking bleed) and DMG Wounding; names stay, never merge.

## FORKS NEEDING A RULING
1. The source's damage scales with the character level (about 800 over 8 s at level 50); a flat 3 per round is the Magic rung of the bleed rows. 2. D2's bleed does not stack, unlike Fatal Wound; kept.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.


---

### PIERCING ATTACK
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "Adds a chance to missile weapon attacks to Pierce the target when hit, and hit subsequent targets behind them"
facts: percent summed from all sources; blocking does not stop a piercing missile; a missile can pierce up to 4 times (5 targets); per-item chances: Stormstrike 25%, Gut Siphon 33%, Razortail 33%, Doomslinger 35%, Kuko Shakaku 50%, Ichorsting 50%, Warshrike 50%, Demon Machine 66%, Buriza-Do Kyanon 100%.
gaps: none.
```

## D&D 3.5e
Ranged weapons only. On each damaging hit, d100 01-25 fires (the Magic-rung of the source's 25 to 100% item values): the missile continues to the next creature in a straight line within 10 ft behind the target, which is attacked as normal; this repeats up to 4 times (5 targets). A shield or block does not stop the missile.

## GURPS 4e
On the same d100: the missile continues to the next target behind, up to 4 times; each target gets its own active defenses.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. The source chance is set per item (25 to 100%); 25% is the Magic rung. 2. 'Behind the target' is read as a line within 10 ft.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.


---

### PREVENT MONSTER HEAL
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "stops monster damage regeneration for 80 minutes (120,000 frames)"
facts: applied only by player characters (not mercenaries or iron golems); only if the monster takes damage; cannot be applied to Uber/Pandemonium event bosses (Lilith, Duriel, Izual, Mephisto, Diablo, Baal).
gaps: none.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires. On fire the target cannot regenerate or benefit from fast healing for 80 minutes (the source's duration); magical healing and potions still work. Not applied by allies or summoned creatures, and not against named bosses.

## GURPS 4e
On the same d100: regeneration and fast healing suppressed for 80 minutes.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Cursed Wound (Condition 55-60).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. The source applies it on every damaging hit (no chance); the ratified 10% proc is used to keep it a Registry-style proc. 2. Named bosses are immune (the source's list of event bosses).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.


---

## COVERED BY AN EXISTING REGISTRY ROW (no second document)

| Modifier | Existing row | Note |
|---|---|---|
| Attack Rating | Striking (Offensive 01-06) | Attack Rating is the 3.5e attack bonus: Striking +1/+1/+2/+3/+4. |
| Attack Speed | Rapid Assault (Offensive 25-30) | Percentage attack rate: Readiness and Alacrity read as the row's T5 to T4 (1/day extra attack), Swiftness and Quickness as T3 to T2 (3/day). |
| Cold Damage | Freezing (Elemental 09-16) | Cold damage with a chill duration: Freezing's rider plus its slow on crit at T3+. The source's chill length (1-4 s) is the row's one-round slow. |
| Damage Reduced | Stoneskin (Defensive 73-78) | Damage Reduced by 1/2/3 (flat per hit) is Stoneskin's 1/2/3/4/5 flat reduction after DR. |
| Damage vs Demons | Banefire (Elemental 93-96) / Demonslaying (WoW corpus) | Extra damage against a creature type: Banefire's +2d6 to +5d6 against a chosen subtype, here the demon subtype. |
| Damage vs Undead | DMG Bane (undead as the designated foe) / Radiant (Elemental 45-50) | Extra damage against undead: Bane (undead foe) or Radiant (positive energy, undead take x1.5). |
| Deadly Strike | Keen Edge (Offensive 13-18) / Lethal Focus (Offensive 31-36) | A chance to double physical damage is a critical hit; 3.5e already has threat range and crit multiplier, which Keen Edge widens and Lethal Focus adds to. No new family. |
| Enhanced Damage | Wounding (Offensive 07-12) | A percentage damage increase is read as Wounding's flat bonus damage +1/+1d4/+1d6/+2d6/+3d6; the percentage form has no 3.5e meaning. |
| Fire Damage | Flaming (Elemental 01-08) | Fire damage ladders (Flame to Incineration, Fiery to Condensing) are the same shape as Flaming's +1d4/+1d6/+1d8/+2d6/+3d6 rider; the large late-ladder numbers are D2's scale, not rescaled. |
| Knockback | Knockback (Condition 49-54) | Same effect (push on hit; the source's size-dependent chance maps to the row's 'creatures of your own size or smaller'). |
| Life Stolen | Leech (Resource 19-24) / Vampiric (MIC, this repo) | Heal as a share of damage dealt: Leech heals a flat 1/1/2/3/5 per hit; the percentage form is read as one HP per 5 damage rounded down, minimum 1 at the Magic rung. Undead (0% drain) give nothing, as bloodless targets do under Leech. |
| Lightning Damage | Shocking (Elemental 17-24) | Same rider; D2's wide min-max spread is a game feature the row's fixed dice already flatten. |
| Mana Stolen | Mana Leech (Resource 25-30) | Mana returned on a hit; Mana Leech's flat 1/2/3/5/8 per hit covers it. |
| Minimum and Maximum Damage | Wounding (Offensive 07-12) | Flat damage added to the weapon die is Wounding's flat bonus; D2's separate min and max have no 3.5e analogue. |
| Monster Defense per Hit | Overpower (Offensive 49-54) | Overpower reduces target AC and DR by 1/1/2/3/4 for a round on a hit; the source's Defense loss (-50 to -100) is the same effect at a different scale. |
| Poison Damage | Venomous (Elemental 33-38) | Poison over time (Blight to Anthrax, Septic to Pestilent): Venomous gives the poison rider and Cyclic GURPS tick. |
| Slows Target | Slowing (Condition 01-08) / Icy Chill (WoW corpus) | Slow on hit (the source's 30 s cap 90%/50% reduced to the row's slow-for-1-round); covered. |
| Target Defense Reduction | Overpower (Offensive 49-54) / Armor Piercing (Offensive 19-24) | Attacks resolve against lowered Defense; Overpower lowers AC on a hit, Armor Piercing ignores DR. Covered together. |

## OPEN VERIFICATION ITEMS

- Ignore Target's Defense: forks listed in its entry
- Chance to Cast on Attack: forks listed in its entry
- Chance to Cast on Striking: forks listed in its entry
- Crushing Blow: forks listed in its entry
- Freeze Target: forks listed in its entry
- Fires Explosive Arrows or Bolts: forks listed in its entry
- Fires Magic Arrows: forks listed in its entry
- Hit Blinds Target: forks listed in its entry
- Hit Causes Monster to Flee: forks listed in its entry
- Life Regeneration: forks listed in its entry
- Open Wounds: forks listed in its entry
- Piercing Attack: forks listed in its entry
- Prevent Monster Heal: forks listed in its entry
