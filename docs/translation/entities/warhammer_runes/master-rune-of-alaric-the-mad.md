# MASTER RUNE OF ALARIC THE MAD
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 201))**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `wow_pipeline.py`; price +3 = 18,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 201)
tooltip: "A weapon engraved with the Master Rune of Alaric the Mad has the Ignores Armour Saves special rule."
facts: cost 40 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
The weapon's attacks ignore armor and shield bonuses to AC (including enhancement bonuses to that armor) and ignore worn DR (the engine's ignores-armor flag). Natural armor, Dex, dodge and deflection still apply. Unlike Brilliant Energy it harms undead, constructs and objects normally. Always on. Master rune: one per item and per army.

## GURPS 4e
The weapon's attacks skip worn DR (ignores_armor flag); the defender's 3d6 active defenses are unchanged.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+3 = 18,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Brilliant Energy (DMG, weapon-affix corpus) / Armor Piercing (Offensive 19-24).

## NAME COLLISION
DMG Brilliant Energy (+4, also passes through nonliving matter); different reach, names stay.

## FORKS NEEDING A RULING
1. 'Ignores Armour Saves' is read as ignore armor and shield AC plus worn DR; natural toughness stays.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.
