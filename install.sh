#!/bin/bash

echo "========================================"
echo "YouTube Scraper - Installation"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed!"
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "  macOS: brew install python3"
    echo "  Linux: sudo apt-get install python3 python3-pip"
    echo ""
    exit 1
fi

echo "[OK] Python is installed"
python3 --version
echo ""

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "[ERROR] pip3 is not installed!"
    echo "Please install pip3:"
    echo "  python3 -m ensurepip --upgrade"
    echo ""
    exit 1
fi

echo "[OK] pip3 is available"
echo ""

# Get YouTube API Key
echo "========================================"
echo "YouTube API Key Setup"
echo "========================================"
echo ""
echo "You need a YouTube Data API v3 key to use this application."
echo ""
echo "If you don't have one:"
echo "1. Go to https://console.cloud.google.com/"
echo "2. Create a new project (or select existing)"
echo "3. Enable 'YouTube Data API v3'"
echo "4. Create credentials (API Key)"
echo "5. Copy your API key"
echo ""
read -p "Enter your YouTube API Key: " API_KEY

if [ -z "$API_KEY" ]; then
    echo "[ERROR] API Key cannot be empty!"
    exit 1
fi

# Create .env file
echo ""
echo "[INFO] Creating .env file..."
echo "YOUTUBE_API_KEY=$API_KEY" > .env
echo "[OK] .env file created"
echo ""

# Install dependencies
echo ""
echo "========================================"
echo "Installing Dependencies"
echo "========================================"
echo ""
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies!"
    exit 1
fi

echo ""
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "To run the application:"
echo "  1. Run: ./run.sh"
echo "  2. Or: python3 main.py"
echo ""
echo "The application will open in your browser at:"
echo "  http://localhost:8000"
echo ""

