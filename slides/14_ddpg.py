"""
DDPG slide: actor-critic overview, main equations, stabilization mechanisms,
and the training algorithm for continuous control.

Example:
    uv run manim-slides render slides/14_ddpg.py DDPGSlide
"""

from pathlib import Path

import numpy as np
from PIL import Image

from manim import *
from manim_slides import Slide


DDPG_SCHEMA = (
    Path(__file__).resolve().parent.parent
    / "LaTex/figures/06_aplicacion_y_evaluacion_de_metodos_rl/ddpg_algorithm.png"
)

ACTOR_CRITIC_SCHEMA = (
    Path(__file__).resolve().parent.parent
    / "LaTex/figures/05_aprendizaje_por_diferencias_temporales/actor_critic.png"
)


def load_inverted(path):
    arr = np.array(Image.open(str(path)).convert("RGB"))
    return ImageMobject(255 - arr)


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
        motivation_group.move_to(LEFT * 3.0 + UP * 0.6)
        motivation_box = make_box(motivation_group)

        # Actor-critic figure (inverted) on the right
        ac_diagram = load_inverted(ACTOR_CRITIC_SCHEMA)
        ac_diagram.scale_to_fit_width(4.5)
        ac_diagram.move_to(RIGHT * 2.8 + UP * 0.3)

        actor_ann_note = Text("Actor: ANN que propone la acción", font_size=20, color=GREEN)
        critic_ann_note = Text("Crítico: ANN que estima Q(x,u)", font_size=20, color=ORANGE)
        ann_notes = VGroup(actor_ann_note, critic_ann_note).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        ann_notes.next_to(ac_diagram, DOWN, buff=0.25)

        self.play(FadeIn(motivation_box), FadeIn(motivation_group))
        self.wait(0.5)
        self.next_slide()

        self.play(FadeIn(ac_diagram), FadeIn(ann_notes))
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
            FadeOut(ac_diagram),
            FadeOut(ann_notes),
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

        ac_schema_img = load_inverted(ACTOR_CRITIC_SCHEMA)
        ac_schema_img.scale_to_fit_width(6.0)
        ac_schema_img.move_to(LEFT * 2.4 + DOWN * 0.2)

        diagram_frame = SurroundingRectangle(ac_schema_img, color=GRAY, buff=0.12, stroke_width=1)

        ac_def_box = RoundedRectangle(
            corner_radius=0.2,
            width=3.9,
            height=2.7,
            color=GRAY,
            fill_opacity=0.15,
            stroke_width=1,
        )
        ac_def_box.move_to(RIGHT * 3.4 + DOWN * 0.15)

        ac_def_items = VGroup(
            Text("Actor:", font_size=24, color=GREEN),
            MathTex(r"\mu(\mathbf{x}; \boldsymbol{\theta}_{\mu})", font_size=28, color=WHITE),
            Text("Política determinista", font_size=20, color=GRAY_B),
            Text("Selecciona acciones continuas", font_size=20, color=GRAY_B),
            Text("Crítico:", font_size=24, color=ORANGE),
            MathTex(r"Q(\mathbf{x}, \mathbf{u}; \boldsymbol{\theta}_{Q})", font_size=28, color=WHITE),
            Text("Evalúa la acción y genera error TD", font_size=20, color=GRAY_B),
        ).arrange(DOWN, buff=0.12)
        ac_def_items.move_to(ac_def_box)

        self.play(
            FadeIn(ac_label),
            FadeIn(diagram_frame),
            FadeIn(ac_schema_img),
            FadeIn(ac_def_box),
            FadeIn(ac_def_items),
        )
        self.wait(0.5)
        self.next_slide()

        ac_note = Text(
            "El actor propone acciones; el crítico retroalimenta su calidad",
            font_size=20,
            color=YELLOW,
        )
        ac_note.next_to(VGroup(diagram_frame, ac_def_box), DOWN, buff=0.35)

        self.play(FadeIn(ac_note))
        self.wait(0.5)
        self.next_slide()

        self.play(
            FadeOut(ac_label),
            FadeOut(diagram_frame),
            FadeOut(ac_schema_img),
            FadeOut(ac_def_box),
            FadeOut(ac_def_items),
            FadeOut(ac_note),
        )
        self.wait(0.3)

        # === ACTOR vs CRITICO (two-column) ===
        col_max_width = config.frame_width / 2 - 0.8

        # --- Left column: Actor ---
        actor_label = Text("Actor", font_size=28, color=GREEN)
        actor_label.move_to(LEFT * 3.0 + UP * 2.5)

        objective_eq = MathTex(
            r"J(\boldsymbol{\theta}_{\mu}) = \mathbb{E}_{\mathbf{x}\sim\rho^{\beta}}"
            r"\left[Q_{\mu}(\mathbf{x}, \mu(\mathbf{x}; \boldsymbol{\theta}_{\mu}))\right]",
            font_size=22,
        )
        shrink_to_fit_width(objective_eq, col_max_width)
        objective_eq.next_to(actor_label, DOWN, buff=0.4)
        objective_box = make_box(objective_eq)

        # FadeIn actor label + objective first
        self.play(FadeIn(actor_label), FadeIn(objective_box), FadeIn(objective_eq))
        self.wait(0.5)
        self.next_slide()

        grad_eq = MathTex(
            r"\nabla_{\boldsymbol{\theta}_{\mu}}J(\boldsymbol{\theta}_{\mu})"
            r"= \mathbb{E}_{\mathbf{x}\sim \rho^{\beta}}\left["
            r"\nabla_{\mathbf{u}}Q(\mathbf{x}, \mathbf{u})"
            r"\nabla \mu(\mathbf{x};\boldsymbol{\theta}_{\mu})"
            r"\big|_{\mathbf{u}=\mu(\mathbf{x};\boldsymbol{\theta}_{\mu})}\right]",
            font_size=18,
        )
        shrink_to_fit_width(grad_eq, col_max_width)
        grad_eq.next_to(objective_box, DOWN, buff=0.3)

        update_eq = MathTex(
            r"\boldsymbol{\theta}^{(k+1)}_{\mu} = \boldsymbol{\theta}^{(k)}_{\mu}"
            r" + \alpha_{\mu}\nabla_{\boldsymbol{\theta}_{\mu}}J\left(\boldsymbol{\theta}_{\mu}^{(k)}\right)",
            font_size=20,
            color=GREEN,
        )
        shrink_to_fit_width(update_eq, col_max_width)
        update_eq.next_to(grad_eq, DOWN, buff=0.3)

        self.play(FadeIn(grad_eq), FadeIn(update_eq))
        self.wait(0.5)
        self.next_slide()

        # --- Right column: Critic ---
        critic_label = Text("Crítico", font_size=28, color=ORANGE)
        critic_label.move_to(RIGHT * 3.0 + UP * 2.5)

        q_approx = MathTex(
            r"Q(\mathbf{x}, \mathbf{u}; \boldsymbol{\theta}_{Q}) \approx Q_{\mu}(\mathbf{x}, \mathbf{u})",
            font_size=20,
            color=ORANGE,
        )
        shrink_to_fit_width(q_approx, col_max_width)
        q_approx.next_to(critic_label, DOWN, buff=0.4)

        critic_loss = MathTex(
            r"\mathcal{L}\left(\boldsymbol{\theta}_Q\right)"
            r"= \mathbb{E}_{(\mathbf{x}, \mathbf{u}, r, \mathbf{x}')\sim U(\mathcal{D})}"
            r"\left[\left(r + \gamma Q\left(\mathbf{x}', \mu\left(\mathbf{x}';\bar{\boldsymbol{\theta}}_{\mu}\right);"
            r"\bar{\boldsymbol{\theta}}_{Q}\right) - Q\left(\mathbf{x}, \mathbf{u};\boldsymbol{\theta}_{Q}\right)\right)^2\right]",
            font_size=16,
        )
        shrink_to_fit_width(critic_loss, col_max_width)
        critic_loss.next_to(q_approx, DOWN, buff=0.3)
        critic_box = make_box(critic_loss)

        critic_update = MathTex(
            r"\boldsymbol{\theta}_Q^{(k+1)} = \boldsymbol{\theta}_{Q}^{(k)}"
            r" - \alpha_{Q}\nabla_{\boldsymbol{\theta}_{Q}} \mathcal{L}\left(\boldsymbol{\theta}_{Q}^{(k)}\right)",
            font_size=20,
            color=GREEN,
        )
        shrink_to_fit_width(critic_update, col_max_width)
        critic_update.next_to(critic_box, DOWN, buff=0.3)

        self.play(
            FadeIn(critic_label),
            FadeIn(q_approx),
            FadeIn(critic_box),
            FadeIn(critic_loss),
            FadeIn(critic_update),
        )
        self.wait(0.5)
        self.next_slide()

        self.play(
            FadeOut(actor_label),
            FadeOut(objective_box),
            FadeOut(objective_eq),
            FadeOut(grad_eq),
            FadeOut(update_eq),
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

        # 1. Replay buffer section
        replay_items = VGroup(
            Text("• Replay buffer: almacena transiciones en", font_size=22, color=WHITE),
            MathTex(r"\mathcal{D}", font_size=22, color=WHITE),
            Text("• Muestreo uniforme de", font_size=22, color=WHITE),
            MathTex(r"\mathcal{D}", font_size=22, color=WHITE),
            Text(": rompe correlación temporal", font_size=22, color=WHITE),
        )
        replay_bullet1 = VGroup(replay_items[0], replay_items[1]).arrange(RIGHT, buff=0.1)
        replay_bullet2 = VGroup(replay_items[2], replay_items[3], replay_items[4]).arrange(RIGHT, buff=0.1)
        replay_list = VGroup(replay_bullet1, replay_bullet2).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        replay_list.next_to(stab_label, DOWN, buff=0.4)

        experience_eq = MathTex(
            r"e_t = (\mathbf{x}_t,\mathbf{u}_t,r_{t+1},\mathbf{x}_{t+1})",
            font_size=26,
            color=GREEN,
        )
        shrink_to_fit_width(experience_eq, config.frame_width - 1.5)
        experience_eq.next_to(replay_list, DOWN, buff=0.35)
        experience_box = make_box(experience_eq)

        self.play(FadeIn(stab_label), FadeIn(replay_list), FadeIn(experience_box), FadeIn(experience_eq))
        self.wait(0.5)
        self.next_slide()

        # 2. Noisy policy exploration
        noisy_eq = MathTex(
            r"\mathbf{u}_t = \mu(\mathbf{x}_t;\boldsymbol{\theta}_{\mu}) + \mathcal{O}_t",
            font_size=30,
            color=ORANGE,
        )
        noisy_eq.next_to(experience_box, DOWN, buff=0.4)

        ou_note = Text(
            "Ruido ℴ_t (Ornstein-Uhlenbeck) favorece la exploración",
            font_size=20,
            color=GRAY_B,
        )
        ou_note.next_to(noisy_eq, DOWN, buff=0.2)

        self.play(FadeIn(noisy_eq), FadeIn(ou_note))
        self.wait(0.5)
        self.next_slide()

        # 3. Soft target updates
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
        soft_updates.next_to(ou_note, DOWN, buff=0.35)
        soft_box = make_box(soft_updates, color=YELLOW, fill_opacity=0.1, stroke_width=2)

        self.play(FadeIn(soft_box), FadeIn(soft_updates))
        self.wait(0.5)
        self.next_slide()

        self.play(
            FadeOut(stab_label),
            FadeOut(replay_list),
            FadeOut(experience_box),
            FadeOut(experience_eq),
            FadeOut(noisy_eq),
            FadeOut(ou_note),
            FadeOut(soft_box),
            FadeOut(soft_updates),
        )
        self.wait(0.3)

        # === ALGORITMO FINAL (two-column: diagram + steps) ===
        alg_label = Text("Algoritmo DDPG", font_size=30, color=BLUE)
        alg_label.move_to(UP * 2.5)

        # Left: inverted ddpg_algorithm.png
        alg_diagram = load_inverted(DDPG_SCHEMA)
        alg_diagram.scale_to_fit_width(6.2)
        alg_diagram.move_to(LEFT * 3.0 + DOWN * 0.3)
        alg_frame = SurroundingRectangle(alg_diagram, color=GRAY, buff=0.1, stroke_width=1)

        # Right: compact algorithm steps
        alg_steps = VGroup(
            MathTex(r"\text{1. Inicializar actor, cr\'itico y redes objetivo}", font_size=17),
            MathTex(r"\text{2. Inicializar buffer } \mathcal{D}", font_size=17),
            MathTex(r"\text{3. Por cada episodio:}", font_size=17, color=GREEN),
            MathTex(
                r"\quad \text{Observar } \mathbf{x}_t,\ \mathbf{u}_t = \mu + \mathcal{O}_t",
                font_size=17,
            ),
            MathTex(r"\quad \text{Almacenar } e_t \text{ en } \mathcal{D}", font_size=17),
            MathTex(r"\quad \text{Muestrear mini-lote } N", font_size=17),
            MathTex(
                r"\quad \text{Actualizar cr\'itico: } \min \mathcal{L}(\boldsymbol{\theta}_Q)",
                font_size=17,
            ),
            MathTex(
                r"\quad \text{Actualizar actor: } \max J(\boldsymbol{\theta}_{\mu})",
                font_size=17,
            ),
            MathTex(
                r"\quad \text{Soft update: } \bar{\boldsymbol{\theta}} \leftarrow"
                r" \tau\boldsymbol{\theta} + (1-\tau)\bar{\boldsymbol{\theta}}",
                font_size=17,
            ),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        shrink_to_fit_width(alg_steps, config.frame_width / 2 - 0.6)
        alg_steps.move_to(RIGHT * 2.8 + DOWN * 0.1)
        alg_steps_box = make_box(alg_steps, color=GRAY, fill_opacity=0.15, stroke_width=1)

        # Hyperparameters box below algorithm steps
        hyperparam_lines = VGroup(
            MathTex(r"N=128,\quad \gamma=0.99,\quad \tau=10^{-3}", font_size=16),
            MathTex(
                r"\text{Buffer: } 10^5,\quad 10 \text{ \'epocas},\quad K=5,\quad T=750",
                font_size=16,
            ),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        shrink_to_fit_width(hyperparam_lines, config.frame_width / 2 - 0.6)
        hyperparam_lines.next_to(alg_steps_box, DOWN, buff=0.3)
        hyperparam_box = make_box(
            hyperparam_lines, color=GRAY, fill_opacity=0.1, stroke_width=1
        )

        self.play(
            FadeIn(alg_label),
            FadeIn(alg_frame),
            FadeIn(alg_diagram),
            FadeIn(alg_steps_box),
            FadeIn(alg_steps),
            FadeIn(hyperparam_box),
            FadeIn(hyperparam_lines),
        )
        self.wait(0.5)
        self.next_slide()

        self.wait(1)
