#!/usr/bin/env python3
"""verse_address.py -- the Stephanus layer: a stable address grid over a book.

Gives every unit of a long-form text an address a session can cite and a
tool can resolve, in the manner of chapter-and-verse: a dumb, stable grid
laid over the words, orthogonal to sense, portable across editions as long
as the edition is pinned.

    KEY ch:verse          a native verse unit         (TEATD1 4:xviii)
    KEY ch:verse ¶n       the n-th paragraph in it    (TEATD1 4:xviii ¶12)
    KEY ch:¶n             chapter + paragraph, for books without verses
    KEY ¶n                paragraph only, for books without chapters

SCHEMES (detected, reported in the map)
    verse              lines reading "9:xxi" head each unit (Abnett's TEATD)
    chapter-paragraph  PART / Chapter / bare-number / spelled-number headings
    paragraph          nothing detectable; the grid is paragraphs from line 1

EDITION PINNING
    The map records the file's SHA-256, byte and line counts. `--verify`
    refuses a map whose edition no longer matches the file. Re-exporting a
    book from Notion with different paragraphing produces a new edition and
    a new map; old addresses are not silently reinterpreted.

WHAT IS AND IS NOT IN THE MAP
    Unit addresses, anchors, line spans, paragraph counts, an optional verse
    title, and an incipit (the first eight words, the unit's traditional
    name). No body text. The book is never copied into this repository.

USAGE
    python verse_address.py BOOK.md --key TEATD1 [--title T] [--out reference/addresses/teatd1.address.json]
    python verse_address.py --map reference/addresses/teatd1.address.json --verify BOOK.md
    python verse_address.py --map MAP --resolve "TEATD1 4:xviii ¶3" --book BOOK.md
    python verse_address.py --selftest

SHARED LOGIC
    scripts/notion_novel_bind.py imports is_verse_title() and paragraph
    counting from here on purpose, so EPUB anchor ids and map addresses agree.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# only the all-caps FRAGMENTS is a section; "Fragments" in title case is a verse title Abnett reuses
PART_LINE = re.compile(r"^\s*\**(?:(?:PART|Part|BOOK|Book)\s+([A-Z]+|[0-9]+|[IVXL]+)|(FRAGMENTS))\**\s*$")
BARE_ROMAN = re.compile(r"^\s*\**([ivxl]{1,7})\**\s*$")
VERSE_LINE = re.compile(r"^\s*\**(\d{1,2}):([ivxl]{1,7})\**\s*$", re.IGNORECASE)
SPELLED = ("ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN|ELEVEN|TWELVE|THIRTEEN|FOURTEEN|"
           "FIFTEEN|SIXTEEN|SEVENTEEN|EIGHTEEN|NINETEEN|TWENTY(?:-(?:ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE))?|"
           "THIRTY(?:-(?:ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE))?")
CHAPTER_LINE = re.compile(
    r"^\s*(?:#{1,3}\s+)?\**(?:(?:CHAPTER|Chapter)\s+(\d{1,3}|[IVXL]+)|(\d{1,3})|(" + SPELLED + r")|([IVXL]{1,6}))\**\s*$")
BACK_MATTER = re.compile(r"^\s*\**(Afterword|Acknowledgements|Acknowledgments|About the Author|"
                         r"An Extract|eBook license|A Black Library Publication|Also available|Glossary)\**\s*$", re.IGNORECASE)
ROMAN = {"i": 1, "v": 5, "x": 10, "l": 50}


def roman_int(s: str) -> int:
    total, prev = 0, 0
    for ch in reversed(s.lower()):
        v = ROMAN[ch]
        total = total - v if v < prev else total + v
        prev = max(prev, v)
    return total


def is_verse_title(line: str) -> bool:
    """The line after a verse heading is a title when it is short and does
    not read like prose: no terminal punctuation, no quotation, under 60
    characters."""
    s = line.strip().strip("*")
    if not s or len(s) >= 60:
        return False
    if s[-1] in ".!?\"'’”,;:" or s[0] in "\"'‘“":
        return False
    return True


def incipit(lines: List[str], start: int, end: int, words: int = 8) -> str:
    for i in range(start, end):
        s = lines[i].strip().strip("*")
        if s:
            ws = s.split()
            return " ".join(ws[:words]) + ("…" if len(ws) > words else "")
    return ""


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def body_start(lines: List[str]) -> int:
    """Skip a front-matter CONTENTS list that repeats every heading: the body
    starts at the second occurrence of the first PART/chapter heading."""
    first = None
    first_at = 0
    for i, line in enumerate(lines):
        if PART_LINE.match(line) or VERSE_LINE.match(line):
            key = line.strip()
            if first is None:
                first, first_at = key, i
            elif key == first:
                return i
    return first_at


def build_map(path: Path, key: str, title: Optional[str]) -> Dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    n = len(lines)
    start = body_start(lines)
    has_verses = any(VERSE_LINE.match(l) for l in lines[start:])
    # back matter: first back-matter heading after the last verse/chapter heading
    # keyed on real verse/chapter headings only: a bare roman numeral inside
    # the back matter must not extend the body
    last_head = start
    for i in range(start, n):
        if VERSE_LINE.match(lines[i]) or (not has_verses and CHAPTER_LINE.match(lines[i])):
            last_head = i
    back = n
    for i in range(last_head + 1, n):
        if BACK_MATTER.match(lines[i]):
            back = i
            break

    parts: List[Dict] = []
    units: List[Dict] = []
    scheme = "verse" if has_verses else "paragraph"
    chapter: Optional[int] = None
    part_title_pending = False
    # pass 1: headings
    heads: List[Tuple[int, str, Dict]] = []  # (line index, kind, payload)
    in_fragments = False
    for i in range(start, back):
        line = lines[i]
        m = PART_LINE.match(line)
        if m:
            parts.append({"part": line.strip().strip("*"), "line": i + 1, "title": None})
            part_title_pending = True
            in_fragments = bool(m.group(2))
            continue
        if in_fragments and BARE_ROMAN.match(line):
            heads.append((i, "verse", {"chapter": "F", "verse": BARE_ROMAN.match(line).group(1).lower()}))
            part_title_pending = False
            continue
        if part_title_pending and line.strip() and not VERSE_LINE.match(line) and not CHAPTER_LINE.match(line) \
                and is_verse_title(line):
            parts[-1]["title"] = line.strip().strip("*")
            part_title_pending = False
            continue
        part_title_pending = False
        m = VERSE_LINE.match(line)
        if m:
            heads.append((i, "verse", {"chapter": int(m.group(1)), "verse": m.group(2).lower()}))
            continue
        if not has_verses:
            m = CHAPTER_LINE.match(line)
            if m:
                scheme = "chapter-paragraph"
                raw = next(g for g in m.groups() if g)
                if raw.isdigit():
                    ch = int(raw)
                elif re.fullmatch(r"[IVXL]+", raw):
                    ch = roman_int(raw)
                else:
                    ch = len([h for h in heads if h[1] == "chapter"]) + 1
                heads.append((i, "chapter", {"chapter": ch}))
    # pass 2: units
    if not heads:
        body_lines = [i for i in range(start, back) if lines[i].strip()]
        units.append({"address": f"{key} ¶1-¶{len(body_lines)}", "anchor": "body", "chapter": None, "verse": None,
                      "title": None, "line": start + 1, "line_end": back, "paragraphs": len(body_lines),
                      "incipit": incipit(lines, start, back)})
    for idx, (i, kind, payload) in enumerate(heads):
        end = heads[idx + 1][0] if idx + 1 < len(heads) else back
        # a PART heading between units ends the unit early
        for j in range(i + 1, end):
            if PART_LINE.match(lines[j]):
                end = j
                break
        title = None
        first = i + 1
        if first < end and is_verse_title(lines[first]):
            title = lines[first].strip().strip("*")
            first += 1
        paras = [j for j in range(first, end) if lines[j].strip()]
        if kind == "verse":
            addr = f"{key} {payload['chapter']}:{payload['verse']}"
            anchor = f"v-{payload['chapter']}-{payload['verse']}"
        else:
            addr = f"{key} {payload['chapter']}"
            anchor = f"c-{payload['chapter']}"
        units.append({"address": addr, "anchor": anchor, "chapter": payload["chapter"],
                      "verse": payload.get("verse"), "title": title, "line": i + 1,
                      "first_paragraph_line": (paras[0] + 1) if paras else None,
                      "line_end": end, "paragraphs": len(paras),
                      "incipit": incipit(lines, first, end)})
    return {
        "generated_by": "scripts/verse_address.py",
        "book_key": key,
        "title": title or path.stem,
        "edition": {"file": path.name, "sha256": sha256(path), "bytes": path.stat().st_size, "lines": n},
        "scheme": scheme,
        "front_matter": {"line": 1, "line_end": start},
        "back_matter": {"line": back + 1 if back < n else None},
        "parts": parts,
        "unit_count": len(units),
        "paragraph_count": sum(u["paragraphs"] for u in units),
        "units": units,
    }


ADDR = re.compile(r"^\s*(\S+)\s+(?:(\d{1,3}|F):([ivxl]{1,7})|(\d{1,3}))?\s*(?:¶\s*(\d{1,5}))?\s*$")


def parse_address(addr: str) -> Dict:
    m = ADDR.match(addr)
    if not m or (m.group(2) is None and m.group(4) is None and m.group(5) is None):
        raise ValueError(f"bad address {addr!r}")
    raw_ch = m.group(2) or m.group(4)
    return {"key": m.group(1), "chapter": (raw_ch if raw_ch == "F" else int(raw_ch)) if raw_ch else None,
            "verse": m.group(3).lower() if m.group(3) else None, "paragraph": int(m.group(5)) if m.group(5) else None}


def find_unit(book_map: Dict, addr: str) -> Optional[Dict]:
    a = parse_address(addr)
    if a["key"] != book_map["book_key"]:
        return None
    for u in book_map["units"]:
        if u["chapter"] == a["chapter"] and (u.get("verse") or None) == a["verse"]:
            return u
    return None


def resolve(book_map: Dict, addr: str, lines: List[str]) -> Optional[str]:
    """Paragraph text for a paragraph address, or the unit's incipit line."""
    a = parse_address(addr)
    u = find_unit(book_map, addr)
    if u is None:
        return None
    paras = [j for j in range(u["line"], u["line_end"]) if lines[j].strip()
             and (u["title"] is None or j != u["line"]) ]
    # paragraphs start after the title line
    body = [j for j in range(u["first_paragraph_line"] - 1, u["line_end"]) if lines[j].strip()] if u.get("first_paragraph_line") else []
    if a["paragraph"] is None:
        return lines[body[0]] if body else ""
    if 1 <= a["paragraph"] <= len(body):
        return lines[body[a["paragraph"] - 1]]
    return None


