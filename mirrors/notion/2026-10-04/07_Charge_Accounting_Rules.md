## Crown Charge Array — Accounting Rules (the live state is on the Crown Charge Ledger child page)
```
PREFLIGHT
Skills loaded: surface-campaign-master-gm, campaign-document-builder, hybrid-research-invention, hybrid-magic-research, empire-operations-engine
Notion pages fetched: Crown Charge Site and Mobile Wedge — Documentation Plan (2026-10-04); LOG-817 Crown charge site rulings (2026-10-04); Deferred Dice — Crown storm nightly yield (2026-10-04); Deferred Dice — Seliara monthly availability (2026-10-04); Echo-Crystal Capacitor (2026-05-31); Crystal Network Ambient Charge System (2026-09-28); Arterial Road Crystal Network (2026-09-28); Baen Light Vehicle Program (2026-07-08). Repo: docs/translation/FUSED_ENGINE_RESOLUTION.md (branch ccr-6d9e69ce-nd0fn0).
Deviations: none
```
> **Canon status — PROJECTED.** These are the rules. Live values go on the Crown Charge Ledger, the way the Crystal Network Ambient Charge System keeps its rules apart from the Arterial Road tracker. The ledger stays at zero until play builds something.

---
## SECTION 1: UNITS
1.1 **Charge.** One charge is one stored 8d6 lightning discharge. Fractions are kept to 0.05.
1.2 **Charge is not Resonance Load.** Charge is never entered on the Arterial Road tracker's RL meter. The two meters are separate.
1.3 **Core equivalents:**

<table header-row="true">
<tr><td>Recharge</td><td>Charges</td><td>Bay time</td><td>Bus draw</td><td>Source</td></tr>
<tr><td>Wardrake, full (2 cores)</td><td>5</td><td>90 min</td><td>3.33/h</td><td>Bound 4 Oct 2026; Light Vehicle Program</td></tr>
<tr><td>Wardrake, one core</td><td>2.5</td><td>90 min</td><td>1.67/h</td><td>Derived</td></tr>
<tr><td>Roadrider, full (1 core)</td><td>2.5</td><td>90 min</td><td>1.67/h</td><td>Derived</td></tr>
<tr><td>Spare core into the battery rack</td><td>2.5</td><td>90 min</td><td>1.67/h</td><td>Derived</td></tr>
<tr><td>Lent section from empty (2 Wardrakes + 1 Roadrider)</td><td>12.5</td><td>—</td><td>—</td><td>Derived</td></tr>
<tr><td>Partial recharge</td><td>Pro rata to the fraction of core run time used</td><td>Pro rata</td><td>—</td><td>Derived</td></tr>
</table>

---
## SECTION 2: NIGHTLY YIELD PROCEDURE (run on each night the Deferred Dice row fires)
2.1 **Lightning check.** Roll 3d6. On **10 or less** lightning is active (R8a). Otherwise the storm is static only, and the night yields nothing.
2.2 **Lightning hours.** If active, roll **1d6** for the number of lightning-active hours (R8b).
2.3 **Strikes, per sonde, per lightning hour:**
- Roll d100. **15 or less** is a direct strike (R4).
- On a strike, roll d100. **10 or less** means the levitation fails (bound 4 Oct 2026).
- On a failure, the enchantment is suppressed for 1d4 days. The sonde drops, and the brake arrests it at half height. The cell is intact, but the housing needs 1 week of repair (R11).
- A failed sonde takes in nothing for the rest of the night.

2.4 **Intake.** Each sonde takes in its grade rate for each lightning hour it was aloft and working:
- Field: 0.25/h
- Standard: 0.3/h
- Stormring Pillar: 0.33/h

A cell stops filling when it is full (Field 5, Standard 25, Pillar 120).

2.5 **Bus.** Charge moves from the cells aloft into the bank at no more than **5 charges/h per node** (R5). The bus also carries any draws in progress, in the same 5/h. Whatever cannot move stays in the sonde cells, which count as banked while tethered.
2.6 **Bank cap.** The bank holds the sum of its cell capacities. Once the bank and the sonde cells are full, intake stops.

