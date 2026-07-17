#!/usr/bin/env python3
"""
deferred_dice.py -- local roller for Deferred Dice & World-Move cash-ins
The New Path campaign engine (the-new-path-engine)

Executes a deferred-die spec (what's rolling, die expression, band mapping
if the entry carries one) with the standard raw-first discipline and emits
a paste-ready provenance block for the user to file into the Notion
registers. This script does NOT read or write Notion.

GOVERNING SOURCES (read 2026-07-17):
    THE WORLD-MOVE LAW -- boot page 390e8214-84b0-819c-9577-d8103a27467e:
        trigger states; DESCRIBE/HINT/MOVE/BILL; close-sweep rule ("any
        uncashed trigger state gets its move ROLLED AT CLOSE"); Register
        entry format (trigger state, raw dice, FULL band table with unhit
        bands marked DEAD, interpretive shadings CHOSEN vs DEAD, binding
        interpretation, links out, seeded-to status); standing texture dice
        (dawn weather d8 per Hell-cycle open, dilation bill d20 per session).
    Deferred Dice database -- data source da0db9c0-9fb7-4ddf-aff5-f1ac55979873
        (DB bd61ff97-0030-4967-8b79-cafb09220fdc). Schema fields mirrored in
        the provenance block: Subject (title), Roll Type, Result, Status
        (Waiting/Rolled/Resolved), Session Resolved, Related NPC,
        Related Event, Trigger Condition.
    World-Move Register -- DB 4ec10078-f1d0-467f-abf5-6542803658f0,
        data source f10ce74a-dcdd-4c4d-9034-5a7a3cd9b52b (cashin target).
    Standing Law G2: python secrets, raw stdout BEFORE outcomes, four
        throws per roll bound mode-else-median (tie rule as in
        session_open.py: unique mode, else median of four = mean of middle
        two, fractional rounds down -- implementation ruling flagged).

COVERAGE NOTE: the World-Move Law names NO fixed die or table for choosing
or resolving a cash-in move -- the S074 close sweep used per-move d20s
chosen by the instance against entity-page tables. Accordingly `cashin`
requires --move (the instance's choice among DESCRIBE/HINT/MOVE/BILL) and
--dice, and takes the band table from --bands. If a governing entity page
carries no band table, leave --bands off; the block records the raw die for
interpretation on the page. Nothing here invents bands.

USAGE
    python deferred_dice.py roll --subject "Feather in the Strongbox" \
        --dice 1d20 --bands "1-8:dormant;9-16:stirs;17-20:fires" \
        --npc "Empyrean" --trigger "first Minauros lawful-order vector"
    python deferred_dice.py cashin --trigger "Dispater attention HIGH" \
        --move MOVE --dice 1d20 --bands "..." --seed "next boot"
    python deferred_dice.py weather          (dawn weather d8, per Law)
    python deferred_dice.py dilation         (dilation bill d20, per Law)
    python deferred_dice.py --selftest
"""

import argparse
import datetime
import re
import secrets
import sys
from typing import Dict, List, Optional, Tuple

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ============================================================================
# DICE -- four throws of the full expression, mode-else-median bind,
# raw shown first (Standing Law G2). --single-throw drops to one throw.
# ============================================================================

SINGLE_THROW = False

DICE_RE = re.compile(
    r"^\s*(\d*)d(\d+)\s*(?:(x|\*)\s*(\d+))?\s*(?:([+-])\s*(\d+))?\s*$",
    re.IGNORECASE)


def parse_expr(expr: str) -> Tuple[int, int, int, int]:
    """'NdS[xK][+/-M]' -> (n, sides, mult, mod). Examples: 1d20, 3d6,
    2d6x10, 1d20+3, d8."""
    m = DICE_RE.match(expr)
    if not m:
        raise SystemExit(f"Bad dice expression {expr!r} -- use NdS, NdSxK, "
                         f"or NdS+M (e.g. 1d20, 2d6x10, 1d20+3).")
    n = int(m.group(1)) if m.group(1) else 1
    sides = int(m.group(2))
    mult = int(m.group(4)) if m.group(4) else 1
    mod = int(m.group(6)) if m.group(6) else 0
    if m.group(5) == "-":
        mod = -mod
    if n < 1 or sides < 2 or n > 100:
        raise SystemExit(f"Unreasonable dice expression {expr!r}.")
    return n, sides, mult, mod


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


