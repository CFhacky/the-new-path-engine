# THE CRUSADER FAMILY — weapon suffix (rate-limited proc: self-heal + Holy Strength)

> **NON-AUTHORITATIVE DRAFT.** Prepared for the Notion Affix Registry
> (`396e8214-84b0-8129-aded-cf6eb787cbbe`), which is canon. Nothing here is ratified.
> On ratification the entry is appended to the Registry with a Canon Change Log pairing,
> and this file is deleted or reduced to the source packet. Five open rulings (D1–D5) are listed at the end.

**Status:** DRAFT · **Source concept:** WoW weapon enchant "Enchant Weapon - Crusader" (Classic spell 20034) · **Category:** Item (affix family), system-translator → loot-engine Registry loop
**Registry diff run:** 2026-10-03. Registry last edited 2026-08-12. Only the Fatal Wound family is ratified after the 2026-07-07 snapshot. No Crusader entry exists in the Registry, the system-translator catalog, or `reference/` (the repo only has the unrelated Tome of Battle Crusader class/maneuvers and Land Raider Crusader).

---

## 0. SOURCE RECORD (sourced vs. adjudicated are kept separate)

**Sourced** (warcraft.wiki.gg *Crusader (enchant)* and *Enchant Weapon - Crusader*, fetched in full; Classic DB / Wowpedia search results; Engadget *Lichborne*):

| Fact | Value |
|---|---|
| Original (Classic) tooltip | Often heals for **75–125** and increases Strength by **100** for **15 sec** when attacking in melee |
| Proc rate | **~1 proc per minute**; chance = weapon speed × 1.667% (time-based, not swing-based) |
| Buff | "Holy Strength" (spell 20007) |
| Dual-wield | Enchant on both weapons: Holy Strength can proc twice and the effects stack |
| Recipe | Formula taught at Enchanting 300 |
| Patch 2.0.1 (2006-12-05) | Reduced effect for players above level 60 |
| Current tooltip (wiki) | Heal **240**, Strength **+40** for 15 sec; reduced effect above level 30 |
| Patch 6.0.2 (2014-10-14) | Cannot be applied to weapons above item level 600 |
| Homage | Rune of the Fallen Crusader (Wrath 3.0.2, 2008-10-14): percent-scaled sibling, 6% heal / +15% Strength / 15 sec |

**Source limit, used as a design lever:** the source itself *removes* flat values at higher levels and bars the enchant from high-end weapons. The enchant is a low-ceiling, flat effect by design. That supports a flat-source family with a hard cap and no wielder scaling.

**Gaps that survived search (flagged, not guessed):**
- The wiki gives the current 240/+40 values and the level-60 and level-30 reduction notes, but not the exact scaling formula. Treat the numbers as "source-given at the stated levels," not as a derivable curve.
- Reagents conflict between pages (2 vs 4 Large Brilliant Shard). Irrelevant to mechanics, since campaign pricing is SRD gp. Not carried.
- Whether re-proc on the *same* weapon refreshes or ignores the buff is not stated in the sources retrieved. The refresh rule below is **design, not sourced**.
- GURPS *Unreliable* limitation percentages could not be retrieved this session (not in `reference/`, web search returned nothing). The GURPS total below stops before that limitation.

---

## 1. TRANSLATION IDENTITY

- **Flat-source.** The enchantment owns both numbers. Wielder Str, enhancement bonus, Power Attack, class features and GURPS ST never scale the heal or the Holy Strength bonus.
- **Rate-limited, not swing-limited.** The source proc is 1 per minute regardless of swing count. In 3.5e that is **10% per round** (1 proc per 10 six-second rounds). The proc rolls at most once per weapon per round, on the first hit that deals damage past DR. This is a deliberate deviation from proc-conventions §1 (one d100 per hit); see D1.
- **Payload scales, proc rate does not.** All three tiers proc at 10%. Tier changes only the heal and the Strength bonus. The source has a single proc rate; inventing a rising rate would be unsourced.
- **Stacking.** Holy Strength stacks across *different* Crusader weapons (sourced) and is additive, never multiplicative. A second proc from the *same* weapon refreshes the duration and does not stack (design; see §0 gap). Hard cap: one instance per wielded Crusader weapon, so at most two with two hands.
- **Damage-through required.** No damage past DR, no proc roll (proc-conventions §1 default).

