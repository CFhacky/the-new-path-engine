# SOULBREAKER
**Weapon property — Magic Item Compendium, PDF p. 45 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
SOULBREAKER [SYNERGY]
Price: +1 bonus
Property: Weapon
Caster Level: 17th
Aura: Strong; (DC 23) necromancy
Activation: --
Synergy Prerequisite: Enervating
This weapon functions as an enervating weapon (see page 34). However, a negative level gained from an attack from a soulbreaker weapon doesn't fade [OCR: "after 1 hour" lost; the text reads] "...24h..." [garbled; delay figure uncertain]: if the negative level or levels have not been purged, the subject must succeed on a DC 18 Fortitude save for each negative level or lose a character level.
Prerequisites: Craft Magic Arms and Armor, energy drain.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 17th; Aura: Strong; (DC 23) necromancy; Activation: --; Synergy Prerequisite: Enervating; Prerequisites: Craft Magic Arms and Armor, energy drain.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; permanent level loss is campaign-weighty, so the default is to apply it only to NPCs unless the owner rules otherwise.

## GURPS 4e
lasting loss of points or a skill level on a failed HT roll (OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 on top of Enervating.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Enervating (MIC).
builds on Enervating (batch 04). Delta = the delayed permanent-loss save.

## RULINGS
NPC wielders use it as printed; against a PC the negative levels last 24 hours unless purged and never convert to level loss. The 24-hour delay is OCR-uncertain; confirm against the book page.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: degraded.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- lasting loss of points or a skill level on a failed HT roll (OPEN).
