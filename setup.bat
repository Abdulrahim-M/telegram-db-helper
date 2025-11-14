@echo off
:: Check Python
python --version || (
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

:: Run main.py
python src\main.py
