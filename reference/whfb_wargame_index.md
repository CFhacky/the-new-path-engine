# Warhammer Fantasy Battle Wargame -- Unit Profile Index

**System:** WHFB (tabletop wargame -- NOT the WFRP roleplay line)  
**Total profiles:** 302
**Profiles with special rules:** 228
**Named special-rules gaps:** 74
**Soft / uncertain rows:** 1  

Profiles (M WS BS S T W I A Ld) extracted geometrically from the PDF text layer (PyMuPDF words mode) of born-digital OFFICIAL Games Workshop army books, plus one bounded High Elves page transcribed from a verified 3x render. Fan-made files and uncovered scanned pages remain explicit NO COVERAGE.

## Methodology

- Profiles reconstructed geometrically from the PDF text layer (PyMuPDF words mode): a header row of characteristic labels (M WS BS S T W I A Ld) fixes each column's x-centre, and every value row maps its stat tokens to the nearest column. The header is read live -- never hard-coded -- so a table that omits or reorders a column still parses. No number is ever guessed or corrected; unreadable cells are left empty.
- The official 8th-edition High Elves PDF is a 96-page image-only scan: PyMuPDF returns 0 characters and 0 words on every page. Exactly PDF page 91 (printed p.92) was rendered at 3x and transcribed by vision, then checked directly against the page image. Its 12 printed profile lines yield 11 unique rows because Elven Steed is repeated identically. Every other High Elves page remains explicit NO COVERAGE.
- These books lay text out glyph-by-glyph (there are no space characters in the content stream), so each unit name is rebuilt from the contiguous glyph cluster immediately left of the first stat column, inserting a space where the horizontal gap widens to a word break. Decorative drop-cap / bullet glyphs are trimmed. The clean ALL-CAPS datasheet heading above the table is captured separately as unit_context.
- A datasheet prints several profile lines -- the unit, its champion/command upgrade, and any mount or monster -- each emitted as its own row sharing the unit_context heading. Troop Type (Infantry/Cavalry/Monster/Chariot/War Beast/...) is captured from the 'TROOP TYPE:' line beneath a bestiary block or from the trailing text column after Ld in the army-list summary.
- Movement values keep verbatim any '*' (variable) or random-movement die (e.g. 2D6); '-' marks a characteristic a model does not have. Leadership can reach 10. Parenthetical values are kept as printed.
- SPECIAL RULES text is copied verbatim from the unit's PDF section. The attachment uses same-column profile geometry, explicit subject-qualified headings, or the army-list summary's printed Page column plus an exact name occurrence on the cited bestiary page. Display-spaced headings such as 'S P E C I A L R U L E S' are recognised. Ambiguous links remain named NO COVERAGE gaps; no rule text is inferred.
- Only the OFFICIAL Games Workshop army books are harvested. Born-digital files whose filenames mark them fan-made/unofficial ('9th', 'PDF Room', 'pdf-free', version tags) are classified DIGITAL-UNOFFICIAL and skipped so a fan stat is never passed as an official one. The 1994 4th-ed Chaos book is born-digital by character count but its font/CMap is broken -- the characteristic DIGITS extract as garbage (a '4' becomes '-j'/'~') -- so a token-corruption gate (alpha-junk fraction > 1.5%) routes it to NO COVERAGE rather than fabricating numbers (Inviolable Rule 1). Core rulebooks are skipped by policy.
- Summary/army-list tables duplicate the per-datasheet bestiary profiles; exact (name, profile) duplicates are merged within each book (space/case insensitive), preferring the row that also carries a troop_type.

## Digital OFFICIAL books harvested

| Book | Army | Edition | Profiles | Rules |
| --- | --- | --- | --- | --- |
| Armybook_8ed - Daemons of Chaos - 2012 | Daemons of Chaos | 8th | 54 | 38 |
| Armybook_8ed - Dwarfs - 2014 | Dwarfs | 8th | 40 | 34 |
| Armybook_8ed - Lizardmen | Lizardmen | 8th | 49 | 28 |
| Armybook_8ed - Vampire Counts | Vampire Counts | 8th | 52 | 44 |
| Armybook_8ed - Warriors of Chaos 2012 | Warriors of Chaos | 8th | 49 | 32 |
| Armybook_8ed - Wood Elves | Wood Elves | 8th | 47 | 41 |

## Bounded VISION coverage (official scanned book)

- Armybook_8ed - High Elves: PDF page 91 (printed p.92), 11 unique profiles from 12 printed profile lines; all other pages remain NO COVERAGE.

## Digital UNOFFICIAL / fan-made (skipped -- not harvested)

- Warhammer Armies_ Dwarfs - PDF Room  _(marker: pdf room)_
- warhammer-dwarfs-9th-ed-v122-pdf-free  _(marker: 9th)_
- warhammer-fantasy-battles-warhammer-armies-eng-dwarfs-of-chaos-pdf-free  _(marker: pdf-free)_
- warhammer-warriors-of-chaos-9th-ed-v124-pdf-free  _(marker: 9th)_
- Warhammer_ Chaos Dwarfs - PDF Room  _(marker: pdf room)_
- Warhammer_ Daemons of Chaos 9th Edition 13 - PDF Room  _(marker: 9th)_
- Warhammer_ Skaven 9th edition 17 - PDF Room  _(marker: 9th)_
- Warhammer_ Vampire Counts 9th Edition 15 - PDF Room  _(marker: 9th)_
- Warhammer_ Warriors of Chaos 9th Edition 14 - PDF Room  _(marker: 9th)_

## NO COVERAGE (born-digital but broken text layer)

- Armybook_4ed - Chaos - 1994  _(2.7% junk-alpha tokens: font/CMap corrupts the characteristic digits; not harvested per Inviolable Rule 1)_

## Skipped by policy (core rulebooks, not army rosters)

- Rulebook_8ed - Warhammer FB Rulebook 8th_2010

## Skipped (FAQ / errata subfolder -- 15 files, not army rosters)

- chaosdwarfs
- Codex Black Legion _Proof Read_
- darkelves
- derevision
- dwarfs
- empire
- highelves
- hordesofchaos
- lizardmen
- ogrekingdoms_faq
- orcsgoblins
- skaven
- tombkings
- vampirecounts
- warhammer_v7_faq

## NO COVERAGE (special-rules attachment)

These profiles remain mechanically indexed, but no unambiguous explicit unit SPECIAL RULES section could be linked:

