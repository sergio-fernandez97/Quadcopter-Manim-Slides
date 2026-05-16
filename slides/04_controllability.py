"""
Controllability concepts for the quadcopter control model.

Defines controllability for linear systems, presents the algebraic criteria,
and illustrates state reachability within the slide sequence.

Example:
    manim -pql slides/04_controllability.py ControllabilitySlide

Author: Sergio Fernández
Date: 2025-01-30
"""

from manim import *
from manim_slides import Slide


class ControllabilitySlide(Slide):
    def construct(self):
        # ── Title (stays visible throughout) ──────────────────────────────────
        title = Text("Controlabilidad", font_size=42, color=BLUE_B)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        # ── FRAME 1 — Intuición + Definición formal ───────────────────────────
        intuition = Text(
            "La controlabilidad indica si un sistema puede llevar su estado a un\n"
            "objetivo mediante una entrada adecuada en tiempo finito.",
            font_size=24,
            color=WHITE,
        )
        intuition.to_edge(LEFT, buff=0.8)
        intuition.shift(UP * 1.8)

        sys_eq = MathTex(
            r"\dot{\mathbf{x}} = \mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{u}",
            font_size=32,
        )
        reach_eq = MathTex(
            r"\mathbf{x}_1 = \mathbf{x}(t_1;\, \mathbf{x}_0,\, \mathbf{u})",
            font_size=32,
        )
        bullet_given = MathTex(
            r"\text{dado }\ \mathbf{x}_0 \in \mathbb{R}^{n_x}",
            font_size=22,
            color=WHITE,
        )
        bullet_ctrl = MathTex(
            r"\mathbf{x}_0\ \text{se dice }",
            r"\textbf{controlable}",
            r"\text{ al estado }\ \mathbf{x}_1",
            font_size=22,
        )
        bullet_ctrl[1].set_color(YELLOW)
        bullet_reach = MathTex(
            r"\mathbf{x}_1\text{ es un }",
            r"\textbf{estado alcanzable}",
            r"\text{ desde }\ \mathbf{x}_0",
            font_size=22,
        )
        bullet_reach[1].set_color(YELLOW)
        bullets = VGroup(bullet_given, bullet_ctrl, bullet_reach).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15
        )
        def_content = VGroup(sys_eq, reach_eq, bullets).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35
        )
        def_content.next_to(intuition, DOWN, buff=0.5, aligned_edge=LEFT)

        def_box = RoundedRectangle(
            corner_radius=0.2,
            width=def_content.width + 0.8,
            height=def_content.height + 0.5,
            color=BLUE_D,
            fill_opacity=0.12,
            stroke_width=1.5,
        )
        def_box.move_to(def_content)

        self.play(FadeIn(intuition))
        self.play(FadeIn(def_box), FadeIn(def_content))
        self.wait(0.5)
        self.next_slide()

        self.play(FadeOut(intuition), FadeOut(def_box), FadeOut(def_content))
        self.wait(0.3)

        # ── FRAME 2 — Matriz de controlabilidad + Teorema de Kalman ──────────
        matrix_label = Text("Matriz de Controlabilidad", font_size=30, color=BLUE)
        matrix_label.to_edge(LEFT, buff=0.8)
        matrix_label.shift(UP * 2.0)

        matrix_eq = MathTex(
            r"R(\mathbf{A}, \mathbf{B}) = "
            r"\left[\mathbf{B}\ \mathbf{AB}\ \mathbf{A}^2\mathbf{B}\ \cdots\ "
            r"\mathbf{A}^{n_x-1}\mathbf{B}\right]"
            r"\in \mathbb{R}^{n_x \times n_u \cdot n_x}",
            font_size=28,
        )
        annotation = MathTex(
            r"[\,\cdot\,]\ \text{denota concatenación horizontal de bloques}",
            font_size=20,
            color=GRAY_A,
        )
        matrix_group = VGroup(matrix_eq, annotation).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25
        )
        matrix_group.next_to(matrix_label, DOWN, buff=0.3, aligned_edge=LEFT)

        matrix_box = RoundedRectangle(
            corner_radius=0.2,
            width=matrix_group.width + 0.8,
            height=matrix_group.height + 0.5,
            color=BLUE_D,
            fill_opacity=0.12,
            stroke_width=1.5,
        )
        matrix_box.move_to(matrix_group)

        kalman_label = Text("Teorema de Kalman", font_size=30, color=BLUE)
        kalman_label.next_to(matrix_box, DOWN, buff=0.5, aligned_edge=LEFT)

        rank_eq = MathTex(
            r"\operatorname{rango}\!\left(R(\mathbf{A}, \mathbf{B})\right) = n_x",
            font_size=34,
        )
        kalman_text = Text(
            "El sistema es completamente controlable si y sólo si se cumple esta condición.",
            font_size=20,
            color=WHITE,
        )
        kalman_pair = MathTex(
            r"(\mathbf{A},\,\mathbf{B})\ \text{se denomina }",
            r"\textbf{controlable}",
            font_size=20,
        )
        kalman_pair[1].set_color(YELLOW)
        kalman_content = VGroup(rank_eq, kalman_text, kalman_pair).arrange(
            DOWN, buff=0.25
        )
        kalman_content.next_to(kalman_label, DOWN, buff=0.3, aligned_edge=LEFT)

        kalman_box = RoundedRectangle(
            corner_radius=0.2,
            width=kalman_content.width + 0.8,
            height=kalman_content.height + 0.5,
            color=BLUE_D,
            fill_opacity=0.12,
            stroke_width=1.5,
        )
        kalman_box.move_to(kalman_content)

        self.play(FadeIn(matrix_label), FadeIn(matrix_box), FadeIn(matrix_group))
        self.wait(0.5)
        self.next_slide()

        self.play(FadeIn(kalman_label), FadeIn(kalman_box), FadeIn(kalman_content))
        self.wait(0.5)
        self.next_slide()
