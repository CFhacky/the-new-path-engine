#!/usr/bin/env python3
"""ad2e_psionics_harvest.py — collate AD&D 2nd-edition psionic powers (labelled).

THE PROCESS (Chad, 2026-08-28): other editions are welcome AS LONG AS labelled by
edition/system — the translator tools convert them. This is the FIRST AD&D 2e
content in the reference layer: the 2e psionics system (Complete Psionics
Handbook), which is a DIFFERENT subsystem from D&D 3.5 psionics (`power_index`) —
2e powers activate on a Power Score check, cost PSPs, and split into Sciences and
Devotions across six disciplines. Every row is stamped `"system": "AD&D 2e"` and
is source material for the system-translator skill.

    reference/ad2e_psionic_index.json — every 2e power: name, discipline,
                                        Science/Devotion, power score, initial &
                                        maintenance cost, range, preparation
                                        time, area of effect, prerequisites, page
    reference/ad2e_psionic_index.md   — the same, for human eyes

GOVERNING SOURCE
    I:\\Sourcebooks\\_text\\AD&D\\...\\Complete Psionics Handbook (2e).md — a
    born-digital text layer (Cyrillic-free). Each power is a NAME line then an
    alternating label/value block ("Power Score:" / "Wis -5" / "Initial Cost:" /
    "9" / …). The anchor is the "Power Score:" line (every power opens with it);
    the name is the line above; the discipline and Science/Devotion come from the
    "Chapter N: <Discipline>" and "<Discipline> Sciences/Devotions" headers above.
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
OUT_JSON = REPO / "reference" / "ad2e_psionic_index.json"
OUT_MD = REPO / "reference" / "ad2e_psionic_index.md"
SYSTEM = "AD&D 2e"

PAGE = re.compile(r"\[PDF page (\d+)\]")
POWER_SCORE = re.compile(r"^Power Score:\s*$", re.IGNORECASE)
DISCIPLINES = ("Clairsentience", "Psychokinesis", "Psychometabolism",
               "Psychoportation", "Telepathy", "Metapsionics")
CHAPTER = re.compile(rf"^Chapter\s+\d+:\s*({'|'.join(DISCIPLINES)})\b", re.IGNORECASE)
# the Science/Devotion section headers use the ADJECTIVE form of the discipline
# ("Clairsentient Sciences", "Telepathic Devotions", …)
CATEGORY = re.compile(r"^(Clairsentient|Psychokinetic|Psychometabolic|Psychoportive|"
                      r"Telepathic|Metapsionic)\s+(Sciences|Devotions)\s*$", re.IGNORECASE)
# the label/value fields, in the order they appear
LABELS: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"^Power Score:\s*$", re.IGNORECASE), "power_score"),
    (re.compile(r"^Initial Cost:\s*$", re.IGNORECASE), "initial_cost"),
    (re.compile(r"^Maintenance Cost:\s*$", re.IGNORECASE), "maintenance_cost"),
    (re.compile(r"^Range:\s*$", re.IGNORECASE), "range"),
    (re.compile(r"^Preparation Time:\s*$", re.IGNORECASE), "preparation_time"),
    (re.compile(r"^Area of Effect:\s*$", re.IGNORECASE), "area_of_effect"),
    (re.compile(r"^Prerequisites:\s*$", re.IGNORECASE), "prerequisites"),
    (re.compile(r"^MTHAC0:\s*$", re.IGNORECASE), "mthac0"),
    (re.compile(r"^Duration:\s*$", re.IGNORECASE), "duration"),
]
ANY_LABEL = re.compile(r"^(Power Score|Initial Cost|Maintenance Cost|Range|"
                       r"Preparation Time|Area of Effect|Prerequisites|MTHAC0|"
                       r"Duration):\s*$", re.IGNORECASE)
NAME_REJECT = re.compile(r"^(Chapter|Sciences|Devotions|Clairsentience|Psychokinesis|"
                         r"Psychometabolism|Psychoportation|Telepathy|Metapsionics|"
                         r"Table|Contents|Introduction|Psionic|Power|The|A|An)\b",
                         re.IGNORECASE)


@dataclass
class Ad2ePower:
    name: str
    book: str
    page: Optional[int]
    start: int
    end: int
    system: str = SYSTEM
    discipline: Optional[str] = None
    category: Optional[str] = None        # Science | Devotion
    power_score: Optional[str] = None
    initial_cost: Optional[str] = None
    maintenance_cost: Optional[str] = None
    range: Optional[str] = None
    preparation_time: Optional[str] = None
    area_of_effect: Optional[str] = None
    prerequisites: Optional[str] = None
    mthac0: Optional[str] = None
    duration: Optional[str] = None

    def quick_fields(self) -> int:
        return sum(1 for v in (self.discipline, self.power_score, self.initial_cost,
                               self.range) if v)


def _name_above(lines: List[str], i: int) -> Optional[Tuple[int, str]]:
    j = i - 1
    while j >= 0:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            j -= 1
            continue
        if 2 <= len(s) <= 40 and s[0].isalpha() and not NAME_REJECT.match(s) \
                and not ANY_LABEL.match(s) and not s.endswith((".", ",", ":")):
            return j, s
        return None
    return None


def detect_ad2e_powers(lines: List[str], pages: List[int], book: str) -> List[Ad2ePower]:
    n = len(lines)
    # discipline/category markers, in order
    markers: List[Tuple[int, str, Optional[str]]] = []
    for i, ln in enumerate(lines):
        s = ln.strip()
        mc = CHAPTER.match(s)
        if mc:
            markers.append((i, mc.group(1).title(), None))
            continue
        mk = CATEGORY.match(s)
        if mk:
            cat = "Science" if mk.group(2).lower().startswith("scienc") else "Devotion"
            markers.append((i, None, cat))       # discipline comes from the Chapter line

    def context(idx: int) -> Tuple[Optional[str], Optional[str]]:
        disc = cat = None
        for mi, mdisc, mcat in markers:
            if mi < idx:
                if mdisc is not None:
                    disc = mdisc
                if mcat is not None:
                    cat = mcat
            else:
                break
        return disc, cat

    starts: List[Tuple[int, str, int]] = []
    used = set()
    for i, ln in enumerate(lines):
        if not POWER_SCORE.match(ln.strip()):
            continue
        got = _name_above(lines, i)
        if got is None or got[0] in used:
            continue
        used.add(got[0])
        starts.append((got[0], got[1], i))

    starts.sort()
    out: List[Ad2ePower] = []
    for k, (nj, name, ps_idx) in enumerate(starts):
        e = starts[k + 1][0] if k + 1 < len(starts) else min(n, nj + 60)
        e = min(e, nj + 60)
        disc, cat = context(nj)
        p = Ad2ePower(name=name, book=book, page=pages[nj], start=nj, end=e,
                      discipline=disc, category=cat)
        # read the alternating label / value block from the Power Score line
        j = ps_idx
        while j < min(n, ps_idx + 26):
            s = lines[j].strip()
            matched = None
            for rx, attr in LABELS:
                if rx.match(s):
                    matched = attr
                    break
            if matched:
                v = j + 1
                while v < n and (lines[v].strip() == "" or PAGE.search(lines[v])):
                    v += 1
                if v < n and getattr(p, matched) is None and not ANY_LABEL.match(lines[v].strip()):
                    setattr(p, matched, re.sub(r"\s+", " ", lines[v].strip()))
                j = v
                continue
            # stop when the description prose begins (a non-label, non-value line
            # well past the first few fields)
            if ANY_LABEL.match(s) is None and j > ps_idx + 2 and p.area_of_effect:
                break
            j += 1
        out.append(p)

    best: Dict[str, Ad2ePower] = {}
    for p in out:
        best.setdefault(p.name.lower(), p)
    return sorted(best.values(), key=lambda x: x.start)


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[Ad2ePower]]] = {
    "ad2e": detect_ad2e_powers,
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
    powers: List[Ad2ePower] = field(default_factory=list)


SOURCES: List[Source] = [
    Source("cph", "Complete Psionics Handbook (2e)",
           Path("AD&D/Complete Psionics Handbook (2e).md"),
           "The Complete Psionics Handbook (TSR, AD&D 2e)", "ad2e"),
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
            src.powers = DETECTORS[src.detector](src.lines, pages, src.book)
            src.coverage = f"ok — {len(src.powers)} powers from {path.name}"

    def all_powers(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for p in src.powers:
                yield src, p

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, p in self.all_powers(book):
            nm = p.name.lower()
            if nm == q:
                exact.append((src, p))
            elif q in nm:
                partial.append((src, p))
        return exact if exact else partial


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# AD&D 2e PSIONIC INDEX — The New Path",
        "",
        "**Generated by `scripts/ad2e_psionics_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** **AD&D 2nd Edition** psionic powers — a DIFFERENT",
        "edition and a DIFFERENT subsystem from the 3.5e `power_index`. Every row",
        "is stamped `system: AD&D 2e`; a 2e power is SOURCE MATERIAL for the",
        "system-translator skill. Powers activate on a Power Score check and cost",
        "PSPs (initial + maintenance); they split into Sciences and Devotions",
        "across six disciplines.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.powers)
        parsed_well += sum(1 for p in src.powers if p.quick_fields() >= 3)
        sources_out.append({"key": src.key, "book": src.book, "system": SYSTEM,
                            "citation": src.citation, "coverage": src.coverage,
                            "powers": [asdict(p) for p in src.powers]})
        md.append(f"## {src.book} — {len(src.powers)} powers  *(system: {SYSTEM})*")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.powers:
            md.append("| Power | Discipline | Type | Power Score | Cost (init/maint) | Range | Area | Page |")
            md.append("|---|---|---|---|---|---|---|---|")
            for p in src.powers:
                cost = f"{p.initial_cost or '—'}/{p.maintenance_cost or '—'}"
                md.append(f"| {p.name} | {p.discipline or '—'} | {p.category or '—'} | "
                          f"{p.power_score or '—'} | {cost} | {p.range or '—'} | "
                          f"{p.area_of_effect or '—'} | {p.page if p.page is not None else '—'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/ad2e_psionics_harvest.py",
                    "system": SYSTEM, "corpus": str(corpus.base),
                    "total_powers": total, "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 6:
        print(f"'{name}' matches {len(hits)} powers; narrow with the exact name:")
        for src, p in hits[:20]:
            print(f"  {p.name}   [{p.book}, p.{p.page}]")
        return 1
    packets = []
    for src, p in hits:
        body = [ln for ln in src.lines[p.start:p.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "ad2e-psionic-for-translation",
            "instructions": ("An AD&D 2e psionic power (system: AD&D 2e). Feed to "
                             "the system-translator skill for the 3.5e and/or GURPS "
                             "treatment. The raw_block is born-digital text."),
            "name": p.name, "system": SYSTEM,
            "source": {"book": p.book, "pdf_page": p.page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [p.start + 1, p.end], "citation": src.citation},
            "parsed": {k: v for k, v in asdict(p).items()
                       if k in ("discipline", "category", "power_score", "initial_cost",
                                "maintenance_cost", "range", "preparation_time",
                                "area_of_effect", "prerequisites", "mthac0", "duration")
                       and v},
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


FIXTURE = """## [PDF page 27]
Chapter 3: Clairsentience
Clairsentient Sciences
Aura Sight
Power Score:
Wis -5
Initial Cost:
9
Maintenance Cost:
9/round
Range:
50 yds.
Preparation Time:
0
Area of Effect:
personal
Prerequisites:
none
An aura is a glowing halo of colored light.

