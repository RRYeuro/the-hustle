# lifestyle goals: tiers from what you own, perks (stress, respect, J price, family safety), one-time notes, profile card, save/load
from playwright.sync_api import sync_playwright
SETUP="()=>{localStorage.setItem('tl-clean','0');startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=22;S.cal=0;S.school='out';S.cash=20000;S._evDay=S.day;S.picQ=[];S.dr92off=1;S.recapOff=1;S.home='couch';S.car=null;S.fit='street';S.jew={};render()}"
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
  pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate;J(SETUP)
  ok=lambda n,c,x='':print(('PASS ' if c else 'FAIL ')+n,'' if c else x)
  ok('starts at zero',J("()=>['home','whip','drip'].every(k=>LF110.tier(k)===0)"))
  J("()=>{S.home='apt';S.car='jeep';S.fit='drip'}");ok('tiers from what you own',J("()=>[LF110.tier('home'),LF110.tier('whip'),LF110.tier('drip')].join()")=='2,2,2')
  J("()=>{S.lf110={best:{}};const r0=S.rep;window.__m=l110day();window.__r=S.rep-r0}");ok('first time = note + rep',J("()=>!!window.__m&&window.__r>0"))
  ok('no repeat note for same tier',J("()=>l110day()===null"))
  r=J("()=>{addCusto('Tay','snow','block');S.custos[0].gid='snow';const c=S.custos[0];S.fit='street';S.jew={};const a=custoPrice(c);S.fit='drip';S.jew={chain:1,grill:1};const b=custoPrice(c);return [a,b]}");ok('drip makes Js pay more',r[1]>r[0],r)
  r=J("()=>{S.car=null;const a=REP109.get('Nobody').respect;S.car='rover';const b=REP109.get('Nobody').respect;return [a,b]}");ok('whip earns respect',r[1]>r[0],r)
  r=J("()=>{S.heat=90;S.home='couch';const a=FM108.safe();S.home='loft';const b=FM108.safe();return [a,b]}");ok('nice home makes family feel safer',r[1]>r[0],r)
  ok('home cuts stress daily',J("()=>{S.home='loft';S.stress=50;l110day();return S.stress<50}"))
  J("()=>{render();document.querySelector('#me').click()}");ok('goals on profile card',J("()=>/Lifestyle goals/i.test(document.getElementById('mcard').innerText)"));pg.screenshot(path='/tmp/lf.png')
  J("()=>{document.getElementById('modal').hidden=true;save();const sl=S.slot;S=load(sl);render()}");ok('save/load',J("()=>!!S.lf110"))
  J("()=>{delete S.lf110;for(let i=0;i<10;i++){try{nextDay()}catch(e){window.__e=String(e)}document.getElementById('modal').hidden=true}}");ok('old save + 10 days',not J("()=>window.__e||''"))
  ok('no errors',not errs,errs);b.close()
