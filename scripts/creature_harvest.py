#!/usr/bin/env python3
"""creature_harvest.py — collate creature stat blocks for translation.

THE PROCESS (Chad, 2026-08-07, companion to term_harvest.py): "make another
to harvest creatures and their stat sheets / rules? then we can use the
system translator skill to convert to 3.5 / gurps when collated."

This script walks the bestiary text extractions and produces the COLLATION:

    reference/creature_index.json  — every stat block found: name, book, PDF
                                     page, line span, and the quick fields a
                                     triage read needs (size, type, HD, hp,
                                     AC, CR) parsed where the OCR is clean
    reference/creature_index.md    — the same index for human eyes, by book

The raw text is deliberately NOT copied into the repository — twelve books
of OCR would bloat it for nothing. Instead, `--export` emits a
TRANSLATOR-READY PACKET on demand: the verbatim block plus provenance and
parsed fields, as JSON on stdout or to a file. That packet is the input the
`system-translator` skill expects when converting a creature into the
hybrid's paired 3.5e + GURPS statlines (both halves always required, per
that skill's own rule).

WORKFLOW
    python creature_harvest.py                  # (re)build the index
    python creature_harvest.py --search dragon  # find candidates
    python creature_harvest.py --export "Wight" --book MM1
        -> JSON packet -> feed to the system-translator skill
    python creature_harvest.py --selftest

GOVERNING SOURCES
    I:\\Sourcebooks\\_md\\_bestiary\\*.md — the curated bestiary extractions
    (MM1-MM5, Draconomicon, Epic Level Handbook, Fiendish Codex I & II,
    Fiend Folio, Libris Mortis, Lords of Madness), the same set
    monster_lookup.py reads. The PDFs on I:\\Sourcebooks stand behind every
    extraction when the text layer is ambiguous.

    Block DETECTION is duplicated from monster_lookup.py on purpose — the
    repo law is "no cross-imports; shared logic gets duplicated or promoted
    deliberately". If detection improves, improve it in both places.

    Non-3.5 shelves (Warhammer 40k RPG bestiaries, WFRP, GURPS creature
    books, AD&D) live under I:\\Sourcebooks\\_text and are the intended
    next SOURCES entries; their statblock grammars differ, so each gets its
    own detector when it is added. NO COVERAGE is printed for a configured
    source that cannot be read — never improvised.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

DEFAULT_BESTIARY = Path(r"I:\Sourcebooks\_md\_bestiary")
REPO = Path(__file__).resolve().parent.parent
OUT_JSON = REPO / "reference" / "creature_index.json"
OUT_MD = REPO / "reference" / "creature_index.md"

# ---------------------------------------------------------------------------
# Detection — duplicated from monster_lookup.py per the no-cross-imports law
# ---------------------------------------------------------------------------

PAGE = re.compile(r"<!-- page (\d+) -->")
BAD_STARTS = ("Hit Dice", "Initiative", "Speed", "Armor Class", "Base Attack",
              "Attack", "Full Attack", "Space/Reach", "Special", "Saves",
              "Abilities", "Skills", "Feats", "Environment", "Organization",
              "Challenge Rating", "Treasure", "Alignment", "Advancement",
              "Level Adjustment", "<!--", "COMBAT", "TACTICS", "LORE",
              "Init ", "Senses", "Languages", "AC ", "hp ", "Fort ",
              "Speed ", "Melee", "Ranged", "Space ", "Base Atk")

SIZES = "Fine|Diminutive|Tiny|Small|Medium|Large|Huge|Gargantuan|Colossal"
TYPES = ("Aberration|Animal|Construct|Dragon|Elemental|Fey|Giant|Humanoid|"
         "Magical Beast|Monstrous Humanoid|Ooze|Outsider|Plant|Undead|Vermin")
CLASSIC = re.compile(rf"^\s*({SIZES})\s+({TYPES})", re.IGNORECASE)
HITDICE = re.compile(r"^\s*Hit Dice:", re.IGNORECASE)
HDDICE = re.compile(r"\d+d(4|6|8|10|12|20)\b")
LATE = re.compile(r"^\s*Init\s+[+\u2013\u2014-]\d")
SKIP_UP = re.compile(rf"^\s*(Always|Usually|Often|CR\s|({SIZES})\b|hp\s\d)",
                     re.IGNORECASE)


def plausible_name(line: str) -> bool:
    s = line.strip()
    if not s or len(s) > 60 or len(s) < 3:
        return False
    if any(s.startswith(b) for b in BAD_STARTS):
        return False
    if ":" in s or s.endswith((".", ",")) or ". ." in s:
        return False
    letters = sum(ch.isalpha() for ch in s)
    return letters >= max(3, len(s) // 2)


def _name_above(lines: List[str], i: int, limit: int = 6) -> Optional[int]:
    j = i - 1
    seen = 0
    while j >= 0 and seen < limit:
        s = lines[j].strip()
        if s:
            seen += 1
            if not SKIP_UP.match(s) and plausible_name(s):
                return j
        j -= 1
    return None


# ---------------------------------------------------------------------------
# The quick fields a triage read needs — parsed only where the OCR is clean
# ---------------------------------------------------------------------------

F_HITDICE = re.compile(r"Hit Dice:\s*([0-9]+d[0-9]+(?:[+\-\u2013][0-9]+)?)\s*\(?\s*([0-9,]+)?\s*hp?\)?",
                       re.IGNORECASE)
F_AC = re.compile(r"Armor Class:\s*([0-9]{1,2})", re.IGNORECASE)
F_CR = re.compile(r"Challenge Rating:\s*([0-9]+(?:/[0-9]+)?)", re.IGNORECASE)
F_SIZETYPE = re.compile(rf"^\s*({SIZES})\s+({TYPES})", re.IGNORECASE | re.MULTILINE)


@dataclass
class Creature:
    name: str
    book: str
    page: int
    start: int  # line span in the extraction, for --export
    end: int
    size: str | None = None
    type: str | None = None
    hit_dice: str | None = None
    hp: str | None = None
    ac: str | None = None
    cr: str | None = None

    def quick_fields(self) -> int:
        return sum(1 for v in (self.size, self.hit_dice, self.hp, self.ac, self.cr) if v)


def parse_quick_fields(creature: Creature, body: str) -> None:
    m = F_SIZETYPE.search(body)
    if m:
        creature.size, creature.type = m.group(1).title(), m.group(2).title()
    m = F_HITDICE.search(body)
    if m:
        creature.hit_dice = m.group(1)
        if m.group(2):
            creature.hp = m.group(2).replace(",", "")
    m = F_AC.search(body)
    if m:
        creature.ac = m.group(1)
    m = F_CR.search(body)
    if m:
        creature.cr = m.group(1)


def index_book(path: Path) -> Tuple[List[str], List[Creature]]:
    book = path.stem
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    pages: List[int] = []
    page = 0
    for ln in lines:
        m = PAGE.search(ln)
        if m:
            page = int(m.group(1))
        pages.append(page)

    starts: List[Tuple[int, str]] = []
    used = set()
    n = len(lines)
    for i, ln in enumerate(lines):
        hit = False
        if HITDICE.match(ln) or LATE.match(ln):
            hit = True
        elif CLASSIC.match(ln):
            tail = [ln]
            j, seen = i + 1, 0
            while j < n and seen < 2:
                s = lines[j].strip()
                if s:
                    seen += 1
                    tail.append(s)
                j += 1
            if HDDICE.search(" ".join(tail)):
                hit = True
        if not hit:
            continue
        at = _name_above(lines, i)
        if at is None or at in used:
            continue
        used.add(at)
        starts.append((at, lines[at].strip().title()))

    starts.sort()
    creatures: List[Creature] = []
    for k, (s, name) in enumerate(starts):
        e = starts[k + 1][0] if k + 1 < len(starts) else min(len(lines), s + 200)
        e = min(e, s + 200)
        creature = Creature(name=name, book=book, page=pages[s], start=s, end=e)
        parse_quick_fields(creature, "\n".join(lines[s:e]))
        creatures.append(creature)
    return lines, creatures


class Corpus:
    def __init__(self, directory: Path):
        self.directory = directory
        self.books: Dict[str, Tuple[List[str], List[Creature]]] = {}
        if directory.is_dir():
            for path in sorted(directory.glob("*.md")):
                self.books[path.stem] = index_book(path)

    def all_creatures(self, book: Optional[str] = None):
        for name, (lines, creatures) in self.books.items():
            if book and book.lower() != name.lower():
                continue
            for c in creatures:
                yield lines, c

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for lines, c in self.all_creatures(book):
            n = c.name.lower()
            if n == q:
                exact.append((lines, c))
            elif q in n:
                partial.append((lines, c))
        return exact if exact else partial


# ---------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    books_out = []
    md: List[str] = [
        "# CREATURE INDEX — The New Path",
        "",
        "**Generated by `scripts/creature_harvest.py`. Do not hand-edit; rerun",
        "the harvest.** One row per stat block found in the bestiary",
        "extractions. The raw text stays on `I:\\Sourcebooks` — use",
        "`python scripts/creature_harvest.py --export \"NAME\" --book BOOK` to",
        "emit the translator-ready packet for any row, then hand that packet",
        "to the system-translator skill for the paired 3.5e + GURPS build.",
        "",
    ]
    for book, (lines, creatures) in corpus.books.items():
        total += len(creatures)
        parsed_well += sum(1 for c in creatures if c.quick_fields() >= 3)
        books_out.append(
            {"book": book, "creatures": [asdict(c) for c in creatures]}
        )
        md.append(f"## {book} — {len(creatures)} stat blocks")
        md.append("")
        md.append("| Creature | Size | Type | HD | hp | AC | CR | Page |")
        md.append("|---|---|---|---|---|---|---|---|")
        for c in creatures:
            md.append(
                f"| {c.name} | {c.size or '—'} | {c.type or '—'} | {c.hit_dice or '—'} | "
                f"{c.hp or '—'} | {c.ac or '—'} | {c.cr or '—'} | {c.page or '—'} |"
            )
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps(
            {
                "generated_by": "scripts/creature_harvest.py",
                "source_directory": str(corpus.directory),
                "total_stat_blocks": total,
                "books": books_out,
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
    if len(hits) > 4:
        print(f"'{name}' matches {len(hits)} blocks; narrow with --book or the exact name:")
        for _, c in hits[:15]:
            print(f"  {c.name}   [{c.book}, p.{c.page}]")
        return 1
    packets = []
    for lines, c in hits:
        body = [ln for ln in lines[c.start:c.end] if not PAGE.search(ln)]
        packets.append(
            {
                "packet": "creature-for-translation",
                "instructions": (
                    "Feed this packet to the system-translator skill. Both a 3.5e "
                    "AND a GURPS statline are required in the output — a conversion "
                    "missing either system is incomplete (that skill's own rule). "
                    "The raw_block is OCR text; check oddities against the source "
                    "PDF on I:\\Sourcebooks before trusting a strange number."
                ),
                "name": c.name,
                "source": {"book": c.book, "pdf_page": c.page,
                           "extraction": str(corpus.directory / (c.book + ".md")),
                           "lines": [c.start + 1, c.end]},
                "parsed": {k: v for k, v in asdict(c).items()
                           if k in ("size", "type", "hit_dice", "hp", "ac", "cr") and v},
                "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
            }
        )
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

FIXTURE = """Skeletal Warden
Medium Undead
Hit Dice: 4d12 (26 hp)
Initiative: +6
Speed: 30 ft. (6 squares)
Armor Class: 15 (+2 Dex, +3 natural), touch 12, flat-footed 13
Challenge Rating: 3

