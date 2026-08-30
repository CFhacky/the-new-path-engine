# Harvest roadmap

This queue is ordered by value, source quality, and the ability to prove the
result without inference. Start only one family unit at a time.

## Completed 2026-08-30: DMG table-first rods and staffs

The magic-item family now includes 34 source-verified table-first rows: 26 rods
and 8 staffs. The additive detector requires both the book's own Table 7-19 or
Table 7-25 row and the matching description heading, locks the old 1,420 rows
unchanged, and raises the family to 1,454 entries.

## 1. Add Tome of Magic shadow mysteries

Create a native D&D 3.5e `mystery` family for the book's shadow-magic
fundamentals and mysteries. Use the born-digital body blocks already proven
usable by the vestige harvester.
Required fields should come from the printed block only: name, path/category,
level, school/descriptors where printed, casting time, range, target/area,
duration, save, resistance, book, page, and exact full-description span.
Do not force mysteries into the standard spell family.

Ship the harvester, JSON, Markdown, manifest row, docs row, `--selftest`, and
Codex registration as one family commit. Deliberately update the locked
repository family/row totals.

## 2. Add Tome of Magic truename utterances

Create a separate native D&D 3.5e `utterance` family. Keep lexicon, level,
Truespeak DC mechanics, normal/reversed effect, duration, save, resistance,
book, page, and full-description span distinct from mysteries and spells.

Do this after mysteries so the shared source-block lessons are known, while
keeping the mechanics and tests independently reviewable.

## 3. Expand native GURPS 4e breadth

In order:

1. **COMPLETE 2026-08-30:** extended `gurps_trait_index` with Control, Create,
   Illusion, Leech, and Static from Powers P90–P98; all 469 Basic Set rows were
   preserved byte-identically, and Basic Set Neutralize was not duplicated;
2. extend `gurps_gear_index` with one coherent higher-TL equipment table.
   Recommended first unit: GURPS Ultra-Tech's Concealable Ballistic Armor Table
   (p. 172 / PDF p. 173), a clean fixed-width roster of 18 TL9–11 armor rows;
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
2. prestige-class requirement/description blocks;
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
