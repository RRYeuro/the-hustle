import sys,random
from playwright.sync_api import sync_playwright
MODES=[("story","startLife?0:0"),]
with sync_playwright() as p:
  b=p.chromium.launch()
  found={}
  for seed in range(int(sys.argv[1])):
    pg=b.new_page(viewport={'width':390,'height':844});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:160]))
    pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1200);J=pg.evaluate
    chars=['lucky','tank','ghost','smoke','nita'] 
    mode=seed%3
    try:
      J("""(a)=>{const [seed,mode]=a;let r=seed*9301+49297;Math.random=()=>{r=(r*9301+49297)%233280;return r/233280};
        try{const c=(CHARS[seed%CHARS.length]||{}).id||'lucky';startLife(c)}catch(e){startLife('lucky')}
        document.getElementById('modal').hidden=true;window.noL31=1;S.dr92off=1;S.age=Math.max(S.age||0,14+seed%10);S.cash+=seed*3000;S.rep=seed*7%120;S.heat=seed*13%90;
        for(let d=0;d<10+seed%25;d++){try{nextDay()}catch(e){}document.getElementById('modal').hidden=true;try{if(S.over)break}catch(e){}}
        render()}""",[seed,mode])
    except Exception as e: errs.append('setup '+str(e)[:100])
    tabs=J("()=>[...document.querySelectorAll('.tabs [data-t]')].map(b=>b.dataset.t)")
    for t in tabs:
      J(f"()=>{{document.getElementById('modal').hidden=true;tab='{t}';try{{render()}}catch(e){{}}}}")
      if J("()=>/This tab hit an error/.test(document.body.innerText)"):
        msg=J("()=>(document.body.innerText.match(/This tab hit an error\\n?(.*)/)||[])[1]||''");found.setdefault('tab '+t+': '+msg[:120],seed)
    J("()=>{tab='phone';window._rph=null;render();const u=document.querySelector('[data-unlock]');u&&u.click()}")
    n=J("()=>document.querySelectorAll('.phx button').length")
    for i in range(min(n,40)):
      lab=J(f"()=>{{const b=document.querySelectorAll('.phx button')[{i}];if(!b)return '';const t=b.innerText.slice(0,14);try{{b.click()}}catch(e){{}}return t}}")
      if J("()=>/This tab hit an error/.test(document.body.innerText)"):
        found.setdefault('phone '+lab.replace(chr(10),' ')+': '+J("()=>(document.body.innerText.match(/This tab hit an error\\n?(.*)/)||[])[1]||''")[:120],seed)
      ths=J("()=>[...document.querySelectorAll('.mth-row')].length")
      for k in range(min(ths,15)):
        J(f"()=>{{const b=document.querySelectorAll('.mth-row')[{k}];b&&b.click()}}")
        if J("()=>/This tab hit an error/.test(document.body.innerText)"):
          found.setdefault('thread: '+J("()=>(document.body.innerText.match(/This tab hit an error\\n?(.*)/)||[])[1]||''")[:120],seed)
        J("()=>{const b=document.querySelector('[data-mth=\"\"]');b&&b.click()}")
      J("()=>{document.getElementById('modal').hidden=true;tab='phone';window._rph=null;render();const u=document.querySelector('[data-unlock]');u&&u.click()}")
    # popups
    for c in ["invModal()","document.querySelector('#me')&&document.querySelector('#me').click()","mainMenu(true)","devPanel()","l92recap()"]:
      J(f"()=>{{try{{document.getElementById('modal').hidden=true;{c}}}catch(e){{window.__e=String(e)}}}}")
    for e in errs: found.setdefault('pageerror: '+e,seed)
    pg.close()
  for k,v in found.items(): print('seed',v,'|',k)
  print('done',len(found),'last phone buttons',n)
  b.close()
