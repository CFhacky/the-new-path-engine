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

**At a glance (2026-08-28).** Thirty-six reference index families, ~15,440 entries.
Native 3.5e + GURPS 4e: terms/affixes (143), D&D creatures (1498), magic items
(1421), psionic powers (409), martial maneuvers (171), feats (1253), D&D spells
(1841), GURPS spells (557), GURPS creatures (472), D&D epic feats (153), D&D epic spells (70), D&D prestige classes (145), D&D epic magic items (153), D&D epic monsters (64), GURPS gear — weapons + armor
(186), GURPS advantages/disadvantages (467), GURPS skills (263), GURPS techniques (101), D&D pact-magic vestiges (31), D&D incarnum soulmelds (88). Separately labeled other editions/systems:
D&D 5e monsters (517), 5e magic items (575), 5e spells (102), AD&D 2e psionic powers (150), AD&D 2e spells (72), AD&D 2e monsters (96), GURPS 3e creatures (853), GURPS 3e spells (766), GURPS 3e items (783); WH40K Roleplay adversaries (291) + weapons (327) + armour (102) + psychic powers (242) + talents (657); WFRP 2e creatures (265) + arms & armour (107). Each has a
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
| `reference/maneuver_index.{md,json}` | `scripts/maneuver_harvest.py` | `_text\D&D 3.5e\Player Options\Tome of Battle - Book of Nine Swords.md` | 171 maneuvers/stances (170 with 3+ quick fields) | `python scripts/maneuver_harvest.py --selftest` |
| `reference/feat_index.{md,json}` | `scripts/feat_harvest.py` | bundled `feats_srd35.json` + `_md\_feats\*.md` (18 supplements) | 1253 feats / 19 books (742 typed, 962 with prerequisite) | `python scripts/feat_harvest.py --selftest` |
| `reference/spell_index.{md,json}` | `scripts/spell_harvest.py` | bundled `spells_srd35.json` (605) + Spell Compendium (982) + post-2005 splatbooks (Complete Mage 130, Complete Champion 52, Races of the Dragon 35, Dragon Magic 37) | 1841 spells / 6 books (all with school + level) | `python scripts/spell_harvest.py --selftest` |
| `reference/gurps_spell_index.{md,json}` | `scripts/gurps_magic_harvest.py` | GURPS Magic (520) + Plant Spells (19) + Thaumatology: Urban Magics (12) + Thaumatology (6) | 557 GURPS spells (541 with 3+ quick fields) | `python scripts/gurps_magic_harvest.py --selftest` |
| `reference/gurps_gear_index.{md,json}` | `scripts/gurps_gear_harvest.py` | GURPS Low-Tech Melee Weapon Table + Armor Table | 186 gear (153 weapons + 33 torso-armor pieces, TL0–TL4, DR up to 9; armor rows carry full TL/DR/cost/weight/don) | `python scripts/gurps_gear_harvest.py --selftest` |
| `reference/gurps_trait_index.{md,json}` | `scripts/gurps_trait_harvest.py` | GURPS Basic Set: Characters — Trait Lists appendix | 467 traits (276 advantages + 191 disadvantages, all with type / exotic-super / point cost / book page) | `python scripts/gurps_trait_harvest.py --selftest` |
| `reference/gurps_skill_index.{md,json}` | `scripts/gurps_skill_harvest.py` | GURPS Basic Set: Characters — Skills in the Trait Lists appendix | 263 skills (attribute, Easy/Average/Hard/Very Hard difficulty, defaults, book page; clustered on B303–B306) | `python scripts/gurps_skill_harvest.py --selftest` |
| `reference/gurps_technique_index.{md,json}` | `scripts/gurps_technique_harvest.py` | GURPS Martial Arts Technique Cheat-Sheet (born-digital text layer, characters exact) | 101 combat techniques (difficulty, prerequisite, default, maximum, damage; cinematic/silly flags) | `python scripts/gurps_technique_harvest.py --selftest` |
| `reference/vestige_index.{md,json}` | `scripts/vestige_harvest.py` | Tome of Magic (born-digital text layer) — pact-magic vestige summary | 31 vestiges (the complete list, vestige level 1–8, binding DC, special-requirement flag) | `python scripts/vestige_harvest.py --selftest` |
| `reference/soulmeld_index.{md,json}` | `scripts/soulmeld_harvest.py` | Magic of Incarnum (born-digital text layer) — soulmeld summary tables 4-1/4-2/4-3 | 88 soulmelds (classes that shape it, bindable chakras, basic effect; column-split descriptions de-interleaved) | `python scripts/soulmeld_harvest.py --selftest` |
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
  Handbook epic feats: DONE** in `epic_feat_index` (153 feats, Table 1-36). The
  `.md`/`.ocr300.md` text layers are corrupt OCR (dropped leading characters,
  Cyrillic bleed — even feat NAMES are mangled: "Deastaing Critical"), so parsing
  them was hopeless. **The fix — and the general technique for any corrupt-OCR
  source — is to render the PDF page images and read them by vision:** the real
  ELH PDF (`I:\Sourcebooks\...\Epic Level Handbook.pdf`, 11.9 MB, 334 pp, NOT a
  stub — the earlier "197 KB stub" note was an `ls` misread) has a corrupt text
  layer but perfectly legible page images. Rendered via PyMuPDF
  (`fitz`, available) at ~2.6× and read directly. The PDF Tools MCP is sandboxed
  to `C:\Users\Chad\{Documents,Downloads,Desktop}` and its own renderer is
  disabled here, so: copy the PDF into Downloads, `fitz.open(...).get_pixmap()`
  to PNG in scratchpad, then Read the PNG. This unblocks the other corrupt-OCR
  targets below. **Two tiers for fixing corrupt OCR (both built 2026-08-28):**
  (1) `scripts/reocr.py` re-OCRs a PDF with Tesseract 5.4 (render → binarize →
  OCR). It reads in visual order, so it FIXES the AD&D Monstrous Compendium's
  scrambled two-column stat blocks and is clean on PLAIN scans — but it slips on
  a few characters (`3+3`→`343`, `Very`→`Verv`), so numbers want a spot-check,
  and it still garbles ORNATE pages (the ELH). (2) VISION (render + read by eye)
  — the reliable method for ornate/decorative pages and for anything mechanical
  where a character slip can't be tolerated. Rule of thumb: plain layout →
  `reocr.py`; ornate → vision.
