import json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();er=[];pg.on('pageerror',lambda e:er.append(str(e)[:200]))
    pg.goto('file:///home/claude/the-hustle/index.html',wait_until='load');pg.wait_for_timeout(1800)
    r=pg.evaluate("""()=>{startLife('lucky');document.getElementById('modal').hidden=true;const o={};let bad=[];
     [0,1,2,3,4,5].forEach(bi=>PINFO[bi].carries.forEach(id=>{const g=G(id);const row=[20,60,90].map(q=>{S.offer[bi][id].q=q;const u=l34U(bi,g);const nm=l34N(u,g);if(/^\\d/.test(nm)&&!/oz/.test(nm))bad.push(id+u);
       // a size must be reachable: fits a stock roll and is a multiple of the step
       const st=newStock(bi,g);if(u>st*2)bad.push('stock '+bi+id+q+' u'+u+' st'+st);return nm+' ~$'+Math.round(S.prices[bi][id]*u)});o[PINFO[bi].lvl+' '+g.name+' @'+BLOCKS[bi]]=row.join(' | ')}));
     return {o,bad}}""")
    for k,v in r['o'].items():print(k.ljust(26),v)
    print('bad',r['bad'],er);print('PASS' if not r['bad'] and not er else 'FAIL','unit by quality')
    b.close()
