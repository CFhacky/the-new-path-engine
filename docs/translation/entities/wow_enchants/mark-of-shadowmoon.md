# MARK OF SHADOWMOON
**WoW weapon enchant — Profession, Warlords of Draenor (https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404))**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Warlords of Draenor
quality: degraded
url: https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404)
tooltip: (as summarized) +500 spirit for 15 sec.
facts: numbers only as summarized.
gaps: verbatim tooltip, proc rate NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire the wielder gains fast healing 1 for 3 rounds (source summary: +500 spirit for 15 s; Spirit is a regeneration stat). Fast healing is magical healing: ends Fatal Wound stacks.

## GURPS 4e
On the same d100: Regeneration (slow) 1 HP per second for exactly 15 seconds, capped at the 3.5e total.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Degraded source (summary only). 2. Spirit to fast healing 1 is an interpretation; flagged.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: degraded.
