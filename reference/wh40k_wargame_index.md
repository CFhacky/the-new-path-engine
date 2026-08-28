# Warhammer 40,000 Wargame -- Unit Profile Index

**System:** WH40K (tabletop wargame -- NOT the 40K Roleplay line)  
**Total profiles:** 136  
**Soft / uncertain rows:** 23  

Extracted geometrically from the PDF text layer (PyMuPDF words mode). Only born-digital codexes are covered; the 45 scanned, image-only codexes are listed below as NO COVERAGE.

## Methodology

- Profiles reconstructed geometrically from the PDF text layer (PyMuPDF words mode): a header row of characteristic labels fixes each column's x-centre, and every value row maps its stat tokens to the nearest column. No number is ever guessed or corrected -- unreadable cells are left empty.
- 3rd-5th ed infantry schema: WS BS S T W I A Ld Sv (some tables prefix a Points column). Values keep any parenthetical modifiers verbatim, e.g. T4(5) on bikes, S6(10) / A2(3) on Dreadnoughts.
- Vehicles use Armour Values: tanks are BS + Front/Side/Rear; walkers are WS BS S (Front Side Rear) I A. The header token 'Armour' is merged into its Front/Side/Rear column, and a walker's abbreviated F/S/R triple is relabelled Front/Side/Rear so it never collides with S (Strength).
- Codex Imperialis 1993 (2nd ed) is a special case: its profile tables' characteristic labels are NOT in the PDF text layer (they are part of the table graphic) and the surrounding text is OCR-mangled. Its rows are therefore captured POSITIONALLY -- name + raw ordered values under c1..cN keys -- and EVERY such row is flagged 'soft'. The 2nd-ed M/WS/BS/.../Int/Cl/WP labels are intentionally NOT fabricated onto these values.
- Summary/reference tables duplicate per-datasheet profiles; exact (name, profile) duplicates are merged within each book (space/case insensitive), keeping the datasheet citation.

## Digital books harvested

| Book | Edition | Profiles |
| --- | --- | --- |
| Blood Angels - 2007 - 5th Edition | 5th | 41 |
| Codex Imperialis - 1993 - 2nd Edition | 2nd | 23 |
| Harlequins | unknown | 18 |
| Space Marines - 2008 - 5th Edition | 5th | 54 |

## NO COVERAGE (scanned, image-only)

- Armageddon - 2000
- Assassins - 1999
- Astronomicon
- Black Templars - 2005 (2)
- Black Templars - 2005
- Blood Angels - 1998
- Blood Angels - 2009
- Catachan - 2006
- Chaos Daemons - 2008
- Chaos Space Marines - 1999
- Chaos Space Marines - 2002
- Chaos Space Marines - 2007
- Cityfight - 2001
- Craftworld Eldar - 2000
- Daemonhunters - 2003 - 3rd Edition
- Dark Angels - 1999
- Dark Angels - 2006 - 4th Edition
- Dark Eldar - 1998
- Eldar - 1999
- Eldar - 2006 - 4th Edition
- Eye Of Terror - 2003 OCR
- Eye Of Terror - 2003
- Genestealer Cults
- Grey Knights & Deathwatch - 2001
- Grey Knights - 2010
- Imperial Guard - 1995
- Imperial Guard - 1999
- Imperial Guard - 2003
- Imperial Guard - 2008 - 5th Edition
- Necrons - 2002 - 3rd Edition
- Orks - 1991
- Orks - 1999
- Orks - 2007 - 4th Edition
- Sisters of Battle - 1997
- Space Marines - 1999
- Space Marines - 2004
- Space Wolves - 2000
- Space Wolves - 2009 - 5th Edition
- Tau Empire - 2001
- Tau Empire - 2005 - 4th Edition
- Tyranids - 2001
- Tyranids - 2004 - 4th Edition
- Tyranids - 2009 - 5th Edition
- Ultramarines - 1993 - 2nd Edition
- Witch Hunters - 2003 - 4th Edition

## Blood Angels - 2007 - 5th Edition

