# 2.5D parallax: estimate depth (MiDaS small, ONNX), then move a virtual camera through the still image.
# python3 parallax.py out.mp4 seconds_per_shot move img1 [img2 ...]   move: dolly | orbit | rise (cycled per shot)
import sys, subprocess, numpy as np, cv2, onnxruntime as ort
from PIL import Image, ImageOps
out, secs = sys.argv[1], float(sys.argv[2]); imgs = sys.argv[4:]; moves = sys.argv[3].split(',')
W, H, FPS = 1080, 1920, 30
sess = ort.InferenceSession('/home/claude/models/midas_small.onnx')
def depth(rgb):
    x = cv2.resize(rgb, (256, 256)).astype(np.float32) / 255
    x = (x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    d = sess.run(None, {'0': x.transpose(2, 0, 1)[None].astype(np.float32)})[0][0]
    d = cv2.resize(d, (rgb.shape[1], rgb.shape[0])); d = (d - d.min()) / (d.max() - d.min() + 1e-6)
    return cv2.GaussianBlur(d, (0, 0), 6)                    # near = 1, far = 0; soft edges avoid tearing
p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
for k, path in enumerate(imgs):
    im = np.asarray(ImageOps.fit(Image.open(path).convert('RGB'), (int(W * 1.12), int(H * 1.12))), np.uint8)
    d = depth(im); h, w = d.shape; ox, oy = (w - W) / 2, (h - H) / 2
    mv = moves[k % len(moves)]; n = int(secs * FPS)
    for f in range(n):
        u = f / (n - 1); e = u * u * (3 - 2 * u)
        if mv == 'dolly':  sx, sy, z = 0, 0, 0.10 * e               # push in: near layers grow faster than far
        elif mv == 'orbit': sx, sy, z = 46 * (e - .5), 0, 0.03      # slide sideways: near slides more than far
        else:              sx, sy, z = 0, -40 * (e - .5), 0.04 * e  # rise: camera floats upward
        dd = d[int(oy):int(oy) + H, int(ox):int(ox) + W]
        zz = 1 + z * (0.35 + dd)                                    # per-pixel zoom by depth
        mx = (xx - W / 2) / zz + W / 2 + ox - sx * dd
        my = (yy - H / 2) / zz + H / 2 + oy - sy * dd
        fr = cv2.remap(im, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        if f < 8 and k > 0: fr = (fr * (f / 8) + prev * (1 - f / 8)).astype(np.uint8)   # short dissolve between shots
        p.stdin.write(fr.tobytes()); last = fr
    prev = last
p.stdin.close(); p.wait(); print(out)
