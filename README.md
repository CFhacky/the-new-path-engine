# the-new-path-engine

Mechanical resolution and runtime-control layer for **The New Path** campaign (D&D 3.5e / GURPS 4e hybrid).

This repository holds resolver scripts, tests, stable runtime-control documents, and explicitly dated Notion mirror snapshots. It does **not** hold live campaign canon or mutable session state.

---

## AUTHORITY ORDER — read first

1. **Notion is canon.** Every resolver or stable control document implements a ruling or procedure documented on a Notion page.
2. **On disagreement, the governing Notion page wins and this repository gets patched.** Never the reverse.
3. Script header comments and runtime-control manifests cite their governing pages. Uncited machinery is not ratified.
4. Dated files beneath `mirrors/notion/` are recovery evidence only and are never current authority.

| Tool / document | Governing source |
|---|---|
| `scripts/fused_round.py` | Talent Catalog — Combat Vocabulary, Parts VII–IX (Notion `37ce8214-84b0-81d3-ab92-fb245a10f9a1`) |
| `scripts/skill_check.py` | D&D 3.5e DM Screen + GURPS 4e GM's Screen transcriptions (`I:\Sourcebooks`) |
| `scripts/personality_roll.py` | Voice & Locks Codex PERSONALITY TELL entries + NPC Personality Axis State DB (`1114d5fb00e1443a95528d7f9c485700`) |
| `scripts/prose_gate.py` | Register Directive + Content Law + AI-Default Sweep Addendum (surface-campaign-master-gm mirror, Notion `349e8214-84b0-8126-ac8f-f2de981bb8a9`) |
| `scripts/resume_card.py` | Campaign Resume Card Schema and Maintenance (Notion `3c4e8214-84b0-81dc-b0ae-eaf6ebb9bb48`) |
| `docs/runtime-control/PLAY_CONTRACT.md` | The New Path Play Contract — Live Session Governance (Notion `3c4e8214-84b0-818f-93c0-df1da2e52043`) |

## THE DESIGN CONTRACT

Every resolver in this repository follows the same shape. New scripts join the family or do not get written.

- **Stateless resolvers.** Flags or JSON in, result out. Session state lives in explicit state surfaces, never hidden inside a script.
- **Real dice only.** Python `secrets`. Raw values print before an outcome is stated. No rerolls, no seeds, no fiat.
- **Visible output.** Every run prints a ready-to-paste header where the governing protocol requires one.
- **No hidden state, no casual cross-imports.** Shared logic is promoted deliberately rather than tangled.
- **Selftests.** Every script carries `--selftest` or equivalent regression coverage tied to its governing source.
- **No script reads a dated Notion mirror as live state.** Mirrors are for recovery, audit, and diffing only.

## RUNTIME CONTROL

The stable control package is under [`docs/runtime-control/`](docs/runtime-control/README.md):

- live-play vs. development-mode scope;
- the five-item boot receipt;
- player-agency and strike law;
- delegated-operation authority;
- resume-card schema and freshness rules;
- Notion/GitHub/vault mirror boundaries.

Current lane resumes live under the Notion **Campaign Resume Router — Current Lanes**. GitHub stores only dated snapshots under `mirrors/notion/YYYY-MM-DD/`, each marked `NON-AUTHORITATIVE MIRROR` and validated by `scripts/resume_card.py`.

## ENFORCEMENT

- The **surface-campaign-master-gm** skill mandates the appropriate resolvers for combat, checks, and NPC beats.
- `prose_gate.py` runs where the active prose law requires it.
- The Play Contract applies only to live play, resuming a freeze, resolving a runtime module, and session close. Research and development work do not emit a session boot receipt.
- A claimed tool run without reproducible output is not evidence of compliance.

## WHAT THIS REPOSITORY IS NOT

- **No live canon.** Current world facts, NPC state, sessions, rulings-as-lore, and resume cards remain in Notion.
- **No mutable campaign state.** Operational mirrors may exist where explicitly ratified, but Notion remains canon.
- **No narrative archive.** Narrative output belongs in the campaign records, not here.
- **No undated current resume.** The only campaign-fact exception is the quarantined, dated, non-authoritative mirror tree.

If an in-world fact appears outside `mirrors/notion/` or a narrowly documented test fixture, treat it as a defect.

## STRUCTURE

```text
scripts/                     resolver and validator family
tests/                       regression tests and fixtures
reference/                   generated mechanical reference indexes
docs/runtime-control/        stable live-play and resume governance
mirrors/notion/YYYY-MM-DD/   immutable, non-authoritative recovery exports
```

## RUNTIME-CONTROL VALIDATION

```bash
python scripts/resume_card.py --selftest
python -m unittest -v tests.test_resume_card
python scripts/resume_card.py --check mirrors/notion/2026-08-22/Campaign_Resumes_All_Lanes.md
```

The repository is the editable source for engine code and versioned control documents. Notion is the operational source for live campaign state.
