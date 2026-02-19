"""
Episode, Return, Policy, and Value Functions slides.

Scene 1: EpisodeReturnSlide - Trajectory, episode, episodic vs continuous, return
Scene 2: PolicyValueSlide - Policy, value functions, optimal policy, Q*

Example:
    uv run manim-slides render slides/11_policy_value.py EpisodeReturnSlide
    uv run manim-slides render slides/11_policy_value.py PolicyValueSlide
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


class PolicyValueSlide(Slide):
    """Covers policy, value functions, optimal policy, Q*, and greedy policy."""

    def construct(self):
        # === TITLE ===
        title = Text("Política y funciones de valor", font_size=42, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))
        self.wait(0.5)
        self.next_slide()

        # === PROBABILISTIC POLICY ===
        policy_label = Text("Política", font_size=32, color=BLUE)
        policy_mapping = MathTex(
            r"\pi: \mathcal{S} \rightarrow \mathcal{P}(\mathcal{A})",
            font_size=34,
        )
        policy_desc = Text(
            "Función de densidad de una distribución\nde las acciones dado el estado",
            font_size=22,
            color=GRAY_B,
            line_spacing=1.2,
        )
        policy_eq = MathTex(
            r"\pi(u|x) = \mathbb{P}\left[U_t = u \,|\, X_t = x\right]",
            font_size=34,
        )

        policy_group = VGroup(policy_label, policy_mapping, policy_desc, policy_eq).arrange(
            DOWN, buff=0.3
        )
        policy_group.move_to(UP * 0.5)

        policy_box = RoundedRectangle(
            corner_radius=0.2,
            width=policy_group.width + 1,
            height=policy_group.height + 0.6,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        policy_box.move_to(policy_group)

        self.play(FadeIn(policy_box), FadeIn(policy_group))
        self.wait(0.5)
        self.next_slide()

        # Policy behavior label
        policy_behavior = Text(
            "La política determina el comportamiento del agente",
            font_size=24,
            color=YELLOW,
        )
        policy_behavior.next_to(policy_box, DOWN, buff=0.5)

        self.play(FadeIn(policy_behavior))
        self.wait(0.5)
        self.next_slide()

        # Clear policy section
        self.play(
            FadeOut(policy_box),
            FadeOut(policy_group),
            FadeOut(policy_behavior),
        )
        self.wait(0.3)

        # === VALUE FUNCTIONS ===
        # V_π on the left
        v_label = Text("Función de valor", font_size=26, color=GREEN)
        v_eq = MathTex(
            r"V_{\pi}(x) = \mathbb{E}_{\pi}\left[G_t \,|\, X_t = x\right]",
            font_size=30,
        )
        v_group = VGroup(v_label, v_eq).arrange(DOWN, buff=0.25)

        v_box = RoundedRectangle(
            corner_radius=0.2,
            width=v_group.width + 0.6,
            height=v_group.height + 0.5,
            color=GREEN,
            fill_opacity=0.1,
            stroke_width=1,
        )
        v_box.move_to(v_group)
        v_complete = VGroup(v_box, v_group)
        v_complete.move_to(LEFT * 3.2 + UP * 1.5)

        # Q_π on the right
        q_label = Text("Función de valor estado-acción", font_size=26, color=ORANGE)
        q_eq = MathTex(
            r"Q_{\pi}(x, u) = \mathbb{E}_{\pi}\left[G_t \,|\, X_t = x, U_t = u\right]",
            font_size=30,
        )
        q_group = VGroup(q_label, q_eq).arrange(DOWN, buff=0.25)

        q_box = RoundedRectangle(
            corner_radius=0.2,
            width=q_group.width + 0.6,
            height=q_group.height + 0.5,
            color=ORANGE,
            fill_opacity=0.1,
            stroke_width=1,
        )
        q_box.move_to(q_group)
        q_complete = VGroup(q_box, q_group)
        q_complete.move_to(RIGHT * 3.2 + UP * 1.5)

        self.play(FadeIn(v_complete), FadeIn(q_complete))
        self.wait(0.5)
        self.next_slide()

        # Descriptive label for value functions
        value_desc = Text(
            "La función de valor mide qué tan bueno es un estado o una acción\n en términos de recompensa futura esperada.",
            font_size=24,
            color=GRAY_B,
            line_spacing=1.2,
        )
        value_desc.move_to(DOWN * 0.3)

        value_desc_box = RoundedRectangle(
            corner_radius=0.2,
            width=value_desc.width + 0.8,
            height=value_desc.height + 0.5,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        value_desc_box.move_to(value_desc)

        self.play(FadeIn(value_desc_box), FadeIn(value_desc))
        self.wait(0.5)
        self.next_slide()

        # Relationship equation with underbraces
        relation_eq = MathTex(
            r"\underbrace{\mathbb{E}_{\pi}[G_t|X_t=x]}_{V_{\pi}(x)}",
            r"=",
            r"\sum_{u \in \mathcal{U}(x)} \pi(u|x)",
            r"\underbrace{\mathbb{E}_{\pi}[G_t|X_t=x, U_t=u]}_{Q_{\pi}(x,u)}",
            font_size=28,
        )
        relation_eq.move_to(DOWN * 2.0)

        self.play(FadeIn(relation_eq))
        self.wait(0.5)
        self.next_slide()

        # Transform to simpler form
        simple_eq = MathTex(
            r"V_{\pi}(x) = \sum_{u \in \mathcal{U}(x)} \pi(u|x) \, Q_{\pi}(x, u)",
            font_size=34,
        )
        simple_eq.move_to(relation_eq)

        simple_box = RoundedRectangle(
            corner_radius=0.2,
            width=simple_eq.width + 0.8,
            height=simple_eq.height + 0.5,
            color=YELLOW,
            fill_opacity=0.1,
            stroke_width=2,
        )
        simple_box.move_to(simple_eq)

        self.play(
            Transform(relation_eq, simple_eq),
            FadeIn(simple_box),
        )
        self.wait(0.5)
        self.next_slide()

        # Clear description and relation, keep v_complete and q_complete
        self.play(
            FadeOut(value_desc_box),
            FadeOut(value_desc),
            FadeOut(relation_eq),
            FadeOut(simple_box),
        )
        self.wait(0.3)

        # === BELLMAN EQUATION DERIVATION ===
        # Change title to "Ecuación de Bellman"
        bellman_title = Text("Ecuación de Bellman", font_size=42, color=YELLOW)
        bellman_title.to_edge(UP, buff=0.5)

        self.play(Transform(title, bellman_title))
        self.wait(0.3)
        self.next_slide()

        # Move v_complete to center-left and make room for derivation
        v_new_pos = LEFT * 3.5 + UP * 2.2
        q_new_pos = RIGHT * 3.5 + UP * 2.2

        self.play(
            v_complete.animate.move_to(v_new_pos).scale(0.85),
            q_complete.animate.move_to(q_new_pos).scale(0.85),
        )
        self.wait(0.3)

        # === V_π BELLMAN DERIVATION ===
        # Step 1: V_π(x) = E_π[R_{t+1}|X_t=x] + γE_π[G_{t+1}|X_t=x]
        v_step1 = MathTex(
            r"V_{\pi}(x) = \mathbb{E}_{\pi}[R_{t+1}|X_t=x] + \gamma\mathbb{E}_{\pi}[G_{t+1}|X_t=x]",
            font_size=26,
        )
        v_step1.move_to(UP * 0.5)

        self.play(TransformMatchingShapes(v_eq.copy(), v_step1))
        self.wait(0.5)
        self.next_slide()

        # Step 2: Expand with policy and transition
        v_step2 = MathTex(
            r"= \sum_{u}\pi(u|x) \mathbb{E}_{\pi}[R_{t+1}|X_t=x, U_t=u] + \gamma \sum_{u}\pi(u|x)\sum_{x'}p(x'|x, u)",
            r"V_{\pi}(x')",
            font_size=24,
        )
        v_step2[1].set_color(YELLOW)
        v_step2.move_to(UP * 0.5)

        self.play(Transform(v_step1, v_step2))
        self.wait(0.5)
        self.next_slide()

        # Step 3: Final Bellman equation for V
        v_bellman = MathTex(
            r"V_{\pi}(x) = \sum_{u}\pi(u|x)\left[r(x,u) + \gamma \sum_{x'}p(x'|x,u)",
            r"V_{\pi}(x')",
            r"\right]",
            font_size=28,
        )
        v_bellman[1].set_color(YELLOW)
        v_bellman.move_to(UP * 0.5)

        v_bellman_box = RoundedRectangle(
            corner_radius=0.2,
            width=v_bellman.width + 0.6,
            height=v_bellman.height + 0.4,
            color=GREEN,
            fill_opacity=0.1,
            stroke_width=2,
        )
        v_bellman_box.move_to(v_bellman)

        self.play(Transform(v_step1, v_bellman), FadeIn(v_bellman_box))
        self.wait(0.5)
        self.next_slide()

        # === Q_π BELLMAN DERIVATION ===
        # Step 1: Q_π(x,u) = r(x,u) + γ Σ_{x'} p(x'|x,u) V_π(x')
        q_step1 = MathTex(
            r"Q_{\pi}(x, u) = r(x,u) + \gamma \sum_{x'}p(x'|x,u)",
            r"V_{\pi}(x')",
            font_size=28,
        )
        q_step1[1].set_color(YELLOW)
        q_step1.move_to(DOWN * 1.0)

        self.play(TransformMatchingShapes(q_eq.copy(), q_step1))
        self.wait(0.5)
        self.next_slide()

        # Step 2: Final Bellman equation for Q
        q_bellman = MathTex(
            r"Q_{\pi}(x, u) = r(x,u) + \gamma \sum_{x'}p(x'|x,u)\sum_{u'}\pi(u'|x')",
            r"Q_{\pi}(x', u')",
            font_size=26,
        )
        q_bellman[1].set_color(YELLOW)
        q_bellman.move_to(DOWN * 1.0)

        q_bellman_box = RoundedRectangle(
            corner_radius=0.2,
            width=q_bellman.width + 0.6,
            height=q_bellman.height + 0.4,
            color=ORANGE,
            fill_opacity=0.1,
            stroke_width=2,
        )
        q_bellman_box.move_to(q_bellman)

        self.play(Transform(q_step1, q_bellman), FadeIn(q_bellman_box))
        self.wait(0.5)
        self.next_slide()

        # Clear Bellman section
        self.play(
            FadeOut(v_complete),
            FadeOut(q_complete),
            FadeOut(v_step1),
            FadeOut(v_bellman_box),
            FadeOut(q_step1),
            FadeOut(q_bellman_box),
        )
        self.wait(0.3)

        # Restore title for next section
        original_title = Text("Política y funciones de valor", font_size=42, color=YELLOW)
        original_title.to_edge(UP, buff=0.5)
        self.play(Transform(title, original_title))
        self.wait(0.3)

        # === PARTIAL ORDERING PRINCIPLE ===
        ordering_label = Text("Principio de orden parcial", font_size=32, color=BLUE)
        ordering_eq = MathTex(
            r"\pi_1 \geq \pi_2 \quad \iff \quad V_{\pi_1}(x) \geq V_{\pi_2}(x) \quad \forall x \in \mathcal{X}",
            font_size=32,
        )
        ordering_group = VGroup(ordering_label, ordering_eq).arrange(DOWN, buff=0.3)
        ordering_group.move_to(UP * 0.5)

        ordering_box = RoundedRectangle(
            corner_radius=0.2,
            width=ordering_group.width + 0.8,
            height=ordering_group.height + 0.6,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        ordering_box.move_to(ordering_group)

        self.play(FadeIn(ordering_box), FadeIn(ordering_group))
        self.wait(0.5)
        self.next_slide()

        # === OPTIMAL POLICY ===
        optimal_label = Text("Política óptima", font_size=28, color=GREEN)
        optimal_eq = MathTex(r"\pi_{*} \quad\iff\quad V_{*}(x) = \max_{\pi}V_{\pi}(x)", font_size=36, color=GREEN)
        optimal_desc = Text(
            "La mejor política",
            font_size=24,
            color=GRAY_B,
        )
        optimal_group = VGroup(optimal_label, optimal_eq, optimal_desc).arrange(
            DOWN, buff=0.2
        )
        optimal_group.next_to(ordering_box, DOWN, buff=0.5)

        self.play(FadeIn(optimal_group))
        self.wait(0.5)
        self.next_slide()

        # Not unique warning
        not_unique = Text(
            "No está garantizado que sea única",
            font_size=22,
            color=RED_C,
        )
        not_unique.next_to(optimal_group, DOWN, buff=0.3)

        self.play(FadeIn(not_unique))
        self.wait(0.5)
        self.next_slide()

        # Clear for Q* section
        self.play(
            FadeOut(ordering_box),
            FadeOut(ordering_group),
            FadeOut(optimal_group),
            FadeOut(not_unique),
        )
        self.wait(0.3)

        # === OPTIMAL STATE-ACTION VALUE FUNCTION ===
        qstar_label = Text(
            "Función óptima de valor estado-acción", font_size=30, color=BLUE
        )
        qstar_eq = MathTex(
            r"Q_{*}(x, u) = \max_{\pi} Q_{\pi}(x, u)",
            font_size=34,
        )
        qstar_group = VGroup(qstar_label, qstar_eq).arrange(DOWN, buff=0.3)
        qstar_group.move_to(UP * 1.0)

        qstar_box = RoundedRectangle(
            corner_radius=0.2,
            width=qstar_group.width + 0.8,
            height=qstar_group.height + 0.6,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        qstar_box.move_to(qstar_group)

        self.play(FadeIn(qstar_box), FadeIn(qstar_group))
        self.wait(0.5)
        self.next_slide()

        # === GREEDY POLICY ===
        greedy_label = Text("Política voraz (greedy)", font_size=28, color=GREEN)
        greedy_eq = MathTex(
            r"\pi_{*}(u|x) = \begin{cases} 1 & \text{si } u = \arg\max_{u} Q_{*}(x, u) \\ 0 & \text{e.o.c} \end{cases}",
            font_size=30,
        )
        greedy_group = VGroup(greedy_label, greedy_eq).arrange(DOWN, buff=0.3)
        greedy_group.next_to(qstar_box, DOWN, buff=0.6)

        greedy_box = RoundedRectangle(
            corner_radius=0.2,
            width=greedy_group.width + 0.8,
            height=greedy_group.height + 0.6,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        greedy_box.move_to(greedy_group)

        self.play(FadeIn(greedy_box), FadeIn(greedy_group))
        self.wait(0.5)
        self.next_slide()

        # === DETERMINISTIC POLICY ===
        deterministic_label = Text("Política determinista", font_size=28, color=GREEN)
        deterministic_eq = MathTex(
            r"\mu_{*}(x) = \arg\max_{u} Q_{*}(x, u)",
            font_size=34,
        )
        deterministic_group = VGroup(deterministic_label, deterministic_eq).arrange(DOWN, buff=0.3)
        deterministic_group.move_to(greedy_group)

        deterministic_box = RoundedRectangle(
            corner_radius=0.2,
            width=deterministic_group.width + 0.8,
            height=deterministic_group.height + 0.6,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        deterministic_box.move_to(deterministic_group)

        self.play(
            Transform(greedy_box, deterministic_box),
            Transform(greedy_group, deterministic_group),
        )
        self.wait(0.5)
        self.next_slide()

        # Final wait
        self.wait(1)
