#!/usr/bin/env python3
"""reocr.py — re-OCR a PDF into clean text, replacing a corrupt OCR extraction.

WHY: some `.md` extractions on I:\\Sourcebooks are corrupt OCR (dropped leading
characters, Cyrillic bleed, and — in the AD&D Monstrous Compendium — a two-column
stat block whose value cells are scrambled out of order). The source PDFs are
fine. This tool renders the PDF pages with PyMuPDF and re-OCRs the images with
Tesseract, which reads in visual order (fixing the column scramble) and, on a
PLAIN layout, is far cleaner than the original pass.

    python scripts/reocr.py --pdf "book.pdf" --pages 7,9,31-36 --out clean.md
    python scripts/reocr.py --pdf "book.pdf" --pages 46-49            # to stdout

LIMITS (measured, 2026-08-28). This helps PLAIN scans (e.g. the AD&D 2e
Monstrous Compendium stat blocks — clean values, correct order). It does NOT fix
ORNATE fantasy pages with decorative/colored text on textured parchment (e.g. the
Epic Level Handbook): Tesseract still garbles the stylised headers and coloured
columns there, so those need vision transcription instead (render the page,
read it by eye — see docs/HARVEST_PROGRESS.md). Tesseract also makes character
slips that matter for mechanics ("3+3" -> "343", "Very" -> "Verv"), so numbers
read out of a re-OCR still want a spot-check against the image.

REQUIREMENTS: PyMuPDF (`fitz`), Pillow, pytesseract, and the Tesseract binary
(auto-detected on PATH or the usual Windows install dir). No network.
"""
from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path
from typing import List, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

_TESS_CANDIDATES = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    r"C:\Users\Chad\AppData\Local\Programs\Tesseract-OCR\tesseract.exe",
]


def _find_tesseract() -> Optional[str]:
    import shutil
    onpath = shutil.which("tesseract")
    if onpath:
        return onpath
    for c in _TESS_CANDIDATES:
        if Path(c).exists():
            return c
    return None


def parse_pages(spec: str, total: int) -> List[int]:
    """'7,9,31-36' -> [7,9,31,32,33,34,35,36] (1-indexed, clamped to the book)."""
    out: List[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return [p for p in out if 1 <= p <= total]


def reocr_page(doc, page_no: int, dpi_scale: float, threshold: int, psm: int, lang: str) -> str:
    import fitz  # noqa: F401  (doc already open)
    import pytesseract
    from PIL import Image
    pix = doc[page_no - 1].get_pixmap(matrix=__import__("fitz").Matrix(dpi_scale, dpi_scale))
    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")
    if threshold > 0:
        img = img.point(lambda p: 255 if p > threshold else 0)
    return pytesseract.image_to_string(img, lang=lang, config=f"--psm {psm}").rstrip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--pdf", required=True, type=Path)
    ap.add_argument("--pages", help="e.g. 7,9,31-36 (1-indexed). Default: all.")
    ap.add_argument("--out", type=Path, help="write Markdown here; default stdout")
    ap.add_argument("--dpi-scale", type=float, default=3.2, help="render scale (≈300+ DPI)")
    ap.add_argument("--threshold", type=int, default=165,
                    help="binarize cutoff 0-255; 0 disables (default 165)")
    ap.add_argument("--psm", type=int, default=4, help="Tesseract page-seg mode (default 4)")
    ap.add_argument("--lang", default="eng")
    args = ap.parse_args()

    tess = _find_tesseract()
    if not tess:
        print("Tesseract binary not found (PATH or the usual Windows install dir). "
              "Install it or add it to PATH.", file=sys.stderr)
        return 2
    try:
        import fitz
        import pytesseract
        pytesseract.pytesseract.tesseract_cmd = tess
    except ImportError as e:
        print(f"Missing dependency: {e}. Need PyMuPDF, Pillow, pytesseract.", file=sys.stderr)
        return 2

    if not args.pdf.exists():
        print(f"PDF not found: {args.pdf}", file=sys.stderr)
        return 2

    doc = fitz.open(str(args.pdf))
    pages = parse_pages(args.pages, doc.page_count) if args.pages else list(range(1, doc.page_count + 1))
    if not pages:
        print("No pages selected.", file=sys.stderr)
        return 1

    chunks: List[str] = [
        f"<!-- re-OCR of {args.pdf.name} via reocr.py "
        f"(Tesseract {pytesseract.get_tesseract_version()}, "
        f"psm {args.psm}, threshold {args.threshold}). "
        f"PLAIN-layout pages only; verify numbers against the image. -->"
    ]
    for p in pages:
        text = reocr_page(doc, p, args.dpi_scale, args.threshold, args.psm, args.lang)
        chunks.append(f"\n<!-- PDF page {p} -->\n{text}")
        if not args.out:
            print(f"\n===== PDF page {p} =====")
            print(text)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text("\n".join(chunks) + "\n", encoding="utf-8")
        print(f"wrote {args.out} ({len(pages)} page(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
