#!/usr/bin/env python3
"""wfrp_creature_harvest.py — collate Warhammer Fantasy Roleplay (WFRP) creatures.

THE PROCESS (Chad, 2026-08-28): the reference layer welcomes OTHER game systems
as long as they are CLEARLY LABELLED by system, so the translator tools know
what they are looking at. This is the **Warhammer Fantasy Roleplay** (the d100
roleplay game — NOT the Warhammer Fantasy Battle tabletop WARGAME) creature /
bestiary index. Every row is stamped `"system": "WFRP"` so nothing here is ever
mistaken for the campaign's native 3.5e / GURPS RAW, nor for a WHFB wargame
profile (the single-digit M/WS/BS/S/T/W/I/A/Ld line — a SEPARATE wargame agent
harvests those; they are deliberately NOT collected here).

    reference/wfrp_creature_index.json  — every WFRP creature: name, the eight
                                          Main-Profile characteristics as
                                          percentages (WS BS S T Ag Int WP Fel),
                                          the eight Secondary-Profile values
                                          (A W SB TB M Mag IP FP), wounds,
                                          movement, and short Skills / Talents /
                                          Traits / Special-Rules / Armour /
                                          Weapons summaries; book + PDF page
    reference/wfrp_creature_index.md     — the same index, for human eyes

The raw text stays on I:\\Sourcebooks; `--export` emits a TRANSLATOR-READY
packet — a WFRP block the system-translator skill converts to the hybrid's
3.5e + GURPS pair (BOTH still required in that skill's output).

WORKFLOW
    python wfrp_creature_harvest.py                    # (re)build the index
    python wfrp_creature_harvest.py --search "goblin"  # find candidates
    python wfrp_creature_harvest.py --export "Bestigor"
    python wfrp_creature_harvest.py --selftest

GOVERNING SOURCES
    I:\\Sourcebooks\\_text\\Warhammer\\Fantasy\\ — a MIX of WFRP roleplay books
    and WHFB wargame army books. Only the ROLEPLAY books carry the percentage
    profile, and only they are configured here. A WFRP roleplay stat block is a
    vertical layout: the name, then a `Main Profile` header, then the eight
    characteristic LABELS run down the page (WS / BS / S / T / Ag / Int / WP /
    Fel), then the eight VALUES run down the page (percentages like `45%`, or
    bare numbers, sometimes with a `(bonus)` such as `30 (3)`), then a
    `Secondary Profile` header with its own eight labels (A / W / SB / TB / M /
    Mag / IP / FP) and eight values, then Skills / Talents / Traits / Special
    Rules / Armour / Weapons / Trappings. Two detectors anchor on this:

      * MAIN-PROFILE (Old World Bestiary, Tome of Corruption, Renegade Crowns,
        Old World Armoury): a `Main Profile` header sits above the label run.
        The name is the nearest `— Name Statistics —` decorative line, or the
        plain name line above a `Career:` / `Race:` pair. Career ADVANCE SCHEMES
        (whose profile values are all `+X%` advances) are rejected — they are
        career progressions, not creatures.

      * HEADERLESS (The Thousand Thrones, a WFRP adventure): the same vertical
        label run WS…Fel, but with NO `Main Profile` header and the secondary
        stats folded into a `Combat` line (`Attacks: 1; Movement: 4; Wounds:
        12`). The name sits two lines up, above a race/career subtitle line
        (`Male Marienburger Human Foreman, ex-Stevedore`), past the description
        prose. Only blocks whose name resolves through that subtitle are kept,
        so the adventure yields creatures without emitting prose fragments.

    A configured source whose file is missing prints NO COVERAGE. Garbage names
    (section headers, prose, label fragments) are filtered out. The extractions
    are born-digital (PyMuPDF text layer — exact characters, not OCR); the PDFs
    stand behind every extraction. All five configured books are WFRP 2nd
    edition (Black Industries / Fantasy Flight Games, 2005-2008).
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
OUT_JSON = REPO / "reference" / "wfrp_creature_index.json"
OUT_MD = REPO / "reference" / "wfrp_creature_index.md"
SYSTEM = "WFRP"

PAGE = re.compile(r"\[PDF page (\d+)\]")

# The eight WFRP Main-Profile characteristics, in profile order, and the eight
# Secondary-Profile values.
MAIN_KEYS = ["ws", "bs", "s", "t", "ag", "int", "wp", "fel"]
SEC_KEYS = ["a", "w", "sb", "tb", "m", "mag", "ip", "fp"]
MAIN_LABELS = set(MAIN_KEYS)
SEC_LABELS = set(SEC_KEYS)
ALL_LABELS = MAIN_LABELS | SEC_LABELS
ROW_LABELS = {"starting", "advance", "current"}

# ── value tokens ────────────────────────────────────────────────────────────
# A characteristic value: a percentage (45%), a bare number (14), each with an
# optional inline (bonus) such as "30 (3)"; a lone "(3)" bonus token; an advance
# modifier (+10%); or a dash meaning "no score".
V_PLAIN = re.compile(r"^(\d{1,3})\s*%?\s*(?:\(\s*\d+\s*\))?$")
V_ADV = re.compile(r"^\+\s*\d{1,3}\s*%?$")
V_BONUS = re.compile(r"^\(\s*\d+\s*\)$")
V_DASH = re.compile(r"^[\u2014\u2013\u2012-]+$")


def _classify(tok: str) -> Optional[Tuple[str, Optional[str]]]:
    """Classify one whitespace-delimited token from a profile row."""
    tok = tok.strip()
    m = V_PLAIN.match(tok)
    if m:
        return "val", m.group(1)
    if V_ADV.match(tok):
        return "adv", None
    if V_BONUS.match(tok):
        return "bonus", None
    if V_DASH.match(tok):
        return "dash", "\u2014"
    return None


def _is_label_line(s: str, label_set=ALL_LABELS) -> bool:
    """A profile label line: a run of characteristic labels alone on a line."""
    toks = s.replace("\t", " ").split()
    return bool(toks) and all(t.strip(".").lower() in label_set for t in toks)


# ── name filtering ──────────────────────────────────────────────────────────

_LIGATURES = {"\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl",
              "\ufb03": "ffi", "\ufb04": "ffl", "\ufb05": "st", "\ufb06": "st"}


def _deligature(s: str) -> str:
    for lig, rep in _LIGATURES.items():
        s = s.replace(lig, rep)
    return s


NAME_REJECT_EXACT = {
    "ws", "bs", "s", "t", "ag", "int", "wp", "fel", "a", "w", "sb", "tb", "m",
    "mag", "ip", "fp", "main profile", "secondary profile", "profile",
    "starting", "advance", "current", "movement", "move", "wounds", "wound",
    "skills", "skill", "talents", "talent", "traits", "trait", "special rules",
    "special rule", "armour", "armor", "armour points", "weapons", "weapon",
    "trappings", "career", "careers", "race", "class", "combat", "attacks",
    "attack", "slaughter margin", "chapter", "contents", "appendix", "index",
    "introduction", "adversaries", "bestiary", "creatures", "creature",
    "description", "descriptions", "background", "history", "appearance",
    "summary", "abilities", "overview", "the end", "game master", "notes",
    "note", "optional", "new talents", "mutations", "magic", "common view",
    "our own words", "special abilities", "typical", "statistics",
}
NAME_REJECT_PREFIX = re.compile(
    r"^(Chapter\b|Appendix\b|Section\b|Special Rules?\b|Career Exits?\b|"
    r"Career Entries?\b|Using |The following\b|Optional Rules?\b|Table \d|"
    r"Skills? and\b|New Rules?\b|Casting (Number|Time)\b|Ingredient\b|"
    r"Armour Points?\b|Slaughter Margin\b)", re.IGNORECASE)

# A race/career subtitle line (the line under a named NPC in adventure blocks),
# used to locate the name two lines above the profile in the headerless format.
SUBTITLE_RX = re.compile(
    r"\b(Human|Elf|Elves|Dwarf|Dwarfs|Halfling|Gnome|Ogre|Skaven|Goblin|Orc|"
    r"Beastman|Beastmen|Mutant|Norse|Norscan|Kislevite|Marienburger|"
    r"Bretonnian|Tilean|Estalian|Reiklander|Averlander|Nordlander|Male|"
    r"Female|ex-)\b", re.IGNORECASE)
# Words that mark a career/kind subtitle even without a race token.
SUBTITLE_CAREER = re.compile(
    r"\b(Watchman|Watchmen|Soldier|Foreman|Stevedore|Mercenary|Wizard|Witch|"
    r"Priest|Knight|Noble|Merchant|Physician|Barber-?Surgeon|Interrogator|"
    r"Torturer|Bodyguard|Thief|Cultist|Sergeant|Captain|Guard|Bandit|Scout|"
    r"Coachman|Boatman|Roadwarden|Rat Catcher|Bounty Hunter|Initiate|Zealot)\b",
    re.IGNORECASE)

DECOR = re.compile(r"^\s*[\u2014\u2013\u2012-]\s*(.+?)\s*[\u2014\u2013\u2012-]\s*$")


def _smart_title(s: str) -> str:
    out = []
    for w in s.split():
        out.append(w[:1].upper() + w[1:] if w and w.islower() else w)
    return " ".join(out)


def _clean_name(raw: str) -> Optional[Tuple[str, Optional[str]]]:
    """Return (name, role) or None if the line is not a plausible creature name.
    A trailing ', role' (Johann Schmidt, Typical Soldier) splits into a role."""
    s = _deligature(re.sub(r"\s+", " ", raw).strip())
    s = s.strip(" \u2014\u2013\u2012-\u2020\u2021*").strip()
    # Drop an unbalanced trailing/leading paren left by a wrapped career line.
    if s.endswith(")") and "(" not in s:
        s = s[:-1].strip()
    if s.startswith("(") and ")" not in s:
        s = s[1:].strip()
    if not s:
        return None
    if re.match(r"^p(age|\.)?\s*\d+$", s, re.IGNORECASE):   # a page reference
        return None
    role = None
    if "," in s:
        head, tail = s.split(",", 1)
        if head.strip():
            s, role = head.strip(), tail.strip() or None
    if not (2 <= len(s) <= 46):
        return None
    if s.isdigit() or s.endswith((".", ";", ":", "!", "?")):
        return None
    low = s.lower()
    if low in NAME_REJECT_EXACT or NAME_REJECT_PREFIX.match(s) or _is_label_line(s):
        return None
    letters = sum(c.isalpha() for c in s)
    if letters < max(3, len(s) // 2):
        return None
    if len(s.split()) > 7:
        return None
    return _smart_title(s), role


@dataclass
class WFRPCreature:
    name: str
    book: str
    page: Optional[int]
    start: int
    end: int
    system: str = SYSTEM
    edition: str = "WFRP 2e"
    role: Optional[str] = None
    # Main Profile (percentages)
    ws: Optional[str] = None
    bs: Optional[str] = None
    s: Optional[str] = None
    t: Optional[str] = None
    ag: Optional[str] = None
    int: Optional[str] = None       # noqa: A003 — WFRP characteristic key is "int"
    wp: Optional[str] = None
    fel: Optional[str] = None
    # Secondary Profile
    a: Optional[str] = None
    w: Optional[str] = None
    sb: Optional[str] = None
    tb: Optional[str] = None
    m: Optional[str] = None
    mag: Optional[str] = None
    ip: Optional[str] = None
    fp: Optional[str] = None
    # convenience / extras
    wounds: Optional[str] = None
    movement: Optional[str] = None
    attacks: Optional[str] = None
    skills: Optional[str] = None
    talents: Optional[str] = None
    traits: Optional[str] = None
    special_rules: Optional[str] = None
    armour: Optional[str] = None
    weapons: Optional[str] = None
    trappings: Optional[str] = None
    slaughter_margin: Optional[str] = None

    def quick_fields(self) -> int:
        """How many of the eight Main-Profile characteristics parsed to a number."""
        return sum(1 for k in MAIN_KEYS
                   if (getattr(self, k) or "").isdigit())


# ── profile value collection ────────────────────────────────────────────────

def _collect_values(lines: List[str], k: int, n: int,
                    label_set) -> Tuple[List[str], int]:
    """From line k, collect up to eight profile values (percentages/numbers,
    or dashes), skipping label lines, row-label words (Starting/Advance/
    Current), and whole advance rows (any '+' token). Stop at the first
    non-value line (e.g. Secondary Profile / Skills)."""
    vals: List[str] = []
    while k < n and len(vals) < 8:
        raw = lines[k]
        s = raw.strip()
        if s == "" or PAGE.search(raw):
            k += 1
            continue
        low = s.lower()
        if low in ROW_LABELS:
            k += 1
            continue
        toks = s.split()
        if _is_label_line(s, label_set):
            k += 1
            continue
        if any(t.startswith("+") for t in toks):     # an advance row — skip it
            k += 1
            continue
        stop = False
        for t in toks:
            c = _classify(t)
            if c is None:
                stop = True
                break
            kind, val = c
            if kind in ("adv", "bonus"):
                continue
            vals.append(val)
            if len(vals) >= 8:
                break
        if stop:
            break
        k += 1
    return vals[:8], k


def _apply(creature: WFRPCreature, keys: List[str], values: List[str]) -> None:
    for key, val in zip(keys, values):
        setattr(creature, key, val)


# ── trailing block (Skills / Talents / … ) ──────────────────────────────────

STOP_KEYWORD = re.compile(
    r"^\s*(Main Profile|Secondary Profile|Skills?|Talents?|Traits?|"
    r"Special Rules?|Armou?r|Armou?r Points?|Weapons?|Trappings?|"
    r"Slaughter Margin|Combat|Career|Movement|Wounds?|Attacks?|Magic|"
    r"Spells?|Optional|Mutations?)\b", re.IGNORECASE)

_EXTRA_FIELDS = [
    (re.compile(r"^\s*Skills?\s*:?\s*(.+)$", re.I), "skills"),
    (re.compile(r"^\s*Talents?\s*:?\s*(.+)$", re.I), "talents"),
    (re.compile(r"^\s*Traits?\s*:?\s*(.+)$", re.I), "traits"),
    (re.compile(r"^\s*Special Rules?\s*:?\s*(.*)$", re.I), "special_rules"),
    (re.compile(r"^\s*Armou?r\s*:\s*(.+)$", re.I), "armour"),
    (re.compile(r"^\s*Weapons?\s*:?\s*(.+)$", re.I), "weapons"),
    (re.compile(r"^\s*Trappings?\s*:?\s*(.+)$", re.I), "trappings"),
    (re.compile(r"^\s*Slaughter Margin\s*:?\s*(.+)$", re.I), "slaughter_margin"),
]
COMBAT_RX = re.compile(
    r"Attacks?\s*:?\s*([0-9]+).*?Movement\s*:?\s*([0-9]+).*?Wounds?\s*:?\s*([0-9]+)",
    re.IGNORECASE | re.DOTALL)
MOVE_RX = re.compile(r"^\s*Movement\s*:?\s*([0-9]+)", re.I)
WOUNDS_RX = re.compile(r"^\s*Wounds?\s*:?\s*([0-9]+)", re.I)


def _extract_extras(c: WFRPCreature, body: List[str]) -> None:
    n = len(body)
    joined = " ".join(x.strip() for x in body[:40])
    mc = COMBAT_RX.search(joined)
    if mc:
        c.attacks = c.attacks or mc.group(1)
        c.movement = c.movement or mc.group(2)
        c.wounds = c.wounds or mc.group(3)
    for i, raw in enumerate(body):
        line = raw.strip()
        if not line:
            continue
        if c.movement is None:
            mm = MOVE_RX.match(line)
            if mm:
                c.movement = mm.group(1)
        if c.wounds is None:
            mw = WOUNDS_RX.match(line)
            if mw:
                c.wounds = mw.group(1)
        for rx, attr in _EXTRA_FIELDS:
            if getattr(c, attr) is not None:
                continue
            m = rx.match(line)
            if not m:
                continue
            chunk = [m.group(1).strip()] if m.group(1).strip() else []
            j = i + 1
            # Slaughter Margin is a single short phrase — gather only enough to
            # close an open "(…)" parenthetical, never the next section's prose.
            if attr == "slaughter_margin":
                while (j < n and j < i + 4
                       and " ".join(chunk).count("(") > " ".join(chunk).count(")")):
                    nxt = body[j].strip()
                    if not nxt or PAGE.search(body[j]):
                        break
                    chunk.append(nxt)
                    j += 1
            else:
                while j < n and len(" ".join(chunk)) < 400:
                    nxt = body[j].strip()
                    if not nxt or PAGE.search(body[j]):
                        j += 1
                        if not chunk:
                            continue
                        break
                    if STOP_KEYWORD.match(nxt) or _is_label_line(nxt) or DECOR.match(nxt):
                        break
                    chunk.append(nxt)
                    j += 1
            text = _deligature(re.sub(r"\s+", " ", " ".join(chunk)).strip())
            text = re.sub(r"^[•\-\u2022\s]+", "", text).strip().rstrip(".")
            if len(text) > 240:
                text = text[:237].rstrip() + "\u2026"
            if text:
                setattr(c, attr, text)
            break


# ── name resolution above a profile anchor ──────────────────────────────────

def _context_above(lines: List[str], anchor: int, limit: int = 20
                   ) -> List[Tuple[int, str]]:
    """The nearest non-blank content lines above the anchor (nearest first),
    dropping structural lines (Main/Secondary Profile, label lines, row-labels)."""
    ctx: List[Tuple[int, str]] = []
    j = anchor - 1
    while j >= 0 and len(ctx) < limit:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            j -= 1
            continue
        low = s.lower()
        if (low in ("main profile", "secondary profile") or low in ROW_LABELS
                or _is_label_line(s)):
            j -= 1
            continue
        ctx.append((j, s))
        j -= 1
    return ctx


def _strip_stat_suffix(inner: str) -> str:
    return re.sub(r"\s*(Statistics|Advance Scheme|Profile|Stats)\s*$", "",
                  inner, flags=re.IGNORECASE).strip()


_CAREER_LINE = re.compile(r"^(Career|Careers?|Race|Class)\b\s*:", re.IGNORECASE)

# Lowercase words that betray a prose fragment rather than a proper name. Common
# name connectors (and/the/von/van/de/…) are deliberately NOT in this set, so
# multi-NPC labels like "Klaus and Ernst" or "Lucas von Speier" survive.
PROSE_WORDS = {
    "is", "are", "was", "were", "be", "been", "being", "am", "has", "have",
    "had", "can", "could", "will", "would", "should", "do", "does", "did",
    "that", "which", "who", "whom", "whose", "whatever", "otherwise", "by",
    "from", "into", "onto", "with", "within", "this", "these", "those", "it",
    "its", "they", "them", "their", "he", "she", "his", "her", "all", "very",
    "more", "most", "of", "in", "on", "to", "as", "at", "for", "but", "not",
    "so", "up", "out", "if", "when", "then", "than", "stares", "keeps",
    "prefers", "consumes", "believes", "spawned", "rolls", "roll", "here",
    "there", "over", "about", "each", "any", "some", "such",
}
NAME_CONNECTORS = {"and", "the", "von", "van", "de", "der", "du", "zu",
                   "und", "le", "la", "des"}


def _is_subtitle(t: str) -> bool:
    """A short race/career subtitle line (not a full description sentence)."""
    if len(t.split()) > 8 or t.rstrip().endswith((".", "!", "?", ":", ";")):
        return False
    return bool(SUBTITLE_RX.search(t) or SUBTITLE_CAREER.search(t))


def _proper_name(raw: str) -> Optional[Tuple[str, Optional[str]]]:
    """Strict name test for the headerless (adventure) format: a Title-Case
    proper-noun NPC/label of up to five words with no prose stopwords, so a
    description sentence above a profile can never masquerade as a name."""
    s = _deligature(re.sub(r"\s+", " ", raw).strip())
    s = s.strip(" —–‒-†‡*\"'“”").strip()
    if not s or s.rstrip().endswith((".", ";", ":", "!", "?")):
        return None
    words = s.replace("(", " ").replace(")", " ").split()
    if not (1 <= len(words) <= 5):
        return None
    for w in words:
        lw = re.sub(r"[^a-z]", "", w.lower())
        if lw in PROSE_WORDS:
            return None
        # every alphabetic word must be capitalised or a known name connector
        if lw and lw not in NAME_CONNECTORS and not (w[0].isupper() or w[0].isdigit()):
            return None
    return _clean_name(s)


def _resolve_name(lines: List[str], anchor: int, has_header: bool
                  ) -> Optional[Tuple[int, str, Optional[str]]]:
    """Resolve the creature name for a profile whose main-label run starts at
    `anchor`. Returns (name_line_index, name, role) or None (reject).

    Blocks that carry a `Main Profile` header (the bestiary/Chaos/GM books) get
    the decorative / Career-Race / nearest-line resolver. Headerless blocks (an
    adventure's NPCs) get a STRICT resolver: only a proper name directly above a
    race/career subtitle is accepted, so prose never becomes a creature name."""
    ctx = _context_above(lines, anchor)
    if not ctx:
        return None

    if not has_header:
        # HEADERLESS: strict "Name directly above race/career subtitle" only.
        for p in range(len(ctx)):
            if not _is_subtitle(ctx[p][1]):
                continue
            if p + 1 < len(ctx):
                nm = _proper_name(ctx[p + 1][1])
                if nm:
                    return ctx[p + 1][0], nm[0], ctx[p][1].strip()
        return None

    # (1) A decorative "— Name Statistics —" line immediately above.
    idx0, txt0 = ctx[0]
    md = DECOR.match(txt0)
    if md:
        inner = md.group(1).strip()
        if re.search(r"Advance Scheme\s*$", inner, re.IGNORECASE):
            return None                     # a career advance scheme, not a creature
        cleaned = _clean_name(_strip_stat_suffix(inner))
        if cleaned:
            return idx0, cleaned[0], cleaned[1]

    # (2) A named NPC block: "Name / Career: … / Race: …" above the profile.
    #     The name sits ABOVE the whole Career/Race cluster, so find the topmost
    #     Career/Race line and take the first clean name above it — a wrapped
    #     "(ex-…)" career tail ("Wizard)", "page 96") is thus never a name.
    career_positions = [p for p, (_, t) in enumerate(ctx[:6]) if _CAREER_LINE.match(t)]
    if career_positions:
        for p in range(max(career_positions) + 1, min(len(ctx), max(career_positions) + 5)):
            cleaned = _clean_name(ctx[p][1])
            if cleaned:
                return ctx[p][0], cleaned[0], cleaned[1]

    # (3) Fallback: the name heading above the description prose. Climb up,
    #     skipping description sentences (rejected by _proper_name), until the
    #     short proper-noun heading (e.g. "War Ponies") — stopping at the
    #     previous block's Skills/Weapons/… so we never cross into it.
    for pidx, t in ctx[:10]:
        if STOP_KEYWORD.match(t) or _CAREER_LINE.match(t):
            break
        nm = _proper_name(t)
        if nm:
            return pidx, nm[0], nm[1]
    return None


# ── the anchor: an ordered vertical run of the eight Main-Profile labels ─────

def _main_label_run(lines: List[str], i: int, n: int) -> Optional[int]:
    """If a vertical WS/BS/S/T/Ag/Int/WP/Fel label run starts at line i, return
    the index just past the 'Fel' label; else None."""
    if lines[i].strip().lower() != "ws":
        return None
    want = MAIN_KEYS[1:]
    k = i + 1
    for label in want:
        while k < n and (lines[k].strip() == "" or PAGE.search(lines[k])):
            k += 1
        if k >= n or lines[k].strip().lower() != label:
            return None
        k += 1
    return k


def _sec_label_run(lines: List[str], k: int, n: int) -> Optional[int]:
    """If a Secondary-Profile label run (A/W/SB/TB/M/Mag/IP/FP) begins at/after
    k (allowing a 'Secondary Profile' header and blanks), return the index past
    'FP'; else None."""
    j = k
    seen_header = False
    steps = 0
    while j < n and steps < 6:
        s = lines[j].strip()
        if s == "" or PAGE.search(lines[j]):
            j += 1
            continue
        if s.lower() == "secondary profile":
            seen_header = True
            j += 1
            steps += 1
            continue
        break
    if j >= n or lines[j].strip().lower() != "a":
        return None
    k2 = j + 1
    for label in SEC_KEYS[1:]:
        while k2 < n and (lines[k2].strip() == "" or PAGE.search(lines[k2])):
            k2 += 1
        if k2 >= n or lines[k2].strip().lower() != label:
            return None
        k2 += 1
    return k2


def detect_wfrp(lines: List[str], pages: List[int], book: str) -> List[WFRPCreature]:
    n = len(lines)
    starts: List[Tuple[int, str, Optional[str], List[str], List[str], int]] = []
    used = set()
    for i in range(n):
        past_main = _main_label_run(lines, i, n)
        if past_main is None:
            continue
        main_vals, after_main = _collect_values(lines, past_main, n, MAIN_LABELS)
        if len(main_vals) < 8 or sum(v.isdigit() for v in main_vals) < 5:
            continue                        # not a real profile (e.g. advance scheme)
        # Does a "Main Profile" header sit just above the label run? (True for
        # the bestiary/Chaos/GM books; False for the adventure's NPC blocks.)
        has_header = False
        j = i - 1
        while j >= 0:
            s = lines[j].strip()
            if s == "" or PAGE.search(lines[j]):
                j -= 1
                continue
            has_header = s.lower() == "main profile"
            break
        got = _resolve_name(lines, i, has_header)
        if got is None or got[0] in used:
            continue
        nidx, name, role = got
        used.add(nidx)
        # Secondary profile (optional — absent in the headerless adventure format)
        sec_vals: List[str] = []
        past_sec = _sec_label_run(lines, after_main, n)
        if past_sec is not None:
            sec_vals, _ = _collect_values(lines, past_sec, n, SEC_LABELS)
        starts.append((nidx, name, role, main_vals, sec_vals, after_main))

    starts.sort()
    out: List[WFRPCreature] = []
    for idx, (nidx, name, role, mvals, svals, body_start) in enumerate(starts):
        e = starts[idx + 1][0] if idx + 1 < len(starts) else min(n, nidx + 90)
        e = min(e, body_start + 70)
        c = WFRPCreature(name=name, book=book, page=pages[nidx], start=nidx,
                         end=e, role=role)
        _apply(c, MAIN_KEYS, mvals)
        if len(svals) == 8:
            _apply(c, SEC_KEYS, svals)
            if c.w and c.w.isdigit():
                c.wounds = c.wounds or c.w
            if c.m and c.m.isdigit():
                c.movement = c.movement or c.m
            if c.a and c.a.isdigit():
                c.attacks = c.attacks or c.a
        _extract_extras(c, lines[body_start:e])
        out.append(c)
    return _finalize(out)


def _finalize(items: List[WFRPCreature]) -> List[WFRPCreature]:
    """Drop running headers (a name recurring 3+ times in one book) and collapse
    exact duplicate names within a book to the first."""
    from collections import Counter
    cnt = Counter(c.name.lower() for c in items)
    out, seen = [], set()
    for c in items:
        key = c.name.lower()
        if cnt[key] >= 3 or key in seen:
            continue
        seen.add(key)
        out.append(c)
    return out


# ── sources ─────────────────────────────────────────────────────────────────

@dataclass
class Source:
    key: str
    book: str
    path: Path
    citation: str
    coverage: str = "pending"
    lines: List[str] = field(default_factory=list)
    creatures: List[WFRPCreature] = field(default_factory=list)


_W = "Warhammer/Fantasy"
SOURCES: List[Source] = [
    Source("owb", "WFRP: Old World Bestiary",
           Path(f"{_W}/Old_World_Bestiary.md"),
           "WFRP Old World Bestiary (Black Industries/Green Ronin, 2005; WFRP 2e)"),
    Source("toc", "WFRP: Tome of Corruption",
           Path(f"{_W}/Tome_of_Corruption.md"),
           "WFRP Tome of Corruption (Black Industries, 2006; WFRP 2e), Chaos bestiary"),
    Source("rc", "WFRP: Renegade Crowns",
           Path(f"{_W}/Renegade_Crowns.md"),
           "WFRP Renegade Crowns (Black Industries, 2007; WFRP 2e), Border Princes NPCs"),
    Source("owa", "WFRP: Old World Armoury",
           Path(f"{_W}/Old_World_Armoury.md"),
           "WFRP Old World Armoury (Black Industries/Green Ronin, 2005; WFRP 2e), animals"),
    Source("ttt", "WFRP: The Thousand Thrones",
           Path(f"{_W}/The_Thousand_Thrones.md"),
           "WFRP The Thousand Thrones (Black Industries, 2008; WFRP 2e), campaign NPCs"),
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
    return [Source(s.key, s.book, s.path, s.citation) for s in SOURCES]


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
            src.creatures = detect_wfrp(src.lines, pages, src.book)
            src.coverage = f"ok — {len(src.creatures)} creatures from {path.name}"

    def all_creatures(self, book: Optional[str] = None):
        for src in self.sources:
            if book and book.lower() not in (src.key.lower(), src.book.lower()):
                continue
            for c in src.creatures:
                yield src, c

    def find(self, query: str, book: Optional[str] = None):
        q = query.strip().lower()
        exact, partial = [], []
        for src, c in self.all_creatures(book):
            nm = c.name.lower()
            if nm == q:
                exact.append((src, c))
            elif q in nm:
                partial.append((src, c))
        return exact if exact else partial


def _profile_str(c: WFRPCreature) -> str:
    return "/".join((getattr(c, k) or "\u2014") for k in MAIN_KEYS)


def _sec_str(c: WFRPCreature) -> str:
    return "/".join((getattr(c, k) or "\u2014") for k in SEC_KEYS)


def write_index(corpus: Corpus) -> Tuple[int, int]:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    parsed_well = 0
    sources_out = []
    md: List[str] = [
        "# WARHAMMER FANTASY ROLEPLAY (WFRP) — CREATURE / BESTIARY INDEX",
        "",
        "**Generated by `scripts/wfrp_creature_harvest.py`. Do not hand-edit;",
        "rerun the harvest.** These are **Warhammer Fantasy Roleplay** (the d100",
        "roleplay game, WFRP 2nd edition) creatures — a DIFFERENT game system",
        "from the campaign's 3.5e / GURPS RAW, and DIFFERENT from the Warhammer",
        "Fantasy Battle tabletop WARGAME (whose single-digit M/WS/BS/S/T/W/I/A/Ld",
        "profiles are NOT collected here). Every row is stamped `system: WFRP`; a",
        "WFRP block is SOURCE MATERIAL for the system-translator skill, not",
        "campaign RAW. The Main Profile is **WS BS S T Ag Int WP Fel** (as",
        "percentages); the Secondary Profile is **A W SB TB M Mag IP FP**. A",
        "`\u2014` is a no-score or a field the source did not cleanly yield. Use",
        "`--export \"NAME\"` for the translator packet.",
        "",
    ]
    for src in corpus.sources:
        total += len(src.creatures)
        parsed_well += sum(1 for c in src.creatures if c.quick_fields() >= 6)
        sources_out.append({"key": src.key, "book": src.book, "system": SYSTEM,
                            "citation": src.citation, "coverage": src.coverage,
                            "creatures": [asdict(c) for c in src.creatures]})
        md.append(f"## {src.book} — {len(src.creatures)} creatures  *(system: {SYSTEM})*")
        md.append("")
        md.append(f"*Source: {src.citation}.*  ")
        md.append(f"*Harvest: {src.coverage}.*")
        md.append("")
        if src.creatures:
            md.append("| Creature | WS/BS/S/T/Ag/Int/WP/Fel | A/W/SB/TB/M/Mag/IP/FP | W | M | Page |")
            md.append("|---|---|---|---|---|---|")
            for c in src.creatures:
                md.append(f"| {c.name} | {_profile_str(c)} | {_sec_str(c)} | "
                          f"{c.wounds or '\u2014'} | {c.movement or '\u2014'} | "
                          f"{c.page if c.page is not None else '\u2014'} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/wfrp_creature_harvest.py",
                    "system": SYSTEM, "corpus": str(corpus.base),
                    "total_creatures": total, "sources": sources_out}, indent=1),
        encoding="utf-8")
    return total, parsed_well


def export_packet(corpus: Corpus, name: str, book: Optional[str],
                  out: Optional[Path]) -> int:
    hits = corpus.find(name, book)
    if not hits:
        print(f"Not found: '{name}'. Try --search.", file=sys.stderr)
        return 1
    if len(hits) > 6:
        print(f"'{name}' matches {len(hits)} creatures; narrow with --book or the exact name:")
        for src, c in hits[:20]:
            print(f"  {c.name}   [{c.book}, p.{c.page}]")
        return 1
    packets = []
    for src, c in hits:
        body = [ln for ln in src.lines[c.start:c.end] if not PAGE.search(ln)]
        parsed = {k: getattr(c, k) for k in
                  (MAIN_KEYS + SEC_KEYS + ["role", "wounds", "movement",
                   "attacks", "skills", "talents", "traits", "special_rules",
                   "armour", "weapons", "trappings", "slaughter_margin"])
                  if getattr(c, k)}
        packets.append({
            "packet": "wfrp-creature-for-translation",
            "instructions": ("A Warhammer Fantasy Roleplay (d100, WFRP 2e) creature "
                             "(system: WFRP). Feed to the system-translator skill to "
                             "build the paired 3.5e AND GURPS statlines — both "
                             "required. Main Profile is percentages (WS BS S T Ag Int "
                             "WP Fel); Secondary is A W SB TB M Mag IP FP. The "
                             "raw_block is born-digital source text; check oddities "
                             "against the source PDF."),
            "name": c.name, "system": SYSTEM, "edition": c.edition,
            "source": {"book": c.book, "pdf_page": c.page,
                       "extraction": str(corpus.base / src.path),
                       "lines": [c.start + 1, c.end], "citation": src.citation},
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


# ── fixtures & selftest ─────────────────────────────────────────────────────

FIXTURE_MAINPROF = """## [PDF page 84]
Bestigors
The toughest and most experienced Beastmen are known as Bestigors.
— Bestigor Statistics —
Main Profile
WS
BS
S
T
Ag
Int
WP
Fel
45%
25%
41%
47%
37%
25%
35%
27%
Secondary Profile
A
W
SB
TB
M
Mag
IP
FP
1
14
4
4
5
0
0
0
Skills: Command, Concealment, Dodge Blow, Intimidate +10%
Talents: Keen Senses, Menacing, Rover, Strike Mighty Blow
Special Rules:
\u2022 Chaos Mutations: Animalistic Legs, Bestial Appearance, and Large Horns.
Armour: Medium Armour (Full Mail Armour)
Weapons: Great Weapon, Hand Weapon, Horns (SB Damage)
Slaughter Margin: Challenging

Bloody Mary
Career: Physician (ex-Barber Surgeon, ex-Interrogator)
Race: Human
Main Profile
WS
BS
S
T
Ag
Int
WP
Fel
48%
28%
51%
45%
53%
50%
56%
41%
Secondary Profile
A
W
SB
TB
M
Mag
IP
FP
1
15
5
4
4
0
6
0
Skills: Charm, Heal +20%, Perception +10%, Torture
Talents: Menacing, Surgery, Wrestling
Armour: Medium Armour (Leather Jerkin and Chain Shirt)
Weapons: Flail
"""

FIXTURE_ADVANCE = """## [PDF page 82]
Shaman
Shamans are the key religious figures of the monstrous tribes.
— Shaman Advance Scheme —
Main Profile
WS
BS
S
T
Ag
Int
WP
Fel
+10% +10% +5% +10% +10% +15% +20% +15%
Secondary Profile
A
W
SB
TB
M
Mag
IP
FP
\u2014
+4
\u2014
\u2014
\u2014
+2
\u2014
\u2014
Skills: Academic Knowledge, Channelling, Charm
"""

FIXTURE_HEADERLESS = """## [PDF page 22]
20
Chapter I: The Call of Chaos
Horst Breuer
Male Marienburger Human Foreman, ex-Stevedore
Horst Breuer is a dock foreman for one of the local guilds of stevedores.
He is a simple, no-nonsense fellow with little patience for elaborate stories.
WS
BS
S
T
Ag
Int
WP
Fel
36
32
45 (4)
42 (4)
41
35
43
39
Skills: Command (Fel), Dodge Blow (Ag), Gamble (Int), Haggle (Fel)
Talents: Coolheaded, Lightning Reflexes, Public Speaking, Very Strong
Combat
Attacks: 1; Movement: 4; Wounds: 11
Armour (Light): Leather Jack (Arms 1, Body 1)
Weapons: Hand Weapon
"""


def selftest(base: Path) -> int:
    failures: List[str] = []

    # ── fixture: MAIN-PROFILE (creature + named NPC) ────────────────────────
    lines = FIXTURE_MAINPROF.splitlines()
    got = detect_wfrp(lines, _pages_for(lines), "WFRP: Old World Bestiary")
    names = [c.name for c in got]
    if names != ["Bestigor", "Bloody Mary"]:
        failures.append(f"main-profile fixture names {names}, wanted "
                        f"['Bestigor', 'Bloody Mary']")
    else:
        b = got[0]
        prof = (b.ws, b.bs, b.s, b.t, b.ag, b.int, b.wp, b.fel)
        if prof != ("45", "25", "41", "47", "37", "25", "35", "27"):
            failures.append(f"Bestigor main profile {prof}")
        sec = (b.a, b.w, b.sb, b.tb, b.m, b.mag, b.ip, b.fp)
        if sec != ("1", "14", "4", "4", "5", "0", "0", "0"):
            failures.append(f"Bestigor secondary profile {sec}")
        if (b.wounds, b.movement) != ("14", "5"):
            failures.append(f"Bestigor wounds/move {(b.wounds, b.movement)}")
        if b.system != SYSTEM:
            failures.append(f"system {b.system!r}, must be {SYSTEM!r}")
        if not (b.skills and b.skills.startswith("Command")):
            failures.append(f"Bestigor skills {b.skills!r}")
        if not (b.weapons and "Great Weapon" in b.weapons):
            failures.append(f"Bestigor weapons {b.weapons!r}")
        if b.slaughter_margin != "Challenging":
            failures.append(f"Bestigor slaughter margin {b.slaughter_margin!r}")
        mary = got[1]
        if (mary.ws, mary.fel, mary.wp) != ("48", "41", "56"):
            failures.append(f"Bloody Mary profile {(mary.ws, mary.fel, mary.wp)}")

    # ── fixture: ADVANCE SCHEME is rejected ─────────────────────────────────
    lines = FIXTURE_ADVANCE.splitlines()
    got = detect_wfrp(lines, _pages_for(lines), "WFRP: Old World Bestiary")
    if got:
        failures.append(f"advance scheme not rejected -> {[c.name for c in got]}")

    # ── fixture: HEADERLESS adventure NPC ───────────────────────────────────
    lines = FIXTURE_HEADERLESS.splitlines()
    got = detect_wfrp(lines, _pages_for(lines), "WFRP: The Thousand Thrones")
    if [c.name for c in got] != ["Horst Breuer"]:
        failures.append(f"headerless fixture names {[c.name for c in got]}, "
                        f"wanted ['Horst Breuer']")
    elif got:
        h = got[0]
        prof = (h.ws, h.bs, h.s, h.t, h.ag, h.int, h.wp, h.fel)
        if prof != ("36", "32", "45", "42", "41", "35", "43", "39"):
            failures.append(f"Horst Breuer profile {prof} (the '(4)' bonus must drop)")
        if (h.attacks, h.movement, h.wounds) != ("1", "4", "11"):
            failures.append(f"Horst Breuer combat {(h.attacks, h.movement, h.wounds)}")

    # ── garbage-name filter ─────────────────────────────────────────────────
    for junk in ["WS", "Main Profile", "Secondary Profile", "Skills",
                 "Slaughter Margin", "Chapter I: The Call of Chaos", "45%",
                 "The toughest and most experienced Beastmen are known as."]:
        if _clean_name(junk) is not None:
            failures.append(f"garbage name not rejected: {junk!r}")

    # ── live checks ─────────────────────────────────────────────────────────
    if base.is_dir() and any((base / s.path).exists() for s in SOURCES):
        corpus = Corpus(base, _fresh_sources())
        total = sum(len(s.creatures) for s in corpus.sources)
        if total < 150:
            failures.append(f"only {total} WFRP creatures indexed; expected > 150")
        for who, bk in [("Bestigor", "owb"), ("Chaos Warrior", "owb"),
                        ("Goblin", "owb"), ("Clanrat", "owb"),
                        ("Chimera", "toc")]:
            hit = corpus.find(who, book=bk)
            if not hit:
                failures.append(f"'{who}' not found in live {bk}")
                continue
            c = hit[0][1]
            if c.quick_fields() < 6:
                failures.append(f"'{who}' parsed only {c.quick_fields()} "
                                f"characteristics: {_profile_str(c)}")
        # The Thousand Thrones (headerless) must yield some NPCs.
        ttt = next((s for s in corpus.sources if s.key == "ttt"), None)
        if ttt and (base / ttt.path).exists() and len(ttt.creatures) < 10:
            failures.append(f"headerless detector yielded only "
                            f"{len(ttt.creatures) if ttt else 0} from The Thousand Thrones")
    else:
        print("  [SKIP] WFRP extractions not found — fixture checks only")

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
        found = sorted({(c.name, c.book, c.page or -1, _profile_str(c))
                        for _, c in corpus.all_creatures(args.book) if q in c.name.lower()})
        for name, bk, page, prof in found:
            loc = bk if page < 0 else f"{bk}, p.{page}"
            print(f"  {name}   [{prof}; {loc}]")
        print(f"{len(found)} match(es).")
        return 0 if found else 1

    if args.export:
        return export_packet(corpus, args.export, args.book, args.out)

    any_ok = any(s.creatures for s in corpus.sources)
    for src in corpus.sources:
        status = f"{len(src.creatures):4d} creatures" if src.creatures else "   0 creatures"
        print(f"  {src.book:34s} {status}  [{src.coverage.split(' — ')[0]}]")
    if not any_ok:
        print("\nNothing harvested — refusing to write empty reference files.")
        return 1
    total, parsed_well = write_index(corpus)
    print(f"\n{total} WFRP creatures across "
          f"{sum(1 for s in corpus.sources if s.creatures)} book(s); "
          f"{parsed_well} with 6+ characteristics parsed. (system: {SYSTEM})")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
