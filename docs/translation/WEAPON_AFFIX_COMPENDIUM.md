# WEAPON AFFIX COMPENDIUM
**Corpus Mass Translation — D&D 3.5e Dungeon Master's Guide v3.5 (PDF pp. 224-227) and Magic Item Compendium (PDF pp. 29-47). Built 2026-10-04.**

## HOW TO USE / TIER OVERVIEW
Each entry is one weapon property: the printed source, the 3.5e rules, the GURPS crosswalk, price, pool coverage, collisions and forks. Item effects run on the 3.5e chassis; GURPS supplies only the defender's 3d6 contest and DR (`docs/translation/FUSED_ENGINE_RESOLUTION.md`, binding). Tier = the wielder band the property suits (rule in `weapon_affixes/triage_affixes.py`). `Registered` means indexed here; the Notion Affix Registry gets a full family entry the first time an affix is rolled or placed. Already ratified outside this corpus: Crusader (Registry section 2). Covered by an existing pool row and therefore not restated: 17 (listed at the end). Inactive: 10.

| Tier | Registered |
|---|---:|
| 1 Legendary | 4 |
| 2 Heroic Elite | 5 |
| 3 Heroic | 31 |
| 4 Competent | 78 |

## TIER 1 — LEGENDARY (levels 17-20)

### BRILLIANT ENERGY
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 225 (3.5e source; printed rules are the 3.5e side)**
**Tier 1 — Legendary (levels 17-20)** (tier rule in `triage_affixes.py`; price +4 = 32,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Brilliant Energy: A brilliant energy weapon has its significant portion--such as its blade, axe head, or arrowhead--transformed into light, although this does not modify the item's weight. It always gives off light as a torch (20-foot radius). A brilliant energy weapon ignores nonliving matter. Armor bonuses to AC (including any enhancement bonuses to that armor) do not count against it because the weapon passes through armor. (Dexterity, deflection, dodge, natural armor, and other such bonuses still apply.) A brilliant energy weapon cannot harm undead, constructs, and objects. This property can only be applied to melee weapons, thrown weapons, and ammunition.
Strong transmutation; CL 16th; Craft Magic Arms and Armor, gaseous form, continual flare; Price +4 bonus
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Melee, thrown weapons and ammunition only (not ranged launchers). Attacks against a target's AC ignore armor and shield bonuses. Weapon sheds torch light, 20 ft radius, cannot be shut off (concealment of the drawn weapon is impossible). It cannot harm undead, constructs or objects (damage 0; also no sunder or object use). No save, no SR, no DC, no proc, no action. Interaction with DR as normal. No Fatal Wound interaction.

## GURPS 4e
Chassis Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10% = -35%). Armor interaction: ignore worn-armor DR but not natural DR = Armor Divisor above the ladder anchors (2) +50% and (5) +150%; the "ignores worn armor" step is not in the brief or in gurps_trait_index (Armor Divisor is "Variable"), so the percentage is OPEN. Shield DB (active-defense bonus) treated as ignored to match the 3.5e shield clause: fork 2. Limitation for the no-harm clause: Accessibility "no effect on Unliving or inanimate targets" with percentage OPEN. Light: a torch's glow has no trait cost. Magical -10%. Points not computable.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+4 bonus-equivalent = 32,000 gp (bonus-squared x 2,000; matches printed +4).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Armor Piercing (Offensive 19-24).
none. Armor Piercing (Offensive 19-24) ignores hardness/DR, not AC bonuses; Overpower (49-54) lowers AC/DR on a hit; Penetrating Strikes (85-90) is material/insubstantial. Gap: nothing ignores armor and shield AC bonuses or carries the cannot-harm-undead/constructs/objects clause.

## NAME COLLISION
SRD Brilliant Energy (identical); pool Armor Piercing (Offensive 19-24; GURPS Armor Divisor ladder collides, see fork 1), Radiant (Elemental 45-50, light flavor only), Overpower, Penetrating Strikes; spell gaseous form / continual flame (prerequisites only).

## FORKS
1. GURPS Armor Divisor ladder collision with Armor Piercing T1 (Armor Divisor (5)). Recommended default: Brilliant Energy is a separate "ignores worn armor" step above (5); percentage set from the Basic Set before ratification.
2. Shield: 3.5e ignores the shield's AC bonus. Recommended default: GURPS ignores the shield's DB and its DR, but keeps Dodge/Parry skill.
3. "Cannot harm undead, constructs, objects" in GURPS. Recommended default: damage 0 vs targets tagged undead or construct on the 3.5e side, and vs inanimate objects.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- the "ignores worn armor" step is not in the brief or in gurps_trait_index (Armor Divisor is "Variable"), so the percentage is OPEN.
- Limitation for the no-harm clause: Accessibility "no effect on Unliving or inanimate targets" with percentage OPEN.


---

