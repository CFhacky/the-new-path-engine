#!/usr/bin/env python3
"""dnd5e_creature_harvest.py — collate D&D 5e monster stat blocks.

THE PROCESS (Chad, 2026-08-28): other editions are welcome in the reference
layer AS LONG AS THEY ARE CLEARLY LABELLED by edition/system — Chad's
translator tools convert them into the hybrid's 3.5e + GURPS from there. This
is the FIFTH-EDITION creature index, kept entirely separate from the 3.5e
`creature_index` and stamped `"system": "D&D 5e"` so nothing here is ever
mistaken for 3.5e RAW.

    reference/dnd5e_creature_index.json  — every 5e monster: name, size, type,
                                          alignment, AC, HP, speed, the six
                                          ability scores, Challenge (CR), book,
                                          PDF page; each stamped system D&D 5e
    reference/dnd5e_creature_index.md    — the same, for human eyes

The raw text stays on I:\\Sourcebooks; `--export` emits a TRANSLATOR-READY
packet — a 5e block the system-translator skill converts to the 3.5e + GURPS
pair (BOTH still required in the output, per that skill's rule).

WORKFLOW
    python dnd5e_creature_harvest.py                   # (re)build the index
    python dnd5e_creature_harvest.py --search "devil"  # find candidates
    python dnd5e_creature_harvest.py --export "Tormenting Shadow"
    python dnd5e_creature_harvest.py --selftest

GOVERNING SOURCES
    I:\\Sourcebooks\\_text\\D&D 5e\\ — the 5e bestiaries (Blood War Bestiary,
    Dante's Guide to Hell, Xanathar's Enemies and Allies, The Book of Hordes).
    A 5e stat block is a NAME line, then "Size type, alignment", then "Armor
    Class N", "Hit Points N (…)", "Speed …", the six ability scores, and
    "Challenge N (XP)". Detection anchors on the size-type-alignment line
    (confirmed by an Armor Class line just below) and takes the name from the
    line above. A configured source whose file is missing prints NO COVERAGE.
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
OUT_JSON = REPO / "reference" / "dnd5e_creature_index.json"
OUT_MD = REPO / "reference" / "dnd5e_creature_index.md"
SYSTEM = "D&D 5e"

PAGE = re.compile(r"\[PDF page (\d+)\]")
SIZES = "Tiny|Small|Medium|Large|Huge|Gargantuan"
TYPES = ("aberration|beast|celestial|construct|dragon|elemental|fey|fiend|"
         "giant|humanoid|monstrosity|ooze|plant|undead|swarm")
SIZE_TYPE = re.compile(rf"^({SIZES})\s+({TYPES})\b[^,]*,\s*(.+)$", re.IGNORECASE)
AC = re.compile(r"^Armor Class\s+(\d+)", re.IGNORECASE)
HP = re.compile(r"^Hit Points\s+(\d+)", re.IGNORECASE)
SPEED = re.compile(r"^Speed\s+(.+)$", re.IGNORECASE)
CR = re.compile(r"^Challenge\s+([\d/]+)", re.IGNORECASE)
ABILITY = re.compile(r"^(\d{1,2})\s*\([+\-\u2212]?\d+\)")
ABIL_LABEL = re.compile(r"^(STR|DEX|CON|INT|WIS|CHA)$", re.IGNORECASE)

BAD_NAME = re.compile(
    r"^(Armor Class|Hit Points|Speed|Challenge|Actions|Traits|Legendary|"
    r"Damage|Condition|Senses|Languages|Skills|Saving|STR|DEX|CON|INT|WIS|CHA|"
    r"Chapter|Contents|Appendix|The\b.{0,4}$)", re.IGNORECASE)


def _plausible_name(s: str) -> bool:
    s = s.strip()
    if not (3 <= len(s) <= 44) or s.isdigit():
        return False
    if s.endswith((".", ",", ":", ";")) or BAD_NAME.match(s):
        return False
    if SIZE_TYPE.match(s):
        return False
    letters = sum(c.isalpha() for c in s)
    return letters >= max(3, len(s) // 2)


@dataclass
class Monster5e:
    name: str
    book: str
    page: Optional[int]
    start: int
    end: int
    system: str = SYSTEM
    size: Optional[str] = None
    type: Optional[str] = None
    alignment: Optional[str] = None
    ac: Optional[str] = None
    hp: Optional[str] = None
    speed: Optional[str] = None
    cr: Optional[str] = None
    STR: Optional[str] = None
    DEX: Optional[str] = None
    CON: Optional[str] = None
    INT: Optional[str] = None
    WIS: Optional[str] = None
    CHA: Optional[str] = None

    def quick_fields(self) -> int:
        return sum(1 for v in (self.ac, self.hp, self.cr, self.STR) if v)


def _name_above(lines: List[str], i: int) -> Optional[int]:
    j, seen = i - 1, 0
    while j >= 0 and seen < 4:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            j -= 1
            continue
        seen += 1
        if _plausible_name(s):
            return j
        return None
    return None


def parse_block(m: Monster5e, body: List[str]) -> None:
    scores: List[str] = []
    for raw in body:
        s = raw.strip()
        if not s:
            continue
        if m.ac is None:
            g = AC.match(s)
            if g:
                m.ac = g.group(1)
                continue
        if m.hp is None:
            g = HP.match(s)
            if g:
                m.hp = g.group(1)
                continue
        if m.speed is None:
            g = SPEED.match(s)
            if g:
                m.speed = re.sub(r"\s+", " ", g.group(1)).strip()
                continue
        if m.cr is None:
            g = CR.match(s)
            if g:
                m.cr = g.group(1)
        if len(scores) < 6:
            g = ABILITY.match(s)
            if g:
                scores.append(g.group(1))
    if len(scores) >= 6:
        m.STR, m.DEX, m.CON, m.INT, m.WIS, m.CHA = scores[:6]


def detect_5e(lines: List[str], pages: List[int], book: str) -> List[Monster5e]:
    n = len(lines)
    starts: List[Tuple[int, str, re.Match]] = []
    used = set()
    for i, ln in enumerate(lines):
        st = SIZE_TYPE.match(ln.strip())
        if not st:
            continue
        # confirm: an Armor Class line within a few lines below
        if not any(AC.match(lines[k].strip())
                   for k in range(i + 1, min(n, i + 6)) if lines[k].strip()):
            continue
        a = _name_above(lines, i)
        if a is None or a in used:
            continue
        used.add(a)
        starts.append((a, lines[a].strip(), st))

    starts.sort()
    out: List[Monster5e] = []
    for k, (a, name, st) in enumerate(starts):
        e = starts[k + 1][0] if k + 1 < len(starts) else min(n, a + 80)
        e = min(e, a + 80)
        m = Monster5e(name=name, book=book, page=pages[a], start=a, end=e,
                      size=st.group(1).title(), type=st.group(2).lower(),
                      alignment=re.sub(r"\s+", " ", st.group(3)).strip().rstrip("."))
        parse_block(m, lines[a + 1:e])
        out.append(m)
    return out


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[Monster5e]]] = {
    "5e": detect_5e,
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
    monsters: List[Monster5e] = field(default_factory=list)


_5E = "D&D 5e"
SOURCES: List[Source] = [
    Source("bloodwar", "Blood War Bestiary (5e, 3pp)",
           Path(f"{_5E}/Third Party and DMs Guild/Blood War Bestiary.md"),
           "Blood War Bestiary (5e, DMs Guild)", "5e"),
    Source("dante", "Dante's Guide to Hell: Monster Manual (5e, 3pp)",
           Path(f"{_5E}/Third Party and DMs Guild/Dantes Guide to Hell - Monster Manual.md"),
           "Dante's Guide to Hell: Monster Manual (5e, DMs Guild)", "5e"),
    Source("xanathar", "Xanathar's Enemies and Allies (5e, 3pp)",
           Path(f"{_5E}/Third Party and DMs Guild/Xanathars Enemies and Allies.md"),
           "Xanathar's Enemies and Allies (5e, DMs Guild)", "5e"),
    Source("hordes", "The Book of Hordes (5e, 3pp)",
           Path(f"{_5E}/Third Party and DMs Guild/The Book of Hordes.md"),
           "The Book of Hordes (5e, DMs Guild)", "5e"),
    Source("diabolical", "Diabolical Designs (5e, 3pp)",
           Path(f"{_5E}/Third Party and DMs Guild/Diabolical Designs.md"),
           "Diabolical Designs (5e, DMs Guild)", "5e"),
    Source("chains", "Chains of Asmodeus (5e, 3pp)",
           Path(f"{_5E}/Third Party and DMs Guild/Chains of Asmodeus.md"),
           "Chains of Asmodeus (5e, DMs Guild)", "5e"),
    Source("legdragons", "Legendary Dragons (5e, 3pp)",
           Path(f"{_5E}/Third Party and DMs Guild/Legendary Dragons Complete Hybrid.md"),
           "Legendary Dragons Complete Hybrid (5e, DMs Guild)", "5e"),
    Source("descent", "Baldur's Gate: Descent into Avernus (5e)",
           Path(f"{_5E}/Official/Baldurs Gate - Descent into Avernus.md"),
           "Baldur's Gate: Descent into Avernus (5e, WotC)", "5e"),
    Source("manythings", "The Book of Many Things (5e)",
           Path(f"{_5E}/Official/The Book of Many Things.md"),
           "The Deck of Many Things: The Book of Many Things (5e, WotC)", "5e"),
    Source("pipyap", "Pipyap's Guide to the Nine Hells (5e, 3pp)",
           Path(f"{_5E}/Third Party and DMs Guild/Pipyaps Guide to the Nine Hells.md"),
           "Pipyap's Guide to the Nine Hells (5e, DMs Guild)", "5e"),
    Source("encavernus", "Encounters in Avernus (5e, 3pp)",
           Path(f"{_5E}/Third Party and DMs Guild/Encounters in Avernus.md"),
           "Encounters in Avernus (5e, DMs Guild)", "5e"),
    Source("darkhold", "Darkhold: Secrets of the Zhentarim (5e, 3pp)",
           Path(f"{_5E}/Third Party and DMs Guild/Darkhold - Secrets of the Zhentarim.md"),
           "Darkhold: Secrets of the Zhentarim (5e, DMs Guild)", "5e"),
    Source("larloch", "Larloch's Lexicon of Lichdom (5e, 3pp)",
           Path(f"{_5E}/Third Party and DMs Guild/Larlochs Lexicon of Lichdom.md"),
           "Larloch's Lexicon of Lichdom (5e, DMs Guild)", "5e"),
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
            src.monsters = DETECTORS[src.detector](src.lines, pages, src.book)
            src.coverage = f"ok — {len(src.monsters)} monsters from {path.name}"

    def all_monsters(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for m in src.monsters:
                yield src, m

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, m in self.all_monsters(book):
            nm = m.name.lower()
            if nm == q:
                exact.append((src, m))
            elif q in nm:
                partial.append((src, m))
        return exact if exact else partial


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# D&D 5e CREATURE INDEX — The New Path",
        "",
        "**Generated by `scripts/dnd5e_creature_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** These are **D&D 5th Edition** monsters — a DIFFERENT",
        "edition from the 3.5e `creature_index`. Every row is stamped",
        "`system: D&D 5e`; the campaign runs 3.5e / GURPS, so a 5e block is",
        "SOURCE MATERIAL for the system-translator skill, not campaign RAW. Use",
        "`--export \"NAME\"` for the translator packet.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.monsters)
        parsed_well += sum(1 for m in src.monsters if m.quick_fields() >= 3)
        sources_out.append({"key": src.key, "book": src.book, "system": SYSTEM,
                            "citation": src.citation, "coverage": src.coverage,
                            "monsters": [asdict(m) for m in src.monsters]})
        md.append(f"## {src.book} — {len(src.monsters)} monsters  *(system: {SYSTEM})*")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.monsters:
            md.append("| Monster | Size | Type | Alignment | AC | HP | CR | STR/DEX/CON/INT/WIS/CHA | Page |")
            md.append("|---|---|---|---|---|---|---|---|---|")
            for m in src.monsters:
                abil = "/".join(x or "—" for x in (m.STR, m.DEX, m.CON, m.INT, m.WIS, m.CHA))
                md.append(f"| {m.name} | {m.size or '—'} | {m.type or '—'} | "
                          f"{m.alignment or '—'} | {m.ac or '—'} | {m.hp or '—'} | "
                          f"{m.cr or '—'} | {abil} | {m.page if m.page is not None else '—'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/dnd5e_creature_harvest.py",
                    "system": SYSTEM, "corpus": str(corpus.base),
                    "total_monsters": total, "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 6:
        print(f"'{name}' matches {len(hits)} monsters; narrow with --book or the exact name:")
        for src, m in hits[:20]:
            print(f"  {m.name}   [{m.book}, p.{m.page}]")
        return 1
    packets = []
    for src, m in hits:
        body = [ln for ln in src.lines[m.start:m.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "dnd5e-creature-for-translation",
            "instructions": ("A D&D 5e monster (system: D&D 5e). Feed to the "
                             "system-translator skill to build the paired 3.5e AND "
                             "GURPS statlines — both required. The raw_block is OCR "
                             "text; check oddities against the source PDF."),
            "name": m.name, "system": SYSTEM,
            "source": {"book": m.book, "pdf_page": m.page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [m.start + 1, m.end], "citation": src.citation},
            "parsed": {k: v for k, v in asdict(m).items()
                       if k in ("size", "type", "alignment", "ac", "hp", "speed",
                                "cr", "STR", "DEX", "CON", "INT", "WIS", "CHA") and v},
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


FIXTURE = """## [PDF page 12]
Tormenting Shadow
Medium undead, neutral evil
Armor Class 14 (natural armor)
Hit Points 97 (13d8 + 39)
Speed 30 ft.
STR
DEX
CON
INT
WIS
CHA
8 (-1)
16 (+3)
16 (+3)
12 (+1)
12 (+1)
14 (+2)
Damage Resistances necrotic
Challenge 6 (2,300 XP)

