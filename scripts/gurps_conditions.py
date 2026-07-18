#!/usr/bin/env python3
"""
gurps_conditions.py — GURPS 4e condition / state reference
The New Path campaign engine (the-new-path-engine)

GOVERNING SOURCES (read, not memory):
    GURPS 4e Basic Set: Campaigns
    (I:\\Sourcebooks\\GURPS\\GURPS 4e\\GURPS 4e - Basic Set - Campaigns.pdf,
     text layer read directly; page cites are BOOK pages, B###)
      B419  General Injury (HP thresholds), Shock
      B420  Major Wounds, Knockdown and Stunning, Effects of Stun,
            Crippling Injury (+ Bleeding optional rule sidebar)
      B421  Crippling effects per body part, Temporary Attribute Penalties
      B423  Mortal Wounds, Death, Recovering from Unconsciousness
      B426  Lost Fatigue Points (FP thresholds)
      B428  Afflictions: Irritating Conditions
      B428-429  Afflictions: Incapacitating Conditions
      B429  Mortal Conditions (Coma, Heart Attack)
      B551  Posture Table

DESIGN CONTRACT (repo README):
    - Stateless resolver: flags in, text out. No state file, no dice.
    - Visible output: every lookup prints a ready-to-paste block.
    - No cross-imports.
    - --selftest runs worked examples against the governing pages' exact values.

USAGE
    python3 gurps_conditions.py stunned
    python3 gurps_conditions.py "severe pain" agony
    python3 gurps_conditions.py --list
    python3 gurps_conditions.py --search "active defense"
    python3 gurps_conditions.py --json paralysis
    python3 gurps_conditions.py --state --hp-max 14 --hp -3
    python3 gurps_conditions.py --state --hp-max 14 --hp 2 --fp-max 12 --fp 3
    python3 gurps_conditions.py --selftest
"""

import argparse
import json
import math
import sys
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict

# ============================================================================
# DATA MODEL
# ============================================================================

@dataclass
class Condition:
    name: str
    source: str                       # book page citation
    category: str                     # hp-state | fp-state | wound | stun |
                                      # irritating | incapacitating | mortal |
                                      # crippling | posture | recovery
    text: str                         # rules text per the source
    effects: List[str]                # bullet mechanics, verbatim-derived
    tags: List[str] = field(default_factory=list)
    see_also: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)

# ============================================================================
# CONDITION DATA — B419-B429, B551
# ============================================================================

_INCAP_PREFIX = ("No voluntary action for the duration; effectively stunned "
                 "(-4 to active defenses); in combat you must Do Nothing on "
                 "your turn. [B428]")

