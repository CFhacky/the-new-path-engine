# DESICCATING BURST
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
