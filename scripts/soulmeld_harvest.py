#!/usr/bin/env python3
"""soulmeld_harvest.py — collate the D&D 3.5 incarnum soulmelds (Magic of Incarnum).

THE PROCESS: incarnum (the incarnate / soulborn / totemist classes) is a self-
contained D&D 3.5 subsystem the reference layer lacked. A meldshaper shapes
"soulmelds" — semi-permanent items of soul-stuff — and binds them to body
"chakras" for greater effect. Magic of Incarnum closes with three soulmeld
summary tables (one per class), each listing every soulmeld by chakra with its
basic effect. Those tables were extracted from a BORN-DIGITAL PDF text layer
(characters exact, not OCR — the book is Cyrillic-free and clean).

    reference/soulmeld_index.json — every soulmeld: name, basic effect, the
                                    classes that can shape it, the chakras it can
                                    bind to, PDF page, and its true full-description
                                    [start,end] line span
    reference/soulmeld_index.md   — the same, for human eyes

GOVERNING SOURCE
    I:\\Sourcebooks\\_text\\D&D 3.5e\\Player Options\\Magic of Incarnum.md — the
    three soulmeld summary tables (Table 4-1 Incarnate, 4-2 Soulborn, 4-3
    Totemist), each a Chakra / Soulmeld / Basic Effect column-dump grouped under
    chakra headers. A soulmeld shared by several classes / bindable to several
    chakras is merged into one entry that records the union. The ALL-CAPS heading
    and Descriptors/Classes/Chakra fields bind every row to its full description
    on PDF pages 54–94. Native D&D 3.5e.
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
OUT_JSON = REPO / "reference" / "soulmeld_index.json"
OUT_MD = REPO / "reference" / "soulmeld_index.md"

PAGE = re.compile(r"\[PDF page (\d+)\]")
TABLE = re.compile(r"Table\s*4[–\-]\d:\s*(Incarnate|Soulborn|Totemist)\s+Soulmelds", re.IGNORECASE)
FOOTNOTE_END = re.compile(r"^\s*[*†]\s*All totemist soulmelds", re.IGNORECASE)
CHAKRAS = ("Crown", "Feet", "Hands", "Arms", "Brow", "Shoulders",
           "Throat", "Waist", "Heart", "Soul", "Totem")
COLHDR = re.compile(r"^(Chakra|Soulmeld|Basic Effect)[\s*†\u2020]*$", re.IGNORECASE)
# an effect (rather than a soulmeld name) tends to start with one of these
EFFECT_START = re.compile(
    r"^(\+|[-–]|\d|Can[’'`]?t|Cannot|Create|Gain|Grant|Heal|Immune|Detect|Touch|"
    r"Move|Walk|Fly|Low-light|Bonus|Continue|Exist|Teleport|Protection|Uncanny|"
    r"Chosen|Constant|See|Reroll|Ignore|Deal|Add|Reduce|Halve|Negate|Reflect|"
    r"Absorb|Emit|Sprout|Grow|Summon|Sense|Speak|Understand|Breathe|Swim|Regain|"
    r"Suppress|Redirect|Change|Produces?|Ignores?|Immunity|Resistance|Damage|"
    r"Enhances?|Ability|Access|Reduction|Reduce|Cure|Convert|Draw|Enable|Extend|"
    r"Improve|Increase|Leave|Never|No\b|Once|Speed|Store|Take|Use|Weapon|You|"
    r"Spell|Telepathy|Fire|Cold|Acid|Sonic|Electricity)\b")
NOTE = re.compile(r"^[*†]|^(See full soulmeld|Chakra binds for these)", re.IGNORECASE)
# a soulmeld DESCRIPTION block (interleaved with the table by column) is marked by
# these field lines; they and the ALL-CAPS description name must not be read as rows
DESC_FIELD = re.compile(r"^(Descriptors|Classes|Chakra|Saving Throw|Essentia|"
                        r"Prerequisite|Chakra Bind)\b", re.IGNORECASE)


def _name_ok(s: str) -> bool:
    # a soulmeld name is a short Title-ish noun phrase, not a full effect sentence
    # and not an ALL-CAPS running header
    if not s or not s[:1].isupper() or s.isupper() or EFFECT_START.match(s):
        return False
    return len(s) <= 36 and len(s.split()) <= 5 and bool(re.search(r"[A-Za-z]", s))


@dataclass
class Soulmeld:
    name: str
    book: str
    page: Optional[int]
    start: int
    end: int
    basic_effect: Optional[str] = None
    classes: List[str] = field(default_factory=list)
    chakras: List[str] = field(default_factory=list)

    def quick_fields(self) -> int:
        return sum(1 for v in (self.basic_effect, self.classes, self.chakras) if v)


def _split_same_line(s: str) -> Tuple[str, Optional[str]]:
    """A few rows put name and effect on one line ('Threefold Mask of the Chimera
    Can't be flanked'). Split at the first word that starts an effect."""
    words = s.split()
    for i in range(2, len(words)):        # keep at least two words in the name
        # "Heart of Fire" is a name, not "Heart of" + an effect beginning Fire.
        if EFFECT_START.match(words[i]) and words[i - 1].lower() not in {
                "of", "the", "and", "or"}:
            return " ".join(words[:i]).strip(), " ".join(words[i:]).strip()
    return s, None


def _is_real_table_header(lines: List[str], i: int) -> bool:
    # the real summary-table header is followed, within a few lines, by the
    # "Chakra" column header; the table-of-contents entry is not.
    if not TABLE.search(lines[i]):
        return False
    return any(lines[j].strip().lower().startswith("chakra")
               for j in range(i + 1, min(len(lines), i + 5)))


def _norm_name(s: str) -> str:
    s = s.translate(str.maketrans({"\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl"}))
    return re.sub(r"[^a-z0-9]+", " ", s.casefold()).strip()


def _title_name(s: str) -> str:
    titled = s.title()
    return re.sub(r"\b(Of|The|And|Or|To)\b", lambda m: m.group(0).lower(), titled)


def _caps_fragment(s: str) -> bool:
    s = s.strip()
    if (not s or PAGE.search(s) or s.isdigit()
            or s in {"CHAPTER 4", "SOULMELDS"} or len(s) > 52):
        return False
    letters = "".join(ch for ch in s if ch.isalpha())
    return bool(letters) and letters == letters.upper()


def _description_spans(lines: List[str], pages: List[int]) -> Dict[str, Tuple[str, int, int, int]]:
    """Find the book's ALL-CAPS soulmeld headings and their full description spans."""
    headers: List[Tuple[int, int, str, int]] = []
    for i, line in enumerate(lines):
        if not re.match(r"^\s*Descriptors\s*:", line, re.IGNORECASE):
            continue
        nearby: List[str] = []
        for j in range(i + 1, min(len(lines), i + 180)):
            if re.match(r"^\s*Descriptors\s*:", lines[j], re.IGNORECASE):
                break
            nearby.append(lines[j].strip())
        if (not any(re.match(r"^Classes\s*:", s, re.IGNORECASE) for s in nearby)
                or not any(re.match(r"^Chakra\s*:", s, re.IGNORECASE) for s in nearby)):
            continue
        fragments: List[Tuple[int, str]] = []
        for j in range(i - 1, max(-1, i - 9), -1):
            s = lines[j].strip()
            if not s or PAGE.search(s) or s.isdigit() or s in {"CHAPTER 4", "SOULMELDS"}:
                continue
            if not _caps_fragment(s):
                break
            fragments.append((j, s))
            if len(fragments) == 3:
                break
        if not fragments:
            continue
        fragments.reverse()
        raw_name = " ".join(s for _, s in fragments)
        if len(raw_name) > 72:
            continue
        headers.append((fragments[0][0], i, _title_name(raw_name), pages[i]))

    spans: Dict[str, Tuple[str, int, int, int]] = {}
    for n, (start, anchor, name, page) in enumerate(headers):
        if n + 1 < len(headers):
            end = headers[n + 1][0]
        else:
            end = len(lines)
            for j in range(anchor + 1, len(lines)):
                m = PAGE.search(lines[j])
                if m and int(m.group(1)) > page:
                    end = j
                    break
        spans[_norm_name(name)] = (name, start, end, page)
    return spans


