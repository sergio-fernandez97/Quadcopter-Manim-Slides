"""
Linearization of the quadcopter flight dynamics around a fixed point.

Covers the full linear control design pipeline:
equilibrium → linearization → non-controllability diagnosis →
controllable subsystem extraction → decoupling into 4 second-order channels →
pole placement via Poincaré diagram → gain matrices → state-feedback control law.

Example:
    manim -pql slides/06_quadcopter_linearization.py QuadcopterLinearizationSlide

Author: Sergio Fernández
Date: 2025-01-30
"""

from manim import *
from manim_slides import Slide


class QuadcopterLinearizationSlide(Slide):
    def construct(self):
        # ── TexTemplate (only needed for A and B matrices in scene 2) ──────────
        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\newcommand{\bigzero}{\mathbf{0}}")
        tex_template.add_to_preamble(r"\newcommand{\rvline}{\;|\;}")

        MAX_W = config.frame_width - 1.4

        def make_box(content, color=GRAY, fill_opacity=0.15, stroke_width=1):
            box = RoundedRectangle(
                corner_radius=0.2,
                width=content.width + 0.8,
                height=content.height + 0.5,
                color=color,
                fill_opacity=fill_opacity,
                stroke_width=stroke_width,
            )
            box.move_to(content)
            return box

        # ── Title (never fades out) ───────────────────────────────────────────
        title = Text(
            "Linealización de dinámica de vuelo de cuadricóptero",
            font_size=38,
            color=YELLOW,
        )
        title.to_edge(UP, buff=0.3)
        if title.width > MAX_W:
            title.scale_to_fit_width(MAX_W)
        self.play(FadeIn(title))
        self.wait(0.5)
        self.next_slide()

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 1 – Fixed point and hover input
        # ══════════════════════════════════════════════════════════════════════
        sc1_label = Text("Punto fijo", font_size=26, color=BLUE)
        sc1_label.move_to(UP * 2.3)

        # Description subtitle in a box
        sc1_desc = Text(
            "Cuadricóptero alineado con los ejes y velocidades en cero.",
            font_size=20,
            color=GRAY_B,
        )
        sc1_desc.next_to(sc1_label, DOWN, buff=0.2)
        sc1_desc_box = make_box(sc1_desc)
        self.play(FadeIn(sc1_label), FadeIn(sc1_desc), FadeIn(sc1_desc_box))
        self.wait(0.5)

        # x* = 0 box
        xstar = MathTex(r"\mathbf{x}^{*} = \mathbf{0}", font_size=28)
        xstar.move_to(UP * 0.6)
        xstar_box = make_box(xstar)
        self.play(FadeIn(xstar), FadeIn(xstar_box))
        self.wait(0.5)
        self.next_slide()

        # Without fading x*, note that evaluating f(x*,u*) zeros all RHS except ẇ
        eval_note = Tex(
            r"Al evaluar $f(\mathbf{x}^{*}, \mathbf{u}^{*})$, todos los lados"
            r" derechos son cero, salvo $\dot{w}$:",
            font_size=22,
            color=GRAY_B,
        )
        eval_note.move_to(ORIGIN)
        if eval_note.width > MAX_W:
            eval_note.scale_to_fit_width(MAX_W)
        self.play(FadeIn(eval_note))
        self.wait(0.3)

        wdot_eq = MathTex(
            r"\dot{w}^{*} = 0 \iff 0 = g - \frac{k}{m}\sum_{i=1}^{4}\omega_i^{2}",
            font_size=26,
        )
        wdot_eq.next_to(eval_note, DOWN, buff=0.3)
        self.play(FadeIn(wdot_eq))
        self.wait(0.5)
        self.next_slide()

        # Particular solution: u* and explicit ω₀
        ustar_intro = Tex(r"Solución particular:", font_size=22, color=GRAY_B)
        ustar_intro.next_to(wdot_eq, DOWN, buff=0.4)
        ustar = MathTex(
            r"\mathbf{u}^{*} = \left[\omega_0,\omega_0,\omega_0,\omega_0\right]^{\top}",
            font_size=26,
        )
        ustar.next_to(ustar_intro, DOWN, buff=0.2)
        donde_txt = Tex(r"donde", font_size=22, color=GRAY_B)
        donde_txt.next_to(ustar, DOWN, buff=0.2)
        omega_def = MathTex(
            r"\omega_0 = \sqrt{\frac{g\cdot m}{4\cdot k}}",
            font_size=26,
            color=GREEN,
        )
        omega_def.next_to(donde_txt, DOWN, buff=0.15)
        self.play(FadeIn(ustar_intro), FadeIn(ustar))
        self.wait(0.3)
        self.play(FadeIn(donde_txt), FadeIn(omega_def))
        self.wait(0.5)
        self.next_slide()

        # FadeOut scene 1 (keep title)
        sc1_mobjects = VGroup(
            sc1_label, sc1_desc, sc1_desc_box,
            xstar, xstar_box,
            eval_note, wdot_eq,
            ustar_intro, ustar, donde_txt, omega_def,
        )
        self.play(FadeOut(sc1_mobjects))
        self.wait(0.3)

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 2 – Jacobians: general form → evaluated as A and B
        # ══════════════════════════════════════════════════════════════════════
        sc2_label = Tex(
            r"Entonces $\mathbf{A}$ y $\mathbf{B}$ estarán dadas por los jacobianos"
            r" $\nabla_{\mathbf{x}} f$ y $\nabla_{\mathbf{u}} f$"
            r" evaluados en $(\mathbf{x}^{*}, \mathbf{u}^{*})$.",
            font_size=22,
            color=GRAY_B,
        )
        sc2_label.move_to(UP * 2.3)
        if sc2_label.width > MAX_W:
            sc2_label.scale_to_fit_width(MAX_W)
        self.play(FadeIn(sc2_label))
        self.wait(0.3)

        # General ∇_x f (before evaluation)
        jac_x_general = MathTex(
            r"\nabla_{\mathbf{x}} f(\mathbf{x}, \mathbf{u}) =",
            r"\left(\begin{array}{c c c c c c c}"
            r"\begin{matrix}0 & r & -q \\ -r & 0 & p \\ q & -p & 0\end{matrix}"
            r" & \rvline &"
            r"\begin{matrix}0 & -w & v \\ w & 0 & -u \\ -v & u & 0\end{matrix}"
            r" & \rvline &"
            r"\begin{matrix}0 & -gC_{\theta} & 0 \\"
            r"-gC_{\theta}C_{\varphi} & gS_{\theta}S_{\varphi} & 0 \\"
            r"-gC_{\theta}S_{\varphi} & -gS_{\theta}C_{\varphi} & 0\end{matrix}"
            r" & \rvline & \bigzero \\"
            r"\hline"
            r"\bigzero & \rvline &"
            r"\begin{matrix}0 & -r\frac{I_{zz}-I_{yy}}{I_{xx}} & -q\frac{I_{zz}-I_{yy}}{I_{xx}} \\"
            r"-r\frac{I_{xx}-I_{zz}}{I_{yy}} & 0 & -p\frac{I_{xx}-I_{zz}}{I_{yy}} \\"
            r"-q\frac{I_{yy}-I_{xx}}{I_{zz}} & -p\frac{I_{yy}-I_{xx}}{I_{zz}} & 0\end{matrix}"
            r" & \rvline & \bigzero & \rvline & \bigzero \\"
            r"\hline"
            r"\bigzero & \rvline &"
            r"\begin{matrix}1 & S_{\varphi}\frac{S_{\theta}}{C_{\theta}} & C_{\varphi}\frac{S_{\theta}}{C_{\theta}} \\"
            r"0 & C_{\varphi} & -S_{\varphi} \\"
            r"0 & \frac{S_{\varphi}}{C_{\theta}} & \frac{C_{\varphi}}{C_{\theta}}\end{matrix}"
            r" & \rvline &"
            r"\begin{matrix}(qC_{\varphi}-rS_{\varphi})\frac{S_{\theta}}{C_{\theta}} &"
            r"(qS_{\varphi}+rC_{\varphi})\frac{1}{C_{\theta}^{2}} & 0 \\"
            r"-qS_{\varphi}-rC_{\varphi} & 0 & 0 \\"
            r"(qC_{\varphi}-rS_{\varphi})\frac{1}{C_{\theta}} &"
            r"(qS_{\varphi}+rC_{\varphi})\frac{S_{\theta}}{C_{\theta}^{2}} & 0\end{matrix}"
            r" & \rvline & \bigzero \\"
            r"\hline"
            r"\begin{matrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{matrix}"
            r" & \rvline & \bigzero & \rvline & \bigzero & \rvline & \bigzero"
            r"\end{array}\right)",
            font_size=14,
            tex_template=tex_template,
        )
        jac_x_general.next_to(sc2_label, DOWN, buff=0.35)
        if jac_x_general.width > MAX_W:
            jac_x_general.scale_to_fit_width(MAX_W)
        self.play(FadeIn(jac_x_general))
        self.wait(0.5)
        self.next_slide()

        # Evaluate at fixed point → transform to A
        eval_note = Tex(r"Evaluando en el punto fijo:", font_size=20, color=GRAY_B)
        eval_note.next_to(jac_x_general, DOWN, buff=0.15)
        self.play(FadeIn(eval_note))
        self.wait(0.2)

        jac_x_eval = MathTex(
            r"\mathbf{A} =",
            r"\left(\begin{array}{c c c c c c c}"
            r"\bigzero & \rvline & \bigzero & \rvline &"
            r"\begin{matrix}0 & -g & 0 \\ -g & 0 & 0 \\ 0 & 0 & 0\end{matrix}"
            r" & \rvline & \bigzero \\"
            r"\hline"
            r"\bigzero & \rvline & \bigzero & \rvline & \bigzero & \rvline & \bigzero \\"
            r"\hline"
            r"\bigzero & \rvline &"
            r"\begin{matrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{matrix}"
            r" & \rvline & \bigzero & \rvline & \bigzero \\"
            r"\hline"
            r"\begin{matrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{matrix}"
            r" & \rvline & \bigzero & \rvline & \bigzero & \rvline & \bigzero"
            r"\end{array}\right)",
            font_size=14,
            tex_template=tex_template,
        )
        jac_x_eval.move_to(jac_x_general.get_center())
        self.play(Transform(jac_x_general, jac_x_eval), FadeOut(eval_note))
        self.wait(0.5)
        self.next_slide()

        # Move A to left; show general ∇_u f on the right
        self.play(jac_x_general.animate.to_edge(LEFT, buff=0.2).shift(DOWN * 0.3))

        jac_u_general = MathTex(
            r"\nabla_{\mathbf{u}} f(\mathbf{x}, \mathbf{u}) =",
            r"2\!\cdot\!\left(\begin{array}{c}"
            r"\begin{matrix}"
            r"0 & 0 & 0 & 0 \\"
            r"0 & 0 & 0 & 0 \\"
            r"-km^{-1}\omega_1 & -km^{-1}\omega_2 & -km^{-1}\omega_3 & -km^{-1}\omega_4 \\"
            r"0 & -\ell bI_{xx}^{-1}\omega_2 & 0 & \ell bI_{xx}^{-1}\omega_4 \\"
            r"-\ell bI_{yy}^{-1}\omega_1 & 0 & \ell bI_{yy}^{-1}\omega_3 & 0 \\"
            r"-\ell bI_{zz}^{-1}\omega_1 & \ell bI_{zz}^{-1}\omega_2 &"
            r"-\ell bI_{zz}^{-1}\omega_3 & \ell bI_{zz}^{-1}\omega_4"
            r"\end{matrix}"
            r"\\ \hline \bigzero"
            r"\end{array}\right)",
            font_size=14,
            tex_template=tex_template,
        )
        jac_u_general.next_to(jac_x_general, RIGHT, buff=0.4)
        if jac_u_general.width > MAX_W / 2:
            jac_u_general.scale_to_fit_width(MAX_W / 2)
        self.play(FadeIn(jac_u_general))
        self.wait(0.5)
        self.next_slide()

        # Evaluate ∇_u f at hover → transform to B
        jac_u_eval = MathTex(
            r"\mathbf{B} =",
            r"2\!\cdot\!\left(\begin{array}{c}"
            r"\begin{matrix}"
            r"0 & 0 & 0 & 0 \\"
            r"0 & 0 & 0 & 0 \\"
            r"-km^{-1}\omega_0 & -km^{-1}\omega_0 & -km^{-1}\omega_0 & -km^{-1}\omega_0 \\"
            r"0 & -\ell bI_{xx}^{-1}\omega_0 & 0 & -\ell bI_{xx}^{-1}\omega_0 \\"
            r"-\ell bI_{yy}^{-1}\omega_0 & 0 & -\ell bI_{yy}^{-1}\omega_0 & 0 \\"
            r"-\ell bI_{zz}^{-1}\omega_0 & \ell bI_{zz}^{-1}\omega_0 &"
            r"-\ell bI_{zz}^{-1}\omega_0 & \ell bI_{zz}^{-1}\omega_0"
            r"\end{matrix}"
            r"\\ \hline \bigzero"
            r"\end{array}\right)",
            font_size=14,
            tex_template=tex_template,
        )
        jac_u_eval.move_to(jac_u_general.get_center())
        self.play(Transform(jac_u_general, jac_u_eval))
        self.wait(0.5)
        self.next_slide()

        # FadeOut scene 2
        sc2_mobjects = VGroup(sc2_label, jac_x_general, jac_u_general)
        self.play(FadeOut(sc2_mobjects))
        self.wait(0.3)

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 3 – Non-controllability + subsystem y
        # ══════════════════════════════════════════════════════════════════════
        sc3_label = Text("No controlabilidad del sistema completo", font_size=26, color=BLUE)
        sc3_label.move_to(UP * 2.3)
        self.play(FadeIn(sc3_label))
        self.wait(0.5)

        # Kalman non-controllability statement + rank < 12
        kalman_text = Text(
            "El cuadricóptero no es controlable en el sentido de Kalman,",
            font_size=21,
            color=GRAY_B,
        )
        kalman_text.move_to(UP * 1.5)
        if kalman_text.width > MAX_W:
            kalman_text.scale_to_fit_width(MAX_W)
        self.play(FadeIn(kalman_text))
        self.wait(0.3)

        rank_eq = MathTex(
            r"\mathrm{rango}(\mathcal{R}(A,B)) < 12",
            font_size=26,
        )
        rank_eq.next_to(kalman_text, DOWN, buff=0.25)
        rank_box = make_box(rank_eq, color=RED, fill_opacity=0.1, stroke_width=2)
        self.play(FadeIn(rank_eq), FadeIn(rank_box))
        self.wait(0.5)

        # Exclusion text (updated per PR)
        excl_text = Text(
            "Si se excluyen x, y, u, v y sus velocidades locales,\n"
            "se considera el subsistema asociado a,",
            font_size=21,
            color=GRAY_B,
        )
        excl_text.next_to(rank_box, DOWN, buff=0.3)
        if excl_text.width > MAX_W:
            excl_text.scale_to_fit_width(MAX_W)
        self.play(FadeIn(excl_text))
        self.wait(0.5)

        # Subsystem y (green highlight)
        y_subsys = MathTex(
            r"\mathbf{y} = (\varphi,\,\theta,\,\psi,\,z,\,p,\,q,\,r,\,w)^{\top}",
            font_size=26,
            color=GREEN,
        )
        y_subsys.next_to(excl_text, DOWN, buff=0.3)
        y_box = make_box(y_subsys, color=GREEN, fill_opacity=0.1, stroke_width=2)
        self.play(FadeIn(y_subsys), FadeIn(y_box))
        self.wait(0.5)

        # Dynamics equation
        y_dyn = MathTex(
            r"\dot{\mathbf{y}} = \tilde{A}\,\mathbf{y} + \tilde{B}\,\mathbf{u}",
            font_size=26,
        )
        y_dyn.next_to(y_box, DOWN, buff=0.3)
        self.play(FadeIn(y_dyn))
        self.wait(0.5)
        self.next_slide()

        # FadeOut scene 3
        sc3_mobjects = VGroup(sc3_label, kalman_text, rank_eq, rank_box, excl_text, y_subsys, y_box, y_dyn)
        self.play(FadeOut(sc3_mobjects))
        self.wait(0.3)

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 4 – Controllability of subsystem (accumulative, all on screen)
        # ══════════════════════════════════════════════════════════════════════
        sc4_label = Text("Controlabilidad del subsistema", font_size=26, color=BLUE)
        sc4_label.move_to(UP * 2.3)
        self.play(FadeIn(sc4_label))
        self.wait(0.5)

        step1 = MathTex(
            r"\mathcal{R}(\tilde{A},\tilde{B}) = [\tilde{B},\;\tilde{A}\tilde{B}]",
            font_size=24,
        )
        step2 = MathTex(
            r"= \begin{bmatrix} \mathbf{0} & B_{3:6} \\ B_{3:6} & \mathbf{0} \end{bmatrix}",
            font_size=24,
        )
        step3 = MathTex(
            r"\mathrm{rango}(\mathcal{R}(\tilde{A},\tilde{B})) = 8",
            font_size=24,
            color=GREEN,
        )
        step4 = Text(
            "La pareja (Ã, B̃) es controlable",
            font_size=22,
            color=GREEN,
        )

        all_steps = VGroup(step1, step2, step3, step4).arrange(DOWN, buff=0.35)
        all_steps.move_to(DOWN * 0.2)

        ctrl_box = make_box(all_steps)

        # Reveal all steps one by one, keep on screen
        self.play(FadeIn(step1))
        self.wait(0.3)
        self.play(FadeIn(step2))
        self.wait(0.3)
        self.play(FadeIn(step3))
        self.wait(0.3)
        self.play(FadeIn(step4))
        self.wait(0.3)
        self.play(FadeIn(ctrl_box))
        self.wait(0.5)
        self.next_slide()

        # FadeOut scene 4
        sc4_mobjects = VGroup(sc4_label, all_steps, ctrl_box)
        self.play(FadeOut(sc4_mobjects))
        self.wait(0.3)

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 5 – Decoupling into 4 second-order channels
        # ══════════════════════════════════════════════════════════════════════
        sc5_label = Text("Desacoplamiento en 4 canales de segundo orden", font_size=26, color=BLUE)
        sc5_label.move_to(UP * 2.3)
        self.play(FadeIn(sc5_label))
        self.wait(0.5)

        desc = Text(
            "Cada canal tiene la misma dinámica base:",
            font_size=22,
            color=GRAY_B,
        )
        common_form = MathTex(
            r"A^{(i)} = \begin{bmatrix}0&1\\0&0\end{bmatrix},\quad"
            r"\dot{x}^{(i)} = A^{(i)}x^{(i)} + B^{(i)}u",
            font_size=24,
        )
        header = VGroup(desc, common_form).arrange(DOWN, buff=0.25)
        header.move_to(UP * 1.3)
        self.play(FadeIn(header))
        self.wait(0.5)

        # 4 channels in 2×2 grid
        ch_zw = MathTex(
            r"\begin{bmatrix}\dot{z}\\\dot{w}\end{bmatrix}"
            r"= A^{(z)}\begin{bmatrix}z\\w\end{bmatrix}"
            r"- \frac{2k}{m}\omega_0\,B^{(z)}\mathbf{u}",
            font_size=19,
        )
        ch_psi = MathTex(
            r"\begin{bmatrix}\dot{\psi}\\\dot{r}\end{bmatrix}"
            r"= A^{(\psi)}\begin{bmatrix}\psi\\r\end{bmatrix}"
            r"+ \frac{2\ell b}{I_{zz}}\omega_0\,B^{(\psi)}\mathbf{u}",
            font_size=19,
        )
        ch_theta = MathTex(
            r"\begin{bmatrix}\dot{\theta}\\\dot{q}\end{bmatrix}"
            r"= A^{(\theta)}\begin{bmatrix}\theta\\q\end{bmatrix}"
            r"+ \frac{2\ell b}{I_{yy}}\omega_0\,B^{(\theta)}\mathbf{u}",
            font_size=19,
        )
        ch_phi = MathTex(
            r"\begin{bmatrix}\dot{\varphi}\\\dot{p}\end{bmatrix}"
            r"= A^{(\varphi)}\begin{bmatrix}\varphi\\p\end{bmatrix}"
            r"+ \frac{2\ell b}{I_{xx}}\omega_0\,B^{(\varphi)}\mathbf{u}",
            font_size=19,
        )

        # Left col: z-w, θ-q; Right col: ψ-r, φ-p
        left_col = VGroup(ch_zw, ch_theta).arrange(DOWN, buff=0.4)
        right_col = VGroup(ch_psi, ch_phi).arrange(DOWN, buff=0.4)
        grid = VGroup(left_col, right_col).arrange(RIGHT, buff=1.0)
        grid.move_to(DOWN * 0.8)

        if grid.width > MAX_W:
            grid.scale_to_fit_width(MAX_W)

        self.play(FadeIn(grid))
        self.wait(0.5)
        self.next_slide()

        # FadeOut scene 5
        sc5_mobjects = VGroup(sc5_label, header, grid)
        self.play(FadeOut(sc5_mobjects))
        self.wait(0.3)

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 6 – Closed-loop + characteristic polynomials
        # ══════════════════════════════════════════════════════════════════════
        sc6_label = Text("Polinomios característicos por canal", font_size=26, color=BLUE)
        sc6_label.move_to(UP * 2.3)
        self.play(FadeIn(sc6_label))
        self.wait(0.5)

        cl_text = Text(
            "Circuito cerrado por canal: A⁽ⁱ⁾ + B⁽ⁱ⁾K⁽ⁱ⁾,  i ∈ {z,ψ,θ,φ}",
            font_size=20,
            color=GRAY_B,
        )
        cl_text.move_to(UP * 1.5)
        self.play(FadeIn(cl_text))
        self.wait(0.3)

        poly_intro = Text("Polinomios característicos:", font_size=20, color=GRAY_B)
        poly_intro.move_to(UP * 0.8)
        self.play(FadeIn(poly_intro))
        self.wait(0.3)

        chi_z = MathTex(
            r"\chi_z(\lambda) = \lambda^2 + g_{z2}\lambda + g_{z1}",
            font_size=22,
        )
        chi_psi = MathTex(
            r"\chi_\psi(\lambda) = \lambda^2 + (\tilde{g}_{\psi 3}-\tilde{g}_{\psi 4})\lambda"
            r" + \tilde{g}_{\psi 1}-\tilde{g}_{\psi 2}",
            font_size=22,
        )
        chi_theta = MathTex(
            r"\chi_\theta(\lambda) = \lambda^2 - \tilde{g}_{\theta 2}\lambda - \tilde{g}_{\theta 1}",
            font_size=22,
        )
        chi_phi = MathTex(
            r"\chi_\varphi(\lambda) = \lambda^2 - \tilde{g}_{\varphi 2}\lambda - \tilde{g}_{\varphi 1}",
            font_size=22,
        )

        polys = VGroup(chi_z, chi_psi, chi_theta, chi_phi).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        polys.move_to(DOWN * 0.5)
        if polys.width > MAX_W - 0.5:
            polys.scale_to_fit_width(MAX_W - 0.5)

        polys_box = make_box(polys)

        self.play(FadeIn(polys), FadeIn(polys_box))
        self.wait(0.5)

        ctrl_note = Text(
            "El control se reduce a elegir coeficientes con polos estables",
            font_size=20,
            color=GRAY_B,
        )
        ctrl_note.next_to(polys_box, DOWN, buff=0.3)
        self.play(FadeIn(ctrl_note))
        self.wait(0.5)
        self.next_slide()

        # FadeOut scene 6
        sc6_mobjects = VGroup(sc6_label, cl_text, poly_intro, polys, polys_box, ctrl_note)
        self.play(FadeOut(sc6_mobjects))
        self.wait(0.3)

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 7 – Poincaré diagram
        # ══════════════════════════════════════════════════════════════════════
        sc7_label = Text(
            "Selección de polos: diagrama de Poincaré",
            font_size=26,
            color=BLUE,
        )
        sc7_label.move_to(UP * 2.3)
        self.play(FadeIn(sc7_label))
        self.wait(0.5)

        # ── Left side: Axes diagram ──────────────────────────────────────────
        axes = Axes(
            x_range=[-0.5, 2.5, 1],
            y_range=[-2.5, 1.5, 1],
            x_length=4.5,
            y_length=3.5,
            axis_config={"color": WHITE, "stroke_width": 2, "include_tip": True},
        )
        axes.move_to(LEFT * 2.5 + DOWN * 0.3)

        ax_labels = axes.get_axis_labels(
            x_label=MathTex(r"\det A", font_size=18),
            y_label=MathTex(r"\mathrm{Tr}\, A", font_size=18),
        )

        # Stability region: det A > 0, Tr A < 0  (green polygon)
        c1 = axes.coords_to_point(0, 0)
        c2 = axes.coords_to_point(2.5, 0)
        c3 = axes.coords_to_point(2.5, -2.5)
        c4 = axes.coords_to_point(0, -2.5)
        stab_region = Polygon(
            c1, c2, c3, c4,
            color=GREEN,
            fill_opacity=0.15,
            stroke_width=0,
        )

        # Delta=0 curve: Tr A = -2*sqrt(det A), x_range avoids sqrt(0)
        delta_curve = axes.plot(
            lambda x: -2 * (x ** 0.5),
            x_range=[0.001, 2.5, 0.01],
            color=YELLOW,
            stroke_width=2,
        )

        # Orange dot (degenerate sink)
        sink_dot = Dot(axes.coords_to_point(0.25, -1), radius=0.1, color=ORANGE)

        # Labels on diagram
        estable_lbl = Text("Estable", font_size=16, color=GREEN)
        estable_lbl.move_to(axes.coords_to_point(1.5, -1.8))

        delta_lbl = Text("Δ=0", font_size=16, color=YELLOW)
        delta_lbl.move_to(axes.coords_to_point(1.8, -2.3))

        sink_lbl = Text("Sumidero\ndegenerado", font_size=14, color=ORANGE)
        sink_lbl.next_to(sink_dot, RIGHT, buff=0.12)

        left_diagram = VGroup(axes, ax_labels, stab_region, delta_curve, sink_dot,
                              estable_lbl, delta_lbl, sink_lbl)

        # ── Right side: criteria panel ───────────────────────────────────────
        crit_header = Text("Criterio:", font_size=20, color=GRAY_B)
        crit_eq = MathTex(r"\det A > 0,\quad \mathrm{Tr}\, A < 0", font_size=22)
        delta_eq = MathTex(
            r"\Delta = (\mathrm{Tr}\, A)^2 - 4\det A = 0",
            font_size=22,
            color=YELLOW,
        )
        sink_text = Text(
            "Polo doble negativo\npara todos los canales",
            font_size=18,
            color=ORANGE,
        )

        right_panel = VGroup(crit_header, crit_eq, delta_eq, sink_text).arrange(DOWN, buff=0.3)
        right_panel.move_to(RIGHT * 3.0)
        if right_panel.width > MAX_W / 2 - 0.3:
            right_panel.scale_to_fit_width(MAX_W / 2 - 0.3)

        right_box = make_box(right_panel)

        self.play(FadeIn(left_diagram), FadeIn(right_panel), FadeIn(right_box))
        self.wait(0.5)
        self.next_slide()

        # FadeOut scene 7
        sc7_mobjects = VGroup(sc7_label, left_diagram, right_panel, right_box)
        self.play(FadeOut(sc7_mobjects))
        self.wait(0.3)

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 8 – Gain matrices
        # ══════════════════════════════════════════════════════════════════════
        sc8_label = Text("Matrices de ganancia resultantes", font_size=26, color=BLUE)
        sc8_label.move_to(UP * 2.3)
        self.play(FadeIn(sc8_label))
        self.wait(0.5)

        kz = MathTex(
            r"K^{(z)} = \frac{m}{2k\omega_0}"
            r"\begin{bmatrix}"
            r"\tfrac{1}{4}&\tfrac{1}{4}&\tfrac{1}{4}&\tfrac{1}{4}\\"
            r"1&1&1&1"
            r"\end{bmatrix}^{\!\top}",
            font_size=19,
        )
        kpsi = MathTex(
            r"K^{(\psi)} = \frac{I_{zz}}{2\ell b\,\omega_0}"
            r"\begin{bmatrix}"
            r"\tfrac{1}{2}&0&\tfrac{1}{2}&0\\"
            r"1&0&1&0"
            r"\end{bmatrix}^{\!\top}",
            font_size=19,
        )
        ktheta = MathTex(
            r"K^{(\theta)} = \frac{I_{yy}}{2\ell b\,\omega_0}"
            r"\begin{bmatrix}"
            r"1&0&\tfrac{3}{4}&0\\"
            r"\tfrac{1}{2}&0&-\tfrac{1}{2}&0"
            r"\end{bmatrix}^{\!\top}",
            font_size=19,
        )
        kphi = MathTex(
            r"K^{(\varphi)} = \frac{I_{xx}}{2\ell b\,\omega_0}"
            r"\begin{bmatrix}"
            r"0&1&0&\tfrac{3}{4}\\"
            r"0&\tfrac{1}{2}&0&-\tfrac{1}{2}"
            r"\end{bmatrix}^{\!\top}",
            font_size=19,
        )

        # Left col: K^(z), K^(θ); Right col: K^(ψ), K^(φ)
        gain_left = VGroup(kz, ktheta).arrange(DOWN, buff=0.5)
        gain_right = VGroup(kpsi, kphi).arrange(DOWN, buff=0.5)
        gain_grid = VGroup(gain_left, gain_right).arrange(RIGHT, buff=0.8)
        gain_grid.move_to(DOWN * 0.3)

        if gain_grid.width > MAX_W:
            gain_grid.scale_to_fit_width(MAX_W)

        self.play(FadeIn(gain_grid))
        self.wait(0.5)
        self.next_slide()

        # FadeOut scene 8
        sc8_mobjects = VGroup(sc8_label, gain_grid)
        self.play(FadeOut(sc8_mobjects))
        self.wait(0.3)

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 9 – alg:Control_retro — state-feedback control law (FINAL)
        # ══════════════════════════════════════════════════════════════════════
        sc9_label = Text(
            "Ley de control: retroalimentación de estados",
            font_size=26,
            color=BLUE,
        )
        sc9_label.move_to(UP * 2.3)
        self.play(FadeIn(sc9_label))
        self.wait(0.5)

        # 4 channel contributions
        u_z = MathTex(
            r"\mathbf{u}^{(z)}_t = K^{(z)}\begin{bmatrix}x^{(z)}_t\\x^{(w)}_t\end{bmatrix}",
            font_size=22,
        )
        u_psi = MathTex(
            r"\mathbf{u}^{(\psi)}_t = K^{(\psi)}\begin{bmatrix}x^{(\psi)}_t\\x^{(r)}_t\end{bmatrix}",
            font_size=22,
        )
        u_theta = MathTex(
            r"\mathbf{u}^{(\theta)}_t = K^{(\theta)}\begin{bmatrix}x^{(\theta)}_t\\x^{(q)}_t\end{bmatrix}",
            font_size=22,
        )
        u_phi = MathTex(
            r"\mathbf{u}^{(\varphi)}_t = K^{(\varphi)}\begin{bmatrix}x^{(\varphi)}_t\\x^{(p)}_t\end{bmatrix}",
            font_size=22,
        )

        channels = VGroup(u_z, u_psi, u_theta, u_phi).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        channels.move_to(UP * 0.6)

        # Total control input
        u_total = MathTex(
            r"\mathbf{u}_t = \mathbf{u}^{(z)}_t + \mathbf{u}^{(\psi)}_t"
            r"+ \mathbf{u}^{(\theta)}_t + \mathbf{u}^{(\varphi)}_t + \mathbf{u}^{*}",
            font_size=24,
            color=YELLOW,
        )

        # Next-step dynamics
        dyn_eq = MathTex(
            r"\mathbf{x}_{t+1} = f(\mathbf{x}_t,\,\mathbf{u}_t)",
            font_size=24,
        )

        # Stack all three elements and build a single box
        full_law = VGroup(channels, u_total, dyn_eq).arrange(DOWN, buff=0.35)
        full_law.move_to(DOWN * 0.15)
        if full_law.width > MAX_W:
            full_law.scale_to_fit_width(MAX_W)

        law_box = make_box(full_law)

        self.play(FadeIn(channels))
        self.wait(0.3)
        self.play(FadeIn(u_total))
        self.wait(0.3)
        self.play(FadeIn(dyn_eq))
        self.wait(0.3)
        self.play(FadeIn(law_box))
        self.wait(0.5)

        # Closing text
        closing = Text(
            "Cuatro canales desacoplados alrededor del hover",
            font_size=20,
            color=GRAY_B,
        )
        closing.next_to(law_box, DOWN, buff=0.3)
        self.play(FadeIn(closing))
        self.wait(0.5)
        self.next_slide()
