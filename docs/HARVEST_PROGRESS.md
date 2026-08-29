# HARVEST PROGRESS — the reference-layer extraction ledger

**Purpose.** This file is the resume point for the reference-layer harvest:
the ongoing effort to extract the *codified mechanical* knowledge of the
sourcebooks into `reference/`. It is written so Chad, or a fresh session on a
different machine, can pick up from exactly where the last one stopped. It is a
work ledger, not authority — the authority order in [AUTHORITY.md](../AUTHORITY.md)
governs, and this file records only what has been built and what is queued.

**Scope reminder (from README/AUTHORITY).** This is the MECHANICS layer, the
least authoritative. It holds **book RAW only** — never canon, never invented
facts. Every harvested entry cites its book and page; a missing anchor prints
`NO COVERAGE` and is never improvised; conditions live in `conditions.py` /
`gurps_conditions.py` and are deliberately not duplicated. Do not touch Notion
from here; do not add any in-world fact or prose to the repo (that is a defect).

**Corpus root.** `I:\Sourcebooks` — OCR/text-layer extractions at `_md`,
`_text`, and `_md\_bestiary`. The PDFs on `I:\Sourcebooks` stand behind every
extraction and are the court of appeal for any garbled number.

**At a glance (2026-08-29).** Forty-one reference index families, ~18,115 entries.
Native 3.5e + GURPS 4e: terms/affixes (143), D&D creatures (1498), magic items
(1421), psionic powers (409), martial maneuvers (208), feats (1253), D&D spells
(1841), GURPS spells (557), GURPS creatures (472), D&D epic feats (154), D&D epic spells (70; all exact full-description spans), D&D prestige classes (145), D&D epic magic items (153; all exact full-description spans), D&D epic monsters (64; all exact full-description spans), GURPS gear — weapons + armor
(186; all exact full-row spans), GURPS advantages/disadvantages (467), GURPS skills (263; all exact full-description spans), GURPS techniques (101), D&D pact-magic vestiges (32), D&D incarnum soulmelds (89). Separately labeled other editions/systems:
D&D 5e monsters (517), 5e magic items (575), 5e spells (102), AD&D 2e psionic powers (150), AD&D 2e spells (72), AD&D 2e monsters (96), GURPS 3e creatures (853), GURPS 3e spells (766), GURPS 3e items (783); WH40K Roleplay adversaries (657, cores+bestiaries+14 supplements) + weapons (657, cores+11 supplements) + armour (145, cores+8 supplements) + force fields (13) + gear (587, cores+10 supplements) + psychic powers (420, cores+6 supplements) + talents (840, cores+11 supplements); WFRP 2e creatures (265) + arms & armour (107) + Chaos mutations & gifts (505); WH40K wargame unit profiles (136, born-digital codexes) + WHFB wargame unit profiles (291, born-digital official 8th-ed army books). Scanned codexes/army books + a broken-CMap 4th-ed book remain vision-pending. Each has a
`--selftest` that passes. Run any `scripts/*_harvest.py` with no args to rebuild
its index.

**This is a high-value SLICE, not the whole corpus.** `I:\Sourcebooks` holds
~1,700 OCR'd `.md` extractions; these indices harvest the mainline 3.5e systems
plus the GURPS modifier set — on the order of 15–20 books. Substantial
harvestable mechanics remain unindexed; see **CORPUS SCOPE** below for the
inventory and what is worth harvesting next. Do not read "the core is done" as
"the corpus is done."

---

## DONE — reference indices built

