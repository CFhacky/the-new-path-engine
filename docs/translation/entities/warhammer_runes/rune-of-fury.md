# RUNE OF FURY
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 203))**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `wow_pipeline.py`; price +1 / +2 / +3 = 2,000 / 8,000 / 18,000 gp by rune count (Magic / Rare / Unique))

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 203)
tooltip: "One Rune of Fury grants its wielder +1 Attack. Two Runes: +1 Attack and the Frenzy special rule. Three Runes: +1 Attack and Frenzy and, after each successful roll To Hit and To Wound, it grants its user another Attack; roll To Hit and To Wound as normal. Attacks generated this way do not generate further Attacks."
facts: cost 15/30/60 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
1 rune: +1 Attack, an extra attack at the highest base attack bonus once per day as a swift action (Rapid Assault T5). 2 runes: three times per day, plus the Frenzy special rule read as rage (+2 Str, -2 AC, must engage) once per encounter. 3 runes: an extra attack at will, rage, and after each hit that deals damage the weapon grants one further attack (the further attacks do not chain).

## GURPS 4e
Altered Time Rate (limited uses 1/day, 3/day, at will matching 3.5e) plus Berserk at 2 and 3 runes.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 / +2 / +3 = 2,000 / 8,000 / 18,000 gp by rune count (Magic / Rare / Unique) (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Rapid Assault (Offensive 25-30).

## NAME COLLISION
DMG Speed (+3, an extra attack on every full attack); different cadence, names stay.

## FORKS NEEDING A RULING
1. '+1 Attack' every round would match DMG Speed; here it follows Rapid Assault's limited-use ladder to keep the price at +1 / +2 / +3.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.
