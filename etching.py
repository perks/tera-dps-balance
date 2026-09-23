"""Etching detection from character stats.

The API never names etchings. It does give, per parse, the character's stat
totals and the exact items worn, so an etching should appear as a surplus the
gear cannot account for:

    Keen      +18 crit factor
    Power     +10 power
    Energetic +4% attack speed (its 2.5% cooldown is not exposed at all)

Two facts about the data decide what is and is not possible.

1. The equipment payload is complete. Character item level is reproduced
   exactly - RMS 0.0000 over 4,024 parses - by a fixed weighting of the 11 worn
   items (weapon .274, chest .207, gloves/boots .185, accessories .030 each).
   Nothing is hidden in the item list, and etchings do not raise item level.

2. The stat snapshot is taken mid-fight, so it carries party buffs. The same
   player reads +56 crit factor with a Mystic in the group and -33 power with a
   Priest, on identical gear. Worse, buffs are not identical between members of
   one party at the moment each snapshot is taken, so they cannot be cancelled
   by a per-encounter constant either: fitting encounter effects still leaves
   RMS 7.2 crit, which is the size of an etching.

So absolute per-player detection is not dependable. What is dependable is the
comparison between two players of the same class in the same kill, where the
buff state is as close to identical as this data gets. That comparison is what
this script reports, and the etching steps show up in it cleanly.

Usage:  python etching.py
"""
import json,os,re,collections,statistics as st
import numpy as np

SLOTS=["weapon","gloves","chest","boots","belt","brooch","necklace",
       "ring-left","ring-right","earring-left","earring-right"]
STEP={"crit":18.0,"power":10.0,"aspd":4.0}
FIELD={"crit":"critFactorBonus","power":"powerBonus","aspd":"attackSpeedBonus"}
NAME={"crit":"Keen (+18 crit factor)","power":"Power (+10 power)","aspd":"Energetic (+4% attack speed)"}
NUM=r"([\d.]+)"
PAT={"crit":[re.compile(r"Increases Crit Factor by "+NUM),re.compile(r"Increases Crit Rate by "+NUM)],
     "power":[re.compile(r"Increases Power by "+NUM)],
     "aspd":[re.compile(r"Increases Attack Speed by "+NUM+r"%")]}

def summed(eq,stat):
    """Everything the worn items themselves declare for this stat."""
    tot=0.0
    for it in (eq or {}).values():
        if not it: continue
        for txt in (it.get("base") or [])+(it.get("rolls") or []):
            for p in PAT[stat]:
                m=p.search(txt or "")
                if m: tot+=float(m.group(1))
    return tot

def load():
    out=[]
    for src,get in (("slayer",lambda d:d["slayers"]),("stats",lambda d:d["players"])):
        if not os.path.isdir(src): continue
        for f in os.listdir(src):
            d=json.load(open(src+"/"+f))
            for p in get(d):
                stt=p.get("stats") or {}; eq=p.get("equipment") or {}
                if not eq or not stt: continue
                out.append(dict(uid=d["uid"],cls=p.get("cls") or "Slayer",name=p.get("name"),
                                stats=stt,eq=eq))
    return out

def verify_itemlevel(recs):
    rows=[(np.array([(r["eq"].get(s) or {}).get("itemLevel") for s in SLOTS],dtype=float),
           r["stats"].get("itemLevel")) for r in recs]
    rows=[(x,y) for x,y in rows if y is not None and not np.isnan(x).any()]
    if len(rows)<50: return
    X=np.array([x for x,_ in rows]); y=np.array([v for _,v in rows])
    coef,*_=np.linalg.lstsq(np.hstack([X,np.ones((len(X),1))]),y,rcond=None)
    res=y-(np.hstack([X,np.ones((len(X),1))])@coef)
    print(f"equipment completeness check: item level reproduced from worn items alone, "
          f"RMS {np.sqrt((res**2).mean()):.4f} over {len(rows)} parses")

def pairs(recs,stat):
    """Same class, same kill: party buffs are shared, so the gap is gear."""
    byenc=collections.defaultdict(list)
    for r in recs:
        if isinstance(r["stats"].get(FIELD[stat]),(int,float)): byenc[r["uid"]].append(r)
    out=[]
    for rows in byenc.values():
        for i in range(len(rows)):
            for j in range(i+1,len(rows)):
                a,b=rows[i],rows[j]
                if a["cls"]!=b["cls"]: continue
                ra=a["stats"][FIELD[stat]]-summed(a["eq"],stat)
                rb=b["stats"][FIELD[stat]]-summed(b["eq"],stat)
                out.append((abs(round(ra-rb,1)),a["cls"]))
    return out

if __name__=="__main__":
    recs=load()
    print(f"loaded {len(recs)} parses with stats and full equipment\n")
    verify_itemlevel(recs)
    for stat in ("aspd","crit","power"):
        P=pairs(recs,stat); step=STEP[stat]
        if not P: continue
        h=collections.Counter(d for d,_ in P)
        n=len(P)
        onestep=sum(v for d,v in h.items() if abs(d-step)<0.25)
        twostep=sum(v for d,v in h.items() if abs(d-2*step)<0.25)
        print(f"\n=== {NAME[stat]} ===")
        print(f"same-class pairs in one kill: {n}")
        print(f"  identical ({h.get(0.0,0)}) — both players' gear fully explains their stats: {100*h.get(0.0,0)/n:.0f}%")
        print(f"  differ by exactly one step  ({onestep}): {100*onestep/n:.0f}%")
        print(f"  differ by exactly two steps ({twostep}): {100*twostep/n:.0f}%")
        near=", ".join(f"{d:g}:{c}" for d,c in sorted(h.items()) if c>=4 and d<=3*step)
        print(f"  gap distribution up to 3 steps: {near}")
        print(f"  (a gap landing on {step:g} or {2*step:g} is one or two more etchings on one side;"
              f" other gaps are buff drift between the two snapshots)")
