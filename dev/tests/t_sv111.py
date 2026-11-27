# saves: normal save + reload, render error still saves, quota retry, warning, backup restore, pagehide save, real menu flow
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={'width':390,'height':844});pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
  pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.evaluate("()=>localStorage.clear()");pg.reload();pg.wait_for_timeout(1500);J=pg.evaluate
  ok=lambda n,c,x='':print(('PASS ' if c else 'FAIL ')+n,'' if c else x)
  # real flow: new story -> slot 2 -> normal -> character -> skip traits -> skip tutorial
  pg.click('#ms');pg.wait_for_timeout(300);pg.click('#mcard [data-slot="2"]');pg.wait_for_timeout(300);pg.get_by_text('Normal').first.click();pg.wait_for_timeout(400)
  J("()=>{const b=[...document.querySelectorAll('#mcard button')].find(b=>/THE /.test(b.innerText));b.click()}");pg.wait_for_timeout(300);pg.click('#cyes');pg.wait_for_timeout(300);pg.click('#tgo');pg.wait_for_timeout(400)
  J("()=>{const s=document.getElementById('tu73s');s&&s.click()}");pg.wait_for_timeout(300)
  J("()=>{document.getElementById('modal').hidden=true;for(let i=0;i<4;i++){nextDay();document.getElementById('modal').hidden=true;render()}}")
  d=J("()=>S.day");ok('real new game saves to the picked slot',J("()=>readSlot(2)&&readSlot(2).day")==d,[d,J("()=>readSlot(2)&&readSlot(2).day")])
  ok('backup copy written',J("()=>!!localStorage.getItem(SV111.bakKey(2))"))
  pg.reload();pg.wait_for_timeout(1500);ok('after reload Continue is there',J("()=>!!document.getElementById('mc')"))
  pg.click('#mc');pg.wait_for_timeout(400);ok('continue loads the same day',J("()=>S.day")==d)
  # render error still saves
  J("()=>{window.__mu=missionUI;missionUI=function(){throw new Error('boom')};S.day+=1;try{render()}catch(e){}missionUI=window.__mu}")
  ok('a render error does not block the save',J("()=>readSlot(2).day===S.day"))
  # quota: first write fails, retry after trimming
  J("()=>{const o=localStorage.setItem.bind(localStorage);let n=0;localStorage.setItem=function(k,v){if(n++===0&&String(k).indexOf('-bak')<0)throw new DOMException('full','QuotaExceededError');return o(k,v)};S.day+=1;save();localStorage.setItem=o}")
  ok('save retries after a storage error',J("()=>readSlot(2).day===S.day"))
  J("()=>{const o=localStorage.setItem.bind(localStorage);localStorage.setItem=function(){throw new DOMException('full','QuotaExceededError')};S.day+=1;save();localStorage.setItem=o}")
  ok('player is told when saving fails',J("()=>SV111.warned()"))
  # backup restore when main save is broken
  J("()=>{save();localStorage.setItem(SV111.bakKey(2),localStorage.getItem(slotKey(2)));localStorage.setItem(slotKey(2),'{broken')}")
  ok('broken main save falls back to backup (slot list)',J("()=>!!readSlot(2)"))
  ok('broken main save falls back to backup (load)',J("()=>{const s=load(2);return !!(s&&s.day)}"))
  # pagehide saves
  J("()=>{S.day+=3;window.dispatchEvent(new Event('pagehide'))}");ok('closing the page saves',J("()=>{try{return JSON.parse(localStorage.getItem(slotKey(2))).day===S.day}catch(e){return false}}"))
  ok('no errors',not [e for e in errs if 'boom' not in e],errs);b.close()
