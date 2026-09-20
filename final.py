import json,os,collections,statistics as st
rows=json.load(open("rows.json"))
meta={r["encounterUid"]:r for r in rows}
AREAS={556:"TS Hard",456:"TS Savage",568:"SS Hard",468:"SS Savage",507:"Dragon's Landing"}
CLS=['Archer','Berserker','Gunner','Ninja','Reaper','Slayer','Sorcerer','Valkyrie','Warrior']
S=[]; drop=collections.Counter()
for f in os.listdir("enc"):
    d=json.load(open("enc/"+f)); m=meta[d["uid"]]
    psize=len(d["players"])
    seen=set()
    for p in d["players"]:
        if p["cls"] not in CLS: continue
        if p["role"]!="dps": drop["role="+str(p["role"])]+=1; continue
        if (p["dps"] or 0)<50000: drop["dps<50k"]+=1; continue
        k=(p["name"],p["cls"])
        if k in seen: drop["dup"]+=1; continue
        seen.add(k)
        wr=p["wRolls"] or []
        S.append(dict(uid=d["uid"],area=AREAS[m["areaId"]],boss=d["boss"],cls=p["cls"],dps=p["dps"],dur=d["dur"],psize=psize,
            pid=p["pid"] or ("anon:"+str(p["name"])),anon=p["pid"] is None,ts=m["encounterUnixEpoch"],crit=p["crit"],deaths=p["deaths"],
            ilvl=p["ilvl"],wEnch=p["wEnchant"],brooch=p["brooch"],hasGear=p["hasGear"],
            enr=sum(1 for r in wr if "enraged" in r),flat=sum(1 for r in wr if r.startswith("Increases damage by 6.0%")),
            behind=sum(1 for r in wr if "from behind" in r),armor=tuple(p["armorEnchant"].values())))
print("samples",len(S),"drop",dict(drop))
def q(xs,p):
    xs=sorted(xs); k=(len(xs)-1)*p; f=int(k); c=min(f+1,len(xs)-1); return xs[f]+(xs[c]-xs[f])*(k-f)
def stats(xs,pids): return dict(n=len(xs),players=len(set(pids)),min=min(xs),p25=q(xs,.25),med=st.median(xs),avg=st.mean(xs),p75=q(xs,.75),p90=q(xs,.9),max=max(xs))
F=[s for s in S if s["psize"]==5]
out={"dataset":dict(samples=len(S),five=len(F),encounters=len({s["uid"] for s in S}),players=len({s["pid"] for s in S if not s["anon"]}),
    anon=sum(s["anon"] for s in S),dateFrom=min(s["ts"] for s in S),dateTo=max(s["ts"] for s in S),drop=dict(drop))}
areas=list(AREAS.values())
bossmed={k:st.median([s["dps"] for s in F if (s["area"],s["boss"])==k]) for k in {(s["area"],s["boss"]) for s in F}}
for s in S: s["rel"]=s["dps"]/bossmed[(s["area"],s["boss"])]
def cnt(sub,a,c,b=None): return sum(1 for s in sub if s["area"]==a and s["cls"]==c and (b is None or s["boss"]==b))
out["byArea"]={a:{c:stats([s["dps"] for s in F if s["area"]==a and s["cls"]==c],[s["pid"] for s in F if s["area"]==a and s["cls"]==c]) for c in CLS if cnt(F,a,c)>=3} for a in areas}
out["byBoss"]={}
for a in areas:
    for b in sorted({s["boss"] for s in F if s["area"]==a}):
        out["byBoss"][a+" / "+b]={c:stats([s["dps"] for s in F if s["area"]==a and s["boss"]==b and s["cls"]==c],[s["pid"] for s in F if s["area"]==a and s["boss"]==b and s["cls"]==c]) for c in CLS if cnt(F,a,c,b)>=3}
