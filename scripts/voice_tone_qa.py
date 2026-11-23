# Tone QA: flags sentences that sound over-emotional / synthetic.
# usage: python3 voice_tone_qa.py <voice_dir>   -> prints a table, writes tone.json, exit 1 if any clip fails
import sys, json, glob, os
import numpy as np, librosa
d = sys.argv[1]; rows = []
for f in sorted(glob.glob(f'{d}/s*_*.wav')):
    y, sr = librosa.load(f, sr=16000)
    f0, vflag, _ = librosa.pyin(y, fmin=60, fmax=400, sr=sr, frame_length=1024)
    f0 = f0[vflag & ~np.isnan(f0)]
    if len(f0) < 10: continue
    st = 12 * np.log2(f0 / np.median(f0))              # semitones around the clip's own median
    spread = float(np.percentile(st, 95) - np.percentile(st, 5))   # pitch range used
    jumps = float(np.mean(np.abs(np.diff(st)) > 2.5))   # share of sudden pitch jumps between frames
    rms = librosa.feature.rms(y=y)[0]; rms = rms[rms > rms.max() * 0.1]
    loud = float(np.percentile(rms, 95) / max(np.median(rms), 1e-6))  # loudness peaks vs median
    med = float(np.median(f0))
    bad = []
    if spread > 17: bad.append('pitch range too wide (emotional)')
    if jumps > 0.07: bad.append('sudden pitch jumps (synthetic/wobbly)')
    if loud > 2.6: bad.append('shouted / uneven loudness')
    if med > 140: bad.append('pitch too high for the deep voice')
    rows.append(dict(clip=os.path.basename(f), median_hz=round(med), range_st=round(spread, 1), jumps=round(jumps, 3), loud=round(loud, 2), fail=bad))
for r in rows: print(f"{r['clip']:10s} {r['median_hz']:4d}Hz range {r['range_st']:5.1f}st jumps {r['jumps']:.3f} loud {r['loud']:.2f}  {'; '.join(r['fail']) or 'ok'}")
json.dump(rows, open(f'{d}/tone.json', 'w'), indent=1)
sys.exit(1 if any(r['fail'] for r in rows) else 0)
