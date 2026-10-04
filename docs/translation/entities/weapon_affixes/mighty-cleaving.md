# MIGHTY CLEAVING
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 226 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Mighty Cleaving: A mighty cleaving weapon allows a wielder with the Cleave feat to make one additional cleave attempt in a round.
Moderate evocation; CL 8th; Craft Magic Arms and Armor, divine power; Price +1 bonus,
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** a wielder with Cleave (or Great Cleave) may make one more cleave attempt per round than the feat normally allows. Requires the Cleave feat, as printed. No save, no SR.

## GURPS 4e
Gadget (Breakable -25%, Can Be Stolen -10%); the wielder's Extra Attack (Trigger: killing blow) may fire one more time per round. Cost of the extra trigger and the GURPS stand-in for the Cleave feat prerequisite: OPEN; no point total stated.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed +1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Cleave Through (temper 23A-1).
Cleave Through (temper 23A-1, a post-affix layer, not an affix pool row): on a kill, a free attack on an adjacent foe (as Cleave; T2+ Great Cleave); GURPS Extra Attack 1 (Trigger: killing blow). The temper grants the cleave itself; it does not add an extra per-round attempt.

## NAME COLLISION
Cleave Through (temper 23A-1); SRD feats Cleave and Great Cleave.

## FORKS
1. Mighty Cleaving on a weapon that also carries the Cleave Through temper. Default: the temper's free attack counts as the first cleave and Mighty Cleaving adds one more, still without needing the feat for the temper's attempt.
2. GURPS prerequisite. Default: the wielder must already own an Extra Attack (Trigger: killing blow) or a campaign-named cleave technique.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Cost of the extra trigger and the GURPS stand-in for the Cleave feat prerequisite: OPEN;
