"""
DDPG slide: actor-critic overview, main equations, stabilization mechanisms,
and the training algorithm for continuous control.

Example:
    uv run manim-slides render slides/14_ddpg.py DDPGSlide
"""

from pathlib import Path

from manim import *
from manim_slides import Slide


DDPG_SCHEMA = (
    Path(__file__).resolve().parent.parent
    / "LaTex/figures/06_aplicacion_y_evaluacion_de_metodos_rl/ddpg_algorithm.png"
)


class DDPGSlide(Slide):
    """DDPG overview grounded in the dissertation chapter on TD learning."""

    def construct(self):
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

        title = Text("DDPG: Deep Deterministic Policy Gradient", font_size=38, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))
        self.wait(0.5)
        self.next_slide()

        # === MOTIVACION ===
        motivation_label = Text("Motivación", font_size=30, color=BLUE)
        motivation_items = VGroup(
            Text("• Extiende Q-learning a control continuo", font_size=24, color=WHITE),
            Text("• Combina actor determinista y crítico Q", font_size=24, color=WHITE),
            Text("• Usa replay buffer y redes objetivo", font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        motivation_group = VGroup(motivation_label, motivation_items).arrange(
            DOWN, buff=0.35, aligned_edge=LEFT
        )
        motivation_group.move_to(UP * 0.6)
        motivation_box = make_box(motivation_group)

        self.play(FadeIn(motivation_box), FadeIn(motivation_group))
        self.wait(0.5)
        self.next_slide()

        motivation_note = Text(
            "Método off-policy para aprendizaje por diferencias temporales",
            font_size=20,
            color=GREEN,
        )
        motivation_note.next_to(motivation_box, DOWN, buff=0.4)

        self.play(FadeIn(motivation_note))
        self.wait(0.5)
        self.next_slide()

        self.play(
            FadeOut(motivation_box),
            FadeOut(motivation_group),
            FadeOut(motivation_note),
        )
        self.wait(0.3)

        # === DISTRIBUCION DE ESTADOS ===
        rho_label = Text("Distribución de estados con descuento", font_size=30, color=BLUE)
        rho_label.move_to(UP * 2.5)

        rho_eq = MathTex(
            r"\rho_{\beta}(\mathbf{x}') = \int_{\mathcal{X}}\sum_{i=1}^{\infty}\gamma^{i-1}"
            r"\rho_{0}(\mathbf{x})\rho_{\beta}\left(\mathbf{x}\rightarrow \mathbf{x}', i\right)d\mathbf{x}",
            font_size=22,
        )
        shrink_to_fit_width(rho_eq, config.frame_width - 1.5)
        rho_eq.next_to(rho_label, DOWN, buff=0.5)

        rho_eq_box = make_box(rho_eq, color=YELLOW, fill_opacity=0.1, stroke_width=2)

        self.play(FadeIn(rho_label), FadeIn(rho_eq_box), FadeIn(rho_eq))
        self.wait(0.5)
        self.next_slide()

        rho_pair = MathTex(
            r"\rho_{\beta}(\mathbf{x}, \mathbf{u}) = \beta(\mathbf{u}|\mathbf{x})\rho_{\beta}(\mathbf{x})",
            font_size=28,
            color=GREEN,
        )
        rho_pair.next_to(rho_eq_box, DOWN, buff=0.45)

        rho_note = Text(
            "Describe las muestras usadas por actor y crítico bajo la política β",
            font_size=20,
            color=GRAY_B,
        )
        rho_note.next_to(rho_pair, DOWN, buff=0.25)

        self.play(FadeIn(rho_pair), FadeIn(rho_note))
        self.wait(0.5)
        self.next_slide()

        self.play(
            FadeOut(rho_label),
            FadeOut(rho_eq_box),
            FadeOut(rho_eq),
            FadeOut(rho_pair),
            FadeOut(rho_note),
        )
        self.wait(0.3)

        # === ACTOR-CRITICO DIAGRAM ===
        ac_label = Text("Esquema actor-crítico", font_size=30, color=BLUE)
        ac_label.move_to(UP * 2.5)

        diagram = ImageMobject(str(DDPG_SCHEMA))
        diagram.scale_to_fit_width(7.0)
        diagram.move_to(LEFT * 2.4 + DOWN * 0.2)

        diagram_frame = SurroundingRectangle(diagram, color=GRAY, buff=0.12, stroke_width=1)

        actor_box = RoundedRectangle(
            corner_radius=0.2,
            width=3.9,
            height=2.7,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        actor_box.move_to(RIGHT * 3.4 + DOWN * 0.15)

        actor_items = VGroup(
            Text("Actor:", font_size=24, color=GREEN),
            MathTex(r"\mu(\mathbf{x}; \boldsymbol{\theta}_{\mu})", font_size=28, color=WHITE),
            Text("Política determinista", font_size=20, color=GRAY_B),
            Text("Selecciona acciones continuas", font_size=20, color=GRAY_B),
            Text("Crítico:", font_size=24, color=ORANGE),
            MathTex(r"Q(\mathbf{x}, \mathbf{u}; \boldsymbol{\theta}_{Q})", font_size=28, color=WHITE),
            Text("Evalúa la acción y genera error TD", font_size=20, color=GRAY_B),
        ).arrange(DOWN, buff=0.12)
        actor_items.move_to(actor_box)

        self.play(
            FadeIn(ac_label),
            FadeIn(diagram_frame),
            FadeIn(diagram),
            FadeIn(actor_box),
            FadeIn(actor_items),
        )
        self.wait(0.5)
        self.next_slide()

        ac_note = Text(
            "El actor propone acciones; el crítico retroalimenta su calidad",
            font_size=20,
            color=YELLOW,
        )
        ac_note.next_to(VGroup(diagram_frame, actor_box), DOWN, buff=0.35)

        self.play(FadeIn(ac_note))
        self.wait(0.5)
        self.next_slide()

        self.play(
            FadeOut(ac_label),
            FadeOut(diagram_frame),
            FadeOut(diagram),
            FadeOut(actor_box),
            FadeOut(actor_items),
            FadeOut(ac_note),
        )
        self.wait(0.3)

        # === ACTOR ===
        actor_label = Text("Actor: objetivo y gradiente determinista", font_size=28, color=BLUE)
        actor_label.move_to(UP * 2.5)

        objective_eq = MathTex(
            r"J(\boldsymbol{\theta}_{\mu}) = \mathbb{E}_{\mathbf{x}\sim\rho^{\beta}}"
            r"\left[Q_{\mu}(\mathbf{x}, \mu(\mathbf{x}; \boldsymbol{\theta}_{\mu}))\right]",
            font_size=24,
        )
        shrink_to_fit_width(objective_eq, config.frame_width - 1.5)
        objective_eq.next_to(actor_label, DOWN, buff=0.5)

        objective_box = make_box(objective_eq)

        self.play(FadeIn(actor_label), FadeIn(objective_box), FadeIn(objective_eq))
        self.wait(0.5)
        self.next_slide()

        grad_eq = MathTex(
            r"\nabla_{\boldsymbol{\theta}_{\mu}}J(\boldsymbol{\theta}_{\mu})"
            r"= \mathbb{E}_{\mathbf{x}\sim \rho^{\beta}}\left["
            r"\nabla_{\mathbf{u}}Q(\mathbf{x}, \mathbf{u})"
            r"\nabla \mu(\mathbf{x};\boldsymbol{\theta}_{\mu})"
            r"\big|_{\mathbf{u}=\mu(\mathbf{x};\boldsymbol{\theta}_{\mu})}\right]",
            font_size=22,
        )
        shrink_to_fit_width(grad_eq, config.frame_width - 1.5)
        grad_eq.next_to(objective_box, DOWN, buff=0.45)

        self.play(FadeIn(grad_eq))
        self.wait(0.5)
        self.next_slide()

        update_eq = MathTex(
            r"\boldsymbol{\theta}^{(k+1)}_{\mu} = \boldsymbol{\theta}^{(k)}_{\mu}"
            r" + \alpha_{\mu}\nabla_{\boldsymbol{\theta}_{\mu}}J\left(\boldsymbol{\theta}_{\mu}^{(k)}\right)",
            font_size=26,
            color=GREEN,
        )
        update_eq.next_to(grad_eq, DOWN, buff=0.45)

        self.play(FadeIn(update_eq))
        self.wait(0.5)
        self.next_slide()

        self.play(
            FadeOut(actor_label),
            FadeOut(objective_box),
            FadeOut(objective_eq),
            FadeOut(grad_eq),
            FadeOut(update_eq),
        )
        self.wait(0.3)

        # === CRITICO ===
        critic_label = Text("Crítico: aproximación de Q", font_size=30, color=BLUE)
        critic_label.move_to(UP * 2.5)

        q_approx = MathTex(
            r"Q(\mathbf{x}, \mathbf{u}; \boldsymbol{\theta}_{Q}) \approx Q_{\mu}(\mathbf{x}, \mathbf{u})",
            font_size=30,
            color=ORANGE,
        )
        q_approx.next_to(critic_label, DOWN, buff=0.45)

        self.play(FadeIn(critic_label), FadeIn(q_approx))
        self.wait(0.5)
        self.next_slide()

        critic_loss = MathTex(
            r"\mathcal{L}\left(\boldsymbol{\theta}_Q\right)"
            r"= \mathbb{E}_{(\mathbf{x}, \mathbf{u}, r, \mathbf{x}')\sim U(\mathcal{D})}"
            r"\left[\left(r + \gamma Q\left(\mathbf{x}', \mu\left(\mathbf{x}';\bar{\boldsymbol{\theta}}_{\mu}\right);"
            r"\bar{\boldsymbol{\theta}}_{Q}\right) - Q\left(\mathbf{x}, \mathbf{u};\boldsymbol{\theta}_{Q}\right)\right)^2\right]",
            font_size=22,
        )
        shrink_to_fit_width(critic_loss, config.frame_width - 1.5)
        critic_loss.next_to(q_approx, DOWN, buff=0.45)

        critic_box = make_box(critic_loss)

        self.play(FadeIn(critic_box), FadeIn(critic_loss))
        self.wait(0.5)
        self.next_slide()

        critic_update = MathTex(
            r"\boldsymbol{\theta}_Q^{(k+1)} = \boldsymbol{\theta}_{Q}^{(k)}"
            r" - \alpha_{Q}\nabla_{\boldsymbol{\theta}_{Q}} \mathcal{L}\left(\boldsymbol{\theta}_{Q}^{(k)}\right)",
            font_size=24,
            color=GREEN,
        )
        critic_update.next_to(critic_box, DOWN, buff=0.45)

        self.play(FadeIn(critic_update))
        self.wait(0.5)
        self.next_slide()

        self.play(
            FadeOut(critic_label),
            FadeOut(q_approx),
            FadeOut(critic_box),
            FadeOut(critic_loss),
            FadeOut(critic_update),
        )
        self.wait(0.3)

        # === ESTABILIZACION ===
        stab_label = Text("Exploración y estabilización", font_size=30, color=BLUE)
        stab_label.move_to(UP * 2.5)

        noisy_eq = MathTex(
            r"\mathbf{u}_t = \mu(\mathbf{x}_t;\boldsymbol{\theta}_{\mu}) + \mathcal{O}_t",
            font_size=30,
            color=ORANGE,
        )
        noisy_eq.next_to(stab_label, DOWN, buff=0.45)

        stab_items = VGroup(
            Text("• Replay buffer: reutiliza experiencias", font_size=22, color=WHITE),
            Text("• Muestreo uniforme: rompe correlación temporal", font_size=22, color=WHITE),
            Text("• Redes objetivo: estabilizan el valor de referencia", font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        stab_items.next_to(noisy_eq, DOWN, buff=0.45)

        stab_group = VGroup(noisy_eq, stab_items)
        stab_box = make_box(stab_group)

        self.play(FadeIn(stab_label), FadeIn(stab_box), FadeIn(stab_group))
        self.wait(0.5)
        self.next_slide()

        soft_q = MathTex(
            r"\bar{\boldsymbol{\theta}}_{Q}^{(k+1)} = \tau \boldsymbol{\theta}_{Q}^{(k+1)}"
            r" +(1-\tau)\bar{\boldsymbol{\theta}}_{Q}^{(k)}",
            font_size=24,
        )
        soft_mu = MathTex(
            r"\bar{\boldsymbol{\theta}}_{\mu}^{(k+1)} = \tau \boldsymbol{\theta}_{\mu}^{(k+1)}"
            r" +(1-\tau)\bar{\boldsymbol{\theta}}_{\mu}^{(k)}",
            font_size=24,
        )
        soft_updates = VGroup(soft_q, soft_mu).arrange(DOWN, buff=0.2)
        shrink_to_fit_width(soft_updates, config.frame_width - 1.6)
        soft_updates.next_to(stab_box, DOWN, buff=0.4)

        self.play(FadeIn(soft_updates))
        self.wait(0.5)
        self.next_slide()

        self.play(
            FadeOut(stab_label),
            FadeOut(stab_box),
            FadeOut(stab_group),
            FadeOut(soft_updates),
        )
        self.wait(0.3)

        # === ALGORITMO FINAL ===
        alg_label = Text("Algoritmo DDPG", font_size=30, color=BLUE)
        alg_label.move_to(UP * 2.5)

        setup_lines = VGroup(
            MathTex(r"\text{1. Inicializar actor y cr\'itico aleatoriamente}", font_size=22),
            MathTex(r"\text{2. Copiar par\'ametros a redes objetivo}", font_size=22),
            MathTex(r"\text{3. Inicializar replay buffer } \mathcal{D}", font_size=22),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        setup_lines.next_to(alg_label, DOWN, buff=0.45)

        setup_box = make_box(setup_lines)

        self.play(FadeIn(alg_label), FadeIn(setup_box), FadeIn(setup_lines))
        self.wait(0.5)
        self.next_slide()

        loop_lines = VGroup(
            MathTex(r"\text{4. Para cada episodio:}", font_size=22, color=GREEN),
            MathTex(r"\bullet \ \text{Inicializar ruido } \mathcal{O} \text{ y recibir } \mathbf{x}_1", font_size=21),
            MathTex(
                r"\bullet \ \mathbf{u}_t = \mu(\mathbf{x}_t;\boldsymbol{\theta}_{\mu}) + \mathcal{O}_t",
                font_size=21,
            ),
            MathTex(
                r"\bullet \ ( \mathbf{x}_t, \mathbf{u}_t, r_t, \mathbf{x}_{t+1}) \rightarrow \mathcal{D}",
                font_size=21,
            ),
            MathTex(r"\bullet \ \text{Muestrear mini-lote de tama\~no } N \text{ desde } \mathcal{D}", font_size=21),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        loop_lines.next_to(alg_label, DOWN, buff=0.45)

        loop_box = make_box(loop_lines)

        self.play(FadeOut(setup_box), FadeOut(setup_lines))
        self.wait(0.2)
        self.play(FadeIn(loop_box), FadeIn(loop_lines))
        self.wait(0.5)
        self.next_slide()

        target_eq = MathTex(
            r"y_i = r_i + \gamma Q\left(\mathbf{x}_{i+1},"
            r"\mu\left(\mathbf{x}_{i+1};\bar{\boldsymbol{\theta}}_{\mu}\right);\bar{\boldsymbol{\theta}}_{Q}\right)",
            font_size=21,
        )
        shrink_to_fit_width(target_eq, config.frame_width - 1.6)

        loss_eq = MathTex(
            r"\mathcal{L} = \frac{1}{N}\sum_i \left(y_i -Q(\mathbf{x}_i, \mathbf{u}_i;\boldsymbol{\theta}_{Q})\right)^2",
            font_size=21,
        )
        shrink_to_fit_width(loss_eq, config.frame_width - 1.6)

        update_group = VGroup(target_eq, loss_eq).arrange(DOWN, buff=0.22)
        update_group.next_to(alg_label, DOWN, buff=0.5)
        update_box = make_box(update_group, color=YELLOW, fill_opacity=0.1, stroke_width=2)

        self.play(FadeOut(loop_box), FadeOut(loop_lines))
        self.wait(0.2)
        self.play(FadeIn(update_box), FadeIn(update_group))
        self.wait(0.5)
        self.next_slide()

        actor_grad = MathTex(
            r"\nabla_{\boldsymbol{\theta}_{\mu}} J \approx \frac{1}{N}\sum_{i}"
            r"\nabla_{\mathbf{u}}Q(\mathbf{x},\mathbf{u};\boldsymbol{\theta}_{Q})"
            r"\Big|_{\mathbf{x}=\mathbf{x}_i,\, \mathbf{u}= \mu(\mathbf{x}_i)}"
            r"\nabla_{\boldsymbol{\theta}_{\mu}}\mu(\mathbf{x};\boldsymbol{\theta}_{\mu})\Big|_{\mathbf{x}=\mathbf{x}_i}",
            font_size=19,
        )
        shrink_to_fit_width(actor_grad, config.frame_width - 1.6)
        actor_grad.next_to(alg_label, DOWN, buff=0.85)
        actor_grad_box = make_box(actor_grad, color=GRAY, fill_opacity=0.15, stroke_width=1)

        self.play(FadeOut(update_box), FadeOut(update_group))
        self.wait(0.2)
        self.play(FadeIn(actor_grad_box), FadeIn(actor_grad))
        self.wait(0.5)
        self.next_slide()

        final_updates = VGroup(
            MathTex(
                r"\bar{\boldsymbol{\theta}}_{Q} \leftarrow \tau \boldsymbol{\theta}_{Q}"
                r" +(1-\tau)\bar{\boldsymbol{\theta}}_{Q}",
                font_size=22,
            ),
            MathTex(
                r"\bar{\boldsymbol{\theta}}_{\mu} \leftarrow \tau \boldsymbol{\theta}_{\mu}"
                r" +(1-\tau)\bar{\boldsymbol{\theta}}_{\mu}",
                font_size=22,
            ),
        ).arrange(DOWN, buff=0.18)

        closing_note = Text(
            "Actor, crítico y redes objetivo se optimizan de forma acoplada",
            font_size=20,
            color=YELLOW,
        )
        closing_group = VGroup(final_updates, closing_note).arrange(DOWN, buff=0.3)
        closing_group.next_to(alg_label, DOWN, buff=0.85)
        closing_box = make_box(closing_group, color=GRAY, fill_opacity=0.15, stroke_width=1)

        self.play(FadeOut(actor_grad_box), FadeOut(actor_grad))
        self.wait(0.2)
        self.play(FadeIn(closing_box), FadeIn(closing_group))
        self.wait(0.5)
        self.next_slide()

        self.wait(1)
