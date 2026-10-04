# WEAKENING
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
