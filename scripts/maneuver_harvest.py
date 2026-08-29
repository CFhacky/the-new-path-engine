#!/usr/bin/env python3
"""maneuver_harvest.py — collate Tome of Battle maneuvers and stances.

THE PROCESS (companion to term_harvest.py, creature_harvest.py,
item_harvest.py, and power_harvest.py): the martial-adept subsystem of Tome of
Battle: Book of Nine Swords — the maneuvers and stances the Warblade, Crusader,
and Swordsage initiate — is codified in the sourcebooks and absent from the
reference layer. This script harvests it.

It walks the Tome of Battle text extraction and produces the COLLATION:

    reference/maneuver_index.json  — every maneuver / stance found: name, book,
                                     PDF page, line span, and the quick fields a
                                     triage read needs (discipline, type,
                                     descriptor, level, prerequisite, initiation
                                     action, range, duration, save), parsed
                                     where the OCR is clean
    reference/maneuver_index.md    — the same index for human eyes, by book

The raw text is deliberately NOT copied into the repository. `--export` emits a
TRANSLATOR-READY PACKET on demand: the verbatim block plus provenance and
parsed fields, for the `system-translator` skill's paired 3.5e + GURPS build.

WORKFLOW
    python maneuver_harvest.py                       # (re)build the index
    python maneuver_harvest.py --search "flame"      # find candidates
    python maneuver_harvest.py --export "Fire Riposte"
        -> JSON packet -> feed to the system-translator skill
    python maneuver_harvest.py --selftest

GOVERNING SOURCE
    I:\\Sourcebooks\\_text\\D&D 3.5e\\Player Options\\Tome of Battle
    (alt scan).md — the clean born-digital text extraction. The book's own
    maneuver-and-stance lists on PDF pages 48–51 are the court of appeal for
    canonical names, levels, disciplines, and types. The detailed entries on
    pages 52–94 follow the ToB grammar:

        FIRE RIPOSTE                             (name, ALL-CAPS, own line)
        Desert Wind (Counter) [Fire]             (discipline (Type) [Descriptor])
        Level: Swordsage 2
        Prerequisite: One Desert Wind maneuver
        Initiation Action: 1 immediate action
        Range: Personal
        Target: You
        Duration: Instantaneous
        [description]

    Detail detection anchors on the Level/Class field, walks upward through a
    possibly wrapped discipline/type line to the ALL-CAPS heading, and records
    the true heading-to-heading span. This also keeps the five book entries whose
    signature intentionally has no Boost/Counter/Stance/Strike token. Summary
    names are reconciled within their printed discipline and level, repairing
    three layout-reordered headings without guessing. The former noisy-scan
    detector remains embedded and fixture-tested as a legacy path.

    Detection is intentionally ToB-specific and self-contained. A configured
    Source whose file is missing prints NO COVERAGE and is never improvised.
    The PDFs on I:\\Sourcebooks stand behind every extraction. See
    docs/HARVEST_PROGRESS.md.
"""
from __future__ import annotations

import argparse
import difflib
import itertools
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
OUT_JSON = REPO / "reference" / "maneuver_index.json"
OUT_MD = REPO / "reference" / "maneuver_index.md"

# ---------------------------------------------------------------------------
# Field grammar (the ToB maneuver entry shape)
# ---------------------------------------------------------------------------

PAGE = re.compile(r"\[PDF page (\d+)\]")

DISCIPLINES = ("Desert Wind|Devoted Spirit|Diamond Mind|Iron Heart|Setting Sun|"
               "Shadow Hand|Stone Dragon|Tiger Claw|White Raven")
# A discipline line is a discipline word followed by END OF LINE or the start
# of a "(Type)" / "[Descriptor]" trailer — never a bare word (which would be
# prose such as "Desert Wind maneuvers focus on ..."). Chapter headers that use
# a discipline name are rejected by the Initiation-Action test below.
DISC_ANCHOR = re.compile(rf"^({DISCIPLINES})\s*($|[\[(].*)$")
DESC_RE = re.compile(r"\[([^\]]+)\]")

# The RELIABLE anchor is the "(Type)" token, not the discipline word: the OCR
# routinely corrupts the discipline ("Tron Heart", "[ron Heart", "4ton Heart"
# for Iron Heart; "Devoted Spirir"; "ert Wind"; "Dragon" for Stone Dragon) but
# leaves the short parenthesised type intact. A type line is a short line whose
# only structured content is "(Type)" plus an optional "[Descriptor]".
TYPE_LINE = re.compile(
    r"^(.{0,34}?)\(\s*(Boost|Counter|Stance|Strike)\s*\)\s*(\[[^\]]{0,32}\])?\s*.{0,4}$",
    re.IGNORECASE)

