@echo off
REM Windows batch file to launch SAM 3D Objects Web Demo
REM 
REM This script activates the conda environment and launches the web interface.
REM Usage: Double-click this file or run from Command Prompt

echo ============================================================
echo SAM 3D Objects - Web Demo Launcher (Windows)
echo ============================================================
echo.

REM Check if conda is available
where conda >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: conda is not found in PATH
    echo Please ensure Anaconda or Miniconda is installed and added to PATH
    echo.
    pause
    exit /b 1
)

REM Activate the sam3d-objects environment
echo Activating sam3d-objects environment...
call conda activate sam3d-objects
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to activate sam3d-objects environment
    echo Please ensure the environment is created. Run:
    echo   conda create -n sam3d-objects python=3.11
    echo.
    pause
    exit /b 1
)

echo Environment activated successfully!
echo.

REM Check if checkpoints exist
if not exist "checkpoints\hf\pipeline.yaml" (
    echo WARNING: Checkpoints not found at checkpoints\hf\pipeline.yaml
    echo Please download checkpoints following the setup instructions.
    echo See doc\setup_windows.md for details.
    echo.
    pause
    exit /b 1
)

REM Launch the web demo
echo Launching web demo...
echo The web interface will open at http://localhost:7860
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python web_demo.py

pause
