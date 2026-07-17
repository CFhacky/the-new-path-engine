#!/usr/bin/env python3
"""
skill_check.py -- non-combat skill/task resolution reference & roller
The New Path / Arik arc -- surface-campaign-master-gm skill

The third engine, sibling to fused_round.py (combat) and personality_roll.py
(social/personality drift). Those two own their domains; this owns
everything else a DM screen actually exists for -- the constant stream of
one-off skill checks (can she climb this, does the lock hold, does the bluff
land) that previously got a DC improvised in the moment instead of looked up.

SOURCE: D&D 3.5e DM Screen (Wizards of the Coast, 2003) and GURPS 4e GM's
Screen (Steve Jackson Games, 2005), both in I:\\Sourcebooks. Both are
scanned-image PDFs with no text layer -- OCR'd via tesseract on 2026-07-02.

CONFIDENCE, stated per the same discipline fused_round.py and
personality_roll.py use for invented numbers -- documented, not hidden:
  - The 3.5e tables below transcribed CLEANLY off the screen and are at
    full confidence.
  - A few 3.5e tables were present on the screen but OCR'd too garbled to
    transcribe safely (full Disguise modifiers, Search DCs, the middle rows
    of the Turn Undead result table) -- these are flagged MISSING below
    with a pointer to the PH page instead of a guessed number.
  - The GURPS 4e side scanned far noisier. GURPS_TASK_MODIFIERS is
    reconstructed from partially-legible OCR plus the standard GURPS 4e
    modifier convention, flagged MEDIUM confidence -- spot-check the
    physical/PDF screen before treating any single GURPS number here as
    final.

OUTPUT DISCIPLINE: unlike personality_roll.py, these rolls are VISIBLE,
Phase-0 style, same as combat. Chad's stated preference is mechanical
transparency for anything outside the backstage personality layer -- print
the DC, the roll, and the modifiers used, don't hide them.

TWO MODES:
    lookup   Look up a DC/modifier from the reference tables without rolling.
    check    Look up AND roll -- d20 + modifier vs DC for 3.5e, 3d6 vs skill
             (GURPS quick-check, margin of success) for GURPS.
"""

import argparse
import json
import secrets
import sys
from typing import Any, Dict, Optional


# ============================================================================
# DICE ENGINE
# ============================================================================

def roll_die(sides: int) -> int:
    return secrets.randbelow(sides) + 1

def roll_d20() -> int:
    return roll_die(20)

def roll_3d6():
    rolls = [roll_die(6) for _ in range(3)]
    return sum(rolls), rolls


# ============================================================================
# 3.5e REFERENCE TABLES -- transcribed from DM Screen (WotC 2003), full confidence
# ============================================================================

BALANCE_DCS = {
    "narrow_surface": {
        "2-6 inches wide": 15,
        "less than 2 inches wide": 20,
    },
    "difficult_surface": {
        "hewn stone floor": 10,
        "sloped or angled floor": 10,
    },
    "modifiers": {
        "lightly obstructed (scree, light rubble)": 2,
        "severely obstructed (natural cavern floor, dense rubble)": 5,
        "lightly slippery (wet floor)": 2,
        "severely slippery (ice sheet)": 5,
        "sloped or angled": 2,
    },
    "source": "PH p.67",
}

BLUFF_VS_SENSE_MOTIVE = {
    "target wants to believe you": -5,
    "bluff is believable and doesn't affect target much": 0,
    "bluff is a little hard to believe or puts target at some risk": 5,
    "bluff is hard to believe or puts target at significant risk": 10,
    "bluff is way out there, almost too incredible to consider": 20,
    "_note": "modifier applies to the base Sense Motive DC the target must beat",
    "source": "PH p.68 (Bluff) opposed by Sense Motive",
}

DISABLE_DEVICE = {
    "simple": {"time": "1 round", "dc": 10, "example": "jam a lock"},
    "tricky": {"time": "1d4 rounds", "dc": 15, "example": "sabotage a wagon wheel"},
    "difficult": {"time": "2d4 rounds", "dc": 20, "example": "disarm a trap, reset a trap"},
    "wicked": {"time": "2d4 rounds", "dc": 25,
               "example": "disarm a complex trap, cleverly sabotage a clockwork device"},
    "leave_no_trace_mod": 5,
    "source": "PH p.72-73",
}

