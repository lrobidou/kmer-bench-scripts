DATA_DIR="$1"
# GGCAT_INDEX_DIR="$2"

COLOR_MAPPING_FILE="$DATA_DIR"/GGCAT_color_mapping.in


# Loop through each .fastq.gz file in the directory
for file in "$DATA_DIR"/*.fasta; do
  # Extract the base name (everything before the first underscore)
  base_name=$(basename "$file" | cut -d'_' -f1)
  # Write the base name and full path to the output file
  echo "$base_name	$file" >> "$COLOR_MAPPING_FILE"
done
