#!/usr/bin/env python3
"""dnd5e_spell_harvest.py — collate D&D 5e spells (labelled system: D&D 5e).

THE PROCESS (Chad, 2026-08-28): other editions are welcome AS LONG AS labelled
by edition/system — the translator tools convert them. This is the D&D 5e SPELL
index, separate from the 3.5e `spell_index` and stamped `"system": "D&D 5e"`.

    reference/dnd5e_spell_index.json  — every 5e spell: name, level, school,
                                        ritual, casting time, range, components,
                                        duration, book, PDF page, system D&D 5e
    reference/dnd5e_spell_index.md    — the same, for human eyes

GOVERNING SOURCES
    I:\\Sourcebooks\\_text\\D&D 5e\\ — 5e books with spell lists (Tasha's,
    Diabolical Designs, Mordenkainen's Almanac of Adventurers, Darkhold). A 5e
    spell is a NAME line then "Nth-level school (ritual)" or "cantrip school",
    then Casting Time / Range / Components / Duration. Detection anchors on the
    level-school line (confirmed by a Casting Time line below), name above. A
    configured source whose file is missing prints NO COVERAGE.
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
OUT_JSON = REPO / "reference" / "dnd5e_spell_index.json"
OUT_MD = REPO / "reference" / "dnd5e_spell_index.md"
SYSTEM = "D&D 5e"

PAGE = re.compile(r"\[PDF page (\d+)\]")
SCHOOLS = ("abjuration|conjuration|divination|enchantment|evocation|illusion|"
           "necromancy|transmutation")
LEVEL_SCHOOL = re.compile(
    rf"^(?:(cantrip)|(\d)(?:st|nd|rd|th)-level)\s+({SCHOOLS})(\s*\(ritual\))?\s*$",
    re.IGNORECASE)
CAST = re.compile(r"^Casting Time\s*:\s*(.+)$", re.IGNORECASE)
RANGE = re.compile(r"^Range\s*:\s*(.+)$", re.IGNORECASE)
COMP = re.compile(r"^Components?\s*:\s*(.+)$", re.IGNORECASE)
DURATION = re.compile(r"^Duration\s*:\s*(.+)$", re.IGNORECASE)
FIELD = re.compile(r"^(Casting Time|Range|Components?|Duration)\s*:", re.IGNORECASE)


_SMALL = {"of", "the", "and", "or", "a", "an", "to", "in", "on", "from", "with", "for"}


def _smart_title(s: str) -> str:
    """Title-case an ALL-CAPS OCR name, keeping small words lower (except first)."""
    words = s.split()
    out = []
    for k, w in enumerate(words):
        lw = w.lower()
        out.append(lw if (k > 0 and lw in _SMALL) else lw.capitalize())
    return " ".join(out)


def _plausible_name(s: str) -> bool:
    s = s.strip()
    if not (3 <= len(s) <= 44):
        return False
    if s.endswith((".", ",", ":", ";")) or FIELD.match(s) or LEVEL_SCHOOL.match(s):
        return False
    if not s[0].isalpha():
        return False
    letters = sum(c.isalpha() for c in s)
    return letters >= max(3, len(s) // 2)


@dataclass
class Spell5e:
    name: str
    book: str
    page: Optional[int]
    start: int
    end: int
    system: str = SYSTEM
    level: Optional[str] = None          # "cantrip" or "1".."9"
    school: Optional[str] = None
    ritual: Optional[bool] = None
    casting_time: Optional[str] = None
    range: Optional[str] = None
    components: Optional[str] = None
    duration: Optional[str] = None

    def quick_fields(self) -> int:
        return sum(1 for v in (self.school, self.casting_time, self.range, self.duration) if v)


def _name_above(lines: List[str], i: int) -> Optional[int]:
    j, seen = i - 1, 0
    while j >= 0 and seen < 3:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            j -= 1
            continue
        seen += 1
        if _plausible_name(s):
            return j
        return None
    return None


def _has_cast_below(lines: List[str], i: int, n: int) -> bool:
    for k in range(i + 1, min(n, i + 6)):
        s = lines[k].strip()
        if s and CAST.match(s):
            return True
    return False


def detect_5e_spells(lines: List[str], pages: List[int], book: str) -> List[Spell5e]:
    n = len(lines)
    starts: List[Tuple[int, str, re.Match]] = []
    used = set()
    for i, ln in enumerate(lines):
        m = LEVEL_SCHOOL.match(ln.strip())
        if not m or not _has_cast_below(lines, i, n):
            continue
        a = _name_above(lines, i)
        if a is None or a in used:
            continue
        used.add(a)
        starts.append((a, lines[a].strip(), m))

    starts.sort()
    out: List[Spell5e] = []
    for k, (a, name, m) in enumerate(starts):
        e = starts[k + 1][0] if k + 1 < len(starts) else min(n, a + 60)
        e = min(e, a + 60)
        nm = _smart_title(name) if name.isupper() else name
        sp = Spell5e(name=nm, book=book, page=pages[a], start=a, end=e,
                     level=("cantrip" if m.group(1) else m.group(2)),
                     school=m.group(3).lower(), ritual=bool(m.group(4)))
        for raw in lines[a + 1:e]:
            s = raw.strip()
            for attr, rx in (("casting_time", CAST), ("range", RANGE),
                             ("components", COMP), ("duration", DURATION)):
                if getattr(sp, attr) is None:
                    g = rx.match(s)
                    if g:
                        setattr(sp, attr, re.sub(r"\s+", " ", g.group(1)).strip())
                        break
        out.append(sp)

    best: Dict[str, Spell5e] = {}
    for sp in out:
        best.setdefault(sp.name.lower(), sp)
    return sorted(best.values(), key=lambda x: x.start)


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[Spell5e]]] = {
    "5e": detect_5e_spells,
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
    spells: List[Spell5e] = field(default_factory=list)


_TP = "D&D 5e/Third Party and DMs Guild"
_OF = "D&D 5e/Official"
SOURCES: List[Source] = [
    Source("tashas", "Tasha's Cauldron of Everything (5e)",
           Path(f"{_OF}/Tashas Cauldron of Everything.md"),
           "Tasha's Cauldron of Everything (5e, WotC)", "5e"),
    Source("diabolical", "Diabolical Designs (5e, 3pp)",
           Path(f"{_TP}/Diabolical Designs.md"), "Diabolical Designs (5e)", "5e"),
    Source("almanac", "Mordenkainen's Almanac of Adventurers (5e, 3pp)",
           Path(f"{_TP}/Mordenkainens Almanac of Adventurers.md"),
           "Mordenkainen's Almanac of Adventurers (5e, DMs Guild)", "5e"),
    Source("darkhold", "Darkhold: Secrets of the Zhentarim (5e, 3pp)",
           Path(f"{_TP}/Darkhold - Secrets of the Zhentarim.md"),
           "Darkhold: Secrets of the Zhentarim (5e, DMs Guild)", "5e"),
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
            src.spells = DETECTORS[src.detector](src.lines, pages, src.book)
            src.coverage = f"ok — {len(src.spells)} spells from {path.name}"

    def all_spells(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for sp in src.spells:
                yield src, sp

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, sp in self.all_spells(book):
            nm = sp.name.lower()
            if nm == q:
                exact.append((src, sp))
            elif q in nm:
                partial.append((src, sp))
        return exact if exact else partial


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# D&D 5e SPELL INDEX — The New Path",
        "",
        "**Generated by `scripts/dnd5e_spell_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** **D&D 5th Edition** spells — a DIFFERENT edition",
        "from the 3.5e `spell_index`. Every row is stamped `system: D&D 5e`;",
        "a 5e spell is SOURCE MATERIAL for the system-translator skill.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.spells)
        parsed_well += sum(1 for sp in src.spells if sp.quick_fields() >= 3)
        sources_out.append({"key": src.key, "book": src.book, "system": SYSTEM,
                            "citation": src.citation, "coverage": src.coverage,
                            "spells": [asdict(sp) for sp in src.spells]})
        md.append(f"## {src.book} — {len(src.spells)} spells  *(system: {SYSTEM})*")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.spells:
            md.append("| Spell | Level | School | Ritual | Casting Time | Range | Duration | Page |")
            md.append("|---|---|---|---|---|---|---|---|")
            for sp in src.spells:
                md.append(f"| {sp.name} | {sp.level or '—'} | {sp.school or '—'} | "
                          f"{'yes' if sp.ritual else '—'} | {sp.casting_time or '—'} | "
                          f"{sp.range or '—'} | {sp.duration or '—'} | "
                          f"{sp.page if sp.page is not None else '—'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/dnd5e_spell_harvest.py",
                    "system": SYSTEM, "corpus": str(corpus.base),
                    "total_spells": total, "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 6:
        print(f"'{name}' matches {len(hits)} spells; narrow with the exact name:")
        for src, sp in hits[:20]:
            print(f"  {sp.name}   [{sp.book}, p.{sp.page}]")
        return 1
    packets = []
    for src, sp in hits:
        body = [ln for ln in src.lines[sp.start:sp.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "dnd5e-spell-for-translation",
            "instructions": ("A D&D 5e spell (system: D&D 5e). Feed to the "
                             "system-translator skill for the paired 3.5e AND GURPS "
                             "treatment. The raw_block is OCR text."),
            "name": sp.name, "system": SYSTEM,
            "source": {"book": sp.book, "pdf_page": sp.page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [sp.start + 1, sp.end], "citation": src.citation},
            "parsed": {k: v for k, v in asdict(sp).items()
                       if k in ("level", "school", "ritual", "casting_time",
                                "range", "components", "duration") and v},
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


FIXTURE = """## [PDF page 40]
The spells are presented in alphabetical order.
BLADE OF DISASTER
9th-level conjuration
Casting Time: 1 bonus action
Range: 60 feet
Components: V, S
Duration: Concentration, up to 1 minute
You create a blade-shaped planar rift.

