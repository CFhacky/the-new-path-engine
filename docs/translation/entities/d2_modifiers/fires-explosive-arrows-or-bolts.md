# FIRES EXPLOSIVE ARROWS OR BOLTS
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 4 — Competent (levels 5-8)** (rule in `wow_pipeline.py`; price +1 = 2,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "replaces any standard Attack with explodingarrow with Skill Level determined by the weapon source"
facts: does not apply if a skill is used with the weapon; weapon source levels: Raven Claw 3, Hellcast 5, Demon Machine 6, Kuko Shakaku 7, Blood Raven's Charge 13, Brand 15.
gaps: Exploding Arrow damage numbers NOT PRESENT.
```

## D&D 3.5e
Ranged weapons only. Each damaging hit also bursts in a 5-ft radius around the target for 1d6 fire damage, Reflex DC 13 half (the Magic-rung value; the source gives no Exploding Arrow damage). No d100; every hit. Does not apply when the wielder uses a skill-based shot.

## GURPS 4e
Innate Attack (Burning, Explosion 1) 1d on every damaging hit, centered on the target.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+1 = 2,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: DELTA. Existing row: Elemental Burst (Elemental 75-80).

## NAME COLLISION
none.

## FORKS NEEDING A RULING
1. Exploding Arrow damage and the item source levels (3 to 15) are not in the source; the Elemental Burst Magic-rung scale is used. 2. Elemental Burst triggers on a crit; this entry triggers on every hit (that is the delta).

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.
