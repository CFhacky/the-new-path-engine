# Harvest gaps and no-coverage register

Every gap here is explicit. A missing value remains empty; it is never inferred
from neighboring text, another edition, or campaign canon.

## Citation exceptions

These accepted bundled Open Game Content rows have source citations but no
printed-book page number:

- `NO COVERAGE: printed-book page numbers for 110 bundled SRD 3.5 feats
  (the bundled source is page-less; no Player's Handbook page is inferred).`
- `NO COVERAGE: printed-book page numbers for 605 bundled SRD 3.5 spells
  (the bundled source is page-less; no Player's Handbook page is inferred).`

The exact exception counts are locked in `reference/families.json` and checked
by `scripts/reference_audit.py`.

## Native D&D extraction gaps

- `NO COVERAGE: Player's Handbook II spells.` Both available text layers
  interleave the three-column pages. Explicit-column re-OCR still corrupts
  mechanical characters and mispairs headings with fields.
- `NO COVERAGE: Player's Handbook v3.5 glossary.` The PDF is image-only;
  available multi-flow OCR drops real headings, promotes wrapped formulas to
  false headings, and corrupts mechanical glyphs. Its condition subset already
  belongs to `scripts/conditions.py`.
- `NO COVERAGE: table-first DMG rod/staff entries.` Their charge and spell
  tables precede any prose name anchor. A dedicated table-aware detector is
  required; Rod of Absorption is the representative failure.
- Five Epic Level Handbook feat descriptions dependent on the genuinely blurred
  p.60 image remain empty. Their verified summary mechanics are retained, and
  the harvester locks the exact five-row gap set.

## Wargame source gaps

- WH40K: 18 of 136 profiles have no unambiguous book-verbatim rule attachment.
  Forty-five scanned codexes remain vision-only.
- WHFB: 74 of 302 profiles have no unambiguous rule attachment. High Elves
  PDF p.91 (printed p.92) now has bounded vision coverage (11 unique profiles,
  all with page-verbatim rule lists); every other page of that scan remains
  `NO COVERAGE`. Other scanned books, fan-made books, and one broken-CMap source
  remain excluded.
- The harvesters record these source/profile gaps directly. No special rule is
  inferred merely because a similarly named unit has one elsewhere.

## Codex presentation backlog

These are full-prose attachment gaps, not missing harvested mechanics:

| Family | Full text |
|---|---:|
| AD&D 2e monsters | 0 / 96 |
| D&D 3.5e prestige classes | 0 / 145 |
| terms and affixes | 0 / 143 |
| WFRP mutations | 0 / 505 |
| WH40K Roleplay force fields | 0 / 13 |
| WH40K Roleplay gear | 0 / 587 |
| WFRP gear | 3 / 107 |
| WH40K Roleplay armour | 5 / 145 |
| WH40K Roleplay weapons | 72 / 657 |
| D&D 3.5e powers | 125 / 409 |
| GURPS 3e items | 297 / 783 |
| GURPS 3e spells | 372 / 766 |

The whole Codex is currently 13,293 / 18,105 full-text blocks. Improve these
only by recording and validating true entry spans or by emitting a book-verbatim
`full` field from the owning harvester.

For WH40K Roleplay weapons, gear, and armour, only 850 unique exact OCR
description headings are available across the configured sources, including
only 35 of 145 armour names. Treat further attachment as expensive unless a
better source layer appears.

## Missing-source policy

All configured source paths currently resolve on the sourcebook machine except
where a harvester reports a scan or CMap limitation. A future missing source
must print:

```text
NO COVERAGE — extraction missing: <path>
```

Record the source and reason here in the same commit. Never substitute a
same-title scan without validating its offsets and content.