## 2. TIER TABLE

| Tier | Affix (suffix) *(placeholder names)* | Proc | Heal | Holy Strength | Duration | Bonus-equiv |
|---|---|---|---|---|---|---|
| Magic | of the Pilgrim's Vigor | 10%/round | 5 | +2 Str | 3 rounds | +1 |
| Rare | of the Crusader | 10%/round | 8 | +4 Str | 3 rounds | +2 |
| Unique | of the Crusader's Oath | 10%/round | 12 | +6 Str | 3 rounds | +3 |

**Where the numbers come from (nothing invented):**
- **Heal 5 / 8 / 12** are the ratified Life Shield tier values at T5 / T4 / T3 (5 / 8 / 12 temp HP). The source heal is a few percent of a Classic character's HP (avg 100), which lands in the same band. Heal is flat, with no dice, per the flat-source rule. The source's ±25% variance is dropped.
- **+2 / +4 / +6 Str** are the SRD stat-bonus steps already baked into the exchange rates (4k / 16k / 36k gp for a permanent bonus).
- **Duration:** the source's 15 sec is 2.5 rounds. It rounds **up to 3 rounds** in 3.5e (see D4) and stays an exact 15 seconds in GURPS.
- **Not rolled.** No generative parameter is left open: every value derives from a source figure or a ratified anchor. `loot_roll.py` was not used, and no roll log is attached.

## 3. D&D 3.5e

**Trigger.** Once per round per Crusader weapon, on the first melee hit that deals damage past DR, roll the proc d100 in the fused-engine Phase 0 header. On 01–10 it fires.

```
PROC [item name — Crusader]: d100=NN vs 10% → FIRES / no effect. Heal: X. Holy Strength: +Y, 3 rounds.
```

**Effect (on fire):**
1. **Heal.** The wielder is healed the tier amount. It is magical healing (positive energy). Undead wielders are damaged instead, per standard positive-energy rules. It restores HP only and does **not** clear Fatal Wound stacks (D2).
2. **Holy Strength.** An **untyped** Strength bonus equal to the tier value for 3 rounds. It applies to melee attack and damage, Strength checks and skills, and carrying capacity. Untyped so that two Crusader weapons stack, as the source states. Same-weapon re-proc refreshes the duration.

**Limits.**
- Maximum concurrent instances: one per wielded Crusader weapon (two total).
- Fixed values. No save, no SR, no DC, since this is a self-effect.
- Melee weapons only. It does not ride ranged weapons, because the source says "when attacking in melee" (a melee-proc family never rides a ranged weapon, per the loot-engine substitution rule).
- Procs never proc other procs.

**Pricing.** Bonus-equivalent +1 / +2 / +3 by tier, priced bonus-squared: **2,000 / 8,000 / 18,000 gp** as an affix on a masterwork weapon. Cross-check by uptime: the buff is active about 3 / (3 + 10) ≈ 23% of the time, so the SRD stat-bonus price × 0.23 gives roughly **920 / 3,680 / 8,280 gp**. The engine convention comes out about 2× the uptime figure, which covers the heal and the dual-wield stack (D5).

**Caster level:** 5th / 8th / 11th (Magic / Rare / Unique). Aura: moderate (strong at Unique) transmutation/conjuration. *Placeholder; set when the entry is ratified.*

## 4. GURPS 4e

One d100 serves both systems: the same 10% proc, rolled once per 6-second interval on the first damaging hit that penetrates DR.

