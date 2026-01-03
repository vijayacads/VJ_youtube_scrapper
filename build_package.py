#!/usr/bin/env python3
"""
Package builder for YouTube Scraper
Creates a distributable zip file with all necessary files.
"""
import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def build_package():
    """Build a distributable package."""
    print("=" * 60)
    print("YouTube Scraper - Package Builder")
    print("=" * 60)
    print()
    
    # Package name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"youtube-scraper-v1.0-{timestamp}"
    package_dir = Path("dist") / package_name
    
    # Create package directory
    print(f"[1/5] Creating package directory: {package_dir}")
    package_dir.mkdir(parents=True, exist_ok=True)
    
    # Files to include
    files_to_include = [
        "main.py",
        "models.py",
        "youtube_id.py",
        "youtube_metadata.py",
        "youtube_transcript.py",
        "youtube_channel.py",
        "requirements.txt",
        "install.bat",
        "install.sh",
        "run.bat",
        "run.sh",
        "README_PACKAGE.md",
    ]
    
    # Directories to include
    dirs_to_include = [
        "static",
    ]
    
    # Copy files
    print("[2/5] Copying files...")
    for file in files_to_include:
        if os.path.exists(file):
            shutil.copy2(file, package_dir / file)
            print(f"  [OK] {file}")
        else:
            print(f"  [WARN] {file} not found, skipping")
    
    # Copy directories
    print("[3/5] Copying directories...")
    for dir_name in dirs_to_include:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, package_dir / dir_name, dirs_exist_ok=True)
            print(f"  [OK] {dir_name}/")
        else:
            print(f"  [WARN] {dir_name}/ not found, skipping")
    
    # Create .gitignore for package (exclude .env, __pycache__, etc.)
    print("[4/5] Creating .gitignore...")
    gitignore_content = """# Environment variables
.env
.env.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
"""
    with open(package_dir / ".gitignore", "w") as f:
        f.write(gitignore_content)
    print("  [OK] .gitignore")
    
    # Create zip file
    print("[5/5] Creating zip archive...")
    zip_path = Path("dist") / f"{package_name}.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            # Skip __pycache__ and .pyc files
            dirs[:] = [d for d in dirs if d != '__pycache__']
            files = [f for f in files if not f.endswith('.pyc')]
            
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arcname)
    
    print(f"  [OK] {zip_path}")
    
    # Get file size
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    
    print()
    print("=" * 60)
    print("Package Built Successfully!")
    print("=" * 60)
    print(f"Package: {zip_path}")
    print(f"Size: {size_mb:.2f} MB")
    print()
    print("The package is ready for distribution!")
    print("Users can extract the zip and run install.bat (Windows) or install.sh (Mac/Linux)")
    print()
    
    return str(zip_path)

if __name__ == "__main__":
    try:
        zip_path = build_package()
        print(f"\n[SUCCESS] Package created: {zip_path}")
    except Exception as e:
        print(f"\n[ERROR] Error building package: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

