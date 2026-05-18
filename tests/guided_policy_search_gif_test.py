from __future__ import annotations

import json
from pathlib import Path

from manim import *
from manim_slides import Slide


ASSET_DIR = Path(__file__).resolve().parent / "assets"
FRAME_DIR = ASSET_DIR / "animation_0_frames"
METADATA_PATH = FRAME_DIR / "metadata.json"
FALLBACK_FPS = 12.0
IMAGE_HEIGHT = 6.8
HUD_WIDTH = 4.2
PROGRESS_WIDTH = 3.0


class GuidedPolicySearchGifTest(Slide):
    def construct(self):
        frame_paths = sorted(FRAME_DIR.glob("frame_*.png"))
        if not frame_paths:
            self._show_missing_frames_notice()
            return

        playback_fps = self._load_playback_fps()
        playback_seconds = len(frame_paths) / playback_fps

        image = self._load_frame(frame_paths[0])
        frame = SurroundingRectangle(
            image,
            color=BLUE_D,
            buff=0.06,
            corner_radius=0.12,
            stroke_width=1.5,
        )
        hud = self._build_hud(playback_fps, len(frame_paths))
        progress_track, progress_fill = self._build_progress_bar(image)

        self.play(
            FadeIn(image, scale=0.98),
            Create(frame),
            FadeIn(hud, shift=0.15 * DOWN),
            FadeIn(progress_track),
            FadeIn(progress_fill),
        )
        self.next_slide()

        state = {"elapsed": 0.0, "frame_index": 0}

        # Swap frame PNGs over time to emulate GIF playback inside Manim.
        def update_frame(mob: ImageMobject, dt: float) -> None:
            state["elapsed"] = min(state["elapsed"] + dt, playback_seconds)
            next_index = min(int(state["elapsed"] * playback_fps), len(frame_paths) - 1)
            if next_index == state["frame_index"]:
                return

            state["frame_index"] = next_index
            mob.become(self._load_frame(frame_paths[next_index]))
            progress = state["elapsed"] / playback_seconds if playback_seconds else 1.0
            progress_fill.stretch_to_fit_width(max(0.001, progress * PROGRESS_WIDTH), about_point=progress_track.get_left())

        image.add_updater(update_frame)
        self.wait(playback_seconds)
        image.remove_updater(update_frame)

        self.next_slide()
        self.play(
            FadeOut(image),
            FadeOut(frame),
            FadeOut(hud),
            FadeOut(progress_track),
            FadeOut(progress_fill),
        )
        self.next_slide()

    def _load_frame(self, path: Path) -> ImageMobject:
        image = ImageMobject(str(path))
        image.scale_to_fit_height(IMAGE_HEIGHT)
        image.move_to(ORIGIN)
        return image

    def _build_hud(self, playback_fps: float, frame_count: int) -> VGroup:
        box = RoundedRectangle(
            width=HUD_WIDTH,
            height=0.9,
            corner_radius=0.16,
            color=BLUE_D,
            fill_opacity=0.12,
            stroke_width=1.5,
        )
        label = Text(
            f"GPS rollout  |  {frame_count} frames  |  {playback_fps:.1f} fps",
            font_size=20,
            color=GRAY_A,
        )
        label.move_to(box.get_center())
        hud = VGroup(box, label)
        hud.to_edge(DOWN, buff=0.3)
        return hud

    def _build_progress_bar(self, image: ImageMobject) -> tuple[RoundedRectangle, RoundedRectangle]:
        track = RoundedRectangle(
            width=PROGRESS_WIDTH,
            height=0.1,
            corner_radius=0.05,
            color=BLUE_D,
            fill_opacity=0.22,
            stroke_width=1,
        )
        track.next_to(image, DOWN, buff=0.16)
        track.align_to(image, LEFT)

        fill = RoundedRectangle(
            width=0.001,
            height=0.1,
            corner_radius=0.05,
            color=GREEN,
            fill_opacity=0.9,
            stroke_width=0,
        )
        fill.align_to(track, LEFT)
        fill.move_to(track.get_left() + RIGHT * 0.0005)
        return track, fill

    def _load_playback_fps(self) -> float:
        if not METADATA_PATH.exists():
            return FALLBACK_FPS

        try:
            metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
            playback_fps = float(metadata.get("playback_fps", FALLBACK_FPS))
            return playback_fps if playback_fps > 0 else FALLBACK_FPS
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return FALLBACK_FPS

    def _show_missing_frames_notice(self) -> None:
        box = RoundedRectangle(
            width=10.2,
            height=3.0,
            corner_radius=0.18,
            color=BLUE_D,
            fill_opacity=0.12,
            stroke_width=1.5,
        )
        headline = Text(
            "Extract PNG frames from the GIF before rendering this test.",
            font_size=28,
            color=WHITE,
        )
        command = Text(
            "python tests/extract_gif_frames.py",
            font_size=24,
            color=YELLOW,
        )
        content = VGroup(headline, command).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        panel = VGroup(box, content)
        content.move_to(box.get_center())
        panel.move_to(ORIGIN)

        self.play(FadeIn(panel, shift=0.2 * UP))
        self.next_slide()