def verify(book_map: Dict, path: Path) -> Tuple[bool, str]:
    actual = sha256(path)
    ok = actual == book_map["edition"]["sha256"]
    return ok, ("edition matches" if ok else
                f"EDITION MISMATCH: map pins {book_map['edition']['sha256'][:12]}…, file is {actual[:12]}…; "
                "addresses are not valid against this file")


def write_markdown(book_map: Dict, out: Path) -> None:
    o = [f"# {book_map['book_key']} -- address map for *{book_map['title']}*", "",
         "**Generated by scripts/verse_address.py. Do not hand-edit.**  ",
         f"Edition: `{book_map['edition']['file']}` sha256 `{book_map['edition']['sha256']}` "
         f"({book_map['edition']['bytes']} bytes, {book_map['edition']['lines']} lines). Scheme: `{book_map['scheme']}`. "
         f"{book_map['unit_count']} units, {book_map['paragraph_count']} paragraphs. "
         "Addresses are valid only against this edition.", ""]
    for p in book_map["parts"]:
        o.append(f"- {p['part']}" + (f" -- *{p['title']}*" if p.get("title") else "") + f" (line {p['line']})")
    o += ["", "| Address | Anchor | Title | ¶ | Incipit |", "|---|---|---|---:|---|"]
    for u in book_map["units"]:
        o.append(f"| {u['address']} | `{u['anchor']}` | {u['title'] or ''} | {u['paragraphs']} | {u['incipit']} |")
    out.write_text("\n".join(o) + "\n", encoding="utf-8")


