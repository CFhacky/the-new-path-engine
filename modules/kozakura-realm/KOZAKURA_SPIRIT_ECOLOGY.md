# Kozakura Spirit Ecology Module: "Every Place Has an Owner"

```
PREFLIGHT
Notion read (2026-10-07): UDRP Monster Ecology Module (334e8214-84b0-8120-9333-e9ee9656ae4c), the parent this module adapts.
Repo read: scripts/session_open.py Step 4.5B corridor ecology (the per-session band-table pattern); scripts/udrp_delve.py (ecology Layer 1A/1B use).
Companion: KOZAKURA_REALM_PRIMER.md §2 (Myth Pressure), §3 (kami, purity), §4 (yokai), §5 (thin hours/places), §14 (the Calamity), §15 (Teruko).
Roller: kozakura_ecology.py (Python secrets; 3d6 lower median per the arc's standing rule; native dice for layer tables).
Deviations: none
```

> **Status. DESIGN DRAFT (P), Chad 7 Oct: "Kozakura naturally needs its own."** This replaces the UDRP Monster Ecology Module **inside Kozakura only**. West of the strait, the UDRP module still governs. Nothing here has happened in play.

**Labels:** S (source-verified) · R (ruling) · G (generated) · P (proposed) · SR (source required).

---

## 0. Why Kozakura needs its own

The UDRP module's premise is **"Nature doesn't care about your empire"**: monsters are wildlife, and the test is biology (*does this creature exist here for a reason that makes biological sense?*). Its voices are Korgan's patrol report, Seren's ecology briefing and Vara's options.

None of that fits Kozakura:
- **There is no wild land here.** Every spring, pass, cedar and bay has an owner (primer §3). A spirit situation is **a dispute over ownership and rules**, not a population problem.
- **Yokai are rules wearing bodies** (primer §4). Their "biology" is their Rule, Appetite and Bargain.
- **Myths are actors.** A situation can become a story that casts the people standing in it (§2).
- **The empire is not the subject.** There is no Korgan here. The petitioner is a village headman, the expert is an onmyōji, and the one choosing may be Electra.

So the parent's **Ecology Test** becomes the **Rule Test**, and the module adds the **Calamity tier** (primer §14) as a modifier that runs through every layer.

### Design principle
Every spirit situation must pass four tests:
1. **Owner Test:** who owns this place, and are they present, absent or dead?
2. **Rule Test:** what Rule is the spirit keeping, or what Rule did someone break?
3. **Appetite Test:** what does it want? (Every yokai eats something: cucumbers, sake, livers, names, silence.)
4. **Folklore Test:** is this real Japanese folklore, adapted? No invented "cute" yokai.

---

## 1. The Realm Pulse (per session, or per tenday on the road)

The Kozakura analog of Step 4.5B's corridor ecology. **Roll 3d6 lower median (four throws, second-lowest) + 2 × Calamity tier.** Record every roll.

The lower median lands on 8–11 about 72% of the time (mean ≈ 9.6), so **each tier mostly lands in its own band**: the tier sets the climate, and the dice set the weather.

| Pulse | Band | What happens | Typical tier |
|---|---|---|---|
| **≤7** | **Quiet** | The land holds its breath. **Log it:** quiet during the Calamity is itself data. | 0 |
| **8–9** | **Background** | One minor situation (run the module at scale 1). | 0 |
| **10–11** | **Active** | One situation, full module roll. | 0–1 |
| **12–13** | **Restless** | Two situations; one rhymes with an active myth (a **Myth Pressure nudge**, primer §2.2, on the nearest rhyme). | 1–2 |
| **14–15** | **Summer Flies** | A dispute or a war on or beside the route (scale minimum 4). **The road bends** (nudge 6). | 2–3 |
| **16–17** | **Unseated** | A town, pass or ford held by a power. Refugees. **Roll a disaster** (§1.1). | 3–4 |
| **18–19** | **Long Night** | Two situations **plus** a disaster. If either situation matches a Calamity raise trigger (primer §14.2), the GM checks the raise. | 4–5 |
| **20+** | **Iwato** | **A god acts in sight.** Scene-worthy. **World-move trigger.** | 5 |

