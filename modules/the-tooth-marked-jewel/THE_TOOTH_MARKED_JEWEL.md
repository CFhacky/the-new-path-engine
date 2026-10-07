# The Tooth-Marked Jewel — the Bout at the Eighth Ring and the Hagata-no-Tama quest

```
PREFLIGHT
Skills loaded: surface-campaign-master-gm (arc reference: arc-arik-north), world-lore-reference, campaign-document-builder
Notion canon pages fetched (2026-10-05): Kusanagi (2026-08-02); Jin the Whisper — Emperor's Hand (2026-09-09); Order of the Storm's Edge (2026-09-09); The Hand — Standing Roster (2026-10-05); Change Log LOG-820..833; Divine Avatars & Aspects — Stat Reference (2026-06-29); Power-Tier Quick Reference (2026-06-29); Aspect of the Pale Name — GURPS Sheet (2026-06-29); The Pale Name Evolution (2026-08-20); Kara-Tur Strategic Survey — Master Index (2026-09-30); Kara-Tur — Extraordinary Force Register (2026-09-29); Eastern Interoperability — Jörmun and Kara-Tur (2026-09-29); Mask of the Occupied Oni (2026-09-29); The Storm King's Claim (2026-03-24); Cloak of Wandering Thunder (2026-06-23)
Repo read: branch ccr-6d9e69ce-nd0fn0, modules/crown-decisive-battle/00-03, 04, 05, 05a, 05b, 06
Name checks: NPC database, Notion search (see §11)
Deviations: adventure-arc-builder not loaded; this is a design document, not yet a module. Load it if Chad wants the arc run as a module.
```

> **Status. DESIGN DRAFT, PROJECTED.** Chad approved the skeleton on 5 Oct 2026 ("good skeleton, need fleshing"). This file is the fleshed version, for his review **before** anything goes to Notion or the Change Log. **Nothing here has happened in play.** The scene prose in §2.4 is draft read-aloud for when the vision fires, not a record of events. Rolls are in `tooth_marked_jewel_rolls.json` (Python `secrets`, 3d6, four throws, lower median, no rerolls).

**Labels:** SOURCE-VERIFIED (S) · CAMPAIGN-RULING (R) · ROLLED (D) · INFERRED (I) · GENERATED (G, authored here, replaceable) · SOURCE REQUIRED (SR) · PROPOSED (P, needs Chad).

---

## Contents
0. Rulings this document carries
1. Canon register
2. The vision: the Bout at the Eighth Ring
3. The readings
4. The objective: Hagata-no-Tama and Okitsu-no-shima
5. The route, stage by stage
6. The opposition across the heavens
7. Stakes and outcomes
8. Choice points
9. The discovery: how the arc ends at Arik
10. Rolls ledger
11. Names, collisions and open items

---

## 0. Rulings this document carries

| # | Ruling | Status |
|---|---|---|
| R1 | The "portion of Arik's aspect" is **testimony**: the Pale Name glimpsed at work, not the CR 18 Aspect body. That keeps the Pale Name Evolution off-page rule intact ("exists only in effects, testimony, and purist countermeasures until instantiation"). | Skeleton approved (Chad, 5 Oct) |
| R2 | The objective is **not** the imperial Yasakani jewel. It is one bead from the string Susanoo chewed in the oath-contest, which kept his bite. The imperial regalia stays where it is, outside the Kara-Tur survey's dynastic stop condition. | Skeleton approved |
| R3 | The vision counts as recognition against the Pale Name meter, **unpriced** until played. | Skeleton approved; price is Chad's |
| R4 | The arc runs on the **Jörmun play clock** (Uktar 1498), where the Hand exists. The discovery scene lands in Arik's lane, and its date is open (Jin's lane placement is unset, LOG-824). | OPEN, Chad |
| R5 | The vision happens **outside** Jörmun's 10-mile Frozen Threshold, so it makes no ruling on the Root Country versus the Threshold. | G |

---

## 1. Canon register (key facts)

