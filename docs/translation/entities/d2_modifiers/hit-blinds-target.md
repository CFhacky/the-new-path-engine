# HIT BLINDS TARGET
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "cast a level 1-20 dimvision on the target which Blinds it"
facts: blinds only normal and minion monsters; reduces monster awareness to melee range only (no skills or special abilities); chance, melee: 30 + 5(4 x {Hit Blinds Target sum} + {attacker level - defender level}), ranged: that / 3; dimvision level min((% chance - random(99)) / 5 + 1, 20); duration halved in Nightmare, quartered in Hell; if applied together with Flee, flee takes precedence.
gaps: base duration NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires. On fire the target is blinded for 1 round unless it succeeds on a Fortitude save (DC 14); a blinded creature can fight only at melee reach and cannot use special attacks or spell-like abilities at range. Creatures of 17+ Hit Dice are immune. Flee takes precedence if both effects fire.

## GURPS 4e
On the same d100: Quick Contest HT against effective skill 14; on failure Affliction (Blindness) for 6 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Blinding (Condition 43-48).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Duration is not in the source (1 round assumed, the Blinding row's value). 2. The source blinds on a plain hit; the pool row blinds on a crit.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.
