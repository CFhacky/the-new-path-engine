#!/usr/bin/env python3
"""
personality_roll.py — social/personality resolution engine
The New Path / Arik arc — surface-campaign-master-gm skill

The social mirror of scripts/fused_round.py. Where the combat engine fuses
3.5e/GURPS/WFRP to resolve a strike, this resolves whether a character's
controlled surface leaks this beat, what it costs them, and (for the PC only)
whether the read that reaches the page is even true. Designed conversationally
with Chad on 2026-07-02 — see memory note arik-personality-dice-mechanic for
the full design history; this is the implementation of that design, not a
restatement of it.

FOUR MODES:
    tell-check    One NPC, one beat. Does something leak? If so, what channel,
                  how big, and (optionally) how does Arik's Lens color what
                  actually gets reported.
    contest       Two characters' axes clash in a scene (Vara's Directness vs
                  Lirien's Deflection) — GURPS quick-contest style, higher
                  margin of success wins the beat.
    drift         Apply a push (event pressures a character toward Breaking)
                  or classify an opportunity scene (Addressed / Deflected /
                  Avoided) which may trigger a growth-forcing scene.
    growth-scene  The contested three-outcome resolution when a character's
                  avoided-opportunity count crosses the growth threshold:
                  REVERT (decays back toward Baseline), LOCK-IN (this becomes
                  the new Baseline — real growth/scarring), or ESCALATE (goes
                  worse before it resolves, no band exists past Breaking so
                  this is a flag, not a new band).

CORE RULINGS (ports/extends fused_round.py's practice of documenting
necessary invented numbers instead of hiding them):
    Bands, not floats: Baseline / Pressured / Breaking. Leak-fire chance by
    band: Baseline 10%, Pressured 40%, Breaking 70%. Intensity of what leaks
    scales with band: Baseline = flicker (barely perceptible, easy to miss),
    Pressured = small tell, Breaking = full tell (the character's authored
    crack-vocabulary from the Voice & Locks Codex).

    Arik's Lens: the ground-truth roll stays backstage always. What gets
    narrated is Arik's READ of it, which can be colored or simply wrong.
    Base misread chance 20%; escalates to 50% when the situation's "domain"
    is people/agency/loyalty (Arik's actual documented blind spot — see his
    character page) rather than facts/logistics, where his diligence
    genuinely covers him. This is not generic unreliable narration — the
    misread rate is keyed specifically to where his blind spot lives.

    Growth-scene distribution shifts with accumulated avoided_count: the
    longer something goes unaddressed, the LESS likely a gentle revert is
    and the more likely lock-in or escalation becomes. Ported from "the
    longer you look away, the more it costs" already implicit in this
    campaign's neglect-tracking pattern elsewhere. OFFSET (2026-07-02): a
    character's cumulative addressed_count -- real engagement banked over
    time, tracked by drift()'s 'addressed' event -- buys back resilience_skill
    at growth-scene time. A well-tended relationship keeps REVERT reachable
    even at a high avoided_count; a neglected one gets the full harsh curve.

OUTPUT DISCIPLINE (binding, per Chad 2026-07-02): rolls stay backstage. Do
not paste this script's full JSON output into session prose. Use the single
receipt line format_receipt() produces — enough to prove a real roll
happened, nothing that spills the mechanism into the scene.

All dice via Python's `secrets` module. No rerolls. Raw values retained in
the JSON result even though only the receipt line is meant for prose.
"""

import argparse
import json
import secrets
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any

# ============================================================================
# DICE ENGINE
# ============================================================================

def roll_die(sides: int) -> int:
    return secrets.randbelow(sides) + 1

def roll_pct() -> int:
    """1-100 roll for probability checks."""
    return secrets.randbelow(100) + 1

def roll_3d6():
    rolls = [roll_die(6) for _ in range(3)]
    return sum(rolls), rolls


# ============================================================================
# CONSTANTS — the documented rulings
# ============================================================================

BANDS = ["Baseline", "Pressured", "Breaking"]

LEAK_FIRE_CHANCE = {"Baseline": 10, "Pressured": 40, "Breaking": 70}
INTENSITY_BY_BAND = {
    "Baseline": "flicker (barely perceptible, easy to miss entirely)",
    "Pressured": "small tell (an overlong pause, a flicker of the mask)",
    "Breaking": "full tell (the character's authored crack-vocabulary)",
}