Exsanguinator
Medium aberration, neutral evil
Armor Class 14 (natural armor)
Hit Points 45 (6d8 + 18)
Speed 40 ft.
STR
DEX
CON
INT
WIS
CHA
16 (+3)
14 (+2)
16 (+3)
6 (-2)
11 (+0)
8 (-1)
Challenge 1 (200 XP)
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    lines = FIXTURE.splitlines()
    monsters = detect_5e(lines, _pages_for(lines), "Blood War Bestiary (5e, 3pp)")
    names = [m.name for m in monsters]
    if names != ["Tormenting Shadow", "Exsanguinator"]:
        failures.append(f"fixture detected {names}, wanted the two 5e monsters")
    else:
        ts = monsters[0]
        got = (ts.size, ts.type, ts.alignment, ts.ac, ts.hp, ts.cr,
               ts.STR, ts.DEX, ts.CHA)
        want = ("Medium", "undead", "neutral evil", "14", "97", "6", "8", "16", "14")
        if got != want:
            failures.append(f"Tormenting Shadow {got}, wanted {want}")
        if ts.system != "D&D 5e":
            failures.append(f"system={ts.system!r}, must be 'D&D 5e'")

    if base.is_dir() and any((base / s.path).exists() for s in SOURCES):
        corpus = Corpus(base, _fresh_sources())
        total = sum(len(s.monsters) for s in corpus.sources)
        if total < 150:
            failures.append(f"only {total} 5e monsters indexed; expected > 150")
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
        found = sorted({(m.name, m.book, m.page or -1, m.cr or "—")
                        for _, m in corpus.all_monsters(args.book) if q in m.name.lower()})
        for name, bk, page, cr in found:
            loc = bk if page < 0 else f"{bk}, p.{page}"
            print(f"  {name}   [CR {cr}; {loc}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.monsters for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.monsters):4d} monsters" if src.monsters else "   0 monsters"
        print(f"  {src.book:44s} {status}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} D&D 5e monsters across {sum(1 for s in corpus.sources if s.monsters)} book(s); "
          f"{parsed_well} with 3+ quick fields. (system: {SYSTEM})")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