- Armybook_8ed - Daemons of Chaos - 2012 / Soul Grinder (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Daemons of Chaos - 2012 / Daemon Prince (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Daemons of Chaos - 2012 / Herald of Khorne (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Daemons of Chaos - 2012 / Herald of Slaanesh (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Daemons of Chaos - 2012 / Herald of Tzeentch (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Daemons of Chaos - 2012 / The Masque (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Daemons of Chaos - 2012 / Bloodreaper (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Daemons of Chaos - 2012 / Beast of Nurgle (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Daemons of Chaos - 2012 / Bloodhunter (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Daemons of Chaos - 2012 / Juggernaut (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Daemons of Chaos - 2012 / Chaos Fury (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Daemons of Chaos - 2012 / Fiend of Slaanesh (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Daemons of Chaos - 2012 / Flamer (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Daemons of Chaos - 2012 / Pyrocaster (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Daemons of Chaos - 2012 / Nurglings (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Daemons of Chaos - 2012 / Daemonette Crew (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Dwarfs - 2014 / Daemon Slayer (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Dwarfs - 2014 / Shieldbearers (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Dwarfs - 2014 / Anvil Guards (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Dwarfs - 2014 / Thorgrim (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Dwarfs - 2014 / Dragon Slayer (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Dwarfs - 2014 / Dwarf Warrior (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Grymloq (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Lord Kroak (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Saurus Oldblood (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Slann Mage-Priest (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Tehenhauin (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Chakax (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Gor-Rok (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Oxyotl (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Saurus Scar-Veteran (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Tetto'eko (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Tiktaq'to (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Patrol Leader (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Bastiladon (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Chameleon Skink (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Stalker (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Jungle Swarm (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Ripperdacyd Brave (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Temple Guard (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Revered Guardian (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Razordon (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Lizardmen / Skink Oracle Rider (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Vampire Counts / Strigoi Ghoul King (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Vampire Counts / Vlad von Carstein (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Vampire Counts / Cairn Wraith (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Vampire Counts / Isabella von Carstein (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Vampire Counts / Krell (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Vampire Counts / Mannfred the Acolyte (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Vampire Counts / Spirit Horde (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Vampire Counts / Skeleton Warrior (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Warriors of Chaos 2012 / Scyla Anfingrimm (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Warriors of Chaos 2012 / Chaos Troll (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Warriors of Chaos 2012 / Chimera (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Warriors of Chaos 2012 / Chaos Sorcerer (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Warriors of Chaos 2012 / Festus the Leechlord (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Warriors of Chaos 2012 / Scyla Anfingrimm (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Warriors of Chaos 2012 / Throgg (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Warriors of Chaos 2012 / Wulfrik the Wanderer (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Warriors of Chaos 2012 / Chaos Chariot (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Warriors of Chaos 2012 / Chaos Charioteer (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Warriors of Chaos 2012 / Chaos Marauder (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Warriors of Chaos 2012 / Marauder Chieftain (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Warriors of Chaos 2012 / Chaos Giant (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Warriors of Chaos 2012 / Mutalith Vortex Beast (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Warriors of Chaos 2012 / Skullcrusher (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Warriors of Chaos 2012 / Skullhunter (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Warriors of Chaos 2012 / Slaughterbrute (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Wood Elves / Handmaiden of the Thorn (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Wood Elves / Durthu (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Wood Elves / Spellweaver (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Wood Elves / Drycha (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Wood Elves / Arahan (no unambiguous explicit SPECIAL RULES section)
- Armybook_8ed - Wood Elves / Forest Dragon (no unambiguous explicit SPECIAL RULES section)

## NO COVERAGE (scanned, image-only books or uncovered pages)

- Armybook_4ed -  Undead - 1994
- Armybook_4ed - Chaos Dwarfs - 1994
- Armybook_4ed - High Elves - 1993
- Armybook_5ed - Bretonnia - 1999
- Armybook_5ed - Dark Elves - 1996
- Armybook_5ed - Dogs of War
- Armybook_5ed - Dwarfs - 1996
- Armybook_5ed - Lizardmen - 1997
- Armybook_5ed - Orcs and Goblins - 1996
- Armybook_5ed - Skaven - 1996
- Armybook_5ed - The Empire - 1996
- Armybook_5ed - Vampire Counts - 1999
- Armybook_5ed - Wood Elves - 1996
- Armybook_6ed - Beasts Of Chaos
- Armybook_6ed - Bretonnia
- Armybook_6ed - Dark Elves
- Armybook_6ed - Dwarfs
- Armybook_6ed - High Elves
- Armybook_6ed - Hordes of Chaos
- Armybook_6ed - Lizardmen
- Armybook_6ed - Orcs & Goblins
- Armybook_6ed - Skaven
- Armybook_6ed - The Empire
- Armybook_6ed - Tomb Kings
- Armybook_6ed - Vampire Counts
- Armybook_6ed - Wood Elves
- Armybook_7ed - Beastmen
- Armybook_7ed - Daemons_of_Chaos
- Armybook_7ed - Dark Elves
- Armybook_7ed - Dwarfs - 2005
- Armybook_7ed - High Elves - 2007 (No_Modeling_Section)
- Armybook_7ed - Lizardmen 2008
- Armybook_7ed - Ogre Kingdoms - 2004
- Armybook_7ed - Orcs & Goblins - 2006
- Armybook_7ed - Skaven armybook 7ed
- Armybook_7ed - The Empire (cut)
- Armybook_7ed - Vampire Counts - 2008
- Armybook_7ed - Warriors of Chaos
- Armybook_7ed - Wood Elves - 2005 - 7th Edition
- Armybook_8ed - Dark_Elves (buggy)
- Armybook_8ed - Dark_Elves (cut)
- Armybook_8ed - High Elves [PDF pages 1-90, 92-96]
- Armybook_8ed - Ogre Kingdoms
- Armybook_8ed - Orcs And Goblins
- Armybook_8ed - The Empire - 2011
- Armybook_8ed - Tomb Kings (cut)
- Rulebook_7ed - WHFB-rulebook-7th
- warhammer-5th-edition-army-book-chaos-dwarfs-pdf-free
- warhammer-fantasy-daemons-of-chaos-7th-pdf-2-pdf-free
- warhammer-fantasy-warriors-of-chaos-7th-no-cover-pdf-pdf-free
- WHFB Rulebook - 1991 - 3th Edition

## Digital pages whose profiles could not be parsed

- Armybook_8ed - Daemons of Chaos - 2012 [PDF page 31]: value rows present but no header row parsed
- Armybook_8ed - Daemons of Chaos - 2012 [PDF page 47]: value rows present but no header row parsed
- Armybook_8ed - Daemons of Chaos - 2012 [PDF page 49]: value rows present but no header row parsed
- Armybook_8ed - Daemons of Chaos - 2012 [PDF page 53]: value rows present but no header row parsed
- Armybook_8ed - Daemons of Chaos - 2012 [PDF page 54]: value rows present but no header row parsed
- Armybook_8ed - Daemons of Chaos - 2012 [PDF page 86]: value rows present but no header row parsed
- Armybook_8ed - Daemons of Chaos - 2012 [PDF page 89]: value rows present but no header row parsed
- Armybook_8ed - Daemons of Chaos - 2012 [PDF page 92]: value rows present but no header row parsed
- Armybook_8ed - Daemons of Chaos - 2012 [PDF page 93]: value rows present but no header row parsed
- Armybook_8ed - Daemons of Chaos - 2012 [PDF page 94]: value rows present but no header row parsed
- Armybook_8ed - Daemons of Chaos - 2012 [PDF page 97]: value rows present but no header row parsed
- Armybook_8ed - Dwarfs - 2014 [PDF page 13]: value rows present but no header row parsed
- Armybook_8ed - Dwarfs - 2014 [PDF page 23]: value rows present but no header row parsed
- Armybook_8ed - Dwarfs - 2014 [PDF page 24]: value rows present but no header row parsed
- Armybook_8ed - Dwarfs - 2014 [PDF page 40]: value rows present but no header row parsed
- Armybook_8ed - Dwarfs - 2014 [PDF page 65]: value rows present but no header row parsed
- Armybook_8ed - Dwarfs - 2014 [PDF page 66]: value rows present but no header row parsed
- Armybook_8ed - Dwarfs - 2014 [PDF page 95]: value rows present but no header row parsed
- Armybook_8ed - Lizardmen [PDF page 35]: value rows present but no header row parsed
- Armybook_8ed - Lizardmen [PDF page 38]: value rows present but no header row parsed
- Armybook_8ed - Lizardmen [PDF page 42]: value rows present but no header row parsed
- Armybook_8ed - Lizardmen [PDF page 44]: value rows present but no header row parsed
- Armybook_8ed - Lizardmen [PDF page 50]: value rows present but no header row parsed
- Armybook_8ed - Lizardmen [PDF page 52]: value rows present but no header row parsed
- Armybook_8ed - Lizardmen [PDF page 56]: value rows present but no header row parsed
- Armybook_8ed - Lizardmen [PDF page 61]: value rows present but no header row parsed
- Armybook_8ed - Lizardmen [PDF page 87]: value rows present but no header row parsed
- Armybook_8ed - Lizardmen [PDF page 102]: value rows present but no header row parsed
- Armybook_8ed - Warriors of Chaos 2012 [PDF page 92]: value rows present but no header row parsed
- Armybook_8ed - Warriors of Chaos 2012 [PDF page 98]: value rows present but no header row parsed
- Armybook_8ed - Wood Elves [PDF page 55]: value rows present but no header row parsed
- Armybook_8ed - Wood Elves [PDF page 102]: value rows present but no header row parsed

## Armybook_8ed - Daemons of Chaos - 2012

| Unit | Profile | Troop Type | Context | Edition | Citation | Rules | Soft |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Bloodthirster | M8 WS10 BS10 S6 T6 W5 I9 A6 Ld9 | Monster(Character) |  | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 28] | yes |  |
| Juggernaut of Khorne | M7 WS5 BS0 S5 T4 W3 I2 A3 Ld7 | Monstrous Beast | BLOODCRUSHERS OF KHORNE | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 30] | yes |  |
| Skull Cannon | M7 BS- S5 T5 W4 I3 A- | Chariot(ArmourSave3+) |  | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 32] | yes |  |
| Bloodletter Crew | M- WS5 BS5 S4 T- W- I4 A1 Ld7 | Chariot(ArmourSave3+) |  | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 32] | yes |  |
| Skulltaker | M5 WS9 BS9 S5 T4 W2 I9 A4 Ld8 | Infantry(SpecialCharacter) |  | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 34] | yes |  |
| Karanak | M8 WS7 BS0 S5 T5 W3 I6 A4 Ld8 |  |  | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 35] | yes |  |
| Skarbrand | M8 WS10 BS10 S6 T6 W5 I10 A6 Ld9 | Monster(SpecialCharacter) |  | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 36] | yes |  |
| Pink Horror | M4 WS3 BS3 S3 T3 W1 I3 A1 Ld7 | Infantry(Character) |  | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 38] | yes |  |
| Iridescent Horror | M4 WS3 BS3 S3 T3 W1 I3 A2 Ld7 | Infantry(Character) |  | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 38] | yes |  |
| Screamer | M1 WS3 BS0 S4 T4 W2 I4 A3 Ld7 | WarBeast | SCREAMERS 6 DISCS OF TZEENTCH | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 39] | yes |  |
| Disc of Tzeenteh | M1 WS3 BS0 S4 T4 W1 I4 A3 Ld7 | WarBeast | SCREAMERS 6 DISCS OF TZEENTCH | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 39] | yes |  |
| The Blue Scribes | M- WS3 BS3 S3 T3 W2 I3 A2 Ld7 |  |  | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 41] | yes |  |
| Disc of Tzeentch | M1 WS3 BS0 S4 T4 W1 I4 A3 Ld7 | WB Mo=Monster,Ch Chariot,Sw=Swarms, Un Unique | THE BLUE SCRIBES | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 41] | yes |  |
| The Changeling | M4 WS3 BS4 S3 T3 W2 I3 A1 Ld8 | Infantry(SpecialCharacter) |  | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 42] | yes |  |
| Kairos Fateweaver | M8 WS1 BS0 S5 T5 W5 I1 A1 Ld9 | Monster(SpecialCharacter) | VKAIROS'A I D H C FATEWEAVERС А Т Ї | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 43] | yes |  |
| Great Unclean One | M6 WS6 BS3 S6 T7 W6 I4 A5 Ld9 | Monster(Character) |  | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 44] | yes |  |
| Plaguebearer | M4 WS3 BS3 S4 T4 W1 I2 A1 Ld7 | Infantry | A /~*T | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 45] | yes |  |
| Plagueridden | M4 WS3 BS3 S4 T4 W1 I2 A2 Ld7 | Infantry | A /~*T | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 45] | yes |  |
| Plaguebringer | M4 WS3 BS3 S4 T4 W1 I2 A2 Ld7 | Monstrous Cavalry | PLAGUE DRONES OF NURGLE | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 46] | yes |  |
| Rot Fly | M1 WS3 BS3 S5 T5 W3 I2 A3 Ld7 | Monstrous Cavalry | PLAGUE DRONES OF NURGLE | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 46] | yes |  |
| Keeper of Secrets | M10 WS9 BS6 S6 T6 W5 I1 A06 Ld9 |  |  | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 50] | yes |  |
| Daemonette | M6 WS5 BS4 S3 T3 W1 I5 A2 Ld7 | T R O O P TYPE Infantry(Character) | DAEMONETTES OF SLAANESH | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 51] | yes |  |
| Alluress | M6 WS5 BS4 S3 T3 W1 I5 A3 Ld7 |  | DAEMONETTES OF SLAANESH | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 51] | yes |  |
| Seeker | M6 WS5 BS4 S3 T3 W1 I5 A2 Ld7 |  |  | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 52] | yes |  |
| Heartseeker | M6 WS5 BS4 S3 T3 W1 I5 A3 Ld7 |  |  | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 52] | yes |  |
| Steed of Slaanesh | M10 WS3 BS0 S3 T3 W1 I5 A1 Ld7 |  | COREUNITS M WS BS s T W I A Ld Type Page | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 52] | yes |  |
| Soul Grinder | WS3 BS3 S6 T7 W6 I3 A4 Ld7 |  | SOUL GRINDERS | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 57] |  |  |
| Daemon Prince | M8 WS9 BS5 S6 T5 W4 I8 A5 Ld9 |  | Y\Y "V | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] |  |  |
| Keeper of Secrets | M10 WS9 BS6 S6 T6 W5 I10 A6 Ld9 | Mo ExaltedChariot Ch | Y\Y "V | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] | yes |  |
| Ku'gath Plaguefather | M6 WS6 BS3 S6 T7 W7 I4 A6 Ld9 |  | Y\Y "V | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] | yes |  |
| Lord of Change | M8 WS6 BS6 S6 T6 W5 I6 A5 Ld9 |  | Y\Y "V | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] | yes |  |
| Epidemius | M- WS5 BS5 S5 T5 W2 I4 A3 Ld8 |  | Y\Y "V | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] | yes |  |
| Herald of Khorne | M5 WS7 BS7 S5 T4 W2 I6 A3 Ld8 |  | Y\Y "V | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] |  |  |
| Herald of Nurgle | M4 WS5 BS5 S5 T5 W2 I4 A3 Ld8 | Infantry(Character) | Y\Y "V | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] | yes |  |
| Herald of Slaanesh | M6 WS7 BS6 S4 T3 W2 I7 A4 Ld8 |  | Y\Y "V | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] |  |  |
| Herald of Tzeentch | M4 WS3 BS4 S3 T3 W2 I3 A2 Ld8 |  | Y\Y "V | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] |  |  |
| The Masque | M10 WS7 BS6 S4 T3 W2 I7 A5 Ld8 |  | Y\Y "V | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] |  |  |
| Blood Throne | M7 WS5 BS- S5 T5 W4 I2 A3 Ld- |  | Y\Y "V | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] | yes |  |
| Palanquin of Nurgle | M4 WS3 BS3 S3 T3 W4 I3 A6 Ld7 |  | Y\Y "V | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] | yes |  |
| Bloodletter | M5 WS5 BS5 S4 T3 W1 I4 A1 Ld7 |  | Y\Y "V | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] | yes |  |
| Bloodreaper | M5 WS5 BS5 S4 T3 W1 I4 A2 Ld7 |  | Y\Y "V | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] |  |  |
| Beast of Nurgle | M6 WS3 BS0 S4 T5 W4 I2 Ld7 |  | COREUNITS M WS BS s T W I A Ld Type Page | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] |  |  |
| Bloodcrusher | M5 WS5 BS5 S4 T3 W1 I4 A1 Ld7 |  | COREUNITS M WS BS s T W I A Ld Type Page | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] | yes |  |
| Bloodhunter | M5 WS5 BS5 S4 T3 W1 I4 A2 Ld7 |  | COREUNITS M WS BS s T W I A Ld Type Page | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] |  |  |
| Juggernaut | M7 WS5 BS0 S5 T4 W3 I2 A3 Ld7 |  | COREUNITS M WS BS s T W I A Ld Type Page | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] |  |  |
| Chaos Fury | M4 WS3 BS0 S4 T3 W1 I4 A1 Ld2 |  | COREUNITS M WS BS s T W I A Ld Type Page | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] |  |  |
| Fiend of Slaanesh | M10 WS4 BS0 S4 T4 W3 I6 A3 Ld7 |  | COREUNITS M WS BS s T W I A Ld Type Page | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] |  |  |
| Flamer | M6 WS2 BS4 S4 T4 W2 I4 A2 Ld7 |  | COREUNITS M WS BS s T W I A Ld Type Page | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] |  |  |
| Pyrocaster | M6 WS2 BS5 S4 T4 W2 I4 A2 Ld7 |  | COREUNITS M WS BS s T W I A Ld Type Page | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] |  |  |
| Flesh Hound | M8 WS5 BS0 S4 T4 W2 I4 A2 Ld7 |  | COREUNITS M WS BS s T W I A Ld Type Page | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] | yes |  |
| Nurglings | M4 WS3 BS3 S3 T3 W4 I3 A4 Ld7 |  | COREUNITS M WS BS s T W I A Ld Type Page | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] |  |  |
| Steed of Slaanesh | M10 WS3 BS0 S3 T- W- I5 A1 Ld7 |  | COREUNITS M WS BS s T W I A Ld Type Page | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] | yes |  |
| Seeker Chariot | M- WS- BS- S4 T4 W4 I- A- Ld- |  | COREUNITS M WS BS s T W I A Ld Type Page | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] | yes |  |
| Daemonette Crew | M- WS5 BS4 S3 T- W- I5 A2 Ld7 |  | COREUNITS M WS BS s T W I A Ld Type Page | 8th | Armybook_8ed - Daemons of Chaos - 2012 [PDF page 96] |  |  |

## Armybook_8ed - Dwarfs - 2014

| Unit | Profile | Troop Type | Context | Edition | Citation | Rules | Soft |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Lord | M3 WS7 BS4 S4 T5 W3 I4 A4 Ld10 | Infantry(Character) | LORDS 6 THANES | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 37] | yes |  |
| Thane | M3 WS6 BS4 S4 T5 W2 I3 A3 Ld10 | Infantry(Character) | LORDS 6 THANES | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 37] | yes |  |
| Master Engineer | M3 WS4 BS4 S4 T4 W2 I2 A2 Ld9 | Infantry(Character) | MASTER ENGINEERS K | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 38] | yes |  |
| Runelord | M3 WS6 BS4 S4 T5 W3 I3 A2 Ld9 | Infantry(Character) |  | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 39] | yes |  |
| Runesmith | M3 WS5 BS4 S4 T4 W2 I2 A2 Ld9 | Infantry(Character) |  | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 39] | yes |  |
| Quarreller | M3 WS4 BS3 S3 T4 W1 I2 A1 Ld9 | Infantry | QUARRELLERS 6 THUNDERERS ® | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 42] | yes |  |
| Thunderer | M3 WS4 BS3 S3 T4 W1 I2 A1 Ld9 | Infantry | QUARRELLERS 6 THUNDERERS ® | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 42] | yes |  |
| Veteran | M3 WS4 BS3 S3 T4 W1 I2 A2 Ld9 | Infantry | QUARRELLERS 6 THUNDERERS ® | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 42] | yes |  |
| Longbeard | M3 WS5 BS3 S4 T4 W1 I2 A1 Ld9 | Infantry | LONGBEARDS 1S» | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 43] | yes |  |
| Old Guard | M3 WS5 BS3 S4 T4 W1 I2 A2 Ld9 | Infantry | LONGBEARDS 1S» | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 43] | yes |  |
| Hammerer | M3 WS5 BS3 S4 T4 W1 I2 A2 | Infantry | HAMMERERS E | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 44] | yes |  |
| Keeper of the Gate | M3 WS5 BS3 S4 T4 W1 I2 A3 | Infantry | HAMMERERS E | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 44] | yes |  |
| Ironbreaker | M3 WS5 BS3 S4 T4 W1 I2 A1 Ld10 | Infantry | m IRONBREAKERS # | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 45] | yes |  |
| Ironbeard | M3 WS5 BS3 S4 T4 W1 I2 A2 Ld10 | Infantry | m IRONBREAKERS # | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 45] | yes |  |
| Irondrake | M3 WS5 BS3 S4 T4 W1 I2 A1 Ld10 | Infantry | IRONDRAKES | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 46] | yes |  |
| Ironwarden | M3 WS5 BS4 S4 T4 W1 I2 A1 Ld10 | Infantry | IRONDRAKES | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 46] | yes |  |
| Slayer | M3 WS4 BS3 S3 T4 W1 I2 A1 Ld10 | Infantry | SLAYERS S | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 47] | yes |  |
| Giant Slayer | M3 WS5 BS3 S4 T4 W1 I3 A2 Ld10 | Infantry | SLAYERS S | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 47] | yes |  |
| Miner | M3 WS4 BS3 S3 T4 W1 I2 A1 Ld9 | Infantry | MINERS W | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 49] | yes |  |
| Prospector | M3 WS4 BS3 S3 T4 W1 I2 A2 Ld9 | Infantry | MINERS W | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 49] | yes |  |
| Ranger | M3 WS4 BS3 S3 T4 W1 I2 A1 Ld9 | Infantry | RANGERS | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 50] | yes |  |
| Ol'Deadeye | M3 WS4 BS4 S3 T4 W1 I2 A1 Ld9 | Infantry | RANGERS | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 50] | yes |  |
| Grudge Thrower | M- WS- BS- S- T1 W2 | WarMachine (Cannon) | IT DWARF ARTILLERY If | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 51] | yes |  |
| Dwarf Crew | M3 WS4 BS3 S3 T4 W1 I2 A1 Ld9 | WarMachine | ORGAN GUN FLAME CANNON | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 52] | yes |  |
| Bolt Thrower | T7 W3 I- A- Ld- | WarMachine (BoltThrower) | ORGAN GUN FLAME CANNON | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 52] | yes |  |
| Gyrocopter | M1 WS4 BS3 S4 T5 W3 I2 A2 Ld9 | Unique | GYROCOPTERS W | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 53] | yes |  |
| Thronebearers | M3 WS5 BS3 S4 T- W- I3 A4 Ld- |  | THORGRIM GRUDGEBEARER 6r | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 55] | yes |  |
| Ungrim Ironfist | M3 WS9 BS4 S4 T6 W3 I5 A4 Ld10 | Infantry(SpecialCharacter) | UNGRIM IRONFIST ♦ | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 56] | yes |  |
| Belegar Ironhammer | M3 WS8 BS4 S4 T5 W3 I4 A4 Ld10 | Infantry(SpecialCharacter) | BELEGAR IRONHAMMER 0 | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 58] | yes |  |
| Grimm Burloksson | M3 WS4 BS5 S6 T4 W2 I2 A2 Ld9 | Infantry(SpecialCharacter) |  | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 59] | yes |  |
| Josef Bugman | M3 WS6 BS5 S5 T5 W2 I4 A4 Ld10 | Infantry(SpecialCharacter) |  | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 60] | yes |  |
| Daemon Slayer | M3 WS7 BS3 S4 T5 W3 I5 A4 Ld10 |  |  | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 99] |  |  |
| Shieldbearers | M3 WS5 BS3 S4 T- W- I3 A2 Ld- |  |  | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 99] |  |  |
| Anvil Guards | M3 WS5 BS3 S4- T- W2 I2 |  |  | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 99] |  | yes |
| Thorgrim | M3 WS7 BS6 S4 T5 W7 I4 A4 Ld10 |  |  | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 99] |  |  |
| Dragon Slayer | M3 WS6 BS3 S4 T5 W2 I4 A3 Ld10 |  |  | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 99] |  |  |
| Flame Cannon | M- WS- BS- S- T7 W3 I- A- Ld- | WarMachine (FireThrower) | ORGAN GUN FLAME CANNON | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 99] | yes |  |
| Gyrobomber | M1 WS4 BS3 S4 T5 W3 I2 A2 Ld9 | Unique | m GYROBOMBERS | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 99] | yes |  |
| Organ Gun | M- WS- BS- S- T7 W3 I- A- Ld- | WarMachine | ORGAN GUN FLAME CANNON | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 99] | yes |  |
| Dwarf Warrior | M3 WS4 BS3 S3 T4 W1 I2 A1 Ld9 | Key: In=Infantry, WB=WarBeast |  | 8th | Armybook_8ed - Dwarfs - 2014 [PDF page 99] |  |  |

