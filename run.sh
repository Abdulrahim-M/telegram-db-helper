#!/usr/bin/env bash

# Check Python
python3 --version || { echo "Python3 not found"; exit 1; }


# Activate venv
source .venv/bin/activate


# Run main.py
python src/main.py
