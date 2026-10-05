"""The Menagerie roster rolls, 5 Oct 2026. Python secrets, 3d6, four throws, lower median (2nd smallest), no rerolls.
Uniqueness tables (captain art, emblem, lawless streak, Hand seat): a repeat bound slides to the next unused
entry down the table (k+1, wrapping 18 -> 3). The slide is recorded; it is not a reroll."""
import secrets, json
def d3():
    return sum(secrets.randbelow(6)+1 for _ in range(3))
def throw():
    t=[d3() for _ in range(4)]
    return t, sorted(t)[1]
def band(table, k):
    for (lo,hi),v in table:
        if lo<=k<=hi: return v
    raise ValueError(k)
def rng(spec):  # spec: list of (lo,hi,val)
    return [((a,b),v) for a,b,v in spec]
T = {
 "captain_level": rng([(3,6,15),(7,9,16),(10,12,17),(13,15,18),(16,17,19),(18,18,20)]),
 "lieutenant_level": rng([(3,6,12),(7,10,13),(11,14,14),(15,18,15)]),
 "race": rng([(3,3,"genasi"),(4,4,"goliath"),(5,5,"aasimar"),(6,6,"tiefling"),(7,7,"half-orc"),(8,9,"human"),(10,10,"half-elf"),(11,11,"elf"),(12,12,"dwarf"),(13,13,"drow"),(14,14,"halfling"),(15,18,"gnome")]),
 "sex": rng([(3,9,"male"),(10,18,"female")]),
 "age": rng([(3,7,"young"),(8,10,"prime"),(11,12,"seasoned"),(13,18,"old")]),
 "triangle_tier": rng([(3,11,"Gray"),(12,18,"Dusk")]),
 "captain_suit_tier": rng([(3,6,"none (Veil kit only)"),(7,8,"Strider"),(9,10,"Stalker"),(11,18,"Phantom")]),
 "lt_suit_tier_stalker_ceiling": rng([(3,8,"Strider"),(9,18,"Stalker")]),
 "lt_suit_tier_phantom_ceiling": rng([(3,8,"Strider"),(9,15,"Stalker"),(16,18,"Phantom")]),
 "second_tradition": rng([(3,7,"none (pure Veil austerity)"),(8,9,"Forgedeep dwarven"),(10,11,"Bloodaxe Nordic"),(12,13,"Calishite-Amnian"),(14,18,"Metropolitan urushi")]),
 "budget_band": rng([(3,6,0),(7,10,1),(11,14,2),(15,18,3)]),
}
BUDGET={"Strider":[300,600,1000,1500],"Stalker":[1500,2500,3750,5000],"Phantom":[5000,8000,11500,15000]}
U = {  # uniqueness tables, keyed by exact sum
 "captain_art": {3:"Favored Soul",4:"Hexblade",5:"Warlock",6:"Ranger (archer-skirmisher)",7:"Monk",8:"Rogue / Assassin",9:"Fighter",10:"Wizard",11:"Cleric",12:"Sorcerer",13:"Swordsage",14:"Barbarian",15:"Druid",16:"Warblade",17:"Duskblade",18:"Psychic Warrior"},
 "emblem": {3:"Manticore",4:"Wolverine",5:"Heron",6:"Wolf",7:"Raven",8:"Adder",9:"Hound",10:"Boar",11:"Hawk",12:"Spider",13:"Bear",14:"Mantis",15:"Shrike",16:"Moray",17:"Tiger",18:"Owl"},
 "lawless": {3:"accepts any challenge, from anyone, anywhere",4:"has killed a Veil operative; sanctioned after the fact",5:"sleeps in the enemy's house",6:"settles grudges personally, off the books",7:"kills when told to take alive, if they judge it cleaner",8:"runs a private side-ledger of operations Lirien learns of afterwards",9:"answers to Arik, and only grudgingly to Lirien's staff",10:"recruits without clearance",11:"duels for sport",12:"keeps a trophy from every kill",13:"walks rather than gate-jumps, so the network never logs them",14:"shows their face in the field",15:"keeps a family the Veil does not know about",16:"writes everything down",17:"refused a direct order from Lirien once, and lived",18:"takes work Arik has not asked for, on Arik's behalf"},
}
SEAT = rng([(3,4,1),(5,5,2),(6,6,3),(7,7,4),(8,8,5),(9,9,6),(10,10,7),(11,11,8),(12,12,9),(13,13,10),(14,14,11),(15,16,12),(17,18,13)])
log=[]
def roll(id_, table=None, result_fn=None):
    t,b=throw()
    r = result_fn(b) if result_fn else band(table,b)
    log.append({"id":id_,"throws":t,"bound":b,"result":r}); return r