| ID | Fact | Source | Status |
|---|---|---|---|
| K1 | Arik fills a vacant Kara-Turan storm-god office (Susanoo) "by inheritance of narrative". Talos has no standing and no mechanism to contest it. | Kusanagi page | S |
| K2 | Kusanagi's fealty feeds the Pale Name. Her half-second vision of Arik as Susanoo (Yoshitoshi iconography) keeps four readings open forever. The coldest one is adopted alongside: the Fourth Tail showed her the image to get the kneeling, because a sworn host is a protected host. | Kusanagi page | S |
| K3 | The Atsuta box holds the wrong sword. Opening it tells Kusanagi someone looked. | Kusanagi page | S |
| K4 | Kusanagi's shrine blade carries **the Sickness**: drawn near a reigning sovereign, 1 Con damage per hour. She never draws it in Arik's hall. | Kusanagi page | S |
| K5 | Nym Esharan (elf **woman**, Cleric 14) and Lorne Ashby (half-elf man, Cleric 13), Trickery/Death, serve the Storm King's office. **Arik does not know he has priests.** | LOG-832; LOG-855 (Nym is a woman, overriding the rolled male); Hand roster | R (Chad) |
| K6 | Forward note, not ruled: when Arik finds out, he takes the Emperor-of-Mankind line. Worship is denied as a rule, and these priests are a sanctioned exception. | LOG-832 | Open (Chad) |
| K7 | Enma-Ō stays in the cosmology. His hells and Susanoo's Root Country are separate afterlives. Oni are Enma's wardens, and the Hand wears their faces. Whether Enma notices is an open hook. | LOG-832 | R (Chad), hook open |
| K8 | **Yashiori**: +2 elven dagger. Eighth Straining (confusion on hit, 3/day, Will DC 21). The Root Country (the slain can't be animated for 24 h). Drunk Serpent (crit 15–20 vs confused or sleeping targets). **Appetite:** wetted at dawn with strong drink or 1 hp of the bearer's blood, offered in the Storm King's name; a missed dawn puts it dormant. It came to Nym "with a list of the dawns it had never missed", from "a Storm's Edge house in Kara-Tur" where it cut the eight seals on the vats at the Orochi festival. Thay will pay to recover or destroy it. Enma's wardens "may object". | 05b | S (authored card) |
| K9 | The Hand: five men in crimson oni masks, Veil operative kit at Gray tier or higher, Shadow Jump, black silk gloves with silver threading to the elbow. Jin draws them from the Menagerie's middle ranks. | Hand roster | S / R |
| K10 | Jin kneels to the seat, not the man. His Code of Honor: serve the seat, never sit it. He never raises a claw to the throne. | Jin page | S |
| K11 | The Hand's theater is Eastern Anauroch on the Jörmun clock, Uktar 1498, around the Crown of Eight Springs (a conditional battle module). | Crown battle 00-03, 05, 06 | S |
| K12 | Aspect of the Pale Name: design draft, uninstantiated, meter 0.65. Arik is CR 18 base and about CR 20 effective in Storm Lord form. | Aspect sheet; Pale Name Evolution; Stat Reference | S |
| K13 | Kara-Tur keeps a celestial bureaucracy. Writs, reclassification and true names are its tools (the Mask of the Occupied Oni's breaker table). | Mask page; Eastern Interoperability | S |
| K14 | Kozakura's sacred geography is not one centralized church. Temples, shrines and local communities hold separate rights, and national permission does not settle them. | Eastern Interoperability §7 | S (provisional prep) |
| K15 | Kozakura/Red Gate/oni hooks are not imported into the Banang theater without evidence of reach. | Extraordinary Force Register | S |
| K16 | Electra is Arik's plenipotentiary for the Thayan parley, Uktar–Nightal 1498, Eastern Anauroch, under a sealed, issue-specific commission. Arik does not attend. | LOG-704, LOG-767 | R (Chad) |
| K17 | Electra's current mechanics are the **July** Complete Character Sheet: Wizard (War Magic) 14 / Rogue (Mastermind) 5 / Aberrant Mind 3, CR 18, Commander of Bloodaxe Military Intelligence, Staff of Thunder and Lightning. The April page stays her narrative home (divine scar, personas, Choice Journal). | Chad, 6 Oct 2026; Change Log 6 Oct | R (Chad) |
| K18 | **Electra notices the vision.** | Chad, 6 Oct 2026 | R (Chad) |
| K19 | **Electra holds it and opens a file.** She does not report to Arik. She goes east after the priests **after the Thayan parley resolves**, and **she tags Nym** at the Crown before they leave. | Chad, 7 Oct 2026 (file); 7 Oct 2026 (after the parley; the tag) | R (Chad) |
| K20 | **The office has four priests**, all in the Menagerie: **Quavein Orlzynn** ("the Bursar": drow, Cleric 17, Captain of Division I; War/Water, *the warrior face*: Susanoo with the sword drawn, the storm on the sea), **Osmund Tarrow** (human, Cleric 12, his lieutenant; Trickery/Death, *the quiet face*), **Nym** (Lt VII under Naevys Tolúrin, "the Barefaced") and **Lorne** (Lt IV under Aerendyl Ostahr). Quavein's private ledger "may be kept for the office too" (hook). | Menagerie roster rulings, 5–6 Oct 2026 | R (Chad) |
| K21 | **Raising the dead is Nym's conviction, not the office's law.** Nym holds that the dead belong to the Root Country and that keeping them there is *her* office. Lorne and Osmund raise the dead and are not heretics. Nym enforces her view with Yashiori's 24-hour ban and her release **Eight Vats** (eight targets in drunken sleep, automatic criticals, her kills unraisable for a year and a day). It resolves when Arik learns he has priests. | LOG-854, LOG-855 | R (Chad) |

**Myth anchors used (real-world sources, adapted as Kara-Turan):**
- **The oath-contest (ukei).** Amaterasu chewed Susanoo's ten-span sword and breathed out three goddesses. Susanoo chewed the jewel-strings from her hair and arms and breathed out five gods. She claimed the five as hers, because the jewels were hers. He declared he had won (gentle daughters from his sword proved a clean heart), then wrecked her hall.
- **The three daughters** are enshrined on the Munakata line, the farthest at Okitsu-gū on Okinoshima. That island takes no women, has men wash naked in the sea before landing, forbids taking anything away, and forbids speaking of what was seen there. It holds tens of thousands of votive offerings, magatama among them.
- **Ame-no-Hohi**, one of the five gods born from the chewed jewels, was sent by Amaterasu to subdue Izumo, went over to its lord for three years, and is the ancestor of Izumo's hereditary high priests.
- **Takemikazuchi** of Kashima, Amaterasu's thunder-and-sword god, took Izumo for Heaven by beating Takeminakata in a hand-grappling contest, the mythic first sumo bout. His messengers are deer.
- **Gozu and Mezu**, ox-head and horse-head, are the jailers of the Buddhist hells under Enma.
- Susanoo wept for his dead mother until the mountains withered and the seas dried. He built his first palace at Suga, saying his heart was refreshed, and made the first poem there: *eight clouds rise*.

---

## 2. The vision: the Bout at the Eighth Ring

### 2.1 Trigger and staging

- **When:** dawn, **12 Uktar 1498 DR** (D, TJ-1 = 12). The rite is Yashiori's daily wetting. Nothing else is needed to trigger it.
- **Where (G):** **the Red Saddle**, a sandstone ridge 14 miles west-south-west of the Crown of Eight Springs and outside Jörmun's 10-mile line (R5). It runs half a mile north to south and is 60 ft wide at its crown. The **rite-stone** is a flat slab of red sandstone 4 ft by 3 ft at the highest point, tilted a hand's breadth toward the east. Nym chose it because it faces the dawn over open plain with nothing in the way.
- **Who (D, TJ-2 = 11):** **both priests witness it.** Nym kneels at the slab. Lorne crouches six paces behind and to her right, the witness's place, out of the line of the dawn.
- **What Lorne sees differs.** On the same bout, **Lorne sees the maned figure throwing the pale one.** Nym sees the pale one bending the maned one to the belt. Neither is lying. This seeds a schism between the office's priests (§3.2, §8 CP6).
- **Duration:** one held breath, about 20 seconds by the hail's own fall time. It does not repeat. Another wetting at the same stone the next dawn produces ordinary weather.

### 2.2 The beats (physical, in order)

| # | Beat | What is physically there afterward | Check that reads it (3.5e / GURPS) |
|---|---|---|---|
| 1 | **Hail from a clear sky, in eight rings.** The first ring lands at arm's length from the slab; each ring falls about one man-length wider. Ground outside the rings stays dry. | Eight concentric rings of hail on the gravel, melting in about 40 minutes under the Uktar sun. The outermost is ~50 ft across. | None needed. The rings are visible. |
| 2 | **The eighth ring stops short.** A gap the width of a doorway in the outermost ring, on the east side. | The gap, which holds a **bearing: east by a hand's width north**. Followed far enough, it runs to the strait between Kozakura and Koryo (§4). | Survival or Knowledge (geography) DC 20 / Navigation-12: the bearing projects past Kara-Tur's coast. The exact landfall comes in Stage 1. |
| 3 | **A wind that wails like a son mourning his mother.** It rises from every side at once: the sob, the catch of breath, the long hoarse cry. Dust sheets off the plain and the dune crests strip. | The dune line west of the ridge has lost its crests. Ridges of loose sand lie against the windward side of every rock. | Knowledge (religion) DC 25 / Theology (Kara-Turan)-14: Susanoo weeping for his mother until the mountains withered. |
| 4 | **Lightning that strikes, then refuses.** Bolts drop from cloud that was not there a breath before, stop a hand's width above the ridge, hang crackling, and withdraw upward. Three of them. | Three fused glass spots on the ridge, each the size of a palm, where the hanging bolts heated the sand without touching it. | Spellcraft DC 22: no spell signature. The effect reads as weather that changed its mind. |
| 5 | **Two figures wrestle in the storm-front**, over the plain to the east, as tall as the Crown's wall is long. Sumo grammar: a belt grip, knees bent, one driving in. | Nothing physical. | Knowledge (religion) DC 25 / Theology-14: gods wrestling for a land, the first bout. |
| 6 | **The bout breaks off** at the moment of the throw. Storm, figures and wind are gone at once. | Silence, and the *tik* of melting hail. | — |
| 7 | **The blade takes both offerings.** The rice spirit is gone from Yashiori's edge, and there is blood on it, Nym's, though she did not cut herself. A shallow nick sits on the heel of her left glove's thumb, through the silk. | 1 hp gone from Nym, unexplained. | Heal DC 15: a self-inflicted angle, from her own blade. |
| 8 | **The grip is bitten.** Two crescents of small dents are pressed into Yashiori's amber bone grip, an upper and a lower arc, the width of a human mouth. | **Permanent.** The tooth-marks stay. | Heal DC 18 / Physiology-12: a human bite, or something with a human jaw. |

**The two figures (for the GM's eye; the prose carries it):**
- **The pale one.** Shoulders and arms of storm-cloud with lightning running in the joints, and no face: a smooth pale oval like the blank of a mask before the carver starts (the Mask of Varn). **Only part of it is there.** Below the waist it is rain, grey ropes of it falling onto the plain. It holds the other by the belt with both hands.
- **The maned one.** The office's temperament. A mane of black cloud flung back, a face streaming wet, the mouth open in the howl the wind is making. Eight long shadows rise behind it like necks. It smells of sake, a heavy sweet-sour reek rolling off the plain as if a brewery had split its vats.

### 2.3 What the vision does not do
- It speaks no words and gives no instruction. The quest is the gap, the bite and the blade's history (Stage 1).
- It does not tell Arik. **Arik does not know it happened.**
- It does not instantiate the Aspect. It moves the meter by an amount Chad has not priced (R3).
- It cannot be summoned again. Divinations aimed at the event return the office's weather: hail, a wailing wind, and nothing that can be cross-examined.

### 2.4 Draft scene prose (read-aloud for when it fires; PROJECTED, not played)

*Appearance details for Nym and Lorne beyond the roster (face, hair, eyes, build, scar, the gourd) are G and replaceable. The kit is S from the roster and 05b.*

---

The Red Saddle ran north to south for half a mile, a spine of broken sandstone sixty feet across at its crown. The rite-stone sat at the highest point: a slab of red rock four feet by three, tilted a hand's breadth toward the east and scoured smooth by more centuries of wind than anyone had counted. Frost furred the gravel around it in a grey crust that crunched under a boot. Fourteen miles east-north-east, the Crown of Eight Springs lay along the plain as a pale bar, its wall still dark, and the sky over it had gone from black to the deep, blood-under-skin blue that comes a quarter-hour before the sun. Nothing moved between the ridge and the wall except a single thread of dust far out on the flats, some Bedine rider already about his business.

The air on the ridge was dry enough to split a lip. It smelled of cold stone and old dust, and of the gun oil Lorne worked into his crossbow's swivel every night whether it needed it or not.

Nym Esharan knelt at the slab's western edge with the dawn in front of her.

She was long in the bone and narrow through the hip, spare across the shoulders, the build elves of her line carried when they had spent their prime working rather than eating. The Strider suit fitted her close: matte gunmetal plates over a quilted underlayer, the fittings at shoulder and knee done in shakudō gone dark as old bronze. Down the spine ran a single band of guilloche engraving cut by a Forgedeep hand, fine parallel lines that followed the strain through the plates the way water finds a gully. Black silk gloves reached to her elbows, with silver thread worked through them in a pattern that showed only when she turned her wrist to the light. A sling of wax-sealed vials hung at her left hip, eleven of them, each stopper marked with a thumbprint of colored wax. Her holy symbol hung at her throat on a plain cord, a disc of black iron filed so flat and clean that it named no god to anyone who looked.

She had pushed the mask up onto her forehead for the rite. Zalantar, the Veil's dark wood, carved into an oni's snarl with short horns, tusks and a heavy brow, and lacquered crimson by her own hand. The grain showed pale at the horn-tips, where her thumb rested when she wore it down. Under it her face was narrow and long, high at the cheekbone, with a wide, thin-lipped mouth and skin the grey-white of birch bark in winter. Black hair was cropped close to the skull so it never caught in the mask's ties, with a single lock left long behind the left ear and bound in black thread. Grey eyes, flecked amber near the pupil. A thin white scar ran from the left corner of her mouth to the hinge of her jaw and pulled that side a fraction tighter when she spoke.

Lorne Ashby crouched six paces behind her and to the right, out of the line of the dawn, where the rite put its witness. He was a head shorter than Nym and lean as a coachman's whip, with the rounder jaw and heavier brow of his human side and ears that came to a blunt point. He wore his sandy hair tied back with a strip of rawhide. Freckles crossed a nose broken once and set crooked by someone in a hurry. His Stalker suit sat heavier than Nym's: russet-burnished plates with Bloodaxe interlace, beasts biting one another's tails, running in black niello down both vambraces. A hand crossbow rode on a swivel mount at the center of his chest, and the split staff lay across his thighs with both rods locked. His own mask, zalantar as well, hung from his belt by its cord, face down against his hip.

He was humming. Three bars of a Moonsea shanty, the same three, over and over, low enough that the wind took most of it.

"You'll hum through the rite," Nym said without turning her head.

"I hum through everything. Gods like a tune."

"This one might not."

"Then he can tell me." Lorne shifted his weight off one knee onto the other. *Crunch* went the frost. "He's never told you anything."

Nym let that go. She drew Yashiori from the sheath at the small of her back. A slim leaf-blade of moon-elf work, the length of her hand from wrist to fingertip, its bone grip stained amber all the way through, as if the bone had drunk. The smell came off it the moment it cleared the leather, rice wine, sweet and sour together. She had cleaned the blade after the last wetting and after every one before it, and it had never once smelled of anything else.

The gourd lay on the slab beside her knee: lacquered black, the size of two fists, full of clear rice spirit she bought from a Shou caravan-master at the Golden Way's western end, at four times what it was worth. She worked the stopper free with her teeth. Then she touched the mask's chin with two fingers of her left hand, the way she did before every casting, and held the blade flat over the stone.

"In the Storm King's name," she said in Elvish. She said it again in Kozakuran, and the vowels were still wrong.

She poured. The spirit ran the length of the blade in a thin bright sheet, gathered at the point and fell onto the red stone. *Tip. Tip. Tip.*

The rim of the sun cleared the plain.

The first hailstone struck the slab beside her knee. *Tik.* It bounced once and lay there, a white bead the size of a pea, in a sky with no cloud in it from one horizon to the other.

Then the rest came down.

They fell in a ring. Nym saw it form: a circle of white an arm's length out from the slab, every stone landing on the line, *tik-tik-tak-tik*, rattling off the gravel and the frost. Inside the ring the ground stayed bare. Outside it stayed bare. Another ring dropped a man's length wider, and the stones were bigger now, grape-sized, cracking where they hit. Then a third. A fourth. The sound built from a patter to a rattle to a long hissing roar, and Lorne said something Nym did not hear. Nym counted. She could not stop herself counting. Five. Six. The sixth ring fell across Lorne's boots and Lorne did not move them. The eighth ring came down fifty feet across, white on the red ridge in the first raw light of the sun, and on its eastern side, dead in the line of the dawn, it stopped short. A gap the width of a doorway. The hail on either side of it lay heaped against nothing, as if it had struck a wall.

The wind rose from every side at once.

It came up off the plain with a sound Nym had heard before, once, a hundred years ago, from a man kneeling in a burned street over a shape under a blanket. The deep hitch of breath. The sob that tears its way up through the chest because there is no room left for it. The long hoarse cry after it, going on past the point where a man's lungs should have given out. Dust lifted off the flats in sheets the color of rust. West of the ridge, the dune crests stripped away in long smoking banners. The shanty stopped.

Lightning dropped out of a sky that had no business holding it.

The bolt came straight down at the ridge, blue-white, and stopped. It hung a hand's width above the sand forty feet north of the slab, a rope of fire hissing and spitting, *krrrrrsssh*, and the stink of it filled Nym's mouth, struck flint and hot iron. Every hair on her arms lifted under the silk. Silver thread sparked at her wrists. Then the bolt went back up the way it had come, slowly, the way a hand withdraws from a dog that has not decided whether to bite. A second came down south of her and did the same. A third hung over the gap in the eighth ring and quivered there, humming at a pitch she felt in her back teeth, and withdrew.

Out on the plain, in the storm-front the wind had raised, two shapes were wrestling.

They stood taller than the Crown's wall was long. Nym saw the grip first, because the grip was everything: two hands of storm-cloud clamped on a belt of black cloud, knuckles lit from inside with running lightning. The one holding the belt had shoulders and arms of thunderhead and no face. A smooth, pale oval sat where a face should have been, like the blank a mask-carver starts from, before the first cut. Below its waist it had no legs, only rain, grey ropes of it pouring onto the plain and driving into the ground for purchase.

The other had a face, and the face was weeping. A mane of black cloud flew back from it. Water streamed off its cheeks and jaw in sheets, and its mouth hung open on the howl the wind was making. Behind it rose eight long shadows, swaying like necks. The smell reached the ridge a breath later, sake, an ocean of it, sweet and rotten, as if every brewery in Kozakura had split its vats on the same morning.

The pale one drove in. It bent the maned one at the belt, both hands, leaning its whole weight down and forward the way a horse-breaker takes a stallion's head down to its chest. The maned one's knees buckled. The rain under the pale one shortened as it closed. Nym watched the maned head go down, down, the howl breaking off into a choked gasp, the eight shadows thrashing behind it—

Everything stopped.

The figures were gone. The wind was gone. The dust hung over the plain a moment longer and then began to fall, very slowly, in a red haze. The sun stood a finger above the horizon, ordinary and cold. There was no cloud in the sky.

On the ridge the hail lay in eight rings around the slab and started to melt. *Tik.* A stone shifted. *Tik.*

Nym looked down at Yashiori.

The rice spirit was gone from the blade. Every drop of it. Where it had run, a thin dark line of blood lay along the edge, from the heel to the point, and when she turned her left hand over there was a nick in the heel of the thumb, through the silk, shallow and clean. She had not felt it go in.

She turned the dagger to see the grip. Two crescents of small dents had been pressed into the amber bone, an upper arc and a lower one, the span of a mouth. They had not been there when she drew it.

Behind her the frost crunched. Lorne had stood. His face had gone the color of the ash in a cold fire, and his right hand rested on the crossbow's swivel without seeming to know it was there.

"It threw him," Lorne said.

Nym did not turn round. "It had him by the belt."

"I saw it. Clean over the hip. The one with the mane. He went in under the pale one's arms and lifted it and threw it down on the plain, and the plain *broke*, Nym, I watched the ground split." Lorne's voice was quite level, and too fast. "Then it stopped."

"It had him to the knee." Nym laid the dagger on the slab with the bitten grip facing up. "The maned one. Bent at the belt. One more breath and he was down."

They looked at each other across six paces of melting ice.

"Well," Lorne said at last. "One of us is wrong."

"Or neither of us is." Nym stood. Her knees cracked; she had knelt longer than she thought. She walked to the eighth ring and stopped at the gap. Fifty feet out from the slab, the hail heaped on either side of it in two neat drifts, the space between them bare gravel with the frost still on it. The ice had not even dusted it. She put her boot in the gap, then took it out again.

"Bearing," she said.

Lorne came up beside her, unclipped the hand crossbow from its swivel and sighted down the stock through the gap at the horizon, the way he would lay a bolt on a man three hundred yards out. He held it a long time.

"East," he said. "A hand's width north of east. Nothing out there for a thousand miles but the Hordelands." He lowered the bow. "And past them, the sea."

Nym went back to the slab. She knelt, picked up Yashiori and worked the oiled packet out of the sheath's lining, where it had ridden since the day the dagger came to her. Forty leaves of rice paper folded small, each one covered in a narrow column of brush-script, one entry to a dawn. A list of the dawns it had never missed. She had read every leaf. She unfolded the first one, the oldest, and held it to the light. In the top corner, faint and brown, an inkstone seal: eight vats in a ring, and a ninth cup set in the middle.

She folded the packet away. Then she reached up and drew the mask down over her face, and the crimson snarl settled into place, and the zalantar was cold against her skin.

"Pack the gourd," she said. "We're going east."

Lorne stood a moment longer at the gap in the ring, looking out at the plain where the ground had or had not split. Then he hung the crossbow back on its swivel, crouched for the gourd, and started down the ridge after the priest with the shanty gone out of his mouth.

---

### 2.5 The third witness: Electra (ruled by Chad, 6 Oct 2026: "yes she notices")

**Where she is.** On station in the Crown's country for the Thayan parley (K16). Her exact position that dawn is open. She does **not** stand on the Red Saddle.

**What she notices (she sees no figures).** The bout is shown only to the office's clergy. Electra gets the event from outside, as an intelligence officer would. **Her account is the sceptic's account, and that keeps the four readings open.**

| Channel | What it gives her | Basis |
|---|---|---|
| **The Staff of Thunder and Lightning** | At dawn the staff pulls in her hand toward the west-south-west, as a compass needle would. She is a lightning battlemage, and she knows lightning that strikes and then refuses to land is not weather. | July sheet (K17) |
| **The divine scar** | The scar burns shoulder to hip for the length of a held breath. It is a celestial beacon, and something divine has just manifested within range. | April narrative page |
| **Identity Anchor on Arik** | She maintains the anchor on Arik without telling him. At the same moment it registers **a pull**: strain on an identity she has sworn to herself to keep whole. She cannot tell whether the pull came from Arik or from her own scar flaring, and she will never be able to. | April narrative page. Ambiguity kept on purpose (§3). |
| **Forensics, the same morning** | Eight melting hail rings, a doorway-wide gap in the eastern one, three palm-sized spots of fused glass, the stripped dune crests, two sets of tracks in Stride suits, and a smell of rice spirit on the stone. | Investigation / Gather Information; Spellcraft DC 22 finds no spell signature |
| **The priests themselves** | Within 30 ft of Nym or Lorne, her telepathy can read surface thoughts. That gives her the words *Storm King*, *the bout*, the bitten grip, and the disagreement about who won. | Aberrant Mind telepathy; the GM sets the DC |

**What this makes her.** The first person in Arik's service who can know that he has priests. She commands Bloodaxe Military Intelligence; the priests are Veil agents in Jin's Hand. So **a counter-intelligence finding crosses the line between two services**, and lands on a woman whose own question is whether an instrument can choose its master.

**Her choice: RULED (Chad, 7 Oct 2026): she holds it and opens a file.** The table below is kept for the record of what she passed over.

| Option | What it sets off |
|---|---|
| **Report to Arik at once** | The discovery arrives now, before the quest. Arik's Emperor-of-Mankind answer (K6) comes **before** the bead exists, and the quest becomes either sanctioned or forbidden. |
| **Hold it and open a file** | Her default lean (P). It is intelligence first: she wants to know if it is real before she puts it in front of him. **Her own mirror question**, an instrument that chose its master, makes her protect them longer than she should. |
| **Go to Nym privately** | Silence in exchange for access. She becomes the sanctioned eye inside an unsanctioned sect, or the third member of it. |
| **Tell Lirien** | The priests are Veil agents. Lirien learns her network has been running a cult inside itself. The fallout routes through `hybrid-intelligence-ops`. |

### 2.6 The Red Saddle file and the pursuit east (K19)

**The Choice Journal entry (the night of 12 Uktar, in her cipher):**
> *Chose not to report the Red Saddle event to A. Chose to open a file. (Own preference? Checked twice. Yes. I want to know whether it is real before I put it in front of him, and I want to know whether two men can choose a master who never asked for them. I know why I want to know that. Noted.)*

**The file (Bloodaxe Military Intelligence, compartment of one).**

| Field | Entry |
|---|---|
| **Subjects** | Nym Esharan (elf, Cleric 14) and Lorne Ashby (half-elf, Cleric 13). Veil, attached to Jin's Hand. **Not her service.** |
| **Finding** | Unsanctioned worship of the Storm King's office, which Arik holds. A daily dawn rite on the blade Yashiori. The event of 12 Uktar on the Red Saddle. The two priests disagree about its meaning. |
| **Evidence** | Hail rings and the doorway gap (bearing east, a hand north); fused glass; tracks; rice spirit; surface thoughts: *Storm King*, *the bout*, *the bitten grip*, *it threw him / it had him by the belt*. Her staff's pull, her scar's burn, and the strain on her anchor on Arik **are her own sensations and are filed as unverified.** |
| **Assessment** | Unknown whether a threat, an asset or a theology. **The possibility that the office is acting on Arik is not excluded.** |
| **Distribution** | None. Not Arik, not Lirien, not Jin. |
| **Why held** | To verify before reporting. (Her journal adds the real reason.) |

**What holding it costs her (live from 12 Uktar):**
- **She holds intelligence on another service's agents** without telling their chief (Lirien) or their officer (Jin). If it comes out, it is an inter-service breach, and it lands on the one woman whose trust status is still Conditional.
- **Her betrayal-potential ladder** (July sheet, Strain stage): denser journal entries and more requests to be checked. **Holding a secret alone is exactly the condition her sheet says the sleeper programming thrives in.** It doesn't fire on its own, but it moves the needle.
- **Jin.** If Jin learns a Military Intelligence commander has a file on his priests, his position is simple: the seat's business, handled by the seat's servants. He may not mind. He will not forget.

**The pursuit east: RULED (Chad, 7 Oct 2026): she goes after the Thayan parley resolves, and she tags Nym before the priests leave.**

1. **The tag (ruled).** On 12 Uktar, after the dawn, she brushes Nym at the Crown in a borrowed face for one touch: a jostle in the commissary line, a hand on a sleeve. That touch is the prior contact her soul-tracing needs (Soulthread Trace, narrative codex). From then on she can find Nym anywhere on the plane, along with direction, distance and **the state of Nym's soul**, which she can read as warm, cold, sharp or under pressure. **Nym will not know she was touched.** A Spot DC 30 the moment it happens is her only chance.
2. **The timing (ruled: after the parley).** Her sealed commission covers the Thayan matter, Uktar–Nightal 1498 (K16). She keeps faith with the seal and goes only when the parley is resolved. The rows below are kept for the record; the first is canon.

	| When she goes | What it means |
	|---|---|
	| **After the parley resolves** (**RULED**) | She keeps faith with the seal. She reaches Kozakura weeks behind the priests, likely meeting them **on the return (S5)** or at the island. She becomes **a pursuer and a protector at once.** |
	| **Mid-parley** | She breaks the commission's scope. Jörmun and Cha Hae-In notice. **It is a breach of Arik's seal to protect Arik's secret from Arik**, and that is a scene of its own when it surfaces. |
	| **Doesn't go** | The file stays in her hand. She is in the room for the discovery (§9) with a dossier she has kept from him. |

3. **Getting there.** She is the fastest of anyone.
	- Greater teleport (7th level, Wizard 14) needs a known destination. **Following the tag gives her one.**
	- The narrative codex's Greater Teleportation (no range limit, no error) does the same.
	- She can be in Kozakura in **a day** once she chooses to go.
4. **What Kozakura does with her** (primer draft, P):
	- **The divine scar** is a celestial beacon. Amaterasu's white deer finds her within a mile on arrival, and the court knows a celestial-touched outsider has landed.
	- **Mezu's ledger** reads everything a creature has killed. **Her centuries as Narberal Gamma** are on it, so Enma's jailers have a docket on her that predates the Hand.
	- **Myth Pressure** reads her as **the fox**: Tamamo-no-Mae (the instrument exposed) or Kuzunoha (the shapeshifter whose chosen life was real). Her Choice Journal is evidence for the second reading.
	- **The Envoy (P):** she carries Arik's seal and acts for him unknown to him, so the realm may read her as the **second envoy**, on the returning-arrow beat. With Dispater's sleeper programming in her, that is the most dangerous beat in the realm.

**Envoy note (primer draft, P).** If Arik later sends Electra into Kozakura, the realm reads the priests as the first envoys and her as the second, which puts her on **the returning-arrow beat**. For a woman carrying Dispater's sleeper programming, a myth whose beat is "the sovereign's tool turns" is the worst possible fit, and the most dramatic one. Not ruled.

---

## 3. The readings (all kept open forever, as with Kusanagi's)

The design rule: **every physical residue in §2.2 is consistent with every reading.** No later discovery may close a reading. Evidence can only make one feel likelier to the character holding it.

| # | Reading | What it says the bout was | What a believer points to | What a sceptic points to |
|---|---|---|---|---|
| 1 | **The priest's own mind** | Nym is a cleric of a god whose holder does not know he exists. Faith, ambition and the dagger's daily rite produced the image. The hail is freak Uktar weather. | It was too precise to be weather: eight rings, the gap, the bite. | Lorne saw a different winner. Two minds, two pictures. |
| 2 | **The Pale Name, shaping its recognition** | The Name showed its own clergy a god at work, because being watched at work is what feeds it. | The faceless pale figure, the Varn blank. The vision counts against the meter (R3). | Testimony of a thing that wants testimony proves nothing. |
| 3 | **The office itself** | Susanoo's residue in the seat, with grief, rage and appetite intact, showed its priest that the temperament is still unbroken, and asked for the pledge that finishes the oath. | The weeping, the eight shadows, the sake, the bite. Every detail is the myth's. | The office is a vacancy filled by narrative. Narratives do not ask for things. |
| 4 | **It was simply true** | Part of Arik's authority is in a real fight with an inheritance that came with the seat, and the fight is not over. | Both witnesses saw a bout. Both saw it break off undecided. | Arik has never shown a sign of it. (He would not. That is the point.) |

**The cold reading, adopted alongside (as Kusanagi's Fourth Tail reading is):** the **Orochi remnant** staged it, or bent it. The island's rule, *nothing leaves*, is the only thing keeping the tooth-marked bead out of the serpent's reach. A bead in motion can be taken. The eight shadows behind the maned figure are the tell for anyone who wants to read it this way. The bite on the grip could be Susanoo's, or the bite of something that remembers being bitten. **Consequence:** the remnant has an interest in the quest succeeding as far as the island's shore and failing everywhere after.

### 3.1 How each witness reads it (defaults; play can move them)
- **Nym** holds reading 4 and lets the others stand. To her the bout is an order without words: the bridle needs the bead.
- **Lorne** holds reading 3, darkened by what he saw. The temperament won, or will. The office is not being broken; it is breaking its holder. If that is true, the bead feeds the maned one, and Lorne has to decide which of the two figures he serves.

### 3.2 The schism: The Two Winners, on top of the quarrel over the dead (TJ-2 + K21)
The office already has four priests (K20). Nym and Lorne already disagree about the dead (K21): Lorne raises them; Nym keeps them in the Root Country, and her dagger and her release make sure of it. **The vision gives that quarrel a theology.**
- **Nym's reading (the bridle):** the pale one is breaking the office's temperament to the belt. A god who holds his own grief in check keeps his dead where they belong. **Her conviction about the dead is the bridle's doctrine.**
- **Lorne's reading (the throw):** the temperament threw its holder. The office is grief, rage and appetite, and its dead get up when it needs them. **His raising is the throw's doctrine.**
- **Osmund** raises as Lorne does, so he leans Lorne's way without having seen anything. **Quavein**, the warrior face and the only captain-rank priest, keeps the ledger and has not been told. **Whoever tells Quavein first gets the office's ranking priest as a judge** (CP7).

**Clock (G): "The Two Winners", 0/4.** It advances when Nym and Lorne act on different readings in the same scene, and **whenever one of them raises or forbids the raising of the dead in the other's presence.** When it fills, the office's priests split. The likely line is **Nym** against **Lorne and Osmund**, with **Quavein** deciding where the weight falls. Both factions still draw spells, because the office has never ruled. **The discovery scene then has to answer two questions at once: which priest Arik sanctions, and whose doctrine of the dead he backs.** Per K21, that answer decides whether Nym was the office's voice all along.

---

## 4. The objective: Hagata-no-Tama and Okitsu-no-shima

### 4.1 Hagata-no-Tama, the Tooth-Marked Jewel (G; properties P)
*Relic · unpriced · cannot be crafted, bought or loot-rolled (artifact tier is outside loot-engine's scope)*

**What it is.** One curved jewel (magatama) from the string Susanoo took from his sister's left hair-bunch and chewed in the oath-contest. Most of what he chewed became breath and gods. This bead kept his bite. When the contest was over he held it up as his proof that his heart was clean, said *I have won*, and went to wreck her hall. Someone laid it with the daughters, the three goddesses his own sword had made, on the island where nothing leaves. It has lain there since, one bead among thousands, unlabelled.

**What it looks like.** Deep green jadeite, comma-shaped, the length of a thumb, bored through the head for a string that rotted away centuries ago. The surface is polished to a wet shine everywhere except two crescents of tiny pits on its convex back, an upper and a lower arc, the span of a mouth: **the same bite now on Yashiori's grip.** It has one old chip at the tail. It is warm at dawn and cold the rest of the day. It smells of rain hitting hot stone.

**How it is found (G).** It is unmarked among ten thousand offerings. **When Yashiori comes within 30 ft of it, the tooth-marks on the grip fill with dew.** Within 5 ft, the dew runs. A Search check alone (DC 35 / Vision-6) can also find it, by a searcher who already knows to look for a bitten bead.

**Properties (P, v2 after Chad's note "the gem needs more concrete powers").** Caster level 18 for all effects. Save DCs are flat. Powers sit in three layers: what **anyone** holding it gets, what **the office's clergy** can wield, and what **the holder** receives when the pledge completes. In anyone else's hand the bead is a curved green stone with a bite in it.

**Who the bead answers (the access rule).**
- **Anyone:** Layer 1 only.
- **Clergy of the office** (Nym, Lorne, and the Yakumo-ha if §11 item 2 rules that they draw through the seat): Layers 1 and 2.
- **The holder, after the pledge is received:** all three layers.
- **Amaterasu's agents:** Layer 1, plus *The Oath-Test* alone. In her hand it answers as her jewel and nothing more.

#### Layer 1 — In any hand

- **The Bite (Su, always on).**
	- The bearer knows the location of every creature of the Orochi line within 60 ft, with no save. That includes **the Fourth Tail in Kusanagi**, and each of them knows where the bead is too.
	- **In the clergy's hands** the awareness widens to **every reptilian creature within 60 ft** (see Bane of the Eight).
- **Scale Remembers (Su, always on; ruled by Chad, 5 Oct 2026: "yes, dragons sense it too").**
	- **Every creature of the dragon type within 60 ft knows where the bead is and what it is**, whoever holds it, in any hand, stolen or given. No save, and no concealment blocks it.
	- To a dragon it registers at the scales, as cold along the spine-ridge and the lips drawing back from the teeth: the serpent-killer's bite, in the room.
	- Lesser reptiles (snakes, lizardfolk, nagas, yuan-ti) do not sense it. **Dragons and the Orochi line do.**
	- At a dragon's own discretion, a Sense Motive DC 15 tells it that the bearer is the threat rather than the room.
	- Within 30 ft of Yashiori, the tooth-marks on the grip fill with dew; within 5 ft, the dew runs (§4.1, finding it).
- **Nothing Leaves** (curse, below) applies to anyone who carries it off the island without leave.

#### Layer 2 — In the office's clergy's hands

**1. The Oath-Test (Ukei) (Su, 3/day, standard action).**
- The bearer names a statement and has a creature within 10 ft swear to it with its breath on the bead.
	- **True oath:** the breath leaves the bead as a white mist that settles and is gone.
	- **False oath:** the mist rises as a snarling face for a heartbeat, and the swearer takes **3d6 sonic damage, no save**, as the lie tears out of the chest.
- **The reading cannot be fooled** by *glibness*, *mind blank*, *nondetection* or any Bluff result. It answers whether the swearer **believes** the statement true. A sincere fool passes.
- A creature that refuses to swear when asked is **marked**: for 24 hours, every Sense Motive check against it is made at +10.
- *The irony for Trickery priests is deliberate.* A bearer who swears falsely on his own bead takes the damage and **loses Layer 2 for a day**.
- GURPS: Detect Lies (Cosmic, ignores all concealment; −10 to resist), plus Innate Attack 3d (cr, triggered by a false oath).

**2. The Five Born of Breath (Su, 1/day, full-round action).**
- In the oath-contest Susanoo chewed the jewels and breathed out five gods. The bearer puts the bead in his mouth, bites down and exhales a 30-ft cone of mist that stands up as **five breath-born warriors**.
- **Each one:** a Large air elemental (MM, CR 5; 60 hp) with a crackling glaive in place of its slam: 2d6+6 slashing plus 1d6 electricity.
- **Duration:** 10 rounds or until destroyed. They obey the bearer without needing a command action.
- **When the five die or time out, they go back into the bead as mist.** If any one of them was destroyed, the bearer takes 1d6 damage per destroyed warrior. They were breathed out of him.
- GURPS: Allies (5 breath-kami, 150-point equivalents, Summonable, Minion), 1/day, Costs Fatigue 3.

**3. The Mourning Wind (Su, 1/day, standard action; concentration up to 1 minute).**
- The bearer weeps on the bead, and Susanoo's grief for his mother pours out of it as a **60-ft-radius windstorm** centered on the bearer, who moves with it.
- **Inside it:**
	- All ranged weapon attacks and thrown objects automatically fail.
	- Medium and smaller creatures make a **Fort DC 24** each round or are knocked prone and blown 2d4×5 ft away from the bearer.
	- Flying creatures smaller than Huge cannot hold position.
	- The wind strips moisture. Living creatures take **2d6 nonlethal damage a round**, and plants inside it wither to straw. Water inside it falls a finger's width per round, as the seas dried for him.
- **The bearer and his allies within 10 ft** sit in the still eye: unaffected, and able to shoot outward.
- **Cost:** the weeping is real. The bearer is **shaken for 1 hour** afterward.
- GURPS: Control (Air) 4, Area 20 yd, Selective (Eye 3 yd); Innate Attack 2d (fatigue, Area, Cyclic), plus Affliction (Knockdown) vs HT-3; 1/day.

**4. Bane of the Eight (Su, always on).** *Revised per Chad, 5 Oct 2026: a bonus against anything reptilian.*
- Susanoo killed the serpent. The bead carries the bite, and the bite remembers **scale**.
- Weapons the bearer wields count as **+2 holy-equivalent** against, and deal **+2d6 damage** to, **anything reptilian**:
	- **Dragons:** the whole dragon type, true dragons and lesser, chromatic and metallic, lindwurms and wyverns, dragonborn and half-dragons, and dracoliches.
	- **Snakes and serpents:** every snake animal, giant and dire snakes, sea serpents, and serpentine magical beasts.
	- **Nagas,** all kinds, named on purpose even though 3.5e types them as aberrations.
	- **The reptilian subtype and its kin:** lizardfolk, kobolds, troglodytes, yuan-ti of every caste, crocodiles and lizards, basilisks, behirs and hydras.
	- **The Orochi line,** including the Fourth Tail's hosts. Against a host, the bane counts only on the host's serpent half, which is the GM's call at the table.
- **Multi-headed reptiles:** a confirmed critical **severs a head**. For creatures that regrow heads, the stump stays sealed for 24 hours, as the sake-drowned heads never rose again. **Tiamat** (five heads, each acting; 185 slashing severs one) qualifies twice over.
- **Test for edge cases:** if it has scales and cold blood, or comes from dragon or serpent stock, it counts. Constructs shaped like dragons do not, since there is nothing in them to bite.
- **Campaign weight (flagged, not hidden):**
	- **Against enemies:** Tiamat and her sent peer chromatic; the Cult of the Dragon's dracolich project (Crown battle, F14); and yuan-ti and naga cults wherever they sit.
	- **Against friends:** the bane does not care about allegiance. It bites **Jörmun** (lindwurm), **Gary** (an ancient red), **Shi'van's bonded dragon** and the **Wyrmhelm Program's** whole roster. A Hand priest carrying the bead walks among the empire's dragons with a weapon that wants their scale. The bead **is aware** of every reptile within 60 ft that it would bane, and **the dragons are aware of the bead** (Scale Remembers). Jörmun, Gary and any Wyrmhelm dragon will know the first time a priest comes within 60 ft, and know what it is.
- GURPS: weapon gadget enhancement +2d (Bane: Reptilian/Draconic, a broad class; suggested limitation −10%, GM's call), plus Follow-Up Crippling (severed head; no regrowth for 1 day) against multi-headed targets.

#### Layer 3 — In the holder's hand (after the pledge is received)

**5. The Pledge of the Clean Heart (Su, permanent once received).**
- When a priest of the office places the bead in the holder's hand and the holder closes his hand on it, the office's priesthood is entered on the Celestial Bureau's rolls under the holder's seal (K13).
- **Primacy:** every Kara-Turan shrine of Susanoo must route its formal petitions through the registered clergy, or the Bureau leaves them unanswered. This is the "sect in primacy" Chad asked for, in Kara-Tur's own grammar.
- **Registered clerics:** +1 caster level on Trickery and Death domain spells. Yashiori's dawn appetite is met by touching the blade to the bead, at any distance from a dawn horizon.
- **If the holder refuses, or never takes it, nothing is registered,** so the quest cannot succeed without the discovery scene (§9).

**6. Bridle or Feed (Su, permanent once received). How the bead came off the island decides which one the holder gets.**

| | **The Bridle** (bead given lawfully: petition granted) | **The Feed** (bead stolen) |
|---|---|---|
| Reading it proves | Nym's: the pale one bends the temperament | Lorne's: the temperament throws the pale one |
| Mind | **+4 sacred bonus on Will saves** against mind-affecting and emotion effects. **Immune to confusion and rage effects** he does not choose. | **Immune to fear.** −2 on Will saves against rage, compulsion and drink. |
| Body | Once per day, end any one ongoing effect on himself as a free action (the horse taken down to its chest) | **The Storm's Rage, 1/day:** as a 15th-level barbarian's greater rage (+6 Str, +6 Con, +3 Will, −2 AC) for 10 rounds. **While raging, every melee hit deals +2d6 electricity.** Ending the rage early takes a Will save, DC 20. |
| The office | **The Sealed Ring:** *Hail of the Eight Rings* (below), 1/day | **The Wrecked Hall:** in a rage, he deals **double damage to structures and objects**, as the hall of the sun was wrecked |
| Cost | None. The bridle holds. | **The Thirst:** Kusanagi's template. Alcohol at double effect; Will DC 20 to refuse a drink offered freely. **A Fourth Tail in the room wakes.** |

- **What the mechanics settle and what they don't.** They settle which effect the holder gets. They do **not** settle the reading: the Bridle could still be the feed in disguise, and the Feed could still be grief that needed out. The four readings stay open (§3).
- GURPS:
	- **Bridle:** Indomitable (vs emotion), Resistant to Mind Control (+8), plus a 1/day Neutralize-self.
	- **Feed:** Berserk (controlled 1/day, Will-4 to stop) with Innate Attack 2d (burn, Follow-Up to melee), Unfazeable (fear only), and Addiction (alcohol)-equivalent Compulsive Carousing (12).

**7. Hail of the Eight Rings (Su, 1/day; holder with the Bridle, or any registered cleric holding the bead).**
- The vision's first beat made into a weapon. **Point:** anywhere within 1 mile that the user can see.
- **The hail:** eight concentric rings of hail fall around that point, each 5 ft wide, the outermost **50 ft** across.
	- A creature caught in a ring takes **8d6 bludgeoning + 4d6 cold** (Reflex DC 25 half).
	- The rings stand for **10 minutes** as **walls of falling ice**: crossing one deals another 4d6 bludgeoning, and they block line of sight.
- **The gap:** the user may leave the eighth ring open with a gap the width of a doorway, facing a direction he chooses. **Allies the user names cross every ring freely.** The open door is the only safe way out for everyone else.
- It is a killing ground with a single exit, and the exit is the user's to choose.
- GURPS: Innate Attack 8d cr + 4d burn (frost), Area 8 yd, Persistent walls (Obstruction) 10 min, Selective (allies), plus a single designed gap; 1/day.

#### The curse: Nothing Leaves (while the bead is held without the daughters' leave)
1. **The Unspoken.** The bearer cannot speak of what they saw on the island. An attempt makes a Will save, DC 25. On a failure they lose their voice for 24 hours (no verbal components, no command words). Each bearer gets one success; after that, failure is automatic.
2. **The sea remembers.** At sea, weather within 1 mile worsens one category every 6 hours until the bead is ashore. Ashore, storms within 10 miles bend toward the bearer.
3. **Standing.** The theft gives Amaterasu's court, and Talos's man, a lawful complaint (§6).
4. **Layers 2 and 3 work while it is stolen.** The Pledge still registers, **and the holder receives the Feed** (power 6).

**Power-tier check.** These powers sit level with Kusanagi's shrine blade, which is also an artifact with an at-will defining power (Turn the Wind). The heaviest lines are the five breath-born (five CR 5 elementals once a day), the Hail (8d6+4d6 in a 50-ft killing ground once a day), and Bane of the Eight, which now covers every reptile, including every dragon, the empire's own among them. The first two sit below the CR 18–20 apex band and give a priest of 13–14 a single scene-defining move a day. Bane of the Eight is the line with strategic weight: Tiamat on one side, the empire's own dragons on the other. **Unpriced (relic). Never loot-rolled.**

**Who claims it:**

- **Amaterasu's court:** the jewel was hers.
- **The Yakumo-ha:** their founding ancestor was breathed out of the jewels Susanoo chewed.
- **The office:** the bite is his.
- **The Orochi remnant:** the bite is its *memory*.

**GURPS summary:** per-power lines above. The Pledge is a Patron-gadget trigger (Celestial Bureau registration, plus +1 effective Power Investiture for two domains for registered clergy).

### 4.2 Okitsu-no-shima, the island of the eldest daughter (G location; Kara-Turan analog to Okinoshima)

- **Where:** in the strait between Kozakura and Koryo, **38 miles** off Kozakura's western coast. It is a Ring 3 location in the Kara-Tur survey's scheme. Its sovereignty is shrine-held and national claims are irrelevant to it (K14).
- **Shape:** an island **2.5 miles** round, one steep granite peak rising **800 ft** from the sea, all of it old forest: camphor, chinquapin and tabu trees, with fern under them and moss on everything. There is one landing, a black-shingle beach on the south side 200 ft long, and one stone stair of **1,140 steps** from the beach to the shrine.
- **The shrine (Okitsu-miya):** a plain cypress hall, 24 ft by 16 ft, built against the foot of a cluster of granite boulders the size of houses at the 300-ft contour, with a roof of cypress bark. Light is green and dim at noon. It smells of wet stone, leaf-rot, salt and cedar smoke. The sound is surf below, wind in the canopy, and crows.
- **The offering field:** among and under the boulders behind the hall, a thousand years of offerings lie where they were set down, never cleared. Bronze mirrors green with age. Iron blades rusted to lace. Gilt-bronze horse-trappings. Gold rings. Glass beads. **Magatama in their thousands.** The ground is a crust of old treasure under leaf mould, about **60 ft by 90 ft**, with boulders for walls and roof. Nothing there has been counted, because counting it would be speaking of it.
- **The island's four rules (S from Okinoshima, adapted):**
	1. **No women.** **Nym cannot land** (K5), nor can Kusanagi, nor Electra in her chosen form (§2.6). See S4 for how the arc handles it.
	2. **Men strip and wash in the sea** before they set foot on the shingle. They come ashore naked, unarmed and **unmasked**. Kit can be landed afterward only with the resident priest's permission, and he does not give it.
	3. **Nothing leaves.** Not a pebble, not a leaf, not a drop of the spring water.
	4. **What is seen is not spoken of.** The island's common name on the mainland is *the Island Not Spoken Of*.
- **The daughters.** Three goddesses breathed out of Susanoo's sword. The eldest keeps Okitsu; her sisters keep the middle island and the mainland shrine. **They are the office's daughters by the contest.** They are not Amaterasu's to command, though she bore them by breath. They answer as sea and weather, never as a voice.

### 4.3 Ichiki Shōun, resident priest (G NPC; name-checked)
*Human (Kozakuran) male, 71. Kannushi of Okitsu-miya, on a ten-day rotation from the mainland shrine. Expert 4/Cleric 5 (the daughters; Protection/Water). GURPS ~150 CP; Religious Ritual (Kozakuran)-15, Boating-12, Weather Sense-14.*

**Description.** Five foot one, bird-boned and bent forward at the shoulders from forty years on that stair. Bald, with white stubble over the scalp and jaw that he shaves every third day with a razor older than he is. His face is brown and deeply creased, and both eyes are cloudy at the rims but sharp in the middle. His hands are salt-cracked across every knuckle. He wears a faded white robe with a hemp sash and straw sandals, and goes barefoot on the stair. He smells of cedar smoke and fish. He carries nothing but a sakaki branch and a wooden ladle.

**Voice.** Speaks rarely and in the island's register: what he says is short, and what he does not say is the point. He has a habit of repeating the last word a visitor said, flatly, as if weighing it. *"Leave."* *"Leave?"*

**Reaction (D, TJ-3 = 8, Poor).** He takes the strangers for pirates, or worse, from the moment their boat grounds. He will watch them wash. He will not refuse their landing, because the rite allows any man who washes to land. **He refuses to admit them to the petition** (§5, Stage 4), and he will not move from in front of the shrine door. Turning him needs a reason the island would accept, which means the truth unadorned. That is a hard thing for two Trickery priests.

**What he knows:** where the bead lies, roughly (the eastern edge of the field, "where the old ones put the things that bit"). What the daughters asked of the last man who petitioned for something to leave, eighty years ago: they asked for the thing he used most to lie, and he gave it.

**His private thought (for the GM):** *"A washed man with a soldier's back, and a woman left in the boat who didn't ask to land. The knife he carries smells of brewery, and it isn't his. The old men said the daughters' father would send for his tooth one day. They didn't say he'd send this."*

### 4.4 Hamaura Sōta, the man who can land (G NPC; name-checked; Chad, 7 Oct 2026: "it leads to us having to influence a local… who can be a character of their own mythology")

*Human (Kozakuran) male, 24. Diver of Isohama: the one man the village's women divers (ama) let dive with them. Expert 5, CR 4 (P). GURPS ~110 CP: Swimming-17, Breath Control-16, Boating-13, Weather Sense-12, Survival (Sea)-13. Honesty (12). Sense of Duty (his mother).*

**Why him.** The island admits no women, so **Nym cannot land** (K5), and neither can Electra in her chosen form. The empire's agent needs a man who can wash, land, find the bead, and **whom the island will believe**. Sōta is that man. Nobody in Arik's service sent the agent who finds him, and **Arik will never know his name.**

**Description.** Five foot seven and built for one thing: shoulders broad and round from hauling himself up a rope against the tide, a narrow waist, and a barrel of a chest that can hold one breath for three minutes. His skin is burned dark by salt and wind, darker on the back than the front, the way divers' skin goes. His hair is long and tied in a knot with a twist of straw. Both ears are thickened and slightly misshapen from pressure. He has a white scar across the back of his right hand where a net-line cut him to the bone. Ashore he wears a patched indigo work-coat over a loincloth; in the water, only the loincloth and a white cotton headscarf **stitched with the divers' charms: a five-pointed star and a grid of four lines by five**, against whatever lives down there. He carries a wooden float-tub on a line and a short iron pry-bar for abalone. He smells of seaweed, cold salt and pine-smoke from the divers' hut. When he surfaces he lets his breath out in a long thin whistle, *hyuuuu*, the sea-whistle every ama on the coast makes. Children on the breakwater can tell which diver is coming up by the pitch, and his is the lowest.

**Voice.** Few words, a dry joke at the end of most of them. He never says anything about the island, not even its name, and calls it *"out there."* *"Out there doesn't care who you are. It cares if you're washed. You're not washed. None of you are washed."*

**His mythology (the Urashima rhyme).** Urashima Tarō was a fisherman who saved a turtle and was carried to the palace beneath the sea, where a sea-king's daughter kept him. He came home with a lacquered box he was told never to open. Three hundred years had passed. He opened it, and the years came out as smoke.
- **Act:** three summers ago Sōta cut a sea turtle out of a drift-net and carried it back to the water. Since then, **a turtle surfaces beside him whenever he dives within sight of the island.**
- **Place:** he lives and dives on the strait.
- Two axes give a folk-tale clock, size 4. **(D, TJ-10 = 8): the clock stands at 1 when the empire's agent meets him.** It is the turtle only: he has not yet been "out there," and he has no box.
- **The island is his palace beneath the sea, and the sword-daughters are its princess.** The clock's remaining beats are:
	1. *Taken to the palace:* he lands on Okitsu.
	2. *Given the box:* the daughters' leave.
	3. *The box opened:* the years come out.
	- Each one Myth Pressure pushes toward him (Kozakura Primer §2).

**The box (G; it fires on the lawful path).** When the daughters grant leave, the bead does not come off the island loose. Ichiki brings it down the stair **in a small box of black lacquer tied with a five-coloured cord**, and gives it to whoever petitioned. Rule (P):
- **Unopened until it is in the holder's hand:** the leave holds, and the holder receives the Bridle (§4.1, power 6).
- **Opened on the road, by anyone:** the leave is undone. The curse (*Nothing Leaves*) attaches as if the bead were stolen, and the holder will receive the Feed. **The one who opened it takes the years**: they age 3d6 × 10 years at once (an elf takes the same years against an elf's span). The smell that comes out is the island's: wet stone, cedar smoke and salt.
- **Myth Pressure pushes the carrier to open it.** Every night it travels, the carrier rolls Will DC 12 + the Urashima clock, or opens the cord "just to look." For anyone carrying it other than Sōta, it is DC 10.
- **This is Sōta's tragedy waiting:** his story ends with him opening it. **Whether he carries it, and whether the empire's agent lets him, is the moral weight of the island.**

**The geas (default path; Chad, 7 Oct 2026).** Sōta asks to be bound, and Nym binds him in the boat after the leave.

- **The spell:** *geas/quest* (Cleric 6; Nym prepares it at CL 14).
	- No save; SR applies, and he has none.
	- It lasts until the task is done.
	- If he is prevented from obeying, he takes −2 to every ability score per day, to a cap of −8.
	- **To break it:** *break enchantment*, *limited wish*, *miracle* or *wish*. *Remove curse* works only at CL 16+.
	- **Kitsuki Masatane** (Cleric 15) is the one opponent with a real chance: *break enchantment*, 1d20+15 against DC 25, about 55%.
	- GURPS: Geas (Mind Control), with Compulsion (task) and a Cosmic tie to the box.
- **Why he asks for it.** Every Kozakuran child knows how the Urashima tale ends. **Once he has been told the truth** (§4.4 levers), he understands what the box will do to him, and asks to be bound so his hands cannot open it.
	- **Asked for, it is not coercion.** It costs nothing with the island, the daughters or his mother.
	- **Laid on him unasked,** he finds out when his fingers will not open the cord. Trust ends that moment, Ume hears, and the women divers' network turns on the Hand. The empire loses an asset it never knew it had.
- **When it is laid: in the boat, after the leave, with the box in his hands.** Laid before the landing, the daughters hear a compelled man and the petition's answer drops a step. Laid after, he petitioned free, and the geas binds only the road home.
- **The wording (Nym's choice, and a Trickery priest's art):**

	| Wording | Effect |
	|---|---|
	| ***"Do not open it. Put it into my hands."*** (default) | It binds him to **Nym**, not to the office. **Lorne hears it** (The Two Winners +1): she has claimed the bead for her side of the quarrel over the dead. |
	| *"…into the hands of the Storm King's priest."* | Neutral, and Lorne's hands satisfy it as well as hers. |
	| *"…into the hands of the one who holds the seat."* | He must walk it to **Arik** himself. That forces the discovery scene with a Kozakuran diver standing in the hall. |

- **The geas against the myth.**
	1. **The geas wins outright.** While bound, Sōta makes **no** nightly Will roll against the cord. He cannot open it.
	2. **That breaks the Urashima beat.** The myth bites (Primer §2.3): Sōta is *Unfinished* until someone plays the beat.
	3. **The handover is the recasting.** When he puts the box into Nym's hands, **the role goes with it.** She becomes the one carrying a lacquered box she must never open, and inherits the Urashima clock where it stands.
	4. **She has no geas.** Each night she carries it she rolls Will DC 12 + the clock (Wis-based; she is a Cleric 14).
	5. **RULED (Chad, 7 Oct 2026): she binds herself.** The moment Sōta puts the box into her hands, Nym lays *geas/quest* on herself: ***"Do not open it. Put it into his hands."*** **His hands are Arik's.** That wording forces the discovery (below).

**Nym's self-geas: what follows (default path, ruled).**
- **She cannot open the box.** The geas beats the myth again, so she makes **no** nightly roll. **That is the Urashima beat refused a second time** (Sōta, then Nym).
- **She must reach Arik.** For every day anyone or anything keeps her from moving toward him, she takes −2 to every ability score, to −8.
	- **Everyone who would rather delay her now costs her body:** Jin's orders, Naevys's division work, Lirien's perimeter, Electra's file, Kitsuki's paper war, Sone's bout.
	- **Sone's bout:** if she loses it, the geas still holds. She cannot hand the bead back to the island, so she is bound to break her word to Kashima or rot. That is a hard scene.
	- **Clock seam (R4):** the geas makes Chad's call on *when* the discovery lands in Arik's lane unavoidable. She walks toward him from the Jörmun clock until she arrives.
- **Electra (K19)** has a tag on Nym's soul and will read **pressure** on it: the geas shows as a soul under duress. She can find Nym, escort her, or try to stop her, and stopping her costs Nym. **The file and the geas meet on the road west.**
- **The schism:** Sōta's geas said *"into my hands"*, which was her claim on the bead. Her own says *"into his"*, which hands the claim to the seat. **Lorne reads it either way:** as surrender (The Two Winners −1), or as the bridle doctrine made flesh, a priest who will not keep what is the god's (no change). The GM chooses by Lorne's tell.
- **Jin** hears that a Hand priest is geased to walk into the Emperor's presence with an offering. By his code (serve the seat, never sit it), she is doing the one thing the office is for. **He may escort her himself.** He will not stop her.
- **The Urashima completion (P).** Refused twice, the myth recasts (Primer §2.3), and **the next hands are Arik's.** In the holder's hand the opening is the lawful one (§4.4, the box rule), so **the beat is played, not broken. The myth completes.** When Arik opens the box:
	- **The smoke comes out:** the island's years, smelling of wet stone, cedar smoke and salt. **Because the box was his to open, the years go back to the sea and touch no one.**
	- **Sōta's *Unfinished* status clears.** His story was finished by someone else's hands, which is the mercy at the end of his thread.
	- **The completion boon** goes to the one who played the last beat, which is Arik: **The Palace Hours** (below).

**The Palace Hours: the Urashima completion boon (RULED, Chad, 7 Oct 2026: keep it, once ever)**

*How it relates to the jewel.* These are **separate rewards from separate sources.** On the lawful path, opening the box gives Arik:
1. **The jewel (Hagata-no-Tama)**, with all its powers (§4.1): the Pledge, the Bridle, Hail of the Eight Rings, and the always-on layers. **This is the quest's prize.**
2. **The Palace Hours, once ever.** This is the bonus for completing **Sōta's Urashima story** (the box carried unopened, then opened lawfully by the one it was meant for). It is not a power of the jewel.

On the theft path there is no box and no Urashima completion, so Arik gets the jewel with the Feed and **no Palace Hours.**

*Why this boon.* Urashima's story is about the palace's time against the world's time. He spent three days under the sea and came home to find three hundred years gone. The box held the difference, and opening it let the years out. A completed Urashima myth gives its last actor **one handful of that palace time**: the power to make time run at the palace's rate, once.

*What it is.* **Once ever** (ruled). A single use, kept until spent, with no expiry and no recharge. Arik chooses one of two modes when he spends it.

**Mode A: A Day as a Breath** (time compressed: a day inside, a breath outside).
- **Effect:** Arik and up to eight willing creatures within 30 ft live **a full 24 hours** while the world outside them passes one breath (one round).
- **The space:** they stand in a pale green-gold room of sea-light, the size of the 30-ft circle. Sound from outside does not come in, and the world beyond the edge is a still picture.
- **What a day buys:**
	- Rest: 8 hours' sleep, natural healing for a day, and **prepared casters and clerics can recover their spells**.
	- Counsel: a full war council, a full interrogation (if the prisoner is brought inside), study.
	- Ritual: any rite of 24 hours or less completes.
	- Crafting, mending of gear, and recovering from exhaustion.
- **What it cannot do:**
	- Nothing inside can touch anything outside. No attack, spell, missile or gaze crosses the edge until the day ends.
	- No one outside can enter.
	- Nobody inside can leave early. The day runs its full length.
- **When it ends:** everyone inside **has lived the day.** They are a day hungrier, a day older and a day more tired, and every spell or effect with a duration has run a day. Then the round resumes where it stopped.
- **The table use:** in the middle of the worst fight of the campaign, Arik buys his commanders and casters a full night's rest and a full council, and comes back on the same heartbeat.
- **3.5e:** Su, standard action, one use. It is a stronger cousin of *time stop*: no gap in action for anyone outside, a fixed 24 hours inside, and the inside sealed from the outside in both directions.
- **GURPS:** Altered Time Rate (Accelerated to a day per second, Area 10 yd, Selective, Cosmic, Single Use), with the Barrier enhancement both ways for the duration.

**Mode B: A Breath as a Day** (time accelerated: a day falls on a target in one breath).
- **Effect:** one creature, object, or 30-ft-radius area within 120 ft **has a full day pass for it in a single breath.** The world around it sees nothing but a flicker, and the smell of the box: wet stone, cedar smoke and salt.
- **What the day does:**
	- **Every timed effect on the target advances 24 hours.** That means buffs, summoned creatures, wards, curses, poisons, diseases, countdowns and the duration of illusions. Effects shorter than a day end.
	- **The body lives a day:** hunger, thirst, a day of bleeding, a day of fatigue, a day of natural healing.
	- **Objects get a day:** fires burn down, water evaporates, rations spoil, ice melts, a day's work is undone or completed.
- **Unwilling creatures:** Will DC 25 negates for the creature itself. Objects, areas and the effects inside them get no save.
- **The table use:**
	- Strip every enemy buff and dismiss every summoned creature in a Red Wizard cadre at once.
	- Run out a 24-hour ward, or a gate that holds for a day.
	- **Push a body past Yashiori's 24-hour Root Country ban.** It cuts both ways: Arik could settle the quarrel over the dead with one breath.
	- Spoil a besieger's water, or end an ally's curse that runs on a day-count.
	- **Danger:** it also advances the clock on any countdown curse **toward** its ending. Used on the Mask of the Occupied Oni's three-day reforging, it brings Kureha a day closer.
- **3.5e:** Su, standard action, one use.
- **GURPS:** Affliction (Advance Time 1 day; Area 10 yd or single target; Will-5 resists for creatures; Single Use).

**What it is not.**
- No time travel, no going back, and **no more than one day** either way. The palace gave Urashima three hundred years, but **it gives his last actor one day**, because the rest went back to the sea when the box opened lawfully.
- No killing by age. A day is a day.

**The cost and the hook.**
- **No price is charged to Arik.** The myth completed in his hand and the years went home to the sea, so the boon is clean.
- **But it is palace time, and the palace has a king.** In Kozakuran myth the sea-palace belongs to **Ryūjin, the dragon king of the sea**, whose daughter kept Urashima. The day Arik spends the Palace Hours, **the sea's own court learns who holds a handful of its time.**
- **It is also the first thing of the sea Arik has ever held.** Susanoo was given the sea by his father and refused it (the Sea Mandate, see the pre-wrath notes). **Spending the boon is the first rhyme of that refused mandate.** It starts a Myth Pressure clock toward the sea that he may not want.
- **What it does to the opposition:**
	- **The Orochi remnant** wants the box opened. A bound carrier is useless to it, so **it waits for the handover** and works on Nym.
	- **Kitsuki** goes after Sōta, not the box: break the geas and the old story does the rest.
	- **Sone** doesn't care how the bead travels. His bout is for the bead.
- **What it does to Sōta.** The geas is mercy disguised as compulsion: it is the one thing that keeps him from his story's ending. When it discharges in Nym's hands he is free, *Unfinished*, and his myth has moved on to someone else. His own beat 4 can still come later, through any box. **His story isn't over; it's postponed.**

**Reaction (D, TJ-9 = 8): Poor.** To Isohama, masked foreigners are oni walking (Kozakura Primer §7), and his mother has told him what the last foreigner who asked about *out there* got. He will talk; he will not go.

**Turning him (the agent's work; GURPS reaction re-rolled with these modifiers, or roleplayed):**

| Lever | Modifier | What it costs |
|---|---|---|
| **Masks off** when they talk to him | +2 | The Hand's faces become known on the strait |
| **Through the ama hut** (only a woman can enter the divers' hut, which makes it **Nym's** lever or later Electra's) | +2 | His mother, Hamaura Ume, decides whether the hut hears it |
| **The truth unadorned:** the office, its holder, and that the holder does not know | +2, and **required anyway for a lawful petition** | **A Kozakuran fisherman now carries the empire's secret.** Arik doesn't know it, and a diver on the strait does. |
| **Coin** | +1, once only | Silver from foreigners is bad luck on the boats. Word gets around. |
| **His myth, played on purpose** ("the sea chose you, the turtle knows you") | +3 | **Deliberate casting** (Primer §2.4): +1 Urashima tick per scene, and the myth knows. The box's beat arrives early and harsh. |
| **Coercion** (his mother, his boat) | +2 to compliance, −6 to his honesty on the island | **A coerced man petitions badly.** The daughters hear the fear, and the answer drops a step. |

**What he does on the island (his choices, rolled or played):** he can petition honestly (he is Honest; truth unadorned is easy for him if he has been told it), steal (only if the agent made him a thief), or **refuse at the shrine**, which he does if he learns at the top of 1,140 steps that he was lied to. His reaction to the petition's answer is his own.

**What the empire gets (unsanctioned).**
- An asset on the strait who can land on the Island Not Spoken Of, with a thousand years of offerings on it.
- A diver who knows Isohama's boats and the women divers' network along the coast.
- A thread into Kozakura that touches **Operation Lacquer Road**, the empire's existing Kozakura supply contact.
- **The Veil gets an asset it didn't recruit, run by priests it doesn't know are priests,** for a throne that doesn't know it has them. When Electra arrives, **he goes into her file.**

**Hamaura Ume (G NPC; name-checked).** His mother, 52, headwoman of Isohama's women divers. She is short and heavy-shouldered, with grey hair cropped to the ears and a face lined like old rope. She has dived forty winters and lost a sister to the strait. She keeps the hut, the charms and the rules. **She is the first door for Nym**, a woman who can sit at the hut's fire where Lorne cannot. She will not let her son go *out there* for strangers unless she believes it is the sea's business. **The divers' own warning:** the sea is not the island, and someone once tried to let the sea carry a thing off Okitsu for him. The tide laid it back on the island's shingle with him drowned beside it. *There is no loophole in the water.*

**Private thoughts.**
- Sōta: *"The turtle came up again yesterday, right where the foreign woman was standing on the breakwater. Mother says don't look at it. I looked at it."*
- Ume: *"A woman priest who can't land, a man priest who wants my son, and a turtle that won't leave him alone. I know this story. Nobody likes how it ends."*

---

## 5. The route, stage by stage

**Awareness map (D):** every watching heaven picks up the trail at **Stage 2**. Yakumo-ha TJ-4 = 8, the Orochi remnant TJ-5 = 9, Talos TJ-6 = 10, Amaterasu's watch TJ-7 = 9. **Stage 2 is the arc's crucible.** Enma's wardens (TJ-8 = 6) arrive **the same night** as the first Yashiori kill on Kara-Turan soil, wherever that falls.

| Stage | Where | Clock pressure | Who is watching |
|---|---|---|---|
| S1 The sign | Red Saddle, Anauroch, and the Golden Way's western end | Leaving Jörmun's theater while the Crown battle is still a live trigger | Nobody yet |
| S2 The rite-house | Yashio-dono, Kurogane valley, Kozakura | The first frost festival (G): the eighth vat is opened in 9 days | **Everyone** |
| S3 The crossing | 38 miles of the strait | Winter seas; the boat captain's nerve | Deer on the headland; eight wakes in the water |
| S4 The island | Okitsu-no-shima | Ten days until Ichiki's relief boat arrives | The daughters; Ichiki |
| S5 The return | Strait → Kozakura → the long road west | The curse, if stolen; the pursuit | Everyone, now moving |
| S6 Delivery | Arik's lane | R4, open | — |

### S1 — The sign (Eastern Anauroch)
- **Leads in hand:** the bearing (east, a hand's width north), the bitten grip, and the **dawn-list seal**: eight vats in a ring with a ninth cup in the middle, the seal of **Yashio-dono, the Hall of the Eight Strainings** (G).
- **Identifying the seal:** Knowledge (religion) DC 25 or Theology (Kara-Turan)-14. Or legwork among the Shou caravan-traders at the Golden Way's western end, routed through `hybrid-information-gathering` (Gather Information DC 22, one day, ~40 gp in drink and goodwill). A success gives "a brewing shrine of the storm god in Kozakura's iron country, the house that brews the Orochi festival's sake". A margin of 5+ adds "the festival opens its eighth vat at first frost".
- **Getting east.** Kozakura is about 5,000 miles away as the wind blows. Four routes:
	1. **Wind walk (default, the priests alone).** *Wind walk* is a cleric 6th-level spell: Nym can carry herself plus up to four others. At 600 ft per round that is about 68 mph, for up to 14 hours a casting, so roughly **950 miles a day and 5–6 days east**. Storm-god priests riding the wind to their god's country: the fiction does the work. Each day's flight still ends in a dawn rite somewhere on the way.
	2. **Shadow walk or greater teleport** through **Teodric Halvane** (Wizard 14) or **Durgan Emberlode** (Sorcerer 14). Faster, but it puts more of the Hand into the arc, which brings Jin into it (CP1). Greater teleport needs a destination someone has seen, and none of them has seen Kozakura.
	3. **The Veil's shadow route** to Kara-Tur, if one exists. SR: Shadow Gate Network GM Reference, not read for this draft.
	4. **The long road**: the Golden Way through the Hordelands and Shou Lung. That is months, and S2's festival clock runs out first.
- **Cost of leaving:** the Crown Decisive Battle is a conditional module, and the Hand is its E0 pre-battle strike if the Cult is involved (06, E0). **Two priests gone means the Hand fights E0 without its healers.** Taking a caster as well means E0 at three.
- **Schism beat:** Lorne asks to read the dawn-list himself. If Nym refuses, The Two Winners +1.

### S2 — The rite-house (Yashio-dono, Kurogane valley, Kozakura) — the crucible
- **Place (G).** A river valley in Kozakura's iron-sand country. The water runs rust-red after rain, and the villages smelt iron in clay furnaces that burn for three days and nights at a time. The shrine-brewery sits on a terrace above the river: a walled compound **200 ft by 150 ft** with a torii of black-lacquered cedar at the gate.
- **The brewing hall** is **90 ft by 60 ft**, dim even at noon, its rafters black with a century of steam. **Eight cedar vats**, each 9 ft tall and 8 ft across, stand in a ring around a waist-high stone. On the stone sits a **ninth cup**, a shallow red-lacquer dish the size of two hands. The hall smells of steamed rice, koji mould, wet cedar and the sour-sweet reek of fermentation. The sound is the vats ticking as they work, *plok … plok*, the brewers' work-songs, and the river below.
- **Hiruta Genzō (G NPC),** master brewer-priest (§6.6). He knows:
	- The rite-knife left this house forty years ago in an apprentice's sleeve, going west. The dawn-list kept going in other hands, and he has wondered about it every autumn since.
	- The house's founding story: the storm god's tooth went to his daughters, and the house brews so the tooth will never thirst.
	- The **eighth vat never empties**, and has not in living memory. Brewers who sleep in the hall dream of heads.
- **What happens here, by default:**
	1. **The eighth vat is the remnant made physical** (the cold reading, §3). It holds sake that is sweeter every year and never runs dry. Anyone carrying Yashiori into the hall finds the grip's tooth-marks dry and hot. A *detect evil* reads the vat as a monstrous outsider, exactly as it reads Kusanagi (K2).
	2. **The Yakumo-ha (TJ-4)** learn through the house's tithe: a novice runs to the Izumo-line shrine with word of masked foreigners asking about the tooth.
	3. **Amaterasu's watch (TJ-7):** at dusk on the first evening, **a white deer stands at the torii** and does not run when approached. It is Kashima's messenger (§6.1).
	4. **Talos (TJ-6):** a Calishite trader moored at the valley's river-mouth port prays to the Storm Lord and passes word west by *sending* to Bereth Calloway (§6.5).
	5. **The remnant (TJ-5)** tries to keep the priests here until festival night. Brewers it has soaked through (Hiruta's two senior men, G) offer the eighth vat's cup. Kusanagi's curse is the template: alcohol at double effect, Will DC 20 to refuse a drink offered freely. **This applies to anyone who drinks from the eighth vat.**
	6. **Enma's wardens (TJ-8):** if Yashiori kills anyone here (Yakumo-ha shrine guards, a soaked brewer), Gozu and Mezu arrive the same night.
- **Choice point:** CP4 (Kusanagi) is first live here, because Hiruta knows her old name and her story. The Atsuta box can be reached from here as a side-path (§8).
- **Schism beat:** Lorne pours his own dawn offering into the eighth vat. The Two Winners +1.

### S3 — The crossing (the strait)
- **From:** Isohama (G), a fishing port at the valley's mouth: stone breakwater, drying racks of squid, tar and smoke, and the women divers' hut on the shingle with its charms painted over the door.
- **The local (§4.4):** this is where the empire's agent meets **Hamaura Sōta** and his mother. Turning him is the stage's work. Reaction starts Poor (TJ-9).
- **The run:** **38 miles** to Okitsu-no-shima in Uktar seas. Boats go only for the shrine rotation. A captain will sail for 300 gp or for a reason he believes (Diplomacy DC 20, or Bluff DC 25 because he has heard every lie about that island). Boating/Profession (sailor) DC 18 for the passage, 10–14 hours.
- **On the headland** as they put out: **Sone Takamichi** watches from the cape shrine with the white deer beside him. He does not act; the bead has not moved.
- **In the water:** eight long wakes run alongside the boat from mid-strait. Nothing surfaces. Spot DC 20: the wakes keep station like an escort. **The remnant wants them to reach the shore.**
- **Schism beat:** Lorne reads the escort as the maned one's favor ("He's seeing us in"). If Nym contradicts him in front of the captain, The Two Winners +1.

### S4 — The island (Okitsu-no-shima)
**The problem (K5 + the island's first rule):** Nym, the priest who saw the bridle, carries Yashiori, keeps the dawn-list and is the only one who can find the bead by the dew on the grip. **She cannot land.** The island admits no women.

**The Nym options (CP2b). Chad, 7 Oct 2026: keep the ban; it leads to influencing a local. Default is E.**

| Option | How it plays | Cost |
|---|---|---|
| **E. Sōta lands (default)** | The empire's agent turns Hamaura Sōta (§4.4). He washes, carries Yashiori ashore (Ichiki will not search a diver he has known since boyhood), finds the bead by the dew, and petitions, or steals if they made him a thief. **The Urashima clock ticks on landing.** On leave, he is handed **the box**. | The empire's secret, told to a fisherman. A man whose story ends with the box opened. The Two Winners clock: whichever priest recruited him owns how he petitions. |

| Option | How it plays | Cost |
|---|---|---|
| **A. Lorne lands alone with her dagger** | Nym hands Yashiori to Lorne in the boat. **The man who saw the other winner** washes, wades in, and carries her blade to the daughters' shrine. He finds the bead by the dew. **He chooses which reading he petitions with**, or whether he petitions at all. | The sharpest schism beat in the arc: The Two Winners +2 if he steals, +1 if he petitions on his own reading. Yashiori's dawn rite must be kept by its bearer. **On the island, the bearer is Lorne.** |
| **B. Nym lands in a changed shape** | *Alter self* or *polymorph* to a man's body. **Rule (P): the island sees a changed shape as a lie** (truth unadorned). Landing in one breaks the daughters' Rule: +2 PP, and the petition's answer drops one step. Illusions such as *disguise self* do not survive the washing at all. | She can still find the bead. She can never win a clean leave. Under the sea-curse rules, a stolen bead brings the holder the **Feed**, which is the opposite of her own reading. |
| **C. Nym petitions from the waterline** | She stands in the surf below the tide-line, which is not the island, and petitions at dawn from the sea. Ichiki can carry her words up the stair, but only if she has turned him (the truth unadorned, told to a priest who refused her). | The daughters' answer comes one step harsher; they hear a woman from the sea, and it is their father's priest asking. **The price is still a mask, and hers stays in the boat**, so Lorne must give his or no leave is granted. |
| **D. Electra's true form** (only if she has caught up; P) | Electra lands **in her true shape: grey, featureless, neither man nor woman.** The island allows it, because the shape is no lie. She does it by **dropping every face she owns**, as she did before the angel. | She lands as the faceless one (*noppera-bō*) in a realm that knows the name. Myth Pressure ticks on her hard. **Timing makes this unlikely:** she leaves after the parley, so she usually arrives at S5. |

**Landing (whoever lands).** The boat grounds on the black shingle. Ichiki Shōun stands at the foot of the stair and watches. Every man who lands strips and wades in to the chest. *Misogi*: winter sea, Fort DC 15 or 1d6 nonlethal from cold, which the cold-hardened ignore.
- **The masks stay in the boat.** Whoever lands comes ashore faceless.
- The kit stays too. Yashiori can be landed only by trickery, by stealing it ashore, or with Ichiki's leave, which he refuses (TJ-3). Options: Sleight of Hand DC 25 against Ichiki's Spot, wrapped in a hair-knot, or carried in the mouth.
- **Without Yashiori the bead is hard to find** (DC 35, §4.1).

**The petition (the lawful path).** At dawn the petitioner stands before the shrine and says why the thing must leave.
1. **Ichiki first.** He refuses (Poor). Turning him needs **the truth unadorned**, so any Bluff or magical persuasion fails automatically on the island. A Diplomacy check (DC 25; GURPS reaction re-rolled at +2 if the truth is told whole) succeeds only if the speaker names the office, its holder and the fact that the holder does not know. **For whichever priest petitions, that means telling a stranger, out loud, the secret the office's priesthood exists inside.**
2. **The daughters answer in weather.**
	- A **flat calm at the shrine** means granted, with a price.
	- **Wind from the land** means refused; leave with nothing.
	- **A squall** means the petition is heard but the petitioner lied somewhere, so try again or be refused.
	- Roll at play: 3d6 + the margin of the Diplomacy check (−3 for Option C). 3–9 refused, 10–14 squall, 15+ calm.
3. **The price (G; Ichiki knows the precedent):** *the thing you use most to lie.* **The masks.** Every petitioner leaves his crimson oni face on the offering field, a lacquered oni among the bronze mirrors.
	- Consequence: the masks pass out of Enma's warden-faces and into the daughters' keeping (§6.2). The Hand is down a face for each petitioner.
	- **Jin and the rest of the Hand must decide whether those masks were theirs to give.** Each member chose his or her own wood (K9).

**The theft (the other path).** Find the bead by the dew on the grip, take it and go. Ichiki cannot stop them and does not try. He watches, repeats the last word they said, and goes into the shrine to pray. The **Nothing Leaves** curse attaches (§4.1), and the sea starts worsening the moment the boat pushes off.

**Schism beat:** if Lorne lands alone (Option A), **what he does at the shrine is the schism.** If he petitions on Nym's reading, the Two Winners clock holds. If he petitions on his own, +1. If he steals, +2, and Nym learns in the boat that her blade came back with a stolen tooth.

### S5 — The return (strait → Kozakura → west)
Everyone who became aware at S2 is now moving (§6 for their methods).

| Threat | When it lands | Lawful path (leave granted) | Theft path |
|---|---|---|---|
| **Sone Takamichi** (Amaterasu) | On the Isohama shingle, first landfall | A formal challenge, once. He wants a **bout for the bead** under Kashima's terms (§6.1). He keeps his word whatever the result. | He fights to kill after one formal challenge. The deer brings a second blade by the next dusk. |
| **The Yakumo-ha** | Within 2 days of landfall | A petition to the Celestial Bureau contesting the registration (paper war), plus shrine warriors to delay them | Shrine warriors to take the bead, and a public denunciation |
| **The Orochi remnant** | The first night ashore, or the eighth vat if they pass Yashio-dono again | It wants the bead in motion and away from Arik. It tries the drink first. | Same, at sea as well: the "escort" turns |
| **Enma's wardens** | The same night as the first Yashiori kill on Kara-Turan soil (TJ-8), if one has not already happened | They want the masks. If the masks are on the island, they want an accounting instead. | Masks and Yashiori's denied dead |
| **Talos (Bereth Calloway)** | Where the priests come back into Faerûn | He has nothing to say, so he tries to provoke a theft-shaped act in front of witnesses | He has his story, and brings witnesses and a Talassan chapter-house |

### S6 — Delivery
The bead must be **placed in the holder's hand and received** (§4.1). See §9.

---

## 6. The opposition across the heavens

*Stat lines are P (proposed): CR bands are set against the Hand (CR 13–14 each) so every opponent is a peer threat, never a wall. Full builds go through the same Phase 6 pipeline as the Hand. Every named NPC is name-checked (§11).*

### 6.1 Amaterasu's court: Sone Takamichi and the white deer
**Why they come.** The bead was **her** jewel. The gods breathed out of her jewels were hers by her own ruling, and the imperial line comes from one of them. A foreign claimant in her banished brother's seat is sending servants to take her property off her nieces' island. Heaven's answer is the one it gave Izumo: send Kashima.

**Sone Takamichi (G).** *Human (Kozakuran) male, 44. Swordsman-retainer of the Kashima shrine. Fighter 13, CR 13 (P). GURPS ~400 CP: Broadsword (katana)-20, Sumo Wrestling-19, Judo-16, Savoir-Faire (Shrine)-14, Strategy-12. Honesty (12), Code of Honor (Kashima: one challenge, stated terms, kept word), Duty (the court).*
- **Description.** Five foot eight, built through the neck and shoulders like a draught ox, a grappler's frame under a swordsman's posture. Shaved pate with a tight topknot. A broad face, the nose broken flat more than once, and the left ear thickened into a lump of gristle from forty years on the bout-ring sand. Black eyes set deep. Clean-shaven. Dark-blue kosode and hakama, plain except for a small white crest at each shoulder: a deer's antler crossed with a lightning stroke. One sword, worn edge-up on the left hip, in an undecorated black scabbard; he carries no companion blade, as the old Kashima men did. A short knife with an antler handle at the small of his back. Straw sandals, bare calves scarred white along both shins. He smells of camphor oil and wet wool.
- **Voice.** Formal. He states terms in full sentences and then stops talking. He never threatens. *"I am Sone Takamichi of Kashima. You have my lady's jewel. I offer you one bout for it, on the sand, by the old terms. If you throw me, it is yours and I will say so to Heaven. If I throw you, it goes back to the island. Choose a day."*
- **The bout (Kashima terms).** A ring of sand 15 ft across. Unarmed and unarmoured. Best of three falls: a fall is any part of the body above the sole touching the sand, or leaving the ring.
	- **3.5e:** opposed grapple checks, three exchanges a fall. Sone's grapple is +22 (P): BAB +13, Str +4, Improved Grapple +4, a +1 sumo specialty.
	- **GURPS:** Sumo Wrestling quick contests, best of three.
	- **He keeps the result exactly**, either way, and reports it to the court through the deer. A thrown Kashima man is the strongest legal footing the office can get in Heaven: **winning the bout clears the bead's standing with Amaterasu's court.**
- **On the theft path,** he gives one formal challenge. If they refuse, he fights to kill, sword out, as soon as they are clear of shrine ground.
- **The white deer.** A spirit messenger, CR 5 (P). It cannot be harmed on shrine ground. It sees through illusion and disguise at will (*true seeing*). It can step into the Spirit World and carry word to the court by the next dusk. It never fights. It watches, and what it sees, the court knows.
- **Private thought:** *"An elf priest and a half-elf priest, and neither of them knows who he serves well enough to say it plainly. My lady's brother was the same. Weeping, raging and clever, and never once still."*

### 6.2 Enma-Ō's hells: Gozu and Mezu
**Why they come.** Two causes of action:
1. **The faces.** Oni are Enma's wardens. The Hand wears warden-faces in the service of a different death-office, and in Enma's court that is impersonation of an officer.
2. **The denied dead.** Yashiori's Root Country keeps the slain from being raised for 24 hours, and in Kara-Tur that interferes with Enma's intake.
They come the **same night** as the first Yashiori kill on Kara-Turan soil (TJ-8 = 6).

**Gozu (Ox-Head) and Mezu (Horse-Head) (myth figures; builds P).** *Large outsiders (lawful, evil, native to Enma's hells), CR 15 each (P), 20 HD. 3.5e chassis: start from the MM oni and ogre-mage line and build up. SR for the full block.*
- **Gozu.** Twelve feet tall: the head of a black ox with the left horn broken off at the root, and below it a man's body, bull-heavy, its skin the dark red of old liver. An iron collar is riveted round the neck. He carries a ten-foot iron fork with three blackened tines. He smells of byre, dung and brimstone. He speaks slowly, one word at a time, as if each costs him.
- **Mezu.** As tall, narrower: a chestnut horse's head with a white blaze and wet, rolling eyes on a long-limbed body with grey-green skin. A chain of black iron hangs coiled from shoulder to hip, and a ledger is bound in hide at his belt. He talks fast, and reads aloud.
- **Ledger-sight (Su, P).** Whatever a creature has killed is written in Mezu's ledger. Neither can be hidden from a killer whose dead they are owed: *nondetection* and *mind blank* do not stop the finding, though they do stop scrying.
- **Warden's Seizure (Su, P).** Mezu's chain grapples at 15 ft reach (grapple +30). With a grappled creature in hand, either of them can plane shift to Enma's court as a standard action. **A seized priest stands trial.**
- **How they open.** With a summons, never an attack: *"Enma-Ō's court requires an accounting of the faces."* They demand the masks.
	- **Surrender:** the masks go to Enma, and the Hand has lost its faces to the court.
	- **Argue jurisdiction:** the dead belong to the Root Country, a separate afterlife (K7). Knowledge (the planes) DC 25 / Law (Kara-Turan celestial) contest vs Mezu's 16. A win buys a hearing in a month instead of a seizure tonight.
	- **Trick them:** the obvious Trickery move. Every trick that works is written in the ledger.
	- **Fight.** Then **Enma notices** (K7 hook fires).
- **If the masks were left on the island** (S4 lawful path), the wardens find them in the daughters' keeping and want an accounting instead: an inter-court matter. That is the cleanest outcome, and it still puts the Hand on Enma's docket.

### 6.3 The rival sect: the Yakumo-ha (the House of Eight Clouds)
**Who they are (G).** The hereditary shrine-house of Susanoo's Izumo line, seated at **Yakumo-dono at Suga** in Kozakura. It is the place the myth says Susanoo built his first palace and made the first poem: *eight clouds rise*. Its high priests descend from a god breathed out of the jewels Susanoo chewed, a god Amaterasu sent to subdue Izumo who served Izumo's lord instead. **Half Sun, half Storm, by blood.**

**Why they come.** The seat is Kozakura's to fill, or no one's. A foreign drow in Susanoo's office is a usurpation, and two foreign priests registered as the office's clergy would put a millennium-old house under the orders of strangers. And the bead is **their ancestor's womb**.

**Kitsuki Masatane (G).** *Human (Kozakuran) male, 63. High priest of the Yakumo-ha. Cleric 15, Trickery/Death (the office's own grant, LOG-832), CR 15. GURPS ~350 CP: Religious Ritual-18, Law (Celestial Bureau)-17, Poetry-16, Savoir-Faire (High)-16, Politics-15.*
- **Description.** Tall for a Kozakuran, five foot eleven, gaunt, and stooped at the neck the way tall men get from bowing through doorways. White hair dressed in the court manner under a tall black-lacquered cap. A long, hollow-cheeked face, clean-shaven, with a mole at the corner of the right eye. Eyes heavy-lidded and dark. White over-robe on pale purple hakama, the colour of his hereditary rank. Long fingers, the right first and second stained grey with ink at the tips. A folding fan of cypress slats that he opens a slat at a time when he is thinking. He smells of incense and inkstone.
- **Voice.** Soft and exact, with the habit of answering in poetry when cornered. *"Eight clouds rise over Izumo. Eight-fold the fence they build. It was our fence first."*
- **The ruling hook (P, flagged for Chad):** since 1493, the year the office filled (K1), **his prayers have answered in a voice he does not know.** His spells still come, and they come **through the seat**: through Arik. He knows something changed and has spent five years trying to learn what. **The Hand's quest tells him.**
- **Methods:**
	- **A paper war.** A petition to the Celestial Bureau contesting any registration, which he has the standing to file. He is a better lawyer than either Hand priest. Without the holder's own seal, he wins.
	- **Shrine warriors.** Twenty sohei (Fighter 4–6, P) under a captain (Fighter 9, G, unnamed).
	- **Alliances.** With Amaterasu's court, on his Sun half, against a common usurper. Possibly with Talos, quietly, because the enemy of my usurper serves.
- **Private thought:** *"Five years my gods have answered in a stranger's weather. Now strangers come asking where the tooth lies. Good. At last someone will tell me who has been listening."*

### 6.4 The Orochi remnant (the Koshi brood)
**What it is.** Not a body; an appetite left in pieces. **The Fourth Tail** lives in Kusanagi (K2). Another piece lives in **the eighth vat at Yashio-dono** (S2), and others in the strait (the eight wakes) and wherever sake is brewed for the festival. It ate seven daughters before the storm god came. It has not stopped wanting.

**What it wants.** The bead **in motion**, off the island and **away from the holder**. The bead carries the bite. A bite that is owned is a bridle; a bite in the serpent's keeping is a memory it can unmake. Its ideal ending: the bead **drowned in the eighth vat**, or carried within 60 ft of the Fourth Tail with no Arik in the room (open).

**Methods (P):**
- **The drink.** Will DC 20 to refuse a cup offered freely, double effect, applied to anyone who drinks the eighth vat (S2).
- **Soaked men.** Hiruta's two senior brewers (G, unnamed). Commoner 3 / Expert 2. They read as monstrous outsiders to *detect evil*, and they offer cups.
- **The wakes.** Huge water-bodies with teeth, CR 12 each (P; elemental chassis with grab and drown). Eight of them, though never more than two strike together.
- **The vision itself**, on the cold reading (§3).
- **Endgame hook:** if the bead reaches Arik's hall while Kusanagi is in it, the Fourth Tail knows (§4.1, the Bite). That ties to the Kusanagi page's warning that the cure will be a war, because the tenant will fight from inside her senses.

### 6.5 Talos's heaven: Stormlord Bereth Calloway
**Why he comes.** Talos has no standing and no mechanism to contest the office (K1). What he can do is make the claim **look stolen**. A theft from a sacred island gives him a complaint any court will hear, and gives the storm-faithful of Faerûn a story that turns recognition into suspicion.

**Bereth Calloway (G).** *Human (Faerûnian) male, 47. Stormlord of Talos, Cleric 13, Destruction/Storm, CR 13 (P). GURPS ~350 CP: Religious Ritual (Talos)-15, Public Speaking-16, Intimidation-15, Fast-Talk-14, Weather Sense-14.*
- **Description.** Six foot one and heavy, gone soft at the belly over a frame that was hard once. A weather-burned red face. A black beard shot through with copper-coloured streaks where lightning crossed it at thirty, and the right eye milky white from the same strike; he wears no patch. Hands like spades. Leather and chain under a storm-grey cloak worked with jagged gold forks. Talos's three-bolt symbol hammered into a bronze plaque on his chest. A heavy flanged mace whose head is forged into a forked bolt. He smells of ozone, sweat and wine.
- **Voice.** Loud and amused, a preacher's voice; he laughs at his own threats. *"A drow sits in a dead god's chair and sends his little elves to rob a girl's island. I don't need to fight you, lads. I need a crowd."*
- **Methods.**
	- **Witnesses**, through a Talassan chapter and hired notaries.
	- **Provocation:** he tries to make the priests do something theft-shaped in public.
	- **On the theft path he already has his story.** He carries it to Talos's church, to Faerûn's storm-faithful, and to anyone who would pay for a lever on Arik (cross-ref: the Pale Name Evolution's "two-front squeeze", where every attack survived is still recognition).
	- He fights only when cornered. He is not stupid.
- **Private thought:** *"The Storm Lord can't touch the chair. I can touch the man's reputation. Gods are made of what people say about them. So are thrones."*

### 6.6 The ground at Yashio-dono: Hiruta Genzō
*Human (Kozakuran) male, 58. Master brewer-priest of Yashio-dono. Expert 6 / Adept 3 (G), CR 6. GURPS ~150 CP: Brewing-18, Religious Ritual-14, Merchant-13.*
- **Description.** Short and thick-armed, with a belly like one of his own vats. Grey hair shaved to stubble. A round face red at the cheeks from forty years of steam, and the left eye half-closed by an old burn from a boiling-rice accident. Indigo work-coat, sleeves tied back with a cord, a headband soaked dark. Forearms scalded pink in patches. Wooden clogs. He smells of koji and rice-steam.
- **Voice.** Gruff, practical, and pious about the work rather than the gods. *"The knife came home smelling of my rice. Forty years. You've kept it fed. Sit down."*
- **What he wants:** the knife's story; to be rid of the eighth vat without losing the festival; and for nobody to drink from it while foreigners are watching.
- **Private thought:** *"Bitten. The grip's bitten. My grandfather said the god's tooth would wake when the god woke. He didn't say the god would be a foreigner, or that I'd be glad."*

### 6.7 Background: Thay
Yashiori's Root Country makes it a Thayan prize (05b). This arc does not activate Thay. If the Crown battle has fired and Thay knows the dagger, the Golden Way legs of the journey are exposed.

---

## 7. Stakes and outcomes

| Outcome | What it takes | What the sect gains | What it costs | What the world does |
|---|---|---|---|---|
| **Full, lawful** | Leave from the daughters (masks given), the bout with Sone won, the bead received by Arik | **Primacy:** registered clergy, Kara-Turan shrines route through them, +1 CL on domain spells, Yashiori's appetite fed anywhere. **The holder receives the Bridle**, and the clergy can call the Hail of the Eight Rings. | Two masks lost to the island. The secret told aloud to Ichiki. Arik knows. | Amaterasu's court is satisfied. Kitsuki loses the paper war and **learns where his prayers go**. Enma's docket holds an inter-court matter. Talos has nothing. |
| **Full, stolen** | The bead taken and received by Arik | The same registration, but the Bureau files it with a theft attached. **The holder receives the Feed** (the Storm's Rage, the Thirst; the Fourth Tail wakes). | The Unspoken and the sea curse until the daughters are appeased. Sone hunting. Calloway's story. | Amaterasu holds a grievance with standing. The Yakumo-ha can contest it forever. **Talos has his lever.** |
| **Partial: offered and refused** | The bead reaches Arik, and he will not close his hand | Nothing is registered. The bead is a pledge offered and not received. | The priests stand exposed before the man they served in secret | Everything rides on Chad's Emperor-of-Mankind answer (§9) |
| **Partial: the bout lost** | Sone throws the petitioner | The bead goes back to the island. The sect keeps its secret and its masks, if they never petitioned. | Face before Heaven. The vision unanswered. | The court's watch ends. Kitsuki knows. |
| **Failure: the remnant** | The bead drowned in the eighth vat, or lost at sea | Nothing | The bite in the serpent's keeping | **Bridle becomes feed.** The temperament in the vision has one less restraint. Read it on reading 3. |
| **Failure: the wardens** | A priest seized to Enma's court | One priest left, alone | A trial in the hells | Enma notices (K7). The Hand is on his docket. |

**The Pale Name meter (R3).** Each outcome feeds it, unpriced. Even the failures were addressed to the Name: every attack survived is recognition, per the Pale Name Evolution's two-front squeeze.

---

## 8. Choice points

| # | Choice | Weight | Options and consequences |
|---|---|---|---|
| CP1 | **Jin's sanction** | Heavy | **Ask** (Jin's code: serve the seat, never sit it; he may judge that the priests are deciding *for* the seat) → roll Jin's reaction at play; he may forbid, join, or send Teodric or Durgan. **Go without asking** → the Hand learns afterward, and Jin's trust in the priests is spent. |
| CP2 | **Petition or theft** (S4) | Heavy | **Petition:** the truth told aloud, the masks given, Sone's bout available, a clean registration. **Theft:** the curse, Sone's sword, Calloway's lever, a registration with a stain. |
| CP3 | **The masks and Enma** (S2/S5) | Medium | **Surrender** them to the wardens → the faces go to Enma. **Argue** jurisdiction → a hearing later. **Trick** → it goes in the ledger. **Fight** → Enma notices. Giving them to the daughters first (CP2) changes the question. |
| CP4 | **Kusanagi** | Heavy | **Involve her:** she opens doors in Kozakura, and Hiruta and Kitsuki know her old name. But she cannot land on the island, **the Fourth Tail feels the bead within 60 ft**, and she is Arik's sworn retainer: **the secret reaches Arik early.** **The Atsuta box** shows the bead's resting place without the dawn-list leads, but opening it tells Kusanagi someone looked (K3), which also brings the discovery early. **Leave her out:** slower, safer. |
| CP4b | **The way home** | Medium | **Through Eastern Anauroch** (fast, wind walk, home ground): every dragon within 60 ft knows (Scale Remembers), and Jörmun may reach Arik first. **Round it** (slower, through the Moonsea or by sea): Calloway's ground, and days added to every pursuer's clock. |
| CP5 | **Delivery** (S6) | Terminal | **Place it in his hand** → forces the discovery and completes the pledge if he closes his hand. **Enshrine it in his name and say nothing** → the office is fed, the holder never receives it, nothing is registered, the secret holds. That is the sect choosing the seat over the man, which Jin would call the one sin of the office. |
| CP7 | **Quavein** (K20) | Heavy | **Tell the Bursar.** The office's captain-rank priest, the warrior face, may claim the quest, bless it, or write it in his black book as a debt. **Whoever tells him first gets him as the schism's judge.** **Keep it from him:** if he learns from his ledger, which is likely, he collects. |
| CP8 | **Hamaura Sōta** (§4.4) | Heavy | **How he's turned** (truth, coin, his own myth, coercion). **The geas** (default: he asks, Nym lays it in the boat after the leave, worded *"into my hands"*): asked or unasked, and the wording. **Who carries the box after the handover:** Nym inherits the Urashima role and the nightly roll unless she binds herself. **What happens to him after:** a kept asset on the strait, or a spent one. |
| CP2b | **Nym and the island** (S4) | Heavy | Lorne lands with her dagger / Nym lands in a changed shape / Nym petitions from the waterline / Electra's true form. See S4. |
| CP6 | **The Two Winners** (§3.2) | Heavy, slow | When the clock fills: does Lorne leave, stay and serve the temperament inside the sect, or get brought back? The discovery scene then has to answer **which priest Arik sanctions**. |

---

## 9. The discovery: how the arc ends at Arik

**The forcing logic (now doubled).** Nym's self-geas (§4.4) **walks her into Arik's presence**: she cannot stop or turn aside without paying for every day of it. The pledge must be *received*, and only the holder can receive it (§4.1). Every success path ends with two masked Veil agents, or two unmasked ones if the island took their faces, standing in front of Arik with a jade bead and a confession. **Failure paths reach him too, worse:** through Calloway's story, Kitsuki's Bureau suit, or a priest's trial in Enma's court.

**The Electra route (K18).** This is the earliest possible discovery. She knows from 12 Uktar. **When she tells Arik, if she does, decides whether the discovery comes before the quest, during it, or after the bead arrives** (§2.5). If she holds the file, she is in the room for the discovery scene with a dossier she has kept from him. That is its own scene.

**The dragon route (Scale Remembers).** The priests come home through Eastern Anauroch, which is Jörmun's country. Any dragon within 60 ft of the bead knows it is there.
- **Jörmun** is the Frostborn Legate, a lindwurm and a PC, and he will feel a serpent-killer's tooth walk past him.
- **Gary** (an ancient red) and **Shi'van's bonded dragon** will feel it too.
- **The Wyrmhelm roster** feels it at any base the priests pass.
- What any of them do with that knowledge belongs to play; for Jörmun it belongs to his player. **Any of them can carry it to Arik before the priests do.** That is the most likely early discovery, and it makes the priests' route home a choice: cross the empire's dragon country, or go round it.

**The room (set the table; do not write Arik's answer).** The venue and date are R4 (open). Whoever is in the hall, these are live:

- **Arik.** He has never been told he has priests. He holds the Pale Name and the Storm King's office, and he wears the Cloak of Wandering Thunder.
	- Chad's forward note (K6): the Emperor-of-Mankind line. Worship denied as a rule, these priests a sanctioned exception. **Chad rules this live.**
	- The question the arc hands him: **which priest?** Nym, who saw the bridle, or Lorne, who saw the throw. Or both. Or neither.
- **Jin.** If present, he kneels at Arik's left knee, as is canon for him (K10). He serves the seat, and the priests served it without the man. **What Jin says, if he speaks, is the office reading of what they did.**
- **Lirien.** The priests are Veil agents. Her network has been running a cult inside itself and she did not know. Her face is a scene of its own; route through `hybrid-intelligence-ops` for the Veil fallout.
- **Kusanagi,** if present. **The Sickness (K4):** she cannot draw the shrine blade in a sovereign's hall. The **Bite (§4.1)**: the Fourth Tail knows the bead is in the room. Her own vision of Arik as Susanoo, with its four readings, is now one of three visions of the same seat. Hers, Nym's and Lorne's disagree on which storm god he is and on who is winning.
- **The bead** on the table, or in his hand, or refused.

**What the discovery is NOT allowed to settle:** the four readings (§3), bridle versus feed (§4.1), or the meter's price. Those stay open, as Kusanagi's vision does.

---

## 10. Rolls ledger (D)
Method: Python `secrets`, 3d6, four throws, **lower median** (second-lowest of four), no rerolls. File: `tooth_marked_jewel_rolls.json`. Script: `roll.py`.

| ID | Question | Throws | Result | Reading |
|---|---|---|---|---|
| TJ-1 | Dawn of the vision (day of Uktar 1498) | 13, 12, 13, 6 | **12** | **12 Uktar 1498 DR** |
| TJ-2 | Lorne witnesses: 3–10 Nym alone; 11–18 both, Lorne sees the other figure win | 17, 11, 11, 9 | **11** | **Both witness. Lorne sees the maned one throw the pale one.** |
| TJ-3 | Ichiki Shōun's reaction (GURPS, no modifier) | 12, 8, 8, 10 | **8** | **Poor.** Allows the landing, refuses the petition. |
| TJ-4 | Yakumo-ha awareness stage | 8, 8, 7, 14 | **8** | **S2**, the rite-house |
| TJ-5 | Orochi remnant awareness stage | 5, 11, 9, 13 | **9** | **S2** |
| TJ-6 | Talos (Calloway) awareness stage | 13, 5, 10, 15 | **10** | **S2** |
| TJ-7 | Amaterasu's watch begins | 10, 10, 9, 6 | **9** | **S2** (the deer at the torii) |
| TJ-8 | Enma's wardens: delay after the first Yashiori kill on Kara-Turan soil | 5, 15, 6, 13 | **6** | **The same night** |

| TJ-9 | Hamaura Sōta's reaction to the masked foreigners | 7, 15, 8, 14 | **8** | **Poor.** He will talk; he will not go. |
| TJ-10 | Where his Urashima clock stands when they meet | 7, 10, 13, 8 | **8** | **1 (the turtle only)** |

**Rolls held for play (not thrown):** Jin's reaction (CP1); the daughters' answer (S4, 3d6 + Diplomacy margin); Sone's bout (opposed grapples / Sumo contests); the wardens' jurisdiction contest; The Two Winners clock advances.

---

## 11. Names, collisions and open items

**Name checks (NPC database SQL + Notion search, 5 Oct 2026):**

| Name | Result |
|---|---|
| Kitsuki Masatane | No match |
| Sone Takamichi | No match. **Note:** *Tenjin Kasuga* exists (an iaijutsu NPC). Kasuga is also the deer shrine tied to Kashima. Sone's crest avoids the Kasuga name. |
| Bereth Calloway | No match |
| Ichiki Shōun | No match |
| Hiruta Genzō | No match |
| Gozu, Mezu, Enma | No NPC rows (myth figures) |
| ~~Varen Hask~~ | **Rejected:** near-miss with *Varen Keth* (Binding Expert) |
| Okitsu-no-shima, Hagata-no-Tama, Yashio-dono | No Notion hits |
| Yakumo-ha, Isohama, Kurogane valley, Red Saddle | Generated; no hits |

**Open items for Chad:**
1. **R4, the clock.** When does the discovery land in Arik's lane, given the Jörmun clock at Uktar 1498, Arik's arc around 1495, and Jin's lane unset (LOG-824)?
2. **Kitsuki's prayers answering through the seat** (§6.3). That is a cosmological ruling: do the office's *other* worshippers already draw through Arik?
3. **Hagata-no-Tama's powers v2** (§4.1): three layers, seven powers, the Bridle/Feed fork, the access rule. Rulings needed: is Celestial Bureau registration the right shape for "primacy"; Bane of the Eight is now ruled (Chad: all reptiles, including dragons, snakes and nagas); dragons sense it in turn (ruled: Scale Remembers); and does the Yakumo-ha count as office clergy for access (ties to item 2).
4. **The masks as the island's price** (S4). The masks are Chad's ruling (the crimson oni masks), so giving them away is his call to allow.
5. **Pale Name meter price** for the vision and for each outcome (R3).
6. **Builds (SR, Phase 6 pipeline):** Gozu and Mezu, the white deer, the wakes, Sone, Kitsuki, Calloway, sohei.
7. **The Veil shadow route to Kara-Tur** (S1 option 3): the Shadow Gate Network page was not read for this draft.
8a. ~~Electra's choice~~: **RULED, she holds it and opens a file** (K19).
8b. ~~Electra's pursuit east~~: **RULED, she goes after the parley and tags Nym** (K19). Open: the parley's length, which sets her arrival stage, normally S5.
8d. ~~Nym and the island~~: **RULED (7 Oct): the ban stays; the default is influencing a local** (Option E, Hamaura Sōta).
8g. **The box rule** (§4.4): an opened box undoes the leave and the opener ages 3d6 × 10 years. Confirm or tune it.
8h. **The geas** (§4.4): **RULED (Chad, 7 Oct).** Sōta asks; Nym lays it in the boat after the leave (*"into my hands"*). **Nym binds herself: *"into his hands," meaning Arik's.*** The discovery is now forced by the geas. Open: R4 (when it lands in Arik's lane); Lorne's reading of the surrender. **Palace Hours: RULED, kept, once ever** (§4.4).
8e. **The changed-shape rule** (S4, Option B): does the island treat *alter self* or *polymorph* as a lie? And does Electra's true form count as neither man nor woman (Option D)?
8f. **Quavein** (CP7): does anyone tell the Bursar, and does his ledger already know?
8c. **Envoy reading of Electra** in Kozakura (primer, P).
8. **Adventure-arc-builder:** if this should become a playable module, run it through the Notion adventure-arc-builder next. This document is its design brief.

**On approval (not done yet):**
- A Notion child page under **The Hand — Standing Roster**, carrying this document.
- The repo mirror (this file) stays on branch `claude/sleepy-hawking-oap9se`.
- A Change Log entry in the 📋 Canon Change Log, Session field blank, PROJECTED, nothing played.
- A cross-link line appended (append-only) to the Hand roster and the Kusanagi page's banked-hooks list.

### 11.1 The Pale Name's Kozakuran titles (APPROVED, Chad 7 Oct; design canon, nothing played)

**The root.** The *Nihon Shoki* writes the god as **素戔嗚尊**. Its first character, **素** (*su*), is undyed white silk: plain, bare, pale. **嗚** is a wail. Read through those characters, the office's name is "the bare one who wails," so the Pale Name has always sat inside it. When Kitsuki or an onmyōji notices this, it is a revelation scene (a candidate recognition event, unpriced; see item 5).

**Before the claim:**

| Title | Meaning | Register |
|---|---|---|
| **Shirana-no-Kami** (白名神) | "The White-Name God"; also *shirana*, "unknown" | Scholars and onmyōji, in writing |
| **Marebito** (稀人) | The visiting stranger-god from across the sea | Villagers and shrine folk |
| **Araburu kami** (荒ぶる神) | A raging, unsubdued god (the Kojiki's term for gods outside heaven's order) | Amaterasu's court, as an accusation |

- Rank: ***mui*** (無位), unranked in the divine register.
- Suffix: ***-no-Kami***.

**After the claim:**

| Title | Meaning | Register |
|---|---|---|
| **Takehaya Susanoo-no-Mikoto** (建速素戔嗚尊) | "Brave, Swift, Impetuous Male, Augustness" | The office's full title |
| **Shō Ichii** (正一位) | Senior First Rank, the top of the divine register | What Celestial Bureau registration (§4.1, Pledge of the Clean Heart) looks like in Kozakuran paperwork: the sect's primacy in one line |
| **Gozu Tennō** (牛頭天王) | The Ox-Headed Heavenly King, the plague-lord | Those who fear him rather than worship him |

**The change, as the world shows it.** *-no-Kami* becomes *-no-Mikoto*, and *mui* becomes *Shō Ichii*. Shrine tablets, placards, prayers and court registers are rewritten, so the ecology and Myth Pressure systems have a visible tell.

**Meter hook (unpriced, see item 5).** In the *Izumo Fudoki*, Susanoo said of Susa: *"This is a small country, but a good place. I will not set my name on trees and stones,"* and he laid his own spirit into the land, which took his name. If Arik ever sets his name into a Kozakuran place, that is the largest recognition event this arc can produce. Price it at or above the vision.
