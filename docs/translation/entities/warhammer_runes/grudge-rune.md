# GRUDGE RUNE
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 203))**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 203)
tooltip: "For each Grudge Rune in your army, nominate one enemy character or monster at the beginning of the game. The wielder of a weapon engraved with a Grudge Rune gains +1 To Hit and can re-roll failed To Wound rolls in close combat when attacking the nominated model. Multiples of this rune have no further effect."
facts: cost 20 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
At the start of each encounter the wielder designates one enemy creature as a swift action; against it the wielder gets +1 on attack rolls and may once per round reroll one damage roll and keep the better. One designation per Grudge Rune carried; multiples have no further effect.

## GURPS 4e
Hunter's Mark accessibility (marked target only) with +1 skill and a damage reroll per second against it.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Hunter's Mark (Offensive 55-60).

## NAME COLLISION
Ranger favored enemy and MIC Hunting: different, names stay.

## FORKS NEEDING A RULING
1. 'Nominate at the beginning of the game' is read as at the start of each encounter.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.
