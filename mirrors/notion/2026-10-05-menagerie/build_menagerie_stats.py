"""Menagerie captains — fused-engine stat arithmetic (5 Oct 2026).
Deterministic: no dice. Derives 3.5e numbers from class/ability/kit data and prints Markdown blocks.
Working rules (flagged on the roster page, Chad to confirm):
 R1 Shadow Jump: Captain's Writ via Nightwind attunement (Su, 80 ft/day, shadow to shadow), not Shadowdancer levels.
 R2 Stride AC: suit AC replaces 10+armor; add pilot's pre-suit Dex mod, deflection, natural armor, class AC bonuses.
    Touch = 10 + effective Dex mod + deflection + class; flat-footed = AC - pre-suit Dex mod.
 R3 Suit attack count: if suit base attacks exceed BAB iteratives, extra attacks are at the lowest iterative bonus.
 R4 Suit Str/Dex/Con bonuses apply to attack, damage, Reflex, Fort, initiative and HP (effective scores).
 R5 Evening's Edge (the gloves) armor bonus does not stack with a suit; the claws are a backup weapon. The gloves hold the
    hands slot, so Dex enhancement is woven into captain's-grade Evening's Edge. Throat slot: periapt of Wisdom OR amulet.
 R6 Signature pieces are masterwork (+1 attack) here; enhancement and affixes go through loot-engine.
 R7 GURPS: attribute = 10 + (pre-item, pre-suit score - 10)//2; Dodge = floor(BS)+3+1(CR)+suit; Parry = skill//2+3+1(CR)+suit.
"""
import json, math
CL={ # HD, BAB, F, R, W
 "cleric":(8,"avg","g","p","g"),"wizard":(4,"p","p","p","g"),"sorcerer":(4,"p","p","p","g"),
 "fighter":(10,"g","g","p","p"),"monk":(8,"avg","g","g","g"),"ranger":(8,"g","g","g","p"),
 "rogue":(6,"avg","p","g","p"),"assassin":(6,"avg","p","g","p"),"swordsage":(8,"avg","p","g","g"),
 "barbarian":(12,"g","g","p","p"),"druid":(8,"avg","g","p","g"),"warblade":(12,"g","g","p","p"),
 "duskblade":(8,"g","g","p","g"),"psychic warrior":(8,"avg","g","p","p")}
SUIT={None:dict(ac=None,ad=0,s=0,d=0,c=0,sv=0,sr=0,dr="—",drm=0,spd=0,atk=0,mins=0),
 "Strider":dict(ac=18,ad=1,s=2,d=3,c=1,sv=1,sr=5,dr="5/magic",drm=2,spd=20,atk=3,mins=14),
 "Stalker":dict(ac=22,ad=2,s=4,d=5,c=2,sv=2,sr=10,dr="7/magic",drm=3,spd=30,atk=4,mins=16),
 "Phantom":dict(ac=25,ad=3,s=5,d=7,c=3,sv=3,sr=12,dr="8/magic",drm=4,spd=40,atk=5,mins=18)}
