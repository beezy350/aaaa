src=open('make_slides.py').read().split("os.makedirs('out'")[0]
ns={}; exec(src, ns)
from PIL import Image
import os
R='/home/claude/aaaa/bebold/raw/2026-11-15/'; X=R
ns['IMG'].update({'E0':R+'G0.png','E1':R+'G1.jpg','E2':R+'G2.jpg','E3':R+'G3.jpg','E4':R+'G4.jpg','E5':R+'G5.jpg'})
ob=ns['base']; ns['base']=lambda k,z,cx,cy,shade=0: ob(k,z,cx,cy,shade=0.9,reach=1250,hold=820)
p2=ns['p2']
ims=[
 p2('E0',1.0,.45,.5,'SILK ROAD WISDOM · EP. 2','THE NET CAUGHT THE GAZELLE.','The fastest of the four friends couldn’t run.'),
 p2('E1',1.0,.5,.5,'THE ALARM','THE CROW SAW IT FROM THE SKY.','He flew straight to the one friend who could help.'),
 p2('E2',1.0,.5,.5,'THE TEETH','THE MOUSE CHEWED THE ROPES.','Small teeth. Big rescue. Again.'),
 p2('E3',1.0,.5,.5,'FREE','THE GAZELLE RAN FREE.','Speed only saved her once the ropes were gone.'),
 p2('E4',1.0,.5,.5,'THE SLOW ONE','BUT THE TORTOISE STAYED BEHIND.','Too slow to run. Too loyal to leave.'),
 p2('E5',1.0,.5,.5,'PART 3 TOMORROW','THE HUNTER TOOK THE TORTOISE.','Now they had to save the slowest of them all.',cta_text='FOLLOW FOR PART 3'),
]
name='2026-11-15_post2_ep2_gazelle'; os.makedirs(f'out/{name}',exist_ok=True)
for i,im in enumerate(ims,1):
    im.save(f'out/{name}/slide_{i:02d}.jpg',quality=92); im.crop((0,200,1080,1550)).save(f'out/{name}/ig_slide_{i:02d}.jpg',quality=92)
tw,th=300,533; sh=Image.new('RGB',(tw*6+70,th+20),(20,20,20))
for i,im in enumerate(ims): sh.paste(im.resize((tw,th)),(10+i*(tw+10),10))
sh.save(f'out/{name}_preview.jpg',quality=90); print('ok')
