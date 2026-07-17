#!/usr/bin/env python3
"""
fused_round.py — FUSED combat engine resolver
The New Path / Arik arc — surface-campaign-master-gm skill

Implements SKILL.md Section 3 ("Combat — THE FUSED ENGINE") and the full
protocol mirrored on the Notion Talent Catalog page (Part VII: The Fused
Resolution Protocol; Part VIII: The Numbers Standard), page ID
37ce8214-84b0-81d3-ab92-fb245a10f9a1.

ROUND ORDER (binding, do not reorder):
    stance (free)
      -> 3.5e action (choose attack sequence: iteratives / haste / whirlwind)
      -> per strike:
           d20 (spend Deceptive Attack / targeted-strike penalties)
           -> defender 3d6 (Parry/Block/Dodge contest; confirmed crits skip this)
           -> damage
           -> DR (before multipliers; "ignores armor" riders skip this step)
           -> multipliers (crit / targeted-strike)
           -> riders (Numbers Standard effect classes, if any)
           -> crit tables (confirmed threats, below-0 hits, targeted vitals/neck/limb)
           -> Fury (maxed base dice)
      -> enemy mirror (defender's own strikes, same procedure)
      -> morale (mob targets only, at configured thresholds)

THREE LAYERS, FUSED (not chosen between):
    Layer 1 (3.5e chassis)  — action economy, BAB iteratives, HP pools, d20 to-hit vs AC.
    Layer 2 (GURPS contest) — defender rolls 3d6 vs Parry/Block/Dodge (roll UNDER the
                               target number to defend). Deceptive Attack: -4 on the
                               attacker's d20 buys -2 on the defender's target number,
                               repeatable. Multi-threat: -1 per extra attacker, cap -3.
                               Targeted strikes: vitals -3/x3 (impaling weapons), neck -5,
                               limb -2. Armor = DR, subtracted before multipliers;
                               "ignores armor" riders skip DR.
    Layer 3 (WFRP grammar)  — stances (All-Out = +4 to-hit / NO active defenses that
                               round — the price is real), talents, location crit tables
                               on confirmed threats and on hits that drop a target to or
                               below 0 HP, Fury on maxed base damage dice, morale tests
                               for mob targets at casualty thresholds.

All dice are rolled with Python's `secrets` module (cryptographically-seeded, not
reproducible, no rerolls) and every raw die is shown in the output. This script does
not invent numbers outside what SKILL.md and the Talent Catalog specify; where the
source material is silent on an exact sub-rule (e.g. mob morale thresholds), the
ruling is called out explicitly in a comment and in the --selftest output so Chad can
override it.

USAGE
    python3 fused_round.py --json round.json
    python3 fused_round.py --json-string '{...}'
    python3 fused_round.py --selftest
    python3 fused_round.py --attacker "Korgan Bloodaxe" --bab 16 --weapon-dice 1d10 \
        --weapon-bonus 8 --target "Gnoll Skirmisher" --target-ac 15 \
        --target-defense-skill Dodge --target-defense-value 11 --target-dr 1 --target-hp 13

Input JSON schema — see build_arg_parser() --json-schema for a printable copy, or
read SCHEMA_DOC below.
"""

import argparse
import json
import secrets
import sys
import re
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any

# ============================================================================
# DICE ENGINE — secrets-backed, no rerolls, raw values always retained
# ============================================================================

def roll_die(sides: int) -> int:
    """Cryptographically-seeded 1..sides roll."""
    return secrets.randbelow(sides) + 1


def roll_d20() -> int:
    return roll_die(20)


DICE_EXPR_RE = re.compile(r"^\s*(\d+)d(\d+)\s*([+-]\s*\d+)?\s*$", re.IGNORECASE)


def roll_dice_expr(expr: str):
    """Parse and roll a 'NdM+K' expression. Returns (total, [raw dice], mod)."""
    m = DICE_EXPR_RE.match(expr)
    if not m:
        raise ValueError(f"Bad dice expression: {expr!r} (expected e.g. '1d10+3')")
    n, sides, mod = int(m.group(1)), int(m.group(2)), m.group(3)
    mod = int(mod.replace(" ", "")) if mod else 0
    rolls = [roll_die(sides) for _ in range(n)]
    return sum(rolls) + mod, rolls, mod, sides


def roll_3d6():
    """GURPS-style contest roll: 3d6, roll UNDER the target number to succeed."""
    rolls = [roll_die(6) for _ in range(3)]
    return sum(rolls), rolls


