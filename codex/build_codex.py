#!/usr/bin/env python3
"""
build_codex.py — assemble THE PATH ENGINE CODEX, a single-file offline browser
for the reference layer of THE NEW PATH ENGINE.

WHAT THIS IS (and where it sits in the authority order)
-------------------------------------------------------
This is a PRESENTATION tool — the least-authoritative thing in the repo. It
creates no knowledge. It consolidates the already-built, already-committed
reference indices registered in `reference/families.json` into ONE
searchable, self-contained HTML page, and — where it safely can — splices in
each entry's FULL book-verbatim stat block / description so the page is usable WITHOUT opening the sourcebook.

Authority order is unchanged and this view is at the bottom of it:
    Notion (canon) > native 3.5e / GURPS resolver modules > reference layer >
    THIS VIEW (the codex).
Every row keeps its `system` label (D&D 3.5e / GURPS 4e / WH40K Roleplay / WFRP /
WH40K / WHFB / ...) and its book + page citation. Nothing here is native canon.

WHY THE BUILT PAGE IS NOT COMMITTED
-----------------------------------
The output embeds book-verbatim text sliced from the OCR sources on
`I:\\Sourcebooks`. Per the repo law ("the raw text is deliberately NOT copied into
the repository"), the generated files under `codex/build/` are git-ignored. Only
THIS builder and `codex/codex_template.html` are tracked. Rebuild on demand; then
publish `codex/build/engine_reference.html` as a private Artifact.

INPUTS
------
- reference/families.json    canonical registry of 42 family files and their
                              explicit accepted-entry paths
- reference/*_index.json      committed family files (name/fields/citation +
                              [start,end] spans and exact paths where emitted)
- scripts/spells_srd35.json   clean SRD 3.5 spell text (Open Game Content, bundled)
- I:\\Sourcebooks\\_md, _text   the OCR sources, sliced by each row's line span
- codex/codex_template.html   the page shell (contains the __ENGINE_DATA_B64__ slot)

OUTPUT (git-ignored)
--------------------
- codex/build/engine_reference.html   the self-contained page (gzip data, ~8 MB)
- codex/build/engine_data.json        the consolidated dataset (for debugging)

FULL-TEXT SOURCING — book RAW, never invented
---------------------------------------------
- SRD spells        pulled by name from spells_srd35.json (clean OGC text).
- harvested spells  sliced from the exact source_path emitted by spell_harvest.py;
                    the Premium Compendium path remains as a legacy fallback.
- soulmelds          sliced from exact-source full-description spans; PDF table
                    columns interleaved into four blocks are removed first.
- vestiges           sliced from exact-source heading spans; floated stat tablets
                    are removed, and the complete descriptions bypass the 4.2k cap.
- mysteries          sliced from exact Tome of Magic heading-to-heading spans;
                    five verified floating illustration blocks are removed and
                    complete descriptions bypass the 4.2k cap.
- utterances         sliced from exact Tome of Magic detail spans; exact
                    source-verified caption exclusions retain the complete text.
- maneuvers          sliced from canonical exact-source description spans; complete
                    descriptions bypass the 4.2k cap.
- psionic powers    sliced from harvester-owned exact source paths and validated
                    description spans; ambiguous column-interleaved rows stay empty.
- GURPS skills        sliced from exact Basic Set description spans; running page
                    furniture is removed and complete descriptions bypass the cap.
- GURPS traits        sliced from exact Basic Set description/inline-definition
                    spans; shared entries retain their common block, running page
                    furniture is removed, and complete descriptions bypass the cap.
- GURPS techniques    sliced from exact Martial Arts ordered description fragments;
                    unrelated sidebars/quotes and running furniture are excluded.
- epic items         sliced from 103 canonical blocks in the reproducible ELH
                    two-column OCR source; variants deliberately share spans.
- epic monsters      sliced from 50 canonical blocks in the reproducible ELH
                    two-column OCR source; printed variants share spans.
- legacy rows        fuzzy-match a source filename, then slice by [start:end].
- every slice is VALIDATED: the entry name (or a family-specific canonical
  description key) must lead it or the block is dropped.
- wargame profiles  use the harvester-attached book-verbatim SPECIAL RULES block;
  profiles whose book prints no recoverable unit rule section remain honestly empty.

The page itself is gzip-compressed and base64-embedded; the browser inflates it on
load with DecompressionStream. This keeps the full-text page under the 16 MB
Artifact ceiling (~9 MB) instead of ~22 MB raw.

Usage:
    python codex/build_codex.py            # build the page
    python codex/build_codex.py --report   # build + print per-family coverage
"""
from __future__ import annotations

