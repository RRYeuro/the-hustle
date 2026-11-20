import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':420,'height':860});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:200]) if m.type=='error' and 'sk38' in m.text else None)
    pg.goto('file:///home/claude/the-hustle/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S.jew={};S.fit='street';S.rep=0;S._evDay=S.day;render()}")
    r=J("()=>{const o={};o.none=l38();S.jew={chain:1};o.fresh=l38();S.jew={chain:1,grill:1};o.flashy=l38();S.jew={chain:1,grill:1,ring:1};S.fits={drip:1};S.fit='drip';o.iced=l38();S.jew={chain:1,grill:1,ring:1,watch:1,pend:1};o.top=l38();return o}")
    ck('tiers: none, Fresh 2, Flashy 5, Iced out 9, Untouchable 17',[r[k]['name'] for k in ['none','fresh','flashy','iced','top']]==['No drip','Fresh','Flashy','Iced out','Untouchable'],json.dumps({k:[r[k]['n'],r[k]['name']] for k in r}))
    ck('rep 0: drip is fake, no snitch help',r['iced']['backed']==False and r['iced']['mul']==1)
    r=J("()=>{S.jew={chain:1,grill:1,ring:1};S.fit='drip';S.rep=27;return l38()}")
    ck('rep 27 backs Iced out: snitch odds x0.65',r['backed'] and r['mul']==0.65,json.dumps(r))
    # respect and loyalty
    J("()=>{S.crews=S.crews||[];const c=S.crews.find(x=>x.alive!==false);S.at=0;S.owner[0]=c.id;c.respect=10;window._c=c;S.soldiers=2;const M=crewList();M.forEach(m=>m.loy=50);S.day=30;WD.find(f=>f.name==='day'&&/l38|drip|respect/.test(f.toString()))?0:0}")
    J("()=>{const f=WD.find(f=>/sk38 day/.test(f.toString()));f();window._r1=window._c.respect;window._l1=crewList().map(m=>m.loy)}")
    ck('Iced out and backed: crew on this block +2 respect, your crew +2 loyalty every 3 days',J("()=>window._r1")==12 and J("()=>window._l1")==[52,52],str([J("()=>window._r1"),J("()=>window._l1")]))
    J("()=>{S.rep=0;window._c.respect=10;WD.find(f=>/sk38 day/.test(f.toString()))()}");ck('fake drip: no respect',J("()=>window._c.respect")==10)
    # snitch: snakeIn daily uses the multiplier
    ck('snitch rolls use the drip multiplier',J("()=>{S.rep=27;return l38Sn()}")==0.65)
    # fake drip gets robbed at low heat
    J("()=>{S.jew={chain:1,grill:1,ring:1,watch:1,pend:1};S.rep=0;S.heat=0;S.fits={};S.fit='street';const R=Math.random;Math.random=()=>0.01;try{wearDay()}finally{Math.random=R}}")
    ck('fake drip: robbed even with no heat',J("()=>!S.jew.pend")==True)
    J("()=>{document.getElementById('modal').hidden=true;S.jew={chain:1};S.rep=40;S.heat=0;const R=Math.random;Math.random=()=>0.01;try{wearDay()}finally{Math.random=R}}")
    ck('backed drip at low heat: not robbed',J("()=>!!S.jew.chain"))
    # UI
    J("()=>{document.getElementById('modal').hidden=true;tab='bag';render()}");ck('character card (bag) shows drip',J("()=>/Your drip/.test(document.getElementById('pane').textContent)"))
    J("()=>{S.at=placeAt('mall');openPlace('mall')}");ck('mall shows drip',J("()=>!!document.querySelector('#mcard .d38')"))
    J("()=>{document.getElementById('modal').hidden=true;devPanel()}");ck('dev buttons',J("()=>document.querySelectorAll('[data-d38]').length")==4)
    ck('tutorial entry',J("()=>TUT.some(t=>/Drip and status/.test(t[0]))"))
    b.close()
print('ERR',errs[:5]);print(sum(res),'/',len(res))
