# ACIDIC BURST
**Weapon property — Magic Item Compendium, PDF p. 29 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
ACIDIC BURST [SYNERGY]
Price: +1 bonus
Property: Weapon
Caster Level: 12th
Aura: Strong; (DC 21) conjuration
Activation: Standard (command) and --
Synergy Prerequisite: Corrosive
An acidic burst weapon functions as a corrosive weapon (see page 31). In addition, the weapon automatically showers an opponent with acid upon a successful critical hit, dealing extra acid damage as set out on the table below. This acid does not harm you or any creature other than the target. This is a continuous effect and requires no activation. Even if the weapon has not been activated to deal the extra 1d6 points of acid damage that comes from the corrosive property, the weapon still deals its extra acid damage on a successful critical hit.
Critical Multiplier / Extra Acid Damage: x2 1d10; x3 2d10; x4 3d10
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, Melf's acid arrow.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 12th; Aura: Strong; (DC 21) conjuration; Activation: Standard (command) and --; Synergy Prerequisite: Corrosive; Prerequisites: Craft Magic Arms and Armor, Melf's acid arrow.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** on a confirmed crit, extra acid damage 1d10 / 2d10 / 3d10 by multiplier class (not multiplied again).

## GURPS 4e
Innate Attack (Corrosion), Follow-Up +0%, Trigger critical, dice default 1d / 2d / 3d.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 on top of Corrosive (printed synergy price).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Corroding (Elemental 25-32).
Corroding (Elemental 25-32) is the acid half. Delta = crit rider only (same shape as DMG Icy Burst).

## FORKS
Engine ruling: the weapon's own 3.5e crit multiplier applies.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.
