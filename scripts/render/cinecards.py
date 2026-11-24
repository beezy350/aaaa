# Full-frame cinematic TikTok carousel slides (default TikTok format), 1080x1920.
# python3 cinecards.py <out_dir> <spec.json>
# spec: [{"img": path, "text": "Line on the slide.", "hl": ["word"], "hook": true, "cy": 0.5, "kicker": "1737"}, ...]
import sys, json, os
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
W, H = 1080, 1920
F = '/home/claude/bebold/fonts/'
ANTON = F + 'anton/package/files/anton-latin-400-normal.woff2'
OSW = F + 'package/files/oswald-latin-500-normal.woff'
GOLD, WHITE = (255, 205, 60), (248, 244, 236)
out, spec = sys.argv[1], json.load(open(sys.argv[2])); os.makedirs(out, exist_ok=True)

def grad(img, top, bottom):
    g = Image.new('L', (1, H))
    for y in range(H):
        a = 0
        if y < top[0]: a = top[1] * (1 - y / top[0]) ** 1.5
        if y > H - bottom[0]: a = max(a, bottom[1] * ((y - (H - bottom[0])) / bottom[0]) ** 1.3)
        g.putpixel((0, y), int(a))
    return Image.composite(Image.new('RGB', (W, H), (0, 0, 0)), img, g.resize((W, H)))

def wrap(d, text, f, maxw):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) > maxw and cur: lines.append(cur); cur = w
        else: cur = t
    return lines + [cur]

n = len(spec)
for i, s in enumerate(spec):
    im = Image.open(s['img']).convert('RGB'); w, h = im.size; sc = max(W / w, H / h)
    im = im.resize((round(w * sc), round(h * sc)), Image.LANCZOS)
    y0 = int(min(max(s.get('cy', 0.5) * im.height - H / 2, 0), im.height - H)); x0 = (im.width - W) // 2
    im = im.crop((x0, y0, x0 + W, y0 + H))
    hook = s.get('hook', False)
    im = grad(im, (760, 210) if hook else (380, 120), (1000, 235))
    d = ImageDraw.Draw(im)
    size = s.get('size', 112 if hook else 84); f = ImageFont.truetype(ANTON, size)
    lines = wrap(d, s['text'].upper() if hook else s['text'], f, 900)
    lh = int(size * 1.18)
    y = s.get('ty', 330) if hook else 1500 - lh * len(lines)
    if s.get('kicker'):
        k = ImageFont.truetype(OSW, 40); d.text((90, y - 66), s['kicker'].upper(), font=k, fill=GOLD)
    hl = [x.lower() for x in s.get('hl', [])]
    for ln in lines:
        x = 90
        for wd in ln.split():
            col = GOLD if wd.strip('.,!?:;"\'').lower() in hl else WHITE
            d.text((x, y), wd, font=f, fill=col, stroke_width=3, stroke_fill=(0, 0, 0)); x += d.textlength(wd + ' ', font=f)
        y += lh
    # slide counter, small, top-right inside safe zone
    c = ImageFont.truetype(OSW, 34); t = f'{i + 1}/{n + 1}'
    d.text((W - 150 - d.textlength(t, font=c), 250), t, font=c, fill=(230, 230, 230))
    im.save(f'{out}/slide_{i + 1:02d}.jpg', quality=93)
print('done', n)
