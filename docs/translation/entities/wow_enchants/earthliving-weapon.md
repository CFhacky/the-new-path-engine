# EARTHLIVING WEAPON
**WoW weapon enchant — Shaman imbue (https://warcraft.wiki.gg/wiki/Earthliving_Weapon)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Shaman imbue
quality: clean
url: https://warcraft.wiki.gg/wiki/Earthliving_Weapon
tooltip: "Imbue your weapon with the element of Earth for 1 hour. Your Riptide, Healing Wave, Healing Surge, and Chain Heal healing a 20% chance to trigger Earthliving on the target, healing for (138.915% of Spell power) over 6 sec."
facts: current retail version; 20% proc; 1 hour imbue, 6 second heal over time; patch 11.0.2 HoT duration 12 to 6 seconds and healing +75%.
gaps: Classic-era version not retrieved.
```

## D&D 3.5e
Proc: one d100 on each healing spell the wielder casts on a creature, 01-20 fires (the source's 20%). On fire the target also regains 3 HP at the start of each of its next 2 turns (the source's heal over 6 s at the Magic rung). Magical healing: ends Fatal Wound stacks.

## GURPS 4e
On the same d100 (per healing spell): Regeneration 3 HP at 3 seconds and again at 6 seconds.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Retail wording used; the Classic version was not retrieved.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `wow_translations.py` header. Extraction quality: clean.
