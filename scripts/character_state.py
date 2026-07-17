#!/usr/bin/env python3
"""
character_state.py — persistent character sheet + active buff engine
The New Path campaign engine (the-new-path-engine)

The Project Infinity role in this stack: the character lives as DATA the
scripts mutate — not as prose the GM re-reads and mis-remembers. Buffs
auto-apply their stat deltas when cast, stack by 3.5e RAW typed-bonus
rules, tick down by duration, and auto-revert on expiry or dispel. The
computed sheet (AC breakdown, attack line, saves) is derived live from
base + active effects, never hand-edited.

GOVERNING RULES (3.5e RAW):
    Bonus stacking — PH p.171 / DMG p.21: bonuses of the same named type
    do NOT stack (highest applies). DODGE bonuses always stack, as do
    CIRCUMSTANCE bonuses from different sources, and all UNNAMED bonuses.
    Penalties always stack. This is the rule humans fumble mid-fight;
    the engine holds it.

DESIGN CONTRACT (repo README):
    - State lives in an explicit character file passed by path
      (*.character.json — the OPERATIONAL mirror; Notion remains canon,
      sync at session end). Buff durations tick in ROUNDS.
    - Real dice where dice are needed: python secrets, raw shown first.
    - Visible output: every command prints the receipt and the computed
      lines it changed.
    - No cross-imports. combat_registry reads HP; this owns the sheet.

USAGE
    python3 character_state.py arik.character.json new "Arik Baen" \
        --str 22 --dex 18 --con 20 --int 16 --wis 18 --cha 16 \
        --hp 196 --bab 13 --fort 12 --ref 11 --will 12 \
        --ac-armor 8 --ac-natural 2 --ac-deflection 2
    python3 character_state.py arik.character.json show
    python3 character_state.py arik.character.json buff haste --cl 18
    python3 character_state.py arik.character.json buff "bull's strength" --cl 12
    python3 character_state.py arik.character.json buff-custom "war chant" \
        --bonus morale --attack 2 --saves 1 --rounds 10
    python3 character_state.py arik.character.json tick        # one round
    python3 character_state.py arik.character.json tick 10
    python3 character_state.py arik.character.json dispel haste
    python3 character_state.py arik.character.json --selftest
"""

import argparse
import json
import math
import os
import secrets
import sys
from typing import Dict, List, Optional

# ============================================================================
# 3.5e BONUS TYPES — stacking law (PH 171)
# ============================================================================

STACKING = {
    "alchemical": False, "armor": False, "circumstance": True,
    "competence": False, "deflection": False, "dodge": True,
    "enhancement": False, "insight": False, "luck": False,
    "morale": False, "natural": False, "profane": False,
    "racial": False, "resistance": False, "sacred": False,
    "shield": False, "size": False, "unnamed": True, "untyped": True,
}

# Stat keys the engine computes over
STATS = ("str", "dex", "con", "int", "wis", "cha",
         "attack", "damage", "ac", "touch_ac", "ff_ac",
         "fort", "ref", "will", "saves", "speed", "hp_temp")

# ============================================================================
# BUFF LIBRARY — high-frequency spells, RAW effects
#   delta keys: stat -> (bonus_type, amount or callable(cl))
#   duration in ROUNDS (min/level = 10 * CL rounds)
# ============================================================================

def _rounds_min_per_cl(cl): return 10 * cl
def _rounds_hr_per_cl(cl): return 600 * cl

