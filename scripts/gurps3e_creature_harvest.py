#!/usr/bin/env python3
"""gurps3e_creature_harvest.py — collate GURPS *3rd-edition* creature stat blocks.

THE PROCESS (Chad, 2026-08-28, extending the GURPS shelf sideways in EDITION):
this is a D&D 3.5e / GURPS 4e hybrid campaign, but the project WELCOMES other
editions so long as they are kept in their OWN clearly-labeled index — the
translator tools convert them. GURPS 3e monsters use a DIFFERENT attribute
grammar than 4e (ST/DX/IQ/HT primaries, then Speed-or-Move/Dodge, PD/DR — and
NO 4e-only Will/Per/FP/SM), so they get their OWN index, separate from the 4e
`gurps_creature_index`, and every row is stamped `system = "GURPS 3e"`.

    reference/gurps3e_creature_index.json — every GURPS 3e creature: name, book,
                                            PDF page, line span, system tag, and
                                            the 3e attribute block (ST, DX, IQ,
                                            HT, HP, Speed, Move, Dodge, PD, DR)
                                            plus Size/Weight/Damage/Reach/Habitat
    reference/gurps3e_creature_index.md    — the same index for human eyes

The raw text stays on I:\\Sourcebooks; `--export` emits a TRANSLATOR-READY packet
(verbatim block + provenance + parsed attributes). The GURPS-3e half is native;
the system-translator skill builds the paired D&D 3.5e (and 4e) statlines.

WORKFLOW
    python gurps3e_creature_harvest.py                    # (re)build the index
    python gurps3e_creature_harvest.py --search "dragon"  # find candidates
    python gurps3e_creature_harvest.py --export "Manticore"
    python gurps3e_creature_harvest.py --selftest

GOVERNING SOURCES  (I:\\Sourcebooks\\_text\\GURPS\\GURPS 3E\\)
    A GURPS 3e creature entry is a Title-Case OR ALL-CAPS name line, then the
    stat block whose first line is "ST: N" (N may be a range like "18-24").
    The 3e-specific signature is the derived-stat cluster near the ST line —
    "Move/Dodge: X/Y" or "Speed/Dodge: X/Y", "PD/DR: X/Y", plus Size / Weight /
    Damage / Reach / Habitat. Two physical layouts appear:
      * HORIZONTAL (Bestiary, Fantasy Bestiary): the derived stats ride ON the
        ST line — "ST: 18-24  Move/Dodge: 7/6  Size: 4-6" — with DX/IQ/HT below.
      * VERTICAL (Space Bestiary, Dinosaurs): every stat on its own line, and
        the label is "Speed/Dodge" rather than "Move/Dodge".
    One detector handles both: it anchors on the ST line, confirms the block by
    counting 3e stat markers in the window below, gathers the nearest name line
    above (rejecting running/section headers and OCR fragments), and reads the
    attributes out of the window. The OCR mangles labels (IQ->"1Q"/"10",
    HT->"H?", the "/" in "Move/Dodge"->"l"/"I"/"J"); the patterns tolerate that.
    A configured source whose file is missing prints NO COVERAGE. The PDFs stand
    behind every extraction — book RAW only, never invented.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CORPUS = Path(r"I:\Sourcebooks\_text")
REPO = Path(__file__).resolve().parent.parent
OUT_JSON = REPO / "reference" / "gurps3e_creature_index.json"
OUT_MD = REPO / "reference" / "gurps3e_creature_index.md"
SYSTEM = "GURPS 3e"

PAGE = re.compile(r"\[PDF page (\d+)\]")

# --- the ST anchor: a line that begins with ST and a number (ranges allowed) ---
ST_LINE = re.compile(r"^\s*ST:?\s*[-–]?\d")

# The OCR renders the "/" inside compound labels as any of / l I J 1 |.
SEP = r"[/lIJ1|]"

# --- 3e stat-block MARKERS (used to confirm an ST line begins a creature) ---
MOVEDODGE = re.compile(rf"(?:Move|Speed|Mave|Movc)\s*{SEP}\s*Dodge", re.I)
PDDR = re.compile(rf"\bPD\s*{SEP}\s*[DO]R", re.I)
HABITAT = re.compile(r"Habitats?\b", re.I)
REACH = re.compile(r"\bReach\b", re.I)
DAMAGE = re.compile(r"\b(?:Damage|Dmg)\b", re.I)
SIZEW = re.compile(r"\bSize\b", re.I)
WEIGHT = re.compile(r"\b(?:Weight|Wt)\b", re.I)
DX_LINE = re.compile(r"^\s*DX:?\s*[-–]?\d")
IQ_LINE = re.compile(r"^\s*(?:IQ|1Q|10|I0|lQ):?\s*[-–]?\d")
HT_LINE = re.compile(r"^\s*(?:HT|H[?T]):?\s*[-–]?\d")

WINDOW = 14        # lines below the ST line that a vertical stat block spans

# --- attribute PARSERS ------------------------------------------------------
P_ST = re.compile(r"^\s*ST:?\s*([0-9][0-9\-–.]*\+?)")
P_DX = re.compile(r"^\s*DX:?\s*([0-9][0-9\-–.]*)")
P_IQ = re.compile(r"^\s*(?:IQ|1Q|10|I0|lQ)\s*:?\s*([0-9][0-9\-–.]*)")
P_HT = re.compile(r"^\s*(?:HT|H[?T])\s*:?\s*([0-9][0-9\-–./]*)")
# derived pairs — require a REAL "/" or "|" between the two numbers so a
# slash-lost OCR value ("710") is left alone rather than mis-split into 7/10.
P_MOVE = re.compile(rf"(?:Move|Mave|Movc)\s*{SEP}?\s*Dodge[:\s.]*([0-9][0-9.]*)\s*[/|]\s*([0-9][0-9.]*)", re.I)
P_SPEED = re.compile(rf"Speed\s*{SEP}?\s*Dodge[:\s.]*([0-9][0-9.]*)\s*[/|]\s*([0-9][0-9.]*)", re.I)
P_PDDR = re.compile(rf"PD\s*{SEP}?\s*[DO]R[:\s.]*([0-9][0-9.]*)\s*[/|]\s*([0-9][0-9.]*)", re.I)

# descriptive fields: value = text after the label up to the next known label
# (OCR-tolerant: "Origi\w*" catches "Origim"), a footnote marker, a stray column
# colon, a 2+-space gap, or end of line.
_BOUND = (r"(?=[\s_]+(?:Move|Speed|Dodge|PD|DR|Size|Weight|Wt|Damage|Dmg|Origi\w*|"
          r"Reach|Habitats?|Time|Range)\b|\s+:|\s*[#*]|\s{2,}|$)")
P_SIZE = re.compile(r"\bSize:?\s*(.+?)" + _BOUND)
P_WEIGHT = re.compile(r"\b(?:Weight|Wt):?\s*(.+?)" + _BOUND)
P_DAMAGE = re.compile(r"\b(?:Damage|Dmg):?\s*(.+?)" + _BOUND)
P_REACH = re.compile(r"\bReach:?\s*(.+?)" + _BOUND)
P_HABITAT = re.compile(r"\bHabitats?:?\s*(.+?)" + _BOUND)
P_ORIGIN = re.compile(r"\bOrigin:?\s*(.+?)" + _BOUND)

# --- NAME filtering ---------------------------------------------------------
# A stat/attribute line, a section/running header, or front-matter is NOT a
# creature name. Anchored at the start of the (junk-stripped) candidate.
NAME_REJECT = re.compile(
    r"^(?:ST|DX|IQ|HT|H[?T]|PD|DR|1Q|10|I0|Move|Speed|Mave|Damage|Dmg|Reach|"
    r"Habitats?|Size|Weight|Wt|Origin|Time|Range|See|HP|SM|Sonar|Skills?|"
    r"Traits?|Discovered|"
    # section / running / front-matter headers seen in these OCR files
    r"Creatures|Adult|Dinosaurs?|Dragons?|Contents|Index|Introduction|"
    r"Bestiary|Glossary|Technical|Chapter|Appendix|Table|Player|Monsters?|"
    r"Animals?|Aquatic|Mammals?|Reptiles?|Birds?|Fish|Insects?|Plants?)\b",
    re.I)
CONNECTORS = {"of", "the", "and", "a", "an", "in", "to", "de", "la", "le", "du",
              "von", "van", "der", "des", "el", "y"}
TRAIL_DROP = {"see", "also"}  # trailing cross-reference words


def _clean_name(s: str) -> str:
    """Strip leading/trailing OCR noise and dangling fragments from a name."""
    s = re.sub(r"^[^A-Za-z]+", "", s)          # leading non-letters
    s = re.sub(r"[^A-Za-z)]+$", "", s)          # trailing junk (keep a ')')
    s = re.sub(r"\s+", " ", s).strip()
    parts = s.split()
    # drop a trailing 1-2 char lowercase OCR fragment, or a cross-ref word
    while len(parts) >= 2 and (re.fullmatch(r"[a-z]{1,2}", parts[-1])
                               or parts[-1].lower() in TRAIL_DROP):
        parts.pop()
    return " ".join(parts)


def _name_like(raw: str) -> Optional[str]:
    """Return the cleaned creature name if `raw` looks like one, else None.
    Names are Title-Case or ALL-CAPS, 1-5 words, mostly alphabetic; case is
    PRESERVED (ALL-CAPS dinosaur genera stay ALL-CAPS)."""
    s = raw.strip()
    if ":" in s:                               # stat lines carry a colon
        return None
    if MOVEDODGE.search(s) or PDDR.search(s):  # a leaked derived-stat line
        return None
    nm = _clean_name(s)
    if not (2 <= len(nm) <= 40):
        return None
    if NAME_REJECT.match(nm):
        return None
    words = nm.split()
    if not (1 <= len(words) <= 5):
        return None
    if sum(c.isalpha() for c in nm) < len(nm) * 0.6:
        return None
    # The lead word must begin with a capital (its alpha core, so a trailing
    # comma in a "Category, Subtype" name like "Ant, Giant" is fine); a
    # lowercase-lead OCR fragment ("ca BR es", "eA U RE") is rejected.
    w0core = re.sub(r"[^A-Za-z’']", "", words[0])
    if not w0core or not w0core[0].isupper():
        return None
    for w in words:                            # every significant word capitalized
        core = re.sub(r"[^A-Za-z]", "", w)
        if not core or w.lower().strip(",.") in CONNECTORS:
            continue
        if not core[0].isupper():
            return None
    return nm


def _name_above(lines: List[str], st_idx: int) -> Optional[Tuple[int, str]]:
    """Nearest creature-name line above the ST anchor (within a short climb),
    skipping blanks, page markers, and rejected headers/fragments. A 1-2 char
    candidate (e.g. an OCR remnant "EL" sitting just under the real "Slasher
    Fish") is only taken as a LAST resort — a longer valid name found higher in
    the climb wins — so a genuine short name ("Al", "Su") still survives when it
    is the only name there."""
    j, steps = st_idx - 1, 0
    fallback: Optional[Tuple[int, str]] = None
    while j >= 0 and steps < 4:
        raw = lines[j]
        if raw.strip() == "" or PAGE.search(raw):
            j -= 1
            continue
        steps += 1
        nm = _name_like(raw)
        if nm:
            if len(nm) >= 3:
                return j, nm
            if fallback is None:
                fallback = (j, nm)
        j -= 1
    return fallback


@dataclass
class Gurps3eCreature:
    name: str
    book: str
    page: Optional[int]
    start: int
    end: int
    system: str = SYSTEM
    ST: Optional[str] = None
    DX: Optional[str] = None
    IQ: Optional[str] = None
    HT: Optional[str] = None
    HP: Optional[str] = None       # 3e lists creature HP as the "HT: X/Y" tail
    Speed: Optional[str] = None
    Move: Optional[str] = None
    Dodge: Optional[str] = None
    PD: Optional[str] = None       # passive defense (3e-only)
    DR: Optional[str] = None
    Size: Optional[str] = None
    Weight: Optional[str] = None
    Damage: Optional[str] = None
    Reach: Optional[str] = None
    Habitat: Optional[str] = None
    Origin: Optional[str] = None

    def quick_fields(self) -> int:
        return sum(1 for k in ("ST", "DX", "IQ", "HT")
                   if getattr(self, k) is not None)


def _grab(win_text_lines: List[str], rx: re.Pattern) -> Optional[str]:
    for ln in win_text_lines:
        m = rx.search(ln)
        if m:
            v = re.sub(r"\s+", " ", m.group(1)).strip(" .,:;#*_-|/")
            if v:
                return v
    return None


def parse_attrs(c: Gurps3eCreature, win: List[str]) -> None:
    """Read the 3e attribute block out of the window lines below the name."""
    for ln in win:
        if c.ST is None:
            m = P_ST.match(ln)
            if m:
                c.ST = m.group(1).rstrip(".")
        if c.DX is None:
            m = P_DX.match(ln)
            if m:
                c.DX = m.group(1).rstrip(".")
        if c.IQ is None:
            m = P_IQ.match(ln)
            if m:
                c.IQ = m.group(1).rstrip(".")
        if c.HT is None:
            m = P_HT.match(ln)
            if m:
                c.HT = m.group(1).rstrip(".")
    # 3e writes big-creature hit points as the tail of "HT: <HT>/<HP>".
    if c.HT and "/" in c.HT:
        c.HP = c.HT.split("/", 1)[1]

    text = "\n".join(win)
    m = P_MOVE.search(text)
    if m:
        c.Move, c.Dodge = m.group(1), m.group(2)
    m = P_SPEED.search(text)
    if m:
        c.Speed = m.group(1)
        if c.Dodge is None:
            c.Dodge = m.group(2)
    m = P_PDDR.search(text)
    if m:
        c.PD, c.DR = m.group(1), m.group(2)

    c.Size = _grab(win, P_SIZE)
    c.Weight = _grab(win, P_WEIGHT)
    c.Damage = _grab(win, P_DAMAGE)
    c.Reach = _grab(win, P_REACH)
    c.Habitat = _grab(win, P_HABITAT)
    c.Origin = _grab(win, P_ORIGIN)


def _is_stat_block(lines: List[str], i: int, n: int) -> bool:
    """An ST line begins a 3e creature stat block if >= 3 distinct 3e stat
    markers appear in the window below it (tolerant of OCR-mangled labels)."""
    win = lines[i:min(n, i + WINDOW)]
    text = "\n".join(win)
    m = 0
    m += bool(MOVEDODGE.search(text))
    m += bool(PDDR.search(text))
    m += bool(HABITAT.search(text))
    m += bool(REACH.search(text))
    m += bool(DAMAGE.search(text))
    m += bool(SIZEW.search(text))
    m += bool(WEIGHT.search(text))
    m += any(DX_LINE.match(ln) for ln in win)
    m += any(IQ_LINE.match(ln) for ln in win)
    m += any(HT_LINE.match(ln) for ln in win)
    return m >= 3


def _finalize(creatures: List[Gurps3eCreature]) -> List[Gurps3eCreature]:
    """Drop running headers (a name recurring 3+ times is a page/section header,
    not a creature) and collapse exact duplicate names to the first."""
    cnt = Counter(c.name.lower() for c in creatures)
    out, seen = [], set()
    for c in creatures:
        key = c.name.lower()
        if cnt[key] >= 3 or key in seen:
            continue
        seen.add(key)
        out.append(c)
    return out


def detect_gurps3e_creatures(lines: List[str], pages: List[int],
                             book: str) -> List[Gurps3eCreature]:
    n = len(lines)
    starts: List[Tuple[int, str, int]] = []   # (name_line, name, st_idx)
    used = set()
    for i, ln in enumerate(lines):
        if not ST_LINE.match(ln) or not _is_stat_block(lines, i, n):
            continue
        got = _name_above(lines, i)
        if got is None or got[0] in used:
            continue
        nj, name = got
        used.add(nj)
        starts.append((nj, name, i))

    starts.sort()
    creatures: List[Gurps3eCreature] = []
    for k, (nj, name, st_idx) in enumerate(starts):
        e = starts[k + 1][0] if k + 1 < len(starts) else min(n, nj + 80)
        e = min(e, nj + 80)
        c = Gurps3eCreature(name=name, book=book, page=pages[nj], start=nj, end=e)
        parse_attrs(c, lines[st_idx:min(n, st_idx + WINDOW)])
        creatures.append(c)
    return _finalize(creatures)


@dataclass
class Source:
    key: str
    book: str
    path: Path
    citation: str
    coverage: str = "pending"
    lines: List[str] = field(default_factory=list)
    creatures: List[Gurps3eCreature] = field(default_factory=list)


_G3 = "GURPS/GURPS 3E"
SOURCES: List[Source] = [
    Source("bestiary", "GURPS Bestiary (3e)",
           Path(f"{_G3}/gurps 3e - bestiary.md"),
           "GURPS Bestiary (SJGames, 3e)"),
    Source("fantasybestiary", "GURPS Fantasy Bestiary (3e)",
           Path(f"{_G3}/gurps 3e - fantasy bestiary [missing p. 72].md"),
           "GURPS Fantasy Bestiary (SJGames, 3e), mythical creatures"),
    Source("spacebestiary", "GURPS Space Bestiary (3e)",
           Path(f"{_G3}/gurps 3e - space bestiary.md"),
           "GURPS Space Bestiary (SJGames, 3e), alien flora & fauna"),
    Source("dinosaurs", "GURPS Dinosaurs (3e)",
           Path(f"{_G3}/gurps 3e - dinosaurs.md"),
           "GURPS Dinosaurs (SJGames, 3e), prehistoric bestiary"),
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
    return [Source(s.key, s.book, s.path, s.citation) for s in SOURCES]


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
            src.creatures = detect_gurps3e_creatures(src.lines, pages, src.book)
            src.coverage = f"ok — {len(src.creatures)} creatures from {path.name}"

    def all_creatures(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for c in src.creatures:
                yield src, c

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, c in self.all_creatures(book):
            nm = c.name.lower()
            if nm == q:
                exact.append((src, c))
            elif q in nm:
                partial.append((src, c))
        return exact if exact else partial


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# GURPS 3e CREATURE INDEX — The New Path",
        "",
        "**Generated by `scripts/gurps3e_creature_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** One row per GURPS *3rd-edition* creature — the 3e",
        "attribute block (ST/DX/IQ/HT, Speed-or-Move/Dodge, PD/DR), kept SEPARATE",
        "from the 4e `gurps_creature_index`. Every row is tagged",
        f"`system = \"{SYSTEM}\"` so the translator tools know which edition they are",
        "reading. The raw text stays on `I:\\Sourcebooks` — use `--export \"NAME\"`",
        "for the translator-ready packet. A field left as `—` is one the OCR did",
        "not cleanly yield; PD is the 3e-only passive defense; a compound `HT` like",
        "`12/20-26` is HT / hit-points as the book prints it.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.creatures)
        parsed_well += sum(1 for c in src.creatures if c.quick_fields() >= 3)
        sources_out.append({"key": src.key, "book": src.book, "system": SYSTEM,
                            "citation": src.citation, "coverage": src.coverage,
                            "creatures": [asdict(c) for c in src.creatures]})
        md.append(f"## {src.book} — {len(src.creatures)} creatures")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*System: {SYSTEM}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.creatures:
            md.append("| Creature | ST | DX | IQ | HT | Spd/Move | Dodge | PD | DR "
                      "| Damage | Habitat | Page |")
            md.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
            for c in src.creatures:
                spd = c.Speed or c.Move
                cells = [c.ST, c.DX, c.IQ, c.HT, spd, c.Dodge, c.PD, c.DR,
                         c.Damage, c.Habitat]
                md.append("| " + c.name + " | "
                          + " | ".join((x or "—") for x in cells)
                          + f" | {c.page if c.page is not None else '—'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/gurps3e_creature_harvest.py",
                    "system": SYSTEM, "corpus": str(corpus.base),
                    "total_creatures": total, "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str],
                  out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 6:
        print(f"'{name}' matches {len(hits)} creatures; narrow with --book or the exact name:")
        for src, c in hits[:20]:
            print(f"  {c.name}   [{c.book}, p.{c.page}]")
        return 1
    packets = []
    for src, c in hits:
        body = [ln for ln in src.lines[c.start:c.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "gurps3e-creature-for-translation",
            "instructions": (
                "A native GURPS 3rd-edition creature. Its GURPS-3e half is here; "
                "the system-translator skill builds the paired D&D 3.5e (and "
                "GURPS 4e) statlines. 3e uses PD (passive defense) and a compound "
                "'HT: HT/HP'; there is no 4e Will/Per/FP/SM. The raw_block is OCR "
                "text — check oddities against the source PDF."
            ),
            "name": c.name,
            "system": SYSTEM,
            "source": {"book": c.book, "pdf_page": c.page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [c.start + 1, c.end], "citation": src.citation},
            "parsed": {k: v for k, v in asdict(c).items()
                       if k in ("ST", "DX", "IQ", "HT", "HP", "Speed", "Move",
                                "Dodge", "PD", "DR", "Size", "Weight", "Damage",
                                "Reach", "Habitat", "Origin") and v},
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


# An embedded fixture exercising BOTH 3e layouts, the running-header reject, and
# the OCR-mangled labels (1Q for IQ, H? for HT, SpeedIDodge with an 'I' slash).
FIXTURE = """## [PDF page 5]
Alligator
Creatures of the Wild

ST: 18-24 Move/Dodge: 7/6 Size: 4-6
DX: 12 PD/DR: 3/4 Weight: 700 lbs.
1Q: 4 Damage: 1d+1 cut Origin: R
H?: 12/20-26 Reach: C Habitats: FW, S

Alligators are large reptiles native to rivers.

DIMETRODON
ST: 25-30
SpeedIDodge: 5/5
Size: 3-4
DX: 10
PD/DR: 2/3
Wt: 500 lbs.
IQ: 3
Damage: 2d cut
HT: 13/25-30
Reach: C
Time: Permian
Habitat: SW
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    lines = FIXTURE.splitlines()
    creatures = detect_gurps3e_creatures(lines, _pages_for(lines),
                                         "GURPS Bestiary (3e)")
    names = [c.name for c in creatures]
    # "Alligator" (horizontal) and "DIMETRODON" (vertical, case preserved) are
    # creatures; "Creatures of the Wild" running header is rejected.
    if names != ["Alligator", "DIMETRODON"]:
        failures.append(f"fixture detected {names}, wanted "
                        f"['Alligator', 'DIMETRODON'] "
                        f"(running header rejected; ALL-CAPS case preserved)")
    else:
        gator = creatures[0]
        got = (gator.ST, gator.DX, gator.IQ, gator.HT, gator.HP,
               gator.Move, gator.Dodge, gator.PD, gator.DR)
        want = ("18-24", "12", "4", "12/20-26", "20-26", "7", "6", "3", "4")
        if got != want:
            failures.append(f"Alligator attrs {got}, wanted {want} "
                            f"(1Q->IQ, H?->HT, HP split from HT/HP)")
        if gator.Habitat != "FW, S" or gator.Damage != "1d+1 cut":
            failures.append(f"Alligator desc Damage={gator.Damage!r} "
                            f"Habitat={gator.Habitat!r}, wanted '1d+1 cut' / 'FW, S'")
        dim = creatures[1]
        # SpeedIDodge (OCR 'I' slash) -> Speed 5, Dodge 5; PD/DR 2/3.
        if (dim.ST, dim.Speed, dim.Dodge, dim.PD, dim.DR) != ("25-30", "5", "5", "2", "3"):
            failures.append(f"Dimetrodon attrs "
                            f"{(dim.ST, dim.Speed, dim.Dodge, dim.PD, dim.DR)}, "
                            f"wanted ('25-30','5','5','2','3')")
        if dim.system != SYSTEM or gator.system != SYSTEM:
            failures.append(f"system tag not '{SYSTEM}'")

    if base.is_dir() and (base / SOURCES[0].path).exists():
        corpus = Corpus(base, _fresh_sources())
        total = sum(len(s.creatures) for s in corpus.sources)
        if total < 400:
            failures.append(f"only {total} GURPS 3e creatures indexed; expected "
                            f">400 across the 4 bestiaries (task floor ~100)")
        # a few known creatures, one per book, with a stat spot-check
        gator = corpus.find("alligator", book="bestiary")
        if not gator:
            failures.append("Alligator not found in live Bestiary")
        elif gator[0][1].ST != "18-24":
            failures.append(f"live Alligator ST={gator[0][1].ST!r}, wanted 18-24")
        man = corpus.find("manticore", book="fantasybestiary")
        if not man:
            failures.append("Manticore not found in live Fantasy Bestiary")
        elif man[0][1].ST != "20-25":
            failures.append(f"live Manticore ST={man[0][1].ST!r}, wanted 20-25")
        if not corpus.find("tyrannosaurus", book="dinosaurs"):
            failures.append("Tyrannosaurus not found in live Dinosaurs")
        if not corpus.find("leviathan", book="spacebestiary"):
            failures.append("Leviathan not found in live Space Bestiary")
        # quick_fields must work and be populated for the bulk of the harvest
        well = sum(1 for s in corpus.sources for c in s.creatures
                   if c.quick_fields() >= 3)
        if well < total * 0.8:
            failures.append(f"only {well}/{total} creatures have 3+ primaries "
                            f"parsed; expected >=80%")
    else:
        print("  [SKIP] GURPS 3e bestiary extractions not found — fixture checks only")

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
        found = sorted({(c.name, c.book, c.page or -1, c.ST or "—")
                        for _, c in corpus.all_creatures(args.book)
                        if q in c.name.lower()})
        for name, bk, page, st in found:
            loc = bk if page < 0 else f"{bk}, p.{page}"
            print(f"  {name}   [ST {st}; {loc}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.creatures for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.creatures):4d} creatures" if src.creatures else "   0 creatures"
        print(f"  {src.book:34s} {status}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} GURPS 3e creatures across "
          f"{sum(1 for s in corpus.sources if s.creatures)} book(s); "
          f"{parsed_well} with 3+ primaries parsed.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
