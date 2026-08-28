#!/usr/bin/env python3
"""wh40krp_psychic_harvest.py — collate Warhammer 40,000 Roleplay psychic powers.

THE PROCESS (Chad, 2026-08-28): other GAME SYSTEMS are welcome AS LONG AS they are
labelled by system — the translator tools convert them. This is the FIRST
**Warhammer 40,000 Roleplay** (Fantasy Flight Games d100) content in the reference
layer: the psychic powers a psyker manifests via a Focus Power Test. Every row is
stamped `"system": "WH40K Roleplay"` and is SOURCE MATERIAL for the
system-translator skill. This is NOT the tabletop wargame and NOT any D&D/GURPS
subsystem — it is the FFG roleplay line (Dark Heresy, Rogue Trader, Deathwatch,
Only War, Black Crusade).

    reference/wh40krp_psychic_index.json — every power: name, discipline, action,
                                           opposed, range, sustained, subtype,
                                           focus power, threshold, value (xp),
                                           prerequisites, one-line effect, book,
                                           PDF page, system WH40K Roleplay
    reference/wh40krp_psychic_index.md   — the same, for human eyes

GOVERNING SOURCES
    I:\\Sourcebooks\\_text\\Warhammer\\40K Roleplay\\ — the five core rulebooks,
    each with a Psychic Powers / Psychic Techniques chapter. THREE stat-block
    formats coexist and each gets its own detector:

      * Dark Heresy (1st ed.): an ALTERNATING label/value block — a "Threshold:"
        line, then the value on the next line, then "Focus Time:" / value /
        "Sustained:" / value / "Range:" / value, then the effect prose. Anchor:
        the "Threshold:" label line; the name is the line above it; discipline
        from the "Minor Powers" / Biomancy / Divination / Pyromancy / Telekinetics
        / Telepathy section headers.

      * Deathwatch / Only War / Black Crusade (the "modern" FFG layout): INLINE
        "Action: Half Action" / "Opposed: Yes" / "Range: …" / "Sustained: …" /
        "Subtype: …" fields under the power name (Only War & Black Crusade add
        Value / Prerequisites / "Focus Power:" and fold Opposed into the Focus
        Power line). Anchor: the "Action:" line whose value is a real action; the
        name is walked up past any Value / Prerequisites / Alternate Names lines;
        discipline from the section headers (Telepathy / Divination / Codex /
        Chapter powers for DW; Biomancy…Telepathy for OW; Unaligned / Nurgle /
        Slaanesh / Tzeentch / Exalted + Telepathy / Telekinesis / Divination for
        BC). NB: the two-column PDFs linearise so a discipline's last powers can
        sit just above the NEXT header, so OW/BC discipline labels are best-effort
        at section boundaries — the mechanical fields stay exact and cited.

      * Rogue Trader: INLINE "Value: … xp" / "Prerequisites: …" / "Focus Power
        Test: …" / "Range: …" technique blocks (no Action/Sustained inline —
        those live in the summary tables). Anchor: a "Value:" line confirmed by a
        Prerequisites/Focus-Power-Test line just below; the name is the line above
        Value; discipline from the "The <X> Discipline" headers. Opposed is read
        off the Focus Power Test text.

    A configured source whose file is missing prints NO COVERAGE. Nothing is
    invented; every row cites its book and PDF page. --selftest runs fixture + live
    checks; --export NAME emits a translation packet; --search TEXT greps names.
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
OUT_JSON = REPO / "reference" / "wh40krp_psychic_index.json"
OUT_MD = REPO / "reference" / "wh40krp_psychic_index.md"
SYSTEM = "WH40K Roleplay"

PAGE = re.compile(r"\[PDF page (\d+)\]")

# ---- shared field patterns (inline "Label: value") -------------------------
ACTION = re.compile(r"^Action\s*:\s*(.+)$", re.IGNORECASE)
OPPOSED = re.compile(r"^Opposed\s*:\s*(.+)$", re.IGNORECASE)
RANGE = re.compile(r"^Range\s*:\s*(.+)$", re.IGNORECASE)
SUSTAINED = re.compile(r"^Sustained\s*:\s*(.+)$", re.IGNORECASE)
SUBTYPE = re.compile(r"^Subtype\s*:\s*(.+)$", re.IGNORECASE)
FOCUS_POWER = re.compile(r"^Focus\s+Power\s*:\s*(.+)$", re.IGNORECASE)
FOCUS_POWER_TEST = re.compile(r"^Focus\s+Power\s+Test\s*:\s*(.+)$", re.IGNORECASE)
VALUE = re.compile(r"^Value\s*:\s*(.+)$", re.IGNORECASE)
PREREQ = re.compile(r"^Prerequisites?\s*:\s*(.+)$", re.IGNORECASE)
DESCRIPTION = re.compile(r"^Description\s*:\s*(.*)$", re.IGNORECASE)
ALT_NAMES = re.compile(r"^Alternate\s+Names?\s*:", re.IGNORECASE)
# lines that can appear ABOVE the name-bearing anchor in a modern block
MODERN_LEADFIELD = re.compile(
    r"^(Value|Prerequisites?|Alternate\s+Names?|Name)\s*:", re.IGNORECASE)
# the value on an "Action:" line must be a real action for the block to be a power
ACTION_VALUE = re.compile(
    r"^(Free|Half|Full|Reaction|Extended|Various|Varies|None)\b", re.IGNORECASE)

# ---- Dark Heresy alternating labels ----------------------------------------
DH_THRESHOLD = re.compile(r"^Threshold\s*:\s*$", re.IGNORECASE)
DH_LABELS: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"^Threshold\s*:\s*$", re.IGNORECASE), "threshold"),
    (re.compile(r"^Focus\s+Time\s*:\s*$", re.IGNORECASE), "action"),
    (re.compile(r"^Sustained\s*:\s*$", re.IGNORECASE), "sustained"),
    (re.compile(r"^Range\s*:\s*$", re.IGNORECASE), "range"),
]
DH_ANY_LABEL = re.compile(
    r"^(Threshold|Focus\s+Time|Sustained|Range|Overbleed)\s*:", re.IGNORECASE)

_SMALL = {"of", "the", "and", "or", "a", "an", "to", "in", "on", "from",
          "with", "for", "at", "by"}


def _norm_name(s: str) -> str:
    """Normalise an OCR-cased / ALL-CAPS power name to clean Title Case.

    Strips a trailing bracket tag like "[CORRUPTION]" and title-cases from a
    lowercased base so "asTroTeLePaThy" -> "Astrotelepathy", "LIFE LEECH" ->
    "Life Leech", "bLooD boiL" -> "Blood Boil", while "Mind's Eye" survives.
    """
    s = re.sub(r"\s*\[[^\]]*\]\s*$", "", s.strip())
    # drop a Rogue Trader label prefix ("Special Power: X", "Basic Technique: X")
    s = re.sub(r"(?i)^(?:special power|basic technique)\s*:\s*", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    words = s.split()
    out = []
    for k, w in enumerate(words):
        lw = w.lower()
        out.append(lw if (k > 0 and lw in _SMALL) else (lw[:1].upper() + lw[1:]))
    return " ".join(out)


def _plausible_name(s: str) -> bool:
    s = re.sub(r"\s*\[[^\]]*\]\s*$", "", s.strip())
    if not (3 <= len(s) <= 46):
        return False
    if s.endswith((".", ",", ":", ";")):
        return False
    if not s[0].isalpha():
        return False
    if DESCRIPTION.match(s) or MODERN_LEADFIELD.match(s) or DH_ANY_LABEL.match(s):
        return False
    # a lone single-letter word is the signature of OCR column/drop-cap damage
    # ("L Cina" for HALLUCINATION), never a real power name here — reject it
    if any(len(w) == 1 and w.isalpha() for w in s.split()):
        return False
    letters = sum(c.isalpha() for c in s)
    return letters >= max(3, len(s) // 2)


def _first_sentence(lines: List[str], cap: int = 240) -> Optional[str]:
    text = " ".join(l.strip() for l in lines if not PAGE.search(l))
    text = re.sub(r"\s+", " ", text).strip()
    text = DESCRIPTION.sub(lambda m: m.group(1), text, count=1).strip()
    if not text:
        return None
    m = re.search(r"(.+?[.!?])(?:\s|$)", text)
    s = m.group(1).strip() if (m and len(m.group(1)) >= 20) else text
    return s[:cap].strip()


@dataclass
class Power:
    name: str
    book: str
    page: Optional[int]
    start: int
    end: int
    system: str = SYSTEM
    discipline: Optional[str] = None
    action: Optional[str] = None          # Focus Power Action (DW/OW/BC); DH Focus Time
    opposed: Optional[str] = None         # Yes / No
    range: Optional[str] = None
    sustained: Optional[str] = None
    subtype: Optional[str] = None         # OW / BC
    focus_power: Optional[str] = None     # OW/BC "Focus Power"; RT "Focus Power Test"
    threshold: Optional[str] = None       # Dark Heresy
    value: Optional[str] = None           # xp cost (DW/OW/BC/RT)
    prerequisites: Optional[str] = None
    effect: Optional[str] = None          # one-line summary

    def quick_fields(self) -> int:
        return sum(1 for v in (self.discipline, self.action, self.range,
                               self.sustained, self.effect) if v)


# ---------------------------------------------------------------------------
# discipline section markers
# ---------------------------------------------------------------------------
def _markers(lines: List[str],
             matchers: List[Tuple[re.Pattern, Callable[[re.Match], str]]],
             reject_bulleted: bool = False) -> List[Tuple[int, str]]:
    out: List[Tuple[int, str]] = []
    n = len(lines)

    def adjacent_bullet(i: int) -> bool:
        for step in (-1, 1):
            j = i + step
            while 0 <= j < n and (lines[j].strip() == "" or PAGE.search(lines[j])):
                j += step
            if 0 <= j < n and lines[j].strip().startswith(("\u2022", "•", "·")):
                return True
        return False

    for i, ln in enumerate(lines):
        s = ln.strip()
        for rx, canon in matchers:
            m = rx.match(s)
            if m:
                if reject_bulleted and adjacent_bullet(i):
                    break
                out.append((i, canon(m)))
                break
    return out


def _discipline_at(markers: List[Tuple[int, str]], idx: int) -> Optional[str]:
    disc = None
    for mi, mname in markers:
        if mi < idx:
            disc = mname
        else:
            break
    if disc is None:
        # a power that sits just ABOVE the first section header (two-column PDFs
        # linearise a discipline's last powers before its header) belongs to the
        # section it flows into — adopt the nearest header just below it.
        for mi, mname in markers:
            if mi >= idx:
                return mname if mi - idx <= 80 else None
    return disc


# ---------------------------------------------------------------------------
# modern detector: Deathwatch / Only War / Black Crusade (inline fields)
# ---------------------------------------------------------------------------
_STOP_UP = re.compile(
    r"^(Description|Sustained|Subtype|Opposed|Action|Focus\s+Power)\s*:", re.IGNORECASE)


def _name_above_modern(lines: List[str], action_idx: int) -> Optional[int]:
    """Find a modern power's name.

    Anchor on the block's ``Value:`` line, not on ``Action:`` — Only War / Black
    Crusade wrap the (long, sometimes one-word-per-line) Prerequisites value
    BELOW Value, so anchoring on Value keeps that mess out of the name search.
    From Value we skip only the Alternate Names line and its wrapped value to
    reach the name. Deathwatch powers carry no Value line; there the name sits
    directly above Action.
    """
    # 1) locate this block's Value line just above Action (past Prerequisites+wraps)
    v = None
    j, hops = action_idx - 1, 0
    while j >= 0 and hops < 12:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            j -= 1
            continue
        if VALUE.match(s):
            v = j
            break
        if _STOP_UP.match(s):          # hit the previous power's fields — no Value here
            break
        j -= 1
        hops += 1
    top = v if v is not None else action_idx

    # 2) from the block top, skip Alternate Names (+ its wrapped value) to the name
    j, hops = top - 1, 0
    while j >= 0 and hops < 8:
        hops += 1
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            j -= 1
            continue
        if MODERN_LEADFIELD.match(s):
            j -= 1
            continue
        kk, nb, wrapped = j - 1, 0, False
        while kk >= 0 and nb < 4:
            ss = lines[kk].strip()
            if ss == "" or PAGE.search(lines[kk]):
                kk -= 1
                continue
            nb += 1
            if ALT_NAMES.match(ss):
                wrapped = True
                break
            if MODERN_LEADFIELD.match(ss) or _STOP_UP.match(ss):
                break
            kk -= 1
        if wrapped:
            j = kk - 1
            continue
        return j if _plausible_name(s) else None
    return None


def make_modern_detector(disc_matchers, reject_bulleted=False):
    def detect(lines: List[str], pages: List[int], book: str) -> List[Power]:
        n = len(lines)
        markers = _markers(lines, disc_matchers, reject_bulleted)
        starts: List[Tuple[int, int]] = []
        used = set()
        for i, ln in enumerate(lines):
            m = ACTION.match(ln.strip())
            if not m or not ACTION_VALUE.match(m.group(1).strip()):
                continue
            nidx = _name_above_modern(lines, i)
            if nidx is None or nidx in used:
                continue
            used.add(nidx)
            starts.append((nidx, i))
        starts.sort()

        out: List[Power] = []
        for k, (nidx, aidx) in enumerate(starts):
            end = starts[k + 1][0] if k + 1 < len(starts) else min(n, nidx + 55)
            end = min(end, nidx + 55)
            p = Power(name=_norm_name(lines[nidx].strip()), book=book,
                      page=pages[nidx], start=nidx, end=end,
                      discipline=_discipline_at(markers, nidx))
            desc_idx = None
            for r in range(nidx + 1, end):
                s = lines[r].strip()
                if s == "" or PAGE.search(lines[r]):
                    continue
                dm = DESCRIPTION.match(s)
                if dm:
                    desc_idx = r
                    break
                for rx, attr in ((VALUE, "value"), (PREREQ, "prerequisites"),
                                 (ACTION, "action"), (OPPOSED, "opposed"),
                                 (FOCUS_POWER, "focus_power"), (RANGE, "range"),
                                 (SUSTAINED, "sustained"), (SUBTYPE, "subtype")):
                    g = rx.match(s)
                    if g and getattr(p, attr) is None:
                        setattr(p, attr, re.sub(r"\s+", " ", g.group(1)).strip())
                        break
            # opposed: explicit field, else read it off the Focus Power line
            if p.opposed is None and p.focus_power:
                p.opposed = "Yes" if re.search(r"oppos", p.focus_power, re.I) else "No"
            elif p.opposed:
                p.opposed = "Yes" if re.search(r"^y", p.opposed.strip(), re.I) else "No"
            if desc_idx is not None:
                p.effect = _first_sentence(lines[desc_idx:end])
            # a real psychic power has both Range and Sustained
            if p.range and p.sustained:
                out.append(p)

        best: Dict[str, Power] = {}
        for p in out:
            best.setdefault(p.name.lower(), p)
        return sorted(best.values(), key=lambda x: x.start)

    return detect


# ---------------------------------------------------------------------------
# Rogue Trader detector: inline Value / Prerequisites / Focus Power Test / Range
# ---------------------------------------------------------------------------
def make_rt_detector(disc_matchers):
    def detect(lines: List[str], pages: List[int], book: str) -> List[Power]:
        n = len(lines)
        markers = _markers(lines, disc_matchers, reject_bulleted=False)
        starts: List[Tuple[int, int]] = []
        used = set()
        for i, ln in enumerate(lines):
            if not VALUE.match(ln.strip()):
                continue
            # confirm this is a technique block: Prereq or Focus Power Test just below
            ok = False
            seen = 0
            for r in range(i + 1, min(n, i + 7)):
                s = lines[r].strip()
                if s == "" or PAGE.search(lines[r]):
                    continue
                seen += 1
                if PREREQ.match(s) or FOCUS_POWER_TEST.match(s):
                    ok = True
                    break
                if seen >= 4:
                    break
            if not ok:
                continue
            # name = first real line above Value
            j = i - 1
            while j >= 0 and (lines[j].strip() == "" or PAGE.search(lines[j])):
                j -= 1
            if j < 0 or j in used or not _plausible_name(lines[j].strip()):
                continue
            used.add(j)
            starts.append((j, i))
        starts.sort()

        out: List[Power] = []
        for k, (nidx, vidx) in enumerate(starts):
            end = starts[k + 1][0] if k + 1 < len(starts) else min(n, nidx + 45)
            end = min(end, nidx + 45)
            p = Power(name=_norm_name(lines[nidx].strip()), book=book,
                      page=pages[nidx], start=nidx, end=end,
                      discipline=_discipline_at(markers, nidx))
            last_field = vidx
            for r in range(nidx + 1, end):
                s = lines[r].strip()
                if s == "" or PAGE.search(lines[r]):
                    continue
                matched = False
                for rx, attr in ((VALUE, "value"), (PREREQ, "prerequisites"),
                                 (FOCUS_POWER_TEST, "focus_power"), (RANGE, "range")):
                    g = rx.match(s)
                    if g and getattr(p, attr) is None:
                        setattr(p, attr, re.sub(r"\s+", " ", g.group(1)).strip())
                        last_field = r
                        matched = True
                        break
                if not matched and r > vidx + 1:
                    # prose has begun
                    break
            if p.focus_power:
                p.opposed = "Yes" if re.search(r"oppos", p.focus_power, re.I) else "No"
            p.effect = _first_sentence(lines[last_field + 1:end])
            if p.value or p.focus_power:
                out.append(p)

        best: Dict[str, Power] = {}
        for p in out:
            best.setdefault(p.name.lower(), p)
        return sorted(best.values(), key=lambda x: x.start)

    return detect


# ---------------------------------------------------------------------------
# Dark Heresy detector: alternating Threshold / Focus Time / Sustained / Range
# ---------------------------------------------------------------------------
def make_dh_detector(disc_matchers):
    def detect(lines: List[str], pages: List[int], book: str) -> List[Power]:
        n = len(lines)
        markers = _markers(lines, disc_matchers, reject_bulleted=False)
        starts: List[Tuple[int, int]] = []
        used = set()
        for i, ln in enumerate(lines):
            if not DH_THRESHOLD.match(ln.strip()):
                continue
            # value on the next non-blank line must be numeric (rejects the format box)
            v = i + 1
            while v < n and (lines[v].strip() == "" or PAGE.search(lines[v])):
                v += 1
            if v >= n or not re.match(r"^\d{1,3}\b", lines[v].strip()):
                continue
            # name = first real line above Threshold
            j = i - 1
            while j >= 0 and (lines[j].strip() == "" or PAGE.search(lines[j])):
                j -= 1
            if j < 0 or j in used or not _plausible_name(lines[j].strip()):
                continue
            used.add(j)
            starts.append((j, i))
        starts.sort()

        out: List[Power] = []
        for k, (nidx, tidx) in enumerate(starts):
            end = starts[k + 1][0] if k + 1 < len(starts) else min(n, nidx + 45)
            end = min(end, nidx + 45)
            p = Power(name=_norm_name(lines[nidx].strip()), book=book,
                      page=pages[nidx], start=nidx, end=end,
                      discipline=_discipline_at(markers, nidx))
            j = tidx
            last = tidx
            while j < min(n, tidx + 20):
                s = lines[j].strip()
                hit = None
                for rx, attr in DH_LABELS:
                    if rx.match(s):
                        hit = attr
                        break
                if hit:
                    v = j + 1
                    while v < n and (lines[v].strip() == "" or PAGE.search(lines[v])):
                        v += 1
                    if v < n and getattr(p, hit) is None \
                            and not DH_ANY_LABEL.match(lines[v].strip()):
                        setattr(p, hit, re.sub(r"\s+", " ", lines[v].strip()))
                        last = v
                    j = v
                    continue
                if p.range and j > tidx + 2 and not DH_ANY_LABEL.match(s):
                    break
                j += 1
            p.effect = _first_sentence(lines[last + 1:end])
            if p.threshold and p.range:
                out.append(p)

        best: Dict[str, Power] = {}
        for p in out:
            best.setdefault(p.name.lower(), p)
        return sorted(best.values(), key=lambda x: x.start)

    return detect


# ---------------------------------------------------------------------------
# per-book discipline vocabularies
# ---------------------------------------------------------------------------
def _const(c):
    return lambda m: c


def _grp_norm(m):
    return _norm_name(m.group(1))


def _grp_title(m):
    return m.group(1).title()


DH_DISC = [
    (re.compile(r"(?i)^(minor psychic powers|minor powers)\s*$"), _const("Minor Powers")),
    (re.compile(r"(?i)^biomancy\s*$"), _const("Biomancy")),
    (re.compile(r"(?i)^divination\s*$"), _const("Divination")),
    (re.compile(r"(?i)^pyromancy\s*$"), _const("Pyromancy")),
    (re.compile(r"(?i)^telekinetics\s*$"), _const("Telekinesis")),
    (re.compile(r"(?i)^telepathy\s*$"), _const("Telepathy")),
]
RT_DISC = [
    (re.compile(r"(?i)^the\s+([A-Za-z]+)\s+discipline\s*$"), _grp_norm),
]
DW_DISC = [
    (re.compile(r"(?i)^(telepathy|divination|codex)\s+powers\s*$"), _grp_norm),
    (re.compile(r"(?i)^(blood angels|dark angels|space wolves|storm wardens?|"
                r"ultramarines)(?:\s+powers)?\s*$"), _grp_norm),
]
OW_DISC = [
    (re.compile(r"^(BIOMANCY|DIVINATION|PYROMANCY|TELEKINESIS|TELEPATHY)\s*$"), _grp_title),
]
BC_DISC = [
    (re.compile(r"^(UNALIGNED|NURGLE|SLAANESH|TZEENTCH|EXALTED)\s+POWERS\s*$"), _grp_title),
    (re.compile(r"^(TELEPATHY|TELEKINESIS|DIVINATION)\s*$"), _grp_title),
]


# ---------------------------------------------------------------------------
# sources
# ---------------------------------------------------------------------------
@dataclass
class Source:
    key: str
    book: str
    path: Path
    citation: str
    make: Callable[[], Callable[[List[str], List[int], str], List[Power]]]
    coverage: str = "pending"
    lines: List[str] = field(default_factory=list)
    powers: List[Power] = field(default_factory=list)


_W = "Warhammer/40K Roleplay"
SOURCES: List[Source] = [
    Source("dark_heresy", "Dark Heresy — Core Rulebook (WH40K Roleplay)",
           Path(f"{_W}/Dark Heresy/Rulebooks/Dark Heresy - Core Rulebook.pdf.md"),
           "Dark Heresy Core Rulebook (Fantasy Flight Games / Black Industries)",
           lambda: make_dh_detector(DH_DISC)),
    Source("rogue_trader", "Rogue Trader — Core Rulebook (WH40K Roleplay)",
           Path(f"{_W}/Rogue Trader/Rulebooks/"
                "Rogue Trader - Core Rulebook (updated with 1.4 errata).md"),
           "Rogue Trader Core Rulebook, 1.4 errata (Fantasy Flight Games)",
           lambda: make_rt_detector(RT_DISC)),
    Source("deathwatch", "Deathwatch — Core Rulebook (WH40K Roleplay)",
           Path(f"{_W}/Deathwatch/Rulebooks/Deathwatch - Core Rulebook.md"),
           "Deathwatch Core Rulebook (Fantasy Flight Games)",
           lambda: make_modern_detector(DW_DISC)),
    Source("only_war", "Only War — Core Rulebook (WH40K Roleplay)",
           Path(f"{_W}/Only War/Rulebooks/Only War - Core Rulebook.md"),
           "Only War Core Rulebook (Fantasy Flight Games)",
           lambda: make_modern_detector(OW_DISC, reject_bulleted=True)),
    Source("black_crusade", "Black Crusade — Core Rulebook (WH40K Roleplay)",
           Path(f"{_W}/Black Crusade/Rulebooks/Black Crusade - Core Rulebook.md"),
           "Black Crusade Core Rulebook (Fantasy Flight Games)",
           lambda: make_modern_detector(BC_DISC)),
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
    return [Source(s.key, s.book, s.path, s.citation, s.make) for s in SOURCES]


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
            src.powers = src.make()(src.lines, pages, src.book)
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
            nm = p.name.lower()
            if nm == q:
                exact.append((src, p))
            elif q in nm:
                partial.append((src, p))
        return exact if exact else partial


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# WARHAMMER 40,000 ROLEPLAY — PSYCHIC POWER INDEX — The New Path",
        "",
        "**Generated by `scripts/wh40krp_psychic_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** **Warhammer 40,000 Roleplay** (the Fantasy Flight",
        "Games d100 line: Dark Heresy, Rogue Trader, Deathwatch, Only War, Black",
        "Crusade) — a DIFFERENT game system from the D&D/GURPS layers. Every row is",
        "stamped `system: WH40K Roleplay`; a power is SOURCE MATERIAL for the",
        "system-translator skill. A psyker manifests a power with a Focus Power",
        "Test; powers are grouped by Discipline. `action` is the Focus Power Action",
        "(Dark Heresy lists it as Focus Time). Discipline labels for the two-column",
        "Only War / Black Crusade PDFs are best-effort at section boundaries; the",
        "mechanical fields are exact and cited to book + PDF page.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.powers)
        parsed_well += sum(1 for p in src.powers if p.quick_fields() >= 3)
        sources_out.append({"key": src.key, "book": src.book, "system": SYSTEM,
                            "citation": src.citation, "coverage": src.coverage,
                            "powers": [asdict(p) for p in src.powers]})
        discs = sorted({p.discipline for p in src.powers if p.discipline})
        md.append(f"## {src.book} — {len(src.powers)} powers  *(system: {SYSTEM})*")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*  ")
        md.append(f"*Disciplines: {', '.join(discs) if discs else '—'}.*")
        md.append("")
        if src.powers:
            md.append("| Power | Discipline | Action | Opposed | Range | Sustained | "
                      "Value | Page | Effect |")
            md.append("|---|---|---|---|---|---|---|---|---|")
            for p in src.powers:
                eff = (p.effect or "").replace("|", "\\|")
                if len(eff) > 90:
                    eff = eff[:88].rstrip() + "…"
                md.append(
                    f"| {p.name} | {p.discipline or '—'} | {p.action or '—'} | "
                    f"{p.opposed or '—'} | {p.range or '—'} | {p.sustained or '—'} | "
                    f"{p.value or '—'} | {p.page if p.page is not None else '—'} | {eff} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/wh40krp_psychic_harvest.py",
                    "system": SYSTEM, "corpus": str(corpus.base),
                    "total_powers": total, "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str],
                  out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 6:
        print(f"'{name}' matches {len(hits)} powers; narrow with the exact name:")
        for src, p in hits[:20]:
            print(f"  {p.name}   [{p.book}, p.{p.page}]")
        return 1
    packets = []
    for src, p in hits:
        body = [ln for ln in src.lines[p.start:p.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "wh40krp-psychic-for-translation",
            "instructions": ("A Warhammer 40,000 Roleplay psychic power "
                             "(system: WH40K Roleplay). Feed to the system-translator "
                             "skill for the paired 3.5e AND GURPS treatment. The "
                             "raw_block is born-digital / OCR text."),
            "name": p.name, "system": SYSTEM,
            "source": {"book": p.book, "pdf_page": p.page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [p.start + 1, p.end], "citation": src.citation},
            "parsed": {k: v for k, v in asdict(p).items()
                       if k in ("discipline", "action", "opposed", "range",
                                "sustained", "subtype", "focus_power", "threshold",
                                "value", "prerequisites", "effect") and v},
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
# fixtures + selftest
# ---------------------------------------------------------------------------
FIXTURE_MODERN = """## [PDF page 231]
BIOMANCY
ENDURANCE
Value: 300xp
Prerequisites: Toughness 30+
Action: Half Action
Focus Power: Difficult (-10) Willpower Test
Range: 3 metres x Psy Rating radius
Sustained: No
Subtype: Concentration
Description: Extending his will over his allies, the psyker reaches into their
bodies to mend their flesh. Psykers trained in this power turn the tides of battle.
LIFE LEECH
Value: 400xp
Prerequisites: Enfeeble, Toughness 40+
Action: Full Action
Focus Power: Difficult (-10) Opposed Willpower Test
Range: 10 metres x Psy Rating
Sustained: Free Action
Subtype: Attack, Concentration
Description: The psyker latches on to his target's life force and tears it from
the hapless victim's body.
"""

FIXTURE_BC = """## [PDF page 236]
UNALIGNED POWERS
These powers are the basic list of powers, not linked to any Chaos God.
ABHORRENT WARD [CORRUPTION]
Alternate Names: Repulsive Shield, Mantle of Esh'raiik,
Bulwark of Detestation
Value: 300xp
Prerequisites: Corruption 30+, Psy Rating 4
Action: Half Action
Focus Power: Challenging (+0) Corruption Test
Range: Self
Sustained: Half Action
Subtype: Concentration
Description: The Sorcerer's tainted soul draws to it the denizens of the warp.
"""

FIXTURE_DH = """## [PDF page 166]
Minor Powers
Call Creatures
Threshold:
9
Focus Time:
Full Action
Sustained:
No
Range:
1 km radius
You call a number of simple-minded creatures within range to travel to your
location. Creatures called depend on the environment.
Chameleon
Threshold:
7
Focus Time:
Half Action
Sustained:
Yes
Range:
You
You cause reality to blur around you, distorting your image.
"""

FIXTURE_RT = """## [PDF page 164]
The TelepAThy Discipline
Activation Time: Free Action.
Maintainable: Yes.
Range: 10 meters x Psy Rating
Focus Power Test: No
Power Scale: At Psy Rating 1-2, the psyker can only send verbal communications.
Mind Link
Value: 200 xp
Prerequisites: None
Focus Power Test: Willpower
Range: 1km x Psy Rating
A successful Focus Power Test allows the psyker to create a telepathic link.
Terrify
Value: 200 xp
Prerequisites: None
Focus Power Test: Opposed Willpower
Range: 30m x Psy Rating
The psyker projects an aura of raw terror into the minds of his foes.
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    # -- modern fixture (Only War style) -----------------------------------
    det = make_modern_detector(OW_DISC)
    lines = FIXTURE_MODERN.splitlines()
    ps = det(lines, _pages_for(lines), "Only War — Core Rulebook (WH40K Roleplay)")
    names = [p.name for p in ps]
    if names != ["Endurance", "Life Leech"]:
        failures.append(f"modern fixture names {names}, wanted Endurance/Life Leech")
    else:
        en = ps[0]
        if (en.action, en.range, en.sustained, en.opposed, en.discipline) != \
                ("Half Action", "3 metres x Psy Rating radius", "No", "No", "Biomancy"):
            failures.append(f"Endurance parsed "
                            f"{(en.action, en.range, en.sustained, en.opposed, en.discipline)}")
        if en.system != SYSTEM:
            failures.append("system must be 'WH40K Roleplay'")
        if not (en.effect and en.effect.startswith("Extending his will")):
            failures.append(f"Endurance effect {en.effect!r}")
        ll = ps[1]
        if ll.opposed != "Yes":
            failures.append(f"Life Leech opposed {ll.opposed!r} (folded in Focus Power)")
        if ll.subtype != "Attack, Concentration":
            failures.append(f"Life Leech subtype {ll.subtype!r}")

    # -- Black Crusade fixture (Alternate Names + [tag] name walk) ----------
    detb = make_modern_detector(BC_DISC)
    lb = FIXTURE_BC.splitlines()
    pb = detb(lb, _pages_for(lb), "Black Crusade — Core Rulebook (WH40K Roleplay)")
    if [p.name for p in pb] != ["Abhorrent Ward"]:
        failures.append(f"BC fixture names {[p.name for p in pb]}, wanted Abhorrent Ward")
    elif (pb[0].discipline, pb[0].range, pb[0].sustained) != ("Unaligned", "Self", "Half Action"):
        failures.append(f"Abhorrent Ward parsed "
                        f"{(pb[0].discipline, pb[0].range, pb[0].sustained)}")

    # -- Dark Heresy fixture (alternating labels) --------------------------
    detd = make_dh_detector(DH_DISC)
    ld = FIXTURE_DH.splitlines()
    pd = detd(ld, _pages_for(ld), "Dark Heresy — Core Rulebook (WH40K Roleplay)")
    if [p.name for p in pd] != ["Call Creatures", "Chameleon"]:
        failures.append(f"DH fixture names {[p.name for p in pd]}")
    else:
        cc = pd[0]
        if (cc.threshold, cc.action, cc.sustained, cc.range, cc.discipline) != \
                ("9", "Full Action", "No", "1 km radius", "Minor Powers"):
            failures.append(f"Call Creatures parsed "
                            f"{(cc.threshold, cc.action, cc.sustained, cc.range, cc.discipline)}")
        if not (cc.effect and cc.effect.startswith("You call a number")):
            failures.append(f"Call Creatures effect {cc.effect!r}")

    # -- Rogue Trader fixture ----------------------------------------------
    detr = make_rt_detector(RT_DISC)
    lr = FIXTURE_RT.splitlines()
    pr = detr(lr, _pages_for(lr), "Rogue Trader — Core Rulebook (WH40K Roleplay)")
    if [p.name for p in pr] != ["Mind Link", "Terrify"]:
        failures.append(f"RT fixture names {[p.name for p in pr]}, wanted Mind Link/Terrify")
    else:
        ml = pr[0]
        if (ml.value, ml.focus_power, ml.range, ml.opposed, ml.discipline) != \
                ("200 xp", "Willpower", "1km x Psy Rating", "No", "Telepathy"):
            failures.append(f"Mind Link parsed "
                            f"{(ml.value, ml.focus_power, ml.range, ml.opposed, ml.discipline)}")
        if pr[1].opposed != "Yes":
            failures.append(f"Terrify opposed {pr[1].opposed!r} (from Opposed Willpower)")

    # -- live corpus checks -------------------------------------------------
    if base.is_dir() and any((base / s.path).exists() for s in SOURCES):
        corpus = Corpus(base, _fresh_sources())
        by_book = {s.key: s.powers for s in corpus.sources}
        total = sum(len(v) for v in by_book.values())
        if total < 220:
            failures.append(f"only {total} WH40KRP powers indexed; expected > 220")
        for key, floor in (("dark_heresy", 65), ("rogue_trader", 25),
                           ("deathwatch", 40), ("only_war", 30), ("black_crusade", 45)):
            got = len(by_book.get(key, []))
            if got < floor:
                failures.append(f"{key}: {got} powers, expected >= {floor}")
        # known powers present
        allnames = {p.name.lower() for v in by_book.values() for p in v}
        for want in ("call creatures", "smite", "doombolt"):
            if want not in allnames:
                failures.append(f"expected a power named '{want}' somewhere")
        # action + range actually parsed across the modern/DH books
        for key in ("deathwatch", "only_war", "black_crusade", "dark_heresy"):
            ps2 = by_book.get(key, [])
            if ps2 and sum(1 for p in ps2 if p.action and p.range) < max(10, len(ps2) // 2):
                failures.append(f"{key}: action/range parsed on < half of powers")
        # disciplines resolved on most powers of a clean book
        dw = by_book.get("deathwatch", [])
        if dw and sum(1 for p in dw if p.discipline) < len(dw) * 0.7:
            failures.append("deathwatch: discipline resolved on < 70% of powers")
    else:
        print("  [SKIP] WH40K Roleplay extractions not found — fixture checks only")

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
        found = sorted({(p.name, p.book, p.page or -1, p.discipline or "—")
                        for _, p in corpus.all_powers(args.book) if q in p.name.lower()})
        for nm, bk, page, disc in found:
            loc = bk if page < 0 else f"{bk}, p.{page}"
            print(f"  {nm}   [{disc}; {loc}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.powers for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.powers):4d} powers" if src.powers else "   0 powers"
        print(f"  {src.book:52s} {status}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} WH40K Roleplay psychic powers across "
          f"{sum(1 for s in corpus.sources if s.powers)} book(s). (system: {SYSTEM})")
    print(f"well-parsed (>=3 quick fields): {parsed_well}")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
