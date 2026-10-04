# THROWING
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 227 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Throwing: This ability can only be placed on a melee weapon. A melee weapon crafted with this ability gains a range increment of 10 feet and can be thrown by a wielder proficient in its normal use.
Faint transmutation; CL 5th; Craft Magic Arms and Armor, magic stone; Price +1 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Melee weapons only. Gains a 10-ft range increment and can be thrown by anyone proficient with it in melee. Attack and damage then follow the standard thrown-weapon rules (Str to damage, 5-increment maximum), which the fetched text does not restate. No return, no save, no SR, no d100. Does not include Returning (a separate SRD ability).

## GURPS 4e
mechanism is a Gadget that gives the weapon a thrown profile (Range, Accuracy) so it can be used with Throwing skill without the improvised-throw penalties. I could not verify the Basic Set thrown-weapon numbers, so the range and Acc values, any skill modifier, and the point cost are open. Gadget limitations -35% (Breakable -25%, Can Be Stolen -10%) apply to whatever trait is chosen.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none in Part 1 pools. The Siege aspect (Part 3, 24E: "Melee attack gains 30/60/100 ft range") is a different layer and a different range. Gap: nothing grants a thrown profile to a melee weapon.

## NAME COLLISION
3.5 "Throwing" weapon property words (throwing axe), SRD Returning, Distance, Siege aspect.

## FORKS
1. Whether the weapon comes back: default no, Returning is a separate ability. 2. Thrown damage uses Str: default the standard rule. 3. GURPS range/Acc numbers: open, take from the Basic Set thrown-weapon table.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.
