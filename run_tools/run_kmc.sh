#!/bin/bash

DATA_DIR="$1"
KMC_BIN="$2"
KMC_TOOL_BIN="$3"

FOFS_DIR="$DATA_DIR"/kmc_fofs
KMC_OUTPUT_FOLDER="$DATA_DIR"/kmc
OPTIONS="-k25 -ci2 -v"


FOFS=$(ls $FOFS_DIR)

# mkdir -p $KMC_OUTPUT_FOLDER

# Function to run kmc in a subdirectory
run_kmc() {
  FOF=$1
  BASE_NAME=$(basename "$FOF" | cut -d'_' -f1)
  # echo $FOF $BASE_NAME
  KMC_TEMPDIR="${KMC_OUTPUT_FOLDER}/${BASE_NAME}_tmp"
  # echo $KMC_TEMPDIR
  mkdir -p $KMC_TEMPDIR

  RES_FILE="$KMC_OUTPUT_FOLDER"/"$BASE_NAME".res
  $KMC_BIN $OPTIONS @"${FOFS_DIR}/${FOF}" $RES_FILE $KMC_TEMPDIR
  $KMC_TOOL_BIN transform $RES_FILE dump "$KMC_OUTPUT_FOLDER"/"${BASE_NAME}_counted"
  rm -r $KMC_TEMPDIR
}

export -f run_kmc
export OPTIONS FOFS_DIR KMC_OUTPUT_FOLDER KMC_BIN KMC_TOOL_BIN

# Run the bcalm command in parallel for each subdirectory
printf "%s\n" "${FOFS[@]}" | parallel run_kmc
