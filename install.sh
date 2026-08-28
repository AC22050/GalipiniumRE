#!/usr/bin/env bash
set -e

echo "Initializing GalipiniumRE Browser Installation Tool..."

if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 could not be found on your system. Please install Python3 first."
    exit 1
fi

echo "Creating virtual environment (venv)..."
python3 -m venv venv
source venv/bin/activate

echo "Installing required dependencies (PyQt6, PyQt6-WebEngine, cryptography, numpy)..."
pip install --upgrade pip
pip install PyQt6 PyQt6-WebEngine cryptography numpy

echo "Installation completed successfully bro"
