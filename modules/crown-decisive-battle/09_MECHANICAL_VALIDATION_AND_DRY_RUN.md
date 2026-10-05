# Crown Decisive Battle — 09 Mechanical Validation and Branch Dry-Run

```
PREFLIGHT
Skills loaded: surface-campaign-master-gm, campaign-document-builder, hybrid-military-ops (movement and supply only)
Notion pages fetched (5 Oct 2026): Jörmun Frostborn (NPCs; incl. aura and Threshold rulings of 5 Oct); GURPS Mass Combat — Battle Layer v0.1 (2026-09-28); Wedge and Anvil Doctrine (2026-10-05)
Sources: SRD 3.5 spell text for every spell named in 08b (levels, SR line, durations, material costs, contingency cap, create undead bands); DMG item pricing (single-use, use-activated)
Probabilities: exact enumeration (Python), shown in §3
Deviations: none. The Mass Combat tables are still untranscribed; every battle step in §5 stops at "LIVE RESULT".
```

> **Status.** PROJECTED. Nothing here happened in play. This phase checks the module's rules against Jörmun's sheet, the SRD and the Battle Layer, then dry-runs 13 branch cases. **The dry-run inputs in §5 are test values, not sealed rolls.** They are never used at fire.

## 1. What the validation found (headline)
Six findings change how the battle plays. All are fixed below or put to Chad.

1. **Thay's spells mostly cannot touch Jörmun (SR).** His sheet gives **SR 25 + HD**. Read at his 12 HD that's **SR 37**. No Red Wizard below Vraxis can beat that on a caster-level check, and Vraxis manages it only 20% of the time with both Spell Penetration feats. The Cold-Breakers sequence in 08b §2D (*slow*, *fear*, *enervation*, *dimensional anchor*, *waves of exhaustion*) **bounces**. It doesn't even spend his Legendary Resistance. → **V1**, Chad call.
2. **He cannot be caged.** Boundary Walker reads "cannot be physically contained". *Forcecage* fails. → V2.
3. **He is permanently death-warded.** *Circle of death*, *enervation* and *finger of death* do nothing to him. → V3.
4. **He sees every binding (Chain-Sight) and can sever one a day (Chain-Breaking).** Every retinue tether, the pre-bound binding and every Grave Lien are visible to him. He can cut one per day. → V5–V6. This is the biggest new lever in the module.
5. **He is aware of everything in his 10-mile territory.** Hidden Thayan layers, planted ghouls, *mirage arcana* and seize-team arrivals are known to him the moment they're inside. → V7, Chad call on scope.
6. **The Battle Layer has no rule for a CR 20 individual.** The empire's troops come to single-digit TS against Thay's 200+. Without Mass Combat's own rule for monsters and heroes, every live result would be a Thay landslide and only significant actions could balance it. → V16, **blocking for Session 2**.

## 2. Findings in full

