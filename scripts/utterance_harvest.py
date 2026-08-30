#!/usr/bin/env python3
r"""Harvest D&D 3.5 truename utterances from Tome of Magic.

This is a native D&D 3.5e family, separate from spells, mysteries, and
recitation feats. The book's three summary rosters supply lexicon, level, and
short printed effect summaries. The detail blocks supply the entry fields and
true heading-to-heading source spans used by the Codex.

Governing source:
  I:\Sourcebooks\_text\D&D 3.5e\Player Options\Tome of Magic.md
  Tome of Magic, Truename Magic, printed pp. 232-253.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CORPUS = Path(r"I:\Sourcebooks\_text")
REPO = Path(__file__).resolve().parent.parent
OUT_JSON = REPO / "reference" / "utterance_index.json"
OUT_MD = REPO / "reference" / "utterance_index.md"

PAGE = re.compile(r"\[PDF page (\d+)\]")
LEVEL_HEADER = re.compile(r"^([1-6])(?:ST|ND|RD|TH)-LEVEL UTTERANCES$")
FIELD_KEYS = {
    "range": "range", "target": "target", "area": "area",
    "duration": "duration", "savingthrow": "saving_throw",
}
LIGATURES = str.maketrans({
    "\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl",
    "\ufb03": "ffi", "\ufb04": "ffl",
})
DETAIL_ALIASES = {
    "master of the four winds": "master the four winds",
}
DETAIL_NAMES = {
    "master the four winds": "Master the Four Winds",
}

LEXICONS = (
    ("evolving_mind", "EVOLVING MIND", 6, True),
    ("crafted_tool", "CRAFTED TOOL", 5, False),
    ("perfected_map", "PERFECTED MAP", 4, False),
)
DC_RULES = {
    "evolving_mind": "15 + (2 × target creature's CR); use Hit Dice for a PC",
    "crafted_tool": (
        "magic object: 15 + (2 × item's caster level); "
        "nonmagical object: DC 25"
    ),
    "perfected_map": None,
}
DC_GAP = (
    "NO COVERAGE: Tome of Magic states no separate base Truespeak DC "
    "for Lexicon of the Perfected Map utterances."
)


@dataclass
class Utterance:
    name: str
    system: str
    book: str
    page: Optional[int]
    pdf_page: Optional[int]
    start: int
    end: int
    lexicon: str
    level: int
    reversible: bool
    truespeak_dc: Optional[str]
    range: Optional[str] = None
    target: Optional[str] = None
    area: Optional[str] = None
    duration: Optional[str] = None
    saving_throw: Optional[str] = None
    spell_resistance: str = "Applies"
    normal_summary: Optional[str] = None
    reverse_summary: Optional[str] = None
    effect_summary: Optional[str] = None
    summary_name: Optional[str] = None
    range_basis: Optional[str] = None
    target_basis: Optional[str] = None
    area_basis: Optional[str] = None
    dc_coverage: Optional[str] = None


@dataclass
class Source:
    key: str
    book: str
    path: Path
    citation: str
    coverage: str = "pending"
    lines: List[str] = field(default_factory=list)
    utterances: List[Utterance] = field(default_factory=list)
    no_coverage: List[str] = field(default_factory=list)


SOURCES = [
    Source(
        "tome",
        "Tome of Magic (Truename Magic)",
        Path("D&D 3.5e/Player Options/Tome of Magic.md"),
        "Tome of Magic (WotC, D&D 3.5e), Truename Magic pp. 232-253",
    )
]


def _norm(text: str) -> str:
    text = text.translate(LIGATURES).replace("\u2019", "'")
    return re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip()


def _join_wrapped(parts: Iterable[str]) -> str:
    out = ""
    for raw in parts:
        text = raw.strip()
        if not text or PAGE.search(text) or re.fullmatch(r"\d{1,3}", text):
            continue
        if out.endswith("-"):
            out = out[:-1] + text
        else:
            out = (out + " " + text).strip()
    return out


def _find_pair(lines: List[str], first: str, second: str, start: int = 0) -> int:
    for i in range(start, len(lines) - 1):
        if lines[i].strip() == first and lines[i + 1].strip() == second:
            return i
    raise ValueError(f"missing section heading: {first} / {second}")


def _page_maps(lines: List[str]) -> Tuple[List[int], List[int]]:
    pdf_pages: List[int] = []
    book_pages: List[int] = []
    pdf_page = 0
    book_page = 0
    after_marker = 0
    for line in lines:
        marker = PAGE.search(line)
        if marker:
            pdf_page = int(marker.group(1))
            book_page = pdf_page - 1
            after_marker = 6
        elif after_marker:
            after_marker -= 1
            if re.fullmatch(r"\d{1,3}", line.strip()):
                book_page = int(line.strip())
                after_marker = 0
        pdf_pages.append(pdf_page)
        book_pages.append(book_page)
    return pdf_pages, book_pages


def _summary_roster(
    lines: List[str], section_start: int, section_end: int
) -> Tuple[int, List[dict]]:
    first = next(
        i for i in range(section_start, section_end)
        if LEVEL_HEADER.match(lines[i].strip())
    )
    detail_start = next(
        i for i in range(first, section_end - 2)
        if lines[i].strip().isupper()
        and (
            lines[i + 1].strip().startswith("Level:")
            or (
                lines[i + 1].strip().isupper()
                and lines[i + 2].strip().startswith("Level:")
            )
        )
    )
    rows: List[dict] = []
    current: Optional[dict] = None
    level: Optional[int] = None
    for i in range(first, detail_start):
        text = lines[i].strip()
        level_match = LEVEL_HEADER.match(text)
        if level_match:
            level = int(level_match.group(1))
            current = None
            continue
        if not text or PAGE.search(text) or re.fullmatch(r"\d{1,3}", text):
            continue
        if ":" in text:
            name, rest = text.split(":", 1)
            if re.fullmatch(r"[A-Za-z\u2019' ,\-]+", name.strip()):
                current = {
                    "name": name.strip(),
                    "level": level,
                    "summary_parts": [rest],
                }
                rows.append(current)
                continue
        if current:
            current["summary_parts"].append(text)
    for row in rows:
        row["summary"] = _join_wrapped(row.pop("summary_parts"))
    return detail_start, rows


def _field_key(text: str) -> Optional[str]:
    match = re.match(r"^([^:]+):\s*(.*)$", text)
    if not match:
        return None
    compact = _norm(match.group(1)).replace(" ", "")
    return FIELD_KEYS.get(compact)


def _detail_fields(lines: List[str], level_line: int, end: int) -> Dict[str, str]:
    starts: List[Tuple[int, str, str]] = []
    for i in range(level_line, min(end, level_line + 14)):
        text = lines[i].strip()
        if re.match(r"^(Normal|Reverse):", text):
            break
        match = re.match(r"^([^:]+):\s*(.*)$", text)
        key = _field_key(text)
        if match and key:
            starts.append((i, key, match.group(2)))
    fields: Dict[str, str] = {}
    for n, (line_no, key, first_value) in enumerate(starts):
        if n + 1 < len(starts):
            next_line = starts[n + 1][0]
            value = _join_wrapped([first_value] + lines[line_no + 1:next_line])
        else:
            value = first_value.strip()
        fields[key] = value
    return fields


def _split_reversible(summary: str) -> Tuple[Optional[str], Optional[str]]:
    marker = ", or "
    if marker not in summary:
        return None, None
    normal, reverse = summary.rsplit(marker, 1)
    return normal.strip(), reverse.strip()


def _apply_defaults(row: Utterance) -> None:
    if row.lexicon in ("evolving_mind", "crafted_tool") and not row.range:
        row.range = "60 feet"
        row.range_basis = "utterance default, Tome of Magic p. 233"
    if row.lexicon == "evolving_mind" and not row.target:
        row.target = "One creature"
        row.target_basis = "lexicon rule, Tome of Magic p. 234"
    if row.lexicon == "crafted_tool" and not row.target:
        row.target = "One object"
        row.target_basis = "lexicon rule, Tome of Magic p. 248"
    if row.lexicon == "perfected_map":
        if not row.range:
            row.range = "100 feet"
            row.range_basis = "lexicon default, Tome of Magic p. 250"
        if not row.area:
            row.area = "20-foot-radius spread"
            row.area_basis = "lexicon default, Tome of Magic p. 250"


def detect_utterances(
    lines: List[str], pdf_pages: List[int], book_pages: List[int], book: str
) -> List[Utterance]:
    starts = [
        _find_pair(lines, "LEXICON OF THE", heading)
        for _, heading, _, _ in LEXICONS
    ]
    truename_spells = next(
        i for i in range(starts[-1], len(lines))
        if lines[i].strip() == "TRUENAME SPELLS"
    )
    bounds = starts[1:] + [truename_spells]
    found: List[Utterance] = []

    for (lexicon, _, max_level, reversible), section_start, section_end in zip(
        LEXICONS, starts, bounds
    ):
        detail_start, summaries = _summary_roster(
            lines, section_start, section_end
        )
        by_detail: Dict[str, dict] = {}
        for summary in summaries:
            detail_key = DETAIL_ALIASES.get(
                _norm(summary["name"]), _norm(summary["name"])
            )
            by_detail[detail_key] = summary

        headings: List[Tuple[int, int, str, dict]] = []
        seen = set()
        for i in range(detail_start, section_end - 1):
            for width in (1, 2):
                if i + width >= section_end:
                    continue
                title = " ".join(lines[j].strip() for j in range(i, i + width))
                key = _norm(title)
                if (
                    key in by_detail
                    and key not in seen
                    and re.match(r"^Level\s*:", lines[i + width].strip())
                ):
                    headings.append((i, i + width, key, by_detail[key]))
                    seen.add(key)
                    break
        headings.sort()
        if len(headings) != len(summaries):
            missing = sorted(set(by_detail) - seen)
            raise ValueError(
                f"{lexicon}: {len(summaries)} roster rows but "
                f"{len(headings)} descriptions; missing {missing}"
            )

        for n, (start, level_line, detail_key, summary) in enumerate(headings):
            end = headings[n + 1][0] if n + 1 < len(headings) else section_end
            if lexicon == "perfected_map" and n + 1 == len(headings):
                unrelated_quote = next(
                    (
                        i for i in range(start + 1, end - 1)
                        if lines[i].lstrip().startswith(("\u201c", '"'))
                        and lines[i + 1].lstrip().startswith("\u2014Utterance")
                    ),
                    None,
                )
                if unrelated_quote is not None:
                    end = unrelated_quote
            level_match = re.match(
                r"^Level:\s*(\d+)", lines[level_line].strip()
            )
            if not level_match:
                raise ValueError(f"missing detail level at source line {level_line + 1}")
            detail_level = int(level_match.group(1))
            if detail_level != summary["level"] or detail_level > max_level:
                raise ValueError(
                    f"{summary['name']}: summary level {summary['level']} "
                    f"does not match detail level {detail_level}"
                )
            name = DETAIL_NAMES.get(detail_key, summary["name"])
            fields = _detail_fields(lines, level_line, end)
            normal_summary = reverse_summary = effect_summary = None
            if reversible:
                normal_summary, reverse_summary = _split_reversible(
                    summary["summary"]
                )
            else:
                effect_summary = summary["summary"]
            row = Utterance(
                name=name,
                system="D&D 3.5e",
                book=book,
                page=book_pages[start] or None,
                pdf_page=pdf_pages[start] or None,
                start=start,
                end=end,
                lexicon=lexicon,
                level=detail_level,
                reversible=reversible,
                truespeak_dc=DC_RULES[lexicon],
                range=fields.get("range"),
                target=fields.get("target"),
                area=fields.get("area"),
                duration=fields.get("duration"),
                saving_throw=fields.get("saving_throw"),
                normal_summary=normal_summary,
                reverse_summary=reverse_summary,
                effect_summary=effect_summary,
                summary_name=(
                    summary["name"] if _norm(summary["name"]) != _norm(name) else None
                ),
                dc_coverage=DC_GAP if lexicon == "perfected_map" else None,
            )
            _apply_defaults(row)
            found.append(row)
    return sorted(found, key=lambda row: (row.lexicon, row.level, row.name))


def _fresh_sources() -> List[Source]:
    return [
        Source(src.key, src.book, src.path, src.citation)
        for src in SOURCES
    ]


class Corpus:
    def __init__(self, base: Path, sources: List[Source]):
        self.base = base
        self.sources = sources
        for src in sources:
            path = base / src.path
            if not path.exists():
                src.coverage = f"NO COVERAGE: extraction missing ({path})"
                src.no_coverage.append(src.coverage)
                continue
            src.lines = path.read_text(
                encoding="utf-8", errors="replace"
            ).splitlines()
            pdf_pages, book_pages = _page_maps(src.lines)
            src.utterances = detect_utterances(
                src.lines, pdf_pages, book_pages, src.book
            )
            src.no_coverage.append(DC_GAP)
            src.coverage = (
                f"ok - {len(src.utterances)} utterances from {path.name}; "
                "65 exact description spans"
            )

    def all_utterances(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.casefold() not in (
                src.key.casefold(), src.book.casefold()
            ):
                continue
            for row in src.utterances:
                yield src, row

    def find(self, query: str, book: Optional[str] = None):
        needle = query.strip().casefold()
        exact, partial = [], []
        for src, row in self.all_utterances(book):
            name = row.name.casefold()
            if name == needle:
                exact.append((src, row))
            elif needle in name:
                partial.append((src, row))
        return exact if exact else partial


def _mechanics() -> dict:
    return {
        "action": "standard action; provokes attacks of opportunity",
        "utter_defensively": "-5 on the Truespeak check per threatening foe",
        "save_dc": "10 + 1/2 truenamer level + Charisma modifier",
        "spell_resistance": (
            "applies; voluntarily add 5 to the Truespeak DC to overcome it"
        ),
        "law_of_resistance": (
            "+2 to the check DC after each successful use of the same utterance "
            "that day"
        ),
        "law_of_sequence": (
            "the same ongoing utterance, including its reverse, cannot be spoken "
            "again until its duration ends"
        ),
        "dc_rules": DC_RULES,
        "dc_no_coverage": DC_GAP,
    }


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    complete = 0
    sources_out = []
    md = [
        "# UTTERANCE INDEX - The New Path",
        "",
        "**Generated by scripts/utterance_harvest.py. Do not hand-edit.**",
        "Native D&D 3.5e truename utterances from Tome of Magic. This family",
        "keeps the three lexicons separate from spells, mysteries, and recitations.",
        "Effect columns reproduce the book's short summary roster; each row also",
        "carries the exact full-description source span used by the Codex.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.utterances)
        complete += sum(
            bool(row.duration and row.range and row.start < row.end)
            for row in src.utterances
        )
        sources_out.append({
            "key": src.key,
            "book": src.book,
            "citation": src.citation,
            "coverage": src.coverage,
            "source_path": str(src.path),
            "mechanics": _mechanics(),
            "no_coverage": src.no_coverage,
            "utterances": [asdict(row) for row in src.utterances],
        })
        md.extend([
            f"## {src.book} - {len(src.utterances)} utterances",
            "",
            f"*Source: {src.citation}.*",
            f"*Extraction: {corpus.base / src.path}.*",
            f"*Harvest: {src.coverage}.*",
            "",
        ])
        for lexicon, _, _, reversible in LEXICONS:
            rows = [row for row in src.utterances if row.lexicon == lexicon]
            md.extend([f"### {lexicon.replace('_', ' ').title()}", ""])
            if reversible:
                md.extend([
                    "| Utterance | Level | Normal | Reverse | Duration | Save | Page |",
                    "|---|---:|---|---|---|---|---:|",
                ])
                for row in rows:
                    md.append(
                        f"| {row.name} | {row.level} | "
                        f"{_md_cell(row.normal_summary)} | "
                        f"{_md_cell(row.reverse_summary)} | "
                        f"{_md_cell(row.duration)} | "
                        f"{_md_cell(row.saving_throw)} | {row.page or '-'} |"
                    )
            else:
                md.extend([
                    "| Utterance | Level | Printed effect | Duration | Save | Page |",
                    "|---|---:|---|---|---|---:|",
                ])
                for row in rows:
                    md.append(
                        f"| {row.name} | {row.level} | "
                        f"{_md_cell(row.effect_summary)} | "
                        f"{_md_cell(row.duration)} | "
                        f"{_md_cell(row.saving_throw)} | {row.page or '-'} |"
                    )
            md.append("")
        for gap in src.no_coverage:
            md.append(f"- {gap}")
        md.append("")

    payload = {
        "generated_by": "scripts/utterance_harvest.py",
        "corpus": str(corpus.base),
        "total_utterances": total,
        "sources": sources_out,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=1), encoding="utf-8")
    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    return total, complete


def _md_cell(value: Optional[str]) -> str:
    return (value or "-").replace("|", "\\|").replace("\n", " ")


def _raw_block(src: Source, row: Utterance) -> str:
    kept = []
    skip_folio = False
    for line in src.lines[row.start:row.end]:
        if PAGE.search(line):
            skip_folio = True
            continue
        if skip_folio and re.fullmatch(r"\d{1,3}", line.strip()):
            skip_folio = False
            continue
        if line.strip():
            skip_folio = False
        kept.append(line)
    return "\n".join(kept).strip()


def export_packet(
    corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]
) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: {name!r}. Try --search.", file=sys.stderr)
        return 1
    packets = []
    for src, row in hits:
        parsed = {
            key: value for key, value in asdict(row).items()
            if key not in ("book", "start", "end") and value is not None
        }
        packets.append({
            "packet": "utterance-for-translation",
            "instructions": (
                "Native D&D 3.5e truename utterance. Preserve lexicon, "
                "Truespeak mechanics, and normal/reversed operation."
            ),
            "name": row.name,
            "source": {
                "book": row.book,
                "page": row.page,
                "pdf_page": row.pdf_page,
                "citation": src.citation,
                "extraction": str(corpus.base / src.path),
                "lines": [row.start + 1, row.end],
            },
            "parsed": parsed,
            "raw_block": _raw_block(src, row),
        })
    text = json.dumps(packets[0] if len(packets) == 1 else packets, indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


FIXTURE = """LEXICON OF THE
EVOLVING MIND
1ST-LEVEL UTTERANCES
Knight's Puissance: Ally gains +2 on attack rolls, or enemy gains -2.
2ND-LEVEL UTTERANCES
Hidden Truth: Grant +10 on Knowledge, or grant +10 on Bluff.
KNIGHT'S
PUISSANCE
Level: 1
Duration: 5 rounds
Saving Throw: None
Normal: Ally gains +2.
Reverse: Enemy gains -2.
HIDDEN TRUTH
Level: 2
Du ration: Instantaneous (normal) or 1 round (reverse)
Saving Throw: None
Normal: Knowledge.
Reverse: Bluff.
LEXICON OF THE
CRAFTED TOOL
1ST-LEVEL UTTERANCES
Analyze Item: Discern the properties of a magic item.
ANALYZE ITEM
Level: 1
Range: Touch
Target: One object
Duration: 1 round
Description.
LEXICON OF THE
PERFECTED MAP
1ST-LEVEL UTTERANCES
Master of the Four Winds: Bend the winds to your will.
MASTER THE FOUR WINDS
Level: 1
Duration: 1 minute
Description.
TRUENAME SPELLS
"""


def selftest(base: Path) -> int:
    failures: List[str] = []
    fixture_lines = FIXTURE.splitlines()
    pdf, pages = _page_maps(fixture_lines)
    fixture = detect_utterances(
        fixture_lines, pdf, pages, "Tome of Magic (Truename Magic)"
    )
    names = [row.name for row in fixture]
    if sorted(names) != [
        "Analyze Item", "Hidden Truth", "Knight's Puissance",
        "Master the Four Winds",
    ]:
        failures.append(f"fixture names {names}")
    by_name = {row.name: row for row in fixture}
    knight = by_name.get("Knight's Puissance")
    if not knight or (knight.level, knight.normal_summary, knight.reverse_summary) != (
        1, "Ally gains +2 on attack rolls", "enemy gains -2."
    ):
        failures.append(f"split reversible fixture mismatch: {knight}")
    hidden = by_name.get("Hidden Truth")
    if not hidden or hidden.duration != (
        "Instantaneous (normal) or 1 round (reverse)"
    ):
        failures.append(f"split Duration field mismatch: {hidden}")
    master = by_name.get("Master the Four Winds")
    if not master or master.summary_name != "Master of the Four Winds":
        failures.append(f"printed name discrepancy mismatch: {master}")
    if not master or master.truespeak_dc is not None or not master.dc_coverage:
        failures.append("Perfected Map DC gap was not kept explicit")

    source_path = base / SOURCES[0].path
    if source_path.exists():
        corpus = Corpus(base, _fresh_sources())
        src = corpus.sources[0]
        rows = src.utterances
        counts = {
            lexicon: sum(row.lexicon == lexicon for row in rows)
            for lexicon, _, _, _ in LEXICONS
        }
        if len(rows) != 65:
            failures.append(f"{len(rows)} utterances indexed; expected exactly 65")
        if counts != {
            "evolving_mind": 43, "crafted_tool": 10, "perfected_map": 12
        }:
            failures.append(f"lexicon counts {counts}")
        if len({row.name for row in rows}) != len(rows):
            failures.append("duplicate accepted utterance names")
        if any(not row.duration for row in rows):
            failures.append(
                "missing durations: "
                + ", ".join(row.name for row in rows if not row.duration)
            )
        evolving = [row for row in rows if row.lexicon == "evolving_mind"]
        if any(not row.normal_summary or not row.reverse_summary for row in evolving):
            failures.append("an Evolving Mind row lacks a normal/reverse summary")
        if any(row.reverse_summary for row in rows if not row.reversible):
            failures.append("a nonreversible lexicon row gained a reverse summary")
        field_coverage = {
            key: sum(getattr(row, key) not in (None, "") for row in rows)
            for key in (
                "range", "target", "area", "duration", "saving_throw",
                "truespeak_dc", "normal_summary", "reverse_summary",
                "effect_summary",
            )
        }
        expected_coverage = {
            "range": 65, "target": 53, "area": 12, "duration": 65,
            "saving_throw": 44, "truespeak_dc": 53,
            "normal_summary": 43, "reverse_summary": 43,
            "effect_summary": 22,
        }
        if field_coverage != expected_coverage:
            failures.append(f"field coverage {field_coverage}")
        if any(row.spell_resistance != "Applies" for row in rows):
            failures.append("spell-resistance rule missing from an accepted row")
        if any(
            row.truespeak_dc is not None or row.dc_coverage != DC_GAP
            for row in rows if row.lexicon == "perfected_map"
        ):
            failures.append("Perfected Map DC gaps are not exact")
        bad_spans = []
        for row in rows:
            head = _norm(" ".join(src.lines[row.start:row.start + 2]))
            block = src.lines[row.start:row.end]
            if (
                _norm(row.name) not in head
                or not any(line.strip().startswith("Level:") for line in block[:4])
                or row.end <= row.start
            ):
                bad_spans.append((row.name, row.start, row.end))
        if bad_spans:
            failures.append(f"invalid full-description spans: {bad_spans[:5]}")
        if "\ufffd" in "\n".join(src.lines):
            failures.append("source extraction contains U+FFFD")
        live = {row.name: row for row in rows}
        hidden_live = live.get("Hidden Truth")
        if not hidden_live or hidden_live.duration != (
            "Instantaneous (normal) or 1 round (reverse)"
        ):
            failures.append(f"live Hidden Truth mismatch: {hidden_live}")
        agitate = live.get("Agitate Metal")
        if not agitate or (
            agitate.level, agitate.range, agitate.duration
        ) != (2, "30 ft.", "7 rounds"):
            failures.append(f"live Agitate Metal mismatch: {agitate}")
        shockwave = live.get("Shockwave")
        if not shockwave or shockwave.saving_throw != "Fortitude negates":
            failures.append(f"live Shockwave mismatch: {shockwave}")
        master_live = live.get("Master the Four Winds")
        if not master_live or master_live.summary_name != (
            "Master of the Four Winds"
        ):
            failures.append(f"live Master Four Winds mismatch: {master_live}")
        transform = live.get("Transform the Landscape")
        if not transform or "Utterance of hidden truth" in "\n".join(
            src.lines[transform.start:transform.end]
        ):
            failures.append("Transform the Landscape span retains the next epigraph")
        if min(row.page or 0 for row in rows) != 235 or max(
            row.page or 0 for row in rows
        ) != 253:
            failures.append("printed pages did not span verified pp. 235-253")
        if min(row.pdf_page or 0 for row in rows) != 236 or max(
            row.pdf_page or 0 for row in rows
        ) != 254:
            failures.append("PDF pages did not span verified pp. 236-254")
    else:
        print("  [SKIP] Tome of Magic extraction not found - fixture checks only")

    for failure in failures:
        print(f"SELFTEST FAIL: {failure}")
    print("selftest: " + ("PASS" if not failures else f"{len(failures)} failure(s)"))
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
        hits = corpus.find(args.search, args.book)
        for _, row in hits:
            print(
                f"  {row.name} [{row.lexicon}; level {row.level}; "
                f"Tome of Magic p.{row.page}]"
            )
        print(f"{len(hits)} match(es).")
        return 0 if hits else 1
    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    for src in corpus.sources:
        print(f"  {src.book}: {len(src.utterances)} utterances [{src.coverage}]")
        for gap in src.no_coverage:
            print(gap)
    if not any(src.utterances for src in corpus.sources):
        print("Nothing harvested - refusing to write empty reference files.")
        return 1
    total, complete = write_index(corpus)
    print(f"{total} D&D 3.5e utterances; {complete} complete indexed spans.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
