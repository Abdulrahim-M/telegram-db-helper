@echo off
:: Check Python
python --version || (
    echo Python not found
    exit /b 1
)

:: Activate venv
call .venv\Scripts\activate

:: Run main.py
python src\main.py