# Channel = which axis a character's control runs on, and the flavor of what
# leaks when it does. Bespoke per character (see Voice & Locks Codex Personality
# Tell subsections) — this table is the mechanical hook the Codex text hangs on,
# not a replacement for it. Claude supplies the actual prose from the Codex;
# this script only tells you WHICH channel fired and how big.
KNOWN_CHANNELS = {
    "verbal": "deadpan joke or oblique allusion, no self-reaction",
    "physical": "goes quiet, displacement activity instead of speaking",
    "numeric": "excessive unrequested precision where an estimate would do",
    "register-inversion": "drops into an unearned, uncharacteristic register",
    "stillness": "sudden stillness or redirects into competence/action",
}

ARIK_LENS_BASE_MISREAD_PCT = 20
ARIK_LENS_PEOPLE_DOMAIN_MISREAD_PCT = 50
DOMAINS = ["people_agency", "facts_logistics", "other"]

DEFAULT_GROWTH_THRESHOLD = 3  # avoided opportunities before a growth-scene fires

# Relationship investment: every INVESTMENT_BONUS_PER addressed events buys +1
# resilience_skill in a growth-scene, capped at INVESTMENT_BONUS_CAP. Chad's
# ruling (2026-07-02, after the growth-scene distribution tested too harsh --
# REVERT was functionally dead past avoided_count=3): "a well tended
# relationship should buy a shot at revert." addressed_count is cumulative and
# does NOT reset the way avoided_count does -- it's the character's whole
# history of real engagement, not just the current unresolved stretch.
INVESTMENT_BONUS_PER = 2
INVESTMENT_BONUS_CAP = 4

# Contest ties: Chad's ruling (2026-07-02), replacing the old "tie goes to the
# responder" convention -- that was a fixed rule, not a roll, and it skewed
# symmetric-skill contests to 45/55 instead of 50/50. On an exact margin tie,
# both sides reroll fresh against their own skill (sudden death) rather than
# defaulting to either side. Capped defensively; a 3d6-vs-3d6 tie chain this
# long isn't expected to occur in practice.
MAX_TIE_REROLLS = 20


# ============================================================================
# RECEIPT — the only thing meant to touch session prose
# ============================================================================

def format_receipt(mode: str, character: str, fired: bool = None, extra: str = "") -> str:
    """Minimal backstage confirmation line. Proves a real Python roll happened
    without spilling the mechanism. This is what's allowed near prose; the
    full JSON result is not."""
    tag = secrets.token_hex(3)
    bits = [f"[personality:{mode}", f"char={character}"]
    if fired is not None:
        bits.append("fired=yes" if fired else "fired=no")
    if extra:
        bits.append(extra)
    return " ".join(bits) + f" #{tag}]"


# ============================================================================
# MODE 1 — TELL CHECK
# ============================================================================

def tell_check(character: str, channel: str, current_band: str,
                situational_mod: int = 0, apply_lens: bool = False,
                domain: str = "other") -> Dict[str, Any]:
    if current_band not in BANDS:
        raise ValueError(f"current_band must be one of {BANDS}")
    if channel not in KNOWN_CHANNELS:
        raise ValueError(f"channel must be one of {list(KNOWN_CHANNELS)}")

    base_chance = LEAK_FIRE_CHANCE[current_band]
    effective_chance = max(1, min(99, base_chance + situational_mod))
    roll = roll_pct()
    fired = roll <= effective_chance

    result = {
        "mode": "tell-check",
        "character": character,
        "channel": channel,
        "current_band": current_band,
        "base_chance_pct": base_chance,
        "situational_mod": situational_mod,
        "effective_chance_pct": effective_chance,
        "roll_1_100": roll,
        "fired": fired,
    }

    if fired:
        result["intensity"] = INTENSITY_BY_BAND[current_band]
        result["craft_hint"] = KNOWN_CHANNELS[channel]
        # ground truth is what actually happened -- this is the backstage fact
        result["ground_truth"] = {
            "leaked": True,
            "channel": channel,
            "intensity": current_band,
        }
    else:
        result["ground_truth"] = {"leaked": False}

    if apply_lens:
        result["arik_lens"] = _apply_lens(result["ground_truth"], domain)

    result["receipt"] = format_receipt("tell-check", character, fired,
                                         extra=f"band={current_band}")
    return result


