# FLESHGRINDING
**Weapon property — Magic Item Compendium, PDF p. 36 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
FLESHGRINDING
Price: +2 bonus
Property: Piercing or slashing melee weapon
Caster Level: 11th
Aura: Moderate; (DC 20) transmutation
Activation: Free (command)
You can activate a fleshgrinding weapon any time you deal damage with it to a living creature in melee. When this occurs, you let go of the weapon and it magically animates, grinding itself into the foe's flesh. In each round at the start of your turn, it automatically damages that creature as if you had scored a normal hit with it (including damage from the weapon's enhancement bonus, other weapon properties, and your normal bonus from Strength, but not extra damage from feats such as Power Attack). The grinding continues for 5 rounds or until you or someone else pulls the fleshgrinding weapon free; doing this requires a standard action and (for anyone other than you) a successful DC 20 Strength check. After the duration expires, a fleshgrinding weapon returns to your hand (as the returning weapon property). It will not return to your hand if the target has pulled the weapon free and still holds it.
Prerequisites: Craft Magic Arms and Armor, animate objects.
Cost to Create: Varies.
```

## D&D 3.5e
**Printed header:** Price: +2 bonus; Property: Piercing or slashing melee weapon; Caster Level: 11th; Aura: Moderate; (DC 20) transmutation; Activation: Free (command); Prerequisites: Craft Magic Arms and Armor, animate objects.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed. It scales with the wielder's Strength and the weapon's properties, stated explicitly; no daily limit printed. Bloodless targets: the text says "living creature", so constructs and undead are immune.

## GURPS 4e
repeated Innate Attack equal to a normal hit each second for 5 turns, ended by pulling it free (Contest of ST DC-equivalent, OPEN); Cyclic is the cost carrier (+400% per cycle, from the Registry constants) but the percentage and the Follow-Up interplay are OPEN.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none (Fatal Wound is a stacking bleed with a proc; this is a weapon-driven repeating hit).

## FORKS
1. the wielder is unarmed for 5 rounds; default as printed.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- repeated Innate Attack equal to a normal hit each second for 5 turns, ended by pulling it free (Contest of ST DC-equivalent, OPEN);
- Cyclic is the cost carrier (+400% per cycle, from the Registry constants) but the percentage and the Follow-Up interplay are OPEN.
