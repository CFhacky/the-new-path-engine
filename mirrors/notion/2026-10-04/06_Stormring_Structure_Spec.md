## Ground-Mounted Pillar Intake Ring — Structure Spec
```
PREFLIGHT
Skills loaded: surface-campaign-master-gm, campaign-document-builder, hybrid-research-invention, hybrid-magic-research, empire-operations-engine
Notion pages fetched: Crown Charge Site and Mobile Wedge — Documentation Plan (2026-10-04); LOG-817 Crown charge site rulings (2026-10-04); Echo-Crystal Capacitor (2026-05-31); construction-sub-routine (2026-09-28); Frontier Installation Phase Advancement Framework (2026-09-28); Baen Light Vehicle — Bill of Materials and Sourcing (2026-07-08); Eastern Anauroch — Frostborn Legate Region (2026-08-30); Crown of Eight Springs (2026-09-28); Holdings & strongholds rulings D1–D18 (2026-09-29). Repo: docs/translation/FUSED_ENGINE_RESOLUTION.md (branch ccr-6d9e69ce-nd0fn0).
Deviations: none
```
> **Canon status — PROJECTED.** Nothing here is built or funded in Jörmun's play. The Stormring is Phase C of the Expansion Roadmap. Construction complications are held in Deferred Dice.

## Overview
The Stormring is the fixed, ground-level intake for the Crown node. A Pillar cell (120 charges) stands on the ring floor under a 60-ft lightning mast, inside a louvred ring wall that keeps the sand off the crystal. Pillar cells cannot fly (R2), so this is how the Array gets Pillar-grade intake. The ring has no levitation enchantment, so it carries none of the sondes' strike-failure risk. Its weaknesses are that it is fixed, visible and a single point of failure. It is a small-scale installation (R7b).

## Components
<table header-row="true">
<tr><td>Component</td><td>Spec</td><td>Cost</td><td>Source</td></tr>
<tr><td>Pillar cell</td><td>Fixed 12-ft vault pillar, 120 charges, at the ring's center</td><td>~12,000 gp market (~6,000 craft)</td><td>Capacitor spec</td></tr>
<tr><td>Mast</td><td>60-ft lightning mast with a strike terminal, bonded to the Pillar cell. The terminal sits at the edge of the cell's ~60-ft intake reach</td><td>In civil works</td><td>Derived from the intake reach</td></tr>
<tr><td>Ring wall with louvres</td><td>120-ft inside diameter (twice the intake reach), louvred to shed sand load while letting the storm through</td><td>In civil works</td><td>Derived; civil works rolled (R7a)</td></tr>
<tr><td>Intake ring</td><td>8 receptive-cut coupling shards set in the wall at ~47-ft intervals around the ~377-ft circumference</td><td>8 × 400 = 3,200 gp</td><td>BOM (shard price); count derived</td></tr>
<tr><td>Crystal apron</td><td>Paved floor between the Pillar and the wall, carrying the shard lines to the bus</td><td>In civil works</td><td>—</td></tr>
<tr><td>Bus coupling</td><td>One network node module joining the Pillar cell to the Crown node bus</td><td>800 gp</td><td>BOM</td></tr>
<tr><td>Surge line</td><td>Buried run from the ring to the Crown bank</td><td>In civil works</td><td>—</td></tr>
</table>

**Total (market crystal prices): 15,000 civil works + 12,000 Pillar + 3,200 shards + 800 module = 31,000 gp.** If the Pillar cell is crafted in-house at half price, the total is 25,000 gp.

**Intake (derived).** While lightning is active the Pillar cell fills at ~0.33 charges/h (120 charges per ~36 h saturated, ÷ 10). That is about 17.5 charges a month at the expected 52 lightning-hours, which is better than one Standard sonde, with no strike-failure losses. Its intake passes through the same 5 charges/h node bus.

