# MASTER RUNE OF BREAKING
**Warhammer Dwarf weapon rune — Weapon rune (WFB Dwarf runic item) (D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 201))**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Weapon rune (WFB Dwarf runic item)
quality: clean
url: D:\Backup\I-drive\Sourcebooks\_text\Warhammer\Fantasy Army Books\Warhammer Armies_ Dwarfs - PDF Room.md (PDF page 201)
tooltip: "If a Dwarf with a weapon engraved with the Master Rune of Breaking scores one or more successful hits against a model with a magic weapon, the foe's magic weapon is destroyed on a D6 roll of 2+ (roll once, regardless of the number of successful hits). A foe with a destroyed magic weapon counts as being armed with a hand weapon. If the foe has more than one magic weapon (Paired weapons count as one), roll a D6 to randomly determine which one is destroyed."
facts: cost 25 points; [lore omitted].
gaps: none.
```

## D&D 3.5e
On a damaging hit against a creature wielding a magic weapon, that weapon must succeed on a Fortitude save (the owner's save bonus, DC 20) or be destroyed; one check per round. A creature with several magic weapons risks one at random. Artifacts are immune. A creature whose weapon is destroyed is armed with an ordinary weapon of the same kind. Master rune.

## GURPS 4e
On the same hit: Quick Contest of the weapon owner's HT against effective skill 20; on failure the weapon breaks.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
Sunder (a combat maneuver) and MIC Sundering (extra damage on sunder): different, names stay.

## FORKS NEEDING A RULING
1. 'D6 roll of 2+' (about 83%) is replaced by a DC 20 save so a well-built weapon can resist. 2. Default applies to NPC weapons; whether it can break a PC's magic weapon is a GM call (default: yes, with the save).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: clean.