# The discipline is then recovered by keyword: each of the nine disciplines has
# a UNIQUE pair of words, and OCR rarely destroys both — "heart" alone means
# Iron Heart, "wind" Desert Wind, and so on. Exact two-word match is tried
# first, then any surviving keyword.
DISC_CANON = {
    "desert wind": "Desert Wind", "devoted spirit": "Devoted Spirit",
    "diamond mind": "Diamond Mind", "iron heart": "Iron Heart",
    "setting sun": "Setting Sun", "shadow hand": "Shadow Hand",
    "stone dragon": "Stone Dragon", "tiger claw": "Tiger Claw",
    "white raven": "White Raven",
}
DISC_KEYWORD = {
    "wind": "Desert Wind", "desert": "Desert Wind",
    "spirit": "Devoted Spirit", "devoted": "Devoted Spirit",
    "mind": "Diamond Mind", "diamond": "Diamond Mind",
    "heart": "Iron Heart",  # 'iron' is what the OCR mangles; 'heart' is stable
    "sun": "Setting Sun", "setting": "Setting Sun",
    "hand": "Shadow Hand", "shadow": "Shadow Hand",
    "dragon": "Stone Dragon", "stone": "Stone Dragon",
    "claw": "Tiger Claw", "tiger": "Tiger Claw",
    "raven": "White Raven", "white": "White Raven",
}


def _recover_discipline(text: str) -> Optional[str]:
    low = text.lower()
    for canon, name in DISC_CANON.items():
        if canon in low:
            return name
    for kw, name in DISC_KEYWORD.items():
        if re.search(rf"\b{kw}\b", low):
            return name
    for kw, name in DISC_KEYWORD.items():  # loosest: keyword as a substring
        if kw in low:
            return name
    return None

# An ALL-CAPS maneuver name, apostrophes and hyphens allowed ("HATCHLING'S
# FLAME", "WHITE RAVEN TACTICS"). No trailing sentence punctuation.
NAME_LINE = re.compile(r"^[A-Z][A-Z0-9 '\u2019\-]{2,44}$")
# OCR sprays junk glyphs onto the edges of a name line ("_ AURA OF CHAOS",
# "MOMENT OF PERFECT MIND \ufffd", ") THICKET OF BLADES"); strip these edges before
# testing a name.
EDGE = r"[\s_|)('\u2019\u2018\u201c\u201d\ufffd\".,:;\-]"
EDGE_LEAD = re.compile(rf"^{EDGE}+")
EDGE_TAIL = re.compile(rf"{EDGE}+$")
# A trailing run of ALL-CAPS words on a line the OCR merged with the previous
# column's prose ("Masters eae Wind cantwinland ZEPHYR DANCE" -> "ZEPHYR
# DANCE"). Requires two or more caps words to avoid grabbing a stray acronym.
TRAIL_CAPS = re.compile(r"([A-Z][A-Z'\u2019]{2,}(?:\s+[A-Z][A-Z'\u2019\-]+){1,4})\s*$")

FIELD_LABEL = re.compile(
    r"^(Level|Class|Prerequisites?|Initiation Action|Range|Target|Targets|Area|"
    r"Effect|Duration|Saving Throw)\s*[:;]", re.IGNORECASE)
# The reliable maneuver-block signal: a Level/Class line (the book uses either,
# and the OCR mangles the label with leading junk or a stray semicolon) close
# below the discipline line. Chapter/TOC headers, NPC stat blocks, and the
# fiction that also name a discipline carry no such line and are rejected.
LEVELISH = re.compile(r"^[^A-Za-z]{0,4}(?:Level|Class)\s*[:;]", re.IGNORECASE)

INIT = re.compile(r"^Initiation Action\s*[:;]\s*(.+)$", re.IGNORECASE)
LEVEL = re.compile(r"^(?:Level|Class)\s*[:;]\s*(.+)$", re.IGNORECASE)
PREREQ = re.compile(r"^Prerequisites?\s*:\s*(.+)$", re.IGNORECASE)
RANGE = re.compile(r"^Range\s*:\s*(.+)$", re.IGNORECASE)
DURATION = re.compile(r"^Duration\s*:\s*(.+)$", re.IGNORECASE)
SAVE = re.compile(r"^Saving Throw\s*:\s*(.+)$", re.IGNORECASE)


