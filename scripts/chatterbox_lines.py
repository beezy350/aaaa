# For each bebold/voice/jobs/<name>.txt (one line per slide, "|" = pause), make one Chatterbox wav per sentence:
# bebold/voice/out/<name>/s<slide>_<n>.wav  (skips jobs that already have a done.txt)
import re, os, glob, time, torch, torchaudio
from chatterbox.tts import ChatterboxTTS
m = ChatterboxTTS.from_pretrained(device="cpu")
for job in sorted(glob.glob("bebold/voice/jobs/*.txt")):
    name = os.path.basename(job)[:-4]; od = f"bebold/voice/out/{name}"
    if os.path.exists(f"{od}/done.txt"): continue
    os.makedirs(od, exist_ok=True); t0 = time.time()
    lines = [l.strip() for l in open(job) if l.strip()]
    for i, line in enumerate(lines, 1):
        parts = [p for p in re.split(r'(?<=[.?!…])\s+|\s*\|\s*', line) if p.strip()]
        for j, p in enumerate(parts, 1):
            # D2 calm: lower emotion so it sounds natural; retry clips that run long (screams/garble at the tail)
            limit = 0.5 * len(p.split()) + 1.0
            for _ in range(4):
                w = m.generate(p, audio_prompt_path="bebold/voice/ref_deep_warm.wav", exaggeration=0.6, cfg_weight=0.4)
                if w.shape[-1] / m.sr <= limit: break
            torchaudio.save(f"{od}/s{i}_{j}.wav", w, m.sr)
    open(f"{od}/done.txt", "w").write(f"{time.time()-t0:.0f}s\n")