import argparse
import base64
import collections
import glob
import gzip
import json
import os
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REF = REPO / "reference"
MANIFEST = REF / "families.json"
SRD_JSON = REPO / "scripts" / "spells_srd35.json"
TEMPLATE = REPO / "codex" / "codex_template.html"
BUILD = REPO / "codex" / "build"

# The OCR sources live outside the repo, exactly as the harvesters read them.
SOURCE_ROOTS = [
    r"I:\Sourcebooks\_md\_bestiary",
    r"I:\Sourcebooks\_md",
    r"I:\Sourcebooks\_text",
]
# Legacy fallback for spell indices created before spell_harvest.py emitted each
# source's exact relative extraction path.
SPELL_COMPENDIUM_PREMIUM = r"I:\Sourcebooks\_text\D&D 3.5e\Magic and Items\Spell Compendium (Premium).md"

CAP = 4200  # exact vestige/mystery/maneuver/GURPS/epic spans bypass it

_STOP = set("gurps wfrp the of a an core rulebook compilation edition pdf md txt "
            "scan updated with errata hq premium".split())


def _toks(s: str) -> set:
    """Distinctive filename/book tokens for fuzzy book->file matching."""
    s = re.sub(r"\.(pdf|md|txt)$", "", str(s), flags=re.I)
    s = re.sub(r"\([^)]*\)", "", s)
    s = s.replace("\u2014", "-").replace("\u2013", "-")
    s = re.sub(r"\b(3e|4e|2e|1e|5e)\b", "", s.lower())
    return set(w for w in re.findall(r"[a-z0-9]+", s) if w not in _STOP and len(w) > 1)


def _build_file_index():
    idx, seen = [], set()
    for root in SOURCE_ROOTS:
        for f in (glob.glob(os.path.join(root, "**", "*.md"), recursive=True)
                  + glob.glob(os.path.join(root, "**", "*.txt"), recursive=True)):
            if f in seen:
                continue
            seen.add(f)
            idx.append((_toks(os.path.basename(f)), f))
    return idx


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def _validate(seg: str, name: str) -> bool:
    """A slice is trusted only if the entry's name leads it (guards misaligned offsets)."""
    nm = _norm(name)
    head = _norm(seg[:300])
    tk = [t for t in nm.split() if len(t) >= 4] or nm.split()
    return bool(tk) and all(t in head for t in tk[:2])


POWER_RUNNING_HEADER = re.compile(
    r"^(?:CHAPTER\s+\d+|POWERS?(?:,\s+MANTLES)?|AND\s+ITEMS)$",
    re.IGNORECASE,
)


def _strip_power_furniture(seg: str) -> str:
    """Remove repeated page furniture from exact XPH/Complete Psionic spans."""
    source = seg.splitlines()
    out = []
    for i, line in enumerate(source):
        text = line.strip()
        if re.fullmatch(r"## \[PDF page \d+\]", text, re.IGNORECASE):
            continue
        if POWER_RUNNING_HEADER.match(text):
            continue
        if text.isdigit():
            neighbors = [value.strip() for value in source[max(0, i - 2):i + 3]
                         if value.strip() and value.strip() != text]
            if any(POWER_RUNNING_HEADER.match(value) for value in neighbors):
                continue
        if text and all(ord(char) < 32 for char in text):
            continue
        out.append(line)
    return "\n".join(out).strip()


