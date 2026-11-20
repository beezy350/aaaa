#!/usr/bin/env python3
"""Kinetic typography Reel: 'What stands in the way becomes the way.' (Marcus Aurelius, Meditations 5.20)
usage: kinetic.py <voice_dir> <music.mp3> <out.mp4>
Voice dir holds s1_1.wav .. s7_1.wav (one sentence each, B2)."""
import sys, os, subprocess, tempfile, math, random, wave
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

VOICE, MUSIC, OUT = sys.argv[1:4]
W, H, FPS = 1080, 1920, 30
TEMPO = float(os.environ.get('TEMPO', '0.9'))
F = '/home/claude/bebold/fonts/'
ANTON = F + 'anton/package/files/anton-latin-400-normal.woff2'
SERIF = F + 'libre-baskerville/package/files/libre-baskerville-latin-400-italic.woff2'
INK = (240, 234, 222, 255)
GOLD = (255, 205, 60, 255)
DIM = (240, 234, 222, 90)
LINES = ["You keep waiting for the road to clear.", "It won't.",
         "Marcus Aurelius wrote it two thousand years ago.",
         "What stands in the way becomes the way.",
         "The wall is not the end of the path.", "The wall is the path.", "So climb."]
GAPS = [0.55, 0.75, 0.6, 0.95, 0.45, 0.8]
LEAD, TAIL = 0.45, 1.6
tmp = tempfile.mkdtemp()

# ---------------- audio: tempo, trim, timeline, word timings ----------------
def load(p):
    o = f'{tmp}/{os.path.basename(p)}'
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', p, '-filter:a', f'atempo={TEMPO}', '-ar', '24000', '-ac', '1', o], check=True)
    with wave.open(o) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    env = np.convolve(np.abs(a), np.ones(480) / 480, 'same')
    on = np.where(env > env.max() * 0.06)[0]
    a = a[max(0, on[0] - 600): on[-1] + 1800]
    return a

clips = [load(f'{VOICE}/s{i+1}_1.wav') for i in range(7)]
SR = 24000
starts, t = [], LEAD
for i, c in enumerate(clips):
    starts.append(t)
    t += len(c) / SR + (GAPS[i] if i < 6 else 0)
DUR = t + TAIL
voice = np.zeros(int(DUR * SR) + SR, np.float32)
for s, c in zip(starts, clips):
    voice[int(s * SR): int(s * SR) + len(c)] += c
voice = voice[:int(DUR * SR)]
with wave.open(f'{tmp}/voice.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(voice, -1, 1) * 32767).astype(np.int16).tobytes())

def word_times(i):
    """distribute words over the voiced part of the clip, weighted by syllable-ish length"""
    words = LINES[i].split()
    c = clips[i]; d = len(c) / SR
    env = np.convolve(np.abs(c), np.ones(480) / 480, 'same')
    act = np.where(env > env.max() * 0.08)[0]
    a0, a1 = act[0] / SR, act[-1] / SR
    wt = [len(w.strip('.,')) + 2 for w in words]
    tot = sum(wt); out, acc = [], a0
    for x in wt:
        out.append(starts[i] + acc - 0.06)
        acc += (a1 - a0) * x / tot
    return out
WT = [word_times(i) for i in range(7)]
SC = starts + [DUR]   # scene boundaries (scene i shown from SC[i] to SC[i+1])

# ---------------- drawing helpers ----------------
_fc, _sc = {}, {}
def font(p, s):
    k = (p, s)
    if k not in _fc: _fc[k] = ImageFont.truetype(p, s)
    return _fc[k]

def sprite(txt, fp, size, col):
    k = (txt, fp, size, col)
    if k not in _sc:
        f = font(fp, size); b = f.getbbox(txt)
        im = Image.new('RGBA', (b[2] - b[0] + 20, b[3] - b[1] + 20), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((10 - b[0], 10 - b[1]), txt, font=f, fill=col)
        _sc[k] = im
    return _sc[k]

def put(L, im, cx, cy, sc=1.0, a=1.0, rot=0, anchor='c'):
    if a <= 0.003 or sc <= 0.01: return
    if sc != 1.0: im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BICUBIC)
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    if a < 1:
        al = im.getchannel('A').point(lambda v: int(v * a)); im = im.copy(); im.putalpha(al)
    x = int(cx - (im.width / 2 if anchor == 'c' else 10 * sc)); y = int(cy - im.height / 2)
    L.alpha_composite(im, (x, y)) if 0 <= x and 0 <= y and x + im.width <= W and y + im.height <= H else L.paste(im, (x, y), im)

def cl(x): return max(0.0, min(1.0, x))
def eo(x): x = cl(x); return 1 - (1 - x) ** 3
def ex(x): x = cl(x); return 1 if x >= 1 else 1 - 2 ** (-10 * x)
def back(x, s=1.9): x = cl(x) - 1; return 1 + (s + 1) * x ** 3 + s * x ** 2
def bounce(x):
    x = cl(x)
    if x < 1 / 2.75: return 7.5625 * x * x
    if x < 2 / 2.75: x -= 1.5 / 2.75; return 7.5625 * x * x + .75
    if x < 2.5 / 2.75: x -= 2.25 / 2.75; return 7.5625 * x * x + .9375
    x -= 2.625 / 2.75; return 7.5625 * x * x + .984375

def new(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))

