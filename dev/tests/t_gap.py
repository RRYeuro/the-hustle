import json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':420,'height':860});er=[];pg.on('pageerror',lambda e:er.append(str(e)[:200]));pg.on('console',lambda m:er.append(m.text[:200]) if m.type=='error' and 'sk33' in m.text else None)
    pg.goto('file:///home/claude/the-hustle/index.html',wait_until='load');pg.wait_for_timeout(1800);J=pg.evaluate
    r=J("""()=>{startLife('country');const M=document.getElementById('modal');M.hidden=true;window.noL31=1;window.noL27=1;S.cash=300000;S.clean=300000;S.rep=95;S.en=200;S.robOn=1;S.scamOn=1;S.scam={noto:0,laptop:0,did:{}};const o={};const H=homeBlock();S.at=H;
     const tryA=(n,a,d,chk)=>{const c=S.cash;try{act(a,{dataset:d||{}})}catch(e){o[n]='ERR '+e.message;return}M.hidden=true;o[n]=(S.cash===c&&(!chk||chk()))?'blocked: '+S.log[0].t.slice(0,46):'WENT THROUGH'};
     const tryP=(n,k,id)=>{const c=S.cash;S.at=placeAt(id);try{placeAct(k,id)}catch(e){o[n]='ERR '+e.message;return}M.hidden=true;o[n]=S.cash===c?'blocked: '+S.log[0].t.slice(0,46):'WENT THROUGH';S.at=H};
     tryA('1 stash house 14','szbuy');tryA('2 soldiers 14','hire');tryA('2 workers 14','hirew',{i:'0'});tryA('3 war 14','twgo',{k:'v'});tryA('3 hit 14','ctput',{k:'v'});tryA('4 getaway car 14','gear',{k:'car'});tryA('4 pro pad 14','pad');
     tryA('5 drive out of town 14','cn_walk',{i:'0'},()=>true);tryA('7 informant 14','w4_inf');tryA('8 parent car 14','parcar');tryP('6 lawyer payroll 14','lpay','lawyer');tryP('6 lawyer on call 14','law','lawyer');tryP('9 block party 14','bparty','park');
     S.car=Object.keys(CARS)[0];S.freeMv=S.day;const d0=S.day;act('go',{dataset:{i:String((H+1)%6)}});o['14 kid drive']=(S.day>d0)?'blocked: took the day (walked)':'WENT THROUGH';M.hidden=true;S.at=H;S.car=null;
     // adult
     S.age=25;S.cal=0;S.school='out';S.grounded=0;
     S.at=(placeAt('mall')+1)%6;tryA('10 punch away from mall','punch');S.at=placeAt('mall');const c1=S.cash;act('punch',{dataset:{}});o['10 punch at mall']=(S.cash<c1||!M.hidden)?'works':'did nothing';M.hidden=true;try{mgOn=false}catch(e){}
     S.at=0;tryA('11 trap on other block','trap',{i:'3'},()=>!S.traps[3]);
     S.at=(placeAt('park')+1)%6;const f0=(S.friends||[]).length;S.fmeet=-1;act('fmeet',{dataset:{}});o['12 meet people away from park']=(S.friends||[]).length===f0&&M.hidden?'blocked: '+S.log[0].t.slice(0,40):'WENT THROUGH';M.hidden=true;
     S.at=H;S.ha=1;S.haOK=-1;const X=(H+1)%6;act('goR',{dataset:{i:String(X)}});o['13 rideshare on monitor']=S.at===H?'blocked':'WENT THROUGH';S.at=H;S.bus=S.day+5;act('goB',{dataset:{i:String(X)}});o['13 bus on monitor']=S.at===H?'blocked':'WENT THROUGH';S.at=H;S.ha=0;M.hidden=true;
     S.loot=[{k:'tv',v:900,p:50,d:1,w:'c'}];o['15 fly with loot']=clCarry()?'blocked: '+S.log[0].t.slice(0,40):'WENT THROUGH';S.loot=[];o['15 fly clean']=clCarry()?'still blocked (BAD)':'allowed';
     S.lt={};S.at=placeAt('pawn');openPlace('pawn');const hb=document.querySelector('#mcard [data-pl="lhouse"]');o['16 pawn house no tip']=hb&&hb.disabled?'disabled: '+hb.textContent:'LIT';M.hidden=true;S.lt={house:S.day+2};openPlace('pawn');const hb2=document.querySelector('#mcard [data-pl="lhouse"]');o['16 pawn house with tip']=hb2&&!hb2.disabled?'lit':'disabled (BAD)';M.hidden=true;
     S.at=H;S.car=Object.keys(CARS)[0];S.en=50;const c2=S.cash,d2=S.day;act('goR',{dataset:{i:String(X)}});o['17 ride with a car']=(S.at===X&&c2-S.cash===5&&S.day===d2)?'drove for $5':'paid '+(c2-S.cash)+' day+'+(S.day-d2);
     // adults still can
     S.at=H;S.car=null;const c3=S.cash;act('hire',{dataset:{}});o['adult can hire soldiers']=S.cash<c3?'works':'blocked (BAD?) '+S.log[0].t.slice(0,40);M.hidden=true;
     return o}""")
    bad=0
    for k,v in r.items():
        f=('WENT THROUGH' in v) or ('BAD' in v) or v.startswith('ERR') or v=='LIT' or v=='did nothing'
        bad+=f;print(('FAIL ' if f else 'PASS ')+k+' -> '+v)
    print('errs',er[:4],'fails',bad);b.close()
