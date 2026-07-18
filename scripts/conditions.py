#!/usr/bin/env python3
"""
conditions.py — D&D 3.5e condition reference / lookup
The New Path campaign engine (the-new-path-engine)

GOVERNING SOURCES (read, not memory):
    Dungeon Master's Guide 3.5, Chapter 8 Glossary, "Condition Summary",
    pp. 300-301  (I:\\Sourcebooks\\_md\\Dungeon_Masters_Guide_3.5.md,
    PDF pages 301-302 of the transcription)
    D&D 3.5 DM Screen, "Armor Class Modifiers (PH page 151)" panel
    (I:\\Sourcebooks\\_md\\DM_Screen.md, PDF page 5) — supplies the melee/ranged
    AC-modifier cross-check table and the two screen-only rows
    (Kneeling or Sitting, Squeezing Through a Space).

DESIGN CONTRACT (repo README):
    - Stateless resolver: flags in, text out. No state file, no dice.
    - Visible output: every lookup prints a ready-to-paste block.
    - No cross-imports. Other scripts that need condition names duplicate them
      deliberately.
    - --selftest runs worked examples against the governing pages' exact values.

USAGE
    python3 conditions.py stunned
    python3 conditions.py "flat-footed" prone
    python3 conditions.py --list
    python3 conditions.py --search "Dexterity bonus"
    python3 conditions.py --json blinded
    python3 conditions.py --selftest
"""

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict

# ============================================================================
# DATA MODEL
# ============================================================================

@dataclass
class Condition:
    name: str
    source: str                      # page citation
    text: str                        # full rules text per the source
    effects: List[str]               # bullet mechanics, verbatim-derived
    ac_melee: Optional[str] = None   # DM Screen AC-modifier table (PH 151)
    ac_ranged: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    see_also: List[str] = field(default_factory=list)


DMG = "DMG 3.5 p.300-301 (Condition Summary)"
SCREEN = "DM Screen — AC Modifiers (PH p.151)"

# ============================================================================
# THE CONDITIONS — DMG 3.5 Condition Summary, pp. 300-301, complete.
# Text fields carry the rules content of the source entries. AC columns are the
# DM Screen panel's melee/ranged rows where the panel lists the condition.
# ============================================================================