## Armybook_8ed - High Elves

| Unit | Profile | Troop Type | Context | Edition | Citation | Rules | Soft |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Spearman | M5 WS4 BS4 S3 T3 W1 I5 A1 Ld8 | Infantry | SPEARMEN | 8th | Armybook_8ed - High Elves [PDF page 91] (printed p.92) | yes |  |
| Sentinel | M5 WS4 BS4 S3 T3 W1 I5 A2 Ld8 | Infantry | SPEARMEN | 8th | Armybook_8ed - High Elves [PDF page 91] (printed p.92) | yes |  |
| Archer | M5 WS4 BS4 S3 T3 W1 I5 A1 Ld8 | Infantry | ARCHERS | 8th | Armybook_8ed - High Elves [PDF page 91] (printed p.92) | yes |  |
| Hawkeye | M5 WS4 BS5 S3 T3 W1 I5 A1 Ld8 | Infantry | ARCHERS | 8th | Armybook_8ed - High Elves [PDF page 91] (printed p.92) | yes |  |
| Sea Guard | M5 WS4 BS4 S3 T3 W1 I5 A1 Ld8 | Infantry | LOTHERN SEA GUARD | 8th | Armybook_8ed - High Elves [PDF page 91] (printed p.92) | yes |  |
| Sea Master | M5 WS4 BS4 S3 T3 W1 I5 A2 Ld8 | Infantry | LOTHERN SEA GUARD | 8th | Armybook_8ed - High Elves [PDF page 91] (printed p.92) | yes |  |
| Silver Helm | M5 WS4 BS4 S3 T3 W1 I5 A1 Ld8 | Cavalry | SILVER HELMS | 8th | Armybook_8ed - High Elves [PDF page 91] (printed p.92) | yes |  |
| High Helm | M5 WS4 BS4 S3 T3 W1 I5 A2 Ld8 | Cavalry | SILVER HELMS | 8th | Armybook_8ed - High Elves [PDF page 91] (printed p.92) | yes |  |
| Elven Steed | M9 WS3 BS0 S3 T3 W1 I4 A1 Ld5 | - | SILVER HELMS | 8th | Armybook_8ed - High Elves [PDF page 91] (printed p.92) | yes |  |
| Ellyrian Reaver | M5 WS4 BS4 S3 T3 W1 I5 A1 Ld8 | Cavalry | ELLYRIAN REAVERS | 8th | Armybook_8ed - High Elves [PDF page 91] (printed p.92) | yes |  |
| Harbinger | M5 WS4 BS5 S3 T3 W1 I5 A1 Ld8 | Cavalry | ELLYRIAN REAVERS | 8th | Armybook_8ed - High Elves [PDF page 91] (printed p.92) | yes |  |

