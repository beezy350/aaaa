"""Download public-domain audio from Wikimedia Commons listed in bebold/music/sources.txt.
Saves bebold/music/<slug>.mp3 (via ffmpeg) and records license info in bebold/music/licenses.json."""
import json, os, subprocess, urllib.parse, urllib.request
UA = {"User-Agent": "BeBoldPipeline/1.0 (https://github.com/beezy350/aaaa)"}
out, lic = "bebold/music", {}
for line in open(f"{out}/sources.txt"):
    if "|" not in line: continue
    name, slug = line.strip().rsplit("|", 1)
    if os.path.exists(f"{out}/{slug}.mp3"): continue
    q = urllib.parse.urlencode({"action": "query", "titles": "File:" + name, "prop": "imageinfo",
                                "iiprop": "url|extmetadata", "format": "json"})
    try:
        with urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + q, headers=UA), timeout=60) as r:
            page = next(iter(json.load(r)["query"]["pages"].values()))
        info = page["imageinfo"][0]; md = info.get("extmetadata", {})
        g = lambda k: (md.get(k) or {}).get("value", "")
        lic[slug] = {"file": name, "url": info["url"], "license": g("LicenseShortName"),
                     "artist": g("Artist")[:200], "credit": g("Credit")[:200]}
        src = f"/tmp/{slug}.src"
        with urllib.request.urlopen(urllib.request.Request(info["url"], headers=UA), timeout=300) as r, open(src, "wb") as f:
            f.write(r.read())
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-ac", "2", "-ar", "44100", "-b:a", "160k", f"{out}/{slug}.mp3"], check=True)
        print("OK", slug, lic[slug]["license"])
    except Exception as e:
        lic[slug] = {"file": name, "error": str(e)[:300]}; print("FAIL", slug, e)
old = json.load(open(f"{out}/licenses.json")) if os.path.exists(f"{out}/licenses.json") else {}
old.update(lic); json.dump(old, open(f"{out}/licenses.json", "w"), indent=1)