CONDITIONS: List[Condition] = [

Condition(
    name="Ability Damaged", source=DMG,
    text=("The character has temporarily lost 1 or more ability score points. "
          "Lost points return at a rate of 1 per day unless noted otherwise by "
          "the condition dealing the damage. Str 0: falls to the ground, helpless. "
          "Dex 0: paralyzed. Con 0: dead. Int, Wis, or Cha 0: unconscious. "
          "Ability damage is different from penalties to ability scores, which go "
          "away when the conditions causing them (fatigue, entanglement, etc.) go away."),
    effects=["Temporary loss of ability points; heals 1 point/day unless noted",
             "Str 0 = helpless (on the ground)", "Dex 0 = paralyzed",
             "Con 0 = dead", "Int/Wis/Cha 0 = unconscious"],
    tags=["ability"], see_also=["Ability Drained", "Helpless", "Paralyzed", "Unconscious"]),

Condition(
    name="Ability Drained", source=DMG,
    text=("The character has permanently lost 1 or more ability score points; "
          "regained only through magical means. Str 0: falls to the ground, "
          "helpless. Dex 0: paralyzed. Con 0: dead. Int, Wis, or Cha 0: unconscious."),
    effects=["Permanent loss of ability points; magic only to restore",
             "Zero-score consequences as Ability Damaged"],
    tags=["ability"], see_also=["Ability Damaged"]),

Condition(
    name="Blinded", source=DMG,
    text=("The character cannot see. He takes a -2 penalty to Armor Class, loses "
          "his Dexterity bonus to AC (if any), moves at half speed, and takes a -4 "
          "penalty on Search checks and on most Strength- and Dexterity-based skill "
          "checks. All checks and activities that rely on vision (such as reading "
          "and Spot checks) automatically fail. All opponents are considered to "
          "have total concealment (50% miss chance) to the blinded character. "
          "Characters who remain blinded for a long time grow accustomed to these "
          "drawbacks and can overcome some of them (DM's discretion)."),
    effects=["-2 AC", "Lose Dex bonus to AC", "Half speed",
             "-4 on Search and most Str-/Dex-based skill checks",
             "Vision-based checks (reading, Spot) automatically fail",
             "All opponents have total concealment vs. you (50% miss chance)"],
    ac_melee="-2", ac_ranged="-2",
    tags=["senses", "lose_dex", "movement"], see_also=["Dazzled"]),

Condition(
    name="Blown Away", source=DMG,
    text=("Depending on its size, a creature can be blown away by winds of high "
          "velocity (Table 3-24, DMG p.95). A creature on the ground that is blown "
          "away is knocked down and rolls 1d4x10 feet, taking 1d4 points of "
          "nonlethal damage per 10 feet. A flying creature that is blown away is "
          "blown back 2d6x10 feet and takes 2d6 points of nonlethal damage due to "
          "battering and buffeting."),
    effects=["Ground: knocked down, roll 1d4x10 ft., 1d4 nonlethal per 10 ft.",
             "Flying: blown back 2d6x10 ft., 2d6 nonlethal"],
    tags=["environment", "wind"], see_also=["Knocked Down", "Checked"]),

Condition(
    name="Checked", source=DMG,
    text=("Prevented from achieving forward motion by an applied force, such as "
          "wind. Checked creatures on the ground merely stop. Checked flying "
          "creatures move back a distance specified in the description of the effect."),
    effects=["Ground: stop", "Flying: pushed back per the effect"],
    tags=["environment", "wind"], see_also=["Blown Away"]),

Condition(
    name="Confused", source=DMG,
    text=("A confused character's actions are determined by rolling d% at the "
          "beginning of his turn: 01-10, attack caster with melee or ranged weapons "
          "(or close with caster if attacking is not possible); 11-20, act normally; "
          "21-50, do nothing but babble incoherently; 51-70, flee away from caster "
          "at top possible speed; 71-100, attack nearest creature (a familiar counts "
          "as part of the subject's self). A confused character who can't carry out "
          "the indicated action does nothing but babble incoherently. Attackers are "
          "not at any special advantage. Any confused character who is attacked "
          "automatically attacks its attackers on its next turn, as long as it is "
          "still confused. A confused character does not make attacks of opportunity "
          "against any creature that it is not already devoted to attacking."),
    effects=["d% each turn: 01-10 attack caster / 11-20 act normally / "
             "21-50 babble / 51-70 flee caster / 71-100 attack nearest",
             "If attacked, auto-attacks its attackers next turn while confused",
             "No AoOs except vs. creatures it's already devoted to attacking"],
    tags=["mind", "action_limit"], see_also=["Dazed"]),

Condition(
    name="Cowering", source=DMG,
    text=("The character is frozen in fear and can take no actions. A cowering "
          "character takes a -2 penalty to Armor Class and loses her Dexterity "
          "bonus (if any)."),
    effects=["No actions", "-2 AC", "Lose Dex bonus to AC"],
    ac_melee="-2", ac_ranged="-2",
    tags=["fear", "no_actions", "lose_dex"],
    see_also=["Shaken", "Frightened", "Panicked"]),

Condition(
    name="Dazed", source=DMG,
    text=("The creature is unable to act normally. A dazed creature can take no "
          "actions, but has no penalty to AC. A dazed condition typically lasts "
          "1 round."),
    effects=["No actions", "No AC penalty", "Typically lasts 1 round"],
    tags=["no_actions"], see_also=["Stunned", "Confused"]),

Condition(
    name="Dazzled", source=DMG,
    text=("The creature is unable to see well because of overstimulation of the "
          "eyes. A dazzled creature takes a -1 penalty on attack rolls, Search "
          "checks, and Spot checks."),
    effects=["-1 on attack rolls, Search checks, and Spot checks"],
    tags=["senses"], see_also=["Blinded"]),

Condition(
    name="Dead", source=DMG,
    text=("The character's hit points are reduced to -10, his Constitution drops "
          "to 0, or he is killed outright by a spell or effect. The soul leaves the "
          "body. Dead characters cannot benefit from normal or magical healing, but "
          "they can be restored to life via magic. A dead body decays normally "
          "unless magically preserved; magic that restores a dead character to life "
          "also restores the body either to full health or to its condition at the "
          "time of death (depending on the spell or device)."),
    effects=["Triggered at -10 hp, Con 0, or death effects",
             "No normal or magical healing; raise/resurrection magic only"],
    tags=["hp_state"], see_also=["Dying", "Stable", "Disabled"]),

Condition(
    name="Deafened", source=DMG,
    text=("A deafened character cannot hear. She takes a -4 penalty on initiative "
          "checks, automatically fails Listen checks, and has a 20% chance of spell "
          "failure when casting spells with verbal components. Characters who remain "
          "deafened for a long time grow accustomed to these drawbacks and can "
          "overcome some of them (DM's discretion)."),
    effects=["-4 on initiative checks", "Automatically fail Listen checks",
             "20% spell failure on verbal-component spells"],
    tags=["senses"], see_also=[]),

Condition(
    name="Disabled", source=DMG,
    text=("A character with 0 hit points, or one who has negative hit points but "
          "has become stable and conscious, is disabled. A disabled character may "
          "take a single move action or standard action each round (but not both, "
          "nor full-round actions). She moves at half speed. Move actions don't risk "
          "further injury, but performing any standard action (or any action the DM "
          "deems strenuous, including some free actions such as casting a quickened "
          "spell) deals 1 point of damage after the completion of the act. Unless "
          "the action increased her hit points, she is now in negative hit points "
          "and dying. A disabled character with negative hit points recovers hit "
          "points naturally if she is being helped; otherwise, each day she has a "
          "10% chance to start recovering naturally, else loses 1 hit point. Once "
          "an unaided character starts recovering naturally she is no longer in "
          "danger of losing hit points."),
    effects=["At exactly 0 hp (or stable-and-conscious in negatives)",
             "Single move action OR standard action per round, never both, "
             "no full-round actions", "Half speed",
             "Strenuous/standard action: 1 damage after completion -> dying"],
    tags=["hp_state", "action_limit", "movement"],
    see_also=["Dying", "Stable", "Staggered"]),

Condition(
    name="Dying", source=DMG,
    text=("A dying character is unconscious and near death. She has -1 to -9 "
          "current hit points. A dying character can take no actions and is "
          "unconscious. At the end of each round (starting with the round in which "
          "the character dropped below 0 hit points), the character rolls d% to see "
          "whether she becomes stable: 10% chance. If she does not, she loses 1 hit "
          "point. If a dying character reaches -10 hit points, she is dead."),
    effects=["-1 to -9 hp", "Unconscious, no actions",
             "End of each round: d%, 10% to stabilize, else lose 1 hp",
             "Dead at -10 hp"],
    tags=["hp_state", "no_actions"], see_also=["Stable", "Dead", "Unconscious"]),

Condition(
    name="Energy Drained", source=DMG,
    text=("The character gains one or more negative levels, which might permanently "
          "drain the character's levels. If the subject has at least as many "
          "negative levels as Hit Dice, he dies. Each negative level gives: -1 on "
          "attack rolls, saving throws, skill checks, ability checks; loss of 5 hit "
          "points; and -1 to effective level (for determining the power, duration, "
          "DC, and other details of spells or special abilities). In addition, a "
          "spellcaster loses one spell or spell slot from the highest spell level "
          "castable."),
    effects=["Per negative level: -1 attacks/saves/skill checks/ability checks",
             "Per negative level: -5 hp and -1 effective level",
             "Spellcaster: lose one spell/slot of highest castable level",
             "Negative levels >= HD: death"],
    tags=["negative_levels"], see_also=[]),

Condition(
    name="Entangled", source=DMG,
    text=("The character is ensnared. Being entangled impedes movement, but does "
          "not entirely prevent it unless the bonds are anchored to an immobile "
          "object or tethered by an opposing force. An entangled creature moves at "
          "half speed, cannot run or charge, and takes a -2 penalty on all attack "
          "rolls and a -4 penalty to Dexterity. Casting a spell requires a "
          "Concentration check (DC 15 + the spell's level) or the spell is lost."),
    effects=["Half speed, no run or charge",
             "-2 on all attack rolls", "-4 to Dexterity",
             "Casting: Concentration DC 15 + spell level or lose the spell",
             "If anchored/tethered: movement entirely prevented"],
    ac_melee="(-4 Dex; may affect AC)", ac_ranged="(-4 Dex; may affect AC)",
    tags=["movement"], see_also=[]),

Condition(
    name="Exhausted", source=DMG,
    text=("An exhausted character moves at half speed and takes a -6 penalty to "
          "Strength and Dexterity. After 1 hour of complete rest, an exhausted "
          "character becomes fatigued. A fatigued character becomes exhausted by "
          "doing something else that would normally cause fatigue."),
    effects=["Half speed", "-6 Str and Dex",
             "1 hour complete rest -> fatigued"],
    tags=["fatigue", "movement"], see_also=["Fatigued"]),

Condition(
    name="Fascinated", source=DMG,
    text=("A fascinated creature is entranced by a supernatural or spell effect. "
          "It stands or sits quietly, taking no actions other than to pay attention "
          "to the fascinating effect, for as long as the effect lasts. It takes a "
          "-4 penalty on skill checks made as reactions, such as Listen and Spot. "
          "Any potential threat (a hostile creature approaching) allows a new saving "
          "throw against the effect. Any obvious threat (someone drawing a weapon, "
          "casting a spell, or aiming a ranged weapon at it) automatically breaks "
          "the effect. An ally may shake the creature free as a standard action."),
    effects=["No actions except attending the effect",
             "-4 on reaction skill checks (Listen, Spot)",
             "Potential threat: new save; obvious threat: effect breaks",
             "Ally can shake free as a standard action"],
    tags=["mind", "no_actions"], see_also=[]),

Condition(
    name="Fatigued", source=DMG,
    text=("A fatigued character can neither run nor charge and takes a -2 penalty "
          "to Strength and Dexterity. Doing anything that would normally cause "
          "fatigue causes the fatigued character to become exhausted. After 8 hours "
          "of complete rest, fatigued characters are no longer fatigued."),
    effects=["No run, no charge", "-2 Str and Dex",
             "Further fatiguing activity -> exhausted",
             "8 hours complete rest ends it"],
    tags=["fatigue"], see_also=["Exhausted"]),

Condition(
    name="Flat-Footed", source=DMG,
    text=("A character who has not yet acted during a combat is flat-footed, not "
          "yet reacting normally to the situation. A flat-footed character loses "
          "his Dexterity bonus to AC (if any) and cannot make attacks of opportunity."),
    effects=["Lose Dex bonus to AC", "Cannot make attacks of opportunity"],
    ac_melee="(lose Dex bonus)", ac_ranged="(lose Dex bonus)",
    tags=["lose_dex"], see_also=[]),

Condition(
    name="Frightened", source=DMG,
    text=("A frightened creature flees from the source of its fear as best it can. "
          "If unable to flee, it may fight. A frightened creature takes a -2 "
          "penalty on all attack rolls, saving throws, skill checks, and ability "
          "checks. A frightened creature can use special abilities, including "
          "spells, to flee; indeed, it must use such means if they are the only "
          "way to escape. Frightened is like shaken, except that the creature must "
          "flee if possible. Panicked is a more extreme state of fear."),
    effects=["Must flee the fear source if possible; may fight if unable",
             "-2 on attack rolls, saves, skill checks, ability checks"],
    tags=["fear"], see_also=["Shaken", "Panicked", "Cowering"]),

Condition(
    name="Grappling", source=DMG,
    text=("Engaged in wrestling or some other form of hand-to-hand struggle with "
          "one or more attackers. A grappling character can undertake only a "
          "limited number of actions. He does not threaten any squares, and loses "
          "his Dexterity bonus to AC (if any) against opponents he isn't grappling."),
    effects=["Limited actions only", "Threatens no squares",
             "Lose Dex bonus to AC vs. opponents you are NOT grappling"],
    ac_melee="(lose Dex vs. non-grapplers)", ac_ranged="(lose Dex vs. non-grapplers)",
    tags=["grapple", "lose_dex"], see_also=["Pinned"]),

Condition(
    name="Helpless", source=DMG,
    text=("A helpless character is paralyzed, held, bound, sleeping, unconscious, "
          "or otherwise completely at an opponent's mercy. A helpless target is "
          "treated as having a Dexterity of 0 (-5 modifier). Melee attacks against "
          "a helpless target get a +4 bonus (equivalent to attacking a prone "
          "target). Ranged attacks get no special bonus. Rogues can sneak attack "
          "helpless targets. As a full-round action, an enemy can deliver a coup de "
          "grace with a melee weapon (or a bow/crossbow if adjacent): the attack "
          "automatically hits and scores a critical hit (sneak attack damage "
          "applies). If the defender survives, he must make a Fortitude save "
          "(DC 10 + damage dealt) or die. Delivering a coup de grace provokes "
          "attacks of opportunity. Creatures immune to critical hits take no "
          "critical damage and need no save."),
    effects=["Effective Dex 0 (-5 modifier)",
             "Melee attackers +4; ranged attackers no bonus",
             "Sneak-attackable",
             "Coup de grace: full-round, auto-hit auto-crit, "
             "Fort save DC 10 + damage or die; provokes AoO"],
    ac_melee="-4 (Dex 0 = -5)", ac_ranged="+0 (Dex 0 = -5)",
    tags=["helpless", "lose_dex"],
    see_also=["Paralyzed", "Unconscious", "Pinned"]),

Condition(
    name="Incorporeal", source=DMG,
    text=("Having no physical body. Incorporeal creatures are immune to all "
          "nonmagical attack forms. They can be harmed only by other incorporeal "
          "creatures, +1 or better magic weapons, spells, spell-like effects, or "
          "supernatural effects. (See Incorporeality under Special Abilities, "
          "DMG Chapter 8.)"),
    effects=["Immune to all nonmagical attack forms",
             "Harmed only by incorporeal creatures, +1 or better weapons, "
             "spells, spell-like or supernatural effects"],
    tags=["special"], see_also=[]),

Condition(
    name="Invisible", source=DMG,
    text=("Visually undetectable. An invisible creature gains a +2 bonus on attack "
          "rolls against sighted opponents, and ignores its opponents' Dexterity "
          "bonuses to AC (if any). (See Invisibility under Special Abilities, "
          "DMG Chapter 8.)"),
    effects=["+2 on attack rolls vs. sighted opponents",
             "Ignores opponents' Dex bonuses to AC"],
    ac_melee="(50% miss chance vs. you)", ac_ranged="(50% miss chance vs. you)",
    tags=["special"], see_also=["Blinded"]),

Condition(
    name="Knocked Down", source=DMG,
    text=("Depending on their size, creatures can be knocked down by winds of high "
          "velocity (Table 3-24: Wind Effects, DMG p.95). Creatures on the ground "
          "are knocked prone by the force of the wind. Flying creatures are instead "
          "blown back 1d6x10 feet."),
    effects=["Ground: knocked prone", "Flying: blown back 1d6x10 ft."],
    tags=["environment", "wind"], see_also=["Prone", "Blown Away"]),

Condition(
    name="Nauseated", source=DMG,
    text=("Experiencing stomach distress. Nauseated creatures are unable to "
          "attack, cast spells, concentrate on spells, or do anything else "
          "requiring attention. The only action such a character can take is a "
          "single move action per turn."),
    effects=["No attacks, no casting, no concentration, nothing requiring attention",
             "Single move action per turn only"],
    tags=["action_limit"], see_also=["Sickened"]),

Condition(
    name="Panicked", source=DMG,
    text=("A panicked creature must drop anything it holds and flee at top speed "
          "from the source of its fear, as well as any other dangers it encounters, "
          "along a random path. It can't take any other actions. It takes a -2 "
          "penalty on all saving throws, skill checks, and ability checks. If "
          "cornered, a panicked creature cowers and does not attack, typically "
          "using the total defense action. It can use special abilities, including "
          "spells, to flee, and must use such means if they are the only way to "
          "escape. Panicked is a more extreme state of fear than shaken or frightened."),
    effects=["Drop held items, flee at top speed along a random path",
             "No other actions", "-2 on saves, skill checks, ability checks",
             "Cornered: cowers (total defense), does not attack"],
    tags=["fear"], see_also=["Shaken", "Frightened", "Cowering"]),

Condition(
    name="Paralyzed", source=DMG,
    text=("A paralyzed character is frozen in place and unable to move or act, "
          "such as by the hold person spell. A paralyzed character has effective "
          "Dexterity and Strength scores of 0 and is helpless, but can take purely "
          "mental actions. A winged creature flying at the time it becomes "
          "paralyzed cannot flap its wings and falls. A paralyzed swimmer can't "
          "swim and may drown. A creature can move through a space occupied by a "
          "paralyzed creature — ally or not — but each such square counts as 2 squares."),
    effects=["Effective Str 0 and Dex 0; helpless",
             "Purely mental actions only",
             "Flyers fall; swimmers may drown",
             "Its space can be moved through (costs 2 squares per square)"],
    tags=["helpless", "no_actions"], see_also=["Helpless"]),

Condition(
    name="Petrified", source=DMG,
    text=("A petrified character has been turned to stone and is considered "
          "unconscious. If a petrified character cracks or breaks, but the broken "
          "pieces are joined with the body as he returns to flesh, he is unharmed. "
          "If the petrified body is incomplete when it returns to flesh, the body "
          "is likewise incomplete and the DM must assign some amount of permanent "
          "hit point loss and/or debilitation."),
    effects=["Turned to stone; treated as unconscious",
             "Breakage carried back to flesh if pieces are missing"],
    tags=["helpless"], see_also=["Unconscious"]),

Condition(
    name="Pinned", source=DMG,
    text=("Held immobile (but not helpless) in a grapple. "
          "[DM Screen AC panel: -4 vs. melee, +0 vs. ranged.]"),
    effects=["Immobile in a grapple; NOT helpless"],
    ac_melee="-4", ac_ranged="+0",
    tags=["grapple"], see_also=["Grappling", "Helpless"]),

Condition(
    name="Prone", source=DMG,
    text=("The character is on the ground. An attacker who is prone has a -4 "
          "penalty on melee attack rolls and cannot use a ranged weapon (except "
          "for a crossbow). A defender who is prone gains a +4 bonus to Armor "
          "Class against ranged attacks, but takes a -4 penalty to AC against "
          "melee attacks. Standing up is a move-equivalent action that provokes "
          "an attack of opportunity."),
    effects=["Attacking while prone: -4 melee; no ranged weapons except crossbow",
             "Defending while prone: -4 AC vs. melee, +4 AC vs. ranged",
             "Standing up: move-equivalent action, provokes AoO"],
    ac_melee="-4", ac_ranged="+4",
    tags=["position"], see_also=["Knocked Down"]),

Condition(
    name="Shaken", source=DMG,
    text=("A shaken character takes a -2 penalty on attack rolls, saving throws, "
          "skill checks, and ability checks. Shaken is a less severe state of fear "
          "than frightened or panicked."),
    effects=["-2 on attack rolls, saves, skill checks, ability checks"],
    tags=["fear"], see_also=["Frightened", "Panicked"]),

Condition(
    name="Sickened", source=DMG,
    text=("The character takes a -2 penalty on all attack rolls, weapon damage "
          "rolls, saving throws, skill checks, and ability checks."),
    effects=["-2 on attack rolls, weapon damage rolls, saves, "
             "skill checks, ability checks"],
    tags=[], see_also=["Nauseated"]),

Condition(
    name="Stable", source=DMG,
    text=("A character who was dying but who has stopped losing hit points and "
          "still has negative hit points is stable. No longer dying, but still "
          "unconscious. If stabilized by aid (Heal check or magical healing), the "
          "character no longer loses hit points and has a 10% chance each hour of "
          "becoming conscious and disabled (even with negative hit points). If "
          "self-stabilized without help, still at risk: each hour, 10% chance of "
          "becoming conscious and disabled, otherwise loses 1 hit point."),
    effects=["Negative hp, not losing hp, unconscious",
             "Aided: 10%/hour to wake disabled, no further hp loss",
             "Unaided: 10%/hour to wake disabled, else lose 1 hp"],
    tags=["hp_state"], see_also=["Dying", "Disabled"]),

Condition(
    name="Staggered", source=DMG,
    text=("A character whose nonlethal damage exactly equals his current hit "
          "points is staggered. A staggered character may take a single move "
          "action or standard action each round (but not both, nor full-round "
          "actions). A character whose current hit points exceed his nonlethal "
          "damage is no longer staggered; a character whose nonlethal damage "
          "exceeds his hit points becomes unconscious."),
    effects=["Nonlethal damage == current hp",
             "Single move OR standard action per round; no full-round actions",
             "Nonlethal > hp: unconscious; hp > nonlethal: recovered"],
    tags=["hp_state", "action_limit"], see_also=["Unconscious", "Disabled"]),

Condition(
    name="Stunned", source=DMG,
    text=("A stunned creature drops everything held, can't take actions, takes a "
          "-2 penalty to AC, and loses his Dexterity bonus to AC (if any)."),
    effects=["Drop everything held", "No actions",
             "-2 AC", "Lose Dex bonus to AC"],
    ac_melee="-2", ac_ranged="-2",
    tags=["no_actions", "lose_dex"], see_also=["Dazed"]),

Condition(
    name="Turned", source=DMG,
    text=("Affected by a turn undead attempt. Turned undead flee for 10 rounds "
          "(1 minute) by the best and fastest means available to them. If they "
          "cannot flee, they cower."),
    effects=["Flee for 10 rounds by best available means",
             "Cannot flee: cower"],
    tags=["undead"], see_also=["Cowering"]),

Condition(
    name="Unconscious", source=DMG,
    text=("Knocked out and helpless. Unconsciousness can result from having "
          "current hit points between -1 and -9, or from nonlethal damage in "
          "excess of current hit points."),
    effects=["Helpless", "Triggered at -1 to -9 hp, or nonlethal > current hp"],
    tags=["hp_state", "helpless"], see_also=["Helpless", "Dying", "Staggered"]),

# ---- DM Screen-only AC-modifier rows (PH p.151 panel) ----

Condition(
    name="Kneeling or Sitting", source=SCREEN,
    text=("DM Screen AC-modifier panel (PH p.151): a kneeling or sitting defender "
          "takes -2 to AC against melee attacks and gains +2 to AC against ranged "
          "attacks."),
    effects=["-2 AC vs. melee", "+2 AC vs. ranged"],
    ac_melee="-2", ac_ranged="+2",
    tags=["position"], see_also=["Prone"]),

Condition(
    name="Squeezing Through a Space", source=SCREEN,
    text=("DM Screen AC-modifier panel (PH p.151): a defender squeezing through a "
          "space takes -4 to AC against both melee and ranged attacks."),
    effects=["-4 AC vs. melee and ranged"],
    ac_melee="-4", ac_ranged="-4",
    tags=["position"], see_also=[]),
]

