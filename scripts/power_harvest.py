#!/usr/bin/env python3
"""power_harvest.py — collate psionic power blocks for translation.

THE PROCESS (companion to term_harvest.py, creature_harvest.py, and
item_harvest.py): the engine has spell, feat, creature, and item reference but
NO psionics — a whole subsystem the sourcebooks codify and the reference layer
lacks. This script harvests it.

It walks the psionics text extractions and produces the COLLATION:

    reference/power_index.json  — every power block found: name, book, PDF
                                  page, line span, and the quick fields a
                                  triage read needs (discipline, subdiscipline
                                  / descriptor, level list, display,
                                  manifesting time, range, power points, power
                                  resistance, save), parsed where clean
    reference/power_index.md    — the same index for human eyes, by book

The raw text is deliberately NOT copied into the repository (the Expanded
Psionics Handbook alone is ~50k lines of OCR). Instead, `--export` emits a
TRANSLATOR-READY PACKET on demand: the verbatim block plus provenance and
parsed fields, for the `system-translator` skill's paired 3.5e + GURPS build.

WORKFLOW
    python power_harvest.py                         # (re)build the index
    python power_harvest.py --search "energy"       # find candidates
    python power_harvest.py --export "Bite of the Wolf"
        -> JSON packet -> feed to the system-translator skill
    python power_harvest.py --selftest

GOVERNING SOURCES
    I:\\Sourcebooks\\_text\\D&D 3.5e\\Player Options\\Expanded Psionics
    Handbook.md — the OCR text extraction, power entries in the XPH grammar:

        Bite of the Wolf                         (name, Title Case, own line)
        Psychometabolism                         (discipline; closed set of 6,
                                                  optional "(Sub) [Descriptor]")
        Level: Psychic warrior 1
        Display: Visual; see text
        Manifesting Time: 1 standard action
        Range: Personal
        Target: You
        Duration: 1 min./level
        Power Points: 1
        [description, Augment paragraph]

    The anchor is a discipline line (one of the six psionic disciplines) whose
    block carries a psionics-specific field (Display / Power Points /
    Manifesting Time) close below — the same header-test discipline
    spell_lookup.py uses for the Spell Compendium. Discipline INTRO headers
    (e.g. a bare "Clairsentience" followed by "Clairsentience powers enable
    ...") carry none of those fields and are correctly rejected. The PDFs on
    I:\\Sourcebooks stand behind every extraction when the OCR is ambiguous.

    Complete Psionic uses the same grammar and is configured as the second
    source. Any future source gets its own Source/detector entry exactly as
    item_harvest.py does. A configured source whose file is missing prints
    NO COVERAGE and is never improvised.
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
OUT_JSON = REPO / "reference" / "power_index.json"
OUT_MD = REPO / "reference" / "power_index.md"

# ---------------------------------------------------------------------------
# Field grammar (the XPH power entry shape)
# ---------------------------------------------------------------------------

PAGE = re.compile(r"\[PDF page (\d+)\]")

DISCIPLINES = ("Clairsentience|Metacreativity|Psychokinesis|Psychometabolism|"
               "Psychoportation|Telepathy")
# A discipline line is a discipline word followed by END OF LINE or the start
# of a "(Subdiscipline)" / "[Descriptor]" trailer — and nothing that begins
# with a bare word. This rejects prose such as "Psychokinesis powers manipulate
# energy ..." (a word follows, not a bracket) while still catching lines whose
# long descriptor WRAPS across the OCR column break ("Telepathy (Compulsion)
# [Mind-" continued by "Affecting]" — 21 Compulsion powers in the XPH). The
# discipline-intro headers (a bare "Clairsentience" above prose) match this too
# but are rejected by the psionics-field test below, which they fail.
DISC_ANCHOR = re.compile(rf"^({DISCIPLINES})\s*($|[\[(].*)$")

FIELD_LABEL = re.compile(
    r"^(Level|Display|Manifesting Time|Range|Target|Targets|Area|Effect|"
    r"Duration|Saving Throw|Power Resistance|Power Points|Metapsionics|"
    r"Augment)\s*:", re.IGNORECASE)

# Psionics-specific fields — their presence just below a discipline line proves
# a real power block (spells and discipline intros have none of these).
PSI_MARK = re.compile(r"^(Display|Power Points|Manifesting Time)\s*:", re.IGNORECASE)

LEVEL = re.compile(r"^Level\s*:\s*(.+)$", re.IGNORECASE)
DISPLAY = re.compile(r"^Display\s*:\s*(.+)$", re.IGNORECASE)
MANIF = re.compile(r"^Manifesting Time\s*:\s*(.+)$", re.IGNORECASE)
RANGE = re.compile(r"^Range\s*:\s*(.+)$", re.IGNORECASE)
PP = re.compile(r"^Power Points\s*:\s*(.+)$", re.IGNORECASE)
PR = re.compile(r"^Power Resistance\s*:\s*(.+)$", re.IGNORECASE)
SAVE = re.compile(r"^Saving Throw\s*:\s*(.+)$", re.IGNORECASE)
RUNNING_HEADER = re.compile(
    r"^(?:CHAPTER\s+\d+|POWERS?(?:,\s+MANTLES)?|AND\s+ITEMS)$",
    re.IGNORECASE,
)


def _plausible_name(s: str) -> bool:
    s = s.strip()
    if not s or len(s) > 52 or len(s) < 2:
        return False
    if FIELD_LABEL.match(s) or DISC_ANCHOR.match(s):
        return False
    # Sentence punctuation marks prose; a trailing ":" is tolerated because the
    # OCR appends one to some names ("Teleport Trigge:" for "Teleport Trigger").
    if s.endswith((".", ",", ";")):
        return False
    letters = sum(ch.isalpha() for ch in s)
    return letters >= max(2, len(s) // 2)


def _complete_descriptor(lines: List[str], disc_idx: int, rest: str) -> Optional[str]:
    """The descriptor trailer after the discipline word, joined across the OCR
    column wrap when a bracket/paren is left open ("[Mind-" + "Affecting]")."""
    text = rest.strip()
    if not text:
        return None

    def unbalanced(t: str) -> bool:
        return t.count("[") > t.count("]") or t.count("(") > t.count(")")

    j, steps = disc_idx + 1, 0
    while unbalanced(text) and steps < 2 and j < len(lines):
        s = lines[j].strip()
        if s and not PAGE.search(lines[j]):
            text = text + s if text.endswith("-") else text + " " + s
            steps += 1
        j += 1
    return re.sub(r"\s+", " ", text).strip() or None


@dataclass
class Power:
    name: str
    book: str
    page: int
    start: int  # line span in the extraction, for --export
    end: int
    discipline: Optional[str] = None
    subdiscipline: Optional[str] = None   # the (Sub) / [Descriptor] trailer
    level: Optional[str] = None
    display: Optional[str] = None
    manifesting_time: Optional[str] = None
    range: Optional[str] = None
    power_points: Optional[str] = None
    power_resistance: Optional[str] = None
    save: Optional[str] = None

    def quick_fields(self) -> int:
        return sum(1 for v in (self.discipline, self.level, self.power_points,
                               self.range, self.save) if v)


def parse_quick_fields(power: Power, body_lines: List[str]) -> None:
    for raw in body_lines:
        line = raw.strip()
        if not line:
            continue
        for attr, rx in (("level", LEVEL), ("display", DISPLAY),
                         ("manifesting_time", MANIF), ("range", RANGE),
                         ("power_points", PP), ("power_resistance", PR),
                         ("save", SAVE)):
            if getattr(power, attr) is None:
                m = rx.match(line)
                if m:
                    setattr(power, attr, m.group(1).strip())
                    break


# ---------------------------------------------------------------------------
# Detectors — one per book grammar (no cross-import; add here)
# ---------------------------------------------------------------------------


def _name_above(lines: List[str], disc_idx: int, limit: int = 4) -> Optional[int]:
    """Nearest plausible name line above a discipline line, skipping blanks and
    page markers. Returns its index or None."""
    j, seen = disc_idx - 1, 0
    while j >= 0 and seen < limit:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            j -= 1
            continue
        seen += 1
        if _plausible_name(s):
            return j
        return None  # first content line above is prose/field -> not a power
    return None


def _find_name(lines: List[str], disc_idx: int) -> Optional[Tuple[int, str]]:
    """The power name above the discipline line. XPH names are single-line Title
    Case; other books (Complete Psionic) use ALL-CAPS names that WRAP across the
    column break ("ANALYZE DWEOMER," / "PSIONIC"). Gather extra ALL-CAPS
    fragments upward ONLY when the nearest name line is itself ALL-CAPS — so a
    Title-Case XPH name is never over-gathered — and title-case an ALL-CAPS
    result so it reads like the Title-Case XPH names. Returns (top line, name).
    """
    idx = _name_above(lines, disc_idx)
    if idx is None:
        return None
    name = lines[idx].strip()
    top = idx
    if name.isupper():
        frags = [name]
        j, gap = idx - 1, 0
        while j >= 0 and len(frags) < 4:
            s = lines[j].strip()
            if s == "" or PAGE.search(lines[j]):
                gap += 1
                if gap > 1:
                    break
                j -= 1
                continue
            # A running chapter header can sit directly above the first power
            # on a page. It terminates the name; it is never a wrapped fragment.
            if RUNNING_HEADER.match(s):
                # Keep the furniture inside the new power's span so the prior
                # power remains byte-identical and does not absorb this page
                # header. Validation still requires the real name immediately
                # afterward.
                top = j
                h = j - 1
                # Preserve the prior detector's four-fragment span boundary:
                # headers consume the remaining fragment slots, but never enter
                # the recovered name.
                remaining = 4 - len(frags)
                while remaining > 1 and h >= 0:
                    header = lines[h].strip()
                    if not header or PAGE.search(lines[h]):
                        break
                    if not RUNNING_HEADER.match(header):
                        break
                    top = h
                    remaining -= 1
                    h -= 1
                break
            # A wrapped ALL-CAPS fragment may legitimately end in a comma
            # ("ANALYZE DWEOMER," / "PSIONIC"), which _plausible_name forbids;
            # use a looser continuation test here.
            if s.isupper() and 3 <= len(s) <= 44 \
                    and not FIELD_LABEL.match(s) and not DISC_ANCHOR.match(s):
                frags.append(s)
                top, gap = j, 0
                j -= 1
                continue
            break
        frags.reverse()
        name = " ".join(frags)
    if name.isupper():
        name = name.title()
    return top, re.sub(r"\s+", " ", name).strip()


def _has_psi_field(lines: List[str], disc_idx: int, n: int,
                   window: int = 10) -> bool:
    j, seen = disc_idx + 1, 0
    while j < n and seen < window:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            j += 1
            continue
        seen += 1
        if PSI_MARK.match(s):
            return True
        j += 1
    return False


def detect_xph(lines: List[str], pages: List[int], book: str) -> List[Power]:
    n = len(lines)
    starts: List[Tuple[int, int, str, str, Optional[str]]] = []
    used = set()
    for i, ln in enumerate(lines):
        m = DISC_ANCHOR.match(ln.strip())
        if not m:
            continue
        if not _has_psi_field(lines, i, n):
            continue
        got = _find_name(lines, i)
        if got is None or got[0] in used:
            continue
        top, name = got
        used.add(top)
        sub = _complete_descriptor(lines, i, m.group(2))
        starts.append((top, i, name, m.group(1), sub))

    starts.sort()
    powers: List[Power] = []
    for k, (nm, disc_idx, name, disc, sub) in enumerate(starts):
        e = starts[k + 1][0] if k + 1 < len(starts) else min(n, nm + 80)
        e = min(e, nm + 80)
        power = Power(name=name, book=book, page=pages[nm], start=nm, end=e,
                      discipline=disc, subdiscipline=sub)
        parse_quick_fields(power, lines[nm + 1:e])
        powers.append(power)
    return powers


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[Power]]] = {
    "xph": detect_xph,
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
    powers: List[Power] = field(default_factory=list)


SOURCES: List[Source] = [
    Source(
        key="xph",
        book="Expanded Psionics Handbook",
        path=Path("D&D 3.5e/Player Options/Expanded Psionics Handbook.md"),
        citation="Expanded Psionics Handbook (WotC, 2004), power descriptions",
        detector="xph",
    ),
    Source(
        key="cpsi",
        book="Complete Psionic",
        path=Path("D&D 3.5e/Player Options/Complete Psionic.md"),
        citation="Complete Psionic (WotC, 2006), power descriptions",
        detector="xph",
    ),
]


# ---------------------------------------------------------------------------
# Corpus
# ---------------------------------------------------------------------------


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
            src.powers = DETECTORS[src.detector](src.lines, pages, src.book)
            src.coverage = f"ok — {len(src.powers)} powers from {path.name}"

    def all_powers(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for p in src.powers:
                yield src, p

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, p in self.all_powers(book):
            n = p.name.lower()
            if n == q:
                exact.append((src, p))
            elif q in n:
                partial.append((src, p))
        return exact if exact else partial


# ---------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# PSIONIC POWER INDEX — The New Path",
        "",
        "**Generated by `scripts/power_harvest.py`. Do not hand-edit; rerun",
        "the harvest.** One row per psionic power found in the psionics",
        "extractions. The raw text stays on `I:\\Sourcebooks` — use",
        "`python scripts/power_harvest.py --export \"NAME\"` to emit the",
        "translator-ready packet for any row, then hand that packet to the",
        "system-translator skill for the paired 3.5e + GURPS build.",
        "",
        "Every entry names its book and the PDF page the extraction recorded.",
        "This index holds the MECHANICAL vocabulary only — discipline, level,",
        "power points, range, and save — never invented facts; a field left as",
        "`—` is one the OCR did not cleanly yield, recoverable from the PDF.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.powers)
        parsed_well += sum(1 for p in src.powers if p.quick_fields() >= 3)
        sources_out.append({
            "key": src.key,
            "book": src.book,
            "citation": src.citation,
            "coverage": src.coverage,
            "powers": [asdict(p) for p in src.powers],
        })
        md.append(f"## {src.book} — {len(src.powers)} powers")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.powers:
            md.append("| Power | Discipline | Level | PP | Range | Save | Page |")
            md.append("|---|---|---|---|---|---|---|")
            for p in src.powers:
                disc = p.discipline or "—"
                if p.subdiscipline:
                    disc = f"{disc} {p.subdiscipline}"
                md.append(
                    f"| {p.name} | {disc} | {p.level or '—'} | "
                    f"{p.power_points or '—'} | {p.range or '—'} | "
                    f"{p.save or '—'} | {p.page or '—'} |"
                )
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps(
            {
                "generated_by": "scripts/power_harvest.py",
                "corpus": str(corpus.base),
                "total_powers": total,
                "sources": sources_out,
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
    if len(hits) > 6:
        print(f"'{name}' matches {len(hits)} powers; narrow with --book or the exact name:")
        for src, p in hits[:20]:
            print(f"  {p.name}   [{p.book}, p.{p.page}]")
        return 1
    packets = []
    for src, p in hits:
        body = [ln for ln in src.lines[p.start:p.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "psionic-power-for-translation",
            "instructions": (
                "Feed this packet to the system-translator skill. Both a 3.5e "
                "AND a GURPS treatment are required in the output — a conversion "
                "missing either system is incomplete (that skill's own rule). "
                "The raw_block is OCR text; check oddities against the source "
                "PDF on I:\\Sourcebooks before trusting a number."
            ),
            "name": p.name,
            "source": {
                "book": p.book, "pdf_page": p.page,
                "extraction": str(corpus.base / src.path),
                "lines": [p.start + 1, p.end],
                "citation": src.citation,
            },
            "parsed": {k: v for k, v in asdict(p).items()
                       if k in ("discipline", "subdiscipline", "level", "display",
                                "manifesting_time", "range", "power_points",
                                "power_resistance", "save") and v},
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


# ---------------------------------------------------------------------------
# Selftest — detector against an embedded fixture, then live corpus checks
# ---------------------------------------------------------------------------

FIXTURE = """## [PDF page 95]
Clairsentience

