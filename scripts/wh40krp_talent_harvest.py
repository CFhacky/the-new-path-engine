#!/usr/bin/env python3
"""wh40krp_talent_harvest.py — collate Warhammer 40,000 Roleplay TALENTS.

THE PROCESS (Chad, 2026-08-28): other game systems are welcome AS LONG AS they
are clearly LABELLED by system — the translator tools convert them into the
hybrid's 3.5e + GURPS. This is the **Warhammer 40,000 Roleplay** (Fantasy Flight
Games d100 line: Dark Heresy, Rogue Trader, Deathwatch, Only War, Black Crusade)
TALENT index, kept entirely separate from every D&D/GURPS index and stamped
`"system": "WH40K Roleplay"`. A 40K RP talent is the analogue of a feat: a NAME,
a Tier and/or Prerequisites line, sometimes an Aptitudes tag, then a Benefit.

    reference/wh40krp_talent_index.json — every talent: name, tier, prerequisites,
                                          aptitudes, one-line benefit, book, PDF
                                          page, system WH40K Roleplay
    reference/wh40krp_talent_index.md   — the same, for human eyes

`--export "NAME"` emits a translator-ready packet (a 40K RP talent the
system-translator skill converts to the 3.5e + GURPS pair).

WORKFLOW
    python wh40krp_talent_harvest.py                 # (re)build the index
    python wh40krp_talent_harvest.py --search "draw" # find candidates
    python wh40krp_talent_harvest.py --export "Quick Draw" --book dh
    python wh40krp_talent_harvest.py --selftest

GOVERNING SOURCES  (I:\\Sourcebooks\\_text\\Warhammer\\40K Roleplay\\)
    Each core rulebook carries a "Talents" chapter. The books split into two
    presentation families, so a talent is read from whichever layer is CLEANEST
    per book (book RAW either way — the same talent, just a different column):

      * Dark Heresy   — summary "Table 4-1: Talents" (TAB-delimited
                        Name / Prerequisite / Benefit cells).  detector=dh_table
      * Deathwatch    — summary "Table 4-1: Talents" (plain lines, benefit
                        terminated by a full stop; the prose headings are
                        OCR-scrambled so the table is the clean layer).
                        detector=plain_table
      * Rogue Trader  — prose Talent descriptions (clean Title-Case headings +
                        "Prerequisites:" / "Talent Groups:"; its summary table
                        de-laminates mid-page, so prose is the clean layer).
                        detector=prose_title
      * Only War      — prose Talent descriptions (ALL-CAPS name, universal
                        "Tier:" line, then "Prerequisite:"/"Aptitudes:").
                        detector=prose_tier
      * Black Crusade — prose Talent descriptions (ALL-CAPS name, universal
                        "Tier:" line, then "Prerequisite:").  detector=prose_tier

    A configured source whose file is missing prints NO COVERAGE (it is never a
    silent gap). Talents are de-duplicated by (name, book): a same-named talent
    in two books is two rows, one per book — that is the point of the labels.

INVIOLABLE: book RAW only, never invent; cite book + PDF page; no cross-imports.
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
OUT_JSON = REPO / "reference" / "wh40krp_talent_index.json"
OUT_MD = REPO / "reference" / "wh40krp_talent_index.md"
SYSTEM = "WH40K Roleplay"

PAGE = re.compile(r"\[PDF page (\d+)\]")
DASHES = ("—", "–", "-", "", "None", "None.")

# lines that are page furniture / running heads / table headers — never talents
JUNK = re.compile(
    r"^(#|\d{1,3}$|Talent Name|Prerequisites?$|Benefi|Table\b|Chapter\b|"
    r"[IVX]+\s*[:.]|†|Talents?$|Traits?$|Gaining|Talent Groups?$|"
    r"Talent\s*$|Groups?$|Listing$|Special Talents|Specialist Talents|"
    r"Specialist Skills)",
    re.IGNORECASE)

# reserved leaders inside prose descriptions (never a talent name heading)
RESERVED = re.compile(
    r"^(Prerequisites?|Tier|Aptitudes?|Talent Groups?|Special|Note|Table|"
    r"Chapter|Traits?|[IVX]+\s*[:.])\b", re.IGNORECASE)

SMALL_WORDS = {"of", "the", "and", "or", "to", "a", "an", "in", "with", "for",
               "on", "unto", "from", "at", "by"}


SENT_OPEN = re.compile(
    r"^(The|This|A|An|When|Whenever|With|Either|Due|Through|Many|No|While|"
    r"Some|Once|Should|If|As|By|In|On|At|For|Whether|Long|Intensive|Mental|"
    r"Vox|Ancient|Gymnastic|Years|Trained|Whereas|Despite|Though|Gene|Even|"
    r"Ferocious|Being|Having|Not|Sometimes|Often|Whilst|Where|These|Their|"
    r"One|Each|Spend|Roll|Re-roll|Gain|Immune|Move|Reduce|Add|Use|Deal)\b")

SUBJECT = re.compile(r"\b(Explorer|character|Heretic|Battle-Brother|Acolyte|"
                     r"psyker|Sergeant)\b")


def _benefit_starts(s: str) -> bool:
    """True once benefit PROSE has begun — it opens a sentence or names the
    subject, which a wrapped specialisation / talent-group list never does."""
    return bool(SENT_OPEN.match(s) or SUBJECT.search(s))


# --------------------------------------------------------------------------- #
#  data model                                                                 #
# --------------------------------------------------------------------------- #
@dataclass
class Talent:
    name: str
    book: str
    page: Optional[int]
    start: int
    end: int
    system: str = SYSTEM
    tier: Optional[int] = None
    prerequisites: Optional[str] = None
    aptitudes: Optional[str] = None
    benefit: Optional[str] = None
    group: bool = False               # a "†" talent group (choose a specialism)

    def quick_fields(self) -> int:
        return sum(1 for v in (self.prerequisites, self.benefit, self.tier) if v)


def _clean_prereq(s: Optional[str]) -> Optional[str]:
    if s is None:
        return None
    s = s.strip().strip(".").strip()
    if s in DASHES or not s:
        return None
    return re.sub(r"\s+", " ", s)


def _plausible_name(s: str) -> bool:
    """Reject prose fragments / headers; accept real talent names."""
    s = s.strip().rstrip("†").strip()
    if not (2 <= len(s) <= 42):
        return False
    if JUNK.match(s) or RESERVED.match(s):
        return False
    # no real 40K RP talent name carries a comma or colon — those are table
    # fragments ("Simple Power Cell, Illuminator") or annotations ("Talent Use:")
    if "," in s or ":" in s:
        return False
    if s[-1] in ".,;:!?":
        return False
    if not (s[0].isalpha() or s[0].isdigit()):
        return False
    words = s.split()
    if len(words) > 7:
        return False
    letters = sum(c.isalpha() for c in s)
    if letters < max(2, len(s) // 2):
        return False
    return True


def _first_sentence(lines: List[str], i: int, n: int, limit: int = 5) -> Optional[str]:
    """The first full sentence of a prose benefit — a clean one-line summary."""
    buf: List[str] = []
    for j in range(i, min(n, i + limit)):
        if PAGE.search(lines[j]):
            if buf:
                break
            continue
        s = lines[j].strip()
        if s == "" or re.match(r"^\d{1,3}$", s):
            if buf:
                break
            continue
        buf.append(s)
        if re.search(r"[.!?]", s):        # a sentence terminator has appeared
            break
    if not buf:
        return None
    text = re.sub(r"\s+", " ", " ".join(buf)).strip()
    # cut to the first sentence: a terminator followed by space+capital or end
    # (skips decimals "1.5" and abbreviations "e.g." — those are followed by
    # a digit or a lower-case letter)
    m = re.search(r"[.!?][”\")]?(?=\s+[A-Z“\"(]|\s*$)", text)
    if m and m.end() >= 15:
        return text[:m.end()].strip()
    return text or None


# --------------------------------------------------------------------------- #
#  detector 1 — Dark Heresy: TAB-delimited Table 4-1                          #
#  Row = NAME<tab> / PREREQ<tab> / BENEFIT.  Name & prereq cells end in a     #
#  tab; the benefit (last cell) does not.  Prereq may carry the benefit after #
#  its tab; benefits may wrap over blank "<tab>" cells.                       #
# --------------------------------------------------------------------------- #
def _tab_cell(l: str) -> bool:
    return l.endswith("\t") and l.strip() != ""


def detect_dh_table(lines: List[str], pages: List[int], book: str) -> List[Talent]:
    n = len(lines)
    # region: after the "Talent Name / Prerequisite / Benefit" header, to "†Denotes"
    start = None
    for i in range(n - 2):
        if lines[i].strip().startswith("Talent Name") and \
           lines[i + 1].strip().startswith("Prerequisite") and \
           lines[i + 2].strip().startswith("Benefi"):
            start = i + 3
            break
    if start is None:
        return []
    # the table ends where the prose descriptions begin (their first
    # "Prerequisites:" line); the per-page "†Denotes" footers are NOT the end.
    end = n
    for i in range(start, n):
        if re.match(r"^Prerequisites?:", lines[i].strip(), re.IGNORECASE):
            end = i
            break

    out: List[Talent] = []
    state = "NAME"
    name = prereq = None
    ben: List[str] = []
    ben_done = False
    row_start = start

    def finalize():
        nonlocal name, prereq, ben, ben_done
        if name and _plausible_name(name):
            benefit = re.sub(r"\s+", " ", " ".join(ben)).strip() or None
            out.append(Talent(name=name.rstrip("†").strip(), book=book,
                              page=pages[row_start], start=row_start, end=min(end, row_start + 6),
                              prerequisites=_clean_prereq(prereq), benefit=benefit,
                              group=name.rstrip().endswith("†")))
        name, prereq, ben, ben_done = None, None, [], False

    i = start
    while i < end:
        l = lines[i]
        if PAGE.search(l):
            i += 1
            continue
        s = l.strip()
        if state == "NAME":
            if s == "" or not _tab_cell(l):
                i += 1
                continue
            name = s
            row_start = i
            prereq, ben, ben_done = None, [], False
            state = "PREREQ"
            i += 1
        elif state == "PREREQ":
            # the prerequisite cell — may be an EMPTY "\t" cell (no prereq)
            if s == "":
                if "\t" in l:                 # empty prereq cell
                    prereq = None
                    state = "BENEFIT"
                i += 1
                continue
            if "\t" in l and l.split("\t", 1)[1].strip():   # prereq<tab>benefit
                left, right = l.split("\t", 1)
                prereq = left.strip()
                ben = [right.strip()]
                ben_done = right.strip().endswith((".", "!", "?", ".”", '."'))
                if ben_done:
                    finalize()
                    state = "NAME"
                else:
                    state = "BENEFIT"
            else:
                prereq = s
                state = "BENEFIT"
            i += 1
        else:  # BENEFIT — a benefit cell can itself wrap and end in a tab, so a
               # tab cell only marks the NEXT row's NAME once this benefit has
               # closed (reached its terminal full stop). Inter-page footers /
               # page numbers arriving after that are then ignored.
            if _tab_cell(l) and (ben_done or len(ben) >= 5):
                finalize()
                state = "NAME"
                continue
            if s != "" and not ben_done:
                ben.append(s)
                if s.endswith((".", "!", "?", ".”", '."')):
                    ben_done = True
            i += 1
    if state != "NAME":
        finalize()
    _tighten_ends(out, end, 8)
    return _dedup(out)


# --------------------------------------------------------------------------- #
#  detector 2 — Deathwatch: plain Table 4-1 (benefit ends at a full stop)     #
#  Row = NAME / PREREQ / BENEFIT(may wrap).  No tab delimiter; the benefit    #
#  sentence's terminal full stop closes the row.  Validation drops the OCR    #
#  de-lamination artefacts (merged cells, orphaned names).                    #
# --------------------------------------------------------------------------- #
_PREREQ_HINT = re.compile(
    r"(^—$|^-$|^\u2013$|^\d|\b\d{2}\b|Adeptus|Astartes|Techmarine|Mechanicus|"
    r"Psy Rating|Frenzy|Dodge|Peer|Pilot|Faith|Weapon|Implants|Nerves|Swift|"
    r"Hatred|Command|Two-Weapon|Acrobatic|Warp|Machinator)", re.IGNORECASE)


def _skip_table_junk(l: str) -> bool:
    s = l.strip()
    if s == "" or PAGE.search(l):
        return True
    if re.match(r"^\d{1,3}$", s):
        return True
    if re.match(r"^(Table\b|Talent Name|Prerequisite\s*$|Benefit\s*$|"
                r"[IVX]+\s*:|†\s*Denotes)", s, re.IGNORECASE):
        return True
    return False


def detect_plain_table(lines: List[str], pages: List[int], book: str,
                       start_re: str, end_re: str) -> List[Talent]:
    n = len(lines)
    start = _find(lines, start_re) or 0
    end = _find(lines, end_re, start + 1) or n

    out: List[Talent] = []
    state = "NAME"
    name = prereq = None
    ben: List[str] = []
    row_start = start

    def finalize():
        nonlocal name, prereq, ben
        benefit = re.sub(r"\s+", " ", " ".join(ben)).strip()
        # validation: a real row has a plausible name + a real benefit sentence
        if (name and _plausible_name(name) and benefit and len(benefit) >= 4
                and benefit[-1] in ".!?"):
            out.append(Talent(name=name.rstrip("†").strip(), book=book,
                              page=pages[row_start], start=row_start,
                              end=min(end, row_start + 6),
                              prerequisites=_clean_prereq(prereq), benefit=benefit,
                              group=name.rstrip().endswith("†")))
        name, prereq, ben = None, None, []

    i = start
    while i < end:
        l = lines[i]
        if _skip_table_junk(l):
            i += 1
            continue
        s = l.strip()
        if state == "NAME":
            # split a merged "Name† —" cell
            m = re.match(r"^(.+?)†?\s+([—\u2013-])\s*$", s)
            if m and _plausible_name(m.group(1)):
                name = m.group(1)
                row_start = i
                prereq = "—"
                ben = []
                state = "BENEFIT"
                i += 1
                continue
            name = s
            row_start = i
            prereq, ben = None, []
            state = "PREREQ"
            i += 1
        elif state == "PREREQ":
            # some no-prerequisite rows carry NAME then straight into a (wrapping)
            # benefit with no "—" cell — detect benefit prose in the prereq slot
            if len(s) > 25 and _benefit_starts(s):
                prereq = None
                ben = [s]
                if s.endswith((".", "!", "?", ".”", '."')):
                    finalize()
                    state = "NAME"
                else:
                    state = "BENEFIT"
            else:
                prereq = s
                ben = []
                state = "BENEFIT"
            i += 1
        else:  # BENEFIT — accumulate to the terminal full stop (cap 3 lines)
            ben.append(s)
            if s.endswith((".", "!", "?", ".”", '."')) or len(ben) >= 3:
                finalize()
                state = "NAME"
            i += 1
    _tighten_ends(out, end, 8)
    return _dedup(out)


# --------------------------------------------------------------------------- #
#  detector 3 — Only War / Black Crusade: prose, universal "Tier:" anchor     #
#  <NAME in ALL CAPS> / Tier: N / [Prerequisite: ...] / [Aptitudes: ...] /    #
#  <benefit prose>.  Every talent carries the Tier line, so it anchors all    #
#  of them (incl. no-prerequisite talents).                                   #
# --------------------------------------------------------------------------- #
def _is_caps(s: str) -> bool:
    letters = [c for c in s if c.isalpha()]
    return len(letters) >= 2 and all(c.isupper() for c in letters)


ROMAN = re.compile(r"^[IVXLC]+$")


def _titlecase(s: str) -> str:
    """Normalise an ALL-CAPS heading to talent Title Case (small words down,
    apostrophe-suffixes and hyphenated parts handled: BLOOD GOD'S CONTEMPT ->
    Blood God's Contempt; ARMOUR-MONGER -> Armour-Monger)."""
    def cap_word(w: str) -> str:
        return "-".join(p[:1].upper() + p[1:] for p in w.split("-"))
    parts = s.split()
    out: List[str] = []
    for k, w in enumerate(parts):
        wl = w.lower()
        if k > 0 and re.sub(r"[^a-z]", "", wl) in SMALL_WORDS:
            out.append(wl)
        else:
            out.append(cap_word(wl))
    return " ".join(out)


def detect_prose_tier(lines: List[str], pages: List[int], book: str) -> List[Talent]:
    n = len(lines)
    out: List[Talent] = []
    for i in range(n):
        m = re.match(r"^Tier:\s*(\d)", lines[i].strip())
        if not m:
            continue
        tier = int(m.group(1))
        # name = the ALL-CAPS line just above (skip blanks / page marks); never a
        # roman-numeral running head ("IV") or other page furniture
        j = i - 1
        while j >= 0 and (lines[j].strip() == "" or PAGE.search(lines[j])
                          or ROMAN.match(lines[j].strip())
                          or JUNK.match(lines[j].strip())):
            j -= 1
        if j < 0 or not _is_caps(lines[j].strip()):
            continue
        raw_name = lines[j].strip()
        name_line = j
        # glue a genuinely wrapped caps line above (short, caps, not junk / roman)
        k = j - 1
        while k >= 0 and (lines[k].strip() == "" or PAGE.search(lines[k])):
            k -= 1
        if k >= 0:
            up = lines[k].strip()
            if (_is_caps(up) and len(up) <= 20 and not ROMAN.match(up)
                    and not JUNK.match(up) and "," not in up
                    and not up.endswith((".", "!", "?", ")"))):
                raw_name = up + " " + raw_name
                name_line = k
        name = _titlecase(re.sub(r"\s+", " ", raw_name))
        if not _plausible_name(name):
            continue
        # walk the header block: Prerequisite(s): / Aptitudes: / Specialisation(s):
        prereq = apt = None
        group = raw_name.rstrip().endswith("†")
        p = i + 1
        last = None
        spec_n = 0
        while p < n:
            s = lines[p].strip()
            if s == "" or PAGE.search(lines[p]) or re.match(r"^\d{1,3}$", s):
                p += 1
                continue
            mp = re.match(r"^(?:Prerequisites?|Category):\s*(.*)$", s, re.IGNORECASE)
            ma = re.match(r"^Aptitudes?:\s*(.*)$", s, re.IGNORECASE)
            msp = re.match(r"^Specialis[ae]tions?\b", s, re.IGNORECASE)
            if mp:
                prereq = mp.group(1).strip()
                last = "prereq"
                p += 1
                continue
            if ma:
                apt = ma.group(1).strip()
                last = "apt"
                p += 1
                continue
            if msp:                       # a specialisation/group list (may wrap)
                group = True
                last = "spec"
                spec_n = 0
                p += 1
                continue
            # a specialisation list wraps over several lines of Title-Case items;
            # keep consuming until the benefit prose begins or a sane bound is hit
            if last == "spec" and spec_n < 15 and not _benefit_starts(s):
                spec_n += 1
                p += 1
                continue
            # a wrapped prerequisite line — a short fragment left over from the
            # prereq wrapping (e.g. "Training (any two)", "ranged)"), not the
            # benefit prose (which fills the column and opens a sentence)
            if (last == "prereq" and prereq and len(s) < 35
                    and not SENT_OPEN.match(s)):
                prereq += " " + s
                p += 1
                continue
            break
        benefit = _first_sentence(lines, p, n)
        # reject truncated-column garbage: a real benefit never opens with a
        # header keyword bleeding in from a mangled two-column page
        if not benefit or re.match(r"^(Prerequ|Aptitud)", benefit):
            continue
        out.append(Talent(name=name, book=book, page=pages[name_line],
                          start=name_line, end=min(n, p + 6), tier=tier,
                          prerequisites=_clean_prereq(prereq),
                          aptitudes=(re.sub(r"\s+", " ", apt).strip() if apt else None),
                          benefit=benefit, group=group))
    _tighten_ends(out, n, 45)
    return _dedup(out)


# --------------------------------------------------------------------------- #
#  detector 4 — Rogue Trader: prose, Title-Case headings                      #
#  <Name> / [Prerequisites: ...] | [Talent Groups: ...] / <benefit prose>.    #
#  Headings are clean Title Case; a no-prereq talent's name is recognised as  #
#  a short Title-Case line that follows a full-stop and precedes prose.       #
# --------------------------------------------------------------------------- #
def _title_heading(s: str) -> bool:
    if not _plausible_name(s):
        return False
    if not s[0].isupper():
        return False
    for w in s.split():
        wl = re.sub(r"[^A-Za-z]", "", w).lower()
        if not wl or wl in SMALL_WORDS:
            continue
        if w[0].islower():          # a real word starting lower-case → prose
            return False
    return True


def detect_prose_title(lines: List[str], pages: List[int], book: str,
                       start_re: str, end_re: str) -> List[Talent]:
    n = len(lines)
    start = _find(lines, start_re) or 0
    end = _find(lines, end_re, start + 1) or n

    def prev_nonblank(i: int) -> Optional[str]:
        j = i - 1
        while j >= start and (lines[j].strip() == "" or PAGE.search(lines[j])
                              or re.match(r"^\d{1,3}$", lines[j].strip())):
            j -= 1
        return lines[j].strip() if j >= start else None

    def next_nonblank_idx(i: int) -> int:
        j = i + 1
        while j < end and (lines[j].strip() == "" or PAGE.search(lines[j])
                           or re.match(r"^\d{1,3}$", lines[j].strip())):
            j += 1
        return j

    out: List[Talent] = []
    first_seen = False
    i = start
    while i < end:
        l = lines[i]
        if lines[i].strip() == "" or PAGE.search(l) or re.match(r"^\d{1,3}$", lines[i].strip()):
            i += 1
            continue
        s = l.strip()
        if RESERVED.match(s) or not _title_heading(s):
            i += 1
            continue
        nxt = next_nonblank_idx(i)
        nxt_s = lines[nxt].strip() if nxt < end else ""
        anchored = bool(re.match(r"^(Prerequisites?|Talent Groups?):", nxt_s, re.IGNORECASE))
        prev = prev_nonblank(i)
        boundary = (not first_seen) or (prev is not None and
                                        prev.endswith((".", "!", "?", ".”", '."', ")")))
        # a heading is either anchored by a Prereq/Groups line, or a clean
        # Title-Case line at a block boundary followed by prose
        if not (anchored or (boundary and nxt_s and nxt_s[0].isupper()
                             and not RESERVED.match(nxt_s))):
            i += 1
            continue
        name = re.sub(r"\s+", " ", s.rstrip("†").strip())
        group = s.rstrip().endswith("†")
        prereq = None
        # walk the header block: a talent may carry BOTH "Prerequisites:" and a
        # (wrapping) "Talent Groups:" list before its benefit prose
        p = nxt
        last = None
        steps = 0
        while p < end and steps < 20:
            ps = lines[p].strip()
            mp = re.match(r"^Prerequisites?:\s*(.*)$", ps, re.IGNORECASE)
            mg = re.match(r"^Talent Groups?:\s*", ps, re.IGNORECASE)
            if mp:
                prereq = mp.group(1).strip()
                last = "prereq"
                p = next_nonblank_idx(p)
                steps += 1
                continue
            if mg:
                group = True
                last = "group"
                p = next_nonblank_idx(p)
                steps += 1
                continue
            if (last == "prereq" and prereq and (prereq.rstrip().endswith(",")
                    or prereq.split()[-1].lower() in SMALL_WORDS)):
                prereq += " " + ps
                p = next_nonblank_idx(p)
                steps += 1
                continue
            if last == "group" and not _benefit_starts(ps):
                p = next_nonblank_idx(p)
                steps += 1
                continue
            break
        benefit = _first_sentence(lines, p, end)
        out.append(Talent(name=name, book=book, page=pages[i], start=i,
                          end=min(end, p + 6), prerequisites=_clean_prereq(prereq),
                          benefit=benefit, group=group))
        first_seen = True
        i += 1
    _tighten_ends(out, end, 45)
    return _dedup(out)


# --------------------------------------------------------------------------- #
#  shared helpers                                                             #
# --------------------------------------------------------------------------- #
def _find(lines: List[str], pattern: Optional[str], frm: int = 0) -> Optional[int]:
    if not pattern:
        return None
    rx = re.compile(pattern)
    for i in range(frm, len(lines)):
        if rx.search(lines[i]):
            return i
    return None


def _tighten_ends(talents: List[Talent], region_end: int, cap: int) -> None:
    """Bound each talent's line span at the next talent's start, so the export
    raw_block is just that talent (not its neighbour too)."""
    ordered = sorted(talents, key=lambda t: t.start)
    for a, b in zip(ordered, ordered[1:]):
        a.end = min(b.start, a.start + cap)
    if ordered:
        ordered[-1].end = min(region_end, ordered[-1].start + cap)


def _dedup(talents: List[Talent]) -> List[Talent]:
    best: Dict[str, Talent] = {}
    for t in talents:
        key = t.name.lower()
        cur = best.get(key)
        if cur is None or t.quick_fields() > cur.quick_fields():
            best.setdefault(key, t)
            if cur is not None and t.quick_fields() > cur.quick_fields():
                best[key] = t
    return sorted(best.values(), key=lambda t: t.start)


def _pages_for(lines: List[str]) -> List[int]:
    pages: List[int] = []
    page = 0
    for ln in lines:
        m = PAGE.search(ln)
        if m:
            page = int(m.group(1))
        pages.append(page)
    return pages


# --------------------------------------------------------------------------- #
#  sources                                                                    #
# --------------------------------------------------------------------------- #
@dataclass
class Source:
    key: str
    book: str
    path: Path
    citation: str
    detector: str
    start_re: Optional[str] = None
    end_re: Optional[str] = None
    coverage: str = "pending"
    lines: List[str] = field(default_factory=list)
    talents: List[Talent] = field(default_factory=list)


_W = "Warhammer/40K Roleplay"
SOURCES: List[Source] = [
    Source("dh", "Dark Heresy Core Rulebook",
           Path(f"{_W}/Dark Heresy/Rulebooks/Dark Heresy - Core Rulebook.pdf.md"),
           "Dark Heresy Core Rulebook (FFG, WH40K Roleplay), Ch. IV: Talents, "
           "Table 4-1", "dh_table"),
    Source("rt", "Rogue Trader Core Rulebook",
           Path(f"{_W}/Rogue Trader/Rulebooks/"
                "Rogue Trader - Core Rulebook (updated with 1.4 errata).md"),
           "Rogue Trader Core Rulebook (FFG, WH40K Roleplay), Ch. IV: Talents",
           "prose_title",
           start_re=r"full explanation.{0,6}of each Talent", end_re=r"V: Armoury"),
    Source("dw", "Deathwatch Core Rulebook",
           Path(f"{_W}/Deathwatch/Rulebooks/Deathwatch - Core Rulebook.md"),
           "Deathwatch Core Rulebook (FFG, WH40K Roleplay), Ch. IV: Talents, "
           "Table 4-1", "plain_table",
           start_re=r"^Table 4.1: Talents", end_re=r"^Prerequisites:"),
    Source("ow", "Only War Core Rulebook",
           Path(f"{_W}/Only War/Rulebooks/Only War - Core Rulebook.md"),
           "Only War Core Rulebook (FFG, WH40K Roleplay), Ch. V: Talents and "
           "Traits", "prose_tier"),
    Source("bc", "Black Crusade Core Rulebook",
           Path(f"{_W}/Black Crusade/Rulebooks/Black Crusade - Core Rulebook.md"),
           "Black Crusade Core Rulebook (FFG, WH40K Roleplay), Talent "
           "Descriptions", "prose_tier"),
]


def _run_detector(src: Source) -> List[Talent]:
    if src.detector == "dh_table":
        return detect_dh_table(src.lines, _pages_for(src.lines), src.book)
    if src.detector == "plain_table":
        return detect_plain_table(src.lines, _pages_for(src.lines), src.book,
                                  src.start_re, src.end_re)
    if src.detector == "prose_tier":
        return detect_prose_tier(src.lines, _pages_for(src.lines), src.book)
    if src.detector == "prose_title":
        return detect_prose_title(src.lines, _pages_for(src.lines), src.book,
                                  src.start_re, src.end_re)
    raise ValueError(src.detector)


def _fresh_sources() -> List[Source]:
    return [Source(*(getattr(s, k) for k in
                     ("key", "book", "path", "citation", "detector",
                      "start_re", "end_re"))) for s in SOURCES]


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
            src.talents = _run_detector(src)
            src.coverage = f"ok — {len(src.talents)} talents from {path.name}"

    def all_talents(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for t in src.talents:
                yield src, t

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, t in self.all_talents(book):
            nm = t.name.lower()
            if nm == q:
                exact.append((src, t))
            elif q in nm:
                partial.append((src, t))
        return exact if exact else partial


# --------------------------------------------------------------------------- #
#  outputs                                                                    #
# --------------------------------------------------------------------------- #
def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# WARHAMMER 40,000 ROLEPLAY — TALENT INDEX — The New Path",
        "",
        "**Generated by `scripts/wh40krp_talent_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** These are **Warhammer 40,000 Roleplay** talents",
        "(Fantasy Flight Games' d100 line: Dark Heresy, Rogue Trader, Deathwatch,",
        "Only War, Black Crusade) — a DIFFERENT system from every D&D/GURPS index.",
        "Every row is stamped `system: WH40K Roleplay`; a 40K RP talent is SOURCE",
        "MATERIAL for the system-translator skill, not campaign RAW. `tier` and",
        "`aptitudes` appear where the book prints them (Only War / Black Crusade,",
        "and Only War aptitudes). `benefit` is the summary line / first sentence;",
        "the full text is at the cited page. Use `--export \"NAME\"` for the packet.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.talents)
        parsed_well += sum(1 for t in src.talents if t.quick_fields() >= 2)
        sources_out.append({"key": src.key, "book": src.book, "system": SYSTEM,
                            "citation": src.citation, "detector": src.detector,
                            "coverage": src.coverage,
                            "talents": [asdict(t) for t in src.talents]})
        md.append(f"## {src.book} — {len(src.talents)} talents  *(system: {SYSTEM})*")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.talents:
            md.append("| Talent | Tier | Prerequisites | Aptitudes | Benefit | Page |")
            md.append("|---|---|---|---|---|---|")
            for t in src.talents:
                nm = t.name + (" †" if t.group else "")
                md.append(f"| {nm} | {t.tier if t.tier else '—'} | "
                          f"{t.prerequisites or '—'} | {t.aptitudes or '—'} | "
                          f"{t.benefit or '—'} | {t.page if t.page is not None else '—'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/wh40krp_talent_harvest.py",
                    "system": SYSTEM, "corpus": str(corpus.base),
                    "total_talents": total, "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str], out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 8:
        print(f"'{name}' matches {len(hits)} talents; narrow with --book or the exact name:")
        for src, t in hits[:24]:
            print(f"  {t.name}   [{t.book}, p.{t.page}]")
        return 1
    packets = []
    for src, t in hits:
        body = [ln for ln in src.lines[t.start:t.end] if not PAGE.search(ln)]
        packets.append({
            "packet": "wh40krp-talent-for-translation",
            "instructions": ("A Warhammer 40,000 Roleplay talent (system: WH40K "
                             "Roleplay). Feed to the system-translator skill for "
                             "the paired 3.5e AND GURPS treatment. raw_block is "
                             "OCR text from the cited page."),
            "name": t.name, "system": SYSTEM,
            "source": {"book": t.book, "pdf_page": t.page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [t.start + 1, t.end], "citation": src.citation},
            "parsed": {k: v for k, v in asdict(t).items()
                       if k in ("tier", "prerequisites", "aptitudes", "benefit",
                                "group") and v not in (None, False)},
            "raw_block": re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip(),
        })
    text = json.dumps(packets if len(packets) > 1 else packets[0], indent=1)
    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


# --------------------------------------------------------------------------- #
#  selftest                                                                   #
# --------------------------------------------------------------------------- #
FIX_TAB = ("Talent Name\t\nPrerequisite\t\nBenefit\n"
           "Quick Draw\t\n—\t\nReady as a Free Action.\n"
           "Ambidextrous\t\nAg 30\t\nUse either hand equally well.\n"
           "Arms Master\t\nBS 30, Basic Weapon Training (any two)\t Use non-proficient weapons at –10 penalty.\n"
           "Assassin Strike\t\nAg 40, Acrobatic\t\nOn a successful Acrobatics Test after making a \n\t\n\t\nmelee attack, you may move as a Free Action.\n"
           "Basic Weapon Training†\t\n—\t\nUse weapon group without penalty.\n"
           "†Denotes Talent group.\n")

FIX_PLAIN = ("Table 4–1: Talents\nTalent Name \nPrerequisite \nBenefit\n"
             "Sprint \n— \nMove more quickly in combat.\n"
             "Bulging Biceps \nS 45 \nRemove bracing requirement for certain weapons.\n"
             "Blind Fighting \nPer 30 \nSuffer half the usual penalties when vision is \nobscured.\n"
             "Prerequisites: dummy\n")

FIX_TIER = ("AIR OF AUTHORITY\nTier: 1\nPrerequisite: Fellowship 30\n"
            "Aptitudes: Fellowship, Leadership\n"
            "The character was born to command those around him. Extra sentence.\n"
            "BERSERK CHARGE\nTier: 1\n"
            "The character hurls himself at enemies, gaining a bonus on the charge.\n")

FIX_TITLE = ("the full explanation of each Talent below.\n"
             "Air of Authority\nPrerequisites: Fellowship 30\n"
             "The Explorer was born to command those around him.\n"
             "Berserk Charge\n"
             "The Explorer puts his whole momentum behind his blows.\n"
             "Basic Weapon Training\nTalent Groups: Bolt, Las, SP\n"
             "Use the weapon group without penalty.\n"
             "V: Armoury\n")


def selftest(base: Path) -> int:
    failures: List[str] = []

    def names(ts):
        return {t.name.lower(): t for t in ts}

    tab = detect_dh_table(FIX_TAB.splitlines(), _pages_for(FIX_TAB.splitlines()), "X")
    nt = names(tab)
    for probe in ("quick draw", "ambidextrous", "arms master", "assassin strike",
                  "basic weapon training"):
        if probe not in nt:
            failures.append(f"[tab] missing {probe!r} (got {sorted(nt)})")
    if "quick draw" in nt and nt["quick draw"].prerequisites is not None:
        failures.append("[tab] Quick Draw should have no prerequisite")
    if "ambidextrous" in nt and nt["ambidextrous"].prerequisites != "Ag 30":
        failures.append(f"[tab] Ambidextrous prereq = {nt['ambidextrous'].prerequisites!r}")
    if "arms master" in nt and "Basic Weapon Training" not in (nt["arms master"].prerequisites or ""):
        failures.append("[tab] Arms Master merged prereq/benefit mis-split")
    if "assassin strike" in nt and "Free Action" not in (nt["assassin strike"].benefit or ""):
        failures.append("[tab] Assassin Strike wrapped benefit not joined")
    if "basic weapon training" in nt and not nt["basic weapon training"].group:
        failures.append("[tab] Basic Weapon Training † group flag missing")

    pl = detect_plain_table(FIX_PLAIN.splitlines(), _pages_for(FIX_PLAIN.splitlines()),
                            "X", r"^Table 4.1: Talents", r"^Prerequisites:")
    npl = names(pl)
    for probe in ("sprint", "bulging biceps", "blind fighting"):
        if probe not in npl:
            failures.append(f"[plain] missing {probe!r} (got {sorted(npl)})")
    if "sprint" in npl and npl["sprint"].prerequisites is not None:
        failures.append("[plain] Sprint should have no prerequisite")
    if "blind fighting" in npl and not (npl["blind fighting"].benefit or "").endswith("obscured."):
        failures.append("[plain] Blind Fighting wrapped benefit not joined")

    ti = detect_prose_tier(FIX_TIER.splitlines(), _pages_for(FIX_TIER.splitlines()), "X")
    nti = names(ti)
    for probe in ("air of authority", "berserk charge"):
        if probe not in nti:
            failures.append(f"[tier] missing {probe!r} (got {sorted(nti)})")
    if "air of authority" in nti:
        a = nti["air of authority"]
        if a.tier != 1 or a.prerequisites != "Fellowship 30" or not a.aptitudes:
            failures.append(f"[tier] Air of Authority parse = {(a.tier, a.prerequisites, a.aptitudes)}")
    if "berserk charge" in nti and nti["berserk charge"].prerequisites is not None:
        failures.append("[tier] Berserk Charge should have no prerequisite")

    tt = detect_prose_title(FIX_TITLE.splitlines(), _pages_for(FIX_TITLE.splitlines()),
                            "X", r"full explanation", r"V: Armoury")
    ntt = names(tt)
    for probe in ("air of authority", "berserk charge", "basic weapon training"):
        if probe not in ntt:
            failures.append(f"[title] missing {probe!r} (got {sorted(ntt)})")
    if "berserk charge" in ntt and ntt["berserk charge"].prerequisites is not None:
        failures.append("[title] Berserk Charge should have no prerequisite")
    if "basic weapon training" in ntt and not ntt["basic weapon training"].group:
        failures.append("[title] Basic Weapon Training group flag missing")

    # ---- live corpus checks ----
    if base.is_dir() and any((base / s.path).exists() for s in SOURCES):
        corpus = Corpus(base, _fresh_sources())
        per = {s.key: len(s.talents) for s in corpus.sources}
        total = sum(per.values())
        if total < 450:
            failures.append(f"only {total} talents indexed; expected > 450 ({per})")
        for key, floor in (("dh", 80), ("rt", 90), ("dw", 90), ("ow", 90), ("bc", 90)):
            if per.get(key, 0) < floor:
                failures.append(f"{key}: {per.get(key,0)} talents < floor {floor}")
        allnames = {t.name.lower() for _, t in corpus.all_talents()}
        for probe in ("quick draw", "rapid reload", "sprint", "nerves of steel",
                      "air of authority", "berserk charge", "swift attack"):
            if probe not in allnames:
                failures.append(f"live: expected talent '{probe}' not found")
        # prerequisites really parsed somewhere
        amb = [t for _, t in corpus.all_talents() if t.name.lower() == "ambidextrous"]
        if not any((t.prerequisites or "").lower().replace("ility", "") .startswith(("ag", "agi"))
                   for t in amb):
            failures.append(f"live: Ambidextrous prereq not parsed ({[t.prerequisites for t in amb]})")
        # tier captured for BC/OW
        if not any(t.tier for _, t in corpus.all_talents(book="bc")):
            failures.append("live: no tiers captured for Black Crusade")
    else:
        print("  [SKIP] 40K RP extractions not found — fixture checks only")

    for f in failures:
        print(f"SELFTEST FAIL: {f}")
    print("selftest: " + ("PASS" if not failures else f"{len(failures)} failure(s)"))
    return 0 if not failures else 1


# --------------------------------------------------------------------------- #
#  main                                                                       #
# --------------------------------------------------------------------------- #
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
        found = sorted({(t.name, t.book, t.page or -1, t.prerequisites or "—")
                        for _, t in corpus.all_talents(args.book) if q in t.name.lower()})
        for name, bk, page, pre in found:
            loc = bk if page < 0 else f"{bk}, p.{page}"
            print(f"  {name}   [{pre}; {loc}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.talents for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.talents):4d} talents" if src.talents else "   0 talents"
        print(f"  {src.book:34s} {status}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} WH40K Roleplay talents across "
          f"{sum(1 for s in corpus.sources if s.talents)} book(s). (system: {SYSTEM})")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
