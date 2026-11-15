import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1280,'height':900});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:200]) if m.type=='error' and 'sk' in m.text else None)
    pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S.lvl=10;S.cash=50000;S.clean=50000;S._evDay=S.day;S.picQ=[];S.fd=null;S.owner[2]='me';S.at=BLOCKS.map((b,i)=>i).find(i=>!myBlock(i));tab='block';render()}")
    ck('Block tab: trap row points to your block',J("()=>/Your trap houses/.test(document.getElementById('pane').innerText)"))
    J("()=>document.querySelector('[data-a61]').click()");pg.wait_for_timeout(200)
    ck('away: go to your block first',J("()=>!!document.querySelector('[data-g61]')"))
    J("()=>{document.getElementById('modal').hidden=true;S.at=2;l61open()}")
    ck('on your block: trap page opens',J("()=>!!document.querySelector('#mcard .tr61')&&/open/i.test(document.querySelector('#mcard .tr61').innerText)"))
    J("()=>document.querySelector('#mcard .tr61 [data-a=\"trap\"][data-i=\"2\"]').click()");pg.wait_for_timeout(400)
    ck('open a trap: page refreshes with the trap',J("()=>!!S.traps[2]&&!!document.querySelector('#mcard .tr61')&&/Bottom trap|trap/.test(document.querySelector('#mcard .tr61').innerText)"),J("()=>document.getElementById('modal').hidden?'hidden':document.querySelector('#mcard').innerText.slice(0,150)"))
    J("()=>{const b=document.querySelector('#mcard .tr61 [data-a=\"hirew\"]');if(b)b.click()}");pg.wait_for_timeout(400)
    ck('hire a worker from the trap page',J("()=>S.workers.length>=1"))
    J("()=>{document.getElementById('modal').hidden=true;tab='move';render()}");pg.wait_for_timeout(200)
    ck('🧺 pin on the Move map',J("()=>!!document.querySelector('#fm26 .tp61')"))
    J("()=>{tab='phone';window._rph=null;render()}");pg.wait_for_timeout(200)
    ck('Trap house app gone from the phone',J("()=>!document.querySelector('.ph-home [data-rph=\"trap\"]')"))
    J("()=>{const w=S.workers[0];w.held=900;S.traps[2].w=w.id;S.w61={};WD.forEach(f=>{try{if(/w61/.test(String(f)))f()}catch(e){}})}")
    ck('worker texts what they are holding',J("()=>S.inbox[0]&&S.inbox[0].f===S.workers[0].name&&/\\$900/.test(S.inbox[0].t)"))
    J("()=>{window._rph='messages';window._mth=S.workers[0].name;render()}");pg.wait_for_timeout(300)
    ck('text them: bring me the money',J("()=>!!document.querySelector('.mth-kb [data-a=\"wcollect\"]')"))
    c0=J("()=>S.cash");J("()=>document.querySelector('.mth-kb [data-a=\"wcollect\"]').click()");pg.wait_for_timeout(300)
    ck('money comes to you',J("(c)=>S.cash>c&&!S.workers[0].held",c0))
    ck('no errors',not errs,json.dumps(errs[:3]))
    b.close()
print(sum(res),'/',len(res))
