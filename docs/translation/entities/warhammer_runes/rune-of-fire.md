# RUNE OF FIRE
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 202))**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `wow_pipeline.py`; price +1 / +2 / +3 = 2,000 / 8,000 / 18,000 gp by rune count (Magic / Rare / Unique))

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 202)
tooltip: "One Rune of Fire: the Flaming Attacks special rule. Two Runes: Flaming Attacks, and grants its wielder a Strength 4 Breath Weapon with the Flaming Attacks special rule. Three Runes: Flaming Attacks and a Strength 4 Breath Weapon that has the Flaming Attacks and Multiple Wounds (D3) special rules."
facts: cost 10/45/75 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
1 rune: Flaming Attacks (the Flaming row's +1d6 fire damage on a hit). 2 runes: also a breath weapon once per encounter, a 15-ft cone of 2d6 fire (Reflex DC 14 half). 3 runes: the breath weapon is 3d6 and the burned target takes one further 1d6 fire damage at the start of its next turn (Multiple Wounds (D3), read as a second damage roll).

## GURPS 4e
Innate Attack Burning 1d Follow-Up on every damaging hit (1 rune); plus an Innate Attack Burning cone 2d once per encounter (2 runes); 3d plus a second 1d the next second (3 runes).

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 / +2 / +3 = 2,000 / 8,000 / 18,000 gp by rune count (Magic / Rare / Unique) (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Flaming (Elemental 01-08) + Elemental Burst (Elemental 75-80).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Strength 4 breath weapon is read as 2d6 / 3d6 by the Elemental Burst Magic and Rare values.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.
