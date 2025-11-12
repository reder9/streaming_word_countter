@echo off@echo off

echo 🎙️ Building Vosk Jabroni Counter for Windows...echo ========================================

echo ⚡ High-accuracy offline speech recognitionecho    JABRONI COUNTER - Windows Builder

echo.echo ========================================

echo.

REM Check if Python is installedecho This script will create a Windows executable

python --version >nul 2>&1echo.

if errorlevel 1 (

    echo ❌ ERROR: Python is not installed or not in PATHREM Check if Python is installed

    echo Please install Python from https://python.orgpython --version >nul 2>&1

    pauseif errorlevel 1 (

    exit /b 1    echo ERROR: Python is not installed or not in PATH

)    echo Please install Python from https://python.org

    pause

REM Check if virtual environment exists    exit /b 1

if not exist "jabroni_env" ()

    echo ❌ Virtual environment not found!

    echo Please run: python -m venv jabroni_envecho Installing dependencies...

    echo Then: jabroni_env\Scripts\activatepip install -r requirements-windows.txt

    echo Then: pip install -r requirements.txt

    pauseecho.

    exit /b 1echo Building Windows executable...

)pyinstaller jabroni_counter.spec



echo 📦 Activating virtual environment...echo.

call jabroni_env\Scripts\activate.batecho ========================================

echo Build complete!

echo 🔧 Installing PyInstaller...echo.

pip install pyinstallerecho Your executable is in: dist\JabroniCounter.exe

echo.

echo 🔨 Building executable...echo To run on any Windows machine:

REM Build executable with Vosk counterecho 1. Copy the 'dist' folder to target machine

pyinstaller --onefile ^echo 2. Run JabroniCounter.exe

    --add-data "jabroni_counter.html;." ^echo 3. The HTML file will be created automatically

    --name=VoskJabroniCounter ^echo 4. Add the HTML file to OBS as Browser Source

    vosk_jabroni_counter.pyecho ========================================

pause
REM Create build output directory
if not exist "build_output" mkdir build_output

REM Copy files to build output
move dist\VoskJabroniCounter.exe build_output\
copy jabroni_counter.html build_output\
copy requirements.txt build_output\

REM Create Windows README
echo # Vosk Jabroni Counter for Windows > build_output\README.txt
echo. >> build_output\README.txt
echo 1. Run VoskJabroniCounter.exe to start >> build_output\README.txt
echo 2. Open jabroni_counter.html in OBS as Browser Source >> build_output\README.txt
echo 3. Set OBS Browser Source to Local File >> build_output\README.txt
echo 4. Width: 800, Height: 400 >> build_output\README.txt
echo. >> build_output\README.txt
echo High accuracy offline speech recognition! >> build_output\README.txt

REM Cleanup
rmdir /s /q build
rmdir /s /q dist

echo.
echo ✅ Build complete! Check build_output\ directory
echo 📁 Files created:
echo    - VoskJabroniCounter.exe (main executable)
echo    - jabroni_counter.html (OBS display)
echo    - requirements.txt (for reference)
echo    - README.txt (instructions)
echo.
echo 🚀 Ready for Windows deployment!
pause