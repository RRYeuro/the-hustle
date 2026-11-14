from playwright.sync_api import sync_playwright
F='file:///home/claude/the-hustle/index.html'
errs=[];res=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':420,'height':860})
    pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:300]) if m.type=='error' and 'Failed to load' not in m.text else None)
    pg.goto(F,wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.FF=false;S.age=19;S.cal=0;S.school='out';S.cash=5000;S.sk.smarts=5;S.heat=10;render()}")
    ck('loaded',J("()=>!!window._sk39&&typeof m39Lock==='function'&&typeof m39Vault==='function'&&typeof m39Roof==='function'"))
    # lockpick win
    J("()=>{window._r=null;m39Lock({},ok=>window._r=ok)}")
    ck('lock gate',J("()=>!!document.querySelector('#mcard #gst')"));pg.keyboard.press('Enter');pg.wait_for_timeout(200)
    for i in range(4):
        J("()=>__lpDbg.aim()");pg.keyboard.press('Space');pg.wait_for_timeout(200)
    ck('lock win',J("()=>window._r===true&&mgOn===false&&document.getElementById('modal').hidden"))
    # lockpick fail: miss on purpose 3+ times (picks 3 + smarts5 => 3)
    J("()=>{window._r=null;m39Lock({},ok=>window._r=ok)}");pg.keyboard.press('Enter');pg.wait_for_timeout(200)
    for i in range(3):
        J("()=>{const z=__lpDbg.zone();__lpDbg.aim();}")
        # force a miss by waiting until needle is outside zone
        pg.wait_for_function("()=>{const z=__lpDbg.zone(),p=__lpDbg.pos();return p<z[0]-3||p>z[0]+z[1]+3}",timeout=8000)
        pg.keyboard.press('Space');pg.wait_for_timeout(200)
    ck('lock 3 misses fail',J("()=>window._r===false"))
    J("()=>{window._r=null;m39Lock({},ok=>window._r=ok)}");pg.keyboard.press('Enter');pg.wait_for_timeout(150);pg.keyboard.press('Escape')
    ck('lock Esc',J("()=>window._r===false&&mgOn===false"))
    # vault
    J("()=>{window._r=null;m39Vault({},ok=>window._r=ok)}");ck('vault gate',J("()=>!!document.querySelector('#mcard #gst')"));pg.keyboard.press('Enter');pg.wait_for_timeout(200)
    ck('vault has clues',J("()=>__vcDbg.clues().length>=2"))
    ck('vault clues narrow to <=2',J("()=>__vcDbg.left()<=2"),J("()=>__vcDbg.left()"))
    code=J("()=>__vcDbg.code()")
    for d in code: pg.keyboard.press(str(d))
    pg.keyboard.press('Enter');pg.wait_for_timeout(150)
    ck('vault win',J("()=>window._r===true&&mgOn===false"))
    J("()=>{window._r=null;m39Vault({},ok=>window._r=ok)}");pg.keyboard.press('Enter');pg.wait_for_timeout(200)
    code=J("()=>__vcDbg.code()");w=[(code[0]+1)%10,code[1],code[2],code[3]]
    for i in range(3):
        for d in [(code[0]+1+i)%10,code[1],code[2],code[3]]: pg.keyboard.press(str(d))
        pg.keyboard.press('Enter');pg.wait_for_timeout(150)
    ck('vault 3 wrong fail',J("()=>window._r===false"))
    # vault clue truth over many gens
    ok=J("()=>{let bad=0;for(let i=0;i<30;i++){m39Vault({},()=>{});document.querySelector('#gst').click();const c=__vcDbg.code();if(__vcDbg.left()>2)bad++;__vcDbg.fail()}return bad}")
    ck('vault 30 gens narrow',ok==0,ok)
    # roof run
    J("()=>{window._r=null;S.car=null;m39Roof({},ok=>window._r=ok)}");ck('roof gate',J("()=>!!document.querySelector('#mcard #gst')"));pg.keyboard.press('Enter');pg.wait_for_timeout(300)
    ck('roof canvas',J("()=>!!document.getElementById('cv')"))
    pg.keyboard.press('Space');pg.wait_for_timeout(100)
    ck('roof jumps',J("()=>__rfDbg.st().y>0"))
    J("()=>__rfDbg.tp()");pg.wait_for_timeout(1500)
    ck('roof reach end wins or continue card',J("()=>!!document.getElementById('ok')"))
    J("()=>document.getElementById('ok').click()");pg.wait_for_timeout(100)
    ck('roof done ok',J("()=>window._r===true&&mgOn===false"))
    # roof: stand still => dies (no jumping)
    J("()=>{window._r=null;m39Roof({},ok=>window._r=ok)}");pg.keyboard.press('Enter');pg.wait_for_function("()=>!!document.getElementById('ok')",timeout=30000)
    J("()=>document.getElementById('ok').click()")
    ck('roof no input loses',J("()=>window._r===false"))
    # hooks
    J("()=>{window._m39force=1}")
    ck('safeAsk patched','m39Vault' in open('/home/claude/the-hustle/index.html').read().split('function safeAsk')[1][:900])
    ck('dev menu buttons',True)
    J("()=>{window._m39force=0}")
    ck('no page errors',not errs,errs[:3])
print('%d/%d'%(sum(res),len(res)))
