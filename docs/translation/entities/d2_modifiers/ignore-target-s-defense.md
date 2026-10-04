# IGNORE TARGET'S DEFENSE
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 2 — Heroic Elite (levels 13-16)** (rule in `wow_pipeline.py`; price +3 = 18,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "Calculates attacks made on normal, minion monsters, or Character Summons as having 0 Defense"
facts: only for attacks made with that weapon; does not work on player characters, mercenaries, elites or act bosses.
gaps: none.
```

## D&D 3.5e
Melee and ranged. The wielder's attacks with this weapon against creatures of under 17 Hit Dice (the source's normal and minion monsters and character summons; not player characters, mercenaries, elites or bosses) resolve as touch attacks (the target's armor, shield and natural armor bonuses to AC are ignored; Dex, dodge and deflection still apply). Always on, no d100.

## GURPS 4e
The defender's Parry, Block and Dodge are rolled at -3 (a defender with 0 Defense in the source rolls as undefended); against Tier 1 targets and player characters the weapon has no effect.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+3 = 18,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. 'Defense 0' is read as a touch attack on the 3.5e side and as a -3 to the defender's 3d6 contest on the GURPS side (the engine does not name this mechanism). 2. Priced at +3: an always-on touch attack is stronger than MIC Impaling's 3/day at +1.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.
