import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;S.age=19;S._evDay=S.day;S.picQ=[];S.fd=null;S.day=1;S.lvl=1;S.rk=0;S.app57=null;tab='phone';window._rph=null;window._ph=1;render()}");pg.wait_for_timeout(300)
    J("()=>{const u=document.querySelector('[data-unlock]');if(u&&document.querySelector('.ph-lock'))u.click()}");pg.wait_for_timeout(300)
    vis=J("()=>[...document.querySelectorAll('.ph-home .ph-ic button[data-rph]')].filter(b=>b.style.display!=='none').map(b=>b.dataset.rph)")
    ck('day 1: simple phone, no licks/trap/orders',vis and 'licks' not in vis and 'trap' not in vis and 'orders' not in vis,json.dumps(vis))
    ck('locked note shows',J("()=>!!document.querySelector('.lk57')"))
    J("()=>{S.day=3;render()}");pg.wait_for_timeout(200)
    J("()=>{const u=document.querySelector('[data-unlock]');if(u&&document.querySelector('.ph-lock'))u.click()}");pg.wait_for_timeout(300)
    ck('day 3: Social unlocks with NEW + text',J("()=>{const b=document.querySelector('.ph-home [data-rph=\"social\"]');return b&&b.style.display!=='none'&&b.classList.contains('nw57')&&S.log.some(x=>/New app on your phone: Social/.test(x.t))}"))
    J("()=>{S.lvl=6;addXP(1);render()}");pg.wait_for_timeout(200)
    J("()=>{const u=document.querySelector('[data-unlock]');if(u&&document.querySelector('.ph-lock'))u.click()}");pg.wait_for_timeout(300)
    ck('Middle Man: backer unlocks',J("()=>['backer'].every(id=>{const b=document.querySelector('.ph-home [data-rph=\"'+id+'\"]');return b&&b.style.display!=='none'})"))
    pg.screenshot(path='/tmp/claude-0/s43/a57.png')
    ck('no errors',not errs,json.dumps(errs[:3]))
    b.close()
print(sum(res),'/',len(res))
