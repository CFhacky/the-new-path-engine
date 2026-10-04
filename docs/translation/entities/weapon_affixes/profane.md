# PROFANE
**Weapon property — Magic Item Compendium, PDF p. 41 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
PROFANE
Price: +1 bonus
Property: Weapon
Caster Level: 7th
Aura: Moderate; (DC 17) necromancy
Activation: Standard (command)
By speaking the appropriate command word, you can sheathe a profane weapon in crackling black negative energy. If you have no Constitution score, this energy does not harm you; otherwise you take 1 point of Constitution damage for each round that you hold the weapon while the effect is activated. This effect lasts until you speak another command word to end it. While activated, a profane weapon deals an extra 1d6 points of damage to any living target (or 2d6 points against a good outsider) on a successful hit. Also, it is treated as evil-aligned for the purpose of overcoming damage reduction.
Projectile weapons bestow this property upon their ammunition.
Prerequisites: Craft Magic Arms and Armor, inflict light wounds.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 7th; Aura: Moderate; (DC 17) necromancy; Activation: Standard (command); Prerequisites: Craft Magic Arms and Armor, inflict light wounds.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed. The wielder's cost is a drawback (stated, per round while active).

## GURPS 4e
Innate Attack Follow-Up 1d6 (2d6 vs good outsiders), Costs Fatigue or HP drain per turn on the wielder (modifier OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Shadowtouch (Elemental 39-44).
Shadowtouch (Elemental 39-44, +1d6 negative energy at T4; undead take half) is the damage half. Delta = the evil-DR tag, the 2d6 vs good outsiders, and the wielder's Constitution cost.

## FORKS
1. the Constitution cost: default keep as printed (it is the property's price for its low +1).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Innate Attack Follow-Up 1d6 (2d6 vs good outsiders), Costs Fatigue or HP drain per turn on the wielder (modifier OPEN).
