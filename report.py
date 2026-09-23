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
.patchbar{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 10px}
.patchbtn{flex:1 1 150px;min-width:140px;text-align:left;background:var(--panel);border:1px solid var(--line2);border-radius:7px;padding:9px 12px;cursor:pointer;font:inherit;color:var(--ink2);transition:border-color .12s,background .12s}
.patchbtn:hover{background:var(--heat0)}
.patchbtn[aria-selected=true]{border-color:var(--bar);background:var(--heat0);color:var(--ink);box-shadow:inset 0 0 0 1px var(--bar)}
.patchbtn .pv{font-family:"Barlow Condensed",sans-serif;font-weight:700;font-size:19px;letter-spacing:.01em;color:var(--ink);display:flex;align-items:baseline;gap:6px}
.patchbtn .pv em{font-style:normal;font-size:10.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--bar)}
.patchbtn .pd{font-size:11.5px;color:var(--muted);margin-top:1px}
.patchbtn .pn{font-size:12px;margin-top:4px;font-variant-numeric:tabular-nums}
.patchbtn .chips{display:flex;gap:3px;flex-wrap:wrap;margin-top:6px}
.chip{font-size:10px;font-weight:700;letter-spacing:.03em;padding:1px 5px;border-radius:3px;background:var(--mid-bg);color:var(--ink2)}
.chip.buff{background:var(--pos-bg);color:var(--pos)}
.chip.nerf{background:var(--neg-bg);color:var(--neg)}
.chip.change{background:var(--mid-bg);color:var(--accent)}
.chip.pvp{background:var(--mid-bg);color:var(--muted)}
.tagchg.pvp{background:var(--mid-bg);color:var(--muted)}
.moves{margin-top:9px;padding-top:9px;border-top:1px solid var(--line)}
.moves .mlab{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-right:6px}
.mv{display:inline-block;font-size:13px;font-weight:600;padding:2px 8px;border-radius:4px;margin:2px 4px 2px 0;font-variant-numeric:tabular-nums}
.mv.up{background:var(--pos-bg);color:var(--pos)}
.mv.down{background:var(--neg-bg);color:var(--neg)}
.mv sup{font-size:9px;opacity:.85;margin-left:2px}
.moves .cav{display:block;font-size:12px;color:var(--muted);margin-top:5px}
.patchinfo{border-left:3px solid var(--bar);background:var(--panel);border-radius:0 6px 6px 0;padding:10px 14px;margin:0 0 18px;font-size:14px}
.patchinfo b{color:var(--ink)}
.patchinfo ul{margin:6px 0 0 18px;padding:0}
.patchinfo li{margin:3px 0;color:var(--ink2)}
.tagchg{font-size:9.5px;font-weight:700;letter-spacing:.04em;padding:1px 4px;border-radius:3px;margin-left:5px;vertical-align:1px}
.tagchg.buff{background:var(--pos-bg);color:var(--pos)}
.tagchg.change{background:var(--mid-bg);color:var(--accent)}
.nav{display:flex;gap:14px;font-size:13px;font-weight:600;margin-bottom:14px;flex-wrap:wrap}.nav a{color:var(--ink2);text-decoration:none;border-bottom:2px solid transparent;padding-bottom:2px}.nav a[aria-current]{color:var(--ink);border-color:var(--bar)}
.nav{display:flex;gap:14px;font-size:13px;font-weight:600;margin-bottom:14px}.nav a{color:var(--ink2);text-decoration:none;border-bottom:2px solid transparent;padding-bottom:2px}.nav a[aria-current]{color:var(--ink);border-color:var(--bar)}
</style>
<div class="wrap">
<div class="nav"><a href="../">Home</a><a href="../tera-dps-balance/" aria-current="page">DPS classes</a><a href="../slayer-build/">Slayer build data</a><a href="../slayer-guide/">Slayer guide</a></div>
<div class="eyebrow">TERA Europe Classic+ · public leaderboard API · __D0__ – __D1__</div>
<h1>Classic+ DPS Balance</h1>
<p class="sub">Pick a patch below — class balance changed between them, so pooling every patch together blurs the picture. Everything on this page then reflects that patch only. Data covers every DPS-role player in every recorded 5-man kill of Timescape (Hard/Savage), Shadow Sanguinary (Hard/Savage) and Dragon's Landing. Warriors count only where the game flagged them as DPS rather than tank; healers, tanks and entries under 50k DPS are excluded.</p>
<div class="patchbar" id="patchbar" role="tablist"></div>
<div class="patchinfo" id="patchinfo"></div>
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
<p class="lead">Burst classes look better on fast kills, sustained classes on long ones. Every boss's kills are ranked fastest first and cut into speed tiers. Each class is compared only against the other classes in <b>the same tier on the same boss</b>, so a fast kill is never measured against a slow one. Tiers are cumulative — the top 10% contains the top 5% — which keeps the small tiers usable. Every class is shown with its parse count. <b>One parse per player</b> first reduces each player to their single best parse on each boss, so an unusually active player cannot weight a class; the baseline is rebuilt to match. All five dungeons are pooled here.</p>
<div class="panel">
<div style="display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;justify-content:space-between;margin-bottom:8px">
<div class="tabs" role="tablist" id="ktTabs" style="margin:0"></div>
<label class="hdr" style="cursor:pointer;white-space:nowrap"><input type="checkbox" id="ktBest"> one parse per player</label>
</div>
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
<li><b>Kill-time matched</b> is the same comparison inside speed tiers (top 5% / 10% / 20% / 30% / 40% / 50% fastest, and the bottom 50%) — it neutralises the "burst class only gets fast kills" and "sustained class only in slow parties" biases.</li>
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
function render(){
 const ds=A.dataset;
 for(const id of ['lensTabs','areaTabs','ktTabs']) document.getElementById(id).innerHTML='';
 document.getElementById('bossSel').innerHTML='';
 const ktBestEl=document.getElementById('ktBest');
 document.getElementById('tiles').innerHTML=[[ds.encounters,'kills'],[ds.five,'DPS parses'],[ds.players,'named players'],[Object.keys(A.killTime).length,'bosses']].map(([v,l])=>`<div class="tile"><b>${fmt(v)}</b><span>${l}</span></div>`).join('');
 // lens chart
 function barChart(el,rows,key,nkey,note){
   const vals=rows.map(r=>r[1][key]); const lo=Math.min(0.8,...vals), hi=Math.max(1.2,...vals);
   const pct=v=>((v-lo)/(hi-lo)*100);
   el.innerHTML=`<div class="bars"><div class="hdr">class</div><div></div><div class="hdr" style="text-align:right">vs typical</div><div class="hdr" style="text-align:right">${nkey}</div>`+
     rows.sort((a,b)=>b[1][key]-a[1][key]).map(([c,r])=>{const v=r[key];const z=pct(1);const p=pct(v);
       const left=Math.min(z,p),w=Math.abs(p-z);
       const chg=(D.patchMeta.find(m=>m.id===ACTIVE)||{classes:[]}).classes.find(x=>x.cls===c);
      return `<div class="lab">${c}${chg?`<span class="tagchg ${chg.dir}" title="${chg.text.replace(/"/g,'&quot;')}">${chg.dir==='buff'?'buffed':chg.dir==='nerf'?'nerfed':chg.dir==='pvp'?'PvP only':'changed'}</span>`:''}</div><div class="track"><div class="zero" style="left:${z}%"></div><div class="fill ${v>=1.03?'pos':v<=0.97?'neg':''}" style="left:${left}%;width:${w}%"></div></div><div class="v" title="${f2(v)}\u00d7">${rel(v)}</div><div class="nn">${r.n}${r.players?' <span style="opacity:.7">/ '+r.players+'</span>':''}</div>`}).join('')+`</div>`;
 }
 const lenses=[
  {id:'raw',label:'All parses',rows:Object.entries(A.relIndex),key:'avg',nkey:'n / uniq',note:`Average across every parse. Counting each player once at their best parse instead: ${Object.entries(A.relIndex).sort((a,b)=>b[1].playerBestMed-a[1].playerBestMed).map(([c,r])=>c+' '+(r.playerBestMed>=1?'+':'−')+Math.round(Math.abs(r.playerBestMed-1)*100)+'%').join(' · ')}.`},
  {id:'kt',label:'Kill-time matched',rows:Object.entries(A.killTimeIndex).map(([c,r])=>[c,{avg:r.rel,n:r.n,players:A.relIndex[c].players}]),key:'avg',nkey:'n / uniq',note:'Class average ÷ median of the same duration quartile on the same boss, weighted by sample count across all 15 bosses.'},
  {id:'gear',label:'Same gear',rows:Object.entries(A.gear.stdBucket.classes),key:'avg',nkey:'n / uniq',note:`Only players wearing ${A.gear.stdBucket.desc} (${A.gear.stdBucket.n} samples).`},
  {id:'top',label:'Top 10% of players',rows:Object.entries(A.relIndex).map(([c,r])=>[c,{avg:r.top10,n:r.n,players:r.players}]),key:'avg',nkey:'n / uniq',note:'Average index of the best 10% of samples per class — the ceiling, not the typical player.'}
 ];
 const tabs=document.getElementById('lensTabs');
 lenses.forEach((L,i)=>{const b=document.createElement('button');b.role='tab';b.textContent=L.label;b.setAttribute('aria-selected',i===0);b.onclick=()=>{[...tabs.children].forEach(x=>x.setAttribute('aria-selected',x===b));barChart(document.getElementById('lensChart'),L.rows.map(r=>[r[0],{...r[1]}]),L.key,L.nkey);document.getElementById('lensNote').textContent=L.note};tabs.appendChild(b)});
 tabs.children[0].click();
 // area tables
 const at=document.getElementById('areaTabs');
 function areaTable(a){const vs=c=>(A.relIndexByArea[a]&&A.relIndexByArea[a][c]?A.relIndexByArea[a][c].avg:-1);
  const rows=Object.entries(A.byArea[a]).sort((x,y)=>vs(y[0])-vs(x[0]));
  document.getElementById('areaTable').innerHTML=`<table><thead><tr><th>class</th><th>n</th><th>uniq</th><th>min</th><th>p25</th><th>median</th><th>avg</th><th>p75</th><th>p90</th><th>max</th><th>vs typical</th></tr></thead><tbody>`+
  rows.map(([c,r])=>`<tr><td><b>${c}</b></td><td class="n">${r.n}</td><td class="n">${r.players}</td><td class="n">${fk(r.min)}</td><td class="n">${fk(r.p25)}</td><td><b>${fk(r.med)}</b></td><td>${fk(r.avg)}</td><td class="n">${fk(r.p75)}</td><td>${fk(r.p90)}</td><td>${fk(r.max)}</td><td>${pill(A.relIndexByArea[a][c]&&A.relIndexByArea[a][c].avg)}</td></tr>`).join('')+`</tbody></table>`}
 AREAS.forEach((a,i)=>{const b=document.createElement('button');b.role='tab';b.textContent=a;b.setAttribute('aria-selected',i===0);b.onclick=()=>{[...at.children].forEach(x=>x.setAttribute('aria-selected',x===b));areaTable(a)};at.appendChild(b)});
 at.children[0].click();
 // kill time: pooled across dungeons, one tab per speed group
 const ktTabs=document.getElementById('ktTabs');
 let ktIdx=0;
 function ktBucket(i){ktIdx=i;const best=document.getElementById('ktBest').checked;const B=(best?A.killTimeGlobalBest:A.killTimeGlobal)[i];
  const rows=Object.entries(B.classes).sort((a,b)=>b[1].rel-a[1].rel);
  barChart(document.getElementById('ktChart'),rows.map(([c,v])=>[c,{avg:v.rel,n:v.n,players:''}]),'avg','kills');
  const tot=rows.reduce((s,r)=>s+r[1].n,0);
  const ns=rows.map(r=>r[1].n), lo=Math.min(...ns), hi=Math.max(...ns);
  const thin=lo<10?` Class samples here run from ${lo} to ${hi} — too few to separate the classes, so read the ordering as noise rather than a ranking.`:'';
  const mode=best?`Each player counted once at their best parse per boss. `:'';
  document.getElementById('ktNote').textContent=mode+`${tot.toLocaleString()} ${best?'entries':'parses'} in this tier across ${B.bosses.length} bosses, each measured against the other classes in the same tier on the same boss.`+thin;
  document.getElementById('ktRanges').innerHTML=`<table><thead><tr><th>boss</th><th>kills</th><th>kill times in this tier</th></tr></thead><tbody>`+
   B.bosses.map(r=>`<tr><td>${r.boss.replace('Nightmare ','N. ')}</td><td class="n">${r.n}</td><td>${dur(r.lo)} – ${dur(r.hi)}</td></tr>`).join('')+`</tbody></table>`;
 }
 A.killTimeGlobal.forEach((B,i)=>{const b=document.createElement('button');b.role='tab';b.textContent=B.label;b.setAttribute('aria-selected',i===0);
  b.onclick=()=>{[...ktTabs.children].forEach(x=>x.setAttribute('aria-selected',x===b));ktBucket(i)};ktTabs.appendChild(b)});
 document.getElementById('ktBest').onchange=()=>ktBucket(ktIdx);
 ktBucket(0);
 // per-boss detail
 const sel=document.getElementById('bossSel');
 const bossKeys=Object.keys(A.killTime).sort((a,b)=>A.killTime[b].n-A.killTime[a].n);
 bossKeys.forEach(k=>{const o=document.createElement('option');o.value=k;o.textContent=`${k.replace('Nightmare ','N. ')} (${A.killTime[k].n})`;sel.appendChild(o)});
 function kt(k){const K=A.killTime[k];document.getElementById('bossN').textContent=`${K.n} parses`;
  const present=CLS.filter(c=>K.buckets.some(b=>b[c]));
  document.getElementById('ktTable').innerHTML=`<table class="heat"><thead><tr><th>class</th>${K.labels.map((l,i)=>`<th>${l}<span class="n" style="display:block;font-weight:400">${K.counts?K.counts[i]+' kills':''}${K.ranges&&K.ranges[i]?' · '+dur(K.ranges[i][0])+'–'+dur(K.ranges[i][1]):''}</span></th>`).join('')}<th>all tiers</th></tr></thead><tbody>`+
  present.map(c=>{const vals=K.buckets.map(b=>b[c]);const have=vals.filter(Boolean);const avg=have.length?have.reduce((s,v)=>s+v.rel*v.n,0)/have.reduce((s,v)=>s+v.n,0):null;
   return `<tr><td><b>${c}</b></td>${vals.map(v=>`<td title="${v?`${v.n} kills · avg ${fk(v.avg)} · best ${fk(v.max)}`:''}">${v?pill(v.rel)+` <span class="n">${v.n}</span>`:''}</td>`).join('')}<td>${pill(avg)}</td></tr>`}).join('')+`</tbody></table>`}
 sel.onchange=()=>kt(sel.value);kt(bossKeys[0]);
 // gear
 document.getElementById('gearCov').textContent=`${A.gear.coverage.withGear.toLocaleString()} of ${A.gear.coverage.of.toLocaleString()} (${Math.round(100*A.gear.coverage.withGear/A.gear.coverage.of)}%)`;
 document.getElementById('gearEffect').innerHTML=`<table><thead><tr><th>weapon</th><th>n</th><th>vs typical</th></tr></thead><tbody>`+Object.entries(A.gear.tierEffect).map(([t,r])=>`<tr><td>${t}</td><td class="n">${r.n}</td><td>${pill(r.med)}</td></tr>`).join('')+
  `</tbody></table><table style="margin-top:10px"><thead><tr><th>brooch (+6 weapon only)</th><th>n</th><th>vs typical</th></tr></thead><tbody>`+Object.entries(A.gear.broochEffect).map(([t,r])=>`<tr><td>${t}</td><td class="n">${r.n}</td><td>${pill(r.med)}</td></tr>`).join('')+`</tbody></table>`;
 document.getElementById('gearProfile').innerHTML=`<table><thead><tr><th>class</th><th>n</th><th>avg ilvl</th><th>avg wpn</th><th>+7 or better</th><th>chrono</th></tr></thead><tbody>`+Object.entries(A.gear.classGearProfile).sort((a,b)=>b[1].pct7plus-a[1].pct7plus).map(([c,r])=>`<tr><td><b>${c}</b></td><td class="n">${r.n}</td><td>${r.avgIlvl?r.avgIlvl.toFixed(1):'–'}</td><td>+${r.avgWEnch.toFixed(2)}</td><td>${Math.round(r.pct7plus*100)}%</td><td>${Math.round(r.pctChrono*100)}%</td></tr>`).join('')+`</tbody></table>`;
 const TIERS=Object.keys(A.gear.tierEffect);
 document.getElementById('classTier').innerHTML=`<table><thead><tr><th>class</th>${TIERS.map(t=>`<th>${t.replace(' weapon','')}</th>`).join('')}<th>+6 → +7</th><th>+6 → +8/9</th><th>% per ilvl</th></tr></thead><tbody>`+
  Object.entries(A.gear.classByTier).sort((a,b)=>(b[1].ilvlSlope?b[1].ilvlSlope.perIlvl:0)-(a[1].ilvlSlope?a[1].ilvlSlope.perIlvl:0)).map(([c,r])=>{
   const g=(a,b)=>r[a]&&r[b]?`<b>+${Math.round((r[b].med/r[a].med-1)*100)}%</b>`:'<span class="n">–</span>';
   return `<tr><td><b>${c}</b></td>${TIERS.map(t=>r[t]?`<td>${pill(r[t].med)} <span class="n">${r[t].n}</span></td>`:'<td></td>').join('')}<td>${g('+6 weapon','+7 weapon')}</td><td>${g('+6 weapon','+8/+9 weapon')}</td><td><b>${r.ilvlSlope?(r.ilvlSlope.perIlvl*100).toFixed(1)+'%':'–'}</b> <span class="n">${r.ilvlSlope?r.ilvlSlope.n:''}</span></td></tr>`}).join('')+`</tbody></table>`;
 document.getElementById('stdDesc').textContent=A.gear.stdBucket.desc;
 const stdTabs=document.getElementById('stdTabs');
 const stdSets=[['All dungeons',A.gear.stdBucket.classes,A.gear.stdBucket.n],...AREAS.map(a=>[a,A.gear.stdBucket.byArea[a],Object.values(A.gear.stdBucket.byArea[a]).reduce((s,r)=>s+r.n,0)])];
 stdSets.forEach(([label,rows,n],i)=>{const b=document.createElement('button');b.role='tab';b.textContent=label;b.setAttribute('aria-selected',i===0);
  b.onclick=()=>{[...stdTabs.children].forEach(x=>x.setAttribute('aria-selected',x===b));barChart(document.getElementById('stdChart'),Object.entries(rows).map(r=>[r[0],{...r[1]}]),'avg','n / uniq');
  document.getElementById('stdNote').textContent=`${n} samples wearing ${A.gear.stdBucket.desc}${label==='All dungeons'?', all five dungeons pooled':' in '+label}. Index is vs the boss median of all players, so a well-geared group sits above 1.00 on average — read the ordering and the gaps, not the absolute level.`};
  stdTabs.appendChild(b)});
 stdTabs.children[0].click();
}

