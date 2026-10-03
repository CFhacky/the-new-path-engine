# d2/ — Diablo 2 item ledger (personal-campaign convenience layer)

Not canon, not book RAW, and **not part of `reference/families.json`** (Notion remains canon per `AUTHORITY.md`).
Item data is harvested from the public d2emu.com database for private tabletop use.

| File | Role |
|---|---|
| `d2emu_harvest.py` | Rebuilds `data/{unique,set,runeword}.json` from d2emu.com (stdlib only; run with no args) |
| `data/*.json` | 415 uniques, 175 set items, 99 runewords: quality, base, stats, mods, icon URL |
| `tracker_template.html` + `build_tracker.py` | Build `tracker.html`, a single offline page |
| `tracker.html` | Paper doll per holder, searchable catalog, hoard with locations and notes, JSON export/import |

Rebuild: `python3 d2/d2emu_harvest.py && python3 d2/build_tracker.py`

Notes: state lives in the browser (localStorage) — use **Export** to back it up. Slot is inferred from stat keys
(block → off-hand, damage → weapon) then base name; charms/jewels are carried, not worn. Icons hotlink d2emu.com and
are hidden if offline. Set bonuses and affix rolls inside ranges are not modelled yet.
