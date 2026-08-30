#!/usr/bin/env python3
"""gurps_trait_harvest.py — collate the GURPS 4e advantage/disadvantage lists.

THE PROCESS (Chad, continuing the GURPS shelf): advantages and disadvantages are
the heart of GURPS character-building — the point-buy traits every GURPS build is
made of — and the reference layer had the GURPS spells, creatures, gear, and
modifiers but NOT the traits. The Basic Set closes with a TRAIT LISTS appendix
that tabulates every advantage and disadvantage with its type, exotic/supernatural
flag, point cost, and the book page where it's described. That appendix was OCR'd
as a vertical column-dump (each row's cells one per line), so it gets its own
detector and its own index.

    reference/gurps_trait_index.json — every advantage/disadvantage: name,
                                       category, mental/physical/social where
                                       printed, exotic/supernatural where printed,
                                       point cost, book page (Bxx/Pxx), PDF page,
                                       exact description [start, end]
    reference/gurps_trait_index.md   — the same, for human eyes

A second pass binds the locked appendix roster to the actual descriptions on
B18-B165. It handles conventional headings, wrapped headings, grouped inline
definitions, four shared pairs, and the printed Xenophilia page drift. The
roster detector also distinguishes section titles from repeated column labels.

GOVERNING SOURCE
    I:\\Sourcebooks\\_text\\GURPS\\GURPS 4e\\GURPS 4e - Basic Set - Characters.md
    — the TRAIT LISTS appendix. A trait row is a NAME line, then the columns one
    per line: M/P/Soc (mental/physical/social), X/Sup (exotic/supernatural, or a
    dash for mundane), Cost, Page. The anchor is the M/P/Soc line immediately
    followed by the X/Sup line — a signature that does not occur in prose.
    Advantage vs. disadvantage is set by the most recent ADVANTAGES /
    DISADVANTAGES section header. The description pass resolves each printed
    B-page to its source heading/inline definition and stops at the next trait or
    chapter cutover.
    I:\\Sourcebooks\\_text\\GURPS\\GURPS 4e\\GURPS 4e - Powers.md
    — the discrete New Advantages section on pp. P90-P98. A separate additive
    detector accepts only the five printed advantages absent from the Basic Set
    roster, validates each heading/cost/page, and stops at the next printed
    advantage or the MODIFIERS section. Neutralize is deliberately not duplicated:
    the Basic Set roster already owns that trait. Powers enhancements/limitations
    remain owned by terms_and_affixes.
    These are native GURPS 4e data; the PDFs stand behind every extraction.
"""
from __future__ import annotations

import argparse
import hashlib
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
OUT_JSON = REPO / "reference" / "gurps_trait_index.json"
OUT_MD = REPO / "reference" / "gurps_trait_index.md"

PAGE = re.compile(r"\[PDF page (\d+)\]")
TYPE = re.compile(r"^(M|P|Soc)(?:/(M|P|Soc)){0,2}$")            # M, P, Soc, M/P, ...
XSUP = re.compile(r"^(X|Sup|[—–\-\u2013\u2014\ufffd])$")        # exotic / super / mundane dash
BOOKPAGE = re.compile(r"^\d{1,3}$")
# GURPS trait costs come in many shapes: "25", "2/level", "-10*" (self-control),
# "Variable", "5 or 10/level", "3, 5, or 8/level", "10+", "1 to 10", "1 or
# 2/culture". Validate by shape: the word Variable/varies/*, or something that
# contains a digit and, once the cost words are stripped, only cost punctuation.
_COST_WORDS = re.compile(r"\b(or|to|per|level|culture|point|points|pts)\b", re.IGNORECASE)


def _is_cost(s: str) -> bool:
    low = s.strip().lower()
    if low in ("variable", "varies", "*"):
        return True
    if not re.search(r"\d", s):
        return False
    stripped = _COST_WORDS.sub("", low)
    return bool(re.fullmatch(r"[\d\s/+*.,\-\u2013\u2014]+", stripped))
# Column headers / rubric lines that must never be read as a trait name.
NOT_NAME = re.compile(
    r"^(TRAIT LISTS|ADVANTAGES?|DISADVANTAGES?|PERKS?|QUIRKS?|SKILLS?|Advantage|"
    r"Disadvantage|Perk|Quirk|Skill|Cost|Page|M/P/Soc.*|X/Sup|Name)\s*$")

