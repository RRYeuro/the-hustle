import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':420,'height':860});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:200]) if m.type=='error' and 'sk40' in m.text else None)
    pg.goto('file:///home/claude/the-hustle/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    r=J("()=>{const o={};['slick','shade','val','tank'].forEach(ch=>{S=fresh(ch,'story');S.v5=1;teenStart(ch,14);roll();o[ch]=S.known.map(i=>PINFO[i].lvl+':'+S.trust[i])});return o}")
    ck('teens start with no Big plug (swapped for Mid)',all(not any(x.startswith('Big') for x in v) for v in r.values()) and any(x.startswith('Mid:50') for x in r['slick']),json.dumps(r))
    r=J("()=>{S=fresh('slick','story');S.v5=1;const k=S.known.slice();teenStart('slick',19);return [k.join(),S.known.join()]}")
    ck('adult start: Big plug swapped for Mid (rank ladder)',J("()=>!S.known.some(i=>PINFO[i].lvl==='Big')"),str(r))
    # guide flow
    J("()=>{S=fresh('val','story');S.v5=1;S.safe=0;dcReseed();teenStart('val',14);S.cash=400;roll();tab='block';window.noL31=1;window.noL27=1;S._evDay=S.day;document.getElementById('modal').hidden=true;render()}")
    r=J("()=>({g:/Your first day/.test(document.getElementById('pane').textContent),step:document.querySelector('#pane .row[style*=\"accent\"] .t').textContent})")
    ck('new game: guide on the Block tab, step 1 is Text a plug',r['g'] and 'Text a plug' in r['step'],json.dumps(r))
    J("()=>document.querySelector('[data-a39=\"go\"]').click()");pg.wait_for_timeout(200)
    ck('Show me goes to Move with plug spots open',J("()=>tab==='move'&&!!document.querySelector('#pane [data-a31=\"tx\"]')"))
    J("()=>document.querySelector('#pane [data-a31=\"tx\"]').click()");pg.wait_for_timeout(100)
    J("()=>document.querySelector('#pane [data-a31=\"go\"]').click()");pg.wait_for_timeout(300);J("()=>{document.getElementById('modal').hidden=true}")
    J("()=>{const b=document.querySelector('#mt31 [data-a=\"buy\"]:not([disabled])');b.click()}");pg.wait_for_timeout(300)
    J("()=>{const q=document.getElementById('q');q.value=Math.min(+q.max,q.min*10);q.oninput();document.getElementById('ok').click()}");pg.wait_for_timeout(300);J("()=>{const b=document.getElementById('bmno');if(b)b.click()}")
    J("()=>{l31End(true);tab='block';render()}")
    r=J("()=>({t:S.fd.t,b:S.fd.b,step:(document.querySelector('#pane .row[style*=\"accent\"] .t')||{}).textContent})")
    ck('texting and buying tick off steps 1 and 2',r['t'] and r['b'] and 'Serve the Js' in (r['step'] or ''),json.dumps(r))
    J("()=>{S.st.sold=(S.st.sold||0)+5;nextDay();document.getElementById('modal').hidden=true;tab='block';render()}")
    ck('all done: the "you know the loop" card shows where things are',J("()=>/You know the loop/.test(document.getElementById('pane').textContent)&&/Side hustles/.test(document.getElementById('pane').textContent)"))
    J("()=>document.querySelector('[data-a39=\"x\"]').click()");ck('Got it hides the guide',J("()=>!/Your first day/.test(document.getElementById('pane').textContent)"))
    # collapse on phone after the guide
    J("()=>{S.known=[0,1,2];S.trust[0]=65;S.uiPs=0;S.scan=1;S.uiSc=0;tab='move';render()}")
    r=J("()=>({ps:!!document.querySelector('#pane [data-a31=\"ps\"]'),go:document.querySelectorAll('#pane [data-a31=\"go\"]').length,sc:!!document.querySelector('#pane [data-a36t]'),list:/Police scanner · today/.test(document.getElementById('pane').textContent)})")
    ck('phone: plug spots and scanner fold to one line each',r['ps'] and r['go']==0 and r['sc'] and not r['list'],json.dumps(r))
    J("()=>{document.querySelector('#pane [data-a31=\"ps\"]').click();document.querySelector('#pane [data-a36t]').click()}")
    r=J("()=>({go:document.querySelectorAll('#pane [data-a31=\"go\"]').length,list:/Police scanner · today/.test(document.getElementById('pane').textContent)})")
    ck('tap Show and Details opens them',r['go']>=1 and r['list'],json.dumps(r))
    # existing save (day 30) never shows the guide
    J("()=>{delete S.fd;S.day=30;S.st.sold=200;tab='block';render()}");ck('older games never see the guide',J("()=>S.fd.off===1&&!/Your first day/.test(document.getElementById('pane').textContent)"))
    # fake drip robbery says why
    J("()=>{S.jew={chain:1,grill:1,ring:1,watch:1,pend:1};S.rep=0;S.heat=0;S.fits={};S.fit='street';const R=Math.random;Math.random=()=>0.01;try{wearDay()}finally{Math.random=R}}")
    ck('fake drip robbery explains why',J("()=>S.log.some(x=>/bigger than your name/.test(x.t))"))
    J("()=>{document.getElementById('modal').hidden=true;devPanel()}");ck('dev buttons',J("()=>document.querySelectorAll('[data-d40]').length")==2)
    b.close()
print('ERR',errs[:5]);print(sum(res),'/',len(res))
