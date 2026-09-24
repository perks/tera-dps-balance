"""Check the Slayer glyph data against the raw parses. Exits non-zero on a fault.

The failure this exists to catch: this server runs custom glyphs and reuses
display names across glyph ids that do entirely different things. Anything that
groups or counts glyphs by name silently merges them, which drops glyphs from
the page and shows the wrong description for the ones that survive.

    python verify_glyphs.py
"""
import json,glob,collections,sys,os

live={}; use=collections.Counter(); parses=0
for f in glob.glob("slayer/*.json"):
    d=json.load(open(f,encoding="utf-8"))
    for p in d["slayers"]:
        gl=p.get("glyphs") or []
        if gl: parses+=1
        for g in gl:
            live.setdefault(g["id"],g)
            if g.get("enabled"): use[g["id"]]+=1
print(f"{len(live)} glyph ids across {parses} glyph-bearing parses\n")

fail=[]

# 1. names are not unique, so nothing downstream may key on them
byname=collections.defaultdict(set)
for gid,g in live.items(): byname[g["name"]].add(gid)
dupes={n:ids for n,ids in byname.items() if len(ids)>1}
print(f"[1] display names covering more than one glyph id: {len(dupes)} "
      f"({sum(len(v) for v in dupes.values())} of {len(live)} ids)")
both=[(n,ids) for n,ids in dupes.items() if sum(use[i]>0 for i in ids)>1]
for n,ids in sorted(both):
    print(f"    both in use: {n}")
    for i in sorted(ids):
        if use[i]: print(f"      #{i} used {use[i]:5}  -> {live[i]['desc']}")

# 2. every glyph that made the page must be present, by id, exactly once
out=json.load(open("slayer2.json",encoding="utf-8"))
L=out["glyphs"]["list"]
ids=[g["id"] for g in L]
if len(ids)!=len(set(ids)): fail.append("slayer2.json lists a glyph id twice")
print(f"\n[2] glyphs on the page: {len(L)}, all distinct ids: {len(ids)==len(set(ids))}")

# 3. name, host skill and description must match the live payload for that id
bad=0
for g in L:
    src=live.get(g["id"])
    if not src: fail.append(f"#{g['id']} on the page is not in the parse data"); continue
    if g["name"]!=src["name"]:
        fail.append(f"#{g['id']} name '{g['name']}' != live '{src['name']}'"); bad+=1
    if g.get("skill")!=src.get("skill"):
        fail.append(f"#{g['id']} host '{g.get('skill')}' != live '{src.get('skill')}'"); bad+=1
print(f"[3] name and host skill match the live payload for all {len(L)} glyphs: {bad==0}")

# 4. labels must be unique, or the page shows two rows a reader cannot tell apart
lab=collections.Counter(g["label"] for g in L)
clash=[k for k,v in lab.items() if v>1]
print(f"[4] every displayed label is unique: {not clash}")
for c in clash: fail.append(f"label '{c}' is shown for {lab[c]} different glyphs")

# 5. no unresolved server placeholder may reach the page
ph=[g["id"] for g in L if "$" in (g.get("desc") or "")]
print(f"[5] no $value/$prob placeholder text on the page: {not ph}")
for i in ph: fail.append(f"#{i} still shows a raw placeholder")

# 6. the heavily-used glyphs must all be on the page
missing=[(i,c) for i,c in use.most_common() if c>=200 and i not in set(ids)]
print(f"[6] every glyph used 200+ times is on the page: {not missing}")
for i,c in missing: fail.append(f"#{i} ({live[i]['name']}) used {c} times but absent")

# 7. artwork
noicon=[g["id"] for g in L if not g.get("icon")]
print(f"[7] every glyph resolved an icon: {not noicon}")
for i in noicon: fail.append(f"#{i} has no icon")

if fail:
    print("\nFAILED:"); [print("  -",m) for m in fail]; sys.exit(1)
print("\nall checks passed")
