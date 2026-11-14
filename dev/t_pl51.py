import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1280,'height':900});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:200]) if m.type=='error' and 'sk' in m.text else None)
    pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cash=5000;S.en=100;S._evDay=S.day;S.picQ=[];S.inbox=[];render()}")
    bi=J("()=>S.known[0]");n=J("(bi)=>plugName(bi)",bi)
    h=J("(bi)=>plugActions(bi)",bi);ck('plug card: one Text button, no menu','data-tx50' in h and 'pfront' not in h and 'pkick' not in h,h[:200])
    ck('plug is a contact',J("(n)=>window._MC().some(c=>c.n===n)",n))
    J("(n)=>{S.at=(S.known[0]+1)%6;tab='phone';window._rph='messages';window._mth=n;render()}",n);pg.wait_for_timeout(300)
    ck('thread shows plug text options',J("()=>document.querySelectorAll('.mth-kb [data-p51]').length>=4"),J("()=>document.querySelector('.mth-kb')?document.querySelector('.mth-kb').innerText:''"))
    J("(bi)=>{S.trust[bi]=10}",bi)
    J("()=>document.querySelector('.mth-kb [data-p51=\"pfront\"]').click()");pg.wait_for_timeout(1300)
    r=J("()=>S.inbox.slice(0,3).map(m=>m.f+': '+m.t)")
    ck('text for a front at low trust: no + gray reason why',any('front' in x.lower() for x in r[1:2]+r[2:3]) and any('Trust 10/100' in x for x in r),json.dumps(r))
    ck('gray note styled in the thread',J("()=>!!document.querySelector('.bub.sys51')"))
    J("()=>document.querySelector('.mth-kb [data-p51=\"setup\"]').click()");pg.wait_for_timeout(1300)
    ck('set up a buy: plug agrees, setup saved',J("(bi)=>S.rb51&&S.rb51.bi===bi&&S.rb51.d===S.day+1",bi))
    J("(bi)=>{S.day+=1;S.at=bi}",bi)
    ck('next day at their spot: Rob button on plug card',J("(bi)=>plugActions(bi).includes('data-rb51')",bi))
    J("(bi)=>{S.rb51={bi,d:S.day-1};WD.forEach(f=>{try{if(/stood me up/.test(String(f)))f()}catch(e){}})}",bi)
    ck('miss the setup: trust drops, stood-up text',J("()=>!S.rb51&&/stood me up/.test(S.inbox[0].t)"))
    ck('Texts to answer section removed from trap phone',J("()=>w4Phone()===''"))
    ck('no errors',not errs,json.dumps(errs[:4]))
    b.close()
print(sum(res),'/',len(res))
