#!/usr/bin/env python3
"""Crop chosen candidates into img/ and record credits. usage: photo_apply.py <picks.json> ; picks = {id: "dir/file.jpg"}"""
import json, os, sys
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
picks = json.load(open(sys.argv[1]))
credits = json.load(open(R + "/img/credits.json"))
for pid, fp in picks.items():
    meta = json.load(open(os.path.join(os.path.dirname(fp), "meta.json")))[os.path.basename(fp)]
    im = Image.open(fp).convert("RGB"); w, h = im.size; r = 640 / 400
    if w / h > r:
        nw = int(h * r); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / r); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im.resize((640, 400), Image.LANCZOS).save(f"{R}/img/{pid}.jpg", quality=78, optimize=True)
    credits[pid] = meta
json.dump(credits, open(R + "/img/credits.json", "w"), ensure_ascii=False, indent=1)
print(len(picks), "applied;", len(credits), "credits")