| Reference file | Built by | Source(s) | Count | Selftest |
|---|---|---|---|---|
| `reference/terms_and_affixes.{md,json}` | `scripts/term_harvest.py` | DMG v3.5 weapon (pp.223–226) + armor/shield (pp.218–219) special abilities; GURPS 4e Basic Set enhancements (B102) + limitations (B110); GURPS 4e **Powers** new enhancements (p.107) + limitations (p.110) | 6 sections (143 entries) | `python scripts/term_harvest.py --selftest` |
| `reference/creature_index.{md,json}` | `scripts/creature_harvest.py` | `_md\_bestiary\*.md` (12 books) + `_text` Monsters and Fiends: Book of Vile Darkness (24 archfiends), Deities and Demigods (9), Monsters of the Planes (120), Book of Exalted Deeds (43 celestial paragons) | 1498 stat blocks / 16 books (a garbage-name filter — stat fragments, class/level lines, prose sentences, dangling parens — removed ~206 non-creature rows the original 1509 had let through) | `python scripts/creature_harvest.py --selftest` |
| `reference/magic_item_index.{md,json}` | `scripts/item_harvest.py` | Magic Item Compendium (842) + DMG v3.5 items (216) + Arms & Equipment Guide 3.0 (363) | 1421 items / 3 sources | `python scripts/item_harvest.py --selftest` |
| `reference/power_index.{md,json}` | `scripts/power_harvest.py` | Expanded Psionics Handbook (281) + Complete Psionic (128) | 409 powers / 2 books (408 with 3+ quick fields) | `python scripts/power_harvest.py --selftest` |
| `reference/maneuver_index.{md,json}` | `scripts/maneuver_harvest.py` | `_text\D&D 3.5e\Player Options\Tome of Battle (alt scan).md` — book lists pp.48–51 + descriptions pp.52–94 | 208 maneuvers/stances (all with 3+ quick fields and exact-source full-description spans) | `python scripts/maneuver_harvest.py --selftest` |
| `reference/feat_index.{md,json}` | `scripts/feat_harvest.py` | bundled `feats_srd35.json` + `_md\_feats\*.md` (18 supplements) | 1253 feats / 19 books (742 typed, 962 with prerequisite) | `python scripts/feat_harvest.py --selftest` |
| `reference/spell_index.{md,json}` | `scripts/spell_harvest.py` | bundled `spells_srd35.json` (605) + Spell Compendium (982) + post-2005 splatbooks (Complete Mage 130, Complete Champion 52, Races of the Dragon 35, Dragon Magic 37) | 1841 spells / 6 books (all with school + level) | `python scripts/spell_harvest.py --selftest` |
| `reference/gurps_spell_index.{md,json}` | `scripts/gurps_magic_harvest.py` | GURPS Magic (520) + Plant Spells (19) + Thaumatology: Urban Magics (12) + Thaumatology (6) | 557 GURPS spells (541 with 3+ quick fields) | `python scripts/gurps_magic_harvest.py --selftest` |
| `reference/gurps_gear_index.{md,json}` | `scripts/gurps_gear_harvest.py` | GURPS Low-Tech Melee Weapon Table + Armor Table | 186 gear (153 weapons + 33 torso-armor pieces, TL0–TL4, DR up to 9; all carry exact non-overlapping full-row spans) | `python scripts/gurps_gear_harvest.py --selftest` |
| `reference/gurps_trait_index.{md,json}` | `scripts/gurps_trait_harvest.py` | GURPS Basic Set: Characters — Trait Lists appendix | 467 traits (276 advantages + 191 disadvantages, all with type / exotic-super / point cost / book page) | `python scripts/gurps_trait_harvest.py --selftest` |
| `reference/gurps_skill_index.{md,json}` | `scripts/gurps_skill_harvest.py` | GURPS Basic Set: Characters — Trait Lists roster + Skills chapter | 263 skills (attribute, Easy/Average/Hard/Very Hard difficulty, defaults, book page; all with exact, non-overlapping full-description or printed cross-reference spans on B174–B228) | `python scripts/gurps_skill_harvest.py --selftest` |
| `reference/gurps_technique_index.{md,json}` | `scripts/gurps_technique_harvest.py` | GURPS Martial Arts Technique Cheat-Sheet (born-digital text layer, characters exact) | 101 combat techniques (difficulty, prerequisite, default, maximum, damage; cinematic/silly flags) | `python scripts/gurps_technique_harvest.py --selftest` |
| `reference/vestige_index.{md,json}` | `scripts/vestige_harvest.py` | Tome of Magic (born-digital text layer) — pact-magic summary, explicit stat tablets, and descriptions, pp.20–50 | 32 vestiges (vestige level 1–8, binding DC, special-requirement flag, exact-source full-description spans) | `python scripts/vestige_harvest.py --selftest` |
| `reference/soulmeld_index.{md,json}` | `scripts/soulmeld_harvest.py` | Magic of Incarnum (born-digital text layer) — soulmeld tables + descriptions, pp.54–94 | 89 soulmelds (classes, bindable chakras, basic effect, exact-source full-description spans; interleaved summary columns removed in codex display) | `python scripts/soulmeld_harvest.py --selftest` |
| `reference/gurps_creature_index.{md,json}` | `scripts/gurps_creature_harvest.py` | GURPS DF Monsters 1, Creatures of the Night 1–5, Fantasy, Banestorm, Lands Out of Time, DF Allies, DF Summoners, Big Lizzie (139) + **Natural Encyclopedia v1.5.2** compilation (333 net-new, 4e stats, each crediting its original GURPS source; deduped against the specific books) | 472 GURPS creatures / 12 sources (all with 3+ attributes) | `python scripts/gurps_creature_harvest.py --selftest` |

**Note on the "MM3 / Draconomicon absent" queue item.** That gap is CLOSED —
both were OCR'd and `creature_index` already indexes them (MM3 = 185 blocks,
Draconomicon = 96). The earlier note in the work queue is stale.

**Caveat on the feat count.** `feat_harvest.py` (like `feat_lookup.py`, whose
detector it duplicates) anchors on a `Benefit:` line, so the 1253 total
includes a minority of non-feat blocks that also carry a `Benefit:` line —
some class features and alternative class features. This is inherited and
honest; a translator triaging the index should expect a few such rows.

### Related lookup scripts (retrieval — the play-time siblings of the indices)

These print one entry, ready to paste, for live play; the harvest indices above
give the browsable/translatable collation. Both are wanted; the lookup is not
made redundant by the index (spells and creatures already run this way, and now
feats do too):

- `scripts/spell_lookup.py` — SRD 3.5 (605 spells, bundled JSON) + Spell
  Compendium (live parse). SRD wins name collisions. Its index sibling is
  `spell_harvest.py`. (Its `DEFAULT_COMPENDIUM` was pointing at a stale
  `_md\Spell_Compendium.md` that no longer exists — the Compendium had gone
  silently inaccessible; fixed 2026-08-27 to the `_text\...\Spell Compendium
  (Premium).md` path, restoring 1031 Compendium spells to the tool.)
