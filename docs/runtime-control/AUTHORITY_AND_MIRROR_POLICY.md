# Runtime-Control Authority and Mirror Policy

**Version:** 1.0.0

This policy adds a runtime-control documentation layer without turning GitHub into campaign canon.

## Ownership split

| Surface | Owns | Does not own |
|---|---|---|
| Notion | live campaign state, current resume cards, canon, current protocol mirrors | executable code |
| Vault mirror | local readable mirror of authorized Notion pages | authority over newer Notion state |
| Engine `docs/runtime-control/` | stable schemas, validation contracts, and ratified operating text | current lane facts |
| Engine `scripts/` | deterministic validation/mechanics | canon or cross-session truth |
| Engine `mirrors/notion/` | immutable dated exports for recovery and audit | live authority; script input |

## Stable documents

`PLAY_CONTRACT.md` and `RESUME_CARD_SCHEMA.md` are stable tool documents. Their GitHub text is the editable source for a versioned revision; the corresponding Notion pages are the operational campaign mirrors. A revision is complete only when both surfaces agree and the mirror manifest records the Notion pages.

Chad's live instruction and newer Notion authority still outrank the repository.

## Installed Notion controls

- Runtime hub: `3c4e8214-84b0-8149-87e1-cc411466bfe7`
- Play Contract: `3c4e8214-84b0-818f-93c0-df1da2e52043`
- Resume Router: `3c4e8214-84b0-8106-ae12-f50082ed43ff`
- Resume Schema: `3c4e8214-84b0-81dc-b0ae-eaf6ebb9bb48`

## Dated state mirrors

The repository's general “no campaign facts” law remains in force everywhere except `mirrors/notion/`.

Files beneath `mirrors/notion/` must:

- be immutable and dated;
- declare `NON-AUTHORITATIVE MIRROR`;
- cite the source Notion page(s) and export date;
- never be imported or read by resolver scripts as state;
- never use an undated `current` filename;
- remain available only for recovery, audit, and diffing.

If a mirror and Notion disagree, Notion wins. Fix the next export; do not edit canon to match the snapshot.

## Why the current resume is not a GitHub file

A mutable `current-resume.md` would become a second state store and eventually open a session from stale data. The current resume therefore lives in Notion and the vault mirror. GitHub receives dated snapshots only.

## Mirroring checklist

1. Fetch the Notion page immediately before export.
2. Record page ID, title, version, and export date.
3. Validate the resume format.
4. Commit the dated snapshot and manifest together.
5. Link the GitHub commit/PR from the Notion hub or Canon Change Log.
6. Never describe a GitHub snapshot as current without re-fetching Notion.
