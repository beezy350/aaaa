# Doodle explainer: white paper, handwritten text that writes itself on, colored-pencil doodles that draw themselves in.
# python3 doodle.py <out.mp4> <music|none> <lines.txt> <voice_dir> <img1> <img2> <img3>
# lines: line 1 = handwritten title, lines 2-4 = the three rules (one doodle each).
import sys, re, random, subprocess, tempfile, os, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
out, music, lf, VDIR = sys.argv[1:5]; IMGS = sys.argv[5:8]
NOMUSIC = music.lower() == 'none'
W, H, FPS, SR = 1080, 1920, 30, 24000
FD = '/home/claude/bebold/fonts/node_modules/@fontsource/'
TITLE_F = ImageFont.truetype(FD + 'caveat/files/caveat-latin-700-normal.woff', 104)
BODY_F = ImageFont.truetype(FD + 'patrick-hand/files/patrick-hand-latin-400-normal.woff', 64)
INK = (28, 28, 34)

# ---------- voice timing (same pipeline as editkit: tempo 0.9, calm pauses) ----------
lines = [re.sub(r'\{[^}]*\}', '', l).strip() for l in open(lf) if l.strip()]
audio, slide_t, t = [], [], 0.0
TEMPO = float(os.environ.get('TEMPO', '0.9'))
for i, line in enumerate(lines):
    random.seed(i); s0 = t
    lead = np.zeros(int(SR * 0.3)); audio.append(lead); t += len(lead) / SR
    parts = [p for p in re.split(r'(?<=[.?!…])\s+|\s*\|\s*', line) if p.strip()]
    sp_start = t
    for j, p in enumerate(parts):
        a, sr0 = sf.read(f'{VDIR}/s{i+1}_{j+1}.wav', dtype='float32')
        if a.ndim > 1: a = a.mean(axis=1)
        if sr0 != SR: a = np.interp(np.linspace(0, len(a), int(len(a) * SR / sr0), endpoint=False), np.arange(len(a)), a).astype(np.float32)
        if TEMPO != 1.0:
            _t = tempfile.mkdtemp(); sf.write(f'{_t}/i.wav', a, SR)
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{_t}/i.wav', '-filter:a', f'atempo={TEMPO}', f'{_t}/o.wav'], check=True)
            a, _ = sf.read(f'{_t}/o.wav', dtype='float32')
        a = a / (np.abs(a).max() + 1e-6) * 0.86
        nz = np.where(np.abs(a) > 0.02)[0]; a = a[max(nz[0]-200, 0):nz[-1]+800] if len(nz) else a
        audio.append(a); t += len(a) / SR
        gap = np.zeros(int(SR * (0.55 if j < len(parts) - 1 else 0.9))); audio.append(gap); t += len(gap) / SR
    slide_t.append((s0, sp_start, t))           # (line start, speech start, line end)
HOLD = 1.6                                         # let the finished page breathe at the end
voice = np.concatenate(audio + [np.zeros(int(SR * HOLD))]); D = len(voice) / SR
tmp = tempfile.mkdtemp(); sf.write(f'{tmp}/voice.wav', voice, SR)
R = np.random.default_rng(11); sfx = np.zeros(len(voice), np.float32)
def band(n, lo, hi):
    x = R.normal(0, 1, n).astype(np.float32); F = np.fft.rfft(x); fr = np.fft.rfftfreq(n, 1 / SR)
    F[(fr < lo) | (fr > hi)] = 0; y = np.fft.irfft(F, n).astype(np.float32); return y / (np.abs(y).max() + 1e-6)
def put(at, sig):
    a0 = max(int(at * SR), 0); e0 = min(a0 + len(sig), len(sfx)); sfx[a0:e0] += sig[:e0 - a0]
def strokes(t0, t1, amp, slen=(0.12, 0.3), gap=(0.03, 0.08), lo=2200, hi=7000):
    t = t0
    while t < t1:
        L = R.uniform(*slen); n = int(L * SR); env = np.sin(np.linspace(0, np.pi, n)) ** 0.6
        put(t, band(n, lo, hi) * env * amp * R.uniform(0.7, 1.0)); t += L + R.uniform(*gap)
def pop(at):
    n = int(SR * .09); tt = np.arange(n) / SR; f = 950 - 2500 * tt
    put(at, (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 40) * .28).astype(np.float32))
