#!/bin/bash

COLOR_MAPPING_FILE="$1"
INDEX_DIR="$2"

GGCAT_INDEX_DIR=$INDEX_DIR/ggcat
mkdir -p $GGCAT_INDEX_DIR
cd $GGCAT_INDEX_DIR
ggcat build -k 31 -j 8 -c -d $COLOR_MAPPING_FILE -o ggcat_index.fasta
