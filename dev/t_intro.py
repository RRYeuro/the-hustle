import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':420,'height':860});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.goto('file:///home/claude/the-hustle/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S.cash=5000;S.clean=1000;S.heat=10;S.rep=0;S.at=0;S.known=[0];S.trust[0]=30;S.friends=[];S.crewM=[];S.soldiers=0;S.en=100;tab='move';render()}")
    r=J("()=>[...document.querySelectorAll('[data-a31=\"in\"]')].map(b=>b.dataset.i+':'+(b.disabled?'off':'on')+':'+PINFO[b.dataset.i].lvl)")
    ck('strangers listed, locked with nobody to vouch',len(r)==5 and all(':off:' in x for x in r),str(r))
    J("()=>{S.trust[0]=65;render()}")
    r=J("()=>[...document.querySelectorAll('[data-a31=\"in\"]')].map(b=>b.dataset.i+':'+(b.disabled?'off':'on')+':'+PINFO[b.dataset.i].lvl)")
    ck('a trusted plug can vouch',all(':on:' in x for x in r),str(r))
    low=[x.split(':')[0] for x in r if x.endswith('Low')];mid=[x.split(':')[0] for x in r if not x.endswith('Low')]
    c0=J("()=>S.cash");d0=J("()=>S.day")
    if low:
        J("(i)=>document.querySelector('#pane [data-a31=\"in\"][data-i=\"'+i+'\"]').click()",low[0]);pg.wait_for_timeout(200)
        ck('link-up popup',J("()=>/Meet /.test(document.querySelector('#mcard h2').textContent)"))
        J("()=>document.getElementById('i31a').click()");pg.wait_for_timeout(300)
        rr=J("(i)=>({kn:S.known.includes(+i),tr:S.trust[i],cash:S.cash,clean:cleanCash(),day:S.day,h:document.querySelector('#mcard h2').textContent})",low[0])
        ck('low plug: in after paying, dirty cash, no day',rr['kn'] and rr['tr']>=20 and rr['cash']==c0-100 and rr['day']==d0,json.dumps(rr))
        J("()=>document.getElementById('ok').click()")
        ck('one link-up a day',J("()=>[...document.querySelectorAll('[data-a31=\"in\"]')].every(b=>b.disabled)"))
    J("()=>{S.introD=-9;pokerGame=(o,cb)=>cb(false);tab='move';render()}")
    J("(i)=>document.querySelector('#pane [data-a31=\"in\"][data-i=\"'+i+'\"]').click()",mid[0]);pg.wait_for_timeout(200);J("()=>document.getElementById('i31a').click()");pg.wait_for_timeout(300)
    rr=J("(i)=>({kn:S.known.includes(+i),cold:S.pk[i].cold-S.day,h:document.querySelector('#mcard h2').textContent})",mid[0])
    ck('mid plug: fail = cold 4 days',(not rr['kn']) and rr['cold']==4 and 'Not feeling' in rr['h'],json.dumps(rr));J("()=>document.getElementById('ok').click()")
    J("()=>{S.introD=-9;pokerGame=(o,cb)=>cb(true);tab='move';render()}")
    J("(i)=>document.querySelector('#pane [data-a31=\"in\"][data-i=\"'+i+'\"]').click()",mid[1]);pg.wait_for_timeout(200);J("()=>document.getElementById('i31a').click()");pg.wait_for_timeout(300)
    ck('mid plug: win = known',J("(i)=>S.known.includes(+i)",mid[1]));J("()=>document.getElementById('ok').click()")
    # balance + dup
    ck('wanted board under gun price',J("()=>{S.pawnW=null;const W=pawnWant();return W.price<GUNS[W.k].cost}"))
    ck('business payback about 23 days',J("()=>['barber','wash','laundry','club'].every(k=>BIZ[k].cost/BIZ[k].pay<25)"))
    J("()=>{S.soldiers=2;S.cwSeen=0;S.cash=500;WD.find(f=>f.name==='crewWarn')();window._w1=S.log[0].t;S.cwD=-9;WD.find(f=>f.name==='crewWarn')();window._w2=S.log[0].t}")
    ck('crew cost warning',J("()=>/crew costs/.test(window._w1)&&/only cover/.test(window._w2)"),J("()=>window._w1+' | '+window._w2"))
    J("()=>{S.soldiers=0;S.robOn=1;S.at=homeBlock();tab='rob';render()}")
    ck('licks not in Heists',J("()=>!/Licks · each one/.test(document.getElementById('pane').textContent)"))
    J("()=>{tab='move';render()}");ck('nap only once',J("()=>document.querySelectorAll('#pane [data-a=\"nap\"]').length")==0,str(J("()=>document.querySelectorAll('#pane [data-a=\"nap\"]').length")))
    b.close()
print('ERR',errs[:5]);print(sum(res),'/',len(res))
