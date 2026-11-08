# Epic Level Handbook source recovery

## Investigation, 2026-11-08

Inspected main `b013b2857fbab32de1fd96d366773f209f2e2c0e`, PR #5 and
merged PR #3. The structural audit measures **44 families / 18,352 rows**.
No owned ELH PDF or either missing extraction is mounted on this host.
Desktop Commander reports both laptop registrations and the desktop offline.
An exact-name Drive search returned no ELH PDF or matching extraction.
Neither file appears in the fetched repository history (all fetched branches),
including the unmerged backup-path branch. This does not establish their absence
from offline disks, archives, or untracked working directories.

No full production build was possible here. PR #5's recorded November 2 build
at `0a0af47` measured **14,226 / 18,351** attachments, with **0/70 epic spells**
and **0/64 epic monsters**. The earlier **14,360** attachment count and the
August 29 100% epic measurements are historical. Do not add 134 to the last
build and describe that as a measured current total.

## Original production and provenance

- Spells: commit `9b45727` introduced description extraction;
  `scripts/epic_spell_harvest.py --extract-source` produces 70 blocks
  (46 sample spells + 24 seeds), from PDF pages **74–88 and 92–102**.
- Monsters: commit `cc93002`; `scripts/epic_monster_harvest.py --extract-source`
  produces **50 shared blocks for 64 rows**, from PDF pages **158–230**.
- Both render page index `book_page - 1` at 4× with PyMuPDF; crop each visual
  column separately (even-page x: 8–350–692; odd-page x: 8–285–692;
  y: 55–945); grayscale; Pillow autocontrast cutoff 1; unsharp mask radius 1,
  percent 130, threshold 2; Tesseract `--oem 3 --psm 6` via pytesseract.
  Tokens group by block/paragraph/line, sort by x, and lines by vertical position.
- `DESCRIPTION_ANCHORS`, `_description_body`, and the spell custom lane routes
  in those scripts retain audited cutovers. The monster Hunefer/Lavawight tie
  uses stable OCR row order. Raw body OCR is preserved; only verified headings
  are restored. Do not replace this with generic `pdftotext` or `reocr.py` output.
- `docs/harvest/OCR_REPAIRS.md` and `HISTORY.md` record the August 29 work.
  The indices retain exact half-open, zero-based `[start:end]` spans and hashes.
  The historical PDF byte hash and OCR dependency versions are **not recorded**
  there; identical output on a different OCR environment is not guaranteed.
- Commit `0ae5faa` moved paths to `D:\Backup\I-drive` on
  `origin/claude/festive-cerf-gedf1j`; that commit is not an ancestor of inspected
  main. It changed locations, not the missing text. No provenance-path rewrite
  is needed for recovery.

Both files belong under `<Sourcebooks>\_text\D&D 3.5e\DM Toolkits`:

| File | Required SHA-256 from committed index |
|---|---|
| `Epic Level Handbook.epic-spells.ocr-columns.md` | `97d770a9f1959fd802fe659972718e4cbb444530bdd1798fab202224a9b362ea` |
| `Epic Level Handbook.epic-monsters.ocr-columns.md` | `ef23d96a12ac837d3ecfeab70fb052e6b1f372fec54bb6a05c0abbbc8f3d2f65` |

## 1. Prefer recovery of identical original bytes

Run PowerShell from the corrected engine checkout. Set `$books` to the actual
Sourcebooks directory on the mounted laptop backup; D: below is a documented
location, not a claim that today's external disk has that letter.

```powershell
$books = 'D:\Backup\I-drive\Sourcebooks'
$env:NEW_PATH_SOURCEBOOKS = $books
python scripts/epic_source_check.py --sourcebooks $books
```

If missing, search the original Sourcebooks folder, the T5 backup and any older
sourcebook backup separately. Use actual accessible roots in `$searchRoots`;
do not invent a drive letter or search unrelated private folders.

```powershell
$searchRoots = @($books) # add the actual original/older backup roots here
$names = @('Epic Level Handbook.epic-spells.ocr-columns.md',
           'Epic Level Handbook.epic-monsters.ocr-columns.md')
foreach ($root in $searchRoots) {
  foreach ($name in $names) {
    Get-ChildItem -LiteralPath $root -Filter $name -File -Recurse |
      ForEach-Object { Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256 }
  }
}
```

