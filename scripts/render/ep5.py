src=open('make_slides.py').read().split("os.makedirs('out'")[0]
ns={}; exec(src, ns)
from PIL import Image
import os
R='/home/claude/aaaa/bebold/raw/2026-11-18/'; X=R
ns['IMG'].update({'E0':R+'G0.png','E1':'/home/claude/aaaa/bebold/raw/2026-11-18-fix/G1.jpg','E2':'/home/claude/aaaa/bebold/raw/2026-11-18-fix/G2.jpg','E3':R+'G3.jpg','E4':R+'G4.jpg','E5':R+'G5.jpg'})
ob=ns['base']; ns['base']=lambda k,z,cx,cy,shade=0: ob(k,z,cx,cy,shade=0.9,reach=1250,hold=820)
p2=ns['p2']
ims=[
 p2('E0',1.0,.5,.5,'SILK ROAD WISDOM · EP. 5','THE VILLAGE WAS SHOUTING.','Every rooftop. Every voice. All at him.'),
 p2('E1',1.0,.5,.5,'THE MOCKING','“LOOK AT THAT FOOL.”','A tortoise who thinks he can fly.'),
 p2('E2',1.2,.5,.55,'THE TEST','HE BIT DOWN HARD.','But every word stung.'),
 p2('E3',1.0,.5,.5,'ONE WORD','HE OPENED HIS MOUTH.','Just to answer them.'),
 p2('E4',1.0,.5,.5,'THE FALL','AND THE SKY LET HIM GO.','The geese flew on.'),
 p2('E5',1.0,.5,.5,'THE LESSON','SOME WORDS AREN’T WORTH THE FALL.','The insult cost him nothing. His answer cost him everything.',cta_text='COMMENT ONE WORD'),
]
name='2026-11-18_ep5'; os.makedirs(f'out/{name}',exist_ok=True)
for i,im in enumerate(ims,1):
    im.save(f'out/{name}/slide_{i:02d}.jpg',quality=92); im.crop((0,200,1080,1550)).save(f'out/{name}/ig_slide_{i:02d}.jpg',quality=92)
tw,th=300,533; sh=Image.new('RGB',(tw*6+70,th+20),(20,20,20))
for i,im in enumerate(ims): sh.paste(im.resize((tw,th)),(10+i*(tw+10),10))
sh.save(f'out/{name}_preview.jpg',quality=90); print('ok')
