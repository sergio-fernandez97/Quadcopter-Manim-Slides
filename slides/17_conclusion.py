"""
Conclusion slide: two-column layout with summary findings (Conclusión)
and future research directions (Trabajo futuro).

Example:
    uv run manim-slides render slides/17_conclusion.py ConclusionSlide
"""

from manim import *
from manim_slides import Slide


class ConclusionSlide(Slide):
    """Conclusión y trabajo futuro — two-column boxed bullet lists."""

    def construct(self):
        # --- Helpers ---
        def make_box(mobject, color=GRAY, fill_opacity=0.15, stroke_width=1):
            box = RoundedRectangle(
                corner_radius=0.2,
                width=mobject.width + 0.8,
                height=mobject.height + 0.6,
                color=color,
                fill_opacity=fill_opacity,
                stroke_width=stroke_width,
            )
            box.move_to(mobject)
            return box

        def shrink_to_fit_width(mobject, max_width):
            if mobject.width > max_width:
                mobject.scale_to_fit_width(max_width)
            return mobject

        # --- Title ---
        title = Text("Conclusión y trabajo futuro", font_size=40, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))
        self.wait(0.5)
        self.next_slide()

        # --- Left column: Conclusión ---
        col_max_width = config.frame_width / 2 - 1.0

        conclusion_label = Text("Conclusión", font_size=28, color=BLUE)
        conclusion_items = VGroup(
            Text("• GPS y DDPG evaluados en vuelo", font_size=19, color=WHITE),
            Text("• GPS aproximó el desempeño de iLQR", font_size=19, color=WHITE),
            Text("• DDPG mostró inestabilidad crónica", font_size=19, color=WHITE),
            Text("• Control clásico: estabilidad más clara", font_size=19, color=WHITE),
            Text("• GPS: potencial con límites globales", font_size=19, color=WHITE),
            Text("• Confiabilidad sensible al entrenamiento", font_size=19, color=WHITE),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)

        conclusion_group = VGroup(conclusion_label, conclusion_items).arrange(
            DOWN, buff=0.3, aligned_edge=LEFT
        )
        shrink_to_fit_width(conclusion_group, col_max_width)
        conclusion_group.move_to(LEFT * 3.2 + DOWN * 1.0)
        conclusion_box = make_box(conclusion_group)

        # --- Right column: Trabajo futuro ---
        future_label = Text("Trabajo futuro", font_size=28, color=BLUE)
        future_items = VGroup(
            Text("• Extender GPS a esquemas MPC-GPS", font_size=19, color=WHITE),
            Text("• Explorar TD3 y SAC como alternativas", font_size=19, color=WHITE),
            Text("• Refinar la función de recompensa", font_size=19, color=WHITE),
            Text("• Comparar con criterios homogéneos", font_size=19, color=WHITE),
            Text("• Muestreo desde regiones estables", font_size=19, color=WHITE),
            Text("• Estrategias híbridas: clásico + ANN", font_size=19, color=WHITE),
            Text("• Arquitecturas ANN más robustas", font_size=19, color=WHITE),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)

        future_group = VGroup(future_label, future_items).arrange(
            DOWN, buff=0.3, aligned_edge=LEFT
        )
        shrink_to_fit_width(future_group, col_max_width)
        future_group.move_to(RIGHT * 3.2 + DOWN * 1.0)
        future_box = make_box(future_group)

        # --- Reveal both columns together ---
        self.play(
            FadeIn(conclusion_box),
            FadeIn(conclusion_group),
            FadeIn(future_box),
            FadeIn(future_group),
        )
        self.wait(0.5)
        self.next_slide()

        self.wait(1)
