query_res_folder=$1
query_file=$2

first_line_of_REINDEER=$(head -n 1 ${query_res_folder}/reindeer.txt )

python to_tsv/bqf.py -i ${query_res_folder}/bqf -q ${query_file} -o to_tsv/bqf.tsv -d "${first_line_of_REINDEER}"
python to_tsv/ggcat.py -i ${query_res_folder}/ggcat.jsonl -q ${query_file} -o to_tsv/ggcat.tsv -d "${first_line_of_REINDEER}"
python to_tsv/needle.py -i ${query_res_folder}/needle.out -o to_tsv/needle.tsv -d "${first_line_of_REINDEER}"
python to_tsv/squeakr.py -i ${query_res_folder}/squeakr -q ${query_file} -o to_tsv/squeakr.tsv -d "${first_line_of_REINDEER}"
python to_tsv/sshash.py -i ${query_res_folder}/sshash -o to_tsv/sshash.tsv -d "${first_line_of_REINDEER}"
# cat ${query_res_folder}/reindeer.txt > to_tsv/reindeer.tsv
sed -e 's/0-0://g' -e 's/\*/0/g' ${query_res_folder}/reindeer.txt > to_tsv/reindeer.tsv