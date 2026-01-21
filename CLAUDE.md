# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Animated presentation for a dissertation on Quadcopter Control using Deep Reinforcement Learning. Uses Manim + manim-slides to create mathematical visualizations covering quadcopter dynamics, control theory, and reinforcement learning concepts.

## Commands

```bash
# Install dependencies (requires FFmpeg: brew install ffmpeg)
pip install -r requirements.txt

# Render all slides
python main.py render

# Launch interactive presentation
python main.py present

# Generate HTML output (Reveal.js)
python main.py html

# Render/preview a single slide
manim-slides render slides/00_inertial_frame.py InertialFrameSlide
manim-slides preview slides/00_inertial_frame.py InertialFrameSlide
```

## Architecture

```
slides/                  # Manim scene files (numbered for ordering)
├── 00_inertial_frame.py # Each file defines one *Slide class
├── 01_newton_euler.py
├── ...
slides.toml              # Presentation config and slide ordering
main.py                  # CLI entry point (render, present, html)
generate_html.py         # Converts slides to Reveal.js HTML
```

**Rendering pipeline**: Python scene → Manim renders animations → FFmpeg encodes MP4 → manim-slides manages presentation

## Slide Pattern

```python
from manim import *
from manim_slides import Slide  # or ThreeDSlide for 3D

class TopicSlide(Slide):
    def construct(self):
        # Use self.play() for animations
        # Use self.next_slide() for slide breaks
        # Use self.wait(seconds) for pauses
```

## Conventions

- **File naming**: `NN_topic_name.py` (two-digit prefix controls order)
- **Class naming**: `CamelCaseSlide` (must end with "Slide")
- **Indentation**: 4 spaces
- **Composition**: Use `VGroup` for related mobjects
- When adding slides: create file in `slides/`, add scene path to `slides.toml`
- Keep generated media (`media/`) out of commits; only commit source files under `slides/`
