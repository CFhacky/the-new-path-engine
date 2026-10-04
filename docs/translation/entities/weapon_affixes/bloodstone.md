# BLOODSTONE
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
