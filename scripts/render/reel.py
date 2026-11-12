# Eye-catching narrated Reel: word-by-word captions, pans/zooms, punch-in hook, film grain, vignette, flicker.
# python3 reel.py <slides_dir> <out.mp4> <music.mp3> <lines.txt>   (one line per slide; "|" forces a pause)
import sys, re, random, subprocess, tempfile, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from kokoro_onnx import Kokoro
sd, out, music, lf = sys.argv[1:5]
W, H, FPS, SR = 1080, 1920, 30, 24000
F = '/home/claude/bebold/fonts/package/files/'
CAP = ImageFont.truetype(F + 'oswald-latin-700-normal.woff', 84)
lines = [l.strip() for l in open(lf) if l.strip()]
k = Kokoro('/home/claude/kokoro/kokoro-v1.0.onnx', '/home/claude/kokoro/voices-v1.0.bin')

# ---------- audio + word timings ----------
audio, words, slide_t = [], [], []   # words: (start, end, text)
t = 0.0
for i, line in enumerate(lines):
    random.seed(i); s0 = t
    lead = np.zeros(int(SR * 0.3)); audio.append(lead); t += len(lead) / SR
    parts = [p for p in re.split(r'(?<=[.?!…])\s+|\s*\|\s*', line) if p.strip()]
    for j, p in enumerate(parts):
        a, _ = k.create(p, voice='am_michael', speed=random.uniform(0.9, 0.97), lang='en-us')
        a = a / (np.abs(a).max() + 1e-6) * random.uniform(0.82, 0.9)
        # trim leading/trailing silence so word timing is tighter
        nz = np.where(np.abs(a) > 0.02)[0]; a = a[max(nz[0]-200, 0):nz[-1]+800] if len(nz) else a
        d = len(a) / SR; ws = p.split(); tot = sum(len(w) + 1 for w in ws); c = t
        for w in ws:
            dw = d * (len(w) + 1) / tot; words.append((c, c + dw, w)); c += dw
        audio.append(a); t += d
        gap = np.zeros(int(SR * (random.uniform(0.28, 0.42) if j < len(parts) - 1 else 0.55)))
        audio.append(gap); t += len(gap) / SR
    slide_t.append((s0, t))
voice = np.concatenate(audio); D = len(voice) / SR
tmp = tempfile.mkdtemp(); sf.write(f'{tmp}/voice.wav', voice, SR)

# ---------- visual helpers ----------
slides = [Image.open(f'{sd}/slide_{i+1:02d}.jpg').convert('RGB').resize((int(W*1.18), int(H*1.18)), Image.LANCZOS) for i in range(len(lines))]
vign = Image.new('L', (W, H), 0); dv = ImageDraw.Draw(vign)
dv.ellipse((-W*0.25, -H*0.15, W*1.25, H*1.15), fill=255); vign = vign.filter(ImageFilter.GaussianBlur(160))
vign_arr = (np.asarray(vign, dtype=np.float32) / 255 * 0.35 + 0.65)[..., None]
rng = np.random.default_rng(3); grains = [rng.normal(0, 9, (H // 2, W // 2, 1)).astype(np.float32) for _ in range(6)]
MOVES = ['in', 'right', 'out', 'left']
def frame_for(i, u, tt):
    im = slides[i]; bw, bh = im.size
    m = MOVES[i % 4]; e = u * u * (3 - 2 * u)  # smoothstep
    if i == 0 and tt - slide_t[0][0] < 0.7:            # punchy hook: fast push-in
        z = 1.18 - 0.14 * min(1, (tt - slide_t[0][0]) / 0.7); cx = 0.5
    elif m == 'in':  z = 1.04 + 0.10 * e; cx = 0.5
    elif m == 'out': z = 1.14 - 0.10 * e; cx = 0.5
    elif m == 'right': z = 1.10; cx = 0.44 + 0.12 * e
    else: z = 1.10; cx = 0.56 - 0.12 * e
    cw, ch = bw / z, bh / z
    x0 = min(max(cx * bw - cw / 2, 0), bw - cw); y0 = (bh - ch) / 2
    return im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
def caption(fr, tt):
    idx = [n for n, (a, b, _) in enumerate(words) if a <= tt < b + 0.12]
    if not idx: return fr
    n = idx[-1]; g0 = (n // 3) * 3; grp = words[g0:g0 + 3]
    d = ImageDraw.Draw(fr); txt = [w for _, _, w in grp]
    widths = [d.textlength(w, font=CAP) for w in txt]; sp = 22
    total = sum(widths) + sp * (len(txt) - 1); x = (W - total) / 2; y = 1300
    pop = min(1, (tt - words[n][0]) / 0.08)
    for j, w in enumerate(txt):
        col = (255, 214, 10) if g0 + j == n else (255, 255, 255)
        d.text((x, y - (6 * (1 - pop) if g0 + j == n else 0)), w, font=CAP, fill=col, stroke_width=7, stroke_fill=(0, 0, 0))
        x += widths[j] + sp
    return fr

# ---------- render ----------
p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-i', f'{tmp}/voice.wav', '-i', music, '-filter_complex',
                      f"[1:a]equalizer=f=180:t=q:w=1:g=2,equalizer=f=3500:t=q:w=1.2:g=1.5,highpass=f=70[v];"
                      f"[2:a]volume=0.14,afade=t=in:d=1.2,afade=t=out:st={D-2:.2f}:d=2[m];[v][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
                      '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '24', '-maxrate', '6M', '-bufsize', '12M', '-pix_fmt', 'yuv420p',
                      '-c:a', 'aac', '-b:a', '160k', '-t', f'{D:.2f}', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
nf = int(D * FPS)
for f in range(nf):
    tt = f / FPS
    i = next((n for n, (a, b) in enumerate(slide_t) if a <= tt < b), len(slide_t) - 1)
    a, b = slide_t[i]; u = (tt - a) / max(b - a, 1e-3)
    fr = frame_for(i, u, tt)
    arr = np.asarray(fr, dtype=np.float32)
    g = np.repeat(np.repeat(grains[f % 6], 2, 0), 2, 1)
    flick = 1 + 0.015 * np.sin(tt * 9.1) * np.sin(tt * 2.3)
    arr = np.clip((arr * vign_arr * flick) + g, 0, 255).astype(np.uint8)
    fr = caption(Image.fromarray(arr), tt)
    p.stdin.write(fr.tobytes())
p.stdin.close(); p.wait()
print(out, round(D, 1))
