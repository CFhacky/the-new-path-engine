# HARVEST HISTORY — extraction ledger through 2026-08-30

This file preserves the complete working ledger that produced the verified
41-family checkpoint. It is historical evidence, not the live resume point.
Start at [../HARVEST_PROGRESS.md](../HARVEST_PROGRESS.md), then use
[STATUS.md](STATUS.md), [GAPS.md](GAPS.md), and [ROADMAP.md](ROADMAP.md).

The authority order in [../../AUTHORITY.md](../../AUTHORITY.md) still governs.
The dated notes below are intentionally retained, including statements that
were later superseded; current facts live in the status and gap documents.

**Scope reminder (from README/AUTHORITY).** This is the MECHANICS layer, the
least authoritative. It holds **book RAW only** — never canon, never invented
facts. Every harvested entry cites its book and page; a missing anchor prints
`NO COVERAGE` and is never improvised; conditions live in `conditions.py` /
`gurps_conditions.py` and are deliberately not duplicated. Do not touch Notion
from here; do not add any in-world fact or prose to the repo (that is a defect).

**Corpus root.** `I:\Sourcebooks` — OCR/text-layer extractions at `_md`,
`_text`, and `_md\_bestiary`. The PDFs on `I:\Sourcebooks` stand behind every
extraction and are the court of appeal for any garbled number.

**At a glance (2026-08-29).** Forty-one reference index families, 18,094 accepted entries.
Native 3.5e + GURPS 4e: terms/affixes (143), D&D creatures (1498), magic items
(1420), psionic powers (409), martial maneuvers (208), feats (1244 accepted), D&D spells
(1869), GURPS spells (557), GURPS creatures (472), D&D epic feats (154), D&D epic spells (70; all exact full-description spans), D&D prestige classes (145), D&D epic magic items (153; all exact full-description spans), D&D epic monsters (64; all exact full-description spans), GURPS gear — weapons + armor
(186; all exact full-row spans), GURPS advantages/disadvantages (469; all exact full-description/inline-definition spans), GURPS skills (263; all exact full-description spans), GURPS techniques (112; all exact full-description spans), D&D pact-magic vestiges (32), D&D incarnum soulmelds (89). Separately labeled other editions/systems:
D&D 5e monsters (517), 5e magic items (575), 5e spells (102), AD&D 2e psionic powers (150), AD&D 2e spells (72), AD&D 2e monsters (96), GURPS 3e creatures (853), GURPS 3e spells (766), GURPS 3e items (783); WH40K Roleplay adversaries (657, cores+bestiaries+14 supplements) + weapons (657, cores+11 supplements) + armour (145, cores+8 supplements) + force fields (13) + gear (587, cores+10 supplements) + psychic powers (420, cores+6 supplements) + talents (840, cores+11 supplements); WFRP 2e creatures (265) + arms & armour (107) + Chaos mutations & gifts (505); WH40K wargame unit profiles (136; 118 with cited book-verbatim SPECIAL RULES from born-digital codexes) + WHFB wargame unit profiles (291; 217 with cited book-verbatim SPECIAL RULES from born-digital official 8th-ed army books). Scanned codexes/army books + a broken-CMap 4th-ed book remain vision-pending. Each has a
`--selftest` that passes. Run any `scripts/*_harvest.py` with no args to rebuild
its index.

**This is a high-value SLICE, not the whole corpus.** `I:\Sourcebooks` holds
~1,700 OCR'd `.md` extractions; these indices harvest the mainline 3.5e systems
plus labeled material from dozens of sourcebooks. Substantial harvestable
mechanics remain unindexed; see **CORPUS SCOPE** below for the
inventory and what is worth harvesting next. Do not read "the core is done" as
"the corpus is done."

---

## DONE — reference indices built

