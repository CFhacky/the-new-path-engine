#!/usr/bin/env python3
"""
udrp_delve.py -- UDRP dungeon-leg roller (dungeons and delves)
The New Path campaign engine (the-new-path-engine)

Per-leg resolver for the UDRP dungeon-leg machinery: site entry rolls the
structure (layout, type, builder, state, Layer 3 Persistent Threat,
objective); each `leg` invocation runs ONE room's full engine pass -- the
one-leg-per-output law. Session state lives in an explicit *.delve.json
passed by path (gitignored, throwaway).

GOVERNING SOURCES (read 2026-07-17; cited per table):
    udrp-dungeon-generation-module.md  (project knowledge, mechanics layer)
        -- layout engine, die/room table, stairs-by-parity + descent bias,
           Layer 0/1/3/4 tables, Stocking Table 1-12, tier scaling 2B,
           puzzle generation d8
    udrp-monster-ecology-module.md  (project knowledge)
        -- denizen rows: Layer 1A Creature Category d12, 1B Behavior d8
    __UNIVERSAL_DICE_ROLLER_PROTOCOL__UDRP__v2.0  (dice philosophy; the
        module's own worked example throws single raw secrets dice, so
        single throws are the default here; --four-throw applies the
        Standing Law G2 four-throw bind instead)

CONTRACT NOTES:
    - The script NEVER invents monsters, items, or rulings. Denizen results
      print as table references ("monster-ecology Layer 1A row N: <name>")
      plus the raw roll; the instance pulls the creature from the module or
      bestiary. Treasure prints a D4 Item Roller reference. Where the UDRP
      files leave a resolution point uncovered (ward degradation, alert
      escalation, intel accuracy, ten-minute state rolls -- all delegated by
      the module to dungeon-state-tables.md, which is not in this repo's
      source set), the script prints "NO COVERAGE -- nearest table: <name>"
      rather than improvising.
    - Exposure/environment clocks (Persistent Threats 3 bad air / 4 heat
      gradient / 6 rising water are progressive per the module) live in the
      state file and tick one step per leg automatically; `clock` reads or
      adjusts them.

USAGE
    python udrp_delve.py SITE.delve.json new --site "Frost Barrow" \
        --dice d4,d6,d6,d10,d12 --tier III [--descent-bias] \
        [--set-type N --set-builder N --set-state N --set-threat N --set-objective N]
    python udrp_delve.py SITE.delve.json leg
    python udrp_delve.py SITE.delve.json clock exposure --advance 1
    python udrp_delve.py SITE.delve.json show
    python udrp_delve.py --selftest
"""

import argparse
import json
import os
import secrets
import sys
from typing import Any, Dict, List, Optional, Tuple

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ============================================================================
# DICE -- secrets only, raw first. Single throw default (module's worked
# example); --four-throw switches to Standing Law G2 binding.
# ============================================================================

FOUR_THROW = False


def _throw(sides: int) -> int:
    return secrets.randbelow(sides) + 1


def bind_four(values: List[int]) -> Tuple[int, str]:
    counts: Dict[int, int] = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    best = max(counts.values())
    modes = sorted(v for v, c in counts.items() if c == best)
    if best >= 2 and len(modes) == 1:
        return modes[0], "mode"
    s = sorted(values)
    return int((s[1] + s[2]) / 2), "median"


def roll(sides: int, label: str) -> Tuple[int, str]:
    if FOUR_THROW:
        raws = [_throw(sides) for _ in range(4)]
        bound, how = bind_four(raws)
        return bound, f"  d{sides} throws {raws} -> bind {bound} ({how})  [{label}]"
    raw = _throw(sides)
    return raw, f"  d{sides} = {raw}  [{label}]"

# ============================================================================
# TABLES -- transcribed from udrp-dungeon-generation-module.md (row names
# abbreviated; full text lives in the module -- the module wins on conflict).
# ============================================================================

