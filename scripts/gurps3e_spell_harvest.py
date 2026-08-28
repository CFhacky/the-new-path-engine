#!/usr/bin/env python3
"""gurps3e_spell_harvest.py — collate GURPS *3rd-edition* spells.

THE PROCESS (Chad, 2026-08-28, extending the GURPS shelf sideways in EDITION):
this is a D&D 3.5e / GURPS 4e hybrid campaign, but the project WELCOMES other
editions so long as they are kept in their OWN clearly-labeled index — the
translator tools convert them. GURPS 3e spells share the 4e class taxonomy
(Regular / Area / Missile / Melee / Blocking / Special / Information /
Enchantment) but are printed differently and were a large untouched shelf: the
3e Magic core (~660 class-tagged spell blocks) and the Grimoire (~590). They get
their OWN index, separate from the 4e `gurps_spell_index`, and every row is
stamped `system = "GURPS 3e"`.

    reference/gurps3e_spell_index.json — every GURPS 3e spell: name, book, PDF
                                         page, line span, system tag, and the 3e
                                         block (class, resist clause, difficulty,
                                         duration, cost, casting time,
                                         prerequisites, item)
    reference/gurps3e_spell_index.md   — the same index for human eyes

The raw text stays on I:\\Sourcebooks; `--export` emits a TRANSLATOR-READY packet
(verbatim block + provenance + parsed fields). The GURPS-3e half is native; the
system-translator skill builds the paired D&D 3.5e (and 4e) treatments.

WORKFLOW
    python gurps3e_spell_harvest.py                    # (re)build the index
    python gurps3e_spell_harvest.py --search "fire"    # find candidates
    python gurps3e_spell_harvest.py --export "Fireball"
    python gurps3e_spell_harvest.py --selftest

GOVERNING SOURCES  (I:\\Sourcebooks\\_text\\GURPS\\GURPS 3E\\)
    A GURPS 3e spell is a Title-Case NAME line, then its CLASS on its own line —
    a bare class word ("Regular", "Missile", ...) OR a class word plus a "; "
    resistance clause the 3e books print ("Regular; Resisted by IQ", "Area;
    Resisted by HT", "Special; Missile"). A description follows, then the field
    block: Duration / Cost or Base Cost / Time to cast / Prerequisite(s) / Item.
    The class word also occurs in prose ("Missile spell attacks are..."), so a
    class line is accepted only when a GURPS spell FIELD (Duration / Cost / Time
    to cast) follows within a window below AND a plausible Title-Case name sits
    directly above — the same header-test discipline the other harvests use.

    The books also carry a columnar "Improvised Spells" TABLE (name / class /
    college / time / duration / energy / prereq as bare, unlabeled lines). That
    table has no LABELED fields, so the field-below test walks straight past it —
    it is neither harvested nor allowed to pollute. A handful of spells whose OCR
    dropped the class line entirely (e.g. the "Create Fire" description) are not
    class-anchorable and are left out rather than guessed. A configured source
    whose file is missing prints NO COVERAGE. The PDFs stand behind every
    extraction — book RAW only, never invented; no cross-imports.
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
OUT_JSON = REPO / "reference" / "gurps3e_spell_index.json"
OUT_MD = REPO / "reference" / "gurps3e_spell_index.md"
SYSTEM = "GURPS 3e"

PAGE = re.compile(r"\[PDF page (\d+)\]")

CLASSES = ("Regular|Area|Missile|Melee|Blocking|Special|Information|Enchantment")
# The class line: a class word alone, or a class word + a "; " clause (the 3e
# resistance / compound-class note, e.g. "Regular; Resisted by IQ", "Special;
# Missile"). The clause is capped short and MUST use a ';' separator, so a prose
# line ("Regular Spells", "Missile spell attacks...", "Blocking, Criticals,...")
# is left alone. Group 1 = base class, group 2 = the clause (may be None).
CLASS_LINE = re.compile(rf"^({CLASSES})(?:\s*;\s*(.{{2,45}}?))?[.*]?\s*$")
# The difficulty marker "(VH)" the OCR sometimes drops on its own line between a
# spell name and its class line — skipped when finding the name.
DIFFICULTY = re.compile(r"^\((VH|H|M|E)\)$")
# The same marker usually sits at the END of the name line ("Shrink (VH)"); it is
# a real GURPS attribute (Very Hard, etc.), not part of the name. Anchored at
# end-of-line so genuine parentheticals ("Create Fire (Elemental)") survive.
NAME_DIFFICULTY = re.compile(r"^(.*?\S)\s*\((VH|H|M|E)\)\s*$")

DURATION = re.compile(r"^Duration\s*[:.]\s*(.+)$", re.IGNORECASE)
COST = re.compile(r"^(Base\s*Cost|Cost)\s*[:.]\s*(.+)$", re.IGNORECASE)
CASTTIME = re.compile(r"^(?:Time to cast|Casting Time)\s*[:.]\s*(.+)$", re.IGNORECASE)
PREREQ = re.compile(r"^Prerequisites?\s*[:.]\s*(.+)$", re.IGNORECASE)
ITEM = re.compile(r"^Items?\s*[:.]\s*(.+)$", re.IGNORECASE)
# The enchant-cost line ("Energy cost to create: 500 ...") is the key datum for
# Enchantment spells, which carry no fatigue Cost / Duration / Time-to-cast.
ENERGY = re.compile(r"^Energy cost(?: to create)?\s*[:.]\s*(.+)$", re.IGNORECASE)
# A GURPS-spell FIELD proves a class line begins a real spell (these do not
# appear under a random prose "Area"/"Regular"/"Special").
SPELL_FIELD = re.compile(r"^(Duration|Base\s*cost|Cost|Time to cast|Casting Time)\s*[:.]",
                         re.IGNORECASE)
# Enchantment spells confirm on the enchant-cost or the prerequisite line instead
# (they have no Duration/Cost/Time), so their class line takes a wider confirm.
ENCHANT_FIELD = re.compile(r"^(Energy cost|Prerequisites?)\b.*[:.]", re.IGNORECASE)

# Title-Case running / section headers that are NOT spell names, even though they
# pass the generic Title-Case test. Anchored; case-insensitive.
HEADER_REJECT = re.compile(
    r"^(?:Spell\s+List|Spell\s+Lists|Spell\s+Table|Improvised\s+Spells?|"
    r"Spell\s+Index|Index|Contents|Introduction|Chapter|Appendix|Glossary|"
    r"Principles\s+of\s+Magic|Magical\s+Items?|Magic\s+Items?|Enchantment\s+Spells?|"
    r"New\s+Spells?|The\s+Spells?|Prerequisites?|Ingredients?|Energy)\b",
    re.IGNORECASE)


def _plausible_name(s: str) -> bool:
    s = s.strip()
    if not (3 <= len(s) <= 40):
        return False
    if s.endswith((".", ",", ";", ":", "!", "?")):
        return False
    if s.isupper():           # a college header ("FIRE SPELLS"), not a spell
        return False
    if not s[0].isupper():
        return False
    if SPELL_FIELD.match(s) or CLASS_LINE.match(s) or PREREQ.match(s) or ITEM.match(s):
        return False
    if HEADER_REJECT.match(s):
        return False
    # a name ending in PLURAL " Spells" is a college/section header ("Fire
    # Spells", "Missile Spells"); the singular "X Spell" meta-spells (Catch
    # Spell, Throw Spell, Hang Spell, Maintain Spell, Suspend Spell) are REAL and
    # must survive, so only the plural is rejected.
    if re.search(r"\bSpells$", s, re.IGNORECASE):
        return False
    letters = sum(c.isalpha() for c in s)
    return letters >= max(3, int(len(s) * 0.6))


@dataclass
class Gurps3eSpell:
    name: str
    book: str
    page: Optional[int]
    start: int
    end: int
    system: str = SYSTEM
    spell_class: Optional[str] = None      # Regular / Area / Missile / ...
    resist: Optional[str] = None           # the "; Resisted by IQ" clause (3e)
    difficulty: Optional[str] = None       # VH / H / M / E (blank = Hard, default)
    duration: Optional[str] = None
    cost: Optional[str] = None
    time_to_cast: Optional[str] = None
    prerequisites: Optional[str] = None
    item: Optional[str] = None
    energy_cost: Optional[str] = None      # "Energy cost to create" (enchant/item)

    def quick_fields(self) -> int:
        return sum(1 for v in (self.spell_class, self.duration, self.cost,
                               self.time_to_cast, self.prerequisites) if v)


def _field_below(lines: List[str], class_idx: int, n: int, cls: str,
                 window: int = 48) -> bool:
    """A GURPS spell FIELD within `window` content lines below the class line.
    3e descriptions run long, so the window is generous; the plausible-name
    requirement above the class keeps prose "Regular"/"Area" lines out. An
    Enchantment class line also confirms on its enchant-cost / prerequisite line,
    since Enchantment spells carry no Duration / Cost / Time-to-cast."""
    enchant = cls.lower() == "enchantment"
    j, seen = class_idx + 1, 0
    while j < n and seen < window:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            j += 1
            continue
        seen += 1
        if SPELL_FIELD.match(s) or (enchant and ENCHANT_FIELD.match(s)):
            return True
        j += 1
    return False


def _name_above(lines: List[str], class_idx: int, limit: int = 3) -> Optional[int]:
    j, seen = class_idx - 1, 0
    while j >= 0 and seen < limit:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]) or DIFFICULTY.match(s):
            j -= 1
            continue
        seen += 1
        if _plausible_name(s):
            return j
        return None  # nearest content line above is prose/header -> not a spell
    return None


def parse_quick_fields(spell: Gurps3eSpell, body_lines: List[str]) -> None:
    for raw in body_lines:
        line = raw.strip()
        if not line:
            continue
        if spell.duration is None:
            m = DURATION.match(line)
            if m:
                spell.duration = m.group(1).strip()
                continue
        if spell.cost is None:
            m = COST.match(line)
            if m:
                spell.cost = m.group(2).strip()
                continue
        if spell.time_to_cast is None:
            m = CASTTIME.match(line)
            if m:
                spell.time_to_cast = m.group(1).strip()
                continue
        if spell.prerequisites is None:
            m = PREREQ.match(line)
            if m:
                spell.prerequisites = m.group(1).strip()
                continue
        if spell.item is None:
            m = ITEM.match(line)
            if m:
                spell.item = m.group(1).strip()
                continue
        if spell.energy_cost is None:
            m = ENERGY.match(line)
            if m:
                spell.energy_cost = m.group(1).strip()
                continue


def detect_gurps3e_spells(lines: List[str], pages: List[int], book: str) -> List[Gurps3eSpell]:
    n = len(lines)
    starts: List[Tuple[int, str, str, Optional[str]]] = []
    used = set()
    for i, ln in enumerate(lines):
        m = CLASS_LINE.match(ln.strip())
        if not m:
            continue
        if not _field_below(lines, i, n, m.group(1)):
            continue
        name_idx = _name_above(lines, i)
        if name_idx is None or name_idx in used:
            continue
        used.add(name_idx)
        starts.append((name_idx, lines[name_idx].strip(), m.group(1), m.group(2)))

    starts.sort()
    spells: List[Gurps3eSpell] = []
    for k, (nm, name, cls, resist) in enumerate(starts):
        e = starts[k + 1][0] if k + 1 < len(starts) else min(n, nm + 70)
        e = min(e, nm + 70)
        difficulty = None
        dm = NAME_DIFFICULTY.match(name)
        if dm:
            name, difficulty = dm.group(1).strip(), dm.group(2)
        resist_clean = None
        if resist:
            resist_clean = re.sub(r"\s+", " ", resist).strip(" .;,")
            if not resist_clean:
                resist_clean = None
        spell = Gurps3eSpell(name=name, book=book, page=pages[nm], start=nm, end=e,
                             spell_class=cls, resist=resist_clean, difficulty=difficulty)
        parse_quick_fields(spell, lines[nm + 1:e])
        spells.append(spell)

    # A GURPS spell can be listed under more than one college, so the same spell
    # may be detected twice; keep one entry per name — the richest (most parsed
    # fields), then the earliest — so the index is the distinct spell list.
    best: Dict[str, Gurps3eSpell] = {}
    for sp in spells:
        key = sp.name.lower()
        cur = best.get(key)
        if cur is None or sp.quick_fields() > cur.quick_fields():
            best[key] = sp
    return sorted(best.values(), key=lambda s: s.start)


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[Gurps3eSpell]]] = {
    "gurps3e_magic": detect_gurps3e_spells,
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
    spells: List[Gurps3eSpell] = field(default_factory=list)


_G3 = "GURPS/GURPS 3E"
SOURCES: List[Source] = [
    Source(key="magic", book="GURPS Magic (3e)",
           path=Path(f"{_G3}/gurps 3e - magic [missing p.120-125,127-128].md"),
           citation="GURPS Magic (SJGames, 3e), spell descriptions",
           detector="gurps3e_magic"),
    Source(key="grimoire", book="GURPS Grimoire (3e)",
           path=Path(f"{_G3}/gurps 3e - grimoire [missing p. 128].md"),
           citation="GURPS Grimoire (SJGames, 3e), additional spell descriptions",
           detector="gurps3e_magic"),
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
    return [Source(**{k: getattr(s, k) for k in
                      ("key", "book", "path", "citation", "detector")})
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
        "# GURPS 3e SPELL INDEX — The New Path",
        "",
        "**Generated by `scripts/gurps3e_spell_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** One row per GURPS *3rd-edition* spell — the 3e magic",
        "system (class / resistance / cost / casting time / prerequisites), kept",
        "SEPARATE from the 4e `gurps_spell_index` and from the D&D `spell_index`.",
        f"Every row is tagged `system = \"{SYSTEM}\"` so the translator tools know",
        "which edition they are reading. The raw text stays on `I:\\Sourcebooks` —",
        "use `--export \"NAME\"` for the translator-ready packet.",
        "",
        "A field left as `—` is one the OCR did not cleanly yield; `resist` is the",
        "3e `; Resisted by ...` clause printed on the class line where present.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.spells)
        parsed_well += sum(1 for sp in src.spells if sp.quick_fields() >= 3)
        sources_out.append({
            "key": src.key, "book": src.book, "system": SYSTEM,
            "citation": src.citation, "coverage": src.coverage,
            "spells": [asdict(sp) for sp in src.spells],
        })
        md.append(f"## {src.book} — {len(src.spells)} spells")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*System: {SYSTEM}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.spells:
            md.append("| Spell | Class | Resist | Duration | Cost | Cast time | Prerequisites | Page |")
            md.append("|---|---|---|---|---|---|---|---|")
            for sp in src.spells:
                pre = (sp.prerequisites or "—").replace("|", "/")
                if len(pre) > 40:
                    pre = pre[:37] + "..."
                cls = sp.spell_class or "—"
                if sp.difficulty:
                    cls = f"{cls} ({sp.difficulty})"
                res = (sp.resist or "—").replace("|", "/")
                md.append(f"| {sp.name} | {cls} | {res} | {sp.duration or '—'} | "
                          f"{sp.cost or '—'} | {sp.time_to_cast or '—'} | {pre} | "
                          f"{sp.page if sp.page is not None else '—'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/gurps3e_spell_harvest.py",
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
        print(f"'{name}' matches {len(hits)} spells; narrow with --book or the exact name:")
        for src, sp in hits[:20]:
            print(f"  {sp.name}   [{sp.book}, p.{sp.page}]")
        return 1
    packets = []
    for src, sp in hits:
        body = [ln for ln in src.lines[sp.start:sp.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "gurps3e-spell-for-translation",
            "instructions": (
                "A native GURPS 3rd-edition spell. Its GURPS-3e half is here; the "
                "system-translator skill builds the paired D&D 3.5e (and GURPS 4e) "
                "treatments. 3e prints the resistance on the class line ('Regular; "
                "Resisted by IQ') and rates spells Hard by default (a '(VH)' marks "
                "Very Hard). The raw_block is OCR text — check oddities against the "
                "source PDF on I:\\Sourcebooks."
            ),
            "name": sp.name,
            "system": SYSTEM,
            "source": {"book": sp.book, "pdf_page": sp.page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [sp.start + 1, sp.end], "citation": src.citation},
            "parsed": {k: v for k, v in asdict(sp).items()
                       if k in ("spell_class", "resist", "difficulty", "duration",
                                "cost", "time_to_cast", "prerequisites", "item",
                                "energy_cost") and v},
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


# An embedded fixture exercising a bare class line, the 3e "; Resisted by IQ"
# clause, the name-line "(VH)" difficulty marker, the section-header reject, and
# a prose standalone "Regular" (no field below) that must NOT be read as a spell.
FIXTURE = """## [PDF page 37]
include a small ruby worth 550.
Ignite Fire
Regular
This is the basic Fire spell. It produces a single spot of heat.
Duration: One second.
Cost: Depends on the amount of heat desired.
Prerequisite: none.
Item: Staff, wand or jewelry. Energy cost to create: 100.

