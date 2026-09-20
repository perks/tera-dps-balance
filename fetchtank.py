import json,urllib.request,os,time
from concurrent.futures import ThreadPoolExecutor
BASE="https://tera-europe-classic.com/api/leaderboard/encounter/"
rows=json.load(open("rows.json"))
uids=sorted({r["encounterUid"] for r in rows})
os.makedirs("enc2",exist_ok=True)
def slim(p):
    eq=p.get("equipment") or {}; cs=p.get("characterStats") or {}
    w=eq.get("weapon") or {}; br=eq.get("brooch") or {}
    return dict(name=p.get("name"),cls=p.get("class"),role=p.get("role"),pid=p.get("playerId"),epid=p.get("encounterPlayerId"),
        dps=p.get("dps"),dmgpct=p.get("damagePercentage"),crit=p.get("critRate"),deaths=p.get("deaths"),alive=p.get("aliveAtEnd"),
        aggro=p.get("aggro"),classPct=p.get("classPercentile"),
        ilvl=cs.get("itemLevel"),power=cs.get("power"),powerBonus=cs.get("powerBonus"),attack=cs.get("attack"),
        wEnchant=w.get("enchant"),brooch=br.get("name"),armorEnchant=[(eq.get(s) or {}).get("enchant") for s in ("chest","gloves","boots")],
        hasGear=bool(eq),
        abn=[(a.get("id"),a.get("start"),a.get("end"),a.get("stack"),a.get("sourceId")) for a in (p.get("abnormals") or [])],
        contributedDebuffs=p.get("contributedDebuffs"))
def one(uid):
    out=f"enc2/{uid}.json"
    if os.path.exists(out): return
    for i in range(3):
        try:
            req=urllib.request.Request(BASE+uid,headers={"User-Agent":"curl/8.0"})
            with urllib.request.urlopen(req,timeout=120) as r: d=json.load(r)
            json.dump(dict(uid=uid,area=d["areaId"],bossId=d["bossId"],boss=d["bossName"],dur=d["fightDuration"],partyDps=d.get("partyDps"),enrage=d.get("enragePercent"),
                buffUptimes=d.get("buffUptimes"),debuffUptimes=d.get("debuffUptimes"),
                players=[slim(p) for p in d["players"]]),open(out,"w")); return
        except Exception as e: time.sleep(2)
    print("FAIL",uid)
t=time.time()
with ThreadPoolExecutor(6) as ex: list(ex.map(one,uids))
print("done",len(os.listdir("enc2")),"in",round(time.time()-t),"s")
