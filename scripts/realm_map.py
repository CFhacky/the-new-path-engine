#!/usr/bin/env python3
"""
realm_map.py -- Regno Kao folio roller: area maps for the warp realms of
The End and the Death (the-new-path-engine)

Per-realm area-map resolver for the TEATD psychotecture bands of the
empyrean-siege-gm skill. `new` rolls a realm's areas, exits and hazards ONCE
(real dice, raws printed) and writes an explicit *.realm.state.json; `render`
draws the same state deterministically as an SVG folio page and a GM area
sheet, so the map is repeatable without seeds or rerolls.

GOVERNING SOURCES
    reference/teatd_realm_index.json (scripts/teatd_realm_harvest.py)
        -- the realm roster: archetype, SOURCE-VERIFIED facts with
           chapter:verse, and the INFERRED myth key whose one-line rule is
           the law of the place. This script never restates a fact the index
           does not carry; it prints the index rows under their own labels.
    empyrean-siege-gm skill, "TEATD bands (modules 05-07)"
        -- expected vs. experienced location are tracked separately; map
           contradiction and false continuity are hazards, not flavour.
           The psychotecture contradiction table below implements that
           sentence and nothing more.
    Vol. III 9:xxi / 10:iii / 10:viii (via the index)
        -- the edge vocabulary: angle, intersection, conjunction, oblique,
           splice, recursion.

CONTRACT NOTES
    - Label discipline (the skill's vocabulary): every line of output is
      SOURCE-VERIFIED (from the index facts), INFERRED (the myth key) or
      ROLLED (this script's dice). The archetype tables themselves are
      APPROVED PREPARATION pending Chad's ratification and say so in the
      header of every sheet; they are not canon and not source.
    - Conditions are refused. A row whose archetype is "condition" is a
      cosmological designation or overlay, not a place; `new` prints its
      rule as a modifier and exits 2.
    - Threat band (0-5) is taken from the caller and printed; its meaning
      lives in the siege package's mechanical reference (NO COVERAGE here).
    - No denizens, no stats, no items: hazards print as bands and rules; the
      instance pulls creatures from the bestiary and the package.
    - State files are throwaway (*.state.json is gitignored).

USAGE
    python realm_map.py --list
    python realm_map.py long_woe.realm.state.json new --realm "Long Woe" \\
        [--areas d6|d8|d10|d12] [--band 0-5] [--entry "how the party arrives"] [--force]
    python realm_map.py long_woe.realm.state.json render [--svg out.svg] [--sheet out.md]
    python realm_map.py long_woe.realm.state.json show
    python realm_map.py --selftest
"""
from __future__ import annotations

import argparse
import json
import math
import os
import secrets
import sys
import tempfile
from html import escape
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO = Path(__file__).resolve().parent.parent
INDEX = REPO / "reference" / "teatd_realm_index.json"
PREP_NOTE = ("Archetype tables: APPROVED PREPARATION (realm_map.py), pending "
             "ratification; not source, not canon.")

# ============================================================================
# DICE -- secrets only, raw first. Single throw default; --four-throw applies
# the Standing Law G2 four-throw bind (as udrp_delve.py).
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


def roll(sides: int, label: str, ledger: List[str]) -> int:
    if FOUR_THROW:
        raws = [_throw(sides) for _ in range(4)]
        bound, how = bind_four(raws)
        ledger.append(f"  d{sides} throws {raws} -> bind {bound} ({how})  [{label}]")
        return bound
    raw = _throw(sides)
    ledger.append(f"  d{sides} = {raw}  [{label}]")
    return raw

