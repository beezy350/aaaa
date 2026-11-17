import sys,os,glob; sys.path.insert(0,'/home/claude/bebold')
from cine import frame
R='/home/claude/aaaa/bebold/raw/2026-11-17-cine/'
def f(k): return (glob.glob(R+k+'.*') or [None])[0]
P={'snake':('T1',"Stop wearing who you used to be.",('stop','used')),
   'stags':('T2',"In an ego war, nobody wins.",('ego','nobody')),
   'pearl':('I1',"Keep your plans in the dark.",('dark.','dark')),
   'oars':('I2',"Nobody is coming to row for you.",('nobody','row'))}
for n,(p,t,hl) in P.items():
    os.makedirs(f'out/cine_{n}',exist_ok=True)
    for i in range(4):
        frame(f(f'{p}_{i}'),t if i==0 else None,hl).save(f'out/cine_{n}/slide_{i+1:02d}.jpg',quality=93)
print('ok')