| Reference file | Built by | Source(s) | Count | Selftest |
|---|---|---|---|---|
| `reference/terms_and_affixes_index.{md,json}` | `scripts/term_harvest.py` | DMG v3.5 weapon (pp.223–226) + armor/shield (pp.218–219) special abilities; GURPS 4e Basic Set enhancements (B102) + limitations (B110); GURPS 4e **Powers** new enhancements (p.107) + limitations (p.110) | 6 sections (143 entries) | `python scripts/term_harvest.py --selftest` |
| `reference/creature_index.{md,json}` | `scripts/creature_harvest.py` | `_md\_bestiary\*.md` (12 books) + `_text` Monsters and Fiends: Book of Vile Darkness (24 archfiends), Deities and Demigods (9), Monsters of the Planes (120), Book of Exalted Deeds (43 celestial paragons) | 1498 stat blocks / 16 books (a garbage-name filter — stat fragments, class/level lines, prose sentences, dangling parens — removed ~206 non-creature rows the original 1509 had let through) | `python scripts/creature_harvest.py --selftest` |
| `reference/magic_item_index.{md,json}` | `scripts/item_harvest.py` | Magic Item Compendium (842) + DMG v3.5 items (216) + Arms & Equipment Guide 3.0 (362) | 1420 items / 3 sources | `python scripts/item_harvest.py --selftest` |
| `reference/power_index.{md,json}` | `scripts/power_harvest.py` | Expanded Psionics Handbook (281) + Complete Psionic (128; running CHAPTER/POWERS headers rejected from names) | 409 powers / 2 books (408 with 3+ quick fields) | `python scripts/power_harvest.py --selftest` |
| `reference/maneuver_index.{md,json}` | `scripts/maneuver_harvest.py` | `_text\D&D 3.5e\Player Options\Tome of Battle (alt scan).md` — book lists pp.48–51 + descriptions pp.52–94 | 208 maneuvers/stances (all with 3+ quick fields and exact-source full-description spans) | `python scripts/maneuver_harvest.py --selftest` |
| `reference/feat_index.{md,json}` | `scripts/feat_harvest.py` | bundled `feats_srd35.json` + `_md\_feats\*.md` (18 supplements) | 1244 accepted feats / 19 books; 9 rejected OCR diagnostics remain under `soft` and are excluded from presentation | `python scripts/feat_harvest.py --selftest` |
| `reference/spell_index.{md,json}` | `scripts/spell_harvest.py` | bundled `spells_srd35.json` (605) + Spell Compendium (982) + post-2005 splatbooks (Complete Mage 130, Complete Champion 52, Races of the Dragon 35, Dragon Magic 37, Complete Scoundrel 28) | 1869 spells / 7 sources (all with school + level and exact-source full-text coverage) | `python scripts/spell_harvest.py --selftest` |
| `reference/gurps_spell_index.{md,json}` | `scripts/gurps_magic_harvest.py` | GURPS Magic (520) + Plant Spells (19) + Thaumatology: Urban Magics (12) + Thaumatology (6) | 557 GURPS spells (541 with 3+ quick fields) | `python scripts/gurps_magic_harvest.py --selftest` |
| `reference/gurps_gear_index.{md,json}` | `scripts/gurps_gear_harvest.py` | GURPS Low-Tech Melee Weapon Table + Armor Table | 186 gear (153 weapons + 33 torso-armor pieces, TL0–TL4, DR up to 9; all carry exact non-overlapping full-row spans) | `python scripts/gurps_gear_harvest.py --selftest` |
| `reference/gurps_trait_index.{md,json}` | `scripts/gurps_trait_harvest.py` | GURPS Basic Set: Characters — Trait Lists roster + descriptions | 469 traits (266 advantages + 203 disadvantages, all with type / exotic-super / point cost / book page and exact full-description/inline-definition spans on B18–B165) | `python scripts/gurps_trait_harvest.py --selftest` |
| `reference/gurps_skill_index.{md,json}` | `scripts/gurps_skill_harvest.py` | GURPS Basic Set: Characters — Trait Lists roster + Skills chapter | 263 skills (attribute, Easy/Average/Hard/Very Hard difficulty, defaults, book page; all with exact, non-overlapping full-description or printed cross-reference spans on B174–B228) | `python scripts/gurps_skill_harvest.py --selftest` |
| `reference/gurps_technique_index.{md,json}` | `scripts/gurps_technique_harvest.py` | GURPS Martial Arts Technique Cheat-Sheet + full Martial Arts extraction (born-digital text layers, characters exact) | 112 combat techniques (difficulty, prerequisite, default, maximum, damage; cinematic/silly flags; 112/112 exact full-description spans over 96 book blocks) | `python scripts/gurps_technique_harvest.py --selftest` |
| `reference/vestige_index.{md,json}` | `scripts/vestige_harvest.py` | Tome of Magic (born-digital text layer) — pact-magic summary, explicit stat tablets, and descriptions, pp.20–50 | 32 vestiges (vestige level 1–8, binding DC, special-requirement flag, exact-source full-description spans) | `python scripts/vestige_harvest.py --selftest` |
| `reference/soulmeld_index.{md,json}` | `scripts/soulmeld_harvest.py` | Magic of Incarnum (born-digital text layer) — soulmeld tables + descriptions, pp.54–94 | 89 soulmelds (classes, bindable chakras, basic effect, exact-source full-description spans; interleaved summary columns removed in codex display) | `python scripts/soulmeld_harvest.py --selftest` |
| `reference/gurps_creature_index.{md,json}` | `scripts/gurps_creature_harvest.py` | GURPS DF Monsters 1, Creatures of the Night 1–5, Fantasy, Banestorm, Lands Out of Time, DF Allies, DF Summoners, Big Lizzie (139) + **Natural Encyclopedia v1.5.2** compilation (333 net-new, 4e stats, each crediting its original GURPS source; deduped against the specific books) | 472 GURPS creatures / 12 sources (all with 3+ attributes) | `python scripts/gurps_creature_harvest.py --selftest` |

