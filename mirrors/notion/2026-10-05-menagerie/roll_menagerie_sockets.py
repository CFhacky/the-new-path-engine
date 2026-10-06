"""Menagerie socket layer (5 Oct 2026). Every die is a call to loot-engine's loot_roll.py 'roll' mode (Python secrets),
raw stdout captured to menagerie_socket_rolls.txt. Tables: loot-engine affix-families.md Section 9 (count d100, type d100),
Section 25 (gems d7 in printed order, as the Hand precedent), Runeword Crafting System high-rune d10 (levels 13-17).
Gem sockets roll d2 first: 1 = stat gem (Section 25), 2 = spell gem (Reservoir row: stores one spell; T1 7th level, T2 5th).
Signature pieces are masterwork (non-magical), so commissioned sockets are legal (Runeword Crafting System)."""
import subprocess, json, re
LR="/root/.claude/skills/synced/07327e22-ff68-47f1-ad4a-8176d4a886f0_c7d5c9b9-16d6-4e70-9b16-504f3872f1f8/loot-engine/scripts/loot_roll.py"
log=open("menagerie_socket_rolls.txt","w"); res={}
def roll(expr,label):
    o=subprocess.run(["python3",LR,"roll",expr],capture_output=True,text=True).stdout.strip()
    log.write(f"[{label}] {o}\n"); return int(re.findall(r"-?\d+",o.split("=")[-1])[-1]) if "=" in o else int(re.findall(r"\d+",o)[-1])
COUNT=[(1,45,0),(46,75,1),(76,92,2),(93,99,3),(100,100,-1)]
TYPE=[(1,30,"Gem"),(31,50,"Rune"),(51,65,"Seal"),(66,80,"Charm"),(81,92,"Shard"),(93,100,"Strange")]
GEMS=["Ruby","Sapphire","Emerald","Diamond","Topaz","Amethyst","Skull"]
HIGH=["Dol","Hel","Io","Lum","Ko","Fal","Lem","Pul","Um","Mal"]
band=lambda t,r:next(v for a,b,v in t if a<=r<=b)
pieces=[("I Quavein","beak-mace",1),("II Hadda","punch-dagger",1),("III Tarvash","paired scimitars",1),("IV Aerendyl","prayer-cord",1),
 ("V Kesh","mantis-sickles",1),("VI Marit","boning knife",1),("VII Naevys","boar-spear",1),("VIII Brunna","the tucks",1),
 ("IX Mercy","the gaff",1),("X Zaheda","notebook and reed pen (focus)",1),("XI Ysmay","the old sword",1),("XII Ilvaera","manticore darts (the quiver)",1),
 ("XIII Dace","short spear",1),("Lt I Osmund Tarrow","brass censer",2),("Lt II Kerra Lisle","duelling rapier",1),("Lt III Wenna Sorrel","short hatchet",1),
 ("Lt IX Faelith Ammarin","darkwood tower shield",1),("Lt X Patience Haskett","two-headed flail",1),("Lt XI Rhun Talbridge","pollaxe",1),
 ("Lt XII Edwyn Coldry","mail mitten",1),("Lt XIII Ashavel Oriym","iron war-fans",1)]
for who,piece,tier in pieces:
    log.write(f"===== {who} — {piece} (Tier {tier})\n")
    n=band(COUNT,roll("d100",f"{who} socket count"))
    socks=[]
    if n==-1: socks=["unusual socket geometry (DM-authored)"]
    for i in range(max(n,0)):
        t=band(TYPE,roll("d100",f"{who} socket {i+1} type"))
        if t=="Gem":
            k=roll("d2",f"{who} socket {i+1} gem kind (1 stat / 2 spell)")
            if k==1: socks.append(f"Gem: {GEMS[roll('d7',f'{who} socket {i+1} gem d7')-1]}")
            else: socks.append(f"Spell gem (Reservoir T{tier}: one stored spell up to {'7th' if tier==1 else '5th'} level)")
        elif t=="Rune": socks.append(f"Rune: {HIGH[roll('d10',f'{who} socket {i+1} high rune d10')-1]}")
        else: socks.append(f"{t} socket (empty; filled in the item pass)")
    res[who]={"piece":piece,"tier":tier,"sockets":socks}
log.close(); json.dump(res,open("menagerie_sockets.json","w"),indent=1)
for k,v in res.items(): print(k,"|",v["piece"],"|",v["sockets"] or "no sockets")
