import json,os,re,collections,statistics as st,random
random.seed(7)
AREAS={556:"TS Hard",456:"TS Savage",568:"SS Hard",468:"SS Savage",507:"Dragon's Landing"}
ORDER=["Dragon's Landing","SS Hard","TS Hard","SS Savage","TS Savage"]
ACC=["necklace","earring-left","earring-right","ring-left","ring-right","belt","brooch"]
JS=["necklace","earring-left","earring-right","ring-left","ring-right"]
PAT=[(r"Increases Power by ([\d.]+)","Power"),(r"Increases Crit Factor by ([\d.]+)","Crit Factor"),
     (r"Increase[s]? Crit Power by ([\d.]+)%","Crit Power"),(r"Increases Attack Speed by ([\d.]+)%","Attack Speed"),
     (r"Increases Endurance by ([\d.]+)","Endurance"),(r"Increases Crit Resist Factor by ([\d.]+)","Crit Resist"),
     (r"Raises max HP by ([\d.]+)%","Max HP %"),(r"Raises max HP by ([\d.]+)","Max HP"),
     (r"Increases your healing skills by ([\d.]+)%","Healing"),(r"Increases your healing skills by ([\d.]+)","Healing"),
     (r"Decreases skill cooldowns by ([\d.]+)%","Cooldown"),(r"Increases damage by ([\d.]+)% when attacking enraged","Dmg vs enraged"),
     (r"Increases damage by ([\d.]+)% when attacking from behind","Dmg from behind"),
     (r"Increases damage by ([\d.]+)% when attacking knocked-down","Dmg vs knocked-down"),
     (r"Increases damage by ([\d.]+)%\.","Flat damage"),(r"Increases damage of ([A-Za-z' ]+) by ([\d.]+)%","Skill damage"),
     (r"Increases ([A-Za-z' ]+) skill damage by ([\d.]+)%","Skill damage"),
     (r"Replenishes ([\d.]+)% of total MP","MP regen"),(r"Recovers ([\d.]+)% of total HP","HP regen"),
     (r"Increases Movement Speed by ([\d.]+)%","Move Speed"),(r"Increases Balance Factor by ([\d.]+)","Balance")]
def parse(t):
    for p,l in PAT:
        if re.search(p,t or ""): return l
    return "Other"
def fam(n):
    if not n: return None
    for k in ("Monarch","Titan","Chrono","Kumasylum","Crimson"):
        if k in n: return k
    return "Other"
# ---------- load every parse ----------
R=[]
for f in os.listdir("slayer"):
    d=json.load(open("slayer/"+f))
    for s in d["slayers"]:
        if (s["dps"] or 0)<50000 or not s["pid"]: continue
        eq=s["equipment"] or {}; stats=s["stats"] or {}
        w=eq.get("weapon") or {}
        rolls=collections.Counter(); slotRoll={}; cry={}
        for slot in ACC:
            it=eq.get(slot)
            if not it: continue
            slotRoll[slot]=tuple(sorted(parse(t) for t in (it["rolls"] or [])))
            cry[slot]=tuple(sorted(it.get("crystals") or []))
            for t in (it["rolls"] or []): rolls[parse(t)]+=1
        for slot2 in ("weapon","chest","gloves","boots"):
            it2=eq.get(slot2)
            if it2 and it2.get("crystals"): cry[slot2]=tuple(sorted(it2["crystals"]))
        NROLL={"weapon":4,"chest":4,"gloves":3,"boots":3}
        armor={}
        for slot2,k2 in NROLL.items():
            it2=eq.get(slot2)
            if it2 and (it2.get("rolls") or []): armor[slot2]=tuple(it2["rolls"][:k2])
        js=[fam((eq.get(s2) or {}).get("name")) for s2 in JS]
        R.append(dict(uid=d["uid"],area=AREAS.get(d["area"]),boss=d["boss"],dur=d["dur"],dps=s["dps"],pid=s["pid"],name=s["name"],
            crit=s["crit"],deaths=s["deaths"],dmgpct=s["dmgpct"],
            ilvl=stats.get("itemLevel"),power=stats.get("powerBonus"),critFactor=stats.get("critFactorBonus"),
            attack=stats.get("attackMaxBonus"),attackSpeed=stats.get("attackSpeedBonus"),
            wName=w.get("name"),wEnch=w.get("enchant"),wCrystals=tuple(sorted(w.get("crystals") or [])),
            wRolls=tuple(sorted({parse(t) for t in (w.get("rolls") or [])})),
            nTitan=sum(1 for x in js if x=="Titan"),nMonarch=sum(1 for x in js if x=="Monarch"),nJewel=sum(1 for x in js if x),
            brooch=(eq.get("brooch") or {}).get("name"),belt=(eq.get("belt") or {}).get("name"),
            slotRoll=slotRoll,rolls=dict(rolls),cry=cry,armor=armor,
            glyphs=tuple(sorted({g["name"] for g in s["glyphs"] if g["enabled"]})),hasGlyphs=bool(s["glyphs"]),
            skills=s["skills"],cpm=60*sum(x["hits"] or 0 for x in s["skills"])/max(1,d["dur"]) if s["skills"] else None,
            hasGear=bool(eq)))
