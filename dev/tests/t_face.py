from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();er=[];pg.on('pageerror',lambda e:er.append(str(e)[:200]))
    pg.goto('file:///home/claude/the-hustle/index.html',wait_until='load');pg.wait_for_timeout(1000)
    r=pg.evaluate("""()=>{startLife('lucky');document.getElementById('modal').hidden=true;
     const pools={workers:WNAMES,friends:FNAMES,crew:CNAMES2,recruitF:NEWF,recruitM:NEWM,debtors:DNAMES,plugs:PLUGS};const miss={};
     for(const k in pools){const m=pools[k].filter(n=>!faceOf(n,'c'));if(m.length)miss[k]=m}
     const mg=GNAMES.filter(n=>!faceOf(n,'g')),mb=BNAMES.filter(n=>!faceOf(n,'b'));if(mg.length)miss.girls=mg;if(mb.length)miss.boys=mb;
     const mc=CNAMES.filter(n=>!CUSTPICS[n]);if(mc.length)miss.customers=mc;const mk=CONNECTS.filter(n=>!CONNPICS[n]);if(mk.length)miss.connects=mk;
     // same face used by two different names
     const all={};const add=(n,u)=>{if(!u)return;(all[u]=all[u]||new Set()).add(n.toLowerCase())};
     Object.entries(ART3.c).forEach(([n,u])=>add(n,u));Object.entries(ART3.g).forEach(([n,u])=>add(n,u));Object.entries(ART3.b).forEach(([n,u])=>add(n,u));Object.entries(CUSTPICS).forEach(([n,u])=>add(n,u));Object.entries(STRAPPICS).forEach(([n,u])=>add(n,u));Object.entries(CONNPICS).forEach(([n,u])=>add(n,u));PLUGS.forEach((n,i)=>add(n,PLUGPICS[i]));
     const shared=Object.values(all).map(s=>[...s]).filter(a=>a.length>1&&!(a.length===2&&a.some(x=>x[0]==='_')));
     // pronoun check for female names
     const fem=[...new Set([...WFEM,...FNAMES_F,...NEWF.filter(n=>true)])];const badp=fem.filter(n=>mHe({name:n},'he')!=='she');
     S.cands=[{id:'a',name:'Kim',hustle:5,loyal:5,wage:100}];S.workers=[{id:'w',name:'Juice',hustle:5,loyal:5,sales:3,stash:{},held:0}];
     return {miss,shared,badp}}""")
    print(r);print('errs',er);b.close()
