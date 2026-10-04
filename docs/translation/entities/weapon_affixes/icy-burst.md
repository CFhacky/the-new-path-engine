# ICY BURST
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 226 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Icy Burst: An icy burst weapon functions as a frost weapon that also explodes with frost upon striking a successful critical hit. The frost does not harm the wielder. In addition to the extra damage from the frost ability, an icy burst weapon deals an extra 1d10 points of cold damage on a successful critical hit. If the weapon's critical multiplier is x3, add an extra 2d10 points of cold damage instead, and if the multiplier is x4, add an extra 3d10 points. Bows, crossbows, and slings so crafted bestow the cold energy upon their ammunition. Even if the frost ability is not active, the weapon still deals its extra cold damage on a successful critical hit.
Moderate evocation; CL 10th; Craft Magic Arms and Armor, chill metal or ice storm; Price +2 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** on a confirmed critical hit, extra cold damage by the weapon's multiplier class: x2 = 1d10, x3 = 2d10, x4 = 3d10, applied even when the Frost toggle is off. Not multiplied by the crit (extra dice are not multiplied). Respects cold resistance and immunity. No save, no SR.

## GURPS 4e
chassis Gadget (Breakable -25%, Can Be Stolen -10%); Innate Attack (Burning [Cold]), Follow-Up +0%, Trigger "critical hit only", Magical -10%. Dice: default 1d / 2d / 3d by multiplier class, matching the Flaming Burst default. Trigger percentage and per-die base cost: OPEN, no point total stated.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
printed +2 = 8,000 gp as a standalone ability that includes the frost half (Freezing at T4 + delta).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Freezing (Elemental 09-16).
Freezing (Elemental 09-16) covers the frost half. Elemental Burst (Elemental 75-80) is a different mechanic (10-ft burst, Reflex half), not a single-target crit rider.

## NAME COLLISION
Elemental Burst (pool, different mechanic); Frost (sibling); SRD Flaming Burst and Shocking Burst (same template).

## FORKS
1. Engine ruling: the weapon's own 3.5e crit multiplier applies; no GURPS conversion is needed.5e multiplier class.
2. Bursts on one weapon: Icy Burst replaces Frost, never stacks with it. Default: not allowed together.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Trigger percentage and per-die base cost: OPEN, no point total stated.
