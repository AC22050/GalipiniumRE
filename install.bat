echo off 
 TITLE GalipiniumRE Browser Installation Tool
 COLOR 0A

echo Initializing GalipiniumRE Browser Installation Tool...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python was not found or is not added to PATH. Please install Python.
    pause
    exit /b %errorlevel%
)

echo Creating virtual environment (venv)...
python -m venv venv
call venv\Scripts\activate.bat

echo Installing required dependencies (PyQt6, PyQt6-WebEngine, cryptography, numpy)...
python -m pip install --upgrade pip
pip install PyQt6 PyQt6-WebEngine cryptography numpy

echo Installation completed successfully
pause