## Armybook_8ed - Lizardmen

| Unit | Profile | Troop Type | Context | Edition | Citation | Rules | Soft |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Saurus Warrior | M4 WS3 BS0 S4 T4 W1 I1 A2 Ld8 | Infantry | SAURUS WARRIORS | 8th | Armybook_8ed - Lizardmen [PDF page 36] | yes |  |
| Spawn Leader | M4 WS3 BS0 S4 T4 W1 I1 A3 Ld8 | Infantry | SAURUS WARRIORS | 8th | Armybook_8ed - Lizardmen [PDF page 36] | yes |  |
| Cold One Rider | M4 WS4 BS0 S4 T4 W1 I2 A2 Ld8 | Cavalry | COLD ONE RIDERS | 8th | Armybook_8ed - Lizardmen [PDF page 37] | yes |  |
| Pack Leader | M4 WS4 BS0 S4 T4 W1 I2 A3 Ld8 | Cavalry | COLD ONE RIDERS | 8th | Armybook_8ed - Lizardmen [PDF page 37] | yes |  |
| Cold One | M7 WS3 BS- S4 T- W- I2 A2 Ld- | Cavalry | COLD ONE RIDERS | 8th | Armybook_8ed - Lizardmen [PDF page 37] | yes |  |
| Skink Priest | M6 WS2 BS3 S3 T2 W2 I4 A1 Ld6 | Infantry (Character) | SKINK LEADERS | 8th | Armybook_8ed - Lizardmen [PDF page 39] | yes |  |
| Skink Chief | M6 WS4 BS5 S4 T3 W2 I6 A3 Ld6 | Infantry (Character) | SKINK LEADERS | 8th | Armybook_8ed - Lizardmen [PDF page 39] | yes |  |
| Troglodon | M7 WS3 BS3 S5 T5 W5 I2 A3 Ld5 | Monster | UPGRADES | 8th | Armybook_8ed - Lizardmen [PDF page 40] | yes |  |
| Skink | M6 WS2 BS3 S3 T2 W1 I4 A1 Ld5 |  | SKINKS | 8th | Armybook_8ed - Lizardmen [PDF page 41] | yes |  |
| Skink Brave | M6 WS2 BS3 S3 T2 W1 I4 A2 Ld5 |  | SKINKS | 8th | Armybook_8ed - Lizardmen [PDF page 41] | yes |  |
| Skink Skirmisher | M6 WS2 BS3 S3 T2 W1 I4 A1 Ld5 |  | SKINKS | 8th | Armybook_8ed - Lizardmen [PDF page 41] | yes |  |
| Kroxigor | M6 WS3 BS0 S5 T4 W3 I1 A3 Ld7 | Monstrous Infantry |  | 8th | Armybook_8ed - Lizardmen [PDF page 43] | yes |  |
| Kroxigor Ancient | M6 WS3 BS0 S5 T4 W3 I1 A4 Ld7 | Monstrous Infantry | KROXIGOR | 8th | Armybook_8ed - Lizardmen [PDF page 43] | yes |  |
| Sky Leader | M6 WS2 BS4 S3 T2 W1 I4 A1 Ld5 | Monstrous Cavalry | TERRADON RIDERS | 8th | Armybook_8ed - Lizardmen [PDF page 45] | yes |  |
| Terradon | M2 WS3 BS0 S4 T3 W2 I2 A1 Ld3 | Monstrous Cavalry | TERRADON RIDERS | 8th | Armybook_8ed - Lizardmen [PDF page 45] | yes |  |
| Ripperdactyl Rider | M6 WS2 BS3 S3 T2 W1 I4 A1 Ld5 | Monstrous Cavalry | RIPPERDACTYL RIDERS | 8th | Armybook_8ed - Lizardmen [PDF page 46] | yes |  |
| Ripperdacytl Brave | M6 WS2 BS3 S3 T2 W1 I4 A2 Ld5 | Monstrous Cavalry | RIPPERDACTYL RIDERS | 8th | Armybook_8ed - Lizardmen [PDF page 46] | yes |  |
| Ripperdactyl | M2 WS3 BS0 S4 T3 W2 I3 A2 Ld3 | Monstrous Cavalry | RIPPERDACTYL RIDERS | 8th | Armybook_8ed - Lizardmen [PDF page 46] | yes |  |
| Stegadon | M6 WS3 BS0 S5 T6 W5 I2 A4 Ld6 | Monster |  | 8th | Armybook_8ed - Lizardmen [PDF page 48] | yes |  |
| Ancient Stegadon | M6 WS3 BS0 S6 T6 W5 I1 A3 Ld6 | Monster |  | 8th | Armybook_8ed - Lizardmen [PDF page 48] | yes |  |
| Skink Crew | M- WS2 BS3 S3 T- W- I4 A1 Ld- | Monster |  | 8th | Armybook_8ed - Lizardmen [PDF page 48] | yes |  |
| Salamander | M6 WS3 BS3 S5 T4 W3 I4 A2 Ld4 | Monstrous Beast | SALAMANDER HUNTING PACKS | 8th | Armybook_8ed - Lizardmen [PDF page 49] | yes |  |
| Skink Handler | M6 WS2 BS3 S3 T2 W1 I4 A1 Ld5 | Monstrous Beast | SALAMANDER HUNTING PACKS | 8th | Armybook_8ed - Lizardmen [PDF page 49] | yes |  |
| Carnosaur | M7 WS3 BS0 S7 T5 W5 I2 A4 Ld5 | Monster | CARNOSAURS | 8th | Armybook_8ed - Lizardmen [PDF page 53] | yes |  |
| Kroq-Gar | M4 WS6 BS0 S5 T5 W3 I3 A5 Ld8 | Infantry (Special Character) |  | 8th | Armybook_8ed - Lizardmen [PDF page 54] | yes |  |
| Grymloq | M7 WS3 BS0 S7 T5 W5 I2 A5 Ld5 | Key: In=Infantry,WB= WarBeast |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |
| Lord Kroak | M4 WS1 BS1 S3 T5 W6 I1 A1 Ld9 | Key: In=Infantry,WB= WarBeast |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |
| Lord Mazdamundi | M4 WS2 BS3 S3 T4 W5 I2 A1 Ld9 | Key: In=Infantry,WB= WarBeast |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] | yes |  |
| Zlaaq | M6 WS3 BS0 S6 T6 I1 A3 Ld6 | Key: In=Infantry,WB= WarBeast |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] | yes |  |
| Saurus Oldblood | M4 WS6 BS0 S5 T5 W3 I3 A5 Ld8 | Key: In=Infantry,WB= WarBeast |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |
| Slann Mage-Priest | M4 WS2 BS3 S3 T4 W5 I2 A1 Ld9 | In Troop Type Key: In Infantry,WB WarBeast |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |
| Tehenhauin | M6 WS6 BS5 S4 T3 W3 I6 A3 Ld8 | Key: In=Infantry,WB= WarBeast |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |
| Chakax | M4 WS5 BS0 S5 T5 W2 I3 A4 Ld8 | In(SC) WM WarMachine |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |
| Gor-Rok | M4 WS5 BS0 S5 T6 W2 I3 A4 Ld8 |  |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |
| Oxyotl | M6 WS4 BS6 S4 T3 W2 I6 A3 Ld7 |  |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |
| Saurus Scar-Veteran | M4 WS5 BS0 S5 T5 W2 I3 A4 Ld8 |  |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |
| Tetto'eko | M6 WS2 BS3 S2 T2 W2 I4 A1 Ld6 |  |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |
| Tiktaq'to | M6 WS4 BS5 S4 T3 W2 I6 A3 Ld7 |  |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |
| Patrol Leader | M6 WS2 BS4 S3 T2 W1 I4 A1 Ld5 |  |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |
| Bastiladon | M4 WS3 BS0 S4 T5 W4 I1 A3 Ld6 |  |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |
| Chameleon Skink | M6 WS2 BS4 S3 T2 W1 I4 A1 Ld5 |  |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |
| Stalker | M6 WS2 BS5 S3 T2 W1 I4 A1 Ld5 |  |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |
| Jungle Swarm | M5 WS3 BS0 S2 T2 W5 I1 A5 Ld10 |  |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |
| Ripperdacyd Brave | M6 WS2 BS3 S3 T2 W1 I4 A2 Ld5 |  |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |
| Temple Guard | M4 WS4 BS0 S4 T4 W1 I2 A2 Ld8 |  |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |
| Revered Guardian | M4 WS4 BS0 S4 T4 W1 I2 A3 Ld8 |  |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |
| Terradon Rider | M6 WS2 BS3 S3 T2 W1 I4 A1 Ld5 | Monstrous Cavalry | TERRADON RIDERS | 8th | Armybook_8ed - Lizardmen [PDF page 99] | yes |  |
| Razordon | M6 WS3 BS3 S5 T4 W3 I4 A2 Ld4 |  |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |
| Skink Oracle Rider | M- WS2 BS3 S3 T- W- I4 A1 Ld6 |  |  | 8th | Armybook_8ed - Lizardmen [PDF page 99] |  |  |

