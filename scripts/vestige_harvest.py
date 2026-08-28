#!/usr/bin/env python3
"""vestige_harvest.py — collate the D&D 3.5 pact-magic vestiges (Tome of Magic).

THE PROCESS: pact magic (the binder class) is a self-contained D&D 3.5 subsystem
the reference layer lacked entirely — a binder makes a pact with a "vestige" (the
remnant of a dead or exiled power) to gain its abilities for a day. Every vestige
is a discrete entity with a vestige level, a binding-check DC, and a special-
requirement flag, tabulated in Tome of Magic's vestige summary. That summary was
extracted from a BORN-DIGITAL PDF text layer (characters exact, not OCR — the
book is Cyrillic-free and clean), so this index is character-clean.

    reference/vestige_index.json — every vestige: name, vestige level (1-8),
                                   binding DC, special-requirement flag, PDF page
    reference/vestige_index.md   — the same, for human eyes

GOVERNING SOURCE
    I:\\Sourcebooks\\_text\\D&D 3.5e\\Player Options\\Tome of Magic.md — the
    vestige summary table (a column-dump: Vestige name, Binding DC, Special
    Requirement Yes/No, Vestige Level ordinal). The anchor is a Yes/No cell
    immediately followed by a level ordinal (1st-8th), with the DC number and the
    vestige name on the two lines above. Native D&D 3.5e; the shadow-magic
    mysteries and truename utterances in the same book are prose-embedded, not
    tabulated, and are left for a body-block detector (see HARVEST_PROGRESS).
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
OUT_JSON = REPO / "reference" / "vestige_index.json"
OUT_MD = REPO / "reference" / "vestige_index.md"

PAGE = re.compile(r"\[PDF page (\d+)\]")
DC = re.compile(r"^\d{1,2}$")
REQ = re.compile(r"^(Yes|No)$")
LEVEL = re.compile(r"^([1-8])(?:st|nd|rd|th)$")
NAMEISH = re.compile(r"^[A-Z][A-Za-z’'\-]{2,24}$")
NOT_NAME = re.compile(r"^(Vestige|Binding|Special|Requirement|Level|Table|DC|Name)\s*$",
                      re.IGNORECASE)


@dataclass
class Vestige:
    name: str
    book: str
    page: Optional[int]
    start: int
    end: int
    vestige_level: Optional[int] = None
    binding_dc: Optional[int] = None
    special_requirement: Optional[bool] = None

    def quick_fields(self) -> int:
        return sum(1 for v in (self.vestige_level, self.binding_dc,
                               self.special_requirement is not None) if v)


def detect_vestiges(lines: List[str], pages: List[int], book: str) -> List[Vestige]:
    toks = [(i, lines[i].strip()) for i in range(len(lines))
            if lines[i].strip() and not PAGE.search(lines[i])]
    out: List[Vestige] = []
    for k in range(2, len(toks) - 1):
        if not (REQ.match(toks[k][1]) and LEVEL.match(toks[k + 1][1])):
            continue
        dc = toks[k - 1][1]
        i_nm, nm = toks[k - 2]
        if not DC.match(dc) or NOT_NAME.match(nm) or not NAMEISH.match(nm):
            continue
        out.append(Vestige(
            name=nm, book=book, page=pages[i_nm], start=i_nm, end=toks[k + 1][0] + 1,
            vestige_level=int(LEVEL.match(toks[k + 1][1]).group(1)),
            binding_dc=int(dc), special_requirement=(toks[k][1] == "Yes")))

    best: Dict[str, Vestige] = {}
    for v in out:
        cur = best.get(v.name.lower())
        if cur is None or v.quick_fields() > cur.quick_fields():
            best[v.name.lower()] = v
    return sorted(best.values(), key=lambda v: (v.vestige_level or 0, v.name))


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[Vestige]]] = {
    "vestiges": detect_vestiges,
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
    vestiges: List[Vestige] = field(default_factory=list)


SOURCES: List[Source] = [
    Source("tome", "Tome of Magic (Pact Magic)",
           Path("D&D 3.5e/Player Options/Tome of Magic.md"),
           "Tome of Magic (WotC, 3.5e), Pact Magic — vestige summary", "vestiges"),
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
            src.vestiges = DETECTORS[src.detector](src.lines, pages, src.book)
            src.coverage = f"ok — {len(src.vestiges)} vestiges from {path.name}"

    def all_vestiges(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for v in src.vestiges:
                yield src, v

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, v in self.all_vestiges(book):
            nm = v.name.lower()
            if nm == q:
                exact.append((src, v))
            elif q in nm:
                partial.append((src, v))
        return exact if exact else partial


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# VESTIGE INDEX — The New Path",
        "",
        "**Generated by `scripts/vestige_harvest.py`. Do not hand-edit; rerun the",
        "harvest.** D&D 3.5 pact-magic vestiges (the binder's summonable powers),",
        "from Tome of Magic. `binding_dc` is the DC of the binding check to make",
        "the pact; a vestige with a special requirement needs some extra condition",
        "met at summoning (detailed at its PDF page). Native D&D 3.5e; the full",
        "granted-ability text is the export packet's `raw_block`.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.vestiges)
        parsed_well += sum(1 for v in src.vestiges if v.quick_fields() >= 3)
        sources_out.append({"key": src.key, "book": src.book, "citation": src.citation,
                            "coverage": src.coverage,
                            "vestiges": [asdict(v) for v in src.vestiges]})
        md.append(f"## {src.book} — {len(src.vestiges)} vestiges")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.vestiges:
            md.append("| Vestige | Level | Binding DC | Special Req. | PDF p. |")
            md.append("|---|---|---|---|---|")
            for v in src.vestiges:
                md.append(f"| {v.name} | {v.vestige_level or '—'} | "
                          f"{v.binding_dc if v.binding_dc is not None else '—'} | "
                          f"{'yes' if v.special_requirement else 'no'} | "
                          f"{v.page if v.page is not None else '—'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/vestige_harvest.py",
                    "corpus": str(corpus.base), "total_vestiges": total,
                    "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 8:
        print(f"'{name}' matches {len(hits)} vestiges; narrow with the exact name:")
        for src, v in hits[:20]:
            print(f"  {v.name}   [{v.book}, p.{v.page}]")
        return 1
    packets = []
    for src, v in hits:
        # widen to the vestige's description: from its summary row to the next few
        # hundred lines is too much; the summary row is the anchor, so hand the
        # translator the summary plus a pointer to the PDF page for the abilities.
        body = [ln for ln in src.lines[v.start:v.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "vestige-for-translation",
            "instructions": ("A D&D 3.5 pact-magic vestige (binder subsystem). The "
                             "3.5e half is here; the system-translator skill builds "
                             "the GURPS treatment. The granted abilities are in the "
                             "vestige's full entry at the cited PDF page — this row "
                             "is the summary (level, binding DC, special requirement)."),
            "name": v.name,
            "source": {"book": v.book, "pdf_page": v.page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [v.start + 1, v.end], "citation": src.citation},
            "parsed": {k: val for k, val in asdict(v).items()
                       if k in ("vestige_level", "binding_dc", "special_requirement")
                       and val is not None},
            "raw_block": "\n".join(body).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


FIXTURE = """## [PDF page 18]
Vestige
Binding DC
Special
Requirement
Level
Amon
20
Yes
1st
Aym
15
No
1st
Dahlver-Nar
17
Yes
2nd
Acererak
25
Yes
5th
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    lines = FIXTURE.splitlines()
    ves = detect_vestiges(lines, _pages_for(lines), "Tome of Magic")
    names = sorted(v.name for v in ves)
    if names != ["Acererak", "Amon", "Aym", "Dahlver-Nar"]:
        failures.append(f"fixture detected {names}, wanted the four vestiges "
                        f"(column headers must not be read as names)")
    else:
        amon = next(v for v in ves if v.name == "Amon")
        if (amon.vestige_level, amon.binding_dc, amon.special_requirement) != (1, 20, True):
            failures.append(f"Amon {(amon.vestige_level, amon.binding_dc, amon.special_requirement)}")
        aym = next(v for v in ves if v.name == "Aym")
        if aym.special_requirement is not False:
            failures.append(f"Aym special_requirement {aym.special_requirement!r}, wanted False")
        dn = next(v for v in ves if v.name == "Dahlver-Nar")
        if dn.vestige_level != 2:
            failures.append(f"Dahlver-Nar level {dn.vestige_level!r}, wanted 2 (hyphenated name)")

    if base.is_dir() and (base / SOURCES[0].path).exists():
        corpus = Corpus(base, _fresh_sources())
        ves = corpus.sources[0].vestiges
        if len(ves) < 20:
            failures.append(f"only {len(ves)} vestiges indexed; expected > 20")
        levels = {v.vestige_level for v in ves}
        if not levels.issuperset({1, 2, 3, 4, 5}):
            failures.append(f"vestige levels {sorted(levels)} — expected the full 1..8 spread")
    else:
        print("  [SKIP] Tome of Magic extraction not found — fixture checks only")

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
        found = sorted({(v.name, v.vestige_level or 0, v.binding_dc or -1,
                         bool(v.special_requirement), v.page or -1)
                        for _, v in corpus.all_vestiges(args.book) if q in v.name.lower()})
        for nm, lvl, dc, req, page in found:
            print(f"  {nm}  [level {lvl}; binding DC {dc}; "
                  f"special req {'yes' if req else 'no'}; PDF p.{page}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.vestiges for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.vestiges):4d} vestiges" if src.vestiges else "   0 vestiges"
        print(f"  {src.book:34s} {status}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} D&D 3.5 vestiges; {parsed_well} with 3+ fields parsed.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
