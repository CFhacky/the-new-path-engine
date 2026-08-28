#!/usr/bin/env python3
"""gurps_technique_harvest.py — collate the GURPS 4e Martial Arts techniques.

THE PROCESS (Chad, continuing the GURPS shelf): combat techniques are a distinct
GURPS mechanic — specialized trained maneuvers bought up from a skill default
(Disarming, Choke Hold, Targeted Attack, …), the GURPS analogue of combat feats.
The reference layer had GURPS traits, skills, spells, gear, and creatures but not
techniques. The official Martial Arts Technique Cheat-Sheet tabulates every one
with its difficulty, prerequisite, default, maximum, and damage — and, crucially,
was extracted from a BORN-DIGITAL PDF text layer (characters exact, not OCR), so
this index is character-clean.

    reference/gurps_technique_index.json — every technique: name, difficulty,
                                           prerequisite, default, maximum, damage,
                                           cinematic/silly flags, book page
    reference/gurps_technique_index.md   — the same, for human eyes

GOVERNING SOURCE
    I:\\Sourcebooks\\_text\\GURPS\\GURPS 4e\\GURPS 4e - Martial Arts - Techniques
    Cheat Sheet.md — the Techniques Table, a column-dump: NAME, Difficulty (A/H/
    H+2/H+3), Prerequisite, Default, Maximum, Damage (may wrap several lines),
    Page. The anchor is a technique-name line immediately followed by a bare
    difficulty cell (A / H / H+2 / H+3); the page is the first bare integer after
    the fixed cells, and the lines before it are the (possibly wrapped) damage.
    Native GURPS 4e; the cheat-sheet summarizes GURPS Martial Arts (Dell'Orto &
    Punch), which is the court of appeal for any technique's full text.
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
OUT_JSON = REPO / "reference" / "gurps_technique_index.json"
OUT_MD = REPO / "reference" / "gurps_technique_index.md"

PAGE = re.compile(r"\[PDF page (\d+)\]")
DIFF = re.compile(r"^(A|H|H\+2|H\+3)$")
BOOKPAGE = re.compile(r"^\d{1,3}$")
DIFF_NAME = {"A": "Average", "H": "Hard",
             "H+2": "Hard (combination, +2)", "H+3": "Hard (combination, +3)"}
# Column headers / rubric words that must never be read as a technique name.
NOT_NAME = re.compile(r"^(Technique|Difficulty|Prerequisite|Default|Maximum|Damage|"
                      r"Page|Notes?|Table|Cinematic|Silly)\s*$", re.IGNORECASE)
# A trailing * (cinematic) or † (silly) is part of the name annotation; allow it
# here (it is stripped by _clean_name) so those techniques are not dropped.
NAMEISH = re.compile(r"^[A-Za-z][A-Za-z0-9 ,'’/()\-–&*†‡†‡]{2,44}$")


def _clean_name(s: str) -> Tuple[str, bool, bool]:
    """Return (name, cinematic, silly). '*' marks cinematic, '†' silly."""
    s = s.strip()
    cinematic = "*" in s
    silly = "\u2020" in s or "†" in s
    s = s.replace("*", "").replace("\u2020", "").replace("†", "").strip()
    return re.sub(r"\s{2,}", " ", s).strip(" ,"), cinematic, silly


@dataclass
class GurpsTechnique:
    name: str
    book: str
    page: Optional[int]          # PDF page (provenance)
    start: int
    end: int
    difficulty: Optional[str] = None
    prerequisite: Optional[str] = None
    default: Optional[str] = None
    maximum: Optional[str] = None
    damage: Optional[str] = None
    cinematic: bool = False
    silly: bool = False
    book_page: Optional[str] = None      # page in GURPS Martial Arts

    def quick_fields(self) -> int:
        return sum(1 for v in (self.difficulty, self.prerequisite, self.default, self.book_page) if v)


def _continues(s: str) -> bool:
    """A table cell wraps onto the next line when its text ends mid-list — with a
    trailing comma or a trailing 'or' (the Prerequisite/Default/Damage columns
    are comma-or-'or' separated lists)."""
    s = s.rstrip()
    return s.endswith(",") or s.endswith(" or") or s == "or"


def detect_techniques(lines: List[str], pages: List[int], book: str) -> List[GurpsTechnique]:
    toks = [(i, lines[i].strip()) for i in range(len(lines))
            if lines[i].strip() and not PAGE.search(lines[i])]
    out: List[GurpsTechnique] = []
    n = len(toks)
    for k in range(1, n - 3):
        if not DIFF.match(toks[k][1]):
            continue
        i_nm, raw = toks[k - 1]
        if NOT_NAME.match(raw) or not NAMEISH.match(raw):
            continue
        # collect the raw cells between the difficulty and the page (first bare int)
        raw_cells: List[str] = []
        page_val: Optional[str] = None
        end_tok = k
        for j in range(k + 1, min(n, k + 1 + 14)):
            cell = toks[j][1]
            if BOOKPAGE.match(cell):
                page_val = cell
                end_tok = j
                break
            raw_cells.append(cell)
            end_tok = j
        if page_val is None or len(raw_cells) < 2:
            continue                          # no page / too few cells — not a clean row
        # rejoin cells that wrapped mid-list, reconstructing the logical columns:
        # Prerequisite, Default, Maximum, Damage (Maximum rarely wraps)
        merged: List[str] = []
        for c in raw_cells:
            if merged and (_continues(merged[-1]) or c.lstrip().lower().startswith("or ")):
                merged[-1] = f"{merged[-1]} {c}".strip()
            else:
                merged.append(c)
        if not re.search(r"[A-Za-z]", merged[0]):
            continue
        name, cine, silly = _clean_name(raw)
        if not name:
            continue
        prereq = merged[0]
        default = merged[1] if len(merged) >= 2 else None
        maximum = merged[2] if len(merged) >= 3 else None
        damage = re.sub(r"\s+", " ", " ".join(merged[3:])).strip() if len(merged) > 3 else None
        out.append(GurpsTechnique(
            name=name, book=book, page=pages[i_nm], start=i_nm, end=toks[end_tok][0] + 1,
            difficulty=DIFF_NAME[toks[k][1]], prerequisite=prereq, default=default,
            maximum=maximum, damage=damage, cinematic=cine, silly=silly,
            book_page=f"MA{page_val}"))

    best: Dict[str, GurpsTechnique] = {}
    for tq in out:
        key = tq.name.lower()
        cur = best.get(key)
        if cur is None or tq.quick_fields() > cur.quick_fields():
            best[key] = tq
    return sorted(best.values(), key=lambda t: t.start)


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[GurpsTechnique]]] = {
    "techniques": detect_techniques,
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
    techniques: List[GurpsTechnique] = field(default_factory=list)


SOURCES: List[Source] = [
    Source("macheat", "GURPS Martial Arts (Technique Cheat-Sheet)",
           Path("GURPS/GURPS 4e/GURPS 4e - Martial Arts - Techniques Cheat Sheet.md"),
           "GURPS Martial Arts Technique Cheat-Sheet (SJGames, 4e; summarizes "
           "GURPS Martial Arts by Dell'Orto & Punch)", "techniques"),
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
            src.techniques = DETECTORS[src.detector](src.lines, pages, src.book)
            src.coverage = f"ok — {len(src.techniques)} techniques from {path.name}"

    def all_techniques(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for tq in src.techniques:
                yield src, tq

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, tq in self.all_techniques(book):
            nm = tq.name.lower()
            if nm == q:
                exact.append((src, tq))
            elif q in nm:
                partial.append((src, tq))
        return exact if exact else partial


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# GURPS TECHNIQUE INDEX — The New Path",
        "",
        "**Generated by `scripts/gurps_technique_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** GURPS 4e Martial Arts combat techniques (native GURPS",
        "4e) — the trained maneuvers bought up from a skill default. Source is the",
        "official Technique Cheat-Sheet, a BORN-DIGITAL text layer (characters",
        "exact, not OCR). `default`/`maximum` are relative to the prerequisite",
        "skill; `*` = cinematic, `†` = silly; `book_page` (MAxx) points into GURPS",
        "Martial Arts. A field left `—` is one the source did not carry.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.techniques)
        parsed_well += sum(1 for t in src.techniques if t.quick_fields() >= 3)
        sources_out.append({"key": src.key, "book": src.book, "citation": src.citation,
                            "coverage": src.coverage,
                            "techniques": [asdict(t) for t in src.techniques]})
        md.append(f"## {src.book} — {len(src.techniques)} techniques")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.techniques:
            md.append("| Technique | Diff | Prerequisite | Default | Max | Damage | Cin | Book p. |")
            md.append("|---|---|---|---|---|---|---|---|")
            for t in src.techniques:
                md.append(f"| {t.name} | {t.difficulty or '—'} | {t.prerequisite or '—'} | "
                          f"{t.default or '—'} | {t.maximum or '—'} | {t.damage or '—'} | "
                          f"{'✓' if t.cinematic else '—'} | {t.book_page or '—'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/gurps_technique_harvest.py",
                    "corpus": str(corpus.base), "total_techniques": total,
                    "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 8:
        print(f"'{name}' matches {len(hits)} techniques; narrow with the exact name:")
        for src, tq in hits[:20]:
            print(f"  {tq.name}   [{tq.book}, p.{tq.page}]")
        return 1
    packets = []
    for src, tq in hits:
        body = [ln for ln in src.lines[tq.start:tq.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "gurps-technique-for-translation",
            "instructions": ("A native GURPS 4e Martial Arts technique. The GURPS "
                             "half is here; the system-translator skill builds the "
                             "D&D 3.5e treatment (combat feat / maneuver, as fits). "
                             "The full rules text is in GURPS Martial Arts at the "
                             "cited MA page; this cheat-sheet row is the summary."),
            "name": tq.name,
            "source": {"book": tq.book, "pdf_page": tq.page, "book_page": tq.book_page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [tq.start + 1, tq.end], "citation": src.citation},
            "parsed": {k: v for k, v in asdict(tq).items()
                       if k in ("difficulty", "prerequisite", "default", "maximum",
                                "damage", "cinematic", "silly", "book_page")
                       and v not in (None, False)},
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


FIXTURE = """## [PDF page 3]
Technique
Difficulty
Prerequisite
Default
Maximum
Damage
Page
Acrobatic Stand
A
Acrobatics
Acrobatics-6
Acrobatics
N/A
65
Aggressive Parry
H
Any SS
Parry-1
Parry
Worse of thr-4 or
thr-2 at -1/d cr‡
65
Arm or Wrist Lock
A
Judo, Wrestling, or app. MWS
PS
PS+4
QC
65
Flying Lunge
H+2
Any MWS
Skill-2
Skill
Per attack
71
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    lines = FIXTURE.splitlines()
    tqs = detect_techniques(lines, _pages_for(lines), "GURPS Martial Arts")
    names = [t.name for t in tqs]
    want = ["Acrobatic Stand", "Aggressive Parry", "Arm or Wrist Lock", "Flying Lunge"]
    if names != want:
        failures.append(f"fixture detected {names}, wanted {want} "
                        f"(column headers must not be read as names)")
    else:
        ap = tqs[1]   # wrapped damage
        if ap.damage != "Worse of thr-4 or thr-2 at -1/d cr‡":
            failures.append(f"Aggressive Parry damage {ap.damage!r} — wrapped damage not rejoined")
        if ap.difficulty != "Hard" or ap.book_page != "MA65":
            failures.append(f"Aggressive Parry {(ap.difficulty, ap.book_page)}")
        fl = tqs[3]   # combination difficulty
        if fl.difficulty != "Hard (combination, +2)":
            failures.append(f"Flying Lunge difficulty {fl.difficulty!r}, wanted the H+2 combination label")
        acc = tqs[0]
        if (acc.prerequisite, acc.default, acc.maximum) != ("Acrobatics", "Acrobatics-6", "Acrobatics"):
            failures.append(f"Acrobatic Stand cells {(acc.prerequisite, acc.default, acc.maximum)}")

    if base.is_dir() and (base / SOURCES[0].path).exists():
        corpus = Corpus(base, _fresh_sources())
        tqs = corpus.sources[0].techniques
        if len(tqs) < 80:
            failures.append(f"only {len(tqs)} techniques indexed; expected > 80")
        dis = corpus.find("disarming", book="macheat")
        if not dis:
            failures.append("Disarming not found in live cheat-sheet")
    else:
        print("  [SKIP] cheat-sheet extraction not found — fixture checks only")

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
        found = sorted({(tq.name, tq.difficulty or "—", tq.prerequisite or "—",
                         tq.book_page or "—", tq.page or -1)
                        for _, tq in corpus.all_techniques(args.book) if q in tq.name.lower()})
        for nm, diff, pre, bp, page in found:
            print(f"  {nm}  [{diff}; prereq {pre}; {bp}; PDF p.{page}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.techniques for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.techniques):4d} techniques" if src.techniques else "   0 techniques"
        print(f"  {src.book:44s} {status}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} GURPS techniques; {parsed_well} with 3+ fields parsed.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
