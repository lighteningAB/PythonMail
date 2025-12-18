#!/bin/bash

# Script to setup Conda environment and run the surveyMail.py script

ENV_NAME="python-mail-env"

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Error: conda is not installed or not in PATH."
    exit 1
fi

echo "Setting up Conda environment: $ENV_NAME"

# Check if environment exists
if conda info --envs | grep -q "$ENV_NAME"; then
    echo "Environment $ENV_NAME already exists. Updating..."
    conda env update --file environment.yml --prune
else
    echo "Creating environment $ENV_NAME..."
    conda env create --file environment.yml
fi

# Activate the environment
# We need to source conda.sh to use 'conda activate' in a script
# Try to find conda.sh
if [ -f "$(conda info --base)/etc/profile.d/conda.sh" ]; then
    source "$(conda info --base)/etc/profile.d/conda.sh"
else
    echo "Warning: Could not find conda.sh. Trying direct activate..."
fi

conda activate $ENV_NAME

if [ $? -ne 0 ]; then
    echo "Error: Failed to activate environment."
    exit 1
fi

# Run the python script
if [ "$#" -eq 0 ]; then
    echo "Usage: ./run.sh <csv_file>"
    echo "Please provide the path to the CSV file containing email addresses."
else
    python surveyMail.py "$@"
fi

