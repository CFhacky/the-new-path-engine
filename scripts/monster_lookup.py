#!/usr/bin/env python3
"""
monster_lookup.py — D&D 3.5e monster stat block finder
The New Path campaign engine (the-new-path-engine)

GOVERNING SOURCES (local text extractions, read live):
    I:\\Sourcebooks\\_md\\_bestiary\\*.md   (override with --bestiary DIR)
    Extracted from text-layer PDFs: MM1 (Premium), MM2, MM4, MM5,
    Fiend Folio, Fiendish Codex I & II, Lords of Madness, Libris Mortis,
    Epic Level Handbook. (MM3 and Draconomicon are image-only scans and
    are absent until OCR'd.)

DESIGN CONTRACT (repo README):
    - Stateless resolver: flags in, text out. No state file, no dice.
    - Visible output: the stat block prints ready to use, with book + page.
    - No cross-imports.
    - --selftest skips (not fails) when the bestiary directory is absent,
      so it passes in any checkout; run it on the machine that has the
      extractions for the full pass.

HOW IT FINDS BLOCKS
    Every 3.5e stat block anchors on a "Hit Dice:" line. The monster's
    name is the nearest plausible name line within the six nonempty lines
    above the anchor. A block runs from its name line to the next block's
    name line (or a hard cap). Extraction noise means boundaries are
    approximate — the block you need is in what prints.

USAGE
    python3 monster_lookup.py vrock
    python3 monster_lookup.py "pit fiend" --book FC2
    python3 monster_lookup.py --search devil
    python3 monster_lookup.py --list-books
    python3 monster_lookup.py --selftest
"""

import argparse
import os
import re
import sys
from typing import Dict, List, Optional, Tuple

DEFAULT_BESTIARY = r"I:\Sourcebooks\_md\_bestiary"

PAGE = re.compile(r"<!-- page (\d+) -->")
BAD_STARTS = ("Hit Dice", "Initiative", "Speed", "Armor Class", "Base Attack",
              "Attack", "Full Attack", "Space/Reach", "Special", "Saves",
              "Abilities", "Skills", "Feats", "Environment", "Organization",
              "Challenge Rating", "Treasure", "Alignment", "Advancement",
              "Level Adjustment", "<!--", "COMBAT", "TACTICS", "LORE",
              "Init ", "Senses", "Languages", "AC ", "hp ", "Fort ",
              "Speed ", "Melee", "Ranged", "Space ", "Base Atk")


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


class Block:
    __slots__ = ("name", "book", "page", "start", "end")

    def __init__(self, name, book, page, start, end):
        self.name, self.book, self.page = name, book, page
        self.start, self.end = start, end


SIZES = "Fine|Diminutive|Tiny|Small|Medium|Large|Huge|Gargantuan|Colossal"
TYPES = ("Aberration|Animal|Construct|Dragon|Elemental|Fey|Giant|Humanoid|"
         "Magical Beast|Monstrous Humanoid|Ooze|Outsider|Plant|Undead|Vermin")
CLASSIC = re.compile(rf"^\s*({SIZES})\s+({TYPES})", re.IGNORECASE)
HITDICE = re.compile(r"^\s*Hit Dice:", re.IGNORECASE)
HDDICE = re.compile(r"\d+d(4|6|8|10|12|20)\b")
LATE = re.compile(r"^\s*Init\s+[+\u2013\u2014-]\d")
SKIP_UP = re.compile(rf"^\s*(Always|Usually|Often|CR\s|({SIZES})\b|hp\s\d)",
                     re.IGNORECASE)


def _name_above(lines, i, limit=6):
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


def index_book(path: str) -> Tuple[List[str], List[Block]]:
    book = os.path.splitext(os.path.basename(path))[0]
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()
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
    blocks: List[Block] = []
    for k, (s, name) in enumerate(starts):
        e = starts[k + 1][0] if k + 1 < len(starts) else min(len(lines), s + 200)
        e = min(e, s + 200)
        blocks.append(Block(name, book, pages[s], s, e))
    return lines, blocks


