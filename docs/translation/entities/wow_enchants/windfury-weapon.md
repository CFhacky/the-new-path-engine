# WINDFURY WEAPON
**WoW weapon enchant — Shaman imbue (https://warcraft.wiki.gg/wiki/Windfury_Weapon)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Shaman imbue
quality: clean
url: https://warcraft.wiki.gg/wiki/Windfury_Weapon
tooltip: "Imbue your main-hand weapon with the element of Wind for 1 hour. Each main-hand attack has a 25% chance to trigger two extra attacks, dealing (27.945% of Attack power) Physical damage each."
facts: current retail version (patch 12.0.0); 25% proc; no internal cooldown but cannot proc off itself; duration 1 hour; many damage retunes 9.0.2 to 12.0.0.
gaps: the Classic-era tooltip was not retrieved.
```

## D&D 3.5e
On each main-hand hit, d100 01-25 fires (the source's 25%): the wielder immediately makes two extra melee attacks at the highest base attack bonus with the same weapon. The extra attacks cannot fire Windfury (source: cannot proc off itself). Melee main-hand weapon only.

## GURPS 4e
On the same d100: two extra attacks at the full weapon skill, same weapon; the extra attacks cannot trigger the effect again.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Rapid Assault (Offensive 25-30).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. The Classic-era tooltip was not retrieved; the current retail wording (25%, two attacks) is used. 2. Priced below DMG Speed (+3): 25% of two attacks is half an extra attack per hit.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
