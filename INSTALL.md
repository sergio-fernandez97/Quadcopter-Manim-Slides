# Installation Guide - Fixing FFmpeg/av Package Error

## Problem
The `av` package (PyAV) requires FFmpeg libraries which are not found on your system.

## Solution

### Step 1: Install Homebrew (if not already installed)

Run this command in your terminal:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the prompts and enter your password when asked.

### Step 2: Install FFmpeg

After Homebrew is installed, run:
```bash
brew install ffmpeg
```

This will install all the required FFmpeg libraries (libavformat, libavcodec, etc.).

### Step 3: Install manim-slides

Now you can install manim-slides:
```bash
pipx install "manim-slides[manim]"
```

Or if you prefer using pip in a virtual environment:
```bash
pip install manim manim-slides
```

## Alternative: Install without full manim dependencies

If you want to avoid the FFmpeg dependency for now, you can install manim-slides without the extra dependencies:

```bash
pipx install manim-slides
pip install manim  # This might still require FFmpeg for video rendering
```

However, note that manim itself typically requires FFmpeg for video rendering, so you'll likely need to install FFmpeg anyway.

## Verify Installation

After installation, verify everything works:
```bash
manim-slides --version
manim --version
```




