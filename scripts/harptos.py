#!/usr/bin/env python3
"""
harptos.py -- Calendar of Harptos arithmetic for The New Path campaign engine

The engine had seventy scripts and none of them knew what a date was. This is
the missing primitive: it converts between Harptos dates, campaign day-numbers,
and Gregorian-equivalent months, and it does date arithmetic. Nothing else.

GOVERNING SOURCES
    Calendar of Harptos -- Forgotten Realms published structure. Twelve months
    of exactly 30 days, five interstitial festival days that belong to no
    month, and Shieldmeet after Midsummer in years divisible by four. Setting
    RAW, not campaign canon.

    Campaign day-number epoch -- NOT OWNED HERE. The anchor of record is the
    Shi'van lane's Day 904 = 30 Tarsakh 1494 DR, from the S073 day-sync
    (Session-End Protocol v3). This module derives Day 1 from that anchor and
    reports it as DERIVED. Notion and the canonical tables own the anchor.

AUTHORITY
    Layer 5, resolver script. Owns deterministic calendar arithmetic and
    nothing else. It does not know what happened on any date, only how dates
    relate to one another. It invents no canon and reads no state.

LANE STAMPS AND TWO NOTATIONS
    Stamps carry a lane tag so two clocks can never be summed by accident:

        ARIK_SURFACE:1495.Hammer.07     SHIVAN:D911     JORMUN:1498.Uktar.01

    A lane counts in ONE of two notations and must say which:

        CALENDAR  a real Harptos date          1495.Hammer.07
        ELAPSED   days since a named epoch     T+35, HELL+35

    ELAPSED stamps are NOT calendar dates and this module will not pretend
    otherwise. An Elapsed converts to a Date only when an epoch mapping is
    supplied; without one it stays a count and says so. This is deliberate:
    writing "Day 35 Hammer 1495" for the 35th day of an operation is what
    put Hammer-1496 figures inside a Day-7 Hammer-1495 table.

    Comparing or subtracting across lanes, or across notations, raises.

USAGE
    python harptos.py convert "ARIK:1495.Hammer.07"
    python harptos.py convert "SHIVAN:D911"
    python harptos.py delta "SHIVAN:D904" "SHIVAN:1494.Mirtul.06"
    python harptos.py add "ARIK:1495.Hammer.07" 28
    python harptos.py year 1496
    python harptos.py selftest
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass

# ---------------------------------------------------------------- structure

MONTH = "month"
FESTIVAL = "festival"

# In calendar order. Shieldmeet is length 1 only in leap years.
_SEQUENCE = [
    ("Hammer", MONTH, "Deepwinter", "January"),
    ("Midwinter", FESTIVAL, "", ""),
    ("Alturiak", MONTH, "The Claw of Winter", "February"),
    ("Ches", MONTH, "The Claw of Sunsets", "March"),
    ("Tarsakh", MONTH, "The Claw of Storms", "April"),
    ("Greengrass", FESTIVAL, "", ""),
    ("Mirtul", MONTH, "The Melting", "May"),
    ("Kythorn", MONTH, "The Time of Flowers", "June"),
    ("Flamerule", MONTH, "Summertide", "July"),
    ("Midsummer", FESTIVAL, "", ""),
    ("Shieldmeet", FESTIVAL, "", ""),          # leap years only
    ("Eleasis", MONTH, "Highsun", "August"),
    ("Eleint", MONTH, "The Fading", "September"),
    ("Highharvestide", FESTIVAL, "", ""),
    ("Marpenoth", MONTH, "Leaffall", "October"),
    ("Uktar", MONTH, "The Rotting", "November"),
    ("Feast of the Moon", FESTIVAL, "", ""),
    ("Nightal", MONTH, "The Drawing Down", "December"),
]

MONTHS = [n for n, k, _, _ in _SEQUENCE if k == MONTH]
FESTIVALS = [n for n, k, _, _ in _SEQUENCE if k == FESTIVAL]
_ALIAS = {n.lower().replace(" ", ""): n for n, _, _, _ in _SEQUENCE}
_COMMON = {n.lower(): c for n, k, c, _ in _SEQUENCE if c}
_ALIAS.update({c.lower().replace(" ", ""): n for n, k, c, _ in _SEQUENCE if c})
_GREGORIAN = {n: g for n, k, _, g in _SEQUENCE if g}

# The anchor of record. Sourced, not invented. See GOVERNING SOURCES.
ANCHOR_DAY = 904
ANCHOR_YEAR = 1494
ANCHOR_PERIOD = "Tarsakh"
ANCHOR_DAY_OF = 30


class HarptosError(ValueError):
    pass


class LaneMismatch(HarptosError):
    pass


class NotationMismatch(HarptosError):
    pass


class NoEpoch(HarptosError):
    pass


def is_leap(year: int) -> bool:
    """Shieldmeet falls in years divisible by four."""
    return year % 4 == 0


def sequence(year: int):
    """The year's periods in order, with lengths resolved for leap."""
    out = []
    for name, kind, common, greg in _SEQUENCE:
        if name == "Shieldmeet" and not is_leap(year):
            continue
        out.append((name, kind, 30 if kind == MONTH else 1))
    return out