def roll_unique(id_, utable, used):
    t,b=throw(); k=b; slid=[]
    while utable[k] in used:
        slid.append(k); k = 3 if k==18 else k+1
    used.add(utable[k])
    e={"id":id_,"throws":t,"bound":b,"result":utable[k]}
    if slid: e["slide"]={"occupied":slid,"landed":k}
    log.append(e); return utable[k]
used={"art":set(),"emblem":set(),"lawless":set()}
caps=[]
for i in range(1,14):
    c={"seat":i}
    c["level"]=roll(f"Captain {i} level",T["captain_level"])
    c["art"]=roll_unique(f"Captain {i} art/class",U["captain_art"],used["art"])
    c["race"]=roll(f"Captain {i} race",T["race"])
    c["sex"]=roll(f"Captain {i} sex",T["sex"])
    c["age"]=roll(f"Captain {i} age",T["age"])
    c["emblem"]=roll_unique(f"Captain {i} emblem animal",U["emblem"],used["emblem"])
    c["lawless"]=roll_unique(f"Captain {i} lawless streak",U["lawless"],used["lawless"])
    tier=roll(f"Captain {i} Stride suit tier (ceiling Phantom)",T["captain_suit_tier"])
    c["suit"]=tier
    if tier in BUDGET:
        c["tradition"]=roll(f"Captain {i} second decoration tradition",T["second_tradition"])
        bb=roll(f"Captain {i} decoration budget band ({tier})",T["budget_band"])
        c["budget"]=BUDGET[tier][bb]; log[-1]["result"]=f"band {bb+1}: {c['budget']} Crowns"
    caps.append(c)
# triangles
tri=[]
for j in range(1,19):
    seat=roll(f"Triangle {j} captain seat",SEAT)
    tier=roll(f"Triangle {j} tier",T["triangle_tier"])
    tri.append({"triangle":j,"seat":seat,"tier":tier})
# Hand members to lieutenant seats (unique)
seatmap={k:v for (lo,hi),v in SEAT for k in range(lo,hi+1)}
hand=["Ivrael Quillatar","Nym Esharan","Teodric Halvane","Durgan Emberlode","Lorne Ashby"]
used_seats=set(); hand_seats={}
for h in hand:
    hand_seats[h]=roll_unique(f"Hand lieutenant seat: {h}",seatmap,used_seats)
lts=[]
for s in range(1,14):
    if s in used_seats: continue
    L={"seat":s}
    L["level"]=roll(f"Lieutenant (seat {s}) level",T["lieutenant_level"])
    L["art"]=roll(f"Lieutenant (seat {s}) art/class",None,lambda b:U["captain_art"][b])
    L["race"]=roll(f"Lieutenant (seat {s}) race",T["race"])
    L["sex"]=roll(f"Lieutenant (seat {s}) sex",T["sex"])
    L["age"]=roll(f"Lieutenant (seat {s}) age",T["age"])
    fullbab=L["art"].split(" ")[0] in ("Fighter","Barbarian","Ranger","Warblade","Duskblade","Hexblade","Favored")
    ceil = "phantom" if (L["level"]>=15 or (fullbab and L["level"]>=12)) else "stalker"
    tier=roll(f"Lieutenant (seat {s}) suit tier (ceiling {ceil})",T["lt_suit_tier_phantom_ceiling" if ceil=="phantom" else "lt_suit_tier_stalker_ceiling"])
    L["suit"]=tier
    L["tradition"]=roll(f"Lieutenant (seat {s}) second decoration tradition",T["second_tradition"])
    bb=roll(f"Lieutenant (seat {s}) decoration budget band ({tier})",T["budget_band"])
    L["budget"]=BUDGET[tier][bb]; log[-1]["result"]=f"band {bb+1}: {L['budget']} Crowns"
    lts.append(L)
tables={k:[[a,b,v] for (a,b),v in t] for k,t in T.items()}
tables.update({k:v for k,v in U.items()}); tables["triangle_and_hand_seat"]=[[a,b,v] for (a,b),v in SEAT]; tables["budget_crowns"]=BUDGET
out={"method":"Python secrets; 3d6; four throws; bound = lower median (2nd smallest); no rerolls. Uniqueness tables slide a repeat to the next unused entry (k+1, 18 wraps to 3).","date":"2026-10-05","tables":tables,"throws":log,
     "summary":{"captains":caps,"lieutenants_new":lts,"hand_seats":hand_seats,"triangles":tri}}
json.dump(out,open("menagerie_roster_rolls.json","w"),indent=1)
print(json.dumps(out["summary"],indent=0))
