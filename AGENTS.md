# Repository Guidelines

## Project Overview
- This repository contains an animated dissertation presentation for quadcopter control with Deep Reinforcement Learning.
- The stack is `manim` + `manim-slides`, with `main.py` as the main CLI entry point and `generate_html.py` for Reveal.js-style HTML output.
- The presentation should feel academically rigorous and visually close to a Beamer defense deck: static-first, clear, and paced for explanation.

## Project Structure & Module Organization
- `slides/`: Manim scene files, named with a two-digit order prefix such as `00_inertial_frame.py`. Each file typically defines one `*Slide` class.
- `slides.toml`: Presentation configuration and slide ordering.
- `main.py`: Main CLI entry point for render, present, and HTML workflows.
- `generate_html.py`: Converts rendered slides to HTML output.
- `presentation/`: Generated HTML slide outputs.
- `draft/`: Markdown draft inputs for slide creation/update workflows.
- `LaTex/`: Dissertation source material, especially `LaTex/chapters/` for mathematical and narrative grounding.
- `slides_assets/`, `media/`, `manimations/`: Assets and generated media.
- `tests/`: Minimal test area; currently lightweight.
- Top-level docs: `README.md`, `INSTALL.md`, `SETUP_GIT.md`, `CLAUDE.md`.

## Build, Test, and Development Commands
- `uv sync`: Install dependencies. FFmpeg is required.
- `uv run python main.py render`: Render the full slide deck.
- `uv run python main.py present`: Launch the interactive presentation.
- `uv run python main.py html`: Generate HTML output.
- `uv run manim-slides render slides/00_inertial_frame.py InertialFrameSlide`: Render a single scene.
- `uv run manim-slides present InertialFrameSlide`: Present a single rendered scene.
- `uv run manim-slides convert SCENE scene.html -ccontrols=true`: Convert a rendered scene to HTML.
- `uv run manim-slides --version`: Verify installation.
- `pytest`: Run tests if a real test suite is added under `tests/`.

## Presentation Controls
- `Space` or `Right Arrow`: Next slide.
- `Left Arrow`: Previous slide.
- `Q`: Quit presentation.
- `R`: Restart presentation.

## Coding Style & Naming Conventions
- Language: Python with `manim` and `manim-slides`.
- Indentation: 4 spaces.
- Slide files use `NN_topic_name.py`.
- Scene classes use `CamelCase` and must end with `Slide`.
- Group related mobjects with `VGroup`.
- Use short comments only for non-obvious animation or layout blocks.
- Keep slides concise and presentation-oriented rather than document-like.

## Manim Slide Conventions
- Use `Slide` or `ThreeDSlide` as appropriate.
- Every scene must use `self.next_slide()` to create speaker-controlled transition points between logical sections.
- Place `self.next_slide()` after revealing content that requires explanation.
- Prefer clarity over motion. Animations should emphasize, not distract.
- Use `BulletedList` for key concepts when bullet structure helps.
- Wrap definitions, theorems, and bulleted content inside a rounded gray rectangle with high transparency when appropriate.
- Minimize text. Rephrase for brevity while preserving meaning.
- Keep scene composition close to a Beamer-style research presentation.

## Required Reference Rule
- When generating, editing, or debugging `manim` or `manim-slides` code, use Context7 as the primary reference source before writing code.
- Retrieve relevant API usage or examples first, then ground code changes in that context.
- If local knowledge conflicts with retrieved documentation, prefer the documentation.

## Architecture
```text
slides/                  # Numbered Manim scene files
slides.toml              # Slide ordering/config
main.py                  # Render/present/html entry point
generate_html.py         # HTML generation
draft/                   # Markdown drafts for slide workflows
LaTex/chapters/          # Dissertation chapters used as source material
presentation/            # Generated HTML slide outputs
```

Rendering pipeline:
`Python scene -> Manim render -> FFmpeg MP4 -> manim-slides presentation/convert`

## Draft-to-Slide Workflow
- Drafts live in `draft/` and may include YAML frontmatter plus optional citations into `LaTex/chapters/*.tex`.
- Use drafts to drive new slide creation or targeted updates.
- Preferred workflow:
  1. Parse the markdown draft and frontmatter.
  2. Read cited LaTeX chapters or sections for authoritative equations and notation.
  3. Inspect existing slide style before building or updating scenes.
  4. Build or update the target slide surgically.
  5. Validate math against the source material.
  6. Render the slide.
  7. Convert it to HTML for layout review.

## Repo-Specific Agent Workflow
- Treat `LaTex/chapters/` as ground truth for mathematical content.
- Do not invent equations, notation, or dissertation claims.
- For existing slides, make surgical updates and preserve everything outside scope.
- For multi-slide narrative work, check continuity across the presentation sequence, not only the edited slide.
- When working from drafts, preserve traceability from slide content back to markdown and LaTeX sources.

Specialized responsibilities reflected by `.claude/agents/`:
- Draft extraction: parse markdown drafts and cited LaTeX into structured content.
- Style inspection: infer canonical visual/layout patterns from existing slides.
- Slide building/updating: create new slides or make scoped edits without unrelated refactors.
- Math validation: verify every scene equation against source material.
- Layout validation: inspect rendered HTML slides for overlap and out-of-viewport issues.
- Continuity review: assess narrative flow, pacing, prerequisites, and coverage gaps across the deck.

## Automation and Guardrails
- Never read or expose `.env`.
- When a `slides/*.py` file is modified, the preferred repo workflow is to:
  1. Render that slide with `uv run manim-slides render <file> <ClassName>`.
  2. Convert it to HTML at `presentation/<slide_name>.html` using `uv run manim-slides convert <ClassName> presentation/<slide_name>.html -ccontrols=true`.
- If rendering fails, treat that as part of the task and report the failure clearly.

## Testing and Validation Guidelines
- No formal suite is established yet; `tests/hello.py` is a placeholder.
- When adding tests, prefer `pytest` with files named `tests/test_*.py`.
- For slide work, validation is not just unit tests:
  - verify rendering succeeds
  - verify HTML conversion succeeds when layout review is needed
  - verify equations and notation match the LaTeX source
  - verify edited slides still fit the overall presentation flow

## Commit & Pull Request Guidelines
- Use short, descriptive, imperative commit messages.
- A conventional-commit style is acceptable when it fits the change.
- Review with `git status` and `git diff` before committing.
- Stage only relevant files.
- If a change adds or renames slides, update `slides.toml` and `README.md` accordingly.
- PRs should briefly describe the visual or narrative change and include screenshots or a short clip when that materially helps review.

## Notes for Contributors
- Prefer editing source files under `slides/`, `draft/`, `LaTex/`, and docs rather than generated outputs.
- Keep generated media out of source edits unless necessary.
- For new slides, follow the numeric sequence and document them in `README.md`.
- Check both local slide quality and dissertation-level coherence when making substantive presentation changes.