| Unit | Profile | Edition | Citation | Soft |
| --- | --- | --- | --- | --- |
| Lord Dante | WS6 BS5 S4 T4 W3 I5 A4 Ld10 Sv2+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 7] |  |
| Brother-Captain Tycho | WS5 BS5 S4 T4 W3 I5 A3 Ld10 Sv2+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 7] |  |
| Mephiston | WS6 BS5 S5 T5 W3 I6 A4 Ld10 Sv2+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 8] |  |
| Brother Corbulo | WS5 BS5 S4 T4 W3 I5 A3 Ld10 Sv3+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 9] |  |
| Chaplain Lemartes | WS5 BS5 S4 T4 W3 I5 A3 Ld10 Sv3+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 9] |  |
| Death Company | WS4 BS4 S4 T4 W1 I4 A2 Ld9 Sv3+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 10] |  |
| Honor Guard | WS4 BS4 S4 T4 W1 I4 A2 Ld9 Sv3+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 11] |  |
| Veteran | WS4 BS4 S4 T4 W1 I4 A2 Ld9 Sv3+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 11] |  |
| Furioso Dreadnought | WS4 BS4 S6(10) I4 A2(3) Front12 Side12 Rear10 | 5th | Blood Angels - 2007 - 5th Edition [PDF page 13] |  |
| Dante | WS6 BS5 S4 T4 W3 I5 A4 Ld10 Sv2+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 16] |  |
| Lemartes | WS5 BS5 S4 T4 W3 I5 A3 Ld10 Sv3+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 16] |  |
| Corbulo | WS5 BS5 S4 T4 W3 I5 A3 Ld10 Sv3+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 16] |  |
| Cpt. Tycho | WS5 BS5 S4 T4 W3 I5 A3 Ld10 Sv2+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 17] |  |
| Chaplain | WS5 BS5 S4 T4 W2 I5 A3 Ld9 Sv3+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 17] |  |
| Librarian | WS5 BS5 S4 T4 W2 I5 A3 Ld9 Sv3+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 17] |  |
| Captain | WS5 BS5 S4 T4 W3 I5 A3 Ld10 Sv3+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 18] |  |
| Company | WS4 BS4 S4 T4 W1 I4 A2 Ld9 Sv3+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 19] |  |
| Terminator | WS4 BS4 S4 T4 W1 I4 A2 Ld9 Sv2+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 19] |  |
| Furioso | WS4 BS4 S6 I4 A2(3) Front12 Side12 Rear10 | 5th | Blood Angels - 2007 - 5th Edition [PDF page 20] |  |
| Dreadnought | WS4 BS4 S6 I4 A2 Front12 Side12 Rear10 | 5th | Blood Angels - 2007 - 5th Edition [PDF page 20] |  |
| Techmarine | WS4 BS4 S4 T4 W2 I4 A2 Ld9 Sv2+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 20] |  |
| Servitor | WS4 BS4 S3 T3 W1 I3 A1 Ld9 Sv4+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 20] |  |
| Veteran Sgt | WS4 BS4 S4 T4 W1 I4 A2 Ld9 Sv4+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 21] |  |
| Scout | WS4 BS4 S4 T4 W1 I4 A1 Ld8 Sv4+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 21] |  |
| Veteran Sgt | WS4 BS4 S4 T4 W1 I4 A2 Ld9 Sv3+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 22] |  |
| Space Marine | WS4 BS4 S4 T4 W1 I4 A1 Ld8 Sv3+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 22] |  |
| Veteran Sgt | WS4 BS4 S4 T4(5) W1 I4 A2 Ld9 Sv3+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 23] |  |
| Biker | WS4 BS4 S4 T4(5) W1 I4 A1 Ld8 Sv3+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 23] |  |
| Attack Bike | WS4 BS4 S4 T4(5) W2 I4 A2 Ld8 Sv3+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 23] |  |
| Company Captain | WS5 BS5 S4 T4 W3 I5 A3 Ld10 Sv3+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 27] |  |
| Servitor | WS4 BS4 S3 T3 W1 I3 A1 Ld8 Sv4+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 27] |  |
| Tycho | WS5 BS5 S4 T4 W3 I5 A3 Ld10 Sv3+ | 5th | Blood Angels - 2007 - 5th Edition [PDF page 27] |  |
| Drop Pod | BS2 Front12 Side12 Rear12 | 5th | Blood Angels - 2007 - 5th Edition [PDF page 27] |  |
| Land Raider | BS4 Front14 Side14 Rear14 | 5th | Blood Angels - 2007 - 5th Edition [PDF page 27] |  |
| Land Raider Crusader | BS4 Front14 Side14 Rear14 | 5th | Blood Angels - 2007 - 5th Edition [PDF page 27] |  |
| Land Speeder | BS4 Front10 Side10 Rear10 | 5th | Blood Angels - 2007 - 5th Edition [PDF page 27] |  |
| Predator/Baal Predator | BS4 Front13 Side11 Rear10 | 5th | Blood Angels - 2007 - 5th Edition [PDF page 27] |  |
| Razorback | BS4 Front11 Side11 Rear10 | 5th | Blood Angels - 2007 - 5th Edition [PDF page 27] |  |
| Rhino | BS4 Front11 Side11 Rear10 | 5th | Blood Angels - 2007 - 5th Edition [PDF page 27] |  |
| Vindicator | BS4 Front13 Side11 Rear10 | 5th | Blood Angels - 2007 - 5th Edition [PDF page 27] |  |
| Whirlwind | BS4 Front11 Side11 Rear10 | 5th | Blood Angels - 2007 - 5th Edition [PDF page 27] |  |