USE_ROPE = {
    "tie a firm knot": 10,
    "secure a grappling hook": 10,
    "grapple_hook_per_10ft_thrown_mod": 2,
    "tie a special knot (slips, slides slowly, or loosens with a tug)": 15,
    "tie a rope around yourself one-handed": 15,
    "splice two ropes together": 15,
    "bind a character": "varies -- opposed by Escape Artist or Str check",
    "source": "PH p.86",
}

IMPERSONATE_SPECIFIC_INDIVIDUAL = {
    "recognizes on sight": 4,
    "friends or associates": 6,
    "close friends": 8,
    "_note": "modifier adds to the Sense Motive DC the observer must beat to see through the disguise",
    "source": "PH p.73",
}

TURN_UNDEAD_RESULT = {
    "0 or lower": "no undead affected",
    "16-18": "cleric's level + 2",
    "19-21": "cleric's level + 3",
    "22 or higher": "cleric's level + 4",
    "_missing": "rows for check result 1-15 OCR'd too garbled to transcribe safely -- consult PH p.159 directly",
    "source": "PH p.159",
}

PERFORM_DCS = {
    10: {"quality": "routine performance", "earnings": "1d6 sp/day (busking, trying to earn money by playing)"},
    15: {"quality": "enjoyable performance", "earnings": "1d10 sp/day in a prosperous city"},
    20: {"quality": "great performance", "earnings": "3d10 sp/day; may be invited to join a professional troupe, regional reputation"},
    25: {"quality": "memorable performance", "earnings": "1d6 gp/day; may draw noble patrons, national reputation"},
    30: {"quality": "extraordinary performance", "earnings": "3d6 gp/day; may draw distant or extraplanar patrons"},
    "source": "PH p.79",
}

RIDE_DCS = {
    5: ["guide with knees", "stay in saddle"],
    10: ["fight with warhorse"],
    15: ["leap", "soft fall", "spur mount", "use mount as cover"],
    20: ["control mount in battle"],
    "_missing": "fast mount/dismount and bareback modifiers OCR'd ambiguous -- consult PH p.80 directly",
    "source": "PH p.80",
}

SPOT_MODIFIERS = {
    "per 10 feet of distance": -1,
    "spotter distracted": -5,
    "source": "PH p.83",
}

SWIM_DCS = {
    "calm water": 10,
    "rough water": 15,
    "stormy water": 20,
    "source": "PH p.84",
}

SURVIVAL_DCS = {
    10: "get along in the wild -- move up to half overland speed while hunting/foraging, no food/water supplies needed",
    15: "gain +2 Fort vs severe weather while moving at half speed (+4 if stationary); grant same bonus to one ally per point the check exceeds 15",
    "15_alt": "keep from getting lost or avoid natural hazards (quicksand, etc.)",
    "15_weather": "predict weather up to 24 hours in advance; +1 additional day per 5 points the check exceeds 15",
    "varies": "follow tracks -- see Track feat, PH p.101",
    "source": "PH p.88-89",
}

TUMBLE_DCS = {
    15: "treat a fall as 10 feet shorter than it really is",
    "15_half_speed": "move at half speed as a full-round action without provoking AoO (+2 DC per enemy after the first)",
    25: "tumble through an enemy-occupied square without provoking (+2 DC per enemy after the first)",
    "modifiers": {
        "lightly obstructed (scree, light rubble, undergrowth)": 2,
        "severely obstructed (cavern floor, rubble, thick undergrowth)": 5,
        "lightly slippery (wet floor)": 2,
        "severely slippery (ice sheet)": 5,
        "sloped or angled": 2,
    },
    "source": "PH p.85",
}

