## Storm-Charge Harvest, Storage and Vehicle Recharge — Two-Node System Spec
```
PREFLIGHT
Skills loaded: surface-campaign-master-gm, campaign-document-builder, hybrid-research-invention, hybrid-magic-research, empire-operations-engine
Notion pages fetched: Crown Charge Site and Mobile Wedge — Documentation Plan (2026-10-04); LOG-817 Crown charge site rulings (2026-10-04); Echo-Crystal Capacitor (2026-05-31); Crystal Network Ambient Charge System (2026-09-28); Arterial Road Crystal Network (2026-09-28); Echo-Crystal Applications Program (2026-07-08); Loudwater (2026-07-25); Baen Light Vehicle Program (2026-07-08); Baen Light Vehicle — Bill of Materials and Sourcing (2026-07-08); Crown of Eight Springs (2026-09-28); Eastern Anauroch — Frostborn Legate Region (2026-08-30); The Legate Doctrine (2026-09-28); Unnatural Sandstorm (2026-08-20); Holdings & strongholds rulings D1–D18 (2026-09-29). Repo: docs/translation/FUSED_ENGINE_RESOLUTION.md (branch ccr-6d9e69ce-nd0fn0).
Deviations: none
```
> **Canon status — PROJECTED.** This is a design spec. Nothing on this page has been built, bought or keyed in Jörmun's play (Uktar 1498 DR). The first glacier is not raised. Every purchase, build and roll below happens only when play authorizes it. Rolls that resolve in play are held in Deferred Dice.

## Overview
The Crown Charge Array is Jörmun's private storm-charge system for the Legate region. It harvests lightning from the unnatural sandstorm with tethered Stormsondes (and later a fixed Stormring), stores it in Echo-Crystal Capacitor banks, and spends it recharging the echo-crystal power cores of the Wardrakes and Roadrider that Korgan has lent to Gaius Cuneus's wedge. It has two nodes: **Node One** at the Crown of Eight Springs and **Node Two** 37 miles out on the southbound line. It is a Legate asset: tracked, not consolidated, outside empire neglect (D9).

It is not part of the Arterial Road Crystal Network and adds nothing to that network's Resonance Load until a coupling phase is built (Expansion Roadmap, Phase E).

## How it works
1. **Intake.** The storm throws lightning on some nights. While lightning is active, every capacitor cell within ~60 ft of the strike field fills at a tenth of its saturated rate (Capacitor spec; bound ruling 4 Oct 2026). Stormsondes lift cells into the storm on tethers; the Stormring holds a Pillar cell on the ground under a lightning mast.
2. **Bus.** Each sonde tether is a conductor. Charge runs down it into the node's bus, and the bus moves it into the bank. A tethered cell feeding the bus counts as banked.
3. **Bank.** Capacitor cells hold the charge. A tended bank loses ~0 a day.
4. **Battery bank.** Racks of spare echo-crystal power cores are kept charged from the bank, so a vehicle can swap cores instead of waiting at the bay.
5. **Discharge.** The bus feeds vehicle bays (a 90-minute recharge), battery racks, and, in an emergency, a burst or a deliberate catastrophic dump.

