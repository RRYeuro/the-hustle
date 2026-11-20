import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1280,'height':900});pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
    pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S._evDay=S.day;S.picQ=[];S.fd=null;S.at=homeBlock();tab='block';render()}");pg.wait_for_timeout(200)
    ck('Skip time button next to Next day',J("()=>!!document.querySelector('#pane .wq [data-sk64]')"))
    J("()=>document.querySelector('[data-sk64]').click()");pg.wait_for_timeout(200)
    ck('popup has week / next event',J("()=>{const t=document.getElementById('modal').innerText;return /week/i.test(t)&&/next event/i.test(t)}"))
    d0=J("()=>S.day");J("()=>{const b=document.querySelector('#mcard [data-a=\"lay7\"]');b&&b.click()}");pg.wait_for_timeout(800)
    ck('lay low for a week skips days',J("(d)=>S.day>d",d0),str(J("()=>S.day")))
    J("()=>{document.getElementById('modal').hidden=true;S.lt={house:S.day};tab='move';render()}");pg.wait_for_timeout(200)
    ck('no store/pharmacy lick pins, no extra trap pins',J("()=>!document.querySelector('#fm26 .lk59[data-lk59=\"store\"],#fm26 .lk59[data-lk59=\"pharm\"],#fm26 .tp61')&&!!document.querySelector('#fm26 .lk59')"))
    ck('no errors',not errs,json.dumps(errs[:3]))
    b.close()
print(sum(res),'/',len(res))
