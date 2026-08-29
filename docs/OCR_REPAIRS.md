# OCR REPAIRS — hand-verified corrections to the source extractions

**Why this file exists.** Chad directed (2026-08-27) that garbled OCR and garbled
index entries be repaired by hand, not left as raw junk. This is a deliberate
exception to the harvest-RAW default in [HARVEST_PROGRESS.md](HARVEST_PROGRESS.md)
(the "NEEDS CHAD" note), now authorized. **Every repair here is verified against
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
