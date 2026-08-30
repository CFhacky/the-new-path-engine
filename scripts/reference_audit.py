#!/usr/bin/env python3
"""Audit every committed reference family from one explicit registry.

This is repository tooling, not a harvester. It never reads or writes Notion
and never invents source values. The manifest selects accepted entry arrays
explicitly, so diagnostic lists cannot leak into the Codex by recursion.

Usage:
    python scripts/reference_audit.py
    python scripts/reference_audit.py --report
    python scripts/reference_audit.py --live --build-codex
    python scripts/reference_audit.py --selftest
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REF = REPO / "reference"
MANIFEST = REF / "families.json"
CODEX_DATA = REPO / "codex" / "build" / "engine_data.json"
CODEX_HTML = REPO / "codex" / "build" / "engine_reference.html"
SYSTEM_ALIASES = {"dnd35": "D&D 3.5e", "gurps4e": "GURPS 4e"}
CONTEXT_KEYS = ("corpus", "source_path", "book", "citation", "system")
BAD_NAME = re.compile(
    r"^(?:CHAPTER\s+\d+\b|POWERS?,\s+MANTLES\b)", re.IGNORECASE
)


def _context(node, inherited):
    out = dict(inherited)
    if isinstance(node, dict):
        for key in CONTEXT_KEYS:
            value = node.get(key)
            if isinstance(value, str) and value.strip():
                out[key] = value.strip()
    return out


def rows_at_path(obj, path):
    """Return (row, effective_context) pairs from a dotted manifest path."""
    tokens = path.split(".") if path else []
    found = []
    errors = []

    def walk(node, index, inherited):
        context = _context(node, inherited)
        if index == len(tokens):
            if isinstance(node, dict) and isinstance(node.get("name"), str):
                found.append((node, context))
            else:
                errors.append(f"{path}: selected value is not a named object")
            return

        if not isinstance(node, dict):
            errors.append(f"{path}: cannot read {tokens[index]!r} from non-object")
            return

        token = tokens[index]
        many = token.endswith("[]")
        key = token[:-2] if many else token
        if key not in node:
            errors.append(f"{path}: missing key {key!r}")
            return
        child = node[key]

        if many:
            if not isinstance(child, list):
                errors.append(f"{path}: {key!r} is not a list")
                return
            for value in child:
                walk(value, index + 1, context)
        elif isinstance(child, list):
            for value in child:
                walk(value, index + 1, context)
        else:
            walk(child, index + 1, context)

    walk(obj, 0, {})
    return found, errors


def _display_system(value):
    return SYSTEM_ALIASES.get(value, value)


def _display_book(value):
    leaf = re.split(r"[\\/]", str(value))[-1]
    return re.sub(r"\.(?:md|txt|pdf)$", "", leaf, flags=re.IGNORECASE).strip()


def load_manifest():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("reference/families.json schema_version must be 1")
    families = data.get("families")
    if not isinstance(families, list):
        raise ValueError("reference/families.json families must be a list")
    return families


def structural_audit(report=False):
    errors = []
    try:
        families = load_manifest()
    except Exception as exc:
        return [f"manifest: {exc}"], {}

    ids = [spec.get("id") for spec in families]
    json_paths = [spec.get("json") for spec in families]
    if len(families) != 43:
        errors.append(f"manifest: {len(families)} families, expected 43")
    if len(ids) != len(set(ids)):
        errors.append("manifest: duplicate family id")
    if len(json_paths) != len(set(json_paths)):
        errors.append("manifest: duplicate JSON path")

    declared = set(json_paths)
    actual = {
        path.relative_to(REPO).as_posix()
        for path in REF.glob("*_index.json")
    }
    for path in sorted(declared - actual):
        errors.append(f"manifest: missing declared index {path}")
    for path in sorted(actual - declared):
        errors.append(f"manifest: unregistered index {path}")

    family_counts = collections.Counter()
    system_counts = collections.Counter()
    total_rows = 0

    for spec in families:
        family = spec.get("id", "<missing-id>")
        json_path = REPO / str(spec.get("json", ""))
        md_path = REPO / str(spec.get("markdown", ""))
        harvester = REPO / str(spec.get("harvester", ""))

        for label, path in (
            ("JSON", json_path),
            ("Markdown", md_path),
            ("harvester", harvester),
        ):
            if not path.is_file():
                errors.append(f"{family}: {label} missing: {path}")
        if not json_path.is_file():
            continue

        try:
            raw_text = json_path.read_text(encoding="utf-8")
            obj = json.loads(raw_text)
        except Exception as exc:
            errors.append(f"{family}: invalid JSON: {exc}")
            continue

        generated_by = obj.get("generated_by") if isinstance(obj, dict) else None
        if generated_by and generated_by != spec.get("harvester"):
            errors.append(
                f"{family}: generated_by={generated_by!r}, "
                f"manifest={spec.get('harvester')!r}"
            )

        pairs, path_errors = rows_at_path(obj, str(spec.get("entry_path", "")))
        errors.extend(f"{family}: {message}" for message in path_errors)
        expected = spec.get("expected_count")
        if len(pairs) != expected:
            errors.append(f"{family}: {len(pairs)} rows, expected {expected}")

        page_gaps = collections.Counter()
        allowed_systems = set(spec.get("systems", []))
        scope = spec.get("scope")

        for row, context in pairs:
            name = row.get("name", "").strip()
            if not name:
                errors.append(f"{family}: empty entry name")
                continue
            if BAD_NAME.match(name):
                errors.append(f"{family}: rejected running header name {name!r}")
            if "\ufffd" in json.dumps(row, ensure_ascii=False):
                errors.append(f"{family}/{name}: parsed U+FFFD present in accepted row")

            book_value = row.get("book") or context.get("book")
            book = _display_book(book_value) if book_value else ""
            if not book:
                errors.append(f"{family}/{name}: missing book provenance")

            page = row.get("page")
            citation = row.get("citation") or context.get("citation") or ""
            cited_page = re.search(
                r"(?:\bpp?\.\s*\d|\bB\d+|\[PDF page \d+\])",
                str(citation),
                re.IGNORECASE,
            )
            if (page is None or page == "") and not cited_page:
                page_gaps[book] += 1

            direct_system = row.get("system")
            inherited_system = direct_system or context.get("system")
            if inherited_system:
                effective_system = _display_system(inherited_system)
            elif len(allowed_systems) == 1:
                effective_system = next(iter(allowed_systems))
            else:
                effective_system = ""

            if effective_system not in allowed_systems:
                errors.append(
                    f"{family}/{name}: system {effective_system!r} "
                    f"not in {sorted(allowed_systems)!r}"
                )
            if scope == "labeled" and direct_system not in allowed_systems:
                errors.append(
                    f"{family}/{name}: non-native row lacks direct exact system label"
                )

            family_counts[family] += 1
            system_counts[effective_system] += 1
            total_rows += 1

        expected_gaps = {
            item["book"]: item["expected_count"]
            for item in spec.get("page_exceptions", [])
        }
        if dict(page_gaps) != expected_gaps:
            errors.append(
                f"{family}: page gaps {dict(page_gaps)!r}, "
                f"expected {expected_gaps!r}"
            )

        if report:
            systems = ", ".join(spec.get("systems", []))
            print(f"{family:24} {len(pairs):5}  {systems}")

    summary = {
        "families": len(families),
        "rows": total_rows,
        "family_counts": family_counts,
        "system_counts": system_counts,
    }
    return errors, summary


def run_live_selftests(families):
    errors = []
    seen = set()
    for spec in families:
        harvester = spec["harvester"]
        if harvester in seen:
            continue
        seen.add(harvester)
        result = subprocess.run(
            [sys.executable, harvester, "--selftest"],
            cwd=REPO,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if result.returncode:
            errors.append(
                f"{harvester}: selftest failed\n"
                + "\n".join(result.stdout.splitlines()[-20:])
            )
            print(f"FAIL {harvester}")
        else:
            print(f"PASS {harvester}")
    print(f"LIVE_SELFTESTS total={len(seen)} failed={len(errors)}")
    return errors


def build_and_audit_codex(summary, report=False):
    errors = []
    command = [sys.executable, "codex/build_codex.py"]
    if report:
        command.append("--report")
    result = subprocess.run(
        command,
        cwd=REPO,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.returncode:
        return [f"Codex build failed with exit {result.returncode}"]

    try:
        rows = json.loads(CODEX_DATA.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"Codex data unreadable: {exc}"]

    if not isinstance(rows, list):
        errors.append("Codex data root is not a list")
        return errors

    family_counts = collections.Counter(row.get("fam") for row in rows)
    system_counts = collections.Counter(row.get("sys") for row in rows)
    if family_counts != summary["family_counts"]:
        errors.append("Codex family counts do not match reference manifest")
    if system_counts != summary["system_counts"]:
        errors.append("Codex system counts do not match reference manifest")
    if any(not row.get("name") or not row.get("book") for row in rows):
        errors.append("Codex contains a row without name/book provenance")
    if any(BAD_NAME.match(str(row.get("name", ""))) for row in rows):
        errors.append("Codex contains a rejected running-header name")
    if "\ufffd" in json.dumps(rows, ensure_ascii=False):
        errors.append("Codex parsed payload contains U+FFFD")

    if not CODEX_HTML.is_file():
        errors.append("Codex HTML was not created")
    else:
        size = CODEX_HTML.stat().st_size
        if size >= 16 * 1024 * 1024:
            errors.append(f"Codex HTML exceeds 16 MiB: {size} bytes")
        html = CODEX_HTML.read_text(encoding="utf-8")
        if "__ENGINE_DATA_B64__" in html:
            errors.append("Codex HTML still contains the data placeholder")
        print(f"CODEX_SMOKE rows={len(rows)} size_bytes={size}")

    return errors


def selftest():
    fixture = {
        "sources": [{
            "book": "folder/Fixture Book.md",
            "citation": "Fixture Book p.1",
            "system": "dnd35",
            "entries": [{"name": "Real Entry", "page": 1}],
            "soft": [{"name": "Rejected Fragment", "page": 1}],
        }]
    }
    pairs, errors = rows_at_path(fixture, "sources[].entries")
    assert not errors, errors
    assert [row["name"] for row, _ in pairs] == ["Real Entry"]
    assert pairs[0][1]["book"] == "folder/Fixture Book.md"
    assert _display_system(pairs[0][1]["system"]) == "D&D 3.5e"
    assert _display_book(pairs[0][1]["book"]) == "Fixture Book"
    print("selftest: manifest path selects accepted rows only")
    print("selftest: source provenance and system aliases resolve")
    print("selftest: PASS")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--build-codex", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)

    if args.selftest:
        selftest()
        return 0

    errors, summary = structural_audit(report=args.report)
    if not errors and args.live:
        errors.extend(run_live_selftests(load_manifest()))
    if not errors and args.build_codex:
        errors.extend(build_and_audit_codex(summary, report=args.report))

    if errors:
        print("\nREFERENCE AUDIT FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"REFERENCE_AUDIT families={summary['families']} "
        f"rows={summary['rows']} errors=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
