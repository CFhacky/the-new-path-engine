# AUTHORITY — read this before using anything in this repository

This repository is the MECHANICS layer of The New Path campaign engine.
It is the least authoritative layer in the stack. If anything in these
scripts conflicts with a Notion page or Chad's live instruction, the
script is wrong.

## The authority order (binding)

1. **Chad's live instruction** — outranks everything.
2. **Notion** — ALL campaign canon: characters, factions, registers,
   session prose, the Canon Change Log. Fetched live, every session,
   before anything is asserted. A script never substitutes for a fetch.
3. **Skill files** — procedure: when engines fire, session protocol,
   prose law, arc state routing.
4. **These scripts** — deterministic arithmetic and book RAW only.
   They hold the rules that never change so no instance ever
   re-derives (or mis-remembers) them.

## What each layer owns

| Layer | Owns | Never owns |
|---|---|---|
| Notion | campaign state, registers, canon, change log | dice mechanics |
| Skills | procedure, protocol, prose law | campaign facts, dice results |
| Scripts | dice, stacking law, condition RAW, stat lookups, state mirrors | canon, invented facts, cross-session truth |

The only cross-session files scripts own are `*.character.json`
operational mirrors. **Notion remains canon for the character** — the
mirror syncs to the Advancement & Training Register at session end, and
every sync pairs with a Canon Change Log entry, per standing law.
`*.registry.json` files are session-local and disposable.

## Governing sources per script

| Script | Governed by |
|---|---|
| `fused_round.py` | surface-campaign-master-gm SKILL.md §3 (THE FUSED ENGINE); Notion Talent Catalog page `37ce8214-84b0-81d3-ab92-fb245a10f9a1` (Parts VII–VIII) |
| `skill_check.py` | PH Ch.4 skill DCs; GURPS Basic Set quick-contest rules |
| `personality_roll.py` | campaign-session-protocol skill (NPC action framework) |
| `conditions.py` | DMG 3.5 Condition Summary (pp. 300–301) + DM Screen roster — verified verbatim against the OCR at `I:\Sourcebooks\_md\Dungeon_Masters_Guide_3.5.md` |
| `gurps_conditions.py` | GURPS 4e Basic Set — Campaigns: B419–429, B551 (extracted from the text-layer PDF, page = PDF − 335) |
| `combat_registry.py` | DMG dying/stabilization RAW; session-local only |
| `character_state.py` | PH p.171 typed-bonus stacking law; PH Ch.3 class tables; spell effects at cited PH pages; **canon source: Notion Advancement & Training Register (fetch by name at session start)** |
| `pc_add.py` | bridge only — inherits both parents' sources |
| `spell_lookup.py` | SRD 3.5 (bundled JSON) + Spell Compendium text extraction at `I:\Sourcebooks\_md\Spell_Compendium.md`; SRD wins name collisions |
| `monster_lookup.py` | ten text-layer bestiary extractions at `I:\Sourcebooks\_md\_bestiary\` (MM3 and Draconomicon absent until OCR'd) |
| `prose_gate.py` | Standing Law prose section; military-fantasy-prose skill |

## Rules for any instance touching this repo

- **Scripts never invent campaign facts.** If a resolution needs a fact
  (an NPC's stats, a register value, a ruling), it comes from a Notion
  page read this session, passed in as flags.
- **Dice discipline is in the scripts** — python `secrets`, raw stdout
  before outcomes, four throws mode-else-median where the protocol says
  so. Do not re-implement dice in chat.
- **A script disagreeing with a page is a bug.** Fix the script; never
  "correct" the page from code.
- **Adding a script?** It ships with a `--selftest`, cites its governing
  sources in the docstring, and gets a row in this table.