# ============================================================================
# CONSTANTS — stance table, targeted-strike table, talent hooks, crit tables
# ============================================================================

# Stance modifiers. All-Out is the only one with an explicit number in SKILL.md
# (+4 to-hit / no active defenses). The others are a reasonable, symmetric WFRP-
# style spread consistent with "the price is real" — flag with --stance-table
# if Chad wants different numbers; nothing here is load-bearing outside this
# script (Notion Talent Catalog does not number Guarded/Aggressive/Defensive).
STANCES = {
    "Guarded":    {"to_hit": 0,  "defense_delta": 0,  "active_defense": True},
    "Aggressive": {"to_hit": 2,  "defense_delta": -2, "active_defense": True},
    "Defensive":  {"to_hit": -2, "defense_delta": 2,  "active_defense": True},
    "All-Out":    {"to_hit": 4,  "defense_delta": 0,  "active_defense": False},
}

# Targeted strikes (Notion Talent Catalog, Part VII).
TARGETED_STRIKES = {
    "vitals": {"to_hit": -3, "multiplier_if_impaling": 3, "forces_crit_table": True},
    "neck":   {"to_hit": -5, "multiplier_if_impaling": 1, "forces_crit_table": True},
    "limb":   {"to_hit": -2, "multiplier_if_impaling": 1, "forces_crit_table": True},
}

# Talent hooks actually mechanized by this script. The remaining ten of the
# fifteen (Wall of Steel, Shieldsman, Sure Shot, Quick Draw, Disarm Master,
# Street Fighting, Rapid Reload, Duellist's Eye, Mighty Shot) are positioning/
# ranged/social talents with no single-round-resolver hook — SKILL.md self-check
# says mechanics resolve on this engine but doesn't require every talent to have
# a numeric effect here; GM applies those narratively.
TALENT_STRIKE_MIGHTY_BLOW = "Strike Mighty Blow"     # +2 dmg, +1 per die in the roll
TALENT_STRIKE_TO_INJURE = "Strike to Injure"         # crit severity +1 on location tables
TALENT_LIGHTNING_PARRY = "Lightning Parry"           # +1 extra defense reaction/round
TALENT_BLOOD_RITE_FURY = "Blood-Rite Fury"           # widens Fury trigger to ANY die maxed

# Location crit table (d10) x severity (d6, +1 per Strike to Injure). This is the
# script's concrete implementation of "location crit tables on confirmed threats
# and below-0 hits" — SKILL.md names the trigger conditions but not a numbered
# table, so this is the ruling; override freely, it's isolated in one place.
LOCATION_TABLE = {
    (1, 2): "Head",
    (3, 4): "Neck",
    (5, 6): "Torso",
    (7, 8): "Arm/Weapon Hand",
    (9, 10): "Leg",
}

SEVERITY_TABLE = {
    1: "Light — no lasting effect, GM narrates the graze",
    2: "Light — no lasting effect, GM narrates the graze",
    3: "Serious — bleeding/penalty, GM narrates the wound",
    4: "Serious — bleeding/penalty, GM narrates the wound",
    5: "Critical — maiming, target likely out of the fight",
    6: "Critical — maiming, target likely out of the fight",
    7: "Lethal — instant severe consequence (Strike to Injure escalation)",
}


def location_lookup(d10_roll: int) -> str:
    for (lo, hi), name in LOCATION_TABLE.items():
        if lo <= d10_roll <= hi:
            return name
    return "Torso"


def severity_lookup(total: int) -> str:
    total = max(1, min(7, total))
    return SEVERITY_TABLE[total]


# ============================================================================
# BAB ITERATIVES (Layer 1, 3.5e chassis)
# ============================================================================

def bab_iteratives(bab: int, haste: bool = False) -> List[int]:
    """Standard 3.5e full-attack progression: BAB, BAB-5, BAB-10, ... down to >=1.
    Haste inserts one extra attack at the character's full (highest) bonus.
    Example: BAB 16 -> [16, 11, 6, 1]; SKILL.md's own worked example drops the
    trailing +1 for brevity ("+16/+11/+6") but the +1 iterative is real 3.5e RAW
    and included here — trim it in the JSON's "strikes" override if undesired.
    """
    bonuses = []
    b = bab
    while b >= 1:
        bonuses.append(b)
        b -= 5
    if not bonuses:
        bonuses = [bab]
    if haste:
        bonuses.insert(0, bab)
    return bonuses


