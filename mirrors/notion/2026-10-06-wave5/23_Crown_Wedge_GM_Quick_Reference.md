# Crown Charge Site and Wedge — GM Quick Reference (Doc 23)

```
PREFLIGHT
Skills loaded: surface-campaign-master-gm, campaign-document-builder
Notion pages fetched (5–6 Oct 2026): Charge Accounting Rules — Crown Charge Array (2026-10-04); Crown Charge Ledger (2026-10-04); Crown Charge Array — System Spec (2026-10-04); Node Two (2026-10-04); Mobile Wedge — Unit TO&E (2026-10-05); Wedge and Anvil Doctrine (2026-10-05); Anauroch Off-Road Movement Table (2026-10-05)
Deviations: none
```

> **One page for the table.** Everything here is copied from the pages named in the Preflight; nothing new is ruled. **Live values live on the Crown Charge Ledger, never here.** Status: PROJECTED. Nothing is built or fielded in Jörmun's play.

## 1. Charge ledger at a glance
| Item | Value |
|---|---|
| 1 charge | One stored 8d6 lightning discharge. Kept to 0.05 |
| Bank per node (Gate Zero) | 5 Standard cells = **125 charges** (13,300 gp with the bus) |
| Bus | **5 charges/h per node**, in or out, shared by intake and draws |
| Wardrake recharge | **5** (2.5 per core), 90-min bay, 3.33/h |
| Roadrider recharge / spare core | **2.5**, 90-min bay, 1.67/h |
| Lent section from empty | **12.5** |
| Bay pairing | 1 Wardrake + 1 Roadrider fill the bus. 2 Wardrakes share it and take 3 h |
| Draw order | Burst/defence → bays → battery racks → line transfer |
| Losses | Tended or tethered ~0/day · isolated, carried or tether cut **1/day per cell** · line Node Two↔Crown **10%** · untended a full month → isolated next month |
| Burst | 1 charge = 8d6, 120-ft line or one target, Reflex DC 22 half; ≤5 per pulse per cell. More than 5 at once: DC 18 or the cell cracks |
| Dump (bank as bomb) | 1d6 per stored charge, 30 ft per 25 charges. A full bank reaches 150 ft. Crown bank sits ≥350 ft from any spring |

## 2. Nightly yield (each night the Deferred Dice row fires)
1. **3d6 ≤ 10** → lightning active (50%). Otherwise nothing tonight.
2. **1d6** lightning hours.
3. **Per sonde, per lightning hour:**
	- d100 ≤ 15 is a strike.
	- On a strike, d100 ≤ 10 means the levitation fails: suppressed 1d4 days, the brake stops it at half height, the housing needs 1 week of repair, and that sonde takes no more intake tonight.
4. **Intake per lightning hour aloft:** Field 0.25 · Standard 0.3 · Stormring Pillar 0.33. Cells stop at full (Field 5 · Standard 25 · Pillar 120).
5. **Bus to bank** at no more than 5/h. What can't move waits in the tethered cells, which count as banked.
6. **Log the night:** Active · hours · sondes up · strikes · lev. fails · charges in · draws · loss · bank end.

**Monthly close:**
- Sum the month.
- Roll Seliara 3d6 vs 12. A miss brings an Athenaeum operator next month, and joint work takes −2 (dropping 1 for each clean month).
- Return repaired housings to the roster.

## 3. Node status board
| | Node One (Crown) | Node Two (37 mi S) |
|---|---|---|
| Site | Crown of Eight Springs, outside the spring precincts | 80 × 100 ft palisade, open erg edge, **no water** |
| Bank | 125 (Gate Zero) | 125 (Gate Zero), dug in and bermed downwind; **the post is inside its blast** |
| Bays | One sealed receptacle block | One bay |
| Intake | Sonde field; Stormring from Phase C | Sonde field on 400-ft tethers outside the palisade |
| Garrison | Mago's ~30 (not wedge) | **8** from the wedge's assault team |
| Supply | Source | Weekly Roadrider water run, 74 mi round trip, ~2.5 charges (~10/month) |
| Keyed by | Seliara | Seliara |
| Air cover | Khorzad: −4 to hostile scrying beneath him | **None** |
| Link | Node line (Phase B): 19 modules, 15,200 gp, 10% loss. Before that, carried cells lose 1/day | |
| **Live state** | **Crown Charge Ledger → Node Registry** | |