- **`Player Options\`** — subsystems not yet indexed: **Magic of Incarnum**
  (the soulmeld summary tables are DONE in `soulmeld_index`; the soulmeld/essentia-scaling detail text remains prose), **Tome of Magic** shadow-magic mysteries + truename utterances
  (the pact-magic VESTIGES are DONE in `vestige_index`; mysteries and utterances
  are prose-embedded spell-like blocks, not summary tables, so they need a
  body-block detector), Savage Species (monster classes), Incantatrix/variant
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

- **Robust anchor detectors handle rough `_text` fine.** The spell (school
  line + Level below), power (discipline + psionics field), maneuver (`(Type)`
  token + Level), and item (trailer / `Name:` colon) detectors all produced
  clean output from raw `_text` books — that is why MIC, DMG, XPH, ToB, the
  Spell Compendium, the splatbook spells, AND Complete Psionic all worked.
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
4. **GURPS Skills** → a new detector in `gurps_trait_harvest.py` (or its own
   `gurps_skill_harvest.py`). The Basic Set Trait Lists appendix continues past
   the advantages/disadvantages into a SKILLS list (`GURPS 4e - Basic Set -
   Characters.md`, the "Skill" column-header blocks from line ~49040 on). Its
   columns differ — Skill / difficulty (e.g. DX/E, IQ/H) / defaults / page —
   so it needs its own row signature, not the trait one. This is the last big
   native-GURPS-4e mechanics gap after traits and gear.

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
