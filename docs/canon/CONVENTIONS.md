# Canon conventions — the four layers

| Layer | Origin | Here |
|---|---|---|
| Address | Langton's chapters (c. 1205), Estienne's verses (1551): a dumb grid, portable across editions once the edition is fixed | `scripts/verse_address.py` → `reference/addresses/*.address.json`; `KEY ch:verse ¶n`; SHA-256 pinned |
| Sense unit | Masoretic paragraphs, Greek *kephalaia*, the lectionary pericope named by its incipit | one unit per verse heading, with title and incipit in the map |
| Narrator | "according to Matthew"; psalm superscriptions; red-letter editions | `narrator` and `mode` on every witness in `reference/canon/events.json` (first / second / close-third / omniscient / hearsay) |
| Event concordance | Eusebius's canon tables (c. 320): same event, every gospel, accounts kept separate; Kings' regnal synchronisms | `scripts/canon_table.py` → `README.md` table + one page per event; `synchronism` is only what the verse states |

Rules the tooling enforces:

- An address that does not resolve to a unit of the pinned edition is an error, not a guess.
- A quote that is not found inside its addressed unit is an error when the corpus is present.
- Witnesses are never merged. A death told three ways gets three rows and a disagreements note.
- No absolute calendar. The published chronology is disputed; the table carries relative markers ("afterwards", "over a period of eight hours") and nothing else.
- Narrator and mode are the registry author's reading and are labelled INFERRED on every event page.
