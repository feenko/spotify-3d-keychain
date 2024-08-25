#!/bin/bash

# Check if the 'venv' folder exists
if [ -d "venv" ]; then
    echo "Virtual environment already exists."
else
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies... This may take a while."
    python3 -m pip install -r requirements.txt -q
else
    echo "requirements.txt not found."
    deactivate
    exit 1
fi

# Clear the screen
clear

# Run the main.py script
if [ -f "main.py" ]; then
    echo "Executing program..."
    echo ""
    python3 main.py
else
    echo "main.py not found."
fi

# Deactivate the virtual environment
deactivate