**Chassis:** Gadget on the weapon.
- **Holy Strength:** ST **+1 / +2 / +3** (the 3.5e +2 / +4 / +6 at the exchange-rate 2:1). Duration **15 seconds, exact**. Refreshes on same-weapon re-proc. Stacks across two Crusader weapons.
- **Heal:** Regeneration (limited: one burst per proc, restores 5 / 8 / 12 HP at once). Same mapping precedent as the ratified Life Shield and Lifedrinker rows.
- **Does not clear Fatal Wound stacks** (D2). Counts as magical healing for the at-cap lock.

**Limitations and point transparency** (ST costs 10/level; point totals are never price):

| Tier | ST before limitations | Breakable (DR 6) −25% + Can Be Stolen (grab first) −10% = −35% | + proc limitation |
|---|---|---|---|
| Magic | 10 | **6.5** | Unreliable/Accessibility for the 10%-per-6-s proc, **percentage not retrieved** |
| Rare | 20 | **13** | same |
| Unique | 30 | **19.5** | same |

Regeneration cost is "Variable" in the repo index (`gurps_trait_index`), so it is not totalled. The total is **incomplete until the proc limitation and the heal cost are set from the book**, so no final point figure is stated.

## 5. COLLISION AND INTERACTION NOTES

- **Name collisions.** (a) Tome of Battle *Crusader* class and *Crusader's Strike*; the affix is a weapon suffix and never touches the class. (b) In-campaign "Crusader" adversaries: a Notion search hit on the Bloodaxe Legion page mentions a 5th Cohort casualty to "Crusader radiant…". That page was **not read** in this pass. (c) The ratified pool affixes *Leech* (HP on hit, flat) and *Radiant* (positive-energy damage) overlap in flavor only. Crusader is a proc heal plus a stat buff and shares no mechanic with either. Names above are placeholders, to be earned from backstory per the naming rule.
- **Fatal Wound.** The Fatal Wound registry rule says *any magical healing* clears stacks below cap and is the only thing that works at cap. A 10%/round self-heal would therefore end a full bleed stack. D2 asks for the override this draft proposes.

**Chekhov note (proposal; touches canon, so not asserted).** The moment this family exists in the lexicon it exists for whoever fields holy orders and for Aldric Steelgaze's smiths. A self-heal-plus-strength weapon in the hands of a crusading order is the natural counter-pressure to the Fatal Wound bleed line. Deliberate: it arms both sides. Which faction fields it first should be read from the Bloodaxe Legion / Crusader page before this is ratified.

---

## OPEN RULINGS (needed before ratification)

- **D1 — Once per round, not per hit.** Preserves the source's 1 ppm. Cost: deviates from proc-conventions §1 (one d100 per hit); a four-attack fighter would otherwise proc about 3.4× as often as the source intends. *Recommended: once per weapon per round.*
- **D2 — Heal vs. Fatal Wound.** Restore HP only and do not clear stacks (recommended), or let it clear below cap like any magical healing?
- **D3 — Holy Strength is untyped.** Required for the two-weapon stack the source states, but it stacks with every other Strength source. The two-weapon cap and 3-round duration are the brakes.
- **D4 — Duration.** 2.5 rounds rounds up to 3. Alternative: 2 rounds (cheaper), with the GURPS 15 s unchanged.
- **D5 — Price.** Engine convention +1 / +2 / +3 (conservative, about 2× the uptime math), or reprice to the uptime figures.

*Sources:*
[Enchant Weapon - Crusader](https://warcraft.wiki.gg/wiki/Enchant_Weapon_-_Crusader) ·
[Crusader (enchant)](https://warcraft.wiki.gg/wiki/Crusader_(enchant)) ·
[Rune of the Fallen Crusader](https://wowpedia.fandom.com/wiki/Rune_of_the_Fallen_Crusader) ·
[Lichborne: PvE Enchantments for Death Knights](https://www.engadget.com/2009-02-08-lichborne-pve-enchantments-for-death-knights.html) ·
Classic spell 20034 (wowclassicdb)
