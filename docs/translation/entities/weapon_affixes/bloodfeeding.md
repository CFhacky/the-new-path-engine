# BLOODFEEDING
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
