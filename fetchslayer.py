import json,urllib.request,os,time
from concurrent.futures import ThreadPoolExecutor
BASE="https://tera-europe-classic.com/api/leaderboard/encounter/"
uids=json.load(open("slayer_uids.json"))
os.makedirs("slayer",exist_ok=True)
def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":"curl/8.0"})
    with urllib.request.urlopen(req,timeout=120) as r: return json.load(r)
def item(it):
    if not it: return None
    return dict(name=it.get("name"),slot=it.get("slot"),enchant=it.get("enchant"),itemLevel=it.get("itemLevel"),rarity=it.get("rarity"),
        masterwork=it.get("masterwork"),awakened=it.get("awakened"),
        rolls=[x.get("description") for x in (it.get("itemPassivities") or []) if isinstance(x,dict)],
        pool=[x.get("description") for x in (it.get("rollablePassivities") or []) if isinstance(x,dict)],
        base=it.get("passivityEffects") or [],
        crystals=[c.get("name") for c in (it.get("crystals") or [])])
def one(uid):
    out=f"slayer/{uid}.json"
    if os.path.exists(out): return
    for attempt in range(3):
        try:
            d=get(BASE+uid)
            recs=[]
            for p in d["players"]:
                if p.get("class")!="Slayer" or p.get("role")!="dps": continue
                eq=p.get("equipment") or {}
                epid=p.get("encounterPlayerId") or p.get("playerId")
                skills=None
                if epid:
                    try: skills=get(f"{BASE}{uid}/skills/{epid}").get("skillStats")
                    except Exception: skills=None
                recs.append(dict(name=p.get("name"),pid=p.get("playerId"),dps=p.get("dps"),totalDamage=p.get("totalDamage"),
                    dmgpct=p.get("damagePercentage"),crit=p.get("critRate"),deaths=p.get("deaths"),alive=p.get("aliveAtEnd"),
                    classPct=p.get("classPercentile"),score=p.get("score"),
                    stats=p.get("characterStats"),
                    equipment={k:item(v) for k,v in eq.items()},
                    glyphs=[dict(id=g.get("id"),name=g.get("name"),skill=g.get("skillName"),points=g.get("points"),enabled=g.get("enabled"),desc=g.get("description")) for g in (p.get("glyphs") or [])],
                    skills=[dict(id=s.get("skillId"),name=s.get("skillName"),dmg=s.get("totalDamage"),hits=s.get("hits"),crits=s.get("crits"),
                        minCrit=s.get("minCrit"),maxCrit=s.get("maxCrit"),avgCrit=s.get("avgCrit"),minWhite=s.get("minWhite"),maxWhite=s.get("maxWhite"),
                        avgWhite=s.get("avgWhite"),dmgpct=s.get("damagePercent")) for s in (skills or [])]))
            json.dump(dict(uid=uid,area=d["areaId"],boss=d["bossName"],dur=d["fightDuration"],partyDps=d.get("partyDps"),
                party=[dict(cls=p.get("class"),role=p.get("role"),dps=p.get("dps")) for p in d["players"]],
                slayers=recs),open(out,"w"))
            return
        except Exception as e:
            time.sleep(2)
    print("FAIL",uid)
t=time.time()
with ThreadPoolExecutor(6) as ex: list(ex.map(one,uids))
print("done",len(os.listdir("slayer")),"in",round(time.time()-t),"s")
