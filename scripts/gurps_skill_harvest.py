#!/usr/bin/env python3
"""gurps_skill_harvest.py — collate the GURPS 4e skill list.

THE PROCESS (Chad, continuing the GURPS shelf): skills are the third leg of GURPS
character-building, after advantages/disadvantages (`gurps_trait_index`) and gear
(`gurps_gear_index`). The Basic Set Trait Lists appendix tabulates every skill
with its controlling attribute, difficulty, defaults, and the book page where
it's described. That table was OCR'd as a vertical column-dump (each row's cells
one per line, with the multi-line Defaults cell interleaved around the Page cell),
so it gets its own detector and its own index.

    reference/gurps_skill_index.json — every skill: name, controlling attribute
                                       (ST/DX/IQ/HT/Will/Per), difficulty (Easy/
                                       Average/Hard/Very Hard), tech-level flag,
                                       defaults text, book page (Bxx), PDF page
    reference/gurps_skill_index.md   — the same, for human eyes

GOVERNING SOURCE
    I:\\Sourcebooks\\_text\\GURPS\\GURPS 4e\\GURPS 4e - Basic Set - Characters.md
    — the Skills portion of the Trait Lists appendix. A skill row is a NAME line,
    then the columns one per line: Attr (the controlling attribute), Diff (the
    difficulty letter), then the Defaults cell and the Page cell interleaved. The
    anchor is the Attr line immediately followed by the Diff line — a signature
    that occurs only in this table (the skill DESCRIPTIONS chapter writes the
    attribute/difficulty inline, e.g. "Acrobatics (DX/Hard)"). Native GURPS 4e
    data; the PDF stands behind every extraction.
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
OUT_JSON = REPO / "reference" / "gurps_skill_index.json"
OUT_MD = REPO / "reference" / "gurps_skill_index.md"

PAGE = re.compile(r"\[PDF page (\d+)\]")
ATTR = re.compile(r"^(ST|DX|IQ|HT|Will|Per)$")
DIFF = re.compile(r"^(E|A|H|VH)$")
BOOKPAGE = re.compile(r"^\d{2,3}$")
DIFF_NAME = {"E": "Easy", "A": "Average", "H": "Hard", "VH": "Very Hard"}
# Header / rubric lines that must never be read as a skill name.
NOT_NAME = re.compile(r"^(TRAIT LISTS|SKILLS?|Skill|Attr Diff|Attr|Diff|Defaults?|"
                      r"Page|Name|Specialties|Techniques?)\s*$", re.IGNORECASE)
FOOTNOTE = re.compile(r"[\*\u2020\u2021\u00a7\ufffd\u2660-\u2667]+\s*$")   # trailing daggers etc.


def _clean_name(s: str) -> Tuple[str, bool]:
    s = s.strip()
    s = FOOTNOTE.sub("", s).strip()
    tl = False
    if s.endswith("/TL"):
        tl = True                       # a tech-level skill (improves with TL)
    return re.sub(r"\s{2,}", " ", s), tl


@dataclass
class GurpsSkill:
    name: str
    book: str
    page: Optional[int]          # PDF page (provenance)
    start: int
    end: int
    attribute: Optional[str] = None      # ST/DX/IQ/HT/Will/Per
    difficulty: Optional[str] = None     # Easy / Average / Hard / Very Hard
    tech_level: bool = False
    defaults: Optional[str] = None
    book_page: Optional[str] = None      # Bxx page of the description

    def quick_fields(self) -> int:
        return sum(1 for v in (self.attribute, self.difficulty, self.book_page) if v)


def detect_skills(lines: List[str], pages: List[int], book: str) -> List[GurpsSkill]:
    toks = [(i, lines[i].strip()) for i in range(len(lines))
            if lines[i].strip() and not PAGE.search(lines[i])]
    # 1) collect anchor positions (Attr line then Diff line, plausible name above)
    anchors: List[int] = []
    for k in range(1, len(toks) - 2):
        if not (ATTR.match(toks[k][1]) and DIFF.match(toks[k + 1][1])):
            continue
        nm = toks[k - 1][1]
        if NOT_NAME.match(nm) or not re.search(r"[A-Za-z]", nm) or len(nm) < 3:
            continue
        anchors.append(k)

    out: List[GurpsSkill] = []
    for a, k in enumerate(anchors):
        i_nm, raw_name = toks[k - 1]
        attr = toks[k][1]
        diff = toks[k + 1][1]
        # the block runs from this name up to the next anchor's name
        stop = (anchors[a + 1] - 1) if a + 1 < len(anchors) else min(len(toks), k + 8)
        block = toks[k + 2:stop]
        page_val: Optional[str] = None
        default_bits: List[str] = []
        for _, cell in block:
            if page_val is None and BOOKPAGE.match(cell):
                page_val = cell
            else:
                default_bits.append(cell)
        name, tl = _clean_name(raw_name)
        defaults = re.sub(r"\s+", " ", " ".join(default_bits)).strip(" ,;") or None
        out.append(GurpsSkill(
            name=name, book=book, page=pages[i_nm], start=i_nm,
            end=(toks[stop][0] if a + 1 < len(anchors) else min(len(lines), i_nm + 8)),
            attribute=attr, difficulty=DIFF_NAME[diff], tech_level=tl,
            defaults=defaults, book_page=(f"B{page_val}" if page_val else None)))

    best: Dict[str, GurpsSkill] = {}
    for sk in out:
        key = sk.name.lower()
        cur = best.get(key)
        if cur is None or sk.quick_fields() > cur.quick_fields():
            best[key] = sk
    return sorted(best.values(), key=lambda s: s.start)


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[GurpsSkill]]] = {
    "skills": detect_skills,
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
    skills: List[GurpsSkill] = field(default_factory=list)


SOURCES: List[Source] = [
    Source("basicset", "GURPS Basic Set: Characters",
           Path("GURPS/GURPS 4e/GURPS 4e - Basic Set - Characters.md"),
           "GURPS Basic Set: Characters (SJGames, 4e), Skills in the Trait Lists appendix",
           "skills"),
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
            src.skills = DETECTORS[src.detector](src.lines, pages, src.book)
            src.coverage = f"ok — {len(src.skills)} skills from {path.name}"

    def all_skills(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for sk in src.skills:
                yield src, sk

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, sk in self.all_skills(book):
            nm = sk.name.lower()
            if nm == q:
                exact.append((src, sk))
            elif q in nm:
                partial.append((src, sk))
        return exact if exact else partial


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# GURPS SKILL INDEX — The New Path",
        "",
        "**Generated by `scripts/gurps_skill_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** GURPS 4e skills (native GURPS 4e), from the Basic",
        "Set Trait Lists appendix. `attribute` is the controlling attribute and",
        "`difficulty` its Easy/Average/Hard/Very Hard rating; `defaults` lists the",
        "skills/attributes it defaults from; `book_page` (Bxx) points to the full",
        "description. A field left `—` is one the OCR did not cleanly yield.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.skills)
        parsed_well += sum(1 for s in src.skills if s.quick_fields() >= 3)
        sources_out.append({"key": src.key, "book": src.book, "citation": src.citation,
                            "coverage": src.coverage,
                            "skills": [asdict(s) for s in src.skills]})
        md.append(f"## {src.book} — {len(src.skills)} skills")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.skills:
            md.append("| Skill | Attr | Difficulty | TL | Defaults | Book p. | PDF p. |")
            md.append("|---|---|---|---|---|---|---|")
            for s in src.skills:
                md.append(f"| {s.name} | {s.attribute or '—'} | {s.difficulty or '—'} | "
                          f"{'✓' if s.tech_level else '—'} | {s.defaults or '—'} | "
                          f"{s.book_page or '—'} | {s.page if s.page is not None else '—'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/gurps_skill_harvest.py",
                    "corpus": str(corpus.base), "total_skills": total,
                    "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 8:
        print(f"'{name}' matches {len(hits)} skills; narrow with the exact name:")
        for src, sk in hits[:20]:
            print(f"  {sk.name}   [{sk.book}, p.{sk.page}]")
        return 1
    packets = []
    for src, sk in hits:
        body = [ln for ln in src.lines[sk.start:sk.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "gurps-skill-for-translation",
            "instructions": ("A native GURPS 4e skill. The GURPS half is here; the "
                             "system-translator skill builds the D&D 3.5e treatment "
                             "(the matching skill / class skill, as fits). The full "
                             "rules text is at the cited book page."),
            "name": sk.name,
            "source": {"book": sk.book, "pdf_page": sk.page, "book_page": sk.book_page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [sk.start + 1, sk.end], "citation": src.citation},
            "parsed": {k: v for k, v in asdict(sk).items()
                       if k in ("attribute", "difficulty", "tech_level", "defaults",
                                "book_page") and v not in (None, False)},
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


FIXTURE = """## [PDF page 301]
TRAIT LISTS
Skill
Attr Diff
Defaults
Page
Accounting
IQ
H
IQ-6, Finance-4,
174
Mathematics (Statistics)-5,
Merchant-5
Acrobatics
DX
H
DX-6
174
Airshipman/TL
IQ
E
IQ-4
185
Alchemy/TL
IQ
VH
None
174
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    lines = FIXTURE.splitlines()
    skills = detect_skills(lines, _pages_for(lines), "GURPS Basic Set: Characters")
    names = [s.name for s in skills]
    want = ["Accounting", "Acrobatics", "Airshipman/TL", "Alchemy/TL"]
    if names != want:
        failures.append(f"fixture detected {names}, wanted {want} "
                        f"(column headers must not be read as names)")
    else:
        acc = skills[0]
        if (acc.attribute, acc.difficulty, acc.book_page) != ("IQ", "Hard", "B174"):
            failures.append(f"Accounting row {(acc.attribute, acc.difficulty, acc.book_page)}")
        if "Mathematics (Statistics)-5" not in (acc.defaults or ""):
            failures.append(f"Accounting defaults dropped the wrapped continuation: {acc.defaults!r}")
        air = skills[2]
        if not air.tech_level or air.attribute != "IQ":
            failures.append(f"Airshipman/TL tech_level={air.tech_level} attr={air.attribute}")
        alc = skills[3]
        if alc.difficulty != "Very Hard":
            failures.append(f"Alchemy difficulty {alc.difficulty!r}, wanted 'Very Hard'")

    if base.is_dir() and (base / SOURCES[0].path).exists():
        corpus = Corpus(base, _fresh_sources())
        skills = corpus.sources[0].skills
        if len(skills) < 150:
            failures.append(f"only {len(skills)} skills indexed; expected > 150")
        acro = corpus.find("acrobatics", book="basicset")
        if not acro:
            failures.append("Acrobatics not found in live Basic Set")
        elif acro[0][1].attribute != "DX":
            failures.append(f"Acrobatics attribute {acro[0][1].attribute!r}, wanted 'DX'")
    else:
        print("  [SKIP] Basic Set extraction not found — fixture checks only")

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
        found = sorted({(sk.name, sk.attribute or "—", sk.difficulty or "—",
                         sk.book_page or "—", sk.page or -1)
                        for _, sk in corpus.all_skills(args.book) if q in sk.name.lower()})
        for nm, attr, diff, bp, page in found:
            print(f"  {nm}  [{attr}/{diff}; {bp}; PDF p.{page}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.skills for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.skills):4d} skills" if src.skills else "   0 skills"
        print(f"  {src.book:34s} {status}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} GURPS skills; {parsed_well} with 3+ fields parsed.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
