# Crown Decisive Battle — Controlling Module v1.0

```
PREFLIGHT
Skills loaded: surface-campaign-master-gm, campaign-document-builder, hybrid-military-ops (movement and supply only)
Procedure: adventure-arc-builder (Notion: runtime-validation-and-installation §8–§12) and hybrid-module-generator (Notion page, read 5 Oct 2026); format precedent: The Ash-Crowned's Tithe — Controlling Module
Notion pages fetched 5 Oct 2026: Jörmun Frostborn; Gary; Khorzad; Vraxis Mor-Sallar; Centurion Mago; GURPS Mass Combat — Battle Layer v0.1; Wedge and Anvil Doctrine; Module Queue — Firing Conditions
Built from: working files 00-03, 04, 05/05a/05b, 06, 07, 08/08b, 09 (design archive, same folder)
Deviations: none
```

> **v1.0 · 5 Oct 2026 · The New Path, Jörmun lane, Eastern Anauroch, Uktar 1498 DR.**
> - **Status:** PROJECTED conditional module, unplayed. Validated in Phase 9, with all rulings in.
> - **Controlling file:** this one. Working files 00–09 are the **design archive**: read them for reasons, run from this.
> - **Value labels:** S = source-verified · C = campaign ruling · D = rolled · I = inferred.
>
> **Hard locks:**
> - Nothing fires until the trigger.
> - Never show the sealed rolls.
> - Jörmun fights forward: the aura doesn't spare allies.
> - Every Mass Combat round takes a **recorded live GURPS result**.
> - No ally sparing.
> - At most 3 hidden layers a side.
> - No soul interrogation by Jörmun.

# GM QUICK REFERENCE

## Fire it
**Trigger (C):** Thay's monthly Annex detection roll returns *seize* after Crown Phase A exists (sondes flying). **Guard (C, pending Chad):** Vraxis is free and in command at Vraxhal (the Northwatch sortie on his page unplayed). That date is Day 0.
**At fire, roll all at once** (Python `secrets`, four throws, lower median, no rerolls) and record on Deferred Dice. Two rows hold the tables:
- **Row A** (F1–F15, F17, F18): *Crown Decisive Battle — sealed order of battle*.
- **Row B** (F13, F19–F23): *Thayan dead, mage cadre and knives*.

| Roll | 3d6 table (short) |
|---|---|
| F1 Thay option | 3–6 Delegation decapitation · 7–11 Vraxis column · 12–15 both · 16–18 Brotherhood-backed (column one band smaller) |
| F2 Column | 800 / 1,200 / 1,700 / 2,300 / 3,000 (3–5/6–8/9–12/13–15/16–18), Veteran 14 |
| F3 Bait target | 3–9 Node Two · 10–14 Al-Saif camps · 15–18 both |
| F4 Bait lancers | 120 / 180 / 250 / 350 / 450 |
| F5 Approach | 3–8 NE past the Vigil · 9–13 W round the Rest · 14–16 split · 17–18 Buried Realms tunnel (3d6 3–10 impassable → use 9–13) |
| F6 Hidden layers | none / one / two / three (3–6/7–10/11–14/15–18) |
| F7 Layer identity | 3–10 household · 11–12 Zhents · 13–14 Al-Asad · 15–16 Brotherhood · 17–18 answer to the cold |
| F8 Layer size or form | Household 40/60/90/130/180 · Zhents 150–900 · Al-Asad 60–260 · Brotherhood 6–30 casters (+1/+2 Strategy) · cold answer: 3–8 rite, 9–13 Cold-Breakers, 14–18 Akhet Brazier |
| F9 Layer arrival | 3–8 with the main body · 9–12 round 2 · 13–15 flank · 16–18 round 3 |
| F10 Jin / Virelle | per 05 §7 (only if their trigger is met) |
| F11 Bedine riders | 20–90; arrival 1 / 3 / 6 h |
| F12 False intel | 3–10 one band low · 11–18 a phantom layer |
| F13 Pre-bound dead | 80 / 150 / 300 / 500 / 800, outside every mage's pool |
| F14 / F15 Cult | Cult involvement; cell strength (05 §9b) |
| F17 Commander | 3–10 subordinate (W12/13/14: Hezrim Tavaskar, W13) · 11–18 **Vraxis** (W16) + 4 wights + 2 wraiths (pre-bound) |
| F18 Leak | 3–12 scrying · 13–18 mole (F18b who) |
| F19 Mage ratio | 1 per 300 / 200 / 120 / 75 (3–8/9–12/13–15/16–18), minimum 3 |
| F20 Level per mage | W7 / W9 / W11 / W13 |
| F21 Temperament (d6) | Herder · Breaker · Butcher · Seizer · Duellist · Survivor |
| F22 Agenda (3d6) | 3 Lien · 4 Watcher · 5 Poacher · 6 Credit thief · 7 Saboteur · 8–12 loyal · 13 Withholder · 14 Friendly fire · 15 Turncoat · 16 False eye · 17 Ambition · 18 Lien on the commander |
| F23 Vraxis's knife | 16–18: a Lien on the commander (void if Vraxis commands) |
| Quality (each undead element) | 3d6+3: Regular / Veteran / Elite / **Legendary** (3–8 / 9–14 / 15–18 / 19–21) |

