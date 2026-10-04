# How the fused combat engine resolves weapon affixes (binding for every draft in this folder)

Sources, all read this session:
- Notion **Talent Catalog, Combat Vocabulary** (`37ce8214-84b0-81d3-ab92-fb245a10f9a1`): Part VII (Fused Resolution Protocol), Part VIII (Numbers Standard), Part IX (engine rulings).
- `scripts/fused_round.py`, `scripts/conditions.py`, `scripts/combat_registry.py`.
- Notion **Sword of Zariel** (ratified artifact): shows how the campaign writes a holy/bane weapon.
- Notion Affix Registry, section 1 (Fatal Wound): shows how the Registry handles a name collision.

Where a draft in this folder disagrees with this file, this file wins. The drafts were written before I searched the engine.

## What the engine is
Inside combat the systems fuse: the 3.5e chassis does the action economy, d20 to-hit, HP, save DCs, threat range and crit multiplier. GURPS is only the defender's 3d6 contest against Parry/Block/Dodge (crits can't be defended) and DR. WFRP supplies stances, crit tables, Fury and morale. Item effects therefore run on the 3.5e side. GURPS is not a second place where an affix has to be rebuilt.

## What that settles

| Question I had raised | Engine answer |
|---|---|
| Does an extra-damage rider (+2d6, +1d6, and so on) get reduced by armor? | No. A **Rider** is "+2d6, ignores armor/DR". "Ignores armor" skips worn DR only, not natural toughness unless stated. This answers Holy, Unholy, Anarchic, Axiomatic, Bane, Magebane, the elemental-subtype weapons, Psibane and every other flat rider. |
| How do GURPS dice convert from 3.5e dice? | They don't convert. "Dice read as-is (shared d6 economy)." 2d6 is 2d, 1d6 is 1d. My conversions like 1d8 = 1d+1 or 2d6 = 2d-1 are superseded and should be ignored. |
| GURPS has no critical multiplier (Icy, Acidic, Screaming, Profane, Sacred, Maiming, Fiercebane bursts). | The engine uses the weapon's own 3.5e threat range and crit multiplier. A confirmed crit multiplies damage by the weapon's multiplier. Burst dice are chosen by that multiplier class, exactly as printed. No GURPS multiplier is needed. |
| Negative level for a wrong-aligned wielder (Holy, Unholy, Anarchic, Axiomatic, Aquan, Auran, Ignan, Terran, Psibane). | Use the 3.5e **Energy Drained** condition already in `conditions.py`: per negative level, -1 on attacks, saves, skill checks and ability checks, -5 HP, -1 effective level. It never converts to level loss from a held weapon. The defender's GURPS 3d6 roll is unaffected. My "-1 to all rolls" invention is replaced by this. |
| Alignment tag in GURPS. | Alignment lives on the 3.5e side of every stat block (for example a campaign port reads "Lawful Evil, Cleric of Lolth 11" next to its GURPS point total). A holy or bane weapon runs on the 3.5e chassis (see Sword of Zariel: "+2d6 holy", "against another evil creature only holy applies"). No GURPS alignment mechanism is built. |
| Conditions with a resist roll (shaken, stunned, paralyzed, slowed, blinded, banished). | The 3.5e save DC is what the book prints and stays fixed (flat-source). The GURPS crosswalk is a Quick Contest of the target's HT or Will against the effect's effective skill; the engine does not say how a printed DC maps onto that skill, so the table uses the printed DC as the effective skill. |
| Every-hit effects (Wounding, Vicious, Implacable, Energy Aura, Corrosive and the like) against the Registry's 10% proc norm. | The engine's Rider class is every weapon hit with no proc roll. A 10% proc is a Registry choice for stacking effects, not an engine rule. Every-hit effects as printed are normal. |
| Open GURPS point costs. | GURPS point totals are bookkeeping on character ports (Sword of Zariel carries "610 CP" for a bonded fighter). Affix entries need no GURPS point total. The ones I could not cost stay uncosted. |
| Armor-ignoring entries (Brilliant Energy, Impaling, Force, Transmuting). | Use the engine's `ignores_armor` flag, which skips worn DR. No Armor Divisor ladder is needed. |
| Name collisions (Berserker, Binding, Venomous, Weakening). | The Fatal Wound entry's own precedent: where a name matches an existing one, the names stay as listed, a collision note records it, and the mechanics never merge. Do not rename. |
| Prismatic Burst against PCs. | The campaign already carries prismatic spray as printed on its strongest NPC (the Empyrean sheet lists it at 1/day). Keep it as printed, with its spell saves. |

## What the engine does not settle (four decisions, with my ruling)
1. **Implacable** (+3, every hit, 2 per stack, no cap in the book). The Registry stacking doctrine says stacks are additive and a family with no cap entry just holds its maximum tick. An uncapped every-hit bleed is still a death spiral, so the ruling is: cap at 5 stacks, never on a weapon that also carries Fatal Wound, and any magical healing ends it.
2. **Vorpal** (decapitation on a confirmed natural 20). The engine already routes every confirmed crit to the location table, with head and neck results and a Lethal severity. Ruling: a confirmed natural-20 crit from a vorpal weapon forces the Head location at Lethal severity. This uses the existing table and needs no separate save. The engine does not say this explicitly; it is my reading of the table.
3. **Soulbreaker** (negative levels that can become permanent level loss). The engine's Energy Drained condition already says negative levels may become permanent when not purged. Ruling: NPC wielders use it as printed; against a PC the levels last 24 hours unless purged and never convert to level loss. The 24-hour delay in my reading of the scan is OCR-uncertain.
4. **Psionic and incarnum entries** (about ten). The engine has nothing on them. Ruling: register them as inactive until a psionic or incarnum character exists.

Keen versus the pool's x1.5 is a pool-row matter, not an engine matter; the pool row stays as ratified.