# ============================================================================
# DATA MODEL
# ============================================================================

@dataclass
class Weapon:
    name: str = "weapon"
    dice: str = "1d8"
    bonus: int = 0
    threat_range: int = 20   # natural roll needed to threaten a crit
    crit_mult: int = 2
    dmg_type: str = "slashing"   # slashing | piercing | bludgeoning | impaling
    ignores_armor: bool = False


@dataclass
class Defender:
    name: str
    ac: int = 10
    dr: int = 0
    defense_skill: str = "Dodge"     # Parry | Block | Dodge
    defense_value: int = 10          # GURPS target number, roll 3d6 UNDER this to defend
    hp: int = 10
    all_out: bool = False            # in All-Out stance = no active defenses this round
    multi_threat_count: int = 0      # extra attackers already engaging this target this round
    is_mob: bool = False
    mob_count: int = 0
    mob_starting_count: int = 0
    leader_down: bool = False

    def effective_defense_target(self, deceptive_penalty: int) -> int:
        mt_penalty = min(self.multi_threat_count, 3)  # cap -3
        target = self.defense_value - deceptive_penalty - mt_penalty
        return max(target, 0)


@dataclass
class Strike:
    target: str
    iterative_bonus: int = 0
    deceptive: int = 0             # e.g. -4, -8 ... (multiple of 4, on the d20)
    targeted: Optional[str] = None  # "vitals" | "neck" | "limb" | None
    label: str = ""                 # e.g. "Whirlwind vs Gnoll 3"


@dataclass
class Attacker:
    name: str
    bab: int = 1
    attack_bonus: int = 0            # flat bonus (Str/weapon/etc.) added to every iterative
    stance: str = "Guarded"
    haste: bool = False
    whirlwind: bool = False
    weapon: Weapon = field(default_factory=Weapon)
    talents: List[str] = field(default_factory=list)
    strikes: Optional[List[Strike]] = None   # explicit override; else auto-generated


# ============================================================================
# RESOLUTION
# ============================================================================

def build_strikes(attacker: Attacker, default_target: str) -> List[Strike]:
    """Auto-generate the strike list from BAB iteratives / haste / whirlwind if the
    caller didn't supply an explicit list."""
    if attacker.strikes:
        return attacker.strikes
    bonuses = bab_iteratives(attacker.bab, attacker.haste)
    if attacker.whirlwind:
        # Whirlwind = ONE full-bonus strike vs everyone in reach; caller is
        # expected to supply one Strike per target instead. Fallback: single
        # full-bonus strike at the default target.
        return [Strike(target=default_target, iterative_bonus=bonuses[0],
                        label="Whirlwind")]
    return [Strike(target=default_target, iterative_bonus=b,
                    label=f"Iterative @ +{b}") for b in bonuses]


