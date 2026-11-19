# Be Bold EDIT KIT — one renderer, many editing styles, so no two videos look alike.
# python3 editkit.py <style> <slides_dir> <out.mp4> <music.mp3|none> <lines.txt> <voice_dir>
# styles: impact, film, vhs, whip, ink, iris, zoom
import sys, re, random, subprocess, tempfile, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

STYLE, sd, out, music, lf, VDIR = sys.argv[1:7]
NOMUSIC = music.lower() == 'none'
W, H, FPS, SR = 1080, 1920, 30, 24000
FB = '/home/claude/bebold/fonts/'
FONTS = {
    'oswald': FB + 'package/files/oswald-latin-700-normal.woff',
    'playfair_i': FB + 'package/files/playfair-display-latin-700-normal.woff',
    'anton': FB + 'anton/package/files/anton-latin-400-normal.woff',
    'barlow': FB + 'barlow-condensed/package/files/barlow-condensed-latin-800-normal.woff',
    'bask': FB + 'libre-baskerville/package/files/libre-baskerville-latin-700-normal.woff',
    'mono': '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',
    'inter': '/usr/share/fonts/opentype/inter/Inter-Bold.otf',
}
_fc = {}
def font(name, sz):
    k = (name, sz)
    if k not in _fc: _fc[k] = ImageFont.truetype(FONTS[name], sz)
    return _fc[k]

# style table: transition, caption look, overlay look, transition length, sfx kind
S = {
 'impact': dict(tr='flash',  cap='oswald3', look='grain',      T=0.35, sfx='boom',    punch=True),
 'film':   dict(tr='dissolve', cap='serif', look='film',       T=0.8,  sfx='swell',   punch=False),
 'vhs':    dict(tr='glitch', cap='type',    look='vhs',        T=0.4,  sfx='static',  punch=True),
 'whip':   dict(tr='whip',   cap='oneword', look='grain',      T=0.28, sfx='whoosh',  punch=False),
 'ink':    dict(tr='ink',    cap='card',    look='paper',      T=0.9,  sfx='swish',   punch=False),
 'iris':   dict(tr='iris',   cap='karaoke', look='pulse',      T=0.5,  sfx='boom',    punch=True),
 'zoom':   dict(tr='zoomthru', cap='color', look='grain',      T=0.45, sfx='riser',   punch=True),
}[STYLE]

# ---------- audio + word timings ----------
lines = [re.sub(r'\{[^}]*\}', '', l).strip() for l in open(lf) if l.strip()]
audio, words, slide_t = [], [], []; punch0 = None; t = 0.0
for i, line in enumerate(lines):
    random.seed(i); s0 = t
    lead = np.zeros(int(SR * 0.3)); audio.append(lead); t += len(lead) / SR
    parts = [p for p in re.split(r'(?<=[.?!…])\s+|\s*\|\s*', line) if p.strip()]
    for j, p in enumerate(parts):
        if i == len(lines) - 1 and punch0 is None and (('|' in line and line.split('|')[-1].strip().startswith(p.strip())) or ('|' not in line and j == len(parts) - 1)):
            punch0 = len(words)
        a, sr0 = sf.read(f'{VDIR}/s{i+1}_{j+1}.wav', dtype='float32')
        if a.ndim > 1: a = a.mean(axis=1)
        if sr0 != SR: a = np.interp(np.linspace(0, len(a), int(len(a) * SR / sr0), endpoint=False), np.arange(len(a)), a).astype(np.float32)
        TEMPO = float(__import__('os').environ.get('TEMPO', '0.83'))   # slower, calmer delivery (pitch unchanged)
        if TEMPO != 1.0:
            _t = tempfile.mkdtemp(); sf.write(f'{_t}/i.wav', a, SR)
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{_t}/i.wav', '-filter:a', f'atempo={TEMPO}', f'{_t}/o.wav'], check=True)
            a, _ = sf.read(f'{_t}/o.wav', dtype='float32')
        a = a / (np.abs(a).max() + 1e-6) * random.uniform(0.82, 0.9)
        nz = np.where(np.abs(a) > 0.02)[0]; a = a[max(nz[0]-200, 0):nz[-1]+800] if len(nz) else a
        d = len(a) / SR; ws = p.split(); tot = sum(len(w) + 1 for w in ws); c = t
        for w in ws:
            dw = d * (len(w) + 1) / tot; words.append((c, c + dw, w)); c += dw
        audio.append(a); t += d
        gap = np.zeros(int(SR * (random.uniform(0.55, 0.7) if j < len(parts) - 1 else 0.9))); audio.append(gap); t += len(gap) / SR
    slide_t.append((s0, t))