**Note on the "MM3 / Draconomicon absent" queue item.** That gap is CLOSED —
both were OCR'd and `creature_index` already indexes them (MM3 = 185 blocks,
Draconomicon = 96). The earlier note in the work queue is stale.

**Caveat on the feat count.** The family has **1,244 accepted rows**. Nine
rejected OCR/name fragments are retained only under source-level `soft`
diagnostics for audit and are not entries or Codex cards. The inherited
`Benefit:` anchor can still admit a small number of source blocks such as class
features; those accepted rows remain visible rather than silently reclassified.

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
| GURPS (3e+4e) | 478 | Basic Set + Powers modifiers (`term_harvest`) + **GURPS Magic (557 spells)** + **GURPS bestiary (139 creatures)** + **Low-Tech gear (186 weapons + armor)** + **Basic Set advantages/disadvantages (469)** + **Basic Set skills (263)** + **Martial Arts techniques (112)**. The native-4e character-building/combat-technique core (traits, skills, gear, spells, techniques) is now indexed; rest of the shelf (Powers advantages, more creature books, higher-TL gear) still open |
| Warhammer | 489 | **DONE for the current mechanically harvestable sources.** Labeled indices cover 40K Roleplay adversaries (657), weapons (657), armour (145), force fields (13), gear (587), psychic powers (420), and talents (840); WFRP creatures (265), gear (107), and mutations/gifts (505); WH40K wargame profiles (136; 118 with rules); and WHFB wargame profiles (291; 217 with rules). Scanned/image-only books, one broken-CMap 4th-ed book, and ambiguous rule links remain explicit NO COVERAGE; fiction is skipped. |
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

## NEXT — no concrete target queued

The dated 2026-08-27 queue is closed:

1. **Arms & Equipment Guide items — DONE.** The native item index contains
   362 accepted A&EG rows; its detector rejects running CHAPTER headers and its
   exact live count is selftested.
2. **Former term extensions — resolved by correct ownership.** GURPS Magic
   Items 1–3 already supply 783 rows in the separately labeled
   `gurps3e_item_index`. Warhammer wargear already lives in the labeled WFRP
   and WH40K Roleplay weapon/gear/armour indexes. Copying either into native
   terms would violate system separation. The image-only PHB glossary is
   explicit `NO COVERAGE` below; its condition subset remains in
   `scripts/conditions.py`.
