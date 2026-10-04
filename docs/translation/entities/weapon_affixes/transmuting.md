# TRANSMUTING
**Weapon property — Magic Item Compendium, PDF p. 46 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
TRANSMUTING
Price: +2 bonus
Property: Weapon
Caster Level: 13th
Aura: Strong; (DC 21) transmutation
Activation: --
When you score a successful hit with a transmuting weapon against a creature that has damage reduction, that attack is resolved normally. At the start of your next turn, however, the weapon transforms, taking on the properties required to overcome that creature's damage reduction. Once so changed, the weapon overcomes the designated type of damage reduction for 10 rounds, or until you strike a creature that has a different type of damage reduction. In this case, the weapon transforms in the same manner to overcome that damage reduction instead. If the target has multiple types of damage reduction, the weapon overcomes all of them. If the creature gains a new type of damage reduction after initially being struck (from changing its form, for example), the weapon must change again before it can overcome the new type. A transmuting weapon does not gain any other benefit of the properties it takes on, and it always deals normal damage.
Prerequisites: Craft Magic Arms and Armor, fabricate.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 13th; Aura: Strong; (DC 21) transmutation; Activation: --; Prerequisites: Craft Magic Arms and Armor, fabricate.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed.

## GURPS 4e
after the first hit the weapon's Armor Divisor or material tag matches the target's DR type for 10 seconds (OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Penetrating Strikes (Offensive 85-90).
Penetrating Strikes (Offensive 85-90) at T1 covers all materials and alignments; Metalline (batch 07) is a chosen material. Delta = automatic adaptation after the first hit.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- after the first hit the weapon's Armor Divisor or material tag matches the target's DR type for 10 seconds (OPEN).
