import json,datetime
D=json.load(open("final.json",encoding="utf-8"))
ds=D["dataset"]
d0=datetime.datetime.utcfromtimestamp(ds["dateFrom"]).strftime("%b %d"); d1=datetime.datetime.utcfromtimestamp(ds["dateTo"]).strftime("%b %d, %Y")
DATA=json.dumps(D,ensure_ascii=False)
html = r"""<title>Classic+ DPS Balance</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
:root{color-scheme:light;
 --bg:#f5f3ee;--panel:#ffffff;--ink:#1b1a17;--ink2:#5b584f;--muted:#8a867a;--line:#e2ded4;--line2:#cfcabc;
 --bar:#2a6fb8;--bar-soft:#c9dcf1;--pos:#1a8a5a;--neg:#c9452b;--pos-bg:#d8f0e4;--neg-bg:#f8d9d1;--mid-bg:#ecebe5;--accent:#b8541f;--heat0:#f4f2ec;--heat1:#2a6fb8}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){color-scheme:dark;
 --bg:#17181a;--panel:#1f2124;--ink:#f1efe8;--ink2:#b8b4a8;--muted:#807c72;--line:#33363b;--line2:#464a51;
 --bar:#4f95e0;--bar-soft:#2a4363;--pos:#3fc48a;--neg:#f0745a;--pos-bg:#1e3a2d;--neg-bg:#452620;--mid-bg:#2a2c30;--accent:#e08a5a;--heat0:#25272b;--heat1:#4f95e0}}
:root[data-theme="dark"]{color-scheme:dark;
 --bg:#17181a;--panel:#1f2124;--ink:#f1efe8;--ink2:#b8b4a8;--muted:#807c72;--line:#33363b;--line2:#464a51;
 --bar:#4f95e0;--bar-soft:#2a4363;--pos:#3fc48a;--neg:#f0745a;--pos-bg:#1e3a2d;--neg-bg:#452620;--mid-bg:#2a2c30;--accent:#e08a5a;--heat0:#25272b;--heat1:#4f95e0}
body{background:var(--bg);color:var(--ink);font-family:Barlow,system-ui,sans-serif;font-size:15px;line-height:1.45;margin:0}
.wrap{max-width:1040px;margin:0 auto;padding-block:28px 64px;padding-inline:20px}
h1{font-family:"Barlow Condensed",Barlow,sans-serif;font-weight:700;font-size:40px;line-height:1;margin:0 0 6px;letter-spacing:.01em;text-wrap:balance}
h2{font-family:"Barlow Condensed",Barlow,sans-serif;font-weight:700;font-size:24px;margin:0 0 4px;letter-spacing:.01em}
h3{font-size:15px;font-weight:600;margin:0 0 6px;color:var(--ink)}
.sub{color:var(--ink2);margin:0 0 18px;max-width:70ch}
.eyebrow{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:600;margin-bottom:4px}
section{margin-top:40px}
.lead{color:var(--ink2);max-width:72ch;margin:0 0 14px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:18px 0 6px}
.tile{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:10px 12px}
.tile b{display:block;font-family:"Barlow Condensed",sans-serif;font-size:28px;font-weight:700;line-height:1.05;font-variant-numeric:tabular-nums}
.tile span{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:16px 18px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media (max-width:760px){.grid2{grid-template-columns:1fr}}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums;font-size:14px}
th{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);text-align:right;padding:6px 8px;border-bottom:1px solid var(--line2);font-weight:600;white-space:nowrap}
th:first-child,td:first-child{text-align:left}
td{padding:6px 8px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}
tr:last-child td{border-bottom:0}
.tscroll{overflow-x:auto}
.mono{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:12.5px}
.n{color:var(--muted);font-size:12px}
.pill{display:inline-block;padding:1px 7px;border-radius:4px;font-size:12.5px;font-weight:600;font-variant-numeric:tabular-nums;min-width:52px;text-align:center}
.pos{background:var(--pos-bg);color:var(--pos)}.neg{background:var(--neg-bg);color:var(--neg)}.mid{background:var(--mid-bg);color:var(--ink2)}
.bars{display:grid;grid-template-columns:90px 1fr 60px 70px;gap:6px 10px;align-items:center;font-size:14px}
.bars .lab{font-weight:600}
.bars .track{position:relative;height:16px;background:var(--heat0);border-radius:3px}
.bars .fill{position:absolute;top:2px;bottom:2px;border-radius:2px;background:var(--bar)}
.bars .fill.neg{background:var(--neg)}
.bars .fill.pos{background:var(--pos)}
.bars .zero{position:absolute;top:-2px;bottom:-2px;width:1px;background:var(--line2)}
.bars .v{text-align:right;font-weight:600;font-variant-numeric:tabular-nums}
.bars .nn{text-align:right;color:var(--muted);font-size:12px}
.hdr{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:600}
select{font:inherit;padding:4px 8px;border:1px solid var(--line2);border-radius:4px;background:var(--panel);color:var(--ink)}
.heat td.h{color:var(--ink);font-weight:500}
.note{font-size:13px;color:var(--ink2);margin-top:8px;max-width:78ch}
ul.tight{margin:6px 0 0 18px;padding:0;max-width:78ch}ul.tight li{margin:4px 0}
.legend{font-size:12px;color:var(--muted);margin-top:8px}
.tabs{display:flex;gap:4px;margin-bottom:10px;flex-wrap:wrap}
.tabs button{font:inherit;font-size:13px;font-weight:600;padding:5px 10px;border:1px solid var(--line2);background:var(--panel);color:var(--ink2);border-radius:4px;cursor:pointer}
.tabs button[aria-selected=true]{background:var(--bar);border-color:var(--bar);color:#fff}
.tabs button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.nav{display:flex;gap:14px;font-size:13px;font-weight:600;margin-bottom:14px;flex-wrap:wrap}.nav a{color:var(--ink2);text-decoration:none;border-bottom:2px solid transparent;padding-bottom:2px}.nav a[aria-current]{color:var(--ink);border-color:var(--bar)}
.nav{display:flex;gap:14px;font-size:13px;font-weight:600;margin-bottom:14px}.nav a{color:var(--ink2);text-decoration:none;border-bottom:2px solid transparent;padding-bottom:2px}.nav a[aria-current]{color:var(--ink);border-color:var(--bar)}
</style>
<div class="wrap">
<div class="nav"><a href="../">Home</a><a href="../tera-dps-balance/" aria-current="page">DPS classes</a><a href="../slayer-build/">Slayer build data</a><a href="../slayer-guide/">Slayer guide</a></div>
<div class="eyebrow">TERA Europe Classic+ · public leaderboard API · __D0__ – __D1__</div>
<h1>Classic+ DPS Balance</h1>
<p class="sub">Every DPS-role player in every recorded 5-man kill of Timescape (Hard/Savage), Shadow Sanguinary (Hard/Savage) and Dragon's Landing. Warriors count only where the game flagged them as DPS rather than tank; healers, tanks and entries under 50k DPS are excluded.</p>
<div class="tiles" id="tiles"></div>

<section>
<h2>Where each class stands</h2>
<p class="lead">Every figure shows <b>how far above or below the typical DPS player</b> a class sits on the same boss, so a Savage kill and a Dragon's Landing kill are on one scale. <b>+10% means 10% more damage than the median player on that boss.</b> Three lenses: raw, kill-time-matched, and same-gear.</p>
<div class="panel">
<div class="tabs" role="tablist" id="lensTabs"></div>
<div id="lensChart"></div>
<p class="note" id="lensNote"></p>
</div>
</section>

<section>
<h2>Raw DPS by dungeon</h2>
<p class="lead">Median / 90th percentile / best recorded DPS per class. <span class="n">n = parses · uniq = distinct named players</span></p>
<div class="panel">
<div class="tabs" role="tablist" id="areaTabs"></div>
<div class="tscroll" id="areaTable"></div>
</div>
</section>

<section>
<h2>Kill-time matched comparison</h2>
<p class="lead">Burst classes look better on fast kills, sustained classes on long ones. Every boss's kills are ranked fastest first and cut into speed tiers. Each class is compared only against the other classes in <b>the same tier on the same boss</b>, so a fast kill is never measured against a slow one. Tiers are cumulative — the top 5% contains the top 1% — which keeps the small tiers usable. Every class is shown with its parse count, because the fastest tiers are thin. All five dungeons are pooled here.</p>
<div class="panel">
<div class="tabs" role="tablist" id="ktTabs"></div>
<div id="ktChart"></div>
<p class="note" id="ktNote"></p>
</div>
<details><summary>Kill times in this tier, per boss</summary><div class="inner tscroll" id="ktRanges"></div></details>
<details><summary>Per-boss breakdown</summary><div class="inner">
<div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:10px"><label for="bossSel" class="hdr">Boss</label><select id="bossSel"></select><span class="n" id="bossN"></span></div>
<div class="tscroll" id="ktTable"></div>
<p class="legend">Cells show each class's average against the middle of that tier. Blank = fewer than 3 parses by that class in the tier.</p>
</div></details>
</section>

<section>
<h2>Gear-matched comparison</h2>
<p class="lead">Recorded equipment snapshots cover <span id="gearCov"></span> of samples. The API exposes weapon/armor enchant, brooch, item level and item rolls; there are no etching or potential fields in this game version, so weapon enchant + brooch + item level is the gear score.</p>
<div class="grid2">
 <div class="panel"><h3>How much gear moves the needle</h3><div class="tscroll" id="gearEffect"></div><p class="note">Median relative DPS (vs boss median) by weapon enchant tier, all classes pooled. The +6 → +7 step is the one to keep in mind when reading raw tables.</p></div>
 <div class="panel"><h3>Who is geared</h3><div class="tscroll" id="gearProfile"></div><p class="note">If a class sits high on the raw table but also has more +7/+8 weapons, the raw number overstates it.</p></div>
</div>
<div class="panel" style="margin-top:16px"><h3>How much each class gains from gear</h3><div class="tscroll" id="classTier"></div><p class="note">Median index per weapon tier, with sample count. <b>% per ilvl</b> is a regression slope over every sample of that class (item level 395–420) — the most robust column, since +7/+8 buckets are thin. Higher = the class scales harder with gear, so it is more undergeared-punished and more BiS-rewarded. Blank = fewer than 3 samples.</p></div>
<div class="panel" style="margin-top:16px"><h3>Same gear, same boss: <span id="stdDesc"></span></h3>
<div class="tabs" role="tablist" id="stdTabs"></div>
<div id="stdChart"></div><p class="note" id="stdNote"></p></div>
</section>

<section>
<h2>Reading guide</h2>
<div class="panel">
<ul class="tight">
<li><b>Vs typical</b> is the fairest single number: it removes boss HP and difficulty differences. A class at +10% does 10% more damage than the median DPS player on the same boss.</li>
<li><b>Player-best</b> figures count each player once at their best parse, so someone who runs a boss fifty times cannot skew a class. The headline lens uses every parse.</li>
<li><b>Kill-time matched</b> is the same comparison inside speed tiers (top 1% / 5% / 10% / 20% / 50% fastest, and the bottom 50%) — it neutralises the "burst class only gets fast kills" and "sustained class only in slow parties" biases.</li>
<li><b>Same gear</b> uses only players in the most common kit (+6 weapon, Chrono Brooch, +6 armor) — smaller sample, but gear is held constant.</li>
<li>Anonymous players are included in DPS stats but can't be de-duplicated; distinct-player counts are lower bounds.</li>
<li>Gear sections cover parses with a recorded equipment snapshot; coverage is shown in that section.</li>
</ul>
</div>
</section>
</div>
<script>
const D=__DATA__;
const CLS=['Archer','Berserker','Gunner','Ninja','Reaper','Slayer','Sorcerer','Valkyrie','Warrior'];
const AREAS=["Dragon's Landing","TS Hard","TS Savage","SS Hard","SS Savage"];
const fmt=n=>n==null?'–':Math.round(n).toLocaleString('en-US');
const fk=n=>n==null?'–':(n/1000).toFixed(0)+'k';
const f2=n=>n==null?'–':n.toFixed(2);
const rel=v=>v==null?'':(v>=1?'+':'\u2212')+Math.round(Math.abs(v-1)*100)+'%';
const pill=v=>v==null?'':`<span class="pill ${v>=1.05?'pos':v<=0.95?'neg':'mid'}" title="${f2(v)}\u00d7 the typical DPS player on the same boss">${rel(v)}</span>`;
const dur=sec=>sec==null?'-':(sec<60?Math.round(sec)+'s':Math.floor(sec/60)+'m'+(Math.round(sec%60)?' '+Math.round(sec%60)+'s':''));
const durLabel=l=>String(l).replace(/(\d+)\s*-\s*(\d+)s/g,(m,a,b)=>dur(+a)+'–'+dur(+b)).replace(/(?<![\d–])(\d+)s/g,(m,d)=>dur(+d));
// tiles
const ds=D.dataset;
document.getElementById('tiles').innerHTML=[[ds.encounters,'kills'],[ds.five,'DPS parses'],[ds.players,'named players'],[Object.keys(D.killTime).length,'bosses']].map(([v,l])=>`<div class="tile"><b>${fmt(v)}</b><span>${l}</span></div>`).join('');
// lens chart
function barChart(el,rows,key,nkey,note){
  const vals=rows.map(r=>r[1][key]); const lo=Math.min(0.8,...vals), hi=Math.max(1.2,...vals);
  const pct=v=>((v-lo)/(hi-lo)*100);
  el.innerHTML=`<div class="bars"><div class="hdr">class</div><div></div><div class="hdr" style="text-align:right">vs typical</div><div class="hdr" style="text-align:right">${nkey}</div>`+
    rows.sort((a,b)=>b[1][key]-a[1][key]).map(([c,r])=>{const v=r[key];const z=pct(1);const p=pct(v);
      const left=Math.min(z,p),w=Math.abs(p-z);
      return `<div class="lab">${c}</div><div class="track"><div class="zero" style="left:${z}%"></div><div class="fill ${v>=1.03?'pos':v<=0.97?'neg':''}" style="left:${left}%;width:${w}%"></div></div><div class="v" title="${f2(v)}\u00d7">${rel(v)}</div><div class="nn">${r.n}${r.players?' <span style="opacity:.7">/ '+r.players+'</span>':''}</div>`}).join('')+`</div>`;
}
const lenses=[
 {id:'raw',label:'All parses',rows:Object.entries(D.relIndex),key:'avg',nkey:'n / uniq',note:`Average across every parse. Counting each player once at their best parse instead: ${Object.entries(D.relIndex).sort((a,b)=>b[1].playerBestMed-a[1].playerBestMed).map(([c,r])=>c+' '+(r.playerBestMed>=1?'+':'−')+Math.round(Math.abs(r.playerBestMed-1)*100)+'%').join(' · ')}.`},
 {id:'kt',label:'Kill-time matched',rows:Object.entries(D.killTimeIndex).map(([c,r])=>[c,{avg:r.rel,n:r.n,players:D.relIndex[c].players}]),key:'avg',nkey:'n / uniq',note:'Class average ÷ median of the same duration quartile on the same boss, weighted by sample count across all 15 bosses.'},
 {id:'gear',label:'Same gear',rows:Object.entries(D.gear.stdBucket.classes),key:'avg',nkey:'n / uniq',note:`Only players wearing ${D.gear.stdBucket.desc} (${D.gear.stdBucket.n} samples).`},
 {id:'top',label:'Top 10% of players',rows:Object.entries(D.relIndex).map(([c,r])=>[c,{avg:r.top10,n:r.n,players:r.players}]),key:'avg',nkey:'n / uniq',note:'Average index of the best 10% of samples per class — the ceiling, not the typical player.'}
];
const tabs=document.getElementById('lensTabs');
lenses.forEach((L,i)=>{const b=document.createElement('button');b.role='tab';b.textContent=L.label;b.setAttribute('aria-selected',i===0);b.onclick=()=>{[...tabs.children].forEach(x=>x.setAttribute('aria-selected',x===b));barChart(document.getElementById('lensChart'),L.rows.map(r=>[r[0],{...r[1]}]),L.key,L.nkey);document.getElementById('lensNote').textContent=L.note};tabs.appendChild(b)});
tabs.children[0].click();
// area tables
const at=document.getElementById('areaTabs');
function areaTable(a){const rows=Object.entries(D.byArea[a]).sort((x,y)=>y[1].med-x[1].med);
 document.getElementById('areaTable').innerHTML=`<table><thead><tr><th>class</th><th>n</th><th>uniq</th><th>min</th><th>p25</th><th>median</th><th>avg</th><th>p75</th><th>p90</th><th>max</th><th>vs typical</th></tr></thead><tbody>`+
 rows.map(([c,r])=>`<tr><td><b>${c}</b></td><td class="n">${r.n}</td><td class="n">${r.players}</td><td class="n">${fk(r.min)}</td><td class="n">${fk(r.p25)}</td><td><b>${fk(r.med)}</b></td><td>${fk(r.avg)}</td><td class="n">${fk(r.p75)}</td><td>${fk(r.p90)}</td><td>${fk(r.max)}</td><td>${pill(D.relIndexByArea[a][c]&&D.relIndexByArea[a][c].avg)}</td></tr>`).join('')+`</tbody></table>`}
AREAS.forEach((a,i)=>{const b=document.createElement('button');b.role='tab';b.textContent=a;b.setAttribute('aria-selected',i===0);b.onclick=()=>{[...at.children].forEach(x=>x.setAttribute('aria-selected',x===b));areaTable(a)};at.appendChild(b)});
at.children[0].click();
// kill time: pooled across dungeons, one tab per speed group
const ktTabs=document.getElementById('ktTabs');
function ktBucket(i){const B=D.killTimeGlobal[i];
 const rows=Object.entries(B.classes).sort((a,b)=>b[1].rel-a[1].rel);
 barChart(document.getElementById('ktChart'),rows.map(([c,v])=>[c,{avg:v.rel,n:v.n,players:''}]),'avg','kills');
 const tot=rows.reduce((s,r)=>s+r[1].n,0);
 const ns=rows.map(r=>r[1].n), lo=Math.min(...ns), hi=Math.max(...ns);
 const thin=lo<10?` Class samples here run from ${lo} to ${hi} parses — too few to separate the classes, so read the ordering as noise rather than a ranking.`:'';
 document.getElementById('ktNote').textContent=`${tot.toLocaleString()} parses in this tier across ${B.bosses.length} bosses, each measured against the other classes in the same tier on the same boss.`+thin;
 document.getElementById('ktRanges').innerHTML=`<table><thead><tr><th>boss</th><th>kills</th><th>kill times in this tier</th></tr></thead><tbody>`+
  B.bosses.map(r=>`<tr><td>${r.boss.replace('Nightmare ','N. ')}</td><td class="n">${r.n}</td><td>${dur(r.lo)} – ${dur(r.hi)}</td></tr>`).join('')+`</tbody></table>`;
}
D.killTimeGlobal.forEach((B,i)=>{const b=document.createElement('button');b.role='tab';b.textContent=B.label;b.setAttribute('aria-selected',i===0);
 b.onclick=()=>{[...ktTabs.children].forEach(x=>x.setAttribute('aria-selected',x===b));ktBucket(i)};ktTabs.appendChild(b)});
ktBucket(0);
// per-boss detail
const sel=document.getElementById('bossSel');
const bossKeys=Object.keys(D.killTime).sort((a,b)=>D.killTime[b].n-D.killTime[a].n);
bossKeys.forEach(k=>{const o=document.createElement('option');o.value=k;o.textContent=`${k.replace('Nightmare ','N. ')} (${D.killTime[k].n})`;sel.appendChild(o)});
function kt(k){const K=D.killTime[k];document.getElementById('bossN').textContent=`${K.n} parses`;
 const present=CLS.filter(c=>K.buckets.some(b=>b[c]));
 document.getElementById('ktTable').innerHTML=`<table class="heat"><thead><tr><th>class</th>${K.labels.map((l,i)=>`<th>${l}<span class="n" style="display:block;font-weight:400">${K.counts?K.counts[i]+' kills':''}${K.ranges&&K.ranges[i]?' · '+dur(K.ranges[i][0])+'–'+dur(K.ranges[i][1]):''}</span></th>`).join('')}<th>all tiers</th></tr></thead><tbody>`+
 present.map(c=>{const vals=K.buckets.map(b=>b[c]);const have=vals.filter(Boolean);const avg=have.length?have.reduce((s,v)=>s+v.rel*v.n,0)/have.reduce((s,v)=>s+v.n,0):null;
  return `<tr><td><b>${c}</b></td>${vals.map(v=>`<td title="${v?`${v.n} kills · avg ${fk(v.avg)} · best ${fk(v.max)}`:''}">${v?pill(v.rel)+` <span class="n">${v.n}</span>`:''}</td>`).join('')}<td>${pill(avg)}</td></tr>`}).join('')+`</tbody></table>`}
sel.onchange=()=>kt(sel.value);kt(bossKeys[0]);
// gear
document.getElementById('gearCov').textContent=`${D.gear.coverage.withGear.toLocaleString()} of ${D.gear.coverage.of.toLocaleString()} (${Math.round(100*D.gear.coverage.withGear/D.gear.coverage.of)}%)`;
document.getElementById('gearEffect').innerHTML=`<table><thead><tr><th>weapon</th><th>n</th><th>vs typical</th></tr></thead><tbody>`+Object.entries(D.gear.tierEffect).map(([t,r])=>`<tr><td>${t}</td><td class="n">${r.n}</td><td>${pill(r.med)}</td></tr>`).join('')+
 `</tbody></table><table style="margin-top:10px"><thead><tr><th>brooch (+6 weapon only)</th><th>n</th><th>vs typical</th></tr></thead><tbody>`+Object.entries(D.gear.broochEffect).map(([t,r])=>`<tr><td>${t}</td><td class="n">${r.n}</td><td>${pill(r.med)}</td></tr>`).join('')+`</tbody></table>`;
document.getElementById('gearProfile').innerHTML=`<table><thead><tr><th>class</th><th>n</th><th>avg ilvl</th><th>avg wpn</th><th>+7 or better</th><th>chrono</th></tr></thead><tbody>`+Object.entries(D.gear.classGearProfile).sort((a,b)=>b[1].pct7plus-a[1].pct7plus).map(([c,r])=>`<tr><td><b>${c}</b></td><td class="n">${r.n}</td><td>${r.avgIlvl?r.avgIlvl.toFixed(1):'–'}</td><td>+${r.avgWEnch.toFixed(2)}</td><td>${Math.round(r.pct7plus*100)}%</td><td>${Math.round(r.pctChrono*100)}%</td></tr>`).join('')+`</tbody></table>`;
const TIERS=Object.keys(D.gear.tierEffect);
document.getElementById('classTier').innerHTML=`<table><thead><tr><th>class</th>${TIERS.map(t=>`<th>${t.replace(' weapon','')}</th>`).join('')}<th>+6 → +7</th><th>+6 → +8/9</th><th>% per ilvl</th></tr></thead><tbody>`+
 Object.entries(D.gear.classByTier).sort((a,b)=>(b[1].ilvlSlope?b[1].ilvlSlope.perIlvl:0)-(a[1].ilvlSlope?a[1].ilvlSlope.perIlvl:0)).map(([c,r])=>{
  const g=(a,b)=>r[a]&&r[b]?`<b>+${Math.round((r[b].med/r[a].med-1)*100)}%</b>`:'<span class="n">–</span>';
  return `<tr><td><b>${c}</b></td>${TIERS.map(t=>r[t]?`<td>${pill(r[t].med)} <span class="n">${r[t].n}</span></td>`:'<td></td>').join('')}<td>${g('+6 weapon','+7 weapon')}</td><td>${g('+6 weapon','+8/+9 weapon')}</td><td><b>${r.ilvlSlope?(r.ilvlSlope.perIlvl*100).toFixed(1)+'%':'–'}</b> <span class="n">${r.ilvlSlope?r.ilvlSlope.n:''}</span></td></tr>`}).join('')+`</tbody></table>`;
document.getElementById('stdDesc').textContent=D.gear.stdBucket.desc;
const stdTabs=document.getElementById('stdTabs');
const stdSets=[['All dungeons',D.gear.stdBucket.classes,D.gear.stdBucket.n],...AREAS.map(a=>[a,D.gear.stdBucket.byArea[a],Object.values(D.gear.stdBucket.byArea[a]).reduce((s,r)=>s+r.n,0)])];
stdSets.forEach(([label,rows,n],i)=>{const b=document.createElement('button');b.role='tab';b.textContent=label;b.setAttribute('aria-selected',i===0);
 b.onclick=()=>{[...stdTabs.children].forEach(x=>x.setAttribute('aria-selected',x===b));barChart(document.getElementById('stdChart'),Object.entries(rows).map(r=>[r[0],{...r[1]}]),'avg','n / uniq');
 document.getElementById('stdNote').textContent=`${n} samples wearing ${D.gear.stdBucket.desc}${label==='All dungeons'?', all five dungeons pooled':' in '+label}. Index is vs the boss median of all players, so a well-geared group sits above 1.00 on average — read the ordering and the gaps, not the absolute level.`};
 stdTabs.appendChild(b)});
stdTabs.children[0].click();
</script>
"""
html=html.replace("__DATA__",DATA).replace("__D0__",d0).replace("__D1__",d1)
open("report.html","w",encoding="utf-8").write(html)
import os
os.makedirs("tera-dps-balance",exist_ok=True)
open("tera-dps-balance/index.html","w",encoding="utf-8").write('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width"></head><body style="margin:0">'+html+'</body></html>')
print("ok",len(html))
