import sys,os,glob; sys.path.insert(0,'/home/claude/bebold')
from cine import frame
from PIL import ImageOps
R='/home/claude/aaaa/bebold/raw/2026-11-19/'
f=lambda k:(glob.glob(R+k+'.*') or [None])[0]
for n,p,t,hl,bw in [('heron','H',"Desperate people chase.",('chase',),False),('pascal','P',"Can you sit alone for 10 minutes?",('alone',),False),('janus','J',"Watch who brings you secrets.",('secrets',),True)]:
    os.makedirs(f'out/c19_{n}',exist_ok=True)
    for i in range(2):
        im=frame(f(f'{p}{i}'),t if i==0 else None,hl)
        if bw and i: im=ImageOps.grayscale(im).convert('RGB')
        im.save(f'out/c19_{n}/slide_{i+1:02d}.jpg',quality=93)
print('ok')
