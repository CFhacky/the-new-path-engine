#!/usr/bin/env python3
r"""Harvest D&D 3.5e shadow-magic fundamentals and mysteries from Tome of Magic.

This is a native D&D 3.5e subsystem family, deliberately separate from spells,
pact-magic vestiges, and truename utterances. The detector reads the book's
born-digital description blocks only. Values absent from a printed block remain
empty; in particular, the chapter's shared standard-action rule is not copied
into each row as though it were a per-entry field.

Outputs:
    reference/mystery_index.json
    reference/mystery_index.md

Governing source:
    I:\Sourcebooks\_text\D&D 3.5e\Player Options\Tome of Magic.md
    Shadow Magic mystery descriptions, PDF pages 142-154. Five exact floating
    illustration blocks are excluded from export/Codex delivery only after
    same-page verification; the entry prose remains untouched.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CORPUS = Path(r"I:\Sourcebooks\_text")
REPO = Path(__file__).resolve().parent.parent
OUT_JSON = REPO / "reference" / "mystery_index.json"
OUT_MD = REPO / "reference" / "mystery_index.md"

PAGE = re.compile(r"\[PDF page (\d+)\]")
FIELD_LABELS = {
    "levelschool": "level_school",
    "castingtime": "casting_time",
    "range": "range",
    "target": "target",
    "targets": "target",
    "area": "area",
    "effect": "effect",
    "duration": "duration",
    "savingthrow": "saving_throw",
    "spellresistance": "spell_resistance",
}
LIGATURES = str.maketrans({
    "\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl",
    "\ufb03": "ffi", "\ufb04": "ffl",
})


@dataclass
class Mystery:
    name: str
    book: str
    page: Optional[int]
    start: int
    end: int
    category: str
    path: Optional[str]
    level: Optional[int]
    school: Optional[str]
    level_school: Optional[str]
    casting_time: Optional[str]
    range: Optional[str]
    target: Optional[str]
    area: Optional[str]
    effect: Optional[str]
    duration: Optional[str]
    saving_throw: Optional[str]
    spell_resistance: Optional[str]

    def populated_core_fields(self) -> int:
        values = (
            self.category, self.level_school, self.casting_time, self.range,
            self.target or self.area or self.effect, self.duration,
            self.saving_throw, self.spell_resistance,
        )
        return sum(value not in (None, "") for value in values)


def _plain(text: str) -> str:
    """Normalize text-layer typography only; never supply a missing value."""
    text = text.translate(LIGATURES)
    text = re.sub(r"\bRefl\s+ex\b", "Reflex", text, flags=re.IGNORECASE)
    text = re.sub(r"\bRefl\s+ections\b", "Reflections", text,
                  flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", text).strip()


def _norm_name(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", _plain(text).casefold()).strip()


# These five floating illustration blocks interrupt or trail mystery descriptions
# in the source text layer. Each exact block was verified against the same PDF
# page; only the unrelated caption/artist lines are removed.
CAPTION_BLOCKS = (
    (
        "Irrin Coradran",
        "uses umbral body to become",
        "incorporeal before attacking",
        "Illus. by S. Prescott",
    ),
    (
        "By casting consume essence, Thanielle sucks the life out of her foe",
        "Illus. by C. Critchlow",
    ),
    ("Illus. by E. Cox",),
    (
        "Afraid of the dark brings forth a shadowy duplicate",
        "that attacks your enemy's will",
        "Illus. by F. Vohwinkel",
    ),
    (
        "Umbral touch turns Eveneth's hand into a deadly weapon",
        "Illus. by J. Thomas",
    ),
)


def _strip_mystery_captions(text: str) -> Tuple[str, int]:
    lines = text.splitlines()
    keys = [_norm_name(line) for line in lines]
    removed: set[int] = set()
    removed_blocks = 0
    for block in CAPTION_BLOCKS:
        wanted = [_norm_name(line) for line in block]
        hits = [
            index for index in range(0, len(keys) - len(wanted) + 1)
            if keys[index:index + len(wanted)] == wanted
        ]
        if len(hits) == 1:
            start = hits[0]
            removed.update(range(start, start + len(wanted)))
            removed_blocks += 1
    cleaned = "\n".join(
        line for index, line in enumerate(lines) if index not in removed
    ).strip()
    return cleaned, removed_blocks


def _title_name(text: str) -> str:
    words = _plain(text).title().split()
    minor = {"a", "an", "and", "of", "or", "the", "to", "into"}
    for index, word in enumerate(words):
        bare = word.strip(",")
        if index and bare.casefold() in minor:
            words[index] = word.replace(bare, bare.casefold())
    return " ".join(words)


def _pages_for(lines: List[str]) -> List[int]:
    pages: List[int] = []
    page = 0
    for line in lines:
        match = PAGE.search(line)
        if match:
            page = int(match.group(1))
        pages.append(page)
    return pages


def _next_nonblank(lines: List[str], index: int, stop: int) -> Optional[int]:
    for probe in range(index, min(stop, len(lines))):
        if lines[probe].strip() and not PAGE.search(lines[probe]):
            return probe
    return None


def _category(text: str) -> Optional[Tuple[str, Optional[str]]]:
    clean = _plain(text)
    if clean == "Fundamental":
        return "Fundamental", None
    match = re.fullmatch(r"([A-Za-z ]+),\s*(.+)", clean)
    if not match:
        return None
    category_key = re.sub(r"\s+", "", match.group(1)).casefold()
    categories = {
        "apprentice": "Apprentice",
        "initiate": "Initiate",
        "master": "Master",
    }
    category = categories.get(category_key)
    return (category, match.group(2)) if category else None


def _is_title_line(text: str) -> bool:
    clean = text.strip()
    return (
        3 <= len(clean) <= 60
        and ":" not in clean
        and any(ch.isalpha() for ch in clean)
        and clean == clean.upper()
        and not PAGE.search(clean)
    )


def _heading_at(lines: List[str], index: int,
                stop: int) -> Optional[Tuple[str, int]]:
    """Return (joined title, category-line index), including a two-line title."""
    first = lines[index].strip()
    if not _is_title_line(first):
        return None
    second_i = _next_nonblank(lines, index + 1, min(stop, index + 5))
    if second_i is None:
        return None
    if _category(lines[second_i]):
        return _title_name(first), second_i
    if _is_title_line(lines[second_i]):
        third_i = _next_nonblank(lines, second_i + 1, min(stop, second_i + 5))
        if third_i is not None and _category(lines[third_i]):
            return _title_name(first + " " + lines[second_i].strip()), third_i
    return None


def _field_at(text: str) -> Optional[Tuple[str, str]]:
    clean = _plain(text)
    match = re.match(r"^([A-Za-z /]+):\s*(.*)$", clean)
    if not match:
        return None
    key = re.sub(r"[^a-z]", "", match.group(1).casefold())
    canonical = FIELD_LABELS.get(key)
    return (canonical, match.group(2)) if canonical else None


def _join_value(parts: Iterable[str]) -> str:
    out = ""
    for raw in parts:
        part = _plain(raw)
        if not part or PAGE.search(raw) or part.isdigit():
            continue
        if not out:
            out = part
        elif out.endswith(("-", "/")):
            out += part
        else:
            out += " " + part
    return out.strip()


def _parse_fields(lines: List[str], category_line: int,
                  end: int) -> Dict[str, Optional[str]]:
    starts: List[Tuple[int, str, str]] = []
    for index in range(category_line + 1, min(end, category_line + 36)):
        found = _field_at(lines[index])
        if found:
            starts.append((index, found[0], found[1]))
    values: Dict[str, Optional[str]] = {
        value: None for value in set(FIELD_LABELS.values())
    }
    for position, (index, key, first) in enumerate(starts):
        following = starts[position + 1][0] if position + 1 < len(starts) else index + 1
        parts = [first] + lines[index + 1:following]
        if key == "level_school":
            kept = [parts[0]]
            for part in parts[1:]:
                current = _join_value(kept)
                clean = _plain(part)
                needs_more = (
                    current.endswith(("-", "/"))
                    or current.count("(") > current.count(")")
                    or current.count("[") > current.count("]")
                    or clean.startswith(("(", "["))
                )
                if not needs_more:
                    break
                kept.append(part)
            parts = kept
        value = _join_value(parts)
        values[key] = value or None
    return values


def _description_headers(lines: List[str]) -> List[Tuple[int, str, int]]:
    """Find every printed NAME / category / Level-School description heading."""
    stop = next((i for i, line in enumerate(lines)
                 if line.strip() == "SHADOW MAGIC ITEMS"), len(lines))
    headers: List[Tuple[int, str, int]] = []
    index = 0
    while index < stop:
        heading = _heading_at(lines, index, stop)
        if heading:
            name, category_line = heading
            probe_fields = _parse_fields(lines, category_line, min(stop, category_line + 36))
            if probe_fields["level_school"]:
                headers.append((index, name, category_line))
                index = category_line + 1
                continue
        index += 1
    return headers


def detect_mysteries(lines: List[str], pages: List[int],
                     book: str) -> List[Mystery]:
    headers = _description_headers(lines)
    section_end = next((i for i, line in enumerate(lines)
                        if line.strip() == "SHADOW MAGIC ITEMS"
                        and (not headers or i > headers[-1][0])), len(lines))
    rows: List[Mystery] = []
    for number, (start, name, category_line) in enumerate(headers):
        end = headers[number + 1][0] if number + 1 < len(headers) else section_end
        category, path = _category(lines[category_line]) or ("", None)
        fields = _parse_fields(lines, category_line, end)
        level_school = fields["level_school"]
        level_match = re.match(r"(\d+)(?:st|nd|rd|th)?\s*/\s*(.+)",
                               level_school or "", flags=re.IGNORECASE)
        level = int(level_match.group(1)) if level_match else None
        school = level_match.group(2).strip() if level_match else None
        rows.append(Mystery(
            name=name, book=book, page=pages[start] or None,
            start=start, end=end, category=category, path=path,
            level=level, school=school, **fields,
        ))
    return sorted(rows, key=lambda row: (row.category, row.path or "", row.level or -1,
                                         row.name))


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[Mystery]]] = {
    "mysteries": detect_mysteries,
}


@dataclass
class Source:
    key: str
    book: str
    path: Path
    citation: str
    detector: str
    system: str = "D&D 3.5e"
    coverage: str = "pending"
    lines: List[str] = field(default_factory=list)
    mysteries: List[Mystery] = field(default_factory=list)


SOURCES = [
    Source(
        "tome",
        "Tome of Magic (Shadow Magic)",
        Path("D&D 3.5e/Player Options/Tome of Magic.md"),
        "Tome of Magic (WotC, 3.5e), Shadow Magic mystery descriptions, PDF pp. 142-154",
        "mysteries",
    ),
]


def _fresh_sources() -> List[Source]:
    return [
        Source(source.key, source.book, source.path, source.citation,
               source.detector, source.system)
        for source in SOURCES
    ]


class Corpus:
    def __init__(self, base: Path, sources: List[Source]):
        self.base = base
        self.sources = sources
        for source in self.sources:
            path = base / source.path
            if not path.exists():
                source.coverage = f"NO COVERAGE — extraction missing: {path}"
                continue
            source.lines = path.read_text(
                encoding="utf-8", errors="replace").splitlines()
            source.mysteries = DETECTORS[source.detector](
                source.lines, _pages_for(source.lines), source.book)
            source.coverage = (
                f"ok — {len(source.mysteries)} fundamentals/mysteries "
                f"from {path.name}"
            )

    def all_mysteries(self, book: Optional[str] = None):
        for source in self.sources:
            if book and book.casefold() not in (
                    source.key.casefold(), source.book.casefold()):
                continue
            for mystery in source.mysteries:
                yield source, mystery

    def find(self, query: str, book: Optional[str] = None):
        sought = _norm_name(query)
        exact, partial = [], []
        for source, mystery in self.all_mysteries(book):
            name = _norm_name(mystery.name)
            if name == sought:
                exact.append((source, mystery))
            elif sought in name:
                partial.append((source, mystery))
        return exact or partial


def _field_coverage(rows: List[Mystery]) -> Dict[str, Dict[str, object]]:
    accessors = {
        "level_school": lambda row: row.level_school,
        "casting_time": lambda row: row.casting_time,
        "range": lambda row: row.range,
        "target_area_effect": lambda row: row.target or row.area or row.effect,
        "duration": lambda row: row.duration,
        "saving_throw": lambda row: row.saving_throw,
        "spell_resistance": lambda row: row.spell_resistance,
    }
    return {
        name: {
            "populated": sum(bool(getter(row)) for row in rows),
            "total": len(rows),
            "no_coverage": [row.name for row in rows if not getter(row)],
        }
        for name, getter in accessors.items()
    }


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    sources_out = []
    markdown = [
        "# SHADOW MYSTERY INDEX — The New Path",
        "",
        "**Generated by scripts/mystery_harvest.py. Do not hand-edit; rerun the harvest.**",
        "Native D&D 3.5e shadow-magic fundamentals and path mysteries from Tome of",
        "Magic. Null fields mean the individual printed description did not include",
        "that field; shared chapter defaults are not silently copied into rows.",
        "",
    ]
    for source in corpus.sources:
        total += len(source.mysteries)
        field_coverage = _field_coverage(source.mysteries)
        caption_cleanup = {
            "source_illustrator_lines": sum(
                "\n".join(source.lines[row.start:row.end]).count("Illus. by")
                for row in source.mysteries
            ),
            "excluded_blocks": sum(
                _strip_mystery_captions(
                    "\n".join(source.lines[row.start:row.end])
                )[1]
                for row in source.mysteries
            ),
            "policy": (
                "Five exact, same-PDF illustration blocks are excluded from "
                "export and Codex full text; description prose is retained."
            ),
        }
        sources_out.append({
            "key": source.key,
            "book": source.book,
            "system": source.system,
            "citation": source.citation,
            "coverage": source.coverage,
            "source_path": str(source.path),
            "field_coverage": field_coverage,
            "caption_cleanup": caption_cleanup,
            "mysteries": [asdict(mystery) for mystery in source.mysteries],
        })
        summary = "; ".join(
            f"{name} {detail['populated']}/{detail['total']}"
            for name, detail in field_coverage.items()
        )
        markdown.extend([
            f"## {source.book} — {len(source.mysteries)} entries",
            "",
            f"*System: {source.system}. Source: {source.citation}.*",
            f"*Extraction: {corpus.base / source.path}.*",
            f"*Harvest: {source.coverage}.*",
            f"*Caption cleanup: {caption_cleanup['excluded_blocks']} exact floating "
            "illustration blocks excluded; entry prose retained.*",
            f"*Printed-field coverage: {summary}.*",
            "*NO COVERAGE values are fields omitted by the individual printed block; "
            "shared chapter defaults and referenced-spell fields are not imputed.*",
            "",
            "| Mystery | Category | Path | Level / school and descriptors | Range | Target / area / effect | Duration | Save | Resistance | PDF p. |",
            "|---|---|---|---|---|---|---|---|---|---|",
        ])
        for mystery in source.mysteries:
            subject = mystery.target or mystery.area or mystery.effect or "—"
            markdown.append(
                f"| {mystery.name} | {mystery.category} | {mystery.path or '—'} | "
                f"{mystery.level_school or '—'} | {mystery.range or '—'} | "
                f"{subject} | {mystery.duration or '—'} | "
                f"{mystery.saving_throw or '—'} | {mystery.spell_resistance or '—'} | "
                f"{mystery.page or '—'} |"
            )
        markdown.append("")
    payload = {
        "generated_by": "scripts/mystery_harvest.py",
        "corpus": str(corpus.base),
        "total_mysteries": total,
        "sources": sources_out,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=1), encoding="utf-8")
    OUT_MD.write_text("\n".join(markdown), encoding="utf-8")
    populated = sum(mystery.populated_core_fields()
                    for _, mystery in corpus.all_mysteries())
    return total, populated


def _raw_block(source: Source, mystery: Mystery) -> str:
    body: List[str] = []
    skip_printed_page = False
    for line in source.lines[mystery.start:mystery.end]:
        if PAGE.search(line):
            skip_printed_page = True
            continue
        if skip_printed_page and line.strip().isdigit():
            skip_printed_page = False
            continue
        if line.strip():
            skip_printed_page = False
        body.append(line)
    cleaned, _ = _strip_mystery_captions("\n".join(body))
    return cleaned


def export_packet(corpus: Corpus, name: str, book: Optional[str],
                  out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 8:
        print(f"'{name}' matches {len(hits)} mysteries; use the exact name.")
        return 1
    packets = []
    for source, mystery in hits:
        parsed = asdict(mystery)
        for key in ("book", "page", "start", "end"):
            parsed.pop(key, None)
        packets.append({
            "packet": "shadow-mystery-for-translation",
            "instructions": (
                "Native D&D 3.5e shadow magic. Preserve its category/path and "
                "do not coerce it into the standard spell family."
            ),
            "name": mystery.name,
            "source": {
                "book": mystery.book,
                "pdf_page": mystery.page,
                "citation": source.citation,
                "extraction": str(corpus.base / source.path),
                "lines": [mystery.start + 1, mystery.end],
            },
            "parsed": {key: value for key, value in parsed.items()
                       if value not in (None, "")},
            "raw_block": _raw_block(source, mystery),
        })
    rendered = json.dumps(packets[0] if len(packets) == 1 else packets, indent=1)
    if out:
        out.write_text(rendered, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(rendered)
    return 0


FIXTURE = """## [PDF page 142]
AFRAID OF THE DARK
Apprentice, Umbral Mind
Level/School: 3rd/Illusion (Mind-Affecting, Shadow)
Range: Medium (100 ft. + 10 ft./level)
Target: One living creature
Duration: Instantaneous
Saving Throw: Will half
Spell Resistance: Yes
Description.
ARMY OF SHADOW
Master, Shadow Calling
Le vel/School: 9th/Conjuration
(Summoning)
Ra nge: Close (25 ft. + 5 ft./2 levels)
Ef fect: One or more summoned
creatures, no two of which are more than 30 ft. apart
Du ration: 1 minute/
level (D)
Sa ving Throw: None
Sp ell Resistance: No
Description.
## [PDF page 149]
REFLECTIONS OF THINGS
TO COME
Master, Eyes of the Night Sky
Level/School: 9th/Divination
Range: Personal
Target: You
Duration: 10 minutes/level or until discharged
Description.
SHADOW MAGIC ITEMS
"""


EXPECTED_NAMES = {
    "Afraid of the Dark", "Army of Shadow", "Arrow of Dusk", "Aura of Shade",
    "Bend Perspective", "Black Candle", "Black Fire", "Bolster",
    "Carpet of Shadow", "Caul of Shadow", "Clinging Darkness",
    "Congress of Shadows", "Consume Essence", "Curtain of Shadows",
    "Dancing Shadows", "Dark Air or Water", "Dark Soul", "Dusk and Dawn",
    "Echo Spell", "Ephemeral Image", "Ephemeral Storm", "Far Sight",
    "Feign Life", "Flesh Fails", "Flesh Fails, Greater", "Flicker",
    "Flood of Shadow", "Killing Shadows", "Languor", "Life Fades",
    "Life Fades, Greater", "Liquid Night", "Mesmerizing Shade",
    "Mystic Reflections", "Pass into Shadow", "Piercing Sight",
    "Prison of Night", "Reflections of Things to Come", "Shadow Evocation",
    "Shadow Evocation, Greater", "Shadow Hood", "Shadow Investiture",
    "Shadow Plague", "Shadow Skin", "Shadow Storm", "Shadow Surge",
    "Shadow Time", "Shadow Vision", "Shadows Fade", "Shadows Fade, Greater",
    "Sharp Shadows", "Sight Eclipsed", "Sight Obscured", "Soul Puppet",
    "Steel Shadows", "Step into Shadow", "Summon Umbral Servant",
    "Thoughts of Shadow", "Tomb of Night", "Truth Revealed", "Umbral Body",
    "Umbral Hand", "Umbral Touch", "Unravel Dweomer", "Unveil", "Voice of Shadow",
    "Voyage into Shadow", "Warp Spell", "Widened Eyes",
}


def selftest(base: Path) -> int:
    failures: List[str] = []
    fixture_lines = FIXTURE.splitlines()
    fixture = detect_mysteries(
        fixture_lines, _pages_for(fixture_lines), "Tome of Magic")
    fixture_by_name = {row.name: row for row in fixture}
    if set(fixture_by_name) != {
            "Afraid of the Dark", "Army of Shadow",
            "Reflections of Things to Come"}:
        failures.append(f"fixture names: {sorted(fixture_by_name)}")
    army = fixture_by_name.get("Army of Shadow")
    if not army or (
            army.level, army.school, army.effect, army.duration,
            army.saving_throw, army.spell_resistance
    ) != (
            9, "Conjuration (Summoning)",
            "One or more summoned creatures, no two of which are more than 30 ft. apart",
            "1 minute/level (D)", "None", "No"):
        failures.append(f"wrapped Army of Shadow fields: {army}")
    reflection = fixture_by_name.get("Reflections of Things to Come")
    if not reflection or reflection.page != 149 or reflection.category != "Master":
        failures.append(f"wrapped Reflections heading: {reflection}")
    caption_fixture = """ARROW OF DUSK
