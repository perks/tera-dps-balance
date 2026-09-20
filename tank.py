import json,os,collections,statistics as st
rows=json.load(open("rows.json")); meta={r["encounterUid"]:r for r in rows}
AREAS={556:"TS Hard",456:"TS Savage",568:"SS Hard",468:"SS Savage",507:"Dragon's Landing"}
TANKS=['Lancer','Brawler','Warrior','Berserker']
DPSC=['Archer','Berserker','Gunner','Ninja','Reaper','Slayer','Sorcerer','Valkyrie','Warrior']
def q(xs,p):
    xs=sorted(xs); k=(len(xs)-1)*p; f=int(k); c=min(f+1,len(xs)-1); return xs[f]+(xs[c]-xs[f])*(k-f)
def stats(xs,pids): return dict(n=len(xs),players=len(set(pids)),min=min(xs),p25=q(xs,.25),med=st.median(xs),avg=st.mean(xs),p75=q(xs,.75),p90=q(xs,.9),max=max(xs))
# buff names to track (encounter-level uptimes)
TRACK={"Guardian Shout":"Lancer","Guardian Power":"Lancer","Adrenaline Rush":"Lancer","Debilitate":"Lancer","Combative Strike":"Warrior","Traverse Cut":"Warrior","Punishing Strike":"Berserker","Berzerker's Lead":"Berserker"}
T=[];D=[];ENC=[];drop=collections.Counter()
for f in os.listdir("enc2"):
    d=json.load(open("enc2/"+f)); m=meta[d["uid"]]
    ps=d["players"]; psize=len(ps)
    tanks=[p for p in ps if p["role"]=="tank" and p["cls"] in TANKS]
    if len(tanks)!=1: drop["tanks!=1"]+=1; continue
    tk=tanks[0]
    if (tk["dps"] or 0)<20000: drop["tank dps<20k"]+=1; continue
    area=AREAS[m["areaId"]]
    dpsp=[p for p in ps if p["role"]=="dps" and p["cls"] in DPSC and (p["dps"] or 0)>=50000]
    hasDpsWarrior=any(p["cls"]=="Warrior" for p in dpsp)
    O=sum(p["dps"] for p in dpsp)
    # encounter-level uptimes
    up={}
    for lst in (d.get("buffUptimes") or [],d.get("debuffUptimes") or []):
        for b in lst:
            n=b.get("name") or ""
            for key in TRACK:
                if n.startswith(key):
                    pct=b.get("percentage")
                    if key=="Berzerker's Lead" and b.get("stacks"):
                        s4=[s for s in b["stacks"] if s.get("stack")==4]; pct4=s4[0]["percentage"] if s4 else 0
                        up[key+" x4"]=max(up.get(key+" x4",0),pct4)
                    if key=="Traverse Cut" and b.get("stacks"):
                        s13=[s for s in b["stacks"] if s.get("stack")>=13]; up[key+" x13"]=max(up.get(key+" x13",0),max([s["percentage"] for s in s13] or [0]))
                    up[key]=max(up.get(key,0),pct or 0)
    # per-DPS-player uptime of tank-sourced party buffs from abnormal intervals
    ABN={"Guardian Power":(200230,200231,200232),"Adrenaline Rush":(200700,200701,201903,201905),"Berzerker's Lead x4":(401405,),"Traverse Cut":(101300,)}
    durms=(d["dur"] or 0)*1000
    pu={}
    if durms>0:
        for key,ids in ABN.items():
            vals=[]
            for p in dpsp:
                iv=[(a[1],a[2]) for a in p["abn"] if a[0] in ids and a[1] is not None and a[2] is not None and (key!="Berzerker's Lead x4" or (a[3] or 0)>=4)]
                iv.sort(); tot=0; cur=None
                for st_,en_ in iv:
                    en_=min(en_,durms); st_=max(st_,0)
                    if en_<=st_: continue
                    if cur and st_<=cur[1]: cur=(cur[0],max(cur[1],en_))
                    else:
                        if cur: tot+=cur[1]-cur[0]
                        cur=(st_,en_)
                if cur: tot+=cur[1]-cur[0]
                vals.append(100*tot/durms)
            if vals: pu[key]=st.mean(vals)
    e=dict(uid=d["uid"],area=area,pu=pu,boss=d["boss"],dur=d["dur"],psize=psize,tank=tk["cls"],tankPid=tk["pid"],tankDps=tk["dps"],O=O,nD=len(dpsp),hasDpsWarrior=hasDpsWarrior,up=up,ts=m["encounterUnixEpoch"])
    ENC.append(e)
    T.append(dict(uid=d["uid"],area=area,boss=d["boss"],cls=tk["cls"],dps=tk["dps"],dur=d["dur"],psize=psize,pid=tk["pid"] or ("anon:"+str(tk["name"])),anon=tk["pid"] is None,
        ts=m["encounterUnixEpoch"],deaths=tk["deaths"],aggro=tk["aggro"],ilvl=tk["ilvl"],wEnch=tk["wEnchant"],brooch=tk["brooch"],hasGear=tk["hasGear"],armor=tuple(tk["armorEnchant"] or [None]*3),O=O))
    for p in dpsp:
        D.append(dict(uid=d["uid"],area=area,boss=d["boss"],cls=p["cls"],dps=p["dps"],dur=d["dur"],psize=psize,pid=p["pid"] or ("anon:"+str(p["name"])+":"+d["uid"]),anon=p["pid"] is None,
            tank=tk["cls"],wEnch=p["wEnchant"],ilvl=p["ilvl"],brooch=p["brooch"],hasDpsWarrior=hasDpsWarrior))
