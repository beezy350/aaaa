# Uzbek voiceover in the owner's cloned voice (Janob, Instagram only).
# Engine: Chatterbox multilingual base + UAzimov/Uzbek-tts-chatterbox LoRA (MIT), via gokhaneraslan/chatterbox-finetuning.
# Jobs: bebold/voice/uz_jobs/<name>.txt  (optional header "#ref=... ex=0.5 cfg=0.5 seed=1234"; one sentence per line)
# Output: bebold/voice/uz_out/<name>/s<n>.wav + qa.json (Whisper 'uz' transcript per line for a rough check)
import os, re, sys, glob, json, time, difflib, torch, torchaudio
sys.path.insert(0, "chatterbox-finetuning"); os.chdir("chatterbox-finetuning")
from src.config import TrainConfig
from src.chatterbox_.tts import ChatterboxTTS
from src.model import resize_and_load_t3_weights
from src.chatterbox_.models.t3.t3 import T3
from peft import LoraConfig, get_peft_model
from safetensors.torch import load_file
cfg = TrainConfig()
eng = ChatterboxTTS.from_local(cfg.model_dir, device="cpu")
hp = eng.t3.hp; hp.text_tokens_dict_size = cfg.new_vocab_size
t3 = resize_and_load_t3_weights(T3(hp=hp), eng.t3.state_dict())
peft_cfg = LoraConfig(r=128, lora_alpha=256, target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj","spkr_enc"],
                      lora_dropout=0.05, bias="none", modules_to_save=["text_emb","text_head"])
model = get_peft_model(t3, peft_cfg)
sd = load_file("../uz_adapter/adapter_model.safetensors")
missing, unexpected = model.load_state_dict(sd, strict=False)
print("adapter missing", len(missing), "unexpected", len(unexpected), flush=True)
eng.t3 = model.merge_and_unload().eval()
os.chdir("..")
from faster_whisper import WhisperModel
asr = WhisperModel("small", device="cpu", compute_type="int8")
def norm_ap(t): return re.sub("[ʻʼ‘’`]", "'", t)
def letters(t): return re.sub(r"[^a-zo'g']", "", norm_ap(t).lower())
for job in sorted(glob.glob("bebold/voice/uz_jobs/*.txt")):
    name = os.path.basename(job)[:-4]; od = f"bebold/voice/uz_out/{name}"
    if os.path.exists(f"{od}/done.txt"): continue
    os.makedirs(od, exist_ok=True); t0 = time.time(); rep = []
    lines = [l.strip() for l in open(job, encoding="utf-8") if l.strip()]
    EX, CFG, SEED, REF = 0.5, 0.5, 1234, "bebold/voice/ref_janob_en_clean.wav"
    if lines[0].startswith("#"):
        h = dict(kv.split("=") for kv in lines.pop(0)[1:].split()); EX=float(h.get("ex",EX)); CFG=float(h.get("cfg",CFG)); SEED=int(h.get("seed",SEED)); REF=h.get("ref",REF)
    for i, line in enumerate(lines, 1):
        best = None
        for k in range(4):
            torch.manual_seed(SEED + k)
            w = eng.generate(norm_ap(line), audio_prompt_path=REF, exaggeration=EX, cfg_weight=CFG)
            tmp = f"{od}/_try.wav"; torchaudio.save(tmp, w, eng.sr)
            segs, _ = asr.transcribe(tmp, beam_size=5, language="uz"); heard = " ".join(s.text for s in segs).strip()
            sc = difflib.SequenceMatcher(None, letters(line), letters(heard)).ratio()
            dur = w.shape[-1] / eng.sr
            if dur > 0.6 * len(line.split()) + 1.5: sc -= 0.3
            if best is None or sc > best[0]: best = (sc, w, heard, k + 1)
            if sc >= 0.85: break
        torchaudio.save(f"{od}/s{i}.wav", best[1], eng.sr)
        rep.append({"clip": f"s{i}", "script": line, "heard": best[2], "score": round(best[0], 3), "tries": best[3]})
        print(rep[-1], flush=True)
    if os.path.exists(f"{od}/_try.wav"): os.remove(f"{od}/_try.wav")
    json.dump(rep, open(f"{od}/qa.json", "w"), indent=1, ensure_ascii=False)
    open(f"{od}/done.txt", "w").write(f"{time.time()-t0:.0f}s\n")
