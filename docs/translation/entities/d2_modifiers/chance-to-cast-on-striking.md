# CHANCE TO CAST ON STRIKING
**Diablo II weapon modifier — Attack modifier (Maxroll) (https://maxroll.gg/d2/resources/attack-modifiers)**
**Tier 3 — Heroic (levels 9-12)** (rule in `wow_pipeline.py`; price +2 = 8,000 gp)

## SOURCE (as fetched; see packet header: extraction, not byte-exact)
```
group: Attack modifier (Maxroll)
quality: clean
url: https://maxroll.gg/d2/resources/attack-modifiers
tooltip: "Gives a % Chance to Cast the listed Skill when making a melee attack hit check that succeeds, and hit is not Blocked or Dodged"
facts: the attack must hit but need not deal damage; venom and enchant are cast on the attacker; poison nova and static field centre on the attacker; directional skills (firestorm, twister, tornado, bone spirit, charged bolt, frozen orb) cast toward the target from the attacker; all others originate at the target. Search example: "5% Chance To Cast Level 18 Volcano On Striking".
gaps: none.
```

## D&D 3.5e
Proc: one d100 on each successful hit with this weapon (the hit must connect and not be blocked or dodged; damage is not required), 01-10 fires. On fire the weapon casts a spell chosen at creation (level 1 to 3, caster level 5, normal save DC), centered on the target (self-centered spells such as a nova or an aura center on the wielder). Melee weapons only.

## GURPS 4e
On the same d100 per successful strike: the chosen spell as an Innate Attack.

**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).

## PRICE
+2 = 8,000 gp (bonus-equivalent squared x 2,000 gp; Crusader rate card).

## POOL COVERAGE / DEDUPE
Verdict: NEW. Existing row: none.

## NAME COLLISION
Chance to Cast on Attack (same corpus), DMG Spell Storing: different triggers and sources; names stay.

## FORKS NEEDING A RULING
1. Same fixed-spell reading as Chance to Cast on Attack. 2. Differs from it only in needing a connecting hit.

## CONVERSION NOTES
Anchor: Crusader (ratified, Registry section 2). Conventions: `d2_translations.py` header. Extraction quality: clean.
