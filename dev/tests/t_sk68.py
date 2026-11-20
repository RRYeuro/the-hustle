from playwright.sync_api import sync_playwright
ok=0;n=0
def chk(c,m):
    global ok,n;n+=1;ok+=bool(c);print(('PASS ' if c else 'FAIL ')+m)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1280,'height':900});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and errs.append(m.text));pg.goto('http://127.0.0.1:8765/index.html');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;S.age=20;S.cash=90000;S._evDay=S.day;S.picQ=[];S.lvl=8;S.soldiers=2;S.inv.loud=100;S.inv.bars=60}")
    J("()=>{devPanel();document.getElementById('dv68').click()}");pg.wait_for_timeout(200)
    chk('Run the operation' in J("()=>document.getElementById('mcard').innerText"),'dev button opens operation')
    tot0=J("()=>({inv:S.inv.loud+S.inv.bars+S.workers.reduce((a,w)=>a+(w.stash.loud||0)+(w.stash.bars||0),0),cash:S.cash,held:S.workers.reduce((a,w)=>a+(w.held||0),0)})")
    pg.click('#r68');pg.wait_for_timeout(100)
    tot1=J("()=>({inv:S.inv.loud+S.inv.bars+S.workers.reduce((a,w)=>a+(w.stash.loud||0)+(w.stash.bars||0),0),ws:S.workers.map(w=>wStashUsed(w)),mine:S.inv.loud})")
    print(tot0,tot1)
    chk(abs(tot1['inv']-tot0['inv'])<0.01,'restock: no product lost or duplicated')
    chk(all(x>0 for x in tot1['ws']),'every worker got product')
    pg.click('#c68');pg.wait_for_timeout(100)
    chk(J("()=>S.cash")==tot0['cash']+tot0['held'],'collect all adds held cash')
    # keep stocked
    J("()=>{S.op68.on=true;S.op68.t={loud:10};S.workers.forEach(w=>w.stash={});S.inv.loud=100}")
    J("()=>{document.getElementById('modal').hidden=true;nextDay();document.getElementById('modal').hidden=true}")
    chk(J("()=>S.inbox.some(m=>m.f==='The Gang')"),'group chat has posts')
    chk(J("()=>S.workers.every(w=>(w.stash.loud||0)>0)") or J("()=>S.workers.some(w=>(w.held||0)>0)"),'auto refill ran in the morning')
    # worker card
    J("()=>{l68card(0)}");pg.wait_for_timeout(100)
    chk(J("()=>!!document.getElementById('k68s')"),'worker card shows Stash')
    # circle tab crew cleanup
    J("()=>{document.getElementById('modal').hidden=true;tab='beef';render()}");pg.wait_for_timeout(200)
    chk(J("()=>document.querySelectorAll('#pane .row.cm68').length")>=2,'crew cards collapsed')
    chk(J("()=>!!document.querySelector('[data-wk68]')"),'workers row on Circle tab')
    J("()=>{document.getElementById('modal').hidden=true;document.querySelector('#pane .row.cm68 .info').click()}");pg.wait_for_timeout(150)
    chk(J("()=>document.querySelectorAll('#mcard .cmc68 button').length")>5,'tap crew name opens actions')
    J("()=>document.querySelector('#mcard [data-a=cmtalk]').click()");pg.wait_for_timeout(200)
    chk(not errs,'no errors after crew action')
    # group chat thread
    J("()=>{document.getElementById('modal').hidden=true;tab='phone';window._rph='messages';window._mth='The Gang';render()}");pg.wait_for_timeout(200)
    chk(J("()=>document.querySelectorAll('[data-gc68]').length")>=4,'group chat reply options')
    J("()=>{S.workers.forEach(w=>w.held=100)}");c0=J("()=>S.cash")
    J("()=>render()");pg.wait_for_timeout(100);J("()=>{document.getElementById('modal').hidden=true;document.querySelector('[data-gc68=money]').click()}");pg.wait_for_timeout(200)
    chk(J("()=>S.cash")==c0+300,'Bring the money collects')
    pg.screenshot(path='/tmp/claude-0/s43/gc.png');J("()=>{tab='beef';window._rph=null;document.getElementById('modal').hidden=true;render()}");pg.screenshot(path='/tmp/claude-0/s43/cm.png',full_page=True);J("()=>l68op()");pg.screenshot(path='/tmp/claude-0/s43/op.png')
    chk(not errs,'no errors '+';'.join(errs[:3]));print(ok,'/',n);b.close()
