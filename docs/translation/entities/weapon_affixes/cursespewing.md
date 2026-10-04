# CURSESPEWING
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