CONDITIONS: List[Condition] = [

    # ---------------- HP STATES (B419) ----------------
    Condition(
        name="Reeling",
        source="B419 (General Injury: Lost Hit Points)",
        category="hp-state",
        text=("Less than 1/3 your HP left: you are reeling from your wounds. "
              "Halve your Move and Dodge (round up). All low-HP effects are "
              "cumulative."),
        effects=["Half Move (round up)", "Half Dodge (round up)"],
        tags=["hp", "threshold"],
        see_also=["Collapse Risk (0 HP)", "Death Check (-1xHP)"],
    ),
    Condition(
        name="Collapse Risk (0 HP)",
        source="B419 (General Injury: Lost Hit Points)",
        category="hp-state",
        text=("At 0 HP or less you are in immediate danger of collapse. In "
              "addition to reeling, make a HT roll at the start of your next "
              "turn, at -1 per full multiple of HP below zero. Failure means "
              "you fall unconscious. Success means you can act normally, but "
              "must roll again every turn to continue functioning. Exception: "
              "if you choose Do Nothing on your turn and attempt no defense "
              "rolls, you can remain conscious without rolling."),
        effects=[
            "All Reeling effects (half Move and Dodge)",
            "HT roll at start of each turn, -1 per full multiple of HP below 0",
            "Failure -> unconscious",
            "Do Nothing + no defenses = no roll required that turn",
        ],
        tags=["hp", "threshold", "ht-roll"],
        see_also=["Reeling", "Death Check (-1xHP)", "Recovering from Unconsciousness"],
    ),
    Condition(
        name="Death Check (-1xHP)",
        source="B419 (General Injury: Lost Hit Points)",
        category="hp-state",
        text=("At -1xHP, in addition to the above effects, make an immediate "
              "HT roll or die. If you fail by only 1 or 2, you are dying but "
              "not dead: mortally wounded (B423). If you succeed, you can "
              "still talk and fight (until you fail a consciousness roll and "
              "collapse). Roll again each time you suffer injury equal to a "
              "further multiple of your HP (at -2xHP, -3xHP, -4xHP)."),
        effects=[
            "Immediate HT roll or die",
            "Fail by 1-2 -> Mortal Wound instead of death",
            "New death check at each further -1xHP multiple",
        ],
        tags=["hp", "threshold", "ht-roll", "death"],
        see_also=["Mortal Wound", "Automatic Death (-5xHP)"],
    ),
    Condition(
        name="Automatic Death (-5xHP)",
        source="B419 (General Injury: Lost Hit Points)",
        category="hp-state",
        text=("At -5xHP you die immediately: you have lost a total of 6 times "
              "your HP. Nobody can survive that much injury. At -10xHP: total "
              "bodily destruction, if this makes sense given the damage "
              "source — matters where resurrection or reanimation is possible."),
        effects=[
            "-5xHP: dead, no roll",
            "-10xHP: total bodily destruction (no body to revive)",
        ],
        tags=["hp", "threshold", "death"],
        aliases=["Dead", "Total Bodily Destruction"],
    ),

    # ---------------- SHOCK (B419) ----------------
    Condition(
        name="Shock",
        source="B419 (Shock)",
        category="wound",
        text=("Whenever you suffer injury, reduce your DX and IQ by the HP "
              "lost — to a maximum penalty of -4 — on your next turn only. "
              "Shock affects DX- and IQ-based skills, but not active defenses "
              "or other defensive reactions. High HP: with 20+ HP the penalty "
              "is -1 per HP/10 of injury (drop fractions), max still -4."),
        effects=[
            "-DX and -IQ equal to HP lost this turn (max -4), next turn only",
            "Does NOT affect active defenses or defensive reactions",
            "20+ HP: -1 per (HP/10) injury instead, max -4",
        ],
        tags=["injury", "penalty", "temporary"],
        see_also=["Knockdown and Stunning", "Major Wound"],
    ),

    # ---------------- WOUNDS AND STUN (B420) ----------------
    Condition(
        name="Major Wound",
        source="B420 (Major Wounds)",
        category="wound",
        text=("A major wound is any single injury of greater than 1/2 your "
              "HP. A lesser injury that cripples a body part also counts. Any "
              "major wound requires a HT roll to avoid knockdown and "
              "stunning."),
        effects=[
            "Single injury > HP/2",
            "Crippling injury always counts as a major wound",
            "Triggers HT roll vs. knockdown and stunning",
        ],
        tags=["injury", "trigger"],
        see_also=["Knockdown and Stunning", "Crippling Injury"],
    ),
    Condition(
        name="Knockdown and Stunning",
        source="B420 (Knockdown and Stunning)",
        category="stun",
        text=("On any major wound, or a head (skull, face, eye) or vitals hit "
              "for enough injury to cause a shock penalty, make an immediate "
              "HT roll. Modifiers: -5 for a major wound to the face, vitals, "
              "or groin (humanoid male); -10 for a major wound to the skull "
              "or eye; +3 High Pain Threshold; -4 Low Pain Threshold. "
              "Success: no penalty beyond ordinary shock. Failure: stunned, "
              "fall prone, drop anything held (knockdown). Failure by 5+ or "
              "critical failure: unconscious."),
        effects=[
            "HT roll; -5 face/vitals/groin major wound; -10 skull/eye major wound",
            "+3 High Pain Threshold; -4 Low Pain Threshold",
            "Fail -> stunned + knocked prone + drop held items",
            "Fail by 5+ or critical failure -> unconscious",
        ],
        tags=["ht-roll", "stun", "prone"],
        see_also=["Stunned", "Major Wound", "Recovering from Unconsciousness"],
    ),
    Condition(
        name="Stunned",
        source="B420 (Effects of Stun)",
        category="stun",
        text=("If stunned, you must Do Nothing on your next turn. You may "
              "perform any active defense while stunned, but your defense "
              "rolls are at -4 and you cannot retreat. At the end of your "
              "turn, roll against HT: success recovers you; failure means "
              "another Do Nothing turn and another roll, until you recover. "
              "Mental Stun (e.g. from surprise) works the same but recovery "
              "is an IQ roll, not HT — you're confused, not hurt."),
        effects=[
            "Must Do Nothing on your turn",
            "Active defenses allowed at -4; no retreat",
            "HT roll at end of each turn to recover (IQ roll for mental stun)",
        ],
        tags=["stun", "recovery-roll"],
        see_also=["Knockdown and Stunning"],
        aliases=["Stun", "Mental Stun", "Physical Stun"],
    ),

    # ---------------- CRIPPLING (B420-421) ----------------
    Condition(
        name="Crippling Injury",
        source="B420-421 (Crippling Injury)",
        category="crippling",
        text=("A single injury over a threshold cripples the body part. "
              "Limb (arm, leg, wing, striker, prehensile tail): over HP/2. "
              "Extremity (hand, foot, tail, fin, extra head): over HP/3. "
              "Eye: over HP/10. Injury to a limb/extremity can never exceed "
              "the minimum required to cripple it (eyes excepted). If injury "
              "before that cap was at least twice the crippling threshold, "
              "the part is destroyed (dismemberment). Any crippling injury "
              "is also a major wound (knockdown/stun roll). Effects: "
              "Hand — drop items in that hand, cannot hold anything, shield "
              "on that arm can block but not attack. Arm — as hand, cannot "
              "carry anything with it; shield stays but cannot block, -1 DB. "
              "Foot — you fall; cannot stand/walk unaided; may kneel or sit. "
              "Leg — you fall; fight from sitting or lying posture. "
              "Eye — blind in that eye."),
        effects=[
            "Limb: injury > HP/2 | Extremity: > HP/3 | Eye: > HP/10",
            "Injury capped at minimum needed to cripple (except eyes)",
            "2x threshold before cap -> dismemberment (destroyed)",
            "Always a major wound: HT roll vs. knockdown/stunning",
            "Hand: drop + cannot hold | Arm: also cannot carry, shield -1 DB no block",
            "Foot/Leg: fall down, posture restricted | Eye: blind that eye",
        ],
        tags=["injury", "hit-location"],
        see_also=["Major Wound", "Knockdown and Stunning"],
        aliases=["Crippled", "Dismemberment"],
    ),
    Condition(
        name="Bleeding",
        source="B420 (Bleeding — optional rule)",
        category="wound",
        text=("Optional rule. If injured, at the end of every minute make a "
              "HT roll at -1 per 5 HP lost. Failure: bleed 1 HP. Critical "
              "failure: bleed 3 HP. Critical success: bleeding stops. "
              "Ordinary success: no bleeding this minute, roll again next. "
              "Three consecutive non-bleeding minutes ends it; otherwise a "
              "First Aid roll is needed. Cutting, impaling, and piercing "
              "wounds usually bleed; crushing generally doesn't; minor "
              "burn/corrosion cauterizes (unless a major wound)."),
        effects=[
            "HT roll per minute at -1 per 5 HP lost",
            "Fail: -1 HP | Crit fail: -3 HP | Crit success: stops",
            "3 clean minutes ends it; else First Aid roll",
        ],
        tags=["optional", "ht-roll", "injury"],
        see_also=["Major Wound"],
    ),

    # ---------------- MORTAL / DEATH / RECOVERY (B423) ----------------
    Condition(
        name="Mortal Wound",
        source="B423 (Mortal Wounds)",
        category="mortal",
        text=("Fail a HT roll to avoid death by 1 or 2: mortally wounded. "
              "Instantly incapacitated; conscious or not is GM's decision. "
              "Any further failed death check kills you. Roll HT every "
              "half-hour: failure = death; success = linger another "
              "half-hour; critical success = no longer mortally wounded "
              "(still incapacitated). TL6+ trauma maintenance: roll the "
              "higher of HT or caregiver's Physician hourly instead (daily "
              "on life support). On recovery, roll HT; failure = lose 1 HT "
              "permanently."),
        effects=[
            "Instantly incapacitated",
            "HT roll per half-hour or die (crit success clears mortal status)",
            "Any further failed death check = death",
            "Surgery can stabilize (B424); recovery risks -1 HT permanently",
        ],
        tags=["death", "ht-roll", "incapacitated"],
        see_also=["Death Check (-1xHP)"],
        aliases=["Mortally Wounded", "Dying"],
    ),
    Condition(
        name="Recovering from Unconsciousness",
        source="B423 (Recovering from Unconsciousness)",
        category="recovery",
        text=("With 1+ HP remaining: awaken automatically in 15 minutes. At "
              "0 HP to above -1xHP: HT roll to awaken every hour; once awake "
              "you act normally (no per-second rolls unless newly injured), "
              "though still reeling. At -1xHP or below: a single HT roll to "
              "awaken after 12 hours; on failure you will not wake without "
              "medical treatment, and must roll HT every 12 hours or die."),
        effects=[
            "1+ HP: wake in 15 minutes",
            "0 to > -1xHP: hourly HT roll to wake",
            "-1xHP or worse: one HT roll at 12h; fail -> medical care or die (HT/12h)",
        ],
        tags=["recovery", "ht-roll", "unconscious"],
        see_also=["Collapse Risk (0 HP)", "Mortal Wound"],
        aliases=["Unconscious (injury)"],
    ),

    # ---------------- FP STATES (B426) ----------------
    Condition(
        name="Very Tired",
        source="B426 (Lost Fatigue Points)",
        category="fp-state",
        text=("Less than 1/3 your FP left: you are very tired. Halve your "
              "Move, Dodge, and ST (round up). This does not affect ST-based "
              "quantities such as HP and damage. All low-FP effects are "
              "cumulative."),
        effects=[
            "Half Move, Dodge, and ST (round up)",
            "HP and damage NOT affected by the ST halving",
        ],
        tags=["fp", "threshold"],
        see_also=["FP Collapse Risk (0 FP)"],
    ),
    Condition(
        name="FP Collapse Risk (0 FP)",
        source="B426 (Lost Fatigue Points)",
        category="fp-state",
        text=("At 0 FP or less you are on the verge of collapse. Each "
              "further FP lost also causes 1 HP of injury. To do anything "
              "besides talk or rest, make a Will roll — in combat, before "
              "each maneuver other than Do Nothing. Failure: collapse, "
              "incapacitated until you recover to positive FP. Critical "
              "failure: immediate HT roll; fail = heart attack (B429)."),
        effects=[
            "All Very Tired effects (half Move, Dodge, ST)",
            "Each further FP lost also costs 1 HP",
            "Will roll to act (per maneuver in combat, except Do Nothing)",
            "Fail -> collapse | Crit fail -> HT roll or Heart Attack",
        ],
        tags=["fp", "threshold", "will-roll"],
        see_also=["Very Tired", "FP Unconsciousness (-1xFP)", "Heart Attack"],
    ),
    Condition(
        name="FP Unconsciousness (-1xFP)",
        source="B426 (Lost Fatigue Points)",
        category="fp-state",
        text=("At -1xFP you fall unconscious. While unconscious you recover "
              "FP at the normal resting rate and awaken at positive FP. FP "
              "can never fall below -1xFP: any further FP cost comes off "
              "your HP instead."),
        effects=[
            "Unconscious; wake at positive FP",
            "FP floor is -1xFP; further FP costs become HP loss",
        ],
        tags=["fp", "threshold", "unconscious"],
        see_also=["FP Collapse Risk (0 FP)"],
    ),

    # ---------------- IRRITATING CONDITIONS (B428) ----------------
    Condition(
        name="Coughing",
        source="B428 (Afflictions: Irritating Conditions)",
        category="irritating",
        text=("Coughing or Sneezing: you are at -3 to DX and -1 to IQ, and "
              "cannot use Stealth."),
        effects=["-3 DX", "-1 IQ", "No Stealth"],
        tags=["affliction"],
        aliases=["Sneezing", "Coughing or Sneezing"],
    ),
    Condition(
        name="Drowsy",
        source="B428 (Afflictions: Irritating Conditions)",
        category="irritating",
        text=("On the verge of falling asleep. Make a Will roll every two "
              "hours spent inactive. Failure: fall asleep until awakened or "
              "fully rested. Success: -2 to DX, IQ, and self-control rolls."),
        effects=[
            "Will roll per 2 inactive hours; fail = asleep",
            "On success: -2 DX, IQ, and self-control rolls",
        ],
        tags=["affliction", "will-roll"],
    ),
    Condition(
        name="Tipsy",
        source="B428 (Afflictions: Irritating Conditions)",
        category="irritating",
        text=("Slightly intoxicated: -1 to DX and IQ, and -2 to self-control "
              "rolls except those to resist Cowardice. Reduce Shyness by one "
              "level, if you have it."),
        effects=["-1 DX and IQ", "-2 self-control (except vs. Cowardice)",
                 "Shyness reduced one level"],
        tags=["affliction", "intoxication"],
    ),
    Condition(
        name="Drunk",
        source="B428 (Afflictions: Irritating Conditions)",
        category="irritating",
        text=("Highly intoxicated: -2 to DX and IQ, and -4 to self-control "
              "rolls except those to resist Cowardice. Reduce Shyness by two "
              "levels, if you have it."),
        effects=["-2 DX and IQ", "-4 self-control (except vs. Cowardice)",
                 "Shyness reduced two levels"],
        tags=["affliction", "intoxication"],
    ),
    Condition(
        name="Euphoria",
        source="B428 (Afflictions: Irritating Conditions)",
        category="irritating",
        text=("You have a -3 penalty to all DX, IQ, skill, and self-control "
              "rolls."),
        effects=["-3 to all DX, IQ, skill, and self-control rolls"],
        tags=["affliction"],
    ),
    Condition(
        name="Nauseated",
        source="B428 (Afflictions: Irritating Conditions)",
        category="irritating",
        text=("-2 to all attribute and skill rolls, and -1 to active "
              "defenses. Roll vs. HT after eating, foul odors, a failed "
              "Fright Check, being stunned, and every hour in free fall or "
              "motion-sickness situations (-2 for a rich meal in the past "
              "hour; +2 for anti-nausea remedies). On a failure, you vomit "
              "for (25 - HT) seconds — treat as Retching."),
        effects=[
            "-2 all attribute and skill rolls",
            "-1 active defenses",
            "HT roll vs. vomiting on triggers; fail -> Retching (25-HT) seconds",
        ],
        tags=["affliction", "ht-roll"],
        see_also=["Retching"],
    ),
    Condition(
        name="Moderate Pain",
        source="B428 (Afflictions: Irritating Conditions — Pain)",
        category="irritating",
        text=("Pain gives a penalty to all DX, IQ, skill, and self-control "
              "rolls: -2 for Moderate Pain. High Pain Threshold halves these "
              "penalties; Low Pain Threshold doubles them."),
        effects=["-2 to all DX, IQ, skill, and self-control rolls",
                 "HPT halves; LPT doubles"],
        tags=["affliction", "pain"],
        see_also=["Severe Pain", "Terrible Pain"],
    ),
    Condition(
        name="Severe Pain",
        source="B428 (Afflictions: Irritating Conditions — Pain)",
        category="irritating",
        text=("Pain gives a penalty to all DX, IQ, skill, and self-control "
              "rolls: -4 for Severe Pain. High Pain Threshold halves these "
              "penalties; Low Pain Threshold doubles them."),
        effects=["-4 to all DX, IQ, skill, and self-control rolls",
                 "HPT halves; LPT doubles"],
        tags=["affliction", "pain"],
        see_also=["Moderate Pain", "Terrible Pain"],
    ),
    Condition(
        name="Terrible Pain",
        source="B428 (Afflictions: Irritating Conditions — Pain)",
        category="irritating",
        text=("Pain gives a penalty to all DX, IQ, skill, and self-control "
              "rolls: -6 for Terrible Pain. High Pain Threshold halves these "
              "penalties; Low Pain Threshold doubles them."),
        effects=["-6 to all DX, IQ, skill, and self-control rolls",
                 "HPT halves; LPT doubles"],
        tags=["affliction", "pain"],
        see_also=["Moderate Pain", "Severe Pain"],
    ),

    # ---------------- INCAPACITATING CONDITIONS (B428-429) ----------------
    Condition(
        name="Agony",
        source="B428-429 (Afflictions: Incapacitating Conditions)",
        category="incapacitating",
        text=(_INCAP_PREFIX + " Conscious but in such terrible pain you can "
              "do nothing but moan or scream. If standing or sitting, you "
              "fall down. Lose 1 FP per minute or fraction. Afterward, "
              "credible threats of resumed pain give +3 to Interrogation and "
              "Intimidation against you. LPT doubles the FP loss and torture "
              "bonus; HPT lets you function at -3 DX and IQ."),
        effects=[
            "Incapacitated + effectively stunned (-4 defenses, Do Nothing)",
            "Fall down; 1 FP lost per minute",
            "+3 Interrogation/Intimidation vs. you afterward",
            "LPT doubles loss/bonus; HPT: function at -3 DX and IQ",
        ],
        tags=["affliction", "incapacitating", "pain"],
        see_also=["Ecstasy"],
    ),
    Condition(
        name="Choking",
        source="B428-429 (Afflictions: Incapacitating Conditions)",
        category="incapacitating",
        text=(_INCAP_PREFIX + " Unable to breathe or speak; you may do "
              "nothing but drop. Suffer suffocation (B436) while it lasts. "
              "A lodged object can be cleared with a First Aid roll (-2 "
              "before TL7), 2 seconds per attempt. Doesn't Breathe or Injury "
              "Tolerance (Homogenous) makes you immune."),
        effects=[
            "Incapacitated + effectively stunned (-4 defenses, Do Nothing)",
            "Cannot breathe or speak; suffocating (B436)",
            "First Aid roll (2 sec/attempt, -2 pre-TL7) clears lodged object",
        ],
        tags=["affliction", "incapacitating", "suffocation"],
    ),
    Condition(
        name="Daze",
        source="B428-429 (Afflictions: Incapacitating Conditions)",
        category="incapacitating",
        text=(_INCAP_PREFIX + " Conscious — you remain upright if standing — "
              "but you can do nothing. If struck, slapped, or shaken, you "
              "recover on your next turn."),
        effects=[
            "Incapacitated + effectively stunned (-4 defenses, Do Nothing)",
            "Remain standing; being struck/slapped/shaken ends it next turn",
        ],
        tags=["affliction", "incapacitating"],
        aliases=["Dazed"],
    ),
    Condition(
        name="Ecstasy",
        source="B428-429 (Afflictions: Incapacitating Conditions)",
        category="incapacitating",
        text=(_INCAP_PREFIX + " Incapacitated with overwhelming pleasure. "
              "Treat as Agony, but pain thresholds have no effect — and "
              "instead of a torture bonus, someone offering to continue the "
              "pleasure gets +3 to any Influence roll. Killjoy grants "
              "immunity."),
        effects=[
            "Incapacitated + effectively stunned (-4 defenses, Do Nothing)",
            "As Agony (fall, 1 FP/min); HPT/LPT irrelevant",
            "+3 Influence rolls for offers to continue; Killjoy immune",
        ],
        tags=["affliction", "incapacitating"],
        see_also=["Agony"],
    ),
    Condition(
        name="Hallucinating",
        source="B429 (Afflictions: Incapacitating Conditions)",
        category="incapacitating",
        text=("You can try to act, but must roll vs. Will before each "
              "success roll. Success: 2d seconds of disorientation at -2 on "
              "success rolls. Failure: hallucinate for 1d minutes at -5. "
              "Critical failure: freak out for 3d minutes — you might do "
              "anything (GM rolls 3d; higher = more dangerous)."),
        effects=[
            "Will roll before each success roll",
            "Success: -2 (2d seconds) | Failure: -5, 1d minutes",
            "Crit failure: freak out 3d minutes",
        ],
        tags=["affliction", "incapacitating", "will-roll"],
    ),
    Condition(
        name="Paralysis",
        source="B429 (Afflictions: Incapacitating Conditions)",
        category="incapacitating",
        text=(_INCAP_PREFIX + " You cannot move any voluntary muscles, and "
              "fall over if not in a balanced position. You remain "
              "conscious, and can still use advantages or spells that "
              "require neither speech nor movement."),
        effects=[
            "Incapacitated + effectively stunned (-4 defenses, Do Nothing)",
            "No voluntary movement; fall if unbalanced",
            "Conscious; no-speech/no-movement abilities still usable",
        ],
        tags=["affliction", "incapacitating"],
        aliases=["Paralyzed"],
    ),
    Condition(
        name="Retching",
        source="B429 (Afflictions: Incapacitating Conditions)",
        category="incapacitating",
        text=("Conscious but vomiting (or dry heaves). You can try to act at "
              "-5 to DX, IQ, and Per, and automatically fail any action "
              "requiring a Concentrate maneuver. At the end of the spell, "
              "lose 1 FP and any benefit from recent meals or oral "
              "medication."),
        effects=[
            "-5 DX, IQ, and Per",
            "Auto-fail Concentrate-maneuver actions",
            "End: -1 FP; recent meals/oral meds lost",
        ],
        tags=["affliction", "incapacitating"],
        see_also=["Nauseated"],
    ),
    Condition(
        name="Seizure",
        source="B429 (Afflictions: Incapacitating Conditions)",
        category="incapacitating",
        text=(_INCAP_PREFIX + " A fit: limbs tremble uncontrollably, you "
              "fall down if standing, and you cannot speak or think clearly. "
              "You can do nothing. At the end of the seizure, lose 1d FP."),
        effects=[
            "Incapacitated + effectively stunned (-4 defenses, Do Nothing)",
            "Fall if standing; no speech or clear thought",
            "End: lose 1d FP",
        ],
        tags=["affliction", "incapacitating"],
    ),
    Condition(
        name="Unconsciousness (affliction)",
        source="B429 (Afflictions: Incapacitating Conditions)",
        category="incapacitating",
        text=("You are knocked out, just as if you had suffered injury. See "
              "Recovering from Unconsciousness (B423)."),
        effects=["Knocked out as if by injury"],
        tags=["affliction", "incapacitating", "unconscious"],
        see_also=["Recovering from Unconsciousness"],
    ),

    # ---------------- MORTAL CONDITIONS (B429) ----------------
    Condition(
        name="Coma",
        source="B429 (Afflictions: Mortal Conditions)",
        category="mortal",
        text=("Collapse as if wounded to -1xHP and passed out. A single HT "
              "roll to awaken after 12 hours; on failure you will not "
              "recover without medical treatment, and must roll HT every 12 "
              "hours — any failure means death."),
        effects=[
            "Unconscious as at -1xHP",
            "One HT roll at 12h; fail -> medical care required, HT/12h or die",
        ],
        tags=["affliction", "mortal", "unconscious"],
        see_also=["Recovering from Unconsciousness"],
    ),
    Condition(
        name="Heart Attack",
        source="B429 (Afflictions: Mortal Conditions)",
        category="mortal",
        text=("Cardiac arrest: immediately drop to -1xFP. Regardless of "
              "current HP, you die in HT/3 minutes unless resuscitated "
              "(B425). If you survive, you are at 0 HP or your current HP, "
              "whichever is worse. Injury Tolerance (Diffuse, Homogenous, or "
              "No Vitals) grants immunity."),
        effects=[
            "Drop to -1xFP immediately",
            "Death in HT/3 minutes without resuscitation",
            "Survival: HP becomes 0 or current, whichever is worse",
        ],
        tags=["affliction", "mortal", "fp"],
        see_also=["FP Collapse Risk (0 FP)"],
        aliases=["Cardiac Arrest"],
    ),

    # ---------------- POSTURES (B551) ----------------
    Condition(
        name="Standing",
        source="B551 (Posture Table)",
        category="posture",
        text="Attack normal; Defense normal; ranged Target normal; Movement normal, may sprint.",
        effects=["Melee attack: normal", "Defense: normal",
                 "Ranged target mod: normal", "Movement: normal; may sprint"],
        tags=["posture"],
    ),
    Condition(
        name="Crouching",
        source="B551 (Posture Table)",
        category="posture",
        text="Attack -2; Defense normal; ranged Target -2; Movement 2/3 (+1/2 per hex).",
        effects=["Melee attack: -2", "Defense: normal",
                 "Ranged target mod: -2 (torso/groin/legs)", "Movement: 2/3"],
        tags=["posture"],
    ),
    Condition(
        name="Kneeling",
        source="B551 (Posture Table)",
        category="posture",
        text="Attack -2; Defense -2; ranged Target -2; Movement 1/3 (+2 per hex).",
        effects=["Melee attack: -2", "Defense: -2",
                 "Ranged target mod: -2 (torso/groin/legs)", "Movement: 1/3"],
        tags=["posture"],
    ),
    Condition(
        name="Crawling",
        source="B551 (Posture Table)",
        category="posture",
        text=("Attack -4 (reach C melee only); Defense -3; ranged Target -2 "
              "(torso half-exposed at -2 vs. same/lower distant attackers, "
              "no groin/leg/foot shots); Movement 1/3 (+2 per hex); occupies "
              "two hexes."),
        effects=["Melee attack: -4, reach C only", "Defense: -3",
                 "Ranged target mod: -2, protected footprint", "Movement: 1/3"],
        tags=["posture"],
    ),
    Condition(
        name="Sitting",
        source="B551 (Posture Table)",
        category="posture",
        text="Attack -2; Defense -2; ranged Target -2; Movement none.",
        effects=["Melee attack: -2", "Defense: -2",
                 "Ranged target mod: -2 (torso/groin/legs)", "Movement: none"],
        tags=["posture"],
    ),
    Condition(
        name="Lying Down",
        source="B551 (Posture Table)",
        category="posture",
        text=("Attack -4; Defense -3; ranged Target -2 (torso half-exposed "
              "at -2 vs. same/lower distant attackers, no groin/leg/foot "
              "shots); Movement 1 yard/second; occupies two hexes."),
        effects=["Melee attack: -4", "Defense: -3",
                 "Ranged target mod: -2, protected footprint",
                 "Movement: 1 yard/second"],
        tags=["posture"],
        aliases=["Prone", "Lying"],
    ),
]