**On F1 3–6 (Delegation only):** Session 2 is **E6 alone on the fused engine.** No Mass Combat.

## Mage Tracker (fill at fire; this sheet *is* the Thayan army)
| # | Name | Lvl | Temper | Agenda → target | Pool HD (4×CL) | Retinue | Quality | Onyx HD (1d4×4) | Contingency | Key slots left | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Pre-bound (F13) | — | — | — | — | outside the pool | F13 bodies | 3d6+3 | — | — | — | Commander controls |

- **W7/W9:** skeletons and zombies. **W11:** + ghouls. **W13:** + ghasts. **Vraxis W16:** 64 HD.
- **Above 12 mages:** group the rest into cadres of 5, one row each.
- **Brotherhood casters** command no dead.
- **Slots** (base, SRD; before Int and specialist bonuses):
	- W7: 4/4/3/2/1.
	- W9: 4/4/4/3/2/1.
	- W11: 4/4/4/4/3/3/1, with a 6th spent on *contingency* (3rd-level companion).
	- W13: 4/4/4/4/4/3/2/1, with a 6th on *contingency* (*dimension door*, 920 ft).
	- **Only Vraxis carries a contingent *teleport*** (it fires below 30 hp; S).

## Jörmun against Thay (the numbers that decide it)
- **SR 37** (C). No Thayan caster penetrates it. Vraxis has no Spell Penetration feats on his sheet (S): 0%.
- **What works on him** (all SR: No): *wall of force*, *wall of iron*, *solid fog*, *acid fog*, *cloudkill* (Con damage), *greater dispel magic* on his buffs, summons, bodies, and the answer to the cold.
- **What doesn't:** containment (Boundary Walker), death effects and energy drain (permanent *death ward*).
- **Aura:** 3d6 a round, 60/100 ft, pierces immunity. Skeletons die in round 1, zombies and ghouls in about 2 rounds, ghasts in about 3.
- **Frightful Presence:** DC 27, 90 ft. Living Thayans only; mindless dead are immune.
- **Breath:** 17d6 cold + negative energy, 80-ft line, DC 27. Psychopomp Mantle gives +4 vs undead. Territory gives +2 to all his rolls.
- **Chain-Sight:** he sees every binding. Which dead belong to which mage, the pre-bound thread to the commander, every Lien (reading it is Knowledge (arcana) DC 25).
- **Chain-Breaking, once a day** (C): sever **one** mage's tether, **one** pre-bound element, or **one** Lien. Freed dead attack the nearest living. **Offer it as a choice every day of the battle.**
- **Territory (10 mi):** he knows presence and position of everything, not identity (C). He can seal any *passwall* or the tunnel as a standard action.
- **Mass Combat:** **TS 260** (Legendary air, C). Gary is TS 260 too.

## Frozen Threshold contest (any raising, soul-trap or resurrection of one who died in the territory)
**Caster d20 + CL vs d20 + 22** (C). Ties reroll; one roll per casting.
- *Animate dead*: +4 to the caster. *Create undead*: −4.
- **Lose:** the corpse stays dead, the soul goes into the ice (+1 trapped), and the caster feels the cold take it.
- **Odds for *animate dead*:** W7 9% · W9 14% · W11 20% · W13 27% · Vraxis 40%. **Grave Lien:** 20%.
- Jörmun releases any soul at will. **The Legion's own dead need his release before they can be raised.**

