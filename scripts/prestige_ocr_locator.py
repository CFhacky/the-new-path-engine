#!/usr/bin/env python3
"""Render scanned prestige-class pages into auditable OCR locator artifacts.

OCR is only a locator/draft. A human or vision reviewer must verify all rules
prose against the rendered page image before it enters the reference index.

By default each page gets two equal-width crops. Scans with offset or three-
column layouts can override normalized edges per page, for example:
  --page-columns 167:0.36,0.66,0.98
  --page-columns 168:0.04,0.34,0.66,0.96
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import shutil
import sys
from collections import defaultdict
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

TESSERACT_CANDIDATES = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    r"C:\Users\Chad\AppData\Local\Programs\Tesseract-OCR\tesseract.exe",
]


def find_tesseract() -> str | None:
    found = shutil.which("tesseract")
    if found:
        return found
    return next((p for p in TESSERACT_CANDIDATES if Path(p).exists()), None)


def parse_pages(spec: str, total: int) -> list[int]:
    pages: list[int] = []
    for item in spec.split(","):
        item = item.strip()
        if not item:
            continue
        if "-" in item:
            first, last = (int(n) for n in item.split("-", 1))
            if first > last:
                raise ValueError(f"descending page range: {item}")
            pages.extend(range(first, last + 1))
        else:
            pages.append(int(item))
    return list(dict.fromkeys(p for p in pages if 1 <= p <= total))


def union(boxes: list[list[float]]) -> list[float]:
    return [
        min(b[0] for b in boxes), min(b[1] for b in boxes),
        max(b[2] for b in boxes), max(b[3] for b in boxes),
    ]


def round_box(box: list[float]) -> list[float]:
    return [round(n, 3) for n in box]


def parse_page_columns(specs: list[str]) -> dict[int, list[float]]:
    result: dict[int, list[float]] = {}
    for spec in specs:
        page_text, edge_text = spec.split(":", 1)
        edges = [float(value) for value in edge_text.split(",")]
        if len(edges) < 3 or len(edges) > 6:
            raise ValueError(f"need 2-5 columns in {spec!r}")
        if edges != sorted(edges) or edges[0] < 0 or edges[-1] > 1:
            raise ValueError(f"column edges must increase within 0..1: {spec!r}")
        if any(a == b for a, b in zip(edges, edges[1:])):
            raise ValueError(f"zero-width column in {spec!r}")
        result[int(page_text)] = edges
    return result


def pdf_box(pixel_box: list[float], scale_x: float, scale_y: float,
            origin_x: float, origin_y: float) -> list[float]:
    x0, y0, x1, y1 = pixel_box
    return round_box([
        origin_x + x0 / scale_x, origin_y + y0 / scale_y,
        origin_x + x1 / scale_x, origin_y + y1 / scale_y,
    ])


def ocr_column(image, page_no: int, column_no: int, page_left: int,
               page_top: int, scale_x: float, scale_y: float,
               origin_x: float, origin_y: float, args, pytesseract) -> dict:
    from PIL import Image
    working = image.convert("L")
    if args.threshold:
        working = working.point(lambda value: 255 if value > args.threshold else 0)
    data = pytesseract.image_to_data(
        working, lang=args.lang, config=f"--psm {args.psm}",
        output_type=pytesseract.Output.DICT)
    tokens: list[dict] = []
    for i, raw in enumerate(data["text"]):
        value = raw.strip()
        confidence = float(data["conf"][i])
        if not value or confidence < args.min_confidence:
            continue
        left, top = int(data["left"][i]), int(data["top"][i])
        right = left + int(data["width"][i])
        bottom = top + int(data["height"][i])
        local = [left, top, right, bottom]
        page = [left + page_left, top + page_top,
                right + page_left, bottom + page_top]
        tokens.append({
            "id": f"p{page_no}-c{column_no}-t{len(tokens) + 1}",
            "page": page_no, "column": column_no, "text": value,
            "confidence": round(confidence, 3),
            "block": int(data["block_num"][i]),
            "paragraph": int(data["par_num"][i]),
            "line": int(data["line_num"][i]),
            "word": int(data["word_num"][i]),
            "column_pixel_bbox": local,
            "page_pixel_bbox": page,
            "pdf_point_bbox": pdf_box(page, scale_x, scale_y, origin_x, origin_y),
        })
    groups: dict[tuple[int, int, int], list[dict]] = defaultdict(list)
    for token in tokens:
        groups[(token["block"], token["paragraph"], token["line"])].append(token)
    lines: list[dict] = []
    for key, members in groups.items():
        local = union([t["column_pixel_bbox"] for t in members])
        page = union([t["page_pixel_bbox"] for t in members])
        lines.append({
            "id": f"p{page_no}-c{column_no}-l{len(lines) + 1}",
            "page": page_no, "column": column_no,
            "block": key[0], "paragraph": key[1], "line": key[2],
            "text": " ".join(t["text"] for t in members),
            "confidence": round(sum(t["confidence"] for t in members) / len(members), 3),
            "token_ids": [t["id"] for t in members],
            "column_pixel_bbox": round_box(local),
            "page_pixel_bbox": round_box(page),
            "pdf_point_bbox": pdf_box(page, scale_x, scale_y, origin_x, origin_y),
        })
    lines.sort(key=lambda row: (row["column_pixel_bbox"][1], row["column_pixel_bbox"][0]))
    return {"tokens": tokens, "lines": lines}


def annotate(image, columns: list[dict], column_local: int | None = None):
    from PIL import ImageDraw
    result = image.copy()
    draw = ImageDraw.Draw(result)
    for column in columns:
        offset_x, offset_y = (column["pixel_bbox"][0], column["pixel_bbox"][1])
        if column_local is None:
            draw.rectangle(column["pixel_bbox"], outline="#00a6ff", width=5)
        for line in column["lines"]:
            box = list(line["page_pixel_bbox"])
            if column_local is not None:
                box = [box[0] - offset_x, box[1] - offset_y,
                       box[2] - offset_x, box[3] - offset_y]
            draw.rectangle(box, outline="#e53935", width=2)
        for token in column["tokens"]:
            box = list(token["page_pixel_bbox"])
            if column_local is not None:
                box = [box[0] - offset_x, box[1] - offset_y,
                       box[2] - offset_x, box[3] - offset_y]
            draw.rectangle(box, outline="#1565c0", width=1)
    return result


def markdown_report(payload: dict) -> str:
    source = payload["source"]
    render = payload["render"]
    out = [
        "# Prestige OCR Locator Report", "",
        "> **Locator/draft only. Vision is the authority.** Verify every rules",
        "> passage against the full-resolution render before accepting it.", "",
        f"- PDF: `{source['name']}`",
        f"- SHA-256: `{source['sha256']}`",
        f"- Render: {render['dpi']} DPI; Tesseract PSM {render['psm']}", "",
    ]
    for page in payload["pages"]:
        out.extend([f"## PDF page {page['page']}", "",
                    f"![Full page]({page['images']['full']})", "",
                    f"![Annotated page]({page['images']['annotated']})", ""])
        for column in page["columns"]:
            out.extend([f"### Column {column['column']}", "",
                        f"![Column {column['column']}]({column['images']['plain']})", "",
                        f"![Annotated column {column['column']}]({column['images']['annotated']})", "",
                        "```text"])
            for line in column["lines"]:
                out.append(f"[{line['id']} conf={line['confidence']:.1f} "
                           f"px={line['page_pixel_bbox']} pdf={line['pdf_point_bbox']}] "
                           f"{line['text']}")
            out.extend(["```", ""])
    return "\n".join(out) + "\n"


def run(args) -> int:
    try:
        import fitz
        import pytesseract
        from PIL import Image
    except ImportError as exc:
        print(f"Missing dependency: {exc}. Need PyMuPDF, Pillow, pytesseract.", file=sys.stderr)
        return 2
    tesseract = find_tesseract()
    if not tesseract:
        print("Tesseract binary not found on PATH or standard Windows paths.", file=sys.stderr)
        return 2
    pytesseract.pytesseract.tesseract_cmd = tesseract
    if not args.pdf.is_file():
        print(f"PDF not found: {args.pdf}", file=sys.stderr)
        return 2
    doc = fitz.open(str(args.pdf))
    try:
        selected = parse_pages(args.pages, doc.page_count)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if not selected:
        print("No valid pages selected.", file=sys.stderr)
        return 2
    try:
        page_columns = parse_page_columns(args.page_columns)
    except (ValueError, TypeError) as exc:
        print(f"Bad --page-columns value: {exc}", file=sys.stderr)
        return 2
    args.out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "warning": "OCR is a locator/draft; vision verification is authoritative.",
        "source": {"path": str(args.pdf.resolve()), "name": args.pdf.name,
                   "sha256": hashlib.sha256(args.pdf.read_bytes()).hexdigest(),
                   "page_count": doc.page_count},
        "render": {"dpi": args.dpi, "psm": args.psm, "lang": args.lang,
                   "threshold": args.threshold, "column_split": args.column_split,
                   "page_column_overrides": page_columns,
                   "min_confidence": args.min_confidence},
        "pages": [],
    }
    matrix = fitz.Matrix(args.dpi / 72.0, args.dpi / 72.0)
    for page_no in selected:
        page = doc[page_no - 1]
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        image = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
        full_name = f"page-{page_no:03d}-full.png"
        annotated_name = f"page-{page_no:03d}-annotated.png"
        image.save(args.out_dir / full_name)
        edges = page_columns.get(page_no, [0.0, args.column_split, 1.0])
        pixel_edges = [max(0, min(image.width, round(image.width * edge)))
                       for edge in edges]
        scale_x, scale_y = image.width / page.rect.width, image.height / page.rect.height
        columns: list[dict] = []
        for number, (left, right) in enumerate(zip(pixel_edges, pixel_edges[1:]), 1):
            box = [left, 0, right, image.height]
            crop = image.crop(tuple(box))
            found = ocr_column(crop, page_no, number, left, 0, scale_x, scale_y,
                               page.rect.x0, page.rect.y0, args, pytesseract)
            plain = f"page-{page_no:03d}-column-{number}.png"
            marked = f"page-{page_no:03d}-column-{number}-annotated.png"
            crop.save(args.out_dir / plain)
            column = {"column": number, "pixel_bbox": box,
                      "pdf_point_bbox": pdf_box(box, scale_x, scale_y,
                                                page.rect.x0, page.rect.y0),
                      "images": {"plain": plain, "annotated": marked}, **found}
            columns.append(column)
            annotate(crop, [column], column_local=number).save(args.out_dir / marked)
        annotate(image, columns).save(args.out_dir / annotated_name)
        payload["pages"].append({
            "page": page_no, "pdf_size_points": [page.rect.width, page.rect.height],
            "pixel_size": [image.width, image.height],
            "images": {"full": full_name, "annotated": annotated_name},
            "columns": columns,
        })
    json_path = args.out_dir / "ocr-locator.json"
    md_path = args.out_dir / "ocr-locator.md"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(markdown_report(payload), encoding="utf-8")
    corpus = " ".join(token["text"] for page in payload["pages"]
                       for column in page["columns"] for token in column["tokens"])
    missing = [probe for probe in args.expect if probe.casefold() not in corpus.casefold()]
    print(f"wrote {len(selected)} page(s), {sum(len(c['tokens']) for p in payload['pages'] for c in p['columns'])} tokens")
    print(json_path)
    print(md_path)
    if missing:
        print("Expected OCR text missing: " + ", ".join(missing), file=sys.stderr)
        return 1
    return 0


def selftest() -> int:
    assert parse_pages("2,4-6,4", 5) == [2, 4, 5]
    assert round_box(union([[1, 2, 3, 4], [0, 3, 7, 9]])) == [0, 2, 7, 9]
    assert pdf_box([100, 200, 300, 400], 2, 4, 10, 20) == [60.0, 70.0, 160.0, 120.0]
    assert parse_page_columns(["167:0.36,0.66,0.98"])[167] == [0.36, 0.66, 0.98]
    print("selftest: PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--pages", help="1-indexed list/ranges, e.g. 167-168")
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--psm", type=int, default=4)
    parser.add_argument("--lang", default="eng")
    parser.add_argument("--threshold", type=int, default=0)
    parser.add_argument("--column-split", type=float, default=0.5)
    parser.add_argument("--page-columns", action="append", default=[],
                        metavar="PAGE:X0,X1,...,XN",
                        help="per-page normalized column edges; repeat as needed")
    parser.add_argument("--min-confidence", type=float, default=0.0)
    parser.add_argument("--expect", action="append", default=[])
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if not args.pdf or not args.pages or not args.out_dir:
        parser.error("--pdf, --pages, and --out-dir are required")
    if not 0.05 < args.column_split < 0.95:
        parser.error("--column-split must be between 0.05 and 0.95")
    if not 72 <= args.dpi <= 600:
        parser.error("--dpi must be between 72 and 600")
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
