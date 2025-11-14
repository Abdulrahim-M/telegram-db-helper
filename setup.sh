#!/usr/bin/env bash

# Check Python
python3 --version || { echo "Python3 not found"; exit 1; }

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run main.py
python src/main.py
