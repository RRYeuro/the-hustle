from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.goto('http://127.0.0.1:8765/index.html');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;S.age=20;S._evDay=S.day;S.picQ=[];S.car=Object.keys(CARS).find(k=>k!=='stolen');w4().chop=1;window.hotwireGame=f=>f(true);window.l27Car=null;lick('car')}")
    pg.wait_for_timeout(150);print(J("()=>[...document.querySelectorAll('#mcard button')].map(b=>b.textContent)"))
    car=J("()=>S.car");J("()=>document.getElementById('kc').click()");print('kept car',J("()=>S.car")==car,'lot',J("()=>w4().lot"))
    J("()=>{document.getElementById('modal').hidden=true;window.stripGame=f=>f(4);w4Act('w4_strip',{dataset:{}})}")
    print('after strip lot',J("()=>w4().lot"),'car still',J("()=>S.car")==car)
    J("()=>{S.rapOn=1;S.rap=S.rap||{};S.rap.fans=5000;S.rap.fat=4;tab='more';render()}")
    print(errs);b.close()
