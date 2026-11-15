import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1280,'height':900});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:200]) if m.type=='error' and 'sk' in m.text else None)
    pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S.cash=3000;S.en=60;S._evDay=S.day;S.picQ=[];S.fd=null;S.at=0;S.lt={house:S.day};tab='move';render()}");pg.wait_for_timeout(400)
    r=J("()=>[...document.querySelectorAll('#fm26 .lk59')].map(b=>b.dataset.lk59)")
    ck('lick pins on the Move map (store, pharmacy, car, tipped house)',set(['store','pharm','car','house'])<=set(r),json.dumps(r))
    J("()=>document.querySelector('#fm26 .lk59[data-lk59=\"store\"]').click()");pg.wait_for_timeout(200)
    ck('pin opens lick card; away = go there first',J("()=>/corner store/i.test(document.querySelector('#mcard').innerText)&&!!document.getElementById('mv59')"))
    J("()=>document.getElementById('mv59').click()");pg.wait_for_timeout(200)
    ck('go there first uses the travel chooser',J("()=>/Go to/.test(document.querySelector('#mcard h2').textContent)"))
    J("()=>{document.getElementById('modal').hidden=true;S.at=1;window.l59card('store',1)}")
    ck('at the block: Do it button',J("()=>!!document.getElementById('go59')"))
    ck('old lick list points to the map',J("()=>/show up on your map/.test(paneLicks())"))
    J("()=>{document.getElementById('modal').hidden=true;S.at=placeAt('mall');openPlace('mall')}");pg.wait_for_timeout(200)
    ck('mall sells the burner (no big pictures)',J("()=>!!document.querySelector('#mcard [data-b59=\"buy\"]')&&!document.querySelector('#mcard img[src=\"'+ARTX('g_glasses')+'\"]')"))
    J("()=>document.querySelector('#mcard [data-b59=\"buy\"]').click()");pg.wait_for_timeout(200)
    ck('buy burner: $40, spare, picture pops after',J("()=>S.cash===2960&&w4().burn>=1&&/Old texts gone/.test(document.getElementById('modal').innerText)"))
    J("()=>document.getElementById('bk59').click()");pg.wait_for_timeout(200)
    ck('back to the mall, swap available',J("()=>!document.querySelector('#mcard [data-b59=\"swap\"]').disabled"))
    J("()=>{document.getElementById('modal').hidden=true;S.at=placeAt('store');openPlace('store')}")
    ck('corner store no longer sells burners',J("()=>!/Burner phone/.test(document.querySelector('#mcard').innerText)"))
    J("()=>{document.getElementById('modal').hidden=true;tab='phone';window._rph='turf';render()}");pg.wait_for_timeout(300)
    J("()=>{const m=document.querySelector('.phx .mapb[data-a=\"go\"]');m.dispatchEvent(new MouseEvent('click',{bubbles:true}))}");pg.wait_for_timeout(200)
    ck('phone Maps: tapping a block only offers a ride',J("()=>!!document.getElementById('rd59')&&!document.querySelector('#mcard [data-g58]')"))
    ck('Licks + Burners apps gone from the phone',J("()=>{document.getElementById('modal').hidden=true;window._rph=null;render();return !document.querySelector('.ph-home [data-rph=\"licks\"],.ph-home [data-rph=\"burners\"]')}"))
    ck('no errors',not errs,json.dumps(errs[:3]))
    b.close()
print(sum(res),'/',len(res))