### 1.1 Disaster sub-roll (d6)
| d6 | Disaster | Notes |
|---|---|---|
| 1–2 | **Earthquake** (the namazu) | Reflex DC 15 + tier or 2d6 + 1d6/tier in a structure; fires follow at tier 3+. Kashima's keystone question (primer §14.3). |
| 3–4 | **Storm / typhoon** | Susanoo's weather. **Ask: does this storm count as Pale Name testimony?** (jewel doc §11 item 5). At sea: the strait closes 1d3 days. |
| 5–6 | **Cold** (the Sun withdrawn) | Snow, frost, frozen fords. Cold-weather rules; Survival DC +tier. Harvest and stores take the hit. |

---

## 2. Layer 0: Situation scale (d6 + half the tier, rounded up; maximum 8)

| Roll | Scale | Character |
|---|---|---|
| 1 | **A haunting** | One spirit, one place, one Rule. One night's work if the Rule is learned. |
| 2–3 | **A dispute** | Two owners claim the same thing (a ford, a hill, a festival). Humans pay both. |
| 4–5 | **A displacement** | Spirits driven out of their place by fire, a dead kami, pollution or the Calamity. Savage and moving. |
| 6 | **A war** | Organized: an oni clan, a tengu host, a splinter of the Night Parade. Fronts and hostages. |
| 7 | **A god stirs** | A province-scale kami acts: a mountain, a river, a strait. Weather and plague. |
| 8 | **Casting** | **A myth takes the place.** Anyone present who rhymes on one axis gains a second (the place). Myth Pressure clocks start. |

---

## 3. Layer 1: The spirit (3 rolls)

### 1A. Category (d12)
Uses the primer §4.2 twenty where possible.

| d12 | Category | Examples (§4.2 and folklore) |
|---|---|---|
| 1 | **Household and tsukumogami** | Zashiki-warashi, rokurokubi, kasa-obake, woken tools (§6) |
| 2 | **Water** | Kappa, nure-onna, ubume at the riverbank |
| 3 | **Sea** | Umibōzu, funayūrei, the sea-lane dead |
| 4 | **Mountain powers** | Tengu, yamauba, kamaitachi in the passes |
| 5 | **Shapeshifters** | Kitsune, tanuki, mujina, bakeneko |
| 6 | **Oni** | Clans, Shuten-dōji's line, the Red Gate's own (S, Akaki) |
| 7 | **The restless dead** | Yūrei, onryō, gaki, gashadokuro |
| 8 | **Serpents and dragons** | The Orochi brood, mizuchi, river-dragons. **Bane of the Eight applies; Scale Remembers if the bead is within 60 ft.** |
| 9 | **Vermin powers** | Jorōgumo, tsuchigumo, ōmukade |
| 10 | **Trees and plants** | Kodama, an old cedar's spirit, jinmenju |
| 11 | **Weather and fire** | Raijū, yuki-onna, onibi, the nue on the roof |
| 12 | **Wrong** | **Shouldn't be here.** A foreign god's echo, a Yashiori wake, Far Realm leakage, drow read as jorōgumo (§7). The Owner Test fails. |

### 1B. Behavior (d8)
| d8 | Behavior | What it looks like |
|---|---|---|
| 1 | **Feeding** | Taking its Appetite from people: livers, sake, travellers, children's names. |
| 2 | **Claiming** | Marking new ground: straw ropes cut, new paths, offerings moved. |
| 3 | **Keeping its Rule** | Someone broke it, and it is answering. Humans caused this. |
| 4 | **Procession** | Moving through on an old route (a Parade, a migrating kami, the dead going home). Get off the road. |
| 5 | **Bargaining** | It wants something and offers something. Every bargain is binding (on a bridge, doubly). |
| 6 | **Haunting** | Tied to a wrong; repeats nightly until the wrong is righted. |
| 7 | **Displaced** | Driven from its place. Savage, desperate, and not where it belongs. |
| 8 | **Possessing** | Inside a person, animal or object (*tsukimono*): fox-possession, an angry ghost in a daughter. |

