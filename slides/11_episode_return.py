"""
Episode, Return, Policy, and Value Functions slides.

Scene: EpisodeReturnSlide - Trajectory, episode, episodic vs continuous, return

Example:
    uv run manim-slides render slides/11_policy_value.py EpisodeReturnSlide
"""

from manim import *
from manim_slides import Slide

class EpisodeReturnSlide(Slide):
    """Covers trajectory, episode, episodic vs continuous tasks, and return."""

    def construct(self):
        # === TITLE ===
        title = Text("Episodio y retorno esperado", font_size=42, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))
        self.wait(0.5)
        self.next_slide()

        # === TRAYECTORIA ===
        trayectoria_label = Text("Trayectoria", font_size=32, color=BLUE)
        trayectoria_eq = MathTex(
            r"\boldsymbol{\tau} = \{x_0, u_0, r_1, x_1, u_1, \cdots, x_{t-1}, u_{t-1}, r_{t-1}, x_t\}",
            font_size=30,
        )
        trayectoria_desc = Text(
            "Secuencia de estados, acciones y recompensas",
            font_size=22,
            color=GRAY_B,
        )
        trayectoria_group = VGroup(trayectoria_label, trayectoria_eq, trayectoria_desc).arrange(
            DOWN, buff=0.25
        )
        trayectoria_group.move_to(UP * 0.8)

        trayectoria_box = RoundedRectangle(
            corner_radius=0.2,
            width=trayectoria_group.width + 0.8,
            height=trayectoria_group.height + 0.5,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        trayectoria_box.move_to(trayectoria_group)

        self.play(FadeIn(trayectoria_box), FadeIn(trayectoria_group))
        self.wait(0.5)
        self.next_slide()

        # === EPISODIO ===
        episodio_label = Text("Episodio", font_size=32, color=BLUE)
        episodio_eq = MathTex(
            r"\mathbf{E} = \{x_0, u_0, r_1, x_1, u_1, \cdots, x_{T-1}, u_{T-1}, r_{T}, x_{T}\}",
            font_size=30,
        )
        episodio_desc = Text(
            "Trayectoria completa desde estado inicial hasta terminal",
            font_size=22,
            color=GRAY_B,
        )
        episodio_group = VGroup(episodio_label, episodio_eq, episodio_desc).arrange(
            DOWN, buff=0.25
        )
        episodio_group.next_to(trayectoria_box, DOWN, buff=0.5)

        episodio_box = RoundedRectangle(
            corner_radius=0.2,
            width=episodio_group.width + 0.8,
            height=episodio_group.height + 0.5,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        episodio_box.move_to(episodio_group)

        self.play(FadeIn(episodio_box), FadeIn(episodio_group))
        self.wait(0.5)
        self.next_slide()

        # Clear trajectory and episode
        self.play(
            FadeOut(trayectoria_box),
            FadeOut(trayectoria_group),
            FadeOut(episodio_box),
            FadeOut(episodio_group),
        )
        self.wait(0.3)

        # === EPISODIC VS CONTINUOUS TASKS ===
        comparison_title = Text("Tareas episódicas vs continuas", font_size=30, color=BLUE)
        comparison_title.move_to(UP * 2)

        # Episodic side
        episodic_label = Text("Episódicas", font_size=26, color=GREEN)
        episodic_items = VGroup(
            Text("• Horizonte finito (T < ∞)", font_size=20, color=WHITE),
            Text("• Estado terminal definido", font_size=20, color=WHITE),
            Text("• Ej: partida de ajedrez", font_size=20, color=GRAY_B),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        episodic_group = VGroup(episodic_label, episodic_items).arrange(DOWN, buff=0.3)
        episodic_group.move_to(LEFT * 3)

        episodic_box = RoundedRectangle(
            corner_radius=0.2,
            width=episodic_group.width + 0.6,
            height=episodic_group.height + 0.5,
            color=GREEN,
            fill_opacity=0.1,
            stroke_width=1,
        )
        episodic_box.move_to(episodic_group)

        # Continuous side
        continuous_label = Text("Continuas", font_size=26, color=ORANGE)
        continuous_items = VGroup(
            Text("• Horizonte infinito (T → ∞)", font_size=20, color=WHITE),
            Text("• Sin estado terminal", font_size=20, color=WHITE),
            Text("• Ej: control de cuadricóptero", font_size=20, color=GRAY_B),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        continuous_group = VGroup(continuous_label, continuous_items).arrange(DOWN, buff=0.3)
        continuous_group.move_to(RIGHT * 3)

        continuous_box = RoundedRectangle(
            corner_radius=0.2,
            width=continuous_group.width + 0.6,
            height=continuous_group.height + 0.5,
            color=ORANGE,
            fill_opacity=0.1,
            stroke_width=1,
        )
        continuous_box.move_to(continuous_group)

        self.play(FadeIn(comparison_title))
        self.wait(0.3)
        self.play(
            FadeIn(episodic_box),
            FadeIn(episodic_group),
            FadeIn(continuous_box),
            FadeIn(continuous_group),
        )
        self.wait(0.5)
        self.next_slide()

        # Clear comparison
        self.play(
            FadeOut(comparison_title),
            FadeOut(episodic_box),
            FadeOut(episodic_group),
            FadeOut(continuous_box),
            FadeOut(continuous_group),
        )
        self.wait(0.3)

        # === RETORNO (RETURN) ===
        retorno_label = Text("Retorno", font_size=32, color=BLUE)
        retorno_eq = MathTex(
            r"G_t = R_{t+1} + R_{t+2} + \cdots + R_{T}",
            font_size=36,
        )
        retorno_group = VGroup(retorno_label, retorno_eq).arrange(DOWN, buff=0.3)
        retorno_group.move_to(UP * 0.5)

        # Box for retorno
        retorno_box = RoundedRectangle(
            corner_radius=0.2,
            width=retorno_group.width + 1,
            height=retorno_group.height + 0.6,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        retorno_box.move_to(retorno_group)

        self.play(FadeIn(retorno_box), FadeIn(retorno_group))
        self.wait(0.5)
        self.next_slide()

        # Description of return
        description = Text(
            "El total de recompensas que el agente espera\nrecibir a partir del tiempo t en adelante",
            font_size=24,
            color=GRAY_B,
        )
        description.next_to(retorno_box, DOWN, buff=0.5)

        self.play(FadeIn(description))
        self.wait(0.5)
        self.next_slide()

        # Problem: infinite sum is unstable
        problem_text = MathTex(
            r"\text{Si } T \rightarrow \infty \text{ la suma se vuelve numéricamente inestable}",
            font_size=28,
            color=RED_C,
        )
        problem_text.next_to(retorno_box, DOWN, buff=0.5)

        self.play(FadeOut(description), FadeIn(problem_text))
        self.wait(0.5)
        self.next_slide()

        # Fade out problem and retorno box
        self.play(FadeOut(problem_text), FadeOut(retorno_box), FadeOut(retorno_group))
        self.wait(0.3)

        # === DISCOUNTED RETURN ===
        discount_label = Text("Retorno con tasa de descuento", font_size=32, color=BLUE)
        discount_eq = MathTex(
            r"G_{t} = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots = \sum_{k=0}^{\infty} \gamma^{k} R_{t+k+1}",
            font_size=32,
        )
        gamma_constraint = MathTex(r"\gamma \in [0, 1)", font_size=28, color=YELLOW)

        discount_group = VGroup(discount_label, discount_eq, gamma_constraint).arrange(
            DOWN, buff=0.3
        )
        discount_group.move_to(UP * 0.3)

        # Box for discounted return
        discount_box = RoundedRectangle(
            corner_radius=0.2,
            width=discount_group.width + 0.8,
            height=discount_group.height + 0.6,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        discount_box.move_to(discount_group)

        self.play(FadeIn(discount_box), FadeIn(discount_group))
        self.wait(0.5)
        self.next_slide()

        # Highlight convergence
        convergence_text = Text(
            "La suma converge para cualquier secuencia acotada de recompensas",
            font_size=24,
            color=GREEN,
        )
        convergence_text.next_to(discount_box, DOWN, buff=0.5)

        self.play(FadeIn(convergence_text))
        self.wait(0.5)
        self.next_slide()

        # Fade out convergence note
        self.play(FadeOut(convergence_text))
        self.wait(0.3)

        # === OBJECTIVE STATEMENT (shown with discounted return) ===
        # Robot head icon
        robot_head = RoundedRectangle(
            corner_radius=0.15,
            width=0.8,
            height=0.9,
            color=BLUE_C,
            fill_opacity=0.8,
            stroke_width=2,
        )
        # Eyes
        left_eye = Circle(radius=0.12, color=WHITE, fill_opacity=1, stroke_width=0)
        right_eye = Circle(radius=0.12, color=WHITE, fill_opacity=1, stroke_width=0)
        left_pupil = Circle(radius=0.05, color=BLACK, fill_opacity=1, stroke_width=0)
        right_pupil = Circle(radius=0.05, color=BLACK, fill_opacity=1, stroke_width=0)
        left_eye.move_to(robot_head.get_center() + UP * 0.15 + LEFT * 0.2)
        right_eye.move_to(robot_head.get_center() + UP * 0.15 + RIGHT * 0.2)
        left_pupil.move_to(left_eye.get_center())
        right_pupil.move_to(right_eye.get_center())
        # Mouth
        mouth = RoundedRectangle(
            corner_radius=0.05,
            width=0.4,
            height=0.12,
            color=WHITE,
            fill_opacity=1,
            stroke_width=0,
        )
        mouth.move_to(robot_head.get_center() + DOWN * 0.2)
        # Antenna
        antenna_base = Rectangle(
            width=0.08, height=0.15, color=GRAY, fill_opacity=1, stroke_width=0
        )
        antenna_tip = Circle(radius=0.08, color=RED, fill_opacity=1, stroke_width=0)
        antenna_base.next_to(robot_head, UP, buff=0)
        antenna_tip.next_to(antenna_base, UP, buff=0)

        robot = VGroup(
            robot_head,
            left_eye,
            right_eye,
            left_pupil,
            right_pupil,
            mouth,
            antenna_base,
            antenna_tip,
        )
        robot.scale(0.7)

        objective = Text(
            "Mi objetivo es actuar de forma que las recompensas\na largo plazo sean lo más satisfactorias posible",
            font_size=22,
            color=WHITE,
            line_spacing=1.3,
        )

        objective_content = VGroup(robot, objective).arrange(RIGHT, buff=0.4)
        objective_content.next_to(discount_box, DOWN, buff=0.5)

        objective_box = RoundedRectangle(
            corner_radius=0.2,
            width=objective_content.width + 0.8,
            height=objective_content.height + 0.5,
            color=YELLOW,
            fill_opacity=0.1,
            stroke_width=2,
        )
        objective_box.move_to(objective_content)

        self.play(FadeIn(objective_box), FadeIn(objective_content))
        self.wait(0.5)
        self.next_slide()

        # Fade out both objective and discounted return before recursive formulation
        self.play(
            FadeOut(objective_box),
            FadeOut(objective_content),
            FadeOut(discount_box),
            FadeOut(discount_group),
        )
        self.wait(0.3)

        # === RECURSIVE FORMULATION ===
        recursive_eq = MathTex(
            r"G_t = R_{t+1} + \gamma G_{t+1}",
            font_size=36,
        )
        recursive_label = Text("Forma recursiva", font_size=28, color=BLUE)
        recursive_group = VGroup(recursive_label, recursive_eq).arrange(DOWN, buff=0.3)
        recursive_group.move_to(UP * 0.3)

        recursive_box = RoundedRectangle(
            corner_radius=0.2,
            width=recursive_group.width + 1.5,
            height=recursive_group.height + 0.6,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        recursive_box.move_to(recursive_group)

        self.play(FadeIn(recursive_box), FadeIn(recursive_group))
        self.wait(0.5)
        self.next_slide()

        # Balance explanation
        balance_text = Text(
            "γ permite hacer un balance entre\noptimizar recompensas inmediatas y futuras",
            font_size=24,
            color=GRAY_B,
            line_spacing=1.2,
        )
        balance_text.next_to(recursive_box, DOWN, buff=0.5)

        self.play(FadeIn(balance_text))
        self.wait(0.5)
        self.next_slide()

        # Final wait
        self.wait(1)

