# VICIOUS
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 227 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Vicious: When a vicious weapon strikes an opponent, it creates a flash of disruptive energy that resonates between the opponent and the wielder. This energy deals an extra 2d6 points of damage to the opponent and 1d6 points of damage to the wielder. Only melee weapons can be vicious.
Moderate necromancy; CL 9th; Craft Magic Arms and Armor, enervation; Price +1 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Melee weapons only. On each hit that deals damage, +2d6 to the opponent and 1d6 to the wielder, both untyped, not multiplied on a crit (unstated; default), no save, no SR, no d100 (printed trigger is every strike, not a proc). Undead/constructs: the wielder still takes the 1d6 (the text has no exception). Does not heal anyone; no Fatal Wound interaction.

## GURPS 4e
Innate Attack Follow-Up +0%, 2d6 to the opponent and 1d6 back to the wielder (dice read as-is). Gadget Breakable -25% + Can Be Stolen -10% = -35%. The percentage for damage to the user, and the mapping of "hurts the wielder" onto a limitation, are open (not retrieved). Points: not computable.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Wounding (Offensive 07-12), Berserker (Offensive 61-66).
none that matches. Wounding (Offensive 07-12) is plain bonus damage with no self-cost; Berserker (Offensive 61-66) trades AC; Blood Price Engine (Rare 31-40) and the Blood Pact temper (23I-9) are HP-cost mechanics of a different shape. Gap: every-hit target damage paired with every-hit wielder damage.

## NAME COLLISION
Blood Price Engine, Blood Pact, Berserker; the word "vicious" is also general weapon flavor text.

## FORKS
1. Trigger on any hit vs only damage past DR: default only a hit that deals damage past DR (matches proc conventions), then the 2d6 joins that damage and the 1d6 hits the wielder. 2. Can the wielder's 1d6 be reduced by DR/resist: default no, untyped and unreducible. 3. GURPS self-damage limitation percentage: open.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.
