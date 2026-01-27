# Build Instructions for VJ Youtube Amaze - Quick Guide

## Complete Process Summary

### Step 1: Build the EXE
```bash
build_exe.bat
```
**Output:** `dist\VJ_Youtube_Amaze.exe` (~72 MB)

### Step 2: Install Inno Setup
```bash
winget install --id JRSoftware.InnoSetup
```
Or download from: https://jrsoftware.org/isdl.php

### Step 3: Build the Installer
```bash
powershell -ExecutionPolicy Bypass -File build_installer.ps1
```
**Output:** `dist\VJ_Youtube_Amaze_Setup.exe` (~73 MB)

## Quick Build (All Steps)
```bash
.\build_exe.bat && powershell -File build_installer.ps1
```

## What We Built

1. **EXE File** - Standalone executable with all dependencies
2. **Installer** - Professional Windows installer with:
   - Desktop shortcut
   - Start Menu shortcut  
   - Auto-launch after install
   - First-run API key setup
   - Uninstaller

## Key Files Created

- `launcher.py` - EXE entry point
- `youtube_scraper.spec` - PyInstaller config
- `installer.iss` - Inno Setup script
- `static/setup.html` - API key setup page
- `build_exe.bat` - EXE build script
- `build_installer.ps1` - Installer build script

## User Experience

1. User downloads `VJ_Youtube_Amaze_Setup.exe`
2. Runs installer → Standard Windows wizard
3. App auto-launches → Browser opens
4. First run → API key setup page (if not configured)
5. User enters API key → Saves to `%APPDATA%\VJ Youtube Amaze\.env`
6. Main app ready to use

## For Detailed Guide

See `INSTALLER_GUIDE.md` for complete documentation.

## What Gets Created

### After Step 1 (EXE Build):
- `dist\VJ_Youtube_Amaze.exe` - Standalone executable

### After Step 2 (Installer Build):
- `dist\VJ_Youtube_Amaze_Setup.exe` - Windows installer (~50-100MB)
- This is what you distribute to users

## What Users Will See

1. **Download:** `VJ_Youtube_Amaze_Setup.exe`
2. **Run Installer:** Standard Windows installer wizard
3. **Install Location:** `C:\Program Files\VJ Youtube Amaze\`
4. **Shortcuts Created:**
   - Desktop shortcut (optional)
   - Start Menu → VJ Youtube Amaze
5. **Auto-Launch:** Application starts automatically after installation
6. **First Run:** API key setup page appears
7. **Subsequent Runs:** Main application opens directly

## Features

✅ Desktop shortcut  
✅ Start Menu shortcut  
✅ App name: "VJ Youtube Amaze"  
✅ Auto-launch after installation  
✅ First-run API key setup  
✅ Clear, non-technical instructions  

## Testing

Before distributing:
1. Test on a clean Windows machine (or VM)
2. Verify installer works
3. Verify shortcuts are created
4. Verify first-run setup works
5. Verify API key saves correctly
6. Verify main app works after setup
