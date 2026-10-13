#!/usr/bin/env python3
"""Download openly licensed photo candidates. usage: photo_fetch.py <openverse|commons> <out_dir> <queries.json>"""
import json, os, re, subprocess, sys, time, urllib.parse
UA = "AustraliaTripGuide/1.0 (personal family trip planner; github.com/syp-del/australia-trip-2027)"
SRC, OUT, Q = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3]))
N = 4
os.makedirs(OUT, exist_ok=True)
meta_path = os.path.join(OUT, "meta.json")
meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
OKLIC = re.compile(r"^(CC BY|CC0|Public domain|CC-BY|PD)", re.I)

def get(url):
    r = subprocess.run(["curl", "-sS", "-f", "-L", "-m", "40", "-A", UA, url], capture_output=True)
    if r.returncode:
        raise RuntimeError(r.stderr.decode()[:120])
    return r.stdout

def openverse(query):
    api = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(
        {"q": query, "license": "by,by-sa,cc0,pdm,by-nc,by-nc-sa", "page_size": 12, "aspect_ratio": "wide,square"})
    for p in json.loads(get(api)).get("results", []):
        if (p.get("width") or 0) < 600:
            continue
        url = p["url"]
        if "staticflickr" in url and re.search(r"_[a-z]\.jpg$", url):
            url = re.sub(r"_[a-z]\.jpg$", "_z.jpg", url)
        lic = {"cc0": "CC0", "pdm": "Public domain"}.get(p["license"], ("CC " + p["license"].upper() + " " + (p.get("license_version") or "")).strip())
        yield url, {"title": p.get("title") or query, "license": lic, "artist": (p.get("creator") or "")[:80],
                    "page": p.get("foreign_landing_url") or p["url"]}

def commons(query):
    api = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query", "generator": "search", "gsrsearch": query + " filetype:bitmap", "gsrnamespace": 6, "gsrlimit": 20,
        "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiextmetadatafilter": "LicenseShortName|Artist",
        "iiurlwidth": 640, "format": "json"})
    pages = sorted(json.loads(get(api)).get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    for p in pages:
        ii = p["imageinfo"][0]
        lic = ii["extmetadata"].get("LicenseShortName", {}).get("value", "")
        if not OKLIC.match(lic) or ii["width"] < 1000 or ii["width"] < ii["height"] * 1.1:
            continue
        if not p["title"].lower().endswith((".jpg", ".jpeg")):
            continue
        artist = re.sub(r"<[^>]+>", "", ii["extmetadata"].get("Artist", {}).get("value", "")).strip()[:80]
        yield ii["thumburl"], {"title": p["title"], "license": lic, "artist": artist, "page": ii["descriptionurl"]}

for pid, query in Q.items():
    if any(k.startswith(pid + "_") for k in meta):
        continue
    k = 0
    try:
        for url, m in (openverse if SRC == "openverse" else commons)(query):
            try:
                data = get(url)
            except Exception:
                continue
            if len(data) < 5000:
                continue
            fn = f"{pid}_{k}.jpg"
            open(os.path.join(OUT, fn), "wb").write(data)
            meta[fn] = m
            k += 1
            if k >= N:
                break
    except Exception as e:
        print(pid, "FAIL", e, flush=True)
        time.sleep(8)
        continue
    print(pid, k, flush=True)
    json.dump(meta, open(meta_path, "w"), ensure_ascii=False, indent=1)
    time.sleep(3)
