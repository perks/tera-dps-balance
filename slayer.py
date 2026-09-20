import json,os,re,collections,statistics as st,math,random
random.seed(7)
AREAS={556:"TS Hard",456:"TS Savage",568:"SS Hard",468:"SS Savage",507:"Dragon's Landing"}
ACC=["necklace","earring-left","earring-right","ring-left","ring-right","belt","brooch"]
def q(xs,p):
    xs=sorted(xs); k=(len(xs)-1)*p; f=int(k); c=min(f+1,len(xs)-1); return xs[f]+(xs[c]-xs[f])*(k-f)
# ---------- roll parsing ----------
PAT=[(r"Increases Power by ([\d.]+)","Power"),(r"Increases Crit Factor by ([\d.]+)","Crit Factor"),
     (r"Increase[s]? Crit Power by ([\d.]+)%","Crit Power"),(r"Increases Attack Speed by ([\d.]+)%","Attack Speed"),
     (r"Increases Endurance by ([\d.]+)","Endurance"),(r"Increases Crit Resist Factor by ([\d.]+)","Crit Resist"),
     (r"Raises max HP by ([\d.]+)%","Max HP %"),(r"Raises max HP by ([\d.]+)","Max HP"),
     (r"Increases your healing skills by ([\d.]+)%","Healing %"),(r"Increases your healing skills by ([\d.]+)","Healing"),
     (r"Decreases skill cooldowns by ([\d.]+)%","Cooldown"),(r"Increases damage by ([\d.]+)% when attacking enraged","Dmg vs enraged"),
     (r"Increases damage by ([\d.]+)% when attacking from behind","Dmg from behind"),
     (r"Increases damage by ([\d.]+)% when attacking knocked-down","Dmg vs knocked-down"),
     (r"Increases damage by ([\d.]+)%\.","Flat damage"),(r"Increases damage of ([A-Za-z' ]+) by ([\d.]+)%","Skill damage"),
     (r"Increases ([A-Za-z' ]+) skill damage by ([\d.]+)%","Skill damage"),
     (r"Replenishes ([\d.]+)% of total MP","MP regen"),(r"Recovers ([\d.]+)% of total HP","HP regen"),
     (r"Increases Movement Speed by ([\d.]+)%","Move Speed"),(r"Increases Balance Factor by ([\d.]+)","Balance"),
     (r"Decreases damage taken","Damage taken"),(r"Increases resistance to knockdown","KD resist")]
def parse(txt):
    if not txt: return None,None
    for pat,lab in PAT:
        m=re.search(pat,txt)
        if m:
            try: v=float(m.group(m.lastindex))
            except Exception: v=None
            return lab,v
    return "Other",None
# ---------- load ----------
R=[]
for f in os.listdir("slayer"):
    d=json.load(open("slayer/"+f))
    for s in d["slayers"]:
        if (s["dps"] or 0)<50000: continue
        eq=s["equipment"] or {}
        stats=s["stats"] or {}
        rolls=collections.Counter(); rollval=collections.Counter(); accset={}; rawRolls={}
        for slot in ACC:
            it=eq.get(slot)
            if not it: continue
            accset[slot]=it["name"]
            rawRolls[slot]=tuple(sorted(parse(t)[0] for t in (it["rolls"] or [])))
            for txt in (it["rolls"] or []):
                lab,v=parse(txt); rolls[lab]+=1
                if v: rollval[lab]+=v
        w=eq.get("weapon") or {}
        R.append(dict(uid=d["uid"],area=AREAS.get(d["area"],str(d["area"])),boss=d["boss"],dur=d["dur"],dps=s["dps"],
            pid=s["pid"],name=s["name"],anon=s["pid"] is None,crit=s["crit"],deaths=s["deaths"],dmgpct=s["dmgpct"],
            ilvl=stats.get("itemLevel"),power=stats.get("powerBonus"),critFactor=stats.get("critFactorBonus"),critPower=stats.get("critPowerBonus"),
            attackSpeed=stats.get("attackSpeedBonus"),attack=stats.get("attackMaxBonus"),endurance=stats.get("enduranceBonus"),critResist=stats.get("critResistBonus"),defense=stats.get("defenseBonus"),
            wName=w.get("name"),wEnch=w.get("enchant"),wCrystals=tuple(sorted(w.get("crystals") or [])),
            wRolls=[parse(t)[0] for t in (w.get("rolls") or [])],
            armorEnch=tuple((eq.get(s2) or {}).get("enchant") for s2 in ("chest","gloves","boots")),
            accset=accset,rawRolls=rawRolls,rolls=dict(rolls),rollval=dict(rollval),nAccRolls=sum(rolls.values()),
            glyphs=tuple(sorted({g["name"] for g in s["glyphs"] if g["enabled"]})),
            glyphPts=sum(g["points"] or 0 for g in s["glyphs"] if g["enabled"]),
            hasGlyphs=bool(s["glyphs"]),hasGear=bool(eq),
            skills=s["skills"]))
