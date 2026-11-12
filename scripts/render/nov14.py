import sys,os; sys.path.insert(0,'/home/claude/bebold')
from engrave import *
from PIL import Image
R='/home/claude/aaaa/bebold/raw/2026-11-14/'; X='/home/claude/aaaa/bebold/raw/2026-11-14-redo/'
def save(name,ims):
    os.makedirs(f'out/{name}',exist_ok=True)
    for i,im in enumerate(ims,1):
        im.save(f'out/{name}/slide_{i:02d}.jpg',quality=92); im.crop((0,200,1080,1550)).save(f'out/{name}/ig_slide_{i:02d}.jpg',quality=92)
    tw,th=300,533; sh=Image.new('RGB',(tw*6+70,th+20),(20,20,20))
    for i,im in enumerate(ims): sh.paste(im.resize((tw,th)),(10+i*(tw+10),10))
    sh.save(f'out/{name}_preview.jpg',quality=90)
save('2026-11-14_post1_marcus_ai',[
 slide(R+'M0.png','MARCUS AURELIUS ON LOSING YOUR JOB TO AI.','He ruled Rome through plague and war. His notes still work.',double=True),
 slide(R+'M1.jpg','1. THE MACHINE ISN’T THE PAIN.','He wrote that what hurts is our judgment of a thing, not the thing. Change the story first.'),
 slide('/home/claude/aaaa/bebold/raw/2026-11-14-redo2/M2.jpg','2. MEET TOMORROW WITH TODAY’S TOOLS.','He told himself the future gets the same clear head you use right now. Fear only borrows trouble.'),
 slide(X+'M3.jpg','3. YOU ARE NOT YOUR TITLE.','Even as emperor, he warned himself not to let the role swallow the man.',inset=0.78),
 slide(R+'M4.jpg','4. DO THE WORK ONLY YOU CAN DO.','His morning rule: get up and do the work of a human being. Machines copy tasks. Not character.'),
 slide(R+'M5.jpg','5. CHANGE IS THE RULE.','Nature keeps turning old things into new ones, he wrote. Your job will change. So can you.','WHICH ONE HELPS YOU MOST? COMMENT THE NUMBER.'),
])
print('ok')
