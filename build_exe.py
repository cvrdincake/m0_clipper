#!/usr/bin/env python3
"""
Build script for M0 Clipper executable
Creates a standalone .exe file using PyInstaller
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def check_dependencies():
    """Check and install required build dependencies."""
    print("🔍 Checking build dependencies...")
    
    # Check PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
        print("✅ PyInstaller installed")
    
    # Check for Pillow (for icon conversion)
    try:
        import PIL
        print(f"✅ Pillow found (version: {PIL.__version__})")
    except ImportError:
        print("⚠️  Pillow not found (optional for icon conversion)")
        print("   Installing Pillow for better icon support...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'Pillow'], check=True)
            print("✅ Pillow installed")
        except subprocess.CalledProcessError:
            print("⚠️  Could not install Pillow - building without custom icon")

def build_executable():
    """Build the M0 Clipper executable."""
    print("🔨 Building M0 Clipper executable...")
    
    # Clean previous builds
    print("🧹 Cleaning previous builds...")
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")
    
    # Build with PyInstaller
    print("📦 Running PyInstaller...")
    try:
        result = subprocess.run([
            sys.executable, '-m', 'PyInstaller', 
            'm0_clipper.spec',
            '--clean',
            '--noconfirm'
        ], check=True, capture_output=False, text=True)
        
        print("✅ Build completed successfully!")
        
        # Check if executable was created
        exe_path = Path('dist/M0_Clipper.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📁 Executable created: {exe_path}")
            print(f"📏 Size: {size_mb:.1f} MB")
            
            # Create a distribution folder with readme
            dist_folder = Path('dist/M0_Clipper_Portable')
            dist_folder.mkdir(exist_ok=True)
            
            # Copy executable
            shutil.copy(exe_path, dist_folder / 'M0_Clipper.exe')
            
            # Create a simple readme for the portable version
            readme_content = """# M0 Clipper - Portable Version

## Quick Start
1. Double-click M0_Clipper.exe to launch the application
2. Drag and drop your video file onto the window
3. Adjust settings if needed (decibel threshold, clip length)
4. Click "Generate Highlights" to start processing

## Requirements
- FFmpeg must be installed on your system and available in PATH
- Windows 10/11 (64-bit)
- Sufficient disk space for output videos

## Features
- Professional modular GUI with glassmorphism design
- Streaming and legacy processing modes
- Reference analysis for optimal threshold detection
- Comprehensive error handling and user feedback
- Batch processing capabilities

## Troubleshooting
- If the app doesn't start, try running from command prompt to see error messages
- Make sure FFmpeg is in your system PATH (test with: ffmpeg -version)
- For best performance, process videos from local storage (not network drives)
- Check the logs folder for detailed error information

## New in This Version
- Complete infrastructure transformation to modular architecture
- Enhanced error handling and validation
- Professional state management system
- Improved user interface with better feedback
- Comprehensive logging system

## Support
For issues and documentation, visit: https://github.com/cvrdincake/m0_clipper
"""
            
            with open(dist_folder / 'README.txt', 'w') as f:
                f.write(readme_content)
            
            print(f"📦 Portable distribution created: {dist_folder}")
            return True
        else:
            print("❌ Executable not found after build")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed!")
        print(f"Error code: {e.returncode}")
        print("\n💡 Common solutions:")
        print("   • Install Pillow: pip install Pillow")
        print("   • Convert icon to ICO format or remove icon line from spec")
        print("   • Check that all dependencies are installed")
        print("   • Try building with console=True for debugging")
        return False

def main():
    """Main build function."""
    print("M0 Clipper Build System for Windows")
    print("=" * 40)
    
    # Check dependencies first
    check_dependencies()
    
    # Check if spec file exists
    if not os.path.exists('m0_clipper.spec'):
        print("❌ m0_clipper.spec not found!")
        print("   Make sure you're running this from the project root directory")
        return 1
    
    # Build the executable
    success = build_executable()
    
    if success:
        print("\n🎉 Build completed successfully!")
        print("💡 Tip: Test the executable on a clean system to ensure all dependencies are included")
        return 0
    else:
        print("\n💥 Build failed! Check the output above for errors.")
        print("Make sure all dependencies are installed and try again.")
        return 1

if __name__ == '__main__':
    sys.exit(main())