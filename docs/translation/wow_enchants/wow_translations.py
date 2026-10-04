"""Translations for the WoW weapon-enchant corpus. Rate card = Crusader (Affix Registry section 2); rules = ../FUSED_ENGINE_RESOLUTION.md.

CONVENTIONS (stated once, applied to every entry):
- Proc: 1 PPM -> 10% per damaging hit (Crusader's ratified convention). One d100 per damaging hit, one roll serves both systems, 01-10 fires, procs never proc other procs.
  Where the source gives a different rate it is used (Blade Ward 5%, Spellsurge 3%) and the rate is kept as a d100 band. Caster enchants roll per damaging spell cast.
- Duration: source seconds / 6, rounded up, in 3.5e rounds (15 s = 3, 12 s = 2, 10 s = 2, 7 s = 2, 6 s = 1, 20 s = 4). GURPS keeps the source's exact seconds.
- Primary-stat buff: Crusader's original 100 Strength = Rare rung (+4); half or less = Magic rung (+2). Untyped, so two weapons stack. GURPS stat = half the 3.5e points (2:1).
- Secondary ratings (crit, haste, mastery, versatility, dodge, parry): one untyped +1 step; ratings have no direct 3.5e equivalent and the mapping is flagged.
- Damage riders: pool ladders (Elemental 1d4/1d6/1d8/2d6/3d6; Life Shield heal 5/8/12; Souldrinker mana 3/5/8/12/20), chosen by rung. GURPS dice read as-is.
- Price: bonus-equivalent squared x 2,000 gp. Rung = the strength of the effect against Crusader's three rungs (+1 Magic, +2 Rare, +3 Unique).
- Healing is ordinary magical healing and ends Fatal Wound stacks (Chad's 2026-10-04 ruling D2).
- GURPS chassis for all: Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%), no GURPS point total (engine resolution).
"""
PROC = "Proc: one d100 on each damaging hit, 01-10 fires (the source's 1 PPM at the ratified Crusader convention)."
T = {}

# ---- COVERED by an existing Registry pool row (no second document) ----
T["Fiery Weapon"] = dict(verdict="COVERED", base="Flaming (Elemental 01-08)", note="Flaming deals +1d4/+1d6/+1d8/+2d6/+3d6 fire on every hit. Fiery Weapon's 34 fire at 6 PPM is the same shape (a near-every-hit fire rider); no new family. Gap: none.")
T["Lifestealing"] = dict(verdict="COVERED", base="Vampiric (MIC, registered in the weapon-affix corpus) / Leech (Resource 19-24)", note="Lifestealing steals about 30 life per proc as shadow damage; Vampiric (+1d6 and heal equal) and Leech (heal per hit) cover the heal-on-hit shape. Difference: Lifestealing is a 6 PPM proc, the existing rows are every-hit. Fork recorded in the compendium: none needed.")
T["Flametongue Weapon"] = dict(verdict="COVERED", base="Flaming (Elemental 01-08)", note="The Enhancement-spec Flametongue adds fire damage to each attack (3.96% of Attack Power): Flaming covers it. The Elemental-spec +5% Fire spell damage is a spell rider, covered by Elemental Attunement (Elemental 87-92).")
T["Frostbrand Weapon"] = dict(verdict="COVERED", base="Freezing (Elemental 09-16) + Slowing (Condition 01-08)", note="Frostbrand (Classic): chance of 48 frost damage and a 25% movement slow for 8 s. Freezing gives the frost rider; Slowing gives the slow. Covered together.")
T["Rockbiter Weapon"] = dict(verdict="COVERED", base="Striking (Offensive 01-06)", note="Classic Rockbiter is +50 melee attack power and threat; a flat enhancement-style bonus, covered by Striking. The threat clause has no 3.5e mechanic.")
T["Rune of the Fallen Crusader"] = dict(verdict="COVERED", base="Crusader family (Affix Registry section 2)", note="The Registry's Crusader source record already names this rune as the percent-scaled sibling (heal 4% max HP, +15% Strength, 15 s). The family covers it; its flat values replace the percentages.")
T["Avalanche"] = dict(verdict="COVERED", base="Shocking (Elemental 17-24), element chosen at creation", note="Avalanche deals 74 Nature damage often (proc rate not given). The Elemental pool rows are element-parametric riders; Nature has no 3.5e energy type. Default element: electricity (Shocking). Fork: acid is the other reasonable reading.")

