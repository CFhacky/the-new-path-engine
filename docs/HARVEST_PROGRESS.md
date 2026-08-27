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

**At a glance (2026-08-27).** Seven reference index families, ~6,200 entries:
terms/affixes (143), creatures (1509), magic items (1058), psionic powers
(281), martial maneuvers (171), feats (1253), spells (1804). Each has a
`--selftest` that passes. Run any `scripts/*_harvest.py` with no args to
rebuild its index.

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
| `reference/creature_index.{md,json}` | `scripts/creature_harvest.py` | `_md\_bestiary\*.md` — MM1–MM5, Draconomicon, Epic Level Handbook, FC1, FC2, Fiend Folio, Libris Mortis, Lords of Madness | 1509 stat blocks / 12 books | `python scripts/creature_harvest.py --selftest` |
| `reference/magic_item_index.{md,json}` | `scripts/item_harvest.py` | Magic Item Compendium (842) + DMG v3.5 specific/wondrous items (216) | 1058 items / 2 sources (982 with 3+ quick fields) | `python scripts/item_harvest.py --selftest` |
| `reference/power_index.{md,json}` | `scripts/power_harvest.py` | `_text\D&D 3.5e\Player Options\Expanded Psionics Handbook.md` | 281 powers (all with 3+ quick fields) | `python scripts/power_harvest.py --selftest` |
| `reference/maneuver_index.{md,json}` | `scripts/maneuver_harvest.py` | `_text\D&D 3.5e\Player Options\Tome of Battle - Book of Nine Swords.md` | 171 maneuvers/stances (170 with 3+ quick fields) | `python scripts/maneuver_harvest.py --selftest` |
| `reference/feat_index.{md,json}` | `scripts/feat_harvest.py` | bundled `feats_srd35.json` + `_md\_feats\*.md` (18 supplements) | 1253 feats / 19 books (742 typed, 962 with prerequisite) | `python scripts/feat_harvest.py --selftest` |
| `reference/spell_index.{md,json}` | `scripts/spell_harvest.py` | bundled `spells_srd35.json` (605) + Spell Compendium (982) + post-2005 splatbooks (Complete Mage 130, Complete Champion 52, Races of the Dragon 35) | 1804 spells / 5 books (all with school + level) | `python scripts/spell_harvest.py --selftest` |

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
| D&D 5e | 35 | none (wrong edition for a 3.5/GURPS game — low priority) |
| AD&D | 19 | none (older edition — low priority) |
| GURPS (3e+4e) | 478 | Basic Set + Powers modifiers only (`term_harvest`) — the GURPS side is barely touched |
| Warhammer | 489 | none here (the `corpus-mass-translator` skill owns Warhammer conversion) |
| Dragon Magazine | 446 | none (mixed crunch/articles — needs a crunch-only detector) |
| Forgotten Realms | 71 | none (setting + some crunch) |
| Other RPG systems | 8 | none |
| **`_text` total** | **1,714** | — |

Highest-value UNHARVESTED 3.5e content, by directory (all under
`_text\D&D 3.5e\`), that the existing scripts can absorb by adding sources:

- **`Monsters and Fiends\`** — bestiaries BEYOND the `_md\_bestiary` twelve:
  **Book of Vile Darkness**, **Book of Exalted Deeds**, **Deities and
  Demigods**, **Monsters of the Planes**. (Draconomicon, Fiend Folio, FC1/FC2,
  Libris Mortis, Lords of Madness here are duplicates of the harvested set.)
  → extend `creature_harvest.py` to a second source directory, deduping by book.
- **`DM Toolkits\`** — Epic Level Handbook (epic feats/spells/items — creatures
  already indexed), Elder Evils, Exemplars of Evil (more stat blocks), Manual of
  the Planes, Planar Handbook, Stronghold Builders Guidebook.
- **`Player Options\`** — subsystems not yet indexed: **Magic of Incarnum**
  (soulmelds), **Tome of Magic** (pact/shadow/truename magic), Savage Species
  (monster classes), Incantatrix/variant material in Unearthed Arcana. The
  Complete-series and Races-of books' feats are already in `feat_index`; their
  pre-2005 spells are already in the Spell Compendium.
- **`Magic and Items\`** — Tome of Feats (3pp, more feats).

GURPS 4e mechanics worth harvesting (in `_text\GURPS\GURPS 4e\`, 478 files
total): GURPS Magic (spell list), GURPS creature books (bestiary lines),
GURPS Fantasy/Dungeon Fantasy gear and templates. These need GURPS-format
detectors, not the D&D ones.

## NEXT — queued harvest targets (in priority order)

All source OCR listed below was verified present on `I:\Sourcebooks` on
2026-08-27. Each is a *new detector/section*, not new OCR.

1. **Arms & Equipment Guide (3.0) items** → `item_harvest.py` `aeg` detector.
   Source: `_text\D&D 3.0\Arms And Equipment Guide.md` (present, 22,767 lines).
2. **`term_harvest.py` extensions** (named in that script's own docstring as
   intended next Sections; their extractions exist in the corpus):
   Warhammer wargear, the PHB glossary, and the GURPS magic-item books. Each
   is a new `Section` with a `start_anchor` / `end_anchor` / `parser`.
3. **More supplemental spells** → add sources to `spell_harvest.py`. The core
   splatbooks are now DONE (Complete Mage, Complete Champion, Races of the
   Dragon — all validated clean and clustered in their spell chapters). What
   remains is lower-value / needs-work:
   - **PHB2** and **Complete Scoundrel** yield 0 with `detect_compendium` — a
     different spell-block format (no ALL-CAPS name / school / `Level:` triple).
     Would need a format-specific detector.
   - Other post-2005 books (Complete Arcane is PRE-2005 and already in the
     Compendium; check publication date before adding — pre-2005 = skip).
   - When adding any book: run it, confirm 0 header-polluted names and that the
     hits cluster in the spell chapter (not scattered), then keep it.
     `HEADER_REJECT` now catches the generic SPELLS / INVOCATIONS / DESCRIPTIONS
     / CHAPTER running-header words, so most books need no per-book header work.

### How to add a source (the pattern, do not deviate)

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

- **(Logged, non-blocking) Raw-OCR fidelity vs. obvious fixes.** The harvest
  deliberately keeps obvious OCR misreads verbatim — e.g. a caster level read
  as `sth` for `5th`, an em-dash rendered as `�`, a name like `Runestatf` for
  `Runestaff`, and psionic power names like `30dy Equilibrium` for `Body
  Equilibrium` or a wholly illegible `yy` (a real Kineticist-4 power whose name
  line the OCR could not resolve — kept, because dropping it would lose a real
  power, and its page provenance recovers the name). This follows the
  harvest-RAW discipline (the PDF is the court of
  appeal; per-entry page provenance lets anyone recover the true value). A
  future session should **not** "correct" these into the index — that would be
  inventing content the source did not cleanly yield. If Chad wants a
  normalization pass instead, that is a separate, explicitly-opted-in feature
  (e.g. an `errata` sidecar), not a silent edit of the harvest. No action
  needed unless Chad rules otherwise.

---

## LOG

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