def _strip_soulmeld_summary_tables(seg: str) -> str:
    """Remove summary-table columns interleaved into four born-digital descriptions."""
    src = seg.splitlines()
    out = []
    i = 0
    while i < len(src):
        s = src[i].strip()
        triplet = (s.casefold().rstrip("*† ") == "chakra"
                   and i + 2 < len(src)
                   and src[i + 1].strip().casefold().rstrip("*† ") == "soulmeld"
                   and src[i + 2].strip().casefold().startswith("basic effect"))
        if s.casefold().startswith("table 4") or triplet:
            resume = next((j for j in range(i + 1, len(src))
                           if "[pdf page " in src[j].casefold()), None)
            if resume is not None:
                i = resume
                continue
        out.append(src[i])
        i += 1
    return "\n".join(out).strip()


def _strip_vestige_tablets(seg: str) -> str:
    """Remove floated Tome of Magic stat tablets and their illustration captions."""
    src = seg.splitlines()
    out = []
    i = 0
    while i < len(src):
        text = src[i].strip()
        caption = text.casefold().startswith(("manifestation of ", "seal of "))
        probe = i
        if caption:
            probe = next((j for j in range(i + 1, min(len(src), i + 7))
                          if src[j].strip()), i)
        repeated_name = (probe + 1 < len(src) and src[probe].strip()
                         and src[probe].strip() == src[probe + 1].strip()
                         and src[probe].strip().isupper())
        if repeated_name:
            resume = next((j for j in range(probe + 2, min(len(src), probe + 45))
                           if "[pdf page " in src[j].casefold()), None)
            has_fields = (resume is not None
                          and any("vestige level:" in src[j].casefold()
                                  for j in range(probe + 2, resume)))
            if has_fields:
                i = resume
                continue
        out.append(src[i])
        i += 1
    return "\n".join(out).strip()


_MYSTERY_CAPTION_BLOCKS = (
    (
        "Irrin Coradran",
        "uses umbral body to become",
        "incorporeal before attacking",
        "Illus. by S. Prescott",
    ),
    (
        "By casting consume essence, Thanielle sucks the life out of her foe",
        "Illus. by C. Critchlow",
    ),
    ("Illus. by E. Cox",),
    (
        "Afraid of the dark brings forth a shadowy duplicate",
        "that attacks your enemy's will",
        "Illus. by F. Vohwinkel",
    ),
    (
        "Umbral touch turns Eveneth's hand into a deadly weapon",
        "Illus. by J. Thomas",
    ),
)


def _strip_mystery_captions(seg: str) -> str:
    """Remove five exact, source-verified floating illustration blocks."""
    src = seg.splitlines()
    keys = [_norm(line) for line in src]
    removed = set()
    for block in _MYSTERY_CAPTION_BLOCKS:
        wanted = [_norm(line) for line in block]
        hits = [
            index for index in range(0, len(keys) - len(wanted) + 1)
            if keys[index:index + len(wanted)] == wanted
        ]
        if len(hits) == 1:
            start = hits[0]
            removed.update(range(start, start + len(wanted)))
    return "\n".join(
        line for index, line in enumerate(src) if index not in removed
    ).strip()


def _strip_gurps_skill_furniture(seg: str) -> str:
    """Remove only running page markers from exact Basic Set skill spans."""
    src = seg.splitlines()

    def neighbor(index: int, step: int) -> str:
        for _ in range(3):
            index += step
            if not (0 <= index < len(src)):
                return ""
            text = src[index].strip()
            if text:
                return text
        return ""

    out = []
    for i, line in enumerate(src):
        text = line.strip()
        if re.fullmatch(r"## \[PDF page \d+\]", text, re.IGNORECASE):
            continue
        before, after = neighbor(i, -1), neighbor(i, 1)
        paired_footer = ((text == "SKILLS" and (before.isdigit() or after.isdigit()))
                         or (text.isdigit() and (before == "SKILLS" or after == "SKILLS")))
        if paired_footer:
            continue
        out.append(line)
    return "\n".join(out).strip()


