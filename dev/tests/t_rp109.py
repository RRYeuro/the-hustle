# reputation record: reads existing numbers, writers (rob plug, fights, memory), readers (plug price, J price, hires), shown on plug chat + workers, save/load
from playwright.sync_api import sync_playwright
SETUP="()=>{localStorage.setItem('tl-clean','0');startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=22;S.cal=0;S.school='out';S.cash=20000;S._evDay=S.day;S.picQ=[];S.dr92off=1;S.recapOff=1;render()}"
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
  pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate;J(SETUP)
  ok=lambda n,c,x='':print(('PASS ' if c else 'FAIL ')+n,'' if c else x)
  r=J("()=>{const bi=S.known[0];S.trust[bi]=70;return REP109.get(plugName(bi))}");ok('plug trust feeds the record',r['trust']==70,r)
  J("()=>{S.workers=[{id:'w',name:'Dre',hustle:5,loyal:9,wage:300,sales:5,from:0}]}");ok('worker loyalty feeds it',J("()=>REP109.get('Dre').loyal===90"))
  ok('memory changes trust',J("()=>{const a=REP109.get('Tre').trust;MEM93.set('Tre','refused');return REP109.get('Tre').trust<a}"))
  r=J("()=>{const bi=S.known[0];S.at=bi;const n=plugName(bi);const raw=S.rp109[n]||(S.rp109[n]={respect:0,fear:0,trust:0});raw.respect=-40;const lo=plugPrice('buy',G('loud'));raw.respect=50;const hi=plugPrice('buy',G('loud'));raw.respect=0;return [lo,hi]}")
  ok('respect gets better plug prices',r[1]<r[0],r)
  r=J("()=>{addCusto('Tay','loud','block');const c=S.custos[0];S.rp109.Tay={respect:-50,fear:0,trust:0};const a=custoPrice(c);S.rp109.Tay={respect:50,fear:0,trust:0};const b=custoPrice(c);return [a,b]}")
  ok('Js pay a bit more when they respect you',r[1]>r[0],r)
  ok('bump works with caps',J("()=>{REP109.bump('X',{fear:500});return REP109.get('X').fear===100}"))
  J("()=>{const bi=S.known[0];S.trust[bi]=50;S.meet={bi,how:'go',from:S.at};S.at=bi;render()}")
  ok('respect + fear on plug chat header',J("()=>/Respect \\d+ · Fear \\d+/.test(document.querySelector('#mt31 .h92').textContent)"))
  J("()=>{document.getElementById('mt31x').click()}")
  ok('worker row shows record',J("()=>/Respect \\d+/.test(paneTraps())"))
  r=J("()=>{S.rep=100;S.cands=[];S.candDay=-99;freshCands();return S.cands.map(c=>c.loyal)}");ok('big rep brings more loyal hires',all(x>=3 for x in r),r)
  J("()=>{save();const sl=S.slot;S=load(sl);render()}");ok('save/load',J("()=>!!S.rp109"))
  J("()=>{delete S.rp109;for(let i=0;i<10;i++){try{nextDay()}catch(e){window.__e=String(e)}document.getElementById('modal').hidden=true}}");ok('old save + 10 days',not J("()=>window.__e||''"))
  ok('no errors',not errs,errs);b.close()
