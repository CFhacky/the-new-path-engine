# DRAGONHUNTER
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
