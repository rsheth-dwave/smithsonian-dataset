# requires aria2 (sudo apt update && sudo apt install -y aria2)

set -e

SUBDIR=$1
JPEGONLY=true

mkdir -p images/$SUBDIR
cut -f5 metadata/$SUBDIR.tsv | sort -u > metadata/"$SUBDIR"_urls.txt
if [ "${JPEGONLY:-false}" = "true" ]
then
    grep -Ei '\.jpe?g$' metadata/"$SUBDIR"_urls.txt > metadata/"$SUBDIR"_jpg_urls.txt
    PTH=metadata/"$SUBDIR"_jpg_urls.txt 
else
    PTH=metadata/"$SUBDIR"_urls.txt 
fi
aria2c -i "$PTH" -x 16 -s 16 -j 16 -d images/$SUBDIR --summary-interval=1
