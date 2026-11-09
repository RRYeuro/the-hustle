# Review request: The Hustle update (trap manager, choices come back, prison carries over, barber tips)
Another AI: ONLY look for potential bugs, check the logic and the balance. Do not add features or restyle anything.
Check hardest: (1) runTraps manager path (stash house stock, fake/paid/quality bookkeeping, 15% cut, mgr cleared on fire/raid/reassign, max 2); (2) slideBack/snLeak timing, jail and FF loops, old saves without S.slid; (3) prEnd rep capture, prRepDay contact (once only), poGunGate flow and the __poGunOk/__poGunViol flags, paroleCrime double-firing with poViol; (4) gfMem hooks (comma operator after the rel drop) and gfMemTick; (5) barber wtip/wrumor tip rules and S.tips shape; (6) anything that assumes S.age is set (sandbox has none).
Format: bug, where, how bad, smallest fix. One page.
Secrets are removed from this file. Art is stripped.

```diff
--- /tmp/old.html	2026-11-09 10:34:21.448288711 -0500
+++ /tmp/new.html	2026-11-09 10:34:21.450629550 -0500
@@ -559,7 +559,7 @@
   if(id==='rec'){const club=(S.age&&S.age<14)?'':row(spOn()?`${SPORTS[S.sp.kind].ic} Your team`:'🏀 Join a team',spOn()?`${SPORTS[S.sp.kind].st[S.sp.stage]} · Overall ${S.sp.ovr}. Open the Sports tab.`:S.char==='tank'?'Your comeback starts here. Join, train, play and move up.':'Pickup, tryouts and the youth leagues start here: ball, boxing, MMA, track.',b('zsjoin',spOn()?'Open':'Join',false));
     const y=(W().youth||0)>S.day-7;return row('🏀 Pickup game','Bet on a 5-shot shootout. Once a day.',b('hoops',S.park===S.day?'Played today':'Play',S.park===S.day||S.cash<100))+club+(adult()?row('👦 Run a youth camp','$600. Community +6, heat −3, rep +1. Once a week. Maybe you spot some talent.',b('wyouth',y?'Wait':'$600',y||S.cash<600)):'')}
   if(id==='stadium'){return row('🏟️ Game day',spOn()?'Your games and tryouts are in the Sports tab.':'Join a team first at the rec center.',spOn()?b('wsptab','Sports tab'):b('zsjoin','Join a team'))+(adult()&&spOn()&&S.sp.stage>=2?row('Sports agency','Run an agency: sign athletes and take a cut. Open the Business tab.',b('wagency','Open')):'')}
-  if(id==='barber'){const cd=(W().cutDay||-9)>S.day-3,sw=W().sweepDay===S.day;return row('💈 Fresh cut','$40. Rep +1, stress −4. Every few days.',b('wcut',cd?'Wait':'$40',cd||S.cash<40))+row('👂 Hear the rumors','Everybody talks in the chair. Free, once a day.',b('wrumor',W().rumDay===S.day?'Heard it':'Listen',W().rumDay===S.day))+row('🧹 Sweep up for tips','Small clean money. Costs energy.',b('wsweep',sw?'Done today':'Work',sw))+(adult()?row('📋 The bookie','Bet on games, or fix one. Once a day.',b('zsbook',spSt().bet===S.day?'Done today':'Bet',spSt().bet===S.day||(spSt().ban||0)>S.day)):'')}
+  if(id==='barber'){const cd=(W().cutDay||-9)>S.day-3,sw=W().sweepDay===S.day;return row('💈 Fresh cut','$40. Rep +1, stress −4. Every few days.',b('wcut',cd?'Wait':'$40',cd||S.cash<40))+row('💵 Tip the barber','$30. Barbers remember who tips, and the chair is where real word comes through. Once a day.',b('wtip',W().barbD===S.day?'Tipped':'$30',W().barbD===S.day||S.cash<30))+row('👂 Hear the rumors','Everybody talks in the chair. Free, once a day. Tip well and some of it is real.',b('wrumor',W().rumDay===S.day?'Heard it':'Listen',W().rumDay===S.day))+row('🧹 Sweep up for tips','Small clean money. Costs energy.',b('wsweep',sw?'Done today':'Work',sw))+(adult()?row('📋 The bookie','Bet on games, or fix one. Once a day.',b('zsbook',spSt().bet===S.day?'Done today':'Bet',spSt().bet===S.day||(spSt().ban||0)>S.day)):'')}
   return ''}
 function wavePlaceAct(k,id,back){
   if(k==='gwork'){if(S.gymDay===S.day||S.cash<30)return true;if(spendEn(10)===false)return true;S.cash-=30;S.gymDay=S.day;addStress(-8);S.hp=Math.min(100,S.hp+4);S.gymX=(S.gymX||0)+1;if(S.gymX>=6&&S.sk.muscle<10){S.gymX=0;S.sk.muscle++;say('Worked out all month. Muscle +1.')}else say('Got a workout in.');back();return true}
@@ -569,7 +569,11 @@
   if(k==='wsptab'){tab='sp';$('modal').hidden=true;render();return true}
   if(k==='wagency'){tab='biz';$('modal').hidden=true;render();return true}
   if(k==='wcut'){if((W().cutDay||-9)>S.day-3||S.cash<40)return true;S.cash-=40;W().cutDay=S.day;S.rep+=1;addStress(-4);say('Fresh cut. Rep +1.');back();return true}
-  if(k==='wrumor'){if(W().rumDay===S.day)return true;W().rumDay=S.day;const bi=rnd(0,BLOCKS.length-1),r=Math.random();say(r<.35?`Heard ${plugName(bi)} on ${BLOCKS[bi]} is getting nervous about the cops.`:r<.7?`Word is prices are about to move on ${BLOCKS[bi]}.`:`Somebody on ${BLOCKS[bi]} has been asking about you.`);back();return true}
+  if(k==='wtip'){if(W().barbD===S.day||S.cash<30)return true;S.cash-=30;W().barbD=S.day;W().barbL=(W().barbL||[]).filter(d=>d>S.day-21);W().barbL.push(S.day);say('You tipped the barber. He nodded. He will remember you.');artPop('barbtip');back();return true}
+  if(k==='wrumor'){if(W().rumDay===S.day)return true;W().rumDay=S.day;
+    {const L=(W().barbL||[]).filter(d=>d>S.day-21),cand=(S.known||[]).filter(i=>!(S.burned&&S.burned[i]>S.day)&&!(S.recr&&S.recr[i])&&!(S.tips||[]).some(t=>t.bi===i));
+     if(L.length&&cand.length&&(W().barbTipD||-9)<=S.day-3&&Math.random()<Math.min(.6,.15+.12*L.length)){W().barbTipD=S.day;const i=pick(cand),g=pick(PINFO[i].carries),disc=pick([.85,.8,.75]);S.tips=S.tips||[];S.tips.push({bi:i,g,day:S.day+1,disc,q:rnd(75,92)});say(`The barber leaned in: ${plugName(i)} on ${BLOCKS[i]} has a new load of ${G(g).name} landing tomorrow, ${Math.round((1-disc)*100)}% off for people in the know.`);artPop('barbtip');back();return true}}
+    const bi=rnd(0,BLOCKS.length-1),r=Math.random();say(r<.35?`Heard ${plugName(bi)} on ${BLOCKS[bi]} is getting nervous about the cops.`:r<.7?`Word is prices are about to move on ${BLOCKS[bi]}.`:`Somebody on ${BLOCKS[bi]} has been asking about you.`);back();return true}
   if(k==='wsweep'){if(W().sweepDay===S.day)return true;if(spendEn(6)===false)return true;W().sweepDay=S.day;const t=rnd(40,110);S.cash+=t;legit(t);say(`Swept up and got ${money(t)} in tips.`);back();return true}
   return false}
 const WACT=[];
@@ -866,7 +870,7 @@
   const go=(fee,base)=>{if(S.cash<fee)return;S.cash-=fee;const wit=(p0)=>wCard('trial','Your strategy',`Your lawyer needs a plan for the jury. ${esc(charge)}. What do you do?`,[{l:'Call an alibi witness',c:'go',dis:!(S.soldiers>0),f:()=>{let p=p0+.1;if(Math.random()<.2){const m=w4Mem()[0];if(m)m.loy=Math.max(0,m.loy-5);say('Prosecutors leaned on your witness.')}w4Verdict(Math.min(.9,p),R,len,charge,bail)}},{l:'Character witness (family)',c:'',dis:!S.par,f:()=>w4Verdict(Math.min(.9,p0+.06),R,len,charge,bail)},{l:'Attack the evidence',c:'',f:()=>w4Verdict(Math.min(.9,p0+(S.fx&&S.fx.lawyer?.1:.06)),R,len,charge,bail)},{l:'Just argue it',c:'',f:()=>w4Verdict(p0,R,len,charge,bail)}],'Court');wit(Math.min(.85,base+extra))};
   return [{l:'Public defender (free)',c:'',f:()=>go(0,.3)},{l:'Private lawyer ($2,500)',c:'go',dis:S.cash<2500,f:()=>go(2500,.5)},{l:'Top attorney ($7,000)',c:'',dis:S.cash<7000,f:()=>go(7000,.68)}]}
 function w4Court(){const R=S.pr,X=w4();if(!R||R.cc)return;R.cc=1;const len=R.len,charge=R.charge,bail=1500+len*100;
-  const opts=w4Counsel(R,len,charge,false).concat([{l:'Take the plea',c:'',f:()=>{const n=Math.max(2,Math.round(len*.7));R.len=n;R.until=R.start+n;say(`You took the plea. ${prLabel(n)} to do.`)}},{l:`Post bail (${money(bail)})`,c:'',dis:S.cash<bail,f:()=>{S.cash-=bail;X.bail={d:S.day+8,len,charge};S.pr=null;S.inJail=0;say('Posted bail. Trial in 8 days. Show up and fight it.');if(ARTX('bail'))wNote('bail','Out on bail','You have eight days. Get your lawyer ready and do not miss your court date.')}},{l:'Give up a name (snitch)',c:'red',dis:!!X.snitch,f:()=>{X.snitch=1;X.snD=S.day;w4Br(-35);S.rep=Math.max(0,S.rep-8);const n=Math.max(1,Math.round(len*.3));R.len=n;R.until=R.start+n;(S.crews||[]).forEach(c=>{if(c.alive)c.beef=Math.min(100,c.beef+10)});say(`You gave up a name. Sentence cut to ${prLabel(n)}, but the street knows.`);if(ARTX('snitch'))wNote('snitch','Marked','Word travels fast. You are a snitch now.')}}]);
+  const opts=w4Counsel(R,len,charge,false).concat([{l:'Take the plea',c:'',f:()=>{const n=Math.max(2,Math.round(len*.7));R.len=n;R.until=R.start+n;say(`You took the plea. ${prLabel(n)} to do.`)}},{l:`Post bail (${money(bail)})`,c:'',dis:S.cash<bail,f:()=>{S.cash-=bail;X.bail={d:S.day+8,len,charge};S.pr=null;S.inJail=0;say('Posted bail. Trial in 8 days. Show up and fight it.');if(ARTX('bail'))wNote('bail','Out on bail','You have eight days. Get your lawyer ready and do not miss your court date.')}},{l:'Give up a name (snitch)',c:'red',dis:!!X.snitch,f:()=>{X.snitch=1;X.snD=S.day;X.snLeak=0;w4Br(-35);S.rep=Math.max(0,S.rep-8);const n=Math.max(1,Math.round(len*.3));R.len=n;R.until=R.start+n;(S.crews||[]).forEach(c=>{if(c.alive)c.beef=Math.min(100,c.beef+10)});say(`You gave up a name. Sentence cut to ${prLabel(n)}, but the street knows.`);if(ARTX('snitch'))wNote('snitch','Marked','Word travels fast. You are a snitch now.')}}]);
   wCard('trial','Court date',`${esc(charge)}. The judge is looking at ${prLabel(len)}. Hire counsel and fight it, take the plea, post bail and go home until trial, or give a name.${X.snitch?'':' The prosecutor hints a name could make this go away.'}`,opts,'Court')}
 function w4Trial(len,charge){const X=w4();
   wCard('trial','Trial day',`You made your court date. ${esc(charge)}. Hire counsel or skip court.`,w4Counsel(null,len,charge,true).concat([{l:'Skip court',c:'red',f:()=>{S.heat=Math.min(100,S.heat+25);say('You skipped court. They added a charge.');w4Sent(Math.round(len*1.4),'Failure to appear')}}]),'Court')}
@@ -907,6 +911,7 @@
     if(X.inf){if(S.cash>=400){S.cash-=400;S.heat=Math.max(0,S.heat-5);try{const C=X8().case;if(C)C.p=Math.max(0,C.p-6)}catch(e){}w4Text('raid');if(Math.random()<.08){X.inf=0;S.heat=Math.min(100,S.heat+15);say('Your informant was working both sides. Heat jumped and he is gone.')}else say('Your informant tipped you. Heat down.')}else{X.inf=0;say('Could not pay your informant. He quit.')}}
     w4Mem().forEach(m=>{if(m.loy<25&&Math.random()<.08){say(`${m.name} stopped answering and left the crew.`);w4Quit(m)}})}
   if(X.snitch){if(!X.snD)X.snD=S.day;
+    snLeak(X);
     if(S.day-X.snD>=90){X.snitch=0;X.snD=0;say('The block finally stopped talking about it. The snitch mark is gone.')}
     else if(X.prot<=S.day&&Math.random()<.04&&!window.FF&&$('modal').hidden){
       wCard('snitch','Somebody is looking for you','Word got around that you gave up a name. A couple of guys have been asking where you stay.',[{l:'Fight them',c:'red',f:()=>{fightGame(myStr(),rnd(10,20),'The guys from the block',win=>{if(win){S.rep+=2;addXP(4);say('You handled it. They will think twice.')}else{S.hp=Math.max(5,S.hp-rnd(15,30));S.cash=Math.round(S.cash*.92);say('They caught you and took some cash.')}render()})}},{l:'Pay them $500',c:'',dis:S.cash<500,f:()=>{S.cash-=500;say('You paid them off. For now.')}},{l:'Run for it',c:'',f:()=>{copSpd=.9;window.chaseWho='The block';chase(ok=>{copSpd=1;close();if(ok){S.heat=Math.min(100,S.heat+3);say('You got away.')}else{S.hp=Math.max(5,S.hp-rnd(8,18));say('They caught up and roughed you up.')}try{checkEnd()}catch(e){}render()})}}],'Snitch')}}
@@ -930,7 +935,7 @@
   if(k==='w4_bail'){w4().bail={d:S.day,len:8,charge:'Distribution'};return done('bail trial due today, advance a day')}
   if(k==='w4_argue'){close();S.soldiers=Math.max(S.soldiers||0,3);crewList();w4Drama('argue');return true}
   if(k==='w4_raise'){close();S.soldiers=Math.max(S.soldiers||0,3);crewList();w4Drama('raise');return true}
-  if(k==='w4_snitch'){const X=w4();X.snitch=1;X.snD=S.day;X.prot=0;return done('snitch mark on')}
+  if(k==='w4_snitch'){const X=w4();X.snitch=1;X.snD=S.day;X.snLeak=0;X.prot=0;return done('snitch mark on')}
   if(k==='w4_flip'){const X=w4();X.chop=1;X.flip=-9;X.strip=-9;S.cash+=2000;return done('chop shop on, flip ready')}
   if(k==='w4_mis'){S.soldiers=Math.max(S.soldiers||0,3);crewList();w4Mem().forEach(m=>m.w4m=null);return done('3 soldiers, missions ready')}
   if(k==='w4_burn'){const X=w4();X.burn=5;X.sw=-9;S.cash+=5000;return done('5 burners')}
@@ -1206,6 +1211,7 @@
   GOODS.forEach(g=>S.pr.px[g.id]=4+Math.random()*4);S.inJail=1;S.lastStrikeLen=len}
 function prLabel(n){return S.cal?`${Math.max(1,Math.round(n/2))} week${Math.round(n/2)===1?'':'s'}`:`${n} day${n===1?'':'s'}`}
 function prEnd(early){const R=S.pr;if(!R)return;const served=S.day-R.start,place=R.place;
+  {const dl=(R.npc||[]).find(n=>n.type==='dealer'),pr=(R.g?R.g.r*10:0)+Math.round(((dl&&dl.trust)||0)/5);if(pr>0){S.prRep=Math.max(S.prRep||0,pr);S.prRepD=S.day;if(S.prRep>=20&&!S.prCon){S.prConD=S.day+rnd(2,6)}}}
   S.cash+=R.bal;S.pr=null;S.inJail=0;
   S.lockPop={n:S.strikes,place,label:prLabel(Math.max(1,served)),life:false};
   say(`Released from ${place} after ${prLabel(Math.max(1,served))}. Strike ${S.strikes} of ${maxStrikes()}.${R.bal?` Your commissary balance (${money(R.bal)}) came back to you.`:''}`);
@@ -1634,8 +1640,8 @@
   if(a==='w5b_mgr'){if(S.cash<5000||B.mgr)return true;if(needClean(5000,'A club manager'))return true;{const c0=cleanCash();S.cash-=5000;S.clean=Math.max(0,c0-5000)}B.mgr=1;say('Hired a manager for the club.');render();return true}
   if(a==='w5b_night'){if(S.cash<800||B.nightD>S.day-7)return true;S.cash-=800;B.nightD=S.day;const p=rnd(1500,4500);if(Math.random()<.12){S.heat=Math.min(100,S.heat+10);say('The club night got shut down by the fire marshal. No money, more heat.')}else{S.cash+=p;legit(p);S.rep+=1;say(`Big club night. The house cleared ${money(p)}.`)}render();return true}
   if(a==='w5b_dist'){if(S.cash<10000||B.dist||!(S.soldiers>0))return true;if(!S.car){say('You need a ride to move weight. Get a car first.');render();return true}if(needClean(10000,'A distribution route'))return true;{const c0=cleanCash();S.cash-=10000;S.clean=Math.max(0,c0-10000)}B.dist=1;say('Your distribution route is up.');render();return true}
-  if(a==='w5b_date'){if(B.dateD>S.day-3||S.cash<150||!S.gf)return true;S.cash-=150;B.dateD=S.day;S.gf.rel=Math.min(100,S.gf.rel+Math.round(8*charmMul()));addStress(-8);say('Had a good date night.');render();return true}
-  if(a==='w5b_gift'){if(B.giftD>S.day-7||S.cash<300||!S.gf||S.at!==placeAt('mall'))return true;S.cash-=300;B.giftD=S.day;S.gf.rel=Math.min(100,S.gf.rel+Math.round(12*charmMul()));say('Bought her a gift. She loved it.');render();return true}
+  if(a==='w5b_date'){if(B.dateD>S.day-3||S.cash<150||!S.gf)return true;S.cash-=150;B.dateD=S.day;S.gf.seen=S.day;S.gf.gap=0;S.gf.rel=Math.min(100,S.gf.rel+Math.round(8*charmMul()));addStress(-8);say('Had a good date night.');render();return true}
+  if(a==='w5b_gift'){if(B.giftD>S.day-7||S.cash<300||!S.gf||S.at!==placeAt('mall'))return true;S.cash-=300;B.giftD=S.day;S.gf.seen=S.day;S.gf.gap=0;S.gf.rel=Math.min(100,S.gf.rel+Math.round(12*charmMul()));say('Bought her a gift. She loved it.');render();return true}
   if(a==='w5b_run'){w5bRun(+k.i);return true}
   return false}
 WACT.push(w5bAct);
@@ -2061,9 +2067,26 @@
 /* ---------- parole ---------- */
 function poHTML(){const P=S.po;if(!P||S.pr)return '';return `<div class="sec">Parole officer</div>${a2i('parolo',300)}<div class="row" style="flex-wrap:wrap"><div class="info"><div class="t">On parole until ${dayTxt(P.until)}</div><div class="s">Check in by ${dayTxt(P.due)}. ${P.vio?`<b style="color:var(--blood)">${P.vio} violation${P.vio>1?'s':''}.</b> One more and you go back. `:''}Keep your heat down and stay clean. Your officer's office is ${BLOCKS[PO_BI]}.${S.at!==PO_BI&&P.did!==P.due?` You're on ${BLOCKS[S.at]}, so going there takes the day.`:''}</div></div>${P.did===P.due?'<button class="btn go" disabled>Checked in</button>':S.at===PO_BI?'<button class="btn go" data-a="pocheck">Check in</button>':`<button class="btn go" data-a="pogo">Head ${BLOCKS[PO_BI]} and check in</button>`}</div>`}
 const PO_BI=5;
