# Build Installer Script for VJ Youtube Amaze
# This script builds the installer once Inno Setup is installed

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Building VJ Youtube Amaze Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check for Inno Setup in common locations
$innoSetupPaths = @(
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    "C:\Program Files\Inno Setup 6\ISCC.exe",
    "$env:LOCALAPPDATA\Microsoft\WinGet\Packages\JRSoftware.InnoSetup_*\InnoSetup\ISCC.exe"
)

$isccPath = $null
foreach ($path in $innoSetupPaths) {
    if ($path -like "*WinGet*") {
        $found = Get-ChildItem (Split-Path $path) -Recurse -Filter "ISCC.exe" -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
        if ($found) {
            $isccPath = $found
            break
        }
    } elseif (Test-Path $path) {
        $isccPath = $path
        break
    }
}

if (-not $isccPath) {
    Write-Host "[ERROR] Inno Setup not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Inno Setup:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://jrsoftware.org/isdl.php" -ForegroundColor White
    Write-Host "2. Or run: winget install --id JRSoftware.InnoSetup" -ForegroundColor White
    Write-Host "3. After installation, run this script again" -ForegroundColor White
    exit 1
}

Write-Host "[OK] Found Inno Setup at: $isccPath" -ForegroundColor Green
Write-Host ""

# Verify EXE exists
if (-not (Test-Path "dist\VJ_Youtube_Amaze.exe")) {
    Write-Host "[ERROR] EXE not found. Building EXE first..." -ForegroundColor Yellow
    & .\build_exe.bat
    if (-not (Test-Path "dist\VJ_Youtube_Amaze.exe")) {
        Write-Host "[ERROR] Failed to build EXE!" -ForegroundColor Red
        exit 1
    }
}

# Verify static files
if (-not (Test-Path "dist\static")) {
    Write-Host "[INFO] Copying static files..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path "dist\static" | Out-Null
    Copy-Item -Path "static\*" -Destination "dist\static\" -Recurse -Force
}

# Build installer
Write-Host "[INFO] Building installer..." -ForegroundColor Yellow
Write-Host ""

& $isccPath installer.iss

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "INSTALLER BUILT SUCCESSFULLY!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    $installerPath = "dist\VJ_Youtube_Amaze_Setup.exe"
    if (Test-Path $installerPath) {
        $installerSize = (Get-Item $installerPath).Length / 1MB
        Write-Host "Installer location: $installerPath" -ForegroundColor Cyan
        Write-Host "Installer size: $([math]::Round($installerSize, 2)) MB" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Ready to distribute!" -ForegroundColor Green
    }
} else {
    Write-Host "[ERROR] Failed to build installer!" -ForegroundColor Red
    exit 1
}
