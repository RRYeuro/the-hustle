import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1280,'height':900});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:200]) if m.type=='error' and 'sk36' in m.text else None)
    pg.goto('file:///home/claude/the-hustle/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S.cash=2000;S.clean=500;S.heat=10;S.en=100;S.scan=0;tab='move';render()}")
    r=J("()=>{const o={};[[0,1],[45,2],[80,3]].forEach(([h,n])=>{S.heat=h;S.pat=null;o[h]=l36Pat().length});S.heat=10;S.pat=null;return o}")
    ck('patrol count grows with heat (1, 2, 3)',r=={'0':1,'45':2,'80':3},json.dumps(r))
    ck('same patrols all day',J("()=>{const a=l36Pat().join();render();return a===l36Pat().join()}"))
    ck('no scanner: hint only, no patrol list',J("()=>/police scanner from the pawn shop/.test(document.getElementById('pane').textContent)&&!/Police scanner · today/.test(document.getElementById('pane').textContent)"))
    # buy at pawn
    J("()=>{S.age=15;S.at=placeAt('pawn');openPlace('pawn')}");ck('under 16 cannot buy',J("()=>document.querySelector('#mcard [data-a36]').disabled"))
    J("()=>{document.getElementById('modal').hidden=true;S.age=19;openPlace('pawn')}")
    c0=J("()=>S.cash");J("()=>document.querySelector('#mcard [data-a36]').click()");pg.wait_for_timeout(300)
    r=J("(c)=>({scan:S.scan,paid:c-S.cash,clean:cleanCash(),tab:tab,list:/Police scanner · today/.test(document.getElementById('pane').textContent)})",c0)
    ck('buy: $350 dirty first, scanner on, Move shows the list',r['scan']==1 and r['paid']==350 and r['clean']==500 and r['tab']=='move' and r['list'],json.dumps(r))
    J("()=>{S.pat={d:S.day,c:'home',b:[2,4]};S.city=null;S.pat.c=(typeof W5BCITY!=='undefined'&&S.city!=null)?String(S.city):'home';render()}")
    r=J("()=>({cop:[...document.querySelectorAll('#pane .row .t')].filter(x=>/🚓/.test(x.textContent)).map(x=>x.textContent.replace('🚓','').trim().slice(0,12)),map:document.querySelectorAll('#fm26 .pat36').length})")
    ck('scanner marks the patrolled blocks and the map',len(r['cop'])==2 and r['map']==2,json.dumps(r))
    # effects
    J("()=>{S.at=2;S.heat=10;S.lh={};srvTick(10,G('loud'))}");r=J("()=>({heat:S.heat,lh:S.lh[2]})")
    ck('serving on a patrolled block: +2 heat',r['heat']==12,json.dumps(r))
    J("()=>{S.at=1;S.heat=10;srvTick(10,G('loud'))}");ck('not patrolled: no extra heat',J("()=>S.heat")==10)
    J("()=>{S.at=2;S.heat=10;S.rob.c0=null;lickDone('t','x',true,true)}");J("()=>{document.getElementById('modal').hidden=true;S.heat=10;lickDone('t','x',true)}")
    ck('lick on a patrolled block: +4 heat',J("()=>S.heat")>=14,str(J("()=>S.heat")))
    J("()=>{document.getElementById('modal').hidden=true}")
    # events
    J("()=>{b5().fc={t:'crack',at:S.day+2};S.heat=75;tab='move';render()}")
    t=J("()=>document.getElementById('pane').textContent")
    ck('events: task force forecast and radio warning',('task force sweep in 2 days' in t) and ('radio' in t),t[:200])
    # raid tip
    J("()=>{S.scanD=-1;Math._r=Math.random;Math.random=()=>0.01;raid();Math.random=Math._r}")
    ck('scanner can tip you off before a raid',J("()=>/scanner went off/.test(document.querySelector('#mcard h2').textContent)"))
    J("()=>{document.getElementById('modal').hidden=true;devPanel()}");ck('dev buttons',J("()=>document.querySelectorAll('[data-d36]').length")==4)
    ck('tutorial entry',J("()=>TUT.some(t=>/Police scanner/.test(t[0]))"))
    b.close()
print('ERR',errs[:5]);print(sum(res),'/',len(res))
