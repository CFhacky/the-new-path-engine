# Runtime Control Layer

This folder governs the boundary between live campaign state and the mechanics engine.

## Read order

1. `PLAY_CONTRACT.md` — binding live-play behavior.
2. `RESUME_CARD_SCHEMA.md` — required shape and maintenance of lane resumes.
3. `AUTHORITY_AND_MIRROR_POLICY.md` — why current state stays in Notion and GitHub stores dated exports only.
4. `NOTION_INSTALLATION.md` — installed page IDs, router wiring, and mirror destinations.

## Runtime surfaces

- **Notion hub:** [The New Path Engine — Runtime Control Layer](https://app.notion.com/p/3c4e821484b0814987e1cc411466bfe7)
- **Current resumes:** [Campaign Resume Router — Current Lanes](https://app.notion.com/p/3c4e821484b08106ae12f50082ed43ff) and its lane-card children
- **Live-play governance:** [The New Path Play Contract — Live Session Governance](https://app.notion.com/p/3c4e821484b0818f93c0df1da2e52043)
- **Resume schema:** [Campaign Resume Card Schema and Maintenance](https://app.notion.com/p/3c4e821484b081dcb0aeeaf6ebb9bb48)
- **Validation:** `python scripts/resume_card.py --check <snapshot.md>`

No file in this folder contains current campaign state. Dated state exports are quarantined beneath `mirrors/notion/`.
