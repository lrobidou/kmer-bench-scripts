#!/bin/bash
# Check if a directory is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <bcalm_output_folder>"
    exit 1
fi

BCALM_OUT_DIR="$1"

# Parameters for bcalm
PARAMS="-kmer-size 31 -abundance-min 2 -nb-cores 8 -all-abundance-counts"

# Gather dataset names automatically
BCALM_TMP_DIRS=($(ls $BCALM_OUT_DIR | grep _tmp))

# Function to run bcalm in a subdirectory
run_move_bcalm() {
  BCALM_TMP_DIR=$1
  mv "${BCALM_OUT_DIR}/${BCALM_TMP_DIR}"/* "${BCALM_OUT_DIR}/"
  # rm -r "${BCALM_OUT_DIR}/${BCALM_TMP_DIR}"  # dangerous if no BCALM_TMP_DIR...
}

echo "${BCALM_FOFS[@]}"
export -f run_move_bcalm
export BCALM_OUT_DIR

# Run the bcalm command in parallel for each subdirectory
printf "%s\n" "${BCALM_TMP_DIRS[@]}" | parallel run_move_bcalm
