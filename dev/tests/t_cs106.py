# seasons: cycle, holiday, J price + business effects, chip, turn note, calendar mode safe
from playwright.sync_api import sync_playwright
SETUP="()=>{localStorage.setItem('tl-clean','0');startLife('lucky');document.getElementById('modal').hidden=true;window.noL31=1;window.noL27=1;S.age=22;S.cal=0;S.school='out';S.cash=20000;S._evDay=S.day;S.picQ=[];S.dr92off=1;S.recapOff=1;S.biz={wash:1,laundry:1};render()}"
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
  pg.goto('http://127.0.0.1:8765/index.html',wait_until='load');pg.wait_for_timeout(1500);J=pg.evaluate;J(SETUP)
  ok=lambda n,c,x='':print(('PASS ' if c else 'FAIL ')+n,'' if c else x)
  ok('all four seasons cycle',J("()=>new Set(Array.from({length:120},(_,i)=>CS106.season(i+1))).size===4"))
  ok('holiday weeks exist',J("()=>Array.from({length:120},(_,i)=>CS106.holiday(i+1)).some(Boolean)"))
  r=J("()=>{addCusto('Tay','loud','block');const c=S.custos[0];const d0=S.day;S.day=10;const su=custoPrice(c);S.day=66;const wi=custoPrice(c);S.day=d0;return [su,wi,CS106.season(10),CS106.season(66)]}")
  ok('weed pays more in summer than winter',r[0]>r[1],r)
  r=J("()=>{const d0=S.day;S.day=10;const a=l96pay('wash');S.day=66;const w=l96pay('wash');S.day=d0;return [a,w]}")
  ok('car wash sells more in summer',r[0]>r[1],r)
  ok('season chip under block name',J("()=>{render();return /Summer|Fall|Winter|Spring/.test(document.getElementById('here').textContent)}"))
  ok('note when season turns',J("()=>{S.day=29;const m=l106day();return !!m&&/here/.test(m.t)}"))
  ok('calendar mode safe',J("()=>{S.cal=1;try{const s=CS106.season();S.cal=0;return !!CS106.SEA[s]}catch(e){S.cal=0;return false}}"))
  J("()=>{for(let i=0;i<10;i++){try{nextDay()}catch(e){window.__e=String(e)}document.getElementById('modal').hidden=true}}");ok('10 days no crash',not J("()=>window.__e||''"))
  ok('no errors',not errs,errs);b.close()
