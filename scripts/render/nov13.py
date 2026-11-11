import sys,os; sys.path.insert(0,'/home/claude/bebold')
from engrave import *
R='/home/claude/aaaa/bebold/raw/2026-11-13/'
def save(name,ims):
    os.makedirs(f'out/{name}',exist_ok=True)
    for i,im in enumerate(ims,1):
        im.save(f'out/{name}/slide_{i:02d}.jpg',quality=92)
        im.crop((0,200,1080,1550)).save(f'out/{name}/ig_slide_{i:02d}.jpg',quality=92)
    tw,th=300,533; sh=Image.new('RGB',(tw*6+70,th+20),(20,20,20))
    for i,im in enumerate(ims): sh.paste(im.resize((tw,th)),(10+i*(tw+10),10))
    sh.save(f'out/{name}_preview.jpg',quality=90)
if 'p1' in sys.argv:
    save('2026-11-13_post1_pictures',[
     slide(R+'A0.png','5 ANCIENT PICTURES THAT HIT HARDER THAN ADVICE','The Stoics taught with images, not rules.',double=True),
     slide(R+'A1.jpg','1. THE BULL AND THE LION.','A bull learns how strong it is only when the lion shows up. Trouble doesn’t break you. It introduces you.'),
     slide(R+'A2.jpg','2. THE ROCK IN THE SEA.','Waves hit it all day. It doesn’t argue back. It stands, and the water calms around it.'),
     slide(R+'A3.jpg','3. THE OLD MAN’S TREE.','He plants a tree he’ll never sit under. Do work that pays off after you’re gone.'),
     slide(R+'A4.jpg','4. THE SHAKEN BOWL.','When the water shakes, the sun’s reflection breaks. The sun is fine.','CALM THE WATER, NOT THE SKY.'),
     slide(R+'A5.jpg','5. THE ARCHER.','He controls the aim, not the wind. Do your part. Let the result go.','WHICH ONE DO YOU NEED TODAY? COMMENT THE NUMBER.'),
    ])
print('ok')
K='/home/claude/aaaa/bebold/raw/2026-11-13-kalila/'
if 'p2' in sys.argv:
    save('2026-11-13_post2_hare',[
     slide(K+'K0.png','A HARE DESTROYED A LION WITHOUT TOUCHING HIM.','A trick from Kalila and Dimna, told for over 1,200 years.',double=True),
     slide(K+'K1.jpg','THE LION ATE ONE ANIMAL EVERY DAY.','When the hare’s turn came, he showed up late. On purpose.'),
     slide(K+'K2.jpg','THEN HE TOLD A STORY.',None,bubbles=[
        ((0.01,0.02,0.52,0.30),'Another lion stopped me. He says this forest is his.',((0.20,0.27),(0.28,0.28),(0.30,0.42))),
        ((0.54,0.05,0.98,0.27),'Take me to him.',((0.70,0.25),(0.78,0.25),(0.68,0.40)))]),
     slide(K+'K3.jpg','HE LED THE LION TO A WELL.','Down in the water, an angry lion stared back.'),
     slide(K+'K4.jpg','THE LION ATTACKED HIS OWN REFLECTION.','He jumped in and drowned. The hare never lifted a paw.'),
     slide(K+'K5.jpg','THEY AIM YOUR PRIDE.','Manipulators rarely fight you head-on. Before you react, ask who walked you to the well.','SEND THIS TO SOMEONE WHO REACTS FAST.'),
    ])
