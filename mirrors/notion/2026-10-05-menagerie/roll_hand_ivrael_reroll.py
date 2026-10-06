"""Ivrael Quillatar signature weapon, REROLL (Chad, 6 Oct 2026: 'include logical sense in the criteria').
loot_roll.py functions, Python secrets, binding. Base AUTHORED from his look (no base roll): a long single-edged
elven blade worn edge-up -> bastard sword stats. Hooks: CR 14, named, archetype martial.
LOGIC CRITERION (stated before rolling): a draw that cannot make sense for a Fighter 14 with no spells, no familiar,
no companion and no summons, on a slashing blade, is rerolled within the same pool/table and logged."""
import sys
sys.path.insert(0, "/root/.claude/skills/synced/07327e22-ff68-47f1-ad4a-8176d4a886f0_c7d5c9b9-16d6-4e70-9b16-504f3872f1f8/loot-engine/scripts")
from loot_roll import (load_tables, set_tier, roll_rarity, affix_count, pick_pool, band_lookup, tier_value,
                       greater_affixes, masterwork, die, out, TEMPER_FAMILIES, ASPECT_TABLES, SOCKET_COUNT, SOCKET_TYPE)

ILLOGICAL_AFFIX = {  # name: reason
 "Mana Well": "no spells", "Cost Reduction": "no spells", "Spell Recovery": "no spells", "Mana Leech": "no spells",
 "Wellspring": "no spells", "Reservoir": "no spells", "Souldrinker": "no spells", "Catalyst": "no spells",
 "Conduit": "no metamagic", "Overcharge": "no spells", "Bloodprice": "no mana", "Undying Flame": "no mana",
 "Arcane Amplification": "not an arcane caster", "Sacred Word": "not a divine caster", "Sneak's Edge": "no sneak attack",
 "Wild Shape": "no wild shape", "Metamagic Font": "no spells", "Turn Mastery": "cannot turn", "Animal Bond": "no animal",
 "Familiar Bond": "no familiar", "Channel": "no caster level", "Stalker's Art": "no sneak attack (ranged)",
 "Wardbreaker": "no caster level", "Elemental Attunement": "no spells", "Beast Bond": "no companion",
 "Familiar Augment": "no familiar", "Minion": "a sword-duellist, not a summoner", "Pack": "not a summoner",
 "Spectral Guardian": "fits (kept)", "Undead Servitor": "not a necromancer", "Elemental Shard": "not a summoner",
 "Shadow Clone": "fits (kept)", "Bound Spirit": "fits (kept)", "Titan's Grip": "a fine blade, not an oversize weapon",
 "Devastating Charge": "fits (kept)", "Thorns": "fits (kept)", "Shield Wall": "carries no shield",
}
KEEP = {k for k, v in ILLOGICAL_AFFIX.items() if v.startswith("fits")}
ILLOGICAL_TEMPER_FAMILY = {"D": "Resource tempers run on mana", "F": "Minion tempers need minions"}
ILLOGICAL_ASPECT = {"D": "Resource-loop aspects run on mana", "F": "Summon aspects need summons",
                    ("E", 1): "Torrent reshapes spells", ("E", 2): "Lance reshapes spells", ("E", 3): "Chain reshapes spells",
                    ("E", 4): "Duration reshapes spells", ("E", 5): "Detonation needs DoT spells", ("E", 6): "Empowerment needs buff spells",
                    ("E", 8): "Comet needs a ranged attack", ("I", 2): "Blood Mage needs spells", ("I", 7): "Death Knight raises dead (not his art)"}

def draw(tables, n, tier):
    drawn, uses = [], {}
    while len(drawn) < n:
        pool = pick_pool("martial")
        if uses.get(pool, 0) >= 2:
            out(f"    pool restriction: {pool} used 2x -> reroll pool"); continue
        while True:
            r = die(100); row = band_lookup(tables[pool], r)
            if row is None: out(f"    d100={r} -> no row -> reroll"); continue
            nm = row["name"]
            if any(d["name"] == nm for d in drawn): out(f"    d100={r} -> {nm} DUPLICATE -> reroll within pool"); continue
            if nm in ILLOGICAL_AFFIX and nm not in KEEP:
                out(f"    d100={r} -> {nm} -- LOGIC: {ILLOGICAL_AFFIX[nm]} -> reroll within pool"); continue
            if pool == "Rare Build-Around":
                import re
                m = re.search(r"T(\d)", row["cells"][-1] if row["cells"] else "")
                if m and tier > int(m.group(1)): out(f"    d100={r} -> {nm} tier-gated -> reroll"); continue
            break
        uses[pool] = uses.get(pool, 0) + 1
        tv = tier_value(" ".join(row["cells"]), tier) if row["cells"] else None
        out(f"    d100={r} -> {nm} [{pool}]" + (f" | T{tier} value: {tv}" if tv else ""))
        drawn.append({"name": nm, "pool": pool, "cells": row["cells"]})
    return drawn