# ============================================================================
# TABLES -- APPROVED PREPARATION. Eight archetype grammars. Each carries:
#   layout  : how render() places the areas
#   areas   : d12 -> (area kind, dimensions)   the scene-setting measurements
#   hazards : d6  -> hazard band text          what the area does to you
#   law     : d6  -> the archetype's law-roll   the parameter the myth rule needs
# ============================================================================
ARCH: Dict[str, Dict[str, Any]] = {
    "composite-city": {
        "layout": "ring",
        "areas": {
            1: ("Alley of a stolen city", "4 yd wide, 60 yd long, walls 3 storeys"),
            2: ("Alley of a stolen city", "3 yd wide, 90 yd long, roofs touching overhead"),
            3: ("Cobbled street", "10 yd wide, 150 yd long, decaying tiled roofs both sides"),
            4: ("Cobbled street", "12 yd wide, 200 yd long; one Palatine street bisects it"),
            5: ("Ivy-draped turret and its stair", "8 yd across, 25 yd tall, stair 1 yd wide"),
            6: ("Market square", "60 x 60 yd, stalls of three different cities"),
            7: ("Wall-top and battlement", "5 yd wide walk, 400 yd long, 30 yd drop"),
            8: ("Black-stone fortification gate", "15 yd arch, 20 yd deep passage"),
            9: ("Collapsed district", "120 x 120 yd rubble field, walls fallen in masses"),
            10: ("Plaza of a stolen city", "200 x 200 yd, monumental and empty"),
            11: ("Ash-ribbon avenue", "30 yd wide charred track, ash 1 ft deep"),
            12: ("Primeval stratum", "grey-diorite hall 80 x 40 yd, columns 12 yd, no human doors"),
        },
        "hazards": {
            1: "Quiet. The city watches; nothing acts this interval.",
            2: "Wall-fall: masonry collapse across the area, sheets of black dust (cover, blindness for one interval).",
            3: "Intrusion: a smouldering battlefield from another place is folded into this street (fire, smoke, unexploded ordnance).",
            4: "Old occupant: whatever lived in the stolen district still keeps its hours here (denizen from the bestiary at the band).",
            5: "Ethereal tide: the district shifts one district over; exits re-roll their type.",
            6: "Parasite architecture: the city bores through what you brought with you (gear, a vehicle, a wall you were holding).",
        },
        "law": {
            1: "Stratum depth 1: today's stolen streets; doors fit people.",
            2: "Stratum depth 2: streets of a century ago.",
            3: "Stratum depth 3: cities nobody living remembers.",
            4: "Stratum depth 4: pre-Imperial masonry; stairs at the wrong pitch.",
            5: "Stratum depth 5: nothing human built this; every human fragment is a memory and a possible exit.",
            6: "Stratum depth 6: primeval; the district is older than the species and does not agree it is a city.",
        },
    },
    "labyrinth": {
        "layout": "branch",
        "areas": {
            1: ("Corridor", "2 yd wide, 40 yd long, one turn"),
            2: ("Corridor", "3 yd wide, 80 yd long, three turns"),
            3: ("Chamber", "12 x 12 yd, four doors"),
            4: ("Chamber", "20 x 15 yd, two doors, one sealed"),
            5: ("Gallery", "6 yd wide, 120 yd long, receding toward a vanishing point"),
            6: ("Stair", "1.5 yd wide, 60 steps, direction uncertain"),
            7: ("Court", "40 x 40 yd open to a black sky"),
            8: ("Dead end", "3 x 3 yd; the way in has closed"),
            9: ("Hall of corners", "30 x 30 yd, nothing upright"),
            10: ("Salt chamber", "18 x 9 yd, asymmetric, crust underfoot"),
            11: ("Dune-walled lane", "8 yd wide between pink stone walls, no end visible"),
            12: ("Heart", "60 x 60 yd; whatever set the trap is here"),
        },
        "hazards": {
            1: "Quiet. The walls are patient.",
            2: "Closure: an exit you have already used is gone.",
            3: "Doubling: the next area is this area again, mirrored.",
            4: "Occupant: something walks the corridors on a fixed circuit (denizen at the band).",
            5: "Angle-hunter: something enters through a corner (band +1).",
            6: "The maker looks: the labyrinth notices you; every later hazard roll is at +1.",
        },
        "law": {
            1: "Rooms close one interval after you leave them.",
            2: "Rooms close two intervals after you leave them.",
            3: "Rooms close when nobody is looking at the door.",
            4: "Rooms close only behind the last person through.",
            5: "Rooms do not close, but they move.",
            6: "Nothing closes; the exit is simply not on the map until it is granted.",
        },
    },
    "crossing": {
        "layout": "chain",
        "areas": {
            1: ("Approach", "a shelf 20 x 10 yd at the brink"),
            2: ("Approach", "a shattered platform 30 x 30 yd, half fallen away"),
            3: ("The span", "narrow bridge, width by the law roll, 150 yd over nothing"),
            4: ("The span", "a stair of brazen steps, 2 yd wide, 200 steps"),
            5: ("The span", "a causeway of ship-deck plating, 8 yd wide, ends moving"),
            6: ("Mid-crossing", "a landing 10 x 10 yd suspended over the pit"),
            7: ("Gate", "dolmen portal, 4 yd wide, 6 yd tall, lintel humming"),
            8: ("Gate", "a tear in the air, doorway-sharp, 1 yd wide"),
            9: ("Far bank", "a ledge 15 x 8 yd; the other realm begins here"),
            10: ("Far bank", "a hall 40 x 20 yd whose floor is the other side"),
            11: ("Under the span", "hanging structure 20 x 5 yd; the pit is below and above"),
            12: ("The pit's lip", "a slope 50 yd long into the aeonic dark"),
        },
        "hazards": {
            1: "Quiet. The crossing waits.",
            2: "Narrowing: the span loses one width band while you are on it.",
            3: "Pursuit: something crosses behind you and it is not slowed by the law.",
            4: "Toll: the crossing takes something (a memory, a name, an item) from one crosser.",
            5: "Tremor: the gate or span shudders; a fall check for everyone on it.",
            6: "Both ends move: the far bank is not the realm you were crossing to.",
        },
        "law": {
            1: "Width band 1: a hair. Only the worthy cross, one at a time, no gear.",
            2: "Width band 2: a plank. Single file, balance every interval.",
            3: "Width band 3: a footpath. Single file, balance under fire.",
            4: "Width band 4: a cart's width. Two abreast.",
            5: "Width band 5: a road. Vehicles cross.",
            6: "Width band 6: a highway; the crossing is not the danger, what waits on it is.",
        },
    },
    "junction": {
        "layout": "star",
        "areas": {
            1: ("The hub", "a crossroads 30 x 30 yd under a fixed sky"),
            2: ("Spoke", "a lane 5 yd wide, 100 yd, thorn trees both sides"),
            3: ("Spoke", "twilit cliffs, ledge 3 yd wide, 200 yd"),
            4: ("Spoke", "a corridor of malnourished light, 4 yd wide, no end"),
            5: ("Spoke", "a stair sideways, 2 yd wide, 80 steps"),
            6: ("Spoke", "a plain 300 yd across under the skull moon"),
            7: ("Spoke", "a bleak plateau, 500 yd, wind"),
            8: ("Spoke", "a bridge of thorns, 1 yd wide, 60 yd"),
            9: ("Spoke", "a lane of doors, 6 yd wide, 90 yd, all locked"),
            10: ("Spoke", "a slope of ash 150 yd down"),
            11: ("Spoke", "a gallery of the Court, 8 yd wide, receding"),
            12: ("Spoke", "a splice: a courtyard 40 x 40 yd with one cell door in it"),
        },
        "hazards": {
            1: "Quiet. The roads hold still.",
            2: "Sorting: the junction sends one traveller down the exit their nature chooses, not the one they chose.",
            3: "Flanked: something arrives beside the party from a spoke that was not open.",
            4: "Toll: crossing the hub ages the crosser one interval of exposure.",
            5: "Inertia: nobody can leave the hub this interval; the spokes are closed.",
            6: "Every road at once: the party is split across two spokes.",
        },
        "law": {
            1: "One exit open.", 2: "Two exits open.", 3: "Three exits open.",
            4: "Four exits open.", 5: "Five exits open.",
            6: "All exits open, and one of them is the way you came in, leading elsewhere.",
        },
    },
    "fortress": {
        "layout": "concentric",
        "areas": {
            1: ("Outer approach", "a dark road 8 yd wide, 400 yd to the wall, no cover"),
            2: ("Outer approach", "stained margin 200 yd wide, footing bad"),
            3: ("Outer approach", "a killing ground 150 x 150 yd under the walls"),
            4: ("Gatehouse", "arch 6 yd wide, passage 20 yd, murder holes"),
            5: ("Outer ward", "60 x 40 yd yard, mildewed stone, water underfoot"),
            6: ("Curtain wall walk", "3 yd wide, 300 yd, 20 yd drop"),
            7: ("Inner ward", "40 x 30 yd, well in the centre"),
            8: ("Hall", "30 x 15 yd, roof half gone"),
            9: ("Chapel", "20 x 10 yd, altar to no one"),
            10: ("Keep stair", "1.5 yd wide, 90 steps, mildew"),
            11: ("Keep chamber", "15 x 15 yd, one window onto the margins"),
            12: ("Roof", "12 x 12 yd, view over the Planes"),
        },
        "hazards": {
            1: "Quiet. The garrison, if any, keeps its hours.",
            2: "Dread on the approach: a Will/Fright band on everyone crossing this area.",
            3: "Watched: the keep tells its master; every later hazard at +1.",
            4: "Garrison: a picket holds this area (denizens at the band).",
            5: "Working: a hostile Chaos working seated here; dispel or endure.",
            6: "The fringe burns: the area is on fire from the outside in; one interval to cross.",
        },
        "law": {
            1: "Dread band 1: unease; no roll.", 2: "Dread band 2: a check on the approach.",
            3: "Dread band 3: a check per approach area.", 4: "Dread band 4: a check per interval outside the walls.",
            5: "Dread band 5: a check per interval anywhere; animals will not enter.",
            6: "Dread band 6: the approaches are the fight; the keep itself is empty and quiet.",
        },
    },
    "wilderness": {
        "layout": "scatter",
        "areas": {
            1: ("Meadow", "200 x 120 yd, waist-high, wet"),
            2: ("Glade", "60 yd across, twilit, ringed by trees that lean in"),
            3: ("Forest", "half a mile of it; visibility 20 yd"),
            4: ("Fen", "300 yd of standing water and tussocks, depth uncertain"),
            5: ("Dune field", "dunes 15 yd high, 80 yd apart, no fixed sun"),
            6: ("Bone-bed", "a ridge 400 yd long that is a ribcage"),
            7: ("Ash plain", "a mile of white ash under a black sky"),
            8: ("Steppe", "open ground to the horizon, no time, no cover"),
            9: ("Folded shelf", "a cliff-terrace 100 yd wide with a dead city clinging below"),
            10: ("Valley", "a defile 40 yd wide, 500 yd long, things in the walls"),
            11: ("Garden", "120 x 120 yd of something planted; it hums"),
            12: ("The end-state", "the realm is ending here: steam, sand, ash or mist across 200 yd"),
        },
        "hazards": {
            1: "Quiet. The ground pretends.",
            2: "Footing: the ground gives (sink, slide, fall) for anyone who stops.",
            3: "The living terrain speaks: cut, burn or dig and it answers (fear band, and it is heard).",
            4: "Swarm: something breeds here and the party is noise (denizens at the band, psykers first).",
            5: "Fever: one interval here costs a Fortitude/HT band; sleep here and it is yours.",
            6: "Ending: the end-state advances one area toward the party.",
        },
        "law": {
            1: "One interval before the end-state reaches this folio.",
            2: "Two intervals.", 3: "Three intervals.", 4: "Four intervals.", 5: "Five intervals.",
            6: "The end-state is not yet coming; the realm is stable for this visit.",
        },
    },
    "shore": {
        "layout": "coast",
        "areas": {
            1: ("Strand", "a beach 300 yd long, 40 yd to the waterline"),
            2: ("Strand", "shingle 200 yd, things washed up"),
            3: ("Headland", "a promontory 80 yd out, 20 yd above the water"),
            4: ("Sea-cave", "30 x 10 yd, tide-line on the roof"),
            5: ("Islet", "60 yd across, life expectancy by the law roll"),
            6: ("Islet", "150 yd across, a dead ship on it"),
            7: ("Pier", "a spar of psychoplastic 5 yd wide, 120 yd out"),
            8: ("Shallows", "knee-deep for 200 yd; then it is not"),
            9: ("Trench edge", "the sea-floor falls away; pressure begins"),
            10: ("Far dark", "the outer darkness begins 100 yd out; nothing returns"),
            11: ("Wreck-field", "300 x 100 yd of fused hulls, half in the water"),
            12: ("Tide-flat", "a mile of exposed bed at low tide, with what it carried"),
        },
        "hazards": {
            1: "Quiet. The tide is between.",
            2: "Tide turns: one area floods or drains this interval.",
            3: "Something surfaces: a trench thing, dying as it comes (denizen at the band, one interval of life).",
            4: "Undertow: whoever is in the water is one area further out.",
            5: "The dead are exposed: the tide-line gives up bodies and what they carried (lore, and it is noticed).",
            6: "Combustion: an islet or wreck goes up; light for miles.",
        },
        "law": {
            1: "Tide: dead low. The bed is exposed and so is everything on it.",
            2: "Tide: falling. Two intervals of exposed ground.",
            3: "Tide: slack. Nothing moves for one interval.",
            4: "Tide: rising. Lose one strand area per interval.",
            5: "Tide: high. The living are taken from the waterline.",
            6: "Tide: storm. The sea is on the shore; islets last one interval each.",
        },
    },
    "repository": {
        "layout": "stacks",
        "areas": {
            1: ("Reading room", "20 x 20 yd, one table, no chairs"),
            2: ("Stack", "a shelf-corridor 2 yd wide, 200 yd, shelves to the dark"),
            3: ("Stack", "a spiral of shelves 40 yd across, no floor between turns"),
            4: ("Index", "a hall 60 x 30 yd; the catalogue is a person"),
            5: ("Root-hall", "a cavern 80 yd across under a root 10 yd thick"),
            6: ("Vault", "12 x 12 yd, one thing in it"),
            7: ("Burned wing", "100 x 40 yd of ash-shelves, still warm"),
            8: ("Dream-gallery", "50 yd of doors, each a mislaid night"),
            9: ("Ledger room", "15 x 15 yd; the names taken are written here"),
            10: ("Canopy", "branches 30 yd up, a walkway 1 yd wide"),
            11: ("Cistern", "water-mirror 30 x 30 yd; it scries"),
            12: ("Heart-shelf", "the one thing you came for, and the shelf behind it"),
        },
        "hazards": {
            1: "Quiet. The shelves keep.",
            2: "Fire behind: the last area taken from burns; no return that way.",
            3: "Custodian: the place has a keeper and it counts (denizen at the band, social first).",
            4: "Mislaid: one item the party carries is now shelved; find it or leave it.",
            5: "Root-slip: a root is a route; someone is on another folio.",
            6: "Unwritten: the party finds a plan of their own that they did not make.",
        },
        "law": {
            1: "One thing may leave with the party.",
            2: "One thing may leave; taking a second burns a wing.",
            3: "One thing per person, and the place remembers each.",
            4: "Nothing leaves that was not brought; what was brought may be exchanged.",
            5: "Anything may leave; the price is a name from the ledger.",
            6: "Nothing leaves. The repository is complete and you are now in the catalogue.",
        },
    },
}

