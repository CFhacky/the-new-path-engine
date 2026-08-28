#!/usr/bin/env python3
"""wh40krp_adversary_harvest.py — collate Warhammer 40,000 Roleplay adversaries.

THE PROCESS (Chad, 2026-08-28): the reference layer welcomes OTHER game systems
as long as they are CLEARLY LABELLED by system, so the translator tools know
what they are looking at. This is the **Warhammer 40,000 Roleplay** (Fantasy
Flight d100) adversary / bestiary index — NPC, xenos, daemon, and creature stat
blocks from Dark Heresy, Rogue Trader, Deathwatch, and Black Crusade. Every row
is stamped `"system": "WH40K Roleplay"` so nothing here is ever mistaken for the
campaign's native 3.5e / GURPS RAW.

    reference/wh40krp_adversary_index.json  — every adversary: name, the nine
                                              characteristics (WS BS S T Ag Int
                                              Per WP Fel, plus Black Crusade's
                                              Infamy), movement, wounds, and
                                              short skills/talents/traits/armour/
                                              weapons/gear summaries; book + page
    reference/wh40krp_adversary_index.md    — the same index, for human eyes

The raw text stays on I:\\Sourcebooks; `--export` emits a TRANSLATOR-READY
packet — a 40kRP block the system-translator skill converts to the hybrid's
3.5e + GURPS pair (BOTH still required in that skill's output).

WORKFLOW
    python wh40krp_adversary_harvest.py                    # (re)build the index
    python wh40krp_adversary_harvest.py --search "ork"     # find candidates
    python wh40krp_adversary_harvest.py --export "Purestrain Genestealer"
    python wh40krp_adversary_harvest.py --selftest

GOVERNING SOURCES
    I:\\Sourcebooks\\_text\\Warhammer\\40K Roleplay\\ — the adversary-dense books.
    A 40kRP adversary is a NAME then a PROFILE of nine characteristics as
    percentages, WS BS S T Ag Int Per WP Fel, then Movement, Wounds, Skills,
    Talents, Traits, Armour, Weapons, Gear. The books lay the profile out five
    ways, so five detectors anchor on it:

      * VERTICAL (Creatures Anathema, Mark of the Xenos, Rogue Trader Core &
        supplements, the Koronus Bestiary, the Deathwatch & Dark Heresy
        supplements): a bare `WS` label line heads the profile, the labels
        run down the page (`WS / BS / S / T / Ag / Int Per WP Fel`), the name
        sits on the line above, and the values run down the page below —
        Unnatural bonuses printed in (parentheses) lead the value run and are
        dropped, leaving the nine characteristics. Movement/Move/Speed, Wounds,
        Corruption/Insanity Points, and the Skills/… lines follow.

      * PROFILE-ROW (Dark Heresy Core, the Inquisitor's Handbook, Deathwatch
        Core): the name sits on an `X Profile` line, the labels are tab-laid,
        and the nine values sit on ONE whitespace-separated row (OCR may append
        `*` footnote marks).

      * INFAMY-ROW (Black Crusade Core + the Tomes of Blood/Excess/Fate): the
        name sits above the profile, the values are ONE whitespace-separated row
        of TEN (Black Crusade adds Infamy as a tenth characteristic) with a
        trailing `- -`, and the labels follow below.

      * INVERTED-VERTICAL (Only War: Enemies of the Imperium): the vertical
        profile is printed UPSIDE-DOWN — name on top, the nine VALUES run down
        next, and only THEN the WS..Fel labels. The OCR drops the parentheses
        around Unnatural bonuses, leaving them as bare LEADING numbers (dropped,
        keeping the nine nearest the labels), and a `## [PDF page N]` marker may
        fall inside a block — so the detector walks THROUGH page markers to
        stitch a split value run or page-separated traits back onto one creature
        (the citation records the page the NAME sits on).

      * MERGED-VERTICAL (Dark Heresy: Blood of Martyrs): ordinary top-down
        vertical, but the OCR merges several values onto one line ("40 – –"), so
        each value line is tokenised before the nine are read off.

    A configured source whose file is missing prints NO COVERAGE. Garbage names
    (section headers, prose, stat fragments) are filtered out. A value run that
    cannot be resolved cleanly to nine characteristics is SET ASIDE (reported on
    SOFT_SKIPS), never guessed. The PDFs stand behind every extraction.
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
OUT_JSON = REPO / "reference" / "wh40krp_adversary_index.json"
OUT_MD = REPO / "reference" / "wh40krp_adversary_index.md"
SYSTEM = "WH40K Roleplay"

PAGE = re.compile(r"\[PDF page (\d+)\]")

# The nine 40kRP characteristics, in profile order. Black Crusade adds a tenth,
# Infamy (Inf), captured separately.
CHAR_KEYS = ["ws", "bs", "s", "t", "ag", "int", "per", "wp", "fel"]
CHAR_LABELS = {"ws", "bs", "s", "t", "ag", "int", "per", "wp", "fel", "inf"}

# A single vertical value line: a characteristic value, an Unnatural bonus in
# (parentheses), or a dash meaning "no score" (— / – / -- / - -). OCR footnote
# marks (*) and stray whitespace are tolerated.
V_PAREN = re.compile(r"^\(\s*(\d{1,3})\s*\)\*?$")          # (6) — Unnatural bonus
V_NUM = re.compile(r"^(\d{1,3})\*?$")                       # 45 / 05 / 45*
V_DASH = re.compile(r"^[\s\u2014\u2013\u2012-]*[\u2014\u2013\u2012-][\s\u2014\u2013\u2012-]*$")

# A profile label line (any run of the characteristic labels, alone on a line):
# "WS", "bS", "Int Per WP Fel", "wS BS", "ag Int Per wP fel", "WP Fel Inf".
def _is_label_line(s: str) -> bool:
    toks = s.replace("\t", " ").split()
    return bool(toks) and all(t.strip(".").lower() in CHAR_LABELS for t in toks)


# Keyword lines that end the profile-value run / open the trailing block.
STAT_KEYWORD = re.compile(
    r"^\s*(Movement|Move|Speed|Wounds?|Corruption Points?|Insanity Points?|"
    r"Total\s*TB|Skills?|Talents?|Traits?|Armou?r|Weapons?|Gear|Special Rules?|"
    r"Mutations?|Malignancies|Disorders?|Bio-?morphs?)\b", re.IGNORECASE)

# Trailing threat/role tag on a name line: (Troops)/(Elite)/(Master)/(Troop)/
# (Minion). The Only War and Rogue Trader supplements add the (Minion) tier.
ROLE_TAG = re.compile(r"\(\s*(Troops?|Elite|Master|Minion)\s*\)\s*$", re.IGNORECASE)

# A name that EXACTLY equals a stat label or a standalone section-header word is
# a fragment, not a creature — rejected. (Whole-string match, case-insensitive.)
NAME_REJECT_EXACT = {
    "ws", "bs", "s", "t", "ag", "int", "per", "wp", "fel", "inf", "profile",
    "movement", "move", "speed", "wounds", "wound", "skills", "skill", "talents",
    "talent", "traits", "trait", "armour", "armor", "weapons", "weapon", "gear",
    "corruption points", "insanity points", "total tb", "special rules",
    "mutations", "malignancies", "disorders", "biomorphs", "chapter", "contents",
    "appendix", "index", "introduction", "adversaries", "bestiary", "engagement",
    "combat", "tactics", "combat tactics", "objectives", "rewards", "overview",
    "background", "history", "description", "appearance", "summary", "abilities",
    "actions", "reactions", "options", "example", "profiles", "the end",
    "game master", "notes", "note", "optional", "adventure seeds", "gm advice",
}
# Header phrases that begin a non-name line — rejected as a prefix.
NAME_REJECT_PREFIX = re.compile(
    r"^(Chapter\b|Appendix\b|Adventure Seeds?\b|Special Rules?\b|Combat Tactics\b|"
    r"GM Advice\b|Game Master\b|Using |The following\b|Optional Rules?\b|"
    r"Designer'?s? Note|New Rules?\b|Skills? and\b|Table \d)", re.IGNORECASE)


def _smart_title(s: str) -> str:
    """Capitalise OCR-lowercased names ('broadside battlesuit' -> 'Broadside
    Battlesuit') while preserving tokens that already carry capitals ('XV-88',
    'big Mek Wurrzog' -> 'Big Mek Wurrzog')."""
    out = []
    for w in s.split():
        out.append(w[:1].upper() + w[1:] if w and w.islower() else w)
    return " ".join(out)


_LIGATURES = {"ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl",
              "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "st", "ﬆ": "st"}


def _deligature(s: str) -> str:
    for lig, rep in _LIGATURES.items():
        s = s.replace(lig, rep)
    return s


def _clean_name(raw: str) -> Tuple[Optional[str], Optional[str]]:
    """Return (name, role) or (None, None) if the line is not a plausible name.
    Strips a trailing 'Profile' word and a (Troops)/(Elite)/(Master) role tag."""
    s = _deligature(re.sub(r"\s+", " ", raw).strip())
    # Strip a trailing 'Profile' label. Several later books' OCR splits the "fi"
    # ligature, printing it as 'Profi le' / 'Profi Le' — catch that variant too.
    s = re.sub(r"\bProfi\s*le\s*$", "", s, flags=re.IGNORECASE).strip()
    role = None
    mt = ROLE_TAG.search(s)
    if mt:
        role = mt.group(1).title()
        s = ROLE_TAG.sub("", s).strip()
    s = s.strip(" \u2014\u2013-\u2020\u2021*").strip()
    if not s or not (2 <= len(s) <= 44):
        return None, None
    if s.isdigit() or s.endswith((".", ",", ";", ":")):
        return None, None
    if s.lower() in NAME_REJECT_EXACT or NAME_REJECT_PREFIX.match(s) or _is_label_line(s):
        return None, None
    letters = sum(c.isalpha() for c in s)
    if letters < max(3, len(s) // 2):        # mostly punctuation/digits -> reject
        return None, None
    if len(s.split()) > 7:                    # a sentence, not a name
        return None, None
    return _smart_title(s), role


@dataclass
class Adversary40k:
    name: str
    book: str
    page: Optional[int]
    start: int
    end: int
    system: str = SYSTEM
    role: Optional[str] = None
    ws: Optional[str] = None
    bs: Optional[str] = None
    s: Optional[str] = None
    t: Optional[str] = None
    ag: Optional[str] = None
    int: Optional[str] = None       # noqa: A003 — 40kRP characteristic key is "int"
    per: Optional[str] = None
    wp: Optional[str] = None
    fel: Optional[str] = None
    inf: Optional[str] = None       # Black Crusade only (Infamy)
    movement: Optional[str] = None
    wounds: Optional[str] = None
    skills: Optional[str] = None
    talents: Optional[str] = None
    traits: Optional[str] = None
    armour: Optional[str] = None
    weapons: Optional[str] = None
    gear: Optional[str] = None

    def quick_fields(self) -> int:
        """How many of the nine characteristics parsed to a number."""
        return sum(1 for k in CHAR_KEYS
                   if (getattr(self, k) or "").replace("\u2014", "").isdigit())


# ── shared value parsing ────────────────────────────────────────────────────

def _apply_profile(a: Adversary40k, values: List[str], inf: Optional[str] = None) -> int:
    """Set the nine characteristics from an ordered value list; return the count
    of numeric ones. A dash value is stored as '—'."""
    for key, val in zip(CHAR_KEYS, values):
        setattr(a, key, val)
    if inf is not None:
        a.inf = inf
    return a.quick_fields()


def _tokens_to_values(tokens: List[str]) -> List[str]:
    """Drop Unnatural-bonus (paren) tokens; keep numbers and dashes in order."""
    out: List[str] = []
    for kind, val in tokens:
        if kind == "paren":
            continue
        out.append(val)
    return out


def _classify(tok: str) -> Optional[Tuple[str, str]]:
    """Classify one whitespace-delimited token: ('paren', n) Unnatural bonus,
    ('val', n) characteristic, ('dash', '—') no-score, or None."""
    tok = tok.strip()
    m = V_PAREN.match(tok)
    if m:
        return "paren", m.group(1)
    m = V_NUM.match(tok)
    if m:
        return "val", m.group(1)
    if V_DASH.match(tok):
        return "dash", "\u2014"
    return None


def _extract_extras(a: Adversary40k, body: List[str]) -> None:
    """Fill movement/wounds/skills/talents/traits/armour/weapons/gear from the
    trailing lines, each captured as a short one-line summary."""
    field_map = [
        (re.compile(r"^\s*(?:Movement|Move|Speed)\s*:\s*(.+)$", re.I), "movement"),
        (re.compile(r"^\s*Wounds?\s*:\s*(.+)$", re.I), "wounds"),
        (re.compile(r"^\s*Skills?\s*:\s*(.+)$", re.I), "skills"),
        (re.compile(r"^\s*Talents?\s*:\s*(.+)$", re.I), "talents"),
        (re.compile(r"^\s*Traits?\s*:\s*(.+)$", re.I), "traits"),
        (re.compile(r"^\s*Armou?r\s*:\s*(.+)$", re.I), "armour"),
        (re.compile(r"^\s*Weapons?\s*:\s*(.+)$", re.I), "weapons"),
        (re.compile(r"^\s*Gear\s*:\s*(.+)$", re.I), "gear"),
    ]
    n = len(body)
    for i, raw in enumerate(body):
        line = raw.strip()
        if not line:
            continue
        for rx, attr in field_map:
            if getattr(a, attr) is not None:
                continue
            m = rx.match(line)
            if not m:
                continue
            # gather continuation lines until the next keyworded stat line
            chunk = [m.group(1).strip()]
            j = i + 1
            while j < n and len(" ".join(chunk)) < 400:
                nxt = body[j].strip()
                if not nxt or PAGE.search(body[j]):
                    break
                if STAT_KEYWORD.match(nxt) or _is_label_line(nxt):
                    break
                chunk.append(nxt)
                j += 1
            text = _deligature(re.sub(r"\s+", " ", " ".join(chunk)).strip().rstrip("."))
            if len(text) > 240:
                text = text[:237].rstrip() + "\u2026"
            setattr(a, attr, text)
            break


# ── detector A: VERTICAL profile (labels & values run down the page) ─────────

def _name_above(lines: List[str], ws_idx: int) -> Optional[Tuple[int, str, Optional[str]]]:
    """Nearest plausible name on the line(s) above the WS label."""
    j, steps = ws_idx - 1, 0
    while j >= 0 and steps < 5:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            j -= 1
            continue
        steps += 1
        name, role = _clean_name(s)
        if name:
            return j, name, role
        return None
    return None


def detect_vertical(lines: List[str], pages: List[int], book: str) -> List[Adversary40k]:
    n = len(lines)
    starts: List[Tuple[int, str, Optional[str], int, List[str]]] = []
    used = set()
    for i, ln in enumerate(lines):
        if ln.strip().lower() != "ws":
            continue
        # skip the label block (WS + the labels that follow)
        j = i + 1
        labels_seen = 0
        while j < n:
            s = lines[j].strip()
            if s == "" or PAGE.search(lines[j]):
                j += 1
                continue
            if _is_label_line(s):
                labels_seen += 1
                j += 1
                continue
            break
        if labels_seen == 0:
            continue
        # collect the contiguous value run
        tokens: List[Tuple[str, str]] = []
        k = j
        while k < n:
            s = lines[k].strip()
            if s == "" or PAGE.search(lines[k]):
                k += 1
                continue
            if STAT_KEYWORD.match(s):
                break
            c = _classify(s)
            if c is None:
                break
            tokens.append(c)
            k += 1
        values = _tokens_to_values(tokens)
        if len(values) < 9:
            continue
        got = _name_above(lines, i)
        if got is None or got[0] in used:
            continue
        nidx, name, role = got
        used.add(nidx)
        starts.append((nidx, name, role, k, values[:9]))

    starts.sort()
    out: List[Adversary40k] = []
    for idx, (nidx, name, role, body_start, values) in enumerate(starts):
        e = starts[idx + 1][0] if idx + 1 < len(starts) else min(n, nidx + 80)
        e = min(e, body_start + 60)
        a = Adversary40k(name=name, book=book, page=pages[nidx], start=nidx,
                         end=e, role=role)
        _apply_profile(a, values)
        _extract_extras(a, lines[body_start:e])
        out.append(a)
    return _finalize(out)


# ── detector C: PROFILE-ROW (name on an "X Profile" line, values on one row) ──

def _is_value_row(s: str, need: int = 9) -> Optional[List[str]]:
    """If a line is a whitespace-separated row of >= `need` value tokens, return
    the ordered non-paren values; else None."""
    toks = s.replace("\t", " ").split()
    if len(toks) < need:
        return None
    classed = [_classify(t) for t in toks]
    if any(c is None for c in classed):
        return None
    vals = _tokens_to_values([c for c in classed if c])
    return vals if len(vals) >= need else None


def detect_profile_row(lines: List[str], pages: List[int], book: str) -> List[Adversary40k]:
    n = len(lines)
    starts: List[Tuple[int, str, Optional[str], int, List[str]]] = []
    used = set()
    for i, ln in enumerate(lines):
        if not re.search(r"\bProfile\s*$", ln.strip(), re.IGNORECASE):
            continue
        name, role = _clean_name(ln)
        if name is None or i in used:
            continue
        # find the value row within the next few lines (skip label / blank lines)
        vrow = None
        vidx = None
        for k in range(i + 1, min(n, i + 8)):
            s = lines[k].strip()
            if s == "" or PAGE.search(lines[k]) or _is_label_line(s):
                continue
            v = _is_value_row(s, 9)
            if v is not None:
                vrow, vidx = v, k
            break
        if vrow is None:
            continue
        used.add(i)
        starts.append((i, name, role, vidx + 1, vrow[:9]))

    starts.sort()
    out: List[Adversary40k] = []
    for idx, (nidx, name, role, body_start, values) in enumerate(starts):
        e = starts[idx + 1][0] if idx + 1 < len(starts) else min(n, nidx + 80)
        e = min(e, body_start + 60)
        a = Adversary40k(name=name, book=book, page=pages[nidx], start=nidx,
                         end=e, role=role)
        _apply_profile(a, values)
        _extract_extras(a, lines[body_start:e])
        out.append(a)
    return _finalize(out)


# ── detector D: INFAMY-ROW (Black Crusade: 10-value row, name above) ─────────

INFAMY_ROW = re.compile(r"^(?:\(?\s*\d{1,3}\s*\)?\*?\s+){8,}")  # >=9 numbers on a row


def detect_infamy_row(lines: List[str], pages: List[int], book: str) -> List[Adversary40k]:
    n = len(lines)
    starts: List[Tuple[int, str, Optional[str], int, List[str], Optional[str]]] = []
    used = set()
    for i, ln in enumerate(lines):
        s = ln.strip()
        if not INFAMY_ROW.match(s):
            continue
        vals = _is_value_row(s, 9)
        if vals is None or len(vals) < 10:      # Black Crusade rows carry ten
            continue
        # name: nearest plausible line above, skipping stray SB/TB numbers,
        # single-letter OCR debris, blanks, and page markers
        nidx = name = role = None
        j, steps = i - 1, 0
        while j >= 0 and steps < 8:
            t = lines[j].strip()
            if t == "" or PAGE.search(lines[j]) or len(t) <= 1 or V_NUM.match(t):
                j -= 1
                continue
            steps += 1
            nm, rl = _clean_name(t)
            if nm:
                nidx, name, role = j, nm, rl
            break
        if name is None or nidx in used:
            continue
        used.add(nidx)
        starts.append((nidx, name, role, i + 1, vals[:9], vals[9]))

    starts.sort()
    out: List[Adversary40k] = []
    for idx, (nidx, name, role, body_start, values, inf) in enumerate(starts):
        e = starts[idx + 1][0] if idx + 1 < len(starts) else min(n, nidx + 80)
        e = min(e, body_start + 60)
        a = Adversary40k(name=name, book=book, page=pages[nidx], start=nidx,
                         end=e, role=role)
        _apply_profile(a, values, inf=inf)
        _extract_extras(a, lines[body_start:e])
        out.append(a)
    return _finalize(out)


# ── detector B: INVERTED / MERGED VERTICAL (Only War; Blood of Martyrs) ──────
# Only War's *Enemies of the Imperium* prints the vertical profile UPSIDE-DOWN
# relative to the other vertical books: the name sits on top, the nine
# characteristic VALUES run down next, and only THEN the WS / BS / … labels.
# Worse, the OCR drops the parentheses around Unnatural bonuses, leaving them as
# bare LEADING numbers (a creature with Unnatural Strength + Toughness shows two
# extra values at the head of the run), and a `## [PDF page N]` marker can fall
# *inside* a stat block — splitting the value run or pushing the
# Movement/Wounds/Traits onto the next page. Blood of Martyrs instead uses the
# ordinary top-down vertical, but its OCR MERGES several values onto one line
# ("40 – –"). Both layouts defeat the line-local `detect_vertical`, so this
# tolerant pair (a) tokenises each value line, (b) walks THROUGH page-break
# markers so a block split across a page is stitched into one creature (the
# citation still records the page the NAME sits on), and (c) resolves the nine
# characteristics RAW — an ambiguous run is set aside on SOFT_SKIPS, never
# guessed or fabricated.

# (book, page, name, raw_values) for every run this detector could not resolve
# cleanly to nine characteristics; reported, never emitted as a parsed row.
SOFT_SKIPS: List[Tuple[str, Optional[int], str, List[str]]] = []


def _label_run_down(lines: List[str], i: int) -> Tuple[List[str], int]:
    """Consume the WS..Fel label run below a standalone 'WS' at line i (labels
    may be combined on one line; blank lines and page markers are skipped).
    Returns (labels_seen, first_line_after_the_run)."""
    n = len(lines)
    labels = ["ws"]
    j = i + 1
    while j < n and len(labels) < 9:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            j += 1
            continue
        toks = s.replace("\t", " ").split()
        if toks and all(t.strip(".").lower() in CHAR_LABELS for t in toks):
            labels.extend(t.strip(".").lower() for t in toks)
            j += 1
            continue
        break
    return labels, j


def _values_line(s: str) -> Optional[List[str]]:
    """If every whitespace token on a line is a value / Unnatural-bonus paren /
    dash, return the kept values (parenthesised bonuses dropped) in left-to-right
    order; else None. Lets a value 'line' actually carry several merged tokens."""
    toks = s.replace("\t", " ").split()
    if not toks:
        return None
    classed = [_classify(t) for t in toks]
    if any(c is None for c in classed):
        return None
    return [v for kind, v in classed if kind != "paren"]


def _nine_from_inverted(vals: List[str]) -> Optional[List[str]]:
    """Map an inverted value run to nine characteristics. Exactly nine → direct.
    Ten-to-twelve → the leading (count−9) tokens are the bare Unnatural bonuses
    (numbers, NEVER dashes — a dash is always a real 'no-score' characteristic)
    and are dropped, keeping the nine nearest the labels. Otherwise the run is
    ambiguous → None (RAW: never guess which values to drop)."""
    if len(vals) == 9:
        return list(vals)
    extra = len(vals) - 9
    if 1 <= extra <= 3 and all(v.isdigit() for v in vals[:extra]):
        return list(vals[extra:])
    return None


def detect_vertical_inverted(lines: List[str], pages: List[int], book: str) -> List[Adversary40k]:
    n = len(lines)
    starts: List[Tuple[int, str, Optional[str], int, List[str]]] = []
    used = set()
    for i, ln in enumerate(lines):
        if ln.strip().lower() != "ws":
            continue
        labels, body_start = _label_run_down(lines, i)
        if labels[:9] != CHAR_KEYS:
            continue
        # Walk UP from the WS line, through blank lines and page markers,
        # gathering the contiguous value run; the first non-value line above it
        # is the name. Multi-token lines are tokenised and kept in order.
        vals: List[str] = []
        k = i - 1
        dist = 0
        while k >= 0 and dist < 60:
            raw = lines[k]
            s = raw.strip()
            dist += 1
            if s == "" or PAGE.search(raw):
                k -= 1
                continue
            got = _values_line(s)
            if got is None:
                break
            vals = got + vals
            k -= 1
        if k < 0:
            continue
        name, role = _clean_name(lines[k])
        if name is None or k in used:
            continue
        nine = _nine_from_inverted(vals)
        if nine is None:
            SOFT_SKIPS.append((book, pages[k], name, vals))
            continue
        used.add(k)
        starts.append((k, name, role, body_start, nine))

    starts.sort()
    out: List[Adversary40k] = []
    for idx, (nidx, name, role, body_start, values) in enumerate(starts):
        e = starts[idx + 1][0] if idx + 1 < len(starts) else min(n, nidx + 90)
        e = min(e, body_start + 70)
        a = Adversary40k(name=name, book=book, page=pages[nidx], start=nidx,
                         end=e, role=role)
        _apply_profile(a, values)
        _extract_extras(a, lines[body_start:e])
        out.append(a)
    return _finalize(out)


def detect_vertical_merged(lines: List[str], pages: List[int], book: str) -> List[Adversary40k]:
    """Ordinary top-down vertical (name above the WS label run, values below the
    labels) but tolerant of OCR that merges several values onto one line."""
    n = len(lines)
    starts: List[Tuple[int, str, Optional[str], int, List[str]]] = []
    used = set()
    for i, ln in enumerate(lines):
        if ln.strip().lower() != "ws":
            continue
        labels, body_start = _label_run_down(lines, i)
        if labels[:9] != CHAR_KEYS:
            continue
        vals: List[str] = []
        k = body_start
        dist = 0
        while k < n and dist < 40:
            raw = lines[k]
            s = raw.strip()
            dist += 1
            if s == "" or PAGE.search(raw):
                k += 1
                continue
            if STAT_KEYWORD.match(s):
                break
            got = _values_line(s)
            if got is None:
                break
            vals += got
            k += 1
        if len(vals) < 9:
            continue
        got_name = _name_above(lines, i)
        if got_name is None or got_name[0] in used:
            continue
        nidx, name, role = got_name
        # RAW guard: tokens beyond the nine are acceptable ONLY when they are
        # spurious trailing dashes (layout padding, e.g. "40 – –" → WP 40, Fel –).
        # A non-dash extra means the OCR split a two-digit characteristic across a
        # space (Fel "25" printed "2 5"); reconstructing it would be a guess, so
        # the block is set aside on SOFT_SKIPS instead of emitting a wrong value.
        if len(vals) > 9 and not all(v == "—" for v in vals[9:]):
            SOFT_SKIPS.append((book, pages[nidx], name, vals))
            continue
        used.add(nidx)
        starts.append((nidx, name, role, k, vals[:9]))

    starts.sort()
    out: List[Adversary40k] = []
    for idx, (nidx, name, role, body_start, values) in enumerate(starts):
        e = starts[idx + 1][0] if idx + 1 < len(starts) else min(n, nidx + 80)
        e = min(e, body_start + 60)
        a = Adversary40k(name=name, book=book, page=pages[nidx], start=nidx,
                         end=e, role=role)
        _apply_profile(a, values)
        _extract_extras(a, lines[body_start:e])
        out.append(a)
    return _finalize(out)


# ── detector E: STANDARD VERTICAL, bare-bonus aware (Rogue Trader supplements) ─
# The Rogue Trader supplements print the ordinary top-down vertical profile, but
# with two OCR wrinkles that the plain first-nine `detect_vertical` gets wrong:
#   * a page-number folio leaks in as TRAILING value(s) (e.g. a p.121 creature's
#     run ends "… 38 121 121") — here the real nine come FIRST (first-nine is
#     right, and this reproduces `detect_vertical`), and
#   * a few creatures print Unnatural bonuses BARE and LEADING (Skabgob "10 10 …",
#     Stalker Hrrithck "8 8 …") — here the real nine come LAST.
# The two are told apart RAW-safely: a real characteristic in these books is
# written two-digit (leading zero below ten), so a run that *starts* with one to
# three tiny bare integers (<=15, and whose tail is not the page folio) is
# leading bonuses → take the last nine; otherwise the extras are trailing folio
# furniture → take the first nine. A run that resolves to several bare single
# digits is OCR garbage and is set aside rather than emitted.

def _nine_std(values: List[str], page: Optional[int]) -> Optional[List[str]]:
    """Resolve a top-down value run to nine characteristics, or None if the run
    is OCR garbage that must be set aside (see the block comment above)."""
    if len(values) < 9:
        return None
    if len(values) == 9:
        nine = list(values)
    else:
        lead = len(values) - 9
        if 1 <= lead <= 3 and all(v.isdigit() and int(v) <= 15 for v in values[:lead]) \
                and values[-1] != str(page):
            nine = list(values[-9:])          # bare leading Unnatural bonuses
        else:
            nine = list(values[:9])           # trailing page-folio furniture
    if sum(1 for v in nine if v.isdigit() and len(v) == 1) >= 4:
        return None                            # scrambled OCR — refuse to guess
    return nine


def detect_vertical_bonus(lines: List[str], pages: List[int], book: str) -> List[Adversary40k]:
    n = len(lines)
    starts: List[Tuple[int, str, Optional[str], int, List[str]]] = []
    used = set()
    for i, ln in enumerate(lines):
        if ln.strip().lower() != "ws":
            continue
        # skip the label block (identical to detect_vertical)
        j = i + 1
        labels_seen = 0
        while j < n:
            s = lines[j].strip()
            if s == "" or PAGE.search(lines[j]):
                j += 1
                continue
            if _is_label_line(s):
                labels_seen += 1
                j += 1
                continue
            break
        if labels_seen == 0:
            continue
        # collect the contiguous value run, one token per line (as detect_vertical)
        tokens: List[Tuple[str, str]] = []
        k = j
        while k < n:
            s = lines[k].strip()
            if s == "" or PAGE.search(lines[k]):
                k += 1
                continue
            if STAT_KEYWORD.match(s):
                break
            c = _classify(s)
            if c is None:
                break
            tokens.append(c)
            k += 1
        values = _tokens_to_values(tokens)
        if len(values) < 9:
            continue
        got = _name_above(lines, i)
        if got is None or got[0] in used:
            continue
        nidx, name, role = got
        nine = _nine_std(values, pages[nidx])
        if nine is None:
            SOFT_SKIPS.append((book, pages[nidx], name, values))
            continue
        used.add(nidx)
        starts.append((nidx, name, role, k, nine))

    starts.sort()
    out: List[Adversary40k] = []
    for idx, (nidx, name, role, body_start, values) in enumerate(starts):
        e = starts[idx + 1][0] if idx + 1 < len(starts) else min(n, nidx + 80)
        e = min(e, body_start + 60)
        a = Adversary40k(name=name, book=book, page=pages[nidx], start=nidx,
                         end=e, role=role)
        _apply_profile(a, values)
        _extract_extras(a, lines[body_start:e])
        out.append(a)
    return _finalize(out)


def _finalize(items: List[Adversary40k]) -> List[Adversary40k]:
    """Drop running headers (a name recurring 3+ times) and collapse exact
    duplicate names within a book to the first."""
    from collections import Counter
    cnt = Counter(a.name.lower() for a in items)
    out, seen = [], set()
    for a in items:
        key = a.name.lower()
        if cnt[key] >= 3 or key in seen:
            continue
        seen.add(key)
        out.append(a)
    return out


DETECTORS: Dict[str, Callable[[List[str], List[int], str], List[Adversary40k]]] = {
    "vertical": detect_vertical,
    "vertical_inverted": detect_vertical_inverted,
    "vertical_merged": detect_vertical_merged,
    "vertical_bonus": detect_vertical_bonus,
    "profile_row": detect_profile_row,
    "infamy_row": detect_infamy_row,
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
    adversaries: List[Adversary40k] = field(default_factory=list)


_W = "Warhammer/40K Roleplay"
SOURCES: List[Source] = [
    # ── VERTICAL profile books (the adversary-dense core of the deliverable) ──
    Source("creatures_anathema", "Dark Heresy: Creatures Anathema",
           Path(f"{_W}/Dark Heresy/Rulebooks/Dark Heresy - Creatures Anathema.md"),
           "Dark Heresy: Creatures Anathema (FFG, 40kRP d100)", "vertical"),
    Source("mark_of_xenos", "Deathwatch: Mark of the Xenos",
           Path(f"{_W}/Deathwatch/Rulebooks/Deathwatch - Mark of the Xenos.md"),
           "Deathwatch: Mark of the Xenos (FFG, 40kRP d100)", "vertical"),
    Source("rt_core", "Rogue Trader: Core Rulebook",
           Path(f"{_W}/Rogue Trader/Rulebooks/Rogue Trader - Core Rulebook (updated with 1.4 errata).md"),
           "Rogue Trader Core Rulebook, Xenos & Adversaries (FFG, 40kRP d100)", "vertical"),
    Source("koronus_bestiary", "Rogue Trader: The Koronus Bestiary",
           Path(f"{_W}/Rogue Trader/Rulebooks/Rogue Trader - The Koronus Bestiary.md"),
           "Rogue Trader: The Koronus Bestiary (FFG, 40kRP d100)", "vertical"),
    # ── PROFILE-ROW books (name on an 'X Profile' line, values on one row) ────
    Source("dh_core", "Dark Heresy: Core Rulebook",
           Path(f"{_W}/Dark Heresy/Rulebooks/Dark Heresy - Core Rulebook.pdf.md"),
           "Dark Heresy Core Rulebook, Adversaries (FFG, 40kRP d100)", "profile_row"),
    Source("inquisitors_handbook", "Dark Heresy: The Inquisitor's Handbook",
           Path(f"{_W}/Dark Heresy/Rulebooks/Dark Heresy - The Inquisitor's Handbook.md"),
           "Dark Heresy: The Inquisitor's Handbook (FFG, 40kRP d100)", "profile_row"),
    Source("dw_core", "Deathwatch: Core Rulebook",
           Path(f"{_W}/Deathwatch/Rulebooks/Deathwatch - Core Rulebook.md"),
           "Deathwatch Core Rulebook, Adversaries (FFG, 40kRP d100)", "profile_row"),
    # ── INFAMY-ROW book (Black Crusade: ten characteristics incl. Infamy) ─────
    Source("bc_core", "Black Crusade: Core Rulebook",
           Path(f"{_W}/Black Crusade/Rulebooks/Black Crusade - Core Rulebook.md"),
           "Black Crusade Core Rulebook, Adversaries (FFG, 40kRP d100)", "infamy_row"),

    # ─────────────────────────────────────────────────────────────────────────
    # EXTENSION: the remaining adversary-bearing 40kRP books. The existing rows
    # above are untouched; everything below is additive.
    # ─────────────────────────────────────────────────────────────────────────
    # ── INVERTED-VERTICAL book (Only War: values above the labels; Unnatural
    #    bonuses printed bare & leading; stat blocks stitched across page breaks)
    Source("ow_enemies", "Only War: Enemies of the Imperium",
           Path(f"{_W}/Only War/Rulebooks/Only War - Enemies of the Imperium.md"),
           "Only War: Enemies of the Imperium (FFG, 40kRP d100)", "vertical_inverted"),
    # ── INFAMY-ROW supplements (Black Crusade Tomes: ten chars incl. Infamy) ──
    Source("bc_tome_blood", "Black Crusade: Tome of Blood",
           Path(f"{_W}/Black Crusade/Rulebooks/Black Crusade - Tome of Blood.md"),
           "Black Crusade: Tome of Blood (FFG, 40kRP d100)", "infamy_row"),
    Source("bc_tome_excess", "Black Crusade: Tome of Excess",
           Path(f"{_W}/Black Crusade/Rulebooks/Black Crusade - Tome of Excess.md"),
           "Black Crusade: Tome of Excess (FFG, 40kRP d100)", "infamy_row"),
    Source("bc_tome_fate", "Black Crusade: Tome of Fate",
           Path(f"{_W}/Black Crusade/Rulebooks/Black Crusade - Tome of Fate.md"),
           "Black Crusade: Tome of Fate (FFG, 40kRP d100)", "infamy_row"),
    # ── VERTICAL supplements (Rogue Trader): name, WS..Fel labels, then values.
    #    These use the bare-bonus-aware detector: their OCR leaks page-folios as
    #    trailing values and prints a few Unnatural bonuses bare & leading. ─────
    Source("rt_soul_reaver", "Rogue Trader: The Soul Reaver",
           Path(f"{_W}/Rogue Trader/Rulebooks/Rogue Trader - The Soul Reaver.md"),
           "Rogue Trader: The Soul Reaver (FFG, 40kRP d100)", "vertical_bonus"),
    Source("rt_stars_inequity", "Rogue Trader: Stars of Inequity",
           Path(f"{_W}/Rogue Trader/Rulebooks/Rogue Trader - Stars of Inequity.md"),
           "Rogue Trader: Stars of Inequity (FFG, 40kRP d100)", "vertical_bonus"),
    Source("rt_edge_abyss", "Rogue Trader: Edge of the Abyss",
           Path(f"{_W}/Rogue Trader/Rulebooks/Rogue Trader - Edge of the Abyss.md"),
           "Rogue Trader: Edge of the Abyss (FFG, 40kRP d100)", "vertical_bonus"),
    # ── VERTICAL supplements (Deathwatch) ─────────────────────────────────────
    Source("dw_achilus", "Deathwatch: The Achilus Assault",
           Path(f"{_W}/Deathwatch/Rulebooks/Deathwatch - The Achilus Assault.md"),
           "Deathwatch: The Achilus Assault (FFG, 40kRP d100)", "vertical"),
    Source("dw_first_founding", "Deathwatch: First Founding",
           Path(f"{_W}/Deathwatch/Rulebooks/Deathwatch - First Founding.md"),
           "Deathwatch: First Founding (FFG, 40kRP d100)", "vertical"),
    Source("dw_jericho_reach", "Deathwatch: The Jericho Reach",
           Path(f"{_W}/Deathwatch/Rulebooks/Deathwatch - The Jericho Reach.md"),
           "Deathwatch: The Jericho Reach (FFG, 40kRP d100)", "vertical"),
    # ── VERTICAL supplements (Dark Heresy) ────────────────────────────────────
    Source("dh_disciples", "Dark Heresy: Disciples of the Dark Gods",
           Path(f"{_W}/Dark Heresy/Rulebooks/Dark Heresy - Disciples of The Dark Gods.md"),
           "Dark Heresy: Disciples of the Dark Gods (FFG, 40kRP d100)", "vertical"),
    Source("dh_daemon_hunter", "Dark Heresy: Daemon Hunter",
           Path(f"{_W}/Dark Heresy/Rulebooks/Dark Heresy - Daemon Hunter.md"),
           "Dark Heresy: Daemon Hunter (FFG, 40kRP d100)", "vertical"),
    Source("dh_ascension", "Dark Heresy: Ascension",
           Path(f"{_W}/Dark Heresy/Rulebooks/Dark Heresy - Ascension.md"),
           "Dark Heresy: Ascension (FFG, 40kRP d100)", "vertical"),
    # ── MERGED-VERTICAL supplement (Dark Heresy: values merged onto one line) ─
    Source("dh_blood_martyrs", "Dark Heresy: Blood of Martyrs",
           Path(f"{_W}/Dark Heresy/Rulebooks/Dark Heresy - Blood of Martyrs.md"),
           "Dark Heresy: Blood of Martyrs (FFG, 40kRP d100)", "vertical_merged"),
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
        SOFT_SKIPS.clear()   # collect this build's unresolved runs from scratch
        for src in self.sources:
            path = base / src.path
            if not path.exists():
                src.coverage = f"NO COVERAGE — extraction missing: {path}"
                continue
            src.lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            pages = _pages_for(src.lines)
            src.adversaries = DETECTORS[src.detector](src.lines, pages, src.book)
            src.coverage = f"ok — {len(src.adversaries)} adversaries from {path.name}"

    def all_adversaries(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for a in src.adversaries:
                yield src, a

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, a in self.all_adversaries(book):
            nm = a.name.lower()
            if nm == q:
                exact.append((src, a))
            elif q in nm:
                partial.append((src, a))
        return exact if exact else partial


def _profile_str(a: Adversary40k) -> str:
    cells = [getattr(a, k) or "\u2014" for k in CHAR_KEYS]
    out = "/".join(cells)
    if a.inf is not None:
        out += f" (Inf {a.inf})"
    return out


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# WARHAMMER 40,000 ROLEPLAY — ADVERSARY / BESTIARY INDEX",
        "",
        "**Generated by `scripts/wh40krp_adversary_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** These are **Warhammer 40,000 Roleplay** (Fantasy",
        "Flight d100) adversaries — a DIFFERENT game system from the campaign's",
        "3.5e / GURPS RAW. Every row is stamped `system: WH40K Roleplay`; a 40kRP",
        "block is SOURCE MATERIAL for the system-translator skill, not campaign",
        "RAW. The nine characteristics are **WS BS S T Ag Int Per WP Fel** (Black",
        "Crusade adds Infamy); a `\u2014` is a no-score or a field the OCR did not",
        "cleanly yield. Use `--export \"NAME\"` for the translator packet.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.adversaries)
        parsed_well += sum(1 for a in src.adversaries if a.quick_fields() >= 6)
        sources_out.append({"key": src.key, "book": src.book, "system": SYSTEM,
                            "citation": src.citation, "coverage": src.coverage,
                            "adversaries": [asdict(a) for a in src.adversaries]})
        md.append(f"## {src.book} — {len(src.adversaries)} adversaries  *(system: {SYSTEM})*")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.adversaries:
            md.append("| Adversary | Role | WS/BS/S/T/Ag/Int/Per/WP/Fel | Move | Wounds | Page |")
            md.append("|---|---|---|---|---|---|")
            for a in src.adversaries:
                md.append(f"| {a.name} | {a.role or '\u2014'} | {_profile_str(a)} | "
                          f"{a.movement or '\u2014'} | {a.wounds or '\u2014'} | "
                          f"{a.page if a.page is not None else '\u2014'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/wh40krp_adversary_harvest.py",
                    "system": SYSTEM, "corpus": str(corpus.base),
                    "total_adversaries": total, "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 6:
        print(f"'{name}' matches {len(hits)} adversaries; narrow with --book or the exact name:")
        for src, a in hits[:20]:
            print(f"  {a.name}   [{a.book}, p.{a.page}]")
        return 1
    packets = []
    for src, a in hits:
        body = [ln for ln in src.lines[a.start:a.end] if not PAGE.search(ln)]
        parsed = {k: getattr(a, k) for k in
                  (CHAR_KEYS + ["inf", "role", "movement", "wounds", "skills",
                                "talents", "traits", "armour", "weapons", "gear"])
                  if getattr(a, k)}
        packets.append({
            "packet": "wh40krp-adversary-for-translation",
            "instructions": ("A Warhammer 40,000 Roleplay (FFG d100) adversary "
                             "(system: WH40K Roleplay). Feed to the system-translator "
                             "skill to build the paired 3.5e AND GURPS statlines — "
                             "both required. The raw_block is OCR text; check "
                             "oddities against the source PDF."),
            "name": a.name, "system": SYSTEM,
            "source": {"book": a.book, "pdf_page": a.page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [a.start + 1, a.end], "citation": src.citation},
            "parsed": parsed,
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


FIXTURE_VERTICAL = """## [PDF page 88]
Purestrain Genestealer (Elite) Profile
WS
bS
S
T
Ag
Int Per WP Fel
(8)
(8)
(8)
65
\u2014
45
40
40
35
60
45
\u2014\u2014
Movement: 8/16/24/48
Wounds: 20
Skills: Awareness (Per) +10, Climb (S) +10, Dodge (Ag) +10.
Talents: Fearless, Lightning Attack, Swift Attack.
Traits: Dark Sight, Fear 2 (Frightening), Unnatural Strength (x2).
Armour: Reinforced Chitin (All 4).
Weapons: Rending Claws (1d10+12 R; Pen 5, Razor Sharp).

