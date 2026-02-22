#!/bin/bash

# Hotel Management System - Linux Launcher
# This script installs Python dependencies and runs the application.

echo "--- Grand Hotel Management System Launcher ---"

# 1. Check if python3-tk is installed (required for Tkinter on Linux)
if ! dpkg -s python3-tk >/dev/null 2>&1; then
    echo "Installing required system dependencies (python3-tk)..."
    sudo apt update
    sudo apt install -y python3-tk
fi

# 2. Check for dependencies in requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Checking Python dependencies..."
    # We use --break-system-packages as a last resort if not in venv, 
    # but ideally, users should use a venv.
    python3 -m pip install -r requirements.txt --break-system-packages
fi

# 3. Handle Detach Mode
DETACH=false
for arg in "$@"; do
    if [ "$arg" == "-d" ]; then
        DETACH=true
    fi
done

if [ "$DETACH" == "true" ]; then
    echo "Launching application in background..."
    # Use setsid or nohup to ensure it survives terminal exit
    nohup python3 main.py > hotel_app.log 2>&1 &
    
    # Wait a second to see if it crashes immediately
    sleep 1
    if ps -p $! > /dev/null; then
        echo "✅ App is running in the background (PID: $!)."
        echo "   The window should appear on your screen shortly."
        echo "   You can now safely close this terminal."
        disown
    else
        echo "❌ Error: App failed to start in background. Check 'hotel_app.log'."
        cat hotel_app.log
    fi
else
    echo "Launching application..."
    python3 main.py
fi

echo "Done."
