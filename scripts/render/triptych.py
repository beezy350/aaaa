# 3 stacked cinematic panels, each with SHOT NAME + yellow emotion tag. python3 triptych.py out.jpg img1 "WIDE ANGLE" "Belonging" img2 ... img3 ...
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
F = '/home/claude/bebold/fonts/package/files/'
W, H = 1080, 1350
out, args = sys.argv[1], sys.argv[2:]
ph = (H - 8) // 3; canvas = Image.new('RGB', (W, H), (255, 255, 255)); d = ImageDraw.Draw(canvas)
lab = ImageFont.truetype(F + 'oswald-latin-600-normal.woff', 40); tag = ImageFont.truetype(F + 'oswald-latin-500-normal.woff', 30)
for i in range(3):
    img, name, emo = args[i * 3:i * 3 + 3]
    p = ImageOps.fit(Image.open(img).convert('RGB'), (W, ph), centering=(0.5, 0.45)); y = i * (ph + 4)
    canvas.paste(p, (0, y))
    d.text((28, y + ph - 112), name.upper(), font=lab, fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
    tw = d.textlength(emo, font=tag); d.rounded_rectangle((26, y + ph - 58, 26 + tw + 22, y + ph - 16), 8, fill=(255, 214, 10))
    d.text((37, y + ph - 56), emo, font=tag, fill=(15, 15, 15))
canvas.save(out, quality=93); print(out)
