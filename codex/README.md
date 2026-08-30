# The Path Engine Codex — offline reference browser

A downstream **presentation layer** for THE NEW PATH ENGINE reference layer:
`build_codex.py` folds all 42 committed reference families registered in
`reference/families.json` into ONE self-contained, searchable HTML page and —
where it safely can — splices in each entry's **full book-verbatim stat block /
description**, so the page is usable at the
table or on a phone without opening the sourcebook.

## Where it sits in the authority order

This is the **least-authoritative** thing in the repo. It creates no knowledge; it
only re-presents what the reference layer already extracted.

```
Notion (canon)  >  native 3.5e / GURPS resolver modules  >  reference layer  >  THIS VIEW
```

Every row keeps its `system` label — **D&D 3.5e**, **GURPS 4e**, **GURPS 3e**,
**D&D 5e**, **AD&D 2e**, **WFRP**, **WH40K Roleplay**, **WH40K** (wargame),
**WHFB** (wargame) — and its **book + page citation**. Nothing here is native canon,
and the full-text blocks are book-RAW (sliced verbatim, never paraphrased or invented).

## The built page is NOT committed

The output embeds book-verbatim text sliced from the OCR sources on `I:\Sourcebooks`.
Per the repo law — *"the raw text is deliberately NOT copied into the repository"* —
everything under `codex/build/` is git-ignored. Only the **builder** and the
**template** are tracked. Rebuild on demand, then publish the page as a **private**
Artifact.

## Build

```bash
python codex/build_codex.py            # build the page
python codex/build_codex.py --report   # build + per-family full-text coverage
```

Produces (git-ignored):

- `codex/build/engine_reference.html` — the self-contained page (gzip-embedded, ~9 MB)
- `codex/build/engine_data.json` — the consolidated dataset (for debugging)

Then publish `engine_reference.html` as a private claude.ai Artifact and open it from
any browser signed into your account — it runs entirely client-side, so once loaded it
works offline.

## Inputs

| Input | Role |
|---|---|
| `reference/families.json` | canonical registry of all 42 families, their files, explicit accepted-entry paths, systems, and locked counts |
| `reference/*_index.json` | committed family data (rows carry `[start,end]` spans where available; harvesters may also emit an exact relative source path) |
| `scripts/spells_srd35.json` | clean SRD 3.5 spell text (Open Game Content) — the 605 SRD core spells |
| `I:\Sourcebooks\_md`, `_text` | the OCR sources, sliced by each row's line span |
| `codex/codex_template.html` | the page shell (search UI + the `__ENGINE_DATA_B64__` slot) |

## How the full text is sourced (book RAW, validated)

- **SRD spells** — pulled by name from `spells_srd35.json` (clean OGC text, not OCR).
- **Harvested spells** — sliced from the exact `source_path` recorded for each source
  by `spell_harvest.py`; the *Premium* Compendium path remains a legacy fallback.
- **Soulmelds** — sliced from the exact Magic of Incarnum source and their true
  description spans; summary-table columns interleaved by the PDF text layer are
  removed before the name-leading validation.
- **Vestiges** — sliced from the exact Tome of Magic source and their true
  description spans; floated duplicate stat tablets are removed, and complete
  descriptions bypass the normal 4,200-character cap.
- **Utterances** — all 65 truename utterances slice their exact Tome of Magic
  detail blocks; normal/reverse text is retained and complete descriptions
  bypass the normal cap.
- **Maneuvers** — sliced from the exact clean Tome of Battle alternate extraction
  and canonical heading-to-heading spans; complete descriptions bypass the normal
  4,200-character cap.
- **GURPS skills** — all 263 rows slice exact Basic Set Skills-chapter spans;
  grouped definitions and wrapped headings are bounded separately, running page
  furniture is removed, and complete descriptions bypass the normal cap.
- **GURPS traits** — all 469 rows slice exact Basic Set description or inline-
  definition spans on B18–B165; four printed pairs share their common block,
  running page furniture is removed, and complete descriptions bypass the cap.
- **GURPS techniques** — all 112 rows slice 96 exact Martial Arts definition
  groups; multi-column descriptions retain ordered fragments while unrelated
  sidebars, quotations, art captions, and running page furniture are excluded.
- **Epic feats** — 149 exact heading-to-heading spans into the harvester's
  reproducible, raw two-column OCR extraction of ELH pp.50-69. Five descriptions
  dependent on unreadable p.60 remain explicit `NO COVERAGE`.
- **Epic spells** — all 70 seeds and sample spells use exact heading spans into
  the harvester's reproducible raw two-column OCR extraction of ELH pp.74-102.
- **Epic items** — all 153 rows slice 103 verified description blocks from the
  harvester's reproducible raw two-column OCR extraction of ELH pp.126-146;
  numeric/color/slot variants deliberately share the book's common block.
- **Epic monsters** — all 64 rows slice 50 verified shared-section blocks from
  the harvester's reproducible raw two-column OCR extraction of ELH pp.158-230;
  printed variants deliberately share the book's common block.
- **WH40K wargame profiles** — 118 of 136 rows use the book-verbatim SPECIAL
  RULES section attached by the geometric PDF harvester, with a separate rules
  page citation; 18 absent/ambiguous sections remain explicit `NO COVERAGE`.
- **WHFB wargame profiles** — 217 of 291 rows use the book-verbatim SPECIAL
  RULES section attached by same-column geometry, an explicit subject heading,
  or a printed summary Page link validated against the exact unit name; 74
  ambiguous sections remain explicit `NO COVERAGE`.
- **Legacy rows** — fuzzy-match a source filename, then slice by `[start:end]`.
- **Every slice** is validated: the entry name—or its source-verified canonical
  `description_key` where the index label differs—must lead it, or the block is
  dropped. A misaligned or wrong-file slice is never attached.

Source-level book, citation, and system metadata are inherited by child rows;
legacy `dnd35`/`gurps4e` labels are normalized for display. Rejected `soft`
diagnostics are never emitted as cards. The 143 terms/affixes rows are included
with their harvested mechanical glosses, but correctly count as zero full-text
attachments because they do not carry complete description spans. The 110
bundled SRD feats cite their page-less SRD 3.5 source and deliberately leave the
page blank instead of inventing a Player's Handbook page.

Empty WH40K and WHFB rule attachments are named explicitly under each
harvester's `special_rules_no_coverage` list.

## Coverage (as of this build)

**13,347 of 18,159 entries** carry the full verbatim block. Strong: D&D 3.5e
creatures 99% / spells, epic spells, epic items, epic monsters, maneuvers,
soulmelds, vestiges, and utterances 100% / epic feats 97% / feats 86%, GURPS 4e gear,
skills, traits, and techniques 100%, GURPS 3e & 4e creatures/spells 94–100%,
AD&D spells/psionics 100%, WFRP creatures 100%, WH40K wargame profiles 86%,
WHFB wargame profiles 74%, and 40K RP adversaries/talents/psychic ~99–100%.
The 40K RP weapon/gear/armour rows already display their complete harvested
mechanical fields; full prose is not a cheap lift. Across 1,389 rows, the OCR
contains only 850 unique exact description headings (35/145 armour), so the
remaining attachments require source-specific reconstruction and are left
empty rather than guessed.

## The page

Single file: search-as-you-type with relevance ranking, per-system filter chips
(roleplay vs wargame labelled), a per-index dropdown, and an expandable
**"full entry · book verbatim"** block on every card that has one. Theme-aware,
mobile-first, self-contained (the gzip dataset inflates in-browser via
`DecompressionStream`). Re-run `build_codex.py` after any harvest to refresh it.