### V1 — Spell Resistance (Chad call)
- **Sheet:** "SR Major T5: SR 25+HD" (Jörmun page, Shepherd's Gifts).
- **Reading A (default here):** HD = his 12 sorcerer levels, giving **SR 37**.
- **Reading B:** HD counts dragon age HD, which is higher. The answer is the same either way.
- **Caster-level check, d20 + CL vs SR:**

| Caster | vs SR 37 | vs SR 26 (floor, if HD read as 1) |
|---|---|---|
| Wizard 13 | 0% | 40% |
| Vraxis, Wizard 16 | 0% | 55% |
| Vraxis + Spell Penetration + Greater (+4) | **20%** | 75% |

Whether Vraxis has the feats is a canon sheet check (SR).
- **What still works on him (SR: No in the SRD):**
	- Conjured walls and clouds: *wall of force*, *wall of iron* (W11+), *solid fog*, *cloudkill* (1d4 Con per round to 6+ HD, Fort half), *acid fog* (W11+).
	- *Dispel magic* / *greater dispel magic* against his buffs (no SR).
	- Summoned creatures.
	- Mundane fire: ballistae, Thayan bolts, poisons.
	- **The answer to the cold** (F7 17–18), because its forms are built for him: the Hearthward rite, the Cold-Breakers cadre and the Akhet Brazier.
- **Proposed doctrine fix** (08b §8 errata). Thay's Duellists stop casting *at* him. They cast **around** him:
	- Walls to split him from the field.
	- Fog to blind the Herders' targets so he wastes breath.
	- *Greater dispel magic* on his buffs.
	- Every mass body thrown into the aura to buy time for the mages to leave.
- **The Cold-Breakers cadre becomes the only true counter.** Its training is the in-world reason it exists: Thay learned at the Siege that its mages can't hurt him with ordinary spells.

### V2 — Boundary Walker
- "Cannot be physically contained": *forcecage* fails. So does any cage-shaped *wall of force*, *resilient sphere* or *maze*-style imprisonment.
- *Wall of force* can **block** a line, but cannot enclose him.
- *Dimensional anchor* isn't containment, but it's a ray with SR: Yes, so V1 applies.

### V3 — Permanent death ward
- Immune to death effects, negative levels and energy drain: *circle of death*, *enervation*, *finger of death*.
- *Waves of fatigue* and *waves of exhaustion* are not death effects, but SR: Yes, so V1 applies.

### V4 — Psychopomp Mantle
- +4 vs undead (his rolls against them). Apply it in every fused-engine exchange with ghasts, wights, wraiths or Vraxis's retinue.

### V5 — Chain-Sight: he sees every binding
- **Every retinue tether is visible to him.** He knows which dead belong to which mage, so **a Herder hiding in their dead is not hidden from him**. Finding a mage is free; reaching them is the cost.
- **The pre-bound horde's binding is visible.** It runs back to the commander, so the commander can't hide among the column either.
- **Every Grave Lien is visible** as a thread from gem to target. Reading what it is: **Knowledge (arcana) DC 25** (R), with +2 territory, which he passes on a 3. **Thay's knives are an open book to him if he looks.**

### V6 — Chain-Breaking: sever one binding a day
Proposed targets (R):
- **One mage's retinue tether.** The retinue is released **uncontrolled**. Under the SRD, uncontrolled mindless undead attack the nearest living creatures, and the nearest living are **the mage and their guard**.
- **One pre-bound element** (about 500 bodies). The pre-bound binding is one per element, R. Same result: it turns on the column.
- **One Grave Lien.** It's destroyed unfired.

Once per day. **This is the single most powerful play available to him in the battle.** Put it in front of the player as a choice, not as a GM note.

### V7 — Territory awareness (Chad call on scope)
- **Sheet:** "Always aware of everything in territory" (10 mi).
- **Applied (R): presence and position, not identity or strength.** He knows *something* is in the north gully and roughly how many. What it is still needs a reveal: scouting, a sighting, or Chain-Sight for bound dead.
	- This keeps the layer and reveal model (05) working for the player.
	- It removes all surprise against Jörmun personally inside 10 mi.
	- His allies still only know what he tells them.
- Consequences:
	- Thay's concealment rolls matter only **outside 10 mi**: the approach to the territory edge, the bait south of Node Two (37 mi), and the Al-Saif camps.
	- Inside, the question becomes whether Jörmun **tells** Mago in time. That's a decision, not a roll.
	- **Seize-team arrivals are known the instant they land.**
- If Chad rules full identity awareness instead, every hidden layer reveals at the territory edge, and the pause points move there.

### V8 — Control of passages
- **Sheet:** "Control all passages/portals" (Threshold Sovereign).
- **Applied (R):**
	- A *passwall* opening inside the territory is a passage. Jörmun can **seal it as a standard action**, ending the spell.
	- *Wall of force* is not a passage.
	- *Teleport* arrivals are not portals, but V7 makes them known.
	- The Buried Realms tunnel (F5 17–18) is a passage, so **he can close it**. A tunnel approach inside the territory is the worst approach Thay can take, which is what the "test it on your own fallen first" order already hints Thay suspects.

### V9 — The aura against the dead
- 3d6 cold a round, average 10.5. It pierces immunity (Primordial Cold). Radius 60 ft with effort, 100 ft relaxed.
- **SRD hit points:**
	- Human skeleton: 6 hp, gone in round 1.
	- Human zombie: 16 hp, about 2 rounds.
	- Ghoul: 13 hp, about 2 rounds.
	- Ghast: 29 hp, about 3 rounds.
- **The mass dead melt in the aura.** The "frozen statues" image (08 §8.2b Beat 1) stands. Mass Combat is where their numbers count, not in his radius.

### V10 — Frightful Presence against undead
- "Affects all HD" overrides HD caps, **not immunities**. Mindless undead are immune to mind-affecting effects, so retinues and the pre-bound horde ignore it.
- Living Thayans: Will DC 27 or flee. **In practice that breaks the living column's nerve while the dead keep coming.** Play it that way.

### V11 — SRD casting corrections to 08b
| 08b said | SRD says | Fix |
|---|---|---|
| Wizard 9 retinue includes ghouls | *Create undead* is 6th level (Wizard 11+). Wizard 7/9 have only *animate dead* | **W7 and W9 retinues are skeletons and zombies only.** Worked example: W9, 36 HD = 12 zombies (24 HD) + 12 skeletons (12 HD) |
| Created ghouls and ghasts fill the 4 HD/CL pool | The 4 HD/CL cap governs *animate dead*. Created undead are not auto-controlled (SRD: *command undead* or *control undead* needed) | **Ruled application (R):** under Chad's "every mage commands" ruling, created undead also fill the pool. That keeps one number per mage. Recorded as a deliberate deviation from RAW |
| CL 11+ carry a contingent *teleport* | *Contingency*: companion spell ≤ CL/3, max 6th. *Teleport* (5th) needs CL 15 | **W11:** a 3rd-level companion (*gaseous form*, *fly*). **W12–14:** *dimension door* (400 + 40×CL ft; W13 = 920 ft). **Only Vraxis (W16)** can carry a contingent *teleport* |
| Contingency escape gets them away | A *dimension door* of 920 ft stays **inside the 10-mile territory**, and V7 means he knows where they land | **The real escape is a *teleport* cast on the mage's own turn** (W9+, if the 5th slot is unspent). Survivors keep it. Others die or are taken |
| *Animate dead* freely mid-battle | Material: a **25 gp onyx per HD** | Each mage carries onyx for **1d4 × 4 HD** of battlefield raising (R). Onyx pouches are **loot and evidence** (a Red Wizard's pouch ≈ 100–400 gp) |
| *Stone shape* cuts firing steps | 10 cu ft + 1 cu ft/level | Correct: steps and notches only. No earthworks |
| *Transmute rock to mud* undermines the wall | Natural rock only, not worked stone | Correct as written (it targets the footing) |
| *Passwall* through the stone wall | Depth 10 ft, +5 ft per 3 levels above 9th | The stone wall's thickness is **SR (Mago page)**. If over 10 ft, only W12+ go through in one cast |

**Slot table (08 §8.2b):** checked against the SRD wizard table for levels 7, 9, 11 and 13. Correct.

### V12 — Grave Lien price (corrects 08b §7b)
- DMG single-use, use-activated: spell level × CL × **50** gp = 8 × 15 × 50 = **6,000 gp**, plus the *trap the soul* gem at 1,000 gp per HD of the target.
- A Lien on a Wizard 13 costs about **19,000 gp**. The 48,000 gp in 08b came from the wrong DMG line and is struck.
- Cheap enough that **every ambitious Red Wizard can afford one.** That fits Chad's "internecine as normal" ruling better.

### V13 — Threshold strength number (corrects 08b §7b)
- Jörmun's effective CL is 20, and his territory gives +2 to all his rolls. **The Threshold rolls d20 + 22**, not +20.
- The GURPS mirror is unchanged: Will 18 + 2 = 20.

### V14 — The Frozen Threshold contest, written in full (replaces the placeholder)
- **Covers:** any effect that animates, creates or moves the soul of a creature that **died inside the territory**:
	- *animate dead*, *create undead*, *create greater undead*;
	- the Grave Lien, *soul bind*, *trap the soul*;
	- *raise dead* and *resurrection* (any side).
- **Contest:** caster d20 + CL vs Threshold d20 + 22. Ties reroll. One roll per casting, not per body.
	- *Animate dead* (mindless, needs the body more than the spirit): **+4 to the caster** (R).
	- *Create undead* / *create greater undead* (needs the spirit): **−4 to the caster** (R).
	- Jörmun outside his territory: the Threshold still holds, without the +2.
- **GURPS:** Quick Contest, the caster's Necromancy or Thaumatology vs Will 20, same ±4 (R).
- **Jörmun can release any soul at will** (Psychopomp Mantle: "souls pass peacefully"). That's a free action, inside the territory.
	- **The Legion's own dead can't be raised unless he releases them.** Mago's garrison clerics will ask. That's a scene.
- **Loss:** the corpse stays dead, and the soul goes into the ice (**Threshold souls trapped +1**). The caster knows the spell failed and **feels the cold take it**.
- **Odds (exact):**

| Caster | *Animate dead* (+4) | *Create undead* (−4) | Old placeholder (3d6 vs lvl + 4) |
|---|---|---|---|
| Wizard 7 | 9% | — | 63% |
| Wizard 9 | 14% | — | 84% |
| Wizard 11 | 20% | 3% | 95% |
| Wizard 13 | 27% | 5% | 99.5% |
| Vraxis, Wizard 16 | 40% | 12% | 100% |
| Grave Lien (CL 15) | 20% to seize the soul | | |

- **What it means:** inside the territory, Thay's dead **mostly stay dead**. Only Vraxis raises reliably, and even he loses most creations. That fits canon: the Threshold is a T6 gift that "souls cannot leave".
	- **This is a sharp swing from the placeholder Chad ratified.** He ratified it "until Phase 9 writes the full contest", so this replaces it on its own terms.
	- If Chad prefers Thay raising more often, the dial is the +4 for mindless raising. At +8, a Wizard 9 raises about 27% of the time.

### V15 — The internecine numbers
- F22 checked: 8–12 is 125/216 = 57.9% loyal enough. That gives 3.4 knives in a cadre of 8 and 9.2 in a cadre of 22. Correct.
- F19 minimum of 3 mages, checked.

### V16 — Individuals in Mass Combat (blocking for Session 2)
- **The Battle Layer's TS is per 500-troop element by Quality, with ×2 for air.** It has no entry for a CR 20 dragon, a CR 20 red dragon in sphinx form, Khorzad, or a five-man Hand.
- **Dry-run TS** (case 1 in §5, using the Battle Layer DIAL values; partial elements count pro rata, R):
	- Empire: the garrison (30 Veteran) **3.6**, the wedge (21 Veteran) **2.5**, and the screen (SR).
	- Thay: column 1,700 Veteran **204**, pre-bound 300 Elite **54**, retinues of about 192 bodies (8 × W9: 12 zombies + 12 skeletons each) Veteran **23**.
	- That's **about 1:45**. No force-ratio table rescues that. In fiction, though, Jörmun alone ends most of those 1,700.
- **The Battle Layer cannot run this battle as written.** It needs one of two things:
	- **(a) Mass Combat's own rule for exceptional individuals and monsters, transcribed.** I recall it has one but can't verify it. The Mass Combat PDF is the source, and Chad has ruled the laptop off, so **Chad supplies the rule or the page**.
	- **(b) A Chad DIAL ruling:** a CR 20 individual counts as a Legendary air element (TS 130 × 2 = **260**) for TS purposes, still acting through significant actions. Gary counts the same. Khorzad and the Hand go by sheet.
	- Under (b), case 1 runs at roughly **266 (plus Khorzad, SR) vs 281**, a real contest. That reads correctly against the fiction.
- **Until one of these is ruled, Session 2's Mass Combat rounds cannot produce honest live results.**

## 3. Probability checks on the sealed tables
| Table | Check | Result |
|---|---|---|
| All 3d6 band tables (F1–F23) | Every table covers 3–18 with no gap or overlap | Pass (F5 tunnel sub-roll, F10 three sub-tables, F18/F18b included) |
| F6 hidden layers | P(none) 9.3% · one 28.2% · two 42.1% · three 20.4% | Fits the "at most 3 a side" cap (Chad) |
| F17 commander | P(Vraxis) = P(11–18) = 50% | The capstone fight is a coin flip. Intended |
| F23 | P(Lien on the commander) 9.3%; void when Vraxis commands | Pass |
| 3d6+3 undead quality | P(Legendary 19–21) = P(16–18 on 3d6) 4.6% · Elite 26.4% · Veteran 52.3% · Regular 16.7% | The +3 weighting works as Chad intended |

## 4. Placeholders closed in this phase
- **E9 Threshold contest:** written (V14). The placeholder is retired.
- **F8 answer to the cold, effects** (05 §7 says "effects in Phase 9"). Now concrete against V1–V3:
	- **Warding rite over a sector (3–8):** inside a 300-ft sector, the Primordial Cold **loses immunity-piercing**, so undead and *resist energy* work again. Lasts 1 hour. Costs the casters (3 Red Wizards) all their 3rd+ slots.
	- **Trained cadre, Cold-Breakers (9–13):** 6 casters drilled on SR: No tools only. They concentrate SR-No tools: walls, *acid fog*, *greater dispel magic*. **Their purpose is to hold him in place for 3 rounds while the column does its work.** That is the doctrine V1 forces.
	- **Artifact, the Akhet Brazier (14–18):** a 120-ft zone where cold is suppressed; the aura deals 0 inside it. Fire immunity matters, because Gary stands inside it. The artifact's defences are **SR (artifact candidate, approved for the module; stats via magic-research at Phase 10)**.
- **Khorzad, Ersk and Vigil scout skills:** still SR. Each needs its sheet.
- **Golem stats (S-4, S-11):** still SR. The war-golem blocks need the sourcebook text.

## 5. Branch dry-run, 13 cases
**Test inputs only (not sealed).** Each case runs §8.0 firing → §8.1 Session 1 → §8.2 Session 2 → §8.3 Session 3, and checks that every trigger has a home, every tracker gets updated, and no step stalls. "LIVE" marks where a recorded GURPS result is needed.

| # | Inputs | Flow check | Found | Fix |
|---|---|---|---|---|
| 1 | **Baseline.** F1 column; F2 1,700; F19 1/200 (8 mages); F13 300; F6 none; F17 subordinate W13 (Hezrim); F14 no | Fire → bait (F3/F4) → Session 1 → contact → Beats 0–7 → LIVE ×2 → withdrawal | V16: no honest TS. V7: the bait south of Node Two (37 mi) sits **outside** the territory, so Session 1's scouting is still a real game | V16 put to Chad. Otherwise flows |
| 2 | **Maximum.** F2 3,000; F19 1/75 (40 mages); F13 800; F6 three (household, Zhents, answer to the cold = Brazier) | 40 mages at ~W9 = 1,440 HD of retinue + 800 pre-bound | The Mage Tracker at 40 rows is unplayable at the table | **Rule (R):** above 12 mages, group the rest in **cadres of 5** (one row each, the median level, one temperament and one agenda per cadre). Named mages stay single rows |
| 3 | **Delegation only** (F1 3–6): parley as cover for decapitation | No column, so F13 and F19 don't fire. The 12 Delegation mages are retinues (08b §1) | Skirmish scale (under 100). The fused engine runs it, not Mass Combat. 08 §8.2 assumes Mass Combat round 1 | **Errata:** on F1 3–6 Session 2 runs as **E6 alone on the fused engine**. Beats 1–2 and 6 drop; Beats 3–5 and 7 still apply |
| 4 | **Both** (F1 12–15) | Delegation decapitation + column | Two Thayan commands: Zaltor (Delegation) and F17. Whose agendas aim where? | F22 targets stay **within each command**. Add one cross-command knife: the highest-level Delegation mage's agenda aims at F17 if it's an aiming result (R) |
| 5 | **Brotherhood mixed** (F1 16–18) | Column one F2 band smaller; one hidden layer is automatically the Brotherhood | Brotherhood casters are not Thayan, so don't they command undead? | **Brotherhood casters don't** (Chad's ruling covers Thayan mages). They give +1/+2 Strategy only (F8). No F19–F22 for them |
| 6 | **Vraxis commands** (F17 11–18) | F23 is void. Vraxis's retinue is 4 wights + 2 wraiths (canon) **plus** his 64 HD pool | Does the canon retinue sit inside his pool? | **Canon retinue is pre-bound** (outside the pool, per Chad's ruling). His 64 HD pool is extra. He's the only reliable raiser in the Threshold (V14) and the only contingent teleporter (V11). **The capstone is harder than written; that's correct** |
| 7 | **Cult + Jin wins** (F14; E0 succeeds) | E0 cut-away (§8.1a) → no third side | Hand XP/advancement: Hand members are named NPCs → Skill Table banking (6.6) | Flows |
| 8 | **Cult + Jin withdraws** | The Cult enters E3 going for the bank | The Cult's dead are raisable by Thay (V14 applies to all who die in the territory). The Cult's dragon ally (F15 15–18) stat is SR | Flows; stat SR noted |
| 9 | **Tunnel approach**, passable (F5 17–18) | The Buried Realms tunnel under the site | V8: Jörmun can seal it. V7: he knows they're in it | **A tunnel approach becomes a trap for Thay.** Add to Beat 0: if F5 rolled the tunnel, Jörmun's sealing it is a **significant action** (cuts off that force; Mass Combat recomputes without it) |
| 10 | **Gary arrives** mid-battle (E7) | 24–36 h after the call. He holds a sector 100+ ft from Jörmun | Every mage reaches for *cone of cold* first. Gary's SR (sphinx form; sheet SR) decides whether that matters | Flows; Gary's SR/save numbers from his sheet at Phase 10 |
| 11 | **Bank seized and dumped** (E11) | Seizer arrives (V7: Jörmun knows instantly) → Mago or Jörmun orders the dump | The dump kills the Seizer's guard **inside the territory**, so their souls go to the ice, and the Seizer's retinue tether snaps (V5) | Flows. Add: a dump at 25+ charges also hits **the bound dead** in its radius (no save for mindless) |
| 12 | **Commander killed early** | The pre-bound horde locks on its last order (05 §9f). Knives: Ambition and Lien agendas fire. 4+ knives → −2 Strategy | If F23 or an F22 Lien targets the commander, a **Lien contest** runs at death (V13: 20% to win) | Flows. **The commander's death is the richest beat in the module.** Mark it a pause point (already one: named death) |
| 13 | **Thay wins** (failure continuation) | Thay holds the bank and withdraws | Can Thay *carry* charged cells out through the territory? Cells are objects, so the Threshold doesn't hold them | Flows into Session 3's counter-raid branch. Add to Session 3: the column's withdrawal path crosses the 10-mi edge, so Jörmun knows its exact route until then (V7) |

**Every case reaches an end state.** The only stall is **V16** (Mass Combat TS for individuals), which hits every case with a battle in it: 1, 2, 4–13.

## 6. Put to Chad
1. **V1 SR reading:** confirm SR 37 (12 HD). If confirmed, the Cold-Breakers rewrite in 08b §8 stands.
2. **V7 awareness scope:** presence and position (applied), or full identity?
3. **V14 Threshold contest:** keep the +4 mindless dial, or raise it?
4. **V16 individuals in Mass Combat:** supply Mass Combat's rule, or rule the DIAL (a CR 20 individual counts as Legendary air, TS 260)? **Session 2 waits on this.**
5. **V6 Chain-Breaking targets:** confirm one tether, one pre-bound element or one Lien per day, with released dead turning on the nearest living.

## 7. Ruled (Chad, 5 Oct 2026)
1. **V1:** SR 37 (HD = 12 sorcerer levels) confirmed. The Cold-Breakers rewrite (08b §8) stands.
2. **V7:** territory awareness = **presence and position**, not identity. The reveal model stays live inside 10 mi.
3. **V14:** the Threshold contest stands as written, including +4 for mindless raising.
4. **V16:** **DIAL ruled.** A CR 20 individual counts in Mass Combat as a **Legendary air element, TS 260** (130 × 2). It still acts through significant actions.
	- This applies to Jörmun and to Gary.
	- **Below CR 20 (R, by the same logic):** Khorzad and other exceptional individuals take the nearest Quality rung by sheet, ×2 if airborne. Rungs: Regular 40, Veteran 60, Elite 90, Legendary 130. Each counts as one element.
	- The Hand counts as **one Elite element** (5 members of CR 13–14; R).
	- Case 1 now reads about **266 + Khorzad vs 281**. **Session 2 is unblocked.**
5. **V6:** Chain-Breaking confirmed. Once a day it severs **one mage's retinue tether, one pre-bound element, or one Grave Lien**. Released dead turn on the nearest living.

**Phase 9 closed.** Remaining SR items carry into Phase 10:
- Khorzad, Ersk and Vigil sheets.
- Golem blocks.
- The Brazier's stats.
- Gary's SR and saves.
- The stone wall's thickness.
- Whether Vraxis has the Spell Penetration feats.
- The Mass Combat Results tables (the live result still stands in).
