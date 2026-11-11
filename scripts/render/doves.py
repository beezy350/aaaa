src=open('make_slides.py').read().split("os.makedirs('out'")[0]
ns={}; exec(src, ns)
from PIL import Image
import os
R='/home/claude/aaaa/bebold/raw/2026-11-13-doves/'
ns['IMG'].update({'R0':R+'R0.png',**{f'R{i}':R+f'R{i}.jpg' for i in range(1,6)}})
ob=ns['base']; ns['base']=lambda k,z,cx,cy,shade=0: ob(k,z,cx,cy,shade=0.9,reach=1150 if k=='R0' else 1250,hold=600 if k=='R0' else 820)
p2=ns['p2']
ims=[
 p2('R0',1.2,.5,.3,'KALILA AND DIMNA','A FLOCK OF DOVES STOLE A HUNTER’S NET.','While they were trapped inside it.'),
 p2('R1',1.0,.5,.5,'THE TRAP','THEY LANDED FOR FREE GRAIN.','Then the net dropped.'),
 p2('R2',1.0,.5,.5,'THE PANIC','EVERY DOVE PULLED ITS OWN WAY.','The harder they fought alone, the tighter it held.'),
 p2('R3',1.0,.5,.5,'THE TURN','THEIR LEADER SAID: PULL TOGETHER.','They rose as one, and the net rose with them.'),
 p2('R4',1.0,.5,.5,'THE FRIEND','A MOUSE CHEWED THEM FREE.','The leader made him free the others first. Herself last.'),
 p2('R5',1.0,.5,.5,'THE LESSON','ALONE, IT’S A TRAP. TOGETHER, IT’S CARGO.','Who would you lift the net with?',cta_text='SEND THIS TO YOUR PEOPLE'),
]
name='2026-11-13_post2_doves'; os.makedirs(f'out/{name}',exist_ok=True)
for i,im in enumerate(ims,1):
    im.save(f'out/{name}/slide_{i:02d}.jpg',quality=92); im.crop((0,200,1080,1550)).save(f'out/{name}/ig_slide_{i:02d}.jpg',quality=92)
tw,th=300,533; sh=Image.new('RGB',(tw*6+70,th+20),(20,20,20))
for i,im in enumerate(ims): sh.paste(im.resize((tw,th)),(10+i*(tw+10),10))
sh.save(f'out/{name}_preview.jpg',quality=90); print('ok')
