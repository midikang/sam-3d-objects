# Windows 10 Setup Guide

This guide explains how to set up and run SAM 3D Objects on Windows 10.

## Prerequisites

* Windows 10 (64-bit)
* A NVIDIA GPU with at least 32 GB of VRAM
* NVIDIA CUDA Toolkit 12.1 (or compatible version)
* Anaconda or Miniconda installed
* Git for Windows

## Important Notes

⚠️ **Windows Support Limitations:**
- Some Linux-specific dependencies may require alternative installations
- The CUDA toolkit must be installed separately on Windows
- PyTorch3D and some other dependencies may require compilation from source or conda-forge packages

## Setup Steps

### 1. Install NVIDIA CUDA Toolkit

Download and install CUDA Toolkit 12.1 from the [NVIDIA website](https://developer.nvidia.com/cuda-downloads).

After installation, verify CUDA is installed:
```cmd
nvcc --version
```

### 2. Create Python Environment

Open Anaconda Prompt or Command Prompt and run:

```cmd
# Create a new conda environment with Python 3.11
conda create -n sam3d-objects python=3.11 -y
conda activate sam3d-objects
```

### 3. Install PyTorch with CUDA Support

```cmd
# Install PyTorch with CUDA 12.1 support
pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121
```

### 4. Install Core Dependencies

```cmd
# Set environment variables for pip installation
set PIP_EXTRA_INDEX_URL=https://pypi.ngc.nvidia.com https://download.pytorch.org/whl/cu121

# Install sam3d-objects in development mode
pip install -e .

# Install PyTorch3D (this may take some time)
# Note: PyTorch3D installation on Windows can be challenging
# Try conda first, then pip as fallback
conda install -c conda-forge pytorch3d -y
# OR if conda fails:
# pip install pytorch3d

# Install inference dependencies
set PIP_FIND_LINKS=https://nvidia-kaolin.s3.us-east-2.amazonaws.com/torch-2.5.1_cu121.html
pip install -e .[inference]
```

### 5. Apply Hydra Patch

The Hydra library requires a small patch. The `patching\hydra` file is a Python script that applies this patch. Run it with:

```cmd
python patching\hydra
```

Note: This script will download and apply a patch to your installed Hydra package.

### 6. Download Checkpoints

Before using SAM 3D Objects, you need to request access to the checkpoints on the [SAM 3D Objects Hugging Face repo](https://huggingface.co/facebook/sam-3d-objects).

Once approved, authenticate with Hugging Face:

```cmd
pip install "huggingface-hub[cli]<1.0"
huggingface-cli login
```

Then download the checkpoints:

```cmd
set TAG=hf
huggingface-cli download --repo-type model --local-dir checkpoints\%TAG%-download --max-workers 1 facebook/sam-3d-objects
move checkpoints\%TAG%-download\checkpoints checkpoints\%TAG%
rmdir /s /q checkpoints\%TAG%-download
```

## Running the Web Interface

After setup is complete, you can launch the web interface in several ways:

### Option 1: Use the Batch Launcher (Easiest)

Simply double-click `launch_web_demo.bat` in the project root directory, or run from Command Prompt:

```cmd
launch_web_demo.bat
```

### Option 2: Use PowerShell Launcher

Right-click `launch_web_demo.ps1` and select "Run with PowerShell", or from PowerShell:

```powershell
.\launch_web_demo.ps1
```

### Option 3: Manual Launch

```cmd
# Activate the environment
conda activate sam3d-objects

# Run the web launcher
python web_demo.py
```

The web interface will be accessible at `http://localhost:7860` (or a different port if 7860 is occupied).

**Available Options:**
- `--port PORT`: Specify a different port (default: 7860)
- `--share`: Create a public Gradio share link
- `--no-compile`: Disable model compilation for faster startup (but slower inference)
- `--server-name HOST`: Set the server host (use `0.0.0.0` to allow connections from other devices)

Example:
```cmd
python web_demo.py --port 8080 --share
```

## Troubleshooting

### Common Issues

**Issue: PyTorch3D installation fails**
- Solution: Try installing from conda-forge: `conda install -c conda-forge pytorch3d`
- Alternative: Build from source following [PyTorch3D installation guide](https://github.com/facebookresearch/pytorch3d/blob/main/INSTALL.md)

**Issue: CUDA out of memory**
- Solution: Ensure your GPU has at least 32 GB VRAM and no other processes are using the GPU
- Check GPU memory: `nvidia-smi`

**Issue: Import errors for compiled dependencies**
- Solution: Ensure Visual Studio Build Tools are installed (required for compiling some Python packages)
- Download from: https://visualstudio.microsoft.com/downloads/ (Build Tools for Visual Studio)

**Issue: kaolin or gsplat installation fails**
- Solution: These packages may need to be compiled for Windows. Check their respective GitHub repositories for Windows installation instructions.

## Running Without Web Interface

If you encounter issues with the web interface, you can still use the command-line demo:

```cmd
python demo.py
```

This will process a sample image and save the result to `splat.ply`.

## Differences from Linux Setup

1. **Path separators**: Windows uses backslashes (`\`) instead of forward slashes (`/`)
2. **Environment variables**: Set with `set` instead of `export`
3. **Shell scripts**: Bash scripts don't work directly; use PowerShell or Python equivalents
4. **Binary packages**: Some packages may need different installation methods on Windows

## Performance Notes

- Inference time may vary depending on your GPU
- First run will be slower due to model compilation
- Subsequent runs should be faster
