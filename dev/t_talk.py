import json
from playwright.sync_api import sync_playwright
res=[];errs=[]
def ck(n,c,x=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('C:'+m.text[:200]) if m.type=='error' and 'sk4' in m.text else None)
    pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{localStorage.setItem('tl-clean','0');startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S.cash=20000;S.heat=10;S._evDay=S.day;S.picQ=[];render()}")
    r=J("()=>{phoneMsg('Dre','Load picked up, boss. $500 made it to the stash.');return S.inbox[0].t}")
    ck('crew text in voice',r!='Load picked up, boss. $500 made it to the stash.' and '$500' in r,r)
    r=J("()=>{const bi=S.known[0];S.trust[bi]=80;phoneMsg(plugName(bi),'\"Bet. I am at the spot on '+BLOCKS[bi]+'. Come through.\"');return [S.inbox[0].t,PINFO[bi].lvl]}")
    ck('plug text uses level + trust voice',r[0].find('Come through.\"')<0,json.dumps(r))
    r=J("()=>{phoneMsg('Dre','Watched the Kings. Strength 40, beef 30/100. You could take them.');return [S.inbox[0].t,S.log[0].t]}")
    ck('numbers moved out of the text into a tag','Strength' not in r[0] and 'strength 40' in r[1],json.dumps(r))
    r=J("()=>{phoneMsg('Some guy','Random text that is not in the table.');return S.inbox[0].t}")
    ck('unknown texts pass through',r=='Random text that is not in the table.',r)
    # court
    J("()=>{S.picQ=[];document.getElementById('modal').hidden=true;S.strikes=1;S.rec={n:2,f:1,last:0};prStart();S.pr.cc=0;document.getElementById('modal').hidden=true;w4Court()}")
    r=J("()=>({v:document.querySelectorAll('#mcard .vb45').length,t:document.querySelector('#mcard').textContent.slice(0,400),btn:document.querySelectorAll('#mcard button').length})")
    ck('court has people talking + facts under',r['v']>=2 and 'seen your name' in r['t'] and r['btn']>=4,json.dumps(r))
    pg.screenshot(path='/tmp/claude-0/s43/court.png')
    J("()=>{document.getElementById('modal').hidden=true;S.pr=null;S.inJail=0;w4Trial(5,'Distribution')}")
    ck('trial: bailiff + judge',J("()=>/All rise/.test(document.querySelector('#mcard').textContent)"))
    J("()=>{[...document.querySelectorAll('#mcard button')].find(b=>/Public defender/.test(b.textContent)).click()}");pg.wait_for_timeout(300)
    r=J("()=>({law:w4().law,t:document.getElementById('modal').hidden?'':document.querySelector('#mcard').textContent.slice(0,300)})")
    ck('lawyer pick remembered (public defender)',r['law']=='pd',json.dumps(r))
    if 'Your strategy' in r['t']: ck('public defender talks like one','two hundred cases' in r['t'],r['t'])
    # clean toggle
    J("()=>{localStorage.setItem('tl-clean','1');phoneMsg('Dre','Something went wrong with the load...');}")
    r=J("()=>S.inbox[0].t");ck('clean language swaps curses',('fuck' not in r.lower()) and ('shit' not in r.lower()),r)
    J("()=>{localStorage.setItem('tl-clean','0');document.getElementById('modal').hidden=true;mainMenu(true)}")
    ck('main menu has the language button',J("()=>!!document.getElementById('mcln')&&/Raw/.test(document.getElementById('mcln').textContent)"))
    J("()=>document.getElementById('mcln').click()");ck('button toggles to Clean',J("()=>localStorage.getItem('tl-clean')==='1'&&/Clean/.test(document.getElementById('mcln').textContent)"))
    J("()=>localStorage.setItem('tl-clean','0')")
    ck('plug lines helper',J("()=>{const bi=S.known[0];return l45pl(bi,'in').length>10&&l45pl(bi,'load','Loud',20).includes('20%')}"))
    ck('no errors',not errs,json.dumps(errs[:5]))
    b.close()
print(sum(res),'/',len(res))
