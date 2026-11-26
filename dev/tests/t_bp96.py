# business performance: stats, caps, costs, reinvest choices, save/load, multi-day, ledger
from playwright.sync_api import sync_playwright
SETUP="()=>{localStorage.setItem('tl-clean','0');startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=22;S.cal=0;S.school='out';S.cash=60000;S.clean=60000;S._evDay=S.day;S.picQ=[];S.dr92off=1;S.recapOff=1;S.biz={barber:1,wash:1};render();L95.reset();L95.flush()}"
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
  pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate;J(SETUP)
  ok=lambda n,c,x='':print(('PASS ' if c else 'FAIL ')+n,'' if c else x)
  J("()=>{tab='biz';render()}");pg.wait_for_timeout(200)
  ok('stats line on owned business',J("()=>/Demand \\d+ · Rep \\d+/i.test(document.getElementById('pane').textContent)"))
  ok('reinvest button',J("()=>!!document.querySelector('[data-a=bp96][data-k=barber]')"))
  J("()=>document.querySelector('[data-a=bp96][data-k=barber]').click()");pg.wait_for_timeout(200);pg.screenshot(path='/tmp/bp_menu.png')
  ok('menu shows expected results',J("()=>document.querySelectorAll('#mcard [data-o96]').length>=4&&/Profit about/.test(document.getElementById('mcard').innerText)"))
  J("()=>document.querySelector('[data-o96=mk]').click()");pg.wait_for_timeout(150)
  ok('confirm step',J("()=>!!document.getElementById('y96')"))
  c0=J("()=>S.cash");J("()=>document.getElementById('y96').click()")
  ok('marketing bought',J("()=>S.bp96.barber.mk===7")and J("()=>S.cash")<c0)
  J("()=>{document.querySelector('[data-o96=save]').click();document.getElementById('y96').click()}")
  ok('save up keeps money as reserve (transfer)',J("()=>S.bp96.barber.fund===1000"))
  L95=J("()=>{L95.flush();return L95.day(S.day)}");ok('reserve not counted as spending',L95['o']==J("()=>Math.round(BIZ.barber.pay*4)"),L95)
  J("()=>{document.getElementById('modal').hidden=true}")
  # caps: push 200 days of stats
  J("()=>{const o=S.bp96.barber;o.dem=100;o.rep=100;o.q=3;for(let i=0;i<200;i++)l96day('barber')}")
  ok('stats stay capped',J("()=>{const o=S.bp96.barber;return o.dem<=100&&o.rep<=100&&o.dem>=10&&o.rep>=0}"))
  r=J("()=>{const pot=l96pay('barber');S.bizUp={barber:0};const a=l96pay('barber');return [a, Math.round(BIZ.barber.pay*1.1*1.15*bizMul()*(S.college==='grad'?1.2:1))]}")
  ok('sales capped by capacity',r[0]<=r[1]+1,r)
  # daily overnight income with costs, ledger tagged business
  d=J("()=>S.day");J("()=>{nextDay();document.getElementById('modal').hidden=true;L95.flush()}")
  D=J(f"()=>L95.day({d+1})");ok('business sales + costs in ledger',D['k'].get('business',0)!=0,D)
  ok('business money is clean',J("()=>{const e=S.lg95.e.find(x=>x.k==='business'&&x.n>0);return e&&e.c===e.n}"))
  # save/load
  J("()=>{save();const sl=S.slot;S=load(sl);render()}")
  ok('save/load keeps business stats',J("()=>!!(S.bp96&&S.bp96.barber&&S.bp96.barber.q===3)"))
  # old save without bp96
  J("()=>{delete S.bp96;render();tab='biz';render()}")
  ok('old save upgrades quietly',J("()=>!!S.bp96&&S.bp96.barber.dem===55"))
  J("()=>{for(let i=0;i<25;i++){try{nextDay()}catch(e){window.__e=String(e)}document.getElementById('modal').hidden=true}}")
  ok('25 days no crash',not J("()=>window.__e||''"),J("()=>window.__e||''"))
  ok('no NaN',J("()=>Object.values(S.bp96).every(o=>isFinite(o.dem)&&isFinite(o.rep)&&isFinite(o.fund))&&isFinite(S.cash)"))
  J("()=>{tab='biz';render()}");pg.screenshot(path='/tmp/bp_tab.png')
  print('errors',errs[:4]);b.close()
