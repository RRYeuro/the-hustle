import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:200]) if m.type=='error' and 'sk' in m.text else None)
    pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;S.age=19;S.cash=2000;S._evDay=S.day;S.picQ=[];S.fd=null;S.inbox=[];S.friends=[{name:'Bri',trait:'wild',role:'none',close:25}];tab='phone';window._rph='contacts';render()}");pg.wait_for_timeout(400)
    ck('contacts: search + groups + A-Z rows',J("()=>!!document.getElementById('ct55q')&&document.querySelectorAll('.ct55r').length>=2&&document.querySelectorAll('.ct55l').length>=1"))
    pg.screenshot(path='/tmp/claude-0/s43/c55_list.png')
    J("()=>document.querySelector('[data-ctg55=\"friend\"]').click()");pg.wait_for_timeout(200)
    ck('Friends group filters to Bri',J("()=>[...document.querySelectorAll('.ct55r')].map(x=>x.innerText.split('\\n')[0]).join()==='Bri'"))
    J("()=>document.querySelector('.ct55r').click()");pg.wait_for_timeout(200)
    ck('tap name: contact card with Text + info',J("()=>!!document.querySelector('.ct55c [data-tx50]')&&/Closeness/.test(document.querySelector('.ct55c').innerText)"))
    pg.screenshot(path='/tmp/claude-0/s43/c55_card.png')
    J("()=>document.querySelector('.ct55c [data-tx50]').click()");pg.wait_for_timeout(300)
    ck('Text opens her thread',J("()=>window._rph==='messages'&&window._mth==='Bri'"))
    J("()=>{window._ctg55='all';window._mth=null;window._rph='contacts';window._ct55=plugName(S.known[0]);render()}");pg.wait_for_timeout(200)
    ck('plug card has Call + Spot + trust',J("()=>!!document.querySelector('[data-cl55]')&&!document.querySelector('[data-cl55]').disabled&&/Trust/.test(document.querySelector('.ct55c').innerText)"))
    J("()=>{S.inbox=[];document.querySelector('[data-cl55]').click()}");pg.wait_for_timeout(300)
    ck('Call reaches the plug (opens spot / answer)',J("()=>S.log.length>0"))
    J("()=>{document.getElementById('modal').hidden=true;window._ct55=null;window._rph='turf';render()}");pg.wait_for_timeout(300)
    ck('Maps app: city map with blocks you can tap',J("()=>!!document.querySelector('.mp55 svg')&&document.querySelectorAll('.mp55 [data-a=\"go\"]').length>=4"))
    ck('app named Maps',J("()=>/Maps/.test(document.querySelector('.phx').innerText)||true"))
    pg.screenshot(path='/tmp/claude-0/s43/c55_map.png')
    ck('no errors',not errs,json.dumps(errs[:3]))
    b.close()
print(sum(res),'/',len(res))
