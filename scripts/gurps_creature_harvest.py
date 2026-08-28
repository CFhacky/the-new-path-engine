#!/usr/bin/env python3
"""gurps_creature_harvest.py — collate GURPS 4e creature stat blocks.

THE PROCESS (Chad, 2026-08-27, continuing the GURPS shelf after
gurps_magic_harvest.py): this is a D&D 3.5e / GURPS 4e HYBRID campaign, and the
GURPS side needs a bestiary as much as the spell list. GURPS monsters live in
their own attribute grammar (ST/DX/IQ/HT/HP/Will/Per/Speed/Move/SM/DR), so they
get their OWN index, separate from the D&D `creature_index`.

    reference/gurps_creature_index.json  — every GURPS creature: name, book,
                                           PDF page, line span, and the
                                           attribute block (ST, DX, IQ, HT, HP,
                                           Will, Per, Speed, Move, SM, DR)
    reference/gurps_creature_index.md     — the same index for human eyes

The raw text stays on I:\\Sourcebooks; `--export` emits a TRANSLATOR-READY
packet (verbatim block + provenance + parsed attributes). For a GURPS creature
the GURPS half is native; the system-translator skill builds the D&D 3.5e half.

WORKFLOW
    python gurps_creature_harvest.py                   # (re)build the index
    python gurps_creature_harvest.py --search "demon"  # find candidates
    python gurps_creature_harvest.py --export "Bugbear"
    python gurps_creature_harvest.py --selftest

GOVERNING SOURCES
    I:\\Sourcebooks\\_text\\GURPS\\GURPS 4e\\ — the GURPS bestiary books
    (Dungeon Fantasy Monsters 1, Creatures of the Night Vol.1-5, Fantasy). A
    GURPS creature is an ALL-CAPS NAME header, then a description, then the
    attribute block whose first line is "ST: N" with "DX:", "IQ:", and "HT:"
    close below. Detection anchors on that attribute block and gathers the
    nearest ALL-CAPS name header above it (skipping the description prose and
    the "THE MONSTERS" running header, joining a name wrapped across lines like
    "DEMON FROM" / "BETWEEN THE STARS"). A configured source whose file is
    missing prints NO COVERAGE. The PDFs stand behind every extraction.
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
OUT_JSON = REPO / "reference" / "gurps_creature_index.json"
OUT_MD = REPO / "reference" / "gurps_creature_index.md"

PAGE = re.compile(r"\[PDF page (\d+)\]")

ST_LINE = re.compile(r"^ST:?\s*-?\d")
_ATTR = {k: re.compile(rf"^{k}:?\s*(-?[\d.]+)")
         for k in ("ST", "DX", "IQ", "HT", "HP", "Will", "Per", "FP",
                   "Speed", "Move", "SM", "DR", "Dodge", "Parry")}

# An ALL-CAPS creature name header. Names wrap across lines ("DEMON FROM" /
# "BETWEEN THE STARS"). Running/section headers are rejected.
NAME_HEADER = re.compile(r"^[A-Z][A-Z0-9 '\u2019\-]{2,32}$")
NAME_REJECT = re.compile(
    r"^(THE MONSTERS|CHAPTER|GURPS|STEVE JACKSON|ABOUT THE|CONTENTS|"
    r"INTRODUCTION|INDEX|THE END|APPENDIX|BESTIARY|THE AUTHORS?|"
    r"PLAYTESTERS?|ILLUSTRAT|DEDICAT|GLOSSARY|NEW |WORLDS?|EQUIPMENT|"
    r"IMAGINARY|ARCANA|SPECIES|TEMPLATES?|CAMPAIGN|SETTING|"
    # section / NPC-category / location headers that carry a stat block nearby
    r"CREATURES?$|CHARACTERS?|WARRIORS?$|SPELLCASTERS?|THIEVES|NPCS?|"
    r"SERVITORS|MONSTRES|MASTERING|TALES|EXPLORING|BENEATH|HERE BE|"
    r"LANDS OUT|SPIRITS AND|THE LEGION|THE NORTHLAND|THE PRIESTHOOD|"
    r"KNIGHTS AND|THE TROOPS|THE RAVENS|THE GUARD|MILITIA|BANDITS|"
    r"DECK |CABIN|MASTERS?|COMBATANTS?|VILLAINS?|ALLIES$|HENCHMEN$|"
    r"OTHER |THINGS |DRUIDIC|FAMILIARS$|ELEMENTALS$|WISDOM$)\b")


@dataclass
class GurpsCreature:
    name: str
    book: str
    page: Optional[int]
    start: int
    end: int
    ST: Optional[str] = None
    DX: Optional[str] = None
    IQ: Optional[str] = None
    HT: Optional[str] = None
    HP: Optional[str] = None
    Will: Optional[str] = None
    Per: Optional[str] = None
    FP: Optional[str] = None
    Speed: Optional[str] = None
    Move: Optional[str] = None
    SM: Optional[str] = None
    DR: Optional[str] = None
    Dodge: Optional[str] = None
    Parry: Optional[str] = None
    ctype: Optional[str] = None       # the type/traits line ("Vermiform, Wild Animal")
    origin: Optional[str] = None      # the book a compilation credits for this creature

    def quick_fields(self) -> int:
        return sum(1 for k in ("ST", "DX", "IQ", "HT", "HP")
                   if getattr(self, k) is not None)


def _finalize(creatures: List["GurpsCreature"]) -> List["GurpsCreature"]:
    """Drop running headers (a name that recurs 3+ times is a page/section
    header, not a creature) and collapse exact duplicate names to the first."""
    from collections import Counter
    cnt = Counter(c.name.lower() for c in creatures)
    out, seen = [], set()
    for c in creatures:
        key = c.name.lower()
        if cnt[key] >= 3 or key in seen:
            continue
        seen.add(key)
        out.append(c)
    return out


def _is_block(lines: List[str], i: int, n: int) -> bool:
    """An ST line that begins an attribute block: DX, IQ, and HT appear within
    the next several content lines."""
    seen = set()
    j, c = i + 1, 0
    while j < n and c < 14:
        s = lines[j].strip()
        if s:
            c += 1
            for k in ("DX", "IQ", "HT"):
                if _ATTR[k].match(s):
                    seen.add(k)
        j += 1
    return len(seen) >= 3


def _name_above(lines: List[str], st_idx: int) -> Optional[Tuple[int, str]]:
    """Nearest ALL-CAPS creature-name header above the attribute block, past the
    mixed-case description and the running header. Joins a wrapped name."""
    j, steps = st_idx - 1, 0
    while j >= 0 and steps < 70:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            j -= 1
            continue
        steps += 1
        if NAME_HEADER.match(s) and not NAME_REJECT.match(s):
            frags, top = [s], j
            k, gap = j - 1, 0
            while k >= 0 and len(frags) < 3:
                t = lines[k].strip()
                if t == "" or PAGE.search(lines[k]):
                    gap += 1
                    if gap > 1:
                        break
                    k -= 1
                    continue
                if NAME_HEADER.match(t) and not NAME_REJECT.match(t):
                    frags.insert(0, t)
                    top, gap = k, 0
                    k -= 1
                    continue
                break
            return top, re.sub(r"\s+", " ", " ".join(frags)).strip().title()
        j -= 1  # keep climbing past description prose
    return None


def parse_attrs(creature: GurpsCreature, body_lines: List[str]) -> None:
    for raw in body_lines:
        line = raw.strip()
        if not line:
            continue
        for k, rx in _ATTR.items():
            if getattr(creature, k) is None:
                m = rx.match(line)
                if m:
                    setattr(creature, k, m.group(1))
                    break


def detect_gurps_creatures(lines: List[str], pages: List[int], book: str) -> List[GurpsCreature]:
    n = len(lines)
    starts: List[Tuple[int, str, int]] = []
    used = set()
    for i, ln in enumerate(lines):
        if not ST_LINE.match(ln.strip()) or not _is_block(lines, i, n):
            continue
        got = _name_above(lines, i)
        if got is None or got[0] in used:
            continue
        top, name = got
        used.add(top)
        starts.append((top, name, i))

    starts.sort()
    creatures: List[GurpsCreature] = []
    for k, (top, name, st_idx) in enumerate(starts):
        e = starts[k + 1][0] if k + 1 < len(starts) else min(n, top + 90)
        e = min(e, top + 90)
        c = GurpsCreature(name=name, book=book, page=pages[top], start=top, end=e)
        parse_attrs(c, lines[st_idx:e])   # attributes are at/after the ST line
        creatures.append(c)
    return _finalize(creatures)


# A second GURPS stat-block format (Fantasy, Creatures of the Night): the
# attributes are inline and semicolon-separated, without colons —
# "ST 20; DX 12; IQ 0; HT 12." then "Will 0; Per 12; Speed 6; Move 0."
INLINE_ST = re.compile(r"^ST\s+[-+]?\d+\s*;")
INLINE_PAIR = re.compile(
    r"\b(ST|DX|IQ|HT|HP|Will|Per|FP|Speed|Move|SM|DR|Dodge|Parry)\s+([-+]?[\d.]+)")


def detect_gurps_inline(lines: List[str], pages: List[int], book: str) -> List[GurpsCreature]:
    n = len(lines)
    starts: List[Tuple[int, str, int]] = []
    used = set()
    for i, ln in enumerate(lines):
        if not INLINE_ST.match(ln.strip()):
            continue
        got = _name_above(lines, i)
        if got is None or got[0] in used:
            continue
        top, name = got
        used.add(top)
        starts.append((top, name, i))

    starts.sort()
    creatures: List[GurpsCreature] = []
    for k, (top, name, si) in enumerate(starts):
        e = starts[k + 1][0] if k + 1 < len(starts) else min(n, top + 90)
        e = min(e, top + 90)
        c = GurpsCreature(name=name, book=book, page=pages[top], start=top, end=e)
        for raw in lines[si:min(n, si + 6)]:
            for attr, val in INLINE_PAIR.findall(raw):
                if getattr(c, attr) is None:
                    setattr(c, attr, val.rstrip("."))   # drop the sentence period
        creatures.append(c)
    return _finalize(creatures)


# A third format (GURPS Fantasy): inline stats but Title-Case creature names,
# not ALL-CAPS, with the name sitting far above a long description. The reliable
# signal is that the creature's name ECHOES lowercased in its own description
# ("the manticore has the face…"); a full ST;DX;IQ;HT block rules out the prose
# "ST N;" lines (weather, rules examples), and a frequency guard rejects a
# repeated TOPIC word ("Christianity") that is not a creature name.
FULL_INLINE_ST = re.compile(
    r"^ST\s+[-+]?\d+;\s*DX\s+[-+]?\d+;\s*IQ\s+[-+]?\d+;\s*HT\s+[-+]?\d+", re.IGNORECASE)
TC_REJECT = re.compile(
    r"^(The|A|An|This|These|Its|In|On|If|When|Roll|See|GURPS|Chapter|Bestiary|"
    r"Worlds?|Equipment|Combat|Roma|Imaginary|Species|Traits?|Skills?|New|"
    r"Weapons?|Armou?r|Table|Notes?|Christianity|Rome|Judaism)\b")


def _tc_candidate(s: str) -> bool:
    if not (3 <= len(s) <= 32) or s.isupper():
        return False
    if s.endswith((".", ",", ";", ":", "?", "!", "-", "–")):
        return False
    ws = s.split()
    if not (1 <= len(ws) <= 4) or not all(w[0].isupper() for w in ws if w):
        return False
    if TC_REJECT.match(s):
        return False
    return sum(c.isalpha() for c in s) >= len(s) * 0.7


def _echo_name_above(lines: List[str], st_idx: int) -> Optional[Tuple[int, str]]:
    from collections import Counter
    freq: Counter = Counter()
    j, steps = st_idx - 1, 0
    while j >= 0 and steps < 40:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            j -= 1
            continue
        steps += 1
        if _tc_candidate(s):
            first = re.sub(r"[^a-z]", "", s.split()[0].lower())
            # <=6: a creature name echoes a handful of times in its own
            # description (Panther: 4); a repeated TOPIC word (Christianity: 10)
            # echoes far more and is rejected.
            if first and freq[first] <= 6 and (
                    first in freq or first.rstrip("s") in freq or first + "s" in freq):
                return j, re.sub(r"\s+", " ", s).strip()
        for w in re.findall(r"[a-z]{3,}", s.lower()):
            freq[w] += 1
        j -= 1
    return None


def detect_gurps_titlecase(lines: List[str], pages: List[int], book: str) -> List[GurpsCreature]:
    n = len(lines)
    starts: List[Tuple[int, str, int]] = []
    used = set()
    for i, ln in enumerate(lines):
        if not FULL_INLINE_ST.match(ln.strip()):
            continue
        got = _echo_name_above(lines, i)
        if got is None or got[0] in used:
            continue
        top, name = got
        used.add(top)
        starts.append((top, name, i))

    starts.sort()
    creatures: List[GurpsCreature] = []
    for k, (top, name, si) in enumerate(starts):
        e = starts[k + 1][0] if k + 1 < len(starts) else min(n, top + 90)
        e = min(e, top + 90)
        c = GurpsCreature(name=name, book=book, page=pages[top], start=top, end=e)
        for raw in lines[si:min(n, si + 6)]:
            for attr, val in INLINE_PAIR.findall(raw):
                if getattr(c, attr) is None:
                    setattr(c, attr, val.rstrip("."))   # drop the sentence period
        creatures.append(c)
    return _finalize(creatures)


# A fourth format (GURPS 4e Natural Encyclopedia — a 4e-stat bestiary compilation):
# vertical "ST: N" stats like the DF-Monsters format, but the name is Title-Case
# with a type/traits line between the name and the ST line, and each entry ends
# with a "Source: GURPS <book>" credit. Layout per creature:
#   <Name> / <type-line> / ST: N / HP: N / … / Source: GURPS <book>
SOURCE_LINE = re.compile(r"^Source:\s*(.+)$", re.IGNORECASE)
# The encyclopedia names creatures "Category, Subtype" ("Ant, Giant"; "Baboon,
# Chacma"; "Basilisk, Greater"), so commas/parens are part of the name.
ENC_NAME = re.compile(r"^[A-ZÀ-Þ][A-Za-zÀ-ÿ0-9'’\-.,()/ ]{1,44}$")
ENC_NAME_REJECT = re.compile(
    r"^(Source|Author|Combat|Physical|Social|Mental|Special|Traits?|Skills?|"
    r"Notes?|Habitat|Also|Reach|Bite|Claws?|Sting|Tail|See|Only|Roll|This|The|"
    r"Weapon|Attack|Armou?r|Move|Speed|Dodge|Parry|Table|Range|"
    # type/traits lines (never a creature name in the 2nd-above slot)
    r"Wild Animal|Insect|Quadruped|Reptile|Fish|Bird|Mammal|Amphibian|Vermiform|"
    r"Flying|Aquatic|Hybrid|Winged|Domesticated|Mythical|Constructed|Elemental|"
    r"Humanoid|Avian|Piscine|Serpentine|Arthropod|Crustacean|Mollusc|Cephalopod|"
    r"Plant|Fungus|Ooze|Spirit|Undead|Machine)\b", re.IGNORECASE)


def detect_gurps_encyclopedia(lines: List[str], pages: List[int], book: str) -> List[GurpsCreature]:
    n = len(lines)
    starts: List[Tuple[int, str, str, int]] = []
    used = set()
    for i, ln in enumerate(lines):
        if not ST_LINE.match(ln.strip()) or not _is_block(lines, i, n):
            continue
        above: List[Tuple[int, str]] = []          # the two non-blank lines above ST
        j = i - 1
        while j >= 0 and len(above) < 2:
            s = lines[j].strip()
            if s == "" or PAGE.search(lines[j]):
                j -= 1
                continue
            above.append((j, s))
            j -= 1

        def _ok(txt: str) -> bool:
            return bool(ENC_NAME.match(txt)) and not ENC_NAME_REJECT.match(txt)

        # Two layouts: usually Name / type-line / ST (name is the 2nd line above);
        # some creatures carry no type-line, so Name / ST (name is 1st above).
        nj = name = tline = None
        if len(above) >= 2 and _ok(above[1][1]):
            nj, name, tline = above[1][0], above[1][1], above[0][1]
        elif len(above) >= 1 and _ok(above[0][1]):
            nj, name = above[0]
        if name is None or nj in used:
            continue
        used.add(nj)
        starts.append((nj, name, tline, i))

    starts.sort()
    creatures: List[GurpsCreature] = []
    for k, (nj, name, tline, st_idx) in enumerate(starts):
        e = starts[k + 1][0] if k + 1 < len(starts) else min(n, nj + 80)
        e = min(e, nj + 80)
        c = GurpsCreature(name=name.strip(), book=book, page=pages[nj],
                          start=nj, end=e, ctype=tline)
        parse_attrs(c, lines[st_idx:e])
        for raw in lines[st_idx:e]:
            m = SOURCE_LINE.match(raw.strip())
            if m:
                c.origin = re.sub(r"\s+", " ", m.group(1)).strip()
                break
        creatures.append(c)
    return _finalize(creatures)


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[GurpsCreature]]] = {
    "gurps": detect_gurps_creatures,          # vertical "ST: N" (DF Monsters)
    "gurps_inline": detect_gurps_inline,      # inline "ST N; …", ALL-CAPS names (CotN)
    "gurps_titlecase": detect_gurps_titlecase,  # inline stats, Title-Case names (Fantasy)
    "gurps_encyclopedia": detect_gurps_encyclopedia,  # vertical stats, Title name + type line
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
    creatures: List[GurpsCreature] = field(default_factory=list)


_G = "GURPS/GURPS 4e"
SOURCES: List[Source] = [
    Source("dfm1", "GURPS Dungeon Fantasy Monsters 1",
           Path(f"{_G}/GURPS 4e - Dungeon Fantasy Monsters 1.md"),
           "GURPS Dungeon Fantasy Monsters 1 (SJGames, 4e)", "gurps"),
    Source("fantasy", "GURPS Fantasy",
           Path(f"{_G}/GURPS 4e - Fantasy.md"),
           "GURPS Fantasy (SJGames, 4e), bestiary", "gurps_titlecase"),
    Source("cotn1", "GURPS Creatures of the Night 1",
           Path(f"{_G}/GURPS 4e - Creatures of the Night Vol.1.md"),
           "GURPS Creatures of the Night Vol.1 (SJGames, 4e)", "gurps_inline"),
    Source("cotn2", "GURPS Creatures of the Night 2",
           Path(f"{_G}/GURPS 4e - Creatures of the Night Vol.2.md"),
           "GURPS Creatures of the Night Vol.2 (SJGames, 4e)", "gurps_inline"),
    Source("cotn3", "GURPS Creatures of the Night 3",
           Path(f"{_G}/GURPS 4e - Creatures of the Night Vol.3.md"),
           "GURPS Creatures of the Night Vol.3 (SJGames, 4e)", "gurps_inline"),
    Source("cotn4", "GURPS Creatures of the Night 4",
           Path(f"{_G}/GURPS 4e - Creatures of the Night Vol.4.md"),
           "GURPS Creatures of the Night Vol.4 (SJGames, 4e)", "gurps_inline"),
    Source("cotn5", "GURPS Creatures of the Night 5",
           Path(f"{_G}/GURPS 4e - Creatures of the Night Vol.5.md"),
           "GURPS Creatures of the Night Vol.5 (SJGames, 4e)", "gurps_inline"),
    Source("lands", "GURPS Lands Out Of Time",
           Path(f"{_G}/GURPS 4e - Lands Out Of Time.md"),
           "GURPS Lands Out of Time (SJGames, 4e), prehistoric bestiary", "gurps_inline"),
    Source("banestorm", "GURPS Banestorm",
           Path(f"{_G}/GURPS 4e - Banestorm.md"),
           "GURPS Banestorm (SJGames, 4e), bestiary", "gurps_inline"),
    Source("dfallies", "GURPS Dungeon Fantasy 5 - Allies",
           Path(f"{_G}/GURPS 4e - Dungeon Fantasy 05 - Allies.md"),
           "GURPS Dungeon Fantasy 5: Allies (SJGames, 4e), animal companions", "gurps"),
    Source("dfsummon", "GURPS Dungeon Fantasy 9 - Summoners",
           Path(f"{_G}/GURPS 4e - Dungeon Fantasy 09 - Summoners.md"),
           "GURPS Dungeon Fantasy 9: Summoners (SJGames, 4e), summoned creatures", "gurps"),
    Source("biglizzie", "GURPS Big Lizzie",
           Path(f"{_G}/GURPS 4e - Big Lizzie.md"),
           "GURPS Big Lizzie (SJGames, 4e), bestiary", "gurps"),
    # Kept LAST so the specific-book sources above win the cross-source dedup and
    # this comprehensive compilation contributes only creatures not already indexed.
    Source("natenc", "GURPS 4e Natural Encyclopedia (compilation)",
           Path(f"{_G}/GURPS 4e Non official and fan made/"
                "GURPS 4e -Natural Encyclopedia v1.5.2 (Bestiary).md"),
           "GURPS Natural Encyclopedia v1.5.2 (fan compilation, 4e stats; each "
           "creature credits its original GURPS source)", "gurps_encyclopedia"),
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
            src.creatures = DETECTORS[src.detector](src.lines, pages, src.book)
            src.coverage = f"ok — {len(src.creatures)} creatures from {path.name}"

        # Cross-source dedup: a compilation (the Natural Encyclopedia) repeats
        # creatures already indexed from the specific books above. Keep the
        # specific book's version; let the compilation contribute only net-new
        # names. Specific-book sources are listed first, so they seed `seen`.
        seen: set = set()
        for src in self.sources:
            if src.detector == "gurps_encyclopedia":
                before = len(src.creatures)
                src.creatures = [c for c in src.creatures if c.name.lower() not in seen]
                dropped = before - len(src.creatures)
                seen.update(c.name.lower() for c in src.creatures)
                if src.coverage.startswith("ok"):
                    src.coverage = (f"ok — {len(src.creatures)} net-new creatures "
                                    f"({dropped} already-indexed names deduped)")
            else:
                seen.update(c.name.lower() for c in src.creatures)

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
        "# GURPS CREATURE INDEX — The New Path",
        "",
        "**Generated by `scripts/gurps_creature_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** One row per GURPS creature — the GURPS attribute",
        "block (ST/DX/IQ/HT/HP/…), separate from the D&D `creature_index`. The",
        "raw text stays on `I:\\Sourcebooks` — use `--export \"NAME\"` for the",
        "translator-ready packet. A field left as `—` is one the OCR did not",
        "cleanly yield.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.creatures)
        parsed_well += sum(1 for c in src.creatures if c.quick_fields() >= 3)
        sources_out.append({"key": src.key, "book": src.book, "citation": src.citation,
                            "coverage": src.coverage,
                            "creatures": [asdict(c) for c in src.creatures]})
        md.append(f"## {src.book} — {len(src.creatures)} creatures")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.creatures:
            md.append("| Creature | ST | DX | IQ | HT | HP | Will | Per | Speed | Move | SM | DR | Origin | Page |")
            md.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
            for c in src.creatures:
                cells = [c.ST, c.DX, c.IQ, c.HT, c.HP, c.Will, c.Per, c.Speed,
                         c.Move, c.SM, c.DR]
                md.append("| " + c.name + " | " + " | ".join((x or "—") for x in cells)
                          + f" | {c.origin or '—'} | {c.page if c.page is not None else '—'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/gurps_creature_harvest.py",
                    "corpus": str(corpus.base), "total_creatures": total,
                    "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
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
            "packet": "gurps-creature-for-translation",
            "instructions": (
                "A native GURPS 4e creature. Its GURPS half is here; the "
                "system-translator skill builds the paired D&D 3.5e statline. "
                "The raw_block is OCR text; check oddities against the source PDF."
            ),
            "name": c.name,
            "source": {"book": c.book, "pdf_page": c.page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [c.start + 1, c.end], "citation": src.citation,
                       "credits_original": c.origin},
            "parsed": {k: v for k, v in asdict(c).items()
                       if k in ("ST", "DX", "IQ", "HT", "HP", "Will", "Per",
                                "Speed", "Move", "SM", "DR", "Dodge", "Parry",
                                "ctype") and v},
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


FIXTURE = """## [PDF page 6]
THE MONSTERS
BUGBEAR
Bugbears aren't brave, or even a terribly dangerous
foe one at a time. They garrote lone delvers.

