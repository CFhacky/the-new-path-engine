# AUTHORITY — read this before using anything in this repository

This repository is the MECHANICS and RUNTIME-CONTROL layer of The New Path campaign engine. It is less authoritative than Chad's instruction, live Notion, and ratified campaign procedure. If anything here conflicts with those authorities, this repository is wrong.

## The authority order (binding)

1. **Chad's live instruction** — outranks everything.
2. **Notion** — campaign canon, current lane state, current resume cards, registers, session prose, and the Canon Change Log. Fetch live before asserting state.
3. **Skill and protocol files** — procedure: when engines fire, session lifecycle, prose law, and arc routing.
4. **Stable runtime-control documents in this repository** — the live-play contract, resume schema, validation rules, and mirror policy, each paired to a Notion operational page.
5. **Resolver scripts** — deterministic arithmetic and source-checked rules.
6. **Dated GitHub mirrors, transcripts, uploads, and archives** — evidence only.

## What each layer owns

| Layer | Owns | Never owns |
|---|---|---|
| Notion | canon, current state, current resumes, registers, change log | executable resolver code |
| Skills / protocols | procedure, routing, prose law | campaign facts or dice results |
| Runtime-control docs | stable operating contract, resume schema, mirror law | current lane facts |
| Scripts | dice, stacking law, condition RAW, validation, stat lookups | canon, invented facts, cross-session truth |
| Dated mirrors | recovery, audit, historical diff | live authority or script input |

The only cross-session files scripts may own are explicitly ratified operational mirrors such as `*.character.json`; Notion remains canon for the character. Session-local registries are disposable.

## Governing sources per script / control document

| File | Governed by |
|---|---|
| `fused_round.py` | surface-campaign-master-gm §3; Notion Talent Catalog `37ce8214-84b0-81d3-ab92-fb245a10f9a1` |
| `skill_check.py` | PH Ch.4 skill DCs; GURPS Basic Set quick-contest rules |
| `personality_roll.py` | campaign-session-protocol NPC action framework |
| `conditions.py` | DMG 3.5 Condition Summary pp. 300–301 + verified DM Screen roster |
| `gurps_conditions.py` | GURPS 4e Basic Set — Campaigns B419–429, B551 |
| `combat_registry.py` | DMG dying/stabilization RAW; session-local only |
| `character_state.py` | PH typed-bonus stacking and class tables; Notion Advancement & Training Register |
| `pc_add.py` | bridge only — inherits both parents' sources |
| `spell_lookup.py` | SRD 3.5 + Spell Compendium extraction; SRD wins name collisions |
| `monster_lookup.py` | sourcebook bestiary extractions at `I:\Sourcebooks\_md\_bestiary\` |
| `prose_gate.py` | standing prose law + military-fantasy-prose skill |
| `session_open.py` | Notion Arik Session Start Protocol `364e8214-84b0-8144-bfc4-cd1f25ae3c3a` and cited state pages |
| `udrp_delve.py` | UDRP v2.0 + dungeon-generation + monster-ecology modules |
| `deferred_dice.py` | World-Move Law + Deferred Dice register; emits provenance, never writes Notion |
| `term_harvest.py` | cited DMG/GURPS source extractions; missing anchors print NO COVERAGE |
| `creature_harvest.py` | cited bestiary extractions; conversions require both 3.5e and GURPS halves |
| `item_harvest.py` | cited magic-item extractions (Magic Item Compendium; DMG v3.5 specific/wondrous items, the affix sections left to `term_harvest.py`); missing sources print NO COVERAGE; conversions require both 3.5e and GURPS halves |
| `power_harvest.py` | cited psionics extractions (Expanded Psionics Handbook + Complete Psionic); missing sources print NO COVERAGE; conversions require both 3.5e and GURPS halves |
| `maneuver_harvest.py` | cited martial-adept extractions (Tome of Battle); missing sources print NO COVERAGE; conversions require both 3.5e and GURPS halves |
| `feat_harvest.py` | bundled SRD 3.5 feats + cited supplement extractions (`_md\_feats\`); duplicates feat_lookup.py detection (no import); missing dir prints NO COVERAGE |
| `spell_harvest.py` | bundled SRD 3.5 spells + cited Spell Compendium and post-2005 splatbook extractions (Complete Mage/Champion, Races of the Dragon); school-anchored detection (sibling of power_harvest.py, no import); missing sources print NO COVERAGE |
| `resume_card.py` | Notion Resume Schema `3c4e8214-84b0-81dc-b0ae-eaf6ebb9bb48`; validates dated mirrors only |
| `docs/runtime-control/PLAY_CONTRACT.md` | Notion Play Contract `3c4e8214-84b0-818f-93c0-df1da2e52043` |

## Runtime-control boundary

- The Play Contract applies to live play, exact-freeze recovery, runtime-module resolution, and session close.
- Research, design, conversion, auditing, and repository maintenance are development mode and do not require a session boot receipt.
- Current resumes live in Notion beneath Resume Router `3c4e8214-84b0-8106-ae12-f50082ed43ff`.
- GitHub may store campaign facts only under `mirrors/notion/YYYY-MM-DD/`, visibly marked `NON-AUTHORITATIVE MIRROR`.
- Resolver scripts must never import or parse those mirrors as current state.

## Rules for any instance touching this repo

- **Scripts never invent campaign facts.** Required facts come from a live Notion read and are passed in explicitly.
- **Dice discipline lives in the scripts.** Do not re-implement dice in chat.
- **A script or control document disagreeing with its governing Notion page is a bug.** Patch the repository; never “correct” live canon from code.
- **Adding a script?** Ship a selftest, cite governing sources, and update this table.
- **Adding a state mirror?** Date it, mark it non-authoritative, cite Notion, validate it, and never overwrite an older export.
