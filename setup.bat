@echo off

REM Check if the 'venv' folder exists
if exist venv (
    echo Virtual environment already exists.
) else (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Install dependencies from requirements.txt
if exist requirements.txt (
    echo Installing dependencies... This may take a while.
    pip install -r requirements.txt -q
) else (
    echo requirements.txt not found!
    deactivate
    exit /b
)

REM Clear the screen
cls

REM Run the main.py script
if exist main.py (
    echo Executing program...
    echo.
    python main.py
) else (
    echo main.py not found!
    deactivate
)

REM Deactivate the virtual environment
deactivate