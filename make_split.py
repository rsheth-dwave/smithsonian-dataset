# python make_split.py /path/flat_images /abs/path/mydata
#
# requires: pillow

import os, random, shutil, sys
from pathlib import Path

src = Path(sys.argv[1])
dst = Path(sys.argv[2])
val_ratio = 0.02
seed = 0

exts = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
imgs = [p for p in src.iterdir() if p.is_file() and p.suffix.lower() in exts]
assert imgs, f"No images found in {src}"

random.Random(seed).shuffle(imgs)
n_val = max(1, int(len(imgs) * val_ratio))
val, train = imgs[:n_val], imgs[n_val:]

for split, items in [("train", train), ("val", val)]:
    out = dst / split / "0"
    out.mkdir(parents=True, exist_ok=True)
    for p in items:
        link = out / p.name
        if link.exists(): continue
        os.symlink(p.resolve(), link)
print(f"Done. train={len(train)} val={len(val)} -> {dst}")

