src=open('make_slides.py').read().split("os.makedirs('out'")[0]
ns={}; exec(src, ns)
from PIL import Image
import os
R='/home/claude/aaaa/bebold/raw/2026-11-20/'; X=R
ns['IMG'].update({'E0':R+'E0.png','E1':'/home/claude/aaaa/bebold/raw/2026-11-20-fix/E1.jpg','E2':'/home/claude/aaaa/bebold/raw/2026-11-20-fix/E2.jpg','E3':'/home/claude/aaaa/bebold/raw/2026-11-20-fix/E3.jpg','E4':R+'E4.jpg','E5':'/home/claude/aaaa/bebold/raw/2026-11-20-fix/E5.jpg'})
ob=ns['base']; ns['base']=lambda k,z,cx,cy,shade=0: ob(k,z,cx,cy,shade=0.9,reach=1250,hold=820)
p2=ns['p2']
ims=[
 p2('E0',1.0,.5,.5,'SILK ROAD WISDOM · EP. 7','THE MOUSE WALKED UP TO THE CAT.','His oldest enemy. Trapped.'),
 p2('E1',1.0,.5,.5,'THE DEAL','“FIRST, YOU PROTECT ME.”','Then I chew through your net.'),
 p2('E2',1.0,.5,.5,'THE SHELTER','UNDER THE PAW OF HIS ENEMY.','The owl and the weasel gave up.'),
 p2('E3',1.0,.5,.5,'THE WORK','HE CHEWED. SLOWLY.','Very slowly.'),
 p2('E4',1.0,.5,.5,'THE TENSION','“HURRY,” THE CAT HISSED.','One rope stayed uncut.'),
 p2('E5',1.0,.5,.5,'FINALE TOMORROW','AT DAWN, THE HUNTER CAME.','Why was the mouse waiting?',cta_text='FOLLOW FOR THE FINALE'),
]
name='2026-11-20_ep7'; os.makedirs(f'out/{name}',exist_ok=True)
for i,im in enumerate(ims,1):
    im.save(f'out/{name}/slide_{i:02d}.jpg',quality=92); im.crop((0,200,1080,1550)).save(f'out/{name}/ig_slide_{i:02d}.jpg',quality=92)
tw,th=300,533; sh=Image.new('RGB',(tw*6+70,th+20),(20,20,20))
for i,im in enumerate(ims): sh.paste(im.resize((tw,th)),(10+i*(tw+10),10))
sh.save(f'out/{name}_preview.jpg',quality=90); print('ok')
