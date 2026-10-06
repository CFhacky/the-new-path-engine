"""FULL-CORPUS AFFIX PASS (Chad, 6 Oct 2026): re-roll the affix layer of the 21 non-Unique signature pieces
(Menagerie 17 + Hand 4) against the loot-engine pools PLUS the registered compendia. Python secrets via loot_roll.py.
Every throw is printed. Rules stated before rolling:
 CORPUS: loot-engine pools (136 rows) + AFFIX_LEXICON NEW/DELTA (not INACTIVE) + D2 modifiers + Warhammer runes
   (source: docs/translation/*, branch ccr-6d9e69ce-nd0fn0; snapshot corpus_affixes_source.json).
   EXCLUDED: WoW enchants, MIC augment crystals, runewords (laid on after creation, Chad); MIC specific weapons (finished
   items); COVERED lexicon rows (duplicates of pool rows); Master Rune of Kragg the Grim (no effect).
 SELECTION: d100 picks the pool by archetype (CLASS_WEIGHTS); then d(N) picks a row uniformly from that pool's N rows.
 NO DUPLICATES (host): first piece to draw an affix keeps it; a later draw of it rerolls within the pool. Also no
   duplicate of the piece's own masterwork property.
 LOGIC: a draw the bearer cannot use (needs spells/CL, sneak attack, rage, turning, ki, smite, bardic music, favoured
   enemy, a companion or familiar, a ranged weapon or ammunition, a thrown weapon, a bludgeoning or spear head; or any
   weapon property / on-hit row on a non-weapon) rerolls within the pool. Tempers and aspects likewise.
 KEPT: rarity, affix count, masterwork result, sockets, Uniques, bases, releases. RE-ROLLED: affixes, Greater, temper,
   aspect, masterwork capstone picks."""
import sys, json, re
sys.path.insert(0, "/root/.claude/skills/synced/07327e22-ff68-47f1-ad4a-8176d4a886f0_c7d5c9b9-16d6-4e70-9b16-504f3872f1f8/loot-engine/scripts")
from loot_roll import load_tables, die, out, pick_pool, tier_value, GREATER_CHANCE, TEMPER_FAMILIES, ASPECT_TABLES