Grave Hound
Large Undead
Hit Dice: 6d12+3 (42 hp)
Armor Class: 17
Challenge Rating: 5
"""


def selftest(directory: Path) -> int:
    failures: List[str] = []

    fixture_path = None
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        fixture_path = Path(tmp) / "FIX1.md"
        fixture_path.write_text(FIXTURE, encoding="utf-8")
        corpus = Corpus(Path(tmp))
        creatures = [c for _, c in corpus.all_creatures()]
        names = [c.name for c in creatures]
        if names != ["Skeletal Warden", "Grave Hound"]:
            failures.append(f"fixture harvested {names}, wanted the two undead")
        else:
            warden = creatures[0]
            got = (warden.size, warden.type, warden.hit_dice, warden.hp, warden.ac, warden.cr)
            want = ("Medium", "Undead", "4d12", "26", "15", "3")
            if got != want:
                failures.append(f"quick fields {got}, wanted {want}")

    if directory.is_dir():
        corpus = Corpus(directory)
        total = sum(len(v[1]) for v in corpus.books.values())
        if len(corpus.books) < 8:
            failures.append(f"only {len(corpus.books)} books indexed; expected >= 8")
        if total < 1000:
            failures.append(f"only {total} stat blocks indexed; expected > 1000")
        hits = corpus.find("wight", book="MM1")
        if not hits:
            failures.append("Wight (MM1) not found")
        else:
            c = hits[0][1]
            if c.hit_dice != "4d12":
                failures.append(f"Wight hit dice parsed as {c.hit_dice!r}, wanted 4d12")
    else:
        print(f"  [SKIP] bestiary dir not found: {directory} — fixture checks only")

    for failure in failures:
        print(f"SELFTEST FAIL: {failure}")
    print("selftest: " + ("PASS" if not failures else f"{len(failures)} failure(s)"))
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--bestiary", type=Path, default=DEFAULT_BESTIARY)
    ap.add_argument("--search", metavar="TEXT", help="substring search on indexed names")
    ap.add_argument("--book", help="restrict to one book (e.g. MM1, FC2)")
    ap.add_argument("--export", metavar="NAME", help="emit a translator-ready packet")
    ap.add_argument("--out", type=Path, help="write the packet here instead of stdout")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest(args.bestiary)

    if not args.bestiary.is_dir():
        print(f"NO COVERAGE — bestiary directory missing: {args.bestiary}", file=sys.stderr)
        return 2
    corpus = Corpus(args.bestiary)

    if args.search:
        q = args.search.lower()
        found = sorted({(c.name, c.book, c.page, c.cr or "—")
                        for _, c in corpus.all_creatures(args.book) if q in c.name.lower()})
        for name, book, page, cr in found:
            print(f"  {name}   [CR {cr}, {book}, p.{page}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    total, parsed_well = write_index(corpus)
    for book, (_, creatures) in corpus.books.items():
        print(f"  {book:24s} {len(creatures):5d} stat blocks")
    print(f"\n{total} stat blocks across {len(corpus.books)} books; "
          f"{parsed_well} with 3+ quick fields parsed.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
