@echo off
echo ========================================
echo Starting YouTube Scraper...
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo [ERROR] .env file not found!
    echo.
    echo Please run install.bat first to set up your API key.
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    pause
    exit /b 1
)

echo [INFO] Starting server on http://localhost:8000
echo [INFO] The application will open in your browser automatically
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start server and open browser after a short delay
start "" "http://localhost:8000"
timeout /t 2 /nobreak >nul
python main.py

