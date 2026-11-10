"""Generate images for Be Bold job files using the OpenAI Images API.

A job file is bebold/jobs/<job_id>.json:
{"images": [{"name": "1A", "prompt": "...", "size": "1024x1536", "quality": "medium", "engine": "openai|cloudflare"}]}
Output goes to bebold/raw/<job_id>/<name>.png plus status.json.
Jobs that already have a status.json are skipped.
"""
import base64, glob, json, os, sys, time, urllib.request, urllib.error

KEY = os.environ.get("OPENAI_API_KEY", "")
CF_ACC = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
CF_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
CF_MODELS = os.environ.get("CF_MODELS", "flux-2-klein-4b,flux-1-schnell").split(",")


def cf_call(model, prompt, w, h):
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACC}/ai/run/@cf/black-forest-labs/{model}"
    if model.startswith("flux-2"):
        b = "----bebold" + str(int(time.time() * 1000))
        parts = []
        for k, v in (("prompt", prompt), ("width", str(w)), ("height", str(h))):
            parts.append(f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n")
        body = ("".join(parts) + f"--{b}--\r\n").encode()
        ctype = f"multipart/form-data; boundary={b}"
    else:
        body = json.dumps({"prompt": prompt, "steps": 8}).encode()
        ctype = "application/json"
    req = urllib.request.Request(url, data=body, headers={"Authorization": f"Bearer {CF_TOKEN}",
                                                          "Content-Type": ctype})
    with urllib.request.urlopen(req, timeout=300) as r:
        raw = r.read()
    try:
        j = json.loads(raw)
    except Exception:
        return raw  # binary image
    res = j.get("result", j)
    return base64.b64decode(res["image"])


def gen_cf(img):
    errors = []
    w, h = (int(x) for x in img.get("size", "1024x1536").split("x"))
    for model in CF_MODELS:
        model = model.strip()
        try:
            return "cf/" + model, cf_call(model, img["prompt"], w, h), None, None
        except urllib.error.HTTPError as e:
            errors.append(f"{model}: HTTP {e.code} {e.read().decode(errors='replace')[:300]}")
        except Exception as e:
            errors.append(f"{model}: {e}")
    return None, None, None, errors
MODELS = os.environ.get("IMAGE_MODELS", "gpt-image-2,gpt-image-1.5,gpt-image-1").split(",")


def call(model, prompt, size, quality):
    body = json.dumps({"model": model, "prompt": prompt, "size": size,
                       "quality": quality, "n": 1}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body,
                                 headers={"Authorization": f"Bearer {KEY}",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def gen(img):
    errors = []
    for model in MODELS:
        model = model.strip()
        for attempt in range(2):
            try:
                res = call(model, img["prompt"], img.get("size", "1024x1536"), img.get("quality", "medium"))
                return model, base64.b64decode(res["data"][0]["b64_json"]), res.get("usage"), None
            except urllib.error.HTTPError as e:
                msg = e.read().decode(errors="replace")[:400]
                errors.append(f"{model}: HTTP {e.code} {msg}")
                if e.code in (400, 403, 404) and ("model" in msg.lower() or e.code == 404):
                    break  # try next model
                if e.code in (401,):
                    return None, None, None, errors
                time.sleep(5)
            except Exception as e:  # network etc.
                errors.append(f"{model}: {e}")
                time.sleep(5)
    return None, None, None, errors


def main():
    if not KEY and not CF_TOKEN:
        sys.exit("No image API secrets found")
    for job in sorted(glob.glob("bebold/jobs/*.json")):
        jid = os.path.splitext(os.path.basename(job))[0]
        out = f"bebold/raw/{jid}"
        if os.path.exists(f"{out}/status.json"):
            continue
        os.makedirs(out, exist_ok=True)
        spec = json.load(open(job))
        status = {"job": jid, "results": []}
        for img in spec["images"]:
            engine = img.get("engine", "openai")
            if engine == "cloudflare" and CF_TOKEN:
                model, data, usage, err = gen_cf(img)
                if not data and KEY:  # fall back to OpenAI medium
                    model, data, usage, err2 = gen({**img, "quality": "medium"})
                    err = (err or []) + (err2 or [])
            else:
                model, data, usage, err = gen(img)
            entry = {"name": img["name"], "quality": img.get("quality", "medium")}
            if data:
                ext = "jpg" if data[:3] == b"\xff\xd8\xff" else "png"
                open(f"{out}/{img['name']}.{ext}", "wb").write(data)
                entry.update(ok=True, model=model, usage=usage)
            else:
                entry.update(ok=False, errors=err)
            status["results"].append(entry)
            print(json.dumps(entry)[:300])
        json.dump(status, open(f"{out}/status.json", "w"), indent=1)


main()