def detect_soulmelds(lines: List[str], pages: List[int], book: str) -> List[Soulmeld]:
    start = next((i for i in range(len(lines)) if _is_real_table_header(lines, i)), None)
    if start is None:
        return []
    end = next((i for i in range(start + 1, len(lines)) if FOOTNOTE_END.match(lines[i])),
               min(len(lines), start + 900))

    merged: Dict[str, Soulmeld] = {}

    def record(name: str, effect: Optional[str], cls: Optional[str],
               chakra: Optional[str], idx: int) -> None:
        name = name.strip(" .,")
        if len(name) < 3 or not re.search(r"[A-Za-z]", name):
            return
        key = name.lower()
        sm = merged.get(key)
        if sm is None:
            sm = Soulmeld(name=name, book=book, page=pages[idx], start=idx, end=idx + 1)
            merged[key] = sm
        if effect and not sm.basic_effect:
            sm.basic_effect = effect
        if cls and cls not in sm.classes:
            sm.classes.append(cls)
        if chakra and chakra not in sm.chakras:
            sm.chakras.append(chakra)

    cur_class: Optional[str] = None
    cur_chakra: Optional[str] = None
    pend_name: Optional[str] = None
    pend_idx = 0
    pend_effect: List[str] = []

    def flush(*_) -> None:
        nonlocal pend_name, pend_effect
        if pend_name is not None:
            record(pend_name, " ".join(pend_effect).strip() or None,
                   cur_class, cur_chakra, pend_idx)
        pend_name, pend_effect = None, []

    for i in range(start, end):
        s = lines[i].strip()
        mt = TABLE.search(s)
        if mt:
            flush(True)
            cur_class = mt.group(1).capitalize()
            cur_chakra = None
            continue
        if s == "":
            flush()                                 # blank ends a table row
            continue
        if (PAGE.search(lines[i]) or COLHDR.match(s) or s.isdigit()
                or NOTE.match(s) or s.isupper() or DESC_FIELD.match(s)):
            continue
        first = s.split()[0].rstrip("*\u2020†")
        # "Totem" is not a column-1 section header here (per the table footnote),
        # so a leading "Totem" is part of a name ("Totem Avatar"), not a chakra —
        # excluding it avoids splitting that soulmeld and cascading a spurious
        # Totem chakra onto later rows.
        rest = s[len(s.split()[0]):].strip()
        if (first in CHAKRAS and first != "Totem"
                and (not rest or _name_ok(rest))):
            # A chakra header may share a line with a name ("Shoulders Adamant
            # Pauldrons"), but "Heart of Fire" is itself a soulmeld name.
            flush(True)
            cur_chakra = first
            if not rest:
                continue
            s = rest                                # chakra header shared a line with a name
        # classify: a name (optionally with an inline effect) starts a new entry;
        # anything else is an effect line for the current entry.
        nm_try, eff_try = _split_same_line(s)
        if _name_ok(nm_try) and (eff_try is not None or _name_ok(s)):
            flush()
            pend_name, pend_idx = nm_try, i
            pend_effect = [eff_try] if eff_try else []
        elif pend_name is not None:
            pend_effect.append(s)                   # effect (or wrapped continuation)
    flush()

    details = _description_spans(lines, pages)
    for sm in merged.values():
        detail = details.get(_norm_name(sm.name))
        if detail:
            _, sm.start, sm.end, sm.page = detail
        sm.classes.sort(key=lambda c: ("Incarnate", "Soulborn", "Totemist").index(c)
                        if c in ("Incarnate", "Soulborn", "Totemist") else 9)
        sm.chakras.sort(key=lambda c: CHAKRAS.index(c) if c in CHAKRAS else 99)
    return sorted(merged.values(), key=lambda s: s.name)


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[Soulmeld]]] = {
    "soulmelds": detect_soulmelds,
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
    soulmelds: List[Soulmeld] = field(default_factory=list)


SOURCES: List[Source] = [
    Source("incarnum", "Magic of Incarnum",
           Path("D&D 3.5e/Player Options/Magic of Incarnum.md"),
           "Magic of Incarnum (WotC, 3.5e), soulmeld tables and descriptions pp. 54–94",
           "soulmelds"),
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
            src.soulmelds = DETECTORS[src.detector](src.lines, pages, src.book)
            src.coverage = f"ok — {len(src.soulmelds)} soulmelds from {path.name}"

    def all_soulmelds(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for sm in src.soulmelds:
                yield src, sm

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, sm in self.all_soulmelds(book):
            nm = sm.name.lower()
            if nm == q:
                exact.append((src, sm))
            elif q in nm:
                partial.append((src, sm))
        return exact if exact else partial


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# SOULMELD INDEX — The New Path",
        "",
        "**Generated by `scripts/soulmeld_harvest.py`. Do not hand-edit; rerun the",
        "harvest.** D&D 3.5 incarnum soulmelds (the meldshaper's shaped soul-items),",
        "from Magic of Incarnum. `classes` are the incarnum classes that can shape",
        "the soulmeld; `chakras` are the body slots it can bind to for greater",
        "effect. `basic_effect` is the unbound effect; the essentia-scaling and",
        "chakra-bind effects are in the full description (PDF page). Native 3.5e.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.soulmelds)
        parsed_well += sum(1 for s in src.soulmelds if s.quick_fields() >= 3)
        sources_out.append({"key": src.key, "book": src.book, "citation": src.citation,
                            "coverage": src.coverage, "source_path": str(src.path),
                            "soulmelds": [asdict(s) for s in src.soulmelds]})
        md.append(f"## {src.book} — {len(src.soulmelds)} soulmelds")
        md.append("")
        md.append(f"*Source: {src.citation}.*")
        md.append(f"*Extraction: `{corpus.base / src.path}`.*")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.soulmelds:
            md.append("| Soulmeld | Classes | Chakras | Basic Effect | PDF p. |")
            md.append("|---|---|---|---|---|")
            for s in src.soulmelds:
                md.append(f"| {s.name} | {', '.join(s.classes) or '—'} | "
                          f"{', '.join(s.chakras) or '—'} | {s.basic_effect or '—'} | "
                          f"{s.page if s.page is not None else '—'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/soulmeld_harvest.py",
                    "corpus": str(corpus.base), "total_soulmelds": total,
                    "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 8:
        print(f"'{name}' matches {len(hits)} soulmelds; narrow with the exact name:")
        for src, sm in hits[:20]:
            print(f"  {sm.name}   [{sm.book}, p.{sm.page}]")
        return 1
    packets = []
    for src, sm in hits:
        packets.append({
            "packet": "soulmeld-for-translation",
            "instructions": ("A D&D 3.5 incarnum soulmeld (meldshaper subsystem). "
                             "The 3.5e half is here (basic effect, classes, bindable "
                             "chakras); the system-translator builds the GURPS side. "
                             "The essentia-scaling and per-chakra bind effects are in "
                             "the full soulmeld description at the cited PDF page."),
            "name": sm.name,
            "source": {"book": sm.book, "pdf_page": sm.page,
                       "extraction": str(corpus.base / src.path),
                       "citation": src.citation},
            "parsed": {k: v for k, v in asdict(sm).items()
                       if k in ("basic_effect", "classes", "chakras") and v},
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


FIXTURE = """## [PDF page 54]
Table 4–1: Incarnate Soulmelds
Chakra
Soulmeld
Basic Effect*
Crown
Crystal Helm
+2 resistance bonus on Will saves against charm and compulsion
Necrocarnum Circlet
Detect undead within 30 feet
Feet
Airstep Sandals
Fly up to 10 feet as a move action
Table 4–3: Totemist Soulmelds
Chakra*
Soulmeld
Basic Effect**
Crown
Beast Tamer Circlet
+2 bonus on Handle Animal and wild empathy checks
Threefold Mask of the Chimera Can’t be flanked
Feet
Airstep Sandals
Fly up to 10 feet as a move action
Waist
Heart of Fire
+1 bonus on attack and damage against cold creatures
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    lines = FIXTURE.splitlines()
    melds = detect_soulmelds(lines, _pages_for(lines), "Magic of Incarnum")
    by = {m.name: m for m in melds}
    if "Crystal Helm" not in by or by["Crystal Helm"].classes != ["Incarnate"]:
        failures.append(f"Crystal Helm missing/mislabeled: {by.get('Crystal Helm')}")
    # Airstep Sandals appears in two class tables → merged, two classes
    air = by.get("Airstep Sandals")
    if not air or set(air.classes) != {"Incarnate", "Totemist"}:
        failures.append(f"Airstep Sandals classes {air.classes if air else None}, "
                        f"wanted Incarnate+Totemist merged")
    elif air.chakras != ["Feet"]:
        failures.append(f"Airstep Sandals chakras {air.chakras}, wanted ['Feet']")
    # same-line name+effect split
    tm = by.get("Threefold Mask of the Chimera")
    if not tm:
        failures.append(f"Threefold Mask not split from its effect; names={sorted(by)}")
    elif tm.basic_effect and "flanked" not in tm.basic_effect:
        failures.append(f"Threefold Mask effect {tm.basic_effect!r}")
    hof = by.get("Heart of Fire")
    if (not hof or hof.classes != ["Totemist"] or hof.chakras != ["Waist"]
            or hof.basic_effect != "+1 bonus on attack and damage against cold creatures"):
        failures.append(f"Heart of Fire name/chakra split failed: {hof}")

    if base.is_dir() and (base / SOURCES[0].path).exists():
        corpus = Corpus(base, _fresh_sources())
        src = corpus.sources[0]
        melds = src.soulmelds
        pages = _pages_for(src.lines)
        details = _description_spans(src.lines, pages)
        if len(melds) != 89:
            failures.append(f"{len(melds)} soulmelds indexed; expected exactly 89")
        if len(details) != 89:
            failures.append(f"{len(details)} full description headings; expected exactly 89")
        classes = {c for m in melds for c in m.classes}
        if classes != {"Incarnate", "Soulborn", "Totemist"}:
            failures.append(f"classes seen {classes}, wanted all three")
        missing_spans = [m.name for m in melds if _norm_name(m.name) not in details]
        if missing_spans:
            failures.append(f"soulmelds without description spans: {missing_spans}")
        bad_spans = []
        for m in melds:
            head = " ".join(src.lines[m.start:min(m.end, m.start + 8)])
            if m.end - m.start < 8 or _norm_name(m.name) not in _norm_name(head):
                bad_spans.append((m.name, m.start, m.end))
        if bad_spans:
            failures.append(f"invalid full description spans: {bad_spans[:5]}")
        if not melds or min(m.page or 0 for m in melds) != 54 or max(m.page or 0 for m in melds) != 94:
            failures.append("live description pages did not span the verified PDF pages 54–94")
        hearts = corpus.find("heart of fire", book="incarnum")
        heart = hearts[0][1] if hearts else None
        if (not heart or heart.page != 70 or heart.classes != ["Totemist"]
                or heart.chakras != ["Waist"]
                or heart.basic_effect != "+1 bonus on attack and damage against cold creatures"):
            failures.append(f"live Heart of Fire mismatch: {heart}")
        for waist_name in ("Lamia Belt", "Manticore Belt", "Phoenix Belt", "Wormtail Belt"):
            hits = corpus.find(waist_name, book="incarnum")
            waist = hits[0][1] if hits else None
            if not waist or waist.chakras != ["Waist"]:
                failures.append(f"{waist_name} chakra mismatch: {waist}")
        iw = corpus.find("incarnate weapon", book="incarnum")
        if not iw:
            failures.append("Incarnate Weapon not found in live index")
    else:
        print("  [SKIP] Magic of Incarnum extraction not found — fixture checks only")

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
        found = sorted({(sm.name, ", ".join(sm.classes), ", ".join(sm.chakras), sm.page or -1)
                        for _, sm in corpus.all_soulmelds(args.book) if q in sm.name.lower()})
        for nm, cls, ch, page in found:
            print(f"  {nm}  [{cls}; chakras {ch}; PDF p.{page}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.soulmelds for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.soulmelds):4d} soulmelds" if src.soulmelds else "   0 soulmelds"
        print(f"  {src.book:28s} {status}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} D&D 3.5 soulmelds; {parsed_well} with 3+ fields parsed.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
