src=open('make_slides.py').read().split("os.makedirs('out'")[0]
ns={}; exec(src, ns)
from PIL import Image
import os
R='/home/claude/aaaa/bebold/raw/2026-11-17/'; X=R
ns['IMG'].update({'E0':R+'Q0.png','E1':R+'Q1.jpg','E2':R+'Q1.jpg','E3':R+'Q3.jpg','E4':R+'Q4.jpg','E5':R+'Q2.jpg'})
ob=ns['base']; ns['base']=lambda k,z,cx,cy,shade=0: ob(k,z,cx,cy,shade=0.9,reach=1250,hold=820)
p2=ns['p2']
ims=[
 p2('E0',1.0,.4,.5,'SILK ROAD WISDOM · EP. 4','THE POND WAS DRYING UP.','A tortoise was about to lose his home.'),
 p2('E1',1.0,.45,.5,'THE PLAN','TWO GEESE HAD AN IDEA.','Bite this stick. We’ll fly you to a new lake.'),
 p2('E2',1.35,.62,.62,'THE RULE','DON’T OPEN YOUR MOUTH.','Not once. Not for anything.'),
 p2('E3',1.0,.5,.5,'THE FLIGHT','AND THEY FLEW.','A tortoise in the sky. It was actually working.'),
 p2('E4',1.0,.5,.5,'THE CROWD','THEN THE VILLAGE LOOKED UP.','People pointed. Laughed. Shouted at him.'),
 p2('E5',1.0,.45,.5,'PART 5 TOMORROW','AND THE TORTOISE HAD SOMETHING TO SAY.','What would you have done?',cta_text='FOLLOW FOR PART 5'),
]
name='2026-11-17_post2_ep4_tortoise'; os.makedirs(f'out/{name}',exist_ok=True)
for i,im in enumerate(ims,1):
    im.save(f'out/{name}/slide_{i:02d}.jpg',quality=92); im.crop((0,200,1080,1550)).save(f'out/{name}/ig_slide_{i:02d}.jpg',quality=92)
tw,th=300,533; sh=Image.new('RGB',(tw*6+70,th+20),(20,20,20))
for i,im in enumerate(ims): sh.paste(im.resize((tw,th)),(10+i*(tw+10),10))
sh.save(f'out/{name}_preview.jpg',quality=90); print('ok')
