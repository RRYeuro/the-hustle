from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':420,'height':860});er=[];pg.on('pageerror',lambda e:er.append(str(e)[:200]))
    pg.goto('file:///home/claude/the-hustle/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    r=J("""()=>{startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=19;S.cal=0;S.school='out';S.cash=1000;S.at=0;S.en=50;
      const o={};S.car=null;let d=S.day;act('go',{dataset:{i:'1'}});o.walk=[S.at,S.day-d];document.getElementById('modal').hidden=true;
      S.car=Object.keys(CARS)[0];d=S.day;const c=S.cash,e=S.en;act('go',{dataset:{i:'2'}});o.drive=[S.at,S.day-d,c-S.cash,e-S.en];
      S.en=1;d=S.day;act('go',{dataset:{i:'3'}});o.tired=[S.at,S.day-d];document.getElementById('modal').hidden=true;
      S.en=50;S.at=0;d=S.day;const P=PLACES.find(p=>placeAt(p.id)!==0);openPlace(P.id);const g=document.getElementById('gt');if(g)g.click();o.place=[S.at===placeAt(P.id),S.day-d];
      tab='move';document.getElementById('modal').hidden=true;render();o.label=[...document.querySelectorAll('.tbs26 small')].map(x=>x.textContent).join(',');return o}""")
    print(r,er)
    ok=r['walk']==[1,1] and r['drive']==[2,0,5,3] and r['tired'][1]==1 and r['place']==[True,0] and 'DRIVE' in r['label']
    print('PASS' if ok else 'FAIL','car moves take no day');b.close()