# ---------- per-boss top-25 shortlist (best parse per player) ----------
by=collections.defaultdict(list)
for r in R: by[(r["area"],r["boss"])].append(r)
SL=[]; boards=[]
for k,xs in sorted(by.items(),key=lambda kv:(ORDER.index(kv[0][0]) if kv[0][0] in ORDER else 9,-len(kv[1]))):
    best={}
    for r in xs:
        if r["pid"] not in best or r["dps"]>best[r["pid"]]["dps"]: best[r["pid"]]=r
    sl=sorted(best.values(),key=lambda r:-r["dps"])[:25]
    for i,r in enumerate(sl,1):
        r2=dict(r); r2["rank"]=i; r2["board"]=f"{k[0]} / {k[1]}"; r2["nBoard"]=len(sl); r2["pctile"]=(i-1)/max(1,len(sl)-1)
        SL.append(r2)
    boards.append(dict(area=k[0],boss=k[1],parses=len(xs),players=len(best),shortlist=len(sl),
        top=sl[0]["dps"],bottom=sl[-1]["dps"],med=st.median(r["dps"] for r in sl),
        rows=[dict(rank=i,name=r["name"],pid=r["pid"],dps=r["dps"],dur=r["dur"],crit=r["crit"],cpm=r["cpm"],ilvl=r["ilvl"],
                   jewel=(f"{r['nMonarch']}M/{r['nTitan']}T" if r["nJewel"] else None),brooch=r["brooch"],
                   wEnch=r["wEnch"],glyphs=len(r["glyphs"])) for i,r in enumerate(sl,1)]))
out={"dataset":dict(allParses=len(R),shortlistParses=len(SL),players=len({r["pid"] for r in SL}),
    boards=len(boards),withGear=sum(r["hasGear"] for r in SL),withGlyphs=sum(r["hasGlyphs"] for r in SL),
    ilvlLo=min([r["ilvl"] for r in SL if r["ilvl"]]),ilvlHi=max([r["ilvl"] for r in SL if r["ilvl"]]),
    ilvlMed=st.median([r["ilvl"] for r in SL if r["ilvl"]])),"boards":boards}
# ---------- what the shortlist runs ----------
def share(rows,key):
    c=collections.Counter(r[key] for r in rows if r.get(key) is not None)
    n=sum(c.values())
    return [dict(value=k,n=v,share=v/n) for k,v in c.most_common()]
G=[r for r in SL if r["hasGear"]]
out["runs"]={
 "jewelry":[dict(value=f"{5-t} Monarch / {t} Titan",n=v,share=v/sum(1 for r in G if r["nJewel"]==5))
            for t,v in sorted(collections.Counter(r["nTitan"] for r in G if r["nJewel"]==5).items())],
 "brooch":share(G,"brooch"),"belt":share(G,"belt"),"weapon":share(G,"wName"),"wEnch":share(G,"wEnch"),
 "crystals":[dict(value=" + ".join(x.replace("Fine ","") for x in k),n=v,share=v/max(1,sum(1 for r in G if r["wCrystals"])))
             for k,v in collections.Counter(r["wCrystals"] for r in G if r["wCrystals"]).most_common(5)],
 "wRolls":[dict(value=k,n=v,share=v/len(G)) for k,v in collections.Counter(x for r in G for x in r["wRolls"]).most_common(8)],
}
out["slotRolls"]={}
for slot in ACC:
    c=collections.Counter(r["slotRoll"].get(slot) for r in G if r["slotRoll"].get(slot))
    n=sum(c.values())
    out["slotRolls"][slot]=[dict(value=" + ".join(k) if k else "(none)",n=v,share=v/n) for k,v in c.most_common(5)]
