# KI FOCUS
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 226 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Ki Focus: The magic weapon serves as a channel for the wielder's ki, allowing her to use her special ki attacks through the weapon as if they were unarmed attacks. These attacks include the monk's stunning attack, ki strike, and quivering palm, as well as the Stunning Fist feat. Only melee weapons can have the ki focus ability.
Moderate transmutation; CL sth; Craft Magic Arms and Armor, creator must be a monk; Price +1 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** the wielder may deliver stunning attack, ki strike, quivering palm and Stunning Fist through the weapon exactly as through an unarmed strike. The abilities keep their own saves and DCs. Melee weapons only. No SR of its own, no healing interaction.

## GURPS 4e
no monk class; the mechanism is that any ability normally limited to bare-handed delivery may be delivered through the weapon. Chassis Gadget (Breakable -25%, Can Be Stolen -10%). The trait that expresses this (a limitation removal on the delivered ability) and its cost are OPEN; no point total stated.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed +1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none. The Skill/Class pool has martial rows (Weapon Mastery, Commander's Voice, Battle Meditation, Signature Move) but nothing for unarmed-only class abilities.

## NAME COLLISION
none in the Registry; the SRD class feature "ki strike" is the thing being delivered.

## FORKS
1. Does the weapon's own damage still apply when a ki attack is delivered through it? Default: the ki ability's effect applies and the weapon's damage is unchanged (the text says "as if unarmed", which does not say damage is lost).
2. Which GURPS abilities count as the monk's ki attacks. Default: the campaign's monk-equivalent techniques named at ratification; none is assumed here.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: degraded.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- The trait that expresses this (a limitation removal on the delivered ability) and its cost are OPEN;