## Armybook_8ed - Vampire Counts

| Unit | Profile | Troop Type | Context | Edition | Citation | Rules | Soft |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Vampires | M6 WS7 BS5 S5 T5 W3 I7 A5 Ld10 | Infantry(Character) | VAMPIRES | 8th | Armybook_8ed - Vampire Counts [PDF page 30] | yes |  |
| Vampire | M6 WS6 BS4 S5 T4 W2 I6 A4 Ld7 | Infantry(Character) | VAMPIRES | 8th | Armybook_8ed - Vampire Counts [PDF page 30] | yes |  |
| Master Necromancer | M4 WS3 BS3 S3 T4 W3 I3 A1 Ld8 | Infantry(Character) | NECROMANCERS | 8th | Armybook_8ed - Vampire Counts [PDF page 31] | yes |  |
| Necromancer | M4 WS3 BS3 S3 T3 W2 I3 A1 Ld7 | Infantry(Character) | NECROMANCERS | 8th | Armybook_8ed - Vampire Counts [PDF page 31] | yes |  |
| Wight King | M4 WS4 BS0 S4 T5 W3 I4 A3 Ld9 | Infantry(Character) | WIGHT KINGS | 8th | Armybook_8ed - Vampire Counts [PDF page 32] | yes |  |
| Tomb Banshee | M6 WS3 BS0 S3 T3 W2 I3 A1 Ld5 | Infantry(Character) | TOMB BANSHEES | 8th | Armybook_8ed - Vampire Counts [PDF page 34] | yes |  |
| Crypt Ghoul | M4 WS3 BS0 S3 T4 W-1 I3 A2 Ld5 | Key: ln=lnfontry,WB=WarBeast,Ca= Cavalry | CRYPT GHOULS | 8th | Armybook_8ed - Vampire Counts [PDF page 36] | yes |  |
| Crypt Ghast | M4 WS3 BS0 S3 T4 I3 A3 Ld5 | Key: ln=lnfontry,WB=WarBeast,Ca= Cavalry | CRYPT GHOULS | 8th | Armybook_8ed - Vampire Counts [PDF page 36] | yes |  |
| Skeleton Warrio | M-4 WS2 BS2 S3 T3 W1 I2 A1 Ld3 | Infantry | SKELETON WARRIORS | 8th | Armybook_8ed - Vampire Counts [PDF page 38] | yes |  |
| Skeleton Champion | M4 WS2 BS2 S3 T3 I2 A2 Ld3 | Infantry | SKELETON WARRIORS | 8th | Armybook_8ed - Vampire Counts [PDF page 38] | yes |  |
| Dire Wolf | M9 WS3 BS0 S3 T3 W1 I3 A1 Ld3 | WarBeasts | DIRE WOLVES | 8th | Armybook_8ed - Vampire Counts [PDF page 39] | yes |  |
| Doom Wolf | M9 WS3 BS0 S3 T3 I3 A2 Ld3 | WarBeasts | DIRE WOLVES | 8th | Armybook_8ed - Vampire Counts [PDF page 39] | yes |  |
| Bat Swarm | M1 WS3 BS0 S2 T2 W5 I4 A5 Ld3 | Swarm | BAT SWARMS | 8th | Armybook_8ed - Vampire Counts [PDF page 40] | yes |  |
| Bat Swarms | M1 WS3 BS0 S3 T3 W2 I3 A2 Ld3 | WarBeasts | BAT SWARMS | 8th | Armybook_8ed - Vampire Counts [PDF page 40] | yes |  |
| Grave Guard | M4 WS3 BS0 S4 T4 W1 I3 Ld6 | Infantry |  | 8th | Armybook_8ed - Vampire Counts [PDF page 41] | yes |  |
| Seneschal | M4 WS3 BS0 S4 T4 I3 A2 Ld6 | Infantry | GRAVE GUARD | 8th | Armybook_8ed - Vampire Counts [PDF page 41] | yes |  |
| Black Knight | M4 WS3 BS0 S4 T4 W1 I3 A1 Ld6 | Cavalry | BLACK KNIGHTS | 8th | Armybook_8ed - Vampire Counts [PDF page 42] | yes |  |
| Hell Knight | M4 WS3 BS0 S4 T4 I3 A2 Ld6 | Cavalry | BLACK KNIGHTS | 8th | Armybook_8ed - Vampire Counts [PDF page 42] | yes |  |
| Spirit Host | M6 WS3 BS0 S3 T3 W4 A4 Ld4 | Swarm | SPIRIT HOSTS | 8th | Armybook_8ed - Vampire Counts [PDF page 44] | yes |  |
| Crypt Horror | M6 WS3 BS0 S4 T5 W3 I2 A3 Ld5 | MonstrousInfantry | CRYPT HORRORS | 8th | Armybook_8ed - Vampire Counts [PDF page 45] | yes |  |
| Crypt Haunter | M6 WS3 BS0 S4 T5 W3 I2 A4 Ld5 | MonstrousInfantry | CRYPT HORRORS | 8th | Armybook_8ed - Vampire Counts [PDF page 45] | yes |  |
| Vargheist | M6 WS4 BS-0 S5 T4 W3 I4 A3 Ld7 | Monstrous Infantry | VARGHEISTS | 8th | Armybook_8ed - Vampire Counts [PDF page 46] | yes |  |
| Vargoyle | M6 WS4 BS0 S5 T4 W3 I4 A4 Ld7 | Monstrous Infantry | VARGHEISTS | 8th | Armybook_8ed - Vampire Counts [PDF page 46] | yes |  |
| Varghulf | M8 WS5 BS0 S5 T5 W4 I4 A5 Ld4 | Monster | VARGHULFS | 8th | Armybook_8ed - Vampire Counts [PDF page 47] | yes |  |
| Blood Knights | M-4 WS5 BS3 S5 T4 W1 I5 A2 Ld7 | Cavalry | BLOOD KNIGHTS | 8th | Armybook_8ed - Vampire Counts [PDF page 48] | yes |  |
| Kastellan | M4 WS5 BS3 S5 T4 W1 I5 A3 Ld7 | Cavalry | BLOOD KNIGHTS | 8th | Armybook_8ed - Vampire Counts [PDF page 48] | yes |  |
| Nightmare | M8 WS3 BS0 S4 T4 W1 I2 A1 Ld3 | Cavalry | BLOOD KNIGHTS | 8th | Armybook_8ed - Vampire Counts [PDF page 48] | yes |  |
| Hexwraith | M6 WS3 BS0 S3 T3 W1 I2 A1 Ld5 | Cavalry | HEXWRAITHS | 8th | Armybook_8ed - Vampire Counts [PDF page 50] | yes |  |
| Hellwraith | M6 WS3 BS0 S3 T3 I2 A2 Ld5 | Cavalry | HEXWRAITHS | 8th | Armybook_8ed - Vampire Counts [PDF page 50] | yes |  |
| Terrorgheist | M-6 WS3 BS0 S5 T6 W6 I3 A4 Ld4 | Monster | TERRORGHEISTS | 8th | Armybook_8ed - Vampire Counts [PDF page 51] | yes |  |
| Hellsteed | M8 WS3 BS0 S4 T4 W1 I2 A1 Ld3 | WarBeast | NIGHTMARES | 8th | Armybook_8ed - Vampire Counts [PDF page 53] | yes |  |
| Skeletal Steed | M8 WS2 BS0 S3 T3 W1 I2 A1 Ld3 | WarBeast | SKELETAL STEEDS | 8th | Armybook_8ed - Vampire Counts [PDF page 54] | yes |  |
| Coven Throne | WS- S5 T5 W5 | Chariot(ArmourSave 5+) | COVEN THRONES | 8th | Armybook_8ed - Vampire Counts [PDF page 55] | yes |  |
| Spirit Horde | M8 WS3 BS0 S3 Ld- | Chariot(ArmourSave 5+) | COVEN THRONES | 8th | Armybook_8ed - Vampire Counts [PDF page 55] | yes |  |
| Corpsemaster | WS3 BS0 S3 A1 Ld5 | Chariot(ArmourSave5+) | MORTIS ENGINES | 8th | Armybook_8ed - Vampire Counts [PDF page 56] | yes |  |
| Banshee Swarm | WS3 BS0 S3 A3 | Chariot(ArmourSave5+) | MORTIS ENGINES | 8th | Armybook_8ed - Vampire Counts [PDF page 56] | yes |  |
| Konrad von Carstein | M6 WS7 BS4 S5 T4 W2 I6 A4 Ld6 | Infantry(SpecialCharacter,Vampire) |  | 8th | Armybook_8ed - Vampire Counts [PDF page 60] | yes |  |
| Heinrich Kemmler | M-4 WS4 BS3 S4 T4 W3 I4 A1 Ld8 | Infantry | HEINRICH KEMMLER | 8th | Armybook_8ed - Vampire Counts [PDF page 61] | yes |  |
| Abyssal Terror | M6 WS4 BS0 S5 T5 W4 I2 A3 Ld4 | Monster Fly,LargeTarget,Terror, Undead | CHARACTER MOUNTS | 8th | Armybook_8ed - Vampire Counts [PDF page 92] | yes |  |
| Terrorgheist | M6 WS3 BS0 S5 T6 W6 I3 A4 Ld4 | Monster DeathShriek, Fly,LargeTarget | CHARACTER MOUNTS | 8th | Armybook_8ed - Vampire Counts [PDF page 92] | yes |  |
| Zombie Dragon | M6 WS4 BS0 S6 T6 W6 I2 A5 Ld4 | Monster Fly,LargeTarget,PestilentialBreath | CHARACTER MOUNTS | 8th | Armybook_8ed - Vampire Counts [PDF page 92] | yes |  |
| Heinrich Kemmler | M4 WS4 BS3 S4 T4 W3 I4 |  |  | 8th | Armybook_8ed - Vampire Counts [PDF page 99] | yes |  |
| Strigoi Ghoul King | M6 WS6 BS3 W3 Ld9 |  |  | 8th | Armybook_8ed - Vampire Counts [PDF page 99] |  |  |
| Vlad von Carstein | M6 WS7 W3 I7 Ld10 |  |  | 8th | Armybook_8ed - Vampire Counts [PDF page 99] |  |  |
| Cairn Wraith | M6 WS3 BS0 S3 T3 W2 I2 Ld5 |  |  | 8th | Armybook_8ed - Vampire Counts [PDF page 99] |  |  |
| Isabella von Carstein | M6 WS6 BS4 S5 T4 W2 I6 A4 Ld7 |  |  | 8th | Armybook_8ed - Vampire Counts [PDF page 99] |  |  |
| Krell | M4 WS5 BS0 S4 T5 W4 A3 Ld9 |  |  | 8th | Armybook_8ed - Vampire Counts [PDF page 99] |  |  |
| Mannfred the Acolyte | M6 WS6 BS4 T4 W2 I6 A4 Ld7 |  |  | 8th | Armybook_8ed - Vampire Counts [PDF page 99] |  |  |
| Pallid Handmaiden | WS5 BS3 S5 W- I5 A2 Ld7 | Chariot(ArmourSave 5+) | COVEN THRONES | 8th | Armybook_8ed - Vampire Counts [PDF page 99] | yes |  |
| Spirit Horde | WS3 BS0 S3 I1 A2D6 |  |  | 8th | Armybook_8ed - Vampire Counts [PDF page 99] |  |  |
| Terrorgheist | M6 WS3 BS0 I2 A4 Ld4 |  |  | 8th | Armybook_8ed - Vampire Counts [PDF page 99] | yes |  |
| Skeleton Warrior | M4 WS2 BS2 S3 T3 I2 | Key: ln=lnfontry,WB=WarBeast,Ca= Cavalry |  | 8th | Armybook_8ed - Vampire Counts [PDF page 99] |  |  |

