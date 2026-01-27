@echo off
echo ========================================
echo YouTube Scraper - Installation
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not installed!
    echo Please reinstall Python with pip included.
    pause
    exit /b 1
)

echo [OK] pip is available
echo.

REM Get YouTube API Key
echo ========================================
echo YouTube API Key Setup
echo ========================================
echo.
echo You need a YouTube Data API v3 key to use this application.
echo.
echo If you don't have one:
echo 1. Go to https://console.cloud.google.com/
echo 2. Create a new project (or select existing)
echo 3. Enable "YouTube Data API v3"
echo 4. Create credentials (API Key)
echo 5. Copy your API key
echo.
set /p API_KEY="Enter your YouTube API Key: "

if "%API_KEY%"=="" (
    echo [ERROR] API Key cannot be empty!
    pause
    exit /b 1
)

REM Create .env file
echo.
echo [INFO] Creating .env file...
echo YOUTUBE_API_KEY=%API_KEY% > .env
echo [OK] .env file created
echo.

REM Install dependencies
echo.
echo ========================================
echo Installing Dependencies
echo ========================================
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To run the application:
echo   1. Double-click run.bat
echo   2. Or open command prompt and type: python main.py
echo.
echo The application will open in your browser at:
echo   http://localhost:8000
echo.
pause

