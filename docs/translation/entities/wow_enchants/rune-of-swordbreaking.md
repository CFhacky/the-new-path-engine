# RUNE OF SWORDBREAKING
**WoW weapon enchant — Death knight runeforging (https://warcraft.wiki.gg/wiki/Rune_of_Swordbreaking)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Death knight runeforging
quality: clean
url: https://warcraft.wiki.gg/wiki/Rune_of_Swordbreaking
tooltip: "Affixes your one-handed rune weapon with a rune that increases Parry chance by 2% and reduces the duration of Disarm effects by 50%."
facts: level 63; cast time 5 seconds; patch 5.1.0 disarm reduction 60% to 50%; patch 4.0.6 50% to 60%; patch 3.0.2 added; removed 6.0.2.
gaps: none.
```

## D&D 3.5e
While wielded: +1 dodge bonus to AC (the source's +2% parry chance, at one step) and a +4 bonus on checks to avoid being disarmed, and a weapon the wielder is disarmed of can be recovered as a move action instead of a standard action (the source halves Disarm duration). One-handed weapons only.

## GURPS 4e
Enhanced Parry +1 and +4 to resist Disarm; recovery of a dropped weapon takes half the time.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Bladesinger (Skill/Class 31-36).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. The WoW disarm debuff (cannot use weapon for a time) is read as the 3.5e disarm maneuver; flagged.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