### 1C. Cause (d8; the Calamity overrides)
| d8 | Cause | Implication |
|---|---|---|
| 1 | **Season and festival** | Obon, Setsubun, the frost festival. Predictable if the calendar is known. |
| 2 | **A broken Rule** | A forgotten offering, a felled sacred tree, blood in a precinct. Humans did this. |
| 3 | **An absent or dead owner** | The kami left or died. A vacuum, and others are moving in. |
| 4 | **Pollution** | Battlefield dead unburied, plague, a massacre. Kegare made into weather. |
| 5 | **A myth rhyming** | Someone nearby is acting a story (primer §2). The spirits are cast too. |
| 6 | **Human exploitation** | An onmyōji binding spirits, a lord feeding an oni, bandits in oni masks. |
| 7 | **The Calamity** | The Sun withdrawn; the summer flies. No single fix. |
| 8 | **An ancient cycle** | It happened in the age of gods; the shrine's oldest scroll records it. |

**Calamity override:** at tier 2+, a rolled 1 counts as 7. At tier 4+, 1–3 count as 7.

---

## 4. Layer 2: Impact (3 rolls)

### 2A. What it hits (d8)
| d8 | Affected | Impact |
|---|---|---|
| 1 | **Road, ford or pass** | Travel stops or pays tolls. The mission's route (nudge 6). |
| 2 | **Shrine or rite** | A rite fails, so a Rule lapses somewhere else. Cascades. |
| 3 | **Rice and stores** | Harvest or granary. Famine pressure (Calamity tier 3+). |
| 4 | **The sea** | Ferries, fishing, the divers. **The strait** if near Isohama. |
| 5 | **Village safety** | Fear, flight, refugees. |
| 6 | **The lord's house** | A castle, a magistrate. Political: the lord demands an answer. |
| 7 | **Trade** | Salt, iron-sand, sake, lacquer (Operation Lacquer Road, S). |
| 8 | **The mission itself** | It is in their way, or it wants something they carry. |

### 2B. Cost (d6 + tier)
| Roll | Cost |
|---|---|
| 1 | Fear only |
| 2–3 | Sickness, dead livestock, broken property |
| 4–5 | Deaths (1–5) |
| 6 | Deaths (6+) |
| 7 | A village lost (fled or dead) |
| 8+ | A district lost |

### 2C. Local response (d6 − tier, minimum 1)
| Roll | Response |
|---|---|
| 1 | **Nothing.** Flight, or pretending. |
| 2–3 | **A village rite.** Brave and wrong; may have fed it. |
| 4–5 | **A priest or onmyōji holding it.** Needs help, not replacement. |
| 6 | **Resolved, Rule still broken.** It will come back. |

---

## 5. Layer 3: Response (3 rolls)

### 3A. Approach (d8)
The suggested approach. Every situation must offer **at least one non-lethal option** and **one that keeps or restores the Rule.**

| d8 | Approach | Character |
|---|---|---|
| 1 | **Exorcism or the blade** | Destroy it. Killing a sacred thing is +3 PP; a dead owner leaves a vacuum (§6, 4A). |
| 2 | **Appeasement** | Feed the Appetite. Works until it doesn't; establishes a precedent. |
| 3 | **Restore the Rule** | Amends: rebuild the shrine, bury the dead, return the stolen thing. Slow, durable. |
| 4 | **Bargain** | Trade and contract. Binding to the letter; read the letter. |
| 5 | **Enshrinement** | Make it a kami: give it a shrine, an offering calendar and a priest. **The problem becomes an owner.** |
| 6 | **Set a rival on it** | One spirit against another. Biocontrol, Kozakura-style. Can work, or create a worse owner. |
| 7 | **Hunters** | Ronin, yamabushi, a peach-born oni-hunter. Bounties breed fakes. |
| 8 | **Play the myth** | Act the rhyme to end it. Boon if played; the bite if broken (primer §2.3). |