# ---------------- scenes ----------------
def s1(t):  # words drop into a left-aligned stack
    L = new(); w = WT[0]
    rows = [(['YOU', 'KEEP'], 640), (['WAITING', 'FOR'], 820), (['THE', 'ROAD'], 1000), (['TO', 'CLEAR.'], 1180)]
    k = 0
    for words, y in rows:
        x = 110
        for wd in words:
            col = GOLD if wd == 'ROAD' else INK
            sp = sprite(wd, ANTON, 165, col); p = (t - w[k]) / 0.32
            if p > 0:
                put(L, sp, x, y - 70 * (1 - eo(p)), back(p) * 0.25 + 0.75 if p < 1 else 1, cl(p * 2.5), anchor='l')
            x += sp.width + 18; k += 1
    return L

def s2(t):  # slam
    L = new(); w = WT[1]
    p0 = (t - w[0]) / 0.2; p1 = (t - w[1]) / 0.22
    put(L, sprite('IT', ANTON, 210, INK), 540, 760, 1 + 1.4 * (1 - ex(p0)), cl(p0 * 3))
    put(L, sprite("WON'T.", ANTON, 360, GOLD), 540, 1060, 1 + 1.8 * (1 - ex(p1)), cl(p1 * 3))
    return L

def s3(t):  # typewriter serif + counter
    L = new(); w = WT[2]
    line1 = 'Marcus Aurelius'; line2 = 'wrote it'
    n = int(cl((t - w[0]) / max(0.3, w[3] - w[0] + 0.25)) * (len(line1) + len(line2)))
    put(L, sprite(line1[:min(n, len(line1))] or ' ', SERIF, 84, INK), 110, 620, anchor='l')
    if n > len(line1): put(L, sprite(line2[:n - len(line1)], SERIF, 84, INK), 110, 730, anchor='l')
    pc = (t - w[4]) / max(0.4, w[6] - w[4] + 0.1)
    if pc > 0:
        v = int(round(2000 * eo(pc) / 10) * 10)
        put(L, sprite(f'{v:,}', ANTON, 360, GOLD), 110, 1010, 0.85 + 0.15 * eo(pc * 2), cl(pc * 4), anchor='l')
    pa = (t - w[6]) / 0.3
    if pa > 0: put(L, sprite('YEARS AGO.', ANTON, 130, INK), 120 + 60 * (1 - eo(pa)), 1250, 1, cl(pa * 2), anchor='l')
    return L

def s4(t):  # key line: everything dims, THE WAY rises
    L = new(); w = WT[3]
    pd = eo((t - w[6]) / 0.35)
    k = 0
    for words, y in [(['WHAT', 'STANDS'], 600), (['IN', 'THE', 'WAY'], 770)]:
        x = 110
        for wd in words:
            col = INK if pd < 0.5 else DIM
            sp = sprite(wd, ANTON, 150, col); p = (t - w[k]) / 0.28
            if p > 0: put(L, sp, x + 120 * (1 - eo(p)), y, 1, cl(p * 3) * (1 - 0.55 * pd), anchor='l')
            x += sp.width + 16; k += 1
    pb = (t - w[5]) / 0.35
    if pb > 0: put(L, sprite('becomes', SERIF, 90, INK), 540, 960, 1, cl(pb * 2))
    pw = (t - w[6]) / 0.5
    if pw > 0:
        put(L, sprite('THE WAY.', ANTON, 300, GOLD), 540, 1210 + 120 * (1 - eo(pw)), 0.7 + 0.3 * back(pw, 1.3), cl(pw * 3))
    return L

