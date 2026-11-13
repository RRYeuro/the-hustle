import sys,json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append((n,bool(c)));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':420,'height':860});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:200]) if m.type=='error' and 'sk31' in m.text else None)
    pg.goto('file:///home/claude/the-hustle/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S.cash=20000;S.clean=5000;S.heat=10;S.rep=80;S.at=0;S.known=[0,1,2];S.trust[0]=60;S.trust[1]=60;S.trust[2]=30;S.cap=900;tab='block';render()}")
    r=J("()=>[...document.querySelectorAll('[data-a31=\"pu\"]')].map(b=>b.dataset.i+':'+(b.disabled?'off':'on'))")
    ck('block tab lists other plugs',r==['1:on','2:off'],str(r))
    p0=J("()=>plugPrice('buy',G(PINFO[1].carries[0]))");d0=J("()=>S.day")
    pg.locator('[data-a31][data-i="1"]').click();pg.wait_for_timeout(300)
    r=J("()=>({meet:S.meet,at:S.at,ov:!!document.getElementById('mt31'),buy:document.querySelectorAll('#mt31 [data-a=\"buy\"]:not([disabled])').length,day:S.day,t:document.querySelector('#mt31 .mt31h').innerText})")
    ck('pull up opens the meet',r['ov'] and r['at']==1 and r['meet']['from']==0 and r['buy']>0 and r['day']==d0,json.dumps(r))
    # delivery tax: compare against the same price with the meet off
    r2=J("()=>{const g=G(PINFO[1].carries[0]);const a=plugPrice('buy',g);const M=S.meet;delete S.meet;const b=plugPrice('buy',g);S.meet=M;return [a,b]}")
    ck('delivery costs 8% more',abs(r2[0]-round(r2[1]*1.08))<=1,str(r2))
    # buy through the real buy flow
    inv0=J("()=>GOODS.reduce((a,g)=>a+S.inv[g.id],0)");c0=J("()=>S.cash")
    pg.locator('#mt31 [data-a="buy"]:not([disabled])').first.click();pg.wait_for_timeout(400)
    ck('buy popup opens over the meet',J("()=>!document.getElementById('modal').hidden"),'')
    t=J("()=>document.getElementById('mcard').innerText.slice(0,300)")
    # click through: prefer a button that buys
    J("()=>document.getElementById('ok').click()");pg.wait_for_timeout(400);J("()=>{const b=document.getElementById('bmno');if(b)b.click()}");pg.wait_for_timeout(300)
    r=J("()=>({inv:GOODS.reduce((a,g)=>a+S.inv[g.id],0),cash:S.cash,at:S.at,ov:!!document.getElementById('mt31'),hid:document.getElementById('modal').hidden})")
    ck('bought from the plug during the meet',r['inv']>inv0 and r['cash']<c0 and r['at']==1 and r['ov'],json.dumps(r)+' | '+t)
    pg.locator('#mt31x').click();pg.wait_for_timeout(200)
    r=J("()=>({at:S.at,meet:S.meet||null,ov:!!document.getElementById('mt31'),day:S.day,again:[...document.querySelectorAll('[data-a31][data-i=\"1\"]')].map(b=>b.disabled)})")
    ck('done: back on your block, no day passed, once a day',r['at']==0 and r['meet'] is None and not r['ov'] and r['day']==d0 and r['again']==[True],json.dumps(r))
    # too hot
    J("()=>{S.pk[1].pu=-9;S.heat=80;render()}");ck('too hot: no pull up',J("()=>document.querySelector('[data-a31][data-i=\"1\"]').disabled"))
    # next day ends a meet
    J("()=>{S.heat=10;l31PullUp(1);nextDay();render()}");r=J("()=>({at:S.at,meet:S.meet||null,ov:!!document.getElementById('mt31')})")
    ck('next day ends the meet',r['at']==0 and r['meet'] is None and not r['ov'],json.dumps(r));J("()=>{document.getElementById('modal').hidden=true}")
    # call popup
    J("()=>{S.pk[1].pu=-9;l31Call(1,true)}");ck('call popup',J("()=>/is calling/.test(document.querySelector('#mcard h2').textContent)&&!!document.getElementById('c31a')"))
    r=J("()=>Object.values(S.offer[1]).filter(o=>o.tip).length");ck('call sets a one-day deal',r>=1,str(r))
    J("()=>document.getElementById('c31a').click()");pg.wait_for_timeout(200);ck('call: pull up on me works',J("()=>!!S.meet&&S.at===1"))
    J("()=>{try{busted()}catch(e){window._be=String(e)}}");ck('bust ends the meet',J("()=>!S.meet&&!window._be"),J("()=>window._be"))
    J("()=>{document.getElementById('modal').hidden=true;S.pr=null;S.over=false;devPanel()}");ck('dev buttons',J("()=>document.querySelectorAll('[data-d31]').length")==4)
    ck('tutorial entry',J("()=>TUT.some(t=>/Plugs call/.test(t[0]))"))
    b.close()
bad=[n for n,c in res if not c];print('ERRORS',errs[:6]);print(f'{len(res)-len(bad)}/{len(res)} passed')
