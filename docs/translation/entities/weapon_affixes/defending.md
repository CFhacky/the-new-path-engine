# DEFENDING
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 225 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Defending: A defending weapon allows the wielder to transfer some or all of the sword's enhancement bonus to his AC as a bonus that stacks with all others. As a free action, the wielder chooses how to allocate the weapon's enhancement bonus at the start of his turn before using the weapon, and the effect to AC lasts until his next turn.
Moderate abjuration; CL 8th; Craft Magic Arms and Armor, shield or shield of faith: Price +1 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** At the start of the wielder's turn, as a free action, the wielder moves any 0..N points of the weapon's enhancement bonus from the weapon to AC (N = base enhancement bonus; special-ability bonus-equivalents never count). The weapon's attack and damage enhancement drops by the same amount; the AC bonus lasts until the wielder's next turn. No d100, no save, no SR, no DC. No Fatal Wound interaction (no healing).

## GURPS 4e
Chassis Gadget (Breakable DR 6 -25%, Can Be Stolen -10% = -35%). Follow the Warding precedent: moving n points reduces the weapon's Weapon Bond by n (Striking row precedent) and grants Damage Resistance +n (5/level in gurps_trait_index; 5 x 0.65 = 3.25 per level after the Gadget limitations), set at the start of the wielder's turn and held until the next. Weapon Bond cost is not in the index; net zero-sum totals are open. Magical -10% not applied (defensive, not an attack).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 bonus-equivalent = 2,000 gp (bonus-squared x 2,000; matches printed +1).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Warding (Defensive 01-06).
Warding (Defensive 01-06): AC +1/+1/+2/+3/+4 (deflection); GURPS DR +n (Gadget). Also Shield Wall (49-54, shield-type AC). Gap: Warding is a free, permanent AC bonus; Defending is a zero-sum reallocation of the weapon's own enhancement bonus, chosen each turn.

## NAME COLLISION
Warding (Defensive 01-06); Shield Wall (Defensive 49-54); SRD "defending" is also a creature-trait word in some stat blocks; SRD Defending is the only weapon property by this name; Savage Blow (Offensive 43-48, a tradeoff of Power Attack, different mechanic).

## FORKS
1. What counts as the "enhancement bonus". Recommended default: only the base +N; pool Striking bonuses and other bonus-equivalent affixes do not count.
2. GURPS mapping: DR (Warding precedent) or Defense Bonus (Aegis precedent). Recommended default: DR, per Warding.
3. Does the transferred amount also reduce damage, not only attack? Recommended default: yes (attack and damage), since the SRD calls it a transfer of the enhancement bonus.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.
