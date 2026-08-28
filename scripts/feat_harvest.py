#!/usr/bin/env python3
"""feat_harvest.py — collate D&D 3.5e feats into a translator-ready index.

THE PROCESS (companion to term_harvest.py, creature_harvest.py,
item_harvest.py, power_harvest.py, and maneuver_harvest.py): the engine has a
feat LOOKUP (feat_lookup.py, one feat at a time) but no feat INDEX — the
browsable, translator-ready collation the other reference families carry. This
script builds it, the same way creature_harvest.py builds the creature index
beside monster_lookup.py.

It merges the two feat sources feat_lookup.py reads and produces the COLLATION:

    reference/feat_index.json  — every feat found: name, type, prerequisite,
                                 book, PDF page, line span, parsed where clean
    reference/feat_index.md    — the same index for human eyes, by book

The bundled SRD core feats (feats_srd35.json) carry their own text; the
supplement extractions keep their raw text on I:\\Sourcebooks and are pulled on
demand. `--export` emits a TRANSLATOR-READY PACKET (verbatim block/text plus
provenance and parsed fields) for the `system-translator` skill's paired
3.5e + GURPS build.

WORKFLOW
    python feat_harvest.py                         # (re)build the index
    python feat_harvest.py --search "power"        # find candidates
    python feat_harvest.py --export "Power Attack"
        -> JSON packet -> feed to the system-translator skill
    python feat_harvest.py --selftest

GOVERNING SOURCES
    1. feats_srd35.json — the bundled SRD 3.5 core feats (Open Game Content),
       the same file feat_lookup.py ships. SRD wins on name collision.
    2. I:\\Sourcebooks\\_md\\_feats\\*.md — the supplement extractions
       (Complete series, PHB II, Tome of Battle, Races of ..., etc.), the same
       directory feat_lookup.py reads (override with --feats-dir).

    Block DETECTION is duplicated from feat_lookup.py on purpose — the repo law
    is "no cross-imports; shared logic gets duplicated or promoted
    deliberately." Every feat body anchors on a "Benefit:" line (ligatures
    normalised); the name is the nearest Title-Case short line above it,
    skipping prerequisite/[Type]/flavor lines. A missing source directory
    prints NO COVERAGE and is never improvised. See docs/HARVEST_PROGRESS.md.
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

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DEFAULT_DIR = Path(r"I:\Sourcebooks\_md\_feats")
REPO = Path(__file__).resolve().parent.parent
SRD_JSON = REPO / "scripts" / "feats_srd35.json"
OUT_JSON = REPO / "reference" / "feat_index.json"
OUT_MD = REPO / "reference" / "feat_index.md"

# ---------------------------------------------------------------------------
# Detection — duplicated from feat_lookup.py per the no-cross-imports law
# ---------------------------------------------------------------------------

ANCHOR = re.compile(r"^\s*Bene\s?fi\s?ts?\s*:")
PAGE = re.compile(r"<!-- page (\d+) -->")
TAG = re.compile(r"^\s*\[([A-Za-z ,]+)\]\s*$")
PREREQ = re.compile(r"^\s*Prerequisites?\s*:\s*(.+)$", re.IGNORECASE)
SKIP_UP = re.compile(r"^\s*(Prerequisites?\s*:|Bene\s?fi\s?ts?\s*:|"
                     r"Special\s*:|Normal\s*:|Table\s|CHAPTER|"
                     r"Feat\s+Descriptions)")

LIGATURES = (("\ufb01", "fi"), ("\ufb02", "fl"), ("\ufb00", "ff"),
             ("\ufb03", "ffi"), ("\ufb04", "ffl"))


def plausible_feat_name(s: str) -> bool:
    s = s.strip()
    if not s or len(s) > 42 or len(s) < 4:
        return False
    if s.endswith((".", ",", ":", ";")) or SKIP_UP.match(s) or TAG.match(s):
        return False
    # A mid-name colon means a stat/field line was grabbed, not a feat name
    # ("Level: 12th", "Special Requirement: Knowledge").
    if ":" in s:
        return False
    # An NPC descriptor ("Kobold, 1st level"), not a feat.
    if re.search(r"\d(?:st|nd|rd|th)\s+level", s, re.IGNORECASE):
        return False
    words = [w for w in re.split(r"[\s\u2013-]+", s) if w]
    if not words or not words[0][:1].isupper():
        return False
    caps = sum(1 for w in words if w[:1].isupper())
    return caps >= max(1, (len(words) * 3) // 5)


@dataclass
class Feat:
    name: str
    book: str
    page: Optional[int]
    start: int  # line span in the extraction (0 for SRD entries)
    end: int
    type: Optional[str] = None          # General / Fighter / Metamagic / ...
    prerequisite: Optional[str] = None
    srd_text: Optional[str] = None      # bundled text for SRD feats; None otherwise

    def quick_fields(self) -> int:
        return sum(1 for v in (self.type, self.prerequisite) if v)


def _prereq_in(lines: List[str]) -> Optional[str]:
    for ln in lines:
        m = PREREQ.match(ln)
        if m:
            return re.sub(r"\s+", " ", m.group(1)).strip()
    return None


def index_book(path: Path) -> Tuple[List[str], List[Feat]]:
    book = path.stem
    raw = path.read_text(encoding="utf-8", errors="replace")
    for lig, plain in LIGATURES:
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
        # Some books append the [Type] tag to the name line itself
        # ("IRONSKIN CHANT [BARDIC MUSIC]") rather than a line of its own;
        # split it off so the name is clean and the type is captured.
        nm = lines[name_at].strip()
        # OCR mangles the tag's brackets: the opener reads "[" or "|", the
        # closer any of "] | } )". The opener set excludes "(" on purpose so
        # parenthetical feat names ("Armor Proficiency (Heavy)") are NOT split.
        # A feat may carry more than one trailing tag ("[Divine] [Epic]"); peel
        # them all, left to right, into the type.
        inline_tags: List[str] = []
        while True:
            im = re.match(r"^(.*?\S)\s*[\[|]\s*([A-Za-z][A-Za-z ,/]*?)\s*[\]|})]+\s*$", nm)
            if not im:
                break
            inline_tags.insert(0, im.group(2).strip())
            nm = im.group(1).strip()
        if inline_tags and not tag:
            tag = ", ".join(inline_tags)
        starts.append((name_at, nm, tag))

    starts.sort()
    feats: List[Feat] = []
    for k, (s, name, tag) in enumerate(starts):
        e = starts[k + 1][0] if k + 1 < len(starts) else min(len(lines), s + 120)
        e = min(e, s + 120)
        feat = Feat(name=name, book=book, page=pages[s], start=s, end=e,
                    type=tag or None, prerequisite=_prereq_in(lines[s:e]))
        feats.append(feat)
    return lines, feats


# ---------------------------------------------------------------------------
# SRD source (bundled JSON — Open Game Content)
# ---------------------------------------------------------------------------

_SRD_PREREQ = re.compile(r"\*{0,2}Prerequisites?\*{0,2}\s*:?\s*(.+?)(?:\n|\*\*Benefit)",
                         re.IGNORECASE | re.DOTALL)


def load_srd(path: Path) -> List[Feat]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    feats: List[Feat] = []
    for entry in data.values():
        text = entry.get("text", "")
        m = _SRD_PREREQ.search(text)
        prereq = re.sub(r"\s+", " ", m.group(1)).strip() if m else None
        if prereq:  # drop the closing "**" of the markdown "**Prerequisite:**"
            prereq = prereq.lstrip("* ").strip() or None
        feats.append(Feat(name=entry["name"], book="SRD 3.5", page=None,
                          start=0, end=0, type=entry.get("type") or None,
                          prerequisite=prereq, srd_text=text))
    return feats


# ---------------------------------------------------------------------------
# Corpus
# ---------------------------------------------------------------------------


class Corpus:
    def __init__(self, feats_dir: Path, srd_path: Path = SRD_JSON):
        # SRD first so it wins name collisions when searching.
        self.books: Dict[str, Tuple[Optional[List[str]], List[Feat]]] = {}
        srd = load_srd(srd_path)
        if srd:
            self.books["SRD 3.5"] = (None, srd)
        self.dir_present = feats_dir.is_dir()
        if self.dir_present:
            for path in sorted(feats_dir.glob("*.md")):
                self.books[path.stem] = index_book(path)

    def all_feats(self, book: Optional[str] = None):
        for name, (lines, feats) in self.books.items():
            if book and book.lower() != name.lower():
                continue
            for f in feats:
                yield lines, f

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for lines, f in self.all_feats(book):
            n = f.name.lower()
            if n == q:
                exact.append((lines, f))
            elif q in n:
                partial.append((lines, f))
        return exact if exact else partial


# ---------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with_prereq = 0
    books_out = []
    md: List[str] = [
        "# FEAT INDEX — The New Path",
        "",
        "**Generated by `scripts/feat_harvest.py`. Do not hand-edit; rerun the",
        "harvest.** One row per feat: the bundled SRD 3.5 core feats plus every",
        "feat found in the supplement extractions under `_md\\_feats\\`. The",
        "supplement raw text stays on `I:\\Sourcebooks` — use `python",
        "scripts/feat_harvest.py --export \"NAME\"` to emit the translator-ready",
        "packet for any row, then hand it to the system-translator skill for",
        "the paired 3.5e + GURPS build.",
        "",
        "Every entry names its book; supplement entries carry the PDF page the",
        "extraction recorded (SRD entries are Open Game Content, no page). A",
        "field left as `—` is one the OCR did not cleanly yield.",
        "",
    ]
    for book, (lines, feats) in corpus.books.items():
        total += len(feats)
        with_prereq += sum(1 for f in feats if f.prerequisite)
        books_out.append({"book": book, "feats": [
            {k: v for k, v in asdict(f).items() if k != "srd_text"} for f in feats]})
        md.append(f"## {book} — {len(feats)} feats")
        md.append("")
        md.append("| Feat | Type | Prerequisite | Page |")
        md.append("|---|---|---|---|")
        for f in feats:
            prereq = (f.prerequisite or "—").replace("|", "/")
            if len(prereq) > 70:
                prereq = prereq[:67] + "..."
            md.append(f"| {f.name} | {f.type or '—'} | {prereq} | "
                      f"{f.page if f.page is not None else '—'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps(
            {
                "generated_by": "scripts/feat_harvest.py",
                "srd_json": str(SRD_JSON),
                "feats_dir": str(DEFAULT_DIR),
                "total_feats": total,
                "books": books_out,
            },
            indent=1,
        ),
        encoding="utf-8",
    )
    return total, with_prereq


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 6:
        print(f"'{name}' matches {len(hits)} feats; narrow with --book or the exact name:")
        for _, f in hits[:20]:
            print(f"  {f.name}   [{f.book}{'' if f.page is None else ', p.' + str(f.page)}]")
        return 1
    packets = []
    for lines, f in hits:
        if f.srd_text is not None:
            raw = f.srd_text
        else:
            body = [ln for ln in lines[f.start:f.end] if not PAGE.search(ln)]
            raw = re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip()
        packets.append({
            "packet": "feat-for-translation",
            "instructions": (
                "Feed this packet to the system-translator skill. Both a 3.5e "
                "AND a GURPS treatment are required in the output — a conversion "
                "missing either system is incomplete (that skill's own rule). "
                "The raw_block is OCR text (SRD entries are clean OGC); check "
                "oddities against the source PDF on I:\\Sourcebooks."
            ),
            "name": f.name,
            "source": {
                "book": f.book, "pdf_page": f.page,
                "extraction": None if f.srd_text is not None else str(DEFAULT_DIR / (f.book + ".md")),
                "lines": None if f.srd_text is not None else [f.start + 1, f.end],
            },
            "parsed": {k: v for k, v in asdict(f).items()
                       if k in ("type", "prerequisite") and v},
            "raw_block": raw,
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


# ---------------------------------------------------------------------------
# Selftest — detection against an embedded fixture, then live corpus checks
# ---------------------------------------------------------------------------

FIXTURE = """<!-- page 96 -->
POWER LUNGE
[Fighter]
Prerequisite: Str 13, Power Attack
Benefit: As a full-round action, you may make a single melee
attack dealing double Strength bonus damage.

