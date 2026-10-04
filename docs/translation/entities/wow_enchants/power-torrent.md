# POWER TORRENT
**WoW weapon enchant — Profession, Cataclysm (https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Power_Torrent)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Profession, Cataclysm
quality: clean
url: https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Power_Torrent
tooltip: "Permanently enchant a weapon to sometimes increase Intellect by 83 for 12 sec when dealing damage or healing with spells."
facts: internal cooldown 45 seconds; approximately 33% proc; item level cap 136; patch 4.0.3a added.
gaps: none.
```

## D&D 3.5e
Proc: one d100 on each damaging or healing spell the wielder casts, 01-10 fires, then not again for 8 rounds (the source's 45 s internal cooldown). On fire: +2 Intelligence (untyped) for 2 rounds (source +83 Intellect, 12 s).

## GURPS 4e
On the same d100: IQ +1 for exactly 12 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Source proc is about 33%; cut to 10% per cast.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