# ---- DELTA / NEW: full entries ----
def e(verdict, base, bonus, three_e, gurps, collision="none.", forks="none.", note=""):
    return dict(verdict=verdict, base=base, bonus=bonus, three_e=three_e, gurps=gurps, collision=collision, forks=forks, note=note)

T["Icy Chill"] = e("DELTA", "Slowing (Condition 01-08)", 1,
 PROC + " On fire the target is chilled for 1 round (5 s): land speed x0.7 (round down to 5 ft) and -1 on attack rolls (the source's 25% longer time between attacks, at one step). No save (the source gives none), no SR. Melee weapons only. Does not stack with itself.",
 "On a damaging hit that fires: Affliction (Reduced Move 30% and -1 to skill with weapon attacks), exactly 5 seconds, no resistance roll. Same d100 as 3.5e.",
 forks="1. Proc rate is not in the source (page says unclear PPM versus chance on hit); default 10% per damaging hit. 2. Slow is lighter than the Slowing row (no save, 1 round, speed x0.7), as the source's 30% implies.")
T["Unholy Weapon"] = e("NEW", "none", 1,
 PROC + " On fire the target takes 1d4 negative-energy damage (the shadow damage added in patch 3.3.0; the amount is not in the source, so this is the Shadowtouch Magic-rung value) and a curse: -2 on its melee damage rolls for 2 rounds (source: -15 damage, 12 s). No save, no SR; undead take the negative damage as Shadowtouch does (half).",
 "Innate Attack Toxic [Cosmic] 1d Follow-Up on the hit, plus Affliction (Weakened: -2 damage on the target's melee attacks), exactly 12 seconds. Same d100.",
 collision="DMG/Registry affix 'Unholy' (alignment weapon, +2d6 vs good): different mechanic; names stay, never merge. Pool 'Weakening' (-Str) is also different.",
 forks="1. Shadow damage amount and proc rate are not in the source; values are Magic-rung design values.")
T["Demonslaying"] = e("DELTA", "Banefire (Elemental 93-96)", 1,
 "Against creatures with the demon subtype (tanar'ri, baatezu and other fiends the campaign names demons): +2d6 damage on every damaging hit (Banefire Magic-rung value, the 'heavy damage'), and on a 01-10 d100 the target is stunned 1 round, Fortitude DC 14 negates (Slowing/Dazing Magic-rung DC). Melee only.",
 "Innate Attack (Bane) 2d Follow-Up against demons, plus Affliction (Stunned) 1 second with a Quick Contest of the target's HT against effective skill 14.",
 collision="Dragondoom, Banefire family (names unrelated).",
 forks="1. Proc rate, stun length and damage amounts are not in the source; Banefire and Dazing Magic-rung values used. 2. 'Demon' means the demon subtype only; devils are a separate subtype (default: devils excluded).")
T["Mongoose"] = e("NEW", "none", 2,
 PROC + " On fire: +4 Dexterity (untyped) for 3 rounds, applying to attack, AC, Reflex and Dex skills (source original: +120 Agility, 15 s). The source's +30 haste rating is under one step and is dropped. Re-proc on the same weapon refreshes and does not stack; two Mongoose weapons stack (untyped, as Crusader).",
 "On the same d100: DX +2 for exactly 15 seconds (the 3.5e +4 at 2:1), refreshed by a same-weapon re-proc, stacking across two weapons.",
 forks="1. The current wiki tooltip is scaled down (60 Agility, 15 haste); the original TBC values (+120, 30 haste rating, 15 s, about 1 PPM) come from a search snippet and are what this entry uses. 2. Haste is dropped as below one step.")
T["Executioner"] = e("DELTA", "Armor Piercing (Offensive 19-24)", 2,
 PROC + " On fire, for 3 rounds the wielder's attacks ignore worn DR (the engine's ignores-armor flag; source original: ignores 840 armor for 15 s). Natural toughness is not ignored. Only one instance active at a time (source patch 3.3.3). The current crit-rating version (+60 crit rating) is the later redesign and is not used.",
 "On the same d100: for exactly 15 seconds the wielder's attacks skip worn DR (ignores_armor flag), natural DR still applies.",
 collision="Pool affix 'Executioner' (Offensive 37-42, bonus damage vs bloodied targets): different mechanic; names stay, never merge. Also the Armor Piercing row is a flat ignore-DR value, not a timed proc.",
 forks="1. Armor-penetration amount is from a search snippet (840); proc rate not in the source (default 10%).")
