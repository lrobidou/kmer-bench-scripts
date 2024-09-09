#!/bin/bash

KMC_DIR="$1"
BQF_BIN="$2"
INDEX_DIR="$3"

# FOFS_DIR="$DATA_DIR"/kmc_fofs
# KMC_OUTPUT_FOLDER="$DATA_DIR"/kmc
OPTIONS="-q 28 -z 6 -k 31 -c 5"

mkdir -p $INDEX_DIR

KMC_FILES=$(ls $KMC_DIR | grep "_counted")

# Function to run bqf in a subdirectory
run_bqf() {
  KMC_FILE=$1
  BASE_NAME=$(basename "$KMC_FILE" | cut -d'_' -f1)
  RES_FILE="$INDEX_DIR"/"$BASE_NAME".bqf
  $BQF_BIN build $OPTIONS -i "${KMC_DIR}"/$KMC_FILE -o $RES_FILE
}

export -f run_bqf
export OPTIONS BQF_BIN INDEX_DIR KMC_DIR

# Run the bcalm command in parallel for each subdirectory
printf "%s\n" "${KMC_FILES[@]}" | parallel run_bqf
