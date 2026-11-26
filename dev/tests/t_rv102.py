# rivals: daily pushes, caps, poaching, hold-block choices, flip only on live days after warning, save/load
from playwright.sync_api import sync_playwright
SETUP="()=>{localStorage.setItem('tl-clean','0');startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=22;S.cal=0;S.school='out';S.cash=20000;S._evDay=S.day;S.picQ=[];S.dr92off=1;S.recapOff=1;render()}"
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
  pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate;J(SETUP)
  ok=lambda n,c,x='':print(('PASS ' if c else 'FAIL ')+n,'' if c else x)
  r=J("()=>{const a=BLOCKS.map((_,b)=>N97.get(b).comp);for(let i=0;i<10;i++)l102day();return BLOCKS.some((_,b)=>N97.get(b).comp>a[b])}")
  ok('rivals push into blocks',r)
  ok('rivals stay in 0-100',J("()=>{for(let i=0;i<300;i++)l102day();return BLOCKS.every((_,b)=>{const c=N97.get(b).comp;return c>=0&&c<=100})}"))
  # poaching
  J("()=>{addCusto('Tay','loud','block');S.custos[0].loy=40;N97.get(homeBlock()).comp=90;for(let i=0;i<12;i++)l102day()}")
  ok('crowded home block poaches Js',J("()=>S.custos.length===0||S.custos[0].loy<40"))
  # hold row + choices
  J("()=>{N97.get(S.at).comp=75;tab='block';render()}");ok('hold row shows at 60+',J("()=>!!document.querySelector('[data-r102m]')"))
  J("()=>document.querySelector('[data-r102m]').click()");ok('choices show expected result',J("()=>document.querySelectorAll('#mcard [data-r102]').length===3&&/Rivals/.test(document.getElementById('mcard').innerText)"));pg.screenshot(path='/tmp/rv.png')
  addCusto=J("()=>{addCusto('Bo','loud','block');return custoPrice(S.custos[S.custos.length-1])}")
  J("()=>document.querySelector('[data-r102=cut]').click()")
  ok('undercut lowers rivals + J price',J("()=>N97.get(S.at).comp<75")and J("()=>custoPrice(S.custos[S.custos.length-1])")<addCusto)
  c0=J("()=>N97.get(S.at).comp");J("()=>{S.soldiers=3;menuR=document.querySelector('[data-r102m]');}")
  J("()=>{const L=S.crews.filter(c=>c.alive)[0];L.beef=0;S.rv102.pk[S.at]=L.id;}")
  J("()=>{document.getElementById('modal').hidden=true;N97.get(S.at).comp=80;tab='block';render();document.querySelector('[data-r102m]').click();document.querySelector('[data-r102=send]').click()}")
  ok('send soldiers: rivals -20, beef up',J("()=>N97.get(S.at).comp<=61")and J("()=>S.crews.find(c=>c.id===S.rv102.pk[S.at]).beef>=15"))
  m0=J("()=>S.cash");J("()=>{N97.get(S.at).comp=80;tab='block';render();document.querySelector('[data-r102m]').click();document.querySelector('[data-r102=pay]').click()}")
  ok('pay off: costs cash, rivals down',J("()=>S.cash")<m0 and J("()=>N97.get(S.at).comp<=68"))
  # flip: owned block at 85+ for 3 live days (with warning), not during skip
  J("()=>{S.owner=S.owner||[];S.owner[S.at]='me';S.rv102.hot={};window.FF=true;for(let i=0;i<5;i++){N97.get(S.at).comp=95;l102day()}window.FF=false}")
  ok('no flip while skipping',J("()=>S.owner[S.at]==='me'"))
  J("()=>{const n=[];for(let i=0;i<3;i++){N97.get(S.at).comp=95;const m=l102day();if(m)n.push(m.t)}window.__n=n}")
  ok('warning then flip after 3 live days',J("()=>S.owner[S.at]!=='me'&&window.__n.some(t=>/about to fall/.test(t))"),J("()=>window.__n"))
  J("()=>{save();const sl=S.slot;S=load(sl);render()}");ok('save/load',J("()=>!!S.rv102"))
  J("()=>{delete S.rv102;for(let i=0;i<20;i++){try{nextDay()}catch(e){window.__e=String(e)}document.getElementById('modal').hidden=true}}");ok('old save + 20 days',not J("()=>window.__e||''")and J("()=>!!S.rv102"))
  ok('no errors',not errs,errs);b.close()
