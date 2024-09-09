DATA_DIR=$1
INDEX_NEEDLE_DIR=$2
NEEDLE_BIN=$3

mkdir -p $INDEX_NEEDLE_DIR
cd $INDEX_NEEDLE_DIR

PARAMETERS1="--paired -k 31 -t 8"
PARAMETERS2="-t 8 -f 0.05 -l 15 "
FILES=$(ls $DATA_DIR/*.fastq.gz)

$NEEDLE_BIN minimiser $FILES $PARAMETERS1
$NEEDLE_BIN ibfmin $PARAMETERS2 *.minimiser -o needle.index
