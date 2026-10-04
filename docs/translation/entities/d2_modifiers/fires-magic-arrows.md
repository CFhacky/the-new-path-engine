# FIRES MAGIC ARROWS
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "Replaces any standard Attack with magicarrow with Skill Level determined by the weapon source"
facts: does not apply if a skill is used with the weapon; source levels: M'avina's Caster 1, Witherstring 3, Wizendraw 5, Widowmaker 11, Witchwild String 20.
gaps: Magic Arrow damage numbers NOT PRESENT.
```

## D&D 3.5e
Ranged weapons only. Every damaging hit counts as magic and deals +1d4 force damage (the Magic-rung value; the source gives no Magic Arrow damage). Force damage ignores DR/X and incorporeal miss chances. No d100.

## GURPS 4e
Innate Attack (Crushing [Cosmic]) 1d Follow-Up on every damaging hit, ignoring worn DR.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Magic Arrow damage and the item source levels (1 to 20) are not in the source; value is design. 2. Force is the closest 3.5e reading of D2's 'magic' damage.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.
