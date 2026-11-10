"""Generate images for Be Bold job files using the OpenAI Images API.

A job file is bebold/jobs/<job_id>.json:
{"images": [{"name": "1A", "prompt": "...", "size": "1024x1536", "quality": "medium"}]}
Output goes to bebold/raw/<job_id>/<name>.png plus status.json.
Jobs that already have a status.json are skipped.
"""
import base64, glob, json, os, sys, time, urllib.request, urllib.error

KEY = os.environ.get("OPENAI_API_KEY", "")
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
    if not KEY:
        sys.exit("OPENAI_API_KEY secret is missing")
    for job in sorted(glob.glob("bebold/jobs/*.json")):
        jid = os.path.splitext(os.path.basename(job))[0]
        out = f"bebold/raw/{jid}"
        if os.path.exists(f"{out}/status.json"):
            continue
        os.makedirs(out, exist_ok=True)
        spec = json.load(open(job))
        status = {"job": jid, "results": []}
        for img in spec["images"]:
            model, data, usage, err = gen(img)
            entry = {"name": img["name"], "quality": img.get("quality", "medium")}
            if data:
                open(f"{out}/{img['name']}.png", "wb").write(data)
                entry.update(ok=True, model=model, usage=usage)
            else:
                entry.update(ok=False, errors=err)
            status["results"].append(entry)
            print(json.dumps(entry)[:300])
        json.dump(status, open(f"{out}/status.json", "w"), indent=1)


main()