// ---- measured movement against the previous patch ----
function moves(m){
  const i=PM.findIndex(x=>x.id===m.id); if(i<1) return '';
  const prev=PM[i-1], A1=D.patches[m.id], A0=D.patches[prev.id];
  if(!A1||!A0) return '';
  // measured on the fastest 20% of kills: those groups clear consistently, so
  // the comparison reflects the class rather than how the run went
  const TIER=2, t1=(A1.killTimeGlobal[TIER]||{}).classes||{}, t0=(A0.killTimeGlobal[TIER]||{}).classes||{};
  const chg=new Set(m.classes.filter(c=>c.dir!=='pvp').map(c=>c.cls));
  const d=Object.keys(t1).filter(c=>t0[c]&&t1[c].n>=50&&t0[c].n>=50)
    .map(c=>[c,(t1[c].rel-t0[c].rel)*100])
    .filter(x=>Math.abs(x[1])>=3).sort((a,b)=>Math.abs(b[1])-Math.abs(a[1])).slice(0,5);
  const lab=`<span class="mlab">Movement vs ${prev.name}, fastest 20% of kills</span>`;
  if(!d.length) return `<div class="moves">${lab}<span class="cav">No class moved by more than 3 points.</span></div>`;
  return `<div class="moves">${lab}`+
   d.map(([c,v])=>`<span class="mv ${v>0?'up':'down'}" title="${c} sits ${Math.abs(v).toFixed(1)} points ${v>0?'higher':'lower'} against the median player than in ${prev.name}, measured on the fastest 20% of kills">${c} ${v>0?'+':'\u2212'}${Math.abs(v).toFixed(0)}${chg.has(c)?'<sup>\u25cf</sup>':''}</span>`).join('')+
   `<span class="cav">Measured on the fastest 20% of kills on each boss, where runs go to plan and the result reflects the class more than the circumstances. Figures are points of the vs-typical number, on a relative scale \u2014 one class climbing pushes the rest down.${d.some(([c])=>chg.has(c))?' \u25cf marks a class this patch changed directly.':''}</span></div>`;
}