# ============================================================================
# LOOKUP
# ============================================================================

ALIASES: Dict[str, str] = {
    "grappled": "Grappling",
    "grapple": "Grappling",
    "flat footed": "Flat-Footed",
    "flatfooted": "Flat-Footed",
    "knocked prone": "Prone",
    "energy drain": "Energy Drained",
    "negative level": "Energy Drained",
    "negative levels": "Energy Drained",
    "ability damage": "Ability Damaged",
    "ability drain": "Ability Drained",
    "kneeling": "Kneeling or Sitting",
    "sitting": "Kneeling or Sitting",
    "squeezing": "Squeezing Through a Space",
    "coup de grace": "Helpless",
    "asleep": "Helpless",
    "sleeping": "Helpless",
    "stunning": "Stunned",
    "nausea": "Nauseated",
    "fear": "Shaken",
    "fatigue": "Fatigued",
    "exhaustion": "Exhausted",
}

_BY_KEY = {c.name.lower(): c for c in CONDITIONS}


def find(query: str) -> Optional[Condition]:
    """Case-insensitive lookup: exact -> alias -> unique prefix -> unique substring."""
    q = query.strip().lower()
    if q in _BY_KEY:
        return _BY_KEY[q]
    if q in ALIASES:
        return _BY_KEY[ALIASES[q].lower()]
    prefix = [c for k, c in _BY_KEY.items() if k.startswith(q)]
    if len(prefix) == 1:
        return prefix[0]
    sub = [c for k, c in _BY_KEY.items() if q in k]
    if len(sub) == 1:
        return sub[0]
    return None


