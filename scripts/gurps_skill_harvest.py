#!/usr/bin/env python3
"""gurps_skill_harvest.py — collate GURPS 4e skills and their exact descriptions.

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
                                       defaults, book page, and exact source span
    reference/gurps_skill_index.md   — the same, for human eyes

GOVERNING SOURCE
    I:\\Sourcebooks\\_text\\GURPS\\GURPS 4e\\GURPS 4e - Basic Set - Characters.md
    — the Skills portion of the Trait Lists appendix. A skill row is a NAME line,
    then the columns one per line: Attr (the controlling attribute), Diff (the
    difficulty letter), then the Defaults cell and the Page cell interleaved. The
    anchor is the Attr line immediately followed by the Diff line — a signature
    that occurs only in this table (the skill DESCRIPTIONS chapter writes the
    attribute/difficulty inline, e.g. "Acrobatics (DX/Hard)"). A second pass
    matches that roster to the alphabetical Skills chapter, including wrapped
    headings and grouped definitions, and records the true heading-to-heading
    span. Native GURPS 4e data; the PDF stands behind every extraction.
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
DESC_ATTR = r"(?:ST|DX|IQ|HT|Will|Per)"
DESC_DIFF = r"(?:Easy|Average|Hard|Very Hard|Varies)"
DESC_SIG = re.compile(rf"^{DESC_ATTR}(?: or {DESC_ATTR})?/{DESC_DIFF}$", re.IGNORECASE)
DESC_INLINE = re.compile(
    rf"^(?P<name>.+?) \({DESC_ATTR}(?: or {DESC_ATTR})?/{DESC_DIFF}\):", re.IGNORECASE)
DESC_INLINE_ONLY = re.compile(
    rf"^\({DESC_ATTR}(?: or {DESC_ATTR})?/{DESC_DIFF}\):", re.IGNORECASE)
TABLE_ROW_REPAIRS = {
    # The appendix puts the second half of these names after the Page cell. The
    # canonical names and defaults below are repeated verbatim in their own
    # description headers; this is source-verified reconstruction, never guessing.
    "Computer": ("Computer Operation/TL", "IQ-4"),
    "Electronics": ("Electronics Operation/TL",
                    "IQ-5, Electronics Repair (same)-5, Engineer (Electronics)-5"),
    "Hazardous": ("Hazardous Materials/TL", "IQ-5"),
    "Intelligence": ("Intelligence Analysis/TL", "IQ-6, Strategy (any)-6"),
}
DESCRIPTION_ALIASES = {
    # The printed cross-reference drops the appendix row's /TL suffix.
    "Brain Hacking/TL": "Brain Hacking",
}
MELEE_SECTION_HEADINGS = {
    "Fencing Weapons", "Flails", "Impact Weapons", "Pole Weapons",
    "Swords", "Whips", "Other Weapons",
}


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
    description_key: Optional[str] = None  # verified heading when table name drifted

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
        if name in TABLE_ROW_REPAIRS:
            name, defaults = TABLE_ROW_REPAIRS[name]
            tl = True
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


def _norm_heading(s: str) -> str:
    """Normalize only layout/footnote noise for exact heading matching."""
    return re.sub(r"\s+", " ", FOOTNOTE.sub("", s.strip()).strip()).casefold()


def _looks_heading_piece(s: str) -> bool:
    """Conservative test for the first half of a wrapped skill heading."""
    s = FOOTNOTE.sub("", s.strip()).strip()
    if not s or len(s) > 45 or re.search(r"[.!?;:]$", s):
        return False
    words = re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)?", s)
    return bool(words) and all(
        w[:1].isupper() or w.casefold() in {"of", "and", "the", "or"} for w in words)


def _heading_start(lines: List[str], signature_at: int, floor: int) -> int:
    """Return the first line of the one- or two-line heading before a signature."""
    start = signature_at - 1
    if start <= floor:
        return max(start, floor)
    tail = lines[start].strip()
    prior = lines[start - 1].strip()
    if (len(tail.split()) == 1 and _looks_heading_piece(tail)
            and _looks_heading_piece(prior)):
        start -= 1
    return start


def _description_bounds(lines: List[str]) -> Tuple[int, int]:
    """Locate the Basic Set alphabetical Skills chapter without fixed offsets."""
    start = next((i for i in range(len(lines) - 1)
                  if lines[i].strip() == "Accounting"
                  and DESC_SIG.match(lines[i + 1].strip())), -1)
    if start < 0:
        return -1, -1
    zen = next((i for i in range(start, len(lines) - 1)
                if lines[i].strip() == "Zen Archery"
                and DESC_SIG.match(lines[i + 1].strip())), -1)
    if zen < 0:
        return start, len(lines)
    # The running SKILLS footer immediately after Zen Archery is the exact end
    # of the chapter; the following page begins the optional Techniques rules.
    footer = next((i for i in range(zen + 2, len(lines))
                   if lines[i].strip() == "SKILLS"), len(lines))
    end = (footer - 1 if footer < len(lines) and footer > zen
           and re.fullmatch(r"\d{2,3}", lines[footer - 1].strip()) else footer)
    return start, end


def attach_description_spans(lines: List[str], pages: List[int],
                             skills: List[GurpsSkill]) -> int:
    """Replace appendix-row markers with exact, non-overlapping description spans."""
    lo, hi = _description_bounds(lines)
    if lo < 0:
        return 0

    wanted = {
        _norm_heading(DESCRIPTION_ALIASES.get(sk.name, sk.name)):
            DESCRIPTION_ALIASES.get(sk.name, sk.name)
        for sk in skills
    }
    candidates: Dict[str, List[Tuple[int, int, str]]] = {k: [] for k in wanted}
    boundaries = {hi}

    # Standalone skill headings: NAME (occasionally wrapped), then Attr/Difficulty.
    # Cross-reference entries use NAME then "see ...". Every such heading is also
    # a boundary, including skills the appendix detector did not recover.
    for j in range(lo + 1, hi):
        text = lines[j].strip()
        kind = "typed" if DESC_SIG.match(text) else (
            "see" if text.casefold().startswith("see ") else None)
        if not kind:
            continue
        start = _heading_start(lines, j, lo)
        boundaries.add(start)
        key = _norm_heading(" ".join(lines[start:j]))
        if key in candidates:
            candidates[key].append((0 if kind == "typed" else 3, start, kind))

    # Grouped definitions (Crewman, Environment Suit, Acrobatics) use "Name:",
    # while Melee Weapon definitions put the Attr/Difficulty signature inline.
    for i in range(lo, hi):
        text = lines[i].strip()
        match = DESC_INLINE.match(text)
        if match:
            boundaries.add(i)
            key = _norm_heading(match.group("name"))
            if key in candidates:
                candidates[key].append((1, i, "inline"))
        elif DESC_INLINE_ONLY.match(text):
            start = _heading_start(lines, i, lo)
            boundaries.add(start)
            key = _norm_heading(" ".join(lines[start:i]))
            if key in candidates:
                candidates[key].append((1, start, "inline"))

        if ":" in text:
            key = _norm_heading(text.split(":", 1)[0])
            if key in candidates:
                boundaries.add(i)
                candidates[key].append((2, i, "colon"))
        if text in MELEE_SECTION_HEADINGS:
            boundaries.add(i)

    mapped = 0
    for sk in skills:
        heading = DESCRIPTION_ALIASES.get(sk.name, sk.name)
        choices = candidates.get(_norm_heading(heading), [])
        if not choices:
            continue
        expected_pdf = int(sk.book_page[1:]) + 3 if sk.book_page else 0
        _rank, start, kind = min(
            set(choices),
            key=lambda c: (c[0], abs(pages[c[1]] - expected_pdf), c[1]))
        end = min(b for b in boundaries if b > start)
        # A grouped one-paragraph definition must not absorb a page footer or a
        # floated neighboring column after the final definition in its group.
        if kind == "colon":
            footer = next((j for j in range(start + 1, end)
                           if lines[j].strip() == "SKILLS"), None)
            if footer is not None:
                end = footer
        if end - start < 2:
            continue
        sk.start, sk.end = start, end
        if _norm_heading(heading) != _norm_heading(sk.name):
            sk.description_key = heading
        mapped += 1
    return mapped


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
            mapped = attach_description_spans(src.lines, pages, src.skills)
            src.coverage = (f"ok — {len(src.skills)} skills from {path.name}; "
                            f"{mapped} exact description spans")

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
        "description, and every row carries its exact source span there. A field",
        "left `—` is one the OCR did not cleanly yield.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.skills)
        parsed_well += sum(1 for s in src.skills if s.quick_fields() >= 3)
        sources_out.append({"key": src.key, "book": src.book, "citation": src.citation,
                            "source_path": str(src.path), "coverage": src.coverage,
                            "skills": [
                                {k: v for k, v in asdict(s).items()
                                 if k != "description_key" or v is not None}
                                for s in src.skills
                            ]})
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
Computer
IQ
E
IQ-4
184
Operation/TL
Alchemy/TL
IQ
VH
None
174
"""

