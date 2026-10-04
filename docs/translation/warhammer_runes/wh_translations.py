"""Translations for the Warhammer Fantasy Dwarf weapon-rune corpus. Rate card = Crusader (Affix Registry section 2); rules = ../FUSED_ENGINE_RESOLUTION.md.
Special-rule mapping from corpus-mass-translator references/wargame-profile-conversion.md (Killing Blow, Frenzy, Fear/Terror, Always Strikes First by analogy).

CONVENTIONS:
- Multiple copies of a rune (1/2/3 runes) = Crusader's three rungs: 1 rune = Magic (+1, 2,000 gp), 2 = Rare (+2, 8,000 gp), 3 = Unique (+3, 18,000 gp); a two-rung rune uses the top two rungs it names.
  Master runes are single-rung: +3 (40 points), +2 (25 to 30 points), +1 (15 to 20 points), adjusted by effect where the 3.5e comparable (Throwing + Returning, Brilliant Energy) prices differently.
- To Hit / To Wound / Armour Save have no 3.5e equivalents: +1 WS = +1 attack per rung (Striking row), +1 S = +2 Strength (untyped), armour-save modifiers = ignored DR (Armor Piercing row), Multiple Wounds (N) = extra weapon-damage rolls on a hit.
- Killing Blow = threat range +1 step and a confirmed natural 20 against a same-size or smaller target forces a Lethal-severity location result on the crit table (the engine's Vorpal ruling); Heroic Killing Blow has no size limit.
- Rule of Three, Rule of Form, Rule of Pride and Jealous Runes carry over as written (one master rune per item and per army).
- GURPS chassis: Gadget on the weapon, no point total, dice as-is; healing and bleeds follow the Registry conventions.
"""
T = {}
def c(base, note): return dict(verdict="COVERED", base=base, note=note)
LAD = "+1 / +2 / +3 = 2,000 / 8,000 / 18,000 gp by rune count (Magic / Rare / Unique)"
def e(verdict, base, bonus, three_e, gurps, collision="none.", forks="none.", price=None):
    d = dict(verdict=verdict, base=base, bonus=bonus, three_e=three_e, gurps=gurps, collision=collision, forks=forks, note="")
    if price: d["price"] = price
    return d

T["Rune of Parrying"] = c("Warding (Defensive 01-06)", "-1 to enemy To Hit in close combat is a +1 deflection bonus to AC against melee, Warding's T5/T4 value. No new family.")
T["Rune of Speed"] = c("Predator's Instinct (Offensive 73-78)", "+1 Initiative per rune is Predator's Instinct's initiative bonus (+1/+2/+2/+3/+4); stacking per rune matches the row's rungs.")

T["Master Rune of Alaric the Mad"] = e("DELTA", "Brilliant Energy (DMG, weapon-affix corpus) / Armor Piercing (Offensive 19-24)", 3,
 "The weapon's attacks ignore armor and shield bonuses to AC (including enhancement bonuses to that armor) and ignore worn DR (the engine's ignores-armor flag). Natural armor, Dex, dodge and deflection still apply. Unlike Brilliant Energy it harms undead, constructs and objects normally. Always on. Master rune: one per item and per army.",
 "The weapon's attacks skip worn DR (ignores_armor flag); the defender's 3d6 active defenses are unchanged.",
 collision="DMG Brilliant Energy (+4, also passes through nonliving matter); different reach, names stay.",
 forks="1. 'Ignores Armour Saves' is read as ignore armor and shield AC plus worn DR; natural toughness stays.")
T["Master Rune of Death"] = e("DELTA", "Vorpal (DMG, weapon-affix corpus ruling)", 3,
 "Heroic Killing Blow: on a confirmed natural 20 the engine forces a Lethal-severity result on the location table (the same table as the Vorpal ruling), against a target of any size. Not a death effect and no separate save. Master rune.",
 "On a confirmed critical hit, the same Lethal-severity location result; no size limit.",
 forks="1. Vorpal forces the Head; this rune forces Lethal severity on the rolled location (less reliable, reflecting the lower cost), per the engine's crit table.")
T["Master Rune of Dragon Slaying"] = e("DELTA", "Bane (DMG, weapon-affix corpus)", 3,
 "Against creatures of the dragon type (including drakes and wyrms): the weapon acts as a bane weapon (+2 effective enhancement bonus and +2d6 damage) and every damaging hit adds one extra roll of the weapon's damage dice (Multiple Wounds (2)). Master rune.",
 "Innate Attack (Bane) 2d Follow-Up against dragons, and the injury is doubled (a second damage roll).",
 collision="DMG Bane and WoW Demonslaying (type-slaying family); names stay.",
 forks="1. 'Always wounds on a 2+' has no 3.5e roll; it is carried by the bane attack bonus.")
