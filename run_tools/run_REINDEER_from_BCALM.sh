#!/bin/bash

data_folder_path="$1"
indexes_folder="$2"

fof_file="$data_folder_path"/REINDEER_fof.txt

# Remove REINDEER_fof.txt if it exists
[ -f "$fof_file" ] && rm "$fof_file"

mkdir -p $indexes_folder

# write the REINDEER_fof.txt
find "$data_folder_path"/* -type f -name '*.fa' > "$fof_file"

cd tools/REINDEER
./Reindeer --index -t 8 -f "$fof_file" -o "$indexes_folder"
# cd -

