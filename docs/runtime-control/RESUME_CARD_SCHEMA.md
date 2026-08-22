# Campaign Resume Card Schema and Maintenance

**Notion operational mirror:** https://app.notion.com/p/3c4e821484b081dcb0aeeaf6ebb9bb48  

**Version:** 1.0.0

A resume card is a compact recovery surface for one campaign lane. It is not canon and does not replace the lane's current-state, session-log, or recovery authorities. Its job is to make those authorities fast to locate and to preserve the exact playable freeze.

## Canonical placement

- **Current mutable resume:** Notion, beneath `Campaign Resume Router — Current Lanes`.
- **Vault mirror:** produced by the normal Notion-to-vault mirror process.
- **GitHub:** dated read-only exports only, beneath `mirrors/notion/YYYY-MM-DD/`.
- **Never:** an undated `current.md` in GitHub.

## Required frontmatter for a GitHub snapshot

```yaml
---
name: campaign-resumes-all-lanes-YYYY-MM-DD
type: notion-mirror-snapshot
authority: NON-AUTHORITATIVE MIRROR
snapshot_date: YYYY-MM-DD
source_notion: <Notion URL or page ID>
scope: <lanes covered>
---
```

The file must also contain the phrase **NON-AUTHORITATIVE MIRROR** above the first lane card.

## Required fields for every lane card

Use one `##` heading per lane and these exact bold labels:

1. **Snapshot authority.** Names the controlling pages checked and the date of the check.
2. **Position.** The current physical/temporal position and advancement state needed to resume.
3. **Last canonical close.** The last fully recorded close; distinguish interrupted/recovery closes.
4. **Exact resume point.** The first unplayed beat. State what has *not* happened.
5. **Rulings required before boot.** Write `None` when no ruling is owed.
6. **Due at boot.** Triggered machinery that must fire before new content; write `None` when empty.
7. **Open machinery.** Near clocks, active threads, and consequences that are not yet due.
8. **Hard prohibitions.** Knowledge limits, no-rerun rules, protected choices, and invalid routes.
9. **Delegated / background operations.** NPC-led modules and off-screen institutions that may proceed without forcing PC attention.
10. **Record debt / stale pointers.** Missing logs, uncashed thresholds, stale routers, and archive-close debt.
11. **Boot line.** One copy-ready line or fenced block that routes to the real authorities.
12. **Freshness invalidators.** Events that make the card stale: any session close, ruling resolution, clock crossing, or current-state rewrite named here.

## Cross-lane ledger

The all-lanes index ends with `## CROSS-LANE LEDGER` and records only shared maintenance:

- advancement awards owed;
- close-from-archive queue;
- cross-lane bridge rulings;
- shared routing/tool defects;
- current delegated economic or institutional modules that touch more than one lane.

It does not duplicate each lane's full machinery.

## Update protocol

At a normal session close:

1. update the lane's Notion resume card after the session log and Canon Change Log are written;
2. update the exact freeze, due machinery, record debt, and boot line;
3. update the Resume Router's one-line summary;
4. update the Campaign Lane Router only when its pointer/clock actually changed;
5. mirror Notion to the vault.

At an explicit GitHub mirror checkpoint:

1. export the current Resume Router and lane cards into one dated Markdown snapshot;
2. mark it `NON-AUTHORITATIVE MIRROR`;
3. validate it with `python scripts/resume_card.py --check <file>`;
4. add or update the mirror manifest with Notion page IDs and export date;
5. never overwrite an older snapshot.

## Freshness law

A resume card is stale immediately when any of the following occurs:

- the lane advances in played text;
- a pre-boot ruling is decided;
- a due die or mandatory clock fires;
- a recovery close is installed;
- a named current-state, boot, or latest-pointer page is rewritten;
- the card's own `Freshness invalidators` condition is met.

A stale card remains useful provenance, but it cannot open play.
