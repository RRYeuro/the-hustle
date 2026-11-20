import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1280,'height':900});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S.cash=500;S.en=60;S.car=null;S._evDay=S.day;S.picQ=[];S.fd=null;S.at=0;tab='move';render()}");pg.wait_for_timeout(300)
    d0=J("()=>S.day")
    J("()=>{document.querySelector('#pane button[data-a=\"go\"][data-i=\"2\"]').click()}");pg.wait_for_timeout(200)
    ck('tapping a block asks first, nothing happens yet',J("()=>/Go to/.test(document.querySelector('#mcard h2').textContent)&&S.at===0"))
    ck('no car: ride, bus, walk choices',J("()=>document.querySelectorAll('#mcard [data-g58]').length")==3)
    J("()=>document.getElementById('no58').click()");ck('Stay here: no move, no day lost',J("(d)=>S.at===0&&S.day===d",d0))
    J("()=>{l58Go(2)}");J("()=>{[...document.querySelectorAll('#mcard .row')].find(r=>/Ride/.test(r.textContent)).querySelector('button').click()}");pg.wait_for_timeout(300)
    ck('Ride: moved, $25, no day lost',J("(d)=>S.at===2&&S.day===d&&S.cash<=475",d0),J("()=>({at:S.at,c:S.cash,d:S.day})"))
    J("()=>{document.getElementById('modal').hidden=true;S.car=Object.keys(CARS).find(k=>k!=='stolen');l58Go(1)}")
    ck('with a car: Drive shows first, no Walk',J("()=>{const t=[...document.querySelectorAll('#mcard .row .t')].map(x=>x.textContent);return /Drive/.test(t[0])&&!t.some(x=>/Walk/.test(x))}"))
    J("()=>{document.querySelector('#mcard [data-g58=\"0\"]').click()}");pg.wait_for_timeout(200)
    ck('Drive: moved, no day lost',J("(d)=>S.at===1&&S.day===d",d0))
    J("()=>{document.getElementById('modal').hidden=true;S.car=null;const id=PLACES.find(p=>placeAt(p.id)!==S.at&&p.id!=='studio').id;window._pid=id;openPlace(id)}")
    ck('place on another block uses the same chooser',J("()=>/Go to/.test(document.querySelector('#mcard h2').textContent)"))
    ck('no errors',not errs,json.dumps(errs[:3]))
    b.close()
print(sum(res),'/',len(res))
