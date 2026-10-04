# SLOW BURST
**Weapon property — Magic Item Compendium, PDF p. 44 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price 5,000 gp (flat))

## SOURCE (verbatim, see packet header for normalization)
```
SLOW BURST
Price: +5,000 gp
Property: Weapon
Caster Level: 5th
Aura: Faint; (DC 17) transmutation
Activation: --
A chill aura numbs this weapon's victim when you strike true. Whenever you score a critical hit with this weapon, the target is slowed (as the slow spell) for 3 rounds (Will DC 14 negates). This effect activates even if the creature struck is not normally subject to extra damage from critical hits.
Prerequisites: Craft Magic Arms and Armor, slow.
Cost to Create: 2,500 gp, 200 XP, 5 days.
```

## D&D 3.5e
**Printed header:** Price: +5,000 gp; Property: Weapon; Caster Level: 5th; Aura: Faint; (DC 17) transmutation; Activation: --; Prerequisites: Craft Magic Arms and Armor, slow.; Cost to Create: 2,500 gp, 200 XP, 5 days.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** As printed: on a critical hit the target is slowed (as the slow spell) for 3 rounds, Will DC 14 negates, even against crit-immune targets. Price printed 5,000 gp flat.

## GURPS 4e
On a confirmed crit (undefended) the target resists with a Quick Contest of Will against effective skill 14 (the printed DC); on failure Affliction (Reduced Move, the Slowing-row mechanism) for 3 turns. Gadget chassis Breakable -25% / Can Be Stolen -10%; uncosted.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed 5,000 gp flat.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Slowing (Condition 01-08).
Slowing (Condition 01-08): on hit 1/encounter, slow 1 round, DC 12/14/16/18/22 (the printed DC 14 matches T4), GURPS Affliction (Reduced Move). Delta = crit trigger and 3-round duration.

## FORKS
1. save type: the pool's Slowing uses Fortitude, the printed Slow Burst Will; default as printed (Will).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.
