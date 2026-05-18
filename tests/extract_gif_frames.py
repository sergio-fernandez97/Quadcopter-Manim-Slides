from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageSequence


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract a GIF into numbered PNG frames for Manim tests.",
    )
    parser.add_argument(
        "input_gif",
        type=Path,
        nargs="?",
        default=Path("tests/assets/animation_0.gif"),
        help="Path to the source GIF.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory where extracted frames will be written. Defaults to <gif_stem>_frames.",
    )
    parser.add_argument(
        "--frame-step",
        type=int,
        default=5,
        help="Keep every Nth source frame. Higher values compress long GIFs into shorter tests.",
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=120,
        help="Maximum number of PNG frames to write.",
    )
    parser.add_argument(
        "--playback-fps",
        type=float,
        default=12.0,
        help="Target playback fps for the Manim test scene.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing extracted PNG frames in the output directory.",
    )
    return parser.parse_args()


def clear_previous_outputs(output_dir: Path) -> None:
    for path in output_dir.glob("frame_*.png"):
        path.unlink()
    metadata_path = output_dir / "metadata.json"
    if metadata_path.exists():
        metadata_path.unlink()


def main() -> None:
    args = parse_args()
    input_gif = args.input_gif.resolve()

    if not input_gif.exists():
        raise FileNotFoundError(f"GIF not found: {input_gif}")
    if args.frame_step < 1:
        raise ValueError("--frame-step must be >= 1")
    if args.max_frames < 1:
        raise ValueError("--max-frames must be >= 1")
    if args.playback_fps <= 0:
        raise ValueError("--playback-fps must be > 0")

    output_dir = args.output_dir or input_gif.with_name(f"{input_gif.stem}_frames")
    output_dir.mkdir(parents=True, exist_ok=True)

    existing_frames = list(output_dir.glob("frame_*.png"))
    if existing_frames and not args.overwrite:
        raise FileExistsError(
            f"Output directory already contains extracted frames: {output_dir}. "
            "Use --overwrite to replace them."
        )
    if args.overwrite:
        clear_previous_outputs(output_dir)

    with Image.open(input_gif) as gif:
        original_frame_count = getattr(gif, "n_frames", 1)
        saved_count = 0
        selected_source_indices: list[int] = []

        for source_index, frame in enumerate(ImageSequence.Iterator(gif)):
            if source_index % args.frame_step != 0:
                continue
            if saved_count >= args.max_frames:
                break

            frame_path = output_dir / f"frame_{saved_count:04d}.png"
            frame.convert("RGBA").save(frame_path)
            selected_source_indices.append(source_index)
            saved_count += 1

        if saved_count == 0:
            raise RuntimeError("No frames were extracted. Check --frame-step and source GIF.")

        metadata = {
            "source_gif": str(input_gif),
            "output_dir": str(output_dir.resolve()),
            "original_frame_count": original_frame_count,
            "saved_frame_count": saved_count,
            "frame_step": args.frame_step,
            "selected_source_indices": selected_source_indices,
            "playback_fps": args.playback_fps,
            "playback_seconds": saved_count / args.playback_fps,
        }
        (output_dir / "metadata.json").write_text(
            json.dumps(metadata, indent=2),
            encoding="utf-8",
        )

    print(f"Extracted {saved_count} frames to {output_dir}")
    print(f"Playback length at {args.playback_fps:.2f} fps: {saved_count / args.playback_fps:.2f}s")


if __name__ == "__main__":
    main()
