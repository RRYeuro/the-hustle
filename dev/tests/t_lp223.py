# lp223: scam laptop + studio software
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c):R.append(c);print(('PASS ' if c else 'FAIL ')+n)
with sync_playwright() as p:
  b=p.chromium.launch();c=b.new_context(viewport={'width':393,'height':852},has_touch=True,is_mobile=True);pg=c.new_page()
  errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
  pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate
  J("()=>{startLife('shade');document.getElementById('modal').hidden=true;S.age=20;S.scamOn=1;S.scam={noto:30,laptop:1,did:{},runs:9};S.rapOn=1;S.rap.fans=900;S.rap.hype=62;S.rap.songs=[{title:'A',q:58,day:S.day-3},{title:'B',q:81,day:S.day-1},{title:'C',q:44,day:S.day,diss:1}];tab='move';render()}")
  ok('laptop on move tab',J("()=>!!document.querySelector('#pane .lap223 .scr')"))
  ok('scam windows',J("()=>document.querySelectorAll('.lap223 .win').length")>=2)
  ok('ghost work terminal',J("()=>!!document.querySelector('.lap223 .win.term')"))
  ok('scam buttons kept',J("()=>document.querySelectorAll('.lap223 [data-a=scam]').length")>=3)
  ok('cracked at corner boy',J("()=>!!document.querySelector('.lap223.t1')"))
  J("()=>{S.rk222f=3;render()}")
  ok('clean at kingpin',J("()=>!!document.querySelector('.lap223.t3')"))
  J("()=>{S.rk222f=0;tab='rap';render()}")
  ok('studio software',J("()=>!!document.querySelector('#pane .daw223 .tp')"))
  ok('song lanes',J("()=>document.querySelectorAll('.daw223 .lane').length")==3)
  ok('diss lane red',J("()=>document.querySelector('.daw223 .lane').style.getPropertyValue('--lc')==='#ff5a4f'"))
  ok('no duplicate hype bar',J("()=>![...document.querySelectorAll('.daw223 .bar i')].some(i=>i.style.width==='62%')"))
  ok('record button kept',J("()=>!!document.querySelector('.daw223 [data-a=rec]')"))
  ok('no errors',not errs);print(errs)
  b.close()
