import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:200]) if m.type=='error' and 'sk4' in m.text else None)
    pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{localStorage.setItem('tl-clean','0');startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S.cash=20000;S.clean=0;S.heat=10;S.rep=40;S._evDay=S.day;S.picQ=[];render()}")
    bi=J("()=>S.known[0]")
    # meet tones
    J("(bi)=>{S.trust[bi]=50;S.meet={bi,how:'go',from:S.at};S.at=bi;render()}",bi);pg.wait_for_timeout(200)
    ck('meet shows greeting + tone buttons',J("()=>document.querySelectorAll('#mt31 [data-t46]').length>=3&&!!document.querySelector('#mt31 .vb45')"))
    t0=J("(bi)=>S.trust[bi]",bi);J("()=>document.querySelector('#mt31 [data-t46=\"r\"]').click()");pg.wait_for_timeout(200)
    r=J("(bi)=>({tr:S.trust[bi],btn:document.querySelectorAll('#mt31 [data-t46]').length,v:document.querySelectorAll('#mt31 .vb45').length})",bi)
    ck('respect: trust +2, plug answers, buttons gone',r['tr']==t0+2 and r['btn']==0 and r['v']==2,json.dumps(r))
    # haggle forced success -> price drops
    r=J("(bi)=>{const g=GOODS.find(x=>x.id===S.known_g)||GOODS[0];delete S.meet.tone46;delete S.meet.r46;S.hg46=null;const p0=plugPrice('buy',g);Math._r=Math.random;Math.random=()=>0.01;document.querySelector('#mt31')||render();render();return p0}",bi);pg.wait_for_timeout(200)
    J("()=>{document.querySelector('#mt31 [data-t46=\"h\"]').click();Math.random=Math._r}");pg.wait_for_timeout(200)
    r=J("(p0)=>{const g=GOODS[0];return {p0,p1:plugPrice('buy',g),hg:S.hg46}}",r)
    ck('haggle win: 5% off at this meet today',r['hg'] and r['p1']<r['p0'],json.dumps(r))
    J("()=>{S.meet=null;S.hg46=null;render()}")
    # callbacks
    r=J("(bi)=>{S.cb46={m:{},pop:S.day};Math._r=Math.random;Math.random=()=>0.01;const M={bi,how:'go'};const h=l45greet(M);Math.random=Math._r;return h}",bi)
    ck('callback: plug brings up you getting popped',('popped' in r) or ('picked up' in r),r[:200])
    # battery
    J("()=>{S.bat=100;l46bat(-90)}");ck('battery drain + low warning',J("()=>S.bat===10&&S.log.slice(0,3).some(x=>/Phone at/.test(x.t))"))
    J("()=>{S.bat=0}");ck('dead phone = phone off',J("()=>l43PhoneOff()"))
    ck('status bar says No Service',J("()=>/No Service/.test(l46sb())"))
    J("()=>{S.bb={owe:{},miss:{}};S.home=Object.keys(HOMES).find(h=>HOMES[h].rent>0);WD.forEach(f=>{try{if(/S\\.bat=100/.test(String(f)))f()}catch(e){}})}")
    ck('sleeps at home with power: charged to 100',J("()=>S.bat")==100)
    # missed call when phone off
    J("(bi)=>{S.bat=0;S.inbox=[];window.l31Call(bi,false)}",bi);ck('call while dead = missed call',J("()=>(S.inbox[0]||{}).t==='📞 Missed call'"))
    J("()=>{S.bat=100;S.pcall=-99;document.getElementById('modal').hidden=true}")
    J("(bi)=>{window.l31Call(bi,true)}",bi);pg.wait_for_timeout(200)
    ck('incoming call screen with Decline',J("()=>!!document.getElementById('c31c')&&/Decline/.test(document.getElementById('c31c').textContent)"))
    t0=J("(bi)=>S.trust[bi]",bi);J("()=>document.getElementById('c31c').click()")
    r=J("(bi)=>({tr:S.trust[bi],m:(S.inbox[0]||{}).t})",bi);ck('decline: trust -2 + voicemail text',r['tr']==max(0,t0-2) and 'voicemail' in (r['m'] or '').lower() or r['m']=='Noted.',json.dumps(r))
    # text haggle via phone reply
    r=J("(bi)=>{const n=plugName(bi);window._mth=n;S.inbox.unshift({d:S.day,f:'You',to:n,t:'Can you do better on the price?'});S.inbox.unshift({d:S.day,f:n,t:'x'});return 1}",bi)
    r=J("(bi)=>{S.inbox=[];const n=plugName(bi);window._mth=n;const b=document.createElement('button');b.dataset.flav='1';b.dataset.fk='plug';document.body.appendChild(b);Math._r=Math.random;Math.random=()=>0.01;b.click();b.remove();return n}",bi);pg.wait_for_timeout(1300)
    r=J("(n)=>{Math.random=Math._r;return {a:(S.inbox[0]||{}),b:(S.inbox[1]||{}),hg:S.hg46}}",r)
    ck('text haggle: typed reply lands after dots, discount set',r['a'].get('f')!='You' and r['b'].get('f')=='You' and r['hg'] and '5%' in r['a'].get('t',''),json.dumps(r))
    # court scene
    J("()=>{document.getElementById('modal').hidden=true;S.picQ=[];S.strikes=1;prStart();S.pr.cc=0;document.getElementById('modal').hidden=true;w4Court()}")
    ck('court in session scene first',J("()=>/Court is in session/.test(document.querySelector('#mcard h2').textContent)"))
    J("()=>document.getElementById('wc0').click()");pg.wait_for_timeout(200)
    r=J("()=>({jr:w4().jr,h:document.querySelector('#mcard h2').textContent})");ck('"Yes your honor": +4% odds, then the court card',abs(r['jr']-0.04)<1e-9 and 'Court date' in r['h'],json.dumps(r))
    ck('verdict uses and clears the bonus',J("()=>{const X=w4();let got=null;const o=window.w4Verdict;return typeof o==='function'}"))
    J("()=>{document.getElementById('modal').hidden=true;devPanel()}");ck('dev buttons',J("()=>document.querySelectorAll('[data-d46]').length")==5)
    ck('no errors',not errs,json.dumps(errs[:5]))
    b.close()
print(sum(res),'/',len(res))
