#!/usr/bin/env python3
"""dnd5e_item_harvest.py — collate D&D 5e magic items (labelled system: D&D 5e).

THE PROCESS (Chad, 2026-08-28): other editions are welcome AS LONG AS they are
clearly labelled by edition/system — the translator tools convert them into the
hybrid's 3.5e + GURPS. This is the D&D 5e MAGIC ITEM index, kept entirely
separate from the 3.5e `magic_item_index` and stamped `"system": "D&D 5e"`.

    reference/dnd5e_item_index.json  — every 5e item: name, item type, rarity,
                                       attunement, book, PDF page, system D&D 5e
    reference/dnd5e_item_index.md    — the same, for human eyes

`--export` emits a translator-ready packet (a 5e item the system-translator
skill converts to the 3.5e + GURPS pair).

WORKFLOW
    python dnd5e_item_harvest.py                    # (re)build the index
    python dnd5e_item_harvest.py --search "sword"   # find candidates
    python dnd5e_item_harvest.py --export "Bag of Beans"
    python dnd5e_item_harvest.py --selftest

GOVERNING SOURCES
    I:\\Sourcebooks\\_text\\D&D 5e\\ — the 5e item books (Mordenkainen's Tome
    of Marvelous Magic, Baldur's Gate: Items and Encounters, Treasures of
    Avernus, Drizzt's Travelogue, etc.). A 5e item is a NAME line then a type
    line: "Wondrous item, rare (requires attunement)" / "Weapon (any sword),
    uncommon" / "Ring, legendary". Detection anchors on that type-rarity line
    and takes the name from the line above. A configured source whose file is
    missing prints NO COVERAGE.
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
OUT_JSON = REPO / "reference" / "dnd5e_item_index.json"
OUT_MD = REPO / "reference" / "dnd5e_item_index.md"
SYSTEM = "D&D 5e"

PAGE = re.compile(r"\[PDF page (\d+)\]")
TYPES = ("Wondrous item|Weapon|Armor|Ring|Rod|Staff|Wand|Potion|Scroll|"
         "Ammunition")
RARITY = "common|uncommon|rare|very rare|legendary|artifact|varies|unique"
TYPE_LINE = re.compile(
    rf"^({TYPES})(\s*\([^)]*\))?,\s*({RARITY})\b(.*)$", re.IGNORECASE)
ATTUNE = re.compile(r"requires attunement", re.IGNORECASE)

# Reject structural/section lines only — NOT item names that begin with a type
# word ("Ring of Three Wishes", "Staff of Power"); the actual type-rarity line is
# already caught by TYPE_LINE in _plausible_name.
BAD_NAME = re.compile(
    r"^(Table|Chapter|Contents|Appendix|Rarity|Magic Items?|Attunement|"
    r"Description|Introduction|Sidebar)\b", re.IGNORECASE)


def _plausible_name(s: str) -> bool:
    s = s.strip()
    if not (3 <= len(s) <= 46):
        return False
    if s.endswith((".", ",", ":", ";")) or BAD_NAME.match(s) or TYPE_LINE.match(s):
        return False
    if not s[0].isalnum():
        return False
    letters = sum(c.isalpha() for c in s)
    return letters >= max(3, len(s) // 2)


@dataclass
class Item5e:
    name: str
    book: str
    page: Optional[int]
    start: int
    end: int
    system: str = SYSTEM
    item_type: Optional[str] = None
    subtype: Optional[str] = None       # "(any sword)" etc.
    rarity: Optional[str] = None
    attunement: Optional[bool] = None

    def quick_fields(self) -> int:
        return sum(1 for v in (self.item_type, self.rarity) if v)


def _name_above(lines: List[str], i: int) -> Optional[int]:
    j, seen = i - 1, 0
    while j >= 0 and seen < 3:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            j -= 1
            continue
        seen += 1
        if _plausible_name(s):
            return j
        return None
    return None


def detect_5e_items(lines: List[str], pages: List[int], book: str) -> List[Item5e]:
    n = len(lines)
    starts: List[Tuple[int, str, re.Match, str]] = []
    used = set()
    for i, ln in enumerate(lines):
        m = TYPE_LINE.match(ln.strip())
        if not m:
            continue
        a = _name_above(lines, i)
        if a is None or a in used:
            continue
        used.add(a)
        starts.append((a, lines[a].strip(), m, ln.strip()))

    starts.sort()
    out: List[Item5e] = []
    for k, (a, name, m, typ) in enumerate(starts):
        e = starts[k + 1][0] if k + 1 < len(starts) else min(n, a + 40)
        e = min(e, a + 40)
        # attunement text can wrap past the type line onto the next line or two
        attune_scan = " ".join([typ] + [lines[j].strip()
                                for j in range(a + 2, min(n, a + 5))])
        it = Item5e(name=name, book=book, page=pages[a], start=a, end=e,
                    item_type=m.group(1).strip().title(),
                    subtype=(m.group(2).strip() if m.group(2) else None),
                    rarity=m.group(3).lower(),
                    attunement=bool(ATTUNE.search(attune_scan)))
        out.append(it)

    # one entry per name (items reprinted across books) — keep the first
    best: Dict[str, Item5e] = {}
    for it in out:
        best.setdefault(it.name.lower(), it)
    return sorted(best.values(), key=lambda x: x.start)


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[Item5e]]] = {
    "5e": detect_5e_items,
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
    items: List[Item5e] = field(default_factory=list)


_5E = "D&D 5e"
_TP = f"{_5E}/Third Party and DMs Guild"
_OF = f"{_5E}/Official"
SOURCES: List[Source] = [
    Source("mordmarvel", "Mordenkainen's Tome of Marvelous Magic (5e, 3pp)",
           Path(f"{_TP}/Mordenkainens Tome of Marvelous Magic.md"),
           "Mordenkainen's Tome of Marvelous Magic (5e, DMs Guild)", "5e"),
    Source("diabolical", "Diabolical Designs (5e, 3pp)",
           Path(f"{_TP}/Diabolical Designs.md"), "Diabolical Designs (5e)", "5e"),
    Source("bgitems", "Baldur's Gate: Items and Encounters (5e, 3pp)",
           Path(f"{_TP}/Baldurs Gate Items and Encounters.md"),
           "Baldur's Gate: Items and Encounters (5e, DMs Guild)", "5e"),
    Source("drizzt", "Drizzt's Travelogue of Everything (5e, 3pp)",
           Path(f"{_TP}/Drizzts Travelogue of Everything Vol 1.md"),
           "Drizzt's Travelogue of Everything Vol.1 (5e, DMs Guild)", "5e"),
    Source("treasures", "Treasures of Avernus (5e, 3pp)",
           Path(f"{_TP}/Treasures of Avernus (3pp).md"),
           "Treasures of Avernus (5e, DMs Guild)", "5e"),
    Source("darkhold", "Darkhold: Secrets of the Zhentarim (5e, 3pp)",
           Path(f"{_TP}/Darkhold - Secrets of the Zhentarim.md"),
           "Darkhold: Secrets of the Zhentarim (5e, DMs Guild)", "5e"),
    Source("chains", "Chains of Asmodeus (5e, 3pp)",
           Path(f"{_TP}/Chains of Asmodeus.md"), "Chains of Asmodeus (5e)", "5e"),
    Source("tashas", "Tasha's Cauldron of Everything (5e)",
           Path(f"{_OF}/Tashas Cauldron of Everything.md"),
           "Tasha's Cauldron of Everything (5e, WotC)", "5e"),
    Source("manythings", "The Book of Many Things (5e)",
           Path(f"{_OF}/The Book of Many Things.md"),
           "The Deck of Many Things: The Book of Many Things (5e, WotC)", "5e"),
    Source("descent", "Baldur's Gate: Descent into Avernus (5e)",
           Path(f"{_OF}/Baldurs Gate - Descent into Avernus.md"),
           "Baldur's Gate: Descent into Avernus (5e, WotC)", "5e"),
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
            src.items = DETECTORS[src.detector](src.lines, pages, src.book)
            src.coverage = f"ok — {len(src.items)} items from {path.name}"

    def all_items(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for it in src.items:
                yield src, it

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, it in self.all_items(book):
            nm = it.name.lower()
            if nm == q:
                exact.append((src, it))
            elif q in nm:
                partial.append((src, it))
        return exact if exact else partial


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# D&D 5e MAGIC ITEM INDEX — The New Path",
        "",
        "**Generated by `scripts/dnd5e_item_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** These are **D&D 5th Edition** magic items — a",
        "DIFFERENT edition from the 3.5e `magic_item_index`. Every row is stamped",
        "`system: D&D 5e`; a 5e item is SOURCE MATERIAL for the system-translator",
        "skill, not campaign RAW. Use `--export \"NAME\"` for the packet.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.items)
        parsed_well += sum(1 for it in src.items if it.quick_fields() >= 2)
        sources_out.append({"key": src.key, "book": src.book, "system": SYSTEM,
                            "citation": src.citation, "coverage": src.coverage,
                            "items": [asdict(it) for it in src.items]})
        md.append(f"## {src.book} — {len(src.items)} items  *(system: {SYSTEM})*")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.items:
            md.append("| Item | Type | Rarity | Attunement | Page |")
            md.append("|---|---|---|---|---|")
            for it in src.items:
                typ = it.item_type + (" " + it.subtype if it.subtype else "")
                md.append(f"| {it.name} | {typ} | {it.rarity or '—'} | "
                          f"{'yes' if it.attunement else '—'} | "
                          f"{it.page if it.page is not None else '—'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/dnd5e_item_harvest.py",
                    "system": SYSTEM, "corpus": str(corpus.base),
                    "total_items": total, "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 6:
        print(f"'{name}' matches {len(hits)} items; narrow with --book or the exact name:")
        for src, it in hits[:20]:
            print(f"  {it.name}   [{it.book}, p.{it.page}]")
        return 1
    packets = []
    for src, it in hits:
        body = [ln for ln in src.lines[it.start:it.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "dnd5e-item-for-translation",
            "instructions": ("A D&D 5e magic item (system: D&D 5e). Feed to the "
                             "system-translator skill for the paired 3.5e AND GURPS "
                             "treatment. The raw_block is OCR text."),
            "name": it.name, "system": SYSTEM,
            "source": {"book": it.book, "pdf_page": it.page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [it.start + 1, it.end], "citation": src.citation},
            "parsed": {k: v for k, v in asdict(it).items()
                       if k in ("item_type", "subtype", "rarity", "attunement") and v},
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


FIXTURE = """## [PDF page 14]
Armband of Healing
Wondrous item, rare
This copper armband bears the insignia of two stags.