Ork Boy (Troops) Profile
WS
bS
S
T
Ag
Int Per WP Fel
(8)
40
20
46
45
30
20
25
25
20
Speed: 3/6/9/18
Wounds: 15
Skills: Awareness (Per), Dodge (Ag), Intimidate (S).
Traits: Brutal Charge, Mob Rule, Unnatural Toughness (x2).
"""

FIXTURE_ROW = """## [PDF page 340]
Combat Servitor Profile
\tWS\t BS
S
T
Ag Int Per WP Fel
\t30\t 15\t 50\t 40\t 15\t 10\t 20\t 30\t 05
Combat Servitor is a mindless drone.
Movement: 3/6/9/18
Wounds: 10
Traits: Fear (1), Machine (2), Natural Weapons.
"""

FIXTURE_INFAMY = """## [PDF page 370]
Bloodletter (Elite)
7
8
50 12 42 42 40 30 30 34 1 4 - -
WS
BS
S
T
Ag
Int
Per
WP
Fel
Inf
Movement: 7/14/21/42
Wounds: 35
Traits: Daemonic (+5), Fear (3), From Beyond.
Weapons: Hellblade (1d10+7 R; Pen 6).
"""

# INVERTED VERTICAL (Only War): the name tops the block, the nine values run
# down NEXT, then the WS..Fel labels. The Warboss shows two bare LEADING
# Unnatural bonuses (11, 11) that must be dropped. The Severan Soldier's
# Movement/Wounds/Weapons sit past a `## [PDF page N]` marker (with folio /
# running-header debris) and must still be stitched onto the creature.
FIXTURE_INVERTED = """## [PDF page 29]
Severan Dominate Soldier (Troop)
36
34
35
35
37
28
34
26
33
WS
BS
S
T
Ag
Int
Per
WP
Fel
28
1

