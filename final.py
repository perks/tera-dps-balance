import json,os,collections,statistics as st
rows=json.load(open("rows.json"))
meta={r["encounterUid"]:r for r in rows}
AREAS={556:"TS Hard",456:"TS Savage",568:"SS Hard",468:"SS Savage",507:"Dragon's Landing"}
CLS=['Archer','Berserker','Gunner','Ninja','Reaper','Slayer','Sorcerer','Valkyrie','Warrior']
S=[]; drop=collections.Counter()
# Encounter details are the source of truth. The rankings row only supplies the
# timestamp; encounters that have since dropped off the board (the board keeps
# each player's best parse per boss) are still counted, they just have no date.
# /recent supplies area + timestamp for encounters the rankings board never
# surfaced (it only keeps each player's best parse per boss)
ridx=json.load(open("recent_index.json")) if os.path.exists("recent_index.json") else {}
offboard=0; notank=0
for f in os.listdir("enc"):
    d=json.load(open("enc/"+f))
    m=meta.get(d["uid"])
    if m is None:
        offboard+=1
        r=ridx.get(d["uid"]) or {}
        m={"areaId":r.get("area",d.get("area")),"encounterUnixEpoch":r.get("ts")}
    psize=len(d["players"])
    # A party with nobody labelled tank is not a standard run: somebody is
    # tanking on a dps-labelled character, and their damage is far below what
    # that class does in a normal group. Warriors take the brunt of this.
    if not any(p["role"]=="tank" for p in d["players"]):
        drop["no tank in party"]+=len([p for p in d["players"] if p["cls"] in CLS and p["role"]=="dps"])
        notank+=1
        continue
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
            ilvl=p["ilvl"],wEnch=p["wEnchant"],gEnch=(p["armorEnchant"] or {}).get("gloves"),brooch=p["brooch"],hasGear=p["hasGear"],
            enr=sum(1 for r in wr if "enraged" in r),flat=sum(1 for r in wr if r.startswith("Increases damage by 6.0%")),
            behind=sum(1 for r in wr if "from behind" in r),armor=tuple(p["armorEnchant"].values())))
print("samples",len(S),"drop",dict(drop),"| encounters not on the rankings board (kept):",offboard,
      "| kills with no tank (dropped):",notank)
# ---------- patch windows ----------
# Only patches that touch DPS class balance or the difficulty of the five
# endgame dungeons matter here; purely cosmetic, questing or healer-only patches
# would split the data without explaining anything, so they are not boundaries.
import datetime
PATCHES=[
 dict(id="v0.04",name="v0.04",start=None,end=datetime.datetime(2026,9,12,2,34),
      summary="Baseline. No DPS-class changes; the patch touched Priest glyphs and dungeon reputation.",
      classes=[],
      content=["Shadow Sanguinary Hard: final enrage countdown cut from 3m30s to 3m."]),
 dict(id="v0.05",name="v0.05",start=datetime.datetime(2026,9,12,2,34),end=datetime.datetime(2026,9,16,0,0),
      summary="First real DPS balance pass, and the difficulty split that created today's Hard modes.",
      classes=[dict(cls="Slayer",dir="buff",text="+10% damage against monsters; Heart Thrust hit area widened."),
               dict(cls="Berserker",dir="buff",text="+5% damage against monsters. Evasive Smash's Cyclone bonus limited to monsters."),
               dict(cls="Archer",dir="change",text="Find Weakness reworked: Weakness Exposed makes Radiant Arrow, Penetrating Arrow and Thunderbolt count as back attacks for +25%. Close Quarters cooldown up to 10.5s."),
               dict(cls="Reaper",dir="pvp",text="PvP-only damage increase; no PvE change.")],
      content=["The old Hard modes were renamed Savage. New Hard modes added with 25% less enemy HP and attack.",
               "Dragon's Landing Normal now starts directly on Calamity Helghan; his attack-speed bonus cut from 30% to 23%."]),
 dict(id="v0.06",name="v0.06",start=datetime.datetime(2026,9,16,0,0),end=None,
      summary="Archer's rework finally works, and the new Hard modes were tuned down.",
      classes=[dict(cls="Archer",dir="buff",text="Fixed Find Weakness III's 25% damage bonus, which had not been applying.")],
      content=["Timescape Hard: all bosses -10% attack; HP cut by 35% (Eremes), 20% (Tempas), 10% (Hemera, Valona).",
               "Shadow Sanguinary Hard: all bosses -10% HP and attack; Imperator's shield 24M to 15.6M.",
               "Dragon's Landing: dive attack disabled, tank-circle hitboxes corrected."]),
]
def patch_of(ts):
    if ts is None: return None
    d=datetime.datetime.utcfromtimestamp(ts)
    for P in PATCHES:
        if (P["start"] is None or d>=P["start"]) and (P["end"] is None or d<P["end"]): return P["id"]
    return None