### DANCING
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 225 (3.5e source; printed rules are the 3.5e side)**
**Tier 1 — Legendary (levels 17-20)** (tier rule in `triage_affixes.py`; price +4 = 32,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Dancing: As a standard action, a dancing weapon can be loosed to attack on its own. It fights for 4 rounds using the base attack bonus of the one who loosed it and then drops. While dancing, it cannot make attacks of opportunity, and the person who activated it is not considered armed with the weapon. In all other respects, it is considered wielded or attended by the creature for all maneuvers and effects that target items (such as the sunder action or a heat metal spell). While dancing, it takes up the same space as the activating character and can attack adjacent foes (weapons with reach can attack opponents up to 10 feet away). The dancing weapon accompanies the person who activated it everywhere, whether she moves by physical or magical means. If the wielder who loosed it has an unoccupied hand, she can grasp it while it is attacking on its own as a free action; when so retrieved the weapon can't dance (attack on its own) again for 4 rounds.
Strong transmutation; CL 15th; Craft Magic Arms and Armor, animate objects; Price +4 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Standard action to loose it. For 4 rounds it makes its own attacks at the loosing creature's BAB (attacks per round: fork 1). It occupies the wielder's square, attacks adjacent foes (10 ft with reach), makes no attacks of opportunity, follows the wielder through any movement (physical or magical), and drops at the end of round 4. While dancing the wielder counts as unarmed with it but it is still wielded/attended for maneuvers and effects targeting items. A wielder with a free hand may catch it as a free action; a caught weapon cannot dance again for 4 rounds. Damage = weapon dice + enhancement and special-ability dice; wielder Str, Power Attack and class features do not apply (design; fork 2). No save, no SR, no DC. No Fatal Wound interaction.

## GURPS 4e
Chassis Gadget (Breakable DR 6 -25%, Can Be Stolen -10% = -35%); the sword is the Gadget, so Breakable matters: a dancing sword that is struck can be destroyed. Mechanism: an Ally-type animated weapon (pool precedent: Ally, Summonable, Minion) that attacks at the wielder's weapon skill (BAB mapping), exact 24 seconds (4 rounds x 6 s), then Takes Recharge 24 s (limitation, "Variable" in the index, percentage OPEN). Activation = one Ready/Concentrate maneuver (standard action). Ally cost is "Variable" in gurps_trait_index; no total stated; open. one attack per turn.
2. Damage bonuses. Recommended default: no Str/Dex-based damage; the weapon's own enhancement and special abilities count; GURPS skill = wielder's skill, damage uses the weapon's base damage with no ST thrust/swing bonus.
3. Two dancing weapons loosed by one wielder. Recommended default: allowed (one standard action each); the Cap is per weapon.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+4 bonus-equivalent = 32,000 gp (bonus-squared x 2,000; matches printed +4).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none. Closest are Minion/Spectral Guardian (Summoning 18, summons a creature, not the item), Echo Strike (Build-Around 41-50, duplicate strike) and Rapid Assault (Offensive 25-30, extra attacks); gap: nothing lets the weapon itself fight unattended on a timer.

## NAME COLLISION
SRD Dancing (identical); spell animate objects; SRD Dancing Lights; pool Minion, Spectral Guardian, Echo Strike, Shadow Clone (no shared mechanic).

## FORKS
1. Attacks per round. SRD says only "BAB of the one who loosed it." Recommended default: one attack per round at full BAB (no iterative attacks);

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: degraded.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Mechanism: an Ally-type animated weapon (pool precedent: Ally, Summonable, Minion) that attacks at the wielder's weapon skill (BAB mapping), exact 24 seconds (4 rounds x 6 s), then Takes Recharge 24 s (limitation, "Variable" in the index, percentage OPEN).


---

### PRISMATIC BURST
**Weapon property — Magic Item Compendium, PDF p. 41 (3.5e source; printed rules are the 3.5e side)**
**Tier 1 — Legendary (levels 17-20)** (tier rule in `triage_affixes.py`; price 30,000 gp (flat))

## SOURCE (verbatim, see packet header for normalization)
```
PRISMATIC BURST
Price: +30,000 gp
Property: Weapon
Caster Level: 13th
Aura: Strong; (DC 21) evocation
Activation: --
Whenever you score a successful critical hit with this weapon, multicolored light springs from the gems and cascades along its blade or head, subjecting the target to a prismatic spray effect (save DC 20; see spell description, PH 264). This effect activates even if the target is not normally subject to extra damage from critical hits.
Prerequisites: Craft Magic Arms and Armor, prismatic spray.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +30,000 gp; Property: Weapon; Caster Level: 13th; Aura: Strong; (DC 21) evocation; Activation: --; Prerequisites: Craft Magic Arms and Armor, prismatic spray.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, fixed DC 20.

## GURPS 4e
a randomized effect from a seven-entry table (effects OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed 30,000 gp flat.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none. The spell's seven rays include instant-death and petrification outcomes; this is the strongest crit rider in the batch.

## FORKS
1. use against PCs and named bosses (default: the effect works as printed on PCs; a named boss is a ruling at ratification). 2. whether the effect should be capped to the weaker rays for a rolled (non-authored) drop (default no, authored Unique-only).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- a randomized effect from a seven-entry table (effects OPEN).


---

### VORPAL
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 227 (3.5e source; printed rules are the 3.5e side)**
**Tier 1 — Legendary (levels 17-20)** (tier rule in `triage_affixes.py`; price +5 = 50,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Vorpal: This potent and feared ability allows the weapon to sever the heads of those it strikes. Upon a roll of natural 20 (followed by a successful roll to confirm the critical hit), the weapon severs the opponent's head (if it has one) from its body. Some creatures, such as many aberrations and all oozes, have no heads. Others, such as golems and undead creatures other than vampires, are not affected by the loss of their heads. Most other creatures, however, die when their heads are cut off. The DM may have to make judgment calls about this sword's effect. A vorpal weapon must be a slashing weapon. (If you roll this property randomly for an inappropriate weapon, reroll.)
Strong necromancy and transmutation; CL 18th; Craft Magic Arms and Armor, circle of death, keen edge; Price +5 bonus
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Natural 20, then a successful confirmation roll. The head is severed with no save and no SR. No effect on headless creatures (many aberrations, all oozes) or those unaffected by head loss (golems, undead other than vampires); creatures immune to crits cannot be vorpaled. Slashing weapons only. No d100 (printed trigger is the confirmed 20). The text does not call it a death effect, so Death Ward does not stop it. No Fatal Wound interaction. Fused-engine resolution: a confirmed natural-20 crit forces Head/Lethal on the location table.

## GURPS 4e
no instant-kill trait verified in my sources. Mechanism: trigger on a GURPS critical hit on the attack roll, effect "head severed", applying the same headless/unaffected exceptions. The 3.5e trigger is about 5% x confirm chance, while GURPS critical hits are 3-4 (and 5-6 at high skill), so the rates differ; the book rules and any trigger limitation are not retrieved and are open. Gadget -35%. Points: not computable.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+5 = 50,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none that matches. "Vorpal Edge" (Offensive 67-72) shares the name and the natural-20 trigger but is bonus slashing damage (base die x1..x3), not decapitation. Fortification (Defensive 07-12) negates crits and so blocks this. Gap: the instant-kill effect.

## NAME COLLISION
Vorpal Edge (Offensive 67-72), SRD vorpal sword (item), Keen Edge row (the SRD prerequisite spell is keen edge).

## RULINGS
1. A confirmed natural-20 crit from a vorpal weapon forces the Head location at Lethal severity on the fused engine's crit table; there is no separate save and the same table applies to PCs and named characters. 2. Not a death effect. 3. GURPS uses the same engine table.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

## TIER 2 — HEROIC ELITE (levels 13-16)

### BODY FEEDER
**Weapon property — Magic Item Compendium, PDF p. 31 (3.5e source; printed rules are the 3.5e side)**
**Tier 2 — Heroic Elite (levels 13-16)** (tier rule in `triage_affixes.py`; price +3 = 18,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
BODY FEEDER
Price: +3 bonus
Property: Weapon
Caster Level: 9th
Aura: Moderate; (DC 19) necromancy
Activation: --
Whenever a bodyfeeder weapon you wield scores a successful critical hit against a living creature, you gain temporary hit points equal to half the damage dealt by the critical hit. These temporary hit points last for up to 1 minute and don't stack with those from any other source, including additional critical hits with this weapon.
Prerequisites: Craft Magic Arms and Armor, vampiric touch or claws of the vampire (EPH 84).
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +3 bonus; Property: Weapon; Caster Level: 9th; Aura: Moderate; (DC 19) necromancy; Activation: --; Prerequisites: Craft Magic Arms and Armor, vampiric touch or claws of the vampire (EPH 84).; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed. Bloodless targets give nothing.

## GURPS 4e
temporary HP buffer equal to half the injury dealt, 1 minute (mechanism; a "Temporary HP" trait and cost OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+3 = 18,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Leech is flat HP per hit; Life Shield is a fixed temp-HP block). It scales with the crit's damage, so it is NOT flat-source; stated explicitly.

## FORKS
1. cap per crit (default none, as printed; the no-stack rule is the brake).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- a "Temporary HP" trait and cost OPEN).


---

### CURSESPEWING
**Weapon property — Magic Item Compendium, PDF p. 32 (3.5e source; printed rules are the 3.5e side)**
**Tier 2 — Heroic Elite (levels 13-16)** (tier rule in `triage_affixes.py`; price +3 = 18,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
CURSESPEWING
Price: +3 bonus
Property: Weapon
Caster Level: 11th
Aura: Moderate; (DC 20) necromancy
Activation: --


Whenever this weapon scores a critical hit against a target, it bestows a curse that imposes a -4 penalty on attack rolls, saving throws, skill checks, and ability checks for 1 minute. Multiple strikes aren't cumulative with one another.
Prerequisites: Craft Magic Arms and Armor, bestow curse.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +3 bonus; Property: Weapon; Caster Level: 11th; Aura: Moderate; (DC 20) necromancy; Activation: --; Prerequisites: Craft Magic Arms and Armor, bestow curse.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, trigger = confirmed critical hit, fixed -4, no save, no SR beyond the weapon's own (the printed text allows none; flagged).

## GURPS 4e
Affliction-style curse, -4 to all success rolls for 1 minute, Trigger critical (percentage OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+3 = 18,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
Weakening and Mind Fog (Condition pool) are narrower and use saves.

## FORKS
1. the printed property allows no save; default keep as printed, since it is +3 and crit-only.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Affliction-style curse, -4 to all success rolls for 1 minute, Trigger critical (percentage OPEN).


---

### ETHEREAL REAVER
**Weapon property — Magic Item Compendium, PDF p. 35 (3.5e source; printed rules are the 3.5e side)**
**Tier 2 — Heroic Elite (levels 13-16)** (tier rule in `triage_affixes.py`; price +3 = 18,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
ETHEREAL REAVER
Price: +3 bonus
Property: Melee weapon
Caster Level: 12th
Aura: Strong; (DC 21) divination
Activation: --
An ethereal reaver weapon functions as a ghost touch weapon (DMG 224). In addition, such a weapon allows you to see invisible creatures as if you were subject to a see invisibility spell.
Prerequisites: Craft Magic Arms and Armor, see invisibility.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +3 bonus; Property: Melee weapon; Caster Level: 12th; Aura: Strong; (DC 21) divination; Activation: --; Prerequisites: Craft Magic Arms and Armor, see invisibility.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Ghost Touch plus continuous see invisibility while wielding.

## GURPS 4e
Ghost Touch's Affects Insubstantial plus See Invisible (Gadget; costs OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed +3 = 18,000 gp (a +1 base ability plus a continuous detection effect).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Ghost Touch (DMG) + Truesight (Utility 31-36).
DMG Ghost Touch (see that file) covers the first half; Truesight (Utility 31-36) gives See Invisibility 1/day at T4, at will only at T1.

## FORKS
none beyond Ghost Touch's.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- costs OPEN).


---

### IMPLACABLE
**Weapon property — Magic Item Compendium, PDF p. 38 (3.5e source; printed rules are the 3.5e side)**
**Tier 2 — Heroic Elite (levels 13-16)** (tier rule in `triage_affixes.py`; price +3 = 18,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
IMPLACABLE
Price: +3 bonus
Property: Weapon
Caster Level: 9th
Aura: Moderate; (DC 18) necromancy
Activation: --
When an implacable weapon deals damage to a living creature, the wound bleeds profusely and the creature takes 2 additional points of damage at the start of each of the wielder's turns for the next 5 rounds. Multiple wounds are cumulative (a creature struck three times in the same round would take 6 points of damage per round for the next 5 rounds). This bleeding can be stopped by a successful DC 15 Heal check or any effect that restores hit points (such as cure light wounds). However, while the wound is active, anyone attempting to cast a spell on the target that would restore hit points must succeed on a DC 15 caster level check. An implacable weapon counts as adamantine for the purpose of overcoming the damage reduction of aberrations.
Prerequisites: Craft Magic Arms and Armor, vampiric touch.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +3 bonus; Property: Weapon; Caster Level: 9th; Aura: Moderate; (DC 18) necromancy; Activation: --; Prerequisites: Craft Magic Arms and Armor, vampiric touch.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed. Stacking is additive and linear (consistent with the stacking doctrine). No cap is printed; flagged.

## GURPS 4e
Innate Attack (Toxic) Follow-Up, Cyclic (+400% per cycle), no ST linkage; the per-wound five-round expiry is the cycle count (point total OPEN). Bloodless targets (constructs, undead, oozes, elementals) are immune, per the Registry baseline and the printed "living creature".

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+3 = 18,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
the ratified Fatal Wound family (Registry section 1) is the Registry's stacking bleed: proc 10/15/20%, ticks 1-3 per stack, caps 3/4/5, a fatal state at cap. Implacable is a second, harder stacking bleed (every damaging hit, 2 per stack, uncapped, 5-round expiry per wound).

## RULINGS
1. cap at 5 stacks, matching the Fatal Wound Unique cap, because an uncapped stack is a death spiral). 2. healing: the printed "any effect that restores hit points stops the bleeding" agrees with the Registry norm, so any magical healing, including the Crusader heal (D2 reversed 2026-10-04), ends Implacable's wounds. 3. overlap with Fatal Wound on one weapon (default not allowed together).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- the per-wound five-round expiry is the cycle count (point total OPEN).


---

### NECROTIC FOCUS
**Weapon property — Magic Item Compendium, PDF p. 40 (3.5e source; printed rules are the 3.5e side)**
**Tier 2 — Heroic Elite (levels 13-16)** (tier rule in `triage_affixes.py`; price +3 = 18,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
NECROTIC FOCUS
Price: +3 bonus
Property: Melee weapon
Caster Level: 7th
Aura: Moderate; (DC 18) necromancy
Activation: --
A necrotic focus weapon serves as a channel for your ability drain or energy drain supernatural ability. While wielding it, you deal ability drain or bestow negative levels through it as if attacking with your natural weapons. If a saving throw against the effect is allowed, add the weapon's enhancement bonus to the save DC.
Prerequisites: Craft Magic Arms and Armor, enervation, spectral hand.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +3 bonus; Property: Melee weapon; Caster Level: 7th; Aura: Moderate; (DC 18) necromancy; Activation: --; Prerequisites: Craft Magic Arms and Armor, enervation, spectral hand.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, gated by a monster or class drain ability.

## GURPS 4e
deliver the drain through the weapon (OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+3 = 18,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- deliver the drain through the weapon (OPEN).


---

## TIER 3 — HEROIC (levels 9-12)

### ANARCHIC
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 224 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Anarchic: An anarchic weapon is chaotically aligned and infused with the power of chaos, It makes the weapon chaos-aligned and thus bypasses the corresponding damage reduction, It deals an extra 2d6 points of damage against all of lawful alignment. It bestows one negative level on any lawful creature attempting to wield it. The negative level remains as long as the weapon is in, hand and disappears when the weapon is no longer wielded. This negative level never results in actual level loss, bur it-canner be overcome. in_any.way (including restoration spells) while the weapon. is wielded. Bows, crossbows, and slings so. crafted bestow the chaotic power upon. their ammunition.
Moderate evocation [chaotic]; CL 7th; Craft Magic Arms and Armor, chaos hammer, creator must be chaotic; Price +2 bonus,
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Weapon counts as chaos-aligned (bypasses DR/chaotic). Every damaging hit on a creature with a lawful alignment component adds +2d6 untyped damage (not multiplied on a crit). No save, no SR, no DC. A lawful creature wielding it gains 1 negative level for as long as it holds the weapon; removable by no effect while held; ends when released; never converts to level loss; standard negative-level rules apply. Bow, crossbow or sling confers the chaotic quality and the +2d6 to its ammunition. No Fatal Wound interaction (no healing).

## GURPS 4e
Chassis: Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10% = -35%). Extra damage = Innate Attack, Follow-Up (+0%), 2d, by the Executioner row precedent (3.5e +2d6 = 2d); Accessibility "only vs. lawful-aligned targets" -20% by the Hunter's Mark precedent (percentage open for ratification); Magical -10%. Limitations total -65% (inside the -80% cap). Base Innate Attack cost per die is "Variable" in gurps_trait_index, so no point total is stated; open. Damage type for the rider: open (no precedent for alignment damage). Wielder penalty for a lawful wielder: mechanism open (see fork 2). No d100 on either side.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 bonus-equivalent = 8,000 gp (bonus-squared x 2,000; matches the printed +2).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none. Closest are Banefire (Elemental 93-96, element-subtype only), Chaos Element (Elemental 97-100, random element, unrelated) and Penetrating Strikes (Offensive 85-90, material DR, not alignment); gap: no row for alignment-keyed bonus damage, alignment-DR bypass, or a wielder-penalty clause.

## NAME COLLISION
SRD Axiomatic (opposed twin; also queued); SRD Holy/Unholy (queued; same "extra 2d6 vs aligned" template); spell chaos hammer; pool Chaos Element (name echo only).

## FORKS
1. RULED by the engine: the target's alignment is read from its 3.5e stat block; no GURPS alignment tag is built.
2. RULED by the engine: a wrong-aligned wielder takes the Energy Drained condition while holding the weapon (-1 attacks/saves/skills/ability checks, -5 HP, -1 effective level; never level loss).
3. Anarchic and Axiomatic on one weapon. Recommended default: mutually exclusive (contradictory alignment; SRD fetched text does not say).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### AQUAN
**Weapon property — Magic Item Compendium, PDF p. 29 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
AQUAN
Price: +2 bonus
Property: Weapon
Caster Level: 7th
Aura: Moderate; (DC 18) evocation
Activation: --
An aquan weapon automatically overcomes the damage reduction of any creature that has the fire subtype. In addition, the weapon deals an extra 2d6 points of damage against such creatures. An aquan weapon also bestows one negative level on any creature that has the fire subtype and attempts to wield it. The negative level remains as long as the weapon is in hand and disappears when the weapon is no longer held. This negative level never results in actual level loss, but it cannot be overcome in any way (including restoration spells) while the weapon is wielded.
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, water subtype.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 7th; Aura: Moderate; (DC 18) evocation; Activation: --; Prerequisites: Craft Magic Arms and Armor, water subtype.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, 2d6 untyped, not multiplied on a crit.

## GURPS 4e
Innate Attack Follow-Up 2d with Accessibility "only vs. the opposed subtype" (percentage OPEN); DR-bypass has no GURPS effect beyond the tag; wielder penalty the Energy Drained condition while held (engine ruling)design intent, same default as the alignment weapons).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Banefire (Elemental 93-96).
Banefire (Elemental 93-96, +2d6 vs a chosen element subtype) gives the 2d6 rider. Delta = the DR bypass and the subtype-wielder negative level. One family with Auran (earth), Ignan (water) and Terran (air), all +2: weapon keyed to the subtype opposed to its element.

## FORKS
shared with the alignment-weapon rulings (GURPS subtype tag, wielder penalty); Aquan and Banefire on one weapon, default not allowed.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- the opposed subtype" (percentage OPEN);


---

### AURAN
**Weapon property — Magic Item Compendium, PDF p. 29 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
AURAN
Price: +2 bonus
Property: Weapon
Caster Level: 7th
Aura: Moderate; (DC 18) evocation
Activation: --
An auran weapon automatically overcomes the damage reduction of any creature that has the earth subtype. In addition, the weapon deals an extra 2d6 points of damage against such creatures. An auran weapon also bestows one negative level on any creature that has the earth subtype and attempts to wield it. The negative level remains as long as the weapon is in hand and disappears when the weapon is no longer held. This negative level never results in actual level loss, but it cannot be overcome in any way (including restoration spells) while the weapon is wielded.
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, air subtype.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 7th; Aura: Moderate; (DC 18) evocation; Activation: --; Prerequisites: Craft Magic Arms and Armor, air subtype.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Keyed to the EARTH subtype instead of fire: read every 'fire subtype' in the Aquan text as 'earth subtype'. as printed, 2d6 untyped, not multiplied on a crit.

## GURPS 4e
Innate Attack Follow-Up 2d with Accessibility "only vs. the opposed subtype" (percentage OPEN); DR-bypass has no GURPS effect beyond the tag; wielder penalty the Energy Drained condition while held (engine ruling)design intent, same default as the alignment weapons).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Banefire (Elemental 93-96).
Banefire (Elemental 93-96, +2d6 vs a chosen element subtype) gives the 2d6 rider. Delta = the DR bypass and the subtype-wielder negative level. One family with Auran (earth), Ignan (water) and Terran (air), all +2: weapon keyed to the subtype opposed to its element.

## FORKS
shared with the alignment-weapon rulings (GURPS subtype tag, wielder penalty); Aquan and Banefire on one weapon, default not allowed.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- the opposed subtype" (percentage OPEN);


---

### AXIOMATIC
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 224 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Axiomatic: An axiomatic weapon is lawfully aligned and infused with the power of law. Ir. makes the weapon low-aligned


and thus bypasses the corresponding damage reduction. It deals an extra 2dé points of damage against all of chaotic alignment. It bestows one negative level on any chaotic creature attempting to wield it. The negative level remains as long as the weapon is in hand and disappears when the weapon is no longer wielded, This. negative level newer results in actual level loss, bur it cannot be overcome in any way (including restoration spells) while the weapon is wielded. Bows, crossbows, and slings so crafted bestow the lawful power upon their ammunition.
Moderate evocation [lawful]; CL 7th; Craft Magic Arms and Armor, order's wrath, creator must be lawful; Price +2 bonus,
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Weapon counts as law-aligned (bypasses DR/lawful). Every damaging hit on a creature with a chaotic alignment component adds +2d6 untyped damage (not multiplied on a crit). No save, no SR, no DC. A chaotic creature wielding it gains 1 negative level while it holds the weapon; removable by no effect while held; ends when released; never converts to level loss; standard negative-level rules apply. Bow, crossbow or sling confers the lawful quality and the +2d6 to its ammunition. No Fatal Wound interaction (no healing).

## GURPS 4e
Chassis: Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10% = -35%). Extra damage = Innate Attack, Follow-Up (+0%), 2d, by the Executioner row precedent (3.5e +2d6 = 2d); Accessibility "only vs. chaotic-aligned targets" -20% by the Hunter's Mark precedent (percentage open for ratification); Magical -10%. Limitations total -65% (inside the -80% cap). Base Innate Attack cost per die is "Variable" in gurps_trait_index, so no point total is stated; open. Damage type for the rider: open. Wielder penalty for a chaotic wielder: mechanism open (see fork 2). No d100 on either side.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 bonus-equivalent = 8,000 gp (bonus-squared x 2,000; matches the printed +2).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none. Closest are Banefire (Elemental 93-96, element-subtype only) and Penetrating Strikes (Offensive 85-90, material DR, not alignment); gap: no row for alignment-keyed bonus damage, alignment-DR bypass, or a wielder-penalty clause.

## NAME COLLISION
SRD Anarchic (opposed twin; also queued); SRD Holy/Unholy (queued; same template); spell order's wrath. The adjective "axiomatic" also names a creature subtype/template in the SRD (axiomatic creatures); unrelated to the weapon quality.

## FORKS
1. RULED by the engine: the target's alignment is read from its 3.5e stat block; no GURPS alignment tag is built.
2. RULED by the engine: a wrong-aligned wielder takes the Energy Drained condition while holding the weapon (-1 attacks/saves/skills/ability checks, -5 HP, -1 effective level; never level loss).
3. Axiomatic and Anarchic on one weapon. Recommended default: mutually exclusive (contradictory alignment; SRD fetched text does not say).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### BANISHING
**Weapon property — Magic Item Compendium, PDF p. 29 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
BANISHING
Price: +2 bonus
Property: Weapon
Caster Level: 13th
Aura: Strong; (DC 21) abjuration
Activation: Free (command)


When you strike an extraplanar creature of 26 Hit Dice or fewer while wielding a weapon that has this property, you can activate the weapon to banish that creature back to its home plane (Will DC 20 negates). A creature so banished cannot return for at least 24 hours. A creature that succeeds on its save cannot be banished by the same weapon for 24 hours.
If the creature struck has damage reduction that requires a particular weapon alignment or special material to overcome, increase the save DC by 2 for each such property shared by the weapon. For example, if you use a holy banishing cold iron weapon against a hezrou (damage reduction 10/good), the save DC would increase by 2, while against a marilith (damage reduction 10/good and cold iron), the save DC would increase by 4.
The banishing property can be activated three times per day.
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, banishment.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 13th; Aura: Strong; (DC 21) abjuration; Activation: Free (command); Prerequisites: Craft Magic Arms and Armor, banishment.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; the DC is fixed at 20 (flat), +2 per shared DR property.

## GURPS 4e
Affliction-style banish with a Will resistance roll, 3/day (Limited Use percentage OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Dispelling Strike is Condition 85-90 and neutralizes magic).

## FORKS
1. does the damage-through rule apply (default: the strike must deal damage).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Affliction-style banish with a Will resistance roll, 3/day (Limited Use percentage OPEN).


---

### BLINDSIGHTED
**Weapon property — Magic Item Compendium, PDF p. 30 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
BLINDSIGHTED
Price: +2 bonus
Property: Weapon
Caster Level: 6th
Aura: Moderate; (DC 18) divination
Activation: Standard (command)
When activated, a blindsighted weapon emits a susurrus of whispered notes (Listen DC 10). While wielding the activated weapon, you gain blindsight out to 30 feet. This effect is negated by silence spells and effects. The blindsighted property functions three times per day, and the effect lasts for 1 minute.
Prerequisites: Craft Magic Arms and Armor, see invisibility.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 6th; Aura: Moderate; (DC 18) divination; Activation: Standard (command); Prerequisites: Craft Magic Arms and Armor, see invisibility.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
the Blindsight-equivalent perception advantage at 30 ft (named trait and cost OPEN) with Limited Use 3/day.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Darksight and Truesight give vision modes, not blindsight).

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- the Blindsight-equivalent perception advantage at 30 ft (named trait and cost OPEN) with Limited Use 3/day.


---

### BLURSTRIKE
**Weapon property — Magic Item Compendium, PDF p. 30 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
BLURSTRIKE
Price: +2 bonus
Property: Melee weapon
Caster Level: 6th
Aura: Moderate; (DC 18) illusion
Activation: Swift (command)


When activated, a blurstrike weapon partially fades from view for 1 round, appearing only as a faint outline (though you, as the wielder, can see it normally). When you attack, an activated blurstrike weapon (along with your hand and arm) appears to others as an amorphous blur, preventing a foe from knowing exactly where the blow is aimed. After you activate this property, your opponent is considered flat-footed against the first attack you make with the blurstrike weapon in the round when you activate it. Creatures that don't rely on sight for combat (such as those with the blindsight special quality) and creatures with uncanny dodge aren't treated as flat-footed against this attack. The blurstrike property functions ten times per day.
Prerequisites: Craft Magic Arms and Armor, blur.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Melee weapon; Caster Level: 6th; Aura: Moderate; (DC 18) illusion; Activation: Swift (command); Prerequisites: Craft Magic Arms and Armor, blur.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, 10 uses/day, no save.

## GURPS 4e
the target is Surprised against the first attack of the round (the combat modifier is OPEN); sight-independent defenders and Danger Sense are excluded.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- the target is Surprised against the first attack of the round (the combat modifier is OPEN);


---

### COLLISION
**Weapon property — Magic Item Compendium, PDF p. 32 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
COLLISION
Price: +2 bonus
Property: Weapon
Caster Level: 6th
Aura: Moderate; (DC 18) transmutation
Activation: --
A collision weapon temporarily increases its own mass at the end point of each swing or shot. When you wield such a weapon, you deal an extra 5 points of damage with each hit.
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, weapon of impact (SC 237).
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 6th; Aura: Moderate; (DC 18) transmutation; Activation: --; Prerequisites: Craft Magic Arms and Armor, weapon of impact (SC 237).; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** +5 untyped damage per hit, not multiplied on a crit.

## GURPS 4e
+2 to damage per hit (the 2:1 conversion rounded, OPEN) or Innate Attack Follow-Up 1d+... (OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
Wounding (Offensive 07-12, bonus damage +1/+1d4/+1d6/+2d6/+3d6) is dice-based and tiered; this is a flat +5.

## FORKS
1. GURPS conversion of a flat +5 (default +2).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- +2 to damage per hit (the 2:1 conversion rounded, OPEN) or Innate Attack Follow-Up 1d+...
- (OPEN).


---

### DISARMING
**Weapon property — Magic Item Compendium, PDF p. 33 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
DISARMING
Price: +2 bonus
Property: Weapon
Caster Level: 5th
Aura: Moderate; (DC 17) transmutation
Activation: --
A disarming weapon grants you a +2 bonus on disarm attempts. In addition, opponents cannot disarm you of this weapon.
Prerequisites: Craft Magic Arms and Armor, bull's strength.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 5th; Aura: Moderate; (DC 17) transmutation; Activation: --; Prerequisites: Craft Magic Arms and Armor, bull's strength.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed (a +2 competence-style bonus; immune to disarm for the weapon).

## GURPS 4e
+2 on the contest to disarm (Weapon Bond-style bonus) and the weapon cannot be taken by a Disarm technique (Weapon Bond precedent, cost OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- +2 on the contest to disarm (Weapon Bond-style bonus) and the weapon cannot be taken by a Disarm technique (Weapon Bond precedent, cost OPEN).


---

### DISRUPTION
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 225 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Disruption: A weapon of disruption is the bane of all undead. Any undead creature struck in combat must succeed on a DC 14 Will save or be destroyed. A weapon of disruption must be a bludgeoning weapon. (If you roll this property randomly for a piercing or slashing weapon, reroll.)
Strong conjuration; CL 14th; Craft Magic Arms and Armor, heal; Price +2 bonus,
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Bludgeoning weapons only (reroll or refuse on piercing/slashing). Each hit on an undead creature forces a DC 14 Will save; failure destroys the undead (it is not a death or mind-affecting effect in the fetched text; incorporeal undead need their own means to be struck). Success leaves the hit as a normal attack. No SR is stated. Each hit rolls its own save. No effect on living, constructs or objects. No Fatal Wound interaction (bloodless targets only; no healing).

## GURPS 4e
Chassis Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10% = -35%). Mechanism: Follow-Up (+0%) rider on a DR-penetrating hit against an Undead target (Accessibility "only vs. undead", percentage OPEN), resisted by a Will roll, failure = destroyed. GURPS has no stock "destroyed" Affliction effect and the d20 DC 14 does not map to a 3d6 Will contest by any retrievable rule, so the effect type and the resistance modifier are OPEN. Magical -10%. Point total not computable.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 bonus-equivalent = 8,000 gp (bonus-squared x 2,000; matches printed +2).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Radiant (Elemental 45-50), Turn Mastery (Skill/Class 43-48).
none. Radiant (Elemental 45-50) deals extra damage to undead (x1.5), Turn Mastery (Skill/Class 43-48) improves turning, Soul Anchor (Condition 97-100) acts on kills; gap: no row destroys an undead outright on a failed save.

## NAME COLLISION
SRD Disruption (identical); spell disrupt undead, SRD Bane (undead as designated foe, +1 affix; stacks); pool Radiant, Turn Mastery, Soul Anchor.

## FORKS
1. "Struck in combat": must the hit deal damage past DR before the save? Recommended default: yes (proc-conventions §1: a hit that deals no damage rolls nothing), so a DR-immune lich is not auto-triggered.
2. Named/unique undead. SRD gives no exemption. Recommended default: as printed (a failed DC 14 save destroys), with the DM free to flag a named undead as immune before ratification.
3. GURPS effect and resistance for "destroyed". Recommended default: treat as an instant destroy on a failed Will roll, penalty set from the Basic Set (number open).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- undead", percentage OPEN), resisted by a Will roll, failure = destroyed.
- GURPS has no stock "destroyed" Affliction effect and the d20 DC 14 does not map to a 3d6 Will contest by any retrievable rule, so the effect type and the resistance modifier are OPEN.


---

### DOMINEERING
**Weapon property — Magic Item Compendium, PDF p. 34 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
DOMINEERING
Price: +2 bonus
Property: Weapon
Caster Level: 11th
Aura: Moderate; (DC 20) necromancy
Activation: --
A creature hit by a domineering weapon becomes shaken for 1 minute (Will DC 16 negates). This effect doesn't stack with itself or with any other fear effects (it can't render an already shaken creature frightened, for example).
Prerequisites: Craft Magic Arms and Armor, fear.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 11th; Aura: Moderate; (DC 20) necromancy; Activation: --; Prerequisites: Craft Magic Arms and Armor, fear.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, flat DC 16.

## GURPS 4e
Affliction (Fright/Fear-lite), Will resistance, every hit (Cyclic not used; percentage OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Terrifying (Condition 25-30).
Terrifying (Condition 25-30): on hit 1/encounter, fear 1d4 rounds, DC 13/15/17/20/24. Delta = every-hit shaken, no daily limit, weaker condition, fixed DC 16.

## FORKS
1. fear immunity applies as normal.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- percentage OPEN).


---

### DOOM BURST
**Weapon property — Magic Item Compendium, PDF p. 34 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
DOOM BURST
Price: +2 bonus
Property: Weapon
Caster Level: 11th
Aura: Moderate; (DC 20) necromancy
Activation: --
Whenever you score a critical hit with this weapon, a wave of blackness washes over the target, causing it to become shaken (no saving throw) for 5 rounds. This effect activates even if the creature struck is not normally subject to extra damage from critical hits. This effect doesn't stack with itself or with any other fear effects (it can't render an already shaken creature frightened, for example).
Prerequisites: Craft Magic Arms and Armor, fear.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 11th; Aura: Moderate; (DC 20) necromancy; Activation: --; Prerequisites: Craft Magic Arms and Armor, fear.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, trigger confirmed crit, no save (flagged), 5 rounds.

## GURPS 4e
Affliction (Fright-lite), Trigger critical, no resistance roll (percentage OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none for the crit-trigger shaken.

## FORKS
1. no save printed, kept (crit-only, weak condition); fear-immune targets stay immune.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Affliction (Fright-lite), Trigger critical, no resistance roll (percentage OPEN).


---

### ENERGY AURA
**Weapon property — Magic Item Compendium, PDF p. 35 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
ENERGY AURA
Price: +2 bonus
Property: Weapon
Caster Level: 15th
Aura: Strong; (DC 22) evocation
Activation: Standard (command)
Once activated, each hit by this weapon deals an extra 1d6 points of damage of an energy type of your choice (acid, cold, electricity, or fire, chosen when activated). This energy does not harm you, regardless of the type selected. The energy damage remains the same until you activate the weapon again.
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, chill metal, flame blade, Melf's acid arrow, shocking grasp.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 15th; Aura: Strong; (DC 22) evocation; Activation: Standard (command); Prerequisites: Craft Magic Arms and Armor, chill metal, flame blade, Melf's acid arrow, shocking grasp.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
Innate Attack Follow-Up with Variable Special Effect (the pool's Prismatic and Chaos Element rows reference variable effects; modifier OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Flaming / Freezing / Shocking / Corroding (Elemental).
Flaming, Freezing, Shocking and Corroding (Elemental pool) each give +1d6 at T4 as a fixed element. Delta = switchable element. The extra +1 over a single element pays for the switch.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- modifier OPEN).


---

### ENERVATING
**Weapon property — Magic Item Compendium, PDF p. 35 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
ENERVATING
Price: +2 bonus
Property: Weapon
Caster Level: 11th
Aura: Moderate; (DC 20) necromancy
Activation: --
When you score a critical hit against a living creature with an enervating weapon, the weapon bestows one negative level on the target. Assuming the subject survives, it regains lost levels after 1 hour. Usually, negative levels have a chance of permanently draining a victim's levels, but the negative levels from the enervating property don't last long enough to do so.
Prerequisites: Craft Magic Arms and Armor, enervation.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 11th; Aura: Moderate; (DC 20) necromancy; Activation: --; Prerequisites: Craft Magic Arms and Armor, enervation.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, no save printed (flagged), crit-only, one level per crit (stacks per crit, each recovers after its own hour). The negative level is the Energy Drained condition for 1 hour (engine).

## GURPS 4e
Trigger: a confirmed critical hit on a living creature (crits are undefended, so no defender 3d6 roll). Effect: one Energy Drained negative level (-1 attacks/saves/skills/ability checks, -5 HP, -1 effective level); no save printed, none added. Fades after 1 hour; never becomes level loss. Repeated crits add one level each, additive. Gadget chassis Breakable -25% / Can Be Stolen -10%; uncosted.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Weakening and Exhaustion are narrower).

## FORKS
1. stacking of repeated crits (default additive, never multiplicative; cap none printed).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### FLAMING BURST
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 225 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Flaming Burst: A flaming burst weapon functions as a flaming weapon that also explodes with flame upon striking a successful critical hit. The fire does not harm the wielder. In addition to the extra fire damage from the flaming ability (see above), a flaming burst weapon deals an extra 1d10 points of fire damage on a successful critical hit. If the weapon's critical multiplier is x3, add an extra 2d10 points of fire damage instead, and if the multiplier is x4, add an extra 3d10 points of fire damage. Bows, crossbows, and slings so crafted bestow the fire energy upon their ammunition. Even if the flaming ability is not active, the weapon still deals its extra fire damage on a successful critical hit.
Strong evocation; CL 12th; Craft Magic Arms and Armor and flame blade, flame strike, or fireball; Price +2 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** On a confirmed critical hit, add fire damage: x2 weapon 1d10, x3 weapon 2d10, x4 weapon 3d10 (x5+ not printed; fork 3). Not multiplied by the crit. Works with the flaming toggle off, and against creatures immune to crits. Fire immunity/resistance applies. Ammunition inherits it (bow, crossbow, sling). No save, no SR, no DC. No healing interaction.

## GURPS 4e
Chassis Gadget (Breakable DR 6 -25%, Can Be Stolen -10% = -35%). Second Innate Attack (Burning), Follow-Up (+0%), Trigger: critical hit only, 1d / 2d / 3d by the weapon's multiplier class (Lethal Focus precedent maps 1d6/2d6/3d6 to 1d/2d/3d; the d10 vs d6 difference is not carried, fork 2). Trigger percentage is "Variable" in the index, so OPEN. Magical -10%. Base Innate Attack cost per die also open; no point total.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
Printed +2 total = 8,000 gp (bonus-squared x 2,000), sold as one affix that replaces Flaming (not Flaming 2,000 + a separate +1 delta; fork 1).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Flaming (Elemental 01-08).
Flaming (Elemental 01-08, T4 = 1d6 fire; IA Burning, Follow-Up) covers the base. Lethal Focus (Offensive 31-36) is untyped crit-only dice; Elemental Burst (Elemental 75-80) is an area burst. Gap: neither is the printed fire rider on a confirmed crit scaled by critical multiplier.

## NAME COLLISION
pool Elemental Burst (Elemental 75-80, 10-ft area, Ref half; NOT this ability, since the SRD burst is not an area); pool Flaming; SRD Icy Burst, Shocking Burst, Thundering (queued; same crit-burst template).

## FORKS
1. Price when combined. Recommended default: Flaming Burst is a standalone +2 that includes Flaming; never stack Flaming and Flaming Burst on one weapon.
2. GURPS dice mapping for d10. Recommended default: 1d / 2d / 3d, as Lethal Focus; revisit if d10 average (5.5) needs a +1.
3. Engine ruling: the weapon's own 3.5e crit multiplier applies; no GURPS conversion is needed.5e multiplier class (x2/x3/x4) to pick 1d/2d/3d; x5+ not printed, so no rung.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Trigger percentage is "Variable" in the index, so OPEN.


---

### FLESHGRINDING
**Weapon property — Magic Item Compendium, PDF p. 36 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
FLESHGRINDING
Price: +2 bonus
Property: Piercing or slashing melee weapon
Caster Level: 11th
Aura: Moderate; (DC 20) transmutation
Activation: Free (command)
You can activate a fleshgrinding weapon any time you deal damage with it to a living creature in melee. When this occurs, you let go of the weapon and it magically animates, grinding itself into the foe's flesh. In each round at the start of your turn, it automatically damages that creature as if you had scored a normal hit with it (including damage from the weapon's enhancement bonus, other weapon properties, and your normal bonus from Strength, but not extra damage from feats such as Power Attack). The grinding continues for 5 rounds or until you or someone else pulls the fleshgrinding weapon free; doing this requires a standard action and (for anyone other than you) a successful DC 20 Strength check. After the duration expires, a fleshgrinding weapon returns to your hand (as the returning weapon property). It will not return to your hand if the target has pulled the weapon free and still holds it.
Prerequisites: Craft Magic Arms and Armor, animate objects.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Piercing or slashing melee weapon; Caster Level: 11th; Aura: Moderate; (DC 20) transmutation; Activation: Free (command); Prerequisites: Craft Magic Arms and Armor, animate objects.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed. It scales with the wielder's Strength and the weapon's properties, stated explicitly; no daily limit printed. Bloodless targets: the text says "living creature", so constructs and undead are immune.

## GURPS 4e
repeated Innate Attack equal to a normal hit each second for 5 turns, ended by pulling it free (Contest of ST DC-equivalent, OPEN); Cyclic is the cost carrier (+400% per cycle, from the Registry constants) but the percentage and the Follow-Up interplay are OPEN.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Fatal Wound is a stacking bleed with a proc; this is a weapon-driven repeating hit).

## FORKS
1. the wielder is unarmed for 5 rounds; default as printed.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- repeated Innate Attack equal to a normal hit each second for 5 turns, ended by pulling it free (Contest of ST DC-equivalent, OPEN);
- Cyclic is the cost carrier (+400% per cycle, from the Registry constants) but the percentage and the Follow-Up interplay are OPEN.


---

### FORCE
**Weapon property — Magic Item Compendium, PDF p. 36 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
FORCE
Price: +2 bonus
Property: Projectile weapon
Caster Level: 9th
Aura: Moderate; (DC 19) evocation
Activation: --
A projectile weapon with the force property turns ammunition shot from it into a force attack. These force projectiles automatically overcome damage reduction and suffer no miss chance against incorporeal targets, but they don't damage creatures immune to force effects. Ammunition shot from a force weapon deals the same amount of damage as normal ammunition.
Prerequisites: Craft Magic Arms and Armor, magic missile.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Projectile weapon; Caster Level: 9th; Aura: Moderate; (DC 19) evocation; Activation: --; Prerequisites: Craft Magic Arms and Armor, magic missile.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
Armor Divisor "ignores DR" (the pool's Armor Divisor ladder tops at 5; the "ignore" step is OPEN) plus Affects Insubstantial.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
Armor Piercing (Offensive 19-24: ignore DR 2/3/5/8/10) is capped; this bypasses all DR.

## FORKS
1. force-immune targets (only the printed ones).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- the "ignore" step is OPEN) plus Affects Insubstantial.


---

### HOLY
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 226 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Holy: A holy weapon is imbued with holy power. This power makes the weapon good-aligned and thus bypasses the corresponding damage reduction. It deals an extra 2d6 points of damage against all of evil alignment. It bestows one negative level on any evil creature attempting to wield it. The negative level remains as long as the weapon is in hand and disappears when the weapon is no longer wielded. This negative level never results in actual level loss, bur it cannot be overcome in any way (including restoration spells) while the weapon is wielded. Bows, crossbows, and slings so crafted bestow the holy power upon their ammunition.
Moderate evocation [good]; CL 7th; Craft Magic Arms and Armor, holy smite, creator must be good; Price +2 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** weapon counts as good-aligned for DR. Each damaging hit on an evil creature adds +2d6 untyped damage (not multiplied on a crit). No save, no SR. An evil wielder gains 1 negative level while holding it. Ammunition weapons confer the property. No healing interaction.

## GURPS 4e
chassis Gadget (Breakable -25%, Can Be Stolen -10% = -35%). Extra damage = Innate Attack, Follow-Up +0%, 2d (Executioner precedent: +2d6 = 2d), Accessibility "only vs. evil-aligned targets" -20% by the Hunter's Mark precedent (percentage open), Magical -10%; limitations total -65%, inside the -80% cap. Per-die base cost is "Variable" in the repo index, so no point total is stated. Damage type for the rider: open. Wielder penalty for an evil wielder: the Energy Drained condition while held (engine ruling), same default as Anarchic fork 2.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Radiant (Elemental 45-50).
none keyed to alignment. Radiant (Elemental 45-50) is positive-energy damage (undead x1.5), not an alignment smite; Banefire is element-subtype only.

## NAME COLLISION
Unholy (twin), Anarchic and Axiomatic (same template), Radiant (pool; flavor overlap only), spell holy smite.

## FORKS
1. Holy plus Radiant on one weapon. Default: allowed, riders add (different keys, additive, never multiplicative).
2. Holy and Unholy together. Default: mutually exclusive.
3. RULED by the engine: alignment is read from the 3.5e stat block; an evil wielder takes the Energy Drained condition; the 2d6 ignores worn DR (Rider class).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### ICY BURST
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 226 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Icy Burst: An icy burst weapon functions as a frost weapon that also explodes with frost upon striking a successful critical hit. The frost does not harm the wielder. In addition to the extra damage from the frost ability, an icy burst weapon deals an extra 1d10 points of cold damage on a successful critical hit. If the weapon's critical multiplier is x3, add an extra 2d10 points of cold damage instead, and if the multiplier is x4, add an extra 3d10 points. Bows, crossbows, and slings so crafted bestow the cold energy upon their ammunition. Even if the frost ability is not active, the weapon still deals its extra cold damage on a successful critical hit.
Moderate evocation; CL 10th; Craft Magic Arms and Armor, chill metal or ice storm; Price +2 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** on a confirmed critical hit, extra cold damage by the weapon's multiplier class: x2 = 1d10, x3 = 2d10, x4 = 3d10, applied even when the Frost toggle is off. Not multiplied by the crit (extra dice are not multiplied). Respects cold resistance and immunity. No save, no SR.

## GURPS 4e
chassis Gadget (Breakable -25%, Can Be Stolen -10%); Innate Attack (Burning [Cold]), Follow-Up +0%, Trigger "critical hit only", Magical -10%. Dice: default 1d / 2d / 3d by multiplier class, matching the Flaming Burst default. Trigger percentage and per-die base cost: OPEN, no point total stated.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed +2 = 8,000 gp as a standalone ability that includes the frost half (Freezing at T4 + delta).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Freezing (Elemental 09-16).
Freezing (Elemental 09-16) covers the frost half. Elemental Burst (Elemental 75-80) is a different mechanic (10-ft burst, Reflex half), not a single-target crit rider.

## NAME COLLISION
Elemental Burst (pool, different mechanic); Frost (sibling); SRD Flaming Burst and Shocking Burst (same template).

## FORKS
1. Engine ruling: the weapon's own 3.5e crit multiplier applies; no GURPS conversion is needed.5e multiplier class.
2. Bursts on one weapon: Icy Burst replaces Frost, never stacks with it. Default: not allowed together.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Trigger percentage and per-die base cost: OPEN, no point total stated.


---

### IGNAN
**Weapon property — Magic Item Compendium, PDF p. 37 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
IGNAN
Price: +2 bonus
Property: Weapon
Caster Level: 7th
Aura: Moderate; (DC 18) evocation
Activation: --
An ignan weapon automatically overcomes the damage reduction of any creature that has the water subtype. In addition, the weapon deals an extra 2d6 points of damage against such targets. An ignan weapon also bestows one negative level on any creature that has the water subtype and attempts to wield it. The negative level remains as long as the weapon is in hand and disappears when it is no longer held. This negative level never results in actual level loss, but it cannot be overcome in any way (including restoration spells) while the weapon is wielded.
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, fire subtype.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 7th; Aura: Moderate; (DC 18) evocation; Activation: --; Prerequisites: Craft Magic Arms and Armor, fire subtype.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Keyed to the WATER subtype instead of fire: read every 'fire subtype' in the Aquan text as 'water subtype'. as printed, 2d6 untyped, not multiplied on a crit.

## GURPS 4e
Innate Attack Follow-Up 2d with Accessibility "only vs. the opposed subtype" (percentage OPEN); DR-bypass has no GURPS effect beyond the tag; wielder penalty the Energy Drained condition while held (engine ruling)design intent, same default as the alignment weapons).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Banefire (Elemental 93-96).
Banefire (Elemental 93-96, +2d6 vs a chosen element subtype) gives the 2d6 rider. Delta = the DR bypass and the subtype-wielder negative level. One family with Auran (earth), Ignan (water) and Terran (air), all +2: weapon keyed to the subtype opposed to its element.

## FORKS
shared with the alignment-weapon rulings (GURPS subtype tag, wielder penalty); Aquan and Banefire on one weapon, default not allowed.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- the opposed subtype" (percentage OPEN);


---

### ILLUSION THEFT
**Weapon property — Magic Item Compendium, PDF p. 38 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
ILLUSION THEFT [SYNERGY]
Price: +2 bonus
Property: Weapon
Caster Level: 17th
Aura: Strong; (DC 23) divination
Activation: Standard (command)
Synergy Prerequisite: Illusion bane
An illusion theft weapon functions as an illusion bane weapon (see above). In addition, such a weapon allows you to disrupt opponents' illusions and transfer their protective qualities to yourself. The first illusion spell that this weapon dispels with its illusion bane property is automatically stored within it. This ability functions like the spell storing property (DMG 225), with the following exceptions. It must be an illusion spell, but it need not be 3rd level or lower. A spell cannot be cast into the weapon; it can store only a spell that it has actually dispelled through the illusion bane ability. An illusion theft weapon need not actually strike a creature to activate the stored spell. The stored spell is preserved as originally cast in every way, except that its duration is effectively arrested at the time you steal it. As soon as the spell is stored, you immediately become aware of its effect and its remaining duration, and you can activate it at any time. You can choose a different target to be affected by the stored spell if you so desire. When the spell is activated, the duration begins passing again as if no time had elapsed. Once a stored illusion spell has been discharged, you cannot activate the weapon's illusion theft property again until you have successfully dispelled another illusion (using the illusion bane property), which is then stored within the weapon.
Prerequisites: Craft Magic Arms and Armor, true seeing, dispel magic.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 17th; Aura: Strong; (DC 23) divination; Activation: Standard (command); Synergy Prerequisite: Illusion bane; Prerequisites: Craft Magic Arms and Armor, true seeing, dispel magic.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
a stolen-effect container that holds one dispelled effect (cost and the duration-pause mechanism OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed +2 = 8,000 gp on top of Illusion Bane.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Reservoir stores a spell cast into it; this steals one).

## FORKS
1. which illusions of a PC or named NPC can be taken (default as printed; the weapon's own CL check against the spell).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- a stolen-effect container that holds one dispelled effect (cost and the duration-pause mechanism OPEN).


---

### IMPEDANCE
**Weapon property — Magic Item Compendium, PDF p. 38 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
IMPEDANCE
Price: +2 bonus
Property: Weapon
Caster Level: 11th
Aura: Moderate; (DC 20) abjuration
Activation: --
An impedance weapon mimics the impeded magic planar trait (DMG 150). When you use it to strike a creature, the target's ability to cast spells or use spell-like abilities is impeded for 1d6 rounds. To cast an impeded spell or use an impeded spell-like ability, the creature must attempt a Spellcraft check, Intelligence check, or Charisma check (whichever one is made with the highest bonus). The DC for this check is 15 + the spell level. If the check succeeds, the effect functions normally; if the check fails, the effect does not function and the spell or the use of the spell-like ability is lost.
Prerequisites: Craft Magic Arms and Armor, antimagic field.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 11th; Aura: Moderate; (DC 20) abjuration; Activation: --; Prerequisites: Craft Magic Arms and Armor, antimagic field.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, every hit, fixed formula DC 15 + spell level.

## GURPS 4e
Affliction on casting (a casting roll penalty or a failure on a Will roll; modifiers OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
Silencing (Condition 31-36: silence 1d4 rounds, Will save) is the nearest; this has no save and a skill check instead.

## FORKS
1. repeated hits: default the duration does not stack, it refreshes.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- modifiers OPEN).


---

### METALLINE
**Weapon property — Magic Item Compendium, PDF p. 39 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
METALLINE
Price: +2 bonus
Property: Weapon
Caster Level: 9th
Aura: Moderate; (DC 19) transmutation
Activation: Standard (command)
When you activate a metalline weapon, you can change its composition to adamantine, alchemical silver, cold iron, or ordinary steel.
Prerequisites: Craft Magic Arms and Armor, fabricate.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 9th; Aura: Moderate; (DC 19) transmutation; Activation: Standard (command); Prerequisites: Craft Magic Arms and Armor, fabricate.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; in GURPS the Armor Divisor or material-DR interactions follow Penetrating Strikes' Armor Divisor (2) (OPEN).

## GURPS 4e
as printed; in GURPS the Armor Divisor or material-DR interactions follow Penetrating Strikes' Armor Divisor (2) (OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Penetrating Strikes (Offensive 85-90).
Penetrating Strikes (Offensive 85-90): counts as magic / silver / cold iron / adamantine / all at T5-T1. Delta = a chosen single material at will, which beats the lower pool tiers.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- in GURPS the Armor Divisor or material-DR interactions follow Penetrating Strikes' Armor Divisor (2) (OPEN).


---

### PARALYTIC BURST
**Weapon property — Magic Item Compendium, PDF p. 40 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
PARALYTIC BURST
Price: +2 bonus
Property: Weapon
Caster Level: 9th
Aura: Moderate; (DC 19) enchantment
Activation: --
Whenever you score a critical hit with this weapon, a wave of green energy washes over the target, paralyzing it for 1 round (Will DC 17 negates). This effect activates even if the target is not normally subject to extra damage from critical hits.
Prerequisites: Craft Magic Arms and Armor, hold monster.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 9th; Aura: Moderate; (DC 19) enchantment; Activation: --; Prerequisites: Craft Magic Arms and Armor, hold monster.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, fixed DC 17.

## GURPS 4e
Affliction (Paralysis), Trigger critical, HT or Will resistance (percentages OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Dazing (Condition 17-24).
Dazing (Condition 17-24) is a 1/encounter daze on a Will save; this is crit-triggered paralysis.

## FORKS
1. immunity: paralysis-immune creatures are unaffected.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Affliction (Paralysis), Trigger critical, HT or Will resistance (percentages OPEN).


---

### PARRYING
**Weapon property — Magic Item Compendium, PDF p. 41 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
PARRYING
Price: +2 bonus
Property: Weapon
Caster Level: 15th
Aura: Strong; (DC 22) enchantment
Activation: --
A parrying weapon allows you to discern events an instant into the future, granting you a +1 insight bonus to AC. The weapon makes you so adept at parrying that it grants you a +1 insight bonus on saving throws. The bonuses are granted whenever you hold the weapon, even if you are flat-footed.
Prerequisites: Craft Magic Arms and Armor, divine protection (SC 70) or defensive precognition (EPH 124).
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 15th; Aura: Strong; (DC 22) enchantment; Activation: --; Prerequisites: Craft Magic Arms and Armor, divine protection (SC 70) or defensive precognition (EPH 124).; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
Defense Bonus +1 and +1 to resist (Will and HT) while held (Gadget).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Warding (Defensive 01-06) + Stalwart (Defensive 13-18).
Warding (Defensive 01-06, AC) and Stalwart (13-18, all saves) at T5-T4 supply +1 each. Delta = the insight bonus type, which stacks with their deflection and resistance bonuses.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### SHOCKING BURST
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 226 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Shocking Burst: A shocking burst weapon functions as a shock weapon that also explodes with electricity upon striking a successful critical hit. The electricity does not harm the wielder. In addition to the extra electricity damage from the shock ability, a shocking burst weapon deals an extra 1d10 points of electricity damage on a successful critical hit. If the weapon's critical multiplier is x3, add an extra 2d10 points of electricity damage instead, and if the multiplier is x4, add an extra 3d10 points. Bows, crossbows, and slings so crafted bestow the electricity energy upon their ammunition. Even if the shock ability is not active, the weapon still deals its extra electricity damage on a successful critical hit.
Moderate evocation; CL 10th; Craft Magic Arms and Armor, call lightning or lightning bolt; Price +2 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** On a confirmed critical hit, +1d10 electricity (x2 weapon), +2d10 (x3), +3d10 (x4). Not multiplied by the crit (implied by the printed ladder; unstated). No action, no save, no SR, instant. Works with the Shock toggle off. Ranged: ammunition carries it. Adds to the Shocking T4 +1d6 on every hit. Procs: no d100 (crit-triggered, not a proc).

## GURPS 4e
Innate Attack (Burning [Lightning]) Follow-Up +0%, triggered on a critical hit; Gadget Breakable -25% + Can Be Stolen -10% = -35%. Crit-only limitation percentage: open (not retrieved). Dice read as-is: 1d10 / 2d10 / 3d10 by the weapon's multiplier class. Resulting points: not computable.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 total = 8,000 gp (inclusive of the Shocking T4 half; do not add Shocking's 2,000 on top).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Shocking (Elemental 17-24).
Shocking (Elemental 17-24) covers the Shock half (T4 +1d6 lightning, GURPS IA Burning [Lightning] Follow-Up). Lethal Focus (Offensive 31-36) is untyped crit dice by tier; Elemental Burst (Elemental 75-80) is a 10-ft Reflex-half crit burst. Gap: crit-only electricity dice on a multiplier ladder (1d10/2d10/3d10), independent of the Shock toggle, is not in any row.

## NAME COLLISION
SRD Shocking Burst vs pool Shocking, Elemental Burst, Stormborn; "Burst" also names the flaming/icy/shocking family.

## FORKS
1. Standalone vs delta: default delta stacked on Shocking T4 (SRD says it "functions as a shock weapon"). 2. Resolved by the engine: the weapon's own 3.5e crit multiplier applies and dice read as-is.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### TERRAN
**Weapon property — Magic Item Compendium, PDF p. 46 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
TERRAN
Price: +2 bonus
Property: Weapon
Caster Level: 7th
Aura: Moderate; (DC 18) evocation
Activation: --
A terran weapon automatically overcomes the damage reduction of any creature that has the air subtype. In addition, the weapon deals an extra 2d6 points of damage against such targets. A terran weapon also bestows one negative level on any creature that has the air subtype and attempts to wield it. The negative level remains as long as the weapon is in hand and disappears when it is no longer held. This negative level never results in actual level loss, but it cannot be overcome in any way (including restoration spells) while the weapon is wielded.
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, earth subtype.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 7th; Aura: Moderate; (DC 18) evocation; Activation: --; Prerequisites: Craft Magic Arms and Armor, earth subtype.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Keyed to the AIR subtype instead of fire: read every 'fire subtype' in the Aquan text as 'air subtype'. as printed, 2d6 untyped, not multiplied on a crit.

## GURPS 4e
Innate Attack Follow-Up 2d with Accessibility "only vs. the opposed subtype" (percentage OPEN); DR-bypass has no GURPS effect beyond the tag; wielder penalty the Energy Drained condition while held (engine ruling)design intent, same default as the alignment weapons).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Banefire (Elemental 93-96).
Banefire (Elemental 93-96, +2d6 vs a chosen element subtype) gives the 2d6 rider. Delta = the DR bypass and the subtype-wielder negative level. One family with Auran (earth), Ignan (water) and Terran (air), all +2: weapon keyed to the subtype opposed to its element.

## FORKS
shared with the alignment-weapon rulings (GURPS subtype tag, wielder penalty); Aquan and Banefire on one weapon, default not allowed.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- the opposed subtype" (percentage OPEN);


---

### TRANSMUTING
**Weapon property — Magic Item Compendium, PDF p. 46 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
TRANSMUTING
Price: +2 bonus
Property: Weapon
Caster Level: 13th
Aura: Strong; (DC 21) transmutation
Activation: --
When you score a successful hit with a transmuting weapon against a creature that has damage reduction, that attack is resolved normally. At the start of your next turn, however, the weapon transforms, taking on the properties required to overcome that creature's damage reduction. Once so changed, the weapon overcomes the designated type of damage reduction for 10 rounds, or until you strike a creature that has a different type of damage reduction. In this case, the weapon transforms in the same manner to overcome that damage reduction instead. If the target has multiple types of damage reduction, the weapon overcomes all of them. If the creature gains a new type of damage reduction after initially being struck (from changing its form, for example), the weapon must change again before it can overcome the new type. A transmuting weapon does not gain any other benefit of the properties it takes on, and it always deals normal damage.
Prerequisites: Craft Magic Arms and Armor, fabricate.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 13th; Aura: Strong; (DC 21) transmutation; Activation: --; Prerequisites: Craft Magic Arms and Armor, fabricate.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
after the first hit the weapon's Armor Divisor or material tag matches the target's DR type for 10 seconds (OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Penetrating Strikes (Offensive 85-90).
Penetrating Strikes (Offensive 85-90) at T1 covers all materials and alignments; Metalline (batch 07) is a chosen material. Delta = automatic adaptation after the first hit.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- after the first hit the weapon's Armor Divisor or material tag matches the target's DR type for 10 seconds (OPEN).


---

### UNHOLY
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 227 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Unholy: An unholy weapon is imbued with unholy power. This power makes the weapon evil-aligned and thus bypasses the corresponding damage reduction. It deals an extra 2d6 points of damage against all of good alignment. It bestows one negative level on any good creature attempting to wield it. The negative level remains as long as the weapon is in hand and disappears when the weapon is no longer wielded. This negative level never results in actual level loss, but it cannot be overcome in any way (including restoration spells) while the weapon is wielded. Bows, crossbows, and slings so crafted bestow the unholy power upon their ammunition.
Moderate evocation [evil]; CL 7th; Craft Magic Arms and Armor, unholy blight, creator must be evil; Price +2 bonus
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** weapon counts as evil-aligned for DR. Each damaging hit on a good creature adds +2d6 untyped damage (not multiplied on a crit). No save, no SR, no d100. A good wielder gains 1 negative level while holding it. Ammunition weapons confer the property. No healing interaction.

## GURPS 4e
identical to Holy with the axis flipped: Gadget (Breakable -25%, Can Be Stolen -10% = -35%); Innate Attack, Follow-Up +0%, 2d (Executioner precedent), Accessibility "only vs. good-aligned targets" -20% (Hunter's Mark precedent, percentage open), Magical -10%. No point total (per-die base cost "Variable"). Good-wielder penalty: the Energy Drained condition while held (engine ruling). GURPS DR is not alignment-typed, so the DR-bypass clause has no GURPS effect beyond the 3.5e tag.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Banefire (Elemental 93-96).
none keyed to alignment. Banefire (Elemental 93-96) keys on element subtype, Radiant and Shadowtouch are energy rows, Penetrating Strikes bypasses material DR only. (The batch agent read this as PARTIAL over Banefire; reconciled to NEW so all four alignment weapons share one verdict and one set of rulings.)

## NAME COLLISION
Holy (twin), Anarchic and Axiomatic (same template), Radiant (flavor overlap), spell unholy blight, Crusader's "Holy Strength" (name only).

## RULINGS
alignment is read from the 3.5e stat block; a good wielder takes the Energy Drained condition; Holy and Unholy are mutually exclusive on one weapon; the 2d6 ignores worn DR (engine Rider class).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### VAMPIRIC
**Weapon property — Magic Item Compendium, PDF p. 46 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
VAMPIRIC
Price: +2 bonus
Property: Melee weapon
Caster Level: 9th
Aura: Moderate; (DC 19) necromancy
Activation: --
A vampiric weapon deals an extra 1d6 points of damage to any living creature it hits, and you heal damage equal to this amount.
Prerequisites: Craft Magic Arms and Armor, vampiric touch.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Melee weapon; Caster Level: 9th; Aura: Moderate; (DC 19) necromancy; Activation: --; Prerequisites: Craft Magic Arms and Armor, vampiric touch.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** +1d6 untyped to living targets, heal equal to the roll (cap 6 per hit); bloodless targets give nothing.

## GURPS 4e
Innate Attack Follow-Up 1d6 plus a Vampiric-style leech of the injury (the pool's Leech row uses Vampiric Attack; costs OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
Leech (Resource 19-24: recover 1/1/2/3/5 HP per hit) is a flat heal with no extra damage; this is damage plus a matching heal (average 3.5, between Leech T3 and T2).

## FORKS
1. healing versus Fatal Wound: default the Registry norm applies: the Vampiric heal is magical healing and ends Fatal Wound stacks like any other (consistent with Crusader after D2 was reversed 2026-10-04).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- costs OPEN).


---

### WOUNDING
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 227 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Wounding: A wounding weapon deals 1 point of Constitution damage from blood loss when it hits a creature. A critical hit does not multiply the Constitution damage. Creatures immune to critical hits (such as plants and constructs) are immune to the Constitution damage dealt by this weapon.
Moderate evocation; CL 10th; Craft Magic Arms and Armor, Mordenkainen's sword; Price +2 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Every hit, 1 Con damage (ability damage, healed by normal ability-damage rules), no save, no SR, not multiplied by a crit. Immune: creatures immune to crits, which covers the Registry's bloodless list (constructs, undead, oozes, elementals) plus plants. No d100: the printed trigger is every hit, not a proc. Fatal Wound interaction: none, no healing is involved.

## GURPS 4e
Follow-Up Affliction (Attribute Penalty: HT), not Fatigue or HP damage. 3.5e 2 Con = 1 HT only if the brief's Str/Dex 2:1 ratio extends to Con (flagged), so one damaging hit is half a point of HT loss and every second hit costs HT -1. Duration, whether it persists until healed, resisting roll, and the Affliction percentage: all open. Gadget -35% (Breakable -25%, Can Be Stolen -10%). Points: not computable. default 2:1 per the brief's Str/Dex rule. 3. Every-hit Con damage is far stronger than the 10% proc rows in the Registry: default SRD-faithful, since the ability is priced +2 and has no proc rate in the source.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Weakening (Condition 37-42).
none that matches. Pool "Wounding" (Offensive 07-12) is flat bonus HP damage; the Fatal Wound family (Part 0) is a stacking HP bleed; Weakening (Condition 37-42) is a short Str penalty; Cursed Wound blocks healing. Gap: persistent Constitution damage on every hit.

## NAME COLLISION
pool "Wounding" (Offensive 07-12), Fatal Wound family, Cursed Wound, SRD Wounding spell effects; keep the three mechanics separate.

## FORKS
1. Every hit vs damage past DR: default only a hit that deals damage past DR (matches proc conventions; the SRD says "hits"). 2. Con-to-HT ratio in

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

## TIER 4 — COMPETENT (levels 5-8)

### ACIDIC BURST
**Weapon property — Magic Item Compendium, PDF p. 29 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
ACIDIC BURST [SYNERGY]
Price: +1 bonus
Property: Weapon
Caster Level: 12th
Aura: Strong; (DC 21) conjuration
Activation: Standard (command) and --
Synergy Prerequisite: Corrosive
An acidic burst weapon functions as a corrosive weapon (see page 31). In addition, the weapon automatically showers an opponent with acid upon a successful critical hit, dealing extra acid damage as set out on the table below. This acid does not harm you or any creature other than the target. This is a continuous effect and requires no activation. Even if the weapon has not been activated to deal the extra 1d6 points of acid damage that comes from the corrosive property, the weapon still deals its extra acid damage on a successful critical hit.
Critical Multiplier / Extra Acid Damage: x2 1d10; x3 2d10; x4 3d10
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, Melf's acid arrow.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 12th; Aura: Strong; (DC 21) conjuration; Activation: Standard (command) and --; Synergy Prerequisite: Corrosive; Prerequisites: Craft Magic Arms and Armor, Melf's acid arrow.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** on a confirmed crit, extra acid damage 1d10 / 2d10 / 3d10 by multiplier class (not multiplied again).

## GURPS 4e
Innate Attack (Corrosion), Follow-Up +0%, Trigger critical, dice default 1d / 2d / 3d.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 on top of Corrosive (printed synergy price).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Corroding (Elemental 25-32).
Corroding (Elemental 25-32) is the acid half. Delta = crit rider only (same shape as DMG Icy Burst).

## FORKS
Engine ruling: the weapon's own 3.5e crit multiplier applies.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### AQUATIC
**Weapon property — Magic Item Compendium, PDF p. 29 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price 2,000 gp (flat))

## SOURCE (verbatim, see packet header for normalization)
```
AQUATIC
Price: +2,000 gp
Property: Weapon
Caster Level: 7th
Aura: Moderate; (DC 18) abjuration
Activation: --
While wielding an aquatic weapon, you do not incur any penalties that would otherwise apply to using the weapon underwater (DMG 92), as though you were affected by a freedom of movement spell.
Prerequisites: Craft Magic Arms and Armor, freedom of movement.
Cost to Create: 1,000 gp, 80 XP, 2 days.

ARCANE MIGHT
Price: +1 bonus
Property: Bows (not crossbows)
Caster Level: 15th
Aura: Strong; (DC 22) transmutation
Activation: Swift (mental)
You can channel the energy of your arcane spells through this bow to make the arrows fired from it more damaging. As a swift action, you can sacrifice a prepared arcane spell from memory (or an unused spell slot if you are a spontaneous arcane caster). Doing so grants a bonus equal to the sacrificed spell's level on the next damage roll you make with the bow that turn.
Prerequisites: Craft Magic Arms and Armor, greater magic weapon.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2,000 gp; Property: Weapon; Caster Level: 7th; Aura: Moderate; (DC 18) abjuration; Activation: --; Prerequisites: Craft Magic Arms and Armor, freedom of movement.; Cost to Create: 1,000 gp, 80 XP, 2 days.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** no penalties from fighting underwater with this weapon.

## GURPS 4e
no underwater combat penalties with this weapon (the specific modifiers are OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed 2,000 gp flat.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Waterborn, Utility 43-48, is water breathing and swim speed, not weapon handling).

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- no underwater combat penalties with this weapon (the specific modifiers are OPEN).


---

### ARCANE MIGHT
**Weapon property — Magic Item Compendium, PDF p. 29 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
ARCANE MIGHT
Price: +1 bonus
Property: Bows (not crossbows)
Caster Level: 15th
Aura: Strong; (DC 22) transmutation
Activation: Swift (mental)
You can channel the energy of your arcane spells through this bow to make the arrows fired from it more damaging. As a swift action, you can sacrifice a prepared arcane spell from memory (or an unused spell slot if you are a spontaneous arcane caster). Doing so grants a bonus equal to the sacrificed spell's level on the next damage roll you make with the bow that turn.
Prerequisites: Craft Magic Arms and Armor, greater magic weapon.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Bows (not crossbows); Caster Level: 15th; Aura: Strong; (DC 22) transmutation; Activation: Swift (mental); Prerequisites: Craft Magic Arms and Armor, greater magic weapon.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; bonus equals sacrificed spell level; one use per swift action.

## GURPS 4e
the campaign's casting resource is Energy Reserve; sacrifice ER for a damage bonus. The ER-per-spell-level exchange is OPEN (the translator rule 1 ER = about 5 mana is a rough guide, unverified here).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Reservoir stores a spell; Cost Reduction trades cost).

## FORKS
1. cap per round (default one swift activation per round, per the swift action).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- The ER-per-spell-level exchange is OPEN (the translator rule 1 ER = about 5 mana is a rough guide, unverified here).


---

### BANE
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 225 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Bane: A bane weapon excels at attacking one type or subtype of creature. Against its designated foe, its effective enhancement bonus is +2 betrer than its normal enhancement bonus (50a +1 longsword isa +3 longsword against its foe), It deals an extra 2d6 points of damage against the foe. Bows, crossbows, and slings so crafted bestow the bane quality upon their ammunition. To randomly determine a weapon's designated foe, roll on the following table.
(designated-foe d% table: Aberrations 01-05, Animals 06-09, Constructs 10-16, Dragons, Elementals 23-27, Fey 28-32, Giants 33-39, Humanoids (aquatic 40, dwarf 41-42, elf 43-44, gnoll 45, gnome 46, goblinoid 47-49, halfling 50, human 51-54, reptilian 55-57, orc 58-60), Magical beasts 61-65, Monstrous humanoids 66-70, Oozes 71-72, Outsiders (air 73, chaotic 74-76, earth 77, evil 78-80, fire 81, good 82-84, lawful 85-87, water 88), Plants 89-90, Undead 91-98, Vermin 99-100)
Moderate conjuration; CL 8th; Craft Magic Arms and Armor, summon monster I: Price +1 bonus,
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** The weapon names one designated foe (a creature type or subtype from the SRD table). Against that foe: +2 to the weapon's effective enhancement bonus (attack and damage, and for overcoming DR), plus the 2d6 rider (Banefire T4/T5 value, not stacked with Banefire; fork 2). No save, no SR, no DC. Ranged weapons pass it to ammunition. Bleed and healing: no interaction.

## GURPS 4e
Chassis Gadget (Breakable DR 6 -25%, Can Be Stolen -10% = -35%). Rider: reuse Banefire's IA (Bane) line, Follow-Up, 2d by the Executioner precedent (3.5e +2d6 = 2d), Accessibility "only vs. designated type" -20% by Hunter's Mark precedent (open). The +2 effective enhancement = Weapon Bond +2 to weapon skill (Striking row precedent, +2 = T3 value), same Accessibility. Magical -10%. Weapon Bond cost is not in gurps_trait_index; open. Totals not stated.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 bonus-equivalent = 2,000 gp (bonus-squared x 2,000; matches printed +1).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Banefire (Elemental 93-96).
Banefire (Elemental pool 93-96): +2d6/+2d6/+3d6/+4d6/+5d6 vs creatures with a chosen element subtype; GURPS IA (Bane). Gap: Banefire keys only to element subtype and carries no attack/damage enhancement bump; SRD Bane keys to any creature type or subtype and adds +2 effective enhancement.

## NAME COLLISION
Banefire (pool Elemental 93-96); SRD "Bane" spell-descriptor and the bane special-ability family (Bane weapon in SRD specific weapons, e.g. Dwarven Thrower is separate); GURPS "IA (Bane)" shorthand in the pool; SRD Disruption (undead-specific, queued here).

## FORKS
1. Foe selection: SRD gives the d% table only for random generation. Recommended default: crafter chooses the foe at creation; the table is used only for loot rolls.
2. Bane and Banefire on one weapon. Recommended default: not allowed together (one "versus" affix per weapon); if allowed, the two 2d6 riders add (additive, never multiplicative) only against a creature matching both.
3. Does the +2 effective enhancement raise the weapon's enhancement for Defending allocation or pool Striking? Recommended default: no, it applies only to the strike against the designated foe.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### BERSERKER
**Weapon property — Magic Item Compendium, PDF p. 30 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
BERSERKER
Price: +1 bonus
Property: Two-handed melee weapon
Caster Level: 7th
Aura: Moderate; (DC 18) enchantment
Activation: --
In your hands, a berserker weapon deals an extra 1d8 points of damage on any successful attack while you are raging.
Prerequisites: Craft Magic Arms and Armor, rage.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Two-handed melee weapon; Caster Level: 7th; Aura: Moderate; (DC 18) enchantment; Activation: --; Prerequisites: Craft Magic Arms and Armor, rage.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** +1d8 untyped on any hit while raging; requires rage.

## GURPS 4e
Innate Attack Follow-Up 1d8 (dice read as-is) with Accessibility "while berserk" (percentage OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
NAME COLLISION. The pool row "Berserker" (Offensive 61-66) is +1/+1/+2/+3/+4 damage with -AC while attacking and needs no rage; this is a different mechanic. Names stay and never merge (Fatal Wound precedent); a collision note is the only change.

## FORKS
1. GURPS rage stand-in (default: while under the Berserk disadvantage or a campaign rage trait).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Innate Attack Follow-Up 1d8 (dice read as-is) with Accessibility "while berserk" (percentage OPEN).


---

### BINDING
**Weapon property — Magic Item Compendium, PDF p. 30 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
BINDING
Price: +1 bonus
Property: Weapon
Caster Level: 10th
Aura: Moderate; (DC 20) abjuration
Activation: Swift (command)
When you activate a binding weapon, the next successful attack you make with it before the end of your turn prevents the target from using any form of extradimensional travel, as the dimensional anchor spell. The binding property functions two times per day, and the effect lasts for 10 minutes.
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, dimensional anchor.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 10th; Aura: Moderate; (DC 20) abjuration; Activation: Swift (command); Prerequisites: Craft Magic Arms and Armor, dimensional anchor.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; no save printed (dimensional anchor allows none to the target beyond SR).

## GURPS 4e
prevent Warp / Teleport / plane travel for 10 minutes on the target (mechanism; cost OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
NAME COLLISION. The pool "Binding" (Condition 09-16) is entangle for 1 round.

## FORKS
1. spell resistance (default: SR applies as dimensional anchor does).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- cost OPEN).


---

### BLESSED
**Weapon property — Magic Item Compendium, PDF p. 30 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
BLESSED
Price: +1 bonus
Property: Weapon
Caster Level: 5th
Aura: Faint; (DC 17) transmutation
Activation: -- and swift (command)
A blessed weapon is treated as good-aligned for the purpose of overcoming damage reduction. This effect is continuous and requires no activation. In addition, three times per day you can activate a blessed weapon to automatically confirm all critical threats against evil foes for 1 round (as if the weapon were affected by the bless weapon spell). Other effects related to threatening or confirming critical hits (such as the keen edge spell or the vorpal weapon property) don't confer an additional benefit on a weapon that has this property.
Prerequisites: Craft Magic Arms and Armor, bless weapon.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 5th; Aura: Faint; (DC 17) transmutation; Activation: -- and swift (command); Prerequisites: Craft Magic Arms and Armor, bless weapon.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
no alignment axis; use the 3.5e tag for the DR rule (no GURPS effect) and "criticals vs evil confirm automatically" as a trigger usable 3/day.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none; shares the good-alignment tag with DMG Holy (see that file for the alignment rulings).

## FORKS
shared alignment-tag ruling.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### BLOODFEEDING
**Weapon property — Magic Item Compendium, PDF p. 30 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
BLOODFEEDING
Price: +1 bonus
Property: Melee weapon
Caster Level: 7th
Aura: Moderate; (DC 18) necromancy
Activation: -- and free (command)
Every time a bloodfeeding weapon deals damage to a living creature, it gains 1 "blood point," which it can store for up to 1 hour. The weapon can store a maximum of 10 blood points. This effect is continuous and requires no activation. When you deal damage to a creature while wielding a bloodfeeding weapon, you can activate the weapon to spend up to 5 stored blood points. Each blood point you spend in this way deals an extra 2 points of damage to that creature. The weapon doesn't gain any blood points from a strike on which you use this ability.
Prerequisites: Craft Magic Arms and Armor, vampiric touch.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 7th; Aura: Moderate; (DC 18) necromancy; Activation: -- and free (command); Prerequisites: Craft Magic Arms and Armor, vampiric touch.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed. Caps stated: 10 stored, 5 spent per strike (+10 damage maximum), 1 hour storage. Flat-source: the +2 per point never scales. Bloodless targets (constructs, undead, oozes, elementals) grant no points.

## GURPS 4e
Innate Attack Follow-Up, +2 damage per point spent (1 point = +2 in GURPS damage, defaults to +1 per point at the 2:1 conversion, OPEN), Trigger "spend stored points".

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Leech and Bloodprice are different). It is an accumulator, so the stacking doctrine applies: additive, linear.

## FORKS
1. conversion of +2 per point to GURPS (default +1 per point). 2. points decay after 1 hour (as printed).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Innate Attack Follow-Up, +2 damage per point spent (1 point = +2 in GURPS damage, defaults to +1 per point at the 2:1 conversion, OPEN), Trigger "spend stored points".


---

### BLOODSTONE
**Weapon property — Magic Item Compendium, PDF p. 30 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
BLOODSTONE
Price: +1 bonus
Property: Melee weapon
Caster Level: 10th
Aura: Moderate; (DC 20) necromancy
Activation: Free (command)
A bloodstone weapon can store and cast a vampiric touch spell against a creature it strikes, just as if it were a spell storing weapon (DMG 225). Any such spell cast from a bloodstone weapon is automatically empowered (as if by the Empower Spell feat). A bloodstone weapon can store no more than one such spell at any time, and it cannot store a spell other than vampiric touch.
Prerequisites: Craft Magic Arms and Armor, Empower Spell, vampiric touch.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 10th; Aura: Moderate; (DC 20) necromancy; Activation: Free (command); Prerequisites: Craft Magic Arms and Armor, Empower Spell, vampiric touch.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, CL of the weapon (10th).

## GURPS 4e
stored attack, Follow-Up, the stored spell's damage empowered x1.5 (rounding OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Reservoir (Resource 49-54).
Reservoir (Resource 49-54) stores a spell; DMG Spell Storing (see that file) is the delivery pattern. Delta = fixed spell, empowered.

## FORKS
1. shares the Spell Storing rulings.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- stored attack, Follow-Up, the stored spell's damage empowered x1.5 (rounding OPEN).


---

### BRASH
**Weapon property — Magic Item Compendium, PDF p. 31 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
BRASH
Price: +1 bonus
Property: Melee weapon
Caster Level: 5th
Aura: Faint; (DC 17) abjuration
Activation: --
If you enter a rage while wielding a brash weapon, the rage lasts for an extra 3 rounds. In addition, while raging and wielding a brash weapon, you gain immunity to fear effects.
Prerequisites: Craft Magic Arms and Armor, remove fear.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 5th; Aura: Faint; (DC 17) abjuration; Activation: --; Prerequisites: Craft Magic Arms and Armor, remove fear.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed (class-gated by rage).

## GURPS 4e
extend the campaign rage by 3 turns (3 seconds each; exact extension OPEN) and Fearlessness while raging.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none.

## FORKS
GURPS rage stand-in as for Berserker.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- exact extension OPEN) and Fearlessness while raging.


