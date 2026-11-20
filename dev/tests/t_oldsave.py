import json
from playwright.sync_api import sync_playwright
CHK="""()=>{const b=[];const n=x=>typeof x==='number'&&isFinite(x);if(!n(S.cash))b.push('cash');if(!n(S.heat))b.push('heat');if(!n(S.rep))b.push('rep');if(!n(S.day))b.push('day');
 try{GOODS.forEach(g=>{if(!n(S.inv[g.id]))b.push('inv '+g.id)})}catch(e){b.push('goods '+e)}const t=document.body.innerText;if(/\\bNaN\\b|undefined|\\[object Object\\]/.test(t)){const m=/.{0,40}(\\bNaN\\b|undefined|\\[object Object\\]).{0,20}/.exec(t);b.push('text: '+(m?m[0]:''))}return b}"""
with sync_playwright() as p:
    b=p.chromium.launch();c=b.new_context(viewport={'width':420,'height':860});pg=c.new_page();er=[];pg.on('pageerror',lambda e:er.append(str(e)[:200]))
    pg.goto('file:///tmp/claude-0/old/index.html',wait_until='load');pg.wait_for_timeout(2500);J=pg.evaluate
    old=J("""()=>{startLife('val');document.getElementById('modal').hidden=true;S.age=19;S.cal=0;S.school='out';S.cash=40000;S.clean=10000;S.rep=60;S.robOn=1;S.soldiers=3;S.known=[0,1,2,3];S.trust=S.trust.map(()=>70);
      try{S.traps[S.at]={w:null,g:null}}catch(e){}S.inv.loud=200;S.bag=1;S.car='civic';S.jew={chain:1};S.slot=S.slot||1;
      for(let i=0;i<6;i++){try{S._evDay=S.day;nextDay()}catch(e){}document.getElementById('modal').hidden=true}
      save();const ls={};for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);ls[k]=localStorage.getItem(k)}return {day:S.day,keys:Object.keys(ls),slot:S.slot,ls}}""")
    print('old game: day',old['day'],'keys',old['keys'])
    ls=old['ls']
    pg2=c.new_page();pg2.on('pageerror',lambda e:er.append('NEW: '+str(e)[:200]))
    pg2.goto('file:///home/claude/the-hustle/index.html',wait_until='load');pg2.wait_for_timeout(2500);J=pg2.evaluate
    J("(ls)=>{for(const k in ls)localStorage.setItem(k,ls[k])}",ls)
    pg2.reload(wait_until='load');pg2.wait_for_timeout(2500)
    r=J("()=>{const mc=document.getElementById('mc');if(mc){mc.click();return 'continued'}try{S=load();render();return 'load()'}catch(e){return 'fail '+e}}")
    pg2.wait_for_timeout(800)
    print('new build:',r,'| day',J("()=>S&&S.day"),'| char',J("()=>S&&S.char"),'| cash',J("()=>S&&Math.round(S.cash)"))
    bad=[]
    J("()=>{document.getElementById('modal').hidden=true}")
    for t in ['block','move','biz','crew','rob','bag','phone']:
        J("(t)=>{tab=t;render()}",t);pg2.wait_for_timeout(250);J("()=>{document.getElementById('modal').hidden=true}");bad+= [t+': '+x for x in J(CHK)]
    for a in ['licks','hustle','crew','family','contacts','wallet']:
        J("()=>{tab='phone';window._rph=null;render()}");pg2.wait_for_timeout(120);J("()=>{const l=document.querySelector('#pane [data-unlock]');if(l&&!document.querySelector('#pane [data-rph]'))l.click()}")
        J("(a)=>{const e=document.querySelector('#pane [data-rph=\"'+a+'\"]');e&&e.click()}",a);pg2.wait_for_timeout(250);J("()=>{document.getElementById('modal').hidden=true}");bad+=['app '+a+': '+x for x in J(CHK)]
    for i in range(6):
        J("()=>{S._evDay=S.day;try{nextDay()}catch(e){window._nd='nextDay: '+e}document.getElementById('modal').hidden=true;tab='move';render()}");pg2.wait_for_timeout(200)
        bad+=J(CHK)
    nd=J("()=>window._nd||''")
    print('new state:',J("()=>({day:S.day,loot:Array.isArray(S.loot),pk:typeof S.pk,fd:S.fd,scan:S.scan||0,cash:Math.round(S.cash)})"))
    print('problems:',sorted(set(bad))[:10],nd)
    print('errors:',er[:8])
    b.close()