## Mass Combat inputs (Battle Layer v0.1)
- **TS per ~500:** Regular 40 · Veteran 60 · Elite 90 · Legendary 130 · air ×2 · ranged ×1.2. Partial elements count pro rata (I).
- **Exceptional individuals** (C/I): CR 20 = 260. CR 15–19 = Elite 90 (×2 airborne). Below CR 15, no TS; they act through significant actions (Khorzad, CR 5).
	- The Hand = one Elite element (90).
- **Strategy:** +1 for a mage cadre of 6+, +2 for 12+.
	- Knives drawn: −1 at 2–3 fired, −2 at 4+ (recompute at each pause).
	- The Brotherhood adds +1/+2 by F8.
- **Fortification:** only through the holding card (unwritten). Until then it's the live result.
- **Pause points:** a layer reveals · Gary arrives · the wedge returns · a named death or capture · a mass surrender · the Cult enters · a Chain-Breaking cut · a tunnel sealed. **At each one, recompute and record.**

## The empire's side
- **Crown:** Mago (orc centurion) and ~22 of his ~30 (8 at the Vigil). Veteran 14 (I).
- **The wedge:** Gaius Cuneus + 20; 3 Wardrakes and a Roadrider. Turn-back 30 mi on the core pair, 45 mi with the stowed core.
	- Pursuit out of contact: Cuneus rolls 3d6 vs 12.
- **Khorzad:** manticore, CR 5, 57 hp, AC 17, fly 50 (clumsy).
	- 6 spikes +8 (1d8+2), 180 ft, 24 a day.
	- **Contested Sky:** −4 to hostile scrying beneath him (S).
	- He engages at his own discretion. Throwing him above his willingness breaks the terms.
- **Gary** (call → 24–36 h; Sania handles):
	- Fly 200; 464 hp; AC 37; **SR 27**; Fort +26, Ref +18, Will +20.
	- Fire breath 22d10, 60-ft cone, DC 34. Frightful Presence 300 ft, DC 30.
	- **Vulnerable to cold:** *cone of cold* ×1.5. A Thayan W13 needs a 14 on the SR check, about 35% (S).
	- He holds a sector **100+ ft from Jörmun**. Follows the plan; never improvises.
- **Vorian:** the screen at the gate; his sealed suit allows short spells in the aura.
- **Ersk / Safiya:** can't enter the aura. Ersk scouts at Per 13 (I). The Vigil watch: Per 12 (I).
- **The stone wall:** 120 ft long; thickness not on record. Treat it as ≤10 ft, so any *passwall* goes through (I).
- **The ice wall:** a 200-ft arc, 15–20 ft high, **12 ft thick** (two *disintegrates* to breach; S).
	- A breach refills in 1d4 rounds (C). The wall doesn't melt.
- **The bank:** 350 ft from any spring.
	- Dump: 1d6 per stored charge, 30 ft per 25 charges.
	- A dump of 25+ charges also destroys mindless dead in its radius.

## Answer to the cold (F7 17–18; F8 form)
| Form | Effect |
|---|---|
| **Warding rite** (3–8) | 3 Red Wizards spend all their 3rd+ slots. For 1 h in a 300-ft sector, his cold loses its immunity-piercing (I) |
| **Cold-Breakers** (9–13) | A cadre of 6 drilled only on SR: No tools: walls, *acid fog*, *greater dispel*. **They hold him 3 rounds while the column works** (I) |
| **Akhet Brazier** (14–18) | **Within 60 ft, all cold damage becomes fire** (07 §7.12c, R approved as artifact candidate). His aura scorches instead; Thay's troops carry fire wards. Jörmun is fire-immune, so it doesn't hurt him; it disarms him. Gary can stand inside it. Bearer: a W14 Evoker (Will +10). **Smothered by snow from the Frozen Threshold.** A second brazier exists at Vraxhal (T3) |

*(The Phase 9 §4 Brazier wording — "120 ft, cold suppressed" — is superseded by 7.12c, which is the approved text.)*

## The Delegation (E6, F1 3–6 or 12–15)
- **Zaltor** (scaffold; five mandates, S-1 picks the live one) + 12 Red Wizards (each a retinue) + 40 guards.
- **War golems: 2 iron golems (I, count and type).**
	- SRD stats: CR 13, 129 hp, AC 30, 2 slams +23 (2d10+11).
	- Poison breath: 10-ft cube, Fort DC 19, 1d4 Con.
	- DR 15/adamantine; immune to magic (electricity slows, fire heals).
	- Golem control amulets (S-4) and command phrases (S-11) are discoveries.

