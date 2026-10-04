# SHATTERMANTLE
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
