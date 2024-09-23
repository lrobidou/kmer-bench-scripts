DATA_DIR=$1
NTCARD_DIR=$2
LOGNUMSLOT=$3
SQUEAKR_BIN=$4
INDEX_FOLDER=$5

extract_number() {
    local filename="$1"
    local number=$(grep 'F0' "$filename" | awk '{print $3}')
    echo "$number"
}

compute_parameter() {
    local ntcard_file=$1
    local number=$(extract_number "${ntcard_file}.output")
    local to_return=$($LOGNUMSLOT $ntcard_file $number)
    echo $to_return
}

FASTQ_FILES=$(ls $DATA_DIR/*_1.fastq.gz)
OPTIONS="-e -k 31 -c 2 -t 8"

mkdir -p $INDEX_FOLDER

run_squeakr() {
  FASTQ_FILE=$1
  BASE_NAME=$(basename "$FASTQ_FILE" | cut -d'_' -f1)
  NTCARD_FILE="ntcard_${BASE_NAME}"
  parameter=$(compute_parameter "${NTCARD_DIR}/${NTCARD_FILE}")
  # echo $parameter
  FILE1="${DATA_DIR}/${BASE_NAME}_1.fastq.gz"
  FILE2="${DATA_DIR}/${BASE_NAME}_2.fastq.gz"

  $SQUEAKR_BIN count $OPTIONS -s $parameter -o "${INDEX_FOLDER}/${BASE_NAME}.squeakr" $FILE1 $FILE2
}

export -f run_squeakr compute_parameter extract_number
export NTCARD_DIR LOGNUMSLOT SQUEAKR_BIN INDEX_FOLDER OPTIONS DATA_DIR

# Run the bcalm command in parallel for each subdirectory
printf "%s\n" "${FASTQ_FILES[@]}" | parallel run_squeakr