Clairsentience powers enable you to learn secrets long forgotten, to
glimpse the immediate future and predict the far future.

Bite of the Wolf

Psychometabolism

Level: Psychic warrior 1

Display: Visual; see text

Manifesting Time: 1 standard action

Range: Personal

Target: You

Duration: 1 min./level

Power Points: 1

Your teeth elongate and sharpen, becoming powerful weapons.

Apopsi

Telepathy [Mind-Affecting]

Level: Psion/wilder 9

Display: Auditory, material, and visual

Manifesting Time: 1 round

Range: Close (25 ft. + 5 ft./2 levels)

Target: One living psionic creature

Duration: Instantaneous

Saving Throw: Fortitude negates

Power Points: 17

You delete a portion of the subject's psionic knowledge.

Dominate, Psionic

Telepathy (Compulsion) [Mind-
Affecting]

Level: Telepath 4

Display: Visual

Manifesting Time: 1 round

Range: Close (25 ft. + 5 ft./2 levels)

Target: One humanoid

Duration: Concentration

Saving Throw: Will negates

Power Points: 7

You can control the actions of a humanoid creature.

CHAPTER 4
POWERS, MANTLES
AND ITEMS
ANALYZE DWEOMER,
PSIONIC

Clairsentience

Level: Seer 6

