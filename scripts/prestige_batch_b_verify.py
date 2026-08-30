#!/usr/bin/env python3
"""Validate isolated Prestige Full-Text Batch B artifacts.

This is a staging validator, not a source verifier.  A passing result proves
that the mapping partitions the locked roster, that every recovered block has
bounded provenance and exact Markdown anchors, and that unresolved entries are
not represented as full text.  Rendered-page review remains authoritative.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


EXPECTED = [
    (38, "Noble Adventurer of Cormyr", 89),
    (39, "Moon Drover of Cormyr", 91),
    (40, "Royal Scout of Cormyr", 93),
    (41, "Companion of the Dead", 95),
    (42, "Shark Cultist", 96),
    (43, "Ranger Knight of Furyondy", 99),
    (44, "Boge of Nomog-Geaya", 102),
    (45, "Knight of the Chase", 105),
    (46, "Mask of Johydee", 110),
    (47, "Barber", 112),
    (48, "Corsair", 113),
    (49, "Holy Slayer", 115),
    (50, "Mamluk", 117),
    (51, "Dragonmark Heir", 121),
    (52, "Ranger of the Night's Watch", 127),
    (53, "Invisible Blade", 131),
    (54, "Occult Slayer", 132),
    (55, "Reaping Mauler", 134),
    (56, "Master Siege Engineer", 135),
    (57, "Duelist", 136),
    (58, "Bowman Charger", 139),
    (59, "Oppressor", 143),
    (60, "Poisoner", 144),
    (61, "Replacement Killer", 146),
    (62, "Poison Fist", 150),
    (63, "Ghost-Faced Killer", 152),
    (64, "Weightless Foot", 155),
    (65, "Nightsong Infiltrator", 157),
    (66, "Nightsong Enforcer", 159),
    (67, "Shen (Crane)", 162),
    (68, "Shen (Dragon)", 163),
    (69, "Shen (Mantis)", 164),
    (70, "Shen (Monkey)", 164),
    (71, "Shen (Panther)", 165),
    (72, "Shen (Snake)", 165),
    (73, "Shen (Tiger)", 166),
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("map", type=Path)
    parser.add_argument("markdown", type=Path)
    args = parser.parse_args()
    errors: list[str] = []
    mapping = json.loads(args.map.read_text(encoding="utf-8"))
    lines = args.markdown.read_text(encoding="utf-8").splitlines()
    expected = {ordinal: (name, page) for ordinal, name, page in EXPECTED}
    recovered = mapping.get("recovered", [])
    unresolved = mapping.get("unresolved", [])

    if mapping.get("owned_ordinals") != [38, 73]:
        fail(errors, "owned_ordinals must be exactly [38, 73]")
    if mapping.get("derived_source") != "reference/prestige_fulltext_batch_b.md":
        fail(errors, "wrong derived_source")

    all_rows = recovered + unresolved
    ordinals = [row.get("ordinal") for row in all_rows]
    if sorted(ordinals) != list(range(38, 74)):
        fail(errors, f"roster is not an exact 38..73 partition: {ordinals}")
    if len(ordinals) != len(set(ordinals)):
        fail(errors, "duplicate ordinals across recovered/unresolved")

    spans: list[tuple[int, int, str]] = []
    for status, rows in (("recovered", recovered), ("unresolved", unresolved)):
        for row in rows:
            ordinal = row.get("ordinal")
            if ordinal not in expected:
                fail(errors, f"{status}: unexpected ordinal {ordinal}")
                continue
            name, page = expected[ordinal]
            if row.get("name") != name or row.get("page") != page:
                fail(errors, f"{ordinal}: canonical name/page mismatch")
            if status == "unresolved":
                forbidden = {"start", "end", "full_description", "source_path"}
                leaked = sorted(forbidden.intersection(row))
                if leaked:
                    fail(errors, f"{ordinal} unresolved row has full-text fields: {leaked}")
                continue

            required = (
                "source_path", "description_pages", "full_text_start_page",
                "full_text_end_page", "start", "end", "start_anchor",
                "end_anchor", "source_flow", "checks",
            )
            missing = [field for field in required if field not in row]
            if missing:
                fail(errors, f"{ordinal} {name}: missing {missing}")
                continue
            pages = row["description_pages"]
            if (not pages or pages != list(range(min(pages), max(pages) + 1))
                    or row["full_text_start_page"] != pages[0]
                    or row["full_text_end_page"] != pages[-1]
                    or page not in pages):
                fail(errors, f"{ordinal} {name}: invalid page window {pages}")
            start, end = row["start"], row["end"]
            if not (isinstance(start, int) and isinstance(end, int)
                    and 0 <= start < end <= len(lines)):
                fail(errors, f"{ordinal} {name}: invalid line span {start}:{end}")
                continue
            block = lines[start:end]
            if block[0] != f"## {name}":
                fail(errors, f"{ordinal} {name}: span does not start at heading")
            text = "\n".join(block)
            if row["start_anchor"] not in "\n".join(block[:16]):
                fail(errors, f"{ordinal} {name}: start anchor not near block start")
            if row["end_anchor"] not in "\n".join(block[-24:]):
                fail(errors, f"{ordinal} {name}: end anchor not near block end")
            checks = row["checks"]
            for check in ("rendered_pages_verified", "caption_leakage_checked",
                          "neighbor_leakage_checked", "rules_tables_checked"):
                if checks.get(check) is not True:
                    fail(errors, f"{ordinal} {name}: check not true: {check}")
            if row.get("full_description") is not True or row.get("soft") is not False:
                fail(errors, f"{ordinal} {name}: acceptance flags are not strict")
            spans.append((start, end, name))

    spans.sort()
    for left, right in zip(spans, spans[1:]):
        if left[1] > right[0]:
            fail(errors, f"overlapping spans: {left[2]} / {right[2]}")
    headings = [line[3:] for line in lines if re.match(r"^## [^#]", line)]
    recovered_names = [row["name"] for row in recovered]
    if headings != recovered_names:
        fail(errors, f"Markdown headings != recovered order: {headings}")

    for error in errors:
        print(f"BATCH-B FAIL: {error}")
    print("batch-b validation: " + ("PASS" if not errors else f"{len(errors)} failure(s)"))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