# crystals by slot
out["crystals"]={}
for slot,label in [("weapon","Weapon"),("chest","Chest armor"),("ring-left","Ring (left)"),("ring-right","Ring (right)"),("earring-left","Earring (left)"),("earring-right","Earring (right)")]:
    c=collections.Counter(r["cry"].get(slot) for r in G if r["cry"].get(slot))
    n=sum(c.values())
    if not n: continue
    out["crystals"][label]=dict(n=n,sets=[dict(value=" + ".join(x.replace("Fine ","") for x in k),n=v,share=v/n) for k,v in c.most_common(4)],
        singles=[dict(value=k.replace("Fine ",""),n=v,share=v/n) for k,v in collections.Counter(x for r in G if r["cry"].get(slot) for x in r["cry"][slot]).most_common(6)])
# weapon / armor rolled lines (the actual rolls, masterwork ladder excluded)
def short(t):
    t=re.sub(r"\.$","",t or "")
    t=t.replace("Increases damage by","+").replace("Increases ","+").replace("Decreases ","-").replace("Recovers ","+").replace("Replenishes ","+")
    t=t.replace(" when attacking"," vs").replace("enraged monsters","enraged").replace("knocked-down targets","knocked down")
    t=t.replace("damage of ","").replace(" skill damage by"," dmg").replace(" by "," ").replace("damage taken","dmg taken")
    return t.strip()
out["gearRolls"]={}
for slot,label,k in [("weapon","Weapon",4),("chest","Chest",4),("gloves","Gloves",3),("boots","Boots",3)]:
    rows=[r for r in G if r["armor"].get(slot)]
    if not rows: continue
    lines=collections.Counter(x for r in rows for x in r["armor"][slot])
    combos=collections.Counter(tuple(sorted(r["armor"][slot])) for r in rows)
    out["gearRolls"][label]=dict(n=len(rows),slots=k,
        lines=[dict(value=short(t),raw=t,n=v,share=sum(1 for r in rows if t in r["armor"][slot])/len(rows),
                    avg=v/len(rows),dbl=sum(1 for r in rows if r["armor"][slot].count(t)>1)/len(rows)) for t,v in lines.most_common(8)],
        combos=[dict(value=[short(x) for x in c],n=v,share=v/len(rows)) for c,v in combos.most_common(3)])
out["rollTypes"]=[dict(value=k,players=sum(1 for r in G if r["rolls"].get(k)),share=sum(1 for r in G if r["rolls"].get(k))/len(G),
                       avgCount=st.mean(r["rolls"].get(k,0) for r in G)) for k,_ in collections.Counter(x for r in G for x in r["rolls"]).most_common(10)]
