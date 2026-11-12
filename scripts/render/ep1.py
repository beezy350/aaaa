src=open('make_slides.py').read().split("os.makedirs('out'")[0]
ns={}; exec(src, ns)
from PIL import Image
import os
R='/home/claude/aaaa/bebold/raw/2026-11-14/'; X='/home/claude/aaaa/bebold/raw/2026-11-14-redo/'
ns['IMG'].update({'E0':X+'E0.png','E1':R+'E1.jpg','E2':R+'E2.jpg','E3':R+'E3.jpg','E4':X+'E4.jpg','E5':R+'E5.jpg'})
ob=ns['base']; ns['base']=lambda k,z,cx,cy,shade=0: ob(k,z,cx,cy,shade=0.9,reach=1250,hold=820)
p2=ns['p2']
ims=[
 p2('E0',1.0,.3,.5,'SILK ROAD WISDOM · EP. 1','A CROW BEGGED A MOUSE TO BE HIS FRIEND.','The mouse had every reason to say no.'),
 p2('E1',1.0,.5,.5,'THE WITNESS','HE SAW THE MOUSE FREE THE DOVES.','The crow wanted a friend like that.'),
 p2('E2',1.0,.5,.5,'THE REFUSAL','THE MOUSE SAID NO.','Crows eat mice. A friendship with your hunter is a trap.'),
 p2('E3',1.0,.5,.4,'THE PROOF','THE CROW REFUSED TO LEAVE.','He stayed at the door until his patience spoke louder than his beak.'),
 p2('E4',1.0,.5,.5,'THE FRIENDSHIP','TRUST WAS EARNED, NOT ASKED FOR.','Soon a tortoise and a gazelle joined them.'),
 p2('E5',1.0,.5,.5,'PART 2 TOMORROW','THEN THE HUNTER CAME BACK.','And this time, his net caught one of them.',cta_text='FOLLOW FOR PART 2'),
]
name='2026-11-14_post2_ep1_crow'; os.makedirs(f'out/{name}',exist_ok=True)
for i,im in enumerate(ims,1):
    im.save(f'out/{name}/slide_{i:02d}.jpg',quality=92); im.crop((0,200,1080,1550)).save(f'out/{name}/ig_slide_{i:02d}.jpg',quality=92)
tw,th=300,533; sh=Image.new('RGB',(tw*6+70,th+20),(20,20,20))
for i,im in enumerate(ims): sh.paste(im.resize((tw,th)),(10+i*(tw+10),10))
sh.save(f'out/{name}_preview.jpg',quality=90); print('ok')