put(0.0, band(int(SR * .5), 300, 3000) * np.hanning(int(SR * .5)) ** 1.5 * .25)          # paper slides in
for i in range(1, len(slide_t)):
    s0, sp, e = slide_t[i]; dur = e - s0
    strokes(s0 + .05, s0 + dur * .6, .09)                                                   # pencil outlines
    strokes(s0 + dur * .35, e - .1, .05, slen=(.05, .09), gap=(.01, .03), lo=3000, hi=9000)  # quick colour hatching
    pop(e - .05)                                                                             # drawing done
strokes(D - .95, D - .1, .12, slen=(.1, .16), gap=(.0, .02), lo=600, hi=4000)                # eraser rubs the page clean
sf.write(f'{tmp}/sfx.wav', sfx, SR)

# ---------- paper ----------
rng = np.random.default_rng(3)
paper = np.full((H, W, 3), (250, 248, 243), np.float32)
grain = np.asarray(Image.fromarray(rng.normal(128, 18, (H // 2, W // 2)).clip(0, 255).astype(np.uint8)).resize((W, H)).filter(ImageFilter.GaussianBlur(1.2)), np.float32)[..., None]
paper = paper + (grain - 128) * 0.08

# ---------- layout: title + 3 alternating rows ----------
ROW_Y = [470, 960, 1450]; DOOD = 460
def wrap(text, font, width):
    d = ImageDraw.Draw(Image.new('L', (10, 10))); words = text.split(); ls, cur = [], ''
    for w in words:
        tst = (cur + ' ' + w).strip()
        if d.textlength(tst, font=font) > width: ls.append(cur); cur = w
        else: cur = tst
    return ls + [cur]
def text_layer(text, font, box_x, box_y, width, line_h, center=False):
    """returns RGBA layer + list of (x0,x1,y0,y1) per line for write-on reveal"""
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); spans = []
    for k, ln in enumerate(wrap(text, font, width)):
        tw = d.textlength(ln, font=font); x = box_x + ((width - tw) / 2 if center else 0); y = box_y + k * line_h
        d.text((x, y), ln, font=font, fill=INK + (255,)); spans.append((x, x + tw, y - 10, y + line_h + 10))
    return np.asarray(lay, np.float32) / 255, spans

title_txt = lines[0]
rules = [re.sub(r'^(One|Two|Three)\.\s*', lambda m: {'One': '1. ', 'Two': '2. ', 'Three': '3. '}[m.group(1)], l) for l in lines[1:4]]
layers = []
T_L, T_S = text_layer(title_txt, TITLE_F, 40, 230, 1000, 112, center=True)
layers.append((T_L, T_S))
for k, r in enumerate(rules):
    left = k % 2 == 0          # text left / doodle right, then swap
    tx = 60 if left else 60 + DOOD + 20
    L_, S_ = text_layer(r, BODY_F, tx, ROW_Y[k] + 130, 520, 76)
    layers.append((L_, S_))

# ---------- doodles: line-art draws first, then colour hatching sweeps in ----------
doods = []
for k, p in enumerate(IMGS):
    im = Image.open(p).convert('RGB').resize((DOOD, DOOD), Image.LANCZOS); a = np.asarray(im, np.float32)
    lum = a.mean(2); sat = a.max(2) - a.min(2)
    line = (lum < 95).astype(np.float32)
    color = (((sat > 40) | (lum < 225)) & (lum >= 95)).astype(np.float32)
    yy, xx = np.mgrid[0:DOOD, 0:DOOD]
    noise = np.asarray(Image.fromarray((np.random.default_rng(k).random((10, 10)) * 255).astype(np.uint8)).resize((DOOD, DOOD), Image.BICUBIC), np.float32) / 255
    order_line = (0.55 * noise + 0.3 * yy / DOOD + 0.15 * xx / DOOD)                 # organic stroke-by-stroke feel
    order_col = ((xx + yy) / (2 * DOOD)) * 0.85 + 0.15 * noise                          # diagonal hatching sweep
    x0 = W - DOOD - 40 if k % 2 == 0 else 40; y0 = ROW_Y[k]
    doods.append(dict(a=a, line=line, color=np.clip(color, 0, 1), ol=order_line, oc=order_col, x=x0, y=y0))

def reveal_text(frame, layer, spans, p):
    """p 0..1 -> pen writes across each line in turn"""
    lay, = (layer,)
    total = sum(s[1] - s[0] for s in spans) or 1; done = p * total; m = np.zeros((H, W, 1), np.float32)
    for (x0, x1, y0, y1) in spans:
        wl = x1 - x0
        if done <= 0: break
        cut = x0 + min(wl, done); m[int(max(y0, 0)):int(min(y1, H)), int(x0):int(cut)] = 1; done -= wl
    a = lay[..., 3:4] * m
    return frame * (1 - a) + lay[..., :3] * 255 * a

def draw_doodle(frame, d, p, f, since_done):
    pl = min(1, p / 0.6); pc = max(0, (p - 0.35) / 0.65)
    ml = (d['ol'] < pl * 1.02).astype(np.float32) * d['line']
    mc = np.clip((pc * 1.05 - d['oc']) / 0.06, 0, 1) * d['color']
    m = np.maximum(ml, mc)
    sc = 1.0
    if since_done is not None and since_done < .6: sc = 1 + .09 * np.exp(-since_done * 7) * np.cos(since_done * 22)   # squash-and-stretch settle
    rr = np.random.default_rng((f // 4) * 7 + d['x'])                                                                  # line boil: new wobble every 4 frames
    dx, dy = rr.integers(-2, 3, 2); ang = rr.uniform(-0.6, 0.6)
    rgba = np.dstack([d['a'], m * 255]).clip(0, 255).astype(np.uint8)
    pim = Image.fromarray(rgba, 'RGBA').rotate(ang, Image.BILINEAR)
    if sc != 1.0: n = int(DOOD * sc); pim = pim.resize((n, n), Image.BILINEAR)
    pa = np.asarray(pim, np.float32); n = pa.shape[0]; x0 = d['x'] + (DOOD - n) // 2 + dx; y0 = d['y'] + (DOOD - n) // 2 + dy
    xa, ya = max(x0, 0), max(y0, 0); xb, yb = min(x0 + n, W), min(y0 + n, H)
    pa = pa[ya - y0:yb - y0, xa - x0:xb - x0]; al = pa[..., 3:4] / 255
    sub = frame[ya:yb, xa:xb]; frame[ya:yb, xa:xb] = sub * (1 - al) + sub * (pa[..., :3] / 255) * al   # multiply onto paper
    return frame

def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 2

filt = ("[1:a]equalizer=f=180:t=q:w=1:g=2,equalizer=f=3200:t=q:w=1.0:g=3,highpass=f=70,acompressor=threshold=0.08:ratio=3:attack=8:release=120:makeup=2[v];" +
        "[2:a]volume=0.7[s];" +
        ("[v][s]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]" if NOMUSIC else
         f"[v]asplit=2[v1][vk];[3:a]volume=0.14,afade=t=in:d=1.2,afade=t=out:st={D-2:.2f}:d=2[m0];[m0][vk]sidechaincompress=threshold=0.03:ratio=5:attack=15:release=350[m];[v1][s][m]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]"))
pp = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-i', f'{tmp}/voice.wav', '-i', f'{tmp}/sfx.wav'] + ([] if NOMUSIC else ['-i', music]) + ['-filter_complex', filt, '-map', '0:v', '-map', '[a]',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-t', f'{D:.2f}',
                       '-movflags', '+faststart', out], stdin=subprocess.PIPE)
for f in range(int(D * FPS)):
    tt = f / FPS; fr = paper.copy()
    for i, (lay, spans) in enumerate(layers):
        s0, sp, e = slide_t[i]
        p = ease((tt - sp) / max((e - 0.9) - sp, 0.3))                # handwriting keeps pace with the voice
        if tt >= s0: fr = reveal_text(fr, lay, spans, p)
        if i >= 1:
            dp = (tt - s0) / max(e - s0, 0.5)                         # doodle draws across the whole line
            if dp > 0: fr = draw_doodle(fr, doods[i - 1], min(dp, 1), f, (tt - e) if tt >= e else None)
    if tt > D - .95:                                                   # eraser sweep (diagonal band) back to blank paper
        u = (tt - (D - .95)) / .85; yy_, xx_ = np.mgrid[0:H:8, 0:W:8]
        band_ = ((xx_ / W * .4 + yy_ / H * .6) < u * 1.15).astype(np.float32)
        band_ = np.asarray(Image.fromarray((band_ * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(8)), np.float32)[..., None] / 255
        fr = fr * (1 - band_) + paper * band_
    # gentle camera: slow push-in over the whole video
    z = 1 + 0.03 * tt / D; im = Image.fromarray(np.clip(fr, 0, 255).astype(np.uint8))
    cw, ch = W / z, H / z; im = im.resize((W, H), Image.BILINEAR, box=((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2))
    if tt < .5:                                                        # page slides up onto the desk with a soft overshoot
        u = tt / .5; off = int(H * (1 - u) ** 3 - 30 * np.sin(np.pi * u) * (u > .6))
        desk = Image.new('RGB', (W, H), (46, 40, 36)); desk.paste(im, (0, off)); im = desk
    pp.stdin.write(im.tobytes())
pp.stdin.close(); pp.wait(); print(out, round(D, 1))