### 3B. Complication (d8)
| d8 | Complication | Impact |
|---|---|---|
| 1 | **Sacred** | Killing it pollutes; a god objects; the shrine sues. |
| 2 | **Thin hour or place only** | It can be reached only at dusk, at the hour of the ox, or across a bridge. |
| 3 | **Someone's ancestor** | A family's dead. Destroying it is murder of kin in their eyes. |
| 4 | **Two owners** | Appeasing one offends the other. Pick a side. |
| 5 | **Holding something worse down** | It is a keystone (the namazu pattern). Remove it and something bigger moves. |
| 6 | **Unknown Rule** | Must be read first: onmyōji DC 20 for the Rule, 25 for the Weakness (primer §4.1). |
| 7 | **The lord forbids it** | Politics: the magistrate wants it handled his way, or not at all. |
| 8 | **None** | It is exactly what it looks like. |

### 3C. Requirement (d6)
| d6 | Requirement |
|---|---|
| 1 | One priest and an offering; a night. |
| 2–3 | Direct intervention by the mission; a day. |
| 4–5 | A rite with a shrine's resources; a tenday. |
| 6 | **A god's attention** (heavenly scale); indefinite. |

---

## 6. Layer 4: Consequence (2 rolls)

### 4A. Cascade (d6 + half the tier, rounded down)
| Roll | Cascade |
|---|---|
| 1 | **Clean.** It was wrong-placed; removing it restores order. |
| 2–3 | **Another fills the niche.** A lesser spirit takes the place. |
| 4–5 | **The rival takes it.** Whoever was waiting moves in, usually worse. |
| 6 | **A keystone falls.** The GM checks a Calamity raise (primer §14.2). |
| 7+ | **The Calamity rises +1.** Log it. |

### 4B. Thread (d8)
| d8 | Thread | Ties to |
|---|---|---|
| 1 | **The Storm's seat** | Yashiori wakes, the Pale Name, storm testimony (jewel doc §2, §13) |
| 2 | **The Sun's court** | Sone and the white deer, Teruko, the saiō investigators (§15) |
| 3 | **The Yakumo-ha** | Kitsuki's prayers, the rival sect (jewel §6.3) |
| 4 | **The Orochi remnant** | The Koshi brood, the drink, the Fourth Tail (jewel §6.4) |
| 5 | **The dead** | Enma's wardens, Gozu and Mezu, wells (jewel §6.2) |
| 6 | **The Red Gate** | Akaki oni, the masks, Setsubun (S) |
| 7 | **A human power** | A lord, the court, Shou merchants, Thay's agents |
| 8 | **Standalone** | The land being the land. |

---

## 7. Synthesis protocol (Kozakura voices)

Replaces the parent's Korgan / Seren / Vara sequence.
1. **The Petition (150 words).** A headman's, priest's or diver-headwoman's petition: formal, polite and desperate. What happened, to whom, since when, and what they have already tried.
2. **The Reading (200 words).** An onmyōji, kannushi or yamabushi reads it: **Owner, Rule, Appetite, Weakness, Bargain**, and **what myth it rhymes with**, if any.
3. **The Choices (200 words).** At least three: one non-lethal, one that keeps or restores the Rule, one that pollutes. Cost in PP, time, offerings and Myth Pressure. **If Electra commands (primer §14.5), this is her file note.**
4. **The Wider Picture (100 words).** What it says about the Sun's withdrawal, who owns this land now, and what is moving into the gaps.

---

## 8. Quality tests and banned approaches

**Quality tests:** Owner · Rule · Appetite · Folklore · **Solution spectrum** (at least two meaningfully different responses, one non-lethal) · **Consequence** (acting and not acting both cost).

**Banned:**
- **Cute yokai.** Strange and dangerous, never cute (primer §11).
- **Kill as the default.** Killing a spirit is pollution and a vacuum, every time.
- **Spirits without a Rule.** If you can't state its Rule in one line, it isn't ready.
- **Infinite respawn.** Handled is handled, **unless the Rule is still broken** or the owner is still absent.
- **Alignment coding.** Spirits keep rules older than good and evil.

---

## 9. Example: the ford at Kurogane (illustrative; not rolled, not played)