def candidates(query: str) -> List[str]:
    q = query.strip().lower()
    return sorted(c.name for k, c in _BY_KEY.items() if q in k)


def search_text(term: str) -> List[Condition]:
    t = term.strip().lower()
    return [c for c in CONDITIONS
            if t in c.text.lower() or any(t in e.lower() for e in c.effects)]

# ============================================================================
# OUTPUT
# ============================================================================

def format_condition(c: Condition) -> str:
    lines = []
    lines.append("=" * 62)
    lines.append(f"CONDITION: {c.name.upper()}")
    lines.append(f"Source: {c.source}")
    lines.append("-" * 62)
    for e in c.effects:
        lines.append(f"  * {e}")
    if c.ac_melee is not None or c.ac_ranged is not None:
        lines.append(f"  AC vs. melee: {c.ac_melee or '--'}   "
                     f"AC vs. ranged: {c.ac_ranged or '--'}   [DM Screen panel]")
    lines.append("-" * 62)
    lines.append(c.text)
    if c.see_also:
        lines.append(f"See also: {', '.join(c.see_also)}")
    lines.append("=" * 62)
    return "\n".join(lines)


def format_list() -> str:
    lines = ["=" * 62, f"3.5e CONDITIONS ({len(CONDITIONS)} entries)", "=" * 62]
    for c in CONDITIONS:
        first = c.effects[0] if c.effects else ""
        lines.append(f"  {c.name:<28} {first}")
    lines.append("=" * 62)
    return "\n".join(lines)

