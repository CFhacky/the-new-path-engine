#!/usr/bin/env python3
"""Offline acceptance checks for the isolated prestige-class Batch A candidate."""

from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEXT_PATH = REPO_ROOT / "reference" / "prestige_fulltext_batch_a.md"
MAP_PATH = REPO_ROOT / "reference" / "prestige_fulltext_batch_a_map.json"
if not TEXT_PATH.exists():
    TEXT_PATH = Path(__file__).resolve().with_name("prestige_fulltext_batch_a.md")
    MAP_PATH = Path(__file__).resolve().with_name("prestige_fulltext_batch_a_map.json")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    text = TEXT_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    mapping = json.loads(MAP_PATH.read_text(encoding="utf-8"))

    require(mapping["generated_by"] == "manual vision transcription with page-image verification", "wrong verification authority")
    require(mapping["owned_ordinals"] == [1, 37], "wrong locked ordinal range")
    require(mapping["owned_names"] == ["Chimeric Champion of Garl Glittergold", "Council Mage of Cormyr"], "wrong locked name endpoints")
    require(mapping["derived_source"] == "reference/prestige_fulltext_batch_a.md", "wrong derived-source destination")

    recovered = mapping["recovered"]
    unresolved = mapping["unresolved"]
    require([row["ordinal"] for row in recovered] == [9, 10, 11, 12], "only verified ordinals 9-12 may be recovered")
    require([row["name"] for row in recovered] == ["Bloodsister", "Nightshade", "Deep Avenger", "Gloomblade"], "wrong verified roster/order")
    require([row["ordinal"] for row in unresolved] == list(range(1, 9)) + list(range(13, 38)), "unresolved ordinals must be exactly 1-8 and 13-37")
    require(len(recovered) + len(unresolved) == 37, "locked batch must contain exactly 37 classes")
    require({row["ordinal"] for row in recovered}.isdisjoint({row["ordinal"] for row in unresolved}), "recovered/unresolved overlap")

    expected_pages = {
        "Bloodsister": (29, 31, [29, 30, 31]),
        "Nightshade": (31, 32, [31, 32]),
        "Deep Avenger": (36, 37, [36, 37]),
        "Gloomblade": (37, 39, [37, 39]),
    }
    expected_anchors = {
        "Bloodsister": ("Bloodsister", "Twist the Knife (Ex)", "Nightshade"),
        "Nightshade": ("Nightshade", "Shadow Walk (Sp)", "For Your Character"),
        "Deep Avenger": ("Deep Avenger", "Resist Poison (Ex)", "Gloomblade"),
        "Gloomblade": ("Gloomblade", "Stonescreen Spell Description", "Gray Sage"),
    }
    expected_hit_dice = {"Bloodsister": "d10", "Nightshade": "d8", "Deep Avenger": "d8", "Gloomblade": "d6"}
    expected_abilities = {
        "Bloodsister": [
            "Weapon and Armor Proficiency", "Combat Reload (Ex)", "Poison Use (Ex)",
            "Two-Weapon Style (Ex)", "Tunnel Fighting (Ex)",
            "Improved Two-Weapon Style (Ex)", "Throw Sword (Ex)",
            "Sneak Attack (Ex)", "Mind of Steel (Ex)", "Twist the Knife (Ex)",
        ],
        "Nightshade": [
            "Weapon and Armor Proficiency", "Light Adjusted (Ex)", "Web Walker (Ex)",
            "Wall Runner (Su)", "Sneak Attack (Ex)", "Change Self (Sp)",
            "Poison Immunity (Ex)", "Poison Spittle (Ex)", "Web (Sp)", "Shadow Walk (Sp)",
        ],
        "Deep Avenger": [
            "Weapon and Armor Proficiency", "Brutal Strike (Ex)", "Drow Sign Language (Ex)",
            "Darkvision (Ex)", "See the Light (Sp)", "Rage (Ex)", "Resist Poison (Ex)",
        ],
        "Gloomblade": [
            "Weapon and Armor Proficiency", "Sneak Attack", "Drow Sign Language (Ex)",
            "Tremorsense (Ex)", "Stonescreen (Sp)", "Immunities (Ex)", "Ranged Disarm",
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
        require(f"Hit Die: {expected_hit_dice[name]}." in block, f"{name} missing or wrong hit die")
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
        require(len(row["source_flow"]) == end_page - start_page + 1, f"{name} needs one source-flow statement per rendered page")
        require(row["flow_overrides"], f"{name} missing explicit flow override")

    require(spans == [(6, 84), (84, 164), (164, 231), (231, 315)], "verified spans changed or are not contiguous")
    for left, right in zip(spans, spans[1:]):
        require(left[1] == right[0], "verified entries have a gap or overlap")
    require(lines[spans[0][1]] == "## Nightshade", "Bloodsister must stop exactly before Nightshade")
    require(lines[spans[1][1]] == "## Deep Avenger", "Nightshade must stop exactly before Deep Avenger")
    require(lines[spans[2][1]] == "## Gloomblade", "Deep Avenger must stop exactly before Gloomblade")
    require(spans[-1][1] == len(lines), "Gloomblade must end at derived-file EOF")

    prohibited = [
        "For Your Campaign", "For Your Character", "Wizards’ Workshop",
        "Dragon Magazine", "miniatures painted by", "illustration by", "Illus. by",
        "continued on", "www.", "Improved Counterspell [General]",
    ]
    body = "\n".join(lines[6:])
    for phrase in prohibited:
        require(phrase.casefold() not in body.casefold(), f"prohibited sidebar/furniture/caption leakage: {phrase}")

    require("If a bloodsister gets a sneak attack bonus from another source" in text, "Bloodsister p31 continuation missing")
    require("the *shadow walk* spell once per day" in text, "Nightshade terminal feature missing")
    require("At 8th level, a deep avenger gains a +4 bonus" in text, "Deep Avenger p37 continuation missing")
    require("| 10th | +10 | +7 | +3 | +7 | Rage 2/day, brutal strike +4 |" in text, "Deep Avenger good Will progression or terminal row is wrong")
    require("who are eager to fight on the front lines" in text, "Deep Avenger visual wording correction missing")
    require("The gloomblade cannot lose her own weapon during such an attempt." in text, "Gloomblade p38 continuation missing")
    require("The martial classes stand to gain more from the deep avenger prestige class" in text, "Gloomblade title-led prose is paraphrased or incomplete")
    require("### Stonescreen Spell Description" in text, "Gloomblade invoked Stonescreen sidebar missing")
    require("**Duration:** 1 hour/level (D)" in text, "Stonescreen dismissible duration missing")
    require("You can dismiss *stonescreen* as a free action instead of as a standard action." in text, "Stonescreen terminal rule missing")
    require(text.endswith("You can dismiss *stonescreen* as a free action instead of as a standard action.\n"), "derived text has wrong EOF")

    print("BATCH_A_OFFLINE_ACCEPTANCE recovered=4 unresolved=33 spans=4 errors=0")


if __name__ == "__main__":
    main()
