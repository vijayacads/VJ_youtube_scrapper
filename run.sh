#!/bin/bash

echo "========================================"
echo "Starting YouTube Scraper..."
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "[ERROR] .env file not found!"
    echo ""
    echo "Please run ./install.sh first to set up your API key."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed!"
    exit 1
fi

echo "[INFO] Starting server on http://localhost:8000"
echo "[INFO] The application will open in your browser automatically"
echo ""
echo "To stop the server:"
echo "  - Click the 'Stop Server' button in the web interface, OR"
echo "  - Press Ctrl+C in this terminal"
echo ""

# Open browser (works on macOS and most Linux)
if command -v open &> /dev/null; then
    # macOS
    open "http://localhost:8000" &
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open "http://localhost:8000" &
fi

# Small delay to let browser open
sleep 2

# Start server
python3 main.py

