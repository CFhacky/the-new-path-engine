# GHOST TOUCH
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 225 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Ghost Touch: A ghost touch weapon deals damage normally against incorporeal creatures, regardless of its bonus. (An incorporeal creature's 50% chance to avoid damage does not apply to attacks with ghost touch weapons.) The weapon can be picked up


and moved by an incorporeal creature at any time. A manifesting ghost can wield the weapon against corporeal foes. Essentially, a ghost touch weapon counts as either corporeal or incorporeal at any given time, whichever is more beneficial to the wielder.
Moderate conjuration; CL 9th; Craft. Magic Arms and Armor, plane shift; Price +1 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** attacks with the weapon ignore the incorporeal 50% miss chance and deal full damage at any item tier; an incorporeal creature may pick up, move and wield the weapon (against corporeal foes too); the weapon counts as corporeal or incorporeal, wielder's choice each turn. No save, no SR.

## GURPS 4e
Gadget (Breakable -25%, Can Be Stolen -10%); the weapon's attacks gain Affects Insubstantial (the pool already uses this trait at T3+). Enhancement percentage for Affects Insubstantial on a weapon attack: OPEN (not in the repo indices); no point total stated. Incorporeal wielding is a mechanism note with no point cost.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed +1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Penetrating Strikes (Offensive 85-90).
Penetrating Strikes (Offensive 85-90): GURPS "Affects Insubstantial at T3+"; 3.5e lists material bypass only. Gap: the pool row works at T3+ only, carries no 50%-miss clause, and has no incorporeal-wielder or dual-status clause.

## NAME COLLISION
Penetrating Strikes (pool, redundant at T3+); SRD ghost touch armor property.

## FORKS
1. Ghost Touch plus Penetrating Strikes on one weapon is redundant above T3. Default: allowed, no stacking benefit.
2. "Whichever is better" on the same swing. Default: wielder declares at the start of each turn.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Enhancement percentage for Affects Insubstantial on a weapon attack: OPEN (not in the repo indices);
