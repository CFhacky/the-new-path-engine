# IMPLACABLE
**Weapon property — Magic Item Compendium, PDF p. 38 (3.5e source; printed rules are the 3.5e side)**
**Tier 2 — Heroic Elite (levels 13-16)** (tier rule in `triage_affixes.py`; price +3 = 18,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
IMPLACABLE
Price: +3 bonus
Property: Weapon
Caster Level: 9th
Aura: Moderate; (DC 18) necromancy
Activation: --
When an implacable weapon deals damage to a living creature, the wound bleeds profusely and the creature takes 2 additional points of damage at the start of each of the wielder's turns for the next 5 rounds. Multiple wounds are cumulative (a creature struck three times in the same round would take 6 points of damage per round for the next 5 rounds). This bleeding can be stopped by a successful DC 15 Heal check or any effect that restores hit points (such as cure light wounds). However, while the wound is active, anyone attempting to cast a spell on the target that would restore hit points must succeed on a DC 15 caster level check. An implacable weapon counts as adamantine for the purpose of overcoming the damage reduction of aberrations.
Prerequisites: Craft Magic Arms and Armor, vampiric touch.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +3 bonus; Property: Weapon; Caster Level: 9th; Aura: Moderate; (DC 18) necromancy; Activation: --; Prerequisites: Craft Magic Arms and Armor, vampiric touch.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed. Stacking is additive and linear (consistent with the stacking doctrine). No cap is printed; flagged.

## GURPS 4e
Innate Attack (Toxic) Follow-Up, Cyclic (+400% per cycle), no ST linkage; the per-wound five-round expiry is the cycle count (point total OPEN). Bloodless targets (constructs, undead, oozes, elementals) are immune, per the Registry baseline and the printed "living creature".

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+3 = 18,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
the ratified Fatal Wound family (Registry section 1) is the Registry's stacking bleed: proc 10/15/20%, ticks 1-3 per stack, caps 3/4/5, a fatal state at cap. Implacable is a second, harder stacking bleed (every damaging hit, 2 per stack, uncapped, 5-round expiry per wound).

## RULINGS
1. cap at 5 stacks, matching the Fatal Wound Unique cap, because an uncapped stack is a death spiral). 2. healing: the printed "any effect that restores hit points stops the bleeding" agrees with the Registry norm, so any magical healing, including the Crusader heal (D2 reversed 2026-10-04), ends Implacable's wounds. 3. overlap with Fatal Wound on one weapon (default not allowed together).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- the per-wound five-round expiry is the cycle count (point total OPEN).
