# Generate a Chatterbox TTS sample (CPU) from bebold/voice/sample_text.txt, voice-matched to ref_michael.wav
import re, time, torch, torchaudio
from chatterbox.tts import ChatterboxTTS
t0 = time.time()
m = ChatterboxTTS.from_pretrained(device="cpu")
text = open("bebold/voice/sample_text.txt").read().strip()
parts = [p for p in re.split(r'(?<=[.?!])\s+', text) if p.strip()]
wavs = []
for p in parts:
    w = m.generate(p, audio_prompt_path="bebold/voice/ref_michael.wav", exaggeration=0.6, cfg_weight=0.4)
    wavs += [w, torch.zeros(1, int(m.sr * 0.3))]
torchaudio.save("bebold/voice/chatterbox_sample.wav", torch.cat(wavs, dim=1), m.sr)
open("bebold/voice/chatterbox_time.txt", "w").write(f"{time.time()-t0:.0f} seconds total on GitHub CPU\n")
