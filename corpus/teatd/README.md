# corpus/teatd/ — The End and the Death, Volumes I–III

The three volumes as clean markdown (one paragraph per line) plus the EPUBs
bound by `scripts/notion_novel_bind.py`. Every tool in this repository that
reads the books looks here by default:

- `scripts/teatd_realm_harvest.py` locates each realm quote in these files (`corpus-exact`).
- `scripts/verse_address.py` pins each file's edition; the maps under `reference/addresses/` are valid only against the hashes below.
- `scripts/canon_table.py` checks every witness quote inside its addressed verse here.

Expected files and their pinned editions:

| File | Book | SHA-256 | Bytes | Lines |
|---|---|---|---|---:|
| `vol1.md` | The End and the Death Volume I | `d2bcb6a30fa2593e7ef1164c5b92f03e3bf02a5aa09c9f0daf48dad8d01be185` | 900911 | 5354 |
| `vol2.md` | The End and the Death Volume II | `a1d8908f51d568a680120eae5239f2eeca18fcd52ce13658f9e3e53ab9c12fa9` | 896968 | 5688 |
| `vol3.md` | The End and the Death Volume III | `3097706ede122c262141c950ac28e5a889006ecf1fe5027864fa3b55033cdd08` | 789534 | 4489 |

Plus `The End and the Death Volume I.epub`, `… Volume II.epub`, `… Volume III.epub`.

## Rebuilding this folder from Notion (no manual file handling)

Any Claude Code session with the Notion connector can rebuild all six files
without a human moving anything. The three volumes are pages in the Horus
Heresy Source Library:

| Volume | Notion page id |
|---|---|
| I | `1f5e8214-84b0-810f-a31e-e15021ec89fc` |
| II | `1f5e8214-84b0-81c2-8d41-f86a2329b9dc` |
| III | `1f5e8214-84b0-81c0-b251-fe878a37aee3` |

Procedure (what the 2026-09-21 build did):

1. Fetch each page with the Notion `fetch` tool. The harness saves the raw
   result to disk (the tool result file); locate it under the session's
   tool-results folder and copy it to a scratch path as `volN.txt`.
2. `python scripts/notion_novel_bind.py volN.txt --md corpus/teatd/volN.md --epub "corpus/teatd/The End and the Death Volume <I|II|III>.epub"`
3. Check the markdown hashes against the table above. A match means the
   address maps under `reference/addresses/` are valid as committed; a
   mismatch means Notion's export changed and the maps must be rebuilt
   with `scripts/verse_address.py`.
4. `python scripts/teatd_realm_harvest.py` and `python scripts/canon_table.py --check`, then commit.

## Placing them by hand instead

Copy the six files sent in the build chat into this folder, then

```
sha256sum corpus/teatd/vol1.md corpus/teatd/vol2.md corpus/teatd/vol3.md
python scripts/teatd_realm_harvest.py
python scripts/canon_table.py --check
git add corpus/teatd && git commit -m "Add The End and the Death corpus" && git push
```

If a hash differs, the file is a different edition: rebuild the map with
`scripts/verse_address.py` before trusting any address.