def relidx(sub):
    r={}
    for c in CLS:
        xs=[s["rel"] for s in sub if s["cls"]==c]
        if len(xs)<3: continue
        pids={s["pid"] for s in sub if s["cls"]==c}
        best=collections.defaultdict(float)
        for s in sub:
            if s["cls"]==c: best[s["pid"]]=max(best[s["pid"]],s["rel"])
        r[c]=dict(n=len(xs),players=len(pids),avg=st.mean(xs),med=st.median(xs),p90=q(xs,.9),top10=st.mean(sorted(xs)[-max(1,len(xs)//10):]),playerBestMed=st.median(best.values()))
    return r
out["relIndex"]=relidx(F)
out["relIndexByArea"]={a:relidx([s for s in F if s["area"]==a]) for a in areas}
out["killTime"]={}; acc=collections.defaultdict(lambda:[0,0])
for a in areas:
    for b in sorted({s["boss"] for s in F if s["area"]==a}):
        xs=[s for s in F if s["area"]==a and s["boss"]==b]
        cuts=[q([x["dur"] for x in xs],p) for p in (.25,.5,.75)]
        labels=["<="+str(int(cuts[0]))+"s",str(int(cuts[0]))+"-"+str(int(cuts[1]))+"s",str(int(cuts[1]))+"-"+str(int(cuts[2]))+"s",">"+str(int(cuts[2]))+"s"]
        bk=[]
        for bi in range(4):
            bx=[x for x in xs if sum(x["dur"]>c for c in cuts)==bi]
            if not bx: bk.append({}); continue
            med=st.median([x["dps"] for x in bx]); row={}
            for c in CLS:
                cx=[x["dps"] for x in bx if x["cls"]==c]
                if len(cx)>=3:
                    row[c]=dict(n=len(cx),avg=st.mean(cx),rel=st.mean(cx)/med,max=max(cx)); acc[c][0]+=row[c]["rel"]*len(cx); acc[c][1]+=len(cx)
            bk.append(row)
        out["killTime"][a+" / "+b]=dict(labels=labels,n=len(xs),buckets=bk)
out["killTimeIndex"]={c:dict(rel=v[0]/v[1],n=v[1]) for c,v in acc.items()}
out["durByClass"]={c:dict(medDur=st.median([s["dur"] for s in F if s["cls"]==c])) for c in CLS}
G=[s for s in F if s["hasGear"] and s["wEnch"] is not None]
TIERS=["<=+5 weapon","+6 weapon","+7 weapon","+8/+9 weapon"]
def tier(s):
    if s["wEnch"]>=8: return TIERS[3]
    if s["wEnch"]==7: return TIERS[2]
    if s["wEnch"]==6: return TIERS[1]
    return TIERS[0]
out["gear"]={"coverage":dict(withGear=len(G),of=len(F)),"tiers":{}}
for t in TIERS:
    sub=[s for s in G if tier(s)==t]
    out["gear"]["tiers"][t]=dict(n=len(sub),classes=relidx(sub),brooch=dict(collections.Counter(s["brooch"] for s in sub).most_common(3)))
STD=[s for s in G if s["wEnch"]==6 and s["brooch"]=="Chrono Brooch" and s["armor"]==(6,6,6)]
out["gear"]["stdBucket"]=dict(desc="+6 weapon, Chrono Brooch, +6/+6/+6 armor",n=len(STD),classes=relidx(STD),
    byArea={a:relidx([s for s in STD if s["area"]==a]) for a in areas})
def band(i): return "<400" if i<400 else "400-407" if i<408 else "408-410" if i<411 else "411+"
IL=[s for s in F if s["ilvl"]]
out["gear"]["ilvlBands"]={}
for b in ["<400","400-407","408-410","411+"]:
    sub=[s for s in IL if band(s["ilvl"])==b]
    out["gear"]["ilvlBands"][b]=dict(n=len(sub),classes=relidx(sub))
out["gear"]["tierEffect"]={t:dict(n=len(x),med=st.median([s["rel"] for s in x])) for t in TIERS for x in [[s for s in G if tier(s)==t]]}
out["gear"]["broochEffect"]={b:dict(n=len(x),med=st.median([s["rel"] for s in x]) if x else None) for b in ["Chrono Brooch","Kumasylum Brooch","Crimson Brooch"] for x in [[s for s in G if s["brooch"]==b and s["wEnch"]==6]]}
out["gear"]["classGearProfile"]={}
for c in CLS:
    x=[s for s in G if s["cls"]==c]
    il=[s["ilvl"] for s in x if s["ilvl"]]
    out["gear"]["classGearProfile"][c]=dict(n=len(x),avgIlvl=st.mean(il) if il else None,avgWEnch=st.mean([s["wEnch"] for s in x]),pctChrono=sum(s["brooch"]=="Chrono Brooch" for s in x)/len(x),pct7plus=sum(s["wEnch"]>=7 for s in x)/len(x))
out["gear"]["classByTier"]={}
for c in CLS:
    row={}
    for t in TIERS:
        x=[s["rel"] for s in G if s["cls"]==c and tier(s)==t]
        if len(x)>=3: row[t]=dict(n=len(x),med=st.median(x),avg=st.mean(x))
    row["ilvlSlope"]=None
    il=[(s["ilvl"],s["rel"]) for s in G if s["cls"]==c and s["ilvl"] and 395<=s["ilvl"]<=420]
    if len(il)>=30:
        mx=st.mean(i for i,_ in il); my=st.mean(r for _,r in il)
        sxx=sum((i-mx)**2 for i,_ in il); sxy=sum((i-mx)*(r-my) for i,r in il)
        row["ilvlSlope"]=dict(n=len(il),perIlvl=sxy/sxx)
    out["gear"]["classByTier"][c]=row
out["representation"]={c:dict(samples=sum(1 for s in F if s["cls"]==c),players=len({s["pid"] for s in F if s["cls"]==c and not s["anon"]}),medDur=out["durByClass"][c]["medDur"],avgCrit=st.mean([s["crit"] for s in F if s["cls"]==c and s["crit"] is not None])) for c in CLS}
json.dump(out,open("final.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)
json.dump(S,open("samples_final.json","w"))
print(json.dumps(out["dataset"]))
def show(d,key):
    for c,v in sorted(d.items(),key=lambda kv:-kv[1][key]): print("  %-10s"%c,{k:(round(v2,3) if isinstance(v2,float) else v2) for k,v2 in v.items()})
print("\nrelIndex"); show(out["relIndex"],"avg")
print("\nkillTimeIndex"); show(out["killTimeIndex"],"rel")
print("\nSTD bucket n=",out["gear"]["stdBucket"]["n"]); show(out["gear"]["stdBucket"]["classes"],"avg")
print("\ntierEffect",out["gear"]["tierEffect"],"\nbrooch",out["gear"]["broochEffect"])
print("\nclass gear profile"); show(out["gear"]["classGearProfile"],"avgWEnch")
