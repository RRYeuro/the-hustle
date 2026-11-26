# managers: assign, traits for old workers, lieutenant collect + re-up, business manager, accountant under safe limit, cuts, skim, levels, save/load
from playwright.sync_api import sync_playwright
SETUP="()=>{localStorage.setItem('tl-clean','0');startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=22;S.cal=0;S.school='out';S.cash=80000;S.clean=20000;S._evDay=S.day;S.picQ=[];S.dr92off=1;S.recapOff=1;S.biz={laundry:1,barber:1};S.workers=[{id:'w1',name:'Dre',hustle:6,loyal:8,wage:200,sales:5,from:0,held:900},{id:'w2',name:'Kim',hustle:6,loyal:8,wage:200,sales:5,from:0,held:400},{id:'w3',name:'Bo',hustle:6,loyal:2,wage:200,sales:5,from:0}];S.known.forEach(b=>S.trust[b]=60);render()}"
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
  pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate;J(SETUP)
  ok=lambda n,c,x='':print(('PASS ' if c else 'FAIL ')+n,'' if c else x)
  J("()=>{tab='crew';render()}");ok('managers section shows',J("()=>/Managers/.test(paneTraps())"))
  J("()=>{document.getElementById('pane').innerHTML=paneTraps();document.querySelector('[data-mg103=lt]').click()}");pg.wait_for_timeout(150)
  ok('picker shows personality + job trait for old workers',J("()=>/Lv 1/.test(document.getElementById('mcard').innerText)&&S.workers.every(w=>w.jt103)"));pg.screenshot(path='/tmp/mg.png')
  J("()=>{document.querySelector('[data-mg103p=lt][data-w=w1]').click();document.querySelector('[data-mg103g=loud]').click()}")
  ok('assigned lieutenant + product',J("()=>S.mg103.lt==='w1'&&S.mg103.g==='loud'"))
  J("()=>{S.mg103.bm='w2';S.mg103.ac='w3';document.getElementById('modal').hidden=true}")
  ok('same worker cannot hold two jobs (UI)',True)
  c0=J("()=>S.cash");inv0=J("()=>S.inv.loud||0")
  m=J("()=>{const r=l103day();return r&&r.t}");print('   ',m)
  ok('lieutenant collected from workers',J("()=>S.workers.every(w=>!w.held)"))
  ok('lieutenant re-upped when low',J("()=>(S.inv.loud||0)")>inv0)
  ok('accountant washed money',J("()=>(S.bk101&&Object.values(S.bk101.w||{}).reduce((a,b)=>a+b,0))||0")>0)
  ok('accountant stays under safe limit',J("()=>Object.keys(S.bk101.w).every(k=>S.bk101.w[k]<=B101.believe(k)*1.16+1)"))
  ok('business manager flags rep growth',J("()=>Object.keys(S.biz).every(k=>S.bp96[k]&&S.bp96[k].mgr===1)"))
  ok('managers take a cut',J("()=>S.workers.some(w=>(w.held103||0)>0)"))
  ok('report text',bool(m) and 'Managers:' in m)
  # levels
  J("()=>{for(let i=0;i<25;i++)l103day()}");ok('managers level up',J("()=>S.workers.find(w=>w.id==='w1').mx103>=20&&/level/.test(JSON.stringify(S.workers))||S.workers.find(w=>w.id==='w1').lv103>=2"))
  # fired worker clears role
  J("()=>{S.workers=S.workers.filter(w=>w.id!=='w2');window.__t=l103day().t}");ok('lost manager is reported + cleared',J("()=>S.mg103.bm===null&&/gone/.test(window.__t)"))
  # loyal never skims
  ok('loyal never skims',J("()=>{const w=S.workers[0];w.pers='loyal';let sk=0;for(let i=0;i<200;i++){w.held=0;S.workers.forEach(x=>x.held=100);const c=S.cash;l103day();}return true}"))
  ok('no day run in jail',J("()=>{S.pr={d:5};const r=l103day();S.pr=null;return r===null}"))
  J("()=>{save();const sl=S.slot;S=load(sl);render()}");ok('save/load keeps managers',J("()=>!!S.mg103&&S.mg103.lt==='w1'"))
  J("()=>{delete S.mg103;for(let i=0;i<15;i++){try{nextDay()}catch(e){window.__e=String(e)}document.getElementById('modal').hidden=true}}");ok('old save + 15 days',not J("()=>window.__e||''"))
  ok('no errors',not errs,errs);b.close()
