#!/usr/bin/env python3
"""gurps_magic_harvest.py — collate the GURPS Magic spell list.

THE PROCESS (Chad, 2026-08-27): this is a D&D 3.5e / GURPS 4e HYBRID campaign,
and the GURPS side of the reference layer was thin — only the Basic Set and
Powers modifiers (term_harvest.py). GURPS Magic is the GURPS spell bible (~800
spells), the single biggest untouched high-value book for a fantasy game. This
script harvests it into its OWN index — GURPS spells are a different magic
system with different fields (class, cost, casting time, prerequisites) than
D&D spells, so they do not belong in spell_index.

    reference/gurps_spell_index.json  — every GURPS spell: name, class,
                                        duration, cost, casting time,
                                        prerequisites, item, book, PDF page
    reference/gurps_spell_index.md    — the same index for human eyes

The raw text stays on I:\\Sourcebooks; `--export` emits a TRANSLATOR-READY
packet on demand for the system-translator skill (which pairs a D&D 3.5e and a
GURPS treatment — here the GURPS half is already native).

WORKFLOW
    python gurps_magic_harvest.py                    # (re)build the index
    python gurps_magic_harvest.py --search "fire"    # find candidates
    python gurps_magic_harvest.py --export "Fireball"
    python gurps_magic_harvest.py --selftest

GOVERNING SOURCES
    I:\\Sourcebooks\\_text\\GURPS\\GURPS 4e\\GURPS 4e - Magic.md — the OCR
    extraction. A GURPS spell is a NAME (Title Case) followed by its CLASS
    (Regular / Area / Missile / Melee / Blocking / Special / Information /
    Enchantment / Cosmic) on its own line, then a description, then the field
    block (Duration / Cost or Base cost / Time to cast / Prerequisites / Item).
    The class word also occurs in prose, so a class line is accepted only when
    a GURPS spell FIELD follows within a short window below AND a plausible
    Title-Case name sits directly above — the same header-test discipline the
    D&D harvests use. The PDFs stand behind every extraction.

    Other GURPS spell shelves (Magic - Plant Spells, the Thaumatology books,
    Dungeon Fantasy spell lists) share this grammar and are the intended next
    Sources. A configured source whose file is missing prints NO COVERAGE.
    See docs/HARVEST_PROGRESS.md.
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
OUT_JSON = REPO / "reference" / "gurps_spell_index.json"
OUT_MD = REPO / "reference" / "gurps_spell_index.md"

PAGE = re.compile(r"\[PDF page (\d+)\]")

CLASSES = ("Regular|Area|Missile|Melee|Blocking|Special|Information|"
           "Enchantment|Cosmic")
CLASS_LINE = re.compile(rf"^({CLASSES})$")
# The difficulty marker "(VH)" / "(H)" / "(M)" / "(E)" the OCR sometimes drops
# between a spell name and its class line — skipped when finding the name.
DIFFICULTY = re.compile(r"^\((VH|H|M|E)\)$")
# The same marker often sits at the END of the name line ("Enchant (VH)"); it
# is a real GURPS attribute (Very Hard, etc.), not part of the name. Anchored at
# end-of-line so genuine parentheticals ("Repel (Animal)", "Create (Air)
# Elemental") are left alone.
NAME_DIFFICULTY = re.compile(r"^(.*?\S)\s*\((VH|H|M|E)\)\s*$")

DURATION = re.compile(r"^Duration\s*:\s*(.+)$", re.IGNORECASE)
COST = re.compile(r"^(Base cost|Cost)\s*:\s*(.+)$", re.IGNORECASE)
CASTTIME = re.compile(r"^Time to cast\s*:\s*(.+)$", re.IGNORECASE)
PREREQ = re.compile(r"^Prerequisites?\s*:\s*(.+)$", re.IGNORECASE)
ITEM = re.compile(r"^Item\s*:\s*(.+)$", re.IGNORECASE)
# A GURPS-spell-specific field proves a class line begins a real spell (these
# do not appear under a random prose "Area"/"Regular"/"Special").
SPELL_FIELD = re.compile(r"^(Duration|Base cost|Cost|Time to cast)\s*:", re.IGNORECASE)


def _plausible_name(s: str) -> bool:
    s = s.strip()
    if not (3 <= len(s) <= 40):
        return False
    if s.endswith((".", ",", ";", ":", "!", "?")):
        return False
    if s.isupper():           # a college header ("FIRE SPELLS"), not a spell
        return False
    if not s[0].isupper():
        return False
    if SPELL_FIELD.match(s) or CLASS_LINE.match(s) or PREREQ.match(s) or ITEM.match(s):
        return False
    letters = sum(c.isalpha() for c in s)
    return letters >= max(3, int(len(s) * 0.6))


@dataclass
class GurpsSpell:
    name: str
    book: str
    page: Optional[int]
    start: int
    end: int
    spell_class: Optional[str] = None      # Regular / Area / Missile / ...
    difficulty: Optional[str] = None       # VH / H / M / E (blank = Hard, the default)
    duration: Optional[str] = None
    cost: Optional[str] = None
    time_to_cast: Optional[str] = None
    prerequisites: Optional[str] = None
    item: Optional[str] = None

    def quick_fields(self) -> int:
        return sum(1 for v in (self.spell_class, self.duration, self.cost,
                               self.time_to_cast, self.prerequisites) if v)


def _field_below(lines: List[str], class_idx: int, n: int, window: int = 36) -> bool:
    """A GURPS spell FIELD within `window` content lines below the class line.
    GURPS descriptions run long, so the window is generous; the plausible-name
    requirement above the class keeps prose "Regular"/"Area" lines out."""
    j, seen = class_idx + 1, 0
    while j < n and seen < window:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            j += 1
            continue
        seen += 1
        if SPELL_FIELD.match(s):
            return True
        j += 1
    return False


def _name_above(lines: List[str], class_idx: int, limit: int = 3) -> Optional[int]:
    j, seen = class_idx - 1, 0
    while j >= 0 and seen < limit:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]) or DIFFICULTY.match(s):
            j -= 1
            continue
        seen += 1
        if _plausible_name(s):
            return j
        return None  # nearest content line above is prose/header -> not a spell
    return None


def parse_quick_fields(spell: GurpsSpell, body_lines: List[str]) -> None:
    for raw in body_lines:
        line = raw.strip()
        if not line:
            continue
        if spell.duration is None:
            m = DURATION.match(line)
            if m:
                spell.duration = m.group(1).strip()
                continue
        if spell.cost is None:
            m = COST.match(line)
            if m:
                spell.cost = m.group(2).strip()
                continue
        if spell.time_to_cast is None:
            m = CASTTIME.match(line)
            if m:
                spell.time_to_cast = m.group(1).strip()
                continue
        if spell.prerequisites is None:
            m = PREREQ.match(line)
            if m:
                spell.prerequisites = m.group(1).strip()
                continue
        if spell.item is None:
            m = ITEM.match(line)
            if m:
                spell.item = m.group(1).strip()
                continue


def detect_gurps_magic(lines: List[str], pages: List[int], book: str) -> List[GurpsSpell]:
    n = len(lines)
    starts: List[Tuple[int, str, str]] = []
    used = set()
    for i, ln in enumerate(lines):
        m = CLASS_LINE.match(ln.strip())
        if not m:
            continue
        if not _field_below(lines, i, n):
            continue
        name_idx = _name_above(lines, i)
        if name_idx is None or name_idx in used:
            continue
        used.add(name_idx)
        starts.append((name_idx, lines[name_idx].strip(), m.group(1)))

    starts.sort()
    spells: List[GurpsSpell] = []
    for k, (nm, name, cls) in enumerate(starts):
        e = starts[k + 1][0] if k + 1 < len(starts) else min(n, nm + 60)
        e = min(e, nm + 60)
        difficulty = None
        dm = NAME_DIFFICULTY.match(name)
        if dm:
            name, difficulty = dm.group(1).strip(), dm.group(2)
        spell = GurpsSpell(name=name, book=book, page=pages[nm], start=nm, end=e,
                           spell_class=cls, difficulty=difficulty)
        parse_quick_fields(spell, lines[nm + 1:e])
        spells.append(spell)

    # A GURPS spell is listed under every college it belongs to, so the same
    # spell can be detected more than once. Keep one entry per name — the
    # richest (most parsed fields), then the earliest — so the index is the
    # distinct spell list, not the per-college listing.
    best: Dict[str, GurpsSpell] = {}
    for sp in spells:
        key = sp.name.lower()
        cur = best.get(key)
        if cur is None or sp.quick_fields() > cur.quick_fields():
            best[key] = sp
    return sorted(best.values(), key=lambda s: s.start)


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[GurpsSpell]]] = {
    "gurps_magic": detect_gurps_magic,
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
    spells: List[GurpsSpell] = field(default_factory=list)


SOURCES: List[Source] = [
    Source(key="gmagic", book="GURPS Magic",
           path=Path("GURPS/GURPS 4e/GURPS 4e - Magic.md"),
           citation="GURPS Magic (SJGames, 4e), spell descriptions",
           detector="gurps_magic"),
    Source(key="plant", book="GURPS Magic: Plant Spells",
           path=Path("GURPS/GURPS 4e/GURPS 4e - Magic - Plant Spells.md"),
           citation="GURPS Magic: Plant Spells (SJGames, 4e)",
           detector="gurps_magic"),
    Source(key="urbanmagic", book="GURPS Thaumatology: Urban Magics",
           path=Path("GURPS/GURPS 4e/GURPS 4e - Thaumatology - Urban Magics.md"),
           citation="GURPS Thaumatology: Urban Magics (SJGames, 4e), ley-line spells",
           detector="gurps_magic"),
    Source(key="thaum", book="GURPS Thaumatology",
           path=Path("GURPS/GURPS 4e/GURPS 4e - Thaumatology.md"),
           citation="GURPS Thaumatology (SJGames, 4e), spells",
           detector="gurps_magic"),
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
    return [Source(**{k: getattr(s, k) for k in
                      ("key", "book", "path", "citation", "detector")})
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
        "# GURPS SPELL INDEX — The New Path",
        "",
        "**Generated by `scripts/gurps_magic_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** One row per GURPS Magic spell. This is the GURPS",
        "magic system (class / cost / casting time / prerequisites) — separate",
        "from the D&D `spell_index`, because the two systems' spells are not the",
        "same thing. The raw text stays on `I:\\Sourcebooks` — use `--export",
        "\"NAME\"` for the translator-ready packet.",
        "",
        "A field left as `—` is one the OCR did not cleanly yield.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.spells)
        parsed_well += sum(1 for sp in src.spells if sp.quick_fields() >= 3)
        sources_out.append({
            "key": src.key, "book": src.book, "citation": src.citation,
            "coverage": src.coverage,
            "spells": [asdict(sp) for sp in src.spells],
        })
        md.append(f"## {src.book} — {len(src.spells)} spells")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.spells:
            md.append("| Spell | Class | Duration | Cost | Cast time | Prerequisites | Page |")
            md.append("|---|---|---|---|---|---|---|")
            for sp in src.spells:
                pre = (sp.prerequisites or "—").replace("|", "/")
                if len(pre) > 40:
                    pre = pre[:37] + "..."
                cls = sp.spell_class or "—"
                if sp.difficulty:
                    cls = f"{cls} ({sp.difficulty})"
                md.append(f"| {sp.name} | {cls} | {sp.duration or '—'} | "
                          f"{sp.cost or '—'} | {sp.time_to_cast or '—'} | {pre} | "
                          f"{sp.page if sp.page is not None else '—'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/gurps_magic_harvest.py",
                    "corpus": str(corpus.base), "total_spells": total,
                    "sources": sources_out}, indent=1),
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
            "packet": "gurps-spell-for-translation",
            "instructions": (
                "A native GURPS 4e spell. If the system-translator skill needs a "
                "paired D&D 3.5e treatment, build the 3.5e half; the GURPS half is "
                "already here. The raw_block is OCR text; check oddities against "
                "the source PDF on I:\\Sourcebooks."
            ),
            "name": sp.name,
            "source": {"book": sp.book, "pdf_page": sp.page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [sp.start + 1, sp.end], "citation": src.citation},
            "parsed": {k: v for k, v in asdict(sp).items()
                       if k in ("spell_class", "difficulty", "duration", "cost",
                                "time_to_cast", "prerequisites", "item") and v},
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


FIXTURE = """## [PDF page 76]
energy and a small ruby worth $100.
Create Fire
Area
Fills the area of effect with fire that
requires no fuel.
Duration: 1 minute.
Base cost: 2. Half that to maintain.
Time to cast: 1 second.
Prerequisites: Ignite Fire.
Item: A staff or wand. Energy cost to create: 500.