# Action economy -- action type + whether it provokes an attack of opportunity.
# Transcribed in full; this is the table fused_round.py's non-combat-adjacent
# rulings (readying a shield, standing up, retrieving a stowed item mid-fight)
# should check instead of improvising.
ACTIONS_TABLE = {
    "attack (melee)": {"type": "standard", "provokes_aoo": False},
    "attack (ranged)": {"type": "standard", "provokes_aoo": True},
    "attack (unarmed)": {"type": "standard", "provokes_aoo": True},
    "activate ring, rod, staff, wand, or misc. item": {"type": "standard", "provokes_aoo": False},
    "aid another": {"type": "standard", "provokes_aoo": "maybe"},
    "bull rush": {"type": "standard", "provokes_aoo": False},
    "cast quickened spell": {"type": "free", "provokes_aoo": False},
    "cast a spell (1 action casting time)": {"type": "standard", "provokes_aoo": True},
    "cast a spell defensively (using concentrate)": {"type": "standard", "provokes_aoo": False},
    "cease concentration (on activated spell/ability)": {"type": "free", "provokes_aoo": False},
    "charge": {"type": "full or standard", "provokes_aoo": False},
    "concentrate on spell or special ability": {"type": "standard", "provokes_aoo": False},
    "control a frightened mount": {"type": "move", "provokes_aoo": True},
    "coup de grace attack": {"type": "full-round", "provokes_aoo": True},
    "delay action": {"type": "free", "provokes_aoo": False},
    "direct or redirect an active spell": {"type": "move", "provokes_aoo": False},
    "disarm foe": {"type": "varies", "provokes_aoo": True},
    "dismiss a spell": {"type": "standard", "provokes_aoo": False},
    "drink a potion": {"type": "standard", "provokes_aoo": True},
    "drop an item": {"type": "free", "provokes_aoo": False},
    "drop to prone": {"type": "free", "provokes_aoo": False},
    "escape a grapple": {"type": "standard", "provokes_aoo": False},
    "escape from entanglement": {"type": "full-round", "provokes_aoo": True},
    "extinguish flames": {"type": "full-round", "provokes_aoo": False},
    "feint (using bluff skill)": {"type": "standard", "provokes_aoo": False},
    "fight defensively": {"type": "free", "provokes_aoo": False},
    "five-foot step": {"type": "free", "provokes_aoo": False},
    "full attack (melee)": {"type": "full-round", "provokes_aoo": False},
    "full attack (ranged)": {"type": "full-round", "provokes_aoo": True},
    "full attack (unarmed)": {"type": "full-round", "provokes_aoo": True},
    "grapple foe (grab, grapple, damage, or pin)": {"type": "varies", "provokes_aoo": "varies"},
    "light a torch with flint and steel": {"type": "full-round", "provokes_aoo": True},
    "light a torch with a tindertwig": {"type": "standard", "provokes_aoo": True},
    "load light or hand crossbow": {"type": "move", "provokes_aoo": True},
    "load a heavy or repeating crossbow": {"type": "full-round", "provokes_aoo": True},
    "lock or unlock a weapon in a locked gauntlet": {"type": "full-round", "provokes_aoo": True},
    "lower spell resistance": {"type": "standard", "provokes_aoo": False},
    "mount a creature or dismount": {"type": "move", "provokes_aoo": True},
    "move a heavy object": {"type": "move", "provokes_aoo": True},
    "move more than 5 feet": {"type": "move", "provokes_aoo": True},
    "open or close a door": {"type": "move", "provokes_aoo": False},
    "overrun": {"type": "standard", "provokes_aoo": False},
    "pick up an item": {"type": "move", "provokes_aoo": True},
    "prepare material components to spell": {"type": "free", "provokes_aoo": False},
    "prepare oil for throwing": {"type": "full-round", "provokes_aoo": True},
    "quick draw weapon (with quick draw feat)": {"type": "free", "provokes_aoo": False},
    "read a scroll": {"type": "standard", "provokes_aoo": True},
    "ready a shield": {"type": "move", "provokes_aoo": False},
    "retrieve a stowed item": {"type": "move", "provokes_aoo": True},
    "run": {"type": "full-round", "provokes_aoo": True},
    "sheathe a weapon": {"type": "move", "provokes_aoo": True},
    "speak": {"type": "free", "provokes_aoo": False},
    "stabilize a dying creature (using heal skill)": {"type": "standard", "provokes_aoo": True},
    "stand up from prone": {"type": "move", "provokes_aoo": True},
    "stow item": {"type": "move", "provokes_aoo": True},
    "sunder a weapon (attack)": {"type": "standard", "provokes_aoo": True},
    "sunder an object (attack)": {"type": "standard", "provokes_aoo": "maybe"},
    "total defense": {"type": "standard", "provokes_aoo": False},
    "trip opponent": {"type": "varies", "provokes_aoo": False},
    "turn or rebuke undead": {"type": "standard", "provokes_aoo": False},
    "use extraordinary ability": {"type": "varies", "provokes_aoo": False},
    "use spell-like ability": {"type": "standard", "provokes_aoo": True},
    "use supernatural ability": {"type": "standard", "provokes_aoo": False},
    "use touch spell on up to six allies": {"type": "full-round", "provokes_aoo": True},
    "withdraw": {"type": "full-round", "provokes_aoo": False},
    "_source": "PH p.133-160",
}


