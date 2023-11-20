#!/bin/bash

branch_name=$(git rev-parse --abbrev-ref HEAD)
# shellcheck disable=SC2001
branch_name_without_prefix=$(echo "$branch_name" | sed 's#.*/##')
pattern="([A-Z0-9]+-[0-9]+)"

if [[ $branch_name_without_prefix =~ $pattern ]]; then
    extracted_part="${BASH_REMATCH[1]}"
else
    # Use a default name or an error message
    extracted_part="BDEV-129"
    echo "Warning: Branch name doesn't match the expected pattern. Using default name: $extracted_part"
fi
output_dir="src/data/input"
output_file="$output_dir/$extracted_part.txt"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

git diff --diff-filter=A --unified=0 "$branch_name" -- '*.php' '*.js' '*.py' >> "$output_file"