# Structural slots -- a crossing always has an approach, a span and a far
# bank; a fortress always has approaches, a gate and a keep; a junction always
# has its hub. Each slot is still rolled, but from the rows that fit the role.
SLOTS: Dict[str, Dict[str, Any]] = {
    "crossing": {"min": 3, "first": [1, 2], "middle": [3, 4, 5], "last": [9, 10]},
    "fortress": {"min": 3, "first": [1, 2, 3], "middle": [4], "last": [10, 11, 12]},
    "junction": {"min": 3, "first": [1], "middle": None, "last": None},
}

# Edge type by d6 -- the trilogy's own vocabulary (index.edge_types)
EDGES = {1: "angle", 2: "intersection", 3: "conjunction", 4: "oblique", 5: "splice", 6: "recursion"}

# Psychotecture contradiction (d8) -- implements the skill's TEATD band rule
# that map contradiction and false continuity are hazards. Faces 1-3 are
# stable so the seeds stay sparse.
CONTRADICTION = {
    1: None, 2: None, 3: None,
    4: "FALSE CONTINUITY: the party's expected location and experienced location disagree here; narrate the expected one until an anchor fails.",
    5: "MAP CONTRADICTION: this area's exits do not match the way it was entered; the folio and the ground disagree, and the ground is lying.",
    6: "DOUBLED PLACE: a second copy of an earlier area is here, with one detail wrong; the wrong detail is the tell.",
    7: "MISSING EXIT: one rolled exit is absent when reached; it returns when nobody expects it to.",
    8: "OFF-FOLIO INTRUSION: a memory of another realm is spliced into this area (rolled below); its law applies inside the splice.",
}

