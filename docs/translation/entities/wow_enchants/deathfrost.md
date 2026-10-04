# DEATHFROST
**WoW weapon enchant — Profession, Burning Crusade (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Deathfrost)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Burning Crusade
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Deathfrost
tooltip: "Permanently enchant a melee weapon to cause your damaging spells and melee weapon hits to occasionally inflict additional Frost damage and slow the target."
facts: spells 50% proc, 25-second internal cooldown; melee 10-12.5% proc, no internal cooldown; item level cap 600; slow does not work on targets level 73 or higher (patch 3.0.3); patch 2.4.0 added; patch 2.4.3 now procs off DoTs including Consecration; reagents 2 Primal Shadow, 2 Primal Water.
gaps: frost damage amount, slow amount and duration NOT PRESENT.
```

## D&D 3.5e
Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention). For spells: one d100 per damaging spell the wielder casts, 01-10, then not again for 4 rounds (the source's 25 s internal cooldown). On fire: +1d6 cold damage and the target's land speed is x0.7 for 1 round (Icy Chill precedent; the source gives neither amount). Procs off damage-over-time ticks (patch 2.4.3). No slow on creatures of 17+ Hit Dice.

## GURPS 4e
On the same d100: Innate Attack Burning [Cold] 1d Follow-Up, plus Affliction (Reduced Move 30%) 5 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Freezing (Elemental 09-16) + Slowing (Condition 01-08).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Frost damage and slow amounts are not in the source; Freezing Magic-rung 1d6 and the Icy Chill slow are used. 2. The source's 'no slow on level 73+' is read as no slow on Tier 1 creatures (17+ Hit Dice). 3. Spell proc is cut from the source's 50% to 10% per cast to match the ratified melee convention.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
