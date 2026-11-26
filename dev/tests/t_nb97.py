# neighborhoods: values per block, slow drift, caps, real effects (J price, business), no skip penalty, save/load
from playwright.sync_api import sync_playwright
SETUP="()=>{localStorage.setItem('tl-clean','0');startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=22;S.cal=0;S.school='out';S.cash=5000;S._evDay=S.day;S.picQ=[];S.dr92off=1;S.recapOff=1;render()}"
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
  pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate;J(SETUP)
  ok=lambda n,c,x='':print(('PASS ' if c else 'FAIL ')+n,'' if c else x)
  ok('every block has values',J("()=>BLOCKS.every((_,i)=>{const v=N97.get(i);return ['pop','pros','comp','safe'].every(k=>v[k]>=0&&v[k]<=100)})"))
  ok('line under block name',J("()=>/Busy \\d+/i.test(document.getElementById('here').textContent)"))
  pg.screenshot(path='/tmp/nb.png')
  r=J("()=>{const v=N97.get(S.at);const a=v.pop;for(let i=0;i<1;i++)N97.tick();return Math.abs(N97.get(S.at).pop-a)}")
  ok('values move slowly (one day)',r<8,r)
  r=J("()=>{N97.bump(S.at,{pop:500,pros:-500});const v=N97.get(S.at);return [v.pop,v.pros]}")
  ok('caps hold',r==[100,0],r)
  r=J("()=>{for(let i=0;i<120;i++)N97.tick();const v=N97.get(S.at);return [Math.round(v.pop),Math.round(v.pros)]}")
  ok('drifts back to normal over time',30<r[0]<80 and r[1]>15,r)
  # real effect: J price
  r=J("()=>{addCusto('Tay','loud','block');const c=S.custos[0];N97.bump(S.at,{pop:-100,pros:-100,comp:100});const lo=custoPrice(c);N97.bump(S.at,{pop:200,pros:200,comp:-200});const hi=custoPrice(c);return [lo,hi]}")
  ok('busy rich block pays more than a dead one',r[1]>r[0],r)
  r=J("()=>{S.biz={barber:1};const hb=homeBlock();N97.bump(hb,{pros:-100,pop:-100});const lo=l96pay('barber');N97.bump(hb,{pros:200,pop:200});const hi=l96pay('barber');return [lo,hi]}")
  ok('home block changes business sales',r[1]>r[0],r)
  # skipping days does not punish: heat not raised during FF
  r=J("()=>{N97.bump(S.at,{safe:100});S.heat=10;window.FF=true;for(let i=0;i<20;i++){nextDay();document.getElementById('modal').hidden=true}window.FF=false;return S.heat}")
  ok('no heat from cops while skipping',r<=10+0,r)
  # day ticks from the single day-engine wrapper
  d0=J("()=>S.nb97.pd");J("()=>{for(let i=0;i<4;i++){nextDay();document.getElementById('modal').hidden=true}}")
  ok('ticks every day',J("()=>S.nb97.pd")!=d0)
  J("()=>{save();const sl=S.slot;S=load(sl);render()}")
  ok('save/load keeps blocks',J("()=>!!(S.nb97&&S.nb97.v&&S.nb97.v[0])"))
  J("()=>{delete S.nb97;render();nextDay();document.getElementById('modal').hidden=true}")
  ok('old save gets blocks',J("()=>!!(S.nb97&&S.nb97.v[5])"))
  ok('no errors',not errs,errs)
  b.close()
