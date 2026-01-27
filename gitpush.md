# Git Push Process - Complete Workflow

## Overview
This document outlines the complete process for pushing code and the installer to GitHub.

## Prerequisites
- All code changes are complete and tested
- Git repository is set up and connected
- Inno Setup is installed (for building installer)

## Complete Push Workflow

### Step 1: Build the EXE
```bash
.\build_exe.bat
```
**Verifies:**
- ✅ EXE created at `dist\VJ_Youtube_Amaze.exe`
- ✅ Static files copied to `dist\static\`

### Step 2: Build the Installer
```bash
powershell -ExecutionPolicy Bypass -File build_installer.ps1
```
**Or manually:**
```bash
"C:\Users\vijay\AppData\Local\Programs\Inno Setup 6\ISCC.exe" installer.iss
```

**Verifies:**
- ✅ Installer created at `dist\VJ_Youtube_Amaze_Setup.exe`
- ✅ Size is ~73 MB (below GitHub's 100MB limit)

### Step 3: Verify Files to Push
Check what will be committed:
```bash
git status
```

**Expected files:**
- ✅ All source code changes (`.py` files)
- ✅ `dist\VJ_Youtube_Amaze_Setup.exe` (installer)
- ✅ Build scripts (`build_exe.bat`, `build_installer.ps1`)
- ✅ Configuration files (`installer.iss`, `youtube_scraper.spec`)
- ✅ Documentation (`BUILD_INSTRUCTIONS.md`, `INSTALLER_GUIDE.md`, `gitpush.md`)
- ✅ `launcher.py`
- ✅ `static\setup.html`

**Should NOT commit:**
- ❌ `dist\VJ_Youtube_Amaze.exe` (standalone EXE - not needed, installer contains it)
- ❌ `build\` folder (temporary PyInstaller files)
- ❌ `.env` files (contains sensitive API keys)
- ❌ `__pycache__\` folders
- ❌ `.cursor\` folder

### Step 4: Add Files to Git
```bash
# Add all source files and documentation
git add *.py *.md *.bat *.ps1 *.iss *.spec
git add static/
git add models.py youtube_*.py

# Add the installer
git add dist/VJ_Youtube_Amaze_Setup.exe

# Add launcher
git add launcher.py

# Check what's staged
git status
```

### Step 5: Commit Changes
```bash
git commit -m "Add installer and build files

- Include VJ_Youtube_Amaze_Setup.exe installer
- Add build scripts and configuration
- Add complete documentation
- Updated .env handling to user data directory"
```

### Step 6: Push to GitHub
```bash
git push origin main
```

**If push fails due to large file:**
- GitHub allows files up to 100MB
- Installer is ~73MB, should work fine
- If needed, use Git LFS (see below)

### Step 7: Verify on GitHub
1. Go to: https://github.com/vijayacads/VJ_youtube_scrapper
2. Check `dist/VJ_Youtube_Amaze_Setup.exe` is visible
3. Verify file size matches local version

## Quick Push Script

For future pushes, you can use this sequence:

```bash
# 1. Build everything
.\build_exe.bat
powershell -File build_installer.ps1

# 2. Add and commit
git add .
git commit -m "Update: [describe your changes]"

# 3. Push
git push
```

## Important Notes

### What to Include in Git
✅ **DO commit:**
- Source code (`.py` files)
- Installer (`dist/VJ_Youtube_Amaze_Setup.exe`)
- Build scripts and configs
- Documentation
- Static files (HTML, CSS, images)

❌ **DON'T commit:**
- Standalone EXE (`dist/VJ_Youtube_Amaze.exe`) - installer contains it
- Build artifacts (`build/` folder)
- Environment files (`.env`)
- Cache folders (`__pycache__/`, `.cursor/`)
- User data

### File Size Considerations
- Installer: ~73 MB (within GitHub's 100MB limit)
- If it grows >100MB, use Git LFS:
  ```bash
  git lfs install
  git lfs track "dist/*.exe"
  git add .gitattributes
  ```

### Before Each Push Checklist
- [ ] Code changes are complete and tested
- [ ] EXE builds successfully
- [ ] Installer builds successfully
- [ ] Installer file exists and is correct size
- [ ] No sensitive data in files (API keys, passwords)
- [ ] Documentation is updated if needed
- [ ] Commit message is descriptive

## Troubleshooting

### "File too large" error
- Use Git LFS for files >100MB
- Or create GitHub Release instead

### "Permission denied" error
- Check `.git/index.lock` doesn't exist
- Close any Git GUI tools
- Try again

### Installer not building
- Verify Inno Setup is installed
- Check `dist\VJ_Youtube_Amaze.exe` exists
- Run build scripts manually

## Alternative: GitHub Releases

For cleaner distribution, create a Release:
1. Go to GitHub repo → "Releases" → "Create a new release"
2. Tag: `v1.0.0`
3. Upload `VJ_Youtube_Amaze_Setup.exe` as asset
4. Add release notes
5. Publish

Users download from release page instead of browsing repo.
