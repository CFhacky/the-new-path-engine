# SHOCKING BURST
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 226 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Shocking Burst: A shocking burst weapon functions as a shock weapon that also explodes with electricity upon striking a successful critical hit. The electricity does not harm the wielder. In addition to the extra electricity damage from the shock ability, a shocking burst weapon deals an extra 1d10 points of electricity damage on a successful critical hit. If the weapon's critical multiplier is x3, add an extra 2d10 points of electricity damage instead, and if the multiplier is x4, add an extra 3d10 points. Bows, crossbows, and slings so crafted bestow the electricity energy upon their ammunition. Even if the shock ability is not active, the weapon still deals its extra electricity damage on a successful critical hit.
Moderate evocation; CL 10th; Craft Magic Arms and Armor, call lightning or lightning bolt; Price +2 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** On a confirmed critical hit, +1d10 electricity (x2 weapon), +2d10 (x3), +3d10 (x4). Not multiplied by the crit (implied by the printed ladder; unstated). No action, no save, no SR, instant. Works with the Shock toggle off. Ranged: ammunition carries it. Adds to the Shocking T4 +1d6 on every hit. Procs: no d100 (crit-triggered, not a proc).

## GURPS 4e
Innate Attack (Burning [Lightning]) Follow-Up +0%, triggered on a critical hit; Gadget Breakable -25% + Can Be Stolen -10% = -35%. Crit-only limitation percentage: open (not retrieved). Dice read as-is: 1d10 / 2d10 / 3d10 by the weapon's multiplier class. Resulting points: not computable.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 total = 8,000 gp (inclusive of the Shocking T4 half; do not add Shocking's 2,000 on top).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Shocking (Elemental 17-24).
Shocking (Elemental 17-24) covers the Shock half (T4 +1d6 lightning, GURPS IA Burning [Lightning] Follow-Up). Lethal Focus (Offensive 31-36) is untyped crit dice by tier; Elemental Burst (Elemental 75-80) is a 10-ft Reflex-half crit burst. Gap: crit-only electricity dice on a multiplier ladder (1d10/2d10/3d10), independent of the Shock toggle, is not in any row.

## NAME COLLISION
SRD Shocking Burst vs pool Shocking, Elemental Burst, Stormborn; "Burst" also names the flaming/icy/shocking family.

## FORKS
1. Standalone vs delta: default delta stacked on Shocking T4 (SRD says it "functions as a shock weapon"). 2. Resolved by the engine: the weapon's own 3.5e crit multiplier applies and dice read as-is.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.
