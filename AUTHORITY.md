# AUTHORITY — read this before using anything in this repository

This repository is the MECHANICS and RUNTIME-CONTROL layer of The New Path campaign engine. It is less authoritative than Chad's instruction, live Notion, and ratified campaign procedure. If anything here conflicts with those authorities, this repository is wrong.

## The authority order (binding)

1. **Chad's live instruction** — outranks everything.
2. **Notion** — campaign canon, current lane state, current resume cards, registers, session prose, and the Canon Change Log. Fetch live before asserting state.
3. **Skill and protocol files** — procedure: when engines fire, session lifecycle, prose law, and arc routing.
4. **Stable runtime-control documents in this repository** — the live-play contract, resume schema, validation rules, and mirror policy, each paired to a Notion operational page.
5. **Resolver scripts and reference indices** — deterministic arithmetic and source-checked, book-RAW mechanics.
6. **Dated GitHub mirrors, transcripts, uploads, and archives** — evidence only.

**Below all of the above — the Path Engine Codex** (`codex/`) is a read-only *presentation* of the reference indices: a single searchable page that re-displays the layer-5 mechanics with their `system` labels, book+page citations, and (where available) the book-verbatim full stat block / description. It is the least-authoritative artifact in the repo — it creates nothing. Its built output embeds source text, so it is **git-ignored and rebuilt on demand** (`python codex/build_codex.py`). See [codex/README.md](codex/README.md).

## What each layer owns

