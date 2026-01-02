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
        # Title
        title = Text("Dinámica de traslación y rotación inercial", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.add(title)
        
        # Opening statement
        opening_statement = Text(
            "Las ecuaciones de movimiento del sistema inerciales\nrelacionan velocidades locales con coordenadas inerciales.",
            font_size=26,
            color=WHITE
        )
        opening_statement.shift(UP * 2)
        self.play(Write(opening_statement))
        self.wait(2)
        self.play(FadeOut(opening_statement))
        self.wait(0.5)
        
        # Translation dynamics statement and initial equation (upper part)
        translation_statement = Text(
            "Dinámica de traslación: Relación entre coordenadas inerciales y velocidades locales",
            font_size=24,
            color=WHITE
        )
        translation_statement.shift(UP * 2.5)
        
        translation_eq_initial = MathTex(
            r"\dot{\boldsymbol{q}} = \boldsymbol{\upsilon}",
            font_size=40
        )
        translation_eq_initial.shift(UP * 1.8)
        
        self.play(Write(translation_statement))
        self.wait(1)
        self.play(Write(translation_eq_initial))
        self.wait(1)
        
        # Rotation dynamics statement and initial equation (lower part)
        rotation_statement = Text(
            "Dinámica de rotación: La velocidad angular inercial se relaciona con la angular local\n mediante una transformación.",
            font_size=24,
            color=WHITE
        )
        rotation_statement.shift(DOWN * 0.2)
        
        rotation_eq_initial = MathTex(
            r"\dot{\boldsymbol{\eta}} = \mathbf{W}_{\boldsymbol{\omega} \rightarrow \boldsymbol{\eta}}\boldsymbol{\omega}",
            font_size=36
        )
        rotation_eq_initial.shift(DOWN * 1.5)
        
        self.play(Write(rotation_statement))
        self.wait(1)
        self.play(Write(rotation_eq_initial))
        self.wait(2)
        
        # Fade out statements
        self.play(
            FadeOut(translation_statement),
            FadeOut(rotation_statement)
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
            r"\dot{\boldsymbol{\eta}} = \mathbf{W}_{\boldsymbol{\omega} \rightarrow \boldsymbol{\eta}}\boldsymbol{\omega}",
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
        self.wait(2.0)
        
        # Expand the rotation equation to show the full form with matrix
        rotation_expanded = MathTex(
            r"\begin{bmatrix} \dot{\varphi} \\ \dot{\theta} \\ \dot{\psi} \end{bmatrix} = "
            r"\begin{bmatrix}"
            r"1 & S_{\varphi}T_{\theta} & C_{\varphi}T_{\theta} \\"
            r"0 & C_{\varphi} & -S_{\varphi} \\"
            r"0 & S_{\varphi}/C_{\theta} & C_{\varphi}/C_{\theta}"
            r"\end{bmatrix}"
            r"\begin{bmatrix} p \\ q \\ r \end{bmatrix}",
            font_size=28
        )
        rotation_expanded.move_to(rotation_eq.get_center())
        rotation_expanded.shift(UP * 0.3)
        
        self.play(
            Transform(rotation_eq, rotation_expanded),
            run_time=2
        )
        self.wait(0.5)
        
        # Create brace under the matrix part (the matrix is part of the MathTex)
        # We'll create a brace that spans the matrix portion
        # The matrix bmatrix is typically the second part (index 1) in the MathTex
        # Create a brace below the entire equation, then position it to point at the matrix
        matrix_brace = Brace(rotation_expanded, DOWN, buff=0.1)
        matrix_label_expanded = matrix_brace.get_text(
            "Matriz de cambio de coordenadas de la velocidad angular"
        )
        
        self.play(
            Create(matrix_brace),
            Write(matrix_label_expanded),
            run_time=1.5
        )
        self.wait(1.5)
        self.play(
            FadeOut(matrix_brace),
            FadeOut(matrix_label_expanded),
            run_time=1
        )
        self.wait(0.5)
        
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
        self.wait(2)
        
        # Expand translation equation
        translation_expanded = MathTex(
            r"\begin{bmatrix} \dot{x} \\ \dot{y} \\ \dot{z} \end{bmatrix} = "
            r"\begin{bmatrix} u \\ v \\ w \end{bmatrix}",
            font_size=36
        )
        translation_expanded.move_to(translation_eq.get_center())
        translation_expanded.set_color_by_tex(r"\begin{bmatrix} u \\ v \\ w \end{bmatrix}", linear_velocity_color)
        
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
        self.wait(2)
        
        self.wait(3)

