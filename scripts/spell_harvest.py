#!/usr/bin/env python3
"""spell_harvest.py — collate D&D 3.5e spells into a browsable index.

THE PROCESS (companion to term_harvest.py, creature_harvest.py,
item_harvest.py, power_harvest.py, maneuver_harvest.py, and feat_harvest.py):
`spell_lookup.py` retrieves one spell's full text for play, but there is no
spell INDEX — the browsable, translator-ready collation the other reference
families carry. This builds it, completing the reference layer (creatures,
items, feats, powers, maneuvers, and now spells each have both a lookup and an
index).

    reference/spell_index.json  — every spell: name, school, subschool /
                                  descriptor, level list, book, PDF page,
                                  parsed where clean
    reference/spell_index.md    — the same index for human eyes, by book

The bundled SRD core spells (spells_srd35.json) carry their own text; the Spell
Compendium keeps its raw text on I:\\Sourcebooks and is pulled on demand.
`--export` emits a TRANSLATOR-READY PACKET for the `system-translator` skill's
paired 3.5e + GURPS build.

WORKFLOW
    python spell_harvest.py                        # (re)build the index
    python spell_harvest.py --search "orb"         # find candidates
    python spell_harvest.py --export "Fireball"
        -> JSON packet -> feed to the system-translator skill
    python spell_harvest.py --selftest

GOVERNING SOURCES
    1. spells_srd35.json — the bundled SRD 3.5 core spells (Open Game Content),
       the same file spell_lookup.py ships (605 spells). SRD wins name
       collision.
    2. I:\\Sourcebooks\\_text\\D&D 3.5e\\Magic and Items\\Spell Compendium
       (Premium).md — the OCR extraction. A spell header is an ALL-CAPS name
       (which may WRAP across the column break) followed by a school line and a
       "Level:" line — the same three-line test spell_lookup.py uses, here
       anchored on the school line so a wrapped name is joined once rather than
       double-counted.

    Detection is a deliberate sibling of power_harvest.py's (school-anchored,
    name gathered above), duplicated rather than imported per the repo law. A
    configured source whose file is missing prints NO COVERAGE and is never
    improvised. See docs/HARVEST_PROGRESS.md.
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
SRD_JSON = REPO / "scripts" / "spells_srd35.json"
OUT_JSON = REPO / "reference" / "spell_index.json"
OUT_MD = REPO / "reference" / "spell_index.md"

# ---------------------------------------------------------------------------
# Grammar
# ---------------------------------------------------------------------------

PAGE = re.compile(r"\[PDF page (\d+)\]")
SCHOOLS = ("Abjuration|Conjuration|Divination|Enchantment|Evocation|Illusion|"
           "Necromancy|Transmutation|Universal")
SCHOOL_ANCHOR = re.compile(rf"^({SCHOOLS})\b(.*)$")
LEVEL = re.compile(r"^Level\s*:\s*(.+)$", re.IGNORECASE)
# An ALL-CAPS spell name (or one fragment of a wrapped one). SRD names are
# Title Case, handled separately.
CAPS_NAME = re.compile(r"^[A-Z][A-Z0-9 ,'’\-/]{1,52}$")
BRACKET_DESC = re.compile(r"^\[[^\]]*\]$")
# A running page header the OCR drops above a spell name, wrapped across three
# lines ("CHAPTER 1" / "SPELL" / "DESCRIPTIONS"). Each matches CAPS_NAME, so the
# name-gather must stop at it. Matched as standalone header tokens so real names
# that merely start with the word ("SPELL TURNING", "TABLE") are NOT rejected.
HEADER_REJECT = re.compile(
    r"^(CHAPTER\b|SPELL$|DESCRIPTIONS$|SPELL DESCRIPTIONS$|APPENDIX\b|"
    r"CONTENTS$|INDEX$|TABLE OF\b|INTRODUCTION$|GLOSSARY$)", re.IGNORECASE)


@dataclass
class Spell:
    name: str
    book: str
    page: Optional[int]
    start: int  # line span in the extraction (0 for SRD entries)
    end: int
    school: Optional[str] = None
    subschool: Optional[str] = None     # "(Creation) [Acid]" etc.
    level: Optional[str] = None         # the class-and-level list
    srd_text: Optional[str] = None      # bundled text for SRD spells; None otherwise

    def quick_fields(self) -> int:
        return sum(1 for v in (self.school, self.level) if v)


# ---------------------------------------------------------------------------
# Compendium detector (school-anchored, name gathered above)
# ---------------------------------------------------------------------------


def _has_level_below(lines: List[str], school_idx: int, n: int, window: int = 4) -> bool:
    j, seen = school_idx + 1, 0
    while j < n and seen < window:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            j += 1
            continue
        seen += 1
        if LEVEL.match(s):
            return True
        j += 1
    return False


def _gather_name_up(lines: List[str], school_idx: int) -> Optional[Tuple[int, str]]:
    frags: List[str] = []
    top = school_idx
    j, gap = school_idx - 1, 0
    while j >= 0 and len(frags) < 4:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            gap += 1
            if gap > 2:
                break
            j -= 1
            continue
        if HEADER_REJECT.search(s):  # a running page header sits above the name
            break
        if CAPS_NAME.match(s) and not SCHOOL_ANCHOR.match(s) and not LEVEL.match(s):
            frags.append(s)
            top, gap = j, 0
            j -= 1
            continue
        break
    if not frags:
        return None
    frags.reverse()
    return top, re.sub(r"\s+", " ", " ".join(frags)).strip().title()


def _level_below(lines: List[str], school_idx: int, n: int, window: int = 5) -> Optional[str]:
    j, seen = school_idx + 1, 0
    while j < n and seen < window:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            j += 1
            continue
        seen += 1
        m = LEVEL.match(s)
        if m:
            return re.sub(r"\s+", " ", m.group(1)).strip()
        j += 1
    return None


def detect_compendium(lines: List[str], pages: List[int], book: str) -> List[Spell]:
    n = len(lines)
    starts: List[Tuple[int, int, str, str, Optional[str]]] = []
    used = set()
    for i, ln in enumerate(lines):
        m = SCHOOL_ANCHOR.match(ln.strip())
        if not m:
            continue
        if not _has_level_below(lines, i, n):
            continue
        got = _gather_name_up(lines, i)
        if got is None or got[0] in used:
            continue
        top, name = got
        used.add(top)
        # subschool/descriptor: the rest of the school line, plus a following
        # "[Descriptor]" line the OCR wrapped onto its own line.
        sub = m.group(2).strip()
        k = i + 1
        while k < n and (lines[k].strip() == "" or PAGE.search(lines[k])):
            k += 1
        if k < n and BRACKET_DESC.match(lines[k].strip()):
            sub = (sub + " " + lines[k].strip()).strip()
        starts.append((top, i, name, m.group(1), sub or None))

    starts.sort()
    spells: List[Spell] = []
    for idx, (top, school_idx, name, school, sub) in enumerate(starts):
        e = starts[idx + 1][0] if idx + 1 < len(starts) else min(n, top + 90)
        e = min(e, top + 90)
        spell = Spell(name=name, book=book, page=pages[top], start=top, end=e,
                      school=school, subschool=sub,
                      level=_level_below(lines, school_idx, n))
        spells.append(spell)
    return spells


# ---------------------------------------------------------------------------
# SRD source (bundled JSON)
# ---------------------------------------------------------------------------


def _parse_srd_fields(text: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    school = subschool = level = None
    for raw in text.splitlines():
        s = raw.strip()
        if not s:
            continue
        if school is None:
            m = SCHOOL_ANCHOR.match(s)
            if m:
                school = m.group(1)
                subschool = m.group(2).strip() or None
                continue
        m2 = LEVEL.match(s)
        if m2:
            level = re.sub(r"\s+", " ", m2.group(1)).strip()
            break
    return school, subschool, level


def load_srd(path: Path) -> List[Spell]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    spells: List[Spell] = []
    for entry in data.values():
        school, subschool, level = _parse_srd_fields(entry.get("text", ""))
        spells.append(Spell(name=entry["name"], book="SRD 3.5", page=None,
                            start=0, end=0, school=school, subschool=subschool,
                            level=level, srd_text=entry.get("text", "")))
    return spells


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[Spell]]] = {
    "compendium": detect_compendium,
}


@dataclass
class Source:
    key: str
    book: str
    path: Optional[Path]      # None for the bundled SRD source
    citation: str
    detector: str             # "compendium" | "srd"
    coverage: str = "pending"
    lines: List[str] = field(default_factory=list)
    spells: List[Spell] = field(default_factory=list)


SOURCES: List[Source] = [
    Source(key="srd", book="SRD 3.5", path=None,
           citation="SRD 3.5 core spells (Open Game Content), bundled",
           detector="srd"),
    Source(key="compendium", book="Spell Compendium",
           path=Path("D&D 3.5e/Magic and Items/Spell Compendium (Premium).md"),
           citation="Spell Compendium (WotC, 2005), spell descriptions",
           detector="compendium"),
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
            if src.detector == "srd":
                src.spells = load_srd(SRD_JSON)
                src.coverage = (f"ok — {len(src.spells)} SRD spells"
                                if src.spells else f"NO COVERAGE — SRD JSON missing: {SRD_JSON}")
                continue
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
            n = sp.name.lower()
            if n == q:
                exact.append((src, sp))
            elif q in n:
                partial.append((src, sp))
        return exact if exact else partial


# ---------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# SPELL INDEX — The New Path",
        "",
        "**Generated by `scripts/spell_harvest.py`. Do not hand-edit; rerun",
        "the harvest.** One row per spell: the bundled SRD 3.5 core spells plus",
        "every spell in the Spell Compendium extraction. The Compendium raw",
        "text stays on `I:\\Sourcebooks` — use `python scripts/spell_harvest.py",
        "--export \"NAME\"` to emit the translator-ready packet for any row.",
        "",
        "For the full spell text in play, `spell_lookup.py` is the retrieval",
        "sibling. Every entry names its book; Compendium entries carry the PDF",
        "page. A field left as `—` is one the OCR did not cleanly yield.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.spells)
        parsed_well += sum(1 for sp in src.spells if sp.quick_fields() >= 2)
        sources_out.append({
            "key": src.key,
            "book": src.book,
            "citation": src.citation,
            "coverage": src.coverage,
            "spells": [{k: v for k, v in asdict(sp).items() if k != "srd_text"}
                       for sp in src.spells],
        })
        md.append(f"## {src.book} — {len(src.spells)} spells")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.spells:
            md.append("| Spell | School | Subschool / Descriptor | Level | Page |")
            md.append("|---|---|---|---|---|")
            for sp in src.spells:
                lvl = (sp.level or "—").replace("|", "/")
                if len(lvl) > 40:
                    lvl = lvl[:37] + "..."
                md.append(f"| {sp.name} | {sp.school or '—'} | {sp.subschool or '—'} | "
                          f"{lvl} | {sp.page if sp.page is not None else '—'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps(
            {
                "generated_by": "scripts/spell_harvest.py",
                "corpus": str(corpus.base),
                "total_spells": total,
                "sources": sources_out,
            },
            indent=1,
        ),
        encoding="utf-8",
    )
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 6:
        print(f"'{name}' matches {len(hits)} spells; narrow with --book or the exact name:")
        for src, sp in hits[:20]:
            print(f"  {sp.name}   [{sp.book}{'' if sp.page is None else ', p.' + str(sp.page)}]")
        return 1
    packets = []
    for src, sp in hits:
        if sp.srd_text is not None:
            raw = sp.srd_text
        else:
            body = [ln for ln in src.lines[sp.start:sp.end] if not PAGE.search(ln)]
            raw = re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip()
        packets.append({
            "packet": "spell-for-translation",
            "instructions": (
                "Feed this packet to the system-translator skill. Both a 3.5e "
                "AND a GURPS treatment are required in the output — a conversion "
                "missing either system is incomplete (that skill's own rule). "
                "The raw_block is OCR text (SRD entries are clean OGC); check "
                "oddities against the source PDF on I:\\Sourcebooks."
            ),
            "name": sp.name,
            "source": {
                "book": sp.book, "pdf_page": sp.page,
                "extraction": None if sp.srd_text is not None else str(corpus.base / src.path),
                "lines": None if sp.srd_text is not None else [sp.start + 1, sp.end],
            },
            "parsed": {k: v for k, v in asdict(sp).items()
                       if k in ("school", "subschool", "level") and v},
            "raw_block": raw,
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


# ---------------------------------------------------------------------------
# Selftest
# ---------------------------------------------------------------------------

FIXTURE = """## [PDF page 8]
ABSORB WEAPON

