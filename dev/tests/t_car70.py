from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.goto('http://127.0.0.1:8765/index.html');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;S.age=20;S._evDay=S.day;S.picQ=[];S.car=Object.keys(CARS).find(k=>k!=='stolen');window.hotwireGame=f=>f(true);window.l27Car=null;lick('car')}")
    pg.wait_for_timeout(200);print(J("()=>[...document.querySelectorAll('#mcard button')].map(b=>b.textContent)"))
    c0=J("()=>S.cap");J("()=>document.getElementById('kw').click()");print(J("()=>S.car"),J("()=>S.cap")-c0,errs)
    b.close()
