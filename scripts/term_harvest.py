#!/usr/bin/env python3
"""term_harvest.py — harvest affixes and terms from the sourcebook corpus.

THE PROCESS (Chad, 2026-08-07): "there should be a file with all the affixes
and terms and what not from gurps and dnd... may I suggest creating a process
to do that from my many many gurps and dnd and warhammer sourcebooks."

This script IS that process. It walks the text-layer extractions the OCR
pipeline already produced under I:\\Sourcebooks\\_text, harvests the named
modifier vocabulary of each configured section, and writes:

    reference/terms_and_affixes.md    — the human reference, grouped by system
    reference/terms_and_affixes.json  — the same data, machine-readable, for
                                        the Everguild mod loader to feed on

Every entry carries provenance: the book, the section, and the PDF page where
the extraction recorded one. Where a configured section's anchors cannot be
found, the harvest prints NO COVERAGE and says which book and which anchor —
it never improvises (udrp_delve.py's convention).

GOVERNING SOURCES
  - DMG v3.5 "Magic Weapon Special Ability Descriptions" (pp. 223-226) and
    "Magic Armor and Shield Special Ability Descriptions" (pp. 218-219), via
    the text extraction at I:\\Sourcebooks\\_text\\D&D 3.5e\\Core\\.
  - GURPS 4e Basic Set: Characters, ENHANCEMENTS (B102) and LIMITATIONS
    (B110), via I:\\Sourcebooks\\_text\\GURPS\\GURPS 4e\\.
  - CONDITIONS ARE DELIBERATELY NOT HARVESTED HERE: conditions.py (DMG
    pp. 300-301) and gurps_conditions.py (B419-429) are already the
    authoritative rosters. One source of truth per layer; this file points
    at them rather than copying them.

Extend by adding a Section to SECTIONS — Warhammer wargear, PHB glossary,
Magic Item Compendium and the GURPS 3e magic item books are the intended
next targets; their extractions already exist in the corpus.

Run:      python term_harvest.py            (writes both reference files)
          python term_harvest.py --selftest (parsers against embedded fixtures)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

CORPUS = Path(r"I:\Sourcebooks\_text")
REPO = Path(__file__).resolve().parent.parent
OUT_MD = REPO / "reference" / "terms_and_affixes.md"
OUT_JSON = REPO / "reference" / "terms_and_affixes.json"

PAGE_MARKER = re.compile(r"^## \[PDF page (\d+)\]")


@dataclass
class Entry:
    name: str
    gloss: str
    cost: str | None = None  # GURPS: the ±% column; D&D: bonus equivalent when parsed
    page: int | None = None  # PDF page from the extraction's own markers
    source_line: int = 0


@dataclass
class Section:
    key: str
    title: str
    system: str  # "dnd35" | "gurps4e" | "warhammer" | ...
    book: Path  # relative to CORPUS
    citation: str
    start_anchor: str  # regex; harvest begins AFTER the first match
    end_anchor: str  # regex; harvest stops AT the first later match
    parser: str  # "colon_defs" | "gurps_modifiers"
    entries: list[Entry] = field(default_factory=list)
    coverage: str = "pending"


SECTIONS: list[Section] = [
    Section(
        key="dnd_weapon_abilities",
        title="D&D 3.5 magic weapon special abilities (the weapon affixes)",
        system="dnd35",
        book=Path("D&D 3.5e/Core/Dungeon Masters Guide v3.5.md"),
        citation="DMG v3.5, Magic Weapon Special Ability Descriptions (pp. 223-226)",
        start_anchor=r"Magic Weapon Special Ability Descriptions",
        end_anchor=r"^Specific Weapons",
        parser="colon_defs",
    ),
    Section(
        key="dnd_armor_abilities",
        title="D&D 3.5 magic armor and shield special abilities (the armor affixes)",
        system="dnd35",
        book=Path("D&D 3.5e/Core/Dungeon Masters Guide v3.5.md"),
        citation="DMG v3.5, Magic Armor and Shield Special Ability Descriptions (pp. 218-219)",
        start_anchor=r"Magic Armor.{0,3}and Shield Special Ability Descriptions",
        end_anchor=r"Specific Armors|TasLe 7.{0,3}7|TABLE 7.{0,3}7",
        parser="colon_defs",
    ),
    Section(
        key="gurps_enhancements",
        title="GURPS 4e enhancements (the +% affixes an ability can carry)",
        system="gurps4e",
        book=Path("GURPS/GURPS 4e/GURPS 4e - Basic Set - Characters.md"),
        citation="GURPS Basic Set: Characters, ENHANCEMENTS (B102-B109)",
        start_anchor=r"^ENHANCEMENTS$",
        end_anchor=r"^LIMITATIONS$",
        parser="gurps_modifiers",
    ),
    Section(
        key="gurps_limitations",
        title="GURPS 4e limitations (the -% affixes an ability can carry)",
        system="gurps4e",
        book=Path("GURPS/GURPS 4e/GURPS 4e - Basic Set - Characters.md"),
        citation="GURPS Basic Set: Characters, LIMITATIONS (B110-B117)",
        start_anchor=r"^LIMITATIONS$",
        end_anchor=r"^DISADVANTAGES$|^SKILLS$",
        parser="gurps_modifiers",
    ),
]

# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------

# "Flaming: Upon command, a flaming weapon is sheathed in fire..." — a name of
# at most four words, starting a line, followed by a colon and prose. The OCR
# drops punctuation strangely, so the name charset is generous but bounded.
COLON_DEF = re.compile(r"^([A-Z][A-Za-z'’\- ]{1,32}?)\s*:\s+(\S.*)$")

# Words that mean a COLON_DEF match is layout, not an affix.
COLON_DEF_REJECT = re.compile(
    r"table|random generation|special qualities|caster level|price|aura|note|"
    r"weight|weapons|armor and shields|activation|charges|slot|synerg",
    re.IGNORECASE,
)

# GURPS: a short title line (OCR sometimes appends a stray glyph read as " 6")
# whose next non-empty line is a cost — "+50%/level", "-40%", "Variable"...
GURPS_TITLE = re.compile(r"^([A-Z][A-Za-z'’,\-/ ]{2,42}?)(?:\s+6)?$")
GURPS_COST = re.compile(
    r"^(?:[+\-\u2212][0-9]{1,3}%(?:/level)?(?:\s+or\s+more)?|Variable|Special)$"
)


def sentence_of(lines: list[str], limit: int = 260) -> str:
    """First sentence-ish of an OCR paragraph, joined and trimmed."""
    text = " ".join(part.strip() for part in lines if part.strip())
    text = re.sub(r"\s+", " ", text)
    match = re.search(r"[.!?](?:\s|$)", text)
    if match and match.start() >= 40:
        text = text[: match.start() + 1]
    return text[:limit].strip()


def parse_colon_defs(lines: list[str], base_line: int) -> list[Entry]:
    entries: list[Entry] = []
    current: tuple[str, int] | None = None
    buffer: list[str] = []
    page: int | None = None
    page_of_current: int | None = None

    def close() -> None:
        nonlocal current, buffer
        if current is not None:
            name, at = current
            entries.append(
                Entry(name=name, gloss=sentence_of(buffer), page=page_of_current, source_line=at)
            )
        current, buffer = None, []

    for offset, raw in enumerate(lines):
        line = raw.rstrip()
        marker = PAGE_MARKER.match(line)
        if marker:
            page = int(marker.group(1))
            continue
        match = COLON_DEF.match(line)
        if match and not COLON_DEF_REJECT.search(match.group(1)):
            close()
            current = (match.group(1).strip(), base_line + offset + 1)
            page_of_current = page
            buffer = [match.group(2)]
        elif current is not None:
            if line.strip() == "" and len(buffer) > 3:
                close()
            else:
                buffer.append(line)
    close()
    return entries


def parse_gurps_modifiers(lines: list[str], base_line: int) -> list[Entry]:
    entries: list[Entry] = []
    page: int | None = None
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        marker = PAGE_MARKER.match(line)
        if marker:
            page = int(marker.group(1))
            i += 1
            continue
        title = GURPS_TITLE.match(line.strip())
        if title:
            # find the next non-empty line; it must be a cost
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and GURPS_COST.match(lines[j].strip()):
                # gloss: prose until the next blank-then-title or next cost pair
                gloss_lines: list[str] = []
                k = j + 1
                while k < len(lines):
                    nxt = lines[k].strip()
                    if PAGE_MARKER.match(lines[k]):
                        k += 1
                        continue
                    peek_title = GURPS_TITLE.match(nxt)
                    if peek_title:
                        j2 = k + 1
                        while j2 < len(lines) and not lines[j2].strip():
                            j2 += 1
                        if j2 < len(lines) and GURPS_COST.match(lines[j2].strip()):
                            break
                    gloss_lines.append(nxt)
                    if len(gloss_lines) > 14:
                        break
                    k += 1
                entries.append(
                    Entry(
                        name=title.group(1).strip(),
                        gloss=sentence_of(gloss_lines),
                        cost=lines[j].strip().replace("\u2212", "-"),
                        page=page,
                        source_line=base_line + i + 1,
                    )
                )
                i = k
                continue
        i += 1
    return entries


PARSERS = {"colon_defs": parse_colon_defs, "gurps_modifiers": parse_gurps_modifiers}

# ---------------------------------------------------------------------------
# Harvest
# ---------------------------------------------------------------------------


def harvest(section: Section) -> Section:
    path = CORPUS / section.book
    if not path.exists():
        section.coverage = f"NO COVERAGE — extraction missing: {path}"
        return section
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()

    start_re = re.compile(section.start_anchor)
    end_re = re.compile(section.end_anchor)
    start = next((i for i, l in enumerate(lines) if start_re.search(l)), None)
    if start is None:
        section.coverage = f"NO COVERAGE — start anchor not found: /{section.start_anchor}/"
        return section
    end = next((i for i in range(start + 1, len(lines)) if end_re.search(lines[i])), None)
    if end is None:
        section.coverage = f"NO COVERAGE — end anchor not found: /{section.end_anchor}/"
        return section

    section.entries = PARSERS[section.parser](lines[start + 1 : end], start + 1)
    section.coverage = f"ok — lines {start + 1}..{end} of {path.name}"
    return section


def write_outputs(sections: list[Section]) -> None:
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)

    md: list[str] = [
        "# TERMS AND AFFIXES — The New Path",
        "",
        "**Generated by `scripts/term_harvest.py`. Do not hand-edit — rerun the",
        "harvest instead; hand corrections belong in the script's parsers or in",
        "an erratum note beside the entry's source.** Every entry names its book;",
        "GURPS entries carry the PDF page the extraction recorded.",
        "",
        "Conditions are deliberately NOT duplicated here: `scripts/conditions.py`",
        "(DMG pp. 300-301) and `scripts/gurps_conditions.py` (B419-429) are the",
        "authoritative rosters, per AUTHORITY.md. This file holds the modifier",
        "vocabulary — what D&D calls weapon and armor special abilities, and",
        "what GURPS calls enhancements and limitations.",
        "",
    ]
    for section in sections:
        md.append(f"## {section.title}")
        md.append("")
        md.append(f"*Source: {section.citation}.*  ")
        md.append(f"*Harvest: {section.coverage}. {len(section.entries)} entries.*")
        md.append("")
        if section.entries:
            has_cost = any(e.cost for e in section.entries)
            md.append("| Name | " + ("Cost | " if has_cost else "") + "What it does | Page |")
            md.append("|---|" + ("---|" if has_cost else "") + "---|---|")
            for e in section.entries:
                gloss = e.gloss.replace("|", "/")
                page = str(e.page) if e.page else "—"
                if has_cost:
                    md.append(f"| {e.name} | {e.cost or '—'} | {gloss} | {page} |")
                else:
                    md.append(f"| {e.name} | {gloss} | {page} |")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps(
            {
                "generated_by": "scripts/term_harvest.py",
                "sections": [
                    {
                        "key": s.key,
                        "title": s.title,
                        "system": s.system,
                        "book": str(s.book),
                        "citation": s.citation,
                        "coverage": s.coverage,
                        "entries": [asdict(e) for e in s.entries],
                    }
                    for s in sections
                ],
            },
            indent=1,
        ),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Selftest — parsers against embedded fixtures shaped like the real OCR
# ---------------------------------------------------------------------------

DMG_FIXTURE = """Anarchic: An anarchic weapon is chaotically aligned and in-
fused with the power of chaos, It makes the weapon chaos-aligned
and thus bypasses the corresponding damage reduction.

