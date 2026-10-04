# MARK OF WARSONG
**WoW weapon enchant — Profession, Warlords of Draenor (https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404))**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Warlords of Draenor
quality: degraded
url: https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404)
tooltip: (as summarized) +1000 haste, -10% every 2 sec.
facts: numbers only as summarized.
gaps: verbatim tooltip, proc rate, duration NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire: +2 on attack rolls in the first round, +1 in the second, nothing after (source summary: +1000 haste decaying 10% every 2 s). Untyped.

## GURPS 4e
On the same d100: +2 then +1 skill with weapon attacks over two seconds-rounds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Degraded source (summary only). 2. Decay stepped to two rounds.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: degraded.
