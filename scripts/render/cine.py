# Cinematic Reel frames: clean full-bleed image, dark top fade, hook title on slide 1 only.
from PIL import Image, ImageDraw, ImageFont
F='/home/claude/bebold/fonts/package/files/'
def frame(src, title=None, hl=(), cy=0.5):
    im=Image.open(src).convert('RGB'); w,h=im.size; s=max(1080/w,1920/h)
    im=im.resize((round(w*s),round(h*s)),Image.LANCZOS); W,H=im.size
    y0=int(min(max(cy*H-960,0),H-1920)); im=im.crop(((W-1080)//2,y0,(W-1080)//2+1080,y0+1920))
    g=Image.new('L',(1,1920)); [g.putpixel((0,y),int(200*max(0,1-y/700)**1.6)) for y in range(1920)]
    im=Image.composite(Image.new('RGB',im.size,(0,0,0)),im,g.resize((1080,1920)))
    if title:
        d=ImageDraw.Draw(im); f=ImageFont.truetype(F+'oswald-latin-700-normal.woff',96)
        words=title.split(); lines=[]; cur=''
        for wd in words:
            t=(cur+' '+wd).strip()
            if d.textlength(t,font=f)>900: lines.append(cur); cur=wd
            else: cur=t
        lines.append(cur); y=340
        for ln in lines:
            x=90
            for wd in ln.split():
                col=(245,197,24) if wd.strip('.,’\'').lower() in hl else (255,255,255)
                d.text((x,y),wd,font=f,fill=col,stroke_width=4,stroke_fill=(0,0,0)); x+=d.textlength(wd+' ',font=f)
            y+=118
    return im