for x in S: x["patch"]=patch_of(x["ts"])

def q(xs,p):
    xs=sorted(xs); k=(len(xs)-1)*p; f=int(k); c=min(f+1,len(xs)-1); return xs[f]+(xs[c]-xs[f])*(k-f)
def stats(rows):
    xs=[r["dps"] for r in rows]
    cr=[r["crit"] for r in rows if r["crit"] is not None]
    dd=[r["deaths"] for r in rows if r["deaths"] is not None]
    return dict(n=len(xs),players=len({r["pid"] for r in rows}),min=min(xs),p25=q(xs,.25),med=st.median(xs),
                avg=st.mean(xs),p75=q(xs,.75),p90=q(xs,.9),max=max(xs),
                crit=st.mean(cr) if cr else None,deaths=st.mean(dd) if dd else None)
def build(S):
    out={}
    F=[s for s in S if s["psize"]==5]
    out["dataset"]=dict(samples=len(S),five=len(F),encounters=len({s["uid"] for s in S}),players=len({s["pid"] for s in S if not s["anon"]}),
        anon=sum(s["anon"] for s in S),dateFrom=min(s["ts"] for s in S if s["ts"]),dateTo=max(s["ts"] for s in S if s["ts"]),drop=dict(drop))
    areas=list(AREAS.values())
    bossmed={k:st.median([s["dps"] for s in F if (s["area"],s["boss"])==k]) for k in {(s["area"],s["boss"]) for s in F}}
    for s in S: s["rel"]=s["dps"]/bossmed[(s["area"],s["boss"])]
    def cnt(sub,a,c,b=None): return sum(1 for s in sub if s["area"]==a and s["cls"]==c and (b is None or s["boss"]==b))
    out["byArea"]={a:{c:stats([s for s in F if s["area"]==a and s["cls"]==c]) for c in CLS if cnt(F,a,c)>=3} for a in areas}
    out["byBoss"]={}
    for a in areas:
        for b in sorted({s["boss"] for s in F if s["area"]==a}):
            out["byBoss"][a+" / "+b]={c:stats([s for s in F if s["area"]==a and s["boss"]==b and s["cls"]==c]) for c in CLS if cnt(F,a,c,b)>=3}
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
    # ---------- gear-equalised comparison ----------
    # Damage-relevant enchanting on this server concentrates in the weapon and the
    # gloves, so that pair is a fair shorthand for how far along someone's gear is.
    # A class is only ever compared inside one (boss, weapon+, gloves+) cell, which
    # holds the boss and the gear level fixed at once. A cell needs several classes
    # in it or its median would just be the class being measured.
    #
    # The enchant ladder runs past what anyone has reached: the highest recorded
    # here is +10 on a weapon and +9 on gloves, and the top of the ladder is held
    # by a handful of people, so bands above +6 rest on very few players however
    # many parses they produce. Player counts travel with every figure for that
    # reason, and a class resting on fewer than MINPLAYERS is marked thin.
    GE=[s for s in F if s.get("wEnch") is not None and s.get("gEnch") is not None]
    cells=collections.defaultdict(list)
    for s2 in GE: cells[(s2["area"],s2["boss"],s2["wEnch"],s2["gEnch"])].append(s2)
    MINCELL,MINCLS,MINN,MINPLAYERS=8,3,25,10
    norm=[]
    for (a2,b2,w,g),xs in cells.items():
        if len(xs)<MINCELL or len({x["cls"] for x in xs})<MINCLS: continue
        med=st.median([x["dps"] for x in xs])
        if not med: continue
        for x in xs: norm.append((x["cls"],x["pid"],x["dps"]/med,w,g))

    def summarise(rows,minn=MINN,minpl=5):
        cl={}
        for c in CLS:
            v=[(r,pid) for cc,pid,r,_,_ in rows if cc==c for r,pid in [(r,pid)]]
            if len(v)<minn: continue
            pl={pid for _,pid in v}
            if len(pl)<minpl: continue
            cl[c]=dict(n=len(v),players=len(pl),rel=st.mean([r for r,_ in v]),
                       med=st.median([r for r,_ in v]),thin=len(pl)<MINPLAYERS)
        return cl

    # One bucket per enchant level, never grouped: levels are not interchangeable
    # and pooling them hides exactly the thing this section exists to show.
    # A class figure needs at least MINPL distinct players behind it, or it is a
    # portrait of one person. That is what rules a level out, not parse count:
    # +9 has 566 parses but ten players in total, several classes being a single
    # person, so it cannot carry a class comparison at any sample size.
    exact=[]; skipped=[]
    for lv in sorted({w for _,_,_,w,g in norm if w==g}):
        rows=[r for r in norm if r[3]==lv and r[4]==lv]
        if len(rows)<60: continue
        cl=summarise(rows,minn=8,minpl=3)
        rec=dict(level=lv,label="+%d weapon and gloves"%lv,short="+%d"%lv,
                 n=len(rows),players=len({r[1] for r in rows}),
                 thin=any(v["thin"] for v in cl.values()),classes=cl)
        (exact if len(cl)>=4 else skipped).append(rec if len(cl)>=4 else
            dict(short=rec["short"],n=rec["n"],players=rec["players"],classes=len(cl)))

    out["gearMatch"]=dict(minCell=MINCELL,minClasses=MINCLS,minPlayers=MINPLAYERS,
        n=len(norm),cells=sum(1 for xs in cells.values() if len(xs)>=MINCELL and len({x["cls"] for x in xs})>=MINCLS),
        maxWeapon=max((w for _,_,_,w,_ in norm),default=None),maxGloves=max((g for _,_,_,_,g in norm),default=None),
        overall=summarise(norm),exact=exact,skipped=skipped)

    # ---------- kill-time tiers ----------
    # Kills on each boss are ranked fastest-first and cut into speed tiers: the top
    # 5%, 10%, 20%, 30%, 40% and 50% fastest, plus the bottom 50%. The top tiers are
    # cumulative (top 5% contains the top 1%), which keeps the small tiers usable on
    # thin bosses. Classes are only ever compared inside the same tier on the same
    # boss, so a fast kill is never measured against a slow one.
    TIERS=[(0.05,"Top 5% fastest"),(0.10,"Top 10%"),(0.20,"Top 20%"),(0.30,"Top 30%"),(0.40,"Top 40%"),(0.50,"Top 50%"),(None,"Bottom 50%")]
    NT=len(TIERS)
    def fmt(sec):
        sec=int(round(sec))
        return f"{sec}s" if sec<60 else (f"{sec//60}m {sec%60}s" if sec%60 else f"{sec//60}m")
    def tier_slice(xs,pct):
        xs=sorted(xs,key=lambda x:x["dur"])
        if pct is None: return xs[len(xs)//2:]
        return xs[:max(1,int(round(len(xs)*pct)))]
    out["killTime"]={}; acc=collections.defaultdict(lambda:[0,0])
    for a in areas:
        for b in sorted({s["boss"] for s in F if s["area"]==a}):
            xs=[s for s in F if s["area"]==a and s["boss"]==b]
            if not xs: continue
            labels=[lab for _,lab in TIERS]; bk=[]; counts=[]; ranges=[]
            for pct,lab in TIERS:
                bx=tier_slice(xs,pct)
                counts.append(len(bx)); ranges.append([min(x["dur"] for x in bx),max(x["dur"] for x in bx)] if bx else None)
                if not bx: bk.append({}); continue
                med=st.median([x["dps"] for x in bx]); row={}
                for c in CLS:
                    cx=[x["dps"] for x in bx if x["cls"]==c]
                    if len(cx)>=3:
                        row[c]=dict(n=len(cx),avg=st.mean(cx),rel=st.mean(cx)/med,max=max(cx))
                        acc[c][0]+=row[c]["rel"]*len(cx); acc[c][1]+=len(cx)
                bk.append(row)
            out["killTime"][a+" / "+b]=dict(labels=labels,n=len(xs),counts=counts,ranges=ranges,buckets=bk)
    out["killTimeIndex"]={c:dict(rel=v[0]/v[1],n=v[1]) for c,v in acc.items()}
    # Pooled view, built twice. "all" counts every parse; "best" first reduces each
    # player to their single best parse per boss, so an active player cannot weight a
    # class. In both modes the baseline median is rebuilt from the same population
    # the classes are drawn from, otherwise the levels would not be comparable.
    def pooled(samples):
        gp=[collections.defaultdict(list) for _ in range(NT)]
        granges=[[] for _ in range(NT)]
        for a in areas:
            for b in sorted({s["boss"] for s in samples if s["area"]==a}):
                xs=[s for s in samples if s["area"]==a and s["boss"]==b]
                if not xs: continue
                key=a+" / "+b
                for ti,(pct,lab) in enumerate(TIERS):
                    bx=tier_slice(xs,pct)
                    if not bx: continue
                    med=st.median([x["dps"] for x in bx])
                    for x in bx: gp[ti][x["cls"]].append(x["dps"]/med)
                    granges[ti].append(dict(boss=key,lo=min(x["dur"] for x in bx),hi=max(x["dur"] for x in bx),n=len(bx)))
        return [dict(label=TIERS[ti][1],
            classes={c:dict(n=len(v),rel=st.mean(v),players=None) for c,v in gp[ti].items() if len(v)>=3},
            bosses=sorted(granges[ti],key=lambda r:-r["n"])) for ti in range(NT)]
    bestonly={}
    for s2 in F:
        k=(s2["pid"],s2["area"],s2["boss"])
        if k not in bestonly or s2["dps"]>bestonly[k]["dps"]: bestonly[k]=s2
    FB=list(bestonly.values())
    out["killTimeGlobal"]=pooled(F)
    out["killTimeGlobalBest"]=pooled(FB)
    out["killTimeModes"]=dict(all=len(F),best=len(FB))
    # ---------- movement metric ----------
    # For comparing one patch against another: the fastest 10% of kills on each
    # boss, measured against the median parse in that same group. No gear
    # control - at this end of the ladder players are geared and executing, and
    # that is the population a balance change should be judged on.
    fast=[]
    for k in {(x["area"],x["boss"]) for x in F}:
        xs=[x for x in F if (x["area"],x["boss"])==k]
        cut=q([x["dur"] for x in xs],.10)
        fast+=[x for x in xs if x["dur"]<=cut]
    mb={}
    for k in {(x["area"],x["boss"]) for x in fast}:
        v=[x["dps"] for x in fast if (x["area"],x["boss"])==k]
        if len(v)>=8: mb[k]=st.median(v)
    mv=collections.defaultdict(list)
    for x in fast:
        k=(x["area"],x["boss"])
        if k in mb: mv[x["cls"]].append(x["dps"]/mb[k])
    out["moveIndex"]={c:dict(n=len(v),rel=st.mean(v)) for c,v in mv.items() if len(v)>=25}
    out["moveCoverage"]=dict(used=sum(len(v) for v in mv.values()),fastest=len(fast))
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
    return out

ALL=build(S)
out=dict(ALL)
out["patches"]={}
for P in PATCHES:
    sub=[x for x in S if x["patch"]==P["id"]]
    if len(sub)<200: continue
    out["patches"][P["id"]]=build(sub)
out["patchMeta"]=[dict(id=P["id"],name=P["name"],summary=P["summary"],classes=P["classes"],content=P["content"],
    start=(P["start"].isoformat()+"Z" if P["start"] else None),end=(P["end"].isoformat()+"Z" if P["end"] else None),
    parses=sum(1 for x in S if x["patch"]==P["id"] and x["psize"]==5),
    kills=len({x["uid"] for x in S if x["patch"]==P["id"] and x["psize"]==5}),
    current=P["end"] is None) for P in PATCHES]
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
