from playwright.sync_api import sync_playwright
ok=0;n=0
def chk(c,m):
    global ok,n;n+=1;ok+=bool(c);print(('PASS ' if c else 'FAIL ')+m)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.goto('http://127.0.0.1:8765/index.html');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;S.age=20;S.cash=90000}")
    chk(J("()=>wMax()")==3,'3 with no traps')
    J("()=>{for(let i=0;i<4;i++){S.owner[i]='me';S.traps[i]={w:null,bought:S.day,stock:{},cash:0}}}")
    chk(J("()=>wMax()")==7,'7 with 4 traps')
    J("()=>{S.workers=[];for(let i=0;i<4;i++)S.workers.push({id:'x'+i,name:'W'+i,sales:0,pct:100});S.at=0;freshCands&&freshCands()}")
    J("()=>l61open()");pg.wait_for_timeout(150)
    hire=J("()=>[...document.querySelectorAll('[data-a=hirew]')].map(b=>!b.disabled)")
    chk(any(hire),'can hire a 5th worker with 4 traps')
    chk(not errs,'no errors '+';'.join(errs[:2]));print(ok,'/',n);b.close()
