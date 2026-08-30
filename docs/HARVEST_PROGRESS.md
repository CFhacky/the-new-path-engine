# HARVEST PROGRESS — read-first router

This is the live resume point for THE NEW PATH ENGINE reference harvest.
It records no campaign canon and never authorizes a Notion write.

## Current checkpoint

| Measure | Verified value |
|---|---:|
| Reference families | 43 |
| Accepted entries | 18,296 |
| System labels | 9 |
| Codex full-text blocks | 13,731 / 18,296 (75%) |
| Harvest base tag | `reference-2026-08-30` |
| Current verified unit | GURPS Ultra-Tech concealable ballistic armor (2026-08-30) |
| Family registry | `reference/families.json` |

The registry is the machine-readable source for family paths, accepted-entry
paths, system ownership, expected counts, and permitted citation exceptions.
Do not infer the family set from filename globs.

## Read order

1. [../AUTHORITY.md](../AUTHORITY.md) — authority and repository law.
2. [../reference/README.md](../reference/README.md) — family catalog.
3. [harvest/STATUS.md](harvest/STATUS.md) — live verified state.
4. [harvest/GAPS.md](harvest/GAPS.md) — explicit no-coverage register.
5. [harvest/ROADMAP.md](harvest/ROADMAP.md) — prioritized next work.
6. [harvest/HISTORY.md](harvest/HISTORY.md) — preserved dated ledger.
7. [harvest/OCR_REPAIRS.md](harvest/OCR_REPAIRS.md) — verified source repairs.
8. [../codex/README.md](../codex/README.md) — presentation-layer build.

## Verification

On the sourcebook machine, the official release gate is:

```powershell
python scripts\reference_audit.py --live --build-codex --report
```

That command audits the registry and accepted rows, runs every registered
harvester selftest, rebuilds the git-ignored Codex, and checks its entry count.
Source-independent checks run in GitHub Actions on every relevant push and PR.

## Working contract

- BOOK RAW only: never invent, infer, or silently repair a value.
- Every accepted row retains book provenance and a page or documented exception.
- Every non-native row has an exact `system` label.
- Missing or unusable sources print and record `NO COVERAGE`.
- Each harvester is self-contained, stdlib-only, and has `--selftest`.
- Extend existing families additively and prove prior rows are unchanged.
- Commit and push one verified family or repository unit at a time.
- Never commit `codex/build/` or sourcebook text.
- Never read from or write to Notion during repository-only harvest work.
