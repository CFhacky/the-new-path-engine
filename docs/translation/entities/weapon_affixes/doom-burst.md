# DOOM BURST
**Weapon property — Magic Item Compendium, PDF p. 34 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
DOOM BURST
Price: +2 bonus
Property: Weapon
Caster Level: 11th
Aura: Moderate; (DC 20) necromancy
Activation: --
Whenever you score a critical hit with this weapon, a wave of blackness washes over the target, causing it to become shaken (no saving throw) for 5 rounds. This effect activates even if the creature struck is not normally subject to extra damage from critical hits. This effect doesn't stack with itself or with any other fear effects (it can't render an already shaken creature frightened, for example).
Prerequisites: Craft Magic Arms and Armor, fear.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Weapon; Caster Level: 11th; Aura: Moderate; (DC 20) necromancy; Activation: --; Prerequisites: Craft Magic Arms and Armor, fear.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed, trigger confirmed crit, no save (flagged), 5 rounds.

## GURPS 4e
Affliction (Fright-lite), Trigger critical, no resistance roll (percentage OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none for the crit-trigger shaken.

## FORKS
1. no save printed, kept (crit-only, weak condition); fear-immune targets stay immune.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Affliction (Fright-lite), Trigger critical, no resistance roll (percentage OPEN).
