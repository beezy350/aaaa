# Animated 3-panel pages: each slide reveals one more panel; a page holds 3 panels.
# python3 pages.py <out_dir> <hook text> <json spec>   spec = [[img, title, tag], ...] (multiples of 3) + optional final full image
import sys, json, os
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
F = '/home/claude/bebold/fonts/package/files/'; A = '/home/claude/bebold/fonts/anton/package/files/anton-latin-400-normal.woff'
W, H = 1080, 1920; TOP, BOT, GAP = 200, 1500, 6
PH = (BOT - TOP - 2 * GAP) // 3
out, hook, spec, final = sys.argv[1], sys.argv[2], json.loads(sys.argv[3]), (sys.argv[4] if len(sys.argv) > 4 else None)
os.makedirs(out, exist_ok=True)
lab = ImageFont.truetype(F + 'oswald-latin-600-normal.woff', 42); tag = ImageFont.truetype(F + 'oswald-latin-500-normal.woff', 30)
def panel(img, title, t):
    p = ImageOps.fit(Image.open(img).convert('RGB'), (W, PH), centering=(0.5, 0.5)); d = ImageDraw.Draw(p)
    sh = Image.new('L', (W, PH), 0); ImageDraw.Draw(sh).rectangle((0, PH - 150, W, PH), fill=150); sh = sh.filter(ImageFilter.GaussianBlur(40))
    p = Image.composite(Image.new('RGB', p.size, (0, 0, 0)), p, sh); d = ImageDraw.Draw(p)
    d.text((30, PH - 118), title.upper(), font=lab, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
    tw = d.textlength(t, font=tag); d.rounded_rectangle((28, PH - 60, 28 + tw + 24, PH - 16), 8, fill=(255, 214, 10)); d.text((40, PH - 58), t, font=tag, fill=(15, 15, 15))
    return p
n = 0
for pg in range(len(spec) // 3):
    panels = [panel(*spec[pg * 3 + k]) for k in range(3)]
    for shown in range(1, 4):
        c = Image.new('RGB', (W, H), (10, 10, 12)); d = ImageDraw.Draw(c)
        for k in range(3):
            y = TOP + k * (PH + GAP)
            if k < shown: c.paste(panels[k], (0, y))
            else: d.rectangle((0, y, W, y + PH), fill=(18, 18, 22))
        if pg == 0 and shown == 1 and hook:     # scroll-stopper in the empty slots
            f = ImageFont.truetype(A, 104); words = hook.split(); lines, cur = [], ''
            for w in words:
                tst = (cur + ' ' + w).strip()
                if d.textlength(tst, font=f) > 960: lines.append(cur); cur = w
                else: cur = tst
            lines.append(cur); y0 = TOP + PH + GAP + (2 * PH - len(lines) * 118) // 2
            for i, ln in enumerate(lines):
                col = (255, 214, 10) if i == len(lines) - 1 else (255, 255, 255)
                d.text(((W - d.textlength(ln, font=f)) / 2, y0 + i * 118), ln, font=f, fill=col)
        n += 1; c.save(f'{out}/slide_{n:02d}.jpg', quality=93)
if final:
    n += 1; ImageOps.fit(Image.open(final).convert('RGB'), (W, H), centering=(0.5, 0.5)).save(f'{out}/slide_{n:02d}.jpg', quality=93)
print(n, 'slides')