**Inputs:** Calamity tier 2. Pulse 13 (Restless). Scale 3 (dispute) · Category 2 (water) · Behavior 3 (keeping its Rule) · Cause 2→7 (tier 2 override: the Calamity) · Hits 1 (ford) · Cost 3+2 = 5 (deaths 1–5) · Response 4−2 = 2 (village rite) · Approach 5 (enshrinement) · Complication 4 (two owners) · Requirement 4 (shrine rite) · Cascade 3+1 = 4 (the rival takes it) · Thread 1 (the Storm's seat).

**The Petition.** *To whoever bears the iron-sand road's protection: the ford below Yashio-dono has taken four since the first frost came early.* The kappa that has held the ford for as long as the village has sold cucumbers no longer bows back. The village threw cucumbers, then a horse, then nothing; the headman's son went in to bow to it and did not come out.

**The Reading.** The river kami that owned the ford has gone quiet (the Calamity: the high order loosening), and the kappa is claiming the ford as its own. Two owners now, one silent and one hungry. Its Rule still holds: it bows if you bow. But it has stopped *wanting* to be bowed to, because it wants to be the owner. **It rhymes with nothing yet.** Every storm upriver smells of the brewery's dagger.

**The Choices.**
- **Enshrine the kappa** as the ford's kami: a shrine, a festival, a cucumber calendar. The problem becomes an owner. The river kami, if it wakes, will sue.
- **Wake the river kami** with a harae at the source: two days, a shrine's resources, and the kappa fights it.
- **Kill it.** +3 PP for the killer, the ford ownerless, and the rival (the Orochi brood upriver, 4A row 4–5) takes it.

**The Wider Picture.** Every owner in this valley that goes quiet makes room for something hungrier. The brewery's knife is waking above a river whose owner just fell silent. Somebody is going to own that water by midwinter.

---

## 10. Pulse log

Every Pulse is recorded in `kozakura_ecology_rolls.json` with its throws. The readings below are **the world as the mission finds it**: rolled world state, not events in play. Nobody has acted on them yet.

### Pulse 1: the tenday the mission arrives (S1 into S2, Kurogane valley). Calamity tier 1. Rolled 7 Oct 2026 at Chad's call.

**Pulse:** throws 11, 8, 13, 10 → lower median 10 + 2 × 1 = **12, Restless.** Two situations; one rhymes with an active myth (a Myth Pressure nudge). No disaster roll at this band.

| Layer | Situation 1 | Situation 2 |
|---|---|---|
| Scale | 4 + 1 → **displacement** | 1 + 1 → **dispute** |
| Category | 12 **Wrong** | 1 **Household / tsukumogami** |
| Behavior | 7 **Displaced** | 2 **Claiming** |
| Cause | 8 **Ancient cycle** | 5 **A myth rhyming** |
| Hits | 6 **The lord's house** | 6 **The lord's house** |
| Cost | 1 + 1 → **sickness, livestock, property** | 5 + 1 → **deaths 6+** (1d6+5 = **10**) |
| Local response | 1 − 1 → **nothing** | 2 − 1 → **nothing** |
| Approach | 3 **Restore the Rule** | 1 **Exorcism / blade** |
| Complication | 6 **Unknown Rule** | 1 **Sacred** |
| Requirement | 2 **the mission, a day** | 3 **the mission, a day** |
| Cascade | 1 + 0 → **clean** | 1 + 0 → **clean** |
| Thread | 5 **The dead** | 4 **The Orochi remnant** |
| Nudge (Restless band) | — | d6 = 4 **omen animals** |

**Both situations land in the same house:** the hall of the **lord of Kurogane** (G; the valley's land-steward, unnamed until Chad names him), a mile downriver from Yashio-dono and the brewery's festival patron. The house is doing nothing about either. That is the story: a lord's household paralyzed by two things at once, a day's walk from where the mission is going anyway.

**Calamity check:** both cascades clean. **No raise. The tier stays at 1.**

#### Situation 2: the festival cask (the rhyme)

**The Petition** (the lord's steward, in a careful hand, sent to Yashio-dono, not to strangers). *Ten of this house have died in their sleep since the autumn feast: my lord's two sons, his wife's brother, four retainers, three maids. Each drank at the feast. Each died dreaming, the women say, of heads. The cask the brewery-house gave my lord's grandfather's grandfather stands in the hall where it always stood, and it is full again each morning though no one fills it. The servants will not pass it. My lord will not let it be moved, and will not speak of it. Snakes lie across the threshold each dawn, in Uktar, when snakes sleep.*

**The Reading** (what an onmyōji or Hiruta would say). The cask is a **tsukumogami**: a hundred years in one house, filled every autumn from Yashio-dono's **eighth vat**. It woke at its hundredth New Year, and what woke in it is a **splinter of the Orochi remnant** (§6.4 of the jewel doc). It is **claiming the house** from the hearth-kami: that is the dispute. **The myth it rhymes with is the Orochi's own:** an old couple's house losing its children one by one to the drink, with one left. **The lord's youngest daughter is alive, and the cask wants her to pour for it on festival night.** That is the Kushinada role, and it is open. Omen animals (the nudge): **snakes on the threshold.**
- **Myth Pressure:** a storm god's priests entering this house rhyme on **Role** at once (the storm god arrives at the grieving house). With the daughter and the drink, that is **Role + Token + Act** for anyone who offers to deal with it: a strong rhyme on the Orochi myth (clock 8).

**The Choices.**
- **The blade (the module's approach).** Break the cask and kill what is in it. **It is sacred**: a consecrated vessel of the brewery shrine. The breaker takes **+3 PP**, Hiruta's house is offended, and the lord's grandfather's gift is destroyed under his eyes. Cascade clean: it ends.
- **Play the myth.** Eight cups, a screen, a sword: the Orochi's own ending. Whoever plays the storm god takes the beat and the Boon, and **the Orochi clock starts for them.** Nym's office makes her the natural actor. So does Lorne's.
- **Starve it.** Stop the eighth vat's sake reaching it. That means Hiruta, and the festival, and the remnant noticing.

**The Wider Picture.** The remnant is already in the valley's houses, one cask at a time, fed from the vat the brewery cannot empty. The mission walks into a story that has its parts written and one actor missing.

#### Situation 1: the thing at the old well

**The Petition** (the same steward, a second, shorter page). *The rice in the north storehouse rots overnight. Two of my lord's horses are sick and will not drink from the well. At night something walks the back garden by the old well. It smells of turned earth. The cook says it stood at her door and asked her a question, and she did not answer. No one will go near the well. My lord has said nothing.*

**The Reading.** The well is **older than the house**: in the iron-sand country, the old scrolls put **the slope to Yomi** close by, and wells here go down (primer §5). The shrine's oldest scroll records the **cycle**: in a restless age the boulder at the slope settles, and what is on the other side comes up. **This one is Wrong** (the Owner Test fails): it is dead, it ate at Yomi's hearth, and it has no place in the living land. **Displaced**, it rots what it touches without meaning to. **Its Rule is unknown** until read (DC 20; DC 25 for its Weakness).
- **GM-side (P, for Chad):** it is **one of the house's own founders**, displaced up the well, asking the question the cook did not answer: *"What is my name?"* Its tablet is in the house shrine, half-burnt in an old fire, the name unreadable. **Restoring the Rule** means finding the name and sending it back down with peach wood and the boulder rite.
- **Nym's Death domain** (her office's grant) gives her the reading at +4. **The dead notice who answers them**: whoever restores the Rule is known to Enma's court from that night (ties to the wardens, jewel §6.2).

**The Choices.**
- **Restore the Rule (the module's approach).** Find the name, answer the question, close the well with peach and the rite. A day. Clean.
- **Destroy it.** Possible; it is weak. But it is someone's ancestor, and it will be back next cycle, angrier, with nothing to ask.
- **Ignore it.** The storehouse rots, the horses die, and at tier 2 the cook answers its question wrong.

**The Wider Picture.** Restless at tier 1 means the old seams are opening before anyone has admitted there is a crisis. The dead are coming up the wells in the same valley where the serpent is coming out of the casks.
