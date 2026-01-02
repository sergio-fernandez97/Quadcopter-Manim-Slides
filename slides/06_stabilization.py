from manim import *
from manim_slides import Slide

class StabilizationSlide(Slide):
    def construct(self):
        # Title
        title = Text("Estabilización de sistemas lineales de control", font_size=40, color=WHITE)
        title.to_edge(UP)
        self.add(title)
        
        # Opening statement - simplified
        opening_text = Text(
            "Estrategias de control para sistemas lineales",
            font_size=28,
            color=WHITE
        )
        opening_text.shift(UP * 2)
        
        self.play(Write(opening_text))
        self.wait(1.5)
        self.play(FadeOut(opening_text))
        self.wait(0.5)
        
        # Definition label
        definition_label = Text("Definición:", font_size=32, color=YELLOW)
        definition_label.shift(UP * 2.5)
        
        self.play(Write(definition_label))
        self.wait(0.5)
        
        # Definition text - Problem of stabilization - simplified
        def_part1 = MathTex(
            r"\textbf{Problema de estabilización:}",
            r"\text{ encontrar }",
            r"\mathbf{K}\in \mathbb{R}^{n_u\times n_x}",
            r"\text{ tal que }",
            r"\mathbf{x}^{*}=\mathbf{0}",
            r"\text{ sea asintóticamente estable}",
            font_size=24
        )
        def_part1.shift(UP * 1.8)
        def_part1[0].set_color(YELLOW)
        
        self.play(Write(def_part1), run_time=2.5)
        self.wait(1.5)
        
        # Closed-loop equation
        closed_loop_eq = MathTex(
            r"\dot{\mathbf{x}} = (\mathbf{A} + \mathbf{BK})\mathbf{x}(t),",
            font_size=32
        )
        closed_loop_eq.shift(DOWN * 0.2)
        
        self.play(Write(closed_loop_eq), run_time=1.5)
        self.wait(1)
        
        # State feedback equation
        state_feedback_eq = MathTex(
            r"\mu(\mathbf{x}) = \mathbf{K}\mathbf{x}.",
            font_size=32
        )
        state_feedback_eq.shift(DOWN * 0.9)
        
        self.play(Write(state_feedback_eq), run_time=1.5)
        self.wait(1)
        
        def_part4 = MathTex(
            r"\mu(\mathbf{x}) = \mathbf{K}\mathbf{x}",
            r"\text{ es la }",
            r"\textbf{ley de retroalimentación de estados}",
            font_size=24
        )
        def_part4.shift(DOWN * 1.7)
        def_part4[2].set_color(YELLOW)
        
        self.play(Write(def_part4), run_time=2)
        self.wait(1.5)
        
        # Fade out definition
        self.play(
            FadeOut(definition_label),
            FadeOut(def_part1),
            FadeOut(def_part2),
            FadeOut(def_part3),
            FadeOut(def_part4),
            run_time=1
        )
        self.wait(0.5)
        
        # Move equations up
        self.play(
            closed_loop_eq.animate.shift(UP * 1.5),
            state_feedback_eq.animate.shift(UP * 1.5),
            run_time=1
        )
        self.wait(0.5)
        
        # Discussion about the closed-loop matrix - simplified
        matrix_abk = MathTex(
            r"(\mathbf{A}+\mathbf{B K})",
            r"\text{ determina la dinámica y estabilidad}",
            font_size=28
        )
        matrix_abk.shift(UP * 0.5)
        
        self.play(Write(matrix_abk), run_time=2)
        self.wait(1)
        
        # About eigenvalues and poles - simplified
        poles_text = Text(
            "Los valores propios de esta matriz se denominan polos del sistema",
            font_size=22,
            color=WHITE
        )
        poles_text.shift(DOWN * 0.8)
        
        self.play(Write(poles_text), run_time=2)
        self.wait(1.5)
        
        # Stability condition - simplified
        stability_condition = MathTex(
            r"\text{Estabilidad asintótica } \Leftrightarrow \text{ Re}(\lambda_i) < 0 \ \forall i",
            font_size=28
        )
        stability_condition.shift(DOWN * 1.8)
        
        self.play(Write(stability_condition), run_time=2)
        self.wait(1.5)
        
        # Fade out and show theorem
        self.play(
            FadeOut(matrix_abk),
            FadeOut(poles_text),
            FadeOut(stability_condition),
            FadeOut(closed_loop_eq),
            FadeOut(state_feedback_eq),
            FadeOut(def_part1),
            FadeOut(def_part4),
            run_time=1
        )
        self.wait(0.5)
        
        # Pole assignment theorem - simplified
        theorem_label = Text("Teorema de asignación de polos:", font_size=32, color=YELLOW)
        theorem_label.shift(UP * 2.5)
        
        self.play(Write(theorem_label))
        self.wait(0.5)
        
        theorem_text = MathTex(
            r"\text{Los polos pueden asignarse arbitrariamente }",
            r"\Leftrightarrow",
            r"(\mathbf{A}, \mathbf{B}) \text{ es controlable}",
            font_size=28
        )
        theorem_text.shift(UP * 1.5)
        
        self.play(Write(theorem_text), run_time=2.5)
        self.wait(1.5)
        
        # Implications - simplified
        implications_text = Text(
            "Relaciona controlabilidad y estabilidad",
            font_size=24,
            color=WHITE
        )
        implications_text.shift(DOWN * 0.5)
        
        self.play(Write(implications_text), run_time=1.5)
        self.wait(3)
        
        self.wait(3)

