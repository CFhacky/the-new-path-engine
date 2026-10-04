# RUNE OF DAEMON SLAYING
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 202))**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `wow_pipeline.py`; price +1 / +2 / +3 = 2,000 / 8,000 / 18,000 gp by rune count (Magic / Rare / Unique))

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 202)
tooltip: "Against any model with the Daemonic special rule, a weapon engraved with a Rune of Daemon Slaying receives a +1 bonus To Hit and To Wound. With two Runes: +1 To Hit and To Wound and the Multiple Wounds (D3) special rule. With three Runes: hits and Wounds on a roll of 2+, has Multiple Wounds (D3) and no ward saves can be taken against it."
facts: cost 25/50/100 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
Against creatures with the demon, devil or daemon subtype (the Daemonic rule). 1 rune: +1 effective enhancement bonus and +1d6 damage. 2 runes: +2 effective enhancement, +2d6, and one extra roll of the weapon's damage dice on a damaging hit (Multiple Wounds (D3), read as one extra roll). 3 runes: hits on a natural 2 or higher, +4d6, one extra damage roll, and the target's SR, ward and deflection bonuses do not apply (no ward saves).

## GURPS 4e
Innate Attack (Bane) 1d / 2d / 4d against daemons, with the extra injury roll at 2 and 3 runes; at 3 runes no ward or Magic Resistance applies.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 / +2 / +3 = 2,000 / 8,000 / 18,000 gp by rune count (Magic / Rare / Unique) (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Banefire (Elemental 93-96).

## NAME COLLISION
WoW Demonslaying and Damage vs Demons (D2): names stay.

## FORKS NEEDING A RULING
1. 'Daemonic' read as the demon, devil or daemon subtype; default includes devils.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.
