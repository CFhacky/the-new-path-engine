# UNHOLY
**Weapon property — Dungeon Masters Guide v3.5, PDF p. 227 (3.5e source; printed rules are the 3.5e side)**
**Tier 3 — Heroic (levels 9-12)** (tier rule in `triage_affixes.py`; price +2 = 8,000 gp)

## SOURCE (verbatim, see packet header for normalization)
```
Unholy: An unholy weapon is imbued with unholy power. This power makes the weapon evil-aligned and thus bypasses the corresponding damage reduction. It deals an extra 2d6 points of damage against all of good alignment. It bestows one negative level on any good creature attempting to wield it. The negative level remains as long as the weapon is in hand and disappears when the weapon is no longer wielded. This negative level never results in actual level loss, but it cannot be overcome in any way (including restoration spells) while the weapon is wielded. Bows, crossbows, and slings so crafted bestow the unholy power upon their ammunition.
Moderate evocation [evil]; CL 7th; Craft Magic Arms and Armor, unholy blight, creator must be evil; Price +2 bonus
```

## D&D 3.5e
**Printed header:** 

**As printed:** the source block above is the rule text.

**Campaign adaptation (engine-bound):** weapon counts as evil-aligned for DR. Each damaging hit on a good creature adds +2d6 untyped damage (not multiplied on a crit). No save, no SR, no d100. A good wielder gains 1 negative level while holding it. Ammunition weapons confer the property. No healing interaction.

## GURPS 4e
identical to Holy with the axis flipped: Gadget (Breakable -25%, Can Be Stolen -10% = -35%); Innate Attack, Follow-Up +0%, 2d (Executioner precedent), Accessibility "only vs. good-aligned targets" -20% (Hunter's Mark precedent, percentage open), Magical -10%. No point total (per-die base cost "Variable"). Good-wielder penalty: the Energy Drained condition while held (engine ruling). GURPS DR is not alignment-typed, so the DR-bypass clause has no GURPS effect beyond the 3.5e tag.

**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.

## PRICE
+2 = 8,000 gp.

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Banefire (Elemental 93-96).
none keyed to alignment. Banefire (Elemental 93-96) keys on element subtype, Radiant and Shadowtouch are energy rows, Penetrating Strikes bypasses material DR only. (The batch agent read this as PARTIAL over Banefire; reconciled to NEW so all four alignment weapons share one verdict and one set of rulings.)

## NAME COLLISION
Holy (twin), Anarchic and Axiomatic (same template), Radiant (flavor overlap), spell unholy blight, Crusader's "Holy Strength" (name only).

## RULINGS
alignment is read from the 3.5e stat block; a good wielder takes the Energy Drained condition; Holy and Unholy are mutually exclusive on one weapon; the 2d6 ignores worn DR (engine Rider class).

## CONVERSION NOTES
Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: clean.
No open items.
