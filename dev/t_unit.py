from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();er=[];pg.on('pageerror',lambda e:er.append(str(e)[:200]))
    pg.goto('file:///home/claude/the-hustle/index.html',wait_until='load');pg.wait_for_timeout(1800)
    r=pg.evaluate("""()=>{startLife('lucky');document.getElementById('modal').hidden=true;S.known=[0,1,2,3,4,5];S.rep=0;const o={};let bad=[];
     [1,3,4,5].forEach(bi=>PINFO[bi].carries.forEach(id=>{const g=G(id);S.at=bi;S.meet={bi,from:bi,how:'spot'};const pr=[20,60,90].map(q=>{S.offer[bi][id].q=q;S.offer[bi][id].tip=0;const u=l34U(bi,g);return grade(q,g)+' $'+Math.round(plugPrice('buy',g,true)*u*bulk(u,g))});
       const u=l34U(bi,g);const nums=pr.map(x=>+x.split('$')[1]);if(!(nums[0]<nums[1]&&nums[1]<nums[2]))bad.push(bi+id);o[PINFO[bi].lvl+' '+g.name+' ('+l34N(u,g)+')']=pr.join(' | ')}));delete S.meet;
     return {o,bad}}""")
    for k,v in r['o'].items():print(k.ljust(30),v)
    print('bad',r['bad'],er);print('PASS' if not r['bad'] and not er else 'FAIL','price of a unit rises with quality')
    b.close()
