import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;S.age=19;S._evDay=S.day;S.picQ=[];S.cash=1000;S.clean=1000;S.safe=0;S.heat=0}")
    run="()=>{WD.forEach(f=>{try{if(/l53\\(\\)/.test(String(f)))f()}catch(e){}})}"
    J(run);ck('small money: no attention',J("()=>S.heat")==0)
    J("()=>{S.cash=17000;S.clean=1000;S.heat=0}");J(run)
    r=J("()=>({h:S.heat,a:l53(),q:(S.picQ||[]).map(x=>x.h)})");ck('$16k street money: watched, +2 (+base) heat, popup',r['a']['t']==2 and r['h']==4 and r['q']==['👀 Watched'],json.dumps(r))
    J("()=>{S.picQ=[];S.heat=0}");J(run);ck('popup only the first time',J("()=>(S.picQ||[]).length")==0)
    J("()=>{S.clean=9000;S.cash=25000;S.heat=0}");J(run);ck('clean money covering half takes 1 off',J("()=>S.heat")==3)
    ck('Money tab shows the attention row','👀' in J("()=>paneExp()"))
    J("()=>{S.cash=150000;S.clean=0;S.heat=0;S.picQ=[]}");J(run);ck('$150k: federal file',J("()=>l53().t===4&&S.heat===7"))
    ck('no errors',not errs,json.dumps(errs[:3]))
    b.close()
print(sum(res),'/',len(res))
