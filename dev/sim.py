import json,statistics
from playwright.sync_api import sync_playwright
BOT="""([ch,boost,seed])=>{let s0=seed*9301+49297;Math.random=()=>{s0=(s0*9301+49297)%233280;return s0/233280};window.dcReseed=()=>{};
 startLife(ch);const M=document.getElementById('modal');M.hidden=true;window.noL31=1;window.noL27=1;window.FF=false;S.age=19;S.cal=0;S.school='out';S.grounded=0;
 const kn=S.known.slice().sort((a,b)=>({Low:0,Mid:1,Big:2})[PINFO[a].lvl]-({Low:0,Mid:1,Big:2})[PINFO[b].lvl]);let bi=kn[0];S.at=bi;
 const jb=jsBudget;const out={};let busted=0,days=0;
 for(let d=1;d<=35;d++){S._evDay=S.day;M.hidden=true;try{mgOn=false}catch(e){}
  if(S.pr||S.over){busted++;break}
  // move up to a Mid plug once there is cash for an ounce
  if(PINFO[bi].lvl==='Low'&&S.cash>2500){const m=kn.find(i=>PINFO[i].lvl==='Mid');if(m!=null){bi=m;S.at=bi}}
  if(S.heat<60){S.meet={bi,from:bi,how:'spot'};
   let best=null;PINFO[bi].carries.forEach(id=>{const g=G(id),u=l34U(bi,g),bp=plugPrice('buy',g),sp=Math.round(plugPrice('sell',g,true)*1.55);const m=sp-bp;if(!best||m/bp>best.r)best={g,u,bp,sp,r:m/bp}});
   delete S.meet;
   if(best){let bud=jb(bi);if(!boost)bud=bud/(1.5*(1+Math.min(50,Math.max(0,S.rep||0))/100));
    const room=(S.cap-used())/best.g.sp;let q=Math.min(S.cash*0.9/best.bp,bud/best.sp,room);q=Math.floor(q/best.u)*best.u;
    if(q>0){S.cash-=q*best.bp;S.cash+=q*best.sp;S.st.sold=(S.st.sold||0)+q;try{srvTick(q,best.g)}catch(e){}S.rep=(S.rep||0)+1}}}
  try{nextDay()}catch(e){out.err=String(e).slice(0,80);break}M.hidden=true;days++;
  if([7,14,21,35].includes(d))out['d'+d]=Math.round(S.cash)}
 out.heat=S.heat;out.rep=S.rep;out.busted=busted;out.days=days;return out}"""
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();er=[];pg.on('pageerror',lambda e:er.append(str(e)[:160]))
    pg.goto('file:///home/claude/the-hustle/index.html',wait_until='load');pg.wait_for_timeout(1500)
    for ch in ['tank','slick','shade','val','country','lucky']:
        row={}
        for boost in [1,0]:
            rs=[pg.evaluate(BOT,[ch,boost,sd]) for sd in [1,2,3]]
            med=lambda k:int(statistics.median([r.get(k,0) or 0 for r in rs]))
            row['now' if boost else 'old Js']={k:med(k) for k in ['d7','d14','d21','d35','heat','rep']}
            row['busts '+('now' if boost else 'old')]=sum(r['busted'] for r in rs)
        print(ch,json.dumps(row))
    print('errs',er[:4]);b.close()
