# ledger: sales, laundering, safe moves, crypto, overnight, save/load, multi-day
from playwright.sync_api import sync_playwright
SETUP="()=>{localStorage.setItem('tl-clean','0');startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S.cash=20000;S.clean=5000;S.heat=10;S.rep=40;S._evDay=S.day;S.picQ=[];S.dr92off=1;S.recapOff=1;render();L95.reset();L95.flush()}"
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
  pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate;J(SETUP)
  ok=lambda n,c,x='':print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
  d=J("()=>S.day")
  J("()=>{addCusto('Tay','loud','block');S.inv.loud=200;S.custos[0].gid='loud';serveCusto(0,true,{});L95.flush()}")
  D=J(f"()=>L95.day({d})");ok('J sale booked as income',D['i']>0 and D['k'].get('sales',0)>0,D)
  J("()=>{L95.ctx('Laundering at the teller');S.cash-=100;S.clean=Math.min(S.cash,cleanCash()+2000);L95.flush()}")
  D=J(f"()=>L95.day({d})");ok('laundering = transfer + fee only',D['tr']>=2000 and D['o']==100,D)
  i0=D['i'];J("()=>{holdIn(S,'safe','safeClean',3000);L95.flush('Safe')}")
  D=J(f"()=>L95.day({d})");ok('safe move is transfer, not income',D['i']==i0 and D['tr']>=5000,D)
  J("()=>{holdOut(S,'safe','safeClean',3000);L95.flush('Safe')}")
  D=J(f"()=>L95.day({d})");ok('safe back out is transfer',D['i']==i0,D)
  J("()=>{const c=cleanCash();S.cash-=1000;S.clean=c-1000;S.cr={amt:1000,d:S.day};L95.flush('crypto buy')}")
  D=J(f"()=>L95.day({d})");ok('crypto buy is transfer',D['i']==i0 and D['o']==100,D)
  J("()=>{S.cr=null;S.cash+=1400;S.clean=cleanCash()+1400;L95.flush('crypto cash out')}")
  D=J(f"()=>L95.day({d})");ok('crypto gain = trading, not income',D['i']==i0 and D['t']==400,D)
  J("()=>{L95.ctx('Bought a chain at the mall');S.cash-=500;L95.flush()}")
  D=J(f"()=>L95.day({d})");ok('spending tagged',D['k'].get('life',0)==-500,D)
  # overnight
  J("()=>{nextDay();document.getElementById('modal').hidden=true}")
  D=J(f"()=>L95.day({d+1})");print('  overnight day',d+1,D)
  # save / load keeps ledger, loading is not income
  n0=J("()=>S.lg95.e.length");J("()=>{save()}");c0=J("()=>S.cash")
  J("()=>{const sl=S.slot;S=load(sl);render();L95.flush()}")
  ok('ledger survives save/load',J("()=>S.lg95&&S.lg95.e.length")==n0)
  ok('loading not booked',J("()=>S.lg95.e.length")==n0)
  # old save without ledger
  J("()=>{delete S.lg95;render();L95.flush();S.cash+=250;L95.ctx('serve');L95.flush()}")
  ok('old save gets ledger',J("()=>!!S.lg95&&S.lg95.e.length>=1"))
  # multi-day run
  J("()=>{for(let i=0;i<20;i++){try{nextDay()}catch(e){window.__e=String(e)}document.getElementById('modal').hidden=true}}")
  ok('20 days no crash',not J("()=>window.__e||''"),J("()=>window.__e||''"))
  ok('days capped',J("()=>Object.keys(S.lg95.days).length<=60 && S.lg95.e.length<=250"))
  J("()=>{tab='exp';render()}");ok('money history shows',J("()=>/money history/i.test(document.getElementById('pane').innerText)"))
  pg.screenshot(path='/tmp/lg95.png',full_page=False)
  print('errors',errs[:4]);b.close()
