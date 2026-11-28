# th224: notebook, fridge, ledger, cell wall
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c):R.append(c);print(('PASS ' if c else 'FAIL ')+n)
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page(viewport={'width':393,'height':852})
  errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
  pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate
  J("()=>{startLife('shade');document.getElementById('modal').hidden=true;S.tut73='skip';S.fd={off:1};render()}")
  for t,th in [('sch','nb'),('exp','fr'),('biz','lg')]:
    J(f"()=>{{tab='{t}';render()}}")
    ok(t+' themed',J("()=>(document.querySelector('#pane>.th224')||{}).dataset?.th")==th)
    ok(t+' top bar not themed',J("()=>!document.querySelector('.th224 [data-a=adv], .th224 #nextday')"))
  J("()=>{tab='block';render()}")
  ok('block not themed',J("()=>!document.querySelector('#pane>.th224')"))
  J("()=>{tab='biz';render();render()}")
  ok('no double wrap',J("()=>document.querySelectorAll('#pane .th224').length")==1)
  ok('biz buttons still work',J("()=>document.querySelectorAll('.th224 .mv-tile').length")>=3)
  J("()=>{S.rk222f=3;render()}")
  ok('kingpin ledger',J("()=>document.querySelector('.th224').classList.contains('t3')"))
  J("()=>{S.rk222f=0;S.age=22;prStart();S.day+=7;tab='prison';render()}")
  ok('cell wall',J("()=>(document.querySelector('#pane>.th224')||{}).dataset?.th")=='cw')
  ok('tally marks',J("()=>/卌/.test(document.querySelector('.tally224').textContent)&&/7 days down/.test(document.querySelector('.tally224').textContent)"))
  ok('no errors',not errs);print(errs)
  b.close()
