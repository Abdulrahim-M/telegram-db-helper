@echo off
setlocal enabledelayedexpansion

REM --------------------------
REM Configuration
REM --------------------------
set FILE_TO_CHECK=src\config.json
set PYTHON_SCRIPT=src\init_script.py
set PYTHON_FUNCTION=create_config
REM --------------------------

:: Check Python
python --version >nul 2>&1 || (
    echo Python not found
    exit /b 1
)

:: Create venv if it doesn't exist
if not exist .venv (
    python -m venv .venv
)

:: Activate venv
call .venv\Scripts\activate

:: Upgrade pip
python -m pip install --upgrade pip

:: Install dependencies
pip install -r requirements.txt

:: Check if file exists
if not exist "%FILE_TO_CHECK%" (
    echo no %FILE_TO_CHECK% was found, creating it with a default SQLite database...

    :: Call a Python function to create it
    python - <<EOF
from %PYTHON_SCRIPT:\=.% import %PYTHON_FUNCTION%
%PYTHON_FUNCTION%()
EOF
)

:: Run main.py
python src\main.py

endlocal
