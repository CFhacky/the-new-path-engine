# Notion Installation — Runtime Control Layer

**Installed:** 2026-08-22  
**GitHub repository:** `CFhacky/the-new-path-engine`

## Control pages

| Role | Notion page | ID |
|---|---|---|
| Runtime-control hub | [The New Path Engine — Runtime Control Layer](https://app.notion.com/p/3c4e821484b0814987e1cc411466bfe7) | `3c4e8214-84b0-8149-87e1-cc411466bfe7` |
| Live-play contract | [The New Path Play Contract — Live Session Governance](https://app.notion.com/p/3c4e821484b0818f93c0df1da2e52043) | `3c4e8214-84b0-818f-93c0-df1da2e52043` |
| Current resume router | [Campaign Resume Router — Current Lanes](https://app.notion.com/p/3c4e821484b08106ae12f50082ed43ff) | `3c4e8214-84b0-8106-ae12-f50082ed43ff` |
| Resume schema | [Campaign Resume Card Schema and Maintenance](https://app.notion.com/p/3c4e821484b081dcb0aeeaf6ebb9bb48) | `3c4e8214-84b0-81dc-b0ae-eaf6ebb9bb48` |

## Current lane cards

| Lane | ID |
|---|---|
| Arik — Avernus, Day 7 Hammer 1495 DR | `3c4e8214-84b0-8113-9b27-d87512bc22d9` |
| Shi'van — Waterdeep, Day 911 · 6 Mirtul 1494 DR | `3c4e8214-84b0-81ac-81a6-c4cb404dc254` |
| Jörmun — Eastern Anauroch, ~Uktar 1, 1498 DR | `3c4e8214-84b0-81c8-adc6-d19d1313f7a7` |
| Drazekh — Old World, Day 15, Iron Rock corridor | `3c4e8214-84b0-8134-a1f3-fb23fea5f3d5` |
| Cross-Lane Ledger — Awards, Recovery Debt & Routing Gaps | `3c4e8214-84b0-818e-8deb-eaf28bc17148` |

## Existing routers wired

- `Campaign Router — Master Index` (`388e8214-84b0-81ad-9acc-e6b3dd09f790`)
- `Campaign Lane Router — Current State Authority` (`388e8214-84b0-81c3-8768-c95147c11b31`)
- `Session Operations Router — Start / Play / End Authority` (`388e8214-84b0-81bd-8fe2-dae92dc6ba28`)

The Lane Router was also corrected to the exact Arik Day-7 freeze, the Jörmun parley ruling gate, and the Drazekh Day-15 S31 freeze.

## Mirror destination

Current state remains in Notion. Explicit checkpoints export a dated, immutable bundle to:

`mirrors/notion/YYYY-MM-DD/`

Scripts must never read those mirrors as current state.
