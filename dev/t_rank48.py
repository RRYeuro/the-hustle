import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:200]) if m.type=='error' and 'sk4' in m.text else None)
    pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S.cash=5000;S._evDay=S.day;S.picQ=[];render()}")
    ck('fresh start: no Big plug known',J("()=>!S.known.some(i=>PINFO[i].lvl==='Big')"),J("()=>JSON.stringify(S.known.map(i=>PINFO[i].lvl))"))
    r=J("()=>{const B=b5();B.ord=[];B.oweek=-9;window.weekTick0=window.weekTick;S.lvl=1;S.rk=0;try{weekTick=()=>true}catch(e){};w5bOrderDay();return (B.ord||[]).length}")
    ck('Corner Boy: no runner orders',r==0,str(r))
    r=J("()=>{const B=b5();B.ord=[];B.oweek=-9;S.lvl=3;addXP(1);w5bOrderDay();return B.ord.map(o=>[o.g,o.n,w5bUnit(G(o.g))])}")
    ck('Petty Dealer: small orders (quarter unit)',len(r)>0 and all(x[1]==max(1,int(x[2]*.25+.5)) for x in r),json.dumps(r))
    r=J("()=>{const B=b5();B.ord=[];B.oweek=-9;S.lvl=20;addXP(1);w5bOrderDay();return B.ord.map(o=>o.n/w5bUnit(G(o.g)))}")
    ck('Kingpin: up to 3 units',len(r)>0 and all(x in (1,2,3) for x in r),json.dumps(r))
    r=J("()=>{S.lvl=1;S.rk=0;S.xp=0;S.log=[];const big=PINFO.map((p,i)=>i).find(i=>PINFO[i].lvl==='Big'&&!S.known.includes(i));document.getElementById('modal').hidden=true;l31Intro(big);return (S.log[0]||{}).t||''}")
    ck('Big plug locked until Middle Man',r and 'Middle Man' in r,str(r))
    r=J("()=>{S.lvl=6;addXP(1);S.log=[];const big=PINFO.map((p,i)=>i).find(i=>PINFO[i].lvl==='Big'&&!S.known.includes(i));document.getElementById('modal').hidden=true;l31Intro(big);return (S.log[0]||{}).t||''}")
    ck('Middle Man: Big plug lock gone',not r or 'Middle Man' not in r,str(r))
    ck('rank-up marks NEW',J("()=>S.rk48i>=2&&S.rk48d===S.day"))
    h=J("()=>paneCrew()");ck('Me tab shows the ladder with locks',('rl48' in h) and ('🔒' in h) and ('NEW' in h))
    J("()=>{document.getElementById('modal').hidden=true;S.lvl=9;S.xp=0;S.rankPop=null;addXP(S.lvl*20);try{missionUI()}catch(e){}}");pg.wait_for_timeout(300)
    t=J("()=>document.getElementById('modal').hidden?'':document.getElementById('mcard').textContent")
    ck('rank-up popup lists what unlocked',('Unlocked' in t) and ('Supplier' in t),t[:200])
    J("()=>{document.getElementById('modal').hidden=true;devPanel()}");ck('dev buttons',J("()=>document.querySelectorAll('[data-d48]').length")==6)
    ck('no errors',not errs,json.dumps(errs[:5]))
    b.close()
print(sum(res),'/',len(res))