Flaming: Upon command, a flaming weapon_is. sheathed in
fire. The fire does not harm the wielder.

Random Generation: To generate magic weapons randomly,
first roll on Table 7-9.

Keen: This ability doubles the threatrange of a weapon. For
example a longsword.
"""

GURPS_FIXTURE = """## [PDF page 104]
Accurate 6
+5%/level
Your attack is unusually accurate.
Each +1 to Accuracy is a +5%
enhancement.
Affects Insubstantial
+20%
Your ability affects insubstantial
targets in addition to normal things.
Radius
Modifier
2 yards
+50%
"""


def selftest() -> int:
    failures: list[str] = []

    dmg = parse_colon_defs(DMG_FIXTURE.splitlines(), 0)
    names = [e.name for e in dmg]
    if names != ["Anarchic", "Flaming", "Keen"]:
        failures.append(f"colon_defs harvested {names}, wanted Anarchic/Flaming/Keen (and Random Generation rejected)")
    if dmg and "chaotically aligned" not in dmg[0].gloss:
        failures.append(f"colon_defs gloss wrong: {dmg[0].gloss!r}")

    gurps = parse_gurps_modifiers(GURPS_FIXTURE.splitlines(), 0)
    got = [(e.name, e.cost, e.page) for e in gurps]
    want = [("Accurate", "+5%/level", 104), ("Affects Insubstantial", "+20%", 104)]
    if got != want:
        failures.append(f"gurps_modifiers harvested {got}, wanted {want} (Radius table must not match)")

    for failure in failures:
        print(f"SELFTEST FAIL: {failure}")
    print("selftest: " + ("PASS" if not failures else f"{len(failures)} failure(s)"))
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()

    sections = [harvest(s) for s in SECTIONS]
    for s in sections:
        status = f"{len(s.entries):4d} entries" if s.entries else "   0 entries"
        print(f"{s.key:24s} {status}  [{s.coverage}]")
    if not any(s.entries for s in sections):
        print("Nothing harvested at all — refusing to write empty reference files.")
        return 1
    write_outputs(sections)
    print(f"\nwrote {OUT_MD}")
    print(f"wrote {OUT_JSON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
