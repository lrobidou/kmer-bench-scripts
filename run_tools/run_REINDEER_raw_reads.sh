#!/bin/bash

folder_path="$1"
REINDEER_BIN=$2
INDEX_FOLDER=$3
fof_file="./REINDEER_fof.txt"

cd tools/REINDEER
# mkdir -p indexes/REINDEER

# Remove REINDEER_fof.txt if it exists
[ -f "$fof_file" ] && rm "$fof_file"

# crates REINDEER_fof.txt
find "$folder_path" -type f -name "*.fastq.gz" -exec readlink -f {} \; > "$fof_file"
sort "$fof_file" -o "$fof_file"

# cd tools/REINDEER
$REINDEER_BIN --index -t 12 --paired-end --bcalm  -f "$fof_file" -o $INDEX_FOLDER/REINDEER
cd -

