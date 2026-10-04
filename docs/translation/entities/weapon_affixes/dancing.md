# DANCING
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 225 (3.5e source; printed rules are the 3.5e side)**
**Tier 1 — Legendary (levels 17-20)** (tier rule in `triage_affixes.py`; price +4 = 32,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Dancing: As a standard action, a dancing weapon can be loosed to attack on its own. It fights for 4 rounds using the base attack bonus of the one who loosed it and then drops. While dancing, it cannot make attacks of opportunity, and the person who activated it is not considered armed with the weapon. In all other respects, it is considered wielded or attended by the creature for all maneuvers and effects that target items (such as the sunder action or a heat metal spell). While dancing, it takes up the same space as the activating character and can attack adjacent foes (weapons with reach can attack opponents up to 10 feet away). The dancing weapon accompanies the person who activated it everywhere, whether she moves by physical or magical means. If the wielder who loosed it has an unoccupied hand, she can grasp it while it is attacking on its own as a free action; when so retrieved the weapon can't dance (attack on its own) again for 4 rounds.
Strong transmutation; CL 15th; Craft Magic Arms and Armor, animate objects; Price +4 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Standard action to loose it. For 4 rounds it makes its own attacks at the loosing creature's BAB (attacks per round: fork 1). It occupies the wielder's square, attacks adjacent foes (10 ft with reach), makes no attacks of opportunity, follows the wielder through any movement (physical or magical), and drops at the end of round 4. While dancing the wielder counts as unarmed with it but it is still wielded/attended for maneuvers and effects targeting items. A wielder with a free hand may catch it as a free action; a caught weapon cannot dance again for 4 rounds. Damage = weapon dice + enhancement and special-ability dice; wielder Str, Power Attack and class features do not apply (design; fork 2). No save, no SR, no DC. No Fatal Wound interaction.

## GURPS 4e
Chassis Gadget (Breakable DR 6 -25%, Can Be Stolen -10% = -35%); the sword is the Gadget, so Breakable matters: a dancing sword that is struck can be destroyed. Mechanism: an Ally-type animated weapon (pool precedent: Ally, Summonable, Minion) that attacks at the wielder's weapon skill (BAB mapping), exact 24 seconds (4 rounds x 6 s), then Takes Recharge 24 s (limitation, "Variable" in the index, percentage OPEN). Activation = one Ready/Concentrate maneuver (standard action). Ally cost is "Variable" in gurps_trait_index; no total stated; open. one attack per turn.
2. Damage bonuses. Recommended default: no Str/Dex-based damage; the weapon's own enhancement and special abilities count; GURPS skill = wielder's skill, damage uses the weapon's base damage with no ST thrust/swing bonus.
3. Two dancing weapons loosed by one wielder. Recommended default: allowed (one standard action each); the Cap is per weapon.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+4 bonus-equivalent = 32,000 gp (bonus-squared x 2,000; matches printed +4).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none. Closest are Minion/Spectral Guardian (Summoning 18, summons a creature, not the item), Echo Strike (Build-Around 41-50, duplicate strike) and Rapid Assault (Offensive 25-30, extra attacks); gap: nothing lets the weapon itself fight unattended on a timer.

## NAME COLLISION
SRD Dancing (identical); spell animate objects; SRD Dancing Lights; pool Minion, Spectral Guardian, Echo Strike, Shadow Clone (no shared mechanic).

## FORKS
1. Attacks per round. SRD says only "BAB of the one who loosed it." Recommended default: one attack per round at full BAB (no iterative attacks);

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: degraded.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- Mechanism: an Ally-type animated weapon (pool precedent: Ally, Summonable, Minion) that attacks at the wielder's weapon skill (BAB mapping), exact 24 seconds (4 rounds x 6 s), then Takes Recharge 24 s (limitation, "Variable" in the index, percentage OPEN).
