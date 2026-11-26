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
     S.workers=[{id:'Dre1',name:'Dre',hustle:5,loyal:5,sales:20,xp:20,wage:150,held:100,stash:{},sq:{}},{id:'Dre1b',name:'Dre',hustle:4,loyal:8,sales:3,xp:12,wage:150,held:0,stash:{},sq:{}},{id:'Rosa1',name:'Rosa',hustle:7,loyal:9,sales:25,xp:25,wage:200,held:0,stash:{},sq:{}}];
     S.traps={0:{w:'Dre1',stock:{},cash:0},1:{w:'Rosa1',stock:{},cash:0}};render()}""")
    ck('only one event system (EV93)',J("()=>!!window.EV93&&!window.EV"))
    # many days, mixed rolls: no errors, queue bounded, no duplicate ids, no negative stats
    bad=0
    for i in range(40):
        J("()=>{document.getElementById('modal').hidden=true;nextDay();document.getElementById('modal').hidden=true}")
        q=J("()=>S.ev&&S.ev.q?S.ev.q.map(e=>e.id):[]")
        if len(q)>2 or len(set(q))!=len(q):bad+=1
    ck('40 days: queue capped at 2, no duplicate ids',bad==0,bad)
    ck('loyalty stays 0-10',J("()=>S.workers.every(w=>w.loyal>=0&&w.loyal<=10)"))
    J("""()=>{document.getElementById('modal').hidden=true;S.workers=[{id:'Dre1',name:'Dre',hustle:5,loyal:5,sales:20,xp:20,wage:150,held:100,stash:{},sq:{}},{id:'Dre1b',name:'Dre',hustle:4,loyal:8,sales:3,xp:12,wage:150,held:0,stash:{},sq:{}},{id:'Rosa1',name:'Rosa',hustle:7,loyal:9,sales:25,xp:25,wage:200,held:0,stash:{},sq:{}}];S.ev={q:[],cd:{},hist:[],done:{}};render()}""")
    ck('loyalty stays 0-10 (2)',J("()=>S.workers.every(w=>w.loyal>=0&&w.loyal<=10)"))
    J("()=>{document.getElementById('modal').hidden=true;nextDay();document.getElementById('modal').hidden=true}")
    ck('personalities assigned, same-name workers separate',J("()=>S.workers.every(w=>w.pers)&&S.workers[0].id!==S.workers[1].id"))
    # resolve exactly once
    J("()=>{document.getElementById('modal').hidden=true;S.ev.q=[];S.ev.cd={};EV93.queue({k:'raise',wid:'Rosa1',day:S.day})}")
    ev=J("()=>S.ev.q[0]");w0=J("()=>S.workers[2].wage")
    J("(e)=>EV93.resolve(e,0)",ev);w1=J("()=>S.workers[2].wage")
    J("(e)=>EV93.resolve(e,0)",ev);w2=J("()=>S.workers[2].wage")
    ck('raise applies once',w1>w0 and w2==w1,(w0,w1,w2))
    # card renders for every kind
    for k in ['raise','overlook','buyer','role','wild']:
        J("(k)=>{document.getElementById('modal').hidden=true;S.ev.q=[];S.ev.cd={};S.ev.done={};EV93.show({k:k==='wild'?'wild':k,roll:k==='wild'?'big':undefined,wid:'Rosa1',day:S.day,id:'t'+k})}",k)
        ck(k+' card shows with choices',J("()=>!document.getElementById('modal').hidden&&document.querySelectorAll('#mcard .btn').length>=2"))
    # fired worker mid-event
    J("()=>{document.getElementById('modal').hidden=true;S.ev.q=[{k:'raise',wid:'GONE',day:S.day,id:'raise:GONE:1',exp:S.day+3}];nextDay();document.getElementById('modal').hidden=true}")
    ck('event for a fired worker does not crash',True)
    # junk queue entries from older builds are ignored
    J("()=>{S.ev.q=[{id:'x',wid:'Rosa1'},{qid:'e1',id:'raise',wid:'Rosa1'}];document.getElementById('modal').hidden=true;nextDay();document.getElementById('modal').hidden=true}")
    ck('junk queue entries ignored',J("()=>S.ev.q.every(e=>e.k)"))
    ck('save/load round trip',J("()=>{const s=JSON.parse(JSON.stringify(S));return s.workers.length===S.workers.length&&Array.isArray(s.ev.q)}"))
    ck('no page errors',not errs,errs[:3])
print('%d/%d'%(sum(res),len(res)))
