# IMPEDANCE
**Weapon property — Magic Item Compendium, PDF p. 38 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
IMPEDANCE
Price: +2 bonus
Property: Weapon
Caster Level: 11th
Aura: Moderate; (DC 20) abjuration
Activation: --
An impedance weapon mimics the impeded magic planar trait (DMG 150). When you use it to strike a creature, the target's ability to cast spells or use spell-like abilities is impeded for 1d6 rounds. To cast an impeded spell or use an impeded spell-like ability, the creature must attempt a Spellcraft check, Intelligence check, or Charisma check (whichever one is made with the highest bonus). The DC for this check is 15 + the spell level. If the check succeeds, the effect functions normally; if the check fails, the effect does not function and the spell or the use of the spell-like ability is lost.
Prerequisites: Craft Magic Arms and Armor, antimagic field.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 11th; Aura: Moderate; (DC 20) abjuration; Activation: --; Prerequisites: Craft Magic Arms and Armor, antimagic field.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, every hit, fixed formula DC 15 + spell level.

## GURPS 4e
Affliction on casting (a casting roll penalty or a failure on a Will roll; modifiers OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
Silencing (Condition 31-36: silence 1d4 rounds, Will save) is the nearest; this has no save and a skill check instead.

## FORKS
1. repeated hits: default the duration does not stack, it refreshes.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- modifiers OPEN).