## [PDF page 30]

29
I: The Traitor
Movement: 3/6/9/18
Wounds: 12
Armour: Flak armour (All 4)
Skills: Awareness (Per), Dodge (Ag).
Talents: Nerves of Steel, Takedown.
Weapons: Autopistol; chainsword.
Gear: Severan Dominate uniform.

Warboss (Master)
11
11
60
30
60
60
40
30
35
40
30
WS
BS
S
T
Ag
Int
Per
WP
Fel
"""

# INVERTED VERTICAL with the PROFILE ITSELF split across a page break: the value
# run (9, 8, 56, 55 | 51, 48, 45, 42, 45, 50, 29) is interrupted mid-run by a
# `## [PDF page N]` marker and must be stitched back into one nine-value profile;
# the citation records page 50 (where the NAME sits), and the two leading bare
# Unnatural bonuses (9, 8) are dropped.
FIXTURE_INVERTED_PAGESPLIT = """## [PDF page 50]
Chaos Space Marine (Elite)
9
8
56
55
## [PDF page 51]
51
48
45
42
45
50
29
WS
BS
S
T
Ag
Int
Per
WP
Fel
Movement: 4/8/12/24
Traits: Unnatural Strength (x2), Unnatural Toughness (x2), Fear (1).
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    # ── fixture: VERTICAL ───────────────────────────────────────────────────
    lines = FIXTURE_VERTICAL.splitlines()
    got = detect_vertical(lines, _pages_for(lines), "Deathwatch: Mark of the Xenos")
    names = [a.name for a in got]
    if names != ["Purestrain Genestealer", "Ork Boy"]:
        failures.append(f"vertical fixture names {names}, wanted "
                        f"['Purestrain Genestealer', 'Ork Boy']")
    else:
        gs = got[0]
        prof = (gs.ws, gs.bs, gs.s, gs.t, gs.ag, gs.int, gs.per, gs.wp, gs.fel)
        want = ("65", "\u2014", "45", "40", "40", "35", "60", "45", "\u2014")
        if prof != want:
            failures.append(f"Genestealer profile {prof}, wanted {want} "
                            f"(three (8) Unnatural bonuses dropped)")
        if gs.role != "Elite":
            failures.append(f"Genestealer role {gs.role!r}, wanted 'Elite'")
        if gs.system != SYSTEM:
            failures.append(f"system {gs.system!r}, must be {SYSTEM!r}")
        if (gs.movement, gs.wounds) != ("8/16/24/48", "20"):
            failures.append(f"Genestealer move/wounds {(gs.movement, gs.wounds)}")
        ork = got[1]
        oprof = (ork.ws, ork.bs, ork.s, ork.t, ork.ag, ork.int, ork.per, ork.wp, ork.fel)
        if oprof != ("40", "20", "46", "45", "30", "20", "25", "25", "20"):
            failures.append(f"Ork Boy profile {oprof}")
        if ork.movement != "3/6/9/18":
            failures.append(f"Ork Boy Speed->movement {ork.movement!r}")

    # ── fixture: PROFILE-ROW ────────────────────────────────────────────────
    lines = FIXTURE_ROW.splitlines()
    got = detect_profile_row(lines, _pages_for(lines), "Dark Heresy: Core Rulebook")
    if [a.name for a in got] != ["Combat Servitor"]:
        failures.append(f"profile-row fixture names {[a.name for a in got]}")
    elif got:
        cs = got[0]
        prof = (cs.ws, cs.bs, cs.s, cs.t, cs.ag, cs.int, cs.per, cs.wp, cs.fel)
        if prof != ("30", "15", "50", "40", "15", "10", "20", "30", "05"):
            failures.append(f"Combat Servitor profile {prof}")

    # ── fixture: INFAMY-ROW ─────────────────────────────────────────────────
    lines = FIXTURE_INFAMY.splitlines()
    got = detect_infamy_row(lines, _pages_for(lines), "Black Crusade: Core Rulebook")
    if [a.name for a in got] != ["Bloodletter"]:
        failures.append(f"infamy-row fixture names {[a.name for a in got]}")
    elif got:
        bl = got[0]
        prof = (bl.ws, bl.bs, bl.s, bl.t, bl.ag, bl.int, bl.per, bl.wp, bl.fel, bl.inf)
        if prof != ("50", "12", "42", "42", "40", "30", "30", "34", "1", "4"):
            failures.append(f"Bloodletter profile+inf {prof}")
        if bl.role != "Elite":
            failures.append(f"Bloodletter role {bl.role!r}, wanted 'Elite'")

    # ── fixture: INVERTED VERTICAL (Only War) + page-break stitch ────────────
    lines = FIXTURE_INVERTED.splitlines()
    got = detect_vertical_inverted(lines, _pages_for(lines),
                                   "Only War: Enemies of the Imperium")
    names = [a.name for a in got]
    if names != ["Severan Dominate Soldier", "Warboss"]:
        failures.append(f"inverted fixture names {names}, wanted "
                        f"['Severan Dominate Soldier', 'Warboss']")
    else:
        sol = got[0]
        sprof = (sol.ws, sol.bs, sol.s, sol.t, sol.ag, sol.int, sol.per, sol.wp, sol.fel)
        if sprof != ("36", "34", "35", "35", "37", "28", "34", "26", "33"):
            failures.append(f"Severan Soldier profile {sprof}")
        if sol.role != "Troop":
            failures.append(f"Severan Soldier role {sol.role!r}, wanted 'Troop'")
        if (sol.movement, sol.wounds) != ("3/6/9/18", "12"):
            failures.append(f"Severan Soldier move/wounds not stitched across the "
                            f"page break: {(sol.movement, sol.wounds)}")
        if not sol.weapons or "chainsword" not in sol.weapons:
            failures.append(f"Severan Soldier weapons not stitched across the page "
                            f"break: {sol.weapons!r}")
        wb = got[1]
        wprof = (wb.ws, wb.bs, wb.s, wb.t, wb.ag, wb.int, wb.per, wb.wp, wb.fel)
        if wprof != ("60", "30", "60", "60", "40", "30", "35", "40", "30"):
            failures.append(f"Warboss profile {wprof} (two bare leading Unnatural "
                            f"bonuses 11,11 must be dropped)")
        if wb.role != "Master":
            failures.append(f"Warboss role {wb.role!r}, wanted 'Master'")

    # ── fixture: INVERTED with the PROFILE split across a page break ─────────
    lines = FIXTURE_INVERTED_PAGESPLIT.splitlines()
    got = detect_vertical_inverted(lines, _pages_for(lines),
                                   "Only War: Enemies of the Imperium")
    if [a.name for a in got] != ["Chaos Space Marine"]:
        failures.append(f"page-split fixture names {[a.name for a in got]}")
    elif got:
        csm = got[0]
        prof = (csm.ws, csm.bs, csm.s, csm.t, csm.ag, csm.int, csm.per, csm.wp, csm.fel)
        if prof != ("56", "55", "51", "48", "45", "42", "45", "50", "29"):
            failures.append(f"Chaos Space Marine stitched profile {prof}")
        if csm.role != "Elite":
            failures.append(f"Chaos Space Marine role {csm.role!r}, wanted 'Elite'")
        if csm.page != 50:
            failures.append(f"Chaos Space Marine page {csm.page}, wanted 50 "
                            f"(the page the name starts on)")
        if not csm.traits or "Unnatural Strength" not in csm.traits:
            failures.append(f"Chaos Space Marine traits not parsed: {csm.traits!r}")

    # ── garbage-name filter ─────────────────────────────────────────────────
    for junk in ["WS", "Movement", "Skills", "Adventure Seeds",
                 "The following creatures are described below and.",
                 "42", "Int Per WP Fel"]:
        nm, _ = _clean_name(junk)
        if nm is not None:
            failures.append(f"garbage name not rejected: {junk!r} -> {nm!r}")

    # ── live checks ─────────────────────────────────────────────────────────
    if base.is_dir() and any((base / s.path).exists() for s in SOURCES):
        corpus = Corpus(base, _fresh_sources())
        total = sum(len(s.adversaries) for s in corpus.sources)
        if total < 150:
            failures.append(f"only {total} 40kRP adversaries indexed; expected > 150")
        for who, bk, min_num in [("Purestrain Genestealer", "mark_of_xenos", 6),
                                 ("Ork Boy", "mark_of_xenos", 9)]:
            hit = corpus.find(who, book=bk)
            if not hit:
                failures.append(f"'{who}' not found in live {bk}")
                continue
            a = hit[0][1]
            if any(getattr(a, k) is None for k in CHAR_KEYS):
                failures.append(f"'{who}' left a characteristic unparsed: "
                                f"{[getattr(a, k) for k in CHAR_KEYS]}")
            if a.quick_fields() < min_num:
                failures.append(f"'{who}' parsed only {a.quick_fields()} numeric characteristics")
        # a Chaos Space Marine adversary lives in Black Crusade (infamy row)
        if any(s.key == "bc_core" and s.adversaries for s in corpus.sources):
            csm = corpus.find("chaos space marine", book="bc_core") or \
                corpus.find("bloodletter", book="bc_core")
            if not csm:
                failures.append("no Black Crusade adversary (Chaos Space Marine / Bloodletter) found")
        # Only War: Enemies of the Imperium — the inverted-vertical book. Its
        # Warboss's two bare leading Unnatural bonuses (11, 11) must be dropped,
        # leaving the printed nine (60/30/60/60/40/30/35/40/30).
        if any(s.key == "ow_enemies" and s.adversaries for s in corpus.sources):
            hit = corpus.find("Warboss", book="ow_enemies")
            if not hit:
                failures.append("'Warboss' not found in live Only War: Enemies of the Imperium")
            else:
                wb = hit[0][1]
                wprof = tuple(getattr(wb, k) for k in CHAR_KEYS)
                if wprof != ("60", "30", "60", "60", "40", "30", "35", "40", "30"):
                    failures.append(f"live OW Warboss profile {wprof} "
                                    f"(leading Unnatural bonuses not dropped cleanly)")
        else:
            failures.append("Only War: Enemies of the Imperium yielded no adversaries")
    else:
        print("  [SKIP] 40kRP extractions not found — fixture checks only")

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
        found = sorted({(a.name, a.book, a.page or -1, _profile_str(a))
                        for _, a in corpus.all_adversaries(args.book) if q in a.name.lower()})
        for name, bk, page, prof in found:
            loc = bk if page < 0 else f"{bk}, p.{page}"
            print(f"  {name}   [{prof}; {loc}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.adversaries for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.adversaries):4d} adversaries" if src.adversaries else "   0 adversaries"
        print(f"  {src.book:42s} {status}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} WH40K Roleplay adversaries across "
          f"{sum(1 for s in corpus.sources if s.adversaries)} book(s); "
          f"{parsed_well} with 6+ characteristics parsed. (system: {SYSTEM})")
    if SOFT_SKIPS:
        print(f"\n{len(SOFT_SKIPS)} stat block(s) SET ASIDE (ambiguous value run, "
              f"left unparsed rather than guessed):")
        for bk, pg, nm, vals in SOFT_SKIPS:
            print(f"  [soft] {nm}  (p.{pg}, {len(vals)} values: {' '.join(vals)})  {bk}")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
