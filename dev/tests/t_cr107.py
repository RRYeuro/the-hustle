# credit: score from clean income, loan tiers, weekly payment from clean, missed payment + collectors, payoff, ledger transfer, minors locked, save/load
from playwright.sync_api import sync_playwright
SETUP="()=>{localStorage.setItem('tl-clean','0');startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=22;S.cal=0;S.school='out';S.cash=10000;S.clean=8000;S._evDay=S.day;S.picQ=[];S.dr92off=1;S.recapOff=1;render()}"
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
  pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate;J(SETUP)
  ok=lambda n,c,x='':print(('PASS ' if c else 'FAIL ')+n,'' if c else x)
  ok('starts thin, no loan offer',J("()=>CR107.get().sc===520&&!CR107.offer()"))
  a=J("()=>{for(let i=0;i<10;i++){L95.post('job',1200,'Paycheck',true);nextDay();document.getElementById('modal').hidden=true}return CR107.get().sc}")
  ok('clean income raises score',a>520,a)
  J("()=>{CR107.get().sc=690;tab='exp';render()}");ok('bank offers a loan at 600+',J("()=>/Bank loan up to/.test(document.getElementById('pane').textContent)"))
  c0=J("()=>S.cash");J("()=>document.querySelector('[data-cr107=take]').click()")
  ok('loan paid out as clean cash',J("()=>!!CR107.get().loan")and J("()=>S.cash")>c0)
  ok('loan is a transfer, not income',J("()=>{L95.flush();const D=L95.day(S.day);return !(D.k.loan>0)&&D.tr>0}"))
  J("()=>{const L=CR107.get().loan;L.due=S.day;S.clean=S.cash;window.__m=l107day()}")
  ok('weekly payment from clean cash',J("()=>/came out of your clean cash|Paid off/.test(window.__m.t)"))
  s0=J("()=>CR107.get().sc");J("()=>{const L=CR107.get().loan;L.due=S.day;S.clean=0;window.__m=l107day()}")
  ok('missed payment crushes score',J("()=>CR107.get().sc")<s0 and J("()=>/Missed/.test(window.__m.t)"))
  J("()=>{const L=CR107.get().loan;L.due=S.day;S.clean=0;window.__m=l107day()}");ok('second miss brings collectors',J("()=>/Collectors/.test(window.__m.t)"))
  J("()=>{S.cash=200000;S.clean=200000;tab='exp';render();document.querySelector('[data-cr107=pay]').click()}");ok('pay off early',J("()=>!CR107.get().loan"))
  ok('minors have no credit',J("()=>{S.age=16;const h=l107html();const m=l107day();S.age=22;return h===''&&m===null}"))
  J("()=>{save();const sl=S.slot;S=load(sl);render()}");ok('save/load',J("()=>!!S.cr107"))
  J("()=>{delete S.cr107;for(let i=0;i<10;i++){try{nextDay()}catch(e){window.__e=String(e)}document.getElementById('modal').hidden=true}}");ok('old save + 10 days',not J("()=>window.__e||''"))
  ok('no errors',not errs,errs);b.close()
