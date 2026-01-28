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
        # SECTION 10: Algorithm Summary
        # ============================================================

        summary_label = Text("Resumen del algoritmo iLQR", font_size=30, color=BLUE)
        summary_label.move_to(UP * 2.5)

        self.play(FadeIn(summary_label))
        self.wait(0.3)

        # Algorithm steps
        steps = VGroup(
            MathTex(r"1. \text{ Inicializar trayectoria nominal } \hat{\boldsymbol{\tau}}", font_size=24),
            MathTex(r"2. \text{ Calcular } \mathbf{F}_t, \mathbf{C}_t, \mathbf{c}_t \text{ (linearizar/cuadratizar)}", font_size=24),
            MathTex(r"3. \text{ Backward pass: calcular } \mathbf{K}_t, \mathbf{k}_t", font_size=24),
            MathTex(r"4. \text{ Forward pass: generar nueva trayectoria}", font_size=24),
            MathTex(r"5. \text{ Line search y regularización}", font_size=24),
            MathTex(r"6. \text{ Repetir hasta convergencia}", font_size=24),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        steps.next_to(summary_label, DOWN, buff=0.5)

        steps_box = RoundedRectangle(
            corner_radius=0.2,
            width=steps.width + 1,
            height=steps.height + 0.6,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        steps_box.move_to(steps)

        self.play(FadeIn(steps_box), FadeIn(steps))
        self.wait(0.5)
        self.next_slide()

        # Final wait
        self.wait(1)
