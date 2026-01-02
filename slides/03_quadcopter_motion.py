"""
Combined equations of motion for the quadcopter.

Contrasts local and inertial system equations, then reframes them into a
state-space representation for control analysis.

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
        
        # Fade out the titles and equations
        self.play(
            FadeOut(local_title),
            FadeOut(inertial_title),
            FadeOut(local_linear),
            FadeOut(local_angular),
            FadeOut(inertial_linear),
            FadeOut(inertial_angular)
        )
        self.wait(0.5)
        
        # Transform to state-space form
        state_space_eq = MathTex(
            r"\dot{\boldsymbol{x}} = \mathbf{f}(\boldsymbol{x}(t), \boldsymbol{u}(t))",
            font_size=40
        )
        state_space_eq.shift(UP * 1.5)
        
        self.play(Write(state_space_eq))
        self.wait(1)
        
        # Change title
        new_title = Text("Cuadricoptero como sistema de control", font_size=48, color=WHITE)
        new_title.to_edge(UP)
        
        self.play(
            Transform(title, new_title),
            run_time=1
        )
        self.wait(1)
        
        # Label x as "variable de estado"
        # Use a simple text label positioned below the left side of the equation
        x_label = Text("variable de estado", font_size=18, color=state_color)
        x_label.next_to(state_space_eq, DOWN, buff=0.3)
        x_label.shift(LEFT * 2.5)  # Position under the \dot{\boldsymbol{x}} part
        
        # Create an arrow or line pointing to x
        x_arrow = Arrow(
            start=x_label.get_top(),
            end=state_space_eq.get_bottom() + LEFT * 2.5,
            buff=0.1,
            color=state_color,
            stroke_width=2
        )
        
        self.play(
            Create(x_arrow),
            Write(x_label),
            run_time=1.5
        )
        self.wait(1.5)
        
        self.play(
            FadeOut(x_arrow),
            FadeOut(x_label),
            run_time=0.5
        )
        
        # Transform u to vector of omega_i
        state_space_with_omega = MathTex(
            r"\dot{\boldsymbol{x}} = \mathbf{f}\left(\boldsymbol{x}(t), \begin{bmatrix} \omega_1 \\ \omega_2 \\ \omega_3 \\ \omega_4 \end{bmatrix}\right)",
            font_size=36
        )
        state_space_with_omega.move_to(state_space_eq.get_center())
        
        self.play(Transform(state_space_eq, state_space_with_omega), run_time=1.5)
        self.wait(1)
        
        # Label as "variable de control"
        # Use a simple text label positioned below the right side of the equation
        u_label = Text("variable de control", font_size=18, color=control_color)
        u_label.next_to(state_space_eq, DOWN, buff=0.3)
        u_label.shift(RIGHT * 2.5)  # Position under the omega vector part
        
        # Create an arrow or line pointing to u
        u_arrow = Arrow(
            start=u_label.get_top(),
            end=state_space_eq.get_bottom() + RIGHT * 2.5,
            buff=0.1,
            color=control_color,
            stroke_width=2
        )
        
        self.play(
            Create(u_arrow),
            Write(u_label),
            run_time=1.5
        )
        self.wait(1.5)
        
        self.play(
            FadeOut(u_arrow),
            FadeOut(u_label),
            run_time=0.5
        )
        
        # Transform back to u
        state_space_final = MathTex(
            r"\dot{\boldsymbol{x}} = \mathbf{f}(\boldsymbol{x}(t), \boldsymbol{u}(t))",
            font_size=40
        )
        state_space_final.move_to(state_space_eq.get_center())
        
        self.play(Transform(state_space_eq, state_space_final), run_time=1.5)
        self.wait(2)
        
        self.wait(3)

