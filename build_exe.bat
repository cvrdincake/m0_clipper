@echo off
echo M0 Clipper Build System for Windows
echo =====================================

REM Check if PyInstaller is installed
python -c "import PyInstaller; print('PyInstaller found:', PyInstaller.__version__)" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build the executable
echo Building M0 Clipper executable...
python -m PyInstaller m0_clipper.spec --clean

REM Check if build was successful
if exist "dist\M0_Clipper.exe" (
    echo.
    echo ✅ Build completed successfully!
    echo 📁 Executable created: dist\M0_Clipper.exe
    
    REM Create portable distribution
    mkdir "dist\M0_Clipper_Portable" 2>nul
    copy "dist\M0_Clipper.exe" "dist\M0_Clipper_Portable\"
    
    echo # M0 Clipper - Portable Version > "dist\M0_Clipper_Portable\README.txt"
    echo. >> "dist\M0_Clipper_Portable\README.txt"
    echo ## Quick Start >> "dist\M0_Clipper_Portable\README.txt"
    echo 1. Double-click M0_Clipper.exe to launch >> "dist\M0_Clipper_Portable\README.txt"
    echo 2. Drag and drop your video file >> "dist\M0_Clipper_Portable\README.txt"
    echo 3. Click "Generate Highlights" to start >> "dist\M0_Clipper_Portable\README.txt"
    echo. >> "dist\M0_Clipper_Portable\README.txt"
    echo ## Requirements >> "dist\M0_Clipper_Portable\README.txt"
    echo - FFmpeg must be installed on your system >> "dist\M0_Clipper_Portable\README.txt"
    echo - Windows 10/11 (64-bit) >> "dist\M0_Clipper_Portable\README.txt"
    
    echo 📦 Portable distribution created: dist\M0_Clipper_Portable\
    echo.
    echo 💡 Tip: Test the executable on a clean system to ensure all dependencies are included
) else (
    echo.
    echo ❌ Build failed! Check the output above for errors.
    echo Make sure all dependencies are installed and try again.
)

pause