MPS = {"M": "mental", "P": "physical", "Soc": "social"}

# The appendix page normally points to a description whose PDF page is B+2.
# Xenophilia is the one printed exception: its heading begins on B162 although
# the appendix cites B163, where the entry continues.
DESCRIPTION_PAGE_OFFSETS = {"Xenophilia": -1}
DESCRIPTION_ALIASES = {
    # The source prints one shared heading for these two roster rows.
    "Sexless": "Neutered or Sexless",
}
# These are chapter/section cutovers, not subheads inside a trait description.
# They prevent the preceding entry from absorbing unrelated general rules.
DESCRIPTION_BOUNDARIES = {
    "SIZE MODIFIER", "OTHER PHYSICAL", "AGE AND BEAUTY",
    "SOCIAL BACKGROUND", "CULTURE", "LANGUAGE", "PRIVILEGE",
    "PERKS", "MODIFIERS", "NEW ADVANTAGES", "QUIRKS", "MENTAL QUIRKS",
    "NEW DISADVANTAGES",
}
ROSTER_FIELDS = ("name", "book", "page", "category", "kind", "nature",
                 "cost", "book_page")
ROSTER_SHA256 = "bc4569f967f7fd26f5ae72812ba80599aebb206eae98a98f77f6a96d0bd1bf4a"


def _decode_type(s: str) -> str:
    return "/".join(MPS.get(p, p) for p in s.split("/"))


def _decode_xsup(s: str) -> str:
    if s == "X":
        return "exotic"
    if s == "Sup":
        return "supernatural"
    return "mundane"


@dataclass
class GurpsTrait:
    name: str
    book: str
    page: Optional[int]          # PDF page (provenance)
    start: int
    end: int
    category: str                # "advantage" | "disadvantage"
    kind: Optional[str] = None   # mental / physical / social
    nature: Optional[str] = None  # exotic / supernatural / mundane
    cost: Optional[str] = None   # point cost as printed ("25", "2/level", "-10", "varies")
    book_page: Optional[str] = None  # printed GURPS page, e.g. B34 or P90

    def quick_fields(self) -> int:
        return sum(1 for v in (self.kind, self.nature, self.cost, self.book_page) if v)


def _clean_name(s: str) -> str:
    s = s.strip().strip("*").strip()
    # collapse the leading garbage some OCR rows carry, keep the visible name
    return re.sub(r"\s{2,}", " ", s)


def detect_traits(lines: List[str], pages: List[int], book: str) -> List[GurpsTrait]:
    # The list was OCR'd as a column-dump with no blank lines between cells. Work
    # on the non-blank/non-page tokens; anchor on the M/P/Soc + X/Sup pair.
    toks = [(i, lines[i].strip()) for i in range(len(lines))
            if lines[i].strip() and not PAGE.search(lines[i])]
    out: List[GurpsTrait] = []
    category = "advantage"
    for k in range(1, len(toks) - 3):
        _, tline = toks[k]
        up = tline.upper()
        if up.startswith("DISADVANTAGE"):
            category = "disadvantage"
            continue
        # Only the plural all-caps section title changes state. Singular
        # "Advantage" is the repeated first-column label on both list sections.
        if up == "ADVANTAGES":
            category = "advantage"
            continue
        # No SKILL break: the Name/M-P-Soc/X-Sup/Cost/Page signature does not occur
        # in the Skills appendix (different columns) or in prose, so scanning past
        # them is harmless — and an early break on the main-body Skills chapter
        # would stop before the Trait Lists appendix is ever reached.
        if not (TYPE.match(tline) and XSUP.match(toks[k + 1][1])):
            continue
        i_nm, nm = toks[k - 1]
        _, cost = toks[k + 2]
        _, bpage = toks[k + 3]
        if NOT_NAME.match(nm) or not _is_cost(cost) or not BOOKPAGE.match(bpage):
            continue
        if not re.search(r"[A-Za-z]", nm):
            continue
        cat = category
        if cost.startswith(("-", "\u2013", "\u2014")):
            cat = "disadvantage"          # negative cost confirms a disadvantage
        out.append(GurpsTrait(
            name=_clean_name(nm), book=book, page=pages[i_nm], start=i_nm,
            end=toks[k + 3][0] + 1, category=cat, kind=_decode_type(tline),
            nature=_decode_xsup(toks[k + 1][1]), cost=cost, book_page=f"B{bpage}"))

    best: Dict[str, GurpsTrait] = {}
    for tr in out:
        key = (tr.category, tr.name.lower())
        cur = best.get(key)
        if cur is None or tr.quick_fields() > cur.quick_fields():
            best[key] = tr
    return sorted(best.values(), key=lambda t: t.start)


