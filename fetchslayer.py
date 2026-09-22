import json,urllib.request,urllib.error,os,time,threading
from concurrent.futures import ThreadPoolExecutor
BASE="https://tera-europe-classic.com/api/leaderboard/encounter/"
uids=json.load(open("slayer_uids.json"))
os.makedirs("slayer",exist_ok=True)
GONE="slayer_gone.json"
gone=set(json.load(open(GONE))) if os.path.exists(GONE) else set()
have={f[:-5] for f in os.listdir("slayer")}
uids=[u for u in uids if u not in have and u not in gone]
lock=threading.Lock(); stat={"ok":0,"gone":0,"fail":0}
print(f"{len(uids)} to fetch",flush=True)
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
            with lock: stat["ok"]+=1
            return
        except urllib.error.HTTPError as e:
            if e.code==404:
                with lock: gone.add(uid); stat["gone"]+=1
                return
            time.sleep(2)
        except Exception as e:
            time.sleep(2)
    with lock: stat["fail"]+=1
t=time.time(); done=threading.Event()
def progress():
    while not done.wait(15):
        with lock:
            n=stat["ok"]+stat["gone"]+stat["fail"]; json.dump(sorted(gone),open(GONE,"w"))
        rate=n/max(1e-9,time.time()-t)
        print(f"  {n}/{len(uids)}  fetched={stat['ok']} missing={stat['gone']} failed={stat['fail']}"
              f"  {time.time()-t:.0f}s  eta {(len(uids)-n)/rate/60 if rate else 0:.0f}m",flush=True)
threading.Thread(target=progress,daemon=True).start()
try:
    with ThreadPoolExecutor(12) as ex: list(ex.map(one,uids))
finally:
    done.set(); json.dump(sorted(gone),open(GONE,"w"))
print(f"done in {time.time()-t:.0f}s | fetched {stat['ok']} | missing {stat['gone']} | failed {stat['fail']} | cache {len(os.listdir('slayer'))}",flush=True)