Transmutation

Level: Assassin 2

Casting Time: 1 standard action

You cause a weapon to meld into your arm.

ACCELERATED
MOVEMENT

Transmutation

Level: Bard 1, ranger 1

You move at full speed while balancing.

CHAPTER 1
SPELL
DESCRIPTIONS
ACID BREATH

Conjuration (Creation) [Acid]

Level: Sorcerer/wizard 3

You breathe a cone of acid.
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "D&D 3.5e" / "Magic and Items").mkdir(parents=True)
        (d / "D&D 3.5e" / "Magic and Items" / "Spell Compendium (Premium).md").write_text(
            FIXTURE, encoding="utf-8")
        pages = _pages_for(FIXTURE.splitlines())
        spells = detect_compendium(FIXTURE.splitlines(), pages, "Spell Compendium")
        names = [sp.name for sp in spells]
        # The wrapped "ACCELERATED MOVEMENT" name must join to one spell, not
        # split into two headers.
        if names != ["Absorb Weapon", "Accelerated Movement", "Acid Breath"]:
            failures.append(f"fixture detected {names}, wanted the three spells "
                            f"(Accelerated Movement joined from its wrapped name)")
        else:
            ab = spells[0]
            if ab.school != "Transmutation" or ab.level != "Assassin 2":
                failures.append(f"Absorb Weapon school={ab.school!r} level={ab.level!r}, "
                                f"wanted Transmutation / Assassin 2")
            acid = spells[2]
            if acid.school != "Conjuration" or acid.subschool != "(Creation) [Acid]" \
                    or acid.level != "Sorcerer/wizard 3":
                failures.append(f"Acid Breath school={acid.school!r} sub={acid.subschool!r} "
                                f"level={acid.level!r}, wanted Conjuration / (Creation) "
                                f"[Acid] / Sorcerer/wizard 3")

    srd = load_srd(SRD_JSON)
    if not srd:
        print(f"  [SKIP] SRD spell JSON not found: {SRD_JSON}")
    else:
        if len(srd) < 500:
            failures.append(f"only {len(srd)} SRD spells loaded; expected >= 500")
        fb = next((s for s in srd if s.name.lower() == "fireball"), None)
        if fb is None or fb.school != "Evocation" or fb.level != "Sor/Wiz 3":
            failures.append(f"Fireball SRD parse school={getattr(fb,'school',None)!r} "
                            f"level={getattr(fb,'level',None)!r}, wanted Evocation / Sor/Wiz 3")

    comp_path = base / SOURCES[1].path
    if comp_path.exists():
        corpus = Corpus(base, _fresh_sources())
        comp = next(s for s in corpus.sources if s.key == "compendium")
        if len(comp.spells) < 900:
            failures.append(f"only {len(comp.spells)} Compendium spells; expected > 900")
        orb = corpus.find("orb of acid", book="compendium")
        if not orb:
            failures.append("Orb of Acid not found in live Compendium")
    else:
        print(f"  [SKIP] Compendium extraction not found: {comp_path} — fixture + SRD only")

    for failure in failures:
        print(f"SELFTEST FAIL: {failure}")
    print("selftest: " + ("PASS" if not failures else f"{len(failures)} failure(s)"))
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--corpus", type=Path, default=CORPUS)
    ap.add_argument("--search", metavar="TEXT", help="substring search on names")
    ap.add_argument("--book", help="restrict to one source (srd, compendium)")
    ap.add_argument("--export", metavar="NAME", help="emit a translator-ready packet")
    ap.add_argument("--out", type=Path, help="write the packet here instead of stdout")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest(args.corpus)

    corpus = Corpus(args.corpus, _fresh_sources())

    if args.search:
        q = args.search.lower()
        found = sorted({(sp.name, sp.book, sp.page if sp.page is not None else -1,
                         sp.level or "—")
                        for _, sp in corpus.all_spells(args.book) if q in sp.name.lower()})
        for name, book, page, level in found:
            loc = book if page < 0 else f"{book}, p.{page}"
            print(f"  {name}   [{level}; {loc}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.spells for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.spells):5d} spells" if src.spells else "    0 spells"
        print(f"  {src.book:22s} {status}  [{src.coverage}]")
    if not any_ok:
        print("\nNothing harvested at all — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} spells across {sum(1 for s in corpus.sources if s.spells)} source(s); "
          f"{parsed_well} with school+level parsed.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
