# BRILLIANT ENERGY
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 225 (3.5e source; printed rules are the 3.5e side)**
**Tier 1 — Legendary (levels 17-20)** (tier rule in `triage_affixes.py`; price +4 = 32,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Brilliant Energy: A brilliant energy weapon has its significant portion--such as its blade, axe head, or arrowhead--transformed into light, although this does not modify the item's weight. It always gives off light as a torch (20-foot radius). A brilliant energy weapon ignores nonliving matter. Armor bonuses to AC (including any enhancement bonuses to that armor) do not count against it because the weapon passes through armor. (Dexterity, deflection, dodge, natural armor, and other such bonuses still apply.) A brilliant energy weapon cannot harm undead, constructs, and objects. This property can only be applied to melee weapons, thrown weapons, and ammunition.
Strong transmutation; CL 16th; Craft Magic Arms and Armor, gaseous form, continual flare; Price +4 bonus
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Melee, thrown weapons and ammunition only (not ranged launchers). Attacks against a target's AC ignore armor and shield bonuses. Weapon sheds torch light, 20 ft radius, cannot be shut off (concealment of the drawn weapon is impossible). It cannot harm undead, constructs or objects (damage 0; also no sunder or object use). No save, no SR, no DC, no proc, no action. Interaction with DR as normal. No Fatal Wound interaction.

## GURPS 4e
Chassis Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10% = -35%). Armor interaction: ignore worn-armor DR but not natural DR = Armor Divisor above the ladder anchors (2) +50% and (5) +150%; the "ignores worn armor" step is not in the brief or in gurps_trait_index (Armor Divisor is "Variable"), so the percentage is OPEN. Shield DB (active-defense bonus) treated as ignored to match the 3.5e shield clause: fork 2. Limitation for the no-harm clause: Accessibility "no effect on Unliving or inanimate targets" with percentage OPEN. Light: a torch's glow has no trait cost. Magical -10%. Points not computable.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+4 bonus-equivalent = 32,000 gp (bonus-squared x 2,000; matches printed +4).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Armor Piercing (Offensive 19-24).
none. Armor Piercing (Offensive 19-24) ignores hardness/DR, not AC bonuses; Overpower (49-54) lowers AC/DR on a hit; Penetrating Strikes (85-90) is material/insubstantial. Gap: nothing ignores armor and shield AC bonuses or carries the cannot-harm-undead/constructs/objects clause.

## NAME COLLISION
SRD Brilliant Energy (identical); pool Armor Piercing (Offensive 19-24; GURPS Armor Divisor ladder collides, see fork 1), Radiant (Elemental 45-50, light flavor only), Overpower, Penetrating Strikes; spell gaseous form / continual flame (prerequisites only).

## FORKS
1. GURPS Armor Divisor ladder collision with Armor Piercing T1 (Armor Divisor (5)). Recommended default: Brilliant Energy is a separate "ignores worn armor" step above (5); percentage set from the Basic Set before ratification.
2. Shield: 3.5e ignores the shield's AC bonus. Recommended default: GURPS ignores the shield's DB and its DR, but keeps Dodge/Parry skill.
3. "Cannot harm undead, constructs, objects" in GURPS. Recommended default: damage 0 vs targets tagged undead or construct on the 3.5e side, and vs inanimate objects.

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):
- the "ignores worn armor" step is not in the brief or in gurps_trait_index (Armor Divisor is "Variable"), so the percentage is OPEN.
- Limitation for the no-harm clause: Accessibility "no effect on Unliving or inanimate targets" with percentage OPEN.
