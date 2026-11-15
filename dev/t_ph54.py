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
    pg.screenshot(path='/tmp/claude-0/s43/p54_contacts.png')
    ck('contacts: long explainers fold into ⓘ',J("()=>document.querySelectorAll('.phx details.i54').length")>=1)
    ck('phone buttons not uppercase',J("()=>{const b=document.querySelector('.phx .btn');return !b||getComputedStyle(b).textTransform==='none'}"))
    mama=J("()=>S.par?S.par.name:'Mama'")
    J("(n)=>{S.inbox.unshift({d:S.day,f:n,t:'Hey baby'});window._rph='messages';window._mth=n;render()}",mama);pg.wait_for_timeout(300)
    ck('family thread has real options',J("()=>document.querySelectorAll('.mth-kb [data-a54]').length")==3,J("()=>document.querySelector('.mth-kb').innerText"))
    pg.screenshot(path='/tmp/claude-0/s43/p54_mama.png')
    J("()=>document.querySelector('[data-a54=\"send\"]').click()");pg.wait_for_timeout(1300)
    r=J("(n)=>({c:S.cash,a:S.inbox[0],b:S.inbox[1]})",mama);ck('send $100: money goes, you text, she answers',r['c']==1900 and r['a']['f']==mama and r['b']['f']=='You',json.dumps(r))
    ck('send is once a day',J("()=>document.querySelector('[data-a54=\"send\"]').disabled"))
    # crew member
    r=J("()=>{try{const m=crewList()[0];return m?m.name:null}catch(e){return null}}")
    if r:
        J("(n)=>{S.inbox.unshift({d:S.day,f:n,t:'yo'});window._mth=n;render()}",r);pg.wait_for_timeout(300)
        ck('crew thread: check in / bonus',J("()=>document.querySelectorAll('.mth-kb [data-a54]').length")==3)
    ck('no errors',not errs,json.dumps(errs[:3]))
    b.close()
print(sum(res),'/',len(res))