Display: Visual

Manifesting Time: 1 standard action

Range: Close (25 ft. + 5 ft./2 levels)

Power Points: 11

You discern the powers of a creature or object.
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "D&D 3.5e" / "Player Options").mkdir(parents=True)
        (d / "D&D 3.5e" / "Player Options" / "Expanded Psionics Handbook.md").write_text(
            FIXTURE, encoding="utf-8")
        corpus = Corpus(d, [Source(key="xph", book="Expanded Psionics Handbook",
                                   path=Path("D&D 3.5e/Player Options/Expanded Psionics Handbook.md"),
                                   citation="fixture", detector="xph")])
        powers = [p for _, p in corpus.all_powers()]
        names = [p.name for p in powers]
        # The four named powers are detected; the bare "Clairsentience" intro
        # and the CHAPTER/POWERS/AND ITEMS running header are rejected. Dominate
        # exercises a descriptor that WRAPS across the column break.
        want_names = ["Bite of the Wolf", "Apopsi", "Dominate, Psionic",
                      "Analyze Dweomer, Psionic"]
        if names != want_names:
            failures.append(f"fixture detected {names}, wanted {want_names} "
                            f"(Clairsentience intro rejected; wrapped Dominate "
                            f"descriptor joined; the ALL-CAPS wrapped name "
                            f"'ANALYZE DWEOMER,'/'PSIONIC' joined + title-cased)")
        else:
            bite = powers[0]
            got = (bite.discipline, bite.level, bite.range, bite.power_points, bite.save)
            want = ("Psychometabolism", "Psychic warrior 1", "Personal", "1", None)
            if got != want:
                failures.append(f"Bite of the Wolf quick fields {got}, wanted {want}")
            apopsi = powers[1]
            if apopsi.discipline != "Telepathy" or apopsi.subdiscipline != "[Mind-Affecting]" \
                    or apopsi.save != "Fortitude negates":
                failures.append(f"Apopsi discipline={apopsi.discipline!r} "
                                f"sub={apopsi.subdiscipline!r} save={apopsi.save!r}, "
                                f"wanted Telepathy / [Mind-Affecting] / Fortitude negates")
            dom = powers[2]
            if dom.discipline != "Telepathy" \
                    or dom.subdiscipline != "(Compulsion) [Mind-Affecting]" \
                    or dom.power_points != "7":
                failures.append(f"Dominate discipline={dom.discipline!r} "
                                f"sub={dom.subdiscipline!r} pp={dom.power_points!r}, "
                                f"wanted Telepathy / (Compulsion) [Mind-Affecting] / 7")

    if base.is_dir() and (base / SOURCES[0].path).exists():
        corpus = Corpus(base, _fresh_sources())
        counts = {s.key: len(s.powers) for s in corpus.sources}
        expected_counts = {"xph": 281, "cpsi": 128}
        if counts != expected_counts:
            failures.append(f"live source counts {counts}, wanted {expected_counts}")
        bite = corpus.find("bite of the wolf", book="xph")
        if not bite:
            failures.append("Bite of the Wolf not found in live XPH")
        else:
            b = bite[0][1]
            if b.discipline != "Psychometabolism":
                failures.append(f"live Bite of the Wolf discipline={b.discipline!r}, "
                                f"wanted Psychometabolism")
        for name, page in (("Energy Missile", 89),
                           ("See Invisibility, Psionic", 99)):
            found = corpus.find(name, book="cpsi")
            if not found:
                failures.append(f"Complete Psionic {name} not recovered")
            elif found[0][1].page != page:
                failures.append(
                    f"Complete Psionic {name} page={found[0][1].page}, "
                    f"wanted {page}")
        polluted = [p.name for s in corpus.sources for p in s.powers
                    if re.match(r"^(?:CHAPTER\b|POWERS?,\s+MANTLES\b)",
                                p.name, re.IGNORECASE)]
        if polluted:
            failures.append(f"running headers leaked into power names: {polluted[:5]}")
    else:
        print(f"  [SKIP] XPH extraction not found under {base} — fixture checks only")

    for failure in failures:
        print(f"SELFTEST FAIL: {failure}")
    print("selftest: " + ("PASS" if not failures else f"{len(failures)} failure(s)"))
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--corpus", type=Path, default=CORPUS,
                    help="base of the text extractions (default I:\\Sourcebooks\\_text)")
    ap.add_argument("--search", metavar="TEXT", help="substring search on indexed names")
    ap.add_argument("--book", help="restrict to one source (key or book title, e.g. xph)")
    ap.add_argument("--export", metavar="NAME", help="emit a translator-ready packet")
    ap.add_argument("--out", type=Path, help="write the packet here instead of stdout")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest(args.corpus)

    corpus = Corpus(args.corpus, _fresh_sources())

    if args.search:
        q = args.search.lower()
        found = sorted({(p.name, p.book, p.page, p.discipline or "—")
                        for _, p in corpus.all_powers(args.book) if q in p.name.lower()})
        for name, book, page, disc in found:
            print(f"  {name}   [{disc}, {book}, p.{page}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.powers for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.powers):5d} powers" if src.powers else "    0 powers"
        print(f"  {src.book:30s} {status}  [{src.coverage}]")
    if not any_ok:
        print("\nNothing harvested at all — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} powers across {sum(1 for s in corpus.sources if s.powers)} source(s); "
          f"{parsed_well} with 3+ quick fields parsed.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
