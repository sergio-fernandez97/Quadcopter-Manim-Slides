"""
Stability concepts and feedback stabilization for linear control systems.

Covers intuitive and formal notions of stability (Lyapunov, asymptotic,
exponential), the feedback stabilization problem, and the pole assignment theorem.

Example:
    manim -pql slides/05_stabilization.py StabilizationSlide
"""

from manim import *
from manim_slides import Slide


class StabilizationSlide(Slide):
    """Stability and feedback stabilization for linear control systems."""

    def construct(self):
        title = Text("Estabilidad", font_size=42, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))
        self.wait(0.5)
        self.next_slide()

        # ── Block 1: Intuición ────────────────────────────────────────────────
        intuition_label = Text("Propiedad fundamental", font_size=28, color=BLUE)
        intuition_label.next_to(title, DOWN, buff=0.4)

        bullets = VGroup(
            MathTex(r"\bullet\ \text{Propiedad fundamental de los sistemas de control}", font_size=24),
            MathTex(r"\bullet\ \text{Evolución de estados }\textbf{acotada}\text{ y }\textbf{predecible}", font_size=24),
            MathTex(r"\bullet\ \text{Permite diseñar estrategias de control efectivas}", font_size=24),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        bullets.next_to(intuition_label, DOWN, buff=0.4)

        intuition_box = RoundedRectangle(
            corner_radius=0.2,
            width=bullets.width + 0.8,
            height=bullets.height + 0.5,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        intuition_box.move_to(bullets)

        self.play(FadeIn(intuition_label), FadeIn(intuition_box), FadeIn(bullets))
        self.wait(0.5)
        self.next_slide()

        self.play(FadeOut(intuition_label), FadeOut(intuition_box), FadeOut(bullets))
        self.wait(0.3)

        # ── Block 2: Definiciones matemáticas ────────────────────────────────
        defs_label = Text("Definiciones de estabilidad", font_size=28, color=BLUE)
        defs_label.next_to(title, DOWN, buff=0.4)

        lyapunov = MathTex(
            r"\textbf{Liapunov:}\;"
            r"\|\mathbf{x}_0-\mathbf{x}^{*}\|\leq\delta"
            r"\;\Rightarrow\;"
            r"\|\mathbf{x}(t;\mathbf{x}_0)-\mathbf{x}^{*}\|\leq\epsilon"
            r"\;\forall t\geq 0",
            font_size=22,
        )
        asymptotic = MathTex(
            r"\textbf{Asintótica:}\;"
            r"\lim_{t\to\infty}\|\mathbf{x}(t;\mathbf{x}_0)-\mathbf{x}^{*}\|=0",
            font_size=22,
        )
        exponential = MathTex(
            r"\textbf{Exponencial:}\;"
            r"\|\mathbf{x}(t;\mathbf{x}_0)-\mathbf{x}^{*}\|\leq c\,e^{-\rho t}\|\mathbf{x}_0-\mathbf{x}^{*}\|",
            font_size=22,
        )

        defs_group = VGroup(lyapunov, asymptotic, exponential).arrange(
            DOWN, buff=0.35, aligned_edge=LEFT
        )
        defs_group.next_to(defs_label, DOWN, buff=0.4)

        for mob in defs_group:
            if mob.width > config.frame_width - 1.6:
                mob.scale_to_fit_width(config.frame_width - 1.6)

        defs_box = RoundedRectangle(
            corner_radius=0.2,
            width=defs_group.width + 0.8,
            height=defs_group.height + 0.5,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        defs_box.move_to(defs_group)

        self.play(FadeIn(defs_label), FadeIn(defs_box), FadeIn(defs_group))
        self.wait(0.5)
        self.next_slide()

        self.play(FadeOut(defs_label), FadeOut(defs_box), FadeOut(defs_group))
        self.wait(0.3)

        # ── Block 3: Problema de estabilización ──────────────────────────────
        stab_label = Text("Estabilización por retroalimentación", font_size=28, color=BLUE)
        stab_label.next_to(title, DOWN, buff=0.4)

        open_loop_eq = MathTex(
            r"\dot{\mathbf{x}}(t)=\mathbf{A}\mathbf{x}(t)+\mathbf{B}\mathbf{u}(t)",
            font_size=28,
        )
        feedback_eq = MathTex(
            r"\mathbf{u}(t)=\mathbf{K}\mathbf{x}(t),\quad\mathbf{K}\in\mathbb{R}^{n_u\times n_x}",
            font_size=28,
        )
        gain_note = MathTex(
            r"\mathbf{K}:\ \textbf{ganancia de retroalimentación}",
            font_size=22,
            color=GRAY_A,
        )
        closed_loop_eq = MathTex(
            r"\dot{\mathbf{x}}(t)=(\mathbf{A}+\mathbf{B}\mathbf{K})\mathbf{x}(t)",
            font_size=28,
        )
        goal_text = MathTex(
            r"\text{Objetivo: elegir }\mathbf{K}"
            r"\text{ para que }\mathbf{x}^{*}=\mathbf{0}"
            r"\text{ sea }\textbf{asintóticamente estable}",
            font_size=24,
        )

        stab_group = VGroup(
            open_loop_eq, feedback_eq, gain_note, closed_loop_eq, goal_text
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        stab_group.next_to(stab_label, DOWN, buff=0.35)

        for mob in stab_group:
            if mob.width > config.frame_width - 1.6:
                mob.scale_to_fit_width(config.frame_width - 1.6)

        stab_box = RoundedRectangle(
            corner_radius=0.2,
            width=stab_group.width + 0.8,
            height=stab_group.height + 0.5,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        stab_box.move_to(stab_group)

        self.play(FadeIn(stab_label), FadeIn(stab_box))
        self.play(FadeIn(open_loop_eq))
        self.play(FadeIn(feedback_eq), FadeIn(gain_note))
        self.play(FadeIn(closed_loop_eq))
        self.play(FadeIn(goal_text))
        self.wait(0.5)
        self.next_slide()

        self.play(
            FadeOut(stab_label), FadeOut(stab_box),
            FadeOut(open_loop_eq), FadeOut(feedback_eq),
            FadeOut(gain_note), FadeOut(closed_loop_eq), FadeOut(goal_text),
        )
        self.wait(0.3)

        # ── Block 4: Polos y teorema de asignación ───────────────────────────
        poles_label = Text("Polos y teorema de asignación", font_size=28, color=BLUE)
        poles_label.next_to(title, DOWN, buff=0.4)

        poles_lines = VGroup(
            MathTex(
                r"\bullet\ \mathbf{A}+\mathbf{B}\mathbf{K}"
                r"\text{ determina la dinámica de circuito cerrado}",
                font_size=24,
            ),
            MathTex(
                r"\bullet\ \text{Sus valores propios son los }\textbf{polos}\text{ del sistema}",
                font_size=24,
            ),
            MathTex(
                r"\bullet\ \mathrm{Re}(\lambda_i)<0\ \forall i"
                r"\;\Leftrightarrow\;\text{estabilidad asintótica}",
                font_size=24,
            ),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)

        theorem_eq = MathTex(
            r"\text{Polos asignables arbitrariamente}"
            r"\;\Leftrightarrow\;"
            r"(\mathbf{A},\mathbf{B})\ \textbf{controlable}",
            font_size=26,
            color=YELLOW,
        )
        if theorem_eq.width > config.frame_width - 1.6:
            theorem_eq.scale_to_fit_width(config.frame_width - 1.6)

        poles_content = VGroup(poles_lines, theorem_eq).arrange(
            DOWN, buff=0.5, aligned_edge=LEFT
        )
        poles_content.next_to(poles_label, DOWN, buff=0.4)

        poles_box = RoundedRectangle(
            corner_radius=0.2,
            width=poles_content.width + 0.8,
            height=poles_content.height + 0.5,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        poles_box.move_to(poles_content)

        self.play(FadeIn(poles_label), FadeIn(poles_box), FadeIn(poles_lines))
        self.wait(0.5)
        self.next_slide()

        self.play(FadeIn(theorem_eq))
        self.wait(0.5)
        self.next_slide()
