# BRUTAL SURGE
**Weapon property — Magic Item Compendium, PDF p. 31 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
BRUTAL SURGE
Price: +1 bonus
Property: Melee weapon
Caster Level: 11th
Aura: Moderate; (DC 20) evocation
Activation: Swift (command)
After a successful melee attack with a brutal surge weapon, you can command the weapon to initiate a bull rush attempt against the target of the attack in addition to dealing its normal damage. This attempt does not provoke attacks of opportunity and is resolved using your size, Strength, and other relevant characteristics. If you wield a brutal surge weapon in two hands, you gain a +2 bonus on the opposed Strength check. If successful, the bull rush pushes the affected creature back the greatest possible distance allowed by the result of the opposed check, but you do not move along with the target. Movement caused by this bull rush attempt provokes attacks of opportunity from other creatures normally, but you cannot make an attack of opportunity against the affected creature. The brutal surge property is usable a number of times per day equal to 1 + your Con bonus (if any). Once you activate this property, it can't be activated by any other creature until the following day.
Prerequisites: Craft Magic Arms and Armor, Bigby's forceful hand.
Cost to Create: Varies.


CHANGELING
Price: +2,000 gp
Property: Spear, shortspear, or longspear
Caster Level: 5th
Aura: Faint; (DC 17) transmutation
Activation: Swift (command)
A changeling weapon allows you to choose its length and appearance each time you attack with it. Once per round, by speaking the appropriate command word, you can change the weapon into a spear, a shortspear, or a longspear sized appropriately for you. As part of the same action, you can make its haft and head appear to be composed of any wood, stone, metal, or combination thereof that you want, and add any decorative flourishes desired, though the spear's actual composition does not change.
Prerequisites: Craft Magic Arms and Armor, shrink item.
Cost to Create: 1,000 gp, 80 XP, 2 days.
```

## D&D 3.5e
**Printed header:** Price: +1 bonus; Property: Melee weapon; Caster Level: 11th; Aura: Moderate; (DC 20) evocation; Activation: Swift (command); Prerequisites: Craft Magic Arms and Armor, Bigby's forceful hand.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** as printed; this is a scaling effect by wielder Str and Con, stated explicitly, not flat-source.

## GURPS 4e
Knockback-style push resolved by a Quick Contest of ST; uses per day 1 + HT bonus (stand-in for Con bonus, OPEN).

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 = 2,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Knockback (Condition 49-54).
Knockback (Condition 49-54) pushes 5-20 ft on a Fortitude save; this uses an opposed Strength check and a no-move push. Delta = the opposed-check bull rush and the daily-use rule.

## FORKS
1. the attunement rule ("cannot be activated by another creature until the following day"), default keep as printed.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- uses per day 1 + HT bonus (stand-in for Con bonus, OPEN).