Copy only hash-matching originals to the expected external `_text` folder,
without changing newlines/encoding. Preserve any conflicting existing file.
Run the checker again. It checks hashes, roster, all committed spans,
page labels, name-leading headings and the 70/50 block counts without writing
reference indices. Exit 0 is required; missing/mismatched input exits 1.

## 2. Regenerate candidates from the owned PDF if originals cannot be found

Use a fresh directory outside the repository. These commands do not regenerate
indices. In particular, **do not run either harvester with no action flag**:
that would replace its committed reference index with newly measured spans.

```powershell
$pdf = Join-Path $books 'D&D 3.5e\DM Toolkits\Epic Level Handbook.pdf'
$tess = 'C:\Program Files\Tesseract-OCR\tesseract.exe'
$candidate = Join-Path $env:TEMP ('elh-recovery-' + [guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $candidate | Out-Null
python -m venv (Join-Path $candidate 'venv')
$py = Join-Path $candidate 'venv\Scripts\python.exe'
& $py -m pip install PyMuPDF Pillow pytesseract
if ($LASTEXITCODE -ne 0) { throw 'OCR dependency installation failed' }
Get-FileHash -LiteralPath $pdf -Algorithm SHA256
& $tess --version
& $py -m pip freeze
# Save these versions, PDF hash, git rev-parse HEAD and console output privately.
& $py scripts/epic_spell_harvest.py --sourcebooks $candidate --pdf $pdf --tesseract $tess --extract-source
if ($LASTEXITCODE -ne 0) { throw 'Epic spell extraction failed' }
& $py scripts/epic_monster_harvest.py --sourcebooks $candidate --pdf $pdf --tesseract $tess --extract-source
if ($LASTEXITCODE -ne 0) { throw 'Epic monster extraction failed' }
& $py scripts/epic_source_check.py --sourcebooks $candidate
if ($LASTEXITCODE -ne 0) { throw 'Candidate is not an exact recovery; retain for review' }
```

On a hash mismatch, stop before installation/building with the candidates.
Keep the original indices and hashes. Recover the original PDF/OCR environment,
rerun and compare, or arrange a separately reviewed source migration: render
all affected page boundaries, compare body text against the PDF, re-detect and
review spans and every changed provenance field. Heading/count success alone
cannot ratify changed body text. Never edit hashes just to make this gate pass.

Only after the checker succeeds, copy the two candidate `.md` files into the
backup's corresponding external `_text` directory. Preserve existing files
before replacement; no source text belongs in git.

## 3. Build and verify measured results

```powershell
$env:NEW_PATH_SOURCEBOOKS = $books
python scripts/epic_source_check.py --sourcebooks $books
if ($LASTEXITCODE -ne 0) { throw 'External epic sources are not verified' }
python scripts/epic_spell_harvest.py --sourcebooks $books --selftest
if ($LASTEXITCODE -ne 0) { throw 'Epic spell selftest failed' }
python scripts/epic_monster_harvest.py --sourcebooks $books --selftest
if ($LASTEXITCODE -ne 0) { throw 'Epic monster selftest failed' }
python scripts/reference_audit.py --build-codex --report
if ($LASTEXITCODE -ne 0) { throw 'Codex build/audit failed' }
python scripts/epic_source_check.py --sourcebooks $books --codex-data codex/build/engine_data.json
if ($LASTEXITCODE -ne 0) { throw 'Codex epic text differs from bounded source slices' }
Get-Content codex/build/coverage.json
Start-Process (Resolve-Path codex/build/engine_reference.html)
git diff --exit-code -- reference
```

Acceptance: source checker and live selftests pass; actual Codex rows match
the current registry; **70/70 spells and 64/64 monsters** attach exactly their
committed, hash-verified bounded source slices. Open the page offline and
exercise both family filters and representative shared monster variants.
Record measured overall totals and commit SHA from this run. `coverage.json`
is build-specific; never report synthetic regression-fixture counts as live
coverage. Existing full-build magic-item acceptance still requires its owned
OCR sources, so an epic-only candidate tree is not a full-build corpus.

No extraction text, PDFs, translator exports, or generated Codex is to be
committed or publicly uploaded. Build output remains ignored; the corrections,
source checks and this recovery procedure contain no new book body text.
