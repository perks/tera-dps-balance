"""Enumerate every recorded encounter in the five endgame dungeons.

The rankings board only surfaces each player's best parse per boss, so it misses
most kills. /recent lists them all. This walks /recent with its cursor for each
dungeon and writes recent_index.json ({uid: {area, ts}}), then merges the uids
into pick.json so fetchgear.py can pull their detail.
"""
import json,os,urllib.request,time
B="https://tera-europe-classic.com/api/leaderboard"
AREAS={556:"TS Hard",456:"TS Savage",568:"SS Hard",468:"SS Savage",507:"Dragon's Landing"}
def get(url,tries=3):
    for i in range(tries):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"curl/8.0"})
            with urllib.request.urlopen(req,timeout=90) as r: return json.load(r)
        except Exception as e:
            if i==tries-1: raise
            time.sleep(2)
idx=json.load(open("recent_index.json")) if os.path.exists("recent_index.json") else {}
t0=time.time()
for area,name in AREAS.items():
    cursor=None; seen=0; added=0
    while True:
        u=f"{B}/recent?dungeon={area}&limit=100"+(f"&cursor={cursor}" if cursor else "")
        d=get(u)
        enc=d.get("encounters") or []
        for e in enc:
            uid=e.get("id")
            if not uid: continue
            seen+=1
            if uid not in idx:
                idx[uid]=dict(area=e.get("areaId",area),ts=e.get("encounterUnixEpoch"),
                              boss=e.get("bossName"),dur=e.get("fightDuration"))
                added+=1
        cursor=d.get("nextCursor")
        if not d.get("hasMore") or not cursor: break
        if seen%1000==0:
            print(f"  {name}: {seen} listed, {added} new  ({time.time()-t0:.0f}s)",flush=True)
    print(f"{name:18} listed {seen:6} | new {added:6} | index now {len(idx)}  ({time.time()-t0:.0f}s)",flush=True)
json.dump(idx,open("recent_index.json","w"))
pick=set(json.load(open("pick.json"))) if os.path.exists("pick.json") else set()
before=len(pick); pick|=set(idx)
json.dump(sorted(pick),open("pick.json","w"))
gone=set(json.load(open("enc_gone.json"))) if os.path.exists("enc_gone.json") else set()
have={f[:-5] for f in os.listdir("enc")} if os.path.isdir("enc") else set()
print(f"\npick.json {before} -> {len(pick)} | cached {len(have)} | known-missing {len(gone)} | "
      f"to fetch {len(pick-have-gone)}")