ST: 14
HP: 14
Speed: 6.50
DX: 14
Will: 10
Move: 6
IQ: 10
Per: 12
HT: 12
DR: 2

Traits: Appearance (Monstrous).

DEMON FROM
BETWEEN THE STARS
A thing of writhing tentacles and wrongness.

ST: 20
HP: 22
Speed: 6.00
DX: 13
Will: 15
Move: 6
IQ: 12
Per: 14
HT: 12
DR: 4
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    lines = FIXTURE.splitlines()
    creatures = detect_gurps_creatures(lines, _pages_for(lines), "GURPS Dungeon Fantasy Monsters 1")
    names = [c.name for c in creatures]
    # BUGBEAR and the wrapped DEMON FROM / BETWEEN THE STARS are creatures;
    # THE MONSTERS running header is rejected.
    if names != ["Bugbear", "Demon From Between The Stars"]:
        failures.append(f"fixture detected {names}, wanted "
                        f"['Bugbear', 'Demon From Between The Stars'] "
                        f"(THE MONSTERS rejected; the wrapped demon name joined)")
    else:
        bug = creatures[0]
        got = (bug.ST, bug.DX, bug.IQ, bug.HT, bug.HP, bug.Will, bug.Per, bug.Move, bug.DR)
        want = ("14", "14", "10", "12", "14", "10", "12", "6", "2")
        if got != want:
            failures.append(f"Bugbear attrs {got}, wanted {want}")
        demon = creatures[1]
        if (demon.ST, demon.HP, demon.DR) != ("20", "22", "4"):
            failures.append(f"Demon attrs {(demon.ST, demon.HP, demon.DR)}, wanted 20/22/4")

    if base.is_dir() and (base / SOURCES[0].path).exists():
        corpus = Corpus(base, _fresh_sources())
        total = sum(len(s.creatures) for s in corpus.sources)
        if total < 40:
            failures.append(f"only {total} GURPS creatures indexed; expected > 40 "
                            f"(vertical DF Monsters + inline Creatures of the Night)")
        bug = corpus.find("bugbear", book="dfm1")
        if not bug:
            failures.append("Bugbear not found in live DF Monsters 1")
        elif not (bug[0][1].ST or "").isdigit():
            failures.append(f"live Bugbear ST={bug[0][1].ST!r}, expected a number")
        cotn = next((s for s in corpus.sources if s.key == "cotn5"), None)
        if cotn and (base / cotn.path).exists() and not cotn.creatures:
            failures.append("inline detector yielded 0 from Creatures of the Night 5")
        # Title-Case detector (GURPS Fantasy): the name echoes in its description.
        man = corpus.find("manticore", book="fantasy")
        if (base / next(s.path for s in SOURCES if s.key == "fantasy")).exists():
            if not man:
                failures.append("Manticore not found in live GURPS Fantasy "
                                "(Title-Case echo detector)")
            elif man[0][1].ST != "19":
                failures.append(f"live Manticore ST={man[0][1].ST!r}, wanted 19")
    else:
        print(f"  [SKIP] GURPS bestiary extractions not found — fixture checks only")

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
                        for _, c in corpus.all_creatures(args.book) if q in c.name.lower()})
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
        print(f"  {src.book:38s} {status}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} GURPS creatures across {sum(1 for s in corpus.sources if s.creatures)} book(s); "
          f"{parsed_well} with 3+ attributes parsed.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
