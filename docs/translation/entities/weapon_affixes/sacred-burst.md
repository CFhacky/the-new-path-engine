# SACRED BURST
**Weapon property — Magic Item Compendium, PDF p. 43 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
SACRED BURST [SYNERGY]
Price: +1 bonus
Property: Weapon
Caster Level: 12th
Aura: Strong; (DC 21) conjuration
Activation: --
Synergy Prerequisite: Sacred
A sacred burst weapon functions as a sacred weapon (see above). In addition, the weapon explodes with positive energy on a successful critical hit, dealing extra positive energy damage to creatures as set out in the table below. (This effect activates even if the target is not normally subject to extra damage from critical hits.) A sacred burst weapon deals even more damage to evil outsiders on a successful critical hit. This burst does not harm you or any creature other than the target unless you are undead; if you are, you take 1d4 points of Charisma damage from the burst. This is a continuous effect and requires no activation. Even if the weapon has not been activated to deal extra damage because of the sacred property, the weapon still deals its extra positive energy damage on a successful critical hit.
Critical Multiplier / Extra Damage / Evil Outsider Extra Damage: x2 1d10 2d10; x3 2d10 4d10; x4 3d10 6d10
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, cure critical wounds.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 12th; Aura: Strong; (DC 21) conjuration; Activation: --; Synergy Prerequisite: Sacred; Prerequisites: Craft Magic Arms and Armor, cure critical wounds.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** As printed over Sacred: on a critical hit, extra positive-energy damage by the weapon's own multiplier class (x2 1d10, x3 2d10, x4 3d10; evil outsider 2d10 / 4d10 / 6d10), even against crit-immune targets; only the target is harmed unless you are undead (then 1d4 Cha damage to you); continuous.

## GURPS 4e
Rider on a confirmed crit (undefended): dice by multiplier class 1d / 2d / 3d, doubled against an evil outsider, ignoring worn DR; works against crit-immune targets; undead wielder takes 1d4 Cha as the burst cost. Gadget chassis Breakable -25% / Can Be Stolen -10%; uncosted.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 on top.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Sacred (MIC).


## FORKS
shared burst fork.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.