# ============================================================================
# INDEX
# ============================================================================

_INDEX: Dict[str, Condition] = {}
for _c in CONDITIONS:
    _INDEX[_c.name.lower()] = _c
    for _a in _c.aliases:
        _INDEX[_a.lower()] = _c


def lookup(name: str) -> Optional[Condition]:
    key = name.strip().lower()
    if key in _INDEX:
        return _INDEX[key]
    hits = [c for k, c in _INDEX.items() if key in k]
    uniq = {id(c): c for c in hits}
    if len(uniq) == 1:
        return next(iter(uniq.values()))
    return None


# ============================================================================
# STATE CALCULATOR — B419 / B426 thresholds from live totals
# ============================================================================

def hp_state(hp_max: int, hp: int) -> List[str]:
    """Active HP-threshold effects for a current HP total. B419."""
    out = []
    third = hp_max / 3.0
    if hp < third:
        out.append("REELING (< 1/3 HP): half Move and Dodge, round up  [B419]")
    if hp <= 0:
        mult_below = abs(hp) // hp_max if hp < 0 else 0
        out.append(
            f"COLLAPSE RISK (<= 0 HP): HT roll at start of each turn at "
            f"-{mult_below} (-1 per full xHP below zero); fail = unconscious; "
            f"Do Nothing + no defenses skips the roll  [B419]")
    if hp <= -1 * hp_max:
        crossed = abs(hp) // hp_max
        thresholds = ", ".join(f"-{m}xHP ({-m * hp_max})"
                               for m in range(1, crossed + 1))
        out.append(
            f"DEATH CHECK territory: immediate HT roll or die at each of "
            f"{thresholds}; fail by 1-2 = Mortal Wound  [B419]")
        nxt = (crossed + 1) * hp_max
        out.append(f"Next death check at -{crossed + 1}xHP ({-nxt})")
    if hp <= -5 * hp_max:
        out.append(f"DEAD automatically (-5xHP = {-5 * hp_max})  [B419]")
    if hp <= -10 * hp_max:
        out.append("TOTAL BODILY DESTRUCTION (-10xHP)  [B419]")
    if not out:
        out.append("No HP-threshold effects (at or above 1/3 HP).")
    return out