voice = np.concatenate(audio); D = len(voice) / SR
CUTS = [a for a, _ in slide_t[1:]]
tmp = tempfile.mkdtemp(); sf.write(f'{tmp}/voice.wav', voice, SR)

# ---------- generated sound design (no library) ----------
sfx = np.zeros(len(voice) + SR, dtype=np.float32); R = np.random.default_rng(7)
def put(at, sig):
    s0 = max(int(at * SR), 0); e = min(s0 + len(sig), len(sfx)); sfx[s0:e] += sig[:e - s0]
def noise(n, smooth): w = R.normal(0, 1, n).astype(np.float32); return np.convolve(w, np.ones(smooth) / smooth, 'same')
def sweep(m, f0, f1, amp):
    tt2 = np.arange(m) / SR; f = f0 + (f1 - f0) * (tt2 / tt2[-1]); car = np.sin(2 * np.pi * np.cumsum(f) / SR)
    return (noise(m, 6) * (0.5 + 0.5 * car)) * np.hanning(m) * amp
# ---- Hollywood-style palette: tonal, varied, used sparingly ----
def tone(parts, dur, decay, amp, glide=None):
    n = int(SR * dur); tt_ = np.arange(n) / SR; out_ = np.zeros(n, np.float32)
    for fr, a_ in parts:
        f = fr if glide is None else fr * (glide ** (tt_ / dur))
        out_ += a_ * np.sin(2 * np.pi * np.cumsum(np.broadcast_to(f, tt_.shape)) / SR)
    return out_ * np.exp(-tt_ * decay) * np.minimum(1, tt_ / .004) * amp
SOUNDS = {
 'sub':     lambda: tone([(45, 1), (90, .25)], 1.6, 2.2, .95),                                  # cinematic sub hit
 'tape':    lambda: tone([(420, 1), (840, .3)], .45, 3, .35, glide=.08),                        # tape-stop drop
 'piano':   lambda: tone([(110, 1), (220, .5), (330, .25), (440, .12)], 2.5, 1.6, .45),         # low piano note
 'gong':    lambda: tone([(90, 1), (181.5, .5), (268, .35), (412, .15)], 3.0, 1.1, .4),        # soft low gong
 'snap':    lambda: np.concatenate([R.normal(0, .8, 90).astype(np.float32) * np.linspace(1, 0, 90), tone([(1250, 1)], .12, 30, .25)]),
 'chime':   lambda: np.concatenate([tone([(659, 1), (1318, .3)], .18, 6, .16), tone([(988, 1), (1976, .3)], 1.2, 3.5, .16)]),
 'descend': lambda: tone([(220, 1), (110, .4)], .7, 3, .38, glide=.5),
 'thud':    lambda: (lambda a_, b_: (a_.__setitem__(slice(0, len(b_)), a_[:len(b_)] + b_), a_)[1])(tone([(55, 1), (110, .3)], .5, 9, .85), tone([(820, 1)], .06, 60, .25)),
 'bell':    lambda: tone([(1000, 1), (2760, .5), (5400, .2)], 1.6, 3, .09),
}
HOOK = {'impact': 'sub', 'zoom': 'sub', 'iris': 'sub', 'vhs': 'tape', 'film': 'piano', 'ink': 'gong', 'whip': 'snap'}[STYLE]
put(0.02, SOUNDS[HOOK]())

