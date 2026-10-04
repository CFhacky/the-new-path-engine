# AURAN
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
