import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1280,'height':900});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;S.age=19;S.cash=1000;S._evDay=S.day;S.picQ=[];S.inbox=[];w4Text('rent');tab='phone';window._rph='messages';window._mth='Mama';render()}");pg.wait_for_timeout(300)
    ck('Mama thread offers real answers',J("()=>/I got you \\(\\$200\\)/.test(document.querySelector('.mth-kb').innerText)"),J("()=>document.querySelector('.mth-kb').innerText"))
    J("()=>document.querySelector('[data-w4r=\"rent:y\"]').click()");pg.wait_for_timeout(1300)
    r=J("()=>({c:S.cash,a:S.inbox[0],b:S.inbox[1]})")
    ck('send $200: money goes, you text, Mama thanks you',r['c']==800 and r['a']['f']=='Mama' and 'love' in r['a']['t'] and r['b']['f']=='You',json.dumps(r))
    ck('no errors',not errs,json.dumps(errs[:3]))
    b.close()
print(sum(res),'/',len(res))
