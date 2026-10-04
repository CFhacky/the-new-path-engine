## Tethered Levitating Storm-Charge Cell — Item Spec
```
PREFLIGHT
Skills loaded: surface-campaign-master-gm, campaign-document-builder, hybrid-research-invention, hybrid-magic-research, empire-operations-engine
Notion pages fetched: Crown Charge Site and Mobile Wedge — Documentation Plan (2026-10-04); LOG-817 Crown charge site rulings (2026-10-04); Deferred Dice — Crown storm nightly yield (2026-10-04); Echo-Crystal Capacitor (2026-05-31); Baen Light Vehicle Program (2026-07-08); Baen Light Vehicle — Bill of Materials and Sourcing (2026-07-08); Echo-Crystal Applications Program (2026-07-08); Unnatural Sandstorm (2026-08-20). Repo: docs/translation/FUSED_ENGINE_RESOLUTION.md (branch ccr-6d9e69ce-nd0fn0).
Deviations: none
```
> **Canon status — PROJECTED.** The Stormsonde is ruled workable (LOG-817, 4 Oct 2026). No sonde has been designed, built or flown in Jörmun's play. The R&D project and every item-creation check below are held in Deferred Dice until play authorizes them.

## Overview
A Stormsonde is an Echo-Crystal Capacitor cell in a louvred housing, held aloft in the unnatural sandstorm by a continuous levitation enchantment and tied to the ground by a conductive tether. While the storm carries lightning, the cell fills, and the charge runs down the tether into a node bus of the Crown Charge Array. Sondes come in two flying grades, Field and Standard. "Pillar grade" is not a flying sonde; it is the ground-mounted mast cell of the Stormring.

## How it works
- **Housing.** A crystal cradle inside a louvred shell that sheds the sand load, with a strike ring on top bonded to the tether.
- **Lifter.** A continuous *levitate* enchantment on the housing. It is the "high-mass lifter" of the ruling: CL 3 lifts up to 300 lb, which carries the body and the full hanging tether.
- **Tether.** A 400-ft conductive line with a crystal-thread core. It runs to a ground winch with a brake on the node bus. While the tether is intact, the cell counts as banked and loses ~0 a day. If the tether is cut, the cell is isolated and loses ~1 charge a day.
- **Intake.** The cell fills from storm lightning within ~60 ft at the ordinary-thunderstorm rate, a tenth of saturated, and only while lightning is active (bound ruling). Cells fill in parallel (Capacitor spec), so sondes flown near each other do not starve each other.
- **Strikes.** A sonde at 400 ft is the tallest thing in the storm. Each lightning-active hour it can take a direct strike. Each direct strike has a 10% chance to fail the levitation enchantment (bound ruling).

## Engineering Spec
<table header-row="true">
<tr><td>Grade</td><td>Cell</td><td>Body mass (cell + housing)</td><td>Tether (400 ft)</td><td>Lifted total</td><td>Intake while lightning is active</td><td>Cell capacity</td></tr>
<tr><td>Field</td><td>Field cell, 5 charges</td><td>18 + 13.5 = 31.5 lb</td><td>16 lb</td><td>47.5 lb</td><td>0.25 charge/h</td><td>5 charges</td></tr>
<tr><td>Standard</td><td>Standard cell, 25 charges</td><td>100 + 75 = 175 lb</td><td>16 lb</td><td>191 lb</td><td>0.3 charge/h</td><td>25 charges</td></tr>
<tr><td>Pillar</td><td>Not a flying grade (R2)</td><td>—</td><td>—</td><td>—</td><td>See Stormring — Structure Spec (ground mast cell)</td><td>120 charges</td></tr>
</table>

**Operating ceiling:** 400 ft on a 400-ft tether.

**Direct strikes:** 15% chance per sonde per lightning-active hour. On a strike, d100 ≤ 10 means the levitation fails.

**On a levitation failure (R11):** the enchantment is suppressed for 1d4 days. The sonde drops, and the winch brake arrests it after half the tether (200 ft). The cell is intact, but the housing needs 1 week of repair before the sonde can fly again. The sonde takes in nothing for the rest of that night.

