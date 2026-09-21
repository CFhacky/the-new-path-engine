#!/usr/bin/env python3
"""notion_novel_bind.py -- clean a Notion page dump into markdown and bind an EPUB.

Corpus tooling, not a harvester and not a resolver. It turns the raw text a
Notion "fetch" returns for a long-form page (a novel stored in the Horus
Heresy Source Library) into (a) a clean markdown file and (b) an EPUB 3
container built with the standard library only. Nothing is summarised,
reflowed or invented: the body text passes through untouched apart from the
Notion wrapper, embedded image links and the duplicated contents list.

The novels themselves are never committed to this repository. Run this in a
scratch folder and file the outputs in the sourcebook corpus
(I:\\Sourcebooks\\_text\\...), where the harvesters expect them.

INPUT SHAPE (what the Notion MCP fetch returns for a page)
    Here is the result of "fetch" ...            <- preamble line
    <page url="...">                             <- wrapper
      <ancestor-path>...</ancestor-path>
      <properties>{"title":"..."}</properties>
      <content>
        ...front matter, CONTENTS list, PART headings, "9:xxi" verse
        headings, prose, ![](image) lines, back matter...
      </content>
    </page>

USAGE
    python notion_novel_bind.py DUMP.txt --md OUT.md --epub OUT.epub [--title T] [--author A]
    python notion_novel_bind.py --selftest
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import tempfile
import uuid
import zipfile
from pathlib import Path
from typing import List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verse_address import is_verse_title  # deliberate shared logic: EPUB anchors must match address maps

IMAGE = re.compile(r"^\s*!\[[^\]]*\]\([^)]*\)\s*$")
PART = re.compile(r"^\s*\**(?:PART [A-Z]+|FRAGMENTS)\**\s*$")
BARE_ROMAN = re.compile(r"^\s*\**([ivxl]{1,7})\**\s*$")
VERSE = re.compile(r"^\s*\**(\d{1,2}):([ivxl]{1,7})\**\s*$", re.IGNORECASE)


def extract_title(raw: str) -> Optional[str]:
    m = re.search(r"<properties>\s*(\{.*?\})\s*</properties>", raw, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1)).get("title")
    except json.JSONDecodeError:
        return None


def clean(raw: str) -> Tuple[List[str], int]:
    """Return (body lines, images stripped). The body is everything between the
    outermost <content> tags with image embeds removed."""
    start = raw.find("<content>")
    end = raw.rfind("</content>")
    if start == -1 or end == -1:
        body = raw
    else:
        body = raw[start + len("<content>"):end]
    lines = []
    stripped = 0
    for line in body.splitlines():
        if IMAGE.match(line):
            stripped += 1
            continue
        lines.append(line.rstrip())
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines, stripped


def body_start(lines: List[str]) -> int:
    """The front matter carries a CONTENTS list that repeats every PART and
    verse heading. The body begins at the second occurrence of the first PART
    heading; if there is only one, the body begins at that one."""
    first = None
    for i, line in enumerate(lines):
        if PART.match(line):
            if first is None:
                first = line.strip()
                first_at = i
            elif line.strip() == first:
                return i
    return first_at if first is not None else 0


def split_chapters(lines: List[str]) -> List[Tuple[str, List[str]]]:
    """Front matter, one chapter per PART, then back matter after the last
    verse's prose runs out (the first non-verse heading block is kept inside
    the final part; a trailing licence is left where it lies)."""
    start = body_start(lines)
    chapters: List[Tuple[str, List[str]]] = []
    if start > 0:
        chapters.append(("Front matter", lines[:start]))
    current_title = None
    current: List[str] = []
    for line in lines[start:]:
        if PART.match(line):
            if current_title is not None:
                chapters.append((current_title, current))
            current_title = line.strip().strip("*")
            current = []
            continue
        current.append(line)
    if current_title is not None:
        chapters.append((current_title, current))
    return chapters


def to_xhtml(title: str, lines: List[str]) -> str:
    """One source line is one paragraph (the Notion export carries no blank
    lines). Verse headings become <h2 id="v-CH-VERSE">, a following title
    line becomes <h3>, and every paragraph carries id="v-CH-VERSE-pN" so
    an address such as "TEATD1 4:xviii ¶3" is a link target."""
    out = [f"<h1>{html.escape(title)}</h1>"]
    anchor = None
    pcount = 0
    expect_title = False
    fragments = title.strip().upper() == "FRAGMENTS"
    for line in lines:
        s = line.strip()
        if not s:
            continue
        m = VERSE.match(s)
        if m:
            anchor = f"v-{m.group(1)}-{m.group(2).lower()}"
            pcount = 0
            expect_title = True
            out.append(f"<h2 id='{anchor}'>{m.group(1)}:{m.group(2).lower()}</h2>")
            continue
        if fragments and BARE_ROMAN.match(s):
            anchor = f"v-F-{BARE_ROMAN.match(s).group(1).lower()}"
            pcount = 0
            expect_title = True
            out.append(f"<h2 id='{anchor}'>F:{BARE_ROMAN.match(s).group(1).lower()}</h2>")
            continue
        if expect_title and is_verse_title(s):
            out.append(f"<h3 class='verse-title'>{html.escape(s.strip('*'))}</h3>")
            expect_title = False
            continue
        expect_title = False
        if s.startswith("**") and s.endswith("**") and len(s) > 4:
            out.append(f"<h3>{html.escape(s.strip('*'))}</h3>")
            continue
        text = s.strip("*") if s.startswith("*") and s.endswith("*") else s
        pcount += 1
        pid = f" id='{anchor}-p{pcount}'" if anchor else ""
        out.append(f"<p{pid}>{html.escape(text)}</p>")
    return ("<?xml version='1.0' encoding='utf-8'?>\n"
            "<html xmlns='http://www.w3.org/1999/xhtml' xmlns:epub='http://www.idpf.org/2007/ops'>"
            f"<head><title>{html.escape(title)}</title>"
            "<style>body{font-family:serif;line-height:1.45}h2{font-variant:small-caps}h3.verse-title{font-style:italic;font-weight:normal}</style></head>"
            "<body>" + "\n".join(out) + "</body></html>\n")


def build_epub(chapters: List[Tuple[str, List[str]]], title: str, author: str, out: Path) -> None:
    book_id = f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, title)}"
    manifest = []
    spine = []
    nav_items = []
    files = []
    for i, (ctitle, lines) in enumerate(chapters, 1):
        name = f"ch{i:02d}.xhtml"
        files.append((name, to_xhtml(ctitle, lines)))
        manifest.append(f"<item id='c{i}' href='{name}' media-type='application/xhtml+xml'/>")
        spine.append(f"<itemref idref='c{i}'/>")
        nav_items.append(f"<li><a href='{name}'>{html.escape(ctitle)}</a></li>")
    nav = ("<?xml version='1.0' encoding='utf-8'?>\n"
           "<html xmlns='http://www.w3.org/1999/xhtml' xmlns:epub='http://www.idpf.org/2007/ops'>"
           "<head><title>Contents</title></head><body><nav epub:type='toc'><h1>Contents</h1><ol>"
           + "".join(nav_items) + "</ol></nav></body></html>\n")
    opf = ("<?xml version='1.0' encoding='utf-8'?>\n"
           "<package xmlns='http://www.idpf.org/2007/opf' version='3.0' unique-identifier='bookid'>"
           "<metadata xmlns:dc='http://purl.org/dc/elements/1.1/'>"
           f"<dc:identifier id='bookid'>{book_id}</dc:identifier>"
           f"<dc:title>{html.escape(title)}</dc:title><dc:creator>{html.escape(author)}</dc:creator>"
           "<dc:language>en</dc:language>"
           "<meta property='dcterms:modified'>2026-09-21T00:00:00Z</meta></metadata>"
           "<manifest><item id='nav' href='nav.xhtml' media-type='application/xhtml+xml' properties='nav'/>"
           + "".join(manifest) + "</manifest><spine>" + "".join(spine) + "</spine></package>\n")
    container = ("<?xml version='1.0' encoding='utf-8'?>\n"
                 "<container version='1.0' xmlns='urn:oasis:names:tc:opendocument:xmlns:container'>"
                 "<rootfiles><rootfile full-path='OEBPS/content.opf' media-type='application/oebps-package+xml'/>"
                 "</rootfiles></container>\n")
    with zipfile.ZipFile(out, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav, compress_type=zipfile.ZIP_DEFLATED)
        for name, xhtml in files:
            z.writestr(f"OEBPS/{name}", xhtml, compress_type=zipfile.ZIP_DEFLATED)


def run(dump: Path, md: Optional[Path], epub: Optional[Path], title: Optional[str], author: str) -> dict:
    raw = dump.read_text(encoding="utf-8", errors="replace")
    title = title or extract_title(raw) or dump.stem
    lines, stripped = clean(raw)
    report = {"title": title, "lines": len(lines), "chars": sum(len(l) + 1 for l in lines),
              "images_stripped": stripped}
    if md:
        md.write_text("\n".join(lines) + "\n", encoding="utf-8")
        report["md"] = str(md)
    if epub:
        chapters = split_chapters(lines)
        build_epub(chapters, title, author, epub)
        report["epub"] = str(epub)
        report["chapters"] = [c[0] for c in chapters]
    return report


def selftest() -> int:
    fails: List[str] = []
    sample = ("Here is the result of \"fetch\" for the Page ...\n<page url='x'>\n<properties>\n"
              "{\"title\":\"Test Novel Volume I\"}\n</properties>\n<content>\n"
              "**CONTENTS**\nPART ONE\n1:i\n1:ii\nPART TWO\n2:i\n"
              "PART ONE\n1:i\n![](https://example/img.png)\nFirst verse prose.\n\n1:ii\nSecond verse prose.\n"
              "PART TWO\n2:i\nThird verse prose with ‘curly’ quotes & ampersand.\n"
              "Afterword\nlicence text\n</content>\n</page>\n")
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        dump = d / "dump.txt"
        dump.write_text(sample, encoding="utf-8")
        rep = run(dump, d / "out.md", d / "out.epub", None, "Tester")
        if rep["title"] != "Test Novel Volume I":
            fails.append(f"title: {rep['title']}")
        if rep["images_stripped"] != 1:
            fails.append("image not stripped")
        text = (d / "out.md").read_text(encoding="utf-8")
        if "<content>" in text or "![](" in text or "Here is the result" in text:
            fails.append("wrapper leaked into markdown")
        if "Third verse prose with ‘curly’ quotes & ampersand." not in text:
            fails.append("prose altered")
        if rep["chapters"] != ["Front matter", "PART ONE", "PART TWO"]:
            fails.append(f"chapters: {rep['chapters']}")
        with zipfile.ZipFile(d / "out.epub") as z:
            names = z.namelist()
            if names[0] != "mimetype" or z.getinfo("mimetype").compress_type != zipfile.ZIP_STORED:
                fails.append("mimetype must be first and stored")
            ch = z.read("OEBPS/ch03.xhtml").decode("utf-8")
            if "<h2 id='v-2-i'>2:i</h2>" not in ch or "&amp; ampersand" not in ch:
                fails.append("xhtml headings or escaping wrong")
            if "<p id='v-2-i-p1'>Third verse" not in ch:
                fails.append("paragraph anchor id missing")
            ch2 = z.read("OEBPS/ch02.xhtml").decode("utf-8")
            if "<p id='v-1-i-p1'>First verse prose.</p>" not in ch2 or "<p id='v-1-ii-p1'>Second verse prose.</p>" not in ch2:
                fails.append("per-line paragraphs / anchors wrong")
            import xml.etree.ElementTree as ET
            for n in names:
                if n.endswith((".xhtml", ".opf", ".xml")):
                    ET.fromstring(z.read(n))
    for f in fails:
        print("FAIL:", f)
    print(f"SELFTEST {'OK' if not fails else 'FAILED'}: {len(fails)} failures")
    return 1 if fails else 0


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("dump", nargs="?", help="raw Notion fetch dump (text)")
    p.add_argument("--md", help="clean markdown output path")
    p.add_argument("--epub", help="EPUB output path")
    p.add_argument("--title")
    p.add_argument("--author", default="Dan Abnett")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.dump:
        p.error("dump path required")
    rep = run(Path(a.dump), Path(a.md) if a.md else None, Path(a.epub) if a.epub else None, a.title, a.author)
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
