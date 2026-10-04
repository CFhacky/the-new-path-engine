# SOULDRINKING
**Weapon property — Magic Item Compendium, PDF p. 45 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
SOULDRINKING [SYNERGY]
Price: +1 bonus
Property: Melee weapon
Caster Level: 5th
Aura: Faint; (DC 17) necromancy
Activation: --
Synergy Prerequisite: Enervating
This weapon functions as an enervating weapon (see page 34). In addition, when a souldrinking weapon scores a critical hit on a living creature, it grants you 5 temporary hit points and a +2 morale bonus on melee damage rolls. The temporary hit points don't stack with temporary hit points from any other source. This effect fades after 10 minutes.
Prerequisites: Craft Magic Arms and Armor, vampiric touch.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 5th; Aura: Faint; (DC 17) necromancy; Activation: --; Synergy Prerequisite: Enervating; Prerequisites: Craft Magic Arms and Armor, vampiric touch.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; flat.

## GURPS 4e
temporary HP buffer of 5, +1 damage for 10 minutes (2:1 default, OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 on top of Enervating.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Enervating (MIC).
Enervating (batch 04); Body Feeder (batch 02) is the nearest temp-HP-on-crit. Delta = fixed 5 temp HP and +2 morale damage.

## FORKS
none.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: degraded.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- temporary HP buffer of 5, +1 damage for 10 minutes (2:1 default, OPEN).
