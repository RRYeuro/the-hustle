import re,sys
s=open('/home/claude/the-hustle/index.html',encoding='utf-8').read()
pat=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 8; b=int(sys.argv[3]) if len(sys.argv)>3 else 60; a=int(sys.argv[4]) if len(sys.argv)>4 else 110
ms=list(re.finditer(pat,s));print('==',pat,len(ms))
for m in ms[:n]:print(s.count('\n',0,m.start())+1,':',s[max(0,m.start()-b):m.end()+a].replace('\n','⏎'))
