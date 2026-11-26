# case file: evidence from patterns, reducers, stages, raid gating, undercover Js, save/load, multi-day
from playwright.sync_api import sync_playwright
SETUP="()=>{localStorage.setItem('tl-clean','0');startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=22;S.cal=0;S.school='out';S.cash=5000;S.clean=5000;S._evDay=S.day;S.picQ=[];S.dr92off=1;S.recapOff=1;render()}"
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
  pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate;J(SETUP)
  ok=lambda n,c,x='':print(('PASS ' if c else 'FAIL ')+n,'' if c else x)
  # same block sales for 8 days
  r=J("""()=>{const out=[];for(let i=0;i<8;i++){L95.post('sales',600,'Sold to a J',false);nextDay();document.getElementById('modal').hidden=true;out.push(Math.round(C100.get().ev*10)/10)}return out}""")
  ok('selling same block builds evidence',r[-1]>r[1] and C100 if False else r[-1]>r[2],r)
  ok('streak tracked',J("()=>C100.get().st>=6"))
  # moving blocks breaks streak
  J("()=>{S.at=(S.at+1)%BLOCKS.length;L95.post('sales',600,'Sold to a J',false);nextDay();document.getElementById('modal').hidden=true}")
  ok('switching blocks resets streak',J("()=>C100.get().st===1"))
  # lawyer + lay low shrink it
  J("()=>{C100.get().ev=50}");a=J("()=>{S.lawPay=1;for(let i=0;i<5;i++){nextDay();document.getElementById('modal').hidden=true}S.lawPay=0;return C100.get().ev}")
  ok('lawyer shrinks the case',a<45,a)
  # dirty cash pile adds evidence
  J("()=>{C100.get().ev=10;S.cash=90000;S.clean=0}");a=J("()=>{for(let i=0;i<3;i++){nextDay();document.getElementById('modal').hidden=true}return C100.get().src.cash||0}")
  ok('big dirty cash adds evidence',a>0,a)
  J("()=>{S.cash=5000;S.clean=5000}")
  # undercover J
  J("()=>{addCusto('Narc','loud','block');S.custos[S.custos.length-1].uc=1;S.custos[S.custos.length-1].buys=5;S.inv.loud=100;C100.get().ev=0;serveCusto(S.custos.length-1,true,{})}")
  ok('undercover J adds evidence',J("()=>(C100.get().src.uc||0)>=6"),J("()=>JSON.stringify(C100.get())"))
  # raid gating
  ok('no raid when case is low',J("()=>{C100.get().ev=40;let n=0;for(let i=0;i<200;i++)if(l100raid())n++;return n===0}"))
  ok('raid possible when case is strong, then case drops',J("()=>{let n=0;for(let i=0;i<50;i++){C100.get().ev=95;if(l100raid()){n++;break}}return n===1&&C100.get().ev===40}"))
  # block row shows at stage 1+
  J("()=>{C100.get().ev=65;tab='block';render()}");ok('case row on Block tab',J("()=>!!document.querySelector('[data-cf100]')"))
  J("()=>document.querySelector('[data-cf100]').click()");ok('detail popup',J("()=>/Case file/.test(document.querySelector('#mcard h2').textContent)"));pg.screenshot(path='/tmp/cf.png')
  J("()=>{document.getElementById('modal').hidden=true;C100.get().ev=5;tab='block';render()}");ok('no row when case is cold',J("()=>!document.querySelector('[data-cf100]')"))
  # caps
  ok('evidence capped 0-100',J("()=>{C100.add('heat',500);const a=C100.get().ev;C100.get().ev=-50;C100.add('heat',0);return a===100}"))
  J("()=>{save();const sl=S.slot;S=load(sl);render()}");ok('save/load keeps case',J("()=>!!S.case"))
  J("()=>{delete S.case;render();nextDay();document.getElementById('modal').hidden=true}");ok('old save gets case',J("()=>!!S.case&&isFinite(S.case.ev)"))
  J("()=>{for(let i=0;i<25;i++){try{nextDay()}catch(e){window.__e=String(e)}document.getElementById('modal').hidden=true}}");ok('25 days no crash',not J("()=>window.__e||''"))
  ok('no errors',not errs,errs);b.close()
