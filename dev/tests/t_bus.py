# bus pass: buying the pass also takes the ride
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c):R.append(c);print(('PASS ' if c else 'FAIL ')+n)
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
  pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate
  J("()=>{startLife('shade');document.getElementById('modal').hidden=true;S.at=0;S.bus=0;S.cash=400;window._go58=1;act('goB',{dataset:{i:'4'}});window._go58=0}")
  ok('bought pass and moved',J("()=>S.at===4&&S.bus>S.day&&S.cash===370"))
  J("()=>{window._go58=1;act('goB',{dataset:{i:'1'}});window._go58=0}")
  ok('second ride uses pass',J("()=>S.at===1&&S.cash===370"))
  J("()=>{S.at=0;S.bus=0;S.cash=10;window._go58=1;act('goB',{dataset:{i:'4'}});window._go58=0}")
  ok('broke stays put',J("()=>S.at===0"))
  ok('no errors',not errs)
  b.close()
