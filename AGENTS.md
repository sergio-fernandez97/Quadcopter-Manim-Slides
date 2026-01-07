# Repository Guidelines

## Project Structure & Module Organization
- `slides/`: Manim scene files for each slide, named with a two-digit order prefix (e.g., `00_inertial_frame.py`). Each file typically defines one `Slide` subclass.
- `slides.toml`: Presentation configuration and slide ordering.
- `slides_assets/`, `media/`, `manimations/`: Image/video outputs and asset files used by Manim/manim-slides.
- `tests/`: Minimal test area (currently a simple script).
- Top-level docs: `README.md`, `INSTALL.md`, `SETUP_GIT.md`.

## Build, Test, and Development Commands
- `manim-slides render slides.toml`: Render the full slide deck.
- `manim-slides present slides.toml`: Run the interactive presentation.
- `manim-slides preview slides/09_q_learning.py QLearningSlide`: Render/preview a single scene (replace file/class as needed).
- `manim-slides --version`: Verify installation.

## Coding Style & Naming Conventions
- Language: Python (Manim + manim-slides).
- Indentation: 4 spaces.
- Naming: slide files use `NN_topic.py` with a two-digit prefix; scene classes use `CamelCase` and end with `Slide` (e.g., `QLearningSlide`).
- Keep animations readable: group related mobjects into `VGroup`s and use short comments only for non-obvious blocks.

## Testing Guidelines
- No formal test suite is configured yet; `tests/hello.py` is a placeholder.
- When adding tests, prefer `pytest` and place files under `tests/` named `test_*.py`.
- Run tests (if added) with `pytest`.

## Commit & Pull Request Guidelines
- Recent history shows concise, sentence-style subjects (e.g., “Enhance MDP slide annotations”). Use short, descriptive imperatives.
- If your change adds or renames slides, update `slides.toml` and `README.md` accordingly.
- PRs should include a brief description of the visual change and, when helpful, a screenshot or short clip of the rendered scene.

## Notes for Contributors
- Keep generated media out of edits unless necessary; prefer checking in source updates under `slides/`.
- For new slides, follow the numeric sequence and document them in `README.md` (scene catalog + slide organization).
