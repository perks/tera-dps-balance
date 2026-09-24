import json,datetime
D=json.load(open("final.json",encoding="utf-8"))
ds=D["dataset"]
d0=datetime.datetime.utcfromtimestamp(ds["dateFrom"]).strftime("%b %d"); d1=datetime.datetime.utcfromtimestamp(ds["dateTo"]).strftime("%b %d, %Y")
DATA=json.dumps(D,ensure_ascii=False)
html = r"""<title>Classic+ DPS Balance</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
:root{color-scheme:light;
 --bg:#e8e5df;--panel:#f3f1ed;--ink:#282c31;--ink2:#5d646d;--muted:#8d939b;--line:#dcd7cf;--line2:#c6c0b6;
 --bar:#4a7fb0;--bar-soft:#cdddea;--pos:#4a8a68;--neg:#b5604f;--pos-bg:#dae8e0;--neg-bg:#f0ddd7;--mid-bg:#e3e1db;--accent:#a8713c;--heat0:#e3e0d9;--heat1:#4a7fb0}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){color-scheme:dark;
 --bg:#1d2126;--panel:#252a31;--ink:#e3e6e9;--ink2:#a6aeb8;--muted:#79818c;--line:#333942;--line2:#434b55;
 --bar:#6098cc;--bar-soft:#2c4560;--pos:#5fb089;--neg:#d2836e;--pos-bg:#24382f;--neg-bg:#3d2a24;--mid-bg:#2d323a;--accent:#c9925c;--heat0:#2a2f36;--heat1:#6098cc}}
:root[data-theme="dark"]{color-scheme:dark;
 --bg:#1d2126;--panel:#252a31;--ink:#e3e6e9;--ink2:#a6aeb8;--muted:#79818c;--line:#333942;--line2:#434b55;
 --bar:#6098cc;--bar-soft:#2c4560;--pos:#5fb089;--neg:#d2836e;--pos-bg:#24382f;--neg-bg:#3d2a24;--mid-bg:#2d323a;--accent:#c9925c;--heat0:#2a2f36;--heat1:#6098cc}
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
.bpwrap{display:grid;grid-template-columns:96px 1fr 72px;gap:2px 12px;align-items:center;font-size:14px}
.bpwrap .hd{font-size:10.5px;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);font-weight:600;padding-bottom:2px}
.bp{position:relative;height:26px}
.bp .whisk{position:absolute;top:12px;height:2px;background:var(--line2);border-radius:1px}
.bp .cap{position:absolute;top:7px;width:2px;height:12px;background:var(--line2);border-radius:1px}
.bp .box{position:absolute;top:5px;height:16px;background:var(--bar-soft);border:1px solid var(--bar);border-radius:3px}
.bp .med{position:absolute;top:3px;width:3px;height:20px;background:var(--bar);border-radius:2px}
.bp .p90{position:absolute;top:8px;width:2px;height:10px;background:var(--accent);opacity:.7;border-radius:1px}
.bp .best{position:absolute;top:9px;width:8px;height:8px;background:var(--accent);border-radius:50%;margin-left:-4px}
.bpname{font-weight:600;white-space:nowrap}
.bpval{text-align:right;font-variant-numeric:tabular-nums;font-weight:600}
.bpaxis{display:grid;grid-template-columns:96px 1fr 72px;gap:12px;margin-top:4px;font-size:11px;color:var(--muted)}
.bpaxis .ticks{display:flex;justify-content:space-between;font-variant-numeric:tabular-nums}
.legendrow{display:flex;gap:16px;flex-wrap:wrap;font-size:12px;color:var(--ink2);margin-top:14px;align-items:center}
.legendrow i{display:inline-block;vertical-align:middle;margin-right:5px}
.lg-box{width:22px;height:11px;background:var(--bar-soft);border:1px solid var(--bar);border-radius:2px}
.lg-med{width:3px;height:13px;background:var(--bar);border-radius:2px}
.lg-whisk{width:22px;height:2px;background:var(--line2)}
.lg-p90{width:2px;height:11px;background:var(--accent);opacity:.7}
.lg-best{width:8px;height:8px;background:var(--accent);border-radius:50%}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;background:var(--line);
 border:1px solid var(--line);border-radius:8px;overflow:hidden;margin:0 0 18px}
.kpi{background:var(--panel);padding:12px 14px}
.kpi .k{font-size:10px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);font-weight:600}
.kpi .v{font-size:23px;font-weight:700;color:var(--ink);line-height:1.25;font-variant-numeric:tabular-nums}
.kpi .s{font-size:12px;color:var(--ink2)}
td.thin{opacity:.55}
.onlycur{display:inline-block;vertical-align:middle;margin-left:9px;padding:3px 8px;border-radius:5px;
 font-size:10.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
 background:var(--bar-soft);color:var(--bar);border:1px solid var(--bar)}
.blocked{border:1px solid var(--line2);background:var(--panel);border-radius:8px;padding:16px 18px;font-size:14px;line-height:1.55;color:var(--ink2)}
.blocked b{color:var(--ink)}
.blocked .h{display:block;font-size:15px;font-weight:700;color:var(--ink);margin-bottom:6px}
.disclaim{display:flex;gap:11px;align-items:flex-start;border:1px solid var(--neg);
 background:var(--neg-bg);border-radius:8px;padding:12px 14px;margin:0 0 15px;font-size:13.5px;line-height:1.5;color:var(--ink)}
.disclaim .ic{flex:0 0 auto;width:20px;height:20px;border-radius:50%;background:var(--neg);color:#fff;
 font-size:13px;font-weight:700;display:flex;align-items:center;justify-content:center;margin-top:1px}
.disclaim b{color:var(--neg)}
.disclaim .sub{display:block;margin-top:3px;color:var(--ink2);font-size:12.5px}
.tabs button .warn{margin-left:5px;color:var(--neg);font-weight:700}
.tabs button[aria-selected="true"] .warn{color:inherit;opacity:.85}
.lab .tagthin{display:inline-block;margin-left:6px;padding:1px 5px;border-radius:4px;font-size:10px;
 font-weight:700;letter-spacing:.04em;text-transform:uppercase;background:var(--neg-bg);color:var(--neg);border:1px solid var(--neg)}
td.thin .np{color:var(--neg)}
.np{display:block;font-style:normal;font-size:10.5px;color:var(--muted);font-variant-numeric:tabular-nums}
th.sortable{cursor:pointer;user-select:none}
th.sortable.on{color:var(--bar)}
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
<div class="eyebrow">TERA Europe Classic+ · public leaderboard API · <span id="eyeRange">__D0__ – __D1__</span></div>
<h1>Classic+ DPS Balance</h1>
<p class="sub">Pick a patch below — class balance changed between them, so pooling every patch together blurs the picture. Everything on this page then reflects that patch only. Data covers every DPS-role player in every recorded 5-man kill of Timescape (Hard/Savage), Shadow Sanguinary (Hard/Savage) and Dragon's Landing. Warriors count only where the game flagged them as DPS rather than tank; healers, tanks and entries under 50k DPS are excluded, as are the 1.6% of kills that ran without any tank at all, where somebody is tanking on a DPS character.</p>
<div class="patchbar" id="patchbar" role="tablist"></div>
<div class="patchinfo" id="patchinfo"></div>
<div class="tiles" id="tiles"></div>

<section>
<h2>How each class performs</h2>
<p class="lead">The spread of every recorded parse, not just the middle. The box covers the middle half of parses, the line inside it is the median, the whisker runs from the weakest parse out to the 90th percentile, and the dot is the best pull on record. Pick a dungeon and boss to compare like with like.</p>
<div class="panel">
<div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:14px">
<label for="distSel" class="hdr">Dungeon</label><select id="distSel"></select>
<label for="distBoss" class="hdr">Boss</label><select id="distBoss"></select>
<span class="n" id="distN"></span></div>
<div class="kpis" id="distKpis"></div>
<div class="bpwrap" id="boxplot"></div>
<div class="bpaxis"><div></div><div class="ticks" id="bpticks"></div><div></div></div>
<div class="legendrow">
<span><i class="lg-whisk"></i>weakest to 90th percentile</span>
<span><i class="lg-box"></i>middle half</span>
<span><i class="lg-med"></i>median</span>
<span><i class="lg-p90"></i>90th percentile</span>
<span><i class="lg-best"></i>best recorded</span>
</div>
<div class="tscroll" id="distTable" style="margin-top:18px"></div>
<p class="legend">Floor is the weakest parse on record and is usually a wipe-adjacent pull, not a typical one — read the median and the box first. Crit and deaths are averages over the same parses.</p>
</div>
</section>

<section>
<h2>Where each class stands</h2>
<p class="lead">Every figure shows <b>how far above or below the typical DPS player</b> a class sits on the same boss, so a Savage kill and a Dragon's Landing kill are on one scale. <b>+10% means 10% more damage than the median player on that boss.</b> Three lenses: every parse, kill-time matched, and the top 10% of players.</p>
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
<h2>Gear-equalised comparison <span class="onlycur" id="gmOnly">current patch only</span></h2>
<p class="lead">Damage enchanting on this server concentrates in the <b>weapon and the gloves</b>, so that pair says most of what there is to say about how far along someone's gear is. Every class here is compared only against the classes in <b>the same dungeon boss at the same two enchant levels</b> — a +6/+6 parse is never measured against a +8/+8 one. <span class="n" id="gmMeta"></span></p>
<div id="gmBlock"></div>
<div class="panel" id="gmPanel">
<div class="tabs" role="tablist" id="gmTabs"></div>
<div id="gmWarn"></div>
<div id="gmChart"></div>
<p class="note" id="gmNote"></p>
</div>
<details id="gmDetails"><summary>Every enchant level side by side</summary><div class="inner">
<div class="tscroll" id="gmTable"></div>
<p class="legend">Each column compares classes only within that exact level, so columns are independent of one another and should not be read as a progression for one player. <b>n</b> is parses, <b>p</b> distinct players. A figure resting on fewer than <span id="gmMin"></span> players is greyed — at the top of the ladder a class is often one or two people, and that is individual skill rather than class balance.</p>
</div></details>
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
const fk=n=>n==null?'–':n>=1e6?(n/1e6).toFixed(2)+'M':(n/1000).toFixed(0)+'k';
const f2=n=>n==null?'–':n.toFixed(2);
const rel=v=>v==null?'':(v>=1?'+':'\u2212')+Math.round(Math.abs(v-1)*100)+'%';
const pill=v=>v==null?'':`<span class="pill ${v>=1.05?'pos':v<=0.95?'neg':'mid'}" title="${f2(v)}\u00d7 the typical DPS player on the same boss">${rel(v)}</span>`;
const dur=sec=>sec==null?'-':(sec<60?Math.round(sec)+'s':Math.floor(sec/60)+'m'+(Math.round(sec%60)?' '+Math.round(sec%60)+'s':''));
const durLabel=l=>String(l).replace(/(\d+)\s*-\s*(\d+)s/g,(m,a,b)=>dur(+a)+'–'+dur(+b)).replace(/(?<![\d–])(\d+)s/g,(m,d)=>dur(+d));
// KPI helpers: both follow whichever patch is selected
function lastKill(){const t=A.dataset&&A.dataset.dateTo;
  return t?new Date(t*1000).toLocaleDateString('en-GB',{day:'numeric',month:'short'}):'–'}
function patchLabel(){const m=PM.find(x=>x.id===ACTIVE);return m?m.name+(m.current?' (current)':''):'all patches pooled'}
// The header range has to describe the selected patch. Left static it claimed
// the whole dataset's span while a single patch was showing.
function rangeOf(ds){
  if(!ds||!ds.dateFrom||!ds.dateTo) return '';
  const f=d=>new Date(d*1000).toLocaleDateString('en-GB',{day:'2-digit',month:'short'});
  return `${f(ds.dateFrom)} – ${f(ds.dateTo)}, ${new Date(ds.dateTo*1000).getFullYear()}`;
}
function render(){
 const ds=A.dataset;
 { const el=document.getElementById('eyeRange'), r=rangeOf(ds); if(el&&r) el.textContent=r; }
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

 // ---- gear-equalised ----
 const GM=A.gearMatch;
 // Enchant levels only mean something on the live patch, so on any other
 // selection the tables are withheld rather than shown with a caveat.
 const gmOK=GM&&GM.reliable&&GM.overall&&Object.keys(GM.overall).length;
 document.getElementById('gmPanel').style.display=gmOK?'':'none';
 document.getElementById('gmDetails').style.display=gmOK?'':'none';
 document.getElementById('gmOnly').style.display=gmOK?'':'none';
 document.getElementById('gmBlock').innerHTML=gmOK?'':
   `<div class="blocked"><span class="h">Not shown for ${ACTIVE==='all'?'the pooled view':((PM.find(m=>m.id===ACTIVE)||{}).name||'this selection')}</span>`+
   `${ACTIVE==='all'?'Pooling every patch mixes that period back in, so the same caveat applies. ':''}${(GM&&GM.note)||''} `+
   `Select <b>${(PM.find(m=>m.current)||{}).name||'the current patch'}</b> to see it.`+
   `<span style="display:block;margin-top:8px;font-size:12.5px;color:var(--muted)">`+
   `Every other section on this page is unaffected and reports the patch you have selected — only the enchant-keyed comparison is withheld.</span></div>`;
 if(gmOK){
  document.getElementById('gmMeta').textContent=
    `${GM.n.toLocaleString()} parses across ${GM.cells} boss+gear cells · enchanting runs to +12, but the highest recorded here is +${GM.maxWeapon} weapon and +${GM.maxGloves} gloves`;
  document.getElementById('gmMin').textContent=GM.minPlayers;
  const skip=(GM.skipped||[]).map(k=>`${k.short} (${k.n.toLocaleString()} parses but only ${k.players} players)`).join(', ');
  const views=[{label:'All levels',cl:GM.overall,players:0,
      note:'Every parse, each measured against its own boss at its own exact enchant level, then pooled. Use the level tabs to see one level on its own.'}]
    .concat(GM.exact.map(e=>({label:e.short,cl:e.classes,players:e.players,
      note:`${e.label} — ${e.n.toLocaleString()} parses from ${e.players} players, ${Object.keys(e.classes).length} classes with enough data.`})));
  // open on the level the most players actually sit at, not whichever comes first
  let DEF=0; views.forEach((v,i)=>{if(v.players>views[DEF].players) DEF=i});
  const gt=document.getElementById('gmTabs');
  function drawGM(v){
   const rows=Object.entries(v.cl).map(([c,r])=>[c,{avg:r.rel,n:r.n,players:r.players}]);
   barChart(document.getElementById('gmChart'),rows,'avg','n / uniq');
   const thin=Object.entries(v.cl).filter(([,r])=>r.thin).map(([c])=>c);
   // Mark the thin classes on the bars themselves, so the caveat travels with
   // the number instead of sitting in a paragraph underneath it.
   document.querySelectorAll('#gmChart .lab').forEach(el=>{
     const c=el.firstChild.textContent.trim();
     const r=v.cl[c];
     if(r&&r.thin) el.insertAdjacentHTML('beforeend',
       `<span class="tagthin" title="${r.players} players">${r.players} player${r.players===1?'':'s'}</span>`);
   });
   const w=document.getElementById('gmWarn');
   if(thin.length){
    const most=thin.length===Object.keys(v.cl).length;
    w.innerHTML=`<div class="disclaim"><div class="ic">!</div><div>`+
      `<b>Small sample — read this as players, not classes.</b> `+
      `${most?'Every class shown here rests':thin.length+' of '+Object.keys(v.cl).length+' classes shown here rest'} on fewer than ${GM.minPlayers} people`+
      ` (${thin.map(c=>c+' '+v.cl[c].players).join(', ')}).`+
      ` Few people have reached this level, so a figure moves with who those individuals are and how they play. Parse count does not fix it: the same handful of players parsing repeatedly still only measures that handful.`+
      `<span class="sub">The +${GM.exact.length?GM.exact.reduce((a,b)=>a.players>b.players?a:b).level:6} tab is the one to trust for class balance.</span>`+
      `</div></div>`;
   } else w.innerHTML='';
   document.getElementById('gmNote').innerHTML=v.note+
     (skip?` <b>Not shown:</b> ${skip} — too few people at that level to say anything about a class.`:'');
  }
  gt.innerHTML='';
  views.forEach((v,i)=>{const b=document.createElement('button');b.role='tab';
    const anyThin=Object.values(v.cl).some(r=>r.thin);
    b.innerHTML=v.label+(anyThin?'<span class="warn" title="small sample">⚠</span>':'');
    b.setAttribute('aria-selected',String(i===DEF));
    b.onclick=()=>{[...gt.children].forEach(x=>x.setAttribute('aria-selected',String(x===b)));drawGM(v)};
    gt.appendChild(b)});
  drawGM(views[DEF]);

  const lv=GM.exact;
  const cls=[...new Set(lv.flatMap(e=>Object.keys(e.classes)))]
    .sort((a,b)=>(GM.overall[b]?GM.overall[b].rel:0)-(GM.overall[a]?GM.overall[a].rel:0));
  document.getElementById('gmTable').innerHTML=
   `<table><thead><tr><th>class</th>`+lv.map(e=>`<th>${e.short} <span class="n">${e.players}p</span></th>`).join('')+`</tr></thead><tbody>`+
   cls.map(c=>`<tr><td><b>${c}</b></td>`+lv.map(e=>{const r=e.classes[c];
     if(!r) return '<td class="n">–</td>';
     return `<td class="${r.thin?'thin':''}" title="${r.n} parses, ${r.players} players">${rel(r.rel)}<i class="np">${r.n}n / ${r.players}p</i></td>`}).join('')+`</tr>`).join('')+
   `</tbody></table>`;
 }
 // ---- distribution box plots ----
 const distSel=document.getElementById('distSel'), distBoss=document.getElementById('distBoss');
 function bossesFor(a){return Object.keys(A.byBoss).filter(k=>k.indexOf(a+" / ")===0)}
 function drawDist(){
  const a=distSel.value, b=distBoss.value;
  const src=(b&&A.byBoss[b])?A.byBoss[b]:A.byArea[a];
  const box=document.getElementById('boxplot');
  if(!src||!Object.keys(src).length){box.innerHTML='';document.getElementById('distN').textContent='Not enough parses here.';document.getElementById('distTable').innerHTML='';document.getElementById('bpticks').innerHTML='';document.getElementById('distKpis').innerHTML='';return}
  const rows=Object.entries(src).sort((x,y)=>y[1].med-x[1].med);
  const hi=Math.max(...rows.map(r=>r[1].max));
  const pc=v=>100*v/hi;
  document.getElementById('distN').textContent=rows.reduce((s,r)=>s+r[1].n,0).toLocaleString()+' parses across '+rows.length+' classes';
  box.innerHTML='<div class="hd">class</div><div class="hd">DPS distribution</div><div class="hd" style="text-align:right">median</div>'+
   rows.map(([c,r])=>'<div class="bpname">'+c+'</div><div class="bp" title="'+c+' \u2014 floor '+fk(r.min)+', Q1 '+fk(r.p25)+', median '+fk(r.med)+', Q3 '+fk(r.p75)+', P90 '+fk(r.p90)+', best '+fk(r.max)+' ('+r.n+' parses)">'+
    '<div class="whisk" style="left:'+pc(r.min)+'%;width:'+Math.max(0.4,pc(r.p90)-pc(r.min))+'%"></div>'+
    '<div class="cap" style="left:'+pc(r.min)+'%"></div>'+
    '<div class="box" style="left:'+pc(r.p25)+'%;width:'+Math.max(0.8,pc(r.p75)-pc(r.p25))+'%"></div>'+
    '<div class="med" style="left:'+pc(r.med)+'%"></div>'+
    '<div class="p90" style="left:'+pc(r.p90)+'%"></div>'+
    '<div class="best" style="left:'+pc(r.max)+'%"></div></div>'+
    '<div class="bpval">'+fk(r.med)+'</div>').join('');
  const bestRow=rows.slice().sort((x,y)=>y[1].max-x[1].max)[0];
  const medRow=rows[0];
  const logs=rows.reduce((s,r)=>s+r[1].n,0), uniq=rows.reduce((s,r)=>s+r[1].players,0);
  const kpi=(k,v,sub)=>'<div class="kpi"><div class="k">'+k+'</div><div class="v">'+v+'</div><div class="s">'+sub+'</div></div>';
  document.getElementById('distKpis').innerHTML=
    kpi('best recorded',fk(bestRow[1].max),bestRow[0])+
    kpi('highest median',fk(medRow[1].med),medRow[0])+
    kpi('parses analysed',logs.toLocaleString(),rows.length+' classes')+
    kpi('latest kill',lastKill(),patchLabel());
  let t='';for(let i=0;i<=5;i++) t+='<span>'+fk(hi*i/5)+'</span>';
  document.getElementById('bpticks').innerHTML=t;
  const cols=[['cls','class'],['n','parses'],['min','floor'],['p25','Q1'],['med','median'],['p75','Q3'],['p90','P90'],['max','best'],['avg','average'],['crit','crit'],['deaths','deaths']];
  let sortKey='med',desc=true;
  function paint(){
   const sorted=rows.slice().sort((x,y)=>{const va=sortKey==='cls'?x[0]:x[1][sortKey],vb=sortKey==='cls'?y[0]:y[1][sortKey];return (va<vb?-1:va>vb?1:0)*(desc?-1:1)});
   document.getElementById('distTable').innerHTML='<table><thead><tr>'+
    cols.map(([k,l])=>'<th class="sortable'+(k===sortKey?' on':'')+'" data-k="'+k+'">'+l+(k===sortKey?(desc?' \u2193':' \u2191'):'')+'</th>').join('')+
    '</tr></thead><tbody>'+sorted.map(([c,r])=>'<tr><td><b>'+c+'</b></td><td class="n">'+r.n+'</td><td class="n">'+fk(r.min)+'</td><td>'+fk(r.p25)+'</td><td><b>'+fk(r.med)+'</b></td><td>'+fk(r.p75)+'</td><td>'+fk(r.p90)+'</td><td>'+fk(r.max)+'</td><td class="n">'+fk(r.avg)+'</td><td class="n">'+(r.crit==null?'–':r.crit.toFixed(0)+'%')+'</td><td class="n">'+(r.deaths==null?'–':r.deaths.toFixed(1))+'</td></tr>').join('')+'</tbody></table>';
   document.querySelectorAll('#distTable th.sortable').forEach(th=>th.onclick=()=>{const k=th.dataset.k;if(k===sortKey)desc=!desc;else{sortKey=k;desc=true;}paint();});
  }
  paint();
 }
 function syncBoss(){
  const bs=bossesFor(distSel.value);
  distBoss.innerHTML='<option value="">All bosses</option>'+bs.map(b=>'<option value="'+b+'">'+b.split(' / ')[1].replace('Nightmare ','N. ')+'</option>').join('');
  drawDist();
 }
 distSel.innerHTML=AREAS.filter(a=>A.byArea[a]&&Object.keys(A.byArea[a]).length).map(a=>'<option>'+a+'</option>').join('');
 distSel.onchange=syncBoss; distBoss.onchange=drawDist;
 syncBoss();
}

// ---- measured movement against the previous patch ----
function moves(m){
  const i=PM.findIndex(x=>x.id===m.id); if(i<1) return '';
  const prev=PM[i-1], A1=D.patches[m.id], A0=D.patches[prev.id];
  if(!A1||!A0||!A1.moveIndex||!A0.moveIndex) return '';
  const t1=A1.moveIndex, t0=A0.moveIndex;
  const chg=new Set(m.classes.filter(c=>c.dir!=='pvp').map(c=>c.cls));
  const d=Object.keys(t1).filter(c=>t0[c]&&t1[c].n>=30&&t0[c].n>=30)
    .map(c=>[c,(t1[c].rel-t0[c].rel)*100])
    .filter(x=>Math.abs(x[1])>=3).sort((a,b)=>Math.abs(b[1])-Math.abs(a[1])).slice(0,5);
  const lab=`<span class="mlab">Movement vs ${prev.name} \u00b7 fastest 10% of kills</span>`;
  if(!d.length) return `<div class="moves">${lab}<span class="cav">No class moved by more than 3 points.</span></div>`;
  return `<div class="moves">${lab}`+
   d.map(([c,v])=>`<span class="mv ${v>0?'up':'down'}" title="${c}: ${Math.abs(v).toFixed(1)} points ${v>0?'higher':'lower'} than in ${prev.name}, across the fastest 10% of kills on each boss">${c} ${v>0?'+':'\u2212'}${Math.abs(v).toFixed(0)}${chg.has(c)?'<sup>\u25cf</sup>':''}</span>`).join('')+
   `<span class="cav">Taken from the fastest 10% of kills on each boss \u2014 the end of the ladder where groups are geared and executing, which is the population a balance change is best judged on. Gear is not held constant, so some of the shift reflects upgrades as well as the patch. Figures are points on a relative scale, so one class climbing pushes the rest down.${d.some(([c])=>chg.has(c))?' \u25cf marks a class this patch changed directly.':''}</span></div>`;
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
