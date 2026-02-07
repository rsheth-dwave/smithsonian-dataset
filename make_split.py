# python make_split.py SRC_DIR [SRC_DIR ...] DST_DIR [--val-ratio 0.02] [--seed 0] [--recursive]
#
# examples:
#   python make_split.py /path/ds1 /path/ds2 /abs/path/mydata
#   python make_split.py /path/flat_images /abs/path/mydata
#   python make_split.py /path/ds1 /path/ds2 /abs/path/mydata --recursive --val-ratio 0.05

import os, random, argparse, hashlib
from pathlib import Path

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

def iter_images(src: Path, recursive: bool):
    it = src.rglob("*") if recursive else src.iterdir()
    for p in it:
        if p.is_file() and p.suffix.lower() in EXTS:
            yield p

def safe_link_name(src: Path, p: Path) -> str:
    """
    Make a deterministic unique filename for the symlink:
    <srcdir>__<relative_path_with__/__separators>
    Also shortens if name gets too long for common filesystems.
    """
    rel = p.relative_to(src)
    base = f"{src.name}__" + "__".join(rel.parts)  # includes original filename
    # If very long, replace middle with a hash to avoid PATH_MAX issues.
    if len(base) > 240:
        h = hashlib.sha1(str(rel).encode("utf-8")).hexdigest()[:12]
        base = f"{src.name}__{rel.name}__{h}"
    return base

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+", help="SRC_DIR [SRC_DIR ...] DST_DIR (dst must be last)")
    ap.add_argument("--val-ratio", type=float, default=0.02)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--recursive", action="store_true")
    args = ap.parse_args()

    if len(args.paths) < 2:
        raise SystemExit("Need at least 1 SRC_DIR and 1 DST_DIR")

    *src_args, dst_arg = args.paths
    srcs = [Path(p) for p in src_args]
    dst = Path(dst_arg)

    for s in srcs:
        if not s.is_dir():
            raise SystemExit(f"Not a directory: {s}")

    # Collect (src, image_path) pairs
    items = []
    seen = set()  # de-dupe if sources overlap
    for src in srcs:
        for p in iter_images(src, args.recursive):
            rp = p.resolve()
            if rp in seen:
                continue
            seen.add(rp)
            items.append((src, p))

    assert items, f"No images found in any of: {', '.join(map(str, srcs))}"

    rng = random.Random(args.seed)
    rng.shuffle(items)

    n_val = max(1, int(len(items) * args.val_ratio))
    val, train = items[:n_val], items[n_val:]

    for split, subset in [("train", train), ("val", val)]:
        out = dst / split / "0"
        out.mkdir(parents=True, exist_ok=True)

        for src, p in subset:
            name = safe_link_name(src, p)
            link = out / name

            # Extremely unlikely now, but just in case:
            if link.exists():
                # add a tiny deterministic suffix based on full path
                h = hashlib.sha1(str(p.resolve()).encode("utf-8")).hexdigest()[:8]
                link = out / f"{link.stem}__{h}{link.suffix}"

            os.symlink(p.resolve(), link)

    print(f"Done. total={len(items)} train={len(train)} val={len(val)} -> {dst}")

if __name__ == "__main__":
    main()

