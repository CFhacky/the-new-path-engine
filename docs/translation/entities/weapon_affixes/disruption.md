# DISRUPTION
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 225 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Disruption: A weapon of disruption is the bane of all undead. Any undead creature struck in combat must succeed on a DC 14 Will save or be destroyed. A weapon of disruption must be a bludgeoning weapon. (If you roll this property randomly for a piercing or slashing weapon, reroll.)
Strong conjuration; CL 14th; Craft Magic Arms and Armor, heal; Price +2 bonus,
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Bludgeoning weapons only (reroll or refuse on piercing/slashing). Each hit on an undead creature forces a DC 14 Will save; failure destroys the undead (it is not a death or mind-affecting effect in the fetched text; incorporeal undead need their own means to be struck). Success leaves the hit as a normal attack. No SR is stated. Each hit rolls its own save. No effect on living, constructs or objects. No Fatal Wound interaction (bloodless targets only; no healing).

## GURPS 4e
Chassis Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10% = -35%). Mechanism: Follow-Up (+0%) rider on a DR-penetrating hit against an Undead target (Accessibility "only vs. undead", percentage OPEN), resisted by a Will roll, failure = destroyed. GURPS has no stock "destroyed" Affliction effect and the d20 DC 14 does not map to a 3d6 Will contest by any retrievable rule, so the effect type and the resistance modifier are OPEN. Magical -10%. Point total not computable.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 bonus-equivalent = 8,000 gp (bonus-squared x 2,000; matches printed +2).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Radiant (Elemental 45-50), Turn Mastery (Skill/Class 43-48).
none. Radiant (Elemental 45-50) deals extra damage to undead (x1.5), Turn Mastery (Skill/Class 43-48) improves turning, Soul Anchor (Condition 97-100) acts on kills; gap: no row destroys an undead outright on a failed save.

## NAME COLLISION
SRD Disruption (identical); spell disrupt undead, SRD Bane (undead as designated foe, +1 affix; stacks); pool Radiant, Turn Mastery, Soul Anchor.

## FORKS
1. "Struck in combat": must the hit deal damage past DR before the save? Recommended default: yes (proc-conventions §1: a hit that deals no damage rolls nothing), so a DR-immune lich is not auto-triggered.
2. Named/unique undead. SRD gives no exemption. Recommended default: as printed (a failed DC 14 save destroys), with the DM free to flag a named undead as immune before ratification.
3. GURPS effect and resistance for "destroyed". Recommended default: treat as an instant destroy on a failed Will roll, penalty set from the Basic Set (number open).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- undead", percentage OPEN), resisted by a Will roll, failure = destroyed.
- GURPS has no stock "destroyed" Affliction effect and the d20 DC 14 does not map to a 3d6 Will contest by any retrievable rule, so the effect type and the resistance modifier are OPEN.
