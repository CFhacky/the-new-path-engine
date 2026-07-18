#!/usr/bin/env python3
"""
feat_lookup.py -- D&D 3.5e feat reference
The New Path campaign engine (the-new-path-engine)

GOVERNING SOURCES:
    1. feats_srd35.json -- bundled, parsed from SRD 3.5 (all PH core
       feats). Ships beside this script. SRD wins on name collision.
    2. Live supplement extractions at I:\\Sourcebooks\\_md\\_feats\\*.md
       (override with --feats-dir).

DESIGN CONTRACT (repo README): stateless, no dice, cites book + page,
--selftest skips dir-dependent checks when the extractions are absent.

HOW SUPPLEMENT BLOCKS ARE FOUND
    Every feat body anchors on a "Benefit:" line (ligatures normalized).
    The feat's name is the nearest Title-Case short line above it,
    skipping prerequisite lines, [Type] tag lines, and flavor prose.
    Boundaries are approximate -- the feat you need is in what prints.

USAGE
    python feat_lookup.py "blind-fight" "power attack"
    python feat_lookup.py --search luck
    python feat_lookup.py --search smite --book Complete_Champion
    python feat_lookup.py --list-books
    python feat_lookup.py --selftest
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional, Tuple

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_DIR = r"I:\Sourcebooks\_md\_feats"
SRD_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "feats_srd35.json")

ANCHOR = re.compile(r"^\s*Bene\s?fi\s?ts?\s*:")
PAGE = re.compile(r"<!-- page (\d+) -->")
TAG = re.compile(r"^\s*\[([A-Za-z ,]+)\]\s*$")
SKIP_UP = re.compile(r"^\s*(Prerequisites?\s*:|Bene\s?fi\s?ts?\s*:|"
                     r"Special\s*:|Normal\s*:|Table\s|CHAPTER|"
                     r"Feat\s+Descriptions)")


def plausible_feat_name(s: str) -> bool:
    s = s.strip()
    if not s or len(s) > 42 or len(s) < 4:
        return False
    if s.endswith((".", ",", ":", ";")) or SKIP_UP.match(s) or TAG.match(s):
        return False
    words = [w for w in re.split(r"[\s\u2013-]+", s) if w]
    if not words or not words[0][:1].isupper():
        return False
    caps = sum(1 for w in words if w[:1].isupper())
    return caps >= max(1, (len(words) * 3) // 5)


class Block:
    __slots__ = ("name", "tag", "book", "page", "start", "end")

    def __init__(self, name, tag, book, page, start, end):
        self.name, self.tag, self.book = name, tag, book
        self.page, self.start, self.end = page, start, end


def index_book(path: str) -> Tuple[List[str], List[Block]]:
    book = os.path.splitext(os.path.basename(path))[0]
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    for lig, plain in (("\ufb01", "fi"), ("\ufb02", "fl"),
                       ("\ufb00", "ff"), ("\ufb03", "ffi"),
                       ("\ufb04", "ffl")):
        raw = raw.replace(lig, plain)
    lines = raw.splitlines()
    pages, page = [], 0
    for ln in lines:
        m = PAGE.search(ln)
        if m:
            page = int(m.group(1))
        pages.append(page)

    starts: List[Tuple[int, str, str]] = []
    used = set()
    for i, ln in enumerate(lines):
        if not ANCHOR.match(ln):
            continue
        j, seen, name_at, tag = i - 1, 0, None, ""
        while j >= 0 and seen < 10:
            s = lines[j].strip()
            if s:
                seen += 1
                m = TAG.match(s)
                if m and not tag:
                    tag = m.group(1)
                elif plausible_feat_name(s):
                    name_at = j
                    break
            j -= 1
        if name_at is None or name_at in used:
            continue
        used.add(name_at)
        starts.append((name_at, lines[name_at].strip(), tag))

    starts.sort()
    blocks: List[Block] = []
    for k, (s, name, tag) in enumerate(starts):
        e = starts[k + 1][0] if k + 1 < len(starts) else min(len(lines), s + 120)
        e = min(e, s + 120)
        blocks.append(Block(name, tag, book, pages[s], s, e))
    return lines, blocks


class FeatDB:
    def __init__(self, directory: str, srd_path: str = SRD_JSON):
        self.srd: Dict[str, dict] = {}
        if os.path.exists(srd_path):
            with open(srd_path, encoding="utf-8") as f:
                self.srd = json.load(f)
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


BAR = "=" * 62


def print_srd(entry: dict) -> None:
    print(BAR)
    tag = f" [{entry['type']}]" if entry.get("type") else ""
    print(f"{entry['name'].upper()}{tag}    [{entry['source']}]")
    print(BAR)
    print(entry["text"])
    print(BAR)


def print_block(lines: List[str], b: Block) -> None:
    print(BAR)
    tag = f" [{b.tag}]" if b.tag else ""
    print(f"{b.name.upper()}{tag}    [{b.book}, p.{b.page}]")
    print(BAR)
    body = [ln for ln in lines[b.start:b.end] if not PAGE.search(ln)]
    print(re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip())
    print(BAR)


def selftest(directory: str) -> int:
    failures = 0

    def check(desc, ok):
        nonlocal failures
        print(f"  [{'PASS' if ok else 'FAIL'}] {desc}")
        if not ok:
            failures += 1

    print("### feat_lookup.py SELFTEST ###\n")
    db = FeatDB(directory)
    check(f"SRD feats loaded: {len(db.srd)} (expect >= 100)",
          len(db.srd) >= 100)
    bf = db.srd.get("blind-fight")
    check("Blind-Fight in SRD with reroll-concealment text",
          bool(bf) and "concealment" in bf["text"])
    pa = db.srd.get("power attack")
    check("Power Attack in SRD", bool(pa))

    if not db.books:
        print(f"  [SKIP] supplement dir not found/empty: {directory}")
    else:
        total = sum(len(v[1]) for v in db.books.values())
        check(f"Supplement books: {len(db.books)} (expect >= 8)",
              len(db.books) >= 8)
        check(f"Supplement feat blocks: {total} (expect > 500)", total > 500)
        hit = any(b.name.lower() == "advantageous avoidance"
                  for _, b in db.all_blocks("Complete_Scoundrel"))
        check("Advantageous Avoidance found in Complete Scoundrel", hit)

    print(f"\n{'ALL checks passed.' if failures == 0 else str(failures) + ' CHECKS FAILED.'}")
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="D&D 3.5e feat reference")
    ap.add_argument("names", nargs="*")
    ap.add_argument("--search", metavar="TEXT")
    ap.add_argument("--book")
    ap.add_argument("--feats-dir", default=DEFAULT_DIR)
    ap.add_argument("--list-books", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest(args.feats_dir)

    db = FeatDB(args.feats_dir)

    if args.list_books:
        print(f"  SRD (bundled): {len(db.srd)} feats")
        for name, (lines, blocks) in db.books.items():
            print(f"  {name}: {len(blocks)} feat blocks")
        return 0

    if args.search:
        q = args.search.lower()
        found = [(e["name"], e["source"], "") for k, e in db.srd.items()
                 if q in k] if not args.book else []
        found += sorted({(b.name, b.book, f"p.{b.page}")
                         for _, b in db.all_blocks(args.book)
                         if q in b.name.lower()})
        if not found:
            print(f"No feats match '{args.search}'.")
            return 1
        for name, book, page in found:
            print(f"  {name}   [{book}{' ' + page if page else ''}]")
        print(f"{len(found)} match(es).")
        return 0

    if not args.names:
        ap.print_help()
        return 2

    rc = 0
    for name in args.names:
        q = name.strip().lower()
        if not args.book and q in db.srd:
            print_srd(db.srd[q])
            continue
        hits = [(lines, b) for lines, b in db.all_blocks(args.book)
                if b.name.lower() == q]
        if not hits:
            hits = [(lines, b) for lines, b in db.all_blocks(args.book)
                    if q in b.name.lower()]
        if not hits:
            print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
            rc = 1
            continue
        if len(hits) > 4:
            print(f"'{name}' matches {len(hits)}; narrow with --book:")
            for _, b in hits[:15]:
                print(f"  {b.name}   [{b.book}, p.{b.page}]")
            continue
        for lines, b in hits:
            print_block(lines, b)
    return rc


if __name__ == "__main__":
    sys.exit(main())