Normal: You deal normal Strength bonus damage.

WHIRLING STEEL STRIKE
[Fighter]
Prerequisite: Weapon Focus (longsword), Combat Expertise
Benefit: You may use your longsword to make attacks of
opportunity as if it were a light weapon.
"""


def selftest(feats_dir: Path) -> int:
    failures: List[str] = []

    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "Fixture_Book.md").write_text(FIXTURE, encoding="utf-8")
        lines, feats = index_book(d / "Fixture_Book.md")
        names = [f.name for f in feats]
        if names != ["POWER LUNGE", "WHIRLING STEEL STRIKE"]:
            failures.append(f"fixture detected {names}, wanted the two feats")
        else:
            pl = feats[0]
            if pl.type != "Fighter" or pl.prerequisite != "Str 13, Power Attack" \
                    or pl.page != 96:
                failures.append(f"Power Lunge type={pl.type!r} prereq={pl.prerequisite!r} "
                                f"page={pl.page}, wanted Fighter / Str 13, Power Attack / 96")

    srd = load_srd(SRD_JSON)
    if not srd:
        print(f"  [SKIP] SRD feats JSON not found: {SRD_JSON}")
    else:
        if len(srd) < 100:
            failures.append(f"only {len(srd)} SRD feats loaded; expected >= 100")
        pa = next((f for f in srd if f.name.lower() == "power attack"), None)
        if pa is None:
            failures.append("Power Attack missing from SRD feats")

    if feats_dir.is_dir():
        corpus = Corpus(feats_dir)
        total = sum(len(v[1]) for v in corpus.books.values())
        if len(corpus.books) < 9:
            failures.append(f"only {len(corpus.books)} books indexed; expected >= 9 (SRD + 8)")
        if total < 500:
            failures.append(f"only {total} feats indexed; expected > 500")
        aa = corpus.find("power attack")
        if not aa:
            failures.append("Power Attack not resolvable in merged corpus")
    else:
        print(f"  [SKIP] supplement dir not found: {feats_dir} — fixture + SRD only")

    for failure in failures:
        print(f"SELFTEST FAIL: {failure}")
    print("selftest: " + ("PASS" if not failures else f"{len(failures)} failure(s)"))
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--feats-dir", type=Path, default=DEFAULT_DIR)
    ap.add_argument("--search", metavar="TEXT", help="substring search on indexed names")
    ap.add_argument("--book", help="restrict to one book (e.g. 'SRD 3.5', Complete_Warrior)")
    ap.add_argument("--export", metavar="NAME", help="emit a translator-ready packet")
    ap.add_argument("--out", type=Path, help="write the packet here instead of stdout")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest(args.feats_dir)

    corpus = Corpus(args.feats_dir)
    if not corpus.books:
        print("NO COVERAGE — no SRD feats JSON and no supplement extractions found.",
              file=sys.stderr)
        return 2
    if not corpus.dir_present:
        print(f"NO COVERAGE — supplement dir missing: {args.feats_dir} "
              f"(SRD feats still indexed)", file=sys.stderr)

    if args.search:
        q = args.search.lower()
        found = sorted({(f.name, f.book, f.page if f.page is not None else -1)
                        for _, f in corpus.all_feats(args.book) if q in f.name.lower()})
        for name, book, page in found:
            loc = book if page < 0 else f"{book}, p.{page}"
            print(f"  {name}   [{loc}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    total, with_prereq = write_index(corpus)
    for book, (_, feats) in corpus.books.items():
        print(f"  {book:26s} {len(feats):5d} feats")
    print(f"\n{total} feats across {len(corpus.books)} books; "
          f"{with_prereq} with a prerequisite parsed.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