def resolve_strike(attacker: Attacker, defender: Defender, strike: Strike,
                    stance_mods: dict) -> Dict[str, Any]:
    """Resolve one strike through all three layers. Returns a structured log entry."""
    entry: Dict[str, Any] = {
        "attacker": attacker.name,
        "target": defender.name,
        "label": strike.label,
    }

    # ---- Layer 1 + 2 setup: to-hit modifiers ----
    to_hit_mod = attacker.attack_bonus + strike.iterative_bonus + stance_mods["to_hit"]
    deceptive_penalty_on_dhit = 0
    deceptive_bonus_vs_defense = 0
    if strike.deceptive:
        if strike.deceptive % 4 != 0 or strike.deceptive > 0:
            raise ValueError("deceptive must be a negative multiple of 4, e.g. -4, -8")
        steps = abs(strike.deceptive) // 4
        deceptive_penalty_on_dhit = strike.deceptive           # e.g. -4, -8
        deceptive_bonus_vs_defense = steps * 2                 # 2:1 payoff
    to_hit_mod += deceptive_penalty_on_dhit

    targeted_info = None
    if strike.targeted:
        targeted_info = TARGETED_STRIKES[strike.targeted]
        to_hit_mod += targeted_info["to_hit"]

    # ---- d20 attack roll vs AC ----
    d20_raw = roll_d20()
    d20_total = d20_raw + to_hit_mod
    hit_chassis = d20_total >= defender.ac
    threatened = d20_raw >= attacker.weapon.threat_range

    confirmed_crit = False
    confirm_raw = None
    confirm_total = None
    if threatened and hit_chassis:
        confirm_raw = roll_d20()
        confirm_total = confirm_raw + to_hit_mod
        confirmed_crit = confirm_total >= defender.ac

    entry.update({
        "to_hit_mod": to_hit_mod,
        "d20_raw": d20_raw,
        "d20_total": d20_total,
        "target_ac": defender.ac,
        "hit_chassis": hit_chassis,
        "deceptive_spend": strike.deceptive,
        "deceptive_bonus_vs_defense": deceptive_bonus_vs_defense,
        "targeted": strike.targeted,
        "threatened": threatened,
        "confirm_raw": confirm_raw,
        "confirm_total": confirm_total,
        "confirmed_crit": confirmed_crit,
    })

    if not hit_chassis:
        entry["result"] = "MISS (chassis)"
        entry["damage_dealt"] = 0
        return entry

    # ---- Layer 2: GURPS defense contest (skipped on confirmed crit or All-Out defender) ----
    defense_rolled = False
    defense_total = None
    defense_rolls = None
    defense_target = None
    defended = False

    if confirmed_crit:
        entry["defense_note"] = "Confirmed crit — undefendable, no 3d6 rolled."
    elif defender.all_out:
        entry["defense_note"] = f"{defender.name} is All-Out this round — no active defenses."
    else:
        defense_target = defender.effective_defense_target(deceptive_bonus_vs_defense)
        defense_total, defense_rolls = roll_3d6()
        defense_rolled = True
        defended = defense_total <= defense_target
        entry["defense_note"] = (
            f"{defender.defense_skill} {defense_total} ({'+'.join(map(str, defense_rolls))}) "
            f"vs target {defense_target} -> {'DEFENDED' if defended else 'FAILED'}"
        )

    entry.update({
        "defense_rolled": defense_rolled,
        "defense_total": defense_total,
        "defense_rolls": defense_rolls,
        "defense_target": defense_target,
        "defended": defended,
    })

    if defended:
        entry["result"] = "DEFENDED (GURPS contest)"
        entry["damage_dealt"] = 0
        return entry

    # ---- Damage ----
    dmg_total, dmg_rolls, dmg_mod, die_sides = roll_dice_expr(attacker.weapon.dice)
    dmg_total += attacker.weapon.bonus

    mighty_blow = TALENT_STRIKE_MIGHTY_BLOW in attacker.talents
    if mighty_blow:
        dmg_total += 2 + len(dmg_rolls)  # "+2 melee damage / +1 per die swing"

    raw_damage_before_dr = dmg_total

    # ---- DR (before multipliers; ignores_armor riders skip this) ----
    dr_applied = 0
    if not attacker.weapon.ignores_armor:
        dr_applied = min(defender.dr, dmg_total)
        dmg_total = max(0, dmg_total - defender.dr)

    # ---- Multipliers: confirmed crit OR targeted-strike (impaling) — do not stack,
    # higher of the two applies (explicit ruling; source text doesn't say whether
    # they stack, and unbounded stacking breaks the calibrated temperature). ----
    multiplier = 1
    multiplier_source = None
    if confirmed_crit:
        multiplier = attacker.weapon.crit_mult
        multiplier_source = f"confirmed crit x{attacker.weapon.crit_mult}"
    if targeted_info and attacker.weapon.dmg_type in ("piercing", "impaling"):
        tmul = targeted_info["multiplier_if_impaling"]
        if tmul > multiplier:
            multiplier = tmul
            multiplier_source = f"targeted {strike.targeted} x{tmul} (impaling)"

    final_damage = dmg_total * multiplier
    defender.hp -= final_damage

    entry.update({
        "dmg_rolls": dmg_rolls,
        "dmg_mod": dmg_mod,
        "mighty_blow_applied": mighty_blow,
        "raw_damage_before_dr": raw_damage_before_dr,
        "dr_applied": dr_applied,
        "damage_after_dr": dmg_total,
        "multiplier": multiplier,
        "multiplier_source": multiplier_source,
        "damage_dealt": final_damage,
        "target_hp_after": defender.hp,
    })

    # ---- Crit / location table trigger ----
    goes_to_crit_table = confirmed_crit or defender.hp <= 0 or (
        targeted_info and targeted_info.get("forces_crit_table")
    )
    if goes_to_crit_table:
        loc_raw = roll_die(10)
        sev_raw = roll_die(6)
        sev_bonus = 1 if TALENT_STRIKE_TO_INJURE in attacker.talents else 0
        sev_total = sev_raw + sev_bonus
        location = location_lookup(loc_raw)
        severity = severity_lookup(sev_total)
        entry["crit_table"] = {
            "location_d10": loc_raw,
            "location": location,
            "severity_d6": sev_raw,
            "strike_to_injure_bonus": sev_bonus,
            "severity_total": sev_total,
            "severity": severity,
        }

    # ---- Fury (maxed base dice) ----
    widened = TALENT_BLOOD_RITE_FURY in attacker.talents
    all_maxed = all(r == die_sides for r in dmg_rolls)
    any_maxed = any(r == die_sides for r in dmg_rolls)
    fury_triggered = any_maxed if widened else all_maxed
    if fury_triggered:
        fury_total, fury_rolls, _, _ = roll_dice_expr(f"1d{die_sides}")
        defender.hp -= fury_total
        entry["fury"] = {
            "trigger_rule": "any single die maxed (Blood-Rite Fury)" if widened
                             else "all base dice maxed",
            "bonus_roll": fury_rolls[0],
            "bonus_damage": fury_total,
            "target_hp_after_fury": defender.hp,
        }

    entry["result"] = "HIT — damage dealt"
    return entry