def execute(expr: str) -> Dict:
    """Roll the expression under the four-throw discipline. Returns the
    full provenance: all raw throw sets, bound base, final total."""
    n, sides, mult, mod = parse_expr(expr)

    def one_throw() -> Tuple[List[int], int]:
        dice = [secrets.randbelow(sides) + 1 for _ in range(n)]
        return dice, sum(dice)

    if SINGLE_THROW:
        throws = [one_throw()]
        bound, how = throws[0][1], "single"
    else:
        throws = [one_throw() for _ in range(4)]
        bound, how = bind_four([t for _, t in throws])
    total = bound * mult + mod
    return {"expr": expr, "n": n, "sides": sides, "mult": mult, "mod": mod,
            "throws": throws, "bound": bound, "how": how, "total": total}


def raw_lines(res: Dict) -> List[str]:
    lines = []
    for i, (dice, tot) in enumerate(res["throws"], 1):
        d = f"{res['n']}d{res['sides']}"
        detail = f" {dice}" if res["n"] > 1 else ""
        lines.append(f"  throw {i}: {d} = {tot}{detail}")
    post = ""
    if res["mult"] != 1:
        post += f" x{res['mult']}"
    if res["mod"]:
        post += f" {res['mod']:+d}"
    lines.append(f"  BIND: {res['bound']} ({res['how']}){post}"
                 f" -> TOTAL {res['total']}")
    return lines

# ============================================================================
# BAND MAPPING -- "1-3:Setback;4-10:Routine;20+:Windfall". The Register
# format requires the FULL band table printed with unhit bands marked DEAD.
# ============================================================================

BAND_RE = re.compile(r"^\s*(\d+)\s*(?:-\s*(\d+)|\+)?\s*$")


def parse_bands(spec: str) -> List[Tuple[int, int, str]]:
    bands = []
    for part in spec.split(";"):
        part = part.strip()
        if not part:
            continue
        if ":" not in part:
            raise SystemExit(f"Bad band {part!r} -- use LO-HI:text or N+:text.")
        rng, text = part.split(":", 1)
        m = BAND_RE.match(rng)
        if not m:
            raise SystemExit(f"Bad band range {rng!r}.")
        lo = int(m.group(1))
        hi = int(m.group(2)) if m.group(2) else (999 if "+" in rng else lo)
        bands.append((lo, hi, text.strip()))
    return bands


def band_table_lines(bands, value: int) -> List[str]:
    lines = []
    hit_any = False
    for lo, hi, text in bands:
        hit = lo <= value <= hi
        hit_any = hit_any or hit
        tag = "<< HIT" if hit else "DEAD"
        rng = f"{lo}+" if hi >= 999 else (f"{lo}" if lo == hi else f"{lo}-{hi}")
        lines.append(f"    {rng:>6}: {text}   [{tag}]")
    if not hit_any:
        lines.append(f"    (value {value} lands OFF-TABLE -- check the band "
                     f"spec against the source page)")
    return lines

# ============================================================================
# PROVENANCE BLOCKS
# ============================================================================

DD_SOURCE = "da0db9c0-9fb7-4ddf-aff5-f1ac55979873"
WMR_DB = "4ec10078-f1d0-467f-abf5-6542803658f0"
WMR_SOURCE = "f10ce74a-dcdd-4c4d-9034-5a7a3cd9b52b"
LAW_PAGE = "390e8214-84b0-819c-9577-d8103a27467e"

MOVES = ("DESCRIBE", "HINT", "MOVE", "BILL")
MOVE_GLOSS = {
    "DESCRIBE": "it intrudes on the senses",
    "HINT": "an NPC notices or reacts unprompted",
    "MOVE": "the off-screen actor acts, rolled openly",
    "BILL": "a cost lands on someone with a name",
}


