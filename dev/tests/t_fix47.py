import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cash=5000;S._evDay=S.day;S.picQ=[];render()}")
    J("()=>{l42q('g_patrol','Patrol','a');l42q('g_raidup','Task force','b');l42q('overdue','Bills','c');render()}");pg.wait_for_timeout(900)
    ck('3 popups become one What happened card',J("()=>/What happened/.test(document.querySelector('#mcard h2').textContent)&&document.querySelectorAll('#mcard .mr47').length===3"))
    J("()=>document.getElementById('ok42').click()");pg.wait_for_timeout(900);ck('one tap clears them all',J("()=>document.getElementById('modal').hidden&&!S.picQ.length"))
    J("()=>{w4().bail={d:S.day,len:3,charge:'x',amt:0};}");ck('street events wait on trial day',J("()=>l47Busy()==='trial'"))
    J("()=>{w4().bail=null;let fired=0;const o=window.streetEvent;S.meet={bi:S.known[0],how:'go',from:S.at};streetEvent();S.meet=null;return 1}")
    ck('no street event during a meet',J("()=>document.getElementById('modal').hidden"))
    J("()=>{wCard('g_court','Big',('x ').repeat(300),[{l:'a'},{l:'b'},{l:'c'},{l:'d'}])}");ck('long card gets thin picture',J("()=>document.getElementById('mcard').classList.contains('long47')"))
    J("()=>{document.getElementById('modal').hidden=true;wNote('g_court','Small','short')}");ck('short card keeps normal picture',J("()=>!document.getElementById('mcard').classList.contains('long47')"))
    ck('text banner hidden while a popup is open',J("()=>{phoneMsg('Dre','yo');const s=document.getElementById('sms');return !s||getComputedStyle(s).opacity==='0'}"))
    ck('no errors',not errs,json.dumps(errs[:5]))
    b.close()
print(sum(res),'/',len(res))