T["Spellsurge"] = e("NEW", "none", 1,
 "Proc: one d100 on each spell the wielder casts, 01-03 fires (the source's 3%). On fire every ally within 30 ft, wielder included, recovers 5 mana (the Souldrinker Magic-rung value; source: 100 mana over 10 s to party members). Hybrid campaign note: only characters who carry a mana pool benefit. Melee weapon, spells cast by the wielder.",
 "On the same d100 (per spell cast): Energy Reserve recovery of 5 points to each ally within 10 yards.",
 forks="1. Mana scale: 100 mana at the source's level is rescaled to the pool's Souldrinker rung; default 5 mana.")
T["Battlemaster"] = e("NEW", "none", 1,
 PROC + " On fire every ally within 30 ft, wielder included, is healed 5 HP (the Crusader Magic-rung heal; source 76 to 126 healing, a little over a third of Crusader's 240). Magical healing: ends Fatal Wound stacks. Melee hits only.",
 "On the same d100: Regeneration burst of 5 HP to each ally within 10 yards, at once.",
 forks="1. Heal is the Magic-rung 5; source ratio to Crusader is about 0.4, which rounds to the same step.")
T["Deathfrost"] = e("DELTA", "Freezing (Elemental 09-16) + Slowing (Condition 01-08)", 2,
 PROC + " For spells: one d100 per damaging spell the wielder casts, 01-10, then not again for 4 rounds (the source's 25 s internal cooldown). On fire: +1d6 cold damage and the target's land speed is x0.7 for 1 round (Icy Chill precedent; the source gives neither amount). Procs off damage-over-time ticks (patch 2.4.3). No slow on creatures of 17+ Hit Dice.",
 "On the same d100: Innate Attack Burning [Cold] 1d Follow-Up, plus Affliction (Reduced Move 30%) 5 seconds.",
 forks="1. Frost damage and slow amounts are not in the source; Freezing Magic-rung 1d6 and the Icy Chill slow are used. 2. The source's 'no slow on level 73+' is read as no slow on Tier 1 creatures (17+ Hit Dice). 3. Spell proc is cut from the source's 50% to 10% per cast to match the ratified melee convention.")
T["Berserking"] = e("NEW", "none", 2,
 PROC + " On fire for 3 rounds: +3 damage on melee damage rolls and -2 AC (untyped; source +400 attack power and 'reduced armor', amounts for armor loss and duration not given). Re-proc refreshes; two weapons stack.",
 "On the same d100: Striking ST +1 and DR -1 (Gadget) for exactly 15 seconds, refreshed by re-proc.",
 collision="Pool affix 'Berserker' (Offensive 61-66, +damage with -AC while attacking) and MIC 'Berserker' (extra 1d8 while raging): different mechanics; names stay, never merge.",
 forks="1. Duration, proc rate and armor reduction are not in the source (default 10%, 3 rounds, -2 AC).")
T["Black Magic"] = e("DELTA", "Catalyst (Resource 73-78)", 1,
 "Proc: one d100 on each damaging spell the wielder casts, 01-10 fires, then not again for 6 rounds (the source's 35 s internal cooldown). On fire: +2 caster level on the wielder's damaging spells for 2 rounds (the source's +62 haste rating has no direct 3.5e step; caster level is the closest damage proxy, the Catalyst Magic-rung +2). Melee weapon.",
 "On the same d100: Talent (Magical) +2 on the wielder's attack spells for exactly 12 seconds.",
 forks="1. Haste maps to +2 caster level; this is an interpretation, flagged. 2. Duration not in the source; 12 s assumed from the Cataclysm-era sibling enchants. 3. Source proc is about 35%; cut to 10% per cast.")