def block_roll(args) -> str:
    res = execute(args.dice)
    today = datetime.date.today().isoformat()
    bands = parse_bands(args.bands) if args.bands else None
    lines = []
    lines.append("=" * 62)
    lines.append("DEFERRED DIE -- PROVENANCE BLOCK (paste into Deferred Dice")
    lines.append(f"register, data source {DD_SOURCE})")
    lines.append("=" * 62)
    lines.append(f"Date rolled (ISO):  {today}")
    lines.append(f"Subject:            {args.subject}")
    lines.append(f"Roll Type (spec):   {args.dice}"
                 + (f" vs bands [{args.bands}]" if args.bands else
                    " (no band mapping supplied -- interpret on the "
                    "governing page)"))
    if args.trigger:
        lines.append(f"Trigger Condition:  {args.trigger}")
    if args.npc:
        lines.append(f"Related NPC:        {args.npc}")
    if args.event:
        lines.append(f"Related Event:      {args.event}")
    lines.append("Raw throws (secrets; shown before any outcome):")
    lines.extend(raw_lines(res))
    if bands:
        lines.append("Band table (unhit bands marked DEAD, per Register format):")
        lines.extend(band_table_lines(bands, res["total"]))
        hit = [t for lo, hi, t in bands if lo <= res["total"] <= hi]
        result_text = hit[0] if hit else "OFF-TABLE"
        lines.append(f"BOUND RESULT:       {res['total']} -> {result_text}")
        lines.append(f"Result (register):  \"{args.dice}={res['total']} "
                     f"({today}): {result_text}\"")
    else:
        lines.append(f"BOUND RESULT:       {res['total']}")
        lines.append(f"Result (register):  \"{args.dice}={res['total']} "
                     f"({today}): <binding interpretation from the "
                     f"governing page>\"")
    lines.append("Status:             Rolled  (flip to Resolved when the "
                 "outcome lands in play)")
    lines.append("Session Resolved:   <fill at session close>")
    return "\n".join(lines)


def block_cashin(args) -> str:
    move = args.move.upper()
    if move not in MOVES:
        raise SystemExit(f"--move must be one of {MOVES} (World-Move Law, "
                         f"boot page {LAW_PAGE}).")
    res = execute(args.dice)
    today = datetime.date.today().isoformat()
    bands = parse_bands(args.bands) if args.bands else None
    lines = []
    lines.append("=" * 62)
    lines.append("WORLD-MOVE CASH-IN -- REGISTER ENTRY BLOCK (paste into the")
    lines.append(f"World-Move Register, DB {WMR_DB},")
    lines.append(f"data source {WMR_SOURCE})")
    lines.append("=" * 62)
    lines.append(f"Date (ISO):          {today}")
    lines.append(f"Trigger state:       {args.trigger}")
    lines.append(f"Move type:           {move} -- {MOVE_GLOSS[move]}")
    lines.append("  (moves considered CHOSEN vs DEAD -- record the "
                 "shadings you weighed:)")
    for m in MOVES:
        lines.append(f"    {m}: {'CHOSEN' if m == move else 'DEAD -- <one-line why not, revivable only by Chad>'}")
    lines.append(f"Dice spec:           {args.dice}"
                 + (f" vs bands [{args.bands}]" if args.bands else
                    " (no page band table supplied -- NO COVERAGE: the Law "
                    "names no fixed cash-in table; interpret on the "
                    "governing entity page)"))
    lines.append("Raw dice (secrets; shown before any outcome):")
    lines.extend(raw_lines(res))
    if bands:
        lines.append("FULL band table rolled against (unhit bands DEAD):")
        lines.extend(band_table_lines(bands, res["total"]))
        hit = [t for lo, hi, t in bands if lo <= res["total"] <= hi]
        lines.append(f"BOUND RESULT:        {res['total']} -> "
                     f"{hit[0] if hit else 'OFF-TABLE'}")
    else:
        lines.append(f"BOUND RESULT:        {res['total']}")
    lines.append("Binding interpretation: <write it; links OUT to affected "
                 "entity pages, never restating them>")
    lines.append(f"Seeded-to status:    {args.seed or '<in-session cash / next-boot seed -- state which>'}")
    lines.append("(Law: no threshold state survives a close uncashed; read "
                 "the last 1-2 Register pages at every boot.)")
    return "\n".join(lines)


