import json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':420,'height':860});er=[];pg.on('pageerror',lambda e:er.append(str(e)[:200]))
    pg.goto('file:///home/claude/the-hustle/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    r=J("""()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;S.char='lucky';S.age=19;S.cal=0;S.school='out';S.cash=9000;S.heat=5;S.at=0;S.known=[0,2];S.ex=2;S.trust[2]=10;S.trust[0]=10;S.friends=[];S.crewM=[];S.rep=0;tab='block';render();
      const row=[...document.querySelectorAll('[data-a31="pu"]')].map(b=>b.dataset.i+':'+b.disabled+':'+b.closest('.row').querySelector('.s').textContent.slice(0,40));
      const intro=[...document.querySelectorAll('[data-a31="in"]')].map(b=>b.disabled);
      const g=G(PINFO[2].carries[0]);const base=plugPrice('buy',g);l31PullUp(2);const inMeet=plugPrice('buy',g);const name=plugName(2);const hd=document.querySelector('#mt31 .mt31h').innerText;l31End();
      return {row,intro,base,inMeet,name,hd,at:S.at}}""")
    print(json.dumps(r,indent=0)[:900]);print('errs',er)
    ok=r['row'][0].startswith('2:false') and 'Your ex' in r['row'][0] and r['name']=='Tre' and r['at']==0 and 'no delivery charge' in r['hd']
    print('PASS' if ok else 'FAIL','story tie: Lucky ex pulls up at low trust, vouches, no delivery charge')
    b.close()
