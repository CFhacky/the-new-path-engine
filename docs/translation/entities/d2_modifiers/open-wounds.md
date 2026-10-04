# OPEN WOUNDS
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "causes the target to begin Bleeding, applying damage and stopping damage regeneration for 8 seconds"
facts: applies only if monsters take damage or are regenerating; always applies to characters if the strike succeeds; damage effectiveness 1/2 for elites and act bosses, 1/4 for player characters (melee), 1/8 (ranged); no damage reduction can affect it; reapplication replaces the effect and resets the timer; duration cannot be reduced; life gain still works. Life drain per frame (1/256ths): level 1-15 9 x slvl + 31; 16-30 18 x slvl - 104; 31-45 27 x slvl - 374; 46-60 36 x slvl - 779; over 60 45 x slvl - 1319. Example: a level 50 character does 797.65 damage over 8 s (200 frames).
gaps: none.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires. On fire the target bleeds 3 HP at the start of its turn for 2 rounds (8 s) and for that time cannot regenerate or benefit from fast healing (magical healing still works). Untyped, ignores DR, bloodless creatures immune. A new proc refreshes the timer and does not stack. Against creatures of 17+ Hit Dice the bleed is 1 HP per round.

## GURPS 4e
On the same d100: Follow-Up Toxic Attack 6 HP spread over exactly 8 seconds; suppresses regeneration for 8 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Fatal Wound family (Affix Registry section 1) + Cursed Wound (Condition 55-60).

## NAME COLLISION
Fatal Wound family (stacking bleed) and DMG Wounding; names stay, never merge.

## FORKS NEEDING A RULING
1. The source's damage scales with the character level (about 800 over 8 s at level 50); a flat 3 per round is the Magic rung of the bleed rows. 2. D2's bleed does not stack, unlike Fatal Wound; kept.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.
