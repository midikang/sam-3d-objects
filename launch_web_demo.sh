#!/bin/bash
# Shell script to launch SAM 3D Objects Web Demo
# 
# This script activates the conda/mamba environment and launches the web interface.
# Usage: ./launch_web_demo.sh

set -e

echo "============================================================"
echo "SAM 3D Objects - Web Demo Launcher"
echo "============================================================"
echo ""

# Detect if mamba or conda is available
if command -v mamba &> /dev/null; then
    CONDA_CMD="mamba"
elif command -v conda &> /dev/null; then
    CONDA_CMD="conda"
else
    echo "ERROR: Neither conda nor mamba is found in PATH"
    echo "Please ensure Anaconda, Miniconda, or Mamba is installed and added to PATH"
    exit 1
fi

echo "Using: $CONDA_CMD"

# Initialize conda/mamba for bash
eval "$($CONDA_CMD shell.bash hook)"

# Activate the sam3d-objects environment
echo "Activating sam3d-objects environment..."
if ! $CONDA_CMD activate sam3d-objects; then
    echo "ERROR: Failed to activate sam3d-objects environment"
    echo "Please ensure the environment is created. Run:"
    echo "  $CONDA_CMD env create -f environments/default.yml"
    echo "  $CONDA_CMD activate sam3d-objects"
    exit 1
fi

echo "Environment activated successfully!"
echo ""

# Check if checkpoints exist
if [ ! -f "checkpoints/hf/pipeline.yaml" ]; then
    echo "WARNING: Checkpoints not found at checkpoints/hf/pipeline.yaml"
    echo "Please download checkpoints following the setup instructions."
    echo "See doc/setup.md for details."
    exit 1
fi

# Launch the web demo
echo "Launching web demo..."
echo "The web interface will open at http://localhost:7860"
echo ""
echo "Press Ctrl+C to stop the server"
echo "============================================================"
echo ""

python web_demo.py "$@"
