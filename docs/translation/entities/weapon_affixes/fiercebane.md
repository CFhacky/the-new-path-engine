# FIERCEBANE
**Weapon property — Magic Item Compendium, PDF p. 36 (3.5e source; printed rules are the 3.5e side)**
**Tier 4 — Competent (levels 5-8)** (tier rule in `triage_affixes.py`; price +1 = 2,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
FIERCEBANE [SYNERGY]
Price: +1 bonus
Property: Weapon
Caster Level: 12th
Aura: Strong; (DC 21) conjuration
Activation: --
Synergy Prerequisite: Bane
A fiercebane weapon excels at attacking one type or subtype of creature. It acts as a bane weapon against the creature type (and subtype, if relevant) to which its synergy prerequisite ability was attuned. Whenever it strikes its designated bane enemy, it begins to emit a low, eager hum, as if it were actually feeding off the victim's life blood. A fiercebane weapon glows when a designated foe comes within 60 feet, even if you cannot see or detect it. In addition, the weapon deals extra damage on every successful critical hit. The amount depends on its critical multiplier, as follows.
Critical Multiplier / Extra Damage: x2 1d10; x3 2d10; x4 3d10
Projectile weapons bestow this property upon their ammunition.
Lore: gnome ranger Tir Hearthand created the first fiercebane weapon, an orc bane scimitar named Hearthand (Knowledge [arcana] or Knowledge [history] DC 20; the original is believed lost, DC 30).
Prerequisites: Craft Magic Arms and Armor, summon monster I.
Cost to Create: Varies.

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
**Printed header:** Price: +1 bonus; Property: Weapon; Caster Level: 12th; Aura: Strong; (DC 21) conjuration; Activation: --; Synergy Prerequisite: Bane; Prerequisites: Craft Magic Arms and Armor, summon monster I.; Cost to Create: Varies.

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** crit rider by multiplier class (default 1d / 2d / 3d), detection 60 ft as a proximity sense.

## GURPS 4e
crit rider by multiplier class (default 1d / 2d / 3d), detection 60 ft as a proximity sense.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+1 on top of Bane.

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Bane (DMG).
DMG Bane (see that file) plus the burst template. Delta = crit rider and 60-ft detection.

## FORKS
shares the Bane rulings (foe chosen by the crafter).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.