def _strip_gurps_trait_furniture(seg: str) -> str:
    """Remove only running page furniture from exact Basic Set trait spans."""
    src = seg.splitlines()
    running_headers = {
        "ADVANTAGES", "DISADVANTAGES",
        "CREATING A CHARACTER", "CHARACTER CREATION",
    }
    list_headers = {"ADVANTAGE LIST", "DISADVANTAGE LIST"}

    def neighbor(index: int, step: int) -> str:
        for _ in range(3):
            index += step
            if not (0 <= index < len(src)):
                return ""
            text = src[index].strip()
            if text:
                return text
        return ""

    out = []
    for i, line in enumerate(src):
        text = line.strip()
        if re.fullmatch(r"## \[PDF page \d+\]", text, re.IGNORECASE):
            continue
        if text in list_headers:
            continue
        before, after = neighbor(i, -1), neighbor(i, 1)
        paired_footer = (
            (text in running_headers and (before.isdigit() or after.isdigit()))
            or (text.isdigit()
                and (before in running_headers or after in running_headers))
        )
        if paired_footer:
            continue
        out.append(line)
    return "\n".join(out).strip()


def _strip_gurps_technique_furniture(seg: str) -> str:
    """Remove only Martial Arts running furniture and floated art captions."""
    src = seg.splitlines()
    art_captions = {"Sodegarami", "Jian", "Hook Swords", "Shuriken", "Tonfas"}

    def neighbor(index: int, step: int) -> str:
        for _ in range(3):
            index += step
            if not (0 <= index < len(src)):
                return ""
            text = src[index].strip()
            if text:
                return text
        return ""

    out = []
    for i, line in enumerate(src):
        text = line.strip()
        if re.fullmatch(r"## \[PDF page \d+\]", text, re.IGNORECASE):
            continue
        if text in art_captions:
            continue
        before, after = neighbor(i, -1), neighbor(i, 1)
        paired_footer = (
            (text == "TECHNIQUES" and (before.isdigit() or after.isdigit()))
            or (text.isdigit()
                and (before == "TECHNIQUES" or after == "TECHNIQUES"))
        )
        if paired_footer:
            continue
        out.append(line)
    return "\n".join(out).strip()


def _fam_sys(fam: str) -> str:
    """System label for the native families that carry no `system` field."""
    return "GURPS 4e" if fam.startswith("gurps_") and "3e" not in fam else "D&D 3.5e"


SYSTEM_ALIASES = {"dnd35": "D&D 3.5e", "gurps4e": "GURPS 4e"}


def _display_book(value: str) -> str:
    """Turn either a book label or a relative extraction path into a label."""
    leaf = re.split(r"[\\/]", value)[-1]
    return re.sub(r"\.(?:md|txt|pdf)$", "", leaf, flags=re.IGNORECASE).strip()


CONTEXT_KEYS = ("corpus", "source_path", "book", "citation", "system")


def _context(node, inherited):
    """Inherit source metadata along one manifest-selected path."""
    out = dict(inherited)
    if isinstance(node, dict):
        for key in CONTEXT_KEYS:
            value = node.get(key)
            if isinstance(value, str) and value.strip():
                out[key] = value.strip()
    return out


def _materialize_row(node, context):
    row = dict(node)
    if not row.get("book") and context.get("book"):
        row["book"] = _display_book(context["book"])
    if not row.get("citation") and context.get("citation"):
        row["citation"] = context["citation"]
    if not row.get("system") and context.get("system"):
        row["system"] = SYSTEM_ALIASES.get(context["system"], context["system"])
    if context.get("corpus"):
        row["_corpus"] = context["corpus"]
    if context.get("source_path"):
        row["_source_path"] = context["source_path"]
    return row


def _rows_at_path(obj, path):
    """Select accepted rows from one explicit dotted manifest path."""
    tokens = path.split(".") if path else []
    rows = []

    def walk(node, index, inherited):
        context = _context(node, inherited)
        if index == len(tokens):
            if not isinstance(node, dict) or not str(node.get("name", "")).strip():
                raise ValueError(f"{path}: selected value is not a named object")
            rows.append(_materialize_row(node, context))
            return
        if not isinstance(node, dict):
            raise ValueError(f"{path}: cannot read {tokens[index]!r} from non-object")

        token = tokens[index]
        many = token.endswith("[]")
        key = token[:-2] if many else token
        if key not in node:
            raise ValueError(f"{path}: missing key {key!r}")
        child = node[key]
        if many:
            if not isinstance(child, list):
                raise ValueError(f"{path}: {key!r} is not a list")
            for value in child:
                walk(value, index + 1, context)
        elif isinstance(child, list):
            for value in child:
                walk(value, index + 1, context)
        else:
            walk(child, index + 1, context)

    walk(obj, 0, {})
    return rows


