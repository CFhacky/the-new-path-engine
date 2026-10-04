# SPELL STORING
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 226 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Spell Storing: A spell storing weapon allows a spellcaster to store a single targeted spell of up to 3rd level in the weapon. (The spell must have a casting time of 1 standard action.) Any time the weapon strikes a creature and the creature takes damage from it, the weapon can immediately cast the spell on that creature as a free action if the wielder desires. (This special ability is an exception to the general rule that casting a spell from an item takes at least as long as casting that spell normally.) Inflict serious wounds, contagion, blindness, and hold person are all common choices for the stored spell. Once the spell has been cast from the weapon, a spellcaster can cast any other targeted spell of up to 3rd level into it. The weapon magically imparts to the wielder the name of the spell currently stored within it. A randomly rolled spell storing weapon has a 50% chance to have a spell stored in it already.
Strong evocation (plus aura of stored spell); CL 12th; Craft Magic Arms and Armor, creator must be a caster of at least 12th level; Price +1 bonus,
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Single rung. Targeted spell, level 3 or lower, 1-standard-action casting time. Discharge is the wielder's choice, free action, on a creature the weapon damaged, once per stored spell; any caster may refill. No d100, no save of its own; the spell's save and SR apply as printed. Bows/crossbows/slings: the SRD text does not extend it to ammunition. If the stored spell is magical healing, discharge on a struck creature ends Fatal Wound stacks below cap per the Registry rule.

## GURPS 4e
Reservoir's ER Battery is the energy store; the delta is casting the stored Magic spell on a DR-penetrating hit as a free action. Follow-Up +0% only applies to Innate Attacks, so no verified chassis exists for "release stored spell on hit". Gadget Breakable -25% + Can Be Stolen -10% = -35%. Spell energy cost and the GURPS equivalent of the 3rd-level cap: open. Points: not computable.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Reservoir (Resource 49-54).
Reservoir (Resource 49-54): store one spell/ability for later use, 1st/2nd/3rd/5th/7th; GURPS ER Battery 2/3/5/8/12 points. Spellthief (Rare Build-Around 71-80) captures a spell on a successful save, a different trigger. Gap: Reservoir's T3 rung (3rd level) matches the cap, but the row does not say targeted-only, free-action discharge on a damaging weapon hit, or refill by any caster.

## NAME COLLISION
Reservoir, Spellthief, SRD ring of spell storing (different item), Wardbreaker.

## FORKS
1. Stored-spell CL and DC: default the storing caster's, as for any stored spell (unsourced here). 2. Delta vs full family: default delta over Reservoir T3. 3. GURPS chassis open: default Reservoir ER Battery plus Gadget, numbers pending the Basic Set.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.
