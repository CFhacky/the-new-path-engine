# HOLY
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 226 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Holy: A holy weapon is imbued with holy power. This power makes the weapon good-aligned and thus bypasses the corresponding damage reduction. It deals an extra 2d6 points of damage against all of evil alignment. It bestows one negative level on any evil creature attempting to wield it. The negative level remains as long as the weapon is in hand and disappears when the weapon is no longer wielded. This negative level never results in actual level loss, bur it cannot be overcome in any way (including restoration spells) while the weapon is wielded. Bows, crossbows, and slings so crafted bestow the holy power upon their ammunition.
Moderate evocation [good]; CL 7th; Craft Magic Arms and Armor, holy smite, creator must be good; Price +2 bonus.
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** weapon counts as good-aligned for DR. Each damaging hit on an evil creature adds +2d6 untyped damage (not multiplied on a crit). No save, no SR. An evil wielder gains 1 negative level while holding it. Ammunition weapons confer the property. No healing interaction.

## GURPS 4e
chassis Gadget (Breakable -25%, Can Be Stolen -10% = -35%). Extra damage = Innate Attack, Follow-Up +0%, 2d (Executioner precedent: +2d6 = 2d), Accessibility "only vs. evil-aligned targets" -20% by the Hunter's Mark precedent (percentage open), Magical -10%; limitations total -65%, inside the -80% cap. Per-die base cost is "Variable" in the repo index, so no point total is stated. Damage type for the rider: open. Wielder penalty for an evil wielder: the Energy Drained condition while held (engine ruling), same default as Anarchic fork 2.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Radiant (Elemental 45-50).
none keyed to alignment. Radiant (Elemental 45-50) is positive-energy damage (undead x1.5), not an alignment smite; Banefire is element-subtype only.

## NAME COLLISION
Unholy (twin), Anarchic and Axiomatic (same template), Radiant (pool; flavor overlap only), spell holy smite.

## FORKS
1. Holy plus Radiant on one weapon. Default: allowed, riders add (different keys, additive, never multiplicative).
2. Holy and Unholy together. Default: mutually exclusive.
3. RULED by the engine: alignment is read from the 3.5e stat block; an evil wielder takes the Energy Drained condition; the 2d6 ignores worn DR (Rider class).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.