// ---- patch selector ----
const PM=D.patchMeta.filter(m=>m.parses>0);
const DATES={};
PM.forEach(m=>{DATES[m.id]=m.start?new Date(m.start).toLocaleDateString('en-GB',{day:'numeric',month:'short'}):'from launch'});
const pbar=document.getElementById('patchbar');
function setPatch(id){
  ACTIVE=id;
  A=(id==='all')?D:D.patches[id];
  [...pbar.children].forEach(b=>b.setAttribute('aria-selected',String(b.dataset.id===id)));
  const m=PM.find(x=>x.id===id);
  const info=document.getElementById('patchinfo');
  if(!m){
    info.innerHTML=`<b>All data.</b> Every recorded kill from ${PM.map(x=>x.id).join(', ')} pooled together. Useful for sample size, but class balance changed between these patches \u2014 pick a single patch to read the standings cleanly.`;
  }else{
    const cls=m.classes.length?`<ul>${m.classes.map(c=>`<li><b>${c.cls}</b> \u2014 ${c.text}</li>`).join('')}</ul>`
      :'<ul><li>No DPS-class changes in this patch.</li></ul>';
    const con=m.content.length?`<ul>${m.content.map(t=>`<li>${t}</li>`).join('')}</ul>`:'';
    info.innerHTML=`<b>${m.name}${m.current?' \u2014 current':''}.</b> ${m.summary}`+cls+
      (con?`<div style="margin-top:6px;font-size:13px;color:var(--muted)">Encounter changes that move kill times:</div>${con}`:'')+moves(m);
  }
  render();
}
pbar.innerHTML=PM.map(m=>{
  const chips=m.classes.map(c=>`<span class="chip ${c.dir}" title="${c.text.replace(/"/g,'&quot;')}">${c.cls}${c.dir==='pvp'?' (PvP)':''}</span>`).join('')||'<span class="chip">no class changes</span>';
  return `<button class="patchbtn" role="tab" data-id="${m.id}" aria-selected="false">
    <span class="pv">${m.name}${m.current?' <em>current</em>':''}</span>
    <span class="pd">${DATES[m.id]}${m.end?' \u2013 '+new Date(m.end).toLocaleDateString('en-GB',{day:'numeric',month:'short'}):' onward'}</span>
    <span class="pn">${m.parses.toLocaleString()} parses \u00b7 ${m.kills.toLocaleString()} kills</span>
    <span class="chips">${chips}</span></button>`}).join('')+
 `<button class="patchbtn" role="tab" data-id="all" aria-selected="false">
    <span class="pv">All data</span><span class="pd">every patch pooled</span>
    <span class="pn">${D.dataset.five.toLocaleString()} parses \u00b7 ${D.dataset.encounters.toLocaleString()} kills</span>
    <span class="chips"><span class="chip change">mixes balance changes</span></span></button>`;
[...pbar.children].forEach(b=>b.onclick=()=>setPatch(b.dataset.id));
setPatch((PM.find(m=>m.current)||PM[PM.length-1]||{id:'all'}).id);
</script>
"""
html=html.replace("__DATA__",DATA).replace("__D0__",d0).replace("__D1__",d1)
open("report.html","w",encoding="utf-8").write(html)
import os
os.makedirs("tera-dps-balance",exist_ok=True)
open("tera-dps-balance/index.html","w",encoding="utf-8").write('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width"></head><body style="margin:0">'+html+'</body></html>')
print("ok",len(html))
