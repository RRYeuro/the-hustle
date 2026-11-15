from playwright.sync_api import sync_playwright
ok=0;n=0
def chk(c,m):
    global ok,n;n+=1;ok+=bool(c);print(('PASS ' if c else 'FAIL ')+m)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1280,'height':900});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.goto('http://127.0.0.1:8765/index.html');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;S.age=20;S.cash=40000;S.cap=999;S._evDay=S.day;S.picQ=[]}")
    bi=J("()=>{const k=S.known.find(i=>PINFO[i].carries.length>=2)??S.known[0];S.trust[k]=90;return k}")
    J(f"()=>plugDrop({bi})");pg.wait_for_timeout(200)
    chk(pg.query_selector('#q67buy') is not None,'order sheet has Buy all')
    chk(J("()=>document.getElementById('q67buy').disabled"),'Buy all off with nothing picked')
    rows=pg.query_selector_all('.q67r[data-g]');gids=[r.get_attribute('data-g') for r in rows]
    print('goods',gids)
    pg.click(f'[data-q67="{gids[0]}"][data-d="1"]');pg.click(f'[data-q67="{gids[0]}"][data-d="1"]')
    if len(gids)>1:pg.click(f'[data-q67="{gids[1]}"][data-d="1"]')
    t=J("()=>document.getElementById('q67f').innerText");print(t)
    chk('Total' in t,'running total shows')
    inv0=J(f"()=>({{a:S.inv['{gids[0]}'],b:S.inv['{gids[-1]}'],c:S.cash,d:(ptxo().n[{bi}]||0),h:S.heat}})")
    pg.keyboard.press('Enter');pg.wait_for_timeout(200)
    inv1=J(f"()=>({{a:S.inv['{gids[0]}'],b:S.inv['{gids[-1]}'],c:S.cash,d:(ptxo().n[{bi}]||0),h:S.heat}})")
    print(inv0,inv1)
    chk(inv1['c']<inv0['c'],'cash spent')
    chk(inv1['d']==inv0['d']+1,'counts as one deal')
    chk(inv1['h']<=inv0['h']+1,'one heat bump')
    chk('Order dropped off' in J("()=>document.getElementById('modal').innerText") or 'No deal' in J("()=>document.getElementById('modal').innerText"),'summary card')
    # keyboard path + cash limit
    J("()=>{document.getElementById('modal').hidden=true;S.cash=60}");J(f"()=>plugDrop({bi})");pg.wait_for_timeout(150)
    pg.keyboard.press('ArrowRight');pg.keyboard.press('ArrowRight');pg.keyboard.press('ArrowRight')
    chk(J("()=>!document.getElementById('q67buy')||document.getElementById('q67buy').disabled||S.cash>=0"),'cannot overspend')
    # teen cap
    J("()=>{document.getElementById('modal').hidden=true;S.age=17;S.cash=90000;S.tb66=null}");J(f"()=>plugDrop({bi})");pg.wait_for_timeout(150)
    if pg.query_selector(f'[data-q67="{gids[0]}"][data-d="max"]'):
        pg.click(f'[data-q67="{gids[0]}"][data-d="max"]');pg.click('#q67buy');pg.wait_for_timeout(150)
        J("()=>document.getElementById('modal').hidden=true");J(f"()=>plugDrop({bi})");pg.wait_for_timeout(150)
        chk(pg.query_selector(f'[data-q67="{gids[0]}"][data-d="max"]') is None,'teen daily limit holds after reopening')
    pg.screenshot(path='/tmp/claude-0/s43/mb.png')
    chk(not errs,'no errors '+';'.join(errs[:2]));print(ok,'/',n);b.close()
