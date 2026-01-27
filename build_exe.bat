@echo off
echo ========================================
echo Building VJ Youtube Amaze EXE
echo ========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [INFO] Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] Failed to install PyInstaller!
        pause
        exit /b 1
    )
)

echo [1/2] Building EXE with PyInstaller...
echo.

REM Build EXE using spec file
python -m PyInstaller youtube_scraper.spec

if errorlevel 1 (
    echo [ERROR] Failed to build EXE!
    pause
    exit /b 1
)

echo.
echo [2/2] Copying static files...
if not exist "dist\static" mkdir "dist\static"
xcopy /E /I /Y static\* dist\static\ >nul

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo EXE Location: dist\VJ_Youtube_Amaze.exe
echo.
echo Next step: Build the installer using Inno Setup
echo   1. Install Inno Setup from: https://jrsoftware.org/isdl.php
echo   2. Run: "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
echo.
pause
