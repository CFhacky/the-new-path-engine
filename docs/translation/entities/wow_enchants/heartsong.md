# HEARTSONG
**WoW weapon enchant — Profession, Cataclysm (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Heartsong)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Cataclysm
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Heartsong
tooltip: "Permanently enchant a weapon to sometimes increase Versatility by 30 for 15 sec when healing or dealing damage with spells."
facts: 20-second internal cooldown, approximately 25% proc; item level cap 136; reagents 9 Hypnotic Dust, 3 Greater Celestial Essence, 3 Heavenly Shard, 3 Volatile Life.
gaps: none.
```

## D&D 3.5e
Proc: one d100 on each damaging or healing spell the wielder casts, 01-10 fires, then not again for 3 rounds (the source's 20 s internal cooldown). On fire for 3 rounds (15 s): +1 untyped bonus to spell damage and to healing done, and the wielder takes 1 less damage from each hit (the source's Versatility +30 turns damage done, healing done and damage taken one step each).

## GURPS 4e
On the same d100: +1 damage on the wielder's spell attacks, +1 HP on healing, DR 1 against hits, exactly 15 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Versatility to three +1 steps is an interpretation; flagged. 2. Source proc about 25%; 10% used.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
