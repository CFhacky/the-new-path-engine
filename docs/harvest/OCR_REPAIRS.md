# OCR REPAIRS — hand-verified corrections to the source extractions

**Why this file exists.** Chad directed (2026-08-27) that garbled OCR and garbled
index entries be repaired by hand, not left as raw junk. This is a deliberate
exception to the harvest-RAW default recorded in [HISTORY.md](HISTORY.md)
(the former "NEEDS CHAD" note), now authorized. **Every repair here is verified against
the source's own surviving text — the creature/spell description, class, level,
and page — never guessed.** Where a garbled entry cannot be resolved from the
source with certainty, it is FLAGGED below, not invented.

**Two kinds of repair:**
1. **Source OCR fix** — the extraction `.md` on `I:\Sourcebooks` had a garbled
   name line; the line was corrected in place (verify-then-replace), so every
   future harvest of that book is clean. Logged here because `I:\Sourcebooks`
   is not version-controlled; this log is the record and the re-apply list if a
   book is ever re-OCR'd.
2. **Detector fix** — the name was fine in the source but the harvest script
   grabbed the wrong line (a field or NPC line). Fixed in the script; no source
   edit.

---

## 2026-08-27 — Expanded Psionics Handbook (source OCR fixes)

File: `I:\Sourcebooks\_text\D&D 3.5e\Player Options\Expanded Psionics Handbook.md`
Nine power NAME lines were OCR-mangled. Each corrected to the true power,
verified from the block's own class / level / description:

| Line | Was | Now | Verified by |
|---|---|---|---|
| 12611 | `30dy Equilibrium` | `Body Equilibrium` | Psychometabolism power; "Bo"→"30" |
| 12709 | `3rain Lock` | `Brain Lock` | Telepathy (Compulsion) power; "B"→"3" |
| 15501 | `imensional Anchor, Psionic` | `Dimensional Anchor, Psionic` | Psychoportation; dropped leading "D" |
| 17087 | `yy` | `Energy Ball` | p.100, Psychokinesis [see text], Kineticist 4; desc = energy explosion (choose cold/electricity/fire/sonic, 7d6, 20-ft radius), garbled echo "cnere Dall" |
| 20116 | `on Body, Psionic` | `Iron Body, Psionic` | p.113, Metacreativity; desc = "As iron body (PH p.245)…"; dropped "Ir" |
| 24674 | `stomp` | `Stomp` | Psychokinesis power; lowercase "s" |
| 25400 | `lemporal Acceleration` | `Temporal Acceleration` | Psychoportation, Psion/wilder 6; "T"→"l" |
| 25971 | `ue Creation` | `True Creation` | Metacreativity, Shaper 9; desc = "As psionic major creation, except… enduring"; "Tr"→"ue" |
| 25987 | `ue Metabolism` | `True Metabolism` | Psychometabolism, Psion/wilder 8; "Tr"→"ue" |

`power_index` was rebuilt after the fix; all nine names are now correct and a
full re-scan of the 409 power names shows no remaining garble.

## 2026-08-27 — feat_harvest.py (detector fix, no source edit)

