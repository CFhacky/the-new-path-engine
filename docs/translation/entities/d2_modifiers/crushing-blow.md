# CRUSHING BLOW
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "deals additional damage prior to the attack's damage, equal to a fraction of the remaining Life total of the target"
facts: formula 1/4 of current Life / (0.5 + 0.5N), N = players in game up to 8; critical hits do not increase it; affected by the target's Damage Resist and Damage Reduced by %; not affected by -% Damage Resistance; integer Damage Reduced does not reduce it; Sanctuary does not protect Immune-to-Physical undead.
gaps: per-item chance values not on this page (the search snippet shows Bloodtree Stump at 50%).
```

## D&D 3.5e
Proc: one d100 on each damaging melee hit, 01-10 fires. On fire the target takes extra damage equal to one quarter of its current hit points, maximum 25, before normal damage. Not multiplied on a critical hit; ignores DR/X; reduced by percentage-type resistances; creatures immune to physical damage take none. Creatures of 17+ Hit Dice take one eighth of current hit points instead (maximum 25).

## GURPS 4e
Crushing Attack (Follow-Up) on the same d100: injury equal to 1/4 of the target's current HP, maximum 25 HP, applied after DR; against Tier 1 targets 1/8.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
Pool 'Lethal Focus' (crit bonus) and DMG Mighty Cleaving: different mechanics.

## FORKS NEEDING A RULING
1. The source gives no cap and halves the fraction for some enemies only by difficulty; the 25 cap and the Tier 1 eighth are design values. 2. Chance per item varies in the source (the search shows Bloodtree Stump at 50%); the ratified 10% proc is used.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.