# ---------- visuals ----------
slides = [Image.open(f'{sd}/slide_{i+1:02d}.jpg').convert('RGB').resize((int(W*1.18), int(H*1.18)), Image.LANCZOS) for i in range(len(lines))]
MOVES = ['in', 'right', 'out', 'left']
def frame_for(i, u, tt):
    im = slides[i]; bw, bh = im.size; u = min(max(u, 0), 1)
    if __import__('os').environ.get('STATIC'):
        return np.asarray(im.resize((W, H), Image.BILINEAR), dtype=np.float32)
    m = MOVES[(i + len(STYLE)) % 4]; e = u * u * (3 - 2 * u)
    if i == 0 and tt - slide_t[0][0] < 0.7 and STYLE in ('impact', 'zoom', 'whip'):
        z = 1.18 - 0.14 * min(1, (tt - slide_t[0][0]) / 0.7); cx = 0.5
    elif m == 'in':  z = 1.04 + 0.10 * e; cx = 0.5
    elif m == 'out': z = 1.14 - 0.10 * e; cx = 0.5
    elif m == 'right': z = 1.10; cx = 0.44 + 0.12 * e
    else: z = 1.10; cx = 0.56 - 0.12 * e
    cw, ch = bw / z, bh / z; x0 = min(max(cx * bw - cw / 2, 0), bw - cw); y0 = (bh - ch) / 2
    return np.asarray(im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch)), dtype=np.float32)

