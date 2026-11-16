# Style B — Be Bold Dark Cinematic: full-bleed dark photo, big white condensed text left, key words yellow, counter, yellow brush CTA
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
W,H=1080,1920; SL=90; SR=930
F='/home/claude/bebold/fonts/package/files/'
OSW=F+'oswald-latin-700-normal.woff'; OSW5=F+'oswald-latin-500-normal.woff'
YEL=(245,197,24)
def cover(src,zoom=1.0,cx=0.5,cy=0.5):
    im=Image.open(src).convert('RGB'); iw,ih=im.size
    cw=min(iw,ih*W/H)/zoom; ch=cw*H/W
    x0=min(max(cx*iw-cw/2,0),iw-cw); y0=min(max(cy*ih-ch/2,0),ih-ch)
    im=im.crop((int(x0),int(y0),int(x0+cw),int(y0+ch))).resize((W,H),Image.LANCZOS)
    g=Image.new('L',(W,H))
    px=g.load()
    for y in range(H):
        for x in range(0,W,8):
            v=int(255*min(0.88,max(0,0.95-x/W*0.9)*max(0.35,1-y/1500)+max(0,(y-1500)/420)*0.6))
            for k in range(8):
                if x+k<W: px[x+k,y]=v
    return Image.composite(Image.new('RGB',(W,H),(0,0,0)),im,g.filter(ImageFilter.GaussianBlur(20)))
def slide(src,text,hl,n,tot,cta=None,zoom=1.0,cx=0.5,cy=0.5,size=104):
    im=cover(src,zoom,cx,cy); d=ImageDraw.Draw(im)
    if tot>1:
        fc=ImageFont.truetype(OSW5,40); c=f'{n}/{tot}'; d.text((SR-d.textlength(c,font=fc),300),c,font=fc,fill=(235,235,235))
    f=ImageFont.truetype(OSW,size); words=text.split(); lines=[]; cur=[]
    for w in words:
        if d.textlength(' '.join(cur+[w]),font=f)<=(SR-SL)*0.78: cur.append(w)
        else: lines.append(cur); cur=[w]
    lines.append(cur); y=380; hlw=set(w.lower().strip('.,?!’\'') for w in hl.split())
    for ln in lines:
        x=SL
        for w in ln:
            col=YEL if w.lower().strip('.,?!’\'') in hlw else (255,255,255)
            d.text((x+4,y+4),w,font=f,fill=(0,0,0)); d.text((x,y),w,font=f,fill=col)
            x+=d.textlength(w+' ',font=f)
        y+=int(size*1.12)
    if cta:
        fb=ImageFont.truetype(OSW,40); lines2=[]; cur=''
        for w in cta.split():
            t=(cur+' '+w).strip()
            if d.textlength(t,font=fb)<=640: cur=t
            else: lines2.append(cur); cur=w
        lines2.append(cur); bh=56*len(lines2)+50; by=1330
        random.seed(3); pts=[(SL-10+random.randint(-6,6),by+random.randint(-8,4))]
        brush=Image.new('L',(W,H)); bd=ImageDraw.Draw(brush)
        bd.rounded_rectangle((SL-14,by,SL+800,by+bh),radius=18,fill=255)
        for k in range(40):
            yy=by+random.randint(0,bh); xx=SL-30+random.randint(0,30); bd.ellipse((xx,yy-12,xx+40,yy+12),fill=255)
        for k in range(40):
            yy=by+random.randint(0,bh); xx=SL+770+random.randint(-20,10); bd.ellipse((xx,yy-12,xx+44,yy+12),fill=255)
        im.paste(Image.new('RGB',(W,H),YEL),(0,0),brush)
        d=ImageDraw.Draw(im)
        bx=SL+20; d.polygon([(bx,by+28),(bx+34,by+28),(bx+34,by+82),(bx+17,by+66),(bx,by+82)],fill=(10,10,10))
        ty=by+25
        for l in lines2: d.text((SL+80,ty),l,font=fb,fill=(10,10,10)); ty+=56
    return im
