"""Menagerie round 3: the two open names (Chad: 'roll the two names'). Python secrets, 3d6, four throws,
lower median, no rerolls. Each name is built from syllable/word tables, one throw per part."""
import secrets, json
def d3(): return sum(secrets.randbelow(6)+1 for _ in range(3))
def throw():
    t=[d3() for _ in range(4)]; return t, sorted(t)[1]
def tab(words): return {s:w for s,w in zip(range(3,19),words)}
T={
 "drow_f_first_a": tab(["Zes","Vel","Ilh","Shi","Mal","Char","Ulvi","Ny","Quil","Bel","Gree","Ard","Ece","Jhael","Vier","SiN"]),
 "drow_f_first_b": tab(["ra","ndra","yrr","ziira","vayas","thra","nolu","dril","viira","lyss","ssra","nzrae","kriiv","bryn","nae","lith"]),
 "drow_house_a":   tab(["Xor","Vrin","Mez","Teken","Hla","Ky","Dyr","Aun","Szol","Ilm","Zau","Rhyl","Oblin","Ghal","Vel","Tor"]),
 "drow_house_b":   tab(["'rret","ndar","'zith","vrae","zaer","'ghal","nnyl","tyrr","xun","'ral","zynt","'vaern","oss","kyn","'quor","laith"]),
 "wd_first":       tab(["Ambrose","Lucan","Osbert","Theron","Cassius","Rowan","Gideon","Aldous","Severin","Jory","Matthias","Corwin","Ellery","Fenwick","Lysander","Peregrine"]),
 "wd_surname":     tab(["Ashgrove","Vantorre","Delcourt","Merriweather","Stallis","Rennick","Brightlance","Holloway","Castellane","Dunmarrow","Ilsworth","Pellucid","Ravenell","Thorncastle","Westerly","Quillon"]),
}
log=[]
def r(i,key):
    t,b=throw(); v=T[key][b]; log.append({"id":i,"throws":t,"bound":b,"result":v}); return v
p=r("Priestess first name, part 1","drow_f_first_a")+r("Priestess first name, part 2","drow_f_first_b")
h=r("Priestess house, part 1","drow_house_a")+r("Priestess house, part 2","drow_house_b")
f=r("Fencing master first name","wd_first"); s=r("Fencing master surname","wd_surname")
json.dump({"method":"Python secrets; 3d6; four throws; lower median; no rerolls.","date":"2026-10-05","tables":{k:v for k,v in T.items()},"throws":log,"results":{"priestess":f"{p} of House {h}","fencing_master":f"{f} {s}"}},open("menagerie_names_rolls.json","w"),indent=1)
for e in log: print(e)
print(p,"of House",h,"|",f,s)
