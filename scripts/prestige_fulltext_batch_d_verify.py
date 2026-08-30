#!/usr/bin/env python3
"""Offline acceptance checks for the isolated prestige-class Batch D candidate."""

from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEXT_PATH = REPO_ROOT / "reference" / "prestige_fulltext_batch_d.md"
MAP_PATH = REPO_ROOT / "reference" / "prestige_fulltext_batch_d_map.json"
if not TEXT_PATH.exists():  # Standalone checkpoint layout used before repository placement.
    TEXT_PATH = Path(__file__).resolve().with_name("prestige_fulltext_batch_d.md")
    MAP_PATH = Path(__file__).resolve().with_name("prestige_fulltext_batch_d_map.json")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    text = TEXT_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    mapping = json.loads(MAP_PATH.read_text(encoding="utf-8"))

    require(mapping["generated_by"] == "manual vision transcription with page-image verification", "wrong verification authority")
    require(mapping["owned_ordinals"] == [110, 145], "wrong locked ordinal range")
    require(mapping["owned_names"] == ["Aerial Avenger", "Dragon Warrior"], "wrong locked name endpoints")
    require(mapping["derived_source"] == "reference/prestige_fulltext_batch_d.md", "wrong derived-source destination")

    recovered = mapping["recovered"]
    unresolved = mapping["unresolved"]
    require([row["ordinal"] for row in recovered] == [144, 145], "only verified ordinals 144-145 may be recovered")
    require([row["name"] for row in recovered] == ["Kabuki Warrior", "Dragon Warrior"], "wrong verified roster/order")
    require([row["ordinal"] for row in unresolved] == list(range(110, 144)), "unresolved ordinals must be exactly 110-143")
    require(len(recovered) + len(unresolved) == 36, "locked batch must contain exactly 36 classes")
    require({row["ordinal"] for row in recovered}.isdisjoint({row["ordinal"] for row in unresolved}), "recovered/unresolved overlap")

    expected_pages = {
        "Kabuki Warrior": (353, 354, [353, 354]),
        "Dragon Warrior": (354, 355, [354, 355]),
    }
    expected_anchors = {
        "Kabuki Warrior": ("Kabuki Warrior", "Master Clowning (Ex)", "Dragon Warrior"),
        "Dragon Warrior": ("Dragon Warrior", "Dragon’s Release (Ex)", "For Your Character"),
    }
    expected_abilities = {
        "Kabuki Warrior": [
            "Weapon and Armor Proficiency", "Canny Defense (Ex)", "Clowning (Ex)",
            "Sneak Attack", "Taunt (Su)", "Stardust (Sp)",
            "Expert Clowning (Ex)", "Master Clowning (Ex)",
        ],
        "Dragon Warrior": [
            "Weapons and Armor", "Body of Soul (Su)", "Chi Shield (Su)",
            "Dragon’s Fire (Su)", "Dragon’s Fury (Ex)", "Dragon’s Grip (Ex)",
            "Dragon’s Release (Ex)",
        ],
    }

    spans: list[tuple[int, int]] = []
    for row in recovered:
        name = row["name"]
        start, end = row["start"], row["end"]
        require(0 <= start < end <= len(lines), f"invalid line span for {name}")
        spans.append((start, end))
        block = "\n".join(lines[start:end])
        require(block.startswith(f"## {name}\n"), f"{name} span does not start at its heading")
        require(block.count("\n## ") == 0, f"{name} span leaks a neighboring class")
        require("### Class Features" in block, f"{name} missing class features")
        require("### Class Requirements" in block, f"{name} missing requirements")
        require("### Class Skills" in block, f"{name} missing skills")
        require("Hit Die: d10." in block, f"{name} missing hit die")
        require(f"### {name} Advancement" in block, f"{name} missing advancement table")
        require(len(re.findall(r"^\| (?:[1-9]|10)(?:st|nd|rd|th) \|", block, flags=re.MULTILINE)) == 10, f"{name} advancement table must have 10 levels")
        for ability in expected_abilities[name]:
            require(f"**{ability}:**" in block, f"{name} missing ability: {ability}")

        start_page, end_page, description_pages = expected_pages[name]
        require(row["full_text_start_page"] == start_page, f"wrong start page for {name}")
        require(row["full_text_end_page"] == end_page, f"wrong end page for {name}")
        require(row["description_pages"] == description_pages, f"wrong description pages for {name}")
        require(row["source_path"] == mapping["source_pdf"], f"wrong source path for {name}")
        start_anchor, end_anchor, stop_before_anchor = expected_anchors[name]
        require((row["start_anchor"], row["end_anchor"], row["stop_before_anchor"]) == (start_anchor, end_anchor, stop_before_anchor), f"wrong source anchors for {name}")
        require(start_anchor in block and end_anchor in block, f"{name} anchors absent from derived block")
        require(stop_before_anchor not in block, f"{name} leaks its stop-before anchor")
        require(row["full_description"] is True and row["soft"] is False, f"{name} not marked as hard full text")
        require(len(row["source_flow"]) == 2, f"{name} needs one source-flow statement per rendered page")

    require(spans == [(6, 81), (81, 154)], "verified spans changed or are not contiguous")
    require(spans[0][1] == spans[1][0], "verified entries have a gap or overlap")
    require(lines[spans[0][1]] == "## Dragon Warrior", "Kabuki Warrior must stop exactly before Dragon Warrior")
    require(spans[1][1] == len(lines), "Dragon Warrior must end at derived-file EOF")

    prohibited = [
        "For Your Campaign", "For Your Character", "Dragon Magazine", "continued on",
        "illustration by", "art by", "photography by", "www.",
    ]
    body = "\n".join(lines[6:])
    for phrase in prohibited:
        require(phrase.casefold() not in body.casefold(), f"prohibited sidebar/furniture/caption leakage: {phrase}")

    require("Creatures who cannot see the lights are not distracted by them." in text, "Kabuki Stardust terminal rule missing")
    require("At 5th level, the resilience of the warrior increases" in text, "Dragon Warrior Chi Shield 5th-level continuation missing")
    require("flaming burst magic weapon enhancement" in text, "Dragon Warrior terminal Dragon’s Release rule missing")
    require(text.endswith("| 10th | +10 | +7 | +3 | +7 | Dragon’s release (dragon’s fury 4/day) |\n"), "derived text has wrong EOF")

    print("BATCH_D_OFFLINE_ACCEPTANCE recovered=2 unresolved=34 spans=2 errors=0")


if __name__ == "__main__":
    main()