def _family_specs():
    """Load the canonical family registry."""
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("families"), list):
        raise ValueError("reference/families.json must be a schema_version 1 registry")
    return data["families"]


def selftest():
    fixture = {
        "source_path": "fixture.md",
        "book": "folder/Fixture Book.md",
        "citation": "Fixture Book p.1",
        "system": "dnd35",
        "entries": [{"name": "Real Entry", "page": 1}],
        "soft": [{"name": "Rejected Fragment", "page": 1}],
    }
    rows = _rows_at_path(fixture, "entries")
    assert [row["name"] for row in rows] == ["Real Entry"]
    assert rows[0]["_source_path"] == "fixture.md"
    assert rows[0]["book"] == "Fixture Book"
    assert rows[0]["citation"] == "Fixture Book p.1"
    assert rows[0]["system"] == "D&D 3.5e"
    assert _display_book("SRD 3.5") == "SRD 3.5"
    power_fixture = ("ZONE OF TRUTH,\nPSIONIC\nTelepathy\n"
                     "## [PDF page 107]\n106\nCHAPTER 4\nPOWERS, MANTLES\nAND ITEMS")
    cleaned_power = _strip_power_furniture(power_fixture)
    assert cleaned_power == "ZONE OF TRUTH,\nPSIONIC\nTelepathy"
    caption_fixture = """ARROW OF DUSK
Actual description prose.
Afraid of the dark brings forth a shadowy duplicate
that attacks your enemy's will
Illus. by F. Vohwinkel"""
    caption_cleaned = _strip_mystery_captions(caption_fixture)
    assert "Actual description prose." in caption_cleaned
    assert "Afraid of the dark" not in caption_cleaned
    assert "Illus. by" not in caption_cleaned
    specs = _family_specs()
    assert len(specs) == 43
    assert sum(spec["expected_count"] for spec in specs) == 18_296
    assert any(spec["id"] == "terms_and_affixes"
               and spec["json"].endswith("terms_and_affixes_index.json")
               for spec in specs)
    print("selftest: manifest path excludes diagnostic siblings")
    print("selftest: source provenance and system aliases inherited")
    print("selftest: psionic page furniture removed from exact spans")
    print("selftest: 43-family registry totals 18,296 rows")
    print("selftest: PASS")


def _exact_source_file(row):
    """Resolve source metadata emitted by a harvester; return None for legacy rows."""
    source_path = row.get("_source_path")
    if not source_path:
        return None
    path = Path(source_path)
    if path.is_absolute():
        return str(path)
    corpus = row.get("_corpus")
    return str(Path(corpus) / path) if corpus else None


