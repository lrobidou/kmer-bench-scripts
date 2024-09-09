#!/bin/bash

UST_DIR="$1"
sshash_bin="$2"
index_destination="$3"

options="-k 31 -m 20 --weighted --canonical-parsing"


ust_files=$(ls $UST_DIR | grep "fa.ust.fa")

mkdir -p $index_destination

# Function to run SSHash in a subdirectory
run_sshash() {
  UST_FILE=$1
  output="${index_destination}/${UST_FILE}"
  WORKDIR="${index_destination}/${UST_FILE}_tmp"
  mkdir -p $WORKDIR
  cd $WORKDIR
  filename=$(basename ${UST_FILE})
  $sshash_bin build -i "${UST_DIR}/${UST_FILE}" -o "${index_destination}/${filename}.index" $options
}

export -f run_sshash
export UST_DIR sshash_bin index_destination options

# Run the bcalm command in parallel for each subdirectory
printf "%s\n" "${ust_files[@]}" | parallel run_sshash