def _desc_norm(s: str) -> str:
    """Normalize layout punctuation while preserving the printed words."""
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", s.casefold())).strip()


def _description_cost_line(s: str) -> bool:
    """Recognize the line immediately below a conventional trait heading."""
    text = _desc_norm(s)
    return bool(
        (re.match(r"^\d", text) and "point" in text)
        or text in {"variable", "varies", "special"}
        or text.startswith("see ")
    )


def _description_candidates(lines: List[str], pages: List[int],
                            trait: GurpsTrait):
    """Find source-leading heading/definition candidates on the cited book page."""
    if not trait.book_page or not trait.book_page[1:].isdigit():
        return []
    target = DESCRIPTION_ALIASES.get(trait.name, trait.name)
    want = _desc_norm(target)
    pdf_page = (int(trait.book_page[1:]) + 2
                + DESCRIPTION_PAGE_OFFSETS.get(trait.name, 0))
    positions = [i for i, page in enumerate(pages) if page == pdf_page]
    if not positions:
        return []

    out = set()
    for i in range(positions[0], positions[-1] + 1):
        raw = lines[i].strip()
        if not raw:
            continue
        raw_norm = _desc_norm(raw)
        prefix = raw_norm == want or raw_norm.startswith(want + " ")
        if prefix:
            out.add((i, 1, False, True, target))
        for width in (1, 2, 3):
            got = _desc_norm(" ".join(lines[i:i + width]))
            exact = (got == want
                     or bool(re.fullmatch(
                         re.escape(want) + r"(?: [1-5]){1,3}", got)))
            if exact:
                out.add((i, width, True, False, target))
    return list(out)


def _description_score(candidate, lines: List[str]):
    """Prefer printed heading shapes over later mentions in body prose."""
    i, width, exact, _prefix, target = candidate
    raw = lines[i].strip()
    folded = raw.casefold()
    direct = folded.startswith(target.casefold())
    following = lines[i + width].strip() if i + width < len(lines) else ""
    score = 0
    if _description_cost_line(following) and (exact or direct):
        score += 1000
    if direct and folded.startswith(target.casefold() + ":"):
        score += 900
    if raw.isupper() and _desc_norm(raw) == _desc_norm(target):
        score += 800
    if exact:
        score += 700
    if direct and "(" in raw[len(target):len(target) + 20]:
        score += 650
    if direct:
        score += 400
    return score, -i, -width


def _description_cutovers(lines: List[str]) -> List[int]:
    out = []
    for i, line in enumerate(lines):
        text = line.strip()
        if text in DESCRIPTION_BOUNDARIES:
            out.append(i)
        if text == "PHYSICAL" and i + 1 < len(lines) \
                and lines[i + 1].strip() == "QUIRKS":
            out.append(i)
    return out


def attach_description_spans(lines: List[str], pages: List[int],
                             traits: List[GurpsTrait]) -> int:
    """Replace appendix-row markers with exact source description spans."""
    mapped = []
    for trait in traits:
        choices = _description_candidates(lines, pages, trait)
        if not choices:
            continue
        choice = max(choices, key=lambda c: _description_score(c, lines))
        mapped.append((trait, choice[0]))

    starts = sorted({start for _trait, start in mapped})
    boundaries = sorted(set(starts + _description_cutovers(lines) + [len(lines)]))
    attached = 0
    for trait, start in mapped:
        end = min(boundary for boundary in boundaries if boundary > start)
        if end - start < 2:
            continue
        trait.start, trait.end = start, end
        attached += 1
    return attached


