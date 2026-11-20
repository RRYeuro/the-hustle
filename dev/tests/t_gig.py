import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':420,'height':860});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:200]) if m.type=='error' and 'sk37' in m.text else None)
    pg.goto('file:///home/claude/the-hustle/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S.cash=1000;S.clean=200;S.heat=20;S.en=100;S.car=null;S._evDay=S.day;const X=w4();X.dv=X.tow=X.taxi=-9;S.gigD=-9;tab='biz';render()}")
    J("()=>{tab='phone';render()}");pg.wait_for_timeout(300);J("()=>{const l=document.querySelector('#pane [data-unlock]');if(l&&!document.querySelector('#pane [data-rph]'))l.click()}");pg.wait_for_timeout(300)
    J("()=>document.querySelector('#pane [data-rph=\"hustle\"]').click()");pg.wait_for_timeout(400);J("()=>{window._tile='hustle app'}")
    print('  tile:',J("()=>window._tile"))
    r=J("()=>({dv:!!document.querySelector('#pane [data-a=\"w4_dv\"]'),tow:!!document.querySelector('#pane [data-a=\"w4_tow\"]'),taxi:[...document.querySelectorAll('#pane [data-a=\"gig_taxi\"]')].map(b=>b.disabled+':'+b.textContent)})")
    ck('Side hustles app: delivery, tow and a locked taxi (no car)',r['dv'] and r['tow'] and r['taxi']==['true:You need your own car.'] or r['taxi']==['true:Locked'],json.dumps(r))
    # delivery via keyboard
    J("()=>act('w4_dv',{dataset:{}})");pg.wait_for_timeout(200)
    ck('delivery opens on a tutorial card',J("()=>!!document.getElementById('gst')"))
    pg.keyboard.press('Enter');pg.wait_for_timeout(200)
    ck('lane game running',J("()=>!!document.getElementById('ln')&&mgOn===true"))
    pg.keyboard.press('ArrowLeft');pg.wait_for_timeout(120);l=J("()=>__gig37.lane()");pg.keyboard.press('ArrowRight');pg.keyboard.press('ArrowRight');pg.wait_for_timeout(120);l2=J("()=>__gig37.lane()")
    ck('arrow keys switch lanes',l==0 and l2==2,str([l,l2]))
    c0=J("()=>S.cash");cl0=J("()=>cleanCash()")
    J("()=>__gig37.done(10,0)");pg.wait_for_timeout(200)
    r=J("(a)=>({pay:S.cash-a[0],clean:cleanCash()-a[1],flag:w4().dv===S.day,gig:S.gigD===S.day,mg:mgOn})",[c0,cl0])
    ck('perfect delivery pays $150 clean, uses the daily slot',r['pay']==150 and r['clean']==150 and r['flag'] and r['gig'] and r['mg']==False,json.dumps(r))
    J("()=>{const c=S.cash;act('md_gig',{dataset:{}});window._c=S.cash-c}")
    ck('second delivery shift shares the slot',J("()=>window._c===0&&/Done today/.test(S.log[0].t)"),J("()=>S.log[0].t"))
    # tow
    J("()=>{document.getElementById('modal').hidden=true;act('w4_tow',{dataset:{}})}");pg.keyboard.press('Enter');pg.wait_for_timeout(200)
    ck('tow hook game running',J("()=>!!document.getElementById('tw')"))
    c0=J("()=>S.cash");J("()=>{Math._r=Math.random;Math.random=()=>0.9;__gig37.done(2,2);Math.random=Math._r}");pg.wait_for_timeout(200)
    ck('half the cars hooked pays about half',J("(c)=>S.cash-c",c0)==135,str(J("(c)=>S.cash-c",c0)))
    # taxi
    J("()=>{S.car='stolen';render()}");ck('stolen car: no rideshare',J("()=>{const c=S.cash;act('gig_taxi',{dataset:{}});return S.cash===c&&/stolen/.test(S.log[0].t)}"))
    J("()=>{S.car='civic';S.inv.loud=0;act('gig_taxi',{dataset:{}})}");pg.keyboard.press('Enter');pg.wait_for_timeout(200)
    c0=J("()=>S.cash");J("()=>__gig37.done(9,0)");pg.wait_for_timeout(200)
    pay=J("(c)=>S.cash-c",c0)
    ck('great rideshare shift pays $230 plus tips',245<=pay<=275,str(pay))
    # age, monitor, energy
    J("()=>{const X=w4();X.dv=X.tow=X.taxi=-9;S.age=15;act('w4_dv',{dataset:{}})}");ck('under 16: no delivery',J("()=>document.getElementById('modal').hidden&&/16/.test(S.log[0].t)"))
    J("()=>{S.age=17;act('w4_tow',{dataset:{}})}");ck('under 18: no tow',J("()=>document.getElementById('modal').hidden&&/18/.test(S.log[0].t)"))
    J("()=>{S.age=19;S.ha=1;S.haOK=-1;act('w4_dv',{dataset:{}})}");ck('ankle monitor: no gigs',J("()=>document.getElementById('modal').hidden"));J("()=>{S.ha=0}")
    J("()=>{document.getElementById('modal').hidden=true;devPanel()}");ck('dev buttons',J("()=>document.querySelectorAll('[data-d37]').length")==4)
    ck('tutorial entry',J("()=>TUT.some(t=>/Side gigs/.test(t[0]))"))
    b.close()
print('ERR',errs[:5]);print(sum(res),'/',len(res))
