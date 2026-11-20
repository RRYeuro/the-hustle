# Rebuilds dev/code-map.md from index.html: features grouped by game area, what each wraps, hot spots. Run by deploy.sh.
import re,collections
R='/home/claude/the-hustle';s=open(R+'/index.html',encoding='utf-8').read()
AREAS=[('Phone & texts',r'panePhone|phoneMsg|_mth|_rph|_MC\b|S\.inbox|mth-'),('Plugs & buying',r'PINFO|plugDrop|plug|ptxo|connect'),
('Crew, workers & runners',r'S\.workers|w5b|runner|crew'),('Licks & heists',r'lick|heist|LICKS|safeGame|chop'),
('Money, bills & business',r'S\.clean|bills|paneExp|paneBiz|biz|laund'),('Map, places & moving',r'openPlace|fm26|paneMove|BLOCKS\[|realty'),
('School, age & life',r'paneSchool|school|teenStart|gAge|S\.age'),('Rap & social',r'\bR\.fat|rap|follow'),('Law, heat & beef',r'busted|raid|heat|court|beef'),
('Look, layout & art',r'classList|style|\.png|art/')]
sk=re.findall(r'<script id="(skin\d+)js">(.*?)</script>',s,re.S)
by=collections.defaultdict(list);wr=collections.defaultdict(list)
for n,b in sk:
    w=sorted(set(re.findall(r'(?<![\w.$])([A-Za-z_$][\w$]*)\s*=\s*function\b',b)))
    for f in w:wr[f].append(n)
    note=re.search(r'/\*\s*(.{5,140}?)\*/',b);note=note.group(1).strip() if note else ''
    sc=[(len(re.findall(p,b)),a) for a,p in AREAS];area=max(sc)[1] if max(sc)[0] else 'Other'
    by[area].append((n,len(b)//1000,', '.join(w) or '-',note))
o=['# Code map (rebuilt automatically on every deploy by tools/codemap.py)','',
'index.html = the main game code, then each feature as a `<script id="skinNjs">` block, loaded in number order. Later features run on top of earlier ones. All feature styles live in one `<style id="game-css">` block, marked per feature.','',
'Feature source copies: dev/skins/. Tests: dev/tests/ (crash test: dev/tests/t_fuzz.py).','']
for a,_ in AREAS+[('Other','')]:
    if a not in by:continue
    o+=[f'## {a}','','| Feature | Size | Wraps | Note |','|---|---|---|---|']
    o+=[f'| {n} | {k}k | {w} | {t} |' for n,k,w,t in sorted(by[a],key=lambda x:int(x[0][4:]))]+['']
o+=['## Functions wrapped by 4+ features (change these carefully)','']
o+=[f'- {f} ({len(v)}): {", ".join(v)}' for f,v in sorted(wr.items(),key=lambda x:-len(x[1])) if len(v)>=4]
open(R+'/dev/code-map.md','w').write('\n'.join(o)+'\n');print('code map:',len(sk),'features')
