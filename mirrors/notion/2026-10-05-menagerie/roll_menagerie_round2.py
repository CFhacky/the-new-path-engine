"""Menagerie round 2 (Chad's rulings, 5 Oct 2026). Same method: Python secrets, 3d6, four throws,
bound = lower median (2nd smallest), no rerolls. A rival roll that lands on the captain's own seat slides k+1."""
import secrets, json
def d3(): return sum(secrets.randbelow(6)+1 for _ in range(3))
def throw():
    t=[d3() for _ in range(4)]; return t, sorted(t)[1]
def band(spec,k):
    for lo,hi,v in spec:
        if lo<=k<=hi: return v
T={
 "wizard_school":[(3,5,"divination"),(6,7,"abjuration"),(8,8,"conjuration"),(9,9,"evocation"),(10,10,"transmutation"),(11,11,"enchantment"),(12,12,"necromancy"),(13,13,"illusion"),(14,18,"universalist")],
 "sorcerer_heritage":[(3,7,"draconic"),(8,9,"elemental (fire)"),(10,11,"fey"),(12,13,"celestial"),(14,18,"aberrant")],
 "quavein_second_domain (War fixed; Susanoo's warrior face; Trickery and Death excluded)":[(3,8,"Weather (the storm)"),(9,10,"Water (the sea he was first given)"),(11,12,"Destruction"),(13,18,"Strength")],
 "ysmay_refused_order":[(3,6,"execute a child who witnessed an operation (Silence Protocol)"),(7,8,"leave a wounded operative behind to make the extraction window"),(9,10,"stand down from a kill already begun, because the target had become an asset mid-operation"),(11,12,"kill an old comrade from her life before the Veil"),(13,14,"hand a prisoner to an interrogation she judged butchery"),(15,18,"leave Arik's side during a fight")],
 "recruitment_route (Veil Recruitment Pipeline + extras)":[(3,5,"a Veil target who was turned instead of killed"),(6,7,"Street (Dock Rats)"),(8,8,"Military (discharged soldiers)"),(9,9,"Magical (academy dropouts)"),(10,10,"Noble (disgraced heirs)"),(11,11,"Social (Drift)"),(12,12,"recruited by Lirien personally"),(13,13,"recruited by Virelle Saan in the demon war"),(14,18,"came to Arik and asked")],
 "what_they_want":[(3,6,"a death worth having"),(7,8,"to be the best alive at their art"),(9,10,"a debt repaid, to them or by them"),(11,12,"a place that is theirs"),(13,14,"one named enemy dead"),(15,18,"to see what Arik becomes")],
}
SEAT=[(3,4,1),(5,5,2),(6,6,3),(7,7,4),(8,8,5),(9,9,6),(10,10,7),(11,11,8),(12,12,9),(13,13,10),(14,14,11),(15,16,12),(17,18,13)]
seatmap={k:v for lo,hi,v in SEAT for k in range(lo,hi+1)}
log=[]
def roll(i,spec):
    t,b=throw(); r=band(spec,b); log.append({"id":i,"throws":t,"bound":b,"result":r}); return r
for who in ["Hadda Krell","Kerra Lisle","Wenna Sorrel","Edwyn Coldry"]: roll(f"{who} wizard school",T["wizard_school"])
roll("Naevys Tolurin sorcerer heritage",T["sorcerer_heritage"])
roll("Quavein Orlzynn second domain",T["quavein_second_domain (War fixed; Susanoo's warrior face; Trickery and Death excluded)"])
roll("Ysmay Corran refused order",T["ysmay_refused_order"])
caps=["Quavein","Hadda","Tarvash","Aerendyl","Kesh","Marit","Naevys","Brunna","Mercy","Zaheda","Ysmay","Ilvaera","Dace"]
for s,c in enumerate(caps,1):
    roll(f"Captain {s} {c} recruitment route",T["recruitment_route (Veil Recruitment Pipeline + extras)"])
    roll(f"Captain {s} {c} what they want",T["what_they_want"])
    t,b=throw(); k=b; slid=[]
    while seatmap[k]==s: slid.append(k); k=3 if k==18 else k+1
    e={"id":f"Captain {s} {c} rival captain (seat)","throws":t,"bound":b,"result":f"{seatmap[k]} {caps[seatmap[k]-1]}"}
    if slid: e["slide"]={"occupied_self":slid,"landed":k}
    log.append(e)
json.dump({"method":"Python secrets; 3d6; four throws; lower median; no rerolls. Rival rolls slide off the captain's own seat.","date":"2026-10-05","tables":{k:[list(x) for x in v] for k,v in T.items()} | {"rival_seat":[list(x) for x in SEAT]},"throws":log},open("menagerie_round2_rolls.json","w"),indent=1)
for e in log: print(e["id"],"|",e["throws"],e["bound"],"->",e["result"],e.get("slide",""))
