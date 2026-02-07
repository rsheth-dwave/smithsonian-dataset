# python scan_resolutions.py /path/to/flat/dir
#
# requires pillow

import sys, os
from collections import Counter
from pathlib import Path

from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True  # helps with partially-downloaded/corrupt files

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}

def iter_images(root: Path):
    if root.is_file():
        yield root
    else:
        for p in root.rglob("*"):
            if p.is_file() and p.suffix.lower() in EXTS:
                yield p

def main(root_str: str):
    root = Path(root_str).expanduser()
    counter = Counter()
    bad = []

    for p in iter_images(root):
        try:
            with Image.open(p) as im:
                w, h = im.size  # reads metadata/header
            counter[(w, h)] += 1
        except Exception as e:
            bad.append((str(p), str(e)))

    total = sum(counter.values())
    print(f"Scanned: {total} images")
    print(f"Unique resolutions: {len(counter)}\n")

    for (w, h), n in counter.most_common(50):
        print(f"{w}x{h}\t{n}")

    if counter:
        ws = [w for (w, h) in counter for _ in range(counter[(w, h)])]
        hs = [h for (w, h) in counter for _ in range(counter[(w, h)])]
        print("\nMin W,H:", min(ws), min(hs))
        print("Max W,H:", max(ws), max(hs))

    if bad:
        print(f"\nUnreadable images: {len(bad)} (showing up to 20)")
        for p, e in bad[:20]:
            print("BAD:", p, "|", e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scan_resolutions.py /path/to/images_or_dir")
        sys.exit(2)
    main(sys.argv[1])

