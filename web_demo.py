#!/usr/bin/env python
# Copyright (c) Meta Platforms, Inc. and affiliates.
"""
Web demo launcher for SAM 3D Objects.

This script launches a Gradio web interface for interacting with SAM 3D Objects.
Users can upload images and masks to generate 3D reconstructions.
"""

import os
import sys
import argparse

# Add notebook directory to path for imports
sys.path.append("notebook")

try:
    import gradio as gr
    import numpy as np
    from PIL import Image
    import torch
    from inference import Inference
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("\nPlease ensure you have installed all dependencies:")
    print("  pip install -e .[inference]")
    sys.exit(1)


# Constants
MASK_THRESHOLD = 10  # Threshold for considering a pixel as part of the mask


def create_demo(inference_engine, checkpoint_tag="hf"):
    """Create and configure the Gradio interface."""
    
    def process_image(image, mask_image, seed):
        """Process an image and mask to generate 3D reconstruction."""
        if image is None:
            return None, "Please upload an image."
        
        if mask_image is None:
            return None, "Please upload a mask image."
        
        try:
            # Convert inputs to numpy arrays
            if isinstance(image, Image.Image):
                image = np.array(image)
            if isinstance(mask_image, Image.Image):
                mask_image = np.array(mask_image)
            
            # Extract mask from image (assuming mask is grayscale or has alpha channel)
            if mask_image.ndim == 3:
                if mask_image.shape[2] == 4:  # RGBA
                    mask = mask_image[:, :, 3] > 0
                else:  # RGB - use any non-black pixel
                    mask = np.any(mask_image > MASK_THRESHOLD, axis=2)
            else:  # Grayscale
                mask = mask_image > 0
            
            # Run inference
            output = inference_engine(image, mask, seed=seed if seed >= 0 else None)
            
            # Save the Gaussian splat
            output_path = "outputs/latest_reconstruction.ply"
            os.makedirs("outputs", exist_ok=True)
            output["gs"].save_ply(output_path)
            
            return output_path, "✓ 3D reconstruction complete!"
        
        except Exception as e:
            import traceback
            error_msg = f"Error during processing:\n{str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)
            return None, error_msg
    
    # Create the Gradio interface
    with gr.Blocks(title="SAM 3D Objects - Web Demo") as demo:
        gr.Markdown("""
        # SAM 3D Objects - 3D Reconstruction from Images
        
        Upload an image and a corresponding mask to generate a 3D Gaussian splat reconstruction.
        
        **Instructions:**
        1. Upload a source image (RGB or RGBA)
        2. Upload a mask image (white regions indicate the object to reconstruct)
        3. Optionally set a random seed for reproducibility
        4. Click "Generate 3D Model" to process
        5. View and download the resulting 3D model
        
        **Note:** Processing may take several minutes depending on your GPU.
        """)
        
        with gr.Row():
            with gr.Column():
                image_input = gr.Image(
                    label="Input Image",
                    type="pil",
                    height=400
                )
                mask_input = gr.Image(
                    label="Mask Image (white = object region)",
                    type="pil",
                    height=400
                )
                
                seed_input = gr.Number(
                    label="Random Seed (use -1 for random)",
                    value=42,
                    precision=0
                )
                
                generate_btn = gr.Button("Generate 3D Model", variant="primary")
            
            with gr.Column():
                model_output = gr.Model3D(
                    label="3D Reconstruction (Gaussian Splat)",
                    height=500
                )
                status_output = gr.Textbox(
                    label="Status",
                    lines=3,
                    max_lines=10
                )
        
        # Example section
        gr.Markdown("### Example")
        gr.Markdown("""
        Try the demo with the included sample image and mask from the kidsroom scene.
        The example files are located in `notebook/images/shutterstock_stylish_kidsroom_1640806567/`.
        """)
        
        # Connect the button to the processing function
        generate_btn.click(
            fn=process_image,
            inputs=[image_input, mask_input, seed_input],
            outputs=[model_output, status_output]
        )
    
    return demo


def main():
    """Main entry point for the web demo."""
    parser = argparse.ArgumentParser(
        description="Launch SAM 3D Objects web demo"
    )
    parser.add_argument(
        "--checkpoint-tag",
        type=str,
        default="hf",
        help="Checkpoint tag to use (default: hf)"
    )
    parser.add_argument(
        "--no-compile",
        action="store_true",
        help="Disable model compilation (faster startup, slower inference)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=7860,
        help="Port to run the web server on (default: 7860)"
    )
    parser.add_argument(
        "--share",
        action="store_true",
        help="Create a public share link (using Gradio share feature)"
    )
    parser.add_argument(
        "--server-name",
        type=str,
        default="127.0.0.1",
        help="Server name/IP to bind to (default: 127.0.0.1). Use 0.0.0.0 to allow external connections."
    )
    
    args = parser.parse_args()
    
    # Check if checkpoint exists
    checkpoint_path = f"checkpoints/{args.checkpoint_tag}/pipeline.yaml"
    if not os.path.exists(checkpoint_path):
        print(f"Error: Checkpoint not found at {checkpoint_path}")
        print("\nPlease download checkpoints following the setup instructions:")
        print("  See doc/setup.md or doc/setup_windows.md")
        sys.exit(1)
    
    print("=" * 60)
    print("SAM 3D Objects - Web Demo")
    print("=" * 60)
    print(f"Loading model from: {checkpoint_path}")
    print(f"Compile mode: {'disabled' if args.no_compile else 'enabled'}")
    print()
    
    # Check CUDA availability
    if not torch.cuda.is_available():
        print("WARNING: CUDA is not available. This will be very slow!")
        print("Please ensure you have:")
        print("  1. A NVIDIA GPU installed")
        print("  2. CUDA Toolkit installed")
        print("  3. PyTorch with CUDA support installed")
        print()
    else:
        print(f"CUDA available: {torch.cuda.get_device_name(0)}")
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        print()
    
    try:
        # Load the inference model
        print("Loading SAM 3D Objects model (this may take a minute)...")
        inference = Inference(checkpoint_path, compile=not args.no_compile)
        print("✓ Model loaded successfully!")
        print()
        
        # Create and launch the demo
        demo = create_demo(inference, args.checkpoint_tag)
        
        print(f"Starting web server on {args.server_name}:{args.port}")
        print(f"Share link: {'enabled' if args.share else 'disabled'}")
        print()
        print("=" * 60)
        print()
        
        demo.launch(
            server_name=args.server_name,
            server_port=args.port,
            share=args.share,
            show_error=True
        )
        
    except Exception as e:
        import traceback
        print(f"\nError launching web demo: {e}")
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
