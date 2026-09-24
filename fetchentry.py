"""Fetch entry-dungeon encounters to calibrate the party-buff baseline.

Players in Vanguard Initiate or low-enchant Mournshard gear cannot have
etchings, so whatever surplus their stats show over their items is purely party
buffs. Sampling Red Refuge and Lakan's Prison gives that baseline, which can
then be subtracted from endgame parses to leave the etching.

    python fetchentry.py [max_encounters_per_dungeon]
"""
import json,os,sys,urllib.request,urllib.error,time,threading
from concurrent.futures import ThreadPoolExecutor
B="https://tera-europe-classic.com/api/leaderboard"
AREAS={739:"Red Refuge",810:"Lakan's Prison"}
LIMIT=int(sys.argv[1]) if len(sys.argv)>1 else 900
os.makedirs("entry",exist_ok=True)
def get(url,tries=3):
    for i in range(tries):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"curl/8.0"})
            with urllib.request.urlopen(req,timeout=90) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code==404: raise
            time.sleep(2)
        except Exception:
            if i==tries-1: raise
            time.sleep(2)
uids=[]
for area,name in AREAS.items():
    cur=None; got=[]
    while len(got)<LIMIT:
        d=get(f"{B}/recent?dungeon={area}&limit=100"+(f"&cursor={cur}" if cur else ""))
        enc=d.get("encounters") or []
        got+=[e["id"] for e in enc if e.get("id")]
        cur=d.get("nextCursor")
        if not d.get("hasMore") or not cur: break
    print(f"{name:16} listed {len(got)}",flush=True)
    uids+=got[:LIMIT]
have={f[:-5] for f in os.listdir("entry")}
todo=[u for u in uids if u not in have]
print(f"{len(uids)} encounters | {len(have)} cached | fetching {len(todo)}",flush=True)
lock=threading.Lock(); stat={"ok":0,"gone":0,"fail":0}
def item(it):
    if not it: return None
    return dict(name=it.get("name"),enchant=it.get("enchant"),itemLevel=it.get("itemLevel"),
        rolls=[x.get("description") for x in (it.get("itemPassivities") or []) if isinstance(x,dict)],
        base=it.get("passivityEffects") or [],
        crystals=[c.get("name") for c in (it.get("crystals") or [])])
def one(uid):
    out=f"entry/{uid}.json"
    if os.path.exists(out): return
    for i in range(3):
        try:
            d=get(B+"/encounter/"+uid,tries=1)
            recs=[dict(name=p.get("name"),pid=p.get("playerId"),cls=p.get("class"),role=p.get("role"),
                       dps=p.get("dps"),crit=p.get("critRate"),stats=p.get("characterStats"),
                       equipment={k:item(v) for k,v in (p.get("equipment") or {}).items()})
                  for p in d["players"]]
            json.dump(dict(uid=uid,area=d["areaId"],boss=d["bossName"],dur=d["fightDuration"],
                           party=[dict(cls=p.get("class"),role=p.get("role")) for p in d["players"]],
                           players=recs),open(out,"w"))
            with lock: stat["ok"]+=1
            return
        except urllib.error.HTTPError as e:
            if e.code==404:
                with lock: stat["gone"]+=1
                return
            time.sleep(2)
        except Exception: time.sleep(2)
    with lock: stat["fail"]+=1
t=time.time(); done=threading.Event()
def prog():
    while not done.wait(15):
        with lock: n=sum(stat.values())
        rate=n/max(1e-9,time.time()-t)
        print(f"  {n}/{len(todo)} ok={stat['ok']} missing={stat['gone']} {time.time()-t:.0f}s "
              f"eta {(len(todo)-n)/rate/60 if rate else 0:.0f}m",flush=True)
threading.Thread(target=prog,daemon=True).start()
try:
    with ThreadPoolExecutor(16) as ex: list(ex.map(one,todo))
finally: done.set()
print(f"done in {time.time()-t:.0f}s | ok {stat['ok']} | missing {stat['gone']} | failed {stat['fail']} "
      f"| cache {len(os.listdir('entry'))}",flush=True)
