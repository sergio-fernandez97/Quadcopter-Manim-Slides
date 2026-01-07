"""
Combined equations of motion and control system formulation for the quadcopter.

Contrasts local and inertial system equations, reframes them into a state-space
representation, and transitions to control system formulation with linearization.

Example:
    manim -pql slides/03_quadcopter_motion.py QuadcopterMotionSlide

Author: Sergio Fernández
Date: 2025-01-30
"""

from manim import *
from manim_slides import Slide

class QuadcopterMotionSlide(Slide):
    def construct(self):
        # Title
        title = Text("Ecuaciones de movimiento de un cuadricoptero", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.add(title)
        
        # Color definitions
        linear_velocity_color = YELLOW
        angular_velocity_color = BLUE
        state_color = GREEN
        control_color = RED
        
        # Show equations of motion for both systems
        # Local system equations (from Newton-Euler)
        local_title = Text("Sistema local", font_size=28, color=WHITE)
        local_title.shift(UP * 2.5 + LEFT * 4)
        
        local_linear = MathTex(
            r"\dot u &= rv - qw - g \sin\theta \\",
            r"\dot v &= pw - ru - g\cos\theta \cdot \sin\phi \\",
            r"\dot w &= qu - pv + g\cos\varphi \cdot \cos\theta - \frac{k}{m}\sum_{i=1}^{4}\omega_i^2",
            font_size=24
        )
        local_linear.shift(UP * 1.2 + LEFT * 4)
        local_linear.set_color_by_tex(r"\dot u", linear_velocity_color)
        local_linear.set_color_by_tex(r"\dot v", linear_velocity_color)
        local_linear.set_color_by_tex(r"\dot w", linear_velocity_color)
        
        local_angular = MathTex(
            r"\dot p &= \frac{\ell k}{I_{xx}}\left(\omega_4^2 - \omega_2^2\right) - qr \left(\frac{I_{zz} - I_{yy}}{I_{xx}}\right) \\",
            r"\dot q &= \frac{\ell k}{I_{yy}}\left(\omega_3^2 - \omega_1^2\right) - pr \left(\frac{I_{xx} - I_{zz}}{I_{yy}}\right) \\",
            r"\dot r &= \frac{b}{I_{zz}}\left(\omega_2^2 + \omega_4^2 - \omega_1^2 - \omega_3^2\right)",
            font_size=24
        )
        local_angular.shift(DOWN * 0.5 + LEFT * 4)
        local_angular.set_color_by_tex(r"\dot p", angular_velocity_color)
        local_angular.set_color_by_tex(r"\dot q", angular_velocity_color)
        local_angular.set_color_by_tex(r"\dot r", angular_velocity_color)
        
        # Inertial system equations
        inertial_title = Text("Sistema inercial", font_size=28, color=WHITE)
        inertial_title.shift(UP * 2.5 + RIGHT * 4)
        
        inertial_linear = MathTex(
            r"\dot{x} &= u \\",
            r"\dot{y} &= v \\",
            r"\dot{z} &= w",
            font_size=24
        )
        inertial_linear.shift(UP * 1.5 + RIGHT * 4)
        inertial_linear.set_color_by_tex(r"\dot{x}", linear_velocity_color)
        inertial_linear.set_color_by_tex(r"\dot{y}", linear_velocity_color)
        inertial_linear.set_color_by_tex(r"\dot{z}", linear_velocity_color)
        
        inertial_angular = MathTex(
            r"\dot{\varphi} &= p + (q \sin\varphi + r \cos\varphi) \tan\theta \\",
            r"\dot{\theta} &= q \cos\varphi - r \sin\varphi \\",
            r"\dot{\psi} &= \left(q \sin\varphi + r \cos\varphi\right) \sec\theta",
            font_size=24
        )
        inertial_angular.shift(DOWN * 0.3 + RIGHT * 4)
        inertial_angular.set_color_by_tex(r"\dot{\varphi}", angular_velocity_color)
        inertial_angular.set_color_by_tex(r"\dot{\theta}", angular_velocity_color)
        inertial_angular.set_color_by_tex(r"\dot{\psi}", angular_velocity_color)
        
        # Show all equations
        self.play(
            Write(local_title),
            Write(inertial_title)
        )
        self.wait(1)
        self.play(
            Write(local_linear),
            Write(local_angular),
            Write(inertial_linear),
            Write(inertial_angular),
            run_time=3
        )
        self.wait(2)
        
        # Fade out the titles
        self.play(
            FadeOut(local_title),
            FadeOut(inertial_title)
        )
        self.wait(0.5)
        
        # Extract left-hand sides from each equation
        # Local linear LHS
        local_linear_lhs = MathTex(
            r"\dot u \\",
            r"\dot v \\",
            r"\dot w",
            font_size=24
        )
        local_linear_lhs.move_to(local_linear.get_left() + RIGHT * 0.5)
        local_linear_lhs.set_color(linear_velocity_color)
        
        # Local angular LHS
        local_angular_lhs = MathTex(
            r"\dot p \\",
            r"\dot q \\",
            r"\dot r",
            font_size=24
        )
        local_angular_lhs.move_to(local_angular.get_left() + RIGHT * 0.5)
        local_angular_lhs.set_color(angular_velocity_color)
        
        # Inertial linear LHS
        inertial_linear_lhs = MathTex(
            r"\dot{x} \\",
            r"\dot{y} \\",
            r"\dot{z}",
            font_size=24
        )
        inertial_linear_lhs.move_to(inertial_linear.get_left() + RIGHT * 0.5)
        inertial_linear_lhs.set_color(linear_velocity_color)
        
        # Inertial angular LHS
        inertial_angular_lhs = MathTex(
            r"\dot{\varphi} \\",
            r"\dot{\theta} \\",
            r"\dot{\psi}",
            font_size=24
        )
        inertial_angular_lhs.move_to(inertial_angular.get_left() + RIGHT * 0.5)
        inertial_angular_lhs.set_color(angular_velocity_color)
        
        # Transform equations to show only LHS
        self.play(
            Transform(local_linear, local_linear_lhs),
            Transform(local_angular, local_angular_lhs),
            Transform(inertial_linear, inertial_linear_lhs),
            Transform(inertial_angular, inertial_angular_lhs),
            run_time=2
        )
        self.wait(1)
        
        # Move all LHS equations to the origin to merge them
        self.play(
            local_linear.animate.move_to(ORIGIN),
            local_angular.animate.move_to(ORIGIN),
            inertial_linear.animate.move_to(ORIGIN),
            inertial_angular.animate.move_to(ORIGIN),
            run_time=2
        )
        self.wait(0.5)
        
        # Merge all LHS into a single row vector
        # Order: u, v, w, p, q, r, phi, theta, psi, x, y, z
        merged_lhs_vector = MathTex(
            r"\begin{bmatrix} \dot u \\ \dot v \\ \dot w \\ \dot p \\ \dot q \\ \dot r \\ \dot{\varphi} \\ \dot{\theta} \\ \dot{\psi} \\ \dot{x} \\ \dot{y} \\ \dot{z} \end{bmatrix}",
            font_size=32
        )
        merged_lhs_vector.move_to(ORIGIN)
        
        # Transform all LHS into the merged vector
        self.play(
            Transform(local_linear, merged_lhs_vector),
            Transform(local_angular, merged_lhs_vector),
            Transform(inertial_linear, merged_lhs_vector),
            Transform(inertial_angular, merged_lhs_vector),
            run_time=2
        )
        self.wait(1)

        # Keep a single merged vector on screen to avoid duplicates.
        self.remove(local_angular, inertial_linear, inertial_angular)
        merged_lhs_vector = local_linear
        
        # Transform into \dot{\boldsymbol{x}}
        dot_x = MathTex(
            r"\dot{\boldsymbol{x}}",
            font_size=48
        )
        dot_x.move_to(ORIGIN)
        
        self.play(Transform(merged_lhs_vector, dot_x), run_time=1.5)
        dot_x = merged_lhs_vector
        self.wait(0.5)
        
        # Move dot_x to the left
        self.play(
            dot_x.animate.move_to(LEFT * 3),
            run_time=1
        )
        self.wait(0.5)

        # Change title
        new_title = Text("Cuadricoptero como sistema de control", font_size=48, color=WHITE)
        new_title.to_edge(UP)
        
        self.play(
            Transform(title, new_title),
            run_time=1
        )
        self.wait(0.5)
        
        # At the same time, create the state vector (copy and remove dots)
        state_vector = MathTex(
            r"\begin{bmatrix} u \\ v \\ w \\ p \\ q \\ r \\ \varphi \\ \theta \\ \psi \\ x \\ y \\ z \end{bmatrix}^{\top}",
            font_size=28
        )
        state_vector.move_to(ORIGIN)
        
        self.play(
            Write(state_vector),
            run_time=1.5
        )
        self.wait(1)
        
        # Add label "variable de estado" to state_vector
        x_label = Text("variable de estado", font_size=20, color=state_color)
        x_label.next_to(state_vector, DOWN, buff=0.3)
        
        x_arrow = Arrow(
            start=x_label.get_top(),
            end=state_vector.get_bottom(),
            buff=0.1,
            color=state_color,
            stroke_width=2
        )
        
        self.play(
            Create(x_arrow),
            Write(x_label),
            run_time=1.5
        )
        self.wait(1)
        
        # Transform state_vector into \boldsymbol{x}
        bold_x = MathTex(
            r"\boldsymbol{x}",
            font_size=40
        )
        bold_x.move_to(state_vector.get_center())
        
        self.play(
            Transform(state_vector, bold_x),
            run_time=1.5
        )
        self.wait(1)
        
        # Fade in the control vector
        control_vector = MathTex(
            r"\begin{bmatrix} \omega_1 \\ \omega_2 \\ \omega_3 \\ \omega_4 \end{bmatrix}^{\top}",
            font_size=32
        )
        control_vector.move_to(state_vector.get_center() + RIGHT * 3)
        
        self.play(FadeIn(control_vector), run_time=1.5)
        self.wait(1)
        
        # Add label "variable de control"
        u_label = Text("aceleración de rotores como variable de control", font_size=20, color=control_color)
        u_label.next_to(control_vector, DOWN, buff=0.3)
        
        u_arrow = Arrow(
            start=u_label.get_top(),
            end=control_vector.get_bottom(),
            buff=0.1,
            color=control_color,
            stroke_width=2
        )
        
        self.play(
            Create(u_arrow),
            Write(u_label),
            run_time=1.5
        )
        self.wait(1)
        
        # Transform control_vector into \boldsymbol{u}
        bold_u = MathTex(
            r"\boldsymbol{u}",
            font_size=40
        )
        bold_u.move_to(control_vector.get_center())
        
        self.play(
            Transform(control_vector, bold_u),
            run_time=1.5
        )
        self.wait(1)
        
        # Disappear all labels
        self.play(
            FadeOut(x_arrow),
            FadeOut(x_label),
            FadeOut(u_arrow),
            FadeOut(u_label),
            run_time=1
        )
        self.wait(0.5)
        
        # Merge everything into the final equation
        # Create the final equation
        state_space_eq = MathTex(
            r"\dot{\boldsymbol{x}} = \mathbf{f}(\boldsymbol{x}(t), \boldsymbol{u}(t))",
            font_size=40
        )
        state_space_eq.move_to(ORIGIN)
        
        # Move all elements to center before merging
        self.play(
            merged_lhs_vector.animate.move_to(ORIGIN),
            state_vector.animate.move_to(ORIGIN),
            control_vector.animate.move_to(ORIGIN),
            run_time=1.5
        )
        self.wait(1.0)

        # Change title
        new_new_title = Text("Sistemas de control", font_size=48, color=WHITE)
        new_new_title.to_edge(UP)
        
        self.play(
            Transform(title, new_new_title),
            run_time=1
        )
        self.wait(0.5)

        control_definition = MarkupText(
            "Es el objeto de estudio de la <b>teoría de control</b>. "
            "Son sistemas dinámicos que dependen de un\nparamétro de control que actua de forma externa.",
            font_size=24,
            color=WHITE
        )
        control_definition.next_to(new_new_title, DOWN, buff=0.3)
        
        self.play(FadeIn(control_definition), run_time=1)
        self.wait(0.5)
        
        # Merge into final equation - transform the dot_x into the full equation
        # and fade out the state and control vectors
        self.play(
            ReplacementTransform(merged_lhs_vector, state_space_eq),
            FadeOut(state_vector),
            FadeOut(control_vector),
            run_time=2
        )
        self.wait(1)
        
        # Continue with control systems content
        # Mention it's a continuous time, time-invariant system
        description = Text(
            "Sistema de control de tiempo continuo e independiente del tiempo",
            font_size=24,
            color=WHITE
        )
        description.next_to(state_space_eq, DOWN, buff=0.5)
        
        self.play(Write(description))
        self.wait(2)
        self.play(FadeOut(description))
        self.wait(0.5)
        
        # Expand as linear system
        linear_eq = MathTex(
            r"\dot{\boldsymbol{x}} = \mathbf{A}\boldsymbol{x} + \mathbf{B}\boldsymbol{u}",
            font_size=40
        )
        linear_eq.move_to(state_space_eq.get_center())
        
        matrix_dims = MathTex(
            r"\mathbf{A} \in \mathbb{R}^{n_x \times n_x},\quad \mathbf{B} \in \mathbb{R}^{n_x \times n_u}",
            font_size=28
        )
        
        linear_label = Text("Sistema lineal", font_size=24, color=WHITE)
        linear_label_group = VGroup(linear_label, matrix_dims)
        linear_label_group.arrange(DOWN, buff=0.2)
        linear_label_group.next_to(linear_eq, DOWN, buff=0.4)
        
        self.play(
            Transform(state_space_eq, linear_eq),
            Write(linear_label_group),
            run_time=1.5
        )
        self.wait(1)
        self.play(FadeOut(linear_label_group))
        self.wait(0.5)
        
        # Mention advantages
        advantages_title = Text("Ventajas de estudiar sistemas lineales:", font_size=24, color=WHITE)
        advantages_title.shift(DOWN * 1.5)
        
        advantages = VGroup(
            Text("• Linealidad", font_size=20, color=WHITE),
            Text("• Estabilidad", font_size=20, color=WHITE),
            Text("• Controlabilidad", font_size=20, color=WHITE)
        )
        advantages.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        advantages.next_to(advantages_title, DOWN, buff=0.3)
        
        self.play(Write(advantages_title))
        self.wait(0.5)
        self.play(Write(advantages), run_time=1.5)
        self.wait(2)
        
        # Fade out advantages
        self.play(
            FadeOut(advantages_title),
            FadeOut(advantages)
        )
        self.wait(0.5)
        
        # Return to continuous system (non-linear)
        nonlinear_eq = MathTex(
            r"\dot{\boldsymbol{x}} = \mathbf{f}(\boldsymbol{x}(t), \boldsymbol{u}(t))",
            font_size=40
        )
        nonlinear_eq.move_to(state_space_eq.get_center())
        
        self.play(
            Transform(state_space_eq, nonlinear_eq),
            run_time=1.5
        )
        self.wait(1)
        
        # Extract right-hand side
        rhs_extracted = MathTex(
            r"\mathbf{f}(\boldsymbol{x}(t), \boldsymbol{u}(t))",
            font_size=40
        )
        rhs_extracted.move_to(state_space_eq.get_center())
        
        linearization_title = Text(
            "Linealización de sistemas no lineales",
            font_size=26,
            color=WHITE
        )
        linearization_title.next_to(rhs_extracted, DOWN, buff=0.6)
        
        linearization_description = MarkupText(
            "Aproxima con términos de primer orden de Taylor\nalrededor de un <b>punto fijo</b>.",
            font_size=22,
            color=WHITE
        )
        linearization_description.next_to(linearization_title, DOWN, buff=0.3)
        
        fixed_point_description = MathTex(
            r"\text{Es } (\mathbf{x}^{*}, \mathbf{u}^{*}) \text{ tal que } \mathbf{f}(\mathbf{x}^{*}, \mathbf{u}^{*}) = \mathbf{0}",
            font_size=22,
            color=WHITE
        )
        fixed_point_description.next_to(linearization_description, DOWN, buff=0.3)
        
        linearization_text = VGroup(
            linearization_title,
            linearization_description,
            fixed_point_description
        )
        
        self.play(
            Transform(state_space_eq, rhs_extracted),
            Write(linearization_text),
            run_time=1.5
        )
        self.wait(1)
        self.play(FadeOut(linearization_text))
        self.wait(1.0)
        
        expanded_eq = MathTex(
            r"\mathbf{f}(\boldsymbol{x}^{*} + \boldsymbol{x} - \boldsymbol{x}^{*}, \boldsymbol{u}^{*} + \boldsymbol{u} - \boldsymbol{u}^{*})",
            font_size=34
        )
        expanded_eq.move_to(rhs_extracted.get_center())
        
        self.play(Transform(state_space_eq, expanded_eq), run_time=1.5)
        self.wait(1)
        
        # Show linearization equation
        linearization_eq = MathTex(
            r"\mathbf{f}(\mathbf{x}^{*} + \overline{\mathbf{x}}, \mathbf{u}^{*} + \overline{\mathbf{u}}) \approx ",
            r"\mathbf{f}(\mathbf{x}^{*}, \mathbf{u}^{*}) + ",
            r"\nabla_{\mathbf{x}} \mathbf{f}(\mathbf{x}^{*}, \mathbf{u}^{*}) \cdot \overline{\mathbf{x}} + ",
            r"\nabla_{\mathbf{u}}\mathbf{f}(\mathbf{x}^{*}, \mathbf{u}^{*}) \cdot \overline{\mathbf{u}}",
            font_size=32
        )
        linearization_eq.shift(DOWN * 1)
        
        self.play(Transform(state_space_eq, linearization_eq), run_time=1.5)
        self.wait(1)
        
        # Show the definitions first
        x_def = MathTex(
            r"\overline{\mathbf{x}} = \mathbf{x} - \mathbf{x}^{*}",
            font_size=28
        )
        u_def = MathTex(
            r"\overline{\mathbf{u}} = \mathbf{u} - \mathbf{u}^{*}",
            font_size=28
        )
        
        definitions = VGroup(x_def, u_def)
        definitions.arrange(DOWN, buff=0.3)
        definitions.next_to(linearization_eq, DOWN, buff=0.5)
        
        self.play(Write(definitions), run_time=1.5)
        self.wait(1.5)
        
        # Replace f(x*, u*) with 0
        linearization_eq_step2 = MathTex(
            r"\mathbf{f}(\mathbf{x}^{*} + \overline{\mathbf{x}}, \mathbf{u}^{*} + \overline{\mathbf{u}}) \approx ",
            r"\mathbf{0} + ",
            r"\nabla_{\mathbf{x}} \mathbf{f}(\mathbf{x}^{*}, \mathbf{u}^{*}) \cdot \overline{\mathbf{x}} + ",
            r"\nabla_{\mathbf{u}}\mathbf{f}(\mathbf{x}^{*}, \mathbf{u}^{*}) \cdot \overline{\mathbf{u}}",
            font_size=32
        )
        linearization_eq_step2.move_to(linearization_eq.get_center())
        
        self.play(Transform(state_space_eq, linearization_eq_step2), run_time=1.5)
        self.wait(1)
        
        # Vanish the 0 term
        linearization_eq_step3 = MathTex(
            r"\mathbf{f}(\mathbf{x}^{*} + \overline{\mathbf{x}}, \mathbf{u}^{*} + \overline{\mathbf{u}}) \approx ",
            r"\nabla_{\mathbf{x}} \mathbf{f}(\mathbf{x}^{*}, \mathbf{u}^{*}) \cdot \overline{\mathbf{x}} + ",
            r"\nabla_{\mathbf{u}}\mathbf{f}(\mathbf{x}^{*}, \mathbf{u}^{*}) \cdot \overline{\mathbf{u}}",
            font_size=32
        )
        linearization_eq_step3.move_to(linearization_eq.get_center())
        
        self.play(Transform(state_space_eq, linearization_eq_step3), run_time=1.5)
        self.wait(1)
        
        # Transform left-hand side to \dot{\mathbf{x}}
        linearization_with_dot = MathTex(
            r"\dot{\mathbf{x}} \approx ",
            r"\nabla_{\mathbf{x}} \mathbf{f}(\mathbf{x}^{*}, \mathbf{u}^{*}) \cdot \overline{\mathbf{x}} + ",
            r"\nabla_{\mathbf{u}}\mathbf{f}(\mathbf{x}^{*}, \mathbf{u}^{*}) \cdot \overline{\mathbf{u}}",
            font_size=32
        )
        linearization_with_dot.move_to(linearization_eq.get_center())
        
        self.play(Transform(state_space_eq, linearization_with_dot), run_time=1.5)
        self.wait(1.5)
        
        # Transform gradients to A and B
        linearization_ab = MathTex(
            r"\dot{\mathbf{x}} \approx ",
            r"\mathbf{A}",
            r"\overline{\mathbf{x}} + ",
            r"\mathbf{B}",
            r"\overline{\mathbf{u}}",
            font_size=32
        )
        linearization_ab.move_to(linearization_eq.get_center())
        
        self.play(Transform(state_space_eq, linearization_ab), run_time=1.5)
        self.wait(0.5)
        
        a_brace = Brace(linearization_ab[1], DOWN, buff=0.1)
        b_brace = Brace(linearization_ab[3], DOWN, buff=0.1)
        a_label = MathTex(
            r"\nabla_{\mathbf{x}} \mathbf{f}(\mathbf{x}^{*}, \mathbf{u}^{*})",
            font_size=22
        )
        b_label = MathTex(
            r"\nabla_{\mathbf{u}} \mathbf{f}(\mathbf{x}^{*}, \mathbf{u}^{*})",
            font_size=22
        )
        a_label.next_to(a_brace, DOWN, buff=0.1)
        b_label.next_to(b_brace, DOWN, buff=0.1)
        
        self.play(
            GrowFromCenter(a_brace),
            GrowFromCenter(b_brace),
            FadeIn(a_label),
            FadeIn(b_label),
            run_time=1.5
        )
        self.wait(3)
