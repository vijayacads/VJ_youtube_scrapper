# VJ Youtube Amaze - Complete Installer Creation Guide

## Quick Summary

This guide covers the complete process of creating a professional Windows installer for VJ Youtube Amaze, including all automated setup features.

## Prerequisites

- Python 3.8+ installed
- All project dependencies installed (`pip install -r requirements.txt`)
- Windows OS (for building Windows installer)

## Step-by-Step Process

### Step 1: Build the EXE File

Run the build script:
```bash
build_exe.bat
```

Or manually:
```bash
python -m PyInstaller youtube_scraper.spec
```

**What this does:**
- Bundles all Python code into `dist\VJ_Youtube_Amaze.exe`
- Includes all dependencies (FastAPI, uvicorn, etc.)
- Includes static files (HTML, CSS, images)
- Creates a standalone executable (~72 MB)

**Output:** `dist\VJ_Youtube_Amaze.exe`

### Step 2: Copy Static Files

Ensure static files are in the dist folder:
```bash
# PowerShell
New-Item -ItemType Directory -Force -Path "dist\static" | Out-Null
Copy-Item -Path "static\*" -Destination "dist\static\" -Recurse -Force
```

### Step 3: Install Inno Setup

**Option A: Using winget (Recommended)**
```bash
winget install --id JRSoftware.InnoSetup
```

**Option B: Manual Download**
1. Go to: https://jrsoftware.org/isdl.php
2. Download and install Inno Setup 6
3. Accept default installation path

### Step 4: Build the Installer

**Option A: Using the automated script**
```bash
powershell -ExecutionPolicy Bypass -File build_installer.ps1
```

**Option B: Manual build**
```bash
"C:\Users\<username>\AppData\Local\Programs\Inno Setup 6\ISCC.exe" installer.iss
```

Or if installed in Program Files:
```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

**Output:** `dist\VJ_Youtube_Amaze_Setup.exe` (~73 MB)

## What the Installer Includes

✅ **Desktop Shortcut** (optional during install)  
✅ **Start Menu Shortcut** (in "VJ Youtube Amaze" folder)  
✅ **Auto-launch** after installation  
✅ **First-run Detection** - Shows API key setup if not configured  
✅ **Professional Installer Wizard** - Standard Windows experience  
✅ **Uninstaller** - Can be removed via Control Panel  

## User Experience Flow

1. **User downloads:** `VJ_Youtube_Amaze_Setup.exe`
2. **Runs installer:** Standard Windows wizard
3. **Chooses options:** Desktop shortcut (optional)
4. **Installation completes:** App auto-launches
5. **First run:** Browser opens to API key setup page
6. **User enters API key:** Clear step-by-step instructions
7. **Saves and redirects:** Main application ready to use

## Key Files Created

| File | Purpose |
|------|---------|
| `launcher.py` | Entry point for EXE - starts server and opens browser |
| `youtube_scraper.spec` | PyInstaller configuration |
| `installer.iss` | Inno Setup installer script |
| `static/setup.html` | API key setup page with non-technical instructions |
| `build_exe.bat` | Script to build EXE |
| `build_installer.ps1` | Script to build installer |

## Features Implemented

### 1. First-Run Detection
- Checks for `.env` file in user data directory (`%APPDATA%\VJ Youtube Amaze\.env`)
- If missing, shows setup page
- If exists, goes directly to main app

### 2. API Key Setup Page
- Step-by-step instructions for non-technical users
- Visual guide with links
- Validates API key format
- Saves to user data directory (not installation folder)

### 3. User Data Storage
- `.env` file stored in: `%APPDATA%\VJ Youtube Amaze\.env`
- Works across Windows, Linux, Mac
- Survives app updates/uninstalls (if user data preserved)

## Troubleshooting

### EXE won't build
- Check PyInstaller is installed: `pip install pyinstaller`
- Verify all dependencies in `requirements.txt` are installed

### Installer won't build
- Verify Inno Setup is installed
- Check `installer.iss` file exists
- Ensure `dist\VJ_Youtube_Amaze.exe` exists

### API key not saving
- Check write permissions to `%APPDATA%\VJ Youtube Amaze\`
- Verify `python-dotenv` is installed

## Distribution

**Final file to distribute:**
- `dist\VJ_Youtube_Amaze_Setup.exe` (~73 MB)

Users only need this one file - everything else is bundled inside!

## Quick Build Commands

```bash
# Complete build process
.\build_exe.bat                    # Build EXE
powershell -File build_installer.ps1  # Build installer

# Or all at once (if Inno Setup is installed)
.\build_exe.bat && powershell -File build_installer.ps1
```

## Notes

- The installer uses LZMA2 compression for smaller file size
- EXE is built with console enabled (for debugging) - can be disabled in spec file
- All static files are bundled in the installer
- First-run detection works automatically - no manual configuration needed
