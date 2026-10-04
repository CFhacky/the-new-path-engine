# CHANCE TO CAST ON ATTACK
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "Gives a % Chance to Cast the listed Skill when making a melee attack hit check against a target"
facts: the attack need not hit, only be attempted; procced also by mercenaries, summons and monsters with gear; skill synergies apply; ranged weapons do not proc unless used by a shape-shifted druid; charged bolt and frozen orb originate from the attacker, all others from the target.
gaps: none.
```

## D&D 3.5e
Proc: one d100 on each attack roll the wielder makes with this weapon, hit or miss (the source triggers on the attack attempt), 01-10 fires. On fire the weapon casts a spell chosen at creation (level 1 to 3, caster level 5, normal save DC for the spell level), centered on the target or the wielder as the spell requires. Melee weapons only. Procs never proc other procs.

## GURPS 4e
On the same d100 per attack roll: the chosen spell as an Innate Attack, resisted as the spell requires.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
DMG Spell Storing (a caster loads the spell); this weapon casts a fixed spell by itself. Different; names stay.

## FORKS NEEDING A RULING
1. The cast skill is chosen at creation and the source's skill level scales; a fixed spell level 1 to 3 at caster level 5 is used. 2. The source's chance varies by item (5 to 25% in the search example); the ratified 10% is used.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.