class Bestiary:
    def __init__(self, directory: str):
        self.books: Dict[str, Tuple[List[str], List[Block]]] = {}
        if os.path.isdir(directory):
            for fn in sorted(os.listdir(directory)):
                if fn.lower().endswith(".md"):
                    p = os.path.join(directory, fn)
                    self.books[os.path.splitext(fn)[0]] = index_book(p)

    def all_blocks(self, book: Optional[str] = None):
        for name, (lines, blocks) in self.books.items():
            if book and book.lower() != name.lower():
                continue
            for b in blocks:
                yield lines, b

    def find(self, query: str, book: Optional[str] = None) -> List[Tuple[List[str], Block]]:
        q = query.strip().lower()
        exact, partial = [], []
        for lines, b in self.all_blocks(book):
            n = b.name.lower()
            if n == q:
                exact.append((lines, b))
            elif q in n:
                partial.append((lines, b))
        return exact if exact else partial


BAR = "=" * 62


def print_block(lines: List[str], b: Block) -> None:
    print(BAR)
    print(f"{b.name.upper()}    [{b.book}, p.{b.page}]")
    print(BAR)
    body = [ln for ln in lines[b.start:b.end] if not PAGE.search(ln)]
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip()
    print(text)
    print(BAR)


def selftest(directory: str) -> int:
    failures = 0

    def check(desc: str, ok: bool) -> None:
        nonlocal failures
        print(f"  [{'PASS' if ok else 'FAIL'}] {desc}")
        if not ok:
            failures += 1

    print("### monster_lookup.py SELFTEST ###\n")
    if not os.path.isdir(directory):
        print(f"  [SKIP] bestiary dir not found: {directory}")
        print("\nALL checks passed (nothing testable here).")
        return 0

    bz = Bestiary(directory)
    check(f"Books indexed: {len(bz.books)} (expect >= 8)", len(bz.books) >= 8)
    total = sum(len(v[1]) for v in bz.books.values())
    check(f"Stat blocks indexed: {total} (expect > 1000)", total > 1000)

    hits = bz.find("wight", book="MM1")
    ok = False
    if hits:
        lines, b = hits[0]
        body = "\n".join(lines[b.start:b.end])
        ok = ("4d12" in body and "Energy Drain" in body
              and "Create Spawn" in body)
    check("Wight (MM1): 4d12 HD, Energy Drain, Create Spawn in block", ok)

    hits = bz.find("vrock")
    check("Vrock found", bool(hits))

    hits = bz.find("pit fiend")
    check("Pit Fiend found", bool(hits))

    print(f"\n{'ALL checks passed.' if failures == 0 else str(failures) + ' CHECKS FAILED.'}")
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="D&D 3.5e monster stat block finder")
    ap.add_argument("names", nargs="*", help="monster name(s)")
    ap.add_argument("--search", metavar="TEXT", help="substring search on names")
    ap.add_argument("--book", help="restrict to one book (e.g. MM1, FC2)")
    ap.add_argument("--bestiary", default=DEFAULT_BESTIARY)
    ap.add_argument("--list-books", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest(args.bestiary)

    bz = Bestiary(args.bestiary)
    if not bz.books:
        print(f"No bestiary files at {args.bestiary}", file=sys.stderr)
        return 2

    if args.list_books:
        for name, (lines, blocks) in bz.books.items():
            print(f"  {name}: {len(blocks)} stat blocks")
        return 0

    if args.search:
        q = args.search.lower()
        found = sorted({(b.name, b.book, b.page)
                        for _, b in bz.all_blocks(args.book)
                        if q in b.name.lower()})
        if not found:
            print(f"No monsters match '{args.search}'.")
            return 1
        for name, book, page in found:
            print(f"  {name}   [{book}, p.{page}]")
        print(f"{len(found)} match(es).")
        return 0

    if not args.names:
        ap.print_help()
        return 2

    rc = 0
    for name in args.names:
        hits = bz.find(name, args.book)
        if not hits:
            print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
            rc = 1
            continue
        if len(hits) > 4:
            print(f"'{name}' matches {len(hits)} blocks; narrow with --book "
                  f"or exact name:")
            for _, b in hits[:15]:
                print(f"  {b.name}   [{b.book}, p.{b.page}]")
            continue
        for lines, b in hits:
            print_block(lines, b)
    return rc


if __name__ == "__main__":
    sys.exit(main())
