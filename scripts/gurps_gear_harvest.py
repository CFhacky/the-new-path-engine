#!/usr/bin/env python3
"""gurps_gear_harvest.py — collate the GURPS Low-Tech weapon table.

THE PROCESS (Chad, 2026-08-28, continuing the GURPS shelf): gear — weapons and
armor — is codified GURPS mechanics the reference layer still lacked. GURPS
Low-Tech is the medieval/fantasy gear book. Its stat TABLES were OCR'd as a
vertical column-dump (each row's cells one per line), so they get their own
detector and their own index.

    reference/gurps_gear_index.json  — every weapon (name, damage, reach, parry,
                                       cost, weight, min ST) AND every torso-armor
                                       (name, TL, DR, cost, weight, don), book+page
    reference/gurps_gear_index.md    — the same, for human eyes

Both the WEAPON table and the ARMOR table are parsed — each was OCR'd as a
vertical column-dump and gets its own detector.

WORKFLOW
    python gurps_gear_harvest.py                    # (re)build the index
    python gurps_gear_harvest.py --search "axe"     # find candidates
    python gurps_gear_harvest.py --export "Katana"
    python gurps_gear_harvest.py --selftest

GOVERNING SOURCE
    I:\\Sourcebooks\\_text\\GURPS\\GURPS 4e\\GURPS 4e - Low-Tech.md
    * Melee Weapon Table — each weapon row is a NAME line, then the columns one
      per line: Damage (sw/thr ± N type), Reach, Parry, Cost ($N), Weight, Min
      ST, then optional [Notes] and "or" + alternate-damage rows. The anchor is
      a damage line whose line above is a plausible weapon name (not "or"). The
      OCR appends stray letters to some values ("0U" for parry 0); those are
      cleaned.
    * Armor Table — each row is the columns one per line: TL, Torso Armor (name),
      DR, Cost ($N), Weight, Don, then optional [Notes]. The anchor is a
      standalone $cost line whose four neighbours match the row signature (TL
      digit / name / DR / $cost / weight / don).
    The PDF stands behind every extraction. This is native GURPS 4e data.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CORPUS = Path(r"I:\Sourcebooks\_text")
REPO = Path(__file__).resolve().parent.parent
OUT_JSON = REPO / "reference" / "gurps_gear_index.json"
OUT_MD = REPO / "reference" / "gurps_gear_index.md"

PAGE = re.compile(r"\[PDF page (\d+)\]")
DAMAGE = re.compile(r"^(sw|thr)[+\-]?\d*\s+(cut|imp|cr|pi\+*|pi-?|burn|tox|dmg)\b",
                    re.IGNORECASE)
NAMEISH = re.compile(r"^[A-Z][A-Za-z][A-Za-z '\u2019\-/]{1,30}$")
# A weapon-table stat cell: a $ cost, a dash (blank/same), a small number (with a
# stray OCR letter tolerated), or a reach/parry code.
STATVAL = re.compile(r"^(\$[\d,]+|[-\u2013\u2014]|\d{1,3}[A-Za-z\u00bd]{0,2}|C|F|\u00bd|\d[,/]\d)$")
NOTE = re.compile(r"^\[\d")

# Armor-table cells (a column-dump: TL / Name / DR / Cost / Weight / Don / Notes)
ARMOR_COST = re.compile(r"^\$[\d,]+$")
ARMOR_DR = re.compile(r"^\d{1,2}(?:/\d{1,2})?\*?$")     # "3", "1*", "4/2*"
ARMOR_TL = re.compile(r"^\d$")                           # TL 0-8
ARMOR_NAME = re.compile(r"^[A-Z][A-Za-z][A-Za-z ,'\u2019\-/()]{1,34}$")
ARMOR_NUM = re.compile(r"^[\d,]+(?:\.\d+)?$")            # weight / don


def _clean(v: str) -> Optional[str]:
    if v in ("-", "\u2013", "\u2014"):
        return None                        # dash = blank / same as primary
    v = re.sub(r"([\d\u00bd])[A-Za-z]+$", r"\1", v)   # strip stray OCR letter ("0U" -> "0")
    return v


@dataclass
class GurpsGear:
    name: str
    book: str
    page: Optional[int]
    start: int
    end: int
    category: str = "weapon"
    damage: Optional[str] = None
    reach: Optional[str] = None
    parry: Optional[str] = None
    cost: Optional[str] = None
    weight: Optional[str] = None
    min_st: Optional[str] = None
    # armor-only columns
    tl: Optional[str] = None
    dr: Optional[str] = None
    don: Optional[str] = None
    notes: Optional[str] = None

    def quick_fields(self) -> int:
        if self.category == "armor":
            return sum(1 for v in (self.dr, self.cost, self.weight, self.don) if v)
        return sum(1 for v in (self.damage, self.cost, self.weight, self.min_st) if v)


def _name_above(lines: List[str], i: int) -> Optional[int]:
    j = i - 1
    while j >= 0 and (lines[j].strip() == "" or PAGE.search(lines[j])):
        j -= 1
    if j < 0:
        return None
    s = lines[j].strip()
    if s.lower() == "or" or not NAMEISH.match(s):
        return None
    return j


def detect_weapons(lines: List[str], pages: List[int], book: str) -> List[GurpsGear]:
    n = len(lines)
    gear: List[GurpsGear] = []
    for i, ln in enumerate(lines):
        if not DAMAGE.match(ln.strip()):
            continue
        a = _name_above(lines, i)
        if a is None:
            continue
        # the five columns after the damage line, in order
        vals: List[str] = []
        j = i + 1
        while j < n and len(vals) < 5:
            s = lines[j].strip()
            if s == "" or PAGE.search(lines[j]):
                j += 1
                continue
            if s.lower() == "or" or NOTE.match(s):
                break
            if STATVAL.match(s):
                vals.append(s)
                j += 1
            else:
                break
        vals += [None] * (5 - len(vals))
        g = GurpsGear(name=lines[a].strip(), book=book, page=pages[a], start=a,
                      end=min(n, i + 9), category="weapon", damage=ln.strip())
        g.reach, g.parry, g.cost, g.weight, g.min_st = (
            _clean(v) if v else None for v in vals)
        gear.append(g)

    # A weapon is listed under each of its attack modes; keep one row per name —
    # the richest (most stats), then the first.
    best: Dict[str, GurpsGear] = {}
    for g in gear:
        k = g.name.lower()
        cur = best.get(k)
        if cur is None or g.quick_fields() > cur.quick_fields():
            best[k] = g
    return sorted(best.values(), key=lambda g: g.start)


def detect_armor(lines: List[str], pages: List[int], book: str) -> List[GurpsGear]:
    # The armor table was OCR'd as a column-dump with no blank lines between
    # cells. Work on the non-blank/non-page tokens and anchor on a standalone
    # $cost cell whose four neighbours match the row signature.
    toks = [(i, lines[i].strip()) for i in range(len(lines))
            if lines[i].strip() and not PAGE.search(lines[i])]
    gear: List[GurpsGear] = []
    for k in range(3, len(toks) - 2):
        i_cost, cost = toks[k]
        if not ARMOR_COST.match(cost):
            continue
        i_tl, tl = toks[k - 3]
        i_nm, nm = toks[k - 2]
        i_dr, dr = toks[k - 1]
        _, wt = toks[k + 1]
        i_don, don = toks[k + 2]
        if not (ARMOR_TL.match(tl) and ARMOR_NAME.match(nm) and ARMOR_DR.match(dr)
                and ARMOR_NUM.match(wt) and ARMOR_NUM.match(don)):
            continue
        notes = toks[k + 3][1] if k + 3 < len(toks) and NOTE.match(toks[k + 3][1]) else None
        gear.append(GurpsGear(name=nm, book=book, page=pages[i_nm], start=i_tl,
                              end=i_don + 1, category="armor", tl=tl, dr=dr,
                              cost=cost, weight=wt, don=don, notes=notes))

    best: Dict[str, GurpsGear] = {}
    for g in gear:
        key = g.name.lower()
        cur = best.get(key)
        if cur is None or g.quick_fields() > cur.quick_fields():
            best[key] = g
    return sorted(best.values(), key=lambda g: g.start)


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[GurpsGear]]] = {
    "weapons": detect_weapons,
    "armor": detect_armor,
}


@dataclass
class Source:
    key: str
    book: str
    path: Path
    citation: str
    detector: str
    coverage: str = "pending"
    lines: List[str] = field(default_factory=list)
    gear: List[GurpsGear] = field(default_factory=list)


_LOWTECH = Path("GURPS/GURPS 4e/GURPS 4e - Low-Tech.md")
SOURCES: List[Source] = [
    Source("lowtech", "GURPS Low-Tech — Weapons", _LOWTECH,
           "GURPS Low-Tech (SJGames, 4e), Melee Weapon Table", "weapons"),
    Source("lowtech-armor", "GURPS Low-Tech — Armor", _LOWTECH,
           "GURPS Low-Tech (SJGames, 4e), Armor Table", "armor"),
]


def _pages_for(lines: List[str]) -> List[int]:
    pages: List[int] = []
    page = 0
    for ln in lines:
        m = PAGE.search(ln)
        if m:
            page = int(m.group(1))
        pages.append(page)
    return pages


def _fresh_sources() -> List[Source]:
    return [Source(*(getattr(s, k) for k in ("key", "book", "path", "citation", "detector")))
            for s in SOURCES]


class Corpus:
    def __init__(self, base: Path, sources: List[Source]):
        self.base = base
        self.sources = sources
        for src in self.sources:
            path = base / src.path
            if not path.exists():
                src.coverage = f"NO COVERAGE — extraction missing: {path}"
                continue
            src.lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            pages = _pages_for(src.lines)
            src.gear = DETECTORS[src.detector](src.lines, pages, src.book)
            noun = "armor pieces" if src.detector == "armor" else "weapons"
            src.coverage = f"ok — {len(src.gear)} {noun} from {path.name}"

    def all_gear(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for g in src.gear:
                yield src, g

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, g in self.all_gear(book):
            nm = g.name.lower()
            if nm == q:
                exact.append((src, g))
            elif q in nm:
                partial.append((src, g))
        return exact if exact else partial


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# GURPS GEAR INDEX — The New Path",
        "",
        "**Generated by `scripts/gurps_gear_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** GURPS Low-Tech weapons AND armor (native GURPS 4e).",
        "The raw text stays on `I:\\Sourcebooks` — use `--export \"NAME\"` for the",
        "packet. The stat tables were OCR'd as column-dumps; a field left `—` is",
        "one the OCR did not cleanly yield.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.gear)
        parsed_well += sum(1 for g in src.gear if g.quick_fields() >= 3)
        sources_out.append({"key": src.key, "book": src.book, "citation": src.citation,
                            "category": src.detector, "coverage": src.coverage,
                            "gear": [asdict(g) for g in src.gear]})
        noun = "armor pieces" if src.detector == "armor" else "weapons"
        md.append(f"## {src.book} — {len(src.gear)} {noun}")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.gear and src.detector == "armor":
            md.append("| Armor | TL | DR | Cost | Weight | Don | Notes | Page |")
            md.append("|---|---|---|---|---|---|---|---|")
            for g in src.gear:
                md.append(f"| {g.name} | {g.tl or '—'} | {g.dr or '—'} | {g.cost or '—'} | "
                          f"{g.weight or '—'} | {g.don or '—'} | {g.notes or '—'} | "
                          f"{g.page if g.page is not None else '—'} |")
        elif src.gear:
            md.append("| Weapon | Damage | Reach | Parry | Cost | Weight | Min ST | Page |")
            md.append("|---|---|---|---|---|---|---|---|")
            for g in src.gear:
                md.append(f"| {g.name} | {g.damage or '—'} | {g.reach or '—'} | "
                          f"{g.parry or '—'} | {g.cost or '—'} | {g.weight or '—'} | "
                          f"{g.min_st or '—'} | {g.page if g.page is not None else '—'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/gurps_gear_harvest.py",
                    "corpus": str(corpus.base), "total_gear": total,
                    "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 8:
        print(f"'{name}' matches {len(hits)} items; narrow with the exact name:")
        for src, g in hits[:20]:
            print(f"  {g.name}   [{g.book}, p.{g.page}]")
        return 1
    packets = []
    for src, g in hits:
        body = [ln for ln in src.lines[g.start:g.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "gurps-gear-for-translation",
            "instructions": ("Native GURPS 4e gear. The GURPS half is here; the "
                             "system-translator skill builds the D&D 3.5e half. "
                             "The raw_block is OCR text from a column-dump table; "
                             "check oddities against the source PDF."),
            "name": g.name,
            "source": {"book": g.book, "pdf_page": g.page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [g.start + 1, g.end], "citation": src.citation},
            "parsed": {k: v for k, v in asdict(g).items()
                       if k in ("category", "damage", "reach", "parry", "cost",
                                "weight", "min_st", "tl", "dr", "don", "notes") and v},
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


FIXTURE = """## [PDF page 64]
Axe
sw+2 cut
1
0U
$50
4
11
0
Hatchet
sw cut
1
0
$40
2
8
[1]
or
thr cr
1
0
–
–
8
Estoc
thr+2 imp
1
0
$500
3
10
[4]
"""

ARMOR_FIXTURE = """## [PDF page 110]
TL
Torso Armor
DR
Cost
Weight
Don
Notes
0
Cane
1
$35
12
28
[1]
0
Cloth, Padded
1*
$50
6
15
2
Mail, Light
3*
$500
12
30
[4]
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    lines = FIXTURE.splitlines()
    gear = detect_weapons(lines, _pages_for(lines), "GURPS Low-Tech")
    names = [g.name for g in gear]
    if names != ["Axe", "Hatchet", "Estoc"]:
        failures.append(f"fixture detected {names}, wanted ['Axe', 'Hatchet', 'Estoc'] "
                        f"(the 'or' alternate-damage row is not a new weapon)")
    else:
        axe = gear[0]
        got = (axe.damage, axe.reach, axe.parry, axe.cost, axe.weight, axe.min_st)
        want = ("sw+2 cut", "1", "0", "$50", "4", "11")
        if got != want:
            failures.append(f"Axe row {got}, wanted {want} (parry '0U' cleaned to '0')")

    alines = ARMOR_FIXTURE.splitlines()
    armor = detect_armor(alines, _pages_for(alines), "GURPS Low-Tech")
    anames = [g.name for g in armor]
    if anames != ["Cane", "Cloth, Padded", "Mail, Light"]:
        failures.append(f"armor fixture detected {anames}, wanted the three armor rows "
                        f"(header row must NOT be captured)")
    else:
        cane = armor[0]
        got = (cane.tl, cane.dr, cane.cost, cane.weight, cane.don, cane.notes)
        want = ("0", "1", "$35", "12", "28", "[1]")
        if got != want:
            failures.append(f"Cane armor row {got}, wanted {want}")
        if armor[2].dr != "3*":
            failures.append(f"Mail, Light DR {armor[2].dr!r}, wanted '3*' (flexible)")

    if base.is_dir() and (base / SOURCES[0].path).exists():
        corpus = Corpus(base, _fresh_sources())
        wpns = sum(len(s.gear) for s in corpus.sources if s.detector == "weapons")
        arm = sum(len(s.gear) for s in corpus.sources if s.detector == "armor")
        if wpns < 120:
            failures.append(f"only {wpns} weapons indexed; expected > 120")
        if arm < 20:
            failures.append(f"only {arm} armor pieces indexed; expected > 20")
        kat = corpus.find("katana", book="lowtech")
        if not kat:
            failures.append("Katana not found in live Low-Tech")
        elif kat[0][1].damage is None:
            failures.append("Katana has no damage parsed")
    else:
        print(f"  [SKIP] Low-Tech extraction not found — fixture checks only")

    for f in failures:
        print(f"SELFTEST FAIL: {f}")
    print("selftest: " + ("PASS" if not failures else f"{len(failures)} failure(s)"))
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--corpus", type=Path, default=CORPUS)
    ap.add_argument("--search", metavar="TEXT")
    ap.add_argument("--book")
    ap.add_argument("--export", metavar="NAME")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest(args.corpus)

    corpus = Corpus(args.corpus, _fresh_sources())

    if args.search:
        q = args.search.lower()
        found = sorted({(g.name, g.book, g.page or -1,
                         g.damage or (f"DR {g.dr}" if g.dr else "—"))
                        for _, g in corpus.all_gear(args.book) if q in g.name.lower()})
        for name, bk, page, stat in found:
            loc = bk if page < 0 else f"{bk}, p.{page}"
            print(f"  {name}   [{stat}; {loc}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.gear for s in corpus.sources)
    for src in corpus.sources:
        noun = "armor" if src.detector == "armor" else "weapons"
        status = f"{len(src.gear):4d} {noun}" if src.gear else f"   0 {noun}"
        print(f"  {src.book:28s} {status}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} GURPS gear entries (weapons + armor); {parsed_well} with 3+ stats parsed.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
