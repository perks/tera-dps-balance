import json,re,datetime
css=re.search(r"<style>(.*?)</style>",open("report.py",encoding="utf-8").read(),re.S).group(1)
D=json.load(open("final.json",encoding="utf-8"))
S=json.load(open("slayer2.json",encoding="utf-8"))
ds=D["dataset"]
d0=datetime.datetime.utcfromtimestamp(ds["dateFrom"]).strftime("%b %d")
d1=datetime.datetime.utcfromtimestamp(ds["dateTo"]).strftime("%b %d, %Y")
cards=[
 ("tera-dps-balance/","DPS class balance",
  f"Every DPS player in {ds['encounters']:,} recorded 5-man kills of Timescape, Shadow Sanguinary and Dragon's Landing. Raw, kill-time-matched and gear-matched comparisons across all nine DPS classes.",
  [(f"{ds['five']:,}","parses"),(f"{ds['players']:,}","named players"),("9","classes")]),
 ("slayer-build/","Slayer build data",
  f"What the top 25 Slayers on each endgame boss actually wear: rolls, crystals, jewelry lines and glyph adoption, measured from their best parses.",
  [(f"{S['dataset']['players']}","players"),(f"{S['dataset']['shortlistParses']}","parses"),(f"{S['dataset']['boards']}","boss lists")]),
 ("slayer-guide/","Slayer guide",
  "How to play the class: gearing targets, glyph tiers, the opener, rotation priority, repositioning and defensives.",
  [("PvE","focus"),("0.04","patch"),("Guide","format")]),
]
html = r"""<title>TERA Classic+ Data</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<style>__CSS__
.hero{margin-bottom:26px}
.cards{display:grid;gap:12px}
.card{display:block;border:1px solid var(--line);border-radius:8px;padding:18px 20px;background:var(--panel);text-decoration:none;color:inherit;transition:border-color .12s}
.card:hover{border-color:var(--bar)}
.card h3{font-family:"Barlow Condensed",sans-serif;font-size:24px;font-weight:700;margin:0 0 4px;letter-spacing:.01em}
.card p{margin:0;color:var(--ink2);font-size:14.5px;line-height:1.5;max-width:68ch}
.card .stats{display:flex;gap:18px;margin-top:12px;flex-wrap:wrap}
.card .stats div{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
.card .stats b{display:block;font-family:"Barlow Condensed",sans-serif;font-size:21px;color:var(--ink);letter-spacing:0;text-transform:none;font-variant-numeric:tabular-nums}
.card .go{color:var(--bar);font-weight:600;font-size:14px;margin-top:12px;display:inline-block}
</style>
<div class="wrap">
<div class="eyebrow">TERA Europe Classic+ · public leaderboard API · __D0__ – __D1__</div>
<div class="hero">
<h1>Classic+ Data</h1>
<p class="sub">Analysis built from the public leaderboard API, covering the five endgame dungeons: Timescape (Hard and Savage), Shadow Sanguinary (Hard and Savage) and Dragon's Landing.</p>
</div>
<div class="cards">__CARDS__</div>
<p class="note" style="margin-top:22px">Data is a snapshot, not live. Anonymous players are included in aggregate statistics but cannot be de-duplicated, so player counts are lower bounds.</p>
</div>
"""
cardhtml="".join(
 f'<a class="card" href="{href}"><h3>{title}</h3><p>{desc}</p>'
 f'<div class="stats">{"".join(f"<div><b>{v}</b>{l}</div>" for v,l in stats)}</div>'
 f'<span class="go">Open &rarr;</span></a>' for href,title,desc,stats in cards)
html=html.replace("__CSS__",css).replace("__CARDS__",cardhtml).replace("__D0__",d0).replace("__D1__",d1)
open("index.html","w",encoding="utf-8").write('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width"></head><body style="margin:0">'+html+'</body></html>')
print("ok",len(html))