Flametongue Greatsword
Weapon (any sword), rare (requires attunement)
You can use a bonus action to speak this magic sword's command word.

Ring of Three Wishes
Ring, legendary
While wearing this ring, you can use an action to expend 1 of its 3 charges.
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    lines = FIXTURE.splitlines()
    items = detect_5e_items(lines, _pages_for(lines), "Mordenkainen's Tome of Marvelous Magic (5e, 3pp)")
    names = [it.name for it in items]
    if names != ["Armband of Healing", "Flametongue Greatsword", "Ring of Three Wishes"]:
        failures.append(f"fixture detected {names}, wanted the three 5e items")
    else:
        ft = items[1]
        if (ft.item_type, ft.rarity, ft.attunement) != ("Weapon", "rare", True):
            failures.append(f"Flametongue {(ft.item_type, ft.rarity, ft.attunement)}, "
                            f"wanted Weapon / rare / True")
        if items[0].system != "D&D 5e":
            failures.append("system must be 'D&D 5e'")

    if base.is_dir() and any((base / s.path).exists() for s in SOURCES):
        corpus = Corpus(base, _fresh_sources())
        total = sum(len(s.items) for s in corpus.sources)
        if total < 200:
            failures.append(f"only {total} 5e items indexed; expected > 200")
    else:
        print("  [SKIP] 5e extractions not found — fixture checks only")

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
        found = sorted({(it.name, it.book, it.page or -1, it.rarity or "—")
                        for _, it in corpus.all_items(args.book) if q in it.name.lower()})
        for name, bk, page, rarity in found:
            loc = bk if page < 0 else f"{bk}, p.{page}"
            print(f"  {name}   [{rarity}; {loc}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.items for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.items):4d} items" if src.items else "   0 items"
        print(f"  {src.book:52s} {status}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} D&D 5e items across {sum(1 for s in corpus.sources if s.items)} book(s). "
          f"(system: {SYSTEM})")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
