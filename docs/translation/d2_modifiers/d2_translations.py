"""Translations for the Diablo II weapon-modifier corpus. Rate card = Crusader (Affix Registry section 2); rules = ../FUSED_ENGINE_RESOLUTION.md.

CONVENTIONS: D2 chance-based mods use one d100 per damaging hit, 01-10 fires (Registry proc convention) unless stated; GURPS keeps the source's
exact seconds; D2's level-difference chance formulas are replaced by a fixed 3.5e save (Fortitude or Will, DC 13-14, the Condition-pool Magic rung);
'normal and minion monsters only' immunities (bosses, uniques) are read as: no effect on creatures of 17+ Hit Dice (Tier 1) or on named bosses;
price = bonus-equivalent squared x 2,000 gp; healing is ordinary magical healing and ends Fatal Wound stacks; GURPS chassis Gadget, no point total.
"""
T = {}
def c(base, note): return dict(verdict="COVERED", base=base, note=note)
def e(verdict, base, bonus, three_e, gurps, collision="none.", forks="none."):
    return dict(verdict=verdict, base=base, bonus=bonus, three_e=three_e, gurps=gurps, collision=collision, forks=forks, note="")

# ---- COVERED by an existing Registry row ----
T["Deadly Strike"] = c("Keen Edge (Offensive 13-18) / Lethal Focus (Offensive 31-36)", "A chance to double physical damage is a critical hit; 3.5e already has threat range and crit multiplier, which Keen Edge widens and Lethal Focus adds to. No new family.")
T["Knockback"] = c("Knockback (Condition 49-54)", "Same effect (push on hit; the source's size-dependent chance maps to the row's 'creatures of your own size or smaller').")
T["Life Stolen"] = c("Leech (Resource 19-24) / Vampiric (MIC, this repo)", "Heal as a share of damage dealt: Leech heals a flat 1/1/2/3/5 per hit; the percentage form is read as one HP per 5 damage rounded down, minimum 1 at the Magic rung. Undead (0% drain) give nothing, as bloodless targets do under Leech.")
T["Mana Stolen"] = c("Mana Leech (Resource 25-30)", "Mana returned on a hit; Mana Leech's flat 1/2/3/5/8 per hit covers it.")
T["Monster Defense per Hit"] = c("Overpower (Offensive 49-54)", "Overpower reduces target AC and DR by 1/1/2/3/4 for a round on a hit; the source's Defense loss (-50 to -100) is the same effect at a different scale.")
T["Slows Target"] = c("Slowing (Condition 01-08) / Icy Chill (WoW corpus)", "Slow on hit (the source's 30 s cap 90%/50% reduced to the row's slow-for-1-round); covered.")
T["Target Defense Reduction"] = c("Overpower (Offensive 49-54) / Armor Piercing (Offensive 19-24)", "Attacks resolve against lowered Defense; Overpower lowers AC on a hit, Armor Piercing ignores DR. Covered together.")
T["Fire Damage"] = c("Flaming (Elemental 01-08)", "Fire damage ladders (Flame to Incineration, Fiery to Condensing) are the same shape as Flaming's +1d4/+1d6/+1d8/+2d6/+3d6 rider; the large late-ladder numbers are D2's scale, not rescaled.")
T["Cold Damage"] = c("Freezing (Elemental 09-16)", "Cold damage with a chill duration: Freezing's rider plus its slow on crit at T3+. The source's chill length (1-4 s) is the row's one-round slow.")
T["Lightning Damage"] = c("Shocking (Elemental 17-24)", "Same rider; D2's wide min-max spread is a game feature the row's fixed dice already flatten.")
T["Poison Damage"] = c("Venomous (Elemental 33-38)", "Poison over time (Blight to Anthrax, Septic to Pestilent): Venomous gives the poison rider and Cyclic GURPS tick.")
T["Enhanced Damage"] = c("Wounding (Offensive 07-12)", "A percentage damage increase is read as Wounding's flat bonus damage +1/+1d4/+1d6/+2d6/+3d6; the percentage form has no 3.5e meaning.")
T["Attack Rating"] = c("Striking (Offensive 01-06)", "Attack Rating is the 3.5e attack bonus: Striking +1/+1/+2/+3/+4.")
T["Minimum and Maximum Damage"] = c("Wounding (Offensive 07-12)", "Flat damage added to the weapon die is Wounding's flat bonus; D2's separate min and max have no 3.5e analogue.")
T["Damage vs Demons"] = c("Banefire (Elemental 93-96) / Demonslaying (WoW corpus)", "Extra damage against a creature type: Banefire's +2d6 to +5d6 against a chosen subtype, here the demon subtype.")
T["Damage vs Undead"] = c("DMG Bane (undead as the designated foe) / Radiant (Elemental 45-50)", "Extra damage against undead: Bane (undead foe) or Radiant (positive energy, undead take x1.5).")
T["Attack Speed"] = c("Rapid Assault (Offensive 25-30)", "Percentage attack rate: Readiness and Alacrity read as the row's T5 to T4 (1/day extra attack), Swiftness and Quickness as T3 to T2 (3/day).")
T["Damage Reduced"] = c("Stoneskin (Defensive 73-78)", "Damage Reduced by 1/2/3 (flat per hit) is Stoneskin's 1/2/3/4/5 flat reduction after DR.")