## Codex Imperialis - 1993 - 2nd Edition

| Unit | Profile | Edition | Citation | Soft |
| --- | --- | --- | --- | --- |
| Champion | c14 c24 c35 c43 c54 c61 c75 c81 c99 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 42] | yes |
| Hero | c14 c25 c36 c44 c55 c62 c76 c82 c99 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 42] | yes |
| MightyHero | c14 c26 c37 c44 c55 c63 c77 c83 c910 c100 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 42] | yes |
| Hero | c14 c25 c35 c44 c54 c62 c75 c82 c98 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 46] | yes |
| MlghtyHero | c14 c26 c36 c44 c54 c63 c76 c83 c99 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 46] | yes |
| Electro Priests | c14 c24 c33 c48 c53 c61 c73 c81 c99 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 47] | yes |
| Servitor | c14 c23 c31 c44 c53 c64 c71 c81 c94 c101 c111 c127 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 47] | yes |
| Ork | c11 c24 c31 c43 c51 c63 c73 c81 c94 c101 c112 c121 c137 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 56] | yes |
| N0b | c14 c24 c34 c43 c54 c61 c73 c81 c98 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 56] | yes |
| Bigboss | c14 c25 c35 c44 c55 c62 c74 c82 c98 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 56] | yes |
| Warboss | c14 c26 c36 c44 c55 c63 c75 c83 c99 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 56] | yes |
| Runtherd | c14 c24 c31 c41 c54 c64 c74 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 57] | yes |
| Madboy | c14 c23 c33 c43 c54 c61 c72 c81 c97 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 61] | yes |
| Dire Avenger | c15 c24 c34 c43 c53 c61 c76 c81 c91 c109 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 67] | yes |
| SwoopingHwk | c15 c24 c34 c43 c53 c61 c76 c81 c99 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 67] | yes |
| Dark Reaper | c14 c24 c34 c43 c53 c61 c74 c81 c99 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 67] | yes |
| Farseers | c15 c27 c37 c44 c55 c64 c79 c83 c91 c100 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 69] | yes |
| Harlequ~n | c16 c25 c35 c43 c53 c61 c77 c81 c91 c100 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 72] | yes |
| Lord | c13 c28 c36 c45 c56 c64 c75 c84 c91 c100 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 77] | yes |
| Beastman | c14 c21 c34 c43 c51 c63 c77 c84 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 91] | yes |
| Hound | c16 c24 c30 c44 c54 c61 c74 c82 c96 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 91] | yes |
| Hybrid | c14 c24 c32 c44 c53 c61 c75 c81 c98 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 94] | yes |
| Termagant | c16 c24 c33 c43 c53 c61 c74 c81 c95 | 2nd | Codex Imperialis - 1993 - 2nd Edition [PDF page 96] | yes |

## Harlequins

