"""
Reverse-engineered iLQR slide from presentation/13_ilqr.html.

This scene recreates the paused states visible in the exported HTML deck,
which differs from the current slides/13_ilqr.py source.

Example:
    uv run manim-slides render slides/13_ilqr_reverse.py ILQRReverseSlide
"""

from manim import *
from manim_slides import Slide


TITLE_COLOR = YELLOW
SECTION_COLOR = BLUE_B
BODY_COLOR = WHITE
ACCENT_COLOR = GREEN
WARN_COLOR = RED_C
HIGHLIGHT_COLOR = ORANGE
BOX_STROKE = GRAY
BOX_FILL_OPACITY = 0.14


def make_box(content: Mobject, color=BOX_STROKE, pad_x=0.8, pad_y=0.55, stroke_width=1.4):
    box = RoundedRectangle(
        corner_radius=0.24,
        width=content.width + pad_x,
        height=content.height + pad_y,
        color=color,
        fill_opacity=BOX_FILL_OPACITY,
        stroke_width=stroke_width,
    )
    box.move_to(content)
    return box


def make_panel(title: Mobject, lines: list[Mobject], width_limit: float | None = None):
    group = VGroup(title, *lines).arrange(DOWN, buff=0.5)
    if width_limit is not None:
        group.scale_to_fit_width(min(group.width, width_limit))
    box = make_box(group)
    return VGroup(box, group)


