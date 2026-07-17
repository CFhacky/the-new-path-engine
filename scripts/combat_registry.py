#!/usr/bin/env python3
"""
combat_registry.py — session-local combat state registry
The New Path campaign engine (the-new-path-engine)

Companion to fused_round.py: fused_round resolves ONE round's strikes and is
stateless by contract; this script keeps the fight's state ACROSS rounds —
hit points (lethal and nonlethal), conditions with durations, and initiative
order — in a throwaway state file passed explicitly by path.

GOVERNING SOURCES (read, not memory):
    DMG 3.5, Chapter 8 Glossary, "Condition Summary", pp. 300-301
    (I:\\Sourcebooks\\_md\\Dungeon_Masters_Guide_3.5.md) — supplies the
    hp-state derivations this script automates:
      * Disabled     — exactly 0 hp (or stable-and-conscious in negatives)
      * Dying        — -1 to -9 hp; end of each round d%: 10% stabilize,
                       else lose 1 hp
      * Dead         — -10 hp or lower
      * Staggered    — nonlethal damage exactly equals current hp
      * Unconscious  — nonlethal damage exceeds current hp
    Initiative tie-break (higher modifier first, then roll-off) is standard
    3.5e RAW; flagged here as such.

DESIGN CONTRACT (repo README):
    - Session state lives in the explicit state file passed by path
      (*.registry.json — gitignored, throwaway, never committed).
    - Real dice: Python secrets, raw values printed BEFORE any outcome.
    - Visible output: every command prints a ready-to-paste board or receipt.
    - No cross-imports. The condition-name roster below is duplicated from
      conditions.py DELIBERATELY (README: shared logic gets duplicated or
      promoted deliberately, never tangled). If conditions.py's roster
      changes, update this list by hand.

USAGE (all commands take the state file first)
    python3 combat_registry.py fight.registry.json new --fight "Dockside ambush"
    python3 combat_registry.py fight.registry.json add "Korgan Bloodaxe" --hp 196 --init-mod 2 --side party
    python3 combat_registry.py fight.registry.json add "Enforcer" --hp 34 --init-mod 5 --side enemy
    python3 combat_registry.py fight.registry.json init
    python3 combat_registry.py fight.registry.json damage "Enforcer" 22
    python3 combat_registry.py fight.registry.json damage "Enforcer" 9 --nonlethal
    python3 combat_registry.py fight.registry.json set-hp "Enforcer" -3
    python3 combat_registry.py fight.registry.json heal "Enforcer" 5
    python3 combat_registry.py fight.registry.json cond-add "Korgan Bloodaxe" stunned --rounds 1
    python3 combat_registry.py fight.registry.json cond-remove "Korgan Bloodaxe" stunned
    python3 combat_registry.py fight.registry.json stabilize "Enforcer"
    python3 combat_registry.py fight.registry.json next
    python3 combat_registry.py fight.registry.json end-round
    python3 combat_registry.py fight.registry.json show
    python3 combat_registry.py --selftest
"""

import argparse
import json
import os
import secrets
import sys
from typing import Any, Dict, List, Optional

# ============================================================================
# DICE — secrets-backed, raw values always printed before outcomes
# ============================================================================

def roll_die(sides: int) -> int:
    return secrets.randbelow(sides) + 1

# ============================================================================
# CONDITION ROSTER — duplicated from conditions.py DELIBERATELY (no imports).
# DMG 3.5 pp.300-301 names + the two DM Screen PH-151 rows.
# ============================================================================

KNOWN_CONDITIONS = {
    "Ability Damaged", "Ability Drained", "Blinded", "Blown Away", "Checked",
    "Confused", "Cowering", "Dazed", "Dazzled", "Dead", "Deafened", "Disabled",
    "Dying", "Energy Drained", "Entangled", "Exhausted", "Fascinated",
    "Fatigued", "Flat-Footed", "Frightened", "Grappling", "Helpless",
    "Incorporeal", "Invisible", "Knocked Down", "Nauseated", "Panicked",
    "Paralyzed", "Petrified", "Pinned", "Prone", "Shaken", "Sickened",
    "Stable", "Staggered", "Stunned", "Turned", "Unconscious",
    "Kneeling or Sitting", "Squeezing Through a Space",
}
_KNOWN_LOWER = {k.lower(): k for k in KNOWN_CONDITIONS}
_CONDITION_ALIASES = {"grappled": "Grappling", "grapple": "Grappling",
                      "flat footed": "Flat-Footed", "flatfooted": "Flat-Footed",
                      "energy drain": "Energy Drained"}

