# BANE
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 225 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Bane: A bane weapon excels at attacking one type or subtype of creature. Against its designated foe, its effective enhancement bonus is +2 betrer than its normal enhancement bonus (50a +1 longsword isa +3 longsword against its foe), It deals an extra 2d6 points of damage against the foe. Bows, crossbows, and slings so crafted bestow the bane quality upon their ammunition. To randomly determine a weapon's designated foe, roll on the following table.
(designated-foe d% table: Aberrations 01-05, Animals 06-09, Constructs 10-16, Dragons, Elementals 23-27, Fey 28-32, Giants 33-39, Humanoids (aquatic 40, dwarf 41-42, elf 43-44, gnoll 45, gnome 46, goblinoid 47-49, halfling 50, human 51-54, reptilian 55-57, orc 58-60), Magical beasts 61-65, Monstrous humanoids 66-70, Oozes 71-72, Outsiders (air 73, chaotic 74-76, earth 77, evil 78-80, fire 81, good 82-84, lawful 85-87, water 88), Plants 89-90, Undead 91-98, Vermin 99-100)
Moderate conjuration; CL 8th; Craft Magic Arms and Armor, summon monster I: Price +1 bonus,
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** The weapon names one designated foe (a creature type or subtype from the SRD table). Against that foe: +2 to the weapon's effective enhancement bonus (attack and damage, and for overcoming DR), plus the 2d6 rider (Banefire T4/T5 value, not stacked with Banefire; fork 2). No save, no SR, no DC. Ranged weapons pass it to ammunition. Bleed and healing: no interaction.

## GURPS 4e
Chassis Gadget (Breakable DR 6 -25%, Can Be Stolen -10% = -35%). Rider: reuse Banefire's IA (Bane) line, Follow-Up, 2d by the Executioner precedent (3.5e +2d6 = 2d), Accessibility "only vs. designated type" -20% by Hunter's Mark precedent (open). The +2 effective enhancement = Weapon Bond +2 to weapon skill (Striking row precedent, +2 = T3 value), same Accessibility. Magical -10%. Weapon Bond cost is not in gurps_trait_index; open. Totals not stated.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 bonus-equivalent = 2,000 gp (bonus-squared x 2,000; matches printed +1).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Banefire (Elemental 93-96).
Banefire (Elemental pool 93-96): +2d6/+2d6/+3d6/+4d6/+5d6 vs creatures with a chosen element subtype; GURPS IA (Bane). Gap: Banefire keys only to element subtype and carries no attack/damage enhancement bump; SRD Bane keys to any creature type or subtype and adds +2 effective enhancement.

## NAME COLLISION
Banefire (pool Elemental 93-96); SRD "Bane" spell-descriptor and the bane special-ability family (Bane weapon in SRD specific weapons, e.g. Dwarven Thrower is separate); GURPS "IA (Bane)" shorthand in the pool; SRD Disruption (undead-specific, queued here).

## FORKS
1. Foe selection: SRD gives the d% table only for random generation. Recommended default: crafter chooses the foe at creation; the table is used only for loot rolls.
2. Bane and Banefire on one weapon. Recommended default: not allowed together (one "versus" affix per weapon); if allowed, the two 2d6 riders add (additive, never multiplicative) only against a creature matching both.
3. Does the +2 effective enhancement raise the weapon's enhancement for Defending allocation or pool Striking? Recommended default: no, it applies only to the strike against the designated foe.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.
