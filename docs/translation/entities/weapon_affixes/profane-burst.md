# PROFANE BURST
**Weapon property — Magic Item Compendium, PDF p. 41 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
PROFANE BURST [SYNERGY]
Price: +1 bonus
Property: Weapon
Caster Level: 12th
Aura: Strong; (DC 21) necromancy
Activation: Standard (command) and --
Synergy Prerequisite: Profane
A profane burst weapon functions as a profane weapon (see above). In addition, the weapon explodes with negative energy on a successful critical hit, dealing extra negative energy damage as set out in the table below. (This effect activates even if the target is not normally subject to extra damage from critical hits.) A profane burst weapon deals even more damage to good outsiders on a successful critical hit. This burst does not harm you or any creature other than the target if you are undead; otherwise, you take 1d4 points of Constitution damage (or Charisma damage if you have no Constitution score). This is a continuous effect and requires no activation. Even if the weapon has not been activated to deal extra damage because of the profane property, the weapon still deals its extra negative energy damage on a successful critical hit.


Critical Multiplier / Extra Damage / Good Outsider Extra Damage: x2 1d10 2d10; x3 2d10 4d10; x4 3d10 6d10
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, inflict critical wounds.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 12th; Aura: Strong; (DC 21) necromancy; Activation: Standard (command) and --; Synergy Prerequisite: Profane; Prerequisites: Craft Magic Arms and Armor, inflict critical wounds.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** crit dice by multiplier class (default 1d / 2d / 3d, doubled vs good outsiders), self-damage 1d4 Con per burst.

## GURPS 4e
crit dice by multiplier class (default 1d / 2d / 3d, doubled vs good outsiders), self-damage 1d4 Con per burst.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 on top of Profane.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Profane (MIC).
Profane (above) plus the burst template (Icy Burst). Delta = the crit rider and the wielder's per-burst cost.

## FORKS
none (the weapon's own 3.5e crit multiplier applies).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.
