# ARCANE MIGHT
**Weapon property — Magic Item Compendium, PDF p. 29 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
ARCANE MIGHT
Price: +1 bonus
Property: Bows (not crossbows)
Caster Level: 15th
Aura: Strong; (DC 22) transmutation
Activation: Swift (mental)
You can channel the energy of your arcane spells through this bow to make the arrows fired from it more damaging. As a swift action, you can sacrifice a prepared arcane spell from memory (or an unused spell slot if you are a spontaneous arcane caster). Doing so grants a bonus equal to the sacrificed spell's level on the next damage roll you make with the bow that turn.
Prerequisites: Craft Magic Arms and Armor, greater magic weapon.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Bows (not crossbows); Caster Level: 15th; Aura: Strong; (DC 22) transmutation; Activation: Swift (mental); Prerequisites: Craft Magic Arms and Armor, greater magic weapon.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; bonus equals sacrificed spell level; one use per swift action.

## GURPS 4e
the campaign's casting resource is Energy Reserve; sacrifice ER for a damage bonus. The ER-per-spell-level exchange is OPEN (the translator rule 1 ER = about 5 mana is a rough guide, unverified here).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Reservoir stores a spell; Cost Reduction trades cost).

## FORKS
1. cap per round (default one swift activation per round, per the swift action).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- The ER-per-spell-level exchange is OPEN (the translator rule 1 ER = about 5 mana is a rough guide, unverified here).
