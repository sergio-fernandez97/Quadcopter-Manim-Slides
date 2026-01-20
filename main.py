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


def generate_html():
    """Generate HTML output."""
    from generate_html import main as gen_html
    gen_html()
    return 0


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
    subparsers.add_parser("html", help="Generate HTML output")

    args = parser.parse_args()

    if args.command == "render":
        return render_slides(args.slide)
    elif args.command == "present":
        return present_slides()
    elif args.command == "html":
        return generate_html()
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
