## Full-corpus pass (6 Oct 2026): what changed and why

**Chad's ruling.** Every signature piece is re-rolled against the **full corpus**: the loot-engine pools (136 rows) plus the registered compendia. That is 118 book weapon properties (DMG and Magic Item Compendium), 13 Diablo II modifiers and 19 Warhammer Dwarf runes.
- **Excluded:**
	- Enchantments laid on a weapon after it is made: WoW enchants, Magic Item Compendium augment crystals, runewords.
	- Magic Item Compendium specific weapons (finished items), inactive psionic and incarnum entries, and "covered" duplicates.
- **Rules applied:**
	- **No duplicates across the host:** the first piece to draw an affix keeps it.
	- **Logic:** a draw the bearer can't use rerolls within its pool.
	- Every throw is printed.
- **Kept:** rarity, affix count, masterwork result, sockets, bases, releases and the five Uniques (Naevys, Mercy, Ilvaera, Kerra, Nym).

**Why the first pass failed.** The first pass drew only from the 136-row snapshot bundled with `loot_roll.py`. The compendia were never read. That produced crowding (Chameleon on four pieces, three each of Familiar Bond, Souldrinker and Wardbreaker) and draws that needed awkward translation.

**Raw output:** `full_corpus_pass_rolls.txt`, plus an audit section at its end. **Driver:** `roll_full_corpus_pass.py`. **Corpus snapshot:** `corpus_affixes_source.json`.
- **In the pass:** 70 draws were rerolled under the logic or no-duplicate rules.
- **On hand audit:** three more illogical results the filter missed were rerolled and logged:
	- Faelith's Signature Move (a fighter has no save-DC class ability);
	- Edwyn's Chain Lightning temper (no lightning on the glove);
	- Durgan's Whirlwind temper, then Momentum Crit (melee and extra-attack techniques on what was then a heavy crossbow).

**Superseded by this pass:**
- The round-5 cards for these 21 pieces.
- Ivrael's reroll from earlier today.
- The round-5 stat-block errata.

The old item names that change are retired on the manifests.

| Piece | Rarity · tier | Affixes (★ = Greater) | Temper · aspect | UDRP |
|---|---|---|---|---|
| Quavein · The Last Column | Legendary · T1 | Dimensional Pocket · Mana Leech★ · Warding · Second Wind | 23H-8 Vital Strike · 24E-5 Detonation | 31 |
| Hadda · Mine to Call | Unique-grade (rolled Legendary draws) · T1 | Souldrinking · Master Rune of Skalf Blackhammer · Striking · Morphing★ | 23H-5 Armor Shatter · 24J-1 Inevitable | 36 |
| Tarvash | Rare · T1 | Parrying · Riposte · Shield Wall | none | 3 |
| Aerendyl | Rare · T1 | Weapon Mastery · Master Rune of Dragon Slaying · Undying | 23H-2 Killing Blow | 16 |
| Kesh · Inside Ten | Legendary · T1 | Animal Bond · Mind Fog · Deflecting · Rune of Cleaving★ | 23E-3 Shadowstep · 24J-5 Cataclysm | 34 |
| Marit · Between the Joints | Legendary · T1 | Stoneskin · Radiant · Freeze Target · Spider's Gift | 23A-4 Precise Thrust · 24G-6 Coiled Spring | 25 |
| Brunna · The Hinge-Pins | Legendary · T1 | Endurance★ (capstone) · Blinding★ · Rune of Striking · Ghost Strike | 23C-3 Parrying Grace · 24G-5 Horizon | 38 |
| Zaheda · The Teacher's Hide | Legendary · T1 | Battle Trance★ · Absorption · Undead Servitor★ (capstone) · Chameleon★ | 23D-8 Sacrifice Pool · 24F-6 Pack | 37 |
| Ysmay | Rare · T1 | Linguist · Aegis · Commander's Voice | 23E-7 Aerial Dash | 8 |
| Dace | Rare · T1 | Lethal Focus · Sweeping · Life Shield | none | 9 |
| Osmund · Mourners' Brass | Legendary · T2 | Penetrating Strikes · Shadowtouch · Leech · Chance to Cast on Attack | 23C-2 Reactive Armor · 24A-3 Tempest | 24 |
| Wenna | Rare · T1 | Stormborn · Trackless · Pack Mule★ | 23A-7 Lunging Reach | 8 |
| Faelith · The Wrong Note | Legendary · T1 | Battle Meditation · Banefire · Thorns★ · Rune of Fire★ | 23H-4 Hemorrhage · 24G-4 Wind | 28 |
| Patience | Rare · T1 | Anarchic★ · Master Rune of Death · Thrift | none | 5 |
| Rhun · The Relief | Legendary · T1 | Prismatic Burst · Prismatic★ · Vicious · Vampiric | 23B-6 Elemental Confluence · 24B-5 Flanker | 35 |
| Edwyn · Compline | Legendary · T1 | Fleshgrinding★ · Holy★ · Flaming Burst · Nimble | 23I-6 Shadow Meld · 24G-2 Tidal Surge | 27 |
| Ashavel | Rare · T1 | Lifedrinker★ · Fiercebane · Bladesinger | 23I-1 Exsanguinate | 12 |
| Ivrael (Hand) | Rare · T1 | Metalline · Stalwart · Master Rune of Smiting | none | 4 |
| Teodric (Hand) | Rare · T1 | Sacred Burst · Metamagic Font · Ignore Target's Defense | 23E-7 Aerial Dash | 12 |
| Durgan (Hand) · light hammer | Rare · T1 | Thundering★ · Profane Burst · Distance | 23I-9 Blood Pact | 12 |
| Lorne (Hand) · split staff | Rare · T1 | Divine Wrath★ · Shadow Clone · Souldrinker | 23C-4 Enduring Ward | 11 |