# index vs median Slayer DPS on that boss
bm=collections.defaultdict(list)
for r in R: bm[(r["area"],r["boss"])].append(r["dps"])
BM={k:st.median(v) for k,v in bm.items() if len(v)>=5}
for r in R: r["rel"]=r["dps"]/BM[(r["area"],r["boss"])] if (r["area"],r["boss"]) in BM else None
S=[r for r in R if r["rel"]]
out={"dataset":dict(records=len(R),indexed=len(S),encounters=len({r["uid"] for r in R}),players=len({r["pid"] for r in R if r["pid"]}),
    anon=sum(r["anon"] for r in R),withGear=sum(r["hasGear"] for r in R),withGlyphs=sum(r["hasGlyphs"] for r in R),
    byArea=dict(collections.Counter(r["area"] for r in R)),bosses={f"{k[0]} / {k[1]}":len(v) for k,v in bm.items()})}
# player-level score (median index), tiers
pl=collections.defaultdict(list)
for r in S:
    if r["pid"]: pl[r["pid"]].append(r)
players={p:dict(name=v[0]["name"],n=len(v),med=st.median(x["rel"] for x in v),best=max(x["rel"] for x in v),
                dps=st.median(x["dps"] for x in v)) for p,v in pl.items()}
rank=sorted([p for p,v in players.items() if v["n"]>=3],key=lambda p:-players[p]["med"])
TOP=set(rank[:max(3,len(rank)//4)])
for r in S: r["tier"]="Top 25%" if r["pid"] in TOP else ("Ranked" if r["pid"] in players and players[r["pid"]]["n"]>=3 else "Other")
out["players"]=dict(ranked=len(rank),top=len(TOP),
    table=[dict(name=players[p]["name"],n=players[p]["n"],med=players[p]["med"],best=players[p]["best"],dps=players[p]["dps"],top=p in TOP) for p in rank])
def grp(rows,ci=True):
    v=[r["rel"] for r in rows]
    d=dict(n=len(rows),players=len({r["pid"] for r in rows if r["pid"]}),med=st.median(v),avg=st.mean(v),p90=q(v,.9))
    if ci and len(v)>=5:
        ms=sorted(st.median(random.choices(v,k=len(v))) for _ in range(800))
        d["lo"]=ms[20]; d["hi"]=ms[779]
    return d
out["tiers"]={t:grp([r for r in S if r["tier"]==t]) for t in ("Top 25%","Ranked","Other") if any(r["tier"]==t for r in S)}
# ---------- gear: accessory pieces ----------
G=[r for r in S if r["hasGear"]]
out["accPieces"]={}
for slot in ACC:
    c=collections.Counter(r["accset"].get(slot) for r in G if r["accset"].get(slot))
    rows={}
    for name,cnt in c.most_common(6):
        sub=[r for r in G if r["accset"].get(slot)==name]
        if len(sub)>=5: rows[name]=dict(**grp(sub),share=cnt/max(1,sum(c.values())),topShare=sum(1 for r in sub if r["tier"]=="Top 25%")/len(sub))
    out["accPieces"][slot]=rows
# full accessory set signature (necklace+earring+ring family)
def fam(n):
    if not n: return None
    for k in ("Monarch","Titan","Chrono","Kumasylum","Crimson"):
        if k in n: return k
    return n.split()[-1]
for r in G:
    r["accFam"]=tuple(sorted(collections.Counter(fam(r["accset"].get(s2)) for s2 in ("necklace","earring-left","earring-right","ring-left","ring-right") if r["accset"].get(s2)).items()))
    r["broochN"]=r["accset"].get("brooch"); r["beltN"]=r["accset"].get("belt")
cc=collections.Counter(r["accFam"] for r in G)
out["accSets"]={" + ".join(f"{k}×{v}" for k,v in sig):dict(**grp([r for r in G if r["accFam"]==sig]),share=n/len(G)) for sig,n in cc.most_common(8) if n>=8}
# ---------- gear: roll lines ----------
labs=collections.Counter()
for r in G: labs.update(r["rolls"])
out["rollTypes"]={}
for lab,cnt in labs.most_common(14):
    has=[r for r in G if r["rolls"].get(lab)]; non=[r for r in G if not r["rolls"].get(lab)]
    if len(has)>=8 and len(non)>=8:
        out["rollTypes"][lab]=dict(rolls=cnt,share=len(has)/len(G),withIt=grp(has),without=grp(non),
            topRate=sum(1 for r in has if r["tier"]=="Top 25%")/len(has),
            avgCount=st.mean(r["rolls"].get(lab,0) for r in G),avgCountTop=st.mean(r["rolls"].get(lab,0) for r in G if r["tier"]=="Top 25%") if any(r["tier"]=="Top 25%" for r in G) else None)
# dose response: count of offensive rolls (Power + Crit Factor + Crit Power + Attack Speed)
OFF=["Power","Crit Factor","Crit Power","Attack Speed"]
for r in G: r["nOff"]=sum(r["rolls"].get(l,0) for l in OFF); r["offVal"]=dict((l,r["rollval"].get(l,0)) for l in OFF)
buckets=[(0,1),(2,3),(4,5),(6,20)]
out["offRolls"]=[dict(label=(f"{a}–{b}" if b<20 else f"{a}+"),**grp([r for r in G if a<=r["nOff"]<=b])) for a,b in buckets if len([r for r in G if a<=r["nOff"]<=b])>=8]
out["offRollsTop"]=dict(top=st.mean(r["nOff"] for r in G if r["tier"]=="Top 25%"),rest=st.mean(r["nOff"] for r in G if r["tier"]!="Top 25%"))
# power vs crit factor totals from accessory rolls
out["rollMix"]={}
for lab in OFF:
    vals=[r["rollval"].get(lab,0) for r in G]
    if max(vals)>0:
        cut=st.median([v for v in vals if v>0]) if any(v>0 for v in vals) else 0
        hi=[r for r in G if r["rollval"].get(lab,0)>cut]; lo=[r for r in G if r["rollval"].get(lab,0)<=cut]
        if len(hi)>=8 and len(lo)>=8: out["rollMix"][lab]=dict(cut=cut,hi=grp(hi),lo=grp(lo),avgTop=st.mean(r["rollval"].get(lab,0) for r in G if r["tier"]=="Top 25%"),avgRest=st.mean(r["rollval"].get(lab,0) for r in G if r["tier"]!="Top 25%"))
wl=collections.Counter()
for r in G: wl.update(set(r["wRolls"] or []))
# gear-controlled: restrict to ilvl>=408 so roll choice is not a proxy for gear level
GC=[r for r in G if (r["ilvl"] or 0)>=408]
out["rollTypesGeared"]={"n":len(GC),"list":{}}
for lab,cnt in labs.most_common(14):
    has=[r for r in GC if r["rolls"].get(lab)]; non=[r for r in GC if not r["rolls"].get(lab)]
    if len(has)>=8 and len(non)>=8:
        out["rollTypesGeared"]["list"][lab]=dict(share=len(has)/len(GC),withIt=grp(has),without=grp(non))
out["offRollsGeared"]=[dict(label=(f"{a}-{b}" if b<20 else f"{a}+"),**grp([r for r in GC if a<=r["nOff"]<=b])) for a,b in buckets if len([r for r in GC if a<=r["nOff"]<=b])>=8]
# per-slot roll signature
out["slotRolls"]={}
for slot in ACC:
    sig=collections.Counter()
    for r in G:
        it=r.get("rawRolls",{}).get(slot)
        if it: sig[it]+=1
    rows={}
    for k,v in sig.most_common(6):
        sub=[r for r in G if r.get("rawRolls",{}).get(slot)==k]
        if len(sub)>=8: rows[" + ".join(k) if k else "(none)"]=dict(**grp(sub),share=v/max(1,sum(sig.values())))
    if rows: out["slotRolls"][slot]=rows
# geared-only variants of the gear tables (fair "what should I roll" comparison)
def slotTable(rows):
    o={}
    for slot in ACC:
        sig=collections.Counter()
        for r in rows:
            it=r.get("rawRolls",{}).get(slot)
            if it: sig[it]+=1
        t={}
        for k,v in sig.most_common(6):
            sub=[r for r in rows if r.get("rawRolls",{}).get(slot)==k]
            if len(sub)>=8: t[" + ".join(k) if k else "(none)"]=dict(**grp(sub),share=v/max(1,sum(sig.values())))
        if t: o[slot]=t
    return o
out["slotRollsGeared"]=slotTable(GC)
out["accSetsGeared"]={" + ".join(f"{k}x{v}" for k,v in sig):dict(**grp([r for r in GC if r["accFam"]==sig]),share=n/max(1,len(GC))) for sig,n in collections.Counter(r["accFam"] for r in GC).most_common(6) if n>=8}
ccg=collections.Counter(r["wCrystals"] for r in GC if r["wCrystals"])
out["crystalsGeared"]={" + ".join(k):dict(**grp([r for r in GC if r["wCrystals"]==k]),share=v/max(1,sum(ccg.values()))) for k,v in ccg.most_common(5) if v>=8}
out["weaponRollsGeared"]={}
for lab,cnt in wl.most_common(10):
    has=[r for r in GC if lab in (r["wRolls"] or [])]; non=[r for r in GC if r["wRolls"] and lab not in r["wRolls"]]
    if len(has)>=8 and len(non)>=8: out["weaponRollsGeared"][lab]=dict(share=len(has)/max(1,len([r for r in GC if r["wRolls"]])),withIt=grp(has),without=grp(non))
out["gearedCut"]=408
# ---------- Monarch (Crit Factor) vs Titan (Power) jewelry ----------
JSLOTS=["necklace","earring-left","earring-right","ring-left","ring-right"]
def line(n):
    if not n: return None
    if "Monarch" in n: return "Monarch"
    if "Titan" in n: return "Titan"
    return "Other"
for r in G:
    ls=[line(r["accset"].get(s2)) for s2 in JSLOTS]
    r["nTitan"]=sum(1 for x in ls if x=="Titan"); r["nMonarch"]=sum(1 for x in ls if x=="Monarch"); r["nJewel"]=sum(1 for x in ls if x)
J={"innate":{"Monarch":{"necklace":"+28 Crit Factor, +6% Attack Speed","ring":"+34 Crit Factor","earring":"+16 Crit Factor"},
             "Titan":{"necklace":"+14 Power, +6% Attack Speed","ring":"+18 Power","earring":"+8 Power"}},"slots":{},"count":[],"countGeared":[],"stats":{},"brooch":{}}
for s2 in JSLOTS:
    row={}
    for lab in ("Monarch","Titan"):
        sub=[r for r in G if line(r["accset"].get(s2))==lab]
        subg=[r for r in GC if line(r["accset"].get(s2))==lab]
        if len(sub)>=8: row[lab]=dict(all=grp(sub),geared=grp(subg) if len(subg)>=8 else None,share=len(sub)/max(1,sum(1 for r in G if line(r["accset"].get(s2)))))
    if row: J["slots"][s2]=row
for lo,hi,lab in [(0,0,"0 Titan (all Crit)"),(1,1,"1 Titan"),(2,2,"2 Titan"),(3,5,"3+ Titan (Power-heavy)")]:
    sub=[r for r in G if r["nJewel"]==5 and lo<=r["nTitan"]<=hi]
    subg=[r for r in GC if r["nJewel"]==5 and lo<=r["nTitan"]<=hi]
    if len(sub)>=8: J["count"].append(dict(label=lab,**grp(sub),share=len(sub)/max(1,sum(1 for r in G if r["nJewel"]==5))))
    if len(subg)>=8: J["countGeared"].append(dict(label=lab,**grp(subg),share=len(subg)/max(1,sum(1 for r in GC if r["nJewel"]==5))))
# do the stat totals and observed crit rate actually move with the choice?
for lab,sel in [("Crit-heavy (0-1 Titan)",lambda r:r["nJewel"]==5 and r["nTitan"]<=1),("Power-heavy (2+ Titan)",lambda r:r["nJewel"]==5 and r["nTitan"]>=2)]:
    sub=[r for r in GC if sel(r)]
    if len(sub)>=8:
        J["stats"][lab]=dict(n=len(sub),critFactor=st.median([r["critFactor"] for r in sub if r["critFactor"]]) if any(r["critFactor"] for r in sub) else None,
            power=st.median([r["power"] for r in sub if r["power"]]) if any(r["power"] for r in sub) else None,
            observedCrit=st.median([r["crit"] for r in sub if r["crit"] is not None]) if any(r["crit"] is not None for r in sub) else None,
            attack=st.median([r["attack"] for r in sub if r["attack"]]) if any(r["attack"] for r in sub) else None,
            index=st.median([r["rel"] for r in sub]))
bc2=collections.Counter(r["broochN"] for r in G if r["broochN"])
for n2,c in bc2.most_common(4):
    sub=[r for r in G if r["broochN"]==n2]; subg=[r for r in GC if r["broochN"]==n2]
    if len(sub)>=8: J["brooch"][n2]=dict(all=grp(sub),geared=grp(subg) if len(subg)>=8 else None,share=c/max(1,sum(bc2.values())))
# observed crit rate vs crit factor bonus (diminishing returns check)
cf=[(r["critFactor"],r["crit"]) for r in S if r.get("critFactor") and r["crit"] is not None]
if len(cf)>=30:
    cf.sort(); n2=len(cf); J["critCurve"]=[dict(range=f"{t[0][0]:.0f}-{t[-1][0]:.0f}",n=len(t),crit=st.median(b for _,b in t)) for t in [cf[:n2//3],cf[n2//3:2*n2//3],cf[2*n2//3:]]]
out["jewelry"]=J
# ---------- stats ----------
out["stats"]={}
for k,lab in [("power","Power (gear bonus)"),("critFactor","Crit Factor (gear bonus)"),("attackSpeed","Attack Speed (gear bonus)"),("attack","Attack (gear bonus)"),("endurance","Endurance (gear bonus)"),("critResist","Crit Resist (gear bonus)"),("ilvl","Item level")]:
    v=[(r[k],r["rel"]) for r in S if r.get(k) is not None]
    if len(v)<30: continue
    xs=[a for a,_ in v]; ys=[b for _,b in v]
    mx,my=st.mean(xs),st.mean(ys); sxx=sum((a-mx)**2 for a in xs); syy=sum((b-my)**2 for b in ys)
    sxy=sum((a-mx)*(b-my) for a,b in v)
    corr=sxy/math.sqrt(sxx*syy) if sxx and syy else 0
    qs=sorted(v); n=len(qs); tert=[qs[:n//3],qs[n//3:2*n//3],qs[2*n//3:]]
    out["stats"][lab]=dict(n=len(v),corr=corr,med=st.median(xs),topMed=st.median([a for a,_ in v if a] ) if False else st.median([r[k] for r in S if r.get(k) is not None and r["tier"]=="Top 25%"]) if any(r.get(k) is not None and r["tier"]=="Top 25%" for r in S) else None,
        terciles=[dict(range=f"{t[0][0]:.0f}–{t[-1][0]:.0f}",n=len(t),med=st.median(b for _,b in t)) for t in tert])
# crystals
cc=collections.Counter(r["wCrystals"] for r in G if r["wCrystals"])
out["crystals"]={" + ".join(k):dict(**grp([r for r in G if r["wCrystals"]==k]),share=v/sum(cc.values())) for k,v in cc.most_common(6) if v>=8}
out["crystalSingles"]={}
singles=collections.Counter(c for r in G for c in set(r["wCrystals"]))
for c,cnt in singles.most_common(8):
    has=[r for r in G if c in r["wCrystals"]]; non=[r for r in G if r["wCrystals"] and c not in r["wCrystals"]]
    if len(has)>=8 and len(non)>=8: out["crystalSingles"][c]=dict(share=len(has)/len([r for r in G if r["wCrystals"]]),withIt=grp(has),without=grp(non))
out["weaponRolls"]={}
for lab,cnt in wl.most_common(10):
    has=[r for r in G if lab in (r["wRolls"] or [])]; non=[r for r in G if r["wRolls"] and lab not in r["wRolls"]]
    if len(has)>=8 and len(non)>=8: out["weaponRolls"][lab]=dict(share=len(has)/len([r for r in G if r["wRolls"]]),withIt=grp(has),without=grp(non))
# ---------- glyphs ----------
GL=[r for r in S if r["hasGlyphs"] and len(r["glyphs"])>=6]
gc=collections.Counter()
for r in GL: gc.update(r["glyphs"])
out["glyphs"]={"n":len(GL),"avgPoints":st.mean(r["glyphPts"] for r in GL) if GL else None,"list":{}}
for g,cnt in gc.most_common(30):
    has=[r for r in GL if g in r["glyphs"]]; non=[r for r in GL if g not in r["glyphs"]]
    if len(has)>=5 and len(non)>=5:
        out["glyphs"]["list"][g]=dict(share=cnt/len(GL),withIt=grp(has),without=grp(non),
            topShare=(sum(1 for r in GL if r["tier"]=="Top 25%" and g in r["glyphs"])/max(1,sum(1 for r in GL if r["tier"]=="Top 25%"))),
            restShare=(sum(1 for r in GL if r["tier"]!="Top 25%" and g in r["glyphs"])/max(1,sum(1 for r in GL if r["tier"]!="Top 25%"))))
# most common full builds
bc=collections.Counter(r["glyphs"] for r in GL)
out["glyphBuilds"]=[dict(glyphs=list(k),**grp([r for r in GL if r["glyphs"]==k])) for k,v in bc.most_common(5) if v>=4]
# ---------- skills ----------
SK=[r for r in S if r["skills"]]
sk=collections.defaultdict(list)
for r in SK:
    tot=sum(float(x["dmg"] or 0) for x in r["skills"]) or 1
    for x in r["skills"]:
        sk[x["name"] or "(unnamed)"].append(dict(rel=r["rel"],tier=r["tier"],dur=r["dur"],hits=x["hits"] or 0,crits=x["crits"] or 0,
            share=100*float(x["dmg"] or 0)/tot,cpm=60*(x["hits"] or 0)/max(1,r["dur"]),
            critRate=100*(x["crits"] or 0)/max(1,x["hits"] or 1),
            avgCrit=x["avgCrit"] or 0,avgWhite=x["avgWhite"] or 0,
            spread=(float(x["maxCrit"] or 0)/float(x["minCrit"]) if x["minCrit"] and float(x["minCrit"])>0 else None)))
out["skills"]={}
for name,v in sorted(sk.items(),key=lambda kv:-st.mean(x["share"] for x in kv[1])):
    if len(v)<20: continue
    top=[x for x in v if x["tier"]=="Top 25%"]; rest=[x for x in v if x["tier"]!="Top 25%"]
    out["skills"][name]=dict(n=len(v),share=st.median(x["share"] for x in v),cpm=st.median(x["cpm"] for x in v),
        critRate=st.median(x["critRate"] for x in v),
        shareTop=st.median(x["share"] for x in top) if len(top)>=5 else None,shareRest=st.median(x["share"] for x in rest) if len(rest)>=5 else None,
        cpmTop=st.median(x["cpm"] for x in top) if len(top)>=5 else None,cpmRest=st.median(x["cpm"] for x in rest) if len(rest)>=5 else None,
        critTop=st.median(x["critRate"] for x in top) if len(top)>=5 else None,critRest=st.median(x["critRate"] for x in rest) if len(rest)>=5 else None,
        spread=st.median([x["spread"] for x in v if x["spread"]]) if any(x["spread"] for x in v) else None)
# total casts per minute and crit rate overall
def cpmTot(rows): return st.median(60*sum(x["hits"] or 0 for x in r["skills"])/max(1,r["dur"]) for r in rows)
out["execution"]=dict(cpmTop=cpmTot([r for r in SK if r["tier"]=="Top 25%"]),cpmRest=cpmTot([r for r in SK if r["tier"]!="Top 25%"]),
    critTop=st.median(r["crit"] for r in SK if r["tier"]=="Top 25%" and r["crit"] is not None),
    critRest=st.median(r["crit"] for r in SK if r["tier"]!="Top 25%" and r["crit"] is not None),
    dmgshareTop=st.median(r["dmgpct"] for r in SK if r["tier"]=="Top 25%" and r["dmgpct"] is not None),
    dmgshareRest=st.median(r["dmgpct"] for r in SK if r["tier"]!="Top 25%" and r["dmgpct"] is not None))
# variance of DPS within player (consistency) and across population
out["variance"]=dict(popCV=st.pstdev([r["rel"] for r in S])/st.mean([r["rel"] for r in S]),
    withinPlayerCV=st.median([st.pstdev([x["rel"] for x in v])/st.mean([x["rel"] for x in v]) for v in pl.values() if len(v)>=4]),
    byArea={a:dict(n=len(v),cv=st.pstdev(v)/st.mean(v)) for a in AREAS.values() for v in [[r["rel"] for r in S if r["area"]==a]] if len(v)>=10},
    p10=q([r["rel"] for r in S],.1),p90=q([r["rel"] for r in S],.9))
json.dump(out,open("slayer.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)
print(json.dumps(out["dataset"],ensure_ascii=False)[:400])
print("\ntiers",{k:(v["n"],round(v["med"],2)) for k,v in out["tiers"].items()})
print("\nacc sets:"); [print("  ",k,round(v["med"],3),v["n"],round(v["share"],2)) for k,v in out["accSets"].items()]
print("\nroll types:"); [print(f"  {k:18} share {v['share']:.2f} with {v['withIt']['med']:.3f} (n{v['withIt']['n']}) without {v['without']['med']:.3f} (n{v['without']['n']}) topRate {v['topRate']:.2f}") for k,v in out["rollTypes"].items()]
print("\noff rolls:",[(b["label"],b["n"],round(b["med"],3)) for b in out["offRolls"]],out["offRollsTop"])
print("\nstats:"); [print(f"  {k:12} corr {v['corr']:+.2f} med {v['med']} terciles",[(t['range'],t['n'],round(t['med'],3)) for t in v['terciles']]) for k,v in out["stats"].items()]
print("\ncrystals:"); [print("  ",k,round(v["med"],3),v["n"]) for k,v in out["crystals"].items()]
print("\nglyph n",out["glyphs"]["n"]); [print(f"  {k:34} share {v['share']:.2f} top {v['topShare']:.2f} rest {v['restShare']:.2f} with {v['withIt']['med']:.3f} without {v['without']['med']:.3f}") for k,v in list(out["glyphs"]["list"].items())[:18]]
print("\nskills:"); [print(f"  {str(k):20} share {v['share'] or 0:.1f}% cpm {v['cpm'] or 0:.1f} crit {v['critRate'] or 0:.0f}% | top cpm {v['cpmTop'] or 0:.1f} rest {v['cpmRest'] or 0:.1f}") for k,v in out["skills"].items()]
print("\nexecution",{k:round(v,1) for k,v in out["execution"].items() if v})
print("variance",{k:(round(v,3) if isinstance(v,float) else v) for k,v in out["variance"].items() if k!="byArea"})