BRICKS = [('THE', 0, 0), ('WALL', 1, 0), ('IS', 2, 0), ('NOT', 0, 1), ('THE', 1, 1), ('END', 2, 1), ('OF', 0, 2), ('THE', 1, 2), ('PATH', 2, 2)]
BW, BH = 300, 160
def wall_layer(t, drop=True):
    L = new(); d = ImageDraw.Draw(L); w = WT[4]
    for k, (wd, c, r) in enumerate(BRICKS):
        p = (t - w[k]) / 0.45 if drop else 1
        if p <= 0: continue
        x0 = 540 - 1.5 * BW + c * BW + (BW / 2 if r == 1 else 0) - (BW / 4)
        y0 = 1240 - r * BH - (1 - bounce(p)) * 700
        d.rectangle([x0 + 6, y0 + 6, x0 + BW - 6, y0 + BH - 6], fill=(34, 32, 30, 255), outline=(120, 110, 95, 255), width=4)
        col = GOLD if wd in ('WALL', 'PATH') else INK
        sp = sprite(wd, ANTON, 96, col)
        L.alpha_composite(sp, (int(x0 + BW / 2 - sp.width / 2), int(y0 + BH / 2 - sp.height / 2)))
    return L

def s5(t): return wall_layer(t)

def s6(t):  # the wall falls backward and becomes a floor/path
    w = WT[5]; p = eo((t - w[0]) / 0.75)
    L = np.array(wall_layer(t, drop=False))
    top, bot = 1240 - 2 * BH + 6, 1240 + BH
    src = np.float32([[40, top], [W - 40, top], [W - 40, bot], [40, bot]])
    ny = top + (bot - 230 - top) * p          # top edge sinks toward the floor
    inset = 330 * p                           # and narrows into perspective
    dst = np.float32([[40 + inset, ny], [W - 40 - inset, ny], [W - 40 + 60 * p, bot + 120 * p], [40 - 60 * p, bot + 120 * p]])
    M = cv2.getPerspectiveTransform(src, dst)
    L = Image.fromarray(cv2.warpPerspective(L, M, (W, H), flags=cv2.INTER_LINEAR))
    for k, (txt, y, col) in enumerate([('THE WALL', 640, INK), ('IS THE PATH.', 830, GOLD)]):
        pk = (t - w[k * 3]) / 0.35
        if pk > 0: put(L, sprite(txt, ANTON, 175, col), 540, y + 50 * (1 - eo(pk)), 1, cl(pk * 2.5))
    return L

def s7(t):  # SO ... CLIMB letters as stairs
    L = new(); w = WT[6]
    put(L, sprite('so', SERIF, 100, INK), 200, 700, 1, cl((t - w[0]) / 0.3))
    x = 150
    for k, ch in enumerate('CLIMB'):
        sp = sprite(ch, ANTON, 260, GOLD if ch != '.' else INK)
        p = (t - w[1] - k * 0.09) / 0.35
        y = 1350 - k * 95
        if p > 0: put(L, sp, x, y + 90 * (1 - back(p, 1.6)), 1, cl(p * 3), anchor='l')
        x += sp.width - 8
    return L

SCENES = [s1, s2, s3, s4, s5, s6, s7]
# exit transition of scene i into i+1: (kind, seconds)
EXITS = ['push_up', 'zoom_through', 'slide_left', 'shrink', None, 'push_up']
TR = 0.32