# Layout engine Step 2 table: die -> room size / danger ceiling
DIE_ROOMS = {
    4:  ("~20 ft sq / ~7 yd", "Trivial"),
    6:  ("~30 ft sq / ~10 yd", "Minor"),
    8:  ("~40 ft sq / ~13 yd", "Major"),
    10: ("~50 ft sq or hall / ~17 yd", "Dangerous"),
    12: ("vast hall or cavern / ~20+ yd", "Deadly"),
}

# Layer 0A Site Type (d20) -- short names; full flavour on the module rows
SITE_TYPES = {
    1: "Mulhorandi tomb-temple", 2: "Drowned Seros site",
    3: "Underdark vault / drow ruin", 4: "Draconic hoard-lair",
    5: "Netherese ruin", 6: "Old fortress / contested ruin",
    7: "Infernal redoubt", 8: "Frost-bound barrow / Jotunn ruin",
    9: "Active cult sanctum", 10: "Mage's tower / laboratory",
    11: "Beast warren / natural lair", 12: "Prison / oubliette",
    13: "Forge / workshop", 14: "Archive / library",
    15: "Mine / delve", 16: "Planar threshold",
    17: "Plague-house / quarantine", 18: "Shrine-complex",
    19: "Smuggler's / criminal hideout", 20: "Ancient-mystery site",
}

# Layer 1A Builder / Origin (d12)
BUILDERS = {
    1: "Death-cult or temple priesthood", 2: "Archmage or arcane order",
    3: "Dwarven hold / delvers", 4: "A dragon (lair grew around the hoard)",
    5: "Drow House or Underdark power", 6: "Fiend -- devil or demon work",
    7: "Giant-kin / Jotunn / primordial hand",
    8: "Forgotten god or dead pantheon",
    9: "Natural -- no builder; tenants claimed it",
    10: "Construct-maker / forge-priest",
    11: "Mortal warlord or fallen kingdom",
    12: "Something that should not have hands (aberration/outsider)",
}

# Layer 1B Current State (d10)
STATES = {
    1: "Intact and actively occupied", 2: "Intact but dormant -- sealed, waiting",
    3: "Partially ruined, still defended", 4: "Flooded, wholly or in part",
    5: "Desecrated -- old power broken, scavengers moved in",
    6: "Overrun by new tenants unlike the builders",
    7: "Warded shut -- defenses still run; builders long gone",
    8: "Collapsing -- structural failure in progress",
    9: "Contested -- two powers fighting over it RIGHT NOW",
    10: "Reawakening -- something inside is coming back",
}

# Layer 3A Persistent Threat (d12); progressive entries drive the auto-clock
THREATS = {
    1: ("None -- bare cold stone; re-roll empties as lore or let the "
        "silence work", False),
    2: ("Toxic growth -- mold/spores; Fort (3.5e) / HT (GURPS) on entry "
        "to a held room", False),
    3: ("Bad air / damp -- suffocation and disease bands; LONGER THE STAY, "
        "WORSE THE ROLL (progressive)", True),
    4: ("Heat gradient -- progressive Fort/HT, penalty worsening each level "
        "down; plate is a liability (progressive)", True),
    5: ("Killing cold -- ward or relic radiating wrongness; worse near its "
        "source", False),
    6: ("Rising water -- TIMED FLOODING, a clock on the whole dungeon "
        "(progressive)", True),
    7: ("Lair effect -- a powerful resident warps the site; reality bends "
        "near the deep room", False),
    8: ("Curse / divine displeasure -- escalating misfortune; save vs the "
        "resident god's attention", False),
    9: ("Structural decay -- tremors; the GM can spend a cave-in at any "
        "dramatic beat", False),
    10: ("Watchful site -- warded to notice; detection bonuses against "
         "intruders; the place tells its master", False),
    11: ("Patrols -- occupants actively hunt; alert-level system lives in "
         "dungeon-state-tables.md (NO COVERAGE here)", False),
    12: ("Magical instability -- wild-magic surges / planar bleed; "
         "spellcasting and teleport unreliable", False),
}