# ---------- corpus pool placement (by effect) ----------
PLACE = {
 "Offensive": ["Bane","Brilliant Energy","Collision","Dancing","Eager","Fiercebane","Ghost Touch","Ghost Strike","Ethereal Reaver",
   "Impaling","Merciful","Mighty Cleaving","Magebane","Dragondoom","Dragonhunter","Precise","Seeking","Distance","Quick Loading",
   "Returning","Throwing","Shadowstrike","Sundering","Transmuting","Vorpal","Vicious","Whirling","Disruption","Blurstrike",
   "Fleshgrinding","Illusion Bane","Incorporeal Binding","Force","IGNORE TARGET'S DEFENSE","CRUSHING BLOW","PIERCING ATTACK",
   "FIRES MAGIC ARROWS","MASTER RUNE OF ALARIC THE MAD","MASTER RUNE OF DEATH","MASTER RUNE OF DRAGON SLAYING",
   "MASTER RUNE OF SMITING","RUNE OF CLEAVING","RUNE OF DAEMON SLAYING","RUNE OF FURY","RUNE OF MIGHT","RUNE OF STRIKING",
   "MASTER RUNE OF BREAKING","MASTER RUNE OF FLIGHT","MASTER RUNE OF SKALF BLACKHAMMER","MASTER RUNE OF SNORRI SPANGELHELM",
   "MASTER RUNE OF SWIFTNESS","GRUDGE RUNE","MASTER RUNE OF BANISHMENT"],
 "Defensive": ["Defending","Defensive Surge","Parrying","Shielding","Spellstrike","LIFE REGENERATION"],
 "Resource": ["Bloodfeeding","Vampiric","Body Feeder","Souldrinking","Spell Storing","Bloodstone","Illusion Theft",
   "CHANCE TO CAST ON ATTACK","CHANCE TO CAST ON STRIKING"],
 "Utility": ["Aquatic","Blindsighted","Changeling","Hideaway","Illuminating","Morphing","Sizing","Metalline","Everbright"],
 "Skill/Class": ["Arcane Might","Divine Wrath","Ki Focus","Hunting","Mighty Smiting","Harmonizing","Berserker","Brash",
   "Resounding","Sweeping","Disarming","Necrotic Focus"],
 "Elemental": ["Acidic Burst","Flaming Burst","Icy Burst","Shocking Burst","Energy Aura","Energy Surge","Desiccating",
   "Desiccating Burst","Screaming","Screaming Burst","Thundering","Holy","Unholy","Anarchic","Axiomatic","Holy Surge",
   "Unholy Surge","Sacred","Sacred Burst","Profane","Profane Burst","Heavenly Burst","Aquan","Auran","Ignan","Terran",
   "Prismatic Burst","FIRES EXPLOSIVE ARROWS OR BOLTS","RUNE OF FIRE"],
 "Condition/Control": ["Binding","Brutal Surge","Chargebreaker","Cursespewing","Dislocator","Dislocator, Great","Domineering",
   "Doom Burst","Enervating","Soulbreaker","Stygian","Impedance","Paralytic Burst","Paralyzing","Revealing","Slow Burst",
   "Stunning","Stunning Surge","Weakening","Wounding","Implacable","Venomous","Banishing","Shattermantle","FREEZE TARGET",
   "HIT BLINDS TARGET","HIT CAUSES MONSTER TO FLEE","OPEN WOUNDS","PREVENT MONSTER HEAL","RUNE OF DISMAY"],
}
# requirement tags: corpus + pool rows. Keys checked against bearer profile.
REQ = {
 # corpus
 "Distance":"ranged","Seeking":"ranged","Quick Loading":"crossbow","Precise":"ranged_or_thrown","Force":"ranged",
 "Dragonhunter":"ranged","FIRES EXPLOSIVE ARROWS OR BOLTS":"ranged","FIRES MAGIC ARROWS":"ranged","PIERCING ATTACK":"ranged",
 "Returning":"thrown","Throwing":"melee","MASTER RUNE OF FLIGHT":"melee","Berserker":"rage","Brash":"rage",
 "Arcane Might":"arcane","Divine Wrath":"turn","Ki Focus":"ki","Harmonizing":"bard","Mighty Smiting":"smite",
 "Hunting":"favored_enemy","Necrotic Focus":"drain","Disruption":"bludgeon","Changeling":"spear","Mighty Cleaving":"melee",
 "Whirling":"melee","Fleshgrinding":"melee","Shielding":"melee","Defensive Surge":"melee","Brutal Surge":"melee",
 "Energy Surge":"melee","Holy Surge":"melee","Unholy Surge":"melee","Stunning Surge":"melee","CRUSHING BLOW":"melee",
 "Shadowstrike":"melee","Sweeping":"melee","Sundering":"melee",
 # pool rows
 "Mana Well":"caster","Cost Reduction":"caster","Spell Recovery":"caster","Mana Leech":"caster","Wellspring":"caster",
 "Reservoir":"caster","Souldrinker":"caster","Catalyst":"caster","Conduit":"caster","Overcharge":"caster","Bloodprice":"caster",
 "Undying Flame":"caster","Metamagic Font":"caster","Elemental Attunement":"caster","Wardbreaker":"caster","Channel":"caster",
 "Arcane Amplification":"arcane","Sacred Word":"divine","Turn Mastery":"turn","Guided Hand":"divine","Sneak's Edge":"sneak",
 "Stalker's Art":"sneak","Wild Shape":"wildshape","Animal Bond":"animal","Beast Bond":"companion","Familiar Bond":"familiar",
 "Familiar Augment":"familiar","Keen Edge":"edged","Vorpal Edge":"slashing","Savage Blow":"melee","Titan's Grip":"heavy",
 "Devastating Charge":"melee","Riposte":"melee","Bladesinger":"weapon","Weapon Mastery":"weapon",
}
ONHIT_POOLS = {"Offensive","Condition/Control"}
ELEMENTAL_DMG = {"Flaming","Freezing","Shocking","Corroding","Venomous","Shadowtouch","Radiant","Stormborn","Prismatic",
   "Elemental Burst","Banefire","Chaos Element"}

