# VAMPIRIC
**Weapon property — Magic Item Compendium, PDF p. 46 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
VAMPIRIC
Price: +2 bonus
Property: Melee weapon
Caster Level: 9th
Aura: Moderate; (DC 19) necromancy
Activation: --
A vampiric weapon deals an extra 1d6 points of damage to any living creature it hits, and you heal damage equal to this amount.
Prerequisites: Craft Magic Arms and Armor, vampiric touch.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Melee weapon; Caster Level: 9th; Aura: Moderate; (DC 19) necromancy; Activation: --; Prerequisites: Craft Magic Arms and Armor, vampiric touch.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** +1d6 untyped to living targets, heal equal to the roll (cap 6 per hit); bloodless targets give nothing.

## GURPS 4e
Innate Attack Follow-Up 1d6 plus a Vampiric-style leech of the injury (the pool's Leech row uses Vampiric Attack; costs OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
Leech (Resource 19-24: recover 1/1/2/3/5 HP per hit) is a flat heal with no extra damage; this is damage plus a matching heal (average 3.5, between Leech T3 and T2).

## FORKS
1. healing versus Fatal Wound: default the Registry norm applies: the Vampiric heal is magical healing and ends Fatal Wound stacks like any other (consistent with Crusader after D2 was reversed 2026-10-04).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- costs OPEN).
