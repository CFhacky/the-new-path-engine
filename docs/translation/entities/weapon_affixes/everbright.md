# EVERBRIGHT
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