# ============================================================================
# SELFTEST — worked examples checked against the governing pages' exact values
# ============================================================================

def selftest() -> int:
    checks = []

    def check(label, ok):
        checks.append((label, ok))
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")

    print("### conditions.py SELFTEST — values vs. DMG p.300-301 / DM Screen PH-151 panel ###\n")

    b = find("blinded")
    check("Blinded: -2 AC in effects", any("-2 AC" in e for e in b.effects))
    check("Blinded: lose Dex bonus", any("Lose Dex" in e for e in b.effects))
    check("Blinded: half speed", any("Half speed" in e for e in b.effects))
    check("Blinded: -4 Search", "-4 on Search" in " ".join(b.effects))
    check("Blinded: screen AC row -2/-2", b.ac_melee == "-2" and b.ac_ranged == "-2")

    e = find("exhausted")
    check("Exhausted: -6 Str and Dex", any("-6 Str and Dex" in x for x in e.effects))
    check("Exhausted: 1 hour rest -> fatigued", "1 hour" in e.text)

    f = find("fatigued")
    check("Fatigued: -2 Str and Dex, no run/charge",
          any("-2 Str and Dex" in x for x in f.effects) and "run" in f.text)

    st = find("stunned")
    check("Stunned: drops everything, no actions, -2 AC, lose Dex",
          all(any(k in x for x in st.effects)
              for k in ("Drop everything", "No actions", "-2 AC", "Lose Dex")))

    dz = find("dazed")
    check("Dazed: no actions, NO AC penalty",
          any("No actions" in x for x in dz.effects) and "no penalty to AC" in dz.text)

    dy = find("dying")
    check("Dying: -1 to -9 hp, 10% stabilize, dead at -10",
          "-1 to -9" in dy.text and "10%" in dy.text and "-10" in dy.text)

    stg = find("staggered")
    check("Staggered: nonlethal == current hp, single move OR standard",
          "exactly equals" in stg.text and "single move" in stg.text)

    en = find("energy drain")
    check("Energy Drained (alias): -1 rolls / -5 hp / -1 level per negative level",
          "-1 on" in en.text and "5 hit" in en.text)

    pr = find("prone")
    check("Prone: -4 melee attack; AC -4 melee / +4 ranged",
          pr.ac_melee == "-4" and pr.ac_ranged == "+4" and "-4" in pr.text)

    hl = find("helpless")
    check("Helpless: Dex 0 (-5), melee +4, coup de grace Fort DC 10 + damage",
          "Dexterity of 0" in hl.text and "+4" in hl.text and "DC 10 + damage" in hl.text)

    gp = find("grappled")
    check("Grappled -> Grappling alias; loses Dex vs. non-grapplers",
          gp.name == "Grappling" and "isn't grappling" in gp.text)

    pin = find("pinned")
    check("Pinned: immobile, not helpless; screen row -4/+0",
          "not helpless" in pin.text and pin.ac_melee == "-4" and pin.ac_ranged == "+0")

    na = find("nauseated")
    check("Nauseated: single move action only", "single move action" in na.text)

    cf = find("confused")
    check("Confused: d% table 01-10/11-20/21-50/51-70/71-100",
          all(s in cf.text for s in ("01-10", "11-20", "21-50", "51-70", "71-100")))

    df = find("deafened")
    check("Deafened: -4 init, auto-fail Listen, 20% verbal spell failure",
          "-4" in df.text and "Listen" in df.text and "20%" in df.text)

    ds = find("disabled")
    check("Disabled: 0 hp, single move OR standard, strenuous act -> 1 damage",
          "0 hit points" in ds.text and "1 point of damage" in ds.text)

    kn = find("kneeling")
    check("Kneeling/Sitting (screen-only): -2 melee / +2 ranged",
          kn.ac_melee == "-2" and kn.ac_ranged == "+2")

    sq = find("squeezing")
    check("Squeezing (screen-only): -4/-4", sq.ac_melee == "-4" and sq.ac_ranged == "-4")

    check("Every DMG Condition Summary entry present (38 DMG + 2 screen rows = 40)",
          len(CONDITIONS) == 40)

    names = {c.name for c in CONDITIONS}
    dmg_list = {"Ability Damaged", "Ability Drained", "Blinded", "Blown Away",
                "Checked", "Confused", "Cowering", "Dazed", "Dazzled", "Dead",
                "Deafened", "Disabled", "Dying", "Energy Drained", "Entangled",
                "Exhausted", "Fascinated", "Fatigued", "Flat-Footed", "Frightened",
                "Grappling", "Helpless", "Incorporeal", "Invisible", "Knocked Down",
                "Nauseated", "Panicked", "Paralyzed", "Petrified", "Pinned",
                "Prone", "Shaken", "Sickened", "Stable", "Staggered", "Stunned",
                "Turned", "Unconscious"}
    check("DMG name roster complete (38/38)", dmg_list <= names)

    failed = [l for l, ok in checks if not ok]
    print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed.")
    if failed:
        print("FAILED:", *failed, sep="\n  - ")
        return 1
    return 0

