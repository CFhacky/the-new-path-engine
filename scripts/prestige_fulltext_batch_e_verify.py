#!/usr/bin/env python3
"""Offline acceptance checks for the isolated prestige-class Batch E payload.

This verifier checks the normalized source and exact uncapped line slices.
Rendered-page review remains the authority for transcription correctness.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
TEXT_PATH = REPO_ROOT / "reference" / "prestige_fulltext_batch_e.md"
MAP_PATH = REPO_ROOT / "reference" / "prestige_fulltext_batch_e_map.json"
if not TEXT_PATH.exists():
    TEXT_PATH = HERE / "prestige_fulltext_batch_e.md"
    MAP_PATH = HERE / "prestige_fulltext_batch_e_map.json"


EXPECTED = {
    13: {
        "name": "Gray Sage", "page": 38, "span": (6, 76),
        "compiled": [38, 39], "issue": "Dragon Magazine #298",
        "issue_pages": [58, 59, 60],
        "ocr_path": r"I:\Sourcebooks\_text\Dragon Magazine\Dragon Magazine #298.md",
        "ocr_lines": ["6186-6208", "6213-6380", "6541-6570"],
        "hit_die": "d4", "rows": 10,
        "abilities": (
            "Weapon and Armor Proficiency", "Spells Per Day",
            "Improved Counterspell", "Handreading (Ex)", "Blindsight (Ex)",
            "Greater Counterspell (Ex)", "Improved Spell Penetration (Ex)",
            "Improved Silent Spell (Su)", "Mordenkainen’s Disjunction (Sp)",
        ),
        "required": (
            "Able to cast any 4th-level Conjuration spell.",
            "| 8th | +4 | +2 | +2 | +6 | Increased spell penetration +6 |",
        ),
        "anomalies": 1,
        "anomaly_note_terms": ("Increased spell penetration +6", "Improved Spell Penetration"),
    },
    14: {
        "name": "Shining Blade of Heironeous", "page": 41, "span": (76, 149),
        "compiled": [40, 41, 42], "issue": "Dragon Magazine #283",
        "issue_pages": [40, 41, 42],
        "ocr_path": r"I:\Sourcebooks\_text\Dragon Magazine\Dragon Magazine #283.md",
        "ocr_lines": ["2828-3104"], "hit_die": "d10", "rows": 10,
        "abilities": (
            "Weapon and Armor Proficiency", "Detect Evil", "Smite Evil",
            "Spells per Day", "Shock Blade", "Holy Blade", "Radiant Blade",
            "Celestial Transformation", "Multiclass Note",
        ),
        "required": (
            "The shining blades of Heironeous is an order",
            "Ability to cast divine spells.",
            "| 10th | +7 | +7 | +3 | +7 | Celestial transformation, smite evil 4/day | +1 level of existing class |",
        ),
        "anomalies": 1,
        "anomaly_note_terms": ("The shining blades of Heironeous is an order",),
    },
    44: {
        "name": "Boge of Nomog-Geaya", "page": 102, "span": (149, 209),
        "compiled": [102, 103], "issue": "Dragon Magazine #315",
        "issue_pages": [91, 92],
        "ocr_path": r"I:\Sourcebooks\_text\Dragon Magazine\Dragon Magazine #315.md",
        "ocr_lines": ["13800-13843", "13885-13931", "13957-14019", "14040-14094"],
        "hit_die": "d8", "rows": 10,
        "abilities": (
            "Weapon and Armor Proficiency", "Spells per Day/Spells Known",
            "Master of Steel (Ex)", "Bane (Su)", "Master of Fire (Su)",
            "Mantle of Authority (Su)",
        ),
        "required": (
            "Ability to cast 3rd-level divine spells.",
            "he can imbue both his longsword and his handaxe he wields",
            "This duration need not be consecutive",
            "| 10th | +7 | +7 | +3 | +7 | Mantle of authority | +1 level of existing spellcasting class |",
        ),
        "anomalies": 1,
        "anomaly_note_terms": ("both his longsword and his handaxe he wields",),
    },
    78: {
        "name": "Fierce Grappler", "page": 176, "span": (209, 270),
        "compiled": [176], "issue": "Dragon Magazine #295",
        "issue_pages": [72],
        "ocr_path": r"I:\Sourcebooks\_text\Dragon Magazine\Dragon Magazine #295.md",
        "ocr_lines": ["9184-9225", "9239-9342"],
        "hit_die": "d10", "rows": 5,
        "abilities": (
            "Weapon and Armor Proficiency", "Precision Strike (Ex)",
            "Power Strike (Ex)", "Great Grappler (Ex)", "Deadly Pin (Ex)",
            "Choke-Out (Ex)",
        ),
        "required": (
            "Escape Artist: 5 ranks.",
            "DC 15 + grapple damage dealt during that round",
            "| 5th | +5 | +4 | +1 | +1 | Choke-out |",
        ),
        "anomalies": 0,
        "anomaly_note_terms": (),
    },
    79: {
        "name": "Brawler", "page": 177, "span": (270, 329),
        "compiled": [176, 177], "issue": "Dragon Magazine #295",
        "issue_pages": [72, 73, 74],
        "ocr_path": r"I:\Sourcebooks\_text\Dragon Magazine\Dragon Magazine #295.md",
        "ocr_lines": ["9343-9398", "9445-9502", "9533-9608"],
        "hit_die": "d10", "rows": 5,
        "abilities": (
            "Weapon and Armor Proficiency", "Improvise Weapon (Ex)",
            "Crowd Fighting (Ex)", "Improvised Weapon Feats (Ex)",
            "Subdual Damage Reduction (Su)", "Bludgeoning Substitution (Su)",
        ),
        "required": (
            "A fierce grappler gains proficiency with all simple and martial weapons.",
            "Intimidate: 5 ranks.",
            "| 5th | +5 | +4 | +4 | +1 | Bludgeoning substitution, crowd fighting +3 |",
        ),
        "anomalies": 1,
        "anomaly_note_terms": ("A fierce grappler gains proficiency",),
    },
    122: {
        "name": "Dragonscribe", "page": 300, "span": (329, 443),
        "compiled": [300, 301], "issue": "Dragon Magazine #296",
        "issue_pages": [29, 30],
        "ocr_path": r"I:\Sourcebooks\_text\Dragon Magazine\Dragon Magazine #296.md",
        "ocr_lines": ["1829-2091"], "hit_die": "d4", "rows": 5,
        "abilities": (
            "Weapon and Armor Proficiency", "Spells per Day/Spells Known",
            "Dragonlore", "Overcome Resistance (Ex)", "Dragon Tongue (Ex)",
            "Summon Dragon (Sp)", "Draconic Binding (Sp)",
        ),
        "required": (
            "The DC to resist the effect is equal to 19 + the dragonscribe’s Charisma modifier.",
            "| 5th | +2 | +1 | +1 | +4 | *Draconic binding* | +1 level of existing class |",
        ),
        "anomalies": 0,
        "anomaly_note_terms": (),
    },
    123: {
        "name": "Knight of the Scale", "page": 302, "span": (443, 523),
        "compiled": [301, 302], "issue": "Dragon Magazine #296",
        "issue_pages": [30, 31],
        "ocr_path": r"I:\Sourcebooks\_text\Dragon Magazine\Dragon Magazine #296.md",
        "ocr_lines": ["2092-2235", "2239-2265", "2293-2313"],
        "hit_die": "d10", "rows": 10,
        "abilities": (
            "Weapon and Armor Proficiency", "Blood of Heroes (Su)",
            "Detect Dragon (Sp)", "Dragonslaying (Su)", "Sacred Shield (Su)",
            "Shatter Scale (Su)", "Mount (Su)", "Ride-By Attack",
            "Heal Mount (Sp)", "Righteous Charge (Su)",
        ),
        "required": (
            "Weapon Focus (lance, heavy).", "starting at 2nd level",
            "| 3rd | +3 | +3 | +1 | +1 | Dragonslaying +1/+1d6 |",
            "quadrupled when using a lance",
            "| 10th | +10 | +6 | +3 | +3 | Righteous charge |",
        ),
        "anomalies": 2,
        "anomaly_note_terms": ("starting at 2nd level", "3rd level", "Weapon Focus (Lance, heavy)"),
    },
}

DRAGONLORE_ROWS = (
    "| Identifying a dragon’s age and color from a rough description. | 10 |",
    "| Identifying a dragon’s size from signs of its passage. | 15 |",
    "| Identifying a dragon’s name, age, and origin after an encounter. | 20 |",
    "| Identifying a dragon’s special abilities and spells known from its description. | 25 |",
    "| Determining the location of a dragon’s lair from scraps of information. | 30 |",
)

SUMMON_DRAGONS = (
    "Celestial brass dragon (wyrmling) (CG)",
    "Fiendish white dragon (wyrmling) (CE)",
    "Celestial bronze dragon (wyrmling) (LG)",
    "Fiendish blue dragon (wyrmling) (CE)",
    "Celestial copper dragon (very young) (CG)",
    "Fiendish green dragon (very young) (LE)",
    "Fiendish wyvern (NE)",
    "Celestial brass dragon (juvenile) (CG)",
    "Fiendish white dragon (juvenile) (CE)",
    "Celestial brass dragon (young adult) (CG)",
    "Fiendish black dragon (young adult) (LE)",
    "Celestial bronze dragon (adult) (LG)",
    "Fiendish blue dragon (adult) (LE)",
    "Celestial silver dragon (adult) (LG)",
    "Fiendish red dragon (adult) (CE)",
)

PROHIBITED = (
    "illustration by", "illustrated by", "art by", "photography by",
    "continued on page", "for your campaign", "for your character",
    "equipping the troops", "radiant servant of pelor", "knight of the chase",
    "master siege engineer", "heartseekers", "back issues", "www.",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    text = TEXT_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    mapping = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    ordinals = list(EXPECTED)
    names = [EXPECTED[ordinal]["name"] for ordinal in ordinals]

    require(
        mapping["generated_by"] == "individual-issue OCR normalization with manual compiled-page verification",
        "wrong verification authority",
    )
    require(
        mapping.get("source_policy") ==
        "individual_issue_ocr_with_compiled_page_visual_verification",
        "wrong source policy",
    )
    require(mapping["derived_source"] == "reference/prestige_fulltext_batch_e.md", "wrong derived source")
    require(mapping["owned_ordinals"] == ordinals, "wrong supplemental ordinal roster")
    require(mapping["owned_names"] == names, "wrong supplemental name roster")
    require(mapping.get("unresolved") == [], "supplemental batch must not claim unresolved rows")
    require([row["ordinal"] for row in mapping["recovered"]] == ordinals, "wrong recovered order")
    require(len(mapping["recovered"]) == 7, "batch must contain exactly seven recoveries")

    spans: list[tuple[int, int]] = []
    total_chars = 0
    for row in mapping["recovered"]:
        ordinal = row["ordinal"]
        expected = EXPECTED[ordinal]
        name = expected["name"]
        require(row["name"] == name and row["page"] == expected["page"], f"{ordinal}: canonical identity mismatch")
        require(row.get("hit_die") == expected["hit_die"], f"{ordinal} {name}: map Hit Die changed")
        require(row.get("advancement_rows") == expected["rows"], f"{ordinal} {name}: map advancement rows changed")
        require((row["start"], row["end"]) == expected["span"], f"{ordinal} {name}: exact line span changed")
        start, end = row["start"], row["end"]
        require(0 <= start < end <= len(lines), f"{ordinal} {name}: invalid line span")
        spans.append((start, end))
        block_lines = lines[start:end]
        block = "\n".join(block_lines)
        total_chars += len(block)

        require(block_lines[0] == f"## {name}", f"{ordinal} {name}: slice does not start at its heading")
        require(len(re.findall(r"^## [^#]", block, flags=re.MULTILINE)) == 1, f"{ordinal} {name}: neighboring class leaked")
        require(row["start_anchor"] in "\n".join(block_lines[:20]), f"{ordinal} {name}: start anchor not near slice start")
        require(row["end_anchor"] in "\n".join(block_lines[-24:]), f"{ordinal} {name}: end anchor not near slice end")
        require(row["stop_before_anchor"].casefold() not in block.casefold(), f"{ordinal} {name}: stop-before anchor leaked")
        require(row["full_description"] is True and row["soft"] is False, f"{ordinal} {name}: not strict full text")
        require(row.get("uncapped_exact_slice") is True, f"{ordinal} {name}: uncapped exact-slice flag absent")
        digest = hashlib.sha256(block.encode("utf-8")).hexdigest()
        require(row.get("slice_sha256") == digest, f"{ordinal} {name}: exact slice digest mismatch")

        require(row["source_path"] == mapping["source_pdf"], f"{ordinal} {name}: wrong compiled source path")
        require(row["description_pages"] == expected["compiled"], f"{ordinal} {name}: wrong description pages")
        require(row["compiled_visual_pages"] == expected["compiled"], f"{ordinal} {name}: compiled page provenance changed")
        require(row["full_text_start_page"] == expected["compiled"][0], f"{ordinal} {name}: wrong compiled start page")
        require(row["full_text_end_page"] == expected["compiled"][-1], f"{ordinal} {name}: wrong compiled end page")
        require(len(row["source_flow"]) == len(expected["compiled"]), f"{ordinal} {name}: source flow must cover every compiled page")
        require(row["issue"] == expected["issue"], f"{ordinal} {name}: wrong issue")
        require(row["issue_pdf_pages"] == expected["issue_pages"], f"{ordinal} {name}: wrong issue pages")
        require(row["issue_ocr_path"] == expected["ocr_path"], f"{ordinal} {name}: wrong OCR path")
        require(row["issue_ocr_lines"] == expected["ocr_lines"], f"{ordinal} {name}: wrong OCR line provenance")

        require(f"Hit Die: {expected['hit_die']}." in block, f"{ordinal} {name}: wrong or missing Hit Die")
        table_rows = len(re.findall(r"^\| (?:[1-9]|10)(?:st|nd|rd|th) \|", block, flags=re.MULTILINE))
        require(table_rows == expected["rows"], f"{ordinal} {name}: expected {expected['rows']} advancement rows, found {table_rows}")
        for ability in expected["abilities"]:
            require(f"**{ability}:**" in block, f"{ordinal} {name}: missing ability {ability}")
        for phrase in expected["required"]:
            require(phrase in block, f"{ordinal} {name}: missing required rules text {phrase!r}")

        checks = row["checks"]
        for check in (
            "issue_ocr_compared", "rendered_pages_verified", "caption_leakage_checked",
            "advertisement_leakage_checked", "sidebar_leakage_checked",
            "neighbor_leakage_checked", "rules_tables_checked",
        ):
            require(checks.get(check) is True, f"{ordinal} {name}: check not locked: {check}")
        require(
            len(row.get("printed_source_anomalies", [])) == expected["anomalies"],
            f"{ordinal} {name}: printed-source anomaly notes changed",
        )
        anomaly_notes = "\n".join(row.get("printed_source_anomalies", []))
        for phrase in expected["anomaly_note_terms"]:
            require(phrase in anomaly_notes, f"{ordinal} {name}: anomaly note missing {phrase!r}")
        for phrase in PROHIBITED:
            require(phrase not in block.casefold(), f"{ordinal} {name}: prohibited caption/ad/sidebar/neighbor leakage: {phrase}")
        require(not re.search(r"^L\d+\s*\|", block, flags=re.MULTILINE), f"{ordinal} {name}: OCR line labels leaked")
        require("## [PDF page" not in block, f"{ordinal} {name}: OCR page marker leaked")
        require("�" not in block and "Â" not in block and "â€" not in block, f"{ordinal} {name}: mojibake leaked")

    require(
        spans == [(6, 76), (76, 149), (149, 209), (209, 270), (270, 329), (329, 443), (443, 523)],
        "locked line-span sequence changed",
    )
    require(all(left[1] == right[0] for left, right in zip(spans, spans[1:])), "slices contain a gap or overlap")
    require(spans[0][0] == 6 and spans[-1][1] == len(lines), "class slices must cover the full Markdown body")
    headings = [line[3:] for line in lines if re.match(r"^## [^#]", line)]
    require(headings == names, "Markdown class headings do not match the recovered roster")

    dragonscribe = "\n".join(lines[EXPECTED[122]["span"][0]:EXPECTED[122]["span"][1]])
    for exact in DRAGONLORE_ROWS:
        require(exact in dragonscribe, f"Dragonscribe: missing exact Dragonlore row {exact!r}")
    for exact in SUMMON_DRAGONS:
        require(exact in dragonscribe, f"Dragonscribe: missing Summon Dragon choice {exact!r}")
    require(
        re.findall(r"^\*\*Summon Monster (III|IV|V|VI|VII|VIII|IX)\*\*$", dragonscribe, flags=re.MULTILINE)
        == ["III", "IV", "V", "VI", "VII", "VIII", "IX"],
        "Dragonscribe: Summon Monster list headings are incomplete or out of order",
    )

    require([EXPECTED[o]["rows"] for o in ordinals] == [10, 10, 10, 5, 5, 5, 10], "locked row-count contract changed")
    print(
        "BATCH_E_OFFLINE_ACCEPTANCE "
        f"recovered=7 spans=7 rows=55 exact_chars={total_chars} errors=0"
    )


if __name__ == "__main__":
    main()