def fp_state(fp_max: int, fp: int) -> List[str]:
    """Active FP-threshold effects for a current FP total. B426."""
    out = []
    third = fp_max / 3.0
    if fp < third:
        out.append("VERY TIRED (< 1/3 FP): half Move, Dodge, and ST "
                   "(round up); HP/damage unaffected  [B426]")
    if fp <= 0:
        out.append("FP COLLAPSE RISK (<= 0 FP): each further FP lost also "
                   "costs 1 HP; Will roll to act (per maneuver in combat); "
                   "crit fail -> HT roll or Heart Attack  [B426]")
    if fp <= -1 * fp_max:
        out.append(f"UNCONSCIOUS (-1xFP = {-fp_max}): FP floor reached; "
                   "further FP costs come off HP  [B426]")
    if not out:
        out.append("No FP-threshold effects (at or above 1/3 FP).")
    return out


# ============================================================================
# OUTPUT
# ============================================================================

BAR = "=" * 62
SUB = "-" * 62


def print_condition(c: Condition) -> None:
    print(BAR)
    print(f"CONDITION: {c.name.upper()}   [{c.category}]")
    print(f"Source: GURPS 4e Basic Set: Campaigns, {c.source}")
    print(SUB)
    for e in c.effects:
        print(f"  * {e}")
    print(SUB)
    print(c.text)
    if c.see_also:
        print("See also: " + ", ".join(c.see_also))
    print(BAR)


