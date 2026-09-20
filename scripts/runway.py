#!/usr/bin/env python3
"""
runway.py -- schedule queries over the campaign's lane-stamped event spine

Answers the three questions the campaign kept having to answer by hand:

    what fires between here and there?   (runway)
    what is stamped at this date?        (at)
    where is each lane standing?         (lanes)

plus an integrity gate (audit) that catches unparseable stamps, lane/stamp
disagreement, and stamps whose stated wording does not match what they were
keyed to -- the class of bug that put Hammer 1496 numbers inside a Day 7
Hammer 1495 table.

GOVERNING SOURCES
    Date arithmetic: harptos.py (sibling module). This script owns no
    calendar rules.
    Event data: data/canonical/events.csv in the baen-economy-engine repo,
    lane-stamped per the Reserved Interval ruling of 2026-09-19.

AUTHORITY
    Layer 5, resolver script. Reads canonical tables, writes nothing, and
    invents no dates. An unparseable row is reported, never guessed at.

USAGE
    python runway.py lanes
    python runway.py runway ARIK:1495.Hammer.07 ARIK:1496.Tarsakh.18
    python runway.py at ARIK:1495.Hammer.07 --window 60
    python runway.py audit
    python runway.py runway --interval        # the Reserved Interval
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harptos  # noqa: E402

DEFAULT_DIRS = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "..", "..", "baen-economy-engine", "data", "canonical"),
    os.path.expanduser("~/baen-economy-engine/data/canonical"),
]

_STATUS_MARK = {
    "ANCHOR": "==", "LOCKED": "!!", "OVERDUE": "!!", "AT_RISK": "!!",
    "NEEDS_USER": "??", "HELD": "..", "HELD_EMPTY": "..", "SCHEDULED": "..",
    "ARMED": "!!", "FIRED": "ok", "ACTIVE": "ok", "POST_CROSSING": "->",
}


def find_canonical(explicit=None) -> str:
    for d in ([explicit] if explicit else []) + DEFAULT_DIRS:
        if d and os.path.isdir(d) and os.path.exists(os.path.join(d, "events.csv")):
            return os.path.abspath(d)
    raise SystemExit("could not locate data/canonical with events.csv; pass --canonical")


def load(canonical: str):
    rows, bad = [], []
    with open(os.path.join(canonical, "events.csv")) as fh:
        for r in csv.DictReader(fh):
            try:
                r["_date"] = harptos.parse(r["stamp"])
            except harptos.HarptosError as e:
                bad.append((r.get("event_id", "?"), r.get("stamp", ""), str(e)))
                continue
            rows.append(r)
    return rows, bad


def _line(r, ref=None) -> str:
    d = r["_date"]
    mark = _STATUS_MARK.get(r["status"], "  ")
    off = ""
    if ref is not None:
        n = harptos.delta(ref, d)
        off = f"{n:+5d}d"
    prec = "" if r["precision"] == "EXACT" else f"  ~{r['precision'].lower()}"
    amt = f"  {int(r['amount_gp']):,}".replace(",", ",") if r["amount_gp"] else ""
    return (f"  {mark} {off:>7}  {d.long():<22} {r['display_name']}"
            f"{amt}{prec}")


def cmd_lanes(rows, _ns):
    lanes = {}
    for r in rows:
        lanes.setdefault(r["lane"], []).append(r)
    print("LANE POSITIONS\n")
    for lane in sorted(lanes):
        anchors = [r for r in lanes[lane] if r["status"] == "ANCHOR"]
        pos = anchors[0] if anchors else None
        head = pos["_date"].long() if pos else "no anchor row"
        print(f"  {lane:<8} {head:<24} {len(lanes[lane])} events")
        if pos:
            print(f"           {pos['display_name']}")
    print("\n  Lanes never share a clock. runway/at refuse to cross them.")
    return 0


def cmd_runway(rows, ns):
    if ns.interval:
        a, b = "ARIK:1495.Hammer.07", "ARIK:1496.Hammer.01"
        title = "THE RESERVED INTERVAL  (SUSPENDED — nothing below advances by elapsed time)"
    else:
        a, b, title = ns.start, ns.end, "RUNWAY"
    A, B = harptos.parse(a), harptos.parse(b)
    if A.lane != B.lane:
        raise SystemExit(f"cross-lane runway refused: {A.lane} vs {B.lane}")
    span = harptos.delta(A, B)
    inside = sorted(
        (r for r in rows
         if r["lane"] == A.lane and A.absolute() <= r["_date"].absolute() <= B.absolute()),
        key=lambda r: r["_date"].absolute())
    print(f"{title}\n")
    print(f"  {A.long()}  ->  {B.long()}")
    print(f"  {span} days ({span/365:.2f} years), {len(inside)} events on lane {A.lane}\n")
    for r in inside:
        print(_line(r, A))
    flagged = [r for r in inside if r["precision"] not in ("EXACT",)]
    if flagged:
        print(f"\n  {len(flagged)} of these are not exact dates "
              f"(month-only, approximate, or flagged ambiguous).")
    return 0


def cmd_at(rows, ns):
    D = harptos.parse(ns.date)
    w = ns.window
    near = sorted(
        (r for r in rows
         if r["lane"] == D.lane and abs(r["_date"].absolute() - D.absolute()) <= w),
        key=lambda r: r["_date"].absolute())
    print(f"AT {D.long()}  (lane {D.lane}, +/-{w} days)\n")
    for r in near:
        print(_line(r, D))
    if not near:
        print("  nothing stamped within the window")
    return 0


def cmd_audit(rows, ns, bad=()):
    problems = []
    for eid, stamp, err in bad:
        problems.append(("UNPARSEABLE", eid, f"{stamp!r}: {err}"))
    for r in rows:
        d, stated = r["_date"], (r["stated_as"] or "")
        if r["lane"] != d.lane:
            problems.append(("LANE_MISMATCH", r["event_id"],
                             f"row lane {r['lane']} vs stamp lane {d.lane}"))
        # A day-number wording ("Day 904", "~D917") carries no year by
        # construction; only check the year when one was actually written.
        if stated and re.search(r"\b1[0-9]{3}\b", stated) \
                and str(d.year) not in stated:
            problems.append(("YEAR_DISAGREES", r["event_id"],
                             f"stamped {d.year}, stated as {stated!r}"))
        if r["precision"] == "AMBIGUOUS":
            problems.append(("AMBIGUOUS_READING", r["event_id"], stated))
        if r["status"] == "NEEDS_USER":
            problems.append(("UNPINNED", r["event_id"], stated))
    print("SPINE AUDIT\n")
    if not problems:
        print("  clean — every stamp parses, every lane agrees, nothing unpinned")
        return 0
    kind_w = max(len(k) for k, _, _ in problems)
    for kind, eid, detail in problems:
        print(f"  {kind:<{kind_w}}  {eid:<22} {detail}")
    print(f"\n  {len(problems)} flagged. UNPINNED and AMBIGUOUS_READING need a ruling; "
          f"the rest need a fix.")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[1],
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--canonical", help="path to data/canonical")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("lanes", help="where each lane is standing")

    r = sub.add_parser("runway", help="what fires between two dates on one lane")
    r.add_argument("start", nargs="?"); r.add_argument("end", nargs="?")
    r.add_argument("--interval", action="store_true",
                   help="use the Reserved Interval (Shelf -> Crossing)")

    a = sub.add_parser("at", help="what is stamped at or near a date")
    a.add_argument("date"); a.add_argument("--window", type=int, default=30)

    sub.add_parser("audit", help="integrity gate over the spine")

    ns = p.parse_args(argv)
    canonical = find_canonical(ns.canonical)
    rows, bad = load(canonical)

    if ns.cmd == "lanes":
        return cmd_lanes(rows, ns)
    if ns.cmd == "runway":
        if not ns.interval and not (ns.start and ns.end):
            raise SystemExit("give two dates, or --interval")
        return cmd_runway(rows, ns)
    if ns.cmd == "at":
        return cmd_at(rows, ns)
    if ns.cmd == "audit":
        return cmd_audit(rows, ns, bad)
    return 1


if __name__ == "__main__":
    sys.exit(main())
