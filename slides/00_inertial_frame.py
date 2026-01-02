from manim import *
from manim_slides import ThreeDSlide

class InertialFrameSlide(ThreeDSlide):
    def construct(self):
        # Show title at the beginning
        title = Text("Cuadricóptero como modelo matemático", font_size=42, color=YELLOW).move_to(ORIGIN)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title), run_time=1.5)
        self.wait(1.5)
        self.play(FadeOut(title), run_time=1)
        self.wait(0.5)
        
        # Set up 3D axes with labels
        axes = ThreeDAxes(x_range=[-2, 2], y_range=[-2, 2], z_range=[-2, 2])
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("z")
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
        self.add(axes, x_label, y_label, z_label)

        # Create quadcopter with arms NOT aligned with axes
        # Use a more realistic body shape (box instead of sphere)
        body = Prism(dimensions=[0.3, 0.3, 0.15], color=BLUE, fill_opacity=0.8)
        
        # Create four arms in X configuration (45 degrees from axes)
        arm_length = 1.5
        arm_radius = 0.05
        
        # Create arms along X and Y axes first, then rotate 45 degrees
        # Arm 1: along +X direction (horizontal)
        arm1 = Cylinder(radius=arm_radius, height=arm_length, color=RED, fill_opacity=0.9)
        arm1.rotate(PI/2, axis=UP, about_point=ORIGIN)
        arm1.shift(RIGHT * arm_length / 2)
        
        # Arm 2: along -X direction (horizontal)
        arm2 = Cylinder(radius=arm_radius, height=arm_length, color=GREEN, fill_opacity=0.9)
        arm2.rotate(PI/2, axis=UP, about_point=ORIGIN)
        arm2.shift(LEFT * arm_length / 2)
        
        # Arm 3: along +Y direction (horizontal)
        arm3 = Cylinder(radius=arm_radius, height=arm_length, color=YELLOW, fill_opacity=0.9)
        arm3.rotate(PI/2, axis=RIGHT, about_point=ORIGIN)
        arm3.shift(UP * arm_length / 2)
        
        # Arm 4: along -Y direction (horizontal)
        arm4 = Cylinder(radius=arm_radius, height=arm_length, color=ORANGE, fill_opacity=0.9)
        arm4.rotate(PI/2, axis=RIGHT, about_point=ORIGIN)
        arm4.shift(DOWN * arm_length / 2)
        
        # Create propellers at the end of each arm
        propeller_radius = 0.2
        propeller_height = 0.02
        
        # Propeller 1 (at +X end)
        prop1 = Cylinder(radius=propeller_radius, height=propeller_height, color=GRAY, fill_opacity=0.7)
        prop1.shift(RIGHT * arm_length)
        
        # Propeller 2 (at -X end)
        prop2 = Cylinder(radius=propeller_radius, height=propeller_height, color=GRAY, fill_opacity=0.7)
        prop2.shift(LEFT * arm_length)
        
        # Propeller 3 (at +Y end)
        prop3 = Cylinder(radius=propeller_radius, height=propeller_height, color=GRAY, fill_opacity=0.7)
        prop3.shift(UP * arm_length)
        
        # Propeller 4 (at -Y end)
        prop4 = Cylinder(radius=propeller_radius, height=propeller_height, color=GRAY, fill_opacity=0.7)
        prop4.shift(DOWN * arm_length)
        
        # Group all components
        quadcopter = VGroup(body, arm1, arm2, arm3, arm4, prop1, prop2, prop3, prop4)
        
        # Rotate the entire quadcopter 45 degrees around Z-axis so arms are NOT aligned with axes
        quadcopter.rotate(PI/4, axis=OUT, about_point=ORIGIN)
        
        self.add(quadcopter)

        # Add axis indicators for better visualization
        x_axis_arrow = Arrow3D(start=ORIGIN, end=RIGHT*1.5, color=RED, thickness=0.02)
        y_axis_arrow = Arrow3D(start=ORIGIN, end=UP*1.5, color=GREEN, thickness=0.02)
        z_axis_arrow = Arrow3D(start=ORIGIN, end=OUT*1.5, color=BLUE, thickness=0.02)
        self.add(x_axis_arrow, y_axis_arrow, z_axis_arrow)

        # Show rotor angular velocities
        self.wait(0.5)
        
        # Create omega labels near each propeller (fixed in frame, not rotated)
        # Position them in screen coordinates to appear near the propellers
        omega1_label = MathTex(r"\omega_1", font_size=24, color=WHITE).move_to(np.array([2.5, 1.5, 0]))
        omega2_label = MathTex(r"\omega_2", font_size=24, color=WHITE).move_to(np.array([-2.5, -1.5, 0]))
        omega3_label = MathTex(r"\omega_3", font_size=24, color=WHITE).move_to(np.array([-1.5, 2.5, 0]))
        omega4_label = MathTex(r"\omega_4", font_size=24, color=WHITE).move_to(np.array([1.5, -2.5, 0]))
        
        rotor_vel_title = Text("velocidades angulares de rotores", font_size=28, color=YELLOW).to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(rotor_vel_title, omega1_label, omega2_label, omega3_label, omega4_label)
        
        self.play(FadeIn(rotor_vel_title), run_time=1)
        self.wait(0.3)
        self.play(
            FadeIn(omega1_label),
            FadeIn(omega2_label),
            FadeIn(omega3_label),
            FadeIn(omega4_label),
            run_time=2
        )
        self.wait(1)
        
        # Show k and transform to "coeficiente de elevación"
        k_label = MathTex(r"k", font_size=32, color=WHITE).to_edge(RIGHT, buff=1).shift(UP*1.5)
        self.add_fixed_in_frame_mobjects(k_label)
        self.play(FadeIn(k_label), run_time=1)
        self.wait(0.5)
        
        k_coef_label = Text("coeficiente de elevación", font_size=24, color=WHITE).to_edge(RIGHT, buff=1).shift(UP*1.5)
        self.play(Transform(k_label, k_coef_label), run_time=1.5)
        self.wait(1)
        
        # Transform omega_i to k*omega_i^2 (use same positions as omega labels)
        omega1_force = MathTex(r"k\omega_1^2", font_size=24, color=WHITE).move_to(np.array([2.5, 1.5, 0]))
        omega2_force = MathTex(r"k\omega_2^2", font_size=24, color=WHITE).move_to(np.array([-2.5, -1.5, 0]))
        omega3_force = MathTex(r"k\omega_3^2", font_size=24, color=WHITE).move_to(np.array([-1.5, 2.5, 0]))
        omega4_force = MathTex(r"k\omega_4^2", font_size=24, color=WHITE).move_to(np.array([1.5, -2.5, 0]))
        
        self.play(
            Transform(omega1_label, omega1_force),
            Transform(omega2_label, omega2_force),
            Transform(omega3_label, omega3_force),
            Transform(omega4_label, omega4_force),
            run_time=2
        )
        self.wait(1)
        
        # Transform title to "fuerza en dirección del rotor"
        fuerza_title = Text("fuerza en dirección del rotor", font_size=28, color=YELLOW).to_edge(UP, buff=0.5)
        self.play(Transform(rotor_vel_title, fuerza_title), run_time=1.5)
        self.wait(1.5)
        
        # Fade out rotor velocity/force labels
        self.play(
            FadeOut(omega1_label),
            FadeOut(omega2_label),
            FadeOut(omega3_label),
            FadeOut(omega4_label),
            FadeOut(k_label),
            FadeOut(rotor_vel_title),
            run_time=1.5
        )
        self.wait(0.5)

        # Roll label and animation
        roll_angle_label = MathTex(r"\text{Ángulo \textit{roll}}: \varphi", r"\text{ (rotación alrededor del eje x}\text{)}").scale(0.6).to_corner(UL)
        roll_angle_label.set_color_by_tex(r"eje x", RED)

        # Roll rotation matrix
        roll_matrix_label = Text("matriz asociada a roll", font_size=18, color=RED).to_corner(UL).shift(DOWN*0.7)
        roll_matrix = MathTex(
            r"\mathbf{R}(\varphi) = \begin{bmatrix} 1 & 0 & 0 \\ 0 & C_{\varphi} & S_{\varphi} \\ 0 & -S_{\varphi} & C_{\varphi} \end{bmatrix}"
        ).scale(0.5).next_to(roll_matrix_label, DOWN, aligned_edge=LEFT)
        roll_matrix.set_color(RED)
        
        # Roll torque
        roll_torque_label = Text("torque asociado a roll", font_size=18, color=RED).next_to(roll_matrix, DOWN, aligned_edge=LEFT)
        roll_torque = MathTex(
            r"\boldsymbol{\tau}_{\varphi} = \ell k (\omega_{4}^2 - \omega_2^{2})"
        ).scale(0.5).next_to(roll_torque_label, DOWN, aligned_edge=LEFT)
        roll_torque.set_color(RED)

        self.add_fixed_in_frame_mobjects(roll_angle_label)
        self.play(FadeIn(roll_angle_label))
        self.wait(0.5)
        self.add_fixed_in_frame_mobjects(roll_matrix_label, roll_matrix)
        self.play(FadeIn(roll_matrix_label), FadeIn(roll_matrix))
        self.add_fixed_in_frame_mobjects(roll_torque_label, roll_torque)
        self.play(FadeIn(roll_torque_label), FadeIn(roll_torque))

        # Highlight X-axis label instead of the axis arrow
        self.play(x_label.animate.set_color(YELLOW))
        
        # Create arrowed arc around X-axis (for roll rotation)
        # The arc is in the YZ plane, perpendicular to X-axis
        roll_arc_radius = 0.8
        roll_arc = ParametricFunction(
            lambda t: np.array([
                0,  # x stays at 0 (rotation around x-axis)
                roll_arc_radius * np.cos(t),  # y component
                roll_arc_radius * np.sin(t)   # z component
            ]),
            t_range=[0, PI/4],
            color=RED,
            stroke_width=3
        )
        
        # Roll animation (rotation around x-axis) - highlight the labels during rotation
        bright_red = "#FF6666"
        self.play(
            Rotate(quadcopter, angle=PI/4, axis=RIGHT, about_point=ORIGIN),
            Create(roll_arc),
            roll_matrix.animate.set_color(bright_red),
            roll_torque.animate.set_color(bright_red),
            roll_matrix_label.animate.set_color(bright_red),
            roll_torque_label.animate.set_color(bright_red),
            run_time=2
        )
        self.play(
            roll_matrix.animate.set_color(RED),
            roll_torque.animate.set_color(RED),
            roll_matrix_label.animate.set_color(RED),
            roll_torque_label.animate.set_color(RED),
            run_time=0.3
        )
        self.wait(0.5)
        # Fade out the arc before returning
        self.play(FadeOut(roll_arc), run_time=0.5)
        self.wait(0.5)
        self.play(Rotate(quadcopter, angle=-PI/4, axis=RIGHT, about_point=ORIGIN), run_time=2)
        self.wait(0.5)
        # Restore original label color and fade out
        self.play(x_label.animate.set_color(WHITE), FadeOut(roll_angle_label), FadeOut(roll_matrix_label), FadeOut(roll_matrix), FadeOut(roll_torque_label), FadeOut(roll_torque))

        # Pitch label and animation
        pitch_angle_label = MathTex(r"\text{Ángulo \textit{pitch}}: \theta", r"\text{ (rotación alrededor del eje y}\text{)}").scale(0.6).to_corner(UL)
        pitch_angle_label.set_color_by_tex(r"eje y", GREEN)

        # Pitch rotation matrix
        pitch_matrix_label = Text("matriz asociada a pitch", font_size=18, color=GREEN).to_corner(UL).shift(DOWN*0.7)
        pitch_matrix = MathTex(
            r"\mathbf{R}(\theta) = \begin{bmatrix} C_{\theta} & 0 & -S_{\theta} \\ 0 & 1 & 0 \\ S_{\theta} & 0 & C_{\theta} \end{bmatrix}"
        ).scale(0.5).next_to(pitch_matrix_label, DOWN, aligned_edge=LEFT)
        pitch_matrix.set_color(GREEN)
        
        # Pitch torque
        pitch_torque_label = Text("momento asociado a pitch", font_size=18, color=GREEN).next_to(pitch_matrix, DOWN, aligned_edge=LEFT)
        pitch_torque = MathTex(
            r"\boldsymbol{\tau}_{\theta} = \ell k (\omega_{3}^2 - \omega_1^{2})"
        ).scale(0.5).next_to(pitch_torque_label, DOWN, aligned_edge=LEFT)
        pitch_torque.set_color(GREEN)

        self.add_fixed_in_frame_mobjects(pitch_angle_label)
        self.play(FadeIn(pitch_angle_label))
        self.wait(0.5)
        self.add_fixed_in_frame_mobjects(pitch_matrix_label, pitch_matrix)
        self.play(FadeIn(pitch_matrix_label), FadeIn(pitch_matrix))
        self.add_fixed_in_frame_mobjects(pitch_torque_label, pitch_torque)
        self.play(FadeIn(pitch_torque_label), FadeIn(pitch_torque))

        # Highlight Y-axis label instead of the axis arrow
        self.play(y_label.animate.set_color(YELLOW))
        
        # Create arrowed arc around Y-axis (for pitch rotation)
        # The arc is in the XZ plane, perpendicular to Y-axis
        pitch_arc_radius = 0.8
        pitch_arc = ParametricFunction(
            lambda t: np.array([
                pitch_arc_radius * np.cos(t),  # x component
                0,  # y stays at 0 (rotation around y-axis)
                pitch_arc_radius * np.sin(t)   # z component
            ]),
            t_range=[0, PI/4],
            color=GREEN,
            stroke_width=3
        )
        
        # Pitch animation (rotation around y-axis) - highlight the labels during rotation
        bright_green = "#66FF66"
        self.play(
            Rotate(quadcopter, angle=PI/4, axis=DOWN, about_point=ORIGIN),
            Create(pitch_arc),
            pitch_matrix.animate.set_color(bright_green),
            pitch_torque.animate.set_color(bright_green),
            pitch_matrix_label.animate.set_color(bright_green),
            pitch_torque_label.animate.set_color(bright_green),
            run_time=2
        )
        self.play(
            pitch_matrix.animate.set_color(GREEN),
            pitch_torque.animate.set_color(GREEN),
            pitch_matrix_label.animate.set_color(GREEN),
            pitch_torque_label.animate.set_color(GREEN),
            run_time=0.3
        )
        self.wait(0.5)
        # Fade out the arc before returning
        self.play(FadeOut(pitch_arc), run_time=0.5)
        self.wait(0.5)
        self.play(Rotate(quadcopter, angle=-PI/4, axis=DOWN, about_point=ORIGIN), run_time=2)
        self.wait(0.5)
        # Restore original label color and fade out
        self.play(y_label.animate.set_color(WHITE), FadeOut(pitch_angle_label), FadeOut(pitch_matrix_label), FadeOut(pitch_matrix), FadeOut(pitch_torque_label), FadeOut(pitch_torque))

        # Yaw label and animation
        yaw_angle_label = MathTex(r"\text{Ángulo \textit{yaw}}: \psi", r"\text{ (rotación alrededor del eje z}\text{)}").scale(0.6).to_corner(UL)
        yaw_angle_label.set_color_by_tex(r"eje z", BLUE)
        
        # Yaw rotation matrix
        yaw_matrix_label = Text("matriz asociada a yaw", font_size=18, color=BLUE).to_corner(UL).shift(DOWN*0.7)
        yaw_matrix = MathTex(
            r"\mathbf{R}(\psi) = \begin{bmatrix} C_{\psi} & S_{\psi} & 0 \\ -S_{\psi} & C_{\psi} & 0 \\ 0 & 0 & 1 \end{bmatrix}"
        ).scale(0.5).next_to(yaw_matrix_label, DOWN, aligned_edge=LEFT)
        yaw_matrix.set_color(BLUE)
        
        # Yaw torque
        yaw_torque_label = Text("momento asociado a yaw", font_size=18, color=BLUE).next_to(yaw_matrix, DOWN, aligned_edge=LEFT)
        yaw_torque = MathTex(
            r"\boldsymbol{\tau}_{\psi} = b \sum_{i=1}^{4} (-1)^{i+1} \omega_{i}^2"
        ).scale(0.5).next_to(yaw_torque_label, DOWN, aligned_edge=LEFT)
        yaw_torque.set_color(BLUE)
        
        self.add_fixed_in_frame_mobjects(yaw_angle_label)
        self.play(FadeIn(yaw_angle_label))
        self.wait(0.5)
        self.add_fixed_in_frame_mobjects(yaw_matrix_label, yaw_matrix)
        self.play(FadeIn(yaw_matrix_label), FadeIn(yaw_matrix))
        self.add_fixed_in_frame_mobjects(yaw_torque_label, yaw_torque)
        self.play(FadeIn(yaw_torque_label), FadeIn(yaw_torque))

        # Highlight Z-axis label instead of the axis arrow
        self.play(z_label.animate.set_color(YELLOW))
        
        # Create arrowed arc around Z-axis (for yaw rotation)
        # The arc is in the XY plane, perpendicular to Z-axis
        yaw_arc_radius = 0.8
        yaw_arc = ParametricFunction(
            lambda t: np.array([
                yaw_arc_radius * np.cos(t),  # x component
                yaw_arc_radius * np.sin(t),   # y component
                0  # z stays at 0 (rotation around z-axis)
            ]),
            t_range=[0, PI/2],
            color=BLUE,
            stroke_width=3
        )
        
        # Yaw animation (rotation around z-axis) - highlight the labels during rotation
        bright_blue = "#6666FF"
        self.play(
            Rotate(quadcopter, angle=PI/2, axis=OUT, about_point=ORIGIN),
            Create(yaw_arc),
            yaw_matrix.animate.set_color(bright_blue),
            yaw_torque.animate.set_color(bright_blue),
            yaw_matrix_label.animate.set_color(bright_blue),
            yaw_torque_label.animate.set_color(bright_blue),
            run_time=2
        )
        self.play(
            yaw_matrix.animate.set_color(BLUE),
            yaw_torque.animate.set_color(BLUE),
            yaw_matrix_label.animate.set_color(BLUE),
            yaw_torque_label.animate.set_color(BLUE),
            run_time=0.3
        )
        self.wait(0.5)
        # Fade out the arc before returning
        self.play(FadeOut(yaw_arc), run_time=0.5)
        self.wait(0.5)
        self.play(Rotate(quadcopter, angle=-PI/2, axis=OUT, about_point=ORIGIN), run_time=2)
        self.wait(0.5)
        # Restore original label color and fade out
        self.play(z_label.animate.set_color(WHITE), FadeOut(yaw_angle_label), FadeOut(yaw_matrix_label), FadeOut(yaw_matrix), FadeOut(yaw_torque_label), FadeOut(yaw_torque))
        
        # Final matrix product visualization
        self.wait(1)
        
        # Create the three individual matrices positioned around the center with full equations
        # Yaw matrix on the left - start with full equation
        final_yaw_matrix_full = MathTex(
            r"\mathbf{R}(\psi) = \begin{bmatrix} C_{\psi} & S_{\psi} & 0 \\ -S_{\psi} & C_{\psi} & 0 \\ 0 & 0 & 1 \end{bmatrix}"
        ).scale(0.4).to_edge(LEFT, buff=1).shift(UP*0.5)
        final_yaw_matrix_full.set_color(BLUE)
        final_yaw_label = Text("matriz asociada a yaw", font_size=16, color=BLUE).next_to(final_yaw_matrix_full, DOWN, buff=0.1)
        
        # Pitch matrix on the right - start with full equation
        final_pitch_matrix_full = MathTex(
            r"\mathbf{R}(\theta) = \begin{bmatrix} C_{\theta} & 0 & -S_{\theta} \\ 0 & 1 & 0 \\ S_{\theta} & 0 & C_{\theta} \end{bmatrix}"
        ).scale(0.4).to_edge(RIGHT, buff=1).shift(UP*0.5)
        final_pitch_matrix_full.set_color(GREEN)
        final_pitch_label = Text("matriz asociada a pitch", font_size=16, color=GREEN).next_to(final_pitch_matrix_full, DOWN, buff=0.1)
        
        # Roll matrix at the bottom - start with full equation
        final_roll_matrix_full = MathTex(
            r"\mathbf{R}(\varphi) = \begin{bmatrix} 1 & 0 & 0 \\ 0 & C_{\varphi} & S_{\varphi} \\ 0 & -S_{\varphi} & C_{\varphi} \end{bmatrix}"
        ).scale(0.4).to_edge(DOWN, buff=1)
        final_roll_matrix_full.set_color(RED)
        final_roll_label = Text("matriz asociada a roll", font_size=16, color=RED).next_to(final_roll_matrix_full, DOWN, buff=0.1)
        
        # Create simplified versions (just left-hand side) at same positions
        final_yaw_matrix_simple = MathTex(r"\mathbf{R}(\psi)").scale(0.6).to_edge(LEFT, buff=1).shift(UP*0.5)
        final_yaw_matrix_simple.set_color(BLUE)
        
        final_pitch_matrix_simple = MathTex(r"\mathbf{R}(\theta)").scale(0.6).to_edge(RIGHT, buff=1).shift(UP*0.5)
        final_pitch_matrix_simple.set_color(GREEN)
        
        final_roll_matrix_simple = MathTex(r"\mathbf{R}(\varphi)").scale(0.6).to_edge(DOWN, buff=1)
        final_roll_matrix_simple.set_color(RED)
        
        # Multiplication expression
        mult_matrix = MathTex(r"\mathbf{R}(\psi) \cdot \mathbf{R}(\theta) \cdot \mathbf{R}(\varphi)").move_to(LEFT)
        mult_matrix.set_color(WHITE)
        
        # Combined product matrix at the bottom
        combined_matrix = MathTex(
            r"\mathbf{R}(\psi, \theta, \varphi) = \begin{bmatrix} C_{\psi}C_{\theta} & C_{\psi}S_{\theta}S_{\varphi} - S_{\psi}C_{\varphi} & C_{\psi}S_{\theta}C_{\varphi} + S_{\psi}S_{\varphi} \\ S_{\psi}C_{\theta} & S_{\psi}S_{\theta}S_{\varphi}+C_{\psi}C_{\varphi} & S_{\psi}S_{\theta}C_{\varphi}-C_{\psi}S_{\varphi} \\ -S_{\theta} & C_{\theta}S_{\varphi} & C_{\theta}C_{\varphi} \end{bmatrix}"
        ).scale(0.5).to_edge(LEFT, buff=0.5)
        combined_label = Text("matriz combinada", font_size=18, color=YELLOW).next_to(combined_matrix, DOWN, buff=0.1)
        
        # Fade in the three individual matrices with full equations
        self.add_fixed_in_frame_mobjects(final_yaw_matrix_full, final_yaw_label, final_pitch_matrix_full, final_pitch_label, final_roll_matrix_full, final_roll_label)
        self.play(
            FadeIn(final_yaw_matrix_full), FadeIn(final_yaw_label),
            FadeIn(final_pitch_matrix_full), FadeIn(final_pitch_label),
            FadeIn(final_roll_matrix_full), FadeIn(final_roll_label),
            run_time=2
        )
        self.wait(1)
        
        # Transform full equations to just left-hand side
        self.play(
            Transform(final_yaw_matrix_full, final_yaw_matrix_simple),
            Transform(final_pitch_matrix_full, final_pitch_matrix_simple),
            Transform(final_roll_matrix_full, final_roll_matrix_simple),
            run_time=2
        )
        self.wait(0.5)
        
        # Move simplified matrices toward center
        self.play(
            final_yaw_matrix_full.animate.move_to(LEFT),
            final_pitch_matrix_full.animate.move_to(LEFT),
            final_roll_matrix_full.animate.move_to(LEFT),
            FadeOut(final_yaw_label),
            FadeOut(final_pitch_label),
            FadeOut(final_roll_label),
            run_time=2
        )
        self.wait(0.5)
        
        # Merge into multiplication expression
        self.play(
            Transform(final_yaw_matrix_full, mult_matrix),
            FadeOut(final_pitch_matrix_full),
            FadeOut(final_roll_matrix_full),
            run_time=2
        )
        self.wait(1)
        
        # Transform multiplication to combined matrix
        self.add_fixed_in_frame_mobjects(combined_label)
        self.play(
            Transform(final_yaw_matrix_full, combined_matrix),
            FadeIn(combined_label),
            run_time=2
        )
        self.wait(1)
        
        # Simulate rotation with all Euler angles
        # Apply rotations in sequence: yaw first, then pitch, then roll (standard Euler angle convention)
        # This demonstrates the combined rotation matrix in action
        
        # Create arcs for all three rotations
        combined_arc_radius = 1.0
        
        # Yaw arc (around z-axis)
        yaw_arc_combined = ParametricFunction(
            lambda t: np.array([
                combined_arc_radius * np.cos(t),
                combined_arc_radius * np.sin(t),
                0
            ]),
            t_range=[0, PI/3],
            color=BLUE,
            stroke_width=3
        )
        
        # Pitch arc (around y-axis) - will be rotated by yaw first
        pitch_arc_combined = ParametricFunction(
            lambda t: np.array([
                combined_arc_radius * np.cos(t),
                0,
                combined_arc_radius * np.sin(t)
            ]),
            t_range=[0, PI/4],
            color=GREEN,
            stroke_width=3
        )
        
        # Roll arc (around x-axis) - will be rotated by yaw and pitch
        roll_arc_combined = ParametricFunction(
            lambda t: np.array([
                0,
                combined_arc_radius * np.cos(t),
                combined_arc_radius * np.sin(t)
            ]),
            t_range=[0, PI/4],
            color=RED,
            stroke_width=3
        )
        
        # Apply rotations sequentially: yaw, then pitch, then roll
        self.play(
            Rotate(quadcopter, angle=PI/3, axis=OUT, about_point=ORIGIN),  # Yaw
            Create(yaw_arc_combined),
            run_time=1.5
        )
        self.wait(0.3)
        self.play(FadeOut(yaw_arc_combined))
        
        # Rotate pitch arc by yaw angle
        pitch_arc_combined.rotate(PI/3, axis=OUT, about_point=ORIGIN)
        self.play(
            Rotate(quadcopter, angle=PI/4, axis=UP, about_point=ORIGIN),    # Pitch
            Create(pitch_arc_combined),
            run_time=1.5
        )
        self.wait(0.3)
        self.play(FadeOut(pitch_arc_combined))
        
        # Rotate roll arc by yaw and pitch angles
        roll_arc_combined.rotate(PI/3, axis=OUT, about_point=ORIGIN)
        roll_arc_combined.rotate(PI/4, axis=UP, about_point=ORIGIN)
        self.play(
            Rotate(quadcopter, angle=PI/4, axis=RIGHT, about_point=ORIGIN), # Roll
            Create(roll_arc_combined),
            run_time=1.5
        )
        self.wait(1)
        self.play(FadeOut(roll_arc_combined))
        
        # Return to original orientation (reverse order: roll, pitch, yaw)
        self.play(
            Rotate(quadcopter, angle=-PI/4, axis=RIGHT, about_point=ORIGIN), # Reverse Roll
            run_time=1.5
        )
        self.wait(0.3)
        self.play(
            Rotate(quadcopter, angle=-PI/4, axis=UP, about_point=ORIGIN),    # Reverse Pitch
            run_time=1.5
        )
        self.wait(0.3)
        self.play(
            Rotate(quadcopter, angle=-PI/3, axis=OUT, about_point=ORIGIN),  # Reverse Yaw
            run_time=1.5
        )
        self.wait(1)
        
        # Fade out the combined matrix (final_yaw_matrix_full was transformed to combined_matrix)
        self.play(FadeOut(final_yaw_matrix_full), FadeOut(combined_label), run_time=1)
        self.wait(0.5)
        
        # Show title "Momentos, fuerzas y torques"
        title_momentos = Text("Momentos, fuerzas y torques", font_size=36, color=YELLOW).to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(title_momentos)
        self.play(FadeIn(title_momentos), run_time=1)
        self.wait(0.5)
        
        # Show the three torques
        torque_roll_final = MathTex(
            r"\boldsymbol{\tau}_{\varphi} = \ell k (\omega_{4}^2 - \omega_2^{2})"
        ).scale(0.6).to_edge(LEFT, buff=1).shift(UP*1.5)
        torque_roll_final.set_color(RED)
        torque_roll_label_final = Text("momento asociado a roll", font_size=20, color=RED).next_to(torque_roll_final, RIGHT, buff=0.3)
        
        torque_pitch_final = MathTex(
            r"\boldsymbol{\tau}_{\theta} = \ell k (\omega_{3}^2 - \omega_1^{2})"
        ).scale(0.6).to_edge(LEFT, buff=1).shift(UP*0.5)
        torque_pitch_final.set_color(GREEN)
        torque_pitch_label_final = Text("momento asociado a pitch", font_size=20, color=GREEN).next_to(torque_pitch_final, RIGHT, buff=0.3)
        
        torque_yaw_final = MathTex(
            r"\boldsymbol{\tau}_{\psi} = b \sum_{i=1}^{4} (-1)^{i+1} \omega_{i}^2"
        ).scale(0.6).to_edge(LEFT, buff=1).shift(DOWN*0.5)
        torque_yaw_final.set_color(BLUE)
        torque_yaw_label_final = Text("momento asociado a yaw", font_size=20, color=BLUE).next_to(torque_yaw_final, RIGHT, buff=0.3)
        
        self.add_fixed_in_frame_mobjects(torque_roll_final, torque_roll_label_final, torque_pitch_final, torque_pitch_label_final, torque_yaw_final, torque_yaw_label_final)
        self.play(
            FadeIn(torque_roll_final), FadeIn(torque_roll_label_final),
            FadeIn(torque_pitch_final), FadeIn(torque_pitch_label_final),
            FadeIn(torque_yaw_final), FadeIn(torque_yaw_label_final),
            run_time=2
        )
        self.wait(1)
        
        # Show thrust T_z
        thrust_eq = MathTex(
            r"T_z = k \sum_{i=1}^{4} \omega_{i}^2"
        ).scale(0.7).to_edge(RIGHT, buff=1).shift(UP*1.5)
        
        self.add_fixed_in_frame_mobjects(thrust_eq)
        self.play(FadeIn(thrust_eq), run_time=1.5)
        self.wait(0.5)
        
        # Show vector T_B and fill it with T_z
        vector_T_label = MathTex(r"\mathbf{T}_{B} = ").scale(0.7).next_to(thrust_eq, DOWN, buff=0.5, aligned_edge=LEFT)
        vector_T_matrix = MathTex(
            r"\begin{bmatrix} 0 \\ 0 \\ T_z \end{bmatrix}"
        ).scale(0.7).next_to(vector_T_label, RIGHT, buff=0.1)
        
        self.add_fixed_in_frame_mobjects(vector_T_label, vector_T_matrix)
        self.play(FadeIn(vector_T_label), FadeIn(vector_T_matrix), run_time=1.5)
        self.wait(1.5)
        
        # Fade out all expressions
        self.play(
            FadeOut(title_momentos),
            FadeOut(torque_roll_final), FadeOut(torque_roll_label_final),
            FadeOut(torque_pitch_final), FadeOut(torque_pitch_label_final),
            FadeOut(torque_yaw_final), FadeOut(torque_yaw_label_final),
            FadeOut(thrust_eq),
            FadeOut(vector_T_label), FadeOut(vector_T_matrix),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Show title "Sistema de referencia inercial"
        title_sistema = Text("Sistema de referencia inercial", font_size=36, color=YELLOW).to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(title_sistema)
        self.play(FadeIn(title_sistema), run_time=1)
        self.wait(0.5)
        
        # Show position vector ξ with label (LEFT)
        pos_lineal_label = Text("posición lineal", font_size=24, color=WHITE).to_edge(LEFT, buff=1).shift(UP*0.5)
        vector_xi_label = MathTex(r"\boldsymbol{\xi} = ").scale(0.8).next_to(pos_lineal_label, RIGHT, buff=0.5)
        vector_xi_matrix = MathTex(
            r"\begin{bmatrix} x \\ y \\ z \end{bmatrix}"
        ).scale(0.8).next_to(vector_xi_label, RIGHT, buff=0.1)
        
        self.add_fixed_in_frame_mobjects(pos_lineal_label, vector_xi_label, vector_xi_matrix)
        self.play(FadeIn(pos_lineal_label), FadeIn(vector_xi_label), FadeIn(vector_xi_matrix), run_time=1.5)
        self.wait(1)
        
        # Show angle vector η with label (RIGHT)
        pos_angular_label = Text("posición angular", font_size=24, color=WHITE).to_edge(RIGHT, buff=1).shift(UP*0.5)
        vector_eta_label = MathTex(r"\boldsymbol{\eta} = ").scale(0.8).next_to(pos_angular_label, RIGHT, buff=0.5)
        vector_eta_matrix = MathTex(
            r"\begin{bmatrix} \varphi \\ \theta \\ \psi \end{bmatrix}"
        ).scale(0.8).next_to(vector_eta_label, RIGHT, buff=0.1)
        
        self.add_fixed_in_frame_mobjects(pos_angular_label, vector_eta_label, vector_eta_matrix)
        self.play(FadeIn(pos_angular_label), FadeIn(vector_eta_label), FadeIn(vector_eta_matrix), run_time=1.5)
        self.wait(1)
        
        # Fade out inertial system
        self.play(
            FadeOut(title_sistema),
            FadeOut(pos_lineal_label), FadeOut(vector_xi_label), FadeOut(vector_xi_matrix),
            FadeOut(pos_angular_label), FadeOut(vector_eta_label), FadeOut(vector_eta_matrix),
            run_time=1
        )
        self.wait(0.5)
        
        # Show title "Sistema de referencia local"
        title_local = Text("Sistema de referencia local", font_size=36, color=YELLOW).to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(title_local)
        self.play(FadeIn(title_local), run_time=1)
        self.wait(0.5)
        
        # Move and rotate quadcopter to show local frame
        # Translate quadcopter away from origin
        translation_vec = np.array([1.5, 1.0, 0.8])
        
        # Rotate quadcopter with Euler angles (yaw, pitch, roll)
        euler_yaw = PI/6
        euler_pitch = PI/8
        euler_roll = PI/12
        
        # First translate
        self.play(
            quadcopter.animate.shift(translation_vec),
            run_time=1.5
        )
        self.wait(0.3)
        
        # Then rotate about the new position
        quadcopter_center = translation_vec
        self.play(
            Rotate(quadcopter, angle=euler_yaw, axis=OUT, about_point=quadcopter_center),
            run_time=1.5
        )
        self.wait(0.3)
        self.play(
            Rotate(quadcopter, angle=euler_pitch, axis=UP, about_point=quadcopter_center),
            run_time=1.5
        )
        self.wait(0.3)
        self.play(
            Rotate(quadcopter, angle=euler_roll, axis=RIGHT, about_point=quadcopter_center),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Draw local axes at quadcopter position (body frame)
        # Create axes in local frame, then transform them the same way as quadcopter
        local_x_arrow = Arrow3D(
            start=ORIGIN, 
            end=RIGHT*0.8, 
            color=RED, 
            thickness=0.02
        )
        local_y_arrow = Arrow3D(
            start=ORIGIN, 
            end=UP*0.8, 
            color=GREEN, 
            thickness=0.02
        )
        local_z_arrow = Arrow3D(
            start=ORIGIN, 
            end=OUT*0.8, 
            color=BLUE, 
            thickness=0.02
        )
        
        # Apply same transformations as quadcopter
        local_x_arrow.shift(translation_vec)
        local_y_arrow.shift(translation_vec)
        local_z_arrow.shift(translation_vec)
        
        local_x_arrow.rotate(euler_yaw, axis=OUT, about_point=quadcopter_center)
        local_x_arrow.rotate(euler_pitch, axis=UP, about_point=quadcopter_center)
        local_x_arrow.rotate(euler_roll, axis=RIGHT, about_point=quadcopter_center)
        
        local_y_arrow.rotate(euler_yaw, axis=OUT, about_point=quadcopter_center)
        local_y_arrow.rotate(euler_pitch, axis=UP, about_point=quadcopter_center)
        local_y_arrow.rotate(euler_roll, axis=RIGHT, about_point=quadcopter_center)
        
        local_z_arrow.rotate(euler_yaw, axis=OUT, about_point=quadcopter_center)
        local_z_arrow.rotate(euler_pitch, axis=UP, about_point=quadcopter_center)
        local_z_arrow.rotate(euler_roll, axis=RIGHT, about_point=quadcopter_center)
        
        self.play(
            Create(local_x_arrow),
            Create(local_y_arrow),
            Create(local_z_arrow),
            run_time=2
        )
        self.wait(0.5)
        
        # Show velocity vector υ (LEFT)
        vel_label = Text("velocidad lineal", font_size=24, color=WHITE).to_edge(LEFT, buff=1).shift(UP*0.5)
        vector_upsilon_label = MathTex(r"\boldsymbol{\upsilon} = ").scale(0.8).next_to(vel_label, RIGHT, buff=0.5)
        vector_upsilon_matrix = MathTex(
            r"\begin{bmatrix} u \\ v \\ w \end{bmatrix}"
        ).scale(0.8).next_to(vector_upsilon_label, RIGHT, buff=0.1)
        
        self.add_fixed_in_frame_mobjects(vel_label, vector_upsilon_label, vector_upsilon_matrix)
        self.play(FadeIn(vel_label), FadeIn(vector_upsilon_label), FadeIn(vector_upsilon_matrix), run_time=1.5)
        self.wait(1)
        
        # Show angular velocity vector ω (RIGHT) - positioned so it's fully visible
        ang_vel_label = Text("velocidad angular", font_size=24, color=WHITE).shift(RIGHT*2.5 + UP*0.5)
        vector_omega_label = MathTex(r"\boldsymbol{\omega} = ").scale(0.8).next_to(ang_vel_label, RIGHT, buff=0.3)
        vector_omega_matrix = MathTex(
            r"\begin{bmatrix} p \\ q \\ r \end{bmatrix}"
        ).scale(0.8).next_to(vector_omega_label, RIGHT, buff=0.1)
        
        self.add_fixed_in_frame_mobjects(ang_vel_label, vector_omega_label, vector_omega_matrix)
        self.play(FadeIn(ang_vel_label), FadeIn(vector_omega_label), FadeIn(vector_omega_matrix), run_time=1.5)
        self.wait(1)