def year_length(year: int) -> int:
    return sum(length for _, _, length in sequence(year))


def canonical_period(name: str) -> str:
    key = name.strip().lower().replace(" ", "").replace("the", "", 1) \
        if name.strip().lower().startswith("the ") else name.strip().lower().replace(" ", "")
    if key in _ALIAS:
        return _ALIAS[key]
    key2 = name.strip().lower().replace(" ", "")
    if key2 in _ALIAS:
        return _ALIAS[key2]
    raise HarptosError(f"unknown Harptos period: {name!r}")


# ---------------------------------------------------------------- the date

@dataclass(frozen=True)
class Date:
    year: int
    period: str          # month or festival name
    day: int = 1         # always 1 for festivals
    lane: str = "UNSTAMPED"

    def __post_init__(self):
        object.__setattr__(self, "period", canonical_period(self.period))
        if self.period == "Shieldmeet" and not is_leap(self.year):
            raise HarptosError(f"Shieldmeet does not occur in {self.year} DR (not a leap year)")
        if self.kind == FESTIVAL:
            if self.day != 1:
                raise HarptosError(f"{self.period} is a single festival day; day must be 1")
        elif not 1 <= self.day <= 30:
            raise HarptosError(f"{self.period} has 30 days; got {self.day}")

    @property
    def kind(self) -> str:
        return MONTH if self.period in MONTHS else FESTIVAL

    @property
    def is_festival(self) -> bool:
        return self.kind == FESTIVAL

    @property
    def common_name(self) -> str:
        return _COMMON.get(self.period.lower(), "")

    @property
    def gregorian_month(self) -> str:
        """The Gregorian month this period sits in. Festivals report the gap."""
        if self.period in _GREGORIAN:
            return _GREGORIAN[self.period]
        seq = [n for n, _, _ in sequence(self.year)]
        i = seq.index(self.period)
        before = next((seq[j] for j in range(i - 1, -1, -1) if seq[j] in _GREGORIAN), None)
        after = next((seq[j] for j in range(i + 1, len(seq)) if seq[j] in _GREGORIAN), None)
        return f"{_GREGORIAN.get(before, '?')}/{_GREGORIAN.get(after, '?')} boundary"

    @property
    def ordinal(self) -> int:
        """Day of year, 1-based."""
        n = 0
        for name, _, length in sequence(self.year):
            if name == self.period:
                return n + self.day
            n += length
        raise HarptosError(f"{self.period} not in year {self.year}")

    def absolute(self) -> int:
        """Days since a notional 1 Hammer 1 DR. Internal arithmetic only."""
        y = self.year - 1
        return 365 * y + y // 4 + self.ordinal

    def day_number(self) -> int:
        return self.absolute() - _epoch_offset()

    def plus(self, days: int) -> "Date":
        return from_absolute(self.absolute() + days, self.lane)

    def stamp(self) -> str:
        return f"{self.lane}:{self.year}.{self.period.replace(' ', '')}.{self.day:02d}"

    def long(self) -> str:
        if self.is_festival:
            return f"{self.period}, {self.year} DR"
        return f"{self.day} {self.period} {self.year} DR"

    def __str__(self) -> str:
        return self.long()