def transform(L, kind, p):
    """p: 0..1 exit progress for outgoing (returns image, alpha)"""
    a = 1 - eo(p)
    if kind == 'push_up': return L, (0, -int(H * 0.5 * eo(p))), 1.0, a
    if kind == 'zoom_through': return L, (0, 0), 1 + 2.2 * ex(p), a
    if kind == 'slide_left': return L, (-int(W * eo(p)), 0), 1.0, 1.0
    if kind == 'shrink': return L, (0, 0), 1 - 0.15 * eo(p), a
    return L, (0, 0), 1, a

def comp(base, L, off=(0, 0), sc=1.0, a=1.0, blur=0):
    if sc != 1.0:
        nw, nh = int(W * sc), int(H * sc); L = L.resize((nw, nh), Image.BILINEAR)
        if sc > 1: L = L.crop(((nw - W) // 2, (nh - H) // 2, (nw - W) // 2 + W, (nh - H) // 2 + H))
        else:
            c = new(); c.paste(L, ((W - nw) // 2, (H - nh) // 2)); L = c
    if blur: L = L.filter(ImageFilter.GaussianBlur(blur))
    if a < 1:
        al = L.getchannel('A').point(lambda v: int(v * a)); L.putalpha(al)
    if off != (0, 0):
        c = new(); c.paste(L, off, L); L = c
    base.alpha_composite(L)

# background: deep warm black, vignette, live grain
yy, xx = np.mgrid[0:H, 0:W]
vig = 1 - 0.55 * (((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.7)) ** 2)
BG = np.dstack([14 * vig, 13 * vig, 12 * vig]).clip(0, 255)
rng = np.random.default_rng(7)
GRAIN = [rng.normal(0, 6, (H // 2, W // 2)).astype(np.float32) for _ in range(6)]

def frame(t):
    base = Image.fromarray(np.uint8(BG)).convert('RGBA')
    i = max(k for k in range(7) if t >= SC[k] - 0.0001) if t >= SC[0] else 0
    # incoming scene: slight entry move
    L = SCENES[i](t)
    since = t - SC[i]
    entry = EXITS[i - 1] if i > 0 else None
    off, sc = (0, 0), 1.0
    if entry == 'push_up' and since < TR: off = (0, int(H * 0.5 * (1 - eo(since / TR))))
    if entry == 'slide_left' and since < TR: off = (int(W * (1 - eo(since / TR))), 0)
    if entry == 'zoom_through' and since < TR: sc = 0.85 + 0.15 * eo(since / TR)
    drift = 1 + 0.025 * cl(since / max(0.5, SC[i + 1] - SC[i]))   # slow push-in on every scene
    comp(base, L, off, sc * drift)
    if i > 0 and since < TR and EXITS[i - 1]:
        P = SCENES[i - 1](t); _, o2, s2_, a2 = transform(P, EXITS[i - 1], since / TR)
        comp(base, P, o2, s2_ * 1.025, a2)
    # loop: fade to black at the very end
    fe = cl((t - (DUR - 0.45)) / 0.45)
    arr = np.asarray(base.convert('RGB')).astype(np.float32)
    g = cv2.resize(GRAIN[int(t * FPS) % 6], (W, H), interpolation=cv2.INTER_LINEAR)
    arr = (arr + g[..., None]) * (1 - fe)
    return np.uint8(arr.clip(0, 255))

N = int(DUR * FPS)
p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-i', f'{tmp}/voice.wav', '-stream_loop', '-1', '-i', MUSIC,
                      '-filter_complex',
                      "[1:a]equalizer=f=180:t=q:w=1:g=2,equalizer=f=3200:t=q:w=1.0:g=3,equalizer=f=6500:t=q:w=1.5:g=1.5,highpass=f=70,"
                      "acompressor=threshold=0.08:ratio=3:attack=8:release=120:makeup=2,asplit=2[v1][vk];"
                      f"[2:a]volume=0.16,afade=t=in:d=1.0,afade=t=out:st={DUR-1.2:.2f}:d=1.2[m0];"
                      "[m0][vk]sidechaincompress=threshold=0.03:ratio=5:attack=15:release=350[m];"
                      "[v1][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
                      '-map', '0:v', '-map', '[a]', '-t', f'{DUR:.2f}', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
                      '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
for n in range(N):
    p.stdin.write(frame(n / FPS).tobytes())
p.stdin.close(); p.wait()
print('done', OUT, f'{DUR:.1f}s')
