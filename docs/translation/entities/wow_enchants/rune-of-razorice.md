# RUNE OF RAZORICE
**WoW weapon enchant — Death knight runeforging (https://warcraft.wiki.gg/wiki/Rune_of_Razorice)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Death knight runeforging
quality: clean
url: https://warcraft.wiki.gg/wiki/Rune_of_Razorice
tooltip: "Engrave your weapon with a rune that causes (1.127% of Attack power) extra weapon damage as Frost damage and increases enemies' vulnerability to your Frost attacks by 3%, stacking up to 5 times."
facts: level 8, cast time 5 seconds; debuff Razorice: Frost damage taken from the Death Knight's abilities +3% per stack, 20 seconds, max 5 stacks; patch 3.3.3 changed from 10 stacks of 1% to 5 stacks of 2%.
gaps: proc NOT PRESENT (it is an every-hit effect).
```

## D&D 3.5e
Every damaging melee hit adds +1d6 cold damage (the Freezing Magic-rung value; source 1.127% of attack power as extra Frost damage) and one Razorice stack on the target, up to 5 stacks, each stack lasting 4 rounds (20 s). While the target holds 2 or more stacks the wielder's cold damage against it gains +1 per damage roll; at 4 or more, +2 (the source's 3% per stack vulnerability, at about 15% on the full 5, read as +1 per 2 stacks). Class lock: runeforging is a Death Knight craft.

## GURPS 4e
Innate Attack Burning [Cold] 1d Follow-Up on every damaging hit; stacks as the 3.5e side; +1 damage on cold attacks at 2 stacks, +2 at 4, for exactly 20 seconds from the last stack.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Freezing (Elemental 09-16) + Vulnerability (Condition 73-78).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Percent vulnerability to flat damage is an interpretation, flagged. 2. Death Knight runeforging has no 3.5e class; the rune is usable only by a wielder the GM rules a rune-smith.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
