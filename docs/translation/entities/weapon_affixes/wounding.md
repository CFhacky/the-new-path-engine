# WOUNDING
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 227 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Wounding: A wounding weapon deals 1 point of Constitution damage from blood loss when it hits a creature. A critical hit does not multiply the Constitution damage. Creatures immune to critical hits (such as plants and constructs) are immune to the Constitution damage dealt by this weapon.
Moderate evocation; CL 10th; Craft Magic Arms and Armor, Mordenkainen's sword; Price +2 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Every hit, 1 Con damage (ability damage, healed by normal ability-damage rules), no save, no SR, not multiplied by a crit. Immune: creatures immune to crits, which covers the Registry's bloodless list (constructs, undead, oozes, elementals) plus plants. No d100: the printed trigger is every hit, not a proc. Fatal Wound interaction: none, no healing is involved.

## GURPS 4e
Follow-Up Affliction (Attribute Penalty: HT), not Fatigue or HP damage. 3.5e 2 Con = 1 HT only if the brief's Str/Dex 2:1 ratio extends to Con (flagged), so one damaging hit is half a point of HT loss and every second hit costs HT -1. Duration, whether it persists until healed, resisting roll, and the Affliction percentage: all open. Gadget -35% (Breakable -25%, Can Be Stolen -10%). Points: not computable. default 2:1 per the brief's Str/Dex rule. 3. Every-hit Con damage is far stronger than the 10% proc rows in the Registry: default SRD-faithful, since the ability is priced +2 and has no proc rate in the source.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Weakening (Condition 37-42).
none that matches. Pool "Wounding" (Offensive 07-12) is flat bonus HP damage; the Fatal Wound family (Part 0) is a stacking HP bleed; Weakening (Condition 37-42) is a short Str penalty; Cursed Wound blocks healing. Gap: persistent Constitution damage on every hit.

## NAME COLLISION
pool "Wounding" (Offensive 07-12), Fatal Wound family, Cursed Wound, SRD Wounding spell effects; keep the three mechanics separate.

## FORKS
1. Every hit vs damage past DR: default only a hit that deals damage past DR (matches proc conventions; the SRD says "hits"). 2. Con-to-HT ratio in

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.