def selftest() -> int:
    fails: List[str] = []
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        verse_book = d / "vb.md"
        verse_book.write_text(
            "CONTENTS\nPART ONE\n1:i\n1:ii\nPART ONE\nA TITLE\n1:i\nFirst light\nPara one.\nPara two.\n1:ii\n"
            "'Quoted opener,' she said.\nPara b.\nPara c.\nPART TWO\n2:i\nPara.\nAfterword\nthanks\n", encoding="utf-8")
        m = build_map(verse_book, "TB", "Test Book")
        if m["scheme"] != "verse": fails.append("verse scheme not detected")
        if [u["address"] for u in m["units"]] != ["TB 1:i", "TB 1:ii", "TB 2:i"]: fails.append(f"units {[u['address'] for u in m['units']]}")
        u1, u2 = m["units"][0], m["units"][1]
        if u1["title"] != "First light" or u1["paragraphs"] != 2: fails.append(f"title/para count {u1}")
        if u2["title"] is not None or u2["paragraphs"] != 3: fails.append(f"quoted opener misread as title {u2}")
        if m["parts"][0]["title"] != "A TITLE": fails.append("part title")
        if m["back_matter"]["line"] != 18: fails.append(f"back matter {m['back_matter']}")
        frag_book = d / "fb.md"
        frag_book.write_text("PART ONE\n1:i\nPART ONE\n1:i\nProse.\n2:i\nProse.\nFRAGMENTS\ni\nFrag one.\nii\nFrag two.\nAfterword\nx\n", encoding="utf-8")
        mf = build_map(frag_book, "FB", None)
        addrs = [u["address"] for u in mf["units"]]
        if addrs != ["FB 1:i", "FB 2:i", "FB F:i", "FB F:ii"]: fails.append(f"fragments units {addrs}")
        if mf["back_matter"]["line"] != 13: fails.append(f"fragments back matter {mf['back_matter']}")
        if resolve(mf, "FB F:ii ¶1", frag_book.read_text(encoding="utf-8").splitlines()) != "Frag two.": fails.append("resolve fragment")
        lines = verse_book.read_text(encoding="utf-8").splitlines()
        if resolve(m, "TB 1:i ¶2", lines) != "Para two.": fails.append("resolve paragraph")
        if resolve(m, "TB 1:ii ¶1", lines) != "'Quoted opener,' she said.": fails.append("resolve first para after no-title")
        if resolve(m, "TB 1:i ¶9", lines) is not None: fails.append("out-of-range paragraph must be None")
        ok, _ = verify(m, verse_book)
        if not ok: fails.append("verify same file")
        verse_book.write_text("changed\n", encoding="utf-8")
        ok, _ = verify(m, verse_book)
        if ok: fails.append("verify must fail on changed file")
        chap_book = d / "cb.md"
        chap_book.write_text("ONE\nPara.\nPara.\nTWO\nPara.\n", encoding="utf-8")
        m2 = build_map(chap_book, "CB", None)
        if m2["scheme"] != "chapter-paragraph" or [u["address"] for u in m2["units"]] != ["CB 1", "CB 2"]:
            fails.append(f"chapter scheme {m2['scheme']} {[u['address'] for u in m2['units']]}")
        plain = d / "pb.md"
        plain.write_text("Just prose.\nMore prose.\n", encoding="utf-8")
        m3 = build_map(plain, "PB", None)
        if m3["scheme"] != "paragraph" or m3["units"][0]["paragraphs"] != 2: fails.append("paragraph scheme")
        write_markdown(m, d / "m.md")
        if "| TB 1:ii |" not in (d / "m.md").read_text(encoding="utf-8"): fails.append("markdown row")
        try:
            parse_address("nonsense")
            fails.append("bad address accepted")
        except ValueError:
            pass
    for f in fails:
        print("FAIL:", f)
    print(f"SELFTEST {'OK' if not fails else 'FAILED'}: {len(fails)} failures")
    return 1 if fails else 0


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("book", nargs="?", help="clean book markdown (one paragraph per line)")
    p.add_argument("--key", help="book key used in addresses, e.g. TEATD1")
    p.add_argument("--title")
    p.add_argument("--out", help="map JSON path (a .md sibling is written too)")
    p.add_argument("--map", help="existing map for --verify / --resolve")
    p.add_argument("--verify", metavar="BOOK", help="check BOOK against the map's pinned edition")
    p.add_argument("--resolve", metavar="ADDRESS", help="print the paragraph at ADDRESS (needs --book)")
    p.add_argument("--book", dest="book_file", help="book file for --resolve")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if a.map and (a.verify or a.resolve):
        m = json.loads(Path(a.map).read_text(encoding="utf-8"))
        if a.verify:
            ok, msg = verify(m, Path(a.verify))
            print(msg)
            sys.exit(0 if ok else 1)
        if not a.book_file:
            p.error("--resolve needs --book")
        ok, msg = verify(m, Path(a.book_file))
        if not ok:
            raise SystemExit(msg)
        text = resolve(m, a.resolve, Path(a.book_file).read_text(encoding="utf-8", errors="replace").splitlines())
        print(text if text is not None else f"NO SUCH ADDRESS: {a.resolve}")
        return
    if not a.book or not a.key:
        p.error("book and --key are required to build a map")
    m = build_map(Path(a.book), a.key, a.title)
    out = Path(a.out) if a.out else Path("reference/addresses") / f"{a.key.lower()}.address.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(m, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    write_markdown(m, out.with_suffix("").with_suffix(".md") if out.suffix == ".json" else out.with_suffix(".md"))
    print(f"WROTE {out}: {m['scheme']}, {m['unit_count']} units, {m['paragraph_count']} paragraphs, "
          f"edition {m['edition']['sha256'][:12]}…")


if __name__ == "__main__":
    main()
