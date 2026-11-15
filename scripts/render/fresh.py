import sys,os; sys.path.insert(0,'/home/claude/bebold')
import engrave as E, darkb as B
from PIL import Image
R='/home/claude/aaaa/bebold/raw/2026-11-15-fresh/'; K='/home/claude/aaaa/bebold/raw/2026-11-13/'
def save(name,ims):
    os.makedirs(f'out/{name}',exist_ok=True)
    for i,im in enumerate(ims,1): im.save(f'out/{name}/slide_{i:02d}.jpg',quality=92)
    tw,th=300,533; sh=Image.new('RGB',(tw*len(ims)+10*(len(ims)+1),th+20),(20,20,20))
    for i,im in enumerate(ims): sh.paste(im.resize((tw,th)),(10+i*(tw+10),10))
    sh.save(f'out/{name}_preview.jpg',quality=90)
save('2026-11-15_fresh_fakequotes',[
 E.slide(R+'F0.png','3 “STOIC” QUOTES YOU’VE SHARED.','Only one of them is real.',double=True),
 E.slide(R+'F1.jpg','FAKE: THE LION AND THE SHEEP.','Not Marcus Aurelius. It’s Tywin Lannister, from Game of Thrones.'),
 E.slide(R+'F2.jpg','FAKE: “LET YOUR SUCCESS MAKE THE NOISE.”','No ancient source has ever been found for it.'),
 E.slide(R+'F3.jpg','REAL: “BE ONE.”','Stop arguing about what a good man should be. Be one. Meditations, Book 10.'),
 E.slide(R+'F4.jpg','MYTH: STOICS FEEL NOTHING.','Wrong. They wanted joy. They just refused to be ruled by fear and anger.'),
 E.slide(R+'F5.jpg','CHECK BEFORE YOU SHARE.','Which fake one have you posted?','COMMENT BELOW. BE HONEST.'),
])
save('2026-11-16_fresh_handles',[
 E.slide(R+'H0.png','EVERY PROBLEM HAS TWO HANDLES.','Grab the wrong one and you can’t carry it. — Epictetus',double=True),
 E.slide(R+'H1.jpg','THE WRONG HANDLE.','“He wronged me.” Pick it up there and it’s too heavy to lift.'),
 E.slide(R+'H2.jpg','THE RIGHT HANDLE.','“He’s my brother. We grew up together.” Now you can carry it.'),
 E.slide(R+'H3.jpg','TRY IT TODAY.','The rude driver. The late boss. The bad news. Find the handle you can carry.'),
 E.slide(R+'H4.jpg','SAME PROBLEM. DIFFERENT GRIP.','Which handle are you grabbing right now?','TELL ME BELOW.'),
])
save('2026-11-17_fresh_well',[
 B.slide(K+'B0.png','Some people treat you like a well.','well.',1,6),
 B.slide(K+'B1.jpg','Notice who only calls when they need something.','need something.',2,6),
 B.slide(K+'B2.jpg','A well that never says no runs dry.','runs dry.',3,6),
 B.slide(K+'B3.jpg','Boundaries aren’t cruelty. They’re a lid on the well.','lid',4,6),
 B.slide(K+'B4.jpg','Keep the ones who sit with you when you have nothing to give.','nothing to give.',5,6,size=96),
 B.slide(K+'B5.jpg','Give freely. Just not endlessly.','endlessly.',6,6,cta='Save this for the next time someone only calls when they need you.',zoom=1.15,cx=0.62),
])
print('ok')
