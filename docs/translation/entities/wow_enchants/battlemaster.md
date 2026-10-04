# BATTLEMASTER
**WoW weapon enchant — Profession, Burning Crusade (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Battlemaster)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Burning Crusade
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Battlemaster
tooltip: "Permanently enchant a melee weapon to occasionally heal nearby party members for 76 to 126 when attacking in melee."
facts: "Proc rate is 1 PPM melee only" (testing data approximately 1.5-1.8% per swing); item level cap 600; reagents 8 Void Crystal, 8 Large Prismatic Shard, 2 Primal Water.
gaps: patch changes NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire every ally within 30 ft, wielder included, is healed 5 HP (the Crusader Magic-rung heal; source 76 to 126 healing, a little over a third of Crusader's 240). Magical healing: ends Fatal Wound stacks. Melee hits only.

## GURPS 4e
On the same d100: Regeneration burst of 5 HP to each ally within 10 yards, at once.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Heal is the Magic-rung 5; source ratio to Crusader is about 0.4, which rounds to the same step.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
