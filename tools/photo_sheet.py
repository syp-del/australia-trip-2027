#!/usr/bin/env python3
"""Contact sheets of candidates. usage: photo_sheet.py <out_prefix> <cand_dir>..."""
import os, sys
from PIL import Image, ImageDraw
out, dirs = sys.argv[1], sys.argv[2:]
items = {}
for d in dirs:
    for f in sorted(os.listdir(d)):
        if f.endswith(".jpg"):
            items.setdefault(f.rsplit("_", 1)[0], []).append((os.path.basename(d), os.path.join(d, f)))
ids, W, H, per = sorted(items), 200, 126, 15
for n in range(0, len(ids), per):
    chunk = ids[n:n + per]
    cols = max(len(items[i]) for i in chunk)
    im = Image.new("RGB", (110 + cols * W, len(chunk) * H), "white")
    dr = ImageDraw.Draw(im)
    for r, i in enumerate(chunk):
        dr.text((4, r * H + 55), i[:16], fill="black")
        for c, (src, fp) in enumerate(items[i]):
            try:
                t = Image.open(fp).convert("RGB"); t.thumbnail((W - 4, H - 4)); im.paste(t, (110 + c * W, r * H + 2))
                dr.rectangle((110 + c * W, r * H + 2, 110 + c * W + 62, r * H + 14), fill="black")
                dr.text((112 + c * W, r * H + 3), f"{src[-2:]}:{os.path.basename(fp).rsplit('_',1)[1][:-4]}", fill="yellow")
            except Exception:
                pass
    im.save(f"{out}_{n // per}.jpg", quality=70)
    print(f"{out}_{n // per}.jpg", " ".join(chunk))
