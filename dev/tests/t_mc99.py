# music loop: vault, promo, release boost, fans growth caps, booking + show day, deposit, no fan multiplier on other income, save/load
from playwright.sync_api import sync_playwright
SETUP="()=>{localStorage.setItem('tl-clean','0');startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=22;S.cal=0;S.school='out';S.cash=30000;S.clean=30000;S._evDay=S.day;S.picQ=[];S.dr92off=1;S.recapOff=1;S.rapOn=1;S.rap=Object.assign(S.rap||{},{fans:2500,hype:40,songs:[],fat:0});render()}"
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
  pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate;J(SETUP)
  ok=lambda n,c,x='':print(('PASS ' if c else 'FAIL ')+n,'' if c else x)
  J("()=>{tab='rap';render()}");ok('studio shows vault + promo + shows',J("()=>{const t=document.getElementById('pane').textContent;return /Vault and promo/.test(t)&&/Book a show/.test(t)}"))
  c0=J("()=>S.cash");J("()=>{l99vault('Test Song',70,false,null);document.getElementById('modal').hidden=true}")
  ok('save for later costs $300, not released',J("()=>S.rap.vault.length===1&&S.rap.songs.length===0")and J("()=>S.cash")==c0-300)
  f0=J("()=>S.rap.fans")
  J("()=>{document.querySelector('[data-m99=c][data-k=street]').click()}");pv=J("()=>S.rap.pr99.v")
  ok('street team raises promo',pv>=15,pv)
  ok('same campaign once a day',J("()=>{const b=document.querySelector('[data-m99=c][data-k=street]');return !b||b.disabled}"))
  J("()=>{S.rap.pr99.v=100;Math.random=(()=>{let r=1;return ()=>{r=(r*9301+49297)%233280;return r/233280}})()}")
  g=J("()=>{const f=S.rap.fans;document.querySelector('[data-m99=r]').click();document.getElementById('modal').hidden=true;return S.rap.fans-f}")
  ok('release from vault adds fans',g>0,g)
  ok('promo mostly resets after release',J("()=>S.rap.pr99.v<=30"))
  ok('released song gets first-week stream boost',J("()=>S.rap.songs[0].pb>0"))
  # fans don't multiply other income
  J("()=>{S.biz={barber:1}}");a=J("()=>l96pay('barber')");J("()=>{S.rap.fans=500000}");b2=J("()=>l96pay('barber')")
  ok('fans do not change business income',a==b2,[a,b2])
  J("()=>{addCusto('Tay','loud','block');}");a=J("()=>{S.rap.fans=0;return custoPrice(S.custos[0])}");b2=J("()=>{S.rap.fans=500000;return custoPrice(S.custos[0])}")
  ok('fans do not change J prices',a==b2,[a,b2])
  J("()=>{S.rap.fans=2500}")
  # booking + show day
  c0=J("()=>S.cash");J("()=>{tab='rap';render();document.querySelector('[data-m99=b][data-k=club]').click()}")
  ok('book club takes deposit',J("()=>!!S.rap.bk99")and J("()=>S.cash")==c0-1000)
  J("()=>{S.rap.bk99.day=S.day+1;nextDay();document.getElementById('modal').hidden=true}")
  ok('show happens on the day',J("()=>!S.rap.bk99"))
  ok('show listed in Today',J("()=>!!(S.dy98&&S.dy98.b.some(b=>/show:/.test(b.t)))"))
  ok('show money in ledger as music',J("()=>{L95.flush();return S.lg95.e.some(e=>e.k==='music'&&e.n>0)}"))
  # missed show in jail
  J("()=>{S.rap.bk99={k:'club',day:S.day+1,dep:1000};S.pr={d:5};const r=l99day.call(null);S.day++;const m=l99day();S.pr=null;window.__m=m&&m.t}")
  ok('missed show loses deposit',J("()=>/missed/i.test(window.__m||'')"),J("()=>window.__m"))
  # save/load + old save
  J("()=>{save();const sl=S.slot;S=load(sl);render()}");ok('save/load keeps vault/promo',J("()=>Array.isArray(S.rap.vault)&&!!S.rap.pr99"))
  J("()=>{delete S.rap.vault;delete S.rap.pr99;tab='rap';render()}");ok('old save upgrades',J("()=>Array.isArray(S.rap.vault)"))
  J("()=>{for(let i=0;i<20;i++){try{nextDay()}catch(e){window.__e=String(e)}document.getElementById('modal').hidden=true}}");ok('20 days no crash',not J("()=>window.__e||''"))
  J("()=>{tab='rap';render()}");pg.screenshot(path='/tmp/mc.png',full_page=True)
  ok('no errors',not errs,errs);b.close()
