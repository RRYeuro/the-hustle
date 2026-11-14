import sys,hashlib,io,json
from PIL import Image
def borders(im,axis):
    g=im.convert('L');W,H=g.size;px=g.load()
    if axis=='x':
        cols=[]
        for x in range(W):
            d=sum(1 for y in range(int(H*.1),int(H*.45),2) if px[x,y]<70)
            cols.append(d/len(range(int(H*.1),int(H*.45),2)))
        return cols
    rows=[]
    for y in range(H):
        d=sum(1 for x in range(int(W*.1),int(W*.45),2) if px[x,y]<70)
        rows.append(d/len(range(int(W*.1),int(W*.45),2)))
    return rows
def runs(v,th=.8):
    out=[];i=0
    while i<len(v):
        if v[i]>=th:
            j=i
            while j<len(v) and v[j]>=th:j+=1
            out.append((i,j));i=j
        else:i+=1
    return out
def panels(path):
    im=Image.open(path).convert('RGB');W,H=im.size
    cx=runs(borders(im,'x'));cy=runs(borders(im,'y'))
    # inner edges: borders near left, middle, right
    def pick(rs,L):
        lefts=[r for r in rs if r[1]<L*.2];mids=[r for r in rs if L*.35<r[0]<L*.65];rights=[r for r in rs if r[0]>L*.8]
        a=lefts[-1][1] if lefts else int(L*.02);m1=mids[0][0] if mids else L//2-6;m2=mids[-1][1] if mids else L//2+6;b=rights[0][0] if rights else int(L*.98)
        return a,m1,m2,b
    x0,x1,x2,x3=pick(cx,W);y0,y1,y2,y3=pick(cy,H)
    boxes=[(x0,y0,x1,y1),(x2,y0,x3,y1),(x0,y2,x1,y3),(x2,y2,x3,y3)]
    return im,boxes
def face(im,box,size=160):
    x0,y0,x1,y1=box;w=x1-x0;h=y1-y0;s=min(w,h);cx=(x0+x1)//2
    sq=im.crop((cx-s//2,y0,cx+s//2,y0+s)).resize((size,size),Image.LANCZOS);return sq
if __name__=='__main__':
    im,b=panels(sys.argv[1]);print(b)