def print_state(hp_max: Optional[int], hp: Optional[int],
                fp_max: Optional[int], fp: Optional[int]) -> None:
    print(BAR)
    print("GURPS STATE READOUT")
    print(SUB)
    if hp_max is not None and hp is not None:
        print(f"HP {hp}/{hp_max}:")
        for line in hp_state(hp_max, hp):
            print(f"  * {line}")
    if fp_max is not None and fp is not None:
        print(f"FP {fp}/{fp_max}:")
        for line in fp_state(fp_max, fp):
            print(f"  * {line}")
    print(BAR)


# ============================================================================
# SELFTEST — values vs. B419/B420/B423/B426/B428-429/B551
# ============================================================================

def selftest() -> int:
    failures = 0

    def check(desc: str, ok: bool) -> None:
        nonlocal failures
        print(f"  [{'PASS' if ok else 'FAIL'}] {desc}")
        if not ok:
            failures += 1

    print("### gurps_conditions.py SELFTEST — vs. Basic Set: Campaigns ###\n")

    c = lookup("shock")
    check("Shock: -DX/-IQ = HP lost, max -4, next turn only",
          c is not None and any("max -4" in e for e in c.effects)
          and any("next turn only" in e for e in c.effects))
    check("Shock: defenses unaffected",
          c is not None and any("NOT affect active defenses" in e for e in c.effects))
    check("Shock: 20+ HP scaling -1 per HP/10",
          c is not None and any("HP/10" in e for e in c.effects))

    c = lookup("stunned")
    check("Stunned: Do Nothing, defenses -4, no retreat, HT to recover",
          c is not None and any("Do Nothing" in e for e in c.effects)
          and any("-4" in e for e in c.effects)
          and any("no retreat" in e for e in c.effects)
          and any("HT roll" in e for e in c.effects))
    check("Mental stun alias resolves and uses IQ recovery",
          lookup("mental stun") is c and "IQ roll" in c.text)

    c = lookup("knockdown and stunning")
    check("Knockdown mods: -5 face/vitals/groin, -10 skull/eye, +3 HPT, -4 LPT",
          c is not None and any("-5" in e and "-10" in e for e in
                                [" ".join(c.effects)]))
    check("Knockdown fail-by-5 -> unconscious",
          c is not None and any("5+" in e and "unconscious" in e for e in c.effects))

    c = lookup("major wound")
    check("Major wound threshold > HP/2",
          c is not None and any("HP/2" in e for e in c.effects))

    c = lookup("crippling injury")
    check("Crippling thresholds: limb HP/2, extremity HP/3, eye HP/10",
          c is not None and any("HP/2" in e and "HP/3" in e and "HP/10" in e
                                for e in [" ".join(c.effects)]))
    check("Dismemberment at 2x threshold",
          c is not None and any("2x" in e for e in c.effects))

    c = lookup("mortal wound")
    check("Mortal wound: fail death check by 1-2; HT per half-hour",
          c is not None and "1 or 2" in c.text
          and any("half-hour" in e for e in c.effects))

    c = lookup("heart attack")
    check("Heart attack: -1xFP, death in HT/3 minutes",
          c is not None and any("-1xFP" in e for e in c.effects)
          and any("HT/3" in e for e in c.effects))

    for name, pen in [("moderate pain", "-2"), ("severe pain", "-4"),
                      ("terrible pain", "-6")]:
        c = lookup(name)
        check(f"{name.title()}: {pen} all rolls, HPT halves / LPT doubles",
              c is not None and any(e.startswith(pen) for e in c.effects)
              and any("HPT halves" in e for e in c.effects))

    c = lookup("nauseated")
    check("Nauseated: -2 attr/skill, -1 active defenses, (25-HT)s vomit",
          c is not None and any("-1 active defenses" in e for e in c.effects)
          and "25 - HT" in c.text.replace("(25-HT)", "(25 - HT)"))

    c = lookup("retching")
    check("Retching: -5 DX/IQ/Per, auto-fail Concentrate, -1 FP end",
          c is not None and any("-5" in e for e in c.effects)
          and any("Concentrate" in e for e in c.effects))

    c = lookup("agony")
    check("Agony: 1 FP/min, +3 interrogation after, incap-stun rider",
          c is not None and any("1 FP" in e for e in c.effects)
          and any("+3 Interrogation" in e for e in c.effects)
          and any("-4 defenses" in e for e in c.effects))

    c = lookup("daze")
    check("Daze: remain standing, struck -> recover next turn",
          c is not None and any("standing" in e for e in c.effects))

    c = lookup("paralysis")
    check("Paralysis: conscious, no voluntary movement",
          c is not None and any("Conscious" in e for e in c.effects))

    c = lookup("coughing")
    check("Coughing: -3 DX, -1 IQ, no Stealth",
          c is not None and c.effects == ["-3 DX", "-1 IQ", "No Stealth"])

    c = lookup("drunk")
    check("Drunk -2/-4 vs. Tipsy -1/-2",
          c is not None and any("-2 DX" in e for e in c.effects)
          and any("-4 self-control" in e for e in c.effects)
          and any("-1 DX" in e for e in lookup("tipsy").effects))

    c = lookup("prone")
    check("Prone/Lying alias: attack -4, defense -3",
          c is not None and c.name == "Lying Down"
          and any("-4" in e for e in c.effects)
          and any("-3" in e for e in c.effects))

    c = lookup("kneeling")
    check("Kneeling: -2/-2/-2, movement 1/3",
          c is not None and sum("-2" in e for e in c.effects) == 3)

    # State calculator vs. Fiendish Friedrick worked example (B419):
    # HP 14. At 2 HP: reeling. At -3: reeling + collapse rolls at -0.
    # Death checks at -14, -28, -42; auto-dead at -70.
    s = hp_state(14, 2)
    check("Friedrick 2/14 HP -> reeling only",
          any("REELING" in x for x in s) and not any("COLLAPSE" in x for x in s))
    s = hp_state(14, -3)
    check("Friedrick -3/14 -> collapse rolls at -0 penalty",
          any("COLLAPSE" in x and "-0" in x for x in s))
    s = hp_state(14, -14)
    check("Friedrick -14/14 -> first death check; next at -28",
          any("DEATH CHECK" in x and "-1xHP (-14)" in x for x in s)
          and any("-2xHP (-28)" in x for x in s))
    s = hp_state(14, -70)
    check("Friedrick -70/14 -> dead automatically (-5xHP)",
          any("DEAD automatically" in x for x in s))
    s = fp_state(12, 3)
    check("FP 3/12 -> very tired (< 1/3)",
          any("VERY TIRED" in x for x in s))
    s = fp_state(12, -12)
    check("FP -12/12 -> unconscious at -1xFP floor",
          any("UNCONSCIOUS" in x for x in s))

    n_conditions = len(CONDITIONS)
    check(f"Roster complete: {n_conditions} entries "
          "(4 HP states + 1 shock + 2 wound + 2 stun + 1 crippling + "
          "2 mortal/recovery + 3 FP states + 9 irritating + "
          "9 incapacitating + 2 mortal conditions + 6 postures = 41)",
          n_conditions == 41)

    print(f"\n{'ALL' if failures == 0 else failures} "
          f"{'checks passed.' if failures == 0 else 'CHECKS FAILED.'}")
    return 1 if failures else 0


