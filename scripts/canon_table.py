#!/usr/bin/env python3
"""canon_table.py -- the Eusebian layer: one event, every witness, addresses kept apart.

Eusebius of Caesarea numbered the sections of the four gospels and built
canon tables saying which sections narrate the same event, and he refused to
merge the accounts. This script does the same for the Siege of Terra library:
an authored event registry lists each event's witnesses by pinned address
(scripts/verse_address.py maps), narrator, narration mode, the synchronism
the verse states, and a short quote. The output is a canon table (rows are
events, columns are books) and one page per event. Disagreements between
witnesses are printed, never resolved.

GOVERNING SOURCES
    reference/canon/events.json          -- the authored registry (data, not canon)
    reference/addresses/*.address.json   -- pinned editions; every address must resolve
    empyrean-siege-gm skill: label rulings; the chronology across published
        sources is disputed, so relative synchronisms only, never a calendar.

CHECKS (`--check` makes them fatal)
    - every witness address resolves to a unit in its book's map
    - with --corpus DIR: the map's pinned edition matches the file, and the
      witness quote is found inside the addressed unit (corpus-exact)
    - a book column with no map is reported as "no edition pinned"

USAGE
    python canon_table.py                           # render docs/canon/
    python canon_table.py --corpus DIR --check      # verify quotes against the pinned editions
    python canon_table.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verse_address import find_unit, parse_address, verify  # deliberate shared logic

REPO = Path(__file__).resolve().parent.parent
REGISTRY = REPO / "reference" / "canon" / "events.json"
OUT_DIR = REPO / "docs" / "canon"
MODE_CODE = {"first": "1st", "second": "2nd", "close-third": "3rd", "omniscient": "omn", "hearsay": "hrs"}
_NORM = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-", " ": " ", "*": "", "_": ""})


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.translate(_NORM)).casefold().strip()


def load_registry(path: Path) -> Dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise SystemExit("events.json schema_version must be 1")
    return data


def load_maps(registry: Dict, repo: Path) -> Dict[str, Dict]:
    maps: Dict[str, Dict] = {}
    for b in registry["books"]:
        if b.get("map"):
            p = repo / b["map"]
            if p.is_file():
                maps[b["key"]] = json.loads(p.read_text(encoding="utf-8"))
    return maps


def check_witness(w: Dict, maps: Dict[str, Dict], corpus: Optional[Path], corpus_lines: Dict[str, List[str]],
                  edition_ok: Dict[str, bool]) -> Tuple[Dict, List[str]]:
    """Resolve the address; verify the quote when the corpus is present."""
    errors: List[str] = []
    out = dict(w)
    try:
        a = parse_address(w["address"])
    except ValueError as e:
        errors.append(str(e))
        out["status"] = "BAD ADDRESS"
        return out, errors
    key = a["key"]
    m = maps.get(key)
    if m is None:
        out["status"] = "no edition pinned"
        errors.append(f"{w['address']}: no address map for {key}")
        return out, errors
    unit = find_unit(m, w["address"])
    if unit is None:
        out["status"] = "UNRESOLVED"
        errors.append(f"{w['address']}: not a unit of {key} ({m['edition']['sha256'][:12]})")
        return out, errors
    out["unit_title"] = unit.get("title")
    out["anchor"] = unit["anchor"]
    if key not in corpus_lines:
        out["status"] = "address-resolved; quote unchecked (no corpus)"
        return out, errors
    if not edition_ok.get(key, False):
        out["status"] = "EDITION MISMATCH"
        errors.append(f"{key}: corpus file does not match the pinned edition")
        return out, errors
    lines = corpus_lines[key]
    span = " ".join(norm(l) for l in lines[unit["line"] - 1:unit["line_end"]])
    if norm(w["quote"]) in span:
        out["status"] = "corpus-exact"
    else:
        out["status"] = "QUOTE MISS"
        errors.append(f"{w['address']}: quote not found in the addressed unit: {w['quote'][:50]!r}")
    return out, errors


def build(registry: Dict, maps: Dict[str, Dict], corpus: Optional[Path]) -> Tuple[Dict, List[str]]:
    corpus_lines: Dict[str, List[str]] = {}
    edition_ok: Dict[str, bool] = {}
    if corpus:
        for key, m in maps.items():
            f = corpus / m["edition"]["file"]
            if f.is_file():
                corpus_lines[key] = f.read_text(encoding="utf-8", errors="replace").splitlines()
                edition_ok[key] = verify(m, f)[0]
    errors: List[str] = []
    events = []
    for ev in registry["events"]:
        ws = []
        for w in ev["witnesses"]:
            checked, errs = check_witness(w, maps, corpus, corpus_lines, edition_ok)
            ws.append(checked)
            errors.extend(errs)
        events.append({**ev, "witnesses": ws})
    return {"books": registry["books"], "modes": registry["narration_modes"], "events": events,
            "maps": {k: m["edition"] for k, m in maps.items()}}, errors


def short_addr(addr: str) -> str:
    return addr.split(" ", 1)[1] if " " in addr else addr


def render_table(data: Dict) -> str:
    books = data["books"]
    o = ["# Siege of Terra canon table", "",
         "**Generated by scripts/canon_table.py from reference/canon/events.json. Do not hand-edit.**  ",
         "Rows are events; columns are books. A cell holds every address in that book that witnesses the event, "
         "with the narration mode (1st, 2nd, 3rd, omn = omniscient, hrs = hearsay). Witnesses are kept apart, "
         "never harmonised; disagreements live on the event page. Addresses are valid only against the pinned "
         "editions listed below. Nothing here is campaign canon.", "",
         "## Pinned editions", ""]
    for b in books:
        ed = data["maps"].get(b["key"])
        if ed:
            o.append(f"- **{b['key']}** {b['title']} ({b['author']}): `{ed['file']}` sha256 `{ed['sha256'][:16]}…`, {ed['lines']} lines")
        else:
            o.append(f"- **{b['key']}** {b['title']} ({b['author']}): *no edition pinned* -- run `scripts/verse_address.py` on the book and add its map to events.json")
    o += ["", "## Table", ""]
    o.append("| Event | " + " | ".join(b["key"] for b in books) + " |")
    o.append("|---|" + "|".join("---" for _ in books) + "|")
    for ev in data["events"]:
        cells = []
        for b in books:
            hits = [w for w in ev["witnesses"] if parse_address(w["address"])["key"] == b["key"]]
            if hits:
                cells.append("<br>".join(f"{short_addr(w['address'])} [{MODE_CODE.get(w['mode'], w['mode'])}]" for w in hits))
            elif not data["maps"].get(b["key"]):
                cells.append("*no edition*")
            else:
                cells.append("·")
        o.append(f"| [{ev['id']}]({ev['id']}-{ev['slug']}.md) {ev['title']} | " + " | ".join(cells) + " |")
    o += ["", "## Verification", ""]
    counts: Dict[str, int] = {}
    for ev in data["events"]:
        for w in ev["witnesses"]:
            counts[w["status"]] = counts.get(w["status"], 0) + 1
    for k, v in sorted(counts.items()):
        o.append(f"- {k}: {v}")
    return "\n".join(o) + "\n"


def render_event(ev: Dict, data: Dict) -> str:
    o = [f"# {ev['id']} -- {ev['title']}", "",
         f"*Class:* {ev['class']}  ", f"*Witnesses:* {len(ev['witnesses'])}  ", "",
         "| Address | Unit title | Narrator | Mode | Synchronism (as the verse states it) | Quote | Verification |",
         "|---|---|---|---|---|---|---|"]
    for w in ev["witnesses"]:
        o.append(f"| {w['address']} | {w.get('unit_title') or ''} | {w['narrator']} | {w['mode']} | {w['synchronism']} | \"{w['quote']}\" | {w['status']} |")
    o += ["", "## Disagreements (kept, not harmonised)", "", ev.get("disagreements") or "None recorded.", "",
          "## Resolving a witness", "",
          "```", f"python scripts/verse_address.py --map reference/addresses/<book>.address.json --resolve \"{ev['witnesses'][0]['address']} ¶1\" --book <corpus>/<file>", "```",
          "", "Labels: the quote and address are SOURCE-VERIFIED when the verification column reads corpus-exact; "
          "the narrator and mode are the registry author's reading (INFERRED); the synchronism is only what the verse states."]
    return "\n".join(o) + "\n"


def write_docs(data: Dict, out_dir: Path) -> List[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written = [out_dir / "README.md"]
    written[0].write_text(render_table(data), encoding="utf-8")
    for ev in data["events"]:
        p = out_dir / f"{ev['id']}-{ev['slug']}.md"
        p.write_text(render_event(ev, data), encoding="utf-8")
        written.append(p)
    return written


def selftest() -> int:
    fails: List[str] = []
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        book = d / "tb.md"
        book.write_text("PART ONE\n1:i\nPART ONE\n1:i\nFirst light\nThe angel fell here.\n1:ii\nElsewhere.\n", encoding="utf-8")
        import verse_address as va
        m = va.build_map(book, "TB", "Test Book")
        (d / "tb.address.json").write_text(json.dumps(m), encoding="utf-8")
        reg = {"schema_version": 1, "books": [
            {"key": "TB", "title": "Test Book", "author": "A", "series": "S", "map": "tb.address.json"},
            {"key": "NB", "title": "No Book", "author": "B", "series": "S", "map": None}],
            "narration_modes": {"first": "", "omniscient": "", "hearsay": ""},
            "events": [{"id": "EV-01", "slug": "fall", "class": "death", "title": "The angel falls", "witnesses": [
                {"address": "TB 1:i", "narrator": "N", "mode": "omniscient", "synchronism": "none", "quote": "The angel fell here."},
                {"address": "TB 1:ii", "narrator": "N", "mode": "hearsay", "synchronism": "none", "quote": "not in this verse"},
                {"address": "TB 3:i", "narrator": "N", "mode": "first", "synchronism": "none", "quote": "x"}],
                "disagreements": "test"}]}
        maps = load_maps(reg, d)
        data, errors = build(reg, maps, d)
        st = [w["status"] for w in data["events"][0]["witnesses"]]
        if st != ["corpus-exact", "QUOTE MISS", "UNRESOLVED"]:
            fails.append(f"statuses {st}")
        if len(errors) != 2:
            fails.append(f"errors {errors}")
        data2, errors2 = build(reg, maps, None)
        if data2["events"][0]["witnesses"][0]["status"] != "address-resolved; quote unchecked (no corpus)":
            fails.append("no-corpus status")
        book.write_text("changed\n", encoding="utf-8")
        data3, errors3 = build(reg, maps, d)
        if data3["events"][0]["witnesses"][0]["status"] != "EDITION MISMATCH":
            fails.append("edition mismatch not detected")
        files = write_docs(data, d / "out")
        table = (d / "out" / "README.md").read_text(encoding="utf-8")
        if "| [EV-01](EV-01-fall.md) The angel falls | 1:i [omn]<br>1:ii [hrs]<br>3:i [1st] | *no edition* |" not in table:
            fails.append("table row wrong:\n" + table)
        if len(files) != 2 or "## Disagreements" not in files[1].read_text(encoding="utf-8"):
            fails.append("event page")
    for f in fails:
        print("FAIL:", f)
    print(f"SELFTEST {'OK' if not fails else 'FAILED'}: {len(fails)} failures")
    return 1 if fails else 0


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--registry", default=str(REGISTRY))
    p.add_argument("--corpus", default=str(REPO / "corpus" / "teatd"), help="folder holding the pinned edition files named as the maps record them (default: corpus/teatd/)")
    p.add_argument("--out", default=str(OUT_DIR))
    p.add_argument("--check", action="store_true", help="exit 1 on any unresolved address, edition mismatch or quote miss")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        sys.exit(selftest())
    reg = load_registry(Path(a.registry))
    maps = load_maps(reg, REPO)
    corpus = Path(a.corpus) if a.corpus and Path(a.corpus).is_dir() else None
    data, errors = build(reg, maps, corpus)
    files = write_docs(data, Path(a.out))
    n_w = sum(len(e["witnesses"]) for e in data["events"])
    print(f"WROTE {len(files)} pages under {a.out}: {len(data['events'])} events, {n_w} witnesses, "
          f"{len(maps)} pinned books of {len(reg['books'])}")
    for e in errors:
        print("  ", e)
    if a.check and errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
