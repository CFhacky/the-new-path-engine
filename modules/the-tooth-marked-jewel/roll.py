import secrets, json, datetime
def d6(): return secrets.randbelow(6)+1
def throw(): return sum(d6() for _ in range(3))
def lower_median():
    t=[throw() for _ in range(4)]; s=sorted(t); return t, s[1]
rolls=[
 ("TJ-1","Dawn of the vision (day of Uktar 1498 = result)"),
 ("TJ-2","Lorne witnesses: 3-10 Nym alone; 11-18 both, Lorne sees the other figure winning"),
 ("TJ-3","Ichiki Shoun reaction to the Hand landing (GURPS reaction, no modifier): 3-6 Bad, 7-9 Poor, 10-12 Neutral, 13-15 Good, 16-18 Very Good"),
 ("TJ-4","Yakumo-ha awareness stage: 3-6 S1 Anauroch, 7-10 S2 rite-house, 11-14 S3 crossing, 15-18 S5 return"),
 ("TJ-5","Orochi remnant awareness stage: 3-6 S1, 7-10 S2, 11-14 S3, 15-18 S5"),
 ("TJ-6","Talos (Calloway) awareness stage: 3-6 S1, 7-10 S2, 11-14 S4 island, 15-18 S5"),
 ("TJ-7","Amaterasu's court watch begins: 3-6 S1 (the deer at the vision), 7-10 S2, 11-14 S3, 15-18 S4"),
 ("TJ-8","Enma's wardens: first Yashiori kill on Kara-Turan soil -> arrival delay: 3-8 same night, 9-13 next dusk, 14-18 three days"),
]
out=[]
for rid,desc in rolls:
    t,r=lower_median(); out.append({"id":rid,"question":desc,"throws":t,"result":r})
    print(rid, t, "->", r)
json.dump({"method":"Python secrets; 3d6 x4 throws; lower median (2nd lowest); no rerolls","date":"2026-10-05","rolls":out},open("tooth_marked_jewel_rolls.json","w"),indent=1)
