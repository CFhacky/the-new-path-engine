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
                                   binding DC, special-requirement flag, PDF page,
                                   and true full-description [start,end] span
    reference/vestige_index.md   — the same, for human eyes

GOVERNING SOURCE
    I:\\Sourcebooks\\_text\\D&D 3.5e\\Player Options\\Tome of Magic.md — the
    vestige summary table plus the explicit per-entry tablets and ALL-CAPS
    ``NAME, EPITHET`` description headings. The summary supplies an initial row;
    the tablets are the court of appeal for level/DC/requirement and recover the
    final Orthos row lost at the summary page break. Heading-to-heading spans cover
    the full descriptions on PDF pages 20–50. Native D&D 3.5e; shadow mysteries
    and truename utterances remain separate future detectors.
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


def _norm_name(s: str) -> str:
    s = s.translate(str.maketrans({"\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl"}))
    return re.sub(r"[^a-z0-9]+", " ", s.casefold()).strip()


def _pair_values(values: List[object]) -> List[object]:
    """Collapse the PDF text layer's exact duplicate rendering of tablet fields."""
    if len(values) % 2 == 0 and all(values[i] == values[i + 1]
                                     for i in range(0, len(values), 2)):
        return values[::2]
    out: List[object] = []
    for value in values:
        if not out or out[-1] != value:
            out.append(value)
    return out


def _tablet_fields(lines: List[str]) -> Dict[str, Tuple[str, int, int, bool]]:
    """Read the explicit per-entry Vestige Level / DC / Requirement tablets."""
    section_end = next(
        (i for i in range(len(lines) - 1)
         if lines[i].strip() == "PACT MAGIC"
         and lines[i + 1].strip() == "PRESTIGE CLASSES"),
        len(lines),
    )
    markers = [i for i in range(section_end) if PAGE.search(lines[i])]
    tablets: Dict[str, Tuple[str, int, int, bool]] = {}
    previous = 0
    tablet_name = re.compile(r"^[A-Z][A-Z’'\-]{2,24}$")
    for end in markers:
        region = lines[previous:end]
        names: List[str] = []
        seen = set()
        for i in range(len(region) - 1):
            name = region[i].strip()
            if (name == region[i + 1].strip() and name.isupper()
                    and tablet_name.match(name) and name not in seen):
                names.append(name.title())
                seen.add(name)
        levels = _pair_values([
            int(m.group(1)) for line in region
            if (m := re.match(r"Vestige Level:\s*([1-8])", line.strip(), re.IGNORECASE))
        ])
        dcs = _pair_values([
            int(m.group(1)) for line in region
            if (m := re.match(r"Binding DC:\s*(\d+)", line.strip(), re.IGNORECASE))
        ])
        requirements = _pair_values([
            m.group(1).casefold() == "yes" for line in region
            if (m := re.match(r"Requirement:\s*(Yes|No)", line.strip(), re.IGNORECASE))
        ])
        if names and len(names) == len(levels) == len(dcs) == len(requirements):
            for name, level, dc, requirement in zip(names, levels, dcs, requirements):
                tablets[_norm_name(name)] = (name, int(level), int(dc), bool(requirement))
        previous = end + 1
    return tablets


def _strip_vestige_tablets(seg: str) -> str:
    """Remove floated stat tablets (and their captions) from description text."""
    src = seg.splitlines()
    out: List[str] = []
    i = 0
    while i < len(src):
        text = src[i].strip()
        caption = text.casefold().startswith(("manifestation of ", "seal of "))
        probe = i
        if caption:
            probe = next((j for j in range(i + 1, min(len(src), i + 7))
                          if src[j].strip()), i)
        repeated_name = (probe + 1 < len(src) and src[probe].strip()
                         and src[probe].strip() == src[probe + 1].strip()
                         and src[probe].strip().isupper())
        if repeated_name:
            resume = next((j for j in range(probe + 2, min(len(src), probe + 45))
                           if PAGE.search(src[j])), None)
            has_fields = (resume is not None
                          and any("vestige level:" in src[j].casefold()
                                  for j in range(probe + 2, resume)))
            if has_fields:
                i = resume
                continue
        out.append(src[i])
        i += 1
    return "\n".join(out).strip()


