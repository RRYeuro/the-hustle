import sys,json,random,subprocess,time
from playwright.sync_api import sync_playwright
N=int(sys.argv[1]) if len(sys.argv)>1 else 1500
srv=subprocess.Popen(['python3','-I','-m','http.server','8765','-d','/home/claude/the-hustle'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
errs={};inv={}
def add(d,k,ctx):
    d.setdefault(k,[0,ctx]);d[k][0]+=1
CHK="""()=>{const b=[];if(!window.S||!S)return b;const n=x=>typeof x==='number'&&isFinite(x);
if(!n(S.cash))b.push('cash NaN');else if(S.cash<-1)b.push('cash negative');if(S.clean!=null&&!n(S.clean))b.push('clean NaN');if(n(S.clean)&&S.clean>S.cash+1&&S.cash>=0)b.push('clean > cash');
if(!n(S.heat)||S.heat<0||S.heat>100.5)b.push('heat range '+S.heat);if(!n(S.hp))b.push('hp NaN');if(!n(S.rep))b.push('rep NaN');if(!n(S.day))b.push('day NaN');if(S.safe!=null&&(!n(S.safe)||S.safe<0))b.push('safe bad');
try{GOODS.forEach(g=>{if(!n(S.inv[g.id])||S.inv[g.id]<0)b.push('inv '+g.id+' '+S.inv[g.id]);if(S.fake[g.id]>S.inv[g.id])b.push('fake>inv '+g.id)})}catch(e){}
if(n(S.cap)&&S.cap<0)b.push('cap negative');if(S.en!=null&&!n(S.en))b.push('en NaN');if(n(S.stress)&&(S.stress<0||S.stress>100.5))b.push('stress range');
(window._secErr||[]).forEach(x=>b.push('section: '+x));window._secErr=[];
const t=document.body.innerText;if(/\\bNaN\\b|undefined|\\[object Object\\]/.test(t)){const m=/.{0,50}(\\bNaN\\b|undefined|\\[object Object\\]).{0,30}/.exec(t);b.push('text: '+(m?m[0].replace(/\\s+/g,' '):''))}
return b}"""
STEP="""(r)=>{const m=document.getElementById('modal');const vis=e=>e&&e.offsetParent&&!e.disabled;
const ctx=()=>{const h=document.querySelector('#mcard h2');return (h?h.textContent:'')+'|'+(typeof tab!=='undefined'?tab:'')};
if(!m.hidden){const bs=[...document.querySelectorAll('#mcard button,#mcard [data-a],#mcard [data-pl]')].filter(vis).filter(b=>!/backup|export|import|reset|delete|discord|share|new game|quit|menu/i.test(b.textContent));
 if(!bs.length){window._st=(window._st||0)+1;if(window._st>25){window._st=0;const c=ctx();try{mgOn=false}catch(e){}m.hidden=true;return 'STUCK '+c}return ctx()}
 window._st=0;const b=bs[Math.floor(r*bs.length)];const c=ctx()+'>'+b.textContent.trim().slice(0,30);b.click();return c}
window._st=0;const bs=[...document.querySelectorAll('[data-a],[data-t],.tabs button,.dock button,[data-p],[data-app],button')].filter(vis).filter(b=>!b.closest('#modal')&&b.id!=='devbtn'&&!/backup|export|import|reset|delete|discord|share|new game|quit|menu|how to play/i.test(b.textContent+(b.getAttribute('aria-label')||'')));
if(!bs.length)return 'NOBTN';const b=bs[Math.floor(r*bs.length)];const c=ctx()+'>'+(b.dataset.a||'')+':'+b.textContent.trim().slice(0,30);b.click();return c}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for ch,age,seed in [('lucky',19,1),('tank',22,2),('slick',16,3),('shade',25,4)]:
        random.seed(seed);pg=b.new_page(viewport={'width':420,'height':860});last=['']
        pg.on('pageerror',lambda e:add(errs,str(e)[:160],last[0]))
        pg.on('console',lambda m:add(errs,'console: '+m.text[:160],last[0]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
        pg.on('dialog',lambda d:d.dismiss())
        pg.goto('http://localhost:8765/index.html',wait_until='load');pg.wait_for_timeout(800)
        pg.evaluate("([c,a])=>{localStorage.clear();startLife(c);document.getElementById('modal').hidden=true;S.age=a;if(a>=18){S.cal=0;S.school='out'}S.cash=20000;S.clean=8000;S.bag=1;S.robOn=1;S.pad=1;try{S.known=[0,1,2,3,4,5];for(let i=0;i<6;i++)S.trust[i]=60}catch(e){}window.confirm=()=>false;window.prompt=()=>null;window.alert=()=>{};window.open=()=>null;render()}",[ch,age])
        for i in range(N):
            try:
                last[0]=pg.evaluate(STEP,random.random())
                if last[0].startswith('STUCK'):add(inv,'stuck popup (no buttons 25 steps)',last[0])
                if i%7==0:
                    for x in pg.evaluate(CHK):add(inv,x,last[0])
                if i%60==59:pg.evaluate("()=>{if(S.over){startLife(S.char);document.getElementById('modal').hidden=true;S.age=19;S.cal=0;S.school='out';S.cash=20000;S.clean=8000;render()}if(S.hp<30)S.hp=100;S.en=100}")
                pg.wait_for_timeout(15)
            except Exception as e:
                add(errs,'driver: '+str(e)[:120],last[0]);pg.wait_for_timeout(200)
        pg.close()
    b.close()
srv.terminate()
print('== ERRORS');[print(v[0],'x',k,' @',v[1][:90]) for k,v in sorted(errs.items(),key=lambda x:-x[1][0])[:40]]
print('== INVARIANTS');[print(v[0],'x',k,' @',v[1][:90]) for k,v in sorted(inv.items(),key=lambda x:-x[1][0])[:40]]