| Layer | Owns | Never owns |
|---|---|---|
| Notion | canon, current state, current resumes, registers, change log | executable resolver code |
| Skills / protocols | procedure, routing, prose law | campaign facts or dice results |
| Runtime-control docs | stable operating contract, resume schema, mirror law | current lane facts |
| Scripts | dice, stacking law, condition RAW, validation, stat lookups | canon, invented facts, cross-session truth |
| Reference indices | cited, book-RAW mechanical entries | campaign canon, inferred values, sourcebook prose archives |
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
| `term_harvest.py` | cited DMG/GURPS modifier extractions; conditions remain in their authoritative lookup scripts, item/wargear bodies remain in dedicated system-labeled indexes, and the image-only PHB glossary is recorded as NO COVERAGE; missing anchors print NO COVERAGE |
| `reference_audit.py` | repository-integrity gate over `reference/families.json`; checks explicit accepted-entry paths, counts, provenance, labels, citation exceptions, U+FFFD, live selftests, and the Codex build; never creates mechanics |
| `codex/build_codex.py` | presentation only over the explicit accepted-entry paths in `reference/families.json`; inherits source-level book/citation/system metadata, validates every source-text slice, and never creates mechanics or canon |
| `creature_harvest.py` | cited bestiary extractions (`_md\_bestiary` + `_text` Monsters and Fiends); a garbage-name filter drops stat-fragment/prose rows; conversions require both 3.5e and GURPS halves |
| `item_harvest.py` | cited magic-item extractions (Magic Item Compendium; DMG v3.5; Arms & Equipment Guide 3.0); A&EG rejects CHAPTER running headers and locks all 362 accepted rows; missing sources print NO COVERAGE; conversions require both 3.5e and GURPS halves |
| `power_harvest.py` | cited psionics extractions (Expanded Psionics Handbook + Complete Psionic); Complete Psionic running CHAPTER/POWERS headers terminate wrapped-name recovery and are fixture/live tested; missing sources print NO COVERAGE; conversions require both 3.5e and GURPS halves |
| `maneuver_harvest.py` | cited Tome of Battle born-digital alternate extraction; Level/Class-anchored parser reconciles 208 detail blocks to the book’s own summary lists and records exact-source full-description spans on pp.52–94 (native D&D 3.5e, its own index); legacy noisy-scan detector remains fixture-tested; missing sources print NO COVERAGE; conversions require both 3.5e and GURPS halves |
| `mystery_harvest.py` | cited Tome of Magic shadow-magic descriptions; heading/category/Level-School detector captures 9 fundamentals and 60 path mysteries with printed fields only and exact full-description spans on PDF pp.142–154 (native D&D 3.5e, its own index); five exact, source-verified floating illustration blocks are excluded from export/Codex text without removing entry prose; shared chapter defaults are not imputed into rows; truename utterances remain separate; missing sources print NO COVERAGE |
| `feat_harvest.py` | bundled SRD 3.5 feats + cited supplement extractions (`_md\_feats\`); duplicates feat_lookup.py detection (no import); missing dir prints NO COVERAGE |
| `spell_harvest.py` | bundled SRD 3.5 spells + cited Spell Compendium and post-2005 splatbook extractions (Complete Mage/Champion, Races of the Dragon, Dragon Magic, Complete Scoundrel); school-anchored detection plus a source-roster/title-case detector for Complete Scoundrel (sibling of power_harvest.py, no import); emits each source’s exact relative extraction path for downstream span slicing; missing sources print NO COVERAGE |
| `gurps_magic_harvest.py` | cited GURPS Magic extraction; class-anchored detection (the GURPS magic system, a separate index from D&D spells); missing sources print NO COVERAGE |
| `dnd5e_spell_harvest.py` | cited D&D 5e spell extractions; a SEPARATE `system: D&D 5e` index (translator source, never 3.5e RAW); missing sources print NO COVERAGE |
| `dnd5e_item_harvest.py` | cited D&D 5e magic-item extractions; a SEPARATE `system: D&D 5e` index (translator source, never 3.5e RAW); missing sources print NO COVERAGE |
| `dnd5e_creature_harvest.py` | cited D&D 5e bestiary extractions; a SEPARATE, clearly-labeled `system: D&D 5e` index (source material for the translator, never 3.5e RAW); missing sources print NO COVERAGE |
| `gurps_gear_harvest.py` | cited GURPS Low-Tech weapon + armor tables; column-dump parser with exact, non-overlapping source-row spans (native GURPS 4e gear, its own index); missing sources print NO COVERAGE |
| `gurps_trait_harvest.py` | cited GURPS Basic Set Trait Lists roster plus exact, non-overlapping description/inline-definition spans on B18–B165 (four source-shared pairs; native GURPS 4e, its own index); missing sources print NO COVERAGE |
| `gurps_skill_harvest.py` | cited GURPS Basic Set skill list; column-dump parser for attribute/difficulty/defaults plus exact, non-overlapping Skills-chapter description spans (including grouped definitions and source-verified wrapped headings; native GURPS 4e, its own index); missing sources print NO COVERAGE |
| `gurps_technique_harvest.py` | cited GURPS Martial Arts Technique Cheat-Sheet + full Martial Arts extraction (born-digital text, not OCR); wrapped-name column parser for 112 combat techniques plus 96 exact, non-overlapping full-description groups (native GURPS 4e, its own index); missing sources print NO COVERAGE |
| `vestige_harvest.py` | cited Tome of Magic vestige summary + explicit per-entry stat tablets + ALL-CAPS description blocks (born-digital text); parser for 32 pact-magic vestiges with exact-source full-description spans on pp.20–50 (native D&D 3.5e, its own index); missing sources print NO COVERAGE |
| `soulmeld_harvest.py` | cited Magic of Incarnum soulmeld tables + ALL-CAPS description blocks (born-digital text); classify-parser for 89 incarnum soulmelds with exact-source full-description spans on pp.54–94 (native D&D 3.5e, its own index); missing sources print NO COVERAGE |
| `ad2e_psionics_harvest.py` | cited Complete Psionics Handbook (2e); a SEPARATE `system: AD&D 2e` index (translator source, never 3.5e RAW) — the first AD&D 2e content; missing sources print NO COVERAGE |
| `ad2e_spells_harvest.py` | cited AD&D 2e spell lists (Menzoberranzan, FOR2/5/7); a SEPARATE `system: AD&D 2e` index (translator source, never 3.5e RAW); missing sources print NO COVERAGE |
| `gurps3e_item_harvest.py` | cited GURPS 3e Magic Items 1-3; prose-item parser anchored on the terminal "Asking Price:" footer + garbage filter; a SEPARATE `system: GURPS 3e` index; missing sources print NO COVERAGE |
| `gurps3e_spell_harvest.py` | cited GURPS 3e Magic + Grimoire; class-anchored parser for 3e spells (native GURPS 3e taxonomy: Regular/Area/Missile/...); a SEPARATE `system: GURPS 3e` index; missing sources print NO COVERAGE |
| `wfrp_mutation_harvest.py` | cited WFRP 2e Chaos mutations & gifts from Tome of Corruption; vertical roll/name index records joined to a shared "Mutations Defined" glossary for RAW effect text; per-god tables + master d1000; a SEPARATE `system: WFRP` index; gifts defined only in an absent parent book print NO COVERAGE |
| `wfrp_gear_harvest.py` | cited WFRP 2e arms & armour from Old World Armoury; vertical column-dump parser, fixed-width rows anchored/validated on the Group cell (weapons) or Location cell (armour) with resync-on-failure; a SEPARATE `system: WFRP` index; missing WFRP core prints NO COVERAGE |
| `whfb_wargame_harvest.py` | cited WHFB *wargame* unit profiles **plus book-verbatim SPECIAL RULES blocks** from BORN-DIGITAL 8th-ed army-book PDFs (PyMuPDF words-mode geometric grid + subject/page-reference rule attachment; 217/291 profiles carry rules with their own page citations, 74 ambiguous rows are named NO COVERAGE); a corruption GATE routes broken-CMap PDFs to NO COVERAGE; fan-made books are never harvested; a SEPARATE `system: WHFB` index |
| `wh40k_wargame_harvest.py` | cited WH40K *wargame* unit profiles **plus book-verbatim SPECIAL RULES blocks** from BORN-DIGITAL codex PDFs (PyMuPDF words-mode geometric grid + text-section reconstruction; 118/136 profiles carry rules with their own page citations); auto-detects digital vs scanned (45 scanned print NO COVERAGE); generic header read (infantry WS…Sv + vehicle Front/Side/Rear); a SEPARATE `system: WH40K` index; 2nd-ed image-only labels captured positionally + flagged soft, never fabricated |
| `wfrp_creature_harvest.py` | cited WFRP 2e creature profiles from 5 born-digital roleplay books; anchors on the 8-characteristic WFRP run (main WS…Fel + secondary), with a strict headerless-block resolver for Thousand Thrones; a SEPARATE `system: WFRP` index; missing sources print NO COVERAGE |
| `wh40krp_talent_harvest.py` | cited 40K Roleplay talents (5 cores); per-book detectors read each book from its cleanest layer (DH/DW tab tables; RT/OW/BC prose w/ Tier: anchor); a SEPARATE `system: WH40K Roleplay` index; missing sources print NO COVERAGE |
| `wh40krp_psychic_harvest.py` | cited 40K Roleplay psychic-power blocks (5 cores); THREE format detectors (DH alternating / modern inline / RT technique); a SEPARATE `system: WH40K Roleplay` index; missing sources print NO COVERAGE |
| `wh40krp_forcefield_harvest.py` | cited 40K Roleplay Force Field tables (protection rating + overload) — the save-rating protective devices the armour & gear indices deliberately excluded; a SEPARATE `system: WH40K Roleplay` index; cores without a Force Fields table print NO COVERAGE |
| `wh40krp_gear_harvest.py` | cited 40K Roleplay non-weapon/non-armour gear (5 cores): general equipment, tools, drugs/consumables, cybernetics; per-table heading allow-list, auto-detects each table template from its header row, terminates rows on the Availability/Renown cell; a SEPARATE `system: WH40K Roleplay` index; missing sources print NO COVERAGE |
| `wh40krp_armour_harvest.py` | cited 40K Roleplay armour tables (5 cores); one universal detector anchors on the AP cell (guarded by a Locations phrase before + Weight after), reads name backward / schema-specific fields forward, handling DH Cost vs DW Req/Renown and RT scrambled/wrapped cells; a SEPARATE `system: WH40K Roleplay` index; missing sources print NO COVERAGE |
| `wh40krp_weapon_harvest.py` | cited 40K Roleplay armoury tables (5 cores + 11 supplements); Damage-cell-anchored column-dump parser (per-book schema variance; additive supplement path leaves core output byte-identical); a SEPARATE `system: WH40K Roleplay` index; missing sources print NO COVERAGE |
| `wh40krp_adversary_harvest.py` | cited Warhammer 40K Roleplay adversary stat blocks (Dark Heresy/Rogue Trader/Deathwatch/Black Crusade); 3 layout detectors + garbage filter; a SEPARATE `system: WH40K Roleplay` index; missing sources print NO COVERAGE |
| `gurps3e_creature_harvest.py` | cited GURPS 3e bestiaries (Bestiary, Fantasy Bestiary, Space Bestiary, Dinosaurs); a SEPARATE `system: GURPS 3e` index (translator source, never 4e RAW); garbage-name filter + dedup; missing sources print NO COVERAGE |
| `ad2e_monster_harvest.py` | AD&D 2e monsters VISION-TRANSCRIBED from the Planescape MC Appendix II PDF images (the OCR scrambles the stat columns); a SEPARATE `system: AD&D 2e` index; still book RAW, cited to the pages |
| `prestige_class_harvest.py` | D&D 3.x prestige classes VISION-TRANSCRIBED from the Dragon Magazine Prestige Class Compendium PDF images (321 of 355 pages are image-only); name + hit die + full requirements, cited to the page; still book RAW |
| `epic_item_harvest.py` | D&D 3.5 epic magic items (special abilities + specific items) VISION-TRANSCRIBED from ELH Ch.4; all 153 rows carry exact spans into a reproducible raw two-column OCR extraction of the 103 printed description blocks (pp.126-146), with variants sharing the book's common block; prices cross-checked vs printed XP costs; book RAW, page-cited |
| `epic_monster_harvest.py` | D&D 3.5 epic monsters VISION-TRANSCRIBED from the ELH PDF images (Ch.6, pp.157-230); all 64 rows carry exact spans into 50 reproducible raw two-column OCR description blocks (pp.158-230), with printed variants sharing the book's common block; degraded glyphs reconstructed only from the block’s own arithmetic and flagged, never guessed |
| `epic_spell_harvest.py` | D&D 3.5 epic spells (24 seeds + 46 sample spells) VISION-TRANSCRIBED from ELH Ch.2; all 70 rows carry exact spans into a reproducible raw two-column OCR extraction of the printed descriptions (pp.74-102); records book-internal DC discrepancies faithfully; book RAW, page-cited |
| `epic_feat_harvest.py` | D&D 3.5 epic feats: 153 Table 1-36 rows VISION-TRANSCRIBED from ELH pp.46-49 plus description-only Dire Charge (p.53); 149 exact full-description spans into a reproducible raw two-column OCR extraction (pp.50-69), with five unreadable p.60-dependent descriptions explicit `NO COVERAGE`; book RAW, page-cited |
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