def build(report=False):
    fileidx = _build_file_index()
    line_cache = {}

    def lines(fp):
        if fp not in line_cache:
            line_cache[fp] = Path(fp).read_text(encoding="utf-8", errors="replace").splitlines()
        return line_cache[fp]

    file_for_book = {}

    def find_file(book):
        if book in file_for_book:
            return file_for_book[book]
        bt = _toks(book)
        best, bs = None, 0.0
        if bt:
            for ft, fp in fileidx:
                inter = len(bt & ft)
                if not inter:
                    continue
                cov = inter / len(bt)
                score = cov + 0.3 * (inter / len(bt | ft))
                if cov >= 0.8 and score > bs:
                    bs, best = score, fp
        file_for_book[book] = best
        return best

    srd_text = {}
    if SRD_JSON.exists():
        srd = json.loads(SRD_JSON.read_text(encoding="utf-8"))
        srd_text = {k.lower(): (v.get("text") or "") for k, v in srd.items()}

    def slice_full(book, start, end, name, source_file=None, transform=None, limit=CAP):
        if end - start < 2:
            return ""
        fp = source_file or find_file(book)
        if not fp or not Path(fp).exists():
            return ""
        try:
            seg = "\n".join(lines(fp)[start:end]).strip()
            if transform:
                seg = transform(seg)
        except Exception:
            return ""
        if seg and _validate(seg, name):
            cleaned = re.sub(r"\n{3,}", "\n\n", seg)
            return cleaned if limit is None else cleaned[:limit]
        return ""

    def slice_full_spans(book, spans, name, source_file=None,
                         transform=None, limit=CAP):
        if not isinstance(spans, list) or not spans:
            return ""
        fp = source_file or find_file(book)
        if not fp or not Path(fp).exists():
            return ""
        try:
            fragments = []
            source_lines = lines(fp)
            for pair in spans:
                if (not isinstance(pair, list) or len(pair) != 2
                        or not all(isinstance(value, int) for value in pair)):
                    return ""
                start, end = pair
                if not (0 <= start < end <= len(source_lines)):
                    return ""
                fragments.append("\n".join(source_lines[start:end]).strip())
            seg = "\n\n".join(fragments).strip()
            if transform:
                seg = transform(seg)
        except Exception:
            return ""
        if seg and _validate(seg, name):
            cleaned = re.sub(r"\n{3,}", "\n\n", seg)
            return cleaned if limit is None else cleaned[:limit]
        return ""

    def spell_full(r):
        book = r.get("book", "")
        name = r.get("description_key") or r["name"]
        # SRD core spells carry clean bundled text (start==end==0, no line span).
        if (r.get("start", 0) == 0 and r.get("end", 0) == 0) or "srd" in book.lower():
            t = srd_text.get(name.lower().strip())
            return re.sub(r"\n{3,}", "\n\n", t.strip())[:CAP] if t else ""
        # Prefer the exact relative source path emitted by spell_harvest.py. The
        # legacy Compendium fallback preserves compatibility with older indices.
        fp = _exact_source_file(r)
        if not fp and "spell compendium" in book.lower():
            fp = SPELL_COMPENDIUM_PREMIUM
        return slice_full(book, r.get("start", 0), r.get("end", 0), name, fp)

    rows_out = []
    cov = collections.Counter()
    tot = collections.Counter()

    for spec in _family_specs():
        fam = spec["id"]
        f = REPO / spec["json"]
        obj = json.loads(f.read_text(encoding="utf-8"))
        rows = _rows_at_path(obj, spec["entry_path"])
        if len(rows) != spec["expected_count"]:
            raise ValueError(
                f"{fam}: registry expects {spec['expected_count']} rows, found {len(rows)}"
            )
        for r in rows:
            tot[fam] += 1
            if isinstance(r.get("special_rules"), str) and r["special_rules"].strip():
                full = r["special_rules"].strip()
            elif fam == "spell":
                full = spell_full(r)
            elif (fam == "power" and isinstance(r.get("description_start"), int)
                  and isinstance(r.get("description_end"), int)):
                full = slice_full(
                    r.get("book", ""), r["description_start"], r["description_end"],
                    r["name"], _exact_source_file(r), _strip_power_furniture, None,
                )
            elif fam == "power":
                full = ""
            elif fam == "soulmeld" and "start" in r and "end" in r:
                full = slice_full(r.get("book", ""), r["start"], r["end"], r["name"],
                                  _exact_source_file(r), _strip_soulmeld_summary_tables)
            elif fam == "vestige" and "start" in r and "end" in r:
                full = slice_full(r.get("book", ""), r["start"], r["end"], r["name"],
                                  _exact_source_file(r), _strip_vestige_tablets, None)
            elif fam == "mystery" and "start" in r and "end" in r:
                full = slice_full(r.get("book", ""), r["start"], r["end"], r["name"],
                                  _exact_source_file(r),
                                  _strip_mystery_captions, None)
            elif fam == "utterance" and r.get("description_spans"):
                full = slice_full_spans(
                    r.get("book", ""), r["description_spans"], r["name"],
                    _exact_source_file(r), limit=None)
            elif fam == "maneuver" and "start" in r and "end" in r:
                full = slice_full(r.get("book", ""), r["start"], r["end"], r["name"],
                                  _exact_source_file(r), limit=None)
            elif fam == "epic_item" and "start" in r and "end" in r:
                full = slice_full(r.get("book", ""), r["start"], r["end"],
                                  r.get("description_key") or r["name"],
                                  _exact_source_file(r), limit=None)
            elif fam == "epic_monster" and "start" in r and "end" in r:
                full = slice_full(r.get("book", ""), r["start"], r["end"],
                                  r.get("description_key") or r["name"],
                                  _exact_source_file(r), limit=None)
            elif fam == "gurps_technique" and r.get("description_spans"):
                full = slice_full_spans(
                    r.get("book", ""), r["description_spans"],
                    r.get("description_key") or r["name"],
                    _exact_source_file(r), _strip_gurps_technique_furniture, None)
            elif fam == "gurps_trait" and "start" in r and "end" in r:
                full = slice_full(r.get("book", ""), r["start"], r["end"],
                                  r.get("description_key") or r["name"],
                                  _exact_source_file(r), _strip_gurps_trait_furniture, None)
            elif fam == "gurps_skill" and "start" in r and "end" in r:
                full = slice_full(r.get("book", ""), r["start"], r["end"],
                                  r.get("description_key") or r["name"],
                                  _exact_source_file(r), _strip_gurps_skill_furniture, None)
            elif "start" in r and "end" in r:
                full = slice_full(r.get("book", ""), r["start"], r["end"], r["name"],
                                  _exact_source_file(r))
            else:
                full = ""
            if full:
                cov[fam] += 1
            extra = {}
            for k, v in r.items():
                if k in ("name", "system", "book", "page", "citation", "start", "end",
                         "description_key", "description_start", "description_end",
                         "description_spans", "excluded_spans", "special_rules",
                         "table_start", "table_end", "_corpus", "_source_path"):
                    continue
                if isinstance(v, (str, int, float)) and str(v).strip() and str(v) != "None":
                    extra[k] = v
                elif isinstance(v, list) and v:
                    extra[k] = "; ".join(str(x) for x in v)
                elif isinstance(v, dict) and v:
                    extra[k] = " ".join(f"{kk} {vv}" for kk, vv in v.items() if vv not in (None, ""))
            e = {
                "fam": fam,
                "name": r["name"],
                "sys": r.get("system") or _fam_sys(fam),
                "book": r.get("book", "") or "",
                "page": str(r.get("page") or r.get("citation") or ""),
                "f": extra,
            }
            if full:
                e["full"] = full
            rows_out.append(e)

    BUILD.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(rows_out, ensure_ascii=False, separators=(",", ":")).replace("\uFFFD", "?")
    (BUILD / "engine_data.json").write_text(raw, encoding="utf-8")

    b64 = base64.b64encode(gzip.compress(raw.encode("utf-8"), 9)).decode("ascii")
    template = TEMPLATE.read_text(encoding="utf-8")
    if "__ENGINE_DATA_B64__" not in template:
        raise SystemExit("template is missing the __ENGINE_DATA_B64__ slot")
    html = template.replace("__ENGINE_DATA_B64__", b64)
    out = BUILD / "engine_reference.html"
    out.write_text(html, encoding="utf-8")

    with_full = sum(1 for r in rows_out if r.get("full"))
    print(f"codex built: {len(rows_out)} entries, {with_full} with full text "
          f"({100 * with_full // max(len(rows_out), 1)}%)")
    print(f"  {out}  ({out.stat().st_size / 1e6:.2f} MB, limit 16 MB)")
    if out.stat().st_size > 16_000_000:
        print("  WARNING: over the 16 MB Artifact ceiling — lower CAP or trim families")
    if report:
        print("\nper-family full-text coverage:")
        for fam in sorted(tot):
            print(f"  {fam:22} {cov[fam]:5}/{tot[fam]:5}  {100 * cov[fam] // max(tot[fam], 1):3}%")


def main():
    ap = argparse.ArgumentParser(description="Build the Path Engine Codex offline browser.")
    ap.add_argument("--report", action="store_true", help="print per-family full-text coverage")
    ap.add_argument("--selftest", action="store_true", help="run embedded regression checks")
    args = ap.parse_args()
    if args.selftest:
        selftest()
        return
    build(report=args.report)


if __name__ == "__main__":
    main()
