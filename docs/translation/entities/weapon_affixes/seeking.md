# SEEKING
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 226 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Seeking: Only ranged weapons can have the seeking ability. The weapon veers toward its target, negating any miss chances that would otherwise apply, such as from concealment. (The wielder still has to aim the weapon at the right square. Arrows mistakenly shot into an empty space, for example, do not veer and hit invisible enemies, even if they are nearby.)
Strong divination; CL 12th; Craft Magic Arms and Armor, true seeing, Price +1 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** ranged attacks with the weapon ignore miss chances that would otherwise apply, such as from concealment; the wielder must still target the correct square. Ammunition weapons confer the property. No save, no SR.

## GURPS 4e
negate vision and concealment attack penalties for the weapon's attacks, still requiring the correct target. Nearest baked modifier is Homing +50% (tracking attacks, from the exchange-rate table); whether it fits a weapon attack that is not an Innate Attack is OPEN, so no point total is stated. Chassis Gadget (Breakable -25%, Can Be Stolen -10%).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed +1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none. Hunter's Mark (bonus damage vs a marked target), Precise Thrust (temper, vs armor) and Deflecting (defense) do not negate miss chances.

## NAME COLLISION
Hunter's Mark (pool), Precise Thrust (temper), spell seeking; none mechanically overlapping.

## FORKS
1. Does it also negate the incorporeal 50% chance? Default: no, only miss chances from concealment-type effects; incorporeal is Ghost Touch's job.
2. Thrown weapons. Default: not covered, per the printed "only ranged weapons" (a Throwing weapon is melee).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- whether it fits a weapon attack that is not an Innate Attack is OPEN, so no point total is stated.
