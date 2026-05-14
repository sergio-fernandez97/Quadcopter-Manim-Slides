"""
Inertial coordinate dynamics and their relation to local velocities.

Shows how inertial translation and rotation equations connect to local motion,
setting up the bridge between coordinate systems for the quadcopter model.

Example:
    manim -pql slides/02_inertial_dynamics.py InertialDynamicsSlide

Author: Sergio Fernández
Date: 2025-01-30
"""

from manim import *
from manim_slides import Slide

class InertialDynamicsSlide(Slide):
    def construct(self):
        # Title - updated to YELLOW per CLAUDE.md style
        title = Text("Dinámica de traslación y rotación inercial", font_size=42, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))
        self.next_slide()

        # --- Idea central (NEW) ---
        idea_items = BulletedList(
            "No se introducen nuevas fuerzas ni torques",
            "Conecta velocidades angulares locales $(p,q,r)$ con tasas de Euler $(\\dot{\\varphi},\\dot{\\theta},\\dot{\\psi})$",
            "Conecta velocidades lineales locales $(u,v,w)$ con derivadas de posición $(\\dot{x},\\dot{y},\\dot{z})$",
            font_size=24,
        )
        idea_label = Text("Idea central", font_size=32, color=BLUE)
        idea_label.next_to(idea_items, UP, buff=0.3)
        idea_box = RoundedRectangle(
            corner_radius=0.2,
            width=idea_items.width + 0.8,
            height=idea_items.height + 0.6,
            color=BLUE_D,
            fill_opacity=0.12,
            stroke_width=1.5,
        )
        idea_box.move_to(idea_items)
        idea_group = VGroup(idea_label, idea_box, idea_items)
        idea_group.next_to(title, DOWN, buff=0.5)

        self.play(FadeIn(idea_group))
        self.wait(0.5)
        self.next_slide()
        self.play(FadeOut(idea_group))
        self.wait(0.3)

        # Opening statement - boxed content per CLAUDE.md
        opening_text = Text(
            "Las ecuaciones de movimiento del sistema inercial\nrelacionan velocidades locales con coordenadas inerciales.",
            font_size=22,
            color=WHITE,
            line_spacing=1.4,
        )
        opening_box = RoundedRectangle(
            corner_radius=0.2,
            width=opening_text.width + 0.6,
            height=opening_text.height + 0.4,
            color=BLUE_D,
            fill_opacity=0.12,
            stroke_width=1.5,
        )
        opening_group = VGroup(opening_box, opening_text).arrange(ORIGIN)
        opening_group.shift(UP * 2)

        self.play(FadeIn(opening_group))
        self.wait(0.5)
        self.next_slide()
        self.play(FadeOut(opening_group))
        self.wait(0.5)

        # Translation dynamics statement and initial equation (upper part)
        translation_statement = Text(
            "Dinámica de traslación: Relación entre coordenadas inerciales y velocidades locales",
            font_size=22,
            color=WHITE,
        )
        translation_stmt_box = RoundedRectangle(
            corner_radius=0.2,
            width=translation_statement.width + 0.6,
            height=translation_statement.height + 0.4,
            color=BLUE_D,
            fill_opacity=0.12,
            stroke_width=1.5,
        )
        translation_statement_group = VGroup(translation_stmt_box, translation_statement).arrange(ORIGIN)
        translation_statement_group.shift(UP * 2.5)

        translation_eq_initial = MathTex(
            r"\dot{\boldsymbol{q}} = \boldsymbol{\upsilon}",
            font_size=40
        )
        translation_eq_initial.shift(UP * 1.8)

        self.play(FadeIn(translation_statement_group))
        self.wait(0.5)
        self.play(FadeIn(translation_eq_initial))
        self.wait(0.5)
        self.next_slide()

        # Rotation dynamics statement and initial equation (lower part)
        rotation_statement = Text(
            "Dinámica de rotación: La velocidad angular inercial se relaciona con la angular local\nmediante una transformación.",
            font_size=22,
            color=WHITE,
            line_spacing=1.3,
        )
        rotation_stmt_box = RoundedRectangle(
            corner_radius=0.2,
            width=rotation_statement.width + 0.6,
            height=rotation_statement.height + 0.4,
            color=BLUE_D,
            fill_opacity=0.12,
            stroke_width=1.5,
        )
        rotation_statement_group = VGroup(rotation_stmt_box, rotation_statement).arrange(ORIGIN)
        rotation_statement_group.shift(DOWN * 0.2)

        rotation_eq_initial = MathTex(
            r"\dot{\boldsymbol{\eta}} = \mathbf{W}_{\boldsymbol{\eta}}\boldsymbol{\omega}",
            font_size=36
        )
        rotation_eq_initial.shift(DOWN * 1.5)

        self.play(FadeIn(rotation_statement_group))
        self.wait(0.5)
        self.play(FadeIn(rotation_eq_initial))
        self.wait(0.5)
        self.next_slide()

        # Fade out statements
        self.play(
            FadeOut(translation_statement_group),
            FadeOut(rotation_statement_group)
        )
        self.wait(0.5)

        # Color definitions for velocity vectors (different colors for linear and angular)
        linear_velocity_color = YELLOW
        angular_velocity_color = BLUE

        # Color velocity vectors in both equations
        translation_eq_initial.set_color_by_tex(r"\boldsymbol{\upsilon}", linear_velocity_color)
        rotation_eq_initial.set_color_by_tex(r"\dot{\boldsymbol{\eta}}", angular_velocity_color)
        rotation_eq_initial.set_color_by_tex(r"\boldsymbol{\omega}", angular_velocity_color)

        self.wait(1)

        # Update references
        translation_eq = translation_eq_initial
        rotation_eq = rotation_eq_initial


        # Transform rotation equation to include the matrix
        rotation_eq_with_matrix = MathTex(
            r"\dot{\boldsymbol{\eta}} = \mathbf{W}_{\boldsymbol{\eta}}\boldsymbol{\omega}",
            font_size=36
        )
        rotation_eq_with_matrix.move_to(rotation_eq.get_center())
        rotation_eq_with_matrix.set_color_by_tex(r"\dot{\boldsymbol{\eta}}", angular_velocity_color)
        rotation_eq_with_matrix.set_color_by_tex(r"\boldsymbol{\omega}", angular_velocity_color)

        self.play(
            Transform(rotation_eq, rotation_eq_with_matrix),
            run_time=1.5
        )
        self.wait(1)

        # Move rotation equation up to make room for matrix
        self.play(
            rotation_eq.animate.shift(UP * 0.8),
            run_time=1
        )
        self.wait(0.5)
        self.next_slide()

        # Expand the rotation equation to show the full form with matrix
        rotation_expanded = MathTex(
            r"\begin{bmatrix} \dot{\varphi} \\ \dot{\theta} \\ \dot{\psi} \end{bmatrix} = "
            r"\begin{bmatrix}"
            r"1 & \sin\varphi\tan\theta & \cos\varphi\tan\theta \\"
            r"0 & \cos\varphi & -\sin\varphi \\"
            r"0 & \dfrac{\sin\varphi}{\cos\theta} & \dfrac{\cos\varphi}{\cos\theta}"
            r"\end{bmatrix}"
            r"\begin{bmatrix} p \\ q \\ r \end{bmatrix}",
            font_size=26
        )
        rotation_expanded.move_to(rotation_eq.get_center())
        rotation_expanded.shift(UP * 0.3)

        self.play(
            Transform(rotation_eq, rotation_expanded),
            run_time=2
        )
        self.wait(0.5)

        matrix_note = Text(
            "W_η: matriz de cambio de coordenadas de la velocidad angular",
            font_size=18,
            color=GRAY_A,
        )
        matrix_note_box = RoundedRectangle(
            corner_radius=0.15,
            width=matrix_note.width + 0.5,
            height=matrix_note.height + 0.35,
            color=BLUE_D,
            fill_opacity=0.12,
            stroke_width=1.5,
        )
        matrix_note_group = VGroup(matrix_note_box, matrix_note).arrange(ORIGIN)
        matrix_note_group.next_to(rotation_expanded, DOWN, buff=0.35)

        self.play(FadeIn(matrix_note_group))
        self.wait(1.5)
        self.next_slide()
        self.play(FadeOut(matrix_note_group), run_time=1)
        self.wait(0.5)

        # --- W_eta conceptual note (NEW) ---
        # Added after the brace is removed, before expanding to explicit Euler equations
        w_eta_line1 = VGroup(
            MathTex(r"\mathbf{W}_{\boldsymbol{\eta}}", font_size=20, color=GRAY_B),
            Text(" transforma la velocidad angular local al sistema inercial.", font_size=20, color=GRAY_B),
        ).arrange(RIGHT, buff=0.1)
        w_eta_line2 = Text(
            "El lado izquierdo es un sistema de EDO de primer orden para los ángulos de Euler.",
            font_size=20,
            color=GRAY_B,
        )
        w_eta_note = VGroup(w_eta_line1, w_eta_line2).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        w_eta_note.next_to(rotation_eq, DOWN, buff=0.5)

        self.play(FadeIn(w_eta_note))
        self.wait(0.5)
        self.next_slide()
        self.play(FadeOut(w_eta_note))
        self.wait(0.3)

        # Expand rotation equation to show explicit Euler angle rates
        rotation_final = MathTex(
            r"\dot{\varphi} &= p + (q \sin\varphi + r \cos\varphi) \tan\theta \\",
            r"\dot{\theta} &= q \cos\varphi - r \sin\varphi \\",
            r"\dot{\psi} &= \left(q \sin\varphi + r \cos\varphi\right) \sec\theta",
            font_size=32
        )
        rotation_final.move_to(rotation_eq.get_center())
        # Color the derivative terms
        rotation_final.set_color_by_tex(r"\dot{\varphi}", angular_velocity_color)
        rotation_final.set_color_by_tex(r"\dot{\theta}", angular_velocity_color)
        rotation_final.set_color_by_tex(r"\dot{\psi}", angular_velocity_color)

        self.play(Transform(rotation_eq, rotation_final), run_time=2)
        self.wait(0.5)

        # --- Euler kinematics note (NEW) ---
        # Added after explicit Euler angle rate equations are shown
        euler_note = Text(
            "Estas ecuaciones describen la cinemática rotacional en el sistema inercial.",
            font_size=20,
            color=GRAY_B,
        )
        euler_note.next_to(rotation_eq, DOWN, buff=0.5)

        self.play(FadeIn(euler_note))
        self.wait(0.5)
        self.next_slide()
        self.play(FadeOut(euler_note))
        self.wait(0.3)

        # Expand translation equation
        translation_expanded = MathTex(
            r"\begin{bmatrix} \dot{x} \\ \dot{y} \\ \dot{z} \end{bmatrix} = "
            r"\begin{bmatrix} u \\ v \\ w \end{bmatrix}",
            font_size=36
        )
        translation_expanded.move_to(translation_eq.get_center())
        translation_expanded.set_color_by_tex(r"u", linear_velocity_color)
        translation_expanded.set_color_by_tex(r"v", linear_velocity_color)
        translation_expanded.set_color_by_tex(r"w", linear_velocity_color)

        self.play(Transform(translation_eq, translation_expanded), run_time=1.5)
        self.wait(1)

        # Transform to individual equation form
        translation_equations = MathTex(
            r"\dot{x} &= u \\",
            r"\dot{y} &= v \\",
            r"\dot{z} &= w",
            font_size=36
        )
        translation_equations.move_to(translation_eq.get_center())
        # Color the velocity components
        translation_equations.set_color_by_tex(r"u", linear_velocity_color)
        translation_equations.set_color_by_tex(r"v", linear_velocity_color)
        translation_equations.set_color_by_tex(r"w", linear_velocity_color)

        self.play(Transform(translation_eq, translation_equations), run_time=1.5)
        self.wait(0.5)

        no_new_law_text = Text(
            "No aparece una nueva\nley dinámica:\nu, v, w son simplemente\nlas derivadas temporales\nde x, y, z.",
            font_size=18,
            color=WHITE,
            line_spacing=1.3,
        )
        no_new_law_box = RoundedRectangle(
            corner_radius=0.2,
            width=no_new_law_text.width + 0.5,
            height=no_new_law_text.height + 0.4,
            color=BLUE_D,
            fill_opacity=0.12,
            stroke_width=1.5,
        )
        no_new_law_group = VGroup(no_new_law_box, no_new_law_text).arrange(ORIGIN)
        no_new_law_group.next_to(translation_eq, LEFT, buff=0.6)

        self.play(FadeIn(no_new_law_group))
        self.next_slide()
        self.play(FadeOut(no_new_law_group))
        self.wait(0.3)

        closing_text = Text(
            "Junto con la dinámica local, estas relaciones completan\n"
            "el sistema de ecuaciones de movimiento de primer orden.",
            font_size=20,
            color=GRAY_A,
            line_spacing=1.3,
        )
        closing_box = RoundedRectangle(
            corner_radius=0.2,
            width=closing_text.width + 0.6,
            height=closing_text.height + 0.4,
            color=BLUE_D,
            fill_opacity=0.12,
            stroke_width=1.5,
        )
        closing_group = VGroup(closing_box, closing_text).arrange(ORIGIN)
        closing_group.to_edge(DOWN, buff=0.3)

        self.play(FadeIn(closing_group), run_time=1)
        self.next_slide()
        self.play(FadeOut(closing_group), run_time=0.8)
        self.wait(1)
