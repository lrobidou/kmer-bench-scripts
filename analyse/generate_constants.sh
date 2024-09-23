#!/bin/bash

TSV_FOLDER=$1
K=$2
ALPHA=$3

FILES=$(find $TSV_FOLDER -name "*.tsv" -exec basename {} .tsv \;)

for FILE in $FILES; do
  echo "${FILE} = \"${TSV_FOLDER}/${FILE}.tsv\""
done

echo "k = ${K}"
echo "alpha = ${ALPHA}"

mkdir -p graphs/mustaches/kmers/
mkdir -p graphs/mustaches/reads/
# sshash = "SSHash/query/query_fusion/query_fusion.tsv"
# ggcat = "ggcat/query_fusion.tsv"
# needle = "needle/query_fusion.tsv"
# reindeer = "REINDEER/query_fusion.tsv"
# kmindex = "kmindex/query_fusion_19G.tsv"
# bqf = "bqf/query_results/query_results_fusion_18G.tsv"
# squeakr = "squeakr/query_fusion/query.tsv"
# 
# 
# 
# k = 31
# alpha = 0.4