import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':420,'height':860});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:200]) if m.type=='error' and 'sk35' in m.text else None)
    pg.goto('file:///home/claude/the-hustle/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    SET="""()=>{startLife('lucky');const M0=document.getElementById('modal');M0.hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S.robOn=1;S.soldiers=4;S.cash=5000;S.clean=1000;S.heat=0;S.en=100;S.day=31;
      const M=crewList();M.forEach((m,i)=>{m.busy=null;m.hurt=0;m.loy=70;m.snake=0;m.rank=i===1?'rh':'sol';m.sk.drive=i===1?8:2;m.sk.look=i===2?8:2;m.sk.scam=i===0?8:i===3?5:2});S.rob.mask=1;S.rob.car=1;S.rob.hd=null;S.rob.fat=0;S.hc=null;S.hcase={};tab='rob';render()}"""
    J(SET)
    J("()=>document.querySelector('#pane [data-a=\"heist\"][data-k=\"bank\"]').click()");pg.wait_for_timeout(200)
    r=J("()=>({open:!!document.getElementById('hc35'),roles:[...document.querySelectorAll('#mcard .row .t')].map(x=>x.textContent).slice(0,3)})")
    ck('plan opens with roles picked by skill',r['open'] and 'Driver' in r['roles'][0] and 'Lookout' in r['roles'][1] and 'Inside' in r['roles'][2],json.dumps(r))
    ids=J("()=>{const M=crewList();return {drive:M[1].name,look:M[2].name,inside:M[0].name}}")
    ck('best members on each role',ids['drive'] in r['roles'][0] and ids['look'] in r['roles'][1] and ids['inside'] in r['roles'][2],json.dumps([ids,r['roles']]))
    pg.keyboard.press('1');pg.wait_for_timeout(100)
    r2=J("()=>document.querySelector('#mcard .row .t').textContent")
    ck('key 1 swaps the driver',ids['drive'] not in r2,r2)
    pg.keyboard.press('1');pg.keyboard.press('1');pg.wait_for_timeout(100)
    # case it (takes the day)
    d0=J("()=>S.day");pg.keyboard.press('c');pg.wait_for_timeout(300)
    r=J("(d)=>({dd:S.day-d,cased:S.hcase.bank>=S.day,open:!!document.getElementById('hc35')})",d0)
    ck('case it: takes the day, +odds for 3 days',r['dd']==1 and r['cased'],json.dumps(r))
    J("()=>{S.rob.hd=null;S.rob.fat=0;render();l35Plan('bank')}")
    # run it yourself: forced win, check cut & clean
    c0=J("()=>S.cash");J("()=>{Math._r=Math.random;Math.random=()=>0.01}")
    J("()=>document.querySelector('[data-h35=\"run\"]').click()");pg.wait_for_timeout(200)
    ck('run goes to the existing quiet/loud heist',J("()=>!!document.getElementById('ld')"))
    J("()=>document.getElementById('ld').click()");pg.wait_for_timeout(300);J("()=>{Math.random=Math._r}")
    r=J("()=>({cash:S.cash,clean:cleanCash(),log:S.log.slice(0,8).map(x=>x.t),loy:crewList().map(m=>m.loy),cased:S.hcase.bank})")
    import re
    m=re.search(r'\$([\d,]+) total, \$([\d,]+) to the crew',' '.join(r['log']))
    ok=m and abs(int(m.group(2).replace(',',''))-round(int(m.group(1).replace(',',''))*0.45))<=2
    ck('run: crew cut = split x 3 on the job (45% fair), money dirty',ok and r['cash']>c0 and r['clean']==1000,json.dumps(r))
    ck('run: fair split +1 loyalty on the job only, case used up',sorted(r['loy'])==[70,71,71,71] and r['cased'] is None,json.dumps(r))
    J("()=>{document.getElementById('modal').hidden=true}")
    # send the crew
    J(SET);J("()=>l35Plan('truck')")
    ck('send allowed with a Right Hand',J("()=>!document.querySelector('[data-h35=\"send\"]').disabled"))
    J("()=>{crewList()[1].rank='sol';l35Plan('truck')}")
    ck('send locked without a Right Hand or Captain',J("()=>document.querySelector('[data-h35=\"send\"]').disabled"))
    J("()=>{crewList()[1].rank='rh';S.day=10;l35Plan('bank')}")
    ck('bank send locked before day 30',J("()=>document.querySelector('[data-h35=\"send\"]').disabled&&/day 30/.test(document.getElementById('mcard').textContent)"))
    J("()=>{S.day=31;l35Plan('truck')}");pg.keyboard.press('s');pg.wait_for_timeout(200)
    r=J("()=>({hc:!!S.hc,busy:crewList().filter(m=>m.busy&&/^heist:/.test(m.busy.r)).map(m=>m.busy.until-S.day),hd:S.rob.hd===S.day})")
    ck('S sends: 2 members busy 3 days, streets hot',r['hc'] and r['busy']==[3,3] and r['hd'],json.dumps(r))
    J("()=>{l35Plan('jewel')}");ck('cannot plan another while crew is out',J("()=>document.querySelector('[data-h35=\"run\"]').disabled"))
    J("()=>{document.getElementById('modal').hidden=true}")
    c0=J("()=>S.cash");J("()=>{nextDay();nextDay();window._still=!!S.hc;S.hc.ids.map(i=>crewList().find(m=>m.id===i)).forEach(m=>m.busy.until=S.day);Math._r=Math.random;Math.random=()=>0.01;l35Resolve();Math.random=Math._r}");pg.wait_for_timeout(200)
    ck('crew still out after 2 days',J("()=>window._still"))
    r=J("(c)=>({hc:S.hc,gain:S.cash-c,clean:cleanCash(),busy:crewList().filter(m=>m.busy).length,heists:S.rob.heists,msg:(S.inbox||[]).slice(0,2).map(x=>x.t).join(' | ')+' || '+S.log.slice(0,6).map(x=>x.t).join(' | ')})",c0)
    ck('crew comes back after 3 days with dirty money',r['hc'] is None and r['gain']>1000 and r['clean']<=1000 and r['busy']==0,json.dumps(r)[:500])
    J("()=>{document.getElementById('modal').hidden=true}")
    # snitch setup
    J(SET);J("()=>{const M=crewList();M[2].loy=5;l35Plan('truck')}")
    J("()=>{P=null}");J("()=>document.querySelector('[data-h35=\"send\"]').click()")
    J("()=>{Math._r=Math.random;Math.random=()=>0.01;S.hc.ids.map(i=>crewList().find(m=>m.id===i)).forEach(m=>m.busy.until=S.day);l35Resolve();Math.random=Math._r}")
    r=J("()=>({heat:S.heat,hurt:crewList().filter(m=>m.hurt>S.day).length})")
    ck('low loyalty can set the crew up: heat +20, crew picked up',r['heat']>=20 and r['hurt']>=2,json.dumps(r))
    # licks app link
    J(SET);ck('Licks app links to heists',J("()=>/Heists with your crew/.test(paneLicks())"))
    J("()=>{devPanel()}");ck('dev buttons',J("()=>document.querySelectorAll('[data-d35]').length")==5)
    ck('tutorial entry',J("()=>TUT.some(t=>/Heist crew/.test(t[0]))"))
    J("()=>{document.getElementById('modal').hidden=true;S.age=15;l35Plan('jewel')}");ck('under 16 blocked',J("()=>document.querySelector('[data-h35=\"run\"]').disabled"))
    b.close()
print('ERR',errs[:5]);print(sum(res),'/',len(res))
