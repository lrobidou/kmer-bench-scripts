DATA_DIR=$1

mkdir -p "$DATA_DIR"/kmc_fofs

# Loop through each .fastq.gz file in the directory
for file in "$DATA_DIR"/*.fastq.gz; do
  # Extract the base name (everything before the first underscore)
  base_name=$(basename "$file" | cut -d'_' -f1)
  # Write the base name and full path to the output file
  echo "$file" >> "$DATA_DIR"/kmc_fofs/"$base_name"_fof
done
