#!/bin/bash

# Script to set up virtual environment and run ai_newsletter.py
# This script checks for venv, creates it if needed, installs dependencies, and runs the main script

VENV_PATH="/opt/general/ai_newsletter/venv"
PROJECT_PATH="/opt/general/ai_newsletter"

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment not found at $VENV_PATH"
    echo "Creating new virtual environment..."
    
    # Create virtual environment
    python3 -m venv "$VENV_PATH"
    
    if [ $? -eq 0 ]; then
        echo "✓ Virtual environment created successfully"
    else
        echo "✗ Failed to create virtual environment"
        exit 1
    fi
    
    # Activate virtual environment and install dependencies
    echo "Installing dependencies from requirements.txt..."
    source "$VENV_PATH/bin/activate"
    pip install -r "$PROJECT_PATH/requirements.txt"
    
    if [ $? -eq 0 ]; then
        echo "✓ Dependencies installed successfully"
    else
        echo "✗ Failed to install dependencies"
        exit 1
    fi
else
    echo "✓ Virtual environment already exists at $VENV_PATH"
    source "$VENV_PATH/bin/activate"
fi

# Run the Python script
echo "Running ai_newsletter.py..."
cd "$PROJECT_PATH"
python3 ai_newsletter.py

python3 send_email.py
