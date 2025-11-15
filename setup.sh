#!/usr/bin/env bash
set -e

########################################
# Configuration
########################################
FILE_TO_CHECK="config.json"
PYTHON_SCRIPT="src/init_script.py"
PYTHON_FUNCTION="create_config"
########################################

# Check Python
if ! python3 --version >/dev/null 2>&1; then
    echo "Python3 not found"
    exit 1
fi

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Activate venv
# shellcheck disable=SC1091
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

########################################
# Check if file exists
########################################
if [ ! -f "$FILE_TO_CHECK" ]; then
    echo "No $FILE_TO_CHECK found, creating it with default SQLite database..."

    python3 - <<EOF
from ${PYTHON_SCRIPT//\//.} import $PYTHON_FUNCTION
$PYTHON_FUNCTION()
EOF
fi

########################################
# Run main.py
########################################
python src/main.py