# ============================================================================
# INDEX
# ============================================================================

def load_index() -> Dict[str, Any]:
    if not INDEX.is_file():
        raise SystemExit(f"NO COVERAGE -- realm index missing at {INDEX}; run scripts/teatd_realm_harvest.py")
    with open(INDEX, "r", encoding="utf-8") as f:
        return json.load(f)


def find_realm(index: Dict[str, Any], query: str) -> Dict[str, Any]:
    q = query.casefold().strip()
    exact = [r for r in index["realms"]
             if r["name"].casefold() == q or q in (a.casefold() for a in r.get("aliases", []))]
    if len(exact) == 1:
        return exact[0]
    partial = [r for r in index["realms"]
               if q in r["name"].casefold() or any(q in a.casefold() for a in r.get("aliases", []))]
    if len(partial) == 1:
        return partial[0]
    if not partial:
        raise SystemExit(f"No realm matches {query!r}. Try --list.")
    names = ", ".join(r["name"] for r in partial)
    raise SystemExit(f"Ambiguous realm {query!r}: {names}")


def mappable(index: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [r for r in index["realms"] if r.get("mappable")]

# ============================================================================
# STATE
# ============================================================================

def load(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        raise SystemExit(f"No realm state at {path!r} -- run `new` first.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save(path: str, state: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


AREA_DICE = {"d6": 6, "d8": 8, "d10": 10, "d12": 12}


def topology(layout: str, n: int, ledger: List[str]) -> List[Tuple[int, int, str]]:
    """Rolled edges between 1-based area indices. Every layout is at least a
    connected chain from A1; the extra rolled links are what the archetype
    grammar adds."""
    edges: List[Tuple[int, int, str]] = []
    if layout == "star":
        for i in range(2, n + 1):
            edges.append((1, i, EDGES[roll(6, f"spoke A1-A{i} edge type", ledger)]))
        return edges
    for i in range(1, n):
        edges.append((i, i + 1, EDGES[roll(6, f"exit A{i}-A{i + 1} edge type", ledger)]))
    if n < 3:
        return edges
    if layout == "ring":
        edges.append((n, 1, EDGES[roll(6, f"ring closure A{n}-A1 edge type", ledger)]))
        a = roll(n, "chord from area", ledger)
        b = roll(n, "chord to area", ledger)
        if a != b and abs(a - b) not in (1, n - 1):
            edges.append((min(a, b), max(a, b), EDGES[roll(6, "chord edge type", ledger)]))
    elif layout == "branch":
        for i in range(1, n + 1):
            if roll(2, f"A{i} spur?", ledger) == 2:
                edges.append((i, 0, "closed"))  # 0 = a spur that has closed behind
    elif layout == "scatter":
        a = roll(n, "extra link from area", ledger)
        b = roll(n, "extra link to area", ledger)
        if a != b and abs(a - b) != 1:
            edges.append((min(a, b), max(a, b), EDGES[roll(6, "extra link edge type", ledger)]))
    elif layout == "stacks":
        a = roll(n, "recursion seat", ledger)
        edges.append((a, a, "recursion"))
    elif layout == "concentric":
        # approaches (first third) all touch the gate (the area after them)
        gate = max(2, (n + 2) // 3 + 1)
        for i in range(1, gate - 1):
            if (i, i + 1, None)[:2] != (i, gate):
                edges.append((i, gate, EDGES[roll(6, f"approach A{i} to gate A{gate} edge type", ledger)]))
    return edges

# ============================================================================
# COMMANDS
# ============================================================================

def cmd_new(path: str, args) -> None:
    if os.path.exists(path) and not args.force:
        raise SystemExit(f"{path} exists -- pass --force to overwrite.")
    index = load_index()
    realm = find_realm(index, args.realm)
    if not realm.get("mappable"):
        print(f"NOT MAPPABLE -- {realm['name']} is a {realm['archetype']} "
              f"({realm['classification']}).")
        print(f"  Apply as an overlay/modifier on another realm's folio. Rule (INFERRED): "
              f"{realm['myth_key']['rule']}")
        sys.exit(2)
    if args.areas not in AREA_DICE:
        raise SystemExit(f"--areas must be one of {sorted(AREA_DICE)}")
    if not 0 <= args.band <= 5:
        raise SystemExit("--band must be 0-5 (siege package threat bands)")
    arch = ARCH[realm["archetype"]]
    ledger: List[str] = []
    ledger.append(f"=== FOLIO ENTRY -- {realm['name']} ({realm['archetype']}) ===")
    ledger.append(f"({PREP_NOTE} Raw dice first.)")
    n = roll(AREA_DICE[args.areas], f"area count ({args.areas})", ledger)
    slots = SLOTS.get(realm["archetype"], {"min": 2, "first": None, "middle": None, "last": None})
    n = max(n, slots["min"])
    law = roll(6, "law roll (the myth rule's parameter)", ledger)
    span_at = (n + 1) // 2 if slots["middle"] else None
    areas = []
    for i in range(1, n + 1):
        rows = None
        if i == 1 and slots["first"]:
            rows, why = slots["first"], "first slot"
        elif i == n and slots["last"]:
            rows, why = slots["last"], "last slot"
        elif i == span_at and slots["middle"]:
            rows, why = slots["middle"], "middle slot"
        if rows is None:
            face = roll(12, f"A{i} area kind", ledger)
        elif len(rows) == 1:
            face = rows[0]
            ledger.append(f"  A{i} area kind fixed by the {why}: row {face}")
        else:
            face = rows[roll(len(rows), f"A{i} area kind ({why}: rows {rows})", ledger) - 1]
        hz = roll(6, f"A{i} hazard band", ledger)
        cz = roll(8, f"A{i} psychotecture contradiction", ledger)
        area = {"n": i, "face": face, "kind": arch["areas"][face][0],
                "dimensions": arch["areas"][face][1], "hazard": hz,
                "contradiction": cz}
        if cz == 8:
            others = [r["name"] for r in mappable(index) if r["name"] != realm["name"]]
            k = roll(len(others), f"A{i} intruding realm (1-{len(others)} of the mappable roster)", ledger)
            area["intrusion"] = others[k - 1]
        areas.append(area)
    edges = topology(arch["layout"], n, ledger)
    state = {
        "realm": realm["name"], "archetype": realm["archetype"], "layout": arch["layout"],
        "band": args.band, "entry": args.entry or "",
        "areas_die": args.areas, "law": law, "areas": areas,
        "edges": [list(e) for e in edges],
        "index_snapshot": {
            "classification": realm["classification"],
            "facts": realm["facts"], "facts_label": realm.get("facts_label", "SOURCE-VERIFIED"),
            "attestations": [f"Vol. {'I' * a['volume']} {a['chapter']}:{a['verse']}" for a in realm["attestations"]],
            "myth_key": realm["myth_key"],
        },
        "ledger": ledger,
    }
    save(path, state)
    print("\n".join(ledger))
    print()
    print(f"  {n} areas rolled; law roll {law}: {arch['law'][law]}")
    print(f"  State written: {path}. Render with `render`; re-rendering is deterministic.")


def _positions(layout: str, n: int, w: int, h: int) -> List[Tuple[float, float]]:
    cx, cy = w / 2, h / 2 + 20
    pos: List[Tuple[float, float]] = []
    if layout in ("ring", "star"):
        r = min(w, h) * 0.33
        if layout == "star":
            pos.append((cx, cy))
            for i in range(1, n):
                a = -math.pi / 2 + 2 * math.pi * (i - 1) / max(1, n - 1)
                pos.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        else:
            for i in range(n):
                a = -math.pi / 2 + 2 * math.pi * i / n
                pos.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    elif layout in ("chain", "coast"):
        left, right = 110, w - 110
        for i in range(n):
            x = left + (right - left) * i / max(1, n - 1)
            y = cy + (60 * math.sin(i * 1.3) if layout == "coast" else 0)
            pos.append((x, y))
    elif layout == "concentric":
        for i in range(n):
            r = min(w, h) * 0.40 * (1 - i / n)
            a = -math.pi / 2 + i * 2.2
            pos.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    elif layout == "branch":
        for i in range(n):
            x = 110 + (w - 220) * i / max(1, n - 1)
            y = cy + (-90 if i % 2 else 90) * (1 if i % 4 < 2 else -1)
            pos.append((x, y))
    elif layout == "scatter":
        for i in range(n):
            r = min(w, h) * 0.06 * (i + 1)
            a = i * 2.399963  # golden angle; deterministic spiral
            pos.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    else:  # stacks
        cols = max(1, int(math.ceil(math.sqrt(n))))
        for i in range(n):
            pos.append((160 + (i % cols) * (w - 320) / max(1, cols - 1) if cols > 1 else cx,
                        140 + (i // cols) * 120))
    return pos


def render_svg(state: Dict[str, Any]) -> str:
    w, h = 1200, 820
    n = len(state["areas"])
    pos = _positions(state["layout"], n, w, h)
    mk = state["index_snapshot"]["myth_key"]
    ink, paper, red, blue = "#2b2118", "#f1e7cf", "#8b1a1a", "#1d3d5c"
    out = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 {w} {h}' "
           f"font-family='Georgia, serif' fill='{ink}'>",
           f"<rect width='{w}' height='{h}' fill='{paper}'/>",
           f"<rect x='14' y='14' width='{w - 28}' height='{h - 28}' fill='none' stroke='{ink}' stroke-width='2'/>",
           f"<text x='40' y='52' font-size='26' font-weight='bold'>REGNO KAO -- folio: {escape(state['realm'])}</text>",
           f"<text x='40' y='76' font-size='13'>{escape(state['archetype'])} / {escape(state['index_snapshot']['classification'])}"
           f" / attested {escape(', '.join(state['index_snapshot']['attestations']))} / band {state['band']}</text>",
           f"<text x='40' y='96' font-size='13' fill='{blue}'>LAW (INFERRED, {escape(mk['referent'])}): {escape(mk['rule'])}</text>",
           f"<text x='40' y='114' font-size='12'>LAW ROLL {state['law']}: {escape(ARCH[state['archetype']]['law'][state['law']])}</text>"]
    if state["layout"] == "coast":
        out.append(f"<path d='M 0 {h / 2 + 140} Q {w / 4} {h / 2 + 90} {w / 2} {h / 2 + 140} T {w} {h / 2 + 140} L {w} {h} L 0 {h} Z' fill='{blue}' opacity='0.12'/>")
        out.append(f"<text x='{w - 200}' y='{h - 60}' font-size='14' fill='{blue}'>the sea / the far dark</text>")
    styles = {"angle": "stroke-dasharray='8 6'", "intersection": "stroke-width='4'",
              "conjunction": "stroke-dasharray='2 5'", "oblique": "stroke-dasharray='14 4 2 4'",
              "splice": f"stroke='{red}' stroke-width='3'", "recursion": "", "closed": f"stroke='{red}' stroke-dasharray='3 3'"}
    for a, b, t in state["edges"]:
        x1, y1 = pos[a - 1]
        if t == "recursion":
            out.append(f"<path d='M {x1 + 60} {y1 - 10} C {x1 + 120} {y1 - 70}, {x1 + 120} {y1 + 50}, {x1 + 60} {y1 + 10}' fill='none' stroke='{blue}' stroke-width='2'/>")
            out.append(f"<text x='{x1 + 96}' y='{y1 - 40}' font-size='11' fill='{blue}'>recursion</text>")
            continue
        if b == 0:
            out.append(f"<line x1='{x1:.0f}' y1='{y1 + 28:.0f}' x2='{x1:.0f}' y2='{y1 + 70:.0f}' {styles['closed']}/>")
            out.append(f"<text x='{x1 + 6}' y='{y1 + 66}' font-size='11' fill='{red}'>closed spur</text>")
            continue
        x2, y2 = pos[b - 1]
        st = styles.get(t, "")
        stroke = "" if "stroke=" in st else f"stroke='{ink}'"
        width = "" if "stroke-width" in st else "stroke-width='2'"
        out.append(f"<line x1='{x1:.0f}' y1='{y1:.0f}' x2='{x2:.0f}' y2='{y2:.0f}' {stroke} {width} {st}/>")
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        out.append(f"<text x='{mx:.0f}' y='{my - 6:.0f}' font-size='11' text-anchor='middle' fill='{blue}'>{t}</text>")
    for area, (x, y) in zip(state["areas"], pos):
        hz = area["hazard"]
        cz = area["contradiction"]
        stroke = red if hz >= 4 else ink
        out.append(f"<rect x='{x - 62:.0f}' y='{y - 28:.0f}' width='124' height='56' rx='6' fill='{paper}' stroke='{stroke}' stroke-width='{1 + hz / 2:.1f}'/>")
        out.append(f"<text x='{x:.0f}' y='{y - 8:.0f}' font-size='13' font-weight='bold' text-anchor='middle'>A{area['n']}</text>")
        kind = area["kind"] if len(area["kind"]) <= 22 else area["kind"][:21] + "."
        out.append(f"<text x='{x:.0f}' y='{y + 9:.0f}' font-size='11' text-anchor='middle'>{escape(kind)}</text>")
        out.append(f"<text x='{x:.0f}' y='{y + 22:.0f}' font-size='10' text-anchor='middle'>hz {hz}{' / contradiction ' + str(cz) if cz >= 4 else ''}</text>")
        if area.get("intrusion"):
            out.append(f"<text x='{x:.0f}' y='{y + 42:.0f}' font-size='10' text-anchor='middle' fill='{red}'>splice: {escape(area['intrusion'][:28])}</text>")
    out.append(f"<text x='40' y='{h - 60}' font-size='11'>Edges: solid intersection (thick) / dashed angle / dotted conjunction / dash-dot oblique / red splice / loop recursion. "
               f"Box weight = hazard band; red box = hazard 4+.</text>")
    out.append(f"<text x='40' y='{h - 42}' font-size='11'>Labels: facts SOURCE-VERIFIED (index); law INFERRED (myth key); every area, exit and hazard ROLLED. {escape(PREP_NOTE)}</text>")
    out.append(f"<text x='40' y='{h - 24}' font-size='11'>Ledger: {escape(' | '.join(l.strip() for l in state['ledger'][2:8]))} ...</text>")
    out.append("</svg>")
    return "\n".join(out) + "\n"


def render_sheet(state: Dict[str, Any]) -> str:
    snap = state["index_snapshot"]
    mk = snap["myth_key"]
    arch = ARCH[state["archetype"]]
    o = [f"# Regno Kao folio -- {state['realm']}", "",
         f"*{state['archetype']}* -- {snap['classification']}  ",
         f"Attested: {', '.join(snap['attestations'])}  ",
         f"Threat band: {state['band']} (meaning per the siege package mechanical reference; NO COVERAGE here)  ",
         f"Entry: {state['entry'] or '(not stated)'}  ", "",
         f"> {PREP_NOTE}", "",
         "## What the book says (SOURCE-VERIFIED)"]
    for f in snap["facts"]:
        o.append(f"- {f}")
    o += ["", f"## Law of the place (INFERRED -- {mk['referent']})",
          f"*{mk['citation']}*  ", "", mk["rule"], "",
          f"**Law roll {state['law']}:** {arch['law'][state['law']]}", "",
          "## Areas (ROLLED)", "",
          "| # | Kind | Dimensions | Hazard | Contradiction |", "|---|---|---|---|---|"]
    for a in state["areas"]:
        cz = CONTRADICTION[a["contradiction"]]
        o.append(f"| A{a['n']} | {a['kind']} | {a['dimensions']} | {a['hazard']} | {'stable' if cz is None else cz.split(':')[0]} |")
    o.append("")
    exits: Dict[int, List[str]] = {a["n"]: [] for a in state["areas"]}
    for a, b, t in state["edges"]:
        if b == 0:
            exits[a].append("a spur that has closed behind (no exit)")
        elif t == "recursion":
            exits[a].append(f"recursion: this area contains {state['realm']} again")
        else:
            exits[a].append(f"A{b} via {t}")
            exits[b].append(f"A{a} via {t}")
    for a in state["areas"]:
        o += [f"### A{a['n']} -- {a['kind']}", "",
              f"- **Dimensions:** {a['dimensions']}",
              f"- **Hazard band {a['hazard']}:** {arch['hazards'][a['hazard']]}"]
        cz = CONTRADICTION[a["contradiction"]]
        if cz:
            o.append(f"- **Psychotecture:** {cz}")
        if a.get("intrusion"):
            o.append(f"- **Off-folio intrusion:** {a['intrusion']} -- roll its folio separately; its law applies inside the splice.")
        o.append(f"- **Exits:** {'; '.join(exits[a['n']]) if exits[a['n']] else 'none rolled (the way in is the way out, if it is still there)'}")
        o.append("")
    o += ["## Running it (skill rules)", "",
          "- Track the party's EXPECTED location and EXPERIENCED location as two lines; a contradiction seed is where they part.",
          "- Anchors matter: a detail the party fixes on (a sound, a mark, a name) is what a doubled place gets wrong.",
          "- Never resolve psychotecture by fiat; use the module reliability procedures, and roll the exits when reached, not before.",
          "- Denizens, wards and items come from the bestiary, the package and the loot pipeline, never from this sheet.",
          "", "## Dice ledger", "", "```"]
    o += state["ledger"]
    o.append("```")
    return "\n".join(o) + "\n"


def cmd_render(path: str, args) -> None:
    state = load(path)
    svg = render_svg(state)
    sheet = render_sheet(state)
    svg_path = args.svg or path.replace(".realm.state.json", "").replace(".json", "") + ".svg"
    sheet_path = args.sheet or path.replace(".realm.state.json", "").replace(".json", "") + ".area.md"
    Path(svg_path).write_text(svg, encoding="utf-8")
    Path(sheet_path).write_text(sheet, encoding="utf-8")
    print(f"  rendered {svg_path} and {sheet_path} ({len(state['areas'])} areas, {len(state['edges'])} edges)")


def cmd_show(path: str, args) -> None:
    state = load(path)
    print(f"=== {state['realm']} ({state['archetype']}, band {state['band']}) ===")
    print(f"  law roll {state['law']}: {ARCH[state['archetype']]['law'][state['law']]}")
    for a in state["areas"]:
        flag = "" if CONTRADICTION[a["contradiction"]] is None else f"  <- {CONTRADICTION[a['contradiction']].split(':')[0]}"
        print(f"  A{a['n']}: {a['kind']} ({a['dimensions']}) hazard {a['hazard']}{flag}")
    for a, b, t in state["edges"]:
        print(f"  A{a} -> {'closed spur' if b == 0 else 'A' + str(b)} [{t}]")


def cmd_list() -> None:
    index = load_index()
    for r in index["realms"]:
        a = r["attestations"][0]
        tag = r["archetype"] if r.get("mappable") else "condition (not mappable)"
        print(f"  {r['name']:<70} {tag:<28} Vol. {'I' * a['volume']} {a['chapter']}:{a['verse']}")

# ============================================================================
# SELFTEST
# ============================================================================

def selftest() -> int:
    import xml.etree.ElementTree as ET
    fails: List[str] = []

    def check(c: bool, m: str) -> None:
        if not c:
            fails.append(m)

    for name, t in ARCH.items():
        check(set(t["areas"]) == set(range(1, 13)), f"{name}: areas table must be d12")
        check(set(t["hazards"]) == set(range(1, 7)), f"{name}: hazards table must be d6")
        check(set(t["law"]) == set(range(1, 7)), f"{name}: law table must be d6")
    index = load_index()
    check(set(r["archetype"] for r in mappable(index)) <= set(ARCH), "index archetype without a table")
    check(find_realm(index, "long woe")["name"] == "Long Woe", "alias/name lookup")
    check(find_realm(index, "Somnopolis")["name"].startswith("Somnopolis"), "alias lookup")
    try:
        find_realm(index, "the")
        fails.append("ambiguous lookup did not raise")
    except SystemExit:
        pass

    class A:  # argument stub
        pass

    with tempfile.TemporaryDirectory() as td:
        for realm in mappable(index):
            p = os.path.join(td, "t.realm.state.json")
            a = A(); a.realm = realm["name"]; a.areas = "d8"; a.band = 2; a.entry = "test"; a.force = True
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                cmd_new(p, a)
            st = load(p)
            check(2 <= len(st["areas"]) <= 8, f"{realm['name']}: area count")
            check(all(1 <= e[0] <= len(st["areas"]) for e in st["edges"]), f"{realm['name']}: edge index")
            check("d8 =" in buf.getvalue() and "law roll" in buf.getvalue(), f"{realm['name']}: raws not printed")
            svg1, sheet1 = render_svg(st), render_sheet(st)
            svg2, sheet2 = render_svg(st), render_sheet(st)
            check(svg1 == svg2 and sheet1 == sheet2, f"{realm['name']}: render not deterministic")
            try:
                ET.fromstring(svg1)
            except ET.ParseError as e:
                fails.append(f"{realm['name']}: SVG not well-formed: {e}")
            check(f"A{len(st['areas'])} --" in sheet1 and "SOURCE-VERIFIED" in sheet1 and "INFERRED" in sheet1 and "ROLLED" in sheet1,
                  f"{realm['name']}: sheet labels")
            sl = SLOTS.get(realm["archetype"])
            if sl:
                check(len(st["areas"]) >= sl["min"], f"{realm['name']}: below slot minimum")
                check(st["areas"][0]["face"] in sl["first"], f"{realm['name']}: first slot not honoured")
                if sl["last"]:
                    check(st["areas"][-1]["face"] in sl["last"], f"{realm['name']}: last slot not honoured")
                if sl["middle"]:
                    check(any(ar["face"] in sl["middle"] for ar in st["areas"][1:-1]), f"{realm['name']}: middle slot not honoured")
            for ar in st["areas"]:
                if ar["contradiction"] == 8:
                    check(ar.get("intrusion") and ar["intrusion"] != realm["name"], f"{realm['name']}: intrusion missing/self")
        # conditions refuse
        cond = next(r for r in index["realms"] if not r.get("mappable"))
        a = A(); a.realm = cond["name"]; a.areas = "d8"; a.band = 0; a.entry = ""; a.force = True
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                cmd_new(os.path.join(td, "c.realm.state.json"), a)
            fails.append("condition was mapped")
        except SystemExit as e:
            check(e.code == 2, "condition refusal must exit 2")
        # render command writes files
        a = A(); a.svg = None; a.sheet = None
        with contextlib.redirect_stdout(io.StringIO()):
            cmd_render(p, a)
        check(os.path.exists(os.path.join(td, "t.svg")) and os.path.exists(os.path.join(td, "t.area.md")), "render outputs missing")
    for f in fails:
        print("FAIL:", f)
    print(f"SELFTEST {'OK' if not fails else 'FAILED'}: {len(mappable(index))} mappable realms rolled and rendered, {len(fails)} failures")
    return 1 if fails else 0


def main() -> None:
    global FOUR_THROW
    p = argparse.ArgumentParser(description="Regno Kao folio roller -- area maps for TEATD warp realms")
    p.add_argument("state", nargs="?", help="NAME.realm.state.json (throwaway; gitignored)")
    sub = p.add_subparsers(dest="cmd")
    n = sub.add_parser("new")
    n.add_argument("--realm", required=True)
    n.add_argument("--areas", default="d8")
    n.add_argument("--band", type=int, default=2)
    n.add_argument("--entry", default="")
    n.add_argument("--force", action="store_true")
    r = sub.add_parser("render")
    r.add_argument("--svg")
    r.add_argument("--sheet")
    sub.add_parser("show")
    p.add_argument("--list", action="store_true")
    p.add_argument("--four-throw", action="store_true")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()
    FOUR_THROW = bool(args.four_throw)
    if args.selftest:
        sys.exit(selftest())
    if args.list:
        cmd_list()
        return
    if not args.state or not args.cmd:
        p.error("state path and a command (new/render/show) are required")
    {"new": cmd_new, "render": cmd_render, "show": cmd_show}[args.cmd](args.state, args)


if __name__ == "__main__":
    main()