FIRE SPELLS

Fireball
Missile
Lets caster throw a ball of fire from his hand.
Cost: Any amount from 1 to 3.
Time to cast: 1 to 3 seconds.
Prerequisite: Magery, Create Fire, Shape Fire.
Item: Staff or wand.

Fear
Area; Resisted by IQ
The subjects become afraid and flee.
Duration: 1 minute.
Cost: 1 per hex.
Prerequisite: none.

Shrink (VH)
Regular
The caster's size decreases, reducing his Strength and hit points.
Duration: 1 hour.
Cost: 4 to reduce the caster to half size.
Time to cast: 5 seconds.
Prerequisites: Magery 2 and Alter Body.

Power
Enchantment
Makes a magic item self-powered, decreasing the energy required to use it.
Energy cost to create: 500 each for the 1st and 2nd points of self-power.
Prerequisite: Recover Strength.

Some spells are described here as Regular in nature, in prose.
Regular
This paragraph continues without any field labels at all, and so this
standalone class word must not be treated as the start of a spell.
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    lines = FIXTURE.splitlines()
    spells = detect_gurps3e_spells(lines, _pages_for(lines), "GURPS Magic (3e)")
    names = [s.name for s in spells]
    if names != ["Ignite Fire", "Fireball", "Fear", "Shrink", "Power"]:
        failures.append(f"fixture detected {names}, wanted "
                        f"['Ignite Fire', 'Fireball', 'Fear', 'Shrink', 'Power'] "
                        f"(FIRE SPELLS header + prose 'Regular' rejected; "
                        f"'(VH)' stripped from Shrink; Enchantment 'Power' confirmed "
                        f"on its Energy-cost line)")
    else:
        ig = spells[0]
        got = (ig.spell_class, ig.duration, ig.cost, ig.prerequisites)
        want = ("Regular", "One second.", "Depends on the amount of heat desired.", "none.")
        if got != want:
            failures.append(f"Ignite Fire fields {got}, wanted {want}")
        if ig.item is None or "Staff" not in ig.item:
            failures.append(f"Ignite Fire item={ig.item!r}, wanted the staff line")
        fb = spells[1]
        if fb.spell_class != "Missile" or fb.cost != "Any amount from 1 to 3.":
            failures.append(f"Fireball class={fb.spell_class!r} cost={fb.cost!r}, "
                            f"wanted Missile / Any amount from 1 to 3.")
        fear = spells[2]
        if fear.spell_class != "Area" or fear.resist != "Resisted by IQ":
            failures.append(f"Fear class={fear.spell_class!r} resist={fear.resist!r}, "
                            f"wanted Area / Resisted by IQ")
        sh = spells[3]
        if sh.name != "Shrink" or sh.difficulty != "VH":
            failures.append(f"Shrink name/difficulty=({sh.name!r},{sh.difficulty!r}), "
                            f"wanted ('Shrink','VH')")
        pw = spells[4]
        if pw.spell_class != "Enchantment" or not pw.energy_cost:
            failures.append(f"Power class={pw.spell_class!r} energy_cost={pw.energy_cost!r}, "
                            f"wanted Enchantment with a parsed energy_cost")
        if any(s.system != SYSTEM for s in spells):
            failures.append(f"system tag not '{SYSTEM}' on every row")

    if base.is_dir() and (base / SOURCES[0].path).exists():
        corpus = Corpus(base, _fresh_sources())
        total = sum(len(s.spells) for s in corpus.sources)
        if total < 400:
            failures.append(f"only {total} GURPS 3e spells indexed across the two "
                            f"books; expected > 400")
        # a few known GURPS spells, with a class/cost spot-check
        fb = corpus.find("fireball", book="magic")
        if not fb:
            failures.append("Fireball not found in live GURPS Magic (3e)")
        elif fb[0][1].spell_class != "Missile":
            failures.append(f"live Fireball class={fb[0][1].spell_class!r}, wanted Missile")
        elif not fb[0][1].cost:
            failures.append("live Fireball has no parsed cost")
        if not corpus.find("light", book="magic"):
            failures.append("Light not found in live GURPS Magic (3e)")
        if not corpus.find("ignite fire", book="magic"):
            failures.append("Ignite Fire not found in live GURPS Magic (3e)")
        # the resistance clause must be captured for the bulk of Resisted spells
        resisted = [sp for _, sp in corpus.all_spells() if sp.resist]
        if len(resisted) < 100:
            failures.append(f"only {len(resisted)} spells carry a parsed resist "
                            f"clause; expected >= 100 across the two books")
        # Enchantment spells (confirmed on their Energy-cost line) must be present
        ench = [sp for _, sp in corpus.all_spells() if sp.spell_class == "Enchantment"]
        if len(ench) < 40:
            failures.append(f"only {len(ench)} Enchantment spells indexed; expected "
                            f">= 40 (they confirm on Energy cost / Prerequisite)")
        # most rows should parse 3+ quick fields
        well = sum(1 for _, sp in corpus.all_spells() if sp.quick_fields() >= 3)
        if well < total * 0.7:
            failures.append(f"only {well}/{total} spells have 3+ quick fields "
                            f"parsed; expected >= 70%")
    else:
        print("  [SKIP] GURPS 3e magic extractions not found — fixture checks only")

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
        found = sorted({(sp.name, sp.book, sp.page or -1, sp.spell_class or "—")
                        for _, sp in corpus.all_spells(args.book) if q in sp.name.lower()})
        for name, bk, page, cls in found:
            loc = bk if page < 0 else f"{bk}, p.{page}"
            print(f"  {name}   [{cls}; {loc}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.spells for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.spells):5d} spells" if src.spells else "    0 spells"
        print(f"  {src.book:24s} {status}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} GURPS 3e spells across "
          f"{sum(1 for s in corpus.sources if s.spells)} book(s); "
          f"{parsed_well} with 3+ quick fields parsed.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
