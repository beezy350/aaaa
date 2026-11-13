src=open('make_slides.py').read().split("os.makedirs('out'")[0]
ns={}; exec(src, ns)
from PIL import Image
import os
R='/home/claude/aaaa/bebold/raw/2026-11-16/'; X='/home/claude/aaaa/bebold/raw/2026-11-16-redo/'
ns['IMG'].update({'E0':R+'T0.png','E1':R+'T1.jpg','E2':R+'T2.jpg','E3':X+'T3.jpg','E4':R+'T4.jpg','E5':X+'T5.jpg'})
ob=ns['base']; ns['base']=lambda k,z,cx,cy,shade=0: ob(k,z,cx,cy,shade=0.9,reach=1250,hold=820)
p2=ns['p2']
ims=[
 p2('E0',1.0,.4,.5,'SILK ROAD WISDOM · EP. 3','THE FRIENDS MADE A PLAN.','The hunter had the tortoise. They had each other.'),
 p2('E1',1.0,.5,.5,'THE BAIT','THE GAZELLE PLAYED DEAD.','She lay on the hunter’s path, still as stone.'),
 p2('E2',1.0,.5,.5,'THE ACT','THE CROW PRETENDED TO FEED ON HER.','Perfect theater for a greedy eye.'),
 p2('E3',1.0,.5,.5,'THE SWITCH','THE HUNTER DROPPED THE TORTOISE.','Why carry a tortoise when a gazelle lies free?'),
 p2('E4',1.0,.5,.5,'THE TEETH','THE MOUSE CHEWED THE SACK OPEN.','The gazelle jumped up and ran. The hunter got nothing.'),
 p2('E5',1.0,.5,.5,'THE LESSON','FOUR WEAK ANIMALS. ONE STRONG TEAM.','Who’s in your four?',cta_text='FOLLOW FOR EP. 4'),
]
name='2026-11-16_post2_ep3_rescue'; os.makedirs(f'out/{name}',exist_ok=True)
for i,im in enumerate(ims,1):
    im.save(f'out/{name}/slide_{i:02d}.jpg',quality=92); im.crop((0,200,1080,1550)).save(f'out/{name}/ig_slide_{i:02d}.jpg',quality=92)
tw,th=300,533; sh=Image.new('RGB',(tw*6+70,th+20),(20,20,20))
for i,im in enumerate(ims): sh.paste(im.resize((tw,th)),(10+i*(tw+10),10))
sh.save(f'out/{name}_preview.jpg',quality=90); print('ok')