T["Master Rune of Smiting"] = e("NEW", "none", 3,
 "Multiple Wounds (D6): every damaging hit adds one extra roll of the weapon's damage dice (dice only: no Strength, no extra dice, not multiplied on a critical hit). Master rune.",
 "Each damaging hit's injury is rolled twice (the second roll the weapon dice only).",
 forks="1. Multiple Wounds (D6) averages 3.5 wounds on the tabletop; one extra damage roll is the 3.5e reading because 3.5e damage already scales with dice. A GM wanting more can step this to 1d3 extra rolls at a higher price.")
T["Master Rune of Skalf Blackhammer"] = e("NEW", "none", 2,
 "The weapon ignores the target's DR/X and natural armor bonus unless the target wears magic armor; against a target in magic armor it ignores DR/X only. Master rune.",
 "The weapon's attacks ignore natural DR (and worn DR on a target in nonmagical armor); against magic armor, ignore natural DR only.",
 forks="1. 'Wound on 2+ regardless of Toughness' is read as ignoring DR/X and natural armor.")
T["Master Rune of Breaking"] = e("NEW", "none", 2,
 "On a damaging hit against a creature wielding a magic weapon, that weapon must succeed on a Fortitude save (the owner's save bonus, DC 20) or be destroyed; one check per round. A creature with several magic weapons risks one at random. Artifacts are immune. A creature whose weapon is destroyed is armed with an ordinary weapon of the same kind. Master rune.",
 "On the same hit: Quick Contest of the weapon owner's HT against effective skill 20; on failure the weapon breaks.",
 collision="Sunder (a combat maneuver) and MIC Sundering (extra damage on sunder): different, names stay.",
 forks="1. 'D6 roll of 2+' (about 83%) is replaced by a DC 20 save so a well-built weapon can resist. 2. Default applies to NPC weapons; whether it can break a PC's magic weapon is a GM call (default: yes, with the save).")
T["Master Rune of Snorri Spangelhelm"] = e("NEW", "none", 2,
 "The weapon's attack rolls hit on any natural 2 or higher (a natural 1 still misses); a hit is a critical threat only if the roll is within the threat range. Master rune.",
 "The weapon's effective skill is never below 16 for attack rolls; the defender still rolls any active defense.",
 forks="1. 'Hits on 2+' is read as removing AC as an obstacle but keeping the natural-1 miss.")
T["Master Rune of Swiftness"] = e("NEW", "none", 2,
 "Always Strikes First: in melee the wielder's attacks resolve before any opposing melee attack in every round regardless of initiative order, and he wins ties. Master rune.",
 "The wielder's attacks resolve before any opposing attack in the same second.",
 forks="1. 'Always Strikes First' is a miniatures initiative override; here it is resolution order inside the round, not an initiative bonus.")
T["Master Rune of Banishment"] = e("DELTA", "Ghost Touch (DMG, weapon-affix corpus)", 1,
 "The weapon functions as ghost touch, and against undead and incorporeal creatures the wielder may once per round reroll one damage roll and keep the better. Master rune.",
 "Affects Insubstantial on all attacks; against undead, one damage reroll per second-turn, take the better.",
 forks="1. 'Re-roll failed To Wound' is read as a damage reroll.")
T["Master Rune of Flight"] = e("DELTA", "Throwing + Returning (DMG, weapon-affix corpus)", 2,
 "The weapon can be thrown with a 20-ft range increment, hits on any natural 2 or higher, and returns to the wielder's hand (Throwing +1 and Returning +1). Any other runes take effect on the thrown hit. It can still be used in melee.",
 "Throwing range ST x 1; the thrown attack succeeds on any roll of skill 16 or better; the weapon returns to the hand.",
 forks="1. 12\" is read as a 20-ft increment (two increments to about 40 ft).", price="+2 = 8,000 gp (Throwing +1 and Returning +1)")
T["Master Rune of Kragg the Grim"] = e("NEW", "none", 1,
 "Utility rune: lets a two-handed weapon (a great weapon) carry runes at all. It has no combat effect and uses one of the item's three rune slots. Master rune.",
 "No GURPS effect; a rules permission only.",
 forks="1. Priced +1 (2,000 gp) as a permission, by its 15 WFB points.")

T["Rune of Daemon Slaying"] = e("DELTA", "Banefire (Elemental 93-96)", 3,
 "Against creatures with the demon, devil or daemon subtype (the Daemonic rule). 1 rune: +1 effective enhancement bonus and +1d6 damage. 2 runes: +2 effective enhancement, +2d6, and one extra roll of the weapon's damage dice on a damaging hit (Multiple Wounds (D3), read as one extra roll). 3 runes: hits on a natural 2 or higher, +4d6, one extra damage roll, and the target's SR, ward and deflection bonuses do not apply (no ward saves).",
 "Innate Attack (Bane) 1d / 2d / 4d against daemons, with the extra injury roll at 2 and 3 runes; at 3 runes no ward or Magic Resistance applies.",
 collision="WoW Demonslaying and Damage vs Demons (D2): names stay.",
 forks="1. 'Daemonic' read as the demon, devil or daemon subtype; default includes devils.", price=LAD)
