"""
Slide 08 — Proceso de decisión de Márkov (MDP).

Narrative flow:
    1. RL intro: "Aprendizaje por Refuerzo (RL)" title + definition box +
       framework-RL.jpeg (color-inverted).
    2. MDP derivation: full history → Markov property (centered) →
       compact notation → trajectory.
    3. Robot de reciclaje: problem setup → graph built in layers → traversals.

Example
-------
uv run manim-slides render slides/08_mdp.py MdpSlide
"""

import tempfile
from pathlib import Path

from manim import *
from manim_slides import Slide

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_FRAMEWORK_IMG = (
    Path(__file__).parent.parent
    / "LaTex/figures/03_aprendizaje_por_refuerzo/framework-RL.jpeg"
)

# ---------------------------------------------------------------------------
# Color constants
# ---------------------------------------------------------------------------
PROB_COLOR = LIGHT_GREY
REWARD_POS_COLOR = GREEN
REWARD_NEG_COLOR = RED
SUBDUED_OPACITY = 0.2


def _invert_image(path: Path) -> ImageMobject:
    """Load an image, invert colors (white bg → black bg), return ImageMobject."""
    from PIL import Image, ImageOps

    img = Image.open(path).convert("RGB")
    inverted = ImageOps.invert(img)
    tmp = tempfile.mktemp(suffix=".png")
    inverted.save(tmp)
    return ImageMobject(tmp)


