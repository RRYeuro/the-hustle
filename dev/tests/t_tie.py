import json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':420,'height':860});er=[];pg.on('pageerror',lambda e:er.append(str(e)[:200]))
    pg.goto('file:///home/claude/the-hustle/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    r=J("""()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;S.char='lucky';S.age=19;S.cal=0;S.school='out';S.cash=9000;S.heat=5;S.at=0;S.known=[0,2];S.ex=2;S.trust[2]=10;S.trust[0]=30;S.friends=[];S.crewM=[];S.rep=0;tab='move';render();
      const go=[...document.querySelectorAll('#pane [data-a31="go"]')].map(b=>b.dataset.i+':'+b.closest('.row').querySelector('.s').textContent.slice(-12));
      const come=[...document.querySelectorAll('#pane [data-a31="pu"]')].map(b=>b.dataset.i);
      const tx=[...document.querySelectorAll('#pane [data-a31="tx"]')].map(b=>b.dataset.i);
      const name=plugName(2);l31PullUp(2);const how=S.meet&&S.meet.how;const g=G(PINFO[2].carries[0]);const a=plugPrice('buy',g);const M=S.meet;delete S.meet;const b2=plugPrice('buy',g);S.meet=M;const hd=document.querySelector('#mt31 .mt31h').innerText;l31End();
      return {go,come,tx,name,how,a,b2,hd,at:S.at}}""")
    print(json.dumps(r,indent=0)[:900]);print('errs',er)
    ok=any(x.startswith('2:') for x in r['go']) and r['come']==['2'] and r['tx']==['0'] and r['name']=='Tre' and r['how']=='pull' and r['a']==r['b2'] and r['at']==0 and 'no delivery charge' in r['hd']
    print('PASS' if ok else 'FAIL',"story tie: Lucky's ex is always open at low trust, comes to her free; a 30-trust plug needs a text")
    b.close()
