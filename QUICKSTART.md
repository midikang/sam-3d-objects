# Quick Start Guide - Web Demo

This is a quick reference for running the SAM 3D Objects web interface.

## Prerequisites

✓ NVIDIA GPU (32+ GB VRAM)  
✓ CUDA Toolkit 12.1  
✓ Conda environment set up  
✓ Checkpoints downloaded  

## Launch Web Interface

### Windows

```cmd
launch_web_demo.bat
```

or

```cmd
conda activate sam3d-objects
python web_demo.py
```

### Linux / Mac

```bash
./launch_web_demo.sh
```

or

```bash
conda activate sam3d-objects
python web_demo.py
```

## Access

Open your browser and go to:
```
http://localhost:7860
```

## Usage

1. **Upload Image** - RGB or RGBA image
2. **Upload Mask** - White pixels indicate the object to reconstruct
3. **Set Seed** (optional) - For reproducible results
4. **Click "Generate 3D Model"** - Wait for processing
5. **View/Download** - Interact with the 3D model

## Command Line Options

```bash
# Change port
python web_demo.py --port 8080

# Enable public sharing
python web_demo.py --share

# Disable compilation (faster startup)
python web_demo.py --no-compile

# Allow external connections
python web_demo.py --server-name 0.0.0.0
```

## Troubleshooting

**Web interface won't start**
- Check CUDA is available: `nvidia-smi`
- Verify checkpoints exist: `checkpoints/hf/pipeline.yaml`
- Check all dependencies installed: `pip list | grep gradio`

**Out of memory error**
- Close other GPU applications
- Check available memory: `nvidia-smi`

**Connection refused**
- Try a different port: `--port 8080`
- Check firewall settings

## Documentation

- Full Windows guide: [doc/setup_windows.md](doc/setup_windows.md)
- Full Linux guide: [doc/setup.md](doc/setup.md)
- Chinese guide: [README_CN.md](README_CN.md)
- Main README: [README.md](README.md)

## Example Images

Try the included example:
- Image: `notebook/images/shutterstock_stylish_kidsroom_1640806567/image.png`
- Masks: `notebook/images/shutterstock_stylish_kidsroom_1640806567/*.png`

## Getting Help

If you encounter issues:
1. Check the documentation above
2. Verify GPU and CUDA are working
3. Ensure all dependencies are installed
4. Check the GitHub issues for similar problems