def bearer_ok(tag, P):
    if tag is None: return True
    w=P["weapon"]
    m={"ranged":P.get("ranged",False),"crossbow":P.get("crossbow",False),"ranged_or_thrown":P.get("ranged",False) or P.get("thrown",False),
       "thrown":P.get("thrown",False),"melee":w and not P.get("ranged",False),"rage":"rage" in P["f"],"arcane":"arcane" in P["f"],
       "divine":"divine" in P["f"],"caster":bool({"arcane","divine","psionic"}&P["f"]),"turn":"turn" in P["f"],"ki":"ki" in P["f"],
       "bard":False,"smite":False,"favored_enemy":"favored_enemy" in P["f"],"drain":False,"bludgeon":P.get("dmg")=="B",
       "spear":P.get("spear",False),"sneak":"sneak" in P["f"],"wildshape":"wildshape" in P["f"],"animal":bool({"companion","wildshape"}&P["f"]),
       "companion":"companion" in P["f"],"familiar":False,"edged":P.get("dmg") in ("S","P","SP"),"slashing":P.get("dmg") in ("S","SP"),
       "heavy":P.get("heavy",False),"weapon":w}
    return m[tag]

def build(T, R):
    pools={p:[{"name":r["name"],"src":"pool","cells":r["cells"]} for r in T[p]] for p in T if p in PLACE or p in ("Summoning/Companion","Rare Build-Around")}
    by={r["name"]:r for r in R}
    for p,names in PLACE.items():
        for n in names:
            r=by[n]; pools[p].append({"name":n,"src":r["src"],"cells":None,"effect":r["effect"],"price":r.get("price","")})
    return pools

PIECES = [ # (bearer, CR, archetype, rarity, count, MWprop, profile)
 ("Quavein",17,"divine","Legendary",4,"mighty cleaving",dict(weapon=True,dmg="B",heavy=True,f={"divine","turn","summoner"})),
 ("Hadda",16,"arcane","Legendary",4,"flaming burst",dict(weapon=True,dmg="P",f={"arcane"})),
 ("Tarvash",17,"martial","Rare",3,None,dict(weapon=True,dmg="S",f=set())),
 ("Aerendyl",16,"martial","Rare",3,None,dict(weapon=True,dmg="B",f={"ki"})),
 ("Kesh",16,"martial","Legendary",4,"shocking burst",dict(weapon=True,dmg="S",f={"divine","companion","favored_enemy"})),
 ("Marit",17,"shadow","Legendary",4,None,dict(weapon=True,dmg="P",f={"arcane","sneak"})),
 ("Brunna",16,"shadow","Legendary",4,"icy burst",dict(weapon=True,dmg="P",f=set())),
 ("Zaheda",16,"divine","Legendary",4,None,dict(weapon=False,f={"divine","wildshape","summoner"})),
 ("Ysmay",16,"martial","Rare",3,None,dict(weapon=True,dmg="S",heavy=True,f=set())),
 ("Dace",16,"hybrid","Rare",3,None,dict(weapon=True,dmg="P",spear=True,thrown=True,f={"psionic"})),
 ("Osmund",12,"divine","Legendary",4,"ghost touch",dict(weapon=True,dmg="B",f={"divine","turn","summoner"})),
 ("Wenna",14,"arcane","Rare",3,None,dict(weapon=True,dmg="S",thrown=True,f={"arcane"})),
 ("Faelith",14,"martial","Legendary",4,"bashing",dict(weapon=True,dmg="B",f=set())),
 ("Patience",13,"martial","Rare",3,None,dict(weapon=True,dmg="B",heavy=True,f=set())),
 ("Rhun",13,"martial","Legendary",4,None,dict(weapon=True,dmg="SP",heavy=True,f=set())),
 ("Edwyn",13,"arcane","Legendary",4,"defending",dict(weapon=True,dmg="P",f={"arcane","summoner"})),
 ("Ashavel",14,"shadow","Rare",3,None,dict(weapon=True,dmg="SP",f=set())),
 ("Ivrael (Hand)",14,"martial","Rare",3,None,dict(weapon=True,dmg="S",heavy=True,f=set())),
 ("Teodric (Hand)",14,"arcane","Rare",3,None,dict(weapon=True,dmg="S",heavy=True,f={"arcane"})),
 ("Durgan (Hand)",14,"arcane","Rare",3,None,dict(weapon=True,dmg="P",ranged=True,crossbow=True,f={"arcane"})),
 ("Lorne (Hand)",13,"divine","Rare",3,None,dict(weapon=True,dmg="S",f={"divine","turn","summoner"})),
]
TIER={k:(1 if cr>=13 else 2) for k,cr,*_ in PIECES}; TIER["Osmund"]=2
CAPSTONE={"Brunna","Zaheda"}

