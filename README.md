# the-new-path-engine

Mechanical resolution layer for **The New Path** campaign (D&D 3.5e / GURPS 4e hybrid).
This repository holds the resolver scripts, their tests, and their documentation. Nothing else.

---

## AUTHORITY ORDER — read first

1. **Notion is canon.** Every script in this repository implements rulings documented on a Notion page.
2. **On any disagreement between a script and its governing page, the page wins and the script gets patched.** Never the reverse.
3. A script's header comment cites its governing page. A script without a citation is not yet ratified.

| Script | Governing source |
|---|---|
| `scripts/fused_round.py` | Talent Catalog — Combat Vocabulary, Parts VII–IX (Notion `37ce8214-84b0-81d3-ab92-fb245a10f9a1`) |
| `scripts/skill_check.py` | D&D 3.5e DM Screen + GURPS 4e GM's Screen transcriptions (`I:\Sourcebooks`) |
| `scripts/personality_roll.py` | Voice & Locks Codex PERSONALITY TELL entries + NPC Personality Axis State DB (`1114d5fb00e1443a95528d7f9c485700`) |
| `scripts/prose_gate.py` *(planned)* | Register Directive + Content Law + AI-Default Sweep Addendum (surface-campaign-master-gm mirror, Notion `349e8214-84b0-8126-ac8f-f2de981bb8a9`) |

## THE DESIGN CONTRACT

Every script in this repository follows the same shape. New scripts join the family or don't get written.

- **Stateless resolvers.** Flags or JSON in, result out. Session state lives in an explicit state file passed by path, never inside a script.
- **Real dice only.** Python `secrets`. Raw values printed **before** any outcome is stated. No rerolls, no seeds, no fiat.
- **Visible output.** Every run prints a ready-to-paste header. The header must appear in the delivered message, in place, at the moment it resolves. A roll whose header the player never sees is indistinguishable from an invented roll and counts as one.
- **No hidden state, no cross-imports.** No script imports another script. Shared logic gets duplicated or promoted deliberately, never tangled.
- **Selftests.** Every script carries `--selftest` running worked examples against its governing page's exact tables. `tests/` holds calibration fixtures (the Measured House run for combat temperature; prose fixtures for the gate).

## ENFORCEMENT

- The **surface-campaign-master-gm** skill mandates `fused_round.py` for every combat round, `skill_check.py` for every one-off check (visible, Phase-0 style), and `personality_roll.py` for Tier 1/2 character beats (backstage, receipt line only).
- `prose_gate.py`, once built, runs on every prose draft **before delivery**, as a visible tool call with stdout in the transcript.
- **A claimed run without stdout in the transcript is a false compliance claim.** Self-assessed compliance is worth nothing; only externally checkable steps count — visible reads, raw stdout, fetch-backs, and commits in this log.

## WHAT THIS REPOSITORY IS NOT

- **No canon.** World facts, NPCs, sessions, rulings-as-lore — Notion, exclusively.
- **No session state.** Session logs and campaign state live in Notion; transient combat registries are throwaway local files, never committed.
- **No prose.** Narrative output is never stored here.

If a file with an in-world fact in it appears in this repository, that is a defect. Delete it and log the correction.

## STRUCTURE

```
scripts/   the resolver family (one job per file)
tests/     selftest fixtures and calibration cases
docs/      anything longer than this README should hold
```

## STATUS

| Script | State |
|---|---|
| fused_round.py | exists (currently shipped inside the skill package; migrating here as source of record) |
| skill_check.py | exists (same) |
| personality_roll.py | exists (same) |
| prose_gate.py | planned — regex ban-list sweep, noun-frequency check, floor word counts, header-presence check |

Once scripts live here, the skill package carries copies; **this repository is the source of record** and the skill copies get updated from it.