T["Rune of Fire"] = e("DELTA", "Flaming (Elemental 01-08) + Elemental Burst (Elemental 75-80)", 3,
 "1 rune: Flaming Attacks (the Flaming row's +1d6 fire damage on a hit). 2 runes: also a breath weapon once per encounter, a 15-ft cone of 2d6 fire (Reflex DC 14 half). 3 runes: the breath weapon is 3d6 and the burned target takes one further 1d6 fire damage at the start of its next turn (Multiple Wounds (D3), read as a second damage roll).",
 "Innate Attack Burning 1d Follow-Up on every damaging hit (1 rune); plus an Innate Attack Burning cone 2d once per encounter (2 runes); 3d plus a second 1d the next second (3 runes).",
 forks="1. Strength 4 breath weapon is read as 2d6 / 3d6 by the Elemental Burst Magic and Rare values.", price=LAD)
T["Rune of Fury"] = e("DELTA", "Rapid Assault (Offensive 25-30)", 3,
 "1 rune: +1 Attack, an extra attack at the highest base attack bonus once per day as a swift action (Rapid Assault T5). 2 runes: three times per day, plus the Frenzy special rule read as rage (+2 Str, -2 AC, must engage) once per encounter. 3 runes: an extra attack at will, rage, and after each hit that deals damage the weapon grants one further attack (the further attacks do not chain).",
 "Altered Time Rate (limited uses 1/day, 3/day, at will matching 3.5e) plus Berserk at 2 and 3 runes.",
 collision="DMG Speed (+3, an extra attack on every full attack); different cadence, names stay.",
 forks="1. '+1 Attack' every round would match DMG Speed; here it follows Rapid Assault's limited-use ladder to keep the price at +1 / +2 / +3.", price=LAD)
T["Rune of Cleaving"] = e("DELTA", "Armor Piercing (Offensive 19-24)", 3,
 "1 rune: the weapon ignores 2 points of DR (Armour Piercing (1)). 2 runes: also +2 Strength (untyped, one WFB Strength step) while wielded. 3 runes: also Killing Blow: the threat range widens by one step and a confirmed natural 20 against a same-size or smaller target forces a Lethal-severity location result.",
 "Armor Divisor (2) at 1 rune; ST +1 at 2 runes; at 3 runes the same Lethal-severity crit result against same-size targets.",
 collision="Mighty Cleaving (DMG, the Cleave feat extension) is unrelated.",
 forks="1. Armour Piercing (1) is read as ignoring 2 DR.", price=LAD)
T["Rune of Striking"] = e("DELTA", "Striking (Offensive 01-06)", 3,
 "1 rune: +1 attack bonus (one WFB Weapon Skill step, the Striking row). 2 runes: +2 attack bonus and once per round the wielder may reroll one missed attack. 3 runes: +4 attack bonus and the reroll (the source's Weapon Skill 10).",
 "Weapon Bond +1 / +2 / +4 to weapon skill, with a reroll of one missed attack per second at 2 and 3 runes.",
 forks="1. Weapon Skill 10 is capped at +4 attack rather than the +26 the profile table would give.", price=LAD)
T["Rune of Might"] = e("NEW", "none", 3,
 "1 rune (Rare): against creatures of Large size or larger (the source's Toughness 5 or higher) the wielder's Strength bonus to damage is doubled. 2 runes (Unique): also one extra roll of the weapon's damage dice on a damaging hit against them (Multiple Wounds (D3), read as one extra roll). A third rune has no further effect.",
 "Striking ST x2 on damage against SM +1 or larger; second damage roll at 2 runes.",
 forks="1. Toughness 5 or higher is read as Large or larger.", price="+2 / +3 = 8,000 / 18,000 gp by rune count (Rare / Unique)")
T["Rune of Dismay"] = e("DELTA", "Terrifying (Condition 25-30)", 2,
 "1 rune (Magic): Fear. Each enemy that first attacks the wielder in an encounter must succeed on a Will save (DC 13) or be shaken for 1d4 rounds. 2 runes (Rare): Terror. The save is DC 15 and a failure leaves the enemy frightened for 1d4 rounds. Mindless creatures and creatures of 17+ Hit Dice are immune. A third rune has no further effect.",
 "A Fright Check at -1 (Fear) or -2 (Terror) for each enemy that first attacks the wielder; Terror on failure for 1d4 seconds-rounds.",
 forks="1. Fear and Terror are read as the Terrifying row's Will DCs 13 and 15.", price="+1 / +2 = 2,000 / 8,000 gp by rune count (Magic / Rare)")
T["Grudge Rune"] = e("DELTA", "Hunter's Mark (Offensive 55-60)", 1,
 "At the start of each encounter the wielder designates one enemy creature as a swift action; against it the wielder gets +1 on attack rolls and may once per round reroll one damage roll and keep the better. One designation per Grudge Rune carried; multiples have no further effect.",
 "Hunter's Mark accessibility (marked target only) with +1 skill and a damage reroll per second against it.",
 collision="Ranger favored enemy and MIC Hunting: different, names stay.",
 forks="1. 'Nominate at the beginning of the game' is read as at the start of each encounter.")
