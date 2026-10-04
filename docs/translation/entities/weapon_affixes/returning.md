# RETURNING
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 226 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Returning: This special ability can only be placed on a weapon that can be thrown. A returning weapon flies through the air back to the creature that threw it. It returns to the thrower just before the creature's next turn (and is therefore ready to use again in that turn). Catching a returning weapon when it comes back is a free action. If the character can't catch it, or if the character has moved since throwing it, the weapon drops to the ground in the square from which it was thrown.
Moderate transmutation; CL 7th; Craft Magic Arms and Armor, telekinesis; Price +1 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed. Return occurs just before the thrower's next turn; catch is a free action; a thrower who moved, or who cannot catch, finds the weapon on the ground in the square it was thrown from. No save, no SR.

## GURPS 4e
no verified GURPS trait for automatic return. Nearest registry precedent is Warp as used for Phasewalk, limited to the weapon only, returning to the thrower's hand, range equal to the throw. The trait, its modifiers and cost are OPEN; no point total stated. Chassis Gadget (Breakable -25%, Can Be Stolen -10%).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed +1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none. Throwing (batch C file) gives melee weapons a thrown range; Returning is its natural pair.

## NAME COLLISION
Throwing (sibling); SRD returning is this ability.

## FORKS
1. GURPS has no initiative-turn "just before your next turn". Default: the weapon returns at the end of the thrower's turn in GURPS, one second later, available next turn.
2. Returning on a weapon that cannot be thrown. Default: invalid, per the printed restriction.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- The trait, its modifiers and cost are OPEN;