| Unit | Profile | Edition | Citation | Soft |
| --- | --- | --- | --- | --- |
| Great Harlequin | Points60 WS7 BS5 S3 T3 W3 I8 A4 Ld10 Sv- | unknown | Harlequins [PDF page 4] |  |
| Shadowseer | Points70 WS6 BS5 S3 T3 W2 I7 A3 Ld10 Sv- | unknown | Harlequins [PDF page 4] |  |
| Solitaire | Points90 WS8 BS5 S3 T3 W3 I8 A4 Ld- Sv- | unknown | Harlequins [PDF page 5] |  |
| Death Jester | Points47 WS6 BS4 S3 T3 W1 I4 A2 Ld9 Sv- | unknown | Harlequins [PDF page 5] |  |
| Harlequin | Points25 WS5 BS3 S3 T3 W1 I6 A2 Ld9 Sv- | unknown | Harlequins [PDF page 6] |  |
| Troupe leader | Points+12 WS6 BS4 S3 T3 W1 I6 A2 Ld9 Sv- | unknown | Harlequins [PDF page 6] |  |
| Harlequin Jetbike | Points45 WS5 BS3 S3 T3(4) W1 I6 A2 Ld9 Sv-/3+ | unknown | Harlequins [PDF page 6] |  |
| Troupe leader | Points+15 WS6 BS4 S3 T3(4) W1 I6 A2 Ld9 Sv-/3+ | unknown | Harlequins [PDF page 6] |  |
| Venom | Points45 Front10 Side10 Rear10 BS3 | unknown | Harlequins [PDF page 7] |  |
| Gt Harlequin | WS7 BS5 S3 T3 W3 I8 A4 Ld10 Sv- | unknown | Harlequins [PDF page 9] |  |
| Shadowseer | WS6 BS5 S3 T3 W2 I7 A3 Ld10 Sv- | unknown | Harlequins [PDF page 9] |  |
| Solitaire | WS8 BS5 S4 T3 W3 I8 A4 Ld- Sv- | unknown | Harlequins [PDF page 9] |  |
| Death Jester | WS6 BS4 S3 T3 W1 I4 A2 Ld9 Sv- | unknown | Harlequins [PDF page 9] |  |
| Harlequin | WS5 BS3 S3 T3 W1 I6 A2 Ld9 Sv- | unknown | Harlequins [PDF page 9] |  |
| Troupe Ld | WS6 BS4 S3 T3 W1 I6 A2 Ld10 Sv- | unknown | Harlequins [PDF page 9] |  |
| Harl. Jetbike | WS5 BS3 S3 T4 W1 I6 A2 Ld10 Sv-/3+ | unknown | Harlequins [PDF page 9] |  |
| Harl. Jetbike Ld | WS6 BS4 S3 T4 W1 I6 A2 Ld10 Sv-/3+ | unknown | Harlequins [PDF page 9] |  |
| Venom | Front10 Side10 Rear10 BS3 | unknown | Harlequins [PDF page 9] |  |

## Space Marines - 2008 - 5th Edition

