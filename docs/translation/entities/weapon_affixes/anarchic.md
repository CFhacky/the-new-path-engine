# ANARCHIC
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 224 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Anarchic: An anarchic weapon is chaotically aligned and infused with the power of chaos, It makes the weapon chaos-aligned and thus bypasses the corresponding damage reduction, It deals an extra 2d6 points of damage against all of lawful alignment. It bestows one negative level on any lawful creature attempting to wield it. The negative level remains as long as the weapon is in, hand and disappears when the weapon is no longer wielded. This negative level never results in actual level loss, bur it-canner be overcome. in_any.way (including restoration spells) while the weapon. is wielded. Bows, crossbows, and slings so. crafted bestow the chaotic power upon. their ammunition.
Moderate evocation [chaotic]; CL 7th; Craft Magic Arms and Armor, chaos hammer, creator must be chaotic; Price +2 bonus,
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** Weapon counts as chaos-aligned (bypasses DR/chaotic). Every damaging hit on a creature with a lawful alignment component adds +2d6 untyped damage (not multiplied on a crit). No save, no SR, no DC. A lawful creature wielding it gains 1 negative level for as long as it holds the weapon; removable by no effect while held; ends when released; never converts to level loss; standard negative-level rules apply. Bow, crossbow or sling confers the chaotic quality and the +2d6 to its ammunition. No Fatal Wound interaction (no healing).

## GURPS 4e
Chassis: Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10% = -35%). Extra damage = Innate Attack, Follow-Up (+0%), 2d, by the Executioner row precedent (3.5e +2d6 = 2d); Accessibility "only vs. lawful-aligned targets" -20% by the Hunter's Mark precedent (percentage open for ratification); Magical -10%. Limitations total -65% (inside the -80% cap). Base Innate Attack cost per die is "Variable" in gurps_trait_index, so no point total is stated; open. Damage type for the rider: open (no precedent for alignment damage). Wielder penalty for a lawful wielder: mechanism open (see fork 2). No d100 on either side.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 bonus-equivalent = 8,000 gp (bonus-squared x 2,000; matches the printed +2).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.
none. Closest are Banefire (Elemental 93-96, element-subtype only), Chaos Element (Elemental 97-100, random element, unrelated) and Penetrating Strikes (Offensive 85-90, material DR, not alignment); gap: no row for alignment-keyed bonus damage, alignment-DR bypass, or a wielder-penalty clause.

## NAME COLLISION
SRD Axiomatic (opposed twin; also queued); SRD Holy/Unholy (queued; same "extra 2d6 vs aligned" template); spell chaos hammer; pool Chaos Element (name echo only).

## FORKS
1. RULED by the engine: the target's alignment is read from its 3.5e stat block; no GURPS alignment tag is built.
2. RULED by the engine: a wrong-aligned wielder takes the Energy Drained condition while holding the weapon (-1 attacks/saves/skills/ability checks, -5 HP, -1 effective level; never level loss).
3. Anarchic and Axiomatic on one weapon. Recommended default: mutually exclusive (contradictory alignment; SRD fetched text does not say).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.