# ---- DELTA / NEW: full entries ----
T["Crushing Blow"] = e("NEW", "none", 2,
 "Proc: one d100 on each damaging melee hit, 01-10 fires. On fire the target takes extra damage equal to one quarter of its current hit points, maximum 25, before normal damage. Not multiplied on a critical hit; ignores DR/X; reduced by percentage-type resistances; creatures immune to physical damage take none. Creatures of 17+ Hit Dice take one eighth of current hit points instead (maximum 25).",
 "Crushing Attack (Follow-Up) on the same d100: injury equal to 1/4 of the target's current HP, maximum 25 HP, applied after DR; against Tier 1 targets 1/8.",
 collision="Pool 'Lethal Focus' (crit bonus) and DMG Mighty Cleaving: different mechanics.",
 forks="1. The source gives no cap and halves the fraction for some enemies only by difficulty; the 25 cap and the Tier 1 eighth are design values. 2. Chance per item varies in the source (the search shows Bloodtree Stump at 50%); the ratified 10% proc is used.")
T["Fires Explosive Arrows or Bolts"] = e("DELTA", "Elemental Burst (Elemental 75-80)", 1,
 "Ranged weapons only. Each damaging hit also bursts in a 5-ft radius around the target for 1d6 fire damage, Reflex DC 13 half (the Magic-rung value; the source gives no Exploding Arrow damage). No d100; every hit. Does not apply when the wielder uses a skill-based shot.",
 "Innate Attack (Burning, Explosion 1) 1d on every damaging hit, centered on the target.",
 forks="1. Exploding Arrow damage and the item source levels (3 to 15) are not in the source; the Elemental Burst Magic-rung scale is used. 2. Elemental Burst triggers on a crit; this entry triggers on every hit (that is the delta).")
T["Fires Magic Arrows"] = e("NEW", "none", 1,
 "Ranged weapons only. Every damaging hit counts as magic and deals +1d4 force damage (the Magic-rung value; the source gives no Magic Arrow damage). Force damage ignores DR/X and incorporeal miss chances. No d100.",
 "Innate Attack (Crushing [Cosmic]) 1d Follow-Up on every damaging hit, ignoring worn DR.",
 forks="1. Magic Arrow damage and the item source levels (1 to 20) are not in the source; value is design. 2. Force is the closest 3.5e reading of D2's 'magic' damage.")
T["Freeze Target"] = e("DELTA", "Freezing (Elemental 09-16) + Slowing (Condition 01-08)", 2,
 "Proc: one d100 on each damaging hit, 01-10 fires. On fire the target must succeed on a Fortitude save (DC 14) or be held (frozen) for 1d2 rounds (the source's 1 to 9 seconds); on a success it is chilled instead (land speed x0.7, -1 on attacks, 1 round). Creatures of 17+ Hit Dice and creatures immune to cold are only chilled. Does not stack.",
 "On the same d100: Quick Contest of the target's HT against effective skill 14; on failure Affliction (Immobilized) for 1d6 seconds (source 1 to 9); on success or against Tier 1, Reduced Move 30% for 5 seconds.",
 forks="1. The source's chance formula depends on the Freeze Target total and the level gap; it is replaced by the fixed DC 14 save. 2. 'Normal and minion monsters only' is read as creatures under 17 Hit Dice.")
T["Hit Blinds Target"] = e("DELTA", "Blinding (Condition 43-48)", 1,
 "Proc: one d100 on each damaging hit, 01-10 fires. On fire the target is blinded for 1 round unless it succeeds on a Fortitude save (DC 14); a blinded creature can fight only at melee reach and cannot use special attacks or spell-like abilities at range. Creatures of 17+ Hit Dice are immune. Flee takes precedence if both effects fire.",
 "On the same d100: Quick Contest HT against effective skill 14; on failure Affliction (Blindness) for 6 seconds.",
 forks="1. Duration is not in the source (1 round assumed, the Blinding row's value). 2. The source blinds on a plain hit; the pool row blinds on a crit.")
T["Hit Causes Monster to Flee"] = e("DELTA", "Terrifying (Condition 25-30)", 1,
 "Proc: one d100 on each damaging hit, 01-10 fires. On fire the target must succeed on a Will save (DC 13) or flee from the attacker for 1d4 rounds (fear). Creatures of 17+ Hit Dice and mindless creatures are immune. Flee takes precedence over blind.",
 "On the same d100: Quick Contest Will against effective skill 13; on failure Terror for 1d4 seconds-rounds (4 to 24 seconds), exact 1d4 x 6 seconds.",
 forks="1. Duration is not in the source (1d4 rounds is the Terrifying row's). 2. The source's monsters 'may continue fleeing after expiry until their next AI check' has no 3.5e meaning.")
