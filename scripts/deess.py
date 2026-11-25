"""Spectral de-esser for the owner's voice: tames s / sh / ch / t hiss frame by frame.
usage: python3 deess.py in.wav out.wav [max_db=-14] [lo=4000]
For each 21 ms frame, energy above `lo` Hz is limited to `max_db` relative to the frame's energy below `lo`.
Gains are smoothed over time and ramped across the crossover so it doesn't sound lispy or phasey.
Also applies a steep cut above 12 kHz, where phone mics add fizz."""
import sys, numpy as np, soundfile as sf
from scipy.signal import stft, istft
from scipy.ndimage import uniform_filter1d
inp, out = sys.argv[1], sys.argv[2]
max_db = float(sys.argv[3]) if len(sys.argv) > 3 else -14.0
lo = float(sys.argv[4]) if len(sys.argv) > 4 else 4000.0
a, sr = sf.read(inp)
if a.ndim > 1: a = a.mean(1)
nper = 1024
f, t, Z = stft(a, sr, nperseg=nper, noverlap=nper * 3 // 4)
P = np.abs(Z) ** 2
hi = f >= lo; low = (f >= 150) & (f < lo)
e_hi = P[hi].sum(0) + 1e-12; e_lo = P[low].sum(0) + 1e-12
ratio_db = 10 * np.log10(e_hi / e_lo)
g_db = np.minimum(0, max_db - ratio_db)            # how much the hi band must drop in each frame
g_db = np.minimum(g_db, uniform_filter1d(g_db, 3))  # spread slightly so onsets of 's' are caught
g_db = uniform_filter1d(g_db, 2)
G = np.ones_like(P)
ramp = np.clip((f - (lo - 1500)) / 1500, 0, 1)[:, None]   # fade the cut in from lo-1.5k to lo
G = 10 ** ((g_db[None, :] * ramp) / 20)
air = np.where(f > 12000, 10 ** (-18 / 20), 1.0)[:, None]  # steep shelf above 12 kHz
_, y = istft(Z * G * air, sr, nperseg=nper, noverlap=nper * 3 // 4)
y = y[:len(a)]
sf.write(out, y, sr)
print(f"de-essed: frames limited {np.mean(g_db < -1)*100:.0f}% , max cut {g_db.min():.1f} dB")
