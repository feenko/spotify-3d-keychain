#!/bin/bash

clear_screen() {
    if [ "$OSTYPE" == "linux-gnu"* ]; then
        clear
        elif [ "$OSTYPE" == "darwin"* ]; then
        clear
    else
        echo "Unknown OS. Cannot clear screen."
    fi
}

# Check if the 'venv' folder exists
if [ -d "venv" ]; then
    echo "Virtual environment already exists."
else
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
if [ "$OSTYPE" == "linux-gnu"* ] || [ "$OSTYPE" == "darwin"* ]; then
    source venv/bin/activate
else
    echo "Unsupported OS. Exiting."
    exit 1
fi

# Install dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies... (This may take a while)"
    python3 -m pip install -r requirements.txt --quiet
else
    echo "requirements.txt not found!"
    deactivate
    exit 1
fi

# Clear the screen
clear_screen

# Run the main.py script
if [ -f "main.py" ]; then
    echo "Running main.py..."
    python3 main.py
else
    echo "main.py not found!"
    deactivate
    exit 1
fi

# Deactivate virtual environment after execution
deactivate