---
## SECTION 3: DRAWS
3.1 **Order of draws:**
1. Emergency burst or defensive discharge
2. Vehicles in bays
3. Battery racks
4. Transfer down the node line

3.2 **Bay limits.** Bays run under the 5/h bus cap. One Wardrake and one Roadrider fill the bus. Two Wardrakes share it and take 3 h.
3.3 **Burst.** A burst is paid from the bank: 1 charge per 8d6, up to 5 per pulse per cell. An overload risks the DC 18 crack.

---
## SECTION 4: LOSSES
4.1 **Decoherence:**
- Banked and tended, or tethered aloft: ~0 per day.
- Isolated, carried, or tether cut: **1 charge per day** per cell, never below 0.

4.2 **Line loss.** Node Two to Crown, either way: **10%** of what is sent (R6).
4.3 **Untended bank.** If no operator tends a node for a full month (Seliara is unavailable and no operator has arrived), its cells count as isolated from the first day of the next month.

---
## SECTION 5: MONTHLY CLOSE
5.1 Sum the night log, the draws and the losses. Carry the bank end to the next month.
5.2 Roll Seliara's availability (3d6 vs 12) from the Deferred Dice row and apply the month-miss rule.
5.3 Any housing whose 1 week of repair is done goes back on the sonde roster.
5.4 Construction months (sondes, banks, line, Stormring) use the construction sub-routine and the R&D roll held in Deferred Dice.

---
## SECTION 6: ADJUDICATED TABLES (rolled 4 Oct 2026; Python secrets, four throws, lower median)
<table header-row="true">
<tr><td>Roll</td><td>Table</td><td>Throws</td><td>Bound result</td></tr>
<tr><td>R8a Nightly lightning threshold</td><td>3d6: 3-5 → active on ≤ 6; 6-8 → ≤ 8; 9-12 → ≤ 10; 13-15 → ≤ 12; 16-18 → ≤ 14</td><td>10, 12, 10, 8</td><td>10: **lightning active on 3d6 ≤ 10 (50%)**</td></tr>
<tr><td>R8b Lightning-active hours per active night</td><td>3d6: 3-5 → 1d2; 6-8 → 1d3; 9-12 → 1d6; 13-15 → 2d4; 16-18 → 2d6</td><td>10, 8, 13, 14</td><td>10: **1d6 hours**</td></tr>
<tr><td>R4 Direct-strike chance</td><td>(Stormsonde spec)</td><td>12, 12, 12, 12</td><td>15% per sonde per lightning hour</td></tr>
<tr><td>R5 Bus capacity</td><td>(Charge Array spec)</td><td>9, 5, 10, 10</td><td>5 charges/h per node</td></tr>
<tr><td>R6 Line loss</td><td>(Charge Array spec)</td><td>8, 12, 15, 9</td><td>10%</td></tr>
<tr><td>R11 Levitation failure outcome</td><td>(Stormsonde spec)</td><td>11, 10, 6, 9</td><td>Suppressed 1d4 days; brake at half height; 1 week repair</td></tr>
</table>

## Sourced
- Charge unit, cell capacities, fill rates and decoherence: Echo-Crystal Capacitor.
- Wardrake 5 charges, ordinary-thunderstorm rate and 10% levitation failure: LOG-817.
- 90-minute bays and paired cores: Light Vehicle Program.
- Seliara's availability roll: Deferred Dice and LOG-817.
- Rules-versus-tracker split and ledger layout: Crystal Network Ambient Charge System and the Arterial Road Crystal Network tracker.

## Open Rulings
- Untended-bank rule 4.3 is adjudicated from the Capacitor spec's "tended ~0" line. Chad may revise it.
- Battery-rack drain out of a vehicle is open.
- Armor-cell top-off is excluded until the Soul Ember Core conflict is reconciled.