def main():
    T=load_tables(); R=json.load(open("corpus_affixes_source.json")); pools=build(T,R)
    out("="*70); out("FULL-CORPUS AFFIX PASS — loot_roll.py dice (Python secrets) — BINDING — every throw printed"); out("="*70)
    out("Pool sizes: "+", ".join(f"{p} {len(v)}" for p,v in pools.items())+f" | total {sum(len(v) for v in pools.values())}")
    host=set(); summary={}
    for name,cr,arch,rar,n,mw,P in PIECES:
        t=TIER[name]; out(); out(f"### {name} · CR {cr} · T{t} · {rar} ({n} affixes, kept) · archetype {arch} · MW property kept: {mw}")
        drawn=[]; uses={}
        while len(drawn)<n:
            pool=pick_pool(arch)
            if pool not in pools: out(f"  pool {pool} not available -> reroll pool"); continue
            if uses.get(pool,0)>=2: out(f"  pool restriction: {pool} used 2x -> reroll pool"); continue
            if not P["weapon"] and pool in ONHIT_POOLS: out(f"  {pool}: on-hit pool, the piece is not a weapon (LOGIC) -> reroll pool"); continue
            rows=pools[pool]; tries=0
            while True:
                tries+=1
                if tries>60: out(f"  {pool}: no usable row after 60 throws -> reroll pool"); row=None; break
                k=die(len(rows)); row=rows[k-1]; nm=row["name"]; tag=f"{nm} [{pool}{'' if row['src']=='pool' else ' · '+row['src']}]"
                if nm in host: out(f"    d{len(rows)}={k} -> {tag} — HOST DUPLICATE -> reroll"); continue
                if mw and nm.lower()==mw.lower(): out(f"    d{len(rows)}={k} -> {tag} — duplicates the piece's masterwork property -> reroll"); continue
                if any(d["name"]==nm for d in drawn): out(f"    d{len(rows)}={k} -> {tag} — duplicate on piece -> reroll"); continue
                if row["src"]!="pool" and not P["weapon"]: out(f"    d{len(rows)}={k} -> {tag} — LOGIC: weapon property on a non-weapon -> reroll"); continue
                if not P["weapon"] and nm in ELEMENTAL_DMG: out(f"    d{len(rows)}={k} -> {tag} — LOGIC: on-hit rider on a non-weapon -> reroll"); continue
                if not bearer_ok(REQ.get(nm),P): out(f"    d{len(rows)}={k} -> {tag} — LOGIC: needs {REQ[nm]} -> reroll"); continue
                if pool=="Rare Build-Around" and row["cells"]:
                    m=re.search(r"T(\d)",row["cells"][-1])
                    if m and t>int(m.group(1)): out(f"    d{len(rows)}={k} -> {tag} — tier-gated -> reroll"); continue
                break
            if row is None: continue
            tv=tier_value(" ".join(row["cells"]),t) if row.get("cells") else None
            out(f"    d{len(rows)}={k} -> {tag}"+(f" | T{t} value: {tv}" if tv else (f" | {row.get('price','')}" if row['src']!='pool' else "")))
            drawn.append({"name":nm,"pool":pool,"src":row["src"]}); uses[pool]=uses.get(pool,0)+1; host.add(nm)
        # greater
        ch=GREATER_CHANCE.get(rar); greater=[]
        if ch and not (rar=="Rare" and t>2):
            for d in drawn:
                r=die(100); hit=r<=ch; out(f"  GREATER [{d['name']}]: d100={r} vs {ch}% -> {'GREATER' if hit else 'no'}")
                if hit: greater.append(d["name"])
        # capstone
        if name in CAPSTONE:
            cand=[d["name"] for d in drawn if d["name"] not in greater]
            if cand: k=die(len(cand)); out(f"  CAPSTONE (MW 20, kept): d{len(cand)}={k} -> {cand[k-1]} becomes Greater"); greater.append(cand[k-1])
        # temper
        if rar=="Legendary": slots=1; out("  TEMPER SLOTS: Legendary -> 1")
        else: r=die(100); slots=1 if r<=50 else 0; out(f"  TEMPER SLOTS: Rare d100={r} -> {slots}")
        has_el=any(d["pool"]=="Elemental" for d in drawn) or (mw or "").endswith("burst")
        has_cc=any(d["pool"]=="Condition/Control" for d in drawn)
        temper=None
        for _ in range(slots):
            while True:
                f=die(10); fam=TEMPER_FAMILIES[f-1]; L=fam[0]
                if L=="J": out(f"  TEMPER: d10={f} -> {fam} — DM gate -> reroll"); continue
                if L=="D" and not ({"arcane","divine","psionic"}&P["f"]): out(f"  TEMPER: d10={f} -> {fam} — LOGIC: needs spells -> reroll"); continue
                if L=="F" and "summoner" not in P["f"]: out(f"  TEMPER: d10={f} -> {fam} — LOGIC: needs minions -> reroll"); continue
                if L=="B" and not has_el: out(f"  TEMPER: d10={f} -> {fam} — LOGIC: no elemental damage on the piece -> reroll"); continue
                if L=="G" and not has_cc: out(f"  TEMPER: d10={f} -> {fam} — LOGIC: no condition on the piece -> reroll"); continue
                if L in "AH" and not P["weapon"]: out(f"  TEMPER: d10={f} -> {fam} — LOGIC: weapon technique on a non-weapon -> reroll"); continue
                e=die(10); out(f"  TEMPER: d10={f} -> {fam}; entry d10={e} (23{L}-{e})"); temper=f"23{L}-{e}"; break
        aspect=None
        if rar=="Legendary":
            while True:
                a=die(10); tab=ASPECT_TABLES[a-1]; L=tab[0]
                if L=="J" and t>1: out(f"  ASPECT: d10={a} -> {tab} — T1 only -> reroll"); continue
                e=die(6 if L=="J" else 8)
                bad=None
                if L=="D" and not ({"arcane","divine","psionic"}&P["f"]): bad="needs spells"
                if L=="E" and e<=6 and not ({"arcane","divine","psionic"}&P["f"]): bad="reshapes spells"
                if L=="E" and e==7 and not P["weapon"]: bad="Siege needs a weapon"
                if L=="E" and e==8 and not P.get("ranged"): bad="Comet needs a ranged attack"
                if L=="F" and "summoner" not in P["f"]: bad="needs summons"
                if L=="H" and not has_cc: bad="no condition on the piece"
                if L in "AB" and not P["weapon"]: bad="weapon damage on a non-weapon"
                if L=="I" and e==2 and not ({"arcane","divine","psionic"}&P["f"]): bad="Blood Mage needs spells"
                if bad: out(f"  ASPECT: d10={a} -> {tab}; entry {e} — LOGIC: {bad} -> reroll"); continue
                out(f"  ASPECT: d10={a} -> {tab}; entry d{'6' if L=='J' else '8'}={e} (24{L}-{e})"); aspect=f"24{L}-{e}"; break
        tadd=die(4)+1 if temper else 0; aadd=sum(die(3) for _ in range(3))+3 if aspect else 0
        if temper: out(f"  temper UDRP add-on 1d4+1 -> {tadd}")
        if aspect: out(f"  aspect UDRP add-on 3d3+3 -> {aadd}")
        summary[name]=dict(affixes=drawn,greater=greater,temper=temper,aspect=aspect,temper_udrp=tadd,aspect_udrp=aadd)
    json.dump(summary,open("full_corpus_pass.json","w"),indent=1)

if __name__=="__main__": main()