def _apply_lens(ground_truth: Dict[str, Any], domain: str) -> Dict[str, Any]:
    """Arik's Lens: what actually gets narrated. Ground truth stays in the
    result dict for the GM's own bookkeeping, but the 'arik_read' field is
    the only part that should ever inform prose. Misread chance is keyed to
    Arik's actual documented blind spot (people/agency, not facts/logistics)
    -- see his character page, Arik's Lens section."""
    if domain not in DOMAINS:
        raise ValueError(f"domain must be one of {DOMAINS}")
    misread_chance = (ARIK_LENS_PEOPLE_DOMAIN_MISREAD_PCT if domain == "people_agency"
                       else ARIK_LENS_BASE_MISREAD_PCT)
    roll = roll_pct()
    misread = roll <= misread_chance
    lens = {
        "domain": domain,
        "misread_chance_pct": misread_chance,
        "roll_1_100": roll,
        "misread": misread,
    }
    if not ground_truth.get("leaked"):
        # nothing leaked -- a misread here means Arik THINKS he saw something
        # that wasn't there (over-reading, projecting his own blind spot)
        lens["arik_read"] = ("imagines a tell that wasn't there -- reads too much "
                              "into an ordinary beat" if misread else
                              "correctly reads nothing unusual")
    else:
        lens["arik_read"] = ("notices SOMETHING but draws the wrong conclusion about "
                              "what it means -- GM: invent a plausible wrong conclusion "
                              "sourced from his blind spot, do not just negate the truth"
                              if misread else
                              "correctly reads the tell for what it is")
    return lens


# ============================================================================
# MODE 2 — CONTEST (two characters' axes clash)
# ============================================================================

def contest(char_a: str, skill_a: int, char_b: str, skill_b: int) -> Dict[str, Any]:
    """GURPS-flavored quick contest: each side rolls 3d6, margin = skill - roll
    (higher margin = better success). Higher margin wins the beat. On an exact
    tie, BOTH sides reroll fresh against their own skill -- sudden death, not a
    fixed tiebreaker -- and this repeats until someone actually wins. Rerolling
    against the real skills (rather than a coin flip) means any genuine skill
    differential still tells even in the rare case a tie happens on unequal
    skills; it's only truly 50/50 when the skills are equal too."""
    rounds = []
    for attempt in range(1, MAX_TIE_REROLLS + 1):
        total_a, rolls_a = roll_3d6()
        total_b, rolls_b = roll_3d6()
        margin_a = skill_a - total_a
        margin_b = skill_b - total_b
        rounds.append({
            "attempt": attempt,
            "char_a": {"roll": total_a, "rolls": rolls_a, "margin": margin_a},
            "char_b": {"roll": total_b, "rolls": rolls_b, "margin": margin_b},
        })
        if margin_a != margin_b:
            break

    final = rounds[-1]
    total_a, rolls_a, margin_a = final["char_a"]["roll"], final["char_a"]["rolls"], final["char_a"]["margin"]
    total_b, rolls_b, margin_b = final["char_b"]["roll"], final["char_b"]["rolls"], final["char_b"]["margin"]
    reroll_count = len(rounds) - 1

    if margin_a == margin_b:
        # Only reached if MAX_TIE_REROLLS was exhausted -- defensive fallback,
        # should not occur in practice.
        winner = char_b
        note = f"tied through {MAX_TIE_REROLLS} reroll attempts -- defensive fallback, goes to {char_b}"
    elif margin_a > margin_b:
        winner = char_a
        note = f"{char_a} wins the beat by margin {margin_a - margin_b}"
        if reroll_count:
            note += f" (after {reroll_count} tie reroll{'s' if reroll_count != 1 else ''})"
    else:
        winner = char_b
        note = f"{char_b} wins the beat by margin {margin_b - margin_a}"
        if reroll_count:
            note += f" (after {reroll_count} tie reroll{'s' if reroll_count != 1 else ''})"

    result = {
        "mode": "contest",
        "char_a": {"name": char_a, "skill": skill_a, "roll": total_a, "rolls": rolls_a, "margin": margin_a},
        "char_b": {"name": char_b, "skill": skill_b, "roll": total_b, "rolls": rolls_b, "margin": margin_b},
        "tie_rerolls": rounds[:-1],  # empty if the first roll settled it
        "winner": winner,
        "note": note,
    }
    result["receipt"] = format_receipt("contest", f"{char_a} vs {char_b}",
                                         extra=f"winner={winner}")
    return result