# ============================================================================
# CLI
# ============================================================================

def main() -> int:
    ap = argparse.ArgumentParser(description="GURPS 4e condition reference")
    ap.add_argument("names", nargs="*", help="condition name(s) to look up")
    ap.add_argument("--list", action="store_true", help="list all conditions")
    ap.add_argument("--search", metavar="TEXT", help="search effects and text")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--state", action="store_true",
                    help="threshold readout from live totals")
    ap.add_argument("--hp-max", type=int)
    ap.add_argument("--hp", type=int)
    ap.add_argument("--fp-max", type=int)
    ap.add_argument("--fp", type=int)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if args.state:
        if (args.hp_max is None or args.hp is None) and \
           (args.fp_max is None or args.fp is None):
            print("--state needs --hp-max/--hp and/or --fp-max/--fp",
                  file=sys.stderr)
            return 2
        print_state(args.hp_max, args.hp, args.fp_max, args.fp)
        return 0

    if args.list:
        cat = None
        for c in CONDITIONS:
            if c.category != cat:
                cat = c.category
                print(f"\n[{cat.upper()}]")
            alias = f"  (aka {', '.join(c.aliases)})" if c.aliases else ""
            print(f"  {c.name}{alias}  — {c.source}")
        return 0

    if args.search:
        needle = args.search.lower()
        hits = [c for c in CONDITIONS
                if needle in c.text.lower()
                or any(needle in e.lower() for e in c.effects)
                or needle in c.name.lower()]
        if not hits:
            print(f"No conditions match '{args.search}'.")
            return 1
        for c in hits:
            print_condition(c)
        return 0

    if not args.names:
        ap.print_help()
        return 2

    rc = 0
    for name in args.names:
        c = lookup(name)
        if c is None:
            print(f"Unknown condition: '{name}'. Try --list or --search.",
                  file=sys.stderr)
            rc = 1
            continue
        if args.json:
            print(json.dumps(asdict(c), indent=2))
        else:
            print_condition(c)
    return rc


if __name__ == "__main__":
    sys.exit(main())
