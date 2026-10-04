# DISTANCE
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 225 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Distance: This property can only be placed on a ranged weapon. A weapon of distance has double the range increment of other weapons of its kind.
Moderate divination; CL 6th; Craft Magic Arms and Armor, clairaudience/clairvoyance; Price +1 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Ranged weapons only. The weapon's range increment is doubled (a 100-ft bow is 200 ft). Range penalty per increment is unchanged; the maximum number of increments is the weapon's normal one (PHB rule, not in the fetched ability text, so treat the maximum range as scaling with the doubled increment). No save, no SR, no DC, no action. No Fatal Wound interaction.

## GURPS 4e
Chassis: the launcher is the Gadget (Breakable DR 6 -25%, Can Be Stolen -10% = -35%). Mechanism: the weapon's 1/2D and Max are doubled. The nearest printed trait is the Increased Range enhancement, +10%/level in gurps_trait_index, but the index does not print what one level multiplies (whether one level doubles range is not verified); so the level count and total are OPEN. Magical -10% not applied (no attack). No d100.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 bonus-equivalent = 2,000 gp (bonus-squared x 2,000; matches printed +1).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none. Siege (aspect table 24E) gives a melee attack range but is an aspect, not an affix; Throwing (SRD, queued) gives a melee weapon a range increment; gap: no pool row doubles a range increment.

## NAME COLLISION
SRD Distance (identical); SRD Throwing (melee gains a 10 ft increment) and Seeking (ranged only), both queued; spell clairaudience/clairvoyance (prerequisite only); aspect Siege (24E).

## FORKS
1. Do thrown weapons count as "ranged weapons"? Recommended default: yes, any weapon with a range increment (thrown or launched); Throwing-crafted melee weapons also qualify.
2. GURPS level size of Increased Range. Recommended default: one level doubles 1/2D and Max (+10%), verified against the Basic Set before ratification (number open).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- so the level count and total are OPEN.
