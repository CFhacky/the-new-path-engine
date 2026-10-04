"""Translations for the MIC specific-weapon and weapon-crystal corpus. Rate card = Crusader (Affix Registry section 2); rules = ../FUSED_ENGINE_RESOLUTION.md.

CONVENTIONS (stated once, applied to every entry):
- These are 3.5e items already: the 3.5e block restates the printed rules unchanged (activation, caster level, DCs, durations as printed). The source block in each entity file carries the normalized book text.
- Fused engine: item effects run on the 3.5e chassis. A printed save DC stays fixed. GURPS contributes only the defender's 3d6 contest and DR; where the book prints a save the GURPS crosswalk is a Quick Contest of the target's HT (Fort), Will (Will) or Dodge (Reflex) against an effective skill equal to the printed DC. GURPS dice read as-is; durations are 6 seconds per round. Riders ignore worn DR. No GURPS point totals on affix or item entries.
- Price: the printed market price (item level in brackets in the entry). Crystals: one price per rung, rungs Least / Lesser / Greater = the Magic / Rare / Unique rungs of the Crusader ladder.
- Tier from item level (the book's price-and-level pair): 1-4 Tier 5, 5-8 Tier 4, 9-12 Tier 3, 13-16 Tier 2, 17-20 Tier 1. A crystal's tier follows its Greater rung.
- GURPS chassis for all: Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); a crystal is a Gadget socketed into the weapon's Gadget.
- Relics: the printed alignment gate and worship/slot condition are kept; a wrong-aligned wielder simply gets the base weapon behaviour the book prints (no negative level; the Energy Drained ruling covers alignment-property weapons).
- Name collisions are checked mechanically against the Registry lexicon, the compendium files and entity slugs; hits are listed and the names stay.
"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
PACKET = os.path.join(HERE, "sources", "mic_specific_weapons_and_crystals.txt")
ORD = lambda s: int(re.match(r"(\d+)", s).group(1))
GAD = "Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen -10%). "
CONTEST = " Resist roll: Quick Contest of the target's {} against an effective skill equal to the printed DC ({})."
KIND = {"Fort": "HT", "Will": "Will", "Reflex": "Dodge"}

RELIC = {"Axe of Ancestral Virtue [RELIC]","Bow of the Wintermoon [RELIC]","Chain of Obeisance [RELIC]","Chromatic Rod [RELIC]","Cudgel That Never Forgets [RELIC]","Dagger of Denial [RELIC]","Dawnstar [RELIC]","Hooked Hammer of the Hearthfire [RELIC]","Morningstar of the Many [RELIC]","Rapier of Desperate Measures [RELIC]","Rapier of Unerring Direction [RELIC]","Raptor Arrow [RELIC]","Rod of the Recluse [RELIC]","Ruby Blade [RELIC]","Skewer-of-Gnomes [RELIC]","Spear of Retribution [RELIC]","Staff of the Unyielding Oak [RELIC]","Sword of Mighty Thews [RELIC]","Sword of Virtue Beyond Reproach [RELIC]"}
NECRO = {"Death Spike","Mace of the Dark Children","Rod of Defiance","Rod of Enervating Strike","Spectral Dagger","Scourge of Pain","Truedeath Crystal","Crystal of Life Drinking","Ruby Blade [RELIC]","Dagger of Denial [RELIC]","Ghost Net","Rod of the Recluse [RELIC]"}
CASTER = {"Bow of Songs","Crystal of Arcane Steel","Warlock's Scepter","Rod of Celestial Might","Mace of the Dark Children","Rod of Defiance","Crystal Echoblade","Witchlight Reservoir","Rogue Blade"}
CLASSLOCK = {"Bow of Songs","Crystal Echoblade","Mace of the Dark Children","Rod of Defiance","Warlock's Scepter","Galeb Duhr Hammer","Dwarf Crusher","Stonereaver","Quarterstaff of Battle"}

G = {  # per-item GURPS crosswalk line (effect only; chassis and contest sentence are appended)
"Arrow of Biting":"Innate Attack follow-up: injury poison (Toxic), primary at once and secondary one minute later, 1d6 as-is, resisted by HT vs 16.",
"Assassin Whip":"Binding of vegetation on a ground-standing Medium or smaller target: Innate Attack Crushing 2d6 each turn for 18 seconds; escape by ST or Escape Artist vs 20.",
"Axe of Ancestral Virtue [RELIC]":"Weapon bonuses per 3.5e (+1 keen adamantine waraxe, alignment-gated); relic powers as printed (bless, cure moderate wounds, faerie fire 3/day; haste at the higher slot); sapient item per the printed Ego 17.",
"Axe of the Sea Reavers":"Continuous water-walking on any surface of water; war cry (+2 morale to attack, damage, saves and checks for 6 seconds, 15 ft); panic (Fear Affliction) 6 seconds, Will vs 16.",
"Bladed Crossbow":"Switchable: heavy crossbow +1 (ranged) or battleaxe +1 (melee); the Gadget holds both modes.",
"Blazing Skylance":"Burning cone 15 ft: Innate Attack Burning 5d4 as-is, 3/day, Dodge-based contest vs 13 for half.",
"Bow of Songs":"Spend a bardic music use as a swift action: Charisma bonus added to the next attack roll and to its damage (3.5e chassis); no separate GURPS rider.",
"Bow of the Wintermoon [RELIC]":"+1 composite longbow (full Strength bonus to damage) when wielded by the listed alignments; relic power: frost and drow bane properties (registered in the DMG/MIC property corpus).",
"Bowstaff":"Swift (command) change between +1 masterwork quarterstaff and +1 longbow; both forms share the Gadget.",
"Chain of Obeisance [RELIC]":"+1 unholy spiked chain (alignment-gated); relic power: wieldable in a grapple as a light weapon; pin a foe and it is dominated (Will vs 22) as dominate monster, one creature at a time.",
"Chromatic Rod [RELIC]":"+1 morningstar; command word picks corrosive, frost, flaming or shock (one at a time); relic powers by slot or HD: wall of ice, insect plague, dominate person (Will vs 20), find the path, veil (Will vs 21), each 1/day.",
"Crystal Echoblade":"+1 longsword; each attack while the wielder is using bardic music adds sonic damage equal to half bard level as a Follow-Up damage rider.",
"Cudgel That Never Forgets [RELIC]":"+1 axiomatic heavy mace; relic: sapient (Int 16, Wis 10, Cha 16), cure moderate wounds 3/day, free demoralize each round; at the higher slot it marks foes that have hit the wielder (+2 enhancement and +2d6 vs that foe).",
"Dagger of Defiance":"+1 dagger; +3 resistance bonus on saves against enchantment and fear (applied to the wielder's contest rolls as +3).",
"Dagger of Denial [RELIC]":"+1 unholy dagger usable by any alignment; sapient (Ego 26); non-evil, non-neutral wielders are betrayed (it dispels their and their allies' spells); detect magic at will, greater dispel magic 1/day; at the higher slot continuous detect scrying and arcane eye 1/day.",
"Dawnstar [RELIC]":"+2 morningstar; relic: brilliant energy; if broken it explodes for 200/150/100 damage at 10/20/30 ft with Dodge contest vs 17 for half, wielder unharmed.",
"Death Spike":"+1 cold iron spear; on reducing a living creature to -1 HP or less in melee: 1d8 temporary HP and +2 morale damage for 1 hour, 3/day.",
"Dwarf Crusher":"Large +1 adamantine greatclub; next attack vs dwarf, construct or earth creature is a touch attack (needs ST 21 and Power Attack at -5), 3/day.",
"Explosive Sling":"+1 sling; stones deal +2d6 fire on hit (no resist) and 2d6 fire to creatures within 10 ft (Dodge contest vs 22 negates).",
"The Fist":"+1 adamantine spiked gauntlet; continuous protection from chill metal and heat metal; 1/day swift: extra 2d6, knockdown and stun 6 seconds (HT contest vs 22 negates).",
"Forceful Skylance":"3/day magic missile: three missiles at up to three targets within 150 ft (auto-hit).",
"Fountainhead Arrow":"Hit on a point (AC 5): geyser of acid, 10-ft radius burst each turn for 18 seconds, Innate Attack Corrosion 2d8 as-is, Dodge contest vs 14 for half.",
"Galeb Duhr Hammer":"+1 warhammer; with stonecunning, a critical hit on a creature standing on the ground holds it: speed 5 ft, -2 attack and AC for 30 seconds.",
"Ghost Net":"Thrown net; an incorporeal target hit becomes corporeal for damage purposes (no 50% miss) and cannot go ethereal; escape by Escape Artist vs 20; cannot be burst.",
"Hooked Hammer of the Hearthfire [RELIC]":"+1/+1 gnome hooked hammer; relic power: both ends flaming (flaming burst at the higher slot), kobolds and goblinoids take 1d6 fire per round holding it.",
"Lash of Sands":"+1 desiccating burst whip, lethal damage, works vs armor; 1/day on a hit: entangle as a net for 18 seconds, 1d4 per turn (1d8 vs plants and water elementals), nonliving take none.",
"Living Chain":"+1 spiked chain; +2 on Strength checks to trip the struck target.",
"Mace of the Dark Children":"+1 adamantine heavy mace; +3 profane bonus on rebuke attempts and level counts two higher for rebuke Hit Dice.",
"Manticore Greatsword":"+1 greatsword; launch one (standard) or six (full-round) spikes, Innate Attack Piercing 1d6 as-is each, range 20 ft increments; regrow at dawn.",
"Meteoric Knife":"+1 dagger, 3 charges per day: 1 returning for 6 seconds; 2 flaming and returning; 3 flaming, returning and on a hit +3d6 fire to target and adjacent (Dodge contest vs 14 for half).",
"Morningstar of the Many [RELIC]":"+1 morningstar that overcomes DR as chaotic, evil, good and lawful; relic: six-round mutation (vicious morningstar, flaming burst shortspear, anarchic morningstar, wounding battleaxe, unholy morningstar, vorpal longsword), 5/day. Vorpal round follows the engine ruling: a confirmed natural 20 forces Head at Lethal.",
"Pick of Piercing":"3/day, touch attack against a force object: disintegrate the object (wall of force, Bigby's hand).",
"Quarterstaff of Battle":"+1/+1 quarterstaff; Improved Disarm; abilities: 2 rounds deflection of small ranged attacks (3/day), speed on both ends 5 rounds (1/day), battlestrike +2d6, knockdown and stun (HT contest vs 22 negates) (1/day).",
"Rapier of Desperate Measures [RELIC]":"+2 rapier; relic power: keen under full HP, speed under half HP (engine: speed applies the printed extra attack, not an extra GURPS step).",
"Rapier of Unerring Direction [RELIC]":"+1 ghost touch rapier; relic power ignores all miss chances from concealment, blink and displacement (Registry convention: miss chance is 3.5e side).",
"Raptor Arrow [RELIC]":"+1 arrow with a returning variant (restrings the shooting bow next round, not destroyed); relic: bane against the targeted foe.",
"Rod of Cats":"+1/masterwork quarterstaff; continuous low-light vision and +5 Hide and Move Silently; 1/day spider climb 50 minutes or darkness on the rod; secret compartment (Search 25).",
"Rod of Celestial Might":"+1/+1 quarterstaff, usable abilities only by a non-evil wielder: 3/day holy smite as an immediate action after a hit on an evil outsider; 1/day summon an avoral guardinal near an evil outsider.",
"Rod of Defiance":"+1 heavy mace; undead within 30 ft are treated as 4 Hit Dice lower (minimum 1) for turn and rebuke checks.",
"Rod of Enervating Strike":"+1 heavy mace; each melee hit adds inflict light wounds (1d8+5, Will contest vs 11 for half), crit adds inflict serious wounds (3d8+15, Will vs 14); empowered on minor and maximized on major negative planes.",
"Rod of Freedom":"+4 silver heavy mace; +4 morale vs charm and compulsion; free-action nonlethal at will; swift dispel check 1d20+9 vs 11 + effect caster level on a struck charmed creature, 5/day.",
"Rod of the Recluse [RELIC]":"+2 light mace; relic: poison on next hit 5/day (Fort 20, 2d6 Str/2d6 Str; a crit makes it Strength drain); worshippers of Lolth.",
"Rod of Surprises":"+1 in all eight forms (javelin, kama, longspear, quarterstaff, scythe, shortspear, short sword, spear); stores a 25-word magic mouth message; extends 60 ft and bears 800 lb.",
"Rod of Whips":"3/day, 10 rounds: a force whip acting as a +1 dancing whip that strikes incorporeal creatures.",
"Rogue Blade":"+1 rapier; twice per day blink for 6 rounds, ends if the blade is dropped.",
"Ruby Blade [RELIC]":"+1 axiomatic dagger; relic: +4 effective level for rebuking or commanding undead (continuous); status 1/day.",
"Scourge of Pain":"+1 scourge; each hit adds 1d8 nonlethal and -4 to attack, saves and checks for 1d4 rounds (HT contest vs 17 negates; no stacking).",
"Skewer-of-Gnomes [RELIC]":"Small +1 gnome bane spear; relic: unholy, quasisentience, auto set against a charge dealing double damage (attack at highest BAB).",
"Spear of Retribution [RELIC]":"+1 returning spear; relic: +2 morale on attack and damage vs any enemy that damaged the wielder last round; keen vs one that critted.",
"Spectral Dagger":"No enhancement; attacks are touch attacks; a struck target suffers chill touch (HT contest vs 11 partial or Will vs 11 negates); fades if released.",
"Spider Fang":"+1 dagger; cuts webs without sticking, half speed through web spells, 1/day 10x10 ft web curtain (concealment, collapses for 2d4 acid on touch).",
"Staff of the Unyielding Oak [RELIC]":"+1/+1 quarterstaff; relic: becomes a real treant (changestaff), 12 hours a day, 28 days of dormancy if reduced to 0 HP.",
"Stonereaver":"+1 greataxe; in a dwarf's hands bane against earth elementals and constructs of earth, stone or metal.",
"Stunshot Sling":"+1 sling; 3/day free action: the next hit must beat a Fortitude save equal to the attack roll or be stunned 6 seconds (HT contest against the attack roll result).",
"Sword of Mighty Thews [RELIC]":"+1 dragonbane greatsword; relic: immune to dragon frightful presence, +5 luck on Reflex saves vs breath weapons.",
"Sword of Virtue Beyond Reproach [RELIC]":"+1 holy longsword; relic: a failed save vs charm or compulsion is suppressed for 1d4 rounds (GM rolls secretly) and takes effect afterwards.",
"Swordbow":"Free-command swap between +1 longbow and +1 longsword; the two forms share one enhancement bonus, improving it costs as two weapons.",
"Swordbow, Great":"Swordbow whose forms are +1 composite longbow (+4 Str) and +1 greatsword.",
"Swordbow, Light":"Swordbow whose forms are +1 shortbow and +1 rapier.",
"Tentacle Rod":"Standard (command): three tentacle attacks at +12 for 6 bludgeoning each; all three hit slows the target 30 seconds (HT contest vs 14 negates).",
"Tentacle Rod, Greater":"Six tentacle attacks at +18 for 9 bludgeoning each; three or more hits fatigue, all six exhaust (HT contest vs 20 negates).",
"Trident of Serenity":"+1 trident; 3/day calm emotions on the wielder for 30 seconds, Will contest vs 16; a creature that resists is immune 24 hours.",
"Viperblade":"+1 dagger, 5 charges: next hit envenomed, 1d6 Con (primary and secondary), Fort DC 12, 15 or 18 by charges spent (HT contest).",
"Warlock's Scepter":"+1 light mace; +1 profane on ranged touch attacks; charges add +1d6, +2d6 or +4d6 to the next eldritch blast.",
"Water Whip":"+1 whip dealing lethal damage, works against armor; returns to hand within 30 ft; frost or flaming +1d6 chosen on activation.",
"Whip of Webs":"+1 whip; 3/day on a hit entangle as a net for 18 seconds; no stacking.",
"Crystal of Adamant Weaponry":"Weapon Breakable DR improved by 2 / 5 / 10 steps on the Gadget (the hardness of 3.5e becomes Gadget DR).",
"Crystal of Arcane Steel":"Rider on a spell delivered through the weapon: +1 damage, +1 attack, then +1 to the effect's resist DC (Quick Contest effective skill +1).",
"Crystal of Energy Assault (acid, cold, electricity, fire)":"Follow-Up damage rider of the crystal's type: +1 / +1d6 / +1d6 with the greater secondary effect (acid -1 AC; cold -10 ft speed; electricity dazzled; fire +1d6 next round).",
"Crystal of Illumination":"Swift command: light radius 5 / 20 / 60 ft with equal shadowy ring.",
"Crystal of Life Drinking":"On each damaging hit to a living target the wielder heals 1 / 3 / 5 HP up to a daily cap of 10 / 30 / 50 HP.",
"Crystal of Return":"Free draw; call from 30 ft (move action); greater adds returning on thrown weapons.",
"Crystal of Security":"+2 / +5 / +10 on checks to draw or keep the weapon (grappling, disarm, Strength contest).",
"Demolition Crystal":"+1d6 vs constructs; adamantine for construct DR; sneak attack and crits against constructs.",
"Fiendslayer Crystal":"+1d6 vs evil outsiders; good-aligned for DR; greater crit blocks teleport for 6 seconds; an evil wielder takes one negative level while holding it (Energy Drained, never level loss).",
"Phoenix Ash Threat":"Smoldering embers: 1 / 3 / 5 fire damage to each target hit last round, no stacking.",
"Revelation Crystal":"Hit on an invisible creature: golden aura for 6 seconds, with greater rungs suppressing invisibility and then blur or displacement; miss chance stays 50%.",
"Truedeath Crystal":"+1d6 vs undead; ghost touch; sneak attacks and crits against undead.",
"Witchlight Reservoir":"Expose 8 hours to sunlight, moonlight, blood or wine; swift activation adds +2d6 fire (+4d6 undead), +2d6 electricity (+4d6 lycanthropes), +2d6 to a living target, or -2 Will saves for 6 seconds; five uses then recharge.",
}
# crystal verdicts / pool bases; every specific weapon is a NEW item (a specific item is not an affix family)
CRYSTAL = {"Crystal of Adamant Weaponry":("NEW","none"),"Crystal of Arcane Steel":("NEW","none"),"Crystal of Energy Assault (acid, cold, electricity, fire)":("DELTA","Flaming (Elemental 01-08) / Freezing (09-16) / Shocking (17-24) / Corrosive: the crystal is a socketable ladder with a greater-rung secondary effect"),"Crystal of Illumination":("NEW","none"),"Crystal of Life Drinking":("DELTA","Leech (Resource 19-24): same heal-on-hit shape, here with a daily cap"),"Crystal of Return":("DELTA","Returning (DMG weapon property, registered in the weapon-affix corpus)"),"Crystal of Security":("NEW","none"),"Demolition Crystal":("DELTA","Bane (construct) family in the weapon-affix corpus"),"Fiendslayer Crystal":("DELTA","Bane (evil outsider) and Holy in the weapon-affix corpus"),"Phoenix Ash Threat":("DELTA","Flaming (Elemental 01-08): lingering fire the following round"),"Revelation Crystal":("NEW","none"),"Truedeath Crystal":("DELTA","Bane (undead) and Ghost Touch in the weapon-affix corpus"),"Witchlight Reservoir":("NEW","none")}
FORKS = {
"Axe of Sea Reavers":"",
}
GAPS = {"Storm gauntlets":"entry text not found in the OCR range read; excluded."}

def _load():
    blocks = re.split(r"^=== (.+?) ===\n", open(PACKET, encoding="utf-8").read(), flags=re.M)[1:]
    out = {}
    for name, body in zip(blocks[0::2], blocks[1::2]):
        f = dict(re.findall(r"^(group|quality|url|tooltip|facts|gaps): (.*)$", body, flags=re.M))
        crystal = f["group"].startswith("Weapon augment")
        if crystal:
            ils = [ORD(x) for x in re.findall(r"\((\d+)(?:st|nd|rd|th)\)", f["facts"])]
            price = re.search(r"prices \(item level\): (.*?); caster", f["facts"]).group(1)
            il = ils[-1]; verdict, base = CRYSTAL[name]
            ladder = ("3.5e ladder: Least = Magic rung, Lesser = Rare rung, Greater = Unique rung of the Crusader ladder." if "least" in price else "Single item; the book calls it a greater augment crystal (Unique rung).")
        else:
            il = ORD(re.search(r"item level (\d+)", f["facts"]).group(1)); price = re.match(r"([\d,]+ gp)", f["facts"]).group(1)
            verdict, base = "NEW", "none (specific item; no affix family involved)"; ladder = ""
        tier = 5 if il <= 4 else 4 if il <= 8 else 3 if il <= 12 else 2 if il <= 16 else 1
        resist = re.findall(r"(Fort|Will|Reflex)\s*(?:DC)?\s*(\d+)", f["tooltip"])
        adj = ""
        if name in RELIC: adj += " Relic: the printed alignment gate and worship or slot condition apply exactly as printed; outside them the item is a masterwork weapon."
        if name == "Dagger of Denial [RELIC]": adj += " Betrayal clause (non-evil, non-neutral wielder) is kept as printed; recommended NPC-side use."
        if name == "Fiendslayer Crystal": adj += " The negative level is the Energy Drained condition (per ruling), never level loss."
        three_e = f"Rules as printed in MIC (restated in the source block): {f['tooltip']}{adj} {ladder}".strip()
        gurps = GAD + G[name] + (CONTEST.format(" / ".join(sorted({KIND[k] for k, _ in resist})), ", ".join(sorted({d for _, d in resist}, key=int))) if resist else "")
        out[name] = dict(verdict=verdict, base=base, tier=tier, il=il, price=price, three_e=three_e, gurps=gurps, collision="__AUTO__", forks="none.", note="", relic=name in RELIC)
    return out
T = _load()
