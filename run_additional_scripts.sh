#!/bin/bash

# 1. Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "creating additional data format based on fixations"

echo "computing reading measures"
python "$SCRIPT_DIR/additional_scripts/compute_reading_measures.py"

echo "merging reading measures with trial data"
python "$SCRIPT_DIR/additional_scripts/merge_reading_measures.py"

python "$SCRIPT_DIR/additional_scripts/generate_scanpaths.py"

echo "merging scanpaths with trial information and reading measures"
python "$SCRIPT_DIR/additional_scripts/merge_scanpaths.py"

echo "all files have been created"