## Armybook_8ed - Warriors of Chaos 2012

| Unit | Profile | Troop Type | Context | Edition | Citation | Rules | Soft |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Exalted Hero | M4 WS7 BS3 S5 T4 W2 I6 A4 Ld8 | Infantry(Character) | CHAOS LORDS | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 27] | yes |  |
| Palanquin of Nurgle | M4 WS3 BS3 S3 T3 W4 I3 A6 Ld7 | MonstrousBeast | DISCS OFTZEENTCH | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 30] | yes |  |
| Chaos Warrior | M4 WS5 BS3 S4 T4 W1 I5 A2 Ld8 | Infantry | CHAOS WARRIORS | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 32] | yes |  |
| Aspiring Champion | M4 WS5 BS3 S4 T4 W1 I5 A3 Ld8 | Infantry | CHAOS WARRIORS | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 32] | yes |  |
| Chosen | M4 WS6 BS3 S4 T4 W1 I5 A2 Ld8 | Infantry | CHAOS WARRIORS | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 32] | yes |  |
| Chosen Champion | M4 WS6 BS3 S4 T4 W1 I5 A3 Ld8 | Infantry | CHAOS WARRIORS | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 32] | yes |  |
| Marauder Horseman | M4 WS4 BS3 S3 T3 W1 I4 A1 Ld7 | Cavalry | CHAOS MARAUDERS | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 33] | yes |  |
| Marauder Horsemaster | M4 WS4 BS3 S3 T3 W1 I4 A2 Ld7 | Cavalry | CHAOS MARAUDERS | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 33] | yes |  |
| Warhorse | M8 WS3 BS0 S3 T3 W1 I3 A1 Ld5 | Cavalry | CHAOS MARAUDERS | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 33] | yes |  |
| Steed of Slaanesh | M10 WS3 BS0 S3 T3 W1 I5 A1 Ld7 | WarBeast | HELLSTRIDERS OF SLAANESH | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 34] | yes |  |
| Chaos Knight | M4 WS5 BS3 S4 T4 W1 I5 A2 Ld8 | Cavalry | CHAOS KNIGHTS | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 35] | yes |  |
| Doom Knight | M4 WS5 BS3 S4 T4 W1 I5 A3 Ld8 | Cavalry | CHAOS KNIGHTS | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 35] | yes |  |
| Chaos Steed | M8 WS3 BS0 S4 T3 W1 I3 A1 Ld5 | Cavalry | CHAOS KNIGHTS | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 35] | yes |  |
| Juggernaut of Khorne | M7 WS5 BS0 S5 T4 W3 I2 A3 Ld7 | Monstrous Beast | SKULLCRUSHERS OF KHORNE | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 36] | yes |  |
| Forsaken | M6 WS4 BS0 S4 T4 W1 I4 AD3 Ld8 | Infantry |  | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 39] | yes |  |
| Chaos Spawn | M2D6 WS3 BS0 S4 T5 W3 I2 | Monstrous Beast |  | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 40] | yes |  |
| Chaos Warhound | M7 WS4 BS0 S3 T3 W1 I3 A1 Ld5 | WarBeast | WARHOUNDS | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 40] | yes |  |
| Chaos Ogre | M6 WS3 BS2 S4 T4 W3 I2 A3 Ld7 | Monstrous Infantry | CHAOS OGRES | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 41] | yes |  |
| Ogre Mutant | M6 WS3 BS2 S4 T4 W3 I2 A4 Ld7 | Monstrous Infantry | CHAOS OGRES | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 41] | yes |  |
| Dragon Ogre | M7 WS4 BS2 S5 T4 W4 I2 A3 Ld8 | Monstrous Beast | DRAGON OGRES | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 42] | yes |  |
| Dragon Ogre Shartak | M7 WS4 BS2 S5 T4 W4 I2 A4 Ld8 | Monstrous Beast | DRAGON OGRES | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 42] | yes |  |
| Dragon Ogre Shaggoth | M7 WS6 BS3 S6 T5 W6 I4 A5 Ld9 | Monster | DRAGON OGRE | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 42] | yes |  |
| Hellcannon | M3 WS4 BS3 S5 T6 W5 I1 A5 Ld4 |  |  | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 43] | yes |  |
| Chaos Dwarf Handlers | M3 WS4 BS3 S3 T4 W1 I2 A1 Ld9 |  |  | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 43] | yes |  |
| Chaos Shrinemaster | M- WS5 BS3 S4 T- I5 A*2 Ld8 | Chariot (Armour Save 4+) | CHAOS WARSHRINES | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 44] | yes |  |
| Chaos Shrine Bearers | M6 WS3 BS3 S4 T- W- A6+2- | Chariot (Armour Save 4+) | CHAOS WARSHRINES | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 44] | yes |  |
| Vilitch the Curseling | M4 WS5 BS3 S5 T4 W3 I5 A3 Ld8 |  |  | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 52] | yes |  |
| Scyla Anfingrimm | M6 WS4 BS0 S5 T5 W4 I3 | Monstrous Beast(Special Character) |  | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 56] |  |  |
| Chaos Troll | M6 WS3 BS1 S5 T4 W3 I1 A3 Ld4 |  |  | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] |  |  |
| Chaos Warshrine | M- WS- BS- S- T5 W5 I- A- Ld- | Chariot (Armour Save 4+) | CHAOS WARSHRINES | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] | yes |  |
| Chaos Shrinemaster | M- WS5 BS3 S4 T- W- I5 A2 Ld8 |  |  | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] | yes |  |
| Chaos Shrine Bearers | M6 WS3 BS3 S4 T- W- A6+2 Ld- |  |  | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] | yes |  |
| Chimera | M6 WS4 BS0 S6 T5 W4 I2 A6 Ld5 |  |  | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] |  |  |
| Chaos Sorcerer | M4 WS5 BS3 S4 T4 W2 I5 A2 Ld8 | In GorebeastChariot Ch |  | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] |  |  |
| Festus the Leechlord | M4 WS4 BS2 S4 T4 W2 I2 A2 Ld8 | InSC I Gorebeast |  | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] |  |  |
| Scyla Anfingrimm | M6 WS4 BS0 S5 T5 W4 I3D6 A2 Ld10 |  |  | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] |  |  |
| Throgg | M6 WS5 BS2 S6 T5 W4 I2 A5 Ld8 |  |  | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] |  |  |
| Wulfrik the Wanderer | M4 WS8 BS3 S5 T4 W2 I7 A4 Ld8 |  |  | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] |  |  |
| Chaos Chariot | M- WS- BS- S5 T5 W4 I- A- Ld- |  | CORE MOUNTS | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] |  |  |
| Chaos Charioteer | M- WS5 BS3 S4 T- W- I5 A2 Ld8 |  | CORE MOUNTS | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] |  |  |
| Chaos Steed | M8 WS3 BS- S4 T- W- I3 A1 Ld- |  | CORE MOUNTS | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] | yes |  |
| Chaos Marauder | M4 WS4 BS3 S3 T3 W1 I4 A1 Ld7 |  | CORE MOUNTS | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] |  |  |
| Marauder Chieftain | M4 WS4 BS3 S3 T3 W1 I4 A2 Ld7 |  | CORE MOUNTS | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] |  |  |
| Chaos Giant | M6. WS3 BS3 S6 T5 W6 I3 Ld10 |  | TEMPLATE | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] |  |  |
| Chaos Spawn | M2D6 WS3 BS0 S4 T5 W3 A6+1 Ld10 |  | TEMPLATE | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] | yes |  |
| Mutalith Vortex Beast | M6 WS3 BS0 S5 T5 W5 A6+2 Ld8 |  | TEMPLATE | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] |  |  |
| Skullcrusher | M4 WS5 BS3 S4 T4 W1 I5 A2 Ld8 |  | TEMPLATE | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] |  |  |
| Skullhunter | M4 WS5 BS3 S4 T4 W1 I5 A3 Ld8 |  | TEMPLATE | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] |  |  |
| Slaughterbrute | M6 WS3 BS0 S7 T5 W5 I3 A4 Ld5 |  | TEMPLATE | 8th | Armybook_8ed - Warriors of Chaos 2012 [PDF page 97] |  |  |

