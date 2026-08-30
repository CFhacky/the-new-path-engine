#!/usr/bin/env python3
"""Structural acceptance checks for isolated prestige full-text Batch C.

This validator cannot replace rendered-page review.  It proves that the batch
map is an exact 74..109 partition, that every claimed recovery has bounded
source provenance and a unique Markdown span, and that common article/caption
leakage is absent.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


OWNED = range(74, 110)
PAGE_MIN = 167
PAGE_MAX = 263
EXPECTED_ENDPOINTS = ["Acolyte of the Fist", "Jester"]
EXPECTED = [
    (74, "Acolyte of the Fist", 168),
    (75, "Reaper's Child", 171),
    (76, "Monk of the Enabled Hand", 172),
    (77, "Primal Rager", 175),
    (78, "Fierce Grappler", 176),
    (79, "Brawler", 177),
    (80, "Cave Stalker", 179),
    (81, "Fiend Binder", 181),
    (82, "Prairie Runner", 182),
    (83, "Elder Druid", 186),
    (84, "The Mystic", 187),
    (85, "Aeromancer", 194),
    (86, "Eldritch Master", 197),
    (87, "Shaper of Form", 198),
    (88, "Force Missile Mage", 202),
    (89, "Earthshaker", 206),
    (90, "Icesinger", 207),
    (91, "Firestorm Berserker", 208),
    (92, "Purebreath Devotee", 210),
    (93, "Flame Steward", 212),
    (94, "Darkwater Knight", 215),
    (95, "Master Astrologer", 219),
    (96, "Rage Mage", 224),
    (97, "Psi-Hunter", 227),
    (98, "Truth Seeker", 230),
    (99, "Zerth Cenobite", 238),
    (100, "Arcanopath Monk", 240),
    (101, "Spirit Speaker", 244),
    (102, "Master of the Secret Sound", 246),
    (103, "Worldspeaker", 249),
    (104, "Mourner", 250),
    (105, "Memory Smith", 251),
    (106, "Battle Howler of Gruumsh", 252),
    (107, "Green Whisperer", 253),
    (108, "Charlatan", 255),
    (109, "Jester", 260),
]
EXPECTED_HIT_DIE = {
    **{ordinal: "d8" for ordinal in (74, 75, 76, 80, 81, 82, 89, 92, 93, 97, 98, 99, 100, 101, 105, 106)},
    **{ordinal: "d10" for ordinal in (77, 78, 79)},
    **{ordinal: "d4" for ordinal in (83, 85, 86, 88, 95)},
    **{ordinal: "d6" for ordinal in (84, 87, 90, 94, 96, 102, 103, 104, 107, 108, 109)},
    91: "d12",
}
PROHIBITED = (
    "illustration by",
    "art by",
    "photography by",
    "dragon magazine",
    "continued on page",
    "www.",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("map", type=Path)
    parser.add_argument("markdown", type=Path)
    args = parser.parse_args()

    errors: list[str] = []

    def fail(message: str) -> None:
        errors.append(message)

    mapping = json.loads(args.map.read_text(encoding="utf-8"))
    markdown = args.markdown.read_text(encoding="utf-8")
    lines = markdown.splitlines()
    recovered = mapping.get("recovered", [])
    unresolved = mapping.get("unresolved", [])

    if mapping.get("generated_by") != "manual vision transcription with page-image verification":
        fail("wrong verification authority")
    if mapping.get("owned_ordinals") != [74, 109]:
        fail("owned_ordinals must be exactly [74, 109]")
    if mapping.get("owned_names") != EXPECTED_ENDPOINTS:
        fail(f"owned_names must be exactly {EXPECTED_ENDPOINTS!r}")
    if mapping.get("derived_source") != "reference/prestige_fulltext_batch_c.md":
        fail("wrong derived_source")
    if [row.get("ordinal") for row in recovered] != [74, 75]:
        fail("bounded candidate may recover only ordinals 74 and 75")
    if [row.get("ordinal") for row in unresolved] != list(range(76, 110)):
        fail("bounded candidate must leave ordinals 76..109 unresolved in order")

    rows = recovered + unresolved
    expected = {ordinal: (name, page) for ordinal, name, page in EXPECTED}
    ordinals = [row.get("ordinal") for row in rows]
    if sorted(ordinals) != list(OWNED):
        fail(f"recovered/unresolved is not an exact 74..109 partition: {ordinals}")
    if len(ordinals) != len(set(ordinals)):
        fail("duplicate ordinal across recovered/unresolved")
    names = [row.get("name") for row in rows]
    if any(not isinstance(name, str) or not name.strip() for name in names):
        fail("every roster row must have a nonempty name")
    if len(names) != len(set(names)):
        fail("duplicate class name across recovered/unresolved")
    for row in rows:
        ordinal = row.get("ordinal")
        if ordinal not in expected:
            continue
        expected_name, expected_page = expected[ordinal]
        if row.get("name") != expected_name or row.get("page") != expected_page:
            fail(f"{ordinal}: canonical name/page mismatch")

    for row in unresolved:
        leaked = sorted({
            "source_path", "description_pages", "full_text_start_page",
            "full_text_end_page", "start", "end", "start_anchor",
            "end_anchor", "stop_before_anchor", "full_description", "soft",
            "checks",
        }.intersection(row))
        if leaked:
            fail(f"unresolved {row.get('ordinal')} {row.get('name')}: full-text fields leak: {leaked}")

    spans: list[tuple[int, int, int, str]] = []
    for row in recovered:
        ordinal = row.get("ordinal")
        name = row.get("name")
        required = (
            "source_path", "description_pages", "full_text_start_page",
            "full_text_end_page", "start", "end", "start_anchor",
            "end_anchor", "stop_before_anchor", "source_flow", "checks",
            "full_description", "soft",
        )
        missing = [field for field in required if field not in row]
        if missing:
            fail(f"{ordinal} {name}: missing fields: {missing}")
            continue

        if row["source_path"] != mapping.get("source_pdf"):
            fail(f"{ordinal} {name}: source_path differs from map source_pdf")
        pages = row["description_pages"]
        if (not isinstance(pages, list) or not pages
                or any(not isinstance(page, int) for page in pages)
                or pages != sorted(set(pages))
                or pages != list(range(pages[0], pages[-1] + 1))
                or pages[0] < PAGE_MIN or pages[-1] > PAGE_MAX):
            fail(f"{ordinal} {name}: invalid rendered-page flow {pages!r}")
        else:
            if row["full_text_start_page"] != pages[0] or row["full_text_end_page"] != pages[-1]:
                fail(f"{ordinal} {name}: full-text page endpoints differ from description_pages")
            if row.get("page") not in pages:
                fail(f"{ordinal} {name}: canonical index page is outside description_pages")
            if len(row["source_flow"]) != len(pages):
                fail(f"{ordinal} {name}: source_flow needs one statement per rendered page")

        if row["full_description"] is not True or row["soft"] is not False:
            fail(f"{ordinal} {name}: acceptance flags are not strict")
        checks = row["checks"]
        for check in (
            "rendered_pages_verified", "caption_leakage_checked",
            "neighbor_leakage_checked", "rules_tables_checked",
        ):
            if checks.get(check) is not True:
                fail(f"{ordinal} {name}: check not true: {check}")

        start, end = row["start"], row["end"]
        if not (isinstance(start, int) and isinstance(end, int)
                and 0 <= start < end <= len(lines)):
            fail(f"{ordinal} {name}: invalid line span {start!r}:{end!r}")
            continue
        block_lines = lines[start:end]
        block = "\n".join(block_lines)
        if block_lines[0] != f"## {name}":
            fail(f"{ordinal} {name}: line span does not start at its heading")
        if len(re.findall(r"^## [^#]", block, flags=re.MULTILINE)) != 1:
            fail(f"{ordinal} {name}: line span contains another class heading")
        if row["start_anchor"] not in "\n".join(block_lines[:20]):
            fail(f"{ordinal} {name}: start_anchor is not near block start")
        if row["end_anchor"] not in "\n".join(block_lines[-30:]):
            fail(f"{ordinal} {name}: end_anchor is not near block end")
        if row["stop_before_anchor"].casefold() in block.casefold():
            fail(f"{ordinal} {name}: stop-before anchor leaked into block")
        expected_hit_die = EXPECTED_HIT_DIE[ordinal]
        if f"Hit Die: {expected_hit_die}" not in block:
            fail(f"{ordinal} {name}: expected Hit Die {expected_hit_die} missing")
        if not re.search(r"^\| Level \|", block, flags=re.MULTILINE):
            fail(f"{ordinal} {name}: advancement table header missing")
        for phrase in PROHIBITED:
            if phrase in block.casefold():
                fail(f"{ordinal} {name}: prohibited article/caption furniture: {phrase}")
        spans.append((start, end, ordinal, name))

    spans.sort()
    for left, right in zip(spans, spans[1:]):
        if left[1] > right[0]:
            fail(f"overlapping spans: {left[3]} / {right[3]}")
    headings = [line[3:] for line in lines if re.match(r"^## [^#]", line)]
    recovered_names = [row.get("name") for row in recovered]
    if headings != recovered_names:
        fail(f"Markdown class headings do not equal recovered order: {headings!r}")

    if [(start, end) for start, end, _, _ in spans] != [(6, 102), (102, 166)]:
        fail(f"verified line spans changed: {[(start, end) for start, end, _, _ in spans]!r}")
    if spans and spans[-1][1] != len(lines):
        fail("final recovered entry must end at derived-file EOF")

    expected_pages = {
        74: (167, 168, [167, 168]),
        75: (170, 171, [170, 171]),
    }
    expected_abilities = {
        74: (
            "Weapon and Armor Proficiency", "Unarmed Damage", "Fast Movement (Ex)",
            "Fist of Speed (Ex)", "Leap of the Clouds (Ex)", "Fists of Iron (Su)",
            "Ki Strike (Su)", "Fist of Destruction (Ex)", "Fist of Mercy (Su)",
            "Evasion/Improved Evasion (Ex)", "Improved Critical (Ex)",
            "Fist of Fury (Su)", "Fist of Power (Su)", "Fist of Energy (Su)",
        ),
        75: (
            "Weapon and Armor Proficiency", "Monk Abilities (Ex)",
            "Whisper of Nerull (Su)", "Reaper’s Reinforcement (Su)",
            "Scythe Strike (Su)", "Oathgiver (Sp)", "Reaper of Flesh (Su)",
        ),
    }
    for row in recovered:
        ordinal = row["ordinal"]
        start, end = row["start"], row["end"]
        block = "\n".join(lines[start:end])
        start_page, end_page, pages = expected_pages[ordinal]
        if (row["full_text_start_page"], row["full_text_end_page"], row["description_pages"]) != (start_page, end_page, pages):
            fail(f"{ordinal}: exact verified page flow changed")
        for ability in expected_abilities[ordinal]:
            if f"**{ability}:**" not in block:
                fail(f"{ordinal}: missing verified ability {ability}")
        expected_rows = 10 if ordinal == 74 else 5
        if len(re.findall(r"^\| (?:[1-9]|10) \|", block, flags=re.MULTILINE)) != expected_rows:
            fail(f"{ordinal}: advancement table must have exactly {expected_rows} rows")

    by_ordinal = {row.get("ordinal"): row for row in recovered}
    if 74 in by_ordinal:
        start, end = by_ordinal[74]["start"], by_ordinal[74]["end"]
        acolyte = "\n".join(lines[start:end])
        if "fists of iron" not in acolyte.casefold():
            fail("Acolyte of the Fist must retain the invoked FISTS OF IRON rules box")
        if by_ordinal[74]["full_text_start_page"] != 167:
            fail("Acolyte of the Fist must begin on true rendered page 167")
        if "**Prerequisites:** Base attack bonus +2, Improved Unarmed Strike." not in acolyte:
            fail("Acolyte FISTS OF IRON prerequisite line missing")
        if "number of times per day equal to 3 + your Wisdom modifier" not in acolyte:
            fail("Acolyte FISTS OF IRON terminal benefit missing")

    body = "\n".join(lines[6:]).casefold()
    for phrase in (
        "for your campaign", "order descriptions", "oath & order",
        "monk of the enabled hand", "illustrated by", "by monte cook",
    ):
        if phrase in body:
            fail(f"excluded article/sidebar/neighbor text leaked: {phrase}")
    for required in (
        "fall unconscious for 1d10 rounds",
        "become *confused* (as per the spell) for 1d10 rounds",
        "immune to his own fist of energy",
        "automatically confirmed a x4 critical",
        "the target is knocked prone by the furious kick",
        "shred (-9 hit points)",
    ):
        if required.casefold() not in body:
            fail(f"verified terminal/corrected rule missing: {required}")

    for error in errors:
        print(f"BATCH-C FAIL: {error}")
    print(
        "batch-c validation: "
        + (f"PASS recovered={len(recovered)} unresolved={len(unresolved)} spans={len(spans)}"
           if not errors else f"{len(errors)} failure(s)")
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
