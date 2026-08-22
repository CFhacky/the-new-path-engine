#!/usr/bin/env python3
"""Validate or generate The New Path campaign resume-card Markdown.

Governing sources:
- Notion: The New Path Play Contract — Live Session Governance
  (3c4e8214-84b0-818f-93c0-df1da2e52043).
- Notion: Campaign Resume Card Schema and Maintenance
  (3c4e8214-84b0-81dc-b0ae-eaf6ebb9bb48).
- GitHub: docs/runtime-control/RESUME_CARD_SCHEMA.md.

This script validates structure only. It never decides whether campaign facts are
true and never reads a resume as live state. Notion remains canon.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

EXIT_OK = 0
EXIT_INVALID = 1
EXIT_USAGE = 2

REQUIRED_FRONTMATTER = {
    "name",
    "type",
    "authority",
    "snapshot_date",
    "source_notion",
    "scope",
}

REQUIRED_LANE_LABELS = (
    "Snapshot authority.",
    "Position.",
    "Last canonical close.",
    "Exact resume point.",
    "Rulings required before boot.",
    "Due at boot.",
    "Open machinery.",
    "Hard prohibitions.",
    "Delegated / background operations.",
    "Record debt / stale pointers.",
    "Boot line.",
    "Freshness invalidators.",
)

LANE_HEADING = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
FIELD_LABEL = re.compile(r"^\*\*(.+?)\*\*", re.MULTILINE)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass(frozen=True)
class ValidationResult:
    errors: tuple[str, ...]
    warnings: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.errors


def parse_frontmatter(text: str) -> tuple[dict[str, str], str, list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, text, ["missing opening YAML-style frontmatter delimiter"]
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text, ["missing closing YAML-style frontmatter delimiter"]

    raw = text[4:end]
    body = text[end + 5 :]
    data: dict[str, str] = {}
    for lineno, line in enumerate(raw.splitlines(), start=2):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"frontmatter line {lineno} is not key: value")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key or not value:
            errors.append(f"frontmatter line {lineno} has an empty key or value")
            continue
        if key in data:
            errors.append(f"frontmatter key repeated: {key}")
            continue
        data[key] = value
    return data, body, errors


def split_lane_sections(body: str) -> list[tuple[str, str]]:
    matches = list(LANE_HEADING.finditer(body))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections.append((title, body[start:end]))
    return sections


def validate_snapshot(text: str) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    frontmatter, body, fm_errors = parse_frontmatter(text)
    errors.extend(fm_errors)

    missing = sorted(REQUIRED_FRONTMATTER - set(frontmatter))
    if missing:
        errors.append("missing frontmatter keys: " + ", ".join(missing))

    if frontmatter.get("type") and frontmatter["type"] != "notion-mirror-snapshot":
        errors.append("frontmatter type must be notion-mirror-snapshot")

    authority = frontmatter.get("authority", "")
    if authority and "NON-AUTHORITATIVE MIRROR" not in authority.upper():
        errors.append("frontmatter authority must declare NON-AUTHORITATIVE MIRROR")

    snapshot_date = frontmatter.get("snapshot_date")
    if snapshot_date:
        if not DATE_RE.match(snapshot_date):
            errors.append("snapshot_date must use YYYY-MM-DD")
        else:
            try:
                dt.date.fromisoformat(snapshot_date)
            except ValueError:
                errors.append("snapshot_date is not a real calendar date")

    source_notion = frontmatter.get("source_notion", "")
    if source_notion and not (
        source_notion.startswith("http://")
        or source_notion.startswith("https://")
        or re.fullmatch(r"[0-9a-fA-F-]{32,36}", source_notion)
    ):
        errors.append("source_notion must be a Notion URL or page UUID")

    if "NON-AUTHORITATIVE MIRROR" not in body.upper():
        errors.append("body must display NON-AUTHORITATIVE MIRROR before lane content")

    sections = split_lane_sections(body)
    lane_sections = [
        (title, section)
        for title, section in sections
        if title.upper() != "CROSS-LANE LEDGER"
    ]
    if not lane_sections:
        errors.append("no lane cards found (expected one or more ## headings)")

    for title, section in lane_sections:
        labels = set(FIELD_LABEL.findall(section))
        missing_labels = [label for label in REQUIRED_LANE_LABELS if label not in labels]
        if missing_labels:
            errors.append(f"lane '{title}' missing labels: " + ", ".join(missing_labels))
        if "```" not in section:
            warnings.append(f"lane '{title}' Boot line is not in a fenced block")

    if "## CROSS-LANE LEDGER" not in body:
        warnings.append("no CROSS-LANE LEDGER section found")

    if re.search(r"\bcurrent(?:-resume)?\.md\b", body, re.IGNORECASE):
        errors.append("snapshot refers to an undated current.md/current-resume.md GitHub state file")

    return ValidationResult(tuple(errors), tuple(warnings))


def render_template(lane: str = "LANE") -> str:
    today = dt.date.today().isoformat()
    return f"""---