Clairsentient Devotions
All-Round Vision
Power Score:
Wis -3
Initial Cost:
4
Maintenance Cost:
4/round
Range:
0
Preparation Time:
0
Area of Effect:
personal
Prerequisites:
none
The psionicist can see in all directions at once.
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    lines = FIXTURE.splitlines()
    powers = detect_ad2e_powers(lines, _pages_for(lines), "The Complete Psionics Handbook (2e)")
    names = [p.name for p in powers]
    if names != ["Aura Sight", "All-Round Vision"]:
        failures.append(f"fixture detected {names}, wanted the two 2e powers")
    else:
        au = powers[0]
        if (au.discipline, au.category, au.power_score, au.initial_cost, au.range) != \
                ("Clairsentience", "Science", "Wis -5", "9", "50 yds."):
            failures.append(f"Aura Sight {(au.discipline, au.category, au.power_score, au.initial_cost, au.range)}")
        if au.system != "AD&D 2e":
            failures.append("system must be 'AD&D 2e'")
        arv = powers[1]
        if arv.category != "Devotion":
            failures.append(f"All-Round Vision category {arv.category!r}, wanted 'Devotion'")

    if base.is_dir() and (base / SOURCES[0].path).exists():
        corpus = Corpus(base, _fresh_sources())
        powers = corpus.sources[0].powers
        if len(powers) < 80:
            failures.append(f"only {len(powers)} 2e powers indexed; expected > 80")
        discs = {p.discipline for p in powers}
        if len(discs & set(DISCIPLINES)) < 5:
            failures.append(f"only disciplines {discs} seen; expected most of the six")
    else:
        print("  [SKIP] Complete Psionics Handbook extraction not found — fixture only")

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
        found = sorted({(p.name, p.discipline or "—", p.category or "—", p.page or -1)
                        for _, p in corpus.all_powers(args.book) if q in p.name.lower()})
        for nm, disc, cat, page in found:
            print(f"  {nm}  [{disc} {cat}; p.{page}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.powers for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.powers):4d} powers" if src.powers else "   0 powers"
        print(f"  {src.book:40s} {status}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} AD&D 2e psionic powers. (system: {SYSTEM})")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