T["Blade Ward"] = e("NEW", "Thorns (Defensive 43-48) + Bladesinger (Skill/Class 31-36)", 2,
 "Proc: one d100 on each damaging hit, 01-05 fires (the source's about 5%). On fire for 2 rounds (10 s): +2 dodge bonus to AC and the first melee attack that misses the wielder deals 2d6 untyped damage to its attacker (source: +100 parry rating and 286 to 315 damage on the next parry). The damage ignores worn DR and the effect then ends.",
 "On the same d100: Enhanced Parry +1 for exactly 10 seconds; the first successful parry deals 2d to the attacker.",
 forks="1. Parry becomes dodge AC because the 3.5e chassis has no parry stat. 2. Damage uses the Thorns Rare-rung 2d6.")
T["Blood Draining"] = e("NEW", "none", 2,
 PROC + " On fire (also on the wielder's bleed ticks dealing damage) the wielder gains one Blood Reserve; up to 5 at once, each lasting 4 rounds (20 s). Whenever the wielder's hit points fall below 35% of maximum, every Blood Reserve is spent at once and each heals 8 HP (the Lifedrinker Magic-to-Rare value; source 180 to 219). Magical healing: ends Fatal Wound stacks.",
 "On the same d100: Regeneration (limited) stored burst, up to 5 stacks, 20 seconds each, each 8 HP when HP drops below 35%.",
 forks="1. The source does not say whether the heal is per stack or total; default per stack, spent together. 2. Proc rate not in the source (default 10%).")
T["Windfury Weapon"] = e("DELTA", "Rapid Assault (Offensive 25-30)", 2,
 "On each main-hand hit, d100 01-25 fires (the source's 25%): the wielder immediately makes two extra melee attacks at the highest base attack bonus with the same weapon. The extra attacks cannot fire Windfury (source: cannot proc off itself). Melee main-hand weapon only.",
 "On the same d100: two extra attacks at the full weapon skill, same weapon; the extra attacks cannot trigger the effect again.",
 forks="1. The Classic-era tooltip was not retrieved; the current retail wording (25%, two attacks) is used. 2. Priced below DMG Speed (+3): 25% of two attacks is half an extra attack per hit.")
T["Earthliving Weapon"] = e("NEW", "none", 1,
 "Proc: one d100 on each healing spell the wielder casts on a creature, 01-20 fires (the source's 20%). On fire the target also regains 3 HP at the start of each of its next 2 turns (the source's heal over 6 s at the Magic rung). Magical healing: ends Fatal Wound stacks.",
 "On the same d100 (per healing spell): Regeneration 3 HP at 3 seconds and again at 6 seconds.",
 forks="1. Retail wording used; the Classic version was not retrieved.")
T["Rune of Razorice"] = e("DELTA", "Freezing (Elemental 09-16) + Vulnerability (Condition 73-78)", 2,
 "Every damaging melee hit adds +1d6 cold damage (the Freezing Magic-rung value; source 1.127% of attack power as extra Frost damage) and one Razorice stack on the target, up to 5 stacks, each stack lasting 4 rounds (20 s). While the target holds 2 or more stacks the wielder's cold damage against it gains +1 per damage roll; at 4 or more, +2 (the source's 3% per stack vulnerability, at about 15% on the full 5, read as +1 per 2 stacks). Class lock: runeforging is a Death Knight craft.",
 "Innate Attack Burning [Cold] 1d Follow-Up on every damaging hit; stacks as the 3.5e side; +1 damage on cold attacks at 2 stacks, +2 at 4, for exactly 20 seconds from the last stack.",
 forks="1. Percent vulnerability to flat damage is an interpretation, flagged. 2. Death Knight runeforging has no 3.5e class; the rune is usable only by a wielder the GM rules a rune-smith.")
T["Rune of Cinderglacier"] = e("NEW", "none", 1,
 PROC + " On fire, the wielder's next two cold or negative-energy damaging effects within 5 rounds (30 s) each deal +2 damage (the source's +20% on typical Magic-rung damage). Class lock as Razorice.",
 "On the same d100: the next two cold or Toxic [Cosmic] attacks within exactly 30 seconds gain +2 damage each.",
 forks="1. Proc rate not in the source (default 10%). 2. 20% to flat +2 is an interpretation.")
T["Rune of Swordbreaking"] = e("NEW", "Bladesinger (Skill/Class 31-36)", 1,
 "While wielded: +1 dodge bonus to AC (the source's +2% parry chance, at one step) and a +4 bonus on checks to avoid being disarmed, and a weapon the wielder is disarmed of can be recovered as a move action instead of a standard action (the source halves Disarm duration). One-handed weapons only.",
 "Enhanced Parry +1 and +4 to resist Disarm; recovery of a dropped weapon takes half the time.",
 forks="1. The WoW disarm debuff (cannot use weapon for a time) is read as the 3.5e disarm maneuver; flagged.")
