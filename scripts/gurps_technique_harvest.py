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
    Page. A row begins after the preceding Page cell; all non-furniture lines
    up to the bare difficulty cell (A / H / H+2 / H+3) form the possibly wrapped
    name. The first following bare integer is its Martial Arts page.
    I:\\Sourcebooks\\_text\\GURPS\\GURPS 4e\\GURPS 4e - Martial Arts.md
    supplies each complete, exact description. Native GURPS 4e; Martial Arts
    (Dell'Orto & Punch) is the court of appeal for all full text.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
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
FULL_BOOK = Path("GURPS/GURPS 4e/GURPS 4e - Martial Arts.md")
TABLE_FURNITURE = {
    "technique", "difficulty", "difficulty prerequisite", "prerequisite",
    "default", "maximum", "damage", "page",
    "martial arts techniques cheat-sheet", "techniques table",
    "techniques table (continued)",
}
RESTORED_NAMES = {
    "Close Combat \u2013 Ranged", "Combination \u2013 2 Attacks",
    "Combination \u2013 3 Attacks", "Combination, 2H \u2013 2 Attacks",
    "Combination, 2H \u2013 3 Attacks", "Dual-Weapon Attack",
    "Dual-Weapon Attack (Bow)", "Dual-Weapon Defense", "Exotic Hand Strike",
    "Eye-Poke Defense", "Fighting While Seated", "Flying Atomic Wedgie",
    "Flying Jump Kick", "Hand Catch (PMW)", "Hand-Clap Parry",
    "Hands-Free Riding", "Lower-Body Arm Lock", "Lower-Body Head Lock",
    "Lower-Body Leg Lock", "Pressure-Point Strike",
    "Retain Weapon \u2013 Ranged", "TA \u2013 Grab, Strike, or Throw",
    "TA \u2013 Grapple", "Two-Handed Punch",
}
BROKEN_FRAGMENTS = {
    "Attack", "Attack (Bow)", "Defense", "Kick", "Lock", "Parry", "Punch",
    "Ranged", "Riding", "Seated", "Strike", "Wedgie", "or Throw",
}


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
    page: Optional[int]                 # cheat-sheet PDF page (table provenance)
    table_start: int
    table_end: int
    start: Optional[int] = None         # full-book span when contiguous
    end: Optional[int] = None
    difficulty: Optional[str] = None
    prerequisite: Optional[str] = None
    default: Optional[str] = None
    maximum: Optional[str] = None
    damage: Optional[str] = None
    cinematic: bool = False
    silly: bool = False
    book_page: Optional[str] = None     # printed page in GURPS Martial Arts
    description_key: Optional[str] = None
    description_spans: List[List[int]] = field(default_factory=list)

    def quick_fields(self) -> int:
        return sum(1 for v in (self.difficulty, self.prerequisite, self.default, self.book_page) if v)


def _continues(s: str) -> bool:
    """A table cell wraps onto the next line when its text ends mid-list — with a
    trailing comma or a trailing 'or' (the Prerequisite/Default/Damage columns
    are comma-or-'or' separated lists)."""
    s = s.rstrip()
    return s.endswith(",") or s.endswith(" or") or s == "or"


def detect_techniques(lines: List[str], pages: List[int], book: str) -> List[GurpsTechnique]:
    """Parse the four printed table pages, including names wrapped over lines."""
    toks = [(i, lines[i].strip()) for i in range(len(lines))
            if (lines[i].strip() and not PAGE.search(lines[i])
                and 3 <= pages[i] <= 6)]
    out: List[GurpsTechnique] = []
    n = len(toks)
    for k in range(n):
        if not DIFF.fullmatch(toks[k][1]):
            continue

        # A row begins after the previous row's bare page number. For the first
        # row, the Page column header is the delimiter. Everything up to the
        # difficulty cell is the (possibly wrapped) technique name.
        prev = next((j for j in range(k - 1, -1, -1)
                     if BOOKPAGE.fullmatch(toks[j][1])), None)
        if prev is None:
            prev = next((j for j in range(k - 1, -1, -1)
                         if toks[j][1].casefold() == "page"), -1)
        name_parts = [(i, text) for i, text in toks[prev + 1:k]
                      if text.casefold() not in TABLE_FURNITURE]
        if not name_parts:
            continue
        raw = " ".join(text for _, text in name_parts).strip()

        raw_cells: List[str] = []
        page_val: Optional[str] = None
        end_tok = k
        for j in range(k + 1, min(n, k + 26)):
            cell = toks[j][1]
            if BOOKPAGE.fullmatch(cell):
                page_val = cell
                end_tok = j
                break
            raw_cells.append(cell)
            end_tok = j
        if page_val is None or len(raw_cells) < 2:
            continue

        merged: List[str] = []
        for cell in raw_cells:
            if merged and (_continues(merged[-1])
                           or cell.lstrip().casefold().startswith("or ")):
                merged[-1] = f"{merged[-1]} {cell}".strip()
            else:
                merged.append(cell)
        if not re.search(r"[A-Za-z]", merged[0]):
            continue

        name, cine, silly = _clean_name(raw)
        if not name:
            continue
        i_nm = name_parts[0][0]
        out.append(GurpsTechnique(
            name=name, book=book, page=pages[i_nm],
            table_start=i_nm, table_end=toks[end_tok][0] + 1,
            difficulty=DIFF_NAME[toks[k][1]], prerequisite=merged[0],
            default=merged[1] if len(merged) >= 2 else None,
            maximum=merged[2] if len(merged) >= 3 else None,
            damage=(re.sub(r"\s+", " ", " ".join(merged[3:])).strip()
                    if len(merged) > 3 else None),
            cinematic=cine, silly=silly, book_page=f"MA{page_val}"))

    best: Dict[str, GurpsTechnique] = {}
    for tq in out:
        key = tq.name.casefold()
        cur = best.get(key)
        if cur is None or tq.quick_fields() > cur.quick_fields():
            best[key] = tq
    return sorted(best.values(), key=lambda t: t.table_start)


def _description_key(name: str) -> str:
    """Map table variants to the one book passage that defines them."""
    if name in {"Back Kick", "Back Strike"}:
        return "Back Kick or Back Strike"
    if name == "Close Combat \u2013 Ranged":
        return "Close Combat"
    if name.startswith("Combination"):
        return "Optional Rule: Combinations"
    if name == "Dual-Weapon Attack (Bow)":
        return "Dual-Weapon Attack"
    if name in {"Flying Jump Kick", "Flying Lunge"}:
        return "Flying Jump Kick or Flying Lunge"
    if name == "Hand Catch (PMW)":
        return "Hand Catch"
    if name in {"Leg Throw", "Lower-Body Arm Lock", "Lower-Body Head Lock",
                "Lower-Body Leg Lock", "Triangle Choke"}:
        return "Using Your Legs"
    if name == "Retain Weapon \u2013 Ranged":
        return "Retain Weapon"
    if name in {"Spinning Kick", "Spinning Punch", "Spinning Strike"}:
        return "Spinning (Attack)"
    if name.startswith("TA \u2013 "):
        return "Optional Rule: Targeted Attacks"
    return name


def _norm_heading(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip()


def _next_text(lines: List[str], start: int) -> str:
    return next((lines[i].strip() for i in range(start + 1, min(len(lines), start + 5))
                 if lines[i].strip()), "")


def _one_prefix(lines: List[str], text: str, after: int = -1) -> int:
    target = _norm_heading(text)
    hits = [i for i, line in enumerate(lines)
            if i > after and _norm_heading(line).startswith(target)]
    if len(hits) != 1:
        raise ValueError(f"full-text anchor {text!r}: expected 1 hit, got {hits}")
    return hits[0]


def _one_exact(lines: List[str], text: str, after: int = -1) -> int:
    target = _norm_heading(text)
    hits = [i for i, line in enumerate(lines)
            if i > after and line.strip() and _norm_heading(line) == target]
    if not hits or (after < 0 and len(hits) != 1):
        raise ValueError(f"full-text heading {text!r}: expected a unique hit, got {hits}")
    return hits[0]


def _book_heading(lines: List[str], pages: List[int], key: str,
                  book_page: str, strong: bool = True) -> int:
    target = _norm_heading(key)
    pdf_page = int(book_page.removeprefix("MA")) + 1
    hits = [i for i, line in enumerate(lines)
            if pages[i] == pdf_page and line.strip()
            and _norm_heading(line) == target]
    if strong:
        hits = [i for i in hits
                if _norm_heading(_next_text(lines, i)) in {"average", "hard"}]
    if len(hits) != 1:
        raise ValueError(
            f"description heading {key!r} on PDF page {pdf_page}: {hits}")
    return hits[0]


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
    description_path: Path
    coverage: str = "pending"
    lines: List[str] = field(default_factory=list)
    description_lines: List[str] = field(default_factory=list)
    techniques: List[GurpsTechnique] = field(default_factory=list)


SOURCES: List[Source] = [
    Source("macheat", "GURPS Martial Arts (Technique Cheat-Sheet)",
           Path("GURPS/GURPS 4e/GURPS 4e - Martial Arts - Techniques Cheat Sheet.md"),
           "GURPS Martial Arts Technique Cheat-Sheet (SJGames, 4e; summarizes "
           "GURPS Martial Arts by Dell'Orto & Punch)", "techniques", FULL_BOOK),
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


def _attach_descriptions(lines: List[str], pages: List[int],
                         techniques: List[GurpsTechnique]) -> Dict[str, List[List[int]]]:
    """Attach exact Martial Arts description fragments to every table row."""
    key_pages: Dict[str, str] = {}
    for tq in techniques:
        key = _description_key(tq.name)
        if not tq.book_page:
            raise ValueError(f"{tq.name}: missing Martial Arts page")
        previous = key_pages.setdefault(key, tq.book_page)
        if previous != tq.book_page:
            raise ValueError(f"{key}: conflicting pages {previous}/{tq.book_page}")

    section_keys = {
        "Optional Rule: Combinations",
        "Optional Rule: Targeted Attacks",
        "Using Your Legs",
    }
    anchors = {
        key: _book_heading(lines, pages, key, book_page,
                           strong=key not in section_keys)
        for key, book_page in key_pages.items()
    }
    ordered = sorted((position, key) for key, position in anchors.items())
    creating = _one_exact(
        lines, "CREATING NEW TECHNIQUES", after=anchors["Whirlwind Attack"])
    spans: Dict[str, List[List[int]]] = {}
    for index, (position, key) in enumerate(ordered):
        end = ordered[index + 1][0] if index + 1 < len(ordered) else creating
        spans[key] = [[position, end]]

    # Sidebar/second-column text interrupts seven descriptions. Preserve the
    # book's exact fragments and their visual reading order without importing
    # the intervening sidebar or quotation.
    target_body = _one_prefix(lines, "attacks on high value targets")
    breakfall_more = _one_prefix(
        lines, "this technique covers ways of controlling or absorbing")
    spans["Breakfall"] = [
        [anchors["Breakfall"], target_body],
        [breakfall_more, anchors["Cavalry Training"]],
    ]
    target_title = anchors["Optional Rule: Targeted Attacks"]
    spans["Optional Rule: Targeted Attacks"] = [
        [target_title, target_title + 1],
        [target_body, target_title],
    ]

    kick_quote = _one_prefix(
        lines, "punches and kicks are tools to", after=anchors["Kicking"])
    kicking_more = _one_prefix(lines, "combine kicking with committed attack")
    spans["Kicking"] = [
        [anchors["Kicking"], kick_quote],
        [kicking_more, anchors["Knee Drop"]],
    ]

    dirty_tricks = _one_exact(lines, "Dirty Tricks", after=anchors["Leg Lock"])
    leg_lock_more = _one_prefix(lines, "a leg lock is an attempt")
    spans["Leg Lock"] = [
        [anchors["Leg Lock"], dirty_tricks],
        [leg_lock_more, anchors["Low Fighting"]],
    ]

    using_body = _one_prefix(lines, "much as you can kick as well as punch")
    spinning_more = _one_prefix(
        lines, "as an all out attack a spinning attack")
    using_title = anchors["Using Your Legs"]
    spans["Spinning (Attack)"] = [
        [anchors["Spinning (Attack)"], using_body],
        [spinning_more, anchors["Stamp Kick"]],
    ]
    spans["Using Your Legs"] = [
        [using_title, using_title + 1],
        [using_body, using_title],
    ]

    combination_body = _one_prefix(
        lines, "martial artists often practice executing")
    stamp_more = _one_prefix(
        lines, "this kick consists of a swift downward stamp")
    combination_title = anchors["Optional Rule: Combinations"]
    spans["Stamp Kick"] = [
        [anchors["Stamp Kick"], combination_body],
        [stamp_more, anchors["Staying Seated"]],
    ]
    spans["Optional Rule: Combinations"] = [
        [combination_title, combination_title + 1],
        [combination_body, combination_title],
    ]

    homer_quote = _one_prefix(lines, "iros lunged", after=anchors["Piledriver"])
    piledriver_more = _one_prefix(lines, "to execute a piledriver")
    secret_body = _one_prefix(lines, "martial arts legend features")
    piledriver_last = _one_prefix(
        lines, "a variation is to grapple your adversary")
    spans["Piledriver"] = [
        [anchors["Piledriver"], homer_quote],
        [piledriver_more, secret_body],
        [piledriver_last, anchors["Pole-Vault Kick"]],
    ]

    silly_body = _one_prefix(
        lines, "humorous movies often feature silly techniques")
    springing_more = _one_prefix(lines, "you may combine springing attack")
    spans["Springing Attack"] = [
        [anchors["Springing Attack"], silly_body],
        [springing_more, anchors["Timed Defense"]],
    ]

    # Standalone furniture that belongs to no technique.
    spans["Lethal Eye-Poke"] = [[
        anchors["Lethal Eye-Poke"],
        _one_prefix(lines, "go for the eyes", after=anchors["Lethal Eye-Poke"]),
    ]]
    spans["Wrench Spine"] = [[
        anchors["Wrench Spine"],
        _one_exact(lines, "CINEMATIC TECHNIQUES", after=anchors["Wrench Spine"]),
    ]]
    spans["Wet Willy"] = [[
        anchors["Wet Willy"],
        _one_exact(lines, "Silly Techniques", after=anchors["Wet Willy"]),
    ]]
    spans["Whirlwind Attack"] = [[anchors["Whirlwind Attack"], creating]]

    for key, fragments in spans.items():
        for start, end in fragments:
            if not (0 <= start < end <= len(lines)):
                raise ValueError(f"{key}: invalid full-text span {start}:{end}")
    for tq in techniques:
        key = _description_key(tq.name)
        tq.description_key = key
        tq.description_spans = [list(pair) for pair in spans[key]]
        if len(tq.description_spans) == 1:
            tq.start, tq.end = tq.description_spans[0]
        else:
            tq.start = tq.end = None
    return spans


def _fresh_sources() -> List[Source]:
    fields = ("key", "book", "path", "citation", "detector", "description_path")
    return [Source(*(getattr(src, key) for key in fields)) for src in SOURCES]


class Corpus:
    def __init__(self, base: Path, sources: List[Source]):
        self.base = base
        self.sources = sources
        for src in self.sources:
            path = base / src.path
            description_path = base / src.description_path
            if not path.exists():
                src.coverage = f"NO COVERAGE: technique table (missing {path})"
                continue
            src.lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            pages = _pages_for(src.lines)
            src.techniques = DETECTORS[src.detector](src.lines, pages, src.book)
            if not description_path.exists():
                src.coverage = (
                    f"NO COVERAGE: full technique descriptions (missing {description_path})")
                continue
            src.description_lines = description_path.read_text(
                encoding="utf-8", errors="replace").splitlines()
            _attach_descriptions(
                src.description_lines, _pages_for(src.description_lines),
                src.techniques)
            src.coverage = (
                f"ok — {len(src.techniques)} techniques from {path.name}; "
                f"full descriptions from {description_path.name}")

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
        "exact, not OCR); exact `description_spans` point into the full Martial Arts",
        "extraction. `default`/`maximum` are relative to the prerequisite skill;",
        "`*` = cinematic, `†` = silly; `book_page` (MAxx) cites GURPS Martial Arts.",
        "A field left `—` is one the source did not carry.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.techniques)
        parsed_well += sum(1 for t in src.techniques if t.quick_fields() >= 3)
        sources_out.append({
            "key": src.key, "book": src.book, "citation": src.citation,
            "source_path": str(src.description_path),
            "table_source_path": str(src.path),
            "coverage": src.coverage,
            "techniques": [asdict(t) for t in src.techniques],
        })
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
        fragments = [
            "\n".join(src.description_lines[start:end]).strip()
            for start, end in tq.description_spans
        ]
        packets.append({
            "packet": "gurps-technique-for-translation",
            "instructions": ("A native GURPS 4e Martial Arts technique. The GURPS "
                             "half is here; the system-translator skill builds the "
                             "D&D 3.5e treatment (combat feat / maneuver, as fits). "
                             "The raw block is the full book-verbatim definition; "
                             "the cheat-sheet supplies the parsed mechanics."),
            "name": tq.name,
            "source": {
                "book": tq.book, "pdf_page": tq.page, "book_page": tq.book_page,
                "extraction": str(corpus.base / src.description_path),
                "description_spans": tq.description_spans,
                "table_extraction": str(corpus.base / src.path),
                "table_lines": [tq.table_start + 1, tq.table_end],
                "citation": src.citation,
            },
            "parsed": {k: v for k, v in asdict(tq).items()
                       if k in ("difficulty", "prerequisite", "default", "maximum",
                                "damage", "cinematic", "silly", "book_page")
                       and v not in (None, False)},
            "raw_block": re.sub(
                r"\n{3,}", "\n\n", "\n\n".join(fragments)).strip(),
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
Close Combat –
Ranged
H
Any weapon skill
Skill-4
Skill
Special
69
Dual-Weapon
Attack (Bow)
H
Bow
Bow-4
Bow
Per attack
83
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    fixture_lines = FIXTURE.splitlines()
    fixture = detect_techniques(
        fixture_lines, _pages_for(fixture_lines), "GURPS Martial Arts")
    by_name = {t.name: t for t in fixture}
    want = [
        "Acrobatic Stand", "Aggressive Parry", "Arm or Wrist Lock",
        "Flying Lunge", "Close Combat \u2013 Ranged",
        "Dual-Weapon Attack (Bow)",
    ]
    if [t.name for t in fixture] != want:
        failures.append(
            f"fixture detected {[t.name for t in fixture]}, wanted {want}")
    elif by_name["Aggressive Parry"].damage != (
            "Worse of thr-4 or thr-2 at -1/d cr‡"):
        failures.append("fixture wrapped damage was not rejoined")
    elif by_name["Flying Lunge"].difficulty != "Hard (combination, +2)":
        failures.append("fixture H+2 difficulty was not preserved")

    table_path = base / SOURCES[0].path
    full_path = base / SOURCES[0].description_path
    if table_path.exists() and full_path.exists():
        corpus = Corpus(base, _fresh_sources())
        source = corpus.sources[0]
        live = source.techniques
        names = [t.name for t in live]
        digest = hashlib.sha256("\n".join(names).encode()).hexdigest()
        if len(live) != 112:
            failures.append(f"live count {len(live)}, wanted 112")
        if digest != "da53091310929be5bd4def4150fba4d609019993e7fe4a3325dfa2870d4848e0":
            failures.append(f"live roster digest drifted: {digest}")
        counts = Counter(t.difficulty for t in live)
        expected_counts = Counter({
            "Average": 21, "Hard": 87,
            "Hard (combination, +2)": 2,
            "Hard (combination, +3)": 2,
        })
        if counts != expected_counts:
            failures.append(f"difficulty counts {dict(counts)}")
        name_set = set(names)
        if not RESTORED_NAMES <= name_set:
            failures.append(
                f"restored wrapped names missing: {sorted(RESTORED_NAMES - name_set)}")
        if BROKEN_FRAGMENTS & name_set:
            failures.append(
                f"broken name fragments survived: {sorted(BROKEN_FRAGMENTS & name_set)}")
        if names.count("Lower-Body Arm Lock") != 1:
            failures.append("Lower-Body Arm Lock duplicate was not collapsed")
        if any(t.quick_fields() < 4 for t in live):
            failures.append("one or more live rows lost a core mechanical field")
        if any(t.page not in range(3, 7) or not t.book_page for t in live):
            failures.append("one or more live rows lacks a valid book/page citation")
        if any("\ufffd" in t.name for t in live):
            failures.append("a live technique name contains U+FFFD")

        groups: Dict[str, List[GurpsTechnique]] = {}
        for tq in live:
            groups.setdefault(tq.description_key or "", []).append(tq)
        shared = {key for key, rows in groups.items() if len(rows) > 1}
        span_sets = {
            tuple(tuple(pair) for pair in tq.description_spans) for tq in live
        }
        if len(groups) != 96 or len(span_sets) != 96:
            failures.append(
                f"description groups/spans {len(groups)}/{len(span_sets)}, wanted 96/96")
        if len(shared) != 10:
            failures.append(f"shared description groups {len(shared)}, wanted 10")

        unique_fragments = sorted({
            tuple(pair) for tq in live for pair in tq.description_spans
        })
        for left, right in zip(unique_fragments, unique_fragments[1:]):
            if left[1] > right[0]:
                failures.append(f"full-text fragments overlap: {left} / {right}")
                break

        def assembled(tq: GurpsTechnique) -> str:
            return "\n\n".join(
                "\n".join(source.description_lines[start:end]).strip()
                for start, end in tq.description_spans)

        for tq in live:
            text = assembled(tq)
            key_tokens = _norm_heading(tq.description_key or "").split()
            if not text or not all(
                    token in _norm_heading(text[:400])
                    for token in key_tokens[:2]):
                failures.append(f"{tq.name}: description does not lead with its key")
                break
            if len(tq.description_spans) == 1:
                if [tq.start, tq.end] != tq.description_spans[0]:
                    failures.append(f"{tq.name}: contiguous span fields disagree")
                    break
            elif tq.start is not None or tq.end is not None:
                failures.append(f"{tq.name}: split description has a false single span")
                break

        leakage = {
            "Breakfall": "attacks on high value targets",
            "Kicking": "punches and kicks are tools to",
            "Leg Lock": "dirty tricks",
            "Spinning Kick": "much as you can kick as well as punch",
            "Stamp Kick": "martial artists often practice executing",
            "Piledriver": "martial arts legend features",
            "Springing Attack": "humorous movies often feature silly techniques",
        }
        lookup = {t.name: t for t in live}
        for name, forbidden in leakage.items():
            if _norm_heading(forbidden) in _norm_heading(assembled(lookup[name])):
                failures.append(f"{name}: unrelated sidebar/quotation leaked")
        continuations = {
            "Breakfall": "this technique covers ways of controlling or absorbing",
            "Kicking": "combine kicking with committed attack",
            "Leg Lock": "a leg lock is an attempt",
            "Spinning Kick": "as an all out attack a spinning attack",
            "Stamp Kick": "this kick consists of a swift downward stamp",
            "Piledriver": "a variation is to grapple your adversary",
            "Springing Attack": "you may combine springing attack",
        }
        for name, required in continuations.items():
            if _norm_heading(required) not in _norm_heading(assembled(lookup[name])):
                failures.append(f"{name}: continuation fragment missing")
    else:
        print("  [SKIP] table/full extraction missing — fixture checks only")

    for failure in failures:
        print(f"SELFTEST FAIL: {failure}")
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