**UDRP** = the kept rarity base + Greater 2 each + the new temper (1d4+1) and aspect (3d3+3) rolls + the kept masterwork and socket add-ons. **Rune rung by tier:** a T1 piece carries a Warhammer stacking rune at 3 runes. **Item CLs** are unchanged.

---

## 1. THE LAST COLUMN — Quavein Orlzynn
Heavy mace, flanged, hooked reverse beak · Legendary · T1 · CL 16
### D&D 3.5e
- **+2 mighty cleaving heavy mace** (masterwork 14, kept). 1d8+2.
- **Dimensional Pocket:** 250 lb of extradimensional space in the haft. The black book travels in it.
- **Mana Leech (Greater; parity ruling):** each hit recovers up to **5 spell levels** of expended slots (ER 3 → 5), at most once per round.
- **Warding:** **+4 deflection**. It replaces his ring's +3.
- **Second Wind:** 3/day, a swift action heals **5d8+16**.
- **Temper 23H-8 Vital Strike:** **+4d6** on a confirmed critical hit against a creature with anatomy.
- **Aspect 24E-5 Detonation:** when one of his damage-over-time spells ends (*acid fog*, *storm of vengeance*), it bursts in 10 ft for the damage it had left to deal.
- **Sockets (kept):** spell gems holding *destruction* and *heal*; seal Stalwart +4.
- Market: +3 bonus-equivalent, **18,312 gp**. **UDRP 31.**
### GURPS 4e
- Fine mace, +2 damage. Payload 125 lb.
- ER recovery 5 per hit. DR +4.
- Regeneration 5d+16, 3/day.
- Innate Attack 4d (critical vs living).
- Detonation: Explosion 1 when a Cyclic spell ends.
### Lore
An iron haft wrapped in raven-black cord. The flanged head is dull, and the beak's tip is the one bright point on the man. It was the bursar's mace of the minor house that raised him. When a rival bought the matron's death from a priestess, the house's last ledger was left open with its final column never totalled, and Quavein carried out the book and the mace together. **Complication:** every account he collects pays for his next spell, so the longer a fight runs the more he has to cast. The priestess who ended his house would know the mace on sight, and the column will not balance until her name does.

