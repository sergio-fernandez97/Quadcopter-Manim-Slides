"""
Inertial frame visualization for the quadcopter model.

Animates the vehicle geometry, rotor forces, and Euler-angle rotations in a 3D
Manim slide to introduce the inertial and local reference frames.

Example:
    manim -pql slides/00_inertial_frame.py InertialFrameSlide

Author: Sergio Fernández
Date: 2025-01-30
"""

from manim import *
from manim_slides import ThreeDSlide
import numpy as np


class InertialFrameSlide(ThreeDSlide):

    def _create_quadcopter(self, arm_length=1.5):
        """Return a VGroup modelling the quadcopter body, arms and propellers."""
        body = Prism(dimensions=[0.3, 0.3, 0.15], color=BLUE, fill_opacity=0.8)
        arm_r = 0.05
        pr, ph = 0.2, 0.02

        arm1 = Cylinder(radius=arm_r, height=arm_length, color=RED, fill_opacity=0.9)
        arm1.rotate(PI / 2, axis=UP, about_point=ORIGIN).shift(RIGHT * arm_length / 2)
        arm2 = Cylinder(radius=arm_r, height=arm_length, color=GREEN, fill_opacity=0.9)
        arm2.rotate(PI / 2, axis=UP, about_point=ORIGIN).shift(LEFT * arm_length / 2)
        arm3 = Cylinder(radius=arm_r, height=arm_length, color=YELLOW, fill_opacity=0.9)
        arm3.rotate(PI / 2, axis=RIGHT, about_point=ORIGIN).shift(UP * arm_length / 2)
        arm4 = Cylinder(radius=arm_r, height=arm_length, color=ORANGE, fill_opacity=0.9)
        arm4.rotate(PI / 2, axis=RIGHT, about_point=ORIGIN).shift(DOWN * arm_length / 2)

        p1 = Cylinder(radius=pr, height=ph, color=GRAY, fill_opacity=0.7).shift(RIGHT * arm_length)
        p2 = Cylinder(radius=pr, height=ph, color=GRAY, fill_opacity=0.7).shift(LEFT * arm_length)
        p3 = Cylinder(radius=pr, height=ph, color=GRAY, fill_opacity=0.7).shift(UP * arm_length)
        p4 = Cylinder(radius=pr, height=ph, color=GRAY, fill_opacity=0.7).shift(DOWN * arm_length)

        quad = VGroup(body, arm1, arm2, arm3, arm4, p1, p2, p3, p4)
        quad.rotate(PI / 4, axis=OUT, about_point=ORIGIN)
        return quad

    # ------------------------------------------------------------------

    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)

        # ==============================================================
        # SECTION 1 – Title + definition + 3D quadcopter
        # ==============================================================
        title = Text(
            "Cuadricóptero como modelo matemático",
            font_size=36,
            color=YELLOW,
        ).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title), run_time=1)
        self.next_slide()

        # Boxed definition (left side of screen)
        def_content = Text(
            "Es vehículo aéreo que se eleva a través\n"
            "del empuje de cuatro rotores, cuyos\n"
            "torques causan rotaciones que permiten\n"
            "controlar su orientación y desplazamiento.",
            font_size=20,
            color=WHITE,
            line_spacing=1.3,
        )
        def_box = RoundedRectangle(
            corner_radius=0.2,
            width=def_content.width + 0.6,
            height=def_content.height + 0.4,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        def_group = VGroup(def_box, def_content).arrange(ORIGIN)
        def_group.to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        self.add_fixed_in_frame_mobjects(def_group)
        self.play(FadeIn(def_group), run_time=1.5)
        self.next_slide()

        # 3D axes + quadcopter (visible on the right half of the screen)
        axes = ThreeDAxes(x_range=[-2, 2], y_range=[-2, 2], z_range=[-2, 2])
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("z")
        quadcopter = self._create_quadcopter()
        x_arrow = Arrow3D(start=ORIGIN, end=RIGHT * 1.5, color=RED, thickness=0.02)
        y_arrow = Arrow3D(start=ORIGIN, end=UP * 1.5, color=GREEN, thickness=0.02)
        z_arrow = Arrow3D(start=ORIGIN, end=OUT * 1.5, color=BLUE, thickness=0.02)

        self.play(
            FadeIn(axes), FadeIn(x_label), FadeIn(y_label), FadeIn(z_label),
            FadeIn(quadcopter),
            FadeIn(x_arrow), FadeIn(y_arrow), FadeIn(z_arrow),
            run_time=2,
        )
        self.next_slide()

        # ==============================================================
        # SECTION 2 – Angular velocities
        # ==============================================================
        vel_label = Text("Velocidades angulares de rotores", font_size=22, color=YELLOW)
        vel_box = RoundedRectangle(
            corner_radius=0.2,
            width=vel_label.width + 0.6,
            height=vel_label.height + 0.4,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        vel_group = VGroup(vel_box, vel_label).arrange(ORIGIN)
        vel_group.move_to(def_group)

        self.play(Transform(def_group, vel_group), run_time=1.5)
        self.next_slide()

        # ω labels near each rotor (screen coords, fixed in frame)
        omega1_label = MathTex(r"\omega_1", font_size=28, color=WHITE).move_to(
            np.array([1.8, 0.8, 0])
        )
        omega2_label = MathTex(r"\omega_2", font_size=28, color=WHITE).move_to(
            np.array([-1.8, -0.8, 0])
        )
        omega3_label = MathTex(r"\omega_3", font_size=28, color=WHITE).move_to(
            np.array([-0.8, 1.8, 0])
        )
        omega4_label = MathTex(r"\omega_4", font_size=28, color=WHITE).move_to(
            np.array([0.8, -1.8, 0])
        )
        self.add_fixed_in_frame_mobjects(
            omega1_label, omega2_label, omega3_label, omega4_label
        )
        self.play(
            FadeIn(omega1_label), FadeIn(omega2_label),
            FadeIn(omega3_label), FadeIn(omega4_label),
            run_time=1.5,
        )
        self.next_slide()

        # ==============================================================
        # SECTION 3 – Three-column rotation display (Roll / Pitch / Yaw)
        # ==============================================================
        # Fade out sections 1-2
        self.play(
            FadeOut(title), FadeOut(def_group),
            FadeOut(axes), FadeOut(x_label), FadeOut(y_label), FadeOut(z_label),
            FadeOut(quadcopter),
            FadeOut(x_arrow), FadeOut(y_arrow), FadeOut(z_arrow),
            FadeOut(omega1_label), FadeOut(omega2_label),
            FadeOut(omega3_label), FadeOut(omega4_label),
            run_time=1,
        )

        # 3D column positions – with camera at phi=60°, theta=45° the
        # screen-horizontal direction is (-sin45, cos45, 0).
        # Placing groups along (1, -1, 0) spreads them on screen-x.
        # screen_x ≈ (-x + y) * 0.707
        d = 3.18  # gives screen_x ≈ ±4.5
        left_3d = np.array([d, -d, 0])
        center_3d = np.array([0, 0, 0])
        right_3d = np.array([-d, d, 0])

        mini_scale = 0.35
        arm_mini = 1.2

        # --- Roll column (left) ----------------------------------
        roll_axes = ThreeDAxes(
            x_range=[-1.5, 1.5], y_range=[-1.5, 1.5], z_range=[-1.5, 1.5],
        )
        roll_quad = self._create_quadcopter(arm_length=arm_mini)
        roll_xa = Arrow3D(start=ORIGIN, end=RIGHT * 1.2, color=RED, thickness=0.04)
        roll_ya = Arrow3D(start=ORIGIN, end=UP * 1.2, color=GREEN, thickness=0.02)
        roll_za = Arrow3D(start=ORIGIN, end=OUT * 1.2, color=BLUE, thickness=0.02)
        roll_3d = VGroup(roll_axes, roll_quad, roll_xa, roll_ya, roll_za)
        roll_3d.scale(mini_scale).shift(left_3d)

        # --- Pitch column (center) -------------------------------
        pitch_axes = ThreeDAxes(
            x_range=[-1.5, 1.5], y_range=[-1.5, 1.5], z_range=[-1.5, 1.5],
        )
        pitch_quad = self._create_quadcopter(arm_length=arm_mini)
        pitch_xa = Arrow3D(start=ORIGIN, end=RIGHT * 1.2, color=RED, thickness=0.02)
        pitch_ya = Arrow3D(start=ORIGIN, end=UP * 1.2, color=GREEN, thickness=0.04)
        pitch_za = Arrow3D(start=ORIGIN, end=OUT * 1.2, color=BLUE, thickness=0.02)
        pitch_3d = VGroup(pitch_axes, pitch_quad, pitch_xa, pitch_ya, pitch_za)
        pitch_3d.scale(mini_scale).shift(center_3d)

        # --- Yaw column (right) ----------------------------------
        yaw_axes = ThreeDAxes(
            x_range=[-1.5, 1.5], y_range=[-1.5, 1.5], z_range=[-1.5, 1.5],
        )
        yaw_quad = self._create_quadcopter(arm_length=arm_mini)
        yaw_xa = Arrow3D(start=ORIGIN, end=RIGHT * 1.2, color=RED, thickness=0.02)
        yaw_ya = Arrow3D(start=ORIGIN, end=UP * 1.2, color=GREEN, thickness=0.02)
        yaw_za = Arrow3D(start=ORIGIN, end=OUT * 1.2, color=BLUE, thickness=0.04)
        yaw_3d = VGroup(yaw_axes, yaw_quad, yaw_xa, yaw_ya, yaw_za)
        yaw_3d.scale(mini_scale).shift(right_3d)

        # Fixed-in-frame labels for each column (screen coords)
        # Titles
        roll_col_title = Text("Roll (eje x)", font_size=22, color=RED).move_to(
            np.array([-4.5, 3.2, 0])
        )
        pitch_col_title = Text("Pitch (eje y)", font_size=22, color=GREEN).move_to(
            np.array([0, 3.2, 0])
        )
        yaw_col_title = Text("Yaw (eje z)", font_size=22, color=BLUE).move_to(
            np.array([4.5, 3.2, 0])
        )

        # Torques
        roll_torque = MathTex(
            r"\boldsymbol{\tau}_{\varphi} = \ell k (\omega_{4}^2 - \omega_2^{2})",
            font_size=24,
        ).set_color(RED).move_to(np.array([-4.5, -1.6, 0]))
        pitch_torque = MathTex(
            r"\boldsymbol{\tau}_{\theta} = \ell k (\omega_{3}^2 - \omega_1^{2})",
            font_size=24,
        ).set_color(GREEN).move_to(np.array([0, -1.6, 0]))
        yaw_torque = MathTex(
            r"\boldsymbol{\tau}_{\psi} = b \sum_{i=1}^{4} (-1)^{i+1} \omega_{i}^2",
            font_size=24,
        ).set_color(BLUE).move_to(np.array([4.5, -1.6, 0]))

        # Rotation matrices
        roll_matrix = MathTex(
            r"\mathbf{R}(\varphi) = \begin{bmatrix}"
            r" 1 & 0 & 0 \\"
            r" 0 & C_{\varphi} & S_{\varphi} \\"
            r" 0 & -S_{\varphi} & C_{\varphi}"
            r" \end{bmatrix}",
            font_size=20,
        ).set_color(RED).move_to(np.array([-4.5, -2.8, 0]))
        pitch_matrix = MathTex(
            r"\mathbf{R}(\theta) = \begin{bmatrix}"
            r" C_{\theta} & 0 & -S_{\theta} \\"
            r" 0 & 1 & 0 \\"
            r" S_{\theta} & 0 & C_{\theta}"
            r" \end{bmatrix}",
            font_size=20,
        ).set_color(GREEN).move_to(np.array([0, -2.8, 0]))
        yaw_matrix = MathTex(
            r"\mathbf{R}(\psi) = \begin{bmatrix}"
            r" C_{\psi} & S_{\psi} & 0 \\"
            r" -S_{\psi} & C_{\psi} & 0 \\"
            r" 0 & 0 & 1"
            r" \end{bmatrix}",
            font_size=20,
        ).set_color(BLUE).move_to(np.array([4.5, -2.8, 0]))

        # --- Fade in each column one at a time ---

        # Roll
        self.add_fixed_in_frame_mobjects(roll_col_title, roll_torque, roll_matrix)
        self.play(
            FadeIn(roll_3d), FadeIn(roll_col_title),
            FadeIn(roll_torque), FadeIn(roll_matrix),
            run_time=1.5,
        )
        self.play(
            Rotate(roll_quad, angle=PI / 4, axis=RIGHT, about_point=left_3d),
            run_time=1.5,
        )
        self.play(
            Rotate(roll_quad, angle=-PI / 4, axis=RIGHT, about_point=left_3d),
            run_time=1,
        )
        self.next_slide()

        # Pitch
        self.add_fixed_in_frame_mobjects(pitch_col_title, pitch_torque, pitch_matrix)
        self.play(
            FadeIn(pitch_3d), FadeIn(pitch_col_title),
            FadeIn(pitch_torque), FadeIn(pitch_matrix),
            run_time=1.5,
        )
        self.play(
            Rotate(pitch_quad, angle=PI / 4, axis=UP, about_point=center_3d),
            run_time=1.5,
        )
        self.play(
            Rotate(pitch_quad, angle=-PI / 4, axis=UP, about_point=center_3d),
            run_time=1,
        )
        self.next_slide()

        # Yaw
        self.add_fixed_in_frame_mobjects(yaw_col_title, yaw_torque, yaw_matrix)
        self.play(
            FadeIn(yaw_3d), FadeIn(yaw_col_title),
            FadeIn(yaw_torque), FadeIn(yaw_matrix),
            run_time=1.5,
        )
        self.play(
            Rotate(yaw_quad, angle=PI / 2, axis=OUT, about_point=right_3d),
            run_time=1.5,
        )
        self.play(
            Rotate(yaw_quad, angle=-PI / 2, axis=OUT, about_point=right_3d),
            run_time=1,
        )
        self.next_slide()

        # ==============================================================
        # SECTION 4 – Merge axes + Euler rotation matrix + simulation
        # ==============================================================

        # Fade out torques and titles
        self.play(
            FadeOut(roll_torque), FadeOut(pitch_torque), FadeOut(yaw_torque),
            FadeOut(roll_col_title), FadeOut(pitch_col_title), FadeOut(yaw_col_title),
            run_time=1,
        )

        # Replace mini groups with a single full-size quadcopter at origin
        merged_axes = ThreeDAxes(x_range=[-2, 2], y_range=[-2, 2], z_range=[-2, 2])
        mx_label = merged_axes.get_x_axis_label("x")
        my_label = merged_axes.get_y_axis_label("y")
        mz_label = merged_axes.get_z_axis_label("z")
        merged_quad = self._create_quadcopter()
        mx_arrow = Arrow3D(start=ORIGIN, end=RIGHT * 1.5, color=RED, thickness=0.02)
        my_arrow = Arrow3D(start=ORIGIN, end=UP * 1.5, color=GREEN, thickness=0.02)
        mz_arrow = Arrow3D(start=ORIGIN, end=OUT * 1.5, color=BLUE, thickness=0.02)

        self.play(
            FadeOut(roll_3d), FadeOut(pitch_3d), FadeOut(yaw_3d),
            run_time=1,
        )
        self.play(
            FadeIn(merged_axes), FadeIn(mx_label), FadeIn(my_label), FadeIn(mz_label),
            FadeIn(merged_quad),
            FadeIn(mx_arrow), FadeIn(my_arrow), FadeIn(mz_arrow),
            run_time=1,
        )

        # Merge the three matrices into a multiplication expression
        mult_expr = MathTex(
            r"\mathbf{R}(\psi) \cdot \mathbf{R}(\theta) \cdot \mathbf{R}(\varphi)",
            font_size=28,
        ).to_edge(DOWN, buff=1)

        self.play(
            roll_matrix.animate.move_to(mult_expr),
            pitch_matrix.animate.move_to(mult_expr),
            yaw_matrix.animate.move_to(mult_expr),
            run_time=1.5,
        )
        self.play(
            FadeOut(roll_matrix), FadeOut(pitch_matrix),
            FadeIn(mult_expr),
            run_time=0.5,
        )
        # yaw_matrix is still there visually; swap it out
        self.play(
            Transform(yaw_matrix, mult_expr),
            run_time=0.3,
        )
        self.remove(yaw_matrix)
        self.next_slide()

        # Transform to combined Euler rotation matrix
        combined_matrix = MathTex(
            r"\mathbf{R}(\psi,\theta,\varphi) = \begin{bmatrix}"
            r" C_{\psi}C_{\theta} & C_{\psi}S_{\theta}S_{\varphi} - S_{\psi}C_{\varphi}"
            r" & C_{\psi}S_{\theta}C_{\varphi} + S_{\psi}S_{\varphi} \\"
            r" S_{\psi}C_{\theta} & S_{\psi}S_{\theta}S_{\varphi}+C_{\psi}C_{\varphi}"
            r" & S_{\psi}S_{\theta}C_{\varphi}-C_{\psi}S_{\varphi} \\"
            r" -S_{\theta} & C_{\theta}S_{\varphi} & C_{\theta}C_{\varphi}"
            r" \end{bmatrix}",
            font_size=22,
        ).to_edge(DOWN, buff=0.5)

        self.play(Transform(mult_expr, combined_matrix), run_time=2)
        self.next_slide()

        # Simulate rotations: yaw → pitch → roll
        self.play(
            Rotate(merged_quad, angle=PI / 3, axis=OUT, about_point=ORIGIN),
            run_time=1.5,
        )
        self.play(
            Rotate(merged_quad, angle=PI / 4, axis=UP, about_point=ORIGIN),
            run_time=1.5,
        )
        self.play(
            Rotate(merged_quad, angle=PI / 4, axis=RIGHT, about_point=ORIGIN),
            run_time=1.5,
        )
        self.next_slide()

        # Return to original orientation (reverse order)
        self.play(
            Rotate(merged_quad, angle=-PI / 4, axis=RIGHT, about_point=ORIGIN),
            run_time=1,
        )
        self.play(
            Rotate(merged_quad, angle=-PI / 4, axis=UP, about_point=ORIGIN),
            run_time=1,
        )
        self.play(
            Rotate(merged_quad, angle=-PI / 3, axis=OUT, about_point=ORIGIN),
            run_time=1,
        )

        # Fade out the combined matrix
        self.play(FadeOut(mult_expr), run_time=1)
        self.next_slide()

        # ==============================================================
        # SECTION 5 – Force T_B / T_z and upward movement
        # ==============================================================
        thrust_eq = MathTex(
            r"T_z = k \sum_{i=1}^{4} \omega_{i}^2", font_size=28,
        ).to_edge(LEFT, buff=1).shift(UP * 1)

        vector_T = MathTex(
            r"\mathbf{T}_{B} = \begin{bmatrix} 0 \\ 0 \\ T_z \end{bmatrix}",
            font_size=28,
        ).next_to(thrust_eq, DOWN, buff=0.5, aligned_edge=LEFT)

        self.add_fixed_in_frame_mobjects(thrust_eq, vector_T)
        self.play(FadeIn(thrust_eq), FadeIn(vector_T), run_time=1.5)
        self.next_slide()

        # Move quadcopter upwards (along z / OUT)
        self.play(merged_quad.animate.shift(OUT * 1.5), run_time=2)
        self.next_slide()

        # Return and clean up
        self.play(
            FadeOut(thrust_eq), FadeOut(vector_T),
            merged_quad.animate.shift(-OUT * 1.5),
            run_time=1,
        )
        self.next_slide()

        # ==============================================================
        # SECTION 6 – Sistema de referencia inercial (kept)
        # ==============================================================
        title_sistema = Text(
            "Sistema de referencia inercial", font_size=36, color=YELLOW,
        ).to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(title_sistema)
        self.play(FadeIn(title_sistema), run_time=1)
        self.next_slide()

        # Position vector ξ (left)
        pos_lineal_label = Text(
            "posición lineal", font_size=24, color=WHITE,
        ).to_edge(LEFT, buff=1).shift(UP * 0.5)
        vector_xi_label = MathTex(
            r"\boldsymbol{\xi} = ", font_size=32,
        ).next_to(pos_lineal_label, RIGHT, buff=0.5)
        vector_xi_matrix = MathTex(
            r"\begin{bmatrix} x \\ y \\ z \end{bmatrix}", font_size=32,
        ).next_to(vector_xi_label, RIGHT, buff=0.1)

        self.add_fixed_in_frame_mobjects(
            pos_lineal_label, vector_xi_label, vector_xi_matrix,
        )
        self.play(
            FadeIn(pos_lineal_label),
            FadeIn(vector_xi_label),
            FadeIn(vector_xi_matrix),
            run_time=1.5,
        )
        self.next_slide()

        # Angle vector η (right)
        pos_angular_label = Text(
            "posición angular", font_size=24, color=WHITE,
        ).to_edge(RIGHT, buff=1).shift(UP * 0.5)
        vector_eta_label = MathTex(
            r"\boldsymbol{\eta} = ", font_size=32,
        ).next_to(pos_angular_label, RIGHT, buff=0.5)
        vector_eta_matrix = MathTex(
            r"\begin{bmatrix} \varphi \\ \theta \\ \psi \end{bmatrix}", font_size=32,
        ).next_to(vector_eta_label, RIGHT, buff=0.1)

        self.add_fixed_in_frame_mobjects(
            pos_angular_label, vector_eta_label, vector_eta_matrix,
        )
        self.play(
            FadeIn(pos_angular_label),
            FadeIn(vector_eta_label),
            FadeIn(vector_eta_matrix),
            run_time=1.5,
        )
        self.next_slide()

        # Fade out inertial system
        self.play(
            FadeOut(title_sistema),
            FadeOut(pos_lineal_label),
            FadeOut(vector_xi_label),
            FadeOut(vector_xi_matrix),
            FadeOut(pos_angular_label),
            FadeOut(vector_eta_label),
            FadeOut(vector_eta_matrix),
            run_time=1,
        )

        # ==============================================================
        # SECTION 7 – Sistema de referencia local (kept)
        # ==============================================================
        title_local = Text(
            "Sistema de referencia local", font_size=36, color=YELLOW,
        ).to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(title_local)
        self.play(FadeIn(title_local), run_time=1)
        self.next_slide()

        # Translate and rotate the quadcopter
        translation_vec = np.array([1.5, 1.0, 0.8])
        euler_yaw = PI / 6
        euler_pitch = PI / 8
        euler_roll = PI / 12

        self.play(merged_quad.animate.shift(translation_vec), run_time=1.5)
        self.wait(0.3)
        quadcopter_center = translation_vec
        self.play(
            Rotate(merged_quad, angle=euler_yaw, axis=OUT, about_point=quadcopter_center),
            run_time=1.5,
        )
        self.wait(0.3)
        self.play(
            Rotate(merged_quad, angle=euler_pitch, axis=UP, about_point=quadcopter_center),
            run_time=1.5,
        )
        self.wait(0.3)
        self.play(
            Rotate(merged_quad, angle=euler_roll, axis=RIGHT, about_point=quadcopter_center),
            run_time=1.5,
        )
        self.next_slide()

        # Draw local axes at the new quadcopter position
        local_x_arrow = Arrow3D(start=ORIGIN, end=RIGHT * 0.8, color=RED, thickness=0.02)
        local_y_arrow = Arrow3D(start=ORIGIN, end=UP * 0.8, color=GREEN, thickness=0.02)
        local_z_arrow = Arrow3D(start=ORIGIN, end=OUT * 0.8, color=BLUE, thickness=0.02)

        for arr in (local_x_arrow, local_y_arrow, local_z_arrow):
            arr.shift(translation_vec)
            arr.rotate(euler_yaw, axis=OUT, about_point=quadcopter_center)
            arr.rotate(euler_pitch, axis=UP, about_point=quadcopter_center)
            arr.rotate(euler_roll, axis=RIGHT, about_point=quadcopter_center)

        self.play(
            Create(local_x_arrow), Create(local_y_arrow), Create(local_z_arrow),
            run_time=2,
        )
        self.next_slide()

        # Linear velocity υ (left)
        vel_lin_label = Text(
            "velocidad lineal", font_size=24, color=WHITE,
        ).to_edge(LEFT, buff=1).shift(UP * 0.5)
        vector_upsilon_label = MathTex(
            r"\boldsymbol{\upsilon} = ", font_size=32,
        ).next_to(vel_lin_label, RIGHT, buff=0.5)
        vector_upsilon_matrix = MathTex(
            r"\begin{bmatrix} u \\ v \\ w \end{bmatrix}", font_size=32,
        ).next_to(vector_upsilon_label, RIGHT, buff=0.1)

        self.add_fixed_in_frame_mobjects(
            vel_lin_label, vector_upsilon_label, vector_upsilon_matrix,
        )
        self.play(
            FadeIn(vel_lin_label),
            FadeIn(vector_upsilon_label),
            FadeIn(vector_upsilon_matrix),
            run_time=1.5,
        )
        self.next_slide()

        # Angular velocity ω (right)
        ang_vel_label = Text(
            "velocidad angular", font_size=24, color=WHITE,
        ).shift(RIGHT * 2.5 + UP * 0.5)
        vector_omega_label = MathTex(
            r"\boldsymbol{\omega} = ", font_size=32,
        ).next_to(ang_vel_label, RIGHT, buff=0.3)
        vector_omega_matrix = MathTex(
            r"\begin{bmatrix} p \\ q \\ r \end{bmatrix}", font_size=32,
        ).next_to(vector_omega_label, RIGHT, buff=0.1)

        self.add_fixed_in_frame_mobjects(
            ang_vel_label, vector_omega_label, vector_omega_matrix,
        )
        self.play(
            FadeIn(ang_vel_label),
            FadeIn(vector_omega_label),
            FadeIn(vector_omega_matrix),
            run_time=1.5,
        )
        self.next_slide()
