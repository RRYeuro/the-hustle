import sys,json
from playwright.sync_api import sync_playwright
F='file:///home/claude/the-hustle/index.html'
errs=[];res=[]
def ck(n,c,x=''):
    res.append((n,bool(c)));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':420,'height':860})
    pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:300]) if m.type=='error' and 'l27' in m.text else None)
    pg.goto(F,wait_until='load');pg.wait_for_timeout(1500)
    J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL27=1;window.FF=false;S.age=19;S.cal=0;S.school='out';S.cash=5000;S.clean=1000;S.sk.smarts=5;S.sk.talk=5;S.heat=10;render()}")
    ck('skin27 loaded',J("()=>!!window._sk27&&typeof l27Sort==='function'"))
    # --- Sort: tutorial card, keyboard, win
    J("()=>{window._r=null;l27Sort({title:'T'},ok=>window._r=ok)}")
    ck('sort tutorial card has Start',J("()=>!!document.querySelector('#mcard #gst')"))
    pg.keyboard.press('Enter');pg.wait_for_timeout(200)
    ck('sort grid 16',J("()=>document.querySelectorAll('#srg button').length")==16)
    # keyboard: move cursor to tile holding 1 and press Enter
    ordv=J("()=>__srDbg.ord()");i=ordv.index(1)
    for _ in range(i//4): pg.keyboard.press('ArrowDown')
    for _ in range(i%4): pg.keyboard.press('ArrowRight')
    pg.keyboard.press('Enter')
    ck('sort arrows+Enter picks',J("()=>__srDbg.next()")==2)
    pg.locator('#srg button').nth(ordv.index(2)).click()
    ck('sort click picks',J("()=>__srDbg.next()")==3)
    J("()=>__srDbg.solve()")
    ck('sort win',J("()=>window._r===true&&mgOn===false&&document.getElementById('modal').hidden"))
    J("()=>{window._r=null;l27Sort({title:'T'},ok=>window._r=ok)}");pg.keyboard.press('Enter');pg.wait_for_timeout(150);pg.keyboard.press('Escape')
    ck('sort Esc gives up',J("()=>window._r===false&&mgOn===false"))
    J("()=>{window._r=null;S.sk.smarts=0;l27Sort({title:'T',sec:8},ok=>window._r=ok)}");pg.keyboard.press('Enter');pg.wait_for_timeout(8600)
    ck('sort timer fails',J("()=>window._r===false"));J("()=>{S.sk.smarts=5}")
    # --- Pin
    J("()=>{window._r=null;l27Pin({title:'P'},ok=>window._r=ok)}")
    ck('pin tutorial card',J("()=>!!document.querySelector('#mcard #gst')"));pg.keyboard.press('Enter');pg.wait_for_timeout(200)
    code=J("()=>__pcDbg.code()")
    wrong=[code[1],code[0]]+[d for d in range(10) if d not in code][:2]
    for d in wrong: pg.keyboard.press(str(d))
    pg.keyboard.press('Enter')
    cls=J("()=>__pcDbg.tries()")
    hist=J("()=>[...document.querySelectorAll('#pch div:last-child i')].map(x=>x.className)")
    ck('pin feedback yellow',cls==1 and hist==['y','y','',''],str(hist))
    for d in code: pg.keyboard.press(str(d))
    pg.keyboard.press('ArrowLeft');pg.keyboard.press('ArrowRight')
    pg.keyboard.press('Enter')
    ck('pin typed code wins',J("()=>window._r===true&&mgOn===false"))
    J("()=>{window._r=null;l27Pin({title:'P'},ok=>window._r=ok)}");pg.keyboard.press('Enter');pg.wait_for_timeout(150)
    code=J("()=>__pcDbg.code()");bad=[d for d in range(10) if d not in code][:4];mx=J("()=>__pcDbg.max")
    for t in range(mx):
        for d in bad: pg.locator(f'[data-pk="{d}"]').click();pg.wait_for_timeout(130)
        pg.locator('[data-pk="c"]').click();pg.wait_for_timeout(130)
    ck('pin out of tries fails',J("()=>window._r===false"))
    # --- loot capacity
    r=J("()=>{S.loot=[];S.bag=0;S.car=null;const L=[];l27House(L,'plug',false);const n=L.map(x=>x.t+(x.f()||''));return {n,loot:S.loot.map(x=>x.k+':'+x.w)}}")
    ck('no bag: pocket loot only',all(x.endswith(':p') for x in r['loot']) and len(r['loot'])>=2,json.dumps(r))
    r=J("()=>{S.loot=[];S.bag=1;const L=[];for(let i=0;i<6;i++)l27House(L,'reg',true);L.forEach(x=>x.f());return {p:S.loot.filter(x=>x.w==='p').length,b:S.loot.filter(x=>x.w==='b').length,c:S.loot.filter(x=>x.w==='c').length}}")
    ck('caps pockets 4 bag 8 no trunk',r['p']<=4 and r['b']<=8 and r['c']==0,json.dumps(r))
    # --- pawn sell: dirty cash, 40-60%
    r=J("()=>{S.loot=[{k:'chain',v:1000,p:50,d:S.day-9,w:'p'},{k:'tv',v:1000,p:50,d:S.day,w:'c'},{k:'phone',v:300,p:50,d:S.day-9,w:'p'}];S.car=S.car||'stolen';const pb=PLACES.find(p=>p.id==='pawn');S.at=placeAt('pawn');S.cash=5000;S.clean=1000;S.heat=10;openPlace('pawn');return [...document.querySelectorAll('#mcard [data-l27]')].map(b=>b.dataset.l27+'='+b.textContent)}")
    ck('pawn rows show',r==['pj=$500','pe=$590'],str(r))
    pg.locator('#mcard [data-l27="pj"]').click();pg.wait_for_timeout(200)
    r=J("()=>({cash:S.cash,clean:cleanCash(),n:S.loot.length,heat:S.heat,open:!document.getElementById('modal').hidden})")
    ck('jewelry sold dirty',r['cash']==5500 and r['clean']==1000 and r['n']==2 and r['heat']==10 and r['open'],json.dumps(r))
    pg.locator('#mcard [data-l27="pe"]').click();pg.wait_for_timeout(200)
    r=J("()=>({cash:S.cash,clean:cleanCash(),n:S.loot.length,heat:S.heat})")
    ck('electronics sold, hot adds heat',r['cash']==6090 and r['clean']==1000 and r['n']==0 and r['heat']==12,json.dumps(r))
    J("()=>{document.getElementById('modal').hidden=true}")
    # --- licks pane + stash home + plug
    r=J("()=>{S.loot=[{k:'laptop',v:500,p:50,d:S.day-9,w:'b'},{k:'ring',v:200,p:50,d:S.day-9,w:'p'}];S.at=homeBlock();const h=paneLicks();return {sec:h.includes('Stolen goods'),stash:h.includes('data-l27=\"stash\"')}}")
    ck('licks pane lists loot + home stash',r['sec'] and r['stash'],json.dumps(r))
    # --- cop search popup
    J("()=>{S.heat=0;S.sk.talk=10;l27Search()}")
    ck('search popup',J("()=>/Stopped and searched/.test(document.querySelector('#mcard h2').textContent)"))
    J("()=>{Math._r=Math.random;Math.random=()=>.99;document.getElementById('l27a').click();Math.random=Math._r}")
    ck('search fail small: loot seized, no bust',J("()=>S.loot.length===0&&S.heat===12&&/They found it/.test(document.querySelector('#mcard h2').textContent)"))
    J("()=>{document.getElementById('ok').click()}")
    J("()=>{S.loot=[{k:'chain',v:3000,p:50,d:S.day-9,w:'p'}];l27Search();Math._r=Math.random;Math.random=()=>0;document.getElementById('l27a').click();Math.random=Math._r}")
    ck('search pass keeps loot',J("()=>S.loot.length===1&&document.getElementById('modal').hidden"))
    # --- dev menu
    J("()=>{devPanel()}")
    ck('dev menu group',J("()=>document.querySelectorAll('#mcard [data-d27]').length")==8)
    pg.locator('[data-d27="loot"]').click();pg.wait_for_timeout(200)
    ck('dev loot gives items',J("()=>S.loot.length>5&&!!S.bag"))
    J("()=>{document.getElementById('modal').hidden=true}")
    ck('tutorial entries',J("()=>TUT.filter(t=>/Licks and loot|Sort and Pin/.test(t[0])).length")==2)
    # --- full flows (core mini games stubbed to a win)
    J("()=>{window._l27force=true;window._m39no=1;seqGame=d=>d(true);grabGame=(d,o)=>d((o&&o.max)||6,false);sneakGame=d=>d(6,false);hotwireGame=d=>d(true);talkGame=d=>d(0);chase=d=>d(true);cut=()=>{};window.noTips=1}")
    R="()=>{window.m39Vault=null;window._m39force=0;window._m39roof=0;S._evDay=S.day;S.loot=[];S.bag=1;S.car=null;S.rob=S.rob||{};S.rob.fat=0;S.lcd={};S.cap=900;S.heat=0;S.cash=1000;S.clean=1000;S.hp=100;S.en=100;S.stress=0;S.over=false;document.getElementById('modal').hidden=true;"
    txt=lambda:J("()=>document.getElementById('modal').hidden?'(hidden)':document.getElementById('mcard').innerText.slice(0,260)")
    def sort_win():
        pg.keyboard.press('Enter');pg.wait_for_timeout(200);J("()=>__srDbg.solve()");pg.wait_for_timeout(300)
    def maybe_lock():
        if J("()=>/Pick the back door lock/.test(document.getElementById('mcard').textContent)"):
            pg.keyboard.press('Enter');pg.wait_for_timeout(200)
            for _ in range(12):
                if not J("()=>!!window.__lpDbg&&!document.getElementById('modal').hidden&&/pins|Pin/.test(document.getElementById('mcard').textContent)"):break
                J("()=>{__lpDbg.aim();__lpDbg.press()}");pg.wait_for_timeout(450)
            pg.wait_for_timeout(300)
    def pin(win=True):
        pg.keyboard.press('Enter');pg.wait_for_timeout(200);J("()=>__pcDbg.%s()"%('solve' if win else 'fail'));pg.wait_for_timeout(300)
    # store: kill alarm, register, crack safe
    J(R+"S.at=1;lick('store')}");pg.wait_for_timeout(200)
    ck('store asks about alarm',J("()=>!!document.getElementById('l27a')"),txt())
    J("()=>document.getElementById('l27a').click()");sort_win()
    ck('store: safe offered after register',J("()=>!!document.getElementById('l27c')&&window._l27q===1&&S.cash>1000"),txt())
    c0=J("()=>S.cash");J("()=>document.getElementById('l27c').click()");pin(True)
    r=J("()=>({cash:S.cash,clean:cleanCash(),t:document.getElementById('mcard').innerText})")
    ck('store: safe pays dirty, result popup',r['cash']>=c0+1500 and r['clean']==1000 and 'back-room safe gave up' in r['t'] ,json.dumps(r)[:300])
    d0=J("()=>S.day");J("()=>document.getElementById('ok').click()");pg.wait_for_timeout(300)
    ck('store: day advanced',J("()=>S.day")==d0+1,txt());J("()=>{document.getElementById('modal').hidden=true}")
    # store: run in, safe fail -> alarm run
    J(R+"S.at=1;lick('store')}");pg.wait_for_timeout(200);J("()=>document.getElementById('l27b').click()");pg.wait_for_timeout(300)
    J("()=>document.getElementById('l27c').click()");pin(False)
    ck('store: safe fail trips alarm',J("()=>/Alarm tripped/.test(document.querySelector('#mcard h2').textContent)&&S.heat>=25"),txt())
    J("()=>document.getElementById('r').click()");pg.wait_for_timeout(300)
    ck('store: got away popup',J("()=>/got away/i.test(document.querySelector('#mcard h2').textContent)"),txt());J("()=>{document.getElementById('modal').hidden=true}")
    # house: alarm panel -> sneak -> grab -> safe
    J(R+"S.at=3;lick('house')}");pg.wait_for_timeout(300)
    if J("()=>!!document.getElementById('sn')"): J("()=>document.getElementById('sn').click()");pg.wait_for_timeout(200)
    maybe_lock()
    ck('house: alarm panel sort card',J("()=>/alarm panel/i.test(document.getElementById('mcard').innerText)&&!!document.getElementById('gst')"),txt())
    sort_win()
    ck('house: loot list shows',J("()=>!!document.getElementById('gg0')"),txt())
    J("()=>document.getElementById('gg0').click()");pg.wait_for_timeout(400)
    r=J("()=>({safe:!!document.getElementById('l27c'),loot:S.loot.length,t:document.getElementById('mcard').innerText.slice(0,200)})")
    ck('house: real loot taken, safe offered',r['safe'],json.dumps(r))
    c0=J("()=>S.cash");J("()=>document.getElementById('l27c').click()");pin(True)
    r=J("()=>({cash:S.cash,clean:cleanCash(),loot:S.loot.map(x=>x.k+':'+x.w),t:document.getElementById('mcard').innerText})")
    ck('house: safe cash dirty + clean lick popup',r['cash']>c0 and r['clean']==1000 and 'The safe had' in r['t'],json.dumps(r)[:400])
    ck('house: no trunk loot without a car',all(not x.endswith(':c') for x in r['loot']),str(r['loot']))
    J("()=>document.getElementById('ok').click()");pg.wait_for_timeout(300);J("()=>{document.getElementById('modal').hidden=true}")
    # house: alarm panel fail
    J(R+"S.at=3;lick('house')}");pg.wait_for_timeout(300)
    if J("()=>!!document.getElementById('sn')"): J("()=>document.getElementById('sn').click()");pg.wait_for_timeout(200)
    maybe_lock()
    pg.keyboard.press('Enter');pg.wait_for_timeout(200);pg.keyboard.press('Escape');pg.wait_for_timeout(300)
    ck('house: failed panel = alarm tripped',J("()=>/Alarm tripped/.test(document.querySelector('#mcard h2').textContent)"),txt());J("()=>{document.getElementById('modal').hidden=true}")
    # pharmacy cabinet
    J(R+"S.at=4;Math._r=Math.random;Math.random=()=>.5;lick('pharm');Math.random=Math._r}");pg.wait_for_timeout(500)
    ck('pharm: cabinet offered',J("()=>!!document.getElementById('l27c')"),txt())
    p0=J("()=>S.inv.percs");J("()=>document.getElementById('l27c').click()");pin(True)
    ck('pharm: cabinet adds pills',J("()=>S.inv.percs")>p0 and 'locked cabinet had' in txt(),txt());J("()=>{document.getElementById('modal').hidden=true}")
    # scam phone
    J(R+"Math._r=Math.random;Math.random=()=>.5;lick('scam');Math.random=Math._r}");pg.wait_for_timeout(300)
    ck('scam: phone offered',J("()=>!!document.getElementById('l27a')"),txt())
    c0=J("()=>S.cash");J("()=>document.getElementById('l27a').click()");sort_win()
    ck('scam: phone pays dirty',J("()=>S.cash")>c0 and J("()=>cleanCash()")==1000 and 'into his phone' in txt(),txt());J("()=>{document.getElementById('modal').hidden=true}")
    # car: sort bypass
    J(R+"S.pad=1;S.age=19;lick('car')}");pg.wait_for_timeout(300)
    ck('car: bypass ignition card',J("()=>/Bypass the ignition/.test(document.getElementById('mcard').textContent)"),txt())
    sort_win();ck('car: got the whip',J("()=>/Got the whip/.test(document.getElementById('mcard').textContent)"),txt());J("()=>{document.getElementById('modal').hidden=true}")
    # busted clears loot; day hook search fires; save/load keeps loot
    J("()=>{window._l27force=false;S.loot=[{k:'ring',v:200,p:50,d:1,w:'p'}];S.lootH=[{k:'tv',v:500,p:50,d:1,w:'c'}];save();const s=load();window._sv=[s.loot.length,s.lootH.length]}")
    ck('save/load keeps loot',J("()=>window._sv")==[1,1])
    J("()=>{window.noL27=0;S.l27s=-99;S.heat=90;Math._r=Math.random;Math.random=()=>0;try{WD.find(f=>f.name==='l27Day')()}finally{Math.random=Math._r}}");pg.wait_for_timeout(700)
    ck('day hook: search pops',J("()=>!document.getElementById('modal').hidden&&/Stopped and searched/.test(document.querySelector('#mcard h2').textContent)"),txt())
    J("()=>{window.noL27=1;document.getElementById('modal').hidden=true;S.loot=[{k:'ring',v:200,p:50,d:1,w:'p'}];try{busted()}catch(e){window._be=String(e)}}")
    ck('busted takes loot',J("()=>S.loot.length===0&&!window._be"),J("()=>window._be"))
    # phone width: no overflow in pin modal
    J("()=>{document.getElementById('modal').hidden=true;S.over=false;mgOn=false;l27Pin({title:'P'},()=>{})}");pg.keyboard.press('Enter');pg.wait_for_timeout(200)
    ck('pin fits phone width',J("()=>{const m=document.getElementById('mcard');return m.scrollWidth<=m.clientWidth+1}"))
    pg.screenshot(path='/tmp/claude-0/pin.png');pg.keyboard.press('Escape')
    J("()=>{l27Sort({title:'Kill the alarm panel'},()=>{})}");pg.keyboard.press('Enter');pg.wait_for_timeout(200);pg.screenshot(path='/tmp/claude-0/sort.png');pg.keyboard.press('Escape')
    b.close()
bad=[n for n,c in res if not c]
print('\nERRORS:',errs[:8]);print(f'{len(res)-len(bad)}/{len(res)} passed');sys.exit(1 if bad or errs else 0)
