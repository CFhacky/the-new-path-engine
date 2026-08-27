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

**Note on the "MM3 / Draconomicon absent" queue item.** That gap is CLOSED —
both were OCR'd and `creature_index` already indexes them (MM3 = 185 blocks,
Draconomicon = 96). The earlier note in the work queue is stale.

### Related lookup scripts (retrieval, not harvest-indices)

These already give ready-to-paste RAW and do **not** need a harvest index; do
not duplicate them:

- `scripts/spell_lookup.py` — SRD 3.5 (605 spells, bundled JSON) + Spell
  Compendium (live parse). SRD wins name collisions.
- `scripts/feat_lookup.py` — SRD 3.5 (bundled JSON) + 19 supplement
  extractions under `_md\_feats\` (live parse).
- `scripts/monster_lookup.py` — `_md\_bestiary\` (live parse); shares its
  block detector's shape with `creature_harvest.py` (duplicated, not imported).

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
3. **Psionic powers** → a new `power_harvest.py` (parallel to a spell index) or
   a `power_lookup.py` (parallel to `spell_lookup.py`). Source: `_text\D&D
   3.5e\Player Options\Expanded Psionics Handbook.md` (present, 49,767 lines).
   Power block grammar: name → Discipline line → "Level:" / "Display:" /
   "Manifesting Time:" — analogous to the spell three-line test. Psionic items
   also live in the XPH and could feed `item_harvest.py`.
4. **Martial maneuvers & stances (Tome of Battle)** → `maneuver_harvest.py`.
   Source: `_text\D&D 3.5e\Player Options\Tome of Battle - Book of Nine
   Swords.md` (present, 26,121 lines). Nine disciplines; block grammar: name →
   "[Discipline] (Boost/Strike/Stance/Counter)" → "Level:" → "Initiation
   Action:" → "Range:".
5. **`term_harvest.py` extensions** (named in that script's own docstring as
   intended next Sections; their extractions exist in the corpus):
   Warhammer wargear, the PHB glossary, and the GURPS magic-item books. Each
   is a new `Section` with a `start_anchor` / `end_anchor` / `parser`.
6. **GURPS 4e Powers modifiers** → `term_harvest.py` new Section. Source:
   `_md\GURPS\GURPS 4e - Powers.md` (present, 37,745 lines) — Powers has its
   own enhancement/limitation set beyond the Basic Set.

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
  `Runestaff`. This follows the harvest-RAW discipline (the PDF is the court of
  appeal; per-entry page provenance lets anyone recover the true value). A
  future session should **not** "correct" these into the index — that would be
  inventing content the source did not cleanly yield. If Chad wants a
  normalization pass instead, that is a separate, explicitly-opted-in feature
  (e.g. an `errata` sidecar), not a silent edit of the harvest. No action
  needed unless Chad rules otherwise.

---

## LOG

- **2026-08-27** — Added `item_harvest.py`; harvested the Magic Item Compendium
  (842 items, 837 with 3+ quick fields). Handles wrapped multi-line names and
  inline `[RELIC]`/`[SYNERGY]` tags. Registered in AUTHORITY.md. Created this
  progress ledger. Confirmed `creature_index` already covers MM3 + Draconomicon
  (the stale "bestiaries absent" queue item is closed).
