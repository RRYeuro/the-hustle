import sys
P='/home/claude/the-hustle/index.html'
def load():return open(P,encoding='utf-8',newline='').read()
def save(s):open(P,'w',encoding='utf-8',newline='').write(s)
def rep(s,a,b,n=1):
    assert s.count(a)==n,(s.count(a),a[:70]);return s.replace(a,b)
SW="<script>if('serviceWorker' in navigator)"
def add_skin(s,code,sid):
    assert ('id="%s"'%sid) not in s,sid
    return rep(s,SW,code+SW)