def _letter_majority(name: str) -> bool:
    letters = sum(ch.isalpha() for ch in name)
    return letters >= max(3, len(name.replace(" ", "")) // 2)


@dataclass
class Maneuver:
    name: str
    book: str
    page: int
    start: int  # line span in the extraction, for --export
    end: int
    discipline: Optional[str] = None
    type: Optional[str] = None            # Boost / Counter / Stance / Strike
    descriptor: Optional[str] = None      # [Fire], [Cold], ...
    level: Optional[str] = None
    prerequisite: Optional[str] = None
    initiation_action: Optional[str] = None
    range: Optional[str] = None
    duration: Optional[str] = None
    save: Optional[str] = None

    def quick_fields(self) -> int:
        return sum(1 for v in (self.discipline, self.type, self.level,
                               self.initiation_action, self.range) if v)


def _join_wrapped_value(left: str, right: str) -> str:
    if left.endswith("-"):
        return left[:-1] + right
    return f"{left} {right}".strip()


def _field_value(body_lines: List[str], index: int, value: str, attr: str) -> str:
    """Join only source-proven signature continuations, never descriptive prose."""
    j = index + 1
    joins = 0
    while j < len(body_lines) and joins < 3:
        while j < len(body_lines) and not body_lines[j].strip():
            j += 1
        if j >= len(body_lines):
            break
        following = body_lines[j].strip()
        if PAGE.search(body_lines[j]) or FIELD_LABEL.match(following):
            break
        needs_more = (
            value.endswith("-")
            or (attr == "level" and value.endswith(","))
            or (attr == "prerequisite"
                and not re.search(r"\b(?:maneuvers?|stances?)\b", value,
                                  re.IGNORECASE))
            or (attr == "initiation_action"
                and not re.search(r"\bactions?\b", value, re.IGNORECASE))
            or (attr in ("duration", "save")
                and (value.endswith(";")
                     or value.casefold().endswith(" see")))
        )
        if not needs_more:
            break
        value = _join_wrapped_value(value, following)
        joins += 1
        j += 1
    return _clean_book_text(re.sub(r"\s+", " ", value)).strip()


def parse_quick_fields(m: Maneuver, body_lines: List[str]) -> None:
    for index, raw in enumerate(body_lines):
        line = raw.strip()
        if not line:
            continue
        if m.initiation_action is None and line.casefold() == "initiation":
            j = index + 1
            while j < len(body_lines) and not body_lines[j].strip():
                j += 1
            if j < len(body_lines):
                split_label = re.match(
                    r"^Action\s*[:;]\s*(.+)$",
                    body_lines[j].strip(), re.IGNORECASE)
                if split_label:
                    m.initiation_action = _field_value(
                        body_lines, j, split_label.group(1).strip(),
                        "initiation_action")
                    continue
        for attr, rx in (("level", LEVEL), ("prerequisite", PREREQ),
                         ("initiation_action", INIT), ("range", RANGE),
                         ("duration", DURATION), ("save", SAVE)):
            if getattr(m, attr) is None:
                match = rx.match(line)
                if match:
                    value = _field_value(body_lines, index,
                                         match.group(1).strip(), attr)
                    setattr(m, attr, value)
                    break


# ---------------------------------------------------------------------------
# Detector
# ---------------------------------------------------------------------------


def _looks_like_maneuver(lines: List[str], disc_idx: int, n: int, window: int = 3) -> bool:
    """A discipline line begins a real maneuver/stance block when a Level (or
    Class) line follows within a couple of content lines. This survives the OCR
    damage to the "Initiation Action" label that a stricter test tripped on."""
    j, seen = disc_idx + 1, 0
    while j < n and seen < window:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            j += 1
            continue
        seen += 1
        if LEVELISH.match(s):
            return True
        j += 1
    return False


def _clean_caps(s: str) -> Optional[str]:
    """A stripped ALL-CAPS name if the line is one after edge junk is removed."""
    t = EDGE_TAIL.sub("", EDGE_LEAD.sub("", s))
    if NAME_LINE.match(t) and _letter_majority(t) \
            and not FIELD_LABEL.match(t) and not DISC_ANCHOR.match(t):
        return t
    return None


def _find_name(lines: List[str], disc_idx: int) -> Optional[Tuple[int, str]]:
    """The ALL-CAPS maneuver name sits above the discipline line. Strategy 1:
    consecutive clean ALL-CAPS fragments (handles wrapped names and edge junk).
    Strategy 2 (fallback): a trailing ALL-CAPS run on a line the OCR merged
    with the previous column's prose. Returns (topmost line, name) or None."""
    frags: List[str] = []
    top = disc_idx
    j, gap = disc_idx - 1, 0
    while j >= 0 and len(frags) < 5:
        raw = lines[j]
        s = raw.strip()
        if s == "" or PAGE.search(raw):
            gap += 1
            if gap > 2:
                break
            j -= 1
            continue
        c = _clean_caps(s)
        if c:
            frags.append(c)
            top, gap = j, 0
            j -= 1
            continue
        break
    if frags:
        frags.reverse()
        return top, re.sub(r"\s+", " ", " ".join(frags)).strip().title()

    j, seen = disc_idx - 1, 0
    while j >= 0 and seen < 3:
        raw = lines[j]
        s = raw.strip()
        if s == "" or PAGE.search(raw):
            j -= 1
            continue
        seen += 1
        m = TRAIL_CAPS.search(s)
        if m:
            return j, re.sub(r"\s+", " ", m.group(1)).strip().title()
        j -= 1
    return None


def detect_tob(lines: List[str], pages: List[int], book: str) -> List[Maneuver]:
    n = len(lines)
    starts: List[Tuple[int, str, Optional[str], Optional[str], Optional[str]]] = []
    used = set()
    for i, ln in enumerate(lines):
        s = ln.strip()
        tm = TYPE_LINE.match(s)
        if not tm:
            continue
        if not _looks_like_maneuver(lines, i, n):
            continue
        got = _find_name(lines, i)
        if got is None or got[0] in used:
            continue
        top, name = got
        used.add(top)
        mtype = tm.group(2).title()
        dm = DESC_RE.search(s)
        desc = f"[{dm.group(1).strip()}]" if dm else None
        # Discipline from the type-line prefix, else from a line between the
        # name and the type (a wrapped discipline word).
        disc = _recover_discipline(tm.group(1))
        if disc is None:
            for k in range(top, i):
                disc = _recover_discipline(lines[k])
                if disc:
                    break
        starts.append((top, name, disc, mtype, desc))

    starts.sort()
    maneuvers: List[Maneuver] = []
    for k, (top, name, disc, mtype, desc) in enumerate(starts):
        e = starts[k + 1][0] if k + 1 < len(starts) else min(n, top + 70)
        e = min(e, top + 70)
        m = Maneuver(name=name, book=book, page=pages[top], start=top, end=e,
                     discipline=disc, type=mtype, descriptor=desc)
        parse_quick_fields(m, lines[top + 1:e])
        maneuvers.append(m)
    return maneuvers


_LIGATURES = str.maketrans({
    "\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl",
    "\ufb03": "ffi", "\ufb04": "ffl",
})
SUMMARY_DISCIPLINES = {
    "Desert": "Desert Wind",
    "Devo": "Devoted Spirit",
    "Diam": "Diamond Mind",
    "Iron": "Iron Heart",
    "Set": "Setting Sun",
    "Shadow": "Shadow Hand",
    "Stone": "Stone Dragon",
    "Tiger": "Tiger Claw",
    "White": "White Raven",
}
SUMMARY_LEVEL = re.compile(r"^([1-9])(?:ST|ND|RD|TH) LEVEL$", re.IGNORECASE)
DETAIL_NAME_LINE = re.compile(r"^[A-Z][A-Z0-9 '\u2019,\-]{2,54}$")


def _clean_book_text(text: str) -> str:
    """Expand PDF ligatures, including a spurious intra-word space after one."""
    for ligature, plain in (("\ufb00", "ff"), ("\ufb01", "fi"), ("\ufb02", "fl"),
                            ("\ufb03", "ffi"), ("\ufb04", "ffl")):
        text = re.sub(ligature + r"\s+(?=[A-Za-z])", plain, text)
    return text.translate(_LIGATURES)


def _name_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", _clean_book_text(text).casefold()).strip()


def _summary_entries(
        lines: List[str]) -> List[Tuple[str, int, str, Optional[str]]]:
    """Parse the book's canonical maneuver/stance lists on PDF pages 48-51."""
    starts = [i for i, line in enumerate(lines) if line.strip() == "STANCE LISTS"]
    if not starts:
        return []
    start = starts[0]
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].strip() == "## [PDF page 52]"), len(lines))
    level: Optional[int] = None
    discipline: Optional[str] = None
    entries: List[Tuple[str, int, str, Optional[str]]] = []
    for raw in lines[start + 1:end]:
        text = _clean_book_text(raw.strip())
        lm = SUMMARY_LEVEL.match(text)
        if lm:
            level = int(lm.group(1))
            discipline = None
            continue
        if text in SUMMARY_DISCIPLINES:
            discipline = SUMMARY_DISCIPLINES[text]
            continue
        # The PDF puts the Shadow Hand column label on the same line as the
        # first Shadow entry at each level. Other discipline labels stand alone.
        if discipline == "Setting Sun" and text.startswith("Shadow "):
            discipline = "Shadow Hand"
            text = text[len("Shadow "):].lstrip()
        if ":" not in text or level is None or discipline is None:
            continue
        name = re.sub(r"\s+", " ", text.split(":", 1)[0]).strip()
        if (len(name) > 70
                or not re.fullmatch(r"[A-Z][A-Za-z0-9\u2019'\- ]+", name)):
            continue
        tm = re.search(r":\s*(Boost|Counter|Stance|Strike)\b",
                       text, re.IGNORECASE)
        mtype = tm.group(1).title() if tm else None
        entries.append((name, level, discipline, mtype))
    return entries


