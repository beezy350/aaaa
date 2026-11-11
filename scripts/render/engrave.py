# Style A — Vintage Engraving renderer (cream paper, framed illustration, condensed serif caps)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
W,H=1080,1920
F='/home/claude/bebold/fonts/'
HEAD=F+'package/files/playfair-display-latin-900-normal.woff'
BODY=F+'libre-baskerville/package/files/libre-baskerville-latin-400-normal.woff'
BODYB=F+'libre-baskerville/package/files/libre-baskerville-latin-700-normal.woff'
INK=(22,20,18); CREAM=(240,232,214)
SQ=0.74   # horizontal squeeze -> condensed newspaper look
def paper():
    random.seed(7)
    im=Image.new('RGB',(W,H),CREAM)
    n=Image.effect_noise((W,H),18).convert('L').filter(ImageFilter.GaussianBlur(1.2))
    tint=Image.new('RGB',(W,H),(214,200,172))
    im=Image.composite(tint,im,n.point(lambda v:int(max(0,v-118)*0.9)))
    # soft warm vignette
    v=Image.new('L',(W,H),0); d=ImageDraw.Draw(v)
    d.rectangle((0,0,W,H),fill=60); d.rectangle((60,60,W-60,H-60),fill=0)
    v=v.filter(ImageFilter.GaussianBlur(90))
    return Image.composite(Image.new('RGB',(W,H),(205,188,156)),im,v)
def cond_lines(text,size,maxw):
    f=ImageFont.truetype(HEAD,size); d=ImageDraw.Draw(Image.new('L',(1,1)))
    words=text.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)*SQ<=maxw: cur=t
        else: lines.append(cur); cur=w
    lines.append(cur); return f,lines
def headline(im,y,text,size=118,maxw=880,gap=0.98):
    f,lines=cond_lines(text,size,maxw)
    for ln in lines:
        d=ImageDraw.Draw(Image.new('L',(1,1))); tw=int(d.textlength(ln,font=f))+10
        L=Image.new('L',(tw,int(size*1.3)),0); ImageDraw.Draw(L).text((5,0),ln,font=f,fill=255)
        L=L.resize((int(tw*SQ),L.height),Image.LANCZOS)
        im.paste(Image.new('RGB',L.size,INK),((W-L.width)//2,y),L)
        y+=int(size*gap)
    return y
def body(im,y,text,size=46,bold=False,maxw=860,gap=1.38):
    f=ImageFont.truetype(BODYB if bold else BODY,size); d=ImageDraw.Draw(im)
    for para in text.split('\n'):
        words=para.split(); cur=''; lines=[]
        for w in words:
            t=(cur+' '+w).strip()
            if d.textlength(t,font=f)<=maxw: cur=t
            else: lines.append(cur); cur=w
        lines.append(cur)
        for ln in lines:
            d.text(((W-d.textlength(ln,font=f))/2,y),ln,font=f,fill=INK); y+=int(size*gap)
    return y
def framed(im,src,y,size=780,double=False):
    art=Image.open(src).convert('RGB')
    s=int(min(art.size)*0.9); art=art.crop(((art.width-s)//2,(art.height-s)//2,(art.width+s)//2,(art.height+s)//2)).resize((size,size),Image.LANCZOS)
    # blend white paper of the art into our cream
    art=Image.blend(art,Image.new('RGB',art.size,CREAM),0.06)
    x=(W-size)//2; im.paste(art,(x,y))
    d=ImageDraw.Draw(im); d.rectangle((x-2,y-2,x+size+2,y+size+2),outline=INK,width=3)
    if double: d.rectangle((x-12,y-12,x+size+12,y+size+12),outline=INK,width=2)
    return (x,y,size)
def bubble(im,box,text,tail,size=34):
    d=ImageDraw.Draw(im); f=ImageFont.truetype(BODY,size)
    x0,y0,x1,y1=box
    d.polygon([tail[0],tail[1],tail[2]],fill=(250,246,236),outline=INK)
    d.ellipse(box,fill=(250,246,236),outline=INK,width=3)
    d.polygon([tail[0],tail[1],tail[2]],fill=(250,246,236))
    d.line([tail[0],tail[2]],fill=INK,width=3); d.line([tail[1],tail[2]],fill=INK,width=3)
    words=text.split(); lines=[]; cur=''; mw=(x1-x0)*0.76
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)<=mw: cur=t
        else: lines.append(cur); cur=w
    lines.append(cur); lh=int(size*1.25); ty=(y0+y1)/2-lh*len(lines)/2
    for ln in lines:
        d.text(((x0+x1)/2-d.textlength(ln,font=f)/2,ty),ln,font=f,fill=INK); ty+=lh
def slide(src,head,txt=None,last=None,hsize=128,double=False,bubbles=None):
    im=paper(); y=330
    hs=hsize if len(cond_lines(head,hsize,880)[1])<=2 else 112
    y=headline(im,y,head,hs)
    y+=48
    if txt: y=body(im,y,txt)
    if last: y=body(im,y+6,last,size=40,bold=True)
    fy=max(y+36,700); fsz=min(860,1580-fy)
    x,fy,fsz=framed(im,src,fy,fsz,double)
    if bubbles:
        for (bx0,by0,bx1,by1),t,(t1,t2,t3) in bubbles:
            P=lambda a,b:(int(x+a*fsz),int(fy+b*fsz))
            bubble(im,(*P(bx0,by0),*P(bx1,by1)),t,[P(*t1),P(*t2),P(*t3)])
    return im