def _transition_label(
    prob_tex: str, reward_tex: str, reward_negative: bool = False
) -> MathTex:
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
    - Aprendizaje por Refuerzo (RL): brief intro with inverted framework-RL.jpeg.
    - Proceso de Decisión de Márkov (MDP): sequential derivation of dynamics.
    - Robot de reciclaje: concrete example with animated graph traversals.

    Example
    -------
    uv run manim-slides render slides/08_mdp.py MdpSlide
    """

    def construct(self):  # noqa: PLR0915 — presentation method, length expected
        # ===================================================================
        # SECTION 1 — APRENDIZAJE POR REFUERZO (RL intro)
        # Title: "Aprendizaje por Refuerzo (RL)" — no MDP title yet
        # ===================================================================
        title = Text("Aprendizaje por Refuerzo (RL)", font_size=42, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))
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
        rl_def_box.move_to(rl_def_text.get_center())
        rl_def_group = VGroup(rl_def_box, rl_def_text)
        rl_def_group.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(rl_def_group))
        self.wait(0.5)
        self.next_slide()

        # --- RL framework image (color-inverted JPEG, below definition box) ---
        rl_image = _invert_image(_FRAMEWORK_IMG)
        # Constrain to at most 9 units wide and 3.0 units tall
        rl_image.scale_to_fit_width(9.0)
        if rl_image.height > 3.0:
            rl_image.scale_to_fit_height(3.0)
        rl_image.next_to(rl_def_group, DOWN, buff=0.4)
        self.play(FadeIn(rl_image))
        self.wait(0.5)
        self.next_slide()

        # ===================================================================
        # TRANSITION: swap title to MDP title, fade out RL intro content
        # ===================================================================
        mdp_title = Text(
            "Proceso de Decisión de Márkov (MDP)", font_size=42, color=YELLOW
        )
        mdp_title.to_edge(UP, buff=0.5)
        self.play(
            FadeOut(rl_def_group),
            FadeOut(rl_image),
            ReplacementTransform(title, mdp_title),
        )
        self.wait(0.3)

        # ===================================================================
        # SECTION 2 — PROCESO DE DECISIÓN DE MÁRKOV
        # Single title already visible; no separate section label.
        # ===================================================================

        # --- Step 1: Full-history transition ---
        step1_eq = MathTex(
            r"\mathbb{P}\!\left[X_{t+1}=x_{t+1}\mid x_0,u_0,\ldots,x_t,u_t\right]",
            font_size=34,
        )
        step1_eq.set_width(min(step1_eq.width, 11.0))
        step1_label = Text(
            "el futuro puede depender de toda la historia",
            font_size=24,
            color=LIGHT_GREY,
        )
        step1_group = VGroup(step1_eq, step1_label).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35
        )
        step1_group.move_to(ORIGIN)
        self.play(FadeIn(step1_group))
        self.wait(0.5)
        self.next_slide()
        self.play(FadeOut(step1_group))
        self.wait(0.3)

        # --- Step 2: Markov property — centered, with "propiedad de Márkov" label ---
        markov_label = Text("propiedad de Márkov", font_size=28, color=BLUE)
        markov_label.next_to(mdp_title, DOWN, buff=0.35)

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
        step2_desc = Text(
            "el siguiente estado depende del presente, no de cómo se llegó ahí",
            font_size=24,
            color=LIGHT_GREY,
        )
        step2_math = VGroup(step2_line1, step2_eq_sign, step2_line2).arrange(
            DOWN, buff=0.2
        )
        step2_group = VGroup(step2_math, step2_desc).arrange(DOWN, buff=0.45)
        step2_group.move_to(ORIGIN)
        self.play(FadeIn(markov_label), FadeIn(step2_group))
        self.wait(0.5)
        self.next_slide()
        self.play(FadeOut(markov_label), FadeOut(step2_group))
        self.wait(0.3)

        # --- Step 3: Compact notation ---
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

        # --- Step 4: Initial state/action + sequential transitions + trajectory ---
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
        self.play(FadeOut(step4_group))
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
            r"\mathcal{U}(\text{high})=\{\text{search},\text{wait}\},"
            r" \qquad \mathcal{U}(\text{low})=\{\text{search},\text{wait},\text{recharge}\}",
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
        # GRAPH — built in layers
        # ===================================================================
        g_shift = RIGHT * 2.2 + DOWN * 0.2

        # Layer 1: state nodes
        # fill_opacity=0 is explicit so set_stroke restore won't expose a white fill.
        high = Circle(
            radius=0.7, stroke_color=WHITE, stroke_width=2, fill_opacity=0
        ).shift(LEFT * 1.8 + UP * 0.5 + g_shift)
        high_text = Text("high", font_size=28, color=YELLOW).move_to(high)
        high_group = VGroup(high, high_text)

        low = Circle(
            radius=0.7, stroke_color=WHITE, stroke_width=2, fill_opacity=0
        ).shift(RIGHT * 1.8 + UP * 0.5 + g_shift)
        low_text = Text("low", font_size=28, color=YELLOW).move_to(low)
        low_group = VGroup(low, low_text)

        # Layer 2: action nodes (filled circles)
        wait_top = Circle(
            radius=0.18, color=WHITE, fill_opacity=1, fill_color=BLUE
        ).shift(LEFT * 1.8 + UP * 2.5 + g_shift)
        wait_top_text = Text("wait", font_size=16).next_to(wait_top, LEFT, buff=0.18)
        wait_top_group = VGroup(wait_top, wait_top_text)

        search_top = Circle(
            radius=0.18, color=WHITE, fill_opacity=1, fill_color=BLUE
        ).shift(RIGHT * 1.8 + UP * 2.5 + g_shift)
        search_top_text = Text("search", font_size=16).next_to(
            search_top, RIGHT, buff=0.18
        )
        search_top_group = VGroup(search_top, search_top_text)

        search_bottom = Circle(
            radius=0.18, color=WHITE, fill_opacity=1, fill_color=BLUE
        ).shift(LEFT * 1.8 + DOWN * 2.0 + g_shift)
        search_bottom_text = Text("search", font_size=16).next_to(
            search_bottom, LEFT, buff=0.18
        )
        search_bottom_group = VGroup(search_bottom, search_bottom_text)

        wait_bottom = Circle(
            radius=0.18, color=WHITE, fill_opacity=1, fill_color=BLUE
        ).shift(RIGHT * 1.8 + DOWN * 2.0 + g_shift)
        wait_bottom_text = Text("wait", font_size=16).next_to(
            wait_bottom, RIGHT, buff=0.18
        )
        wait_bottom_group = VGroup(wait_bottom, wait_bottom_text)

        recharge = Circle(
            radius=0.18, color=WHITE, fill_opacity=1, fill_color=BLUE
        ).move_to(ORIGIN + g_shift)
        recharge_text = Text("recharge", font_size=16).next_to(
            recharge, UP, buff=0.18
        )
        recharge_group = VGroup(recharge, recharge_text)

        # Legend
        estados_label = Text("estados", font_size=22, color=YELLOW).move_to(
            LEFT * 6.2 + UP * 2.2
        )
        acciones_label = Text("acciones", font_size=20, color=BLUE).move_to(
            LEFT * 6.2 + UP * 0.6
        )
        prob_legend = Text(
            "prob. transición", font_size=20, color=LIGHT_GREY
        ).move_to(LEFT * 5.8 + DOWN * 0.8)
        rewards_legend = VGroup(
            Text("recompensas ( ", font_size=20, color=WHITE),
            Text("+", font_size=20, color=GREEN),
            Text(", ", font_size=20, color=WHITE),
            Text("-", font_size=20, color=RED),
            Text(" )", font_size=20, color=WHITE),
        ).arrange(RIGHT, buff=0.05).move_to(LEFT * 5.8 + DOWN * 1.6)

        # Layer 3: arrows
        high_wait_top = Arrow(
            high.get_top() + LEFT * 0.25, wait_top.get_bottom(),
            color=WHITE, buff=0.05, stroke_width=2, tip_length=0.16,
        )
        wait_top_high = Arrow(
            wait_top.get_bottom() + RIGHT * 0.05, high.get_top() + RIGHT * 0.25,
            color=WHITE, buff=0.05, stroke_width=2, tip_length=0.16,
        )
        low_search_top = CurvedArrow(
            low.get_top() + RIGHT * 0.25, search_top.get_bottom(),
            angle=-0.3, color=WHITE, stroke_width=2, tip_length=0.16,
        )
        search_top_low = CurvedArrow(
            search_top.get_bottom() + LEFT * 0.05, low.get_top() + LEFT * 0.25,
            angle=-0.3, color=WHITE, stroke_width=2, tip_length=0.16,
        )
        search_top_high = CurvedArrow(
            search_top.get_left() + DOWN * 0.05, high.get_top() + RIGHT * 0.25,
            angle=0.3, color=WHITE, stroke_width=2, tip_length=0.16,
        )
        low_recharge = Arrow(
            low.get_left(), recharge.get_right(),
            color=WHITE, buff=0.1, stroke_width=2, tip_length=0.16,
        )
        recharge_high = Arrow(
            recharge.get_left(), high.get_right(),
            color=WHITE, buff=0.1, stroke_width=2, tip_length=0.16,
        )
        high_search_bottom = Arrow(
            high.get_bottom() + LEFT * 0.25, search_bottom.get_top(),
            color=WHITE, buff=0.05, stroke_width=2, tip_length=0.16,
        )
        search_bottom_high = Arrow(
            search_bottom.get_top() + RIGHT * 0.05, high.get_bottom() + RIGHT * 0.25,
            color=WHITE, buff=0.05, stroke_width=2, tip_length=0.16,
        )
        search_bottom_low = CurvedArrow(
            search_bottom.get_right(), low.get_bottom() + LEFT * 0.25,
            angle=-0.5, color=WHITE, stroke_width=2, tip_length=0.16,
        )
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
        search_top_low_label = _transition_label(
            r"1-\beta", "-3", reward_negative=True
        ).move_to(RIGHT * 3.5 + UP * 1.4 + g_shift)
        low_high_label = _transition_label("1", "0").next_to(recharge, UP, buff=0.55)
        search_bottom_label = _transition_label(
            r"\alpha", r"r_{\text{search}}"
        ).move_to(LEFT * 1.8 + DOWN * 3.0 + g_shift)
        search_bottom_low_label = _transition_label(
            r"1-\alpha", r"r_{\text{search}}"
        ).move_to(RIGHT * 0.2 + DOWN * 2.2 + g_shift)
        wait_bottom_label = _transition_label("1", r"r_{\text{wait}}").move_to(
            RIGHT * 1.8 + DOWN * 3.0 + g_shift
        )

        # ---------------------------------------------------------------
        # Animate graph — layer by layer
        # ---------------------------------------------------------------
        self.play(Create(high_group), Create(low_group), FadeIn(estados_label))
        self.wait(0.5)
        self.next_slide()

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

        self.play(
            Create(high_wait_top), Create(wait_top_high),
            Create(low_search_top), Create(search_top_low), Create(search_top_high),
            Create(low_recharge), Create(recharge_high),
            Create(high_search_bottom), Create(search_bottom_high),
            Create(search_bottom_low),
            Create(low_wait_bottom), Create(wait_bottom_low),
            FadeIn(prob_legend),
        )
        self.wait(0.5)
        self.next_slide()

        self.play(
            FadeIn(wait_top_label), FadeIn(search_top_label),
            FadeIn(search_top_low_label), FadeIn(low_high_label),
            FadeIn(search_bottom_label), FadeIn(search_bottom_low_label),
            FadeIn(wait_bottom_label), FadeIn(rewards_legend),
        )
        self.wait(0.5)
        self.next_slide()

        # ===================================================================
        # GRAPH TRAVERSALS
        # ===================================================================
        state_nodes = [high_group, low_group]
        action_nodes = [
            wait_top_group, search_top_group, search_bottom_group,
            wait_bottom_group, recharge_group,
        ]
        all_nodes = state_nodes + action_nodes
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

        def _attenuate(exclude_edges, exclude_nodes=None, exclude_labels=None):
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
                        if n in state_nodes:
                            # Hollow circle: dim stroke and text independently
                            anims.append(
                                n[0].animate.set_stroke(opacity=SUBDUED_OPACITY)
                            )
                            anims.append(n[1].animate.set_opacity(SUBDUED_OPACITY))
                        else:
                            anims.append(n.animate.set_opacity(SUBDUED_OPACITY))
            return anims

        def _restore():
            anims = []
            for e in all_edges:
                anims.append(e.animate.set_opacity(1.0))
            for lbl in all_labels:
                anims.append(lbl.animate.set_opacity(1.0))
            for n in all_nodes:
                if n in state_nodes:
                    # Restore stroke fully; keep fill transparent to avoid white-fill artefact
                    anims.append(
                        n[0].animate.set_stroke(opacity=1.0).set_fill(opacity=0)
                    )
                    anims.append(n[1].animate.set_opacity(1.0))
                else:
                    anims.append(n.animate.set_opacity(1.0))
            return anims

        dot = Dot(color=RED, radius=0.15).move_to(high.get_center())
        self.play(FadeIn(dot))
        self.wait(0.3)

        # Traversal 1: high → search_bottom → high  (α probability)
        self.play(
            *_attenuate(
                [high_search_bottom, search_bottom_high],
                [high_group, search_bottom_group],
                [search_bottom_label],
            ),
            run_time=0.5,
        )
        self.play(MoveAlongPath(dot, high_search_bottom.copy()), run_time=0.8)
        self.wait(0.2)
        self.play(MoveAlongPath(dot, search_bottom_high.copy()), run_time=0.8)
        self.wait(0.5)
        self.next_slide()

        # Traversal 2: high → search_bottom → low  (1−α probability)
        self.play(*_restore(), run_time=0.4)
        dot.move_to(high.get_center())
        self.play(
            *_attenuate(
                [high_search_bottom, search_bottom_low],
                [high_group, search_bottom_group, low_group],
                [search_bottom_label, search_bottom_low_label],
            ),
            run_time=0.5,
        )
        self.play(MoveAlongPath(dot, high_search_bottom.copy()), run_time=0.8)
        self.wait(0.2)
        self.play(MoveAlongPath(dot, search_bottom_low.copy()), run_time=0.8)
        self.wait(0.5)
        self.next_slide()

        # Traversal 3: low → recharge → high
        self.play(*_restore(), run_time=0.4)
        dot.move_to(low.get_center())
        self.play(
            *_attenuate(
                [low_recharge, recharge_high],
                [low_group, recharge_group, high_group],
                [low_high_label],
            ),
            run_time=0.5,
        )
        self.play(MoveAlongPath(dot, low_recharge.copy()), run_time=0.8)
        self.wait(0.2)
        self.play(MoveAlongPath(dot, recharge_high.copy()), run_time=0.8)
        self.wait(0.5)
        self.next_slide()

        # End: restore and hold
        self.play(*_restore(), FadeOut(dot), run_time=0.4)
        self.wait(1)