def _clean_detail_caps(text: str) -> Optional[str]:
    cleaned = EDGE_TAIL.sub("", EDGE_LEAD.sub("", text))
    if (DETAIL_NAME_LINE.match(cleaned) and _letter_majority(cleaned)
            and not FIELD_LABEL.match(cleaned) and not DISC_ANCHOR.match(cleaned)):
        return cleaned
    return None


def _find_detail_name(lines: List[str], discipline_idx: int) -> Optional[Tuple[int, str]]:
    """Find a possibly wrapped ALL-CAPS heading above a detail signature."""
    frags: List[str] = []
    top = discipline_idx
    j, gap = discipline_idx - 1, 0
    while j >= 0 and len(frags) < 5:
        raw = lines[j]
        text = raw.strip()
        if text == "" or PAGE.search(raw):
            gap += 1
            if gap > 2:
                break
            j -= 1
            continue
        cleaned = _clean_detail_caps(text)
        if cleaned:
            frags.append(cleaned)
            top, gap = j, 0
            j -= 1
            continue
        break
    if frags:
        frags.reverse()
        return top, re.sub(r"\s+", " ", " ".join(frags)).strip().title()

    j, seen = discipline_idx - 1, 0
    while j >= 0 and seen < 3:
        raw = lines[j]
        text = raw.strip()
        if text == "" or PAGE.search(raw):
            j -= 1
            continue
        seen += 1
        match = TRAIL_CAPS.search(text)
        if match:
            return j, re.sub(r"\s+", " ", match.group(1)).strip().title()
        j -= 1
    return None


def _level_number(text: Optional[str]) -> Optional[int]:
    values = {int(value) for value in re.findall(r"\b([1-9])\b", text or "")}
    return next(iter(values)) if len(values) == 1 else None


