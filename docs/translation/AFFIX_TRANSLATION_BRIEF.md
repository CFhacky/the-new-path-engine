# Weapon-affix translation brief (read fully before converting anything)

**Read `docs/translation/FUSED_ENGINE_RESOLUTION.md` first. It supersedes this brief wherever they differ:** GURPS dice read as-is; riders ignore worn DR; negative levels use the Energy Drained condition; alignment stays on the 3.5e side; colliding names stay and never merge; GURPS point totals are not required on affix entries.

Job: convert each assigned weapon affix into a campaign Affix Registry entry in **both** D&D 3.5e and GURPS 4e, using the ratified Crusader entry as the format and rate card.
Reference entry: `docs/translation/crusader_weapon_affix_DRAFT.md` (Notion Affix Registry section 2 is canon; this repo file mirrors it).

## Hard rules
1. **Source first.** Fetch the full SRD text for your ability from the 3.5 SRD (d20srd.org, "Magic Weapons" special abilities) with WebFetch before writing a number. Never write a mechanic from memory. If a value cannot be sourced, say "unverified; built from design intent". Do not invent tiers the source lacks: a DMG ability has one printed bonus-equivalent, so write one rung, not three.
2. **Dedupe against existing pool rows first.** The Registry's canonical affix pools already carry both-system rows. Read the Part 1 pool tables in `/root/.claude/skills/synced/07327e22-ff68-47f1-ad4a-8176d4a886f0_c7d5c9b9-16d6-4e70-9b16-504f3872f1f8/loot-engine/references/affix-families.md` (Offensive, Defensive, Resource, Utility, Skill/Class, Elemental, Condition/Control pools) and Part 0 (Fatal Wound). Classify each ability: **COVERED** (an existing row already does it; name the row, state any gap in one line, emit no new family), **PARTIAL** (an existing row covers most; emit only the delta), or **NEW** (emit a full entry).
3. **Both systems, always. No 5e rules** (no advantage/disadvantage, proficiency bonus, bonus action, short rest).
4. **Never write to Notion.** Output goes to `docs/translation/affixes/<slug>.md` only. Registry ratification is the owner's call.
5. Do not touch any file except your own output files.

## Proc and stacking conventions (from loot-engine proc-conventions)
- One d100 per **damaging hit** (hit must deal damage past DR to roll), one d100 serves both systems, low threshold fires (10% = 01-10). Procs never proc other procs.
- Flat-source by default: wielder Str, enhancement, crits, sneak attack, GURPS ST never scale the proc. Scaling must be stated explicitly.
- Stacking is additive per stack, never multiplicative. Cap behavior is a state change, not a bigger number.
- Bleed/biological DoTs: bloodless targets (constructs, undead, oozes, elementals) immune. Energy procs respect resistances per tick.
- Pricing: bonus-equivalent priced bonus-squared x 2,000 gp (+1 = 2,000; +2 = 8,000; +3 = 18,000; +4 = 32,000; +5 = 50,000). Flat plus-gp abilities keep their printed gp.
- Fatal Wound interaction: any magical healing normally ends Fatal Wound stacks below cap. State in one line if your affix interacts with healing.

## GURPS constants
- Gadget on the weapon: Breakable (DR 6) -25%, Can Be Stolen (grab first) -10%.
- Follow-Up +0% (rides a DR-penetrating hit); Cyclic +400% per cycle; Armor Divisor (2) +50%, (5) +150%; Magical -10% on magic-sourced attacks; Costs Fatigue -5% per FP.
- 3.5e Str/Dex 2 points = GURPS 1 point; ST 10 pts/level.
- Proc-to-limitation match (activation roll, retrieved from the Basic Set B116 via search, not read from the book): proc 10% = 3d6 <=5 = Unreliable -80%; 25% = <=8 = -40%; 50% = <=11 = -20%; 90% = <=14 = -10%.
- Total limitations cap at -80% (a trait costs at least 20% of base). Point totals are transparency, never price.
- Innate Attack damage types: fire/cold = Burning (cold modifier), acid = Corrosion, poison = Toxic, lightning = Burning, sonic = Crushing [Sonic], holy/positive = Burning [Holy], necrotic = Toxic [Cosmic].
- Where you cannot verify a GURPS number, state the mechanism and mark the number open; do not guess.

## Output format (one file per ability)
```
# <ABILITY> — <COVERED | PARTIAL | NEW>
Source: <SRD URL fetched> · printed bonus-equivalent / price: <...>
Source text (key facts, quoted briefly): <...>
Existing pool coverage: <row name(s) and pool, or "none">; gap: <one line>
Verdict: <one line>
(if NEW or PARTIAL:)
Translation identity: flat/scaling · armor interaction · cap behavior
3.5e: <exact numbers, action, duration, save with fixed DC if any, SR, stacking, immunities>
GURPS: <chassis, modifiers with percentages, resulting points where computable, open numbers flagged>
Pricing: <bonus-equivalent and gp>
Name collision: <existing Registry/pool/SRD names that overlap>
Forks needing a ruling: <numbered, each with a recommended default; "none" if none>
```
Keep each file under ~60 lines. End your final report with a table: ability | verdict | existing row | forks needing rulings.
