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

---

## DONE — reference indices built

| Reference file | Built by | Source(s) | Count | Selftest |
|---|---|---|---|---|
| `reference/terms_and_affixes.{md,json}` | `scripts/term_harvest.py` | DMG v3.5 weapon (pp.223–226) + armor/shield (pp.218–219) special abilities; GURPS 4e Basic Set enhancements (B102) + limitations (B110) | 4 sections | `python scripts/term_harvest.py --selftest` |
| `reference/creature_index.{md,json}` | `scripts/creature_harvest.py` | `_md\_bestiary\*.md` — MM1–MM5, Draconomicon, Epic Level Handbook, FC1, FC2, Fiend Folio, Libris Mortis, Lords of Madness | 1509 stat blocks / 12 books | `python scripts/creature_harvest.py --selftest` |
| `reference/magic_item_index.{md,json}` | `scripts/item_harvest.py` | `_text\D&D 3.5e\Magic and Items\Magic Item Compendium.md` | 842 items (837 with 3+ quick fields) | `python scripts/item_harvest.py --selftest` |
| `reference/power_index.{md,json}` | `scripts/power_harvest.py` | `_text\D&D 3.5e\Player Options\Expanded Psionics Handbook.md` | 281 powers (all with 3+ quick fields) | `python scripts/power_harvest.py --selftest` |
| `reference/maneuver_index.{md,json}` | `scripts/maneuver_harvest.py` | `_text\D&D 3.5e\Player Options\Tome of Battle - Book of Nine Swords.md` | 171 maneuvers/stances (170 with 3+ quick fields) | `python scripts/maneuver_harvest.py --selftest` |
| `reference/feat_index.{md,json}` | `scripts/feat_harvest.py` | bundled `feats_srd35.json` + `_md\_feats\*.md` (18 supplements) | 1253 feats / 19 books (742 typed, 962 with prerequisite) | `python scripts/feat_harvest.py --selftest` |

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
  Compendium (live parse). SRD wins name collisions. (No spell harvest index
  yet — a candidate; see NEXT.)
- `scripts/feat_lookup.py` — SRD 3.5 (bundled JSON) + supplement extractions
  under `_md\_feats\` (live parse). Its index sibling is `feat_harvest.py`.
- `scripts/monster_lookup.py` — `_md\_bestiary\` (live parse); its index
  sibling is `creature_harvest.py` (detector duplicated, not imported).

---

## NEXT — queued harvest targets (in priority order)

All source OCR listed below was verified present on `I:\Sourcebooks` on
2026-08-27. Each is a *new detector/section*, not new OCR.

1. **DMG v3.5 magic items** → extend `item_harvest.py` with a `dmg` detector.
   Source: `_text\D&D 3.5e\Core\Dungeon Masters Guide v3.5.md` (present, 53,566
   lines). Grammar differs from the MIC: the DMG lists Caster Level /
   Prerequisites / Market Price / Weight at the END of each item description,
   not the top, and groups items under type headers (Rings, Rods, Staffs,
   Wands, Wondrous Items). Add a `Source(key="dmg", ..., detector="dmg")` to
   `SOURCES` and a `detect_dmg` in `DETECTORS`. This closes the biggest item
   gap — the "generic" items everyone knows (Ring of Protection, Staff of
   Fire, Boots of Speed, etc.).
2. **Arms & Equipment Guide (3.0) items** → `item_harvest.py` `aeg` detector.
   Source: `_text\D&D 3.0\Arms And Equipment Guide.md` (present, 22,767 lines).
3. **`term_harvest.py` extensions** (named in that script's own docstring as
   intended next Sections; their extractions exist in the corpus):
   Warhammer wargear, the PHB glossary, and the GURPS magic-item books. Each
   is a new `Section` with a `start_anchor` / `end_anchor` / `parser`.
4. **GURPS 4e Powers modifiers** → `term_harvest.py` new Section. Source:
   `_md\GURPS\GURPS 4e - Powers.md` (present, 37,745 lines) — Powers has its
   own enhancement/limitation set beyond the Basic Set.
5. **Spell index / supplemental spells** → a `spell_harvest.py` mirroring the
   others. `spell_lookup.py` already retrieves SRD + Spell Compendium, but
   there is no browsable spell *index*, and supplement spell lists (the
   Complete series, Races of the Dragon, etc. under `_md\_feats\` and
   `_text\D&D 3.5e\Player Options\`) are not collated. The Spell Compendium's
   header grammar (name / school / `Level:`) is already parsed by
   `spell_lookup._is_header` and can be duplicated into a harvest.

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
