# MASTER RUNE OF DEATH
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 201))**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `wow_pipeline.py`; price +3 = 18,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 201)
tooltip: "A weapon engraved with the Master Rune of Death grants its wielder the Heroic Killing Blow special rule."
facts: cost 40 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
Heroic Killing Blow: on a confirmed natural 20 the engine forces a Lethal-severity result on the location table (the same table as the Vorpal ruling), against a target of any size. Not a death effect and no separate save. Master rune.

## GURPS 4e
On a confirmed critical hit, the same Lethal-severity location result; no size limit.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+3 = 18,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Vorpal (DMG, weapon-affix corpus ruling).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Vorpal forces the Head; this rune forces Lethal severity on the rolled location (less reliable, reflecting the lower cost), per the engine's crit table.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.
