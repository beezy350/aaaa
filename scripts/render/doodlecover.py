# Scroll-stopper cover frame for doodle Reels: big exaggerated doodle + handwritten hook on paper.
# python3 doodlecover.py out.png doodle.png "LINE ONE" "LINE TWO (red)" [sticker]
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FD = '/home/claude/bebold/fonts/node_modules/@fontsource/'
W, H = 1080, 1920
out, src, l1, l2 = sys.argv[1:5]; sticker = sys.argv[5] if len(sys.argv) > 5 else None
c = Image.new('RGB', (W, H), (250, 248, 242)); d = ImageDraw.Draw(c)
rng = np.random.default_rng(1)
for _ in range(1400):  # faint paper speckle
    x, y = rng.integers(0, W), rng.integers(0, H); d.point((x, y), fill=(232, 228, 218))
im = Image.open(src).convert('RGB')
a = np.asarray(im).astype(np.float32); m = (a.mean(2) < 240).astype(np.uint8) * 255
mask = Image.fromarray(m).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(2))
s = 1000 / max(im.size); im = im.resize((int(im.width * s), int(im.height * s))); mask = mask.resize(im.size)
c.paste(im, ((W - im.width) // 2, 640), mask)
f1 = ImageFont.truetype(FD + 'caveat/files/caveat-latin-700-normal.woff', 132)
f2 = ImageFont.truetype(FD + 'caveat/files/caveat-latin-700-normal.woff', 150)
for txt, f, y, col in [(l1, f1, 300, (25, 25, 25)), (l2, f2, 450, (214, 40, 40))]:
    tw = d.textlength(txt, font=f); d.text(((W - tw) / 2, y), txt, font=f, fill=col)
# scribbled underline under line two
tw = d.textlength(l2, font=f2); x0 = (W - tw) / 2
pts = [(x0 + i * tw / 30, 625 + 6 * np.sin(i * 1.3)) for i in range(31)]
d.line(pts, fill=(214, 40, 40), width=8, joint='curve')
if sticker:
    fs = ImageFont.truetype(FD + 'patrick-hand/files/patrick-hand-latin-400-normal.woff', 56)
    tw = d.textlength(sticker, font=fs)
    d.rounded_rectangle((W - tw - 170, 1560, W - 110, 1650), 20, fill=(255, 214, 10), outline=(25, 25, 25), width=4)
    d.text((W - tw - 140, 1572), sticker, font=fs, fill=(25, 25, 25))
c.save(out); print(out)