def block_texture(kind: str) -> str:
    """Standing texture dice named by the Law: dawn weather d8 per
    Hell-cycle open; dilation bill d20 per session. Both always Register-
    logged."""
    expr = "1d8" if kind == "weather" else "1d20"
    label = ("DAWN WEATHER (d8, per Hell-cycle scene-open -- rotate the "
             "sensorium; Avernus has weather)" if kind == "weather" else
             "DILATION BILL (d20, once per session -- the 27:1 gradient "
             "costs a named person something)")
    res = execute(expr)
    today = datetime.date.today().isoformat()
    lines = []
    lines.append("=" * 62)
    lines.append(f"STANDING TEXTURE DIE -- {label}")
    lines.append(f"(World-Move Law, boot page {LAW_PAGE}; runs under the Law,")
    lines.append(f"logged to the Register {WMR_DB})")
    lines.append("=" * 62)
    lines.append(f"Date (ISO): {today}")
    lines.append("Raw throws:")
    lines.extend(raw_lines(res))
    lines.append(f"BOUND RESULT: {res['total']} -- interpret in-scene; no "
                 f"fixed band table on the page (the die rotates texture, "
                 f"the instance narrates).")
    return "\n".join(lines)

# ============================================================================
# SELFTEST
# ============================================================================

class _Args:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def selftest() -> int:
    global SINGLE_THROW
    ok = True

    def expect(label, cond):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
        ok = ok and cond

    print("### deferred_dice.py SELFTEST ###\n")
    print("-- expression parser --")
    expect("1d20 -> (1,20,1,0)", parse_expr("1d20") == (1, 20, 1, 0))
    expect("d8 -> (1,8,1,0)", parse_expr("d8") == (1, 8, 1, 0))
    expect("2d6x10 -> (2,6,10,0)", parse_expr("2d6x10") == (2, 6, 10, 0))
    expect("3d6+2 -> (3,6,1,2)", parse_expr("3d6+2") == (3, 6, 1, 2))
    expect("1d20-4 -> (1,20,1,-4)", parse_expr("1d20-4") == (1, 20, 1, -4))
    try:
        parse_expr("banana")
        expect("garbage expression rejected", False)
    except SystemExit:
        expect("garbage expression rejected", True)

    print("\n-- band parser + DEAD marking --")
    bands = parse_bands("1-3:Setback;4-10:Routine;11-16:Productive;"
                        "17-19:Breakthrough;20+:Windfall")
    expect("five bands parsed", len(bands) == 5)
    expect("open band 20+ maps to 999", bands[4][1] >= 999)
    tbl = band_table_lines(bands, 17)
    expect("hit band marked << HIT", any("Breakthrough" in l and "HIT" in l
                                          for l in tbl))
    expect("unhit bands marked DEAD",
           sum(1 for l in tbl if "[DEAD]" in l) == 4)
    tbl2 = band_table_lines(parse_bands("1-3:x;4-10:y"), 15)
    expect("off-table value flagged", any("OFF-TABLE" in l for l in tbl2))

    print("\n-- binder (same rule as session_open.py) --")
    expect("mode: [7,7,3,19] -> 7", bind_four([7, 7, 3, 19]) == (7, "mode"))
    expect("median: [2,5,9,16] -> 7", bind_four([2, 5, 9, 16]) == (7, "median"))
    expect("two-pair -> median: [5,5,9,9] -> 7",
           bind_four([5, 5, 9, 9]) == (7, "median"))

    print("\n-- execution sanity --")
    res = execute("2d6x10")
    expect("2d6x10 total in 20..120 and = bound x10",
           20 <= res["total"] <= 120 and res["total"] == res["bound"] * 10)
    expect("four throw sets recorded", len(res["throws"]) == 4)
    vals = [execute("1d20")["total"] for _ in range(20)]
    expect("20 bound d20s in 1..20", all(1 <= v <= 20 for v in vals))
    expect("not all identical (no-repeat sanity)", len(set(vals)) > 1)

    print("\n-- worked provenance blocks (visual check) --\n")
    print(block_roll(_Args(subject="Selftest -- Feather in the Strongbox",
                           dice="1d20",
                           bands="1-8:dormant;9-16:stirs;17-20:fires",
                           trigger="first Minauros lawful-order vector",
                           npc="Empyrean", event="Minauros Debt")))
    print()
    print(block_cashin(_Args(trigger="Selftest -- Dispater attention HIGH",
                             move="MOVE", dice="1d20", bands=None,
                             seed="next boot")))
    print()
    print(block_texture("weather"))

    print(f"\nSELFTEST {'PASSED' if ok else 'FAILED'}.")
    return 0 if ok else 1

