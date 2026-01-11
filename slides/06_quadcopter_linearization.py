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

        self.play(Transform(jacobian_general, jacobian_eval), run_time=1.5)
        self.play(FadeOut(eval_note), run_time=0.6)

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
        self.play(Transform(jacobian_u, jacobian_u_eval), run_time=1.3)