T["Rune of Swordshattering"] = e("NEW", "Bladesinger (Skill/Class 31-36)", 1,
 "As Swordbreaking on a two-handed weapon, at double the parry step: +2 dodge bonus to AC (source +4% parry), +4 on checks to avoid being disarmed, disarmed weapon recovered as a move action.",
 "Enhanced Parry +2 and +4 to resist Disarm; recovery in half the time.",
 forks="1. Same disarm reading as Swordbreaking.")
T["Rune of Spellbreaking"] = e("NEW", "Spell Ward (Defensive 37-42)", 1,
 "While wielded: each damaging spell that hits the wielder deals 1 less damage (minimum 0; the source deflects 2% of spell damage, which at the Magic rung is 1 point), and Silence effects on the wielder last half as long (rounded down, minimum 1 round). One-handed weapons only.",
 "Damage Resistance 1 against spell damage only (Gadget; Only vs spells -20%) and Silence duration halved.",
 forks="1. Percentage deflection to a flat point; flagged.")
T["Rune of Spellshattering"] = e("NEW", "Spell Ward (Defensive 37-42)", 1,
 "As Spellbreaking on a two-handed weapon at double the step: each damaging spell that hits the wielder deals 2 less damage (source 4%), Silence on the wielder lasts half as long.",
 "Damage Resistance 2 against spell damage only and Silence duration halved.",
 forks="1. Same flat-point reading as Spellbreaking.")
T["Rune of the Stoneskin Gargoyle"] = e("NEW", "Iron Skin (Defensive 19-24)", 2,
 "While wielded: +1 untyped bonus to every ability score and +1 natural armor bonus to AC (the source's +5% Armor and +5% all stats, which on typical scores is about +1 each). Class lock as Razorice; the page calls it the death knight tank's rune.",
 "Attributes +1 each (ST, DX, IQ, HT) and DR +1 (Gadget), uncosted.",
 forks="1. Percent stats to a flat +1 on every score is an interpretation; flagged. 2. Priced at +2 although the all-stat bonus is generous, to keep it Rare-rung.")
T["Windwalk"] = e("DELTA", "Swiftfoot (Utility 01-06)", 1,
 PROC + " On fire for 2 rounds: +1 dodge bonus to AC and +5 ft land speed (source: +99 dodge rating and +10% movement speed, 10 s, no internal cooldown, refreshes itself). Re-proc refreshes.",
 "On the same d100: Enhanced Dodge +1 and Enhanced Move (Ground) 0.5 for exactly 10 seconds.",
 forks="1. Proc rate not in the source (default 10%).")
T["Mending"] = e("NEW", "none", 1,
 PROC + " On fire the wielder heals 5 HP (the Crusader Magic-rung heal; the source gives no amount). Works on spell damage as well as melee (one d100 per damaging spell cast). Magical healing: ends Fatal Wound stacks.",
 "On the same d100: Regeneration burst of 5 HP at once.",
 forks="1. Heal amount and proc rate are not in the source; both default to the Crusader Magic rung. 2. Overlaps the heal half of the Crusader Magic rung; kept separate because it carries no Strength bonus.")
T["Landslide"] = e("DELTA", "Striking (Offensive 01-06)", 1,
 PROC + " On fire for 2 rounds (12 s): +2 on melee damage rolls (untyped; source +100 attack power at 1 PPM). Re-proc refreshes; two weapons stack.",
 "On the same d100: Striking ST +1 for exactly 12 seconds.",
 forks="none.")
T["Power Torrent"] = e("NEW", "none", 1,
 "Proc: one d100 on each damaging or healing spell the wielder casts, 01-10 fires, then not again for 8 rounds (the source's 45 s internal cooldown). On fire: +2 Intelligence (untyped) for 2 rounds (source +83 Intellect, 12 s).",
 "On the same d100: IQ +1 for exactly 12 seconds.",
 forks="1. Source proc is about 33%; cut to 10% per cast.")
