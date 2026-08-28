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
| `creature_harvest.py` | cited bestiary extractions (`_md\_bestiary` + `_text` Monsters and Fiends); a garbage-name filter drops stat-fragment/prose rows; conversions require both 3.5e and GURPS halves |
| `item_harvest.py` | cited magic-item extractions (Magic Item Compendium; DMG v3.5; Arms & Equipment Guide 3.0); missing sources print NO COVERAGE; conversions require both 3.5e and GURPS halves |
| `power_harvest.py` | cited psionics extractions (Expanded Psionics Handbook + Complete Psionic); missing sources print NO COVERAGE; conversions require both 3.5e and GURPS halves |
| `maneuver_harvest.py` | cited martial-adept extractions (Tome of Battle); missing sources print NO COVERAGE; conversions require both 3.5e and GURPS halves |
| `feat_harvest.py` | bundled SRD 3.5 feats + cited supplement extractions (`_md\_feats\`); duplicates feat_lookup.py detection (no import); missing dir prints NO COVERAGE |
| `spell_harvest.py` | bundled SRD 3.5 spells + cited Spell Compendium and post-2005 splatbook extractions (Complete Mage/Champion, Races of the Dragon, Dragon Magic); school-anchored detection (sibling of power_harvest.py, no import); missing sources print NO COVERAGE |
| `gurps_magic_harvest.py` | cited GURPS Magic extraction; class-anchored detection (the GURPS magic system, a separate index from D&D spells); missing sources print NO COVERAGE |
| `dnd5e_spell_harvest.py` | cited D&D 5e spell extractions; a SEPARATE `system: D&D 5e` index (translator source, never 3.5e RAW); missing sources print NO COVERAGE |
| `dnd5e_item_harvest.py` | cited D&D 5e magic-item extractions; a SEPARATE `system: D&D 5e` index (translator source, never 3.5e RAW); missing sources print NO COVERAGE |
| `dnd5e_creature_harvest.py` | cited D&D 5e bestiary extractions; a SEPARATE, clearly-labeled `system: D&D 5e` index (source material for the translator, never 3.5e RAW); missing sources print NO COVERAGE |
| `gurps_gear_harvest.py` | cited GURPS Low-Tech weapon table; column-dump parser (native GURPS 4e gear, its own index); missing sources print NO COVERAGE |
| `gurps_trait_harvest.py` | cited GURPS Basic Set Trait Lists appendix; column-dump parser for advantages/disadvantages (native GURPS 4e, its own index); missing sources print NO COVERAGE |
| `gurps_skill_harvest.py` | cited GURPS Basic Set skill list; column-dump parser for skills (attribute/difficulty/defaults; native GURPS 4e, its own index); missing sources print NO COVERAGE |
| `gurps_technique_harvest.py` | cited GURPS Martial Arts Technique Cheat-Sheet (born-digital text, not OCR); column-dump parser for combat techniques (native GURPS 4e, its own index); missing sources print NO COVERAGE |
| `vestige_harvest.py` | cited Tome of Magic vestige summary (born-digital text); column-dump parser for pact-magic vestiges (native D&D 3.5e, its own index); missing sources print NO COVERAGE |
| `soulmeld_harvest.py` | cited Magic of Incarnum soulmeld tables (born-digital text); classify-parser for incarnum soulmelds, de-interleaving the column-split descriptions (native D&D 3.5e, its own index); missing sources print NO COVERAGE |
| `ad2e_psionics_harvest.py` | cited Complete Psionics Handbook (2e); a SEPARATE `system: AD&D 2e` index (translator source, never 3.5e RAW) — the first AD&D 2e content; missing sources print NO COVERAGE |
| `ad2e_spells_harvest.py` | cited AD&D 2e spell lists (Menzoberranzan, FOR2/5/7); a SEPARATE `system: AD&D 2e` index (translator source, never 3.5e RAW); missing sources print NO COVERAGE |
| `gurps3e_item_harvest.py` | cited GURPS 3e Magic Items 1-3; prose-item parser anchored on the terminal "Asking Price:" footer + garbage filter; a SEPARATE `system: GURPS 3e` index; missing sources print NO COVERAGE |
| `gurps3e_spell_harvest.py` | cited GURPS 3e Magic + Grimoire; class-anchored parser for 3e spells (native GURPS 3e taxonomy: Regular/Area/Missile/...); a SEPARATE `system: GURPS 3e` index; missing sources print NO COVERAGE |
| `wfrp_gear_harvest.py` | cited WFRP 2e arms & armour from Old World Armoury; vertical column-dump parser, fixed-width rows anchored/validated on the Group cell (weapons) or Location cell (armour) with resync-on-failure; a SEPARATE `system: WFRP` index; missing WFRP core prints NO COVERAGE |
| `wfrp_creature_harvest.py` | cited WFRP 2e creature profiles from 5 born-digital roleplay books; anchors on the 8-characteristic WFRP run (main WS…Fel + secondary), with a strict headerless-block resolver for Thousand Thrones; a SEPARATE `system: WFRP` index; missing sources print NO COVERAGE |
| `wh40krp_talent_harvest.py` | cited 40K Roleplay talents (5 cores); per-book detectors read each book from its cleanest layer (DH/DW tab tables; RT/OW/BC prose w/ Tier: anchor); a SEPARATE `system: WH40K Roleplay` index; missing sources print NO COVERAGE |
| `wh40krp_psychic_harvest.py` | cited 40K Roleplay psychic-power blocks (5 cores); THREE format detectors (DH alternating / modern inline / RT technique); a SEPARATE `system: WH40K Roleplay` index; missing sources print NO COVERAGE |
| `wh40krp_weapon_harvest.py` | cited 40K Roleplay armoury tables (5 cores); Damage-cell-anchored column-dump parser (per-book schema variance); a SEPARATE `system: WH40K Roleplay` index; missing sources print NO COVERAGE |
| `wh40krp_adversary_harvest.py` | cited Warhammer 40K Roleplay adversary stat blocks (Dark Heresy/Rogue Trader/Deathwatch/Black Crusade); 3 layout detectors + garbage filter; a SEPARATE `system: WH40K Roleplay` index; missing sources print NO COVERAGE |
| `gurps3e_creature_harvest.py` | cited GURPS 3e bestiaries (Bestiary, Fantasy Bestiary, Space Bestiary, Dinosaurs); a SEPARATE `system: GURPS 3e` index (translator source, never 4e RAW); garbage-name filter + dedup; missing sources print NO COVERAGE |
| `ad2e_monster_harvest.py` | AD&D 2e monsters VISION-TRANSCRIBED from the Planescape MC Appendix II PDF images (the OCR scrambles the stat columns); a SEPARATE `system: AD&D 2e` index; still book RAW, cited to the pages |
| `prestige_class_harvest.py` | D&D 3.x prestige classes VISION-TRANSCRIBED from the Dragon Magazine Prestige Class Compendium PDF images (321 of 355 pages are image-only); name + hit die + full requirements, cited to the page; still book RAW |
| `epic_item_harvest.py` | D&D 3.5 epic magic items (special abilities + specific items) VISION-TRANSCRIBED from the ELH PDF images (Ch.4, pp.124-147); prices cross-checked vs printed XP costs; book RAW, cited to the page |
| `epic_monster_harvest.py` | D&D 3.5 epic monsters VISION-TRANSCRIBED from the ELH PDF images (Ch.6, pp.157-230); name/size-type/HD/AC/CR/abilities per the p.156 roster; degraded glyphs reconstructed only from the block’s own arithmetic and flagged, never guessed |
| `epic_spell_harvest.py` | D&D 3.5 epic spells (seeds + sample spells) VISION-TRANSCRIBED from the Epic Level Handbook PDF images (Ch.2, pp.72-88); still book RAW, cited to the pages; records book-internal DC discrepancies faithfully |
| `epic_feat_harvest.py` | D&D 3.5 epic feats VISION-TRANSCRIBED from the Epic Level Handbook PDF page images (Table 1-36, pp.46-49) because the OCR text layer is corrupt; still book RAW, cited to the pages |
| `gurps_creature_harvest.py` | cited GURPS bestiary extractions (Dungeon Fantasy Monsters, Creatures of the Night, Fantasy); attribute-block detection across three name/stat formats; a separate index from D&D creatures; missing sources print NO COVERAGE |
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