---

### BRUTAL SURGE
**Weapon property — Magic Item Compendium, PDF p. 31 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
BRUTAL SURGE
Price: +1 bonus
Property: Melee weapon
Caster Level: 11th
Aura: Moderate; (DC 20) evocation
Activation: Swift (command)
After a successful melee attack with a brutal surge weapon, you can command the weapon to initiate a bull rush attempt against the target of the attack in addition to dealing its normal damage. This attempt does not provoke attacks of opportunity and is resolved using your size, Strength, and other relevant characteristics. If you wield a brutal surge weapon in two hands, you gain a +2 bonus on the opposed Strength check. If successful, the bull rush pushes the affected creature back the greatest possible distance allowed by the result of the opposed check, but you do not move along with the target. Movement caused by this bull rush attempt provokes attacks of opportunity from other creatures normally, but you cannot make an attack of opportunity against the affected creature. The brutal surge property is usable a number of times per day equal to 1 + your Con bonus (if any). Once you activate this property, it can't be activated by any other creature until the following day.
Prerequisites: Craft Magic Arms and Armor, Bigby's forceful hand.
Cost to Create: Varies.


CHANGELING
Price: +2,000 gp
Property: Spear, shortspear, or longspear
Caster Level: 5th
Aura: Faint; (DC 17) transmutation
Activation: Swift (command)
A changeling weapon allows you to choose its length and appearance each time you attack with it. Once per round, by speaking the appropriate command word, you can change the weapon into a spear, a shortspear, or a longspear sized appropriately for you. As part of the same action, you can make its haft and head appear to be composed of any wood, stone, metal, or combination thereof that you want, and add any decorative flourishes desired, though the spear's actual composition does not change.
Prerequisites: Craft Magic Arms and Armor, shrink item.
Cost to Create: 1,000 gp, 80 XP, 2 days.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 11th; Aura: Moderate; (DC 20) evocation; Activation: Swift (command); Prerequisites: Craft Magic Arms and Armor, Bigby's forceful hand.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; this is a scaling effect by wielder Str and Con, stated explicitly, not flat-source.

