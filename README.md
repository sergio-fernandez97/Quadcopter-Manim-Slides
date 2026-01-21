# Quadcopter-Manim-Slides - Dissertation Presentation

A manim-slides presentation for the dissertation on Quadcopter Control using Deep Reinforcement Learning.

## Project Structure

```
.
├── slides/              # Slide scenes organized by presentation sections
│   ├── __init__.py
│   ├── 00_inertial_frame.py
│   ├── 01_newton_euler.py
│   ├── 02_inertial_dynamics.py
│   ├── 03_quadcopter_motion.py
│   ├── 04_control_systems.py
│   ├── 05_controllability.py
│   ├── 06_stabilization.py
│   └── 07_agent_environment.py
├── slides.toml          # Presentation configuration
├── requirements.txt     # Python dependencies
└── README.md
```

## Slide Python scripts

The `slides/` directory contains the Python scripts that define each scene:

- Files are numbered with a two-digit prefix to control ordering (e.g., `00_inertial_frame.py`).
- Each file typically exposes a single Manim Scene class that represents one slide or section.
- Supporting helpers for slides live alongside the scenes so that related visuals stay close to their definitions.
- `__init__.py` wires the package together so scenes can be imported with dotted paths (e.g., `slides.00_inertial_frame`).

You can add new slides by creating an additional `NN_name.py` file and including the scene in `slides.toml` under the desired section.

### Scene catalog

Each slide script includes the author, the Manim scene class it defines, and a short description of its focus:

| File | Scene class | Description | Author |
| --- | --- | --- | --- |
| `00_inertial_frame.py` | `InertialFrameSlide` | Visualizes the quadcopter in a 3D inertial frame, highlighting rotor forces and roll motion with labeled axes. | Sergio Fernández |
| `01_newton_euler.py` | `NewtonEulerSlide` | Derives translation and rotation dynamics in the body frame from Newton–Euler equations, emphasizing linear and angular velocities. | Sergio Fernández |
| `02_inertial_dynamics.py` | `InertialDynamicsSlide` | Links local velocities to inertial coordinates, introducing translation and rotation dynamics in the inertial frame. | Sergio Fernández |
| `03_quadcopter_motion.py` | `QuadcopterMotionSlide` | Presents the full equations of motion for the quadcopter in both local and inertial systems, coloring state and control variables. | Sergio Fernández |
| `04_control_systems.py` | `ControlSystemsSlide` | Introduces the control system model, walking through continuous and discrete representations before linearization. | Sergio Fernández |
| `05_controllability.py` | `ControllabilitySlide` | Defines controllability for linear systems and explains reachable states using the state-space solution. | Sergio Fernández |
| `06_stabilization.py` | `StabilizationSlide` | Explains stabilization of linear systems via state-feedback control, focusing on the closed-loop formulation. | Sergio Fernández |
| `07_agent_environment.py` | `AgentEnvironmentSlide` | Depicts the reinforcement learning agent–environment loop with actions, rewards, and state transitions. | Sergio Fernández |

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

3. Install uv (if not installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

4. Install Python dependencies:
   ```bash
   uv sync
   ```

### Verify Installation

```bash
uv run manim-slides --version
```

## Usage

### Common manim-slides commands

- **Render a specific scene**
  ```bash
  uv run manim-slides render slides/00_inertial_frame.py InertialFrameSlide
  ```
- **Preview a specific scene**
  ```bash
  uv run manim-slides preview slides/00_inertial_frame.py InertialFrameSlide
  ```
- **Render the whole presentation**
  ```bash
  uv run manim-slides render slides.toml
  ```

### Render all slides
```bash
uv run manim-slides render slides.toml
```

### Present the slides
```bash
uv run manim-slides present slides.toml
```

### Render a specific slide
```bash
uv run manim-slides render slides/00_inertial_frame.py InertialFrameSlide
```

### Preview a slide
```bash
uv run manim-slides preview slides/00_inertial_frame.py InertialFrameSlide
```

## Slide Organization

The slides are organized in a logical flow:

1. **Inertial Frame** (`00_inertial_frame.py`) - 3D view of the quadcopter model and rotor forces in the inertial frame
2. **Newton–Euler Dynamics** (`01_newton_euler.py`) - Body-frame translation and rotation equations from Newton–Euler laws
3. **Inertial Dynamics** (`02_inertial_dynamics.py`) - Mapping body velocities to inertial coordinates
4. **Equations of Motion** (`03_quadcopter_motion.py`) - Complete motion equations in local and inertial systems
5. **Control Systems** (`04_control_systems.py`) - State-space control formulation and linearization steps
6. **Controllability** (`05_controllability.py`) - Criteria for reachability in linear systems
7. **Stabilization** (`06_stabilization.py`) - State-feedback stabilization strategy
8. **Agent–Environment Loop** (`07_agent_environment.py`) - Reinforcement learning interaction diagram

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