name: campaign-resumes-all-lanes-{today}
type: notion-mirror-snapshot
authority: NON-AUTHORITATIVE MIRROR
snapshot_date: {today}
source_notion: 00000000-0000-0000-0000-000000000000
scope: {lane}
---

# Campaign Resumes — All Lanes

> **NON-AUTHORITATIVE MIRROR.** Fetch the current Notion Resume Router before play.

## {lane} — POSITION

**Snapshot authority.** Notion pages read and date checked.

**Position.** Current physical/temporal state.

**Last canonical close.** Last fully installed close.

**Exact resume point.** First unplayed beat and what has not happened.

**Rulings required before boot.** None.

**Due at boot.** None.

**Open machinery.** Active but not yet due.

**Hard prohibitions.** Knowledge and agency locks.

**Delegated / background operations.** None.

**Record debt / stale pointers.** None.

**Boot line.**
```text
Run {lane}. Fetch the current Notion resume card and its named authorities.
```

**Freshness invalidators.** Any session close or state rewrite.

## CROSS-LANE LEDGER

None.
"""


def print_result(result: ValidationResult, path: Path | None = None) -> int:
    prefix = f"{path}: " if path else ""
    for warning in result.warnings:
        print(f"WARNING: {prefix}{warning}")
    for error in result.errors:
        print(f"ERROR: {prefix}{error}")
    if result.ok:
        print(f"PASS: {prefix}resume snapshot structure is valid")
        return EXIT_OK
    print(f"FAIL: {prefix}{len(result.errors)} validation error(s)")
    return EXIT_INVALID


def run_selftest() -> int:
    valid = render_template("TEST LANE")
    valid_result = validate_snapshot(valid)
    if not valid_result.ok:
        print("SELFTEST FAIL: generated template did not validate")
        print_result(valid_result)
        return EXIT_INVALID

    invalid = valid.replace("**Exact resume point.**", "**Resume maybe.**", 1)
    invalid_result = validate_snapshot(invalid)
    if invalid_result.ok or not any(
        "Exact resume point" in error for error in invalid_result.errors
    ):
        print("SELFTEST FAIL: missing required label was not detected")
        return EXIT_INVALID

    bad_authority = valid.replace(
        "authority: NON-AUTHORITATIVE MIRROR", "authority: CURRENT", 1
    )
    bad_result = validate_snapshot(bad_authority)
    if bad_result.ok:
        print("SELFTEST FAIL: authoritative snapshot was not rejected")
        return EXIT_INVALID

    print("SELFTEST PASS: template, missing-label, and authority checks behaved correctly")
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument(
        "--check", metavar="FILE", type=Path, help="validate a dated Notion mirror snapshot"
    )
    action.add_argument(
        "--write-template", action="store_true", help="print a blank valid resume snapshot template"
    )
    action.add_argument("--selftest", action="store_true", help="run built-in regression checks")
    parser.add_argument("--lane", default="LANE", help="lane name used by --write-template")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.write_template:
        print(render_template(args.lane), end="")
        return EXIT_OK
    if args.selftest:
        return run_selftest()
    if args.check:
        try:
            text = args.check.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"ERROR: cannot read {args.check}: {exc}")
            return EXIT_USAGE
        return print_result(validate_snapshot(text), args.check)
    return EXIT_USAGE


if __name__ == "__main__":
    raise SystemExit(main())
