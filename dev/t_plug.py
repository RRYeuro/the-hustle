import sys,json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append((n,bool(c)));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':420,'height':860});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:200]) if m.type=='error' and 'sk31' in m.text else None)
    pg.goto('file:///home/claude/the-hustle/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S.cash=20000;S.clean=5000;S.heat=10;S.rep=80;S.at=0;S.known=[0,1,2,3];S.trust[0]=65;S.trust[1]=30;S.trust[2]=10;S.trust[3]=70;S.cap=900;S.en=100;S.car=null;S.friends=[];tab='block';render()}")
    # Block tab: no plug card
    r=J("()=>({buy:document.querySelectorAll('#pane [data-a=\"buy\"]').length,card:/Knows you|Kick it|Rob h/.test(document.getElementById('pane').textContent),txt:/Plugs are spots on the Move map/.test(document.getElementById('pane').textContent)})")
    ck('Block tab has no plug card or Buy',r['buy']==0 and not r['card'] and r['txt'],json.dumps(r))
    # Move: plug spots section
    J("()=>{tab='move';render()}")
    r=J("()=>({go:[...document.querySelectorAll('#pane [data-a31=\"go\"]')].map(b=>b.dataset.i+':'+b.textContent.trim()),tx:[...document.querySelectorAll('#pane [data-a31=\"tx\"]')].map(b=>b.dataset.i),intro:[...document.querySelectorAll('#pane [data-a31=\"in\"]')].map(b=>b.dataset.i),sec:/Plug spots/.test(document.getElementById('pane').textContent)})")
    ck('Move lists plug spots: 60+ go, 20-59 text, under 20 and strangers intro',r['sec'] and r['go']==['3:Go · 1 day','0:Meet'] and r['tx']==['1'] and sorted(r['intro'])==['2','4','5'],json.dumps(r))
    # text first
    d0=J("()=>S.day")
    J("()=>l31Text(1)");r=J("()=>({open:S.pk[1].open-S.day,go:!!document.querySelector('#pane [data-a31=\"go\"][data-i=\"1\"]'),msg:S.log[0].t})")
    ck('text opens the spot today and tomorrow',r['open']==1 and r['go'] and 'spot' in r['msg'],json.dumps(r))
    J("()=>{S.pk[1].txt=-9;S.pk[1].open=-9;S.heat=80;l31Text(1)}");ck('too hot: text gets a no',J("()=>!(S.pk[1].open>=S.day)&&/hot|Cool off|Not today/i.test(S.log[0].t)"),J("()=>S.log[0].t"));J("()=>{S.heat=10}")
    # meet here: free, full card with actions
    J("()=>l31Go(0)");pg.wait_for_timeout(200)
    r=J("()=>({ov:!!document.getElementById('mt31'),day:S.day,how:S.meet&&S.meet.how,acts:[...new Set([...document.querySelectorAll('#mt31 [data-a]')].map(b=>b.dataset.a))],tx:!!document.querySelector('#mt31 [data-tx50]'),hd:document.querySelector('#mt31 .mt31h').innerText})")
    ck('meet at the spot: slim plug line + Text, buy/sell, no day',r['ov'] and r['day']==d0 and r['how']=='spot' and 'buy' in r['acts'] and r['tx'] and 'pkick' not in r['acts'],json.dumps(r))
    # no delivery tax at the spot
    r2=J("()=>{const g=G(PINFO[0].carries[0]);const a=plugPrice('buy',g);const M=S.meet;delete S.meet;const b=plugPrice('buy',g);S.meet=M;return [a,b]}")
    ck('no delivery charge at the spot',r2[0]==r2[1],str(r2))
    # Low plug sells grams: buy via the real popup
    c0=J("()=>S.cash");cl0=J("()=>cleanCash()")
    J("()=>document.querySelector('#mt31 [data-a=\"buy\"]:not([disabled])').click()");pg.wait_for_timeout(300)
    r=J("()=>({min:+document.getElementById('q').min,step:+document.getElementById('q').step,lvl:PINFO[0].lvl})")
    ck('Low plug sells small (gram or single steps)',r['lvl']=='Low' and r['min']<=1,json.dumps(r))
    J("()=>{const q=document.getElementById('q');q.value=q.min;q.oninput();document.getElementById('ok').click()}");pg.wait_for_timeout(300);J("()=>{const b=document.getElementById('bmno');if(b)b.click()}");pg.wait_for_timeout(200)
    r=J("()=>({cash:S.cash,clean:cleanCash(),ov:!!document.getElementById('mt31')})")
    ck('buy spends dirty first, clean untouched',r['cash']<c0 and r['clean']==min(cl0,r['cash']) and r['ov'],json.dumps(r)+str([c0,cl0]))
    J("()=>document.getElementById('mt31x').click()");ck('Done ends the meet',J("()=>!S.meet&&!document.getElementById('mt31')&&S.at===0"))
    # go to a 60+ spot on foot = a day, then meet opens
    J("()=>{window._nd0=S.day;l31Go(3)}");pg.wait_for_timeout(400)
    r=J("()=>({at:S.at,dd:S.day-window._nd0,meet:!!S.meet,modal:!document.getElementById('modal').hidden})")
    ck('walking to a spot takes the day',r['at']==3 and r['dd']==1 and (r['meet'] or r['modal']),json.dumps(r))
    J("()=>{document.getElementById('modal').hidden=true;if(!S.meet)l31Meet(3);render()}")
    # Big/Mid plug: bulk units
    r=J("""()=>{const out={};[0,1,2,3,4,5].forEach(bi=>{out[bi+PINFO[bi].lvl]=PINFO[bi].carries.map(id=>id+':'+l34U(bi,G(id))+' '+l34N(l34U(bi,G(id)),G(id)))});return out}""")
    print('  units',json.dumps(r))
    lvl=J("()=>PINFO[3].lvl");gid=J("()=>PINFO[3].carries[0]")
    J("()=>{S.cash=60000;S.clean=5000;render();document.querySelector('#mt31 [data-a=\"buy\"]:not([disabled])').click()}");pg.wait_for_timeout(300)
    r=J("()=>({min:+document.getElementById('q').min,step:+document.getElementById('q').step,max:+document.getElementById('q').max,sizes:[...document.querySelectorAll('#mcard [data-z]')].map(b=>b.textContent.trim()),txt:/sold by the/.test(document.getElementById('mcard').textContent)})")
    ck(f'{lvl} plug sells in bulk units only',r['min']>=14 and r['step']==r['min'] and abs(r['max']/r['min']-round(r['max']/r['min']))<1e-6 and r['txt'] and not any(x.startswith('8th') or x.startswith('Quarter') for x in r['sizes']),json.dumps(r))
    inv0=J("(g)=>S.inv[g]",gid);c0=J("()=>S.cash");u0=J("()=>used()")
    J("()=>{const q=document.getElementById('q');q.value=q.min;q.oninput();document.getElementById('ok').click()}");pg.wait_for_timeout(300);J("()=>{const b=document.getElementById('bmno');if(b)b.click()}");pg.wait_for_timeout(200)
    r2=J("(g)=>({inv:S.inv[g],cash:S.cash,clean:cleanCash(),used:used()})",gid)
    ck('bulk buy: one unit lands, stash space follows, cash stays dirty-first',abs((r2['inv']-inv0)-r['min'])<1e-6 and r2['cash']<c0 and r2['clean']==5000 and r2['used']>u0,json.dumps(r2))
    J("()=>{S.cash=40;render();const b=document.querySelector('#mt31 [data-a=\"buy\"]:not([disabled])');b&&b.click()}");pg.wait_for_timeout(300)
    ck('cannot afford a bulk unit: clear message',J("()=>/only sells|Can't afford/.test(S.log[0].t)&&document.getElementById('modal').hidden"),J("()=>S.log[0].t+' MODAL:'+(document.getElementById('modal').hidden?'':document.querySelector('#mcard').textContent.slice(0,160))"))
    # next day ends a meet; bust ends a meet
    J("()=>{S.cash=20000;nextDay();render()}");ck('next day ends the meet',J("()=>!S.meet&&!document.getElementById('mt31')"));J("()=>{document.getElementById('modal').hidden=true}")
    # street sells only to the Js
    J("()=>{S.meet&&l31End();S.inv.loud=20;tab='block';render();document.querySelector('#pane [data-a=\"sell\"]').click()}");pg.wait_for_timeout(300)
    r=J("()=>({open:!document.getElementById('modal').hidden,plug:document.querySelectorAll('#mcard [data-to=\"plug\"]').length,js:/Js/.test(document.getElementById('mcard').textContent)})")
    ck('Block tab sell goes to the Js only',r['open'] and r['plug']==0 and r['js'],json.dumps(r));J("()=>{document.getElementById('modal').hidden=true}")
    J("()=>{qtyModal('buy',G('loud'))}");ck('no buying outside a meet',J("()=>document.getElementById('modal').hidden&&/Move map/.test(S.log[0].t)"))
    # call: come to me (delivery 8%) and spot opens
    J("()=>{S.trust[1]=45;S.pk[1].pu=-9;S.at=0;l31Call(1,true)}");ck('call popup',J("()=>/is calling/.test(document.querySelector('#mcard h2').textContent)&&S.pk[1].open>=S.day"))
    J("()=>document.getElementById('c31a').click()");pg.wait_for_timeout(200)
    r=J("()=>{const g=G(PINFO[1].carries[0]);const a=plugPrice('buy',g);const M=S.meet;delete S.meet;const b=plugPrice('buy',g);S.meet=M;return {how:M&&M.how,from:M&&M.from,a,b}}")
    ck('call: plug comes to you, 8% more, you stay put',r['how']=='pull' and r['from']==0 and abs(r['a']-round(r['b']*1.08))<=1,json.dumps(r))
    J("()=>{try{busted()}catch(e){window._be=String(e)}}");ck('bust ends the meet',J("()=>!S.meet&&!window._be"),J("()=>window._be"))
    J("()=>{document.getElementById('modal').hidden=true;S.pr=null;S.over=false;S.inJail=0;devPanel()}");ck('dev buttons',J("()=>document.querySelectorAll('[data-d31]').length")==7)
    ck('tutorial entry',J("()=>TUT.some(t=>/Plug spots and bulk/.test(t[0]))"))
    b.close()
bad=[n for n,c in res if not c];print('ERRORS',errs[:6]);print(f'{len(res)-len(bad)}/{len(res)} passed')