3. **Supplemental spells — resolved.** Complete Scoundrel contributes all 28
   source-listed spells with complete spans. Player's Handbook II is explicit
   `NO COVERAGE` below. Pre-2005 spell books remain deliberate dedupe skips
   because their material is already folded into the Spell Compendium; Tome of
   Magic's mysteries/utterances are separate subsystems, not standard spells.

Future expansion should be selected deliberately from **CORPUS SCOPE**, then
entered here as a concrete book/family target before work begins.

---

## NO COVERAGE — active gaps

- `NO COVERAGE: printed-book page numbers for 110 bundled SRD 3.5 feats
  (the bundled Open Game Content source is page-less; rows cite SRD 3.5 and no
  Player's Handbook page is inferred).`
- `NO COVERAGE: Player's Handbook II spells (both available text layers
  interleave the source's three-column pages; explicit-column re-OCR still
  corrupts mechanical characters and mispairs headings/fields).`
- `NO COVERAGE: Player's Handbook v3.5 glossary (the original PDF is
  image-only; available multi-flow OCR drops real headings, promotes wrapped
  formulas to false headings, and corrupts mechanical glyphs).` Its condition
  subset is already authoritative in `scripts/conditions.py`.
- `NO COVERAGE: table-first DMG rod/staff entries (the charge/spell table
  precedes any prose name anchor).` Examples such as Rod of Absorption need a
  dedicated table-aware pass; nothing is inferred from neighboring rows.
- `NO COVERAGE: cheap full-text attachment for the 1,389 WH40K Roleplay
  weapon/gear/armour rows.` Only 850 unique exact OCR description headings are
  available across those sources, including only 35/145 armour names. Current
  Codex attachment is 72/657 weapons, 0/587 gear, and 5/145 armour; the complete
  mechanical rows remain intact and system-labeled.
- Wargame rule gaps remain explicit per harvester: 18/136 WH40K profiles and
  74/291 WHFB profiles have no unambiguous book-verbatim rule attachment.
  Scanned/image-only books and the broken-CMap WHFB source remain source-level
  `NO COVERAGE`; no rule is inferred.

Every configured source path currently resolves on this machine unless its
harvester explicitly reports a scan/CMap limitation. A future missing source
must print `NO COVERAGE — extraction missing: <path>` and be recorded here.

---

## RESOLVED POLICY

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

- **2026-08-30** — Completed the first bounded wargame vision pilot against
  official WHFB 8e High Elves PDF p.91 (printed p.92). Twelve printed profile
  lines yielded 11 unique cited profiles; the repeated Elven Steed deduped
  normally. All previous 291 WHFB rows remain byte-identical. WHFB is now 302
  profiles / 228 with rules; all other scan pages remain explicit NO COVERAGE.

- **2026-08-30** — Replaced fuzzy source resolution and 80-line caps for the
  D&D 3.5e power family with harvester-owned exact source paths and validated
  description boundaries. The 409 mechanical rows are unchanged after removing
  provenance/span metadata. Expanded Psionics Handbook supplies 278 exact spans
  and Complete Psionic 128; three XPH rows with column-interleaved power blocks
  remain explicit `NO COVERAGE`. Codex power coverage rose **125/409 → 406/409**
  and whole-Codex coverage rose **13,282 → 13,563 / 18,094**.

- **2026-08-29** — Completed the cross-index integrity audit. All **41/41**
  harvester selftests pass. The Codex now walks all 41 committed families,
  including the legacy-named 143-row terms/affixes file; inherits source-level
  book, citation, and system metadata; and excludes rejected `soft`
  diagnostics. The rebuilt payload has **18,094 accepted entries**, **13,282**
  full-text attachments, all nine exact display-system labels, zero missing
  book labels, zero polluted CHAPTER/POWERS names, and zero parsed U+FFFD.
  The 9.11 MB offline HTML passes its placeholder/size smoke test. Its only 110
  page-empty cards are bundled SRD 3.5 feats: the page-less SRD source is cited
  and no Player's Handbook page is invented.