## Armybook_8ed - Wood Elves

| Unit | Profile | Troop Type | Context | Edition | Citation | Rules | Soft |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Spellsinger | M5 WS4 BS4 S3 T3 W2 I5 A1 Ld8 |  | ISHA,THEMOTHER | 8th | Armybook_8ed - Wood Elves [PDF page 42] | yes |  |
| Eternal Guard | M5 WS5 BS4 S3 T3 W1 I5 A1 Ld9 | Infantry |  | 8th | Armybook_8ed - Wood Elves [PDF page 43] | yes |  |
| Eternal Warden | M5 WS5 BS4 S3 T3 W1 I5 A2 Ld9 | Infantry | ETERNAL GUARD | 8th | Armybook_8ed - Wood Elves [PDF page 43] | yes |  |
| Deepwood Scout | M5 WS4 BS4 S3 T3 W1 I5 A1 Ld8 | Infantry | GLADE GUARD | 8th | Armybook_8ed - Wood Elves [PDF page 44] | yes |  |
| Master Scout | M5 WS4 BS5 S3 T3 W1 I5 A1 Ld8 | Infantry | GLADE GUARD | 8th | Armybook_8ed - Wood Elves [PDF page 44] | yes |  |
| Glade Guard | M5 WS4 BS4 S3 T3 W1 I5 A1 Ld8 | Infantry |  | 8th | Armybook_8ed - Wood Elves [PDF page 44] | yes |  |
| Lord's Bowman | M5 WS4 BS5 S3 T3 W1 I5 A1 Ld8 | Infantry | GLADE GUARD | 8th | Armybook_8ed - Wood Elves [PDF page 44] | yes |  |
| Glade Rider | M5 WS4 BS4 S3 T3 W1 | Cavalry | KNIGHTS OF ATHEL LOREN | 8th | Armybook_8ed - Wood Elves [PDF page 45] | yes |  |
| Glade Knight | M5 WS4 BS5 S3 T3 W1 | Cavalry | KNIGHTS OF ATHEL LOREN | 8th | Armybook_8ed - Wood Elves [PDF page 45] | yes |  |
| Unicorn | M10 WS5 BS0 S4 T4 W3 I5 A2 Ld8 | Monstrous Beast | KNIGHTS OF ATHEL LOREN | 8th | Armybook_8ed - Wood Elves [PDF page 45] | yes |  |
| Wind Rider | M5 WS4 BS4 S3 T3 W1 I5 A2 Ld8 | MonstrousCavalry | WARHAWKRIDERS | 8th | Armybook_8ed - Wood Elves [PDF page 46] | yes |  |
| Warhawk | M1 WS4 BS0 S4 T4 W3 I5 A2 Ld5 | MonstrousCavalry | WARHAWKRIDERS | 8th | Armybook_8ed - Wood Elves [PDF page 46] | yes |  |
| Great Eagle | M2 WS5 BS0 S4 T4 W3 I4 A2 Ld8 | Monstrous Beast | WARHAWKRIDERS | 8th | Armybook_8ed - Wood Elves [PDF page 46] | yes |  |
| Wildwood Ranger | M5 WS5 BS4 S3 T3 W1 I5 A1 Ld9 | Infantry | WILDWOOD RANGERS | 8th | Armybook_8ed - Wood Elves [PDF page 47] | yes |  |
| Wildwood Warden | M5 WS5 BS4 S3 T3 W1 I5 A2 Ld9 | Infantry | WILDWOOD RANGERS | 8th | Armybook_8ed - Wood Elves [PDF page 47] | yes |  |
| Shadowdancer | M5 WS8 BS6 S4 T3 W2 I8 A3 Ld8 | Infantry(Character) | WARDANCERS | 8th | Armybook_8ed - Wood Elves [PDF page 48] | yes |  |
| Wardancer | M5 WS6 BS4 S3 T3 W1 I6 A1 Ld8 | Infantry | WS BS S T W I A Ld | 8th | Armybook_8ed - Wood Elves [PDF page 48] | yes |  |
| Bladesinger | M5 WS6 BS4 S3 T3 W1 I6 A2 Ld8 | Infantry | WS BS S T W I A Ld | 8th | Armybook_8ed - Wood Elves [PDF page 48] | yes |  |
| Sister of the Thorn | M5 WS4 BS5 S3 T3 W1 I5 A1 Ld9 | Cavalry | SISTERS OF THE THORN | 8th | Armybook_8ed - Wood Elves [PDF page 49] | yes |  |
| Steed of Isha | M9 WS3 BS0 S4 T3 W1 I4 A1 Ld5 | Cavalry | SISTERS OF THE THORN | 8th | Armybook_8ed - Wood Elves [PDF page 49] | yes |  |
| Great Stag | M9 WS5 BS0 S5 T4 W3 I4 A2 Ld7 | Monstrous Beast | WILD RIDERS | 8th | Armybook_8ed - Wood Elves [PDF page 50] | yes |  |
| Wild Rider | M5 WS5 BS4 S4 T3 W1 I5 A1 Ld9 |  | WILD RIDERS | 8th | Armybook_8ed - Wood Elves [PDF page 50] | yes |  |
| Wild Hunter | M5 WS5 BS4 S4 T3 W1 I5 A2 Ld9 |  | WILD RIDERS | 8th | Armybook_8ed - Wood Elves [PDF page 50] | yes |  |
| Steed of Kurnous | M9 WS3 BS0 S4 T3 W1 I4 A1 Ld5 |  | WILD RIDERS | 8th | Armybook_8ed - Wood Elves [PDF page 50] | yes |  |
| Waywatcher | M5 WS4 BS5 S3 T3 W1 I5 A1 Ld8 | Infantry | WAYWATCHERS | 8th | Armybook_8ed - Wood Elves [PDF page 51] | yes |  |
| Waywatcher Sentinel | M5 WS4 BS6 S3 T3 W1 I5 A1 Ld8 | Infantry | WAYWATCHERS | 8th | Armybook_8ed - Wood Elves [PDF page 51] | yes |  |
| Waystalker | M5 WS6 BS7 S4 T3 W2 I7 A1 Ld8 | Infantry (Character) | WAYWATCHERS | 8th | Armybook_8ed - Wood Elves [PDF page 51] | yes |  |
| Branchwraith | M5 WS6 BS6 S4 T4 W2 I7 A3 Ld9 | Infantry (Character) | DRYADS | 8th | Armybook_8ed - Wood Elves [PDF page 52] | yes |  |
| Dryad | M5 WS4 BS4 S3 T4 W1 I5 A2 Ld8 | Infantry | DRYADS | 8th | Armybook_8ed - Wood Elves [PDF page 52] | yes |  |
| Branch Nymph | M5 WS4 BS4 S3 T4 W1 I5 A3 Ld8 | Infantry | DRYADS | 8th | Armybook_8ed - Wood Elves [PDF page 52] | yes |  |
| Treeman | M5 WS6 BS6 S5 T6 W5 I2 A5 Ld9 | Monster | TREEMANANCIENTS | 8th | Armybook_8ed - Wood Elves [PDF page 54] | yes |  |
| Treeman Ancient | M5 WS4 BS4 S5 T6 W6 I2 A3 Ld10 | Monster(Character) | TREEMANANCIENTS | 8th | Armybook_8ed - Wood Elves [PDF page 54] | yes |  |
| Orion | M9 WS8 BS8 S6 T5 W5 I9 A5 Ld10 | Monster (Special Character) |  | 8th | Armybook_8ed - Wood Elves [PDF page 58] | yes |  |
| Hound of Orion | M9 WS4 BS0 S4 T4 W1 I4 A1 Ld6 | Monster (Special Character) |  | 8th | Armybook_8ed - Wood Elves [PDF page 58] | yes |  |
| Araloth | M5 WS8 BS7 S4 T3 W3 I8 A5 Ld10 | Infantry (SpecialCharacter) |  | 8th | Armybook_8ed - Wood Elves [PDF page 59] | yes |  |
| Naestra | M5 WS6 BS6 S4 T3 W2 I7 A3 Ld9 | Infantry (SpecialCharacter) |  | 8th | Armybook_8ed - Wood Elves [PDF page 62] | yes |  |
| Ceithin-Har | M6 WS6 BS0 S6 T6 W6 I3 A5 Ld8 | Infantry (SpecialCharacter) |  | 8th | Armybook_8ed - Wood Elves [PDF page 62] | yes |  |
| Gwindalor | M2 WS5 BS0 S4 T4 W3 I4 A2 Ld8 | Infantry (SpecialCharacter) |  | 8th | Armybook_8ed - Wood Elves [PDF page 62] | yes |  |
| Handmaiden of the Thorn | M5 WS4 BS6 S3 T3 W1 I5 A1 Ld9 | Cavalry |  | 8th | Armybook_8ed - Wood Elves [PDF page 97] |  |  |
| Durthu | M5 WS7 BS7 S6 T6 W6 I2 A6 Ld10 |  |  | 8th | Armybook_8ed - Wood Elves [PDF page 99] |  |  |
| Glade Lord | M5 WS7 BS7 S4 T3 W3 I8 A4 Ld10 | Infantry (Character) | HIGHBORN OF ATHEL LOREN | 8th | Armybook_8ed - Wood Elves [PDF page 99] | yes |  |
| Spellweaver | M5 WS4 BS4 S3 T3 W3 I5 A1 Ld9 |  |  | 8th | Armybook_8ed - Wood Elves [PDF page 99] |  |  |
| Drycha | M5 WS7 BS5 S4 T4 W3 I7 A4 Ld9 |  |  | 8th | Armybook_8ed - Wood Elves [PDF page 99] |  |  |
| Glade Captain | M5 WS6 BS6 S4 T3 W2 I7 A3 Ld9 | Infantry (Character) | HIGHBORN OF ATHEL LOREN | 8th | Armybook_8ed - Wood Elves [PDF page 99] | yes |  |
| Arahan | M5 WS6 BS6 S4 T3 W2 I7 A3 Ld9 |  |  | 8th | Armybook_8ed - Wood Elves [PDF page 99] |  |  |
| Elven Steed | M9 WS3 BS0 S3 T3 W1 I4 A1 Ld5 | Cavalry | KNIGHTS OF ATHEL LOREN | 8th | Armybook_8ed - Wood Elves [PDF page 99] | yes |  |
| Forest Dragon | M6 WS6 BS0 S6 T6 W6 I3 A5 Ld8 |  |  | 8th | Armybook_8ed - Wood Elves [PDF page 99] |  |  |
