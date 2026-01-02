# Quadcopter-Manim-Slides - Dissertation Presentation

A manim-slides presentation for the dissertation on Quadcopter Control using Deep Reinforcement Learning.

## Project Structure

```
.
├── slides/              # Slide scenes organized by presentation sections
│   ├── __init__.py
│   ├── 01_title.py      # Title slide
│   ├── 02_introduction.py
│   ├── 03_problem.py
│   ├── 04_methodology.py
│   ├── 05_results.py
│   └── 06_conclusion.py
├── slides.toml          # Presentation configuration
├── requirements.txt     # Python dependencies
└── README.md
```

## Setup

### Prerequisites

**Important:** manim-slides requires FFmpeg libraries. If you encounter errors about missing `libavformat`, `libavcodec`, etc., see [INSTALL.md](INSTALL.md) for detailed installation instructions.

**Quick fix:**
1. Install Homebrew (if not installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Install FFmpeg:
   ```bash
   brew install ffmpeg
   ```

3. Then install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or using pipx:
   ```bash
   pipx install "manim-slides[manim]"
   ```

### Verify Installation

```bash
manim-slides --version
```

## Usage

### Render all slides
```bash
manim-slides render slides.toml
```

### Present the slides
```bash
manim-slides present slides.toml
```

### Render a specific slide
```bash
manim-slides render slides/01_title.py TitleSlide
```

### Preview a slide
```bash
manim-slides preview slides/01_title.py TitleSlide
```

## Slide Organization

The slides are organized in a logical flow:

1. **Title Slide** (`01_title.py`) - Introduction with title and author
2. **Introduction** (`02_introduction.py`) - Background and overview
3. **Problem Statement** (`03_problem.py`) - Problem definition and challenges
4. **Methodology** (`04_methodology.py`) - Approach and methods used
5. **Results** (`05_results.py`) - Findings and evaluation
6. **Conclusion** (`06_conclusion.py`) - Summary and future work

## Customization

- Edit individual slide files in the `slides/` directory
- Modify `slides.toml` to reorder slides or change settings
- Add new slides by creating new Python files and adding them to `slides.toml`

## Tips

- Use `self.next_slide()` to create slide breaks within a scene
- Use `self.wait()` for pauses
- Add animations using Manim's animation functions (Write, FadeIn, etc.)
- For complex visualizations, consider creating separate utility modules

## Keyboard Controls (during presentation)

- **Space/Right Arrow**: Next slide
- **Left Arrow**: Previous slide
- **Q**: Quit presentation
- **R**: Restart presentation