- **2026-08-29** — Corrected two Complete Psionic names polluted by running
  page furniture: **Energy Missile** and **See Invisibility, Psionic**. The
  header terminates wrapped ALL-CAPS name recovery while retaining the prior
  span boundary. All 281 Expanded Psionics Handbook rows and the other 126
  Complete Psionic rows are byte-identical; the family remains **409** rows.
  Fixture and live selftests lock both repairs and reject future CHAPTER or
  POWERS, MANTLES leakage.

- **2026-08-29** — Corrected Arms & Equipment Guide running-header pollution.
  Twenty-one source-verified item names that had been swallowed by CHAPTER
  furniture are restored, including the printed wrapped heading **Headband of
  Simplemindedness**; one wholly false CHAPTER 6 row attached to Blackrazor's
  footer is dropped. MIC's 842 rows, DMG's 216 rows, and 341 unaffected A&EG
  rows are byte-identical. The family is now **1,420** rows (A&EG 362), and the
  live selftest locks the three source counts plus representative repairs.

- **2026-08-29** — Closed the dated NEXT queue and corrected its stale
  ownership notes. Arms & Equipment Guide was then believed complete at 363
  native item rows; the later header-pollution audit above corrected that to
  362. GURPS Magic Items 1–3 were already complete at 783 separately
  labeled GURPS 3e rows; and Warhammer wargear was already complete in the
  labeled WFRP/WH40K Roleplay weapon, gear, and armour families. All seven
  relevant harvester selftests pass and every non-native row retains its exact
  system label. The image-only PHB glossary is now machine-recorded as
  `NO COVERAGE` by `term_harvest.py`; its OCR invents headings from wrapped
  formulas, drops real headings, and corrupts mechanics, while conditions stay
  in their authoritative lookup. The 40K Roleplay full-text cheapness gate is
  also closed: 1,389 mechanical rows but only 850 unique exact OCR description
  headings (35/145 armour), so no speculative attachment was made.

- **2026-08-29** — Added all **28** source-listed Complete Scoundrel spells
  through a title-case roster detector that joins wrapped headings,
  descriptors, and level fields and records each complete source span. The
  prior 1,841 spell rows are byte-identical (0 changed/missing), the new names
  have 0 normalised overlap, and all 1,869 rows retain school, level, page, and
  source provenance. Codex spell coverage is **1,869/1,869 (100%)** and total
  coverage is **13,282/17,952 (73%)**. Player's Handbook II was separately
  tested against both available text layers and explicit three-column re-OCR;
  missing/mispaired headings and corrupt mechanical characters make it
  `NO COVERAGE`, so no PHB II row was guessed.

- **2026-08-29** — Fixed the Codex row walker so harvester `soft` diagnostic
  arrays are not presented as real entries. The bug affected only
  `wh40krp_gear_index`: 40 rejected OCR fragments nested under source
  diagnostics inflated that family from its real **587** rows to 627. The
  corrected build is **17,924** entries with the same **13,254** full-text
  blocks; every other family count is unchanged. An embedded Codex selftest
  locks the diagnostic-row exclusion.

- **2026-08-29** — Attached WHFB wargame SPECIAL RULES to the existing
  **291** official 8th-ed unit-profile rows. The additive path recognises both
  normal and display-spaced headings, pairs same-column profile grids
  geometrically, honours explicit subjects such as `SPECIAL RULES (Hound of
  Orion)`, and uses an army-list summary's printed Page value only when the
  named profile also occurs on that exact bestiary page. It preserves the
  complete named-rule paragraphs while stopping at the next subject or
  structural section. **217/291** profiles now carry book-verbatim rules and
  their own PDF-page citations: Daemons 38/54, Dwarfs 34/40, Lizardmen 28/49,
  Vampire Counts 44/52, Warriors of Chaos 32/49, and Wood Elves 41/47. The
  other **74** profiles remain mechanically indexed and are individually
  listed as `NO COVERAGE`; nothing was inferred. A canonical old/new
  projection proves all 291 pre-existing profile/mechanics/provenance rows
  unchanged. Codex WHFB coverage rose **0/291 → 217/291 (74%)** and total
  full-text coverage rose **13,037/17,964 → 13,254/17,964 (73%)**. The
  selftest locks all six profile and rule counts, the exact 74-gap complement,
  spaced/subject heading grammar, representative named rules, citations, and
  section-leak exclusions.