def _apply_summary_names(
        maneuvers: List[Maneuver],
        summary: List[Tuple[str, int, str, Optional[str]]]) -> None:
    """Reconcile detail headings to canonical names within discipline + level."""
    summary_groups: Dict[Tuple[str, int],
                         List[Tuple[str, int, str, Optional[str]]]] = {}
    detail_groups: Dict[Tuple[str, int], List[Maneuver]] = {}
    for entry in summary:
        summary_groups.setdefault((entry[2], entry[1]), []).append(entry)
    for maneuver in maneuvers:
        level = _level_number(maneuver.level)
        if maneuver.discipline and level is not None:
            detail_groups.setdefault((maneuver.discipline, level), []).append(maneuver)

    def apply(maneuver: Maneuver,
              entry: Tuple[str, int, str, Optional[str]]) -> None:
        maneuver.name = entry[0]
        if maneuver.type is None and entry[3]:
            maneuver.type = entry[3]

    for group, entries in summary_groups.items():
        details = detail_groups.get(group, [])
        if len(details) != len(entries):
            continue
        by_summary = {_name_key(entry[0]): entry for entry in entries}
        by_detail = {_name_key(maneuver.name): maneuver for maneuver in details}
        exact = set(by_summary) & set(by_detail)
        for key in exact:
            apply(by_detail[key], by_summary[key])

        remaining_entries = [by_summary[key]
                             for key in sorted(set(by_summary) - exact)]
        remaining_details = [by_detail[key]
                             for key in sorted(set(by_detail) - exact)]
        if len(remaining_entries) != len(remaining_details):
            continue
        if not remaining_entries:
            continue
        best = max(
            itertools.permutations(remaining_entries),
            key=lambda permutation: sum(
                difflib.SequenceMatcher(
                    None, _name_key(maneuver.name), _name_key(entry[0])
                ).ratio()
                for maneuver, entry in zip(remaining_details, permutation)
            ),
        )
        for maneuver, entry in zip(remaining_details, best):
            ratio = difflib.SequenceMatcher(
                None, _name_key(maneuver.name), _name_key(entry[0])
            ).ratio()
            if ratio >= 0.55:
                apply(maneuver, entry)