## GURPS 4e
Knockback-style push resolved by a Quick Contest of ST; uses per day 1 + HT bonus (stand-in for Con bonus, OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Knockback (Condition 49-54).
Knockback (Condition 49-54) pushes 5-20 ft on a Fortitude save; this uses an opposed Strength check and a no-move push. Delta = the opposed-check bull rush and the daily-use rule.

## FORKS
1. the attunement rule ("cannot be activated by another creature until the following day"), default keep as printed.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- uses per day 1 + HT bonus (stand-in for Con bonus, OPEN).


---

### CHANGELING
**Weapon property — Magic Item Compendium, PDF p. 32 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price 2,000 gp (flat))

## SOURCE (verbatim, see packet header for normalization)
```
CHANGELING
Price: +2,000 gp
Property: Spear, shortspear, or longspear
Caster Level: 5th
Aura: Faint; (DC 17) transmutation
Activation: Swift (command)
A changeling weapon allows you to choose its length and appearance each time you attack with it. Once per round, by speaking the appropriate command word, you can change the weapon into a spear, a shortspear, or a longspear sized appropriately for you. As part of the same action, you can make its haft and head appear to be composed of any wood, stone, metal, or combination thereof that you want, and add any decorative flourishes desired, though the spear's actual composition does not change.
Prerequisites: Craft Magic Arms and Armor, shrink item.
Cost to Create: 1,000 gp, 80 XP, 2 days.
```

## D&D 3.5e
**Printed header:** Price: +2,000 gp; Property: Spear, shortspear, or longspear; Caster Level: 5th; Aura: Faint; (DC 17) transmutation; Activation: Swift (command); Prerequisites: Craft Magic Arms and Armor, shrink item.; Cost to Create: 1,000 gp, 80 XP, 2 days.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
Morph (cosmetic) already used by the pool row, plus switching reach and damage profile among three weapon types; cost OPEN.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed 2,000 gp flat.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Chameleon (Utility 91-96).
Chameleon (Utility 91-96) covers appearance change. Delta = the resize among the three spear types.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- cost OPEN.


---

### CHARGEBREAKER
**Weapon property — Magic Item Compendium, PDF p. 32 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
CHARGEBREAKER
Price: +1 bonus
Property: Melee weapon
Caster Level: 5th
Aura: Faint; (DC 17) enchantment
Activation: --
Any charging creature hit by a chargebreaker weapon must succeed on a DC 14 Fortitude save or be knocked prone.
Prerequisites: Craft Magic Arms and Armor, daze monster.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 5th; Aura: Faint; (DC 17) enchantment; Activation: --; Prerequisites: Craft Magic Arms and Armor, daze monster.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; fixed DC 14 (flat-source), no daily limit, passive.

## GURPS 4e
a HT roll or the target falls down (Knockdown-style effect; the modifier OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none.

## FORKS
1. does it need damage past DR to trigger (default yes, a hit that deals damage).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- the modifier OPEN).


---

### DEFENDING
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 225 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Defending: A defending weapon allows the wielder to transfer some or all of the sword's enhancement bonus to his AC as a bonus that stacks with all others. As a free action, the wielder chooses how to allocate the weapon's enhancement bonus at the start of his turn before using the weapon, and the effect to AC lasts until his next turn.
Moderate abjuration; CL 8th; Craft Magic Arms and Armor, shield or shield of faith: Price +1 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** At the start of the wielder's turn, as a free action, the wielder moves any 0..N points of the weapon's enhancement bonus from the weapon to AC (N = base enhancement bonus; special-ability bonus-equivalents never count). The weapon's attack and damage enhancement drops by the same amount; the AC bonus lasts until the wielder's next turn. No d100, no save, no SR, no DC. No Fatal Wound interaction (no healing).

## GURPS 4e
Chassis Gadget (Breakable DR 6 -25%, Can Be Stolen -10% = -35%). Follow the Warding precedent: moving n points reduces the weapon's Weapon Bond by n (Striking row precedent) and grants Damage Resistance +n (5/level in gurps_trait_index; 5 x 0.65 = 3.25 per level after the Gadget limitations), set at the start of the wielder's turn and held until the next. Weapon Bond cost is not in the index; net zero-sum totals are open. Magical -10% not applied (defensive, not an attack).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 bonus-equivalent = 2,000 gp (bonus-squared x 2,000; matches printed +1).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Warding (Defensive 01-06).
Warding (Defensive 01-06): AC +1/+1/+2/+3/+4 (deflection); GURPS DR +n (Gadget). Also Shield Wall (49-54, shield-type AC). Gap: Warding is a free, permanent AC bonus; Defending is a zero-sum reallocation of the weapon's own enhancement bonus, chosen each turn.

## NAME COLLISION
Warding (Defensive 01-06); Shield Wall (Defensive 49-54); SRD "defending" is also a creature-trait word in some stat blocks; SRD Defending is the only weapon property by this name; Savage Blow (Offensive 43-48, a tradeoff of Power Attack, different mechanic).

## FORKS
1. What counts as the "enhancement bonus". Recommended default: only the base +N; pool Striking bonuses and other bonus-equivalent affixes do not count.
2. GURPS mapping: DR (Warding precedent) or Defense Bonus (Aegis precedent). Recommended default: DR, per Warding.
3. Does the transferred amount also reduce damage, not only attack? Recommended default: yes (attack and damage), since the SRD calls it a transfer of the enhancement bonus.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### DEFENSIVE SURGE
**Weapon property — Magic Item Compendium, PDF p. 33 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
DEFENSIVE SURGE
Price: +1 bonus
Property: Melee weapon
Caster Level: 5th
Aura: Faint; (DC 17) abjuration
Activation: Swift (command)
After a successful melee attack with a defensive surge weapon in any round in which you use the Combat Expertise feat or fight defensively, you can activate the weapon and gain an additional +2 bonus to Armor Class until the start of your next turn. This ability is usable a number of times per day equal to 1 + your Int bonus (if any). Once you activate this property, it can't be activated by any other creature until the following day.
Prerequisites: Craft Magic Arms and Armor, shield.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 5th; Aura: Faint; (DC 17) abjuration; Activation: Swift (command); Prerequisites: Craft Magic Arms and Armor, shield.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed. This scales with Int bonus for daily uses (stated).

## GURPS 4e
+1 to Defense Bonus (+2 AC at roughly 1 DB) until the wielder's next turn, trigger "after a hit while on All-Out/Defensive attack posture" (OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
nearest Warding (Defensive 01-06, always-on deflection AC) and Aegis; neither is conditional or limited-use.

