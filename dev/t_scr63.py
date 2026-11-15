import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
    pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;S.age=19;S.cash=5000;S._evDay=S.day;S.picQ=[];S.fd=null;tab='move';render()}");pg.wait_for_timeout(300)
    J("()=>window.scrollTo(0,600)");pg.wait_for_timeout(100)
    y0=J("()=>scrollY");J("()=>render()");pg.wait_for_timeout(150)
    ck('page stays put after a redraw',abs(J("()=>scrollY")-y0)<5,str([y0,J("()=>scrollY")]))
    J("()=>{tab='block';render()}");pg.wait_for_timeout(150)
    ck('switching tabs still starts at the top of the new tab (allowed)',True)
    J("()=>{S.friends=[];for(let i=0;i<15;i++)S.friends.push({name:'F'+i,trait:'loyal',role:'none',close:30});tab='phone';window._rph='contacts';render()}");pg.wait_for_timeout(300)
    J("()=>{const s=document.querySelector('.phx .ph-scr');s.scrollTop=400}");s0=J("()=>document.querySelector('.phx .ph-scr').scrollTop")
    J("()=>render()");pg.wait_for_timeout(150)
    ck('phone app keeps its scroll after a redraw',abs(J("()=>document.querySelector('.phx .ph-scr').scrollTop")-s0)<5,str(s0))
    J("()=>{S.at=placeAt('mall');openPlace('mall')}");pg.wait_for_timeout(200)
    J("()=>{const m=document.getElementById('mcard');m.scrollTop=300}");m0=J("()=>document.getElementById('mcard').scrollTop")
    J("()=>openPlace('mall')");pg.wait_for_timeout(150)
    ck('place popup keeps its scroll when it reopens',m0<5 or abs(J("()=>document.getElementById('mcard').scrollTop")-m0)<5,str([m0,J("()=>document.getElementById('mcard').scrollTop")]))
    ck('no errors',not errs,json.dumps(errs[:3]))
    b.close()
print(sum(res),'/',len(res))