def detect_tob_born_digital(
        lines: List[str], pages: List[int], book: str) -> List[Maneuver]:
    """Parse all detailed entries, then bind their canonical summary-list names."""
    detail_start = next((i for i, line in enumerate(lines)
                         if line.strip() == "## [PDF page 52]"), 0)
    detail_end = next((i for i in range(detail_start + 1, len(lines))
                       if lines[i].strip() == "## [PDF page 95]"), len(lines))
    starts: List[Tuple[int, str, str, Optional[str], Optional[str]]] = []
    used = set()
    for level_idx in range(detail_start, detail_end):
        if not LEVELISH.match(lines[level_idx].strip()):
            continue
        discipline_idx: Optional[int] = None
        discipline: Optional[str] = None
        j, seen = level_idx - 1, 0
        while j >= detail_start and seen < 5:
            text = lines[j].strip()
            if not text or PAGE.search(lines[j]):
                j -= 1
                continue
            seen += 1
            recovered = _recover_discipline(text)
            if recovered and len(text) < 100:
                discipline_idx, discipline = j, recovered
                break
            j -= 1
        if discipline_idx is None or discipline is None:
            continue
        got = _find_detail_name(lines, discipline_idx)
        if got is None or got[0] in used:
            continue
        top, name = got
        used.add(top)
        signature = " ".join(
            line.strip() for line in lines[discipline_idx:level_idx]
            if line.strip() and not PAGE.search(line)
        )
        tm = TYPE_LINE.match(signature)
        mtype = tm.group(2).title() if tm else None
        dm = DESC_RE.search(signature)
        descriptor = f"[{dm.group(1).strip()}]" if dm else None
        starts.append((top, name, discipline, mtype, descriptor))

    starts.sort()
    maneuvers: List[Maneuver] = []
    for position, (top, name, discipline, mtype, descriptor) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else detail_end
        maneuver = Maneuver(
            name=name,
            book=book,
            page=pages[top],
            start=top,
            end=end,
            discipline=discipline,
            type=mtype,
            descriptor=descriptor,
        )
        parse_quick_fields(maneuver, lines[top + 1:end])
        maneuvers.append(maneuver)

    _apply_summary_names(maneuvers, _summary_entries(lines))
    return maneuvers


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[Maneuver]]] = {
    "tob": detect_tob,
    "tob_born_digital": detect_tob_born_digital,
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
    maneuvers: List[Maneuver] = field(default_factory=list)


SOURCES: List[Source] = [
    Source(
        key="tob",
        book="Tome of Battle",
        path=Path("D&D 3.5e/Player Options/Tome of Battle (alt scan).md"),
        citation=("Tome of Battle: The Book of Nine Swords (WotC, 2006), "
                  "maneuver/stance lists pp. 48–51 and full descriptions pp. 52–94"),
        detector="tob_born_digital",
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
            src.maneuvers = DETECTORS[src.detector](src.lines, pages, src.book)
            src.coverage = f"ok — {len(src.maneuvers)} maneuvers from {path.name}"

    def all_maneuvers(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for m in src.maneuvers:
                yield src, m

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, m in self.all_maneuvers(book):
            n = m.name.lower()
            if n == q:
                exact.append((src, m))
            elif q in n:
                partial.append((src, m))
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
        "# MARTIAL MANEUVER INDEX — The New Path",
        "",
        "**Generated by `scripts/maneuver_harvest.py`. Do not hand-edit; rerun",
        "the harvest.** One row per Tome of Battle maneuver or stance found in",
        "the extraction. Every row records its true full-description span;",
        "the raw text stays on `I:\\Sourcebooks`. Use",
        "`python scripts/maneuver_harvest.py --export \"NAME\"` to emit a",
        "translator-ready packet for the paired 3.5e + GURPS build.",
        "",
        "Every entry names its book and the PDF page the extraction recorded.",
        "This index holds the MECHANICAL vocabulary only — discipline, type,",
        "level, initiation action, range — never invented facts; a field left",
        "as `—` is not separately stated in that entry's printed signature.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.maneuvers)
        parsed_well += sum(1 for m in src.maneuvers if m.quick_fields() >= 3)
        sources_out.append({
            "key": src.key,
            "book": src.book,
            "citation": src.citation,
            "coverage": src.coverage,
            "source_path": str(src.path),
            "maneuvers": [asdict(m) for m in src.maneuvers],
        })
        md.append(f"## {src.book} — {len(src.maneuvers)} maneuvers and stances")
        md.append("")
        md.append(f"*Source: {src.citation}.*")
        md.append(f"*Extraction: `{corpus.base / src.path}`.*")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.maneuvers:
            md.append("| Maneuver / Stance | Discipline | Type | Level | Initiation | Range | Page |")
            md.append("|---|---|---|---|---|---|---|")
            for m in src.maneuvers:
                disc = m.discipline or "—"
                if m.descriptor:
                    disc = f"{disc} {m.descriptor}"
                md.append(
                    f"| {m.name} | {disc} | {m.type or '—'} | {m.level or '—'} | "
                    f"{m.initiation_action or '—'} | {m.range or '—'} | {m.page or '—'} |"
                )
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps(
            {
                "generated_by": "scripts/maneuver_harvest.py",
                "corpus": str(corpus.base),
                "total_maneuvers": total,
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
        print(f"'{name}' matches {len(hits)} maneuvers; narrow with the exact name:")
        for src, m in hits[:20]:
            print(f"  {m.name}   [{m.book}, p.{m.page}]")
        return 1
    packets = []
    for src, m in hits:
        body = [ln for ln in src.lines[m.start:m.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "maneuver-for-translation",
            "instructions": (
                "Feed this packet to the system-translator skill. Both a 3.5e "
                "AND a GURPS treatment are required in the output — a conversion "
                "missing either system is incomplete (that skill's own rule). "
                "The raw_block is clean born-digital book text; the source "
                "PDF on I:\\Sourcebooks remains the final court of appeal."
            ),
            "name": m.name,
            "source": {
                "book": m.book, "pdf_page": m.page,
                "extraction": str(corpus.base / src.path),
                "lines": [m.start + 1, m.end],
                "citation": src.citation,
            },
            "parsed": {k: v for k, v in asdict(m).items()
                       if k in ("discipline", "type", "descriptor", "level",
                                "prerequisite", "initiation_action", "range",
                                "duration", "save") and v},
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

FIXTURE = """## [PDF page 42]
Desert Wind

Desert Wind maneuvers focus on fire and mobility, granting flame.

BLISTERING FLOURISH

Desert Wind (Strike) [Fire]

Level: Swordsage 1

Initiation Action: 1 standard action

Range: 30 ft.

Target: All creatures in range

Duration: Instantaneous

Saving Throw: Reflex negates

A wave of fire washes out from you.

FIRE RIPOSTE

Desert Wind (Counter) [Fire]

Level: Swordsage 2

Prerequisite: One Desert Wind maneuver

Initiation Action: 1 immediate action

Range: Personal

Target: You

Duration: Instantaneous

When an enemy strikes you, you retaliate with flame.

STEEL WIND

Tron Heart (Strike)

Level: Warblade 1

Initiation Action; 1 standard action

Range: Melee attack

Target: Two creatures

Duration: Instantaneous

You attack with unbelievable speed, striking two enemies.
"""


BORN_FIXTURE = """MANEUVER AND
STANCE LISTS
1ST LEVEL
Desert
Blistering Flourish: Strike—Dazzle nearby creatures.
3RD LEVEL
Iron
Iron Heart Surge: Remove one debilitating effect.
2ND LEVEL
Set
Mighty Throw: Strike—Throw a foe.
Shadow Shadow Jaunt: Teleport through shadows.
8TH LEVEL
Devo
Greater Divine Surge: Strike—Channel a devastating attack.
## [PDF page 52]
BLISTERING FLOURISH
Desert Wind (Strike) [Fire]
Level: Swordsage 1
Initiation Action: 1 standard action
Range: 30 ft.
Duration: Instantaneous
A wave of flame dazzles your foes.
IRON HEART SURGE
Iron Heart
Level: Warblade 3
Initiation Action: 1 standard action
Range: Personal
Duration: See text
You break free of a debilitating state.
SHADOW JAUNT
Shadow Hand [Teleportation]
Level: Swordsage 2
Initiation Action: 1 standard action
Range: 50 ft.
Target: You
You disappear and reappear in shadow.
DIVINE SURGE, GREATER
Devoted Spirit (Strike)
Level: Crusader 8
Prerequisite: Two Devoted Spirit maneuvers
Initiation Action: 1 full-round action
Range: Melee attack
Duration: 1 round; see text
A torrent of divine energy courses through you.
## [PDF page 95]
The next chapter begins here.
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "D&D 3.5e" / "Player Options").mkdir(parents=True)
        (d / "D&D 3.5e" / "Player Options" / "Tome of Battle - Book of Nine Swords.md").write_text(
            FIXTURE, encoding="utf-8")
        corpus = Corpus(d, [Source(key="tob", book="Tome of Battle",
                                   path=Path("D&D 3.5e/Player Options/Tome of Battle - Book of Nine Swords.md"),
                                   citation="fixture", detector="tob")])
        maneuvers = [m for _, m in corpus.all_maneuvers()]
        names = [m.name for m in maneuvers]
        # The three named maneuvers are detected; the bare "Desert Wind"
        # discipline intro (no Level line below it) is rejected. Steel Wind
        # exercises OCR damage: a corrupted discipline ("Tron Heart" -> Iron
        # Heart by keyword) and a semicolon in the Initiation Action label.
        want_names = ["Blistering Flourish", "Fire Riposte", "Steel Wind"]
        if names != want_names:
            failures.append(f"fixture detected {names}, wanted {want_names} "
                            f"(the Desert Wind discipline intro must be rejected)")
        else:
            bf = maneuvers[0]
            got = (bf.discipline, bf.type, bf.descriptor, bf.level,
                   bf.initiation_action, bf.range, bf.save)
            want = ("Desert Wind", "Strike", "[Fire]", "Swordsage 1",
                    "1 standard action", "30 ft.", "Reflex negates")
            if got != want:
                failures.append(f"Blistering Flourish quick fields {got}, wanted {want}")
            fr = maneuvers[1]
            if fr.type != "Counter" or fr.prerequisite != "One Desert Wind maneuver":
                failures.append(f"Fire Riposte type={fr.type!r} "
                                f"prereq={fr.prerequisite!r}, wanted Counter / "
                                f"One Desert Wind maneuver")
            sw = maneuvers[2]
            if sw.discipline != "Iron Heart" or sw.type != "Strike" \
                    or sw.initiation_action != "1 standard action":
                failures.append(f"Steel Wind discipline={sw.discipline!r} "
                                f"type={sw.type!r} init={sw.initiation_action!r}, "
                                f"wanted Iron Heart / Strike / 1 standard action "
                                f"(keyword recovery + semicolon-tolerant label)")

    born_lines = BORN_FIXTURE.splitlines()
    born = detect_tob_born_digital(
        born_lines, _pages_for(born_lines), "Tome of Battle fixture")
    born_names = [m.name for m in born]
    expected_born = [
        "Blistering Flourish", "Iron Heart Surge",
        "Shadow Jaunt", "Greater Divine Surge",
    ]
    if born_names != expected_born:
        failures.append(f"born-digital fixture detected {born_names}, "
                        f"wanted {expected_born}")
    else:
        by_name = {m.name: m for m in born}
        if (by_name["Greater Divine Surge"].type,
                by_name["Greater Divine Surge"].level,
                by_name["Greater Divine Surge"].initiation_action) != (
                    "Strike", "Crusader 8", "1 full-round action"):
            failures.append("born fixture did not reconcile comma-reordered "
                            "Greater Divine Surge or parse its fields")
        if (by_name["Shadow Jaunt"].type is not None
                or by_name["Shadow Jaunt"].descriptor != "[Teleportation]"):
            failures.append("born fixture Shadow Jaunt must retain its printed "
                            "type-less [Teleportation] signature")
        if any(born[i].end != born[i + 1].start
               for i in range(len(born) - 1)):
            failures.append("born fixture spans are not heading-to-heading")
        if (not born or born[-1].end >= len(born_lines)
                or born_lines[born[-1].end].strip() != "## [PDF page 95]"):
            failures.append("born fixture final span did not end at the next chapter")

    if base.is_dir() and (base / SOURCES[0].path).exists():
        corpus = Corpus(base, _fresh_sources())
        src = corpus.sources[0]
        maneuvers = src.maneuvers
        summary = _summary_entries(src.lines)
        if len(maneuvers) != 208:
            failures.append(f"{len(maneuvers)} ToB detail entries; expected exactly 208")
        if len(summary) != 208:
            failures.append(f"{len(summary)} ToB summary entries; expected exactly 208")
        names = {_name_key(m.name) for m in maneuvers}
        summary_names = {_name_key(entry[0]) for entry in summary}
        if len(names) != 208 or names != summary_names:
            failures.append("live detail names do not reconcile one-to-one with "
                            "the 208 canonical summary-list names")
        discipline_counts = {
            discipline: sum(m.discipline == discipline for m in maneuvers)
            for discipline in DISC_CANON.values()
        }
        expected_disciplines = {
            "Desert Wind": 27, "Devoted Spirit": 26, "Diamond Mind": 22,
            "Iron Heart": 21, "Setting Sun": 20, "Shadow Hand": 25,
            "Stone Dragon": 24, "Tiger Claw": 23, "White Raven": 20,
        }
        if discipline_counts != expected_disciplines:
            failures.append(f"discipline counts {discipline_counts}, "
                            f"wanted {expected_disciplines}")
        type_counts = {
            mtype: sum(m.type == mtype for m in maneuvers)
            for mtype in ("Boost", "Counter", "Stance", "Strike", None)
        }
        expected_types = {
            "Boost": 22, "Counter": 22, "Stance": 46, "Strike": 113, None: 5,
        }
        if type_counts != expected_types:
            failures.append(f"type counts {type_counts}, wanted {expected_types}")
        if sum(m.quick_fields() >= 3 for m in maneuvers) != 208:
            failures.append("not all 208 live entries carry at least 3 quick fields")
        if (not maneuvers or min(m.page for m in maneuvers) != 52
                or max(m.page for m in maneuvers) != 94):
            failures.append("live detail headings did not span PDF pages 52–94")
        bad_spans = []
        for position, maneuver in enumerate(maneuvers):
            head = _name_key("\n".join(
                src.lines[maneuver.start:min(maneuver.end, maneuver.start + 5)]))
            tokens = [token for token in _name_key(maneuver.name).split()
                      if len(token) >= 4] or _name_key(maneuver.name).split()
            expected_end = (maneuvers[position + 1].start
                            if position + 1 < len(maneuvers)
                            else maneuver.end)
            if (maneuver.end - maneuver.start < 12
                    or not all(token in head for token in tokens[:2])
                    or (position + 1 < len(maneuvers)
                        and maneuver.end != expected_end)
                    or not maneuver.initiation_action):
                bad_spans.append((maneuver.name, maneuver.start, maneuver.end))
        if bad_spans:
            failures.append(f"invalid live full-description spans: {bad_spans[:5]}")
        if (maneuvers and (maneuvers[-1].end >= len(src.lines)
                           or src.lines[maneuvers[-1].end].strip()
                           != "## [PDF page 95]")):
            failures.append("live final maneuver span did not stop before chapter 5")
        if any("\ufffd" in line for line in src.lines):
            failures.append("born-digital Tome of Battle source contains U+FFFD")
        by_name = {m.name: m for m in maneuvers}
        expected_recoveries = {
            "Greater Divine Surge": (58, "Devoted Spirit", "Strike", "Crusader 8"),
            "Iron Heart Surge": (68, "Iron Heart", None, "Warblade 3"),
            "Shadow Jaunt": (79, "Shadow Hand", None, "Swordsage 2"),
            "Shadow Stride": (80, "Shadow Hand", None, "Swordsage 5"),
            "Shadow Blink": (78, "Shadow Hand", None, "Swordsage 7"),
            "Order Forged from Chaos": (
                92, "White Raven", None, "Crusader 6, warblade 6"),
        }
        for name, expected in expected_recoveries.items():
            maneuver = by_name.get(name)
            got = ((maneuver.page, maneuver.discipline, maneuver.type,
                    maneuver.level) if maneuver else None)
            if got != expected:
                failures.append(f"live {name} fields {got}, wanted {expected}")
        death = by_name.get("Death in the Dark")
        if (not death or death.type != "Strike"
                or death.initiation_action != "1 standard action"):
            failures.append(f"live Death in the Dark signature mismatch: {death}")
        greater = by_name.get("Greater Insightful Strike")
        absolute = by_name.get("Absolute Steel Stance")
        if not greater or not absolute:
            failures.append("summary reconciliation lost a canonical reordered name")
    else:
        print(f"  [SKIP] ToB alternate extraction not found under {base} — "
              "fixture checks only")

    for failure in failures:
        print(f"SELFTEST FAIL: {failure}")
    print("selftest: " + ("PASS" if not failures else f"{len(failures)} failure(s)"))
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--corpus", type=Path, default=CORPUS,
                    help="base of the text extractions (default I:\\Sourcebooks\\_text)")
    ap.add_argument("--search", metavar="TEXT", help="substring search on indexed names")
    ap.add_argument("--book", help="restrict to one source (key or book title, e.g. tob)")
    ap.add_argument("--export", metavar="NAME", help="emit a translator-ready packet")
    ap.add_argument("--out", type=Path, help="write the packet here instead of stdout")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest(args.corpus)

    corpus = Corpus(args.corpus, _fresh_sources())

    if args.search:
        q = args.search.lower()
        found = sorted({(m.name, m.book, m.page, m.discipline or "—")
                        for _, m in corpus.all_maneuvers(args.book) if q in m.name.lower()})
        for name, book, page, disc in found:
            print(f"  {name}   [{disc}, {book}, p.{page}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.maneuvers for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.maneuvers):5d} maneuvers" if src.maneuvers else "    0 maneuvers"
        print(f"  {src.book:28s} {status}  [{src.coverage}]")
    if not any_ok:
        print("\nNothing harvested at all — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} maneuvers/stances across {sum(1 for s in corpus.sources if s.maneuvers)} source(s); "
          f"{parsed_well} with 3+ quick fields parsed.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
