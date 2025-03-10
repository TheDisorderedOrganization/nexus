#!/bin/bash

# Define the output file
output_file="combined_output.xyz"

# Create or empty the output file
> "$output_file"

# Find all list.txt files using fdfind
list_files=$(find ./ -name list.txt)

# Check if any list.txt files were found
if [[ -z "$list_files" ]]; then
    echo "No list.txt files found!"
    exit 1
fi

# Process each list.txt file
for list_file in $list_files; do
    # Read each line from the current list.txt
    while IFS= read -r file_path; do
        # Check if the file exists
        if [[ -f "$file_path" ]]; then
            # Append the content of the file to the output file
            cat "$file_path" >> "$output_file"
        else
            echo "File $file_path not found, skipping..."
        fi
    done < "$list_file"
done

echo "All files have been combined into $output_file"