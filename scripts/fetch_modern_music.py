"""Search Wikimedia Commons for modern ambient/cinematic tracks that are free for commercial use
(CC0, public domain, CC BY), download them and make 25 s previews. Writes bebold/music/modern/."""
import json, os, re, subprocess, urllib.parse, urllib.request
UA = {"User-Agent": "BeBoldPipeline/1.0 (https://github.com/beezy350/aaaa)"}
OUT = "bebold/music/modern"; os.makedirs(OUT + "/previews", exist_ok=True)
OK = re.compile(r"^(CC0|Public domain|CC BY [0-9.]+)$", re.I)
OLD = re.compile(r"beethoven|chopin|mozart|bach|satie|debussy|schubert|liszt|vivaldi|brahms|tchaikovsky|handel|haydn|wagner|anthem|speech|interview|bird|recording of", re.I)
def api(**p):
    p.update(format="json")
    with urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p), headers=UA), timeout=60) as r:
        return json.load(r)
seen, picks = set(), []
for q in ["ambient music", "cinematic music", "ambient electronic", "dark ambient", "piano ambient", "lofi", "atmospheric music", "film score", "chill electronic", "drone ambient", "soundtrack instrumental", "meditation music"]:
    try:
        res = api(action="query", generator="search", gsrsearch=q + " filetype:audio", gsrnamespace=6, gsrlimit=40,
                  prop="imageinfo", iiprop="url|extmetadata|mediatype|size")
    except Exception as e:
        print("search fail", q, e); continue
    for pg in (res.get("query") or {}).get("pages", {}).values():
        t = pg["title"]
        if t in seen or OLD.search(t): continue
        seen.add(t); ii = (pg.get("imageinfo") or [{}])[0]; md = ii.get("extmetadata", {})
        g = lambda k: re.sub("<[^>]+>", "", (md.get(k) or {}).get("value", "")).strip()
        lic = g("LicenseShortName"); dur = float(ii.get("duration") or 0)
        if not OK.match(lic) or not (50 <= dur <= 900): continue
        picks.append({"title": t, "url": ii["url"], "license": lic, "artist": g("Artist")[:120], "dur": dur, "query": q})
print(len(picks), "candidates")
done = []
for p in picks[:24]:
    slug = re.sub(r"[^a-z0-9]+", "_", p["title"][5:].rsplit(".", 1)[0].lower())[:40].strip("_")
    src = f"/tmp/{slug}.src"
    try:
        with urllib.request.urlopen(urllib.request.Request(p["url"], headers=UA), timeout=300) as r, open(src, "wb") as f:
            f.write(r.read())
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-ac", "2", "-ar", "44100", "-b:a", "160k", f"{OUT}/{slug}.mp3"], check=True)
        st = min(20, p["dur"] / 4)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(st), "-t", "25", "-i", src, "-af", "afade=t=in:d=1.5,afade=t=out:st=23:d=2", "-ac", "2", "-b:a", "128k", f"{OUT}/previews/{slug}.mp3"], check=True)
        p["slug"] = slug; done.append(p); print("OK", slug, p["license"], int(p["dur"]))
    except Exception as e:
        print("FAIL", slug, e)
json.dump(done, open(f"{OUT}/licenses.json", "w"), indent=1)
