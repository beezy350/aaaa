# Ink-wash trait carousel slides (TikTok Format B), 1080x1920.
# Painting on top fading into rice paper, title BELOW the picture, small Roman numeral label above the title.
# python3 inkcards.py <out_dir> <spec.json>
# spec: [{"img": path, "label": "I · THE ANT", "title": "Save in summer.", "red": "summer.", "sub": "Winter always comes."}, ...]
import sys, json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
W, H = 1080, 1920
F = '/home/claude/bebold/fonts/'
SERIF_B = F + 'libre-baskerville/package/files/libre-baskerville-latin-700-normal.woff2'
SERIF_I = F + 'libre-baskerville/package/files/libre-baskerville-latin-400-italic.woff2'
SANS = F + 'package/files/oswald-latin-500-normal.woff'
INK, RED, SOFT = (28, 22, 18), (168, 28, 22), (95, 80, 66)
out, spec = sys.argv[1], json.load(open(sys.argv[2]))
os.makedirs(out, exist_ok=True)

def paper():
    rng = np.random.default_rng(3)
    base = np.ones((H, W, 3), np.float32) * np.array([232, 222, 200], np.float32)
    n = rng.normal(0, 1, (H // 4, W // 4)).astype(np.float32)
    n = np.array(Image.fromarray(((n + 3) * 40).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6)), np.float32) / 255 - 0.5
    fib = rng.normal(0, 1, (H, W)).astype(np.float32) * 4
    yy, xx = np.mgrid[0:H, 0:W]
    vig = 1 - 0.18 * (((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2) * 4
    img = (base + n[..., None] * 26 + fib[..., None]) * vig[..., None]
    return Image.fromarray(img.clip(0, 255).astype(np.uint8))
PAPER = paper()

def ink_layer(src, box_h=1180, top=150):
    im = ImageOps.fit(Image.open(src).convert('RGB'), (W, box_h))
    # multiply onto paper so the painting's own paper tone blends in; feather all edges
    a = np.asarray(im, np.float32) / 255
    a = a / np.maximum(a.reshape(-1, 3).mean(0) * 0 + np.percentile(a.reshape(-1, 3), 97, axis=0), 1e-3)
    a = a.clip(0, 1)
    m = Image.new('L', (W, box_h), 0); d = ImageDraw.Draw(m); d.rectangle((60, 60, W - 60, box_h - 120), fill=255)
    m = np.asarray(m.filter(ImageFilter.GaussianBlur(70)), np.float32) / 255
    return a, m, top

def font(p, s): return ImageFont.truetype(p, s)

def wrap(d, text, f, maxw):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) > maxw and cur: lines.append(cur); cur = w
        else: cur = t
    return lines + [cur]

for i, s in enumerate(spec):
    c = np.asarray(PAPER, np.float32).copy() / 255
    a, m, top = ink_layer(s['img'], s.get('box_h', 1180), s.get('top', 150))
    region = c[top:top + a.shape[0]]
    region[:] = region * (1 - m[..., None]) + region * a * m[..., None]
    img = Image.fromarray((c * 255).clip(0, 255).astype(np.uint8)); d = ImageDraw.Draw(img)
    y = top + a.shape[0] - 70
    if s.get('label'):
        f = font(SANS, 34); t = s['label']; tw = d.textlength(t, font=f)
        d.text(((W - tw) / 2, y), t, font=f, fill=RED); y += 64
        d.line(((W / 2 - 40, y), (W / 2 + 40, y)), fill=SOFT, width=2); y += 28
    size = s.get('size', 84 if len(s['title']) < 34 else 70)
    f = font(SERIF_B, size)
    for ln in wrap(d, s['title'], f, 900):
        words = ln.split(); tw = d.textlength(ln, font=f); x = (W - tw) / 2
        for wd in words:
            col = RED if wd.strip('.,!?') in [r.strip('.,!?') for r in s.get('red', '').split()] else INK
            d.text((x, y), wd, font=f, fill=col); x += d.textlength(wd + ' ', font=f)
        y += int(size * 1.25)
    if s.get('sub'):
        f = font(SERIF_I, 44); y += 14
        for ln in wrap(d, s['sub'], f, 860):
            tw = d.textlength(ln, font=f); d.text(((W - tw) / 2, y), ln, font=f, fill=SOFT); y += 62
    # small brand mark, bottom center
    f = font(SANS, 30); t = 'B E   B O L D'; tw = d.textlength(t, font=f)
    d.rectangle(((W - tw) / 2 - 22, 1786, (W + tw) / 2 + 22, 1838), outline=RED, width=3)
    d.text(((W - tw) / 2, 1792), t, font=f, fill=RED)
    img.save(f'{out}/slide_{i + 1:02d}.jpg', quality=93)
print('done', len(spec))
