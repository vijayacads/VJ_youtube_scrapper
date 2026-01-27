# Auto-download and build installer script for VJ Youtube Amaze

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "VJ Youtube Amaze - Installer Builder" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$innoSetupPath = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

# Check if Inno Setup is installed
if (Test-Path $innoSetupPath) {
    Write-Host "[OK] Inno Setup found!" -ForegroundColor Green
} else {
    Write-Host "[INFO] Inno Setup not found. Downloading..." -ForegroundColor Yellow
    
    # Inno Setup download URL (direct link to latest stable)
    $innoSetupUrl = "https://jrsoftware.org/download.php/is-unicode.exe"
    $innoSetupInstaller = "$env:TEMP\innosetup-installer.exe"
    
    try {
        Write-Host "Downloading Inno Setup..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri $innoSetupUrl -OutFile $innoSetupInstaller -UseBasicParsing
        
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Yellow
        Write-Host "MANUAL INSTALLATION REQUIRED" -ForegroundColor Yellow
        Write-Host "========================================" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Inno Setup installer has been downloaded to:" -ForegroundColor White
        Write-Host $innoSetupInstaller -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Please:" -ForegroundColor White
        Write-Host "1. Run the installer" -ForegroundColor White
        Write-Host "2. Accept defaults (install to C:\Program Files (x86)\Inno Setup 6\)" -ForegroundColor White
        Write-Host "3. Run this script again" -ForegroundColor White
        Write-Host ""
        Write-Host "Opening installer now..." -ForegroundColor Yellow
        
        Start-Process $innoSetupInstaller
        Read-Host "Press Enter after installing Inno Setup to continue..."
        
        # Check again after installation
        if (-not (Test-Path $innoSetupPath)) {
            Write-Host "[ERROR] Inno Setup still not found. Please install manually." -ForegroundColor Red
            exit 1
        }
    } catch {
        Write-Host "[ERROR] Failed to download Inno Setup: $_" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please download manually from: https://jrsoftware.org/isdl.php" -ForegroundColor Yellow
        exit 1
    }
}

# Verify EXE exists
if (-not (Test-Path "dist\VJ_Youtube_Amaze.exe")) {
    Write-Host "[ERROR] EXE not found. Building EXE first..." -ForegroundColor Red
    Write-Host ""
    & .\build_exe.bat
    if (-not (Test-Path "dist\VJ_Youtube_Amaze.exe")) {
        Write-Host "[ERROR] Failed to build EXE!" -ForegroundColor Red
        exit 1
    }
}

# Verify static files exist
if (-not (Test-Path "dist\static")) {
    Write-Host "[INFO] Copying static files..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path "dist\static" | Out-Null
    Copy-Item -Path "static\*" -Destination "dist\static\" -Recurse -Force
}

# Build installer
Write-Host ""
Write-Host "[INFO] Building installer with Inno Setup..." -ForegroundColor Yellow
Write-Host ""

& $innoSetupPath installer.iss

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "INSTALLER BUILT SUCCESSFULLY!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Installer location: dist\VJ_Youtube_Amaze_Setup.exe" -ForegroundColor Cyan
    $installerSize = (Get-Item "dist\VJ_Youtube_Amaze_Setup.exe").Length / 1MB
    Write-Host "Installer size: $([math]::Round($installerSize, 2)) MB" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "[ERROR] Failed to build installer!" -ForegroundColor Red
    exit 1
}
