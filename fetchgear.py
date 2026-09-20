import json,urllib.request,os,re,time
from concurrent.futures import ThreadPoolExecutor
BASE="https://tera-europe-classic.com/api/leaderboard/encounter/"
pick=json.load(open("pick.json"))
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
                partyDps=d.get("partyDps"),players=[slim(p) for p in d["players"]]),open(out,"w")); return
        except Exception as e: time.sleep(2)
    print("FAIL",uid)
t=time.time()
with ThreadPoolExecutor(6) as ex: list(ex.map(one,pick))
print("done",len(os.listdir("enc")),"in",round(time.time()-t),"s")
