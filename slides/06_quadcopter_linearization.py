"""
Linearization of the quadcopter flight dynamics around a fixed point.

Adds a focused scene that evaluates the equilibrium condition and the
corresponding steady input for hover.

Example:
    manim -pql slides/06_quadcopter_linearization.py QuadcopterLinearizationSlide

Author: Sergio Fernández
Date: 2025-01-30
"""

from manim import *
from manim_slides import Slide


class QuadcopterLinearizationSlide(Slide):
    def construct(self):
        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\newcommand{\bigzero}{\mathbf{0}}")
        tex_template.add_to_preamble(r"\newcommand{\rvline}{\;|\;}")

        title = Text(
            "Linealización de dinámica de vuelo de cuadricóptero",
            font_size=34,
            color=WHITE
        )
        title.to_edge(UP)
        self.add(title)
        self.next_slide()

        fixed_point_state = MathTex(
            r"\mathbf{x}^{*} = \mathbf{0}",
            font_size=32
        )
        fixed_point_state.shift(UP * 1.4)
        
        fixed_point_text = Text(
            "Punto fijo: Cuadricóptero alineado con los ejes y velocidades locales en cero.",
            font_size=22,
            color=WHITE,
            t2c={"Punto fijo": YELLOW}
        )
        fixed_point_text.next_to(fixed_point_state, UP, buff=0.3)
        
        self.play(Write(fixed_point_state), Write(fixed_point_text), run_time=1.5)
        self.wait(1.5)
        self.next_slide()

        fixed_point_f = MathTex(
            r"\mathbf{f}(\mathbf{x}^{*}, \mathbf{u}^{*})",
            font_size=32
        )
        fixed_point_f.move_to(ORIGIN)
        
        self.play(FadeIn(fixed_point_f), run_time=1)
        self.wait(0.5)
        
        u_star_eq_target = MathTex(
            r"\mathbf{u}^{*} = \left[\omega_0, \omega_0, \omega_0, \omega_0\right]^{\top}",
            r"\iff",
            r"g - \frac{k}{m}\sum_{i=1}^{4}\omega_i^{2} = 0",
            font_size=30
        )
        u_star_eq_target.move_to(ORIGIN)

        self.play(Transform(fixed_point_f, u_star_eq_target), run_time=1.5)
        u_star_eq = fixed_point_f
        self.wait(3)
        self.next_slide()

        self.play(
            FadeOut(u_star_eq_target),
            FadeOut(fixed_point_text), run_time=1.0
        )

        self.play(FadeOut(fixed_point_state), FadeOut(u_star_eq), FadeOut(title), run_time=0.6)

        jacobians_text = Tex(
            r"Entonces $\mathbf{A}$ y $\mathbf{B}$ estarán dadas por los jacobianos"
            r" $\nabla_{\mathbf{x}} f$ $\nabla_{\mathbf{u}} f$ evaluados en el punto fijo $(\mathbf{x}^*, \mathbf{u}^{*})$.",
            font_size=24,
            color=WHITE
        )
        jacobians_text.to_edge(UP)
        self.play(FadeIn(jacobians_text), run_time=0.8)

        matrix_offset = DOWN * 0.7
        jacobian_general = MathTex(
            r"\nabla_{\mathbf{x}} f(\mathbf{x}, \mathbf{u}) =",
            r"\left(\begin{array}{c c c c c c c}"
            r"\begin{matrix}"
            r"0 & r & -q \\"
            r"-r & 0 & p \\"
            r"q & -p & 0"
            r"\end{matrix} & \rvline &"
            r"\begin{matrix}"
            r"0 & -w & v \\"
            r"w & 0 & -u \\"
            r"-v & u & 0"
            r"\end{matrix} & \rvline &"
            r"\begin{matrix}"
            r"0 & -gC_{\theta} & 0 \\"
            r"-gC_{\theta}C_{\varphi} & gS_{\theta}S_{\varphi} & 0 \\"
            r"-gC_{\theta}S_{\varphi} & -gS_{\theta}C_{\varphi} & 0"
            r"\end{matrix} & \rvline & \bigzero \\"
            r"\hline"
            r"\bigzero & \rvline &"
            r"\begin{matrix}"
            r"0 & -r \frac{I_{zz}-I_{yy}}{I_{xx}} & -q \frac{I_{zz}-I_{yy}}{I_{xx}} \\"
            r"-r \frac{I_{xx}-I_{zz}}{I_{yy}} & 0 & -p \frac{I_{xx}-I_{zz}}{I_{yy}} \\"
            r"-q \frac{I_{yy}-I_{xx}}{I_{zz}} & -p \frac{I_{yy}-I_{xx}}{I_{zz}} & 0"
            r"\end{matrix} & \rvline & \bigzero & \rvline & \bigzero \\"
            r"\hline"
            r"\bigzero & \rvline &"
            r"\begin{matrix}"
            r"1 & S_{\varphi} \frac{S_{\theta}}{C_{\theta}} & C_{\varphi} \frac{S_{\theta}}{C_{\theta}} \\"
            r"0 & C_{\varphi} & -S_{\varphi} \\"
            r"0 & \frac{S_{\varphi}}{C_{\theta}} & \frac{C_{\varphi}}{C_{\theta}}"
            r"\end{matrix} & \rvline &"
            r"\begin{matrix}"
            r"(qC_{\varphi}-rS_{\varphi}) \frac{S_{\theta}}{C_{\theta}} &"
            r"(qS_{\varphi}+rC_{\varphi}) \frac{1}{C_{\theta}^{2}} & 0 \\"
            r"-qS_{\varphi}-rC_{\varphi} & 0 & 0 \\"
            r"(qC_{\varphi}-rS_{\varphi}) \frac{1}{C_{\theta}} &"
            r"(qS_{\varphi}+rC_{\varphi}) \frac{S_{\theta}}{C_{\theta}^{2}} & 0"
            r"\end{matrix} & \rvline & \bigzero \\"
            r"\hline"
            r"\begin{matrix}"
            r"1 & 0 & 0 \\"
            r"0 & 1 & 0 \\"
            r"0 & 0 & 1"
            r"\end{matrix} & \rvline & \bigzero & \rvline & \bigzero & \rvline & \bigzero"
            r"\end{array}\right)",
            font_size=18,
            tex_template=tex_template
        )
        jacobian_general.next_to(jacobians_text, DOWN, buff=0.5)
        jacobian_general.shift(matrix_offset)
        self.play(Write(jacobian_general), run_time=1)
        self.next_slide()

        eval_note = Tex(
            r"Evaluando en el punto fijo",
            font_size=22,
            color=WHITE
        )
        eval_note.next_to(jacobian_general, DOWN, buff=0.3)
        self.play(FadeIn(eval_note), run_time=0.6)

        jacobian_eval = MathTex(
            r"\nabla_{\mathbf{x}} f(\mathbf{x}^*, \mathbf{u}^*) =",
            r"\left(\begin{array}{c c c c c c c}"
            r"\bigzero & \rvline & \bigzero & \rvline &"
            r"\begin{matrix}"
            r"0 & -g & 0 \\"
            r"-g & 0 & 0 \\"
            r"0 & 0 & 0"
            r"\end{matrix} & \rvline & \bigzero \\"
            r"\hline"
            r"\bigzero & \rvline & \bigzero & \rvline & \bigzero & \rvline & \bigzero \\"
            r"\hline"
            r"\bigzero & \rvline &"
            r"\begin{matrix}"
            r"1 & 0 & 0 \\"
            r"0 & 1 & 0 \\"
            r"0 & 0 & 1"
            r"\end{matrix} & \rvline & \bigzero & \rvline & \bigzero \\"
            r"\hline"
            r"\begin{matrix}"
            r"1 & 0 & 0 \\"
            r"0 & 1 & 0 \\"
            r"0 & 0 & 1"
            r"\end{matrix} & \rvline & \bigzero & \rvline & \bigzero & \rvline & \bigzero"
            r"\end{array}\right)",
            font_size=18,
            tex_template=tex_template
        )
        jacobian_eval.move_to(jacobian_general.get_center())
        jacobian_eval.shift(UP * 0.4)

        self.play(Transform(jacobian_general, jacobian_eval), run_time=1.5)
        self.play(FadeOut(eval_note), run_time=0.6)
        self.next_slide()

        jacobian_x = jacobian_general
        a_symbol = MathTex(r"\mathbf{A}=", font_size=28)
        a_symbol.move_to(jacobian_x[0].get_center())
        self.play(Transform(jacobian_x[0], a_symbol), run_time=0.8)
        self.play(jacobian_x.animate.to_edge(LEFT).shift(matrix_offset), run_time=0.8)

        jacobian_u = MathTex(
            r"\nabla_{\mathbf{u}} f(\mathbf{x}, \mathbf{u}) =",
            r"2 \cdot \left(\begin{array}{c}"
            r"\begin{matrix}"
            r"0 & 0 & 0 & 0 \\"
            r"0 & 0 & 0 & 0 \\"
            r"-km^{-1}\omega_1 & -km^{-1}\omega_2 & -km^{-1}\omega_3 & -km^{-1}\omega_4 \\"
            r"0 & -\ell bI_{xx}^{-1}\omega_2 & 0 & -\ell bI_{xx}^{-1}\omega_4 \\"
            r"-\ell bI_{yy}^{-1}\omega_1 & 0 & -\ell bI_{yy}^{-1}\omega_3 & 0 \\"
            r"-\ell bI_{zz}^{-1}\omega_1 &"
            r"\ell bI_{zz}^{-1}\omega_2 &"
            r"-\ell bI_{zz}^{-1}\omega_3 &"
            r"\ell bI_{zz}^{-1}\omega_4"
            r"\end{matrix}"
            r"\\ \hline"
            r"\bigzero"
            r"\end{array}\right)",
            font_size=18,
            tex_template=tex_template
        )
        jacobian_u.next_to(jacobian_x, RIGHT, buff=0.8)
        self.play(FadeIn(jacobian_u), run_time=1)
        self.next_slide()

        jacobian_u_eval = MathTex(
            r"\mathbf{B} =",
            r"2 \cdot \left(\begin{array}{c}"
            r"\begin{matrix}"
            r"0 & 0 & 0 & 0 \\"
            r"0 & 0 & 0 & 0 \\"
            r"-km^{-1}\omega_0 & -km^{-1}\omega_0 & -km^{-1}\omega_0 & -km^{-1}\omega_0 \\"
            r"0 & -\ell bI_{xx}^{-1}\omega_0 & 0 & -\ell bI_{xx}^{-1}\omega_0 \\"
            r"-\ell bI_{yy}^{-1}\omega_0 & 0 & -\ell bI_{yy}^{-1}\omega_0 & 0 \\"
            r"-\ell bI_{zz}^{-1}\omega_0 &"
            r"\ell bI_{zz}^{-1}\omega_0 &"
            r"-\ell bI_{zz}^{-1}\omega_0 &"
            r"\ell bI_{zz}^{-1}\omega_0"
            r"\end{matrix}"
            r"\\ \hline"
            r"\bigzero"
            r"\end{array}\right)",
            font_size=18,
            tex_template=tex_template
        )
        jacobian_u_eval.move_to(jacobian_u.get_center())
        jacobian_u_eval.shift(UP * 0.4)
        self.play(
            FadeOut(jacobians_text),
            Transform(jacobian_u, jacobian_u_eval),
            run_time=1.3
        )

        controllability_legend = Tex(
            r"Se puede demostrar que el cuadricoptero no es controlable en el sentido de Kalman,",
            font_size=20,
            tex_template=tex_template
        )
        controllability_eq = MathTex(
            r"\mathrm{rango}(R(A, B)) < 12",
            font_size=26,
            tex_template=tex_template
        )
        controllability_group = VGroup(controllability_legend, controllability_eq).arrange(
            DOWN,
            buff=0.2
        )
        controllability_group.next_to(jacobian_u, DOWN, buff=0.5)
        self.play(FadeIn(controllability_legend), run_time=0.8)
        self.play(FadeIn(controllability_eq), run_time=0.8)
        self.next_slide()

        subsystem_legend = Tex(
            r"Sin embargo, si se considera el subsistema asociado a $\mathbf{y}$,",
            font_size=20,
            tex_template=tex_template
        )
        subsystem_eq = MathTex(
            r"\mathbf{y}= (\varphi, \theta, \psi, z, p,q, r, w)^{\top}",
            font_size=24,
            tex_template=tex_template
        )
        subsystem_group = VGroup(subsystem_legend, subsystem_eq).arrange(DOWN, buff=0.15)
        subsystem_group.to_edge(UP).shift(DOWN * 0.2)
        self.play(FadeIn(subsystem_legend), run_time=0.7)
        self.play(FadeIn(subsystem_eq), run_time=0.7)

        extract_legend = Tex(
            r"extraemos las submatrices asociadas a $\mathbf{y}$",
            font_size=20,
            tex_template=tex_template
        )
        extract_legend.next_to(subsystem_group, DOWN, buff=0.2)
        self.play(FadeIn(extract_legend), run_time=0.7)

        a_tilde = MathTex(
            r"\mathbf{\tilde{A}} =",
            r"\begin{bmatrix}"
            r"\bigzero & \rvline & \mathbf{I}_{4} \\"
            r"\hline"
            r"\bigzero & \rvline & \bigzero"
            r"\end{bmatrix}",
            font_size=18,
            tex_template=tex_template
        )
        a_tilde.move_to(jacobian_x.get_center())

        b_tilde = MathTex(
            r"\mathbf{\tilde{B}} =",
            r"\begin{bmatrix}"
            r"\bigzero_{4\times4} \\"
            r"\hline"
            r"\\[-2ex]"
            r"\begin{matrix}"
            r"-km^{-1}\omega_0 & -km^{-1}\omega_0 & -km^{-1}\omega_0 & -km^{-1}\omega_0 \\"
            r"0 & -\ell bI_{xx}^{-1}\omega_0 & 0 & -\ell bI_{xx}^{-1}\omega_0 \\"
            r"-\ell bI_{yy}^{-1}\omega_0 & 0 & -\ell bI_{yy}^{-1}\omega_0 & 0 \\"
            r"-\ell bI_{zz}^{-1}\omega_0 &"
            r"\ell bI_{zz}^{-1}\omega_0 &"
            r"-\ell bI_{zz}^{-1}\omega_0 &"
            r"\ell bI_{zz}^{-1}\omega_0"
            r"\end{matrix}"
            r"\end{bmatrix}",
            font_size=18,
            tex_template=tex_template
        )
        b_tilde.move_to(jacobian_u.get_center())

        self.play(
            Transform(jacobian_x, a_tilde),
            Transform(jacobian_u, b_tilde),
            run_time=1.3
        )
        self.wait(1.0)
        self.next_slide()

        fade_targets = VGroup(
            jacobian_x,
            jacobian_u,
            controllability_group,
            subsystem_group,
            extract_legend
        )
        self.play(FadeOut(fade_targets), run_time=0.8)
        self.wait(1.0)

        controllability_matrix = MathTex(
            r"R\left(\mathbf{\tilde{B}}, \mathbf{\tilde{A}}\right) =",
            r"\left[\mathbf{\tilde{B}}, \mathbf{\tilde{A}}\mathbf{\tilde{B}}\right]",
            font_size=24,
            tex_template=tex_template
        )
        controllability_matrix.move_to(ORIGIN)
        self.play(FadeIn(controllability_matrix), run_time=0.9)
        self.wait(1.0)
        self.next_slide()

        controllability_matrix_expanded = MathTex(
            r"R\left(\mathbf{\tilde{B}}, \mathbf{\tilde{A}}\right) =",
            r"\begin{bmatrix}"
            r"\mathbf{0} & \mathbf{B}_{3:6} \\"
            r"\mathbf{B}_{3:6} & \mathbf{0}"
            r"\end{bmatrix}",
            font_size=24,
            tex_template=tex_template
        )
        controllability_matrix_expanded.move_to(controllability_matrix.get_center())
        self.play(Transform(controllability_matrix, controllability_matrix_expanded), run_time=1.0)
        kalman_legend = Tex(
            r"Aplicamos el criterio de Kalman,",
            font_size=20,
            tex_template=tex_template
        )
        kalman_eq = MathTex(
            r"\mathrm{rango}\left(R\left(\mathbf{\tilde{A}}, \mathbf{\tilde{B}}\right)\right)= 8",
            font_size=26,
            tex_template=tex_template
        )
        kalman_group = VGroup(kalman_legend, kalman_eq).arrange(DOWN, buff=0.2)
        kalman_group.move_to(ORIGIN)
        self.play(FadeOut(controllability_matrix), run_time=0.6)
        self.play(FadeIn(kalman_group), run_time=0.9)
        self.wait(1.0)
        self.next_slide()

        self.play(FadeOut(kalman_group), run_time=0.6)
        system_legend = Tex(
            r"Consideramos el sistema:",
            font_size=20,
            tex_template=tex_template
        )
        system_eq = MathTex(
            r"\dot{\mathbf{y}} = \mathbf{\tilde{A}}\mathbf{y} + \mathbf{\tilde{B}}\mathbf{u}",
            font_size=26,
            tex_template=tex_template
        )
        system_group = VGroup(system_legend, system_eq).arrange(DOWN, buff=0.2)
        system_group.move_to(ORIGIN)
        self.play(FadeIn(system_group), run_time=0.9)
        self.wait(1.0)
        self.next_slide()

        decoupled_legend = Tex(
            r"Al desacoplar las matrices,",
            font_size=20,
            tex_template=tex_template
        )
        decoupled_eq = MathTex(
            r"\begin{aligned}"
            r"\mathbf{A}^{(z)}+\mathbf{B}^{(z)}\mathbf{K}^{(z)}="
            r"\begin{bmatrix}0&1\\0&0\end{bmatrix}"
            r"-\frac{2k}{m}\omega_0"
            r"\begin{bmatrix}0&0\\ g_{z1}&g_{z2}\end{bmatrix},"
            r"\\ \\"
            r"\mathbf{A}^{(\psi)}+\mathbf{B}^{(\psi)}\mathbf{K}^{(\psi)}="
            r"\begin{bmatrix}0&1\\0&0\end{bmatrix}"
            r"+\frac{2\ell b}{I_{zz}}\omega_0"
            r"\begin{bmatrix}0&0\\ -g_{\psi1}+g_{\psi2}&-g_{\psi3}+g_{\psi4}\end{bmatrix},"
            r"\\ \\"
            r"\mathbf{A}^{(\theta)}+\mathbf{B}^{(\theta)}\mathbf{K}^{(\theta)}="
            r"\begin{bmatrix}0&1\\0&0\end{bmatrix}"
            r"+\frac{2\ell b}{I_{yy}}\omega_0"
            r"\begin{bmatrix}0&0\\ g_{\theta1}&g_{\theta2}\end{bmatrix},"
            r"\\ \\"
            r"\mathbf{A}^{(\varphi)}+\mathbf{B}^{(\varphi)}\mathbf{K}^{(\varphi)}="
            r"\begin{bmatrix}0&1\\0&0\end{bmatrix}"
            r"+\frac{2\ell b}{I_{xx}}\omega_0"
            r"\begin{bmatrix}0&0\\ g_{\varphi1}&g_{\varphi2}\end{bmatrix}"
            r"\end{aligned}",
            font_size=20,
            tex_template=tex_template
        )
        decoupled_legend.move_to(system_legend.get_center())
        system_legend.move_to(UP)
        self.play(
            Transform(system_legend, decoupled_legend),
            Transform(system_eq, decoupled_eq),
            run_time=1.1
        )
        self.next_slide()
