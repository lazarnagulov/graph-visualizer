#!/bin/bash

if [ -d "venv" ]; then
    echo "Removing existing environment."
    rm -rf venv
fi

echo "Creating environment."
python -m venv venv
source venv/bin/activate

echo "Environment has been activated successfully!"