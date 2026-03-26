# SAM 3D Objects - Interactive Course

An interactive, single-page HTML course that teaches how the SAM 3D Objects codebase works.

## What is this?

This course transforms the SAM 3D Objects codebase into a beautiful, interactive learning experience. It's designed for "vibe coders" — people who build software using AI coding tools but want to understand what's happening under the hood.

## How to Use

1. **Open the course**: Simply open `sam3d-course.html` in any modern web browser
2. **Navigate**: Scroll through modules or use arrow keys (↑↓) to jump between sections
3. **Interact**: Hover over technical terms for definitions, try the quizzes, and explore animations
4. **Learn**: Follow the journey from "photo to 3D model" through all 7 modules

## What You'll Learn

### Module 1: From Photo to 3D
- What SAM 3D Objects does
- The complete user journey from image to 3D model
- Meet the actors: generators, decoders, and depth models

### Module 2: The Two-Stage Architecture
- Why SAM 3D uses two stages (WHERE vs WHAT)
- Sparse structure generation (Stage 1)
- Shape-latent generation (Stage 2)
- Coarse-to-fine generation patterns

### Module 3: Sparse Representations
- Memory-efficient 3D data structures
- SparseTensor abstraction
- Why sparse operations are fast
- When to use sparse vs dense

### Module 4: Depth Maps and Scene Awareness
- MoGe depth estimation
- Point maps guide the generation
- Pose estimation from geometry
- Layout optimization with ICP

### Module 5: Diffusion Transformers
- What diffusion models are
- Classifier-free guidance (CFG)
- Multi-step generation process
- Why Transformers for 3D

### Module 6: From Latents to 3D Outputs
- Decoding to Gaussian splats
- Decoding to triangle meshes
- Post-processing (simplification, texture baking)
- Export formats (PLY, GLB)

### Module 7: The Big Picture
- Full pipeline architecture
- Debugging guide: when to tweak what
- Real-world scenarios and tradeoffs
- Mastery quiz

## Features

- **🎨 Beautiful Design**: Warm palette, distinctive typography, generous whitespace
- **📚 Glossary Tooltips**: Every technical term explained on hover
- **🎯 Interactive Quizzes**: Test your understanding with scenario-based questions
- **💬 Group Chat Animations**: See components communicate in iMessage style
- **🔄 Data Flow Visualizations**: Animated pipelines showing how data transforms
- **📝 Code ↔ English Translations**: Real code with plain-English explanations side-by-side
- **⌨️ Keyboard Navigation**: Use arrow keys to jump between modules
- **📊 Progress Tracking**: Visual progress bar shows where you are in the course

## Who Is This For?

This course is for:
- **AI-assisted developers** who want to understand the code they're building
- **Researchers** exploring 3D generation techniques
- **Students** learning computer vision and 3D reconstruction
- **Engineers** debugging or extending SAM 3D Objects
- **Anyone curious** about how AI generates 3D models from photos

## No Setup Required

The course is completely self-contained:
- ✅ Single HTML file
- ✅ No dependencies (except Google Fonts CDN)
- ✅ Works offline (after fonts load)
- ✅ No JavaScript frameworks
- ✅ Mobile responsive

## Technical Details

- **Size**: ~119KB (uncompressed)
- **Browser Support**: Modern browsers (Chrome, Firefox, Safari, Edge)
- **Accessibility**: Keyboard navigation, ARIA labels, readable fonts
- **Performance**: GPU-accelerated animations, passive scroll listeners

## Course Philosophy

This course inverts traditional CS education:

**Old way**: Memorize concepts → Eventually build something → See the point (most quit before step 3)

**This way**: Build something → Experience it working → Understand how it works

Every module answers "why should I care?" before diving into implementation. The course teaches you to:
- **Steer AI better**: Make informed architectural decisions
- **Debug confidently**: Know where to look when things break
- **Communicate precisely**: Use the right technical vocabulary
- **Build production software**: Understand quality vs speed tradeoffs

## Credits

Created using the [codebase-to-course](https://github.com/zarazhangrui/codebase-to-course) skill for Claude Code.

Based on the [SAM 3D Objects](https://github.com/facebookresearch/sam-3d-objects) codebase by Meta AI Research.

## License

The course content is provided for educational purposes. The SAM 3D Objects code and models are licensed under the [SAM License](../LICENSE).