**Expected yield (derived, GM guidance only):** lightning is active on 50% of nights (3d6 ≤ 10), for a mean of 3.5 h. That gives 1.75 lightning-hours a night and about 52 a month. A Field sonde averages about 13 charges a month, which is roughly one full recharge of the lent section (12.5 charges). A Standard sonde averages about 15.75. Each sonde averages about 0.8 levitation failures a month, and each failure grounds it for 1 to 2 weeks.

## D&D 3.5e
**Stormsonde, Field grade.** Wondrous item.
- Aura: strong evocation (cell, manufacture CL 13) and faint transmutation (levitation, CL 3). Slot: none.
- Price: **24,500 gp** (cell ~500 + continuous levitation 24,000).
- Weight: 31.5 lb body, 16 lb tether.
- Construction:
  - The cell is made as an Echo-Crystal Capacitor Field cell: charge-trapping fractal cut by a Craft specialist, a CL 13+ caster, and echo crystal.
  - The levitation needs Craft Wondrous Item and *levitate*.
  - Cost: 12,250 gp + 960 XP. Time: 24 days for the levitation enchantment.

**Stormsonde, Standard grade.** Wondrous item.
- Aura and slot as Field grade.
- Price: **26,500 gp** (cell ~2,500 + levitation 24,000).
- Weight: 175 lb body, 16 lb tether.
- Construction: cost 13,250 gp + 960 XP. Time: 24 days for the levitation.

**Levitation pricing (sourced formula).** Use-activated or continuous items cost spell level × caster level × 2,000 gp. *Levitate* is a 2nd-level spell at CL 3, which gives 12,000 gp. Its duration is 1 min/level, so a continuous item costs ×2, which gives 24,000 gp. Crafting is half the price, and the XP cost is 1/25 of the price.

**Item creation checks (hybrid-magic-research, custom item):**
- Design: Spellcraft DC 15 + CL 3 + 5 (unprecedented effect) = **DC 23**.
- Creation: Spellcraft DC 5 + CL 3 + 5 (unprecedented) = **DC 13**.
- On a failed creation, roll d8 on the creation complications table: Flawed, Cursed, Unstable, Sentient or Linked.

**Discharge:** a sonde is not a weapon platform. Its stored charge goes down the tether. A cell in a grounded sonde can burst like any capacitor cell (8d6 per charge, Reflex DC 22 half).

## GURPS 4e
No point totals (FUSED_ENGINE_RESOLUTION). The housing is Breakable (DR 6), the same as the capacitor cell. Levitation, intake and strike checks run on the 3.5e side and in the Charge Accounting procedure. A grounded cell bursting against a defender uses a Quick Contest of HT against an effective skill of 22, with armor DR applied before wounding.

## R&D project (hybrid-research-invention)
```
PROJECT: Stormsonde
TYPE: Applied (magic + technology)
COMPLEXITY: Complex — 10 successes (new application of known principles: Capacitor cell + levitation + tether bus)
LEAD RESEARCHER: Seliara Frostwind (Crystal Networks 15; Artificer 16)
RESOURCES: budget 50,000 gp (Complex band); Institut facilities
TIMELINE: 3–12 months at monthly cadence
PROGRESS: 0/10
STATUS: Not started — held in Deferred Dice until authorized in play
```
- **Cadence.** Infrastructure-scale projects roll monthly, and the effective-skill margin is capped at 16 (Light Vehicle Program convention).
- **Magic plus technology.** Each month, roll Thaumatology (Crystal Networks) and Engineering (Artificer) separately. Both must succeed for progress. A critical success on either gives full success. A critical failure on either causes a setback.
- **Results.** Success by 5+ gives 2 successes. Success gives 1. A margin of 0 gives 1 plus a d12 complication. Failure gives 0. Failure by 5+ loses 1. A critical failure loses 1d3 and rolls on the d8 setback table.
- **Seliara's availability.** A month counts only if she is available. Her monthly 3d6 vs 12 roll (Seliara month-miss rule) gates each project month. On a missed month the Athenaeum operator arrives the following month, and joint work takes the −2 penalty, which decays as ruled.