- `scripts/feat_lookup.py` — SRD 3.5 (bundled JSON) + supplement extractions
  under `_md\_feats\` (live parse). Its index sibling is `feat_harvest.py`.
- `scripts/monster_lookup.py` — `_md\_bestiary\` (live parse); its index
  sibling is `creature_harvest.py` (detector duplicated, not imported).

---

## CORPUS SCOPE — what is on the drive vs. what is harvested

`I:\Sourcebooks` is far larger than the harvested slice. Counts from a
2026-08-27 sweep (`.md` extractions; `_text` tree unless noted):

| Shelf | `.md` files | Harvested so far |
|---|---|---|
| D&D 3.5e | 121 | ~12 books (Core DMG/PHB spells, MIC, XPH, ToB, Spell Compendium, +feat supplements from `_md\_feats`) |
| D&D 3.0 | 16 | none (mostly superseded; A&EG queued) |
| D&D 5e | 35 | **517 monsters** across 12 books in `dnd5e_creature_index`, plus **575 magic items** in `dnd5e_item_index` and **102 spells** in `dnd5e_spell_index` — all stamped `system: D&D 5e`. OTHER EDITIONS ARE WELCOME if labeled by edition/system (Chad has translator tools that convert). |
| AD&D | 19 | **AD&D 2e psionic powers (150)** in `ad2e_psionic_index` + **AD&D 2e spells (72)** in `ad2e_spell_index` (Menzoberranzan + FOR2/5/7 + Ravenloft, born-digital, labeled `system: AD&D 2e`). The 2e Monstrous Compendium bestiaries have two-column OCR with scrambled value order — SOLVED by rendering the PDF pages and reading them by vision: **MC Appendix II (25 monsters) is DONE** in `ad2e_monster_index`. MC Appendix III (~30 more) can be added the same way. |
| GURPS (3e+4e) | 478 | Basic Set + Powers modifiers (`term_harvest`) + **GURPS Magic (557 spells)** + **GURPS bestiary (139 creatures)** + **Low-Tech gear (186 weapons + armor)** + **Basic Set advantages/disadvantages (467)** + **Basic Set skills (263)**. The native-4e character-building core (traits, skills, gear, spells) is now indexed; rest of the shelf (Powers advantages, Martial Arts techniques, more creature books, higher-TL gear) still open |
| Warhammer | 489 | **IN PROGRESS (per Chad, 2026-08-28)** — harvesting the MECHANICS into labeled `system:` indices (distinct from the translator skill, which owns conversion INTO canon). 40K Roleplay adversaries (291) done; weapons/talents/psychic-powers agents running; WFRP + the 40K/WHFB wargames queued. Fiction files skipped. |
| Dragon Magazine | 446 | none (mixed crunch/articles — needs a crunch-only detector) |
| Forgotten Realms | 71 | none (setting + some crunch) |
| Other RPG systems | 8 | none |
| **`_text` total** | **1,714** | — |

Highest-value UNHARVESTED 3.5e content, by directory (all under
`_text\D&D 3.5e\`), that the existing scripts can absorb by adding sources:

- **`Monsters and Fiends\`** — DONE. The bestiaries beyond the `_md\_bestiary`
  twelve (Book of Vile Darkness, Book of Exalted Deeds, Deities and Demigods,
  Monsters of the Planes) are now in `creature_index` via `creature_harvest.py`'s
  `EXTRA_BOOKS`. (Draconomicon, Fiend Folio, FC1/FC2, Libris Mortis, Lords of
  Madness here were duplicates of the harvested set.)
- **`DM Toolkits\`** — Elder Evils, Exemplars of Evil (more stat blocks), Manual
  of the Planes, Planar Handbook, Stronghold Builders Guidebook. **Epic Level
  Handbook epic feats: DONE** in `epic_feat_index`: all 153 Table 1-36 rows plus
  description-only **Dire Charge** (154 total), with **149 exact full-description
  spans**. The `.md`/`.ocr300.md` text layers corrupt names and interleave the
  ornate two-column pages, so table mechanics remain vision-transcribed from
  pp.46-49. The harvester's reproducible `--extract-source` path renders
  description pages 50-69 through PyMuPDF at 4×, OCRs each column separately
  with Tesseract, preserves the body OCR raw, and restores only canonical
  book-verified headings. Five descriptions that cross or occupy the genuinely
  blurred p.60 image remain empty and explicit `NO COVERAGE`; they are never
  inferred from neighboring text. The real ELH PDF
  (`I:\Sourcebooks\...\Epic Level Handbook.pdf`, 11.9 MB, 334 pp) is the court
  of appeal and PyMuPDF reads it directly from `I:\`.
  **Two tiers for corrupt OCR:** (1) `scripts/reocr.py` handles plain scans and
  fixes visual order, but individual characters still need mechanical
  spot-checks; (2) rendered-page vision is required for ornate pages and exact
  table values. The epic-feat description extraction uses raw OCR only for
  prose bodies, never to overwrite verified summary mechanics.
- **`Player Options\`** — subsystems not yet indexed: **Magic of Incarnum**
  (all 89 soulmeld summary rows and full description spans are DONE in
  `soulmeld_index`; essentia/bind details remain book-verbatim prose rather than
  separately parsed fields), **Tome of Magic** shadow-magic mysteries + truename utterances
  (all 32 pact-magic vestige summary/tablet fields and full description spans are
  DONE in `vestige_index`; granted powers remain book-verbatim prose, while
  mysteries and utterances are prose-embedded spell-like blocks that need a
  separate body-block detector), Savage Species (monster classes), Incantatrix/variant
  material in Unearthed Arcana. The
  Complete-series and Races-of books' feats are already in `feat_index`; their
  pre-2005 spells are already in the Spell Compendium.
- **`Magic and Items\`** — Tome of Feats (3pp, more feats).

GURPS 4e mechanics worth harvesting (in `_text\GURPS\GURPS 4e\`, 478 files
total): GURPS Magic (spell list), GURPS creature books (bestiary lines),
GURPS Fantasy/Dungeon Fantasy gear and templates. These need GURPS-format
detectors, not the D&D ones.

### KEY finding — detector robustness × OCR pipeline (read before harvesting more)

Two OCR pipelines exist on the drive: the `_md` pipeline (`_md\_bestiary`,
`_md\_feats`, and `_md\*.md`) is CLEANER, and the `_text` pipeline (pytesseract,
column-aware) is ROUGHER — both are near-full books, not curated subsets. Which
matters depends on the detector:

- **Robust anchor detectors usually handle rough `_text` well.** The spell
  (school line + Level below), power (discipline + psionics field), and item
  (trailer / `Name:` colon) detectors produced clean output from their raw
  `_text` books. Tome of Battle is the caution: its old `(Type)` + Level
  detector produced a useful 171-row slice, but the clean alternate extraction
  and Level/Class anchor prove the complete list is 208.
- **Fragile name-above detectors produce GARBAGE on rough `_text`.** The feat
  (`Benefit:` anchor, name gathered above) and creature (stat line + name
  above) detectors, run against `_text` books, grabbed prose fragments as names
  (Epic Level Handbook feats → "A minimum ability", "Your", "Noucancast";
  Book of Vile Darkness creatures → "Outsider (Chaotic, Evil); Hd 6D8+6..."). On
  the `_md` pipeline (where feat_harvest/creature_harvest source their books)
  the SAME detectors are clean.

**Implication for the remaining work:** feed each detector the pipeline it likes.
Anchor-detector content (more spells/powers/items/maneuvers) can be pulled from
`_text` and validated per book (as Complete Psionic was — verify 0 junk, hits
clustered in the right chapter, count sane). Name-above content (feats,
creatures) from `_text`-only books (Epic Level Handbook, Book of Vile Darkness,
Deities and Demigods, the third-party bestiaries) needs EITHER a hardened
detector (wrapped-name gathering + a stricter name test, the way power_harvest
was hardened for Complete Psionic) OR an `_md`-pipeline re-OCR of that book.
Do not add them as-is — they degrade the clean index. The `_text` bestiaries
also use varied stat-block grammars (inline `CR X; Size Type; HD Y`, deity
blocks, prose-embedded NPCs), so a `_text` creature detector is its own task.

## NEXT — queued harvest targets (in priority order)

All source OCR listed below was verified present on `I:\Sourcebooks` on
2026-08-27. Each is a *new detector/section*, not new OCR.

1. **Arms & Equipment Guide (3.0) items** → `item_harvest.py` `aeg` detector.
   Source: `_text\D&D 3.0\Arms And Equipment Guide.md` (present, 22,767 lines).
2. **`term_harvest.py` extensions** (named in that script's own docstring as
   intended next Sections; their extractions exist in the corpus):
   Warhammer wargear, the PHB glossary, and the GURPS magic-item books. Each
   is a new `Section` with a `start_anchor` / `end_anchor` / `parser`.
3. **More supplemental spells** → add sources to `spell_harvest.py`. The clean
   post-2005 books are DONE (Complete Mage, Complete Champion, Races of the
   Dragon, Dragon Magic — validated clean, clustered, genuinely new). **Do not
   bulk-add the rest without a dedupe pass:** a 2026-08-27 sweep found the
   2004-2005 books (Complete Arcane/Divine/Adventurer, Races of Stone/Destiny/
   Wild, Sandstorm/Stormwrack/Frostburn, Heroes of Horror, Magic of Incarnum)
   PRE-date or coincide with the 2005 Spell Compendium, so most of their spells
   are already indexed — harvesting them injects OCR-variant duplicates
   ("Bsorption" for "Absorption"). Tome of Magic is truename/pact/shadow
   subsystem content (school+level-shaped but not standard spells). To add any
   of these, first dedupe against the existing index by normalised name. What
   remains cleanly harvestable:
   - **PHB2** and **Complete Scoundrel** yield 0 with `detect_compendium` — a
     different spell-block format (no ALL-CAPS name / school / `Level:` triple).
     Would need a format-specific detector.
   - Other post-2005 books (Complete Arcane is PRE-2005 and already in the
     Compendium; check publication date before adding — pre-2005 = skip).
   - When adding any book: run it, confirm 0 header-polluted names and that the
     hits cluster in the spell chapter (not scattered), then keep it.
     `HEADER_REJECT` now catches the generic SPELLS / INVOCATIONS / DESCRIPTIONS
     / CHAPTER running-header words, so most books need no per-book header work.

- **`item_harvest.py`**: append a `Source(...)` to `SOURCES` with a new
  `detector` key, write `detect_<key>(lines, pages, book)` returning
  `List[Item]`, register it in `DETECTORS`, add a fixture + assertions to
  `selftest`, rerun `--selftest`, then rebuild. A configured source whose file
  is missing prints `NO COVERAGE` automatically.
- **`term_harvest.py`**: append a `Section(...)` to `SECTIONS` (choose
  `parser="colon_defs"` or `"gurps_modifiers"`, or add a parser). Missing
  anchors print `NO COVERAGE`.
- **new harvest script**: mirror `creature_harvest.py` / `item_harvest.py`
  exactly — stateless, real provenance per entry (book + PDF page), on-demand
  `--export` packet rather than copying raw text into the repo, `--selftest`
  with an embedded fixture AND live checks, `NO COVERAGE` for missing sources.
  Then **add a row to the AUTHORITY.md governing-sources table** — a script
  without that row is not ratified.

---

## NO COVERAGE — active gaps

None active. Every source currently configured in a harvest script resolves on
this machine. The items in **NEXT** above are *unbuilt detectors for OCR that
exists*, not missing OCR. If a future session configures a source whose
extraction is absent, the harvest prints `NO COVERAGE — extraction missing:
<path>` and this section should record the book and the missing extraction so
the OCR pipeline can be pointed at it.

Partial-coverage gap (detector limitation, not missing OCR): in the DMG item
harvest, rod and staff entries whose block opens with a charge/spell table
before any prose (e.g. Rod of Absorption) are not caught by the trailer+name
detector and are absent from `magic_item_index`. Closing this needs a
table-aware pass over the DMG `RODS`/`STAFFS`/`WANDS` sections; low priority
since the MIC already supplies a large clean item set.

Known genuinely-un-OCR'd shelves (different grammars; not yet worth a detector
until OCR'd and prioritized): Warhammer 40k RPG bestiaries and WFRP profiles
(WS/BS/S/T/W/I/A/Ld percentile blocks), AD&D 2e monstrous compendia. These are
the `corpus-mass-translator` skill's territory, not this layer's, unless Chad
asks for them here.

---

## NEEDS CHAD

- **(RESOLVED 2026-08-27) Raw-OCR fidelity vs. hand repair.** Chad ruled: repair
  the garbled OCR and entries by hand rather than leave raw junk. The
  harvest-RAW default is now overridden BY THAT INSTRUCTION — but only for
  VERIFIED corrections: a garble is fixed to the value its own surrounding text
  (description / class / level / page) proves, never guessed; anything that
  cannot be resolved from the source is FLAGGED, not invented. The repair method
  and every fix are recorded in [OCR_REPAIRS.md](OCR_REPAIRS.md): source `.md`
  name lines are corrected in place (so every future harvest is clean, since
  `I:\Sourcebooks` is not version-controlled and that log is the re-apply list),
  and detector-level false positives are fixed in the scripts. First pass fixed
  9 XPH power names and 8 feat false positives; 5 fragmentary creature names are
  flagged for PDF verification.

---

## LOG

- **2026-08-29** — Closed the native GURPS 4e skill full-text gap. The Basic
  Set harvester still reads all **263** roster rows from the Trait Lists
  appendix, but now binds each row to its exact, non-overlapping Skills-chapter
  description span on B174–B228 and emits the exact relative `source_path`.
  Grouped definitions under Acrobatics, Crewman, Environment Suit,
  Enthrallment, and Melee Weapon are bounded independently. Four appendix rows
  whose names wrapped after the Page cell are source-verified and repaired to
  Computer Operation/TL, Electronics Operation/TL, Hazardous Materials/TL, and
  Intelligence Analysis/TL, including their clean defaults and lost TL flags;
  Brain Hacking's printed cross-reference uses the book's no-`/TL`
  `description_key`. All 259 unaffected rows retain their names and mechanics,
  and all 263 retain their citation, page, position, and order. The Codex removes
  only running page furniture and keeps the three descriptions longer than its
  normal 4,200-character cap. GURPS-skill coverage rose **14/263 → 263/263
  (100%)**; total full-text coverage rose **12,097/17,951 → 12,346/17,951
  (68%)**. The live selftest locks the 263-row roster, the four verified row
  repairs and Brain Hacking alias, unique source-leading spans, non-overlap, the
  nested Axe/Mace and cross-page Knife boundaries, and the Zen
  Archery/Techniques cutover. Independent JSON/Codex audits and a rendered
  offline-page check passed.

- **2026-08-29** — Closed the native GURPS 4e gear full-text gap. The
  Low-Tech harvester now emits its exact relative `source_path` and bounds all
  **153 weapon** and **33 armor** table rows at their real ends. The former
  fixed-width weapon spans could bleed into the next item (Axe admitted the
  opening of Hatchet); section/page furniture and the next row are now excluded,
  while alternate attack modes and armor note cells remain inside their owning
  block. All 186 prior names, mechanics, citations, pages, categories, and row
  order are unchanged; only 160 location ends needed correction. GURPS-gear
  coverage rose **0/186 → 186/186 (100%)**; total full-text coverage rose
  **11,911/17,951 → 12,097/17,951 (67%)**. The live selftest locks the 153/33
  counts, exact name-leading spans, non-overlap, page-furniture exclusion, and
  the Axe/Hatchet boundary; an independent audit matched every Codex full block
  byte-for-byte to its bounded source slice.

- **2026-08-29** — Recovered the D&D 3.5e epic-monster description layer.
  The harvester now generates a deterministic 4× two-column OCR source from
  rendered Epic Level Handbook pp.158-230, preserves every body line raw,
  restores only the **50** book-verified shared-section headings, and records
  exact spans for all **64** roster rows. Printed families such as behemoths,
  colossi, devastation vermin, primal elementals, golems, legendary animals,
  sirrushes, and slaadi deliberately share the book's common description block.
  A same-height Hunefer/Lavawight boundary is split by stable OCR row order so
  neither the final Hunefer line nor the Lavawight title is lost or crossed.
  All 64 prior rows are byte-identical across their original mechanical and
  provenance fields (0 missing, 0 added, 0 changed, 0 reordered).
  Epic-monster coverage rose **0/64 → 64/64 (100%)**; total full-text coverage
  rose **11,847/17,951 → 11,911/17,951 (66%)**. The live selftest locks the
  64-row roster, 50 shared blocks and their multiplicities, exact source-leading
  spans, complete soft-free recovery, and the tied-row boundary; two complete
  source generations produced the same SHA-256, which the JSON index records.

- **2026-08-29** — Recovered the D&D 3.5e epic-spell description layer. The
  harvester now generates a deterministic two-column OCR source from rendered
  Epic Level Handbook pp.74-102, keeps every body line raw, restores only the
  **70** book-verified headings, and records one exact heading span for each of
  the 24 seeds and 46 sample spells. Verified custom lane routes retain the
  Contact/Energy/Ward “another use” mechanics while excluding unrelated inset
  boxes and the following epic-psionics section. All 70 prior rows are
  byte-identical across their original name/kind/book/DC/school/effect/citation/
  page/note fields (0 missing, 0 added, 0 changed). Epic-spell coverage rose
  **0/70 → 70/70 (100%)**; total full-text coverage rose **11,777/17,951 →
  11,847/17,951 (65%)**. The live selftest locks the 24/46/70 family counts,
  the exact anchor set, 70 unique source-leading spans, complete soft-free
  recovery, and exclusion boundaries; the index records the external source
  SHA-256.

- **2026-08-29** — Recovered the D&D 3.5e epic-item description layer. The
  harvester now generates a deterministic two-column OCR source from rendered
  Epic Level Handbook pp.126-146, keeps all body OCR raw, restores only **103**
  book-verified item/ability headings, and records exact heading spans for all
  **153** rows. Numeric variants, armor/shield duplicates, elemental-immunity
  rings, and the ten Wyrm rods deliberately reuse the one common description
  block printed by the book. Nine descriptions that flow around generation
  tables use verified lane cutovers, so unrelated tables are not admitted as
  false full text. All 153 prior rows are byte-identical across their original
  name/kind/type/book/price/effect/citation/page fields (0 missing, 0 added, 0
  changed). Epic-item coverage rose **0/153 → 153/153 (100%)**; total full-text
  coverage rose **11,624/17,951 → 11,777/17,951 (65%)**. The live selftest locks
  the 55/98/153 family counts, 103 description groups, shared-span
  multiplicities, source-leading validation, exact mechanics, and absence of
  swallowed numbered tables; the index records the external source SHA-256.

- **2026-08-29** — Recovered the D&D 3.5e epic-feat description layer. The
  harvester now generates a deterministic two-column OCR source from rendered
  Epic Level Handbook pp.50-69, restores only book-verified canonical headings,
  and records exact heading-to-heading spans. It also adds **Dire Charge**, whose
  full p.53 entry is present in the book although Table 1-36 omits it, raising
  the family **153 → 154**. All 153 prior rows are byte-identical across their
  original name/book/type/prerequisite/citation/page fields. **149** entries now
  carry complete bounded source blocks. Five descriptions dependent on the
  genuinely blurred p.60 image — Improved Spell Capacity, Improved Spell
  Resistance, Improved Stunning Fist, Improved Whirlwind Attack, and Incite
  Rage — remain empty with explicit `NO COVERAGE`, never reconstructed.
  Epic-feat coverage rose **0/153 → 149/154 (97%)**; total full-text coverage
  rose **11,475/17,950 → 11,624/17,951 (64%)**. The live selftest locks the
  154-name/type set, exact five-gap set, page/span boundaries, the page-64
  floated Planar Turning alternative, Dire Charge mechanics/citation, and
  absence of U+FFFD in parsed fields; the independent audit also verifies the
  recorded source hash.

- **2026-08-29** — Completed and fully spanned the D&D 3.5e martial-maneuver
  family. The book’s own lists on pp.48–51 and its detailed blocks on pp.52–94
  independently reconcile to **208** unique maneuvers/stances; the former noisy
  scan’s `(Type)`-anchored detector found only 171. The clean alternate
  extraction now uses a Level/Class anchor, retaining five legitimate entries
  whose printed signatures have no Boost/Counter/Stance/Strike token and the
  comma-ordered **DIVINE SURGE, GREATER** heading. Summary-list reconciliation
  supplies canonical book names; all 171 prior rows map one-to-one after 16
  source-verified name repairs, and the other **37** rows are genuine additions.
  Wrapped signature values are joined only across source-proven continuations,
  replacing OCR truncation/cross-column leakage with the clean book text.
  Every row now emits the exact alternate `source_path` and a validated
  heading-to-heading full-description span; complete long entries bypass the
  codex’s normal cap. Maneuver coverage rose **1/171 → 208/208 (100%)**; total
  full-text coverage rose **11,268/17,913 → 11,475/17,950 (63%)**. The live
  selftest locks the 208 summary/detail names, discipline and type totals, all
  core fields, pp.52–94 span boundaries, canonical repairs, and recovered
  type-less entries.

- **2026-08-29** — Closed the D&D 3.5e vestige full-text gap. Replaced the
  summary-table marker offsets with all **32** validated ALL-CAPS description
  spans (PDF pp.20–50) and emitted the exact Tome of Magic `source_path`.
  Explicit per-entry stat tablets are now the court of appeal for the summary:
  they recover **Orthos** (level 8, binding DC 35, special requirement; p.43),
  whose final summary-table level cell was lost at a page break, raising the
  index 31 → 32. They also verify seven level corrections: Ronove 2 → 1,
  Savnok 3 → 2, Paimon 4 → 3, Tenebrous 5 → 4, Otiax 6 → 5, Zagan 7 → 6,
  and Marchosias 8 → 7. Every other non-location field in the original 31 rows
  is unchanged. The codex removes only duplicated stat tablets floated into the
  description stream, keeps complete long descriptions beyond its normal cap,
  and applies name-leading validation. Vestige coverage rose **0/31 → 32/32
  (100%)**; total full-text coverage rose **11,236/17,912 → 11,268/17,913
  (62%)**. The live selftest locks all 32 tablet records and headings, explicit
  mechanics, span leads, cleaned granted-ability text, and the corrected values.

- **2026-08-29** — Closed the D&D 3.5e soulmeld full-text gap. Replaced the
  summary-table marker offsets with all **89** validated ALL-CAPS description
  spans (PDF pp.54–94) and emitted the exact Magic of Incarnum `source_path`.
  The table parser now preserves the verified **Heart of Fire** row (p.70),
  raising the index 88 → 89. Its former misclassification had also assigned the
  following Lamia, Manticore, Phoenix, and Wormtail Belts to Heart; the book’s
  Waist header verifies all four corrections to Waist. Every other non-location
  field in the original 88 rows is unchanged. The codex removes only the
  summary-table columns interleaved into four description spans, then applies
  its normal name-leading validation. Soulmeld coverage rose **0/88 → 89/89
  (100%)**; total full-text coverage rose **11,147/17,911 → 11,236/17,912
  (62%)**. The live selftest locks the 89 rows/headings, page range, span leads,
  Heart of Fire values, and the four corrected Waist chakras.

- **2026-08-29** — Closed the D&D 3.5e spell full-text gap. The 1,841 committed
  spell rows and their `[start,end]` spans were already byte-identical and valid
  against the harvesters’ `_text` files; the codex’s global fuzzy filename cache
  had instead bound Complete Mage/Champion, Races of the Dragon, and Dragon Magic
  to same-named `_md\_feats` scans before it reached the spell family.
  `spell_harvest.py` now emits each source’s exact relative `source_path`, and the
  codex honors that provenance before any fuzzy fallback. The live selftest locks
  all six source counts and validates every non-SRD span against its own source.
  Codex spell coverage rose **1,730/1,841 → 1,841/1,841 (100%)**; total full-text
  coverage rose **11,036/17,911 → 11,147/17,911 (62%)**, with all prior spell
  mechanics byte-identical.

- **2026-08-27** — Un-deferred GURPS Fantasy creatures (Chad: "keep going on
  the gurps fantasy creatures"). Added a third detector, `gurps_titlecase`:
  Fantasy uses inline stats but Title-Case names sitting far above long
  descriptions, so detection requires a FULL `ST;DX;IQ;HT` block (rules out the
  prose "ST N;" weather/rules lines) and finds the name by the fact that a
  creature's name ECHOES lowercased in its own description ("the manticore has
  the face…"), with a frequency guard that rejects a repeated topic word
  ("Christianity", ~10×) while keeping a real name ("Panther", 4×). +8 clean
  Fantasy creatures (Manticore, Unicorn, Satyr, Amphisbaena, Megalogryphon, …);
  GURPS bestiary now 52.
- **2026-08-27** — Added `gurps_creature_harvest.py` (continuing the GURPS
  shelf): a GURPS bestiary index (`reference/gurps_creature_index`), 44
  creatures with the GURPS attribute block (ST/DX/IQ/HT/HP/…), separate from
  the D&D creatures. Two stat formats handled — the vertical "ST: N" layout
  (Dungeon Fantasy Monsters 1, 25) and the inline "ST N; DX N; …" layout
  (Creatures of the Night Vol.1–5, 19); names are the ALL-CAPS header gathered
  above the block (wrapped names joined, "THE MONSTERS"/section headers
  rejected). **GURPS Fantasy is DEFERRED** — inline stats but Title-Case
  creature names, so the ALL-CAPS detector yields its section headers, not
  creatures; it needs a Title-Case name detector (a real next task). More GURPS
  creature books (Banestorm, Monster Hunters, Dungeon Fantasy adventures) can
  be added as sources once their name style is checked.
- **2026-08-27** — Hand-repair pass (Chad's direction). Fixed 9 OCR-mangled
  power names in the XPH source `.md` (verified from each block's own text;
  e.g. `yy` → Energy Ball, `ue Creation` → True Creation) and rebuilt
  `power_index`; tightened `feat_harvest`'s name test to drop 8 field/NPC-line
  false positives (1253 → 1244 feats). All fixes recorded in
  [OCR_REPAIRS.md](OCR_REPAIRS.md); 5 fragmentary creature names flagged there
  for PDF verification (not guessed).
- **2026-08-27** — Added `gurps_magic_harvest.py` (Chad's direction — start the
  GURPS shelf, the biggest untouched high-value body for a D&D/GURPS hybrid):
  harvested **GURPS Magic** into a NEW index, `reference/gurps_spell_index`,
  520 spells (505 with 3+ fields), the GURPS magic system kept separate from the
  D&D `spell_index`. Class-anchored detection (Regular/Area/Missile/...) proven
  by a spell field below + a Title-Case name above; dedupes the per-college
  listings by name (keeping the richest entry); captures the (VH) Very-Hard
  difficulty marker as a field and strips it from the name while leaving genuine
  parentheticals ("Repel (Animal)") intact. GURPS Magic's OCR is clean, so no
  per-entry hand-repair was needed here (0 garbled names/fields).
- **2026-08-27** — Added Dragon Magic (2006) to `spell_harvest.py`: +37 clean
  spells (index 1804 → 1841), genuinely new (post-Compendium). Swept the other
  spell-bearing books and found the 2004-2005 ones overlap the Compendium with
  OCR-variant duplicates — left out, with the dedupe requirement recorded in
  NEXT.
- **2026-08-27** — Corpus review (prompted by Chad): the harvested set is a
  high-value SLICE of ~1,700 OCR'd files, not the whole corpus. Added
  `reference/README.md` (folder manifest), a CORPUS SCOPE inventory, and the
  detector-robustness finding above. Then, validating that robust detectors work
  on rough `_text`, added **Complete Psionic** to `power_harvest.py`: +128
  powers (125 new; index 281 → 409). Hardened the power detector with ALL-CAPS
  wrapped-name gathering ("ANALYZE DWEOMER," / "PSIONIC" → "Analyze Dweomer,
  Psionic") + conditional title-casing; XPH output unchanged (still 281).
- **2026-08-27** — Added three post-2005 splatbooks to `spell_harvest.py`
  (Complete Mage 130, Complete Champion 52, Races of the Dragon 35 = 217 new
  spells; index now 1804). These spells postdate the 2005 Spell Compendium and
  are genuinely new — Complete Mage overlaps the Compendium by only 1 of 130.
  Generalised `HEADER_REJECT` to strip any book's spell-chapter running header
  (SPELLS / INVOCATIONS / DESCRIPTIONS / CHAPTER as whole words) while keeping
  real "Spell ..."-named spells; all three books validated 0-junk and clustered
  in their spell chapters. PHB2 and Complete Scoundrel use a different block
  format (0 hits) and were left out.
- **2026-08-27** — Extended `term_harvest.py` with two GURPS 4e **Powers**
  Sections (New Enhancements p.107, New Limitations p.110): 11 + 13 = 24 new
  modifiers (Affects Others, Force Field, Reflexive, Insubstantial Only, ...),
  balancing the thin GURPS side of this D&D/GURPS hybrid. The existing
  `gurps_modifiers` parser handled the Powers grammar unchanged; the existing
  four Sections are untouched.
- **2026-08-27** — Added `spell_harvest.py`; built the spell index (1587
  spells: bundled SRD core 605 + Spell Compendium 982, all with school +
  level). School-anchored detection with the name gathered above, joining
  wrapped names ("ACCELERATED MOVEMENT") once and stripping the three-line
  running page header ("CHAPTER 1 / SPELL / DESCRIPTIONS") the OCR drops above
  spell names — while keeping real "SPELL ..."-prefixed names. Completes the
  core reference layer (creatures, items, feats, powers, maneuvers, spells all
  have both a lookup and an index). Registered in AUTHORITY.md.
- **2026-08-27** — Fixed `spell_lookup.py`'s stale `DEFAULT_COMPENDIUM`: it
  pointed at `_md\Spell_Compendium.md`, which no longer exists, so the Spell
  Compendium had gone silently inaccessible to the play-time tool. Repointed to
  `_text\D&D 3.5e\Magic and Items\Spell Compendium (Premium).md`; its selftest
  Compendium checks (Orb of Acid, >900 spells) now run and pass (1031 spells).
- **2026-08-27** — Extended `item_harvest.py` with a `dmg` detector; harvested
  the DMG v3.5 specific and wondrous items (216, all with aura + caster level,
  145 priced) — the canonical items nothing else covered. Detection anchors on
  the trailer line (`Aura School; CL Nth; ...; Price`) and takes the name from
  the nearest `Name:` colon-line above. The two weapon/armor "special ability"
  sections (the affixes) are MASKED because `term_harvest.py` owns them — the
  selftest asserts Ghost Touch does not leak. Rings and staffs listed by
  property ("Protection:" = Ring of Protection, "Frost:" = Staff of Frost) are
  captured under those terse names; rods/staffs whose entries begin with a
  charge table (e.g. Rod of Absorption) are the accepted partial gap below.
- **2026-08-27** — Added `feat_harvest.py`; built the feat index (1253 feats
  across the bundled SRD core + 18 supplement extractions; 742 typed, 962 with
  a prerequisite). Detection duplicated from `feat_lookup.py`; adds inline
  `[Type]`-tag splitting (peeling multiple OCR-mangled tags off the name line)
  and SRD prerequisite parsing. Completes the reference-layer symmetry (every
  family now has both a lookup and an index). Registered in AUTHORITY.md.
- **2026-08-27** — Added `maneuver_harvest.py`; harvested Tome of Battle (171
  maneuvers/stances across all nine disciplines, 170 with 3+ quick fields). The
  discipline word is badly OCR-corrupted in this book (Iron Heart appears as
  Tron/[ron/Jron/4ton Heart), so detection anchors on the reliable `(Type)`
  token + a Level/Class line below, and recovers the discipline by keyword
  (each discipline has a unique surviving word — "heart" -> Iron Heart, "wind"
  -> Desert Wind). That lifted Iron Heart from 8 to 16 and balanced the
  distribution. Registered in AUTHORITY.md.
- **2026-08-27** — Added `power_harvest.py`; harvested the Expanded Psionics
  Handbook (281 powers, all with 3+ quick fields). Discipline-anchored
  detection with a psionics-field test; tolerates descriptor lines that wrap
  across the OCR column break (recovered the 20 Telepathy [Compulsion] powers —
  Dominate, Insanity, Suggestion, etc.). Registered in AUTHORITY.md.
- **2026-08-27** — Added `item_harvest.py`; harvested the Magic Item Compendium
  (842 items, 837 with 3+ quick fields). Handles wrapped multi-line names and
  inline `[RELIC]`/`[SYNERGY]` tags. Registered in AUTHORITY.md. Created this
  progress ledger. Confirmed `creature_index` already covers MM3 + Draconomicon
  (the stale "bestiaries absent" queue item is closed).