T["Hurricane"] = e("NEW", "none", 1,
 PROC + " On a damaging hit or spell, then not again for 8 rounds (45 s internal cooldown): +1 untyped bonus on attack rolls and +2 initiative for 2 rounds (the source's +74 haste rating, 12 s; haste is read as one attack-step plus initiative). Healing spells also roll it.",
 "On the same d100: +1 skill with weapon attacks and +2 to initiative-type reaction rolls for exactly 12 seconds.",
 forks="1. Haste rating to a +1 step is an interpretation; flagged. 2. Source proc about 10-15%; 10% used.")
T["Elemental Slayer"] = e("NEW", "none", 1,
 PROC + " Against creatures of the elemental type: +1d6 force damage (the source's Arcane damage; force is the 3.5e arcane damage type) and the target cannot cast spells or use spell-like abilities for 1 round (source: silenced 5 s). No save. Melee only.",
 "On the same d100, against Elemental-type foes: Innate Attack Crushing [Cosmic] 1d Follow-Up plus Affliction (Mute) 5 seconds.",
 collision="Banefire (Elemental 93-96) keys on element subtypes; this keys on the elemental creature type. Different; names stay.",
 forks="1. Damage amount and proc rate not in the source (Magic-rung 1d6, 10%).")
T["Heartsong"] = e("NEW", "none", 1,
 "Proc: one d100 on each damaging or healing spell the wielder casts, 01-10 fires, then not again for 3 rounds (the source's 20 s internal cooldown). On fire for 3 rounds (15 s): +1 untyped bonus to spell damage and to healing done, and the wielder takes 1 less damage from each hit (the source's Versatility +30 turns damage done, healing done and damage taken one step each).",
 "On the same d100: +1 damage on the wielder's spell attacks, +1 HP on healing, DR 1 against hits, exactly 15 seconds.",
 forks="1. Versatility to three +1 steps is an interpretation; flagged. 2. Source proc about 25%; 10% used.")
T["Dancing Steel"] = e("DELTA", "Mongoose (this corpus)", 2,
 PROC + " On fire for 3 rounds: +4 to Strength or Dexterity, whichever score is higher (untyped; source: +81 Strength or Agility, the highest stat is always chosen). Re-proc refreshes; two weapons stack.",
 "On the same d100: ST or DX +2 (the higher), exactly 15 seconds assumed.",
 forks="1. Duration and proc rate are not in the source (3 rounds and 10% assumed). 2. Same rung as Mongoose, which it mirrors.")
T["Elemental Force"] = e("DELTA", "Prismatic (Elemental 69-74)", 1,
 PROC + " On fire +1d6 damage of a random element (the Prismatic Magic-rung rider; the source's 58 'Elemental damage'). Works on damaging spells and melee hits. Level cap in the source (items up to level 50) is dropped.",
 "On the same d100: Innate Attack Follow-Up 1d of a randomly chosen energy type.",
 forks="1. Proc rate not in the source (10%). 2. The source's item-level cap of 50 is a game-balance cap with no 3.5e meaning.")
T["River's Song"] = e("NEW", "none", 1,
 PROC + " On fire for 2 rounds (7 s): +1 dodge bonus to AC (the source's +65 dodge rating).",
 "On the same d100: Enhanced Dodge +1 for exactly 7 seconds.",
 forks="1. Proc rate not in the source (10%).")
T["Jade Spirit"] = e("NEW", "none", 1,
 "Proc: one d100 on each damaging or healing spell cast by the wielder, 01-10 fires. On fire: +2 Intelligence (untyped) for 3 rounds (source +65 Intellect; duration not given). If the wielder has used more than 75% of a mana pool, also +1 on spell damage (the source's Versatility +30 below 25% mana).",
 "On the same d100: IQ +1; if Energy Reserve is below a quarter, also +1 damage on attack spells, 15 seconds assumed.",
 forks="1. Duration and proc rate not in the source (3 rounds, 10%).")
T["Colossus"] = e("DELTA", "Life Shield (Defensive 31-36)", 1,
 PROC + " On a damaging melee hit that fires, the wielder gains 8 temporary hit points (the Life Shield Rare-rung value; source: a Mogu protection absorbing up to 371 damage). The temporary hit points last until used or 1 minute; they do not stack with other temporary hit points.",
 "On the same d100: a damage absorption pool of 8 HP (Damage Resistance burst) until used or 60 seconds.",
 forks="1. Duration and proc rate are not in the source (10%, 1 minute). 2. Absorb shield read as temporary hit points.")
