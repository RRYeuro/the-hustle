# rk222: rank skins, crime board, heist board
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c):R.append(c);print(('PASS ' if c else 'FAIL ')+n)
with sync_playwright() as p:
  b=p.chromium.launch();c=b.new_context(viewport={'width':393,'height':852},has_touch=True,is_mobile=True);pg=c.new_page()
  errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
  pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate
  J("()=>{startLife('shade');document.getElementById('modal').hidden=true;S.age=20;S.soldiers=2;S.crewM=[mkMember('Mateo',{loy:70,trust:60}),mkMember('Kesha',{loy:55,trust:40})];S.crews[0].beef=20;S.tut73='skip';S.fd={off:1};document.getElementById('tu73')&&document.getElementById('tu73').remove();tab='beef';render()}");pg.wait_for_timeout(300)
  for i in range(4):
    J("()=>{const b=document.querySelector('#tu73b button');b&&b.click()}");pg.wait_for_timeout(200)
  ok('board shows you, crew and rival',J("()=>document.querySelectorAll('.cbd .pol').length")==4)
  ok('strings drawn',J("()=>document.querySelectorAll('.cbd svg line').length")==3)
  ok('rival string dashed',J("()=>!!document.querySelector('.cbd svg line[stroke-dasharray]')"))
  J("()=>document.querySelector('.cbd .pol.crew').click()");pg.wait_for_timeout(300)
  ok('tap flips',J("()=>document.querySelector('.cbd .pol.crew').classList.contains('flip')"))
  ok('starts corner boy look',J("()=>!document.documentElement.classList.contains('rk2')&&!document.documentElement.classList.contains('rk3')&&RK222.tier()===1"))
  J("()=>{S.lvl=6;render()}")
  ok('middle man = boss look',J("()=>document.documentElement.classList.contains('rk2')&&document.querySelector('.cbd.t2')!=null"))
  ok('unlock note',J("()=>S.log.some(x=>/New look unlocked: Boss/.test(x.t))"))
  J("()=>{S.lvl=20;render()}")
  ok('kingpin look',J("()=>document.documentElement.classList.contains('rk3')"))
  J("()=>{S.rk222f=1;render()}")
  ok('dev force look',J("()=>!document.documentElement.classList.contains('rk3')"))
  J("()=>{S.rk222f=0;S.robOn=1;tab='rob';render()}")
  ok('heist board',J("()=>document.querySelectorAll('.hbd .hcard').length")==3)
  ok('plan buttons kept',J("()=>document.querySelectorAll('.hbd [data-a=heist]').length")==3)
  ok('old heist rows gone',J("()=>!/before cuts/.test(document.getElementById('pane').innerHTML)"))
  J("()=>{save();const s=S.slot||1;load(s);tab='beef';render()}")
  ok('save/load keeps look',J("()=>S.rk222===3&&document.documentElement.classList.contains('rk3')"))
  ok('no errors',not errs);print(errs)
  b.close()
