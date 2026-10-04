# LIFE REGENERATION
**Diablo II weapon modifier — Magic affix ladder (PureDiablo) (https://www.purediablo.com/?p=3211)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Magic affix ladder (PureDiablo)
quality: clean
url: https://www.purediablo.com/?p=3211
tooltip: suffix "Regeneration" +3-5 life regeneration (req. 52).
facts: as returned.
gaps: the time unit of the regeneration NOT PRESENT.
```

## D&D 3.5e
While wielded the wielder has fast healing 1 (the Magic rung of the source's +3 to +5 life regeneration; the source gives no time unit). Fast healing is magical healing: it ends Fatal Wound stacks.

## GURPS 4e
Regeneration (slow) 1 HP per second while wielded, Gadget.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. The source's time unit is not given (the page says only '+3-5 life regeneration'); fast healing 1 is the Magic rung.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.
