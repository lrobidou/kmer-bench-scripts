#!/bin/bash
# Check if a directory is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <fof_directory> <bcalm_binary> <bcalm_output_folder>"
    exit 1
fi
# Check if a directory is provided
if [ -z "$2" ]; then
    echo "Usage: $0 <fof_directory> <bcalm_binary> <bcalm_output_folder>"
    exit 1
fi

# Check if a directory is provided
if [ -z "$3" ]; then
    echo "Usage: $0 <fof_directory> <bcalm_output_folder>"
    exit 1
fi

# Directory containing fof
FOF_DIR="$1"

# Path to bcalm binary
BCALM_BIN="$2"

BCALM_OUT_DIR="$3"

# Parameters for bcalm
PARAMS="-kmer-size 31 -abundance-min 2 -nb-cores 8 -all-abundance-counts"

# Gather dataset names automatically
BCALM_FOFS=($(ls $FOF_DIR))

mkdir -p "$BCALM_OUT_DIR"

# Function to run bcalm in a subdirectory
run_bcalm() {
  BCALM_FOF=$1
  WORKDIR="$BCALM_OUT_DIR/${BCALM_FOF}_tmp"
  mkdir -p "$WORKDIR"
  cd "$WORKDIR"
  # echo ${BCALM_FOF}
  $BCALM_BIN -in "${FOF_DIR}/${BCALM_FOF}" $PARAMS
  cd ..
  # mv "${WORKDIR}/*" . 
  # rm -r "${WORKDIR}"
}

echo "${BCALM_FOFS[@]}"
export -f run_bcalm
export BCALM_OUT_DIR BCALM_BIN PARAMS FOF_DIR

# Run the bcalm command in parallel for each subdirectory
printf "%s\n" "${BCALM_FOFS[@]}" | parallel run_bcalm
