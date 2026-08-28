#!/usr/bin/env python3
"""gurps3e_item_harvest.py — collate GURPS *3rd-edition* MAGIC ITEMS.

THE PROCESS (Chad, 2026-08-28, completing the GURPS 3e shelf in EDITION): this
is a D&D 3.5e / GURPS 4e hybrid campaign, but the project WELCOMES other editions
so long as they are kept in their OWN clearly-labeled index — the translator tools
convert them. GURPS 3e creatures and spells already have their indexes
(gurps3e_creature_index / gurps3e_spell_index); this finishes the edition with the
MAGIC ITEMS, from the three GURPS Magic Items books. Every row is stamped
`system = "GURPS 3e"`.

    reference/gurps3e_item_index.json — every GURPS 3e magic item: name, book, PDF
                                        page, line span, system tag, and the item
                                        block (asking price, component spells [the
                                        prerequisite enchantments], suggested
                                        setting, energy cost to create)
    reference/gurps3e_item_index.md   — the same index for human eyes

The raw text stays on I:\\Sourcebooks; `--export` emits a TRANSLATOR-READY packet
(verbatim block + provenance + parsed fields). The GURPS-3e half is native; the
system-translator skill builds the paired D&D 3.5e (and 4e) treatments.

WORKFLOW
    python gurps3e_item_harvest.py                    # (re)build the index
    python gurps3e_item_harvest.py --search "sword"   # find candidates
    python gurps3e_item_harvest.py --export "Demon Armor"
    python gurps3e_item_harvest.py --selftest

GOVERNING SOURCES  (I:\\Sourcebooks\\_text\\GURPS\\GURPS 3E\\)
    Unlike D&D magic items (a labeled Price/Body Slot/Aura stat block), a GURPS 3e
    magic item is written as PROSE with a two-line FOOTER: a `Component Spells:`
    line (the prerequisite enchantments) followed by an `Asking Price:` line (the
    $ cost). Magic Items 3 adds a `Suggested Setting:` line, and "Energy cost to
    create" appears inline in some entries. The RELIABLE ANCHOR is the terminal
    `Asking Price:` line — 316/425/135 of them across the three books.

    The item NAME is a short Title-Case line at the TOP of the block. It is found
    by scanning DOWN from the previous item's Asking Price to the FIRST plausible
    name, which skips the running headers, section headers ("Thieving Items"),
    chapter titles, and section-intro prose that sit between items. A garbage-name
    filter (in the spirit of item_harvest.py / gurps_creature_harvest.py) REJECTS
    those: ALL-CAPS headers, category headers ("... Items/Weapons/Spells", bare
    "Armor"/"Jewelry"/...), field/prose lines, spell-class leaks ("Regular;
    Resisted by IQ"), OCR fragments, and — the workhorse — any Title-Case line that
    carries a lowercase NON-connective word (a sure sign of a prose sentence, since
    real item names are Title Case with only of/the/and/'s lowercase). A
    multi-Asking-Price item (price variants) keeps its first, named block; the
    unnamed variant blocks are dropped rather than guessed.

    Magic Items 1 is a born-digital text-layer extraction (clean); Magic Items 2/3
    are OCR / reflowed text, so a handful of glyph-mangled names survive verbatim
    (book RAW only — never "corrected"). The PDFs stand behind every extraction; no
    cross-imports (the detector logic is duplicated here on purpose).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
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
OUT_JSON = REPO / "reference" / "gurps3e_item_index.json"
OUT_MD = REPO / "reference" / "gurps3e_item_index.md"
SYSTEM = "GURPS 3e"

PAGE = re.compile(r"\[PDF page (\d+)\]")

# --- The GURPS Magic Items footer grammar -----------------------------------
# The terminal anchor: "Asking Price: <value>". A COLON is required — that keeps
# the sidebar sentence "Asking Price is the suggested value computed by ..."
# (which explains pricing, and is not an item) from being read as an anchor. The
# OCR "Asking Price :$ 10,000." with a stray space before the colon still matches.
ASKING = re.compile(r"^Asking Price\s*:", re.IGNORECASE)
ASKING_VAL = re.compile(r"^Asking Price\s*:\s*(.+?)\s*$", re.IGNORECASE)
# A parsed price must LOOK like a price (a $ figure, or one of the book's
# non-numeric prices) — a value that reads as prose means the anchor was a
# mis-detected sentence, and the "item" is dropped.
PRICE_SHAPE = re.compile(
    r"^\s*(?:[\$£€]|\d|—|-|Varies|Variable|Various|Unimaginable|"
    r"Special|Free|Priceless|Negotiable|See\b|Not\b|None|Typically|About|Roughly|"
    r"At least|Some\b|Nil|Depends|Never|Unknown|Whatever|Anywhere|Up to|Cost)",
    re.IGNORECASE)
COMPONENT = re.compile(r"^Component Spells?\s*[:.]\s*(.+)$", re.IGNORECASE)
SETTING = re.compile(r"^Suggested Setting\s*[:.]\s*(.+)$", re.IGNORECASE)
ENERGY = re.compile(r"Energy cost to create\s*[:.]?\s*([0-9][\d,]*)", re.IGNORECASE)

# Any labeled field line (a value continuation stops when it hits one of these).
FIELD_LINE = re.compile(
    r"^(Component Spells?|Asking Price|Suggested Setting|Statistics|"
    r"Prerequisites?|Energy cost|Base Cost|Cost to make|Legality|Time to make|"
    r"Mana|Variant|Note|Item)\s*[:.]", re.IGNORECASE)

# --- Garbage-name filter -----------------------------------------------------
# Words that may appear lowercase inside a real Title-Case item name (connectives
# and the possessive/foreign particles). ANY OTHER lowercase word marks the line
# as a prose sentence, not a name.
CONNECT = set("of the a an and or nor but to for in on at with by from o l d de la "
              "le du des von van der und e y da di del della".split())
# A leading word that starts a sentence (real item names do not begin this way).
LEAD_REJECT = set("These Those This There When While With However Although Because "
                  "Though Since Unlike Despite Whether During Each Every Both Either "
                  "Neither Most Many Some Any Its It He She They We You If As At So "
                  "Then Thus Here Now Also And But Or For Nor Yet".split())
# Words that, at the END of a line, mark it as a wrapped sentence fragment.
FUNC_TAIL = set("the a an of and or nor but for to with in on at by as is are was "
                "were be been being that this his her hers its their they them from "
                "into off over under also any each some many most such these those "
                "one two three no not will would can could may might must up out "
                "about which who whom whose than then when while".split())
# Bare category / section-header words that pass the Title-Case shape test.
# These are matched EXACTLY (a bare header word), so a real modified name —
# "Hidden Swords", "Slayer Sword", "Winged Boots" — is unaffected.
CATEGORY = set(["Jewelry", "Clothing", "Armor", "Weapons", "Weaponry", "Shields",
                "Potions", "Wands", "Staves", "Staffs", "Rings", "Amulets",
                "Talismans", "Elixirs", "Miscellaneous", "Introduction",
                "Powerstones", "Scrolls", "Books", "Tools", "Vehicles", "Relics",
                "Thrones", "Golems", "Contents", "Credits", "Swords", "Blades",
                "Bows", "Arrows", "Axes", "Rods", "Cloaks", "Boots", "Helmets",
                "Gloves", "Robes", "Belts", "Pipes", "Drums", "Horns"])
# Exact structural headers / table labels that pass the Title-Case shape test but
# are NOT items — each captured a neighbouring item's footer (belt-and-braces, in
# the spirit of item_harvest.py's NON_ITEM set). Confirmed non-items only.
NON_ITEM = {"Enchantment", "Charmers and Soothers", "Drive Core Field Volume",
            "Other Transportation", "Miscellaneous Wizardly Tools",
            "Common Curses", "Anti-Curse Items", "Powerstone Economics"}
# Structural first-words (headers / field labels) — never an item name.
HEADER_REJECT = re.compile(
    r"^(Component|Asking|Statistics|Prerequisite|Energy|Contents|Introduction|"
    r"Chapter|Index|Appendix|Glossary|Note|Suggested|Table|Common)\b",
    re.IGNORECASE)
# Trailing punctuation that disqualifies a name (sentence/label/decoration ends).
BAD_TAIL = tuple(".,;:!?)]}>\u2014\u2013\u2212-\u201d\u201c\"'\u2019")
# Characters that never appear in a clean item name (field/table/spell-leak junk).
BAD_CHARS = set("$:;=/\\|@#[]{}<>*\u2014\u2013\u201c\u201d\u2192\u2026")
# Trailing category plurals ("... Items", "... Weapons", "... Spells").
CAT_TAIL = re.compile(r"\b(Items|Weapons|Spells|Golems|Characters|Shapes|Curses|"
                      r"Headgear)$", re.IGNORECASE)


def _title_case_ok(name: str) -> bool:
    """A real item name is Title Case: after the first word, every word is either
    capitalized, a connective (of/the/and/'s...), or a possessive/particle. A
    lowercase content word means this is a prose sentence, not a name."""
    words = name.split()
    for w in words[1:]:
        if not w:
            continue
        if w[0].isupper() or w[0].isdigit():
            continue
        wl = w.lower().strip(".,;:'\u2019\u201c\u201d\"")
        if wl in CONNECT:
            continue
        return False
    return True


def _plausible_name(s: str, freq: Counter) -> bool:
    s = s.strip()
    if not (3 <= len(s) <= 45):
        return False
    if not (s[0].isalpha() and s[0].isupper()):
        return False
    if s.endswith(BAD_TAIL):
        return False
    if s.isupper():                          # section header ("SHIELDS")
        return False
    if any(c in BAD_CHARS for c in s):       # field / table / spell-leak junk
        return False
    if HEADER_REJECT.match(s) or FIELD_LINE.match(s):
        return False
    words = s.split()
    if len(words) > 6:                       # a full sentence, not a name
        return False
    if words[0] in LEAD_REJECT:
        return False
    if words[-1].lower() in FUNC_TAIL:
        return False
    if len(words) >= 2 and len(words[-1].strip(".,")) == 1:  # OCR truncation ("Wizardly T")
        return False
    if s in CATEGORY or s in NON_ITEM or CAT_TAIL.search(s):  # category / header
        return False
    if not _title_case_ok(s):                # lowercase content word -> prose
        return False
    letters = sum(c.isalpha() for c in s)
    if letters < max(3, int(len(s) * 0.55)):
        return False
    if freq.get(s, 0) >= 3:                  # running header / footer / section
        return False
    return True


@dataclass
class Gurps3eItem:
    name: str
    book: str
    page: Optional[int]
    start: int
    end: int
    system: str = SYSTEM
    asking_price: Optional[str] = None       # the $ cost (the item's price)
    component_spells: Optional[str] = None    # prerequisite enchantments
    suggested_setting: Optional[str] = None   # Magic Items 3 field
    energy_cost: Optional[str] = None         # "Energy cost to create" (inline)

    def quick_fields(self) -> int:
        return sum(1 for v in (self.asking_price, self.component_spells,
                               self.suggested_setting, self.energy_cost) if v)


def _is_boundary(s: str, freq: Counter) -> bool:
    """A line at which a wrapping field value STOPS: another field, a plausible
    item name, or a section/running header (ALL-CAPS, a category header, or a
    '... Items/Weapons/Shapes' line). Stopping at headers keeps the reflowed
    'text only' Magic Items 3 from bleeding the next section into a price."""
    if FIELD_LINE.match(s) or _plausible_name(s, freq):
        return True
    if s.isupper() and len(s) >= 3:
        return True
    if s in CATEGORY or CAT_TAIL.search(s) or HEADER_REJECT.match(s):
        return True
    return False


def _join_value(lines: List[str], first: str, start: int, end: int,
                freq: Counter, max_cont: int = 3) -> str:
    """A field value can wrap across lines (Component Spells lists especially).
    Append following lines until a blank, a page marker, or a boundary line
    (another field, the next item name, or a section header) — never crossing
    into the next entry or the next section."""
    parts = [first.strip()]
    j, taken = start + 1, 0
    while j < end and taken < max_cont:
        # A GURPS field value ends in a period; once complete, do not append the
        # prose that follows it (the reflowed Magic Items 3 puts a sentence right
        # after the price on the next line).
        if parts[-1].endswith((".", "!", "?")):
            break
        raw = lines[j]
        s = raw.strip()
        if s == "" or PAGE.search(raw) or _is_boundary(s, freq):
            break
        parts.append(s)
        taken += 1
        j += 1
    return re.sub(r"\s+", " ", " ".join(parts)).strip()


def parse_fields(item: Gurps3eItem, lines: List[str], name_idx: int,
                 price_idx: int, freq: Counter) -> None:
    block_end = min(len(lines), price_idx + 4)
    # Component Spells / Suggested Setting / Energy cost live between name & price.
    for j in range(name_idx + 1, price_idx):
        s = lines[j].strip()
        if not s:
            continue
        if item.component_spells is None:
            m = COMPONENT.match(s)
            if m:
                item.component_spells = _join_value(lines, m.group(1), j,
                                                    price_idx, freq)
                continue
        if item.suggested_setting is None:
            m = SETTING.match(s)
            if m:
                item.suggested_setting = _join_value(lines, m.group(1), j,
                                                     price_idx, freq, max_cont=1)
                continue
        if item.energy_cost is None:
            m = ENERGY.search(s)
            if m:
                item.energy_cost = m.group(1)
    # Asking Price is the terminal anchor line (its value can wrap downward).
    m = ASKING_VAL.match(lines[price_idx].strip())
    if m and m.group(1):
        item.asking_price = _join_value(lines, m.group(1), price_idx, block_end,
                                        freq, max_cont=2)


def detect_gurps3e_items(lines: List[str], pages: List[int],
                         book: str) -> List[Gurps3eItem]:
    n = len(lines)
    freq = Counter(l.strip() for l in lines if l.strip())
    anchors = [i for i, ln in enumerate(lines) if ASKING.match(ln.strip())]
    raw: List[Gurps3eItem] = []
    for k, a in enumerate(anchors):
        lo = anchors[k - 1] if k > 0 else max(-1, a - 120)
        name_idx = None
        j = lo + 1
        while j < a:
            s = lines[j].strip()
            if s == "" or PAGE.search(lines[j]):
                j += 1
                continue
            if _plausible_name(s, freq):
                name_idx = j
                break
            j += 1
        if name_idx is None:
            continue
        item = Gurps3eItem(name=lines[name_idx].strip(), book=book,
                           page=pages[name_idx], start=name_idx,
                           end=min(n, a + 4))
        parse_fields(item, lines, name_idx, a, freq)
        # The price must read as a price; a prose value means the "Asking Price"
        # line was a mis-detected sentence, not an item's footer.
        if not (item.asking_price and PRICE_SHAPE.match(item.asking_price)):
            continue
        raw.append(item)

    # Dedup within the book: an item listed under two sections is one item. Keep
    # the richest (most parsed fields), then the earliest.
    best: Dict[str, Gurps3eItem] = {}
    for it in raw:
        key = it.name.lower()
        cur = best.get(key)
        if cur is None or it.quick_fields() > cur.quick_fields():
            best[key] = it
    return sorted(best.values(), key=lambda it: it.start)


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[Gurps3eItem]]] = {
    "gurps3e_items": detect_gurps3e_items,
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
    items: List[Gurps3eItem] = field(default_factory=list)


_G3 = "GURPS/GURPS 3E"
SOURCES: List[Source] = [
    Source(key="mi1", book="GURPS Magic Items 1 (3e)",
           path=Path(f"{_G3}/gurps 3e - magic items 1.md"),
           citation="GURPS Magic Items (SJGames, 3e), item catalog",
           detector="gurps3e_items"),
    Source(key="mi2", book="GURPS Magic Items 2 (3e)",
           path=Path(f"{_G3}/gurps 3e - magic items 2 [missing p.94-95].md"),
           citation="GURPS Magic Items 2 (SJGames, 3e), item catalog",
           detector="gurps3e_items"),
    Source(key="mi3", book="GURPS Magic Items 3 (3e)",
           path=Path(f"{_G3}/gurps 3e - magic items 3 [text only].md"),
           citation="GURPS Magic Items 3 (SJGames, 3e), item catalog",
           detector="gurps3e_items"),
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
        "# GURPS 3e MAGIC ITEM INDEX — The New Path",
        "",
        "**Generated by `scripts/gurps3e_item_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** One row per GURPS *3rd-edition* magic item — the 3e",
        "Magic Items books (prose entries with a `Component Spells:` /",
        "`Asking Price:` footer), kept SEPARATE from the D&D `magic_item_index`.",
        f"Every row is tagged `system = \"{SYSTEM}\"` so the translator tools know",
        "which edition they are reading. The raw text stays on `I:\\Sourcebooks` —",
        "use `--export \"NAME\"` for the translator-ready packet.",
        "",
        "`Component Spells` are the prerequisite enchantments needed to make the",
        "item; `Asking Price` is its market cost in $. A field left as `—` is one",
        "the entry did not carry (or the OCR did not cleanly yield), recoverable",
        "from the source PDF.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.items)
        parsed_well += sum(1 for it in src.items if it.quick_fields() >= 2)
        sources_out.append({
            "key": src.key, "book": src.book, "system": SYSTEM,
            "citation": src.citation, "coverage": src.coverage,
            "items": [asdict(it) for it in src.items],
        })
        md.append(f"## {src.book} — {len(src.items)} items")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*System: {SYSTEM}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.items:
            md.append("| Item | Asking Price | Component Spells | Setting | Page |")
            md.append("|---|---|---|---|---|")
            for it in src.items:
                comp = (it.component_spells or "—").replace("|", "/")
                if len(comp) > 48:
                    comp = comp[:45] + "..."
                price = (it.asking_price or "—").replace("|", "/")
                if len(price) > 32:
                    price = price[:29] + "..."
                setg = "yes" if it.suggested_setting else "—"
                md.append(f"| {it.name} | {price} | {comp} | {setg} | "
                          f"{it.page if it.page is not None else '—'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/gurps3e_item_harvest.py",
                    "system": SYSTEM, "corpus": str(corpus.base),
                    "total_items": total, "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str],
                  out: Optional[Path]) -> int:
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
            "packet": "gurps3e-item-for-translation",
            "instructions": (
                "A native GURPS 3rd-edition magic item. Its GURPS-3e half is here; "
                "the system-translator skill builds the paired D&D 3.5e (and GURPS "
                "4e) treatments. 'Component Spells' are the prerequisite "
                "enchantments; 'Asking Price' is the $ market cost. The raw_block is "
                "prose (Magic Items 2/3 are OCR) — check oddities against the source "
                "PDF on I:\\Sourcebooks."
            ),
            "name": it.name,
            "system": SYSTEM,
            "source": {"book": it.book, "pdf_page": it.page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [it.start + 1, it.end], "citation": src.citation},
            "parsed": {k: v for k, v in asdict(it).items()
                       if k in ("asking_price", "component_spells",
                                "suggested_setting", "energy_cost") and v},
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


# An embedded fixture exercising: a clean item, an item whose Component Spells
# list WRAPS across two lines, a price-variant (second Asking Price with no name
# between -> dropped), a section header ("Thieving Items") and a chapter title
# and a prose sentence and a spell-class leak (all rejected), and a name that is
# recovered by skipping a section-intro paragraph.
FIXTURE = """## [PDF page 25]
Animate Armor
Animate Armor is armor which can fight on its own - no wearer needed.
Both magical and nonmagical armor can be made animate.
Component Spells: Golem (variant), often Fortify and Deflect.
Asking Price: $30,000 and up.
Sun King's Armor
This is a suit of solid gold heavy plate that protects like steel.
Component Spells: Might, Lighten, Fortify, Deflect, Missile
Shield, Great Voice, Flash, Continual Light, unknown.
Asking Price: $5,000,000.

Thieving Items
5. Criminal and Law-Enforcement Magic
This section includes items useful to the discerning burglar.
Transfer Loyalty Regular; Resisted by IQ
Glass Armor
Glass Armor is transparent armor, favored by illusionists.
Item: Wand. Energy cost to create: 400.
Suggested Setting: Yrth, Technomancer.
Component Spells: Create Object.
Asking Price: $80,000, but variants exist.
Some enchanters offer a discount for bulk orders, of course.
Asking Price: $60,000 for the plain version.
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    lines = FIXTURE.splitlines()
    items = detect_gurps3e_items(lines, _pages_for(lines), "GURPS Magic Items 1 (3e)")
    names = [it.name for it in items]
    want = ["Animate Armor", "Sun King's Armor", "Glass Armor"]
    if names != want:
        failures.append(f"fixture detected {names}, wanted {want} (section header "
                        f"'Thieving Items', chapter title, prose intro, and the "
                        f"spell-class leak 'Transfer Loyalty Regular; Resisted by "
                        f"IQ' all rejected; the price-variant second Asking Price "
                        f"dropped as unnamed)")
    else:
        aa = items[0]
        if aa.asking_price != "$30,000 and up." or \
                aa.component_spells != "Golem (variant), often Fortify and Deflect.":
            failures.append(f"Animate Armor price={aa.asking_price!r} "
                            f"component={aa.component_spells!r}")
        sk = items[1]
        if sk.component_spells != ("Might, Lighten, Fortify, Deflect, Missile "
                                   "Shield, Great Voice, Flash, Continual Light, "
                                   "unknown."):
            failures.append(f"Sun King's Armor component-wrap not joined: "
                            f"{sk.component_spells!r}")
        if sk.asking_price != "$5,000,000.":
            failures.append(f"Sun King's Armor price={sk.asking_price!r}")
        gl = items[2]
        if gl.suggested_setting != "Yrth, Technomancer." or \
                gl.component_spells != "Create Object." or \
                gl.energy_cost != "400" or \
                not gl.asking_price.startswith("$80,000"):
            failures.append(f"Glass Armor fields: setting={gl.suggested_setting!r} "
                            f"component={gl.component_spells!r} energy={gl.energy_cost!r} "
                            f"price={gl.asking_price!r}")
        if any(it.system != SYSTEM for it in items):
            failures.append(f"system tag not '{SYSTEM}' on every row")

    if base.is_dir() and (base / SOURCES[0].path).exists():
        corpus = Corpus(base, _fresh_sources())
        per = {s.key: len(s.items) for s in corpus.sources}
        total = sum(per.values())
        if total < 650:
            failures.append(f"only {total} GURPS 3e items indexed across the three "
                            f"books; expected >= 650 (per-book {per})")
        for key, floor in (("mi1", 240), ("mi2", 300), ("mi3", 95)):
            if per.get(key, 0) < floor:
                failures.append(f"{key}: only {per.get(key,0)} items; expected >= {floor}")
        # known GURPS 3e magic items, with field spot-checks
        dm = corpus.find("demon armor", book="mi1")
        if not dm:
            failures.append("Demon Armor not found in live Magic Items 1")
        elif not (dm[0][1].asking_price and "50,000" in dm[0][1].asking_price):
            failures.append(f"Demon Armor price={dm[0][1].asking_price!r}, wanted $50,000")
        elif not (dm[0][1].component_spells and "Fortify" in dm[0][1].component_spells):
            failures.append(f"Demon Armor component={dm[0][1].component_spells!r}")
        for nm, bk in (("Juggernaut Armor", "mi1"), ("Seven-League Boots", "mi1"),
                       ("Chainmail Bikini", "mi2"), ("Jericho Trumpet", "mi2"),
                       ("The Magic Candle", "mi3"), ("Klein Beer", "mi3")):
            if not corpus.find(nm, book=bk):
                failures.append(f"{nm!r} not found in live {bk}")
        # a Magic Items 3 item should carry a Suggested Setting
        settings = [it for _, it in corpus.all_items("mi3") if it.suggested_setting]
        if len(settings) < 30:
            failures.append(f"only {len(settings)} Magic Items 3 items carry a "
                            f"Suggested Setting; expected >= 30")
        # most items should parse the price + at least one more field
        priced = [it for _, it in corpus.all_items() if it.asking_price]
        if len(priced) < total * 0.9:
            failures.append(f"only {len(priced)}/{total} items have a parsed asking "
                            f"price; expected >= 90%")
        well = sum(1 for _, it in corpus.all_items() if it.quick_fields() >= 2)
        if well < total * 0.6:
            failures.append(f"only {well}/{total} items parse 2+ fields; expected >= 60%")
    else:
        print("  [SKIP] GURPS 3e Magic Items extractions not found — fixture only")

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
        found = sorted({(it.name, it.book, it.page or -1, it.asking_price or "—")
                        for _, it in corpus.all_items(args.book) if q in it.name.lower()})
        for name, bk, page, price in found:
            loc = bk if page < 0 else f"{bk}, p.{page}"
            print(f"  {name}   [{price}; {loc}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.items for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.items):5d} items" if src.items else "    0 items"
        print(f"  {src.book:28s} {status}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} GURPS 3e magic items across "
          f"{sum(1 for s in corpus.sources if s.items)} book(s); "
          f"{parsed_well} with 2+ fields parsed.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
