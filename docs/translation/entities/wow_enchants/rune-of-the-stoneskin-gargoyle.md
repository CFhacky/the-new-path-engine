# RUNE OF THE STONESKIN GARGOYLE
**WoW weapon enchant — Death knight runeforging (https://warcraft.wiki.gg/wiki/Rune_of_the_Stoneskin_Gargoyle)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Death knight runeforging
quality: clean
url: https://warcraft.wiki.gg/wiki/Rune_of_the_Stoneskin_Gargoyle
tooltip: "Engrave your weapon with a rune that increases Armor by 5% and all stats by 5%." (current)
facts: level 8; cast time 5 seconds; patch 7.0.3 armor 4% to 5%, stat bonus changed from 2% Stamina to 5% all stats; patch 4.0.1 Defense 25 replaced with 4% Armor; patch 3.0.8 added. Page calls it the only recommended runeforge for death knight tanks.
gaps: original Wrath tooltip not retrieved.
```

## D&D 3.5e
While wielded: +1 untyped bonus to every ability score and +1 natural armor bonus to AC (the source's +5% Armor and +5% all stats, which on typical scores is about +1 each). Class lock as Razorice; the page calls it the death knight tank's rune.

## GURPS 4e
Attributes +1 each (ST, DX, IQ, HT) and DR +1 (Gadget), uncosted.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: Iron Skin (Defensive 19-24).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Percent stats to a flat +1 on every score is an interpretation; flagged. 2. Priced at +2 although the all-stat bonus is generous, to keep it Rare-rung.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
