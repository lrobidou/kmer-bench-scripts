#!/bin/bash

# BCALM Directory
BCALM_DIR=$1

# Path to UST binary
UST_BIN=$2

# Parameters for UST
PARAMS="-k 31 -a 1"

# Gather subdirectory names automatically
BCALM_FILES=($(ls $BCALM_DIR ))

# Function to run UST in a subdirectory
run_ust() {
  BCALM_FILE=$1
  mkdir "${BCALM_DIR}/${BCALM_FILE}_tmp"
  cd "${BCALM_DIR}/${BCALM_FILE}_tmp"
  $UST_BIN -i "${BCALM_DIR}/${BCALM_FILE}" $PARAMS
  cd ..
}

export -f run_ust
export BCALM_DIR UST_BIN PARAMS

# Run the bcalm command in parallel for each subdirectory
printf "%s\n" "${BCALM_FILES[@]}" | parallel run_ust
