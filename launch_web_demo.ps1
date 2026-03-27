# PowerShell script to launch SAM 3D Objects Web Demo
# 
# This script activates the conda environment and launches the web interface.
# Usage: Right-click and select "Run with PowerShell" or run from PowerShell

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "SAM 3D Objects - Web Demo Launcher (Windows)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if conda is available
$condaCommand = Get-Command conda -ErrorAction SilentlyContinue
if (-not $condaCommand) {
    Write-Host "ERROR: conda is not found in PATH" -ForegroundColor Red
    Write-Host "Please ensure Anaconda or Miniconda is installed and added to PATH"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Initialize conda for PowerShell if needed
$condaPath = Split-Path -Parent (Split-Path -Parent $condaCommand.Source)
$condaHookScript = Join-Path $condaPath "shell\condabin\conda-hook.ps1"
if (Test-Path $condaHookScript) {
    . $condaHookScript
}

# Activate the sam3d-objects environment
Write-Host "Activating sam3d-objects environment..." -ForegroundColor Yellow
try {
    conda activate sam3d-objects
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to activate environment"
    }
} catch {
    Write-Host "ERROR: Failed to activate sam3d-objects environment" -ForegroundColor Red
    Write-Host "Please ensure the environment is created. Run:" -ForegroundColor Yellow
    Write-Host "  conda create -n sam3d-objects python=3.11" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Environment activated successfully!" -ForegroundColor Green
Write-Host ""

# Check if checkpoints exist
if (-not (Test-Path "checkpoints\hf\pipeline.yaml")) {
    Write-Host "WARNING: Checkpoints not found at checkpoints\hf\pipeline.yaml" -ForegroundColor Yellow
    Write-Host "Please download checkpoints following the setup instructions."
    Write-Host "See doc\setup_windows.md for details."
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Launch the web demo
Write-Host "Launching web demo..." -ForegroundColor Green
Write-Host "The web interface will open at http://localhost:7860" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

python web_demo.py

Read-Host "Press Enter to exit"