`plausible_feat_name` now rejects a candidate that contains a mid-name colon
(a stat/field line grabbed as a feat — "Level: 12th", "Special Requirement:
Knowledge") or an NPC descriptor ("Kobold, 1st level"). This removed 8
non-feat rows from `feat_index` (1253 → 1244) with no loss of real feats.

## 2026-08-29 — GURPS Basic Set trait roster (detector fix, no source edit)

Files:

- `I:\Sourcebooks\_text\GURPS\GURPS 4e\GURPS 4e - Basic Set - Characters.md`
- `I:\Sourcebooks\GURPS\GURPS 4e\GURPS 4e - Basic Set - Characters.pdf`

The Trait Lists repeat the singular word `Advantage` as a *column heading* on
both the ADVANTAGES and DISADVANTAGES pages. The old detector treated every
such column label as a section change. Negative costs later forced most affected
rows back to `disadvantage`, masking the defect; the twelve printed
`Variable` rows on PDF p.302 exposed it.

The detector now changes state only on the plural section titles. The original
PDF's word coordinates and the extraction's all-caps `DISADVANTAGES` title
verify the result. Ten existing rows are corrected from advantage to
disadvantage: Neurological Disorder, No Legs, Pacifism, Secret Identity, Sleepy,
Supernatural Features, Susceptible, Unnatural Features, Vulnerability, and
Weakness. The negative-side Reputation and Wealth rows are also restored; their
positive-side rows remain. Every affected cost stays the book's printed
`Variable` — no value was inferred from prose.

## 2026-08-29 — GURPS Basic Set skill roster (detector fixes, no source edit)

File: `I:\Sourcebooks\_text\GURPS\GURPS 4e\GURPS 4e - Basic Set - Characters.md`

Four Trait Lists rows put the second half of the skill name *after* the Page
cell. The old detector therefore indexed a truncated name, lost the `/TL` flag,
and admitted that trailing name fragment (plus, for Electronics, the following
row) into `defaults`. The same book's description heading and Defaults line
verify every correction:

| Old row | Verified row | Verified defaults | Book page |
|---|---|---|---|
| `Computer` | `Computer Operation/TL` | `IQ-4` | B184 |
| `Electronics` | `Electronics Operation/TL` | `IQ-5, Electronics Repair (same)-5, Engineer (Electronics)-5` | B189 |
| `Hazardous` | `Hazardous Materials/TL` | `IQ-5` | B199 |
| `Intelligence` | `Intelligence Analysis/TL` | `IQ-6, Strategy (any)-6` | B201 |

`gurps_skill_harvest.py` now applies those four exact detector-level repairs;
the extraction file remains untouched. All four rows are correctly marked as
tech-level skills.

## 2026-08-29 — Epic Level Handbook epic feats (derived OCR source)

File: `I:\Sourcebooks\_text\D&D 3.5e\DM Toolkits\Epic Level Handbook.epic-feats.ocr-columns.md`

This is reproducible source generation, not a hand-repair of body text.
`epic_feat_harvest.py --extract-source` renders ELH pp.50-69 at 4× and OCRs
each visual column separately. The **149 body blocks remain raw Tesseract
output**. Only their headings are restored from the book-verified Table 1-36
names plus Dire Charge on p.53, so future harvests have stable, name-leading
span anchors. The generated file's SHA-256 is recorded in the JSON index.

Five descriptions dependent on the truly blurred p.60 page image are not
written to the derived source: Improved Spell Capacity, Improved Spell
Resistance, Improved Stunning Fist, Improved Whirlwind Attack, and Incite Rage.
They remain explicit `NO COVERAGE`; no OCR body value was guessed or repaired.

## 2026-08-29 — Epic Level Handbook epic items (derived OCR source)

File: `I:\Sourcebooks\_text\D&D 3.5e\DM Toolkits\Epic Level Handbook.epic-items.ocr-columns.md`

This is reproducible source generation, not hand-repaired body text.
`epic_item_harvest.py --extract-source` renders ELH pp.126-146 at 4× and OCRs
both visual columns independently. All **103 description bodies remain raw
Tesseract output**; only their headings are restored from the existing
book-verified 153-row transcription. Variant rows share the book's single
common block. Verified lane cutovers skip nine intervening generation tables
that the physical layout places above a continuation column. The JSON index
records the generated file's SHA-256; no OCR mechanic was guessed or rewritten.

## 2026-08-29 — Epic Level Handbook epic spells (derived OCR source)

File: `I:\Sourcebooks\_text\D&D 3.5e\DM Toolkits\Epic Level Handbook.epic-spells.ocr-columns.md`

This is reproducible source generation, not hand-repaired body text.
`epic_spell_harvest.py --extract-source` renders ELH pp.74-88 and 92-102 at 4×
and OCRs both visual columns independently. All **70 description bodies** (46
sample spells plus 24 seeds) remain raw Tesseract output; only their headings
are restored from the existing book-verified transcription. Verified lane
cutovers retain mechanically related “another use” boxes while excluding
unrelated inset examples and the following epic-psionics section. The JSON
index records the generated file's SHA-256; no OCR mechanic was guessed or
rewritten.

## 2026-08-29 — Epic Level Handbook epic monsters (derived OCR source)

File: `I:\Sourcebooks\_text\D&D 3.5e\DM Toolkits\Epic Level Handbook.epic-monsters.ocr-columns.md`

This is reproducible source generation, not hand-repaired body text.
`epic_monster_harvest.py --extract-source` renders ELH pp.158-230 at 4× and
OCRs both visual columns independently. All **50 shared description bodies**
remain raw Tesseract output; only their headings are restored from the existing
book-verified 64-row transcription. Printed variants share the book's single
common block. One Hunefer/Lavawight boundary whose two OCR rows have the same
vertical coordinate is split by their stable OCR row order, preserving both
raw lines without rewriting either. Two complete generations produced the same
SHA-256, which the JSON index records; no OCR mechanic was guessed or repaired.

## 2026-08-29 — GURPS Martial Arts cheat-sheet wrapped names (parser repair)

File: `I:\Sourcebooks\_text\GURPS\GURPS 4e\GURPS 4e - Martial Arts - Techniques Cheat Sheet.md`

No source text was edited. The born-digital table dumps several technique names
over two or three lines, but the old detector treated only the line immediately
before the difficulty cell as the name. It therefore emitted 13 fragments:
`Attack`, `Attack (Bow)`, `Defense`, `Kick`, `Lock`, `Parry`, `Punch`,
`Ranged`, `Riding`, `Seated`, `Strike`, `Wedgie`, and `or Throw`.
The detector now reconstructs the complete name from every non-furniture line
between the preceding row's Page cell and the current Difficulty cell. This is
a structural parse of the exact text layer, not a guessed spelling or value.
It yields all 113 printed rows / 112 unique techniques and collapses only the
book's repeated Lower-Body Arm Lock row. The selftest locks every restored name
and forbids all 13 fragments.

---

## FLAGGED — not yet resolved (need PDF page verification; NOT guessed)

Five creature NAME lines in the `_md\_bestiary` extractions are OCR-fragmented
to three letters, and the surrounding `.md` text does not carry enough to
recover the true name with certainty. They are left as-is rather than invented.
Resolving them needs the source PDF (the `.md` page marker and the PDF page may
be offset, so each must be located visually):

| Index name | Book | md page | Stat clues |
|---|---|---|---|
| `Lal` | Epic Level Handbook | 220 | CR 24, Gargantuan Magical Beast |
| `Bla` | Epic Level Handbook | 224 | ~38 HD |
| `Olg` | MM2 | 101 | CR 12, Large Giant, 136 hp; OCR context "FIRE"/"OLG" |
| `Gre` | MM2 | 121 | CR 3, Medium aberration |
| `Evi` | MM3 | 161 | CR 12, Construct, 112 hp |

Not garbled (checked, correct as-is): the DMG "`Ram`" is Ring of the Ram listed
by property (like "Protection" = Ring of Protection); short creatures like Imp,
Roc, Ape, Bat; the feat "Run"; the GURPS spell "Dye"; and the title-cased NPC
sample entries ("4Th-Level Ranger").