# ============================================================================
# GURPS 4e REFERENCE -- reconstructed from noisy OCR + standard convention.
# MEDIUM CONFIDENCE. Spot-check against the physical screen before treating
# any single number here as final -- same discipline as an unverified
# fused_round.py ruling.
# ============================================================================

GURPS_TASK_MODIFIERS = {
    10: "Automatic",
    8: "Trivial",
    6: "Very Easy",
    4: "Easy",
    2: "Very Favorable",
    1: "Favorable",
    0: "Average",
    -1: "Unfavorable",
    -2: "Very Unfavorable",
    -4: "Hard",
    -6: "Very Hard",
    -8: "Formidable",
    -10: "Impossible / no realistic chance",
    "_confidence": "MEDIUM -- reconstructed from partial OCR of GURPS 4e GM's Screen "
                    "plus standard GURPS 4e task-modifier convention. Verify before final use.",
    "source": "GURPS 4e GM's Screen",
}

GURPS_FAMILIARITY_PENALTIES = {
    "unfamiliar technique or specialty": -2,
    "unfamiliar equipment (basic or better than what you trained on)": -2,
    "equipment one TL below yours": -2,
    "equipment two or more TL below yours": -5,
    "equipment above your TL": -5,
    "_confidence": "MEDIUM -- reconstructed from partial OCR. Verify before final use.",
    "source": "GURPS 4e GM's Screen / Basic Set familiarity rules",
}


# ============================================================================
# LOOKUP
# ============================================================================

_TABLES = {
    "balance": BALANCE_DCS,
    "bluff_vs_sense_motive": BLUFF_VS_SENSE_MOTIVE,
    "disable_device": DISABLE_DEVICE,
    "use_rope": USE_ROPE,
    "impersonate": IMPERSONATE_SPECIFIC_INDIVIDUAL,
    "turn_undead": TURN_UNDEAD_RESULT,
    "perform": PERFORM_DCS,
    "ride": RIDE_DCS,
    "spot": SPOT_MODIFIERS,
    "swim": SWIM_DCS,
    "survival": SURVIVAL_DCS,
    "tumble": TUMBLE_DCS,
    "actions": ACTIONS_TABLE,
    "gurps_task_modifiers": GURPS_TASK_MODIFIERS,
    "gurps_familiarity": GURPS_FAMILIARITY_PENALTIES,
}


def lookup(category: str) -> Dict[str, Any]:
    """Return a reference table by name, no roll. See _TABLES for valid categories."""
    if category not in _TABLES:
        raise ValueError(f"Unknown category {category!r}. Valid: {sorted(_TABLES)}")
    return {"category": category, "table": _TABLES[category]}


# ============================================================================
# CHECK -- roll and resolve, VISIBLE Phase-0-style output (not backstage)
# ============================================================================

def format_header(system: str, label: str, dc_or_target: int, modifier: int,
                   roll_result: int, total: int, success: bool, rolls=None) -> str:
    """Visible Phase-0-style header -- this belongs in prose, unlike
    personality_roll.py's backstage-only receipt. Mechanical transparency is
    the rule outside the personality layer."""
    lines = [f"═══ SKILL CHECK: {label} ({system}) ═══"]
    if system == "3.5e":
        lines.append(f"d20 roll: {roll_result} + modifier {modifier:+d} = {total}  vs DC {dc_or_target}")
    else:
        lines.append(f"3d6 roll: {rolls} = {roll_result}  vs target {dc_or_target} (skill {modifier:+d} applied)")
    lines.append(f"RESULT: {'SUCCESS' if success else 'FAILURE'}")
    return "\n".join(lines)


