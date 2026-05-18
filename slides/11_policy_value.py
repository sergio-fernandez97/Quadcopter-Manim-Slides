"""
Episode, Return, Policy, and Value Functions slides.

Scene: EpisodeReturnSlide - Trajectory, episode, episodic vs continuous, return

Example:
    uv run manim-slides render slides/11_policy_value.py EpisodeReturnSlide
"""

from manim import *
from manim_slides import Slide


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