T["Windsong"] = e("NEW", "none", 1,
 PROC + " On fire roll d3: 1 = +1 on confirmation rolls for critical hits, 2 = +1 on attack rolls, 3 = +1 damage; all untyped, 2 rounds (the source randomly picks crit, haste or mastery at +59 for 12 s). Heals and spells also roll it.",
 "On the same d100 plus a d3: +1 to confirm crits, +1 skill, or +1 damage, exactly 12 seconds.",
 forks="1. Ratings read as +1 steps; flagged. 2. Proc rate not in the source (10%).")
# Warlords marks (degraded sources)
T["Mark of the Thunderlord"] = e("NEW", "none", 1,
 PROC + " On fire for 1 round (6 s): +2 on rolls to confirm critical hits; each confirmed critical hit during it extends the effect by 1 round, up to 3 rounds in all (source summary: +500 crit for 6 s, crits extend the duration).",
 "On the same d100: +1 to critical-hit confirmation, extended 1 second-round per crit, exactly 6 seconds base.",
 forks="1. Degraded source: only a summary of the numbers was retrieved; no verbatim tooltip, no proc rate.")
T["Mark of the Frostwolf"] = e("NEW", "none", 1,
 PROC + " On fire, +1 damage on melee damage rolls for 1 round (6 s); a second proc stacks once (2 stacks, +2) (source summary: +500 multistrike for 6 s, 2 stacks; multistrike is a chance to repeat a hit, read at one step).",
 "On the same d100: +1 damage per stack, 2 stacks, exactly 6 seconds each.",
 forks="1. Degraded source (summary only). 2. Multistrike to flat damage is an interpretation; flagged.")
T["Mark of Blackrock"] = e("NEW", "none", 1,
 PROC + " On fire while the wielder is at or below half hit points: +2 natural armor bonus to AC for 2 rounds (source summary: +500 armor below 50% health for 12 s).",
 "On the same d100, only below half HP: DR +1 for exactly 12 seconds.",
 forks="1. Degraded source (summary only).")
T["Mark of Shadowmoon"] = e("NEW", "none", 1,
 PROC + " On fire the wielder gains fast healing 1 for 3 rounds (source summary: +500 spirit for 15 s; Spirit is a regeneration stat). Fast healing is magical healing: ends Fatal Wound stacks.",
 "On the same d100: Regeneration (slow) 1 HP per second for exactly 15 seconds, capped at the 3.5e total.",
 forks="1. Degraded source (summary only). 2. Spirit to fast healing 1 is an interpretation; flagged.")
T["Mark of the Shattered Hand"] = e("DELTA", "Fatal Wound family (Affix Registry section 1)", 1,
 PROC + " On fire the target bleeds 2 HP at the start of its turn for 3 rounds (6 HP total); bleeds from repeated procs do not stack, they refresh. Untyped, ignores DR, bloodless creatures immune (the Fatal Wound conventions). Source summary: 1500 bleed damage plus 4500 per 6 s (ambiguous).",
 "Follow-Up Toxic Attack (Follow-Up +0%) 2 HP per second for 3 seconds on the same d100.",
 collision="Fatal Wound family (stacking bleed) and DMG Wounding; names stay, never merge.",
 forks="1. Degraded source (summary only); the '4500/6 sec' reading is ambiguous and the entry uses the smaller bleed. 2. Does not stack, unlike Fatal Wound.")
T["Mark of Warsong"] = e("NEW", "none", 1,
 PROC + " On fire: +2 on attack rolls in the first round, +1 in the second, nothing after (source summary: +1000 haste decaying 10% every 2 s). Untyped.",
 "On the same d100: +2 then +1 skill with weapon attacks over two seconds-rounds.",
 forks="1. Degraded source (summary only). 2. Decay stepped to two rounds.")
T["Mark of Bleeding Hollow"] = e("NEW", "none", 1,
 PROC + " On fire for 2 rounds (12 s): +1 untyped bonus on melee damage rolls (source summary: +500 mastery; mastery is class-dependent and read at one step).",
 "On the same d100: +1 damage for exactly 12 seconds.",
 forks="1. Degraded source (summary only). 2. Mastery read as +1 damage.")
