import os,sys
from PIL import Image,ImageDraw
R='/home/claude/artzip/art-export';O='/home/claude/sheets'
T=150;C=8;RW=5;LH=22
dirs=sys.argv[1:] or sorted(os.listdir(R))
for d in dirs:
    fs=sorted(os.listdir(R+'/'+d))
    for pi in range(0,len(fs),C*RW):
        part=fs[pi:pi+C*RW];rows=(len(part)+C-1)//C
        im=Image.new('RGB',(C*T,rows*(T+LH)),(20,20,24));dr=ImageDraw.Draw(im)
        for i,f in enumerate(part):
            try:
                t=Image.open(f'{R}/{d}/{f}').convert('RGB');w,h=t.size;t.thumbnail((T-4,T-4))
                x=(i%C)*T;y=(i//C)*(T+LH);im.paste(t,(x+(T-t.width)//2,y+(T-t.height)//2))
                dr.text((x+2,y+T),f.rsplit('.',1)[0][:22],fill=(255,255,120));dr.text((x+2,y+T+10),f'{w}x{h}',fill=(150,150,150))
            except Exception as e:dr.text(((i%C)*T,(i//C)*(T+LH)),'ERR '+f[:14],fill=(255,0,0))
        fn=f'{O}/{d}_{pi//(C*RW)}.jpg';im.save(fn,quality=80);print(fn,len(part))
