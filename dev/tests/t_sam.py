from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();er=[];pg.on('pageerror',lambda e:er.append(str(e)[:200]))
    pg.goto('file:///home/claude/the-hustle/index.html',wait_until='load');pg.wait_for_timeout(1500)
    r=pg.evaluate("()=>{startLife('lucky');document.getElementById('modal').hidden=true;return [mHe({name:'Sam'},'he'),mHe({name:'Sam'},'His'),wHer({name:'Sam'}),!!faceOf('Sam','c')]}")
    print(r,er);print('PASS' if r==['she','Her',True,True] and not er else 'FAIL','Sam is a she everywhere and has a face')
    b.close()
