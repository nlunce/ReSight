import re
import os
import datetime

def create_qmd_template(title):
    """Create a basic template for .qmd files"""
    return f"""---
title: "{title.replace('_', ' ').title()}"
date: {datetime.datetime.now().strftime('%Y-%m-%d')}
---

# {title.replace('_', ' ').title()}

[Add content here]

## Overview

[Add overview here]

## Details

[Add detailed content here]

## Notes

[Add any additional notes here]
"""

# Find all unique missing file targets
with open('error_log.txt', 'r') as file:
    content = file.read()

# Extract all unique file paths from WARN messages
missing_files = set(re.findall(r'Unable to resolve link target: ([^\n]+)', content))

print(f"Found {len(missing_files)} unique missing files:")
for file in missing_files:
    print(f"  - {file}")

print("\nCreating files...")

# Create each missing file
for file_path in missing_files:
    # Create the directory if it doesn't exist
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    
    # Only create file if it doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            # Get the base name without extension and use it as title
            title = os.path.splitext(os.path.basename(file_path))[0]
            f.write(create_qmd_template(title))
        print(f"Created file: {file_path}")
    else:
        print(f"File already exists: {file_path}")

print("\nAll missing files have been created!")