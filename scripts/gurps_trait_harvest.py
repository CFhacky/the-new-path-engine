#!/usr/bin/env python3
"""gurps_trait_harvest.py — collate the GURPS 4e advantage/disadvantage lists.

THE PROCESS (Chad, continuing the GURPS shelf): advantages and disadvantages are
the heart of GURPS character-building — the point-buy traits every GURPS build is
made of — and the reference layer had the GURPS spells, creatures, gear, and
modifiers but NOT the traits. The Basic Set closes with a TRAIT LISTS appendix
that tabulates every advantage and disadvantage with its type, exotic/supernatural
flag, point cost, and the book page where it's described. That appendix was OCR'd
as a vertical column-dump (each row's cells one per line), so it gets its own
detector and its own index.

    reference/gurps_trait_index.json — every advantage/disadvantage: name,
                                       category, mental/physical/social, exotic/
                                       supernatural, point cost, book page (Bxx),
                                       PDF page
    reference/gurps_trait_index.md   — the same, for human eyes

Skills are a DIFFERENT appendix with a different column shape (Skill / difficulty
/ default) and are left for a dedicated detector — see docs/HARVEST_PROGRESS.md.

GOVERNING SOURCE
    I:\\Sourcebooks\\_text\\GURPS\\GURPS 4e\\GURPS 4e - Basic Set - Characters.md
    — the TRAIT LISTS appendix. A trait row is a NAME line, then the columns one
    per line: M/P/Soc (mental/physical/social), X/Sup (exotic/supernatural, or a
    dash for mundane), Cost, Page. The anchor is the M/P/Soc line immediately
    followed by the X/Sup line — a signature that does not occur in prose.
    Advantage vs. disadvantage is set by the most recent ADVANTAGES /
    DISADVANTAGES section header. This is native GURPS 4e data; the PDF stands
    behind every extraction.
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
OUT_JSON = REPO / "reference" / "gurps_trait_index.json"
OUT_MD = REPO / "reference" / "gurps_trait_index.md"

PAGE = re.compile(r"\[PDF page (\d+)\]")
TYPE = re.compile(r"^(M|P|Soc)(?:/(M|P|Soc)){0,2}$")            # M, P, Soc, M/P, ...
XSUP = re.compile(r"^(X|Sup|[—–\-\u2013\u2014\ufffd])$")        # exotic / super / mundane dash
BOOKPAGE = re.compile(r"^\d{1,3}$")
# GURPS trait costs come in many shapes: "25", "2/level", "-10*" (self-control),
# "Variable", "5 or 10/level", "3, 5, or 8/level", "10+", "1 to 10", "1 or
# 2/culture". Validate by shape: the word Variable/varies/*, or something that
# contains a digit and, once the cost words are stripped, only cost punctuation.
_COST_WORDS = re.compile(r"\b(or|to|per|level|culture|point|points|pts)\b", re.IGNORECASE)


def _is_cost(s: str) -> bool:
    low = s.strip().lower()
    if low in ("variable", "varies", "*"):
        return True
    if not re.search(r"\d", s):
        return False
    stripped = _COST_WORDS.sub("", low)
    return bool(re.fullmatch(r"[\d\s/+*.,\-\u2013\u2014]+", stripped))
# Column headers / rubric lines that must never be read as a trait name.
NOT_NAME = re.compile(
    r"^(TRAIT LISTS|ADVANTAGES?|DISADVANTAGES?|PERKS?|QUIRKS?|SKILLS?|Advantage|"
    r"Disadvantage|Perk|Quirk|Skill|Cost|Page|M/P/Soc.*|X/Sup|Name)\s*$")

MPS = {"M": "mental", "P": "physical", "Soc": "social"}


def _decode_type(s: str) -> str:
    return "/".join(MPS.get(p, p) for p in s.split("/"))


def _decode_xsup(s: str) -> str:
    if s == "X":
        return "exotic"
    if s == "Sup":
        return "supernatural"
    return "mundane"


@dataclass
class GurpsTrait:
    name: str
    book: str
    page: Optional[int]          # PDF page (provenance)
    start: int
    end: int
    category: str                # "advantage" | "disadvantage"
    kind: Optional[str] = None   # mental / physical / social
    nature: Optional[str] = None  # exotic / supernatural / mundane
    cost: Optional[str] = None   # point cost as printed ("25", "2/level", "-10", "varies")
    book_page: Optional[str] = None  # the Bxx page where it's described

    def quick_fields(self) -> int:
        return sum(1 for v in (self.kind, self.nature, self.cost, self.book_page) if v)


def _clean_name(s: str) -> str:
    s = s.strip().strip("*").strip()
    # collapse the leading garbage some OCR rows carry, keep the visible name
    return re.sub(r"\s{2,}", " ", s)


def detect_traits(lines: List[str], pages: List[int], book: str) -> List[GurpsTrait]:
    # The list was OCR'd as a column-dump with no blank lines between cells. Work
    # on the non-blank/non-page tokens; anchor on the M/P/Soc + X/Sup pair.
    toks = [(i, lines[i].strip()) for i in range(len(lines))
            if lines[i].strip() and not PAGE.search(lines[i])]
    out: List[GurpsTrait] = []
    category = "advantage"
    for k in range(1, len(toks) - 3):
        _, tline = toks[k]
        up = tline.upper()
        if up.startswith("DISADVANTAGE"):
            category = "disadvantage"
            continue
        if up == "ADVANTAGES" or up == "ADVANTAGE":
            category = "advantage"
            continue
        # No SKILL break: the Name/M-P-Soc/X-Sup/Cost/Page signature does not occur
        # in the Skills appendix (different columns) or in prose, so scanning past
        # them is harmless — and an early break on the main-body Skills chapter
        # would stop before the Trait Lists appendix is ever reached.
        if not (TYPE.match(tline) and XSUP.match(toks[k + 1][1])):
            continue
        i_nm, nm = toks[k - 1]
        _, cost = toks[k + 2]
        _, bpage = toks[k + 3]
        if NOT_NAME.match(nm) or not _is_cost(cost) or not BOOKPAGE.match(bpage):
            continue
        if not re.search(r"[A-Za-z]", nm):
            continue
        cat = category
        if cost.startswith(("-", "\u2013", "\u2014")):
            cat = "disadvantage"          # negative cost confirms a disadvantage
        out.append(GurpsTrait(
            name=_clean_name(nm), book=book, page=pages[i_nm], start=i_nm,
            end=toks[k + 3][0] + 1, category=cat, kind=_decode_type(tline),
            nature=_decode_xsup(toks[k + 1][1]), cost=cost, book_page=f"B{bpage}"))

    best: Dict[str, GurpsTrait] = {}
    for tr in out:
        key = (tr.category, tr.name.lower())
        cur = best.get(key)
        if cur is None or tr.quick_fields() > cur.quick_fields():
            best[key] = tr
    return sorted(best.values(), key=lambda t: t.start)


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[GurpsTrait]]] = {
    "traits": detect_traits,
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
    traits: List[GurpsTrait] = field(default_factory=list)


SOURCES: List[Source] = [
    Source("basicset", "GURPS Basic Set: Characters",
           Path("GURPS/GURPS 4e/GURPS 4e - Basic Set - Characters.md"),
           "GURPS Basic Set: Characters (SJGames, 4e), Trait Lists appendix",
           "traits"),
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
            src.traits = DETECTORS[src.detector](src.lines, pages, src.book)
            src.coverage = f"ok — {len(src.traits)} traits from {path.name}"

    def all_traits(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for tr in src.traits:
                yield src, tr

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, tr in self.all_traits(book):
            nm = tr.name.lower()
            if nm == q:
                exact.append((src, tr))
            elif q in nm:
                partial.append((src, tr))
        return exact if exact else partial


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# GURPS TRAIT INDEX — The New Path",
        "",
        "**Generated by `scripts/gurps_trait_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** GURPS 4e advantages and disadvantages (native GURPS",
        "4e), from the Basic Set Trait Lists appendix. `cost` is the point cost as",
        "printed; `book_page` (Bxx) points to the full description; a field left",
        "`—` is one the OCR did not cleanly yield. Use `--export \"NAME\"` for a",
        "translator packet.",
        "",
    ]
    for src in corpus.sources:
        adv = [t for t in src.traits if t.category == "advantage"]
        dis = [t for t in src.traits if t.category == "disadvantage"]
        total += len(src.traits)
        parsed_well += sum(1 for t in src.traits if t.quick_fields() >= 3)
        sources_out.append({"key": src.key, "book": src.book, "citation": src.citation,
                            "coverage": src.coverage,
                            "advantages": len(adv), "disadvantages": len(dis),
                            "traits": [asdict(t) for t in src.traits]})
        md.append(f"## {src.book} — {len(adv)} advantages, {len(dis)} disadvantages")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        for label, group in (("Advantages", adv), ("Disadvantages", dis)):
            if not group:
                continue
            md.append(f"### {label} ({len(group)})")
            md.append("")
            md.append("| Trait | Type | Nature | Cost | Book p. | PDF p. |")
            md.append("|---|---|---|---|---|---|")
            for t in group:
                md.append(f"| {t.name} | {t.kind or '—'} | {t.nature or '—'} | "
                          f"{t.cost or '—'} | {t.book_page or '—'} | "
                          f"{t.page if t.page is not None else '—'} |")
            md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/gurps_trait_harvest.py",
                    "corpus": str(corpus.base), "total_traits": total,
                    "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 8:
        print(f"'{name}' matches {len(hits)} traits; narrow with the exact name:")
        for src, tr in hits[:20]:
            print(f"  {tr.name} ({tr.category})   [{tr.book}, p.{tr.page}]")
        return 1
    packets = []
    for src, tr in hits:
        body = [ln for ln in src.lines[tr.start:tr.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "gurps-trait-for-translation",
            "instructions": ("A native GURPS 4e advantage/disadvantage. The GURPS "
                             "half is here (point-buy trait); the system-translator "
                             "skill builds the D&D 3.5e treatment (feat / template / "
                             "flaw / racial trait, as fits). The full rules text is at "
                             "the cited book page; this table row gives the summary."),
            "name": tr.name, "category": tr.category,
            "source": {"book": tr.book, "pdf_page": tr.page, "book_page": tr.book_page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [tr.start + 1, tr.end], "citation": src.citation},
            "parsed": {k: v for k, v in asdict(tr).items()
                       if k in ("category", "kind", "nature", "cost", "book_page") and v},
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


FIXTURE = """## [PDF page 300]
TRAIT LISTS
Advantage
M/P/Soc X/Sup
Cost
Page
360° Vision
P
X
25
34
Absolute Direction
P
–
5
34
Acute Hearing
P
–
2/level
35
DISADVANTAGES
Advantage
M/P/Soc X/Sup
Cost
Page
Bad Sight
P
–
-25
123
Bloodlust
M
–
-10
125
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    lines = FIXTURE.splitlines()
    traits = detect_traits(lines, _pages_for(lines), "GURPS Basic Set: Characters")
    names = [t.name for t in traits]
    want = ["360° Vision", "Absolute Direction", "Acute Hearing", "Bad Sight", "Bloodlust"]
    if names != want:
        failures.append(f"fixture detected {names}, wanted {want} "
                        f"(column headers must not be read as names)")
    else:
        v = traits[0]
        got = (v.category, v.kind, v.nature, v.cost, v.book_page)
        if got != ("advantage", "physical", "exotic", "25", "B34"):
            failures.append(f"360° Vision row {got}")
        ah = traits[2]
        if ah.cost != "2/level":
            failures.append(f"Acute Hearing cost {ah.cost!r}, wanted '2/level'")
        bs = traits[3]
        if bs.category != "disadvantage" or bs.cost != "-25":
            failures.append(f"Bad Sight {(bs.category, bs.cost)}, wanted disadvantage / -25")

    if base.is_dir() and (base / SOURCES[0].path).exists():
        corpus = Corpus(base, _fresh_sources())
        traits = corpus.sources[0].traits
        adv = sum(1 for t in traits if t.category == "advantage")
        dis = sum(1 for t in traits if t.category == "disadvantage")
        if adv < 150:
            failures.append(f"only {adv} advantages indexed; expected > 150")
        if dis < 100:
            failures.append(f"only {dis} disadvantages indexed; expected > 100")
        cr = corpus.find("combat reflexes", book="basicset")
        if not cr:
            failures.append("Combat Reflexes not found in live Basic Set")
        elif cr[0][1].cost != "15":
            failures.append(f"Combat Reflexes cost {cr[0][1].cost!r}, wanted '15'")
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
        found = sorted({(tr.name, tr.category, tr.cost or "—", tr.book_page or "—", tr.page or -1)
                        for _, tr in corpus.all_traits(args.book) if q in tr.name.lower()})
        for nm, cat, cost, bp, page in found:
            print(f"  {nm}  [{cat}; {cost} pts; {bp}; PDF p.{page}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.traits for s in corpus.sources)
    for src in corpus.sources:
        adv = sum(1 for t in src.traits if t.category == "advantage")
        dis = len(src.traits) - adv
        print(f"  {src.book:34s} {adv:4d} adv / {dis:3d} disadv  "
              f"[{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} GURPS traits (advantages + disadvantages); "
          f"{parsed_well} with 3+ fields parsed.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