def _description_spans(lines: List[str], pages: List[int],
                       names: List[str]) -> Dict[str, Tuple[int, int, int]]:
    """Bind each vestige to its unique ALL-CAPS ``NAME, EPITHET`` heading."""
    headers: List[Tuple[int, str]] = []
    for name in names:
        prefix = name.upper() + ","
        hits = [i for i, line in enumerate(lines)
                if line.strip().isupper() and line.strip().upper().startswith(prefix)]
        if len(hits) == 1:
            headers.append((hits[0], name))
    headers.sort()
    if not headers:
        return {}

    section_end = next(
        (i for i in range(headers[-1][0] + 1, len(lines) - 1)
         if lines[i].strip() == "PACT MAGIC"
         and lines[i + 1].strip() == "PRESTIGE CLASSES"),
        len(lines),
    )
    spans: Dict[str, Tuple[int, int, int]] = {}
    for n, (start, name) in enumerate(headers):
        end = headers[n + 1][0] if n + 1 < len(headers) else section_end
        spans[_norm_name(name)] = (start, end, pages[start])
    return spans


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
        key = _norm_name(v.name)
        cur = best.get(key)
        if cur is None or v.quick_fields() > cur.quick_fields():
            best[key] = v

    # The explicit per-entry tablets are the court of appeal for the summary
    # column dump. They also recover Orthos, whose final summary row loses its
    # level cell at the page break.
    tablets = _tablet_fields(lines)
    for key, (name, level, dc, requirement) in tablets.items():
        v = best.get(key)
        if v is None:
            v = Vestige(name=name, book=book, page=None, start=0, end=0)
            best[key] = v
        v.vestige_level = level
        v.binding_dc = dc
        v.special_requirement = requirement

    details = _description_spans(lines, pages, [v.name for v in best.values()])
    for key, v in best.items():
        detail = details.get(key)
        if detail:
            v.start, v.end, v.page = detail
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
           "Tome of Magic (WotC, 3.5e), Pact Magic — vestige summary, tablets, and descriptions pp. 20–50", "vestiges"),
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
        "met at summoning (detailed at its PDF page). Native D&D 3.5e; every row",
        "is bound to its complete book-verbatim description and granted powers.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.vestiges)
        parsed_well += sum(1 for v in src.vestiges if v.quick_fields() >= 3)
        sources_out.append({"key": src.key, "book": src.book, "citation": src.citation,
                            "coverage": src.coverage, "source_path": str(src.path),
                            "vestiges": [asdict(v) for v in src.vestiges]})
        md.append(f"## {src.book} — {len(src.vestiges)} vestiges")
        md.append("")
        md.append(f"*Source: {src.citation}.*")
        md.append(f"*Extraction: `{corpus.base / src.path}`.*")
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
        cleaned = _strip_vestige_tablets("\n".join(src.lines[v.start:v.end]))
        body = [ln for ln in cleaned.splitlines() if not PAGE.search(ln)]
        packets.append({
            "packet": "vestige-for-translation",
            "instructions": ("A D&D 3.5 pact-magic vestige (binder subsystem). The "
                             "3.5e half is here; the system-translator skill builds "
                             "the GURPS treatment. This packet includes the parsed "
                             "level/DC/requirement and the complete book-verbatim "
                             "description with all granted powers."),
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
        src = corpus.sources[0]
        ves = src.vestiges
        pages = _pages_for(src.lines)
        tablets = _tablet_fields(src.lines)
        details = _description_spans(src.lines, pages, [v.name for v in ves])
        if len(ves) != 32:
            failures.append(f"{len(ves)} vestiges indexed; expected exactly 32")
        if len(tablets) != 32:
            failures.append(f"{len(tablets)} explicit vestige tablets; expected exactly 32")
        if len(details) != 32:
            failures.append(f"{len(details)} full description headings; expected exactly 32")
        levels = {v.vestige_level for v in ves}
        if levels != set(range(1, 9)):
            failures.append(f"vestige levels {sorted(levels)} — expected the full 1..8 spread")
        tablet_mismatches = []
        for v in ves:
            tablet = tablets.get(_norm_name(v.name))
            values = (v.vestige_level, v.binding_dc, v.special_requirement)
            if not tablet or values != tablet[1:]:
                tablet_mismatches.append((v.name, values, tablet))
        if tablet_mismatches:
            failures.append(f"rows disagree with explicit tablets: {tablet_mismatches[:5]}")
        bad_spans = []
        missing_abilities = []
        tablet_artifacts = []
        for v in ves:
            head = " ".join(src.lines[v.start:min(v.end, v.start + 3)])
            raw_body = "\n".join(src.lines[v.start:v.end])
            body = _strip_vestige_tablets(raw_body)
            if v.end - v.start < 20 or _norm_name(v.name) not in _norm_name(head):
                bad_spans.append((v.name, v.start, v.end))
            if not re.search(r"Granted (?:Abilities|Powers):", body):
                missing_abilities.append(v.name)
            if "Vestige Level:" in body:
                tablet_artifacts.append(v.name)
        if bad_spans:
            failures.append(f"invalid full description spans: {bad_spans[:5]}")
        if missing_abilities:
            failures.append(f"description spans without Granted Abilities/Powers: {missing_abilities}")
        if tablet_artifacts:
            failures.append(f"cleaned descriptions retain floated tablets: {tablet_artifacts}")
        if not ves or min(v.page or 0 for v in ves) != 20 or max(v.page or 0 for v in ves) != 49:
            failures.append("live description headings did not span verified PDF pages 20–49")
        orthos = next((v for v in ves if v.name == "Orthos"), None)
        if (not orthos or orthos.page != 43
                or (orthos.vestige_level, orthos.binding_dc,
                    orthos.special_requirement) != (8, 35, True)):
            failures.append(f"live Orthos mismatch: {orthos}")
        corrected_levels = {"Marchosias": 7, "Otiax": 5, "Paimon": 3,
                            "Ronove": 1, "Savnok": 2, "Tenebrous": 4, "Zagan": 6}
        by_name = {v.name: v for v in ves}
        for name, level in corrected_levels.items():
            if name not in by_name or by_name[name].vestige_level != level:
                failures.append(f"{name} level mismatch: {by_name.get(name)}")
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