# Layer 4A Objective (d12)
OBJECTIVES = {
    1: "A relic or artifact (D4 Item Roller, Tier 0-1)",
    2: "A bound entity -- the boss is the prize (demon/sovereign or divine pass)",
    3: "Knowledge / intel -- a thread unlocks",
    4: "A captive -- extract alive",
    5: "A resource node -- the empire wants the site itself",
    6: "A planar threshold -- the building is the doorframe",
    7: "A corpse-god relic -- world-altering, deepest ward",
    8: "Bait -- there is no prize; the site is the trap",
    9: "A seat of power -- claimed, not carried",
    10: "A cache -- materiel, dangerous to move",
    11: "A production site -- destroy, don't take",
    12: "Two prizes, warded apart (the split objective; cross the site twice)",
}

# Layer 2A Stocking Table (face 1-12), with kind tags driving the leg pass
STOCKING = {
    1:  ("Empty -- apply the site's Persistent Threat; a breath between "
         "rooms", "empty"),
    2:  ("Lore / discovery -- environmental story; no fight", "lore"),
    3:  ("Hazard, minor -- Search/Disable + Reflex/Fort at the tier's minor "
         "band; CR ~ APL-3 to -2 / GURPS low injury band", "hazard"),
    4:  ("Lesser denizen -- one or two weak occupants; CR ~ APL-2 / GURPS "
         "minor (<= half PC points)", "denizen"),
    5:  ("Puzzle, minor -- one good idea solves it; design against the PC's "
         "tools", "puzzle"),
    6:  ("Denizen, standard -- a proper encounter; CR ~ APL / GURPS even "
         "footing", "denizen"),
    7:  ("Ward / hazard, major -- DC at the tier's hard band / GURPS "
         "resistance at -2 or worse; decay routes through "
         "dungeon-state-tables.md", "ward"),
    8:  ("Denizen, elite -- named or augmented foe, often with support; "
         "CR ~ APL+2 / GURPS serious", "denizen"),
    9:  ("Puzzle / gate, major -- real barrier; failure triggers a hazard "
         "(Heart of Winter's Grief standard)", "puzzle"),
    10: ("Treasure / reliquary -- roll the D4 Item Roller at the site's "
         "tier; usually guarded", "treasure"),
    11: ("Lethal ward / deadly trap -- the site's worst passive defense, "
         "themed to the builder; save-or-suffer / GURPS deadly band", "ward"),
    12: ("Apex -- strongest thing short of the objective; CR ~ APL+3 to +4 "
         "/ GURPS deadly; sovereign-tier stats via its own module", "denizen"),
}

# Layer 2B tier scaling
TIERS = {
    "I":   ("APL 1-5 / ~150-250 pts",  "CR 1-3",   "CR 4-6",   "CR 7-9"),
    "II":  ("APL 6-10 / ~250-400 pts", "CR 4-8",   "CR 8-11",  "CR 12-14"),
    "III": ("APL 11-15 / ~400-600",    "CR 9-13",  "CR 13-16", "CR 17-19"),
    "IV":  ("APL 16-20 / 600+",        "CR 14-18", "CR 18-21", "CR 22-25"),
    "V":   ("Epic 21+ / gestalt",      "CR 19+",   "CR 22+",   "CR 26+ (custom)"),
}

# Puzzle Generation d8
PUZZLES = {
    1: "Offering / libation", 2: "Name / word", 3: "Weighing / balance",
    4: "Sequence / order", 5: "Reflection / positioning",
    6: "Sacrifice / cost", 7: "Cipher / knowledge", 8: "Rite / devotion",
}

