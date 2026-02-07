# downloads jsonl index files
#
# https://github.com/Smithsonian/OpenAccess

BASEDIR=metadata/edan
SUBDIR=$1

mkdir -p $BASEDIR/$SUBDIR

aws s3 sync --no-sign-request \
  s3://smithsonian-open-access/metadata/edan/$SUBDIR/ \
  $BASEDIR/$SUBDIR/ \
  --exclude "*" --include "*.txt"
