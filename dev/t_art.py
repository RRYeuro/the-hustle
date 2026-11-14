import json,subprocess,time
from playwright.sync_api import sync_playwright
F=json.load(open('/tmp/claude-0/slice/faces.json'))
srv=subprocess.Popen(['python3','-I','-m','http.server','8771','-d','/home/claude/the-hustle'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();er=[];pg.on('pageerror',lambda e:er.append(str(e)[:200]));bad=[];pg.on('response',lambda r:bad.append(r.url) if r.status>=400 else None)
    pg.goto('http://localhost:8771/index.html',wait_until='load');pg.wait_for_timeout(2500)
    r=pg.evaluate("""(F)=>{startLife('lucky');document.getElementById('modal').hidden=true;const out={wrong:[],shared:[]};
     const look=n=>{const k=n.toLowerCase();return [ART3.c[k],ART3.g&&ART3.g[k],ART3.b&&ART3.b[k],CUSTPICS[n],CONNPICS[n],STRAPPICS[n]].filter(Boolean)};
     const city={'Mr. Dell':'charlotte','Sweets':'atlanta','Big Ray':'houston','Uncle Sal':'newyork'};
     Object.entries(F).forEach(([n,u])=>{if(city[n]){if(ARTX('cp_'+city[n])!==u)out.wrong.push(n);return}const L=look(n);if(!L.length||L.some(x=>x!==u))out.wrong.push(n+':'+L.length)});
     // no face used by two different names
     const all={};const add=(n,u)=>{if(!u)return;(all[u]=all[u]||new Set()).add(n.toLowerCase())};Object.entries(ART3.c).forEach(([n,u])=>add(n,u));Object.entries(ART3.g||{}).forEach(([n,u])=>add(n,u));Object.entries(ART3.b||{}).forEach(([n,u])=>add(n,u));Object.entries(CUSTPICS).forEach(([n,u])=>add(n,u));Object.entries(CONNPICS).forEach(([n,u])=>add(n,u));
     out.shared=Object.values(all).map(s=>[...s]).filter(a=>a.length>1&&!(a.length===2&&a.some(x=>x[0]==='_')));
     out.missing=['Ana','Jess','Toya','Lala','Shon','Roxy','Danny','Minh','Black','Fresh','Gee','Shawty','Big Lo','Boogie','Nay','Jaylen','Coop'].filter(n=>!faceOf(n,'c'));
     return out}""",F)
    print(json.dumps(r));print('broken files',bad[:5],'errs',er[:3])
    imgs=pg.evaluate("(F)=>Promise.all(Object.values(F).map(u=>new Promise(r=>{const i=new Image();i.onload=()=>r(i.naturalWidth);i.onerror=()=>r(0);i.src=u})))",F)
    print('all load:',all(x==160 for x in imgs),len(imgs))
    ok=not r['wrong'] and not r['missing'] and all(x==160 for x in imgs) and not er
    print('PASS' if ok else 'FAIL','new faces wired, one per name')
    b.close()
srv.terminate()
