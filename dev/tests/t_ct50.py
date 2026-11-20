import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1280,'height':900});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:200]) if m.type=='error' and 'sk' in m.text else None)
    pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S.cash=5000;S.en=100;S._evDay=S.day;S.picQ=[];S.friends=[{name:'Bri',trait:'wild',role:'none',close:25}];S.inbox=[];tab='phone';window._rph='contacts';render()}")
    pg.wait_for_timeout(300)
    ck('friend card in Contacts has one Text button, no menu',J("()=>!!document.querySelector('[data-tx50]')&&!document.querySelector('.phx[data-app=\"contacts\"] [data-a=\"fhang\"]')"),J("()=>document.querySelector('.phx')?document.querySelector('.phx').innerText.slice(0,300):'nophx'"))
    ck('Bri listed as a contact',J("()=>window._MC().some(c=>c.n==='Bri')"))
    J("()=>document.querySelector('[data-tx50]').click()");pg.wait_for_timeout(300)
    ck('Text opens her thread with texting options',J("()=>window._mth==='Bri'&&document.querySelectorAll('.mth-kb [data-fr50]').length>=3"),J("()=>document.querySelector('.phx')?document.querySelector('.phx').innerText.slice(0,300):''"))
    pg.screenshot(path='/tmp/claude-0/s43/thread.png')
    J("()=>document.querySelector('.mth-kb [data-fr50=\"hang\"]').click()");pg.wait_for_timeout(1300)
    r=J("()=>({a:S.inbox[0],b:S.inbox[1],h:S.friends[0].hang,d:S.day})")
    ck('text "wanna kick it": you text, it happens, she texts back',r['a']['f']=='Bri' and r['b']['f']=='You' and r['h']==r['d'],json.dumps(r))
    ck('no errors',not errs,json.dumps(errs[:5]))
    b.close()
print(sum(res),'/',len(res))
