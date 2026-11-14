import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:200]) if m.type=='error' and 'sk4' in m.text else None)
    pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S.cash=5000;S._evDay=S.day;S.picQ=[];S.friends=[];render()}")
    ck('no runners handed out, even at Petty Dealer',J("()=>{S.lvl=3;addXP(1);return w5bDealers().length===0}"))
    J("()=>{try{weekTick=()=>true}catch(e){};const B=b5();B.ord=[];B.oweek=-9;w5bOrderDay()}");ck('no runners = no orders',J("()=>b5().ord.length===0"))
    h=J("()=>w5bOrders()");ck('phone shows Your runners 0/1',('Your runners (0/1)' in h),h[:200])
    J("()=>{S.friends=[{name:'Kash',trait:'loyal',role:'none',close:30},{name:'Bean',trait:'loyal',role:'none',close:60}]}")
    h=J("()=>w5bOrders()");ck('friend under 40 close cannot be put on','need 40' in h)
    J("()=>{document.getElementById('pane').innerHTML=w5bOrders();document.querySelector('[data-a49=\"put\"][data-i=\"1\"]').click()}")
    ck('put Bean on: runner + text',J("()=>b5().dl.length===1&&b5().dl[0].n==='Bean'&&S.inbox[0].f==='Bean'"))
    ck('limit 1 runner at Petty Dealer',J("()=>{S.friends[0].close=60;return !w5bOrders().includes('data-a49=\"put\" data-i=\"0\" ')||w5bOrders().includes('disabled>Put on')}"))
    J("()=>{const B=b5();B.ord=[];B.oweek=-9;w5bOrderDay()}");r=J("()=>b5().ord.map(o=>[o.d,o.n])");ck('orders come from your runner only',len(r)==1 and r[0][0]==0,json.dumps(r))
    J("()=>{document.getElementById('pane').innerHTML=w5bOrders();document.querySelector('[data-a49=\"cut\"]').click()}");ck('cut off removes runner and its orders',J("()=>b5().dl.length===0&&b5().ord.length===0"))
    # school lunch
    J("()=>{S.age=15;S.school='in';S.classDay=S.day;S.lunch49=-1;S.friends=[]}")
    h=J("()=>paneSchool()");ck('school has Lunch button',('Sit with new people' in h))
    J("()=>{Math._r=Math.random;Math.random=()=>0.9;document.getElementById('pane').innerHTML=paneSchool();document.querySelector('[data-a49=\"lunch\"]').click();Math.random=Math._r}")
    t=J("()=>document.getElementById('modal').hidden?'':document.getElementById('mcard').textContent")
    ck('meet a classmate at lunch',('at lunch' in t) and ('New face' in t),t[:200])
    J("()=>document.getElementById('y').click()");ck('classmate added as friend, from school',J("()=>S.friends.length===1&&S.friends[0].sch===1"))
    ck('lunch once a day',J("()=>paneSchool().includes('Ate today')"))
    J("()=>{S.age=19;document.getElementById('modal').hidden=true;devPanel()}");ck('dev buttons',J("()=>document.querySelectorAll('[data-d49]').length")==2)
    ck('no errors',not errs,json.dumps(errs[:5]))
    b.close()
print(sum(res),'/',len(res))
