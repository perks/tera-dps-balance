import json, urllib.request, urllib.parse, time
BASE="https://tera-europe-classic.com/api/leaderboard"
AREAS={556:"TS Hard",456:"TS Savage",568:"SS Hard",468:"SS Savage",507:"Dragon's Landing"}
def get(path, **q):
    url=f"{BASE}{path}?{urllib.parse.urlencode(q)}"
    for i in range(3):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"curl/8.0","Accept":"application/json"})
            with urllib.request.urlopen(req, timeout=60) as r: return json.load(r)
        except Exception as e:
            print("retry",url,e); time.sleep(2)
    raise SystemExit("fail "+url)
rows=[]
for a in AREAS:
    page=1
    while True:
        d=get("/rankings",dungeon=a,mode="solo",roleKey="dps",pageSize=100,page=page,sortBy="dps")
        rows+=d["items"]
        if page*100>=d["total"]: break
        page+=1
    print(a,AREAS[a],d["total"])
json.dump(rows,open("rows.json","w"))
print("rows",len(rows),"unique encounters",len({r["encounterUid"] for r in rows}))