# Monster ecology module, Layer 1A Creature Category (d12) row names
ECO_CATEGORY = {
    1: "Beast (mundane predator)", 2: "Beast (exotic/magical)",
    3: "Aerial threat", 4: "Burrowing/subterranean", 5: "Aquatic/riparian",
    6: "Insectoid/vermin (swarm)", 7: "Plant/fungal", 8: "Undead (ambient)",
    9: "Giant-kin", 10: "Elemental/fey (wild)", 11: "Dragon-adjacent",
    12: "Aberration/exotic",
}

# Monster ecology module, Layer 1B Behavior Pattern (d8) row names
ECO_BEHAVIOR = {
    1: "Hunting in humanoid territory", 2: "Nesting/breeding",
    3: "Territorial defense", 4: "Migration path conflict",
    5: "Resource competition", 6: "Infestation/colonization",
    7: "Displacement aggression", 8: "Symbiotic/parasitic relationship",
}

NO_COVERAGE_STATE = ("NO COVERAGE -- nearest table: dungeon-state-tables.md "
                     "(intel accuracy / ten-minute state roll / alert "
                     "escalation / ward degradation). Not in this repo's "
                     "source set; resolve on that document or flag to Chad.")

# ============================================================================
# STATE FILE
# ============================================================================

def load(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        raise SystemExit(f"No delve state at {path!r} -- run `new` first.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save(path: str, state: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def parse_dice(spec: str) -> List[int]:
    """'d4,d6,d6,d10,d12' -> [4, 6, 6, 10, 12]."""
    sides = []
    for tok in spec.split(","):
        tok = tok.strip().lower().lstrip("d")
        if not tok.isdigit() or int(tok) not in DIE_ROOMS:
            raise SystemExit(f"Bad room die {tok!r} -- valid: d4 d6 d8 d10 "
                             f"d12 (module Step 2 table).")
        sides.append(int(tok))
    if not sides:
        raise SystemExit("At least one room die required.")
    return sides


def compute_depths(faces: List[int], descent_bias: bool) -> List[int]:
    """Stairs by parity (module Step 4). Standard: even->odd DOWN,
    odd->even UP, same parity SAME LEVEL. Descent bias: any parity change
    is a step DOWN; same parity is a side-chamber on the current level."""
    depths = [0]
    for a, b in zip(faces, faces[1:]):
        parity_change = (a % 2) != (b % 2)
        if descent_bias:
            step = 1 if parity_change else 0
        else:
            if not parity_change:
                step = 0
            elif a % 2 == 0:      # even -> odd: stairs DOWN
                step = 1
            else:                 # odd -> even: stairs UP
                step = -1
        depths.append(depths[-1] + step)
    return depths


def stairs_text(a: int, b: int, descent_bias: bool) -> str:
    parity_change = (a % 2) != (b % 2)
    if descent_bias:
        return "DOWN" if parity_change else "side-chamber, same level"
    if not parity_change:
        return "same level"
    return "DOWN" if a % 2 == 0 else "UP"

# ============================================================================
# COMMANDS
# ============================================================================

def cmd_new(path: str, args) -> None:
    if os.path.exists(path) and not args.force:
        raise SystemExit(f"{path} exists -- pass --force to overwrite.")
    if args.tier not in TIERS:
        raise SystemExit(f"--tier must be one of {sorted(TIERS)}.")
    out = [f"=== SITE ENTRY -- {args.site} ===",
           "(udrp-dungeon-generation-module.md: layout engine + Layers "
           "0/1/3/4; raw dice first)"]

    def fixed_or_roll(fixed: Optional[int], sides: int, label: str) -> int:
        if fixed is not None:
            out.append(f"  d{sides} [AUTHORED, not rolled] = {fixed}  [{label}]")
            return fixed
        v, line = roll(sides, label)
        out.append(line)
        return v

    site_type = fixed_or_roll(args.set_type, 20, "Layer 0A site type")
    builder = fixed_or_roll(args.set_builder, 12, "Layer 1A builder/origin")
    st = fixed_or_roll(args.set_state, 10, "Layer 1B current state")
    threat = fixed_or_roll(args.set_threat, 12, "Layer 3A persistent threat")
    objective = fixed_or_roll(args.set_objective, 12, "Layer 4A objective")

    sides = parse_dice(args.dice)
    out.append("  Room dice thrown (the throw IS the map; face = content "
               "result, module Step 3):")
    faces = []
    for i, s in enumerate(sides, 1):
        v, line = roll(s, f"room {i} (d{s})")
        out.append(line)
        faces.append(v)
    depths = compute_depths(faces, args.descent_bias)

    threat_text, progressive = THREATS[threat]
    state = {
        "site": args.site, "tier": args.tier,
        "descent_bias": bool(args.descent_bias),
        "site_type": site_type, "builder": builder, "state": st,
        "threat": threat, "objective": objective,
        "room_dice": sides, "faces": faces, "depths": depths,
        "leg": 0,
        "clocks": {},
    }
    if progressive:
        state["clocks"]["exposure"] = 0
    save(path, state)

    out.append("")
    out.append(f"  SITE TYPE {site_type}: {SITE_TYPES[site_type]}")
    out.append(f"  BUILDER {builder}: {BUILDERS[builder]}")
    out.append(f"  STATE {st}: {STATES[st]}")
    out.append(f"  PERSISTENT THREAT {threat}: {threat_text}")
    out.append(f"  OBJECTIVE {objective}: {OBJECTIVES[objective]}")
    deepest = max(range(len(depths)), key=lambda i: depths[i])
    out.append(f"  MAP ({'descent bias' if args.descent_bias else 'standard parity'}):")
    for i, (s, f_, d) in enumerate(zip(sides, faces, depths), 1):
        size, ceil = DIE_ROOMS[s]
        link = ("entry" if i == 1 else
                stairs_text(faces[i - 2], f_, args.descent_bias))
        out.append(f"    Room {i}: d{s} face {f_}  depth {d}  ({size}; "
                   f"ceiling {ceil})  [{link}]")
    out.append(f"  OBJECTIVE SITED in the deepest room: Room {deepest + 1} "
               f"(depth {depths[deepest]}) -- module Layer 4: 'place this in "
               f"the deepest room or author it directly'. Boss stats via the "
               f"antagonist modules, never the Stocking Table.")
    out.append(f"  Persistent Threat must be FORESHADOWED ON ENTRY (module "
               f"Layer 3) -- narrate its first sign before Room 1.")
    if progressive:
        out.append("  Progressive threat detected -> 'exposure' clock seated "
                   "at 0; ticks +1 per leg automatically.")
    out.append(f"\n  State written: {path}. One leg per invocation from here "
               f"(`leg`).")
    print("\n".join(out))

def cmd_leg(path: str, args) -> None:
    state = load(path)
    leg = state["leg"]
    n_rooms = len(state["faces"])
    if leg >= n_rooms:
        raise SystemExit(f"Site exhausted: all {n_rooms} rooms run. The "
                         f"objective room was Room "
                         f"{max(range(n_rooms), key=lambda i: state['depths'][i]) + 1}; "
                         f"anything further is authored content.")
    i = leg                      # 0-based room index, roll order
    face = state["faces"][i]
    die = state["room_dice"][i]
    depth = state["depths"][i]
    tier = state["tier"]
    tier_desc, minor, standard, apex = TIERS[tier]
    threat_text, progressive = THREATS[state["threat"]]

    out = [f"=== LEG {i + 1}/{n_rooms} -- {state['site']} -- Room {i + 1} "
           f"(d{die} face {face}, depth {depth}) ===",
           f"  Tier {tier} ({tier_desc}); bands: minor {minor} / standard "
           f"{standard} / apex {apex}  [module 2B]"]

    text, kind = STOCKING[face]
    out.append(f"  STOCKING TABLE face {face}: {text}")

    # -- layer passes in module order (Frame->Site->Stock->Run->Resolve; the
    # Run layers delegated to dungeon-state-tables.md get NO COVERAGE lines).
    if kind == "empty":
        out.append(f"  PERSISTENT THREAT IS THE ENCOUNTER (module: 'It IS "
                   f"the encounter in every result-1 room'):")
        out.append(f"    Threat {state['threat']}: {threat_text}")
    elif kind == "denizen":
        out.append("  DENIZEN ROLLS (udrp-monster-ecology-module.md, Layer 1 "
                   "-- the script names the row; pull the creature from the "
                   "module/bestiary, never from here):")
        cat, line = roll(12, "ecology Layer 1A creature category")
        out.append(line)
        out.append(f"    -> monster-ecology Layer 1A row {cat}: "
                   f"{ECO_CATEGORY[cat]}")
        beh, line = roll(8, "ecology Layer 1B behavior pattern")
        out.append(line)
        out.append(f"    -> monster-ecology Layer 1B row {beh}: "
                   f"{ECO_BEHAVIOR[beh]}")
        strength = (apex if face == 12 else minor if face == 4 else
                    standard if face == 6 else
                    f"{standard} upper band (elite, ~APL+2)" if face == 8
                    else standard)
        out.append(f"    Strength for Tier {tier}: {strength}; theme to "
                   f"builder ({BUILDERS[state['builder']]}) and site state "
                   f"({STATES[state['state']]}).")
    elif kind == "puzzle":
        ptype, line = roll(8, "puzzle type (module Puzzle Generation)")
        out.append(line)
        out.append(f"    -> Puzzle type {ptype}: {PUZZLES[ptype]} -- set "
                   f"difficulty from the room's tier band; build it against "
                   f"what THIS party can actually do (Heart of Winter's "
                   f"Grief standard). Failure on face 9 triggers a hazard.")
    elif kind == "ward":
        out.append(f"    Ward/trap themed to the builder "
                   f"({BUILDERS[state['builder']]}); DC at the tier "
                   f"{'deadly' if face == 11 else 'hard'} band.")
        out.append(f"    Ward degradation: {NO_COVERAGE_STATE}")
    elif kind == "treasure":
        out.append("    TREASURE: roll the D4 Item Roller at the site's "
                   "tier -- NO COVERAGE here; nearest engine: the loot-engine "
                   "skill (campaign loot pipeline). Usually guarded -- fold "
                   "in a denizen or make it the Persistent Threat's nest.")
    elif kind == "lore":
        out.append("    Lore/discovery: environmental story; mechanical "
                   "discovery model lives in dungeon-state-tables.md "
                   "(NO COVERAGE here). No fight.")

    # -- persistent threat pressure on every leg
    if kind != "empty":
        out.append(f"  SITE-WIDE PRESSURE: Threat {state['threat']} "
                   f"({threat_text.split(' -- ')[0]}) applies per module "
                   f"Layer 3.")
    if progressive:
        clocks = state.setdefault("clocks", {})
        clocks["exposure"] = clocks.get("exposure", 0) + 1
        out.append(f"  EXPOSURE CLOCK ticks -> {clocks['exposure']} "
                   f"(progressive threat; longer the stay / deeper the "
                   f"level, worse the roll -- module Layer 3 rows 3/4/6). "
                   f"Penalty scaling is interpreted on the module row; "
                   f"clock 8+ is a World-Move Law trigger state.")

    # -- live-run layers the module delegates
    out.append(f"  LIVE-RUN LAYERS: {NO_COVERAGE_STATE}")

    state["leg"] = i + 1
    save(path, state)
    out.append(f"\n  Leg complete. One leg per output (one-leg-per-output "
               f"law); next invocation runs Room {i + 2}."
               if i + 1 < n_rooms else
               "\n  Leg complete. That was the final room.")
    print("\n".join(out))


def cmd_clock(path: str, args) -> None:
    state = load(path)
    clocks = state.setdefault("clocks", {})
    name = args.name
    if args.set is not None:
        clocks[name] = args.set
    elif args.advance:
        clocks[name] = clocks.get(name, 0) + args.advance
    save(path, state)
    if not clocks:
        print("(no clocks seated)")
        return
    for k, v in clocks.items():
        flag = "  <- WORLD-MOVE TRIGGER (clock at 8+)" if v >= 8 else ""
        print(f"  clock {k}: {v}{flag}")


def cmd_show(path: str, args) -> None:
    state = load(path)
    print(f"=== {state['site']} (Tier {state['tier']}, "
          f"{'descent bias' if state['descent_bias'] else 'standard parity'}) ===")
    print(f"  Type {state['site_type']}: {SITE_TYPES[state['site_type']]}")
    print(f"  Builder {state['builder']}: {BUILDERS[state['builder']]}")
    print(f"  State {state['state']}: {STATES[state['state']]}")
    print(f"  Threat {state['threat']}: {THREATS[state['threat']][0]}")
    print(f"  Objective {state['objective']}: {OBJECTIVES[state['objective']]}")
    for i, (s, f_, d) in enumerate(zip(state["room_dice"], state["faces"],
                                       state["depths"]), 1):
        mark = "RUN" if i <= state["leg"] else "unvisited"
        print(f"  Room {i}: d{s} face {f_} depth {d}  [{mark}]")
    for k, v in state.get("clocks", {}).items():
        print(f"  clock {k}: {v}")

# ============================================================================
# SELFTEST -- structure checks, parity math, worked delve in a temp dir
# ============================================================================

class _Args:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def selftest() -> int:
    ok = True

    def expect(label, cond):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
        ok = ok and cond

    print("### udrp_delve.py SELFTEST ###\n")
    print("-- table structure --")
    expect("Stocking Table has faces 1..12", sorted(STOCKING) == list(range(1, 13)))
    expect("Site types 1..20", sorted(SITE_TYPES) == list(range(1, 21)))
    expect("Builders 1..12", sorted(BUILDERS) == list(range(1, 13)))
    expect("States 1..10", sorted(STATES) == list(range(1, 11)))
    expect("Threats 1..12", sorted(THREATS) == list(range(1, 13)))
    expect("Objectives 1..12", sorted(OBJECTIVES) == list(range(1, 13)))
    expect("Puzzles 1..8", sorted(PUZZLES) == list(range(1, 9)))
    expect("Ecology category 1..12 / behavior 1..8",
           sorted(ECO_CATEGORY) == list(range(1, 13))
           and sorted(ECO_BEHAVIOR) == list(range(1, 9)))
    expect("Die/room table is d4/d6/d8/d10/d12",
           sorted(DIE_ROOMS) == [4, 6, 8, 10, 12])
    expect("Progressive threats are exactly rows 3, 4, 6 (module Layer 3)",
           [k for k, (_, p) in sorted(THREATS.items()) if p] == [3, 4, 6])

    print("\n-- stairs-by-parity math (module Step 4 worked example: faces "
          "1,3,4,10,2 -> same, UP, same, same) --")
    expect("worked example parity", compute_depths([1, 3, 4, 10, 2], False)
           == [0, 0, -1, -1, -1])
    expect("even->odd is DOWN", stairs_text(4, 3, False) == "DOWN")
    expect("odd->even is UP", stairs_text(3, 4, False) == "UP")
    expect("descent bias: every parity change sinks",
           compute_depths([1, 3, 4, 10, 2], True) == [0, 0, 1, 1, 1])

    print("\n-- dice sanity --")
    vals = [_throw(12) for _ in range(60)]
    expect("60 d12 throws in 1..12", all(1 <= v <= 12 for v in vals))
    expect("not all identical", len(set(vals)) > 1)

    print("\n-- worked delve in a temp dir (raw output follows) --\n")
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "selftest.delve.json")
        cmd_new(p, _Args(site="Selftest Barrow", dice="d4,d6,d10",
                         tier="III", descent_bias=True, force=False,
                         set_type=8, set_builder=7, set_state=9,
                         set_threat=4, set_objective=6))
        s = load(p)
        expect("\nauthored layers stored as fixed",
               (s["site_type"], s["builder"], s["state"], s["threat"],
                s["objective"]) == (8, 7, 9, 4, 6))
        expect("exposure clock seated (threat 4 is progressive)",
               s["clocks"].get("exposure") == 0)
        print()
        cmd_leg(p, _Args())
        s = load(p)
        expect("\nleg counter advanced to 1", s["leg"] == 1)
        expect("exposure ticked to 1", s["clocks"]["exposure"] == 1)
        print()
        cmd_leg(p, _Args())
        cmd_leg(p, _Args())
        try:
            cmd_leg(p, _Args())
            expect("4th leg on 3-room site refused", False)
        except SystemExit:
            expect("4th leg on 3-room site refused", True)
        cmd_clock(p, _Args(name="exposure", advance=5, set=None))
        expect("clock 8+ flags World-Move trigger",
               load(p)["clocks"]["exposure"] == 8)
        print()
        cmd_show(p, _Args())

    print(f"\nSELFTEST {'PASSED' if ok else 'FAILED'}.")
    return 0 if ok else 1

# ============================================================================
# CLI
# ============================================================================

def main():
    global FOUR_THROW
    p = argparse.ArgumentParser(
        description="UDRP dungeon-leg roller: site entry, one-leg-per-"
                    "invocation engine passes, exposure clocks. State in an "
                    "explicit *.delve.json.")
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--four-throw", action="store_true",
                   help="Bind every roll over four throws, mode-else-median "
                        "(Standing Law G2) instead of single raw throws "
                        "(the module's own worked-example format).")
    p.add_argument("state", nargs="?", help="Path to the site's *.delve.json.")
    sub = p.add_subparsers(dest="command")

    sp = sub.add_parser("new", help="Site entry: roll structure + Layer 3 "
                                    "Persistent Threat, throw the room dice.")
    sp.add_argument("--site", required=True)
    sp.add_argument("--dice", required=True,
                    help="Room dice, e.g. d4,d6,d6,d10,d12 (die = size + "
                         "danger ceiling).")
    sp.add_argument("--tier", default="III",
                    help="Party tier I-V (module 2B; default III).")
    sp.add_argument("--descent-bias", action="store_true",
                    help="Vertical-site override: every parity change is a "
                         "step DOWN; same parity is a side-chamber.")
    sp.add_argument("--force", action="store_true")
    for name in ("type", "builder", "state", "threat", "objective"):
        sp.add_argument(f"--set-{name}", type=int, default=None,
                        dest=f"set_{name}",
                        help=f"Authored-Skeleton mode: fix Layer {name} "
                             f"instead of rolling.")

    sub.add_parser("leg", help="Run ONE room's full engine pass (one-leg-"
                               "per-output law).")

    sp = sub.add_parser("clock", help="Advance/read exposure & environment "
                                      "clocks.")
    sp.add_argument("name")
    sp.add_argument("--advance", type=int, default=0)
    sp.add_argument("--set", type=int, default=None)

    sub.add_parser("show", help="Print the site summary and room states.")

    args = p.parse_args()
    if args.selftest:
        sys.exit(selftest())
    FOUR_THROW = args.four_throw
    if not args.state or not args.command:
        p.print_help()
        sys.exit(1)
    handlers = {"new": cmd_new, "leg": cmd_leg, "clock": cmd_clock,
                "show": cmd_show}
    handlers[args.command](args.state, args)


if __name__ == "__main__":
    main()
