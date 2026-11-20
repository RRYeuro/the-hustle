from playwright.sync_api import sync_playwright
res=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':420,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
    pg.goto('file:///home/claude/the-hustle/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.FF=false;S.age=19;S.cal=0;S.school='out';S.car=null;S.en=enMax();S.at=0;render()}")
    d0=J("()=>S.day");J("()=>{S.bus=0;act('go',{dataset:{i:'2'}})}")
    ck('no pass: move costs the day',J("()=>S.day")>d0)
    J("()=>{document.getElementById('modal').hidden=true;S.at=0;S.en=enMax();S.bus=S.day+10}")
    d1=J("()=>S.day");e1=J("()=>S.en");J("()=>act('go',{dataset:{i:'2'}})")
    ck('pass: same day',J("()=>S.day")==d1,J("()=>S.day"))
    ck('pass: 3 energy',J("()=>S.en")==e1-3,J("()=>S.en"))
    ck('pass: moved',J("()=>S.at")==2)
    J("()=>{S.en=2;S.at=0;document.getElementById('modal').hidden=true}");d2=J("()=>S.day");J("()=>act('go',{dataset:{i:'1'}})")
    ck('too tired: walks, costs day',J("()=>S.day")>d2)
    ck('no page errors',not errs,errs[:2])
print('%d/%d'%(sum(res),len(res)))
