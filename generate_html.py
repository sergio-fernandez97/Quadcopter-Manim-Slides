#!/usr/bin/env python3
"""Export the dissertation deck as a single offline HTML presentation."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:  # pragma: no cover - Python 3.11+ is required by the project
    tomllib = None


DEFAULT_OUTPUT = Path("presentation/dissertation_defense.html")
DEFAULT_SLIDES_TOML = Path("slides.toml")
DEFAULT_SLIDES_FOLDER = Path("slides")


def load_scene_order(slides_toml: Path = DEFAULT_SLIDES_TOML) -> list[str]:
    """Return the ordered scene class names from ``slides.toml``."""
    if not slides_toml.exists():
        raise FileNotFoundError(f"Missing slides configuration: {slides_toml}")

    if tomllib is not None:
        with slides_toml.open("rb") as file:
            data = tomllib.load(file)
        slide_entries = data.get("slides", {}).get("slides", [])
        return [
            entry.rsplit(".", 1)[-1]
            for entry in slide_entries
            if isinstance(entry, str)
        ]

    text = slides_toml.read_text(encoding="utf-8")
    match = re.search(r"(?s)\[slides\].*?slides\s*=\s*\[(.*?)\]", text)
    if not match:
        raise ValueError(f"Could not parse ordered slides from {slides_toml}")

    entries = re.findall(r"\"([^\"]+)\"", match.group(1))
    return [entry.rsplit(".", 1)[-1] for entry in entries]


def get_missing_scene_exports(
    scene_order: list[str],
    slides_folder: Path = DEFAULT_SLIDES_FOLDER,
) -> list[str]:
    """Return scene names missing rendered ``.json`` metadata."""
    return [
        scene_name
        for scene_name in scene_order
        if not (slides_folder / f"{scene_name}.json").exists()
    ]


def build_convert_command(
    scene_order: list[str],
    output_path: Path,
    slides_folder: Path = DEFAULT_SLIDES_FOLDER,
) -> list[str]:
    """Build the ``manim-slides convert`` command for a single-file deck."""
    return [
        "manim-slides",
        "convert",
        "--to",
        "html",
        "--folder",
        str(slides_folder),
        "--one-file",
        "--offline",
        "--config",
        "controls=true",
        *scene_order,
        str(output_path),
    ]


def render_presentation(slides_toml: Path = DEFAULT_SLIDES_TOML) -> int:
    """Render the ordered deck defined in ``slides.toml``."""
    command = ["manim-slides", "render", str(slides_toml)]
    return subprocess.run(command).returncode


def export_html(
    output_path: Path = DEFAULT_OUTPUT,
    slides_toml: Path = DEFAULT_SLIDES_TOML,
    slides_folder: Path = DEFAULT_SLIDES_FOLDER,
    render_first: bool = False,
) -> int:
    """Export the canonical dissertation deck to one offline HTML file."""
    output_path = Path(output_path)
    scene_order = load_scene_order(slides_toml)

    if not scene_order:
        print(f"No scenes found in {slides_toml}", file=sys.stderr)
        return 1

    if render_first:
        print(f"Rendering slides from {slides_toml}...")
        render_return_code = render_presentation(slides_toml)
        if render_return_code != 0:
            return render_return_code

    missing_scenes = get_missing_scene_exports(scene_order, slides_folder)
    if missing_scenes:
        print(
            "Missing rendered slide metadata for: "
            + ", ".join(missing_scenes),
            file=sys.stderr,
        )
        print(
            "Run `uv run python main.py render` first, or re-run this command "
            "with `--render-first`.",
            file=sys.stderr,
        )
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = build_convert_command(scene_order, output_path, slides_folder)
    print(
        "Exporting dissertation deck from slides.toml order to "
        f"{output_path}..."
    )
    return subprocess.run(command).returncode


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for HTML export."""
    parser = argparse.ArgumentParser(
        description="Export the dissertation deck as one offline HTML file."
    )
    parser.add_argument(
        "--output",
        "-o",
        default=str(DEFAULT_OUTPUT),
        help="Destination HTML file. Defaults to presentation/dissertation_defense.html.",
    )
    parser.add_argument(
        "--render-first",
        action="store_true",
        help="Render slides.toml before converting to HTML.",
    )
    return parser.parse_args()


def main() -> int:
    """CLI entry point."""
    args = parse_args()
    return export_html(
        output_path=Path(args.output),
        render_first=args.render_first,
    )


if __name__ == "__main__":
    sys.exit(main())
