"""
GPS: Guided Policy Search slide.

Covers the GPS algorithm as a coupling cycle between local planning
(iLQR-based trajectory optimization) and global policy learning (ANN),
enforced through dual variables (BADMM).

Example:
    uv run manim-slides render slides/15_gps.py GPSSlide
"""

from pathlib import Path

from manim import *
from manim_slides import Slide


GPS_SCHEMA = (
    Path(__file__).resolve().parent.parent
    / "LaTex/figures/06_aplicacion_y_evaluacion_de_metodos_rl/gps_algorithm.png"
)


class GPSSlide(Slide):
    """GPS overview: local controllers, global policy, and BADMM dual updates."""

    def construct(self):
        # ------------------------------------------------------------------ #
        # Helpers
        # ------------------------------------------------------------------ #
        def make_box(mobject, color=GRAY, fill_opacity=0.15, stroke_width=1):
            box = RoundedRectangle(
                corner_radius=0.2,
                width=mobject.width + 0.8,
                height=mobject.height + 0.6,
                color=color,
                fill_opacity=fill_opacity,
                stroke_width=stroke_width,
            )
            box.move_to(mobject)
            return box

        def shrink_to_fit_width(mobject, max_width):
            if mobject.width > max_width:
                mobject.scale_to_fit_width(max_width)
            return mobject

        # ------------------------------------------------------------------ #
        # TITLE
        # ------------------------------------------------------------------ #
        title = Text("GPS: Búsqueda Guiada de Política", font_size=42, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))
        self.wait(0.5)
        self.next_slide()

        # ================================================================== #
        # === SECTION: IDEA CENTRAL ===
        # ================================================================== #
        idea_label = Text("Idea central", font_size=30, color=BLUE)
        idea_label.move_to(UP * 2.0)

        idea_items = VGroup(
            Text("• Alterna entre controladores locales", font_size=22, color=WHITE),
            MathTex(r"p_i(\mathbf{u}_t|\mathbf{x}_t)", font_size=22, color=ORANGE),
            Text("  y una política global", font_size=22, color=WHITE),
            MathTex(r"\pi_{\boldsymbol{\theta}}(\mathbf{u}_t|\mathbf{x}_t)", font_size=22, color=GREEN),
            Text("• El acoplamiento se fuerza con multiplicadores de Lagrange", font_size=22, color=WHITE),
            MathTex(r"\boldsymbol{\lambda}_t \text{ y } \nu_t", font_size=22, color=YELLOW),
            Text("• BADMM deriva las reglas de actualización dual", font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        idea_items.next_to(idea_label, DOWN, buff=0.35)

        idea_group = VGroup(idea_label, idea_items)
        idea_group.move_to(ORIGIN + UP * 0.3)
        idea_box = make_box(idea_group)

        self.play(FadeIn(idea_box), FadeIn(idea_group))
        self.wait(0.5)
        self.next_slide()

        self.play(FadeOut(idea_box), FadeOut(idea_group))
        self.wait(0.3)

        # ================================================================== #
        # === SECTION: DISTRIBUCIONES ===
        # ================================================================== #
        dist_label = Text("Distribuciones del algoritmo", font_size=30, color=BLUE)
        dist_label.move_to(UP * 2.5)

        local_label = Text("Controlador local (Gaussiano lineal):", font_size=22, color=ORANGE)
        local_eq = MathTex(
            r"p_i(\mathbf{u}_t|\mathbf{x}_t) = \mathcal{N}\!\left(\mu_{ti}(\mathbf{x}_t),\,"
            r"\boldsymbol{\Sigma}_{it}\right)",
            font_size=26,
        )
        shrink_to_fit_width(local_eq, config.frame_width - 2.0)
        local_group = VGroup(local_label, local_eq).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        local_box = make_box(local_group)

        global_label = Text("Política global (red neuronal):", font_size=22, color=GREEN)
        global_eq = MathTex(
            r"\pi_{\boldsymbol{\theta}}(\mathbf{u}_t|\mathbf{x}_t) = "
            r"\mathcal{N}\!\left(\mu^{\pi}(\mathbf{x}_t;\boldsymbol{\theta}),\,"
            r"\boldsymbol{\Sigma}^{\pi}(\mathbf{x}_t)\right)",
            font_size=26,
        )
        shrink_to_fit_width(global_eq, config.frame_width - 2.0)
        global_group = VGroup(global_label, global_eq).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        global_box = make_box(global_group)

        dist_content = VGroup(
            VGroup(local_box, local_group),
            VGroup(global_box, global_group),
        ).arrange(DOWN, buff=0.5)
        dist_content.next_to(dist_label, DOWN, buff=0.45)

        self.play(FadeIn(dist_label))
        self.play(FadeIn(local_box), FadeIn(local_group))
        self.wait(0.5)
        self.next_slide()

        self.play(FadeIn(global_box), FadeIn(global_group))
        self.wait(0.5)
        self.next_slide()

        self.play(
            FadeOut(dist_label),
            FadeOut(local_box),
            FadeOut(local_group),
            FadeOut(global_box),
            FadeOut(global_group),
        )
        self.wait(0.3)

        # ================================================================== #
        # === SECTION: DIAGRAMA GPS ===
        # ================================================================== #
        diag_label = Text("Ciclo de entrenamiento GPS", font_size=30, color=BLUE)
        diag_label.to_edge(UP, buff=1.15)

        diagram = ImageMobject(str(GPS_SCHEMA))
        diagram.scale_to_fit_width(8.5)
        diagram.move_to(DOWN * 0.3)
        diagram_frame = SurroundingRectangle(diagram, color=GRAY, buff=0.12, stroke_width=1)

        self.play(FadeIn(diag_label), FadeIn(diagram_frame), FadeIn(diagram))
        self.wait(0.5)
        self.next_slide()

        # --- Label 1: Generación de trayectorias locales ---
        lbl1 = Text("1. Generar trayectorias\nlocales con iLQR", font_size=18, color=YELLOW)
        lbl1.move_to(diagram.get_left() + RIGHT * 1.4 + UP * 1.5)

        self.play(FadeIn(lbl1))
        self.wait(0.5)
        self.next_slide()

        # --- Label 2: Base de datos de trayectorias ---
        lbl2 = VGroup(
            Text("2. Base de datos", font_size=18, color=YELLOW),
            MathTex(r"\{\tau_i^{(j)}\}", font_size=18, color=YELLOW),
        ).arrange(DOWN, buff=0.08)
        lbl2.move_to(diagram.get_bottom() + UP * 0.55 + LEFT * 2.0)

        self.play(FadeIn(lbl2))
        self.wait(0.5)
        self.next_slide()

        # --- Label 3: Entrenamiento política global ---
        lbl3 = Text("3. Entrenar\npolítica global π_θ", font_size=18, color=GREEN)
        lbl3.move_to(diagram.get_right() + LEFT * 1.5 + UP * 1.5)

        self.play(FadeIn(lbl3))
        self.wait(0.5)
        self.next_slide()

        # --- Label 4: Actualizar variables duales ---
        lbl4 = Text("4. Actualizar\nλ_t y ν_t", font_size=18, color=ORANGE)
        lbl4.move_to(diagram.get_bottom() + UP * 0.55 + RIGHT * 2.0)

        self.play(FadeIn(lbl4))
        self.wait(0.5)
        self.next_slide()

        # --- Label 5: k = k + 1 ---
        lbl5 = Text("5. k = k + 1", font_size=18, color=WHITE)
        lbl5.move_to(diagram.get_top() + DOWN * 0.4)

        self.play(FadeIn(lbl5))
        self.wait(0.5)
        self.next_slide()

        self.play(
            FadeOut(diag_label),
            FadeOut(diagram_frame),
            FadeOut(diagram),
            FadeOut(lbl1),
            FadeOut(lbl2),
            FadeOut(lbl3),
            FadeOut(lbl4),
            FadeOut(lbl5),
        )
        self.wait(0.3)

        # ================================================================== #
        # === SECTION: ACTUALIZACIONES BADMM ===
        # ================================================================== #
        badmm_label = Text("Actualizaciones BADMM", font_size=30, color=BLUE)
        badmm_label.move_to(UP * 2.8)

        self.play(FadeIn(badmm_label))
        self.wait(0.3)

        # --- Update theta ---
        theta_desc = Text("Actualizar política global θ:", font_size=22, color=GREEN)
        theta_desc.move_to(UP * 2.0)

        theta_eq = MathTex(
            r"\boldsymbol{\theta}^{(k+1)} = \arg\min_{\boldsymbol{\theta}} \sum_{i,t} "
            r"\mathbb{E}\!\left[\boldsymbol{\lambda}_{t}^{\top}\mathbf{u}_t\right]"
            r"+ \nu_t\, D_{\mathrm{KL}}\!\left(\pi_{\boldsymbol{\theta}} \| p_i\right)",
            font_size=24,
        )
        shrink_to_fit_width(theta_eq, config.frame_width - 1.4)
        theta_eq.next_to(theta_desc, DOWN, buff=0.35)
        theta_box = make_box(theta_eq)

        self.play(FadeIn(theta_desc), FadeIn(theta_box), FadeIn(theta_eq))
        self.wait(0.5)
        self.next_slide()

        self.play(FadeOut(theta_desc), FadeOut(theta_box), FadeOut(theta_eq))
        self.wait(0.2)

        # --- Update p ---
        p_desc = Text("Actualizar controlador local p:", font_size=22, color=ORANGE)
        p_desc.move_to(UP * 2.0)

        p_eq = MathTex(
            r"p^{(k+1)} = \arg\min_{p} \sum_{i,t} "
            r"\mathbb{E}\!\left[c(\mathbf{x}_t, \mathbf{u}_t) - \boldsymbol{\lambda}_t^{\top}\mathbf{u}_t\right]"
            r"+ \nu_t\, D_{\mathrm{KL}}\!\left(p_i \| \pi_{\boldsymbol{\theta}}\right)",
            font_size=24,
        )
        shrink_to_fit_width(p_eq, config.frame_width - 1.4)
        p_eq.next_to(p_desc, DOWN, buff=0.35)
        p_box = make_box(p_eq)

        self.play(FadeIn(p_desc), FadeIn(p_box), FadeIn(p_eq))
        self.wait(0.5)
        self.next_slide()

        self.play(FadeOut(p_desc), FadeOut(p_box), FadeOut(p_eq))
        self.wait(0.2)

        # --- Update lambda ---
        lambda_desc = Text("Actualizar multiplicador λ_t:", font_size=22, color=YELLOW)
        lambda_desc.move_to(UP * 2.0)

        lambda_eq = MathTex(
            r"\boldsymbol{\lambda}_t^{(k+1)} = \boldsymbol{\lambda}_t^{(k)}"
            r"+ \alpha_{\boldsymbol{\lambda}}\,\nu_t"
            r"\left(\mathbb{E}_{\pi_{\boldsymbol{\theta}}}[\mathbf{u}_t]"
            r"- \mathbb{E}_{p_i}[\mathbf{u}_t]\right)",
            font_size=26,
        )
        shrink_to_fit_width(lambda_eq, config.frame_width - 1.4)
        lambda_eq.next_to(lambda_desc, DOWN, buff=0.35)
        lambda_box = make_box(lambda_eq, color=YELLOW, fill_opacity=0.1, stroke_width=2)

        self.play(FadeIn(lambda_desc), FadeIn(lambda_box), FadeIn(lambda_eq))
        self.wait(0.5)
        self.next_slide()

        self.play(
            FadeOut(badmm_label),
            FadeOut(lambda_desc),
            FadeOut(lambda_box),
            FadeOut(lambda_eq),
        )
        self.wait(0.3)

        # ================================================================== #
        # === SECTION: COSTO AUMENTADO PARA iLQR ===
        # ================================================================== #
        cost_label = Text("Costo aumentado para iLQR", font_size=30, color=BLUE)
        cost_label.move_to(UP * 2.5)

        cost_note = Text(
            "El costo efectivo pasado a iLQR incorpora la restricción de política:",
            font_size=20,
            color=GRAY_B,
        )
        cost_note.next_to(cost_label, DOWN, buff=0.35)

        ctilde_eq = MathTex(
            r"\tilde{c}(\mathbf{x}_t, \mathbf{u}_t) = c(\mathbf{x}_t, \mathbf{u}_t)"
            r"- \boldsymbol{\lambda}_t^{\top}\mathbf{u}_t"
            r"- \nu_t \log \pi_{\boldsymbol{\theta}}(\mathbf{u}_t|\mathbf{x}_t)",
            font_size=26,
            color=WHITE,
        )
        shrink_to_fit_width(ctilde_eq, config.frame_width - 1.4)
        ctilde_eq.next_to(cost_note, DOWN, buff=0.45)

        ctilde_box = make_box(ctilde_eq, color=YELLOW, fill_opacity=0.1, stroke_width=2)

        self.play(FadeIn(cost_label), FadeIn(cost_note))
        self.wait(0.3)
        self.play(FadeIn(ctilde_box), FadeIn(ctilde_eq))
        self.wait(0.5)
        self.next_slide()

        cost_breakdown = VGroup(
            Text("• Primer término: costo original del sistema", font_size=20, color=WHITE),
            MathTex(r"\bullet\;-\boldsymbol{\lambda}_t^{\top}\mathbf{u}_t\text{: correcci\'{o}n dual (Lagrangiano)}", font_size=20),
            MathTex(r"\bullet\;-\nu_t \log \pi_{\boldsymbol{\theta}}\text{: penalizaci\'{o}n por divergencia de pol\'{i}tica}", font_size=20),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        shrink_to_fit_width(cost_breakdown, config.frame_width - 1.6)
        cost_breakdown.next_to(ctilde_box, DOWN, buff=0.4)

        self.play(FadeIn(cost_breakdown))
        self.wait(0.5)
        self.next_slide()

        self.play(
            FadeOut(cost_label),
            FadeOut(cost_note),
            FadeOut(ctilde_box),
            FadeOut(ctilde_eq),
            FadeOut(cost_breakdown),
        )
        self.wait(0.3)

        # ================================================================== #
        # === SECTION: CONFIGURACION DE LA TESIS ===
        # ================================================================== #
        config_label = Text("Configuración experimental", font_size=30, color=BLUE)
        config_label.move_to(UP * 2.5)

        config_items = VGroup(
            Text("• Iteraciones GPS:              K = 5", font_size=22, color=WHITE),
            Text("• Controladores locales:        N = 7  condiciones iniciales", font_size=22, color=WHITE),
            Text("• Muestras por controlador:     M = 800  trayectorias", font_size=22, color=WHITE),
            Text("• Optimizador política global:  Adam,  lr = 0.01", font_size=22, color=WHITE),
            MathTex(
                r"\bullet\;\text{Tasa de actualizaci\'{o}n dual: }\alpha_{\boldsymbol{\lambda}} = 0.01",
                font_size=22,
            ),
            MathTex(
                r"\bullet\;\text{Penalizaci\'{o}n inicial: }\nu_t^{(0)} = 0.001",
                font_size=22,
            ),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        shrink_to_fit_width(config_items, config.frame_width - 1.4)
        config_items.next_to(config_label, DOWN, buff=0.45)

        config_group = VGroup(config_label, config_items)
        config_group.move_to(ORIGIN + DOWN * 0.2)
        config_box = make_box(config_group)

        self.play(FadeIn(config_box), FadeIn(config_group))
        self.wait(0.5)
        self.next_slide()

        closing = Text(
            "GPS combina la precisión local de iLQR con la generalización global de redes neuronales",
            font_size=20,
            color=YELLOW,
        )
        closing.next_to(config_box, DOWN, buff=0.4)
        shrink_to_fit_width(closing, config.frame_width - 1.4)

        self.play(FadeIn(closing))
        self.wait(0.5)
        self.next_slide()

        self.wait(1)