## FORKS
1. GURPS stand-in for Combat Expertise (default Defensive Attack).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- +1 to Defense Bonus (+2 AC at roughly 1 DB) until the wielder's next turn, trigger "after a hit while on All-Out/Defensive attack posture" (OPEN).


---

### DESICCATING
**Weapon property — Magic Item Compendium, PDF p. 33 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
DESICCATING
Price: +1 bonus
Property: Weapon
Caster Level: 5th
Aura: Moderate; (DC 19) necromancy
Activation: --
A desiccating weapon destroys the water in a living creature that it strikes, dealing an extra 1d4 points of damage (or an extra 1d8 points against plants and against elementals that have the water subtype).
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, desiccating bubble (SC 63).
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 5th; Aura: Moderate; (DC 19) necromancy; Activation: --; Prerequisites: Craft Magic Arms and Armor, desiccating bubble (SC 63).; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** +1d4 untyped on a hit (+1d8 vs plants and water elementals), not multiplied on a crit; bloodless targets that have no water (constructs, undead) take none.

## GURPS 4e
Innate Attack Follow-Up 1d4 (1d8 for the vulnerable targets; dice read as-is).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Venomous is poison; Shadowtouch is negative energy).

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### DESICCATING BURST
**Weapon property — Magic Item Compendium, PDF p. 33 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
DESICCATING BURST [SYNERGY]
Price: +1 bonus
Property: Weapon
Caster Level: 12th
Aura: Strong; (DC 21) necromancy
Activation: --
Synergy Prerequisite: Desiccating
A desiccating burst weapon functions as a desiccating weapon (see above). In addition, the weapon explodes with a dehydrating blast on a successful critical hit, dealing extra damage as set out in the table below. (This effect activates even if the target is not normally vulnerable to extra damage from critical hits.) The amount of damage is determined by the weapon's critical multiplier and is doubled against plants and against elementals that have the water subtype. This burst does not harm you or any creature other than the target. This is a continuous effect and requires no activation. Even if the weapon has not been activated to deal extra damage because of the desiccating property, the weapon still deals its extra damage on a successful critical hit.
Critical Multiplier / Extra Damage / Plant-Elemental Damage: x2 1d8 2d8; x3 2d8 4d8; x4 3d8 6d8
In addition, the critical hit renders the struck creature fatigued for 8 hours or until it consumes at least 1 gallon of water or some other rehydrating liquid.
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, horrid wilting.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 12th; Aura: Strong; (DC 21) necromancy; Activation: --; Synergy Prerequisite: Desiccating; Prerequisites: Craft Magic Arms and Armor, horrid wilting.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; fatigue has no save printed (flagged).

