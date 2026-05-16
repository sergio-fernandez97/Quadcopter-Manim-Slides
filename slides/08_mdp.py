"""
Slide 08 — Proceso de decisión de Márkov (MDP).

Narrative flow:
    1. RL intro block: definition box + agent-environment diagram.
    2. MDP derivation: full history → Markov property → compact notation → trajectory.
    3. Robot de reciclaje example: problem setup → graph built in layers → traversals.
    4. RL framework closer: agent-environment loop diagram alongside the graph.
"""

from manim import *
from manim_slides import Slide


# ---------------------------------------------------------------------------
# Color constants
# ---------------------------------------------------------------------------
STATE_COLOR = YELLOW
ACTION_COLOR = BLUE
PROB_COLOR = LIGHT_GREY
REWARD_POS_COLOR = GREEN
REWARD_NEG_COLOR = RED
SUBDUED_OPACITY = 0.2


def _transition_label(prob_tex: str, reward_tex: str, reward_negative: bool = False) -> MathTex:
    """Return a small MathTex label with colored probability and reward parts."""
    label = MathTex(prob_tex, ",", reward_tex, font_size=22)
    label[0].set_color(PROB_COLOR)
    label[1].set_color(WHITE)
    label[2].set_color(REWARD_NEG_COLOR if reward_negative else REWARD_POS_COLOR)
    return label


