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

# Bootstrap the dev integration branch for Claude slide work
.claude/scripts/bootstrap_dev_branch.sh

# Prepare a dedicated slide worktree from dev
.claude/scripts/prepare_slide_branch.sh --id 14 --slug td_learning
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
- **Color palette** (canonical, established in `slides/00_portrait.py`):
  - Titles / section headings: `BLUE_B`
  - Box borders, separators, and strokes: `BLUE_D`
  - Box fill background: `BLUE_D` with `fill_opacity=0.12, stroke_width=1.5`
  - Body / main text: `WHITE`
  - Subdued / secondary text: `GRAY_A`
  - Background: `BLACK` (configured in `slides.toml`, never set in code)
  - Semantic accents (titles, labels, equations, or any element that benefits from visual distinction):
    - `GREEN` — definitions, positive properties, update rules, algorithm outputs
    - `ORANGE` — alternatives, exploration, secondary concepts, local controllers
    - `RED_C` — warnings, problems, instabilities
    - `GOLD` — reward signals
    - `PURPLE` — neural network hidden layers
    - `YELLOW` — inline highlights within a slide (Lagrange multipliers, key variables being introduced)
  - Rule: body prose stays `WHITE`; use accent colors on the specific term or label that carries the semantic weight, not on entire paragraphs
- **Transitions**: Every scene must use `self.next_slide()` to create transition points between logical sections. These pauses allow the speaker to explain each element before proceeding. Place `next_slide()` after revealing new content (equations, diagrams, bullet points) that requires explanation.
- **Boxed content**: Wrap definitions, theorems, and bulleted lists (not simple labels) inside a rounded gray rectangle with high transparency. Example:
  ```python
  box = RoundedRectangle(corner_radius=0.2, width=10, height=2, color=BLUE_D, fill_opacity=0.12, stroke_width=1.5)
  content = BulletedList("Item 1", "Item 2", font_size=24)
  VGroup(box, content).arrange(ORIGIN)
  ```
- **Math rendering**: Every mathematical expression — variables, operators, equations, Greek letters, superscripts, subscripts — must be rendered with `MathTex` (for pure LaTeX math) or `Tex` (for mixed text+math). Never render math inside a plain `Text` object, not even inline symbols like θ, λ, or x_t. When mixing prose and math in a single line, use `VGroup` of `Text` + `MathTex` arranged horizontally, or use `Tex` with `\text{}` for the prose portion.
- **Concise text**: Minimize words in theorems and definitions. You may rephrase user-provided content for brevity while preserving meaning.
- When adding slides: create file in `slides/`, add scene path to `slides.toml`
- Keep generated media (`media/`) out of commits; only commit source files under `slides/`

## Git Workflow

- The integration branch for slide work is `dev`.
- New slide work should be done from a dedicated `slide/*` feature branch created from `dev`.
- Preferred branch format: `slide/<nn>-<topic-slug>`.
- Preferred workflow:
  1. Run `.claude/scripts/bootstrap_dev_branch.sh` once to create or track `dev`.
  2. Run `.claude/scripts/prepare_slide_branch.sh --id <nn> --slug <topic_slug>` to create or reuse a worktree under `.worktrees/`.
  3. Launch a dedicated `claude --worktree` session from that worktree path.
  4. Run `/slide <draft-or-topic>` inside that worktree session.
- Never publish slide work from `main`.
- Never publish slide work directly from `dev`.
- PRs for slide work must target `dev`.
- Only stage source files that belong to the slide task. Do not include `media/` or `presentation/` outputs unless the user explicitly asks for generated artifacts in git.

## GitHub Integration

- Context7 is required before writing Manim or manim-slides code.
- PR automation expects a GitHub integration in Claude Code:
  - preferred: a configured GitHub MCP/app so Claude can create or update PRs directly
  - fallback: authenticated `gh` CLI
- If neither GitHub MCP nor authenticated `gh` is available, the workflow may still push the feature branch but must report that PR creation remains manual.

## `/slide` Skill — Draft-to-Slide Pipeline

Create or update slides from markdown drafts in `./draft/`:

```bash
/slide draft/14_td_learning.md                # full pipeline: parse → build → validate → render → publish to dev PR
/slide td_learning                       # matches draft by topic name
/slide draft/14_td_learning.md --no-render    # skip rendering (fast iteration)
/slide draft/14_td_learning.md --no-validate  # skip math + layout validation
/slide draft/14_td_learning.md --no-publish   # build/update only, no commit/push/PR
/slide draft/14_td_learning.md --draft-pr     # open the PR as draft
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

The skill orchestrates these agents: `draft-reader` + `style-inspector` (parallel) → `slide-builder`/`slide-updater` → `math-validator` → render → `slide-layout-validator` → `slide-publisher`.

### Worktree guardrails

- If `/slide` is run on `main` or `dev` with publishing enabled, it must stop before any Git publication step and direct the user to `/worktree_slide`.
- If `/slide` is run from a feature branch that does not match `slide/*`, it must not auto-publish unless that branch is explicitly confirmed as intentional.
- `/worktree_slide` is the preparation command for creating or reusing a slide-specific worktree before opening a dedicated Claude worktree session.

### Auto-render hook

A PostToolUse hook auto-renders slides when any `slides/*.py` file is created or modified via Write/Edit tools.