# ============================================================================
# MODE 3 — DRIFT (push / classify an opportunity scene)
# ============================================================================

def drift(character: str, current_band: str, event: str,
          avoided_count: int = 0, growth_threshold: int = DEFAULT_GROWTH_THRESHOLD,
          addressed_count: int = 0) -> Dict[str, Any]:
    """event: 'push' | 'addressed' | 'deflected' | 'avoided'
    push -> band moves one step toward Breaking (event-triggered, narrative call)
    addressed -> resets avoided_count to 0 regardless of band outcome (handled by
                 growth-scene); ALSO increments addressed_count by 1 -- this is a
                 cumulative, never-reset tally of real engagement, separate from
                 avoided_count's current-stretch clock. It's the relationship's
                 investment history, and growth_scene() spends it as a resilience
                 bonus.
    deflected -> avoided_count nudged down by 1 (floor 0), band unchanged, addressed_count unchanged
    avoided -> avoided_count +1, band unchanged, addressed_count unchanged; if it
               crosses growth_threshold, flags that a growth-scene should be run
    """
    if current_band not in BANDS:
        raise ValueError(f"current_band must be one of {BANDS}")
    if event not in ("push", "addressed", "deflected", "avoided"):
        raise ValueError("event must be one of: push, addressed, deflected, avoided")

    idx = BANDS.index(current_band)
    new_band = current_band
    new_avoided = avoided_count
    new_addressed = addressed_count
    growth_scene_due = False
    note = ""

    if event == "push":
        new_idx = min(idx + 1, len(BANDS) - 1)
        new_band = BANDS[new_idx]
        note = (f"{character} pushed from {current_band} to {new_band}"
                if new_idx != idx else f"{character} already at ceiling ({current_band}), push had no further room")
    elif event == "addressed":
        new_avoided = 0
        new_addressed = addressed_count + 1
        note = (f"{character}'s avoided-opportunity count reset to 0 (addressed); "
                f"cumulative addressed_count now {new_addressed} (relationship investment banked)")
    elif event == "deflected":
        new_avoided = max(0, avoided_count - 1)
        note = f"{character}'s avoided-opportunity count nudged down to {new_avoided} (attempt made, mask held)"
    elif event == "avoided":
        new_avoided = avoided_count + 1
        note = f"{character}'s avoided-opportunity count now {new_avoided}"
        if new_avoided >= growth_threshold:
            growth_scene_due = True
            note += f" -- CROSSES THRESHOLD ({growth_threshold}): a growth-forcing scene is due"

    result = {
        "mode": "drift",
        "character": character,
        "event": event,
        "previous_band": current_band,
        "new_band": new_band,
        "previous_avoided_count": avoided_count,
        "new_avoided_count": new_avoided,
        "previous_addressed_count": addressed_count,
        "new_addressed_count": new_addressed,
        "growth_threshold": growth_threshold,
        "growth_scene_due": growth_scene_due,
        "note": note,
    }
    result["receipt"] = format_receipt("drift", character, extra=f"event={event} band={new_band}")
    return result


# ============================================================================
# MODE 4 — GROWTH SCENE (contested three-outcome resolution)
# ============================================================================

