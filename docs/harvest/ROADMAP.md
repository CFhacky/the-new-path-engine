# Harvest roadmap

This queue is ordered by value, source quality, and the ability to prove the
result without inference. Start only one family unit at a time.

## Completed 2026-08-30: DMG table-first rods and staffs

The magic-item family now includes 34 source-verified table-first rows: 26 rods
and 8 staffs. The additive detector requires both the book's own Table 7-19 or
Table 7-25 row and the matching description heading, locks the old 1,420 rows
unchanged, and raises the family to 1,454 entries.

## Completed 2026-08-30: magic-item exact OCR routing

All 1,454 existing MIC, DMG, and A&EG source spans now route through the exact
OCR path already configured in `item_harvest.py`. This closes a Codex routing
defect rather than performing new extraction or re-OCR. Three source-verified
validation aliases cover the damaged headings `Tusion`, `Ulumination`, and the
split `Headband of Sim-` / `plemindedness`; canonical item names and prose remain
unchanged. Magic-item Codex coverage is 1,454/1,454.

For every remaining Codex-empty family, audit existing OCR, exact source paths,
and recorded spans before scheduling re-OCR or vision work.

## 1. Tome of Magic shadow mysteries — completed 2026-08-30

The native D&D 3.5e `mystery` family now contains all 69 printed shadow-magic
fundamentals and path mysteries from PDF pp.142–154. Each row retains its
category/path, printed level-school and optional per-block fields, exact page,
and heading-to-heading full-description span. The shared chapter casting-time
default was deliberately not imputed into individual rows whose blocks omit it.
Mysteries remain separate from standard spells, vestiges, and utterances.

## 2. Tome of Magic truename utterances — completed 2026-08-30

The separate native D&D 3.5e `utterance` family now contains 65 entries:
43 Evolving Mind, 10 Crafted Tool, and 12 Perfected Map. It preserves the
printed lexicon/level rosters, normal and reversed summaries, duration, save,
resistance, book/page provenance, and exact full-description spans. It remains
independent of both spells and shadow mysteries.

The book does not state a distinct base Truespeak DC for Perfected Map
utterances. That 12-row mechanical gap is explicit rather than inferred.

## 3. Expand native GURPS 4e breadth

In order:

1. **COMPLETE 2026-08-30:** extended `gurps_trait_index` with Control, Create,
   Illusion, Leech, and Static from Powers P90–P98; all 469 Basic Set rows were
   preserved byte-identically, and Basic Set Neutralize was not duplicated;
2. **COMPLETE 2026-08-30:** extended `gurps_gear_index` with GURPS
   Ultra-Tech's Concealable Ballistic Armor Table (p.172 / PDF p.173): exactly
   18 TL9–11 rows with location, split DR, cost, weight, LC, and exact seven-cell
   source spans; all 186 prior Low-Tech rows remain unchanged;
3. add additional bestiary books only where the existing attribute-block
   detector is demonstrably clean.

Each extension must preserve the previous family rows exactly and keep edition
labels separate from the existing GURPS 3e families.

## 4. Improve Codex prose coverage selectively

Prefer cheap, exact-span wins in families with stable headings. Do not chase a
percentage by fuzzy-matching prose to names.

Suggested order:

1. **COMPLETE 2026-08-30:** D&D 3.5e powers now carry 406/409 validated
   description spans; the three column-interleaved XPH rows remain explicit
   `NO COVERAGE`;
2. **IN PROGRESS 2026-08-30:** prestige-class full text now has 23/145 exact,
   visually verified spans. Continue OCR-first from each row's manifest-routed
   individual Dragon issue; use the compiled PDF only for visual verification.
   Knight of the Chase and Master of the Secret Sound remain explicit #297
   OCR gaps until their actual article source is located;
3. AD&D 2e monster descriptions where page-image transcription is already
   available;
4. GURPS 3e items and spells;
5. WFRP mutations and gear.

WH40K Roleplay gear/armour/weapon prose remains low priority until a better text
layer appears. Existing mechanical rows are already useful and complete enough
for lookup.

## 5. Reserve vision work for explicit batches

Treat scanned wargame books, the broken-CMap WHFB book, and the PHB II
three-column spell pages as separate vision projects. Define a bounded book and
page range before starting, preserve image/page provenance, and commit each
verified batch independently.

The first pilot is complete: WHFB High Elves 8th edition, PDF p.91 (printed
p.92), rendered at 3x and checked directly against the source image. It yielded
11 unique profiles and cited rule lists from 12 printed profile lines while all
other pages stayed explicit `NO COVERAGE`. Continue scan work only through the
same gate: measure the text layer, locate with OCR, render at 3x or better,
transcribe against the image, lock exact rows in `--selftest`, and prove every
previous row survives byte-identically.

Dragon Magazine should begin with a read-only feasibility spike for a
crunch-only detector. Do not create an index until precision can be measured
against a representative issue sample.

## Git operating model

- `main` is always a verified, releasable reference state.
- Use short branches named `harvest/<family-or-book>` or `repo/<unit>`.
- Commit one family or one repository-maintenance unit at a time.
- Push immediately after the selftest, audit, independent JSON scan, and Codex
  rebuild pass.
- Tag meaningful whole-reference checkpoints as `reference-YYYY-MM-DD`;
  append `-2`, `-3`, and so on for multiple checkpoints in one day.
- Open a pull request only when Chad asks for review; otherwise use a verified
  fast-forward.
- Keep generated indexes in Git. Do not use LFS for the current repository.
- Never commit sourcebooks, extracted book prose, or `codex/build/`.

## Deliberately deferred reorganization

Do not split this into multiple repositories. Runtime tools, harvesters,
versioned indices, and the Codex share one authority boundary and one audit
surface. Also do not move all harvesters into nested directories yet: the move
would churn dozens of documented commands and generated-by paths without
improving extraction quality. Revisit physical script grouping only when a
specific tooling need outweighs that migration cost.
