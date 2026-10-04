# DEMONSLAYING
**WoW weapon enchant — Profession, Classic (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Demonslaying)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Classic
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Demonslaying
tooltip: "Permanently enchant a melee weapon to have a chance of stunning and doing heavy damage to demons. Causes your weapon to become engulfed in flames, much like Fiery Weapon."
facts: enchanting skill 230-290; item level cap 136; reagents 1 Elixir of Demonslaying, 2 Rich Illusion Dust, 2 Large Brilliant Shard.
gaps: proc rate, stun length and damage amounts NOT PRESENT.
```

## D&D 3.5e
Against creatures with the demon subtype (tanar'ri, baatezu and other fiends the campaign names demons): +2d6 damage on every damaging hit (Banefire Magic-rung value, the 'heavy damage'), and on a 01-10 d100 the target is stunned 1 round, Fortitude DC 14 negates (Slowing/Dazing Magic-rung DC). Melee only.

## GURPS 4e
Innate Attack (Bane) 2d Follow-Up against demons, plus Affliction (Stunned) 1 second with a Quick Contest of the target's HT against effective skill 14.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Banefire (Elemental 93-96).

## NAME COLLISION
Dragondoom, Banefire family (names unrelated).

## FORKS NEEDING A RULING
1. Proc rate, stun length and damage amounts are not in the source; Banefire and Dazing Magic-rung values used. 2. 'Demon' means the demon subtype only; devils are a separate subtype (default: devils excluded).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