## Engineering Spec
<table header-row="true">
<tr><td>Element</td><td>Node One (Crown)</td><td>Node Two (37 mi, southbound line)</td><td>Source</td></tr>
<tr><td>Capacitor bank, opening configuration</td><td>Gate Zero minimum: 5 Standard cells, 125 charges, ~12,500 gp</td><td>Same</td><td>Applications Program, Gate Zero; Capacitor spec</td></tr>
<tr><td>Bank expansion tiers</td><td>+Standard cells (25 charges, ~2,500 gp each) or Pillar cells (120 charges, ~12,000 gp each, fixed 12-ft vault pillar)</td><td>Same</td><td>Capacitor spec</td></tr>
<tr><td>Bus</td><td>One network node module (800 gp). Capacity 5 charges/hour, in or out</td><td>Same</td><td>BOM (module price); bus capacity rolled (R5)</td></tr>
<tr><td>Vehicle bay</td><td>Depot-tier sealed receptacle block with an Institut contact-cut; 90-minute recharge</td><td>Same</td><td>Light Vehicle Program; BOM</td></tr>
<tr><td>Battery bank</td><td>Racked spare echo cores, 2,000 gp each, 2.5 charges to fill each</td><td>Same</td><td>BOM; Loudwater three-class storage; derived</td></tr>
<tr><td>Intake</td><td>Stormsonde field; Stormring from Phase C</td><td>Stormsonde field; Stormring optional (Phase D)</td><td>Stormsonde and Stormring specs</td></tr>
<tr><td>Keying</td><td>Seliara keys the node</td><td>Seliara keys the node</td><td>LOG-817 (bare success: she keys both; glacier survey slips a season)</td></tr>
</table>

**Recharge demand (derived).** A full Wardrake recharge costs 5 charges (bound, 4 Oct 2026). A Wardrake runs two cores in parallel, so each core takes 2.5 charges. A Roadrider runs one core, so a full Roadrider recharge costs 2.5 charges. The lent section (two Wardrakes, one Roadrider) costs **12.5 charges** to recharge from empty.

**Bus arithmetic (derived).** One Wardrake in a 90-minute bay draws 5 charges over 1.5 h, which is 3.33 charges/h. One Roadrider draws 1.67 charges/h. Together they use the whole 5 charges/h bus. A second Wardrake waits, or the two Wardrakes share the bus at 2.5 charges/h each and take 3 hours. While vehicles are on the bus, intake from the sondes queues in the cells aloft, which hold their own charge.

**Inter-node transfer.** From Phase B the nodes are joined by a node line along the southbound route: 19 node modules at the standard 2-mile spacing, 15,200 gp. Charge sent down the line loses **10%** (rolled R6; a "long arterial run" under the Capacitor spec). Until the line exists, charge moves as carried cells on a vehicle. A carried cell is isolated and loses ~1 charge a day.

## Charge cycle (one active night, summary)
Full procedure and the live ledger are in Charge Accounting Rules and the Crown Charge Ledger.
1. Roll whether lightning is active (3d6 ≤ 10).
2. If active, roll the hours of lightning (1d6).
3. Each sonde aloft takes in its grade rate × hours. The Stormring Pillar does the same.
4. Each sonde rolls for direct strikes each lightning hour, and each strike rolls for levitation failure.
5. Charge moves through the bus into the bank, at no more than 5 charges/h per node.
6. Draws (bays, racks) are paid from the bank.

## Losses
- Banked, tended cell: ~0 per day (Capacitor spec).
- Isolated or carried cell, or a sonde cell whose tether is cut: ~1 charge per day (Capacitor spec).
- Node line, Node Two to Crown: 10% of what is sent (R6).
- A bank at full capacity takes no more intake. Excess intake is lost (see Open Rulings).

## Security
- **Bank-as-bomb.** A catastrophic dump destroys a cell and releases its whole stored charge as an area discharge (Capacitor spec). A Gate Zero bank at full holds 125 charges, and each charge is 8d6 lightning. Overloading a cell (more than 5 charges at once) needs a Fort-equivalent DC 18 or the cell cracks and dumps. The bank sits away from the bays, the barracks and the springs.
- **Sacred ground.** The eight springs are sanctified in Bedine cosmology (Legate Region). No node, bank, sonde anchor or ring sits inside the spring precinct. The sacred-precinct exclusion is drawn on the Crown addendum (Wave 3, Doc 9).
- **Phylornel.** The Netherese site is 21 miles northeast of the Crown, just outside the 20-mile range that triggers the ±2 Netherese modifier on a network roll. It does not matter while the Array is uncoupled. Any later node placed within 20 miles of it brings the modifier into play at coupling.
- **The storm itself.** The sandstorm's cause is unresolved (Cult, Shade Remnant, Thay, a Netherese activation, or something new). Harvesting it does not resolve or explain the thread, and the people who made the storm may notice someone drinking from it (Hazard and Threat Annex, Wave 3, Doc 14).
- **Single operator.** Seliara is the only person who can key and retune the nodes. While nodes are built or tended she rolls 3d6 vs 12 each month. A miss brings in a certified Athenaeum operator the following month, and joint Crystal Networks work takes −2, dropping by 1 for each full month they work together without a miss. Serapha Moonfire then knows the site exists.

