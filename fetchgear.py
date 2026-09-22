"""Fetch encounter detail (gear, glyphs, per-player role) for the encounters in
pick.json, caching one JSON per encounter in enc/.

Already-cached encounters are never refetched. A 404 means the encounter is not
retrievable - hidden by the server's consent checks, or purged - so it is
recorded in enc_gone.json and skipped on later runs rather than retried forever.
"""
import json,urllib.request,urllib.error,os,time,threading
from concurrent.futures import ThreadPoolExecutor
BASE="https://tera-europe-classic.com/api/leaderboard/encounter/"
pick=json.load(open("pick.json"))
os.makedirs("enc",exist_ok=True)
GONE="enc_gone.json"
gone=set(json.load(open(GONE))) if os.path.exists(GONE) else set()
have={f[:-5] for f in os.listdir("enc")}
todo=[u for u in pick if u not in have and u not in gone]
print(f"{len(pick)} referenced | {len(have)} cached | {len(gone)} known-missing | {len(todo)} to fetch",flush=True)
lock=threading.Lock(); stat={"ok":0,"gone":0,"fail":0}
def slim(p):
    eq=p.get("equipment") or {}
    cs=p.get("characterStats") or {}
    w=eq.get("weapon") or {}; br=eq.get("brooch") or {}
    def rolls(it): return [x.get("description") for x in (it.get("itemPassivities") or []) if isinstance(x,dict)]
    return dict(name=p.get("name"),cls=p.get("class"),role=p.get("role"),pid=p.get("playerId"),classPct=p.get("classPercentile"),alive=p.get("aliveAtEnd"),dps=p.get("dps"),dmgpct=p.get("damagePercentage"),crit=p.get("critRate"),deaths=p.get("deaths"),
        ilvl=cs.get("itemLevel"),power=cs.get("power"),critFactor=cs.get("critFactor"),attack=cs.get("attack"),
        weapon=w.get("name"),wEnchant=w.get("enchant"),wIlvl=w.get("itemLevel"),wRolls=rolls(w),wCrystals=[c.get("name") for c in (w.get("crystals") or [])],
        brooch=br.get("name"),
        armorEnchant={s:(eq.get(s) or {}).get("enchant") for s in ("chest","gloves","boots")},
        jewelry={s:(eq.get(s) or {}).get("name") for s in ("necklace","ring-left","ring-right","earring-left","earring-right","belt")},
        hasGear=bool(eq))
def one(uid):
    out=f"enc/{uid}.json"
    if os.path.exists(out): return
    for i in range(3):
        try:
            req=urllib.request.Request(BASE+uid,headers={"User-Agent":"curl/8.0"})
            with urllib.request.urlopen(req,timeout=120) as r: d=json.load(r)
            json.dump(dict(uid=uid,area=d["areaId"],boss=d["bossName"],dur=d["fightDuration"],enrage=d.get("enragePercent"),
                partyDps=d.get("partyDps"),players=[slim(p) for p in d["players"]]),open(out,"w"))
            with lock: stat["ok"]+=1
            return
        except urllib.error.HTTPError as e:
            if e.code==404:
                with lock: gone.add(uid); stat["gone"]+=1
                return
            time.sleep(2)
        except Exception:
            time.sleep(2)
    with lock: stat["fail"]+=1
t=time.time(); done=threading.Event()
def progress():
    while not done.wait(15):
        with lock:
            n=stat["ok"]+stat["gone"]+stat["fail"]
            json.dump(sorted(gone),open(GONE,"w"))   # checkpoint, so a stop loses nothing
        rate=n/max(1e-9,time.time()-t)
        eta=(len(todo)-n)/rate/60 if rate else 0
        print(f"  {n}/{len(todo)}  fetched={stat['ok']} not-retrievable={stat['gone']} failed={stat['fail']}"
              f"  {time.time()-t:.0f}s  eta {eta:.0f}m",flush=True)
threading.Thread(target=progress,daemon=True).start()
try:
    with ThreadPoolExecutor(16) as ex: list(ex.map(one,todo))
finally:
    done.set(); json.dump(sorted(gone),open(GONE,"w"))
print(f"done in {time.time()-t:.0f}s | fetched {stat['ok']} | not retrievable {stat['gone']} | failed {stat['fail']} | cache now {len(os.listdir('enc'))}",flush=True)
