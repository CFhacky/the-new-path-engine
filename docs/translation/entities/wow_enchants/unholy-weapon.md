# UNHOLY WEAPON
**WoW weapon enchant — Profession, Classic (https://warcraft.wiki.gg/wiki/Unholy_Weapon)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Classic
quality: clean
url: https://warcraft.wiki.gg/wiki/Unholy_Weapon
tooltip: "Permanently enchant a melee weapon to often inflict a curse on the target, inflicting Shadow damage and reducing their melee damage."
facts: enchanting skill 295-300; item level cap 136; reagents 4 Essence of Undeath, 4 Large Brilliant Shard; patch 3.3.0 (2009-12-08): now inflicts Shadow damage in addition to its original effect. Secondary (search): the curse reduces the target's damage by 15 and lasts 12 seconds.
gaps: proc rate NOT PRESENT; shadow damage amount NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). On fire the target takes 1d4 negative-energy damage (the shadow damage added in patch 3.3.0; the amount is not in the source, so this is the Shadowtouch Magic-rung value) and a curse: -2 on its melee damage rolls for 2 rounds (source: -15 damage, 12 s). No save, no SR; undead take the negative damage as Shadowtouch does (half).

## GURPS 4e
Innate Attack Toxic [Cosmic] 1d Follow-Up on the hit, plus Affliction (Weakened: -2 damage on the target's melee attacks), exactly 12 seconds. Same d100.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
DMG/Registry affix 'Unholy' (alignment weapon, +2d6 vs good): different mechanic; names stay, never merge. Pool 'Weakening' (-Str) is also different.

## FORKS NEEDING A RULING
1. Shadow damage amount and proc rate are not in the source; values are Magic-rung design values.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