Actual description prose.
Afraid of the dark brings forth a shadowy duplicate
that attacks your enemy's will
Illus. by F. Vohwinkel"""
    caption_cleaned, caption_count = _strip_mystery_captions(caption_fixture)
    if (caption_count != 1 or "Actual description prose." not in caption_cleaned
            or "Afraid of the dark" in caption_cleaned
            or "Illus. by" in caption_cleaned):
        failures.append(
            f"caption fixture cleanup count={caption_count}: {caption_cleaned!r}")

    source_path = base / SOURCES[0].path
    if base.is_dir() and source_path.exists():
        corpus = Corpus(base, _fresh_sources())
        source = corpus.sources[0]
        rows = source.mysteries
        by_name = {row.name: row for row in rows}
        if len(rows) != 69 or len(by_name) != 69:
            failures.append(f"{len(rows)} rows / {len(by_name)} unique; expected 69")
        if set(by_name) != EXPECTED_NAMES:
            failures.append(
                f"name roster mismatch; missing={sorted(EXPECTED_NAMES - set(by_name))}, "
                f"extra={sorted(set(by_name) - EXPECTED_NAMES)}")
        category_counts = {
            category: sum(row.category == category for row in rows)
            for category in ("Fundamental", "Apprentice", "Initiate", "Master")
        }
        if category_counts != {
                "Fundamental": 9, "Apprentice": 21,
                "Initiate": 21, "Master": 18}:
            failures.append(f"category counts: {category_counts}")
        if any(row.category != "Fundamental" and not row.path for row in rows):
            failures.append("one or more path mysteries lack a path")
        if any(row.level is None or not row.school for row in rows):
            failures.append("one or more rows lack printed level/school")
        bad_spans = []
        for row in rows:
            head = " ".join(source.lines[row.start:min(row.end, row.start + 4)])
            if (row.end <= row.start or row.end > len(source.lines)
                    or _norm_name(row.name) not in _norm_name(head)):
                bad_spans.append((row.name, row.start, row.end))
        if bad_spans:
            failures.append(f"invalid description spans: {bad_spans[:5]}")
        raw_illustrator_lines = 0
        removed_caption_blocks = 0
        caption_leaks = []
        caption_phrases = {
            _norm_name(line) for block in CAPTION_BLOCKS for line in block
        }
        for row in rows:
            raw = "\n".join(source.lines[row.start:row.end])
            raw_illustrator_lines += raw.count("Illus. by")
            cleaned, removed = _strip_mystery_captions(raw)
            removed_caption_blocks += removed
            cleaned_key = _norm_name(cleaned)
            if ("Illus. by" in cleaned
                    or any(phrase and phrase in cleaned_key
                           for phrase in caption_phrases)):
                caption_leaks.append(row.name)
        if raw_illustrator_lines != 5:
            failures.append(
                f"raw mystery spans contain {raw_illustrator_lines} illustrator "
                "lines; expected the five source-verified floating captions")
        if removed_caption_blocks != 5 or caption_leaks:
            failures.append(
                f"caption cleanup removed {removed_caption_blocks}/5 blocks; "
                f"leaks={caption_leaks}")
        preserved_prose = {
            "Voice of Shadow": "This mystery functions like the spell command.",
            "Dusk and Dawn": "By drawing shade from the Plane of Shadow",
            "Shadow Skin": "damage reduction according to your caster level",
            "Arrow of Dusk": "triple the damage.",
            "Widened Eyes": "four times as far as a human",
        }
        missing_prose = []
        for name, phrase in preserved_prose.items():
            row = by_name[name]
            cleaned, _ = _strip_mystery_captions(
                "\n".join(source.lines[row.start:row.end])
            )
            if phrase not in cleaned:
                missing_prose.append(name)
        if missing_prose:
            failures.append(
                f"caption cleanup removed required entry prose: {missing_prose}")
        pages = {row.page for row in rows}
        if min(pages) != 142 or max(pages) != 154:
            failures.append(f"PDF page range {min(pages)}-{max(pages)}, wanted 142-154")
        exact = {
            "Army of Shadow": (142, 9, "Conjuration (Summoning)",
                               "1 minute/level (D)"),
            "Shadow Hood": (149, 0, "Evocation", "1 round/level (D)"),
            "Warp Spell": (154, 4, "Abjuration", "Instantaneous"),
            "Widened Eyes": (154, 1, "Divination", "10 minutes/level (D)"),
        }
        for name, wanted in exact.items():
            row = by_name.get(name)
            got = ((row.page, row.level, row.school, row.duration)
                   if row else None)
            if got != wanted:
                failures.append(f"{name}: {got}, wanted {wanted}")
        coverage = {
            name: detail["populated"]
            for name, detail in _field_coverage(rows).items()
        }
        expected_coverage = {
            "level_school": 69, "casting_time": 0, "range": 61,
            "target_area_effect": 62, "duration": 63,
            "saving_throw": 50, "spell_resistance": 50,
        }
        if coverage != expected_coverage:
            failures.append(f"printed-field coverage {coverage}, wanted {expected_coverage}")
        if any("\ufffd" in json.dumps(asdict(row), ensure_ascii=False)
               for row in rows):
            failures.append("accepted row metadata contains U+FFFD")
    else:
        print("  [SKIP] Tome of Magic extraction not found — fixture checks only")

    for failure in failures:
        print(f"SELFTEST FAIL: {failure}")
    print("selftest: " + ("PASS" if not failures
                          else f"{len(failures)} failure(s)"))
    return 0 if not failures else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--corpus", type=Path, default=CORPUS)
    parser.add_argument("--search", metavar="TEXT")
    parser.add_argument("--book")
    parser.add_argument("--export", metavar="NAME")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()

    if args.selftest:
        return selftest(args.corpus)
    corpus = Corpus(args.corpus, _fresh_sources())
    if args.search:
        matches = [
            mystery for _, mystery in corpus.all_mysteries(args.book)
            if _norm_name(args.search) in _norm_name(mystery.name)
        ]
        for mystery in matches:
            print(
                f"  {mystery.name} [{mystery.category}"
                f"{', ' + mystery.path if mystery.path else ''}; "
                f"level {mystery.level}; PDF p.{mystery.page}]"
            )
        print(f"{len(matches)} match(es).")
        return 0 if matches else 1
    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(source.mysteries for source in corpus.sources)
    for source in corpus.sources:
        print(f"  {source.book:35} {len(source.mysteries):3d} entries "
              f"[{source.coverage.split(' — ')[0]}]")
        if source.coverage.startswith("NO COVERAGE"):
            print(f"NO COVERAGE: {source.book} ({source.coverage})")
        elif source.mysteries:
            for name, detail in _field_coverage(source.mysteries).items():
                if detail["populated"] < detail["total"]:
                    print(
                        f"NO COVERAGE: {name} "
                        f"({detail['populated']}/{detail['total']} printed blocks; "
                        "empty rows left blank)"
                    )
    if not any_ok:
        print("Nothing harvested — refusing to write empty reference files.")
        return 1
    total, populated = write_index(corpus)
    print(f"\n{total} D&D 3.5e shadow fundamentals/mysteries; "
          f"{populated} populated core fields.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
