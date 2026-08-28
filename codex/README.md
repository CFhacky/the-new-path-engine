# The Path Engine Codex — offline reference browser

A downstream **presentation layer** for THE NEW PATH ENGINE reference layer:
`build_codex.py` folds the 40+ committed `reference/*_index.json` families into ONE
self-contained, searchable HTML page and — where it safely can — splices in each
entry's **full book-verbatim stat block / description**, so the page is usable at the
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

- `codex/build/engine_reference.html` — the self-contained page (gzip-embedded, ~8 MB)
- `codex/build/engine_data.json` — the consolidated dataset (for debugging)

Then publish `engine_reference.html` as a private claude.ai Artifact and open it from
any browser signed into your account — it runs entirely client-side, so once loaded it
works offline.

## Inputs

| Input | Role |
|---|---|
| `reference/*_index.json` | the committed index families (each row carries a `[start,end]` LINE span into its source) |
| `scripts/spells_srd35.json` | clean SRD 3.5 spell text (Open Game Content) — the 605 SRD core spells |
| `I:\Sourcebooks\_md`, `_text` | the OCR sources, sliced by each row's line span |
| `codex/codex_template.html` | the page shell (search UI + the `__ENGINE_DATA_B64__` slot) |

## How the full text is sourced (book RAW, validated)

- **SRD spells** — pulled by name from `spells_srd35.json` (clean OGC text, not OCR).
- **Spell Compendium** — sliced from the *Premium* scan (the scan the spell harvest
  indexed; the "alt scan" has different offsets and must not be used).
- **Everything else** — sliced from its source file by the row's `[start:end]` line
  span, then **validated**: the entry's name must lead the slice, or the block is
  dropped. A misaligned slice is never attached.

Families that legitimately carry **no** full block: the two **wargame** indices
(a unit's profile line *is* the whole entry; its special rules live elsewhere in the
army book) and a few families whose harvesters recorded only a marker offset
(soulmelds, vestiges, epic-tier). That is honest emptiness, not a bug.

## Coverage (as of this build)

**11,036 of 17,911 entries** carry the full verbatim block. Strong: D&D 3.5e
creatures 99% / spells 93% / feats 86%, GURPS 3e & 4e creatures and spells 94–100%,
AD&D 100%, WFRP creatures 100%, 40K RP adversaries/talents/psychic ~99–100%. Known
low families (need harvester-level work to lift): Complete Champion / Dragon Magic
spells, several GURPS gear/skill/trait indices, epic-tier, and the 40K RP
weapon/gear tables (which already display their mechanical fields).

## The page

Single file: search-as-you-type with relevance ranking, per-system filter chips
(roleplay vs wargame labelled), a per-index dropdown, and an expandable
**"full entry · book verbatim"** block on every card that has one. Theme-aware,
mobile-first, self-contained (the gzip dataset inflates in-browser via
`DecompressionStream`). Re-run `build_codex.py` after any harvest to refresh it.
