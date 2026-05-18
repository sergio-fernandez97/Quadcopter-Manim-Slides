from pathlib import Path

from manim import *
from manim_slides import Slide


ASSET_DIR = Path(__file__).resolve().parent / "assets"
IMAGE_PATH = ASSET_DIR / "guided_policy_search.png"
ZOOM_SHIFT = 0.35 * RIGHT + 0.18 * UP
ZOOM_SCALE = 1.08


class GuidedPolicySearchImageTest(Slide):
    def construct(self):
        title = Text(
            "Guided Policy Search Snapshot",
            font_size=34,
            color=BLUE_B,
        ).to_edge(UP, buff=0.35)

        self.play(FadeIn(title, shift=0.2 * DOWN))

        if not IMAGE_PATH.exists():
            self._show_missing_asset_notice(title)
            return

        image = ImageMobject(str(IMAGE_PATH))
        image.scale_to_fit_height(5.8)
        image.next_to(title, DOWN, buff=0.3)

        frame = SurroundingRectangle(
            image,
            color=BLUE_D,
            buff=0.06,
            corner_radius=0.12,
            stroke_width=1.5,
        )
        stage = VGroup(image, frame)

        caption = Text(
            "Simple test: fade in, zoom, then highlight the state plot and reward.",
            font_size=24,
            color=GRAY_A,
        )
        caption.next_to(image, DOWN, buff=0.28)
        caption.align_to(image, LEFT)

        self.play(FadeIn(image, scale=0.98), Create(frame))
        self.next_slide()

        self.play(stage.animate.scale(ZOOM_SCALE).shift(ZOOM_SHIFT), run_time=2.5, rate_func=smooth)

        state_focus = self._focus_box(width=3.45, height=3.0)
        state_focus.move_to(image.get_center() + 1.1 * RIGHT + 0.52 * UP)

        reward_focus = self._focus_box(width=2.65, height=1.28)
        reward_focus.move_to(image.get_center() + 2.98 * LEFT + 2.18 * DOWN)

        self.play(FadeIn(caption, shift=0.15 * UP), Create(state_focus))
        self.next_slide()

        self.play(ReplacementTransform(state_focus, reward_focus), run_time=1.4)
        self.next_slide()

        self.play(
            FadeOut(reward_focus),
            FadeOut(caption),
            stage.animate.scale(1 / ZOOM_SCALE).shift(-ZOOM_SHIFT),
            run_time=1.6,
            rate_func=smooth,
        )
        self.next_slide()

    def _focus_box(self, width: float, height: float) -> RoundedRectangle:
        return RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.16,
            color=YELLOW,
            stroke_width=3,
        ).set_fill(YELLOW, opacity=0.08)

    def _show_missing_asset_notice(self, title: Text):
        box = RoundedRectangle(
            width=9.4,
            height=2.7,
            corner_radius=0.18,
            color=BLUE_D,
            fill_opacity=0.12,
            stroke_width=1.5,
        )

        headline = Text(
            "Add the screenshot below to preview the image animation.",
            font_size=28,
            color=WHITE,
        )
        asset_path = Text(
            str(IMAGE_PATH.relative_to(Path.cwd())),
            font_size=24,
            color=YELLOW,
        )

        content = VGroup(headline, asset_path).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        panel = VGroup(box, content)
        content.move_to(box.get_center())
        panel.next_to(title, DOWN, buff=0.5)

        self.play(FadeIn(panel, shift=0.2 * UP))
        self.next_slide()