## GURPS 4e
Innate Attack Follow-Up, Trigger critical, 1d / 2d / 3d (default) doubled vs plants and water elementals, plus the Fatigue effect (FP loss, OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 over Desiccating.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Desiccating (MIC).
none for the burst; Desiccating (above) is the base. Delta = crit rider plus fatigue.

## FORKS
1. the printed fatigue allows no save.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Innate Attack Follow-Up, Trigger critical, 1d / 2d / 3d (default) doubled vs plants and water elementals, plus the Fatigue effect (FP loss, OPEN).


---

### DISLOCATOR
**Weapon property — Magic Item Compendium, PDF p. 33 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
DISLOCATOR
Price: +1 bonus
Property: Weapon
Caster Level: 12th
Aura: Strong; (DC 21) conjuration
Activation: Swift (mental)
When you activate a dislocator weapon, the next successful attack you make before the end of your turn causes your target to be teleported up to 10 feet in any direction you choose (Will DC 17 negates). You can't teleport a target into an occupied space (such an attempt automatically fails and wastes the effect).
Projectile weapons bestow this property on their ammunition.
A dislocator weapon functions three times per day.
Prerequisites: Craft Magic Arms and Armor, teleport.
Cost to Create: Varies.


DISLOCATOR, GREAT [SYNERGY]
Price: +1 bonus
Synergy Prerequisite: Dislocator
This property functions as a dislocator weapon (see above), except the target can be teleported up to 30 feet in any direction (Will DC 20 negates).
Prerequisites: Craft Magic Arms and Armor, greater teleport.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 12th; Aura: Strong; (DC 21) conjuration; Activation: Swift (mental); Synergy Prerequisite: Dislocator; Prerequisites: Craft Magic Arms and Armor, teleport.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; fixed DCs 17 and 20 (flat-source). Two rungs because the source prints two properties; Great needs Dislocator as a synergy prerequisite.

## GURPS 4e
Teleport the target (Affliction-style with a Will resistance roll, 3/day; cost OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 and +1 (the Great adds +1 on top, printed).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Knockback (Condition 49-54).
Knockback (Condition 49-54) pushes; this teleports. Phasewalk is the wielder's own teleport.

## FORKS
1. does the 10-ft and 30-ft teleport provoke or carry the target into hazards (default yes, wielder's choice of destination, no safe-landing guarantee).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- cost OPEN).


---

### DISLOCATOR, GREAT
**Weapon property — Magic Item Compendium, PDF p. 34 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
DISLOCATOR, GREAT [SYNERGY]
Price: +1 bonus
Synergy Prerequisite: Dislocator
This property functions as a dislocator weapon (see above), except the target can be teleported up to 30 feet in any direction (Will DC 20 negates).
Prerequisites: Craft Magic Arms and Armor, greater teleport.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Synergy Prerequisite: Dislocator; Prerequisites: Craft Magic Arms and Armor, greater teleport.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Great rung only: the target is teleported up to 30 feet (Will DC 20 negates) instead of 10 feet (DC 17); synergy prerequisite Dislocator; +1 bonus on top, as printed. as printed; fixed DCs 17 and 20 (flat-source). Two rungs because the source prints two properties; Great needs Dislocator as a synergy prerequisite.

## GURPS 4e
Teleport the target (Affliction-style with a Will resistance roll, 3/day; cost OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 and +1 (the Great adds +1 on top, printed).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Knockback (Condition 49-54).
Knockback (Condition 49-54) pushes; this teleports. Phasewalk is the wielder's own teleport.

## FORKS
1. does the 10-ft and 30-ft teleport provoke or carry the target into hazards (default yes, wielder's choice of destination, no safe-landing guarantee).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- cost OPEN).


---

### DISTANCE
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 225 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Distance: This property can only be placed on a ranged weapon. A weapon of distance has double the range increment of other weapons of its kind.
Moderate divination; CL 6th; Craft Magic Arms and Armor, clairaudience/clairvoyance; Price +1 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Ranged weapons only. The weapon's range increment is doubled (a 100-ft bow is 200 ft). Range penalty per increment is unchanged; the maximum number of increments is the weapon's normal one (PHB rule, not in the fetched ability text, so treat the maximum range as scaling with the doubled increment). No save, no SR, no DC, no action. No Fatal Wound interaction.

## GURPS 4e
Chassis: the launcher is the Gadget (Breakable DR 6 -25%, Can Be Stolen -10% = -35%). Mechanism: the weapon's 1/2D and Max are doubled. The nearest printed trait is the Increased Range enhancement, +10%/level in gurps_trait_index, but the index does not print what one level multiplies (whether one level doubles range is not verified); so the level count and total are OPEN. Magical -10% not applied (no attack). No d100.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 bonus-equivalent = 2,000 gp (bonus-squared x 2,000; matches printed +1).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none. Siege (aspect table 24E) gives a melee attack range but is an aspect, not an affix; Throwing (SRD, queued) gives a melee weapon a range increment; gap: no pool row doubles a range increment.

## NAME COLLISION
SRD Distance (identical); SRD Throwing (melee gains a 10 ft increment) and Seeking (ranged only), both queued; spell clairaudience/clairvoyance (prerequisite only); aspect Siege (24E).

## FORKS
1. Do thrown weapons count as "ranged weapons"? Recommended default: yes, any weapon with a range increment (thrown or launched); Throwing-crafted melee weapons also qualify.
2. GURPS level size of Increased Range. Recommended default: one level doubles 1/2D and Max (+10%), verified against the Basic Set before ratification (number open).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- so the level count and total are OPEN.


---

### DIVINE WRATH
**Weapon property — Magic Item Compendium, PDF p. 34 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
DIVINE WRATH
Price: +1 bonus
Property: Weapon
Caster Level: 13th
Aura: Strong; (DC 21) evocation
Activation: Swift (mental)
Divine wrath weapons are especially prized by paladins and clerics of Heironeous. Whenever you hold such a weapon in your hand, you can expend a turn undead attempt to imbue it with divine power for 1 round. If your next successful attack with it hits an undead target, the weapon deals an extra 1d6 points of damage per point of Charisma bonus you possess (minimum 1d6).
Prerequisites: Craft Magic Arms and Armor, searing light, turn undead, good alignment.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 13th; Aura: Strong; (DC 21) evocation; Activation: Swift (mental); Prerequisites: Craft Magic Arms and Armor, searing light, turn undead, good alignment.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; this SCALES with Cha bonus and costs a class resource (turn undead use), both stated.

## GURPS 4e
Innate Attack Follow-Up, +1d per point of Will-based Cha stand-in, Trigger "spend a Turn Undead / True Faith use" (stand-in and costs OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Turn Mastery (Skill/Class 43-48).
Turn Mastery (Skill/Class 43-48) modifies turning damage; nothing delivers turning as weapon damage. Related to DMG Disruption (destroys undead).

## FORKS
1. no cap printed; default cap +5d6 (Cha bonus 5), design intent.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Innate Attack Follow-Up, +1d per point of Will-based Cha stand-in, Trigger "spend a Turn Undead / True Faith use" (stand-in and costs OPEN).


---

### DRAGONDOOM
**Weapon property — Magic Item Compendium, PDF p. 34 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
DRAGONDOOM
Price: +1 bonus
Property: Melee weapon
Caster Level: 7th
Aura: Moderate; (DC 18) transmutation
Activation: Swift (command)
When wielding a dragondoom weapon, you can choose to deliver a smite attack against a Large or larger creature of the dragon type up to three times each day. For every size category of the dragon larger than Medium, the smite attack deals an extra 1d6 points of damage (+1d6 against a Large dragon, +2d6 against Huge, +3d6 against Gargantuan, and +4d6 against Colossal). You must declare the smite attack before you make your attack roll. If the attack misses (or the creature you strike is not of the dragon type), the smite is wasted.
Prerequisites: Craft Magic Arms and Armor, fell the greatest foe (SC 90).
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 7th; Aura: Moderate; (DC 18) transmutation; Activation: Swift (command); Prerequisites: Craft Magic Arms and Armor, fell the greatest foe (SC 90).; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, cap +4d6, 3/day.

## GURPS 4e
Innate Attack Follow-Up by size category (1d6 / 2d6 / 3d6 / 4d6 for Large, Huge, Gargantuan, Colossal; dice read as-is), Limited Use 3/day.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
Banefire is element-subtype only; Hunter's Mark is the closest bonus-vs-target row.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### DRAGONHUNTER
**Weapon property — Magic Item Compendium, PDF p. 34 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
DRAGONHUNTER
Price: +1 bonus
Property: Projectile weapon
Caster Level: 9th
Aura: Moderate; (DC 19) transmutation, necromancy
Activation: --
A creature of the dragon type that is hit by a projectile fired from this weapon takes 1 point of Strength damage in addition to the normal damage from the weapon. In addition, the weapon's critical multiplier increases by 1 if the target is a dragon. For example, a critical hit from a dragonhunter longbow has a x4 damage multiplier (instead of the normal x3) against a dragon, so such a creature would take four times normal damage (but still only 1 point of Strength damage) with a critical hit.


Other effects related to threatening or confirming critical hits (such as keen edge or bless weapon spells) don't function when placed on a weapon that has this property.
Prerequisites: Craft Magic Arms and Armor, keen edge, ray of enfeeblement.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Projectile weapon; Caster Level: 9th; Aura: Moderate; (DC 19) transmutation, necromancy; Activation: --; Prerequisites: Craft Magic Arms and Armor, keen edge, ray of enfeeblement.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
1 point of ST damage to the target (a lasting ST reduction; recovery rule OPEN) and +1 to the weapon's multiplier class vs dragons.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
Weakening (Condition 37-42: -1/-1/-2/-3/-4 Str for 1d4 rounds, Fort save) is the nearest; this has no save and is permanent-style ability damage on a type.

## FORKS
1. conflict with Keen Edge (the printed text forbids it), default the two cannot share a weapon.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- recovery rule OPEN) and +1 to the weapon's multiplier class vs dragons.


---

### EAGER
**Weapon property — Magic Item Compendium, PDF p. 35 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
EAGER
Price: +1 bonus
Property: Melee weapon
Caster Level: 9th
Aura: Moderate; (DC 19) evocation
Activation: --
An eager weapon can be drawn as a free action. While wielding it, you gain a +2 bonus on initiative checks and a +2 bonus on damage rolls made during a surprise round and the first round of combat.
Prerequisites: Craft Magic Arms and Armor, cat's grace.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 9th; Aura: Moderate; (DC 19) evocation; Activation: --; Prerequisites: Craft Magic Arms and Armor, cat's grace.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
Combat Reflexes-style +2 to initiative-equivalent (Predator's Instinct uses Combat Reflexes), Quick Draw for free, +2 damage opening round (OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Predator's Instinct (Offensive 73-78).
Predator's Instinct (Offensive 73-78): +1/+2/+2/+3/+4 initiative, +1 attack first round at T2+. The +2 initiative matches T4-T3. Delta = free-action draw and +2 damage in the opening rounds.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Combat Reflexes-style +2 to initiative-equivalent (Predator's Instinct uses Combat Reflexes), Quick Draw for free, +2 damage opening round (OPEN).


---

### ENERGY SURGE
**Weapon property — Magic Item Compendium, PDF p. 35 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
ENERGY SURGE [SYNERGY]
Price: +1 bonus
Property: Melee weapon
Caster Level: 5th
Aura: Faint; (DC 17) evocation
Activation: Swift (command)
Synergy Prerequisite: Corrosive, flaming, frost, or shock
An energy surge weapon functions as a weapon of the prerequisite type (corrosive, flaming, frost, or shock). In addition, on a successful melee attack with an energy surge weapon, you can command it to expel a blast of energy, of the same type as the prerequisite property, which deals an extra 3d6 points of damage to the target of the attack. The synergy prerequisite property need not be active to activate the energy surge property. This ability is usable a number of times per day equal to 1 + your Con bonus (if any). Once you activate this property, it can't be activated by any other creature until the following day. A weapon can have this property more than once, but only once per synergy prerequisite, and each activation only triggers one type of surge. For example, you could have a +1 corrosive surge flaming surge longsword, and each activation would deal either 3d6 points of acid damage or 3d6 points of fire damage. Each diamond set into the pommel or haft of an energy surge weapon radiates a different color that corresponds to the energy damage dealt by the weapon: green (acid), blue (cold), yellow (electricity), or red (fire).
Prerequisites: Craft Magic Arms and Armor, spell for the prerequisite property.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 5th; Aura: Faint; (DC 17) evocation; Activation: Swift (command); Synergy Prerequisite: Corrosive, flaming, frost, or shock; Prerequisites: Craft Magic Arms and Armor, spell for the prerequisite property.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; scales with Con bonus for uses (stated).

## GURPS 4e
Innate Attack Follow-Up 3d6 (dice read as-is), Limited Use.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 on top of the base.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Flaming / Freezing / Shocking / Corroding (Elemental).
the four Elemental rows give the base; no on-demand burst.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### EVERBRIGHT
**Weapon property — Magic Item Compendium, PDF p. 35 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price 2,000 gp (flat))

## SOURCE (verbatim, see packet header for normalization)
```
EVERBRIGHT
Price: +2,000 gp
Property: Weapon
Caster Level: 12th
Aura: Strong; (DC 21) evocation
Activation: Standard (command)
An everbright weapon can flash with a brilliant light twice per day at your command. When it is activated, all creatures within 20 feet of you are blinded for 1 round (Reflex DC 14 negates).


An everbright weapon is also immune to acid damage and rusting effects.
Prerequisites: Craft Magic Arms and Armor, searing light.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2,000 gp; Property: Weapon; Caster Level: 12th; Aura: Strong; (DC 21) evocation; Activation: Standard (command); Prerequisites: Craft Magic Arms and Armor, searing light.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, fixed DC 14, 2/day.

## GURPS 4e
Affliction (Blindness) with an Area effect centered on the wielder (Emanation -20%), DX or reaction roll to avoid, Limited Use 2/day (percentages OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed 2,000 gp flat.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Blinding (Condition 43-48).
Blinding (Condition 43-48) is crit-triggered single-target; this is a self-centered burst.

## FORKS
1. does it blind the wielder and allies within 20 ft (printed "all creatures within 20 feet of you"); default yes, the wielder included unless blind-immune.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Affliction (Blindness) with an Area effect centered on the wielder (Emanation -20%), DX or reaction roll to avoid, Limited Use 2/day (percentages OPEN).


---

### FIERCEBANE
**Weapon property — Magic Item Compendium, PDF p. 36 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
FIERCEBANE [SYNERGY]
Price: +1 bonus
Property: Weapon
Caster Level: 12th
Aura: Strong; (DC 21) conjuration
Activation: --
Synergy Prerequisite: Bane
A fiercebane weapon excels at attacking one type or subtype of creature. It acts as a bane weapon against the creature type (and subtype, if relevant) to which its synergy prerequisite ability was attuned. Whenever it strikes its designated bane enemy, it begins to emit a low, eager hum, as if it were actually feeding off the victim's life blood. A fiercebane weapon glows when a designated foe comes within 60 feet, even if you cannot see or detect it. In addition, the weapon deals extra damage on every successful critical hit. The amount depends on its critical multiplier, as follows.
Critical Multiplier / Extra Damage: x2 1d10; x3 2d10; x4 3d10
Projectile weapons bestow this property upon their ammunition.
Lore: gnome ranger Tir Hearthand created the first fiercebane weapon, an orc bane scimitar named Hearthand (Knowledge [arcana] or Knowledge [history] DC 20; the original is believed lost, DC 30).
Prerequisites: Craft Magic Arms and Armor, summon monster I.
Cost to Create: Varies.

FLESHGRINDING
Price: +2 bonus
Property: Piercing or slashing melee weapon
Caster Level: 11th
Aura: Moderate; (DC 20) transmutation
Activation: Free (command)
You can activate a fleshgrinding weapon any time you deal damage with it to a living creature in melee. When this occurs, you let go of the weapon and it magically animates, grinding itself into the foe's flesh. In each round at the start of your turn, it automatically damages that creature as if you had scored a normal hit with it (including damage from the weapon's enhancement bonus, other weapon properties, and your normal bonus from Strength, but not extra damage from feats such as Power Attack). The grinding continues for 5 rounds or until you or someone else pulls the fleshgrinding weapon free; doing this requires a standard action and (for anyone other than you) a successful DC 20 Strength check. After the duration expires, a fleshgrinding weapon returns to your hand (as the returning weapon property). It will not return to your hand if the target has pulled the weapon free and still holds it.
Prerequisites: Craft Magic Arms and Armor, animate objects.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 12th; Aura: Strong; (DC 21) conjuration; Activation: --; Synergy Prerequisite: Bane; Prerequisites: Craft Magic Arms and Armor, summon monster I.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** crit rider by multiplier class (default 1d / 2d / 3d), detection 60 ft as a proximity sense.

## GURPS 4e
crit rider by multiplier class (default 1d / 2d / 3d), detection 60 ft as a proximity sense.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 on top of Bane.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Bane (DMG).
DMG Bane (see that file) plus the burst template. Delta = crit rider and 60-ft detection.

## FORKS
shares the Bane rulings (foe chosen by the crafter).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### GHOST STRIKE
**Weapon property — Magic Item Compendium, PDF p. 36 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
GHOST STRIKE [SYNERGY]
Price: +1 bonus
Property: Melee weapon
Caster Level: 11th
Aura: Moderate; (DC 20) conjuration
Activation: --
Synergy Prerequisite: Ghost touch
A ghost strike weapon functions as a ghost touch weapon (DMG 224). In addition, sneak attacks and critical hits made with a ghost strike weapon against an undead creature affect it as if it were a living creature.
Prerequisites: Craft Magic Arms and Armor, undeath to death.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 11th; Aura: Moderate; (DC 20) conjuration; Activation: --; Synergy Prerequisite: Ghost touch; Prerequisites: Craft Magic Arms and Armor, undeath to death.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; in GURPS the weapon's attacks ignore the Unliving crit and precision immunities (named trait handling OPEN).

## GURPS 4e
as printed; in GURPS the weapon's attacks ignore the Unliving crit and precision immunities (named trait handling OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 on top of Ghost Touch.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Ghost Touch (DMG).
DMG Ghost Touch (see that file). Delta = precision and crit immunity of undead removed.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- in GURPS the weapon's attacks ignore the Unliving crit and precision immunities (named trait handling OPEN).


---

### GHOST TOUCH
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 225 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Ghost Touch: A ghost touch weapon deals damage normally against incorporeal creatures, regardless of its bonus. (An incorporeal creature's 50% chance to avoid damage does not apply to attacks with ghost touch weapons.) The weapon can be picked up


and moved by an incorporeal creature at any time. A manifesting ghost can wield the weapon against corporeal foes. Essentially, a ghost touch weapon counts as either corporeal or incorporeal at any given time, whichever is more beneficial to the wielder.
Moderate conjuration; CL 9th; Craft. Magic Arms and Armor, plane shift; Price +1 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** attacks with the weapon ignore the incorporeal 50% miss chance and deal full damage at any item tier; an incorporeal creature may pick up, move and wield the weapon (against corporeal foes too); the weapon counts as corporeal or incorporeal, wielder's choice each turn. No save, no SR.

## GURPS 4e
Gadget (Breakable -25%, Can Be Stolen -10%); the weapon's attacks gain Affects Insubstantial (the pool already uses this trait at T3+). Enhancement percentage for Affects Insubstantial on a weapon attack: OPEN (not in the repo indices); no point total stated. Incorporeal wielding is a mechanism note with no point cost.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed +1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Penetrating Strikes (Offensive 85-90).
Penetrating Strikes (Offensive 85-90): GURPS "Affects Insubstantial at T3+"; 3.5e lists material bypass only. Gap: the pool row works at T3+ only, carries no 50%-miss clause, and has no incorporeal-wielder or dual-status clause.

## NAME COLLISION
Penetrating Strikes (pool, redundant at T3+); SRD ghost touch armor property.

## FORKS
1. Ghost Touch plus Penetrating Strikes on one weapon is redundant above T3. Default: allowed, no stacking benefit.
2. "Whichever is better" on the same swing. Default: wielder declares at the start of each turn.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Enhancement percentage for Affects Insubstantial on a weapon attack: OPEN (not in the repo indices);


---

### HARMONIZING
**Weapon property — Magic Item Compendium, PDF p. 36 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
HARMONIZING
Price: +1 bonus
Property: Melee weapon
Caster Level: 5th
Aura: Faint; (DC 17) illusion
Activation: --; see text
A harmonizing weapon accompanies you in song if drawn, granting a +2 competence bonus on Perform (sing) checks. In addition, if you hold a harmonizing weapon when you begin a bardic music effect, the weapon can continue the effect for you, allowing you to focus on other efforts. One round after you begin a bardic music effect that allows or requires continued use or concentration (including inspire courage, countersong, fascinate, inspire competence, inspire greatness, song of freedom, and inspire heroics), the weapon picks up and continues the performance flawlessly for 10 rounds, until you start another bardic music effect, or until you command it to end as a swift (mental) action.
Prerequisites: Craft Magic Arms and Armor, ghost sound, bardic music.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 5th; Aura: Faint; (DC 17) illusion; Activation: --; see text; Prerequisites: Craft Magic Arms and Armor, ghost sound, bardic music.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; class-gated by bardic music.

## GURPS 4e
+2 to Singing and a Delayed ongoing Bard Song effect for 10 turns (campaign bard analogue named at ratification, OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- +2 to Singing and a Delayed ongoing Bard Song effect for 10 turns (campaign bard analogue named at ratification, OPEN).


---

### HEAVENLY BURST
**Weapon property — Magic Item Compendium, PDF p. 37 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
HEAVENLY BURST
Price: +1 bonus
Property: Weapon
Caster Level: 7th
Aura: Moderate; (DC 18) evocation
Activation: --
On a critical hit against an evil creature, a heavenly burst weapon discharges a shower of radiance that deals 3d6 points of damage to the target and blinds it for 1 round. A successful DC 14 Fortitude save negates the blindness.
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, holy smite.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 7th; Aura: Moderate; (DC 18) evocation; Activation: --; Prerequisites: Craft Magic Arms and Armor, holy smite.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, fixed DC 14, damage is not multiplied.

## GURPS 4e
Innate Attack Follow-Up 2d (Executioner T3 for 3d6 is a proxy, OPEN), Trigger critical, Accessibility evil only (percentage OPEN), blindness Affliction.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Radiant (Elemental 45-50).
Radiant (Elemental 45-50) is always-on positive energy damage. This is crit-triggered and evil-keyed.

## FORKS
shared alignment-tag ruling (GURPS has no alignment axis, see DMG Holy).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Innate Attack Follow-Up 2d (Executioner T3 for 3d6 is a proxy, OPEN), Trigger critical, Accessibility evil only (percentage OPEN), blindness Affliction.


---

### HIDEAWAY
**Weapon property — Magic Item Compendium, PDF p. 37 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price 2,000 gp (flat))

## SOURCE (verbatim, see packet header for normalization)
```
HIDEAWAY
Price: +2,000 gp
Property: Weapon
Caster Level: 5th
Aura: Faint; (DC 17) transmutation
Activation: Swift (command)
When activated, a hideaway weapon folds up into a bundle two size categories smaller than you, making it easy to conceal. You gain a +2 bonus on Sleight of Hand checks to conceal a hideaway weapon when it's folded up (as if it were a dagger). A second command word (also a swift action) causes the weapon to unfold to its normal shape.
Prerequisites: Craft Magic Arms and Armor, shrink item.
Cost to Create: 1,000 gp, 80 XP, 2 days.
```

## D&D 3.5e
**Printed header:** Price: +2,000 gp; Property: Weapon; Caster Level: 5th; Aura: Faint; (DC 17) transmutation; Activation: Swift (command); Prerequisites: Craft Magic Arms and Armor, shrink item.; Cost to Create: 1,000 gp, 80 XP, 2 days.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
Gadget with Shrinking-style concealment and +2 to Concealment-type skill (Sleight of Hand analogue; costs OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed 2,000 gp flat.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- costs OPEN).


---

### HOLY SURGE
**Weapon property — Magic Item Compendium, PDF p. 37 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
HOLY SURGE [SYNERGY]
Price: +1 bonus
Property: Melee weapon
Caster Level: 11th
Aura: Moderate; (DC 20) evocation
Activation: -- and swift (command)
Synergy Prerequisite: Holy
A holy surge weapon functions as a holy weapon (DMG 225). This is a continuous effect and requires no activation. In addition, on a successful melee attack with a holy surge weapon, you can command it to emit a burst of holy energy. Against an evil target, this burst deals an extra 3d6 points of damage. If used against a non-evil creature, it deals no additional damage, and that use of the property is wasted. This ability is usable a number of times per day equal to 1 + your Cha bonus (if any). Once you activate this property, it can't be activated by any other creature until the following day.
Prerequisites: Craft Magic Arms and Armor, holy smite or holy word.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 11th; Aura: Moderate; (DC 20) evocation; Activation: -- and swift (command); Synergy Prerequisite: Holy; Prerequisites: Craft Magic Arms and Armor, holy smite or holy word.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; scales with Cha bonus for uses (stated).

## GURPS 4e
Holy's Follow-Up plus a 3d6 burst, Limited Use (1 + Will-based Cha stand-in, OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 on top of Holy.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Holy (DMG).
DMG Holy (see that file) plus the Energy Surge on-demand burst pattern.

## FORKS
shared alignment-tag ruling.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Holy's Follow-Up plus a 3d6 burst, Limited Use (1 + Will-based Cha stand-in, OPEN).


---

### HUNTING
**Weapon property — Magic Item Compendium, PDF p. 37 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
HUNTING
Price: +1 bonus
Property: Weapon
Caster Level: 6th
Aura: Moderate; (DC 18) abjuration
Activation: --
A hunting weapon increases your bonus on weapon damage rolls by 4 against your favored enemies (see the ranger class feature; PH 47).
Prerequisites: Craft Magic Arms and Armor, greater magic fang.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 6th; Aura: Moderate; (DC 18) abjuration; Activation: --; Prerequisites: Craft Magic Arms and Armor, greater magic fang.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** +4 damage vs favored enemies, a flat bonus that requires the ranger feature (class-gated); not multiplied on a crit.

## GURPS 4e
+2 damage vs favored enemies (2:1 default), requires the campaign's ranger analogue (OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Hunter's Mark (Offensive 55-60).
Hunter's Mark (Offensive 55-60) is a marked-target bonus, not a favored-enemy bonus.

## FORKS
1. GURPS conversion of a flat +4 (default +2).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- +2 damage vs favored enemies (2:1 default), requires the campaign's ranger analogue (OPEN).


---

### ILLUMINATING
**Weapon property — Magic Item Compendium, PDF p. 37 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price 500 gp (flat))

## SOURCE (verbatim, see packet header for normalization)
```
ILLUMINATING
Price: +500 gp
Property: Weapon
Caster Level: 5th
Aura: Faint; (DC 17) evocation
Activation: --
When drawn, an illuminating weapon glows with pure white light, brightly illuminating a 20-foot-radius area and providing shadowy illumination for another 20 feet beyond that.
Prerequisites: Craft Magic Arms and Armor, light.
Cost to Create: 250 gp, 20 XP, 1 day.
```

## D&D 3.5e
**Printed header:** Price: +500 gp; Property: Weapon; Caster Level: 5th; Aura: Faint; (DC 17) evocation; Activation: --; Prerequisites: Craft Magic Arms and Armor, light.; Cost to Create: 250 gp, 20 XP, 1 day.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed (GURPS Light-source, no combat effect).

## GURPS 4e
as printed (GURPS Light-source, no combat effect).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed 500 gp flat.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### ILLUSION BANE
**Weapon property — Magic Item Compendium, PDF p. 37 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
ILLUSION BANE
Price: +1 bonus
Property: Weapon
Caster Level: 10th
Aura: Moderate; (DC 20) divination
Activation: -- and swift (command)
Any attack with an illusion bane weapon ignores any miss chance created by an illusion effect (including effects that mimic illusions, such as a displacer beast's displacement effect). However, you must still target the correct square when making an attack against a foe that has total concealment. This is a continuous effect and requires no activation. In addition, once per day you can activate an illusion bane weapon to destroy illusion effects. This ability can take one of two forms: After hitting a creature, you can activate the weapon in the same round to make a dispel check (1d20+10) against each illusion spell currently affecting the target. This effect essentially acts as a targeted dispel magic spell, but it functions only against magic of the illusion school. You must make a separate check for each illusion spell affecting the target. Alternatively, you can attempt to dispel a single illusion by touching it with the


illusion bane weapon and speaking the appropriate command word. For example, touching a silent image spell (or an image generated by the mirror image spell) with the weapon subjects it to the dispel check immediately. A successful check against any part of the illusion dispels the whole effect, so dispelling one mirror image ends the spell entirely for the target creature.
Lore: created by a sect of the church of St. Cuthbert (Knowledge [religion] DC 20); functions much like dispel magic but only against illusion effects (Knowledge [arcana] DC 25).
Prerequisites: Craft Magic Arms and Armor, true seeing, dispel magic.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 10th; Aura: Moderate; (DC 20) divination; Activation: -- and swift (command); Prerequisites: Craft Magic Arms and Armor, true seeing, dispel magic.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; fixed +10 on the dispel check (flat-source), 1/day.

## GURPS 4e
ignore illusion-based attack penalties plus an Neutralize (Illusion) once per day (modifier OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Dispelling Strike (Condition 85-90).
Dispelling Strike (Condition 85-90) is school-agnostic and 1/encounter; DMG Seeking is the miss-chance half for ranged weapons.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- ignore illusion-based attack penalties plus an Neutralize (Illusion) once per day (modifier OPEN).


---

### IMPALING
**Weapon property — Magic Item Compendium, PDF p. 38 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
IMPALING
Price: +1 bonus
Property: Piercing melee weapon
Caster Level: 9th
Aura: Moderate; (DC 19) transmutation
Activation: Swift (command)
Three times per day, you can activate this weapon to treat its next attack (if made before the end of your turn) as a touch attack. You must declare that you are using this property before making your attack roll. If the attack misses, the use is wasted.
Prerequisites: Craft Magic Arms and Armor, find the gap (SC 91).
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Piercing melee weapon; Caster Level: 9th; Aura: Moderate; (DC 19) transmutation; Activation: Swift (command); Prerequisites: Craft Magic Arms and Armor, find the gap (SC 91).; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, 3/day.

## GURPS 4e
the attack ignores worn and natural armor DR (Armor Divisor "ignores", OPEN) for one attack, Limited Use 3/day.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Armor Piercing (Offensive 19-24).
Armor Piercing (Offensive 19-24) ignores DR, not AC; Precise Thrust (temper 23A-4) is +2/+3/+4 against armor.

## FORKS
1. the pool's Armor Divisor ladder tops at 5, so "ignore all armor" needs an open step.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- the attack ignores worn and natural armor DR (Armor Divisor "ignores", OPEN) for one attack, Limited Use 3/day.


---

### INCORPOREAL BINDING
**Weapon property — Magic Item Compendium, PDF p. 39 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
INCORPOREAL BINDING [SYNERGY]
Price: +1 bonus
Property: Melee weapon
Caster Level: 9th
Aura: Moderate; (DC 19) conjuration
Activation: --
Synergy Prerequisite: Ghost touch
An incorporeal binding weapon functions as a ghost touch weapon (DMG 224). In addition, when this weapon strikes an incorporeal creature, it emits a single pulse of gray energy that temporarily anchors the target more firmly to the material world. An incorporeal creature damaged by this weapon loses the benefit of its incorporeal miss chance (50%) and its 50% chance to ignore spells for 1 round. It does, however, retain all other benefits of incorporealness, including immunity to all nonmagical attack forms, the ability to pass through solid objects, and a deflection bonus to AC equal to its Charisma bonus (if any).
Prerequisites: Craft Magic Arms and Armor, dimensional anchor, plane shift.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 9th; Aura: Moderate; (DC 19) conjuration; Activation: --; Synergy Prerequisite: Ghost touch; Prerequisites: Craft Magic Arms and Armor, dimensional anchor, plane shift.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; in GURPS the target loses the Insubstantial defenses that rely on a miss roll for 1 second (OPEN).

## GURPS 4e
as printed; in GURPS the target loses the Insubstantial defenses that rely on a miss roll for 1 second (OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 on top of Ghost Touch.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Ghost Touch (DMG).
DMG Ghost Touch (see that file). Delta = the one-round anchoring on damage.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- in GURPS the target loses the Insubstantial defenses that rely on a miss roll for 1 second (OPEN).


---

### KI FOCUS
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 226 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Ki Focus: The magic weapon serves as a channel for the wielder's ki, allowing her to use her special ki attacks through the weapon as if they were unarmed attacks. These attacks include the monk's stunning attack, ki strike, and quivering palm, as well as the Stunning Fist feat. Only melee weapons can have the ki focus ability.
Moderate transmutation; CL sth; Craft Magic Arms and Armor, creator must be a monk; Price +1 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** the wielder may deliver stunning attack, ki strike, quivering palm and Stunning Fist through the weapon exactly as through an unarmed strike. The abilities keep their own saves and DCs. Melee weapons only. No SR of its own, no healing interaction.

## GURPS 4e
no monk class; the mechanism is that any ability normally limited to bare-handed delivery may be delivered through the weapon. Chassis Gadget (Breakable -25%, Can Be Stolen -10%). The trait that expresses this (a limitation removal on the delivered ability) and its cost are OPEN; no point total stated.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed +1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none. The Skill/Class pool has martial rows (Weapon Mastery, Commander's Voice, Battle Meditation, Signature Move) but nothing for unarmed-only class abilities.

## NAME COLLISION
none in the Registry; the SRD class feature "ki strike" is the thing being delivered.

## FORKS
1. Does the weapon's own damage still apply when a ki attack is delivered through it? Default: the ki ability's effect applies and the weapon's damage is unchanged (the text says "as if unarmed", which does not say damage is lost).
2. Which GURPS abilities count as the monk's ki attacks. Default: the campaign's monk-equivalent techniques named at ratification; none is assumed here.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: degraded.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- The trait that expresses this (a limitation removal on the delivered ability) and its cost are OPEN;


---

### MAGEBANE
**Weapon property — Magic Item Compendium, PDF p. 39 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
MAGEBANE
Price: +1 bonus
Property: Weapon
Caster Level: 5th
Aura: Moderate; (DC 19) evocation
Activation: --
Weapons that have this property are feared by arcane spellcasters. Against any creature that can cast arcane spells or use invocations (CAr 7), a magebane weapon's enhancement bonus is 2 higher than normal. (Thus, a +1 longsword with the magebane property becomes a +3 longsword when wielded against such targets.) Furthermore, a magebane weapon deals an extra 2d6 points of damage against targets capable of casting arcane spells or using invocations. The magebane property can be added to a cold iron weapon without paying the extra 2,000 gp (DMG 284).
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, dispel magic.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 5th; Aura: Moderate; (DC 19) evocation; Activation: --; Prerequisites: Craft Magic Arms and Armor, dispel magic.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
Innate Attack Follow-Up 2d with Accessibility "only vs. arcane casters" plus a +2 skill bonus (percentages and Weapon Bond cost OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp (cold iron surcharge waived as printed).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Bane (DMG).
DMG Bane (see that file) and Banefire. Delta = keyed to a capability (arcane caster) instead of a creature type.

## FORKS
shares the Bane forks.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- arcane casters" plus a +2 skill bonus (percentages and Weapon Bond cost OPEN).


---

### MERCIFUL
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 226 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Merciful: The weapon deals an extra 1d6 points of damage, and all damage it deals is nonlethal damage. On command, the weapon suppresses this ability until commanded to resume it. Bows, crossbows, and slings so crafted bestow the merciful effect upon their ammunition.
Faint conjuration; CL 5th; Craft Magic Arms and Armor, cure light wounds; Price +1 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** on each damaging hit the weapon adds +1d6 untyped damage, and all damage from the weapon (base and extra) is nonlethal. Command word suppresses and resumes the ability. No save, no SR. No healing interaction.

## GURPS 4e
chassis Gadget (Breakable -25%, Can Be Stolen -10%). Extra damage = Innate Attack, Follow-Up +0%, 1d6 (dice read as-is), Magical -10%. Nonlethal delivery means the damage is taken as FP loss rather than HP; the trait and its modifier for that are OPEN, so no point total is stated.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed +1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Life Shield and Second Wind are healing, not nonlethal delivery).

## NAME COLLISION
none in the Registry; SRD merciful special ability is this one.

## FORKS
1. Does the extra 1d6 stay when the ability is suppressed? Default: no, suppression turns off both the extra damage and the nonlethal conversion.
2. Does the nonlethal conversion also cover the base weapon damage in GURPS? Default: yes, to match the printed "all damage".

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- the trait and its modifier for that are OPEN, so no point total is stated.


---

### MIGHTY CLEAVING
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 226 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Mighty Cleaving: A mighty cleaving weapon allows a wielder with the Cleave feat to make one additional cleave attempt in a round.
Moderate evocation; CL 8th; Craft Magic Arms and Armor, divine power; Price +1 bonus,
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** a wielder with Cleave (or Great Cleave) may make one more cleave attempt per round than the feat normally allows. Requires the Cleave feat, as printed. No save, no SR.

## GURPS 4e
Gadget (Breakable -25%, Can Be Stolen -10%); the wielder's Extra Attack (Trigger: killing blow) may fire one more time per round. Cost of the extra trigger and the GURPS stand-in for the Cleave feat prerequisite: OPEN; no point total stated.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed +1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Cleave Through (temper 23A-1).
Cleave Through (temper 23A-1, a post-affix layer, not an affix pool row): on a kill, a free attack on an adjacent foe (as Cleave; T2+ Great Cleave); GURPS Extra Attack 1 (Trigger: killing blow). The temper grants the cleave itself; it does not add an extra per-round attempt.

## NAME COLLISION
Cleave Through (temper 23A-1); SRD feats Cleave and Great Cleave.

## FORKS
1. Mighty Cleaving on a weapon that also carries the Cleave Through temper. Default: the temper's free attack counts as the first cleave and Mighty Cleaving adds one more, still without needing the feat for the temper's attempt.
2. GURPS prerequisite. Default: the wielder must already own an Extra Attack (Trigger: killing blow) or a campaign-named cleave technique.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Cost of the extra trigger and the GURPS stand-in for the Cleave feat prerequisite: OPEN;


---

### MIGHTY SMITING
**Weapon property — Magic Item Compendium, PDF p. 40 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
MIGHTY SMITING
Price: +1 bonus
Property: Melee weapon
Caster Level: 5th
Aura: Moderate; (DC 19) evocation
Activation: --
If you have a smite ability (smite, smite evil, smite shadowlands, or the like), you gain an extra +2 bonus on your smite attack rolls and damage rolls. In addition, you gain one additional use of your smite ability each day while wielding this weapon. If you have more than one smite ability, you must choose which one gains the extra use. A weapon of mighty smiting only grants one extra smite per day, regardless of how many characters wield it.
Prerequisites: Craft Magic Arms and Armor, divine power.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 5th; Aura: Moderate; (DC 19) evocation; Activation: --; Prerequisites: Craft Magic Arms and Armor, divine power.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; class-gated and flat.

## GURPS 4e
+1 on the smite roll and damage (2:1), one extra use, requires a campaign smite analogue (OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Sacred Word and Signature Move are different).

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- +1 on the smite roll and damage (2:1), one extra use, requires a campaign smite analogue (OPEN).


---

### MORPHING
**Weapon property — Magic Item Compendium, PDF p. 40 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
MORPHING
Price: +1 bonus
Property: Melee or thrown weapon
Caster Level: 9th
Aura: Moderate; (DC 19) transmutation
Activation: Standard
You can reshape a morphing weapon into any other melee or thrown weapon of the same size and type (light, one-handed, or two-handed). For instance, a morphing greatsword could become a spear, greataxe, or dire flail. If a single weapon created with the morphing property becomes a double weapon, only one end of the double weapon retains the weapon's magical bonus, although the other end is masterwork. If a double weapon created with the morphing property becomes a single weapon, it can have the properties of either end of the original double weapon. The properties of the other end are dormant but not lost; they become active again when the morphing weapon once again becomes a double weapon.
Prerequisites: Craft Magic Arms and Armor, fabricate.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee or thrown weapon; Caster Level: 9th; Aura: Moderate; (DC 19) transmutation; Activation: Standard; Prerequisites: Craft Magic Arms and Armor, fabricate.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; GURPS reshapes into any weapon of the same weight class and reach profile (modifier OPEN).

## GURPS 4e
as printed; GURPS reshapes into any weapon of the same weight class and reach profile (modifier OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
Changeling (batch 02) is spear-only; Chameleon changes appearance.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- GURPS reshapes into any weapon of the same weight class and reach profile (modifier OPEN).


---

### PARALYZING
**Weapon property — Magic Item Compendium, PDF p. 40 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
PARALYZING
Price: +1 bonus
Property: Melee weapon
Caster Level: 10th
Aura: Moderate; (DC 20) enchantment
Activation: Swift (command)


When a paralyzing weapon is activated, the next creature struck by the weapon must succeed on a DC 17 Will save or be paralyzed. Each round on its turn, the target can attempt a new saving throw to end the effect; otherwise, the paralysis lasts for 10 rounds. A paralyzing weapon functions once per day.
Prerequisites: Craft Magic Arms and Armor, hold monster.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 10th; Aura: Moderate; (DC 20) enchantment; Activation: Swift (command); Prerequisites: Craft Magic Arms and Armor, hold monster.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, fixed DC 17, 1/day.

## GURPS 4e
Affliction (Paralysis) with a Will roll each second to end it (10-turn cap), Limited Use 1/day (percentages OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
Dazing is a daze, not paralysis.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Affliction (Paralysis) with a Will roll each second to end it (10-turn cap), Limited Use 1/day (percentages OPEN).


---

### PRECISE
**Weapon property — Magic Item Compendium, PDF p. 41 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
PRECISE
Price: +1 bonus
Property: Ranged weapon
Caster Level: 5th
Aura: Faint; (DC 17) evocation
Activation: --
You can shoot or throw a precise weapon at an opponent engaged in melee without incurring the standard -4 penalty. This benefit does not apply if you already have the Precise Shot feat.
Prerequisites: Craft Magic Arms and Armor, Precise Shot.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Ranged weapon; Caster Level: 5th; Aura: Faint; (DC 17) evocation; Activation: --; Prerequisites: Craft Magic Arms and Armor, Precise Shot.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
no penalty for shooting into melee (the penalty for a melee-engaged target; OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- OPEN).


---

### PROFANE
**Weapon property — Magic Item Compendium, PDF p. 41 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
PROFANE
Price: +1 bonus
Property: Weapon
Caster Level: 7th
Aura: Moderate; (DC 17) necromancy
Activation: Standard (command)
By speaking the appropriate command word, you can sheathe a profane weapon in crackling black negative energy. If you have no Constitution score, this energy does not harm you; otherwise you take 1 point of Constitution damage for each round that you hold the weapon while the effect is activated. This effect lasts until you speak another command word to end it. While activated, a profane weapon deals an extra 1d6 points of damage to any living target (or 2d6 points against a good outsider) on a successful hit. Also, it is treated as evil-aligned for the purpose of overcoming damage reduction.
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, inflict light wounds.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 7th; Aura: Moderate; (DC 17) necromancy; Activation: Standard (command); Prerequisites: Craft Magic Arms and Armor, inflict light wounds.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed. The wielder's cost is a drawback (stated, per round while active).

## GURPS 4e
Innate Attack Follow-Up 1d6 (2d6 vs good outsiders), Costs Fatigue or HP drain per turn on the wielder (modifier OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Shadowtouch (Elemental 39-44).
Shadowtouch (Elemental 39-44, +1d6 negative energy at T4; undead take half) is the damage half. Delta = the evil-DR tag, the 2d6 vs good outsiders, and the wielder's Constitution cost.

## FORKS
1. the Constitution cost: default keep as printed (it is the property's price for its low +1).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Innate Attack Follow-Up 1d6 (2d6 vs good outsiders), Costs Fatigue or HP drain per turn on the wielder (modifier OPEN).


---

### PROFANE BURST
**Weapon property — Magic Item Compendium, PDF p. 41 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
PROFANE BURST [SYNERGY]
Price: +1 bonus
Property: Weapon
Caster Level: 12th
Aura: Strong; (DC 21) necromancy
Activation: Standard (command) and --
Synergy Prerequisite: Profane
A profane burst weapon functions as a profane weapon (see above). In addition, the weapon explodes with negative energy on a successful critical hit, dealing extra negative energy damage as set out in the table below. (This effect activates even if the target is not normally subject to extra damage from critical hits.) A profane burst weapon deals even more damage to good outsiders on a successful critical hit. This burst does not harm you or any creature other than the target if you are undead; otherwise, you take 1d4 points of Constitution damage (or Charisma damage if you have no Constitution score). This is a continuous effect and requires no activation. Even if the weapon has not been activated to deal extra damage because of the profane property, the weapon still deals its extra negative energy damage on a successful critical hit.


Critical Multiplier / Extra Damage / Good Outsider Extra Damage: x2 1d10 2d10; x3 2d10 4d10; x4 3d10 6d10
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, inflict critical wounds.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 12th; Aura: Strong; (DC 21) necromancy; Activation: Standard (command) and --; Synergy Prerequisite: Profane; Prerequisites: Craft Magic Arms and Armor, inflict critical wounds.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** crit dice by multiplier class (default 1d / 2d / 3d, doubled vs good outsiders), self-damage 1d4 Con per burst.

## GURPS 4e
crit dice by multiplier class (default 1d / 2d / 3d, doubled vs good outsiders), self-damage 1d4 Con per burst.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 on top of Profane.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Profane (MIC).
Profane (above) plus the burst template (Icy Burst). Delta = the crit rider and the wielder's per-burst cost.

## FORKS
none (the weapon's own 3.5e crit multiplier applies).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### QUICK LOADING
**Weapon property — Magic Item Compendium, PDF p. 42 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
QUICK LOADING
Price: +1 bonus
Property: Crossbow
Caster Level: 9th
Aura: Moderate; (DC 19) conjuration
Activation: Free (manipulation) or move (manipulation); see text
A quick loading crossbow accesses an extradimensional space that can hold up to 100 bolts, allowing you to reload the crossbow more rapidly than normal. Reloading a quick loading hand or light crossbow is a free action (allowing a character with multiple attacks to use his full attack rate), and reloading a quick loading heavy crossbow is a move action. Different types of bolts can be held in the extradimensional space, and you can select freely from these when reloading the crossbow. Adding or removing a bolt


by hand from an extradimensional space requires a move (manipulation) action.
Prerequisites: Craft Magic Arms and Armor, Leomund's secret chest, shrink item.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Crossbow; Caster Level: 9th; Aura: Moderate; (DC 19) conjuration; Activation: Free (manipulation) or move (manipulation); see text; Prerequisites: Craft Magic Arms and Armor, Leomund's secret chest, shrink item.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
Payload (the pool's Dimensional Pocket trait) of 100 bolts and Fast-Draw (Ammo) for free reloads (costs OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
Dimensional Pocket (Utility 97-100, capacity 10/25/50/100/250 lbs) is the storage half; Rapid Assault is extra attacks, not reload speed.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Payload (the pool's Dimensional Pocket trait) of 100 bolts and Fast-Draw (Ammo) for free reloads (costs OPEN).


---

### RESOUNDING
**Weapon property — Magic Item Compendium, PDF p. 43 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
RESOUNDING
Price: +1 bonus
Property: Melee weapon
Caster Level: 5th
Aura: Faint; (DC 17) enchantment
Activation: --
A resounding weapon emits a deep, ringing chime each time it successfully hits a target. The sound carries over the din of battle, encouraging your allies. When you strike a foe with a resounding weapon, allies (including you) within 30 feet gain a +1 morale bonus on attack rolls and saves against fear effects for 1 round.
Prerequisites: Craft Magic Arms and Armor, bless.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 5th; Aura: Faint; (DC 17) enchantment; Activation: --; Prerequisites: Craft Magic Arms and Armor, bless.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, fixed +1.

## GURPS 4e
allies within 10 yards get +1 to hit and +1 to Fright Checks for 1 second after each hit (OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Commander's Voice (Skill/Class 25-30).
Commander's Voice (Skill/Class 25-30) is a leadership/rally score bonus, not an aura.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- allies within 10 yards get +1 to hit and +1 to Fright Checks for 1 second after each hit (OPEN).


---

### RETURNING
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 226 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Returning: This special ability can only be placed on a weapon that can be thrown. A returning weapon flies through the air back to the creature that threw it. It returns to the thrower just before the creature's next turn (and is therefore ready to use again in that turn). Catching a returning weapon when it comes back is a free action. If the character can't catch it, or if the character has moved since throwing it, the weapon drops to the ground in the square from which it was thrown.
Moderate transmutation; CL 7th; Craft Magic Arms and Armor, telekinesis; Price +1 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed. Return occurs just before the thrower's next turn; catch is a free action; a thrower who moved, or who cannot catch, finds the weapon on the ground in the square it was thrown from. No save, no SR.

## GURPS 4e
no verified GURPS trait for automatic return. Nearest registry precedent is Warp as used for Phasewalk, limited to the weapon only, returning to the thrower's hand, range equal to the throw. The trait, its modifiers and cost are OPEN; no point total stated. Chassis Gadget (Breakable -25%, Can Be Stolen -10%).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed +1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none. Throwing (batch C file) gives melee weapons a thrown range; Returning is its natural pair.

## NAME COLLISION
Throwing (sibling); SRD returning is this ability.

## FORKS
1. GURPS has no initiative-turn "just before your next turn". Default: the weapon returns at the end of the thrower's turn in GURPS, one second later, available next turn.
2. Returning on a weapon that cannot be thrown. Default: invalid, per the printed restriction.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- The trait, its modifiers and cost are OPEN;


---

### REVEALING
**Weapon property — Magic Item Compendium, PDF p. 43 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
REVEALING
Price: +1 bonus
Property: Weapon
Caster Level: 5th
Aura: Faint; (DC 17) evocation
Activation: --
Any opponent struck by a weapon that has this property is outlined in magical flames, as the faerie fire spell, for 1 round.
Prerequisites: Craft Magic Arms and Armor, faerie fire.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 5th; Aura: Faint; (DC 17) evocation; Activation: --; Prerequisites: Craft Magic Arms and Armor, faerie fire.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; faerie fire negates concealment and displacement-style benefits for 1 round.

## GURPS 4e
the target is Highlighted: vision penalties from darkness or invisibility do not apply against it for 1 second.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Hunter's Mark marks a target on a swift action; Seeking negates the wielder's own miss chances).

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### SACRED
**Weapon property — Magic Item Compendium, PDF p. 43 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
SACRED
Price: +1 bonus
Property: Weapon
Caster Level: 7th
Aura: Moderate; (DC 18) conjuration
Activation: Standard (command)
By speaking the appropriate command word, you can sheathe a sacred weapon in luminous positive energy. If you are not undead, this energy does not harm you; otherwise, you take 1 point of Charisma damage for each round that you hold the weapon. This effect lasts until you speak another command word to end it. While activated, a sacred weapon deals an extra 1d6 points of damage to any undead target (or 2d6 points against an evil outsider) on a successful hit. Also, it is treated as good-aligned for the purpose of overcoming damage reduction.
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, cure light wounds.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 7th; Aura: Moderate; (DC 18) conjuration; Activation: Standard (command); Prerequisites: Craft Magic Arms and Armor, cure light wounds.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; GURPS Innate Attack Follow-Up 1d6 (2d6 vs evil outsiders), Costs Fatigue-style drain on an undead wielder (OPEN).

## GURPS 4e
as printed; GURPS Innate Attack Follow-Up 1d6 (2d6 vs evil outsiders), Costs Fatigue-style drain on an undead wielder (OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Radiant (Elemental 45-50).
Radiant (Elemental 45-50) gives +1d6 positive energy at T4 (undead x1.5). Delta = the good-DR tag, the 2d6 vs evil outsiders, and the undead wielder's Charisma cost. Mirror of Profane (batch 09).

## FORKS
shared alignment-tag ruling.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- GURPS Innate Attack Follow-Up 1d6 (2d6 vs evil outsiders), Costs Fatigue-style drain on an undead wielder (OPEN).


---

### SACRED BURST
**Weapon property — Magic Item Compendium, PDF p. 43 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
SACRED BURST [SYNERGY]
Price: +1 bonus
Property: Weapon
Caster Level: 12th
Aura: Strong; (DC 21) conjuration
Activation: --
Synergy Prerequisite: Sacred
A sacred burst weapon functions as a sacred weapon (see above). In addition, the weapon explodes with positive energy on a successful critical hit, dealing extra positive energy damage to creatures as set out in the table below. (This effect activates even if the target is not normally subject to extra damage from critical hits.) A sacred burst weapon deals even more damage to evil outsiders on a successful critical hit. This burst does not harm you or any creature other than the target unless you are undead; if you are, you take 1d4 points of Charisma damage from the burst. This is a continuous effect and requires no activation. Even if the weapon has not been activated to deal extra damage because of the sacred property, the weapon still deals its extra positive energy damage on a successful critical hit.
Critical Multiplier / Extra Damage / Evil Outsider Extra Damage: x2 1d10 2d10; x3 2d10 4d10; x4 3d10 6d10
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, cure critical wounds.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 12th; Aura: Strong; (DC 21) conjuration; Activation: --; Synergy Prerequisite: Sacred; Prerequisites: Craft Magic Arms and Armor, cure critical wounds.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** As printed over Sacred: on a critical hit, extra positive-energy damage by the weapon's own multiplier class (x2 1d10, x3 2d10, x4 3d10; evil outsider 2d10 / 4d10 / 6d10), even against crit-immune targets; only the target is harmed unless you are undead (then 1d4 Cha damage to you); continuous.

## GURPS 4e
Rider on a confirmed crit (undefended): dice by multiplier class 1d / 2d / 3d, doubled against an evil outsider, ignoring worn DR; works against crit-immune targets; undead wielder takes 1d4 Cha as the burst cost. Gadget chassis Breakable -25% / Can Be Stolen -10%; uncosted.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 on top.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Sacred (MIC).


## FORKS
shared burst fork.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### SCREAMING
**Weapon property — Magic Item Compendium, PDF p. 43 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
SCREAMING
Price: +1 bonus
Property: Weapon
Caster Level: 7th
Aura: Moderate; (DC 18) evocation
Activation: Standard (command)
Upon command, this weapon begins to vibrate gently, though it emits no actual sound in this mode. Whenever an activated screaming weapon hits, it produces a high-pitched sound and deals an extra 1d4 points of sonic damage to the target. This noise is unpleasant, but it has no adverse effect upon any creatures other than the one struck. The ability of a screaming weapon to deal extra sonic damage is negated in any area of magical silence. Screaming weapons have no additional adverse effect on creatures with unusually acute hearing, although such creatures tend to dislike them.
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, shout or sound burst.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 7th; Aura: Moderate; (DC 18) evocation; Activation: Standard (command); Prerequisites: Craft Magic Arms and Armor, shout or sound burst.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
Innate Attack Follow-Up 1d4 (dice read as-is) with a Crushing [Sonic] special effect (the exchange table lists sonic as Crushing; the pool uses Crushing [Sonic]).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
the Elemental pool has no pure sonic row (Stormborn is sonic plus lightning, split); the printed 1d4 equals the Elemental T5 die.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### SCREAMING BURST
**Weapon property — Magic Item Compendium, PDF p. 43 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
SCREAMING BURST [SYNERGY]
Price: +1 bonus
Property: Weapon
Caster Level: 12th
Aura: Strong; (DC 21) evocation
Activation: --
Synergy Prerequisite: Screaming
A screaming burst weapon functions as a screaming weapon (see above). In addition, the weapon explodes with sonic energy on a successful critical hit, dealing extra sonic damage as set out in the table below. (This effect activates even if the target is not normally subject to extra damage from critical hits.) This burst does not harm you or any creature other than the target. This is a continuous effect and requires no activation. Even if the weapon has not been activated to deal extra damage because of the screaming property, the weapon still deals its extra sonic damage on a successful critical hit.


Critical Multiplier / Extra Sonic Damage: x2 1d8; x3 2d8; x4 3d8
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, shout or sound burst.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 12th; Aura: Strong; (DC 21) evocation; Activation: --; Synergy Prerequisite: Screaming; Prerequisites: Craft Magic Arms and Armor, shout or sound burst.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** As printed over Screaming: on a critical hit, extra sonic damage by the weapon's own multiplier class (x2 1d8, x3 2d8, x4 3d8), even against crit-immune targets; only the target is harmed; continuous.

## GURPS 4e
Rider on a confirmed crit (undefended): sonic dice by multiplier class 1d / 2d / 3d, ignoring worn DR; works against crit-immune targets. Gadget chassis Breakable -25% / Can Be Stolen -10%; uncosted.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 on top.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Screaming (MIC).


## FORKS
shared burst fork.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### SEEKING
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 226 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Seeking: Only ranged weapons can have the seeking ability. The weapon veers toward its target, negating any miss chances that would otherwise apply, such as from concealment. (The wielder still has to aim the weapon at the right square. Arrows mistakenly shot into an empty space, for example, do not veer and hit invisible enemies, even if they are nearby.)
Strong divination; CL 12th; Craft Magic Arms and Armor, true seeing, Price +1 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** ranged attacks with the weapon ignore miss chances that would otherwise apply, such as from concealment; the wielder must still target the correct square. Ammunition weapons confer the property. No save, no SR.

## GURPS 4e
negate vision and concealment attack penalties for the weapon's attacks, still requiring the correct target. Nearest baked modifier is Homing +50% (tracking attacks, from the exchange-rate table); whether it fits a weapon attack that is not an Innate Attack is OPEN, so no point total is stated. Chassis Gadget (Breakable -25%, Can Be Stolen -10%).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed +1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none. Hunter's Mark (bonus damage vs a marked target), Precise Thrust (temper, vs armor) and Deflecting (defense) do not negate miss chances.

## NAME COLLISION
Hunter's Mark (pool), Precise Thrust (temper), spell seeking; none mechanically overlapping.

## FORKS
1. Does it also negate the incorporeal 50% chance? Default: no, only miss chances from concealment-type effects; incorporeal is Ghost Touch's job.
2. Thrown weapons. Default: not covered, per the printed "only ranged weapons" (a Throwing weapon is melee).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- whether it fits a weapon attack that is not an Innate Attack is OPEN, so no point total is stated.


---

### SHADOWSTRIKE
**Weapon property — Magic Item Compendium, PDF p. 44 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price 5,000 gp (flat))

## SOURCE (verbatim, see packet header for normalization)
```
SHADOWSTRIKE
Price: +5,000 gp
Property: Weapon
Caster Level: 15th
Aura: Strong; (DC 22) illusion
Activation: Swift (mental)
A shadowstrike weapon can reach through your own shadow to catch foes off guard. Once per day, you can activate the property to add 5 feet to the weapon's reach for a single attack. The target is denied its Dexterity bonus to AC for this attack.
Prerequisites: Craft Magic Arms and Armor, shadow conjuration.
Cost to Create: 2,500 gp, 200 XP, 5 days.
```

## D&D 3.5e
**Printed header:** Price: +5,000 gp; Property: Weapon; Caster Level: 15th; Aura: Strong; (DC 22) illusion; Activation: Swift (mental); Prerequisites: Craft Magic Arms and Armor, shadow conjuration.; Cost to Create: 2,500 gp, 200 XP, 5 days.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
+1 yard of reach for one attack and the target gets no active defense bonus from Dexterity-based Dodge for it (OPEN), Limited Use 1/day.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed 5,000 gp flat.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- +1 yard of reach for one attack and the target gets no active defense bonus from Dexterity-based Dodge for it (OPEN), Limited Use 1/day.


---

### SHATTERMANTLE
**Weapon property — Magic Item Compendium, PDF p. 44 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
SHATTERMANTLE
Price: +1 bonus
Property: Weapon
Caster Level: 5th
Aura: Faint; (DC 17) divination
Activation: --
A shattermantle weapon damages a foe's spell resistance. Each time the weapon strikes a foe that has spell resistance, the value of that spell resistance is reduced by 2 for 1 round. The penalties for multiple hits during the same round stack. For example, if you succeed on three attacks in the same round against the same foe, that foe's spell resistance is reduced by 6 until the beginning of your next turn.
Prerequisites: Craft Magic Arms and Armor, assay spell resistance (SC 17).
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 5th; Aura: Faint; (DC 17) divination; Activation: --; Prerequisites: Craft Magic Arms and Armor, assay spell resistance (SC 17).; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; additive, linear (stacking doctrine); the cap is SR 0.

## GURPS 4e
reduce the target's Magic Resistance by 1 per hit (2:1 default, OPEN) for 1 second.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Wardbreaker (Skill/Class 91-96).
Wardbreaker (Skill/Class 91-96) gives the caster a bonus to overcome SR; this lowers the target's SR.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- reduce the target's Magic Resistance by 1 per hit (2:1 default, OPEN) for 1 second.


---

### SHIELDING
**Weapon property — Magic Item Compendium, PDF p. 44 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
SHIELDING
Price: +1 bonus
Property: Light melee weapon
Caster Level: 10th
Aura: Moderate; (DC 20) transmutation
Activation: Swift (command)
A shielding weapon is most often employed as an off-hand weapon. Activating a shielding weapon transforms it into a heavy steel shield, with the same enhancement bonus as the weapon itself (both for AC and when making shield bash attacks).
Prerequisites: Craft Magic Arms and Armor, animate objects, shield.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Light melee weapon; Caster Level: 10th; Aura: Moderate; (DC 20) transmutation; Activation: Swift (command); Prerequisites: Craft Magic Arms and Armor, animate objects, shield.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
Gadget that swaps between a weapon and a heavy steel shield with the same bonus as DB (Shield Wall's DB ladder, OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Shield Wall (Defensive 49-54).
Shield Wall (Defensive 49-54) is a shield bonus affix on a shield, not a transformation.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Gadget that swaps between a weapon and a heavy steel shield with the same bonus as DB (Shield Wall's DB ladder, OPEN).


---

### SIZING
**Weapon property — Magic Item Compendium, PDF p. 44 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price 5,000 gp (flat))

## SOURCE (verbatim, see packet header for normalization)
```
SIZING
Price: +5,000 gp
Property: Weapon
Caster Level: 9th
Aura: Moderate; (DC 19) transmutation
Activation: Swift (command)
Activating a sizing weapon changes its size category to any other that you desire.
Prerequisites: Craft Magic Arms and Armor, shrink item.
Cost to Create: 2,500 gp, 200 XP, 5 days.
```

## D&D 3.5e
**Printed header:** Price: +5,000 gp; Property: Weapon; Caster Level: 9th; Aura: Moderate; (DC 19) transmutation; Activation: Swift (command); Prerequisites: Craft Magic Arms and Armor, shrink item.; Cost to Create: 2,500 gp, 200 XP, 5 days.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; damage dice and handedness follow the new size.

## GURPS 4e
change the weapon's weight, reach and ST requirement to the chosen size class (OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed 5,000 gp flat.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Titan's Grip is wielding an oversize weapon).

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- change the weapon's weight, reach and ST requirement to the chosen size class (OPEN).


---

### SLOW BURST
**Weapon property — Magic Item Compendium, PDF p. 44 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price 5,000 gp (flat))

## SOURCE (verbatim, see packet header for normalization)
```
SLOW BURST
Price: +5,000 gp
Property: Weapon
Caster Level: 5th
Aura: Faint; (DC 17) transmutation
Activation: --
A chill aura numbs this weapon's victim when you strike true. Whenever you score a critical hit with this weapon, the target is slowed (as the slow spell) for 3 rounds (Will DC 14 negates). This effect activates even if the creature struck is not normally subject to extra damage from critical hits.
Prerequisites: Craft Magic Arms and Armor, slow.
Cost to Create: 2,500 gp, 200 XP, 5 days.
```

## D&D 3.5e
**Printed header:** Price: +5,000 gp; Property: Weapon; Caster Level: 5th; Aura: Faint; (DC 17) transmutation; Activation: --; Prerequisites: Craft Magic Arms and Armor, slow.; Cost to Create: 2,500 gp, 200 XP, 5 days.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** As printed: on a critical hit the target is slowed (as the slow spell) for 3 rounds, Will DC 14 negates, even against crit-immune targets. Price printed 5,000 gp flat.

## GURPS 4e
On a confirmed crit (undefended) the target resists with a Quick Contest of Will against effective skill 14 (the printed DC); on failure Affliction (Reduced Move, the Slowing-row mechanism) for 3 turns. Gadget chassis Breakable -25% / Can Be Stolen -10%; uncosted.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed 5,000 gp flat.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Slowing (Condition 01-08).
Slowing (Condition 01-08): on hit 1/encounter, slow 1 round, DC 12/14/16/18/22 (the printed DC 14 matches T4), GURPS Affliction (Reduced Move). Delta = crit trigger and 3-round duration.

## FORKS
1. save type: the pool's Slowing uses Fortitude, the printed Slow Burst Will; default as printed (Will).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### SOULBREAKER
**Weapon property — Magic Item Compendium, PDF p. 45 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
SOULBREAKER [SYNERGY]
Price: +1 bonus
Property: Weapon
Caster Level: 17th
Aura: Strong; (DC 23) necromancy
Activation: --
Synergy Prerequisite: Enervating
This weapon functions as an enervating weapon (see page 34). However, a negative level gained from an attack from a soulbreaker weapon doesn't fade [OCR: "after 1 hour" lost; the text reads] "...24h..." [garbled; delay figure uncertain]: if the negative level or levels have not been purged, the subject must succeed on a DC 18 Fortitude save for each negative level or lose a character level.
Prerequisites: Craft Magic Arms and Armor, energy drain.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 17th; Aura: Strong; (DC 23) necromancy; Activation: --; Synergy Prerequisite: Enervating; Prerequisites: Craft Magic Arms and Armor, energy drain.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; permanent level loss is campaign-weighty, so the default is to apply it only to NPCs unless the owner rules otherwise.

## GURPS 4e
lasting loss of points or a skill level on a failed HT roll (OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 on top of Enervating.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Enervating (MIC).
builds on Enervating (batch 04). Delta = the delayed permanent-loss save.

## RULINGS
NPC wielders use it as printed; against a PC the negative levels last 24 hours unless purged and never convert to level loss. The 24-hour delay is OCR-uncertain; confirm against the book page.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: degraded.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- lasting loss of points or a skill level on a failed HT roll (OPEN).


---

### SOULDRINKING
**Weapon property — Magic Item Compendium, PDF p. 45 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
SOULDRINKING [SYNERGY]
Price: +1 bonus
Property: Melee weapon
Caster Level: 5th
Aura: Faint; (DC 17) necromancy
Activation: --
Synergy Prerequisite: Enervating
This weapon functions as an enervating weapon (see page 34). In addition, when a souldrinking weapon scores a critical hit on a living creature, it grants you 5 temporary hit points and a +2 morale bonus on melee damage rolls. The temporary hit points don't stack with temporary hit points from any other source. This effect fades after 10 minutes.
Prerequisites: Craft Magic Arms and Armor, vampiric touch.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 5th; Aura: Faint; (DC 17) necromancy; Activation: --; Synergy Prerequisite: Enervating; Prerequisites: Craft Magic Arms and Armor, vampiric touch.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; flat.

## GURPS 4e
temporary HP buffer of 5, +1 damage for 10 minutes (2:1 default, OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 on top of Enervating.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Enervating (MIC).
Enervating (batch 04); Body Feeder (batch 02) is the nearest temp-HP-on-crit. Delta = fixed 5 temp HP and +2 morale damage.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: degraded.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- temporary HP buffer of 5, +1 damage for 10 minutes (2:1 default, OPEN).


---

### SPELL STORING
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 226 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Spell Storing: A spell storing weapon allows a spellcaster to store a single targeted spell of up to 3rd level in the weapon. (The spell must have a casting time of 1 standard action.) Any time the weapon strikes a creature and the creature takes damage from it, the weapon can immediately cast the spell on that creature as a free action if the wielder desires. (This special ability is an exception to the general rule that casting a spell from an item takes at least as long as casting that spell normally.) Inflict serious wounds, contagion, blindness, and hold person are all common choices for the stored spell. Once the spell has been cast from the weapon, a spellcaster can cast any other targeted spell of up to 3rd level into it. The weapon magically imparts to the wielder the name of the spell currently stored within it. A randomly rolled spell storing weapon has a 50% chance to have a spell stored in it already.
Strong evocation (plus aura of stored spell); CL 12th; Craft Magic Arms and Armor, creator must be a caster of at least 12th level; Price +1 bonus,
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Single rung. Targeted spell, level 3 or lower, 1-standard-action casting time. Discharge is the wielder's choice, free action, on a creature the weapon damaged, once per stored spell; any caster may refill. No d100, no save of its own; the spell's save and SR apply as printed. Bows/crossbows/slings: the SRD text does not extend it to ammunition. If the stored spell is magical healing, discharge on a struck creature ends Fatal Wound stacks below cap per the Registry rule.

## GURPS 4e
Reservoir's ER Battery is the energy store; the delta is casting the stored Magic spell on a DR-penetrating hit as a free action. Follow-Up +0% only applies to Innate Attacks, so no verified chassis exists for "release stored spell on hit". Gadget Breakable -25% + Can Be Stolen -10% = -35%. Spell energy cost and the GURPS equivalent of the 3rd-level cap: open. Points: not computable.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Reservoir (Resource 49-54).
Reservoir (Resource 49-54): store one spell/ability for later use, 1st/2nd/3rd/5th/7th; GURPS ER Battery 2/3/5/8/12 points. Spellthief (Rare Build-Around 71-80) captures a spell on a successful save, a different trigger. Gap: Reservoir's T3 rung (3rd level) matches the cap, but the row does not say targeted-only, free-action discharge on a damaging weapon hit, or refill by any caster.

## NAME COLLISION
Reservoir, Spellthief, SRD ring of spell storing (different item), Wardbreaker.

## FORKS
1. Stored-spell CL and DC: default the storing caster's, as for any stored spell (unsourced here). 2. Delta vs full family: default delta over Reservoir T3. 3. GURPS chassis open: default Reservoir ER Battery plus Gadget, numbers pending the Basic Set.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### SPELLSTRIKE
**Weapon property — Magic Item Compendium, PDF p. 45 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
SPELLSTRIKE
[heading and price line lost to column interleave; name and +1 inferred from surrounding text, OCR-uncertain]
Property: Weapon
Caster Level: 8th
Aura: Moderate; (DC 19) abjuration
Activation: Free (mental)
A spellstrike weapon allows you to transfer some or all of the weapon's enhancement bonus, using it as a bonus on your saving throws against spells or spell-like abilities. As a free action, you choose how to allocate the weapon's enhancement bonus at the start of your turn before using the weapon, and the effect on saving throws lasts until the start of your next turn.
Prerequisites: Craft Magic Arms and Armor, resistance.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Property: Weapon; Caster Level: 8th; Aura: Moderate; (DC 19) abjuration; Activation: Free (mental); Prerequisites: Craft Magic Arms and Armor, resistance.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
allocate weapon bonus points to resistance rolls versus spells (the Defending mapping, OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp if the printed bonus is +1.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Defending (DMG) / Stalwart (Defensive 13-18).
DMG Defending (the same allocation pattern for AC); Stalwart (Defensive 13-18) is a fixed save bonus.

## FORKS
1. confirm the printed price against the book page.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: degraded.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- allocate weapon bonus points to resistance rolls versus spells (the Defending mapping, OPEN).


---

### STUNNING
**Weapon property — Magic Item Compendium, PDF p. 45 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
STUNNING [SYNERGY]
Price: +1 bonus
Property: Weapon
Caster Level: 9th
Aura: Moderate; (DC 19) enchantment
Activation: --
Synergy Prerequisite: Screaming
A stunning weapon functions as a screaming weapon (see page 42). In addition, on a successful critical hit with a stunning weapon, the target must succeed on a DC 17 Fortitude save or be stunned for 1 round.
Projectile weapons bestow this property on their ammunition.
Prerequisites: Craft Magic Arms and Armor, hold monster.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 9th; Aura: Moderate; (DC 19) enchantment; Activation: --; Synergy Prerequisite: Screaming; Prerequisites: Craft Magic Arms and Armor, hold monster.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

## GURPS 4e
Affliction (Stunned), Trigger critical, HT roll (percentages OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 on top of Screaming.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Dazing (Condition 17-24).
Dazing (Condition 17-24) is a 1/encounter Will daze; Screaming (batch 10) is the base. Delta = crit-triggered stun, fixed DC 17.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: degraded.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Affliction (Stunned), Trigger critical, HT roll (percentages OPEN).


---

### STUNNING SURGE
**Weapon property — Magic Item Compendium, PDF p. 45 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
STUNNING SURGE
Price: +1 bonus
Property: Weapon
Caster Level: 9th
Aura: Moderate; (DC 19) enchantment
Activation: Swift (command)
On a successful melee attack, you can command this weapon to emit a surge of magical energy. Unless the target succeeds on a Fortitude save (DC 10 + 1/2 your character level + your Cha modifier), it is stunned for [duration garbled in OCR; read as 1 round]. This ability is usable a number of times per day equal to 1 + your Charisma bonus (if any). Once you activate this ability, it can't be activated by any other creature until the following day.
Prerequisites: Craft Magic Arms and Armor, hold monster.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 9th; Aura: Moderate; (DC 19) enchantment; Activation: Swift (command); Prerequisites: Craft Magic Arms and Armor, hold monster.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; the DC and the uses scale with the wielder (stated; not flat-source).

## GURPS 4e
Affliction (Stunned) with an HT roll penalized by the wielder's level analogue, Limited Use (1 + Will-based Cha stand-in, OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: degraded.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Affliction (Stunned) with an HT roll penalized by the wielder's level analogue, Limited Use (1 + Will-based Cha stand-in, OPEN).


---

### STYGIAN
**Weapon property — Magic Item Compendium, PDF p. 45 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
STYGIAN
Price: +1 bonus
Property: Weapon
Caster Level: 9th
Aura: Moderate; (DC 19) necromancy
Activation: Swift (mental)
When you activate a stygian weapon, the next successful attack you make before the end of your turn bestows one negative level on the target in addition to dealing normal damage. This negative level lasts for 10 minutes, and thus can't result in a permanent level decrease. A stygian weapon functions three times per day.
Prerequisites: Craft Magic Arms and Armor, enervation.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 9th; Aura: Moderate; (DC 19) necromancy; Activation: Swift (mental); Prerequisites: Craft Magic Arms and Armor, enervation.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, 3/day. The negative level is the Energy Drained condition for 10 minutes; usable 3/day.

## GURPS 4e
Swift (mental) activation, 3/day. The next attack that lands before the end of your turn (it still has to beat the defender's 3d6 Parry/Block/Dodge contest as any attack) bestows one Energy Drained negative level for 10 minutes, on top of normal damage; no save printed, none added; never becomes level loss. Gadget chassis Breakable -25% / Can Be Stolen -10%; uncosted.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Enervating is crit-triggered; this is activated, no crit needed, no save printed).

## FORKS
1. no save printed (default as printed, limited by 3/day).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### SUNDERING
**Weapon property — Magic Item Compendium, PDF p. 45 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
SUNDERING
Price: +1 bonus
Property: Melee weapon
Caster Level: 5th
Aura: Faint; (DC 17) transmutation
Activation: --
A sundering weapon allows you to attack as if you have the Improved Sunder feat, and it deals an extra 1d6 points of damage on a sunder attempt.
Prerequisites: Craft Magic Arms and Armor, Improved Sunder, weapon of impact (SC 237) or metaphysical weapon (EPH 118).
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 5th; Aura: Faint; (DC 17) transmutation; Activation: --; Prerequisites: Craft Magic Arms and Armor, Improved Sunder, weapon of impact (SC 237) or metaphysical weapon (EPH 118).; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
the Sunder-equivalent technique at no penalty and +1d on damage against the object (technique names OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (DMG Mighty Cleaving is a different feat-extension).

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- the Sunder-equivalent technique at no penalty and +1d on damage against the object (technique names OPEN).


---

### SWEEPING
**Weapon property — Magic Item Compendium, PDF p. 45 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
SWEEPING
Price: +1 bonus
Property: Melee weapon
Caster Level: 5th
Aura: Faint; (DC 17) transmutation
Activation: --


This property grants you a +2 competence bonus on any Strength check made to trip an opponent with the weapon.
Prerequisites: Craft Magic Arms and Armor, bull's strength.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 5th; Aura: Faint; (DC 17) transmutation; Activation: --; Prerequisites: Craft Magic Arms and Armor, bull's strength.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
+2 on the Trip contest (OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Titan's Grip's staff reading gives trip, disarm and sunder bonuses on an oversize weapon).

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- +2 on the Trip contest (OPEN).


---

### THROWING
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 227 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Throwing: This ability can only be placed on a melee weapon. A melee weapon crafted with this ability gains a range increment of 10 feet and can be thrown by a wielder proficient in its normal use.
Faint transmutation; CL 5th; Craft Magic Arms and Armor, magic stone; Price +1 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Melee weapons only. Gains a 10-ft range increment and can be thrown by anyone proficient with it in melee. Attack and damage then follow the standard thrown-weapon rules (Str to damage, 5-increment maximum), which the fetched text does not restate. No return, no save, no SR, no d100. Does not include Returning (a separate SRD ability).

## GURPS 4e
mechanism is a Gadget that gives the weapon a thrown profile (Range, Accuracy) so it can be used with Throwing skill without the improvised-throw penalties. I could not verify the Basic Set thrown-weapon numbers, so the range and Acc values, any skill modifier, and the point cost are open. Gadget limitations -35% (Breakable -25%, Can Be Stolen -10%) apply to whatever trait is chosen.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none in Part 1 pools. The Siege aspect (Part 3, 24E: "Melee attack gains 30/60/100 ft range") is a different layer and a different range. Gap: nothing grants a thrown profile to a melee weapon.

## NAME COLLISION
3.5 "Throwing" weapon property words (throwing axe), SRD Returning, Distance, Siege aspect.

## FORKS
1. Whether the weapon comes back: default no, Returning is a separate ability. 2. Thrown damage uses Str: default the standard rule. 3. GURPS range/Acc numbers: open, take from the Basic Set thrown-weapon table.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### THUNDERING
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 226 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Thundering: A thundering weapon creates a cacophonous roar like thunder upon striking a successful critical hit. The sonic energy does not harm the wielder. A thundering weapon deals an extra 1d8 points of sonic damage on a successful critical hit. If the weapon's critical multiplier is x3, add an extra 2d8 points of sonic damage instead, and if the multiplier is x4, add an extra 3d8 points of sonic damage. Bows, crossbows, and slings so crafted bestow the sonic energy upon their ammunition. Subjects dealt a critical hit by a thundering weapon must make a DC 14 Fortitude save or be deafened permanently.
Faint necromancy; CL 5th; Craft Magic Arms and Armor, blindness/deafness; Price +1 bonus,
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** On a confirmed critical hit, +1d8 sonic (x2), +2d8 (x3), +3d8 (x4), not multiplied by the crit (unstated; implied by the ladder). Target makes Fortitude DC 14 (fixed) or is deafened permanently. No SR stated. Instant, no action. Immune: creatures immune to crits, sonic, or deafness. No d100 (crit-triggered). No healing interaction with Fatal Wound.

## GURPS 4e
Innate Attack (Crushing [Sonic]) Follow-Up +0%, triggered on a critical hit, plus an Affliction (Deafness) rider resisted by HT; Gadget -35% (Breakable -25%, Can Be Stolen -10%). Crit-only limitation percentage, the HT penalty equivalent to Fort DC 14, and the permanent-duration modifier: all open. Dice read as-is: 1d8 / 2d8 / 3d8 by multiplier class. Points: not computable.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Stormborn (Elemental 51-56), Lethal Focus (Offensive 31-36), Blinding (Condition 43-48).
none that matches. Stormborn (Elemental 51-56) is an every-hit sonic+lightning split; Lethal Focus (Offensive 31-36) is untyped crit dice; Blinding (Condition 43-48) is the nearest crit-triggered condition (blind 1 round). Gap: crit-only sonic dice on a multiplier ladder plus a permanent-deafness save.

## NAME COLLISION
SRD Thundering vs Stormborn (thunder flavor), Silencing (Mute), Elemental Burst; no Registry name "Thundering".

## FORKS
1. "Permanently" deaf: default as written; curable by remove blindness/deafness, heal or regeneration (default, not sourced). 2. Shocking Burst delta and Thundering share a crit-ladder engine: default one shared "crit-burst" rule text. 3. GURPS multiplier mapping, as in Shocking Burst: default by the 3.5e weapon's multiplier.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### UNHOLY SURGE
**Weapon property — Magic Item Compendium, PDF p. 46 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
UNHOLY SURGE [SYNERGY]
Price: +1 bonus
Property: Melee weapon
Caster Level: 11th
Aura: Moderate; (DC 20) evocation
Activation: -- and swift (command)
Synergy Prerequisite: Unholy
This weapon functions as an unholy weapon (DMG 226). This is a continuous effect and requires no activation. In addition, on a successful melee attack with an unholy surge weapon, you can command it to emit a burst of unholy energy, which deals an extra 3d6 points of damage to a good-aligned target. If used against a non-good creature, it deals no additional damage, and that use of the ability is wasted. This ability is usable a number of times per day equal to 1 + your Cha bonus (if any). Once you activate this property, it can't be activated by any other creature until the following day.
Prerequisites: Craft Magic Arms and Armor, unholy blight or unholy word.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 11th; Aura: Moderate; (DC 20) evocation; Activation: -- and swift (command); Synergy Prerequisite: Unholy; Prerequisites: Craft Magic Arms and Armor, unholy blight or unholy word.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Mirror of Holy Surge: read holy as unholy, 'evil target' as 'good-aligned target'; synergy prerequisite is Unholy; same 1 + Cha bonus uses per day, no other change. as printed; scales with Cha bonus for uses (stated).

## GURPS 4e
Holy's Follow-Up plus a 3d6 burst, Limited Use (1 + Will-based Cha stand-in, OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 on top of Holy.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Unholy (DMG).
DMG Holy (see that file) plus the Energy Surge on-demand burst pattern.

## FORKS
shared alignment-tag ruling.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Holy's Follow-Up plus a 3d6 burst, Limited Use (1 + Will-based Cha stand-in, OPEN).


---

### VENOMOUS
**Weapon property — Magic Item Compendium, PDF p. 46 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
VENOMOUS
Price: +1 bonus
Property: Weapon
Caster Level: 9th
Aura: Moderate; (DC 19) necromancy
Activation: Swift (command)
When activated, a venomous weapon coats itself in injury poison (Fort DC 14, 1d4 Str/1d4 Str), which lasts for 1 minute or until your next successful attack with the weapon, whichever comes first. A venomous weapon functions three times per day.
Projectile weapons bestow this property on their ammunition.
Prerequisites: Craft Magic Arms and Armor, poison.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 9th; Aura: Moderate; (DC 19) necromancy; Activation: Swift (command); Prerequisites: Craft Magic Arms and Armor, poison.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, fixed DC 14, poison immunities apply.

## GURPS 4e
Innate Attack (Toxic) as a Follow-Up poison with a HT roll and an ST-loss effect (modifiers OPEN), Limited Use 3/day.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: none (pool 'Venomous' is a different affix; names stay).
NAME COLLISION with the pool "Venomous" (Elemental 33-38: +1d4/+1d6/+1d8/+2d6/+3d6 poison damage; Fort DC 12/14/16/18/22 or sickened; IA Toxic, Follow-Up, Cyclic). The printed one delivers a poison that does ability damage. Delta = the payload and the 3/day, 1-minute window.

## FORKS
1. names stay, never merge (Fatal Wound precedent).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Innate Attack (Toxic) as a Follow-Up poison with a HT roll and an ST-loss effect (modifiers OPEN), Limited Use 3/day.


---

### VICIOUS
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 227 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Vicious: When a vicious weapon strikes an opponent, it creates a flash of disruptive energy that resonates between the opponent and the wielder. This energy deals an extra 2d6 points of damage to the opponent and 1d6 points of damage to the wielder. Only melee weapons can be vicious.
Moderate necromancy; CL 9th; Craft Magic Arms and Armor, enervation; Price +1 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Melee weapons only. On each hit that deals damage, +2d6 to the opponent and 1d6 to the wielder, both untyped, not multiplied on a crit (unstated; default), no save, no SR, no d100 (printed trigger is every strike, not a proc). Undead/constructs: the wielder still takes the 1d6 (the text has no exception). Does not heal anyone; no Fatal Wound interaction.

## GURPS 4e
Innate Attack Follow-Up +0%, 2d6 to the opponent and 1d6 back to the wielder (dice read as-is). Gadget Breakable -25% + Can Be Stolen -10% = -35%. The percentage for damage to the user, and the mapping of "hurts the wielder" onto a limitation, are open (not retrieved). Points: not computable.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Wounding (Offensive 07-12), Berserker (Offensive 61-66).
none that matches. Wounding (Offensive 07-12) is plain bonus damage with no self-cost; Berserker (Offensive 61-66) trades AC; Blood Price Engine (Rare 31-40) and the Blood Pact temper (23I-9) are HP-cost mechanics of a different shape. Gap: every-hit target damage paired with every-hit wielder damage.

## NAME COLLISION
Blood Price Engine, Blood Pact, Berserker; the word "vicious" is also general weapon flavor text.

## FORKS
1. Trigger on any hit vs only damage past DR: default only a hit that deals damage past DR (matches proc conventions), then the 2d6 joins that damage and the 1d6 hits the wielder. 2. Can the wielder's 1d6 be reduced by DR/resist: default no, untyped and unreducible. 3. GURPS self-damage limitation percentage: open.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.


---

### WEAKENING
**Weapon property — Magic Item Compendium, PDF p. 47 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
WEAKENING
Price: +1 bonus
Property: Weapon
Caster Level: 5th
Aura: Faint; (DC 17) necromancy
Activation: --
When you score a critical hit with a weakening weapon, the target takes a -4 penalty to its Strength score (to a minimum score of 1) for 10 minutes. Multiple strikes aren't cumulative.
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, ray of enfeeblement.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 5th; Aura: Faint; (DC 17) necromancy; Activation: --; Prerequisites: Craft Magic Arms and Armor, ray of enfeeblement.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, no save (flagged), no stacking.

## GURPS 4e
Affliction (ST penalty) Trigger critical (percentages OPEN), -2 ST at the 2:1 conversion.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: none (pool 'Weakening' is a different affix; names stay).
NAME COLLISION with the pool "Weakening" (Condition 37-42): on hit -1/-1/-2/-3/-4 Str for 1d4 rounds, Fortitude save; the printed one is crit-triggered, -4 for 10 minutes, no save. The T1 value matches the magnitude only.

## FORKS
1. names stay, never merge (Fatal Wound precedent); 2. no save printed (default as printed, crit-only).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Affliction (ST penalty) Trigger critical (percentages OPEN), -2 ST at the 2:1 conversion.


---

### WHIRLING
**Weapon property — Magic Item Compendium, PDF p. 47 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
WHIRLING
Price: +1 bonus
Property: Slashing melee weapon
Caster Level: 11th
Aura: Moderate; (DC 20) transmutation
Activation: Full-round (mental)
Three times per day, you can use this weapon to make a whirling attack that has a chance of striking all nearby opponents. Instead of making your regular attacks, you instead make one melee attack at your full attack bonus against each opponent within reach of the weapon. This property otherwise functions like the Whirlwind Attack feat.
Prerequisites: Craft Magic Arms and Armor, haste.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Slashing melee weapon; Caster Level: 11th; Aura: Moderate; (DC 20) transmutation; Activation: Full-round (mental); Prerequisites: Craft Magic Arms and Armor, haste.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, 3/day.

## GURPS 4e
a single All-Out-style attack against every adjacent foe, one roll each at full skill, Limited Use 3/day (the modifier set, and whether it needs a Whirlwind-like technique, OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Rapid Assault adds an extra attack; Cleave Through chains on kills).

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- a single All-Out-style attack against every adjacent foe, one roll each at full skill, Limited Use 3/day (the modifier set, and whether it needs a Whirlwind-like technique, OPEN).


---

## COVERED BY AN EXISTING REGISTRY POOL ROW (no second document)

| Affix | Source | Existing row |
|---|---|---|
| Charging | MIC, PDF p. 32 | Devastating Charge (Offensive 91-96) |
| Consumptive | MIC, PDF p. 32 | Shadowtouch (Elemental 39-44) |
| Corrosive | MIC, PDF p. 32 | Corroding (Elemental 25-32) |
| Deadly Precision | MIC, PDF p. 33 | Sneak's Edge (Skill/Class 13-18) |
| Dispelling | MIC, PDF p. 34 | Dispelling Strike (Condition 85-90) |
| Dispelling, Greater | MIC, PDF p. 34 | Dispelling Strike (Condition 85-90) |
| Flaming | DMG v3.5, PDF p. 225 | Flaming (Elemental 01-08) |
| Frost | DMG v3.5, PDF p. 225 | Freezing (Elemental 09-16) |
| Impact | MIC, PDF p. 38 | Keen Edge (Offensive 13-18) |
| Keen | DMG v3.5, PDF p. 226 | Keen Edge (Offensive 13-18) |
| Knockback | MIC, PDF p. 39 | Knockback (Condition 49-54) |
| Lucky | MIC, PDF p. 39 | Battle Meditation (Skill/Class 85-90) |
| Maiming | MIC, PDF p. 39 | Lethal Focus (Offensive 31-36) |
| Shock | DMG v3.5, PDF p. 226 | Shocking (Elemental 17-24) |
| Speed | DMG v3.5, PDF p. 226 | Rapid Assault (Offensive 25-30) |
| Vanishing | MIC, PDF p. 46 | Phasewalk (Utility 37-42) |
| Warning | MIC, PDF p. 47 | Timesense (Utility fragment 97-100) |

## BLOCKED — INACTIVE (psionic or incarnum; no such character in the campaign)

- Manifester (MIC, PDF p. 39)
- Mindcrusher (MIC, PDF p. 40)
- Mindfeeder (MIC, PDF p. 40)
- Power Storing (MIC, PDF p. 41)
- Psibane (MIC, PDF p. 42)
- Psychic (MIC, PDF p. 42)
- Psychokinetic (MIC, PDF p. 42)
- Psychokinetic Burst (MIC, PDF p. 42)
- Soulbound (MIC, PDF p. 44)
- Soulbound, Greater (MIC, PDF p. 44)

## OPEN VERIFICATION ITEMS

- Brilliant Energy: 2 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Dancing: source figure OCR-doubtful (see packet header); check the book page
- Dancing: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Prismatic Burst: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Body Feeder: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Cursespewing: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Ethereal Reaver: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Implacable: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Necrotic Focus: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Aquan: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Auran: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Banishing: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Blindsighted: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Blurstrike: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Collision: 2 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Disarming: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Disruption: 2 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Domineering: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Doom Burst: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Energy Aura: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Flaming Burst: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Fleshgrinding: 2 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Force: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Icy Burst: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Ignan: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Illusion Theft: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Impedance: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Metalline: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Paralytic Burst: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Terran: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Transmuting: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Vampiric: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Aquatic: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Arcane Might: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Berserker: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Binding: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Bloodfeeding: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Bloodstone: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Brash: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Brutal Surge: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Changeling: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Chargebreaker: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Defensive Surge: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Desiccating Burst: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Dislocator: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Dislocator, Great: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Distance: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Divine Wrath: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Dragonhunter: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Eager: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Everbright: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Ghost Strike: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Ghost Touch: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Harmonizing: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Heavenly Burst: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Hideaway: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Holy Surge: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Hunting: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Illusion Bane: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Impaling: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Incorporeal Binding: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Ki Focus: source figure OCR-doubtful (see packet header); check the book page
- Ki Focus: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Magebane: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Merciful: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Mighty Cleaving: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Mighty Smiting: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Morphing: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Paralyzing: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Precise: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Profane: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Quick Loading: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Resounding: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Returning: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Sacred: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Seeking: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Shadowstrike: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Shattermantle: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Shielding: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Sizing: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Soulbreaker: source figure OCR-doubtful (see packet header); check the book page
- Soulbreaker: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Souldrinking: source figure OCR-doubtful (see packet header); check the book page
- Souldrinking: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Spellstrike: source figure OCR-doubtful (see packet header); check the book page
- Spellstrike: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Stunning: source figure OCR-doubtful (see packet header); check the book page
- Stunning: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Stunning Surge: source figure OCR-doubtful (see packet header); check the book page
- Stunning Surge: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Sundering: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Sweeping: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Unholy Surge: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Venomous: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Weakening: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
- Whirling: 1 GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)