def temper_roll(rarity):
    slots = 1 if rarity == "Legendary" else (1 if (rarity == "Rare" and die(100) <= 50) else 0)
    out(f"TEMPER SLOTS: {rarity} -> {slots}")
    for _ in range(slots):
        while True:
            f = die(10); fam = TEMPER_FAMILIES[f-1]
            if fam.startswith("J"): out(f"  TEMPER: d10={f} -> {fam} -- DM gate -> reroll"); continue
            if fam[0] in ILLOGICAL_TEMPER_FAMILY: out(f"  TEMPER: d10={f} -> {fam} -- LOGIC: {ILLOGICAL_TEMPER_FAMILY[fam[0]]} -> reroll"); continue
            e = die(10); out(f"  TEMPER: d10={f} -> family {fam}; entry d10={e} (23{fam[0]})"); break

def aspect_roll(rarity, tier):
    if rarity not in ("Legendary", "Ancestral Legendary"): out(f"LEGENDARY ASPECT: {rarity} -> n/a"); return
    while True:
        t = die(10); tab = ASPECT_TABLES[t-1]
        if tab.startswith("J") and tier > 1: out(f"ASPECT: d10={t} -> {tab} -- T1 only -> reroll"); continue
        if tab[0] in ILLOGICAL_ASPECT: out(f"ASPECT: d10={t} -> {tab} -- LOGIC: {ILLOGICAL_ASPECT[tab[0]]} -> reroll"); continue
        e = die(6 if tab.startswith("J") else 8)
        if (tab[0], e) in ILLOGICAL_ASPECT: out(f"ASPECT: d10={t} -> {tab}; entry {e} -- LOGIC: {ILLOGICAL_ASPECT[(tab[0], e)]} -> reroll"); continue
        out(f"LEGENDARY ASPECT: d10={t} -> table {tab}; entry d{'6' if tab.startswith('J') else '8'}={e} (24{tab[0]})"); break

def main():
    T = load_tables()
    out("=" * 62); out("IVRAEL QUILLATAR -- SIGNATURE WEAPON REROLL -- BINDING (logic criterion in force)"); out("=" * 62)
    out("BASE: AUTHORED -- elven single-edged longblade worn edge-up, bastard sword stats (1d10, 19-20, S)")
    tier, _ = set_tier(14, "named")
    rarity, _ = roll_rarity("named")
    if rarity in ("Unique", "Mythic / Artifact"):
        out(f"-> {rarity}: author per unique-design.md")
        r = die(16); out(f"UDRP BASE: 1d16+14 -> raw {r} -> {r+14}")
    else:
        n = affix_count(rarity); out("AFFIX DRAWS:")
        drawn = draw(T, n, tier)
        greater_affixes(rarity, drawn, tier)
        temper_roll(rarity); aspect_roll(rarity, tier)
        r = die(100); cnt = band_lookup([{"lo": a, "hi": b, "name": x} for a, b, x in SOCKET_COUNT], r)["name"]
        out(f"SOCKETS: d100={r} -> {cnt}")
        for i in range(max(cnt, 0)):
            t = die(100); ty = band_lookup([{"lo": a, "hi": b, "name": x} for a, b, x in SOCKET_TYPE], t)["name"]
            out(f"  SOCKET {i+1}: d100={t} -> {ty}")
            if ty == "Gem":
                g = die(7); out(f"    gem d7={g} -> {['Ruby','Sapphire','Emerald','Diamond','Topaz','Amethyst','Skull'][g-1]}")
        masterwork(rarity)
        if rarity in ("Legendary", "Ancestral Legendary", "Unique"):
            pass
        base = {"Rare": (1, 4, 2), "Legendary": (2, 4, 4), "Ancestral Legendary": (2, 5, 8), "Magic": (1, 3, 0)}[rarity]
        raws = [die(base[1]) for _ in range(base[0])]; out(f"UDRP BASE: {rarity} -> raw {raws} +{base[2]} -> {sum(raws)+base[2]}")
    c = die(4); out(f"ITEM CL: 1d4+12 -> raw {c} -> {c+12}")

if __name__ == "__main__":
    main()