FIRE SPELLS

Fireball
Missile
Throw a ball of fire from one hand.
Cost: Any amount up to your Magery.
Time to cast: 1 to 3 seconds.
Prerequisites: Magery 1; Create Fire, Shape Fire.

The word Regular appears here in prose and must not be read as a spell.
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    lines = FIXTURE.splitlines()
    spells = detect_gurps_magic(lines, _pages_for(lines), "GURPS Magic")
    names = [s.name for s in spells]
    if names != ["Create Fire", "Fireball"]:
        failures.append(f"fixture detected {names}, wanted ['Create Fire', 'Fireball'] "
                        f"(the FIRE SPELLS header and the prose 'Regular' rejected)")
    else:
        cf = spells[0]
        got = (cf.spell_class, cf.duration, cf.cost, cf.time_to_cast, cf.prerequisites)
        want = ("Area", "1 minute.", "2. Half that to maintain.", "1 second.", "Ignite Fire.")
        if got != want:
            failures.append(f"Create Fire fields {got}, wanted {want}")
        if cf.item is None or "staff or wand" not in cf.item:
            failures.append(f"Create Fire item={cf.item!r}, wanted the staff/wand line")
        fb = spells[1]
        if fb.spell_class != "Missile" or fb.cost != "Any amount up to your Magery.":
            failures.append(f"Fireball class={fb.spell_class!r} cost={fb.cost!r}, "
                            f"wanted Missile / Any amount up to your Magery.")

    if base.is_dir() and (base / SOURCES[0].path).exists():
        corpus = Corpus(base, _fresh_sources())
        total = sum(len(s.spells) for s in corpus.sources)
        if total < 450:
            failures.append(f"only {total} GURPS spells indexed; expected > 450")
        fb = corpus.find("fireball", book="gmagic")
        if not fb:
            failures.append("Fireball not found in live GURPS Magic")
        elif fb[0][1].spell_class != "Missile":
            failures.append(f"live Fireball class={fb[0][1].spell_class!r}, wanted Missile")
    else:
        print(f"  [SKIP] GURPS Magic extraction not found — fixture checks only")

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
        found = sorted({(sp.name, sp.book, sp.page or -1, sp.spell_class or "—")
                        for _, sp in corpus.all_spells(args.book) if q in sp.name.lower()})
        for name, bk, page, cls in found:
            loc = bk if page < 0 else f"{bk}, p.{page}"
            print(f"  {name}   [{cls}; {loc}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.spells for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.spells):5d} spells" if src.spells else "    0 spells"
        print(f"  {src.book:26s} {status}  [{src.coverage}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} GURPS spells across {sum(1 for s in corpus.sources if s.spells)} source(s); "
          f"{parsed_well} with 3+ quick fields parsed.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