## DC index
| Check | Value |
|---|---|
| Scouting | 3d6 vs the scout's skill + the layer's concealment (05 §4). Inside 10 mi Jörmun knows presence anyway |
| Reading a Lien or binding | Knowledge (arcana) DC 25 |
| Spotting a Withholder or friendly fire | Vision or Spot at −4 |
| Turning an Ambition or Turncoat mage in the field | Diplomacy vs Will, +4 if their target is alive and winning |
| Interrogation | Intimidate vs Will. Margin 10+ full; 5–9 mostly true; 1–4 partial; tie stonewalls; loss = defiance or the set lie |
| Cuneus's pursuit | 3d6 vs 12 |
| Thayan *cloudkill* | Up to 3 HD dies; 4–6 HD Fort or die; 6+ HD 1d4 Con |
| Thayan *circle of death* | 40-ft burst, 1d4 HD per CL, under 9 HD only, Fort negates |
| Lien vs Threshold | d20 + 15 vs d20 + 22 |

# SESSION 1 — LANCERS IN THE SOUTH
- **Opening:** Day 1 dawn at the Crown.
	- Mago has ~22 on the walls (8 at the Vigil).
	- The wedge is home, or on the water run (d6 1–2).
	- Node Two holds 8. Gary is cat-sized in Sania's coat on Isle de Troll. The sondes are up.
	- The Delegation is at the boundary if F1 includes it.
- **Player's objective:** learn what's coming and commit before Thay does.
- **Thay's objective:** pull the wedge south and keep the main body unseen.
- **Sequence (situations, not a script):**
	1. The scouting window. Thay's concealment only matters **outside 10 mi**.
	2. **E1, the bait** (F3/F4) on Day 1–2. Decide: send the wedge, hold it, or split it. Cuneus wants to go.
	3. Calls, each with a clock:
		- Gary: 24–36 h.
		- Bedine: F11.
		- Korgan: past the window.
		- The Veil: Virelle's trigger decides.
	4. E2, the Vigil sighting (F5 3–8).
	5. Zaltor's parley, if present.
- **Branches:**
	- The wedge goes: E1 fight, then the pursuit rule.
	- The wedge holds: the bait becomes a real raid on Node Two and the Al-Saif camps.
	- Gary called on Day 1: he arrives before a Day 3+ blow.
- **Discoveries:** S-3 route card, P8 Captain Sulk, S-9 codebook, S-13 Vigil log.
- **Partial:** the wedge is drawn past its turn-back point, or Node Two is lost.
- **Failure:** Node Two falls (R-4), the wedge is stranded, and Session 2 opens with no fast arm.
- **End:** dust on the northern horizon, or silence. **Cut** to the night before the blow.
- **E0, Jin's strike** (F14 only): a cut-away fused fight outside the Threshold. Survivors become the third side.

# SESSION 2 — THE BLOW ON THE CROWN
**Opening:** the night before contact.
- Jörmun forward of the walls.
- Mago on the platform at the gate.
- Vorian at the gate.
- Khorzad high.
- The bank at its standoff.

**Objectives:**
- **Player:** hold the Crown and the bank; kill or take the commander; survive the answer to the cold.
- **Thay:** take the bank whole (C-2a). It doesn't burn it.

**Beats:** full text in 08 §8.2b. Run them in this order, each a situation.

