# MARK OF THE SHATTERED HAND
**WoW weapon enchant — Profession, Warlords of Draenor (https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404))**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Warlords of Draenor
quality: degraded
url: https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404)
tooltip: (as summarized) 1500 bleed damage + 4500/6 sec.
facts: numbers only as summarized; the "4500/6 sec" reading is ambiguous.
gaps: verbatim tooltip, proc rate NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire the target bleeds 2 HP at the start of its turn for 3 rounds (6 HP total); bleeds from repeated procs do not stack, they refresh. Untyped, ignores DR, bloodless creatures immune (the Fatal Wound conventions). Source summary: 1500 bleed damage plus 4500 per 6 s (ambiguous).

## GURPS 4e
Follow-Up Toxic Attack (Follow-Up +0%) 2 HP per second for 3 seconds on the same d100.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Fatal Wound family (Affix Registry section 1).

## NAME COLLISION
Fatal Wound family (stacking bleed) and DMG Wounding; names stay, never merge.

## FORKS NEEDING A RULING
1. Degraded source (summary only); the '4500/6 sec' reading is ambiguous and the entry uses the smaller bleed. 2. Does not stack, unlike Fatal Wound.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: degraded.