yy, xx = np.mgrid[0:H, 0:W]; RAD = np.hypot(xx - W / 2, yy - H / 2) / np.hypot(W / 2, H / 2)
vign = (1 - 0.38 * RAD ** 2.2)[..., None]
lowf = np.asarray(Image.fromarray((np.random.default_rng(5).random((24, 14)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), dtype=np.float32) / 255
paper = np.asarray(Image.fromarray((np.random.default_rng(9).normal(128, 30, (H // 3, W // 3))).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(2)), dtype=np.float32)[..., None] / 255
grains = [np.random.default_rng(s).normal(0, 9, (H // 2, W // 2, 1)).astype(np.float32) for s in range(6)]
scan = ((np.arange(H) % 4) < 2).astype(np.float32)[:, None, None] * 0.12

SEQ = ['push_up', 'push_left', 'split', 'push_down', 'spin', 'push_right', S['tr']]
_o = len(STYLE) % len(SEQ); TR_FOR = [SEQ[(_o + k) % len(SEQ)] for k in range(len(CUTS))]
import os
if os.environ.get('EDIT_TR'): TR_FOR = (os.environ['EDIT_TR'].split(',') + TR_FOR)[:len(CUTS)]
# only the moments that matter get sound: the climax cut, and the middle cut in longer pieces
TR_SOUND = {'push_up': 'chime', 'push_down': 'descend', 'split': 'thud', 'spin': 'bell'}   # horizontal pushes & style moves stay silent
key_cuts = {len(CUTS) - 1} | ({len(CUTS) // 2} if len(CUTS) >= 3 else set())
for k, c in enumerate(CUTS):
    if k in key_cuts and TR_FOR[k] in TR_SOUND: put(c - (.15 if TR_FOR[k] == 'chime' else 0), SOUNDS[TR_SOUND[TR_FOR[k]]]())
# the drop: music falls silent just before the punchline, then a sub thump lands with it
TP = words[punch0][0] if punch0 is not None else None
if TP: put(TP, tone([(42, 1)], 1.0, 3.5, .7))
if __import__('os').environ.get('NOSFX', '1') == '1': sfx[:] = 0
sf.write(f'{tmp}/sfx.wav', sfx[:len(voice)], SR)
def mblur(o, axis, k):
    if k < 2: return o
    im = Image.fromarray(o.clip(0, 255).astype(np.uint8)); w = im.size
    sm = im.resize((max(1, w[0] // k), w[1]) if axis == 1 else (w[0], max(1, w[1] // k)), Image.BILINEAR).resize(w, Image.BILINEAR)
    return np.asarray(sm, dtype=np.float32)
def transition(A, B, p, f, tr=None):
    tr = tr or S['tr']; e = p * p * (3 - 2 * p); e3 = 1 - (1 - p) ** 3
    if tr in ('push_up', 'push_down'):
        off = int(e3 * H); o = np.concatenate([A[off:], B[:off]], 0) if tr == 'push_up' else np.concatenate([B[H - off:], A[:H - off]], 0)
        return mblur(o, 0, int(1 + 18 * np.sin(np.pi * p)))
    if tr in ('push_left', 'push_right'):
        off = int(e3 * W); o = np.concatenate([A[:, off:], B[:, :off]], 1) if tr == 'push_left' else np.concatenate([B[:, W - off:], A[:, :W - off]], 1)
        return mblur(o, 1, int(1 + 22 * np.sin(np.pi * p)))
    if tr == 'split':
        gap = int(e3 * H / 2); o = B.copy(); top = A[:H // 2]; bot = A[H // 2:]
        if gap < H // 2: o[:H // 2 - gap] = top[gap:]; o[H // 2 + gap:] = bot[:H // 2 - gap]
        return o
    if tr == 'spin':
        ang = 25 * e; sc = 1 - 0.5 * e
        ia = Image.fromarray(A.clip(0, 255).astype(np.uint8)).rotate(ang, Image.BILINEAR)
        ia = ia.resize((int(W * sc), int(H * sc)), Image.BILINEAR); canvas = Image.fromarray(B.clip(0, 255).astype(np.uint8))
        mask = Image.new('L', ia.size, int(255 * (1 - e))); canvas.paste(ia, ((W - ia.size[0]) // 2, (H - ia.size[1]) // 2), mask)
        return np.asarray(canvas, dtype=np.float32)
    if tr == 'dissolve': return A * (1 - e) + B * e
    if tr == 'flash':
        out_ = B if p > .3 else A
        k = 1 - abs(p - .3) / .7; sh = int(16 * k * np.sin(f * 2.7)); out_ = np.roll(out_, sh, axis=1)
        o = int(18 * k); out_ = out_.copy(); out_[..., 0] = np.roll(out_[..., 0], o, 1); out_[..., 2] = np.roll(out_[..., 2], -o, 1)
        if abs(p - .3) < .15: out_ = out_ + (255 - out_) * .85 * (1 - abs(p - .3) / .15)
        return out_
    if tr == 'glitch':
        src = A if p < .5 else B; o = src.copy(); rr = np.random.default_rng(f)
        for _ in range(14):
            y = rr.integers(0, H - 60); hgt = rr.integers(8, 90); o[y:y+hgt] = np.roll(o[y:y+hgt], rr.integers(-160, 160), axis=1)
        o[..., 0] = np.roll(o[..., 0], 12, 1); o[..., 2] = np.roll(o[..., 2], -12, 1); return o
    if tr == 'whip':
        off = int(e * W); o = np.concatenate([A[:, off:], B[:, :off]], axis=1) if off else A
        blur = Image.fromarray(o.clip(0, 255).astype(np.uint8)).filter(ImageFilter.BoxBlur(int(1 + 40 * np.sin(np.pi * p))))
        return np.asarray(blur, dtype=np.float32)
    if tr == 'ink':
        m = ((lowf * .7 + RAD * .3) < e * 1.1).astype(np.float32)
        m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6)), dtype=np.float32)[..., None] / 255
        return A * (1 - m) + B * m
    if tr == 'iris':
        m = (RAD < e * 1.05).astype(np.float32)
        m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)), dtype=np.float32)[..., None] / 255
        ring = ((np.abs(RAD - e * 1.05) < .006) * 255).astype(np.float32)[..., None]
        return np.maximum(A * (1 - m) + B * m, ring * (0 < p < 1))
    if tr == 'zoomthru':
        za = 1 + 1.2 * e; ca = Image.fromarray(A.clip(0, 255).astype(np.uint8))
        cw, ch = W / za, H / za; ca = ca.resize((W, H), Image.BILINEAR, box=((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2)).filter(ImageFilter.GaussianBlur(int(12 * e)))
        return np.asarray(ca, dtype=np.float32) * (1 - e) + B * e
    return B

def look(arr, tt, f):
    lk = S['look']; g = np.repeat(np.repeat(grains[f % 6], 2, 0), 2, 1)
    if lk == 'film':
        arr = arr * vign + g * .7; leak = np.clip(1 - np.hypot(xx - (W * (0.2 + 0.6 * ((tt * .15) % 1))), yy - H * .25) / 700, 0, 1)[..., None]
        arr = arr + leak * np.array([90, 40, 0], np.float32) * .55
        arr[:170] = 0; arr[-170:] = 0
    elif lk == 'vhs':
        arr = arr * (1 - scan) + g * 1.4; arr[..., 0] = np.roll(arr[..., 0], 4, 1); arr[..., 2] = np.roll(arr[..., 2], -3, 1)
        arr = arr * np.array([1.02, 1.0, .94], np.float32)
        if f % 47 < 2: arr = np.roll(arr, 6, 0)
    elif lk == 'paper':
        arr = arr * (0.55 + 0.6 * paper) * vign; arr = arr * np.array([1.03, 1.0, .9], np.float32)
    elif lk == 'pulse':
        on = any(a <= tt < a + .12 for a, _, _ in words); arr = arr * (vign * (0.92 if on else 1.0)) + g
    else:
        arr = arr * vign * (1 + .015 * np.sin(tt * 9.1)) + g
    return arr

def cur_word(tt):
    idx = [n for n, (a, b, _) in enumerate(words) if a <= tt < b + .12]; return idx[-1] if idx else None
def draw_caps(im, tt):
    n = cur_word(tt); d = ImageDraw.Draw(im); cap = S['cap']
    if S['punch'] and punch0 is not None:
        pi = [k for k, (a, _, _) in enumerate(words) if k >= punch0 and a <= tt]
        if pi:
            k = pi[-1]; w = words[k][2].upper(); pop = min(1, (tt - words[k][0]) / .1); sz = int(170 * (1 + .35 * (1 - pop)))
            nm = 'anton' if STYLE != 'vhs' else 'mono'; fo = font(nm, sz)
            while d.textlength(w, font=fo) > 960 and sz > 60: sz -= 10; fo = font(nm, sz)
            d.text(((W - d.textlength(w, font=fo)) / 2, 860 - sz / 2), w, font=fo, fill=(255, 214, 10) if k % 2 == 0 else (255, 255, 255), stroke_width=9, stroke_fill=(0, 0, 0))
            return im
    if n is None: return im
    if cap == 'oneword':
        w = words[n][2].upper(); pop = min(1, (tt - words[n][0]) / .09); sz = int(150 * (1 + .3 * (1 - pop))); fo = font('anton', sz)
        while d.textlength(w, font=fo) > 950: sz -= 8; fo = font('anton', sz)
        d.text(((W - d.textlength(w, font=fo)) / 2, 1180), w, font=fo, fill=(255, 255, 255), stroke_width=10, stroke_fill=(0, 0, 0)); return im
    g0 = (n // 3) * 3 if cap != 'serif' else (n // 5) * 5; grp = words[g0:g0 + (5 if cap == 'serif' else 3)]
    txt = [w for _, _, w in grp]
    if cap == 'type':
        fo = font('mono', 64); s = ' '.join(txt).upper(); a = grp[0][0]; nchar = int(len(s) * min(1, (tt - a) / max(grp[-1][1] - a, .1)))
        s2 = s[:nchar] + ('█' if int(tt * 4) % 2 else ' '); x = (W - d.textlength(s, font=fo)) / 2
        d.text((x, 1320), s2, font=fo, fill=(210, 255, 210), stroke_width=4, stroke_fill=(0, 0, 0)); return im
    if cap == 'serif':
        fo = font('playfair_i', 62); s = ' '.join(txt); x = (W - d.textlength(s, font=fo)) / 2
        al = min(1, (tt - grp[0][0]) / .25); col = tuple(int(255 * al) for _ in range(3))
        d.text((x, int(__import__('os').environ.get('CAPY', 1560))), s, font=fo, fill=col, stroke_width=2, stroke_fill=(0, 0, 0)); return im
    if cap == 'card':
        fo = font('bask', 58); s = ' '.join(txt); tw = d.textlength(s, font=fo); x = (W - tw) / 2
        d.rounded_rectangle((x - 34, 1290, x + tw + 34, 1400), 22, fill=(242, 232, 210)); d.text((x, 1310), s, font=fo, fill=(25, 20, 15)); return im
    fo = font({'oswald3': 'oswald', 'karaoke': 'barlow', 'color': 'inter'}[cap], 84 if cap != 'color' else 74)
    widths = [d.textlength(w, font=fo) for w in txt]; sp = 24; x = (W - sum(widths) - sp * (len(txt) - 1)) / 2; y = 1300
    for j, w in enumerate(txt):
        on = g0 + j == n
        if cap == 'karaoke' and on: d.rounded_rectangle((x - 12, y - 6, x + widths[j] + 12, y + 104), 14, fill=(255, 214, 10))
        col = (0, 0, 0) if (cap == 'karaoke' and on) else ((255, 214, 10) if on and cap == 'oswald3' else ((90, 200, 255) if on and cap == 'color' else (255, 255, 255)))
        d.text((x, y), w, font=fo, fill=col, stroke_width=0 if (cap == 'karaoke' and on) else 7, stroke_fill=(0, 0, 0)); x += widths[j] + sp
    return im

# ---------- render ----------
filt = "[1:a]equalizer=f=180:t=q:w=1:g=2,equalizer=f=3500:t=q:w=1.2:g=1.5,highpass=f=70[v];[2:a]volume=0.55[s];" + (
    "[v][s]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]" if NOMUSIC else
    f"[v]asplit=2[v1][vk];[3:a]volume=0.16,afade=t=in:d=1.2,afade=t=out:st={D-2:.2f}:d=2" +
    (f",volume='if(between(t,{TP-.45:.2f},{TP+.5:.2f}),0.05,1)':eval=frame" if TP else "") +
    "[m0];[m0][vk]sidechaincompress=threshold=0.03:ratio=5:attack=15:release=350[m];[v1][s][m]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-i', f'{tmp}/voice.wav', '-i', f'{tmp}/sfx.wav'] + ([] if NOMUSIC else ['-i', music]) + ['-filter_complex', filt,
                      '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '24', '-maxrate', '6M', '-bufsize', '12M', '-pix_fmt', 'yuv420p',
                      '-c:a', 'aac', '-b:a', '160k', '-t', f'{D:.2f}', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
T = S['T']
for f in range(int(D * FPS)):
    tt = f / FPS
    i = next((n for n, (a, b) in enumerate(slide_t) if a <= tt < b), len(slide_t) - 1)
    a, b = slide_t[i]; arr = frame_for(i, (tt - a) / max(b - a, 1e-3), tt)
    for k, c in enumerate(CUTS):
        if c - max(T, .42) / 2 <= tt < c + max(T, .42) / 2:
            TT = T if TR_FOR[k] == S['tr'] else 0.42
            if not (c - TT / 2 <= tt < c + TT / 2): continue
            pp = (tt - (c - TT / 2)) / TT; A = frame_for(k, 1, tt); B = frame_for(k + 1, 0, tt); arr = transition(A, B, pp, f, TR_FOR[k])
    if tt > D - .3: arr = arr * (1 - (tt - (D - .3)) / .3) + frame_for(0, 0, slide_t[0][0] + .71) * ((tt - (D - .3)) / .3)
    im = Image.fromarray(np.clip(look(arr, tt, f), 0, 255).astype(np.uint8))
    p.stdin.write(draw_caps(im, tt).tobytes())
p.stdin.close(); p.wait(); print(out, round(D, 1), STYLE)
