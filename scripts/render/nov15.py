import sys,os; sys.path.insert(0,'/home/claude/bebold')
from engrave import *
from PIL import Image
R='/home/claude/aaaa/bebold/raw/2026-11-15/'
def save(name,ims):
    os.makedirs(f'out/{name}',exist_ok=True)
    for i,im in enumerate(ims,1):
        im.save(f'out/{name}/slide_{i:02d}.jpg',quality=92); im.crop((0,200,1080,1550)).save(f'out/{name}/ig_slide_{i:02d}.jpg',quality=92)
    tw,th=300,533; sh=Image.new('RGB',(tw*6+70,th+20),(20,20,20))
    for i,im in enumerate(ims): sh.paste(im.resize((tw,th)),(10+i*(tw+10),10))
    sh.save(f'out/{name}_preview.jpg',quality=90)
save('2026-11-15_post1_seneca_wealth',[
 slide(R+'S0.png','RICH BUT EMPTY? SENECA KNEW THE FEELING.','One of Rome’s richest men wrote 5 fixes to a friend.',double=True),
 slide(R+'S1.jpg','1. POOR IS WANTING MORE.','The man with too little isn’t poor, he wrote. The man who always craves more is.'),
 slide(R+'S2.jpg','2. PRACTICE BEING POOR.','A few days of plain bread and a rough cloak. The fear of losing it all shrinks fast.'),
 slide(R+'S3.jpg','3. TIME IS THE REAL MONEY.','He called time the only thing that’s truly ours. Spend it like gold.'),
 slide(R+'S4.jpg','4. MAKE MONEY YOUR SERVANT.','For the wise, wealth serves. For the fool, it rules. Which one are you feeding?',inset=0.82),
 slide(R+'S5.jpg','5. PICK A PORT.','No wind helps a sailor who doesn’t know his port. Drive follows direction.','WHICH ONE DO YOU NEED? COMMENT THE NUMBER.'),
])
print('ok')
