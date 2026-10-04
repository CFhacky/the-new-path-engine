# FLAMING BURST
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 225 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Flaming Burst: A flaming burst weapon functions as a flaming weapon that also explodes with flame upon striking a successful critical hit. The fire does not harm the wielder. In addition to the extra fire damage from the flaming ability (see above), a flaming burst weapon deals an extra 1d10 points of fire damage on a successful critical hit. If the weapon's critical multiplier is x3, add an extra 2d10 points of fire damage instead, and if the multiplier is x4, add an extra 3d10 points of fire damage. Bows, crossbows, and slings so crafted bestow the fire energy upon their ammunition. Even if the flaming ability is not active, the weapon still deals its extra fire damage on a successful critical hit.
Strong evocation; CL 12th; Craft Magic Arms and Armor and flame blade, flame strike, or fireball; Price +2 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** On a confirmed critical hit, add fire damage: x2 weapon 1d10, x3 weapon 2d10, x4 weapon 3d10 (x5+ not printed; fork 3). Not multiplied by the crit. Works with the flaming toggle off, and against creatures immune to crits. Fire immunity/resistance applies. Ammunition inherits it (bow, crossbow, sling). No save, no SR, no DC. No healing interaction.

## GURPS 4e
Chassis Gadget (Breakable DR 6 -25%, Can Be Stolen -10% = -35%). Second Innate Attack (Burning), Follow-Up (+0%), Trigger: critical hit only, 1d / 2d / 3d by the weapon's multiplier class (Lethal Focus precedent maps 1d6/2d6/3d6 to 1d/2d/3d; the d10 vs d6 difference is not carried, fork 2). Trigger percentage is "Variable" in the index, so OPEN. Magical -10%. Base Innate Attack cost per die also open; no point total.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
Printed +2 total = 8,000 gp (bonus-squared x 2,000), sold as one affix that replaces Flaming (not Flaming 2,000 + a separate +1 delta; fork 1).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Flaming (Elemental 01-08).
Flaming (Elemental 01-08, T4 = 1d6 fire; IA Burning, Follow-Up) covers the base. Lethal Focus (Offensive 31-36) is untyped crit-only dice; Elemental Burst (Elemental 75-80) is an area burst. Gap: neither is the printed fire rider on a confirmed crit scaled by critical multiplier.

## NAME COLLISION
pool Elemental Burst (Elemental 75-80, 10-ft area, Ref half; NOT this ability, since the SRD burst is not an area); pool Flaming; SRD Icy Burst, Shocking Burst, Thundering (queued; same crit-burst template).

## FORKS
1. Price when combined. Recommended default: Flaming Burst is a standalone +2 that includes Flaming; never stack Flaming and Flaming Burst on one weapon.
2. GURPS dice mapping for d10. Recommended default: 1d / 2d / 3d, as Lethal Focus; revisit if d10 average (5.5) needs a +1.
3. Engine ruling: the weapon's own 3.5e crit multiplier applies; no GURPS conversion is needed.5e multiplier class (x2/x3/x4) to pick 1d/2d/3d; x5+ not printed, so no rung.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Trigger percentage is "Variable" in the index, so OPEN.