Detect Portal
1st-level divination (ritual)
Casting Time: 1 action
Range: Self
Components: V, S
Duration: Instantaneous
You sense the distance and direction to the closest planar portal.
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    lines = FIXTURE.splitlines()
    spells = detect_5e_spells(lines, _pages_for(lines), "Tasha's Cauldron of Everything (5e)")
    names = [s.name for s in spells]
    if names != ["Blade of Disaster", "Detect Portal"]:
        failures.append(f"fixture detected {names}, wanted the two 5e spells "
                        f"(ALL-CAPS name title-cased)")
    else:
        bd = spells[0]
        if (bd.level, bd.school, bd.casting_time, bd.range) != \
                ("9", "conjuration", "1 bonus action", "60 feet"):
            failures.append(f"Blade of Disaster {(bd.level, bd.school, bd.casting_time, bd.range)}")
        dp = spells[1]
        if dp.level != "1" or not dp.ritual:
            failures.append(f"Detect Portal level={dp.level!r} ritual={dp.ritual!r}, wanted 1 / True")
        if bd.system != "D&D 5e":
            failures.append("system must be 'D&D 5e'")

    if base.is_dir() and any((base / s.path).exists() for s in SOURCES):
        corpus = Corpus(base, _fresh_sources())
        total = sum(len(s.spells) for s in corpus.sources)
        if total < 60:
            failures.append(f"only {total} 5e spells indexed; expected > 60")
    else:
        print("  [SKIP] 5e extractions not found — fixture checks only")

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
        found = sorted({(sp.name, sp.book, sp.page or -1, sp.level or "—", sp.school or "")
                        for _, sp in corpus.all_spells(args.book) if q in sp.name.lower()})
        for name, bk, page, lvl, sch in found:
            loc = bk if page < 0 else f"{bk}, p.{page}"
            print(f"  {name}   [L{lvl} {sch}; {loc}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.spells for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.spells):4d} spells" if src.spells else "   0 spells"
        print(f"  {src.book:48s} {status}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} D&D 5e spells across {sum(1 for s in corpus.sources if s.spells)} book(s). "
          f"(system: {SYSTEM})")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