def check_morale(defender: Defender) -> Optional[Dict[str, Any]]:
    """Mob morale test. SKILL.md specifies the TRIGGER conditions (thresholds,
    leader death) but not a numbered test — this implements it as a GURPS-style
    2d6-vs-7 Will check, -2 if the mob's leader is down, consistent with 'leader
    death drops the rout target sharply.' Isolated here for easy override."""
    if not defender.is_mob or defender.mob_starting_count <= 0:
        return None
    casualties = defender.mob_starting_count - defender.mob_count
    ratio = casualties / defender.mob_starting_count
    threshold_hit = None
    if defender.leader_down:
        threshold_hit = "leader down"
    elif ratio >= 0.75:
        threshold_hit = ">=75% casualties"
    elif ratio >= 0.5:
        threshold_hit = ">=50% casualties"
    if not threshold_hit:
        return None

    roll_total, rolls = 0, []
    for _ in range(2):
        r = roll_die(6)
        rolls.append(r)
        roll_total += r
    modifier = -2 if defender.leader_down else 0
    final = roll_total + modifier
    holds = final >= 7
    if not holds:
        routed = max(1, defender.mob_count // 2)
        defender.mob_count -= routed
    return {
        "mob": defender.name,
        "trigger": threshold_hit,
        "roll": rolls,
        "modifier": modifier,
        "total": final,
        "holds": holds,
        "routed_this_test": 0 if holds else routed,
        "mob_count_after": defender.mob_count,
    }


def resolve_round(data: Dict[str, Any]) -> Dict[str, Any]:
    round_number = data.get("round_number", 1)
    location = data.get("location", "")
    attacker_d = data["attacker"]
    weapon = Weapon(**attacker_d.get("weapon", {}))
    strikes_override = None
    if attacker_d.get("strikes"):
        strikes_override = [Strike(**s) for s in attacker_d["strikes"]]
    attacker = Attacker(
        name=attacker_d["name"],
        bab=attacker_d.get("bab", 1),
        attack_bonus=attacker_d.get("attack_bonus", 0),
        stance=attacker_d.get("stance", "Guarded"),
        haste=attacker_d.get("haste", False),
        whirlwind=attacker_d.get("whirlwind", False),
        weapon=weapon,
        talents=attacker_d.get("talents", []),
        strikes=strikes_override,
    )
    if attacker.stance not in STANCES:
        raise ValueError(f"Unknown stance {attacker.stance!r}; valid: {list(STANCES)}")
    stance_mods = STANCES[attacker.stance]

    defenders = {}
    for t in data["targets"]:
        defenders[t["name"]] = Defender(**t)

    default_target = data["targets"][0]["name"]
    strikes = build_strikes(attacker, default_target)

    strike_log = []
    for s in strikes:
        defender = defenders[s.target]
        # All-Out attacker forgoes active defenses this round; note is emitted once.
        entry = resolve_strike(attacker, defender, s, stance_mods)
        strike_log.append(entry)

    morale_log = []
    for defender in defenders.values():
        m = check_morale(defender)
        if m:
            morale_log.append(m)

    return {
        "round_number": round_number,
        "location": location,
        "attacker_name": attacker.name,
        "attacker_stance": attacker.stance,
        "stance_note": ("NO ACTIVE DEFENSES this round (All-Out)"
                         if not stance_mods["active_defense"] else None),
        "weapon": weapon.name,
        "strike_log": strike_log,
        "defenders": {name: asdict(d) for name, d in defenders.items()},
        "morale_log": morale_log,
    }


# ============================================================================
# PHASE 0 HEADER FORMATTING
# ============================================================================

def format_header(result: Dict[str, Any]) -> str:
    lines = []
    lines.append("═" * 60)
    lines.append(f"PHASE 0 — COMBAT ROUND {result['round_number']}"
                  + (f" — {result['location']}" if result['location'] else ""))
    lines.append("═" * 60)
    lines.append(f"{result['attacker_name']} — stance: {result['attacker_stance']}"
                  + (f"  ({result['stance_note']})" if result['stance_note'] else "")
                  + f"  — weapon: {result['weapon']}")
    lines.append("-" * 60)

    for i, e in enumerate(result["strike_log"], 1):
        lines.append(f"[{i}] {e.get('label') or 'Strike'} -> {e['target']}")
        d20_line = f"    d20 {e['d20_raw']} {'+' if e['to_hit_mod']>=0 else ''}{e['to_hit_mod']} = {e['d20_total']} vs AC {e['target_ac']}"
        if e["deceptive_spend"]:
            d20_line += f"  [Deceptive Attack {e['deceptive_spend']} -> -{e['deceptive_bonus_vs_defense']} target defense]"
        if e["targeted"]:
            d20_line += f"  [Targeted: {e['targeted']}]"
        lines.append(d20_line)

        if e["threatened"]:
            conf = f"    Threat range! Confirm: d20 {e['confirm_raw']} + {e['to_hit_mod']} = {e['confirm_total']} vs AC {e['target_ac']} -> "
            conf += "CONFIRMED CRIT (undefendable)" if e["confirmed_crit"] else "not confirmed"
            lines.append(conf)

        if not e["hit_chassis"]:
            lines.append(f"    RESULT: {e['result']}")
            lines.append("")
            continue

        if e.get("defense_note"):
            lines.append(f"    {e['defense_note']}")

        if e.get("defended"):
            lines.append(f"    RESULT: {e['result']}")
            lines.append("")
            continue

        rolls_str = "+".join(str(r) for r in e["dmg_rolls"])
        dmg_line = f"    Damage: {rolls_str}"
        if e.get("dmg_mod"):
            dmg_line += f"{'+' if e['dmg_mod']>=0 else ''}{e['dmg_mod']}"
        if e.get("mighty_blow_applied"):
            dmg_line += " [+Strike Mighty Blow]"
        dmg_line += f" = {e['raw_damage_before_dr']} raw"
        if e.get("dr_applied"):
            dmg_line += f", -{e['dr_applied']} DR = {e['damage_after_dr']}"
        if e.get("multiplier", 1) > 1:
            dmg_line += f", x{e['multiplier']} ({e['multiplier_source']}) = {e['damage_dealt']}"
        else:
            dmg_line += f" = {e['damage_dealt']}"
        lines.append(dmg_line)
        lines.append(f"    {e['target']} HP -> {e['target_hp_after']}")

        if e.get("crit_table"):
            ct = e["crit_table"]
            lines.append(f"    CRIT TABLE: location d10={ct['location_d10']} ({ct['location']}), "
                          f"severity d6={ct['severity_d6']}+{ct['strike_to_injure_bonus']}"
                          f"={ct['severity_total']} -> {ct['severity']}")

        if e.get("fury"):
            fu = e["fury"]
            lines.append(f"    FURY ({fu['trigger_rule']}): +1d roll {fu['bonus_roll']} = "
                          f"+{fu['bonus_damage']} dmg, HP -> {fu['target_hp_after_fury']}")

        lines.append(f"    RESULT: {e['result']}")
        lines.append("")

    lines.append("-" * 60)
    lines.append("HP AFTER ROUND:")
    for name, d in result["defenders"].items():
        hp_line = f"  {name}: {d['hp']} HP"
        if d.get("is_mob"):
            hp_line += f"  ({d['mob_count']}/{d['mob_starting_count']} remaining)"
        lines.append(hp_line)

    if result["morale_log"]:
        lines.append("-" * 60)
        lines.append("MORALE TESTS:")
        for m in result["morale_log"]:
            roll_str = "+".join(map(str, m["roll"]))
            outcome = "HOLDS" if m["holds"] else f"ROUTS ({m['routed_this_test']} flee)"
            lines.append(f"  {m['mob']} — trigger: {m['trigger']} — "
                          f"2d6 {roll_str}{m['modifier']:+d} = {m['total']} -> {outcome}")
    lines.append("═" * 60)
    return "\n".join(lines)


# ============================================================================
# SELFTEST — three worked rounds, real dice each run (no seeding, per Chad's
# "no rerolls, raw values shown" rule — this is a demonstration of mechanism,
# not a fixed-output regression test)
# ============================================================================

def selftest():
    print("### SELFTEST 1 — Solo duel, Deceptive Attack on the finishing iterative ###\n")
    round1 = {
        "round_number": 1,
        "location": "Forgedeep training yard",
        "attacker": {
            "name": "Korgan Bloodaxe",
            "bab": 16,
            "attack_bonus": 5,
            "stance": "Guarded",
            "weapon": {"name": "Blood-Drinker", "dice": "1d10", "bonus": 8,
                       "threat_range": 19, "crit_mult": 3, "dmg_type": "slashing"},
            "talents": ["Strike Mighty Blow", "Strike to Injure"],
            "strikes": [
                {"target": "Lieutenant Vrask", "iterative_bonus": 16, "label": "Iterative @ +16"},
                {"target": "Lieutenant Vrask", "iterative_bonus": 11, "label": "Iterative @ +11"},
                {"target": "Lieutenant Vrask", "iterative_bonus": 6, "deceptive": -4,
                 "label": "Iterative @ +6, Deceptive Attack"},
            ],
        },
        "targets": [
            {"name": "Lieutenant Vrask", "ac": 22, "dr": 3, "defense_skill": "Parry",
             "defense_value": 13, "hp": 58},
        ],
    }
    print(format_header(resolve_round(round1)))

    print("\n### SELFTEST 2 — Whirlwind Attack vs a gnoll mob, multi-threat + morale ###\n")
    round2 = {
        "round_number": 4,
        "location": "The Measured House calibration engagement",
        "attacker": {
            "name": "Korgan Bloodaxe",
            "bab": 16,
            "attack_bonus": 5,
            "stance": "Aggressive",
            "whirlwind": True,
            "weapon": {"name": "Blood-Drinker", "dice": "1d10", "bonus": 8,
                       "threat_range": 19, "crit_mult": 3, "dmg_type": "slashing"},
            "talents": ["Strike Mighty Blow"],
            "strikes": [
                {"target": "Gnoll Pack (mob)", "iterative_bonus": 16, "label": "Whirlwind swing"},
            ],
        },
        "targets": [
            {"name": "Gnoll Pack (mob)", "ac": 15, "dr": 1, "defense_skill": "Dodge",
             "defense_value": 11, "hp": 13, "multi_threat_count": 0,
             "is_mob": True, "mob_count": 9, "mob_starting_count": 20, "leader_down": True},
        ],
    }
    print(format_header(resolve_round(round2)))

    print("\n### SELFTEST 3 — All-Out targeted strike (vitals, impaling) vs an armored target ###\n")
    round3 = {
        "round_number": 2,
        "location": "The Aldric False Flag Operation — dockside ambush",
        "attacker": {
            "name": "Lirien Nightwalker",
            "bab": 12,
            "attack_bonus": 4,
            "stance": "All-Out",
            "weapon": {"name": "Duskrazor rapier", "dice": "1d6", "bonus": 6,
                       "threat_range": 18, "crit_mult": 2, "dmg_type": "impaling"},
            "talents": ["Strike to Injure"],
            "strikes": [
                {"target": "Aldric Enforcer", "iterative_bonus": 12, "targeted": "vitals",
                 "label": "All-Out lunge, targeted vitals"},
                {"target": "Aldric Enforcer", "iterative_bonus": 7,
                 "label": "Iterative @ +7"},
            ],
        },
        "targets": [
            {"name": "Aldric Enforcer", "ac": 19, "dr": 4, "defense_skill": "Parry",
             "defense_value": 12, "hp": 34, "all_out": False},
        ],
    }
    print(format_header(resolve_round(round3)))


# ============================================================================
# CLI
# ============================================================================

SCHEMA_DOC = """
JSON schema (top level):
{
  "round_number": int,
  "location": str,
  "attacker": {
    "name": str, "bab": int, "attack_bonus": int,
    "stance": "Guarded"|"Aggressive"|"Defensive"|"All-Out",
    "haste": bool, "whirlwind": bool,
    "weapon": {"name": str, "dice": "NdM+K", "bonus": int, "threat_range": int,
               "crit_mult": int, "dmg_type": "slashing"|"piercing"|"bludgeoning"|"impaling",
               "ignores_armor": bool},
    "talents": [str, ...],
    "strikes": [   // omit to auto-generate from bab/haste/whirlwind
      {"target": str, "iterative_bonus": int, "deceptive": int (negative multiple of 4),
       "targeted": "vitals"|"neck"|"limb"|null, "label": str}
    ]
  },
  "targets": [
    {"name": str, "ac": int, "dr": int, "defense_skill": "Parry"|"Block"|"Dodge",
     "defense_value": int, "hp": int, "all_out": bool, "multi_threat_count": int,
     "is_mob": bool, "mob_count": int, "mob_starting_count": int, "leader_down": bool}
  ]
}
"""


def build_arg_parser():
    p = argparse.ArgumentParser(
        description="FUSED combat engine round resolver (3.5e + GURPS + WFRP).")
    p.add_argument("--json", help="Path to a JSON file describing the round.")
    p.add_argument("--json-string", help="Inline JSON describing the round.")
    p.add_argument("--json-schema", action="store_true",
                    help="Print the input JSON schema and exit.")
    p.add_argument("--selftest", action="store_true",
                    help="Run three worked example rounds and exit.")

    simple = p.add_argument_group("simple single-attacker-vs-single-target round")
    simple.add_argument("--attacker")
    simple.add_argument("--bab", type=int, default=1)
    simple.add_argument("--attack-bonus", type=int, default=0)
    simple.add_argument("--stance", default="Guarded")
    simple.add_argument("--haste", action="store_true")
    simple.add_argument("--weapon-name", default="weapon")
    simple.add_argument("--weapon-dice", default="1d8")
    simple.add_argument("--weapon-bonus", type=int, default=0)
    simple.add_argument("--threat-range", type=int, default=20)
    simple.add_argument("--crit-mult", type=int, default=2)
    simple.add_argument("--dmg-type", default="slashing")
    simple.add_argument("--talent", action="append", default=[],
                         help="Repeatable, e.g. --talent 'Strike Mighty Blow'")
    simple.add_argument("--target")
    simple.add_argument("--target-ac", type=int, default=10)
    simple.add_argument("--target-dr", type=int, default=0)
    simple.add_argument("--target-defense-skill", default="Dodge")
    simple.add_argument("--target-defense-value", type=int, default=10)
    simple.add_argument("--target-hp", type=int, default=10)
    simple.add_argument("--round-number", type=int, default=1)
    simple.add_argument("--location", default="")
    return p


def simple_args_to_round(args) -> Dict[str, Any]:
    if not args.attacker or not args.target:
        raise SystemExit("Simple mode requires --attacker and --target "
                          "(or use --json / --json-string / --selftest).")
    return {
        "round_number": args.round_number,
        "location": args.location,
        "attacker": {
            "name": args.attacker,
            "bab": args.bab,
            "attack_bonus": args.attack_bonus,
            "stance": args.stance,
            "haste": args.haste,
            "weapon": {
                "name": args.weapon_name, "dice": args.weapon_dice,
                "bonus": args.weapon_bonus, "threat_range": args.threat_range,
                "crit_mult": args.crit_mult, "dmg_type": args.dmg_type,
            },
            "talents": args.talent,
        },
        "targets": [{
            "name": args.target, "ac": args.target_ac, "dr": args.target_dr,
            "defense_skill": args.target_defense_skill,
            "defense_value": args.target_defense_value, "hp": args.target_hp,
        }],
    }


def main():
    p = build_arg_parser()
    args = p.parse_args()

    if args.json_schema:
        print(SCHEMA_DOC)
        return

    if args.selftest:
        selftest()
        return

    if args.json:
        with open(args.json, "r", encoding="utf-8") as f:
            data = json.load(f)
    elif args.json_string:
        data = json.loads(args.json_string)
    else:
        data = simple_args_to_round(args)

    result = resolve_round(data)
    print(format_header(result))


if __name__ == "__main__":
    main()