def growth_scene(character: str, avoided_count: int, resilience_skill: int = 10,
                  addressed_count: int = 0) -> Dict[str, Any]:
    """Roll 3d6 against a difficulty that STIFFENS with accumulated
    avoided_count -- the longer something goes unaddressed, the less likely a
    gentle revert becomes -- offset by an investment bonus drawn from
    addressed_count, the character's cumulative history of real engagement
    (see drift()'s 'addressed' event). Chad's ruling (2026-07-02): "a well
    tended relationship should buy a shot at revert." Every INVESTMENT_BONUS_PER
    addressed events buys +1 effective skill, capped at INVESTMENT_BONUS_CAP --
    this is what makes REVERT reachable again at realistic avoided_count values
    for a relationship that's actually been tended, while a neglected one still
    gets the harsh curve. Three outcomes, not a guaranteed one, per
    commit-over-convenience:
        REVERT   -- margin clearly positive: resolves, decays toward Baseline
        LOCK-IN  -- margin near zero: this becomes the new Baseline (real growth/scarring)
        ESCALATE -- margin clearly negative: goes worse before it resolves (no band
                    past Breaking exists -- this is a flag for the GM to escalate
                    narratively, not a new tracked state)
    """
    difficulty_penalty = avoided_count  # each avoided opportunity stiffens the roll
    investment_bonus = min(addressed_count // INVESTMENT_BONUS_PER, INVESTMENT_BONUS_CAP)
    effective_skill = resilience_skill + investment_bonus - difficulty_penalty
    total, rolls = roll_3d6()
    margin = effective_skill - total

    if margin >= 3:
        outcome = "REVERT"
        note = f"{character} gets a genuine release -- decays back toward Baseline"
    elif margin >= -2:
        outcome = "LOCK-IN"
        note = f"{character}'s Breaking state becomes the new Baseline -- real, permanent growth/scarring"
    else:
        outcome = "ESCALATE"
        note = f"{character}'s confrontation goes worse before it resolves -- no band past Breaking, flag for narrative escalation, re-run when the next scene addresses it"

    result = {
        "mode": "growth-scene",
        "character": character,
        "avoided_count": avoided_count,
        "difficulty_penalty": difficulty_penalty,
        "addressed_count": addressed_count,
        "investment_bonus": investment_bonus,
        "resilience_skill": resilience_skill,
        "effective_skill": effective_skill,
        "roll_3d6": total,
        "rolls": rolls,
        "margin": margin,
        "outcome": outcome,
        "note": note,
    }
    result["receipt"] = format_receipt("growth-scene", character, extra=f"outcome={outcome}")
    return result


# ============================================================================
# SELFTEST
# ============================================================================

def selftest():
    print("### SELFTEST 1 -- tell-check, Lirien at Breaking, verbal channel, Arik's Lens on, people_agency domain ###")
    r = tell_check("Lirien Nightwalker", "verbal", "Breaking", situational_mod=0,
                    apply_lens=True, domain="people_agency")
    print(json.dumps(r, indent=2))
    print("RECEIPT:", r["receipt"])

    print("\n### SELFTEST 2 -- tell-check, Vara at Pressured, numeric channel, Lens off ###")
    r = tell_check("Vara Torsten", "numeric", "Pressured", situational_mod=10)
    print(json.dumps(r, indent=2))
    print("RECEIPT:", r["receipt"])

    print("\n### SELFTEST 3 -- contest, Vara's Directness vs Lirien's Deflection ###")
    r = contest("Vara Torsten", 12, "Lirien Nightwalker", 13)
    print(json.dumps(r, indent=2))
    print("RECEIPT:", r["receipt"])

    print("\n### SELFTEST 4 -- drift, Lirien pushed to Breaking after a mole discovery ###")
    r = drift("Lirien Nightwalker", "Pressured", "push")
    print(json.dumps(r, indent=2))
    print("RECEIPT:", r["receipt"])

    print("\n### SELFTEST 5 -- drift, third avoided opportunity in a row crosses threshold ###")
    r = drift("Lirien Nightwalker", "Breaking", "avoided", avoided_count=2, growth_threshold=3)
    print(json.dumps(r, indent=2))
    print("RECEIPT:", r["receipt"])

    print("\n### SELFTEST 6 -- growth-scene, triggered by selftest 5, no investment banked ###")
    r = growth_scene("Lirien Nightwalker", avoided_count=3, resilience_skill=11)
    print(json.dumps(r, indent=2))
    print("RECEIPT:", r["receipt"])

    print("\n### SELFTEST 7 -- same trigger, but a well-tended relationship (addressed_count=8 -> +4 bonus) ###")
    r = growth_scene("Lirien Nightwalker", avoided_count=3, resilience_skill=11, addressed_count=8)
    print(json.dumps(r, indent=2))
    print("RECEIPT:", r["receipt"])


# ============================================================================
# CLI
# ============================================================================

def build_arg_parser():
    p = argparse.ArgumentParser(description="Personality/social resolution engine (companion to fused_round.py).")
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--mode", choices=["tell-check", "contest", "drift", "growth-scene"])
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
        print("Specify --mode {tell-check,contest,drift,growth-scene} with --json/--json-string, or use --selftest.",
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

    fn = {"tell-check": tell_check, "contest": contest, "drift": drift, "growth-scene": growth_scene}[args.mode]
    result = fn(**kwargs)
    print(json.dumps(result, indent=2))
    print("\nRECEIPT (only this line belongs anywhere near prose):", result["receipt"])


if __name__ == "__main__":
    main()