T["Ignore Target's Defense"] = e("NEW", "none", 3,
 "Melee and ranged. The wielder's attacks with this weapon against creatures of under 17 Hit Dice (the source's normal and minion monsters and character summons; not player characters, mercenaries, elites or bosses) resolve as touch attacks (the target's armor, shield and natural armor bonuses to AC are ignored; Dex, dodge and deflection still apply). Always on, no d100.",
 "The defender's Parry, Block and Dodge are rolled at -3 (a defender with 0 Defense in the source rolls as undefended); against Tier 1 targets and player characters the weapon has no effect.",
 forks="1. 'Defense 0' is read as a touch attack on the 3.5e side and as a -3 to the defender's 3d6 contest on the GURPS side (the engine does not name this mechanism). 2. Priced at +3: an always-on touch attack is stronger than MIC Impaling's 3/day at +1.")
T["Chance to Cast on Attack"] = e("NEW", "none", 2,
 "Proc: one d100 on each attack roll the wielder makes with this weapon, hit or miss (the source triggers on the attack attempt), 01-10 fires. On fire the weapon casts a spell chosen at creation (level 1 to 3, caster level 5, normal save DC for the spell level), centered on the target or the wielder as the spell requires. Melee weapons only. Procs never proc other procs.",
 "On the same d100 per attack roll: the chosen spell as an Innate Attack, resisted as the spell requires.",
 collision="DMG Spell Storing (a caster loads the spell); this weapon casts a fixed spell by itself. Different; names stay.",
 forks="1. The cast skill is chosen at creation and the source's skill level scales; a fixed spell level 1 to 3 at caster level 5 is used. 2. The source's chance varies by item (5 to 25% in the search example); the ratified 10% is used.")
T["Chance to Cast on Striking"] = e("NEW", "none", 2,
 "Proc: one d100 on each successful hit with this weapon (the hit must connect and not be blocked or dodged; damage is not required), 01-10 fires. On fire the weapon casts a spell chosen at creation (level 1 to 3, caster level 5, normal save DC), centered on the target (self-centered spells such as a nova or an aura center on the wielder). Melee weapons only.",
 "On the same d100 per successful strike: the chosen spell as an Innate Attack.",
 collision="Chance to Cast on Attack (same corpus), DMG Spell Storing: different triggers and sources; names stay.",
 forks="1. Same fixed-spell reading as Chance to Cast on Attack. 2. Differs from it only in needing a connecting hit.")
T["Open Wounds"] = e("DELTA", "Fatal Wound family (Affix Registry section 1) + Cursed Wound (Condition 55-60)", 1,
 "Proc: one d100 on each damaging hit, 01-10 fires. On fire the target bleeds 3 HP at the start of its turn for 2 rounds (8 s) and for that time cannot regenerate or benefit from fast healing (magical healing still works). Untyped, ignores DR, bloodless creatures immune. A new proc refreshes the timer and does not stack. Against creatures of 17+ Hit Dice the bleed is 1 HP per round.",
 "On the same d100: Follow-Up Toxic Attack 6 HP spread over exactly 8 seconds; suppresses regeneration for 8 seconds.",
 collision="Fatal Wound family (stacking bleed) and DMG Wounding; names stay, never merge.",
 forks="1. The source's damage scales with the character level (about 800 over 8 s at level 50); a flat 3 per round is the Magic rung of the bleed rows. 2. D2's bleed does not stack, unlike Fatal Wound; kept.")
T["Piercing Attack"] = e("NEW", "none", 1,
 "Ranged weapons only. On each damaging hit, d100 01-25 fires (the Magic-rung of the source's 25 to 100% item values): the missile continues to the next creature in a straight line within 10 ft behind the target, which is attacked as normal; this repeats up to 4 times (5 targets). A shield or block does not stop the missile.",
 "On the same d100: the missile continues to the next target behind, up to 4 times; each target gets its own active defenses.",
 forks="1. The source chance is set per item (25 to 100%); 25% is the Magic rung. 2. 'Behind the target' is read as a line within 10 ft.")
T["Prevent Monster Heal"] = e("DELTA", "Cursed Wound (Condition 55-60)", 1,
 "Proc: one d100 on each damaging hit, 01-10 fires. On fire the target cannot regenerate or benefit from fast healing for 80 minutes (the source's duration); magical healing and potions still work. Not applied by allies or summoned creatures, and not against named bosses.",
 "On the same d100: regeneration and fast healing suppressed for 80 minutes.",
 forks="1. The source applies it on every damaging hit (no chance); the ratified 10% proc is used to keep it a Registry-style proc. 2. Named bosses are immune (the source's list of event bosses).")
T["Life Regeneration"] = e("NEW", "none", 1,
 "While wielded the wielder has fast healing 1 (the Magic rung of the source's +3 to +5 life regeneration; the source gives no time unit). Fast healing is magical healing: it ends Fatal Wound stacks.",
 "Regeneration (slow) 1 HP per second while wielded, Gadget.",
 forks="1. The source's time unit is not given (the page says only '+3-5 life regeneration'); fast healing 1 is the Magic rung.")
