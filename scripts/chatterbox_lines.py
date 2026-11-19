# For each bebold/voice/jobs/<name>.txt (one line per slide, "|" = pause), make one Chatterbox wav per sentence:
# bebold/voice/out/<name>/s<slide>_<n>.wav  (skips jobs that already have a done.txt)
# QA: every sentence is transcribed by Whisper and compared word by word with the script; mispronounced,
# skipped, garbled or screamed takes are regenerated (best of up to 6). Report: bebold/voice/out/<name>/qa.json
import re, os, glob, time, json, difflib, torch, torchaudio
from chatterbox.tts import ChatterboxTTS
from faster_whisper import WhisperModel
from num2words import num2words
m = ChatterboxTTS.from_pretrained(device="cpu")
asr = WhisperModel("small.en", device="cpu", compute_type="int8")
def norm(t):
    t = re.sub(r"(\d+)s\b", lambda x: num2words(int(x.group(1)), to="year") + "s", t)
    t = re.sub(r"\d+", lambda x: num2words(int(x.group(0))), t)
    return re.sub(r"[^a-z]", "", t.lower())
def spiky(w):
    # scream / shout detector: loudest 50 ms window vs typical voiced loudness
    a = w.squeeze().numpy(); n = int(m.sr * .05); rms = [float((a[k:k+n] ** 2).mean() ** .5) for k in range(0, len(a) - n, n)]
    v = sorted(r for r in rms if r > 0.02)
    return (max(v) / v[len(v) // 2]) if len(v) > 4 else 1.0
def heard(path):
    segs, _ = asr.transcribe(path, beam_size=5, language="en")
    return " ".join(s.text for s in segs).strip()
for job in sorted(glob.glob("bebold/voice/jobs/*.txt")):
    name = os.path.basename(job)[:-4]; od = f"bebold/voice/out/{name}"
    if os.path.exists(f"{od}/done.txt"): continue
    os.makedirs(od, exist_ok=True); t0 = time.time(); report = []
    lines = [l.strip() for l in open(job) if l.strip()]
    EX, CFG, SEED = 0.85, 0.6, 1234          # default = B2: energetic, steady (owner's pick, Nov 18)
    if lines and lines[0].startswith('#'):    # optional per-job header, e.g. "#ex=0.95 cfg=0.5"
        hdr = dict(kv.split('=') for kv in lines.pop(0)[1:].split()); EX = float(hdr.get('ex', EX)); CFG = float(hdr.get('cfg', CFG)); SEED = int(hdr.get('seed', SEED))
    for i, line in enumerate(lines, 1):
        parts = [p for p in re.split(r'(?<=[.?!…])\s+|\s*\|\s*', line) if p.strip()]
        for j, p in enumerate(parts, 1):
            limit = 0.5 * len(p.split()) + 1.0; best = None; tmp = f"{od}/_try.wav"
            for k in range(6):
                torch.manual_seed(SEED + k)   # same seed family for every sentence = steady, consistent tone
                w = m.generate(p, audio_prompt_path="bebold/voice/ref_deep_warm.wav", exaggeration=EX, cfg_weight=CFG)
                dur = w.shape[-1] / m.sr; torchaudio.save(tmp, w, m.sr)
                h = heard(tmp); score = difflib.SequenceMatcher(None, norm(p), norm(h)).ratio()
                if dur > limit: score -= 0.3
                sp = spiky(w)
                if sp > 3.2: score -= 0.5   # shouted / screamed word -> reject
                if best is None or score > best[0]: best = (score, w, h, k + 1)
                if score >= 0.93: break
            torchaudio.save(f"{od}/s{i}_{j}.wav", best[1], m.sr)
            report.append({"clip": f"s{i}_{j}", "script": p, "heard": best[2], "score": round(best[0], 3), "tries": best[3], "spike": round(spiky(best[1]), 2)})
            print(f"s{i}_{j} {best[0]:.2f} x{best[3]} | {p} || {best[2]}", flush=True)
    if os.path.exists(f"{od}/_try.wav"): os.remove(f"{od}/_try.wav")
    json.dump(report, open(f"{od}/qa.json", "w"), indent=1)
    open(f"{od}/done.txt", "w").write(f"{time.time()-t0:.0f}s\n")
