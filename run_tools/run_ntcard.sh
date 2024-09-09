#!/bin/bash

DATA_DIR=$1
NTCARD_BIN=$2

mkdir -p "$DATA_DIR"/ntcards


FILES=$(ls "$DATA_DIR"/*_1.fastq.gz)

run_ntcard() {
#for file in "$DATA_DIR"/*_1.fastq.gz; do
  file=$1
  # Extract the base name (everything before the first underscore)
  base_name=$(basename "$file" | cut -d'_' -f1)

  file1="$DATA_DIR/${base_name}_1.fastq.gz"
  file2="$DATA_DIR/${base_name}_2.fastq.gz"
  output="${DATA_DIR}/ntcards/ntcard_${base_name}"
  # Write the base name and full path to the output file
  $NTCARD_BIN -t 8 -k 31 -o $output $file1 $file2 &> "${output}".output
}

export -f run_ntcard
export DATA_DIR NTCARD_BIN

# Run the ntcard command in parallel for each subdirectory
printf "%s\n" "${FILES[@]}" | parallel run_ntcard
