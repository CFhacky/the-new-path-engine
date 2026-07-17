#!/usr/bin/env python3
"""
pc_add.py — put a character-file PC into a combat registry in one command
The New Path campaign engine (the-new-path-engine)

Bridges character_state.py's persistent sheet (*.character.json) into
combat_registry.py's session state (*.registry.json) so the PC's hp,
max hp, and initiative modifier are pulled from the sheet — including
active buff deltas (a hasted, cat's-graced PC enters combat with the
right numbers, not the flat-footed sheet).

No imports across scripts (repo contract): this shells combat_registry.py
sitting in the same directory.

USAGE
    python3 pc_add.py arik.character.json vault_fight.registry.json
    python3 pc_add.py arik.character.json fight.registry.json --init-misc 4
"""

import argparse
import json
import os
import subprocess
import sys

STACK_ALWAYS = {"dodge", "circumstance", "unnamed", "untyped"}


def dex_effect_total(st: dict) -> int:
    by_type = {}
    for eff in st.get("effects", []):
        d = eff["deltas"].get("dex")
        if d:
            by_type.setdefault(d[0], []).append(d[1])
    total = 0
    for btype, vals in by_type.items():
        pos = [v for v in vals if v > 0]
        neg = [v for v in vals if v < 0]
        if btype in STACK_ALWAYS:
            total += sum(pos)
        elif pos:
            total += max(pos)
        total += sum(neg)          # penalties always stack
    return total


def main() -> int:
    ap = argparse.ArgumentParser(description="Add the PC from a character "
                                             "file to a combat registry.")
    ap.add_argument("character", help="*.character.json")
    ap.add_argument("registry", help="*.registry.json")
    ap.add_argument("--init-misc", type=int, default=0,
                    help="Improved Initiative, familiar, etc.")
    args = ap.parse_args()

    with open(args.character, encoding="utf-8") as f:
        st = json.load(f)
    b = st["base"]
    dex = b["dex"] + dex_effect_total(st)
    init_mod = (dex - 10) // 2 + args.init_misc
    hp = b.get("hp_cur", b["hp_max"])

    here = os.path.dirname(os.path.abspath(__file__))
    reg = os.path.join(here, "combat_registry.py")
    if not os.path.exists(reg):
        print(f"combat_registry.py not found beside this script ({here}).",
              file=sys.stderr)
        return 2

    cmd = [sys.executable, reg, args.registry, "add", st["name"],
           "--hp", str(hp), "--max-hp", str(b["hp_max"]),
           "--init-mod", str(init_mod)]
    print(f"{st['name']}: hp {hp}/{b['hp_max']}, init "
          f"{init_mod:+d} (Dex {dex}"
          + (f", misc {args.init_misc:+d}" if args.init_misc else "") + ")")
    print("> " + " ".join(cmd[1:]))
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main())
