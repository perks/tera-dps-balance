"""Fetch character stats + full equipment for chosen classes, for etching detection.

The main enc/ cache is slimmed and keeps only a few stat fields, none of them
the *Bonus totals an etching would show up in. This pulls the full payload for a
sample of encounters containing the classes asked for, and keeps one record per
player per encounter in stats/<uid>.json.

    python fetchstats.py Berserker Valkyrie [max_encounters]
"""
import json,os,sys,urllib.request,urllib.error,time,threading,random
from concurrent.futures import ThreadPoolExecutor
BASE="https://tera-europe-classic.com/api/leaderboard/encounter/"
args=[a for a in sys.argv[1:] if not a.isdigit()]
CLASSES=set(args) or {"Berserker","Valkyrie"}
LIMIT=int([a for a in sys.argv[1:] if a.isdigit()][0]) if any(a.isdigit() for a in sys.argv[1:]) else 1200
os.makedirs("stats",exist_ok=True)
gone=set(json.load(open("enc_gone.json"))) if os.path.exists("enc_gone.json") else set()
cand=[]
for f in os.listdir("enc"):
    d=json.load(open("enc/"+f))
    if len(d["players"])!=5: continue
    if any(p.get("cls") in CLASSES and p.get("role")=="dps" and (p.get("dps") or 0)>=50000 for p in d["players"]):
        cand.append(d["uid"])
random.seed(11); random.shuffle(cand)
have={f[:-5] for f in os.listdir("stats")}
todo=[u for u in cand if u not in have and u not in gone][:LIMIT]
print(f"{len(cand)} encounters contain {', '.join(sorted(CLASSES))} | {len(have)} cached | fetching {len(todo)}",flush=True)
lock=threading.Lock(); stat={"ok":0,"gone":0,"fail":0}
def item(it):
    if not it: return None
    return dict(name=it.get("name"),enchant=it.get("enchant"),itemLevel=it.get("itemLevel"),
        rolls=[x.get("description") for x in (it.get("itemPassivities") or []) if isinstance(x,dict)],
        base=it.get("passivityEffects") or [],
        crystals=[c.get("name") for c in (it.get("crystals") or [])])
def one(uid):
    out=f"stats/{uid}.json"
    if os.path.exists(out): return
    for i in range(3):
        try:
            req=urllib.request.Request(BASE+uid,headers={"User-Agent":"curl/8.0"})
            with urllib.request.urlopen(req,timeout=120) as r: d=json.load(r)
            recs=[dict(name=p.get("name"),pid=p.get("playerId"),cls=p.get("class"),role=p.get("role"),
                       dps=p.get("dps"),crit=p.get("critRate"),stats=p.get("characterStats"),
                       equipment={k:item(v) for k,v in (p.get("equipment") or {}).items()})
                  for p in d["players"] if p.get("class") in CLASSES and p.get("role")=="dps"]
            json.dump(dict(uid=uid,area=d["areaId"],boss=d["bossName"],dur=d["fightDuration"],players=recs),open(out,"w"))
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
def progress():
    while not done.wait(15):
        with lock: n=sum(stat.values())
        rate=n/max(1e-9,time.time()-t)
        print(f"  {n}/{len(todo)} ok={stat['ok']} missing={stat['gone']} failed={stat['fail']} "
              f"{time.time()-t:.0f}s eta {(len(todo)-n)/rate/60 if rate else 0:.0f}m",flush=True)
threading.Thread(target=progress,daemon=True).start()
try:
    with ThreadPoolExecutor(16) as ex: list(ex.map(one,todo))
finally: done.set()
print(f"done in {time.time()-t:.0f}s | ok {stat['ok']} | missing {stat['gone']} | failed {stat['fail']} | cache {len(os.listdir('stats'))}",flush=True)