m=lambda x:(x-10)//2
def bab(k,l): return {"g":l,"avg":3*l//4,"p":l//2}[k]
def sv(k,l): return 2+l//2 if k=="g" else l//3
def ladder(b,bonus,count):
    it=[b-5*i for i in range(4) if b-5*i>0] or [b]
    a=[x+bonus-b+b for x in it]; a=[bonus-(b-x) for x in it]
    while len(a)<count: a.append(a[-1])
    return "/".join(f"+{x}" if x>=0 else str(x) for x in a)
def build(c):
    s=dict(c["base"])
    for k,v in c.get("race",{}).items(): s[k]+=v
    for k,v in c.get("age",{}).items(): s[k]+=v
    for k,v in c.get("bumps",{}).items(): s[k]+=v
    pre_item=dict(s)
    for k,v in c.get("items",{}).items(): s[k]+=v
    pre_suit=dict(s); su=SUIT[c.get("suit")]
    e=dict(s); e["str"]=max(s["str"]+su["s"],su["mins"]) if c.get("suit") else s["str"]; e["dex"]+=su["d"]; e["con"]+=su["c"]
    B=F=R=W=0; hp=0; first=True; lvl=0
    for cn,l in c["classes"]:
        hd,bk,fk,rk,wk=CL[cn]; B+=bab(bk,l); F+=sv(fk,l); R+=sv(rk,l); W+=sv(wk,l)
        for i in range(l):
            hp+= hd if first else hd/2+0.5; first=False
        lvl+=l
    hp=int(hp)+m(e["con"])*lvl
    cloak=4; defl=3; nat=0 if (c.get('items',{}).get('con') or c.get('items',{}).get('wis')) else 2
    F+=m(e["con"])+cloak+su["sv"]; R+=m(e["dex"])+cloak+su["sv"]; W+=m(e[c.get("wis_stat","wis")])+cloak+su["sv"]
    cls_ac=c.get("class_ac",0)
    if c.get("suit") and not c.get("suit_as_clothing"):
        ac=su["ac"]+m(pre_suit["dex"])+defl+nat+cls_ac
    else:
        ac=10+c.get("armor",0)+m(e["dex"])+defl+nat+cls_ac
    touch=10+m(e["dex"])+defl+cls_ac
    flat=ac-m(pre_suit["dex"]) if not c.get("uncanny") else ac
    init=m(e["dex"])+c.get("init_extra",4)
    spd=c.get("speed",30)+su["spd"]+c.get("speed_extra",0)
    return dict(s=pre_suit,pi=pre_item,e=e,B=B,F=F,R=R,W=W,hp=hp,ac=ac,touch=touch,flat=flat,init=init,spd=spd,su=su,lvl=lvl)
def gurps(c,d):
    pi=d["pi"]; g=lambda k:10+(pi[k]-10)//2
    ST,DX,IQ,HT=g("str"),g("dex"),g("int"),g("con"); bs=(DX+HT)/4
    will=max(IQ,g(c.get("wis_stat","wis"))); per=max(IQ,g("wis"))
    skill=DX+c["g_skill_bonus"]; ad=d["su"]["ad"]
    dodge=math.floor(bs)+3+1+ad; parry=skill//2+3+1+ad+c.get("parry_adj",0)
    return ST,DX,IQ,HT,will,per,bs,math.floor(bs),dodge,parry,skill
caps=json.load(open("menagerie_captains_data.json"))
out=[]
for c in caps:
    d=build(c); ST,DX,IQ,HT,will,per,bs,mv,dodge,parry,skill=gurps(c,d); su=d["su"]
    S=d["e"]; ab=lambda k:f"{k.upper()} {S[k]}"
    presuit=", ".join(k.upper()+" "+str(d["s"][k]) for k in ["str","dex","con"])
    sr=max(su["sr"],c.get("sr_other",0))
    lines=[f"#### {c['div']} — {c['name']}",
     f"**{c['class_line']}; Level {d['lvl']}; CR {d['lvl']}.** {c['suit_line']}",
     f"**HP {d['hp']}; AC {d['ac']}, touch {d['touch']}, flat-footed {d['flat']}; Initiative +{d['init']}; Speed {d['spd']} ft.**{(' '+c['speed_note']) if c.get('speed_note') else ''}",
     f"**{', '.join(ab(k) for k in ['str','dex','con','int','wis','cha'])}** (effective, suit and items included; pre-suit {presuit}).",
     f"**BAB +{d['B']}; Fort +{d['F']}, Ref +{d['R']}, Will +{d['W']}.** {c.get('save_note','')}".rstrip(),
     f"**DR {su['dr'] if c.get('suit') else c.get('dr_line','—')}{('; '+c['dr_extra']) if c.get('dr_extra') else ''}; magical DR {su['drm']}; SR {sr}.**" if c.get('suit') else f"**DR {c.get('dr_line','—')}; SR {sr if sr else '—'}.**",
     f"**Fused active defenses:** Dodge {dodge}; Parry {parry}{(' ('+c['parry_note']+')') if c.get('parry_note') else ''}.",
     "**Attacks** (full-attack count {}):".format(max(su['atk'],len(ladder(d['B'],0,0).split('/'))) if c.get('suit') else len(ladder(d['B'],0,0).split('/')))]
    cnt=su["atk"] if c.get("suit") else 0
    for a in c["attacks"]:
        st=S[a["stat"]]; bon=d["B"]+m(st)+a.get("mod",0)
        dm=a.get("dstat","str"); dmod=int(m(S[dm])*a.get("dmult",1))+a.get("dbonus",0)
        lad=a.get("ladder") or (ladder(d["B"],bon,cnt) if a.get("full",True) else f"+{bon}")
        dmg=a.get("text_dmg") or (a['dice']+('+'+str(dmod) if dmod>0 else ''))
        lines.append(f"- *{a['name']}* {lad}, {dmg}{(', '+a['note']) if a.get('note') else ''}")
    for k in ["features","casting","feats","skills","kit","tactics"]:
        if c.get(k): lines.append(f"**{k.capitalize()}.** {c[k]}")
    lines.append(f"**GURPS 4e (≈{30*d['lvl']} CP, campaign scale, not itemised).** ST {ST}; DX {DX}; IQ {IQ}; HT {HT}. HP {ST+c.get('g_hp',0)}; Will {will+c.get('g_will',0)}; Per {per+c.get('g_per',0)}; FP {HT}. Basic Speed {bs:.2f}; Move {mv} ({mv+su['spd']//10 if c.get('suit') else mv} suited); Dodge {dodge}; Parry {parry}.")
    lines.append(f"Advantages: {c['g_adv']}. Key skills: {c['g_skill_name']}-{skill}, {c['g_skills']}. Disadvantages: {c['g_dis']}.")
    out.append("\n".join(lines))
open("captains_statblocks.md","w").write("\n\n".join(out)+"\n")
print("\n\n".join(out))
