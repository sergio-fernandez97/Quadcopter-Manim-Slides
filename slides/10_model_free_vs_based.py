"""
Model-free vs Model-based RL comparison slide.

Example:
    uv run manim-slides render slides/10_model_free_vs_based.py ModelFreeVsModelBasedSlide

Author: Sergio Fernández
"""

from manim import *
from manim_slides import Slide


class ModelFreeVsModelBasedSlide(Slide):
    def construct(self):
        # Colors
        MODEL_FREE = GREEN
        MODEL_BASED = BLUE
        SHARED = YELLOW

        # === TITLE ===
        title = Text("Model-free vs Model-based RL", font_size=42, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))
        self.wait(0.5)
        self.next_slide()

        # === DIAGRAM BOXES (LEFT SIDE) ===
        # Experiencia (top)
        exp_box = Rectangle(width=2.8, height=1.0, color=SHARED, stroke_width=2)
        exp_label = Text("Experiencia", font_size=22, color=WHITE)
        exp_label.move_to(exp_box)
        experiencia = VGroup(exp_box, exp_label).move_to(LEFT * 2.5 + UP * 1.2)

        # Valor/Política (bottom)
        valor_box = Rectangle(width=2.8, height=1.0, color=SHARED, stroke_width=2)
        valor_label = Text("Valor/Política", font_size=22, color=WHITE)
        valor_label.move_to(valor_box)
        valor_politica = VGroup(valor_box, valor_label).move_to(LEFT * 2.5 + DOWN * 1.5)

        # Modelo (left, shown later)
        modelo_box = Rectangle(
            width=2.2, height=1.0, color=MODEL_BASED, stroke_width=2, fill_opacity=0.1
        )
        modelo_label = Text("Modelo", font_size=22, color=MODEL_BASED, weight=BOLD)
        modelo_label.move_to(modelo_box)
        modelo = VGroup(modelo_box, modelo_label).move_to(LEFT * 5 + DOWN * 0.2)

        # Show shared boxes
        self.play(FadeIn(experiencia), FadeIn(valor_politica))
        self.wait(0.5)
        self.next_slide()

        # === MODEL-FREE PATH (GREEN) ===
        # Arrow: Experiencia → Valor/Política
        arrow_exp_valor = Arrow(
            experiencia.get_bottom(),
            valor_politica.get_top(),
            color=MODEL_FREE,
            stroke_width=3,
            buff=0.1,
        )
        label_sin_modelos = Text(
            "Aprendizaje\nsin modelos", font_size=16, color=MODEL_FREE
        )
        label_sin_modelos.next_to(arrow_exp_valor, RIGHT, buff=0.15)

        # Curved arrow: Valor/Política → Experiencia (Actuación) - on the RIGHT side
        arrow_actuacion = CurvedArrow(
            valor_politica.get_right() + UP * 0.2,
            experiencia.get_right() + DOWN * 0.2,
            color=SHARED,
            angle=TAU / 4,
            stroke_width=3,
        )
        label_actuacion = Text("Actuación", font_size=16, color=WHITE)
        label_actuacion.next_to(arrow_actuacion, RIGHT, buff=0.1)

        self.play(
            Create(arrow_exp_valor),
            FadeIn(label_sin_modelos),
            Create(arrow_actuacion),
            FadeIn(label_actuacion),
        )
        self.wait(0.5)
        self.next_slide()

        # Model-free text (RIGHT SIDE)
        mf_heading = Text("Model-free RL", font_size=28, color=MODEL_FREE, weight=BOLD)
        mf_points = BulletedList(
            "Optimiza políticas por experiencia",
            "Estrategia de prueba y error",
            "No usa modelo de la dinámica",
            font_size=18,
            color=MODEL_FREE,
            buff=0.2,
        )

        mf_group = VGroup(mf_heading, mf_points).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        mf_group.move_to(RIGHT * 3.5 + UP * 1.5)

        self.play(FadeIn(mf_group))
        self.wait(1)
        self.next_slide()

        # === MODEL-BASED PATH (BLUE) ===
        # Show Modelo box
        self.play(FadeIn(modelo))
        self.wait(0.3)

        # Curved arrow: Experiencia → Modelo (Aprendizaje basado en modelos)
        arrow_modelo_exp = CurvedArrow(
            experiencia.get_left() + DOWN * 0.2,
            modelo.get_top() + RIGHT * 0.3,
            color=MODEL_BASED,
            angle=TAU / 6,
            stroke_width=2,
        )
        label_basado = Text(
            "Aprendizaje\nbasado en modelos", font_size=14, color=MODEL_BASED
        )
        label_basado.next_to(arrow_modelo_exp, UP, buff=0.05)

        # Arrow: Modelo → Valor/Política (Planeación) - on the right side of Modelo
        arrow_planeacion = CurvedArrow(
            modelo.get_bottom() + RIGHT * 0.3,
            valor_politica.get_left() + UP * 0.2,
            color=MODEL_BASED,
            angle=TAU / 6,
            stroke_width=2,
        )
        label_planeacion = Text("Planeación", font_size=14, color=MODEL_BASED)
        label_planeacion.next_to(arrow_planeacion, LEFT, buff=0.05)

        self.play(
            Create(arrow_modelo_exp),
            FadeIn(label_basado),
            Create(arrow_planeacion),
            FadeIn(label_planeacion),
        )
        self.wait(0.5)
        self.next_slide()

        # Model-based text (RIGHT SIDE, below model-free)
        mb_heading = Text(
            "Model-based RL", font_size=28, color=MODEL_BASED, weight=BOLD
        )
        mb_points = BulletedList(
            "Usa modelo aprendido o conocido",
            "Aproxima valor/política global",
            "Combina planificación y aprendizaje",
            font_size=18,
            color=MODEL_BASED,
            buff=0.2,
        )

        mb_group = VGroup(mb_heading, mb_points).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        mb_group.move_to(RIGHT * 3.5 + DOWN * 1.2)

        self.play(FadeIn(mb_group))
        self.wait(1)
