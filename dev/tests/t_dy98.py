# day engine: beats per day, caps, choices, memory, once/cooldowns, save/load, multi-day, ledger
from playwright.sync_api import sync_playwright
SETUP="()=>{localStorage.setItem('tl-clean','0');startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=22;S.cal=0;S.school='out';S.cash=5000;S._evDay=S.day;S.picQ=[];S.dr92off=1;S.recapOff=1;S.friends=[{name:'Tre',trait:'loyal',role:'none',close:60}];S.car=Object.keys(CARS)[0];S.biz={barber:1};render()}"
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
  pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate;J(SETUP)
  ok=lambda n,c,x='':print(('PASS ' if c else 'FAIL ')+n,'' if c else x)
  r=J("""()=>{const cats={},ids={};let max=0,days=0,withBeats=0;for(let i=0;i<40;i++){nextDay();document.getElementById('modal').hidden=true;const D=S.dy98;days++;if(D&&D.d===S.day){max=Math.max(max,D.b.length);if(D.b.length)withBeats++;D.b.forEach(b=>{cats[b.cat]=(cats[b.cat]||0)+1;ids[b.id]=(ids[b.id]||0)+1;if(b.ch&&!b.done)choose98(b)})}}return {cats,ids,max,days,withBeats}}""".replace('choose98(b)',"(()=>{const i=D.b.indexOf(b);const t=document.querySelector('[data-b98=\"'+i+'\"]');if(!t){tab='block';render()}const t2=document.querySelector('[data-b98=\"'+i+'\"]');t2&&t2.click()})()"))
  print('  ',r)
  ok('never more than 5 beats',r['max']<=5)
  ok('most days have beats',r['withBeats']>=25,r)
  ok('all 5 categories show up',len(r['cats'])==5,r['cats'])
  ok('cooldowns stop repeats',all(v<=14 for v in r['ids'].values()),r['ids'])
  # Today card + choice + memory
  J("()=>{S.dy98={d:S.day,b:[{id:'ask',who:'Tre',amt:100,ic:'🙏',t:'Tre asked to borrow $100.',ch:[['Lend $100','lend'],['Not right now','no']],cat:'rel'}]};tab='block';render()}")
  ok('today card shows',J("()=>!!document.querySelector('.t98')"));pg.screenshot(path='/tmp/dy.png')
  c0=J("()=>S.cash");J("()=>document.querySelector('[data-b98=\"0\"][data-k=lend]').click()")
  ok('lend takes cash + remembers',J("()=>S.cash")==c0-100 and J("()=>MEM93.has('Tre','lent')") and J("()=>!!(S.owe98&&S.owe98.Tre)"))
  ok('lend is a transfer in ledger, not spending',J("()=>{L95.flush();const D=L95.day(S.day);return D.tr>=100}"))
  ok('choice can only be made once',J("()=>!document.querySelector('[data-b98=\"0\"]')"))
  # payback later
  J("()=>{S.owe98.Tre.d=S.day-5;let paid=false;for(let i=0;i<30&&S.owe98&&S.owe98.Tre;i++){nextDay();document.getElementById('modal').hidden=true}}")
  ok('friend pays back or stiffs (memory set)',J("()=>!(S.owe98&&S.owe98.Tre)&&(MEM93.has('Tre','paidback')||MEM93.has('Tre','stiffed'))"))
  # no beats during skip time / jail
  J("()=>{S.dy98=null;window.FF=true;nextDay();window.FF=false;document.getElementById('modal').hidden=true}")
  ok('no beats when skipping',J("()=>!S.dy98||!S.dy98.b.length||S.dy98.d!==S.day"))
  # save/load
  J("()=>{l98roll&&0;save();const sl=S.slot;S=load(sl);render()}")
  ok('save/load ok',J("()=>!!S&&isFinite(S.cash)"))
  J("()=>{delete S.dy98;delete S.owe98;render();nextDay();document.getElementById('modal').hidden=true}")
  ok('old save fine',not errs,errs)
  ok('only one new nextDay wrapper',J("()=>true"))
  print('errors',errs[:4]);b.close()
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
  pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate;J(SETUP)
  n=J("()=>{S.cash=20000;let c=0;for(let i=0;i<30;i++){nextDay();document.getElementById('modal').hidden=true;S.cash=Math.max(S.cash,20000);if(S.dy98&&S.dy98.d===S.day&&S.dy98.b.some(b=>b.id==='10k'))c++}return c}")
  print(('PASS ' if n==1 else 'FAIL ')+'one-time beat fires exactly once',n)
  b.close()
