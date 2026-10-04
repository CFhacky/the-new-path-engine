# THUNDERING
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 226 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Thundering: A thundering weapon creates a cacophonous roar like thunder upon striking a successful critical hit. The sonic energy does not harm the wielder. A thundering weapon deals an extra 1d8 points of sonic damage on a successful critical hit. If the weapon's critical multiplier is x3, add an extra 2d8 points of sonic damage instead, and if the multiplier is x4, add an extra 3d8 points of sonic damage. Bows, crossbows, and slings so crafted bestow the sonic energy upon their ammunition. Subjects dealt a critical hit by a thundering weapon must make a DC 14 Fortitude save or be deafened permanently.
Faint necromancy; CL 5th; Craft Magic Arms and Armor, blindness/deafness; Price +1 bonus,
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** On a confirmed critical hit, +1d8 sonic (x2), +2d8 (x3), +3d8 (x4), not multiplied by the crit (unstated; implied by the ladder). Target makes Fortitude DC 14 (fixed) or is deafened permanently. No SR stated. Instant, no action. Immune: creatures immune to crits, sonic, or deafness. No d100 (crit-triggered). No healing interaction with Fatal Wound.

## GURPS 4e
Innate Attack (Crushing [Sonic]) Follow-Up +0%, triggered on a critical hit, plus an Affliction (Deafness) rider resisted by HT; Gadget -35% (Breakable -25%, Can Be Stolen -10%). Crit-only limitation percentage, the HT penalty equivalent to Fort DC 14, and the permanent-duration modifier: all open. Dice read as-is: 1d8 / 2d8 / 3d8 by multiplier class. Points: not computable.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Stormborn (Elemental 51-56), Lethal Focus (Offensive 31-36), Blinding (Condition 43-48).
none that matches. Stormborn (Elemental 51-56) is an every-hit sonic+lightning split; Lethal Focus (Offensive 31-36) is untyped crit dice; Blinding (Condition 43-48) is the nearest crit-triggered condition (blind 1 round). Gap: crit-only sonic dice on a multiplier ladder plus a permanent-deafness save.

## NAME COLLISION
SRD Thundering vs Stormborn (thunder flavor), Silencing (Mute), Elemental Burst; no Registry name "Thundering".

## FORKS
1. "Permanently" deaf: default as written; curable by remove blindness/deafness, heal or regeneration (default, not sourced). 2. Shocking Burst delta and Thundering share a crit-ladder engine: default one shared "crit-burst" rule text. 3. GURPS multiplier mapping, as in Shocking Burst: default by the 3.5e weapon's multiplier.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.
