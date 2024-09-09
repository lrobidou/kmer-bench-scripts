#!/bin/bash

fastq_files=$(ls *.gz)

# Function to run SSHash in a subdirectory
run_uncompress() {
  FILENAME=$1
  BASENAME=$(basename "$FILENAME")
  BASENAME="${BASENAME%.*}"
  BASENAME="${BASENAME%.*}"
  zcat $FILENAME | sed -n '1~4s/^@/>/p;2~4p' > $BASENAME.fasta
}

export -f run_uncompress
export fastq_files

# Run the bcalm command in parallel for each subdirectory
printf "%s\n" "${fastq_files[@]}" | parallel run_uncompress
