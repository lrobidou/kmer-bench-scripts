#!/bin/bash

# Check if a directory is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Directory containing the files
DIR="$1"

mkdir -p "${DIR}/bcalm_fof"

# Loop through the files, assuming they are paired by the same prefix before the underscore
for file in ${DIR}/*_1.fastq.gz; do
    # Extract the prefix
    prefix=$(basename "$file" | cut -d_ -f1)

    # Construct the pair file names
    file1="${DIR}/${prefix}_1.fastq.gz"
    file2="${DIR}/${prefix}_2.fastq.gz"

    # Output file name
    output_file="${DIR}/bcalm_fof/${prefix}"

    # Write the pairs to the output file
    echo -e "$file1\n$file2" > "$output_file"
done
