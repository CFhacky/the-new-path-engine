# MARK OF THE THUNDERLORD
**WoW weapon enchant — Profession, Warlords of Draenor (https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404))**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Warlords of Draenor
quality: degraded
url: https://warcraft.wiki.gg/wiki/Enchantments_by_slot (own page returned 404)
tooltip: (as summarized from the truncated slot page) +500 crit for 6 sec, crits extending duration.
facts: numbers only as summarized; no tooltip wording.
gaps: verbatim tooltip, proc rate, caps NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire for 1 round (6 s): +2 on rolls to confirm critical hits; each confirmed critical hit during it extends the effect by 1 round, up to 3 rounds in all (source summary: +500 crit for 6 s, crits extend the duration).

## GURPS 4e
On the same d100: +1 to critical-hit confirmation, extended 1 second-round per crit, exactly 6 seconds base.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Degraded source: only a summary of the numbers was retrieved; no verbatim tooltip, no proc rate.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: degraded.
