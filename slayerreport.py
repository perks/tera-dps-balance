import json,re
D=json.load(open("slayer2.json",encoding="utf-8"))
DATA=json.dumps(D,ensure_ascii=False).replace('"icons/','"../icons/')
css=re.search(r"<style>(.*?)</style>",open("report.py",encoding="utf-8").read(),re.S).group(1)
html = r"""<title>Slayer Build Data</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<style>__CSS__
.nav{display:flex;gap:14px;font-size:13px;font-weight:600;margin-bottom:14px}.nav a{color:var(--ink2);text-decoration:none;border-bottom:2px solid transparent;padding-bottom:2px}.nav a[aria-current]{color:var(--ink);border-color:var(--bar)}
.lede{font-size:16.5px;line-height:1.5;max-width:72ch;margin:0 0 18px}
.build .row{display:grid;grid-template-columns:128px 1fr 150px;gap:14px;padding:10px 0;border-bottom:1px solid var(--line);align-items:baseline}
.build .row:last-child{border-bottom:0}
.build .slot{font-weight:600;color:var(--ink2);font-size:12.5px;text-transform:uppercase;letter-spacing:.05em}
.build .pick{font-size:15.5px;font-weight:600}
.build .alt{font-size:13px;color:var(--ink2);margin-top:3px}
.build .pctn{text-align:right;font-weight:700;font-variant-numeric:tabular-nums;font-size:15px;white-space:nowrap}
.build .pctn small{display:block;font-size:10.5px;font-weight:600;color:var(--muted);letter-spacing:.05em;text-transform:uppercase}
@media (max-width:760px){.build .row{grid-template-columns:1fr 90px}.build .slot{grid-column:1/3}}
.skillgroup{border:1px solid var(--line);border-radius:6px;padding:12px 14px;background:var(--panel)}
.skillgroups{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:12px}
.skillhead{display:flex;align-items:center;gap:10px;margin-bottom:8px}
.skillhead img{width:34px;height:34px;border-radius:5px;background:var(--heat0)}
.skillhead b{font-size:16px}
.skillhead span{font-size:12px;color:var(--muted);margin-left:auto;font-variant-numeric:tabular-nums;white-space:nowrap}
.gitem{display:flex;align-items:center;gap:9px;padding:5px 0;border-top:1px solid var(--line)}
.gitem img{width:24px;height:24px;border-radius:4px;background:var(--heat0)}
.gitem .nm{font-size:14px;flex:1}
.gitem .nm i{display:block;font-style:normal;font-size:11.5px;color:var(--muted)}
.gitem .pctn{font-size:13px;font-weight:700;font-variant-numeric:tabular-nums}
.gitem .pctn.hi{color:var(--pos)}
.dmg{display:grid;grid-template-columns:34px 130px 1fr 50px;gap:8px 10px;align-items:center;font-size:14.5px}
.dmg img{width:28px;height:28px;border-radius:4px;background:var(--heat0)}
.dmg .bar{height:18px;background:var(--heat0);border-radius:3px;overflow:hidden}
.dmg .bar i{display:block;height:100%;background:var(--bar);border-radius:3px}
.dmg .v{text-align:right;font-weight:600;font-variant-numeric:tabular-nums}
details{border:1px solid var(--line);border-radius:6px;background:var(--panel);margin-top:12px}
summary{cursor:pointer;padding:11px 16px;font-weight:600;font-size:14.5px;list-style:none}
summary::-webkit-details-marker{display:none}
summary::before{content:"\25B8   ";color:var(--muted)}
details[open] summary::before{content:"\25BE   "}
details .inner{padding:0 16px 10px}
tr.me td{background:var(--heat0)}
</style>
<div class="wrap">
<div class="nav"><a href="../">Home</a><a href="../tera-dps-balance/">DPS classes</a><a href="../slayer-build/" aria-current="page">Slayer build data</a><a href="../slayer-guide/">Slayer guide</a></div>
<div class="eyebrow">TERA Europe Classic+ · <span id="ds"></span></div>
<h1>Slayer Build Data</h1>
<p class="lede">What the top Slayers run. For each endgame boss, the top 25 players by best recorded parse form the shortlist; every figure below is a share of that shortlist. Median item level <span id="ilvlm2"></span>.</p>
<div class="tiles" id="tiles"></div>

<section>
<h2>Gear</h2>
<div class="panel"><div class="build" id="build"></div></div>
</section>

<section>
<h2>Accessory rolls</h2>
<p class="lead">Roll lines on each slot, as a share of the shortlist.</p>
<div class="panel"><div class="tscroll" id="rolls"></div></div>
<details><summary>Roll lines counted across all accessories</summary><div class="inner tscroll" id="rollTypes"></div></details>
</section>

<section>
<h2>Weapon and armor rolls</h2>
<p class="lead">The rolled lines only; masterwork tiers excluded. Weapon and chest carry four, gloves and boots three.</p>
<div class="panel"><div class="tscroll" id="gearRolls"></div></div>
<details><summary>Most common complete sets per piece</summary><div class="inner tscroll" id="gearCombos"></div></details>
</section>

<section>
<h2>Crystals</h2>
<div class="panel"><div class="tscroll" id="crystals"></div></div>
</section>

<section>
<h2>Jewelry: Monarch or Titan</h2>
<p class="lead">Monarch pieces carry Crit Factor; Titan pieces carry Power.</p>
<div class="panel">
<div class="tscroll" id="jewel"></div>
<p class="note" id="jewelNote"></p>
</div>
</section>

<section>
<h2>Glyphs</h2>
<p class="lead">Grouped by skill, ordered by that skill's share of Slayer damage. Percentage is the share of shortlisted players running the glyph; <span id="glcov2"></span> of shortlist parses have a recorded glyph page.</p>
<div class="skillgroups" id="glyphs"></div>
<details><summary>Full glyph table, top third of the shortlist vs the rest</summary><div class="inner tscroll" id="gfull"></div></details>
</section>

<section>
<h2>Rotation</h2>
<div class="panel"><div class="dmg" id="dmg"></div></div>
<details><summary>Casts per minute and crit rate per skill</summary><div class="inner tscroll" id="rot"></div></details>
</section>

<section>
<h2>The shortlists</h2>
<div class="panel">
<div class="tabs" role="tablist" id="boardTabs"></div>
<div class="tscroll" id="board"></div>
<p class="note" id="boardNote"></p>
</div>
</section>

<section>
<h2>Method</h2>
<div class="panel"><ul class="tight">
<li>For each boss, each player's single best parse is ranked and the top 25 kept. One parse per player per boss.</li>
<li>Item level across the shortlist runs <span id="ilvlr"></span>, median <span id="ilvlm"></span>.</li>
<li>Top third vs rest uses each player's rank within their own boss shortlist.</li>
<li>Combat logs are available for all shortlist parses; glyph pages for <span id="glcov"></span>.</li>
<li>Savage bosses have 1–5 players on record.</li>
</ul></div>
</section>
</div>
<script>
const D=__DATA__;
const f1=n=>n==null?'-':n.toFixed(1);
const pc=n=>n==null?'-':Math.round(n*100)+'%';
const fk=n=>n==null?'-':Math.round(n/1000)+'k';
const fmt=n=>n==null?'-':Math.round(n).toLocaleString('en-US');
const ds=D.dataset;
document.getElementById('ds').textContent=`${ds.players} players · ${ds.shortlistParses} shortlisted parses · ${ds.boards} boss lists`;
document.getElementById('tiles').innerHTML=[[ds.players,'shortlisted players'],[ds.shortlistParses,'shortlisted parses'],[ds.allParses,'parses considered'],[ds.boards,'boss lists']]
 .map(([v,l])=>`<div class="tile"><b>${fmt(v)}</b><span>${l}</span></div>`).join('');
const R=D.runs, first=a=>a&&a[0];
const jew=R.jewelry.slice().sort((a,b)=>b.n-a.n);
const cry=first(R.crystals), br=R.brooch, belt=first(R.belt), we=R.wEnch.slice().sort((a,b)=>b.n-a.n);
const enr=R.wRolls.find(x=>x.value==='Dmg vs enraged'), beh=R.wRolls.find(x=>x.value==='Dmg from behind'), flat=R.wRolls.find(x=>x.value==='Flat damage'), cd=R.wRolls.find(x=>x.value==='Cooldown');
const alt=(arr,skip)=>arr.filter(x=>x.value!==skip).slice(0,2).map(x=>`${x.value}${typeof x.value==='number'?'':''} ${pc(x.share)}`).join(' · ');
function row(slot,pick,share,unit,alt){return `<div class="row"><div class="slot">${slot}</div><div><div class="pick">${pick}</div>${alt?`<div class="alt">${alt}</div>`:''}</div><div class="pctn">${share}<small>${unit}</small></div></div>`}
document.getElementById('build').innerHTML=[
 row('Belt',belt.value,pc(belt.share),'of shortlist',''),
 row('Brooch',br[0].value,pc(br[0].share),'of shortlist',br.slice(1).map(x=>`${x.value} ${pc(x.share)}`).join(' · ')),
 row('Jewelry',jew[0].value,pc(jew[0].share),'of shortlist',jew.slice(1,3).map(x=>`${x.value} ${pc(x.share)}`).join(' · ')),
 row('Weapon enchant','+'+we[0].value,pc(we[0].share),'of shortlist',we.slice(1).map(x=>`+${x.value} ${pc(x.share)}`).join(' · ')),
 row('Weapon lines','Damage vs enraged monsters',pc(enr.share),'carry it',[beh&&`Damage from behind ${pc(beh.share)}`,flat&&`Flat damage ${pc(flat.share)}`,cd&&`Cooldown reduction ${pc(cd.share)}`].filter(Boolean).join(' · '))
].join('');
// rolls per slot
const SLOTS=[['necklace','Necklace'],['earring-left','Earring (left)'],['earring-right','Earring (right)'],['ring-left','Ring (left)'],['ring-right','Ring (right)'],['belt','Belt'],['brooch','Brooch']];
document.getElementById('rolls').innerHTML=`<table><thead><tr><th>slot</th><th>most common</th><th></th><th>second</th><th></th><th>third</th><th></th></tr></thead><tbody>`+
 SLOTS.map(([k,l])=>{const a=D.slotRolls[k]||[];
  return `<tr><td><b>${l}</b></td>`+[0,1,2].map(i=>a[i]?`<td>${a[i].value}</td><td class="n">${pc(a[i].share)}</td>`:'<td></td><td></td>').join('')+`</tr>`}).join('')+`</tbody></table>`;
document.getElementById('rollTypes').innerHTML=`<table><thead><tr><th>roll line</th><th>players with at least one</th><th>average count per player</th></tr></thead><tbody>`+
 D.rollTypes.map(x=>`<tr><td><b>${x.value}</b></td><td>${pc(x.share)}</td><td>${f1(x.avgCount)}</td></tr>`).join('')+`</tbody></table>`;
// weapon/armor rolls
document.getElementById('gearRolls').innerHTML=Object.entries(D.gearRolls).map(([k,v])=>
 `<table style="margin-bottom:14px"><thead><tr><th>${k} · ${v.slots} rolls</th><th>players with it</th><th>average per player</th></tr></thead><tbody>`+
 v.lines.map(l=>`<tr><td><b>${l.value}</b></td><td>${pc(l.share)}${l.dbl>=0.05?` <span class="n">(${pc(l.dbl)} run two)</span>`:''}</td><td class="n">${l.avg.toFixed(2)}</td></tr>`).join('')+`</tbody></table>`).join('');
document.getElementById('gearCombos').innerHTML=Object.entries(D.gearRolls).map(([k,v])=>
 `<table style="margin-bottom:14px"><thead><tr><th>${k}</th><th>players</th><th>share</th></tr></thead><tbody>`+
 v.combos.map(c=>`<tr><td>${c.value.join(' · ')}</td><td class="n">${c.n}</td><td>${pc(c.share)}</td></tr>`).join('')+`</tbody></table>`).join('');
// crystals
document.getElementById('crystals').innerHTML=`<table><thead><tr><th>slot</th><th>most common</th><th></th><th>second</th><th></th><th>third</th><th></th></tr></thead><tbody>`+
 Object.entries(D.crystals).map(([k,v])=>`<tr><td><b>${k}</b></td>`+[0,1,2].map(i=>v.sets[i]?`<td>${v.sets[i].value}</td><td class="n">${pc(v.sets[i].share)}</td>`:'<td></td><td></td>').join('')+`</tr>`).join('')+`</tbody></table>`;
// jewelry
document.getElementById('jewel').innerHTML=`<table><thead><tr><th>build</th><th>parses</th><th>share</th></tr></thead><tbody>`+
 jew.map(x=>`<tr${x.n===jew[0].n?' class="me"':''}><td><b>${x.value}</b></td><td class="n">${x.n}</td><td>${pc(x.share)}</td></tr>`).join('')+`</tbody></table>`;
const sp=D.split;
document.getElementById('jewelNote').textContent=`On Calamity Helghan the top third of the shortlist averages ${f1(sp.top.titan)} Titan pieces, the middle third ${f1(sp.mid.titan)}, the bottom third ${f1(sp.bottom.titan)}. Crit Factor: ${fmt(sp.top.critFactor)} top third vs ${fmt(sp.bottom.critFactor)} bottom third. Attack: ${fmt(sp.top.attack)} vs ${fmt(sp.bottom.attack)}.`;
// glyphs by skill
document.getElementById('glyphs').innerHTML=D.glyphsBySkill.filter(g=>g.glyphs.some(x=>x.share>=0.15)).map(g=>`
 <div class="skillgroup">
  <div class="skillhead">${g.icon?`<img src="${g.icon}" alt="">`:''}<b>${g.skill}</b><span>${g.share!=null?f1(g.share)+'% of damage':''}</span></div>
  ${g.glyphs.filter(x=>x.share>=0.15).map(x=>`<div class="gitem">${x.icon?`<img src="${x.icon}" alt="">`:''}<div class="nm">${x.name}${x.points?`<i>${x.points} points${x.desc?' · '+x.desc:''}</i>`:''}</div><div class="pctn ${x.share>=0.9?'hi':''}">${pc(x.share)}</div></div>`).join('')}
 </div>`).join('');
document.getElementById('gfull').innerHTML=`<table><thead><tr><th>glyph</th><th>skill</th><th>points</th><th>shortlist</th><th>top third</th><th>rest</th></tr></thead><tbody>`+
 D.glyphs.list.map(g=>`<tr><td><b>${g.name}</b></td><td class="n">${g.skill||''}</td><td class="n">${g.points||''}</td><td>${pc(g.share)}</td><td class="n">${pc(g.top)}</td><td class="n">${pc(g.rest)}</td></tr>`).join('')+
 `</tbody></table><p class="note">Top third n=${D.glyphs.nTop}, rest n=${D.glyphs.nRest}.</p>`;
// rotation
const icons={}; D.glyphsBySkill.forEach(g=>{if(g.icon)icons[g.skill]=g.icon});
const rot=D.rotation.filter(r=>r.name!=='(unnamed)'&&r.share>=0.5);
const mx=rot[0].share;
document.getElementById('dmg').innerHTML=rot.map(r=>`<div>${icons[r.name]?`<img src="${icons[r.name]}" alt="">`:''}</div><div>${r.name}</div><div class="bar"><i style="width:${100*r.share/mx}%"></i></div><div class="v">${f1(r.share)}%</div>`).join('');
document.getElementById('rot').innerHTML=`<table><thead><tr><th>skill</th><th>damage share</th><th>casts / min</th><th>crit rate</th></tr></thead><tbody>`+
 D.rotation.filter(r=>r.name!=='(unnamed)').map(r=>`<tr><td><b>${r.name}</b></td><td><b>${f1(r.share)}%</b></td><td>${f1(r.cpm)}</td><td class="n">${f1(r.crit)}%</td></tr>`).join('')+`</tbody></table>`;
// boards
const bt=document.getElementById('boardTabs');
function board(i){const b=D.boards[i];
 document.getElementById('board').innerHTML=`<table><thead><tr><th>#</th><th>player</th><th>DPS</th><th>kill time</th><th>casts / min</th><th>crit</th><th>item level</th><th>jewelry</th><th>brooch</th></tr></thead><tbody>`+
  b.rows.map(r=>`<tr><td class="n">${r.rank}</td><td><b>${r.name}</b></td><td><b>${fk(r.dps)}</b></td><td class="n">${Math.round(r.dur)}s</td><td>${r.cpm?f1(r.cpm):'-'}</td><td class="n">${r.crit!=null?f1(r.crit)+'%':'-'}</td><td class="n">${r.ilvl?r.ilvl.toFixed(1):'-'}</td><td>${r.jewel||'-'}</td><td class="n">${(r.brooch||'-').replace(' Brooch','')}</td></tr>`).join('')+`</tbody></table>`;
 document.getElementById('boardNote').textContent=`${b.shortlist} of ${b.players} players with a recorded parse on this boss. Shortlist median ${fk(b.med)}.`}
D.boards.forEach((b,i)=>{const btn=document.createElement('button');btn.role='tab';btn.textContent=`${b.area} · ${b.boss.replace('Nightmare ','')} (${b.shortlist})`;btn.setAttribute('aria-selected',i===0);btn.onclick=()=>{[...bt.children].forEach(x=>x.setAttribute('aria-selected',x===btn));board(i)};bt.appendChild(btn)});
board(0);
document.getElementById('ilvlr').textContent=`${ds.ilvlLo.toFixed(0)}-${ds.ilvlHi.toFixed(0)}`;
document.getElementById('ilvlm').textContent=ds.ilvlMed.toFixed(1);
document.getElementById('ilvlm2').textContent=ds.ilvlMed.toFixed(1);
document.getElementById('glcov').textContent=pc(ds.withGlyphs/ds.shortlistParses);
document.getElementById('glcov2').textContent=pc(ds.withGlyphs/ds.shortlistParses);
</script>
"""
html=html.replace("__CSS__",css).replace("__DATA__",DATA)
open("slayerreport.html","w",encoding="utf-8").write(html)
open("slayer-build/index.html","w",encoding="utf-8").write('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width"></head><body style="margin:0">'+html+'</body></html>')
print("ok",len(html))
