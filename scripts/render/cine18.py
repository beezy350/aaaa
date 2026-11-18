import sys,os,glob; sys.path.insert(0,'/home/claude/bebold')
from cine import frame
R='/home/claude/aaaa/bebold/raw/2026-11-18/'
f=lambda k:(glob.glob(R+k+'.*') or [None])[0]
for n,p,t,hl in [('kintsugi','K',"Where you broke is where the gold goes.",('broke','gold')),('foxlion','F',"Be the fox. Then be the lion.",('fox.','lion.'))]:
    os.makedirs(f'out/c18_{n}',exist_ok=True)
    for i in range(4): frame(f(f'{p}{i}'),t if i==0 else None,hl).save(f'out/c18_{n}/slide_{i+1:02d}.jpg',quality=93)
print('ok')