## D&D 3.5e
**Crown Charge Array (installation).** The component items are those of the Echo-Crystal Capacitor (manufactured wondrous item, storm-charge store, manufacture CL 13) and the Stormsonde.
- Burst from a bank: 1 charge = 8d6 lightning, 120-ft line or one target, Reflex DC 22 half, standard action. Up to 5 charges stack (+8d6 each, max 40d6 from one cell), one save.
- Overload: a cell Fort-equivalent DC 18 or it cracks.
- Stored discharge is ordinary lightning. Normal resistance and immunity apply.
- Opening cost per node: bank 12,500 + bus module 800 = **13,300 gp**, before sondes, bays, battery racks and line.

## GURPS 4e
No point totals (FUSED_ENGINE_RESOLUTION). Cells are Breakable (DR 6) housings. A burst against a target resolves on the 3.5e side. The defender's GURPS crosswalk for the printed save is a Quick Contest of HT against an effective skill equal to the printed DC (22). Armor DR applies before wounding.

## Sourced
Charge unit, cell grades, fill rates, discharge modes, losses and prices: Echo-Crystal Capacitor. Gate Zero bank: Applications Program. Cores, bays, the 90-minute recharge and parallel cores: Light Vehicle Program. Node module, core and receptacle descriptions: Bill of Materials. Three-class storage (cores and capacitor banks): Loudwater. Sacred springs: Legate Region. Legate tracking: D9. Seliara rule, the Wardrake recharge (5 charges), +1 Investment per node, the 37-mile distance and Phylornel at 21 miles: LOG-817. Standard 2-mile node spacing: Crystal Network Ambient Charge System.

## Adjudicated (rolled 4 Oct 2026; Python secrets, four throws, lower median)
<table header-row="true">
<tr><td>Roll</td><td>Table</td><td>Throws</td><td>Bound result</td></tr>
<tr><td>R5 Bus capacity per node</td><td>3d6: 3-5 = 2/h; 6-8 = 3; 9-12 = 5; 13-15 = 8; 16-18 = 12</td><td>9, 5, 10, 10</td><td>9: **5 charges/hour**</td></tr>
<tr><td>R6 Line loss, Node Two to Crown (37 mi)</td><td>3d6: 3-5 = 2%; 6-8 = 5%; 9-12 = 10%; 13-15 = 15%; 16-18 = 20%</td><td>8, 12, 15, 9</td><td>9: **10%**</td></tr>
</table>
Derived without a roll: 2.5 charges per core, a 2.5-charge Roadrider recharge, the 12.5-charge section recharge, the bus arithmetic, 19 line modules (37 miles at 2-mile spacing), and a tethered cell counting as banked.

## Open Rulings
- **Armor-cell top-off.** The Wardrake page has suits topping off armor cells from vehicle cores, but power armor runs on Soul Ember Cores. Until that conflict is reconciled, the Array charges vehicle cores only, and armor top-off draws nothing.
- **Bay receptacle price.** It is not priced in the Bill of Materials.
- **Excess intake at a full bank.** This spec says the intake stops. Whether it can be dumped or burst instead is open.
- **Spare cores out of a vehicle.** Whether a racked spare core loses charge out of the vehicle is not sourced. It is treated as banked while racked on a tended bus.
- **Network accounting.** Whether the private node line generates its own Resonance Load before coupling is open (Expansion Roadmap, Phase E).
