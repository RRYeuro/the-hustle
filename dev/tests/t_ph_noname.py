from playwright.sync_api import sync_playwright
SETUP="()=>{localStorage.setItem('tl-clean','0');startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S._evDay=S.day;S.picQ=[];S.dr92off=1;render()}"
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
  pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate;J(SETUP)
  J("()=>{S.inbox=(S.inbox||[]).concat([{f:undefined,t:'x',d:S.day},{t:'y',d:S.day}]);try{phoneMsg(undefined,'hi')}catch(e){}tab='phone';window._rph='msgs';render()}");pg.wait_for_timeout(400)
  print('tab error' if 'This tab hit an error' in J("()=>document.body.innerText") else 'phone OK', J("()=>document.querySelectorAll('.mth-row').length"), errs)
  b.close()
