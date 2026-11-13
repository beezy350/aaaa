import sys,os; sys.path.insert(0,'/home/claude/bebold')
from engrave import *
from PIL import Image
R='/home/claude/aaaa/bebold/raw/2026-11-17/'
def save(name,ims):
    os.makedirs(f'out/{name}',exist_ok=True)
    for i,im in enumerate(ims,1):
        im.save(f'out/{name}/slide_{i:02d}.jpg',quality=92); im.crop((0,200,1080,1550)).save(f'out/{name}/ig_slide_{i:02d}.jpg',quality=92)
    tw,th=300,533; sh=Image.new('RGB',(tw*6+70,th+20),(20,20,20))
    for i,im in enumerate(ims): sh.paste(im.resize((tw,th)),(10+i*(tw+10),10))
    sh.save(f'out/{name}_preview.jpg',quality=90)
save('2026-11-17_post1_seneca_fear',[
 slide(R+'W0.png','PLANNING OR WORRYING?','Seneca’s test, written to a friend scared of the future.',double=True),
 slide(R+'W1.jpg','1. FEAR IS BIGGER THAN LIFE.','More things scare us than actually hurt us. We suffer more in imagination than in reality.'),
 slide(R+'W2.jpg','2. IS IT HAPPENING NOW?','If not, it’s a story. Treat it like one until there’s evidence.'),
 slide(R+'W3.jpg','3. PLANNING HAS A PEN.','Worry has a loop. Writing steps? You’re planning. Replaying fears? Stop.'),
 slide(R+'W4.jpg','4. PREPARE ONCE.','Look at the worst case squarely. Get ready for it. Then stop rehearsing it.',inset=0.84),
 slide(R+'W5.jpg','5. DON’T SUFFER EARLY.','Don’t be miserable before the crisis shows up. It may never come.','SAVE THIS FOR YOUR NEXT 3 A.M. SPIRAL.'),
])
print('ok')