## Sourced
- Cell grades, capacities, fill rates, the parallel-fill rule, discharge, the Breakable DR 6 housing and manufacture CL 13: Echo-Crystal Capacitor.
- The ordinary-thunderstorm rate (0.25/h per Field cell), the 10% levitation failure per direct strike, and the sonde concept (levitated cell, tether, high-mass lifter): LOG-817.
- The monthly roll with margin cap 16: Light Vehicle Program.
- The complexity table, magic-plus-technology rule, result table and complications: hybrid-research-invention.
- Custom-item DCs and creation complications: hybrid-magic-research.
- The continuous-item price formula and duration multiplier: D&D 3.5e DMG magic-item pricing.

## Adjudicated (rolled 4 Oct 2026; Python secrets, four throws, lower median)
<table header-row="true">
<tr><td>Roll</td><td>Table</td><td>Throws</td><td>Bound result</td></tr>
<tr><td>R1a Field cell mass</td><td>3d6: 3-5 = 10 lb; 6-8 = 14; 9-12 = 18; 13-15 = 24; 16-18 = 30</td><td>11, 8, 11, 9</td><td>9: **18 lb**</td></tr>
<tr><td>R1b Standard cell mass</td><td>3d6: 3-5 = 60 lb; 6-8 = 80; 9-12 = 100; 13-15 = 120; 16-18 = 140</td><td>11, 8, 13, 12</td><td>11: **100 lb**</td></tr>
<tr><td>R2 Pillar-grade sonde aloft</td><td>3d6: 3-5 feasible aloft; 6-18 not feasible (Pillar grade = Stormring mast cell)</td><td>16, 13, 8, 15</td><td>13: **not feasible aloft**</td></tr>
<tr><td>R3 Operating ceiling / tether</td><td>3d6: 3-5 = 200 ft; 6-8 = 300; 9-12 = 400; 13-15 = 600; 16-18 = 800</td><td>15, 12, 14, 9</td><td>12: **400 ft**</td></tr>
<tr><td>R4 Direct-strike chance per sonde per lightning hour</td><td>3d6: 3-5 = 5%; 6-8 = 10%; 9-12 = 15%; 13-15 = 25%; 16-18 = 35%</td><td>12, 12, 12, 12</td><td>12: **15%**</td></tr>
<tr><td>R9 Housing mass</td><td>3d6: 3-5 = 25% of cell; 6-8 = 50%; 9-12 = 75%; 13-15 = 100%; 16-18 = 150%</td><td>14, 9, 9, 11</td><td>9: **75%**</td></tr>
<tr><td>R10 Tether mass</td><td>3d6: 3-5 = 2 lb/100 ft; 6-8 = 4; 9-12 = 6; 13-15 = 8; 16-18 = 12</td><td>8, 12, 12, 8</td><td>8: **4 lb per 100 ft**</td></tr>
<tr><td>R11 Levitation failure outcome</td><td>3d6: 3-5 enchantment destroyed, full fall, cell cracks and dumps; 6-8 destroyed, falls, cell survives on d100 ≤ 50; 9-12 suppressed 1d4 days, falls, brake arrests at half height, cell intact, housing 1 week repair; 13-15 suppressed 1d6 rounds, brake arrests, no damage; 16-18 flicker, no damage</td><td>11, 10, 6, 9</td><td>9: **suppressed 1d4 days; brake arrests at half height; housing 1 week repair**</td></tr>
</table>
Derived without a roll:
- The masses and the CL 3 lift requirement (100 lb/level, minimum CL 3 for a 2nd-level arcane spell).
- The prices.
- The Standard intake rate: ~3/h saturated ÷ 10 = 0.3/h.
- The expected-yield guidance.

## Open Rulings
- Mundane parts (housing shell, tether line, winch and brake) are unpriced. They are small against the 24,000 gp enchantment.
- A direct strike gives no extra yield. This page treats a strike as a hazard only.
- Housing hardness and hit points in 3.5e are not printed.
- Anchor spacing and tether-tangle risk in high wind.
- Whether the storm's makers can sense a sonde field (Hazard and Threat Annex, Wave 3, Doc 14).