BUFFS: Dict[str, dict] = {
    "haste": {
        "source": "PH 239",
        "duration": lambda cl: cl,
        "deltas": {"attack": ("unnamed", 1), "ac": ("dodge", 1),
                   "ref": ("dodge", 1), "speed": ("enhancement", 30)},
        "notes": "One extra attack on a full attack (not stat-computable); "
                 "+30 ft enhancement to speed capped at double base.",
    },
    "bless": {
        "source": "PH 205",
        "duration": lambda cl: _rounds_min_per_cl(cl),
        "deltas": {"attack": ("morale", 1)},
        "notes": "+1 morale on attacks and on saves vs. fear (fear rider "
                 "not auto-computed).",
    },
    "prayer": {
        "source": "PH 264",
        "duration": lambda cl: cl,
        "deltas": {"attack": ("luck", 1), "damage": ("luck", 1),
                   "saves": ("luck", 1)},
        "notes": "Also -1 luck penalty to enemies in area (track on their "
                 "side); skill checks +1 luck.",
    },
    "heroism": {
        "source": "PH 240",
        "duration": lambda cl: _rounds_min_per_cl(cl) * 10,
        "deltas": {"attack": ("morale", 2), "saves": ("morale", 2)},
        "notes": "10 min/level. +2 morale on attacks, saves, and skill "
                 "checks.",
    },
    "greater heroism": {
        "source": "PH 240",
        "duration": lambda cl: _rounds_min_per_cl(cl),
        "deltas": {"attack": ("morale", 4), "saves": ("morale", 4),
                   "hp_temp": ("untyped", lambda cl: min(cl, 20))},
        "notes": "+4 morale attacks/saves/skills, immunity to fear, "
                 "temp hp = CL (max 20).",
    },
    "divine favor": {
        "source": "PH 224",
        "duration": lambda cl: 10,
        "deltas": {"attack": ("luck", lambda cl: min(3, max(1, cl // 3))),
                   "damage": ("luck", lambda cl: min(3, max(1, cl // 3)))},
        "notes": "+1/3 levels (max +3) luck to attack and damage. 1 minute.",
    },
    "shield": {
        "source": "PH 278",
        "duration": lambda cl: _rounds_min_per_cl(cl),
        "deltas": {"ac": ("shield", 4)},
        "notes": "+4 shield bonus (applies to touch? No — shield bonus, "
                 "not vs touch); negates magic missile.",
    },
    "mage armor": {
        "source": "PH 249",
        "duration": lambda cl: _rounds_hr_per_cl(cl),
        "deltas": {"ac": ("armor", 4)},
        "notes": "+4 armor bonus; applies vs. incorporeal touch.",
    },
    "barkskin": {
        "source": "PH 202",
        "duration": lambda cl: _rounds_min_per_cl(cl),
        "deltas": {"ac": ("natural", lambda cl: min(5, 2 + max(0, (cl - 3) // 3)))},
        "notes": "Enhancement to existing natural armor by RAW wording; "
                 "tracked as 'natural' slot here so it collides with "
                 "natural-armor buffs, which is the RAW outcome.",
    },
    "bull's strength": {
        "source": "PH 207",
        "duration": lambda cl: _rounds_min_per_cl(cl),
        "deltas": {"str": ("enhancement", 4)},
        "notes": "",
    },
    "cat's grace": {
        "source": "PH 208",
        "duration": lambda cl: _rounds_min_per_cl(cl),
        "deltas": {"dex": ("enhancement", 4)},
        "notes": "",
    },
    "bear's endurance": {
        "source": "PH 203",
        "duration": lambda cl: _rounds_min_per_cl(cl),
        "deltas": {"con": ("enhancement", 4)},
        "notes": "Con-based hp shift applies while active.",
    },
    "shield of faith": {
        "source": "PH 278",
        "duration": lambda cl: _rounds_min_per_cl(cl),
        "deltas": {"ac": ("deflection", lambda cl: min(5, 2 + cl // 6))},
        "notes": "+2 deflection, +1 per 6 levels (max +5). Applies to touch.",
    },
    "protection from evil": {
        "source": "PH 266",
        "duration": lambda cl: _rounds_min_per_cl(cl),
        "deltas": {"ac": ("deflection", 2), "saves": ("resistance", 2)},
        "notes": "Bonuses apply vs. EVIL attackers only — engine applies "
                 "them; drop mentally vs. non-evil.",
    },
    "righteous might": {
        "source": "PH 273",
        "duration": lambda cl: cl,
        "deltas": {"str": ("size", 4), "con": ("size", 2),
                   "ac": ("natural", 2), "attack": ("size", -1)},
        "notes": "Size increase to Large: -1 size to AC and attack, reach "
                 "10 ft, DR /evil or /good by caster. AC size penalty "
                 "folded into the attack line note; natural +2 "
                 "enhancement.",
    },
    "stoneskin": {
        "source": "PH 284",
        "duration": lambda cl: _rounds_min_per_cl(cl),
        "deltas": {},
        "notes": "DR 10/adamantine, absorbs 10/level (max 150) points. "
                 "Tracked as note; no stat delta.",
    },
    "false life": {
        "source": "PH 229",
        "duration": lambda cl: _rounds_hr_per_cl(cl),
        "deltas": {"hp_temp": ("untyped", lambda cl: min(cl, 10))},
        "notes": "1d10 + CL (max +10) temp hp by RAW — engine applies "
                 "CL-cap flat; roll the d10 and set exact with "
                 "buff-custom if you want the die.",
    },
}

# ============================================================================
# STATE FILE
# ============================================================================

def load(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path: str, st: dict) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(st, f, indent=1)
    os.replace(tmp, path)

# ============================================================================
# STACKING RESOLUTION
# ============================================================================

def resolve_stat(st: dict, stat: str) -> Dict[str, object]:
    """Total active-effect modifier for one stat, RAW stacking applied.
    Returns {'total': int, 'lines': [readable breakdown]}."""
    by_type: Dict[str, List] = {}
    for eff in st.get("effects", []):
        for dstat, (btype, amt) in eff["deltas"].items():
            targets = [dstat]
            if dstat == "saves":
                pass  # handled by callers folding saves into fort/ref/will
            if dstat != stat:
                continue
            by_type.setdefault(btype, []).append((eff["name"], amt))
    total = 0
    lines = []
    for btype, entries in sorted(by_type.items()):
        if STACKING.get(btype, True):
            for name, amt in entries:
                total += amt
                lines.append(f"{amt:+d} {btype} ({name})")
        else:
            pos = [(a, n) for n, a in entries if a > 0]
            neg = [(a, n) for n, a in entries if a < 0]
            if pos:
                best = max(pos)
                total += best[0]
                lines.append(f"{best[0]:+d} {btype} ({best[1]})")
                for a, n in pos:
                    if (a, n) != best:
                        lines.append(f"    [{a:+d} {btype} ({n}) — does not stack]")
            for a, n in neg:      # penalties always stack
                total += a
                lines.append(f"{a:+d} {btype} penalty ({n})")
    return {"total": total, "lines": lines}


def effective(st: dict, stat: str) -> int:
    base = st["base"].get(stat, 0)
    mod = resolve_stat(st, stat)["total"]
    if stat in ("fort", "ref", "will"):
        mod += resolve_stat(st, "saves")["total"]
    return base + mod


def ability_mod(score: int) -> int:
    return (score - 10) // 2

# ============================================================================
# COMMANDS
# ============================================================================

def cmd_new(path: str, name: str, args) -> None:
    st = {
        "name": name,
        "round": 0,
        "base": {
            "str": args.str, "dex": args.dex, "con": args.con,
            "int": args.int_, "wis": args.wis, "cha": args.cha,
            "hp_max": args.hp, "bab": args.bab,
            "fort": args.fort, "ref": args.ref, "will": args.will,
            "speed": args.speed,
            "ac_armor": args.ac_armor, "ac_shield": args.ac_shield,
            "ac_natural": args.ac_natural, "ac_deflection": args.ac_deflection,
            "ac_dodge": args.ac_dodge, "ac_misc": args.ac_misc,
            "attack": 0, "damage": 0, "saves": 0, "ac": 0,
            "hp_temp": 0,
        },
        "classes": {},
        "cp": {"unspent": 0, "log": []},
        "effects": [],
    }
    st["base"]["hp_cur"] = st["base"]["hp_max"]
    save(path, st)
    print(f"Created {st['name']} -> {path}")
    cmd_show(path)


def _materialize(name: str, spec: dict, cl: int) -> dict:
    deltas = {}
    for stat, (btype, amt) in spec["deltas"].items():
        val = amt(cl) if callable(amt) else amt
        deltas[stat] = (btype, val)
    dur = spec["duration"](cl)
    return {"name": name, "cl": cl, "rounds_left": dur,
            "deltas": deltas, "source": spec.get("source", ""),
            "notes": spec.get("notes", "")}


def cmd_buff(path: str, name: str, cl: int) -> None:
    st = load(path)
    key = name.strip().lower()
    if key not in BUFFS:
        near = [b for b in BUFFS if key in b]
        print(f"Unknown buff '{name}'."
              + (f" Close: {', '.join(near)}" if near else
                 " Use buff-custom for anything not in the library."),
              file=sys.stderr)
        sys.exit(1)
    if any(e["name"] == key for e in st["effects"]):
        print(f"{st['name']}: '{key}' already active — recast rejected "
              "(same spell doesn't stack with itself; dispel first to "
              "refresh).")
        return
    eff = _materialize(key, BUFFS[key], cl)
    st["effects"].append(eff)
    save(path, st)
    d = ", ".join(f"{s} {b}{'+' if isinstance(v,int) and v>=0 else ''}{v}"
                  for s, (b, v) in eff["deltas"].items())
    print(f"{st['name']}: {key.upper()} (CL {cl}) active — "
          f"{eff['rounds_left']} rounds. [{d}]")
    if eff["notes"]:
        print(f"  note: {eff['notes']}")
    _print_computed(st)


def cmd_buff_custom(path: str, name: str, args) -> None:
    st = load(path)
    deltas = {}
    for stat in ("attack", "damage", "ac", "fort", "ref", "will", "saves",
                 "str", "dex", "con", "wis", "cha", "speed", "hp_temp"):
        v = getattr(args, stat.replace("hp_temp", "hp_temp"), None) \
            if stat != "int" else None
        v = getattr(args, stat, None)
        if v:
            deltas[stat] = (args.bonus, v)
    if not deltas:
        print("buff-custom needs at least one stat flag "
              "(--attack/--ac/--saves/...)", file=sys.stderr)
        sys.exit(2)
    eff = {"name": name.lower(), "cl": 0, "rounds_left": args.rounds,
           "deltas": deltas, "source": "custom", "notes": args.note or ""}
    st["effects"].append(eff)
    save(path, st)
    print(f"{st['name']}: {name.upper()} active — {args.rounds} rounds "
          f"({args.bonus} bonus).")
    _print_computed(st)


def cmd_dispel(path: str, name: str) -> None:
    st = load(path)
    key = name.strip().lower()
    before = len(st["effects"])
    st["effects"] = [e for e in st["effects"] if e["name"] != key]
    if len(st["effects"]) == before:
        print(f"'{key}' not active.", file=sys.stderr)
        sys.exit(1)
    save(path, st)
    print(f"{st['name']}: {key.upper()} ended — deltas reverted.")
    _print_computed(st)


def cmd_tick(path: str, n: int) -> None:
    st = load(path)
    st["round"] += n
    expired = []
    for e in st["effects"]:
        e["rounds_left"] -= n
        if e["rounds_left"] <= 0:
            expired.append(e["name"])
    st["effects"] = [e for e in st["effects"] if e["rounds_left"] > 0]
    save(path, st)
    print(f"{st['name']}: round {st['round']} (+{n})")
    for name in expired:
        print(f"  EXPIRED: {name.upper()} — deltas reverted.")
    if st["effects"]:
        for e in sorted(st["effects"], key=lambda x: x["rounds_left"]):
            print(f"  active: {e['name']} ({e['rounds_left']}r left)")
    else:
        print("  no active effects")


def _print_computed(st: dict) -> None:
    b = st["base"]
    eff_str = b["str"] + resolve_stat(st, "str")["total"]
    eff_dex = b["dex"] + resolve_stat(st, "dex")["total"]
    eff_con = b["con"] + resolve_stat(st, "con")["total"]
    con_shift = (ability_mod(eff_con) - ability_mod(b["con"]))
    level_est = b["hp_max"] // 10  # display aid only for hp shift note

    ac_mod = resolve_stat(st, "ac")
    dex_mod = ability_mod(eff_dex)
    ac_total = (10 + b["ac_armor"] + b["ac_shield"] + b["ac_natural"]
                + b["ac_deflection"] + b["ac_dodge"] + b["ac_misc"]
                + dex_mod + ac_mod["total"])
    atk_mod = resolve_stat(st, "attack")
    str_mod = ability_mod(eff_str)
    melee = b["bab"] + str_mod + atk_mod["total"]
    tmp = resolve_stat(st, "hp_temp")["total"]

    print("-" * 62)
    print(f"COMPUTED — {st['name']}  (round {st['round']})")
    print(f"  STR {eff_str} ({str_mod:+d})  DEX {eff_dex} "
          f"({dex_mod:+d})  CON {eff_con}"
          + (f"  [hp {'+' if con_shift>=0 else ''}{con_shift}/HD while active]"
             if con_shift else ""))
    print(f"  AC {ac_total}  (10 + armor {b['ac_armor']} + shield "
          f"{b['ac_shield']} + nat {b['ac_natural']} + defl "
          f"{b['ac_deflection']} + dodge {b['ac_dodge']} + misc "
          f"{b['ac_misc']} + Dex {dex_mod:+d} + effects "
          f"{ac_mod['total']:+d})")
    for ln in ac_mod["lines"]:
        print(f"      {ln}")
    print(f"  Melee +{melee}  (BAB +{b['bab']} + Str {str_mod:+d} + "
          f"effects {atk_mod['total']:+d})")
    for ln in atk_mod["lines"]:
        print(f"      {ln}")
    saves_mod = resolve_stat(st, "saves")["total"]
    print(f"  Fort +{effective(st,'fort')}  Ref +{effective(st,'ref')}  "
          f"Will +{effective(st,'will')}"
          + (f"  (incl. {saves_mod:+d} all-saves effects)" if saves_mod else ""))
    if tmp:
        print(f"  Temp HP: {tmp}")
    print("-" * 62)


def cmd_show(path: str) -> None:
    st = load(path)
    if st["effects"]:
        print(f"ACTIVE EFFECTS ({st['name']}):")
        for e in sorted(st["effects"], key=lambda x: x["rounds_left"]):
            d = ", ".join(f"{s} {b} {v:+d}" for s, (b, v) in e["deltas"].items())
            print(f"  {e['name']} — {e['rounds_left']}r left  [{d}]"
                  f"  ({e['source']})")
    else:
        print(f"No active effects on {st['name']}.")
    _print_computed(st)


# ============================================================================
# CLASS PROGRESSION (PH Ch.3) — per-class RAW summation for multiclass
# ============================================================================

CLASSES = {
    #  name        HD  BAB      Fort   Ref    Will   skill pts/lvl
    "barbarian": (12, "good", "good", "poor", "poor", 4),
    "bard":      (6, "avg", "poor", "good", "good", 6),
    "cleric":    (8, "avg", "good", "poor", "good", 2),
    "druid":     (8, "avg", "good", "poor", "good", 4),
    "fighter":   (10, "good", "good", "poor", "poor", 2),
    "monk":      (8, "avg", "good", "good", "good", 4),
    "paladin":   (10, "good", "good", "poor", "poor", 2),
    "ranger":    (8, "good", "good", "good", "poor", 6),
    "rogue":     (6, "avg", "poor", "good", "poor", 8),
    "sorcerer":  (4, "poor", "poor", "poor", "good", 2),
    "wizard":    (4, "poor", "poor", "poor", "good", 2),
}

def _bab_for(kind: str, lvl: int) -> int:
    return {"good": lvl, "avg": (3 * lvl) // 4, "poor": lvl // 2}[kind]

def _save_for(kind: str, lvl: int) -> int:
    return (2 + lvl // 2) if kind == "good" else lvl // 3

def derived_progression(classes: Dict[str, int]) -> Dict[str, int]:
    out = {"bab": 0, "fort": 0, "ref": 0, "will": 0}
    for cname, lvl in classes.items():
        if cname not in CLASSES or lvl <= 0:
            continue
        hd, bab, f, r, w, sp = CLASSES[cname]
        out["bab"] += _bab_for(bab, lvl)
        out["fort"] += _save_for(f, lvl)
        out["ref"] += _save_for(r, lvl)
        out["will"] += _save_for(w, lvl)
    return out

FEAT_LEVELS = {1, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30}
ABILITY_LEVELS = {4, 8, 12, 16, 20, 24, 28}


def _roll_hd(sides: int) -> int:
    throws = [1 + secrets.randbelow(sides) for _ in range(4)]
    print(f"  HD d{sides} raw: {throws}")
    counts = {}
    for t in throws:
        counts[t] = counts.get(t, 0) + 1
    best = max(counts.values())
    modes = [v for v, c in counts.items() if c == best]
    if best > 1 and len(modes) == 1:
        bound = modes[0]
        how = "mode"
    else:
        s = sorted(throws)
        bound = (s[1] + s[2] + 1) // 2
        how = "median"
    print(f"  bound: {bound} ({how})")
    return bound


def cmd_level_up(path: str, cname: str) -> None:
    st = load(path)
    key = cname.strip().lower()
    if key not in CLASSES:
        print(f"Unknown class '{cname}'. Known: {', '.join(sorted(CLASSES))}",
              file=sys.stderr)
        sys.exit(1)
    st.setdefault("classes", {})
    st.setdefault("cp", {"unspent": 0, "log": []})
    before = derived_progression(st["classes"])
    st["classes"][key] = st["classes"].get(key, 0) + 1
    after = derived_progression(st["classes"])
    total_lvl = sum(st["classes"].values())
    hd, babk, fk, rk, wk, sp = CLASSES[key]
    con_m = ability_mod(st["base"]["con"])
    print(f"{st['name']} -> {key} {st['classes'][key]} "
          f"(character level {total_lvl})")
    if total_lvl == 1:
        hp_gain = hd + con_m
        print(f"  HD d{hd}: MAX at level 1 -> {hd}")
    else:
        hp_gain = _roll_hd(hd) + con_m
    hp_gain = max(1, hp_gain)
    st["base"]["hp_max"] += hp_gain
    st["base"]["hp_cur"] = st["base"].get("hp_cur", st["base"]["hp_max"] - hp_gain) + hp_gain
    print(f"  HP +{hp_gain} (Con {con_m:+d}) -> {st['base']['hp_max']} max")
    for stat in ("bab", "fort", "ref", "will"):
        d = after[stat] - before[stat]
        if d:
            st["base"][stat if stat != "bab" else "bab"] += d
            print(f"  {stat.upper()} +{d} -> +{st['base'][stat]}")
    int_m = ability_mod(st["base"]["int"])
    pts = max(1, sp + int_m) * (4 if total_lvl == 1 else 1)
    print(f"  Skill points: {pts} ({key} {sp} + Int {int_m:+d}"
          + (", x4 first level)" if total_lvl == 1 else ")"))
    if total_lvl in FEAT_LEVELS:
        print(f"  FEAT due at character level {total_lvl} — pick at table, "
              "log in Notion register.")
    if total_lvl in ABILITY_LEVELS:
        print(f"  ABILITY INCREASE due at character level {total_lvl}.")
    save(path, st)


def cmd_rest(path: str, hours: int, bed: bool) -> None:
    st = load(path)
    rounds = hours * 600
    st["round"] += rounds
    expired = [e["name"] for e in st["effects"] if e["rounds_left"] <= rounds]
    for e in st["effects"]:
        e["rounds_left"] -= rounds
    st["effects"] = [e for e in st["effects"] if e["rounds_left"] > 0]
    lvl = max(1, sum(st.get("classes", {}).values()))
    healed = 0
    if hours >= 8:
        rate = lvl * (2 if bed else 1)
        cur = st["base"].get("hp_cur", st["base"]["hp_max"])
        healed = min(rate, st["base"]["hp_max"] - cur)
        st["base"]["hp_cur"] = cur + healed
    save(path, st)
    print(f"{st['name']}: rested {hours}h"
          + (" (full bed rest)" if bed else "") + f" — +{rounds} rounds.")
    for n in expired:
        print(f"  EXPIRED: {n.upper()} — deltas reverted.")
    if healed:
        print(f"  Natural healing: +{healed} hp "
              f"({st['base']['hp_cur']}/{st['base']['hp_max']}) "
              "[PH 146: 1 hp/level/night, x2 bed rest]")
    print("  Prepared casters: slots refresh after rest + prep — "
          "handle at table.")


def cmd_cp(path: str, sub: str, amount: int, note: str) -> None:
    st = load(path)
    st.setdefault("cp", {"unspent": 0, "log": []})
    if sub == "add":
        st["cp"]["unspent"] += amount
        st["cp"]["log"].append(f"+{amount} {note}".strip())
    elif sub == "spend":
        if amount > st["cp"]["unspent"]:
            print(f"REFUSED: {amount} CP > {st['cp']['unspent']} unspent.",
                  file=sys.stderr)
            sys.exit(1)
        st["cp"]["unspent"] -= amount
        st["cp"]["log"].append(f"-{amount} {note}".strip())
    save(path, st)
    print(f"{st['name']}: CP {st['cp']['unspent']} unspent.")
    for line in st["cp"]["log"][-6:]:
        print(f"  {line}")

# ============================================================================
# SELFTEST — stacking law + library math
# ============================================================================

def selftest() -> int:
    failures = 0

    def check(desc, ok):
        nonlocal failures
        print(f"  [{'PASS' if ok else 'FAIL'}] {desc}")
        if not ok:
            failures += 1

    print("### character_state.py SELFTEST — PH 171 stacking law ###\n")
    st = {"name": "T", "round": 0,
          "base": {"str": 22, "dex": 18, "con": 20, "int": 16, "wis": 18,
                   "cha": 16, "hp_max": 196, "bab": 13, "fort": 12,
                   "ref": 11, "will": 12, "speed": 30, "ac_armor": 8,
                   "ac_shield": 0, "ac_natural": 2, "ac_deflection": 2,
                   "ac_dodge": 1, "ac_misc": 0, "attack": 0, "damage": 0,
                   "saves": 0, "ac": 0, "hp_temp": 0},
          "effects": []}

    # 1. Same-type bonuses don't stack: bless (+1 morale atk) + heroism
    #    (+2 morale atk) -> +2, not +3.
    st["effects"] = [_materialize("bless", BUFFS["bless"], 10),
                     _materialize("heroism", BUFFS["heroism"], 10)]
    r = resolve_stat(st, "attack")
    check("morale+morale on attack -> highest only (+2)", r["total"] == 2)
    check("suppressed bonus is shown in breakdown",
          any("does not stack" in x for x in r["lines"]))

    # 2. Different types stack: + divine favor CL 12 (+3 luck) -> 2+3=5
    st["effects"].append(_materialize("divine favor", BUFFS["divine favor"], 12))
    check("morale + luck stack (+5 total attack)",
          resolve_stat(st, "attack")["total"] == 5)

    # 3. Dodge always stacks: haste dodge AC +1 twice (haste + custom dodge)
    st["effects"] = [_materialize("haste", BUFFS["haste"], 18),
                     {"name": "mobility stance", "cl": 0, "rounds_left": 5,
                      "deltas": {"ac": ("dodge", 2)}, "source": "x", "notes": ""}]
    check("dodge + dodge stack (+3 AC)",
          resolve_stat(st, "ac")["total"] == 3)

    # 4. Armor spell vs worn armor: mage armor +4 armor collides with the
    #    armor SLOT conceptually — engine adds effect-armor typed; the base
    #    armor field stays; RAW: doesn't stack with worn armor bonus. Two
    #    armor-typed effects -> highest.
    st["effects"] = [_materialize("mage armor", BUFFS["mage armor"], 10),
                     {"name": "lesser bracers", "cl": 0, "rounds_left": 99,
                      "deltas": {"ac": ("armor", 3)}, "source": "x", "notes": ""}]
    check("armor + armor typed effects -> highest (+4)",
          resolve_stat(st, "ac")["total"] == 4)

    # 5. shield of faith scaling: CL 18 -> min(5, 2+3) = +5 deflection
    e = _materialize("shield of faith", BUFFS["shield of faith"], 18)
    check("shield of faith CL18 -> +5 deflection",
          e["deltas"]["ac"] == ("deflection", 5))

    # 6. barkskin scaling: CL 12 -> min(5, 2 + (12-3)//3 = 3) = 5
    e = _materialize("barkskin", BUFFS["barkskin"], 12)
    check("barkskin CL12 -> +5 natural", e["deltas"]["ac"] == ("natural", 5))

    # 7. righteous might: size penalties fold in; enhancement Str +4 size
    e = _materialize("righteous might", BUFFS["righteous might"], 15)
    check("righteous might: Str +4 size, attack -1 size",
          e["deltas"]["str"] == ("size", 4)
          and e["deltas"]["attack"] == ("size", -1))
    st["effects"] = [e]
    check("size penalty stacks into attack total (-1 net of +4 Str "
          "handled via Str mod)", resolve_stat(st, "attack")["total"] == -1)

    # 8. greater heroism temp hp: CL 18 -> 18
    e = _materialize("greater heroism", BUFFS["greater heroism"], 18)
    check("greater heroism CL18 -> 18 temp hp",
          e["deltas"]["hp_temp"] == ("untyped", 18))

    # 9. duration math: haste CL18 = 18 rounds; heroism CL10 = 6000 rounds
    check("haste CL18 -> 18 rounds",
          _materialize("haste", BUFFS["haste"], 18)["rounds_left"] == 18)
    check("heroism CL10 -> 1000 rounds (100 min)",
          _materialize("heroism", BUFFS["heroism"], 10)["rounds_left"] == 1000)

    # 10. penalties always stack even same-typed
    st["effects"] = [
        {"name": "curse a", "cl": 0, "rounds_left": 9,
         "deltas": {"attack": ("morale", -2)}, "source": "x", "notes": ""},
        {"name": "curse b", "cl": 0, "rounds_left": 9,
         "deltas": {"attack": ("morale", -1)}, "source": "x", "notes": ""},
    ]
    check("same-type penalties stack (-3)",
          resolve_stat(st, "attack")["total"] == -3)

    # 11. effective saves fold all-saves effects into each save
    st["effects"] = [_materialize("prayer", BUFFS["prayer"], 10)]
    check("prayer +1 luck folds into Fort/Ref/Will",
          effective(st, "fort") == 13 and effective(st, "ref") == 12
          and effective(st, "will") == 13)

    # 12. multiclass RAW summation: monk 9 / fighter 4
    prog = derived_progression({"monk": 9, "fighter": 4})
    check("monk9/fighter4 BAB +10 (6+4)", prog["bab"] == 10)
    check("monk9/fighter4 Fort +10 (6+4)", prog["fort"] == 10)
    check("monk9/fighter4 Ref +7 (6+1)", prog["ref"] == 7)
    check("monk9/fighter4 Will +7 (6+1)", prog["will"] == 7)

    # 13. milestone flags
    check("feat due at 18, not 17", 18 in FEAT_LEVELS and 17 not in FEAT_LEVELS)
    check("ability bump at 16, not 15",
          16 in ABILITY_LEVELS and 15 not in ABILITY_LEVELS)

    print(f"\n{'ALL checks passed.' if failures == 0 else str(failures) + ' CHECKS FAILED.'}")
    return 1 if failures else 0

# ============================================================================
# CLI
# ============================================================================

def main() -> int:
    ap = argparse.ArgumentParser(description="character sheet + buff engine")
    ap.add_argument("state", nargs="?", help="path to *.character.json")
    ap.add_argument("command", nargs="?",
                    choices=["new", "show", "buff", "buff-custom", "dispel",
                             "tick", "list-buffs", "level-up", "rest",
                             "cp-add", "cp-spend", "cp-show"])
    ap.add_argument("arg", nargs="?", help="name / count for the command")
    ap.add_argument("--cl", type=int, default=1, help="caster level for buff")
    ap.add_argument("--bonus", default="untyped",
                    choices=sorted(STACKING.keys()))
    ap.add_argument("--rounds", type=int, default=10)
    ap.add_argument("--note", default="")
    for stat in ("attack", "damage", "ac", "fort", "ref", "will", "saves",
                 "str", "dex", "con", "wis", "cha", "speed", "hp_temp"):
        ap.add_argument(f"--{stat.replace('_','-')}", dest=stat, type=int,
                        default=0)
    ap.add_argument("--int", dest="int_", type=int, default=10)
    ap.add_argument("--hp", type=int, default=10)
    ap.add_argument("--bab", type=int, default=0)
    ap.add_argument("--ac-armor", type=int, default=0)
    ap.add_argument("--ac-shield", type=int, default=0)
    ap.add_argument("--ac-natural", type=int, default=0)
    ap.add_argument("--ac-deflection", type=int, default=0)
    ap.add_argument("--ac-dodge", type=int, default=0)
    ap.add_argument("--ac-misc", type=int, default=0)
    ap.add_argument("--bed", action="store_true",
                    help="full bed rest (x2 natural healing)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if args.command == "list-buffs" or (args.state == "list-buffs"):
        for k in sorted(BUFFS):
            spec = BUFFS[k]
            print(f"  {k}  ({spec['source']})")
        return 0

    if not args.state or not args.command:
        ap.print_help()
        return 2

    if args.command == "new":
        cmd_new(args.state, args.arg or "Unnamed", args)
    elif args.command == "show":
        cmd_show(args.state)
    elif args.command == "buff":
        cmd_buff(args.state, args.arg or "", args.cl)
    elif args.command == "buff-custom":
        cmd_buff_custom(args.state, args.arg or "custom", args)
    elif args.command == "dispel":
        cmd_dispel(args.state, args.arg or "")
    elif args.command == "tick":
        cmd_tick(args.state, int(args.arg) if args.arg else 1)
    elif args.command == "level-up":
        cmd_level_up(args.state, args.arg or "")
    elif args.command == "rest":
        cmd_rest(args.state, int(args.arg) if args.arg else 8, args.bed)
    elif args.command == "cp-add":
        cmd_cp(args.state, "add", int(args.arg or 0), args.note)
    elif args.command == "cp-spend":
        cmd_cp(args.state, "spend", int(args.arg or 0), args.note)
    elif args.command == "cp-show":
        cmd_cp(args.state, "add", 0, "")
    return 0


if __name__ == "__main__":
    sys.exit(main())