print("encounters",len(ENC),"tank samples",len(T),"dps samples",len(D),"drop",dict(drop))
F=[t for t in T if t["psize"]==5]; FD=[x for x in D if x["psize"]==5]; FE=[e for e in ENC if e["psize"]==5]
areas=list(AREAS.values())
out={"dataset":dict(encounters=len(ENC),five=len(FE),tankSamples=len(F),dpsSamples=len(FD),players=len({t["pid"] for t in T if not t["anon"]}),anon=sum(t["anon"] for t in T),
    dateFrom=min(t["ts"] for t in T),dateTo=max(t["ts"] for t in T),drop=dict(drop),tankMix=dict(collections.Counter(t["cls"] for t in F)))}
# ---------- tank personal DPS ----------
bossmed={k:st.median([t["dps"] for t in F if (t["area"],t["boss"])==k]) for k in {(t["area"],t["boss"]) for t in F}}
for t in T: t["rel"]=t["dps"]/bossmed[(t["area"],t["boss"])]
def relidx(sub,classes=TANKS,minn=3):
    r={}
    for c in classes:
        xs=[s["rel"] for s in sub if s["cls"]==c]
        if len(xs)<minn: continue
        pids={s["pid"] for s in sub if s["cls"]==c}
        best=collections.defaultdict(float)
        for s in sub:
            if s["cls"]==c: best[s["pid"]]=max(best[s["pid"]],s["rel"])
        r[c]=dict(n=len(xs),players=len(pids),avg=st.mean(xs),med=st.median(xs),p90=q(xs,.9),top10=st.mean(sorted(xs)[-max(1,len(xs)//10):]),playerBestMed=st.median(best.values()))
    return r
out["relIndex"]=relidx(F); out["relIndexByArea"]={a:relidx([t for t in F if t["area"]==a]) for a in areas}
def cnt(sub,a,c,b=None): return sum(1 for s in sub if s["area"]==a and s["cls"]==c and (b is None or s["boss"]==b))
out["byArea"]={a:{c:stats([t["dps"] for t in F if t["area"]==a and t["cls"]==c],[t["pid"] for t in F if t["area"]==a and t["cls"]==c]) for c in TANKS if cnt(F,a,c)>=3} for a in areas}
out["byBoss"]={}
for a in areas:
    for b in sorted({t["boss"] for t in F if t["area"]==a}):
        out["byBoss"][a+" / "+b]={c:stats([t["dps"] for t in F if t["area"]==a and t["boss"]==b and t["cls"]==c],[t["pid"] for t in F if t["area"]==a and t["boss"]==b and t["cls"]==c]) for c in TANKS if cnt(F,a,c,b)>=3}
# kill-time
out["killTime"]={}; acc=collections.defaultdict(lambda:[0,0])
for a in areas:
    for b in sorted({t["boss"] for t in F if t["area"]==a}):
        xs=[t for t in F if t["area"]==a and t["boss"]==b]
        cuts=[q([x["dur"] for x in xs],p) for p in (.25,.5,.75)]
        labels=["<="+str(int(cuts[0]))+"s",str(int(cuts[0]))+"-"+str(int(cuts[1]))+"s",str(int(cuts[1]))+"-"+str(int(cuts[2]))+"s",">"+str(int(cuts[2]))+"s"]
        bk=[]
        for bi in range(4):
            bx=[x for x in xs if sum(x["dur"]>c for c in cuts)==bi]
            if not bx: bk.append({}); continue
            med=st.median([x["dps"] for x in bx]); row={}
            for c in TANKS:
                cx=[x["dps"] for x in bx if x["cls"]==c]
                if len(cx)>=3: row[c]=dict(n=len(cx),avg=st.mean(cx),rel=st.mean(cx)/med,max=max(cx)); acc[c][0]+=row[c]["rel"]*len(cx); acc[c][1]+=len(cx)
            bk.append(row)
        out["killTime"][a+" / "+b]=dict(labels=labels,n=len(xs),buckets=bk)
out["killTimeIndex"]={c:dict(rel=v[0]/v[1],n=v[1]) for c,v in acc.items()}
# gear
G=[t for t in F if t["hasGear"] and t["wEnch"] is not None]
TIERS=["<=+5 weapon","+6 weapon","+7 weapon","+8/+9 weapon"]
def tier(s): return TIERS[3] if s["wEnch"]>=8 else TIERS[2] if s["wEnch"]==7 else TIERS[1] if s["wEnch"]==6 else TIERS[0]
out["gear"]={"coverage":dict(withGear=len(G),of=len(F)),"tierEffect":{t:dict(n=len(x),med=st.median([s["rel"] for s in x]) if x else None) for t in TIERS for x in [[s for s in G if tier(s)==t]]}}
out["gear"]["classByTier"]={}
for c in TANKS:
    row={}
    for t in TIERS:
        x=[s["rel"] for s in G if s["cls"]==c and tier(s)==t]
        if len(x)>=3: row[t]=dict(n=len(x),med=st.median(x),avg=st.mean(x))
    il=[(s["ilvl"],s["rel"]) for s in G if s["cls"]==c and s["ilvl"] and 395<=s["ilvl"]<=420]
    row["ilvlSlope"]=None
    if len(il)>=30:
        mx=st.mean(i for i,_ in il); my=st.mean(r for _,r in il); sxx=sum((i-mx)**2 for i,_ in il)
        row["ilvlSlope"]=dict(n=len(il),perIlvl=sum((i-mx)*(r-my) for i,r in il)/sxx if sxx else 0)
    out["gear"]["classByTier"][c]=row
out["gear"]["classGearProfile"]={}
for c in TANKS:
    x=[s for s in G if s["cls"]==c]
    if not x: continue
    il=[s["ilvl"] for s in x if s["ilvl"]]
    out["gear"]["classGearProfile"][c]=dict(n=len(x),avgIlvl=st.mean(il) if il else None,avgWEnch=st.mean([s["wEnch"] for s in x]),pct7plus=sum(s["wEnch"]>=7 for s in x)/len(x),brooch=dict(collections.Counter(s["brooch"] for s in x).most_common(3)))
STD=[s for s in G if s["wEnch"]==6 and s["armor"]==(6,6,6)]
out["gear"]["stdBucket"]=dict(desc="+6 weapon, +6/+6/+6 armor",n=len(STD),classes=relidx(STD),byArea={a:relidx([s for s in STD if s["area"]==a]) for a in areas})
# ---------- buff uptimes by tank class ----------
out["uptimesPlayer"]={}
for c in TANKS:
    es=[e for e in FE if e["tank"]==c]; row={}
    for key in ["Guardian Power","Adrenaline Rush","Berzerker's Lead x4","Traverse Cut"]:
        vals=[e["pu"].get(key,0) for e in es if e["pu"]]
        if len(vals)>=3: row[key]=dict(n=len(vals),seenIn=sum(1 for v in vals if v>0)/len(vals),medAll=st.median(vals),avgAll=st.mean(vals))
    out["uptimesPlayer"][c]=row
out["uptimes"]={}
for c in TANKS:
    es=[e for e in FE if e["tank"]==c]
    row={}
    for key in ["Guardian Shout","Guardian Power","Adrenaline Rush","Debilitate","Combative Strike","Traverse Cut","Traverse Cut x13","Punishing Strike","Berzerker's Lead","Berzerker's Lead x4"]:
        vals=[e["up"].get(key,0) for e in es]
        present=[v for v in vals if v>0]
        if len(present)>=3: row[key]=dict(n=len(es),seenIn=len(present)/len(es),medAll=st.median(vals),medWhenSeen=st.median(present),avgAll=st.mean(vals))
    out["uptimes"][c]=row
# ---------- empirical teammate lift ----------
# index each DPS sample vs same DPS class on same boss
cbmed={k:st.median([x["dps"] for x in FD if (x["cls"],x["area"],x["boss"])==k]) for k in {(x["cls"],x["area"],x["boss"]) for x in FD}}
cbn=collections.Counter((x["cls"],x["area"],x["boss"]) for x in FD)
for x in FD: x["relC"]=x["dps"]/cbmed[(x["cls"],x["area"],x["boss"])]; x["ok"]=cbn[(x["cls"],x["area"],x["boss"])]>=8
FDo=[x for x in FD if x["ok"]]
def lift(sub):
    r={}
    for c in TANKS:
        xs=[x["relC"] for x in sub if x["tank"]==c]
        if len(xs)>=10: r[c]=dict(n=len(xs),avg=st.mean(xs),med=st.median(xs),encounters=len({x["uid"] for x in sub if x["tank"]==c}))
    return r
out["lift"]={"all":lift(FDo),"plus6only":lift([x for x in FDo if x["wEnch"]==6]),"noDpsWarrior":lift([x for x in FDo if not x["hasDpsWarrior"]]),
  "byArea":{a:lift([x for x in FDo if x["area"]==a]) for a in areas},
  "byDpsClass":{c:lift([x for x in FDo if x["cls"]==c]) for c in DPSC}}
# within-player: demean by (player,boss) mean across their runs, only players with >=2 tank classes on that boss
grp=collections.defaultdict(list)
for x in FDo:
    if not x["anon"]: grp[(x["pid"],x["area"],x["boss"])].append(x)
wp=collections.defaultdict(list); npl=set()
for k,xs in grp.items():
    if len({x["tank"] for x in xs})<2: continue
    npl.add(k[0]); m=st.mean(x["relC"] for x in xs)
    for x in xs: wp[x["tank"]].append(x["relC"]-m)
out["liftWithinPlayer"]={c:dict(n=len(v),avgDelta=st.mean(v)) for c,v in wp.items() if len(v)>=10}
out["liftWithinPlayer"]["_players"]=len(npl)
# party O index by tank class (boss-normalized other-party DPS)
Omed={k:st.median([e["O"] for e in FE if (e["area"],e["boss"])==k]) for k in {(e["area"],e["boss"]) for e in FE}}
out["partyO"]={c:dict(n=len(v),avg=st.mean(v),med=st.median(v)) for c in TANKS for v in [[e["O"]/Omed[(e["area"],e["boss"])] for e in FE if e["tank"]==c]] if len(v)>=5}
# ---------- rDPS ----------
# modeled multipliers from the reviewed workbook
M={"floor":{"Brawler":1.0,"Lancer":1.2153,"Warrior":1.0433,"Berserker":1.1},
   "base":{"Brawler":1.0,"Lancer":1.3607,"Warrior":1.1608,"Berserker":1.1871},
   "ceiling":{"Brawler":1.0,"Lancer":1.4231,"Warrior":1.2170,"Berserker":1.2162}}
# empirical multiplier: teammate lift relative to Brawler (all-sample avg)
L=out["lift"]["all"]; base=L["Brawler"]["avg"] if "Brawler" in L else 1.0
M["empirical"]={c:(L[c]["avg"]/base if c in L else None) for c in TANKS}
Lw=out["liftWithinPlayer"]; bw=Lw.get("Brawler",{}).get("avgDelta",0)
M["empiricalWithinPlayer"]={c:(1+(Lw[c]["avgDelta"]-bw) if c in Lw else None) for c in TANKS}
# corrected model: same structure as the reviewed workbook (base elasticities 75%), but with uptimes measured here,
# Traverse Cut treated as self-only (not on teammates), Adrenaline Rush II = +20% AS / +10% dmg (game metadata id 200701)
up=out["uptimesPlayer"]; eu=out["uptimes"]
def med(c,k,src): return (src.get(c,{}).get(k,{}).get("medAll") or 0)/100
gp=med("Lancer","Guardian Power",up); ar=med("Lancer","Adrenaline Rush",up); deb=med("Lancer","Debilitate",eu)
cs=med("Warrior","Combative Strike",eu); lead=med("Berserker","Berzerker's Lead x4",up); pun=med("Berserker","Punishing Strike",eu)
out["modelInputs"]={"Lancer":{"Guardian Power (+30 Power)":dict(model=0.5456,measured=gp),"Adrenaline Rush (+20% AS, +10% dmg)":dict(model=0.29288,measured=ar),"Debilitate (-14% End.)":dict(model=0.99,measured=deb)},
  "Warrior":{"Traverse Cut (+11.7% AS) on teammates":dict(model=0.74,measured=med("Warrior","Traverse Cut",up)),"Combative Strike (-12% End.)":dict(model=1.0,measured=cs)},
  "Berserker":{"Berzerker's Lead x4 (+10 Power) on teammates":dict(model=1.0,measured=lead),"Punishing Strike (-12% End.)":dict(model=0.88,measured=pun)},
  "Brawler":{"(no offensive party utility)":dict(model=0,measured=0)}}
AS_EL=0.75; END_CONV=0.75
M["correctedModel"]={"Brawler":1.0,
  "Lancer":(1+0.30*gp)*(1+0.10*ar)*(1+0.20*ar*AS_EL)*(1+0.14*deb*END_CONV),
  "Warrior":(1+0.12*cs*END_CONV),
  "Berserker":(1+0.10*lead)*(1+0.12*pun*END_CONV)}
out["multipliers"]=M
# standardized rDPS per boss: T + S_boss*(M-1)/M ; index vs Brawler median on same boss; median across bosses with >=3 per class
out["rdps"]={}
bosses=sorted({(t["area"],t["boss"]) for t in F})
for scen,mm in M.items():
    per={c:[] for c in TANKS}; absv={c:[] for c in TANKS}
    for k in bosses:
        S=Omed.get(k)
        if S is None: continue
        meds={}
        for c in TANKS:
            xs=[t["dps"] for t in F if (t["area"],t["boss"])==k and t["cls"]==c]
            if len(xs)>=3 and mm.get(c): meds[c]=st.median(xs)+S*(mm[c]-1)/mm[c]
        if "Brawler" not in meds: continue
        for c,v in meds.items(): per[c].append(100*v/meds["Brawler"]); absv[c].append(v)
    out["rdps"][scen]={c:dict(bosses=len(v),index=st.median(v),indexAvg=st.mean(v),absMed=st.median(absv[c])) for c,v in per.items() if v}
# personal index vs Brawler same way
per={c:[] for c in TANKS}
for k in bosses:
    meds={c:st.median(xs) for c in TANKS for xs in [[t["dps"] for t in F if (t["area"],t["boss"])==k and t["cls"]==c]] if len(xs)>=3}
    if "Brawler" in meds:
        for c,v in meds.items(): per[c].append(100*v/meds["Brawler"])
out["personalVsBrawler"]={c:dict(bosses=len(v),index=st.median(v)) for c,v in per.items() if v}
out["representation"]={c:dict(samples=sum(1 for t in F if t["cls"]==c),players=len({t["pid"] for t in F if t["cls"]==c and not t["anon"]}),medDur=st.median([t["dur"] for t in F if t["cls"]==c]) if any(t["cls"]==c for t in F) else None,deathRate=st.mean([1 if (t["deaths"] or 0)>0 else 0 for t in F if t["cls"]==c]) if any(t["cls"]==c for t in F) else None) for c in TANKS}
json.dump(out,open("tank.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)
print(json.dumps(out["dataset"]))
def show(d,key):
    for c,v in sorted(d.items(),key=lambda kv:-(kv[1].get(key) or 0) if isinstance(kv[1],dict) else 0):
        if isinstance(v,dict): print("  %-10s"%c,{k:(round(v2,3) if isinstance(v2,float) else v2) for k,v2 in v.items()})
print("\nTANK personal relIndex"); show(out["relIndex"],"avg")
print("\nkillTimeIndex"); show(out["killTimeIndex"],"rel")
print("\nuptimes"); [print(" ",c,{k:(round(v["medAll"],1),round(v["seenIn"],2)) for k,v in r.items()}) for c,r in out["uptimes"].items()]
print("\nLIFT all"); show(out["lift"]["all"],"avg")
print("LIFT +6 only"); show(out["lift"]["plus6only"],"avg")
print("LIFT no dps warrior"); show(out["lift"]["noDpsWarrior"],"avg")
print("LIFT within player",out["liftWithinPlayer"])
print("partyO",{c:round(v["avg"],3) for c,v in out["partyO"].items()})
print("\nmultipliers",json.dumps({k:{c:(round(v,3) if v else None) for c,v in m.items()} for k,m in M.items()}))
print("\nrDPS index (Brawler=100)"); [print(" ",s,{c:round(v["index"],1) for c,v in r.items()}) for s,r in out["rdps"].items()]
print("personal vs Brawler",{c:round(v["index"],1) for c,v in out["personalVsBrawler"].items()})
