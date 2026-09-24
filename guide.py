import json,re
D=json.load(open("slayer2.json",encoding="utf-8"))
IC=json.load(open("slayer_skill_icons.json",encoding="utf-8"))
ICONS={k:"../icons/"+v.split("/")[-1].lower() for k,v in IC.items()}
# keyed by glyph id: display names are reused across different custom glyphs
GLY={g["id"]:g for g in D["glyphs"]["list"]}
CTX=dict(icons=ICONS,glyphs={str(k):dict(share=v["share"],icon=v.get("icon"),points=v.get("points"),skill=v.get("skill"),desc=v.get("desc"),label=v.get("label"),name=v.get("name"),vague=v.get("vague")) for k,v in GLY.items()},
         rotation=D["rotation"],crystals=D["crystals"],gearRolls=D["gearRolls"],runs=D["runs"],jewelry=D["runs"]["jewelry"],
         split=D["split"],dataset=D["dataset"])
DATA=json.dumps(CTX,ensure_ascii=False).replace('"icons/','"../icons/')
css=re.search(r"<style>(.*?)</style>",open("report.py",encoding="utf-8").read(),re.S).group(1)
html = r"""<title>Slayer Guide</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<style>__CSS__
.nav{display:flex;gap:14px;font-size:13px;font-weight:600;margin-bottom:14px;flex-wrap:wrap}.nav a{color:var(--ink2);text-decoration:none;border-bottom:2px solid transparent;padding-bottom:2px}.nav a[aria-current]{color:var(--ink);border-color:var(--bar)}
.lede{font-size:16.5px;line-height:1.55;max-width:72ch;margin:0 0 16px}
p{max-width:72ch;line-height:1.55}
h3{margin-top:18px}
.sk{display:inline-flex;align-items:center;gap:5px;background:var(--heat0);border:1px solid var(--line);border-radius:4px;padding:1px 7px 1px 3px;font-weight:600;font-size:13.5px;white-space:nowrap;vertical-align:1px}
.sk img{width:20px;height:20px;border-radius:3px}
.chain{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:10px 0}
.chain .arw{color:var(--muted);font-weight:700}
.tierhead{display:flex;align-items:center;gap:8px;font-weight:700;font-size:15px;margin:14px 0 6px}
.dot{width:11px;height:11px;border-radius:50%;display:inline-block}
.dot.red{background:var(--neg)}.dot.yel{background:var(--accent)}.dot.blu{background:var(--bar)}
.gcards{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:8px}
.gcard{display:flex;gap:9px;align-items:flex-start;border:1px solid var(--line);border-left:3px solid var(--line2);border-radius:5px;padding:8px 10px;background:var(--panel)}
.gcard.red{border-left-color:var(--neg)}.gcard.yel{border-left-color:var(--accent)}.gcard.blu{border-left-color:var(--bar)}
.gcard img{width:26px;height:26px;border-radius:4px;background:var(--heat0);flex:none}
.gcard .nm{font-size:14px;font-weight:600;line-height:1.25}
.gcard .mt{font-size:11.5px;color:var(--muted);margin-top:2px}
.callout{border-left:3px solid var(--accent);background:var(--panel);border-radius:0 5px 5px 0;padding:10px 14px;margin:12px 0;font-size:14.5px}
.callout b{color:var(--accent)}
.linkcard{display:flex;justify-content:space-between;align-items:center;gap:12px;border:1px solid var(--line2);border-radius:6px;padding:12px 14px;background:var(--panel);margin:12px 0}
.linkcard a{color:var(--bar);font-weight:600;text-decoration:none;white-space:nowrap}
.bigcard{display:flex;justify-content:space-between;align-items:center;gap:16px;border:2px solid var(--bar);border-radius:8px;padding:16px 18px;background:var(--panel);margin:14px 0 20px;text-decoration:none;color:inherit}
.bigcard:hover{background:var(--heat0)}
.bigcard .bt{font-size:17px;font-weight:700;font-family:"Barlow Condensed",sans-serif;letter-spacing:.01em}
.bigcard .bs{font-size:13.5px;color:var(--ink2);margin-top:3px;max-width:60ch}
.bigcard .ba{background:var(--bar);color:#fff;font-weight:700;font-size:14px;padding:8px 14px;border-radius:5px;white-space:nowrap}
@media (max-width:620px){.bigcard{flex-direction:column;align-items:flex-start}}
.linkcard .t{font-size:14.5px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media (max-width:760px){.two{grid-template-columns:1fr}}
ol.steps{counter-reset:s;list-style:none;padding:0;margin:10px 0;max-width:72ch}
ol.steps li{counter-increment:s;position:relative;padding:7px 0 7px 34px;border-bottom:1px solid var(--line);font-size:14.5px;line-height:1.5}
ol.steps li:last-child{border-bottom:0}
ol.steps li::before{content:counter(s);position:absolute;left:0;top:7px;width:22px;height:22px;border-radius:50%;background:var(--heat0);color:var(--ink2);font-size:12px;font-weight:700;display:grid;place-items:center}
.miss{border:1px dashed var(--line2);border-radius:5px;padding:10px 14px;color:var(--ink2);font-size:14px;background:var(--heat0)}
.seq{display:flex;flex-wrap:wrap;gap:6px 4px;align-items:flex-start;margin:10px 0}
.seq .arw{color:var(--muted);font-weight:700;align-self:center;padding:0 2px}
.seq .st{display:flex;flex-direction:column;gap:2px;max-width:170px}
.seq .stn{font-size:11px;color:var(--muted);line-height:1.25;padding-left:2px}
.seqbox{border:1px solid var(--line);border-left:3px solid var(--line2);border-radius:0 6px 6px 0;padding:10px 14px;margin:10px 0;background:var(--panel)}
.seqbox.bad{border-left-color:var(--neg)}.seqbox.good{border-left-color:var(--pos)}
.seqlab{font-size:11.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.seqbox.bad .seqlab{color:var(--neg)}.seqbox.good .seqlab{color:var(--pos)}
.seqnote{font-size:13.5px;color:var(--ink2)}
</style>
<div class="wrap">
<div class="nav"><a href="../">Home</a><a href="../tera-dps-balance/">DPS classes</a><a href="../slayer-build/">Slayer build data</a><a href="../slayer-guide/" aria-current="page">Slayer guide</a></div>
<div class="eyebrow">TERA Europe Classic+ · PvE · Patch 0.04</div>
<h1>Playing Slayer</h1>
<p class="lede">It is true that you mostly chain <span class="sk" data-sk="Overhand Strike"></span>, but there are a handful of things that position you to get more out of the class. This is a PvE guide — nothing here applies to PvP.</p>
<div class="callout"><b>Disclaimer.</b> I am not the best Slayer and do not claim to be. Some of this is stylistic and true min-maxing depends on comp, encounter and kill time. Once you are comfortable, compare your own logs against top leaderboard performers at similar kill times. This is a baseline to grow your own Slayer style from.</div>

<section>
<h2>Gearing</h2>
<p>There is no one-size-fits-all here, because your roll lines are RNG. Below are the objectively good lines to aim for and rough breakpoints.</p>
<a class="bigcard" href="../slayer-build/"><div><div class="bt">See what the top 25 Slayers on every boss actually wear</div><div class="bs">Every roll line, crystal, accessory and glyph, measured from their best parses. Start there if you want the numbers behind anything below.</div></div><span class="ba">Build data &rarr;</span></a>

<h3>Crystals</h3>
<div class="two">
<div>
<ul class="tight">
<li><b>Armor:</b> 4× Hardy (blue) for boss damage</li>
<li><b>Accessories:</b> 4× Keen Vyrsk (green crit)</li>
<li><b>Weapon:</b> Savage, Bitter, Focused, Pounding</li>
</ul>
<p>Once you have enough crit rate you may want to switch the green crit crystals to green power. If you are less geared and short on crit, swapping Pounding for a Carving (+crit) is viable early.</p>
</div>
<div id="crystalData"></div>
</div>

<h3>Weapon rolls</h3>
<p>The god roll is <b>2× enrage damage, cooldown reduction, back attack</b>. There are plenty of fine alternatives among the % damage lines, and an argument for attack speed. Generally avoid MP lines, low crit power, and increasingly Crit Factor — it loses value on the weapon as you gear up.</p>
<div id="weaponData"></div>

<h3>Armor rolls</h3>
<div class="two">
<div>
<ul class="tight">
<li><b>Chest:</b> <span class="sk" data-sk="Overhand Strike"></span> <b>+10%</b> is the important one. Then enrage damage reduction, then max HP.</li>
<li><b>Gloves:</b> any offensive stat. Power and attack speed are my preference, but any of them work.</li>
<li><b>Boots:</b> 6% movement speed, alongside endurance.</li>
</ul>
</div>
<div id="armorData"></div>
</div>

<h3>Accessory rolls</h3>
<p>Same as gloves: take any valuable offensive stat from the pool, with Power probably the most valuable.</p>
</section>

<section>
<h2>Stat caps and accessories</h2>
<p>How much crit to go for, and which accessories, changes as you clear new content and upgrade gear. As of Patch 0.04 a solid setup is:</p>
<ul class="tight">
<li>1× Titan + 1× Monarch earrings</li>
<li>1× Titan + 1× Monarch rings</li>
<li>1× Monarch necklace</li>
</ul>
<p>The longer answer: you want crit only up to a point, then you move into Power, cooldown reduction and attack speed. To gauge where you are, open Shinra DPS Meter mid-fight by right-clicking your name and check your crit rate — it should be around or above 80% on a decent fight.</p>
<p>Gearing up with etchings and new accessories is what lets you start shifting selective stats into Power. You will juggle this every time you get new gear or reroll.</p>
<div id="jewelData"></div>

<h3>Brooch</h3>
<p>Both cooldown reduction and attack speed brooches are good. On test servers attack speed performed slightly better in a vacuum, but that assumes CDR rolls on weapon and etchings. Both work well.</p>
<div class="callout"><b>Watch your MP.</b> On attack speed under party buffs you will very likely go OOM even with charm. If you find yourself running out of things to hit off cooldown to chain, that is a sign you need more CDR.</div>
<div id="broochData"></div>
</section>

<section>
<h2>Glyphs</h2>
<p>There is flexibility in how you glyph Slayer depending on how you want to play. Baseline picks first, then the flexible ones.</p>
<div class="tierhead"><span class="dot red"></span>Baseline — take these</div>
<p style="margin:0 0 8px">They meaningfully contribute to the damage of the class and most people agree on them.</p>
<div class="gcards" id="gRed"></div>
<div class="tierhead"><span class="dot yel"></span>High-value utility</div>
<p style="margin:0 0 8px">Worth picking up if you have the points spare and they fit what you need.</p>
<div class="gcards" id="gYel"></div>
<div class="tierhead"><span class="dot blu"></span>Playstyle</div>
<p style="margin:0 0 8px">These depend entirely on how you want to play — experiment.</p>
<div class="gcards" id="gBlu"></div>
<p class="note">Tiers are ordered by how widely the top 25 players per boss actually run each glyph. <a href="../slayer-build/" style="color:var(--bar)">Full adoption table →</a></p>

<h3>Notes on the flexible picks</h3>
<ul class="tight">
<li>The 50% damage reduction is a comfortable buffer for non-one-shots, but has less value the harder the content you progress. Since you want to keep the <span class="sk" data-sk="Knockdown Strike"></span> buff rolling at all times, you cannot really treat it as an on-demand defensive.</li>
<li>In this version of Slayer you hit your chain starters a lot, so anything that speeds them up compounds. The <span class="sk" data-sk="Fury Strike"></span> glyph has a speed-up component for <span class="sk" data-sk="Whirlwind"></span> — it makes Whirlwind come out really fast. I enjoy that, so I glyph it, and since I use <span class="sk" data-sk="Fury Strike"></span> more I also take its damage glyph. Fury Strike does poor damage, but glyphed it is fast and very safe: easy to cancel out of.</li>
<li>Some people prefer the damage of <span class="sk" data-sk="Stunning Backhand"></span>. Some prioritise resets on <span class="sk" data-sk="Heart Thrust"></span>; I find that one miserable to use, and even on a reset I usually have an alternative button to press. None of this is clearly optimal, which is why it is stylistic.</li>
<li><span class="sk" data-sk="Startling Kick"></span> has a lot of utility value. I have not glyphed anything there, but several options look fun and strong.</li>
<li><span class="sk" data-sk="Distant Blade"></span> and auto-attack speed glyphs give a nice attack speed buff. Distant Blade is useful to gap-close and chain into <span class="sk" data-sk="Knockdown Strike"></span>; both can also be used for boss hitbox pushback.</li>
</ul>
</section>

<section>
<h2>Rotation</h2>
<p>Roughly half your damage is <span class="sk" data-sk="Overhand Strike"></span>, followed by <span class="sk" data-sk="Measured Slice"></span>. So the whole game is chaining cleanly into Overhand Strike as often as possible.</p>
<div id="dmgData"></div>
<p>Our most important glyph is the reset chance on Overhand Strike. It starts around 50%, goes to 66%, then 70% as you upgrade it. That is strong because you can follow almost any skill with Overhand Strike — except itself.</p>
<h3>The basic chain</h3>
<div class="chain" id="chain"></div>
<p>The gamble is whether the reset comes. During <span class="sk" data-sk="In Cold Blood"></span> that chance is 100%.</p>
<h3>Buff upkeep priority</h3>
<p>Which starter you use follows a rough priority based on keeping three buffs rolling:</p>
<ol class="steps">
<li><span class="sk" data-sk="Knockdown Strike"></span> — doubles crit chance</li>
<li><span class="sk" data-sk="Eviscerate"></span> — gives <span class="sk" data-sk="Overhand Strike"></span> and <span class="sk" data-sk="Measured Slice"></span> extra damage</li>
<li><span class="sk" data-sk="Whirlwind"></span> — +10% flat damage</li>
</ol>
<p>If you are new, this mostly means hit everything as soon as it comes up. <span class="sk" data-sk="Knockdown Strike"></span>, <span class="sk" data-sk="Heart Thrust"></span> and <span class="sk" data-sk="Whirlwind"></span> are the starters to prioritise.</p>
<div class="callout"><b>Never raw-dog <span class="sk" data-sk="Whirlwind"></span> without <span class="sk" data-sk="Headlong Rush"></span>.</b> Do not use it unless you can chain out of it — on its own it is giga slow and will get you killed.</div>
<h3>Example opener</h3>
<p>Once you are slaying you will mostly hit whatever starter is available and smash <span class="sk" data-sk="Overhand Strike"></span>, but this is a clean opener to work from.</p>
<div class="seq" id="opener"></div>
<p class="note">I prefer getting as many Overhand Strikes into the boss during burst as I can before mechanics start, so Headlong Rush goes late here rather than early — it is then up for the next rotation. That is a personal choice, not a rule. The one piece of general consensus: always start with the double-crit buff, because it is giga strong and cancels fast out of the animation.</p>
</section>

<section>
<h2>Advanced rotation tips</h2>
<h3>Never drift Overhand Strike</h3>
<p>You can spacebar effectively, but outside of <span class="sk" data-sk="In Cold Blood"></span> you are gambling on the reset. If you always gamble, there will be a moment where Overhand Strike is about to come off cooldown, you do not get the reset, and your starter is also on cooldown — leaving you auto-attacking awkwardly.</p>
<p>So watch how fast Overhand Strike is coming off cooldown. Pause the monkey-Slayer brain and consider saving a starter.</p>
<p>Say <span class="sk" data-sk="Measured Slice"></span> has <b>3 seconds</b> left on cooldown and everything else is up.</p>
<div class="seqbox bad"><div class="seqlab">Instead of this</div><div class="seq" id="seqBad"></div><div class="seqnote">No reset, half a second left on Measured Slice — and now Overhand Strike is on cooldown too.</div></div>
<div class="seqbox good"><div class="seqlab">Do this</div><div class="seq" id="seqGood"></div><div class="seqnote">Heart Thrust’s longer animation means the chain does not run out before Measured Slice comes off cooldown.</div></div>
<p>You can use <span class="sk" data-sk="Distant Blade"></span> to chain into <span class="sk" data-sk="Knockdown Strike"></span> during your rotation if you want to gamble for attack speed. In tests this came out very neutral, since the proc is random — but it helps because Distant Blade pushes you forward and doubles as a repositioning tool.</p>
<h3>Line up Measured Slice behind a Whirlwind</h3>
<p>If you know <span class="sk" data-sk="Measured Slice"></span> will be available in your next chain, prioritise <span class="sk" data-sk="Whirlwind"></span> as the starter so Measured Slice comes out buffed.</p>
<p><span class="sk" data-sk="Startling Kick"></span> as a starter: do not brainlessly spam it if you know a stun mechanic is coming. It is fast, but without something to chain out of it the animation is really slow.</p>
</section>

<section>
<h2>Repositioning</h2>
<p>The core problem with Slayer is that our defensives are also our mobility, so we constantly choose between keeping iframes up and losing uptime by not being behind the boss.</p>
<p>This is where <span class="sk" data-sk="Startling Kick"></span> comes in, and it is our strongest repositioning tool that new Slayers do not use enough. I always try to keep it out of the normal rotation for exactly this reason.</p>
<h3>Abusing boss pushback</h3>
<p>For bosses that jump backwards (Dragon's Landing, for example): as the boss jumps back, hold S and time the <span class="sk" data-sk="Startling Kick"></span> so you end up inside the boss hitbox. From there you can abuse your chains — or even <span class="sk" data-sk="Distant Blade"></span> and auto attacks — to get pushed out directly behind the boss.</p>
<div class="callout"><b>Dodge rolling for position.</b> Always roll <b>through</b> the boss, never off to the side at an angle. Roll directly to the back, and if you can reach, use the pushback trick to get spat out there. The worst thing you can do is double dodge roll for positioning — that is probably the number one reason you die.</div>
</section>

<section>
<h2>Managing defensives</h2>
<p>This is the hardest part of playing Slayer. We have two skills that give iframes: <span class="sk" data-sk="Backstab"></span> and dodge roll.</p>
<h3>Backstab</h3>
<p>It bugs easily when the boss moves out of range or there is no space to teleport behind. The startup is slow and it does not chain into anything, so taking the glyph for +% speed on other skills is a bit of a grief pick. The good news: you are invulnerable during the travel and for a short window afterwards.</p>
<h3>Dodge roll</h3>
<p>Understanding and planning your rolls is what keeps you alive. Slayer is unusual in getting two rolls back to back on a 4-second cooldown — but rolling twice in a row is the worst thing you can do.</p>
<p>Because you store a charge: roll once, wait 4 seconds, and the charge replenishes — so you can roll again, and then twice more if you need to.</p>
<ol class="steps">
<li>Use your first dodge on the incoming attack.</li>
<li>Handle the second attack another way — reposition early, or use the <span class="sk" data-sk="Backstab"></span> iframe.</li>
<li>By then your charges have refreshed, and you have two iframes available if you need them.</li>
</ol>
</section>

<section>
<h2>Where the numbers come from</h2>
<div class="linkcard"><div class="t" id="srcNote"></div><a href="../slayer-build/">Build data →</a></div>
</section>
</div>
<script>
const C=__DATA__;
const pc=n=>n==null?'-':Math.round(n*100)+'%';
const f1=n=>n==null?'-':n.toFixed(1);
// inline skill chips
document.querySelectorAll('.sk[data-sk]').forEach(el=>{const n=el.dataset.sk,ic=C.icons[n];
 el.innerHTML=(ic?`<img src="${ic}" alt="">`:'')+n});
// crystal data
const cr=C.crystals;
document.getElementById('crystalData').innerHTML=`<table><thead><tr><th>slot</th><th>what the top 25 run</th><th></th></tr></thead><tbody>`+
 Object.entries(cr).map(([k,v])=>`<tr><td><b>${k}</b></td><td>${v.sets[0].value}</td><td class="n">${pc(v.sets[0].share)}</td></tr>`).join('')+`</tbody></table>`;
// weapon rolls
const wr=C.gearRolls.Weapon;
document.getElementById('weaponData').innerHTML=`<table><thead><tr><th>weapon line</th><th>top 25 carrying it</th><th>running two</th></tr></thead><tbody>`+
 wr.lines.slice(0,5).map(l=>`<tr><td><b>${l.value}</b></td><td>${pc(l.share)}</td><td class="n">${l.dbl>0?pc(l.dbl):'-'}</td></tr>`).join('')+`</tbody></table>`;
// armor rolls
document.getElementById('armorData').innerHTML=['Chest','Gloves','Boots'].map(k=>{const v=C.gearRolls[k];
 return `<table style="margin-bottom:12px"><thead><tr><th>${k} · ${v.slots} rolls</th><th>top 25</th></tr></thead><tbody>`+
 v.lines.slice(0,3).map(l=>`<tr><td>${l.value}</td><td class="n">${pc(l.share)}</td></tr>`).join('')+`</tbody></table>`}).join('');
// jewelry
const jw=C.jewelry.slice().sort((a,b)=>b.n-a.n)[0];
document.getElementById('jewelData').innerHTML=`<div class="callout">That is the <b>${jw.value}</b> split, which <b>${pc(jw.share)}</b> of shortlisted players run — the most common setup by a distance. Measured crit rate across the shortlist sits at <b>${f1(C.split.top.crit)}%</b> for the top third of Calamity Helghan.</div>`;
// brooch
const br=C.runs.brooch;
document.getElementById('broochData').innerHTML=`<table><thead><tr><th>brooch</th><th>top 25 running it</th></tr></thead><tbody>`+
 br.map(b=>`<tr><td><b>${b.value}</b></td><td>${pc(b.share)}</td></tr>`).join('')+`</tbody></table>`;
// glyph tiers by measured adoption
const gl=Object.entries(C.glyphs).map(([id,g])=>({id:+id,...g})).sort((a,b)=>b.share-a.share);
const card=(g,cls)=>`<div class="gcard ${cls}">${g.icon?`<img src="${g.icon}" alt="">`:''}<div><div class="nm">${g.label}</div><div class="mt">${g.points?g.points+' pts · ':''}${pc(g.share)} of top 25${g.desc?' · '+(g.vague?'~ ':'')+g.desc:''}</div></div></div>`;
const CORE=[23080], HIDE=[23058];   // Carving Knockdown Strike / Keen Overpower, by id
const tier=g=>HIDE.includes(g.id)?null:(CORE.includes(g.id)||g.share>=0.9?'red':g.share>=0.35?'yel':g.share>=0.1?'blu':null);
document.getElementById('gRed').innerHTML=gl.filter(g=>tier(g)==='red').map(g=>card(g,'red')).join('');
document.getElementById('gYel').innerHTML=gl.filter(g=>tier(g)==='yel').map(g=>card(g,'yel')).join('');
document.getElementById('gBlu').innerHTML=gl.filter(g=>tier(g)==='blu').map(g=>card(g,'blu')).join('');
// damage split
const rot=C.rotation.filter(r=>r.name!=='(unnamed)'&&r.share>=1);
document.getElementById('dmgData').innerHTML=`<table><thead><tr><th>skill</th><th>share of damage</th><th>casts / min</th><th>crit rate</th></tr></thead><tbody>`+
 rot.map(r=>`<tr><td><b>${r.name}</b></td><td><b>${f1(r.share)}%</b></td><td>${f1(r.cpm)}</td><td class="n">${f1(r.crit)}%</td></tr>`).join('')+`</tbody></table>`;
// chain
const chain=[['Any starter',null],['Overhand Strike','Overhand Strike'],['starter (if up)',null],['Overhand Strike (if reset)','Overhand Strike'],['next starter (if up)',null]];
document.getElementById('chain').innerHTML=chain.map(([l,sk],i)=>
 `${i?'<span class="arw">&rsaquo;</span>':''}<span class="sk">${sk&&C.icons[sk]?`<img src="${C.icons[sk]}" alt="">`:''}${l}</span>`).join('');
const step=(sk,note)=>`<div class="st"><span class="sk">${sk&&C.icons[sk]?`<img src="${C.icons[sk]}" alt="">`:''}${sk||''}</span>${note?`<span class="stn">${note}</span>`:''}</div>`;
const seq=(arr)=>arr.map((x,i)=>(i?'<span class="arw">&rsaquo;</span>':'')+step(x[0],x[1])).join('');
document.getElementById('opener').innerHTML=seq([
 ['Distant Blade','prepull, for the attack speed glyph'],['In Cold Blood','with brooch'],['Knockdown Strike',''],['Overhand Strike',''],
 ['Eviscerate',''],['Overhand Strike','100% reset chance inside In Cold Blood'],['Measured Slice',''],
 ['Fury Strike','if not glyphed, prioritise Heart Thrust'],['Overhand Strike',''],['Headlong Rush',''],['Whirlwind',''],
 ['Overhand Strike',''],['Eviscerate',''],['Overhand Strike','still inside In Cold Blood'],['Measured Slice',''],['Heart Thrust',''],['Overhand Strike','']]);
document.getElementById('seqBad').innerHTML=seq([['Knockdown Strike',''],['Overhand Strike',''],['Eviscerate',''],['Overhand Strike','no reset']]);
document.getElementById('seqGood').innerHTML=seq([['Knockdown Strike',''],['Overhand Strike',''],['Heart Thrust',''],['Eviscerate',''],['Measured Slice','']]);

document.getElementById('srcNote').textContent=`Percentages on this page are measured from ${C.dataset.shortlistParses} parses by the top 25 players on each of ${C.dataset.boards} endgame bosses.`;
</script>
"""
html=html.replace("__CSS__",css).replace("__DATA__",DATA)
open("guide.html","w",encoding="utf-8").write(html)
open("slayer-guide/index.html","w",encoding="utf-8").write('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width"></head><body style="margin:0">'+html+'</body></html>')
print("ok",len(html))
