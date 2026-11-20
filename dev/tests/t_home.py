import subprocess,time,json
from playwright.sync_api import sync_playwright
srv=subprocess.Popen(['python3','-I','-m','http.server','8769','-d','/home/claude/the-hustle'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
with sync_playwright() as p:
    b=p.chromium.launch();ok=True
    for nm,vw,mob in [('d',(1280,900),False),('m',(390,800),True)]:
        c=b.new_context(viewport={'width':vw[0],'height':vw[1]},is_mobile=mob,has_touch=mob);pg=c.new_page();er=[];pg.on('pageerror',lambda e:er.append(str(e)[:200]))
        pg.goto('http://localhost:8769/index.html',wait_until='load');pg.wait_for_timeout(2500);J=pg.evaluate
        J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S.cash=2000;S.en=60;S.car=null;S.at=(homeBlock()+2)%6;tab='move';render()}");pg.wait_for_timeout(900)
        if mob:J("()=>{const t=document.querySelector('.tbs26 [data-t=\"'+homeBlock()+'\"]');t&&t.click()}");pg.wait_for_timeout(300)
        r=J("()=>{const h=document.querySelector('#pane .mapp[data-p=\"home\"]');return {pin:!!h,vis:!!(h&&h.offsetParent),txt:h?(h.textContent.trim()||h.dataset.n):''}}")
        d0=J("()=>S.day");J("()=>document.querySelector('#pane .mapp[data-p=\"home\"]').click()");pg.wait_for_timeout(500)
        r2=J("()=>({home:S.at===homeBlock(),dd:S.day-%d,modal:document.getElementById('modal').hidden?null:document.querySelector('#mcard h2').textContent})"%d0)
        J("()=>{document.getElementById('modal').hidden=true;tab='move';render()}");pg.wait_for_timeout(400)
        if mob:J("()=>{const t=document.querySelector('.tbs26 [data-t=\"'+homeBlock()+'\"]');t&&t.click()}");pg.wait_for_timeout(300)
        J("()=>document.querySelector('#pane .mapp[data-p=\"home\"]').click()");pg.wait_for_timeout(400)
        r3=J("()=>({h:document.querySelector('#mcard h2').textContent,btns:['h34a','h34b','h34c'].every(i=>!!document.getElementById(i))})")
        pg.screenshot(path=f'/tmp/claude-0/home_{nm}.png')
        d1=J("()=>S.day");J("()=>document.getElementById('h34a').click()");pg.wait_for_timeout(400);r4=J("()=>S.day-%d"%d1)
        good=r['pin'] and r['vis'] and r2['home'] and r2['dd']==1 and 'Home' in r3['h'] and r3['btns'] and r4==1 and not er
        ok=ok and good;print(nm,'PASS' if good else 'FAIL',json.dumps([r,r2,r3,r4]),er[:3]);c.close()
    b.close()
srv.terminate()
