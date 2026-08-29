#!/usr/bin/env python3
"""
build_codex.py — assemble THE PATH ENGINE CODEX, a single-file offline browser
for the reference layer of THE NEW PATH ENGINE.

WHAT THIS IS (and where it sits in the authority order)
-------------------------------------------------------
This is a PRESENTATION tool — the least-authoritative thing in the repo. It
creates no knowledge. It consolidates the already-built, already-committed
reference indices (`reference/*_index.json`) into ONE searchable, self-contained
HTML page, and — where it safely can — splices in each entry's FULL book-verbatim
stat block / description so the page is usable WITHOUT opening the sourcebook.

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
- reference/*_index.json      the 40+ committed index families (name/fields/citation
                              + a [start,end] LINE span and, where emitted, the exact
                              relative extraction path for each source)
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
- maneuvers          sliced from canonical exact-source description spans; complete
                    descriptions bypass the 4.2k cap.
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
Artifact ceiling (~8 MB) instead of ~22 MB raw.

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

CAP = 4200  # exact vestige/maneuver/GURPS skill/trait/epic spans bypass it

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


def _index_rows(obj, out, context=None):
    """Collect rows while retaining an index source's exact extraction path."""
    context = context or {}
    if isinstance(obj, dict):
        updates = {}
        if isinstance(obj.get("corpus"), str) and obj["corpus"].strip():
            updates["corpus"] = obj["corpus"]
        if isinstance(obj.get("source_path"), str) and obj["source_path"].strip():
            updates["source_path"] = obj["source_path"]
        child_context = {**context, **updates} if updates else context
        if (isinstance(obj.get("name"), str) and obj["name"].strip()
                and any(k in obj for k in ("book", "citation", "page", "system"))):
            row = dict(obj)
            if "corpus" in child_context:
                row["_corpus"] = child_context["corpus"]
            if "source_path" in child_context:
                row["_source_path"] = child_context["source_path"]
            out.append(row)
        for key, value in obj.items():
            # Harvester `soft` arrays are rejected diagnostics, never index rows.
            if key == "soft":
                continue
            _index_rows(value, out, child_context)
    elif isinstance(obj, list):
        for v in obj:
            _index_rows(v, out, context)


def selftest():
    fixture = {
        "source_path": "fixture.md",
        "entries": [{"name": "Real Entry", "book": "Fixture Book"}],
        "soft": [{"name": "Rejected Fragment", "book": "Fixture Book"}],
    }
    rows = []
    _index_rows(fixture, rows)
    assert [row["name"] for row in rows] == ["Real Entry"]
    assert rows[0]["_source_path"] == "fixture.md"
    print("selftest: diagnostic soft rows excluded")
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

    for f in sorted(glob.glob(str(REF / "*_index.json"))):
        fam = os.path.basename(f).replace("_index.json", "")
        rows = []
        _index_rows(json.loads(Path(f).read_text(encoding="utf-8")), rows)
        for r in rows:
            tot[fam] += 1
            if isinstance(r.get("special_rules"), str) and r["special_rules"].strip():
                full = r["special_rules"].strip()
            elif fam == "spell":
                full = spell_full(r)
            elif fam == "soulmeld" and "start" in r and "end" in r:
                full = slice_full(r.get("book", ""), r["start"], r["end"], r["name"],
                                  _exact_source_file(r), _strip_soulmeld_summary_tables)
            elif fam == "vestige" and "start" in r and "end" in r:
                full = slice_full(r.get("book", ""), r["start"], r["end"], r["name"],
                                  _exact_source_file(r), _strip_vestige_tablets, None)
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
                         "description_key", "description_spans", "special_rules",
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
