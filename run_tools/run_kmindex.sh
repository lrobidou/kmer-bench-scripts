#!/bin/bash

DATA_DIR="$1"
INDEX_FOLDER="$2"

FOF="$INDEX_FOLDER"/kmindex_fof.txt

mkdir -p "${INDEX_FOLDER}"

# Erase the output file if it exists
rm ${FOF}

# Generate the new kmindex_fof.txt content
ls "${DATA_DIR}" | grep fastq.gz | cut -d_ -f1 | sort | uniq | while read -r prefix; do
    echo "${prefix}: ${DATA_DIR}/${prefix}_1.fastq.gz ; ${DATA_DIR}/${prefix}_2.fastq.gz" >> ${FOF}
done


#mkdir -p indexes/kmindex
cd $INDEX_FOLDER
kmindex build --fof $FOF --run-dir ./D1 --index ./G --register-as CCLE --hard-min 2 --kmer-size 25 --nb-cell 123792627 --bitw 5
