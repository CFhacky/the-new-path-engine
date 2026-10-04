# VENOMOUS
**Weapon property — Magic Item Compendium, PDF p. 46 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
VENOMOUS
Price: +1 bonus
Property: Weapon
Caster Level: 9th
Aura: Moderate; (DC 19) necromancy
Activation: Swift (command)
When activated, a venomous weapon coats itself in injury poison (Fort DC 14, 1d4 Str/1d4 Str), which lasts for 1 minute or until your next successful attack with the weapon, whichever comes first. A venomous weapon functions three times per day.
Projectile weapons bestow this property on their ammunition.
Prerequisites: Craft Magic Arms and Armor, poison.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 9th; Aura: Moderate; (DC 19) necromancy; Activation: Swift (command); Prerequisites: Craft Magic Arms and Armor, poison.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, fixed DC 14, poison immunities apply.

## GURPS 4e
Innate Attack (Toxic) as a Follow-Up poison with a HT roll and an ST-loss effect (modifiers OPEN), Limited Use 3/day.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: none (pool 'Venomous' is a different affix; names stay).
NAME COLLISION with the pool "Venomous" (Elemental 33-38: +1d4/+1d6/+1d8/+2d6/+3d6 poison damage; Fort DC 12/14/16/18/22 or sickened; IA Toxic, Follow-Up, Cyclic). The printed one delivers a poison that does ability damage. Delta = the payload and the 3/day, 1-minute window.

## FORKS
1. names stay, never merge (Fatal Wound precedent).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Innate Attack (Toxic) as a Follow-Up poison with a HT roll and an ST-loss effect (modifiers OPEN), Limited Use 3/day.
