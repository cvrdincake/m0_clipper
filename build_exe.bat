@echo off
setlocal enabledelayedexpansion

echo M0 Clipper Build System for Windows
echo =====================================

REM Find tbb12.dll
echo Searching for tbb12.dll...
set "TBB_PATH="
for /R "%LOCALAPPDATA%\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages" %%f in (tbb12.dll) do (
    if exist "%%f" (
        set "TBB_PATH=%%~dpf"
        goto :found_tbb
    )
)

:found_tbb
if defined TBB_PATH (
    echo Found tbb12.dll in !TBB_PATH!
    set "PYINSTALLER_ARGS=--add-binary \"!TBB_PATH!tbb12.dll;.\" "
) else (
    echo WARNING: tbb12.dll not found. The build may fail.
    set "PYINSTALLER_ARGS="
)

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
python -m PyInstaller m0_clipper.spec --clean %PYINSTALLER_ARGS%

REM Check if build was successful
if errorlevel 1 (
    echo.
    echo ❌ Build failed! Check the output above for errors.
    goto :end
)

echo.
echo ✅ Build completed successfully!
echo 📁 Executable created: dist\M0_Clipper.exe

REM Create portable distribution
echo 📦 Creating portable distribution...
set "PORTABLE_DIR=dist\M0_Clipper_Portable"
if exist "%PORTABLE_DIR%" rmdir /s /q "%PORTABLE_DIR%"
mkdir "%PORTABLE_DIR%"

copy "dist\M0_Clipper.exe" "%PORTABLE_DIR%\"

echo # M0 Clipper - Portable Version > "%PORTABLE_DIR%\README.txt"
echo. >> "%PORTABLE_DIR%\README.txt"
echo ## Quick Start >> "%PORTABLE_DIR%\README.txt"
echo 1. Double-click M0_Clipper.exe to launch >> "%PORTABLE_DIR%\README.txt"
echo 2. Drag and drop your video file >> "%PORTABLE_DIR%\README.txt"
echo 3. Click "Generate Highlights" to start >> "%PORTABLE_DIR%\README.txt"
echo. >> "%PORTABLE_DIR%\README.txt"
echo ## Requirements >> "%PORTABLE_DIR%\README.txt"
echo - FFmpeg must be installed on your system >> "%PORTABLE_DIR%\README.txt"
echo - Windows 10/11 (64-bit) >> "%PORTABLE_DIR%\README.txt"

echo ✅ Portable distribution created: %PORTABLE_DIR%\
echo.
echo 💡 Tip: Test the executable on a clean system to ensure all dependencies are included

:end
pause