## 2. MINE TO CALL — Hadda Krell
A duelling hilt with no blade until she wants one · **Unique-grade** (authored on her rolled Legendary draws; Chad, 6 Oct 2026) · T1 · CL 17
*Replaces The Pointing Trowel. The rolled affixes, temper, aspect, masterwork result and sockets are kept and ride on the hilt. The base is now a permanent* black blade of disaster *(Spell Compendium p. 29), held rather than floating.*
### D&D 3.5e
- **The hilt:** blackened steel, a swept guard, Forgedeep guilloche along the lines of force, a sigil filed off the pommel. Empty, it passes any search as a sword with a broken blade.
- **The blade (Su):** as a free action she opens a **black blade-shaped planar rift**, a slot in the air where the light doesn't go, and closes it the same way.
	- **Melee touch attacks** at **base attack bonus + Int bonus** (as the spell) + Striking. Attack **+20/+15/+15/+15/+15 touch**. No weapon proficiency is needed; she directs it the way the spell's caster does.
	- **Damage:** **2d6+3 force**, plus **1d6 fire** (flaming burst runs down the rift's edge). Threat **18–20, ×2**; on a critical hit +1d10 fire.
	- Force: it hits incorporeal and ethereal creatures normally.
	- **It passes through magical barriers of 9th level or lower**: *wall of force*, *forcecage*, *globe of invulnerability*, her own Silk. It cannot enter an *antimagic field* or dead magic.
- **Disaster (her call).** On a confirmed critical hit she may **call it**. The target must make a **Fort save (DC 23)** or be **disintegrated**: **34d6** (2d6 per caster level, CL 17), and a creature reduced to 0 HP is dust. On a successful save it takes **5d6**. Spell resistance applies to the Disaster, at CL 17.
	- If she doesn't call it, the crit is a crit and nothing more: first blood, hers to call.
- **Striking:** **+4 enhancement** to attack. It replaces the hilt's +3 on attack rolls.
- **Souldrinking (Magic Item Compendium):** enervating. A critical hit gives a negative level, and against a living creature gives Hadda 5 temporary HP and +2 morale on melee damage for 10 minutes. It applies whether or not she calls Disaster.
- **Master Rune of Skalf Blackhammer (Warhammer):** her hits ignore the target's DR/X (touch attacks already ignore its armour and natural armour).
- **Morphing (Greater):** as a swift action the rift's length changes, from a stiletto's span to a sidesword's three feet. Knife range stays her range.
- **Temper 23H-5 Armor Shatter:** a critical hit still costs the target's armour **2d4 AC** until repaired. The rift doesn't care, but her allies do.
- **Aspect 24J-1 Inevitable:** she can't be surprised, flanked or denied her Dex bonus. She always acts in a surprise round and is immune to illusions below 7th level.
- **Sockets (kept), set in the hilt:** spell gem holding *forcecage*; rune **Fal** (+10 on Strength checks).
- **Stopping it:**
	- *Dimensional anchor* cast at the rift closes it and **seals the hilt for 1d4 rounds**.
	- *Dispel magic* (targeted) suppresses the hilt for 1d4 rounds, as for any magic item.
	- A rod of cancellation or a sphere of annihilation destroys the rift permanently; the hilt becomes steel.
	- It can't be harmed by physical attacks.
- Market: the rolled hilt (+9 bonus-equivalent) 162,302 gp, plus the rift (a 9th-level effect at CL 17, continuous: 306,000 gp). **≈ 468,302 gp.** Not for sale. **UDRP 36** (the rolled 31, +5 for an authored 9th-level built-in, as a capstone).
- **Hadda's feats:** Weapon Finesse is retrained to **Spell Penetration** (+2 on caster level checks against SR, which the Disaster needs). Her old punching dagger was never covered by a wizard's proficiencies; that hidden −4 is gone with it.
### GURPS 4e
- Innate Attack 2d+3 crushing (force; Affects Insubstantial; Armor Divisor (Ignores) against non-magical DR; Melee, Reach C–1), plus burning 1d Follow-Up. Uses Innate Attack (Beam) skill.
- Disaster: Follow-Up Innate Attack 34d corrosion (Accessibility: critical hit, user's choice; Resistible, HT-5); on a success, 5d.
- Penetrates magical barriers (Cosmic, ≤9th level). Disrupted by Dimensional Anchor and Dispel.
- Weapon Bond +4. Souldrinking: temp HP 5 and +1 damage. Armor Shatter: DR −2d4.
- Inevitable: Combat Reflexes, 360° Vision and Illusion resistance.
### Lore
The sea-wizard who bought her apprenticeship rented her to the Luskan pits as a girl and let his pit-mages carry no blades. He carried this. The rift was his work, a ninth-circle working laid permanently into a duelling hilt: the pit-master's last word, opened on anyone who forgot whose pit it was. When she had won enough purses to buy herself free, Hadda challenged him to a formal duel, with witnesses, and killed him inside the rules. The hilt was hers by right of the duel. A Forgedeep master in Waterdeep reworked the grip for a half-orc's hand, cut the guilloche along the lines of force and filed the sea-wizard's sigil off the pommel. She named it the first time someone asked her how her duels end: *"First blood. Mine to call."*
**Complication:** the Arcane Brotherhood of Luskan knows that hilt; one of their own made it, and they never accepted how he lost it. The master rune in the grip is dwarf work no one at Forgedeep will admit to striking. And Hadda has never lost a duel. Every fight she has won, she decided how it ended. If the hilt is ever taken from her, she will find out what she is without the choice.

## 3. PARRYING SCIMITARS OF RIPOSTE — Tarvash Oruk
Paired Calishite scimitars (one item) · Rare · T1 · CL 14
### D&D 3.5e
- **Masterwork scimitars**, a pair.
- **Parrying:** **+1 insight** to AC and saves while held, even when flat-footed. It doesn't stack across the pair.
- **Riposte:** **at will**, an immediate-action melee attack on a creature that has just missed him.
- **Shield Wall:** **+4 shield** bonus to AC. He carries no shield, so it applies.
- Market: Parrying (+2) on each blade, **16,630 gp**. **UDRP 3.**
### GURPS 4e
- Defense Bonus +1, +1 to resist.
- Counter Attack (free).
- DB +3.

*Rolled Rare: a mechanical name with no lore weight.* He comes down from the roof, and the man who swings back at him pays twice.

## 4. UNDYING PRAYER-CORD OF DRAGON SLAYING — Aerendyl Ostahr
Knotted cord with a bear's claw (garrotte) · Rare · T1 · CL 14
### D&D 3.5e
- **Masterwork garrotte cord.**
- **Weapon Mastery:** **+2** to confirm critical hits, and **+1 threat range**.
- **Master Rune of Dragon Slaying (Warhammer):** against dragons it is a bane weapon (+2 effective enhancement, +2d6). Every damaging hit adds a second roll of the weapon's damage dice.
- **Undying:** he automatically stabilises at −1 HP. Below 0 HP he has **DR 5/—**.
- **Temper 23H-2 Killing Blow:** **+1** to the critical multiplier.
- **Sockets (kept):**
	- Strange socket (Weave: 3/day, any spell of 3rd level or lower from any list).
	- *Regenerate* spell gem.
	- Charm: Dimensional Pocket, 100 lb.
- Market: +3 bonus-equivalent, **18,300 gp**. **UDRP 16.**
### GURPS 4e
- Weapon Master (limited).
- Bane 2d against dragons, with a second injury roll.
- Hard to Kill 4. Critical: +1 per die.

*Rolled Rare.* A monk's cord that wants to strangle a dragon. He hasn't met one yet.

## 5. INSIDE TEN — Kesh Durrow
Mantis-sickles, reversed (one item, a pair) · Legendary · T1 · CL 15
### D&D 3.5e
- **+3 shocking burst sickles** (masterwork 17, kept). Each 1d6+3 plus 1d6 electricity.
- **Rune of Cleaving (Warhammer, 3 runes, Greater):**
	- Each hit ignores **3 points of DR** (base 2).
	- **+2 Strength** (untyped) while wielded.
	- **Killing Blow:** threat range +1 step, and a confirmed natural 20 against a creature of his size or smaller forces a **Lethal** location result.
- **Mind Fog:** on a hit, 1/encounter: **−6 on the target's next save**, Will DC 24.
- **Deflecting:** 1/round, deflect one ranged attack (Reflex DC 25).
- **Animal Bond:** **+5** on Handle Animal and wild empathy, for his ranger companion.
- **Temper 23E-3 Shadowstep:** 1/encounter, teleport behind the target. +4 on the next attack.
- **Aspect 24J-5 Cataclysm:** 1/day, for 1 round:
	- maximum damage;
	- +5 to his DCs;
	- an extra standard action;
	- then he is exhausted for 1d4 rounds.
- Market: +8 bonus-equivalent, 128,006 each, **256,012 gp**. **UDRP 34.**
### GURPS 4e
- Fine sickles, +2 damage, burning (electrical) 1d.
- Armor Divisor (2), ST +1, and the Lethal critical result.
- Affliction (−6 to resist). Enhanced Parry (Missile) 2.
- Warp (behind the target). Cataclysm: 1/day maximum dice and an Extra Attack.
### Lore
The old Luskan bosun who taught a one-eyed dock rat to shoot carried these for the moments the bow was too slow, reversed along his forearms because a man in the rigging needs his hands. Kesh stole them before the gravedigger could, and paid the Forgedeep smiths extra to leave the bosun's grind alone. **Complication:** the dockmaster who burned his eye stands inside ten paces of Kesh once a year. The sickles were made for exactly that distance, and Cataclysm makes it one round.

## 6. BETWEEN THE JOINTS — Marit Hollowell
Boning knife, crescent-worn, beech handle · Legendary · T1 · CL 16
### D&D 3.5e
- **+1 dagger** (masterwork 5, kept). 1d4+1, 19–20.
- **Radiant:** **+3d6 positive energy**. Undead take ×1.5.
- **Freeze Target (Diablo II):** d100 on each damaging hit; 01–10 fires.
	- The target makes Fort DC 14 or is held (frozen) for 1d2 rounds.
	- On a success, it is chilled instead.
- **Stoneskin:** physical damage she takes is reduced by **5** per hit, after DR.
- **Spider's Gift:** *spider climb* and *freedom of movement* at will.
- **Temper 23A-4 Precise Thrust:** **+4** against medium or heavy armour.
- **Aspect 24G-6 Coiled Spring:** an extra move action in round 1, and **+4 initiative**.
- **Socket (kept):** shard, Huge earth elemental 1/day.
- Market: +3 bonus-equivalent, **18,302 gp**. **UDRP 25.**
### GURPS 4e
- Fine knife, +1 damage. Burning (holy) 3d Follow-Up.
- Freeze: an HT contest, or Immobilized.
- DR +5 (physical only). Clinging, plus *freedom of movement*.
- Enhanced Time Sense and Extra Move in round 1.
### Lore
Her husband boned salt pork on the Waterdeep provisioning docks and taught her that a good knife finds the space between the joints. Four men killed him over a cargo. Marit took the knife off his bench and used it four times. **Complication:** with Spider's Gift and the earth elemental, no wall, roof or cellar floor stops her following a quarry. The name in her file, the one who paid for the cargo, lives behind the Veil's own walls.

## 7. THE HINGE-PINS — Brunna Coldhollow
The tucks: square needle estocs, Coldhollow mark (one item, a pair) · Legendary · T1 · CL 16
### D&D 3.5e
- **+3 icy burst estocs (rapier stats)** (masterwork 20, kept). Each 1d6+3 plus 1d6 cold, 18–20.
- **Rune of Striking (Warhammer, 3 runes):**
	- **+4** to attack. It doesn't stack with the +3 enhancement, so the net is +1.
	- Once per round she may reroll one missed attack.
- **Ghost Strike (Magic Item Compendium):** ghost touch. Sneak attacks and critical hits work against undead as if they were living.
- **Blinding (Greater):** on a critical hit, blinded for 1 round, Fort **DC 27**.
- **Endurance (Greater by capstone):** **+12** against fatigue and forced march. Very Fit; doesn't sleep.
- **Temper 23C-3 Parrying Grace:** **+4 AC** while fighting defensively.
- **Aspect 24G-5 Horizon:** 1/encounter, teleport to any space she can see within **500 ft**.
- Market: +9 bonus-equivalent per blade, **324,640 gp**. **UDRP 38.**
### GURPS 4e
- Fine estocs, +2 damage, burning (cold) 1d.
- Weapon Bond +4, with a reroll per second. Affects Insubstantial.
- Affliction (Blindness, HT −2 at Greater). Very Fit, Doesn't Sleep.
- Warp 167 yd, 1/encounter.
### Lore
When Coldhollow fell, the rescuers brought up a girl beside her mother's body and the great door's hinge-pins. At the forge-school she drew the pins into two square needles and struck the clan mark on each. **Complication:** to hang Coldhollow's doors again she would have to give up the swords. The prisoner she keeps alive has seen them, and knows what they are.

## 8. THE TEACHER'S HIDE — Zaheda Qorrin
Notebook in a tiger-hide cover; reed pen · Legendary · T1 · CL 16 · wondrous
### D&D 3.5e
Masterwork 20 under table 21C (kept): +2 to every affix value, and the capstone. The book is not a weapon, so no weapon properties were drawn.
- **Battle Trance (Greater):** after 3 consecutive rounds of combat, **+7 morale** to attack and damage (base +3; Greater +5; masterwork +2).
- **Absorption:** at will, convert one incoming **fire** attack into healing, up to **52**.
- **Undead Servitor (Greater by capstone):** raise one corpse as a skeleton or zombie of up to **20 HD** for 24 hours (base 12; Greater 18; masterwork +2).
- **Chameleon (Greater):** at will, the book looks like any book: a prayer book, a ledger, a child's primer.
	- *Detect magic* and *identify* see only the disguise.
	- *True seeing* sees through it only on a caster level check against DC 27.
- **Temper 23D-8 Sacrifice Pool (parity ruling):** a willing ally may give HP for her slots, 5 HP per spell level.
- **Aspect 24F-6 Pack:** when 3 or more of her summoned creatures attack the same target, each gains **+2 to attack and +1d6 damage**.
- **Tiger form (ruled):** the notebook melds into the tiger and **its powers stay active**. That overrides the RAW rule that melded items stop working; the cover is the tiger's own hide.
- Market: no SRD enhancement; **UDRP 37.**
### GURPS 4e
- Gadget, held. Berserk (controlled, after 3 turns) +5.
- Absorption (fire). Ally (raised, 20 HD).
- Morph (cosmetic), plus resistance to detection.
- Sacrifice Pool: an ally's HP for her ER. Pack: Ally Group bonus.
### Lore
The pasha's tiger she let go came back to her years later, old and grey at the muzzle, and lay down at the edge of her camp to die. The cover is its hide, and the reed pen is cut from the bed it died in. **Complication:** the book can pass for any book now, so a captured notebook is harder to find, and only her cipher protects it once found. It also raises the dead. Her exiled circle would call that proof she is lost, and Nym would call it theft.

## 9. AEGIS BASTARD SWORD OF COMMAND — Ysmay Corran
The old sword · Rare · T1 · CL 13
### D&D 3.5e
- **Masterwork bastard sword.**
- **Aegis:** **+5 insight** to AC against attacks of opportunity.
- **Commander's Voice:** **+5** to her leadership score and rally checks.
- **Linguist:** *comprehend languages* and *tongues* at will; telepathy 30 ft.
- **Temper 23E-7 Aerial Dash:** 1/encounter, fly **100 ft** in a straight line, with no hover. The owl's drop.
- Market **335 gp**. **UDRP 8.**
### GURPS 4e
- DB +5 (opportunity attacks only). Leadership +5.
- Language Talent 4, Telepathy. Flight 1/encounter (straight line).

*Rolled Rare.* **The Undeath Covenant is gone with the first pass.** Ysmay heals normally again, and every pairing and release line that leaned on it is corrected.

## 10. LETHAL SHORTSPEAR OF SWEEPING — Dace Tolland
Short spear, red-lacquered socket · Rare · T1 · CL 15
### D&D 3.5e
- **Masterwork shortspear.**
- **Lethal Focus:** **+4d6** on a confirmed critical hit.
- **Sweeping (Magic Item Compendium):** **+2** on Strength checks to trip with the spear.
- **Life Shield:** 1/encounter, when he takes damage, gain **25 temporary HP**.
- **Socket (kept):** strange, Coiled Spring (+4 initiative, an extra move action in round 1).
- Market: Sweeping (+1), **2,301 gp**. **UDRP 9.**
### GURPS 4e
- Crushing Attack 4d (critical only). +2 on the Trip contest.
- Regeneration (1/combat, 4d over 3 turns).

## 11. MOURNERS' BRASS — Osmund Tarrow
Brass censer on a chain (light flail) · Legendary · T2 · CL 15
### D&D 3.5e (T2 column)
- **+1 ghost touch light flail** (masterwork 9, kept). 1d8+1; it smokes on a hit.
- **Penetrating Strikes:** his attacks count as **adamantine**.
- **Shadowtouch:** **+2d6 negative energy**. Undead take half.
- **Leech:** each hit heals him **3 HP**.
- **Chance to Cast on Attack (Diablo II):** d100 on each attack roll, hit or miss; 01–10 casts ***silence*** (chosen at creation; CL 5), centred on the target.
- **Temper 23C-2 Reactive Armor:** when he takes a critical hit, he gets **DR 8** against it after the fact.
- **Aspect 24A-3 Tempest:** all physical damage the censer deals is **lightning**. 25% of the time it arcs to an adjacent creature.
- Market: +4 bonus-equivalent, **32,308 gp**. **UDRP 24.**
### GURPS 4e
- Fine flail, +1 damage, Affects Insubstantial.
- Toxic 2d (cosmic) Follow-Up. Vampiric 2.
- Affliction (Mute) on the proc. DR 8 (critical hits only).
- Tempest: damage becomes burning (lightning), with an arc.
### Lore
For years this censer swung over the common pits at the Neverwinter paupers' burials, where nobody paid a priest. Three old women gave it to Osmund when the last of them died. **Complication:** the censer now strikes like the Storm King's weather. If the empire's priests of the Judge see a funeral censer throwing lightning out of a Veil operation, that's a political event. And it drinks from whatever it hits.

## 12. STORMBORN HANDAXE OF TRACKLESS PASSAGE — Wenna Sorrel
Short hatchet · Rare · T1 · CL 16
### D&D 3.5e
- **Masterwork handaxe.**
- **Stormborn:** **+2d6** on a hit, split sonic and lightning.
- **Trackless:** **+20 competence** to Hide and Move Silently.
- **Pack Mule (Greater):** carrying capacity **×4**.
- **Temper 23A-7 Lunging Reach:** **+10 ft reach** on her first attack each turn.
- Market **306 gp**. **UDRP 8.**
### GURPS 4e
- Innate Attack (sonic + lightning) 2d Follow-Up. Stealth +8.
- Lifting ST +8. +1 Reach on the first attack.

## 13. THE WRONG NOTE — Faelith Ammarin
Darkwood tower shield edged in iron, used to hit people · Legendary · T1 · CL 14
### D&D 3.5e
- **+2 bashing darkwood tower shield** (masterwork 13, kept). Shield AC +6. Bash 2d6, with the bashing property's +1.
- **Rune of Fire (Warhammer, 3 runes, Greater):**
	- Each bash deals **+1d6 fire**.
	- 1/encounter, a **15-ft cone of 5d6 fire** (base 3d6), Reflex DC 14 half; a burned target takes 1d6 more at the start of its next turn.
- **Thorns (Greater):** melee attackers take **5d6** (base 3d6).
- **Banefire:** **+5d6** against creatures of the **fire** subtype (chosen at creation).
- **Battle Meditation:** 1/encounter, reroll one attack roll. (This was rerolled from Signature Move: a fighter has no save-DC class ability.)
- **Temper 23H-4 Hemorrhage:** a critical bash makes the target bleed **2d4 a round** for 3 rounds.
- **Aspect 24G-4 Wind:** **+20 ft speed**, and immunity to attacks of opportunity from movement. Not in heavy armour. **Open:** the Stalker suit's armour category isn't ruled; the Strider counts as light.
- Market: the shield (+3 armour bonus-equivalent) plus Rune of Fire on the bash (+3), **27,480 gp**. **UDRP 28.**
### GURPS 4e
- Shield DB +3 and DR +2. Burning 1d on a bash. Cone 5d, 1/encounter.
- Damage Aura 5d (melee). Bane 5d (fire).
- Luck (1/encounter, attack). Toxic (bleed) on a critical.
- Enhanced Move +20 ft, with movement AoO immunity.
### Lore
The shield comes from an elven border company that sang its wall into line. The bearer before Faelith sang it wrong and loud on the morning the wall broke, and his was the only stretch that held. **Complication:** with fire and thorns on it, nobody wants to touch her stretch of the wall, and the company's survivors want the shield back for their own.

## 14. ANARCHIC DIRE FLAIL OF THE DEATH RUNE — Patience Haskett
Two-headed heavy flail · Rare · T1 · CL 14
### D&D 3.5e
- **Masterwork dire flail.**
- **Anarchic (Greater):** chaos-aligned, so it bypasses DR/chaotic. Each damaging hit on a lawful creature deals **+3d6** (base 2d6). A **lawful wielder** gains a negative level while holding it. **Open:** Patience's alignment isn't set.
- **Master Rune of Death (Warhammer):** a confirmed natural 20 forces a **Lethal** location result, against a target of any size. It is not a death effect, and there is no save.
- **Thrift:** **50%** chance that a daily-use ability isn't spent. That includes his release, *Thrice*.
- Market: +5 bonus-equivalent, **50,690 gp**. **UDRP 5.**
### GURPS 4e
- Innate Attack 3d (vs lawful targets). The Lethal critical result.
- Luck (daily abilities only).

## 15. THE RELIEF — Rhun Talbridge
Pollaxe (halberd) · Legendary · T1 · CL 13
### D&D 3.5e
- **Masterwork halberd** (masterwork 1, kept: +1 on trip attempts). 1d10, ×3.
- **Prismatic (Greater):** each hit adds **3d8 of a random energy type** (base 2d8).
- **Temper 23B-6 Elemental Confluence:** a second random energy type also strikes, at half dice.
- **Prismatic Burst (Magic Item Compendium):** a critical hit subjects the target to ***prismatic spray*** (DC 20), even if it's immune to critical hits.
- **Vicious:** each hit deals **+2d6** to the target and **1d6 to Rhun**.
- **Vampiric:** **+1d6** against living targets, and he heals that amount.
- **Aspect 24B-5 Flanker:** **+5d6 precision** damage when flanking.
- **Socket (kept):** strange, Revenant.
- Market: Vicious and Vampiric (+3 bonus-equivalent) plus Prismatic Burst (30,000 flat), **48,310 gp**. **UDRP 35.**
### GURPS 4e
- Variable Innate Attack 3d, plus a second at half.
- Prismatic table on a critical (effects open in the compendium).
- 2d to the target and 1d back to him. Vampiric 1d.
- Backstab-style +5d when flanking. Unkillable 2 (Revenant).
### Lore
An Amnian city-watch pollaxe that passed to whoever relieved the post: fourteen brass bands, and Rhun's is the last. **Complication:** the pollaxe bites its own bearer on every hit, and his Revenant socket won't let him die properly. The Veil's priests have started to notice Division XI.

## 16. COMPLINE — Edwyn Coldry
Mail mitten over a spell-burned hand (spiked gauntlet) · Legendary · T1 · CL 13
### D&D 3.5e
- **+1 defending spiked gauntlet** (masterwork 12, kept). 1d4+1.
- **Holy (Greater):** good-aligned, so it bypasses DR/good. **+3d6** against evil creatures (base 2d6). An evil wielder gains a negative level.
- **Flaming Burst:** **+1d6 fire**; on a critical hit, +1d10 fire.
- **Fleshgrinding (Greater):** when he deals damage to a living creature in melee, he may let go. The mitten animates and grinds into the foe, dealing a normal hit automatically at the start of his turn for **8 rounds** (base 5), until it's pulled free.
- **Nimble:** the Max Dex of his armour rises by **+4**.
- **Temper 23I-6 Shadow Meld:** **+15 Hide** in dim light or darkness, with concealment. (This was rerolled from Chain Lightning: there's no lightning on the glove.)
- **Aspect 24G-2 Tidal Surge:** when he moves 20 ft or more in a straight line, adjacent enemies take **1d6 + Str** and must make a Reflex save or fall prone.
- Market: +8 bonus-equivalent, **128,305 gp**. **UDRP 27.**
### GURPS 4e
- Fine gauntlet, +1 damage. Holy 3d (vs evil). Burning 1d, with a critical rider.
- Cyclic attack, 8 turns (Fleshgrinding). Reduce armour DX penalty by 4.
- Stealth +6 in darkness. Slam on a straight-line move.
### Lore
The mitten was a relic-glove of the order he left, laid on the altar at compline, the last hymn before sleep. **Complication:** the glove is still *holy*. The faith he walked out of hasn't let go of its relic, and when he lets go of it, the glove keeps working on its own. (The faith is left open for Chad.)

## 17. FIERCEBANE WAR-FANS OF LIFEDRINKING — Ashavel Oriym
Iron war-fans (one item, a pair) · Rare · T1 · CL 14
### D&D 3.5e
- **Masterwork war-fans** (dagger stats).
- **Bladesinger:** **+3 dodge** to AC while wielding them.
- **Lifedrinker (Greater):** a kill heals her **38 HP** (base 25).
- **Fiercebane (Magic Item Compendium):** bane against a creature type chosen at attunement: **humanoid (human)**, the Veil's commonest target.
	- The fans glow when such a foe comes within 60 ft, even unseen.
	- On a critical hit, +1d10.
- **Temper 23I-1 Exsanguinate:** each hit on a living creature causes **1d8 bleed a round** for 3 rounds.
- **Socket (kept):** shard, Huge air elemental 1/day.
- Market: Fiercebane (+1) on each fan, **4,604 gp**. **UDRP 12.**
### GURPS 4e
- Enhanced Parry 3. Regeneration on a kill (4d+).
- Bane (humans), with Detect within 20 yd. Toxic (bleed) 1d.

---

# THE HAND (four rolled pieces; Yashiori, a Unique, is unchanged)

## H1. METALLINE LONGBLADE OF SMITING — Ivrael Quillatar
Elven single-edged longblade (bastard sword stats) · Rare · T1 · CL 15 · *replaces today's earlier reroll*
### D&D 3.5e
- **Masterwork elven longblade.** 1d10, 19–20, slashing.
- **Master Rune of Smiting (Warhammer):** every damaging hit adds a **second roll of the weapon's damage dice** (dice only, not multiplied on a critical hit).
- **Metalline (Magic Item Compendium):** as a standard action, the blade becomes **adamantine, alchemical silver, cold iron or steel**.
- **Stalwart:** **+4 resistance** to all saves.
- **Socket (kept):** charm, Skillmaster +5 Spot, Search and Listen.
- Market: +5 bonus-equivalent, **50,335 gp**. **UDRP 4.**
### GURPS 4e
- A second injury roll per hit. Material switch (Armor Divisor (2) against the matching DR).
- Will +4, HT +3.

## H2. SACRED BURST BASTARD SWORD OF IGNORED DEFENSE — Teodric Halvane
Elven bastard sword, two-handed · Rare · T1 · CL 14
### D&D 3.5e
- **Masterwork bastard sword.**
- **Ignore Target's Defense (Diablo II):** his attacks against creatures **under 17 HD** resolve as touch attacks: armour, shield and natural armour are ignored.
- **Sacred Burst (Magic Item Compendium):** on a critical hit, **+1d10 positive energy** (×2), or 2d10 against an evil outsider.
- **Metamagic Font:** 3/day, apply one metamagic feat to a spell without raising its level.
- **Temper 23E-7 Aerial Dash:** 1/encounter, fly 100 ft in a straight line.
- **Sockets (kept):** Topaz (3d6 retaliation) and Skull (8 HP per hit).
- Market: +4 bonus-equivalent, **32,335 gp**. **UDRP 12.**
### GURPS 4e
- Defender's Parry, Block and Dodge at −3 (Tier 2 and below).
- Burning (holy) on a critical. Modular metamagic, 3/day.

## H3. THUNDERING LIGHT HAMMER OF DISTANCE — Durgan Emberlode
The short hammer he never seems to use · Rare · T1 · CL 14 · *rebased 6 Oct 2026 from a heavy crossbow to his kit (Chad: Claude's call)*
### D&D 3.5e
- **Masterwork light hammer.** 1d4, ×2, bludgeoning; thrown, range increment 20 ft.
- **Distance:** thrown range increment **40 ft**, double. (Ruling: a thrown weapon counts as a ranged weapon for Distance.)
- **Thundering (Greater):** on a critical hit, **+1d10 sonic** (base 1d8 at ×2), and the target is **deafened** permanently unless it makes Fort **DC 16** (base 14).
- **Profane Burst (Magic Item Compendium):** negative energy on a hit while active; on a critical hit, +1d10 (2d10 against good outsiders). Each burst costs Durgan **1d4 Con**.
- **Temper 23I-9 Blood Pact:** 1/day, spend 25% of his maximum HP to **double one spell's or attack's damage**. A doubled *delayed blast fireball* is the point. (Rerolled twice: Whirlwind and Momentum Crit were rolled against the crossbow; neither suits a sorcerer's hammer either, so the reroll stands.)
- Market: +3 bonus-equivalent, **18,301 gp**. **UDRP 12.**
### GURPS 4e
- Fine throwing hammer; range ×2. Crushing (sonic) critical rider, plus Deafness.
- Toxic (cosmic) critical rider, which costs HT. Damage ×2 (HP cost), 1/day.

*Why the hammer.* His kit was authored with a short hammer he never seems to use. Now when he does use it, it thunders: a sorcerer's last-ditch weapon that deafens the casters it touches. The crossbow is gone.

## H4. STAFF OF DIVINE WRATH — Lorne Ashby
The staff that splits into two short rods · Rare · T1 · CL 13 · *rebased 6 Oct 2026 from a longsword to his kit (Chad: Claude's call)*
### D&D 3.5e
- **Masterwork quarterstaff** (double weapon, 1d6/1d6). It splits into **two short rods** (light clubs, 1d6 each) as a move action and locks back together the same way. The properties sit on the **head rod**; the tail rod is masterwork only.
- **Divine Wrath (Greater):** as a swift action, spend a turn-undead attempt. If his next hit lands on an undead creature, it deals **+1d8 per point of Charisma bonus** (base 1d6).
- **Shadow Clone:** at will, a shadow duplicate of himself with **50%** of his statistics. Split, each of them holds a rod.
- **Souldrinker (parity ruling):** a kill recovers up to **6 spell levels** of expended slots, once per round.
- **Temper 23C-4 Enduring Ward:** **+4 SR**.
- **Sockets (kept):** Topaz and two Amethyst (+50 HP), set in the head rod.
- Market: +1 bonus-equivalent on one end, **2,600 gp**. **UDRP 11.**
### GURPS 4e
- Fine quarterstaff / paired batons. Holy Innate Attack against undead. Duplication (50%).
- ER 6 on a kill. Magic Resistance +4.

*The staff puts the dead down.* Lorne still raises with his spells; the head rod ends anyone else's dead, and his shadow takes the other rod. It is the staff from Tethford, the man who stepped out of a two-foot rock's shadow. His hand crossbow stays unmagicked kit.

---

## Stat-block errata (supersede the round-5 errata)
The masterwork-driven attack lines from round 5 stand: Quavein +22, Hadda +19, Kesh +28, Marit +23, Brunna +20, Osmund +15, Rhun +23 (1d10+15), Edwyn +10, Faelith bash +23. Changes:

| Bearer | Changed lines |
|---|---|
| Quavein | **AC 31, touch 20, flat-footed 29** (Warding). Second Wind 3/day. Mana Leech: 5 spell levels per hit. |
| Hadda | Attack **+20/+15/+15/+15/+15 touch** with the rift (BAB + Int + Striking), 2d6+3 force + 1d6 fire, 18–20; Disaster on a called crit (Fort DC 23, 34d6). Weapon Finesse → Spell Penetration. DR back to 8/magic. **Spell DC back to 18 + level, evocation 20 + level.** Can't be flanked or surprised. |
| Tarvash | AC **+5** (Parrying +1 insight, Shield Wall +4); saves +1. Riposte at will. Initiative back to +14. |
| Aerendyl | Unarmed damage back to 2d8. Stunning Fist back to 16/day. Threat range +1; critical multiplier +1. DR 5/— below 0 HP. |
| Kesh | Damage **1d6+9** (Rune of Cleaving +2 Str). No longer immune to critical hits; swim speed gone. |
| Marit | Damage back to normal (no force). Physical damage −5 per hit. Initiative **+17**; extra move in round 1. Spider climb and *freedom of movement* at will. |
| Brunna | Attack **+21/+16/+11** (Rune of Striking +4). **No flight.** Teleport 500 ft, 1/encounter. |
| Zaheda | Speed back to 60 ft. +7 to attack and damage after 3 rounds. Raises one corpse (20 HD). |
| Ysmay | **Heals normally** (Covenant gone). +5 AC vs attacks of opportunity. Flies 100 ft, 1/encounter. |
| Dace | 25 temporary HP, 1/encounter. Coiled Spring (+4 initiative) stays (socket). No Phasewalk or Terrifying. |
| Osmund | **Divine DC back to 17 + level.** Hits count as adamantine and deal lightning damage. |
| Wenna | +2d6 sonic/lightning per hit. Rapid Assault gone. |
| Faelith | Shield AC +6 stays. Bash +1d6 fire. Thorns 5d6. Speed +20 ft (if the suit isn't heavy). |
| Patience | +3d6 against lawful creatures. Lethal critical result. |
| Rhun | +3d8 random energy, plus a half-dice second energy. Vicious costs him 1d6 per hit. |
| Edwyn | **AC back to 24, touch 15, flat-footed 24** (Shield Wall gone). +3d6 against evil creatures, plus fire. |
| Ashavel | AC **+3 dodge** (Bladesinger). Heals 38 per kill. |
| Ivrael | +4 to all saves. Damage dice rolled twice. |
| Teodric | Touch attacks against creatures under 17 HD. |
| Durgan | Thrown light hammer, range increment 40 ft. Profane Burst costs him 1d4 Con. |
| Lorne | Staff 1d6/1d6 or two rods. SR +4 (Stalker suit SR 10 → 14). Shadow clone. |

---

## Rulings (Chad, 6 Oct 2026: "your choice")
- **Patience Haskett is chaotic neutral.** A tiefling who whirls a flail at whatever is in front of him and keeps no code. The Anarchic flail sits with him cleanly: no negative level.
- **The Stalker suit is medium armour** for every armour-category test. The Strider stays light. Faelith's Wind aspect works in her Stalker suit; Edwyn's Nimble raises its Max Dex.
- **Edwyn Coldry is lawful neutral.** He kept the order's discipline and lost its faith. The Holy mitten works for him without penalty, and it still burns evil for a god he no longer prays to.
- **Bases follow the kit.** Durgan's piece is his short hammer, and Lorne's is his splitting staff (cards H3 and H4, rebased). Teodric's sword stays; his kit has no weapon to move it onto.

## Rulings (Chad, 6 Oct 2026: "take these leans")
- **Socket fills confirmed** as proposed in round five: Quavein's seal Stalwart +4, Naevys's seal Aegis +5, Aerendyl's charm Dimensional Pocket 100 lb, the strange sockets (Aerendyl Weave, Dace Coiled Spring, Rhun Revenant), and the shards (Marit earth, Ashavel air).
- **Zaheda's notebook works in tiger form.** It melds and stays active, as a campaign override of the RAW rule that melded items stop working. Battle Trance, Absorption, the raised servitor, Chameleon, Sacrifice Pool and Pack all carry into the tiger.
- **The companion-draw rule is moot.** After the full-corpus pass no piece carries a companion- or minion-keyed draw without a companion: Kesh's Animal Bond has his animal companion, and Zaheda's Pack has her summons. The round-five division rule (such a draw applies to one sworn operative of the bearer's division) stays on file, unruled, in case a later roll needs it.

## Ruling (Chad, 6 Oct 2026): Hadda's weapon
Hadda's piece must be a real weapon. **The Pointing Trowel is retired.** Her signature piece is now ***Mine to Call***: the sea-wizard's duelling hilt holding a permanent *black blade of disaster* (Spell Compendium p. 29), with her rolled Legendary draws riding on the hilt (card 2). It is authored, Unique-grade, and pairs with Kerra's *Not Mine*. Disaster fires only on a confirmed critical hit she chooses to call.
