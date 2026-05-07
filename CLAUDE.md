# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Animated presentation for a dissertation on Quadcopter Control using Deep Reinforcement Learning. Uses Manim + manim-slides to create mathematical visualizations covering quadcopter dynamics, control theory, and reinforcement learning concepts.

## Commands

```bash
# Install dependencies (requires FFmpeg: brew install ffmpeg)
uv sync

# Render all slides
uv run python main.py render

# Launch interactive presentation
uv run python main.py present

# Generate HTML output (Reveal.js)
uv run python main.py html

# Render/preview a single slide
uv run manim-slides render slides/00_inertial_frame.py InertialFrameSlide
uv run manim-slides present InertialFrameSlide

# Convert a scene to HTML
uv run manim-slides convert SCENE scene.html -ccontrols=true
```

## Presentation Controls

- **Space/Right Arrow**: Next slide
- **Left Arrow**: Previous slide
- **Q**: Quit presentation
- **R**: Restart presentation

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

- **Manim Slides Development Rule**: Whenever the agent generates, edits, or debugs code related to **Manim** or **manim-slides**, it MUST use the `context7` MCP server as the primary reference source.
the agent MUST:

1. Query the `context7` MCP server before writing code.
2. Retrieve relevant API usage, examples, or documentation.
3. Ground generated code in the retrieved context.
4. Prefer Context7 references over internal memory when conflicts exist.

- **File naming**: `NN_topic_name.py` (two-digit prefix controls order)
- **Class naming**: `CamelCaseSlide` (must end with "Slide")
- **Indentation**: 4 spaces
- **Composition**: Use `VGroup` for related mobjects
- **Key concepts**: Use `BulletedList` from Manim to present key concepts or bullet points on slides
- **Slide style**: Aim for slides that resemble Beamer presentations—more static, with animations used sparingly for emphasis rather than constant motion. Prioritize clarity and readability over complex animations.
- **Transitions**: Every scene must use `self.next_slide()` to create transition points between logical sections. These pauses allow the speaker to explain each element before proceeding. Place `next_slide()` after revealing new content (equations, diagrams, bullet points) that requires explanation.
- **Boxed content**: Wrap definitions, theorems, and bulleted lists (not simple labels) inside a rounded gray rectangle with high transparency. Example:
  ```python
  box = RoundedRectangle(corner_radius=0.2, width=10, height=2, color=GRAY, fill_opacity=0.15, stroke_width=1)
  content = BulletedList("Item 1", "Item 2", font_size=24)
  VGroup(box, content).arrange(ORIGIN)
  ```
- **Concise text**: Minimize words in theorems and definitions. You may rephrase user-provided content for brevity while preserving meaning.
- When adding slides: create file in `slides/`, add scene path to `slides.toml`
- Keep generated media (`media/`) out of commits; only commit source files under `slides/`

## `/slide` Skill — Draft-to-Slide Pipeline

Create or update slides from markdown drafts in `./draft/`:

```bash
/slide draft/14_td_learning.md          # full pipeline: parse → build → validate → render
/slide td_learning                       # matches draft by topic name
/slide draft/14_td_learning.md --no-render    # skip rendering (fast iteration)
/slide draft/14_td_learning.md --no-validate  # skip math + layout validation
```

### Draft format

Markdown files in `./draft/` with YAML frontmatter. See `draft/TEMPLATE.md` for the full reference. Drafts can cite LaTeX chapters for equation sourcing:

```markdown
---
title: "Temporal Difference Learning"
slide_number: 14
---

<!-- cite: LaTex/chapters/05_aprendizaje_por_diferencias_temporales.tex, sections: 5.1 -->

# Temporal Difference Learning

## Key Ideas
- Bullet points for key concepts

$$V(s_t) \leftarrow V(s_t) + \alpha [r_{t+1} + \gamma V(s_{t+1}) - V(s_t)]$$

> **Definition**: TD error definition here.
```

### Pipeline

The skill orchestrates these agents: `draft-reader` + `style-inspector` (parallel) → `slide-builder`/`slide-updater` → `math-validator` → render → `slide-layout-validator`.

### Auto-render hook

A PostToolUse hook auto-renders slides when any `slides/*.py` file is created or modified via Write/Edit tools.