| Beat | Thay does | Empire answer on the board | Trackers |
|---|---|---|---|
| **0 Night** | Scrying (−4 under Khorzad), ghouls planted, *mirage arcana*, *stone shape* steps | He knows presence inside 10 mi. Does he tell Mago? Hunting mages in the dark | Thay's Enemy Knowledge |
| **1 Dawn** | **The pre-bound horde walks first** to find the aura; retinues follow; mages stand among their dead | Aura statues. Chain-Sight picks out the mages. Mago's d6. **LIVE result 1** | Live log · mages killed |
| **2 Breach** | Fog the 40-ft kill zone. Breakers pair *disintegrate* on the ice (two casts) or *passwall* the stone wall. Butchers cast *cloudkill* and *circle of death* on the parapet | Vorian plugs the breach (1d4 rounds to refill). Jörmun seals a *passwall*. The garrison drops off the platform | Breach timer · garrison count |
| **3 Seize** | A Seizer *teleports* onto the bank with a guard; a second seals it with *wall of force* | Known on arrival. **E11 dump** (also kills the guard's dead) | Bank state |
| **4 Answer** | The answer to the cold, or Duellists casting around him: walls, fog, *greater dispel*, bodies | Chain-Breaking choice. Gary in sector. Kill Duellists first | LR untouched (SR) |
| **5 Raising** | Herders raise every round | **Threshold contest.** "There's nothing in it." | Souls trapped |
| **6 Pauses** | Layers arrive · Gary · wedge · deaths · the Cult | **Recompute and record each time** | Live log |
| **7 Break** | *Teleport* on their own turn (W9+ with the slot left); contingency hops of ≤920 ft stay inside 10 mi; the rearguard holds; a baggage burner | Pursuit rule. Commander dead: pre-bound locked on last order, **knives fire**, any Lien contests | Mage rows · retinues · bank |

**Branches:**
- **Answer to the cold present:** Gary becomes the ally who can stand close.
- **Gary arrives:** every mage reaches for *cone of cold*. Point four of Thay's orders breaks (R-6).
- **The Cult:** a third side, going for the bank.
- **Thay routs:** pursuit; past the region's edge only on Jörmun's order.
- **Tunnel approach:** sealing it is a significant action.

**Discoveries:** C-1, C-2, S-1, S-2, S-4–S-8, S-10–S-12, S-14; P1–P6, P9–P12; R-1–R-7; onyx pouches; Grave Liens (full or cracked).
- **Partial:** the Crown holds but the bank is dumped or breached, the garrison breaks, or the commander escapes with C-2.
- **Failure:** Thay takes the bank or the site. Session 3 becomes counter-raid or negotiation. Jörmun knows the withdrawal route until it crosses 10 mi.
- **End:** the field at dusk. The ice holds Thay's dead standing; masterless dead sway in the wind. **Cut** to the morning.

# SESSION 3 — ICE AND CUSTODY
- **Opening:** the morning after. The count, the ice, the prisoners. Jin and Virelle may be present.
- **Player's objective:** turn the result into leverage: proof for Arik, intelligence for the Veil, the Bedine, pursuit.
- **Thay's objective:** recover or ransom the commander, learn what the Crown fields, revise its doctrine.
- **Sequence:**
	1. E9 aftermath and the Threshold dead (Hezrim's break scene).
	2. Interrogations, one full extraction per prisoner per day.
	3. E10 custody.
	4. Politics: spirit-speakers and S-12, Tariq, the parley.
	5. **The Legion asks for its dead.** Jörmun's release decides who can be raised.
	6. The Legate question.
	7. Advancement close.
- **Branches:**
	- Pursuit authorised: the Hollow Reach opens.
	- Pursuit refused: Thay's surge comes in 10 days, relief in 30–40.
	- The Cult thread (C-3).
	- The leak (F18).
	- Susanoo priests exposed (R-1).
	- A filled Lien held: bargain, question by *speak with dead*, or sell it back.
- **End:** the module closes. Hand off to the parley, Hollow Reach, Cult and Susanoo threads.

# PRISONERS (short form; full matrix 07 §7.9–7.10)
- **P1 Hezrim Tavaskar** (W13, Will +9). Breaks when shown his fallen in the ice.
- **P1-V Vraxis** (W16, Will 17 GURPS). Doesn't break by force. Trades knowledge for his life and title. **Holding a Tharchion is an act of war.**
- **Agenda-holders:** each gives up their target's agenda at T2+; Turncoats at T1.
- **No soul interrogation by Jörmun** (C).

# ADVANCEMENT (06 §6.6, C)
- **Jörmun:** 3,200 story XP + DMG XP for foes he personally overcomes; CP 5–8.
- **Named NPCs:** Skill Table only. +2 for a significant action, +1 present.
- **Units:** veterancy on a win, 3d6. ≤6 up a step; ≥17 down a step.

# RULINGS CARRIED
- Gate B: Zama in reverse · no ally sparing · 3 layers a side.
- Undead +3 quality.
- Every Thayan mage commands undead (4 HD/CL); pre-bound outside the limit.
- Knives (F22/F23); the Lien contests the Threshold.
- SR 37 · presence awareness · the Threshold contest · CR 20 = TS 260 · Chain-Breaking targets.
- Breach refill 1d4.
- No soul interrogation.
- Leak option C.
- Hand roster and items (05a/05b).
