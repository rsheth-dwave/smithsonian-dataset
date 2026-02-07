# vipsthumbnail runs files one after another
# 
# requires parallel, libvips-tools

IN=/home/user/smithsonian-dataset/images/npg_128
OUT=/home/user/smithsonian-dataset/images/npg_64

mkdir -p "$OUT"

export VIPS_CONCURRENCY=1      # 1 thread per process (good for throughput)
J=$(nproc)                     # number of processes

find "$IN" -maxdepth 1 -type f -print0 \
| parallel -0 -q -j "$J" --bar -- \
  vipsthumbnail --size '1024x1024>' --rotate \
    -o "$OUT/%s.jpg[Q=90,optimize_coding,keep=none]" \
    {}

# --size MxN shrinks to fit within the box; > means only if input is larger.
# --rotate is the documented EXIF autorotate flag.
# -o supports output options like Q=... and keep=none (metadata stripping) in brackets.
