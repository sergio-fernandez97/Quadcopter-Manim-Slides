#!/usr/bin/env python3
"""Main entry point for the Quadcopter Manim Slides project."""

import argparse
import subprocess
import sys
from pathlib import Path


def render_slides(specific_slide: str = None):
    """Render slides using manim-slides."""
    if specific_slide:
        cmd = ["manim-slides", "render", f"slides/{specific_slide}"]
    else:
        cmd = ["manim-slides", "render", "slides.toml"]
    return subprocess.run(cmd).returncode


def present_slides():
    """Launch interactive presentation."""
    return subprocess.run(["manim-slides", "present", "slides.toml"]).returncode


def generate_html(output: str = None, render_first: bool = False):
    """Generate one self-contained HTML deck for the dissertation."""
    from generate_html import export_html

    return export_html(
        output_path=(
            Path(output)
            if output
            else Path("presentation/dissertation_defense.html")
        ),
        render_first=render_first,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Quadcopter Deep RL Presentation"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Render command
    render_parser = subparsers.add_parser("render", help="Render slides")
    render_parser.add_argument("--slide", "-s", help="Render specific slide file")

    # Present command
    subparsers.add_parser("present", help="Launch interactive presentation")

    # HTML command
    html_parser = subparsers.add_parser(
        "html",
        help="Generate one offline HTML deck from slides.toml order",
    )
    html_parser.add_argument(
        "--output",
        "-o",
        help="Destination HTML file",
    )
    html_parser.add_argument(
        "--render-first",
        action="store_true",
        help="Render slides.toml before converting to HTML",
    )

    args = parser.parse_args()

    if args.command == "render":
        return render_slides(args.slide)
    elif args.command == "present":
        return present_slides()
    elif args.command == "html":
        return generate_html(args.output, args.render_first)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
