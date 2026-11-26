from playwright.sync_api import sync_playwright
res=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':420,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
    pg.on('console',lambda m:errs.append('C '+m.text[:160]) if m.type=='error' and 'TUNNEL' not in m.text else None)
    pg.goto('file:///home/claude/the-hustle/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate
    J("""()=>{startLife('tank');document.getElementById('modal').hidden=true;window.FF=false;S.age=19;S.cash=5000;S.clean=1000;S.en=enMax();
     S.workers=[{id:'Dre1',name:'Dre',hustle:5,loyal:5,sales:20,wage:150,held:100,stash:{},sq:{}},{id:'Dre1b',name:'Dre',hustle:4,loyal:8,sales:3,wage:150,held:0,stash:{},sq:{}},{id:'Rosa1',name:'Rosa',hustle:6,loyal:9,sales:25,wage:200,held:0,stash:{},sq:{}}];render()}""")
    # old save: personalities appear without announcements, stable ids
    J("()=>EV.ensureAll()");pers=J("()=>S.workers.map(w=>w.pers)");ck('every worker gets a personality',all(pers),pers)
    ck('two workers named Dre keep separate records',J("()=>S.workers[0].id!==S.workers[1].id&&S.workers[0].pers!==undefined&&S.workers[1].pers!==undefined"))
    ck('no announcement spam for old saves',not any('is The' in l['t'] for l in J("()=>S.log")))
    same=J("()=>{const a=S.workers.map(w=>w.pers+w.rel);EV.ensureAll();return JSON.stringify(a)===JSON.stringify(S.workers.map(w=>w.pers+w.rel))}")
    ck('ensureAll is idempotent',same)
    # a worker hired later is announced once
    J("()=>{S.workers.push({id:'New'+S.day,name:'Newbie',hustle:4,loyal:7,sales:0,wage:200});EV.ensureAll()}")
    ck('new hire announced once',sum('Newbie is The' in l['t'] for l in J("()=>S.log"))==1)
    J("()=>{S.workers.pop()}")
    # forcing every event: resolves once, applies once
    for ev in ['raise','overlooked','recommend','dayoff','promo']:
        J("()=>{document.getElementById('modal').hidden=true;S.ev.q=[];S.workers[0].loyal=5;S.workers[0].cared=S.day-20;S.workers[0].wage=150;S.workers[0].sales=30}")
        q=J(f"()=>EV.force('{ev}','Dre1')")
        ck(ev+': card shows',J("()=>!document.getElementById('modal').hidden&&/CREW/.test(document.getElementById('mcard').innerText)"))
        n=J("()=>S.ev.q.length");ck(ev+': queued once',n==1,n)
        btns=pg.query_selector_all('#mcard .btn')
        btns[0].click();pg.wait_for_timeout(200)
        ck(ev+': first choice resolves',J("()=>S.ev.q.length")==0 and J(f"()=>S.ev.h[0].id")==ev)
        before=J("()=>JSON.stringify([S.workers[0].loyal,S.workers[0].wage,S.workers.length,S.cash])")
        ck(ev+': double resolve does nothing',J(f"()=>EV.resolve('{q['qid']}',0)")==False and J("()=>JSON.stringify([S.workers[0].loyal,S.workers[0].wage,S.workers.length,S.cash])")==before)
    # recommend hires a new worker, no duplicate names
    cap=J("()=>wMax()");ck('recommend respects worker cap (no hire when full)',J("()=>S.workers.length")==3 and cap<=3,cap)
    J("()=>{document.getElementById('modal').hidden=true;S.ev.q=[];S.workers.pop();S.workers[0].loyal=5}")
    J("()=>EV.force('recommend','Dre1')");pg.query_selector_all('#mcard .btn')[0].click();pg.wait_for_timeout(200)
    ck('recommend hires when there is room',J("()=>S.workers.length")==3 and J("()=>S.workers[2].ref")=='Dre1' and J("()=>!!S.workers[2].pers"))
    ck('hire has a unique name',J("()=>new Set(S.workers.map(w=>w.name)).size")>=2)
    # expiry: ignored once, consequence applied once
    J("()=>{Math.random=()=>0.99;S.ev.q=[];S.workers[2].loyal=9;EV.push(EV.defs.overlooked,S.workers[2],true)}")
    l0=J("()=>S.workers[2].loyal");J("()=>{S.day+=5;EV.tick()}");l1=J("()=>S.workers[2].loyal")
    ck('expired event resolves as ignored',J("()=>S.ev.q.length")==0 and l1==l0-1,(l0,l1))
    J("()=>{S.day+=1;EV.tick();S.day+=1;EV.tick()}")
    ck('expired event does not re-apply',J("()=>S.workers[2].loyal")==l1)
    # worker fired mid-event: dropped cleanly
    J("()=>{S.ev.q=[];EV.push(EV.defs.raise,S.workers[1],true);S.workers.splice(1,1);EV.tick()}")
    ck('missing worker drops the event',J("()=>S.ev.q.length")==0)
    # tick twice same day queues at most once per worker+event, cap 3
    J("()=>{S.ev.q=[];S.ev.cd={};S.ev.last=null;Math.random=()=>0;S.workers.forEach(w=>{w.sales=30;w.loyal=5;w.cared=S.day-30;w.pers='ambitious';w.rel=7});EV.tick();EV.tick();}")
    q=J("()=>S.ev.q.map(q=>q.id+':'+q.wid)");ck('queue capped at 3, no duplicates',len(q)<=3 and len(set(q))==len(q),q)
    # save / load round trip keeps queue and history
    ok=J("()=>{const s=JSON.parse(JSON.stringify(S));return s.ev.q.length===S.ev.q.length&&s.ev.h.length===S.ev.h.length&&s.workers.every(w=>w.pers)}")
    ck('save/load keeps events and traits',ok)
    # a real day advance does not crash and shows at most one card
    J("()=>{document.getElementById('modal').hidden=true;S.ev.q=[];Math.random=()=>0.5;nextDay();document.getElementById('modal').hidden=true}")
    ck('nextDay still works',J("()=>typeof S.day")=='number')
    ck('no page errors',not errs,errs[:3])
print('%d/%d'%(sum(res),len(res)))
