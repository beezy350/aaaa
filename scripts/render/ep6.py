src=open('make_slides.py').read().split("os.makedirs('out'")[0]
ns={}; exec(src, ns)
from PIL import Image
import os
R='/home/claude/aaaa/bebold/raw/2026-11-19/'; X=R
ns['IMG'].update({'E0':R+'C0.png','E1':R+'C1.jpg','E2':R+'C2.jpg','E3':'/home/claude/aaaa/bebold/raw/2026-11-19-fix/C3.jpg','E4':R+'C4.jpg','E5':R+'C5.jpg'})
ob=ns['base']; ns['base']=lambda k,z,cx,cy,shade=0: ob(k,z,cx,cy,shade=0.9,reach=1250,hold=820)
p2=ns['p2']
ims=[
 p2('E0',1.0,.5,.5,'SILK ROAD WISDOM · EP. 6','A CAT WAS CAUGHT IN A NET.','A new story begins.'),
 p2('E1',1.0,.5,.55,'THE MOUSE','HE CAME OUT FOR FOOD.','Small. Hungry. Unaware.'),
 p2('E2',1.0,.5,.5,'BEHIND HIM','A WEASEL WAS CREEPING CLOSER.','Then he froze.'),
 p2('E3',1.0,.5,.5,'ABOVE HIM','AN OWL WAS WATCHING.','From the tree. Waiting.'),
 p2('E4',1.15,.5,.55,'NO WAY OUT','DANGER BEHIND. DANGER ABOVE.','And in front of him, his oldest enemy. Trapped.'),
 p2('E5',1.0,.5,.5,'PART 7 TOMORROW','HE MADE A CHOICE NO MOUSE EVER MADE.','What would you do?',cta_text='FOLLOW FOR PART 7'),
]
name='2026-11-19_ep6'; os.makedirs(f'out/{name}',exist_ok=True)
for i,im in enumerate(ims,1):
    im.save(f'out/{name}/slide_{i:02d}.jpg',quality=92); im.crop((0,200,1080,1550)).save(f'out/{name}/ig_slide_{i:02d}.jpg',quality=92)
tw,th=300,533; sh=Image.new('RGB',(tw*6+70,th+20),(20,20,20))
for i,im in enumerate(ims): sh.paste(im.resize((tw,th)),(10+i*(tw+10),10))
sh.save(f'out/{name}_preview.jpg',quality=90); print('ok')
