import subprocess,sys
R='/home/claude/the-hustle'
s=subprocess.run(['git','-C',R,'show','HEAD:index.html'],capture_output=True).stdout.decode('utf-8')
if 'id="skin27js"' in s: sys.exit('HEAD already has skin27; build from the pre-skin27 commit')
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:60])
    s=s.replace(a,b)
# car: half the cars are push to start (Sort)
rep("if(k==='car')return hotwireGame(ok=>{","if(k==='car')return (window.l27Car?(f=>l27Car(hotwireGame,f)):hotwireGame)(ok=>{")
# store: alarm panel first, back-room safe after
rep("if(k==='store')return seqGame(ok=>{","if(k==='store'){const _go=()=>seqGame(ok=>{")
rep("return lickDone('Register emptied',`You moved too fast for him. Walked out with ${money(pay)}.`,true)}",
    "const _f=x=>lickDone('Register emptied',`You moved too fast for him. Walked out with ${money(pay)}.`+(x||''),true);return window.l27StoreSafe?l27StoreSafe(_f,t=>alarmRun('Alarm tripped',t,'You got away','Out the door with the register money.')):_f()}")
rep("lickDone('Clerk had a bat',`You froze up and he came over the counter. −${dmg} health.`,false)});\n  if(k==='house'){let inv=false;",
    "lickDone('Clerk had a bat',`You froze up and he came over the counter. −${dmg} health.`,false)});return window.l27Store?l27Store(_go,()=>{S.heat=Math.min(100,S.heat+10);alarmRun('Alarm tripped','You crossed the wrong wire and the panel started screaming before you got inside.','You got away','Empty handed, but free.')}):_go()}\n  if(k==='house'){let inv=false;")
# pharmacy: locked cabinet
rep("lickDone('Cleaned out the shelves',`You grabbed ${got} bags. That's ${pa} Percs and ${pb} Xans, pharm grade.${pa+pb<a+b2?' Your stash was too full for the rest.':''}`,true)},{T:7000",
    "const _f=x=>lickDone('Cleaned out the shelves',`You grabbed ${got} bags. That's ${pa} Percs and ${pb} Xans, pharm grade.${pa+pb<a+b2?' Your stash was too full for the rest.':''}`+(x||''),true);return window.l27Pharm?l27Pharm(_f,t=>alarmRun('Alarm tripped',t,'You got away','Out the door with what you grabbed.')):_f()},{T:7000")
# scam lick: his phone
rep("return lickDone('He came with the bread',`He fell for every word. Buyer showed up with ${money(pay)} and you took it.`,true)}",
    "const _f=x=>lickDone('He came with the bread',`He fell for every word. Buyer showed up with ${money(pay)} and you took it.`+(x||''),true);return window.l27Scam?l27Scam(_f):_f()}")
# house: alarm panel, real loot, safe
rep("if(woke)return alarmRun('Somebody\\'s home','A floorboard creaked and the lights came on. They\\'re calling 911.','You got away','Over the back fence and gone.');",
    "if(woke&&window._l27al){window._l27al=0;return alarmRun('Alarm tripped','You fumbled the alarm panel and it started screaming. Somebody called it in.','You got away','Over the back fence and gone.')}if(woke)return alarmRun('Somebody\\'s home','A floorboard creaked and the lights came on. They\\'re calling 911.','You got away','Over the back fence and gone.');")
rep("const sneak=()=>{cut('door','');sneakGame(run)};",
    "const sneak=()=>{cut('door','');const _go=()=>sneakGame(run);if(window.l27Alarm)return l27Alarm(_go,()=>{window._l27al=1;run(0,true)});_go()};")
rep("cash(400,2500,'jewelry box (pawn)');if(Math.random()<.5)cash(200,900,'a game system and a TV (pawn)');","")
rep("cash(500,1800,'$V in wallets, phones and a watch')","cash(200,700,'$V in wallets')")
rep("    if(type==='empty'){S.heat=Math.min(100,S.heat+6)","    try{if(type!=='empty')l27House(L,type,inv)}catch(e){console.error('l27',e)}\n    if(type==='empty'){S.heat=Math.min(100,S.heat+6)")
rep("lickDone(take.length?'Clean lick':'Empty handed',`${list}${take.length<L.length?` You left ${L.length-take.length} thing${L.length-take.length===1?'':'s'} behind.`:' Cleaned it out.'}`,take.length>0)},",
    "const _f=x=>lickDone(take.length||x?'Clean lick':'Empty handed',`${list}${take.length<L.length?` You left ${L.length-take.length} thing${L.length-take.length===1?'':'s'} behind.`:' Cleaned it out.'}${x||''}`,take.length>0||!!x);if(window.l27Safe)return l27Safe(type,inv,_f,t=>alarmRun('Safe alarm',`${list} ${t}`,'You got away','Over the back fence with the bag.'));_f('')},")
sk=open('/home/claude/tools/skin27.html',encoding='utf-8').read()
rep("<script>if('serviceWorker' in navigator)",sk+"<script>if('serviceWorker' in navigator)")
open(R+'/index.html','w',encoding='utf-8',newline='').write(s)
print('built',len(s))
