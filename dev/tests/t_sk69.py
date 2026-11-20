from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and errs.append(m.text));pg.goto('http://127.0.0.1:8765/index.html');pg.wait_for_timeout(1800);J=pg.evaluate
    J("()=>{startLife('lucky');document.getElementById('modal').hidden=true;S.age=20;Math.random=()=>0.5}")
    bi=J("()=>S.known[0]")
    J(f"()=>{{ptxo().n[{bi}]=PTX_MAX;const L=conList();if(L[0])L[0].low=S.day+1;return L.length}}")
    J("()=>{nextDay();document.getElementById('modal').hidden=true}")
    print(J("()=>S.log.slice(0,8).map(l=>l.t).filter(t=>/order again/.test(t))"))
    print(J("()=>S.inbox.slice(0,4).map(m=>m.f+': '+m.t)"))
    print(errs);b.close()
