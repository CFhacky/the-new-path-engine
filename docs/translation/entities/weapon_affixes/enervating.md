# ENERVATING
**Weapon property — Magic Item Compendium, PDF p. 35 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
ENERVATING
Price: +2 bonus
Property: Weapon
Caster Level: 11th
Aura: Moderate; (DC 20) necromancy
Activation: --
When you score a critical hit against a living creature with an enervating weapon, the weapon bestows one negative level on the target. Assuming the subject survives, it regains lost levels after 1 hour. Usually, negative levels have a chance of permanently draining a victim's levels, but the negative levels from the enervating property don't last long enough to do so.
Prerequisites: Craft Magic Arms and Armor, enervation.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 11th; Aura: Moderate; (DC 20) necromancy; Activation: --; Prerequisites: Craft Magic Arms and Armor, enervation.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, no save printed (flagged), crit-only, one level per crit (stacks per crit, each recovers after its own hour). The negative level is the Energy Drained condition for 1 hour (engine).

## GURPS 4e
Trigger: a confirmed critical hit on a living creature (crits are undefended, so no defender 3d6 roll). Effect: one Energy Drained negative level (-1 attacks/saves/skills/ability checks, -5 HP, -1 effective level); no save printed, none added. Fades after 1 hour; never becomes level loss. Repeated crits add one level each, additive. Gadget chassis Breakable -25% / Can Be Stolen -10%; uncosted.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Weakening and Exhaustion are narrower).

## FORKS
1. stacking of repeated crits (default additive, never multiplicative; cap none printed).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.
