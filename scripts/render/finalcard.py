# Last carousel slide: takeaway + CTA on a dark card, matching pages.py (1080x1920).
# python3 finalcard.py out.jpg "line one|line two (gold)" "cta text" [bg_img]
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageEnhance
A = '/home/claude/bebold/fonts/anton/package/files/anton-latin-400-normal.woff2'
F = '/home/claude/bebold/fonts/package/files/oswald-latin-500-normal.woff'
W, H = 1080, 1920
out, take, cta = sys.argv[1:4]; bg = sys.argv[4] if len(sys.argv) > 4 else None
if bg:
    c = ImageOps.fit(Image.open(bg).convert('RGB'), (W, H)).filter(ImageFilter.GaussianBlur(18))
    c = ImageEnhance.Brightness(c).enhance(0.28)
else:
    c = Image.new('RGB', (W, H), (12, 12, 14))
d = ImageDraw.Draw(c); f = ImageFont.truetype(A, 118)
def wrap(t):
    ls, cur = [], ''
    for w in t.split():
        s = (cur + ' ' + w).strip()
        if d.textlength(s, font=f) > 900: ls.append(cur); cur = w
        else: cur = s
    return ls + [cur]
rows = []
for i, part in enumerate(take.split('|')):
    rows += [(ln, (255, 214, 10) if i == len(take.split('|')) - 1 else (245, 240, 230)) for ln in wrap(part)]
    rows.append(None)
rows = rows[:-1]
hgt = sum(132 if r else 50 for r in rows); y = (H - hgt) // 2 - 80
for r in rows:
    if r is None: y += 50; continue
    d.text(((W - d.textlength(r[0], font=f)) / 2, y), r[0], font=f, fill=r[1]); y += 132
g = ImageFont.truetype(F, 46); tw = d.textlength(cta, font=g)
d.rounded_rectangle(((W - tw) / 2 - 30, y + 90, (W + tw) / 2 + 30, y + 170), 14, outline=(255, 214, 10), width=3)
d.text(((W - tw) / 2, y + 100), cta, font=g, fill=(255, 214, 10))
c.save(out, quality=93); print(out)