def check_35e(label: str, dc: int, modifier: int = 0) -> Dict[str, Any]:
    """d20 + modifier vs DC."""
    roll = roll_d20()
    total = roll + modifier
    success = total >= dc
    result = {
        "mode": "check",
        "system": "3.5e",
        "label": label,
        "dc": dc,
        "modifier": modifier,
        "roll_d20": roll,
        "total": total,
        "success": success,
        "critical": roll == 20,
        "fumble": roll == 1,
    }
    result["header"] = format_header("3.5e", label, dc, modifier, roll, total, success)
    return result


def check_gurps(label: str, skill: int, modifier: int = 0) -> Dict[str, Any]:
    """GURPS quick check: roll 3d6, succeed if roll <= (skill + modifier),
    margin of success/failure = (skill + modifier) - roll."""
    total, rolls = roll_3d6()
    effective_skill = skill + modifier
    success = total <= effective_skill
    margin = effective_skill - total
    result = {
        "mode": "check",
        "system": "GURPS",
        "label": label,
        "skill": skill,
        "modifier": modifier,
        "effective_skill": effective_skill,
        "roll_3d6": total,
        "rolls": rolls,
        "margin": margin,
        "success": success,
        "critical_success": total <= 4 or (total == 5 and effective_skill >= 15) or (total == 6 and effective_skill >= 16),
        "critical_failure": total >= 18 or (total == 17 and effective_skill < 15) or (not success and margin <= -10),
    }
    result["header"] = format_header("GURPS", label, effective_skill, modifier, total, total, success, rolls=rolls)
    return result


# ============================================================================
# SELFTEST
# ============================================================================

def selftest():
    print("### SELFTEST 1 -- lookup, Disable Device reference table ###")
    print(json.dumps(lookup("disable_device"), indent=2))

    print("\n### SELFTEST 2 -- lookup, GURPS task modifier ladder (flagged MEDIUM confidence) ###")
    print(json.dumps(lookup("gurps_task_modifiers"), indent=2))

    print("\n### SELFTEST 3 -- check, 3.5e, disarming a Wicked trap (DC 25, +8 Disable Device) ###")
    r = check_35e("Disarm a wicked trap", dc=25, modifier=8)
    print(json.dumps(r, indent=2))
    print(r["header"])

    print("\n### SELFTEST 4 -- check, GURPS, Vara talking her way past a checkpoint (skill 14, -2 unfamiliar jurisdiction) ###")
    r = check_gurps("Fast-Talk the checkpoint guard", skill=14, modifier=-2)
    print(json.dumps(r, indent=2))
    print(r["header"])

    print("\n### SELFTEST 5 -- check, 3.5e, Tumble through an enemy-occupied square, second enemy in the chain (DC 25 base +2) ###")
    r = check_35e("Tumble through enemy square (2nd enemy)", dc=27, modifier=12)
    print(json.dumps(r, indent=2))
    print(r["header"])


# ============================================================================
# CLI
# ============================================================================

def build_arg_parser():
    p = argparse.ArgumentParser(description="Non-combat skill/task reference & roller (companion to fused_round.py and personality_roll.py).")
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--mode", choices=["lookup", "check-35e", "check-gurps"])
    p.add_argument("--json", help="Path to a JSON file with kwargs for the chosen mode.")
    p.add_argument("--json-string", help="Inline JSON with kwargs for the chosen mode.")
    return p


def main():
    p = build_arg_parser()
    args = p.parse_args()

    if args.selftest:
        selftest()
        return

    if not args.mode:
        print("Specify --mode {lookup,check-35e,check-gurps} with --json/--json-string, or use --selftest.",
              file=sys.stderr)
        sys.exit(1)

    if args.json:
        with open(args.json, "r", encoding="utf-8") as f:
            kwargs = json.load(f)
    elif args.json_string:
        kwargs = json.loads(args.json_string)
    else:
        print("Provide --json or --json-string with the mode's arguments.", file=sys.stderr)
        sys.exit(1)

    fn = {"lookup": lookup, "check-35e": check_35e, "check-gurps": check_gurps}[args.mode]
    result = fn(**kwargs)
    print(json.dumps(result, indent=2))
    if "header" in result:
        print("\n" + result["header"])


if __name__ == "__main__":
    main()
