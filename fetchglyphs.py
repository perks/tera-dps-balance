"""Rebuild the Slayer glyph catalogue straight from live encounter payloads.

Glyph metadata is static per glyph id, so one sighting of each id is enough.
This is kept separate from fetchslayer.py because the server runs custom
glyphs: display names are reused across several different glyph ids that do
completely different things, so the id is the only safe key, and the payload
carries icon/skillIcon/parentId fields the parse fetcher throws away.

Old encounters age out of the API (404), so this walks /recent for current
ones. The catalogue is merged, never replaced - a bad run can only fail to add
ids, it can never drop the ones already recorded.

    python fetchglyphs.py [encounters_per_dungeon]
"""
import json,os,sys,time,threading,urllib.request,urllib.error
from concurrent.futures import ThreadPoolExecutor
B="https://tera-europe-classic.com/api/leaderboard"
PER=int(sys.argv[1]) if len(sys.argv)>1 else 400
AREAS=[556,456,568,468,507]
KEEP=("id","name","points","class","level","grade","parentId",
      "skillOrder","glyphOrder","icon","skillIcon")
# The catalogue has always called these "skill" and "desc"; keep that schema so
# entries written by different runs stay comparable.
RENAME={"skillName":"skill","description":"desc"}
CAT="glyph_catalogue.json"

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
for a in AREAS:
    cur=None; got=[]
    while len(got)<PER:
        d=get(f"{B}/recent?dungeon={a}&limit=100"+(f"&cursor={cur}" if cur else ""))
        got+=[e["id"] for e in (d.get("encounters") or []) if e.get("id")]
        cur=d.get("nextCursor")
        if not d.get("hasMore") or not cur: break
    print(f"  dungeon {a}: {len(got)} recent encounters",flush=True)
    uids+=got[:PER]
print(f"{len(uids)} encounters to scan",flush=True)

cat={}; lock=threading.Lock(); stat={"ok":0,"gone":0,"fail":0}
def one(uid):
    try: d=get(B+"/encounter/"+uid,tries=2)
    except urllib.error.HTTPError as e:
        with lock: stat["gone" if e.code==404 else "fail"]+=1
        return
    except Exception:
        with lock: stat["fail"]+=1
        return
    with lock:
        stat["ok"]+=1
        for p in d.get("players") or []:
            for g in (p.get("glyphs") or []):
                gid=g.get("id")
                if gid is None or gid in cat: continue
                e={k:g.get(k) for k in KEEP if g.get(k) is not None}
                for src,dst in RENAME.items():
                    if g.get(src) is not None: e[dst]=g[src]
                e["class"]=p.get("class") or g.get("class")
                cat[gid]=e

t=time.time(); done=threading.Event()
def prog():
    while not done.wait(15):
        with lock: n=sum(stat.values()); c=len(cat)
        print(f"  {n}/{len(uids)} encounters | {c} glyph ids | {time.time()-t:.0f}s",flush=True)
threading.Thread(target=prog,daemon=True).start()
try:
    with ThreadPoolExecutor(12) as ex: list(ex.map(one,uids))
finally: done.set()

if not cat:
    print("no glyphs harvested - leaving the catalogue untouched",flush=True); sys.exit(1)
old=json.load(open(CAT,encoding="utf-8")) if os.path.exists(CAT) else {}
merged=dict(old); added=0
for gid,v in cat.items():
    if str(gid) not in merged: added+=1
    merged[str(gid)]=v                      # refresh metadata, keep unseen ids
json.dump(merged,open(CAT,"w",encoding="utf-8"),indent=1,ensure_ascii=False,sort_keys=True)
slay=sum(1 for v in merged.values() if (v.get("class") or "")=="Slayer")
print(f"\ndone in {time.time()-t:.0f}s | {stat['ok']} encounters read, {stat['gone']} gone | "
      f"catalogue {len(old)} -> {len(merged)} ids (+{added}), {slay} Slayer",flush=True)
