#!/usr/bin/env python3
"""ad2e_spells_harvest.py — collate AD&D 2nd-edition spells (labelled).

THE PROCESS (Chad, 2026-08-28): other editions are welcome AS LONG AS labelled by
edition/system — the translator tools convert them. This is the AD&D 2e SPELL
index (wizard and priest spells), a DIFFERENT edition from the 3.5e `spell_index`
and the 5e `dnd5e_spell_index`. Every row is stamped `"system": "AD&D 2e"`.

    reference/ad2e_spell_index.json — every 2e spell: name, school(s), level,
                                      wizard/priest, sphere (priest), range,
                                      components, duration, casting time, area of
                                      effect, saving throw, book, page
    reference/ad2e_spell_index.md   — the same, for human eyes

GOVERNING SOURCES
    AD&D 2e books with NEW spell lists on `I:\\Sourcebooks\\_text\\AD&D\\` —
    Menzoberranzan, Drow of the Underdark (FOR2), Elves of Evermeet (FOR5),
    Giantcraft (FOR7). Each spell is a "Nth-Level Spell" header, a NAME (School)
    line, then the fields — either inline ("Range: 40 yards") or as an alternating
    label/value column-dump ("Range:" / "40 yards"). The anchor is the field block
    (a Range/Sphere line with Casting Time and Area of Effect close below); the
    name+school is the parenthesised line above, and the level is the header above
    that. A configured source whose file is missing prints NO COVERAGE.
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
OUT_JSON = REPO / "reference" / "ad2e_spell_index.json"
OUT_MD = REPO / "reference" / "ad2e_spell_index.md"
SYSTEM = "AD&D 2e"

PAGE = re.compile(r"\[PDF page (\d+)\]")
FIELD_START = re.compile(r"^(Sphere|Range)\s*:", re.IGNORECASE)
FIELDS = [
    (re.compile(r"^Sphere\s*:\s*(.*)$", re.IGNORECASE), "sphere"),
    (re.compile(r"^Range\s*:\s*(.*)$", re.IGNORECASE), "range"),
    (re.compile(r"^Components?\s*:\s*(.*)$", re.IGNORECASE), "components"),
    (re.compile(r"^Duration\s*:\s*(.*)$", re.IGNORECASE), "duration"),
    (re.compile(r"^Casting Time\s*:\s*(.*)$", re.IGNORECASE), "casting_time"),
    (re.compile(r"^Area of Effect\s*:\s*(.*)$", re.IGNORECASE), "area_of_effect"),
    (re.compile(r"^Saving Throw\s*:\s*(.*)$", re.IGNORECASE), "saving_throw"),
]
ANY_FIELD = re.compile(r"^(Sphere|Range|Components?|Duration|Casting Time|"
                       r"Area of Effect|Saving Throw)\s*:", re.IGNORECASE)
LEVEL_WORDS = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
               "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9}
LEVEL_HDR = re.compile(r"^(First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth)"
                       r"[-\s]Level\s+(Spell|Priest Spell|Wizard Spell)s?\b", re.IGNORECASE)
LEVEL_HDR2 = re.compile(r"^([1-9])(?:st|nd|rd|th)[-\s]Level\b", re.IGNORECASE)
# a name line carries the school in parentheses
NAME_SCHOOL = re.compile(r"^(.{2,44}?)\s*\(([A-Za-z/,'’ \-]+)\)?\s*$")


@dataclass
class Ad2eSpell:
    name: str
    book: str
    page: Optional[int]
    start: int
    end: int
    system: str = SYSTEM
    school: Optional[str] = None
    level: Optional[int] = None
    kind: Optional[str] = None            # wizard | priest
    sphere: Optional[str] = None
    range: Optional[str] = None
    components: Optional[str] = None
    duration: Optional[str] = None
    casting_time: Optional[str] = None
    area_of_effect: Optional[str] = None
    saving_throw: Optional[str] = None

    def quick_fields(self) -> int:
        return sum(1 for v in (self.school, self.range, self.duration, self.casting_time) if v)


def _confirms(lines: List[str], i: int, n: int) -> bool:
    """A field block: Casting Time and Area of Effect appear within a few lines."""
    seen = set()
    for j in range(i, min(n, i + 18)):
        s = lines[j].strip()
        if re.match(r"^Casting Time\s*:", s, re.IGNORECASE):
            seen.add("ct")
        elif re.match(r"^Area of Effect\s*:", s, re.IGNORECASE):
            seen.add("aoe")
    return len(seen) == 2


def _clean_school(s: str) -> str:
    s = re.sub(r"([A-Za-z])-\s+([a-z])", r"\1\2", s)   # de-hyphenate "Abjura- tion"
    s = re.sub(r"\s*/\s*", "/", s)                      # "Conjuration/ Summoning"
    return re.sub(r"\s+", " ", s).strip()


def _name_above(lines: List[str], i: int) -> Optional[Tuple[int, str, str]]:
    """Gather the NAME (School) line above the field block, joining a wrapped
    parenthesised school ("Web of Shadows (Conjuration/" / "Summoning)"). `top`
    is the index of the line that opens the name (carries the "(")."""
    j = i - 1
    while j >= 0:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            j -= 1
            continue
        block, top = s, j
        if "(" not in block and ")" in block:
            # wrapped: this line closes the parens; climb to the line with "("
            gathered = [s]
            u_idx = j - 1
            while u_idx >= 0 and len(gathered) < 4:
                u = lines[u_idx].strip()
                if u == "" or PAGE.search(lines[u_idx]):
                    u_idx -= 1
                    continue
                gathered.insert(0, u)
                top = u_idx
                if "(" in u:
                    break
                u_idx -= 1
            block = " ".join(gathered)
        m = NAME_SCHOOL.match(block)
        if m and m.group(1).strip() and m.group(1)[0].isalpha():
            return top, m.group(1).strip(), _clean_school(m.group(2))
        return None
    return None




def detect_ad2e_spells(lines: List[str], pages: List[int], book: str) -> List[Ad2eSpell]:
    n = len(lines)
    # level-group headers ("First-Level Spells", "Ninth Level Spell") apply to all
    # spells below them until the next header — collect them as ordered markers.
    lvl_markers: List[Tuple[int, int, Optional[str]]] = []
    for i, ln in enumerate(lines):
        s = ln.strip()
        m = LEVEL_HDR.match(s)
        if m:
            kind = ("priest" if "priest" in s.lower()
                    else "wizard" if "wizard" in s.lower() else None)
            lvl_markers.append((i, LEVEL_WORDS[m.group(1).lower()], kind))
            continue
        m2 = LEVEL_HDR2.match(s)
        if m2:
            lvl_markers.append((i, int(m2.group(1)), None))

    def level_ctx(idx: int) -> Tuple[Optional[int], Optional[str]]:
        lvl = kind = None
        for mi, ml, mk in lvl_markers:
            if mi < idx:
                lvl, kind = ml, (mk if mk is not None else kind)
            else:
                break
        return lvl, kind

    starts: List[Tuple[int, str, str, int]] = []
    used = set()
    for i, ln in enumerate(lines):
        s = ln.strip()
        if not FIELD_START.match(s) or not _confirms(lines, i, n):
            continue
        got = _name_above(lines, i)
        if got is None or got[0] in used:
            continue
        top, name, school = got
        used.add(top)
        starts.append((top, name, school, i))

    starts.sort()
    out: List[Ad2eSpell] = []
    for k, (top, name, school, fi) in enumerate(starts):
        e = starts[k + 1][0] if k + 1 < len(starts) else min(n, top + 70)
        e = min(e, top + 70)
        level, kind = level_ctx(top)
        sp = Ad2eSpell(name=name, book=book, page=pages[top], start=top, end=e,
                       school=school, level=level, kind=kind)
        if sp.sphere is None and school and re.match(r"^Sphere", lines[fi].strip(), re.IGNORECASE):
            sp.kind = sp.kind or "priest"
        # read the fields (inline "Label: value" or alternating "Label:" / value)
        j = fi
        while j < min(n, fi + 24):
            s = lines[j].strip()
            hit = None
            for rx, attr in FIELDS:
                m = rx.match(s)
                if m:
                    hit = (attr, m.group(1).strip())
                    break
            if hit:
                attr, val = hit
                if not val:                       # alternating: value on the next line
                    v = j + 1
                    while v < n and (lines[v].strip() == "" or PAGE.search(lines[v])):
                        v += 1
                    if v < n and not ANY_FIELD.match(lines[v].strip()):
                        val = lines[v].strip()
                        j = v
                if getattr(sp, attr) is None and val:
                    setattr(sp, attr, re.sub(r"\s+", " ", val))
                j += 1
                continue
            if j > fi and ANY_FIELD.match(s) is None and sp.saving_throw:
                break                             # description prose begins
            j += 1
        if sp.sphere and not sp.kind:
            sp.kind = "priest"
        elif sp.school and not sp.kind:
            sp.kind = "wizard"
        out.append(sp)

    best: Dict[str, Ad2eSpell] = {}
    for sp in out:
        best.setdefault(sp.name.lower(), sp)
    return sorted(best.values(), key=lambda x: x.start)


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[Ad2eSpell]]] = {
    "ad2e": detect_ad2e_spells,
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
    spells: List[Ad2eSpell] = field(default_factory=list)


_A = "AD&D"
SOURCES: List[Source] = [
    Source("menzo", "Menzoberranzan Boxed Set (2e)",
           Path(f"{_A}/Menzoberranzan Boxed Set.md"),
           "Menzoberranzan (TSR, AD&D 2e), new drow spells", "ad2e"),
    Source("drow", "FOR2 Drow of the Underdark (2e)",
           Path(f"{_A}/FOR2 - Drow of the Underdark.md"),
           "FOR2: Drow of the Underdark (TSR, AD&D 2e), new spells", "ad2e"),
    Source("evermeet", "FOR5 Elves of Evermeet (2e)",
           Path(f"{_A}/FOR5 - Elves of Evermeet.md"),
           "FOR5: Elves of Evermeet (TSR, AD&D 2e), new spells", "ad2e"),
    Source("giantcraft", "FOR7 Giantcraft (2e)",
           Path(f"{_A}/FOR7 - Giantcraft.md"),
           "FOR7: Giantcraft (TSR, AD&D 2e), new spells", "ad2e"),
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
            src.spells = DETECTORS[src.detector](src.lines, pages, src.book)
            src.coverage = f"ok — {len(src.spells)} spells from {path.name}"

    def all_spells(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for sp in src.spells:
                yield src, sp

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, sp in self.all_spells(book):
            nm = sp.name.lower()
            if nm == q:
                exact.append((src, sp))
            elif q in nm:
                partial.append((src, sp))
        return exact if exact else partial


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# AD&D 2e SPELL INDEX — The New Path",
        "",
        "**Generated by `scripts/ad2e_spells_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** **AD&D 2nd Edition** spells — a DIFFERENT edition",
        "from the 3.5e `spell_index` and the 5e `dnd5e_spell_index`. Every row is",
        "stamped `system: AD&D 2e`; a 2e spell is SOURCE MATERIAL for the system-",
        "translator skill. Priest spells carry a `sphere`; wizard spells a school.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.spells)
        parsed_well += sum(1 for sp in src.spells if sp.quick_fields() >= 3)
        sources_out.append({"key": src.key, "book": src.book, "system": SYSTEM,
                            "citation": src.citation, "coverage": src.coverage,
                            "spells": [asdict(sp) for sp in src.spells]})
        md.append(f"## {src.book} — {len(src.spells)} spells  *(system: {SYSTEM})*")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.spells:
            md.append("| Spell | Lvl | Kind | School / Sphere | Range | Duration | Casting | Save | Page |")
            md.append("|---|---|---|---|---|---|---|---|---|")
            for sp in src.spells:
                sch = sp.sphere or sp.school or "—"
                md.append(f"| {sp.name} | {sp.level or '—'} | {sp.kind or '—'} | {sch} | "
                          f"{sp.range or '—'} | {sp.duration or '—'} | {sp.casting_time or '—'} | "
                          f"{sp.saving_throw or '—'} | {sp.page if sp.page is not None else '—'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/ad2e_spells_harvest.py",
                    "system": SYSTEM, "corpus": str(corpus.base),
                    "total_spells": total, "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 6:
        print(f"'{name}' matches {len(hits)} spells; narrow with the exact name:")
        for src, sp in hits[:20]:
            print(f"  {sp.name}   [{sp.book}, p.{sp.page}]")
        return 1
    packets = []
    for src, sp in hits:
        body = [ln for ln in src.lines[sp.start:sp.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "ad2e-spell-for-translation",
            "instructions": ("An AD&D 2e spell (system: AD&D 2e). Feed to the "
                             "system-translator skill for the 3.5e / 5e / GURPS "
                             "treatment. The raw_block is born-digital text."),
            "name": sp.name, "system": SYSTEM,
            "source": {"book": sp.book, "pdf_page": sp.page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [sp.start + 1, sp.end], "citation": src.citation},
            "parsed": {k: v for k, v in asdict(sp).items()
                       if k in ("school", "level", "kind", "sphere", "range",
                                "components", "duration", "casting_time",
                                "area_of_effect", "saving_throw") and v},
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


FIXTURE_INLINE = """## [PDF page 100]
Ninth Level Spell
Web of Shadows (Conjuration/
Summoning)
Range: 40 yards
Components: V, S, M
Duration: 1 hour/level
Casting Time: 1 round
Area of Effect: 40 sq. ft./level
Saving Throw: Special
This spell fills an area with shadowy strands.
"""
FIXTURE_ALT = """## [PDF page 27]
Fourth-Level Spell
Lesser Spellsong (Evocation, Alteration)
Sphere:
Creation
Range:
Variable
Components:
V,S
Duration:
Variable
Casting Time:
1 round
Area of Effect:
Variable
Saving Throw:
None
The bard weaves a lesser song of magic.
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    a = detect_ad2e_spells(FIXTURE_INLINE.splitlines(), _pages_for(FIXTURE_INLINE.splitlines()),
                           "Menzoberranzan Boxed Set (2e)")
    if [s.name for s in a] != ["Web of Shadows"]:
        failures.append(f"inline fixture names {[s.name for s in a]}, wanted ['Web of Shadows']")
    else:
        w = a[0]
        if (w.school, w.level, w.range, w.casting_time, w.saving_throw) != \
                ("Conjuration/Summoning", 9, "40 yards", "1 round", "Special"):
            failures.append(f"Web of Shadows {(w.school, w.level, w.range, w.casting_time, w.saving_throw)}")
        if w.kind != "wizard" or w.system != "AD&D 2e":
            failures.append(f"Web of Shadows kind/system {(w.kind, w.system)}")

    b = detect_ad2e_spells(FIXTURE_ALT.splitlines(), _pages_for(FIXTURE_ALT.splitlines()),
                           "FOR2 Drow of the Underdark (2e)")
    if [s.name for s in b] != ["Lesser Spellsong"]:
        failures.append(f"alt fixture names {[s.name for s in b]}, wanted ['Lesser Spellsong']")
    else:
        ls = b[0]
        if (ls.level, ls.sphere, ls.range, ls.kind) != (4, "Creation", "Variable", "priest"):
            failures.append(f"Lesser Spellsong {(ls.level, ls.sphere, ls.range, ls.kind)} "
                            f"(alternating label/value not read)")

    if base.is_dir() and any((base / s.path).exists() for s in SOURCES):
        corpus = Corpus(base, _fresh_sources())
        total = sum(len(s.spells) for s in corpus.sources)
        if total < 40:
            failures.append(f"only {total} 2e spells indexed; expected > 40")
    else:
        print("  [SKIP] AD&D 2e extractions not found — fixture checks only")

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
        found = sorted({(sp.name, sp.level or 0, sp.kind or "—",
                         sp.sphere or sp.school or "—", sp.page or -1)
                        for _, sp in corpus.all_spells(args.book) if q in sp.name.lower()})
        for nm, lvl, kind, sch, page in found:
            print(f"  {nm}  [L{lvl} {kind} {sch}; p.{page}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.spells for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.spells):4d} spells" if src.spells else "   0 spells"
        print(f"  {src.book:36s} {status}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} AD&D 2e spells across {sum(1 for s in corpus.sources if s.spells)} book(s). "
          f"(system: {SYSTEM})")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
