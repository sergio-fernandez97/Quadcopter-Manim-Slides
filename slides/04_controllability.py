"""
Controllability concepts for the quadcopter control model.

Defines controllability for linear systems, presents the algebraic criteria,
and illustrates state reachability within the slide sequence.

Example:
    manim -pql slides/04_controllability.py ControllabilitySlide

Author: Sergio Fernández
Date: 2025-01-30
"""

from manim import *
from manim_slides import Slide

class ControllabilitySlide(Slide):
    def construct(self):
        # Title
        title = Text("Controlabilidad", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.add(title)
        self.next_slide()

        # Opening statement
        statement = Text(
            "Es la propiedad de un sistema de control que determina si puede\n"
            "alcanzar un estado en particular.",
            font_size=28,
            color=WHITE
        )
        statement.shift(UP * 2.5)
        
        self.play(Write(statement))
        self.wait(2)
        self.next_slide()
        self.play(FadeOut(statement))
        self.wait(0.5)

        # Definition text
        definition_label = Text("Definición:", font_size=32, color=YELLOW)
        definition_label.shift(UP * 2.5)
        
        self.play(Write(definition_label))
        self.wait(0.5)
        
        # Definition content - using MathTex with text mode for better formatting
        definition_part1 = MathTex(
            r"\text{Considerando el sistema de control lineal }",
            r"\dot{\mathbf{x}} = \mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{u}, \text{ un estado }",
            r"\mathbf{x}_0 \in \mathbb{R}^{n_x}",
            r"\text{ se dice que es }",
            font_size=22
        )
        definition_part1.shift(UP * 1.8)
        
        definition_part2 = MathTex(
            r"\textbf{controlable}",
            r"\text{ al estado }",
            r"\mathbf{x}_1 \in \mathbb{R}^{n_x}",
            r"\text{ en el tiempo }",
            r"t_1 > 0,",
            font_size=22
        )
        definition_part2.shift(UP * 1.2)
        definition_part2[0].set_color(YELLOW)  # Highlight "controlable"
        
        definition_part3 = MathTex(
            r"\text{si existe }",
            r"\mathbf{u} \in \mathcal{U}",
            r"\text{ tal que}",
            font_size=22
        )
        definition_part3.shift(UP * 0.5)
        
        # The equation - centered
        controllability_eq = MathTex(
            r"\mathbf{x}_1 = \mathbf{x}(t_1; \mathbf{x}_0, \mathbf{u}),",
            font_size=36
        )
        controllability_eq.shift(DOWN * 0.2)
        
        definition_part4 = MathTex(
            r"\text{donde }",
            r"\mathbf{x}(t_1; \mathbf{x}_0, \mathbf{u})",
            r"\text{ representa una solución particular}",
            font_size=22
        )
        definition_part4.shift(DOWN * 0.9)
        
        definition_part5 = MathTex(
            r"\text{de la forma }",
            r"\mathbf{x}(t) = e^{\mathbf{A}t}\mathbf{x}_0 + \int_0^t e^{\mathbf{A}(t-\tau)}\mathbf{B}\mathbf{u}(\tau) d\tau.",
            font_size=20
        )
        definition_part5.shift(DOWN * 1.6)
        
        definition_part6 = MathTex(
            r"\text{En este caso, }",
            r"\mathbf{x}_1",
            r"\text{ es llamado estado }",
            r"\textbf{alcanzable}",
            r"\text{ desde }",
            r"\mathbf{x}_0",
            r"\text{ al tiempo }",
            r"t_1.",
            font_size=22
        )
        definition_part6.shift(DOWN * 2.3)
        definition_part6[3].set_color(YELLOW)  # Highlight "alcanzable"
        
        # Create box for definition
        definition_box = RoundedRectangle(
            corner_radius=0.2,
            width=12,
            height=5.5,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1
        )
        definition_box.shift(DOWN * 0.3)

        self.play(FadeIn(definition_box))

        # Show definition parts
        self.play(Write(definition_part1), run_time=2)
        self.wait(1)
        self.next_slide()
        self.play(Write(definition_part2), run_time=2)
        self.wait(1)
        self.next_slide()
        self.play(Write(definition_part3), run_time=1.5)
        self.wait(0.5)
        self.play(Write(controllability_eq), run_time=1.5)
        self.wait(1)
        self.next_slide()
        self.play(Write(definition_part4), run_time=2)
        self.wait(0.5)
        self.play(Write(definition_part5), run_time=2.5)
        self.wait(1)
        self.next_slide()
        self.play(Write(definition_part6), run_time=2.5)
        self.wait(2)
        self.next_slide()

        # Fade out the definition
        self.play(
            FadeOut(definition_label),
            FadeOut(definition_box),
            FadeOut(definition_part1),
            FadeOut(definition_part2),
            FadeOut(definition_part3),
            FadeOut(controllability_eq),
            FadeOut(definition_part4),
            FadeOut(definition_part5),
            FadeOut(definition_part6),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Creatively present the controllability matrix
        matrix_title = Text("Matriz de Controlabilidad", font_size=32, color=YELLOW)
        matrix_title.shift(UP * 2.5)
        
        self.play(Write(matrix_title))
        self.wait(1)
        
        # Show the matrix notation step by step - build centered
        R_label = MathTex(r"R(\mathbf{A}, \mathbf{B})", font_size=36, color=WHITE)
        R_label.shift(UP * 1.5)
        
        self.play(Write(R_label))
        self.wait(0.5)
        
        equals_sign = MathTex(r"=", font_size=36)
        equals_sign.next_to(R_label, RIGHT, buff=0.3)
        
        self.play(Write(equals_sign))
        self.wait(0.5)
        
        # Build the matrix column by column
        B_col = MathTex(r"\mathbf{B}", font_size=32)
        B_col.next_to(equals_sign, RIGHT, buff=0.3)
        
        self.play(Write(B_col))
        self.wait(0.8)
        
        AB_col = MathTex(r"\mathbf{AB}", font_size=32)
        AB_col.next_to(B_col, RIGHT, buff=0.4)
        
        self.play(Write(AB_col))
        self.wait(0.8)
        
        dots = MathTex(r"\cdots", font_size=32)
        dots.next_to(AB_col, RIGHT, buff=0.4)
        
        self.play(Write(dots))
        self.wait(0.8)
        
        A_power_col = MathTex(r"\mathbf{A}^{n_x - 1}\mathbf{B}", font_size=32)
        A_power_col.next_to(dots, RIGHT, buff=0.4)
        
        self.play(Write(A_power_col))
        self.wait(1)
        
        # Combine into full matrix - centered
        matrix_full = MathTex(
            r"R(\mathbf{A}, \mathbf{B}) = ",
            r"\left(\mathbf{B}\ \mathbf{AB}\ \cdots\ \mathbf{A}^{n_x - 1}\mathbf{B}\right)",
            r"\in \mathbb{R}^{n_x \times n_u \cdot n_x}",
            font_size=32
        )
        matrix_full.shift(UP * 1.5)
        
        # Group all the step-by-step elements
        matrix_parts = VGroup(R_label, equals_sign, B_col, AB_col, dots, A_power_col)
        
        self.play(
            Transform(matrix_parts, matrix_full),
            run_time=2
        )
        self.wait(2)
        self.next_slide()

        # Transform to theorem
        theorem_label = Text("Teorema (Criterio de Kalman):", font_size=32, color=YELLOW)
        theorem_label.shift(UP * 2.5)
        
        self.play(
            Transform(matrix_title, theorem_label),
            run_time=1
        )
        self.wait(0.5)
        
        # Create box for theorem
        theorem_box = RoundedRectangle(
            corner_radius=0.2,
            width=11,
            height=3,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1
        )
        theorem_box.shift(UP * 0.5)

        self.play(FadeIn(theorem_box))

        # Theorem statement - first part
        theorem_part1 = MathTex(
            r"\text{El sistema }",
            r"\dot{\mathbf{x}} = \mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{u}",
            r"\text{ es completamente controlable si y sólo si}",
            font_size=22
        )
        theorem_part1.shift(UP * 1.5)

        self.play(
            FadeOut(matrix_parts),
            Write(theorem_part1),
            run_time=2
        )
        self.wait(1)
        self.next_slide()

        # The rank condition - centered
        rank_condition = MathTex(
            r"\text{rank}(R(\mathbf{A}, \mathbf{B})) = n_x.",
            font_size=36
        )
        rank_condition.shift(UP * 0.5)

        self.play(Write(rank_condition), run_time=1.5)
        self.wait(1)
        self.next_slide()

        # Final statement - centered
        theorem_part2 = MathTex(
            r"\text{En este caso, la pareja de matrices }",
            r"(\mathbf{A}, \mathbf{B})",
            r"\text{ se denomina }",
            r"\textbf{controlable}.",
            font_size=22
        )
        theorem_part2.shift(DOWN * 0.5)
        theorem_part2[3].set_color(YELLOW)  # Highlight "controlable"

        self.play(Write(theorem_part2), run_time=2)
        self.wait(3)
        self.next_slide()
