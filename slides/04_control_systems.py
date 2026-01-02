"""
Control system formulation for the quadcopter model.

Transitions from continuous-time dynamics to a discrete-time representation,
introducing the control vector and state updates used in later slides.

Example:
    manim -pql slides/04_control_systems.py ControlSystemsSlide

Author: Sergio Fernández
Date: 2025-01-30
"""

from manim import *
from manim_slides import Slide

class ControlSystemsSlide(Slide):
    def construct(self):
        # Title
        title = Text("Sistemas de control", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.add(title)
        
        # Recover the differential equation from previous slide
        state_space_eq = MathTex(
            r"\dot{\boldsymbol{x}} = \mathbf{f}(\boldsymbol{x}(t), \boldsymbol{u}(t))",
            font_size=40
        )
        state_space_eq.shift(UP * 2)
        
        self.play(Write(state_space_eq))
        self.wait(1)
        
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
        
        # Transform to discrete time system
        discrete_eq = MathTex(
            r"\boldsymbol{x}_{k+1} = \mathbf{f}(\boldsymbol{x}_k, \boldsymbol{u}_k)",
            font_size=40
        )
        discrete_eq.move_to(state_space_eq.get_center())
        
        discrete_label = Text(
            "Sistema de tiempo discreto",
            font_size=24,
            color=WHITE
        )
        discrete_label.next_to(discrete_eq, DOWN, buff=0.5)
        
        self.play(
            Transform(state_space_eq, discrete_eq),
            Write(discrete_label),
            run_time=1.5
        )
        self.wait(2)
        self.play(FadeOut(discrete_label))
        self.wait(0.5)
        
        # Transform back to continuous
        continuous_eq = MathTex(
            r"\dot{\boldsymbol{x}} = \mathbf{f}(\boldsymbol{x}(t), \boldsymbol{u}(t))",
            font_size=40
        )
        continuous_eq.move_to(state_space_eq.get_center())
        
        self.play(Transform(state_space_eq, continuous_eq), run_time=1.5)
        self.wait(1)
        
        # Expand as linear system
        linear_eq = MathTex(
            r"\dot{\mathbf{x}} = \mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{u}",
            font_size=40
        )
        linear_eq.move_to(state_space_eq.get_center())
        
        # Add tag
        linear_tag = MathTex(r"\tag{1}", font_size=32)
        linear_tag.next_to(linear_eq, RIGHT, buff=0.3)
        
        # Add label "Sistema lineal"
        linear_label = Text("Sistema lineal", font_size=24, color=WHITE)
        linear_label.next_to(linear_eq, DOWN, buff=0.4)
        
        self.play(
            Transform(state_space_eq, linear_eq),
            Write(linear_tag),
            Write(linear_label),
            run_time=1.5
        )
        self.wait(1)
        self.play(FadeOut(linear_label))
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
            FadeOut(linear_tag),
            run_time=1.5
        )
        self.wait(1)
        
        # Extract right-hand side
        rhs_extracted = MathTex(
            r"\mathbf{f}(\boldsymbol{x}(t), \boldsymbol{u}(t))",
            font_size=40
        )
        rhs_extracted.move_to(state_space_eq.get_center())
        
        rhs_description = Text(
            "Proceso de linealización de un sistema continuo:",
            font_size=24,
            color=WHITE
        )
        rhs_description.next_to(rhs_extracted, DOWN, buff=0.8)
        
        self.play(
            Transform(state_space_eq, rhs_extracted),
            Write(rhs_description),
            run_time=1.5
        )
        self.wait(1)
        self.play(FadeOut(rhs_description))
        
        # Show linearization equation
        linearization_eq = MathTex(
            r"\mathbf{f}(\mathbf{x}^{*} + \overline{\mathbf{x}}, \mathbf{u}^{*} + \overline{\mathbf{u}}) \approx ",
            r"\mathbf{f}(\mathbf{x}^{*}, \mathbf{u}^{*}) + ",
            r"\nabla_{\mathbf{x}} \mathbf{f}(\mathbf{x}^{*}, \mathbf{u}^{*}) \cdot \overline{\mathbf{x}} + ",
            r"\nabla_{\mathbf{u}}\mathbf{f}(\mathbf{x}^{*}, \mathbf{u}^{*}) \cdot \overline{\mathbf{u}}",
            font_size=32
        )
        linearization_eq.shift(DOWN * 1)
        
        self.play(Write(linearization_eq), run_time=2)
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
        
        self.play(Transform(linearization_eq, linearization_eq_step2), run_time=1.5)
        self.wait(1)
        
        # Vanish the 0 term
        linearization_eq_step3 = MathTex(
            r"\mathbf{f}(\mathbf{x}^{*} + \overline{\mathbf{x}}, \mathbf{u}^{*} + \overline{\mathbf{u}}) \approx ",
            r"\nabla_{\mathbf{x}} \mathbf{f}(\mathbf{x}^{*}, \mathbf{u}^{*}) \cdot \overline{\mathbf{x}} + ",
            r"\nabla_{\mathbf{u}}\mathbf{f}(\mathbf{x}^{*}, \mathbf{u}^{*}) \cdot \overline{\mathbf{u}}",
            font_size=32
        )
        linearization_eq_step3.move_to(linearization_eq.get_center())
        
        self.play(Transform(linearization_eq, linearization_eq_step3), run_time=1.5)
        self.wait(1)
        
        # Transform gradients to A and B
        linearization_final = MathTex(
            r"\mathbf{f}(\mathbf{x}^{*} + \overline{\mathbf{x}}, \mathbf{u}^{*} + \overline{\mathbf{u}}) \approx ",
            r"\mathbf{A} \cdot \overline{\mathbf{x}} + ",
            r"\mathbf{B} \cdot \overline{\mathbf{u}}",
            font_size=32
        )
        linearization_final.move_to(linearization_eq.get_center())
        
        self.play(Transform(linearization_eq, linearization_final), run_time=1.5)
        self.wait(1.5)
        
        # Transform left-hand side to \dot{\mathbf{x}}
        linearization_with_dot = MathTex(
            r"\dot{\mathbf{x}} \approx ",
            r"\mathbf{A} \cdot \overline{\mathbf{x}} + ",
            r"\mathbf{B} \cdot \overline{\mathbf{u}}",
            font_size=32
        )
        linearization_with_dot.move_to(linearization_eq.get_center())
        
        self.play(Transform(linearization_eq, linearization_with_dot), run_time=1.5)
        self.wait(2)
        
        # Highlight and label fixed points
        fixed_point_label = Text(
            "Puntos fijos:",
            font_size=24,
            color=YELLOW
        )
        fixed_point_label.next_to(definitions, DOWN, buff=0.5)
        
        x_star_label = MathTex(
            r"\mathbf{x}^{*}",
            font_size=32,
            color=YELLOW
        )
        u_star_label = MathTex(
            r"\mathbf{u}^{*}",
            font_size=32,
            color=YELLOW
        )
        
        fixed_points = VGroup(x_star_label, u_star_label)
        fixed_points.arrange(RIGHT, buff=1)
        fixed_points.next_to(fixed_point_label, DOWN, buff=0.3)
        
        self.play(Write(fixed_point_label))
        self.wait(0.5)
        self.play(Write(fixed_points), run_time=1.5)
        self.wait(1)
        
        # Note: We can't easily highlight specific parts after transformations
        # The fixed points are already shown in the labels above
        
        self.wait(3)

