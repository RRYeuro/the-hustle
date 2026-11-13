# moves embedded pictures out of index.html into art/ so the page opens fast. Safe to run again.
import re,hashlib,base64,os,json
R='/home/claude/the-hustle';p=R+'/index.html'
s=open(p,encoding='utf-8',newline='').read()
os.makedirs(R+'/art',exist_ok=True);n=0
def f(m):
    global n
    mt,d=m.group(1),m.group(2)
    if not mt.startswith('image/') or len(d)<3000:return m.group(0)
    raw=base64.b64decode(d);ext={'image/jpeg':'jpg','image/png':'png','image/webp':'webp'}.get(mt,'img')
    fn='art/'+hashlib.sha1(raw).hexdigest()[:12]+'.'+ext
    if not os.path.exists(R+'/'+fn):open(R+'/'+fn,'wb').write(raw)
    n+=1;return fn
s2=re.sub(r'data:([a-z]+/[a-z0-9+.-]+);base64,([A-Za-z0-9+/=]+)',f,s)
used=sorted(set(re.findall(r'art/[0-9a-f]{12}\.[a-z]+',s2)))
for x in os.listdir(R+'/art'):
    if x!='list.json' and 'art/'+x not in used:os.remove(R+'/art/'+x)
json.dump(used,open(R+'/art/list.json','w'))
if s2!=s:open(p,'w',encoding='utf-8',newline='').write(s2)
print('moved',n,'pictures; art files',len(used),'; index.html',round(len(s2.encode())/1e6,2),'MB')