def _roster_digest(traits: List[GurpsTrait]) -> str:
    payload = json.dumps(
        [[getattr(trait, field_name) for field_name in ROSTER_FIELDS]
         for trait in traits],
        ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# Printed Powers New Advantages roster. Neutralize is a section boundary only:
# the Basic Set already owns that trait, and existing rows must remain untouched.
POWERS_ADVANTAGES = {
    "Control": (90, ("Variable",), True),
    "Create": (92, ("Variable",), True),
    "Illusion": (94, ("25 points",), True),
    "Leech": (96, ("25 points for level 1 + 4", "points/additional level"), True),
    "Neutralize": (97, ("50 points",), False),
    "Static": (98, ("30 points",), True),
}


def detect_powers_traits(lines: List[str], pages: List[int],
                         book: str) -> List[GurpsTrait]:
    """Read the discrete P90-P98 New Advantages section without inference."""
    anchors: Dict[str, Tuple[int, int, str]] = {}
    for name, (printed_page, cost_lines, _accept) in POWERS_ADVANTAGES.items():
        pdf_page = printed_page + 2
        matches = []
        for i, line in enumerate(lines):
            if line.strip() != name or pages[i] != pdf_page:
                continue
            found, cursor = [], i + 1
            while cursor < len(lines) and len(found) < len(cost_lines):
                value = lines[cursor].strip()
                cursor += 1
                if value and not PAGE.search(value):
                    found.append(value)
            if tuple(found) == cost_lines:
                matches.append((i, cursor, " ".join(found)))
        if len(matches) != 1:
            return []
        anchors[name] = matches[0]

    modifier_ends = [i for i, line in enumerate(lines)
                     if line.strip() == "MODIFIERS"
                     and pages[i] == 101 and i > anchors["Static"][0]]
    if not modifier_ends:
        return []

    ordered_starts = sorted(start for start, _cursor, _cost in anchors.values())
    section_end = min(modifier_ends)
    out = []
    for name, (printed_page, _cost_lines, accept) in POWERS_ADVANTAGES.items():
        if not accept:
            continue
        start, _cursor, cost = anchors[name]
        end = next((other for other in ordered_starts if other > start), section_end)
        out.append(GurpsTrait(
            name=name, book=book, page=printed_page + 2, start=start, end=end,
            category="advantage", cost=cost, book_page=f"P{printed_page}"))
    return sorted(out, key=lambda trait: trait.start)


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[GurpsTrait]]] = {
    "traits": detect_traits,
    "powers_traits": detect_powers_traits,
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
    traits: List[GurpsTrait] = field(default_factory=list)


SOURCES: List[Source] = [
    Source("basicset", "GURPS Basic Set: Characters",
           Path("GURPS/GURPS 4e/GURPS 4e - Basic Set - Characters.md"),
           "GURPS Basic Set: Characters (SJGames, 4e), Trait Lists appendix",
           "traits"),
    Source("powers", "GURPS Powers",
           Path("GURPS/GURPS 4e/GURPS 4e - Powers.md"),
           "GURPS Powers (SJ Games, 4e), New Advantages, pp. P90-P98",
           "powers_traits"),
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
            src.traits = DETECTORS[src.detector](src.lines, pages, src.book)
            if src.detector == "traits":
                mapped = attach_description_spans(src.lines, pages, src.traits)
            else:
                mapped = len(src.traits)
            if src.detector == "powers_traits" and len(src.traits) != 5:
                src.traits = []
                src.coverage = (
                    "NO COVERAGE — Powers New Advantages roster did not yield "
                    "the five non-Basic traits cleanly")
            else:
                src.coverage = (f"ok — {len(src.traits)} traits from {path.name}; "
                                f"{mapped} exact description spans")

    def all_traits(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for tr in src.traits:
                yield src, tr

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, tr in self.all_traits(book):
            nm = tr.name.lower()
            if nm == q:
                exact.append((src, tr))
            elif q in nm:
                partial.append((src, tr))
        return exact if exact else partial


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# GURPS TRAIT INDEX — The New Path",
        "",
        "**Generated by `scripts/gurps_trait_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** Native GURPS 4e advantages and disadvantages from",
        "the Basic Set Trait Lists appendix plus Powers' five New Advantages absent",
        "from that roster. `cost` is the point cost as printed; `book_page` (Bxx",
        "or Pxx) points to the full description, and every row carries its exact",
        "source span there. A field left `—` was not printed in the source roster.",
        "Use `--export \"NAME\"` for a translator packet.",
        "",
    ]
    for src in corpus.sources:
        adv = [t for t in src.traits if t.category == "advantage"]
        dis = [t for t in src.traits if t.category == "disadvantage"]
        total += len(src.traits)
        parsed_well += sum(1 for t in src.traits if t.quick_fields() >= 3)
        sources_out.append({"key": src.key, "book": src.book, "citation": src.citation,
                            "source_path": str(src.path), "coverage": src.coverage,
                            "advantages": len(adv), "disadvantages": len(dis),
                            "traits": [asdict(t) for t in src.traits]})
        md.append(f"## {src.book} — {len(adv)} advantages, {len(dis)} disadvantages")
        md.append("")
        md.append(f"*Source: {src.citation}.*")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        for label, group in (("Advantages", adv), ("Disadvantages", dis)):
            if not group:
                continue
            md.append(f"### {label} ({len(group)})")
            md.append("")
            md.append("| Trait | Type | Nature | Cost | Book p. | PDF p. |")
            md.append("|---|---|---|---|---|---|")
            for t in group:
                md.append(f"| {t.name} | {t.kind or '—'} | {t.nature or '—'} | "
                          f"{t.cost or '—'} | {t.book_page or '—'} | "
                          f"{t.page if t.page is not None else '—'} |")
            md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/gurps_trait_harvest.py",
                    "corpus": str(corpus.base), "total_traits": total,
                    "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 8:
        print(f"'{name}' matches {len(hits)} traits; narrow with the exact name:")
        for src, tr in hits[:20]:
            print(f"  {tr.name} ({tr.category})   [{tr.book}, p.{tr.page}]")
        return 1
    packets = []
    for src, tr in hits:
        body = [ln for ln in src.lines[tr.start:tr.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "gurps-trait-for-translation",
            "instructions": ("A native GURPS 4e advantage/disadvantage. The GURPS "
                             "half is here (point-buy trait); the system-translator "
                             "skill builds the D&D 3.5e treatment (feat / template / "
                             "flaw / racial trait, as fits). The complete source "
                             "description follows verbatim with its cited book page."),
            "name": tr.name, "category": tr.category,
            "source": {"book": tr.book, "pdf_page": tr.page, "book_page": tr.book_page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [tr.start + 1, tr.end], "citation": src.citation},
            "parsed": {k: v for k, v in asdict(tr).items()
                       if k in ("category", "kind", "nature", "cost", "book_page") and v},
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


FIXTURE = """## [PDF page 300]
TRAIT LISTS
Advantage
M/P/Soc X/Sup
Cost
Page
360° Vision
P
X
25
34
Absolute Direction
P
–
5
34
Acute Hearing
P
–
2/level
35
Wealth
Soc
–
Variable
25
DISADVANTAGES
Advantage
M/P/Soc X/Sup
Cost
Page
Bad Sight
P
–
-25
123
Bloodlust
M
–
-10
125
Wealth
Soc
–
Variable
25
Unnatural Features
P
–
Variable
22
"""

DESCRIPTION_FIXTURE = """## [PDF page 32]
Police Rank: Position in a police force.
Police body.
Religious Rank: Position in a religious hierarchy.
Religious body.
PRIVILEGE
Unrelated privilege rules.
## [PDF page 36]
360° Vision 3 1
25 points
Vision body.
Absolute Direction 2/3
5 points
Direction body.
## [PDF page 37]
Acute Senses 3
2 points/level
Acute Hearing gives you a bonus to notice sounds.
Hearing body.
Acute Taste and Smell gives you a bonus.
Taste body.
Affliction 3 1
10 points/level
Affliction body.
## [PDF page 164]
Xenophilia 2
-10 points*
Xenophilia body.
162
DISADVANTAGES
QUIRKS
Unrelated quirk rules.
## [PDF page 167]
Neutered or Sexless
Shared body.
DISADVANTAGES
165
NEW DISADVANTAGES
Unrelated design rules.
"""

POWERS_FIXTURE = """## [PDF page 92]
NEW
ADVANTAGES
Control
Variable
Control body.
## [PDF page 94]
Create
Variable
Create body.
## [PDF page 96]
Illusion
25 points
Illusion body.
## [PDF page 98]
Leech
25 points for level 1 + 4
points/additional level
Leech body.
## [PDF page 99]
Neutralize
50 points
Existing Basic Set trait expansion.
## [PDF page 100]
Static
30 points
Static body.
## [PDF page 101]
BUILDING ABILITIES
99
MODIFIERS
Modifier rules.
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    lines = FIXTURE.splitlines()
    traits = detect_traits(lines, _pages_for(lines), "GURPS Basic Set: Characters")
    names = [t.name for t in traits]
    want = ["360° Vision", "Absolute Direction", "Acute Hearing", "Wealth",
            "Bad Sight", "Bloodlust", "Wealth", "Unnatural Features"]
    if names != want:
        failures.append(f"fixture detected {names}, wanted {want} "
                        f"(column headers must not be read as names)")
    else:
        v = traits[0]
        got = (v.category, v.kind, v.nature, v.cost, v.book_page)
        if got != ("advantage", "physical", "exotic", "25", "B34"):
            failures.append(f"360° Vision row {got}")
        if traits[2].cost != "2/level":
            failures.append(f"Acute Hearing cost {traits[2].cost!r}, wanted '2/level'")
        if traits[4].category != "disadvantage" or traits[4].cost != "-25":
            failures.append("Bad Sight fixture did not retain disadvantage / -25")
        if [traits[3].category, traits[6].category] != [
                "advantage", "disadvantage"]:
            failures.append("dual-category Wealth fixture was not preserved")
        if traits[7].category != "disadvantage" or traits[7].cost != "Variable":
            failures.append("singular column header reset the disadvantage section")

    desc_lines = DESCRIPTION_FIXTURE.splitlines()
    desc_traits = [
        GurpsTrait("Police Rank", "fixture", None, 0, 1, "advantage", book_page="B30"),
        GurpsTrait("Religious Rank", "fixture", None, 0, 1, "advantage", book_page="B30"),
        GurpsTrait("360° Vision", "fixture", None, 0, 1, "advantage", book_page="B34"),
        GurpsTrait("Absolute Direction", "fixture", None, 0, 1, "advantage", book_page="B34"),
        GurpsTrait("Acute Hearing", "fixture", None, 0, 1, "advantage", book_page="B35"),
        GurpsTrait("Acute Taste and Smell", "fixture", None, 0, 1,
                   "advantage", book_page="B35"),
        GurpsTrait("Affliction", "fixture", None, 0, 1, "advantage", book_page="B35"),
        GurpsTrait("Xenophilia", "fixture", None, 0, 1,
                   "disadvantage", book_page="B163"),
        GurpsTrait("Sexless", "fixture", None, 0, 1,
                   "disadvantage", book_page="B165"),
    ]
    mapped = attach_description_spans(
        desc_lines, _pages_for(desc_lines), desc_traits)
    if mapped != len(desc_traits):
        failures.append(f"description fixture mapped {mapped}/{len(desc_traits)} spans")
    else:
        by_name = {trait.name: trait for trait in desc_traits}

        def fixture_block(name: str) -> List[str]:
            trait = by_name[name]
            return desc_lines[trait.start:trait.end]

        if fixture_block("Police Rank") != [
                "Police Rank: Position in a police force.", "Police body."]:
            failures.append(f"Police Rank fixture leaked: {fixture_block('Police Rank')!r}")
        if "Absolute Direction 2/3" in fixture_block("360° Vision"):
            failures.append("360° Vision fixture crossed into Absolute Direction")
        if fixture_block("Acute Hearing") != [
                "Acute Hearing gives you a bonus to notice sounds.", "Hearing body."]:
            failures.append(f"Acute Hearing fixture leaked: {fixture_block('Acute Hearing')!r}")
        if "QUIRKS" in fixture_block("Xenophilia"):
            failures.append("Xenophilia fixture crossed its chapter cutover")
        sexless = fixture_block("Sexless")
        if not sexless or sexless[0] != "Neutered or Sexless" \
                or "NEW DISADVANTAGES" in sexless:
            failures.append(f"Sexless shared fixture span {sexless!r}")

    powers_lines = POWERS_FIXTURE.splitlines()
    powers_traits = detect_powers_traits(
        powers_lines, _pages_for(powers_lines), "GURPS Powers")
    powers_names = [trait.name for trait in powers_traits]
    expected_powers = ["Control", "Create", "Illusion", "Leech", "Static"]
    if powers_names != expected_powers:
        failures.append(
            f"Powers fixture detected {powers_names}, wanted {expected_powers}")
    else:
        powers_by_name = {trait.name: trait for trait in powers_traits}
        if powers_by_name["Control"].cost != "Variable":
            failures.append("Powers Control fixture cost drifted")
        if powers_by_name["Leech"].cost != (
                "25 points for level 1 + 4 points/additional level"):
            failures.append("Powers Leech wrapped cost was not joined exactly")
        if powers_by_name["Static"].book_page != "P98":
            failures.append("Powers Static fixture citation drifted")
        if any(trait.name == "Neutralize" for trait in powers_traits):
            failures.append("Powers duplicated Basic Set Neutralize")
        for trait in powers_traits:
            block = powers_lines[trait.start:trait.end]
            if not block or block[0] != trait.name:
                failures.append(f"Powers {trait.name} fixture span does not lead")
            if trait.name != "Static" and "MODIFIERS" in block:
                failures.append(f"Powers {trait.name} crossed into modifiers")
        static = powers_by_name["Static"]
        if "MODIFIERS" in powers_lines[static.start:static.end]:
            failures.append("Powers Static crossed into modifiers")

    if base.is_dir() and (base / SOURCES[0].path).exists():
        corpus = Corpus(base, _fresh_sources())
        source = corpus.sources[0]
        traits = source.traits
        adv = sum(1 for trait in traits if trait.category == "advantage")
        dis = sum(1 for trait in traits if trait.category == "disadvantage")
        if (len(traits), adv, dis) != (469, 266, 203):
            failures.append(
                f"live roster {(len(traits), adv, dis)}, wanted (469, 266, 203)")
        digest = _roster_digest(traits)
        if digest != ROSTER_SHA256:
            failures.append(
                f"legacy roster/mechanics digest {digest}, wanted {ROSTER_SHA256}")

        invalid = [trait.name for trait in traits
                   if not (0 <= trait.start < trait.end <= len(source.lines)
                           and trait.end - trait.start >= 2)]
        if invalid:
            failures.append(f"{len(invalid)} invalid description spans: {invalid[:8]}")

        groups: Dict[Tuple[int, int], List[str]] = {}
        for trait in traits:
            label = f"{trait.name}|{trait.category}"
            groups.setdefault((trait.start, trait.end), []).append(label)
        shared = {tuple(sorted(labels)) for labels in groups.values() if len(labels) > 1}
        expected_shared = {
            ("Neutered|disadvantage", "Sexless|disadvantage"),
            ("Reputation|advantage", "Reputation|disadvantage"),
            ("Status|advantage", "Status|disadvantage"),
            ("Wealth|advantage", "Wealth|disadvantage"),
        }
        if shared != expected_shared or len(groups) != 465:
            failures.append(
                f"shared spans {shared!r}; expected {expected_shared!r} and 465 unique")

        intervals = sorted(groups)
        overlaps = [(left, right) for left, right in zip(intervals, intervals[1:])
                    if left[1] > right[0]]
        if overlaps:
            failures.append(f"distinct description spans overlap: {overlaps[:5]}")

        bad_leads = []
        for trait in traits:
            head = _desc_norm(" ".join(
                source.lines[trait.start:min(trait.end, trait.start + 3)]))
            tokens = [word for word in _desc_norm(trait.name).split()
                      if len(word) >= 4] or _desc_norm(trait.name).split()
            if not tokens or not all(word in head for word in tokens[:2]):
                bad_leads.append(trait.name)
        if bad_leads:
            failures.append(f"description heading validation failed: {bad_leads[:8]}")

        def live_trait(name: str, category: Optional[str] = None) -> Optional[GurpsTrait]:
            return next((trait for trait in traits
                         if trait.name == name
                         and (category is None or trait.category == category)), None)

        def live_block(name: str, category: Optional[str] = None) -> str:
            trait = live_trait(name, category)
            return ("\n".join(source.lines[trait.start:trait.end])
                    if trait is not None else "")

        for name, forbidden in (
                ("Very Fat", "SIZE MODIFIER"),
                ("Appearance", "OTHER PHYSICAL"),
                ("Unnatural Features", "SOCIAL BACKGROUND"),
                ("High TL", "CULTURE"),
                ("Cultural Familiarity", "LANGUAGE"),
                ("Religious Rank", "PRIVILEGE"),
                ("Gigantism", "AGE AND BEAUTY"),
                ("Zeroed", "PERKS"),
                ("Shtick", "MODIFIERS"),
                ("Xenophilia", "QUIRKS"),
                ("Neutered", "NEW DISADVANTAGES")):
            block = live_block(name)
            if not block or forbidden in block:
                failures.append(f"{name} is missing or crossed into {forbidden}")

        if "Acute Taste and Smell" in live_block("Acute Hearing"):
            failures.append("Acute Hearing absorbed the next Acute Senses definition")
        if "Religious Rank:" in live_block("Police Rank"):
            failures.append("Police Rank absorbed the next Rank definition")
        xenophilia = live_trait("Xenophilia")
        page_map = _pages_for(source.lines)
        if xenophilia is None or page_map[xenophilia.start] != 164:
            failures.append("Xenophilia did not bind to its source-verified B162 heading")
        unnatural = live_trait("Unnatural Features", "disadvantage")
        if unnatural is None or unnatural.cost != "Variable":
            failures.append("Unnatural Features did not retain its printed disadvantage row")
        for dual_name in ("Reputation", "Wealth"):
            categories = {trait.category for trait in traits if trait.name == dual_name}
            if categories != {"advantage", "disadvantage"}:
                failures.append(f"{dual_name} dual-category rows {categories!r}")
        allies = live_block("Allies")
        if len(allies) < 10000 or "Special Limitations" not in allies:
            failures.append("Allies full description was truncated")
        cr = live_trait("Combat Reflexes")
        if cr is None or cr.cost != "15":
            failures.append("Combat Reflexes missing or cost drifted from 15")

        powers_path = base / SOURCES[1].path
        powers_source = corpus.sources[1]
        expected_powers_rows = [
            ("Control", "Variable", "P90", 92),
            ("Create", "Variable", "P92", 94),
            ("Illusion", "25 points", "P94", 96),
            ("Leech", "25 points for level 1 + 4 points/additional level",
             "P96", 98),
            ("Static", "30 points", "P98", 100),
        ]
        got_powers_rows = [
            (trait.name, trait.cost, trait.book_page, trait.page)
            for trait in powers_source.traits]
        if not powers_path.exists():
            failures.append(f"Powers extraction missing: {powers_path}")
        elif got_powers_rows != expected_powers_rows:
            failures.append(
                f"live Powers roster {got_powers_rows!r}, "
                f"wanted {expected_powers_rows!r}")
        else:
            powers_pages = _pages_for(powers_source.lines)
            for trait in powers_source.traits:
                block = powers_source.lines[trait.start:trait.end]
                if not (block and block[0].strip() == trait.name):
                    failures.append(f"live Powers {trait.name} span does not lead")
                if powers_pages[trait.start] != trait.page:
                    failures.append(f"live Powers {trait.name} PDF page drifted")
                if trait.kind is not None or trait.nature is not None:
                    failures.append(
                        f"live Powers {trait.name} inferred an unprinted type")
                if "MODIFIERS" in block:
                    failures.append(
                        f"live Powers {trait.name} crossed into modifiers")
            if any(trait.name == "Neutralize" for trait in powers_source.traits):
                failures.append("live Powers duplicated Basic Set Neutralize")
    else:
        print("  [SKIP] Basic Set extraction not found — fixture checks only")

    for failure in failures:
        print(f"SELFTEST FAIL: {failure}")
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
        found = sorted({(tr.name, tr.category, tr.cost or "—", tr.book_page or "—", tr.page or -1)
                        for _, tr in corpus.all_traits(args.book) if q in tr.name.lower()})
        for nm, cat, cost, bp, page in found:
            print(f"  {nm}  [{cat}; {cost} pts; {bp}; PDF p.{page}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.traits for s in corpus.sources)
    for src in corpus.sources:
        adv = sum(1 for t in src.traits if t.category == "advantage")
        dis = len(src.traits) - adv
        print(f"  {src.book:34s} {adv:4d} adv / {dis:3d} disadv  "
              f"[{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} GURPS traits (advantages + disadvantages); "
          f"{parsed_well} with 3+ fields parsed.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
