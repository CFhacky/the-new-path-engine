# FREEZE TARGET
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "Freezes normal or minions monsters, and applies Chill to all other targets as long as target is not Immune to Cold or have 0 Chill Effectiveness"
facts: only freezes normal and minion monsters; freeze or chill length random 1 to 9 seconds (25-225 frames), effectiveness 1/2 in Nightmare and 1/4 in Hell; chance, melee: 30 + 5(4 x {Freeze Target sum} + {attacker level - defender level}); ranged: that / 3; applied by any melee or ranged attack except blade sentinel, blade shield and extra multishot arrows.
gaps: none.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires. On fire the target must succeed on a Fortitude save (DC 14) or be held (frozen) for 1d2 rounds (the source's 1 to 9 seconds); on a success it is chilled instead (land speed x0.7, -1 on attacks, 1 round). Creatures of 17+ Hit Dice and creatures immune to cold are only chilled. Does not stack.

## GURPS 4e
On the same d100: Quick Contest of the target's HT against effective skill 14; on failure Affliction (Immobilized) for 1d6 seconds (source 1 to 9); on success or against Tier 1, Reduced Move 30% for 5 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Freezing (Elemental 09-16) + Slowing (Condition 01-08).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. The source's chance formula depends on the Freeze Target total and the level gap; it is replaced by the fixed DC 14 save. 2. 'Normal and minion monsters only' is read as creatures under 17 Hit Dice.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.