class ILQRReverseSlide(Slide):
    """Rebuild the older HTML-exported iLQR slide as source code."""

    def construct(self):
        title = Text(
            "iLQR: Regulador Cuadrático Lineal Iterativo",
            font_size=42,
            color=TITLE_COLOR,
        )
        title.to_edge(UP, buff=0.45)

        self.play(FadeIn(title))
        self.wait(0.3)
        self.next_slide()

        # 1) Programación dinámica
        pd_title = Text("Programación Dinámica", font_size=32, color=SECTION_COLOR)
        pd_eq = MathTex(
            r"V^{*}(x_t)=\min_{u_t}\left[c(x_t,u_t)+V^{*}(x_{t+1})\right]",
            font_size=34,
        )
        pd_sub = Text(
            "Principio de optimalidad de Bellman",
            font_size=23,
            color=GRAY_A,
        )
        pd_panel = make_panel(pd_title, [pd_eq, pd_sub], width_limit=8.3)
        pd_panel.move_to(UP * 0.35)

        self.play(FadeIn(pd_panel))
        self.wait(0.3)
        self.next_slide()

        pd_note = Text(
            "Iteración de valor: resolver hacia atrás desde t = T",
            font_size=26,
            color=BODY_COLOR,
        )
        pd_note.next_to(pd_panel, DOWN, buff=0.7)

        pd_timeline = MathTex(
            r"0 \;\;\leftarrow\;\; \cdots \;\;\leftarrow\;\; T-2 \;\;\leftarrow\;\; T-1 \;\;\leftarrow\;\; T",
            font_size=28,
            color=SECTION_COLOR,
        )
        pd_timeline.next_to(pd_note, DOWN, buff=0.35)

        self.play(FadeIn(pd_note), FadeIn(pd_timeline))
        self.wait(0.3)
        self.next_slide()

        self.play(FadeOut(pd_panel), FadeOut(pd_note), FadeOut(pd_timeline))
        self.wait(0.2)

        # 2) Caso especial
        case_title = Text("iLQR: Caso especial", font_size=31, color=SECTION_COLOR)
        case_bullets = BulletedList(
            "Aproximación cuadrática local del costo",
            "Aproximación lineal de la dinámica",
            "Controlador lineal variante en el tiempo",
            font_size=23,
            color=BODY_COLOR,
        )
        case_bullets.align_to(case_bullets[0], LEFT)
        case_panel = make_panel(case_title, [case_bullets], width_limit=8.0)
        case_panel.move_to(UP * 0.45)

        self.play(FadeIn(case_panel))
        self.wait(0.3)
        self.next_slide()

        case_note = Text(
            "LQR para sistemas no lineales mediante linealización iterativa",
            font_size=25,
            color=TITLE_COLOR,
        )
        case_note.next_to(case_panel, DOWN, buff=0.65)

        self.play(FadeIn(case_note))
        self.wait(0.3)
        self.next_slide()

        self.play(FadeOut(case_panel), FadeOut(case_note))
        self.wait(0.2)

        # 3) Planteamiento del problema
        problem_title = Text("Planteamiento del problema", font_size=31, color=SECTION_COLOR)
        dyn_line = MathTex(
            r"\text{Dinámica: }\; x_{t+1}=f(x_t,u_t)",
            font_size=31,
        )
        dyn_line.set_color_by_tex("x_{t+1}=f(x_t,u_t)", ACCENT_COLOR)

        cost_line = MathTex(
            r"\text{Costo: }\; J=\sum_{t=0}^{T-1} c(x_t,u_t)+c_T(x_T)",
            font_size=31,
        )

        objective_line = MathTex(
            r"\text{Objetivo: }\;\min_{u_0,\ldots,u_{T-1}}\; J",
            font_size=31,
        )
        objective_line.set_color_by_tex(r"u_0,\ldots,u_{T-1}", HIGHLIGHT_COLOR)
        objective_line.set_color_by_tex("J", HIGHLIGHT_COLOR)

        problem_panel = make_panel(
            problem_title,
            [dyn_line, cost_line, objective_line],
            width_limit=8.2,
        )
        problem_panel.move_to(UP * 0.3)

        self.play(FadeIn(problem_panel))
        self.wait(0.3)
        self.next_slide()

        problem_note = Text(
            "f y c son funciones no lineales arbitrarias",
            font_size=25,
            color=WARN_COLOR,
        )
        problem_note.next_to(problem_panel, DOWN, buff=0.6)

        self.play(FadeIn(problem_note))
        self.wait(0.3)
        self.next_slide()

        self.play(FadeOut(problem_panel), FadeOut(problem_note))
        self.wait(0.2)

        # 4) Estabilización de trayectorias locales
        stab_label = Text(
            "Estabilización de trayectorias locales",
            font_size=31,
            color=SECTION_COLOR,
        )
        stab_label.move_to(UP * 2.0)

        x_positions = [-5.4, -3.55, -1.7, 0.15, 2.0, 4.6]
        y_pos = 0.1
        node_labels = [r"\bar{x}_0", r"\bar{x}_1", r"\bar{x}_2", r"\bar{x}_3", r"\bar{x}_4", r"\bar{x}_T"]
        ctrl_labels = [r"\bar{u}_0", r"\bar{u}_1", r"\bar{u}_2", r"\bar{u}_3", r"\bar{u}_4"]

        nodes = VGroup()
        arrows = VGroup()
        node_tex = VGroup()
        ctrl_tex = VGroup()
        for idx, x in enumerate(x_positions):
            dot = Dot(point=np.array([x, y_pos, 0]), radius=0.12, color=SECTION_COLOR)
            dot.set_fill(SECTION_COLOR, opacity=1.0)
            nodes.add(dot)
            label = MathTex(node_labels[idx], font_size=26, color=BODY_COLOR)
            label.next_to(dot, UP, buff=0.22)
            node_tex.add(label)
            if idx < len(x_positions) - 1:
                arrow = Arrow(
                    start=dot.get_right() + RIGHT * 0.08,
                    end=np.array([x_positions[idx + 1] - 0.18, y_pos, 0]),
                    buff=0.02,
                    stroke_width=2.5,
                    max_tip_length_to_length_ratio=0.12,
                    color=SECTION_COLOR,
                )
                arrows.add(arrow)
                ctrl = MathTex(ctrl_labels[idx], font_size=24, color=GRAY_B)
                ctrl.next_to(arrow, DOWN, buff=0.18)
                ctrl_tex.add(ctrl)

        self.play(
            FadeIn(stab_label),
            FadeIn(nodes),
            FadeIn(arrows),
            FadeIn(node_tex),
            FadeIn(ctrl_tex),
        )
        self.wait(0.3)
        self.next_slide()

        nominal_note = MathTex(
            r"\bar{x}_t,\bar{u}_t:\ \text{trayectoria nominal}",
            font_size=28,
            color=BODY_COLOR,
        )
        nominal_note.move_to(DOWN * 1.95)

        delta_note = MathTex(
            r"\delta x_t = x_t-\bar{x}_t,\qquad \delta u_t = u_t-\bar{u}_t",
            font_size=30,
            color=HIGHLIGHT_COLOR,
        )
        delta_note.next_to(nominal_note, DOWN, buff=0.4)

        self.play(FadeIn(nominal_note), FadeIn(delta_note))
        self.wait(0.3)
        self.next_slide()

        self.play(
            FadeOut(stab_label),
            FadeOut(nodes),
            FadeOut(arrows),
            FadeOut(node_tex),
            FadeOut(ctrl_tex),
            FadeOut(nominal_note),
            FadeOut(delta_note),
        )
        self.wait(0.2)

        # 5) Backward pass
        backward_label = Text(
            "Paso hacia atrás (Backward Pass)",
            font_size=31,
            color=SECTION_COLOR,
        )
        backward_label.move_to(UP * 2.0)

        linearize = MathTex(
            r"\text{Linealizar: }\; A_t=\frac{\partial f}{\partial x}(\bar{x}_t,\bar{u}_t),\qquad "
            r"B_t=\frac{\partial f}{\partial u}(\bar{x}_t,\bar{u}_t)",
            font_size=27,
        )
        linearize.move_to(UP * 0.8)

        quadratize = MathTex(
            r"\text{Cuadratizar: }\; Q_t,R_t,q_t,r_t\ \text{de}\ c(x_t,u_t)",
            font_size=27,
        )
        quadratize.next_to(linearize, DOWN, buff=0.55)

        self.play(FadeIn(backward_label), FadeIn(linearize), FadeIn(quadratize))
        self.wait(0.3)
        self.next_slide()

        back_y = -0.75
        back_positions = [3.55, 1.55, -0.45, -2.45]
        back_nodes = VGroup()
        back_arrows = VGroup()
        back_labels = VGroup()
        gain_labels = VGroup()

        node_texts = [r"t=T", r"t=T-1", r"t=T-2", r"t=\cdots"]
        fills = [0.0, 0.0, 0.0, 0.26]
        colors = [GRAY_B, GRAY_B, GRAY_B, ACCENT_COLOR]

        for idx, x in enumerate(back_positions):
            circle = Circle(radius=0.42, color=colors[idx], stroke_width=1.6)
            circle.set_fill(colors[idx], opacity=fills[idx])
            circle.move_to(np.array([x, back_y, 0]))
            back_nodes.add(circle)

            label = MathTex(node_texts[idx], font_size=24, color=BODY_COLOR)
            label.move_to(circle.get_center())
            back_labels.add(label)

            if idx < len(back_positions) - 1:
                arrow = Arrow(
                    start=np.array([x - 0.55, back_y, 0]),
                    end=np.array([back_positions[idx + 1] + 0.55, back_y, 0]),
                    buff=0.02,
                    stroke_width=2.2,
                    max_tip_length_to_length_ratio=0.12,
                    color=SECTION_COLOR,
                )
                back_arrows.add(arrow)

        gain_texts = [
            r"K_T,k_T",
            r"K_{T-1},k_{T-1}",
            r"K_{T-2},k_{T-2}",
        ]
        for idx, txt in enumerate(gain_texts):
            gain = MathTex(txt, font_size=24, color=TITLE_COLOR)
            gain.next_to(back_nodes[idx], DOWN, buff=0.28)
            gain_labels.add(gain)

        more_text = MathTex(r"\cdots", font_size=24, color=TITLE_COLOR)
        more_text.next_to(back_nodes[-1], DOWN, buff=0.22)

        self.play(
            FadeIn(back_nodes),
            FadeIn(back_arrows),
            FadeIn(back_labels),
            FadeIn(gain_labels),
            FadeIn(more_text),
        )
        self.wait(0.3)
        self.next_slide()

        delta_u = MathTex(
            r"\delta u_t = K_t \delta x_t + k_t",
            font_size=34,
            color=TITLE_COLOR,
        )
        delta_u_box = make_box(delta_u, color=TITLE_COLOR, pad_x=0.65, pad_y=0.45, stroke_width=2.0)
        delta_u_group = VGroup(delta_u_box, delta_u)
        delta_u_group.move_to(DOWN * 2.55)

        self.play(FadeIn(delta_u_group))
        self.wait(0.3)
        self.next_slide()

        self.play(
            FadeOut(backward_label),
            FadeOut(linearize),
            FadeOut(quadratize),
            FadeOut(back_nodes),
            FadeOut(back_arrows),
            FadeOut(back_labels),
            FadeOut(gain_labels),
            FadeOut(more_text),
            FadeOut(delta_u_group),
        )
        self.wait(0.2)

        # 6) Forward pass
        forward_label = Text(
            "Paso hacia adelante (Forward Pass)",
            font_size=31,
            color=SECTION_COLOR,
        )
        forward_label.move_to(UP * 2.0)

        forward_eq1 = MathTex(
            r"u_t=\bar{u}_t+K_t(x_t-\bar{x}_t)+\alpha k_t",
            font_size=31,
        )
        forward_eq2 = MathTex(
            r"x_{t+1}=f(x_t,u_t)",
            font_size=31,
        )
        forward_panel = make_panel(
            VGroup(),
            [forward_eq1, forward_eq2],
            width_limit=6.7,
        )
        forward_panel.move_to(UP * 0.25)

        self.play(FadeIn(forward_label), FadeIn(forward_panel))
        self.wait(0.3)
        self.next_slide()

        alpha_note = MathTex(
            r"\alpha \in (0,1]:\ \text{tamaño de paso (line search)}",
            font_size=27,
            color=GRAY_A,
        )
        alpha_note.next_to(forward_panel, DOWN, buff=0.6)

        forward_note = Text(
            "Nueva trayectoria nominal para la siguiente iteración",
            font_size=27,
            color=ACCENT_COLOR,
        )
        forward_note.next_to(alpha_note, DOWN, buff=0.45)

        self.play(FadeIn(alpha_note), FadeIn(forward_note))
        self.wait(0.3)
        self.next_slide()

        self.play(
            FadeOut(forward_label),
            FadeOut(forward_panel),
            FadeOut(alpha_note),
            FadeOut(forward_note),
        )
        self.wait(0.2)

        # 7) Line search
        ls_title = Text("Búsqueda lineal (Line Search)", font_size=31, color=SECTION_COLOR)
        ls_eq = MathTex(
            r"\alpha^{*}=\arg\min_{\alpha \in (0,1]} J(\alpha)",
            font_size=34,
        )
        ls_sub = Text(
            "Evita divergencia por pasos demasiado grandes",
            font_size=24,
            color=GRAY_A,
        )
        ls_panel = make_panel(ls_title, [ls_eq, ls_sub], width_limit=8.4)
        ls_panel.move_to(UP * 0.15)

        self.play(FadeIn(ls_panel))
        self.wait(0.3)
        self.next_slide()

        self.play(FadeOut(ls_panel))
        self.wait(0.2)

        # 8) Regularización
        reg_title = Text("Regularización", font_size=31, color=SECTION_COLOR)
        reg_eq = MathTex(
            r"Q_{uu}\leftarrow Q_{uu}+\mu I",
            font_size=35,
        )
        reg_sub = Text(
            "Garantiza que la matriz Hessiana sea definida positiva",
            font_size=24,
            color=GRAY_A,
        )
        reg_panel = make_panel(reg_title, [reg_eq, reg_sub], width_limit=9.0)
        reg_panel.move_to(UP * 0.15)

        self.play(FadeIn(reg_panel))
        self.wait(0.3)
        self.next_slide()

        reg_note = Text(
            "μ se ajusta adaptativamente (estilo Levenberg-Marquardt)",
            font_size=23,
            color=TITLE_COLOR,
        )
        reg_note.next_to(reg_panel, DOWN, buff=0.62)

        self.play(FadeIn(reg_note))
        self.wait(0.3)
        self.next_slide()

        self.wait(1)