- **2026-08-29** — Closed the native GURPS 4e technique full-text gap and
  repaired the cheat-sheet's wrapped-name parsing. The four-page table now
  reconstructs all **113 printed rows / 112 unique techniques** instead of
  treating 13 continuation words (such as `Ranged`, `Attack (Bow)`, and
  `or Throw`) as names. This removes those 13 fragments and restores 24 full
  names, for a net **101 → 112** rows; the duplicate Lower-Body Arm Lock row is
  collapsed. All 88 unaffected old rows retain byte-identical mechanics, table
  provenance, citation, and order. Every row now points into the full
  born-digital Martial Arts extraction: **112/112** rows over **96** exact
  description groups, including ten source-shared definitions. Ordered
  multi-spans preserve seven descriptions split across columns while excluding
  the Targeted Attacks, Dirty Tricks, Using Your Legs, Combinations, Secret
  Techniques, and Silly Techniques sidebars and two unrelated quotations.
  Codex coverage rose **1/101 → 112/112 (100%)**; total full-text coverage rose
  **12,808/17,953 → 12,919/17,964 (71%)**. The live selftest locks the roster
  digest, difficulty counts, restored/forbidden names, 96 groups, ten shared
  groups, source-leading bounds, non-overlap, continuation presence, and
  sidebar/quotation exclusion. Independent old/new JSON and Codex payload
  audits plus a rendered Edge check passed.

- **2026-08-29** — Closed the native GURPS 4e trait full-text gap. The Basic
  Set harvester now reads all **469** printed Trait Lists rows (266 advantages +
  203 disadvantages), binds each to its exact description or inline-definition
  span on B18–B165, and emits the exact relative `source_path`. The repeated
  singular `Advantage` column label no longer resets the DISADVANTAGES section:
  this restores the printed negative-side Reputation and Wealth rows and
  corrects ten variable-cost rows that had been mislabeled as advantages. Of
  the former 467 rows, 457 are byte-identical and only those ten source-verified
  category fields change; two printed rows are added. Conventional, wrapped,
  grouped, perk, and quirk headings resolve on the cited B-page; Xenophilia's
  heading begins on B162 although the appendix cites B163. Reputation, Status,
  Wealth, and Neutered/Sexless deliberately share their four book blocks,
  yielding **465** unique, non-overlapping spans. Section cutovers exclude the
  following general-rule sections: Size Modifier, Other Physical Features,
  Social Background, and Culture. The Codex removes only running page
  furniture (including list headers) and preserves descriptions beyond its
  normal 4,200-character cap.
  GURPS-trait coverage rose **7/467 → 469/469 (100%)**; total full-text
  coverage rose **12,346/17,951 → 12,808/17,953 (71%)**. The live selftest locks
  the roster/mechanics SHA-256, exact counts, source-leading bounds, shared-span
  set, non-overlap, grouped definitions, chapter cutovers, page drift, and the
  10,000-character-plus Allies block. Independent source/JSON/Codex audits and a
  rendered offline-page check passed.

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


- **2026-08-30** — Added the native D&D 3.5e shadow-mystery family from
  *Tome of Magic*: 9 fundamentals and 60 path mysteries, 69 total, on PDF
  pp.142–154. The heading/category/Level-School detector handles the printed
  two-line title and split column labels, preserves every individually printed
  mechanical field, and records exact heading-to-heading description spans.
  Per-block omissions remain explicit NO COVERAGE rather than inheriting the
  chapter-wide casting-time rule or values from referenced spells. Registered
  the family in the manifest and Codex; all 69 descriptions validate as full
  text.


- **2026-08-30** — Corrected the shadow-mystery delivery spans after review
  found unrelated floating illustration captions inside five raw line ranges.
  The source-verified blocks are attached to Voice of Shadow, Dusk and Dawn,
  Shadow Skin, Arrow of Dusk, and Widened Eyes. Export and Codex delivery now
  remove exactly those five caption/artist blocks while retaining all actual
  description prose. The live selftest locks five raw illustrator lines,
  five successful exclusions, and zero delivered caption leaks.
