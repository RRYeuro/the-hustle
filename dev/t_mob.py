import subprocess,time,sys
from playwright.sync_api import sync_playwright
srv=subprocess.Popen(['python3','-I','-m','http.server','8766','-d','/home/claude/the-hustle'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch();c=b.new_context(viewport={'width':390,'height':780},has_touch=True,is_mobile=True,device_scale_factor=2);pg=c.new_page()
    pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
    bad=[];pg.on('response',lambda r:bad.append(r.url) if r.status>=400 else None)
    pg.goto('http://localhost:8766/index.html',wait_until='load');pg.wait_for_timeout(1200)
    pg.evaluate("()=>{startLife('shade');document.getElementById('modal').hidden=true;tab='move';render()}");pg.wait_for_timeout(800)
    r=pg.evaluate("""()=>{const t=document.querySelector('.tbs26'),m=[...document.querySelectorAll('.tabs')].filter(x=>x.offsetParent||getComputedStyle(x).position==='fixed');
      const imgs=[...document.images].filter(i=>i.complete&&!i.naturalWidth&&i.src).length;
      return {tb:t?getComputedStyle(t).position:null,tabs:m.map(x=>getComputedStyle(x).position+':'+x.children.length),fm:!!document.getElementById('fm26'),broken:imgs}}""")
    print(r);pg.screenshot(path='/tmp/claude-0/mob.png')
    # tap the Block tab in the real bar
    ok=pg.evaluate("()=>{const b=[...document.querySelectorAll('.tabs button')].find(x=>/block/i.test(x.textContent));if(!b)return 'nobtn';const r=b.getBoundingClientRect();const e=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return (e===b||b.contains(e))?'clickable':'covered by '+(e&&e.className)}")
    print('block tab:',ok)
    # manager: trap with worker, no t.g
    m=pg.evaluate("""()=>{S.age=19;S.traps=S.traps||{};S.traps[3]={w:'w1',up:0};S.workers=[{id:'w1',name:'Juice',sales:20,hustle:9,loyal:7,stash:{}}];try{shSt().own=1}catch(e){return 'sh '+e}
      const el=document.createElement('button');el.dataset.a='tmgr';el.dataset.i='3';document.body.appendChild(el);el.click();return (S.log[0]||{}).t+' | mgr='+JSON.stringify(S.traps[3])}""")
    print('manager:',m)
    b.close()
srv.terminate();print('errs',errs[:5],'bad',bad[:5])