class MdpSlide(Slide):
    """
    Manim-slides scene covering Markov Decision Processes.

    Sections
    --------
    - Aprendizaje por refuerzo: brief RL definition + agent-environment loop.
    - Proceso de decisión de Márkov: sequential derivation of MDP dynamics.
    - Robot de reciclaje: concrete example with animated graph traversals.
    - Closing: RL framework diagram alongside the recycling-robot graph.
    """

    def construct(self):  # noqa: PLR0915 — presentation method, length expected
        # ===================================================================
        # PERSISTENT TITLE
        # ===================================================================
        title = Text(
            "Proceso de Decisión de Márkov (MDP)",
            font_size=42,
            color=YELLOW,
        )
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))
        self.wait(0.5)
        self.next_slide()

        # ===================================================================
        # SECTION 1 — APRENDIZAJE POR REFUERZO (RL intro)
        # ===================================================================
        section_rl = Text("Aprendizaje por refuerzo", font_size=32, color=BLUE)
        section_rl.move_to(UP * 2.5)
        self.play(FadeIn(section_rl))
        self.wait(0.5)
        self.next_slide()

        # --- RL definition box ---
        rl_def_text = Text(
            "El aprendizaje por refuerzo es un paradigma en el que un agente\n"
            "interactúa con un entorno y aprende a tomar decisiones\n"
            "para maximizar recompensas acumuladas.",
            font_size=24,
            line_spacing=1.3,
        )
        rl_def_box = RoundedRectangle(
            corner_radius=0.2,
            width=10.5,
            height=2.4,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        rl_def_group = VGroup(rl_def_box, rl_def_text)
        rl_def_box.move_to(rl_def_text.get_center())
        rl_def_group.next_to(section_rl, DOWN, buff=0.5)
        self.play(FadeIn(rl_def_group))
        self.wait(0.5)
        self.next_slide()

        # --- Agent-environment diagram ---
        agent_box = Rectangle(width=2.2, height=1.0, color=YELLOW, stroke_width=2)
        agent_label = Text("Agente", font_size=26, color=YELLOW).move_to(agent_box)
        agent_group = VGroup(agent_box, agent_label)

        env_box = Rectangle(width=2.6, height=1.0, color=RED_C, stroke_width=2)
        env_label = Text("Entorno", font_size=26, color=RED_C).move_to(env_box)
        env_group = VGroup(env_box, env_label)

        diagram_group = VGroup(agent_group, env_group).arrange(DOWN, buff=1.2)
        diagram_group.move_to(DOWN * 0.3)
        self.play(FadeIn(agent_group), FadeIn(env_group))
        self.wait(0.5)
        self.next_slide()

        # state arrow: env -> agent (right side going up)
        state_arrow = Arrow(
            env_box.get_right() + UP * 0.2,
            agent_box.get_right() + DOWN * 0.2,
            buff=0.05,
            color=WHITE,
            stroke_width=2.5,
            tip_length=0.18,
        )
        state_label = MathTex(r"X_t", font_size=28, color=WHITE)
        state_label.next_to(state_arrow, RIGHT, buff=0.15)
        self.play(GrowArrow(state_arrow), FadeIn(state_label))
        self.wait(0.5)
        self.next_slide()

        # action arrow: agent -> env (left side going down)
        action_arrow = Arrow(
            agent_box.get_left() + DOWN * 0.2,
            env_box.get_left() + UP * 0.2,
            buff=0.05,
            color=WHITE,
            stroke_width=2.5,
            tip_length=0.18,
        )
        action_label = MathTex(r"U_t", font_size=28, color=WHITE)
        action_label.next_to(action_arrow, LEFT, buff=0.15)
        self.play(GrowArrow(action_arrow), FadeIn(action_label))
        self.wait(0.5)
        self.next_slide()

        # uppercase = random variables note
        rv_note = Text(
            "Mayúsculas = variables aleatorias",
            font_size=22,
            color=LIGHT_GREY,
        ).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(rv_note))
        self.wait(0.5)
        self.next_slide()

        # realizations
        realizations = MathTex(
            r"X_t = x, \qquad U_t = u",
            font_size=30,
        )
        realizations.next_to(rv_note, UP, buff=0.3)
        self.play(FadeIn(realizations))
        self.wait(0.5)
        self.next_slide()

        # Fade out entire RL intro block
        rl_intro_all = VGroup(
            section_rl, rl_def_group,
            agent_group, env_group,
            state_arrow, state_label,
            action_arrow, action_label,
            rv_note, realizations,
        )
        self.play(FadeOut(rl_intro_all))
        self.wait(0.3)

        # ===================================================================
        # SECTION 2 — PROCESO DE DECISIÓN DE MÁRKOV
        # ===================================================================
        section_mdp = Text("Proceso de decisión de Márkov", font_size=32, color=BLUE)
        section_mdp.move_to(UP * 2.5)
        self.play(FadeIn(section_mdp))
        self.wait(0.5)
        self.next_slide()

        # --- MDP Step 1: Full-history transition ---
        step1_eq = MathTex(
            r"\mathbb{P}\!\left[X_{t+1}=x_{t+1}\mid x_0,u_0,\ldots,x_t,u_t\right]",
            font_size=34,
        )
        step1_eq.set_width(min(step1_eq.width, 11.0))  # shrink if needed
        step1_label = Text(
            "el futuro puede depender de toda la historia",
            font_size=24,
            color=LIGHT_GREY,
        )
        step1_group = VGroup(step1_eq, step1_label).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        step1_group.move_to(ORIGIN)
        self.play(FadeIn(step1_group))
        self.wait(0.5)
        self.next_slide()
        self.play(FadeOut(step1_group))
        self.wait(0.3)

        # --- MDP Step 2: Markov property ---
        step2_line1 = MathTex(
            r"\mathbb{P}\!\left[X_{t+1}=x_{t+1}\mid X_t=x_t,U_t=u_t\right]",
            font_size=34,
        )
        step2_eq_sign = MathTex(r"=", font_size=34)
        step2_line2 = MathTex(
            r"\mathbb{P}\!\left[X_{t+1}=x_{t+1}\mid X_t=x_t,U_t=u_t,\ldots,X_0=x_0,U_0=u_0\right]",
            font_size=28,
        )
        step2_line2.set_width(min(step2_line2.width, 11.0))
        step2_label = Text(
            "el siguiente estado depende del presente, no de cómo se llegó ahí",
            font_size=24,
            color=LIGHT_GREY,
        )
        step2_math = VGroup(step2_line1, step2_eq_sign, step2_line2).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2
        )
        step2_group = VGroup(step2_math, step2_label).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        step2_group.move_to(ORIGIN)
        self.play(FadeIn(step2_group))
        self.wait(0.5)
        self.next_slide()
        self.play(FadeOut(step2_group))
        self.wait(0.3)

        # --- MDP Step 3: Compact notation ---
        step3_eq = MathTex(
            r"p(x_{t+1}\mid x_t,u_t):=\mathbb{P}\!\left[X_{t+1}=x_{t+1}\mid X_t=x_t,U_t=u_t\right]",
            font_size=34,
        )
        step3_eq.set_width(min(step3_eq.width, 11.5))
        step3_group = VGroup(step3_eq).move_to(ORIGIN)
        self.play(FadeIn(step3_group))
        self.wait(0.5)
        self.next_slide()
        self.play(FadeOut(step3_group))
        self.wait(0.3)

        # --- MDP Step 4: Initial state/action + sequential transitions + trajectory ---
        step4_init = MathTex(
            r"x_0 \in \mathcal{X}, \qquad u_0 \in \mathcal{U}(x_0)",
            font_size=34,
        )
        step4_seq = MathTex(
            r"p(x_1\mid x_0,u_0), \qquad p(x_2\mid x_1,u_1)",
            font_size=34,
        )
        step4_traj = MathTex(
            r"x_0 \xrightarrow{u_0} x_1 \xrightarrow{u_1} x_2 \xrightarrow{u_2} \cdots x_t \xrightarrow{u_t} \cdots",
            font_size=32,
        )
        step4_traj.set_width(min(step4_traj.width, 11.0))
        step4_group = VGroup(step4_init, step4_seq, step4_traj).arrange(
            DOWN, aligned_edge=LEFT, buff=0.45
        )
        step4_group.move_to(ORIGIN)
        self.play(FadeIn(step4_init))
        self.wait(0.3)
        self.play(FadeIn(step4_seq))
        self.wait(0.3)
        self.play(FadeIn(step4_traj))
        self.wait(0.5)
        self.next_slide()

        # Fade out MDP section label and math; keep visible for context
        self.play(FadeOut(section_mdp), FadeOut(step4_group))
        self.wait(0.3)

        # ===================================================================
        # SECTION 3 — ROBOT DE RECICLAJE
        # ===================================================================
        section_robot = Text("Robot de reciclaje", font_size=32, color=BLUE)
        section_robot.move_to(UP * 2.5)
        self.play(FadeIn(section_robot))
        self.wait(0.5)
        self.next_slide()

        # --- Problem setup ---
        problem_heading = Text("Planteamiento del problema", font_size=28, color=WHITE)
        problem_points = BulletedList(
            "El robot decide en cada paso: buscar latas, esperar o recargar.",
            "Estado de la batería: high o low.",
            "Recompensa proporcional al número de latas recolectadas.",
            font_size=23,
            buff=0.2,
        )
        problem_box = RoundedRectangle(
            corner_radius=0.2,
            width=10.5,
            height=2.6,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        problem_box.move_to(problem_points.get_center())
        problem_boxed = VGroup(problem_box, problem_points)
        problem_group = VGroup(problem_heading, problem_boxed).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35
        )
        problem_group.next_to(section_robot, DOWN, buff=0.5)
        self.play(FadeIn(problem_group))
        self.wait(0.5)
        self.next_slide()

        # --- MDP elements ---
        mdp_elements = MathTex(
            r"\mathcal{X}=\{\text{high},\text{low}\}",
            font_size=30,
        )
        mdp_actions = MathTex(
            r"\mathcal{U}(\text{high})=\{\text{search},\text{wait}\}, \qquad \mathcal{U}(\text{low})=\{\text{search},\text{wait},\text{recharge}\}",
            font_size=30,
        )
        mdp_rewards = MathTex(
            r"r_{\text{search}} > r_{\text{wait}} \geq 0",
            font_size=30,
        )
        mdp_elem_group = VGroup(mdp_elements, mdp_actions, mdp_rewards).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35
        )
        mdp_elem_group.move_to(problem_group.get_center())
        self.play(FadeOut(problem_group), FadeIn(mdp_elem_group))
        self.wait(0.5)
        self.next_slide()
        self.play(FadeOut(mdp_elem_group), FadeOut(section_robot))
        self.wait(0.3)

        # ===================================================================
        # GRAPH — built in layers, positioned RIGHT half
        # ===================================================================
        g_shift = RIGHT * 2.2 + DOWN * 0.2

        # Layer 1: state nodes
        high = Circle(radius=0.7, color=WHITE, stroke_width=2).shift(LEFT * 1.8 + UP * 0.5 + g_shift)
        high_text = Text("high", font_size=28, color=YELLOW).move_to(high)
        high_group = VGroup(high, high_text)

        low = Circle(radius=0.7, color=WHITE, stroke_width=2).shift(RIGHT * 1.8 + UP * 0.5 + g_shift)
        low_text = Text("low", font_size=28, color=YELLOW).move_to(low)
        low_group = VGroup(low, low_text)

        # Layer 2: action nodes
        wait_top = Circle(radius=0.18, color=WHITE, fill_opacity=1, fill_color=BLUE).shift(
            LEFT * 1.8 + UP * 2.5 + g_shift
        )
        wait_top_text = Text("wait", font_size=16).next_to(wait_top, LEFT, buff=0.18)
        wait_top_group = VGroup(wait_top, wait_top_text)

        search_top = Circle(radius=0.18, color=WHITE, fill_opacity=1, fill_color=BLUE).shift(
            RIGHT * 1.8 + UP * 2.5 + g_shift
        )
        search_top_text = Text("search", font_size=16).next_to(search_top, RIGHT, buff=0.18)
        search_top_group = VGroup(search_top, search_top_text)

        search_bottom = Circle(radius=0.18, color=WHITE, fill_opacity=1, fill_color=BLUE).shift(
            LEFT * 1.8 + DOWN * 2.0 + g_shift
        )
        search_bottom_text = Text("search", font_size=16).next_to(search_bottom, LEFT, buff=0.18)
        search_bottom_group = VGroup(search_bottom, search_bottom_text)

        wait_bottom = Circle(radius=0.18, color=WHITE, fill_opacity=1, fill_color=BLUE).shift(
            RIGHT * 1.8 + DOWN * 2.0 + g_shift
        )
        wait_bottom_text = Text("wait", font_size=16).next_to(wait_bottom, RIGHT, buff=0.18)
        wait_bottom_group = VGroup(wait_bottom, wait_bottom_text)

        recharge = Circle(radius=0.18, color=WHITE, fill_opacity=1, fill_color=BLUE).move_to(
            ORIGIN + g_shift
        )
        recharge_text = Text("recharge", font_size=16).next_to(recharge, UP, buff=0.18)
        recharge_group = VGroup(recharge, recharge_text)

        # Legend labels
        estados_label = Text("estados", font_size=22, color=YELLOW).move_to(
            LEFT * 6.2 + UP * 2.2
        )
        acciones_label = Text("acciones", font_size=20, color=BLUE).move_to(
            LEFT * 6.2 + UP * 0.6
        )
        prob_legend = Text(
            "prob. transición", font_size=20, color=LIGHT_GREY
        ).move_to(LEFT * 5.8 + DOWN * 0.8)
        rewards_prefix = Text("recompensas ( ", font_size=20, color=WHITE)
        rewards_plus = Text("+", font_size=20, color=GREEN)
        rewards_comma = Text(", ", font_size=20, color=WHITE)
        rewards_minus = Text("-", font_size=20, color=RED)
        rewards_suffix = Text(" )", font_size=20, color=WHITE)
        rewards_legend = VGroup(
            rewards_prefix, rewards_plus, rewards_comma, rewards_minus, rewards_suffix
        ).arrange(RIGHT, buff=0.05).move_to(LEFT * 5.8 + DOWN * 1.6)

        # Layer 3: arrows
        # high <-> wait_top
        high_wait_top = Arrow(
            high.get_top() + LEFT * 0.25, wait_top.get_bottom(),
            color=WHITE, buff=0.05, stroke_width=2, tip_length=0.16,
        )
        wait_top_high = Arrow(
            wait_top.get_bottom() + RIGHT * 0.05, high.get_top() + RIGHT * 0.25,
            color=WHITE, buff=0.05, stroke_width=2, tip_length=0.16,
        )
        # low <-> search_top
        low_search_top = CurvedArrow(
            low.get_top() + RIGHT * 0.25, search_top.get_bottom(),
            angle=-0.3, color=WHITE, stroke_width=2, tip_length=0.16,
        )
        search_top_low = CurvedArrow(
            search_top.get_bottom() + LEFT * 0.05, low.get_top() + LEFT * 0.25,
            angle=-0.3, color=WHITE, stroke_width=2, tip_length=0.16,
        )
        # search_top <-> high
        search_top_high = CurvedArrow(
            search_top.get_left() + DOWN * 0.05, high.get_top() + RIGHT * 0.25,
            angle=0.3, color=WHITE, stroke_width=2, tip_length=0.16,
        )
        # low -> recharge -> high
        low_recharge = Arrow(
            low.get_left(), recharge.get_right(),
            color=WHITE, buff=0.1, stroke_width=2, tip_length=0.16,
        )
        recharge_high = Arrow(
            recharge.get_left(), high.get_right(),
            color=WHITE, buff=0.1, stroke_width=2, tip_length=0.16,
        )
        # high <-> search_bottom
        high_search_bottom = Arrow(
            high.get_bottom() + LEFT * 0.25, search_bottom.get_top(),
            color=WHITE, buff=0.05, stroke_width=2, tip_length=0.16,
        )
        search_bottom_high = Arrow(
            search_bottom.get_top() + RIGHT * 0.05, high.get_bottom() + RIGHT * 0.25,
            color=WHITE, buff=0.05, stroke_width=2, tip_length=0.16,
        )
        # search_bottom -> low
        search_bottom_low = CurvedArrow(
            search_bottom.get_right(), low.get_bottom() + LEFT * 0.25,
            angle=-0.5, color=WHITE, stroke_width=2, tip_length=0.16,
        )
        # low <-> wait_bottom
        low_wait_bottom = Arrow(
            low.get_bottom() + RIGHT * 0.25, wait_bottom.get_top(),
            color=WHITE, buff=0.05, stroke_width=2, tip_length=0.16,
        )
        wait_bottom_low = Arrow(
            wait_bottom.get_top() + LEFT * 0.05, low.get_bottom() + LEFT * 0.25,
            color=WHITE, buff=0.05, stroke_width=2, tip_length=0.16,
        )

        # Layer 4: probability and reward labels
        wait_top_label = _transition_label("1", r"r_{\text{wait}}").move_to(
            LEFT * 1.8 + UP * 3.3 + g_shift
        )
        search_top_label = _transition_label(r"\beta", r"r_{\text{search}}").move_to(
            RIGHT * 1.8 + UP * 3.3 + g_shift
        )
        search_top_low_label = _transition_label(r"1-\beta", "-3", reward_negative=True).move_to(
            RIGHT * 3.5 + UP * 1.4 + g_shift
        )
        low_high_label = _transition_label("1", "0").next_to(recharge, UP, buff=0.55)
        search_bottom_label = _transition_label(r"\alpha", r"r_{\text{search}}").move_to(
            LEFT * 1.8 + DOWN * 3.0 + g_shift
        )
        search_bottom_low_label = _transition_label(r"1-\alpha", r"r_{\text{search}}").move_to(
            RIGHT * 0.2 + DOWN * 2.2 + g_shift
        )
        wait_bottom_label = _transition_label("1", r"r_{\text{wait}}").move_to(
            RIGHT * 1.8 + DOWN * 3.0 + g_shift
        )

        # ---------------------------------------------------------------
        # Animate graph — layer by layer
        # ---------------------------------------------------------------
        # Layer 1: states
        self.play(
            Create(high_group),
            Create(low_group),
            FadeIn(estados_label),
        )
        self.wait(0.5)
        self.next_slide()

        # Layer 2: action nodes + legend
        self.play(
            Create(wait_top_group),
            Create(search_top_group),
            Create(search_bottom_group),
            Create(wait_bottom_group),
            Create(recharge_group),
            FadeIn(acciones_label),
        )
        self.wait(0.5)
        self.next_slide()

        # Layer 3: transitions
        self.play(
            Create(high_wait_top), Create(wait_top_high),
            Create(low_search_top), Create(search_top_low), Create(search_top_high),
            Create(low_recharge), Create(recharge_high),
            Create(high_search_bottom), Create(search_bottom_high), Create(search_bottom_low),
            Create(low_wait_bottom), Create(wait_bottom_low),
            FadeIn(prob_legend),
        )
        self.wait(0.5)
        self.next_slide()

        # Layer 4: prob + reward labels
        self.play(
            FadeIn(wait_top_label),
            FadeIn(search_top_label),
            FadeIn(search_top_low_label),
            FadeIn(low_high_label),
            FadeIn(search_bottom_label),
            FadeIn(search_bottom_low_label),
            FadeIn(wait_bottom_label),
            FadeIn(rewards_legend),
        )
        self.wait(0.5)
        self.next_slide()

        # ===================================================================
        # GRAPH TRAVERSALS
        # ===================================================================
        # Collect ALL graph mobjects for opacity control
        all_edges = [
            high_wait_top, wait_top_high,
            low_search_top, search_top_low, search_top_high,
            low_recharge, recharge_high,
            high_search_bottom, search_bottom_high, search_bottom_low,
            low_wait_bottom, wait_bottom_low,
        ]
        all_labels = [
            wait_top_label, search_top_label, search_top_low_label,
            low_high_label, search_bottom_label, search_bottom_low_label,
            wait_bottom_label,
        ]
        all_nodes = [
            high_group, low_group,
            wait_top_group, search_top_group,
            search_bottom_group, wait_bottom_group,
            recharge_group,
        ]

        def _attenuate(exclude_edges, exclude_nodes=None, exclude_labels=None):
            """Fade non-relevant elements to low opacity."""
            anims = []
            for e in all_edges:
                if e not in exclude_edges:
                    anims.append(e.animate.set_opacity(SUBDUED_OPACITY))
            for lbl in all_labels:
                if exclude_labels and lbl not in exclude_labels:
                    anims.append(lbl.animate.set_opacity(SUBDUED_OPACITY))
            if exclude_nodes:
                for n in all_nodes:
                    if n not in exclude_nodes:
                        anims.append(n.animate.set_opacity(SUBDUED_OPACITY))
            return anims

        def _restore():
            """Restore all elements to full opacity."""
            anims = []
            for e in all_edges:
                anims.append(e.animate.set_opacity(1.0))
            for lbl in all_labels:
                anims.append(lbl.animate.set_opacity(1.0))
            for n in all_nodes:
                anims.append(n.animate.set_opacity(1.0))
            return anims

        # Dot marker
        dot = Dot(color=RED, radius=0.15).move_to(high.get_center())
        self.play(FadeIn(dot))
        self.wait(0.3)

        # Traversal 1: high → search_bottom → high  (alpha probability)
        trav1_edges = [high_search_bottom, search_bottom_high]
        trav1_nodes = [high_group, search_bottom_group]
        trav1_labels = [search_bottom_label]
        self.play(*_attenuate(trav1_edges, trav1_nodes, trav1_labels), run_time=0.5)
        self.play(MoveAlongPath(dot, high_search_bottom.copy()), run_time=0.8)
        self.wait(0.2)
        self.play(MoveAlongPath(dot, search_bottom_high.copy()), run_time=0.8)
        self.wait(0.5)
        self.next_slide()

        # Traversal 2: high → search_bottom → low  (1-alpha probability)
        trav2_edges = [high_search_bottom, search_bottom_low]
        trav2_nodes = [high_group, search_bottom_group, low_group]
        trav2_labels = [search_bottom_label, search_bottom_low_label]
        self.play(*_restore(), run_time=0.4)
        dot.move_to(high.get_center())
        self.play(*_attenuate(trav2_edges, trav2_nodes, trav2_labels), run_time=0.5)
        self.play(MoveAlongPath(dot, high_search_bottom.copy()), run_time=0.8)
        self.wait(0.2)
        self.play(MoveAlongPath(dot, search_bottom_low.copy()), run_time=0.8)
        self.wait(0.5)
        self.next_slide()

        # Traversal 3: low → recharge → high
        trav3_edges = [low_recharge, recharge_high]
        trav3_nodes = [low_group, recharge_group, high_group]
        trav3_labels = [low_high_label]
        self.play(*_restore(), run_time=0.4)
        dot.move_to(low.get_center())
        self.play(*_attenuate(trav3_edges, trav3_nodes, trav3_labels), run_time=0.5)
        self.play(MoveAlongPath(dot, low_recharge.copy()), run_time=0.8)
        self.wait(0.2)
        self.play(MoveAlongPath(dot, recharge_high.copy()), run_time=0.8)
        self.wait(0.5)
        self.next_slide()

        # Restore full graph
        self.play(*_restore(), FadeOut(dot), run_time=0.4)
        self.wait(0.3)

        # ===================================================================
        # SECTION 4 — RL FRAMEWORK CLOSER
        # ===================================================================
        # Fade out math labels, keep graph structure visible on right
        self.play(
            FadeOut(wait_top_label), FadeOut(search_top_label),
            FadeOut(search_top_low_label), FadeOut(low_high_label),
            FadeOut(search_bottom_label), FadeOut(search_bottom_low_label),
            FadeOut(wait_bottom_label),
            FadeOut(estados_label), FadeOut(acciones_label),
            FadeOut(prob_legend), FadeOut(rewards_legend),
        )
        self.wait(0.3)

        # Shift graph to right side to make room for RL diagram
        graph_all = VGroup(
            high_group, low_group,
            wait_top_group, search_top_group, search_bottom_group,
            wait_bottom_group, recharge_group,
            high_wait_top, wait_top_high,
            low_search_top, search_top_low, search_top_high,
            low_recharge, recharge_high,
            high_search_bottom, search_bottom_high, search_bottom_low,
            low_wait_bottom, wait_bottom_low,
        )
        self.play(graph_all.animate.scale(0.72).to_edge(RIGHT, buff=0.4), run_time=0.8)
        self.wait(0.3)

        # RL framework diagram — LEFT side
        closer_agent_box = Rectangle(width=2.0, height=0.95, color=YELLOW, stroke_width=2)
        closer_agent_text = Text("Agente", font_size=24, color=YELLOW).move_to(closer_agent_box)
        closer_agent_group = VGroup(closer_agent_box, closer_agent_text)

        closer_env_box = Rectangle(width=2.4, height=0.95, color=RED_C, stroke_width=2)
        closer_env_text = Text("Entorno", font_size=24, color=RED_C).move_to(closer_env_box)
        closer_env_group = VGroup(closer_env_box, closer_env_text)

        closer_diagram = VGroup(closer_agent_group, closer_env_group).arrange(DOWN, buff=1.3)
        closer_diagram.move_to(LEFT * 3.8 + DOWN * 0.3)

        # estado arrow: env -> agent (right side)
        closer_state_arr = Arrow(
            closer_env_box.get_right() + UP * 0.2,
            closer_agent_box.get_right() + DOWN * 0.2,
            buff=0.05, color=WHITE, stroke_width=2, tip_length=0.16,
        )
        closer_state_lbl = MathTex(r"X_t", font_size=24).next_to(closer_state_arr, RIGHT, buff=0.12)

        # recompensa arrow: env -> agent (further right)
        closer_reward_arr = Arrow(
            closer_env_box.get_right() + DOWN * 0.2,
            closer_agent_box.get_right() + DOWN * 0.38,
            buff=0.05, color=GREEN, stroke_width=2, tip_length=0.16,
        )
        closer_reward_lbl = MathTex(r"R_t", font_size=24, color=GREEN).next_to(
            closer_reward_arr, RIGHT, buff=0.12
        )

        # acción arrow: agent -> env (left side)
        closer_action_arr = Arrow(
            closer_agent_box.get_left() + DOWN * 0.2,
            closer_env_box.get_left() + UP * 0.2,
            buff=0.05, color=WHITE, stroke_width=2, tip_length=0.16,
        )
        closer_action_lbl = MathTex(r"U_t", font_size=24).next_to(
            closer_action_arr, LEFT, buff=0.12
        )

        closer_group = VGroup(
            closer_agent_group, closer_env_group,
            closer_state_arr, closer_state_lbl,
            closer_reward_arr, closer_reward_lbl,
            closer_action_arr, closer_action_lbl,
        )

        self.play(FadeIn(closer_group))
        self.wait(0.5)
        self.next_slide()
