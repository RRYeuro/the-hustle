from playwright.sync_api import sync_playwright
ok=0;n=0
def chk(c,m):
    global ok,n;n+=1;ok+=bool(c);print(('PASS ' if c else 'FAIL ')+m)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.goto('http://127.0.0.1:8765/index.html');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;S.lvl=8;S.cash=50000}")
    big=J("()=>PINFO.findIndex(p=>p.lvl==='Big')");low=J("()=>PINFO.findIndex(p=>p.lvl==='Low')")
    J(f"()=>{{S.age=17;S.known=[...new Set([...(S.known||[]),{big},{low}])];S.trust[{big}]=80}}")
    J("()=>{S._evDay=S.day;S.picQ=[];tab='move';render()}");chk("deal with kids" in J("()=>document.body.innerText"),'intro row says wait till 18')
    chk(J(f"()=>l66kidBlock({big})")==True and 'grown' in J("()=>document.getElementById('modal').innerText"),'big plug refuses 17yo')
    J("()=>document.getElementById('modal').hidden=true")
    chk(J(f"()=>window.l66kid({low})")==False,'low plug fine at 17')
    J("()=>{S.age=19}")
    chk(J(f"()=>window.l66kid({big})")==False,'big plug ok at 19')
    J("()=>{render()}");chk("deal with kids" not in J("()=>document.body.innerText"),'no kid line at 19')
    chk(not errs,'no errors '+';'.join(errs[:2]))
    print(ok,'/',n);b.close()
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.goto('http://127.0.0.1:8765/index.html');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;S.age=17;S.cash=50000}")
    g=J("()=>GOODS.findIndex(x=>x.unit==='g')")
    J(f"()=>{{l66rec(GOODS[{g}],50)}}")
    chk(J(f"()=>l66tb(GOODS[{g}])")==50,'teen buys add up for the day')
    J("()=>{S.day++}")
    chk(J(f"()=>l66tb(GOODS[{g}])")==0,'resets next day')
    J("()=>{S.age=19;S.tb66=null;l66rec(GOODS[0],99)}")
    chk(J("()=>l66tb(GOODS[0])")==0,'adults not tracked')
    chk(not errs,'no errors 2 '+';'.join(errs[:2]));print(ok,'/',n);b.close()
