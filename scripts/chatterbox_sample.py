# Chatterbox voice samples (CPU): several reference voices / emotion settings on the same text
import re, torch, torchaudio
from chatterbox.tts import ChatterboxTTS
m = ChatterboxTTS.from_pretrained(device="cpu")
text = open("bebold/voice/sample_text.txt").read().strip()
parts = [p for p in re.split(r'(?<=[.?!])\s+', text) if p.strip()]
V = [("C_deep_warm", "ref_deep_warm.wav", 0.75, 0.35),
     ("D_deep_warm_emotional", "ref_deep_warm.wav", 0.95, 0.3),
     ("E_deep_storyteller", "ref_deep_story.wav", 0.8, 0.35)]
for name, ref, ex, cfg in V:
    wavs = []
    for p in parts:
        w = m.generate(p, audio_prompt_path=f"bebold/voice/{ref}", exaggeration=ex, cfg_weight=cfg)
        wavs += [w, torch.zeros(1, int(m.sr * 0.35))]
    torchaudio.save(f"bebold/voice/sample_{name}.wav", torch.cat(wavs, dim=1), m.sr)
