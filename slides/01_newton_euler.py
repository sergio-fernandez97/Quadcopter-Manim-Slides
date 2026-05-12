"""
Newton–Euler equations for quadcopter dynamics.

Introduces the local equations of motion, highlighting Newton's second law and
their role in deriving translational and rotational dynamics for the vehicle.
Adds conceptual bridges for the rigid-body model, external forces (gravity and
thrust), the non-inertial body frame, and the transport theorem.

Example:
    manim -pql slides/01_newton_euler.py NewtonEulerSlide

Author: Sergio Fernández
Date: 2025-01-30
"""

from manim import *
from manim_slides import Slide


class NewtonEulerSlide(Slide):
    """Newton-Euler dynamics: translational and rotational equations in the body frame."""

    def construct(self):
        # Title
        title = Text("Dinámica de traslación y rotación local", font_size=40, color=YELLOW)
        title.to_edge(UP)
        self.add(title)
        self.next_slide()

        # ===========================
        # IDEA CENTRAL (NEW)
        # ===========================
        idea_label = Text("Modelo del cuadricóptero", font_size=28, color=BLUE)
        idea_label.move_to(UP * 2.5)

        idea_items = VGroup(
            Text("• Cuadricóptero modelado como un sólido rígido", font_size=22, color=WHITE),
            Text("• Las ecuaciones de Newton-Euler combinan:", font_size=22, color=WHITE),
            Text("    — traslación del centro de masa", font_size=20, color=GRAY_B),
            Text("    — rotación del cuerpo", font_size=20, color=GRAY_B),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        idea_items.next_to(idea_label, DOWN, buff=0.4)

        idea_box = RoundedRectangle(
            corner_radius=0.2,
            width=idea_items.width + 0.8,
            height=idea_items.height + 0.5,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        idea_box.move_to(idea_items)

        self.play(FadeIn(idea_label))
        self.wait(0.5)
        self.play(FadeIn(idea_box), FadeIn(idea_items))
        self.wait(0.5)
        self.next_slide()
        self.play(FadeOut(idea_label), FadeOut(idea_box), FadeOut(idea_items))
        self.wait(0.5)

        # ===========================
        # Opening statement (EXISTING)
        # ===========================
        opening_text = Text(
            "Las ecuaciones de movimiento del sistema local\nderivan de las ecuaciones de Newton-Euler.",
            font_size=22,
            color=WHITE,
            line_spacing=1.4,
        )
        opening_box = RoundedRectangle(
            corner_radius=0.2,
            width=opening_text.width + 0.6,
            height=opening_text.height + 0.4,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        opening_group = VGroup(opening_box, opening_text).arrange(ORIGIN)
        opening_group.shift(UP * 1.5)
        self.play(Write(opening_group))
        self.wait(2)
        self.next_slide()
        self.play(FadeOut(opening_group))
        self.wait(0.5)

        # Newton's second law statement - boxed
        newton_statement = Text(
            "Segunda ley de Newton",
            font_size=22,
            color=YELLOW
        )
        newton_statement.shift(UP * 2.5)

        # m·υ̇ = f  (notation consistent with the body-frame derivation)
        newton_eq_initial = MathTex(
            r"m\dot{\boldsymbol{\upsilon}} = \mathbf{f}",
            font_size=40
        )
        newton_eq_initial.shift(UP * 1.8)

        # Box for Newton's law
        newton_box = RoundedRectangle(
            corner_radius=0.2,
            width=newton_eq_initial.width + 1,
            height=newton_eq_initial.height + 0.8,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        newton_box.move_to(newton_eq_initial.get_center())

        self.play(Write(newton_statement), run_time=0.5)
        self.wait(0.5)
        self.play(Write(newton_eq_initial), Create(newton_box))
        self.wait(1)
        self.next_slide()

        # Euler's equation statement and initial equation (lower part)
        # — make explicit: torque acts on the rigid body; angular momentum is I·ω
        euler_statement = Text(
            "Segunda ley de Euler: el torque τ_B actúa sobre el momento angular Iω del cuerpo rígido",
            font_size=22,
            color=WHITE
        )
        euler_statement.shift(DOWN * 0.2)

        euler_eq_initial = MathTex(
            r"\boldsymbol{\tau}_B = \mathbf{I}\dot{\boldsymbol{\omega}} + \boldsymbol{\omega} \times (\mathbf{I}\boldsymbol{\omega})",
            font_size=40
        )
        euler_eq_initial.shift(DOWN * 1.5)

        self.play(Write(euler_statement))
        self.wait(1)
        self.play(Write(euler_eq_initial))
        self.wait(2)
        self.next_slide()

        # Fade out statements
        self.play(
            FadeOut(newton_statement),
            FadeOut(euler_statement)
        )
        self.wait(0.5)

        # Transform Newton's equation to quadcopter translation equation (upper)
        newton_eq = MathTex(
            r"\mathbf{R}^{\top}\mathbf{G} + \mathbf{T}_{B} = m\dot{\boldsymbol{\upsilon}} + \boldsymbol{\omega} \times (m \boldsymbol{\upsilon})",
            font_size=36
        )
        newton_eq.move_to(newton_eq_initial.get_center())

        # Euler's equation (already in correct form, just reposition)
        euler_eq = MathTex(
            r"\boldsymbol{\tau}_B = \mathbf{I}\dot{\boldsymbol{\omega}} + \boldsymbol{\omega} \times (\mathbf{I}\boldsymbol{\omega})",
            font_size=36
        )
        euler_eq.move_to(euler_eq_initial.get_center())

        self.play(
            Transform(newton_eq_initial, newton_eq),
            Transform(euler_eq_initial, euler_eq),
            run_time=2
        )
        self.wait(1)
        self.next_slide()

        # Update references
        newton_eq = newton_eq_initial
        euler_eq = euler_eq_initial

        # ===========================
        # FUERZAS Y MARCO NO INERCIAL (NEW)
        # ===========================
        # Shown at the bottom while the body-frame equations remain visible above.
        forces_note = VGroup(
            Text(
                "Fuerza externa neta: RᵀG (gravedad proyectada) + T_B (empuje de rotores)",
                font_size=20,
                color=GRAY_B,
            ),
            Text(
                "Marco local rota con ω → no inercial; teorema de transporte introduce −ω×(mυ).",
                font_size=20,
                color=GRAY_B,
            ),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        forces_note.to_edge(DOWN, buff=0.4)

        self.play(FadeIn(forces_note))
        self.wait(0.5)
        self.next_slide()
        self.play(FadeOut(forces_note))
        self.wait(0.3)

        # ===========================
        # LINEAR VELOCITIES (EXISTING)
        # ===========================
        # Color definitions for velocity vectors (different colors for linear and angular)
        linear_velocity_color = YELLOW
        angular_velocity_color = BLUE

        # Color velocity vectors in both equations
        newton_eq.set_color_by_tex(r"\dot{\boldsymbol{\upsilon}}", linear_velocity_color)
        euler_eq.set_color_by_tex(r"\dot{\boldsymbol{\omega}}", angular_velocity_color)

        self.wait(1)

        # Expand Newton's equation first
        translation_expanded = MathTex(
            r"m\dot{\boldsymbol{\upsilon}} + \boldsymbol{\omega} \times (m \boldsymbol{\upsilon}) = \mathbf{R}^{\top}\begin{bmatrix} 0 \\ 0 \\ -g \end{bmatrix} + \begin{bmatrix}0 \\0 \\T_z\end{bmatrix}",
            font_size=32
        )
        translation_expanded.move_to(newton_eq.get_center())
        translation_expanded.set_color_by_tex(r"\dot{\boldsymbol{\upsilon}}", linear_velocity_color)

        self.play(Transform(newton_eq, translation_expanded), run_time=1.5)
        self.wait(2)
        self.next_slide()

        upsilon_eq = MathTex(r"\dot{\boldsymbol{\upsilon}}")
        upsilon_eq.move_to(newton_eq.get_center())
        upsilon_eq.set_color_by_tex(r"\dot{\boldsymbol{\upsilon}}", linear_velocity_color)

        # FIRST: Transform Newton's equation to linear velocities
        explanation_linear = Text(
            "Despejando la aceleración lineal de la ecuación de Newton",
            font_size=20,
            color=WHITE
        )
        explanation_linear.to_edge(DOWN, buff=0.3)

        self.play(Transform(newton_eq, upsilon_eq),
            Write(explanation_linear),
            run_time=1.5
            )
        self.wait(1)

        # Transform to linear velocities
        linear_velocities = MathTex(
            r"\dot u &= rv - qw - g \sin\theta \\",
            r"\dot v &= pw - ru - g\cos\theta \cdot \sin\phi \\",
            r"\dot w &= qu - pv + g\cos\varphi \cdot \cos\theta - \frac{1}{m}T_z",
            font_size=32
        )
        linear_velocities.shift(UP * 1.2)
        # Color velocity components
        linear_velocities.set_color_by_tex(r"\dot u", linear_velocity_color)
        linear_velocities.set_color_by_tex(r"\dot v", linear_velocity_color)
        linear_velocities.set_color_by_tex(r"\dot w", linear_velocity_color)

        linear_label = Text("Velocidades lineales", font_size=24, color=linear_velocity_color)
        linear_label.next_to(linear_velocities, UP, buff=0.2)

        self.play(
            Transform(newton_eq, linear_velocities),
            Write(linear_label),
            FadeOut(explanation_linear),
            run_time=2
        )
        self.wait(1)
        self.next_slide()

        linear_velocities_expanded = MathTex(
            r"\dot u &= rv - qw - g \sin\theta \\",
            r"\dot v &= pw - ru - g\cos\theta \cdot \sin\phi \\",
            r"\dot w &= qu - pv + g\cos\varphi \cdot \cos\theta - \frac{k}{m}\sum_{i=1}^{4}\omega_i^2",
            font_size=32
        )
        linear_velocities_expanded.move_to(newton_eq.get_center())
        linear_velocities_expanded.set_color_by_tex(r"\dot u", linear_velocity_color)
        linear_velocities_expanded.set_color_by_tex(r"\dot v", linear_velocity_color)
        linear_velocities_expanded.set_color_by_tex(r"\dot w", linear_velocity_color)

        self.play(Transform(
            newton_eq,
            linear_velocities_expanded
            ),
            run_time=1.5)

        self.wait(2)
        self.next_slide()

        # Brief closing for translational dynamics (NEW)
        linear_close = Text(
            "Estas tres ecuaciones describen la dinámica de traslación en el sistema local.",
            font_size=19,
            color=GRAY_B,
        )
        linear_close.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(linear_close))
        self.wait(0.5)
        self.next_slide()
        self.play(FadeOut(linear_close))
        self.wait(0.3)

        # ===========================
        # ROTATIONAL DYNAMICS (EXISTING)
        # ===========================
        # THEN: Transform Euler's equation to angular velocities
        explanation_angular = Text(
            "Despejando la aceleración angular de la ecuación de Euler",
            font_size=20,
            color=WHITE
        )
        explanation_angular.to_edge(DOWN, buff=0.3)

        omega_eq = MathTex(r"\dot{\boldsymbol{\omega}}")
        omega_eq.move_to(euler_eq.get_center())
        omega_eq.set_color_by_tex(r"\dot{\boldsymbol{\omega}}", angular_velocity_color)

        self.play(
            Transform(euler_eq, omega_eq),
            Write(explanation_angular),
            run_time=1.5
            )
        self.wait(1)

        # Expand Euler's equation (expanded form obtained by solving for ω̇)
        rotation_expanded = MathTex(
            r"\dot{\boldsymbol{\omega}} = \mathbf{I}^{-1} \left(- \begin{bmatrix} p \\ q \\ r \end{bmatrix} \times \begin{bmatrix} I_{xx} \cdot p \\ I_{yy} \cdot q \\ I_{zz} \cdot r \end{bmatrix} + \begin{bmatrix} \tau_{\varphi} \\ \tau_{\theta} \\ \tau_{\psi} \end{bmatrix} \right)",
            font_size=28
        )
        rotation_expanded.move_to(euler_eq.get_center())
        rotation_expanded.set_color_by_tex(r"\dot{\boldsymbol{\omega}}", angular_velocity_color)

        self.play(Transform(euler_eq, rotation_expanded), run_time=1.5)
        self.wait(1)
        self.next_slide()

        # Transform to angular velocities
        angular_velocities = MathTex(
            r"\dot p &= \frac{1}{I_{xx}}\tau_{\varphi} - qr \left(\frac{I_{zz} - I_{yy}}{I_{xx}}\right) \\",
            r"\dot q &= \frac{1}{I_{yy}}\tau_{\theta} - pr \left(\frac{I_{xx} - I_{zz}}{I_{yy}}\right) \\",
            r"\dot r &= \frac{1}{I_{zz}}\tau_{\psi}",
            font_size=32
        )
        angular_velocities.shift(DOWN * 1.5)
        # Color velocity components
        angular_velocities.set_color_by_tex(r"\dot p", angular_velocity_color)
        angular_velocities.set_color_by_tex(r"\dot q", angular_velocity_color)
        angular_velocities.set_color_by_tex(r"\dot r", angular_velocity_color)

        angular_label = Text("Velocidades angulares", font_size=24, color=angular_velocity_color)
        angular_label.next_to(angular_velocities, UP, buff=0.2)

        self.play(
            Transform(euler_eq, angular_velocities),
            Write(angular_label),
            FadeOut(explanation_angular),
            run_time=2
        )
        self.wait(1)
        self.next_slide()

        angular_velocities_expanded = MathTex(
            r"\dot p &= \frac{\ell k}{I_{xx}}\left(\omega_4^2 - \omega_2^2\right)-qr \left(\frac{I_{zz} -I_{yy}}{I_{xx}}\right) \\",
            r"\dot q &= \frac{\ell k}{I_{xx}}\left(\omega_3^2 - \omega_1^2\right) - pr \left(\frac{I_{xx} -I_{zz}}{I_{yy}}\right) \\",
            r"\dot r &= \frac{b}{I_{zz}}\left(\omega_2^2 + \omega_4^2 - \omega_1^2 - \omega_3^2\right)",
            font_size=32
        )
        angular_velocities_expanded.move_to(euler_eq.get_center())
        angular_velocities_expanded.set_color_by_tex(r"\dot p", angular_velocity_color)
        angular_velocities_expanded.set_color_by_tex(r"\dot q", angular_velocity_color)
        angular_velocities_expanded.set_color_by_tex(r"\dot r", angular_velocity_color)

        self.play(Transform(
            euler_eq,
            angular_velocities_expanded
            ),
            run_time=1.5)

        self.wait(3)
        self.next_slide()

        # Brief closing for rotational dynamics (NEW)
        angular_close = Text(
            "Estas tres ecuaciones corresponden a la dinámica de rotación en el sistema local.",
            font_size=19,
            color=GRAY_B,
        )
        angular_close.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(angular_close))
        self.wait(0.5)
        self.next_slide()
