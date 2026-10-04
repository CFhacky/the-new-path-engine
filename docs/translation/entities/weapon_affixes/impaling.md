# IMPALING
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
