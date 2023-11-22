To create the requirements in the main path, execute 

```python
pip freeze > requirements.txt
```


Show only my changes and save in file whitch the name of the branch. Only the key of jira. 
**Note** If the branch didn't have jira, I make the review in a branch by default. Maybe will be better create that 
branch or maybe ignored that cases
```bash
branch_name=$(git rev-parse --abbrev-ref HEAD)
branch_name_without_prefix=$(echo $branch_name | sed 's#.*/##')
pattern="([A-Z0-9]+-[0-9]+)"

if [[ $branch_name_without_prefix =~ $pattern ]]; then
    extracted_part="${match[1]}"
else
    # Use a default name or an error message
    extracted_part="BDEV-129"     
    echo "Warning: Branch name doesn't match the expected pattern. Using default name: $extracted_part"
fi
output_dir="src/data/input"
output_file="$output_dir/$extracted_part.txt"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

git diff --diff-filter=AM --unified=0 $branch_name -- '*.php' '*.js' '*.py' >> "$output_file"
```

