import json,datetime,re
D=json.load(open("tank.json",encoding="utf-8"))
ds=D["dataset"]
d0=datetime.datetime.utcfromtimestamp(ds["dateFrom"]).strftime("%b %d"); d1=datetime.datetime.utcfromtimestamp(ds["dateTo"]).strftime("%b %d, %Y")
DATA=json.dumps(D,ensure_ascii=False)
css=re.search(r"<style>(.*?)</style>",open("report.py",encoding="utf-8").read(),re.S).group(1)
html = r"""<title>Classic+ Tank Balance</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<style>__CSS__
.nav{display:flex;gap:14px;font-size:13px;font-weight:600;margin-bottom:14px}.nav a{color:var(--ink2);text-decoration:none;border-bottom:2px solid transparent;padding-bottom:2px}.nav a[aria-current]{color:var(--ink);border-color:var(--bar)}
.verdict{display:grid;grid-template-columns:28px 1fr;gap:6px 10px;align-items:start;font-size:14px}.verdict .ok{color:var(--pos);font-weight:700}.verdict .bad{color:var(--neg);font-weight:700}.verdict .warn{color:var(--accent);font-weight:700}
</style>
<div class="wrap">
<div class="nav"><a href="index.html">DPS classes</a><a href="tanks.html" aria-current="page">Tanks</a></div>
<div class="eyebrow">TERA Europe Classic+ · public leaderboard API · __D0__ – __D1__</div>
<h1>Classic+ Tank Balance</h1>
<p class="sub">Every tank in every recorded 5-man kill of Timescape (Hard/Savage), Shadow Sanguinary (Hard/Savage) and Dragon's Landing — personal DPS, and raid DPS (rDPS): how much more the party's DPS players do when this tank is in the group. Warriors and Berserkers count only when the meter flagged them as the tank.</p>
<div class="tiles" id="tiles"></div>

<section>
<h2>Verdict on the rDPS report</h2>
<p class="lead">The reviewed workbook (31,905 tank parses, 11 dungeons) models rDPS = personal DPS + teammate DPS × (M−1)/M, where M is a buff multiplier built from skill values × uptime. The structure is sound; several inputs are not. Checked against the game's own abnormality metadata and buff uptimes recorded in these 1,592 kills:</p>
<div class="panel">
<div class="verdict">
<span class="ok">OK</span><span><b>(M−1)/M attribution</b> avoids double-counting, and standardising teammate DPS per boss removes the "Lancers get better parties" confound. Median-of-bosses is a fair aggregation.</span>
<span class="ok">OK</span><span><b>Brawler has no offensive party buff.</b> No party-wide Power / attack-speed / damage abnormality sourced from Brawler appears in the metadata or in any teammate's buff log.</span>
<span class="bad">NO</span><span><b>Traverse Cut is self-only.</b> The model credits Warrior tanks with +11.7% party attack speed at 74% uptime. Teammates in Warrior-tank parties carry the buff 0% of the time (it appears only on DPS Warriors themselves). Warrior's utility is the Endurance debuff only.</span>
<span class="bad">NO</span><span><b>Berzerker's Lead at 100% four-stack uptime.</b> Measured on teammates: <span id="vLead"></span> median. Berserker's modeled Power contribution is ~5× too high.</span>
<span class="warn">LOW</span><span><b>Lancer uptimes are overstated.</b> Guardian Power on teammates: model 54.6%, measured <span id="vGP"></span>. Adrenaline Rush: model 29.3%, measured <span id="vAR"></span>. Debilitate: model 99%, measured <span id="vDeb"></span>. (Adrenaline Rush II in this build is +20% AS / <b>+10%</b> damage, not +5%.)</span>
<span class="warn">?</span><span><b>"+30 Power = +30% damage"</b> is an assumption the report flags itself. It is the single largest term in Lancer's multiplier. Rather than resolve it from formulas, the section below measures the total teammate uplift directly.</span>
<span class="warn">?</span><span><b>Endurance debuffs don't stack across sources.</b> A DPS Warrior applies Combative Strike anyway; one is present in <span id="vDW"></span> of these kills, making the tank's debuff redundant there.</span>
<span class="warn">SCOPE</span><span><b>Different content.</b> The workbook's 31,905 parses are dominated by Heaven's Arena, Red Refuge and Lakan's Prison; it holds only ~580 tank rows across these five dungeons (and 0–7 for Brawler in three of them) because the solo board returns ~1 of 3 party members. Encounter detail returns everyone: 1,592 tank samples here.</span>
</div>
<h3 style="margin-top:16px">Model inputs vs measured uptime (share of fight time on teammates)</h3>
<div class="tscroll" id="inputs"></div>
</div>
</section>

<section>
<h2>Where each tank stands</h2>
<p class="lead">Personal DPS ÷ <b>median tank DPS on that boss</b> (all tank classes pooled); 1.00 = typical tank. Teammate lift and rDPS lenses are explained in the raid-contribution section.</p>
<div class="panel">
<div class="tabs" role="tablist" id="lensTabs"></div>
<div id="lensChart"></div>
<p class="note" id="lensNote"></p>
</div>
</section>

<section>
<h2>Raid contribution (rDPS)</h2>
<p class="lead">Instead of assuming buff values, measure the outcome: each DPS player's DPS ÷ the median for <b>that DPS class on that boss</b>, grouped by which tank class was in the party. 1.00 = a typical run of that class.</p>
<div class="grid2">
<div class="panel"><h3>Teammate DPS lift by tank</h3><div class="tscroll" id="lift"></div><p class="note"><b>Within-player</b> is the strongest lens: <span id="vWP"></span> DPS players who killed the same boss with two or more different tank classes, each compared only to their own average. It removes player skill and most gear differences; what remains is the tank's buffs plus how well the tank controls the boss.</p></div>
<div class="panel"><h3>Teammate lift by dungeon</h3><div class="tscroll" id="liftArea"></div><p class="note">Blank = fewer than 10 DPS samples with that tank.</p></div>
</div>
<div class="panel" style="margin-top:16px"><h3>rDPS index, Brawler = 100</h3><div class="tscroll" id="rdps"></div>
<p class="note">Every row uses the same recipe as the workbook — median personal DPS per boss + that boss's median teammate DPS × (M−1)/M, indexed to Brawler, median across bosses where each class has ≥3 kills — and differs only in where M comes from. <b>Berserker tank: 15 kills from 7 players — directional only.</b></p></div>
</section>

<section>
<h2>Personal DPS by dungeon</h2>
<p class="lead">Median / 90th percentile / best recorded tank DPS per class, 5-man kills only. <span class="n">n = samples · uniq = distinct named players</span></p>
<div class="panel"><div class="tabs" role="tablist" id="areaTabs"></div><div class="tscroll" id="areaTable"></div></div>
</section>

<section>
<h2>Kill-time matched comparison</h2>
<p class="lead">Each boss's kills split into duration quartiles; each tank's average DPS ÷ the tank median of that bucket only.</p>
<div class="panel">
<div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:10px"><label for="bossSel" class="hdr">Boss</label><select id="bossSel"></select><span class="n" id="bossN"></span></div>
<div class="tscroll" id="ktTable"></div>
<p class="legend">Green ≥ 1.05 · grey 0.95–1.05 · red ≤ 0.95 · blank = fewer than 3 samples.</p>
</div>
</section>

<section>
<h2>Gear</h2>
<p class="lead">Recorded equipment covers <span id="gearCov"></span> of tank samples. Weapon enchant + brooch + item level is the gear score (no etching/potential fields in this game version).</p>
<div class="grid2">
 <div class="panel"><h3>How much gear moves the needle</h3><div class="tscroll" id="gearEffect"></div></div>
 <div class="panel"><h3>Who is geared</h3><div class="tscroll" id="gearProfile"></div></div>
</div>
<div class="panel" style="margin-top:16px"><h3>How much each tank gains from gear</h3><div class="tscroll" id="classTier"></div><p class="note">Median index per weapon tier with n; <b>% per ilvl</b> is a regression slope over all samples of the class (ilvl 395–420). Blank = fewer than 3 samples.</p></div>
<div class="panel" style="margin-top:16px"><h3>Same gear, same boss: <span id="stdDesc"></span></h3><div class="tabs" role="tablist" id="stdTabs"></div><div id="stdChart"></div><p class="note" id="stdNote"></p></div>
</section>

<section>
<h2>Reading guide</h2>
<div class="panel"><ul class="tight">
<li><b>Personal index</b> = tank DPS ÷ median tank DPS on the same boss. Lancer is 80% of all tank samples, so the median is mostly "a Lancer".</li>
<li><b>Teammate lift</b> is what the party's DPS players actually did with this tank, class- and boss-matched. It captures buffs, debuffs and boss control together — it cannot separate them.</li>
<li><b>rDPS</b> = personal + standardised teammate DPS × (M−1)/M. Rows labelled "workbook" use the reviewed report's multipliers; "corrected model" swaps in measured uptimes and removes Traverse Cut; "measured" derives M from teammate lift relative to Brawler.</li>
<li>Anonymous tanks are included in DPS stats but can't be de-duplicated; distinct-player counts are lower bounds.</li>
</ul></div>
</section>
</div>
<script>
const D=__DATA__;
const TANKS=['Lancer','Brawler','Warrior','Berserker'];
const AREAS=["Dragon's Landing","TS Hard","TS Savage","SS Hard","SS Savage"];
const fmt=n=>n==null?'–':Math.round(n).toLocaleString('en-US');
const fk=n=>n==null?'–':(n/1000).toFixed(0)+'k';
const f2=n=>n==null?'–':n.toFixed(2);
const pct=n=>n==null?'–':Math.round(n*100)+'%';
const pill=v=>v==null?'':`<span class="pill ${v>=1.05?'pos':v<=0.95?'neg':'mid'}">${f2(v)}</span>`;
const ds=D.dataset;
document.getElementById('tiles').innerHTML=[[ds.five,'kills (5-man)'],[ds.players,'named tanks'],...TANKS.map(c=>[ds.tankMix[c]||0,c+' kills'])].map(([v,l])=>`<div class="tile"><b>${fmt(v)}</b><span>${l}</span></div>`).join('');
const up=D.uptimesPlayer, eu=D.uptimes;
document.getElementById('vLead').textContent=Math.round(up.Berserker["Berzerker's Lead x4"].medAll)+'%';
document.getElementById('vGP').textContent=Math.round(up.Lancer["Guardian Power"].medAll)+'%';
document.getElementById('vAR').textContent=Math.round(up.Lancer["Adrenaline Rush"].medAll)+'%';
document.getElementById('vDeb').textContent=Math.round(eu.Lancer["Debilitate"].medAll)+'%';
document.getElementById('vWP').textContent=D.liftWithinPlayer._players;
{const l=D.lift.all, a=D.lift.noDpsWarrior; let tot=0,nw=0; for(const c in l){tot+=l[c].n; nw+=(a[c]||{n:0}).n;} document.getElementById('vDW').textContent=Math.round(100*(1-nw/tot))+'%';}
document.getElementById('inputs').innerHTML=`<table><thead><tr><th>tank</th><th>buff / debuff</th><th>model uptime</th><th>measured</th></tr></thead><tbody>`+Object.entries(D.modelInputs).flatMap(([c,r])=>Object.entries(r).map(([k,v],i)=>`<tr><td>${i===0?'<b>'+c+'</b>':''}</td><td style="text-align:left">${k}</td><td>${pct(v.model)}</td><td><b>${pct(v.measured)}</b></td></tr>`)).join('')+`</tbody></table>`;
function barChart(el,rows,key,nkey){
  const vals=rows.map(r=>r[1][key]); const lo=Math.min(0.7,...vals), hi=Math.max(1.3,...vals);
  const p=v=>((v-lo)/(hi-lo)*100);
  el.innerHTML=`<div class="bars"><div class="hdr">tank</div><div></div><div class="hdr" style="text-align:right">index</div><div class="hdr" style="text-align:right">${nkey}</div>`+
    rows.sort((a,b)=>b[1][key]-a[1][key]).map(([c,r])=>{const v=r[key];const z=p(1);const x=p(v);
      return `<div class="lab">${c}</div><div class="track"><div class="zero" style="left:${z}%"></div><div class="fill ${v>=1.03?'pos':v<=0.97?'neg':''}" style="left:${Math.min(z,x)}%;width:${Math.abs(x-z)}%"></div></div><div class="v">${f2(v)}</div><div class="nn">${r.n} <span style="opacity:.7">/ ${r.players??''}</span></div>`}).join('')+`</div>`;
}
const wpB=D.liftWithinPlayer.Brawler.avgDelta;
const lenses=[
 {label:'Personal DPS',rows:Object.entries(D.relIndex),note:'Average of per-kill index vs the boss tank median. Player-best median: '+Object.entries(D.relIndex).sort((a,b)=>b[1].playerBestMed-a[1].playerBestMed).map(([c,r])=>c+' '+f2(r.playerBestMed)).join(' · ')+'.'},
 {label:'Kill-time matched',rows:Object.entries(D.killTimeIndex).map(([c,r])=>[c,{avg:r.rel,n:r.n,players:D.relIndex[c].players}]),note:'Personal DPS ÷ tank median of the same duration quartile on the same boss.'},
 {label:'Same gear',rows:Object.entries(D.gear.stdBucket.classes),note:`Only tanks wearing ${D.gear.stdBucket.desc} (${D.gear.stdBucket.n} samples).`},
 {label:'Teammate lift',rows:Object.entries(D.lift.all).map(([c,r])=>[c,{avg:r.avg,n:r.n,players:r.encounters}]),note:'What the party\'s DPS players did with this tank (class- and boss-matched). n = DPS samples / kills.'},
 {label:'Teammate lift, within-player',rows:Object.entries(D.liftWithinPlayer).filter(([c])=>c!=='_players').map(([c,r])=>[c,{avg:1+r.avgDelta,n:r.n,players:''}]),note:'Same DPS players, same boss, different tank: deviation from each player\'s own average, +1.'}
];
const tabs=document.getElementById('lensTabs');
lenses.forEach((L,i)=>{const b=document.createElement('button');b.role='tab';b.textContent=L.label;b.setAttribute('aria-selected',i===0);b.onclick=()=>{[...tabs.children].forEach(x=>x.setAttribute('aria-selected',x===b));barChart(document.getElementById('lensChart'),L.rows.map(r=>[r[0],{...r[1]}]),'avg','n / uniq');document.getElementById('lensNote').textContent=L.note};tabs.appendChild(b)});
tabs.children[0].click();
// lift table
const liftRows=[['All DPS samples',D.lift.all],['DPS wearing +6 weapon only',D.lift.plus6only],['Parties with no DPS Warrior',D.lift.noDpsWarrior],['Within-player (same player, same boss)',Object.fromEntries(Object.entries(D.liftWithinPlayer).filter(([c])=>c!=='_players').map(([c,r])=>[c,{avg:1+r.avgDelta,n:r.n}]))]];
document.getElementById('lift').innerHTML=`<table><thead><tr><th>lens</th>${TANKS.map(c=>`<th>${c}</th>`).join('')}</tr></thead><tbody>`+liftRows.map(([l,r])=>`<tr><td style="white-space:normal">${l}</td>${TANKS.map(c=>r[c]?`<td>${pill(r[c].avg)} <span class="n">${r[c].n}</span></td>`:'<td></td>').join('')}</tr>`).join('')+`</tbody></table>`;
document.getElementById('liftArea').innerHTML=`<table><thead><tr><th>dungeon</th>${TANKS.map(c=>`<th>${c}</th>`).join('')}</tr></thead><tbody>`+AREAS.map(a=>{const r=D.lift.byArea[a]||{};return `<tr><td>${a}</td>${TANKS.map(c=>r[c]?`<td>${pill(r[c].avg)} <span class="n">${r[c].n}</span></td>`:'<td></td>').join('')}</tr>`}).join('')+`</tbody></table>`;
// rdps table
const scen=[['Personal DPS only',D.personalVsBrawler,null],['Workbook · buffs-only floor',D.rdps.floor,D.multipliers.floor],['Workbook · base',D.rdps.base,D.multipliers.base],['Workbook · linear ceiling',D.rdps.ceiling,D.multipliers.ceiling],['Corrected model (measured uptimes, no Traverse Cut)',D.rdps.correctedModel,D.multipliers.correctedModel],['Measured lift, all samples',D.rdps.empirical,D.multipliers.empirical],['Measured lift, within-player',D.rdps.empiricalWithinPlayer,D.multipliers.empiricalWithinPlayer]];
const ip=v=>v==null?'':`<span class="pill ${v>=105?'pos':v<=95?'neg':'mid'}">${Math.round(v)}</span>`;
document.getElementById('rdps').innerHTML=`<table><thead><tr><th>scenario</th>${TANKS.map(c=>`<th>${c}</th>`).join('')}</tr></thead><tbody>`+scen.map(([l,r,m])=>`<tr><td style="white-space:normal">${l}</td>${TANKS.map(c=>r[c]?`<td>${ip(r[c].index)}${m&&m[c]?` <span class="n">M ${f2(m[c])}</span>`:''}</td>`:'<td></td>').join('')}</tr>`).join('')+`</tbody></table>`;
// area tables
const at=document.getElementById('areaTabs');
function areaTable(a){const rows=Object.entries(D.byArea[a]).sort((x,y)=>y[1].med-x[1].med);
 document.getElementById('areaTable').innerHTML=rows.length?`<table><thead><tr><th>tank</th><th>n</th><th>uniq</th><th>min</th><th>p25</th><th>median</th><th>avg</th><th>p75</th><th>p90</th><th>max</th><th>index</th></tr></thead><tbody>`+
 rows.map(([c,r])=>`<tr><td><b>${c}</b></td><td class="n">${r.n}</td><td class="n">${r.players}</td><td class="n">${fk(r.min)}</td><td class="n">${fk(r.p25)}</td><td><b>${fk(r.med)}</b></td><td>${fk(r.avg)}</td><td class="n">${fk(r.p75)}</td><td>${fk(r.p90)}</td><td>${fk(r.max)}</td><td>${pill(D.relIndexByArea[a][c]&&D.relIndexByArea[a][c].avg)}</td></tr>`).join('')+`</tbody></table>`:'<p class="n">Fewer than 3 samples for every class.</p>'}
AREAS.forEach((a,i)=>{const b=document.createElement('button');b.role='tab';b.textContent=a;b.setAttribute('aria-selected',i===0);b.onclick=()=>{[...at.children].forEach(x=>x.setAttribute('aria-selected',x===b));areaTable(a)};at.appendChild(b)});
at.children[0].click();
// kill time
const sel=document.getElementById('bossSel');
const bossKeys=Object.keys(D.killTime).sort((a,b)=>D.killTime[b].n-D.killTime[a].n);
bossKeys.forEach(k=>{const o=document.createElement('option');o.value=k;o.textContent=`${k} (${D.killTime[k].n})`;sel.appendChild(o)});
function kt(k){const K=D.killTime[k];document.getElementById('bossN').textContent=`${K.n} kills · quartile cuts by fight length`;
 const present=TANKS.filter(c=>K.buckets.some(b=>b[c]));
 document.getElementById('ktTable').innerHTML=`<table class="heat"><thead><tr><th>tank</th>${K.labels.map((l,i)=>`<th>${['fast','','','slow'][i]||''} ${l}</th>`).join('')}<th>all-bucket avg</th></tr></thead><tbody>`+
 present.map(c=>{const vals=K.buckets.map(b=>b[c]);const have=vals.filter(Boolean);const avg=have.length?have.reduce((s,v)=>s+v.rel*v.n,0)/have.reduce((s,v)=>s+v.n,0):null;
  return `<tr><td><b>${c}</b></td>${vals.map(v=>`<td title="${v?`n=${v.n} · avg ${fk(v.avg)} · max ${fk(v.max)}`:''}">${v?pill(v.rel)+` <span class="n">${v.n}</span>`:''}</td>`).join('')}<td>${pill(avg)}</td></tr>`}).join('')+`</tbody></table>`}
sel.onchange=()=>kt(sel.value);kt(bossKeys[0]);
// gear
document.getElementById('gearCov').textContent=`${D.gear.coverage.withGear.toLocaleString()} of ${D.gear.coverage.of.toLocaleString()} (${Math.round(100*D.gear.coverage.withGear/D.gear.coverage.of)}%)`;
document.getElementById('gearEffect').innerHTML=`<table><thead><tr><th>weapon</th><th>n</th><th>median index</th></tr></thead><tbody>`+Object.entries(D.gear.tierEffect).map(([t,r])=>`<tr><td>${t}</td><td class="n">${r.n}</td><td>${pill(r.med)}</td></tr>`).join('')+`</tbody></table>`;
document.getElementById('gearProfile').innerHTML=`<table><thead><tr><th>tank</th><th>n</th><th>avg ilvl</th><th>avg wpn</th><th>+7 or better</th><th>chrono</th></tr></thead><tbody>`+Object.entries(D.gear.classGearProfile).map(([c,r])=>`<tr><td><b>${c}</b></td><td class="n">${r.n}</td><td>${r.avgIlvl?r.avgIlvl.toFixed(1):'–'}</td><td>+${r.avgWEnch.toFixed(2)}</td><td>${Math.round(r.pct7plus*100)}%</td><td>${Math.round(100*(r.brooch['Chrono Brooch']||0)/r.n)}%</td></tr>`).join('')+`</tbody></table>`;
const TIERS=Object.keys(D.gear.tierEffect);
document.getElementById('classTier').innerHTML=`<table><thead><tr><th>tank</th>${TIERS.map(t=>`<th>${t.replace(' weapon','')}</th>`).join('')}<th>+6 → +7</th><th>% per ilvl</th></tr></thead><tbody>`+Object.entries(D.gear.classByTier).map(([c,r])=>{const g=(a,b)=>r[a]&&r[b]?`<b>${r[b].med>=r[a].med?'+':''}${Math.round((r[b].med/r[a].med-1)*100)}%</b>`:'<span class="n">–</span>';
 return `<tr><td><b>${c}</b></td>${TIERS.map(t=>r[t]?`<td>${pill(r[t].med)} <span class="n">${r[t].n}</span></td>`:'<td></td>').join('')}<td>${g('+6 weapon','+7 weapon')}</td><td><b>${r.ilvlSlope?(r.ilvlSlope.perIlvl*100).toFixed(1)+'%':'–'}</b> <span class="n">${r.ilvlSlope?r.ilvlSlope.n:''}</span></td></tr>`}).join('')+`</tbody></table>`;
document.getElementById('stdDesc').textContent=D.gear.stdBucket.desc;
const stdTabs=document.getElementById('stdTabs');
const stdSets=[['All dungeons',D.gear.stdBucket.classes,D.gear.stdBucket.n],...AREAS.map(a=>[a,D.gear.stdBucket.byArea[a],Object.values(D.gear.stdBucket.byArea[a]).reduce((s,r)=>s+r.n,0)])].filter(s=>Object.keys(s[1]).length);
stdSets.forEach(([label,rows,n],i)=>{const b=document.createElement('button');b.role='tab';b.textContent=label;b.setAttribute('aria-selected',i===0);
 b.onclick=()=>{[...stdTabs.children].forEach(x=>x.setAttribute('aria-selected',x===b));barChart(document.getElementById('stdChart'),Object.entries(rows).map(r=>[r[0],{...r[1]}]),'avg','n / uniq');
 document.getElementById('stdNote').textContent=`${n} samples wearing ${D.gear.stdBucket.desc}${label==='All dungeons'?', all five dungeons pooled':' in '+label}. Index is vs the tank median of all players on the boss.`};
 stdTabs.appendChild(b)});
stdTabs.children[0].click();
</script>
"""
html=html.replace("__CSS__",css).replace("__DATA__",DATA).replace("__D0__",d0).replace("__D1__",d1)
open("tankreport.html","w",encoding="utf-8").write(html)
open("tanks.html","w",encoding="utf-8").write('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width"></head><body style="margin:0">'+html+'</body></html>')
print("ok",len(html))