# HP-derived states are AUTOMATIC (DMG p.300-301); adding them by hand is
# rejected so the ledger can't contradict the hit-point math.
AUTO_HP_STATES = {"Disabled", "Dying", "Dead", "Staggered", "Unconscious"}


def canonical_condition(name: str):
    """Returns (canonical_name, known: bool)."""
    q = name.strip().lower()
    if q in _KNOWN_LOWER:
        return _KNOWN_LOWER[q], True
    if q in _CONDITION_ALIASES:
        return _CONDITION_ALIASES[q], True
    prefix = [v for k, v in _KNOWN_LOWER.items() if k.startswith(q)]
    if len(prefix) == 1:
        return prefix[0], True
    return name.strip(), False

# ============================================================================
# STATE FILE
# ============================================================================

def new_state(fight: str) -> Dict[str, Any]:
    return {"fight": fight, "round": 0, "turn_index": 0,
            "order": [], "combatants": {}}


def load(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        raise SystemExit(f"No registry at {path!r} — run `new` first.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save(path: str, state: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def get_combatant(state: Dict[str, Any], name: str) -> Dict[str, Any]:
    combs = state["combatants"]
    if name in combs:
        return combs[name]
    lower = {k.lower(): k for k in combs}
    q = name.strip().lower()
    if q in lower:
        return combs[lower[q]]
    prefix = [k for kl, k in lower.items() if kl.startswith(q)]
    if len(prefix) == 1:
        return combs[prefix[0]]
    raise SystemExit(f"No unique combatant match for {name!r}. "
                     f"Roster: {', '.join(combs) or '(empty)'}")


def combatant_key(state: Dict[str, Any], name: str) -> str:
    c = get_combatant(state, name)
    for k, v in state["combatants"].items():
        if v is c:
            return k
    raise SystemExit("internal: combatant key not found")

# ============================================================================
# HP-STATE DERIVATION — DMG 3.5 p.300-301, mechanical text as read
# ============================================================================

def hp_state(c: Dict[str, Any]) -> str:
    hp, nl = c["hp"], c["nonlethal"]
    if hp <= -10:
        return "DEAD"
    if -9 <= hp <= -1:
        if c.get("stable"):
            return "STABLE (unconscious)"
        return "DYING"
    if hp == 0:
        return "DISABLED"
    # hp >= 1 from here
    if nl > hp:
        return "UNCONSCIOUS (nonlethal)"
    if nl == hp and nl > 0:
        return "STAGGERED"
    return "up"

# ============================================================================
# OUTPUT
# ============================================================================

def format_board(state: Dict[str, Any]) -> str:
    lines = []
    lines.append("=" * 66)
    lines.append(f"COMBAT REGISTRY — {state['fight']} — ROUND {state['round']}")
    lines.append("=" * 66)
    order = state["order"]
    if not order:
        lines.append("(initiative not yet rolled — `init`)")
        roster = list(state["combatants"])
    else:
        roster = order
    for i, name in enumerate(roster):
        c = state["combatants"][name]
        marker = "->" if (order and state["round"] >= 1
                          and i == state["turn_index"]) else "  "
        init_str = (f"init {c['init_total']:>2}" if c.get("init_total") is not None
                    else f"mod {c['init_mod']:+d}")
        hp_str = f"{c['hp']}/{c['max_hp']} hp"
        if c["nonlethal"]:
            hp_str += f" ({c['nonlethal']} NL)"
        status = hp_state(c)
        conds = ", ".join(
            f"{x['name']}" + (f" ({x['rounds_left']}r)" if x.get("rounds_left") is not None else "")
            for x in c["conditions"])
        line = f" {marker} {name:<24} [{c['side']:<6}] {init_str}  {hp_str:<18} {status}"
        lines.append(line)
        if conds:
            lines.append(f"      conditions: {conds}")
    lines.append("=" * 66)
    return "\n".join(lines)

# ============================================================================
# COMMANDS
# ============================================================================

def cmd_new(path, args):
    if os.path.exists(path) and not args.force:
        raise SystemExit(f"{path} exists — pass --force to overwrite.")
    state = new_state(args.fight)
    save(path, state)
    print(f"Registry created: {path}  (fight: {args.fight})")


def cmd_add(path, args):
    state = load(path)
    if args.name in state["combatants"]:
        raise SystemExit(f"{args.name!r} already in the registry.")
    state["combatants"][args.name] = {
        "hp": args.hp, "max_hp": args.max_hp if args.max_hp is not None else args.hp,
        "nonlethal": 0, "init_mod": args.init_mod,
        "init_total": None, "side": args.side, "notes": args.notes,
        "conditions": [], "stable": False,
    }
    if state["order"]:
        state["order"].append(args.name)   # late arrivals act last this round
    save(path, state)
    print(f"Added {args.name}: {args.hp} hp, init mod {args.init_mod:+d}, side {args.side}."
          + ("  (joined at the bottom of the current order)" if state["order"] else ""))


def cmd_remove(path, args):
    state = load(path)
    key = combatant_key(state, args.name)
    if key in state["order"]:
        idx = state["order"].index(key)
        state["order"].remove(key)
        if state["order"]:
            if idx < state["turn_index"]:
                state["turn_index"] -= 1
            state["turn_index"] %= len(state["order"])
        else:
            state["turn_index"] = 0
    del state["combatants"][key]
    save(path, state)
    print(f"Removed {key} from the registry.")


def cmd_init(path, args):
    state = load(path)
    if not state["combatants"]:
        raise SystemExit("No combatants — `add` some first.")
    print("INITIATIVE — d20 + modifier (raw first, per contract):")
    rolled = []
    for name, c in state["combatants"].items():
        if args.set and name in dict(args.set):
            total = int(dict(args.set)[name])
            c["init_total"] = total
            print(f"  {name:<24} set {total} (manual)")
        else:
            raw = roll_die(20)
            total = raw + c["init_mod"]
            c["init_total"] = total
            print(f"  {name:<24} d20 {raw:>2} {c['init_mod']:+d} = {total}")
        rolled.append(name)
    # 3.5e RAW tie-break: higher modifier acts first; dead ties roll off.
    def sort_key(n):
        c = state["combatants"][n]
        return (-c["init_total"], -c["init_mod"])
    order = sorted(rolled, key=sort_key)
    i = 0
    while i < len(order) - 1:
        a, b = state["combatants"][order[i]], state["combatants"][order[i + 1]]
        if (a["init_total"], a["init_mod"]) == (b["init_total"], b["init_mod"]):
            ra, rb = roll_die(20), roll_die(20)
            print(f"  TIE {order[i]} vs {order[i+1]} — roll-off d20: {ra} vs {rb}")
            if rb > ra:
                order[i], order[i + 1] = order[i + 1], order[i]
            if ra == rb:
                continue   # reroll the same pair
        i += 1
    state["order"] = order
    state["round"] = max(state["round"], 1)
    state["turn_index"] = 0
    save(path, state)
    print(f"ORDER: {' > '.join(order)}")
    print(format_board(state))


def _apply_damage(c, amount, nonlethal):
    if nonlethal:
        c["nonlethal"] += amount
    else:
        was_positive = c["hp"] > 0
        c["hp"] -= amount
        if c["hp"] <= -1 and was_positive:
            c["stable"] = False   # freshly dropped into dying


def cmd_damage(path, args):
    state = load(path)
    key = combatant_key(state, args.name)
    c = state["combatants"][key]
    before = hp_state(c)
    _apply_damage(c, args.amount, args.nonlethal)
    if not args.nonlethal and args.amount > 0 and c["hp"] <= -1 and before not in ("DYING", "DEAD"):
        c["stable"] = False
    after = hp_state(c)
    save(path, state)
    kind = "nonlethal" if args.nonlethal else "damage"
    print(f"{key}: {args.amount} {kind} -> {c['hp']}/{c['max_hp']} hp"
          + (f" ({c['nonlethal']} NL)" if c["nonlethal"] else "")
          + (f"  [{before} -> {after}]" if after != before else f"  [{after}]"))


def cmd_heal(path, args):
    state = load(path)
    key = combatant_key(state, args.name)
    c = state["combatants"][key]
    before = hp_state(c)
    if args.nonlethal:
        c["nonlethal"] = max(0, c["nonlethal"] - args.amount)
    else:
        c["hp"] = min(c["max_hp"], c["hp"] + args.amount)
        # DMG: healing that raises a dying character above the threshold ends dying;
        # any healing on a dying character stabilizes (magical healing / aid).
        if c["hp"] >= 0 or args.amount > 0:
            c["stable"] = True if -9 <= c["hp"] <= -1 else False
        # Nonlethal: DMG p.146 healing lore lives outside the Condition Summary;
        # this script only clamps NL at 0 and hp at max.
    after = hp_state(c)
    save(path, state)
    print(f"{key}: healed {args.amount}{' NL' if args.nonlethal else ''} -> "
          f"{c['hp']}/{c['max_hp']} hp"
          + (f" ({c['nonlethal']} NL)" if c["nonlethal"] else "")
          + (f"  [{before} -> {after}]" if after != before else f"  [{after}]"))


def cmd_set_hp(path, args):
    """Direct sync with fused_round.py's 'HP AFTER ROUND' line."""
    state = load(path)
    key = combatant_key(state, args.name)
    c = state["combatants"][key]
    before = hp_state(c)
    was_positive = c["hp"] > 0
    c["hp"] = args.value
    if -9 <= c["hp"] <= -1 and was_positive:
        c["stable"] = False
    after = hp_state(c)
    save(path, state)
    print(f"{key}: hp set to {c['hp']}/{c['max_hp']}"
          + (f"  [{before} -> {after}]" if after != before else f"  [{after}]"))


def cmd_cond_add(path, args):
    state = load(path)
    key = combatant_key(state, args.name)
    c = state["combatants"][key]
    cname, known = canonical_condition(args.condition)
    if cname in AUTO_HP_STATES:
        raise SystemExit(f"{cname} is derived automatically from hit points "
                         f"(DMG p.300-301) — adjust hp/nonlethal instead.")
    if not known and not args.force:
        raise SystemExit(f"{args.condition!r} is not on the DMG/DM-Screen roster. "
                         f"Pass --force to record a custom rider.")
    for x in c["conditions"]:
        if x["name"].lower() == cname.lower():
            raise SystemExit(f"{key} already has {cname}.")
    entry = {"name": cname if known else f"{cname} [custom]",
             "rounds_left": args.rounds, "note": args.note}
    c["conditions"].append(entry)
    save(path, state)
    dur = f" for {args.rounds} round(s)" if args.rounds is not None else ""
    print(f"{key}: +{entry['name']}{dur}."
          + (f"  ({args.note})" if args.note else ""))


def cmd_cond_remove(path, args):
    state = load(path)
    key = combatant_key(state, args.name)
    c = state["combatants"][key]
    q = args.condition.strip().lower()
    hits = [x for x in c["conditions"] if x["name"].lower().startswith(q)]
    if len(hits) != 1:
        have = ", ".join(x["name"] for x in c["conditions"]) or "(none)"
        raise SystemExit(f"No unique condition match for {args.condition!r} on {key}. "
                         f"Active: {have}")
    c["conditions"].remove(hits[0])
    save(path, state)
    print(f"{key}: -{hits[0]['name']}.")


def cmd_stabilize(path, args):
    state = load(path)
    key = combatant_key(state, args.name)
    c = state["combatants"][key]
    if not (-9 <= c["hp"] <= -1):
        raise SystemExit(f"{key} is not dying ({c['hp']} hp).")
    c["stable"] = True
    save(path, state)
    print(f"{key}: stabilized at {c['hp']} hp (aid — Heal check or magic).  "
          f"[{hp_state(c)}]")


def _tick_round_end(state: Dict[str, Any], no_dying_rolls: bool) -> None:
    """End-of-round bookkeeping: condition durations tick, dying d% rolls fire.
    DMG p.301: 'At the end of each round... the character rolls d% to see
    whether she becomes stable. She has a 10% chance... If she does not, she
    loses 1 hit point.'"""
    for name, c in state["combatants"].items():
        expired = []
        for x in c["conditions"]:
            if x.get("rounds_left") is not None:
                x["rounds_left"] -= 1
                if x["rounds_left"] <= 0:
                    expired.append(x)
        for x in expired:
            c["conditions"].remove(x)
            print(f"  {name}: {x['name']} expires.")
        if -9 <= c["hp"] <= -1 and not c.get("stable") and not no_dying_rolls:
            raw = roll_die(100)
            if raw <= 10:
                c["stable"] = True
                print(f"  {name} DYING — d% {raw:>3} (<=10 stabilizes) -> STABILIZES at {c['hp']} hp.")
            else:
                c["hp"] -= 1
                tail = " — DEAD at -10." if c["hp"] <= -10 else f" -> {c['hp']} hp."
                print(f"  {name} DYING — d% {raw:>3} (<=10 stabilizes) -> fails, loses 1 hp{tail}")


def cmd_next(path, args):
    state = load(path)
    if not state["order"]:
        raise SystemExit("No initiative order — run `init` first.")
    state["turn_index"] += 1
    if state["turn_index"] >= len(state["order"]):
        state["turn_index"] = 0
        print(f"— end of round {state['round']} —")
        _tick_round_end(state, args.no_dying_rolls)
        state["round"] += 1
        print(f"— ROUND {state['round']} —")
    save(path, state)
    up = state["order"][state["turn_index"]]
    print(f"Acting: {up}  ({hp_state(state['combatants'][up])})")


def cmd_end_round(path, args):
    state = load(path)
    if not state["order"]:
        raise SystemExit("No initiative order — run `init` first.")
    print(f"— end of round {state['round']} —")
    _tick_round_end(state, args.no_dying_rolls)
    state["round"] += 1
    state["turn_index"] = 0
    save(path, state)
    print(f"— ROUND {state['round']} —")
    print(format_board(state))


def cmd_show(path, args):
    state = load(path)
    print(format_board(state))

# ============================================================================
# SELFTEST — one worked fight, real dice, assertions on the DMG hp-state math
# ============================================================================

class _Args:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def selftest() -> int:
    import tempfile
    ok = True

    def expect(label, cond):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
        ok = ok and cond

    with tempfile.TemporaryDirectory() as td:
        path = os.path.join(td, "selftest.registry.json")
        print("### combat_registry.py SELFTEST — worked fight ###\n")

        cmd_new(path, _Args(fight="Selftest skirmish", force=False))
        cmd_add(path, _Args(name="Korgan Bloodaxe", hp=196, max_hp=None,
                            init_mod=2, side="party", notes=""))
        cmd_add(path, _Args(name="Enforcer A", hp=34, max_hp=None,
                            init_mod=5, side="enemy", notes=""))
        cmd_add(path, _Args(name="Enforcer B", hp=34, max_hp=None,
                            init_mod=5, side="enemy", notes=""))
        print()
        cmd_init(path, _Args(set=None))
        state = load(path)
        expect("init: every combatant has a total",
               all(c["init_total"] is not None for c in state["combatants"].values()))
        expect("init: order sorted descending by (total, mod)",
               all(( state["combatants"][state["order"][i]]["init_total"],
                     state["combatants"][state["order"][i]]["init_mod"]) >=
                   ( state["combatants"][state["order"][i+1]]["init_total"],
                     state["combatants"][state["order"][i+1]]["init_mod"])
                   for i in range(len(state["order"]) - 1)))

        print("\n-- damage into DMG hp states --")
        cmd_damage(path, _Args(name="Enforcer A", amount=34, nonlethal=False))
        expect("0 hp -> DISABLED", hp_state(load(path)["combatants"]["Enforcer A"]) == "DISABLED")
        cmd_damage(path, _Args(name="Enforcer A", amount=3, nonlethal=False))
        expect("-3 hp -> DYING", hp_state(load(path)["combatants"]["Enforcer A"]) == "DYING")

        cmd_damage(path, _Args(name="Enforcer B", amount=20, nonlethal=False))   # 14 hp
        cmd_damage(path, _Args(name="Enforcer B", amount=14, nonlethal=True))    # NL == hp
        expect("nonlethal == hp -> STAGGERED",
               hp_state(load(path)["combatants"]["Enforcer B"]) == "STAGGERED")
        cmd_damage(path, _Args(name="Enforcer B", amount=1, nonlethal=True))     # NL > hp
        expect("nonlethal > hp -> UNCONSCIOUS",
               hp_state(load(path)["combatants"]["Enforcer B"]) == "UNCONSCIOUS (nonlethal)")

        print("\n-- conditions --")
        cmd_cond_add(path, _Args(name="Korgan", condition="stunned",
                                 rounds=1, note="", force=False))
        cmd_cond_add(path, _Args(name="Korgan", condition="shaken",
                                 rounds=None, note="fear aura", force=False))
        try:
            cmd_cond_add(path, _Args(name="Korgan", condition="dying",
                                     rounds=None, note="", force=False))
            expect("auto hp-state rejected as manual condition", False)
        except SystemExit:
            expect("auto hp-state rejected as manual condition", True)
        try:
            cmd_cond_add(path, _Args(name="Korgan", condition="smoke-blind",
                                     rounds=None, note="", force=False))
            expect("unknown condition rejected without --force", False)
        except SystemExit:
            expect("unknown condition rejected without --force", True)
        cmd_cond_add(path, _Args(name="Korgan", condition="smoke-blind",
                                 rounds=2, note="Quiet Plate rider", force=True))
        expect("custom condition recorded with --force",
               any("smoke-blind" in x["name"] for x in
                   load(path)["combatants"]["Korgan Bloodaxe"]["conditions"]))

        print("\n-- round advance: duration ticks + dying d% (raw shown) --")
        cmd_end_round(path, _Args(no_dying_rolls=False))
        s = load(path)
        expect("1-round condition expired after end-round",
               not any(x["name"] == "Stunned" for x in
                       s["combatants"]["Korgan Bloodaxe"]["conditions"]))
        expect("untimed condition persists",
               any(x["name"] == "Shaken" for x in
                   s["combatants"]["Korgan Bloodaxe"]["conditions"]))
        a = s["combatants"]["Enforcer A"]
        expect("dying enforcer either stabilized or lost exactly 1 hp",
               (a["stable"] and a["hp"] == -3) or (not a["stable"] and a["hp"] == -4))
        expect("round advanced to 2", s["round"] == 2)

        print("\n-- stabilize + set-hp sync --")
        if not load(path)["combatants"]["Enforcer A"]["stable"]:
            cmd_stabilize(path, _Args(name="Enforcer A"))
        expect("stabilized dying -> STABLE",
               hp_state(load(path)["combatants"]["Enforcer A"]).startswith("STABLE"))
        cmd_set_hp(path, _Args(name="Korgan", value=150))
        expect("set-hp syncs fused_round totals",
               load(path)["combatants"]["Korgan Bloodaxe"]["hp"] == 150)
        cmd_set_hp(path, _Args(name="Enforcer B", value=-12))
        expect("set-hp to -12 -> DEAD",
               hp_state(load(path)["combatants"]["Enforcer B"]) == "DEAD")

        print("\n-- next-turn pointer --")
        cmd_next(path, _Args(no_dying_rolls=True))
        expect("turn pointer advanced", load(path)["turn_index"] == 1)

        print()
        cmd_show(path, _Args())

    print(f"\nSELFTEST {'PASSED' if ok else 'FAILED'}.")
    return 0 if ok else 1

# ============================================================================
# CLI
# ============================================================================

def main():
    p = argparse.ArgumentParser(
        description="Session-local combat registry: hp, conditions, initiative "
                    "across rounds (companion to fused_round.py).")
    p.add_argument("--selftest", action="store_true",
                   help="Run a worked fight in a temp directory and exit.")
    p.add_argument("state", nargs="?",
                   help="Path to the fight's *.registry.json state file.")
    sub = p.add_subparsers(dest="command")

    sp = sub.add_parser("new", help="Create a fresh registry file.")
    sp.add_argument("--fight", default="Unnamed engagement")
    sp.add_argument("--force", action="store_true")

    sp = sub.add_parser("add", help="Add a combatant.")
    sp.add_argument("name")
    sp.add_argument("--hp", type=int, required=True)
    sp.add_argument("--max-hp", type=int, dest="max_hp", default=None,
                    help="Defaults to --hp.")
    sp.add_argument("--init-mod", type=int, dest="init_mod", default=0)
    sp.add_argument("--side", default="enemy", help="party | enemy | other")
    sp.add_argument("--notes", default="")

    sp = sub.add_parser("remove", help="Remove a combatant.")
    sp.add_argument("name")

    sp = sub.add_parser("init", help="Roll initiative (d20 + mod, raw shown).")
    sp.add_argument("--set", nargs=2, action="append", metavar=("NAME", "TOTAL"),
                    help="Fix a combatant's total instead of rolling. Repeatable.")

    sp = sub.add_parser("damage", help="Apply damage.")
    sp.add_argument("name"); sp.add_argument("amount", type=int)
    sp.add_argument("--nonlethal", action="store_true")

    sp = sub.add_parser("heal", help="Heal damage (clamped at max hp / 0 NL).")
    sp.add_argument("name"); sp.add_argument("amount", type=int)
    sp.add_argument("--nonlethal", action="store_true")

    sp = sub.add_parser("set-hp", help="Set hp directly (sync with fused_round).")
    sp.add_argument("name"); sp.add_argument("value", type=int)

    sp = sub.add_parser("cond-add", help="Add a condition.")
    sp.add_argument("name"); sp.add_argument("condition")
    sp.add_argument("--rounds", type=int, default=None,
                    help="Duration; expires at end of round when it hits 0.")
    sp.add_argument("--note", default="")
    sp.add_argument("--force", action="store_true",
                    help="Allow a condition not on the DMG/DM-Screen roster.")

    sp = sub.add_parser("cond-remove", help="Remove a condition.")
    sp.add_argument("name"); sp.add_argument("condition")

    sp = sub.add_parser("stabilize", help="Stabilize a dying combatant (aid).")
    sp.add_argument("name")

    sp = sub.add_parser("next", help="Advance the turn pointer; wraps into a new round.")
    sp.add_argument("--no-dying-rolls", action="store_true", dest="no_dying_rolls",
                    help="Suppress the automatic end-of-round dying d% rolls.")

    sp = sub.add_parser("end-round", help="Jump to the top of the next round.")
    sp.add_argument("--no-dying-rolls", action="store_true", dest="no_dying_rolls")

    sub.add_parser("show", help="Print the status board.")

    args = p.parse_args()

    if args.selftest:
        sys.exit(selftest())
    if not args.state or not args.command:
        p.print_help()
        sys.exit(1)

    handlers = {"new": cmd_new, "add": cmd_add, "remove": cmd_remove,
                "init": cmd_init, "damage": cmd_damage, "heal": cmd_heal,
                "set-hp": cmd_set_hp, "cond-add": cmd_cond_add,
                "cond-remove": cmd_cond_remove, "stabilize": cmd_stabilize,
                "next": cmd_next, "end-round": cmd_end_round, "show": cmd_show}
    handlers[args.command](args.state, args)


if __name__ == "__main__":
    main()
