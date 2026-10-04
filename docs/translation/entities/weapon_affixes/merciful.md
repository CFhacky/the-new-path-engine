# MERCIFUL
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 226 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Merciful: The weapon deals an extra 1d6 points of damage, and all damage it deals is nonlethal damage. On command, the weapon suppresses this ability until commanded to resume it. Bows, crossbows, and slings so crafted bestow the merciful effect upon their ammunition.
Faint conjuration; CL 5th; Craft Magic Arms and Armor, cure light wounds; Price +1 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** on each damaging hit the weapon adds +1d6 untyped damage, and all damage from the weapon (base and extra) is nonlethal. Command word suppresses and resumes the ability. No save, no SR. No healing interaction.

## GURPS 4e
chassis Gadget (Breakable -25%, Can Be Stolen -10%). Extra damage = Innate Attack, Follow-Up +0%, 1d6 (dice read as-is), Magical -10%. Nonlethal delivery means the damage is taken as FP loss rather than HP; the trait and its modifier for that are OPEN, so no point total is stated.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed +1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Life Shield and Second Wind are healing, not nonlethal delivery).

## NAME COLLISION
none in the Registry; SRD merciful special ability is this one.

## FORKS
1. Does the extra 1d6 stay when the ability is suppressed? Default: no, suppression turns off both the extra damage and the nonlethal conversion.
2. Does the nonlethal conversion also cover the base weapon damage in GURPS? Default: yes, to match the printed "all damage".

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- the trait and its modifier for that are OPEN, so no point total is stated.