# ============================================================================
# CLI
# ============================================================================

def main():
    global SINGLE_THROW
    p = argparse.ArgumentParser(
        description="Local roller for Deferred Dice entries and World-Move "
                    "Law cash-ins. Emits paste-ready provenance blocks; "
                    "never reads or writes Notion.")
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--four-throw", action="store_true",
                   help="Four-throw mode-else-median bind for RULING-type "
                        "entries wanting stability. Default is single raw "
                        "dice — play events keep their outliers "
                        "(Chad ruling, 17 Jul 2026).")
    p.add_argument("--single-throw", action="store_true",
                   help="(default) Kept for compatibility; single raw dice.")
    sub = p.add_subparsers(dest="command")

    sp = sub.add_parser("roll", help="Execute a deferred-die spec.")
    sp.add_argument("--subject", required=True,
                    help="Deferred Dice 'Subject' (title field).")
    sp.add_argument("--dice", required=True,
                    help="Die expression from the entry's Roll Type: NdS, "
                         "NdSxK, NdS+M (e.g. 1d20, 2d6x10, 3d6+2).")
    sp.add_argument("--bands", default=None,
                    help="Band mapping IF the entry carries one, e.g. "
                         "\"1-3:Setback;4-10:Routine;20+:Windfall\".")
    sp.add_argument("--trigger", default=None, help="Trigger Condition text.")
    sp.add_argument("--npc", default=None, help="Related NPC.")
    sp.add_argument("--event", default=None, help="Related (Shadow) Event.")

    sp = sub.add_parser("cashin", help="World-Move Law cash-in (in-session "
                                       "or close sweep).")
    sp.add_argument("--trigger", required=True,
                    help="The trigger state being cashed (Law list: "
                         "attention HIGH / reaction <=7 or >=16 / margin "
                         "<=3 / clock 8+ / watcher logged / unfelt cost).")
    sp.add_argument("--move", required=True,
                    help="DESCRIBE | HINT | MOVE | BILL (instance's choice; "
                         "the Law fixes the menu, not the die).")
    sp.add_argument("--dice", required=True,
                    help="Resolution die per the governing entity page.")
    sp.add_argument("--bands", default=None,
                    help="The page's band table, if it carries one.")
    sp.add_argument("--seed", default=None,
                    help="Seeded-to status (e.g. 'in-session', 'next boot').")

    sub.add_parser("weather", help="Dawn weather d8 (standing texture die).")
    sub.add_parser("dilation", help="Dilation bill d20 (standing texture die).")

    args = p.parse_args()
    if args.selftest:
        sys.exit(selftest())
    # Chad ruling 17 Jul 2026 ("it depends"): deferred entries are usually
    # PLAY events — single raw dice default, outliers stay possible.
    # --four-throw for ruling-stability entries.
    SINGLE_THROW = not args.four_throw
    if not args.command:
        p.print_help()
        sys.exit(1)
    if args.command == "roll":
        print(block_roll(args))
    elif args.command == "cashin":
        print(block_cashin(args))
    elif args.command == "weather":
        print(block_texture("weather"))
    elif args.command == "dilation":
        print(block_texture("dilation"))


if __name__ == "__main__":
    main()
