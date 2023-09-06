#!/bin/bash

# Define variables
source_dir="img_crawl_fb"          # Change this to the source directory path
subfolder_dir="subfolder"  # Change this to the subfolder path
file_count=0             # Counter for moved files
max_count=19000

# Create the subfolder if it doesn't exist
mkdir -p "$subfolder_dir"

# Loop through files in the source directory
for file in "$source_dir"/*; do
    if [ -f "$file" ]; then  # Check if it's a regular file
        mv "$file" "$subfolder_dir/"
        ((file_count++))

        if [ "$file_count" -eq $max_count ]; then
            break
        fi
    fi
done

echo "Moved $file_count files to $subfolder_dir."
