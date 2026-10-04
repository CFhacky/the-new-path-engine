# VORPAL
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 227 (3.5e source; printed rules are the 3.5e side)**
**Tier 1 — Legendary (levels 17-20)** (tier rule in `triage_affixes.py`; price +5 = 50,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Vorpal: This potent and feared ability allows the weapon to sever the heads of those it strikes. Upon a roll of natural 20 (followed by a successful roll to confirm the critical hit), the weapon severs the opponent's head (if it has one) from its body. Some creatures, such as many aberrations and all oozes, have no heads. Others, such as golems and undead creatures other than vampires, are not affected by the loss of their heads. Most other creatures, however, die when their heads are cut off. The DM may have to make judgment calls about this sword's effect. A vorpal weapon must be a slashing weapon. (If you roll this property randomly for an inappropriate weapon, reroll.)
Strong necromancy and transmutation; CL 18th; Craft Magic Arms and Armor, circle of death, keen edge; Price +5 bonus
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Natural 20, then a successful confirmation roll. The head is severed with no save and no SR. No effect on headless creatures (many aberrations, all oozes) or those unaffected by head loss (golems, undead other than vampires); creatures immune to crits cannot be vorpaled. Slashing weapons only. No d100 (printed trigger is the confirmed 20). The text does not call it a death effect, so Death Ward does not stop it. No Fatal Wound interaction. Fused-engine resolution: a confirmed natural-20 crit forces Head/Lethal on the location table.

## GURPS 4e
no instant-kill trait verified in my sources. Mechanism: trigger on a GURPS critical hit on the attack roll, effect "head severed", applying the same headless/unaffected exceptions. The 3.5e trigger is about 5% x confirm chance, while GURPS critical hits are 3-4 (and 5-6 at high skill), so the rates differ; the book rules and any trigger limitation are not retrieved and are open. Gadget -35%. Points: not computable.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+5 = 50,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none that matches. "Vorpal Edge" (Offensive 67-72) shares the name and the natural-20 trigger but is bonus slashing damage (base die x1..x3), not decapitation. Fortification (Defensive 07-12) negates crits and so blocks this. Gap: the instant-kill effect.

## NAME COLLISION
Vorpal Edge (Offensive 67-72), SRD vorpal sword (item), Keen Edge row (the SRD prerequisite spell is keen edge).

## RULINGS
1. A confirmed natural-20 crit from a vorpal weapon forces the Head location at Lethal severity on the fused engine's crit table; there is no separate save and the same table applies to PCs and named characters. 2. Not a death effect. 3. GURPS uses the same engine table.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.
