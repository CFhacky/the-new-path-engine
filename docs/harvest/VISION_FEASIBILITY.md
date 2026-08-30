# Wargame scan and CMap feasibility

Verified 2026-08-30 against the PDFs under `I:\Sourcebooks\Warhammer`.
This is mechanics-source analysis only; it contains no campaign canon.

## Explicit backlog inventory

The generated indexes remain the machine-readable inventory:

- `wh40k_wargame_index.json:no_coverage_scanned` lists 45 scanned codexes.
- `whfb_wargame_index.json:no_coverage_scanned` lists 51 scanned sources or
  uncovered page ranges after the bounded pilot.
- `whfb_wargame_index.json:no_coverage_mangled` lists one broken-CMap book:
  `Armybook_4ed - Chaos - 1994`.
- Fan-made/unofficial digital books remain separately excluded and are not
  candidates for official mechanics coverage.

## Extraction measurements

| Source | Pages | PyMuPDF average chars/page | Non-empty text pages | Words on first page | Gate result |
|---|---:|---:|---:|---:|---|
| WHFB 8e High Elves | 96 | 0.0 | 0 | 0 | image-only; digital gate rejects |
| WH40K Space Marines 2004 | 82 | 0.0 | 0 | 0 | image-only; digital gate rejects |
| WHFB 4e Chaos 1994 | 92 | 2,972.0 | 88 | 0 | broken CMap; 2.73% distributed-sample junk-alpha vs 1.5% limit |

The High Elves and Space Marines files contain no word geometry for the existing
parsers to reconstruct. The Chaos file has abundant text but corrupts profile
digits; its junk-alpha rate is roughly eighteen times the clean-book ceiling
noted in the harvester (clean at or below 0.15%). None can safely enter through
the born-digital path.

## Bounded pilot: High Elves roster page

Selected source: `Fantasy\Armybooks\8 ed\Armybook_8ed - High Elves.pdf`.
Selected range: PDF page 91 only, which is printed page 92. The verified
source SHA-256 is `43e54b9b3b52d363708a823287d87fd439c4e0038de3ab20393455f5cb22056b`;
the harvester refuses the hard-coded vision rows if the file hash or 96-page
count changes.

Tesseract at 1.5x was useful only as a locator: it found the roster grid among
PDF pages 85-95 but merged adjacent numeric cells and misread several glyphs.
No OCR value was accepted as mechanics. PDF page 91 was then rendered with
PyMuPDF at 3x (1701 x 2340) and every name, characteristic, troop type, and
SPECIAL RULES list was checked directly against that page image.

Result: 12 printed profile lines, yielding 11 unique `(name, profile)` rows
because `Elven Steed` is printed identically beneath both Silver Helms and
Ellyrian Reavers. All 11 rows carry `system: WHFB`, book plus PDF/printed-page
citations, the verbatim page rule list, and `vision_transcribed: true`.
Every other High Elves page remains `NO COVERAGE`.

## Required workflow for later batches

1. Measure page count, text-page count, average characters, words, and the
   distributed junk-alpha fraction before selecting any page.
2. Use OCR only to locate likely profile pages; never accept OCR values unseen.
3. Render each selected page at 3x or better and verify every accepted cell
   directly against the page image.
4. Bound the batch by one book and an explicit PDF-page range. Record printed
   page numbers separately where they differ.
5. Lock exact row counts and representative complete profiles in `--selftest`.
6. Prove all previously committed rows remain byte-identical, run the repository
   audit, rebuild the Codex, and commit the batch independently.

The next scan batch should extend adjacent High Elves roster pages only if each
page passes the same direct-image verification. The broken-CMap Chaos book must
not be repaired from its text layer; it requires the same page-image workflow.