DESCRIPTION_FIXTURE = """## [PDF page 176]
Accounting
IQ/Hard
Default: IQ-6.
Accounting body.
Computer
Operation/TL†
IQ/Easy
Default: IQ-4.
Computer body.
Computer Programming
IQ/Hard
Default: None.
Programming body.
## [PDF page 210]
Melee Weapon
DX/Varies
Defaults: Special.
Impact Weapons
Axe/Mace (DX/Average): Any one-handed
impact weapon.
Two-Handed
Axe/Mace
(DX/Average): Any two-handed impact weapon.
Zen Archery
IQ/Very Hard
Defaults: None.
Zen body.
228
SKILLS
## [PDF page 231]
Technique chapter text.
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    lines = FIXTURE.splitlines()
    skills = detect_skills(lines, _pages_for(lines), "GURPS Basic Set: Characters")
    names = [s.name for s in skills]
    want = ["Accounting", "Acrobatics", "Airshipman/TL",
            "Computer Operation/TL", "Alchemy/TL"]
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
        computer = skills[3]
        if not computer.tech_level or computer.defaults != "IQ-4":
            failures.append(f"Computer Operation/TL repair {asdict(computer)!r}")
        alc = skills[4]
        if alc.difficulty != "Very Hard":
            failures.append(f"Alchemy difficulty {alc.difficulty!r}, wanted 'Very Hard'")

    desc_lines = DESCRIPTION_FIXTURE.splitlines()
    desc_skills = [
        GurpsSkill("Accounting", "fixture", 301, 0, 1, book_page="B174"),
        GurpsSkill("Computer Operation/TL", "fixture", 301, 0, 1, book_page="B184"),
        GurpsSkill("Axe/Mace", "fixture", 301, 0, 1, book_page="B208"),
        GurpsSkill("Zen Archery", "fixture", 301, 0, 1, book_page="B228"),
    ]
    mapped = attach_description_spans(desc_lines, _pages_for(desc_lines), desc_skills)
    if mapped != 4:
        failures.append(f"description fixture mapped {mapped}/4 spans")
    else:
        by_name = {s.name: s for s in desc_skills}
        acc_block = desc_lines[by_name["Accounting"].start:by_name["Accounting"].end]
        if acc_block != ["Accounting", "IQ/Hard", "Default: IQ-6.", "Accounting body."]:
            failures.append(f"Accounting description span {acc_block!r}")
        computer = by_name["Computer Operation/TL"]
        computer_block = desc_lines[computer.start:computer.end]
        if (computer.description_key is not None
                or computer_block[:3] != ["Computer", "Operation/TL†", "IQ/Easy"]
                or "Computer Programming" in computer_block):
            failures.append(f"Computer wrapped description span {computer_block!r}")
        axe_block = desc_lines[by_name["Axe/Mace"].start:by_name["Axe/Mace"].end]
        if axe_block != ["Axe/Mace (DX/Average): Any one-handed", "impact weapon."]:
            failures.append(f"Axe/Mace boundary leaked: {axe_block!r}")
        zen_block = desc_lines[by_name["Zen Archery"].start:by_name["Zen Archery"].end]
        if zen_block[-1:] != ["Zen body."] or "Technique chapter text." in zen_block:
            failures.append(f"Zen Archery chapter boundary leaked: {zen_block!r}")

    if base.is_dir() and (base / SOURCES[0].path).exists():
        corpus = Corpus(base, _fresh_sources())
        source = corpus.sources[0]
        skills = source.skills
        if len(skills) != 263:
            failures.append(f"{len(skills)} skills indexed; expected locked core count 263")
        lo, hi = _description_bounds(source.lines)
        outside = [s.name for s in skills
                   if not (lo <= s.start < s.end <= hi and s.end - s.start >= 2)]
        if outside:
            failures.append(f"{len(outside)} invalid description spans: {outside[:8]}")
        starts = [s.start for s in skills]
        if len(set(starts)) != len(starts):
            failures.append("live description spans do not have unique starts")
        ordered = sorted(skills, key=lambda s: s.start)
        overlaps = [(a.name, b.name) for a, b in zip(ordered, ordered[1:])
                    if a.end > b.start]
        if overlaps:
            failures.append(f"description spans overlap: {overlaps[:5]}")
        bad_leads = []
        for sk in skills:
            heading = sk.description_key or sk.name
            lead = _norm_heading(" ".join(source.lines[sk.start:min(sk.end, sk.start + 3)]))
            if not lead.startswith(_norm_heading(heading)):
                bad_leads.append(sk.name)
        if bad_leads:
            failures.append(f"description heading validation failed: {bad_leads[:8]}")
        got_aliases = {s.name: s.description_key for s in skills if s.description_key}
        if got_aliases != DESCRIPTION_ALIASES:
            failures.append(f"description aliases {got_aliases!r}, wanted {DESCRIPTION_ALIASES!r}")

        by_name = {s.name: s for s in skills}
        acro = by_name.get("Acrobatics")
        if not acro or acro.attribute != "DX":
            failures.append(f"Acrobatics attribute {getattr(acro, 'attribute', None)!r}, wanted 'DX'")
        for name, expected_start in {
                "Computer Operation/TL": "Computer Operation/TL",
                "Electronics Operation/TL": "Electronics\nOperation/TL",
                "Hazardous Materials/TL": "Hazardous\nMaterials/TL",
                "Intelligence Analysis/TL": "Intelligence Analysis/TL"}.items():
            sk = by_name.get(name)
            block = "\n".join(source.lines[sk.start:sk.end]) if sk else ""
            if not block.startswith(expected_start):
                failures.append(f"{name} did not bind to verified full heading")
        for original, (canonical, defaults) in TABLE_ROW_REPAIRS.items():
            sk = by_name.get(canonical)
            if not sk or not sk.tech_level or sk.defaults != defaults:
                failures.append(f"{original} table repair is not book-exact: {sk!r}")
        axe = by_name.get("Axe/Mace")
        axe_block = source.lines[axe.start:axe.end] if axe else []
        if not axe_block or not axe_block[0].startswith("Axe/Mace (DX/Average):") \
                or any(line == "Two-Handed" for line in axe_block):
            failures.append(f"Axe/Mace nested boundary leaked: {axe_block[-4:]!r}")
        flail = by_name.get("Two-Handed Flail")
        flail_block = source.lines[flail.start:flail.end] if flail else []
        if "Impact Weapons" in flail_block:
            failures.append("Two-Handed Flail absorbed the next Melee Weapon section")
        knife = by_name.get("Knife")
        knife_block = "\n".join(source.lines[knife.start:knife.end]) if knife else ""
        if "Gauche-3" not in knife_block or "Shortsword (DX/Average):" in knife_block:
            failures.append("Knife cross-page span is incomplete or crosses into Shortsword")
        brain = by_name.get("Brain Hacking/TL")
        brain_block = source.lines[brain.start:brain.end] if brain else []
        if brain_block != ["Brain Hacking", "see Brainwashing, below"]:
            failures.append(f"Brain Hacking cross-reference span {brain_block!r}")
        zen = by_name.get("Zen Archery")
        zen_block = source.lines[zen.start:zen.end] if zen else []
        if not zen_block or "SKILLS" in zen_block or any("TECHNIQUES" in x for x in zen_block):
            failures.append("Zen Archery crossed into the Techniques chapter")
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
