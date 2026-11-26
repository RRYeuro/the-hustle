# books must add up: believable limit per business, suspicion from over-washing, decay, audit trigger, row text, save/load
from playwright.sync_api import sync_playwright
SETUP="()=>{localStorage.setItem('tl-clean','0');startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=22;S.cal=0;S.school='out';S.cash=60000;S.clean=0;S._evDay=S.day;S.picQ=[];S.dr92off=1;S.recapOff=1;S.biz={laundry:1};render()}"
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
  pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate;J(SETUP)
  ok=lambda n,c,x='':print(('PASS ' if c else 'FAIL ')+n,'' if c else x)
  lim=J("()=>B101.believe('laundry')");ok('business has a believable limit',lim>0,lim)
  ok('row shows the limit',J("()=>/Looks normal up to/.test(launHTML())"))
  # wash within limit: no suspicion
  J("()=>{S.bk101={v:0,d:S.day,w:{}};launAct({dataset:{k:'laundry',v:'1000',a:'lwash'}});document.getElementById('modal').hidden=true}")
  w=J("()=>S.bk101.w.laundry||0");v=J("()=>S.bk101.v");print('   washed',w,'limit',lim,'susp',v)
  ok('washing within limit is safe',(w<=lim and v==0) or w>lim,[w,lim,v])
  # wash way over (several max washes)
  J("()=>{for(let i=0;i<3;i++){launAct({dataset:{k:'laundry',v:'max',a:'lwash'}});document.getElementById('modal').hidden=true}}")
  v=J("()=>S.bk101.v");w=J("()=>S.bk101.w.laundry||0")
  ok('over-washing builds suspicion',(w>lim and v>0),[w,lim,v])
  ok('suspicion shows in laundering',J("()=>S.bk101.v<10||/Books suspicion/.test(launHTML())"))
  a=J("()=>{const a=S.bk101.v;nextDay();document.getElementById('modal').hidden=true;return [a,S.bk101.v]}")
  ok('suspicion fades daily',a[1]<a[0] or a[0]==0,a)
  J("()=>{S.audit=0;S.bk101.v=75}");n=J("()=>{const m=l101day();return [!!m,S.audit>S.day,S.bk101.v]}")
  ok('at 70 the IRS pulls the books (audit set)',n[0] and n[1] and n[2]==40,n)
  ok('better rep washes more',J("()=>{const o=S.bp96.laundry;o.rep=10;const a=B101.believe('laundry');o.rep=95;const b=B101.believe('laundry');return b>a}"))
  J("()=>{save();const sl=S.slot;S=load(sl);render()}");ok('save/load keeps books',J("()=>!!S.bk101"))
  J("()=>{delete S.bk101;tab='money';render();launHTML()}");ok('old save fine',J("()=>!!S.bk101"))
  ok('no errors',not errs,errs);b.close()
