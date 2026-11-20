import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:200]) if m.type=='error' and 'sk4' in m.text else None)
    pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S.cash=5000;S.heat=10;S.en=100;S._evDay=S.day;render()}");pg.wait_for_timeout(800)
    ks=['g_copstop','g_search','g_jewel','g_trunk','g_safe','g_alarm','g_pharm','g_phone','g_hplan','g_hsend','g_hpay','g_hsetup','g_scan1','g_patrol','g_tipoff','g_raidup','cp_miami','cp_losangeles']
    r=J("""async(ks)=>{const bad=[];for(const k of ks){const u=ARTX(k);if(!u){bad.push(k+':none');continue}const ok=await new Promise(r=>{const i=new Image();i.onload=()=>r(i.naturalWidth>0);i.onerror=()=>r(false);i.src=u});if(!ok)bad.push(k)}return bad}""",ks)
    ck('all 18 new pictures load',r==[],json.dumps(r))
    ck('planner shows the plan picture',J("()=>{l35Plan('jewel');return !!document.querySelector('#mcard img[src*=\"'+ARTX('g_hplan')+'\"]')}"))
    J("()=>{document.getElementById('modal').hidden=true;S.scanD=-1;Math._r=Math.random;Math.random=()=>0.01;S.scan=1;raid();Math.random=Math._r}")
    ck('scanner tip-off has its picture',J("()=>!!document.querySelector('#mcard img[src*=\"'+ARTX('g_tipoff')+'\"]')&&/scanner went off/.test(document.querySelector('#mcard').textContent)"))
    J("()=>{document.getElementById('modal').hidden=true;S.picQ=[];b5().crack=S.day+5;render()}");pg.wait_for_timeout(800)
    ck('task force popup with picture',J("()=>/Task force/.test(document.querySelector('#mcard h2').textContent)&&!!document.querySelector('#mcard img[src*=\"'+ARTX('g_raidup')+'\"]')"))
    J("()=>document.getElementById('ok42').click()");ck('OK closes it and it does not come back',J("()=>{render();return document.getElementById('modal').hidden&&!S.picQ.length}"))
    J("()=>{S.patSaid=S.day;render()}");pg.wait_for_timeout(800);ck('first patrol popup once',J("()=>/Patrol/.test(document.querySelector('#mcard h2').textContent)"))
    J("()=>document.getElementById('ok42').click()");J("()=>{S.patSaid=S.day;render()}");pg.wait_for_timeout(800);ck('patrol popup only the first time',J("()=>document.getElementById('modal').hidden"))
    # crew heist result via cmResolve (the real day path)
    SET="""()=>{startLife('lucky');const M0=document.getElementById('modal');M0.hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S.robOn=1;S.soldiers=4;S.cash=5000;S.clean=1000;S.heat=0;S.en=100;S.day=31;
          const M=crewList();M.forEach((m,i)=>{m.busy=null;m.hurt=0;m.loy=70;m.snake=0;m.rank=i===1?'rh':'sol';m.sk.drive=i===1?8:2;m.sk.look=i===2?8:2;m.sk.scam=i===0?8:i===3?5:2});S.rob.mask=1;S.rob.car=1;S.rob.hd=null;S.rob.fat=0;S.hc=null;S.hcase={};tab='rob';render()}"""
    J(SET);J("()=>{S.picQ=[];l35Plan('truck')}");J("()=>document.querySelector('[data-h35=\"send\"]').click()")
    r=J("()=>{document.getElementById('modal').hidden=true;S.picQ=[];Math._r=Math.random;Math.random=()=>0.01;const M=S.hc.ids.map(i=>crewList().find(m=>m.id===i));M.forEach(m=>m.busy.until=S.day);cmResolve(M[0]);Math.random=Math._r;return {q:(S.picQ||[]).map(x=>x.k+'|'+x.h),hc:S.hc}}")
    ck('crew heist result queues payday or setup picture',r['hc'] is None and len(r['q'])==1 and r['q'][0].split('|')[0] in ('g_hpay','g_hsetup'),json.dumps(r))
    J("()=>{render()}");pg.wait_for_timeout(800);ck('result popup shows with picture',J("()=>!!document.getElementById('ok42')"))
    J("()=>document.getElementById('ok42').click()")
    J("()=>{S.picQ=[];document.getElementById('modal').hidden=true;devPanel()}");ck('dev buttons',J("()=>document.querySelectorAll('[data-d42]').length")==5)
    J("()=>document.querySelector('[data-d42=\"pay\"]').click()");pg.wait_for_timeout(800);ck('dev payday shows picture',J("()=>!!document.querySelector('#mcard img[src*=\"'+ARTX('g_hpay')+'\"]')"))
    pg.screenshot(path='/tmp/claude-0/s42/pop.png')
    J("()=>document.getElementById('ok42').click()")
    J("()=>{S.loot=[{k:'chain',d:S.day-9}];S.at=placeAt('pawn');openPlace('pawn')}")
    ck('jewelry picture at the pawn shop',J("()=>!!document.querySelector('#mcard .p42j img')"),J("()=>document.querySelector('#mcard').textContent.slice(0,200)"))
    ck('no errors',not errs,json.dumps(errs[:5]))
    b.close()
print(sum(res),'/',len(res))
