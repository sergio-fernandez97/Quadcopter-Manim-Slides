"""
iLQR: Iterative Linear Quadratic Regulator slide.

Covers the iLQR algorithm for trajectory optimization in non-linear systems,
including Taylor approximations, backward/forward passes, line search, and regularization.

Example:
    uv run manim-slides render slides/13_ilqr.py ILQRSlide
"""

from manim import *
from manim_slides import Slide


class ILQRSlide(Slide):
    """iLQR algorithm explanation with trajectory visualization and backward/forward pass."""

    def construct(self):
        # === TITLE ===
        title = Text("iLQR: Regulador Cuadrático Lineal Iterativo", font_size=38, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))
        self.wait(0.5)
        self.next_slide()

        # ============================================================
        # SECTION A: Control Óptimo
        # ============================================================

        oc_label = Text("Control Óptimo", font_size=32, color=BLUE)
        oc_label.move_to(UP * 2)

        oc_eq = MathTex(
            r"\min_{\mathbf{u}_0, \cdots, \mathbf{u}_{T-1}} \sum_{t=0}^{T} c(\mathbf{x}_t, \mathbf{u}_t)"
            r" \quad \text{s.t.} \quad \mathbf{x}_{t+1} = f(\mathbf{x}_t, \mathbf{u}_t)",
            font_size=26,
        )
        oc_eq.next_to(oc_label, DOWN, buff=0.5)

        oc_eq_box = RoundedRectangle(
            corner_radius=0.2,
            width=oc_eq.width + 0.8,
            height=oc_eq.height + 0.5,
            color=YELLOW,
            fill_opacity=0.1,
            stroke_width=2,
        )
        oc_eq_box.move_to(oc_eq)

        self.play(FadeIn(oc_label), FadeIn(oc_eq_box), FadeIn(oc_eq))
        self.wait(0.5)
        self.next_slide()

        oc_bullets = VGroup(
            MathTex(r"\bullet \text{ Encontrar trayectoria que minimice costo sujeto a dinámica}", font_size=24),
            MathTex(r"\bullet \; c(\mathbf{x}_t, \mathbf{u}_t) \text{: costo instantáneo}", font_size=24),
            MathTex(r"\bullet \; c(\boldsymbol{\tau}) \text{: costo acumulado de la trayectoria}", font_size=24),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        oc_bullets.next_to(oc_eq_box, DOWN, buff=0.5)

        self.play(FadeIn(oc_bullets))
        self.wait(0.5)
        self.next_slide()

        # Clear section A
        self.play(
            FadeOut(oc_label),
            FadeOut(oc_eq_box),
            FadeOut(oc_eq),
            FadeOut(oc_bullets),
        )
        self.wait(0.3)

        # ============================================================
        # SECTION B: Función de valor V
        # ============================================================

        vf_label = Text("Función de valor V", font_size=32, color=BLUE)
        vf_label.move_to(UP * 2.5)

        vf_def = Text(
            "La función de valor óptima V* satisface la ecuación de Bellman",
            font_size=22,
            color=GRAY_B,
        )
        vf_def.next_to(vf_label, DOWN, buff=0.4)

        self.play(FadeIn(vf_label), FadeIn(vf_def))
        self.wait(0.3)

        vf_bellman = MathTex(
            r"V_{*}(\mathbf{x}_t) = \min_{\mathbf{u}_t \in \mathcal{U}(\mathbf{x}_t)}"
            r" \left\{ \underbrace{c(\mathbf{x}_t, \mathbf{u}_t) + V_{*}(\mathbf{x}_{t+1})}_{Q(\mathbf{x}_t, \mathbf{u}_t)} \right\}",
            font_size=26,
        )
        vf_bellman.next_to(vf_def, DOWN, buff=0.4)

        vf_bellman_box = RoundedRectangle(
            corner_radius=0.2,
            width=vf_bellman.width + 0.8,
            height=vf_bellman.height + 0.5,
            color=YELLOW,
            fill_opacity=0.1,
            stroke_width=2,
        )
        vf_bellman_box.move_to(vf_bellman)

        self.play(FadeIn(vf_bellman_box), FadeIn(vf_bellman))
        self.wait(0.5)
        self.next_slide()

        vf_boundary = MathTex(
            r"\text{donde } \mathbf{x}_{t+1} = f(\mathbf{x}_t, \mathbf{u}_t)"
            r" \text{ y } V_{*}(\mathbf{x}_{T}) = c(\mathbf{x}_{T}, \mathbf{0})",
            font_size=22,
            color=GRAY_B,
        )
        vf_boundary.next_to(vf_bellman_box, DOWN, buff=0.4)

        vf_note = MathTex(
            r"Q(\mathbf{x}_t, \mathbf{u}_t) \text{: costo inmediato + costo óptimo futuro}",
            font_size=22,
            color=GREEN,
        )
        vf_note.next_to(vf_boundary, DOWN, buff=0.3)

        self.play(FadeIn(vf_boundary), FadeIn(vf_note))
        self.wait(0.5)
        self.next_slide()

        # Clear section B
        self.play(
            FadeOut(vf_label),
            FadeOut(vf_def),
            FadeOut(vf_bellman_box),
            FadeOut(vf_bellman),
            FadeOut(vf_boundary),
            FadeOut(vf_note),
        )
        self.wait(0.3)

        # ============================================================
        # SECTION C: Iteración de Valores
        # ============================================================

        vi_label = Text("Programación Dinámica: Iteración de Valores", font_size=30, color=BLUE)
        vi_label.move_to(UP * 2.5)

        vi_bullets = VGroup(
            MathTex(r"\bullet \text{ Principio de optimalidad de Bellman: subsecuencia óptima sigue siendo óptima}", font_size=22),
            MathTex(r"\bullet \text{ Resuelve la ecuación de Bellman recursivamente}", font_size=22),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        vi_bullets.next_to(vi_label, DOWN, buff=0.4)

        self.play(FadeIn(vi_label), FadeIn(vi_bullets))
        self.wait(0.5)
        self.next_slide()

        vi_eval = MathTex(
            r"V_{k+1}(\mathbf{x}) = \min_{\mathbf{u}} \left\{ c(\mathbf{x}, \mathbf{u}) + V_k(f(\mathbf{x}, \mathbf{u})) \right\}",
            font_size=26,
        )
        vi_eval_label = Text("Evaluación de política", font_size=20, color=GRAY_B)
        vi_eval_group = VGroup(vi_eval, vi_eval_label).arrange(DOWN, buff=0.15)

        vi_policy = MathTex(
            r"\mu_{k+1}(\mathbf{x}) = \arg\min_{\mathbf{u}} \left\{ c(\mathbf{x}, \mathbf{u}) + V_k(f(\mathbf{x}, \mathbf{u})) \right\}",
            font_size=26,
        )
        vi_policy_label = Text("Ley de control óptimo", font_size=20, color=GRAY_B)
        vi_policy_group = VGroup(vi_policy, vi_policy_label).arrange(DOWN, buff=0.15)

        vi_eqs = VGroup(vi_eval_group, vi_policy_group).arrange(DOWN, buff=0.4)
        vi_eqs.next_to(vi_bullets, DOWN, buff=0.5)

        vi_box = RoundedRectangle(
            corner_radius=0.2,
            width=vi_eqs.width + 0.8,
            height=vi_eqs.height + 0.5,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        vi_box.move_to(vi_eqs)

        self.play(FadeIn(vi_box), FadeIn(vi_eqs))
        self.wait(0.5)
        self.next_slide()

        # Clear section C
        self.play(
            FadeOut(vi_label),
            FadeOut(vi_bullets),
            FadeOut(vi_box),
            FadeOut(vi_eqs),
        )
        self.wait(0.3)

        # ============================================================
        # SECTION 1: Introduction and Motivation
        # ============================================================

        intro_label = Text("Motivación", font_size=32, color=BLUE)
        intro_label.move_to(UP * 2)

        intro_items = VGroup(
            MathTex(r"\bullet \text{ Extiende LQR a sistemas no lineales}", font_size=24),
            MathTex(r"\bullet \text{ Aproximación lineal variable en el tiempo de } f", font_size=24),
            MathTex(r"\bullet \text{ Aproximación cuadrática variable en el tiempo de } c", font_size=24),
            MathTex(r"\bullet \text{ Captura la no linealidad para controles más efectivos}", font_size=24),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)

        intro_group = VGroup(intro_label, intro_items).arrange(DOWN, buff=0.4)
        intro_group.move_to(UP * 0.3)

        intro_box = RoundedRectangle(
            corner_radius=0.2,
            width=intro_group.width + 1,
            height=intro_group.height + 0.6,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        intro_box.move_to(intro_group)

        self.play(FadeIn(intro_box), FadeIn(intro_group))
        self.wait(0.5)
        self.next_slide()

        # Key insight
        insight_text = MathTex(
            r"\text{Aproximación de Newton para optimización de trayectorias}",
            font_size=24,
            color=YELLOW,
        )
        insight_text.next_to(intro_box, DOWN, buff=0.4)

        self.play(FadeIn(insight_text))
        self.wait(0.5)
        self.next_slide()

        # Clear section 1
        self.play(
            FadeOut(intro_box),
            FadeOut(intro_group),
            FadeOut(insight_text),
        )
        self.wait(0.3)

        # ============================================================
        # SECTION 2: Hypotheses
        # ============================================================

        hyp_label = Text("Hipótesis", font_size=32, color=BLUE)

        hyp_dynamics = MathTex(
            r"f \in \mathcal{C}^{1}(\mathcal{X} \times \mathcal{U}, \mathcal{X})",
            font_size=28,
        )
        hyp_dynamics_desc = Text("Dinámica diferenciable", font_size=20, color=GRAY_B)

        hyp_cost = MathTex(
            r"c \in \mathcal{C}^{2}(\mathcal{X} \times \mathcal{U}, \mathbb{R}^{+})",
            font_size=28,
        )
        hyp_cost_desc = Text("Costo doblemente diferenciable", font_size=20, color=GRAY_B)

        hyp_content = VGroup(
            VGroup(hyp_dynamics, hyp_dynamics_desc).arrange(DOWN, buff=0.1),
            VGroup(hyp_cost, hyp_cost_desc).arrange(DOWN, buff=0.1),
        ).arrange(DOWN, buff=0.4)

        hyp_group = VGroup(hyp_label, hyp_content).arrange(DOWN, buff=0.5)
        hyp_group.move_to(UP * 0.3)

        hyp_box = RoundedRectangle(
            corner_radius=0.2,
            width=hyp_group.width + 1,
            height=hyp_group.height + 0.6,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        hyp_box.move_to(hyp_group)

        self.play(FadeIn(hyp_box), FadeIn(hyp_group))
        self.wait(0.5)
        self.next_slide()

        # Clear section 2
        self.play(FadeOut(hyp_box), FadeOut(hyp_group))
        self.wait(0.3)

        # ============================================================
        # SECTION 3: Nominal Trajectory
        # ============================================================

        traj_label = Text("Trayectoria nominal", font_size=30, color=BLUE)
        traj_label.move_to(UP * 2.5)

        self.play(FadeIn(traj_label))
        self.wait(0.3)

        # Nominal trajectory equation
        traj_eq = MathTex(
            r"\hat{\boldsymbol{\tau}} = \left\{\hat{\mathbf{x}}_1, \hat{\mathbf{u}}_1, \hat{\mathbf{x}}_2, \hat{\mathbf{u}}_2, \cdots, \hat{\mathbf{x}}_T, \hat{\mathbf{u}}_T\right\}",
            font_size=28,
        )
        traj_eq.move_to(UP * 1.3)

        self.play(FadeIn(traj_eq))
        self.wait(0.5)
        self.next_slide()

        # Deviation coordinates
        dev_label = Text("Sistema de coordenadas relativas", font_size=26, color=GREEN)
        dev_label.next_to(traj_eq, DOWN, buff=0.5)

        dev_eq = MathTex(
            r"\bar{\mathbf{x}}_t = \mathbf{x}_t - \hat{\mathbf{x}}_t, \qquad \bar{\mathbf{u}}_t = \mathbf{u}_t - \hat{\mathbf{u}}_t",
            font_size=28,
            color=ORANGE,
        )
        dev_eq.next_to(dev_label, DOWN, buff=0.3)

        dev_group = VGroup(dev_label, dev_eq)

        dev_box = RoundedRectangle(
            corner_radius=0.2,
            width=dev_group.width + 0.8,
            height=dev_group.height + 0.5,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        dev_box.move_to(dev_group)

        self.play(FadeIn(dev_box), FadeIn(dev_group))
        self.wait(0.5)
        self.next_slide()

        # Clear section 3
        self.play(
            FadeOut(traj_label),
            FadeOut(traj_eq),
            FadeOut(dev_box),
            FadeOut(dev_group),
        )
        self.wait(0.3)

        # ============================================================
        # SECTION 4: Taylor Linearization of Dynamics
        # ============================================================

        lin_label = Text("Aproximación lineal de la dinámica", font_size=30, color=BLUE)
        lin_label.move_to(UP * 2.5)

        self.play(FadeIn(lin_label))
        self.wait(0.3)

        # First order Taylor expansion
        taylor_eq = MathTex(
            r"\bar{\mathbf{x}}_{t+1} \approx",
            r"\underbrace{\nabla_{\mathbf{x}} f(\hat{\mathbf{x}}_t, \hat{\mathbf{u}}_t)}_{\mathbf{A}_t}",
            r"\bar{\mathbf{x}}_t +",
            r"\underbrace{\nabla_{\mathbf{u}} f(\hat{\mathbf{x}}_t, \hat{\mathbf{u}}_t)}_{\mathbf{B}_t}",
            r"\bar{\mathbf{u}}_t",
            font_size=26,
        )
        taylor_eq.move_to(UP * 1)

        self.play(FadeIn(taylor_eq))
        self.wait(0.5)
        self.next_slide()

        # Compact form
        compact_eq = MathTex(
            r"\bar{\mathbf{x}}_{t+1} \approx \mathbf{F}_t \begin{bmatrix} \bar{\mathbf{x}}_t \\ \bar{\mathbf{u}}_t \end{bmatrix}",
            r"\quad \text{donde } \mathbf{F}_t = \begin{bmatrix} \mathbf{A}_t & \mathbf{B}_t \end{bmatrix}",
            font_size=26,
        )
        compact_eq.next_to(taylor_eq, DOWN, buff=0.5)

        self.play(FadeIn(compact_eq))
        self.wait(0.5)
        self.next_slide()

        # Note about time-varying
        tv_note = Text(
            "Sistema lineal no autónomo (variable en el tiempo)",
            font_size=22,
            color=YELLOW,
        )
        tv_note.next_to(compact_eq, DOWN, buff=0.4)

        self.play(FadeIn(tv_note))
        self.wait(0.5)
        self.next_slide()

        # Clear section 4
        self.play(
            FadeOut(lin_label),
            FadeOut(taylor_eq),
            FadeOut(compact_eq),
            FadeOut(tv_note),
        )
        self.wait(0.3)

        # ============================================================
        # SECTION 5: Quadratic Cost Approximation
        # ============================================================

        cost_label = Text("Aproximación cuadrática del costo", font_size=30, color=BLUE)
        cost_label.move_to(UP * 2.5)

        self.play(FadeIn(cost_label))
        self.wait(0.3)

        # Taylor expansion of cost (second order)
        cost_taylor = MathTex(
            r"c(\mathbf{x}_t, \mathbf{u}_t) \approx \text{cte} + \frac{1}{2} \begin{bmatrix} \bar{\mathbf{x}}_t \\ \bar{\mathbf{u}}_t \end{bmatrix}^\top \mathbf{C}_t \begin{bmatrix} \bar{\mathbf{x}}_t \\ \bar{\mathbf{u}}_t \end{bmatrix} + \begin{bmatrix} \bar{\mathbf{x}}_t \\ \bar{\mathbf{u}}_t \end{bmatrix}^\top \mathbf{c}_t",
            font_size=24,
        )
        cost_taylor.move_to(UP * 1.2)

        self.play(FadeIn(cost_taylor))
        self.wait(0.5)
        self.next_slide()

        # Partition of C and c
        partition_label = Text("Partición en componentes:", font_size=22, color=GREEN)
        partition_label.next_to(cost_taylor, DOWN, buff=0.5)

        partition_C = MathTex(
            r"\mathbf{C}_t = \begin{bmatrix} \mathbf{C}_{\mathbf{xx}_t} & \mathbf{C}_{\mathbf{xu}_t} \\ \mathbf{C}_{\mathbf{ux}_t} & \mathbf{C}_{\mathbf{uu}_t} \end{bmatrix}",
            font_size=24,
        )

        partition_c = MathTex(
            r"\mathbf{c}_t = \begin{bmatrix} \mathbf{c}_{\mathbf{x}_t} \\ \mathbf{c}_{\mathbf{u}_t} \end{bmatrix}",
            font_size=24,
        )

        partition_group = VGroup(partition_C, partition_c).arrange(RIGHT, buff=1)
        partition_group.next_to(partition_label, DOWN, buff=0.3)

        self.play(FadeIn(partition_label), FadeIn(partition_group))
        self.wait(0.5)
        self.next_slide()

        # Clear section 5
        self.play(
            FadeOut(cost_label),
            FadeOut(cost_taylor),
            FadeOut(partition_label),
            FadeOut(partition_group),
        )
        self.wait(0.3)

        # ============================================================
        # SECTION 6: Backward Pass
        # ============================================================

        backward_label = Text("Backward Pass", font_size=30, color=BLUE)
        backward_label.move_to(UP * 2.5)

        self.play(FadeIn(backward_label))
        self.wait(0.3)

        # Boundary condition
        boundary_eq = MathTex(
            r"Q(\mathbf{x}_T, \mathbf{u}_T) = c(\mathbf{x}_T, \mathbf{u}_T)",
            font_size=26,
        )
        boundary_label = Text("Condición de frontera (t = T)", font_size=20, color=GRAY_B)
        boundary_group = VGroup(boundary_label, boundary_eq).arrange(DOWN, buff=0.2)
        boundary_group.move_to(UP * 1.3)

        self.play(FadeIn(boundary_group))
        self.wait(0.5)
        self.next_slide()

        # Q function recursion
        q_recursion_label = Text("Recursión para t < T:", font_size=22, color=GREEN)
        q_recursion_label.next_to(boundary_group, DOWN, buff=0.4)

        q_eq = MathTex(
            r"\mathbf{Q}_t = \mathbf{C}_t + \mathbf{F}_t^\top \mathbf{V}_{t+1} \mathbf{F}_t",
            font_size=24,
        )
        q_vec_eq = MathTex(
            r"\mathbf{q}_t = \mathbf{c}_t + \mathbf{F}_t^\top \mathbf{v}_{t+1}",
            font_size=24,
        )

        q_group = VGroup(q_eq, q_vec_eq).arrange(DOWN, buff=0.2)
        q_group.next_to(q_recursion_label, DOWN, buff=0.3)

        self.play(FadeIn(q_recursion_label), FadeIn(q_group))
        self.wait(0.5)
        self.next_slide()

        # Clear for control law
        self.play(
            FadeOut(boundary_group),
            FadeOut(q_recursion_label),
            FadeOut(q_group),
        )
        self.wait(0.2)

        # Optimal control law
        control_label = Text("Ley de control óptimo", font_size=26, color=GREEN)
        control_label.next_to(backward_label, DOWN, buff=0.5)

        control_eq = MathTex(
            r"\mathbf{u}_t = \hat{\mathbf{u}}_t + \mathbf{K}_t(\mathbf{x}_t - \hat{\mathbf{x}}_t) + \mathbf{k}_t",
            font_size=30,
            color=YELLOW,
        )
        control_eq.next_to(control_label, DOWN, buff=0.4)

        control_box = RoundedRectangle(
            corner_radius=0.2,
            width=control_eq.width + 0.8,
            height=control_eq.height + 0.5,
            color=YELLOW,
            fill_opacity=0.1,
            stroke_width=2,
        )
        control_box.move_to(control_eq)

        self.play(FadeIn(control_label), FadeIn(control_box), FadeIn(control_eq))
        self.wait(0.5)
        self.next_slide()

        # Gains
        gains_eq = MathTex(
            r"\mathbf{K}_t = -\mathbf{Q}_{\mathbf{uu}_t}^{-1} \mathbf{Q}_{\mathbf{ux}_t}, \quad \mathbf{k}_t = -\mathbf{Q}_{\mathbf{uu}_t}^{-1} \mathbf{q}_{\mathbf{u}_t}",
            font_size=26,
        )
        gains_eq.next_to(control_box, DOWN, buff=0.5)

        self.play(FadeIn(gains_eq))
        self.wait(0.5)
        self.next_slide()

        # Value function update
        value_label = Text("Función de valor:", font_size=22, color=GREEN)
        value_label.next_to(gains_eq, DOWN, buff=0.4)

        value_eq = MathTex(
            r"V(\mathbf{x}_t) = \text{cte} + \frac{1}{2} \bar{\mathbf{x}}_t^\top \mathbf{V}_t \bar{\mathbf{x}}_t + \bar{\mathbf{x}}_t^\top \mathbf{v}_t",
            font_size=24,
        )
        value_eq.next_to(value_label, DOWN, buff=0.2)

        self.play(FadeIn(value_label), FadeIn(value_eq))
        self.wait(0.5)
        self.next_slide()

        # Clear section 6
        self.play(
            FadeOut(backward_label),
            FadeOut(control_label),
            FadeOut(control_box),
            FadeOut(control_eq),
            FadeOut(gains_eq),
            FadeOut(value_label),
            FadeOut(value_eq),
        )
        self.wait(0.3)

        # ============================================================
        # SECTION 7: Forward Pass
        # ============================================================

        forward_label = Text("Forward Pass", font_size=30, color=BLUE)
        forward_label.move_to(UP * 2.5)

        self.play(FadeIn(forward_label))
        self.wait(0.3)

        # Forward pass equations
        forward_init = MathTex(
            r"\hat{\mathbf{x}}_0 = \mathbf{x}_0",
            font_size=28,
        )
        forward_init.move_to(UP * 1.3)

        forward_eq1 = MathTex(
            r"\hat{\mathbf{u}}_t = \hat{\mathbf{u}}_t + \alpha \mathbf{k}_t + \mathbf{K}_t(\mathbf{x}_t - \hat{\mathbf{x}}_t)",
            font_size=28,
        )
        forward_eq2 = MathTex(
            r"\hat{\mathbf{x}}_{t+1} = f(\hat{\mathbf{x}}_t, \hat{\mathbf{u}}_t)",
            font_size=28,
        )

        forward_eqs = VGroup(forward_init, forward_eq1, forward_eq2).arrange(DOWN, buff=0.4)
        forward_eqs.move_to(UP * 0.3)

        forward_box = RoundedRectangle(
            corner_radius=0.2,
            width=forward_eqs.width + 0.8,
            height=forward_eqs.height + 0.6,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        forward_box.move_to(forward_eqs)

        self.play(FadeIn(forward_box), FadeIn(forward_eqs))
        self.wait(0.5)
        self.next_slide()

        # Note about new trajectory
        update_note = Text(
            "Nueva trayectoria nominal para la siguiente iteración",
            font_size=22,
            color=GREEN,
        )
        update_note.next_to(forward_box, DOWN, buff=0.4)

        self.play(FadeIn(update_note))
        self.wait(0.5)
        self.next_slide()

        # Clear section 7
        self.play(
            FadeOut(forward_label),
            FadeOut(forward_box),
            FadeOut(forward_eqs),
            FadeOut(update_note),
        )
        self.wait(0.3)

        # ============================================================
        # SECTION 8: Line Search
        # ============================================================

        ls_label = Text("Búsqueda de línea", font_size=30, color=BLUE)
        ls_label.move_to(UP * 2.5)

        self.play(FadeIn(ls_label))
        self.wait(0.3)

        # Alpha parameter
        alpha_eq = MathTex(
            r"\mathbf{u}_t = \hat{\mathbf{u}}_t + \mathbf{K}_t(\mathbf{x}_t - \hat{\mathbf{x}}_t) + \alpha \mathbf{k}_t",
            font_size=28,
        )
        alpha_note = MathTex(
            r"\alpha \in (0, 1]",
            font_size=26,
            color=ORANGE,
        )
        alpha_group = VGroup(alpha_eq, alpha_note).arrange(DOWN, buff=0.3)
        alpha_group.move_to(UP * 1)

        self.play(FadeIn(alpha_group))
        self.wait(0.5)
        self.next_slide()

        # Convergence criterion
        conv_label = Text("Criterio de convergencia:", font_size=22, color=GREEN)
        conv_label.next_to(alpha_group, DOWN, buff=0.5)

        conv_eq = MathTex(
            r"\frac{|c(\boldsymbol{\tau}) - c(\hat{\boldsymbol{\tau}})|}{c(\hat{\boldsymbol{\tau}})} < \epsilon_{\text{tol}}",
            font_size=28,
        )
        conv_eq.next_to(conv_label, DOWN, buff=0.3)

        conv_box = RoundedRectangle(
            corner_radius=0.2,
            width=conv_eq.width + 0.8,
            height=conv_eq.height + 0.5,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        conv_box.move_to(conv_eq)

        self.play(FadeIn(conv_label), FadeIn(conv_box), FadeIn(conv_eq))
        self.wait(0.5)
        self.next_slide()

        # Purpose
        ls_purpose = Text(
            "Evita divergencia cuando la trayectoria se aleja del modelo",
            font_size=20,
            color=GRAY_B,
        )
        ls_purpose.next_to(conv_box, DOWN, buff=0.4)

        self.play(FadeIn(ls_purpose))
        self.wait(0.5)
        self.next_slide()

        # Clear section 8
        self.play(
            FadeOut(ls_label),
            FadeOut(alpha_group),
            FadeOut(conv_label),
            FadeOut(conv_box),
            FadeOut(conv_eq),
            FadeOut(ls_purpose),
        )
        self.wait(0.3)

        # ============================================================
        # SECTION 9: Regularization
        # ============================================================

        reg_label = Text("Regularización", font_size=30, color=BLUE)
        reg_label.move_to(UP * 2.5)

        self.play(FadeIn(reg_label))
        self.wait(0.3)

        # Problem: Hessian not always positive definite
        problem_text = Text(
            "Problema: El hessiano no siempre es positivo definido",
            font_size=22,
            color=RED_C,
        )
        problem_text.move_to(UP * 1.5)

        self.play(FadeIn(problem_text))
        self.wait(0.5)
        self.next_slide()

        # Regularization scheme
        reg_eqs = VGroup(
            MathTex(
                r"\tilde{\mathbf{Q}}_{\mathbf{uu}_t} = \mathbf{C}_{\mathbf{uu}_t} + \mathbf{F}_{\mathbf{u}_t}^\top (\mathbf{V}_t + \lambda \mathbf{I}) \mathbf{F}_{\mathbf{u}_t}",
                font_size=24,
            ),
            MathTex(
                r"\tilde{\mathbf{Q}}_{\mathbf{ux}_t} = \mathbf{C}_{\mathbf{ux}_t} + \mathbf{F}_{\mathbf{u}_t}^\top (\mathbf{V}_t + \lambda \mathbf{I}) \mathbf{F}_{\mathbf{x}_t}",
                font_size=24,
            ),
        ).arrange(DOWN, buff=0.3)
        reg_eqs.next_to(problem_text, DOWN, buff=0.5)

        reg_box = RoundedRectangle(
            corner_radius=0.2,
            width=reg_eqs.width + 0.8,
            height=reg_eqs.height + 0.5,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        reg_box.move_to(reg_eqs)

        self.play(FadeIn(reg_box), FadeIn(reg_eqs))
        self.wait(0.5)
        self.next_slide()

        # Lambda update rules
        lambda_label = Text("Actualización de λ:", font_size=22, color=GREEN)
        lambda_label.next_to(reg_box, DOWN, buff=0.4)

        lambda_rules = VGroup(
            MathTex(r"\text{Incrementar: } \lambda^{(k+1)} = \max(\lambda_{\min}, \lambda^{(k)} \cdot \Delta)", font_size=22),
            MathTex(r"\text{Reducir: } \lambda^{(k+1)} = \lambda^{(k)} / \Delta \text{ si } \lambda > \lambda_{\min}", font_size=22),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        lambda_rules.next_to(lambda_label, DOWN, buff=0.2)

        self.play(FadeIn(lambda_label), FadeIn(lambda_rules))
        self.wait(0.5)
        self.next_slide()

        # Clear section 9
        self.play(
            FadeOut(reg_label),
            FadeOut(problem_text),
            FadeOut(reg_box),
            FadeOut(reg_eqs),
            FadeOut(lambda_label),
            FadeOut(lambda_rules),
        )
        self.wait(0.3)

        # ============================================================
        # SECTION 10: iLQR Algorithm
        # ============================================================

        alg_label = Text("Algoritmo iLQR", font_size=30, color=BLUE)
        alg_label.move_to(UP * 2.5)

        loop_header = Text("Mientras no haya convergencia", font_size=24, color=YELLOW)
        loop_header.next_to(alg_label, DOWN, buff=0.35)

        self.play(FadeIn(alg_label), FadeIn(loop_header))
        self.wait(0.3)

        step1_title = Text("1. Linealizar dinámica y cuadratizar costo", font_size=22, color=GREEN)
        step1_eq = MathTex(
            r"\mathbf{F}_t = \nabla_{\mathbf{x}_t,\mathbf{u}_t} f(\hat{\mathbf{x}}_t, \hat{\mathbf{u}}_t),"
            r"\quad \mathbf{c}_t = \nabla_{\mathbf{x}_t,\mathbf{u}_t} c(\hat{\mathbf{x}}_t, \hat{\mathbf{u}}_t),"
            r"\quad \mathbf{C}_t = \nabla_{\mathbf{x}_t,\mathbf{u}_t}^{2} c(\hat{\mathbf{x}}_t, \hat{\mathbf{u}}_t)",
            font_size=21,
        )
        step1_eq.scale_to_fit_width(config.frame_width - 1.4)
        step1_group = VGroup(step1_title, step1_eq).arrange(DOWN, buff=0.25, aligned_edge=LEFT)

        step2_title = Text("2. Backward pass para t = T-1, ..., 0", font_size=22, color=GREEN)
        step2_eqs = VGroup(
            MathTex(
                r"\mathbf{Q}_t = \mathbf{C}_t + \mathbf{F}_t^\top \mathbf{V}_{t+1} \mathbf{F}_t,"
                r"\quad \mathbf{q}_t = \mathbf{c}_t + \mathbf{F}_t^\top \mathbf{v}_{t+1}",
                font_size=22,
            ),
            MathTex(
                r"\mathbf{K}_t = -\tilde{\mathbf{Q}}_{\mathbf{uu}_t}^{-1}\tilde{\mathbf{Q}}_{\mathbf{ux}_t},"
                r"\quad \mathbf{k}_t = \tilde{\mathbf{Q}}_{\mathbf{uu}_t}^{-1}\tilde{\mathbf{q}}_{\mathbf{u}_t}",
                font_size=22,
            ),
            MathTex(
                r"\mathbf{V}_t,\mathbf{v}_t \leftarrow \text{actualizar función de valor}",
                font_size=22,
                color=GRAY_B,
            ),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        step2_eqs.scale_to_fit_width(config.frame_width - 1.4)
        step2_group = VGroup(step2_title, step2_eqs).arrange(DOWN, buff=0.25, aligned_edge=LEFT)

        phase1 = VGroup(step1_group, step2_group).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        phase1.next_to(loop_header, DOWN, buff=0.45)

        phase1_box = RoundedRectangle(
            corner_radius=0.2,
            width=phase1.width + 0.8,
            height=phase1.height + 0.6,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        phase1_box.move_to(phase1)

        self.play(FadeIn(phase1_box), FadeIn(step1_group))
        self.wait(0.5)
        self.next_slide()

        self.play(FadeIn(step2_group))
        self.wait(0.5)
        self.next_slide()

        self.play(FadeOut(phase1_box), FadeOut(phase1))
        self.wait(0.2)

        step3_title = Text("3. Forward pass con búsqueda de línea", font_size=22, color=GREEN)
        step3_eqs = VGroup(
            MathTex(
                r"\forall \alpha \in \boldsymbol{\alpha}:"
                r"\quad \mathbf{u}_t = \hat{\mathbf{u}}_t + \alpha \mathbf{k}_t + \mathbf{K}_t(\mathbf{x}_t - \hat{\mathbf{x}}_t)",
                font_size=20,
            ),
            MathTex(
                r"\mathbf{x}_{t+1} = f(\mathbf{x}_t, \mathbf{u}_t),"
                r"\quad \text{calcular } c(\boldsymbol{\tau}) \text{ y } c(\hat{\boldsymbol{\tau}})",
                font_size=20,
            ),
            MathTex(
                r"\text{si } c(\boldsymbol{\tau}) < c(\hat{\boldsymbol{\tau}})"
                r"\Rightarrow \hat{\boldsymbol{\tau}} \leftarrow \boldsymbol{\tau},\ \lambda \downarrow,\ \alpha^{*} = \alpha",
                font_size=19,
                color=GRAY_B,
            ),
            MathTex(
                r"\text{en otro caso } \lambda \uparrow \text{ y continuar con el siguiente } \alpha",
                font_size=19,
                color=GRAY_B,
            ),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        step3_eqs.scale_to_fit_width(config.frame_width - 1.6)
        step3_group = VGroup(step3_title, step3_eqs).arrange(DOWN, buff=0.25, aligned_edge=LEFT)

        step4_title = Text("4. Verificar convergencia y actualizar trayectoria nominal", font_size=22, color=GREEN)
        step4_eqs = VGroup(
            MathTex(
                r"\frac{|c(\boldsymbol{\tau}) - c(\hat{\boldsymbol{\tau}})|}{c(\hat{\boldsymbol{\tau}})} < \epsilon_{\text{tol}}",
                font_size=22,
            ),
            MathTex(
                r"\text{si se cumple el umbral: terminar; en otro caso continuar iterando}",
                font_size=20,
            ),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        step4_group = VGroup(step4_title, step4_eqs).arrange(DOWN, buff=0.25, aligned_edge=LEFT)

        step3_group.next_to(loop_header, DOWN, buff=0.45)

        step3_box = RoundedRectangle(
            corner_radius=0.2,
            width=step3_group.width + 0.8,
            height=step3_group.height + 0.6,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        step3_box.move_to(step3_group)

        self.play(FadeIn(step3_box), FadeIn(step3_group))
        self.wait(0.5)
        self.next_slide()

        self.play(FadeOut(step3_box), FadeOut(step3_group))
        self.wait(0.2)

        step4_group.next_to(loop_header, DOWN, buff=0.55)

        step4_box = RoundedRectangle(
            corner_radius=0.2,
            width=step4_group.width + 0.8,
            height=step4_group.height + 0.6,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        step4_box.move_to(step4_group)

        self.play(FadeIn(step4_box), FadeIn(step4_group))
        self.wait(0.5)
        self.next_slide()

        closing_note = Text(
            "El ciclo alterna planeación hacia atrás y simulación hacia adelante",
            font_size=20,
            color=YELLOW,
        )
        closing_note.next_to(step4_box, DOWN, buff=0.35)

        self.play(FadeIn(closing_note))
        self.wait(0.5)
        self.next_slide()

        # Final wait
        self.wait(1)
