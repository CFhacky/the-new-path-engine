# Harvest status

Verified 2026-08-30. This is the live human summary; the enforceable family
inventory is [../../reference/families.json](../../reference/families.json).

## Accepted mechanical entries

| System label | Entries |
|---|---:|
| D&D 3.5e | 7,440 |
| GURPS 4e | 2,151 |
| GURPS 3e | 2,402 |
| D&D 5e | 1,194 |
| AD&D 2e | 318 |
| WH40K Roleplay | 3,319 |
| WFRP | 877 |
| WH40K | 136 |
| WHFB | 291 |
| **Total** | **18,128** |

There are 41 registered families. Native D&D 3.5e and GURPS 4e rows remain
separate from every labeled edition or game line. The shared terms family
contains explicit D&D 3.5e and GURPS 4e rows rather than an unlabeled blend.
The native magic-item family now holds 1,454 entries, including 34 table-first
DMG rods and staffs joined directly to Tables 7-19/7-25 and their descriptions.

## Codex presentation coverage

The verified Codex build contains all 18,128 accepted entries and attaches
13,282 validated full-text blocks (73.3%). Missing full text affects the
presentation layer only; it does not remove already-harvested mechanical fields.

Current complete full-text families include spells, soulmelds, vestiges,
maneuvers, epic items/monsters/spells, and native GURPS gear, skills, traits,
techniques, and spells. Several labeled legacy or equipment families retain
lower prose coverage; see [GAPS.md](GAPS.md).

The built files under `codex/build/` embed sourcebook text and are intentionally
git-ignored. Rebuild them from the external corpus; never commit them.

## Repository map

| Path | Ownership |
|---|---|
| `scripts/*_harvest.py` | one self-contained extractor per family |
| `reference/families.json` | canonical registry and locked counts |
| `reference/*_index.json` | machine-readable generated mechanics |
| `reference/*_index.md` | human-readable generated mechanics |
| `scripts/reference_audit.py` | repository-wide integrity and release gate |
| `codex/` | downstream searchable presentation layer |
| `docs/harvest/` | live status, gaps, roadmap, history, OCR repair log |

## Verified release commands

Source-independent:

```powershell
python scripts\reference_audit.py
python scripts\reference_audit.py --selftest
python codex\build_codex.py --selftest
python -m unittest discover -s tests -p "test_*.py" -v
```

Full source-machine gate:

```powershell
python scripts\reference_audit.py --live --build-codex --report
```

Expected terminal summaries are `REFERENCE_AUDIT families=41 rows=18128
errors=0`, `LIVE_SELFTESTS total=41 failed=0`, and a Codex build of 18,128
entries with 13,282 full-text blocks.