# ---------- what separates the very top from the rest of the shortlist ----------
def half(rows,lo,hi): return [r for r in rows if lo<=r["pctile"]<=hi]
def prof(rows):
    sk=collections.defaultdict(list)
    for r in rows:
        tot=sum(float(x["dmg"] or 0) for x in r["skills"]) or 1
        for x in r["skills"]:
            sk[x["name"] or "(unnamed)"].append(dict(cpm=60*(x["hits"] or 0)/max(1,r["dur"]),share=100*float(x["dmg"] or 0)/tot,
                crit=100*(x["crits"] or 0)/max(1,x["hits"] or 1)))
    return dict(n=len(rows),players=len({r["pid"] for r in rows}),
        dps=st.median(r["dps"] for r in rows),cpm=st.median([r["cpm"] for r in rows if r["cpm"]]),
        crit=st.median([r["crit"] for r in rows if r["crit"] is not None]),
        ilvl=st.median([r["ilvl"] for r in rows if r["ilvl"]]) if any(r["ilvl"] for r in rows) else None,
        power=st.median([r["power"] for r in rows if r["power"]]) if any(r["power"] for r in rows) else None,
        critFactor=st.median([r["critFactor"] for r in rows if r["critFactor"]]) if any(r["critFactor"] for r in rows) else None,
        attack=st.median([r["attack"] for r in rows if r["attack"]]) if any(r["attack"] for r in rows) else None,
        titan=st.mean(r["nTitan"] for r in rows if r["nJewel"]==5) if any(r["nJewel"]==5 for r in rows) else None,
        dur=st.median(r["dur"] for r in rows),
        skills={k:dict(cpm=st.median(x["cpm"] for x in v),share=st.median(x["share"] for x in v),crit=st.median(x["crit"] for x in v),n=len(v))
                for k,v in sk.items() if len(v)>=max(3,len(rows)//4)})
DL=[r for r in SL if r["board"].startswith("Dragon")]
out["split"]={"board":"Dragon's Landing / Calamity Helghan","n":len(DL),
    "top":prof(half(DL,0,0.34)),"mid":prof(half(DL,0.34,0.67)),"bottom":prof(half(DL,0.67,1.0))}
out["splitAll"]={"top":prof([r for r in SL if r["pctile"]<=0.34]),"rest":prof([r for r in SL if r["pctile"]>0.34])}
# gear differences top vs rest of shortlist
def gearmix(rows):
    rows=[r for r in rows if r["hasGear"]]
    return dict(n=len(rows),
        titanAvg=st.mean(r["nTitan"] for r in rows if r["nJewel"]==5) if any(r["nJewel"]==5 for r in rows) else None,
        chrono=sum(1 for r in rows if r["brooch"]=="Chrono Brooch")/max(1,len(rows)),
        stdCrystal=sum(1 for r in rows if set(x.replace("Fine ","") for x in r["wCrystals"])=={"Bitter Niveot","Focused Niveot","Pounding Niveot","Savage Niveot"})/max(1,len(rows)),
        w7=sum(1 for r in rows if (r["wEnch"] or 0)>=7)/max(1,len(rows)),
        enraged=sum(1 for r in rows if "Dmg vs enraged" in r["wRolls"])/max(1,len(rows)),
        behind=sum(1 for r in rows if "Dmg from behind" in r["wRolls"])/max(1,len(rows)),
        ilvl=st.median([r["ilvl"] for r in rows if r["ilvl"]]) if any(r["ilvl"] for r in rows) else None,
        offRolls=st.mean(sum(r["rolls"].get(l,0) for l in ("Power","Crit Factor","Crit Power","Attack Speed")) for r in rows))
out["gearSplit"]={"Top third of every shortlist":gearmix([r for r in SL if r["pctile"]<=0.34]),
                  "Rest of the shortlist":gearmix([r for r in SL if r["pctile"]>0.34])}
# ---------- glyphs among the shortlist ----------
GL=[r for r in SL if r["hasGlyphs"] and len(r["glyphs"])>=6]
gc=collections.Counter()
for r in GL: gc.update(r["glyphs"])
topG=[r for r in GL if r["pctile"]<=0.34]; restG=[r for r in GL if r["pctile"]>0.34]
out["glyphs"]={"n":len(GL),"nTop":len(topG),"nRest":len(restG),"list":[
  dict(name=g,share=c/len(GL),top=sum(1 for r in topG if g in r["glyphs"])/max(1,len(topG)),
       rest=sum(1 for r in restG if g in r["glyphs"])/max(1,len(restG)))
  for g,c in gc.most_common() if c>=3]}
# ---------- rotation reference ----------
allsk=collections.defaultdict(list)
for r in SL:
    tot=sum(float(x["dmg"] or 0) for x in r["skills"]) or 1
    for x in r["skills"]:
        allsk[x["name"] or "(unnamed)"].append(dict(cpm=60*(x["hits"] or 0)/max(1,r["dur"]),share=100*float(x["dmg"] or 0)/tot,
            crit=100*(x["crits"] or 0)/max(1,x["hits"] or 1)))
out["rotation"]=[dict(name=k,n=len(v),share=st.median(x["share"] for x in v),cpm=st.median(x["cpm"] for x in v),crit=st.median(x["crit"] for x in v))
                 for k,v in sorted(allsk.items(),key=lambda kv:-st.median(x["share"] for x in kv[1])) if len(v)>=10]
# ---------- glyph catalogue: icons, skill grouping ----------
try: cat=json.load(open("glyph_catalogue.json",encoding="utf-8"))
except Exception: cat={}
meta={}
try: BASE=json.load(open("slayer_skills.json",encoding="utf-8"))
except Exception: BASE=[]
try: SICON=json.load(open("slayer_skill_icons.json",encoding="utf-8"))
except Exception: SICON={}
def skill_of(name,api):
    for b in BASE:
        if name==b or name.endswith(" "+b): return b
    parts=(name or "").split()
    if len(parts)>=2: return " ".join(parts[1:])
    return api
for gid,v in cat.items():
    n=v.get("name")
    if not n: continue
    cur=meta.get(n)
    if not cur or (v.get("points") or 0)>(cur.get("points") or 0):
        sk2=skill_of(n,v.get("skill"))
        meta[n]=dict(skill=sk2,points=v.get("points"),
            icon=("icons/"+v["icon"].split("/")[-1].lower()) if v.get("icon") else None,
            skillIcon=("icons/"+SICON[sk2].split("/")[-1].lower()) if sk2 in SICON else (("icons/"+v["skillIcon"].split("/")[-1].lower()) if (v.get("skillIcon") and v.get("skill")==sk2) else None),
            desc=re.sub(r"<[^>]+>","",v.get("desc") or "").replace("$BR"," ").strip(),
            skillOrder=v.get("skillOrder") or 0,glyphOrder=v.get("glyphOrder") or 0)
for g in out["glyphs"]["list"]: g.update(meta.get(g["name"],{}))
# group glyphs by skill, ordered by that skill's damage share
dmgshare={r["name"]:r["share"] for r in out["rotation"]}
groups=collections.defaultdict(list)
for g in out["glyphs"]["list"]: groups[g.get("skill") or "Other"].append(g)
out["glyphsBySkill"]=[dict(skill=k,icon=(v[0].get("skillIcon")),share=dmgshare.get(k),
    glyphs=sorted(v,key=lambda g:-g["share"]))
    for k,v in sorted(groups.items(),key=lambda kv:(-(dmgshare.get(kv[0]) or 0),-max(g["share"] for g in kv[1])))]
json.dump(out,open("slayer2.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)
print(json.dumps(out["dataset"],ensure_ascii=False))
print("\nboards:"); [print(f"  {b['area']+' / '+b['boss'][:24]:40} shortlist {b['shortlist']:2} of {b['players']:3} players · {b['bottom']/1000:.0f}k-{b['top']/1000:.0f}k") for b in out["boards"]]
print("\nruns jewelry:",[(x['value'],x['n'],round(x['share'],2)) for x in out['runs']['jewelry']])
print("brooch:",[(x['value'],round(x['share'],2)) for x in out['runs']['brooch'][:3]])
print("crystals:",[(x['value'][:46],round(x['share'],2)) for x in out['runs']['crystals'][:3]])
print("wEnch:",[(x['value'],round(x['share'],2)) for x in out['runs']['wEnch']])
print("belt:",[(x['value'],round(x['share'],2)) for x in out['runs']['belt'][:2]])
print("\nDL split:")
for k in ("top","mid","bottom"):
    p=out["split"][k]; print(f"  {k:7} n{p['n']:3} dps {p['dps']/1000:.0f}k cpm {p['cpm']:.1f} crit {p['crit']:.1f} ilvl {p['ilvl']} power {p['power']} cf {p['critFactor']} atk {p['attack']} titan {p['titan'] and round(p['titan'],2)} dur {p['dur']:.0f}")
print("\ngear split:"); [print("  ",k,{k2:(round(v2,2) if isinstance(v2,float) else v2) for k2,v2 in v.items()}) for k,v in out["gearSplit"].items()]
print("\nglyphs (n=%d, top=%d, rest=%d):"%(out["glyphs"]["n"],out["glyphs"]["nTop"],out["glyphs"]["nRest"]))
for g in out["glyphs"]["list"][:20]: print(f"  {g['name']:34} all {g['share']:.2f} top {g['top']:.2f} rest {g['rest']:.2f} gap {g['top']-g['rest']:+.2f}")
print("\nrotation:"); [print(f"  {r['name']:20} share {r['share']:5.1f}% cpm {r['cpm']:5.1f} crit {r['crit']:5.1f}%") for r in out["rotation"]]
