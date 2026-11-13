import sys,os; sys.path.insert(0,'/home/claude/bebold')
from engrave import *
from PIL import Image
R='/home/claude/aaaa/bebold/raw/2026-11-16/'
def save(name,ims):
    os.makedirs(f'out/{name}',exist_ok=True)
    for i,im in enumerate(ims,1):
        im.save(f'out/{name}/slide_{i:02d}.jpg',quality=92); im.crop((0,200,1080,1550)).save(f'out/{name}/ig_slide_{i:02d}.jpg',quality=92)
    tw,th=300,533; sh=Image.new('RGB',(tw*6+70,th+20),(20,20,20))
    for i,im in enumerate(ims): sh.paste(im.resize((tw,th)),(10+i*(tw+10),10))
    sh.save(f'out/{name}_preview.jpg',quality=90)
save('2026-11-16_post1_nietzsche',[
 slide(R+'N0.png','NIETZSCHE VS. THE STOICS.','He thought they were fooling themselves. Was he right?',double=True),
 slide(R+'N1.jpg','THE STOIC CLAIM.','Live in agreement with nature. Nature is rational, so be rational too.'),
 slide(R+'N2.jpg','NIETZSCHE’S ATTACK.','Nature is wasteful and indifferent, he wrote. You’re not reading its rules. You’re painting yours onto it.',inset=0.84),
 slide(R+'N3.jpg','HIS DEEPER POINT.','Every philosophy builds the world in its own image. The Stoics did too.'),
 slide(R+'N4.jpg','THE STOIC REPLY.','Fine, call it a choice, not a law of nature. Choosing calm still beats being thrown around by every storm.'),
 slide(R+'N5.jpg','YOU DECIDE.','Was Nietzsche right, or is calm worth choosing anyway?','COMMENT: NIETZSCHE OR THE STOICS?'),
])
print('ok')