## 4. Wedge roster (lent, Legion-owned)
| Vehicle | Who | Pace (road / cross-country) | Charge | Protection |
|---|---|---|---|---|
| **W1** Wardrake, Command | Gaius Cuneus + 7 (driver, ring gunner, signaller, senior sergeant, 3 dismounts) | ~22 / ~6 mph | 2 cores in parallel + 1 stowed, ~10 h a pair | DR 25F/18S/12T&R; Hardness 10 (12 frontal), 200 hp |
| **W2** Wardrake | Driver, gunner, sapper + 7 | ~22 / ~6 mph | As W1 | As W1 |
| **R1** Roadrider | Driver, mechanic, medic (1 seat spare; or driver + 1 + 900 lb) | ~32 / ~10 mph | 1 + 1 stowed, ~14 h | DR 4; Hardness 8, 90 hp/section |
| **With Node Two manned** | W1, W2 (crew only, a shuttle), R1: **12 Legion + Cuneus** | | | |

**Chain:**
- Jörmun has tactical authority. Cuneus commands in the field. The senior sergeant holds Legion discipline under Korgan's standing orders.
- Korgan can recall the loan.
- Mago and Vorian are peers, not superiors.

## 5. The wedge turn (each move or day)
1. **Declare the leg and the terrain.** Pace factor:

| Terrain | Factor |
|---|---|
| Hamada / dry sabkha | ×1.25 |
| Sand sheet / dry wadi | ×1 |
| Broken rock | ×0.5 |
| Erg | ×0.2 |
| Wadi in flood | hard stop |
| True mountain | hard stop |
| Wet sabkha | ×0.2 |

2. **Active sandstorm?** Pace ×0.5. The core clock doesn't slow, so reach halves.
3. **Spend the core clock by the hour, not the mile.** A halted vehicle draws little.
4. **Turn-back check:** at half charge with no node or stowed core ahead, turn back.
	- Radius 30 mi on the core pair, 45 mi with the stowed core.
	- In a storm: 15 / 22 mi.
	- **Cuneus plans to 45. The rule is 30.**
5. **Hard day?** 6 h or more off-road. Debt is 1 workshop day per 2 hard days, ×1.25 (the wedge is one mechanic short).
6. **Supply:** 3 lb food + 8 lb water a head a day. The wedge (21) needs ~231 lb; Node Two (8) needs 88 lb.
	- Status: 14+ days well supplied · 7–13 adequate · 3–6 short · 1–2 critical · 0 starving.
7. **Contact:**
	- Under 100 troops: the fused 3.5e/GURPS engine.
	- 100–5,000: Mass Combat with a **recorded live result**. The wedge's own effect on it isn't formulated.
	- The Maw fires from a **short halt only**.
8. **Ambush, storm or immobilised → turtle:**
	1. Laager the Wardrakes nose-out in a V round the Roadrider, W1 to windward.
	2. Dismount to the lee.
	3. Short-halt fire only.
	4. Hold the clock.
	- Occupants have total cover.
9. **Pursuit:**
	- Inside the region and inside the turn-back radius: Cuneus may pursue.
	- At the turn-back point: break off. Only Jörmun's order overrides.
	- Across the region's edge or toward Thay: Jörmun's order only.
	- **Out of contact while the enemy crosses the line:** Cuneus rolls **3d6 vs 12**. On a failure he goes one more leg; record the cost.
10. **At a node:** bay or core swap, paid from the bank in draw order. Log it on the Ledger's Draw Log.

**Crown → Node Two:**
- Clear: 6.2 h; arrives with ~38% of the pair.
- In a storm: ~12.3 h; needs the stowed core.
- Roadrider: half a day.

## 6. Sources
Charge Accounting Rules · Crown Charge Ledger (live) · Crown Charge Array — System Spec · Node Two · Mobile Wedge — Unit TO&E · Wedge and Anvil Doctrine · Anauroch Off-Road Movement Table.