def from_ordinal(year: int, ordinal: int, lane: str = "UNSTAMPED") -> Date:
    if not 1 <= ordinal <= year_length(year):
        raise HarptosError(f"ordinal {ordinal} out of range for {year} DR")
    n = 0
    for name, kind, length in sequence(year):
        if ordinal <= n + length:
            return Date(year, name, ordinal - n, lane)
        n += length
    raise HarptosError("unreachable")


def from_absolute(absolute: int, lane: str = "UNSTAMPED") -> Date:
    year = max(1, absolute // 366)
    while True:
        y = year - 1
        start = 365 * y + y // 4
        if absolute <= start:
            year -= 1
            continue
        if absolute > start + year_length(year):
            year += 1
            continue
        return from_ordinal(year, absolute - start, lane)


def _epoch_offset() -> int:
    anchor = Date(ANCHOR_YEAR, ANCHOR_PERIOD, ANCHOR_DAY_OF)
    return anchor.absolute() - ANCHOR_DAY


def from_day_number(day: int, lane: str = "UNSTAMPED") -> Date:
    return from_absolute(day + _epoch_offset(), lane)


def day_one() -> Date:
    """DERIVED from the anchor. Not campaign canon -- confirm before relying."""
    return from_day_number(1)


# ---------------------------------------------------------------- parsing

_DOTTED = re.compile(r"^(\d{1,5})\.([A-Za-z' ]+?)\.?(\d{1,2})?$")
_DAYNUM = re.compile(r"^[Dd](?:ay)?\s*(\d{1,6})$")
_SPOKEN = re.compile(r"^(?:day\s+)?(\d{1,2})\s+([A-Za-z' ]+?)\s+(\d{3,5})(?:\s*DR)?$", re.I)
_SPOKEN2 = re.compile(r"^([A-Za-z' ]+?)\s+(\d{1,2}),?\s+(\d{3,5})(?:\s*DR)?$", re.I)
_FEST = re.compile(r"^([A-Za-z' ]+?),?\s+(\d{3,5})(?:\s*DR)?$", re.I)
_ELAPSED = re.compile(r"^([A-Za-z_]{1,12})\s*\+\s*(\d{1,6})$")


def parse(text: str, lane: str | None = None) -> Date:
    """Parse a stamp or a date in any of the forms the campaign actually writes."""
    s = text.strip()
    if ":" in s:
        head, s = s.split(":", 1)
        lane = head.strip().upper() if lane is None else lane
        s = s.strip()
    lane = (lane or "UNSTAMPED").upper()

    m = _ELAPSED.match(s)
    if m:
        return Elapsed(int(m.group(2)), lane, m.group(1).upper())
    m = _DAYNUM.match(s)
    if m:
        return from_day_number(int(m.group(1)), lane)
    m = _DOTTED.match(s)
    if m:
        return Date(int(m.group(1)), m.group(2), int(m.group(3) or 1), lane)
    m = _SPOKEN.match(s)
    if m:
        return Date(int(m.group(3)), m.group(2), int(m.group(1)), lane)
    m = _SPOKEN2.match(s)
    if m:
        try:
            return Date(int(m.group(3)), m.group(1), int(m.group(2)), lane)
        except HarptosError:
            pass
    m = _FEST.match(s)
    if m:
        return Date(int(m.group(2)), m.group(1), 1, lane)
    raise HarptosError(f"cannot parse date: {text!r}")


@dataclass(frozen=True)
class Elapsed:
    """N days since a lane's named epoch. Not a calendar date."""

    count: int
    lane: str = "UNSTAMPED"
    epoch_name: str = "T"

    @property
    def notation(self) -> str:
        return "ELAPSED"

    def stamp(self) -> str:
        return f"{self.lane}:{self.epoch_name}+{self.count}"

    def long(self) -> str:
        return f"{self.epoch_name}+{self.count} ({self.epoch_name}-day {self.count})"

    def plus(self, days: int) -> "Elapsed":
        return Elapsed(self.count + days, self.lane, self.epoch_name)

    def resolve(self, epoch: "Date | None") -> Date:
        """Convert to a calendar date. Refuses without an epoch."""
        if epoch is None:
            raise NoEpoch(
                f"{self.stamp()} is a count, not a date. Declare the epoch for "
                f"lane {self.lane} before resolving it."
            )
        return epoch.plus(self.count)

    def __str__(self) -> str:
        return self.long()


def notation(x) -> str:
    return "ELAPSED" if isinstance(x, Elapsed) else "CALENDAR"


def delta(a, b) -> int:
    """Days from a to b. Refuses to cross lanes or notations."""
    if a.lane != b.lane and "UNSTAMPED" not in (a.lane, b.lane):
        raise LaneMismatch(
            f"refusing to subtract across lanes: {a.lane} vs {b.lane}. "
            "Two clocks are not one clock."
        )
    if notation(a) != notation(b):
        raise NotationMismatch(
            f"refusing to subtract a {notation(a)} stamp from a {notation(b)} one "
            f"({a.stamp()} vs {b.stamp()}). An elapsed count is not a date."
        )
    if isinstance(a, Elapsed):
        if a.epoch_name != b.epoch_name:
            raise NotationMismatch(
                f"different epochs: {a.epoch_name} vs {b.epoch_name}")
        return b.count - a.count
    return b.absolute() - a.absolute()


# ---------------------------------------------------------------- cli

def _show(d: Date) -> str:
    lines = [
        f"  stamp        {d.stamp()}",
        f"  long         {d.long()}",
        f"  period       {d.period}" + (f" ({d.common_name})" if d.common_name else "  [festival]"),
        f"  day of year  {d.ordinal} of {year_length(d.year)}",
        f"  day-number   {d.day_number()}",
        f"  gregorian    {d.gregorian_month}",
        f"  leap year    {'yes (Shieldmeet)' if is_leap(d.year) else 'no'}",
    ]
    return "\n".join(lines)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[1],
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("convert", help="show every representation of one date")
    c.add_argument("date")

    d = sub.add_parser("delta", help="days between two dates on the same lane")
    d.add_argument("a"); d.add_argument("b")

    a = sub.add_parser("add", help="advance a date by N days")
    a.add_argument("date"); a.add_argument("days", type=int)

    y = sub.add_parser("year", help="print a whole year's structure")
    y.add_argument("year", type=int)

    sub.add_parser("epoch", help="show the day-number anchor and derived Day 1")
    sub.add_parser("selftest", help="run the built-in checks")

    ns = p.parse_args(argv)

    if ns.cmd == "convert":
        print(_show(parse(ns.date))); return 0
    if ns.cmd == "delta":
        A, B = parse(ns.a), parse(ns.b)
        n = delta(A, B)
        print(f"{A.long()}  ->  {B.long()}")
        print(f"  {n:+d} days  ({n / 365:+.2f} years)")
        return 0
    if ns.cmd == "add":
        A = parse(ns.date)
        print(f"{A.long()}  {ns.days:+d} days"); print(_show(A.plus(ns.days))); return 0
    if ns.cmd == "year":
        n = 0
        print(f"{ns.year} DR — {year_length(ns.year)} days"
              f"{'  (Shieldmeet year)' if is_leap(ns.year) else ''}")
        for name, kind, length in sequence(ns.year):
            span = f"{n+1}" if length == 1 else f"{n+1}-{n+length}"
            greg = _GREGORIAN.get(name, "")
            common = _COMMON.get(name.lower(), "")
            tag = f"  {common}" if common else "  [festival]"
            print(f"  {span:>8}  {name:<18}{greg:<11}{tag}")
            n += length
        return 0
    if ns.cmd == "epoch":
        print(f"  anchor (sourced)  Day {ANCHOR_DAY} = "
              f"{ANCHOR_DAY_OF} {ANCHOR_PERIOD} {ANCHOR_YEAR} DR")
        print(f"  Day 1 (DERIVED)   {day_one().long()}")
        print("  Day 1 is arithmetic from the anchor, not campaign canon. Confirm it.")
        return 0
    if ns.cmd == "selftest":
        return selftest()
    return 1


def selftest() -> int:
    checks, failed = [], 0

    def ck(label, got, want):
        nonlocal failed
        ok = got == want
        if not ok:
            failed += 1
        checks.append((ok, label, got, want))

    ck("year length, common", year_length(1495), 365)
    ck("year length, Shieldmeet", year_length(1496), 366)
    ck("12 months", len(MONTHS), 12)
    ck("5 festivals in a common year",
       len([n for n, k, _ in sequence(1495) if k == FESTIVAL]), 5)
    ck("6 festivals in a Shieldmeet year",
       len([n for n, k, _ in sequence(1496) if k == FESTIVAL]), 6)
    ck("Tarsakh is April", _GREGORIAN["Tarsakh"], "April")
    ck("Tarsakh 30 ordinal", Date(1494, "Tarsakh", 30).ordinal, 121)
    ck("Greengrass follows Tarsakh", Date(1494, "Greengrass").ordinal, 122)

    # The two sourced lane facts. These are the reason the module exists.
    ck("anchor: Day 904 = 30 Tarsakh 1494",
       Date(1494, "Tarsakh", 30).day_number(), 904)
    ck("S073: Day 911 = 6 Mirtul 1494",
       Date(1494, "Mirtul", 6).day_number(), 911)
    ck("Day 905 is Greengrass", from_day_number(905).period, "Greengrass")

    ck("round trip, day-number", from_day_number(911).day_number(), 911)
    ck("round trip, absolute",
       from_absolute(Date(1495, "Hammer", 7).absolute()).long(), "7 Hammer 1495 DR")
    ck("add crosses a festival",
       Date(1494, "Tarsakh", 30).plus(1).period, "Greengrass")
    ck("add crosses a year", Date(1495, "Nightal", 30).plus(1).long(), "1 Hammer 1496 DR")
    ck("Shieldmeet exists in 1496",
       Date(1496, "Flamerule", 30).plus(2).period, "Shieldmeet")
    ck("Shieldmeet skipped in 1495",
       Date(1495, "Flamerule", 30).plus(2).period, "Eleasis")

    ck("parse dotted", parse("ARIK:1495.Hammer.07").long(), "7 Hammer 1495 DR")
    ck("parse day-number", parse("SHIVAN:D911").long(), "6 Mirtul 1494 DR")
    ck("parse spoken", parse("Day 7 Hammer 1495 DR").long(), "7 Hammer 1495 DR")
    ck("parse comma form", parse("Hammer 7, 1495").long(), "7 Hammer 1495 DR")
    ck("parse festival", parse("Greengrass 1494").period, "Greengrass")
    ck("parse common name", parse("1495.Deepwinter.07").period, "Hammer")
    ck("lane survives parse", parse("JORMUN:1498.Uktar.01").lane, "JORMUN")
    ck("stamp round trip",
       parse(parse("ARIK:1495.Hammer.07").stamp()).stamp(), "ARIK:1495.Hammer.07")

    lane_guard = False
    try:
        delta(parse("ARIK:1495.Hammer.07"), parse("SHIVAN:D911"))
    except LaneMismatch:
        lane_guard = True
    ck("cross-lane subtraction refused", lane_guard, True)

    ck("elapsed parses", parse("ARIK_HELL:T+35").count, 35)
    ck("elapsed stamp round trip",
       parse(parse("ARIK_HELL:T+35").stamp()).stamp(), "ARIK_HELL:T+35")
    ck("elapsed delta", delta(parse("ARIK_HELL:T+7"), parse("ARIK_HELL:T+35")), 28)
    ck("elapsed resolves against an epoch",
       parse("ARIK_HELL:T+35").resolve(Date(1496, "Hammer", 1)).long(),
       "5 Alturiak 1496 DR")

    epoch_guard = False
    try:
        parse("ARIK_HELL:T+35").resolve(None)
    except NoEpoch:
        epoch_guard = True
    ck("refuses to resolve without an epoch", epoch_guard, True)

    notation_guard = False
    try:
        delta(parse("ARIK_HELL:T+7"), parse("ARIK_HELL:1495.Hammer.07"))
    except NotationMismatch:
        notation_guard = True
    ck("elapsed vs calendar subtraction refused", notation_guard, True)

    shield_guard = False
    try:
        Date(1495, "Shieldmeet")
    except HarptosError:
        shield_guard = True
    ck("Shieldmeet rejected in a common year", shield_guard, True)

    for ok, label, got, want in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {label}"
              + ("" if ok else f"   got {got!r}, want {want!r}"))
    print(f"\n  {len(checks) - failed}/{len(checks)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