# ============================================================================
# CLI
# ============================================================================

def main():
    p = argparse.ArgumentParser(
        description="D&D 3.5e condition reference (DMG p.300-301 + DM Screen AC panel).")
    p.add_argument("names", nargs="*", help="Condition name(s) to look up.")
    p.add_argument("--list", action="store_true", help="List every condition.")
    p.add_argument("--search", help="Full-text search across condition rules.")
    p.add_argument("--json", action="store_true",
                   help="Emit matched condition(s) as JSON instead of text.")
    p.add_argument("--selftest", action="store_true",
                   help="Verify entries against the governing pages' exact values.")
    args = p.parse_args()

    if args.selftest:
        sys.exit(selftest())

    if args.list:
        print(format_list())
        return

    if args.search:
        hits = search_text(args.search)
        if not hits:
            print(f"No condition text matches {args.search!r}.")
            return
        print(f"{len(hits)} condition(s) match {args.search!r}:")
        for c in hits:
            print(f"  - {c.name}")
        return

    if not args.names:
        p.print_help()
        return

    out_json = []
    for name in args.names:
        c = find(name)
        if c is None:
            near = candidates(name)
            print(f"No unique match for {name!r}."
                  + (f" Candidates: {', '.join(near)}" if near else ""))
            continue
        if args.json:
            out_json.append(asdict(c))
        else:
            print(format_condition(c))
    if args.json and out_json:
        print(json.dumps(out_json if len(out_json) > 1 else out_json[0], indent=2))


if __name__ == "__main__":
    main()