## Construction (empire-operations-engine, construction sub-routine)
- **Build time:** 1 week per 10,000 gp. 31,000 gp is **about 3.1 weeks** of SBG work.
- **Formicorps:** ×3 speed, no cost cut, so about 1 week. Formicorps are available from Flamerule 1496 (D3).
- **Caster discounts (Table 1-5):**
  - *Wall of stone* can cut the hewn-stone ring wall by 15% at CL 9, 50% at CL 12, and to free at CL 16+. The discount applies to the wall share of the 15,000 gp civil works only.
  - The *levitate* discount (−25% of height cost) can apply to the mast.
  - Seliara's *fabricate* applies to fittings.
- **Underground:** the surge line is buried. Hewn stone underground costs nothing, which is a site modifier.
- **Complications:** roll a d20 per project at each phase boundary or quarterly, using the sub-routine table (1-2 major; 3-5 minor; 6-8 supply; 9-15 on schedule; 16-18 ahead; 19 discovery; 20 breakthrough). Modifiers: Formicorps +2, Kalnar Stonebrow supervising +2, contested territory −2. **Held in Deferred Dice.**
- **Pillar cell:** this is manufactured crystal on its own crafting track, like wondrous architecture. It is installed once the ring is built and needs a CL 13+ caster plus the fractal-cut specialist.
- **Keying:** Seliara keys the ring to the Crown bus. Her hours fall under the month-miss rule.

## Siting
- The ring sits outside the sacred spring precinct (Legate Region; drawn on the Crown addendum, Doc 9).
- It sits away from the bank and the bays, because a Pillar cell is a demolition event if it dumps.
- It needs open ground on the storm's approach side, clear of the eagle aerie on the crest.

## D&D 3.5e
**Stormring (structure).**
- The Pillar cell is a manufactured wondrous item (manufacture CL 13). Burst: 8d6 per charge, Reflex DC 22 half, up to 5 charges per pulse.
- Overload (more than 5 at once): Fort-equivalent DC 18 or the cell cracks.
- Catastrophic dump: a full 120-charge Pillar releases area discharge that scales with its stored charge (Capacitor spec). Treat the ring as a demolition hazard.

## GURPS 4e
No point totals (FUSED_ENGINE_RESOLUTION). The Pillar cell housing is Breakable (DR 6), per the Capacitor spec. Ring-wall DR follows the wall material chosen at build. Bursts resolve on the 3.5e side, with a Quick Contest of HT against an effective skill of 22 for the printed save.

## Sourced
- Pillar cell grade, price, intake reach and discharge: Echo-Crystal Capacitor.
- Shard and node-module prices: Bill of Materials.
- Build rate, Formicorps, caster discounts, complications table and modifiers: construction sub-routine.
- Phase 2 small-installation capital band (12,000–25,000 gp): Frontier Installation Phase Advancement Framework.
- Sacred springs: Legate Region.
- Aerie: Crown of Eight Springs.

## Adjudicated (rolled 4 Oct 2026; Python secrets, four throws, lower median)
<table header-row="true">
<tr><td>Roll</td><td>Table</td><td>Throws</td><td>Bound result</td></tr>
<tr><td>R2 Pillar-grade sonde aloft</td><td>3d6: 3-5 feasible; 6-18 not feasible (Pillar grade is the ground mast cell)</td><td>16, 13, 8, 15</td><td>13: **Pillar grade is ground-mounted**</td></tr>
<tr><td>R7a Civil works base</td><td>3d6 across the Frontier Phase 2 band: 3-5 = 12,000; 6-8 = 15,000; 9-12 = 18,000; 13-15 = 21,000; 16-18 = 25,000</td><td>6, 8, 7, 9</td><td>7: **15,000 gp**</td></tr>
<tr><td>R7b Counts as a major installation (×3)</td><td>3d6: 3-6 major (×3); 7-18 small-scale (×1)</td><td>10, 8, 5, 13</td><td>8: **small-scale, ×1**</td></tr>
</table>
Derived without a roll: the 120-ft ring diameter and 60-ft mast (from the ~60-ft intake reach), the shard count and spacing, the intake rate, and the build time.

## Open Rulings
- Ring wall height and material are set at build against the SBG wall tables.
- Whether the mast draws strikes away from nearby sondes. Not rolled; sondes keep the 15% strike chance.
- A second Stormring at Node Two is optional (Expansion Roadmap, Phase D).