-function poAct(a){const P=S.po;if(!P||(a!=='pocheck'&&a!=='pogo')||P.did===P.due)return;if(a==='pocheck'&&S.at!==PO_BI)return;if(!spendEn(5))return;const trip=a==='pogo';if(trip){S.at=PO_BI;say(`Went ${BLOCKS[PO_BI]} to see your parole officer.`)}P.did=P.due;addStress(4);
+function poAct(a){const P=S.po;if(!P||(a!=='pocheck'&&a!=='pogo')||P.did===P.due)return;if(a==='pocheck'&&S.at!==PO_BI)return;if(poGunGate(a))return;if(!spendEn(5))return;const trip=a==='pogo';if(trip){S.at=PO_BI;say(`Went ${BLOCKS[PO_BI]} to see your parole officer.`)}P.did=P.due;addStress(4);
+  if(window.__poGunViol)return poViol('You walked into your officer\'s office with a gun on you.');
   if(S.heat>=70&&Math.random()<.35){return poViol('Your officer did not like how things looked at the check-in.')}
   say('Checked in with your parole officer. All good.');modal(`${a2('checkin',340)}<h2>Parole check-in</h2><p>You sat across from your officer and kept it short. All good this time.${trip?' The trip took the rest of your day.':''}</p><div class="btns"><button class="btn go" id="ok">Continue</button></div>`);$('ok').onclick=()=>{close();if(trip){nextDay();checkEnd()}render()}}
+function prRepDay(){if(!(S.prRep>0)||S.pr)return;
+  if(S.day-(S.prRepD||S.day)>=7){S.prRepD=S.day;S.prRep=Math.max(0,S.prRep-1)}
+  if(S.prRep>=20&&S.prConD&&!S.prCon&&S.day>=S.prConD&&!window.FF&&!S.inJail&&!S.over&&$('modal').hidden){S.prCon=1;
+    const unk=BLOCKS.map((b,i)=>i).filter(i=>!(S.known||[]).includes(i)&&!(S.burned&&S.burned[i]>S.day));
+    if(unk.length&&Math.random()<.6){const i=pick(unk);S.known.push(i);S.trust=S.trust||{};S.trust[i]=Math.max(S.trust[i]||0,12);
+      const m=`A man you met inside texted you. He passed your name to ${plugName(i)} on ${BLOCKS[i]}. They know who you are now.`;say(m);wCard('prcall','Word from inside',m,[{l:'Good looking out',f:()=>{}}]);return}
+    const g=pick(GOODS.filter(x=>x.step>=1)),room=Math.floor((S.cap-used())/g.sp),n=Math.min(3,room);
+    if(n>=1){const each=Math.round(street(g)*.5),cost=each*n;
+      wCard('prcall','Word from inside',`A man you met inside texted you. He has ${n} ${g.name} he will move cheap, half the street price: ${money(cost)}.`,[{l:`Take it (${money(cost)})`,dis:S.cash<cost,f:()=>{if(S.cash<cost)return;S.cash-=cost;const h=S.inv[g.id];S.q[g.id]=Math.round(((S.q[g.id]||50)*h+60*n)/(h+n));S.paid[g.id]=Math.round(((S.paid[g.id]||0)*h+each*n)/(h+n));S.inv[g.id]=h+n;say(`Picked up ${n} ${g.name} from your man from inside for ${money(cost)}.`)}},{l:'Pass',f:()=>{}}])}}}
+function paroleCrime(what){if(!S.po||S.pr||S.inJail||S.heat<50)return;poViol(`Cops noticed the ${what}. Parole does not allow that.`)}
+function poGunGate(a){const gs=Object.keys(S.guns||{});if(!gs.length||window.__poGunOk)return false;
+  modal(`<h2>You are carrying</h2><p>You have ${gs.length>1?'guns':'a gun'} on you. Walking into your officer's office like that is a violation.</p><div class="btns"><button class="btn go" id="pgs">Stash it first</button><button class="btn red" id="pgy">Go in anyway</button><button class="btn" id="pgn">Never mind</button></div>`);
+  $('pgn').onclick=close;
+  $('pgs').onclick=()=>{S.vgun=S.vgun||{};let left=0;gs.forEach(k=>{if(Object.keys(S.vgun).length<VGUNS){delete S.guns[k];S.vgun[k]=1}else left++});close();if(left){say(`The safe only holds ${VGUNS} guns. ${left} still on you.`);render();return}say('Locked it in the safe before the check-in.');poAct(a)};
+  $('pgy').onclick=()=>{close();window.__poGunOk=1;window.__poGunViol=1;try{poAct(a)}finally{window.__poGunOk=0;window.__poGunViol=0}};
+  return true}
 function poViol(t){const P=S.po;if(!P)return;P.vio++;S.heat=Math.min(100,S.heat+8);say(`Parole violation. ${t}`);
   if(P.vio>=2){S.po=null;S.strikes=Math.min(maxStrikes()-1,S.strikes);window.FF=false;prStart();S.pr.len=Math.max(3,Math.round(S.pr.len*.5));S.pr.until=S.day+S.pr.len;S.pr.charge='Parole violation';say(`Parole revoked. Back in for ${prLabel(S.pr.len)}.`);return}
   if($('modal').hidden){modal(`<h2>Parole violation</h2><p>${esc(t)} That is strike one with your officer. One more and you go back in.</p><div class="btns"><button class="btn go" id="ok">Understood</button></div>`);$('ok').onclick=close}
@@ -2558,13 +2581,13 @@
 function runTraps(){const did=new Set();
   Object.entries(S.traps).forEach(([bi,t])=>{bi=+bi;const w=S.workers.find(w=>w.id===t.w);if(!w||!t.g)return;if(w.low>=S.day){did.add(w.id);return}
     if(!myBlock(bi)){say(`${w.name} couldn't work ${BLOCKS[bi]}. That's not your block no more.`);return}
-    let worked=0;
+    let worked=0;const Hm=(t.mgr&&t.mgr===t.w)?shSt():null,isM=!!(Hm&&Hm.own);if(isM&&S.day-(t.mgrL||S.day)>=14){t.mgrL=S.day;if(w.loyal<10)w.loyal++}
     trapGoods(t).slice(0,wLv(w)).forEach(gid=>{const g=G(gid);
-      w.stash=w.stash||{};w.sq=w.sq||{};const ws=(w.stash[gid]||0)>0,have=ws?w.stash[gid]:S.inv[g.id];if(have<=0){say(`${w.name} ran out of ${g.name} at the ${BLOCKS[bi]} trap.`);return}
+      w.stash=w.stash||{};w.sq=w.sq||{};const ws=(w.stash[gid]||0)>0,mg=isM&&!ws,have=ws?w.stash[gid]:(mg?(Hm.inv[g.id]||0):S.inv[g.id]);if(have<=0){say(`${w.name} ran out of ${g.name} at the ${BLOCKS[bi]} trap.`);return}
       let n=Math.min(have,Math.floor(w.hustle*(g.unit==='g'?5:g.unit==='pills'?8:1)*(.6+.4*(typeof demand==='function'?Math.min(1.2,Math.max(.4,demand(bi,g.id))):1))));if(g.step<1)n=Math.floor(n*2)/2;if(n<=0)return;
-      const fk=ws?0:Math.min(S.fake[g.id],Math.round(n*S.fake[g.id]/have));S.fake[g.id]-=fk;
-      const p=S.prices[bi]?.[g.id]??street(g);const each=p*gmult(ws?(w.sq[gid]||S.q[g.id]):S.q[g.id])*.8*Math.min(1.25,(rankAt(3)?1.15:1)*(crewOk().some(m=>(m.sk.trap||0)>=5)?1.1:1));
-      let take=Math.round((n-fk)*each+fk*each*.15);if(ws){w.stash[gid]-=n;if(w.stash[gid]<=0)w.stash[gid]=0}else{S.inv[g.id]-=n;if(S.inv[g.id]<=0){S.inv[g.id]=0;S.paid[g.id]=0;S.fake[g.id]=0}}
+      const fkS=mg?Hm.fake:S.fake,fk=ws?0:Math.min(fkS[g.id]||0,Math.round(n*(fkS[g.id]||0)/have));if(!ws)fkS[g.id]=(fkS[g.id]||0)-fk;
+      const p=S.prices[bi]?.[g.id]??street(g);const each=p*gmult(ws?(w.sq[gid]||S.q[g.id]):(mg?(Hm.q[g.id]||S.q[g.id]):S.q[g.id]))*.8*Math.min(1.25,(rankAt(3)?1.15:1)*(crewOk().some(m=>(m.sk.trap||0)>=5)?1.1:1));
+      let take=Math.round((n-fk)*each+fk*each*.15);if(mg)take=Math.round(take*.85);if(ws){w.stash[gid]-=n;if(w.stash[gid]<=0)w.stash[gid]=0}else if(mg){Hm.inv[g.id]-=n;if(Hm.inv[g.id]<=0){Hm.inv[g.id]=0;Hm.paid[g.id]=0;Hm.fake[g.id]=0}}else{S.inv[g.id]-=n;if(S.inv[g.id]<=0){S.inv[g.id]=0;S.paid[g.id]=0;S.fake[g.id]=0}}
       if(!is('val')&&Math.random()<(10-w.loyal)*.02){const stole=Math.round(take*.3);take-=stole;say(`${w.name} came up short ${money(stole)} at the ${BLOCKS[bi]} trap. Watch ${wHer(w)?'her':'him'}.`)}
       w.held=(w.held||0)+take;S.st.sold+=n*g.sp*5;worked++;
       say(`${w.name} moved ${amt(n,g)} of ${g.name} out the ${BLOCKS[bi]} trap: ${money(take)} waiting for you to collect.`)});
@@ -2575,7 +2598,7 @@
     /*F4 trap raid*/
     {const rc=(.008+S.heat/100*.025)*(1-.25*(t.up||0))*(crewRank('stash')?.6:1);
     if(t.g&&t.w===w.id&&Math.random()<rc){const lost=w.held||0;w.held=0;let keep='';if((t.up||0)>=2&&Math.random()<.5)keep=' The stash was hidden good and made it through.';else if(w.stash){Object.keys(w.stash).forEach(k=>w.stash[k]=0)}
-      t.w=null;w.low=S.day+4;S.heat=Math.min(100,S.heat+10);const msg=`Police hit the ${BLOCKS[bi]} trap. ${w.name} got picked up and ${money(lost)} in cash is gone.${keep||' The product inside went with it.'} The house is empty until you put someone back.`;
+      t.w=null;t.mgr=null;w.low=S.day+4;S.heat=Math.min(100,S.heat+10);const msg=`Police hit the ${BLOCKS[bi]} trap. ${w.name} got picked up and ${money(lost)} in cash is gone.${keep||' The product inside went with it.'} The house is empty until you put someone back.`;
       say(msg);if($('modal').hidden&&!window.FF)modal(`<h2>Trap house raided</h2><p>${msg}</p><p class="s" style="color:var(--dim)">Upgrades make the house harder to hit and hide the stash better.</p><div class="btns"><button class="btn go" id="ok">Damn</button></div>`),$('ok').onclick=close}}
   });
   (S.workers||[]).forEach(w=>{if(w.low>=S.day){did.add(w.id);return}if(w.from===undefined||!(S.recr&&S.recr[w.from])||did.has(w.id)||Object.values(S.traps||{}).some(t=>t.w===w.id))return;
@@ -2591,7 +2614,7 @@
     if(w.dry>=4&&!w.dwarn){w.dwarn=1;say(`📱 ${w.name}: "Boss, I been sitting with nothing for days. Give me some work or I'm moving on."`)}
     if(w.dry>=7&&w.loyal<9){const st=w.stash||{};Object.keys(st).forEach(k=>{if(st[k]>0)S.inv[k]=(S.inv[k]||0)+st[k]});S.cash+=(w.held||0);
       if(w.from!==undefined&&S.recr){delete S.recr[w.from];S.trust[w.from]=Math.min(S.trust[w.from]||40,40)}
-      S.workers=S.workers.filter(x=>x!==w);Object.values(S.traps).forEach(t=>{if(t.w===w.id)t.w=null});
+      S.workers=S.workers.filter(x=>x!==w);Object.values(S.traps).forEach(t=>{if(t.w===w.id){t.w=null;t.mgr=null}});
       say(`${w.name} moved on. No work for a week. ${wHer(w)?'She':'He'} handed back your product and ${money(w.held||0)}${w.from!==undefined?` and went back to plugging on ${BLOCKS[w.from]}`:''}.`)}});
   S.workers.slice().forEach(w=>{const pay=wPay(w),pc=w.pct||100,gone=(back)=>{if(back){const st=w.stash||{};Object.keys(st).forEach(k=>{if(st[k]>0)S.inv[k]=(S.inv[k]||0)+st[k]})}if(w.from!==undefined&&S.recr)delete S.recr[w.from];S.workers=S.workers.filter(x=>x!==w);Object.values(S.traps).forEach(t=>{if(t.w===w.id)t.w=null})};
     pullSafeCash(pay,'You');if(S.cash<pay){S.cash+=(w.held||0);gone(1);say(`Couldn't pay ${w.name}. ${wHer(w)?'She':'He'} quit and handed back the ${money(w.held||0)} ${wHer(w)?'she':'he'} was holding.`);return}
@@ -2608,15 +2631,17 @@
     <div class="btns"><button class="btn go" id="ok">Set pay</button><button class="btn" id="no">Cancel</button></div>`);
   const upd=()=>{const pc=+$('wp').value;{const wn=$('wn');if(wn&&document.activeElement!==wn)wn.value=pc}$('wo').textContent=pc+'%';$('wt').innerHTML=`${money(Math.round(w.wage*pc/100))}/day · ${bossTag(pc)}`};$('wp').oninput=upd;$('wn').oninput=()=>{$('wp').value=Math.max(50,Math.min(200,Math.round((+$('wn').value||100)/5)*5));upd()};upd();
   $('no').onclick=close;$('ok').onclick=()=>{w.pct=+$('wp').value;say(`${w.name} now gets ${money(wPay(w))}/day. ${w.pct<75?'He is not happy.':w.pct>=140?'He is happy.':''}`.trim());close()}}
+function trapMgrs(){return Object.values(S.traps||{}).filter(t=>t&&t.mgr&&t.mgr===t.w).length}
+function mgrBtn(i,t,w){if(!w)return '';if(t.mgr&&t.mgr===t.w)return `<button class="btn" data-a="tmgrx" data-i="${i}">Take off manager</button>`;if((w.sales||0)<10)return '';return `<button class="btn green" data-a="tmgr" data-i="${i}">Make manager</button>`}
 function paneTraps(){
   freshCands();
   const spots=BLOCKS.map((b,i)=>i).filter(myBlock);
   let h=`<div class="sec">Trap houses</div>`;
   h+=spots.map(i=>{const t=S.traps[i];
-    if(!t)return `<div class="row"><div class="info"><div class="t">${BLOCKS[i]}</div><div class="s">No trap here yet. A worker sells for you every day.</div></div><button class="btn green" data-a="trap" data-i="${i}" ${S.cash>=trapCost()?'':'disabled'}>Open ${money(trapCost())}</button></div>`;
+    if(!t)return `<div class="row"><div class="info"><div class="t">${BLOCKS[i]}</div><div class="s">No trap here yet. A worker sells for you every day.</div></div><button class="btn green" data-a="trap" data-i="${i}" ${S.cash>=trapCost()&&!(S.age&&S.age<16)?'':'disabled'}>Open ${money(trapCost())}</button></div>`;
     const w=S.workers.find(w=>w.id===t.w);
-    return `<div class="row" style="flex-wrap:wrap"><div class="info"><div class="t">${BLOCKS[i]} trap</div><div class="s">${w?`${w.name} working`:'Nobody working'} · ${t.g?`selling ${trapGoods(t).map(x=>`${G(x).name} (${S.inv[x]?amt(S.inv[x],G(x)):'none'})`).join(', ')}`:'no product picked'}</div></div>
-      <div class="btns"><button class="btn" data-a="assign" data-i="${i}">Worker</button><button class="btn" data-a="tgood" data-i="${i}">Product</button>${(t.up||0)<3?`<button class="btn green" data-a="tup" data-i="${i}" ${cleanCash()>=[3000,8000,20000][t.up||0]?'':'disabled'}>Upgrade ${money([3000,8000,20000][t.up||0])}</button>`:''}</div>${t.up?`<div class="s" style="flex-basis:100%;color:var(--dim)">Fortified, level ${t.up}. Harder for police to hit.</div>`:''}</div>`}).join('');
+    return `<div class="row" style="flex-wrap:wrap"><div class="info"><div class="t">${BLOCKS[i]} trap</div><div class="s">${w?`${w.name} ${t.mgr&&t.mgr===t.w?'managing':'working'}`:'Nobody working'} · ${t.g?`selling ${trapGoods(t).map(x=>`${G(x).name} (${S.inv[x]?amt(S.inv[x],G(x)):'none'})`).join(', ')}`:'no product picked'}</div></div>
+      <div class="btns"><button class="btn" data-a="assign" data-i="${i}">Worker</button><button class="btn" data-a="tgood" data-i="${i}">Product</button>${(t.up||0)<3?`<button class="btn green" data-a="tup" data-i="${i}" ${cleanCash()>=[3000,8000,20000][t.up||0]?'':'disabled'}>Upgrade ${money([3000,8000,20000][t.up||0])}</button>`:''}${mgrBtn(i,t,w)}</div>${t.up||(t.mgr&&t.mgr===t.w)?`<div class="s" style="flex-basis:100%;color:var(--dim)">${t.up?`Fortified, level ${t.up}. Harder for police to hit.`:''}${t.mgr&&t.mgr===t.w?` ${w?w.name:'He'} runs the house out of your stash house and keeps 15%.`:''}</div>`:''}</div>`}).join('');
   if(!spots.length)h+=`<div class="row"><div class="info"><div class="s">You need a block to open a trap. Take one from a crew.</div></div></div>`;
   const busy=id=>Object.values(S.traps).some(t=>t.w===id);
   {const tot=S.workers.reduce((a,w)=>a+(w.held||0),0);h+=`<div class="sec">Your workers (${S.workers.length})</div>`+(tot?`<div class="row" style="padding:8px 12px"><div class="info"><div class="t">${money(tot)} waiting</div><div class="s">Workers hold the money until you collect it. Low loyalty workers can skim or run.</div></div><button class="btn green" data-a="wcollectall">Collect all</button></div>`:'');}
@@ -2631,8 +2656,8 @@
   modal(`<h2>Who's working ${BLOCKS[bi]}?</h2>${S.workers.length?'':'<p>Hire a worker first.</p>'}<div class="pane">${S.workers.map((w,i)=>{const where=Object.entries(S.traps).find(([k,x])=>x.w===w.id);
     return `<button class="btn" data-w="${i}" style="text-align:left;text-transform:none">${w.name} · Hustle ${w.hustle} · Loyalty ${w.loyal}${where?` · now at ${BLOCKS[where[0]]}`:''}</button>`}).join('')}</div>
     <div class="btns"><button class="btn" id="nb">Nobody</button><button class="btn" id="no">Cancel</button></div>`);
-  $('no').onclick=close;$('nb').onclick=()=>{t.w=null;close()};
-  $('mcard').querySelectorAll('[data-w]').forEach(b=>b.onclick=()=>{const w=S.workers[+b.dataset.w];Object.values(S.traps).forEach(x=>{if(x.w===w.id)x.w=null});t.w=w.id;say(`${w.name} is working the ${BLOCKS[bi]} trap.`);close()});
+  $('no').onclick=close;$('nb').onclick=()=>{t.w=null;t.mgr=null;close()};
+  $('mcard').querySelectorAll('[data-w]').forEach(b=>b.onclick=()=>{const w=S.workers[+b.dataset.w];Object.values(S.traps).forEach(x=>{if(x.w===w.id){x.w=null;x.mgr=null}});t.mgr=null;t.w=w.id;say(`${w.name} is working the ${BLOCKS[bi]} trap.`);close()});
 }
 function trapGoodModal(bi,slot){const t=S.traps[bi],w=S.workers.find(w=>w.id===t.w),lv=w?wLv(w):1,keys=['g','g2','g3'];slot=slot||0;
   modal(`<h2>What's ${BLOCKS[bi]} selling?</h2><p>${w?`${w.name} is level ${lv}${lv<3?` (${lv===1?6-(w.sales||0):18-(w.sales||0)} more work days to level ${lv+1})`:' (max)'}. Each level adds one more product to sell.`:'Put a worker on this trap first.'} The worker sells out of your stash every day.</p>
@@ -3139,7 +3164,7 @@
   $('c4').onclick=close;
   $('c1').onclick=()=>{addCusto(nm,gid,'neighbor');S.comm=Math.min(100,(S.comm??30)+3);say(`${nm} is a regular now.`);close()};
   $('c2').onclick=()=>{addCusto(nm,pick(['loud','loud','kicks','bars']),'neighbor');S.rep+=1;say(`Gave ${nm} your number.`);close()};
-  $('c3').onclick=()=>{if(S.gf){addSide(nm);addStress(-8);say(`Took ${nm} out. ${he==='she'?'She':'He'} is on your side list.${S.gf&&Math.random()<.3?'':''}`);if(Math.random()<.3){S.gf.rel=Math.max(0,S.gf.rel-25);say(`${S.gf.name} heard about it. Relationship −25.`)}}
+  $('c3').onclick=()=>{if(S.gf){addSide(nm);addStress(-8);say(`Took ${nm} out. ${he==='she'?'She':'He'} is on your side list.${S.gf&&Math.random()<.3?'':''}`);if(Math.random()<.3){S.gf.rel=Math.max(0,S.gf.rel-25),gfMem('cheat');say(`${S.gf.name} heard about it. Relationship −25.`)}}
     else{S.gf={name:nm,rel:55,plug:null};addStress(-12);say(`You and ${nm} are together now.`)}close()}}
 function neighborAsk(){const N=NEIGH[S.home]||NEIGH.low,nm=pick(N.who),gid=pick(N.want),g=G(gid),n=g.unit==='g'?(gid==='loud'?3.5:1):g.unit==='pills'?5:1,have=S.inv[gid]>=n;
   const c=Math.round(S.comm??30);
@@ -3289,7 +3314,7 @@
   const squad=Math.round(Math.min(op.str*.7,10+S.lvl*4+Math.floor(S.rep/8)));
   modal(`<h2>Slide on the ${od.name}</h2><p>${nm} been beefing with the ${od.name}. A few of them hang out by the corner store. You could slide on them for ${him}.</p><p class="s">Your strength ${mine} vs ${squad}.</p><div class="btns"><button class="btn red" id="go">Pull up</button><button class="btn" id="no">Nah</button></div>`);
   $('no').onclick=()=>{pk.fav=_f0;pk.favs=Math.max(0,pk.favs-1);S.fx.ride=_r0;close()};
-  $('go').onclick=()=>fightGame(mine,squad,`The ${od.name}`,win=>{S.heat=Math.min(100,S.heat+15);op.beef=Math.min(100,op.beef+30);addStress(10);
+  $('go').onclick=()=>fightGame(mine,squad,`The ${od.name}`,win=>{S.heat=Math.min(100,S.heat+15);op.beef=Math.min(100,op.beef+30);S.slid=S.slid||{};S.slid[op.id]={d:S.day,fd:0,hit:0};addStress(10);
     if(win){S.trust[bi]=Math.min(100,S.trust[bi]+20);op.str=Math.max(4,op.str-3);addXP(6);brag();S.st.fights++;
       say(`Spun on the ${od.name} for ${nm}. ${He} told the homies.`);
       return lickDone('You ran them off',`The ${od.name} scattered. ${nm} heard about it before you even got back, and ${he}'s telling everybody. Trust +20, rep +5${homeCrew?`, the ${cdef(o).name} respect you more`:''}. The ${od.name} won't forget though.`,true,true)}
@@ -3413,7 +3438,7 @@
   if(!yes){S.trust[bi]=Math.max(0,S.trust[bi]-5);say(`${nm} curved you. Trust −5.`);
     modal(`<h2>Curved</h2><p>${nm} laughed and said ${she} keeps business and pleasure separate. Awkward.</p><div class="btns"><button class="btn go" id="ok">My bad</button></div>`);$('ok').onclick=close;return}
   S.trust[bi]=Math.min(100,S.trust[bi]+15);addStress(-20);k.disc=1;k.hooked=1;let extra='';
-  if(S.gf&&Math.random()<.4){S.gf.rel=Math.max(0,S.gf.rel-30);extra=` ${S.gf.name} found out. Relationship −30.`}
+  if(S.gf&&Math.random()<.4){S.gf.rel=Math.max(0,S.gf.rel-30),gfMem('cheat');extra=` ${S.gf.name} found out. Relationship −30.`}
   say(`Spent the night with ${nm}. Trust +15, and your next buy from ${her} is 30% off.${extra}`);
   modal(`<h2>Late night</h2><p>One drink turned into a few, and you ended up staying at ${nm}'s place. ${she[0].toUpperCase()+she.slice(1)} made you breakfast in the morning.</p>
     <p>Trust +15. Stress down. ${she[0].toUpperCase()+she.slice(1)} is looking out: your next buy from ${her} is 30% off.${extra}</p><div class="btns"><button class="btn go" id="ok">Continue</button></div>`);$('ok').onclick=close}
@@ -3750,7 +3775,7 @@
     if(!S.gf){S.gf={name,rel:35};{const kn=S.known.filter(i=>!(S.burned&&S.burned[i])),cs=(typeof conList==='function'?conList():[]);if(Math.random()<.25&&(kn.length||cs.length)){const useC=cs.length&&(!kn.length||Math.random()<.4);if(useC){const C=pick(cs);S.gf.dad={t:'con',n:C.name};C.tr=Math.min(100,(C.tr||50)+8)}else{const bi=pick(kn);S.gf.dad={t:'plug',bi};S.trust[bi]=Math.min(100,(S.trust[bi]||0)+10)}say(`${name} is ${dadName(S.gf.dad)}'s daughter. Treat ${p.him} right.`)}}say(`You and ${name} are talking now.`);
         modal(`<h2>${name} is real</h2><p>Y'all chilled all night. You're talking now. Keep it good with ${p.him} and you can keep your stuff at ${p.his} place.</p><div class="btns"><button class="btn go" id="ok">Bet</button></div>`)}
       else{let msg=`Had a good night with ${name}.`;addStress(-10);
-        if(Math.random()<.35){S.gf.rel=Math.max(0,S.gf.rel-25);msg+=` But ${S.gf.name} found out. Relationship −25.`;if(S.gf.dad)dadHit(12,'you cheated on '+S.gf.name)}
+        if(Math.random()<.35){S.gf.rel=Math.max(0,S.gf.rel-25),gfMem('cheat');msg+=` But ${S.gf.name} found out. Relationship −25.`;if(S.gf.dad)dadHit(12,'you cheated on '+S.gf.name)}
         if(Math.random()<.6){addSide(name);msg+=` ${name} is on your side list now.`}
         say(msg);modal(`<h2>Good night</h2><p>${msg}</p><div class="btns"><button class="btn go" id="ok">Okay</button></div>`)}
   
@@ -3758,7 +3783,7 @@
     modal(`<h2>${name}</h2><p>The night is going good. How you wanna play it with ${p.him}?</p><div class="btns"><button class="btn go" id="kp">Keep seeing ${p.him}</button><button class="btn" id="ons">One night stand</button></div>`);
     $('kp').onclick=keep;
     $('ons').onclick=()=>{addStress(-12);let msg=`One night with ${name}, no strings. Stress −12.`;
-      if(S.gf&&Math.random()<.3){S.gf.rel=Math.max(0,S.gf.rel-25);msg+=` ${S.gf.name} heard about it. Relationship −25.`}
+      if(S.gf&&Math.random()<.3){S.gf.rel=Math.max(0,S.gf.rel-25),gfMem('cheat');msg+=` ${S.gf.name} heard about it. Relationship −25.`}
       if(Math.random()<.15){addSide(name);msg+=` ${name} caught feelings and kept texting. ${name} is on your side list now.`}
       say(msg);modal(`<h2>No strings</h2><p>${msg}</p><div class="btns"><button class="btn go" id="ok">Okay</button></div>`);$('ok').onclick=close}};
 }
@@ -3922,7 +3947,7 @@
   $('fa').onclick=()=>{const g=rnd(5,9);S.comm=Math.min(100,(S.comm??30)+g);S.rep+=1;addStress(-3);const tip=Math.random()<.35?rnd(20,80):0;S.cash+=tip;done(`${f.help}. ${f.gain||nm+' appreciated it.'} Community love +${g}.${tip?` ${nm} slid you ${money(tip)}.`:''}`)};
   $('fb').onclick=()=>{const ok=Math.random()<.25+S.sk.hustle*.07+S.sk.talk*.03;if(ok){const gid=pick(['loud','loud','bars','percs']);addCusto(nm,gid);S.comm=Math.min(100,(S.comm??30)+2);addXP(2)}else{S.comm=Math.max(0,(S.comm??30)-4);S.heat=Math.min(100,S.heat+3);say(`${nm} was not with it. Word got around that you pitching on folks. Community love −4.`)}save();$('modal').hidden=true;render()};
   if($('fc'))$('fc').onclick=()=>{const ok=Math.random()<.4+S.sk.talk*.05;if(!ok){addStress(4);return done(`${nm} laughed and kept it moving.`)}
-    addSide(nm);let t=`${nm} gave you ${p.his} number. ${nm} is on your side list now.`;if(S.gf&&Math.random()<.25){S.gf.rel=Math.max(0,S.gf.rel-30);t+=` Somebody saw it and told ${S.gf.name}. Relationship −30.`}done(t)};
+    addSide(nm);let t=`${nm} gave you ${p.his} number. ${nm} is on your side list now.`;if(S.gf&&Math.random()<.25){S.gf.rel=Math.max(0,S.gf.rel-30),gfMem('cheat');t+=` Somebody saw it and told ${S.gf.name}. Relationship −30.`}done(t)};
   $('fd').onclick=()=>{const take=rnd(40,220);S.cash+=take;S.heat=Math.min(100,S.heat+10);S.comm=Math.max(0,(S.comm??30)-12);let t=`You took ${money(take)} off ${nm}. Community love −12.`;
     if(Math.random()<.3){S.heat=Math.min(100,S.heat+10);S.rep=Math.max(0,S.rep-2);t+=' Somebody saw it. Rep −2, more heat.'}
     if(Math.random()<.1){const d=rnd(5,12);S.hp-=d;t+=` ${nm} fought back and you lost ${d} health.`}done(t)}
@@ -3932,11 +3957,11 @@
   modal(`<h2>${f.name}</h2><p>${f.name} has been looking at you different lately. ${f.role==='setup'?"She still sets people up for you either way.":''}</p><div class="btns" style="flex-direction:column;align-items:stretch"><button class="btn" id="o1">One night stand</button>${inSide?'':'<button class="btn go" id="o2">Keep it going (side girl)</button>'}<button class="btn" id="o3">Keep it friends</button></div>`);
   $('o3').onclick=close;
   $('o1').onclick=()=>{f.linked=S.day;addStress(-12);let m=`One night with ${f.name}. No strings. Stress −12.`;
-    if(S.gf&&Math.random()<.3){S.gf.rel=Math.max(0,S.gf.rel-25);m+=` ${S.gf.name} heard about it. Relationship −25.`}
+    if(S.gf&&Math.random()<.3){S.gf.rel=Math.max(0,S.gf.rel-25),gfMem('cheat');m+=` ${S.gf.name} heard about it. Relationship −25.`}
     if(Math.random()<.2){f.close=Math.max(0,f.close-8);m+=` ${f.name} caught feelings. Closeness −8.`}else f.close=Math.min(100,f.close+3);
     say(m);save();modal(`<h2>No strings</h2><p>${m}</p><div class="btns"><button class="btn go" id="ok">Okay</button></div>`);$('ok').onclick=close};
   if($('o2'))$('o2').onclick=()=>{f.linked=S.day;addStress(-8);addSide(f.name);const x=S.sides.find(z=>z.name===f.name);if(x)x.friend=1;let m=`${f.name} is on your side list now, and still your friend.${f.role==='setup'?' She can still set people up for you.':''}`;
-    if(S.gf&&Math.random()<.25){S.gf.rel=Math.max(0,S.gf.rel-25);m+=` ${S.gf.name} found out. Relationship −25.`}
+    if(S.gf&&Math.random()<.25){S.gf.rel=Math.max(0,S.gf.rel-25),gfMem('cheat');m+=` ${S.gf.name} found out. Relationship −25.`}
     say(m);save();modal(`<h2>Side girl and friend</h2><p>${m}</p><div class="btns"><button class="btn go" id="ok">Okay</button></div>`);$('ok').onclick=close}}
 const SIDEQ=['Chill','A little much','Crazy'];
 function addSide(name){S.sides=S.sides||[];if(S.sides.some(x=>x.name===name))return;S.sides.push({name,crazy:rnd(5,95),since:S.day})}
@@ -3945,22 +3970,28 @@
 function sideDo(i,k){const x=(S.sides||[])[i];if(!x)return;
   if(k==='cut'){const bad=x.crazy>=60&&Math.random()<.5;S.sides.splice(i,1);if(bad){S.heat=Math.min(100,S.heat+8);addStress(8);say(`You cut ${x.name} off. ${x.name} screamed in your DMs for an hour and told everybody. Heat up.`)}else say(`You cut ${x.name} off. It went quiet.`);save();return render()}
   if(!spendEn('link'))return;S.sideDay=S.day;addStress(-8);S.cash=Math.max(0,S.cash-60);let t=`Linked up with ${x.name}. Good time. −$60.`;
-  if(S.gf&&Math.random()<.25){S.gf.rel=Math.max(0,S.gf.rel-30);t+=` ${S.gf.name} found out. Relationship −30.`}say(t);save();render()}
+  if(S.gf&&Math.random()<.25){S.gf.rel=Math.max(0,S.gf.rel-30),gfMem('cheat');t+=` ${S.gf.name} found out. Relationship −30.`}say(t);save();render()}
 function sideDay(){const L=S.sides||[];if(!L.length||window.FF||S.inJail||!adult())return;
-  if(S.gf&&Math.random()<.025*L.length){S.gf.rel=Math.max(0,S.gf.rel-25);say(`${S.gf.name} heard about the other ones. Relationship −25.`)}
+  if(S.gf&&Math.random()<.025*L.length){S.gf.rel=Math.max(0,S.gf.rel-25),gfMem('cheat');say(`${S.gf.name} heard about the other ones. Relationship −25.`)}
   if(Math.random()>.05*L.length+.03)return;const i=rnd(0,L.length-1),x=L[i],p=PR(),r=Math.random();let t,h='';
   const ev=x.crazy>=70&&r<.55?pick(['cops','shoot','fam']):pick(['spam','pullup','scare','money','keys','story']);
   if(ev==='cops'){S.heat=Math.min(100,S.heat+25);h=`${x.name} called the police on you`;t=`${x.name} told 911 you threatened ${p.him}. Heat +25.`;if(Math.random()<.15){L.splice(i,1);S.sides=L;save();say(t);S.sides=L;busted();return}}
   else if(ev==='shoot'){const dmg=Math.random()<.04*S.sk.smarts?0:rnd(10,30);S.hp-=dmg;h=`${x.name} shot at you`;t=dmg?`${x.name} pulled up with a pistol and let it go on you. You took ${dmg} damage.`:`${x.name} pulled up and shot at you. You ducked and it missed.`;L.splice(i,1)}
   else if(ev==='fam'){const lost=Math.round(S.cash*.12),d=rnd(6,14);S.cash-=lost;S.hp-=d;h=`${x.name} called ${p.his} family`;t=`${x.name} got ${p.his} cousins to catch you slipping. They took ${money(lost)} and you lost ${d} health.`}
   else if(ev==='spam'){addStress(6);h=`${x.name} blew up your phone`;t=`${x.name} sent 47 texts and 6 voicemails in one hour. "Why you ain't answering." Stress +6.`}
-  else if(ev==='pullup'){h=`${x.name} pulled up on you`;if(S.gf){S.gf.rel=Math.max(0,S.gf.rel-30);t=`${x.name} showed up while you were with ${S.gf.name}. Awkward. Relationship −30.`}else{addStress(5);t=`${x.name} showed up unannounced with a whole plan for the two of you. Stress +5.`}}
+  else if(ev==='pullup'){h=`${x.name} pulled up on you`;if(S.gf){S.gf.rel=Math.max(0,S.gf.rel-30),gfMem('cheat');t=`${x.name} showed up while you were with ${S.gf.name}. Awkward. Relationship −30.`}else{addStress(5);t=`${x.name} showed up unannounced with a whole plan for the two of you. Stress +5.`}}
   else if(ev==='scare'){addStress(15);h=`${x.name} says ${p.he} is late`;t=`You sweated for three days. It was a false alarm. Stress +15.`}
   else if(ev==='money'){const m=rnd(100,300);S.cash=Math.max(0,S.cash-m);h=`${x.name} needs a favor`;t=`"Just till Friday." You sent ${money(m)} so ${p.he} would stop texting. You will not see that again.`}
   else if(ev==='keys'){const m=S.car?rnd(150,400):0;S.cash=Math.max(0,S.cash-m);h=`${x.name} caught feelings`;t=m?`${x.name} keyed your car. Repair ran ${money(m)}.`:`${x.name} posted a long story about you. Everybody saw it.`}
   else{S.rep=Math.max(0,S.rep-2);h=`${x.name} posted you`;t=`${x.name} put your face on every story with "beware." Rep −2.`}
   say(t);S.favMsg={h,t}}
-function gfDay(){if(!S.gf)return;const p=PR();gfMood();if(S.home!=='gfplace')S.gf.rel=Math.max(0,S.gf.rel-1);else if(Math.random()<.15)S.gf.rel=Math.max(0,S.gf.rel-rnd(3,8));
+function gfMem(k){const g=S.gf;if(!g)return;g.mem=g.mem||[];g.mem.push({k,d:S.day});if(g.mem.length>8)g.mem.shift()}
+function gfMemTick(){const g=S.gf;if(!g)return;g.mem=g.mem||[];if(g.seen===undefined)g.seen=S.day;const ok=!window.FF&&!S.pr&&!S.inJail;
+  if(ok&&S.day-g.seen>=14&&!g.gap){g.gap=1;gfMem('missed')}
+  if(!ok||Math.random()>.06)return;const e=g.mem.find(m=>!m.u&&S.day-m.d>=5);if(!e)return;e.u=1;const p=PR(),n=g.name;
+  const L={cheat:[`${n} brought up what happened with the other one. ${p.he[0].toUpperCase()+p.he.slice(1)} said ${p.he} has not forgotten.`,-4],missed:[`${n} said you went weeks without coming around. ${p.he[0].toUpperCase()+p.he.slice(1)} noticed.`,-3],gift:[`${n} is still wearing what you bought ${p.him}. That meant something.`,3]}[e.k];
+  if(L){g.rel=Math.max(0,Math.min(100,g.rel+L[1]));say(L[0])}}
+function gfDay(){if(!S.gf)return;const p=PR();gfMood();gfMemTick();if(S.home!=='gfplace')S.gf.rel=Math.max(0,S.gf.rel-1);else if(Math.random()<.15)S.gf.rel=Math.max(0,S.gf.rel-rnd(3,8));
   if(S.gf.rel<25&&gUsed()>0&&Math.random()<.2){GOODS.forEach(g=>{const x=S.gst[g.id];if(x)x.n=Math.floor(x.n*.6*2)/2});say(`${S.gf.name} been going through your stuff at ${p.his} place. Some of it is gone.`)}
   if(S.gf.rel<=0){say(`${S.gf.name} is done with you. Everything you kept at ${p.his} place is gone.`);endGF()}}
 
@@ -3991,10 +4022,10 @@
 function dadName(d){return d?(d.t==='plug'?plugName(d.bi):d.n):''}
 function dadHit(amt,why){const d=S.gf&&S.gf.dad;if(!d)return;if(d.t==='plug'){S.trust[d.bi]=Math.max(0,(S.trust[d.bi]||0)-amt);if(amt>=20){S.pk[d.bi]=S.pk[d.bi]||{};S.pk[d.bi].ban=S.day+10}}else{const C=conList().find(c=>c.name===d.n);if(C)C.tr=Math.max(0,(C.tr||50)-amt)}say(`${dadName(d)} heard ${why}. That's their daughter.`)}
 function endGF(){dadHit(25,'you dumped '+(S.gf?S.gf.name:'her'));if(S.home==='gfplace'){S.cap-=HOMES.gfplace.stash;S.home='couch';say("You're back on your cousin's couch.");addStress(15)}S.gf=null;S.gst={}}
-function gfDo(k){const g=S.gf,p=PR();if(!g)return;
+function gfDo(k){const g=S.gf,p=PR();if(!g)return;if(k==='chill'||k==='out'||k==='gift'){g.seen=S.day;g.gap=0}
   if(k==='chill'){S.chill=S.day;g.rel=Math.min(100,g.rel+5);addStress(-15);say(`Chilled with ${g.name}. Stress down.`)}
   if(k==='out'){S.cash-=300;g.rel=Math.min(100,g.rel+12);say(`Took ${g.name} out to eat. Relationship +12.`)}
-  if(k==='gift'){if(g.gifted===S.day||S.cash<1000)return;g.gifted=S.day;S.cash-=1000;g.rel=Math.min(100,g.rel+25);say(`Bought ${g.name} something nice. Relationship +25.`)}
+  if(k==='gift'){if(g.gifted===S.day||S.cash<1000)return;g.gifted=S.day;S.cash-=1000;g.rel=Math.min(100,g.rel+25);gfMem('gift');say(`Bought ${g.name} something nice. Relationship +25.`)}
   if(k==='leave'){if(gUsed()>0)say(`You broke up with ${g.name}. Everything at ${p.his} place stayed there.`);else say(`You broke up with ${g.name}.`);endGF()}
   if(k==='movein'){S.cash-=300;S.grounded=0;S.gSeen=0;const old=HOMES[S.home];S.cap+=HOMES.gfplace.stash-old.stash;S.home='gfplace';S.rentDay=S.day+7;addStress(-10);say(`You moved in with ${g.name}. Y'all splitting the bills.`)}
   if(k==='moveout'){S.cap-=HOMES.gfplace.stash;S.home='couch';g.rel=Math.max(0,g.rel-15);say(`You moved out of ${g.name}'s. ${PR().he[0].toUpperCase()+PR().he.slice(1)} wasn't happy about it.`)}}
@@ -4047,7 +4078,7 @@
   if(good&&!noLick&&S.rob.c0!=null&&S.cash>S.rob.c0){const gain=S.cash-S.rob.c0,m=1/(1+(S.rob.fat||0)*.3),cut=Math.round(gain*(1-m));if(cut>0){S.cash-=cut;text+=` Word is getting around, so marks are careful. Your take is down ${money(cut)}.`}S.rob.c0=null}
   if(good&&!noLick){S.rob.fat=(S.rob.fat||0)+1;S.st.licks=(S.st.licks||0)+1;S.rob.noto+=S.rob.mask?6:5;if(S.rob.mask)S.heat=Math.max(0,S.heat-5)}
   modal(`${img?a2(img,340):''}<h2 style="color:${good?'var(--money)':'var(--blood)'}">${title}</h2><p>${text}</p><div class="btns"><button class="btn go" id="ok">Continue</button></div>`);
-  $('ok').onclick=()=>{$('modal').hidden=true;nextDay();checkEnd();render()};
+  $('ok').onclick=()=>{$('modal').hidden=true;nextDay();checkEnd();paroleCrime('job');render()};
 }
 function lickBust(title,text){lickDone(title,text,false);const _ok=$('ok');if(_ok)_ok.onclick=()=>{$('modal').hidden=true;busted();if($('modal').hidden){nextDay();checkEnd()}render()}}
 function caughtOrNot(ok,goodTitle,goodText,then){
@@ -4354,8 +4385,8 @@
  ['Block tab: the money','Buy from the plug, sell it back for a profit. Sell to the plug for safe money and respect, or serve the Js for 40% more but way more heat and beef. Some blocks have way more money than others, so check the tag on the block. Always check the grade, test for fakes, and talk price once a day.'],
  ['School tab','Going to class takes the whole school week, so do your hustles first. You get 3 moves a week: steal phones, serve classmates, fight, hack your grades, or rap at the lunch table. Get caught and it is a strike: suspended, then alt school, then expelled. Keep your grades at 70 or higher and teachers give you the benefit of the doubt. School hustles only show on school days, and only when you are at the school on Northline.'],
  ['Move tab: the city','Tap a block on the map to go there. Each block has its own plug, prices and crew. The Move tab also has hoops, dice and licks like the pharmacy and stores. The Time section lets you lay low, take a nap, skip to the next event or lay low for a whole week when things get hot.'],
- ['Spots tab: every place','The gym, rec center, stadium, stores, mall, car lot, barber, pharmacy, hospital, lawyer, school, park and studio are all listed here. Tap one to go in. If it is on another block it takes a day to get there.'],
- ['Circle tab: your people','Your fight style, trap houses, family and where you stay, homies, your girl and the crews all live here. Your fight style levels up every time you win a fight. After 18 your girl texts you, and how you answer matters. If a plug turns on you, go to their block and settle it.'],
+ ['Spots tab: every place','The gym, rec center, stadium, stores, mall, car lot, barber, pharmacy, hospital, lawyer, school, park and studio are all listed here. Tap one to go in. If it is on another block it takes a day to get there. Tip the barber and the rumors get real: a plug tip for tomorrow.'],
+ ['Circle tab: your people','Your fight style, trap houses, family and where you stay, homies, your girl and the crews all live here. Your fight style levels up every time you win a fight. After 18 your girl texts you, and how you answer matters. If a plug turns on you, go to their block and settle it. A worker who has put in enough days can be made a trap house manager: he sells out of your stash house, keeps 15%, and you can have two. What you do comes back: slide on a crew\'s opps and they may hit you or your trap later, giving up a name gets out, and your girl remembers how you treated her.'],
  ['Plugs','Every block has a plug. Do 3 deals with one and they know you: better prices, and at Talk 4 you can haggle (that is the talk rhythm game). Rob a plug and they disappear until somebody new takes over the block. With enough rep and trust you can recruit a plug to work for you: they sell whatever you front them on their block, and a trap house sells more with less heat.'],
  ['Phone tab: plays and connects','Plays text you for product. If you are out on you but it is in your safe, they go in the safe. You can see the grade of what you carry before you meet up. Once you earn a connect you can order up to 3 times a day, and you can drop one to get a shot at a better one.'],
  ['Me tab: your life','Spend skill points, handle your stash and safe, jobs and life choices. There are nine skills: Hustle, Talk, Muscle, Street Smarts and Luck, plus Stamina (energy), Charm (music and shows), Business (what your businesses pay) and Discipline (stress and grades). The traits you pick at the start are locked in for the whole run. Cash in the safe stays hidden from strict parents and can pay for things your family or remote connects ask for.'],
@@ -4364,7 +4395,7 @@
  ['Business and going legit','Buy a business once you have the clean money. It pays every week, cools your heat a little and works as a front for laundering. You can upgrade it three times, and a high Business skill makes everything pay more. Reach $100,000 clean with low heat, a business and no debts, and you can walk away clean.'],
  ['Bag, Business and Money tabs','Bag is what you carry, your ride, your place and your fits. Business holds your businesses, your label and laundering. Money shows clean and dirty cash, your bills and loans. The goal bar at the top tells you what to do next, and a red dot on a tab means something needs you.'],
  ['Sports and social media','Play sports to build your overall rating, then open an agency and sign athletes for a cut. Skip a team doctor and an injury keeps you out longer. Social media grows your followers: post often, buy a manager, open merch, get verified and sponsors pay more. Fake followers are cheap but they do not buy anything.'],
- ['Prison and parole','Get locked up and the game keeps going inside. Put money on your books, talk the dealer down and your sell price up, get a job, and learn which guards are dirty and which are strict. Call your people to collect from workers or re-up them. When you get out you are on parole: check in with your officer Downtown before the due day. Miss it or catch a violation and you go back.'],
+ ['Prison and parole','Get locked up and the game keeps going inside. Put money on your books, talk the dealer down and your sell price up, get a job, and learn which guards are dirty and which are strict. Call your people to collect from workers or re-up them. When you get out you are on parole: check in with your officer Downtown before the due day, and leave the gun at home or in the safe first. What you built inside follows you out: a man you met in there may text with a plug or a cheap deal. A lick or job that gets your heat up on parole is a violation. Miss it or catch a violation and you go back.'],
  ['Stash house and loan shark','A stash house (Me tab) keeps cash and product safe when you get busted, but it can get raided. A Stash House Leader on your crew cuts the risk in half. Need money fast? Mr. Vince in the Money tab lends it, but the interest grows every day you are late, and he sends people.'],
  ['Cops, court and protection','Heat brings arrests. In court you pick a strategy, take a plea or post bail. A lawyer, an informant on the inside and paid protection all lower the damage, and every one of them costs money. Keep your phone clean, because a new number drops heat but your plugs lose some trust.'],
  ['Big business and the casino','Clubs need staff, a manager and a distribution route, and the big buys of $5,000 or more must come from clean money. House flips cost the buy, the renovation and surprise repairs, so check the real profit. The casino is a trap: a backer will front you cash, and you owe more than you borrowed.'],
@@ -4391,7 +4422,7 @@
     <div class="sec">Wave 4 tests</div><div class="btns">${B('w4_court','Court date (jail)')}${B('w4_trial','Trial day')}${B('w4_bail','Bail trial due')}${B('w4_argue','Crew argue')}${B('w4_raise','Crew raise')}${B('w4_mis','Missions ready')}${B('w4_snitch','Snitch mark')}${B('w4_flip','Chop shop + flip')}${B('w4_burn','5 burners')}${B('w4_text','Add text')}${B('w4_br','Block rep +20')}${B('w4_inf','Informant')}${B('w4_dog','Dog')}</div><div class="sec">Wave 6 tests</div><div class="btns">${B('w6d_perk','Perk at lvl 10')}${B('w6d_ach','Badges test')}${B('w6d_wk','Weekly ready')}${B('w6d_king','Kingpin ending')}${B('w6d_end','Show final score')}${B('w6d_iron','Go Ironman')}${B('w6d_stats','All stats')}</div><div class="sec">Revamp tests</div><div class="btns">${B('rv_sch','School week at Northline')}${B('rv_wplug','Recruit a worker plug')}${B('rv_prph','Prison phone')}${B('rv_lock','Prison lockdown')}${B('rv_po','Parole due tomorrow')}${B('rv_en1','Energy full')}${B('rv_en0','Energy 0')}${B('rv_tr','Toggle Runner + Sticky')}${B('rv_wash','Reset wash limit')}${B('rv_alert','Push an alert')}${B('rv_ha','House arrest 4 days')}${B('rv_safe','$5K dirty in safe')}${B('rv_strk','Strikes to max-1')}${B('rv_soc','150K followers')}${B('rv_gf','Girlfriend 90')}</div>
     <div class="sec">New stuff</div><div class="btns">${B('hp20','Health 20')}${B('hot','Heat 80')}${B('str95','Stress 95')}${B('allg','QP of every drug')}${B('fkp','20 fake Percs')}${B('plays','3 trap phone plays')}${B('hook','Get hooked')}</div>
     <div class="btns">${B('econn','Meet the connect')}${B('dateplug','Date the plug here')}${B('crewok','Crews 75 respect')}${B('crewmad','Crews want smoke')}${B('nogang','Reset gang stuff')}${B('gcall','Gang call')}${B('gally','Ally event')}${B('bizev','Business event')}${B('strap','Gun + 2 soldiers')}${B('swstock','Unc has switches')}${B('bodies','+19 bodies')}${B('jail','Get locked up')}${B('sstrike','School strike')}${B('kid','Have a kid')}${B('kidage','Kid +5 years')}</div>
-    <div class="sec">v193 to v194 tests</div><div class="btns">${B('cclean','+$100K clean','green')}${B('cdirty','+$100K dirty','green')}${B('wdry','Workers idle +3 days')}${B('prdeal','Prison: dealer trust 60 + 2 packs')}${B('lvl30','Level 30')}${B('bills','Bills due now')}${B('lcdr','Reset lookouts')}${B('ha','House arrest')}${B('run','Cut monitor (on the run)')}${B('bizall','Own every business')}${B('bizmax','Max upgrades')}${B('szall','Stash house lvl 3')}${B('party','Reset block party')}</div>
+    <div class="sec">v193 to v194 tests</div><div class="btns">${B('cclean','+$100K clean','green')}${B('cdirty','+$100K dirty','green')}${B('wdry','Workers idle +3 days')}${B('prdeal','Prison: dealer trust 60 + 2 packs')}${B('lvl30','Level 30')}${B('bills','Bills due now')}${B('lcdr','Reset lookouts')}${B('ha','House arrest')}${B('run','Cut monitor (on the run)')}${B('bizall','Own every business')}${B('bizmax','Max upgrades')}${B('szall','Stash house lvl 3')}${B('tmgr','Trap manager test')}${B('f9','Slide + snitch window open')}${B('f8','Prison rep + parole + gun')}${B('btip','Barber trusts you (3 tips)')}${B('party','Reset block party')}</div>
     <div class="btns">${B('f5k','Rap: 5K fans')}${B('f20k','Rap: 20K fans')}${B('fnew','Rap: free agent')}${B('labopen','Open own label')}${B('labart','+3 artists')}${B('labday','Label +7 days')}${B('jew','All jewelry')}${B('jack','Get jumped')}${B('fitold','Fits wear out')}${B('bfate','Big plug decision')}${B('wait0','Clear Big plug wait')}</div>
     <div class="sec">Mini games</div><div class="btns">${B('mchase','Police chase')}${B('mshoot','Shootout')}${B('mhoop','Hoops')}${B('mdice','Dice')}${B('mcar','Steal a car')}${B('mstore','Rob store')}${B('mpharm','Rob pharmacy')}${B('mhouse','Hit a house')}${B('mscam','Fake gun sale')}</div>
     <div class="sec">Wave 3 tests (sports and social)</div><div class="btns">${B('w3_sport','Join MMA stage 3')}${B('w3_hurt','Injure 8 days')}${B('w3_endo','Endorsement offer')}${B('w3_mob','Mob offer')}${B('w3_meet','Track meet')}${B('w3_agency','Agency and bar')}${B('w3_social','60K followers')}${B('w3_dm','Test DM')}${B('w3_drama','Social drama')}</div>
@@ -4482,6 +4513,10 @@
   if(k==='bizall'){S.biz=S.biz||{};Object.keys(BIZ).forEach(x=>S.biz[x]=1);return done('own every business')}
   if(k==='bizmax'){S.bizUp=S.bizUp||{};Object.keys(S.biz||{}).forEach(x=>S.bizUp[x]=3);return done('all businesses level 4')}
   if(k==='szall'){const H=shSt();H.own=1;H.up=3;return done('stash house level 3')}
+  if(k==='btip'){W().barbL=[S.day,S.day,S.day];W().barbTipD=-9;W().rumDay=-9;W().barbD=-9;return done('barber trusts you: Hear the rumors now has a good chance of a real plug tip (needs a known plug)')}
+  if(k==='f8'){S.prRep=40;S.prCon=0;S.prConD=S.day;S.prRepD=S.day;S.po={until:S.day+12,sp:3,due:S.day+3,did:0,vio:0};S.guns=S.guns||{};const gk=Object.keys(GUNS)[0];S.guns[gk]=1;return done('prison rep 40 (a contact texts on the next day), parole on, one gun on you (try the check-in downtown)')}
+  if(k==='f9'){const c=(S.crews||[]).find(x=>x.alive&&!x.ally&&S.gang!==x.id);S.slid=S.slid||{};if(c)S.slid[c.id]={d:S.day-6,fd:5,hit:0};const X=w4();X.snitch=1;X.snD=S.day-56;X.snLeak=0;return done(c?'slide window open (12% a day) and the snitch paperwork will leak on the next day':'no crew to slide on')}
+  if(k==='tmgr'){const H=shSt();H.own=1;const g=GOODS[0];H.inv[g.id]=(H.inv[g.id]||0)+20;H.q[g.id]=H.q[g.id]||S.q[g.id]||50;const w=(S.workers||[])[0];if(w)w.sales=Math.max(w.sales||0,10);return done(w?`stash house + 20 ${g.name}, first worker has 10 sales. Open a trap, put him on it, pick a product, tap Make manager`:`stash house + 20 ${g.name}. Hire a worker first`)}
   if(k==='party'){S.bpDay=0;return done('block party ready')}
   if(k==='f5k'||k==='f20k'){S.rapOn=1;S.rap.fans=Math.max(S.rap.fans,k==='f5k'?5000:20000);if(!S.rap.songs.length)S.rap.songs.push({title:'Dev Song',q:70,day:S.day});return done(`fans ${S.rap.fans}`)}
   if(k==='fnew'){S.rap.signed=0;S.rap.rec=0;S.rap.take=0;S.rap.dm=1;S.rap.lbl=null;S.rap.nodeal=0;return done('free agent')}
@@ -5145,7 +5180,7 @@
   if(turf){S.cash+=turf*300;}
   {const sh=S.owner.filter(o=>o!=='me'&&o!=='none'&&crew(o)&&crew(o).ally).length;if(sh)S.cash+=sh*100}
   if(S.myGang&&S.soldiers)S.cash+=S.soldiers*50;
-  flowTick();runTraps();flowTick();crewDay();flowTick();ctDay();shDay();poDay();launDay();prisonDay();plugsHear();lickTipDay();x8Tick();try{spDay()}catch(e){}
+  flowTick();runTraps();flowTick();crewDay();flowTick();ctDay();shDay();poDay();prRepDay();launDay();prisonDay();plugsHear();lickTipDay();x8Tick();try{spDay()}catch(e){}
   gfDay();sideDay();if(S.car==='stolen'){S.heat=Math.min(100,S.heat+2);addXP(1)}favorRoll();
   shipDay();debtDay();loanDay();checkpointDay();rapDay();
   if(S.cal?calCheck():(S.day-1)%30===0)say("It's the first of the month. Checks hit and the Js got money to spend.");
@@ -5204,6 +5239,7 @@
   if(schoolRandom())return;
   if(guardianEvent())return;
   const quiet=S.quiet===S.day;
+  if(slideBack())return;
   // rival hits first
   const angry=S.crews.filter(c=>c.alive&&c.beef>=45&&!c.ally&&S.gang!==c.id).sort((a,b)=>b.beef-a.beef)[0];
   if(!quiet&&angry&&!(S.ambCD>S.day)&&Math.random()<Math.min(.22,angry.beef/300)*(rankAt(5)?.5:1)*D().risk){S.ambCD=S.day+3;return ambush(angry)}
@@ -5244,6 +5280,21 @@
   $('r').onclick=()=>{if(Math.random()<(badKnee()?.35:.55)+(S.sk.smarts-3)*.03){say(`You got away from the ${d.name}.`)}else{const dmg=vcut(rnd(10,25));S.hp-=dmg;say(`Couldn't shake the ${d.name}. −${dmg} health.`)}close()};
   $('p').onclick=()=>{S.cash-=pay;c.beef=Math.max(0,c.beef-15);S.rep=Math.max(0,S.rep-4);say(`Paid the ${d.name} ${money(pay)} to back off. Looks soft.`);close()};
 }
+function slideBack(){if(!S.slid||window.FF||S.pr||S.inJail||S.over||!$('modal').hidden||S.quiet===S.day||S.ambCD>S.day)return false;
+  for(const id of Object.keys(S.slid)){const e=S.slid[id],c=(S.crews||[]).find(x=>x.id===id);if(!e||e.hit)continue;
+    if(!c||!c.alive||c.ally||S.gang===c.id){e.hit=1;continue}
+    if(e.l!==S.day){e.l=S.day;e.fd=(e.fd||0)+1}
+    if(e.fd<5)continue;if(e.fd>15){e.hit=1;continue}
+    if(Math.random()<.12){e.hit=1;S.ambCD=S.day+7;const d=cdef(c.id);
+      const tr=Object.entries(S.traps||{}).filter(([b,t])=>t&&t.w&&(S.workers||[]).some(w=>w.id===t.w));
+      if(tr.length&&Math.random()<.5){const [b,t]=pick(tr),w=S.workers.find(x=>x.id===t.w),lost=w.held||0;w.held=0;if(w.stash)Object.keys(w.stash).forEach(k=>{w.stash[k]=Math.floor((w.stash[k]||0)*.6)});S.heat=Math.min(100,S.heat+5);c.beef=Math.min(100,c.beef+5);
+        const m=`The ${d.name} did not forget that slide. They hit the ${BLOCKS[b]} trap while ${w.name} was working.${lost?` ${money(lost)} in cash is gone and some`:' Some'} of the product went with it.`;say(m);
+        modal(`<h2 style="color:${d.color}">They hit your trap</h2><p>${m}</p><div class="btns"><button class="btn go" id="ok">Damn</button></div>`);$('ok').onclick=close;return true}
+      say(`The ${d.name} did not forget you slid on them.`);ambush(c);return true}}
+  return false}
+function snLeak(X){if(X.snLeak||window.FF||S.pr||S.inJail||S.over||!$('modal').hidden)return;const dd=S.day-X.snD;if(dd<20||dd>85)return;if(dd<55&&Math.random()>.1)return;
+  X.snLeak=1;const cs=(S.crews||[]).filter(c=>c.alive&&!c.ally&&S.gang!==c.id);if(!cs.length)return;const c=pick(cs),d=cdef(c.id);c.beef=Math.min(100,c.beef+40);
+  const m=`The paperwork got out. The ${d.name} saw your name on it and they want you.`;say(m);wCard('snitch','The paperwork got out',m,[{l:'Damn',f:()=>{}}])}
 function stealStash(f){GOODS.forEach(g=>{S.inv[g.id]-=Math.floor(S.inv[g.id]*f)})}
 const COPS={
  rookie:{name:'Rookie cop',col:'var(--heat)',txt:'Fresh out the academy. Nervous, easy to talk to, slow behind the wheel.',cool:.65,spd:.8},
@@ -5331,8 +5382,8 @@
   if(a==='use')useCard(+el.dataset.i);
   if(a==='sk'&&S.pts>0&&S.sk[el.dataset.k]<10){S.pts--;S.sk[el.dataset.k]++;say(`${SKN[el.dataset.k]} went up to ${S.sk[el.dataset.k]}.`)}
   if(a==='hoops')return hoops();
-  if(a==='trap'){if(proStop())return;const bi=+el.dataset.i;S.cash-=trapCost();S.traps[bi]={w:null,g:null};say(`Opened a trap house on ${BLOCKS[bi]}.`)}
-  if(a==='hirew'){if(S.workers.length>=3)return say('You can only run 3 workers.');const c=S.cands.splice(+el.dataset.i,1)[0];S.cash-=500;S.workers.push(c);say(`Put ${c.name} on the team for $500 up front and ${money(c.wage)} a day.`)}
+  if(a==='trap'){if(proStop())return;if(S.age&&S.age<16){say('Opening a trap house starts at 16.');return render()}const bi=+el.dataset.i;S.cash-=trapCost();S.traps[bi]={w:null,g:null};say(`Opened a trap house on ${BLOCKS[bi]}.`)}
+  if(a==='hirew'){if(S.age&&S.age<16)return say('Hiring workers starts at 16.');if(S.workers.length>=3)return say('You can only run 3 workers.');const c=S.cands.splice(+el.dataset.i,1)[0];S.cash-=500;S.workers.push(c);say(`Put ${c.name} on the team for $500 up front and ${money(c.wage)} a day.`)}
   if(a==='precruit'){recruitAsk(+el.dataset.i);return}
   if(a==='wstash')return wStashModal(+el.dataset.i);
   if(a==='wgive')return wGive(+el.dataset.i,el.dataset.g,el.dataset.m);
@@ -5340,8 +5391,10 @@
   if(a==='wcollect'){const w=S.workers[+el.dataset.i];if(w&&w.held){S.cash+=w.held;say(`Collected ${money(w.held)} from ${w.name}.`);w.held=0}}
   if(a==='wcollectall'){let t=0;S.workers.forEach(w=>{t+=w.held||0;w.held=0});if(t){S.cash+=t;say(`Collected ${money(t)} from your workers.`)}}
   if(a==='wpay')return wPayModal(+el.dataset.i);
-  if(a==='firew'){const w=S.workers.splice(+el.dataset.i,1)[0];if(w&&w.stash)Object.keys(w.stash).forEach(k=>{S.inv[k]+=w.stash[k]});if(w.from!==undefined&&S.recr)delete S.recr[w.from];S.cash+=(w.held||0);Object.values(S.traps).forEach(t=>{if(t.w===w.id)t.w=null});say(`Cut ${w.name} off.`)}
+  if(a==='firew'){const w=S.workers.splice(+el.dataset.i,1)[0];if(w&&w.stash)Object.keys(w.stash).forEach(k=>{S.inv[k]+=w.stash[k]});if(w.from!==undefined&&S.recr)delete S.recr[w.from];S.cash+=(w.held||0);Object.values(S.traps).forEach(t=>{if(t.w===w.id){t.w=null;t.mgr=null}});say(`Cut ${w.name} off.`)}
   if(a==='tup'){const bi=+el.dataset.i,t=S.traps[bi];if(!t||(t.up||0)>=3)return;const c=[3000,8000,20000][t.up||0];if(cleanCash()<c){say('Upgrades come out of clean money.');return render()}S.cash-=c;S.clean=Math.max(0,cleanCash()-c);t.up=(t.up||0)+1;say(`Fortified the ${BLOCKS[bi]} trap. Level ${t.up}. Police will have a harder time hitting it.`);return render()}
+  if(a==='tmgr'){const bi=+el.dataset.i,t=S.traps[bi],w=t&&S.workers.find(x=>x.id===t.w);if(!w)return;const hh=wHer(w)?'She':'He';if(S.age&&S.age<16){say('Too young to run a house.');return render()}if((w.sales||0)<10){say(`${w.name} needs more work days before ${hh.toLowerCase()} can run a house.`);return render()}if(!t.g){say('Pick a product for the house first.');return render()}if(!shSt().own){say('A manager sells out of your stash house. Get one first.');return render()}if(trapMgrs()>=2){say('Two managers is plenty. Take one off first.');return render()}t.mgr=w.id;t.mgrL=S.day;say(`${w.name} runs the ${BLOCKS[bi]} house now. ${hh} sells out of your stash house and keeps 15%.`);return render()}
+  if(a==='tmgrx'){const bi=+el.dataset.i,t=S.traps[bi];if(!t)return;t.mgr=null;say(`Took the manager job off at the ${BLOCKS[bi]} house. Back to selling what you front.`);return render()}
   if(a==='assign')return assignModal(+el.dataset.i);
   if(a==='tgood')return trapGoodModal(+el.dataset.i);
   if(a==='cut'){cutProduct(G(el.dataset.g),+el.dataset.p)}

```