| Unit | Profile | Edition | Citation | Soft |
| --- | --- | --- | --- | --- |
| Chapter Master | WS6 BS5 S4 T4 W3 I5 A3 Ld10 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 54] |  |
| Chapter Champion | WS5 BS4 S4 T4 W1 I4 A3 Ld10 Sv2+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 55] |  |
| Honour Guard | WS4 BS4 S4 T4 W1 I4 A2 Ld10 Sv2+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 55] |  |
| Captain | WS6 BS5 S4 T4 W3 I5 A3 Ld10 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 56] |  |
| Company Champion | WS5 BS4 S4 T4 W1 I4 A2 Ld9 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 57] |  |
| Veteran | WS4 BS4 S4 T4 W1 I4 A2 Ld9 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 57] |  |
| Apothecary | WS4 BS4 S4 T4 W1 I4 A2 Ld9 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 57] |  |
| Librarian | WS5 BS4 S4 T4 W2 I4 A2 Ld10 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 58] |  |
| Chaplain | WS5 BS4 S4 T4 W2 I4 A2 Ld10 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 60] |  |
| Space Marine Sergeant | WS4 BS4 S4 T4 W1 I4 A2 Ld9 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 61] |  |
| Space Marine | WS4 BS4 S4 T4 W1 I4 A1 Ld8 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 61] |  |
| Terminator Sergeant | WS4 BS4 S4 T4 W1 I4 A2 Ld9 Sv2+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 66] |  |
| Terminator | WS4 BS4 S4 T4 W1 I4 A2 Ld9 Sv2+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 66] |  |
| Venerable Dreadnought | WS5 BS5 S6 Front12 Side12 Rear10 I4 A2 | 5th | Space Marines - 2008 - 5th Edition [PDF page 67] |  |
| Dreadnought | WS4 BS4 S6 Front12 Side12 Rear10 I4 A2 | 5th | Space Marines - 2008 - 5th Edition [PDF page 67] |  |
| Ironclad Dreadnought | WS4 BS4 S6 Front13 Side13 Rear10 I4 A2(3) | 5th | Space Marines - 2008 - 5th Edition [PDF page 67] |  |
| Scout Sergeant | WS4 BS4 S4 T4 W1 I4 A2 Ld9 Sv4+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 68] |  |
| Scout | WS3 BS3 S4 T4 W1 I4 A1 Ld8 Sv4+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 68] |  |
| Scout Biker Sergeant | WS4 BS4 S4 T4(5) W1 I4 A2 Ld9 Sv4+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 69] |  |
| Scout Biker | WS3 BS3 S4 T4(5) W1 I4 A1 Ld8 Sv4+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 69] |  |
| Biker Sergeant | WS4 BS4 S4 T4(5) W1 I4 A2 Ld9 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 70] |  |
| Space Marine Biker | WS4 BS4 S4 T4(5) W1 I4 A1 Ld8 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 70] |  |
| Attack Bike | WS4 BS4 S4 T4(5) W2 I4 A2 Ld8 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 70] |  |
| Master of the Forge | WS4 BS5 S4 T4 W2 I4 A2 Ld10 Sv2+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 72] |  |
| Techmarine | WS4 BS4 S4 T4 W1 I4 A1 Ld8 Sv2+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 73] |  |
| Servitor | WS3 BS3 S3 T3 W1 I3 A1 Ld8 Sv4+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 74] |  |
| Marneus Calqar | WS6 BS5 S4 T4 W4 I5 A4 Ld10 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 86] |  |
| Cato Sicarius | WS6 BS5 S4 T4 W3 I5 A3 Ld10 Sv2+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 87] |  |
| Varro Tigurius | WS5 BS4 S4 T4 W2 I4 A2 Ld10 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 88] |  |
| Ortan Cassius | WS5 BS4 S4 T6 W2 I4 A2 Ld10 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 89] |  |
| Sergeant Telion | WS5 BS6 S4 T4 W1 I4 A2 Ld9 Sv4+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 90] |  |
| Antaro Chronus | WS4 BS5 S4 T4 W1 I4 A2 Ld9 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 91] |  |
| Pedro Kantor | WS6 BS5 S4 T4 W3 I5 A3 Ld10 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 92] |  |
| Darnath Lysander | WS6 BS5 S4 T4 W4 I5 A3 Ld10 Sv2+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 93] |  |
| Kayvaan Shrike | WS6 BS5 S4 T4 W3 I5 A3 Ld10 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 94] |  |
| Vulkan He'stan | WS6 BS5 S4 T4 W3 I5 A3 Ld10 Sv2+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 95] |  |
| Kor'sarro Khan | WS6 BS5 S4 T4 W3 I5 A3 Ld10 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 96] |  |
| Damned Sergeant | WS5 BS4 S4 T4 W1 I4 A2 Ld10 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 97] |  |
| Damned Legionnaire | WS4 BS4 S4 T4 W1 I4 A2 Ld10 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 97] |  |
| Marneus Calgar | WS6 BS5 S4 T4 W4 I5 A4 Ld10 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 131] |  |
| Chronus | WS4 BS5 S4 T4 W1 I4 A2 Ld9 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 146] |  |
| Space Marine Sgt | WS4 BS4 S4 T4 W1 I4 A2 Ld9 Sv3+ | 5th | Space Marines - 2008 - 5th Edition [PDF page 146] |  |
| Drop Pod | BS4 Front12 Side12 Rear12 | 5th | Space Marines - 2008 - 5th Edition [PDF page 146] |  |
| Land Raider | BS4 Front14 Side14 Rear14 | 5th | Space Marines - 2008 - 5th Edition [PDF page 146] |  |
| Land Raider Crusader | BS4 Front14 Side14 Rear14 | 5th | Space Marines - 2008 - 5th Edition [PDF page 146] |  |
| Land Raider Redeemer | BS4 Front14 Side14 Rear14 | 5th | Space Marines - 2008 - 5th Edition [PDF page 146] |  |
| Land Speeder | BS4 Front10 Side10 Rear10 | 5th | Space Marines - 2008 - 5th Edition [PDF page 146] |  |
| Land Speeder Storm | BS3 Front10 Side10 Rear10 | 5th | Space Marines - 2008 - 5th Edition [PDF page 146] |  |
| Predator | BS4 Front13 Side11 Rear10 | 5th | Space Marines - 2008 - 5th Edition [PDF page 146] |  |
| Razorback | BS4 Front11 Side11 Rear10 | 5th | Space Marines - 2008 - 5th Edition [PDF page 146] |  |
| Rhino | BS4 Front11 Side11 Rear10 | 5th | Space Marines - 2008 - 5th Edition [PDF page 146] |  |
| Vindicator | BS4 Front13 Side11 Rear10 | 5th | Space Marines - 2008 - 5th Edition [PDF page 146] |  |
| Whirlwind | BS4 Front11 Side11 Rear10 | 5th | Space Marines - 2008 - 5th Edition [PDF page 146] |  |
| Ironclad | WS4 BS4 S6 Front13 Side13 Rear10 I4 A2(3) | 5th | Space Marines - 2008 - 5th Edition [PDF page 146] |  |
